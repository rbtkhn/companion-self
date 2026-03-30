# Git branch hygiene (operator)

**Purpose:** A **small, repeatable** check so you do not lose track of branches or confuse **“merge into `main`”** with **Record gate merge** (identity pipeline). Use it during **hey** (startup) and **hey night** (closeout) rhythms when you want a quick **branch snapshot** (read-only triage). Contract detail lives in the existing specs (paths still named `good-morning-brief-spec.md` / `good-night-brief-spec.md` on disk until renamed): [startup / hey rhythm](../../good-morning-brief-spec.md), [closeout / hey night](../../good-night-brief-spec.md). The **git** rules here stay the same across instances.

**Not the same as template vs instance alignment.** Audits that compare **template and instance** (or fork isolation, reconciliation code) answer a different question than **local git** branches. **Branch hygiene** = **`main` vs feature branches** only.

**Not the same as splitting operator menus:** If your instance separates **template/boundary audit** from **repository hygiene**, put **branch snapshot** with **repository hygiene**, not with template alignment.

---

## When you merge branches (git)

Merge a **git branch** when that line of work should **become part of `main`** (or your chosen target branch) and is **ready** (reviewed, tested if you care, not half-finished).

You do **not** merge every day by habit — you **triage** often; you **merge** when a unit of work is done.

**Different from Record:** Merging **candidates** into **SELF / EVIDENCE** uses **RECURSION-GATE** and your instance’s approved merge path (e.g. `process_approved_candidates.py`) — companion approval. **Git merge** is **repository history** only. See [Identity Fork Protocol](../../identity-fork-protocol.md).

---

## Branch snapshot (read-only)

**Commands:**

```bash
git status -sb
git branch -vv
```

**Plain-language rules:**

| What you see | Meaning | Typical action |
|--------------|---------|----------------|
| Only `* main` and `main` tracks `origin/main` | No extra branches | **None** — “branch hygiene: clean.” |
| Branch listed, `[gone]` or already contained in `main` | **Stale** — work is on `main` already | **Delete** local (and remote if it still exists): `git branch -d name` then `git push origin --delete name` if needed. |
| Branch with commits **not** on `main` | **Active or parked** work | If **done** → merge via PR or `git merge` then push. If **not done** → leave; optionally `git merge main` into it so it stays current. |
| Dirty `main` (modified files) | Uncommitted work | **Not** a branch problem first — commit, stash, or discard per your workflow; optional handoff or warmup scripts may already flag this. |

If you are unsure, the **prescription** is: **one sentence** — “No action,” “Delete branch X (merged),” or “Finish or merge branch Y when ready.”

---

## Fit in operator rhythm

- **Hey (startup):** After your brief or checklist (see [startup / hey rhythm spec](../../good-morning-brief-spec.md)), run the snapshot and capture **one short paragraph** unless only `main` exists and the tree is clean.
- **Hey night (closeout):** Same snapshot when ending a work block if it helps the next session ([closeout / hey night spec](../../good-night-brief-spec.md)).

**Guardrail:** The snapshot is **read-only** during triage. **Merging or deleting** branches is **ship** work — run git deliberately when you are ready (or your instance’s hygiene menu / lane when you choose to execute).

---

## See also

- [Identity Fork Protocol](../../identity-fork-protocol.md) — gated Record merge vs git history.
- [Startup / hey rhythm spec](../../good-morning-brief-spec.md) — operator startup contract (legacy filename on disk).
- [Template–instance contract](../../template-instance-contract.md) — what the template promises vs instance-owned surfaces.
