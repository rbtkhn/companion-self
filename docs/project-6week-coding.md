# 6-Week Coding Project: Student Product Interface

**Companion-Self template · Shippable student-facing product**

This document defines a **6-week coding project** implemented **in the companion-self repo**. The deliverable is the **product/service interface given to the student**: a minimal web app the student (or operator on their behalf) uses to see their Record, submit "we did X," review and approve candidates, view progress and edge, and export for curriculum/tutor.

**Audience:** Developer or team implementing in companion-self. **Student** = the end user (learner/companion) who receives this interface.

**Time calibration:** Companion-Self targets **2 hours of screen time per day** for all screen-based learning (aligned with Alpha). The student interface and any curriculum/tutor use are designed to fit within that window. See [Alpha School reference (skill-work)](skill-work/alpha-school-reference.md) §3 Two-hour screen-time target.

### Regression

After **schema or pipeline changes** (Weeks 1, 2, or 4), run the eval fixtures to avoid regressions:

```bash
node scripts/run-eval-fixtures.js
```

See [Evaluation design and regression](evaluation-design-and-regression.md) for fixture design and when to add cases.

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
│       ├── self-knowledge.md
│       ├── self-curiosity.md
│       ├── self-personality.md
│       ├── self-skill-think.md
│       ├── self-skill-write.md
│       ├── self-skill-work.md
│       ├── self-evidence.md
│       ├── recursion-gate.json   # staged candidates (machine-readable)
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

**Prerequisite:** None.

### Tasks

