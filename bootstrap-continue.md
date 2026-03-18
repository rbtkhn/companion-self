# Bootstrap: Continue in New Agent Session

**Use this file when starting a new Cursor conversation in the companion-self repo.** Open this file and say: *"Read bootstrap-continue.md and continue from here."* The agent will have full context to resume work.

---

## 1) Quick context

- **Repo:** companion-self (template). Grace-mar = first instance (read-only in this workspace).
- **Workspace rule:** Do not write to or modify grace-mar from this workspace unless the user explicitly requests it.
- **Long-term objectives:** See [docs/long-term-objective.md](docs/long-term-objective.md) — democratize Alpha-style education, companion sovereignty (human-approval gate), knowledge boundary.

---

## 2) Current project state

| Area | Status | Notes |
|------|--------|-------|
| Phase A–E (docs, template) | Done | README, concept, protocol, seed-phase, users/_template, how-instances-consume-upgrades |
| Phase F (consistency, handoff) | Pending | F1 cross-check, F2 bootstrap, F3 template-manifest |
| **Task 1** (schema/spec consistency) | **Pending** | `app/schema/record.js`, `docs/schema-record-api.md`, `docs/project-6week-coding.md` |
| **Task 2** (student UI accessibility) | **Done** | ARIA, live regions, focus visibility in `app/public/*.html` and `style.css` |
| Market research | Done | `docs/market-research-timeback-alpha-thirdparty.md` — 10 implementable proposals |

---

## 3) Key paths

| Path | Purpose |
|------|---------|
| `companion-self-bootstrap.md` | Full bootstrap (first-run, parallel tasks §10) |
| `docs/companion-self-developer-plan.md` | Phases A–F checklist |
| `docs/tasks-parallel-cursor-conversations.md` | Task 1 & 2 briefs, scope, acceptance criteria |
| `docs/long-term-objective.md` | Permanent system rules; check alignment |
| `docs/market-research-timeback-alpha-thirdparty.md` | Market research; 10 proposals with pros/cons |
| `app/public/` | Student UI (dashboard, activity, review, export) |
| `app/schema/record.js` | Record schema (Task 1 scope) |

---

## 4) Commands

```bash
# Run eval fixtures (after schema/pipeline changes)
node scripts/run-eval-fixtures.js

# Start dev server (if needed for UI check)
node app/server.js   # or npm start — check package.json
```

---

## 5) Suggested next steps

1. **Task 1 (schema/spec):** Read `docs/tasks-parallel-cursor-conversations.md` Task 1. Edit `record.js`, `schema-record-api.md`, `project-6week-coding.md`. Run eval fixtures.
2. **Phase F:** Complete F1 (cross-check), F2 (bootstrap), F3 (template-manifest) per developer plan.
3. **Other:** User may specify a different task (e.g. refine market research, add features, fix bugs).

---

## 6) What was done recently (prior session)

- **Student UI accessibility (Task 2):** ARIA labels on nav, activity textarea/skill dropdown, Approve/Reject; `aria-live="polite"` on form feedback; `:focus-visible` for links/buttons/inputs; `.visually-hidden` for hints.
- **Market research:** Deep research on TimeBack, Alpha apps, third-party edtech; 10 proposals with pros/cons written to `docs/market-research-timeback-alpha-thirdparty.md`.

---

**End of bootstrap.** Use this file to continue seamlessly.
