---
name: bridge
preferred_activation: bridge
description: "Session-scale handoff ritual. Primary trigger: bridge. Commits and pushes the repo, then synthesizes current state into a structured transfer prompt for pasting into a fresh Cursor session. Run once when closing a session and carrying context forward."
---

# Bridge

**Preferred activation:** say **`bridge`**. Also responds to **`session handoff`**, **`close session`**, or **`transfer`**.

`bridge` is the session-scale handoff. It seals the current session — committing and pushing all work — then synthesizes the state into a single structured markdown block that the operator pastes into the next fresh Cursor session as the opening message.

Its purpose is **high-fidelity context transfer** across the session boundary where agent memory goes to zero. A good bridge means the next session starts with full orientation instead of spending turns reconstructing what happened.

## When to use

| Scenario | Path | Why |
|----------|------|-----|
| **End of day + closing session** | `dream` then `bridge` | Dream settles continuity; bridge seals repo and generates transfer prompt |
| **End of day, keeping session** | `dream` alone | Maintenance pass; same thread continues tomorrow |
| **Mid-day, closing session** | `bridge` alone | Seal repo, carry context forward; no maintenance needed |
| **Quick check before stepping away** | coffee closeout (instance-defined) | Lightweight status; no commit/push, no transfer prompt |

**Default:** If in doubt, `bridge`. It commits, pushes, and produces a transfer prompt. If it's also end of day, run `dream` first.

**Bridge vs coffee closeout:** Coffee closeout is lightweight — quick status, no git operations. Bridge is structural — seals the session with commits and produces the carry-forward block. Bridge is the default for any session close.

This is event-driven: the operator says `bridge` when they're ready. There is no scheduled cadence.

---

## Step 1 — Read on-disk state

When the operator says `bridge`, read the following files (do not ask — just read them):

1. **`users/<id>/self-memory.md`** — long-horizon pointers, open loops, calibrations
2. **`users/<id>/recursion-gate.md`** — pending candidates (ids, summaries, status)
3. **`users/<id>/daily-handoff/night-handoff.json`** — last dream summary (day status, signal, carry-forward action)
4. Active `docs/skill-work/` territory READMEs and history files — scan for recent motion

Also run:

5. **`git status -sb`** — uncommitted work
6. **`git log --oneline -10`** — recent commits (what moved)
7. **`users/<id>/daily-handoff/last-bridge-state.json`** (if present) — prior bridge snapshot for **Since last bridge** in Step 3

---

## Step 2 — Worktree risk preflight and commit/push

### Worktree risk preflight (read-only)

From `git status -sb` and `git diff --stat`, classify:

| Class | Meaning |
|-------|---------|
| **safe** | Clean worktree. |
| **inspect** | Light residue. |
| **conflict-prone** | Unmerged paths, conflicts, or very large/wide diff. |

Emit one line, e.g. `Worktree risk: inspect — review diff before sealing.` **Pause and ask** before committing if **conflict-prone**.

### Commit and push

Seal the session by committing and pushing. Use a **two-bucket** approach:

### Bucket 1: Runtime residue (auto-commit, no confirmation needed)

Files that are always safe to commit without review — ephemeral state, generated artifacts, audit logs. Examples: `self-memory.md`, handoff JSON files, event logs, compute ledgers.

Commit message: `chore: bridge session residue [YYYY-MM-DD]`

### Bucket 2: Substantive work (commit with summary)

Any remaining dirty files (docs, scripts, skills, territory edits, config changes) are real work. For these:

1. Run `git diff --stat` to see what changed
2. Draft a concise commit message that summarizes the substantive changes
3. Commit and report what was included

Commit message: a real summary of the work, not a generic label.

### Push

After both buckets are committed (or if the worktree was already clean), push:

```bash
git push
```

If push fails (e.g. remote has new commits), pull-rebase first, then push. If there are conflicts, stop and report — do not force-push.

**After push, run `git status -sb` to confirm clean state.**

### Cadence audit

After confirming clean state, log the bridge event:

```bash
python3 scripts/log_cadence_event.py --kind bridge -u <id> --ok --kv refs=<SHA>
```

Replace `<SHA>` with the HEAD commit just pushed (from `git rev-parse --short HEAD`).

After a successful bridge, update session delta state:

```bash
python3 scripts/bridge_last_state.py -u <id> --write
```

Optional: `python3 scripts/bridge_last_state.py -u <id> --print-delta` for **Since last bridge** bullets while composing the packet.

---

## Step 3 — Generate the transfer prompt

Now that the repo is sealed and pushed, synthesize the readings from Step 1 into a single markdown block following this format. For the canonical section list and per-section rules, see [bridge-packet-contract.md](../../../docs/skill-work/work-cadence/bridge-packet-contract.md). Include **`## Agent surface`** with **Cursor model:** from the **Cursor UI** (model picker); use `unknown` only if it is not visible.

