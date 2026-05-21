# Post-v10 Index Staleness Audit

## Summary

- Part indexes audited: 12
- Chapter indexes audited: 66
- Pages with NEW staleness (introduced by v10): 1 (only `appendix-q-course-syllabi` slug landed; `appendix-e-tooling-ecosystem` is pre-v10)
- Pages still stale (carried from pre-v10, possibly not yet fixed by in-flight agent): 28
  - 12 part indexes: 4 still stale (parts 6, 8, 9, 10, 11, 12 had stale "What Comes Next" / Part-XII labels / capstone links)
  - 66 chapter indexes: roughly 24 still have at least one residual stale element (prereq labels, body cross-refs, broken module hrefs, nav-num labels, section card title mismatches)
- Pages clean: ~50
- "In flight (skipped)": 0 (no obvious mid-edit signatures; module-31 was edited between reads but is in a coherent state)

Methodology: walked `book_structure.yaml` (12 parts, 66 chapters, 21 appendices A-U) against every `part-N/index.html` and `part-N/module-MM/index.html`. Cross-checked yaml against on-disk section files, against pagefind meta, against title/meta, against What's Next blocks, against prereq labels, against nav-num labels. Spot-checked all 78 pages individually after the regex sweep.

Post-v10 letter cascade verification: searched for `Appendix [LMNOP]\s+Topic` text and `appendix-[a-z]-` slugs across the 78 index pages.
- ZERO references to old appendix letters with old topics ("Appendix M Distributed ML", "Appendix N Docker", "Appendix O Course Syllabi", "Appendix S War Stories") in any part or chapter index.
- ZERO references to dropped resources ("Master Reference Tables", "Freshness Index", "Glossary", "Appendix AD/AE/AF/AI") in any part or chapter index. The dropped-refs cleanup landed cleanly.

Letter cascade is therefore NOT a problem in the part/chapter index files. The v10 reshuffle did not introduce new letter-cascade staleness in these pages.

---

## P0: Severely stale post-v10

None. The 12 part indexes and 66 chapter indexes have no severe v10-introduced regressions. The audit task hypothesized stale "Appendix N Docker", "Appendix M Distributed ML", "Appendix O Course Syllabi" text and old `appendix-n-docker` / `appendix-o-course-syllabi` slugs in part / chapter index pages. None of these patterns appears in any index page audited.

---

## P1: New-appendix gaps (missing references)

These are gaps where post-v10 new appendices SHOULD be referenced but aren't. Pre-v10 chapter-cards typically didn't cross-reference appendices at all from part-index "What Comes Next" blocks, so these are not regressions, but they are missed opportunities:

- `part-4-training-adapting/index.html` — "What Comes Next" block has no pointer to Appendix N (Distributed ML), the natural complement to Chapters 18-20 fine-tuning content. The new Appendix N (DDP, FSDP, ZeRO, Ray Train) is the production-scale companion. Module-21 (Tools of the Trade) does link to `appendix-m-data-engineering` and `appendix-n-distributed-ml`, but the part-index doesn't surface them.
- `part-8-evaluation-production/index.html` — "What Comes Next" block has no pointer to Appendix O (MLOps). Appendix O explicitly covers observability, monitoring, deployment patterns, model registry, SLOs, FinOps; these are direct companions to Chapter 34/35 content. Should be surfaced.
- `part-8-evaluation-production/index.html` — also no pointer to Appendix L (Inference Serving) despite Chapter 35 covering deployment and Chapter 36 listing vLLM/TGI/SGLang. Module-36 (Tools of the Trade) does cite `appendix-l-inference-serving`, but the part-index does not.
- `part-2-understanding-llms/index.html` — "What Comes Next" block does not surface Appendix L (Inference Serving) despite Chapter 10 being Inference Optimization. Module-10 chapter-index references `appendix-l-inference-serving` (good), but the part-index doesn't.
- `part-7-multimodal-generation/index.html` — no pointer to any companion appendix (multimodal does not have a natural appendix companion; this is fine; noting for completeness).
- `part-5-retrieval-conversation/module-25-tools-of-the-trade/index.html` — references `appendix-d-langchain` (correct) but ALSO references `appendix-e-tooling-ecosystem` (WRONG SLUG; the actual is `appendix-e-orchestration-frameworks`). This is a real broken link.

