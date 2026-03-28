from datetime import datetime
from pawpal_system import Owner, Pet, Task, Scheduler


# --- Display helpers ---

def section(title: str):
    """Print a section header banner."""
    print("\n" + "=" * 52)
    print(f"  {title}")
    print("=" * 52)


def priority_label(priority: int) -> str:
    """Convert numeric priority to a readable emoji label."""
    if priority == 1:
        return "🔴 High"
    elif priority == 2:
        return "🟡 Medium"
    else:
        return "🟢 Low"


def status_label(completed: bool) -> str:
    """Convert completed boolean to a readable emoji status."""
    return "✅ Done" if completed else "⏳ Pending"


if __name__ == "__main__":

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

    # --- Tasks BEFORE sorting ---
    section("TASKS BEFORE SORTING")
    print(f"  {'TIME':<10}  {'TASK':<24}  {'PET':<8}  PRIORITY")
    print(f"  {'-'*10}  {'-'*24}  {'-'*8}  {'-'*11}")
    for task in scheduler.allTasks:
        print(
            f"  {task.dueTime.strftime('%I:%M %p'):<10}  "
            f"{task.taskName:<24}  "
            f"{task.petName:<8}  "
            f"{priority_label(task.priority)}"
        )

    # --- Tasks AFTER sorting (priority-first) ---
    scheduler.sortByTime()

    section("TASKS AFTER SORTING  (priority first, then time)")
    print(f"  {'TIME':<10}  {'TASK':<24}  {'PET':<8}  PRIORITY")
    print(f"  {'-'*10}  {'-'*24}  {'-'*8}  {'-'*11}")
    for task in scheduler.allTasks:
        print(
            f"  {task.dueTime.strftime('%I:%M %p'):<10}  "
            f"{task.taskName:<24}  "
            f"{task.petName:<8}  "
            f"{priority_label(task.priority)}"
        )

    # --- Filter by pet ---
    section("BUDDY'S TASKS ONLY")
    print(f"  {'TIME':<10}  TASK")
    print(f"  {'-'*10}  {'-'*24}")
    for task in scheduler.filterByPet("Buddy"):
        print(f"  {task.dueTime.strftime('%I:%M %p'):<10}  {task.taskName}")

    # --- Filter by status ---
    section("PENDING TASKS ONLY")
    print(f"  {'TASK':<24}  PET")
    print(f"  {'-'*24}  {'-'*8}")
    for task in scheduler.filterByStatus(False):
        print(f"  {task.taskName:<24}  {task.petName}")

    # --- Conflict detection ---
    # Morning Walk (Buddy) and Breakfast Feeding (Luna) are both at 7:00 AM — intentional conflict
    section("CONFLICT DETECTION")
    conflicts = scheduler.detectConflicts()
    if conflicts:
        for warning in conflicts:
            print(f"  ⚠️  {warning}")
    else:
        print("  No scheduling conflicts found.")

    # --- Recurring task demo ---
    # Find Morning Walk (a Daily task) and mark it complete
    morning_walk = None
    for task in scheduler.allTasks:
        if task.taskName == "Morning Walk":
            morning_walk = task
            break

    if morning_walk:
        section("RECURRING TASK DEMO")
        print(f"  Completing: {morning_walk.taskName} ({morning_walk.petName})")
        scheduler.markTaskComplete(morning_walk)
        print(f"  Original task completed: {morning_walk.completed}")

        print(f"\n  {'DATE/TIME':<18}  {'TASK':<24}  {'PET':<8}  {'PRIORITY':<13}  STATUS")
        print(f"  {'-'*18}  {'-'*24}  {'-'*8}  {'-'*13}  {'-'*10}")
        for task in scheduler.allTasks:
            dt = task.dueTime.strftime("%m/%d %I:%M %p")
            print(
                f"  {dt:<18}  "
                f"{task.taskName:<24}  "
                f"{task.petName:<8}  "
                f"{priority_label(task.priority):<13}  "
                f"{status_label(task.completed)}"
            )

    # --- Next available slot demo ---
    section("NEXT AVAILABLE SLOT")
    requested_time = datetime(2026, 3, 27, 7, 0)   # 7:00 AM — already booked (conflict)
    next_slot = scheduler.findNextAvailableSlot(requested_time)
    print(f"  Requested time : {requested_time.strftime('%I:%M %p')}")
    print(f"  Next open slot : {next_slot.strftime('%I:%M %p')}")
