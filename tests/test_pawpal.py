import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from datetime import datetime
from pawpal_system import Task, Pet


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
