# Phase 4: Self-Containment Verification Report

**Reviewer:** Self-Containment Verifier Agent
**Date:** 2026-03-26
**Scope:** All 6 modules in Part I (Modules 00 through 05), all 23 section HTML files, all 6 chapter plans, and all 6 prior phase reports.

---

## Executive Summary

Part I is largely self-contained for its stated audience (Python-proficient engineers with basic linear algebra and probability). The dependency chain across modules is sound, and no module uses a concept that is formally introduced only in a later module. However, several concepts are used without ever being formally explained anywhere in Part I, and several cross-references that would help readers connect material across modules are missing. The most significant self-containment failures are: (1) the Adam optimizer is used in code across four modules but never explained; (2) information theory concepts (entropy, perplexity, KL divergence) are referenced in Modules 04 and 05 but never formally introduced; (3) the Jacobian matrix appears in Module 03 without a primer; and (4) the concepts of "self-supervised learning" and "unsupervised learning" are never defined despite being foundational to understanding LLM pretraining.

**Overall Self-Containment Rating: ADEQUATE** (no blocking gaps for the core narrative, but several important background concepts are assumed rather than provided)

---

## Chapter Prerequisite Map

This map shows what each module needs and where that knowledge is provided.

```
Module 00: ML and PyTorch Foundations
  Needs: Python, basic linear algebra, basic probability (EXTERNAL)
  Provides: gradient descent, loss functions, backpropagation, SGD,
            regularization, PyTorch basics, RL/RLHF overview

Module 01: NLP and Text Representation
  Needs: neural networks (M00), PyTorch (M00), NumPy (M00, implicit)
  Provides: NLP task taxonomy, preprocessing, BoW, TF-IDF, Word2Vec,
            GloVe, FastText, cosine similarity, ELMo, pre-train/fine-tune paradigm

Module 02: Tokenization and Subword Models
  Needs: vocabulary concepts (M01), Python data structures (M00)
  Provides: BPE, WordPiece, Unigram, byte-level BPE, special tokens,
            chat templates, fertility analysis

Module 03: Sequence Models and Attention
  Needs: backpropagation (M00), embeddings (M01), token IDs (M02)
  Provides: RNNs, LSTM, GRU, seq2seq, Bahdanau attention, Luong attention,
            Q/K/V framework, multi-head self-attention, causal masking

Module 04: Transformer Architecture
  Needs: multi-head attention (M03), embeddings (M01), tokenization (M02),
         PyTorch nn.Module (M00)
  Provides: full Transformer, positional encoding, FFN, residual connections,
            LayerNorm, from-scratch implementation, variants survey, GPU fundamentals

Module 05: Decoding and Text Generation
  Needs: Transformer forward pass (M04), softmax and logits (M00/M04),
         autoregressive masking (M03/M04)
  Provides: greedy decoding, beam search, temperature, top-k, top-p, min-p,
            repetition penalties, contrastive/speculative decoding, watermarking,
            diffusion LMs
```

---

## Module-by-Module Self-Containment Audit

### Module 00: ML and PyTorch Foundations

**Missing Background Concepts:**

| Concept | Where Used | Where Explained | Status | Severity |
|---------|-----------|-----------------|--------|----------|
| Adam optimizer | Sections 0.1, 0.2, 0.3, 0.4 (code) | Section 0.3 has one bullet: "Adapts the learning rate per parameter" | INSUFFICIENT | **BLOCKING** |
| Self-supervised learning | Nowhere | Nowhere | ABSENT | IMPORTANT |
| Unsupervised learning | Nowhere | Nowhere | ABSENT | IMPORTANT |
| Probability distribution (formal) | Section 0.4 (policy as distribution) | Assumed as prerequisite | OK for audience | OPTIONAL |
| Bayes' theorem | Listed as prerequisite | Never used in Part I | N/A | OPTIONAL |

**Findings:**

