# Part I: Visual Learning & Exercise Design Report

**Date:** 2026-03-26
**Scope:** Modules 00 through 05 (Part I: Foundations)
**Agents:** Visual Learning Designer + Exercise Designer

---

## Executive Summary

Part I contains 23 section HTML files across 6 modules with a total of **53 SVG diagrams** and approximately **115 quiz/exercise items**. Diagram quality is generally strong, with descriptive captions and clear labeling throughout. The biggest visual gaps are in Module 04 (sections 4.2, 4.3, 4.5 each have only 1 SVG) and Module 01 (section 1.1 has zero exercises; sections 1.2 and 1.3 have no formal quizzes). Exercise coverage is uneven: Modules 02 through 05 have consistent quiz sections in every file, while Module 00 has a gap in section 0.3 and Module 01 concentrates all exercises at the end of 1.4.

**Overall Visual Quality:** ADEQUATE (strong in places, thin in Module 04 mid-sections)
**Overall Exercise Quality:** ADEQUATE (good variety but uneven distribution)

---

## Part 1: Visual Learning Review

### Module 00: ML & PyTorch Foundations

#### Visual Inventory
| Section | SVG Count | Captioned | Caption Quality |
|---------|-----------|-----------|-----------------|
| 0.1 | 2 | 2/2 | GOOD (gradient descent, bias-variance) |
| 0.2 | 2 | 2/2 | GOOD (perceptron anatomy, backprop walkthrough) |
| 0.3 | 2 | 2/2 | GOOD (computational graph, training loop) |
| 0.4 | 2 | 2/2 | GOOD (agent-environment loop, RLHF pipeline) |
| **Total** | **8** | **8/8** | |

#### Assessment
- **Clarity and labeling:** All 8 SVGs have descriptive captions that explain what the diagram shows, not just what it is. Example: "Gradient descent follows the slope downhill, step by step. The learning rate controls step size." This matches best practices.
- **Style consistency:** Section 0.1 uses a gradient header with different CSS variables than 0.2 through 0.4. Section 0.2 uses `.diagram-caption` class while 0.1 embeds captions inside the diagram container. The SVG themselves share a consistent look (clean lines, labeled nodes), but the surrounding HTML styling diverges across sections.
- **Text references:** Diagrams are generally referenced in prose, though some references are implicit (the diagram appears after the prose without a "see Figure X" callout).
- **Complexity match:** Appropriate. Simple diagrams for simple concepts (gradient descent curve), detailed diagrams for complex ones (backprop walkthrough with numerical values).

#### Missing Visuals (Priority-Ordered)
1. **Section 0.1:** Overfitting vs. underfitting three-panel diagram (underfit line, good quadratic, overfit high-degree). The polynomial overfitting code example has no companion visual.
   - Type: SVG
   - Description: Three side-by-side panels showing polynomial fits of degree 1, 3, and 15 to the same noisy data
2. **Section 0.2:** MLP architecture diagram. The perceptron diagram exists but there is no multi-layer network visualization.
   - Type: SVG
   - Description: Input layer, 2 hidden layers, output layer with arrows showing data flow and labeled dimensions
3. **Section 0.3:** Broadcasting shape alignment diagram. Broadcasting is explained in text and code but never visualized.
   - Type: SVG
   - Description: Show how shapes (3,1) + (1,4) align to produce (3,4) with color-coded expansions
4. **Section 0.4:** REINFORCE update numerical walkthrough. The backprop section (0.2) has a step-by-step numerical diagram; the REINFORCE section has none.
   - Type: SVG or Python (matplotlib)
   - Description: Trace one episode of the grid world through the policy gradient update equation with concrete numbers

#### Python Figure Opportunities
1. **Section 0.1:** Loss landscape contour plot showing gradient descent trajectory
   - Plot type: contour with trajectory overlay
   - Insight: Visualize how learning rate affects convergence path
2. **Section 0.2:** Activation function comparison plot (ReLU, sigmoid, tanh, GELU, Leaky ReLU)
   - Plot type: multi-line plot
   - Insight: Show where each function saturates or has zero gradients
