# Companion-Self Developer Plan — Minimal Docs and Implementation Checklist

**Audience:** Developer (or agent) working in the **companion-self** repo. Use this plan to implement the minimum viable template. Source: [companion-self-bootstrap](../companion-self-bootstrap.md) §3; reference implementation: [grace-mar](https://github.com/rbtkhn/grace-mar).

---

## Workspace boundary (template vs instance)

When working on the template, use a workspace where **companion-self is primary and grace-mar is read-only** (e.g. open `companion-self-and-grace-mar.code-workspace`). Read grace-mar for reference; **do not modify grace-mar from this workspace**. All instance changes (Record, bot, config, and merging upgrades) happen in a **separate grace-mar workspace**. See [companion-self-bootstrap](../companion-self-bootstrap.md) §7.

---

## Part 1: Minimal docs companion-self needs

### Required (minimum viable)

| # | Deliverable | Purpose |
|---|-------------|---------|
| 1 | **README.md** | Entry point: what this repo is, how instances are created, where to find the first instance. |
| 2 | **Concept doc(s)** | What is a companion self? (Mind + Record + Voice; cognitive fork; sovereign merge; knowledge boundary.) Generic — no real person, no age. |
| 3 | **Protocol doc** | Identity Fork Protocol in short form: stage → approve → merge; agent may stage, may not merge; evidence linkage. |
| 4 | **Seed-phase doc** | Definition of seed phases (surveys, artifacts, what populates initial SELF, self-skill-*, self-evidence). Rule: "New instance = new user + seed phase" only. |

### Optional (minimum viable)

| # | Deliverable | Purpose |
|---|-------------|---------|
| 5 | **users/_template/** | Minimal scaffold: self.md, self-knowledge.md, self-curiosity.md, self-personality.md, self-skill-read.md, self-skill-write.md, self-skill-work.md, self-evidence.md, recursion-gate.md, self-memory.md (structure only, no real data). Used when creating a new user dir in an instance. |
| 6 | **how-instances-consume-upgrades.md** | How an instance (e.g. grace-mar) pulls upgrades from this template; link to grace-mar's [MERGING-FROM-COMPANION-SELF](https://github.com/rbtkhn/grace-mar/blob/main/docs/MERGING-FROM-COMPANION-SELF.md). Optionally: list of template paths. |

### Optional later (not minimal)

- One-page static site for companion-self.com.
- Script/checklist: "Initialize new user from seed."
- LICENSE, CONTRIBUTING.
- Template paths list (e.g. TEMPLATE-PATHS.txt) for instance sync.

---

## Part 2: Where to get content

All minimal docs can be **extracted and generalized** from grace-mar. Do not copy Record data or instance-specific details.

| Companion-Self doc | Grace-mar source(s) | Generalize by |
|--------------------|---------------------|---------------|
| Concept | `docs/CONCEPTUAL-FRAMEWORK.md`, `docs/ARCHITECTURE.md` | Remove "Abby", age ("6-year-old"), grace-mar-specific examples. Keep: Record, Voice, fork, knowledge boundary, dyad. |
| Protocol | `docs/identity-fork-protocol.md` | Summarize; keep stage → approve → merge, evidence linkage, agent may not merge. |
| Seed phase | `docs/ARCHITECTURE.md` (Fork Lifecycle, Seeding), `docs/OPERATOR-BRIEF.md` | Describe phases, surveys, artifacts, what creates initial SELF, self-skill-*, self-evidence. No operator-specific workflow. |
| users/_template/* | `docs/SELF-TEMPLATE.md`, `self-skill-* templates`, `docs/Evidence-TEMPLATE.md` or self-evidence equivalent, `docs/self-memory-TEMPLATE.md` or equivalent | Render as minimal empty or scaffold files (structure only). |
| how-instances-consume-upgrades | grace-mar's `docs/MERGING-FROM-COMPANION-SELF.md` | Invert perspective: "Instances pull from here. Safe paths: … Never overwrite: users/<id>/." Link to grace-mar merge checklist. |

---

## Part 3: Implementation checklist and plan

**Order:** Do in sequence so later steps can reference earlier artifacts.

### Phase A: Repo identity and entry

- [x] **A1. README.md**
  - One line: companion-self = template; grace-mar = first instance.
  - One line: "A new companion self is created when a new user completes seed phase."
  - Links: [grace-mar repo](https://github.com/rbtkhn/grace-mar), [grace-mar.com](https://grace-mar.com) (or placeholder). Optional: companion-self.com when it exists.
  - **Done when:** A reader knows what this repo is and where the reference instance lives.

### Phase B: Concept

- [x] **B1. Concept doc** (e.g. `docs/concept.md` or `docs/CONCEPTUAL-FRAMEWORK.md`)
  - Topics: Mind + Record + Voice; cognitive fork (not twin); sovereign merge; knowledge boundary; dyad (human + Record/Voice).
  - Generalize from grace-mar's CONCEPTUAL-FRAMEWORK and ARCHITECTURE; remove instance-specific references.
  - **Done when:** Someone can understand "what is a companion self" without reading grace-mar.

### Phase C: Protocol

- [x] **C1. Protocol doc** (e.g. `docs/identity-fork-protocol.md` or section in CONCEPT)
  - Stage → approve → merge; agent may stage, may not merge; evidence linkage; no direct merge into Record.
  - Summarize from grace-mar's IDENTITY-FORK-PROTOCOL.
  - **Done when:** Protocol rules are clear and instance-agnostic.

### Phase D: Seed phase

- [x] **D1. Seed-phase doc** (e.g. `docs/seed-phase.md` or section in ARCHITECTURE or README)
  - What seed phases are; what surveys/artifacts; what creates initial SELF, self-skill-*, self-evidence.
  - Rule: new instance = new user + seed phase only (no copy from another instance).
  - Derive from grace-mar's ARCHITECTURE (Fork Lifecycle, Seeding) and OPERATOR-BRIEF.
  - **Done when:** A new operator knows how an instance is created and what to run.

### Phase E: Optional scaffold and upgrade guide

- [x] **E1. users/_template/** (optional)
  - Create `users/_template/` with minimal self.md, self-knowledge.md, self-curiosity.md, self-personality.md, self-skill-read.md, self-skill-write.md, self-skill-work.md, self-evidence.md, recursion-gate.md, self-memory.md.
  - Content: structure/headings only (or placeholders). No real data. Use grace-mar's docs/*-TEMPLATE.md as reference.
  - **Done when:** Copying this directory gives a valid empty user scaffold.

- [x] **E2. how-instances-consume-upgrades.md** (optional)
  - Short doc: instances pull from this template; safe to sync (concept, protocol, schema templates); never overwrite `users/<id>/`. Link to grace-mar's [MERGING-FROM-COMPANION-SELF](https://github.com/rbtkhn/grace-mar/blob/main/docs/MERGING-FROM-COMPANION-SELF.md).
  - Optionally list template paths (same list as in MERGING-FROM-COMPANION-SELF §1).
  - **Done when:** An instance operator knows how to pull upgrades.

### Phase F: Consistency and handoff

- [ ] **F1. Cross-check**
  - No bot code, no Record data, no instance config (no Telegram token, no grace-mar.com paths). See bootstrap §4.
  - **Done when:** Repo contains only template content.

- [ ] **F2. Bootstrap and grace-mar**
  - Ensure companion-self-bootstrap.md remains at repo root and §9 (source material) still points to correct grace-mar paths.
  - **Done when:** Next agent or developer can open companion-self, read bootstrap + this plan, and continue.

- [ ] **F3. When adding or renaming canonical template paths**
  - Update both the table in how-instances-consume-upgrades and **`template-manifest.json`** (paths, descriptions, optional flag, and `canonicalAsOf` date). Keeps the audit manifest in sync with the path list.

---

## Part 4: Suggested file layout (after implementation)

```
companion-self/
├── companion-self-bootstrap.md   # Already present
├── README.md                     # A1
├── how-instances-consume-upgrades.md   # E2 optional (at root)
├── template-manifest.json        # Canonical paths for audit; update when adding/renaming paths (F3)
├── companion-self-and-grace-mar.code-workspace   # §7: template + grace-mar (read-only)
├── docs/
│   ├── companion-self-developer-plan.md  # This file
│   ├── concept.md                # B1 (or CONCEPTUAL-FRAMEWORK.md)
│   ├── identity-fork-protocol.md  # C1 (or section in CONCEPT)
│   ├── seed-phase.md             # D1 (or section elsewhere)
│   ├── template-source.example.json  # Example for instances: record merge commit + date (auditability)
│   └── recursive-self-learning-objectives.md  # Learning-science-inspired objectives for Record improvement
└── users/
    └── _template/               # E1 optional
        ├── self.md
        ├── self-knowledge.md
        ├── self-curiosity.md
        ├── self-personality.md
        ├── self-skill-read.md
        ├── self-skill-write.md
        ├── self-skill-work.md
        ├── self-evidence.md
        ├── recursion-gate.md
        └── self-memory.md
```

---

## Part 5: Definition of done (minimal)

Companion-Self is **minimally viable** when:

1. README explains template vs instance and links to grace-mar.
2. At least one concept doc explains what a companion self is (generic).
3. Protocol is documented (stage → approve → merge; no merge without approval).
4. Seed phase is defined (how a new instance is created).
5. Repo contains no bot code, no Record data, no instance config.

Optional: `users/_template/` scaffold and how-instances-consume-upgrades complete the picture for instance operators and new-user creation.

---

**Reference:** [companion-self-bootstrap](../companion-self-bootstrap.md) §3 (What to Create), §7 (Workspace boundary), §8 (First-Run Agent Instructions), §9 (Grace-Mar source material).
