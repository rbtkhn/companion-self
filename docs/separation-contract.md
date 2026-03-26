# Separation Contract — self modules

Purpose: prevent drift between identity surfaces, skill containers, ephemeral context, and orchestration.

This contract is normative for template scripts and instance integrations.

---

## 1) Module boundaries

- `self-knowledge.md`
  - Scope: factual understanding and learned concepts.
  - Not for: session tone, live planning notes, or procedural checklists.

- `self-curiosity.md`
  - Scope: interests and open questions.
  - Not for: durable values, identity commitments, or execution logs.

- `self-personality.md`
  - Scope: observed voice, preferences, values.
  - Not for: factual claims that belong to knowledge.

- `self-skill-think.md`, `self-skill-write.md`, `self-skill-work.md`
  - Scope: capability state and edge per skill container.
  - Not for: raw session chatter; use evidence + gate linkage.

- `self-memory.md`
  - Scope: ephemeral continuity only (tone, recent topics, calibrations).
  - Not for: Record truth. Never used as merge source for identity.

- `self-work.md`
  - Scope: cross-lane daily/weekly orchestration (focus, actions, blockers).
  - Includes: current intent (operational, cycle-bound).
  - Not for: identity truth storage.

- `self-identity.md`
  - Scope: durable identity commitments and core purpose.
  - Not for: daily or cycle execution planning.

---

## 2) Allowed directional flows (read path)

- Identity -> skills (advisory shaping):
  - `self-knowledge`, `self-curiosity`, `self-personality` may shape skill planning.

- Identity + skills -> orchestration:
  - `self-work` may consume bridge outputs for execution focus.

- Library -> orchestration (lookup anchor only):
  - `self-library` may provide advisory reference anchors.

- Memory -> orchestration (ephemeral only):
  - `self-memory` may influence continuity phrasing, never identity updates.

---

## 3) Disallowed flows

- `self-memory` -> identity merge (disallowed)
- `self-work` -> direct write into identity files (disallowed)
- `self-work` replacing durable core purpose in `self-identity` (disallowed)
- `self-library` -> IX-A direct write without gate (disallowed)
- Any script auto-merge into `self.md`, `self-knowledge.md`, `self-curiosity.md`, `self-personality.md` (disallowed)

---

## 4) Write policy for helper scripts

- Default mode: read-only advisory output.
- Optional writes must be explicitly flagged and limited to operational files (e.g., daily intention notes).
- Identity updates require normal gate process.

---

## 5) Bridge contract (operational)

Current advisory bridges:

- `knowledgeBridge`
- `curiosityBridge`
- `personalityBridge`
- `libraryBridge`
- `writeBridge`
- `selfWorkBridge`

Rules:

- Bridges are planning helpers, not Record truth.
- Bridge confidence must gate action suggestions.
- Low-confidence bridges degrade to generic suggestions.

---

## 6) Verification checklist (quick)

- No script writes to identity files without gate.
- `self-memory` use is explicitly marked ephemeral.
- `self-work` remains orchestration-only in templates/docs.
- Shared parsing logic is reused across consumers where possible.

