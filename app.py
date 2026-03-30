from __future__ import annotations

from datetime import date
from datetime import datetime

import streamlit as st

from pawpal_system import Owner
from pawpal_system import Pet
from pawpal_system import Scheduler
from pawpal_system import Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")


def get_owner() -> Owner:
    """Return the session-scoped owner instance."""

    if "owner" not in st.session_state:
        st.session_state.owner = Owner(name="Jordan", available_minutes=120)
    return st.session_state.owner


def build_schedule_rows(scheduler: Scheduler) -> list[dict[str, str]]:
    """Convert scheduled tasks into a table-friendly shape."""

    rows: list[dict[str, str]] = []
    for pet, task in scheduler.sort_tasks_by_time():
        rows.append(
            {
                "Date": task.due_date.isoformat(),
                "Time": task.due_time,
                "Pet": pet.name,
                "Species": pet.species,
                "Task": task.description,
                "Frequency": task.frequency,
                "Priority": task.priority,
                "Status": "Done" if task.is_completed else "Pending",
            }
        )
    return rows


owner = get_owner()
scheduler = Scheduler(owner)

st.title("🐾 PawPal+")
st.caption("Plan care tasks, spot conflicts, and keep up with recurring pet routines.")

with st.expander("Project Summary", expanded=True):
    st.markdown(
        """
PawPal+ helps a pet owner manage daily care tasks across multiple pets.
The scheduler sorts tasks by time, filters by pet or completion status,
warns about conflicts, and automatically creates the next recurring task when needed.
"""
    )

st.subheader("Owner Setup")
owner.name = st.text_input("Owner name", value=owner.name)
owner.available_minutes = int(
    st.number_input(
        "Available minutes today",
        min_value=15,
        max_value=720,
        value=owner.available_minutes,
        step=15,
    )
)

st.divider()

st.subheader("Pets")
with st.form("add_pet_form", clear_on_submit=True):
    pet_name = st.text_input("Pet name")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    age = st.number_input("Age", min_value=0, max_value=40, value=0)
    add_pet_submitted = st.form_submit_button("Add pet")

if add_pet_submitted:
    if not pet_name.strip():
        st.warning("Enter a pet name before adding a pet.")
    elif owner.get_pet(pet_name.strip()) is not None:
        st.warning(f"{pet_name.strip()} is already in the household.")
    else:
        owner.add_pet(Pet(name=pet_name.strip(), species=species, age=int(age)))
        st.success(f"Added {pet_name.strip()} to {owner.name}'s household.")

if owner.pets:
    st.table(
        [
            {"Name": pet.name, "Species": pet.species, "Age": pet.age if pet.age is not None else "-"}
            for pet in owner.pets
        ]
    )
else:
    st.info("No pets added yet.")

st.divider()

st.subheader("Tasks")
pet_options = [pet.name for pet in owner.pets]

with st.form("add_task_form", clear_on_submit=True):
    selected_pet = st.selectbox("Assign to pet", pet_options if pet_options else ["No pets yet"])
    task_title = st.text_input("Task title")
    due_date = st.date_input("Due date", value=date.today())
    due_time = st.time_input("Due time", value=datetime.strptime("08:00", "%H:%M").time())
    frequency = st.selectbox("Frequency", ["once", "daily", "weekly"])
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=1)
    add_task_submitted = st.form_submit_button("Add task", disabled=not owner.pets)

if add_task_submitted:
    task = Task(
        description=task_title.strip(),
        due_date=due_date,
        due_time=due_time.strftime("%H:%M"),
        frequency=frequency,
        priority=priority,
    )
    if not task.description:
        st.warning("Enter a task title before adding a task.")
    elif owner.add_task_to_pet(selected_pet, task):
        st.success(f"Added {task.description} for {selected_pet}.")
    else:
        st.warning("Choose a valid pet before adding a task.")

st.divider()

st.subheader("Build Schedule")

filter_pet = st.selectbox("Filter by pet", ["All pets", *pet_options], index=0)
filter_status = st.selectbox("Filter by status", ["All", "Pending", "Done"], index=0)

rows = build_schedule_rows(scheduler)
if filter_pet != "All pets":
    rows = [row for row in rows if row["Pet"] == filter_pet]
if filter_status != "All":
    rows = [row for row in rows if row["Status"] == filter_status]

if st.button("Generate schedule"):
    warnings = scheduler.check_conflicts()
    if warnings:
        for warning in warnings:
            st.warning(warning)
    else:
        st.success("No task conflicts detected.")

if rows:
    st.table(rows)
else:
    st.info("No scheduled tasks match the current filters.")

st.subheader("Complete a Task")
completion_pet = st.selectbox("Pet to update", pet_options if pet_options else ["No pets yet"], key="complete_pet")

completion_options = []
if owner.pets and completion_pet != "No pets yet":
    completion_options = [
        task.description
        for _, task in scheduler.filter_tasks(pet_name=completion_pet, is_completed=False)
    ]

completion_task = st.selectbox(
    "Pending task",
    completion_options if completion_options else ["No pending tasks"],
)

if st.button("Mark task complete", disabled=not completion_options):
    next_task = scheduler.mark_task_complete(completion_pet, completion_task)
    st.success(f"Marked {completion_task} complete for {completion_pet}.")
    if next_task is not None:
        st.info(
            f"Created next {next_task.frequency} occurrence on "
            f"{next_task.due_date.isoformat()} at {next_task.due_time}."
        )
