# Schema and API contract

**Companion-Self template · Minimal schema for Record and pipeline**

This document defines the Record schema, recursion-gate shape, and API contracts for the 6-week student interface and future extensions. See [CONCEPT](concept.md), [IDENTITY-FORK-PROTOCOL](identity-fork-protocol.md), and [PROJECT-6WEEK-CODING](project-6week-coding.md).

---

## Record schema

| Component | File | Fields / structure |
|-----------|------|--------------------|
| **SELF** | self.md | Identity baseline (I–VIII); optional pointer to IX. |
| **IX-A** | self-knowledge.md | Topics, facts; one line per entry; optional evidence id. |
| **IX-B** | self-curiosity.md | Interests, questions; one line per entry; optional evidence id. |
| **IX-C** | self-personality.md | Voice, preferences, values, narrative; one line per entry; optional evidence id. |
| **THINK** | self-skill-think.md | Intake and comprehension; evidence links. |
| **WRITE** | self-skill-write.md | Expression and voice; evidence links. |
| **WORK** | self-skill-work.md | Making and doing; evidence links. See **WORK objectives and tasks** below. |
| **self-evidence** | self-evidence.md | Activity log entries: `id`, `date`, `summary`, `skill_tag` (THINK \| WRITE \| WORK). |

All Record files live under `users/<id>/`. Dimension files (IX-A, IX-B, IX-C) are the source of truth for post-seed growth.

---

## WORK (self-skill-work): objectives and tasks standard

Standard modular structure for objectives and tasks in `self-skill-work.md`. Instances may extend (e.g. add levels, creative context) but these fields are the template contract.

### Objectives

| Element | Type | Description |
|--------|------|--------------|
| **module_intent** | string | One sentence: WORK as tutor; edge, scaffolding, work goals, life mission; human-gated. |
| **default_objectives** | list of { label, description } | **Default objectives for new users** (standard set of five): Learn and grow, Express and create, Build and ship, Make progress visible, Stay within the design. Instance may replace or extend. In markdown: `- **Label** — description`. |
| **work_goals** | object | Companion's own goals; evidence-linked when captured. |
| **work_goals.near_term** | string[] | Near-term goals (e.g. "finish X", "learn Y"). May be empty. |
| **work_goals.horizon** | string[] | Longer-term goals (e.g. "SAT ≥ 1200"). May be empty. |
| **work_goals.source** | string (optional) | Evidence id when goals were captured. |
| **life_mission_ref** | string | Pointer to SELF (e.g. `self.md § VALUES`). WORK goals align with life mission. |

### Tasks

Planning and execution items (projects, next steps, deliverables). Each task:

| Field | Type | Description |
|-------|------|-------------|
| **id** | string (optional) | Stable id for linking (e.g. `task-1`, `T-001`). |
| **summary** | string | Short description of the task. |
| **status** | string | One of: `pending`, `in_progress`, `done`. |
| **evidence_id** | string (optional) | Evidence id when task is completed and recorded (links to self-evidence). |
| **updated** | string (optional) | ISO date or timestamp of last change. |

**Markdown representation:** Use a table or a consistent list form. Example table:

```markdown
| id | summary | status | evidence_id |
|----|---------|--------|-------------|
| T-001 | Finish dragon drawing | done | ACT-xxx |
| T-002 | Next chapter read-aloud | pending | — |
```

Or list form: `- **summary** — status (evidence_id)`.

Instances may add fields (e.g. priority, target_date, skill_tag). The minimum for template compliance is **summary** and **status**.

---

## Recursive-gate shape

Array of candidates. Each candidate:

| Field | Type | Description |
|-------|------|--------------|
| id | string | Unique id (uuid or timestamp). |
| raw_text | string | Raw "we did X" or activity text. |
| skill_tag | string | THINK, WRITE, or WORK. |
| mind_category | string | knowledge, curiosity, or personality (keyword or default). |
| suggested_ix_section | string | IX-A, IX-B, or IX-C (target dimension). |
| created_at | string | ISO date or timestamp. |
| status | string | "pending" until approved/rejected. |

**Format:** `users/<id>/recursion-gate.json` — JSON array, append-only on stage. Candidates are removed on approve (merge) or reject.

---

## Edge response shape (Week 5)

GET `/api/edge` returns suggested next focus per READ, WRITE, WORK. Also included in GET `/api/record` and `/api/export` curriculum profile.

| Field | Type | Description |
|-------|------|--------------|
| THINK | string | Suggested next focus for intake/comprehension (e.g. "Keep reading", "Continue with: topic"). |
| WRITE | string | Suggested next focus for expression (e.g. "Try a short story", "Build on: …"). |
| WORK | string | Suggested next focus for making/doing. Phrased using self-personality (IX-C) when available. See [CONCEPT](concept.md) §4 "How WORK utilizes self-personality (IX-C)". |

**Example:** `{ "THINK": "Keep reading", "WRITE": "Try a short story", "WORK": "One small project" }`
