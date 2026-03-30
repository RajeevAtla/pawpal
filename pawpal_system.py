"""Core data model and scheduling logic for the PawPal+ app."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from datetime import datetime
from datetime import timedelta
from typing import Optional


@dataclass
class Task:
    """Represent a single pet care activity."""

    description: str
    due_date: date
    due_time: str
    frequency: str = "once"
    is_completed: bool = False
    priority: str = "medium"

    def mark_complete(self) -> None:
        """Mark the task as completed."""

        self.is_completed = True

    def next_occurrence(self) -> Optional[Task]:
        """Create the next recurring task when the frequency supports it."""

        if self.frequency == "daily":
            next_date = self.due_date + timedelta(days=1)
        elif self.frequency == "weekly":
            next_date = self.due_date + timedelta(days=7)
        else:
            return None

        return Task(
            description=self.description,
            due_date=next_date,
            due_time=self.due_time,
            frequency=self.frequency,
            priority=self.priority,
        )

    def sort_key(self) -> tuple[date, datetime]:
        """Return a sortable key for date and time ordering."""

        return self.due_date, datetime.strptime(self.due_time, "%H:%M")


@dataclass
class Pet:
    """Store pet details and its associated care tasks."""

    name: str
    species: str
    age: Optional[int] = None
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Attach a task to this pet."""

        self.tasks.append(task)


@dataclass
class Owner:
    """Manage a collection of pets."""

    name: str
    available_minutes: int = 120
    preferences: list[str] = field(default_factory=list)
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner's household."""

        self.pets.append(pet)

    def get_all_tasks(self) -> list[tuple[Pet, Task]]:
        """Return every task across the owner's pets."""

        all_tasks: list[tuple[Pet, Task]] = []
        for pet in self.pets:
            for task in pet.tasks:
                all_tasks.append((pet, task))
        return all_tasks


class Scheduler:
    """Organize and evaluate tasks across an owner's pets."""

    def __init__(self, owner: Owner) -> None:
        """Initialize the scheduler with an owner."""

        self.owner = owner

    def sort_tasks_by_time(self) -> list[tuple[Pet, Task]]:
        """Return all tasks in chronological order."""

        return sorted(self.owner.get_all_tasks(), key=lambda item: item[1].sort_key())

    def filter_tasks(
        self,
        *,
        pet_name: Optional[str] = None,
        is_completed: Optional[bool] = None,
    ) -> list[tuple[Pet, Task]]:
        """Return tasks filtered by pet name and/or completion status."""

        filtered_tasks = self.owner.get_all_tasks()

        if pet_name is not None:
            filtered_tasks = [
                (pet, task)
                for pet, task in filtered_tasks
                if pet.name.lower() == pet_name.lower()
            ]

        if is_completed is not None:
            filtered_tasks = [
                (pet, task)
                for pet, task in filtered_tasks
                if task.is_completed == is_completed
            ]

        return sorted(filtered_tasks, key=lambda item: item[1].sort_key())

    def check_conflicts(self) -> list[str]:
        """Return non-fatal warnings for tasks scheduled at the same time."""

        schedule_map: dict[tuple[date, str], list[str]] = {}

        for pet, task in self.owner.get_all_tasks():
            key = (task.due_date, task.due_time)
            schedule_map.setdefault(key, []).append(f"{pet.name}: {task.description}")

        warnings: list[str] = []
        for (due_date, due_time), scheduled_items in schedule_map.items():
            if len(scheduled_items) > 1:
                joined_items = ", ".join(scheduled_items)
                warnings.append(
                    f"Conflict at {due_date.isoformat()} {due_time} for {joined_items}."
                )

        return warnings

    def mark_task_complete(self, pet_name: str, task_description: str) -> Optional[Task]:
        """Mark a task complete and create its next occurrence when needed."""

        for pet, task in self.owner.get_all_tasks():
            if pet.name != pet_name or task.description != task_description:
                continue

            task.mark_complete()
            next_task = task.next_occurrence()
            if next_task is not None:
                pet.add_task(next_task)
            return next_task

        return None

    def daily_schedule_lines(self) -> list[str]:
        """Return a readable schedule summary for terminal and UI display."""

        lines: list[str] = []
        for pet, task in self.sort_tasks_by_time():
            status = "done" if task.is_completed else "pending"
            lines.append(
                f"{task.due_date.isoformat()} {task.due_time} | {pet.name} | "
                f"{task.description} | {task.priority} | {status}"
            )
        return lines
