# Part 10 Split Plan — LLMOps + Designing LLM-Based Products

**Author**: Architecture planning pass, 2026-05-16
**Status**: DESIGN (no files moved yet)
**Predecessor**: `docs/part-8-restructure-plan.md`

---

## Section A — Current State Map

| Module | Sections | Class | Notes |
|--------|---------:|-------|-------|
| 42 Ideation | 3 | PRODUCT | clean |
| 43 Product Management | 3 | PRODUCT | clean |
| 44 Strategy & Prioritization | 4 (2 dupes) | PRODUCT | needs dedupe before split |
| 45 Vibe-Coding | 3 | PRODUCT | clean |
| 46 MVP | 3 | PRODUCT | clean |
| 47 Prototype to Production | 7 | MIXED | 47.7 needs split |
| 48 Compute Planning | 4 | OPS | fix 48.4 stale H1 |
| 49 Scaling Economics | 3 | MIXED | 49.2, 49.3 need split |
| 50 Shipping & Deploying | 6 | MIXED | 50.3, 50.5, 50.6 need split |
| 51 Production Engineering | 7 | OPS | wholesale redistribute |
| 52 Tools of the Trade | 5 | MIXED | split into ops + product tools |

---

## Section B — Proposed New Part 10 (LLMOps)

**Title**: Part X — LLM Operations & Production Infrastructure
**Target**: 7 substantive + 1 Tools = 8 chapters, ~32 sections.

### Chapter 42 — Compute Planning & Infrastructure (was Ch 48)

1. **42.1** LLM Compute Planning & Infrastructure
2. **42.2** Enterprise Integration Patterns
3. **42.3** GPU Procurement Strategy & Spot-Reserved Economics
4. **42.4** LLM Performance Benchmarking & Cross-Hardware Portability

### Chapter 43 — Inference Serving & AI Gateways (NEW)

1. **43.1** Inference Serving Stacks: vLLM, TensorRT-LLM, SGLang, TGI *(NEW)*
2. **43.2** Scaling, Latency & Queue Management *(from 51.1)*
3. **43.3** AI Gateways & Model Routing *(from 51.3)*
4. **43.4** Semantic Caching & Prompt Caching at the Gateway *(NEW)*

### Chapter 44 — LLMOps: CI/CD, Versioning, Model Registry (NEW)

1. **44.1** LLMOps Foundations *(NEW + 51.2 opener)*
2. **44.2** Prompt Versioning, Model Registry & Continuous Improvement *(from 51.2)*
3. **44.3** Deployment Patterns: Canary, Blue-Green, Shadow *(NEW)*
4. **44.4** A/B Testing & Online Experimentation *(from 51.2 + 50.4)*
5. **44.5** Data Pipelines for LLM Applications *(NEW)*

### Chapter 45 — Reliability Engineering & Production Guardrails

1. **45.1** Failure Taxonomy for LLM Systems *(from 51.6.1)*
2. **45.2** Circuit Breakers, Retries & Idempotency *(from 51.6 + 51.4)*
3. **45.3** SLOs & SLIs for Probabilistic Systems *(from 51.6)*
4. **45.4** Chaos Engineering for LLM Workloads *(from 51.6)*
5. **45.5** Production Guardrails & Output Validation *(from 51.1)*

### Chapter 46 — Workflow Orchestration, Durable Execution & Edge

1. **46.1** Workflow Orchestration: Temporal, Inngest, LangGraph *(from 51.4)*
2. **46.2** Durable Execution Patterns *(from 51.4)*
3. **46.3** Edge & On-Device LLM Deployment *(from 51.5)*
4. **46.4** Hybrid Edge-Cloud Architectures *(NEW from 51.5 tail)*

### Chapter 47 — Kubernetes-Native LLM Operations & Cost FinOps

1. **47.1** K8s-Native LLM Ops: Scheduling, Serving, GPU Management *(from 51.7)*
2. **47.2** GPU Multi-Tenancy: MIG, MPS, Time-Slicing *(from 51.7)*
3. **47.3** Autoscaling & Scale-to-Zero *(from 51.7)*
4. **47.4** LLM FinOps: Cost Attribution, Showback, Chargeback *(NEW)*
5. **47.5** Multi-Vendor Cost Arbitrage *(from 49.3 ops half)*

### Chapter 48 — Application Architecture, Deployment & Observability of Production Traffic

1. **48.1** Application Architecture for LLM Apps *(from 50.5)*
2. **48.2** Deployment Topologies: Bedrock, Vertex, Modal, Self-Host *(from 50.5)*
3. **48.3** Provider Portability & Multi-Provider (operational) *(from 50.3 ops half)*
4. **48.4** Post-Launch Monitoring & Iteration *(from 50.4)*
5. **48.5** Secrets Management & Operational Security *(NEW)*

### Chapter 49 — Tools of the Trade: LLMOps Stack

