# Cursor pack from seed intake

**Companion-Self template**

Stage 0 **`seed_intake.json`** may include **`cursor_operator_profile`**: answers from the same intake / seed survey used for formation, so a **new instance** (or steward) records **how the operator will work in the IDE** before activation.

## Purpose

- **Single survey path** — No separate “Cursor questionnaire”; operator workspace preferences live beside use cases and constraints.
- **Deterministic presets later** — A future script (e.g. `scripts/generate-cursor-pack.py`) can read validated `seed_intake.json` and emit `.cursor/rules/` + `.cursor/skills/` from **versioned templates** under `templates/cursor-presets/` (to be added). **Human review** before commit is still required.
- **Knowledge boundary** — `operator_notes` is for **process** only. Do **not** treat free text as approved Record facts or inject undocumented companion claims into rules.

## Fields (`cursor_operator_profile`)

| Field | Meaning |
|--------|---------|
| `ide_primary` | Primary editor: `cursor`, `vscode`, `jetbrains`, `other`, `unspecified`. |
| `rules_pack_preset` | **template_steward** — minimal pack for upstream template work (see repo `.cursor/`). **instance_light** — forked instance: gate + path hygiene, no heavy operator cadence. **instance_operator** — aim to align with reference instance operator skills (e.g. grace-mar) when tooling is copied. **unspecified** — decide later. |
| `work_surface_hints` | Strings such as `work-politics`, `work-dev` to flag which WORK territories matter for optional rules. |
| `generate_cursor_pack_on_activation` | **true** = operator intends to run generator after activation; **false** = manual `.cursor` setup. |
| `operator_notes` | Human-readable; not auto-merged into rule bodies without review. |

## Preset → behavior (target state)

| `rules_pack_preset` | Intended pack (when generator exists) |
|---------------------|----------------------------------------|
| `template_steward` | Current companion-self defaults: long-term objective, workspace boundary, template layers, users-tree guard, generalize-from-reference, first-hour + promote skills. |
| `instance_light` | Steward subset + **instance fork** rules (see grace-mar work-companion-self **Phase 2** spec): `users/<id>/` boundary, no cross-instance copy, optional gate-before-merge. |
| `instance_operator` | Instance light + optional copy/adapt of reference **daily-warmup / handoff** skills **only if** instance ships matching scripts and `user_slug` substitution. |

## Validation

`cursor_operator_profile` is **optional** on `seed_intake.json`. If present, every property inside it is optional in practice (fill what you know); the schema allows partial objects. Run:

```bash
python3 scripts/validate-seed-phase.py users/<id>/seed-phase
```

## Related

- [seed-phase-artifacts.md](seed-phase-artifacts.md) — `seed_intake.json`
- [seed-phase-stages.md](seed-phase-stages.md) — Stage 0 intake
- Grace-Mar reference: [CURSOR-PERSONAS-RULES-SKILLS.md](https://github.com/rbtkhn/grace-mar/blob/main/docs/skill-work/work-companion-self/CURSOR-PERSONAS-RULES-SKILLS.md) (phase 2 instance owner)
