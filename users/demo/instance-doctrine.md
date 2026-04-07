# Instance Doctrine — demo

> Instance-specific operating rules for the demo companion fork. This file is **Layer 2** in the [four-layer instruction architecture](../../docs/layer-architecture.md). Core doctrine lives in the system's AGENTS.md (or equivalent); this file may narrow but never contradict it.

---

## Operating Modes

| Mode | Purpose | Agent behavior |
|------|---------|----------------|
| **Session** | Interactive conversation with companion | Respond as Voice; propose activities. Do not merge. |
| **Pipeline** | Process staged candidates | Detect signals, stage to RECURSION-GATE, merge only on approval via script. |
| **Query** | Browse or answer questions about the Record | Read-only. Report what is documented. |
| **Maintenance** | End-of-day consolidation | Normalize memory, check integrity, refresh contradiction digest. |

When in doubt, default to Session (conversational, no merges).

---

## Success Metrics

| Metric | Target | How to verify |
|--------|--------|---------------|
| **Knowledge boundary** | No undocumented references | Bot never cites facts not in profile |
| **Pipeline health** | Candidates processed, not stale | RECURSION-GATE queue doesn't grow unbounded |
| **Profile growth** | IX entries increase over time | IX-A, IX-B, IX-C counts in profile |
| **Calibrated abstention** | "I don't know" when outside knowledge | Bot says "do you want me to look it up?" appropriately |

---

## File Update Protocol

When pipeline candidates are approved, merge via script only. Do not edit profile, evidence, or prompt files directly.

| File | What to update |
|------|---------------|
| `users/demo/self.md` | New entries merged into IX-A, IX-B, IX-C |
| `users/demo/self-evidence.md` | New activity log entry |
| `users/demo/recursion-gate.json` | Move candidates to Processed |

---

## Prompt Architecture

| Prompt | Purpose |
|--------|---------|
| `SYSTEM_PROMPT` | Emulation persona — defines who the self is |
| `ANALYST_PROMPT` | Signal detection — analyzes exchanges for profile-relevant signals |

---

## Repository Structure

```
users/demo/
├── instance-doctrine.md  # This file (Layer 2)
├── self.md               # Identity + three-dimension mind
├── self-evidence.md      # EVIDENCE — activity log
├── seed-registry.jsonl   # Seed phase claims
├── recursion-gate.json   # Pipeline staging
└── review-queue/         # Diff queue
```
