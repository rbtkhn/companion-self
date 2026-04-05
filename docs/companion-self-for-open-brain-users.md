# companion-self for Open Brain users

**Audience:** People who already know **Open Brain**–style systems (Slack or MCP **capture**, **embeddings**, **semantic search** in a database, Nate B Jones stack, etc.) and are starting **companion-self** as a **cognitive fork** template.

**What this is:** Orientation for **template and instance** repos — not live Record content. It **maps** concepts so you do **not** treat “searchable memory” and “governed identity” as the same thing.

**Canonical template:** [github.com/rbtkhn/companion-self](https://github.com/rbtkhn/companion-self) — use your clone’s [`docs/seed-phase.md`](seed-phase.md) and related files for formation.

---

## Comparison — one screen

Open Brain here means the common pattern: **capture → embed → retrieve** (e.g. `thoughts` table, MCP `search_thoughts` / `capture_thought`). **Record** means **`self.md`**, **EVIDENCE**, IX, and the **gated pipeline** in a **live instance**. **MEMORY** is **`self-memory.md`** (continuity, not authoritative vs SELF). **WORK** is **`docs/skill-work/**`** and operator staging — not the triad seat “Voice.”

| | **Open Brain** | **companion-self Record** | **MEMORY** (`self-memory.md`) | **WORK / operator docs** |
|---|----------------|----------------------------|-------------------------------|---------------------------|
| **What it is for** | Fast **find** and **store** of notes for AI retrieval | **Who the companion is** — durable, approved identity and evidence | **Session / continuity** — pointers, tone, open loops | **Plans, mirrors, drafts** — instrumental layer |
| **Who owns “truth”** | You; database is **source** for captured rows | **Companion** (human) via **approval**; SELF is authoritative | **Operator** rotatable prose; **loses** to SELF if they conflict | **Operator**; not identity truth |
| **How something becomes official** | Insert / capture pipeline (config + keys) | **Stage** → **`recursion-gate.md`** → **approve** → merge (SELF, EVIDENCE, prompt, etc.) per **instance** pipeline | Write in MEMORY file; **never** bypasses gate into SELF | Commit WORK markdown; **no** automatic promotion to Record |
| **How AI is supposed to use it** | **Tools** (MCP) **search** and **add** rows | **Voice** **reads** merged profile; **abstains** outside boundary; lookup when offered | **Continuity** for sessions — not a fact source for identity | **Assistants** draft; **stage** to gate — **not** merge |
| **Typical mistake** | Assuming **retrieval rank** = **importance** or **consent** | **Hand-editing** `self.md` or skipping gate | Treating MEMORY as **substitute Record** | Pasting **instance A** `users/` into **instance B** |
| **Tooling seat (optional)** | MCP server + client connectors | **Voice** (emulation) + **bot** prompts; merge **scripts** | N/A | **Cursor / work agents** — [context-pack-for-agents.md](context-pack-for-agents.md); live instances add **AGENTS.md** for gate + merge rules ([identity-fork-protocol.md](identity-fork-protocol.md)) |

---

## Same shape, different job (rhyme)

Both systems care **what the AI can rely on**. Open Brain optimizes **volume and recall** of captures. companion-self optimizes **explicit, human-approved identity** and **evidence** so the Voice does not silently absorb unvetted text as “self.”

```mermaid
flowchart LR
  subgraph OB [Open_Brain]
    c1[capture] --> c2[embed]
    c2 --> c3[semantic_search]
  end
  subgraph CS [companion_self_Record]
    d1[stage_or_report] --> d2[gate_review]
    d2 --> d3[merged_Record]
  end
```

Parallel **pipelines**, not interchangeable: **search** does not replace **gate**.

---

## What not to do

If you are used to “everything searchable is fair game for the model,” **pause** — companion-self **splits** **capture** from **identity**.

- Do **not** **bulk-import** notes or chat exports straight into **`self.md` / IX** as if **searchability** or **embedding** meant **approval**.
- Do **not** treat **embedding similarity** or **RAG** hits as **consent** to merge **facts** or **personality** into the Record.
- Do **not** **replace** the **recursion gate** with “the AI **remembered** it from a vector database.”
- Do **not** connect **MCP**, **Cursor**, or other tools to **silent writes** into **SELF**, **EVIDENCE**, or **Voice prompts** — use staging + companion-approved merge per [identity-fork-protocol.md](identity-fork-protocol.md) and your instance’s **AGENTS.md**.
- Do **not** **copy** another instance’s **`users/<id>/`** tree into yours. See [instance-patterns.md](instance-patterns.md) and the root **README** north star (new companions complete **seed phase**, not repo duplication).

---

## Where to go next

- **Template:** [`docs/seed-phase.md`](seed-phase.md), [`docs/seed-phase-readiness.md`](seed-phase-readiness.md), [`docs/seed-phase-validation.md`](seed-phase-validation.md).
- **Gate and fork semantics:** [`docs/concept.md`](concept.md), [`docs/identity-fork-protocol.md`](identity-fork-protocol.md).
- **Agent load order:** [`docs/context-pack-for-agents.md`](context-pack-for-agents.md). **WORK territory:** [`docs/skill-work/README.md`](skill-work/README.md).

---

## Revision log

| Date | Note |
|------|------|
| 2026-04-03 | Added on companion-self via PR (mirror of grace-mar `work-companion-self` bridge; links adapted for template paths). |
