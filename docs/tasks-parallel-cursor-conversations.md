# Two parallel tasks for separate Cursor conversations

**Companion-Self template · ~15–30 minutes each, zero file overlap**

Use **Conversation A** for Task 1 and **Conversation B** for Task 2 in parallel. They touch different files so you can run both at once and merge changes after.

---

## Task 1: Schema and spec consistency (docs + schema code)

**Scope (only these files):** `app/schema/record.js`, `docs/schema-record-api.md`, `docs/project-6week-coding.md`

**Goal:** Align JSDoc and docs with the actual schema and add the regression step to the 6-week plan so spec and code stay in sync.

**Subtasks:**

1. **Fix JSDoc in `app/schema/record.js`**  
   The `Record` typedef still says `selfSkillRead` (legacy READ name). The runtime uses `selfSkillThink` (THINK). Update the typedef so it lists `selfSkillThink` (and remove or correct `selfSkillRead`) so JSDoc matches the returned object.

2. **Document default SKILL_MAP in `docs/schema-record-api.md`**  
   The template’s staging logic maps: THINK → IX-A (knowledge), WRITE → IX-C (personality), WORK → IX-B (curiosity). This is only in code (`app/pipeline/stage.js`). Add one sentence or a small table in the schema doc (e.g. in or after “Recursive-gate shape”) that states this default mapping so readers and agents don’t have to infer it from code.

3. **Add regression step to `docs/project-6week-coding.md`**  
   After changing schema or pipeline (Weeks 1, 2, or 4), the project should run the eval fixtures to avoid regressions. Add a short “Regression” note or bullet: e.g. “After schema or pipeline changes (Weeks 1, 2, 4), run: `node scripts/run-eval-fixtures.js`.” Place it in the Success section of the relevant week(s), or add a single “Regression” subsection near the top that points to [Evaluation design and regression](evaluation-design-and-regression.md).

**Acceptance criteria:**

- `record.js` typedef uses `selfSkillThink` (no misleading `selfSkillRead`).
- Schema doc explicitly states the default skill → dimension mapping (THINK→IX-A, WRITE→IX-C, WORK→IX-B).
- Project-6week doc tells the reader to run the eval script after schema/pipeline work; link to evaluation-design-and-regression if appropriate.
- `node scripts/run-eval-fixtures.js` still passes after your edits.

**Do not change:** Any other files (no pipeline logic, no other docs, no frontend).

---

## Task 2: Student UI accessibility and focus polish

**Scope (only these files):** `app/public/*.html`, `app/public/assets/style.css` (and `app/public/assets/app.js` only if needed for dynamic ARIA/live regions)

**Goal:** Improve accessibility and keyboard usability of the student UI (dashboard, activity form, review, export) so the app is clearer for screen-reader and keyboard users.

**Subtasks:**

1. **ARIA and semantics**  
   Add or fix ARIA where it helps: e.g. `aria-label` or `aria-describedby` on the activity textarea and skill dropdown; `aria-label` on Approve/Reject buttons in review; ensure section headings and “Pending” count are in a sensible landmark/heading order. Don’t add ARIA that duplicates visible text; only add what’s missing for context.

2. **Form feedback announcement**  
   On the activity page, success and error messages (e.g. “Submitted. Go to review to approve.” or the error string) should be announced to screen readers. Use `role="alert"` or `aria-live="polite"` on the message container (e.g. `#message`) so when the text is updated after submit, it’s announced. On the review page, if there are status or error messages, ensure they’re also announced when they appear or change.

3. **Focus visibility**  
   In `app/public/assets/style.css`, ensure interactive elements (links, buttons, inputs, textarea, select) have a visible focus style so keyboard users can see focus. Use `:focus-visible` (with a fallback for older browsers if you want) and avoid removing outline without a replacement (e.g. outline + box-shadow, or a clear border/background change).

**Acceptance criteria:**

- Activity form and review controls have appropriate labels/ARIA so purpose is clear.
- Submitting the activity form (success or error) results in the message being announced.
- All focusable elements have a visible focus indicator when navigated by keyboard.
- No changes to backend, schema, or docs; only `app/public/` as above.

**Do not change:** `app/server.js`, `app/schema/`, `app/pipeline/`, `docs/`, or any file outside `app/public/`.

---

## After both tasks

- Run `node scripts/run-eval-fixtures.js` (Task 1 may touch schema; fixture script should still pass).
- Manually check: load dashboard, submit an activity, approve/reject one candidate, and tab through the UI to confirm focus and announcements.
- Commit each task in its own commit (or merge the two branches) so the two parallel workstreams stay traceable.
