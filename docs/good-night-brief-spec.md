# Good Night Brief Script Spec

This spec defines `scripts/good-night-brief.py` for companion-self instances.

Objective: provide a short end-of-day closeout (2-4 minutes standard mode) that captures one high-value signal and one actionable handoff for tomorrow.

---

## 1) CLI Contract

### Command

```bash
python3 scripts/good-night-brief.py --user <id> [options]
```

### Required

- `--user <id>`

### Optional

- `--mode minimal|standard|reflective` (default: `standard`)
- `--emit-json` (machine-readable output)
- `--write-closeout` (persist closeout note)
- `--suggest-gate` (include gated candidate suggestions, no merges)
- `--max-lines <n>` (output cap for chat surfaces)

### Exit codes

- `0`: success (including graceful degraded output)
- `1`: invalid arguments
- `2`: missing instance path (`users/<id>/`)
- `3`: unrecoverable runtime failure

---

## 2) Inputs and precedence

Primary instance-local sources:

1. `users/<id>/self-memory.md`
2. `users/<id>/self-evidence.md` (recent entries)
3. `users/<id>/recursion-gate.md`
4. `users/<id>/self-skill-think.md`
5. `users/<id>/self-skill-write.md`
6. `users/<id>/self-skill-work.md`

Optional context:

- `docs/good-night-template.md`
- instance-specific nightly preference doc if present (future extension)

Precedence:

1. explicit CLI args
2. instance-local defaults
3. template defaults

---

## 3) Output schema

### Human-readable sections

1. `dayStatus`
2. `oneSignal`
3. `tomorrowTopAction` + `topActionReason`
4. `stopCondition` (may reflect `tomorrowEnergyFit`)
5. `optionalResetCue`
6. Optional lines: `quietRun`, `activeLaneHint`, `ignoreTomorrow`, `residueLedger`, gate hints, `worktreeState` / `worktreeAdvice` (after runner merge)

### JSON shape

`handoffSchemaVersion` **2** (current template) adds judgment and residue fields while keeping the core keys stable. Readers should tolerate missing optional keys (older handoffs).

```json
{
  "handoffSchemaVersion": 2,
  "user": "string",
  "date": "YYYY-MM-DD",
  "mode": "minimal|standard|reflective",
  "dayStatus": "finished_well|partial|blocked",
  "oneSignal": "string",
  "tomorrowTopAction": "string",
  "topActionReason": "string",
  "stopCondition": "string",
  "optionalResetCue": "string",
  "tomorrowEnergyFit": "low|normal|high",
  "quietRun": true,
  "activeLaneHint": "GATE|WORK|SEED|NONE",
  "ignoreTomorrow": "string",
  "residueLedger": {
    "must_resume": "string",
    "safe_to_drop": "string",
    "blocked": "string",
    "watch_later": "string"
  },
  "worktreeState": "clean|light residue|risky residue",
  "worktreeAdvice": "string",
  "gateSuggestions": [
    "string | { \"item\": \"string\", \"reason\": \"string\", \"urgency\": \"string\" }"
  ],
  "warnings": [
    "string"
  ]
}
```

`worktreeState` / `worktreeAdvice` are written by `cadence-dream.py` after `good-night-brief.py` completes (git triage only; no commits).

**Reflective mode:** also writes `users/<id>/daily-handoff/weekly-reflection.json` (rolling artifact for end-of-sprint/week).

---

## 4) Write targets and safety

Allowed writes only with `--write-closeout`:

- recommended: append/update in `users/<id>/self-memory.md`
- or write daily note under an operational path (instance policy)

Disallowed:

- no writes to `users/<id>/self.md`
- no direct merges into identity/evidence truth containers
- no auto-approval of gate candidates

Generated content should include a marker, e.g.:

`generated_by: good-night-brief.py`

---

## 5) Fallback logic

- Missing optional files -> continue with defaults.
- Missing recent evidence -> generate minimal closeout with prompt placeholders.
- Parse issues -> raw-text fallback and warning.

---

## 6) Test matrix (spec-level)

1. baseline minimal instance
2. full instance with recent evidence
3. missing/malformed optional files
4. deterministic `--emit-json` output
5. idempotent repeated runs without duplicate unsafe writes
6. `--write-closeout` writes only to allowed surfaces

---

## 7) Alignment references

- [Good Night Template](good-night-template.md)
- [Good Morning Brief Spec](good-morning-brief-spec.md)
- [Identity Fork Protocol](identity-fork-protocol.md)

