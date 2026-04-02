# Work modules — territory history logs

**Design principle:** Each **work** territory (`work-*`) may carry a single **append-only operator log** — significant sessions, ingest milestones, ship notes, and pointers to commits or artifacts **scoped to that lane**. **New lane scaffold:** [work-template.md](work-template.md).

| Convention | Meaning |
|------------|---------|
| **Filename** | `work-<territory>-history.md` (e.g. `work-dev-history.md`) |
| **Location** | `docs/skill-work/<territory>/` alongside that territory’s README and `*-sources.md` (if present) |
| **Content** | Dated sections under **Log**; short bullets; optional SHAs and paths |
| **Not** | Record truth, Voice knowledge, or automatic pipeline output. **Not** a substitute for `users/[id]/session-log.md` or RECURSION-GATE. |

**Fence:** History files document **what the operator did or noted in this lane** — not what is canonically true.

**Relation to cadence:** Instances that use **`coffee`** / **`dream`** / **`bridge`** may append per-run lines under `work-cadence/work-cadence-events.md` (telemetry) while **design** changes to those rituals live in cadence docs or a `work-*-history.md` when you split cadence design from events.

**Existing logs (this template repo):**

| Territory | File |
|-----------|------|
| work-cadence | [work-cadence/work-cadence-events.md](work-cadence/work-cadence-events.md) *(per-run telemetry)* |

_Add rows here when new `work-*` territories gain a `work-*-history.md`._

**Cross-reference:** Authorized sources lists — [work-modules-sources-principle.md](work-modules-sources-principle.md).

**Optional downstream rollup:** A forked instance may maintain **`users/[id]/self-history.md`** as a derived rollup — not Record; see instance **AGENTS.md** and canonical-paths when present.
