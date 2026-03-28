import streamlit as st
from datetime import datetime
from pawpal_system import Owner, Pet, Task, Scheduler, save_owners, load_owners


def priority_label(priority: int) -> str:
    """Convert a numeric priority to a human-readable emoji label."""
    if priority == 1:
        return "🔴 High"
    elif priority == 2:
        return "🟡 Medium"
    else:
        return "🟢 Low"


def status_label(completed: bool) -> str:
    """Convert a completed boolean to a human-readable emoji status."""
    return "✅ Done" if completed else "⏳ Pending"


st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
**PawPal+** helps a pet owner plan and schedule care tasks for their pet(s).
Add tasks below, then generate a sorted daily schedule with conflict detection.
"""
)

st.divider()

st.subheader("Owner & Pet")
owner_name = st.text_input("Owner name", value="Jordan")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

st.markdown("### Tasks")
st.caption("Add tasks below. Each task will be included in the generated schedule.")

if "owners" not in st.session_state:
    st.session_state.owners = load_owners()

current_owner_name = owner_name.strip() or "Default Owner"

if current_owner_name not in st.session_state.owners:
    st.session_state.owners[current_owner_name] = Owner(
        ownerName=current_owner_name,
        phone="",
        address="",
        emergencyContact=""
    )
    save_owners(st.session_state.owners)

owner = st.session_state.owners[current_owner_name]

col1, col2 = st.columns(2)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
    
col3, col4, col5 = st.columns(3)
with col3:
    task_date = st.date_input("Task date")
    st.caption(f"Selected date: {task_date.strftime('%m/%d/%Y')}")
with col4:
    task_time = st.time_input("Task time")
with col5:
    frequency = st.selectbox("Frequency", ["once", "daily", "weekly"], index=1)

existing_pet = None
for pet in owner.getPets():
    if pet.petName == pet_name:
        existing_pet = pet
        break

if existing_pet is None:
    existing_pet = Pet(
        petName=pet_name,
        type=species,
        breed="",
        dateOfBirth=datetime.now(),
        allergies="",
        medicalNotes="",
    )
    owner.addPet(existing_pet)
    save_owners(st.session_state.owners)

if st.button("Add task"):
    priority_value = 1 if priority == "high" else 2 if priority == "medium" else 3
    due_datetime = datetime.combine(task_date, task_time)

    task = Task(
        taskName=task_title,
        dueTime=due_datetime,
        frequency=frequency,
        priority=priority_value,
        petName=existing_pet.petName
    )

    existing_pet.addTask(task)
    save_owners(st.session_state.owners)
    st.success(f"Added task '{task_title}' for {existing_pet.petName}")

if existing_pet.getTasks():
    st.write("Current tasks:")
    task_rows = []
    for task in existing_pet.getTasks():
        task_rows.append(
            {
                "title": task.taskName,
                "owner": owner.ownerName,
                "pet": task.petName,
                "due_time": task.dueTime.strftime("%Y-%m-%d %H:%M"),
                "frequency": task.frequency,
                "priority": priority_label(task.priority),
                "status": status_label(task.completed),
            }
        )
    st.table(task_rows)
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("Generates a sorted schedule for all pets under this owner and checks for conflicts.")

if st.button("Generate schedule"):
    scheduler = Scheduler(owner)
    schedule = scheduler.getDailySchedule()

    # Show conflict warnings
    conflicts = scheduler.detectConflicts()
    if conflicts:
        for warning in conflicts:
            st.warning(warning)
    else:
        st.success("Schedule generated! No conflicts found.")

    # Display schedule as a table
    if schedule:
        schedule_rows = []
        for task in schedule:
            schedule_rows.append({
                "Time": task.dueTime.strftime("%I:%M %p"),
                "Task": task.taskName,
                "Pet": task.petName,
                "Frequency": task.frequency,
                "Priority": priority_label(task.priority),
                "Status": status_label(task.completed),
            })
        st.table(schedule_rows)
    else:
        st.info("No tasks found. Add some tasks above first.")
