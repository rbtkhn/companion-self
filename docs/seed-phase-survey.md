# Seed Phase — Survey prompts

**Companion-Self template · Intake copy**

Operators use these prompts to collect answers that map into seed-phase JSON artifacts. This doc is **not** the live Record.

See [seed-phase-artifacts.md](seed-phase-artifacts.md) for the file layout and [seed-phase.md](seed-phase.md) for the protocol.

---

## work-business seed survey

Answers feed **`work_business_seed.json`** (validated by **`schema-registry/work-business-seed.v1.json`**). Map free-text lists into JSON arrays; use the schema enums for single-choice and multi-select fields.

**Mapping hints**

| Question theme | JSON field | Enum / shape |
|----------------|------------|----------------|
| Involvement | `business_involvement` | `none`, `light`, `regular`, `core` |
| Role modes | `business_role_modes` | `founder`, `operator`, `investor`, `advisor`, `employee`, `side_project`, `student_entrepreneur`, `researcher_commercial`, `other` (array, unique) |
| Commerce surfaces | `commerce_surfaces` | `none`, `etsy_or_marketplace`, `saas`, `consulting_services`, `content_or_media`, `nonprofit_earned_revenue`, `physical_goods`, `other` (array, unique) |
| Activity kinds | `business_activity_modes` | `market_research`, `competitive_analysis`, `positioning`, `fundraising`, `partnerships`, `operations`, `sales`, `product_strategy`, `content_marketing`, `regulatory_compliance`, `ecommerce_ops`, `other` (array, unique) |
| Companion help | `companion_help_priorities` | `brainstorming`, `planning`, `market_research`, `positioning`, `pitch_review`, `partnership_mapping`, `prioritization`, `business_writing`, `ecommerce_ops`, `competitive_intel`, `other` (array, unique) |

1. Do you run or plan to run a business, side project, or commercial activity?
   - Maps to `business_involvement`: no → `none`; occasional → `light`; regular → `regular`; central to life → `core`.

2. Which roles fit you? (multi-select)
   - founder, operator, investor, advisor, employee, side project, student entrepreneur, commercial researcher, other (note in `notes`).

3. What ventures, brands, or offerings matter most right now?
   - `primary_ventures_or_brands` (string array).

4. Which markets or sectors are you in or watching?
   - `markets_or_sectors` (string array).

5. How do you sell or earn revenue (if at all)?
   - Map to `commerce_surfaces` (Etsy/marketplace, SaaS, consulting, content, nonprofit earned revenue, physical goods, none, other).

6. What kinds of business work do you do most often? (multi-select)
   - Align with `business_activity_modes` above.

7. What commercial or market topics should this companion help you research or think through?
   - `research_or_interest_areas` (string array).

8. What should the companion prioritize when helping with business questions? (multi-select)
   - Align with `companion_help_priorities` above.

9. What business topics, claims, or activities should the companion **avoid** or treat carefully (compliance, privacy, no financial advice, etc.)?
   - `important_constraints` (string array).

10. What are your top 1–3 business focuses for the next few months?
    - `active_focuses` (string array).

After capture, set `evidence_basis` to `seed_survey` when answers are survey-driven; `explicit_user_input` for direct statements only; `mixed` when both apply. Leave `none` only while no evidence is recorded yet.
