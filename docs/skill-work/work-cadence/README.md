# work-cadence

**Purpose:** Template-level doctrine, boundaries, and architecture for the daily cadence triad — `coffee` (orientation), `dream` (consolidation), and `bridge` (session handoff). The executable trigger surfaces live in `.cursor/skills/coffee/SKILL.md`, `.cursor/skills/dream/SKILL.md`, and `.cursor/skills/bridge/SKILL.md`.

**Not** Record truth. **Not** a merge path. **Not** identity-relevant unless gated.

---

## Role

| Role | Description |
|------|-------------|
| **Cadence architecture** | Defines the shape of daily rhythm: coffee (orientation, repeated), dream (consolidation, once). |
| **Night-to-morning handoff** | Documents the `daily-handoff/night-handoff.json` data contract that bridges dream output to coffee Step 1. |
| **Cadence event audit** | Append-only telemetry of each run via `work-cadence-events.md` and `scripts/log_cadence_event.py`. |
| **Boundary surface** | Explains what belongs in operational/ephemeral surfaces versus what must escalate to the gate. |
| **Script topology** | Maps how consolidated runners delegate to underlying brief generators. |

---

## Daily rhythm

`coffee`, `dream`, and `bridge` form the cadence triad:

| Time | Ritual | What it does |
|------|--------|-------------|
| **Morning** | `coffee` (standard) | Read dream handoff, context snapshot, skill focus, session options |
| **During day** | `coffee` (reorientation) | Re-sip as needed — many per day is normal |
| **End of day** | `dream` | Capture signal, set carry-forward, write handoff JSON |
| **Session close** | `bridge` | Seal (commit/push), synthesize transfer prompt for next session |

**Many coffees, one dream, one bridge.** `coffee` is for repetition. `dream` is for closure. `bridge` is for carry-forward.

`coffee` should feel like a sip. `dream` should feel like sleep. `bridge` should feel like sealing an envelope.

---

## Why three rituals

Work fails on three clocks:

**The framing clock (hours).** During the day, orientation degrades under context load. Not lack of information — degraded framing. `coffee` restores it. Many sips per day.

**The residue clock (day).** By evening, unresolved threads, integrity drift, and unprocessed signals accumulate. `dream` settles them without dramatic mutation.

**The context clock (session).** At session boundaries, agent memory goes to zero. Everything not on disk is lost. `bridge` seals the session and produces a transfer prompt so the next thread starts oriented instead of blank.

Each clock needs its own ritual because the failure modes are different. Reorientation is not consolidation. Consolidation is not transfer. Merging them into one ritual would either make it too heavy for frequent use or too shallow for end-of-day closure.

---

## Script topology

```
cadence-coffee.py
  └─ good-morning-brief.py        context, bridges, session options, handoff pickup
       └─ write_style_bridge.py   optional WRITE synthesis

cadence-dream.py
  └─ good-night-brief.py          signal capture, handoff write, gate suggestion
  └─ git status summary           uncommitted-work awareness
```

**Runners** are lightweight dispatch wrappers. **Briefs** hold all the parsing, bridge-building, and output logic. Instances may extend or replace the runners while keeping the briefs stable.

---

## Handoff contract

`dream` (via `good-night-brief.py --write-closeout`) writes `users/<id>/daily-handoff/night-handoff.json`.

`coffee` (via `good-morning-brief.py`) reads that file the next morning.

### night-handoff.json schema

| Field | Type | Purpose |
|-------|------|---------|
| `user` | string | Instance user id |
| `date` | ISO date | When dream ran |
| `mode` | string | Dream mode |
| `dayStatus` | string | `finished_well` / `partial` / `blocked` |
| `oneSignal` | string | Strongest signal from the day |
| `tomorrowTopAction` | string | Carry-forward action for morning |
| `stopCondition` | string | What not to overdo tomorrow |
| `optionalResetCue` | string | What to let go of tonight |
| `gateSuggestions` | string[] | Advisory gate staging hints |
| `warnings` | string[] | Parse/fallback warnings |

