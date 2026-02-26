# 6-Week Coding Project: Student Product Interface

**Companion-Self template · Convert 3-year roadmap into a shippable student-facing product**

This document turns the [3-year roadmap (90% Alpha value at 10% cost)](roadmap-3y-90-10.md) into a **6-week coding project**. All work is implemented **in the companion-self repo**. The deliverable is the **product/service interface given to the student**: a minimal web app the student (or operator on their behalf) uses to see their Record, submit "we did X," review and approve candidates, view progress and edge, and export for curriculum/tutor.

**Audience:** Developer or team implementing in companion-self. **Student** = the end user (learner/companion) who receives this interface.

**Time calibration:** Companion-Self targets **2 hours of screen time per day** for all screen-based learning (aligned with Alpha). The student interface and any curriculum/tutor use are designed to fit within that window. See [two-hour-screentime-target](two-hour-screentime-target.md).

---

## Scope and principles

- **In scope:** Schema in code, demo user (`users/demo/`), pipeline (stage → review → merge), student UI (Record summary, "we did X," review queue, approve/reject, edge, export). No real Record data in repo; demo user only.
- **Out of scope for 6 weeks:** LLM analyst, Voice/chat, curriculum integration, auth (single-user/demo ok), hosting. Can be added later by instance or extension.
- **Tech:** Minimal stack that runs from repo root: **Node + Express** (or **Python + Flask**), simple HTML + vanilla JS (or minimal framework). Data: markdown + JSON under `users/demo/`. No database required.

---

## Repo layout after 6 weeks

```
companion-self/
├── docs/                    # existing
├── users/
│   ├── _template/           # existing
│   └── demo/                # demo user for student interface
│       ├── self.md
│       ├── self-skill-read.md
│       ├── self-skill-write.md
│       ├── self-skill-work.md
│       ├── self-evidence.md
│       ├── recursive-gate.json   # staged candidates (machine-readable)
│       └── self-memory.md   # optional
├── app/                     # NEW: student-facing application
│   ├── package.json        # or requirements.txt
│   ├── server.js           # or app.py (Express/Flask)
│   ├── schema/             # Record schema and types
│   │   └── record.js       # or record.py
│   ├── pipeline/           # stage and merge logic
│   │   ├── stage.js
│   │   └── merge.js
│   ├── export/             # curriculum profile export
│   │   └── curriculum-profile.js
│   └── public/             # front-end
│       ├── index.html      # dashboard
│       ├── activity.html   # "we did X" form
│       ├── review.html     # approve/reject queue
│       ├── export.html     # download profile
│       └── assets/
│           └── app.js
├── scripts/                # optional CLI entrypoints
│   ├── run-seed.js         # first-time survey → populate demo SELF
│   └── export-profile.js   # CLI export
└── readme-student-app.md    # how to run and use (for student/operator)
```

---

## Week 1: Schema, data model, demo user

**Goal:** Record and pipeline data structures in code; demo user on disk; load/save.

### Tasks