```markdown
# Session Bridge — [YYYY-MM-DD]

## Session Arc
[Episodic — what happened, in what order:
- Started: initial intent or task
- Pivots: where direction changed and why
- Ended: current state, what's unfinished
2-4 sentences. This is narrative, not a list. Write from what you observed.]

## Session Output
[Semantic — what was figured out or produced:
- Decisions made (with warrant if available — the assumption that would invalidate them)
- Patterns identified
- Artifacts created or modified
- Open questions surfaced
Bullet list, 2-5 items. Facts and deliverables, not narrative.]

## Carry-forward from last dream
[Condensed from night-handoff.json: day status, signal, tomorrow action.
If no dream ran or file is missing, say so.]

## Gate snapshot
[Pending count. Top 1-3 candidate ids with one-line summaries from the gate file.
If none pending, say "Gate clear."]

## Active territories
[Which work lanes had recent motion based on history files. One line each.
Skip lanes with no recent activity.]

## Priority lanes for next session
1. [Lane or theme — one short reason why this rank]
2. [Lane or theme — one short reason]
3. [Third if warranted — lane or theme — reason]

## Watch this
**Risk kind:** continuity | git | governance | focus | context — [one sentence: the single most important alert.]

## Since last bridge
[Max 3-4 bullets: delta vs last-bridge-state or `bridge_last_state.py --print-delta`. If no prior file, say first bridge / no prior delta.]

## Bridge transfer quality
- **Confidence:** high | medium | low
- **Signals:** [2-4 short phrases]
- **Gaps:** [one line]
- **Seal:** [post-push `git status -sb` + short HEAD]

## Next session posture
**Posture:** reorient | execute | inspect | resolve | write — [brief justification]

## Not transferred on purpose
[Optional; max 2 bullets, or omit section.]

## Commits sealed in this bridge
[List commit(s) from Step 2. One line: `Residue commit: … / Substantive commit: …` (or none). Or "Worktree was already clean."]

## Recent commits
[Last 5-10 commits from git log, verbatim — includes the bridge commits]

## Agent surface
- **Cursor model:** [Model name from the Cursor chat UI / model picker. `unknown` only if not visible.]

## Instructions for next session
Paste this entire block as the first message in a fresh Cursor session, then say `coffee` to reorient.

**Parallel import:** For an already-running session, run **harvest** separately — do not append a second packet here.
```

Output the entire block so the operator can copy it.

---

## Step 4 — Done

Bridge is complete. The repo is pushed, the transfer prompt is generated, `bridge_last_state.py --write` ran after seal. The operator copies the prompt and closes the session.

**Optional receipt:** Save the transfer block under `docs/skill-work/work-cadence/bridge-packets/YYYY-MM-DD-session.md` if a durable copy is needed.

---

## After the new session opens — doc-only loop

**Optional operator habit:** In the **fresh** thread, confirm **coffee** (or instance morning ritual) ran on the pasted block, the **`coffee` tail** is still a lone line, and length was tolerable. If the same failure repeats **twice**, patch **this skill** or [bridge-packet-contract.md](../../../docs/skill-work/work-cadence/bridge-packet-contract.md).

---

## Guardrails

- **Commits only to the current branch.** Never switch branches, force-push, or commit to a branch the operator didn't intend.
- **No gate action.** Report gate state; do not process, approve, or defer candidates.
- **No merges into Record.** Committing files to git is not the same as merging into identity truth. The gated pipeline is untouched.
- **Signal over volume.** The transfer prompt should be concise. Aim for one screen of text, not a wall. Omit sections that have nothing to report.
- **Narrative arc matters.** The "Session Arc" section is the most valuable part — it's the thing no script can produce. Synthesize, don't just list. "Session Output" is the semantic complement — facts and deliverables.
- **Stop on conflict.** If push fails after pull-rebase due to conflicts, stop and report. Do not force-push or resolve conflicts silently.
- **Ephemeral output.** The transfer prompt exists only in the chat unless the operator saves it (optional `bridge-packets/` path).

## Relation to coffee and dream

`bridge` sits alongside coffee and dream but at a different timescale:

- **`coffee`** — many per day (orientation sips)
- **`dream`** — once per day (nightly consolidation)
- **`bridge`** — once per session (seal, push, carry forward)

**Typical close sequence:** `dream` first (if end of day), then `bridge` (seals and generates the handoff). Or just `bridge` alone if mid-day and you simply want a fresh thread.

**Next session:** Paste the bridge prompt, then say `coffee` to run the grounding stack on top of the carried context.

## Instance extensions

Instances may customize bridge for their needs:

- Add instance-specific territory names to the read list
- Extend the runtime residue file list for instance-specific generated files
- Include additional handoff artifacts (e.g. runtime bundles, fork exports)
- Commit/push multiple repos if the instance spans workspaces
- Add a persistent archive step if session history is valuable

The template provides the structural pattern; instances customize for their needs.

## Related files

- `.cursor/skills/coffee/SKILL.md` — morning cadence (run after pasting bridge)
- `.cursor/skills/dream/SKILL.md` — nightly cadence (run before bridge if end of day)
- `.cursor/skills/harvest/SKILL.md` — parallel-session import (separate paste)
- `docs/skill-work/work-cadence/README.md` — cadence territory
- `docs/skill-work/work-cadence/bridge-packet-contract.md` — section contract
- `scripts/bridge_last_state.py` — `last-bridge-state.json` + `--print-delta`
- `scripts/cadence-coffee.py` — morning runner
- `scripts/cadence-dream.py` — night runner

## Revision log

| Date | Change |
|------|--------|
| 2026-04-06 | Doc-only cold-thread loop § *After the new session opens*. |
| 2026-04-06 | Split Arc into Session Arc (episodic) + Session Output (semantic) — LoreSpec-derived. |
