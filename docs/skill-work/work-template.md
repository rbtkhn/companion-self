# Work territory template — new `work-*` lane

**Purpose:** Checklist and README skeleton for adding a **new** WORK territory under `docs/skill-work/work-<name>/` in this repo or in a **forked instance**. Reduces drift (missing history, unclear boundaries, wrong gate expectations).

**Not:** A replacement for [`users/_template/`](../../users/_template/) (that scaffolds **instances** and Record-shaped files, not skill-work lane folders). **Not** Record truth.

---

## Before you create files

1. **Pick a stable folder name:** `work-<short-id>/` (lowercase, hyphenated). Avoid colliding with existing [skill-work README](README.md) rows.
2. **Decide lane scope:** one primary objective; what is in / out of bounds; whether content ever crosses into **SELF / EVIDENCE / prompt** (then **RECURSION-GATE** + companion approval only in the instance).
3. **Read once:** [concept.md](../concept.md), [identity-fork-protocol.md](../identity-fork-protocol.md), [instance-patterns.md](../instance-patterns.md). In a live instance, also read that repo’s **AGENTS.md** (gate, knowledge boundary) and any **work-menu** conventions the instance maintains.
4. **Run a lane survey** (recommended): `.cursor/skills/lane-survey/SKILL.md` — scan existing tools and approaches before building. Don’t build what already exists.

---

## Required (minimum viable lane)

| Step | Artifact | Notes |
|------|----------|--------|
| 1 | `docs/skill-work/work-<id>/README.md` | Use [skeleton](#readme-skeleton) below; **Objective**, **Boundary**, **Not**. |
| 2 | `docs/skill-work/work-<id>/work-<id>-history.md` | Append-only log per [work-modules-history-principle.md](work-modules-history-principle.md). |
| 3 | Register the territory | Add a row to [skill-work README.md](README.md) submodule table (or legacy note if merged elsewhere). |
| 4 | Register history file | Add a row to the **Existing logs** table in [work-modules-history-principle.md](work-modules-history-principle.md). |

---

## Recommended (most lanes)

| Step | Artifact | When |
|------|----------|------|
| A | `LANE-CI.md` | PRs use a GitHub label such as **`lane/work-<id>`**; align with the instance’s PR template / CI docs. |
| B | `work-<id>-sources.md` | External channels / feeds / accounts that orient the lane — [work-modules-sources-principle.md](work-modules-sources-principle.md). |
| C | Cross-links in README | Point to adjacent territories and any scripts under `scripts/`. |

---

## Optional

- **Scripts** under `scripts/` or `scripts/work_<id>/` — document invocations in README.
- **Cursor skills** under `.cursor/skills/` — when the lane has a stable operator trigger (instances may use a portable skill ladder if present).
- **Template → instance** — if the new tree should ship to **every** fork, plan an upgrade slice per [how-instances-consume-upgrades.md](../how-instances-consume-upgrades.md). Instance-only lanes can stay private to that instance.

---

## README skeleton

Copy into `README.md` and replace placeholders.

```markdown
# work-<id>

**Objective:** _One sentence — what this lane is for._

_Not:_ Record truth; not Voice knowledge; not a substitute for `users/<id>/self.md` or RECURSION-GATE queue (unless you document explicit gate use).

---

## Purpose

| Role | Description |
|------|-------------|
| _Primary_ | _…_ |
| _Secondary (optional)_ | _…_ |

---

## Boundary

- **WORK-only** drafts and operator notes live here.
- **Promotion to Record / Voice:** only via **RECURSION-GATE** + companion approval + merge script per the instance’s **AGENTS.md**.
- **Relation to other lanes:** _…_

---

## Contents _(optional table)_

| Doc / path | Role |
|------------|------|
| `README.md` | This file |
| `work-<id>-history.md` | Operator trail |
| `work-<id>-sources.md` | Authorized sources _(if present)_ |
| `LANE-CI.md` | PR label convention _(if present)_ |

---

## Related

- [work-template.md](work-template.md) (this checklist)
- [work-modules-history-principle.md](work-modules-history-principle.md)
- [work-modules-sources-principle.md](work-modules-sources-principle.md)
```

---

## Governance reminder

- **Stage, do not merge** gate candidates unless the companion approves and the operator runs the instance’s merge flow.
- **Knowledge boundary** for Voice-facing output: follow the instance’s governance; do not leak undocumentable claims into the Record from WORK drafts.

---

**Last updated:** 2026-04-04 (mirrored from grace-mar; template-adapted paths)