1. **BLOCKING: Adam optimizer is used but not explained.** The code `optim.Adam(...)` appears in Sections 0.2, 0.3, and 0.4, and later in Section 4.2 as `AdamW`. Section 0.3 gives a single bullet point ("adapts the learning rate per parameter"), but this is not a real explanation. Students do not learn what distinguishes Adam from SGD (momentum, adaptive per-parameter rates), why it is the default for LLM training, or what AdamW adds (decoupled weight decay). This is the single most referenced unexplained concept in Part I.

2. **IMPORTANT: Self-supervised learning is never defined.** LLM pretraining is self-supervised (the model predicts tokens it has seen, with no human labels), yet this learning paradigm is never named or defined. Section 0.1 covers supervised learning only. When the "pre-train, then fine-tune" paradigm is introduced in Section 1.4, students have no formal category for how pretraining works. The chapter plan for Module 00 identifies this gap.

3. **IMPORTANT: The cross-reference error in Section 0.4 remains.** The "What Comes Next" paragraph refers to "transformers (Module 02)" when it should say Module 04. This is a factual navigation error that has been flagged in multiple prior reports but not yet fixed.

**Recommendation:**
- Add a 2-paragraph callout box in Section 0.2 or 0.3 explaining Adam (momentum + adaptive rates) and AdamW (decoupled weight decay). Priority: BLOCKING.
- Add a 1-paragraph callout in Section 0.1 naming and briefly defining supervised, unsupervised, and self-supervised learning. Priority: IMPORTANT.
- Fix the Section 0.4 cross-reference. Priority: IMPORTANT.

---

### Module 01: Foundations of NLP and Text Representation

**Missing Background Concepts:**

| Concept | Where Used | Where Explained | Status | Severity |
|---------|-----------|-----------------|--------|----------|
| NumPy basics | Sections 1.2, 1.3 (code) | Assumed from M00; M00 uses NumPy but does not teach it | GAP | OPTIONAL |
| Softmax function | Section 1.3 (negative sampling), 1.4 (BERT) | Explained in Section 0.2 | OK | N/A |
| Negative sampling cost | Section 1.3 | Not quantified | SHALLOW | IMPORTANT |
| Co-occurrence matrix factorization | Section 1.3 (GloVe) | Named but not demonstrated | SHALLOW | IMPORTANT |
| LSTM architecture | Section 1.4 (ELMo) | Introduced conceptually; formalized in M03 | FORWARD REF | OPTIONAL |

**Findings:**

1. **IMPORTANT: No backward reference to Module 00.** Section 1.1 does not mention Module 00. Students arriving from Module 00 get no orientation sentence connecting their prior learning to NLP. The four-eras framework starts fresh with no bridge.

2. **IMPORTANT: Negative sampling is assumed to "just work."** Section 1.3 presents the negative sampling formula but does not quantify why the naive softmax is intractable (100K+ vocabulary, billions of training pairs) or why sampling 5 to 20 negatives per positive is a valid approximation. This leaves a conceptual gap: students know the formula but not why it exists.

3. **IMPORTANT: GloVe's co-occurrence ratio insight is named but not demonstrated.** The text mentions that GloVe uses co-occurrence ratios to capture meaning, but no worked numeric example shows how the ratio P(solid|ice)/P(solid|steam) encodes the ice/steam relationship. Students are told the insight without seeing it.

4. **OPTIONAL: ELMo uses LSTMs, which are not formally introduced until Module 03.** Section 1.4 says ELMo uses "bidirectional LSTMs" and provides a brief explanation, but the full LSTM architecture (gates, cell state) is covered in Module 03. This is an acceptable forward reference since the section does not require deep LSTM understanding; it uses BERT code instead of ELMo code.

**Recommendation:**
- Add a one-sentence bridge at the top of Section 1.1 referencing Module 00. Priority: IMPORTANT.
- Add a quantified explanation of negative sampling's cost benefit in Section 1.3. Priority: IMPORTANT.
- Add a small co-occurrence ratio worked example to the GloVe subsection. Priority: IMPORTANT.

---

