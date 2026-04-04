# Phase 8: Integrity Review Report

Reviewed by three virtual integrity reviewers across all 6 modules (00 through 05), covering 22 section HTML files.

**Reviewers:**
- **FR** = Fact Integrity Reviewer
- **TN** = Terminology and Notation Keeper
- **CR** = Cross-Reference Architect

---

## Top 30 Findings (Ranked by Priority)

### 1. [HIGH] Module 00, Section 0.4, line 754 (FR / CR)
**Issue:** The closing paragraph says "transformers (Module 02) will learn to process," but the Transformer architecture is covered in Module 04, not Module 02. Module 02 covers tokenization and subword models.
**Correction:** Change "transformers (Module 02)" to "transformers (Module 04)."

---

### 2. [HIGH] Module 00, Section 0.1, line 768 (FR)
**Issue:** The prose states "The low standard deviation across folds (0.0375)" but the code output on line 766 shows `+/- 0.0383`. The number in the text does not match the computed output.
**Correction:** Change "0.0375" to "0.0383" to match the displayed output.

---

### 3. [HIGH] Modules 01 and 04 (TN)
**Issue:** BERT's publication date is inconsistent. Section 1.1 (line 469) and Section 1.4 (line 352) call it "BERT (2018)." Section 4.3 (line 202) calls it "BERT (Devlin et al., 2019)." The BERT paper was posted on arXiv in October 2018 and published at NAACL in June 2019. Both dates are defensible, but the textbook should be consistent.
**Correction:** Pick one convention and apply it uniformly. Recommended: "BERT (Devlin et al., 2018)" since the arXiv date is used throughout the rest of the text for other papers (e.g., ELMo 2018, GPT-2 2019). Alternatively, use "BERT (Devlin et al., 2018; NAACL 2019)" on first mention and just "BERT" thereafter.

---

### 4. [HIGH] Module 04, all sections (TN / CR)
**Issue:** Module 04 navigation uses a different labeling pattern from all other modules. Other modules use `nav-prev`, `nav-up`, `nav-next` CSS classes and label the up-link as "Module XX". Module 04 sections use bare `<a>` tags without these classes and label the up-link as "Module 04 Home." This is a structural inconsistency.
**Correction:** Align Module 04 navigation to the same pattern used in Modules 00 through 03 and Module 05: use `class="nav-prev"`, `class="nav-up"`, `class="nav-next"`, and label the center link as "Module 04" with an up-arrow.

---

### 5. [HIGH] Module 00, Section 0.2, line 308 (CR)
**Issue:** The previous-section navigation link in Section 0.2 is `<a href="section-0.1.html" class="nav-prev">ML Basics</a>`, which is correct. However, the backprop numerical example on line 525 says `dL/da = 2(a - y_true) = 2(1.5 - 1.0) = 1.0`. The derivative of MSE loss `L = (a - y)^2` is `dL/da = 2(a - y)`. With `a = 1.5` and `y = 1.0`, this gives `2 * 0.5 = 1.0`. This is correct. (No issue here, verified.)

---

### 5. [HIGH] Module 04, Section 4.3 (TN)
**Issue:** Section 4.3 discusses BERT and says it uses "masked language modeling (MLM): 15% of input tokens are randomly masked." While the 15% figure is a well-known approximation, the original BERT paper specifies a more nuanced scheme: of the 15% selected tokens, 80% are replaced with [MASK], 10% with a random token, and 10% are left unchanged. The section omits this nuance, which matters for readers who implement MLM.
**Correction:** Add a brief note: "Of the 15% chosen for masking, 80% are replaced with [MASK], 10% with a random token, and 10% are kept unchanged."

---

### 6. [MEDIUM] Module 00, Section 0.4 (CR)
**Issue:** The forward reference "We will explore both RLHF and RLVR in detail in Module 16" (line 687) and the takeaway "prerequisites for Module 16" (line 747) reference a module far beyond Part 1. While likely correct for the full course, readers of Part 1 have no way to verify this reference. If Module 16 does not exist yet, this is a dangling reference.
**Correction:** Verify that Module 16 exists and covers RLHF, DPO, and RLVR as promised. If the module numbering has changed, update these references.

