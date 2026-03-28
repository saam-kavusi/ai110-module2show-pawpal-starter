import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from datetime import datetime, timedelta
from pawpal_system import Task, Pet, Owner, Scheduler


# --- Helpers ---
# Shared setup used by Scheduler tests

def make_owner_with_pet(pet_name="Buddy"):
    """Create a minimal Owner with one Pet and return both."""
    owner = Owner(ownerName="Test Owner", phone="", address="", emergencyContact="")
    pet = Pet(
        petName=pet_name,
        type="Dog",
        breed="Lab",
        dateOfBirth=datetime(2020, 1, 1),
        allergies="None",
        medicalNotes=""
    )
    owner.addPet(pet)
    return owner, pet


def make_task(name, hour, frequency="once", priority=1, pet_name="Buddy"):
    """Create a Task due on a fixed date at the given hour."""
    return Task(
        taskName=name,
        dueTime=datetime(2026, 3, 27, hour, 0),
        frequency=frequency,
        priority=priority,
        petName=pet_name
    )


# --- Existing tests (unchanged) ---

def test_mark_complete_changes_status():
    task = Task(
        taskName="Feed Buddy",
        dueTime=datetime(2026, 3, 27, 8, 0),
        frequency="daily",
        priority=1,
        petName="Buddy"
    )
    assert task.completed == False
    task.markComplete()
    assert task.completed == True


def test_add_task_increases_pet_task_count():
    pet = Pet(
        petName="Buddy",
        type="Dog",
        breed="Labrador",
        dateOfBirth=datetime(2020, 5, 10),
        allergies="None",
        medicalNotes="Healthy"
    )
    task = Task(
        taskName="Walk Buddy",
        dueTime=datetime(2026, 3, 27, 9, 0),
        frequency="daily",
        priority=2,
        petName="Buddy"
    )
    assert len(pet.getTasks()) == 0
    pet.addTask(task)
    assert len(pet.getTasks()) == 1


# --- Phase 5 Step 2: New tests ---

def test_sort_orders_tasks_by_time():
    """Tasks added out of order should come out in chronological order after sortByTime."""
    owner, pet = make_owner_with_pet()
    pet.addTask(make_task("Evening Feed", hour=18))
    pet.addTask(make_task("Morning Walk", hour=7))
    pet.addTask(make_task("Flea Medicine", hour=9))

    scheduler = Scheduler(owner)
    scheduler.collectTasks()
    scheduler.sortByTime()

    hours = [task.dueTime.hour for task in scheduler.allTasks]
    assert hours == [7, 9, 18]


def test_sort_tie_breaks_by_priority():
    """When two tasks share the same time, the one with lower priority number comes first."""
    owner, pet = make_owner_with_pet()
    # Add priority=2 first to confirm sort is not just insertion order
    pet.addTask(make_task("Low Urgency", hour=7, priority=2))
    pet.addTask(make_task("High Urgency", hour=7, priority=1))

    scheduler = Scheduler(owner)
    scheduler.collectTasks()
    scheduler.sortByTime()

    assert scheduler.allTasks[0].taskName == "High Urgency"
    assert scheduler.allTasks[1].taskName == "Low Urgency"


def test_daily_task_creates_next_occurrence():
    """Completing a Daily task should add a new task due the following day."""
    owner, pet = make_owner_with_pet()
    original = make_task("Morning Walk", hour=7, frequency="Daily")
    pet.addTask(original)

    scheduler = Scheduler(owner)
    scheduler.collectTasks()
    scheduler.markTaskComplete(original)

    tasks = pet.getTasks()
    assert len(tasks) == 2
    assert original.completed == True

    next_task = tasks[1]
    assert next_task.completed == False
    assert next_task.dueTime == original.dueTime + timedelta(days=1)
    assert next_task.taskName == original.taskName


def test_weekly_task_creates_next_occurrence():
    """Completing a Weekly task should add a new task due 7 days later."""
    owner, pet = make_owner_with_pet()
    original = make_task("Bath Time", hour=10, frequency="Weekly")
    pet.addTask(original)

    scheduler = Scheduler(owner)
    scheduler.collectTasks()
    scheduler.markTaskComplete(original)

    tasks = pet.getTasks()
    assert len(tasks) == 2
    assert original.completed == True

    next_task = tasks[1]
    assert next_task.completed == False
    assert next_task.dueTime == original.dueTime + timedelta(weeks=1)
    assert next_task.taskName == original.taskName


def test_once_task_does_not_create_next_occurrence():
    """Completing a Once task should not create any new tasks."""
    owner, pet = make_owner_with_pet()
    task = make_task("Vet Visit", hour=14, frequency="Once")
    pet.addTask(task)

    scheduler = Scheduler(owner)
    scheduler.collectTasks()
    scheduler.markTaskComplete(task)

    assert len(pet.getTasks()) == 1
    assert task.completed == True


def test_detect_conflicts_finds_same_time_tasks():
    """Two tasks at the same time should produce one warning string."""
    owner, pet = make_owner_with_pet()
    pet.addTask(make_task("Morning Walk", hour=7))
    pet.addTask(make_task("Breakfast Feed", hour=7))

    scheduler = Scheduler(owner)
    scheduler.collectTasks()
    conflicts = scheduler.detectConflicts()

    assert len(conflicts) == 1
    assert "Morning Walk" in conflicts[0]
    assert "Breakfast Feed" in conflicts[0]


def test_detect_conflicts_empty_returns_empty_list():
    """detectConflicts on a scheduler with no tasks should return an empty list."""
    owner, pet = make_owner_with_pet()
    # No tasks added

    scheduler = Scheduler(owner)
    scheduler.collectTasks()

    assert scheduler.detectConflicts() == []


def test_filter_by_pet_no_match_returns_empty():
    """filterByPet with a name that doesn't exist should return [] not crash."""
    owner, _ = make_owner_with_pet("Buddy")
    owner.getPets()[0].addTask(make_task("Walk", hour=8))

    scheduler = Scheduler(owner)
    scheduler.collectTasks()

    assert scheduler.filterByPet("Ghost") == []


def test_filter_by_status_returns_completed_and_pending():
    """filterByStatus should split tasks correctly by their completed field."""
    owner, pet = make_owner_with_pet()
    task_a = make_task("Morning Walk", hour=7)
    task_b = make_task("Evening Feed", hour=18)
    pet.addTask(task_a)
    pet.addTask(task_b)

    task_a.markComplete()

    scheduler = Scheduler(owner)
    scheduler.collectTasks()

    completed = scheduler.filterByStatus(True)
    pending = scheduler.filterByStatus(False)

    assert len(completed) == 1
    assert completed[0].taskName == "Morning Walk"

    assert len(pending) == 1
    assert pending[0].taskName == "Evening Feed"