### Module 02: Tokenization and Subword Models

**Missing Background Concepts:**

| Concept | Where Used | Where Explained | Status | Severity |
|---------|-----------|-----------------|--------|----------|
| Dynamic programming | Section 2.2 (Viterbi) | Named but not explained | GAP | IMPORTANT |
| Mutual information | Section 2.2 (WordPiece) | Named in passing | GAP | IMPORTANT |
| Log-likelihood | Section 2.2 (Unigram) | Assumed from probability prerequisites | THIN | OPTIONAL |
| Unicode / UTF-8 | Section 2.2 (byte-level BPE) | Briefly mentioned | THIN | OPTIONAL |

**Findings:**

1. **IMPORTANT: Viterbi decoding assumes familiarity with dynamic programming.** Section 2.2 states that Unigram uses "the Viterbi algorithm (dynamic programming over all possible tokenizations)" but does not explain what dynamic programming is or how Viterbi works. The SVG diagram shows a lattice with probabilities, but the algorithm for finding the optimal path is not walked through step by step. For students without algorithms background, this is a gap.

2. **IMPORTANT: WordPiece's "likelihood-based" criterion is underspecified.** The section says WordPiece uses a "likelihood-based merge criterion" related to mutual information, but does not explain what mutual information is, why it differs from BPE's frequency criterion, or when it produces different results. This leaves the core differentiator between BPE and WordPiece unclear.

3. **OPTIONAL: No backward reference from Module 02 to Module 01.** Section 2.1 does not mention Module 01's preprocessing discussion or vocabulary concepts. The transition from "classical preprocessing" (Module 01) to "modern tokenization" (Module 02) is left implicit.

4. **OPTIONAL: No forward reference from Module 02 to Module 03.** Module 02's final section ends without previewing how token sequences become inputs to sequence models.

**Recommendation:**
- Add a 1-paragraph primer on dynamic programming before the Viterbi explanation, or add a small step-by-step worked example showing how Viterbi finds the optimal segmentation path. Priority: IMPORTANT.
- Add a brief explanation of why likelihood-based merging (WordPiece) and frequency-based merging (BPE) produce different results. Priority: IMPORTANT.
- Add cross-module bridges at both ends: backward to Module 01, forward to Module 03. Priority: OPTIONAL.

---

### Module 03: Sequence Models and the Attention Mechanism

**Missing Background Concepts:**

| Concept | Where Used | Where Explained | Status | Severity |
|---------|-----------|-----------------|--------|----------|
| Jacobian matrix | Section 3.1 (vanishing gradients), 3.2 (backprop through attention) | Not defined; assumed from linear algebra | GAP | IMPORTANT |
| Singular values | Section 3.1 (gradient analysis) | Not defined | GAP | OPTIONAL |
| Hadamard (element-wise) product | Section 3.1 (LSTM gates) | Used in code without naming | THIN | OPTIONAL |
| Matrix calculus notation | Section 3.2 (Jacobian of softmax) | Used without primer | GAP | IMPORTANT |
| Token sequences from Module 02 | Section 3.1 (input to RNNs) | No explicit bridge from M02 | MISSING BRIDGE | OPTIONAL |

**Findings:**

1. **IMPORTANT: The Jacobian matrix is used without definition.** Section 3.1 states: "This is a product of (T - t) Jacobian matrices. Each factor contains the derivative of h_t with respect to h_{t-1}." Section 3.2 has a subsection titled "The Jacobian of Softmax." Neither section defines what a Jacobian is. The stated math prerequisite is "basic linear algebra (vectors, dot products, matrix multiplication)," which does not cover the Jacobian. Students without calculus beyond the chain rule will be lost here.

2. **IMPORTANT: Matrix calculus notation in Section 3.2.** The "Backpropagation through Attention" subsection uses Jacobian notation and partial derivatives of the softmax function. This is substantially more advanced than the math used elsewhere in Part I. While the chapter plan tags this as "Intermediate," it requires comfort with matrix calculus that is not provided or referenced.

