# Identity Fork Protocol — Short Form

**Companion-Self template · Protocol summary**

*Full specification (IFP v1.0): see the reference implementation’s [identity-fork-protocol.md](https://github.com/rbtkhn/grace-mar/blob/main/docs/identity-fork-protocol.md).*

**Routing vs sensemaking vs accountability:** [governance-unbundling.md](governance-unbundling.md).

---

## Sovereign Merge Rule

> **The agent may stage. It may not merge.**

- **Stage** — Propose candidates for addition to the Record (e.g. recursion-gate).
- **Merge** — Commit changes to SELF, self-evidence, or canonical profile.

Only the companion (or an explicitly delegated human) may merge. Agents and systems may stage. The gate is architectural.

---

## Stages

1. **Detect** — Identify profile-relevant signals (knowledge, curiosity, personality).
2. **Stage** — Write candidates to recursion-gate (or equivalent).
3. **Review** — Companion approves, rejects, or modifies.
4. **Merge** — Approved changes are integrated into SELF, self-evidence, and related files.

---

## Process the gate (self-evidence pipeline)

**Command (for system clarity):** *Process the gate* or *Process the self-evidence pipeline*.

**Meaning:** The companion (or delegated human) performs the gate step: open the review queue, then for **each** pending candidate choose **Approve** or **Reject**. Each Approve runs merge for that candidate (write to self-evidence and dimension/skill files); each Reject removes the candidate from the gate. No batch or automatic merge—only the human can merge, one candidate at a time per action.

Use this phrase in operator instructions, agent rules, and docs when referring to "run the gate" or "do the review step."

---

## Evidence Linking

Every claim in the Record must reference evidence (e.g. activity id, provenance). No claim without traceability to an artifact or approved source.

---

## Identity Schema (Modules)

| Module | Contains | Purpose |
|--------|----------|---------|
| **SELF** | Identity, baseline (I–VIII); optional pointer/summary for growth files. Post-seed growth **source of truth** is the split files below. | Who they ARE |
| **self-knowledge** (IX-A) | What they've learned; topics, facts, understanding. | `self-knowledge.md` |
| **self-identity** | Durable identity commitments, boundaries, and role-level self-definition. | `self-identity.md` |
| **self-curiosity** (IX-B) | What they're curious about; interests, questions. **Source of truth** for IX-B. | `self-curiosity.md` |
| **self-personality** (IX-C) | Voice, preferences, values (observed growth). **Source of truth** for IX-C. | `self-personality.md` |
| **SKILLS** | THINK, WRITE, WORK (self-skill-think, self-skill-write, self-skill-work) | What they CAN DO; education is structured around these three. **WORK utilizes self-personality (IX-C)** for what to build, how they work, voice in outputs, resilience/difficulty, ritual ("we did X"), and edge phrasing. Template: `self-skill-think.md`, `self-skill-write.md`, `self-skill-work.md`. Schema tags in APIs/export: THINK, WRITE, WORK. |
| **self-evidence** | Activity log, writing log, creation log | Raw artifacts; immutable once captured |
| **self-library** (optional) | Curated lookup sources (books, reference works, videos) | Bounded lookup extension; query-first for answers; does not auto-merge into Record |

Post-seed growth: `self-knowledge`, `self-identity`, `self-curiosity`, `self-personality`. The **source of truth** for this content is the split growth files; self.md holds baseline only (or an optional summary). Activity is filtered and distilled into these files through the gate; the companion approves merges.

---

## Knowledge Boundary

The Record may contain only what the companion has explicitly provided. No LLM inference into the Record; calibrated abstention when outside documented knowledge.

---

## Process Over Prompt

Quality of outputs depends on **process** (staging, evidence linking, review, merge)—not on model strength or prompt tuning. The protocol and pipeline are the lever; prompts support the process.

---

*Companion-Self template · Protocol summary*
