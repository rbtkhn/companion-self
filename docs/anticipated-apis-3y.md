# Anticipated APIs (Non-LLM) — 3-Year Horizon

**Companion-Self template · Planning**

This doc anticipates which **non-LLM** APIs are likely to be most useful for companion-self users (instances, operators, companions) over the next three years. It informs integration priorities, export schema design, and pipeline contracts. Excludes LLM/chat APIs; focuses on data, content, evidence, and workflow.

---

## 1. Curriculum / learning platforms (READ, mastery)

**What:** APIs that consume the Record (knowledge, curiosity, edge) and return suggested lessons, skills, or practice; and/or report progress (topic mastered, score, time on task) back into the pipeline.

**Why useful:** Closes the loop: Record → curriculum → activity → evidence → Record. Delivers “90% value” with free/low-cost content; 2-hour block is filled with personalized lessons at the right edge.

**Examples (likely to matter 2025–2028):**

- **Khan Academy** — Skills API, progress API; consume profile/edge, return recommended skills or units; report progress back (if available). Widely used; free.
- **IXL** — Similar: diagnostic, recommendations, progress. Paid but common in schools; export could drive “next IXL skill.”
- **Open curriculum / OER** — Standards-aligned content APIs (e.g. state standards, Lexile, subject/topic taxonomies). Map Record knowledge/edge to “next best” content without locking to one vendor.
- **State or district assessment / rostering** — If instances serve schools: roster APIs, assessment results as evidence (read-only import, then stage for merge). Lower priority for pure family product.

**Template/instance role:** Export schema (curriculum_profile) is the main contract. Year 1: stable export. Year 2: one reference integration (e.g. Khan). Year 3: evidence ingestion from curriculum (progress, mastery) with provenance.

---

## 2. Tutor / adaptive learning (READ, WRITE, edge)

**What:** APIs that take the Record (or export) and return “next best action,” practice items, or prompts; optional callback when a session or activity is completed so the instance can stage evidence.

**Why useful:** Replaces or augments in-room tutoring; respects knowledge boundary (tutor suggests, Record stays gated). Fits 2-hour block and edge-driven flow.

**Examples:**

- **Khanmigo or future tutor APIs** — If they expose “suggest lesson from profile” and “activity completed” webhook (non-LLM endpoints), they fit the pull-export → suggest → capture pattern.
- **Open-source tutor / problem banks** — APIs that accept a minimal profile (level, topics, interests) and return problem sets or prompts. Instance stages “we did X” or receives webhook.
- **Writing / feedback services** — APIs that take a prompt + optional context (e.g. “at this level”) and return structured prompts or rubrics; no LLM required if they use rule-based or template-based generation. WRITE evidence still captured by instance.

**Template/instance role:** Same as curriculum: export is the input; optional “activity completed” or “outcome” callback is the return path. Document in integration pattern.

---

## 3. Evidence / artifacts (WORK, WRITE, READ)

**What:** APIs for storing and referencing artifacts (documents, images, links, project outputs) so evidence is not only “we did X” text but links to real work. Optional: portfolio or showcase APIs.

**Why useful:** Record stays evidence-grounded; WORK and WRITE are credible with links to what they built or wrote. Export can include artifact URLs for tutors or admissions.

**Examples:**

- **Object storage (S3, R2, GCS)** — Upload project photos, PDFs, screenshots; store URLs in self-evidence or activity payload. Simple, vendor-neutral.
- **Portfolio / showcase platforms** — If a platform exposes “add item” + “get portfolio URL” APIs, instance could link evidence to portfolio entries. Less standardized; Year 2–3.
- **File/link metadata** — No single API; pattern: store canonical URL + optional checksum; pipeline stages “artifact: url” for merge. Enables future verification.

**Template/instance role:** Schema supports artifact URLs and optional storage contract (e.g. “evidence may include `artifact_url`”). Instance chooses storage; template documents the pattern.

---

## 4. Time / session / 2-hour block (analytics, UX)

**What:** APIs or local logic for session length, screen time, and “2-hour block” tracking so the system (or operator) can see time-in-block and optionally cap or prompt. Non-LLM: timers, device/session APIs, or simple analytics.

**Why useful:** 2-hour design constraint is an equivalent metric; users and operators need visibility and optional guardrails.

**Examples:**

- **Session timers (instance-owned)** — Start/stop session; store duration per day; expose in dashboard or export (e.g. `screen_time_today_minutes`). No external API required; logic in instance.
- **Device or OS APIs** — If running in a managed environment (e.g. school device), device usage or MDM APIs might report “app usage” or “screen time.” Niche; document as optional.
- **Analytics / metrics** — Internal API: GET /api/analytics or daily summary (time in app, activities per skill, evidence count). Feeds operator dashboard and proof architecture.

