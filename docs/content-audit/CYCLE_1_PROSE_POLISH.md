# Cycle 1 Prose Polish

Autonomous polish cycle for parts 1-5. Focus: clarity, fragment fixes, broken cross-references masked as prose, and tightening of awkward phrasings. No new content added.

## Summary

- **Sections touched:** 22
- **Edits applied:** 29
- **Themes:**
  - Orphan figure-reference fragments (most common): sentences that started with "shows the X" or "summarizes the Y" because the figure number got dropped during automated edits. Rewrote each as "The diagram below shows..." or restored the specific reference.
  - Broken or self-referential prerequisites: e.g. "Section 6.1 pipeline covered in Section 6.1: The Landmark Models" rewritten to a single, clean reference.
  - Wrong cross-references to "transformer mechanics from Section 4.1" (Section 4.1 is decoding, not transformer mechanics) repointed to Section 3.1.
  - Two factual phrasing cleanups: "Transformer architecture loss" -> "cross-entropy loss"; "consumed during pretraining data and post-training" -> "consumed during pretraining and post-training".
  - One passive/awkward construction tightened in Section 2.1.
  - One overstuffed nested-parenthetical paragraph reflowed using semicolons (Section 7.1).

---

## Edits

### Part 1: LLM Building Blocks

**part-1-llm-building-blocks/module-02-sequence-models-attention/section-2.1.html**
- Before: "The vanilla RNN cell, just three matrix multiplications and a tanh, was the building block on which a decade of sequence modeling was constructed. Every later complication ... was added to fix a problem ..."
- After: "The vanilla RNN cell, just three matrix multiplications and a tanh, built a decade of sequence modeling. Every later complication ... addressed a problem ..."
- Rationale: Two passive constructions reduced to active voice; tightens by ~10 words.

### Part 2: Understanding LLMs

**part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.1.html**
- Before: "The MLM training objective minimizes the Transformer architecture loss over only the masked positions"
- After: "The MLM training objective minimizes the cross-entropy loss over only the masked positions"
- Rationale: "Transformer architecture loss" is not standard terminology; cross-entropy is the actual loss.

**part-2-understanding-llms/module-07-modern-llm-landscape/section-7.1.html**
- Before: A single paragraph with nested parentheticals stacking RLHF, constitutional AI, and RLAIF definitions inside one comma-separated parenthetical.
- After: Reflowed with semicolons separating each alignment procedure, with each acronym expanded inline. Same content, far easier to parse.

**part-2-understanding-llms/module-08-reasoning-test-time-compute/section-8.1.html**
- Before: "Train-time compute is the total processing power consumed during pretraining data and post-training."
- After: "Train-time compute is the total processing power consumed during pretraining and post-training."
- Rationale: "consumed during pretraining data" is ungrammatical.

**part-2-understanding-llms/module-10-interpretability/section-10.1.html**
- Before: "This section builds on softmax architecture from Section 3.1 ... and Section 6.1 covered in Section 6.1: The Landmark Models."
- After: "This section builds on the attention mechanism from Section 3.1 ... and the pretrained models introduced in Section 6.1: The Landmark Models."
- Rationale: "Softmax architecture" was wrong; "Section 6.1 covered in Section 6.1" was a self-reference loop.

### Part 3: Working with LLMs

**part-3-working-with-llms/module-11-llm-apis/section-11.1.html** (two edits)
- Edit 1: "creating a de facto standard. maps this ecosystem..." -> "creating a de facto standard. Figure 11.1.2 maps this ecosystem..."
- Edit 2: "all providers follow the same fundamental lifecycle. illustrates this universal request/response cycle." -> "...lifecycle. The diagram below illustrates this universal request/response cycle."
- Rationale: Two orphan figure references; figure number was dropped, leaving sentences without subjects.

**part-3-working-with-llms/module-11-llm-apis/section-11.2.html**
- Before: "Your application code executes the function and sends the result back to the model, which then incorporates it into its response. shows this request, execute, and respond loop in detail."
- After: "...incorporates it into its response. Figure 11.2.4 shows this request, execute, and respond loop in detail."
- Rationale: Orphan figure reference.