3. **OPTIONAL: Singular values mentioned without definition.** Section 3.1 discusses gradient behavior in terms of "the largest singular value" of the Jacobian being less than or greater than 1. Singular values are a concept from linear algebra that is not covered in Module 00's prerequisites (which list "vectors, matrices, dot products"). A one-sentence definition or footnote would close this gap.

4. **OPTIONAL: Weak bridge from Module 02 to Module 03.** Section 3.1 opens with a "Big Picture" about why we study RNNs but does not reference token sequences from Module 02. The connection "token IDs become embedding vectors that become x_t inputs to the RNN" is stated later in the section body but not in the opening bridge.

**Recommendation:**
- Add a brief footnote or callout defining the Jacobian matrix when first used in Section 3.1 (e.g., "The Jacobian is the matrix of all partial derivatives of a vector-valued function"). Priority: IMPORTANT.
- Add a note at the start of Section 3.2's backpropagation subsection that this material is mathematically advanced and can be skipped without losing the narrative thread. Priority: IMPORTANT.
- Add a one-line definition of singular values in Section 3.1, or rephrase in terms of eigenvalues. Priority: OPTIONAL.

---

### Module 04: The Transformer Architecture

**Missing Background Concepts:**

| Concept | Where Used | Where Explained | Status | Severity |
|---------|-----------|-----------------|--------|----------|
| Information theory (entropy, cross-entropy, perplexity, KL divergence) | Syllabus promises it; referenced in 4.2 (cross-entropy loss), 4.4 (memory budgeting mentions optimizer states) | **Never formally taught** | **ABSENT** | **BLOCKING** |
| Cross-entropy loss for next-token prediction | Section 4.2 (training loop code) | Section 0.1 defines cross-entropy for classification; 4.2 uses it for language modeling without bridging | GAP | IMPORTANT |
| Label smoothing | Syllabus promises; Section 4.2 code does not use it | ABSENT | GAP | OPTIONAL |
| KV cache | Section 4.3 (MQA, GQA, MLA discussion) | Defined briefly in context | THIN | OPTIONAL |
| CUDA / GPU programming basics | Section 4.4 (Triton labs) | Section 4.4 teaches GPU concepts from scratch | OK | N/A |
| Circuit complexity (TC0) | Section 4.5 | Explained from scratch within the section | OK | N/A |
| AdamW optimizer | Section 4.2 (training loop) | Named; explained in a brief note but not formally | THIN | IMPORTANT |

**Findings:**

1. **BLOCKING: Information theory block is entirely missing.** The syllabus promises a dedicated subsection in Section 4.1 covering "entropy as the theoretical lower bound on compression; cross-entropy loss is an upper bound on true entropy; perplexity = 2^(cross-entropy); KL divergence; mutual information." This subsection does not exist anywhere in Part I. These concepts are referenced later in the course (scaling laws use perplexity, evaluation uses cross-entropy, alignment uses KL divergence, typical sampling in Section 5.2 uses entropy). This is the single most impactful self-containment gap in Part I.

2. **IMPORTANT: Cross-entropy for language modeling is used without the bridge from classification.** Section 0.1 defines cross-entropy as a classification loss. Section 4.2 uses `F.cross_entropy` in the training loop for next-token prediction. The connection between these two uses (classification over the vocabulary at each position) is not explicitly drawn. Students may not realize that next-token prediction is essentially a V-way classification problem at each position.

3. **IMPORTANT: AdamW is used but underspecified.** Section 4.2 uses `torch.optim.AdamW` and has a brief note that AdamW uses "decoupled weight decay," but this presupposes understanding of Adam (which, as noted in Module 00, is itself underexplained). The note mentions "betas" without defining what they control.

4. **OPTIONAL: Section 4.5 (expressiveness theory) is self-contained.** Despite being the most theoretical section, it defines TC0 and universal approximation from scratch within its own text. No prerequisite gap here.

