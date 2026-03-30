# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

My initial UML centered on four classes: `Task`, `Pet`, `Owner`, and `Scheduler`. `Task` was responsible for storing the details of one care activity, including time, date, recurrence, completion, and priority. `Pet` owned a list of tasks. `Owner` managed multiple pets and acted as the entry point for the household's data. `Scheduler` sat on top of those classes and handled sorting, filtering, conflict detection, and completion workflows.

Three core user actions I identified early were:

1. Add and manage pets in one household.
2. Add care tasks with a time and recurrence pattern.
3. Generate and review a daily schedule with warnings.

**b. Design changes**

The main design change during implementation was moving lookup helpers into `Owner`. I originally expected the UI to search through pets directly, but that would have duplicated logic in `app.py`. I added `get_pet()` and `add_task_to_pet()` so the Streamlit layer could stay thinner and the domain layer could remain responsible for object access. I also added a `Task.next_occurrence()` helper instead of putting all recurrence logic directly inside `Scheduler`, because recurrence belongs naturally to the task model.

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

The scheduler currently considers:

- task date and time
- completion status
- pet ownership
- recurrence frequency
- priority values stored on each task

I treated time ordering and recurrence as the most important constraints because the assignment required a usable daily schedule. Priority is stored and displayed, but I did not make it the primary sort rule because the base project requirement focused more directly on chronological scheduling.

**b. Tradeoffs**

One intentional tradeoff is that conflict detection only checks for exact duplicate date/time slots. It does not calculate overlaps based on task duration. That tradeoff is reasonable here because it keeps the code readable, easy to test, and aligned with the assignment's “lightweight warning” requirement. A richer overlap model would be useful in a production planner, but it would add more complexity than this project needs.

## 3. AI Collaboration

**a. How you used AI**

I used AI as a structured implementation partner across the project lifecycle:

- translating the assignment into an execution plan
- inspecting the starter repo and identifying missing deliverables
- shaping the class design and method boundaries
- implementing the backend incrementally
- wiring the Streamlit UI to the backend
- creating the Mermaid UML and project documentation
- debugging the local environment when `pytest` was broken

The most helpful prompts were specific prompts about architecture boundaries, verification steps, and concrete deliverables. Asking for small, isolated changes was more useful than asking for one large end-to-end solution.

**b. Judgment and verification**

One moment where I did not accept the first AI-shaped path as-is was the Mermaid export workflow. The Mermaid Live editor became unstable with malformed prior content, so instead of forcing more brittle page manipulation, I preserved the Mermaid source locally and rendered it through a small HTML wrapper to generate the final image reliably. I verified each step by checking the rendered diagram in the browser and saving the final PNG asset.

## 4. Testing and Verification

**a. What you tested**

I tested:

- `mark_complete()` changes a task's status
- adding a task increases a pet's task count
- tasks are sorted in chronological order
- completing a daily task creates the next occurrence
- duplicate date/time conflicts return warnings
- filtering by pet and completion status works
- an owner with no pets has no tasks or conflicts

These tests were important because they cover both the basic object model and the assignment's required algorithmic behavior.

**b. Confidence**

I am at about 4/5 confidence that the scheduler works correctly for the implemented scope. The tested behaviors all pass, and the CLI plus Streamlit layers both use the same backend. If I had more time, I would add tests for invalid time strings, weekly recurrence edge cases, duplicate task descriptions on the same pet, and overlap-based conflict detection using task duration.

## 5. Reflection

**a. What went well**

The strongest part of the project is the separation between the domain layer and the UI. `pawpal_system.py` contains the real logic, while `app.py` mostly translates user actions into backend method calls. That made the CLI demo, tests, and UI all reinforce the same implementation instead of diverging.

**b. What you would improve**

On another iteration, I would redesign `Task` to include duration and stronger validation. I would also add persistence so pets and tasks survive app restarts, and I would upgrade conflict detection from exact-time matching to true overlap detection.

**c. Key takeaway**

The most important takeaway was that AI works best when the human stays in the architect role. AI sped up scaffolding, implementation, and debugging, but the quality of the result depended on making clear decisions about boundaries, testing, and tradeoffs instead of accepting every suggestion at face value.
