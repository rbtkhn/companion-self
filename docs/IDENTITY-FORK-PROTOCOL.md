# Identity Fork Protocol — Short Form

**Companion-Self template · Protocol summary**

*Full specification: see the reference implementation's [IDENTITY-FORK-PROTOCOL](https://github.com/rbtkhn/grace-mar/blob/main/docs/IDENTITY-FORK-PROTOCOL.md).*

---

## Sovereign Merge Rule

> **The agent may stage. It may not merge.**

- **Stage** — Propose candidates for addition to the Record (e.g. PENDING-REVIEW).
- **Merge** — Commit changes to SELF, EVIDENCE, or canonical profile.

Only the companion (or an explicitly delegated human) may merge. Agents and systems may stage. The gate is architectural.

---

## Stages

1. **Detect** — Identify profile-relevant signals (knowledge, curiosity, personality).
2. **Stage** — Write candidates to PENDING-REVIEW (or equivalent).
3. **Review** — Companion approves, rejects, or modifies.
4. **Merge** — Approved changes are integrated into SELF, EVIDENCE, and related files.

---

## Evidence Linking

Every claim in the Record must reference evidence (e.g. activity id, provenance). No claim without traceability to an artifact or approved source.

---

## Identity Schema (Modules)

| Module | Contains | Purpose |
|--------|----------|---------|
| **SELF** | Identity, personality, preferences, values, narrative, post-seed growth (IX-A, IX-B, IX-C) | Who they ARE |
| **SKILLS** | READ, WRITE, WORK (self-skill-read, self-skill-write, self-skill-work) | What they CAN DO; education is structured around these three. Template uses **modular files**: `self-skill-read.md`, `self-skill-write.md`, `self-skill-work.md`. Schema tags in APIs/export remain READ, WRITE, WORK. |
| **EVIDENCE** | Activity log, writing log, creation log | Raw artifacts; immutable once captured |
| **LIBRARY** (optional) | Curated lookup sources (books, reference works, videos) | Bounded lookup extension; query-first for answers; does not auto-merge into Record |

Post-seed growth: **IX-A** (self-knowledge), **IX-B** (self-curiosity), **IX-C** (self-personality). Self-skill-read (READ) activity is **filtered and distilled** into these three; the pipeline suggests merges, the companion gates.

---

## Knowledge Boundary

The Record may contain only what the companion has explicitly provided. No LLM inference into the Record; calibrated abstention when outside documented knowledge.

---

## Process Over Prompt

Quality of outputs depends on **process** (staging, evidence linking, review, merge)—not on model strength or prompt tuning. The protocol and pipeline are the lever; prompts support the process.

---

*Companion-Self template · Protocol summary*
