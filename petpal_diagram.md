```mermaid
classDiagram
    class Owner {
        +String ownerName
        +String phone
        +String address
        +String emergencyContact
        +List pets
        +addPet(pet)
        +getPets()
    }

    class Pet {
        +String petName
        +String type
        +String breed
        +datetime dateOfBirth
        +String allergies
        +String medicalNotes
        +List tasks
        +addTask(task)
        +getTasks()
    }

    class Task {
        +String taskName
        +datetime dueTime
        +String frequency
        +int priority
        +String petName
        +bool completed
        +markComplete()
        +getDetails()
    }

    class Scheduler {
        +Owner owner
        +List allTasks
        +collectTasks()
        +sortByTime()
        +markTaskComplete(task)
        +filterByPet(petName) List~Task~
        +filterByStatus(completed) List~Task~
        +detectConflicts() List~str~
        +getDailySchedule() List~Task~
    }

    Owner "1" --> "1..*" Pet : owns
    Pet "1" --> "0..*" Task : has
    Scheduler "1" --> "1" Owner : schedules for
    Scheduler "1" --> "0..*" Task : collects and manages
    Scheduler --> Pet : adds next occurrence via markTaskComplete
```
