# Evolving practice and recursive improvement

**Companion-Self template · How to keep improving companion-self and the human companion as technology advances**

The default WORK objective **Recursively improve** (“Improve the ability of companion-self and the human companion over time; this objective can evolve as technology and practice advance”) is operationalized in part by staying current with how we specify work for AI systems and for each other. As autonomous agents and long-running tasks become normal, the skills that differentiate effective use of AI are shifting from chat-based prompting to a stack of disciplines that apply to both human and agent delegation.

---

## Why this matters for companion-self

Companion-self’s Record, pipeline, and docs already function as **context** and **intent** infrastructure: the Record is what agents (and humans) read to know the companion; the gate encodes “what may be merged” (intent); schema and API contracts are specifications agents can execute against. As models and tools evolve (e.g. long-running agents, planner–worker setups, multi-session tasks), the same discipline that makes companion-self work—clear context, human-gated intent, evidence-linked specs—maps onto broader practice for working with AI and with teams. Keeping the Recursively improve objective in mind means periodically revisiting how we write down goals, constraints, and “done” so that both companion-self and the human companion get better as technology advances.

---

## A useful framework: four disciplines (post–Feb 2026)

One influential framing treats “prompting” as having diverged into **four distinct disciplines**, each operating at a different altitude. Summarized here for relevance to recursive improvement; not a substitute for the primary source.

| Discipline | What it is | Companion-self analogue |
|------------|------------|--------------------------|
| **Prompt craft** | Clear instructions, examples, guardrails, output format for a single session. | How we phrase pipeline prompts, edge copy, “we did X” prompts. |
| **Context engineering** | Curating the full information environment an agent operates in (system prompts, tools, docs, memory). | The Record (SELF, IX-A/B/C, skills, evidence) and docs; what we load into any agent’s context. |
| **Intent engineering** | Encoding purpose, goals, values, trade-offs, decision boundaries so agents can act autonomously in alignment. | Identity Fork Protocol (agent may stage, may not merge); WORK goals and life mission ref; default objectives. |
| **Specification engineering** | Writing documents that autonomous agents can execute against over long horizons without real-time human intervention. | schema-record-api, project-6week-coding, CONCEPT; acceptance criteria and structure for pipeline and export. |

**Implication:** Recursively improving companion-self and the human companion includes getting better at all four—especially context and intent (Record + gate) and specification (how we define “done” and structure work for agents and humans).

---

## Primitives that support good specifications

Practitioners often emphasize a small set of **primitives** that make specs and delegation effective, for both AI and humans:

- **Self-contained problem statements** — State the problem with enough context that the task is plausibly solvable without the receiver having to “go fetch” missing information. Surfaces hidden assumptions; reduces ambiguity.
- **Acceptance criteria** — What does “done” look like? If it can’t be described so an independent observer could verify it, the task isn’t ready to delegate.
- **Constraint architecture** — What must be done, what must not be done, what is preferred when multiple approaches are valid, what gets escalated rather than decided autonomously. (The gate is a constraint: merge only with approval.)
- **Decomposition** — Break large outcomes into independently executable, testable pieces with clear input/output boundaries. Supports long-running or multi-session work.
- **Evaluation design** — How do we know the output is good? Recurring tasks benefit from test cases and periodic checks, especially after model or process changes.

These map directly onto companion-self: evidence and merge receipts as evaluation; gate and life mission as constraints; schema and API contracts as specs; Record as the curated context.

---

## Reference

- **Video:** *10x AI Users Aren't Smarter Than You. They Just Know Something You Don't.* (YouTube; post–Feb 2026 framing on prompt craft, context engineering, intent engineering, specification engineering.)
- **Companion-self:** [Recursive self-learning objectives](recursive-self-learning-objectives.md), [Identity Fork Protocol](identity-fork-protocol.md), [Schema and API contract](schema-record-api.md), [CONCEPT](concept.md). The WORK objective **Recursively improve** in `self-skill-work.md` is the place this evolving practice is explicitly owned.
- **Evaluation:** [Evaluation: Companion-Self against the four disciplines](evaluation-four-disciplines.md) — how the template scores on each discipline and where to improve. **Specification only:** [Evaluation: Specification discipline](evaluation-specification-discipline.md).
- **Actionable:** [Actionable insights from the transcript](actionable-insights-transcript.md) — transcript ideas turned into concrete docs and scripts (self-contained submissions, acceptance criteria, failure modes, context pack, eval fixtures).
- **Multi-agent parallelism:** [Multi-agent parallelism](multi-agent-parallelism.md) — running multiple complex tasks on different agents at the same time (lanes, coordination, role-specific context, planner–worker).
