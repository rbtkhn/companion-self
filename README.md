# companion-self

**Companion-Self** is the **template** repo. **Grace-Mar** is the **instance** repo (the first and currently only instance).

**Release + compatibility metadata:** [`template-version.json`](template-version.json) — semver, release date, git tag, and `compatibilityContract` pointers (single source; no separate `template-contract.json`).

**Companion-Self** is a general-purpose system for companion formation, activation, memory governance, and post-seed revision. Education, coaching, personal knowledge work, and guided interaction are downstream use cases, not the category definition.

A new companion self is created **only when a new user completes seed phase** — not by copying another repo's `users/` or pre-filling a Record. **Seed Phase v2** is a visible artifact pipeline with JSON Schemas, confidence signals, and **readiness gating** before activation ([docs/seed-phase.md](docs/seed-phase.md)).

Companion-Self now treats major post-seed self-revision as governed change, not silent Record drift.

## North star: hand off the template for new instances

**Product goal:** Make it **easy for new people** to take **this repo**, run **seed phase**, and spin up **their own** companion instance—same **governance and structure**, **their** Record and Voice, **not** a copy of another family’s live fork.

- **This repository** is the **portable constitution**: concept, protocol, seed-phase definitions, `users/_template/` scaffolds, validators, `docs/skill-work/` patterns, and upgrade contracts. It does **not** contain a real companion’s merged identity data.
- **A new companion self** is created **only** when a **new user completes seed phase** ([docs/seed-phase.md](docs/seed-phase.md))—not by duplicating someone else’s `users/<id>/`.
- **After you fork:** use [how-instances-consume-upgrades.md](how-instances-consume-upgrades.md) to pull template improvements safely; [docs/template-instance-contract.md](docs/template-instance-contract.md) and [docs/instance-patterns.md](docs/instance-patterns.md) spell out compatibility and reference patterns.

**First reference instance:** [Grace-Mar](https://github.com/rbtkhn/grace-mar) (fully lived example to compare against, not something to paste into your Record).

## Governed change

Companion-Self does not treat meaningful post-seed revision as silent memory drift.

When new evidence materially affects identity, curiosity, pedagogy, expression, memory governance, safety rules, or other durable operating commitments, the change should enter a change-review pipeline that preserves prior state, supporting evidence, contradiction type, confidence delta when available, and an explicit decision before governed state is updated.

See:
- [docs/change-review.md](docs/change-review.md)
- [docs/contradiction-policy.md](docs/contradiction-policy.md)
- [docs/change-types.md](docs/change-types.md)
- [docs/change-review-lifecycle.md](docs/change-review-lifecycle.md)

## Governed lifecycle

Companion-Self uses a two-part governance model:

- **Seed Phase** forms the initial companion before activation.
- **Change review** governs materially important post-seed revision after activation.

The project does not treat meaningful change as silent memory accumulation or silent overwrite. When new evidence materially affects identity, pedagogy, memory governance, safety, or other durable commitments, the change should become a visible review object before governed state is updated. That positioning is not just persistent memory, but a governed lifecycle. Doctrine links for change review are under **Governed change** above; formation and readiness are in [docs/seed-phase.md](docs/seed-phase.md), [docs/seed-phase-readiness.md](docs/seed-phase-readiness.md), [how-instances-consume-upgrades.md](how-instances-consume-upgrades.md) (template upgrade collisions), and [docs/instance-patterns.md](docs/instance-patterns.md).

- **Template (this repo):** Concept, protocol, seed-phase definition, and structure for creating a new companion self. No one's Record; no pilot data.
- **Instance (e.g. [Grace-Mar](https://github.com/rbtkhn/grace-mar)):** One live companion self — Record, bot, pipeline. Created from the template when a new user completes seed phase.
- **Compatibility:** Canonical template/instance rules — [docs/template-instance-contract.md](docs/template-instance-contract.md).

## State model

Companion-Self distinguishes **three layers** of system state:

- **Evidence Layer** — raw source material  
- **Prepared Context Layer** — normalized or staged material for agent use  
- **Governed State Layer** — durable companion state (Record, approved seed outputs, change-review outcomes)  

See [docs/state-model.md](docs/state-model.md), [docs/evidence-layer.md](docs/evidence-layer.md), [docs/prepared-context-layer.md](docs/prepared-context-layer.md), [docs/governed-state-layer.md](docs/governed-state-layer.md).

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

**Companion app:** Seed Phase (demo) at **[/seed-phase](http://localhost:3000/seed-phase)**; change-review demo at **[/change-review](http://localhost:3000/change-review)** via **`GET /api/change-review?profile=demo`** (reads **`users/<profile>/review-queue/`**). See [readme-app.md](readme-app.md).

---

## Contents

- **docs/** — **Long-term objective** ([LONG-TERM-OBJECTIVE](docs/long-term-objective.md) — permanent system rule: democratize Alpha-style education; prevents intention drift). Concept, protocol, seed phase; education structure (self-skill-think, self-skill-write, self-skill-work); recursive self-learning objectives; business/white-paper insights; 6-week coding project; Alpha School reference (benchmarks, 2-hour screen-time target) in [skill-work-alpha-school submodule](docs/skill-work/skill-work-alpha-school/alpha-school-reference.md); no human guide assumed.
- **users/_template/** — Minimal scaffold (self, self-knowledge, self-identity, self-curiosity, self-personality, self-skill-think, self-skill-write, self-skill-work, self-evidence, work-dev, work-business, recursion-gate, self-memory) for creating a new user directory in an instance repo; plus **`users/_template/seed-phase/`** — canonical **pre-activation** seed artifact placeholders (not the live Record); **`users/_template/review-queue/`** — empty change-review scaffold (validate with `--allow-empty`). No real data.
  - **`work-dev.md`** starts blank; filled only from seed survey / explicit input / governed updates (see `seed-phase/work_dev_seed.json`). **Not** the same as **`docs/skill-work/work-dev/`** (operator integration territory). Distinct from **`self-skill-work`** (capability claims).
  - **`work-business.md`** starts blank; it is filled only from seed survey / explicit input / governed updates (see `seed-phase/work_business_seed.json`). It is **not** the same as **`docs/skill-work/work-business/`** (operator research territory). Distinct from **`self-skill-work`** (capability claims).
- **users/demo/** — Demo user for the companion app; **`users/demo/seed-phase/`** — synthetic filled seed artifacts and dossier for validation and UI demos (not a live person). **`users/demo/review-queue/`** — synthetic post-seed change-review tree (queue, proposals, decisions, diffs) for validation and demos.
- **how-instances-consume-upgrades.md** — How an instance merges upgrades from this template without overwriting its Record.
- **[docs/system-tensions-and-mysteries.md](docs/system-tensions-and-mysteries.md)** — Canonical challenges and open mysteries the template carries; instances may add local annotations.
- **readme-app.md** — Companion app / local demo: how to run (clone, `cd app`, `npm install`, `npm start`; localhost:3000). [readme-student-app.md](readme-student-app.md) is a legacy pointer to the same doc.
- **companion-self-and-grace-mar.code-workspace** — Recommended workspace: companion-self (writable) + grace-mar (read-only). Template work here; instance modifications only in a separate grace-mar workspace. See companion-self-bootstrap §7.
- **`.cursor/`** — Cursor **rules** and **skills** for **template contributors**: template vs `_template` vs `demo`, `users/` guard, generalizing from Grace-Mar (read-only); skills **companion-self-first-hour** (orient + optional demo validation / app) and **promote-from-grace-mar** (checklist + proposal). Say e.g. “run the first-hour skill” or “help me promote this from grace-mar” in chat.
