# Evaluation and response: template-repo feedback

**Companion-Self template · Implementable actions for approve/deny**

This doc evaluates external feedback on the template repo and turns it into **specific implementable actions** for you to approve or deny. Each action is marked **Approve / Deny / Defer** with rationale and scope.

---

## Summary of feedback (acknowledged)

- **Template vs instance split** and **Sovereign Merge Rule** are correct and well documented.
- **template-manifest.json** is the right audit mechanism; semantics (date/version) need tightening.
- **Merge does not write to skill files** (THINK/WRITE/WORK); only evidence + IX. This contradicts the schema and Week 4 plan (“optionally append to matching self-skill-*”).
- **Staging** uses a fixed skill→IX mapping; feedback suggests rule-based cues and multi-write (defer or scope down).
- **Evidence** IDs and parsing could be more robust; cross-link validation is missing.
- **Demo user** is hardcoded; multi-user would need allowlist and query/header.
- **Template versioning** (tags, template-version.json) would make upgrades auditable.
- **Repo hygiene**: .DS_Store is tracked; LICENSE, SECURITY.md, optional CODE_OF_CONDUCT, basic CI suggested.
- **Template Integrity checker** script suggested.

---

## Implementable actions (approve / deny / defer)

### 1) Merge: write to skill files as well as IX + evidence

**Proposal:** When merging an approved candidate, append a bullet to the **matching skill file** (THINK → self-skill-think.md, WRITE → self-skill-write.md, WORK → self-skill-work.md) in addition to self-evidence and the IX file. Use the same evidence id and a consistent line format (e.g. `raw_text — ACT-xxx`).

**Evaluation:** **Approve.** The schema and concept doc treat THINK/WRITE/WORK as first-class; project-6week Week 4 task 4.3 already says “(3) optionally append to matching self-skill-*.” Today merge only does (1) and (2). Implementing (3) aligns code with the protocol and makes “skills grow” with activity.

**Implementable action:**

