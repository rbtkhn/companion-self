# Evaluation design and regression

**Companion-Self template · Test cases and regression after schema or pipeline changes**

**Transcript primitive:** Build an eval: build three to five test cases with known good outputs and run them periodically, especially after model updates. (Here we apply it to the pipeline and schema: run after code or schema changes.)

---

## Purpose

- **Regression** — After changing schema, merge logic, or stage logic, run the fixture script to confirm staging and merge still produce the expected Record and gate state.
- **Acceptance** — Fixtures encode "known good" inputs and outputs; they double-check the [acceptance criteria](schema-record-api.md#acceptance-criteria-for-staging-and-merge).

---

## Fixture user

The script uses a dedicated user **`eval-fixture`** (`users/eval-fixture/`) so the demo user is not modified. The script creates minimal Record files there if missing, runs stage-and-merge flows, asserts, and optionally resets for the next run.

---

## Test cases (fixtures)

| # | Name | Input | Expected after stage | Expected after approve |
|---|------|--------|----------------------|-------------------------|
| 1 | THINK activity | raw_text: "Read chapter 2 of Dragon Guide; summarized migration habits.", skill_tag: THINK | One candidate; mind_category: knowledge; suggested_ix_section: IX-A | One evidence entry; one line in self-knowledge (IX-A). |
| 2 | WORK activity | raw_text: "Finished the dragon drawing; used watercolors.", skill_tag: WORK | One candidate; mind_category: curiosity; suggested_ix_section: IX-B | One evidence entry; one line in self-curiosity (IX-B). |
| 3 | Reject | (same as 1, but we reject) | — | Candidate removed from gate; no change to evidence or dimension files. |

The script runs at least (1) stage two activities → load and assert gate and candidate fields; (2) approve one → assert evidence count, dimension line, gate length; (3) optionally reject one → assert gate shrinks, Record unchanged.

---

## How to run

From repo root:

```bash
node scripts/run-eval-fixtures.js
```

Exit code 0 if all assertions pass; non-zero and stderr if any fail. Run after changing:

- `app/schema/record.js` (load, mergeCandidate, createCandidate, parsing)
- `app/pipeline/stage.js` (SKILL_MAP, staging)
- `app/pipeline/merge.js` (reviewCandidate, receipt writing)

---

## Adding or changing fixtures

- **Add a case:** Add a fixture entry in `scripts/run-eval-fixtures.js` (input + expected fields) and an assertion block.
- **Change schema:** Update expected assertions (e.g. new field, new file) and run; fix code until the script passes.
- **Periodic runs:** E.g. in CI or pre-commit hook; see [Project 6-week](project-6week-coding.md) for where a test step could be added.

See [Actionable insights from the transcript](actionable-insights-transcript.md) for why we added this.