3. **Section 0.4:** Reward over episodes training curve from grid world
   - Plot type: line chart
   - Insight: Make learning visible; currently the code never shows output

---

### Module 01: NLP & Text Representation

#### Visual Inventory
| Section | SVG Count | Captioned | Caption Quality |
|---------|-----------|-----------|-----------------|
| 1.1 | 3 | 3/3 | GOOD (eras timeline, task types, language layers) |
| 1.2 | 4 | 3/4 | GOOD (pipeline, stemming vs. lemma, BoW matrix, TF-IDF) |
| 1.3 | 4 | 4/4 | GOOD (Skip-gram, embedding matrix, cosine, FastText) |
| 1.4 | 4 | 3/4 | GOOD (static vs. contextual, ELMo arch, journey summary) |
| **Total** | **15** | **13/15** | |

#### Assessment
- **Clarity and labeling:** The richest module visually. Section 1.3 has particularly effective diagrams for the Skip-gram architecture and cosine similarity geometry. All use consistent font families.
- **Style consistency:** Module 01 sections share the same CSS, making it the most visually cohesive module in Part I.
- **Text references:** Most diagrams are introduced before they appear. Two SVGs in sections 1.2 and 1.4 lack explicit prose references.
- **Complexity match:** Excellent. Conceptual sections (1.1) have simple timeline/overview SVGs. Technical sections (1.3) have detailed architectural SVGs.

#### Missing Visuals
1. **Section 1.2:** Comparison table/graphic for BoW vs. TF-IDF vs. one-hot encoding side by side
   - Type: SVG comparison graphic
   - Description: Three panels showing the same sentence encoded as BoW, TF-IDF, and one-hot, highlighting sparsity differences
2. **Section 1.3:** GloVe co-occurrence ratio visualization
   - Type: Python (matplotlib heatmap)
   - Description: Show how co-occurrence ratios for (ice, steam) vs. (ice, fashion) differ using a small matrix
3. **Section 1.4:** Model size comparison bar chart (Word2Vec, ELMo, BERT, GPT-3)
   - Type: Python (matplotlib bar chart, log scale)
   - Description: Contextualize the scale progression from static to contextual to LLMs

#### Python Figure Opportunities
1. **Section 1.3:** t-SNE embedding space visualization is described in code but not shown as a figure in the HTML
   - Plot type: scatter plot with word labels
   - Insight: Category clusters emerge from Word2Vec training
2. **Section 1.3:** Cosine similarity heatmap code exists but no pre-rendered figure appears
   - Plot type: heatmap
   - Insight: Within-category words cluster more tightly

---

### Module 02: Tokenization & Subword Models

#### Visual Inventory
| Section | SVG Count | Captioned | Caption Quality |
|---------|-----------|-----------|-----------------|
| 2.1 | 3 | 3/3 | GOOD (vocab spectrum, context window, artifact pipeline) |
| 2.2 | 3 | 3/3 | GOOD (BPE merge steps, Unigram lattice, byte-level BPE) |
| 2.3 | 3 | 3/3 | GOOD (chat template, image patches, tokenizer landscape) |
| **Total** | **9** | **9/9** | |

#### Assessment
- **Clarity and labeling:** All 9 SVGs are fully captioned with descriptive text. The BPE merge step-by-step diagram is especially effective for illustrating the algorithm.
- **Style consistency:** Consistent CSS across all three sections. Uses a Georgia serif font family in SVG text for visual cohesion with the body text.
- **Text references:** Each diagram is explicitly referenced in the preceding paragraph.
- **Complexity match:** Well calibrated. The Unigram lattice diagram is appropriately complex for an intermediate concept.

#### Missing Visuals
1. **Section 2.1:** Multilingual fertility comparison bar chart (same text, different languages, token counts)
   - Type: Python (matplotlib grouped bar chart)
   - Description: Show token count for "Hello, how are you?" in English, Chinese, Arabic, Korean to visualize the token tax
