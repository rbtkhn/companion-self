# Evaluation: Specification discipline

**Companion-Self template · Focused assessment of specification engineering**

This document evaluates companion-self **only** on the **specification engineering** discipline: writing documents that autonomous agents (and humans) can execute against over extended time horizons—complete, structured, internally consistent descriptions of outputs and quality, with an agent-readable corpus. For the four-disciplines overview, see [Evaluation: Companion-Self against the four disciplines](evaluation-four-disciplines.md).

---

## 1. Definition and scope

**Specification engineering** (from the transcript and [evolving-practice](evolving-practice-recursive-improvement.md)):

- **What it is:** Documents that define *what an output should be* for a given task so that a capable system can execute against them without real-time human intervention.
- **At org level:** The whole document corpus is treated as agent-fungible: everything written is something an agent can read and act on.
- **Primitives that support it:** Self-contained problem statements, acceptance criteria, constraint architecture, decomposition, evaluation design.

**In scope for this evaluation:**

- All docs and code that function as *specs* (schema, API contract, CONCEPT, project plan, instance contracts, acceptance criteria, constraints, eval design).
- Alignment between specs and code (single source of truth, no silent drift).
- Gaps and concrete improvements.

---

## 2. Evaluation framework

We assess specification discipline along six dimensions:

| Dimension | Question | Source |
|-----------|----------|--------|
| **Completeness** | Is the spec sufficient for an independent executor (human or agent) to produce or verify the outcome without asking? | Transcript: self-contained problem statements, acceptance criteria. |
| **Structure** | Are specs organized (sections, tables, field lists) and cross-referenced so that the right information is findable? | Specification engineering as “structured, internally consistent.” |
| **Consistency** | Do specs agree with each other and with code? Are terms and shapes stable across docs and implementation? | Internal consistency; agent-readable. |
| **Agent-readability** | Can an agent parse and use the spec (stable paths, field names, formats, explicit “done” and “must not”)? | Transcript: “agent-fungible” corpus. |
| **Decomposition** | Are large outcomes broken into verifiable, independently executable pieces with clear inputs/outputs? | Transcript: decomposition primitive; 6-week project. |
| **Evaluation design** | Is there a defined way to prove the output is good (test cases, regression, receipts)? | Transcript: eval design primitive. |

---

## 3. Artifact-by-artifact assessment

### 3.1 Schema and API contract (`docs/schema-record-api.md`)

| Dimension | Assessment | Evidence |
|-----------|------------|----------|
| Completeness | **Strong** | Record table (all components, files, fields); recursion-gate shape (every field typed and described); WORK objectives and tasks standard (module_intent, default_objectives, work_goals, life_mission_ref, task fields); edge response shape. Single doc for “what the data looks like” and “what the API returns.” |
| Structure | **Strong** | Tables for Record, objectives, tasks, gate, edge; code blocks for markdown examples; cross-links to CONCEPT, Identity Fork, project-6week. |
| Consistency | **Strong** | Field names and enums (THINK/WRITE/WORK, IX-A/IX-B/IX-C) match `record.js` and pipeline. Minor: JSDoc in record.js still references `selfSkillRead` in typedef while runtime uses `selfSkillThink`; doc says THINK everywhere. |
| Agent-readability | **Strong** | Stable paths (`users/<id>/*.md`, `recursion-gate.json`), stable field names, allowed value sets. An agent can generate or validate payloads from this doc alone. |
| Decomposition | **N/A** | Schema describes structure, not task breakdown. Decomposition lives in project-6week. |
| Evaluation design | **Strong** | Acceptance criteria for staging and merge are in this doc (verifiable by independent observer); linked to evaluation-design-and-regression. |

**Verdict:** Core specification artifact. Complete, structured, and executable. Acceptance criteria section makes “done” verifiable.

---

### 3.2 CONCEPT (`docs/concept.md`)

