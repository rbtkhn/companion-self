# Multi-agent parallelism

**Companion-Self template · Running multiple complex tasks on different agents at the same time**

The transcript (10x AI / post–Feb 2026) emphasizes running **multiple complex tasks on different agents in parallel**, with a shared specification so agents produce coherent output without stepping on each other. This doc defines how companion-self supports that: **agent lanes**, **coordination points**, **role-specific context**, and **planner–worker patterns**.

---

## 1. Why multi-agent parallelism

- **Throughput** — Multiple staging sources (conversation analyst, calendar webhook, quiz result, manual entry) can feed the gate at once; read-only work (edge, export, dashboard, session brief) can run alongside staging.
- **Separation of concerns** — Staging agents never write the Record; merge is human-gated and single-threaded; read-only agents never block writers.
- **Planner–worker** — A planner can decompose a large task (e.g. "add Voice," "onboard new user") and assign subtasks to worker agents; shared specs (schema, CONCEPT, project-6week) keep output coherent.

Companion-self’s **Identity Fork** (agent may stage, may not merge) and **single Record** already give clear write boundaries. This doc makes the parallelism model explicit so instances can run multiple agents safely.

---

## 2. Agent lanes (who may do what, in parallel with whom)

| Lane | Who | May run in parallel with | Writes to | Coordination |
|------|-----|---------------------------|-----------|---------------|
| **Staging** | Staging agents (analyst, webhooks, API, import scripts) | Each other; Read-only | **recursion-gate only** (append candidates) | Gate is shared; see §3. |
| **Read-only** | Edge, export, dashboard, session brief, Voice (read), any reader | Each other; Staging | **Nothing** (read Record + gate) | None; read is safe in parallel. |
| **Merge** | Human (or single merge executor after human approve) | **No one** while merging | **Record** (self-evidence, dimension files, gate update, receipts) | Exclusive: one merge at a time; human-gated. |
| **Codebase / docs** (optional) | Dev agents (e.g. Cursor, coding workers) | Each other **by scope** (different dirs/features) | **app/, docs/, scripts/** | Scope per agent; see §5. |

**Summary:**

- **Staging** and **Read-only** can run in parallel with each other and with multiple agents in the same lane.
- **Merge** is exclusive and human-gated.
- **Codebase** parallelism is by scope (module or feature) so two agents don’t edit the same file.

---

## 3. Coordination points

### 3.1 Recursion gate (staging)

- **Role:** Single shared queue of candidates. All staging agents **append**; no agent removes (merge does that on approve/reject).
- **Concurrency:** Multiple staging agents may produce candidates at the same time. The gate file (`recursion-gate.json`) is one JSON array; **writes must be serialized** to avoid lost updates (e.g. two agents load, each appends, each saves → last save wins and one candidate is lost).
- **Instance responsibility:** Instances that run multiple staging agents must ensure **one writer at a time** to the gate, for example:
  - **Single staging API** — All agents call one POST `/api/activity` (or equivalent); the server serializes requests and does load → push → save per request.
  - **Queue** — Agents push to a queue (e.g. Redis, in-memory); a single worker reads the queue and appends to the gate.
  - **Lock** — Before load/push/save, acquire a lock (file or distributed); release after save.
- **Candidate IDs:** Each candidate has a unique `id` (e.g. `cand-<timestamp>-<random>`). Multiple agents must not reuse IDs; the template’s `createCandidate` generates unique IDs per call.

### 3.2 Record (identity + evidence)

- **Role:** Single source of truth for the companion. Only the **merge** path writes to Record files (self-evidence, self-knowledge, self-curiosity, self-personality, etc.).
- **Concurrency:** Merge is **exclusive**: one approve at a time; no parallel merge. Read-only agents may read Record at any time (during or between merges).
- **No staging agent** may write to Record; Identity Fork is strict.

### 3.3 Shared specification

- **Role:** All agents (staging, read-only, planner, workers) share the same **specs** (schema, CONCEPT, Identity Fork, constraints) so outputs are coherent and consistent.
- **Context pack per role:** §4 below gives a minimal load order per lane so each agent has the right context without overload.

---

## 4. Context pack per role (what to load when)

So that multiple agents can run in parallel without conflicting, each **role** should load only what it needs. Order within each list: constraints first, then schema, then task-specific docs.

| Role | Load (in order) | Purpose |
|------|------------------|---------|
| **Staging agent** | Identity Fork → Constraint architecture and failure modes → Schema (Record + recursion-gate shape) → Ingestion and sources (§ Self-contained submissions) → Record for user X (if needed to suggest dimension) | Stage candidates that conform to the contract; never merge; self-contained raw_text. |
| **Read-only agent** (edge, export, dashboard) | Schema (Record, edge shape) → CONCEPT (§ education structure, WORK + IX-C) → Record for user X | Derive edge, build export, or render dashboard; no writes. |
| **Merge executor** (human or single process) | Identity Fork → Schema (acceptance criteria, merge outcome) → Constraint architecture → Record + gate | Run approve/reject; write Record and receipts; exclusive. |
| **Planner / dev agent** | Context pack (full order) → Project 6-week → Instance patterns (if extending) | Decompose work; assign subtasks; keep outputs aligned with schema and CONCEPT. |

Full load order for a generic or planner agent remains [Context pack for agents](context-pack-for-agents.md). The table above is a **subset per role** so parallel agents don’t all load the same large context when they only need a slice.

---

## 5. Planner–worker pattern (complex tasks across agents)

The transcript’s **planner–worker** model: a capable model plans the work, decomposes into subtasks, defines acceptance criteria, and assigns work to (possibly cheaper/faster) worker agents. Companion-self supports this in two ways.

### 5.1 Pipeline / product work (staging, edge, export)

- **Planner:** Produces a plan (e.g. “Process three sources: conversation, calendar, manual; then run edge and export.”).
- **Workers:** One agent (or process) per source stages to the gate; another computes edge; another builds export. They run in parallel where possible (staging and read-only).
- **Shared spec:** Schema, Identity Fork, and [Constraint architecture](constraint-architecture-and-failure-modes.md) ensure workers don’t merge, don’t infer into Record, and produce valid candidates.
- **Handoff:** Gate is the handoff: staging workers write candidates; merge (human) consumes; read-only workers read Record + gate.

### 5.2 Codebase / feature work (app, docs)

- **Planner:** Decomposes a feature (e.g. “Add Voice”) into subtasks (schema extension, API endpoint, prompt design, UI).
- **Workers:** Each worker owns a **scope** (e.g. `app/schema/`, `app/server.js`, `docs/`, `app/public/`) or a **feature slice** (e.g. “you own export API,” “you own review UI”). Specification is the handoff: [Schema and API contract](schema-record-api.md), [Project 6-week](project-6week-coding.md), [CONCEPT](concept.md).
- **Coordination:** Workers don’t edit the same file in the same sprint; planner assigns non-overlapping scope. Acceptance criteria (from schema and project-6week) let each worker verify “done” without asking.

Instances that use coding agents in parallel should define **scope per agent** (by directory, module, or feature) and point agents at the same specs so outputs integrate.

**Concrete example:** [Two parallel tasks for separate Cursor conversations](tasks-parallel-cursor-conversations.md) — Task 1: schema + docs (record.js, schema-record-api, project-6week). Task 2: student UI accessibility (app/public). Zero file overlap; ~15–30 min each.

---

## 6. Instance implementation notes

| Need | Suggestion |
|------|------------|
| **Multiple staging agents** | Route all staging through one API or queue; single process appends to `recursion-gate.json`. Or use a lock around load → push → save. |
| **Multiple read-only consumers** | No coordination needed; read Record and gate anytime. |
| **Merge** | Keep merge single-threaded and human-gated; one approve/reject at a time. |
| **Planner + workers** | Give planner full [Context pack](context-pack-for-agents.md); give each worker the role-specific pack (§4) and a clear scope (e.g. “you own staging API,” “you own edge derivation”). |
| **Regression** | After changing schema or pipeline, run [Evaluation design and regression](evaluation-design-and-regression.md) (`node scripts/run-eval-fixtures.js`) so multi-agent behavior still matches acceptance criteria. |

---

## 7. Cross-references

- [Identity Fork Protocol](identity-fork-protocol.md) — Agent may stage, may not merge.
- [Constraint architecture and failure modes](constraint-architecture-and-failure-modes.md) — What staging and merge must not do.
- [Context pack for agents](context-pack-for-agents.md) — Full load order; §4 above is role-specific subset.
- [Ingestion and sources](ingestion-and-sources.md) — Many sources → one gate → one Record.
- [Schema and API contract](schema-record-api.md) — Record and gate shape; acceptance criteria.
- [Evolving practice and recursive improvement](evolving-practice-recursive-improvement.md) — Four disciplines; specification as scaffolding for coherent multi-agent output.
