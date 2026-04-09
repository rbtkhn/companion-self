# Forced Absorption

Companion-Self template · Named risk pattern

---

## Definition

**Forced absorption** is the risk that unreviewed content enters canonical state through convenience paths — passive indexing, infrastructure-level defaults, or tooling that collapses draft material into governed truth without an explicit human decision.

The pattern is borrowed from financial regulation: a rule change that silently forces downstream holders to absorb risk they never agreed to. In companion-self, the downstream holder is the Record. The risk is that retrieval, synthesis, prepared context, or agent-generated content becomes Record fact without passing through the governed pipeline.

---

## Standing line

> Identity never enters canonical state through convenience paths. Only governed review and authorized merge may change the Record.

This restates the **Sovereign Merge Rule** (the agent may stage; it may not merge) and the **change-review pipeline** (meaningful revision becomes a visible review object before governed state is updated) as a single defensive principle. The emphasis is on what the system must *prevent*, not what it must *do*.

---

## How the existing architecture defends against it

Companion-self already has structural defenses. This doctrine names the risk they protect against.

| Defense | Where it lives | What it prevents |
|---------|----------------|------------------|
| **Sovereign Merge Rule** | [AGENTS.md](../AGENTS.md) (instances), change-review decision rule 4 | Agent or automation writing directly to governed state |
| **Proposal-first workflow** | [change-review.md](change-review.md), [state-proposals.md](state-proposals.md) | State changes that bypass structured review objects |
| **Authority map** | [authority-map.md](authority-map.md), `config/authority-map.json` | Unauthorized actors writing to governed surfaces |
| **Source-of-truth order** | [source-of-truth.md](source-of-truth.md), `config/source-of-truth.json` | Prepared context or evidence overriding governed state |
| **Three-layer state model** | [state-model.md](state-model.md), [governed-state-layer.md](governed-state-layer.md) | Collapsing evidence or prepared context into canonical state |
| **Observability** | [observability.md](observability.md), `scripts/build-observability-report.py` | Invisible state transitions that leave no audit trail |
| **Legible surfaces** | [legible-surfaces.md](legible-surfaces.md), [action-receipts.md](action-receipts.md) | Meaningful operations that leave no inspectable trace |

---

## Convenience paths to watch for

These are patterns that could bypass governed review if not guarded:

1. **Retrieval treated as authorization.** An agent retrieves content from evidence or prepared context and presents it as Record truth. Retrieval is a read operation, not a governance decision.
2. **Synthesis treated as incorporation.** An agent synthesizes across evidence and the synthesis enters governed state without a proposal object. Synthesis is analytical work, not a merge.
3. **Prepared context promoted without review.** A prepared-context object (normalized, staged, agent-generated) is treated as governed state because it looks clean and well-structured. Prepared context is input to review, not output of review.
4. **Infrastructure defaults that widen write surfaces.** A new script, integration, or export path writes to a governed surface without checking authority. The authority map exists to catch this; new tooling must be authority-aware.
5. **Template upgrades that silently override instance state.** A template version bump changes governed-surface behavior without triggering a change proposal in the instance. See [how-instances-consume-upgrades.md](../how-instances-consume-upgrades.md) and the compatibility contract in [template-version.json](../template-version.json).

---

## What this doctrine does not add

This is a named risk pattern, not new machinery. It does not:
- Create new governance surfaces (the existing five docs above cover the territory)
- Add new terminology beyond "forced absorption" and "convenience path"
- Replace or override the Sovereign Merge Rule, change-review pipeline, or authority map
- Require new scripts or validators (existing `build-observability-report.py`, `validate-change-review.py`, and `check-authority.py` already enforce the pattern)

If a convenience-path violation is detected in practice, that creates demand for targeted validator extensions. Until then, the existing defenses are structural and sufficient.

---

## Cross-references

- [change-review.md](change-review.md) — governed self-revision doctrine
- [architectural-principles.md](architectural-principles.md) — §2 branch/fork/mainline (the test: "Can you point to the status field that distinguishes this data from governed truth?")
- [authority-map.md](authority-map.md) — who may write what
- [observability.md](observability.md) — inspectability without trusting agent self-report
- [legible-surfaces.md](legible-surfaces.md) — meaningful actions should leave a trace

---

Companion-Self template · Forced absorption v1