---

## P2: Letter-cascade drift

None found in part or chapter index files. The pre-v10 audit and the dropped-refs cleanup report appear to have caught these, and the v10 letter reshuffle did not affect any index-page text since no part / chapter index file referenced any of the renumbered appendices directly.

Per-letter check (all zero matches):
- "Appendix N Docker" (now P): 0 files
- "Appendix O Course Syllabi" (now Q): 0 files
- "Appendix M Distributed ML" (now N): 0 files
- "Appendix P Reading Pathways" (now R): 0 files
- "Appendix Q Intermediate Projects" (now S): 0 files
- "Appendix R Capstone" (now T): 0 files
- "Appendix S War Stories" (now U): 0 files
- Dropped-ref ghosts ("Master Reference Tables", "Freshness Index", "Glossary", "Appendix AD/AE/AF/AI"): 0 files

---

## P3: Pre-v10 staleness still pending fix

Items the `index-staleness-fix-report.md` claimed were resolved but that still appear in the current files. These are items the in-flight fix agent has not yet addressed (or that survived its sweep):

### Part-index files

**`part-6-agentic-ai/index.html`**
- "What Comes Next" still says: "Continue to Part VII: AI Applications" — Part 7 is now "Multimodal Generation" not "AI Applications". Pre-v10 issue.

**`part-8-evaluation-production/index.html`**
- "What Comes Next" still says: "Continue to Part IX: Safety and Strategy" — Part 9 is now "LLM Safety, Security, and Ethics" not "Safety and Strategy". Pre-v10 issue. Also the meta-description `<meta name="description">` says "Part VIII: Evaluation & Production" but `<title>` says "Evaluation of LLM-Based Systems" — a minor inconsistency.

**`part-9-safety-security-ethics/index.html`**
- `<meta name="description">` still says "Part IX: Safety & Strategy" (old name; `<title>` is correct). Pre-v10.
- "What Comes Next" prose says "Continue to Part X: Frontiers" but the href points to `../part-12-frontiers/index.html`. Both the label AND the target are wrong. After v10 the next part is Part 10 (Building LLM and Agent Products). Should link to `../part-10-idea-to-product/index.html` labeled "Part X: Building LLM and Agent Products".

**`part-10-idea-to-product/index.html`**
- "What Comes Next" prose implies the book ends with Part 10 ("you have completed the book's journey from foundations to frontiers to product. Explore the Appendices..."). But Parts 11 (Applications) and 12 (Frontiers) follow. The block should hand off to Part 11.

**`part-11-applications-across-industries/index.html`**
- "What Comes Next" links to `../capstone/index.html` labeled "Capstone Project". That path does not exist on disk; the capstone is at `../appendices/appendix-t-capstone-project/index.html`. Pre-v10 issue; not fixed.
- Subtitle says "Seven vertical applications" but the part actually has 10 chapters: 7 vertical industry chapters (51-57) PLUS Creative Industries (58), Recommendation & Search (59), and Tools of the Trade (60). Subtitle and `<meta description>` undercount.

**`part-12-frontiers/index.html`**
- "What Comes Next" prose still says "Continue to Part XI: From Idea to AI Product" with href pointing to `../part-10-idea-to-product/index.html`. After v10 Part 12 is the LAST part; nothing comes next (Appendices follow). Both label ("Part XI: From Idea to AI Product") and prose are wrong.

### Chapter-index files

**`part-1-foundations/module-00-ml-pytorch-foundations/index.html`**
- Section 0.1 card title: "ML Basics: Features, Optimization & Generalization" but yaml expects "What Every LLM Engineer Needs From Classical ML".
- Section 0.3 card title: "PyTorch Tutorial" but yaml expects "PyTorch in 90 Minutes: Tensors to Training Loop".
- Section 0.1 description references "pretraining and scaling (Chapter 06)" — Ch 06 is now Tools of the Trade, pretraining is Ch 07.
- Section 0.3 description references "inference optimization (Chapter 09)" — Ch 09 is now Reasoning, inference optimization is Ch 10.