**Recommendation:**
- Add a dedicated information theory subsection to Section 4.1 (or as an appendix) covering entropy, cross-entropy, perplexity, and KL divergence with worked examples. Priority: BLOCKING.
- Add a 1-paragraph bridge in Section 4.2 explicitly connecting cross-entropy for classification (from Module 00) to cross-entropy for next-token prediction. Priority: IMPORTANT.
- Strengthen the AdamW explanation or cross-reference a proper Adam explanation in Module 00. Priority: IMPORTANT.

---

### Module 05: Decoding Strategies and Text Generation

**Missing Background Concepts:**

| Concept | Where Used | Where Explained | Status | Severity |
|---------|-----------|-----------------|--------|----------|
| Entropy (information-theoretic) | Section 5.2 (typical sampling, lab output) | Used in code and prose; never formally defined | GAP | IMPORTANT |
| Log-probability | Section 5.1 (beam search scoring) | Used extensively; explained inline | OK | N/A |
| KL divergence | Section 5.4 (diffusion models) | Mentioned; not defined | GAP | OPTIONAL |
| Finite-state machines / automata | Section 5.3 (grammar-constrained decoding) | Named but not defined | GAP | OPTIONAL |
| ROUGE metric | Section 5.3 (MBR decoding) | Named; not defined | GAP | OPTIONAL |
| Transformer forward pass | Section 5.1 (decoding problem) | Assumed from M04 | OK | N/A |

**Findings:**

1. **IMPORTANT: Entropy is used without formal definition.** Section 5.2 uses entropy in both code (`entropy = -(probs * probs.log()).sum()`) and prose ("typical sampling keeps tokens whose information content is close to the entropy of the distribution"). This is the information-theoretic concept of entropy, not a casual usage. Since the information theory block is missing from Module 04 (as noted above), students encounter entropy in Module 05 with no prior formal treatment.

2. **IMPORTANT: No backward reference to Module 04.** Section 5.1 opens with the decoding problem but does not explicitly say "In Module 04, you built a Transformer that outputs logits at each position; now we learn what to do with those logits." The connection is implied but not stated.

3. **OPTIONAL: Finite-state machines in Section 5.3.** Grammar-constrained decoding is described in terms of "finite-state machines" and "pushdown automata" applied to logit masking. These are computer science concepts that the target audience (software engineers) likely knows, but they are not defined. A one-sentence definition would make the section fully self-contained.

4. **OPTIONAL: ROUGE metric is named but not defined.** Section 5.3's MBR decoding uses "ROUGE as the utility metric." ROUGE is not defined anywhere in Part I. Since evaluation metrics are covered in a later module, a brief parenthetical definition (e.g., "ROUGE, which measures overlap between a candidate and reference texts") would suffice.

**Recommendation:**
- The entropy gap is best fixed by adding the information theory block to Module 04 (see above). If that is deferred, add a brief inline definition of entropy in Section 5.2. Priority: IMPORTANT.
- Add a backward-reference opening sentence in Section 5.1 connecting to Module 04's forward pass. Priority: IMPORTANT.
- Add one-sentence definitions for FSMs and ROUGE where first used. Priority: OPTIONAL.

---

## Cross-Module Bridging Assessment

| Transition | Forward Ref (end of prior module) | Backward Ref (start of next module) | Quality |
|-----------|-----------------------------------|--------------------------------------|---------|
| 00 to 01 | Section 0.4 has "What Comes Next" (but contains a factual error) | Section 1.1 does NOT reference Module 00 | WEAK |
| 01 to 02 | Section 1.4 previews Module 02 | Section 2.1 does NOT reference Module 01 explicitly | ADEQUATE |
| 02 to 03 | Section 2.3 has NO "What Comes Next" | Section 3.1 does NOT reference Module 02 token sequences | WEAK |
| 03 to 04 | Section 3.3 has a "Looking Ahead" callout referencing Module 04 | Section 4.1 recaps multi-head attention from Module 03 | STRONG |
| 04 to 05 | Section 4.5 has NO "What Comes Next" | Section 5.1 does NOT reference Module 04's forward pass | WEAK |