| # | Task | Deliverable |
|---|------|-------------|
| 1.1 | Define **Record schema** in code: SELF (self.md), IX-A/IX-B/IX-C (self-knowledge, self-curiosity, self-personality), THINK/WRITE/WORK (self-skill-*), self-evidence (id, type, summary, date, skill_tag). | `app/schema/record.js` (or .py) with types and validation. |
| 1.2 | Define **recursion-gate** structure: array of `{ id, raw_text, skill_tag, mind_category, suggested_ix_section, created_at, status }`. | Same schema module; `users/demo/recursion-gate.json` format. |
| 1.3 | Create **users/demo/** from `users/_template/` (all Record + recursion-gate.json empty array). Populate minimal seed (one line each in self-knowledge, self-curiosity, self-personality). | Demo user on disk; parsable by app. |
| 1.4 | Implement **load** and **save** for demo: read markdown into structured objects; write back on merge. Append-only where possible; simple section/list parsing. | Load/save in schema or `pipeline/io.js`. |
| 1.5 | Add and maintain `docs/schema-record-api.md`: ensure it exists with Record field list and recursion-gate shape. Week 5 adds edge response shape. | Doc for API contract and extensions. |

### Success

- Running load (e.g. `node app/schema/record.js`) loads `users/demo/` and returns a Record object; save updates files.

---

## Week 2: Pipeline — stage "we did X"

**Goal:** Student submits "we did X"; backend stages a candidate into recursion-gate. No LLM; rule-based or manual tagging.

**Prerequisite:** Week 1 (schema, demo user, load/save).

### Tasks

| # | Task | Deliverable |
|---|------|-------------|
| 2.1 | **API:** POST `/api/activity` body `{ text, skill_tag? }` (skill_tag = THINK, WRITE, or WORK). Create candidate: id, raw_text, skill_tag, mind_category (keyword or "curiosity"), suggested_ix_section (e.g. IX-B), created_at, status: "pending". Append to recursion-gate.json. Idempotent, append-only. | POST endpoint. |
| 2.2 | **API:** GET `/api/recursion-gate` returns pending candidates. | For review UI. |
| 2.3 | *Optional:* CLI to stage one activity for testing (e.g. `scripts/stage-activity.js`). | Script. |

### Success

- Submitting "We drew a dragon" and "We read chapter 3" creates two pending candidates. GET returns them.

---

## Week 3: Student UI — dashboard and "we did X"

**Goal:** Student-facing pages: home (Record summary), "we did X" form, link to review queue.

**Prerequisite:** Week 1 (load/save), Week 2 (POST /api/activity, GET /api/recursion-gate).

### Tasks

| # | Task | Deliverable |
|---|------|-------------|
| 3.1 | **API:** GET `/api/record` returns Record summary for demo user (IX-A/IX-B/IX-C, skills, optional full Record). Consumed by dashboard and later by edge/export. | Backend. |
| 3.2 | **Dashboard** (e.g. `/` or `/dashboard`): Call GET /api/record; show Knowledge, Curiosity, Personality, Skills; pending count (from GET /api/recursion-gate or include in /api/record); link to review. | index.html + app.js. |
| 3.3 | **"We did X" page** (e.g. `/activity`): Textarea + skill dropdown (THINK/WRITE/WORK) + Submit → POST /api/activity; success state; optional redirect to dashboard or review. | activity.html + form handler. |
| 3.4 | **Navigation:** Dashboard, We did X, Review, Export on all pages. Static from `app/public/`; server serves HTML + API. | Nav + Express static and routes. |

### Success

- Student opens app; sees Record summary and can submit "we did X"; sees pending count and can open review.

---

## Week 4: Review queue and merge

**Goal:** Student sees recursion-gate list; approves or rejects each; on approve, merge into Record and self-evidence.

**Prerequisite:** Weeks 1–3 (Record load/save, staging APIs, UI with nav).

### Tasks

| # | Task | Deliverable |
|---|------|-------------|
| 4.1 | **Review page** (e.g. `/review`): GET pending candidates; show raw_text, skill_tag, suggested_ix_section; [Approve] [Reject] per candidate. | review.html + app.js. |
| 4.2 | **API:** POST `/api/review` body `{ candidate_id, action: "approve" or "reject" }`. Reject: remove from gate. Approve: run merge, then remove from queue. One approve = one merge (idempotent). | Backend. |
| 4.3 | **Merge logic:** For approved candidate: (1) append to self-evidence.md (id, date, summary, skill_tag); (2) append one line to dimension file from suggested_ix_section (self-knowledge, self-curiosity, or self-personality); (3) optionally append to matching self-skill-*. Append-only; no dedup. | `app/pipeline/merge.js`. |
| 4.4 | *Optional:* Merge receipt log (e.g. `users/demo/merge-receipts.jsonl`) for proof architecture. | Receipt. |

### Success

- Student approves one candidate; self-evidence.md and the appropriate dimension file (self-knowledge, self-curiosity, or self-personality) update; candidate removed from queue. Reject removes from queue only.

---

## Week 5: Edge and export

**Goal:** Compute and show "edge" (next suggested focus); export curriculum profile for tutor/curriculum.

**API contract (edge / "what's next"):** GET `/api/edge` (or edge in GET `/api/record`) returns suggested next focus per THINK, WRITE, WORK. Document response shape in `docs/schema-record-api.md` for UI and export consumers. **WORK and self-personality (IX-C):** When deriving WORK edge or phrasing "what's next," use self-personality (voice, preferences, values, narrative) so suggestions match how the companion works and sound like them. See [CONCEPT](concept.md) §4 "How WORK utilizes self-personality (IX-C)."

**Prerequisite:** Weeks 1–4 (Record, merge; edge derives from current Record).

### Tasks

| # | Task | Deliverable |
|---|------|-------------|
| 5.1 | **Edge derivation:** From self-skill-* + self-evidence (and for WORK, self-personality / IX-C when available), compute simple edge (e.g. last topic or "next" per THINK/WRITE/WORK). Phrase WORK edge in companion voice/values where possible. Rule-based; no LLM. Expose as GET `/api/edge` or in GET `/api/record`. | Backend; add edge shape to schema-record-api.md. |
| 5.2 | **Dashboard:** Show "What's next" per skill (e.g. THINK: keep reading; WRITE: try a short story; WORK: one small project). WORK line may use IX-C for phrasing. Include one line: "Designed for up to 2 hours of screen-based learning per day" (or link to [Alpha School reference](skill-work/alpha-school-reference.md) §3). | UI. |
| 5.3 | **Export:** Build `curriculum_profile` from IX-A/IX-B/IX-C, edge, evidence count, export date. GET `/api/export` returns JSON (optional `screen_time_target_minutes: 120`). Optional download response for file. | `app/export/curriculum-profile.js` + backend. |
| 5.4 | **Export page** (e.g. `/export`): Button "Download curriculum profile" → JSON (or markdown summary) for tutor/curriculum. | export.html. |

### Success

- Student sees "What's next" on dashboard (and 2-hour line); can download curriculum profile JSON (optional `screen_time_target_minutes: 120`) for tutor/curriculum.

---

## Week 6: Polish, run instructions, handoff

**Goal:** Clear run instructions; graceful errors and empty states; verify definition of done.

**Prerequisite:** Weeks 1–5 complete.

### Tasks

| # | Task | Deliverable |
|---|------|-------------|
| 6.1 | **Run instructions:** Add `readme-student-app.md` (clone, `cd app`, `npm install`, `npm run dev` or `python app.py`; app at e.g. localhost:3000; no env vars for demo). Link from main README: "Student interface: see readme-student-app.md." | Doc + README link. |
| 6.2 | **Error handling:** Graceful message if `users/demo/` missing or malformed; empty state for empty recursion-gate. | UX. |
| 6.3 | *Optional:* Seed flow (e.g. `/seed` or first-run): short survey → write into demo self.md, self-curiosity.md, self-personality.md. | Script or /seed page. |
| 6.4 | **Definition of done:** Verify student can open app, see Record, submit "we did X", review and approve/reject, see Record update, see edge, download export. See checklist below. | Verification. |

### Success

- New user clones repo, runs app, completes full loop in under 10 minutes.

---

## Tech stack (recommended)

| Layer | Choice | Rationale |
|-------|--------|-----------|
| **Runtime** | Node 18+ or Python 3.10+ | Single install; no DB. |
| **Server** | Express (Node) or Flask (Python) | Minimal; serve static + JSON API. |
| **Front-end** | HTML + vanilla JS | No build step; or minimal Vite if preferred. |
| **Data** | `users/demo/*.md` + `recursion-gate.json` | Git-friendly; matches template. |
| **Schema** | JS objects or Python dataclasses; markdown parsed by section | No DB schema; easy to evolve. |

---

## Mapping to 6 weeks

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

- **Auto triggers for suggested merges** — Staging is one candidate per POST. Instances may add triggers (e.g. on activity type = quiz or assessment, auto-stage evidence + suggested self-knowledge candidate). Implementable pattern: [Ingestion and sources](ingestion-and-sources.md) § Triggers for suggested merges.
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
6. **See** "what’s next" / edge (THINK, WRITE, WORK).
7. **Download** curriculum profile (JSON) to give to a tutor or curriculum.

All implemented **in companion-self**, deliverable as the **product/service interface** given to the student.
