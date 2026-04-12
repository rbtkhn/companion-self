# AGENTS.md — AI coding assistant guardrails (companion-self template)

This file gives **portable** rules for assistants working in the **companion-self** upstream template. Instance repositories (for example Grace-Mar) typically ship a **fuller** `AGENTS.md` layered with instance doctrine, harness rules, and operator menus—merge those when upgrading an instance from this template.

**Prime directive:** Read [docs/identity-fork-protocol.md](docs/identity-fork-protocol.md). **The agent may stage. It may not merge.**

**Conceptual baseline:** [docs/concept.md](docs/concept.md) — Record vs Voice, cognitive fork, knowledge boundary.

---

## Agent role boundaries — unbundled management functions

Assistants and automation in this repo are limited to the **routing** layer unless a human explicitly runs a merge:

- **Allowed (routing):** Detect signals; structure knowledge / curiosity / personality candidates; stage proposals in `users/[id]/recursion-gate.md` with evidence; cluster or dedupe suggestions in operator tooling.
- **Prohibited without human gate (sensemaking and accountability):** Auto-approve, auto-merge, or silently resolve conflicting candidates; substitute deep personal or ethical judgment for companion review; overwrite user intent.

When uncertain, stage with an explicit note that **human sensemaking** may be required—never merge without companion approval. Full framing: [`docs/governance-unbundling.md`](docs/governance-unbundling.md).

---

## Layer hint (template)

| Layer | Where it lives in this repo |
|-------|-----------------------------|
| Core portable doctrine | `docs/` (concept, identity fork, this file) |
| Schema / API | `docs/schema-record-api.md`, `app/schema/` |
| Instance-specific profile & gate | **Not** in the template’s live `users/` tree for real companions—copy scaffolds into an instance repo. |

For governed merge procedures in a live instance, follow that repository’s `AGENTS.md` and scripts.
