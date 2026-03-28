import json
import os
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List

DATA_FILE = os.path.join(os.path.dirname(__file__), "data.json")


def save_owners(owners: dict):
    """Save all owners (and their pets/tasks) to data.json.

    Args:
        owners: The st.session_state.owners dict mapping owner name -> Owner.
    """
    data = {name: owner.to_dict() for name, owner in owners.items()}
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


def load_owners() -> dict:
    """Load owners from data.json and return them as a dict of Owner objects.

    Returns an empty dict if the file does not exist yet.
    """
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
    return {name: Owner.from_dict(owner_data) for name, owner_data in data.items()}


@dataclass
class Task:
    taskName: str
    dueTime: datetime
    frequency: str
    priority: int
    petName: str
    completed: bool = False

    def markComplete(self):
        """Mark this task as completed."""
        self.completed = True

    def to_dict(self) -> dict:
        """Convert this Task to a plain dictionary for JSON serialization."""
        return {
            "taskName": self.taskName,
            "dueTime": self.dueTime.isoformat(),
            "frequency": self.frequency,
            "priority": self.priority,
            "petName": self.petName,
            "completed": self.completed,
        }

    @staticmethod
    def from_dict(data: dict) -> "Task":
        """Reconstruct a Task from a dictionary loaded from JSON."""
        return Task(
            taskName=data["taskName"],
            dueTime=datetime.fromisoformat(data["dueTime"]),
            frequency=data["frequency"],
            priority=data["priority"],
            petName=data["petName"],
            completed=data["completed"],
        )

    def getDetails(self):
        """Return a formatted string summary of the task's details and status."""
        status = "Completed" if self.completed else "Pending"
        return (
            f"Task: {self.taskName}\n"
            f"Pet: {self.petName}\n"
            f"Due: {self.dueTime}\n"
            f"Frequency: {self.frequency}\n"
            f"Priority: {self.priority}\n"
            f"Status: {status}"
        )


@dataclass
class Pet:
    petName: str
    type: str
    breed: str
    dateOfBirth: datetime
    allergies: str
    medicalNotes: str
    tasks: List[Task] = field(default_factory=list)

    def addTask(self, task: Task):
        """Add a task to this pet's task list."""
        self.tasks.append(task)

    def getTasks(self) -> List[Task]:
        """Return all tasks assigned to this pet."""
        return self.tasks

    def to_dict(self) -> dict:
        """Convert this Pet to a plain dictionary for JSON serialization."""
        return {
            "petName": self.petName,
            "type": self.type,
            "breed": self.breed,
            "dateOfBirth": self.dateOfBirth.isoformat(),
            "allergies": self.allergies,
            "medicalNotes": self.medicalNotes,
            "tasks": [task.to_dict() for task in self.tasks],
        }

    @staticmethod
    def from_dict(data: dict) -> "Pet":
        """Reconstruct a Pet (and its tasks) from a dictionary loaded from JSON."""
        pet = Pet(
            petName=data["petName"],
            type=data["type"],
            breed=data["breed"],
            dateOfBirth=datetime.fromisoformat(data["dateOfBirth"]),
            allergies=data["allergies"],
            medicalNotes=data["medicalNotes"],
        )
        for task_data in data.get("tasks", []):
            pet.addTask(Task.from_dict(task_data))
        return pet


@dataclass
class Owner:
    ownerName: str
    phone: str
    address: str
    emergencyContact: str
    pets: List[Pet] = field(default_factory=list)

    def addPet(self, pet: Pet):
        """Add a pet to this owner's pet list."""
        self.pets.append(pet)

    def getPets(self) -> List[Pet]:
        """Return all pets belonging to this owner."""
        return self.pets

    def to_dict(self) -> dict:
        """Convert this Owner to a plain dictionary for JSON serialization."""
        return {
            "ownerName": self.ownerName,
            "phone": self.phone,
            "address": self.address,
            "emergencyContact": self.emergencyContact,
            "pets": [pet.to_dict() for pet in self.pets],
        }

    @staticmethod
    def from_dict(data: dict) -> "Owner":
        """Reconstruct an Owner (with pets and tasks) from a dictionary loaded from JSON."""
        owner = Owner(
            ownerName=data["ownerName"],
            phone=data["phone"],
            address=data["address"],
            emergencyContact=data["emergencyContact"],
        )
        for pet_data in data.get("pets", []):
            owner.addPet(Pet.from_dict(pet_data))
        return owner


