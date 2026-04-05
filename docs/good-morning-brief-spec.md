# Good Morning Brief Script Spec

This document specifies `scripts/good-morning-brief.py` for companion-self instances.

Goal: provide a daily startup brief in under ~3 minutes while preserving gate safety and optional sync behavior.

---

## 1) CLI Contract

### Command

```bash
python3 scripts/good-morning-brief.py --user <id> [options]
```

### Required arguments

- `--user <id>`: Instance user id under `users/<id>/`.

### Optional arguments

- `--mode minimal|standard|deep` (default: `standard`)
  - `minimal`: greeting + condensed sync status
  - `standard`: full default flow
  - `deep`: adds richer snapshot and expanded session options
- `--emit-json`
  - Print machine-readable JSON object to stdout.
- `--check-sync`
  - Run optional sync checks in this order:
    1. template alignment
    2. work-dev sync (if established)
    3. work-business sync (if established)
- `--write-intention`
  - Persist daily intention note only (no identity merges).
- `--upstream-repo <url>`
  - Template upstream URL for alignment checks.
  - Default: `https://github.com/rbtkhn/companion-self`.
- `--upstream-ref <ref>`
  - Template ref for alignment checks.
  - Default: `main`.
- `--max-lines <n>`
  - Cap human-readable output length for chat/UI surfaces.
- `--write-checkback`
  - Write `users/<id>/daily-handoff/morning-checkback-<today>.json` (requires `--checkback-helpful`). Operational telemetry only; not Record.
- `--checkback-helpful yes|no|partial`
  - Whether last night’s `night-handoff.json` was helpful (paired with `--write-checkback`).
- `--checkback-outcome "text"`
  - Optional one-line outcome for yesterday’s top action.
- `--coffee-context-file <path>`
  - JSON written by `cadence-coffee.py` (operational only). Supplies delta lines, branch triage, suggested next mode, and optional lane hook inputs. When absent, orientation hints still run from on-disk context only.
- `--coffee-lane <id>`
  - Optional session-shaping hook: `write`, `gate`, `build`, `research`, or `none`. Passed through from `cadence-coffee.py --lane`. Instance overrides may extend mapping in a forked `good-morning-brief.py`.

### Handoff schema v2 pickup

When `night-handoff.json` includes `handoffSchemaVersion: 2`, the morning brief surfaces `topActionReason`, `residueLedger`, `worktreeState` / `worktreeAdvice`, `quietRun`, `ignoreTomorrow`, `activeLaneHint`, and structured `gateSuggestions` in the context snapshot (capped lines).

If the WRITE bridge overrides `tomorrowTopAction`, the payload includes `writeBridgeOverrodeHandoff` and `handoffExecutionBeforeWriteBridge`, and the human-readable output notes the override so `topActionReason` does not look contradictory.

### Exit codes

- `0`: Success (including degraded-success fallbacks).
- `1`: Invalid CLI usage/arguments.
- `2`: Missing required instance path (`users/<id>/` not found).
- `3`: Unrecoverable runtime error (unexpected parsing/execution exception).

Notes:
- Missing optional files, missing sync surfaces, or upstream unreachable should not return non-zero by default; report status in output instead.

---

## 2) Input Sources and Precedence

All instance data should be read from `users/<id>/` first.

### Primary context sources

1. `users/<id>/self-memory.md` (ephemeral context)
2. `users/<id>/self-evidence.md` (recent activity/evidence)
3. `users/<id>/recursion-gate.md` (pending candidates)
4. `users/<id>/self-curiosity.md`
5. `users/<id>/self-personality.md`
6. `users/<id>/self-knowledge.md` (knowledge edge extraction; read-only)
7. `users/<id>/self-work.md` (cross-lane coordination surface)
8. `users/<id>/self-skill-think.md`
9. `users/<id>/self-skill-write.md`
10. `users/<id>/self-skill-work.md`
11. `users/<id>/self-library.md` (reference shelf advisory; read-only)

### Optional sync surfaces

Used only when `--check-sync` is enabled and surfaces exist:

- `docs/skill-work/work-dev/**` (or instance mirror equivalent)
- `docs/skill-work/work-business/**` (or instance mirror equivalent)
- `docs/skill-work/self-work/sync-pack/*` (template sync references)