- [ ] **Action A1:** In `app/schema/record.js`, inside `mergeCandidate`, after appending to the dimension file (step 2), add step 2b: map `candidate.skill_tag` to the skill file (THINK → self-skill-think.md, WRITE → self-skill-write.md, WORK → self-skill-work.md), choose a section header (e.g. “Activity” or reuse the first ## in the file), and call `appendBulletToFile(dimPath, sectionHeader, `${candidate.raw_text} — ${evidenceId}`)` for the **skill** file path. Ensure skill files exist (create empty or rely on users/demo and eval-fixture already having them).
- [ ] **Action A2:** Update `docs/schema-record-api.md` “Merge outcome (good)” to state that merge writes to evidence, **one dimension file** from suggested_ix_section, **and the matching skill file** from skill_tag.
- [ ] **Action A3:** Run `node scripts/run-eval-fixtures.js` and extend fixtures if needed so that after approve, the corresponding self-skill-*.md file contains the new bullet.

**Scope:** `app/schema/record.js`, `docs/schema-record-api.md`, optionally `scripts/run-eval-fixtures.js`. No change to stage.js or API surface.

---

### 2) Staging: rule-based IX cues and multi-write

**Proposal:** Add a small rule-based classifier on `raw_text` (e.g. “I learned/understood…” → IX-A, “I’m curious/wonder…” → IX-B, “I prefer/I’m the kind of person…” → IX-C); if no match, keep current skill→IX default. Optionally allow one candidate to propose entries for multiple IX sections and/or skills.

**Evaluation:** **Defer** (or **Approve in minimal form**). Improving IX targeting is valuable, but:
- Rule-based cues are heuristic and may be wrong; the **human at the gate** already corrects placement by approving/rejecting. suggested_ix_section is “suggested,” not final.
- Multi-write (one candidate → multiple IX lines) complicates merge semantics (one evidence entry, multiple dimension lines?) and receipt format. The current contract is “one approve = one evidence entry + one dimension line.”
- A **minimal** approve could be: add 3–5 keyword rules in `stage.js` that **override** the default SKILL_MAP suggested_ix_section when `raw_text` matches (e.g. “learned/understood/realized” → IX-A; “curious/wonder/want to try” → IX-B; “prefer/love/hate/I’m the kind of” → IX-C). No multi-write; one candidate still maps to one suggested_ix_section.

**Implementable action:**

- [ ] **Action B1 (minimal):** In `app/pipeline/stage.js`, before calling `createCandidate`, run a small function `suggestIxFromRawText(raw_text, skill_tag)` that returns `{ mind_category, suggested_ix_section }`. Rules: if `raw_text` matches (e.g. regex or includes) “learned”|“understood”|“realized” → IX-A; “curious”|“wonder”|“want to try”|“interested in” → IX-B; “prefer”|“love”|“hate”|“I’m the kind of”|“voice” → IX-C. Else use existing SKILL_MAP[skill_tag]. Use that result in createCandidate. Document in stage.js and optionally in schema-record-api that “staging may use simple text cues to suggest IX section; companion gates at review.”
- [ ] **Action B2 (defer):** Multi-write (one candidate → multiple IX/skill lines) and full “classifier” — leave for a later iteration or instance (e.g. Grace-Mar analyst).

**Scope:** `app/pipeline/stage.js` only for B1. No schema change.

---

### 3) Evidence: canonical format, parsing fallback, and cross-link validation

**Proposal C (canonical format):** Use a single machine-parsable format for new evidence lines, e.g. `- ACT-2026-02-27T14-22-10Z_ab12cd | THINK | summary text`, and have `parseEvidenceEntries` accept that first, then fall back to the current em-dash format.

**Proposal D (linking integrity):** When appending to IX and skill files, always include `— ACT-...` (already done for IX; add for skill in Action A1). Add a validator that ensures every ACT-* referenced in IX/skill files exists in self-evidence.md.

**Evaluation:** **Approve C in conservative form; Approve D.**

- **C:** Today we **write** em-dash format in `appendEvidenceEntry`. The comment in record.js mentions a pipe format but the code only parses em-dash. Either: (1) **Switch write to pipe format** and parse pipe first, with fallback to em-dash for legacy lines, or (2) **Keep writing em-dash** and add **parse fallback** for a second supported format (pipe) so both are valid. Option (1) is a breaking change for any existing self-evidence.md; option (2) is backward compatible. **Recommend (2):** keep writing em-dash; extend `parseEvidenceEntries` to also recognize a pipe line (e.g. `- ACT-xxx | THINK | summary`) so future or instance-generated evidence can use either. Document the two supported formats in schema-record-api.
- **Evidence ID collision:** Feedback is right that `ACT-${suffix}` from candidate id can theoretically collide. Making evidence id deterministic (e.g. `ACT-${date}-${shortId}` or timestamp-based) reduces collision and helps audit. **Approve:** when generating evidenceId in mergeCandidate, use a format that includes date and a short unique suffix (e.g. `ACT-${today}-${candidate.id.slice(-8).replace(/\D/g, '')}` or use a nano-id), and document in schema-record-api.
- **D:** Validator script that (1) parses self-evidence.md for all ACT-* ids, (2) scans IX and skill files for `ACT-*` references, (3) reports orphans (referenced but not in evidence) and unreferenced (in evidence but not in IX/skills is optional). **Approve** as a separate script (e.g. `scripts/validate-evidence-links.js`) or as part of a broader “Template Integrity” checker.

**Implementable actions:**

- [ ] **Action C1:** In `app/schema/record.js`, in `mergeCandidate`, set `evidenceId = \`ACT-${today.replace(/-/g, '-')}-${candidate.id.slice(-9).replace(/\D/g, '')}\` or similar (date + short suffix) to reduce collision and improve readability. Document in JSDoc and schema-record-api.
- [ ] **Action C2:** In `parseEvidenceEntries`, add a second regex branch: if line matches `- ACT-(\w+)\s*\|\s*(THINK|WRITE|WORK)\s*\|\s*(.+)`, push `{ id, summary: trim(m[3]), date: '' or from context, skill_tag: m[2] }`. For pipe format, date might be omitted or in a fourth column; document. Keep existing em-dash parsing so both formats are valid.
- [ ] **Action D1:** Add `scripts/validate-evidence-links.js`: read users/demo (or a given user dir), parse self-evidence for ACT-* ids, grep IX and self-skill-* files for ACT-* refs, print list of referenced ids and list of evidence ids; report any ACT-* in files that’s not in evidence. Optional: report evidence ids that are never referenced. Document in evaluation-design-and-regression or how-instances-consume-upgrades.

**Scope:** `app/schema/record.js`, `docs/schema-record-api.md`, new script, docs.

---

### 4) Multi-user / allowlist (query param or header + allowed-users.json)

**Proposal:** Support `?user=grace-mar` or header `X-User-Id`, default to `demo`. Add `app/config/allowed-users.json` in the template (e.g. `["demo"]`) so the template repo never writes to a real user dir by mistake.

**Evaluation:** **Approve with narrow scope.** For the **template** repo, the 6-week plan is “single-user/demo ok”; multi-user is out of scope. So the main benefit is (1) not accidentally writing to a real user when testing, and (2) a clear path for instances to enable multi-user later. Allowlist + default demo is safe and small.

**Implementable actions:**

- [ ] **Action E1:** Add `app/config/allowed-users.json` with content `["demo"]`. In `app/server.js` (and any code that resolves userId), read userId from `req.query.user` or `req.headers['x-user-id']`, default to `"demo"`. If userId is not in allowed-users.json, respond 403 or 400 with a clear message (“User not in allowed list; template supports demo only.”). Load allowed list once at startup.
- [ ] **Action E2:** In `app/pipeline/stage.js`, `merge.js`, `edge.js`, `curriculum-profile.js`, pass through a userId argument (from server) instead of hardcoding DEMO_USER. Server resolves userId and passes it into the pipeline/export.
- [ ] **Action E3:** Document in readme-student-app.md that the app runs as demo only unless allowed-users is changed (and that instances can add users and use query/header for multi-user).

**Scope:** `app/server.js`, `app/config/allowed-users.json`, pipeline and export call sites, readme.

---

### 5) Template versioning and manifest semantics

**Proposal:** Add template releases/tags (e.g. template-v0.2.0), add `template-version.json` at repo root with templateVersion, releasedAt, gitTag; update instance guidance to record commit hash + tag on merge.

**Evaluation:** **Approve.** Makes upgrades auditable and avoids “canonicalAsOf is stale” confusion.

**Implementable actions:**

- [ ] **Action F1:** Add `template-version.json` at repo root: `{ "templateVersion": "0.2.0", "releasedAt": "2026-02-27", "gitTag": "template-v0.2.0" }`. Update it (or a script) when cutting a template release. Document in how-instances-consume-upgrades that instances should record `templateVersion` and `gitTag` (or commit) when merging.
- [ ] **Action F2:** In `template-manifest.json`, set `canonicalAsOf` to the same date as the current release (e.g. 2026-02-27) and add a note in the description or a short “version” field that ties to template-version.json. Optionally add `"templateVersion": "0.2.0"` in the manifest for one-place consistency.
- [ ] **Action F3:** Tag current state as `template-v0.2.0` (or next semver) after the version file and manifest are in place. Document in how-instances-consume-upgrades: “Pull from a template tag (e.g. template-v0.2.0) and record the tag and commit in your instance.”

**Scope:** New file, manifest update, docs, git tag (you run tag locally).

---

### 6) Repo hygiene: .DS_Store, LICENSE, SECURITY.md, CODE_OF_CONDUCT, CI

**Proposal:** Remove tracked .DS_Store; add LICENSE, SECURITY.md, optional CODE_OF_CONDUCT; basic GitHub Actions (lint + node test).

**Evaluation:** **Approve** .DS_Store removal and LICENSE/SECURITY; **optional** CODE_OF_CONDUCT and CI.

**Implementable actions:**

- [x] **Action G1:** Run `git rm --cached .DS_Store` and `git rm --cached library/.DS_Store` (if path exists), commit. Ensure .gitignore keeps .DS_Store so they stay untracked.
- [x] **Action G2:** Add a LICENSE file (e.g. MIT or Apache-2.0) at repo root. You choose license.
- [x] **Action G3:** Add SECURITY.md with a short “How to report a vulnerability” (e.g. open an issue or contact maintainer; no confidential disclosure required unless you want it).
- [x] **Action G4 (optional):** Add CODE_OF_CONDUCT.md (e.g. Contributor Covenant) if you want it.
- [x] **Action G5 (optional):** Add `.github/workflows/ci.yml`: run `node scripts/run-eval-fixtures.js` and optionally `npm run lint` if you add a lint script. Keeps template green on push.

**Scope:** Repo root, .github/workflows. No app code.

---

### 7) Template Integrity checker script

**Proposal:** Add `scripts/validate-template.js` (or similar) that: (1) all paths in template-manifest.json exist, (2) canonicalAsOf is not older than last commit touching those paths (or at least documented), (3) no forbidden files tracked (e.g. .DS_Store).

**Evaluation:** **Approve.** Low effort, high confidence for template consumers.

**Implementable actions:**

- [x] **Action H1:** Add `scripts/validate-template.js`: read template-manifest.json, for each path in paths[], check `fs.existsSync(path)` (from repo root); print missing paths and exit 1 if any. Optionally check that .DS_Store is not in `git ls-files`; optionally check canonicalAsOf or template-version.json exists. Document in how-instances-consume-upgrades and/or evaluation-design-and-regression.
- [x] **Action H2:** Run the script in CI (if Action G5 is approved) so every push validates manifest paths.

**Scope:** New script, optional CI step, docs.

---

## “If you do only 3 things” (feedback’s ROI)

1. **Merge writes to skill files** (Action A1–A3).
2. **Evidence: canonical/robust IDs + parsing fallback + cross-link validator** (Actions C1–C2, D1).
3. **Template versioning + manifest semantics** (Actions F1–F3).

---

## Optional next step (feedback)

The feedback offered a “sync harness” for the instance (grace-mar): pull template at a tagged version, diff only allowed paths, open a PR in the instance with a checklist + receipts. That is **out of scope** for this template repo; it would live in the instance or in a separate tool. No action in this doc.

---

## Approval checklist (for you)

Use this to approve/deny each block:

| # | Action block | Approve / Deny / Defer | Notes |
|---|--------------|------------------------|--------|
| 1 | Merge → skill files (A1–A3) | | |
| 2 | Staging rule-based IX cues (B1); defer multi-write (B2) | | |
| 3 | Evidence format + parsing + validator (C1–C2, D1) | | |
| 4 | Multi-user allowlist (E1–E3) | | |
| 5 | Template versioning (F1–F3) | | |
| 6 | Repo hygiene (G1–G5) | | |
| 7 | Template Integrity script (H1–H2) | | |

Once you approve, implementation can proceed in that order (1 → 7) or in parallel where independent.
