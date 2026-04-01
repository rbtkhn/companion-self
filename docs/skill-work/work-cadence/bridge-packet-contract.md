# Bridge packet contract

The bridge transfer prompt is the structured markdown block that `bridge` generates at session close. It is the primary artifact for carrying context across the session boundary where agent memory goes to zero.

This document defines the canonical sections, what each must contain, and the rules for extending the format.

---

## Canonical sections

Every bridge packet must include these sections in this order. Omit a section only if it has genuinely nothing to report (e.g. gate is empty, no territories had motion). Never drop a section because the agent ran out of context or forgot.

| Section | What to include | What to omit |
|---------|----------------|-------------|
| **Arc** | 2-4 sentence narrative of what the session accomplished, what shifted, current posture. Synthesize — do not list. | Bullet-point summaries, file-by-file changelogs. |
| **Carry-forward from last dream** | Condensed dream handoff: day status, strongest signal, carry-forward action, integrity/governance flags. If no dream ran, say so. | Raw JSON dump. Speculative interpretation of dream output. |
| **Gate snapshot** | Pending candidate count. Top 1-3 candidate ids with one-line summaries. If none pending, "Gate clear." | Full candidate YAML. Approval recommendations (bridge does not process the gate). |
| **Active territories** | One line per territory with recent motion. Name the territory and what moved. | Territories with no recent activity. Full history excerpts. |
| **Priority lanes for next session** | 1-3 ranked priorities derived from gate state, territory momentum, and arc. | More than 3 unless genuinely warranted. Priorities not grounded in on-disk evidence. |
| **Watch this** | One sentence: the single most important thing the next session should be alert to. Agent-synthesized from arc + gate + territories. | Multiple warnings (pick the one that matters most). Vague hedging. |
| **Commits sealed in this bridge** | List the commit(s) made during bridge Step 2, with messages. If worktree was already clean, say so. | Full diffs. File-level detail beyond the commit message. |
| **Recent commits** | Last 5-10 commits from `git log --oneline`, verbatim. | Older history unless specifically relevant. |
| **Instructions for next session** | "Paste this entire block as the first message in a fresh Cursor session, then say `coffee` to reorient." | Instance-specific instructions belong in instance extensions, not the template contract. |

---

## Extension rules

Instances may extend the bridge packet:

- **Add sections** after Priority lanes and before Commits sealed (e.g. instance-specific territory summaries, risk flags, companion-facing notes).
- **Add fields** within existing sections when grounded in on-disk state (e.g. grace-mar adds contradiction counts inside Carry-forward).
- **Do not drop** any canonical section. The contract guarantees that every bridge packet is parseable by the same reader regardless of instance.
- **Do not reorder** the canonical sections. Extensions slot into the gap between Priority lanes / Watch this and Commits sealed.

---

## Design rationale: I-PASS mapping

The section list is informed by the I-PASS clinical handoff protocol (Illness severity, Patient summary, Action list, Situation awareness, Synthesis). Bridge is not medical, but the structural discipline of I-PASS — particularly its insistence on an explicit synthesis step — strengthens the handoff.

| I-PASS element | Bridge equivalent | Notes |
|---------------|-------------------|-------|
| Illness severity | **Arc** | Narrative posture of the session — how things stand, not just what happened. |
| Patient summary | **Carry-forward** + **Gate snapshot** | State carried from prior rituals plus the pipeline queue. |
| Action list | **Priority lanes** + **Commits sealed** | What to do next and what was just done. |
| Situation awareness | **Active territories** | Where motion is happening across the work surface. |
| Synthesis | **Watch this** | The one thing the next session must not miss. Added explicitly to close the I-PASS gap. |

---

## Relation to other cadence surfaces

- The bridge packet is **ephemeral** — it exists in the chat, not on disk, unless the operator chooses to save it.
- It is **not** Record truth, not self-memory, and not a pipeline artifact.
- It complements `last-dream.json` / `night-handoff.json` (which carries dream state) and `self-memory.md` (which carries long-horizon continuity). Bridge synthesizes across all of these for the specific purpose of session restart.
- The canonical skill file is `.cursor/skills/bridge/SKILL.md`. This contract documents the output format; the skill file documents the full ritual (read, commit, generate, done).
