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

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

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
