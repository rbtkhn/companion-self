# Identity Fork Protocol — Short Form

**Companion-self template · Protocol summary**

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
| **SKILLS** | READ, WRITE, BUILD capability containers | What they CAN DO |
| **EVIDENCE** | Activity log, writing log, creation log | Raw artifacts; immutable once captured |

Post-seed growth: **IX-A** (knowledge), **IX-B** (curiosity), **IX-C** (personality).

---

## Knowledge Boundary

The Record may contain only what the companion has explicitly provided. No LLM inference into the Record; calibrated abstention when outside documented knowledge.

---

*Companion-self template · Protocol summary*
