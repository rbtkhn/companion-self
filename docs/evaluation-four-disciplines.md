# Evaluation: Companion-Self Against the Four Disciplines

**Companion-Self template · Prompt craft, context engineering, intent engineering, specification engineering**

This document evaluates the companion-self template (and, where relevant, instance patterns) against the four disciplines of effective AI input: **prompt craft**, **context engineering**, **intent engineering**, and **specification engineering**. See [Evolving practice and recursive improvement](evolving-practice-recursive-improvement.md) for the framework and [Recursively improve](evolving-practice-recursive-improvement.md#reference) for how this ties to the WORK objective.

---

## 1. Prompt craft

**Definition:** Clear instructions, examples, guardrails, and output format for a single session. Synchronous, session-based.

### Current state

| Area | What exists | Assessment |
|------|-------------|------------|
| **Template pipeline** | Stage and edge are **rule-based** (no LLM). `stage.js` maps `skill_tag` → `mind_category`, `suggested_ix_section`; `edge.js` derives THINK/WRITE/WORK from Record. No prompts to tune. | N/A for prompt craft in the narrow sense; quality comes from schema and rules. |
| **Student UI** | Activity form: "What did you do?" with placeholder "e.g. We drew a dragon"; skill dropdown (THINK/WRITE/WORK). Review: Approve/Reject per candidate. | Minimal copy; no LLM-facing prompts. Adequate for human input. |
| **Instance: analyst** | When an instance adds an LLM analyst (e.g. Grace-Mar), [instance-patterns](instance-patterns.md) define an **analyst output contract**: required fields (mind_category, signal_type, summary, profile_target, suggested_entry, prompt_section, prompt_addition). | Contract is **output spec**, not a prompt template. Instances must supply their own analyst prompts; template doesn’t. |

### Gaps

- **No shared prompt templates** for the template itself (by design: no LLM in 6-week scope).
- **Analyst:** Instances that add an LLM analyst get a **output contract** but no canonical prompt (system + user) for "conversation → staged candidates." Prompt craft lives in the instance (e.g. Grace-Mar).
- **Future Voice / Co-pilot:** Any future in-repo Voice or co-pilot would need explicit prompt craft (system prompt, few-shot, guardrails). Not yet present.

### Summary

| Criterion | Status | Notes |
|-----------|--------|--------|
| Clear instructions | ✅ (for humans) / ⚪ (for LLM) | UI and API are clear; no LLM prompts in template. |
| Examples / few-shot | ⚪ | Not applicable in template; would apply to analyst or Voice. |
| Guardrails | ✅ (process) | Gate and merge rules are guardrails; no model-side guardrails. |
| Output format | ✅ | recursion-gate shape and analyst contract define format. |

**Verdict:** Prompt craft is **intentionally minimal** in the template (process over prompt). It becomes relevant for **instances** that add an analyst or Voice; the template supports that via contracts and schema, but does not supply prompts.

---

## 2. Context engineering

**Definition:** Curating and maintaining the optimal set of tokens/information an agent (or human) operates within—system prompts, tools, docs, memory, Record.

### Current state

| Area | What exists | Assessment |
|------|-------------|------------|
| **Record as context** | `record.js` **load()** reads `users/<id>/*.md` and builds a structured object: self, selfKnowledge, selfCuriosity, selfPersonality, selfSkillThink, selfSkillWrite, selfSkillWork, selfEvidence. Gate is loaded alongside. | **Strong.** Single function provides full Record + gate; any agent or UI can consume it. |
| **Document corpus** | `docs/` holds CONCEPT, schema-record-api, identity-fork-protocol, instance-patterns, project-6week-coding, recursive-self-learning-objectives, evolving-practice-recursive-improvement, etc. | **Strong.** Clear, cross-linked; suitable for "load into context" for an agent or developer. |
| **Template vs instance** | Template defines *what* context is (Record + gate); it does not define *how* to pack it into a context window (e.g. priority order, truncation, MCP). | Instances decide token budget and ordering. |
| **Memory** | Optional `self-memory.md` (ephemeral, rotation); template. Grace-Mar uses `self-archive.md`. | Lightweight; not a full "memory layer" for agents. |

### Gaps

- **No single "context pack" doc** that says: "To run an agent against this companion, load these files in this order with these roles (e.g. system vs. user)." Instances (or a future Cursor/agent rule) could derive that from schema + docs.
- **Retrieval / RAG:** Template does not prescribe retrieval over Record or docs; flat load is the model. For very large Records, instances would add retrieval.
- **MCP / tools:** Not in template scope; instances could expose Record or gate via MCP for agent tool use.

### Summary

| Criterion | Status | Notes |
|-----------|--------|--------|
| Curated information environment | ✅ | Record + docs are the environment. |
| Structured load API | ✅ | `load(repoRoot, userId)` returns record + recursionGate. |
| Clear boundaries | ✅ | Knowledge boundary (no LLM inference into Record); evidence linking. |
| Token/section guidance | ⚪ | No explicit "what to load first" or max tokens; instance-level. |

**Verdict:** Context engineering is **strong**. The Record and docs are the context; load() and the schema make them agent- and human-readable. The main improvement would be an optional **context-pack** guide (what to load, in what order) for instances that add LLM agents.

---

## 3. Intent engineering

**Definition:** Encoding organizational (and companion) purpose, goals, values, trade-off hierarchies, and decision boundaries so agents can act in alignment—what to want, not just what to know.

### Current state

| Area | What exists | Assessment |
|------|-------------|------------|
| **Sovereign merge rule** | "The agent may stage. It may not merge." ([Identity Fork Protocol](identity-fork-protocol.md)). Only the companion (or delegated human) may merge. | **Strong.** Single, unambiguous decision boundary. |
| **Long-term objectives** | [CONCEPT](concept.md) + [long-term-objective](long-term-objective.md): (1) Democratize Alpha-style education, (2) Companion sovereignty, (3) Knowledge boundary. | **Strong.** Permanent system rules; prevent intention drift. |
| **WORK intent** | `self-skill-work.md`: module intent, default objectives (six, including Recursively improve), work_goals, life_mission_ref. Schema enforces structure. | **Strong.** Goals and life mission are intent; objectives are trade-off/priority signals. |
| **Key invariants** | CONCEPT §6: Divergence by design; Merge not add; Agent may stage not merge; Identity beyond productivity; Augmentation not automation; Two-hour screen-time target. | **Strong.** Escalation and constraints are explicit (e.g. "human-in-the-loop is mandatory"). |
| **Gate semantics** | Process the gate = approve or reject **per candidate**; no batch merge. Review UI and merge.js enforce one-at-a-time. | **Strong.** Prevents "optimize for throughput" at the cost of sovereignty. |

### Gaps

- **Explicit "escalation" list** (when agent must stop and ask) is implied (anything that would require merge, or anything outside Record) but not a single checklist. Could be a short "Agent decision boundaries" section in Identity Fork or CONCEPT.
- **Trade-off hierarchy** (e.g. "prefer X over Y when both can’t be satisfied") is partly in objectives and two-hour target; not a dedicated matrix. Likely sufficient for template.

### Summary

| Criterion | Status | Notes |
|-----------|--------|--------|
| Purpose and goals encoded | ✅ | Long-term objectives, WORK goals, life mission. |
| Decision boundaries | ✅ | Stage vs merge; human-only merge; knowledge boundary. |
| Escalation vs autonomous | ✅ | Merge is always human; agent never merges. |
| Written, stable artifact | ✅ | CONCEPT, Identity Fork, schema, self-skill-work. |

**Verdict:** Intent engineering is **strong**. The protocol and docs encode what agents may do (stage) and must not do (merge, infer into Record), plus organizational goals (Alpha-style education, sovereignty, knowledge boundary). Optional improvement: one-page "Agent decision boundaries / escalation" for instances that add autonomous analysts.

---

## 4. Specification engineering

**Definition:** Writing documents that autonomous agents (and humans) can execute against over extended time horizons—complete, structured, internally consistent descriptions of outputs and quality, agent-readable corpus.

### Current state

| Area | What exists | Assessment |
|------|-------------|------------|
| **Schema and API** | [schema-record-api](schema-record-api.md): Record table, recursion-gate shape, edge shape, WORK objectives/tasks standard, field types and semantics. | **Strong.** Executable by code (record.js, merge.js) and readable by agents. |
| **CONCEPT** | [concept](concept.md): What a companion self is, Record vs Voice, education structure (THINK/WRITE/WORK), distillation, invariants, knowledge boundary. | **Strong.** Spec for "what the system is"; supports multi-session and instance work. |
| **6-week project** | [project-6week-coding](project-6week-coding.md): Scope, repo layout, week-by-week deliverables, API contracts, student UI. | **Strong.** Acceptance criteria and decomposition (weeks, endpoints). |
| **Instance patterns** | [instance-patterns](instance-patterns.md): Staging format, analyst output contract (required fields), session brief, conflict check. | **Strong.** Specs for instance extensions; analyst contract is machine-usable. |
| **Identity Fork** | Short form in template; full spec in Grace-Mar. Process-the-gate command, evidence linking, module table. | **Strong.** Clear enough for implementation and agent rules. |
| **Merge receipt** | merge.js writes merge-receipts.jsonl (candidate_id, raw_text, suggested_ix_section, merged_at). | **Strong.** Audit trail and eval artifact. |

### Gaps

- **Eval design:** No formal test cases or regression suite described in docs (e.g. "run these fixtures after schema or merge changes"). Merge receipts support auditing; adding a short "Evaluation and regression" note would align with the evaluation-design primitive.
- **Decomposition for agents:** Project is decomposed by weeks and endpoints; there is no explicit "break pattern" for a planner agent (e.g. "here is how to decompose a new feature into subtasks"). Optional for template; relevant if long-running coding agents are used.

### Summary

| Criterion | Status | Notes |
|-----------|--------|--------|
| Complete, structured descriptions | ✅ | Schema, CONCEPT, 6-week, instance-patterns. |
| Agent-readable | ✅ | Markdown + JSON; stable paths and field names. |
| Acceptance criteria | ✅ | Schema fields, API shapes, "process the gate" semantics. |
| Multi-session / long-horizon | ✅ | CONCEPT and schema don’t assume a single session. |
| Evaluation / regression | ⚪ | Receipts exist; no doc-level eval plan. |

**Verdict:** Specification engineering is **strong**. The doc corpus is structured, cross-referenced, and executable (code + agents). Main improvement: document **evaluation design** (e.g. fixture data, regression checks) and, optionally, **decomposition patterns** for agent-led work.

**Deeper dive:** [Evaluation: Specification discipline](evaluation-specification-discipline.md) — focused assessment of specification engineering only (artifact-by-artifact, primitives scorecard, gaps, recommendations).

---

## Overall summary

| Discipline | Verdict | Strength | Main gap |
|------------|---------|----------|----------|
| **Prompt craft** | Minimal by design | Process over prompt; contracts for output | No in-repo LLM prompts; instances own analyst/Voice prompts. |
| **Context engineering** | Strong | Record + load() + docs | Optional "context pack" guide for agents. |
| **Intent engineering** | Strong | Gate, CONCEPT, WORK, invariants | Optional one-page escalation/decision-boundaries. |
| **Specification engineering** | Strong | Schema, CONCEPT, 6-week, instance-patterns | Eval design doc; optional decomposition patterns. |

Companion-self is **strongest on context, intent, and specification** and **intentionally light on prompt craft** in the template. That aligns with the design: the lever is process (staging, gate, evidence, merge), not model or prompt tuning. For instances that add LLM analysts or Voice, the template already supports them via **context** (Record + docs), **intent** (may stage, may not merge), and **specs** (schema, analyst contract); the main addition would be explicit prompt-craft guidance or templates at the instance layer, and optional docs for context-pack, escalation, and eval design in the template.

---

## Actionable follow-up from the transcript

The transcript’s **primitives** (self-contained problem statements, acceptance criteria, constraint architecture, context pack, evaluation design) were turned into concrete changes. See **[Actionable insights from the transcript](actionable-insights-transcript.md)** for the mapping and links to:

- **Self-contained submissions** — [Ingestion and sources § Self-contained submissions](ingestion-and-sources.md#self-contained-submissions) + activity form placeholder.
- **Acceptance criteria** — [Schema § Acceptance criteria for staging and merge](schema-record-api.md#acceptance-criteria-for-staging-and-merge).
- **Constraint architecture / failure modes** — [Constraint architecture and failure modes](constraint-architecture-and-failure-modes.md).
- **Context pack** — [Context pack for agents](context-pack-for-agents.md).
- **Evaluation and regression** — [Evaluation design and regression](evaluation-design-and-regression.md) + `scripts/run-eval-fixtures.js`.