class Scheduler:
    def __init__(self, owner: Owner):
        self.owner: Owner = owner
        self.allTasks: List[Task] = []

    def collectTasks(self):
        """Gather all tasks from every pet under the owner into allTasks."""
        self.allTasks = []
        for pet in self.owner.getPets():
            for task in pet.getTasks():
                self.allTasks.append(task)

    def sortByTime(self):
        """Sort allTasks by priority first, then by dueTime within each priority level.

        Lower priority numbers mean higher urgency (1 = high, 2 = medium, 3 = low),
        so the most urgent tasks always appear first regardless of their scheduled time.
        Within the same priority level, earlier tasks come first.
        Modifies allTasks in place — does not return a new list.
        """
        self.allTasks.sort(key=lambda task: (task.priority, task.dueTime))

    def markTaskComplete(self, task: Task):
        """Mark a task complete and schedule the next occurrence if Daily or Weekly.

        Steps:
          1. Sets task.completed = True on the given task.
          2. Checks task.frequency (case-insensitive).
          3. For "daily", creates a copy of the task due tomorrow.
          4. For "weekly", creates a copy of the task due 7 days later.
          5. For "once" or "monthly", stops — no next occurrence is created.
          6. Adds the new task to the correct Pet, then refreshes allTasks.

        Args:
            task: The Task object to mark as complete.
        """
        task.markComplete()

        frequency = task.frequency.lower()
        if frequency == "daily":
            delta = timedelta(days=1)
        elif frequency == "weekly":
            delta = timedelta(weeks=1)
        else:
            return  # "once" or "monthly" — no next occurrence needed

        next_task = Task(
            taskName=task.taskName,
            dueTime=task.dueTime + delta,
            frequency=task.frequency,
            priority=task.priority,
            petName=task.petName
        )

        for pet in self.owner.getPets():
            if pet.petName == task.petName:
                pet.addTask(next_task)
                break

        self.collectTasks()

    def filterByPet(self, petName: str) -> List[Task]:
        """Return only tasks that belong to the given pet name.

        Does not modify allTasks — returns a new filtered list.

        Args:
            petName: The name of the pet to filter by (must match task.petName exactly).

        Returns:
            A list of Task objects whose petName matches the given name.
            Returns an empty list if no tasks match.
        """
        return [task for task in self.allTasks if task.petName == petName]

    def filterByStatus(self, completed: bool) -> List[Task]:
        """Return only tasks matching the given completed status.

        Does not modify allTasks — returns a new filtered list.

        Args:
            completed: Pass False to get pending tasks, True to get completed tasks.

        Returns:
            A list of Task objects whose completed field matches the given value.
            Returns an empty list if no tasks match.
        """
        return [task for task in self.allTasks if task.completed == completed]

    def detectConflicts(self) -> List[str]:
        """Return warning messages for any tasks scheduled at the same time.

        Sorts tasks by time first, then checks only neighboring pairs.
        This is faster than comparing every task against every other task.
        """
        warnings = []
        sorted_tasks = sorted(self.allTasks, key=lambda task: task.dueTime)
        for i in range(len(sorted_tasks) - 1):
            a = sorted_tasks[i]
            b = sorted_tasks[i + 1]
            if a.dueTime == b.dueTime:
                warnings.append(
                    f"Warning: '{a.taskName}' ({a.petName}) and "
                    f"'{b.taskName}' ({b.petName}) are both scheduled at "
                    f"{a.dueTime.strftime('%I:%M %p')}"
                )
        return warnings

    def getDailySchedule(self) -> List[Task]:
        """Collect and sort all tasks, then return the full daily schedule."""
        self.collectTasks()
        self.sortByTime()
        return self.allTasks

    def findNextAvailableSlot(self, start_time: datetime, duration_minutes: int = 60) -> datetime:
        """Find the next open time slot starting from start_time.

        Collects and sorts all tasks, then checks whether start_time
        conflicts with any existing task. If it does, the method moves
        forward in 30-minute increments and keeps checking until it finds
        a time that is not already taken.

        Args:
            start_time: The earliest datetime to consider for the new slot.
            duration_minutes: How long the slot needs to be (default 60).
                              Currently used as context — simple conflict
                              check compares exact task times only.

        Returns:
            The first datetime starting at or after start_time that does
            not match any existing task's dueTime.
        """
        self.collectTasks()
        self.sortByTime()

        booked_times = {task.dueTime for task in self.allTasks}

        slot = start_time
        while slot in booked_times:
            slot += timedelta(minutes=30)

        return slot
