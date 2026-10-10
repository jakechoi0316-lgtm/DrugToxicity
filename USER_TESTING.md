# User testing plan: harm reduction non-profits

**Goal:** show that staff at harm reduction non-profits can use the map without help, and that it helps them decide where to send outreach and naloxone.

**Who to test with first:** outreach workers, program coordinators or managers at harm reduction non-profits in BC. Aim for **3–5 people**. Classmates or friends can do a practice run first, but count them separately.

**Privacy:** do not collect names of clients, health details, or anything about the people your testers serve. Only record the tester's role and organization type.

---

## 1. Message to send to a non-profit

> **Subject:** 10 minutes to try a free naloxone planning map?
>
> Hi [name],
>
> I'm a health informatics student building a free map for harm reduction non-profits in BC. It shows, for each health region, drug deaths, paramedic-attended overdoses, naloxone sites, and naloxone kits per overdose. It also flags where overdoses are rising.
>
> Could you spend 10 minutes trying it and telling me what's useful or missing? It's all public data. No login needed.
>
> Map: https://jakechoi0316-lgtm.github.io/DrugToxicity/
> Feedback (3 questions, 1 minute): [your Google Form link]
>
> Thank you,
> [your name]

---

## 2. Test session (10 minutes)

Open the map on the tester's own device if possible. Say: *"Think out loud. I'm testing the map, not you."* Don't help unless they're stuck for more than a minute.

| # | Task | What success looks like |
|---|---|---|
| 1 | "Which region in BC most needs more naloxone kits right now?" | Finds the **Where to send naloxone first** list or the **Kits per overdose** view. Answers Fraser East (2025). |
| 2 | "Show me your own health authority." | Uses **Zoom to** or clicks a region. |
| 3 | "In your health authority, is anywhere getting worse?" | Finds the **Early warning** list or the purple dots. |
| 4 | "Compare overdoses in 2021 and 2025 for one region." | Uses the year slider and hovers a region. |
| 5 | "Send a summary of your area to a coworker." | Uses **Copy summary** and pastes it somewhere. |

**Record for each task:** done / done with help / not done, time taken, and what confused them (their words).

**Then ask:**
1. How do you decide today where to send outreach staff or naloxone?
2. Would this change any decision you make? Which one?
3. What's missing for this to be useful every month?
4. Is anything confusing or wrong?
5. Can I quote you (no name, just your role)?

---

## 3. Google Form (paste these questions in)

1. **What is your role?** *(multiple choice)* Outreach worker · Program coordinator or manager · Peer worker · Health authority staff · Researcher or student · Other
2. **Did the map help you see where naloxone or outreach is needed most?** *(scale 1–5: Not at all → Very much)*
3. **What would you change or add?** *(short answer)*
4. *(optional)* **Can we contact you for a 10-minute follow-up?** Email *(short answer)*

Copy the form's share link into `index.html`: find the line `const FEEDBACK_URL = "";` near the top of the script and paste the link between the quotes. The "Give feedback" links then appear on the map.

---

## 4. Results (fill in)

| Tester (role, org type) | Task 1 | Task 2 | Task 3 | Task 4 | Task 5 | Most useful | Most confusing | Quote |
|---|---|---|---|---|---|---|---|---|
| | | | | | | | | |
| | | | | | | | | |
| | | | | | | | | |

**Summary after testing:**
- Tasks completed without help: __ of __
- Changes we made because of feedback:
- Best quote:
