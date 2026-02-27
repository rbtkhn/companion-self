# Actionable insights from the transcript

**Companion-Self template · Transcript → concrete actions**

This doc maps the *10x AI Users Aren't Smarter Than You* transcript (four disciplines + primitives) to **concrete actions** we took in the template. The evaluation [already scored us strong](evaluation-four-disciplines.md); here we turn transcript advice into implemented practice.

---

## Transcript → action mapping

| Transcript idea | Action we took |
|-----------------|----------------|
| **Self-contained problem statements** — "State the problem with enough context that the task is plausibly solvable without the receiver going out and getting more information." "Rewrite as if the person receiving it has never seen your dashboard... has no access to any information other than what you include." | **[Self-contained submission guidance](ingestion-and-sources.md#self-contained-submissions)** — When submitting "we did X," include enough that a reviewer (or future agent) who wasn’t there can understand what was done and where it might go. Activity form placeholder and docs updated. |
| **Acceptance criteria** — "For every task you delegate, write three sentences that an independent observer could use to verify the output without asking you any questions." | **[Acceptance criteria for staging and merge](schema-record-api.md#acceptance-criteria-for-staging-and-merge)** — What "good" looks like for a staged candidate and for a merge outcome; an independent reviewer can verify without asking. |
| **Constraint architecture / failure modes** — "Write down what a smart well-intentioned person might do that would technically satisfy the request but produce the wrong outcome. Those failure modes end up being your constraint architecture." | **[Constraint architecture and failure modes](constraint-architecture-and-failure-modes.md)** — Explicit list of behaviors we prevent (e.g. batch merge, inference into Record). Use in analyst prompts and agent rules. |
| **Context pack** — "Their agents start each session with the right project files, the right conventions, the right constraints already loaded." | **[Context pack for agents](context-pack-for-agents.md)** — What to load, in what order, when an agent (or human) works against this repo or a companion. |
| **Evaluation design** — "Build an eval: build three to five test cases with known good outputs and run them periodically, especially after model updates." | **[Evaluation design and regression](evaluation-design-and-regression.md)** — Fixture candidates and merge scenarios; script to run stage/load/merge and assert. Catches regressions after schema or pipeline changes. |

---

## Primitives we already had (and strengthened)

- **Constraint: merge only with approval** — Already in Identity Fork; we made **failure modes** explicit so instances can encode them in analyst prompts.
- **Specs as executable** — Schema and CONCEPT already; we added **acceptance criteria** in prose so "done" is verifiable by an independent observer.
- **Evidence and receipts** — Merge receipts and evidence linking already; we added **eval fixtures and a regression script** so we can prove behavior after changes.

---

## Where to look

| If you want to… | See |
|-----------------|-----|
| Write self-contained "we did X" submissions | [Ingestion and sources § Self-contained submissions](ingestion-and-sources.md#self-contained-submissions) |
| Verify what "good" looks like for staging and merge | [Schema and API § Acceptance criteria](schema-record-api.md#acceptance-criteria-for-staging-and-merge) |
| Encode what agents must not do (for analyst or Cursor) | [Constraint architecture and failure modes](constraint-architecture-and-failure-modes.md) |
| Load the right context for an agent session | [Context pack for agents](context-pack-for-agents.md) |
| Run regression after schema/pipeline changes | [Evaluation design and regression](evaluation-design-and-regression.md) + `scripts/run-eval-fixtures.js` |
