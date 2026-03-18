# Approval Inbox Spec

**Companion-Self template ·** implementation-ready product spec

**Purpose:** define a browser-first **review surface** for the recursion-gate queue that reduces operator fatigue without weakening the Sovereign Merge Rule.

**Primary sources:** [identity-fork-protocol.md](identity-fork-protocol.md), [schema-record-api.md](schema-record-api.md), [instance-patterns.md](instance-patterns.md), [CONTRADICTION-ENGINE-SPEC.md](CONTRADICTION-ENGINE-SPEC.md)

**Reference implementation:** Grace-Mar — `docs/approval-inbox-spec.md`, `gate-review-app.py`, `recursion-gate.md`, `pipeline-events.jsonl`.

---

## 1. Goal

- Show pending candidates in a structured inbox  
- Approve, reject, batch-review, or defer  
- Preserve human gate: agent stages; only companion or delegated human merges  
- Reuse canonical queue shape and audit logging  

This is a **review surface**, not a new memory system.

---

## 2. Constraints (MUST PRESERVE)

- Agent may stage; may not merge  
- **One canonical queue** per user: `recursion-gate.md` (markdown blocks) or `recursion-gate.json` per instance choice  
- Candidate status remains canonical (`pending` / `approved` / `rejected` or equivalent)  
- Quick merge / low-risk automation only where instance policy explicitly allows (see reference impl `is_low_risk_candidate`)  
- Review actions audit-visible  

The inbox may add **derived UI fields** and **helper endpoints**; it must not create a second source of truth.

**Contradiction workflow:** Identity-diff decisions follow [CONTRADICTION-ENGINE-SPEC.md](CONTRADICTION-ENGINE-SPEC.md) — escalation, before/proposed/after, resolution types, no quick-merge on active contradictions.

---

## 3. Non-Goals

- No autonomous merge  
- No silent replacement of canonical queue  
- No new agent merge authority beyond staging and policy-allowed automation  

---

## 4. Instance mapping

| Template concept | Instance implements |
|------------------|----------------------|
| Queue parse | Markdown YAML blocks or JSON array per [instance-patterns.md](instance-patterns.md) |
| Approve action | Merge into SELF / self-evidence / skill files + audit event |
| Contradiction | CONFLICT sidecars + resolution types before merge |

Full inbox UX (batch, dedup hints, saved views) may match Grace-Mar approval-inbox-spec as instances mature.

---

*Template: companion-self. March 2026.*