### Precedence rules

1. Instance-local files (`users/<id>/...`) override generic defaults.
2. Explicit CLI flags override default values from docs.
3. If optional files are missing, emit structured fallback status and continue.

---

## 3) Output Schema

Script must produce:

- human-readable brief (default)
- JSON object when `--emit-json` is set

### Human-readable sections

1. `warmGreeting`
2. `contextSnapshot` (2-4 high-signal bullets; may prefix “Since last coffee” when runner supplies delta)
3. Optional **Coffee orientation** block (capped bullets from `coffeeOrientationHints`)
4. `intentionPrompt` (optional; mode-dependent)
5. `syncSummary` (optional; if `--check-sync`)
6. `sessionOptions` (2-3 realistic options; may be lane- or residue-tweaked)
7. `dailyOpsHandoff` (top sync/execution/gate action suggestions)
8. Optional **Suggested next mode** line when runner passes `suggestedCoffeeMode` via context file

### JSON schema (target shape)

```json
{
  "user": "string",
  "date": "YYYY-MM-DD",
  "mode": "minimal|standard|deep",
  "warmGreeting": "string",
  "contextSnapshot": [
    "string"
  ],
  "intentionPrompt": {
    "enabled": true,
    "prompt": "string"
  },
  "syncSummary": {
    "enabled": true,
    "templateAlignment": {
      "status": "aligned|minor_drift|major_drift|unavailable|skipped",
      "upstreamRepo": "string",
      "upstreamRef": "string",
      "notes": [
        "string"
      ]
    },
    "workDev": {
      "status": "not_established|no_relevant_updates|relevant_updates_found|blocked|skipped",
      "nextSteps": [
        "string"
      ]
    },
    "workBusiness": {
      "status": "not_established|no_relevant_updates|relevant_updates_found|blocked|skipped",
      "nextSteps": [
        "string"
      ]
    }
  },
  "sessionOptions": [
    {
      "label": "string",
      "reason": "string"
    }
  ],
  "selfWorkBridge": {
    "topSkillFocus": "THINK|WRITE|WORK",
    "skillObjectiveId": "string",
    "nextEvidenceTarget": "string"
  },
  "knowledgeBridge": {
    "knowledgeEdge": "string",
    "knowledgeObjectiveId": "string",
    "parseConfidence": "none|low|medium|high"
  },
  "curiosityBridge": {
    "curiosityEdge": "string",
    "curiosityObjectiveId": "string",
    "parseConfidence": "none|low|medium|high"
  },
  "personalityBridge": {
    "workStyle": "neutral|analytical|playful",
    "pacePreference": "standard|short_bursts|deep_focus",
    "tonePreference": "direct|calm|playful",
    "parseConfidence": "none|medium|high"
  },
  "libraryBridge": {
    "activeShelfTopic": "string",
    "staleReferenceAlert": "string",
    "suggestedLookupAction": "string",
    "parseConfidence": "none|low|medium|high"
  },
  "writeBridge": {
    "knowledgeSeed": "string",
    "curiositySeed": "string",
    "voiceStyle": "string",
    "suggestedWriteAction": "string",
    "parseConfidence": "none|low|medium|high"
  },
  "dailyOpsHandoff": {
    "topSyncAction": "string",
    "topExecutionAction": "string",
    "topGateAction": "string"
  },
  "coffeeOrientationHints": {
    "sipDiagnosis": "string",
    "bestNextMove": "string",
    "likelyFriction": "string",
    "doNotStartWith": "string",
    "branchHygieneClass": "string",
    "recommendedBranchAction": "string"
  },
  "coffeeRunnerMeta": {
    "branchHygieneClass": "clean|watch|risky",
    "recommendedBranchAction": "none|inspect|reconcile",
    "suggestedCoffeeMode": "light|standard|deep",
    "deltaLines": ["string"]
  },
  "warnings": [
    "string"
  ]
}
```

**Coffee orientation (human output):** After the greeting and before session options, the script may print a capped `### Coffee orientation` block (up to four bullets) derived from `coffeeOrientationHints`. It is heuristic and read-only.

**Residue-aware options:** When night handoff v2 signals strong carry-forward (`tomorrowTopAction` + `topActionReason`, not `quietRun`), `sessionOptions` may be trimmed or reordered conservatively.