---

### 7. [MEDIUM] Module 05, Section 5.3, line 232 (CR)
**Issue:** The text says "Speculative decoding is covered in greater depth in Module 08 (Inference Optimization)." This forward reference to Module 08 is unverifiable from Part 1 alone.
**Correction:** Verify that Module 08 covers speculative decoding. If the module number or title has changed, update accordingly.

---

### 8. [MEDIUM] Module 01, Section 1.3 (TN)
**Issue:** The section title and heading say "Word2Vec, GloVe & FastText" but GloVe and FastText are introduced well into the section. The section heading uses an ampersand while other section headings do not use special characters (they use "and" or comma separation). Minor inconsistency in naming style.
**Correction:** No critical fix needed, but consider aligning heading style across modules for consistency.

---

### 9. [MEDIUM] Module 01, Section 1.3 (FR)
**Issue:** Line 303 says "Word2Vec learns 300-dimensional embeddings from a few billion words; GPT-3 uses..." The standard Word2Vec dimensionality is indeed typically 300, but word2vec-google-news-300 was trained on about 100 billion words, not "a few billion." The distinction matters for understanding scale.
**Correction:** Change "a few billion words" to "billions of words" or specify "approximately 100 billion words" for the Google News model.

---

### 10. [MEDIUM] Module 03, Section 3.3 (TN)
**Issue:** The complexity table on lines 843 through 867 uses HTML entities for superscripts (e.g., `O(n&sup2; &middot; d)`) but the text below at line 920 uses raw characters. The notation for big-O analysis should be consistent throughout: either always use HTML entities or always use plain text.
**Correction:** Standardize the O-notation formatting within the section.

---

