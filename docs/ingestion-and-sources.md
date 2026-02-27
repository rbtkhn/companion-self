# Ingestion and sources

**Companion-Self template · Pattern**

---

## Principle

The **Record** is the single convergence point. Activity and evidence can come from many sources; the instance accepts them through **staging/ingestion**, and the **human gate** decides what merges into the Record. Sources are pluggable—no single tool or format is required.

---

## Pattern

1. **Many sources** — Calendar exports, task/chore apps, manual entry, webhooks (e.g. from a family calendar or Skylight), CSV uploads, or other tools emit "something happened" or "someone did X."
2. **Staging / ingestion** — The instance accepts that input (e.g. POST activity with a skill_tag, webhook callback, or one-off import). Nothing is written directly to the Record; candidates are staged.
3. **Human gate** — The companion (or delegated human) reviews and approves what to merge. Only then does the activity become evidence and update the Record.
4. **Record and evidence** — Merged content lives in the Record and self-evidence; edge (what's next) and export reflect it.

So: **many sources → one staging pipeline → gate → one Record.**

**Multiple agents:** Several staging sources (or agents) can run in parallel; they all feed the same gate. Coordination (serialized writes to the gate, unique candidate IDs) and role-specific context are described in [Multi-agent parallelism](multi-agent-parallelism.md).

**Staging format:** Instances may use `recursion-gate.json` (JSON array of candidates) or `pending-review.md` (YAML/markdown blocks). The gate contract (candidates, approve/reject, merge) is what matters; format is instance choice. See [Instance patterns](instance-patterns.md) § Staging format.

---

## Examples

- **Chore completed in Skylight (or similar)** — A bridge or webhook sends "chore X completed by profile Y at time Z" as POST activity with `skill_tag: WORK`. Pipeline stages it; caregiver gates; merge creates evidence (e.g. ACT-xxxx) linked to self-skill-work.
- **Quiz or assessment completed** — Tutor or curriculum sends "quiz Q completed: topic X, score 4/5." Pipeline stages (1) the quiz as an **evidence activity** (id, date, summary) and (2) an **optional suggested merge to self-knowledge** (e.g. "Topic X: demonstrated via quiz Q (4/5, date)"). Both are candidates at the gate. Companion approves or rejects each. On approve: evidence → self-evidence; approved knowledge candidate → one line in self-knowledge with evidence link to the quiz. No auto-merge of inferred knowledge; see [CONCEPT](concept.md) §5 Knowledge Boundary.
- **CSV upload of past events** — User exports calendar or task history to CSV. An instance script or UI maps rows to staged activity (e.g. READ or WORK). User reviews and merges in batches. Record and evidence now reflect history without manual re-entry.
- **Manual "we did X"** — Companion or caregiver posts activity via instance API or UI. Same pipeline: stage → gate → merge. Source is "manual," but the path is the same.

---

## Self-contained submissions

**Transcript primitive:** State the problem with enough context that the task is plausibly solvable without the receiver having to "go fetch" missing information. Rewrite as if the person receiving it has never seen your context and has no access to any information other than what you include.

**Application:** When submitting "we did X" (via UI, API, or analyst), make the submission **self-contained** so that:

1. A reviewer who wasn’t there can understand **what** was done (activity, topic, artifact).
2. They can reason about **where** it might go in the Record (which dimension or skill) without asking you.
3. Optional but useful: a short "why it matters" or "what we’re building on" so merge decisions are informed.

**Examples:**

- Weak: "Did the thing."  
- Better: "Read chapter 3 of *Dragon Guide* and summarized the migration habits. THINK."
- Better: "Finished the dragon drawing we started yesterday; used watercolors. WORK."

The activity form and API accept freeform text; the discipline is in what you put in `raw_text`. Instances that use an LLM analyst should prompt the analyst to produce self-contained `raw_text` (and suggested dimension) so the companion can gate without re-reading the original conversation. See [Actionable insights from the transcript](actionable-insights-transcript.md).

---

## Triggers for suggested merges

**Template today:** The template and 6-week app do **not** implement automatic triggers. Staging is request-driven: each POST or webhook creates the candidate(s) that the caller explicitly sends. One POST = one candidate unless the caller or instance logic creates more.

**Instances may add triggers** so that when certain activity types are received, the instance **automatically stages both** an evidence candidate and an optional suggested dimension-merge candidate (e.g. suggested self-knowledge line). The companion still gates both; no auto-merge.

### Implementable trigger pattern

1. **Payload** — Incoming activity includes an **activity type** (or equivalent). Examples: `quiz` | `assessment` | `read_completion` | `write_demonstration` | `work_project` | `manual`. Optional: `topic`, `score`, `source_id`, `summary`.
2. **Trigger rule** — Instance staging logic (e.g. in POST handler or webhook handler) checks activity type. If type is one that warrants a **suggested merge** (see table below), create **two** candidates and append both to the gate:
   - **Candidate 1 (evidence):** id, raw_text (e.g. "Quiz on topic X, 4/5"), skill_tag, suggested_ix_section (can be null or default), created_at, status: "pending". Optional: `evidence_summary`, `source_id`.
   - **Candidate 2 (suggested dimension merge):** id, raw_text = the **suggested line** (e.g. "Topic X: demonstrated via quiz Q (4/5, &lt;date&gt;)"), skill_tag (same as candidate 1 or derived), suggested_ix_section = target dimension (IX-A, IX-B, or IX-C), created_at, status: "pending". Optional: `link_to_evidence_id` = candidate 1's id so merge logic can link the dimension line to the evidence activity.
3. **Gate** — Companion sees two candidates. They may approve both, approve only evidence, or reject either. Merge logic: approving the evidence candidate writes to self-evidence; approving the dimension candidate writes one line to the appropriate dimension file (self-knowledge, self-curiosity, or self-personality) and, if `link_to_evidence_id` is set, links that line to the evidence entry.
4. **Schema** — Extend the recursion-gate candidate shape as needed. Minimal extension: allow `link_to_evidence_id` (optional) on a candidate so the second candidate references the first. Merge logic uses it when writing the dimension line (e.g. store evidence id in the line or in a structured evidence link).

### Trigger types and suggested dimension

| Activity type | Evidence candidate | Second candidate (suggested merge) |
|---------------|--------------------|-----------------------------------|
| `quiz`, `assessment` | Quiz/assessment summary (topic, score, date) | suggested_ix_section: **IX-A** (self-knowledge). Suggested line: e.g. "Topic X: demonstrated via quiz (score, date)." |
| `read_completion` | Read completed (source, topic, date) | suggested_ix_section: **IX-A** or **IX-B** (knowledge or curiosity). Suggested line: e.g. "Topic X: read and understood (source, date)." |
| `write_demonstration` | Write/reflection summary | suggested_ix_section: **IX-A**, **IX-B**, or **IX-C** (knowledge, curiosity, or personality). Suggested line: e.g. "Topic X: demonstrated in writing (evidence id)." |
| `work_project` | Project/ship summary | suggested_ix_section: **IX-A**, **IX-B**, or **IX-C** as appropriate. Suggested line: e.g. "Topic X: applied in project Y (evidence id)." |
| `manual` (default) | Raw text only | No second candidate unless caller sends two payloads. |

Implementations may use different activity-type names or add types (e.g. `flashcards`, `tutor_qa`); the pattern is the same: evidence candidate + optional dimension candidate with suggested_ix_section and suggested line, both gated.

---

## Why it matters

Users should not maintain two worlds. Companion-self is designed so that **messy or scattered input** (different apps, exports, one-off events) can be normalized into one flow and one Record. Ingestion from many sources is a first-class pattern, not an afterthought.
