# What Is a Companion Self?

**Companion-Self template · Concept**

---

## Long-term objectives (permanent system rules)

Companion-Self has **three** long-term objectives of equal importance: (1) **Democratize Alpha-style education** — comparable outcomes at a fraction of the cost, without a school or in-room guides, via Record as spine. (2) **Companion sovereignty** — all modification of skill and self containers is human-approval gated; agent may stage, may not merge. (3) **Knowledge boundary** — the Record contains only what the companion has provided and approved; no LLM inference in. These are permanent system rules to prevent intention drift and optimize alignment. Full statement and use: [LONG-TERM-OBJECTIVE](LONG-TERM-OBJECTIVE.md).

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

## 4. Education structure

Companion-Self education is **structured** around three skill containers:

| Structure | Schema tag | Meaning |
|-----------|------------|---------|
| **self-skill-read** | READ | Intake and comprehension: what the companion has consumed and understood (reading, media, lessons). Evidence and edge drive what to read/watch next. |
| **self-skill-write** | WRITE | Expression and voice: what the companion produces (journal, stories, explanations). Evidence of WRITE is evidence of understanding and voice. |
| **self-skill-build** | BUILD | Making and doing: what the companion plans, builds, and ships (projects, creations). Evidence links to SKILLS.BUILD and life skills. |

In schema, APIs, and export we use the tags **READ**, **WRITE**, **BUILD**; the canonical names for the **education structure** are **self-skill-read**, **self-skill-write**, **self-skill-build**. All screen-based learning and evidence capture are organized under these three.

**Self-skill-read → self-knowledge, self-curiosity, self-personality.** Activity in **self-skill-read** (READ) is **filtered and distilled** into three dimensions of the Record (SELF):

| Distillation target | Schema | Meaning |
|--------------------|--------|---------|
| **self-knowledge** | IX-A | What the companion has learned and knows (topics, facts, understanding). |
| **self-curiosity** | IX-B | What they are curious about, interests, questions. |
| **self-personality** | IX-C | Voice, preferences, values, narrative—how they see themselves and express. |

The pipeline stages READ activity and suggests merges into IX-A, IX-B, or IX-C; the companion gates what actually enters. So READ feeds **who they are** (SELF) as well as **what they can do** (SKILLS.READ, evidence).

---

## 5. Knowledge Boundary

The Record contains only what the companion has explicitly provided and approved.

- No LLM inference — facts from model training must not enter the Record.
- Evidence linkage — every claim traces to an artifact or approved source.
- When queried outside documented knowledge, the system may say "I don't know" and offer to look up.

This boundary is both an architectural invariant and a regulatory advantage (e.g. COPPA, GDPR).

---

## 6. Key Invariants

1. **Divergence by design** — Fork and real person may drift apart; that is correct.
2. **Merge, not add** — Content enters the Record by merging through a gate; the companion approves every merge.
3. **Agent may stage; it may not merge** — Only the companion (or an explicitly delegated human) may merge into the Record.
4. **Identity beyond productivity** — The Record records who someone is, not what they produce.
5. **Augmentation, not automation** — The system augments human judgment; it does not replace it. Human-in-the-loop is mandatory.
6. **Two-hour screen-time target** — All screen-based learning is designed to occur within **2 hours per day**, aligned with models (e.g. Alpha School) that squeeze full mandatory education into a 2-hour block. This is both a design constraint and an **equivalent metric** for comparison (2 hours = full academic coverage). See [TWO-HOUR-SCREENTIME-TARGET](TWO-HOUR-SCREENTIME-TARGET.md).
7. **No human guide assumed** — Companion-Self must achieve its recursive self-learning objectives **without assuming the help of a human guide**. Guide-like support (motivation, “did you read the explanation?”, learning-how-to-learn) is designed into the **system** (Voice, pipeline prompts, session copy, edge suggestions) so the companion can succeed with zero or minimal adult involvement. An operator/parent may augment but is not required for the design to work.

---

## 7. Where Things Live (Template View)

| Component | In an instance |
|-----------|----------------|
| **Record** | `users/<id>/SELF.md`, SKILLS.md, EVIDENCE.md |
| **Voice** | Bot or other interface (lives in the instance repo; not in this template) |
| **Staging** | PENDING-REVIEW.md — candidates before merge |
| **Ephemeral context** | MEMORY.md (optional; not part of the Record) |

This template defines concept, protocol, and seed phase. Bot code and Record data live in instance repos only.

---

## 8. Recursive self-learning

The Record can **improve itself over time**: each pipeline cycle refines the Record, and the updated Record shapes the next cycle (what gets detected, what the Voice says, what activities might be proposed at the edge). For objectives that guide this—inspired by learning science and AI-powered education models—see [RECURSIVE-SELF-LEARNING-OBJECTIVES](RECURSIVE-SELF-LEARNING-OBJECTIVES.md).

---

*Companion-Self template · No instance-specific content*
