# Imports and capture (companion-self)

**Purpose:** Same **safety story** as instances: ingestion feeds **evidence and prepared context** first; **governed Record** updates wait for the human gate.

> Imports do **not** auto-write durable governed state. **Approval Inbox** (`recursion-gate`) remains the merge boundary for routine gate candidates ([identity-fork-protocol.md](identity-fork-protocol.md)).

---

## Canonical pattern

See **[ingestion-and-sources.md](ingestion-and-sources.md)** — many sources → staging → **human gate** → one Record.

Layered model: [state-model.md](state-model.md), [evidence-layer.md](evidence-layer.md), [prepared-context-layer.md](prepared-context-layer.md), [governed-state-layer.md](governed-state-layer.md).

---

## Instance reference

**Grace-Mar** documents the same boundary with instance paths: **[imports-and-capture.md](https://github.com/rbtkhn/grace-mar/blob/main/docs/imports-and-capture.md)** (evidence, prepared context, `recursion-gate.md`).

---

## See also

- [gate-vs-change-review.md](gate-vs-change-review.md) — when escalation adds process
- [start-here-ob1-users.md](start-here-ob1-users.md) — OB1-oriented map
