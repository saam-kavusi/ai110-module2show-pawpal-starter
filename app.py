import streamlit as st
from datetime import datetime
from pawpal_system import Owner, Pet, Task, Scheduler


st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value="Jordan")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

st.markdown("### Tasks")
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

if "owners" not in st.session_state:
    st.session_state.owners = {}

current_owner_name = owner_name.strip() or "Default Owner"

if current_owner_name not in st.session_state.owners:
    st.session_state.owners[current_owner_name] = Owner(
        ownerName=current_owner_name,
        phone="",
        address="",
        emergencyContact=""
    )

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
                "priority": task.priority,
                "completed": task.completed,
            }
        )
    st.table(task_rows)
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("This button should call your scheduling logic once you implement it.")

if st.button("Generate schedule"):
    scheduler = Scheduler(owner)
    schedule = scheduler.getDailySchedule()
    st.success("Schedule generated!")

    for task in schedule:
        st.write(task.getDetails())
