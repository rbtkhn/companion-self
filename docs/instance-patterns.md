# Instance patterns and reference implementation

**Companion-Self template · Patterns from advanced instances**

---

## Reference implementation: Grace-Mar

**Grace-Mar** (https://github.com/rbtkhn/grace-mar) is the first and currently only instance. It implements bot (Telegram, WeChat), LLM analyst, full pipeline, profile, miniapp, export, and metrics. Instances can reference it for implementation patterns.

The template stays code-light and protocol-first; Grace-Mar diverges in several ways (see below). These divergences are documented so the template remains minimal while instances know what extensions are possible.

---

## Instance variations

| Area | Template | Grace-Mar |
|------|----------|-----------|
| **Intake skill** | READ (self-skill-read) | THINK — semantically equivalent (intake, comprehension). |
| **Staging format** | recursion-gate.json (JSON array) | pending-review.md (YAML/markdown blocks). |
| **Analyst** | Out of scope for 6 weeks | LLM analyst runs on conversation and "we did X"; stages candidates automatically. |
| **Voice** | Not implemented | Telegram + WeChat bots. |
| **Archive** | self-memory.md (ephemeral, optional) | self-archive.md (gated log, rotation when large). |

---

## Staging format

Instances may use either:

- **recursion-gate.json** — JSON array of candidates: `{ id, raw_text, skill_tag, mind_category, suggested_ix_section, created_at, status }`. Suits API-driven staging (POST activity).
- **pending-review.md** — YAML/markdown blocks per candidate. Suits analyst output and manual review workflows. Candidate fields may include `mind_category`, `signal_type`, `summary`, `profile_target`, `suggested_entry`, `prompt_section`, `prompt_addition`.

The gate contract (candidates, approve/reject, merge) is identical; format is instance choice.

---

## Analyst output contract (optional)

When an instance adds an **LLM analyst** that stages candidates from conversation or activity, the analyst output should conform to a contract so merge logic can consume it. Grace-Mar uses flat YAML with these required fields:

| Field | Meaning |
|-------|---------|
| mind_category | One of: knowledge, curiosity, personality (maps to IX-A, IX-B, IX-C). |
| signal_type | Kind of signal (e.g. lookup, knowledge, teach, new_interest, personality). |
| summary | Brief description of what was observed. |
| profile_target | Target dimension/section (e.g. IX-A, IX-B, IX-C). |
| suggested_entry | Proposed line for the dimension file. |
| prompt_section | Section of prompt/Record this relates to. |
| prompt_addition | Proposed addition to that section. |

Optional: `priority_score` (1–5), `tension_with` or `alternative_interpretation` when the signal conflicts with existing profile. Analyst may return `NONE` when no signal is detected.

**Design principle:** The analyst detects and stages; the companion gates. No merge without approval.

---

## Session brief (operator tool)

**Session brief** — Before or during a session, the operator (or companion) may want a short summary: what's pending at the gate, recent activity, suggested next focus. This is an **operator tool pattern**, not a template requirement.

Instances that support it can expose: pending count, list of candidate summaries, recent merges, edge ("what's next"). Useful for "quick sync" before processing the gate or starting a session.

---

## Conflict check (optional)

Before merge, an instance may run a **conflict check** on a candidate: compare suggested content against existing Record (e.g. IX-A, IX-B, IX-C) and flag potential contradictions or overlap. Surfaces for user resolution; does not block staging. The companion still decides at the gate; conflict check is advisory.

---

## Cross-references

- [Concept](concept.md) — READ/WRITE/WORK, identity and instrument.
- [Ingestion and sources](ingestion-and-sources.md) — Many sources → staging → gate → Record; triggers for suggested merges.
- [Identity Fork Protocol](identity-fork-protocol.md) — Sovereign Merge Rule, schema, Process the gate.
- [Project 6-week coding](project-6week-coding.md) — Minimal student interface (no analyst, no Voice).
