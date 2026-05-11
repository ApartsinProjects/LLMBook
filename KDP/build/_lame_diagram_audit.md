# Lame Diagram Audit — Building Conversational AI with LLMs and Agents
*Generated: 2026-05-11. Skips Chapter 6 / Quick Wins addressed in _diagram_audit_v60.md.*

---

## Top 15 Lame Diagrams (ranked by improvement impact)

### #1 — Figures 20.1.1 AND 20.1.2: Duplicate "open book" cartoons in the same section
- **File:** `part-5-retrieval-conversation/module-20-rag/section-20.1.html`
- **Type:** Gemini illustration ×2
- **Why lame:** Both are "student with open book" cartoons for RAG. Fig 20.1.1 = "open-book exam"; Fig 20.1.2 = "flipping through reference materials while writing." Functionally identical. The same open-book-exam metaphor also appears in Section 6.7 (Figure 6.7.1) for in-context learning, making this trope appear three times book-wide.
- **Action:** DROP both. Replace with one technical SVG showing the RAG loop (query → retriever → context window → LLM → grounded answer) with annotated failure modes. The adjacent Algorithm 20.1.1 pseudocode already teaches the pipeline; a flowchart with failure-mode callouts would show what the prose cannot.

### #2 — Figures 13.3.1–13.3.5: Five consecutive Gemini cartoons in one data-filtering section
- **File:** `part-4-training-adapting/module-13-synthetic-data/section-13.3.html`
- **Type:** Gemini illustration ×5
- **Why lame:** Quality inspector, second quality inspector, deduplication twins, "diverse dataset," model-collapse photocopy. All five map 1:1 to an adjacent callout or list item in the same section. The section already has a well-designed comparison table. Five decorative cartoons in a data-engineering section with dense code is the single worst illustration cluster in the book.
- **Action:** DROP all five. If one visual is desired, CHANGE TYPE → matplotlib: a horizontal funnel bar chart showing dataset size at each filter stage (generated → after rule filters → after LLM scorer → deduplicated → final training set).

### #3 — Figures 6.6.1 + 6.6.2: Orchestra and "many GPUs" for distributed training
- **File:** `part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.6.html`
- **Type:** Gemini illustration ×2
- **Why lame:** "Orchestra" and generic GPUs illustrations open a section that has four technically precise parallelism diagrams (DDP, FSDP, pipeline, tensor) plus a communication-primitives comparison table. Any distributed computation can be illustrated with an orchestra. These cartoons add zero specificity.
- **Action:** DROP both. The four technical diagrams carry the visual load without competition.

### #4 — Figures 13.1.1 + 13.1.2: Back-to-back decorative openers for synthetic data principles
- **File:** `part-4-training-adapting/module-13-synthetic-data/section-13.1.html`
- **Type:** Gemini illustration ×2
- **Why lame:** "Synthetic data factory" and "seed data garden" appear consecutively before any substantive content. Neither encodes a concept — they encode excitement. The section's inline SVG four-drivers diagram (appearing 60 lines later) is the real useful visual.
- **Action:** DROP Figure 13.1.1 (factory). IMPROVE Figure 13.1.2: matplotlib bar chart comparing annotation costs (expert: $5–$20; crowd: $0.10–$0.50; GPT-4o: $0.005–$0.02; self-hosted: $0.0005–$0.002) using the numbers from the adjacent code fragment.

### #5 — Figure 31.1.1: "Rocket launch" for LLM deployment
- **File:** `part-8-evaluation-production/module-31-production-engineering/section-31.1.html`
- **Type:** Gemini illustration
- **Why lame:** A rocket launching from a laptop is pure excitement signaling. It tells readers nothing about the actual deployment challenges covered in the section (async handling, API contracts, scaling). The section's own Figure 31.1.2 (restaurant kitchen architecture SVG) is the real visual anchor.
- **Action:** DROP. Figure 31.1.2 already serves as the section opener.

### #6 — Figure 14.1.1: "Old dog new tricks" for fine-tuning
- **File:** `part-4-training-adapting/module-14-fine-tuning-fundamentals/section-14.1.html`
- **Type:** Gemini illustration
- **Why lame:** A cartoon dog teaches nothing about transfer learning, frozen parameters, or catastrophic forgetting. The section has an adaptation-spectrum SVG (Figure 14.1.6) that is the correct visual anchor. This illustration is a space-filler opener.
- **Action:** DROP. Move the adaptation-spectrum SVG to open the section.

### #7 — Figures 11.1.2, 11.1.3, 11.1.4: Three consecutive prompting-strategy cartoons
- **File:** `part-3-working-with-llms/module-11-prompt-engineering/section-11.1.html`
- **Type:** Gemini illustration ×3
- **Why lame:** "Students studying" (zero/few/CoT), "cooking without a recipe" (zero vs few-shot), and "director of the show" (system prompt) appear in sequence. All three restate information already in the code examples and the high-quality Figure 11.1.7 anatomy-of-a-prompt SVG.
- **Action:** DROP all three. If one Gemini illustration is retained, keep cooking (zero-shot = no recipe, few-shot = example dishes).

### #8 — Figure 14.4.1: Cloud-factory illustration redundant with adjacent callout box
- **File:** `part-4-training-adapting/module-14-fine-tuning-fundamentals/section-14.4.html`
- **Type:** Gemini illustration
- **Why lame:** Shows ingredients going into a cloud-shaped factory. The callout box directly below it reads: "Think of provider fine-tuning APIs as a cloud workshop where you send raw materials and receive a finished product." Caption and callout are textually identical.
- **Action:** DROP. Callout is more informative than the cartoon.