| # | Task | Deliverable |
|---|------|-------------|
| 1.1 | Define **Record schema** in code: SELF (self.md baseline), IX-A/IX-B/IX-C from self-knowledge.md, self-curiosity.md, self-personality.md, self-skill-read / self-skill-write / self-skill-work (READ, WRITE, WORK with optional level/edge), self-evidence (list of activities with id, type, summary, date, skill tag). | `app/schema/record.js` (or .py) with types and validation. |
| 1.2 | Define **recursive-gate** structure: array of `{ id, raw_text, skill_tag, mind_category, suggested_ix_section, created_at, status }`. | Schema in code; `users/demo/recursive-gate.json` format. |
| 1.3 | Create **users/demo/** with self.md, self-knowledge.md, self-curiosity.md, self-personality.md, self-skill-read.md, self-skill-write.md, self-skill-work.md, self-evidence.md, self-memory.md from `users/_template/`; add recursive-gate.json (empty array). Populate demo with minimal seed (e.g. one line each in self-knowledge, self-curiosity, self-personality). | Demo user runnable; parsable by app. |
| 1.4 | Implement **load** and **save** for demo user: read markdown into structured objects (or simplified key sections); write back on merge. Use simple markdown parsing (e.g. section headers + lists) or keep minimal and append-only where possible. | `app/schema/record.js` (or pipeline/io.js) load/save. |
| 1.5 | Document schema in `docs/schema-record-api.md` (minimal: field list, recursive-gate shape). | Doc for future extensions. |

### Success

- Running `node app/schema/record.js` (or equivalent) loads `users/demo/` and returns a Record object. Save updates files.

---

## Week 2: Pipeline — stage "we did X"

**Goal:** Student (or operator) submits "we did X"; backend stages a candidate into recursive-gate. No LLM; rule-based or manual tagging.

### Tasks

| # | Task | Deliverable |
|---|------|-------------|
| 2.1 | **API:** POST `/api/activity` body `{ text, skill_tag? }` (skill_tag = READ | WRITE | WORK). Create candidate: id (uuid or timestamp), raw_text, skill_tag, mind_category inferred from keyword or default to "curiosity", suggested_ix_section (e.g. IX-B), created_at, status: "pending". Append to recursive-gate.json. | POST endpoint; recursive-gate grows. |
| 2.2 | **API:** GET `/api/recursive-gate` returns list of pending candidates. | Used by review UI. |
| 2.3 | Optional: **CLI** `node scripts/stage-activity.js "We read a book about volcanoes"` for testing. | Script. |
| 2.4 | Ensure **idempotent** and **append-only** for stage; no overwrite of existing candidates. | Safe staging. |

### Success

- Submitting "We drew a dragon" and "We read chapter 3" creates two pending candidates. GET returns them.

---

## Week 3: Student UI — dashboard and "we did X"

**Goal:** Student-facing pages: home (Record summary), "we did X" form, link to review queue.

### Tasks

| # | Task | Deliverable |
|---|------|-------------|
| 3.1 | **Dashboard** (e.g. `/` or `/dashboard`): Load demo Record; show summary: Knowledge (IX-A from self-knowledge.md), Curiosity (IX-B from self-curiosity.md), Personality (IX-C from self-personality.md), Skills (READ/WRITE/WORK with simple edge or last activity). Show count of items at recursive-gate; link to review. | index.html + app.js; GET /api/record or /api/summary. |
| 3.2 | **"We did X" page** (e.g. `/activity`): Single textarea + optional skill dropdown (READ/WRITE/WORK) + Submit. On submit, POST to /api/activity; show success; optional redirect to dashboard or review. | activity.html + form handler. |
| 3.3 | **API:** GET `/api/record` or `/api/summary` returns Record summary (and optionally full Record) for demo user. | Backend. |
| 3.4 | Simple **navigation**: Dashboard | We did X | Review queue | Export. No auth; single-user demo. | Nav in all pages. |
| 3.5 | **Static assets** served from `app/public/`; server serves HTML and API. | Express static + routes. |

### Success

- Student opens app; sees Record summary and can submit "we did X"; sees pending count and can open review.

---

## Week 4: Review queue and merge

**Goal:** Student (or operator) sees recursive-gate list; approves or rejects each; on approve, merge into Record and self-evidence.

### Tasks

| # | Task | Deliverable |
|---|------|-------------|
| 4.1 | **Review page** (e.g. `/review`): GET pending candidates; display each with raw_text, skill_tag, suggested section; [Approve] [Reject] buttons. | review.html + app.js. |
| 4.2 | **API:** POST `/api/review` body `{ candidate_id, action: "approve" | "reject" }`. Reject: remove from recursive-gate (or set status rejected). Approve: call merge logic; then remove from queue. | Backend. |
| 4.3 | **Merge logic:** For approved candidate, (1) append to self-evidence.md as new activity (id, date, summary, skill_tag); (2) append one line to the appropriate **dimension file** from suggested_ix_section: self-knowledge.md (IX-A), self-curiosity.md (IX-B), or self-personality.md (IX-C); (3) optionally append to the appropriate self-skill-* file (READ/WRITE/WORK) as one evidence link. Keep merge simple: append only; no dedup for 6 weeks. | `app/pipeline/merge.js`. |
| 4.4 | **Idempotency:** One approve = one merge; candidate removed so cannot approve twice. | Safe merge. |
| 4.5 | Optional: **Merge receipt** append to a log file (e.g. `users/demo/merge-receipts.jsonl`) for proof architecture. | Receipt. |

### Success

- Student approves one candidate; self-evidence.md and the appropriate dimension file (self-knowledge, self-curiosity, or self-personality) update; candidate removed from queue. Reject removes from queue only.

---

## Week 5: Edge and export

**Goal:** Compute and show "edge" (next suggested focus); export curriculum profile for tutor/curriculum.

### Tasks

| # | Task | Deliverable |
|---|------|-------------|
| 5.1 | **Edge derivation:** From self-skill-read, self-skill-write, self-skill-work + self-evidence, compute simple edge: e.g. last topic per READ/WRITE/WORK, or "next" suggestion (e.g. "Add another READ" / "Try a WORK project"). No LLM; rule-based. Expose as GET `/api/edge` or part of `/api/record`. | Backend + schema. |
| 5.2 | **Dashboard:** Show edge or "What’s next" (e.g. "READ: keep reading at your level" / "WRITE: try a short story" / "WORK: one small project"). | UI. |
| 5.3 | **Export:** Build `curriculum_profile` object from self-knowledge.md (IX-A topics), self-curiosity.md (IX-B), self-personality.md (IX-C snippets), READ/WRITE/WORK edge, evidence count, export date. | `app/export/curriculum-profile.js`. |
| 5.4 | **API:** GET `/api/export` or `/api/curriculum-profile` returns JSON. Include optional `screen_time_target_minutes: 120` in export so curriculum/tutor can align to the 2-hour block. Optional: GET `/api/export/download` returns file download. | Backend. |
| 5.5 | **Export page** (e.g. `/export`): Button "Download curriculum profile"; downloads JSON (or markdown summary) so student can hand to tutor or curriculum. | export.html. |
| 5.6 | **2-hour target in UX:** On dashboard or activity page, show short line: "Designed for up to 2 hours of screen-based learning per day" (or link to two-hour-screentime-target). Optional: simple "Today's block" or session placeholder (e.g. "0 / 120 min") for future expansion. | UI copy; optional session metric. |

### Success

- Student sees "What’s next" on dashboard; can download a curriculum profile JSON (with optional `screen_time_target_minutes: 120`) that a tutor or Khan/IXL could consume. 2-hour target is visible as design/compare metric.

---

## Week 6: Polish, run instructions, handoff

**Goal:** App runs from repo; clear instructions for student/operator; optional seed flow; doc for "student product."

### Tasks

| # | Task | Deliverable |
|---|------|-------------|
| 6.1 | **Run instructions:** README or `readme-student-app.md`: clone repo, `cd app`, `npm install`, `npm run dev` (or `python app.py`). App runs at e.g. http://localhost:3000. No env vars required for demo. | Doc. |
| 6.2 | **Optional seed flow:** First-run or `/seed`: short survey (e.g. 3–4 questions: favorite book, favorite thing to make, one thing you’re curious about). Write answers into demo self.md (baseline) and/or self-curiosity.md, self-personality.md as appropriate. | Script or /seed page. |
| 6.3 | **Error handling:** Graceful message if `users/demo/` missing or malformed; empty state for empty recursive-gate. | UX. |
| 6.4 | **Link from main README:** "Student interface: see [readme-student-app](readme-student-app.md) and run the app in `app/`." | README. |
| 6.5 | **Definition of done:** Student can (1) open app, (2) see Record summary, (3) submit "we did X", (4) open review, (5) approve/reject and see Record update, (6) see edge / what’s next, (7) download export. All in companion-self repo. | Checklist. |

### Success

- New user clones companion-self, runs app, completes full loop in &lt; 10 minutes. Student receives this as the product interface.

---

## Tech stack (recommended)

| Layer | Choice | Rationale |
|-------|--------|-----------|
| **Runtime** | Node 18+ or Python 3.10+ | Single install; no DB. |
| **Server** | Express (Node) or Flask (Python) | Minimal; serve static + JSON API. |
| **Front-end** | HTML + vanilla JS | No build step; or minimal Vite if preferred. |
| **Data** | `users/demo/*.md` + `recursive-gate.json` | Git-friendly; matches template. |
| **Schema** | JS objects or Python dataclasses; markdown parsed by section | No DB schema; easy to evolve. |

---

## Mapping from 3-year roadmap to 6 weeks

| Roadmap (Year 1) | 6-week implementation |
|------------------|------------------------|
| Curriculum-consumable export | Week 5: curriculum_profile JSON + download. |
| Pipeline and edge | Week 2: stage; Week 4: merge; Week 5: edge derivation. |
| Hosted family product | Week 3–6: student UI; "hosted" = run server (instance can deploy). |
| Proof architecture | Week 4: optional merge receipts; Week 6: doc. |
| Seed and onboarding | Week 1: demo user; Week 6: optional seed survey. |
| "We did X" first-class | Week 2–3: submit; Week 4: review and merge. |

---

## Out of scope for 6 weeks (later)

- LLM analyst (auto-suggest IX-A/IX-B/IX-C from raw text).
- Voice / chat interface.
- Auth and multi-user (beyond single demo user).
- Real curriculum or tutor integration (only export format).
- Vision or screen monitoring.
- Hosting and production deploy (instance responsibility).

---

## Definition of done (student product)

The **student** (or operator) can:

1. **Open** the app (local or deployed).
2. **See** their Record summary (knowledge, curiosity, personality, skills).
3. **Submit** "we did X" and have it staged.
4. **Review** pending items and approve or reject.
5. **See** their Record update after approve (self-evidence + SELF).
6. **See** "what’s next" / edge (READ, WRITE, WORK).
7. **Download** curriculum profile (JSON) to give to a tutor or curriculum.

All implemented **in companion-self**, deliverable as the **product/service interface** given to the student.