The handoff artifact is an operational file, not identity truth. It should not be committed to the Record or treated as evidence.

---

## Gate threshold

`work-cadence` is **operational by default**.

Keep changes in territory docs when they are about:

- cadence architecture (what each ritual does, in what order)
- handoff contract shape and fields
- runner mode definitions and dispatch logic
- coffee/dream choreography and timing

Stage to the instance's gate (`recursion-gate.md` or `review-queue/`) only when a cadence insight would change governed behavior, such as:

- durable prompt or policy behavior
- changes to how identity-relevant signals are captured
- new surfaces that cross into Record territory

This territory never creates a merge path. The instance's gate remains the membrane.

---

## Modes reference

### Coffee modes

| Mode | Brief mode | Sync checks | Branch snapshot | When to use |
|------|-----------|-------------|-----------------|-------------|
| `standard` | `standard` | Only if `--check-sync` | Full | Most mornings |
| `light` | `minimal` | Only if `--check-sync` | Compact (one line) | Quick reorientation |
| `deep` | `deep` | Yes (automatic) | Full | Start of week, template updates |
| `closeout` | N/A (delegates to dream) | No | No | End of day (prefer `dream`) |

### Dream modes

| Mode | Duration | When to use |
|------|----------|-------------|
| `minimal` | ~1-2 min | Low-energy nights |
| `standard` | ~2-4 min | Most nights |
| `reflective` | ~4-6 min | End of sprint/week |

---

## Instance extensions

Instances built from this template may extend cadence with:

- **Custom menu systems** (e.g. grace-mar's A-H multi-choice pattern)
- **Additional maintenance passes** (e.g. integrity checks, contradiction digest, memory normalization)
- **Territory-specific tracks** (e.g. work-politics, Predictive History)
- **Instance-specific runners** (replacing or wrapping the template runners)

These extensions belong in instance-local skills and territories, not in this template. The template provides the structural pattern; instances customize for their needs.

---

## Cadence event audit

Each coffee, dream, and bridge run appends one line to [work-cadence-events.md](work-cadence-events.md) via `scripts/log_cadence_event.py`. This is operator-facing telemetry — not the Record, not self-memory.

**Leaf-only rule:** Orchestrator scripts (wrappers that chain multiple steps) do not emit their own events. Only the leaf ritual logs.

**Split threshold:** If cadence events exceed ~200 lines/month, consider adding a JSONL sibling and keeping monthly rollup bullets in the markdown file.

---

## Write authority map

Which on-disk surfaces each ritual reads, writes, and whether companion approval is required.

| Ritual | Reads | Writes | Gate required? |
|--------|-------|--------|---------------|
| **coffee** | self-memory, gate, dream handoff, git status | nothing (read-only planning) | No |
| **dream** | self-memory, SELF, EVIDENCE, gate | self-memory, night handoff JSON, cadence events | No (Maintenance mode) |
| **bridge** | self-memory, gate, dream handoff, territories, git | git commits, cadence events | No (operational) |
| **gate merge** | gate candidates, SELF, EVIDENCE, prompt | SELF, EVIDENCE, prompt, session-log, gate, pipeline events | **Yes — companion approval required** |

**Key boundary:** coffee and bridge never write to identity surfaces. Dream writes to ephemeral/operational surfaces only. Only the gated merge path touches the Record.

---

## End-of-session decision tree

| Scenario | Path | Why |
|----------|------|-----|
| **End of day + closing session** | `dream` then `bridge` | Dream settles continuity; bridge seals and generates transfer prompt |
| **End of day, keeping session** | `dream` alone | Maintenance pass; same thread continues tomorrow |
| **Mid-day, closing session** | `bridge` alone | Seal repo, carry context forward; no maintenance needed |
| **Quick check before stepping away** | coffee closeout (instance-defined) | Lightweight status; no commit/push, no transfer prompt |

**Default:** If in doubt, `bridge`. It commits, pushes, and produces a transfer prompt. If it's also end of day, run `dream` first.

---

## Cadence troubleshooting

When a cadence run produces unexpected output, check these in order:

### Coffee output looks wrong

1. **Dream handoff missing?** Check the night handoff JSON — if absent or stale, dream didn't run or didn't complete.
2. **Wrong mode?** Check which mode was passed to the coffee runner. Run with the intended mode explicitly.
3. **Script failed silently?** Consolidated runners chain sub-scripts and stop on first failure. Check exit codes.

### Dream output looks wrong

1. **Integrity or governance failed?** Check the dream summary for failure flags. In strict mode, dream halts — no memory update, no handoff written.
2. **Handoff not written?** Dream only writes the handoff artifact when `apply=True` and maintenance is not halted.
3. **Cadence event not logged?** Gated on successful completion. Dry-run and halted dreams produce no cadence line by design.

### Bridge output looks wrong

1. **Commit failed?** Bridge commits are agent-driven. Check `git status -sb` in all relevant repos.
2. **Push rejected?** Usually means remote has new commits. Pull-rebase and retry.
3. **Transfer prompt thin?** Bridge synthesizes from on-disk state. Sparse sections mean those surfaces had nothing to report.

### General

- **Which cadence events actually ran?** Check `work-cadence-events.md` — one line per run.
- **Agent reading stale skill file?** Long sessions can cache file contents. Ask the agent to re-read.

---

## Continuity and trail

`work-cadence` does **not** replace any existing continuity surface.

- **Spec docs:** `docs/good-morning-brief-spec.md`, `docs/good-night-brief-spec.md`, `docs/good-night-template.md`
- **Sync pack:** `docs/skill-work/self-work/sync-pack/` (optional territory sync module)
- **Operational handoff:** `users/<id>/daily-handoff/night-handoff.json`
- **Ephemeral memory:** `users/<id>/self-memory.md`
- **Governed changes:** Instance-specific gate (`recursion-gate.md` or `review-queue/`)

---

## Adjacent surfaces

- [.cursor/skills/coffee/SKILL.md](../../../.cursor/skills/coffee/SKILL.md) — coffee trigger
- [.cursor/skills/dream/SKILL.md](../../../.cursor/skills/dream/SKILL.md) — dream trigger
- [.cursor/skills/bridge/SKILL.md](../../../.cursor/skills/bridge/SKILL.md) — bridge trigger
- [work-cadence-events.md](work-cadence-events.md) — per-run cadence telemetry
- [scripts/log_cadence_event.py](../../../scripts/log_cadence_event.py) — cadence event append helper
- [scripts/cadence-coffee.py](../../../scripts/cadence-coffee.py) — coffee runner
- [scripts/cadence-dream.py](../../../scripts/cadence-dream.py) — dream runner
- [scripts/good-morning-brief.py](../../../scripts/good-morning-brief.py) — morning brief generator
- [scripts/good-night-brief.py](../../../scripts/good-night-brief.py) — night brief generator
- [docs/good-morning-brief-spec.md](../../good-morning-brief-spec.md) — full morning spec
- [docs/good-night-brief-spec.md](../../good-night-brief-spec.md) — full night spec
- [docs/good-night-template.md](../../good-night-template.md) — recommended night sequence

---

## Scope boundaries

In scope:

- daily cadence architecture (coffee/dream/bridge triad)
- handoff contract design and schema
- cadence event audit (per-run telemetry)
- runner mode definitions and dispatch
- script topology and extension points
- boundary rules for operational vs gated content

Out of scope:

- instance-specific menu systems (A-H, etc.)
- instance-specific maintenance passes (integrity, governance, contradiction)
- Record merges or identity edits without the gate
- individual work-territory content (politics, dev, business, etc.)
- sync-pack mechanics (those live in `self-work/sync-pack/`)