**`part-1-foundations/module-03-sequence-models-attention/index.html`**
- Section 3.1 card title: "Recurrent Neural Networks & Their Limitations" but yaml expects "Why RNNs Couldn't Scale to Modern LLMs".

**`part-1-foundations/module-04-transformer-architecture/index.html`**
- Section 4.1 card title: "Transformer Architecture Deep Dive" but yaml expects "How a Transformer Computes One Token".
- Line 46: "explored further in Chapter 07: Modern LLM Landscape" — Ch 07 is now Pretraining; Ch 08 is Modern LLM Landscape.
- Line 51: "inference optimization techniques in Chapter 09" — Ch 09 is now Reasoning; inference optimization is Ch 10.
- Line 65: "preparing you for Chapter 06's pretraining discussion" — Ch 06 is now Tools of the Trade; pretraining is Ch 07.
- Line 116: section 4.3 desc references "Chapter 07" — same stale label.

**`part-2-understanding-llms/module-07-pretraining-scaling-laws/index.html`**
- `<title>` says "Chapter 06: Pre-training..." (should be Chapter 7).
- `<meta name="description">` same stale "Chapter 06".
- Missing the explicit `chapter:Chapter 7: ...` pagefind meta injection (only `chapter` on breadcrumb).
- Section 7.1 card title: "The Landmark Models" but yaml expects "BERT, GPT, T5: Three Bets That Shaped Today's LLMs".
- Section 7.8 card title: "Production LLM Training Systems" but yaml expects the longer "Production LLM Training Systems: Megatron, Elastic Training, and Fault Tolerance".

**`part-2-understanding-llms/module-08-modern-llm-landscape/index.html`**
- `<title>` says "Chapter 07: Modern LLM Landscape..." (should be Chapter 8).
- `<meta name="description">` same stale "Chapter 07".
- Missing explicit `chapter:Chapter 8: ...` pagefind meta injection.

**`part-2-understanding-llms/module-09-reasoning-test-time-compute/index.html`**
- `<title>` says "Chapter 08: Reasoning..." (should be Chapter 9).
- `<meta name="description">` same stale "Chapter 08".
- Missing explicit `chapter:Chapter 9: ...` pagefind meta injection.
- Section 9.1 card title: "The Test-Time Compute Paradigm" but yaml expects "Trading FLOPs for IQ: The Test-Time Compute Bet".

**`part-2-understanding-llms/module-10-inference-optimization/index.html`**
- `<title>` says "Chapter 09: Inference Optimization..." (should be Chapter 10).
- `<meta name="description">` same stale "Chapter 09".
- Missing explicit `chapter:Chapter 10: ...` pagefind meta injection.

**`part-2-understanding-llms/module-11-interpretability/index.html`**
- Missing explicit `chapter:Chapter 11: ...` pagefind meta injection.

