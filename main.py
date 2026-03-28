from datetime import datetime
from pawpal_system import Owner, Pet, Task, Scheduler

# --- Owner ---
owner = Owner(
    ownerName="Alex Rivera",
    phone="555-1234",
    address="123 Maple Street",
    emergencyContact="555-5678"
)

# --- Pets ---
buddy = Pet(
    petName="Buddy",
    type="Dog",
    breed="Golden Retriever",
    dateOfBirth=datetime(2019, 4, 10),
    allergies="None",
    medicalNotes="Annual checkup in June"
)

luna = Pet(
    petName="Luna",
    type="Cat",
    breed="Siamese",
    dateOfBirth=datetime(2021, 8, 22),
    allergies="Chicken",
    medicalNotes="Sensitive stomach"
)

owner.addPet(buddy)
owner.addPet(luna)

# --- Tasks (added OUT of order on purpose to demo sorting) ---
buddy.addTask(Task(
    taskName="Flea Medicine",
    dueTime=datetime(2026, 3, 27, 9, 0),
    frequency="Monthly",
    priority=2,
    petName="Buddy"
))

buddy.addTask(Task(
    taskName="Morning Walk",
    dueTime=datetime(2026, 3, 27, 7, 0),
    frequency="Daily",
    priority=1,
    petName="Buddy"
))

luna.addTask(Task(
    taskName="Vet Appointment",
    dueTime=datetime(2026, 3, 27, 14, 0),
    frequency="Once",
    priority=3,
    petName="Luna"
))

luna.addTask(Task(
    taskName="Breakfast Feeding",
    dueTime=datetime(2026, 3, 27, 7, 0),
    frequency="Daily",
    priority=1,
    petName="Luna"
))

# --- Scheduler ---
scheduler = Scheduler(owner)
scheduler.collectTasks()

# Print BEFORE sorting
print("=" * 40)
print("     TASKS BEFORE SORTING")
print("=" * 40)
for task in scheduler.allTasks:
    print(f"{task.dueTime.strftime('%I:%M %p')} | {task.taskName} ({task.petName})")

# Sort tasks, then print AFTER sorting
scheduler.sortByTime()

print("\n" + "=" * 40)
print("     TASKS AFTER SORTING")
print("=" * 40)
for task in scheduler.allTasks:
    print(f"{task.dueTime.strftime('%I:%M %p')} | {task.taskName} ({task.petName})")

# Filter by pet name
print("\n" + "=" * 40)
print("     BUDDY'S TASKS ONLY")
print("=" * 40)
for task in scheduler.filterByPet("Buddy"):
    print(f"{task.dueTime.strftime('%I:%M %p')} | {task.taskName}")

# Filter by completed status
print("\n" + "=" * 40)
print("     PENDING TASKS ONLY")
print("=" * 40)
for task in scheduler.filterByStatus(False):
    print(f"{task.taskName} ({task.petName})")

# --- Conflicts ---
# Morning Walk (Buddy) and Breakfast Feeding (Luna) are both at 7:00 AM — intentional conflict
print("\n" + "=" * 40)
print("     CONFLICT DETECTION")
print("=" * 40)
conflicts = scheduler.detectConflicts()
if conflicts:
    for warning in conflicts:
        print(f"  - {warning}")
else:
    print("No scheduling conflicts found.")

# --- Recurring Task Demo ---
# Find Morning Walk (a Daily task) and mark it complete
morning_walk = None
for task in scheduler.allTasks:
    if task.taskName == "Morning Walk":
        morning_walk = task
        break

if morning_walk:
    print("\n" + "=" * 40)
    print("     RECURRING TASK DEMO")
    print("=" * 40)
    print(f"Completing: {morning_walk.taskName} ({morning_walk.petName})")
    scheduler.markTaskComplete(morning_walk)

    print(f"Original task completed: {morning_walk.completed}")

    print("\nAll tasks after completing Morning Walk:")
    for task in scheduler.allTasks:
        status = "Done" if task.completed else "Pending"
        print(f"  {task.dueTime.strftime('%m/%d %I:%M %p')} | {task.taskName} ({task.petName}) | {status}")
