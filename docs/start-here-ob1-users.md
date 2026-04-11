# Coming from OB1? Start here (companion-self template)

Plain-language bridge for people who know **Open Brain (OB1)**-style systems. **This repository is the template** — no live `users/<id>/` Record ships here; use **[Grace-Mar](https://github.com/rbtkhn/grace-mar)** as the fully lived reference instance. Precise protocol: [identity-fork-protocol.md](identity-fork-protocol.md), [concept.md](concept.md).

> A companion-self **instance** is not just a memory layer; it is a **governed companion record**. If you know OB1, the easiest way in is **Library, Skills, Evidence, Workflows, Dashboard, and Approval Inbox** — with durable writes still **gated**.

---

## Translation table

| If you think in… | In companion-self / instances |
|------------------|--------------------------------|
| **Library** | **SELF-LIBRARY** — governed reference (`self-library.md` in an instance) |
| **Skills** (executable packs) | Two layers: **SKILLS** (Record capability) vs **portable skills** (operator assets — many instances add `skills-portable/`; see [Grace-Mar skills-explained](https://github.com/rbtkhn/grace-mar/blob/main/docs/skills-explained.md)) |
| **Evidence / activity log** | **EVIDENCE** — e.g. `self-archive.md` / `self-evidence.md` in an instance |
| **Pending approvals** | **Approval Inbox** — user-facing name for pending candidates in **`users/<id>/recursion-gate.md`** (canonical: **recursion-gate**). Spec: [approval-inbox-spec.md](approval-inbox-spec.md). |
| **Workflows / recipes** | `docs/skill-work/**`, scripts, instance bridges — [workflow-catalog.md](workflow-catalog.md) |
| **Imports / capture** | [imports-and-capture.md](imports-and-capture.md) (instance narrative); pattern: [ingestion-and-sources.md](ingestion-and-sources.md) |
| **Dashboard** | [observability.md](observability.md), demo observability under `users/demo/`; local app: [readme-app.md](../readme-app.md) |

---

## What will feel familiar

- **Inspectability** — [observability.md](observability.md), legible receipts ([legible-surfaces.md](legible-surfaces.md)).
- **A queue before durable memory** — [approval-inbox-spec.md](approval-inbox-spec.md); Sovereign Merge Rule in [identity-fork-protocol.md](identity-fork-protocol.md).
- **Imports** — [ingestion-and-sources.md](ingestion-and-sources.md): many sources → staging → **human gate** → one Record.

---

## What is different

- **Template vs instance** — This repo holds **constitution and scaffolds** (`users/_template/`); a real fork lives in an **instance repo** after seed phase ([instance-patterns.md](instance-patterns.md)).
- **Four Record surfaces** — SELF, SELF-LIBRARY, SKILLS, EVIDENCE — see [concept.md](concept.md) and [boundary-self-knowledge-self-library.md](https://github.com/rbtkhn/grace-mar/blob/main/docs/boundary-self-knowledge-self-library.md) (grace-mar copy is the detailed boundary doc; template links portable doctrine).
- **No silent merge** — [gate-vs-change-review.md](gate-vs-change-review.md), [state-model.md](state-model.md).

---

## Where to start first

1. Read [README.md](../README.md) — North star and template vs instance.
2. Open [seed-phase.md](seed-phase.md) if you are forming a new companion.
3. Skim [workflow-catalog.md](workflow-catalog.md) for link-shaped orientation.
4. Reference implementation: **[Grace-Mar](https://github.com/rbtkhn/grace-mar)** — [start-here](https://github.com/rbtkhn/grace-mar/blob/main/docs/start-here.md), [workflow catalog](https://github.com/rbtkhn/grace-mar/blob/main/docs/workflow-catalog.md).

---

## See also

- [imports-and-capture.md](imports-and-capture.md)
- [skills-explained.md](skills-explained.md)
- [glossary.md](glossary.md) — template glossary (short)
