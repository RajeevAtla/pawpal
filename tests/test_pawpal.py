from __future__ import annotations

from datetime import date

from pawpal_system import Owner
from pawpal_system import Pet
from pawpal_system import Scheduler
from pawpal_system import Task


def build_scheduler() -> Scheduler:
    owner = Owner("Jordan")
    mochi = Pet("Mochi", "dog")
    luna = Pet("Luna", "cat")

    mochi.add_task(Task("Breakfast", date(2026, 3, 30), "08:30"))
    mochi.add_task(Task("Morning walk", date(2026, 3, 30), "07:45", "daily"))
    luna.add_task(Task("Medication", date(2026, 3, 30), "08:30", "daily"))

    owner.add_pet(mochi)
    owner.add_pet(luna)
    return Scheduler(owner)


def test_mark_complete_sets_task_status() -> None:
    task = Task("Walk", date(2026, 3, 30), "08:00")

    task.mark_complete()

    assert task.is_completed is True


def test_add_task_increases_pet_task_count() -> None:
    pet = Pet("Mochi", "dog")

    pet.add_task(Task("Feed", date(2026, 3, 30), "09:00"))

    assert len(pet.tasks) == 1


def test_sort_tasks_returns_chronological_order() -> None:
    scheduler = build_scheduler()

    descriptions = [task.description for _, task in scheduler.sort_tasks_by_time()]

    assert descriptions == ["Morning walk", "Breakfast", "Medication"]


def test_marking_daily_task_complete_creates_next_occurrence() -> None:
    scheduler = build_scheduler()

    next_task = scheduler.mark_task_complete("Mochi", "Morning walk")

    assert next_task is not None
    assert next_task.due_date == date(2026, 3, 31)
    assert next_task.description == "Morning walk"


def test_conflict_detection_flags_duplicate_times() -> None:
    scheduler = build_scheduler()

    warnings = scheduler.check_conflicts()

    assert len(warnings) == 1
    assert "08:30" in warnings[0]


def test_filtering_incomplete_tasks_for_single_pet() -> None:
    scheduler = build_scheduler()
    scheduler.mark_task_complete("Mochi", "Morning walk")

    filtered = scheduler.filter_tasks(pet_name="Mochi", is_completed=False)

    assert [task.description for _, task in filtered] == ["Breakfast", "Morning walk"]


def test_empty_owner_has_no_tasks_or_conflicts() -> None:
    scheduler = Scheduler(Owner("Jordan"))

    assert scheduler.sort_tasks_by_time() == []
    assert scheduler.check_conflicts() == []
