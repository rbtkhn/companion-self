# companion-self

**Companion-Self** is the **template** repo. **Grace-Mar** is the **instance** repo (the first and currently only instance).

**Release + compatibility metadata:** [`template-version.json`](template-version.json) — semver, release date, git tag, and `compatibilityContract` pointers (single source; no separate `template-contract.json`).

A new companion self is created **only when a new user completes seed phase** — not by copying another repo's `users/` or pre-filling a Record. **Seed Phase v2** is a visible artifact pipeline with JSON Schemas, confidence signals, and **readiness gating** before activation ([docs/seed-phase.md](docs/seed-phase.md)).

## Governed change

Companion-Self does not treat meaningful post-seed revision as silent memory drift.

When new evidence materially affects identity, curiosity, pedagogy, expression, memory governance, safety rules, or other durable operating commitments, the change should enter a change-review pipeline that preserves prior state, supporting evidence, contradiction type, confidence delta when available, and an explicit decision before governed state is updated.

See:
- [docs/change-review.md](docs/change-review.md)
- [docs/contradiction-policy.md](docs/contradiction-policy.md)
- [docs/change-types.md](docs/change-types.md)
- [docs/change-review-lifecycle.md](docs/change-review-lifecycle.md)

## Lawful Succession Engine

Companion-Self treats major post-seed changes not merely as profile updates, but as possible succession events that must preserve intelligible continuity.

The Lawful Succession Engine introduces a constitutional interpretation layer for materially important governed change. It asks not only whether a proposal is supported, but whether the proposed future state remains a lawful successor to the prior one.

See:
- [docs/lawful-succession.md](docs/lawful-succession.md)
- [docs/regime-classification.md](docs/regime-classification.md)
- [docs/constitutional-continuity.md](docs/constitutional-continuity.md)

- **Template (this repo):** Concept, protocol, seed-phase definition, and structure for creating a new companion self. No one's Record; no pilot data.
- **Instance (e.g. [Grace-Mar](https://github.com/rbtkhn/grace-mar)):** One live companion self — Record, bot, pipeline. Created from the template when a new user completes seed phase.
- **Compatibility:** Canonical template/instance rules — [docs/template-instance-contract.md](docs/template-instance-contract.md).

**Reference implementation:** [Grace-Mar](https://github.com/rbtkhn/grace-mar) — [grace-mar.com](https://grace-mar.com) (profile, bot, PRP). See [Instance patterns](docs/instance-patterns.md) for Grace-Mar variations and advanced patterns (analyst, staging format, session brief).

**Instance-specific boundary narrative** (grace-mar · companion-self · companion-xavier — what may cross, hard lines) lives in Grace-Mar: [docs/audit-boundary-grace-mar-companion-xavier-companion-self.md](https://github.com/rbtkhn/grace-mar/blob/main/docs/audit-boundary-grace-mar-companion-xavier-companion-self.md).

Optional: [companion-self.com](https://companion-self.com) when the concept site exists.

---

## Seed Phase as a formal asset

A companion instance is **not** created by prompt cloning alone. It must pass **Seed Phase**, a structured formation pipeline that establishes identity, curiosity, pedagogy, expression, and memory governance. Seed Phase produces **inspectable artifacts**, **confidence signals**, and a **readiness decision** before activation.

See:

- [docs/seed-phase.md](docs/seed-phase.md)
- [docs/seed-phase-stages.md](docs/seed-phase-stages.md)
- [docs/seed-phase-readiness.md](docs/seed-phase-readiness.md)
- [docs/seed-phase-confidence-model.md](docs/seed-phase-confidence-model.md)
- [docs/seed-phase-artifacts.md](docs/seed-phase-artifacts.md)
- [docs/cursor-pack-from-seed.md](docs/cursor-pack-from-seed.md) — optional **`cursor_operator_profile`** on `seed_intake.json` for Cursor rules preset intent

### Seed Phase validation

```bash
pip install -r scripts/requirements-seed-phase.txt
python3 scripts/validate-seed-phase.py users/demo/seed-phase
python3 scripts/generate-seed-dossier.py users/demo/seed-phase
```

Full instructions: [docs/seed-phase-validation.md](docs/seed-phase-validation.md).

### Change-review validation

Change-review artifacts live under **`users/<id>/review-queue/`** (queue + event log + `proposals/`, `decisions/`, `diffs/`).

```bash
pip install -r scripts/requirements-seed-phase.txt
python3 scripts/validate-change-review.py users/demo/review-queue
python3 scripts/validate-change-review.py users/_template/review-queue --allow-empty
```

Readable Markdown from a structured diff:

```bash
python3 scripts/generate-identity-diff.py users/demo/review-queue/diffs/diff-001.json --output users/demo/review-queue/identity_diff.md
```

Full instructions: [docs/change-review-validation.md](docs/change-review-validation.md).

**Student app:** Seed Phase (demo) at **[/seed-phase](http://localhost:3000/seed-phase)**; change-review demo bundle at **[/change-review](http://localhost:3000/change-review)** (`GET /api/change-review?profile=demo`) should read **`users/<profile>/review-queue/`** when the app is updated. See [readme-student-app.md](readme-student-app.md).

---

## Contents

- **docs/** — **Long-term objective** ([LONG-TERM-OBJECTIVE](docs/long-term-objective.md) — permanent system rule: democratize Alpha-style education; prevents intention drift). Concept, protocol, seed phase; education structure (self-skill-think, self-skill-write, self-skill-work); recursive self-learning objectives; business/white-paper insights; 6-week coding project; Alpha School reference (benchmarks, 2-hour screen-time target) in [skill-work-alpha-school submodule](docs/skill-work/skill-work-alpha-school/alpha-school-reference.md); no human guide assumed.
- **users/_template/** — Minimal scaffold (self, self-knowledge, self-identity, self-curiosity, self-personality, self-skill-think, self-skill-write, self-skill-work, self-evidence, recursion-gate, self-memory) for creating a new user directory in an instance repo; plus **`users/_template/seed-phase/`** — canonical **pre-activation** seed artifact placeholders (not the live Record); **`users/_template/review-queue/`** — empty change-review scaffold (validate with `--allow-empty`). No real data.
- **users/demo/** — Demo user for the student app; **`users/demo/seed-phase/`** — synthetic filled seed artifacts and dossier for validation and UI demos (not a live person). **`users/demo/review-queue/`** — synthetic post-seed change-review tree (queue, proposals, decisions, diffs) for validation and demos.
- **how-instances-consume-upgrades.md** — How an instance merges upgrades from this template without overwriting its Record.
- **[docs/system-tensions-and-mysteries.md](docs/system-tensions-and-mysteries.md)** — Canonical challenges and open mysteries the template carries; instances may add local annotations.
- **readme-student-app.md** — Student interface: how to run the app (clone, `cd app`, `npm install`, `npm start`; app at localhost:3000).
- **companion-self-and-grace-mar.code-workspace** — Recommended workspace: companion-self (writable) + grace-mar (read-only). Template work here; instance modifications only in a separate grace-mar workspace. See companion-self-bootstrap §7.
- **`.cursor/`** — Cursor **rules** and **skills** for **template contributors**: template vs `_template` vs `demo`, `users/` guard, generalizing from Grace-Mar (read-only); skills **companion-self-first-hour** (orient + optional demo validation / app) and **promote-from-grace-mar** (checklist + proposal). Say e.g. “run the first-hour skill” or “help me promote this from grace-mar” in chat.