### #9 — Figure 6.5.1: "Adam as GPS navigator"
- **File:** `part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.5.html`
- **Type:** Gemini illustration
- **Why lame:** The metaphor of a GPS navigator imprecisely maps onto per-parameter adaptive learning rates. The navigator routes to different destinations; Adam scales gradients by accumulated variance. The section has the exact AdamW equations.
- **Action:** CHANGE TYPE → matplotlib. Two-panel loss landscape contour plot: (left) SGD oscillating in a narrow ravine; (right) Adam descending diagonally.

### #10 — Figure 6.5.2: "Don't sprint when you wake up" for learning rate warmup
*(Already converted to matplotlib in v6.3.0 — keep for the record.)*

### #11 — Figure 21.2.1: "Persona dressing room" immediately before a good SVG
- **File:** `part-5-retrieval-conversation/module-21-conversational-ai/section-21.2.html`
- **Type:** Gemini illustration
- **Why lame:** A robot trying on theatrical masks precedes the concentric-rectangles SVG (Figure 21.2.5) that actually explains persona layers.
- **Action:** DROP. The concentric SVG is sufficient.

### #12 — Figure 6.2.1: "Puzzle" for CLM vs MLM distinction
- **File:** `part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.2.html`
- **Type:** Gemini illustration
- **Why lame:** Puzzles have unique solutions; CLM's next-token prediction is a probability distribution over the full vocabulary. The puzzle metaphor is imprecise enough to be misleading.
- **Action:** CHANGE TYPE → inline SVG. Horizontal token-sequence boxes: left panel CLM with previous tokens visible and rightmost masked with "?"; right panel MLM with middle tokens [MASK].

### #13 — Figures 6.4.1 + 6.4.2: Deduplication clones and gold panning
- **File:** `part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.4.html`
- **Type:** Gemini illustration ×2
- **Why lame:** Both cartoons describe "filter out bad stuff" with different props in a section already heavy with MinHash code and tables.
- **Action:** DROP both. IMPROVE Figure 6.4.3 with a matplotlib waterfall chart showing token counts at each pipeline stage using FineWeb numbers (100 TB raw → 15T after curation).

### #14 — Figure 6.3.1: "Kitchen recipe" opener for scaling laws
- **File:** `part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.3.html`
- **Type:** Gemini illustration
- **Why lame:** "Ingredients = data, oven = compute, recipe = parameters" is an imprecise warm-up for a section that immediately produces the real insight: power laws on log-log plots (Figures 6.3.2 and 6.3.3 — both already matplotlib charts post-v6.3.0).
- **Action:** DROP. Move Figure 6.3.2 to the section opener.

### #15 — Figure 29.1.1: "Quality inspector on conveyor belt" for LLM evaluation
- **File:** `part-8-evaluation-production/module-29-evaluation-observability/section-29.1.html`
- **Type:** Gemini illustration
- **Why lame:** Generic QA-line imagery; could illustrate any quality-control process. Teaches nothing specific about LLM evaluation.
- **Action:** DROP. If a visual opener is desired, matplotlib scatter plot of human preference scores vs BLEU scores showing poor correlation — the motivation for LLM-as-judge.

---

## Per-Chapter Count

| Chapter | Lame figures | Priority |
|---|---:|---|
| Ch 6 (Pretraining + Scaling) | 10 | HIGH |
| Ch 13 (Synthetic Data) | 7 | HIGH |
| Ch 11 (Prompt Engineering) | 3 | MEDIUM |
| Ch 20 (RAG) | 2 | HIGH |
| Ch 14 (Fine-Tuning) | 2 | MEDIUM |
| Ch 31 (Production Eng) | 1 | MEDIUM |
| Ch 21 (Conversational) | 1 | LOW |
| Ch 29 (Evaluation) | 1 | LOW |
| **Total** | **27** | |

---

## Patterns Observed

**A. "Warm-up cartoon" antipattern (~12 of 27)** — every section opens with a Gemini illustration that restates the section heading as a metaphor. Pure clip-art-style padding.

**B. Metaphor-before-math displacement** — Gemini cartoon appears first, consumes reader attention, then a precise quantitative visual (formula, chart, SVG) does the actual teaching. The cartoon competes with the content.

**C. Triple redundancy (cartoon + caption + callout = same sentence three times)** — illustration adjacent to a callout box that contains the identical metaphor in prose. Worst example: section 14.4 cloud-factory + "Cloud Workshop" callout.

**D. "Open book exam" cliché — three deployments for three different concepts** — same imagery used for in-context learning, RAG retrieval, and RAG generation. Trains readers to stop reading captions.

**E. Illustration clusters in dense code sections** — sections 13.3 (5 cartoons) and 6.4 (3 cartoons) are data-engineering sections dominated by code and tables. Highest cartoon density in the book sits on top of the most code-heavy content.

---

**Net recommendation:** Drop 15 illustrations outright; convert 7 to matplotlib/SVG. Net effect: lose 15 figures, gain 7 better ones. Reduces ~27 weak figures to ~12 improved ones. The genuinely clever Gemini illustrations that survive (speculative decoding, latency-cost-quality trilemma, RLHF talent show, agent control room) become more impactful when no longer drowned in decorative filler.

*Report by `book-09-visual-learning` agent, audit pass v6.5, 2026-05-11.*
