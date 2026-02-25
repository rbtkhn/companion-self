# What Is a Companion Self?

**Companion-self template · Concept**

---

## 1. Core Idea

A **companion self** is a documented, queryable identity that grows from a snapshot of a person and accompanies them over time. It has two parts:

- **Record** — The documented self: who they are (knowledge, curiosity, personality) and what they can do (skills), with evidence linking every claim to artifacts or approved sources.
- **Voice** — The queryable interface that speaks the Record when the companion asks. It never speaks unbidden.

**Companion self = Mind + Record + Voice.** The human (Mind) is sovereign. The Record holds the documented self. The Voice renders it when queried.

---

## 2. Cognitive Fork, Not Twin

| Term | Meaning |
|------|---------|
| **Cognitive fork** | Versioned branch from a snapshot. Diverges by design. Has its own history. |
| **Cognitive twin** | Parallel copy that stays in sync with the original. |

We use **cognitive fork** only. The fork and the real person grow independently; divergence is intentional.

---

## 3. Record vs. Voice

- **Record** — The documented self (e.g. SELF.md, SKILLS.md, EVIDENCE.md). It is its own entity: it started from a snapshot but has its own trajectory. It does not "mimic" or "replicate" the person.
- **Voice** — Renders the Record in conversation. When the companion queries, the system generates responses constrained by the Record. That rendering is the Voice.

The Record records; the Voice speaks the Record. The Record does not command; the Voice does not speak unbidden.

---

## 4. Knowledge Boundary

The Record contains only what the companion has explicitly provided and approved.

- No LLM inference — facts from model training must not enter the Record.
- Evidence linkage — every claim traces to an artifact or approved source.
- When queried outside documented knowledge, the system may say "I don't know" and offer to look up.

This boundary is both an architectural invariant and a regulatory advantage (e.g. COPPA, GDPR).

---

## 5. Key Invariants

1. **Divergence by design** — Fork and real person may drift apart; that is correct.
2. **Merge, not add** — Content enters the Record by merging through a gate; the companion approves every merge.
3. **Agent may stage; it may not merge** — Only the companion (or an explicitly delegated human) may merge into the Record.
4. **Identity beyond productivity** — The Record records who someone is, not what they produce.
5. **Augmentation, not automation** — The system augments human judgment; it does not replace it. Human-in-the-loop is mandatory.

---

## 6. Where Things Live (Template View)

| Component | In an instance |
|-----------|----------------|
| **Record** | `users/<id>/SELF.md`, SKILLS.md, EVIDENCE.md |
| **Voice** | Bot or other interface (lives in the instance repo; not in this template) |
| **Staging** | PENDING-REVIEW.md — candidates before merge |
| **Ephemeral context** | MEMORY.md (optional; not part of the Record) |

This template defines concept, protocol, and seed phase. Bot code and Record data live in instance repos only.

---

*Companion-self template · No instance-specific content*
