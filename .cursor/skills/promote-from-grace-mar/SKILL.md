---
name: promote-from-grace-mar
description: Turn read-only Grace-Mar reference into a safe companion-self template change — checklist, strip instance data, proposal only. Use when porting patterns from the first instance into the upstream template.
---

# Promote from Grace-Mar (template-side)

Use when the user wants to **upstream** ideas from **grace-mar** into **companion-self**.

## 1. Boundary

- Respect **`.cursor/rules/workspace-boundary.mdc`**: **no writes** to grace-mar from this workspace unless the user **explicitly** overrides.
- Work **only** in companion-self files unless override.

## 2. Checklist before proposing or editing

- Remove **user id** `grace-mar`, **PII**, **secrets**, and paths like **`users/grace-mar/**`** from any pasted or adapted content.
- Do not copy **Record** prose or **EVIDENCE** as template canon; **generalize** into protocol, schema, or docs.
- Check **`template-manifest.json`** and **`docs/instance-patterns.md`** when paths or “how instances differ” matter.
- Prefer **links** to Grace-Mar for narrative examples instead of duplicating private instance files.

## 3. Output shape

1. Short **proposal**: intended files, rationale, risks.
2. Implement in companion-self **after** human approval (or implement small doc-only fixes if the user already said to apply).

## 4. Multi-root workspace

If **companion-self-and-grace-mar.code-workspace** is open: read grace-mar for comparison; still **default** to **no grace-mar modifications** from this workflow.
