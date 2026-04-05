---
name: harvest
preferred_activation: harvest
description: "Cross-agent extraction ritual. Primary trigger: harvest. Reads on-disk cadence context (self-memory, gate, dream handoff, territories, git), then emits a structured Session Harvest Packet for pasting into a midstream agent session — analysis import, not cold start. Does not end with coffee."
---

# Session Harvest (`harvest`)

**Preferred activation:** say **`harvest`**. Also responds to **`session harvest`**, **`export session`**, **`analysis handoff`**, **`extract session`**, or **`harvest this session`**.

`harvest` produces a **Session Harvest Packet** — a structured markdown block the operator pastes into **another agent session that is already underway** (parallel tooling, second Cursor thread, review agent). It is **not** a replacement for **`bridge`** (fresh-thread continuity + seal + trailing `coffee`).

**Chat arc limits:** The agent **does not** receive a full Cursor thread export API. **Session arc** = (a) **visible conversation in this thread**, (b) **operator one-line steer** if context is thin, (c) optional **`users/<id>/session-transcript.md`** on disk when instances use it. Do not promise full transcript replay from the skill alone.

**Dual-repo / EXECUTE scope:** When work spans **template + instance** repos, **EXECUTE** should name scope: **instance only**, **companion-self (template) only**, or **both**. Harvest does **not** require push.

---

## When to use

| Scenario | Path | Why |
|----------|------|-----|
| **Parallel or downstream agent needs dense context** | `harvest` | Single paste: outcomes, insights, files, risks, asks — **no** `coffee` tail |
| **Closing Cursor for a fresh thread** | **`bridge`** | Seal repo + **Session Bridge** packet ending with lone `coffee` |
| **Work-start / reorientation hub** | **`coffee`** | Template/instance morning ritual; not an export packet |
| **End-of-day consolidation** | **`dream`** | Night closeout + handoff artifact; not a handoff packet |

**Harvest vs bridge (one line):** Bridge packet **must** end with standalone **`coffee`** for cold start (see [bridge-packet-contract](../../../docs/skill-work/work-cadence/bridge-packet-contract.md)). Harvest packet **must not** end with **`coffee`**; it ends with the contract closing line so pastes are never confused.

---

## Modes

One skill; adjust emphasis via operator wording or optional script flag:

| Mode | Emphasis |
|------|----------|
| **`default`** | Balanced outcomes + insights + next steps |
| **`technical`** | Files, modules, commands, failure modes |
| **`strategic`** | Decisions, tradeoffs, tensions, executive compression |
| **`minimal`** | Short packet; still follow [harvest-packet-contract](../../../docs/skill-work/work-cadence/harvest-packet-contract.md) (omit empty sections) |

---

## Guardrails

- **No default commit/push** — harvest is read + synthesize unless the operator explicitly asks for git actions.
- **No gate merges** — harvest does not approve candidates or touch the review queue beyond reading.
- **No Record authority** — the packet is operator/tooling context, not governed truth.
- **Signal over volume** — compress; tag brittle lines `{fact}` / `{proposal}` / `{uncertain}`.
- **Preserve uncertainty** — do not flatten open questions into false closure.

---

## Step 1 — Read on-disk state

Resolve **`<id>`** from the instance (`COMPANION_USER_ID`, default **`demo`** in this template). Read (do not ask — just read):

1. **`users/<id>/self-memory.md`** — pointers, open loops, calibrations (if present)
2. **Gate surface** — `users/<id>/recursion-gate.md` and/or `users/<id>/recursion-gate.json`, and/or instance `review-queue/` per layout (**do not** merge)
3. **`users/<id>/daily-handoff/night-handoff.json`** — template dream handoff (if present)
4. **Instances** may use **`users/<id>/last-dream.json`** instead of or alongside the handoff JSON — read if present
5. **Territories** — active `docs/skill-work/**` READMEs and `*-history.md` files (scan for recent motion; omit empty)
6. Optionally **`users/<id>/session-transcript.md`** — if the instance uses it

Also run in **this** repo:

7. **`git status -sb`**
8. **`git log --oneline -10`**

**Dual-repo awareness:** If the session touched a **second** git root (e.g. instance + template in a multi-root workspace), add **one line** `git status -sb` there — mirror **bridge** awareness; **no** required push.

**Optional helper:** `python3 scripts/session_harvest.py -u <id> [--mode MODE] [--emit-template] [--log]` — checklist + template only; the agent still fills narrative from the thread.

---

## Step 2 — Extract from the visible session

From **this thread** (plus operator steer / optional session-transcript), compress into:

- Main outcomes, strongest insights, decisions vs discussion
- Artifacts (paths, roles, existing vs proposed)
- Risks, tensions, critiques, open questions
- Recommended next steps, **suggested asks** for the receiving agent (Analyze…, Critique…, Compare…)

---

## Step 3 — Emit packet

Output **one** markdown block following **[harvest-packet-contract](../../../docs/skill-work/work-cadence/harvest-packet-contract.md)** — section order, **no** trailing **`coffee`**, **required final line** per contract.

---

## After the paste — improve the ritual (no extra tooling)

**Optional operator habit** (scratch or mental note is enough): once the packet is in the **receiving** session, briefly score:

1. **Load** — Did the receiver skip re-discovery? (yes / partial / no)
2. **Accuracy** — Any wrong `{fact}` or missing caveat?
3. **Action** — Did **Suggested asks** produce useful work without scope creep?

**Recursive tightening:** If the **same friction** shows up **twice**, patch **[harvest-packet-contract](../../../docs/skill-work/work-cadence/harvest-packet-contract.md)** or **this skill** — not governed identity surfaces. Optional: save a strong packet under `harvest-packets/` as an informal quality bar.

**Cadence telemetry** (`log_cadence_event.py --kind harvest`) stays **optional**; this loop does not require it.

---

## Optional persistence

Default: packet **only in chat**. If the operator says **save:** suggest `docs/skill-work/work-cadence/harvest-packets/YYYY-MM-DD-harvest.md` or a rolling `last-harvest.md` — **operator-owned**, not Record.

---

## Related

- **`bridge`** — [SKILL.md](../bridge/SKILL.md) · [bridge-packet-contract.md](../../../docs/skill-work/work-cadence/bridge-packet-contract.md)
- **`coffee`** — [SKILL.md](../coffee/SKILL.md)
- **`dream`** — [SKILL.md](../dream/SKILL.md)
- **Cadence hub** — [work-cadence README](../../../docs/skill-work/work-cadence/README.md)
- **Packet contract** — [harvest-packet-contract.md](../../../docs/skill-work/work-cadence/harvest-packet-contract.md)

---

## Revision log

| Date | Change |
|------|--------|
| 2026-04-05 | Template skill (bridge sibling; gate + night-handoff + instance variants). |
| 2026-04-06 | Doc-only post-paste review loop (load / accuracy / action); recursive tighten contract or skill. |
