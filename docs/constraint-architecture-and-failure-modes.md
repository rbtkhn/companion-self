# Constraint architecture and failure modes

**Companion-Self template · What we must prevent so agents and humans stay aligned**

**Transcript primitive:** Write down what a smart well-intentioned person might do that would technically satisfy the request but produce the wrong outcome. Those failure modes end up being your constraint architecture.

This doc makes **failure modes we prevent** explicit. Use it when writing analyst prompts, agent rules, or operator instructions so that "technically correct" behavior doesn’t violate sovereignty or the knowledge boundary.

---

## Constraint architecture (four categories)

| Category | Meaning | Companion-self encoding |
|----------|---------|--------------------------|
| **Must** | What the system/agent must do | Stage candidates in the agreed shape; write merge receipts; link evidence. |
| **Must not** | What the system/agent must not do | See failure modes below. |
| **Prefer** | When multiple valid approaches exist | Prefer one candidate per approve; prefer self-contained raw_text; prefer explicit suggested_ix_section. |
| **Escalate** | When to stop and ask a human | Any merge decision; any content that would go into the Record; anything outside documented knowledge for Voice. |

---

## Failure modes we prevent

These are behaviors that might seem reasonable (e.g. "batch merge for efficiency") but produce the wrong outcome. The template and instances should encode them as **must not** or **escalate**.

| Failure mode | Why it’s wrong | How we prevent it |
|-------------|----------------|-------------------|
| **Batch or automatic merge** | Merge is a sovereign act; only the companion (or delegated human) may merge. Automating merge removes human gate. | One-at-a-time approve in UI and API; no "merge all" in template. Process-the-gate command means: for each candidate, human chooses approve or reject. |
| **Inferring into the Record from model knowledge** | Record may contain only what the companion has provided and approved. LLM inference is not provision. | Knowledge boundary (CONCEPT §5): no LLM inference into Record; calibrated abstention when outside documented knowledge. Analyst stages *suggested* lines; human gates. |
| **Skipping the gate** | Writing directly to Record (self-evidence, dimension files) bypasses the companion’s approval. | All writes to Record go through merge path; merge is only after approve. Stage writes to recursion-gate only. |
| **Optimizing for throughput over sovereignty** | E.g. "merge 10 candidates in one click" or "auto-approve when confidence > 0.9." | Design choice: we never auto-merge. Instances that add scoring may show scores to the human but must not merge without explicit approve. |
| **Staging without enough context** | raw_text like "Did it" leaves the companion unable to verify what "it" is or where it belongs. | Self-contained submission guidance (ingestion-and-sources); acceptance criteria for staged candidate; analyst prompt should ask for self-contained raw_text. |
| **Changing Record for "consistency" without approval** | E.g. normalizing dates or fixing "typos" in dimension files by an agent. | Only merge path may write to Record; merge is triggered only by human approve of a specific candidate. No background "cleanup" agent writing to Record. |
| **Voice speaking from training data** | Voice must speak the Record; when outside Record, say "I don’t know" or offer lookup. | Voice implementation must be constrained by Record + knowledge boundary; no unbounded generation from model knowledge into answers. |

---

## Use in analyst prompts (instances)

When an instance adds an LLM analyst that stages candidates from conversation, the analyst prompt should include constraints that mirror these failure modes, for example:

- "Stage one candidate per distinct activity; do not batch multiple activities into one candidate."
- "Do not merge or write to the Record; only stage. The human will approve or reject."
- "raw_text must be self-contained: a reviewer who did not see the conversation must understand what was done and where it might go."
- "Do not infer facts from your training; only stage what was said or demonstrated in the conversation (or linked artifact)."

See [Instance patterns](instance-patterns.md) for the analyst output contract and [Identity Fork Protocol](identity-fork-protocol.md) for the sovereign merge rule.
