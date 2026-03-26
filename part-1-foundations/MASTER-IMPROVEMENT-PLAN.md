# Part I: Foundations, Master Improvement Plan

**Consolidated from 13 agent review reports (36 agents)**
**Date:** 2026-03-26

---

## Executive Summary

### What Is Strong

Part I has a sound six-module arc (prerequisites, NLP domain, tokenization, sequence models, Transformer, decoding) with no dependency violations and a clean difficulty ramp from Basic to Advanced. The strongest assets are:

- **Section 4.2 (Build a Transformer from Scratch):** The crown jewel of Part I; ~300-line lab with shape annotations and progressive scaffolding.
- **Module 02 (Tokenization):** Distinctive pedagogical choice to treat tokenization as center-stage. The BPE from-scratch lab and "token tax" framing are above average.
- **Module 05 (Decoding):** Comprehensive and current; covers contrastive decoding, speculative decoding, grammar-constrained generation, watermarking, and diffusion LMs.
- **Narrative voice:** Warm, conversational register from Module 01 onward; effective "Big Picture" callouts; rich SVG diagrams; consistent four-question structure (WHAT/WHY/HOW/WHEN).
- **Code quality:** Nearly every concept has runnable code with actual output (with notable exceptions listed below).

### What Needs Work

1. **Missing content blocks:** Information theory (entropy, perplexity, KL divergence) is entirely absent despite being promised in the syllabus. Adam/AdamW optimizer is used in code across four modules but never explained. Self-supervised learning is never defined.
2. **Depth gaps:** Several key concepts lack the "WHY" explanation (negative sampling cost, GloVe co-occurrence ratio, LSTM gate design, sqrt(d_k) scaling, FFN role, length normalization).
3. **Structural inconsistency:** Module 00 has three competing CSS templates; Module 01 deviates from the quiz/takeaway template; six different callout class naming conventions exist across the 23 sections.
4. **Uneven exercises:** Module 01 back-loads all exercises into Section 1.4; no module has create-level (Bloom's L6) exercises; "modify and observe" exercises are missing from most sections.
5. **Visual gaps:** Module 04 has only 8 of 20+ planned diagrams; several critical diagrams (LSTM cell, causal mask, Pre-LN vs. Post-LN, RoPE) are missing.
6. **Cross-module transitions:** 3 of 5 module boundaries lack both forward and backward references.

---

## TIER 1: BLOCKING FIXES (Must Do Before Release)

These issues prevent students from understanding core concepts or cause factual errors.

### T1-01: Add Information Theory Subsection to Section 4.1

| Field | Detail |
|-------|--------|
| **Source reports** | Curriculum Alignment, Self-Containment (Phase 4), Learning Quality (Phase 7) |
| **Module/Section** | Module 04, Section 4.1 |
| **What to change** | Add a new subsection (~800 words) covering entropy (with coin-flip example), cross-entropy as the loss we minimize, perplexity = 2^(cross-entropy), KL divergence, and mutual information. Include worked numeric examples for each concept. |
| **Why blocking** | Syllabus promises this content. Entropy is used in Section 5.2 code; perplexity appears in scaling laws (Part II); KL divergence appears in alignment (Part III). Students have no formal grounding. |
| **Effort** | LARGE |

### T1-02: Add Adam/AdamW Optimizer Explanation

| Field | Detail |
|-------|--------|
| **Source reports** | Self-Containment (Phase 4), Code Pedagogy (Phase 2), Learning Quality (Phase 7) |
| **Module/Section** | Module 00, Section 0.3 (before first use of `optim.Adam`) |
| **What to change** | Add a 2-paragraph callout explaining: momentum (smooths noisy gradients), adaptive per-parameter learning rates, and AdamW's decoupled weight decay. Include a comparison table: SGD vs. Adam convergence characteristics. |
| **Why blocking** | Adam appears in code across 4 modules. Students cannot reason about optimizer choice without this explanation. |
| **Effort** | SMALL |

### T1-03: Fix Section 0.4 Cross-Reference Error

| Field | Detail |
|-------|--------|
| **Source reports** | Teaching Flow, Structural (Phase 3), Self-Containment (Phase 4), Integrity (Phase 8), Learning Quality (Phase 7) |
| **Module/Section** | Module 00, Section 0.4, closing "What Comes Next" paragraph |
| **What to change** | Change "transformers (Module 02)" to "transformers (Module 04)." |
| **Why blocking** | Factual navigation error. Sends students to the wrong module. Flagged in 5 separate reports. |
| **Effort** | SMALL |

### T1-04: Fix Cross-Validation Standard Deviation Mismatch

| Field | Detail |
|-------|--------|
| **Source reports** | Integrity (Phase 8) |
| **Module/Section** | Module 00, Section 0.1 |
| **What to change** | Change "0.0375" to "0.0383" to match the code output displayed above it. |
| **Why blocking** | Prose contradicts computed output on the same page. Undermines trust. |
| **Effort** | SMALL |

### T1-05: Standardize BERT Date Across Modules

| Field | Detail |
|-------|--------|
| **Source reports** | Integrity (Phase 8) |
| **Module/Section** | Modules 01 and 04 |
| **What to change** | Use "BERT (Devlin et al., 2018)" consistently, since arXiv date convention is used for all other papers. Update Section 4.3 from "2019" to "2018." |
| **Why blocking** | Inconsistent dates for the same paper erode credibility. |
| **Effort** | SMALL |

---

## TIER 2: HIGH PRIORITY FIXES (Significant Quality Improvement)

### Content Depth Fixes

### T2-01: Add Cross-Entropy Log Magnification Table (Section 0.1)

| Field | Detail |
|-------|--------|
| **Source reports** | Deep Explanation (Phase 1), Code Pedagogy (Phase 2), Engagement (Phase 5), Learning Quality (Phase 7) |
| **Module/Section** | Module 00, Section 0.1 |
| **What to change** | Add a 4-row table after the cross-entropy formula: P=0.9 / loss=0.105 / "Confidently correct"; P=0.5 / loss=0.693 / "Coin flip"; P=0.1 / loss=2.303 / "Mostly wrong"; P=0.01 / loss=4.605 / "Catastrophically wrong." Add: "The loss has a magnifying glass for low-confidence predictions." |
| **Effort** | SMALL |

### T2-02: Add Negative Sampling Cost Quantification (Section 1.3)

| Field | Detail |
|-------|--------|
| **Source reports** | Deep Explanation, Self-Containment (Phase 4), Learning Quality (Phase 7) |
| **Module/Section** | Module 01, Section 1.3 |
| **What to change** | Add cost comparison: full softmax = 100K+ dot products per step; negative sampling (k=5) = 6 dot products; 16,000x reduction. Add note that this makes billion-pair training feasible. |
| **Effort** | SMALL |

### T2-03: Add GloVe Co-Occurrence Ratio Worked Example (Section 1.3)

| Field | Detail |
|-------|--------|
| **Source reports** | Deep Explanation, Self-Containment, Learning Quality |
| **Module/Section** | Module 01, Section 1.3 |
| **What to change** | Add a 3-row table: P(solid\|ice)/P(solid\|steam) >> 1; P(gas\|ice)/P(gas\|steam) << 1; P(water\|ice)/P(water\|steam) near 1. Explain that GloVe trains vectors to reproduce these log-ratios. |
| **Effort** | SMALL |

### T2-04: Add WordPiece vs. BPE Concrete Comparison (Section 2.2)

| Field | Detail |
|-------|--------|
| **Source reports** | Deep Explanation, Self-Containment, Learning Quality (Phase 7) |
| **Module/Section** | Module 02, Section 2.2 |
| **What to change** | Add example: BPE picks ('th','e') at frequency 1000; WordPiece might pick ('qu','antum') at frequency 5 if the pair is surprisingly frequent relative to its parts. "BPE asks 'what appears most often?' WordPiece asks 'what appears most surprisingly often?'" |
| **Effort** | SMALL |

### T2-05: Add Viterbi Decoding Worked Example (Section 2.2)

| Field | Detail |
|-------|--------|
| **Source reports** | Deep Explanation, Self-Containment, Learning Quality |
| **Module/Section** | Module 02, Section 2.2 |
| **What to change** | Add a step-by-step lattice example: 4-character word, 3 possible segmentations, log-probabilities on edges, dynamic programming walk-through showing optimal path selection. |
| **Effort** | MEDIUM |

### T2-06: Add Vanishing Gradient Quantification (Section 3.1)

| Field | Detail |
|-------|--------|
| **Source reports** | Deep Explanation, Engagement (Phase 5) |
| **Module/Section** | Module 03, Section 3.1 |
| **What to change** | Add: "If the gradient shrinks by 10% per step, after 100 steps: 0.9^100 = 0.0000266. That is not a small gradient. That is no gradient." |
| **Effort** | SMALL |

### T2-07: Add LSTM Gate Design Rationale (Section 3.1)

| Field | Detail |
|-------|--------|
| **Source reports** | Deep Explanation, Learning Quality (Phase 7) |
| **Module/Section** | Module 03, Section 3.1 |
| **What to change** | Add explanation: forget gate answers "what to discard?", input gate answers "what to remember?", output gate answers "what to reveal?" Also add the LSTM cell state as "additive shortcut" insight: additive updates avoid vanishing gradients. Connect to residual connections in Module 04. |
| **Effort** | SMALL |

### T2-08: Add sqrt(d_k) Scaling Intuition (Section 4.1)

| Field | Detail |
|-------|--------|
| **Source reports** | Deep Explanation, Learning Quality |
| **Module/Section** | Module 04, Section 4.1 |
| **What to change** | Add: "Without scaling, dot products grow with d_k. For d_k=64, dot products have standard deviation 8, pushing softmax into extreme tails where gradients are near zero. Dividing by sqrt(d_k) restores variance to 1." Move full derivation to an optional sidebar. |
| **Effort** | SMALL |

### T2-09: Add FFN Role Explanation with Geva Citation (Section 4.1)

| Field | Detail |
|-------|--------|
| **Source reports** | Deep Explanation, Engagement (Phase 5), Learning Quality (Phase 7) |
| **Module/Section** | Module 04, Section 4.1 |
| **What to change** | Add "Paper Spotlight" sidebar: FFN layers act as key-value memories storing factual knowledge (Geva et al., 2021). Use "Attention reads, FFN thinks" analogy. |
| **Effort** | SMALL |

### T2-10: Add Length Normalization Explanation (Section 5.1)

| Field | Detail |
|-------|--------|
| **Source reports** | Deep Explanation |
| **Module/Section** | Module 05, Section 5.1 |
| **What to change** | Add: "Log-probabilities are negative. Summing more terms produces a more negative total. Without normalization, beam search always prefers shorter sequences." |
| **Effort** | SMALL |

### T2-11: Add Self-Supervised Learning Definition (Section 0.1)

| Field | Detail |
|-------|--------|
| **Source reports** | Self-Containment (Phase 4), Learning Quality |
| **Module/Section** | Module 00, Section 0.1 |
| **What to change** | Add callout after supervised learning subsection defining supervised, unsupervised, and self-supervised learning. Note that LLM pretraining is self-supervised. |
| **Effort** | SMALL |

### T2-12: Add Jacobian Matrix Definition (Section 3.1)

| Field | Detail |
|-------|--------|
| **Source reports** | Self-Containment (Phase 4), Learning Quality |
| **Module/Section** | Module 03, Section 3.1 |
| **What to change** | Add a "Math Checkpoint" callout defining the Jacobian with a 2x2 numeric example. Mark the surrounding gradient analysis as "skippable for intuition-first readers." |
| **Effort** | SMALL |

### T2-13: Mark Section 3.2 Backprop-Through-Attention as Optional

| Field | Detail |
|-------|--------|
| **Source reports** | Self-Containment, Learning Quality, Teaching Flow |
| **Module/Section** | Module 03, Section 3.2 |
| **What to change** | Wrap the Jacobian/matrix-calculus material in a collapsible "Advanced Deep Dive (Optional)" container. Provide a one-sentence summary takeaway before it. |
| **Effort** | SMALL |

### T2-14: Add Cross-Module Bridge Sentences (All Module Boundaries)

| Field | Detail |
|-------|--------|
| **Source reports** | Teaching Flow, Structural, Self-Containment, Learning Quality |
| **Module/Section** | End of Modules 00, 02, 04; Start of Modules 01, 03, 05 |
| **What to change** | Add 1-2 sentence forward reference at the end of every module's final section ("What Comes Next"); add 1-2 sentence backward reference at the start of every module's first section ("Where We Are"). |
| **Effort** | SMALL |

### T2-15: Bridge Cross-Entropy from Classification to Language Modeling (Section 4.2)

| Field | Detail |
|-------|--------|
| **Source reports** | Self-Containment, Learning Quality |
| **Module/Section** | Module 04, Section 4.2 |
| **What to change** | Add paragraph before training loop: "Next-token prediction is classification. At each position, the model performs a V-way classification over the vocabulary. Cross-entropy loss from Section 0.1 applies directly." |
| **Effort** | SMALL |

### Structural and Visual Fixes

### T2-16: Add Quizzes and Key Takeaways to Module 01 Sections 1.1, 1.2, 1.3

| Field | Detail |
|-------|--------|
| **Source reports** | Structural (Phase 3), Visual/Exercise (Phase 2), Teaching Flow |
| **Module/Section** | Module 01, Sections 1.1, 1.2, 1.3 |
| **What to change** | Add 3-5 quiz questions with details/summary reveal answers and a Key Takeaways box to each section. Redistribute some exercises from Section 1.4 into earlier sections. |
| **Effort** | MEDIUM |

### T2-17: Create Unified CSS Template (shared-styles.css)

| Field | Detail |
|-------|--------|
| **Source reports** | Visual Polish (Phase 9-10), Structural, Integrity |
| **Module/Section** | All 23 sections + 6 index pages |
| **What to change** | Create a single `shared-styles.css` with the majority template variables (`--primary/#1a1a2e`, `--accent/#0f3460`, `--highlight/#e94560`). Standardize callout classes to `callout big-picture`, `callout key-insight`, `callout note`, `callout warning`. Standardize code font, output block naming (`.code-output`), quiz format (`details/summary`), body font size (17px), content wrapper (`<main class="content">`). |
| **Effort** | LARGE |

### T2-18: Add Chapter Header Banners to Sections 0.2, 0.3, 0.4

| Field | Detail |
|-------|--------|
| **Source reports** | Visual Polish (Phase 9-10) |
| **Module/Section** | Module 00, Sections 0.2, 0.3, 0.4 |
| **What to change** | Add the `.chapter-header` gradient banner used by all other sections. Replace bare `<span>` + `<h1>` with `<header class="chapter-header">`. |
| **Effort** | SMALL |

### T2-19: Convert Section 0.4 Quizzes from JavaScript to details/summary

| Field | Detail |
|-------|--------|
| **Source reports** | Visual/Exercise (Phase 2), Visual Polish (Phase 9-10) |
| **Module/Section** | Module 00, Section 0.4 |
| **What to change** | Replace `checkAnswer()` onclick handlers with native `<details>/<summary>` elements matching the pattern used in all other modules. |
| **Effort** | SMALL |

### T2-20: Add Missing Module 04 Diagrams (Top 5)

| Field | Detail |
|-------|--------|
| **Source reports** | Visual/Exercise (Phase 2) |
| **Module/Section** | Module 04 |
| **What to change** | Add: (1) Pre-LN vs. Post-LN comparison SVG, (2) Residual stream information flow SVG, (3) Positional encoding heatmap (Python/matplotlib), (4) Training loss curve for the 4.2 lab, (5) RoPE rotation visualization SVG. |
| **Effort** | LARGE |

### T2-21: Add LSTM Cell Diagram (Section 3.1)

| Field | Detail |
|-------|--------|
| **Source reports** | Visual/Exercise (Phase 2) |
| **Module/Section** | Module 03, Section 3.1 |
| **What to change** | Add SVG diagram of the LSTM cell with forget gate, input gate, output gate, and cell state clearly labeled. |
| **Effort** | MEDIUM |

### T2-22: Add Code Output to Section 0.4 (RL) and Make REINFORCE Runnable

| Field | Detail |
|-------|--------|
| **Source reports** | Code Pedagogy (Phase 2), Engagement (Phase 5) |
| **Module/Section** | Module 00, Section 0.4 |
| **What to change** | Add a complete training loop (10-15 lines) that trains for 1000 episodes. Show output: reward improving over episodes. Add a reward curve plot. |
| **Effort** | MEDIUM |

### T2-23: Add "Modify and Observe" Exercises Across All Modules

| Field | Detail |
|-------|--------|
| **Source reports** | Code Pedagogy (Phase 2) |
| **Module/Section** | All modules |
| **What to change** | Add 2-3 "modify and observe" prompts per section, each asking students to change one parameter and describe the effect. Priority sections: 0.4 (RL), 1.1-1.3, 3.1-3.3, 5.1-5.4. |
| **Effort** | MEDIUM |

### T2-24: Add One-Hot Equidistance Callout (Section 1.2)

| Field | Detail |
|-------|--------|
| **Source reports** | Engagement (Phase 5), Learning Quality |
| **Module/Section** | Module 01, Section 1.2 |
| **What to change** | Add callout: "In one-hot space, 'dog' is exactly as far from 'puppy' as it is from 'quantum.' Every word is an island. This single limitation motivated the word embeddings revolution in Section 1.3." |
| **Effort** | SMALL |

### T2-25: Add Decision Framework for Decoding Methods (Section 5.2)

| Field | Detail |
|-------|--------|
| **Source reports** | Learning Quality, Engagement |
| **Module/Section** | Module 05, Section 5.2 |
| **What to change** | Add a roadmap table or decision tree at the start of Section 5.2 listing all sampling methods, their one-line purpose, and when to use each. Add comparison table at end with columns: What it controls, Typical range, When to use, When to avoid. |
| **Effort** | SMALL |

### T2-26: Add Temperature vs. Top-p Misconception Callout (Section 5.2)

| Field | Detail |
|-------|--------|
| **Source reports** | Learning Quality (Phase 7) |
| **Module/Section** | Module 05, Section 5.2 |
| **What to change** | Add "Common Misconception" callout explaining that temperature reshapes the distribution while top-p truncates it. Note that temperature=0.1 with top-p=0.9 is almost identical to temperature=0.1 alone. |
| **Effort** | SMALL |

### T2-27: Add Word2Vec Misconception Callout (Section 1.3)

| Field | Detail |
|-------|--------|
| **Source reports** | Learning Quality (Phase 7) |
| **Module/Section** | Module 01, Section 1.3 |
| **What to change** | Add "Common Misconception" callout after analogy section: Word2Vec does not understand meaning; it learns distributional similarity. Include bias example (man:programmer :: woman:homemaker) as evidence. |
| **Effort** | SMALL |

### T2-28: Rewrite Section 4.1 Opening (Impact First, History Second)

| Field | Detail |
|-------|--------|
| **Source reports** | Engagement (Phase 5), Teaching Flow |
| **Module/Section** | Module 04, Section 4.1 |
| **What to change** | Replace the paper-history opening with: "This is the architecture inside every AI you have ever used. ChatGPT, Claude, Gemini, Llama: they are all Transformers." Follow with the 2017 paper history. |
| **Effort** | SMALL |

### T2-29: Expand Syllabus Coverage: TF-IDF Depth (Section 1.2)

| Field | Detail |
|-------|--------|
| **Source reports** | Curriculum Alignment |
| **Module/Section** | Module 01, Section 1.2 |
| **What to change** | Add sublinear TF scaling (`1 + log(tf)` variant), document length normalization, and brief mention of vector space model for retrieval. These are explicitly promised in the syllabus. |
| **Effort** | MEDIUM |

### T2-30: Add Speculative Decoding Mathematical Guarantee (Section 5.3)

| Field | Detail |
|-------|--------|
| **Source reports** | Learning Quality, Engagement |
| **Module/Section** | Module 05, Section 5.3 |
| **What to change** | Add "Why Does This Work?" sidebar explaining the rejection sampling scheme, acceptance probability formula, and the proof that output distribution is identical to the target model. |
| **Effort** | SMALL |

---

## TIER 3: MEDIUM PRIORITY FIXES (Nice to Have)

### Content Enrichment

| # | Source Report(s) | Module | Section | What to Change | Effort |
|---|-----------------|--------|---------|---------------|--------|
| T3-01 | Deep Explanation | 00 | 0.1 | Add L1 vs. L2 regularization geometric intuition (diamond vs. circle constraint diagram) | SMALL |
| T3-02 | Deep Explanation | 00 | 0.2 | Add BatchNorm loss-smoothing mechanism (Santurkar et al., 2018) | SMALL |
| T3-03 | Deep Explanation | 01 | 1.3 | Add embedding dimension choice justification (Mikolov dimension sweep, plateau at 300) | SMALL |
| T3-04 | Deep Explanation | 01 | 1.4 | Add ELMo layer evidence (same word, different layers, different representations) | SMALL |
| T3-05 | Deep Explanation | 01 | 1.4 | Add pre-train/fine-tune medical training analogy | SMALL |
| T3-06 | Deep Explanation | 02 | 2.2 | Add byte-level BPE mechanism explanation (256-byte base vocabulary) | SMALL |
| T3-07 | Deep Explanation | 02 | 2.2 | Quantify tokenizer-free model tradeoffs (4x sequence length, O(n^2) cost) | SMALL |
| T3-08 | Deep Explanation | 03 | 3.2 | Explain why dot-product attention works (shared embedding space) | SMALL |
| T3-09 | Deep Explanation | 04 | 4.1 | Explain Pre-LN vs. Post-LN stability (gradient magnitude at initialization) | SMALL |
| T3-10 | Deep Explanation | 04 | 4.1 | Add residual connection gradient highway explanation + "residual stream" sidebar (Elhage et al., 2021) | SMALL |
| T3-11 | Deep Explanation | 04 | 4.1 | Add parameter count worked example (MiniTransformer to GPT-3 scale) | SMALL |
| T3-12 | Deep Explanation | 05 | 5.1 | Explain greedy repetition mechanism (positive feedback cycle) | SMALL |
| T3-13 | Deep Explanation | 05 | 5.2 | Explain repetition penalty asymmetry (pos/neg logit treatment) | SMALL |
| T3-14 | Curriculum Alignment | 04 | 4.2 | Resolve positional encoding mismatch: either add RoPE to lab or update syllabus | MEDIUM |
| T3-15 | Curriculum Alignment | 04 | 4.1 | Add activation function comparison table (ReLU vs. GELU vs. SwiGLU with ablation results) | SMALL |
| T3-16 | Curriculum Alignment | 05 | 5.3 | Add classifier-free guidance for language models subsection | MEDIUM |
| T3-17 | Curriculum Alignment | 04 | 4.3 | Expand encoder-decoder coverage (T5 text-to-text, BART denoising) | MEDIUM |
| T3-18 | Curriculum Alignment | 04 | 4.1 | Add loss function subsection (cross-entropy for next-token, label smoothing, auxiliary losses) | MEDIUM |
| T3-19 | Learning Quality | 01 | 1.3 | Add "Why Does This Work?" sidebar on Word2Vec analogy mechanism (Levy and Goldberg 2014, implicit PMI factorization) | SMALL |
| T3-20 | Learning Quality | 04 | 4.2 | Add Paper Spotlight for weight tying (Press and Wolf, 2017) | SMALL |
| T3-21 | Research/Frontier | 04 | 4.3 | Expand state space model coverage (S4, Mamba, Mamba-2, Jamba) | MEDIUM |
| T3-22 | Research/Frontier | 04 | 4.1 | Add KV cache explanation subsection | MEDIUM |
| T3-23 | Research/Frontier | 04 | 4.1 | Add GQA/MQA coverage (Ainslie et al., 2023; Shazeer, 2019) | MEDIUM |
| T3-24 | Research/Frontier | All | All | Add "Open Problems" box to each module | MEDIUM |
| T3-25 | Research/Frontier | 00 | 0.2 | Add SwiGLU and RMSNorm to activation/normalization coverage | SMALL |

### Structural and Visual Fixes

| # | Source Report(s) | Module | Section | What to Change | Effort |
|---|-----------------|--------|---------|---------------|--------|
| T3-26 | Structural, Teaching Flow | 03 | 3.1 | Consider splitting Section 3.1 into two: RNNs/gradients and gated RNNs/seq2seq | LARGE |
| T3-27 | Structural, Teaching Flow | 02 | 2.2 | Consider splitting Section 2.2 into two: core algorithms and byte-level/tokenizer-free | LARGE |
| T3-28 | Structural, Teaching Flow | 04 | 4.1 | Consider splitting Section 4.1 into two: components and assembly | LARGE |
| T3-29 | Structural | Part I | N/A | Add Part I Introduction page (roadmap, dependency diagram, study time) | MEDIUM |
| T3-30 | Structural, Teaching Flow | Part I | N/A | Add Part I closing summary page or section | MEDIUM |
| T3-31 | Code Pedagogy | All | All | Pin library versions in code comments (`gensim>=4.3`, `transformers>=4.36`, `tiktoken>=0.5`) | SMALL |
| T3-32 | Code Pedagogy | 01 | 1.4 | Show output for BERT contextual embedding demo (cosine similarity values) | SMALL |
| T3-33 | Code Pedagogy | 01 | 1.4 | Add scaffolding to Word2Vec from-scratch exercise (skeleton code, function signatures) | MEDIUM |
| T3-34 | Code Pedagogy | 04 | 4.5 | Add one code example demonstrating Transformer failure on counting task (with/without CoT) | MEDIUM |
| T3-35 | Visual/Exercise | 03 | 3.1 | Add causal mask visualization SVG (lower-triangular matrix) | SMALL |
| T3-36 | Visual/Exercise | 03 | 3.2 | Add attention weight heatmap for translation example | MEDIUM |
| T3-37 | Visual/Exercise | 00 | 0.1 | Add overfitting three-panel diagram (underfit, good, overfit) | MEDIUM |
| T3-38 | Clarity (Phase 6) | Multiple | Multiple | Break 6 dense single-paragraph callouts into intro + bullet lists | SMALL |
| T3-39 | Clarity | Multiple | Multiple | Add brief glosses when using jargon defined in later modules (bi-LSTM, feature map, naive softmax) | SMALL |
| T3-40 | Integrity | 04 | All | Align Module 04 navigation CSS to the pattern used by other modules | SMALL |
| T3-41 | Engagement | Multiple | Multiple | Rewrite 5-8 section titles from technical taxonomy to curiosity-driven hooks | SMALL |
| T3-42 | Visual Polish | 01 | All | Remove drop cap styling or add to all sections for consistency | SMALL |
| T3-43 | Visual Polish | 01 | All | Change inline code color from red to blue (match other modules) | SMALL |
| T3-44 | Visual Polish | All | All | Add responsive media query from Module 01 to unified CSS template | SMALL |
| T3-45 | Engagement | Multiple | Multiple | Reframe 4 existing labs as "Projects" with motivational framing | SMALL |
| T3-46 | Integrity | 04 | 4.3 | Add BERT MLM 80/10/10 masking scheme note | SMALL |

---

## Summary Counts

### By Tier

| Tier | Count |
|------|-------|
| TIER 1 (BLOCKING) | 5 |
| TIER 2 (HIGH) | 30 |
| TIER 3 (MEDIUM) | 46 |
| **Total** | **81** |

### By Effort

| Effort | TIER 1 | TIER 2 | TIER 3 | Total |
|--------|--------|--------|--------|-------|
| Small | 4 | 18 | 26 | 48 |
| Medium | 0 | 8 | 16 | 24 |
| Large | 1 | 4 | 4 | 9 |

### By Module

| Module | TIER 1 | TIER 2 | TIER 3 | Total |
|--------|--------|--------|--------|-------|
| 00: ML and PyTorch | 3 | 6 | 4 | 13 |
| 01: NLP and Text | 1 | 5 | 6 | 12 |
| 02: Tokenization | 0 | 2 | 5 | 7 |
| 03: Sequence/Attention | 0 | 5 | 5 | 10 |
| 04: Transformer | 1 | 6 | 17 | 24 |
| 05: Decoding | 0 | 4 | 3 | 7 |
| Cross-cutting/Part I | 0 | 2 | 6 | 8 |

---

## Conflict Resolutions

1. **Section 4.2 positional encoding (RoPE vs. learned):** The curriculum report says the syllabus promises RoPE, but the code uses learned embeddings. Resolution: keep learned embeddings for pedagogical simplicity in the lab; add a brief RoPE sidebar showing how to swap it in. Update the syllabus to say "learned positional embeddings (with RoPE sidebar)."

2. **Section 3.2 backprop-through-attention placement:** Teaching Flow recommends moving it after the seq2seq integration; Learning Quality recommends making it collapsible. Resolution: make it a collapsible "Advanced Deep Dive" in its current position. This preserves logical ordering while letting students skip it.

3. **Module 00 restructuring (split vs. keep):** Teaching Flow suggests splitting Section 0.1; Frontier report suggests condensing all of Module 00. Resolution: keep the current structure but add checkpoint moments within dense sections. Module 00 serves a necessary prerequisite function.

4. **Section 1.2 preprocessing depth:** Frontier report says classical preprocessing is obsolete; Curriculum Alignment says TF-IDF depth is promised. Resolution: add the promised TF-IDF depth but frame it with upfront honesty about modern relevance.

5. **Section titles (technical vs. catchy):** Engagement report recommends curiosity-driven rewrites for 14 titles. Resolution: add compelling subtitles rather than replacing technical titles, since the technical titles serve as reference labels in the syllabus navigation.
