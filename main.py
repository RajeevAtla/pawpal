"""CLI demo for the PawPal+ scheduling system."""

from __future__ import annotations

from datetime import date

from pawpal_system import Owner
from pawpal_system import Pet
from pawpal_system import Scheduler
from pawpal_system import Task


def build_demo_owner() -> Owner:
    """Create demo data used by the terminal walkthrough."""

    owner = Owner(name="Jordan", available_minutes=150)
    mochi = Pet(name="Mochi", species="dog", age=4)
    luna = Pet(name="Luna", species="cat", age=2)

    mochi.add_task(Task("Morning walk", date(2026, 3, 30), "08:00", "daily", priority="high"))
    mochi.add_task(Task("Breakfast", date(2026, 3, 30), "08:00", priority="high"))
    luna.add_task(Task("Medication", date(2026, 3, 30), "09:00", "daily", priority="high"))
    luna.add_task(Task("Grooming", date(2026, 3, 30), "15:30", priority="medium"))

    owner.add_pet(mochi)
    owner.add_pet(luna)
    return owner


def print_schedule(scheduler: Scheduler) -> None:
    """Print the current daily schedule and any warnings."""

    print("Today's Schedule")
    print("-" * 72)
    for line in scheduler.daily_schedule_lines():
        print(line)

    warnings = scheduler.check_conflicts()
    if warnings:
        print("\nWarnings")
        print("-" * 72)
        for warning in warnings:
            print(warning)


def main() -> None:
    """Run the PawPal+ CLI demo."""

    owner = build_demo_owner()
    scheduler = Scheduler(owner)

    print_schedule(scheduler)

    print("\nCompleting Mochi's Morning walk to trigger recurrence...")
    next_task = scheduler.mark_task_complete("Mochi", "Morning walk")
    if next_task is not None:
        print(f"Created next occurrence for {next_task.due_date.isoformat()} at {next_task.due_time}.")

    print("\nUpdated Schedule")
    print("-" * 72)
    for line in scheduler.daily_schedule_lines():
        print(line)


if __name__ == "__main__":
    main()