| Dimension | Assessment | Evidence |
|-----------|------------|----------|
| Completeness | **Strong** | What a companion self is; Record vs Voice; education structure (THINK/WRITE/WORK); distillation (THINK → IX-A/B/C); skill flow; WORK + IX-C; invariants (§6); knowledge boundary (§5); APIs and integrations. Enough for an implementer or agent to understand “what the system is” and what must hold. |
| Structure | **Strong** | Numbered sections; tables (cognitive fork, structure, distillation, skill flow); cross-refs to long-term-objective, identity-fork, schema, two-hour target, ingestion. |
| Consistency | **Strong** | Terminology (Record, Voice, IX-A/B/C, THINK/WRITE/WORK) aligned with schema and Identity Fork. |
| Agent-readability | **Strong** | Prose is clear; section headers and tables are parseable; “must” and “must not” (e.g. no LLM inference, agent may stage may not merge) are explicit. |
| Decomposition | **Partial** | CONCEPT explains *what* (identity, instruments, flow) not *how to build in steps*. Decomposition is in project-6week. |
| Evaluation design | **N/A** | CONCEPT does not define test or regression; that’s in evaluation-design-and-regression. |

**Verdict:** Authoritative spec for “what the system is.” Supports long-horizon and multi-session work; no assumption of a single chat or session.

---

### 3.3 Project 6-week coding (`docs/project-6week-coding.md`)

| Dimension | Assessment | Evidence |
|-----------|------------|----------|
| Completeness | **Strong** | Scope (in/out); repo layout; week-by-week goals; tasks per week with deliverables; API contracts (POST activity, GET recursion-gate, review, record, edge, export); success criteria per week. |
| Structure | **Strong** | Weeks 1–6; tables (tasks, deliverables); code block for repo tree; explicit “Success” and “Prerequisite.” |
| Consistency | **Strong** | Endpoints and shapes match server.js and schema; week numbering and deliverables match current app layout. |
| Agent-readability | **Strong** | Task IDs (1.1, 1.2, …); deliverable paths; API body/response described. A planner or coding agent can treat this as a checklist. |
| Decomposition | **Strong** | Work decomposed into weeks and per-week tasks; each task has a deliverable; clear input/output (e.g. “POST endpoint,” “Load/save in schema”). Fits transcript idea: “subtasks that each take less than 2 hours… clear input output boundaries.” |
| Evaluation design | **Partial** | Success criteria are narrative (“Running load… returns a Record object”). No pointer to run-eval-fixtures in the 6-week doc; evaluation-design-and-regression doc and script exist separately. Adding “Run `node scripts/run-eval-fixtures.js` after schema/pipeline changes” to project-6week would close the loop. |

**Verdict:** Primary decomposition spec. Strong for implementation and verification per week; could explicitly reference the regression script.

---

### 3.4 Instance patterns (`docs/instance-patterns.md`)

| Dimension | Assessment | Evidence |
|-----------|------------|----------|
| Completeness | **Strong** | Staging format (recursion-gate.json vs pending-review.md); analyst output contract (required fields listed); session brief; conflict check; design principle (analyst stages, companion gates). |
| Structure | **Strong** | Tables (template vs Grace-Mar, analyst fields); clear sectioning. |
| Consistency | **Strong** | Analyst field names (mind_category, profile_target, suggested_entry, etc.) form a contract; merge logic in template consumes recursion-gate shape; Grace-Mar uses extended format. |
| Agent-readability | **Strong** | Analyst contract is machine-usable: an LLM or adapter can emit YAML/JSON that conforms to the table. |
| Decomposition | **Partial** | Describes *what* instances can do and *what* analyst must output; “how to add an analyst” (steps) could be a short decomposition (e.g. in context-pack or a future “Adding an analyst” section). |
| Evaluation design | **N/A** | No test cases for analyst output; instances would define their own. |

**Verdict:** Spec for instance extensions and analyst output. Contract is complete and agent-readable; decomposition for “add analyst” is optional.

---

### 3.5 Identity Fork Protocol (`docs/identity-fork-protocol.md`)

| Dimension | Assessment | Evidence |
|-----------|------------|----------|
| Completeness | **Strong** | Sovereign merge rule; stages (Detect, Stage, Review, Merge); process-the-gate command; evidence linking; identity schema (module table); knowledge boundary. Short form; full spec in Grace-Mar. |
| Structure | **Strong** | Numbered stages; table (modules, files, purpose); blockquote for the rule. |
| Consistency | **Strong** | Aligned with CONCEPT and schema; “agent may stage, may not merge” repeated. |
| Agent-readability | **Strong** | Command phrase (“Process the gate”) and rule are explicit; module table gives file ↔ purpose. |
| Decomposition | **N/A** | Protocol is constraints and flow, not task breakdown. |
| Evaluation design | **N/A** | Receipts and evidence support auditing; eval design is in evaluation-design-and-regression. |

