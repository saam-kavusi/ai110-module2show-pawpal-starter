from dataclasses import dataclass, field
from typing import List


@dataclass
class Task:
    taskName: str
    dueTime: str
    frequency: str
    priority: int
    completed: bool = False

    def markComplete(self):
        pass

    def getDetails(self):
        pass


@dataclass
class Pet:
    petName: str
    type: str
    breed: str
    age: str
    allergies: str
    medicalNotes: str
    tasks: List[Task] = field(default_factory=list)

    def addTask(self, task: Task):
        pass

    def getTasks(self):
        pass


class Owner:
    def __init__(self, ownerName: str, phone: str, address: str, emergencyContact: str):
        self.ownerName = ownerName
        self.phone = phone
        self.address = address
        self.emergencyContact = emergencyContact
        self.pets: List[Pet] = []

    def addPet(self, pet: Pet):
        pass

    def getPets(self):
        pass


class Scheduler:
    def __init__(self):
        self.allTasks: List[Task] = []

    def collectTasks(self, owner: Owner):
        pass

    def sortByTime(self):
        pass

    def detectConflicts(self):
        pass

    def getDailySchedule(self):
        pass
