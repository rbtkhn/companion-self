# 3-Year Roadmap: 90% Alpha Value at 10% Cost

**Companion-Self template · Strategic roadmap**

**Goal:** Enable companion-self instances (and their ecosystem) to deliver **~90% of Alpha School’s value** at **~10% of the cost** within three years. This doc defines the target, the value/cost framing, and the project and technology advancement required at the template and instance level. Instances (e.g. grace-mar) and ecosystem partners execute; the template evolves protocol, schema, and guidance so the stack can credibly achieve this.

---

## Target definitions

### 90% of Alpha value (what we’re aiming at)

| Alpha value dimension | 90% interpretation | Delivered by |
|-----------------------|--------------------|--------------|
| **Mastery-based academic progress** | Personalized progress at the right level; 2–5x effective pace vs traditional classroom; evidence of mastery, not grades. | Record (knowledge, edge) + curriculum/tutor that consumes Record; pipeline captures evidence. |
| **Motivation and ownership** | Companion (and operator) see progress; “time back”; love of learning; lightweight ritual (“we did X”). | Record as engagement substrate; structure of day; **system** provides progress visibility and prompts; operator/guardian optional. |
| **Life skills and creation** | READ/WRITE/WORK balance; passion projects; evidence of what they’ve made and done. | Record WORK evidence; operator + community workshops/prompts; project templates. |
| **Identity and evidence** | Portable, artifact-grounded Record; no platform lock-in; truth about level and capability. | Companion-Self protocol and schema; pipeline and gate; export. |
| **Closed-loop improvement** | System gets better with use; next best action informed by Record. | Pipeline recursion; edge export; curriculum/tutor that adapts from Record. |
| **Guide-like support** | High standards + high support; “did you read the explanation?”; connect to resources. | **System first:** Voice, pipeline prompts, session copy, edge suggestions. Operator/parent may augment but is **not assumed**; companion-self must achieve objectives without a human guide. See [CONCEPT](CONCEPT.md) §6 invariant 7. |

We do **not** aim to replicate Alpha’s physical schools, their $100M+ Timeback engine, or their guide hiring at six figures. We aim to deliver equivalent **outcomes** (mastery, motivation, life skills, identity) via **Record + best-available free/low-cost curriculum and tutor + operator + community**.

### 10% of cost

| Alpha cost | 10% target | How |
|------------|------------|-----|
| **$40K–$75K/year tuition** | **$400–$2,500/year total cost to family** (software + optional tutoring/curriculum). | Hosted Record: ~$80–$200/year. Curriculum: free/low-cost (Khan, IXL, open tutor, public resources). Optional paid tutor or microschool: add $200–$2K. No $40K school. |
| **Interpretation** | “10% cost” = order-of-magnitude reduction in **total out-of-pocket** while preserving the **value stack** (identity, mastery, motivation, life skills). | Template + instances + ecosystem make the Record the spine; teaching comes from integrated free/low-cost tools and human guide. |

### Equivalent metric: 2 hours screen time per day

Alpha squeezes **all mandatory education into ~2 hours of screen time per day**. Companion-Self is calibrated to the **same 2-hour window**: all screen-based learning (curriculum, tutor, Record capture, student interface) is designed to fit within **2 hours per day**. This is a **design constraint** and an **equivalent metric** for comparison — "2 hours = full academic coverage." Outcomes (mastery, evidence, motivation) are comparable per 2-hour block. See [TWO-HOUR-SCREENTIME-TARGET](TWO-HOUR-SCREENTIME-TARGET.md).

---

## Year 1: Foundation (Record-first, export, proof)

**Theme:** The Record is the identity spine. Export formats and pipeline maturity let curriculum and tutors “plug in.” Prove retention and trust.

### Project

| Initiative | Deliverable | Owner |
|------------|-------------|--------|
| **Curriculum-consumable export** | Stable schema and export (e.g. `curriculum_profile` or equivalent): IX-A, IX-B, IX-C, READ/WRITE/WORK edge, Lexile or level, evidence anchors. Document in template; instance implements. | Template: schema doc. Instance: export script, docs. |
| **Pipeline and edge** | Pipeline produces “edge” (per skill/module) from self-skill-read, self-skill-write, self-skill-work + EVIDENCE; edge exposed in export. No auto-merge; stage-only. | Instance. |
| **Hosted family product** | One instance (e.g. grace-mar) offers hosted Record + pipeline + Voice for families; onboarding, “we did X,” review queue, export. | Instance. |
| **Proof architecture** | Pipeline health, gate integrity, retention (e.g. week-4, month-3), evidence-linked claim ratio. Report quarterly. | Instance + template (metrics definition). |
| **Seed and onboarding** | Seed-phase definition and templates in template; instance has repeatable onboarding (survey, first captures, first merge). | Template: SEED-PHASE, users/_template. Instance: flows. |

