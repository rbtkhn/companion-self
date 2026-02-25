# How Instances Consume Upgrades from This Template

**Companion-Self template**

When companion-self (this repo) is updated, an instance (e.g. [Grace-Mar](https://github.com/rbtkhn/grace-mar)) can pull those changes **without overwriting its Record**.

**Workspace boundary:** When working on the template, use a workspace where grace-mar is read-only (e.g. `companion-self-and-grace-mar.code-workspace`). Do not modify the instance from this workspace; all instance changes and template merges happen in the instance's own workspace. See [COMPANION-SELF-BOOTSTRAP](COMPANION-SELF-BOOTSTRAP.md) §7.

---

## Safe to Sync from Template

- **Concept docs** — e.g. CONCEPT.md, generalized framework
- **Protocol docs** — e.g. IDENTITY-FORK-PROTOCOL (short form or full spec if maintained here)
- **Seed-phase definition** — what seed is, what it produces, that it is the only creation path
- **SELF/SKILLS/EVIDENCE/PENDING-REVIEW/MEMORY templates** — schema and structure only; instance keeps its own copies and updates them to match the template when upgrading
- **Template-level governance** — pipeline rule, knowledge boundary, operating modes (e.g. in AGENTS.md or equivalent in the instance, derived from template guidance)

The instance **compares** template docs and templates with its own, **merges** changes into its files, and runs any validation (e.g. governance checker, validate-integrity). There is **no** automated overwrite of `users/<id>/`.

---

## Never Overwrite with Template

- **`users/<id>/`** — The Record (SELF, SKILLS, EVIDENCE, etc.) for a real companion. Template has no Record; instance must never replace it with template content.
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

## Optional: Template Paths to Copy When Upgrading

Instances may treat these as the canonical list of template paths safe to compare and merge (structure only; no Record data):

- `README.md` — optional; instance may keep its own README and take only the template vs instance distinction and links.
- `docs/CONCEPT.md`
- `docs/IDENTITY-FORK-PROTOCOL.md`
- `docs/SEED-PHASE.md`
- `users/_template/SELF.md`, `SKILLS.md`, `EVIDENCE.md`, `PENDING-REVIEW.md`, `MEMORY.md` — as schema/structure reference or scaffold for **new** users only.

A small sync script could list these paths and diff/merge them into the instance; it must exclude `users/<id>/` for any real user id.

---

*Companion-Self template · Upgrade consumption*
