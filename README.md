# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.


## Smarter Scheduling

- PawPal+ includes smarter scheduling features to help organize pet care tasks. The scheduler sorts tasks by due time and uses priority as a tie-breaker when tasks happen at the same time. It can also filter tasks by pet name or completion status.

- The system supports recurring care by automatically creating the next daily or weekly task when one is marked complete. It also detects exact-time conflicts and returns warning messages so the user can spot scheduling problems without the program crashing.

## Testing PawPal+

The PawPal+ system uses `pytest` to verify the main scheduling features and core behaviors.

Run the tests with:

```bash
python -m pytest
``` 
The tests cover the following:
- Task completion
- Adding tasks to pets
- Sorting by due time
- Priority tie-breaks
- Daily and weekly recurrence
- Non-recurring “Once” tasks
- Conflict detection for duplicate times
- Filtering by pet name
- Filtering by completion status
- Empty or no-match edge cases


## Confidence Level: ★★★★★

- All current tests are passing, and the main scheduling features are working as expected.

## Challenge 1
- As an extra algorithmic feature, I added a      
  findNextAvailableSlot method to the Scheduler     
  class. This method accepts a requested start time 
  and checks whether that time is already occupied  
  by an existing task. If it is, the scheduler moves
   forward in 30-minute increments until it finds a 
  free slot, then returns that datetime. I used
  Agent Mode to help plan where this logic should
  live and how it could fit into my existing
  Scheduler class without redesigning the rest of
  the system. I kept the final implementation simple
   and beginner-friendly so it would match the
  structure of the rest of the project.

## Features 

1) Priority-First Sorting
Tasks are sorted by priority number first (1 = High, 2 = Medium, 3 = Low), then by due time within each priority level. A high-priority task scheduled at 6:00 PM will always appear before a low-priority task at 7:00 AM. The sort uses a two-value tuple key — `(priority, dueTime)` — so Python handles both levels of ordering in a single pass.

2) Conflict Detection
The scheduler detects when two or more tasks are booked at the exact same time and returns a plain-English warning string for each conflict instead of crashing. The algorithm sorts tasks first, then checks only neighboring pairs — O(n) instead of the O(n²) approach of comparing every task against every other task.

3) Daily and Weekly Recurrence
When a task with frequency `"daily"` or `"weekly"` is marked complete, the scheduler automatically creates a new copy due the next day or 7 days later using Python's `timedelta`. The original task stays marked as complete. Tasks with frequency `"once"` or `"monthly"` do not generate a next occurrence.

4) Filter by Pet
`filterByPet(petName)` returns only the tasks belonging to a specific pet without modifying the main task list. Returns an empty list if no tasks match — no crash.

5) Filter by Status
`filterByStatus(completed)` returns either all pending tasks (`False`) or all completed tasks (`True`). Returns a new filtered list and leaves `allTasks` unchanged.

6) Next Available Slot
`findNextAvailableSlot(start_time)` finds the first open time slot at or after a requested time. It builds a set of all currently booked times, then steps forward in 30-minute increments until it finds a free slot. Using a set makes each lookup O(1).

7) JSON Persistence
Owner, pet, and task data is saved to `data.json` after every change and loaded back on app startup. Each class implements `to_dict()` for serialization and `from_dict()` for reconstruction — so the full Owner → Pet → Task tree survives page refreshes and app restarts.

8) Human-Readable Priority and Status Labels
Priority numbers are displayed as `🔴 High`, `🟡 Medium`, and `🟢 Low`. Completion status is shown as `✅ Done` or `⏳ Pending`. Priority is still stored as an integer internally so all sorting and filtering logic is unaffected.

## 📸 Demo

<a href="/course_images/ai110/Demo_TOP.png" target="_blank"><img src="/course_images/ai110/Demo_TOP.png" title="PawPal App - Top" alt="PawPal App - Top" class="center-block" /></a>

<a href="/course_images/ai110/DEMO_MID.png" target="_blank"><img src="/course_images/ai110/DEMO_MID.png" title="PawPal App - Middle" alt="PawPal App - Middle" class="center-block" /></a>

<a href="/course_images/ai110/DEMO_LOW.png" target="_blank"><img src="/course_images/ai110/DEMO_LOW.png" title="PawPal App - Bottom" alt="PawPal App - Bottom" class="center-block" /></a>