2. **Section 2.2:** Side-by-side BPE vs. WordPiece vs. Unigram tokenization of the same sentence
   - Type: SVG comparison
   - Description: Three rows showing how each algorithm segments the same input differently

#### Python Figure Opportunities
1. **Section 2.1:** Token count by language bar chart (using tiktoken)
   - Insight: Quantify the multilingual fairness gap
2. **Section 2.2:** Vocabulary growth curve during BPE training (merge count vs. vocab size)
   - Insight: Visualize the compression/coverage tradeoff

---

### Module 03: Sequence Models & Attention

#### Visual Inventory
| Section | SVG Count | Captioned | Caption Quality |
|---------|-----------|-----------|-----------------|
| 3.1 | 3 | 3/3 | GOOD (RNN unrolled, vanishing gradient, seq2seq bottleneck) |
| 3.2 | 2 | 2/2 | GOOD (Bahdanau attention, gradient flow) |
| 3.3 | 2 | 2/2 | GOOD (scaled dot-product, multi-head attention) |
| **Total** | **7** | **7/7** | |

#### Assessment
- **Clarity and labeling:** All SVGs are captioned with detailed, explanatory descriptions. The Bahdanau attention caption is particularly strong.
- **Style consistency:** Sections 3.2 and 3.3 share the same CSS. Section 3.1 has slightly different CSS variable names but the visual result is similar.
- **Text references:** Every diagram is referenced in the text before it appears.
- **Complexity match:** Good. The LSTM cell diagram is notably absent from the section despite being mentioned in the chapter plan. The vanishing gradient diagram effectively uses a bar chart to show exponential decay.

#### Missing Visuals
1. **Section 3.1:** LSTM cell architecture diagram with gates labeled. The chapter plan lists it as present but only 3 SVGs exist; the LSTM diagram appears to be missing or may be combined with another diagram.
   - Type: SVG
   - Description: LSTM cell with forget gate, input gate, output gate, and cell state clearly labeled
2. **Section 3.2:** Attention weight heatmap for a translation example
   - Type: SVG or Python (seaborn heatmap)
   - Description: Source language (rows) vs. target language (columns) with attention weights as colors
3. **Section 3.3:** Causal mask visualization as a lower-triangular matrix
   - Type: SVG
   - Description: Show the triangular mask pattern and explain which positions can attend to which

#### Python Figure Opportunities
1. **Section 3.1:** Gradient magnitude decay plot across time steps
   - Plot type: line chart (semi-log)
   - Insight: Quantify how quickly gradients vanish in vanilla RNNs vs. LSTMs
2. **Section 3.3:** Attention weight distribution visualization (sharp vs. diffuse at different temperatures)
   - Plot type: bar chart with multiple temperature settings
   - Insight: Show how scaling affects the attention distribution

---

### Module 04: Transformer Architecture

#### Visual Inventory
| Section | SVG Count | Captioned | Caption Quality |
|---------|-----------|-----------|-----------------|
| 4.1 | 3 | 3/3 | GOOD (full architecture, positional encoding, attention flow) |
| 4.2 | 1 | 1/1 | GOOD (model schematic with shapes) |
| 4.3 | 1 | 1/1 | ADEQUATE (three families comparison) |
| 4.4 | 2 | 2/2 | GOOD (GPU memory hierarchy, FlashAttention tiling) |
| 4.5 | 1 | 1/1 | ADEQUATE (CoT extending computation) |
| **Total** | **8** | **8/8** | |

