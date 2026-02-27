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

App at **http://localhost:3000**. No env vars for demo.

---

## What you can do

1. **Open** the app (local or deployed)
2. **See** your Record summary (knowledge, curiosity, personality, skills)
3. **Submit** "we did X" and have it staged
4. **Review** pending items and approve or reject
5. **See** your Record update after approve (self-evidence + SELF)
6. **See** "what's next" / edge (THINK, WRITE, WORK)
7. **Download** curriculum profile (JSON) for tutor or curriculum

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