Three of the five cross-module transitions are WEAK. The consistent pattern: the prior module's final section fails to preview the next module, and the next module's opening section fails to reference the prior module.

**Recommendation:** Add a 1 to 2 sentence forward reference at the end of every module's final section and a 1 to 2 sentence backward reference at the start of every module's first section. This is a systematic fix that can be applied as a template across all 6 modules. Priority: IMPORTANT.

---

## Concepts That Are Never Formally Defined in Part I

These concepts appear in the text or code of Part I but are never given a formal definition or explanation anywhere in the six modules.

| Concept | Where It Appears | Impact | Recommended Fix |
|---------|-----------------|--------|-----------------|
| Adam / AdamW optimizer | Code in M00, M04 | Students use it without understanding it | Add explanation in Section 0.2 or 0.3 |
| Entropy (information-theoretic) | M05 Section 5.2 (code and prose) | Students compute it without definition | Add info theory block in M04 Section 4.1 |
| Perplexity | Syllabus; not in delivered content | Referenced in later parts | Add to info theory block |
| KL divergence | M00 Section 0.4 (KL penalty in RLHF), M05 Section 5.4 | Named but never defined | Add to info theory block |
| Self-supervised learning | Implicit throughout (LLM pretraining) | Students lack the category name | Add callout in M00 Section 0.1 |
| Jacobian matrix | M03 Sections 3.1, 3.2 | Used in gradient analysis | Add footnote/callout in M03 Section 3.1 |
| Mutual information | M02 Section 2.2 (WordPiece) | Named but not explained | Add brief definition in context |
| Dynamic programming | M02 Section 2.2 (Viterbi) | Algorithm named but approach not explained | Add brief primer or worked example |
| Singular values | M03 Section 3.1 | Used in gradient analysis | Add one-sentence definition |
| ROUGE metric | M05 Section 5.3 | Named without definition | Add parenthetical definition |
| Finite-state machines | M05 Section 5.3 | Named without definition | Add one-sentence definition |

---

## Recommendations: Where to Add What

### Strategy

Fixes fall into four categories:

1. **Local additions**: Add a paragraph, callout, or footnote within the existing section where the concept is used.
2. **Appendix additions**: Create a standalone reference appendix for foundational concepts (math, information theory).
3. **Cross-references**: Add bridge sentences connecting modules.
4. **Refresher inserts**: Add a brief "refresher box" that recaps a concept from an earlier module at the point of reuse.

### Priority-Ranked Action Items

