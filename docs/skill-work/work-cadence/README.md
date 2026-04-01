# work-cadence

**Purpose:** Template-level doctrine, boundaries, and architecture for the daily cadence pair — `coffee` (morning orientation) and `dream` (night consolidation). The executable trigger surfaces live in `.cursor/skills/coffee/SKILL.md` and `.cursor/skills/dream/SKILL.md`.

**Not** Record truth. **Not** a merge path. **Not** identity-relevant unless gated.

---

## Role

| Role | Description |
|------|-------------|
| **Cadence architecture** | Defines the shape of daily rhythm: coffee (orientation, repeated), dream (consolidation, once). |
| **Night-to-morning handoff** | Documents the `daily-handoff/night-handoff.json` data contract that bridges dream output to coffee Step 1. |
| **Boundary surface** | Explains what belongs in operational/ephemeral surfaces versus what must escalate to the gate. |
| **Script topology** | Maps how consolidated runners delegate to underlying brief generators. |

---

## Daily rhythm

`coffee` and `dream` form a cognitive pair:

| Time | Ritual | What it does |
|------|--------|-------------|
| **Morning** | `coffee` (standard) | Read dream handoff, context snapshot, skill focus, session options |
| **During day** | `coffee` (reorientation) | Re-sip as needed — many per day is normal |
| **End of day** | `dream` | Capture signal, set carry-forward, write handoff JSON |

**Many coffees, one dream.** `coffee` is designed for repetition (each run restores orientation). `dream` is designed for closure (one per day is the norm).

`coffee` should feel like a sip. `dream` should feel like sleep.

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

- daily cadence architecture (coffee/dream pair)
- handoff contract design and schema
- runner mode definitions and dispatch
- script topology and extension points
- boundary rules for operational vs gated content

Out of scope:

- instance-specific menu systems (A-H, etc.)
- instance-specific maintenance passes (integrity, governance, contradiction)
- Record merges or identity edits without the gate
- individual work-territory content (politics, dev, business, etc.)
- sync-pack mechanics (those live in `self-work/sync-pack/`)
