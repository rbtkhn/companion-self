# Runtime vs durable Record

**Purpose:** Map **canonical, governed** surfaces versus **temporary, derived, or operator-only** outputs.

---

## Durable Record (typical instance)

Changes flow through the **gated pipeline** and companion-approved merge (see [identity-fork-protocol.md](identity-fork-protocol.md), instance `AGENTS.md`).

| Surface | Typical anchors | Holds |
|---------|-----------------|-------|
| **SELF** | `users/<id>/self.md` | Identity, knowledge dimensions |
| **SELF-LIBRARY** | `users/<id>/self-library.md` | Governed reference |
| **SKILLS** | `users/<id>/self-skills.md` | Capability index |
| **EVIDENCE** | `users/<id>/self-evidence.md` or `self-archive.md` | Activity log, evidence |

**Approval Inbox:** `users/<id>/recursion-gate.md` — staging until processed.

---

## Work territories (`docs/skill-work/work-*`)

WORK lanes are for planning and execution support. They are **not** Record truth.

---

## Forecasting boundary

Forecast outputs belong to WORK unless a human separately stages a downstream conclusion.
A forecast artifact is not a Record fact.
See [docs/skill-work/work-forecast/forecast-protocol.md](skill-work/work-forecast/forecast-protocol.md).

## Forecast receipts and observability

Forecast artifacts, receipts, and observability reports belong to WORK.
They are rebuildable legibility surfaces, not Record truth.

## Forecast references (instance work-strategy)

In instance repos, forecast artifacts may be cited in WORK strategy surfaces.
Citation does not make the forecast a Record fact.
See [Grace-Mar work-strategy README](https://github.com/rbtkhn/grace-mar/blob/main/docs/skill-work/work-strategy/README.md) for a full example tree.