**`part-3-working-with-llms/module-13-llm-apis/index.html`**
- Prereq label "Chapter 05" (correct ch href, but should read "Chapter 5" not "Chapter 05" to match the rest of the book's convention - cosmetic).
- Prereq label "Chapter 09: Inference Optimization" — Ch 09 is now Reasoning; inference optimization is Ch 10. The href (line 76) correctly goes to module-10, only the label is stale.
- Stray empty `<li></li>` at line 125-126.
- Missing explicit `chapter:Chapter 13: ...` pagefind meta injection.

**`part-3-working-with-llms/module-14-prompt-engineering/index.html`** — missing pagefind chapter meta.

**`part-3-working-with-llms/module-15-hybrid-ml-llm/index.html`** — missing pagefind chapter meta.

**`part-4-training-adapting/module-17-synthetic-data/index.html`** — missing pagefind chapter meta. Stray empty `<li></li>`.

**`part-4-training-adapting/module-18-fine-tuning-fundamentals/index.html`** — missing pagefind chapter meta.

**`part-4-training-adapting/module-19-peft/index.html`** — missing pagefind chapter meta.

**`part-4-training-adapting/module-20-alignment-rlhf-dpo/index.html`**
- Missing pagefind chapter meta.
- Section 20.1 card title: "RLHF: Reinforcement Learning from Human Feedback" but yaml expects "RLHF: Teaching a Model What 'Helpful' Means".

**`part-5-retrieval-conversation/module-22-embeddings-vector-db/index.html`** — missing pagefind chapter meta.

**`part-5-retrieval-conversation/module-23-rag/index.html`** — missing pagefind chapter meta.

**`part-5-retrieval-conversation/module-24-conversational-ai/index.html`** — missing pagefind chapter meta.

**`part-5-retrieval-conversation/module-25-tools-of-the-trade/index.html`**
- Body references `appendix-e-tooling-ecosystem` (broken slug; actual is `appendix-e-orchestration-frameworks`).

**`part-6-agentic-ai/module-26-ai-agents/index.html`**
- Missing pagefind chapter meta.
- Looking Back: "the four-step pattern that everything in Chapters 21 through 24 specializes" — old chapter numbers; current Ch 21 is Tools of Trade (Part 4), Ch 22-24 are RAG/Embeddings/Conversational AI (Part 5). Should reference Chapters 27-29 (the Part 6 chapters that build on the agent loop).
- Big-Picture callout: "production agent deployment (Chapter 25)" — Ch 25 is now Tools of the Trade in Part 5; agent safety is now Ch 38 in Part 9.
- Prereq label "Chapter 08: Reasoning & Test-Time Compute" — reasoning is now Ch 9; href correctly goes to module-09.
- Section 26.1 card title: "The Agent Paradigm: From Chains to Autonomous Agents" but yaml expects "What Makes an LLM an Agent (and What Doesn't)".
- Section 26.5 card title: "End-to-End Agent System Architecture" — yaml adds ": A Deployment Blueprint" suffix.
- Section 26.6 card title: "Agent Memory Systems" — yaml says "Memory Architecture for Agents: Taxonomy, Storage, and Policies".

**`part-6-agentic-ai/module-27-tool-use-protocols/index.html`** — missing pagefind chapter meta.

**`part-6-agentic-ai/module-28-multi-agent-systems/index.html`** — missing pagefind chapter meta.

**`part-6-agentic-ai/module-29-specialized-agents/index.html`**
- "What's Next" links to `../module-26-ai-agents/index.html` labeled "Chapter 25: Agent Safety and Production". Both the chapter number and the title are wrong. Should be Chapter 30 Tools of the Trade or jump to Chapter 38 (Agent Safety) in Part 9.

**`part-7-multimodal-generation/module-31-multimodal/index.html`**
- Missing pagefind chapter meta.
- Big-Picture callout: "These capabilities unlock the application patterns surveyed in Chapter 27" — Ch 27 is now Tool Use, not Applications. Pre-v10 reference to the dissolved "Ch 27 LLM Applications" should now point at Part 11.
- Prereq label "Chapter 06: Inside LLMs" (href -> module-07 which is Pretraining) — label stale; should be "Chapter 7" with current title.
- Prereq label "Chapter 07: Training LLMs" (href -> module-08 which is Modern LLM Landscape) — label stale.

**`part-8-evaluation-production/module-34-evaluation-observability/index.html`**
- Missing pagefind chapter meta.

**`part-8-evaluation-production/module-35-production-engineering/index.html`**
- Missing pagefind chapter meta.
- Body line 60: "strategic and business considerations are covered in Chapter 31: LLM Strategy, Product Management and ROI" — Ch 31 is now Multimodal Generation; strategy is now in Part 10 (Ch 42, Ch 47).
- Still has "Safety and Strategy" stale Part 9 label somewhere (flagged by `Safety and Strategy` grep).
- Section 35.9 card title: "Kubernetes-Native LLM Operations" — yaml adds ": Scheduling, Serving, and GPU Management" suffix.

**`part-9-safety-security-ethics/module-37-safety-ethics-regulation/index.html`**
- Missing pagefind chapter meta.
- Body line 56: "preparing the ground for the strategic and ROI considerations in Chapter 31" — Ch 31 is now Multimodal; strategy/ROI is now Part 10 (Ch 42, Ch 47).

**`part-10-idea-to-product/module-40-ideation/index.html`**
- Section files `section-40.2.html` and `section-40.3.html` exist on disk but the yaml only lists 40.1 AND the chapter index only links section-40.1. Either yaml is stale (needs to add 40.2, 40.3) or the extra files should be removed. Index doesn't show 40.2/40.3 cards.

**`part-10-idea-to-product/module-45-prototype-to-production/index.html`**
- Prereq broken href: `../../part-9-safety-security-ethics/module-31-strategy-product-roi/index.html` labeled "Chapter 31: Strategy & ROI" — module-31-strategy-product-roi does not exist (dissolved into Part 10). Should point to Ch 42 in Part 10.
- Nav prev/up nav-num says "Part XI" — Part 10 = Part X. Two occurrences (prev and up).

**`part-10-idea-to-product/module-48-shipping-deploying/index.html`**
- Body line 41: "every skill from Part XI" — should be "Part X".
- Body line 42: "...the build methodology from Chapter 45. It references production engineering from Chapter 35, evaluation from Chapter 34, and enterprise strategy from Chapter 31" — two issues: "Chapter 45 and the build methodology from Chapter 45" is a duplicate / typo (which one?), and "enterprise strategy from Chapter 31" is stale (Ch 31 dissolved).
- Nav up nav-num says "Part XI" with title "From Idea to AI Product" — should be "Part X" / "Building LLM and Agent Products".

**`part-11-applications-across-industries/module-51-legal-llms/index.html`**
- Body line 137: "cited in section 36.3" — section 36.3 refers to OLD chapter 36 numbering; current chapter is 51, so should be section 51.3.
- Nav prev/up nav-num "Part XII" with title "LLM LLM Applications Across Industries" — should be "Part XI" with title "LLM Applications Across Industries".

**`part-11-applications-across-industries/module-52-finance-llms/index.html`**
- Nav prev/up nav-num "Part XII" with title "LLM LLM Applications Across Industries" — should be "Part XI" / "LLM Applications Across Industries".

**`part-11-applications-across-industries/module-53-healthcare-llms/index.html`** — same nav-num "Part XII" / wrong title.

**`part-11-applications-across-industries/module-54-education-llms/index.html`** — same nav-num "Part XII" / wrong title.

**`part-11-applications-across-industries/module-55-cybersecurity-llms/index.html`**
- Body line 61: broken href `../../part-6-agentic-ai/module-25-agent-safety-production/section-25.1.html` labeled "Section 25.1" — module-25-agent-safety-production does not exist (dissolved); agent safety is now Ch 38 (`module-38-agent-safety-security`).
- Same nav-num "Part XII" / wrong title.

**`part-11-applications-across-industries/module-56-government-llms/index.html`**
- Body line 148: broken href `../../part-9-safety-security-ethics/module-31-strategy-product-roi/section-31.4.html` labeled "Section 31.4 (Vendor Evaluation & Build vs. Buy)" — module-31-strategy-product-roi does not exist; vendor evaluation is in Ch 42 (Part 10).
- Same nav-num "Part XII" / wrong title.

**`part-11-applications-across-industries/module-57-manufacturing-llms/index.html`** — same nav-num "Part XII" / wrong title.

**`part-12-frontiers/module-61-frontier-architectures/index.html`**
- Missing pagefind chapter meta.
- Prereq labels stale: "Chapter 04" (correct), "Chapter 06" (href -> module-07 / Pretraining; label should be "Chapter 7"), "Chapter 09" (href -> module-10 / Inference Optimization; label should be "Chapter 10").
- "What's Next" link target `../../part-10-idea-to-product/index.html` labeled "Part XI" — should be "Part X". Also says "takes you from an idea to a shipped AI product, including unit economics, post-launch monitoring, and multi-provider strategy" — content description is roughly correct for Part 10 but the part labelling is wrong.

**`part-12-frontiers/module-64-agi-trajectories/index.html`**
- Body line 54: broken href `../../capstone/index.html` labeled "capstone project" — capstone now lives at `../../appendices/appendix-t-capstone-project/`.

---

## Cross-cutting findings

1. **Missing `chapter:Chapter N: ...` pagefind meta injection in 23 chapter indexes.** All 23 have the `chapter` attribute on the breadcrumb (search will still partially work), but they lack the explicit `<span class="pagefind-meta-injected" data-pagefind-meta="chapter:Chapter N: Title" hidden="">` block that 43 other chapter indexes include. Affected files (all in module-XX/index.html):
   - module-07, module-08, module-09, module-10, module-11 (Part 2)
   - module-13, module-14, module-15 (Part 3)
   - module-17, module-18, module-19, module-20 (Part 4)
   - module-22, module-23, module-24 (Part 5)
   - module-26, module-27, module-28, module-29 (Part 6)
   - module-31 (Part 7)
   - module-34, module-35 (Part 8)
   - module-37 (Part 9)
   - module-61 (Part 12)

2. **Stale "Chapter NN" labels in prereq lists across 6+ chapter indexes.** The href is correct (points to the right module) but the visible label still says the old chapter number. Pattern: prereq label "Chapter 06" with href `module-07-pretraining-scaling-laws/`. Same for "Chapter 07" -> `module-08-`, "Chapter 08" -> `module-09-`, "Chapter 09" -> `module-10-`, "Chapter 05" -> `module-05-` (where the label uses zero-prefix not "Chapter 5"). Affected: module-00, module-04, module-13, module-26, module-31, module-61. Probably a few more.

3. **Stale Part-XI / Part-XII nav-num labels in 9 chapter indexes.** Pattern: `<span class="nav-num">Part XI</span>` in a Part 10 module, or `<span class="nav-num">Part XII</span>` in a Part 11 module. These are the pre-v10 numbering. Affected files all flagged in P3 above (part-10 module-45, module-48; part-11 module-51 through module-57).

4. **Broken cross-references to dissolved modules** (3 chapter indexes):
   - `part-10-idea-to-product/module-45-prototype-to-production/index.html` → `module-31-strategy-product-roi` (in Part 9)
   - `part-11-applications-across-industries/module-55-cybersecurity-llms/index.html` → `module-25-agent-safety-production` (in Part 6)
   - `part-11-applications-across-industries/module-56-government-llms/index.html` → `module-31-strategy-product-roi` (in Part 9)

5. **Two broken `capstone/index.html` links** (Part 11 index and Part 12 module-64).

6. **One broken `appendix-e-tooling-ecosystem` link** (Part 5 module-25; correct slug is `appendix-e-orchestration-frameworks`).

7. **Section files on disk that yaml does not list** in `part-10/module-40`: `section-40.2.html`, `section-40.3.html` exist but yaml only declares 40.1.

8. **Section card title mismatches vs yaml** in 9 chapter indexes (module-00, module-03, module-04, module-07, module-09, module-20, module-26, module-35, module-64). Most are minor wording deltas (the visible card title is a short variant; yaml has the canonical long form). Note module-64's section 64.5 visibly displays "33.11 What 2026 Settled" — the leading "33.11" is leftover pre-v10 numbering inside the title string.

---

## What the post-v10 reshuffle did NOT break

- Zero references to the renamed appendix letters (M/N/O/P/Q/R/S/T/U) using their OLD topic labels in any index page.
- Zero references to dropped resources (Master Reference Tables, Freshness Index, Glossary, Appendix AD/AE/AF/AI) in any index page.
- All 12 part `<title>` tags are correct with respect to their roman numerals (I-XII).
- All 66 chapter indexes have a section-num prefix that matches the chapter number (P1 from pre-v10 audit appears fully fixed: no more `6.1` cards inside a Chapter 7 module).
- All 64 chapter indexes whose chapter `<title>` includes a number have a matching number (only exception: 4 module indexes in Part 2 whose titles still show `Chapter 0X` — pre-v10 staleness, not v10).
- All chapter modules have on-disk section files that match yaml (except `part-10/module-40` which has 2 extras).

The v10 reshuffle was clean at the part/chapter-index level. The remaining ~28 stale items are all pre-v10 staleness that the in-flight fix agent has not yet swept.