**Verdict:** Constraint and process spec. Clear and executable for agents (e.g. “do not merge” encoded in behavior).

---

### 3.6 Constraint architecture and failure modes (`docs/constraint-architecture-and-failure-modes.md`)

| Dimension | Assessment | Evidence |
|-----------|------------|----------|
| Completeness | **Strong** | Four categories (must / must not / prefer / escalate); table of failure modes with “why wrong” and “how we prevent”; analyst-prompt examples. |
| Structure | **Strong** | Table for categories; table for failure modes; bullet list for analyst prompts. |
| Consistency | **Strong** | Mirrors Identity Fork and CONCEPT; no new contradictions. |
| Agent-readability | **Strong** | “Must not” and “escalate” are explicit; an agent or prompt engineer can copy constraints into system prompts. |
| Decomposition | **N/A** | Not a task spec. |
| Evaluation design | **N/A** | Failure modes inform what to test (e.g. “no batch merge”); actual tests are in run-eval-fixtures and evaluation-design doc. |

**Verdict:** Specification of constraints and failure modes. Directly supports specification discipline by making “wrong” outcomes specifiable and preventable.

---

### 3.7 Evaluation design and regression (`docs/evaluation-design-and-regression.md`)

| Dimension | Assessment | Evidence |
|-----------|------------|----------|
| Completeness | **Strong** | Purpose (regression, acceptance); fixture user; test cases table (input, expected after stage, expected after approve/reject); how to run; when to run; how to add/change fixtures. |
| Structure | **Strong** | Sections and table; command and exit semantics. |
| Consistency | **Strong** | Fixtures align with schema and acceptance criteria; script path and behavior match doc. |
| Agent-readability | **Strong** | A human or CI agent can run the script and interpret exit code; test cases are named and described. |
| Decomposition | **Partial** | Script is one “task”; adding fixtures is described in prose. Fine for current scope. |
| Evaluation design | **Strong** | This doc *is* the evaluation design: test cases, known-good outputs, periodic run (after schema/pipeline changes). Implements the transcript primitive. |

**Verdict:** Spec for “how we know the output is good.” Completes the specification stack with executable regression.

---

### 3.8 Context pack for agents (`docs/context-pack-for-agents.md`)

| Dimension | Assessment | Evidence |
|-----------|------------|----------|
| Completeness | **Strong** | Load order (1–6 + optional); role per doc; code entry points; token/scope note. |
| Structure | **Strong** | Numbered order; table (order, document, role). |
| Consistency | **Strong** | Doc names and purposes match the rest of the corpus. |
| Agent-readability | **Strong** | An agent can follow the list to load context before working; entry points are file paths and function names. |
| Decomposition | **N/A** | Specifies “what to load,” not “how to do a multi-step task.” |
| Evaluation design | **N/A** | Not about testing. |

**Verdict:** Meta-spec for context. Makes the corpus explicitly “loadable” in order for agent sessions.

---

### 3.9 Ingestion and self-contained submissions (`docs/ingestion-and-sources.md` § Self-contained submissions)

| Dimension | Assessment | Evidence |
|-----------|------------|----------|
| Completeness | **Strong** | Definition of self-contained; three criteria (what, where, optional why); weak vs better examples; note for analyst prompts. |
| Structure | **Strong** | Numbered list; examples; link to actionable-insights. |
| Consistency | **Strong** | Aligns with acceptance criteria in schema (self-contained raw_text) and constraint doc (staging without context as failure mode). |
| Agent-readability | **Strong** | Criteria and examples are actionable for humans and for analyst prompt design. |
| Decomposition | **N/A** | Specifies quality of one artifact (submission), not task breakdown. |
| Evaluation design | **N/A** | Not about testing. |

**Verdict:** Spec for input quality. Supports specification discipline by making “good submission” verifiable.

---

### 3.10 Code as specification

