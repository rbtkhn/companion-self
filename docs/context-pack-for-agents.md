# Context pack for agents

**Companion-Self template · What to load, in what order, when working as an agent (or human) against this repo**

**Transcript idea:** Agents that start each session with the right project files, conventions, and constraints already loaded perform better. This doc is the **context pack**: what to load and in what order when you are an AI agent (e.g. Cursor, Claude Code, or an instance’s analyst) or a human onboarding to the codebase.

**Multiple agents in parallel:** When running several agents at once (e.g. one staging, one read-only, one planner), use **role-specific** load orders so each agent gets only what it needs. See [Multi-agent parallelism](multi-agent-parallelism.md) §4 Context pack per role.

---

## Load order (recommended)

Load these in order so constraints and intent come before detail. Instances may extend (e.g. add instance-specific rules or MCP tool definitions).

| Order | Document | Role |
|-------|----------|------|
| 1 | [Identity Fork Protocol](identity-fork-protocol.md) | Constraints: agent may stage, may not merge; evidence linking; process-the-gate. |
| 2 | [Constraint architecture and failure modes](constraint-architecture-and-failure-modes.md) | What we must prevent (batch merge, inference into Record, etc.). |
| 3 | [Schema and API contract](schema-record-api.md) | Record shape, recursion-gate shape, acceptance criteria, edge shape, WORK objectives/tasks. |
| 4 | [CONCEPT](concept.md) | What a companion self is; Record vs Voice; education structure (THINK/WRITE/WORK); invariants; knowledge boundary. |
| 5 | [Long-term objectives](long-term-objective.md) | Permanent system rules: Alpha-style education, sovereignty, knowledge boundary. |
| 6 | **Record for user X** | For a specific companion: `load(repoRoot, userId)` or read `users/<id>/*.md` + `recursion-gate.json`. |

**Optional depending on task:**

- [Instance patterns](instance-patterns.md) — If extending with analyst, Voice, or different staging format.
- [Ingestion and sources](ingestion-and-sources.md) — Self-contained submissions; triggers; many sources → one Record.
- [Project 6-week coding](project-6week-coding.md) — Repo layout, app structure, API endpoints.
- [Evaluation design and regression](evaluation-design-and-regression.md) — How to run fixtures and regression after changes.

---

## Code entry points

- **Load Record + gate:** `app/schema/record.js` → `load(repoRoot, userId)`.
- **Stage activity:** `app/pipeline/stage.js` → `stageActivity({ text, skill_tag })`.
- **Review (approve/reject):** `app/pipeline/merge.js` → `reviewCandidate({ candidate_id, action })`.
- **Edge:** `app/pipeline/edge.js` → `deriveEdge(data)` or `getEdge()`.

---

## Token / scope note

For large Records or long docs, instances may use retrieval (e.g. RAG) instead of loading everything. The template assumes flat load; the **order** above still applies to what is retrieved first (constraints and schema before Record content).
