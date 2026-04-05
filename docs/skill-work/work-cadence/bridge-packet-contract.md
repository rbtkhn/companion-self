# Bridge packet contract

The bridge transfer prompt is the structured markdown block that `bridge` generates at session close. It is the primary artifact for carrying context across the session boundary where agent memory goes to zero.

This document defines the canonical sections, what each must contain, and the rules for extending the format.

---

## Canonical sections

Every bridge packet must include these sections in **this order**. Omit a section only if it has genuinely nothing to report (e.g. gate is empty, no territories had motion). Never drop a section because the agent ran out of context or forgot.

| Section | What to include | What to omit |
|---------|----------------|-------------|
| **Arc** | 2-4 sentence narrative of what the session accomplished, what shifted, current posture. Synthesize — do not list. | Bullet-point summaries, file-by-file changelogs. |
| **Carry-forward from last dream** | Condensed dream handoff: day status, strongest signal, carry-forward action, integrity/governance flags. If no dream ran, say so. | Raw JSON dump. Speculative interpretation of dream output. |
| **Gate snapshot** | Pending candidate count. Top 1-3 candidate ids with one-line summaries. If none pending, "Gate clear." | Full candidate YAML. Approval recommendations (bridge does not process the gate). |
| **Active territories** | One line per territory with recent motion. Name the territory and what moved. | Territories with no recent activity. Full history excerpts. |
| **Priority lanes for next session** | 1-3 ranked priorities. Each line: **lane or theme — one short reason** (why this rank), grounded in gate, territories, arc. | More than 3 unless genuinely warranted. Flat labels without reasons. |
| **Watch this** | Start with **risk kind** then the warning: `**Risk kind:** continuity \| git \| governance \| focus \| context` on one line, then one sentence (or `**context** — sentence` on one line). | Multiple unrelated warnings; vague hedging. |
| **Since last bridge** | Max 3-4 bullets: what changed since `last-bridge-state.json` (commits, gate count/fingerprint, active territories set, worktree risk class). If no prior state file, say *First bridge state — no prior delta.* | Long lists; speculation beyond on-disk diffs. |
| **Bridge transfer quality** | **Confidence:** high \| medium \| low. **Signals:** 2-4 short phrases (e.g. clean push, dream handoff present, gate readable, territories detected). **Gaps:** one line (what is missing or weak). **Seal:** post-push `git status -sb` summary per repo in scope + `HEAD` short SHAs (clean / ahead / diverged). | Duplicating the full Recent commits section. |
| **Next session posture** | One line: **Posture:** reorient \| execute \| inspect \| resolve \| write — plus three to six words of justification tied to arc + gate + worktree risk. | A second priority list. |
| **Not transferred on purpose** | Optional. Max **2** bullets: what the packet deliberately did not carry (e.g. noisy branches, speculative notes). Omit if nothing honest to say. | Excuses; more than two bullets. |
| **Commits sealed in this bridge** | Per repo: which commits (messages). One **composite line**: `Residue commit: … / Substantive commit: …` (or `none` for each). If worktree was already clean, say so. | Full diffs. File-level detail beyond the commit message. |
| **Recent commits** | Last 5-10 commits from `git log --oneline`, verbatim. | Older history unless specifically relevant. |
| **Instructions for next session** | Paste as first message; assistant runs **coffee** Step 1. **Harvest:** if the operator needs a **parallel warm-session import**, run the **harvest** skill separately — do not append a second packet to this block (avoids confusion with the required `coffee` tail). | Instance-specific automation in the template contract. |

**Coffee tail (required):** After Instructions, the copyable block must end with a **final line that is exactly `coffee`** (lowercase, alone on its line, not inside a code fence) when the instance uses the grace-mar bridge + coffee chain.

---

## Extension rules

Instances may extend the bridge packet:

- **Template extensions** listed above (**Since last bridge** through **Not transferred**) sit **after Watch this** and **before Commits sealed**. Do not insert other sections between those template extensions and **Commits sealed**.
- **Additional instance sections** may be added in the same gap (after **Not transferred**, before **Commits sealed**) when needed.
- **Add fields** within existing sections when grounded in on-disk state (e.g. contradiction counts inside Carry-forward).
- **Do not drop** any canonical section. The contract guarantees that every bridge packet is parseable by the same reader regardless of instance.
- **Do not reorder** the core narrative block: Arc through Watch this stays fixed; then template extensions; then Commits sealed through Instructions.

---

## Operational state: `last-bridge-state.json`

For **Since last bridge**, instances may persist a small operational snapshot (not Record truth), e.g. `users/<id>/daily-handoff/last-bridge-state.json`, written **after** a successful push and cadence log. Shape is instance-defined; typical fields include HEAD short SHAs, gate pending count and fingerprint, sorted active territory ids, and worktree risk class (`safe` / `inspect` / `conflict-prone`) per repo. See instance docs and `scripts/bridge_last_state.py` (grace-mar).

---

## Design rationale: I-PASS mapping

The section list is informed by the I-PASS clinical handoff protocol (Illness severity, Patient summary, Action list, Situation awareness, Synthesis). Bridge is not medical, but the structural discipline of I-PASS — particularly its insistence on an explicit synthesis step — strengthens the handoff.

| I-PASS element | Bridge equivalent | Notes |
|---------------|-------------------|-------|
| Illness severity | **Arc** | Narrative posture of the session — how things stand, not just what happened. |
| Patient summary | **Carry-forward** + **Gate snapshot** | State carried from prior rituals plus the pipeline queue. |
| Action list | **Priority lanes** + **Commits sealed** | What to do next and what was just done. |
| Situation awareness | **Active territories** + **Since last bridge** | Where motion is happening; what changed across sessions. |
| Synthesis | **Watch this** + **Bridge transfer quality** + **Next session posture** | Risk, trust in the packet, and how to open the next session. |

---

## Relation to other cadence surfaces

- The bridge packet is **ephemeral** — it exists in the chat, not on disk, unless the operator chooses to save it.
- It is **not** Record truth, not self-memory, and not a pipeline artifact.
- It complements `last-dream.json` / `night-handoff.json` (which carries dream state) and `self-memory.md` (which carries long-horizon continuity). Bridge synthesizes across all of these for the specific purpose of session restart.
- The canonical skill file is `.cursor/skills/bridge/SKILL.md` (instance path). This contract documents the output format; the skill file documents the full ritual (read, commit, generate, done).
