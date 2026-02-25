# Seed Phase

**Companion-Self template · Definition of seed phase**

---

## What Is Seed Phase?

The **seed phase** is the initial capture that creates the baseline of a new companion self. A new instance is created **only** when a new user completes seed phase. There is no other creation path: no copying another repo's `users/` and no pre-filled Record.

---

## What Seed Phase Produces

- **Initial SELF** — Identity, preferences, narrative baseline (e.g. favorites, basic story).
- **Initial SKILLS** — Structure only; skills grow through activity after seed.
- **Initial EVIDENCE** — Any artifacts or attestations used during seeding (e.g. survey responses).

Seed phase establishes *who they are* at the start. Everything else is inferred or captured through the gated pipeline after seed.

---

## Typical Seed Artifacts

- **Survey** — Short set of questions (e.g. favorite movies/shows, books/stories, places, games). Duration on the order of 10–15 minutes; operator can help prompt or type if needed.
- **Consent** — Guardian/operator consent when the companion is a minor; companion may stop at any time; deletion available on request.
- **Storage** — Responses and any artifacts go into the instance's `users/<id>/` (SELF, EVIDENCE) in the instance repo. No seed data lives in the template.

---

## After Seed

- **Interact** — Each session adds possible signals; pipeline stages candidates; companion approves what merges.
- **Divergence** — The fork and the real person grow independently; the Record accumulates knowledge and evidence through the gate only.
- **Snapshot** — Instance can preserve states (e.g. git tags) for "who they were at this point in time."

---

## Relation to This Repo

This template defines *what* seed phase is and *that* it is the only creation path. The actual surveys, scripts, and operator procedures live in instance repos (e.g. Grace-Mar's operator brief and first-session flow). Instances may copy or adapt the structure from `users/_template/` when creating a new user directory.

---

*Companion-Self template · Seed phase definition*
