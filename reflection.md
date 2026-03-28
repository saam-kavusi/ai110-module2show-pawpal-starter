# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Allow user to input basic owner and pet info
    - pet name, type, age/DOB, breed, allergies, ongoing medicl issues, current medicines with dosage and frequency, and a notes section
    - User/owner Name, phone number, emergency contact for pet, and address
- Allow user to add and edit tasks.
    - task duration
    - order of tasks
    - medical appointment 
    - feedings, walks, medicines
- A calander like feature for todays tasks
- A to do/reminders list 

- I would include 4 main classes for my design
- 1) Task: Stores info about a single pet care activity, such as the task description, time, frequency, priority, and completion status. Its responsibility is to represent one scheduled action like feeding, walking, giving medicine, or attending an appointment.

- 2) Pet: Stores information about an individual pet, such as its name, type, breed, age, health notes, and its list of tasks. Its responsibility is to keep all data related to one pet together and allow tasks to be added or managed for that pet.

- 3) Owner: Stores the owner’s information and manages multiple pets. Its responsibility is to act as the main container for the user’s pets and provide access to all pets in the system.

- 4) Scheduler: Organizes and manages tasks across all pets. Its responsibility is to collect tasks, sort them by time, detect conflicts, and generate a daily schedule that is easy for the user to follow.
**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.
- Yes it did, scheduer had no direct reference to owner. Scheduler never directly interacted with pet. Collect tasks in scheduler does all the heavy lifting so looping through every pet under owner could get messy fast. detect conflicts had no return type or output plan. Age was a string which could get stale so we changed that and owner was not a dataclass. This resolved all bottle necks and missing relationships.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- My scheduler considers due time, priority, frequency, completion status, and pet name. Due time is the main constraint because tasks should be organized in chronological order. Priority is used as a tie-breaker when tasks share the same time. Frequency is used for recurring tasks, completion status helps separate pending and finished tasks, and pet name allows filtering for a specific pet.

- I decided time mattered most because the main job of a scheduler is to show what should happen and when. Priority mattered next because it helps when tasks are scheduled at the same time. I focused on these constraints because they were the most useful and simplest to implement for this project.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- My scheduler uses a sort then scan approach for conflict detection. This makes the logic simpler and avoids comparing every task against every other task, but it only checks whether tasks happen at the exact same time instead of handling more advanced overlapping durations.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?


## Prompt Comparison

- For the multi-model prompt comparison, I compared responses from Claude and ChatGPT on how to extend PawPal+ with JSON persistence and scheduling improvements. Claude was strong at producing direct implementation steps and making file-by-file edits, which was helpful when I wanted fast code changes. ChatGPT was more helpful for planning the safest approach first, especially when checking whether the design still matched my current architecture and warning me about edge cases like saving multiple owners instead of only one.

- Overall, Claude gave me a fast implementation oriented workflow, while ChatGPT gave me stronger guidance for reasoning through tradeoffs and keeping the project structure clean. I found Claude’s responses useful for coding speed, but ChatGPT’s responses felt more modular and better for understanding why certain design choices were safer or more maintainable.