**part-3-working-with-llms/module-11-llm-apis/section-11.4.html** (three edits)
- Edit 1 (line ~70): "...adopted across providers. illustrates how reasoning tokens fit into the generation pipeline, and the table below summarizes..." -> "...adopted across providers. The figure below illustrates how reasoning tokens fit into the generation pipeline, and the table that follows summarizes..."
- Edit 2 (line ~248): "you pass an array of content blocks, each with a type and corresponding data. shows the content block structure..." -> "...corresponding data. The schema below shows the content block structure..."
- Edit 3 (line ~393): "...stream the answer tokens as they arrive. illustrates the streaming event timeline..." -> "...as they arrive. The diagram below illustrates the streaming event timeline..."
- Rationale: Three orphan figure references in the same file.

**part-3-working-with-llms/module-12-prompt-engineering/section-12.1.html**
- Before: "...the actual query arrives. maps these structural components to their corresponding chat API roles."
- After: "...the actual query arrives. Figure 12.1.2 maps these structural components to their corresponding chat API roles."
- Rationale: Orphan figure reference.

**part-3-working-with-llms/module-13-hybrid-ml-llm/section-13.1.html**
- Before: "<p> summarizes this decision framework, showing how data structure..."
- After: "<p>The diagram below summarizes this decision framework, showing how data structure..."
- Rationale: Orphan figure reference at the start of a paragraph.

**part-3-working-with-llms/module-13-hybrid-ml-llm/section-13.3.html**
- Before: "the request is escalated to an LLM for more careful analysis. shows this routing logic. <strong>Code Fragment 13.3.1</strong> shows this approach in practice."
- After: "...for more careful analysis. The figure above illustrates this routing logic, and <strong>Code Fragment 13.3.1</strong> shows the approach in practice."
- Rationale: Orphan figure reference; also consolidated two short sentences into one.

**part-3-working-with-llms/module-13-hybrid-ml-llm/section-13.4.html**
- Before: "...reducing costs by 60-80% with less than 2% quality degradation. shows a complexity-based router..."
- After: "...quality degradation. The diagram below shows a complexity-based router..."
- Rationale: Orphan figure reference.

### Part 4: Training and Adaptation

**part-4-training-adaptation/module-15-synthetic-data/section-15.5.html**
- Before: "...labeling systems at Google, Apple, Intel, and many startups. shows this paradigm."
- After: "...and many startups. The diagram below shows this paradigm."
- Rationale: Orphan figure reference.

**part-4-training-adaptation/module-15-synthetic-data/section-15.6.html**
- Before: "Each stage introduces opportunities for quality control that do not exist in standard data generation. illustrates this pipeline."
- After: "...do not exist in standard data generation. The diagram below illustrates this pipeline."
- Rationale: Orphan figure reference.

**part-4-training-adaptation/module-16-fine-tuning-fundamentals/section-16.1.html** (three edits)
- Edit 1 (prerequisites): "This section builds on pretraining data from Section 6.1: The Landmark Models and training in Section 0.3 covered in Section 0.3: PyTorch Tutorial." -> "This section builds on the pretraining background from Section 6.1: The Landmark Models and the PyTorch training loops covered in Section 0.3: PyTorch Tutorial."
- Edit 2 (line ~72): "Fine-tuning modifies the model weights themselves through additional training on task-specific data. places these approaches on the adaptation spectrum." -> "...task-specific data. The diagram below places these approaches on the adaptation spectrum."
- Edit 3 (line ~222): "and failing to include regularization. shows how task-specific and general performance diverge over training. Code Fragment 16.1.3 shows this approach in practice." -> "...failing to include regularization. The figure below shows how task-specific and general performance diverge over training, and Code Fragment 16.1.3 demonstrates the approach in practice."
- Rationale: One garbled prerequisite, two orphan figure references.

**part-4-training-adaptation/module-16-fine-tuning-fundamentals/section-16.7.html**
- Before: "the rotation angles for unseen positions are extrapolated, causing attention scores to become increasingly noisy. shows this quality degradation beyond the training window."
- After: "...increasingly noisy. The figure below shows this quality degradation beyond the training window."
- Rationale: Orphan figure reference.

**part-4-training-adaptation/module-17-peft/section-17.1.html**
- Before: "This section builds on fine-tuning fundamentals from Section 16.1 ... and layer normalization architecture covered in Section 3.1: Transformer Architecture Deep Dive."
- After: "This section builds on fine-tuning fundamentals from Section 16.1 ... and the transformer architecture covered in Section 3.1: Transformer Architecture Deep Dive."
- Rationale: "Layer normalization architecture" was wrong; the actual prerequisite is the transformer architecture as a whole.

