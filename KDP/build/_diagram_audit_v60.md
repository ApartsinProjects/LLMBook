# Diagram Type Audit — v6.0 Snapshot

**Date:** 2026-05-11
**Scope:** all `part-*/module-*/section-*.html` + appendix sections (~140 files, ~320 visual elements)
**Goal:** flag figures where a different visualization type would be more effective.

---

## Executive Summary

1. **Chapter 6 (Pretraining and Scaling Laws) has a systematic Gemini-for-matplotlib substitution problem.** Three figures have alt text that accurately describes a real chart, but the actual image is a Gemini cartoon. Figures **6.3.2** (power-law plot), **6.3.3** (Chinchilla vs. Kaplan), and **6.5.2** (LR warmup) should be matplotlib figures; the data for 6.5.2 already exists as code output in the section.

2. **Two Gemini cartoons are redundant before superior matplotlib charts.** The GPT rocket cartoon (Fig 6.1.2) appears 14 lines before the parameter-growth chart (Fig 6.1.6), and the emergent-abilities butterfly (Fig 6.3.4) appears three paragraphs before the metric-mirage chart (Fig 6.3.11). Both cartoons should be removed.

3. **The catastrophic-forgetting crossing-curve chart is duplicated across sections 14.1 and 15.7** with essentially identical visual content. One should become a cross-reference.

4. **Figure 7.4.3 and Figure 33.1.1 both make quantitative claims the visual cannot support.** The multilingual performance-gap claim ("40+ pp gap") needs a bar chart; the AI-readiness radar chart should be converted to a horizontal bar chart (radars with <6 axes systematically distort relative magnitude through quadratic area scaling).

5. **19 of 26 chapters surveyed have zero flagged issues.** The book's visual strategy (Gemini openers for tone, Mermaid/SVG for flows, matplotlib for data) works well when applied correctly. The problems are concentrated in Chapter 6.

---

## Top 10 Highest-Priority Redesigns

### #1 — Figure 6.3.2 "Power law in action"
- **Current:** Gemini cartoon `scaling-laws-power-law.png`
- **Problem:** Alt text reads "a log-log plot showing power law relationships," and the surrounding text gives three exact exponents (α_N=0.076, α_D=0.095, α_C=0.050). A reader expects axes, not a kitchen metaphor.
- **Recommended:** Matplotlib log-log line chart, three curves (L vs N, L vs D, L vs C), slopes annotated, irreducible-loss floor marked.