**Lane hook:** `--coffee-lane` may promote a matching option or add one lane-specific line; default mapping is a small stub suitable for instance override.

---

## 4) Write Targets and Persistence Rules

Writes are opt-in and bounded.

### Allowed writes

- Daily intention note only when `--write-intention` is set.
  - Recommended path: `users/<id>/daily-intentions/YYYY-MM-DD.md`
  - If path does not exist, create directory safely.
- No automatic write to `self-work.md` from this script. The script may read it to infer `selfWorkBridge` suggestions.
- Optional sync summary handoff block in a non-identity operational file if explicitly enabled in future flags (not default).

### Disallowed writes

- No writes to:
  - `users/<id>/self.md`
  - `users/<id>/self-evidence.md` merge sections
  - any identity truth containers outside explicit gate process
- No direct merges from script into Record.

### Generated-content marker

Any persisted output should include a short marker, e.g.:

`generated_by: good-morning-brief.py`

---

## 5) Fallback Logic

- If `users/<id>/` missing -> exit code `2`.
- If optional file missing -> continue; add warning and fallback phrasing.
- If `self-knowledge.md` parse confidence is low:
  - keep existing `topExecutionAction` fallback behavior,
  - emit warning and continue.
- If `self-curiosity.md` parse confidence is high:
  - allow advisory "curiosity edge" execution suggestion when no stronger handoff/knowledge edge is available.
  - do not write curiosity suggestions back to identity files.
- If `self-personality.md` is present:
  - derive advisory pacing/tone preferences (`personalityBridge`) and use them to rank session options.
  - do not write these preferences back to identity files.
- If `self-library.md` exists:
  - derive advisory `libraryBridge` hints for lookup anchoring only (no identity writes).
  - allow `topSyncAction` to include a shelf anchor when parse confidence is high.
- Build `writeBridge` from `knowledgeBridge + curiosityBridge + personalityBridge`:
  - advisory-only synthesis for WRITE planning,
  - if `topSkillFocus == WRITE`, `topExecutionAction` may use `writeBridge.suggestedWriteAction`.
- If sync lanes not established -> set status to `not_established`.
- If upstream unavailable during template alignment:
  - set `templateAlignment.status = unavailable`
  - continue without failing full run.
- If markdown parse fails for a source file:
  - treat as raw text fallback and continue.

---

## 6) Safety Constraints

- Preserve gate discipline:
  - never merge identity updates
  - route identity implications to suggestions for `recursion-gate.md`
- Keep `standard` mode under ~3 minutes in normal local conditions.
- No assumptions about symlinks or specialized repo layout beyond `users/<id>/`.
- No destructive file operations.
- No dependency on external packages; Python stdlib + existing system tools only.

---

## 7) Test Matrix (Spec-Level)

1. **Minimal instance baseline**
   - Required files present, optional sync surfaces absent.
   - Expected: success with `not_established` sync statuses.

2. **Full instance with sync lanes**
   - work-dev/work-business sync surfaces established.
   - Expected: ordered sync summary with next-step suggestions.

3. **Missing/malformed files**
   - Missing `self-memory.md`, malformed markdown in `self-evidence.md`.
   - Expected: warnings + successful fallback output.

4. **Upstream unavailable**
   - network/repo resolution failure.
   - Expected: `templateAlignment=unavailable`, overall success.

5. **Deterministic JSON shape**
   - `--emit-json` always returns schema-compliant keys.

6. **Idempotent repeated runs**
   - Running twice without new inputs should not produce unintended writes.

7. **Write-intention safety**
   - `--write-intention` writes only to allowed path and leaves identity files untouched.

---

## 8) Mapping to Existing Template Docs

This spec aligns with:

- [INITIAL-GOOD-MORNING](skill-work/self-work/sync-pack/INITIAL-GOOD-MORNING.md)
- [LONG-TERM-OBJECTIVE](long-term-objective.md)
- [IDENTITY-FORK-PROTOCOL](identity-fork-protocol.md)
- [SYNC-PACK README](skill-work/self-work/sync-pack/README.md)

---

## 9) Implementation Notes

- This is a specification document only.
- Implementation target is `scripts/good-morning-brief.py`.
- Add script tests after implementation under repo test conventions.