**Template/instance role:** Template defines optional `screen_time_target_minutes: 120` in export and metrics framework; instance implements timers and analytics APIs.

---

## 5. Project / maker / WORK (life skills)

**What:** APIs that suggest projects, workshops, or “what to build” from the Record (interests, edge); or that report “project completed” back to the instance so WORK evidence can be staged.

**Why useful:** WORK needs structure and evidence; life skills and “afternoon” activities are a core value. External tools can propose work and push completion.

**Examples:**

- **Project / lesson libraries** — Curated lists (e.g. “projects for age X,” “workshop: simple circuits”). API: get projects by topic/level; instance or operator picks and records “we did this.” Could be static JSON or a simple REST “list projects” API.
- **Maker / creation platforms** — If a platform (e.g. Scratch, Arduino education, a workshop app) exposes “project completed” webhook or “get user projects” API, instance can link evidence or pull completion. Fragmented today; document pattern for Year 2–3.
- **Calendar / scheduling** — Block “2-hour learning window” or “WORK project slot”; remind operator or companion. Calendar APIs (e.g. Google Calendar, CalDAV) for read/write of blocks. Useful for ritual and time-bounding.

**Template/instance role:** WORK templates and evidence schema in template; instance integrates one or two project sources and optional webhook for completion. Roadmap Year 2: life skills/WORK templates; Year 3: evidence ingestion from external.

---

## 6. Identity / export / portability

**What:** APIs that consume or produce the Record in a standard form so the companion can move, backup, or hand the Record to another instance or tutor. Not “login with X” but “export/import format.”

**Why useful:** Portable identity is a differentiator; families and schools want to own the Record and plug it into other tools.

**Examples:**

- **Export format as API contract** — GET /api/export returns curriculum_profile (and optionally full Record). Any consumer (curriculum, tutor, other instance) that speaks the schema can use it. Versioning (e.g. v1, v2) for stability.
- **Import / restore** — POST /api/import or “restore from backup” that accepts the same schema. Enables migration and backup. Instance-owned API.
- **OAuth / identity (optional)** — If instances need “login with Google” or “link to school IdP,” that’s an identity API. Lower priority for MVP; document as optional for hosted product.

**Template/instance role:** Template defines export schema and versioning; instance implements GET/POST for export and optional import. No external identity API required for core flow.

---

## 7. Communication / notifications (operator, companion)

**What:** APIs to send lightweight notifications (e.g. “recursion-gate has 3 items,” “weekly summary”) to operator or guardian. Email, push, or in-app.

**Why useful:** Reduces “did you check the queue?” friction; keeps operator in the loop without requiring them to open the app daily.

**Examples:**

- **Email (SendGrid, Resend, SES)** — Transactional: “You have N items in recursion-gate.” Simple, non-LLM.
- **Push (FCM, APNs)** — If instance has a mobile or PWA: “Time for your 2-hour block” or “New activity to review.” Optional.
- **In-app only** — No external API; dashboard shows counts and “last reviewed.” Sufficient for Year 1; add email/push in Year 2 if retention or operator engagement demands it.

**Template/instance role:** Template does not require notifications; instance may add them. Document as optional enhancement.

---

## Summary: priority by year

| Priority | API category | Year 1 | Year 2 | Year 3 |
|----------|--------------|--------|--------|--------|
| **1** | Curriculum / learning (export consumer, progress back) | Export schema; one consumer path | One reference integration (e.g. Khan); callback pattern | Evidence ingestion; closed-loop |
| **2** | Tutor / adaptive (export in, suggestion out; optional callback) | Same export contract | Document; optional tutor API | Optional low-cost tutor path |
| **3** | Evidence / artifacts (storage, URLs) | Schema supports artifact_url | Instance storage + link in evidence | Portfolio/shadow if needed |
| **4** | Time / session / 2-hour | Optional screen_time in export; instance timer | Analytics API; operator dashboard | Metrics framework |
| **5** | Project / WORK (suggest, complete webhook) | WORK evidence schema | Project templates; optional webhook | Evidence from external WORK tools |
| **6** | Identity / export (versioned, import) | Stable export; versioning | Import/restore if needed | Certification/conformance |
| **7** | Notifications | — | Optional email/push | If operator engagement needs it |

**Non-LLM focus:** All of the above avoid reliance on LLM APIs for the integration contract. LLMs can still be used inside curriculum or tutor products; companion-self’s integration points are export (out) and evidence/callback (in), which can be implemented with REST, webhooks, and structured JSON.

---

*Companion-Self template · Anticipated APIs (3-year horizon)*