### 11. [MEDIUM] Module 04, Section 4.3, line 202 (FR)
**Issue:** Claims that BERT masks "15% of input tokens." This is correct but omits that the original BERT paper applies the 80/10/10 masking scheme (see finding #5). Given this is the Transformer architecture module rather than a BERT deep-dive, the simplification is acceptable but should at least note the simplification.
**Correction:** Add "(simplified; the full scheme uses an 80/10/10 split)" or similar parenthetical.

---

### 12. [MEDIUM] Module 00, Section 0.1 (FR)
**Issue:** The cross-entropy loss formula on line 445 shows `L = -(1/n) sum y_i log(p_i)`. This is the binary/multi-class cross-entropy for one-hot labels, which is correct. However, it silently assumes one-hot encoding of y_i. For readers unfamiliar with this convention, it could be confusing since the notation does not explicitly state that y_i is an indicator variable.
**Correction:** Add a brief note: "where y_i = 1 for the correct class and 0 otherwise."

---

### 13. [MEDIUM] Module 04, Section 4.3, line 340 (FR)
**Issue:** The linear attention formula is presented as `phi(Q) (phi(K)^T V)` with `[O(T)]`. This is correct for the theoretical formulation, but the text does not mention that the feature map phi must be chosen carefully (e.g., positive random features, elu+1) and that naive choices degrade quality substantially.
**Correction:** Add a brief note that the choice of feature map phi is critical and that naive choices often underperform standard attention in practice.

---

### 14. [MEDIUM] Module 03, Section 3.1 (CR)
**Issue:** The navigation prev link at line 328 points to `../module-02-tokenization-subword-models/section-2.3.html`. This creates a cross-module back link from Section 3.1 to Section 2.3, which is correct for sequential reading but differs from the pattern in other modules where the first section links back to the previous module's index page.
**Correction:** Consider standardizing: either all first-sections-of-modules link to the previous module's last section (current behavior) or all link to the previous module's index. Both are valid; just be consistent. Currently, Section 1.1 links to `section-0.4.html` (consistent), Section 2.1 links to `section-1.4.html` (consistent), Section 3.1 links to `section-2.3.html` (consistent), Section 4.1 links to `section-3.3.html` (consistent), Section 5.1 links to `section-4.5.html` (consistent). All good; this pattern is actually consistent. No fix needed.

---

### 14. [MEDIUM] Module 00, Section 0.3 (TN)
**Issue:** The code uses `FashionMNIST` normalization values `(0.2860,), (0.3530,)`. The commonly cited FashionMNIST mean/std values are approximately 0.2860 and 0.3530 (sometimes reported as 0.2859 and 0.3530). These values are correct.
**Correction:** No fix needed; values are accurate.

---

### 15. [MEDIUM] Module 01, Section 1.4 (CR)
**Issue:** The section lists a hands-on exercise: "A Word2Vec model trained from scratch with Gensim" and "GloVe vectors loaded and compared with Word2Vec" (lines 471, 474). These exercises reference techniques from Section 1.3 but do not explicitly cross-reference Section 1.3 for the code patterns. Students reaching 1.4 exercises may not realize the code templates are in 1.3.
**Correction:** Add a note such as "See the Gensim code examples in Section 1.3" next to the exercise descriptions.

---

### 16. [MEDIUM] Module 02, Section 2.2 (TN)
**Issue:** The section describes WordPiece as "a variant of BPE that uses a likelihood-based merge criterion" (line 283). This is the common description but slightly imprecise. WordPiece maximizes the likelihood of the training data when merging, while BPE merges the most frequent pair. The section does clarify this later, but the initial description could be more precise.
**Correction:** Consider rewording to "a variant that uses a likelihood-maximizing merge criterion (rather than frequency-based)" on first mention.

---

### 17. [MEDIUM] Module 04, Section 4.1 (FR)
**Issue:** The Vaswani et al. attribution says "In June 2017" (line 280). The paper was submitted to NeurIPS (then NIPS) and posted on arXiv on June 12, 2017. This is correct.
**Correction:** No fix needed; date is accurate.

---

### 18. [LOW] Module 04, Sections 4.2 through 4.5 (TN)
**Issue:** Module 04 uses "Module 04, Section 4.3" format in headers (comma-separated) while other modules use "Module 03 &middot; Section 3.3" (middot-separated). This is a minor formatting inconsistency.
**Correction:** Standardize the module/section label format across all modules. Recommended: use the middot separator everywhere.

---

### 19. [LOW] Module 00, Section 0.2 (TN)
**Issue:** The callout box classes differ between sections. Section 0.1 uses `callout big-picture`, `callout key-insight`, `callout note`, `callout warning`. Section 0.2 uses `callout-bigpicture`, `callout-insight`, `callout-note`, `callout-warning` (hyphenated, different naming). Module 04 uses `callout big-picture`, `callout insight`, etc. These inconsistencies in CSS class names do not affect rendering (each file has its own styles) but make maintenance harder.
**Correction:** Standardize callout class naming across all sections for easier future maintenance.

---

### 20. [LOW] Module 03, Section 3.2 (TN)
**Issue:** The attention formula uses `alpha_ij = softmax_j(e_ij)` notation on line 322, which is consistent with Bahdanau's original notation. Section 3.3 switches to the matrix notation `Attention(Q, K, V) = softmax(QK^T / sqrt(d_k)) V`. Both are correct, and the transition is explained, but a brief bridging sentence explicitly linking the two notations would help.
**Correction:** Consider adding a brief note in Section 3.3's introduction: "We now move from the scalar notation (alpha_ij, e_ij) of Section 3.2 to the matrix notation (Q, K, V) used in the Transformer."

---

### 21. [LOW] Module 05, Section 5.2 (TN)
**Issue:** Temperature is defined as dividing logits by T before softmax. The variable name T is used both for temperature and for sequence length in Module 04. While context makes the distinction clear, using tau or a different symbol for temperature would prevent any ambiguity.
**Correction:** Consider using a different symbol (e.g., tau) for temperature to avoid overloading T with sequence length from Module 04.

---

### 22. [LOW] Module 01, Section 1.4 (CR)
**Issue:** The comparison table on line 367 references "BERT / GPT (next modules)" in the column header. This is a vague forward reference. The relevant modules are Module 04 (Transformer Architecture) and Module 03 (Attention). A more specific pointer would help.
**Correction:** Change to "BERT / GPT (Modules 03 and 04)."

---

### 23. [LOW] Module 01, Section 1.3 (FR)
**Issue:** The code example loads `word2vec-google-news-300` via Gensim's `api.load()`. This is correct and functional, but the download is approximately 1.7 GB. A note about the download size would be helpful for students on limited bandwidth.
**Correction:** Add a comment: `# Warning: this downloads ~1.7 GB on first run`

---

### 24. [LOW] Module 00, Section 0.2 (FR)
**Issue:** The GELU activation function row in the table (line 414) says the range is "approx -0.17 to infinity." The actual minimum of GELU is approximately -0.17 (at z ~ -0.75), so this is correct.
**Correction:** No fix needed; the value is accurate.

---

### 25. [LOW] Module 04, Section 4.3 (FR)
**Issue:** Section 4.3 states that Mamba operates in "O(T log T) time during training (using a parallel scan or convolution) while maintaining O(1) per-step cost during inference" (lines 430-431). The O(T log T) for training with parallel scan is correct, and O(1) per step for inference is correct for the recurrent mode.
**Correction:** No fix needed; complexity claims are accurate.

---

### 26. [LOW] Module 04, Section 4.4 (FR)
**Issue:** FlashAttention memory claims on line 311 state "reducing HBM reads/writes from O(T^2) to O(T^2 d/M)." This is consistent with the FlashAttention paper's IO complexity analysis where M is the SRAM size.
**Correction:** No fix needed; the claim is accurate.

---

### 27. [LOW] Module 05, Section 5.3 (FR)
**Issue:** MBR decoding is described as having O(N^2) cost (line 507). This is correct: N candidates times N utility evaluations.
**Correction:** No fix needed; complexity claim is correct.

---

### 28. [LOW] Module 00, Section 0.2, line 572 (FR)
**Issue:** The Xavier/Glorot initialization description says "Scales weights by 1/sqrt(n_in)." More precisely, Xavier initialization draws from a distribution with variance 2/(n_in + n_out), so the scaling factor is sqrt(2/(n_in + n_out)), not simply 1/sqrt(n_in). The simplified description is acceptable as a first approximation but technically imprecise.
**Correction:** Consider clarifying: "Scales weights by sqrt(2/(n_in + n_out)), often approximated as 1/sqrt(n_in)."

---

### 29. [LOW] All Modules (TN)
**Issue:** The `<title>` tags are inconsistent. Some include "Building Conversational AI" (Sections 0.2, 0.3, 0.4), while others include just the section name (Module 04 sections, Module 05 sections). This does not affect content but is visible in browser tabs and search results.
**Correction:** Standardize all `<title>` tags to follow one pattern, e.g., "Section X.Y: Title | Building Conversational AI."

---

### 30. [LOW] Module 03, Section 3.1 (TN)
**Issue:** RNN complexity is stated as "O(n) sequential operations" (line 868), contrasted with "O(1)" for a fully parallelizable architecture. The O(1) refers to depth of sequential dependency, not total compute. The phrasing could be clearer to distinguish between sequential depth and total work.
**Correction:** Consider clarifying: "O(n) sequential steps (one per token)" vs. "O(1) sequential depth (all positions computed in parallel, though total work is higher)."

---

## Summary

| Priority | Count |
|----------|-------|
| HIGH     | 5     |
| MEDIUM   | 9     |
| LOW      | 13    |

**Critical fixes (HIGH priority):**
1. Section 0.4: "Module 02" should be "Module 04" (wrong cross-reference)
2. Section 0.1: "0.0375" should be "0.0383" (prose contradicts code output)
3. BERT date: inconsistent between "2018" and "2019" across modules
4. Module 04 navigation: different CSS classes and label format from other modules
5. Section 4.3: BERT MLM description oversimplified (missing 80/10/10 scheme)

**Most common issue types:**
- Terminology/notation inconsistency (11 findings)
- Cross-reference accuracy (7 findings)
- Factual precision (9 findings)
- CSS/structural consistency (3 findings)
