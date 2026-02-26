# Two-Hour Screen-Time Target

**Companion-Self template · Design constraint and equivalent metric**

Companion-Self is calibrated so that **all screen-based learning is designed to occur within a 2-hour window per day**. This aligns with Alpha School’s model (full mandatory education in ~2 hours of screen time) and provides an **equivalent metric** for comparison and design.

---

## 1. Alpha’s 2-hour frame

Alpha School squeezes the full academic program into **~2 hours of screen time per day**: personalized AI-tutored lessons, mastery-based progress, at the zone of proximal development. The rest of the day is life skills, workshops, and non-screen activity. That 2-hour block is the **mandatory education** window.

### 1.1 Estimated composition of the 2 hours (from Moonshots #233 transcript)

From the Alpha leadership (McKenzie Price, Joe Lamont) description, the **2 hours of screen time** are composed as follows. Use this as a target breakdown when designing companion-self's equivalent block.

| Component | What it is (from transcript) | Approx. role in 2 hours |
|-----------|------------------------------|--------------------------|
| **When** | "2-hour core learning block" after "Limitless Launch"; "by lunchtime they're finished with academics." | Single continuous block; **Limitless Launch is not screen time** (physical/growth mindset). |
| **Structure** | "Kids are on computers"; "breaks every 30 minutes … stretch and play." | ~**4 segments** of ~25–30 min net focus, with short breaks in between. |
| **Content** | "Full academic program"; "reading and writing and math and science"; "crush your APs"; K–12. | **All core subjects** in one block; personalized mix per kid (no fixed subject clock in transcript). |
| **Delivery** | "One-to-one interaction on the computer"; "zone of proximal development"; "lessons aren't too hard … not so easy." | **AI-generated personalized lessons** (dynamic per kid), not lecture or open chat. |
| **AI (1) – Lesson generation** | "Generate the personalized lesson"; "knowledge graph … what do they know and not know? Interest graph"; "cognitive load … working memory … reps … long-term memory." | **Most of the 2 hours**: curriculum/tutor content driven by knowledge + interest + cognitive load. |
| **AI (2) – Vision / coaching** | "Vision models … watching the screen"; "stream the screen … AI is watching … you're scrolling, you're guessing … you're not listening to the explanation." | **Continuous during the block**: real-time focus/behavior monitoring and in-the-moment coaching. |
| **Modality** | "Dual coding … visual and auditory at the same time." | Lessons use **both** visual and auditory presentation. |
| **No open chat** | "We don't have chat functionality enabled" in the morning; "chat steals that away … we want to fill kids with ideas"; "even our best kids, they all use it to cheat." | **Structured lessons only**; no general-purpose chat during the 2 hours. |
| **Platform / apps** | Timeback platform; "Math Academy," "Alpha Read," "Alpha Write," best-in-class third-party apps. | 2 hours = time inside **Timeback + these apps**; no separate "homework" screen time. |
| **Adults in room** | "Guides" — "not teaching academics"; "Did you check your resources? … Were you reading the explanation?"; motivation, dance parties, high standards. | **Guides do not deliver curriculum**; they motivate and coach "learning how to learn," so screen time = AI + apps. |

**Summary for companion-self:** The 2 hours are **personalized, mastery-oriented, one-to-one screen lessons** (READ/math/science/writing) with **breaks every ~30 minutes**, **no open chat**, **dual coding**, and optional **vision/behavior coaching**. Companion-Self's equivalent 2-hour window should target the same *type* of activity: curriculum/tutor-driven intake and practice, Record capture, and review—not unfocused chat or entertainment.

---

## 2. Companion-Self calibration

Companion-Self targets the **same 2-hour window** for all screen-time learning:

- **Design constraint:** Structure the product and ritual so that curriculum, tutor use, Record capture, and any screen-based learning (READ, WRITE, and screen-linked WORK) are **designed to fit within 2 hours per day**. The Record and pipeline support this: capture and review can be part of the block or immediately after; export feeds curriculum/tutor that operates inside the block.
- **Equivalent metric:** When comparing companion-self (or an instance) to Alpha, **2 hours of screen time per day** is the common denominator. Outcomes (mastery, evidence, motivation) can be compared **per 2-hour block** or **per day** so that “2 hours = full academic coverage” is the shared frame.
- **Time back:** Anything that reduces required screen time below 2 hours (e.g. more efficient capture, faster review) preserves “time back” for the companion; 2 hours is the **ceiling** for mandatory screen-based learning, not a minimum to fill.

---

## 3. What counts as screen time (for the metric)

For the **equivalent metric**, screen time includes:

- Time in curriculum/tutor apps (Khan, IXL, AI tutor, etc.) that feed the Record.
- Time in the companion-self student interface (dashboard, “we did X,” review queue, export).
- Time in Voice/chat that is part of the learning or capture flow.
- Any other screen-based activity that is explicitly part of the **learning block** (READ/WRITE/screen WORK).

Excluded from the 2-hour **learning** metric: non-learning screen use (e.g. entertainment), and optional off-screen activity (life skills, WORK that isn’t on screen). Instances may define precise boundaries (e.g. “session type: learning” vs “session type: other”).

---

## 4. Use in product and roadmap

- **Student app:** Where applicable, surface or assume a **daily 2-hour learning block** (e.g. session timer, “today’s block” summary, or copy: “Designed for up to 2 hours of screen-based learning per day.”).
- **Export / curriculum profile:** Optional field or note: `screen_time_target_minutes: 120` so curriculum/tutor integrations can align to the same window.
- **Roadmap and proof:** When reporting “90% Alpha value,” the 2-hour screen-time target is the **time-equivalent** basis: we deliver comparable value within the same 2-hour screen-time budget.
- **Recursive self-learning:** Objectives (edge, mastery, motivation) are calibrated so that progress is achievable **within** the 2-hour block when combined with external curriculum/tutor.

---

## 5. Reference

- Alpha School / Moonshots #233 — “Full academic program with only two hours a day of academic education”; “we’ve really figured out how to use technology to deliver these really incredible learning results and do it in a fraction of the time.”
- Section 1.1 composition table is estimated from the same Moonshots #233 transcript (structure, AI dimensions, no chat, dual coding, breaks every 30 min).
- [ROADMAP-3Y-90-10](roadmap-3y-90-10.md) — 90% value at 10% cost; 2-hour target is the time-equivalent metric.
- [PROJECT-6WEEK-CODING](project-6week-coding.md) — Student interface can surface or assume the 2-hour block.
