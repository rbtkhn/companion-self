---
name: coffee
preferred_activation: coffee
description: "Daily startup cadence for companion-self instances. Primary trigger: coffee. Coffee is a repeatable sip of coherence: a lightweight reorientation ritual that restores clarity, framing, and agency. Multiple coffee sessions per day are normal."
---

# Coffee

**Preferred activation:** say **`coffee`**. Also responds to **`morning brief`** or **`cadence morning`**.

`coffee` is not a startup ceremony. `coffee` is a **repeatable sip of coherence**.

Its purpose is to help the operator become more awake to the actual situation, more coherent about priorities, and more directed about the next move. A coffee session does not need to complete the day's thinking. It only needs to improve orientation enough that action becomes easier.

Multiple `coffee` sessions per day are normal. That is not redundancy; it is the point. Each `coffee` is another sip.

## Guardrails

- Do not turn `coffee` into a heavy maintenance ritual by default.
- Prefer a small number of salient next paths over exhaustive review.
- Keep the operator in the position of renewed agency, not procedural burden.
- `coffee` is for orientation; heavier consolidation belongs to `dream`.
- This is read-only planning. Do not merge or stage just because the warmup mentions candidates.
- If integrity fails, surface that before optional improvements.
- Agents have no cross-thread institutional memory; authority for the Record is **on-disk files + gated pipeline** — not model recall or chat summary.

## Relation to dream

`coffee`, `dream`, and `bridge` form the cadence triad:
- **`coffee`** = repeated framing dose (many per day)
- **`dream`** = end-of-day consolidation pass (usually once)
- **`bridge`** = session-scale handoff (once per session close)

`coffee` should feel like a sip. `dream` should feel like sleep. See `.cursor/skills/dream/SKILL.md` § *Cadence choreography* for the full day sequence and data handoff.

---

## "Coffee" = start here (two steps)

When the operator begins with **`coffee`** (or equivalent intent), treat it as opening a coffee session. If the message **clearly means closeout** (signing off, end of day), redirect to **`.cursor/skills/dream/SKILL.md`** instead. Otherwise, run **Step 1** scaled by the operator's chosen mode.

### Multiple coffees per day

The operator may say **`coffee`** more than once per calendar day for reorientation. This is normal. Each new `coffee` runs Step 1 again and starts a new session cycle.

### Step 1 — Automated actions

Run the consolidated cadence runner:

```bash
python3 scripts/cadence-coffee.py --user <id>                   # standard (default)
python3 scripts/cadence-coffee.py --user <id> --mode light      # lighter pass
python3 scripts/cadence-coffee.py --user <id> --mode deep       # deep with sync checks
```

Add `--write-intention` for a daily intention note. The underlying `good-morning-brief.py` is still callable directly for finer control.

**Dream handoff:** If `dream` ran yesterday, the morning brief automatically includes context from `users/<id>/daily-handoff/night-handoff.json` — the carry-forward action and last signal from the night closeout.

**Step 1 deliverables:** Greeting, context snapshot (recent evidence, curiosity spark, night handoff), skill focus, knowledge/curiosity edges, session options, top actions (sync, execution, gate). No identity writes.

**Step 1 guardrail:** Stay read-only — no merge/stage unless the operator uses a pipeline phrase.

### Step 2 — Session options

After Step 1 content, present the session options from the brief output. The `good-morning-brief.py` script generates personalized options based on the instance's personality bridge:

- **Deep Work** — Focus on one difficult task end-to-end.
- **Analyst Mode** — Review signals and synthesize next actions.
- **Light Review + Capture** — Close loops and stage signals safely.
- **End session** — Close the coffee session and proceed to normal work.

Instances may customize these options (e.g. add work-lane picks, gate review, territory-specific tracks) by extending the runner or overriding Step 2 in an instance-local skill.

**Re-offer rules:** After a session option is chosen and completed, re-offer the options unless the operator ends the session or switches to normal workflow.

---

## Modes

| Mode | What it runs | When to use |
|------|-------------|-------------|
| `standard` | Full morning brief + branch snapshot | Most mornings |
| `light` | Minimal brief + compact branch line | Quick reorientation |
| `deep` | Deep brief + sync checks + full branch snapshot | Start of week, after template updates |
| `closeout` | Night brief via `good-night-brief.py` | End of day (prefer `dream` skill) |

---

## Session trail (optional)

Sessions begin when the operator says **`coffee`**. To keep a trail: use `users/<id>/self-memory.md` (ephemeral) or a daily note surface per instance conventions. **Not** the gated Record.

## Cadence audit

Each successful coffee run may append one line to `docs/skill-work/work-cadence/work-cadence-events.md` via `scripts/log_cadence_event.py`. Instances wire this into their consolidated runners.

## Related files

- `scripts/cadence-coffee.py` — consolidated runner
- `scripts/good-morning-brief.py` — underlying brief generator
- `docs/good-morning-brief-spec.md` — full spec
- `docs/skill-work/work-cadence/README.md` — cadence territory
- `docs/skill-work/work-cadence/work-cadence-events.md` — per-run cadence telemetry
- `.cursor/skills/dream/SKILL.md` — night-side counterpart
