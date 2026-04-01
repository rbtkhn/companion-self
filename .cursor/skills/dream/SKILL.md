---
name: dream
preferred_activation: dream
description: "End-of-day closeout cadence for companion-self instances. Primary trigger: dream. Dream is the end-of-day consolidation pass: a bounded ritual that captures the day's signal, writes a handoff for tomorrow's coffee, and reports uncommitted work. Usually one session per day."
---

# Dream

**Preferred activation:** say **`dream`**. Also responds to **`night brief`**, **`cadence night`**, or **`closeout`**.

`dream` is not another work-start ritual. `dream` is the **end-of-day consolidation pass**.

Its purpose is to help the system settle, compress, and prepare for tomorrow. A dream session does not try to push work forward aggressively. It closes the day by capturing the strongest signal, setting a clear carry-forward action, and writing a handoff artifact that tomorrow's `coffee` will pick up.

Normally there is only one `dream` session per day, near the end of the day. Extra runs are allowed, but they are exceptional rather than the norm.

## Design intent

`dream` should feel like closure, settling, and quiet integration. It should not feel like another stimulant or another planning sprint. Because it is a consolidation ritual, it should be bounded, calm, and trustworthy: enough maintenance to reduce entropy, but never so much autonomy that it blurs governance or begins acting like a second operator.

## Success condition

A `dream` succeeds if, after using it, the system feels quieter, cleaner, and better prepared for tomorrow.

Its success condition is not dramatic change. Its success condition is that the day's signal is captured, a clear next action is set, and no ungated mutation has occurred.

## Step 1 — Automated actions

Run the consolidated cadence runner:

```bash
python3 scripts/cadence-dream.py --user <id>                        # standard (default)
python3 scripts/cadence-dream.py --user <id> --mode reflective      # deeper end-of-week
python3 scripts/cadence-dream.py --user <id> --mode minimal         # low-energy nights
python3 scripts/cadence-dream.py --user <id> --dry-run              # inspect without writing
```

Add `--suggest-gate` for gated candidate suggestions. The underlying `good-night-brief.py` is still callable directly.

The ritual:

1. Assesses the day's status (finished well / partial / blocked)
2. Captures one high-value signal
3. Sets one carry-forward action for tomorrow
4. Sets a stop condition (what not to overdo)
5. Optional reset cue (what to let go of tonight)
6. Writes `daily-handoff/night-handoff.json` (handoff for tomorrow's coffee)
7. Reports uncommitted work (git status)

**Morning handoff:** When `--write-closeout` is active (the default via the runner), the night brief writes `users/<id>/daily-handoff/night-handoff.json` — a compact summary that tomorrow's `coffee` Step 1 automatically picks up and displays. This closes the choreography gap: coffee knows what dream captured without the operator carrying it across threads.

## What to return

Return a short night-close brief with:

- Day status: finished well / partial / blocked
- One signal: the strongest thing captured today
- Tomorrow top action: one clear next step
- Stop condition: what to avoid overdoing
- Optional reset cue: what to let go of tonight
- Git status: uncommitted work snapshot

If nothing important changed, say so plainly. A quiet run is success.

## Example return shape

```md
## Dream

- Day status: partial
- One signal: WORK signal: completed cadence upstream
- Tomorrow top action: Review pending gate candidates first.
- Stop condition: Stop after top action is complete; avoid adding new maintenance tasks.
- Optional reset cue: Release unfinished loops; begin with the top action tomorrow.
```

## Guardrails

- Do not bypass `recursion-gate.md`.
- Do not directly rewrite identity truth containers (`self.md`, `self-evidence.md`, etc.).
- Do not let `dream` become an autonomous merge agent.
- Prefer bounded closeout over speculative semantic intervention.
- A quiet run is normal; do not manufacture significance.
- Gate suggestions are advisory — they do not auto-stage.

## Relation to coffee

`coffee`, `dream`, and `bridge` form the cadence triad.

- **`coffee`** = repeated framing dose
- **`dream`** = end-of-day consolidation pass
- **`bridge`** = session-scale handoff (seal, push, carry forward)

`coffee` restores orientation, clarity, and agency.
`dream` settles continuity, captures the day's signal, and prepares tomorrow's state.

Multiple `coffee` sessions per day are normal.
Usually one `dream` session per day is normal.

`coffee` should feel like a sip.
`dream` should feel like sleep.

## Cadence choreography

`coffee`, `dream`, and `bridge` form the cadence triad:

| Time | Ritual | What it does |
|------|--------|-------------|
| **Morning** | `coffee` (work-start) | Read dream handoff, context snapshot, session options |
| **During day** | `coffee` (reorientation) | Re-sip as needed — many per day is normal |
| **End of day** | `dream` | Capture signal, set carry-forward, write handoff JSON |
| **Session close** | `bridge` | Seal repo (commit/push), synthesize transfer prompt for next session |

**Dream's role is maintenance, not session closure.** Dream settles continuity and writes the handoff artifact. It does not commit, push, or produce a transfer prompt. If the operator is also closing the session, `bridge` follows dream.

| Scenario | Path |
|----------|------|
| End of day + closing session | `dream` then `bridge` |
| End of day, keeping session | `dream` alone |
| Mid-day, closing session | `bridge` alone (no dream needed) |

**Morning pickup:** `good-morning-brief.py` reads `daily-handoff/night-handoff.json` and displays the carry-forward action and last-night signal.

For the full decision tree, see [bridge SKILL.md](../bridge/SKILL.md).

## Modes

| Mode | Duration | When to use |
|------|----------|-------------|
| `minimal` | ~1-2 min | Low-energy nights |
| `standard` | ~2-4 min | Most nights |
| `reflective` | ~4-6 min | End of sprint/week |

## Cadence audit

Each successful dream run may append one line to `docs/skill-work/work-cadence/work-cadence-events.md` via `scripts/log_cadence_event.py`. Instances wire this into their consolidated runners.

## Related files

- `scripts/cadence-dream.py` — consolidated runner
- `scripts/good-night-brief.py` — underlying brief generator
- `docs/good-night-brief-spec.md` — full spec
- `docs/good-night-template.md` — recommended night sequence
- `docs/skill-work/work-cadence/README.md` — cadence territory
- `docs/skill-work/work-cadence/work-cadence-events.md` — per-run cadence telemetry
- `.cursor/skills/coffee/SKILL.md` — morning-side counterpart