### Technology advancement

| Area | Advancement |
|------|-------------|
| **Schema** | READ/WRITE/WORK and edge represented in export; modality (text, video, etc.) where relevant for READ. |
| **Export** | Machine-readable profile for curriculum/tutor: knowledge, curiosity, personality, skills edge, evidence anchors. Versioned; backward compatible. |
| **Pipeline** | Reliable stage → review → merge; merge receipts; pipeline events for analytics. Recursion: updated Record influences next analyst run and Voice. |
| **Voice** | Voice speaks Record; knowledge boundary; optional “teaching” mode (answer questions in-character at Record level). |

### Success criteria (end of Year 1)

- Export consumed by at least one curriculum or tutor path (e.g. Khan + manual use of export, or one pilot integration).
- Hosted product: repeatable onboarding, week-4 and month-3 retention measurable, evidence ratio tracked.
- Template: protocol and schema stable; RECURSIVE-SELF-LEARNING-OBJECTIVES and INSIGHTS-ALPHA-MOONSHOTS-233 referenced by instance.

---

## Year 2: Integration (curriculum, tutor, life skills, operator tools)

**Theme:** Record drives what to do next. Integrations with free/low-cost curriculum and tutors. Life skills and WORK get structure. Operator effectiveness rises.

### Project

| Initiative | Deliverable | Owner |
|------------|-------------|--------|
| **Curriculum integration** | At least one “Record-in, lesson-out” path: curriculum or tutor reads export, suggests next lessons/activities at edge. E.g. Khan + export; or open-source tutor that consumes profile. | Instance + ecosystem. |
| **Edge-driven suggestions** | System (or operator dashboard) suggests “next at edge” for READ, WRITE, WORK from Record. No auto-merge; suggestions only. | Instance. |
| **Life skills / WORK templates** | Template and instance provide project prompts, workshop-in-a-box ideas, WORK evidence templates so operators can run “afternoon” style activities without building from zero. | Template: docs. Instance: prompts, templates. |
| **Operator tools** | Session brief (what’s in queue, what’s at edge); optional “guide prompts” (e.g. “Did you read the explanation?”); weekly review checklist. | Instance. |
| **“We did X” as first-class** | “We did X” ritual documented and prominent in UX and docs; pipeline processes it; retention and evidence metrics track it. | Template: reference in CONCEPT/SEED. Instance: UX, docs. |

### Technology advancement

| Area | Advancement |
|------|-------------|
| **Export** | Optional “next best action” or “suggested activities” derived from edge (instance or integration); still stage-only for Record. |
| **Integrations** | Documented integration pattern: pull export → suggest content → user does activity → capture to pipeline. One reference integration (e.g. Khan, Khanmigo, or open tutor) documented end-to-end. |
| **READ evidence** | Where feasible, READ evidence includes modality and source; quality signal (e.g. time on task, artifact link) for analytics. No requirement for vision models; can be self-report or platform webhook. |
| **WORK evidence** | Schema and templates for projects, artifacts, “what they built”; link to self-skill-work dimensions. |

### Success criteria (end of Year 2)

- At least one curriculum or tutor uses Record export to personalize (measure: export calls or integration usage).
- Operator tools in use; session brief and edge visibility available.
- Life skills/WORK templates in use; WORK evidence growing in sample Records.
- Retention and evidence quality stable or improving vs Year 1.

---

## Year 3: Scale and outcome parity (closed-loop, metrics, ecosystem)

**Theme:** Closed-loop with external curriculum. Measurable outcome parity with “90% Alpha value.” Community and ecosystem can run without the founding instance.

### Project

