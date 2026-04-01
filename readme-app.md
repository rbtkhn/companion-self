# Companion app — how to run

**Companion-Self** ships a **local demo app** (Express + static HTML) to inspect the Record shape, run the pipeline demo, view seed-phase and change-review bundles, and export a curriculum-style profile. Operators and integrators use the same surface for quick validation.

---

## Quick start

```bash
git clone https://github.com/rbtkhn/companion-self.git
cd companion-self/app
npm install
npm start
```

App at **http://localhost:3000**. No env vars for demo. The app runs as user **demo** by default. Optional: `?user=<id>` or header `X-User-Id` (the id must be listed in `app/config/allowed-users.json`). The template ships with `["demo"]` only; instances can add users for multi-user mode.

When running this demo alongside Grace-Mar local web surfaces, keep the origin split in mind:

- `http://localhost:3000` = companion-self demo
- `http://localhost:5000` = Grace-Mar miniapp / family hub

Because the port differs, browser storage and page-relative `/api/...` calls stay separate by default. See `docs/miniapp-setup.md` in Grace-Mar for the fuller local-dev boundary note.

---

## What you can do

1. **Open** the companion app (local or deployed)
2. **See** your Record summary (knowledge, curiosity, personality, skills)
3. **Submit** "we did X" and have it staged
4. **Review** pending items and approve or reject
5. **See** your Record update after approve (self-evidence + SELF)
6. **See** "what's next" / edge (THINK, WRITE, WORK)
7. **Download** curriculum profile (JSON) for a tutor or external profile consumer
8. **Seed Phase** — Open **[/seed-phase](http://localhost:3000/seed-phase)** to view pre-activation demo (or `_template` scaffold) readiness, confidence map, stages, and dossier preview via **GET `/api/seed-phase?profile=demo`**. Does not read the live Record.

## Change Review page

The app includes a **`/change-review`** page for viewing governed post-seed revision artifacts.

This page reads from **`users/<profile>/review-queue/`** and displays:

- review summary counts
- queue items
- latest decision
- visible diff
- event history

Related API endpoints:

- `GET /api/change-review?profile=demo`
- `GET /api/change-review/summary?profile=demo`

Use `profile=template` for the `_template` scaffold (may be sparse). Not the live Record.

---

## Prerequisites

- **Node 18+**
- `users/demo/` must exist. If missing, the API will return a clear error.

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

## Status microcopy

The normative framework for loading/process wording lives in [docs/status-microcopy.md](docs/status-microcopy.md). This repo now has a small shared microcopy helper in `app/public/assets/app.js`, with primary demo surfaces consuming it directly.

This remains **docs-led** in this pass:

- it defines lane-aware process language
- it now has a lightweight implementation seam in `app/public/assets/app.js`
- primary app surfaces (`app/public/index.html`, `activity.html`, `review.html`, `change-review.html`) can share wording without introducing a larger UI framework

For downstream instances such as Grace-Mar, this app remains an **optional implementation parity surface**. The default sync expectation is still: pull the docs/spec layer first, then decide intentionally whether any `app/` implementation pattern should propagate.

---

*Legacy filename:* [readme-student-app.md](readme-student-app.md) redirects here conceptually; prefer this doc for new links.
