# Instance Doctrine — [instance-name]

> Instance-specific operating rules for this companion fork. This file is **Layer 2** in the [four-layer instruction architecture](../../docs/layer-architecture.md). Core doctrine lives in the system's AGENTS.md (or equivalent); this file may narrow but never contradict it.

---

## Operating Modes

<!-- Define which modes this instance supports and any instance-specific mode behavior. -->

| Mode | Purpose | Agent behavior |
|------|---------|----------------|
| **Session** | Interactive conversation with companion | Respond as Voice; propose activities. Do not merge. |
| **Pipeline** | Process staged candidates | Detect signals, stage to RECURSION-GATE, merge only on approval via script. |
| **Query** | Browse or answer questions about the Record | Read-only. Report what is documented. |
| **Maintenance** | End-of-day consolidation | Normalize memory, check integrity, refresh contradiction digest. |

When in doubt, default to Session (conversational, no merges).

---

## Success Metrics

<!-- Define instance-specific success metrics. Common metrics: -->

| Metric | Target | How to verify |
|--------|--------|---------------|
| **Knowledge boundary** | No undocumented references | Bot never cites facts not in profile |
| **Pipeline health** | Candidates processed, not stale | RECURSION-GATE queue doesn't grow unbounded |
| **Profile growth** | IX entries increase over time | IX-A, IX-B, IX-C counts in profile |
| **Calibrated abstention** | "I don't know" when outside knowledge | Bot says "do you want me to look it up?" appropriately |

---

## File Update Protocol

<!-- Instance-specific merge paths, script commands, and file update targets. -->

When pipeline candidates are approved, merge via script only. Do not edit profile, evidence, or prompt files directly.

| File | What to update |
|------|---------------|
| `users/[id]/self.md` | New entries merged into IX-A, IX-B, IX-C |
| `users/[id]/self-evidence.md` | New activity log entry |
| `users/[id]/recursion-gate.md` | Move candidates to Processed |
| `users/[id]/session-log.md` | New session record |

---

## Prompt Architecture

<!-- Instance-specific prompt configuration. -->

| Prompt | Purpose |
|--------|---------|
| `SYSTEM_PROMPT` | Emulation persona — defines who the self is |
| `ANALYST_PROMPT` | Signal detection — analyzes exchanges for profile-relevant signals |
| `LOOKUP_PROMPT` | Knowledge lookup — rephrases search queries for age-appropriate results |
| `REPHRASE_PROMPT` | Answer rephrasing — converts search results into the self's voice |

---

## Repository Structure

<!-- Instance-specific file tree. -->

```
users/[id]/
├── instance-doctrine.md  # This file (Layer 2)
├── self.md               # Identity + three-dimension mind
├── self-evidence.md      # EVIDENCE — activity log
├── self-memory.md        # Continuity context (not part of Record)
├── session-log.md        # Interaction history
├── recursion-gate.md     # Pipeline staging
└── artifacts/            # Raw files
```