**part-4-training-adaptation/module-17-peft/section-17.5.html** (two edits)
- Edit 1: "these 'soft' probabilities encode semantic relationships that hard labels cannot convey. shows this teacher-student training setup." -> "...cannot convey. The diagram below shows this teacher-student training setup."
- Edit 2: "can be effectively compressed through distillation. summarizes the key principles..." -> "...through distillation. The table below summarizes the key principles..."
- Rationale: Two orphan figure references.

**part-4-training-adaptation/module-17-peft/section-17.7.html**
- Before: "performance on target benchmarks, retention of base model capabilities, and overall coherence. depicts this optimization loop."
- After: "...overall coherence. The diagram below depicts this optimization loop."
- Rationale: Orphan figure reference.

**part-4-training-adaptation/module-18-alignment-rlhf-dpo/section-18.1.html** (two edits)
- Edit 1 (prerequisites): "This section builds on fine-tuning from Section 16.1 ... and Section 6.1 pipeline covered in Section 6.1: The Landmark Models." -> "This section builds on fine-tuning from Section 16.1 ... and the pretraining pipeline covered in Section 6.1: The Landmark Models."
- Edit 2 (line ~117): "transforms a pretrained base model into an aligned assistant. shows the three stages and how they connect." -> "...aligned assistant. Figure 18.1.2a shows the three stages and how they connect."
- Rationale: One garbled prerequisite, one orphan figure reference.

**part-4-training-adaptation/module-18-alignment-rlhf-dpo/section-18.5.html**
- Before: "replacing the human labelers in standard RLHF. shows both phases of this pipeline."
- After: "replacing the human labelers in standard RLHF. The diagram below shows both phases of this pipeline."
- Rationale: Orphan figure reference.

### Part 5: Multimodal LLMs

**part-5-multimodal-llms/module-20-audio-music-generation/section-20.1.html**
- Before (prerequisites): "This section assumes the transformer mechanics from Section 4.1, the tokenization and vocabulary discussion from Section 2.1, and..."
- After: "This section assumes the transformer mechanics from Section 3.1, the tokenization and vocabulary discussion from Section 1.6, and..."
- Rationale: Section 4.1 is "Deterministic Decoding Strategies", not transformer mechanics. Section 2.1 is RNN-era, not tokenization. Repointed to the correct sections.

**part-5-multimodal-llms/module-22-vision-language-models/section-22.1.html**
- Before (prerequisites): "This section assumes the transformer mechanics from Section 4.1, the tokenization and embedding intuition from Section 2.1, and..."
- After: "This section assumes the transformer mechanics from Section 3.1, the tokenization and embedding intuition from Section 1.6, and..."
- Rationale: Same incorrect cross-references as 20.1; repointed identically.

**part-5-multimodal-llms/module-23-3d-generation-neural-scenes/section-23.1.html**
- Before: "This section assumes ... the diffusion intuition from Section 31.1. Familiarity with PyTorch gradient flow from Section 1.5 helps when reading the training loop."
- After: "This section assumes comfort with camera matrices and basic linear algebra (covariance, eigendecomposition). Familiarity with PyTorch gradient flow from Section 0.3 helps when reading the training loop."
- Rationale: Section 31.1 does not exist in this book layout; Section 1.5 is not about PyTorch (Section 0.3 is). Dropped the broken diffusion ref, fixed the PyTorch ref.

---

## What was not touched

- Code blocks, captions, callout titles, and section structure: untouched per cycle constraints.
- Long passages without obvious clarity bugs: left in place to keep the cycle scope-bounded.
- "There are N..." paragraph openings: kept because each one directly precedes a list and the construction is contextually appropriate.
- Heavy passive constructions inside callouts (postmortems, key insights): left because their formal tone is consistent with the book's voice.

## Notes for future cycles

- The orphan-figure-reference pattern (a sentence whose subject is a figure number that was dropped) appears widely in Parts 3 and 4. A targeted regex sweep would surface similar issues in Parts 6+ and the appendices.
- Several prerequisites paragraphs have telltale signs of an automated cross-link rewriter that doubled section references and produced loops like "Section X covered in Section X". A second pass focused only on prerequisite blocks would be efficient.
- The mismatched cross-references in Part 5 (Section 4.1 used as the "transformer mechanics" reference) likely originated from a chapter-renumbering migration; worth auditing all Part 5 prerequisites against the current Part 1 layout.
