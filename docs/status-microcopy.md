# Status Microcopy

**Purpose:** Define a docs-first framework for status, loading, and process language across companion-self surfaces and downstream instances.

**Status:** Normative guidance for wording and future UI implementation. This document does not require a frontend framework and does not itself introduce a shared code module.

---

## Why this exists

Status language is not cosmetic filler. It teaches the operator or companion what kind of process is happening, how much authority that process has, and what mood the product should create while waiting.

Good status microcopy should make process feel:

- legible
- bounded
- emotionally coherent
- governance-aware

It should not create a false impression of hidden sovereignty, memory, or merge authority.

---

## Core rule

**Status language should communicate lane, authority, and mood at once.**

Every phrase should answer three questions:

1. What kind of process is happening?
2. What authority does that process actually have?
3. What emotional posture should the surface create?

---

## Anti-principles

Do not use status language that implies any of the following when it is not true:

- a merge is happening when the system is only staging or reviewing
- memory is being updated when the system is only reading or retrieving
- hidden autonomous judgment beyond the documented workflow
- companion-facing interiority that belongs to operator tooling or work execution
- mystical or omniscient cognition where the actual process is lookup, routing, validation, or waiting on I/O

Short version:

**No fake merge. No fake memory. No fake sovereignty.**

---

## Surface split

Different surfaces should not share one undifferentiated vocabulary.

| Surface | What the wording should optimize for |
|---------|--------------------------------------|
| **Companion-facing chat** | warmth, clarity, boundedness, low cognitive load |
| **Family / operator chrome** | precise operational state, trust, and calm orientation |
| **Governance / review** | correctness of authority and decision state |
| **Lookup / grounded answer flows** | truthful provenance and bounded knowledge |
| **Work execution surfaces** | operational clarity without pretending work output is Record truth |
| **Maintenance** | quiet integration, health checks, and closure |
| **Errors** | explicit failure without panic or mystification |

---

## Plain vs expressive language

Use **plain operational language** when:

- the action has governance consequences
- the user must understand exact authority
- the system is in an error or validation state
- the surface is operator-facing or review-heavy

Use **expressive language** only when:

- the operation is low-risk
- the emotional tone matters to the product experience
- the phrase still truthfully describes the lane
- the wording cannot be mistaken for a merge, memory write, or hidden reasoning claim

Rule of thumb:

- governance and validation: prefer plain
- companion chat and low-risk waiting: expressive is allowed
- expressive must still be truthful

---

## Lane taxonomy

This taxonomy is the shared vocabulary for future implementations.

### `chat`

- **Actual process:** waiting for or formulating a companion-facing reply
- **Authority:** no merge authority; response only
- **Tone:** warm, light, low-friction
- **Good examples:**
  - `Listening`
  - `Finding the thread`
  - `Getting ready to answer`
- **Avoid:**
  - `Rewriting memory`
  - `Deciding what matters`

### `lookup`

- **Actual process:** searching outside the current profile, library, or runtime context
- **Authority:** retrieval only; not Record truth by itself
- **Tone:** concrete, transparent, trustworthy
- **Good examples:**
  - `Looking it up`
  - `Checking sources`
  - `Tracing the answer`
- **Avoid:**
  - `Learning this now`
  - `Adding this to memory`

### `grounded_record`

- **Actual process:** checking the existing Record, profile, or grounded excerpts
- **Authority:** read-only use of documented material
- **Tone:** exact, calm, provenance-aware
- **Good examples:**
  - `Checking the Record`
  - `Reading what is already documented`
  - `Grounding in the current profile`
- **Avoid:**
  - `Remembering more`
  - `Updating the self`

### `gate_review`

- **Actual process:** staging, comparing, reviewing, approving, rejecting, or waiting for approval
- **Authority:** governance-aware; may stage or review, but approval state must be explicit
- **Tone:** plain, exact, non-poetic
- **Good examples:**
  - `Staging for review`
  - `Waiting for approval`
  - `Reviewing pending changes`
  - `Applying approved changes`  # only when an actual merge/apply is occurring
- **Avoid:**
  - `Committing this to identity`  # unless that exact governed step is truly happening
  - `Saving to memory`

### `work_execution`

- **Actual process:** drafting, synthesis, tooling, runbooks, planning, or operator-facing work
- **Authority:** instrumental execution; not Record truth by itself
- **Tone:** capable, lucid, non-mystical
- **Good examples:**
  - `Drafting`
  - `Synthesizing`
  - `Outlining`
  - `Grounding the draft`
- **Avoid:**
  - `Becoming smarter`
  - `Thinking for you`

### `maintenance`

- **Actual process:** bounded upkeep, validation, cleanup, warmup, or closeout
- **Authority:** maintenance only; no implied merge unless one is actually running
- **Tone:** quiet, settling, low-stimulus
- **Good examples:**
  - `Settling continuity`
  - `Checking integrity`
  - `Tidying the runtime`
  - `Preparing re-entry`
- **Avoid:**
  - `Rebuilding the self`
  - `Reorganizing identity`

### `error`

- **Actual process:** failed fetch, invalid state, blocked action, or missing prerequisite
- **Authority:** explicit failure state
- **Tone:** plain, specific, steady
- **Good examples:**
  - `Could not load the Record`
  - `Review queue unavailable`
  - `Validation failed`
- **Avoid:**
  - `Something weird happened`
  - `The system got confused`  # unless deliberately companion-facing and low stakes

---

## Good vs bad examples

| Situation | Good | Bad |
|-----------|------|-----|
| fetching grounded profile context | `Checking the Record` | `Remembering who you are` |
| external search | `Looking it up` | `Learning this` |
| queueing a change | `Staging for review` | `Adding this to the self` |
| merge button after approval | `Applying approved changes` | `Updating memory` |
| work drafting | `Drafting with references` | `Thinking deeply` |
| maintenance run | `Checking integrity` | `Rewriting the system` |

---

## Default mood guidance

| Lane | Default mood |
|------|--------------|
| `chat` | warm, quick, lightly companionable |
| `lookup` | transparent, exact |
| `grounded_record` | calm, anchored |
| `gate_review` | sober, explicit |
| `work_execution` | focused, operational |
| `maintenance` | quiet, settling |
| `error` | steady, specific |

Mood may vary by product, but it should never outrun the truth of the lane.

---

## Future implementation notes

This document is docs-first. A later code pass may implement shared microcopy using:

- a small status dictionary or JSON table
- lane-specific helper functions
- per-surface overrides for companion-facing vs operator-facing tone

Likely implementation points in the template repo:

- `app/public/*.html`
- `app/public/assets/app.js`
- any future shared client helper that centralizes UI strings

That later pass should preserve the lane taxonomy in this document rather than inventing ad hoc strings page by page.

---

## Downstream instances

Instances such as Grace-Mar may adapt this framework to stronger local architecture, especially where:

- Record vs Voice distinctions are explicit
- gating and merge authority are central to the product
- chat-first constraints discourage decorative wait states
- operator and companion surfaces have very different voice requirements

The adaptation should preserve the core rule while narrowing phrases to the local governance model.