From 52 ops-side split + new tools survey.

---

## Section C — Proposed New Part 11 (Designing LLM-Based Products)

**Title**: Part XI — Designing LLM-Based Products
**Target**: 7 substantive + 1 Tools = 8 chapters, ~36 sections.

### Chapter 50 — Ideation: Finding LLM-Worthy Problems (from Ch 42, intact)

### Chapter 51 — LLM Product Management (from Ch 43 + new 51.4)

1. 51.1 From Hypothesis to Product Spec
2. 51.2 LLM Product Management
3. 51.3 UX and Iteration for LLM Products
4. **51.4** User Research & Feedback Loops *(NEW)*

### Chapter 52 — LLM Strategy & Build-vs-Buy (from Ch 44 deduped + 50.3)

1. 52.1 Strategy & Use Case Prioritization *(44.1 + 44.3 deduped)*
2. 52.2 Vendor Evaluation & Build vs. Buy *(44.2 + 44.4 deduped)*
3. 52.3 Provider Portability (product lens) *(50.3 strategic half)*

### Chapter 53 — Prototyping via Vibe-Coding (from Ch 45, intact)

### Chapter 54 — Building the MVP (from Ch 46, intact)

### Chapter 55 — From Prototype to Production (Product View) (from Ch 47 product half)

47.1-47.6 + 47.7 product half.

### Chapter 56 — LLM Economics: Unit Costs, ROI & Pricing

1. 56.1 ROI Measurement & Value Attribution *(from 49.1)*
2. 56.2 Economic Design of LLM Systems (product view) *(from 49.2 product half)*
3. 56.3 Token Cost Forecasting *(from 49.3 product half)*
4. 56.4 Launch Constraints & AI Unit Economics *(from 50.1)*
5. 56.5 AI Copilots Across the Lifecycle *(from 50.2)*
6. **56.6** Pricing & Packaging LLM Products *(NEW)*

### Chapter 57 — Shipping AI Products (Product View)

1. 57.1 UX Considerations for Probabilistic Products *(from 50.6 product half)*
2. **57.2** Launch Playbooks & Go-to-Market *(NEW)*
3. **57.3** Post-Launch Iteration (product lens) *(NEW)*

### Chapter 58 — Tools of the Trade: Idea-to-Product Toolkit

From 52 product-side split.

---

## Section D — Section-by-Section Move Table

(See plan source for full table; major sections requiring SPLIT:)

- 47.7 → 55.7 (P11) + 48.x (P10 architecture hardening)
- 49.2 → 56.2 (P11) + 43.4 (P10 caching)
- 49.3 → 56.3 (P11 forecasting) + 47.5 (P10 arbitrage)
- 50.3 → 52.3 (P11 strategy) + 48.3 (P10 implementation)
- 50.5 → 48.1 + 48.2 (P10)
- 50.6 → 57.1 (P11 UX) + P10 tools (Gradio/Streamlit)
- 51.1 → 43.2 (scaling) + 45.5 (guardrails)
- 51.2 → 44.1 + 44.2 + 44.4 (P10)
- 51.4 → 46.1 + 46.2 (P10)
- 51.5 → 46.3 + 46.4 (P10)
- 51.6 → 45.1-4 (P10)
- 51.7 → 47.1-3 (P10)
- 52.1 → 58.1 (P11) + 49.1 (P10)
- 52.2 → 58.2 (P11) + 49.2 (P10)
- 52.5 → 58.6 (P11) + 49.5 (P10)

---

## Section E — Cascade Renumbering

The split adds one new Part. Top-level Parts shift.

| Before | After |
|--------|-------|
| Part X — Building LLM and Agent Products | (DISSOLVED) |
| Part XI — Applications Across Industries | **Part XII — Applications Across Industries** |
| Part XII — Frontiers | **Part XIII — Frontiers** |
| — | **Part X — LLM Operations & Production Infrastructure** |
| — | **Part XI — Designing LLM-Based Products** |

Chapter range cascade:
- P10 LLMOps: Ch 42-49 (NEW)
- P11 Designing: Ch 50-58
- P12 Applications: Ch 59-68 (was 51-60, shift +8)
- P13 Frontiers: Ch 69-73 (was 61-65, shift +8)

Net chapter growth: 52 → 60 (+8). Caused by: module-51 expands into 5 chapters in P10; gap-fill new sections justify additional standalone chapters; module-52 splits into two Tools chapters.

Directory renames: 11 source modules → 16 destination modules; +2 new top-level part dirs.

---

## Section F — Content Gaps Requiring NEW Authoring (11 sections)

### P10 LLMOps (7 gaps)