#### Assessment
- **Clarity and labeling:** The SVGs that exist are well labeled. However, 8 SVGs across 5 sections for the course's most important module is thin. Several sections have only 1 SVG for concepts that would benefit from 2 to 3.
- **Style consistency:** Sections 4.1 and 4.3 through 4.5 use the same gradient-header CSS. Section 4.2 uses a different styling (closer to Module 01's style).
- **Text references:** All diagrams are referenced in text.
- **Complexity match:** The mismatch is notable. This is the deepest, most complex module, yet it has fewer diagrams per section than the simpler Modules 01 and 02. The chapter plan calls for 20+ diagrams across all sections; only 8 are present.

#### Missing Visuals (Priority-Ordered, High Impact)
1. **Section 4.1:** Pre-LN vs. Post-LN comparison diagram
   - Type: SVG
   - Description: Side-by-side showing where LayerNorm goes in each variant and the impact on gradient flow
2. **Section 4.1:** Residual stream information flow diagram
   - Type: SVG
   - Description: Show how information bypasses attention/FFN blocks through residual connections
3. **Section 4.1:** Sinusoidal positional encoding heatmap
   - Type: Python (matplotlib imshow)
   - Description: Heatmap with position on y-axis, dimension on x-axis, showing the sinusoidal wave patterns
4. **Section 4.2:** Training loss curve from the character-level model
   - Type: Python (matplotlib line plot)
   - Description: Show the model actually learning; currently the lab code produces no visible training output
5. **Section 4.3:** RoPE rotation visualization
   - Type: SVG
   - Description: Show how 2D rotation matrices encode relative positions
6. **Section 4.3:** Sparse attention pattern diagrams (local window, strided, BigBird)
   - Type: SVG grid
   - Description: Show which positions attend to which in each pattern as a mask matrix
7. **Section 4.3:** MoE routing diagram
   - Type: SVG
   - Description: Show token routing to experts with top-k gating
8. **Section 4.3:** MLA compression flow
   - Type: SVG
   - Description: Show how low-rank projections compress K and V
9. **Section 4.4:** Roofline model plot with Transformer operations placed on it
   - Type: Python (matplotlib)
   - Description: Show where matmuls, attention, and LayerNorm fall on the compute/bandwidth spectrum
10. **Section 4.5:** TC0 circuit depth illustration
    - Type: SVG
    - Description: Show a constant-depth circuit and what it can/cannot compute

#### Python Figure Opportunities
1. **Section 4.1:** Positional encoding heatmap (mandatory for understanding frequency patterns)
2. **Section 4.2:** Training loss curve (mandatory for the lab to feel complete)
3. **Section 4.4:** Roofline model plot (mandatory for the GPU section to be effective)
4. **Section 4.3:** Parameter count comparison bar chart across model families

---

### Module 05: Decoding & Text Generation

#### Visual Inventory
| Section | SVG Count | Captioned | Caption Quality |
|---------|-----------|-----------|-----------------|
| 5.1 | 2 | 2/2 | GOOD (greedy tree, beam search tree) |
| 5.2 | 2 | 2/2 | GOOD (temperature effect, top-p cutoff) |
| 5.3 | 2 | 2/2 | GOOD (contrastive decoding, speculative pipeline) |
| 5.4 | 2 | 2/2 | GOOD (diffusion process, AR vs. diffusion comparison) |
| **Total** | **8** | **8/8** | |

#### Assessment
- **Clarity and labeling:** All 8 SVGs have descriptive captions. The beam search tree diagram effectively shows how multiple hypotheses are tracked. The temperature effect diagram is particularly clear.
- **Style consistency:** All 4 sections share the same CSS. This is the second most visually cohesive module (after Module 01).
- **Text references:** All diagrams are referenced before they appear.
- **Complexity match:** Good. Each section has exactly 2 SVGs, which is appropriate for the concept density.

#### Missing Visuals
1. **Section 5.3:** Grammar-constrained decoding state machine diagram
   - Type: SVG
   - Description: Show a finite-state machine for JSON schema enforcement with token masking at each state
2. **Section 5.2:** Min-p vs. top-k vs. top-p comparison on the same distribution
   - Type: Python (matplotlib) or SVG
   - Description: Three panels showing which tokens survive under each filtering method

#### Python Figure Opportunities
1. **Section 5.2:** Interactive probability distribution reshaping
   - Plot type: bar charts at different temperature/top-k/top-p settings
   - Insight: Show how each parameter changes the shape of the token distribution
2. **Section 5.4:** Parallel generation timeline
   - Plot type: Gantt-style horizontal bar chart
   - Insight: Show speed advantage of diffusion (multiple tokens per step vs. one)

---

## Part 2: Exercise Design Review

### Module 00: ML & PyTorch Foundations

#### Exercise Inventory
| Section | Quiz Qs | Coding Ex | Lab | Type |
|---------|---------|-----------|-----|------|
| 0.1 | 5 | 0 | No | Conceptual (details/summary reveal) |
| 0.2 | 5 | 0 | No | Conceptual (details/summary reveal) |
| 0.3 | 0 | 4 | Yes (FashionMNIST) | Coding (lab at end) |
| 0.4 | 3 | 0 | No | Conceptual (JavaScript onclick reveal) |
| **Total** | **13** | **4** | **1** | |

#### Assessment
- **Distribution:** Uneven. Sections 0.1 and 0.2 have quiz-only exercises. Section 0.3 has coding-only exercises (no conceptual quiz). Section 0.4 has quizzes but no coding practice.
- **Variety:** Limited. Quizzes are all short-answer/explanation format. No multiple choice, no true/false, no fill-in-the-blank, no matching exercises.
- **Bloom's Taxonomy:**
  - Remember: ~20% (definition-style questions)
  - Understand: ~40% (explain-why questions)
  - Apply: ~30% (lab exercises in 0.3)
  - Analyze: ~10% (bias-variance LLM question in 0.1)
  - Evaluate/Create: 0%
- **Solutions:** Quiz questions have detailed reveal-able answers. Lab exercises in 0.3 have expected output but no full solution code.
- **Progressive chains:** The 0.3 lab has a good progression (overfit single batch, add scheduler, switch to CNN, add gradient clipping). Other sections lack progressive difficulty.
- **Quiz format inconsistency:** Sections 0.1 and 0.2 use `<details>/<summary>`. Section 0.4 uses JavaScript `checkAnswer()`. This should be standardized.

#### Gaps
1. **Section 0.3 has NO conceptual quiz.** Students complete the lab but are not tested on understanding autograd, broadcasting, or GPU management.
2. **Section 0.4 has NO coding exercises.** The RL section is purely conceptual despite having runnable code examples. Students should modify the grid world or experiment with gamma.
3. **No evaluation/create-level exercises** anywhere in the module. Consider adding a mini-design exercise: "Design a training pipeline for X" or "What experiments would you run to diagnose Y?"

---

### Module 01: NLP & Text Representation

#### Exercise Inventory
| Section | Quiz Qs | Coding Ex | Lab | Type |
|---------|---------|-----------|-----|------|
| 1.1 | 0 | 0 | No | None |
| 1.2 | 0 | 0 | No | 1 inline "Try It" prompt (no structure) |
| 1.3 | 0 | 0 | No | None (exercises deferred to 1.4) |
| 1.4 | 5 | 4 | No | Conceptual + Coding (at end of module) |
| **Total** | **5** | **4** | **0** | |

#### Assessment
- **Distribution:** POOR. All 9 exercises are in the final section. Sections 1.1, 1.2, and 1.3 have zero formal exercises. Students read 3 full sections with no practice checkpoints.
- **Variety:** Good within the 1.4 exercise set. Conceptual questions test understanding (not memorization). Coding exercises range from exploration to a challenge-level implementation.
- **Bloom's Taxonomy:**
  - Remember: 0% (no recall questions)
  - Understand: ~35% (conceptual questions 1, 3, 4)
  - Apply: ~35% (coding exercises 1, 2, 3)
  - Analyze: ~15% (question 5 on TF-IDF tradeoffs, question 2 on distributional hypothesis limits)
  - Create: ~15% (exercise 4: Word2Vec from scratch)
- **Solutions:** Conceptual questions have NO revealed answers. Students must self-assess, which reduces the value for solo learners.
- **Progressive chains:** The coding exercises form a reasonable progression from exploration (exercise 1) to full implementation (exercise 4). However, exercise 4 (Word2Vec from scratch) is extremely ambitious with no scaffolding.

#### Gaps
1. **Sections 1.1, 1.2, and 1.3 need exercises.** At minimum, a 3-question "Check Your Understanding" quiz per section.
2. **No answer keys** for the conceptual questions. Add `<details>/<summary>` reveal blocks.
3. **Exercise 4 needs scaffolding.** Provide a skeleton code structure, suggested function signatures, or a step-by-step breakdown.

---

### Module 02: Tokenization & Subword Models

#### Exercise Inventory
| Section | Quiz Qs | Coding Ex | Lab | Type |
|---------|---------|-----------|-----|------|
| 2.1 | 5 | 0 | No | Conceptual (details/summary) |
| 2.2 | 5 | 0 | Yes (BPE from scratch) | Conceptual + Lab |
| 2.3 | 5 | 0 | Yes (tokenizer comparison) | Conceptual + Lab |
| **Total** | **15** | **0** | **2** | |

#### Assessment
- **Distribution:** GOOD. Every section has 5 quiz questions. Labs are in sections 2.2 and 2.3 alongside the quizzes.
- **Variety:** Quiz questions mix comprehension, reasoning, and applied scenarios. Lab exercises involve hands-on coding.
- **Bloom's Taxonomy:**
  - Remember: ~20% (definition recall)
  - Understand: ~35% (explain-why, compare-contrast)
  - Apply: ~30% (trace BPE by hand, cost estimation)
  - Analyze: ~15% (tradeoff analysis, edge case identification)
  - Create: 0%
- **Solutions:** All quiz questions have detailed `<details>/<summary>` reveal answers. Consistent format.
- **Progressive chains:** Within each section, questions escalate from simple recall to applied analysis. The final question in each section is the most challenging.
- **Quiz quality:** Distractors are not applicable (open-ended format). Questions test genuine understanding, not trivia.

#### Gaps
1. **No coding exercises separate from labs.** Consider adding 1 to 2 short coding tasks per section (tokenize this text, compute fertility for this input).
2. **No create-level exercise.** Consider: "Design a tokenizer training strategy for a new language with limited data."

---

### Module 03: Sequence Models & Attention

#### Exercise Inventory
| Section | Quiz Qs | Coding Ex | Lab | Type |
|---------|---------|-----------|-----|------|
| 3.1 | 5 | 0 | No | Conceptual (details/summary) |
| 3.2 | 5 | 0 | No | Conceptual (details/summary) |
| 3.3 | 5 | 0 | Yes (MultiHeadSelfAttention) | Conceptual + Lab |
| **Total** | **15** | **0** | **1** | |

#### Assessment
- **Distribution:** GOOD. Every section has 5 quiz questions. The lab is in the final section.
- **Variety:** Questions are well-calibrated. They require explanation, not recitation. The lab (implementing multi-head self-attention) is excellent.
- **Bloom's Taxonomy:**
  - Remember: ~15%
  - Understand: ~40%
  - Apply: ~25% (lab implementation)
  - Analyze: ~20% (gradient flow, complexity analysis, design tradeoff questions)
  - Create: 0%
- **Solutions:** All quiz answers are revealed via `<details>/<summary>`.
- **Progressive chains:** Each section's questions progress from basic recall to deeper analysis. The Q3.3 quiz builds well on the lab.

#### Gaps
1. **No coding exercises outside the lab.** Students implement multi-head attention but do not get smaller coding tasks for RNNs or Bahdanau attention.
2. **No "debug this code" exercise.** Given the complexity of attention implementations, a debugging exercise would test understanding effectively.
3. **Missing create-level exercise.** Consider: "Propose a modification to the attention mechanism that would reduce memory usage. What tradeoffs would your design introduce?"

---

### Module 04: Transformer Architecture

#### Exercise Inventory
| Section | Quiz Qs | Coding Ex | Lab | Type |
|---------|---------|-----------|-----|------|
| 4.1 | 6 | 0 | No | Conceptual (details/summary) |
| 4.2 | 5 | 4 (experiments) | Yes (build from scratch) | Conceptual + Lab |
| 4.3 | 5 | 0 | No | Conceptual |
| 4.4 | 5 | 0 | Yes (Triton) | Conceptual + Lab |
| 4.5 | 5 | 0 | No | Conceptual |
| **Total** | **26** | **4** | **2** | |

#### Assessment
- **Distribution:** STRONG. Every section has 5 to 6 quiz questions. Two sections have hands-on labs.
- **Variety:** Best variety in Part I. Questions range from calculation (parameter count in 4.1), to reasoning (what if you removed the mask in 4.2), to applied analysis (arithmetic intensity in 4.4). The 4.2 experiments (vary depth, width, context length) add exploration-level work.
- **Bloom's Taxonomy:**
  - Remember: ~10%
  - Understand: ~30%
  - Apply: ~30% (labs, parameter calculation, experiments)
  - Analyze: ~20% (tradeoff questions in 4.3, complexity in 4.4)
  - Evaluate: ~10% (question 5.1 on why decoder-only won, CoT utility in 4.5)
  - Create: 0%
- **Solutions:** All quiz answers have `<details>/<summary>` reveals with detailed explanations.
- **Progressive chains:** The 4.2 experiments form a natural difficulty progression. Quiz questions within each section escalate.

#### Gaps
1. **Section 4.3 has no coding exercises.** Given the survey nature, even short pseudocode exercises (implement GQA given MHA code) would reinforce understanding.
2. **No create-level exercise.** This is the ideal module for one: "Design a hybrid architecture combining attention and SSMs. Where would you use each, and why?"
3. **Section 4.5 exercises are purely conceptual.** For a theory section this is acceptable, but consider adding one that connects theory to practice (e.g., predict whether CoT helps for a given task type).

---

### Module 05: Decoding & Text Generation

#### Exercise Inventory
| Section | Quiz Qs | Coding Ex | Lab | Type |
|---------|---------|-----------|-----|------|
| 5.1 | 4 | 0 | Yes (greedy vs. beam) | Conceptual + Lab |
| 5.2 | 3 | 0 | Yes (distribution viz) | Conceptual + Lab |
| 5.3 | 3 | 0 | No | Conceptual |
| 5.4 | 3 | 0 | No | Conceptual |
| **Total** | **13** | **0** | **2** | |

#### Assessment
- **Distribution:** GOOD. Every section has quiz questions. Labs are in the two core implementation sections.
- **Variety:** Quiz questions test reasoning (beam search failure modes, why length normalization helps, speculative decoding guarantees). Labs provide hands-on practice.
- **Bloom's Taxonomy:**
  - Remember: ~10%
  - Understand: ~40%
  - Apply: ~30% (labs)
  - Analyze: ~20% (comparing approaches, predicting behavior under parameter changes)
  - Create: 0%
- **Solutions:** All quiz answers are revealed.
- **Progressive chains:** Within sections, questions progress well. Across the module, the progression from deterministic (5.1) to stochastic (5.2) to advanced (5.3, 5.4) mirrors increasing difficulty.

#### Gaps
1. **No coding exercises in 5.3 or 5.4.** Even a simplified contrastive decoding implementation or a "trace the speculative decoding acceptance/rejection steps" exercise would be valuable.
2. **Section 5.4 exercises are lightweight.** The research-oriented nature justifies fewer exercises, but one analysis exercise ("Given these outputs, which was likely generated by a diffusion model vs. an autoregressive model? Why?") would strengthen assessment.

---

## Consolidated Findings

### Visual Summary by Module

| Module | SVG Total | Avg/Section | Captions | Style Consistent | Chapter Plan Target Met |
|--------|-----------|-------------|----------|-----------------|------------------------|
| 00 | 8 | 2.0 | 8/8 | No (4 different CSS) | Partially (missing 3) |
| 01 | 15 | 3.75 | 13/15 | Yes | Mostly (missing 2) |
| 02 | 9 | 3.0 | 9/9 | Yes | Mostly (missing 2) |
| 03 | 7 | 2.3 | 7/7 | Mostly | Partially (missing 3) |
| 04 | 8 | 1.6 | 8/8 | Mostly | No (8/20+ planned) |
| 05 | 8 | 2.0 | 8/8 | Yes | Mostly (missing 2) |

### Exercise Summary by Module

| Module | Total Items | Per Section | Has Solutions | Coding Exercises | Labs | Bloom's Coverage |
|--------|-------------|-------------|---------------|-----------------|------|-----------------|
| 00 | 17 | 4.25 | Partial | 4 | 1 | L1-L3 |
| 01 | 9 | 2.25 | No (conceptual) | 4 | 0 | L2-L5 |
| 02 | 15 | 5.0 | Yes | 0 | 2 | L1-L4 |
| 03 | 15 | 5.0 | Yes | 0 | 1 | L1-L4 |
| 04 | 26 | 5.2 | Yes | 4 | 2 | L1-L5 |
| 05 | 13 | 3.25 | Yes | 0 | 2 | L1-L4 |

### Top 10 Priority Actions (Visual)

1. **[Module 04]** Add 10+ missing diagrams. This module has the largest gap between planned and actual visuals. Priority: Pre-LN vs. Post-LN, RoPE, sparse attention patterns, MoE routing, positional encoding heatmap.
2. **[Module 03]** Add LSTM cell diagram and causal mask visualization. Core architecture diagrams that students need.
3. **[Module 00]** Add overfitting three-panel diagram and MLP architecture SVG. Reinforces the two most important concepts.
4. **[Module 04]** Add training loss curve to the 4.2 lab. The lab is incomplete without visible learning.
5. **[Module 04]** Add roofline model plot to 4.4. Essential for understanding the GPU section.
6. **[Module 00]** Standardize CSS across all 4 sections. Visual inconsistency is jarring when reading sequentially.
7. **[Module 01]** Add comparison graphic for BoW vs. TF-IDF vs. one-hot in section 1.2.
8. **[Module 05]** Add grammar-constrained decoding state machine to section 5.3.
9. **[Module 02]** Add multilingual fertility bar chart (Python-generated).
10. **[Module 03]** Add attention weight heatmap for translation example.

### Top 10 Priority Actions (Exercises)

1. **[Module 01]** Add "Check Your Understanding" quizzes to sections 1.1, 1.2, and 1.3 (3 to 5 questions each with answer reveals).
2. **[Module 01]** Add answer keys (`<details>/<summary>`) to the conceptual questions in section 1.4.
3. **[Module 00]** Add a conceptual quiz to section 0.3 (PyTorch tutorial). Currently has only lab exercises.
4. **[Module 00]** Add 2 to 3 coding exercises to section 0.4 (RL foundations). Currently has only conceptual quizzes.
5. **[Module 00]** Standardize quiz interaction pattern. Use `<details>/<summary>` everywhere (currently JavaScript onclick in 0.4).
6. **[Module 01]** Add scaffolding to the "Word2Vec from scratch" challenge exercise (skeleton code, function signatures).
7. **[All Modules]** Add at least one create-level (Bloom's L6) exercise per module: design a system, propose an architecture, or build something novel.
8. **[Module 03]** Add a "debug this attention code" exercise to section 3.3.
9. **[Module 04]** Add coding exercises to section 4.3 (e.g., implement GQA given MHA code).
10. **[Module 05]** Add coding exercises to sections 5.3 and 5.4.

### Cross-Cutting Style Issues

1. **CSS inconsistency in Module 00:** Four different stylesheets with different variable names, callout classes, heading styles, and navigation patterns.
2. **Quiz format inconsistency in Module 00:** `<details>/<summary>` in 0.1/0.2 vs. JavaScript onclick in 0.4.
3. **Code syntax highlighting inconsistency in Module 00:** Span classes in 0.2/0.3, inline styles in 0.1, plain text in 0.4.
4. **Caption element inconsistency:** Some modules use `<div class="diagram-caption">`, others use `<figcaption>` inside `<figure>`. Recommend standardizing on `<figure>/<figcaption>` for semantic HTML.
5. **No Python-generated figures exist yet.** All visuals are hand-coded SVGs. Several concepts (loss landscapes, training curves, embedding spaces, roofline plots) would be better served by data-driven Python figures.
