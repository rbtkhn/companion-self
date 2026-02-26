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

---

## Examples

- **Chore completed in Skylight (or similar)** — A bridge or webhook sends "chore X completed by profile Y at time Z" as POST activity with `skill_tag: WORK`. Pipeline stages it; caregiver gates; merge creates evidence (e.g. ACT-xxxx) linked to self-skill-work.
- **CSV upload of past events** — User exports calendar or task history to CSV. An instance script or UI maps rows to staged activity (e.g. READ or WORK). User reviews and merges in batches. Record and evidence now reflect history without manual re-entry.
- **Manual "we did X"** — Companion or caregiver posts activity via instance API or UI. Same pipeline: stage → gate → merge. Source is "manual," but the path is the same.

---

## Why it matters

Users should not maintain two worlds. Companion-self is designed so that **messy or scattered input** (different apps, exports, one-off events) can be normalized into one flow and one Record. Ingestion from many sources is a first-class pattern, not an afterthought.
