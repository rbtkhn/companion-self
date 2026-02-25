# companion-self

**Companion-Self** is the **template** repo. **Grace-Mar** is the **instance** repo (the first and currently only instance).

A new companion self is created **only when a new user completes seed phase** — not by copying another repo's `users/` or pre-filling a Record.

- **Template (this repo):** Concept, protocol, seed-phase definition, and structure for creating a new companion self. No one's Record; no pilot data.
- **Instance (e.g. [Grace-Mar](https://github.com/rbtkhn/grace-mar)):** One live companion self — Record, bot, pipeline. Created from the template when a new user completes seed phase.

**Reference implementation:** [Grace-Mar](https://github.com/rbtkhn/grace-mar) — [grace-mar.com](https://grace-mar.com) (profile, bot, PRP).

Optional: [companion-self.com](https://companion-self.com) when the concept site exists.

---

## Contents

- **docs/** — **Long-term objective** ([LONG-TERM-OBJECTIVE](docs/LONG-TERM-OBJECTIVE.md) — permanent system rule: democratize Alpha-style education, 90% value at 10% cost; prevents intention drift). Concept, protocol, seed phase; education structure (self-skill-read, self-skill-write, self-skill-build); recursive self-learning objectives; business/white-paper insights; 3-year roadmap; 6-week coding project; two-hour screen-time target; Alpha School benchmarks; no human guide assumed.
- **users/_template/** — Minimal scaffold (SELF, SKILLS, EVIDENCE, PENDING-REVIEW, MEMORY) for creating a new user directory in an instance repo. No real data.
- **HOW-INSTANCES-CONSUME-UPGRADES.md** — How an instance merges upgrades from this template without overwriting its Record.
- **companion-self-and-grace-mar.code-workspace** — Recommended workspace: companion-self (writable) + grace-mar (read-only). Template work here; instance modifications only in a separate grace-mar workspace. See COMPANION-SELF-BOOTSTRAP §7.
