---
name: companion-self-first-hour
description: First time opening companion-self in Cursor — orient (template vs instance vs demo), optional seed-phase validation smoke test, optional student app. Use when a new contributor or template editor wants a quick map of the repo or to verify demo validation runs.
---

# Companion-self — first hour in Cursor

Use when someone opens **companion-self** for the first time (or returns after a long gap) and wants orientation or a **smoke test**.

## 1. Orient

1. Read root **`README.md`** (template vs instance; Contents).
2. Skim **`companion-self-bootstrap.md`** for first-run / continue flow.
3. Return a short **“you are here”** map:
   - **Template** = this repo’s docs, schemas, `_template`, `demo`
   - **Instance** = e.g. [Grace-Mar](https://github.com/rbtkhn/grace-mar) (not this repo’s Record)
   - **Demo** = `users/demo/` — synthetic only, not a real person

## 2. Optional — seed-phase validation (demo)

If the user wants to confirm tooling works:

```bash
pip install -r scripts/requirements-seed-phase.txt
python3 scripts/validate-seed-phase.py users/demo/seed-phase
python3 scripts/generate-seed-dossier.py users/demo/seed-phase
```

(Adjust paths if demo layout changes; see `README.md` and `docs/seed-phase-validation.md`.)

## 3. Optional — student app

If they want the UI locally: follow **`readme-student-app.md`** (`cd app`, `npm install`, `npm start`).

## Guardrails

- **Do not** treat **`users/demo/`** as a real Record or merge demo content into identity truth.
- **Do not** write to a **grace-mar** folder from this workspace unless the user explicitly overrides (see `.cursor/rules/workspace-boundary.mdc`).