| # | Finding | Severity | Fix Type | Modules |
|---|---------|----------|----------|---------|
| 1 | Information theory block (entropy, cross-entropy, perplexity, KL divergence) is entirely absent | BLOCKING | Local addition to Section 4.1 (new subsection, ~800 words) or Appendix | 04 |
| 2 | Adam/AdamW optimizer used in code but never explained | BLOCKING | Local addition to Section 0.2 or 0.3 (~200 words + code callout) | 00 |
| 3 | Cross-module bridges missing at 3 of 5 transitions | IMPORTANT | Cross-references: add forward/backward sentences at module boundaries | All |
| 4 | Self-supervised learning never defined | IMPORTANT | Local addition: 1-paragraph callout in Section 0.1 | 00 |
| 5 | Jacobian matrix used without definition in M03 | IMPORTANT | Local addition: footnote or callout in Section 3.1 | 03 |
| 6 | Matrix calculus in Section 3.2 needs a "skip-safe" marker | IMPORTANT | Local addition: note marking the subsection as optional/advanced | 03 |
| 7 | Viterbi/dynamic programming assumed in M02 | IMPORTANT | Local addition: brief primer or step-by-step worked example | 02 |
| 8 | Negative sampling cost not quantified in M01 | IMPORTANT | Local addition: add computational cost comparison | 01 |
| 9 | GloVe co-occurrence ratio not demonstrated in M01 | IMPORTANT | Local addition: add small numeric example | 01 |
| 10 | Entropy used without definition in M05 Section 5.2 | IMPORTANT | Refresher insert (or solved by item 1 above) | 05 |
| 11 | Cross-entropy for language modeling not bridged from classification | IMPORTANT | Refresher insert in Section 4.2 | 04 |
| 12 | WordPiece likelihood criterion underspecified in M02 | IMPORTANT | Local addition: explain difference from BPE | 02 |
| 13 | Section 0.4 cross-reference error ("Module 02" should be "Module 04") | IMPORTANT | Fix: correct the text | 00 |
| 14 | Module 01 has no backward bridge from Module 00 | IMPORTANT | Cross-reference: 1 sentence at top of Section 1.1 | 01 |
| 15 | Singular values used without definition in M03 | OPTIONAL | Local addition: 1-sentence definition or rephrase | 03 |
| 16 | Mutual information named but undefined in M02 | OPTIONAL | Local addition: 1-sentence definition in context | 02 |
| 17 | ROUGE metric named but undefined in M05 | OPTIONAL | Local addition: parenthetical definition | 05 |
| 18 | FSMs named but undefined in M05 | OPTIONAL | Local addition: 1-sentence definition | 05 |
| 19 | NumPy not explicitly taught in M00 | OPTIONAL | Local addition: 2-3 examples in Section 0.3 before PyTorch tensors | 00 |
| 20 | KL divergence named in M00 Section 0.4 but not defined | OPTIONAL | Solved by item 1 above, or add brief definition in M00 | 00, 04 |

---

## Relationship to Prior Phase Reports

Several findings in this report were identified in earlier phases but have not been addressed. This section maps the overlap and notes net-new findings.

### Previously Identified (confirmed in this review)

- Adam optimizer gap: flagged in Phase 1 (Curriculum Alignment), Phase 2 (Code Pedagogy). Still unfixed.
- Information theory gap: flagged in Phase 1 (Curriculum Alignment) as the highest-priority issue. Still unfixed.
- Cross-module bridging weakness: flagged in Phase 1 (Teaching Flow). Still unfixed.
- Section 0.4 cross-reference error: flagged in Phase 1 (Teaching Flow) and Phase 3 (Structural). Still unfixed.
- Negative sampling and GloVe depth gaps: flagged in Phase 1 (Deep Explanation). Still unfixed.
- Viterbi mechanics thinness: flagged in Phase 1 (Deep Explanation). Still unfixed.

### Net-New Findings (unique to this self-containment review)

- Self-supervised learning is never named or defined anywhere in Part I (not flagged by prior phases).
- Jacobian matrix is used without definition, which is a prerequisite gap relative to the stated audience (not flagged by prior phases).
- Matrix calculus subsection in Section 3.2 exceeds the stated math prerequisites without a skip marker (not flagged by prior phases).
- The systematic cross-module bridge analysis (forward + backward at each boundary) is new; prior phases identified individual bridge issues but did not produce the complete transition quality table.
- The comprehensive "never-defined concepts" table is new.

---

## Summary

Part I's core narrative is self-contained: a student can read Modules 00 through 05 in sequence and build a working understanding of ML foundations, NLP representations, tokenization, attention, the Transformer, and text generation. No module uses a concept introduced only in a later module, and no module has an unresolvable dependency.

The gaps that do exist are in two categories:

1. **Background concepts assumed but not provided.** The Adam optimizer, information theory, the Jacobian, dynamic programming, and self-supervised learning are all used in the text without adequate explanation. These gaps affect students who match the stated prerequisites (Python + basic linear algebra + basic probability) but do not have ML or advanced math experience.

2. **Missing connections between modules.** Three of five module transitions lack both a forward preview and a backward bridge. This makes the six-module arc feel like six separate chapters rather than one cohesive journey.

Both categories can be fixed with targeted additions (callout boxes, footnotes, bridge sentences, and one new information theory subsection) totaling roughly 2,000 to 3,000 words across all modules. No structural reorganization is required.