### #2 — Figure 6.3.3 "Chinchilla vs Kaplan"
- **Current:** Gemini cartoon `chinchilla-vs-kaplan.png`
- **Problem:** Caption promises "two different recipes for spending your compute budget"; text gives exact exponents (N_opt ∝ C^0.50 vs Kaplan's 5:2). The cartoon cannot show this quantitative difference.
- **Recommended:** Matplotlib dual-curve log-log chart (optimal N vs compute), real models (GPT-3, Chinchilla, Gopher, Llama 1) overlaid as scatter points.

### #3 — Figure 6.5.2 "Learning rate warmup"
- **Current:** Gemini cartoon `learning-rate-warmup.png`
- **Problem:** Alt text says "A graph showing learning rate warmup followed by decay" — but the image is a cartoon. Code Fragments 6.5.2 + 6.5.3 in the same section compute the schedules and print values; the data is already there.
- **Recommended:** Matplotlib dual-line plot (cosine + WSD on same axes, step vs LR), generated from existing code.

### #4 — Figure 7.4.3 "Multilingual QA performance gap"
- **Current:** PNG with truncated alt text, ambiguous content; caption claims "40+ percentage points gap"
- **Problem:** Quantitative claim not supported by a quantitative chart.
- **Recommended:** Horizontal bar chart, 10 languages sorted by benchmark accuracy, English as reference.

### #5 — Figure 15.5.2 "Temperature softmax distribution"
- **Current:** Gemini cartoon `temperature-softmax.png`
- **Problem:** Caption describes a precise mathematical effect (temperature scaling of softmax). Cartoons cannot show probability redistribution.
- **Recommended:** Matplotlib 3-panel bar chart (same logits at T=0.5, 1.0, 3.0). NOTE: a similar chart was generated for Figure 5.2.4 in this commit — pattern can be re-used.

### #6 — Figure 6.1.2 GPT rocket cartoon
- **Current:** Gemini rocket cartoon, captioned "took off like a rocket"
- **Problem:** 14 lines later, Figure 6.1.6 is a real matplotlib chart of parameter growth covering the same concept.
- **Recommended:** **REMOVE** Figure 6.1.2. Keep the rocket metaphor in prose only.

### #7 — Figures 14.1.3 + 15.7.3 duplicate crossing-curves chart
- **Current:** Two near-identical charts in different chapters
- **Problem:** Visually indistinguishable; same crossing-curves of task vs general performance
- **Recommended:** Make 14.1 canonical. In 15.7, replace image with cross-reference callout.

### #8 — Figure 6.3.4 emergent-abilities butterfly cartoon
- **Current:** Gemini butterfly cartoon before Figure 6.3.11 (real matplotlib metric-mirage chart)
- **Problem:** Pure redundancy.
- **Recommended:** **REMOVE** the butterfly. Move section header to appear directly before Figure 6.3.11.

### #9 — Figure 9.4.3 "LLM request latency"
- **Current:** matplotlib chart with truncated alt, undefined axes in caption
- **Problem:** Practitioners can't use the chart for capacity planning without knowing what the axes are.
- **Recommended:** **ENHANCE caption** with explicit axis labels and a "what to notice" line. If axes lack labels in the chart itself, regenerate.

### #10 — Figure 33.1.1 "AI Readiness Radar"
- **Current:** 4-axis radar chart (Data=4, Tech=3, Org=2, Talent=3)
- **Problem:** Radars with <6 axes distort relative magnitude through quadratic area scaling. The weakest pillar appears less weak than it is.
- **Recommended:** Horizontal bar chart on a 0–5 scale with a "minimum viable" reference line at 3.

---

## Per-Chapter Summary

| Chapter | n_figures | n_flagged | Dominant issue |
|---------|----------:|----------:|---|
| Ch 0 ML/PyTorch Foundations | 10 | 0 | Clean |
| Ch 1 NLP + Text Representation | 12 | 0 | Clean |
| Ch 2 Tokenization | 10 | 0 | Clean |
| Ch 3 Sequence Models | 8 | 0 | Clean |
| Ch 4 Transformer Architecture | 14 | 0 | **Best-illustrated chapter** |
| Ch 5 Decoding / Text Generation | 8 | 0 | Clean |
| **Ch 6 Pretraining and Scaling Laws** | **28** | **6** | **Cartoons substituting for required data charts** |
| Ch 7 Modern LLM Landscape | 10 | 2 | Multilingual perf gap chart needed |
| Ch 8 Reasoning / Test-Time Compute | 6 | 0 | Clean |
| Ch 9 Inference Optimization | 14 | 1 | Fig 9.4.3 caption ambiguity |
| Ch 10 LLM APIs | 8 | 0 | Clean |
| Ch 11 Prompt Engineering | 12 | 0 | Decision flowcharts excellent |
| Ch 12 Hybrid ML/LLM | 10 | 0 | Clean |
| Ch 13 Synthetic Data | 12 | 0 | Clean |
| Ch 14 Fine-Tuning Fundamentals | 10 | 2 | Duplicate crossing-curves chart |
| Ch 15 PEFT | 18 | 3 | Temperature cartoon; duplicate forgetting chart |
| Ch 17 Alignment / RLHF / DPO | 8 | 0 | Clean |
| Ch 18 Interpretability | 8 | 0 | Clean |
| Ch 19-21 Embeddings / RAG / Conversation | 12 | 0 | Clean |
| Ch 22-26 Agentic AI | 18 | 0 | Clean across 6 sections |
| Ch 29 Evaluation / Observability | 6 | 0 | Clean |
| Ch 31 Production Engineering | 10 | 0 | Clean |
| Ch 32 Safety, Ethics, Regulation | 10 | 0 | EU AI Act tier chart is among the book's best |
| Ch 33 Strategy / Product / ROI | 4 | 1 | Radar should be bar chart |
| Ch 34 Emerging Architectures | 10 | 0 | Clean |
| Appendices A-V | ~20 | 0 | Code-heavy; appropriate visuals |

---

## Chapters That Look Great As-Is

- **Ch 4 (Transformer Architecture):** the most visually complete chapter — all SVG architecture diagrams correctly typed
- **Ch 11 (Prompt Engineering):** inline SVG decision flowcharts well-matched to sequential decision content
- **Ch 17 (Alignment / RLHF / DPO):** Constitutional AI framework + preference-dataset SVG are accurate process diagrams
- **Ch 22-26 (Agentic AI):** tool-use protocol diagrams, agent-loop SVGs, multi-agent topology — all appropriate types
- **Ch 32 (Safety, Ethics, Regulation):** EU AI Act risk-tier diagram is among the book's best-executed technical diagrams

---

## Summary Statistics

| Metric | Count |
|--------|------:|
| Section HTML files surveyed | ~140 |
| Total visual elements estimated | ~320 |
| Gemini illustrations in technical positions where data charts belong | 3 |
| Quantitative captions with no supporting chart | 2 |
| Near-duplicate figures across chapters | 2 pairs |
| Redundant cartoon before superior chart | 2 |
| Caption ambiguity (axes undefined) | 1 |
| Chapters with zero flagged issues | 19 of 26 |
| **Highest-priority chapter for remediation** | **Chapter 6** (6 flags) |

---

*Generated by `book-09-visual-learning` agent, audit pass v6.0, 2026-05-11.*
