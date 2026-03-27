# Student interface — how to run

**Companion-Self** student-facing app. For the student (or operator) to see their Record, submit "we did X," review and approve candidates, view edge, and export curriculum profile.

---

## Quick start

```bash
git clone https://github.com/rbtkhn/companion-self.git
cd companion-self/app
npm install
npm start
```

App at **http://localhost:3000**. No env vars for demo. The app runs as user **demo** by default. Optional: `?user=<id>` or header `X-User-Id` (user must be listed in `app/config/allowed-users.json`). Template ships with `["demo"]` only; instances can add users for multi-user mode.

---

## What you can do

1. **Open** the app (local or deployed)
2. **See** your Record summary (knowledge, curiosity, personality, skills)
3. **Submit** "we did X" and have it staged
4. **Review** pending items and approve or reject
5. **See** your Record update after approve (self-evidence + SELF)
6. **See** "what's next" / edge (THINK, WRITE, WORK)
7. **Download** curriculum profile (JSON) for tutor or curriculum
8. **Seed Phase** — Open **[/seed-phase](http://localhost:3000/seed-phase)** to view pre-activation demo (or `_template` scaffold) readiness, confidence map, stages, and dossier preview via **GET `/api/seed-phase?profile=demo`**. Does not read the live Record.
9. **Change review (demo)** — Open **[/change-review](http://localhost:3000/change-review)** for post-seed governed-change JSON (proposal, decision, queue, events, identity diff) via **GET `/api/change-review?profile=demo`**. On-disk layout is **`users/<profile>/review-queue/`** (see repo root). **`profile=template`** can load once **`users/_template/review-queue/`** exists (scaffold ships in the template). The API implementation may still expect the legacy flat `change-review` directory until updated to aggregate `review-queue` files. Not the live Record.

---

## Prerequisites

- **Node 18+**
- `users/demo/` must exist (created in Week 1). If missing, the app will show a graceful error.

---

## Scripts

| Command | Description |
|---------|-------------|
| `npm start` | Start server (port 3000) |
| `npm run dev` | Same as start |

---

## Tech

- **Server:** Express
- **Data:** `users/demo/*.md` + `recursion-gate.json` — no database
- **Front-end:** HTML + vanilla JS
