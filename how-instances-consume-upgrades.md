# How Instances Consume Upgrades from This Template

**Companion-Self template**

When companion-self (this repo) is updated, an instance (e.g. [Grace-Mar](https://github.com/rbtkhn/grace-mar)) can pull those changes **without overwriting its Record**.

**Workspace boundary:** When working on the template, use a workspace where grace-mar is read-only (e.g. `companion-self-and-grace-mar.code-workspace`). Do not modify the instance from this workspace; all instance changes and template merges happen in the instance's own workspace. See [companion-self-bootstrap](companion-self-bootstrap.md) §7.

---

## Safe to Sync from Template

- **Concept docs** — e.g. concept.md, generalized framework
- **Protocol docs** — e.g. identity-fork-protocol (short form or full spec if maintained here)
- **Seed-phase definition** — what seed is, what it produces, that it is the only creation path
- **SELF / self-knowledge, self-curiosity, self-personality / self-skill-think / self-skill-write / self-skill-work / self-evidence / recursion-gate / self-memory templates** — schema and structure only; instance keeps its own copies and updates them to match the template when upgrading
- **Template-level governance** — pipeline rule, knowledge boundary, operating modes (e.g. in AGENTS.md or equivalent in the instance, derived from template guidance)

The instance **compares** template docs and templates with its own, **merges** changes into its files, and runs any validation (e.g. governance checker, validate-integrity). There is **no** automated overwrite of `users/<id>/`.

---

## Never Overwrite with Template

- **`users/<id>/`** — The Record (SELF, self-skill-think, self-skill-write, self-skill-work, self-evidence, etc.) for a real companion. Template has no Record; instance must never replace it with template content.
- **Instance-specific config** — Bot tokens, instance domains, PRP output paths, etc.
- **Instance-only code** — Bot, pipeline scripts, instance tooling.

---

## Process (Recommended)

1. Pull or merge from companion-self (e.g. `git pull origin main` from template remote, or copy specific files).
2. Compare template paths with instance paths (docs, `users/_template/` vs instance’s template or schema docs).
3. Merge changes into the instance’s docs and template files by hand (or with a small sync script that only touches allowed paths).
4. Run instance validation (e.g. governance check, validate-integrity).
5. Do **not** copy template `users/_template/` *over* an existing `users/<id>/` Record — use it only when creating a **new** user directory.

---

## Canonical Template Paths (for instance merge checklist)

When an instance (e.g. Grace-Mar) merges upgrades from companion-self, it should compare and merge **only** these paths. **When companion-self adds or renames files, this list and the template manifest are updated.** Instance merge docs (e.g. grace-mar's `docs/MERGING-FROM-COMPANION-SELF.md`) should align with this list.

**Machine-readable:** The same list is in **`template-manifest.json`** at repo root (paths, descriptions, optional flag, `canonicalAsOf` date). Scripts and CI can diff instance files against it; keep the manifest and this table in sync.

| Path | Description |
|------|-------------|
| `docs/concept.md` | Concept: Record, Voice, education structure, knowledge boundary, invariants, long-term objectives. |
| `docs/identity-fork-protocol.md` | Protocol: Sovereign Merge Rule, schema (SELF, self-skill-*, self-evidence), evidence linking. |
| `docs/seed-phase.md` | Definition of seed phase; what creates initial Record. |
| `docs/long-term-objective.md` | Permanent system rules (democratize Alpha-style education; sovereignty; knowledge boundary). |
| `docs/two-hour-screentime-target.md` | 2-hour design constraint and equivalent metric; what counts as screen time. |
| `docs/instance-patterns.md` | Instance patterns and reference implementation (Grace-Mar variations, analyst contract, staging format). |
| `users/_template/self.md` | SELF schema/structure scaffold for new users only. |
| `users/_template/self-knowledge.md` | IX-A: what they've learned (self-knowledge) scaffold. |
| `users/_template/self-curiosity.md` | IX-B: what they're curious about (self-curiosity) scaffold. |
| `users/_template/self-personality.md` | IX-C: voice, preferences, values (self-personality) scaffold. |
| `users/_template/self-skill-think.md` | THINK (self-skill-think) scaffold. |
| `users/_template/self-skill-write.md` | WRITE (self-skill-write) scaffold. |
| `users/_template/self-skill-work.md` | WORK (self-skill-work) scaffold. |
| `users/_template/self-evidence.md` | Evidence schema/structure scaffold. |
| `users/_template/recursion-gate.md` | Recursive-gate staging scaffold (candidates at the gate). |
| `users/_template/self-memory.md` | Ephemeral context scaffold (optional). |
| `users/_template/self-library.md` | Curated lookup sources scaffold (optional; bounded lookup extension). |

Optional (instance may keep its own and take only selected content): `README.md`, `companion-self-bootstrap.md`, other `docs/` (roadmap, recursive-self-learning-objectives, insights, etc.). **Never overwrite** `users/<id>/` for any real user id.

A small sync script could list these paths and diff/merge them into the instance; it must exclude `users/<id>/` for any real user.

---

## Auditability (bridging the gap)

**Template side:** `template-manifest.json` is the single source of truth for canonical paths and the date they were last updated (`canonicalAsOf`). When the path list or key docs change, update the manifest and commit. An auditor can read the manifest and compare to any companion-self commit.

**Instance side:** When you merge from companion-self, **record in your repo** the template commit (or tag) and date. For example, in `docs/MERGING-FROM-COMPANION-SELF.md` or a small file such as `template-source.json`:

- `companionSelfCommit`: the full git commit hash (or tag) you merged from
- `mergedAt`: date (ISO) or commit hash in the instance repo

An example schema lives in **`docs/template-source.example.json`**; copy to your instance (e.g. repo root or `docs/template-source.json`) and update it after each merge. That gives a verifiable audit trail: "this instance merged from companion-self at this point."

**How to audit:** (1) From companion-self: open `template-manifest.json` at the commit the instance claims it merged. (2) From the instance: read its recorded commit and merged-at. (3) Optionally: instance CI or a script can diff its copy of the canonical paths against the manifest (e.g. fetch manifest from companion-self at the recorded commit, compare paths and optionally checksums). No automated link is required; both sides are independently auditable and can be compared by hand or script.

---

*Companion-Self template · Upgrade consumption*