| Artifact | Role | Alignment with docs |
|----------|------|----------------------|
| `app/schema/record.js` | Canonical implementation of Record and gate shape; load/save/merge. | Matches schema-record-api; JSDoc has stale `selfSkillRead` reference (runtime uses selfSkillThink). |
| `app/pipeline/stage.js` | Creates candidate; SKILL_MAP → mind_category, suggested_ix_section. | Matches schema and project-6week; no doc that exhaustively lists SKILL_MAP (could add one line in schema or stage comment). |
| `app/pipeline/merge.js` | Approve/reject; mergeCandidate; receipt. | Matches Identity Fork and acceptance criteria; receipt shape in doc. |
| `app/pipeline/edge.js` | Derives THINK/WRITE/WORK from Record. | Edge shape in schema; CONCEPT §4 for WORK + IX-C. |
| `app/export/curriculum-profile.js` | Builds export JSON. | Matches project-6week and export shape (knowledge, curiosity, personality, edge, evidenceCount, exportDate, screen_time_target_minutes). |

**Verdict:** Code is the executable spec. Alignment is strong; only minor cleanup (JSDoc, optional SKILL_MAP in doc) would improve consistency.

---

## 4. Specification primitives (transcript) — scorecard

| Primitive | How companion-self addresses it | Score |
|-----------|---------------------------------|--------|
| **Self-contained problem statements** | Ingestion § Self-contained submissions; activity placeholder; acceptance criteria (raw_text self-contained). | ✅ Strong |
| **Acceptance criteria** | Schema-record-api § Acceptance criteria for staging and merge (staged candidate good, merge outcome good, independent observer). | ✅ Strong |
| **Constraint architecture** | Constraint-architecture-and-failure-modes; Identity Fork; CONCEPT invariants. | ✅ Strong |
| **Decomposition** | Project-6week (weeks, tasks, deliverables); per-week success criteria. No explicit “decomposition pattern for planner agents” for arbitrary features. | ✅ Strong for build; ⚪ Optional for agent-led feature work |
| **Evaluation design** | Evaluation-design-and-regression doc; run-eval-fixtures.js; merge receipts. | ✅ Strong |

---

## 5. Gaps and recommendations

| Gap | Severity | Recommendation |
|-----|----------|----------------|
| **JSDoc in record.js** still says `selfSkillRead` in Record typedef; runtime and schema use THINK / selfSkillThink. | Low | Update typedef to `selfSkillThink` (or both if backward compat needed) so doc and code match. |
| **Project-6week** does not mention running `scripts/run-eval-fixtures.js` after schema/pipeline changes. | Low | Add one line under “Success” for relevant weeks or a short “Regression” subsection: run eval script after changes to schema or pipeline. |
| **SKILL_MAP** (THINK→IX-A, WRITE→IX-C, WORK→IX-B) is only in code; schema describes suggested_ix_section but not the default mapping. | Low | Optional: add one sentence or table in schema-record-api or in stage.js comment: “Template default mapping: THINK→IX-A, WRITE→IX-C, WORK→IX-B.” |
| **Decomposition for planner agents** (e.g. “how to break a new feature into subtasks”) is not specified. | Optional | If long-running coding agents are used, add a short “Decomposition patterns” or “Break pattern for new work” (e.g. in context-pack or a new doc). |
| **Analyst output contract** has no formal test in template (instances test their own). | Optional | Keep in instance scope; template provides the contract only. |

---

## 6. Summary

| Dimension | Overall | Notes |
|-----------|---------|--------|
| Completeness | **Strong** | Schema, CONCEPT, project-6week, instance-patterns, Identity Fork, constraint doc, evaluation design, context pack, and self-contained guidance together specify structure, behavior, constraints, and “done.” |
| Structure | **Strong** | Tables, sections, cross-refs; consistent formatting and naming. |
| Consistency | **Strong** | Terminology and shapes aligned across docs and code; one minor JSDoc mismatch. |
| Agent-readability | **Strong** | Stable paths, field names, enums; explicit must/must not; load order and entry points. |
| Decomposition | **Strong** | 6-week project is the decomposition spec; optional extension for planner-agent break patterns. |
| Evaluation design | **Strong** | Acceptance criteria in schema; evaluation-design-and-regression doc; runnable fixtures script. |

**Verdict:** Companion-self’s **specification discipline is strong**. The corpus is complete, structured, consistent, and agent-readable; acceptance criteria and evaluation design are implemented. The main improvements are small: align JSDoc with runtime, reference the regression script in the 6-week doc, and optionally document the default SKILL_MAP and decomposition patterns for agent-led work.
