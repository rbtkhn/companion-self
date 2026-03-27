# companion-self

**Companion-Self** is the **template** repo. **Grace-Mar** is the **instance** repo (the first and currently only instance).

A new companion self is created **only when a new user completes seed phase** — not by copying another repo's `users/` or pre-filling a Record. **Seed Phase v2** is a visible artifact pipeline with JSON Schemas, confidence signals, and **readiness gating** before activation ([docs/seed-phase.md](docs/seed-phase.md)).

## Governed change

Companion-Self does not treat meaningful post-seed revision as silent memory drift.

When new evidence materially affects identity, curiosity, pedagogy, expression, memory governance, safety rules, or other durable operating commitments, the change should enter a change-review pipeline that preserves prior state, supporting evidence, contradiction type, confidence delta when available, and an explicit decision before governed state is updated.

See:
- [docs/change-review.md](docs/change-review.md)
- [docs/contradiction-policy.md](docs/contradiction-policy.md)
- [docs/change-types.md](docs/change-types.md)
- [docs/change-review-lifecycle.md](docs/change-review-lifecycle.md)

- **Template (this repo):** Concept, protocol, seed-phase definition, and structure for creating a new companion self. No one's Record; no pilot data.
- **Instance (e.g. [Grace-Mar](https://github.com/rbtkhn/grace-mar)):** One live companion self — Record, bot, pipeline. Created from the template when a new user completes seed phase.

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

### Seed Phase validation

```bash
pip install -r scripts/requirements-seed-phase.txt
python3 scripts/validate-seed-phase.py users/demo/seed-phase
python3 scripts/generate-seed-dossier.py users/demo/seed-phase
```

Full instructions: [docs/seed-phase-validation.md](docs/seed-phase-validation.md).

### Change-review validation (demo)

```bash
pip install -r scripts/requirements-seed-phase.txt
python3 scripts/validate-change-review.py users/demo/change-review
```

**Student app:** Seed Phase status (demo data) is visible at **[/seed-phase](http://localhost:3000/seed-phase)** when running the app. See [readme-student-app.md](readme-student-app.md).

---

## Contents

- **docs/** — **Long-term objective** ([LONG-TERM-OBJECTIVE](docs/long-term-objective.md) — permanent system rule: democratize Alpha-style education; prevents intention drift). Concept, protocol, seed phase; education structure (self-skill-think, self-skill-write, self-skill-work); recursive self-learning objectives; business/white-paper insights; 6-week coding project; Alpha School reference (benchmarks, 2-hour screen-time target) in [skill-work-alpha-school submodule](docs/skill-work/skill-work-alpha-school/alpha-school-reference.md); no human guide assumed.
- **users/_template/** — Minimal scaffold (self, self-knowledge, self-identity, self-curiosity, self-personality, self-skill-think, self-skill-write, self-skill-work, self-evidence, recursion-gate, self-memory) for creating a new user directory in an instance repo; plus **`users/_template/seed-phase/`** — canonical **pre-activation** seed artifact placeholders (not the live Record). No real data.
- **users/demo/** — Demo user for the student app; **`users/demo/seed-phase/`** — synthetic filled seed artifacts and dossier for validation and UI demos (not a live person). **`users/demo/change-review/`** — synthetic change-review JSON for schema validation (post-seed governance demos).
- **how-instances-consume-upgrades.md** — How an instance merges upgrades from this template without overwriting its Record.
- **[docs/system-tensions-and-mysteries.md](docs/system-tensions-and-mysteries.md)** — Canonical challenges and open mysteries the template carries; instances may add local annotations.
- **readme-student-app.md** — Student interface: how to run the app (clone, `cd app`, `npm install`, `npm start`; app at localhost:3000).
- **companion-self-and-grace-mar.code-workspace** — Recommended workspace: companion-self (writable) + grace-mar (read-only). Template work here; instance modifications only in a separate grace-mar workspace. See companion-self-bootstrap §7.
