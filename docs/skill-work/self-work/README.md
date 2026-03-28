# self-work — territory (WORK coordination)

**Canonical (template):** This README is maintained in [companion-self](https://github.com/rbtkhn/companion-self). Instances should reconcile after upstream edits using `template_diff.py --use-manifest` (where available) or a documented upgrade slice per `how-instances-consume-upgrades.md`.

**Purpose:** One **cross-lane dashboard** per fork: `users/<id>/self-work.md` — **objectives**, **active threads**, **history**, **strategy**. **Not** IX-A/B/C identity content (that stays in `self.md` + gate). Record shape lives in each instance’s SELF templates (see reference [self-template.md](https://github.com/rbtkhn/grace-mar/blob/main/docs/self-template.md) in grace-mar if you need a worked example).

## Clarity: skill-work vs self-work vs self.md

| Surface | Role | Example |
|---------|------|---------|
| **`docs/skill-work/`** | Many **territories** — deep lane docs (`work-politics`, `work-dev`, …) | Lane handbooks, integration README |
| **`self-work.md`** | **One** operator thread per fork — cross-lane steering | “This month: seed work + client floor + template upgrade order” |
| **`self.md`** | **Record** — SELF-KNOWLEDGE (IX), identity | Survey → gate → merge |

**Anti-patterns:** Long procedures **only** in `self-work` (belongs under **skill-work**). Duplicating a cross-lane story in every lane README (belongs in **`self-work`** or you drift).

**Decision rule:** Lane-specific → that `work-*` doc. Cross-lane sequencing → `self-work.md`. Identity facts → `self.md` + gate.

---

## Optional template module: territory sync pack

Use [sync-pack/README.md](sync-pack/README.md) for a reusable manual sync pattern across instances.

Includes:

- contract template (`SYNC-CONTRACT.template.md`)
- log template (`SYNC-LOG.template.md`)
- optional daily aggregator (`SYNC-DAILY.template.md`, training mode)
- enablement runbook (`ENABLE-SYNC-PACK.md`)

**Instance file:** Each companion keeps `users/<id>/self-work.md` in **their own** instance repo (not in the template Record).

**Template scaffold:** Prefer adding `users/_template/self-work.md` in companion-self when promoting a default starter for new instances.
