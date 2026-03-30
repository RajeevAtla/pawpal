"""Core data model and scheduling logic for the PawPal+ app."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
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


@dataclass
class Pet:
    """Store pet details and its associated care tasks."""

    name: str
    species: str
    age: Optional[int] = None
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Attach a task to this pet."""


@dataclass
class Owner:
    """Manage a collection of pets."""

    name: str
    available_minutes: int = 120
    preferences: list[str] = field(default_factory=list)
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner's household."""

    def get_all_tasks(self) -> list[tuple[Pet, Task]]:
        """Return every task across the owner's pets."""


class Scheduler:
    """Organize and evaluate tasks across an owner's pets."""

    def __init__(self, owner: Owner) -> None:
        """Initialize the scheduler with an owner."""

        self.owner = owner

    def sort_tasks_by_time(self) -> list[tuple[Pet, Task]]:
        """Return all tasks in chronological order."""

    def filter_tasks(
        self,
        *,
        pet_name: Optional[str] = None,
        is_completed: Optional[bool] = None,
    ) -> list[tuple[Pet, Task]]:
        """Return tasks filtered by pet name and/or completion status."""

    def check_conflicts(self) -> list[str]:
        """Return non-fatal warnings for tasks scheduled at the same time."""

    def mark_task_complete(self, pet_name: str, task_description: str) -> Optional[Task]:
        """Mark a task complete and create its next occurrence when needed."""
