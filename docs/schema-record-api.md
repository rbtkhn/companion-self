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
| **READ** | self-skill-read.md | Intake and comprehension; evidence links. |
| **WRITE** | self-skill-write.md | Expression and voice; evidence links. |
| **WORK** | self-skill-work.md | Making and doing; evidence links. |
| **self-evidence** | self-evidence.md | Activity log entries: `id`, `date`, `summary`, `skill_tag` (READ \| WRITE \| WORK). |

All Record files live under `users/<id>/`. Dimension files (IX-A, IX-B, IX-C) are the source of truth for post-seed growth.

---

## Recursive-gate shape

Array of candidates. Each candidate:

| Field | Type | Description |
|-------|------|--------------|
| id | string | Unique id (uuid or timestamp). |
| raw_text | string | Raw "we did X" or activity text. |
| skill_tag | string | READ, WRITE, or WORK. |
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
| READ | string | Suggested next focus for intake/comprehension (e.g. "Keep reading", "Continue with: topic"). |
| WRITE | string | Suggested next focus for expression (e.g. "Try a short story", "Build on: …"). |
| WORK | string | Suggested next focus for making/doing. Phrased using self-personality (IX-C) when available. See [CONCEPT](concept.md) §4 "How WORK utilizes self-personality (IX-C)". |

**Example:** `{ "READ": "Keep reading", "WRITE": "Try a short story", "WORK": "One small project" }`