| Initiative | Deliverable | Owner |
|------------|-------------|--------|
| **Closed-loop with curriculum** | Curriculum/tutor returns outcomes (e.g. topic mastered, score) to instance; pipeline stages or links to EVIDENCE; Record updates via gate. Full loop: Record → curriculum → activity → evidence → Record. | Instance + integration partner. |
| **Outcome metrics** | Define and track “90% value” proxies: e.g. mastery coverage (topics/levels), READ/WRITE/WORK evidence growth, retention, operator NPS. No need to match Alpha’s SAT; do match “mastery-based, evidence-rich, portable identity.” | Template: metrics framework. Instance: instrumentation. |
| **Cost transparency** | Total cost of ownership (TCO) for a family: hosted Record + curriculum/tutor + optional guide. Document “10% cost” stack (e.g. $400–$2,500/year examples). | Instance + template (docs). |
| **Ecosystem and community** | Templates, docs, and optional certification so other instances or adopters can run “90% value / 10% cost” stacks. Open-source curriculum/tutor options listed; integration patterns published. | Template + ecosystem. |
| **Optional: low-cost AI tutor path** | If viable, document or partner for a low-cost AI tutor that consumes Record (interest, knowledge, edge) and respects knowledge boundary. Not required for 90/10; accelerates parity. | Ecosystem or instance. |

### Technology advancement

| Area | Advancement |
|------|-------------|
| **Pipeline** | Evidence ingestion from external systems (curriculum, tutor) with provenance; staged for merge; no direct write to Record by third parties. |
| **Export** | Versioned API or export format for curriculum/tutor; optional callback or webhook for “activity completed” to trigger capture. |
| **Analytics** | Dashboards or reports: edge movement, evidence by READ/WRITE/WORK, retention, cost per family. Template defines minimal set; instance implements. |
| **Protocol** | Identity Fork Protocol (and template) stable; certification or conformance criteria if ecosystem demands. |

### Success criteria (end of Year 3)

- Closed-loop demonstrated: Record → curriculum/tutor → activity → evidence → Record with gate.
- “90% value” documented via chosen metrics (mastery, evidence, retention, identity portability).
- “10% cost” documented via TCO examples ($400–$2,500/year range).
- At least one additional instance or adopter using template and running a 90/10-style stack.

---

## Summary: project and technology by year

| Year | Project focus | Technology focus |
|------|----------------|------------------|
| **1** | Export for curriculum; pipeline + edge; hosted product; proof; seed/onboarding. | Schema (edge, modality); export format; pipeline recursion; Voice + knowledge boundary. |
| **2** | Curriculum/tutor integration; edge-driven suggestions; life skills/WORK templates; operator tools; “we did X” first-class. | Export “next best action”; integration pattern; READ/WORK evidence quality and structure. |
| **3** | Closed-loop with curriculum; outcome metrics; cost transparency; ecosystem/community; optional low-cost AI tutor. | Evidence ingestion from external; export API; analytics; protocol stability/certification. |

---

## What we do not build (stays with Alpha or partners)

- **Proprietary K–12 curriculum engine** (Alpha’s Timeback/Incept). We consume best-available free/low-cost curriculum and tutors.
- **Physical schools or guide employment.** Operator/parent is the guide; optional community or microschool partners.
- **Incentive systems** (Alpha Bucks, store). We provide Record and ritual; incentives can be operator-designed or external.
- **Vision models for screen monitoring.** Optional for instances later; not required for 90/10. Evidence can be self-report, platform webhook, or manual capture.

---

## 6-week coding project (student interface)

The 3-year roadmap is compressed into a **6-week coding project** implemented entirely in companion-self and delivered as the **student product interface**. See [PROJECT-6WEEK-CODING](PROJECT-6WEEK-CODING.md) for week-by-week tasks, repo layout (`app/`, `users/demo/`), pipeline (stage → review → merge), and UI (dashboard, "we did X," review queue, export).

---

## References

- [LONG-TERM-OBJECTIVE](LONG-TERM-OBJECTIVE.md) — Permanent system rule; north star for alignment and drift prevention.
- [PROJECT-6WEEK-CODING](PROJECT-6WEEK-CODING.md) — 6-week implementation plan for student-facing app in companion-self.
- [RECURSIVE-SELF-LEARNING-OBJECTIVES](RECURSIVE-SELF-LEARNING-OBJECTIVES.md) — learning-science objectives for the Record.
- [INSIGHTS-ALPHA-MOONSHOTS-233-FOR-BUSINESS](INSIGHTS-ALPHA-MOONSHOTS-233-FOR-BUSINESS.md) — READ/WRITE/WORK and business narrative.
- [ALPHA-SCHOOL-BENCHMARKS](ALPHA-SCHOOL-BENCHMARKS.md) — Alpha's benchmarks (SAT, state tests, love-of-school); reference for comparable metrics.
- [IDENTITY-FORK-PROTOCOL](IDENTITY-FORK-PROTOCOL.md) — Sovereign Merge Rule, schema, staging.
- Alpha School / Moonshots #233 — 2-hour model, mastery, life skills, guides, closed-loop; source of “90% value” definition.
