from dataclasses import dataclass, field
from datetime import datetime
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
        """Sort allTasks in ascending order by dueTime."""
        self.allTasks.sort(key=lambda task: task.dueTime)

    def detectConflicts(self) -> List[Task]:
        """Return a list of tasks that share the same dueTime."""
        conflicts = []
        for i in range(len(self.allTasks)):
            for j in range(i + 1, len(self.allTasks)):
                if self.allTasks[i].dueTime == self.allTasks[j].dueTime:
                    if self.allTasks[i] not in conflicts:
                        conflicts.append(self.allTasks[i])
                    if self.allTasks[j] not in conflicts:
                        conflicts.append(self.allTasks[j])
        return conflicts

    def getDailySchedule(self) -> List[Task]:
        """Collect and sort all tasks, then return the full daily schedule."""
        self.collectTasks()
        self.sortByTime()
        return self.allTasks
