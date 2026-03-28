from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List


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
        """Sort allTasks in ascending order by dueTime, then by priority if times match.

        Uses a tuple sort key so that when two tasks share the same dueTime,
        the one with the lower priority number (higher urgency) comes first.
        Modifies allTasks in place — does not return a new list.
        """
        self.allTasks.sort(key=lambda task: (task.dueTime, task.priority))

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