1. **44.3** Deployment Patterns: Canary, Blue-Green, Shadow Traffic — ~3000 words
2. **47.4** LLM FinOps: Cost Attribution, Showback, Chargeback — ~3000 words
3. **43.1** Inference Serving Stacks (deep-dive) — ~4000 words
4. **48.5** Secrets Management & Operational Security — ~2500 words
5. **44.5** Data Pipelines for LLM Applications — ~2500 words
6. **43.4** Semantic Caching & Prompt Caching at the Gateway — ~2500 words
7. **49.4** Reliability & FinOps Tools — ~2000 words

### P11 Designing (4 gaps)

8. **56.6** Pricing & Packaging LLM Products — ~3000 words
9. **57.2** Launch Playbooks & Go-to-Market — ~2500 words
10. **57.3** Post-Launch Iteration (product lens) — ~2000 words
11. **51.4** User Research & Feedback Loops — ~2500 words

**Total**: ~30k words across 11 new sections.

---

## Section G — Cross-References & Edge Cases

### The Economics question

- Product owner's "should we ship and at what price?" → P11 Ch 56
- Operator's "how to attribute cost and arbitrage?" → P10 Ch 47

Section 49.3 (Token Cost Forecasting) must split at "Multi-Vendor Arbitrage" heading.

### Lock-in & Portability

Same logic. Strategic decision (P11 Ch 52.3) vs operational implementation (P10 Ch 48.3). Section 50.3 splits at "Implementation Patterns" heading.

### Production Guardrails — Safety vs. Operational

Safety guardrails (NeMo, Llama Guard) → Part 9 (already relocated). Operational guardrails (backpressure, rate limits) → P10 Ch 45.5.

### Module 47.7 (From Prototype to MVP)

The bridge section. Product half (quality gates, MVP eval contracts) → 55.7 (P11). Ops half (architecture hardening) → 48.x as subsection (P10).

### Pathways

After the split, "Build AI Products" pathway runs through P11 + dips into specific P10 chapters. A new "Run LLMs in Production" pathway runs through P10 wholesale.

### Capstone

The capstone (a *product*) anchors to P11 Designing; ops content is referenced via cross-links to P10.

### Appendices & Front-Matter Prose

Need rewriting of "see Chapter 49 for ROI" → "see Chapter 56 for ROI" type prose mentions. Phase 50 cross-link rewrite doesn't catch prose; phase 55 prose-chapter-rewrite added.

---

## Section H — Risks & Migration Script Outline

### Risks

- **Migration scale**: ~40 file moves, hundreds of anchor rewrites, dozens of cross-link updates
- **Capstone churn**: capstone narrative spans new boundaries; anchor to P11
- **Visual identity**: each new Part needs new `part-opener.png`
- **Pathways drift**: 5 existing learning pathways need re-threading
- **EPUB/KDP rebuild**: regenerate after restructure; KPF must pass 0-error qualitychecks
- **URL stability**: redirect map
- **Pagefind**: rebuild + validate meta values
- **Bibliography**: cross-section numbers may shift

### Migration script outline

`scripts/restructure_part10_split/`:

```
00_validate_preconditions.py
10_dedupe_module_44.py          (pre-step: dedupe 44.3->44.1, 44.4->44.2)
20_build_migration_map.py
30_create_new_part_dirs.py      (mkdir part-10-llmops, part-11-designing-llm-products)
40_move_module_dirs.py
50_split_sections.py            (heaviest — 15+ sections need splitting)
55_rewrite_prose_chapter_names.py  (NEW phase — book-wide "Chapter NN" rewrites)
60_rewrite_section_anchors.py
70_rewrite_cross_links.py
80_create_new_chapter_skeletons.py  (10 new chapters)
90_renumber_p11_p12.py          (cascade Parts 11/12 → 12/13)
95_regenerate_yaml_and_toc.py
96_generate_redirect_map.py
97_rebuild_search_index.py      (pagefind rebuild)
98_rebuild_epub_kpf.py          (html2epub + Kindle Previewer 3)
99_verify_outcome.py
```

Estimated runtime: 60-120 seconds. Manual content phase after: 11 new sections via book-skills 23-stage pipeline.

### Validation checklist

- [ ] 99_verify_outcome.py reports zero failures
- [ ] pagefind rebuild produces same or larger index
- [ ] All exercises/labs in moved sections execute
- [ ] Bibliography refs resolve
- [ ] book_structure.yaml valid
- [ ] Capstone pathway references new chapter numbers
- [ ] Front-matter pathways re-threaded
- [ ] CLAUDE.md / BOOK_CONFIG.md updated ("P10 = LLMOps, P11 = Designing")
- [ ] No prose "Chapter 48" still pointing at compute planning after renumber
- [ ] KPF passes 0 errors in Kindle Previewer 3

---

## Critical Files

- `book_structure.yaml`
- `toc.html`
- `part-10-idea-to-product/index.html`
- `part-10-idea-to-product/module-51-production-engineering/index.html`
- `docs/part-8-restructure-plan.md` (reference precedent)
