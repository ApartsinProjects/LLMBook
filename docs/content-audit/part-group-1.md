# Content Audit, Parts 1 to 4

Audit scope: `part-1-llm-building-blocks/` (modules 00 to 05), `part-2-understanding-llms/` (modules 06 to 10), `part-3-working-with-llms/` (modules 11 to 14), `part-4-training-adaptation/` (modules 15 to 19). Dimensions audited: title clarity, one-line descriptions, section home fit, ordering, and stale references. Read-only audit; no source files were changed.

---

## Cross-Cutting Findings

These issues recur across every chapter in scope. They are listed here once so the per-chapter sections can focus on the specifics.

### A. The placeholder section description "A comprehensive chapter from the Building Conversational AI textbook."

Every `<span class="section-desc">` in every Part-1-through-4 chapter index uses this exact boilerplate (occasionally with "A chapter from..." variant in tools-of-the-trade chapters). It is a global placeholder, not the targeted summary the user asked the audit to flag. The user specifically called out a list of placeholder texts; this one is its sibling, identical in spirit. Proposed: every section needs a one-line description derived from its content. Where I have proposed concrete replacements below, they are starting points; the proposal column for the rest is "REPLACE with one-line summary derived from section body."

The same placeholder also appears in the `<meta name="description">` of every section file, propagated into search snippets and EPUB metadata. Fixing the section-desc spans should also propagate to the meta tag.

A second related placeholder, only one instance in Part-1-to-4: `module-13-hybrid-ml-llm/index.html` line 97, section-desc text is `"Classical ML. A comprehensive chapter from the Building Conversational AI textbook."` (truncated fragment of the title got prepended).

### B. The dual-numbering problem (module number vs. chapter number)

Across all 20 modules in Parts 1 to 4, every module page is internally numbered by its physical module number (Chapter 00, 01, 02, ..., 19) in `<title>`, `<meta description>`, breadcrumb, h1, pagefind meta. But the part index re-labels them with a different sequential chapter number that counts from 0 (Part 1) or skips ahead (Part 2 starts at Chapter 7). Result:

- A reader entering through the part index sees "Chapter 7 Pre-training" linking to `module-06-pretraining-scaling-laws/section-6.1.html`.
- Once on that section, the page identifies itself as "Section 6.1" of "Chapter 6: Pre-training" in breadcrumb, h1, and footnote nav, never as Chapter 7.
- Internal cross-references in body text and `What's Next` callouts say sometimes "Chapter 7" and sometimes "Chapter 6" for the same chapter.

This is structurally inconsistent and is the root cause of most of the "stale reference" findings below. Either:
- Renumber pages to match the part-index numbering (preferred for reader sanity, large mechanical change), or
- Renumber the part index back to match the module numbering (smaller change, but loses the "Chapter 0" through "Chapter 21" linear scheme).

A first-pass rule: a reader looking at "Section 6.1" in their tab title should see "Chapter 6" in every cross-reference to that chapter, in every part index, and in every chapter-card label.

### C. Module-internal section heading IDs vs. heading text drift

Every section file uses `id="X-Y-Z-slug"` IDs that follow the physical module-section numbering (e.g. `id="5-1-1-hardware-tiers"`) while the visible heading text follows the part-index chapter number (`<h2>6.1.1 Hardware tiers</h2>`). Examples confirmed in section-5.1.html, section-3.1.html, section-3.2.html, section-5.2.html, section-15.7.html, section-10.6.html. This makes deep anchors fragile: a link to `#5-1-1-...` works, a link to `#6-1-1-...` 404s. Recommend: pick one numbering and re-emit both IDs and visible heading numbers to match it.

### D. Figure / Code Fragment numbers drift

Figure numbers in `<figcaption><strong>Figure X.Y.Z</strong>` use the new chapter number while the surrounding ID and section labels often use the old/module number. Examples:
- section-2.1.html line 55: "Figure 3.1.1" caption but section is "Section 2.1" and breadcrumb is "Chapter 2".
- section-3.5.html line 55: "Figure 4.3.1" caption, but section ID is "3.3", breadcrumb is "Chapter 3".
- section-4.1.html line 55: "Figure 5.1.1" caption, but section is "Section 4.1", breadcrumb is "Chapter 4".

Same pattern across most figure captions in Parts 1 to 4. After picking one numbering scheme, regenerate figure/code-fragment captions to match.

### E. Tools-of-the-Trade super-chapter inflation

Every "Tools of the Trade" chapter in Parts 1 to 4 (modules 05, 14, 19 in our scope, and module-10 sections 10.6 to 10.9 covertly housing Part 2's tools content) inflates its section count by listing anchor-deep sub-headings as if they were top-level sections in the part index:

- Part 1 index, Chapter 6: lists 18 sections, but 6.6 to 6.18 are anchor links into sections 6.1 / 6.2 (e.g. 6.6 HuggingFace Hub points to `section-5.2.html#6-2-huggingface-hub`).
- Part 2 index, Chapter 12: lists 10 sections, but 12.6 to 12.10 are anchor links.
- Part 3 index, Chapter 16: lists 8 sections, but 16.6 to 16.8 are anchor links.
- Part 4 index, Chapter 21: lists 20 sections, but 21.6 to 21.20 are anchor links. This is the worst offender.

These are restructure artifacts from an older toolbox layout. Anchor sub-headings should be presented as sub-section bullets *underneath* their parent section card, not as siblings. Currently they make the part index look like the book has a 20-section super-chapter at the end of every part, which exaggerates the actual content count and visually buries the real sections.

Also, the Tools-of-the-Trade content for Part 2 ("Chapter 12") physically lives inside `module-10-interpretability/section-10.6.html` through `section-10.11.html`. This makes searching, linking, and authoring confusing. Should move into a dedicated `module-XX-tools-of-the-trade-models-tokenizers/` directory parallel to other parts' tools modules.

### F. Cross-part jumps disguised as in-part sections

- Part 2 index, Chapter 8 "Modern LLM Landscape" includes Section 8.3 "Reasoning Models & Test-Time Compute" whose href jumps out to `module-08-reasoning-test-time-compute/index.html` (a different chapter). Then Section 8.4 (Multilingual) lives in module-07. Two distinct section cards both numbered 8.3 (one href into module-08, one into module-07).
- Part 3 index, Chapter 15 "Hybrid ML+LLM" includes Section 15.5 "Structured Information Extraction" linking to `../part-7-retrieval-information-extraction-with-llms/module-34-structured-information-extraction-ner/`. Jumps to Part 7.

These produce duplicate or non-sequential section numbers in the part index and make the "what is in this chapter" question unanswerable. Recommend: either inline the content into the chapter, drop the misleading section card, or surface it as a clearly-labeled "See also" pointer rather than a section number.

### G. Pervasive stale chapter-number references in body text

Cross-references in body text use a mix of old chapter numbers (20, 23, 26, 31, 32, 37, 50) and new ones. The old numbers correspond to the pre-restructure book where alignment was Ch 20, agents Ch 26, RAG Ch 23, safety Ch 37, vibe-coding Ch 50, etc. The new structure renumbers everything. Examples are listed under each chapter below. Bulk fix needed.

### H. Module 00 (Chapter 0) appears last in Part 1 index

In `part-1-llm-building-blocks/index.html` the chapter cards are ordered Chapter 1 (NLP), Chapter 2 (Tokenization), Chapter 3 (Seq Models), Chapter 4 (Transformer), Chapter 5 (Decoding), Chapter 6 (Tools), then *finally* Chapter 0 (ML & PyTorch Foundations) at the bottom. The body and prerequisites both rely on Chapter 0 being the first chapter you read. The reading order is broken in the part index. Move Chapter 0 to the top of the card list.

---

## Part 1: LLM Building Blocks

### Part 1 index page (`part-1-llm-building-blocks/index.html`)

- **Title**: KEEP "Part I: Foundations" (subtitle is good).
- **Ordering**: PROPOSE Chapter 0 first. Currently it appears as the last chapter-card after Chapter 6 (line 122). Move the Chapter 0 card to the top, before Chapter 1.
- **Description (big-picture)**: KEEP (line 41 reads well).
- **Section count claim**: Line 36 says "Chapters: 7 (Chapters 0 through 6) covering approximately 60,000 words". Verify the 60,000-word claim is still accurate after the restructure.
- **Chapter 2 split-from-module-01**: Tokenization (Ch 2) sections live inside `module-01-foundations-nlp-text-representation/`. Section files are `section-1.5.html` through `section-1.7.html` but appear in the part index as "2.1", "2.2", "2.3". Either rename the section files (`section-2.1.html` etc., move into a new `module-02-tokenization/` directory) or accept the split. Right now reading-order, breadcrumbs, and prerequisite links all reference the new chapter (2) numbering but URLs and file paths reference the old (1.5-1.7) numbering. This is the single most confusing structural artifact in Part 1.
- **Tools chapter inflation**: Ch 6 lists 18 sections; only the first 5 are real. 6.6 to 6.18 are anchor links into 6.1 and 6.2. See cross-cutting finding E.

### Chapter 0: ML and PyTorch Foundations (`module-00-ml-pytorch-foundations/`)

- **Title**: KEEP.
- **Description (big-picture)**: KEEP (line 61 reads well).
- **Section descriptions**: All four sections (0.1 to 0.4) use the global placeholder text. Proposed replacements:
  - 0.1 What Every LLM Engineer Needs From Classical ML: "Features, supervised learning, loss functions, gradient descent, and the bias-variance tradeoff, the classical-ML vocabulary every LLM concept later in the book depends on."
  - 0.2 Deep Learning Essentials: "Perceptrons, multi-layer networks, backpropagation, activation functions, and the layer-stacking idea that powers every modern deep model."
  - 0.3 PyTorch in 90 Minutes: Tensors to Training Loop: "Hands-on PyTorch tour from tensors and autograd through Datasets, DataLoaders, and a complete training loop on GPU."
  - 0.4 Reinforcement Learning Foundations: "Agents, policies, rewards, value functions, and the RL framework that RLHF and RLVR will build on in Part 4."
- **Ordering**: KEEP. ML basics, deep learning, PyTorch tutorial, RL is a clean ladder.
- **Stale refs**:
  - `index.html` line 49: "AI agents (Chapter 26)". Chapter 26 belongs to old numbering. Verify whether agents are in Part 6 module-26 still or renumbered; the in-text "Chapter 26" reference is dangling.
  - `index.html` line 59: "explored in full in Chapter 20: Alignment, RLHF & DPO". Alignment is now Chapter 20 in the *part-index numbering* (module-18), but it's labeled as Chapter 18 in the module's own header. Pick one and use everywhere.
  - `index.html` line 68: "(Chapter 20)" alignment reference, same issue.
  - `section-0.2.html` line 282: "Chapter 31: Multimodal Models" linked to `part-5-multimodal-llms/module-20-audio-music-generation/`. Module-20 is about audio/music, not Ch 31. Title and link both wrong.
  - `section-0.5.html` line 47: "Section 20.1" in text, link goes to `module-18-alignment-rlhf-dpo/section-18.1.html`. The link is correct (alignment chapter); the text "20.1" matches the new part-index number for alignment but conflicts with the file's own "Section 18.1" h1. Same root cause as cross-cutting finding B.
  - `section-0.5.html` lines 374, 379, 451: "Chapter 20" alignment references; one (line 451) correctly links to `module-18-alignment-rlhf-dpo/`. Same dual-numbering issue.
- **Home fit / consolidation**: Section 0.5 (RL) is correctly placed here as a foundation for RLHF later. Good.

### Chapter 1: Foundations of NLP & Text Representation (`module-01-foundations-nlp-text-representation/`)

- **Title**: KEEP. Strong, clear, hierarchy-fit.
- **Description (big-picture)**: KEEP (line 59 reads well).
- **Section descriptions**: All four (1.1 to 1.4) use the placeholder.
  - 1.1 Introduction to NLP & the LLM Revolution: "The story of NLP from rule-based systems to today's LLMs, and why representation is the question every breakthrough answers."
  - 1.2 Text Preprocessing & Classical Representations: "Tokenization, stemming, lemmatization, stop-word filtering, plus Bag-of-Words, n-grams, and TF-IDF as your first numeric representations of text."
  - 1.3 Word Embeddings: Word2Vec, GloVe & FastText: "Static word vectors, the king-queen analogy, training your own Word2Vec, and the geometric intuition that makes neural NLP possible."
  - 1.4 Contextual Embeddings: ELMo & the Path to Transformers: "From a single vector per word to a context-dependent one, the conceptual bridge from static embeddings to the attention models in Chapter 3."
- **Ordering**: KEEP.
- **Stale refs**:
  - `index.html` line 110: `next` nav points to `../module-01-foundations-nlp-text-representation/` (the same module). Should point to `../module-02-sequence-models-attention/`. The label says "Chapter 02 Tokenization and Subword Models", consistent with the Chapter-2-lives-in-module-01 split.
  - `section-1.3.html` line 324-325: "Chapter 22 ... Chapter 23" references vector DBs and RAG; these are now in Part 7 with new module numbers. Update labels to match new chapter numbering or rely on link text alone.
  - `section-1.2.html` line 419: "Chapter 23" RAG reference, same.
- **Home fit / consolidation**: Good. Section 1.4 (ELMo) is the natural bridge to seq2seq attention in Ch 3.

### Chapter 2: Tokenization and Subword Models (sections 1.5 to 1.7 in `module-01-...`)

- **Title**: KEEP "Tokenization and Subword Models".
- **Index page**: There is no separate `module-02-tokenization/index.html`. The chapter has no chapter index at all; it's a phantom chapter inside module-01. Either:
  1. Create a real `module-02-tokenization/` directory with an index and move section files in, renamed to `section-2.1.html` etc., or
  2. At minimum, add a `chapter-2-index.html` inside module-01 with the chapter overview, big-picture, prerequisites, and section cards.
- **Description (big-picture)**: No big-picture exists. Propose: "Tokenization is the alphabet your model speaks. This chapter covers BPE, WordPiece, SentencePiece, Unigram, and the multilingual considerations that make subword tokenization the modern default."
- **Section descriptions** (Part 1 index labels these 2.1, 2.2, 2.3):
  - 2.1 Why Tokenization Matters (file 1.5): "What tokenization is, why it matters for vocabulary size, OOV rates, and model performance, and why the choice of tokenizer shapes everything downstream."
  - 2.2 Subword Tokenization Algorithms (file 1.6): "BPE, WordPiece, SentencePiece, Unigram, and the algorithmic tradeoffs that make subword tokenization the default for modern LLMs."
  - 2.3 Tokenization in Practice & Multilingual Considerations (file 1.7): "Using HuggingFace tokenizers, handling whitespace, byte fallback, and the multilingual edge cases that break naive tokenization."
- **Ordering**: KEEP. Why -> How -> Practice.
- **Stale refs**:
  - `section-1.7.html` line 38: "Section 13.1" / `section-11.1.html` link, prereq says "how LLMs are accessed through APIs". Chapter 13 in new numbering is APIs (module-11). Stale numbering in label text.
  - `section-1.7.html` line 132: "LLM APIs (Section 13.1) ... Chapter 14" same dual-numbering.
  - File numbering itself: physical files named 1.5, 1.6, 1.7 but rendered as 2.1, 2.2, 2.3 in part index. Decide on a single scheme.
- **Home fit / consolidation**: Section content fits Ch 2 well, but the physical-file split into module-01 is the problem.

### Chapter 3: Sequence Models & the Attention Mechanism (`module-02-sequence-models-attention/`)

- **Title**: KEEP. Clear, fits Part 1.
- **Description (big-picture)**: KEEP (line 68 reads well: "Attention solves the problem that ended the RNN era").
- **Section descriptions** (all three use the placeholder):
  - 3.1 Why RNNs Couldn't Scale to Modern LLMs: "Recurrent neural networks, LSTM and GRU cells, the vanishing-gradient problem, and the information bottleneck that motivated the search for something better."
  - 3.2 The Attention Mechanism: "Bahdanau and Luong attention, alignment scores, weighted context vectors, and the breakthrough idea that lets a decoder look back at any encoder state."
  - 3.3 Scaled Dot-Product & Multi-Head Attention: "Query/Key/Value abstraction, scaled dot-product attention, causal masking, and multi-head attention, the engine inside every Transformer block."
- **Ordering**: KEEP. RNN failure -> attention concept -> formal multi-head.
- **Stale refs**:
  - `index.html` line 33: breadcrumb "Chapter 2" but Part 1 index calls this Chapter 3. Dual-numbering.
  - `index.html` line 8 (title) and line 7 (meta): "Chapter 03". The Part 1 index calls it Chapter 3 too, so this is consistent. But other modules use the part-index number in title; pick one convention.
  - `section-2.1.html` line 36: breadcrumb "Chapter 2" but section 2.1 in this module is labeled "3.1" in part index. Line 47 prereq says "Section 2.2" but link goes to `module-01/section-1.6.html` which is in fact Section 2.2 of Ch 2 (Tokenization). Consistent with Ch 2 split but confusing across the dual-numbering.
  - `section-2.1.html` line 51: "Sections 3.2 and 3.3" referring to its own chapter, in the new numbering. Good direction, bad consistency with breadcrumb.
  - `section-2.1.html` line 55: "Figure 3.1.1" caption, consistent with new chapter numbering, but section h1 still labeled "Section 2.1".
  - `section-2.1.html` line 57: id "2-1-1-...", visible heading "3.1.1 The Sequence Modeling Problem".
  - `section-2.1.html` line 59: "Chapter 02" link, but goes to module-01 which is Chapter 1 (NLP) in new numbering. Tokenization is the right concept but Chapter 1 holds NLP not Chapter 2.
- **Home fit / consolidation**: Good fit in Part 1.

### Chapter 4: The Transformer Architecture (`module-03-transformer-architecture/`)

- **Title**: KEEP. The marquee chapter of Part 1.
- **Description (big-picture)**: KEEP (line 55 reads well).
- **Section descriptions** (all five use the placeholder):
  - 4.1 How a Transformer Computes One Token: "End-to-end walkthrough of a single forward pass: embeddings, positional encoding, attention, residual + LayerNorm, feed-forward, repeat, and the final unembedding."
  - 4.2 Build a Transformer from Scratch: "A 300-line decoder-only Transformer in PyTorch trained on a small corpus, the most important code in the book."
  - 4.3 Transformer Variants & Efficiency: "Encoder-only vs decoder-only vs encoder-decoder, sparse and linear attention, FlashAttention, SSMs, MoE, and the design space beyond vanilla Transformers."
  - 4.4 GPU Fundamentals & Systems: "Streaming Multiprocessors, memory hierarchy, bandwidth, kernel fusion, and a basic Triton kernel, the systems substrate every Transformer sits on."
  - 4.5 Transformer Expressiveness Theory: "Universal approximation, computational complexity (TC0, P, PSPACE), and why chain-of-thought changes the picture, an optional deep dive."
- **Ordering**: PROPOSE KEEP, but consider moving 4.4 (GPU Fundamentals) ahead of 4.3 since 4.3 (Variants & Efficiency) refers to FlashAttention which is GPU-aware. Currently 4.3 leans on hardware vocabulary that 4.4 hasn't introduced. Either move 4.4 before 4.3, or add a forward pointer in 4.3.
- **Stale refs**:
  - `index.html` line 24: breadcrumb "Chapter 3" but Part 1 index calls this Chapter 4.
  - `index.html` line 38: "Section 3.1" / "Section 3.2" references in the new numbering; consistent.
  - `index.html` line 45: "Chapter 03" prereq label; conflicts with new "Chapter 3 Sequence Models" being module-02.
  - `index.html` line 69: "Chapter 11: Interpretability". In new numbering, interpretability is Chapter 11 (module-10), so this is correct. But the reference text and target are both ambiguous given the dual-numbering elsewhere.
  - `section-3.1.html` line 51 prereq: "Section 3.5" for self-attention, link to module-02 (sequence models). Section 2.3 of module-02 IS Section 3.5 in part-index. Consistent in *spirit*, confusing on the page.
  - `section-3.1.html` line 59 big-picture: "Section 3.5" same.
  - `section-3.2.html` line 38: "Section 3.5" reference to layer norm via module-02/section-2.3.html. Same.
  - `section-3.2.html` line 48: "Chapter 18" reference to fine-tuning, link to `module-16-fine-tuning-fundamentals/section-16.1.html`. Module 16's own title says "Chapter 16". Dual-numbering.
  - `section-3.5.html` line 51 prereq: "Section 3.5" referring to module-02/section-2.3.html (self-attention); same.
  - `section-3.5.html` line 51: "Chapter 09" link to inference-optimization. Module 09 is inference, but new numbering calls it Chapter 10. Stale.
  - `section-3.6.html` line 51: "Section 10.1" / `module-09-inference-optimization/section-9.1.html`. Same.
  - `section-3.6.html` line 51: "Section 7.4" / `module-06-pretraining-scaling-laws/section-6.3.html`. New numbering for pretraining is 7.3.
  - `section-3.7.html` line 49 / line 59 / line 211: "Section 14.2" in text linked to `module-12-prompt-engineering/section-12.2.html`. New numbering 14.2. Consistent.
  - `section-3.7.html` line 211: "Section 8.3" reasoning models reference, link to `module-08-reasoning-test-time-compute/index.html`. The chapter now has its own home but section reference is loose.
- **Home fit / consolidation**: 4.5 (Expressiveness Theory) is correctly marked Optional. Reader who skips it loses nothing for Part 2.

### Chapter 5: Decoding Strategies & Text Generation (`module-04-decoding-text-generation/`)

- **Title**: KEEP.
- **Description (big-picture)**: KEEP (line 56 includes useful canonical references).
- **Section descriptions** (all four use the placeholder):
  - 5.1 Deterministic Decoding Strategies: "Greedy and beam search, why they fail open-ended generation but win at translation, and the degenerate-repetition trap."
  - 5.2 Stochastic Sampling Methods: "Temperature, top-k, top-p (nucleus), min-p, frequency and presence penalties, and the API knobs you actually turn in production."
  - 5.3 Advanced Decoding & Structured Generation: "Contrastive decoding, speculative decoding, MBR, grammar-constrained generation, and text watermarking."
  - 5.4 Diffusion-Based Language Models: "Discrete diffusion for text, masked-diffusion training, and the non-autoregressive paradigm that started challenging next-token prediction in 2024-2025."
- **Ordering**: KEEP. Deterministic -> stochastic -> advanced -> diffusion (paradigm-shift) is a clean arc.
- **Stale refs**:
  - `section-4.1.html` line 47: "Section 13.2" / `module-11-llm-apis/section-11.2.html`. New numbering correct in text label.
  - `section-4.2.html` line 93: "Chapter 13 ... Chapter 20" references to APIs and distillation. Distillation is now Section 19.6, not Chapter 20 (which is alignment in new numbering).
  - `section-4.4.html` line 38: "Sections 5.1 and 5.2" referencing 4.1 / 4.2 in new chapter numbering; consistent.
- **Home fit / consolidation**: Section 5.5 (Diffusion LMs) is appropriately marked as research-frontier.

### Chapter 6: Tools of the Trade: Foundations Stack (`module-05-tools-of-the-trade/`)

- **Title**: KEEP "Tools of the Trade: Foundations Stack".
- **Description (big-picture)**: KEEP (line 35 is a strong summary).
- **Section descriptions** (placeholder "A chapter from..." variant):
  - 6.1 Platforms: "Hardware tiers (laptop CPU, consumer GPU, cloud accelerator), hosted notebooks (Colab, Kaggle, Lightning), local stack (Python, uv, MLX), and how to pick the platform for each Part-1 exercise."
  - 6.2 Libraries & Frameworks: "PyTorch 2.x with torch.compile, JAX as the second engine, NumPy / SciPy / pandas / polars, scikit-learn baselines, and the HuggingFace tokenizer/datasets layer."
  - 6.3 Datasets & Benchmarks: "MNIST, CIFAR-10, SQuAD, GLUE, WikiText, and the canonical teaching corpora every Part-1 exercise uses."
  - 6.4 Models: "BERT-base, GPT-2, and the other small open-weight checkpoints small enough to fit on a 6 GB GPU."
  - 6.5 External Reading & Communities: "Books, papers, blogs, Discord servers, and the open-source projects worth following for Part-1-level work."
- **Ordering**: KEEP for the first five sections. Subsections 6.6 to 6.18 should not be top-level cards (see finding E).
- **Stale refs**:
  - `index.html` line 8: title "Chapter 5" but Part 1 index labels this Chapter 6. Dual-numbering.
  - `index.html` line 22: breadcrumb "Chapter 5".
  - `index.html` line 73 What Comes Next: "Chapter 12 closes Part II". Part 2's tools chapter is module-14 in part 3 (no, wait, it's the *Part 2* tools chapter, which is the buried module-10/section-10.5-10.9 content labeled Chapter 12 in Part 2 index). The reference is roughly correct but understated; says nothing about where the chapter actually lives.
  - `index.html` line 76 prev nav: "Chapter 05 Decoding Strategies"; should be Chapter 5 (Decoding) but Part-1-index calls this current chapter (Tools) Chapter 6, so prev would be Chapter 5 (Decoding). Need to update so the prev label matches the part-index numbering.
  - `index.html` line 78 next nav: "Chapter 07 Pretraining"; should be Chapter 7 in part-index numbering. Inconsistent capitalization of "Chapter 07" vs "Chapter 7".
  - `section-5.1.html` line 30, 32, 39, 51: h2 IDs start with `5-1-`, visible heading numbers say `6.1.`. Sub-section drift (finding C).
  - `section-5.1.html` line 55: "Section 12.1" in text, link goes to `module-10-interpretability/section-10.6.html`. New numbering correct in label, but target is the Tools-of-Trade content hidden inside the interp module (finding E continued).
  - `section-5.1.html` line 377, 443: "Chapter 50.2 (Vibe-Coding with LLMs)". Chapter 50 belongs to old numbering. Replace with the correct new-numbering location of vibe coding content (probably in Part 14 designing-llm-agent-products, but unverified).
  - `section-5.2.html` line 29 onward: h2 IDs `5-2-X`, visible "6.2.X".
  - `section-5.2.html` line 43: "Chapter 7" tokenizers reference, link to `module-01-foundations-nlp-text-representation/` (Chapter 1 in new numbering, *not* 7). Wrong target chapter number AND wrong target chapter for tokenizers (should be Chapter 2 / module-01 sections 1.5-1.7).
  - `section-5.2.html` line 547: "Section 20.1" DPO reference, label uses old numbering.
  - `section-5.2.html` line 1058: "Section H.6" and "Section 16.1" references; "Section H.6" probably refers to an appendix section that needs verification.
- **Home fit / consolidation**: The 13 anchor-only sub-sections (6.6 through 6.18) should be demoted to sub-headings under their parent section card. Their current top-level presentation is misleading.

---

## Part 2: Understanding LLMs

### Part 2 index page (`part-2-understanding-llms/index.html`)

- **Title**: KEEP "Part II: Understanding LLMs".
- **Description (big-picture)**: KEEP (line 41).
- **Chapter card numbering**: Chapters 7 through 12 in the part index; module folders are 06 through 10 with module-10 holding sections for both Chapter 11 (10.1-10.4) AND Chapter 12 (10.5-10.9). This is the "tools chapter hidden inside the interpretability module" problem (finding E). Recommend splitting into a real `module-XX-tools-models-tokenizers/` directory.
- **Chapter 8 has duplicate Section 8.3**: Lines 65 and 66 list two different "8.3" entries:
  - 8.3 Reasoning Models & Test-Time Compute, href to `module-08-reasoning-test-time-compute/index.html`
  - 8.4 Multilingual & Cross-Cultural LLMs, href to `module-07/section-7.4.html`
  
  Wait, line 66 is labeled "8.4" but the wider Chapter 8 card structure has the "8.3 Reasoning" card pointing to a *different chapter's index*. Fix: drop the cross-chapter "8.3 Reasoning Models" card from Chapter 8 (since reasoning has its own Chapter 9), or move multilingual content into module-08. The current state misleads the reader into thinking Chapter 8 has 4 sections.
- **Chapter 12 inflation**: 10 sections, 5 of which are anchor links (12.6 to 12.10).

### Chapter 6 (part-index: Chapter 7): Pre-training, Scaling Laws & Data Curation (`module-06-pretraining-scaling-laws/`)

- **Title**: KEEP. Long but descriptive.
- **Description (big-picture)**: KEEP (line 59).
- **Section descriptions** (placeholder; 9 sections):
  - 6.1 BERT, GPT, T5: Three Bets That Shaped Today's LLMs: "How the encoder-only, decoder-only, and encoder-decoder bets played out, and what each got right."
  - 6.2 Pre-training Objectives & Paradigms: "Causal LM, masked LM, span corruption, fill-in-the-middle, and multi-token prediction objectives compared head to head."
  - 6.3 Scaling Laws & Compute-Optimal Training: "Kaplan and Chinchilla laws, the Chinchilla reconciliation, and how to plan a training budget."
  - 6.4 Data Curation at Scale: "Deduplication, quality filtering, FineWeb-style pipelines, and the data hygiene that determines model quality."
  - 6.5 Optimizers & Training Dynamics: "Adam, AdamW, Adafactor, learning-rate schedules, and the optimization choices that make billion-parameter training stable."
  - 6.6 Distributed Training at Scale: "DDP, FSDP, ZeRO, tensor parallelism, pipeline parallelism, and the right strategy for your hardware."
  - 6.7 In-Context Learning Theory: "Meta-learning, implicit gradient descent, and task vectors, theories of how an LLM learns from few-shot examples."
  - 6.8 Production LLM Training Systems: Megatron, Elastic Training, and Fault Tolerance: "Megatron-LM, elastic training, checkpointing, and the systems engineering of a real pretraining run."
  - 6.9 Lab: Pretrain a Tiny Language Model: KEEP existing desc on line 125 (it's already non-placeholder).
- **Ordering**: PROPOSE KEEP. 6.1 (history) -> 6.2 (objectives) -> 6.3 (scaling) -> 6.4 (data) -> 6.5 (optimizers) -> 6.6 (distributed) -> 6.7 (ICL theory) -> 6.8 (production systems) -> 6.9 (lab). Reasonable arc. Consider moving 6.7 (ICL theory) before 6.8 or as an optional sidebar since it's conceptual rather than operational.
- **Stale refs**:
  - `index.html` line 67: "Chapter 18: Fine-Tuning" reference for distributed training, matches new numbering.
  - `index.html` line 142 next: "Chapter 08 Modern LLM Landscape", inconsistent zero-padding.
  - `index.html` line 124 the duplicate 6.9 card (lines 128-134): redundant section-grid duplication. Drop one.
  - `section-6.2.html` line 168: "Chapter 14" prompt engineering reference, matches new numbering.
  - `section-6.9.html` line 280: "Chapter 15: Hybrid ML and LLM Systems" reference for the *next* chapter, but the actual next chapter is "Chapter 7 (or 8 in part-index) Modern LLM Landscape", not Chapter 15. This is a hard error in the "what's next" text.

### Chapter 7 (part-index: Chapter 8): Modern LLM Landscape & Model Internals (`module-07-modern-llm-landscape/`)

- **Title**: KEEP "Modern LLM Landscape & Model Internals". But the subtitle "Model Internals" promises more than 3 sections deliver; consider trimming to just "Modern LLM Landscape" since model internals are covered in Ch 4 / Ch 11.
- **Description (big-picture)**: KEEP (line 63).
- **Section descriptions** (placeholders):
  - 7.1 Closed-Source Frontier Models: "GPT, Claude, Gemini, and their architectural hints, pricing tiers, context windows, and the capability frontier as of 2026."
  - 7.2 Open-Source & Open-Weight Models: "Llama, Mistral, Qwen, DeepSeek, Gemma, and the architectural innovations (MoE, MLA, FP8, GQA, sliding window) that distinguish them."
  - 7.3 Multilingual & Cross-Cultural LLMs: "Tokenizer bias, cross-lingual transfer, fine-tuning for low-resource languages, and the cultural choices baked into a model's training data."
- **Ordering**: Currently 7.1 (closed) -> 7.2 (open) -> 7.3 (a fake card linking to reasoning chapter) -> 7.3 (multilingual). Duplicate numbering. Drop the cross-chapter card; renumber multilingual as 7.3 cleanly.
- **Stale refs**:
  - `index.html` line 38: "Chapter 7 told you how LLMs are trained" referring to module-06 (pretraining). In new part-index numbering, pretraining IS Chapter 7. But this module's own footer numbering says it is Chapter 7 too (in title) but Chapter 8 in part-index. Confusion.
  - `index.html` lines 53-57 chapter overview text: "Section 7.1", "Section 7.3", "Section 7.4", "Section 7.4" (literally two 7.3s in the body text).
  - `index.html` line 97: section-card href `../module-08-reasoning-test-time-compute/index.html` listed as Section 7.4, but module-08 is its own chapter. Drop this card.
  - `index.html` line 115 next: "Chapter 09 Reasoning Models". Inconsistent zero-padding.
  - `section-7.1.html` line 50, 91 contain content with "Chapter 1X" inline references (omitted lines, need spot fix).
  - `section-7.3.html` line 475: "Chapter 15" hybrid ML reference matches new numbering.
  - `section-7.4.html` lines 66, 334: "Chapter 18" fine-tuning reference matches new numbering.
- **Home fit / consolidation**: Section 7.4 (multilingual) is small and could live as a sub-section of 7.2 (open-weight models, where most multilingual variants exist) if the chapter feels thin. But the topic is important enough to deserve its own section.

### Chapter 8 (part-index: Chapter 9): Reasoning Models & Test-Time Compute (`module-08-reasoning-test-time-compute/`)

- **Title**: KEEP. Clear and topical.
- **Description (big-picture)**: KEEP (line 65). 
- **Section descriptions** (all 6 use placeholder; chapter has 8.1 to 8.6):
  - 8.1 Trading FLOPs for IQ: The Test-Time Compute Bet: "Why letting a model think longer at inference time can beat training a bigger one, with worked examples on AIME and MATH-500."
  - 8.2 Reasoning Model Architectures: o1, o3, R1, QwQ: "Architecture, training data, and reasoning patterns of the major reasoning models released 2024-2025."
  - 8.3 Training Reasoning Models: RLVR, GRPO, PRM: "Reinforcement Learning with Verifiable Rewards, Group Relative Policy Optimization, and Process Reward Models, the techniques behind DeepSeek-R1."
  - 8.4 Prompting and Using Reasoning Models: "Budget control, hidden-CoT extraction, and the practical recipes for getting useful work out of o3-class models in production."
  - 8.5 Compute-Optimal Inference and Evaluation: "Best-of-N, majority voting, MCTS, and the compute-quality Pareto curve that decides how many tokens to spend on each query."
  - 8.6 Formal and Verifiable Reasoning with Proof Assistants: "Lean, Coq, AlphaProof, and the marriage of LLM-driven proof search with formal verification."
- **Ordering**: KEEP. Concept -> models -> training -> usage -> evaluation -> formal frontier.
- **Stale refs**:
  - `index.html` line 36: "from Chapter 8" referring to *this same chapter*, recursive nonsense. Should say "from Chapter 8 (Modern LLM Landscape)" referring to *module-07*. As written it's incoherent.
  - `index.html` line 51: "Section 8.3" reference linking to *this same module's index*. Looks like restructure artifact where module-07 used to have a section 8.3 introducing reasoning. Drop the reference.
  - `index.html` line 83 prereq: "Chapter 08" labeled "Modern LLM Landscape" matches the dual-numbering scheme.
  - `section-8.1.html` line 63, 146: "Chapter 20.1" RLHF reference, old numbering. New is 20.1 in part-index for alignment.
  - `section-8.2.html` line 210, `section-8.3.html` line 38/42/298, `section-8.4.html` line 42/333, `section-8.5.html` line 333: omitted-line stale refs that need spot fixes.
- **Home fit / consolidation**: Section 8.6 (formal reasoning with proof assistants) is missing from the Chapter Overview body text, which only walks through 8.1 to 8.5. Add 8.6 to the overview.

### Chapter 9 (part-index: Chapter 10): Inference Optimization & Efficient Serving (`module-09-inference-optimization/`)

- **Title**: KEEP.
- **Description (big-picture)**: KEEP (line 69).
- **Section descriptions** (placeholders; 7 sections):
  - 9.1 Model Quantization: "INT8, INT4, GPTQ, AWQ, bitsandbytes, GGUF, and the quality-vs-memory tradeoff at every bit width."
  - 9.2 KV Cache & Memory Optimization: "PagedAttention, prefix caching, grouped-query attention, sliding window, and the techniques that turn a 70B model into a 24GB GPU citizen."
  - 9.3 Speculative Decoding: "Draft-and-verify decoding, Medusa, EAGLE, and the rejection-sampling math that breaks the sequential-token bottleneck."
  - 9.4 Serving Infrastructure: "vLLM, SGLang, TGI, TensorRT-LLM, continuous batching, request scheduling, and the production inference stack."
  - 9.5 Model Pruning & Sparsity: "Structured and unstructured pruning, 2:4 sparsity, magnitude pruning, and SparseGPT."
  - 9.6 Test-Time Compute & Reasoning Models: "Latency budgets, deferred decoding, and the inference-side considerations specific to reasoning models."
  - 9.7 GPU Kernel Programming for LLM Optimization: "Triton, CUDA basics, kernel fusion, and writing a custom attention kernel."
- **Ordering**: PROPOSE move 9.6 (Test-Time Compute / Reasoning) to be 9.4 or later than 9.7, since it leans on serving (9.4) and reasoning models (Ch 8). Current ordering (between Serving and Pruning) is awkward.
- **Stale refs**:
  - `index.html` line 30: agent reference to `module-26` is in Part 6, which uses non-zero-padded "Chapter 26" but might be renumbered in the new numbering. Verify.
  - `index.html` line 42: "TGI" and "SGLang" anchor-href targets `module-10-interpretability/section-10.6.html#12-2-...`. Q-numbered sub-section IDs (Q.2, Q.3) hint at a previous "Appendix Q" structure now folded into Tools chapter; clean up.
  - `index.html` line 47: "Chapter 06: Pretraining & Scaling Laws". Matches module numbering. Inconsistent with the in-part renaming.
  - `index.html` line 88 prereq: "Chapter 08 Modern LLM Landscape" reference.
  - `index.html` line 122 What's Next: "Chapter 10 (this chapter)" wording recursion; reads "This concludes Chapter 11" but the file labels itself Chapter 9. Pick one.
  - `index.html` line 133 What's Next: "Chapter 11 Interpretability" matches the dual-numbering.
  - `section-9.8.html` line 314: "Chapter 11: Inference Optimization" labels module-09 (this module) as Chapter 11, which conflicts with line 122 / part-index Chapter 10.
  - `section-9.8.html` line 314: "Chapter 13: LLM APIs" reference matches new numbering.
  - `section-9.8.html` line 327: "Chapter 20" alignment reference.
- **Home fit / consolidation**: 9.6 (Test-Time Compute & Reasoning) duplicates concepts from Chapter 8 (Reasoning Models). Consider either trimming to a focused inference-side angle or moving the bulk of its content into Chapter 8.

### Chapter 10 (part-index: Chapter 11): Interpretability & Mechanistic Understanding (`module-10-interpretability/`)

- **Title**: KEEP "Interpretability & Mechanistic Understanding".
- **Description (big-picture)**: KEEP (line 68 reads well).
- **Section descriptions** (placeholders; the 4 "real" sections; sections 10.6-10.9 are the buried Tools-of-the-Trade content):
  - 10.1 Attention Analysis & Probing: "Visualizing attention patterns, induction heads, previous-token heads, and probing classifiers for what hidden states encode."
  - 10.2 Mechanistic Interpretability: "Circuits and features, logit lens, tuned lens, sparse autoencoders, and the program of reverse-engineering transformers."
  - 10.3 Practical Interpretability for Applications: "TransformerLens, nnsight, activation patching, ROME / MEMIT, and the toolbox for debugging real models."
  - 10.4 Explaining Transformers: "Integrated Gradients, SHAP, attention rollout, and feature-attribution methods for explaining individual predictions."
- **Ordering**: KEEP for the four real interpretability sections.
- **Stale refs**:
  - `index.html` line 52: "interpretability methods for softmax" appears to be auto-substitution corruption ("softmax" replacing "Transformer" or "language models"?). The text reads "the full spectrum of interpretability methods for softmax" which is nonsense. Real text should likely read "for LLMs" or "for transformers".
  - `index.html` line 68 big-picture: "Chapters 17 and 32". Ch 17 (synthetic data) and Ch 32 (probably RAG / safety in old numbering). 32 is stale.
  - `index.html` line 86 prereq: "Chapter 07" linking to module-07 (modern landscape), but module-07 is "Chapter 8" in part-index. Dual-numbering.
  - `index.html` line 87 prereq: "Chapter 05 Embeddings and Representation Learning" but Chapter 5 in new numbering is Decoding Strategies. This is a stale chapter title from old numbering; embeddings are now in Chapter 1 (module-01 sections 1.3, 1.4).
  - `index.html` line 121 next nav: "Chapter 12 Tools of the Trade" href to `../module-10-interpretability/index.html` (the same page). Broken link, should point to wherever Chapter 12 truly lives (currently sections 10.6-10.9 within this module). 
  - `section-10.1.html` line 208: "Chapter 20 ... Chapter 34 ... Chapter 37". 34 and 37 are old-numbering safety/eval chapters. Update.
  - `section-10.4.html` line 1069: stale ref needing fix.
  - `section-10.6.html` to `section-10.11.html`: these are the Tools-of-the-Trade content (Platforms, Libraries, Datasets, Models, External Reading). They live in module-10 but display "Chapter 12: Tools of the Trade: Models & Tokenizers" in breadcrumb and headers. Move into a real module-XX-tools-of-trade-models-tokenizers directory.
  - `section-10.6.html` line 28: "Section 16.2's job in Part III" reference matches new numbering.
  - `section-10.6.html` line 39: "Appendix L" reference for multi-GPU; verify Appendix L still exists in new structure.
  - `section-10.6.html` line 46: Table caption "Table 12.1.1" but section heading id is `10-5-4-...`.
  - `section-10.6.html` line 858: stale ref needing fix.
- **Home fit / consolidation**: Sections 10.6-10.9 (Tools content for Part 2) need to be relocated or the module renamed to reflect that it holds two chapters' worth of content (interpretability + tools). Currently this is the biggest structural artifact in Part 2.

---

## Part 3: Working with LLMs

### Part 3 index page (`part-3-working-with-llms/index.html`)

- **Title**: KEEP.
- **Description (big-picture)**: KEEP (line 45).
- **Part-overview claim line 40**: "Chapters: 4 (Chapters 13 through 16). Builds on the model knowledge from Part II..." OK.
- **Chapter 15 cross-part jump**: Section 15.5 "Structured Information Extraction" links to Part 7 module-34 (line 78). See finding F. Either inline the structured-extraction content into Chapter 15 or drop the card.
- **Chapter 16 inflation**: 8 sections, 3 of which (16.6-16.8) are anchor links.

### Chapter 11 (part-index: Chapter 13): Working with LLM APIs (`module-11-llm-apis/`)

- **Title**: KEEP.
- **Description (big-picture)**: KEEP (line 58).
- **Section descriptions** (placeholders):
  - 11.1 API Landscape & Architecture: "OpenAI Chat Completions, Anthropic Messages, Google Gemini, and the architectural patterns that make them interchangeable (and where they diverge)."
  - 11.2 Structured Output & Tool Integration: "JSON mode, response schemas, function calling, tool use, and the Instructor / Pydantic stack for reliable structured outputs."
  - 11.3 API Engineering Best Practices: "Retry, circuit breakers, semantic caching, cost tracking, observability, and the production patterns for running LLM calls at scale."
  - 11.4 Reasoning Models & Multimodal APIs: "Calling o1, o3, Claude 3.5+, and the multimodal endpoints, with budget control and streaming considerations."
- **Ordering**: KEEP. Landscape -> structured/tools -> reliability -> reasoning/multimodal.
- **Stale refs**:
  - `index.html` line 7-8 title: "Chapter 11" but part-index calls this Chapter 13.
  - `index.html` line 75 prereq: "Chapter 05 Decoding Strategies" matches part-index numbering.
  - `index.html` line 76 prereq: "Chapter 10" inference optimization matches.
  - `index.html` line 109 prev nav: "Chapter 12 Tools of the Trade" matches new numbering.
  - `index.html` line 111 next nav: "Chapter 14 Prompt Engineering" matches.

### Chapter 12 (part-index: Chapter 14): Prompt Engineering & Advanced Techniques (`module-12-prompt-engineering/`)

- **Title**: KEEP.
- **Description (big-picture)**: KEEP (line 67).
- **Section descriptions** (placeholders):
  - 12.1 Foundational Prompt Design: "Zero-shot, few-shot, role prompts, system prompts, and the templating patterns every prompt engineer reaches for first."
  - 12.2 Chain-of-Thought & Reasoning Techniques: "Chain-of-thought, self-consistency, tree-of-thought, ReAct, and the reasoning strategies that unlock harder problems."
  - 12.3 Advanced Prompt Patterns: "Self-reflection, meta-prompting, prompt chaining, and the multi-step patterns for complex pipelines."
  - 12.4 Prompt Security & Optimization: "Direct and indirect prompt injection, jailbreaks, defense strategies, structured-output enforcement, and prompt compression with LLMLingua."
  - 12.5 Automatic Prompt & Context Engineering: "DSPy, OPRO, automatic prompt optimization, MCP for dynamic context assembly, and the move from artisan prompts to programmatic ones."
- **Ordering**: KEEP. Foundations -> reasoning -> advanced patterns -> security -> automation is a clean ladder.
- **Stale refs**:
  - `index.html` line 24: breadcrumb "Chapter 12" while part-index labels Chapter 14.
  - `index.html` line 67 big-picture: "RAG systems (Chapter 23), agents (Chapter 26), and evaluation (Chapter 34)". 23/26/34 are old-numbering chapters. New numbering would put RAG in module-32 area but in the part-index for Part 7, agents probably remain Ch 26 in Part 6, and eval is in Part 9. Update or remove the parenthetical numbers.
  - `index.html` line 77: "Section 37.1" `module-47/section-47.1.html` reference for security; mixed up. Old numbering 37.1 was security, but link goes to module-47 (current number).
  - `index.html` line 78 LO: "Section 13.2" matches new numbering for `module-11/section-11.2.html`.

### Chapter 13 (part-index: Chapter 15): Hybrid ML+LLM Architectures & Decision Frameworks (`module-13-hybrid-ml-llm/`)

- **Title**: KEEP. Decision-frameworks framing is the right hook.
- **Description (big-picture)**: KEEP (line 67).
- **Section descriptions**:
  - 13.1 When to Use LLM vs. Classical ML: "Decision matrix for LLM vs classical ML vs rules-based, with cost, latency, and accuracy criteria." (Note: current desc has "Classical ML." prefix corruption; remove.)
  - 13.2 LLM as Feature Extractor: "Using LLM embeddings and outputs as features in classical ML pipelines, and when this beats end-to-end LLM."
  - 13.3 Hybrid Pipeline Patterns: "Triage with LLM escalation, confidence-based routing, ensemble voting, and cascading small-to-large model architectures."
  - 13.4 Cost-Performance Optimization at Scale: "Per-query cost modeling, TCO analysis, build-vs-buy economics, and quality-cost Pareto frontiers."
  - 13.5 Dataset Engineering for LLM Applications: "Extracting, normalizing, filtering, and formatting training data from production logs, the bridge to Part 4's fine-tuning chapters."
- **Ordering**: KEEP.
- **Stale refs**:
  - `index.html` line 53 chapter overview: "Chapter 23 on RAG" old numbering; should be Part 7 reference with new numbering.
  - `index.html` line 65 big-picture: "Part VIII" reference; ensure the new structure still has Part VIII or update.
  - `index.html` line 97 section-desc: "Classical ML. A comprehensive chapter from..." truncated cruft.
  - `index.html` line 122 What's Next: "Part IV: LLM Training and Adaptation" correct.
- **Home fit / consolidation**: Section 15.5 (Structured Information Extraction) in the Part 3 index points outside this chapter to module-34 in Part 7. Either inline that content here, drop the cross-link, or surface as a "See also" pointer.

### Chapter 14 (part-index: Chapter 16): Tools of the Trade: LLM API Stack (`module-14-tools-of-the-trade/`)

- **Title**: KEEP.
- **Description (big-picture)**: KEEP (line 31).
- **Section descriptions** (placeholders):
  - 14.1 Platforms: "OpenAI, Anthropic, Google AI, Azure OpenAI, AWS Bedrock, and the API-provider landscape for Part 3 workflows."
  - 14.2 Libraries & Frameworks: "openai-python, anthropic-sdk, litellm, LangChain, LlamaIndex, Pydantic AI, and the SDK layer for orchestrating calls."
  - 14.3 Datasets & Benchmarks: "Prompt-evaluation datasets, public chat logs, MT-Bench, AlpacaEval, and the benchmarks worth running against your API stack."
  - 14.4 Models: "GPT, Claude, Gemini, Llama, Mistral, and the model menus exposed through each provider in 2026."
  - 14.5 External Reading & Communities: "Books, blogs, Discords, and projects worth following for API-stack work."
- **Ordering**: KEEP for the first 5; subsections 16.6-16.8 are anchor links and should be demoted.
- **Stale refs**:
  - `index.html` line 22 breadcrumb: "Chapter 14".
  - `index.html` line 63 What Comes Next: "Chapter 21 closes Part IV" matches new numbering.
  - `index.html` line 66 prev nav: "Chapter 15 Hybrid ML+LLM" matches.
  - `index.html` line 68 next nav: "Chapter 17 Synthetic Data Generation" matches.
- **Home fit / consolidation**: Anchor-only sub-sections (16.6-16.8) should be demoted to sub-headings under 16.2.

---

## Part 4: LLM Training and Adaptation

### Part 4 index page (`part-4-training-adaptation/index.html`)

- **Title**: KEEP.
- **Description (big-picture)**: KEEP (line 45).
- **Part-overview claim line 40**: "Chapters: 5 (Chapters 17 through 21)." OK.
- **Chapter 19 (PEFT) scope creep**: Includes sections on Knowledge Distillation (19.5), Model Merging (19.6), Continual Learning (19.7). These are adjacent but distinct from PEFT. Either:
  - Rename Chapter 19 to "Parameter-Efficient Fine-Tuning, Distillation & Merging", or
  - Split into two chapters (Ch 19 PEFT, Ch 20 Distillation/Merging) and renumber subsequent chapters.
  
  Currently the chapter title says "PEFT" only but the contents go beyond.
- **Chapter 21 inflation**: 20 section cards, 15 of which (21.6-21.20) are anchor links. Worst offender of finding E.

### Chapter 15 (part-index: Chapter 17): Synthetic Data Generation & LLM Simulation (`module-15-synthetic-data/`)

- **Title**: KEEP.
- **Description (big-picture)**: KEEP (line 54), but fix the "Chapters 14 and 15" reference; should be "Chapters 18 and 19" (fine-tuning, PEFT) per the new numbering, or just "the fine-tuning workflows".
- **Section descriptions**:
  - 15.1 Principles of Synthetic Data Generation: "Why synthetic data, when it works, when it collapses, and the quality dimensions (diversity, accuracy, naturalness) that decide outcomes."
  - 15.2 LLM-Powered Data Generation Pipelines: "Self-Instruct, Evol-Instruct, Magpie, persona-driven generation, and the production pipelines that produce instruction-response pairs at scale."
  - 15.3 Quality Assurance & Data Curation: "LLM-as-judge scoring, exact / near-duplicate / semantic dedup, and the multi-dimensional filtering that catches bad synthetic data before it poisons training."
  - 15.4 LLM-Assisted Labeling & Active Learning: "Confidence-based routing, active learning, human-in-the-loop verification, Argilla, Label Studio."
  - 15.5 Weak Supervision & Programmatic Labeling: "Labeling functions, label aggregation, Snorkel, and the cost-quality tradeoffs of programmatic labeling."
  - 15.6 Synthetic Reasoning Data: "Chain-of-thought trace generation, RLVR-friendly data, verification and filtering of reasoning chains."
  - 15.7 Data Augmentation for LLMs: KEEP (already has non-placeholder description on line 116).
- **Ordering**: KEEP. Principles -> pipelines -> QA -> human-in-loop -> programmatic -> reasoning -> augmentation.
- **Stale refs**:
  - `index.html` line 30, 62: agent / red-teaming references with concept-link to old numbering.
  - `index.html` line 46: "RLHF, covered in Chapter 20" matches part-index.
  - `index.html` line 54 big-picture: "Chapters 14 and 15" should be "Chapters 18 and 19".
  - `index.html` line 60: "Chapter 14's prompt engineering" matches.
  - `index.html` line 62: `module-42-evaluation-foundations` reference matches.
  - `index.html` line 68: "Chapter 18 ... Chapter 20" matches.
  - `index.html` line 121 What's Next: "Chapter 18 Fine-Tuning Fundamentals" matches.
  - `index.html` line 124 prev: "Chapter 16 Tools of the Trade: LLM API Stack" matches.
  - `section-15.7.html` line 45: heading id "15-7-1-...", visible heading "17.8.1 Why Augment?". Dual-numbering.
  - `section-15.7.html` line 58: "Sections 13.1 through 13.3" with hrefs that go (a) to `section-15.1.html` (correct local link), and (b) to `module-42-evaluation-foundations/section-42.1.html` (way outside the chapter). Should both point inside the chapter.

### Chapter 16 (part-index: Chapter 18): Fine-Tuning Fundamentals (`module-16-fine-tuning-fundamentals/`)

- **Title**: KEEP.
- **Description (big-picture)**: KEEP (line 65).
- **Section descriptions**:
  - 16.1 When and Why to Fine-Tune: "Prompting vs RAG vs fine-tuning decision tree, including the 5-question framework that the rest of the book cross-references."
  - 16.2 Data Preparation for Fine-Tuning: "Alpaca, ShareGPT, ChatML formats, train/val/test splits, balancing strategies, and the data hygiene that decides fine-tuning outcomes."
  - 16.3 Supervised Fine-Tuning (SFT): "HuggingFace Trainer and TRL SFTTrainer, hyperparameter selection (LR, batch size, warmup, weight decay), and the standard SFT loop."
  - 16.4 Fine-Tuning via Provider APIs: "OpenAI fine-tuning API, Google Vertex AI, and the trade-offs of managed fine-tuning vs your own infrastructure."
  - 16.5 Fine-Tuning for Representation Learning: "Sentence embeddings, contrastive learning, hard-negative mining, and adapting encoders for retrieval."
  - 16.6 Fine-Tuning for Classification & Sequence Tasks: "Adding heads for single-label, multi-label, and token-level classification, plus sequence labeling and span extraction."
  - 16.7 Adapting Models for Long Text: "RoPE scaling, position interpolation, YaRN, and the context-extension techniques that turn 4K models into 128K models."
- **Ordering**: KEEP.
- **Stale refs**:
  - `index.html` line 24 breadcrumb: "Chapter 16" while part-index labels Chapter 18.
  - `index.html` line 82-86 prereq labels: "Chapter 02 Tokenization", "Chapter 04 Transformer", "Chapter 06 Pre-training", "Chapter 13 LLM APIs", "Chapter 17 Synthetic Data Generation". All match new numbering.
  - `index.html` line 129 What's Next: "Chapter 19 PEFT" matches.
  - `index.html` line 132 prev: "Chapter 17 Synthetic Data" matches.
- **Home fit / consolidation**: Good fit. 7 sections is on the long side for "Fundamentals" but each is distinct.

### Chapter 17 (part-index: Chapter 19): Parameter-Efficient Fine-Tuning (PEFT) (`module-17-peft/`)

- **Title**: PROPOSE rename to "Parameter-Efficient Fine-Tuning, Distillation & Merging" or split into two chapters. Current title "PEFT" doesn't capture 19.5 (Distillation), 19.6 (Merging), 19.7 (Continual Learning).
- **Description (big-picture)**: KEEP (line 68).
- **Section descriptions**:
  - 17.1 LoRA & QLoRA: "Low-rank decomposition, NF4 quantization, double quantization, paged optimizers, the dominant PEFT recipe in 2026."
  - 17.2 Advanced PEFT Methods: "DoRA, LoRA+, IA3, adapter modules, and the second-generation PEFT methods that close the gap with full fine-tuning."
  - 17.3 Training Platforms & Tools: "Axolotl, LLaMA-Factory, Unsloth, torchtune, TRL, and the high-level recipe layers that make fine-tuning a one-config-file job."
  - 17.4 Soft Prompts: Prompt Tuning, Prefix Tuning, and P-Tuning: "Learning continuous prompt vectors instead of training model weights, when soft prompts beat LoRA, and the original prompt-tuning literature."
  - 17.5 Knowledge Distillation for LLMs: "Teacher-student training, on-policy distillation, sequence-level vs response-level distillation, and the Phi / TinyLlama lineage."
  - 17.6 Model Merging & Composition: "SLERP, TIES, DARE, model souping, and the post-fine-tuning composition techniques that beat ensembles for free."
  - 17.7 Continual Learning & Domain Adaptation: "Replay, EWC, LoRA-stacking, and strategies for adapting models to a moving target without catastrophic forgetting."
- **Ordering**: PROPOSE move 17.4 (Soft Prompts) to after 17.2 (Advanced PEFT) since soft prompts are *also* PEFT. Currently 17.4 sits after 17.3 (tooling) which is awkward. Suggested order: 17.1 (LoRA) -> 17.2 (Advanced PEFT) -> 17.4 (Soft Prompts) -> 17.3 (Tooling) -> 17.5 (Distillation) -> 17.6 (Merging) -> 17.7 (Continual). Or split into PEFT-proper (1, 2, 4, 3) and Adjacent-Adaptation (5, 6, 7).
- **Stale refs**:
  - `index.html` line 24 breadcrumb: "Chapter 17".
  - `index.html` line 38: "LoRA, QLoRA, IA^3, prefix tuning, prompt tuning, and the merging tricks (DARE, TIES)" Good summary.
  - `index.html` line 44 canonical reference callout: "Section 18.1" reference matches part-index.
  - `index.html` line 84-86 prereq labels: "Chapter 18 Fine-Tuning", "Chapter 10 Inference Optimization", "Chapter 04 Transformer" match.
  - `index.html` line 87 prereq: "Hugging Face softmax library" – appears to be auto-substitution corruption (likely "Hugging Face Transformers library" originally).
  - `index.html` line 131 What's Next: "Chapter 20: Distillation and Model Merging" – wrong title. Chapter 20 in new numbering is Alignment (RLHF/DPO), not Distillation. Distillation is Section 19.6 within this very chapter. The What's Next text is stale from when distillation was its own chapter.
- **Home fit / consolidation**: Scope creep. See proposed title change or split above.

### Chapter 18 (part-index: Chapter 20): Alignment: RLHF, DPO & Preference Tuning (`module-18-alignment-rlhf-dpo/`)

- **Title**: KEEP.
- **Description (big-picture)**: KEEP (line 65), but fix "Chapter 37" reference (old numbering for safety).
- **Section descriptions**:
  - 18.1 RLHF: Teaching a Model What 'Helpful' Means: "The three-stage RLHF pipeline (SFT, reward model, PPO), Bradley-Terry preferences, KL constraints, and the recipe that powered ChatGPT."
  - 18.2 DPO & Modern Preference Optimization: "DPO, KTO, ORPO, SimPO, IPO, the post-PPO landscape of preference optimization."
  - 18.3 Constitutional AI & Self-Alignment: "Anthropic's RLAIF, constitution-based critique, self-rewarding LMs, and scalable principle-based alignment."
  - 18.4 RLVR: Reinforcement Learning with Verifiable Rewards: "Verifiable rewards for math and code, GRPO, and the DeepSeek-R1 reasoning recipe."
  - 18.5 Alignment Research Frontiers: "Scalable oversight, debate, weak-to-strong generalization, and the open research questions in 2026."
- **Ordering**: KEEP. RLHF -> DPO -> CAI -> RLVR -> frontiers is a clean historical and conceptual arc.
- **Stale refs**:
  - `index.html` line 24 breadcrumb: "Chapter 18".
  - `index.html` line 38 Looking Back: "Chapter 18" (fine-tuning) and "Chapter 19" (PEFT) references. Matches part-index.
  - `index.html` line 65 big-picture: "Chapter 37" – stale, should be the new safety chapter number (Part 10 module-47 area).
  - `index.html` line 83 prereq: "Chapter 18 Fine-tuning Foundations" matches.
  - `index.html` line 84 prereq: "Chapter 06 Pretraining & Scaling Laws (attention, decoder-only models)". The parenthetical is mostly correct but cribbed from a different chapter; pretraining isn't where you learn attention.
  - `index.html` line 85 prereq: "Chapter 07 Modern LLM Landscape (next-token prediction, loss functions)". Modern LLM Landscape doesn't teach next-token-prediction or loss functions. This prereq description is fabricated. Fix.
  - `index.html` line 112-116 / 119-123: Section 18.7 listed twice (once in main sections-list, once in a duplicate section-grid below). Drop the duplicate.
  - `index.html` line 127 What's Next: "Part V: Retrieval and Conversation with LLMs and Agents" linked to `part-7-retrieval-information-extraction-with-llms`. So Part 5 in the link text but Part 7 in the URL. Need to verify the part numbering; if the new structure renumbers parts, the link text should follow the new numbering.
  - `index.html` line 130 prev: "Chapter 19 PEFT" matches.
  - `index.html` line 132 next: "Chapter 21 Tools of the Trade" matches.
- **Home fit / consolidation**: Good fit.

### Chapter 19 (part-index: Chapter 21): Tools of the Trade: Training & Adaptation Stack (`module-19-tools-of-the-trade/`)

- **Title**: KEEP.
- **Description (big-picture)**: KEEP (line 35).
- **Section descriptions** (placeholders):
  - 19.1 Platforms: "Local GPU box, cloud rentals (RunPod, vast.ai, Lambda, Modal), managed training services, and the platform decision tree for Part-4 jobs."
  - 19.2 Libraries & Frameworks: "transformers, TRL, PEFT, accelerate, axolotl, LLaMA-Factory, Unsloth, torchtune, and the open-recipe ecosystem."
  - 19.3 Datasets & Benchmarks: "Alpaca, ShareGPT, FineWeb-Edu, UltraFeedback, and the preference / instruction datasets that drive Part-4 training."
  - 19.4 Models: "Llama 3.1, Mistral, Qwen3, Gemma2, Phi-4, and the open-weight base models worth fine-tuning."
  - 19.5 External Reading & Communities: "Papers, blogs, Discords, and projects worth following for training-stack work."
- **Ordering**: KEEP for the first 5; subsections 21.6-21.20 are anchor links and should be demoted.
- **Stale refs**:
  - `index.html` line 22 breadcrumb: "Chapter 19".
  - `index.html` line 41: "Appendix L" anchor reference, verify Appendix L still exists.
  - `index.html` line 73 What Comes Next: "Part V ... Chapter 25 closes Part V". Part V in old numbering is Retrieval (RAG). The link in the next-nav (line 78) points to module-31 (embeddings) in part-7, suggesting Part V text should be updated to whatever the new part name is. Currently the part has two names: "Part V: Retrieval and Conversation" in some places, "Part VII: Retrieval and Information Extraction" implied by the path.
  - `index.html` line 76 prev: "Chapter 20 Alignment" matches.
  - `index.html` line 78 next: "Chapter 22 Embeddings, Vector Databases & Semantic Search" matches new numbering for first chapter of Part 7.
- **Home fit / consolidation**: Anchor-only sub-sections 21.6-21.20 should be demoted to sub-headings.

---

## Aggregated Stale-Reference Index (file:line, finding, fix)

This list collects the discrete stale references called out above plus a few more found during the audit. It is not exhaustive; a global grep for `Chapter (1[3-9]|2[0-9]|3[0-9]|4[0-9]|5[0-9])` would surface additional cases.

| File | Line | Stale text | Fix |
| --- | --- | --- | --- |
| `part-1-llm-building-blocks/module-00-ml-pytorch-foundations/index.html` | 49 | `building AI agents (Chapter 26)` | Update to new agents chapter number, or drop the numeric tag and rely on the link. |
| `part-1-llm-building-blocks/module-00-ml-pytorch-foundations/index.html` | 59 | `explored in full in Chapter 20: Alignment` | Pick part-index (Ch 20) or module (Ch 18) and use consistently. |
| `part-1-llm-building-blocks/module-00-ml-pytorch-foundations/index.html` | 68 | `(Chapter 20)` | Same. |
| `part-1-llm-building-blocks/module-00-ml-pytorch-foundations/section-0.2.html` | 282 | `Chapter 31: Multimodal Models` linking to `module-20-audio-music-generation` | Module-20 is audio/music. Update Chapter label to new number or link to the correct multimodal chapter. |
| `part-1-llm-building-blocks/module-00-ml-pytorch-foundations/section-0.5.html` | 47 | "Section 20.1" in text, href to `module-18-alignment-rlhf-dpo/section-18.1.html` | Pick numbering. |
| `part-1-llm-building-blocks/module-00-ml-pytorch-foundations/section-0.5.html` | 374, 379, 451 | `Chapter 20` | Same. |
| `part-1-llm-building-blocks/module-01-foundations-nlp-text-representation/index.html` | 110 | `next` nav points to same module instead of `module-02-...` | Fix href. |
| `part-1-llm-building-blocks/module-01-foundations-nlp-text-representation/section-1.2.html` | 419 | `Chapter 23` RAG ref | New numbering. |
| `part-1-llm-building-blocks/module-01-foundations-nlp-text-representation/section-1.3.html` | 324-325 | `Chapter 22 ... Chapter 23` | New numbering. |
| `part-1-llm-building-blocks/module-01-foundations-nlp-text-representation/section-1.7.html` | 38, 132 | `Section 13.1 ... Chapter 14` | OK if part-index numbering is the chosen convention. |
| `part-1-llm-building-blocks/module-02-sequence-models-attention/index.html` | 33 | breadcrumb "Chapter 2" | Should be Chapter 3 (part-index). |
| `part-1-llm-building-blocks/module-02-sequence-models-attention/section-2.1.html` | 36 | breadcrumb "Chapter 2" | Same. |
| `part-1-llm-building-blocks/module-02-sequence-models-attention/section-2.1.html` | 47 | "Section 2.2" linked to `module-01/section-1.6.html` | Verify; module-01/section-1.6 IS Section 2.2 of Ch 2 (Tokenization) in part-index. Confusing. |
| `part-1-llm-building-blocks/module-02-sequence-models-attention/section-2.1.html` | 57 | id `2-1-1-...` vs visible "3.1.1" heading | Pick numbering. |
| `part-1-llm-building-blocks/module-02-sequence-models-attention/section-2.1.html` | 55 | Figure caption "Figure 3.1.1" | Consistent with new chapter numbering. |
| `part-1-llm-building-blocks/module-02-sequence-models-attention/section-2.1.html` | 59 | "Chapter 02" linked to module-01 | Module-01 is Chapter 1 in new numbering. |
| `part-1-llm-building-blocks/module-03-transformer-architecture/index.html` | 24 | breadcrumb "Chapter 3" | Should be Chapter 4 per part-index. |
| `part-1-llm-building-blocks/module-03-transformer-architecture/index.html` | 69 | `(Chapter 11: Interpretability)` | Correct in new numbering; double-check no module-10 prefix conflict. |
| `part-1-llm-building-blocks/module-03-transformer-architecture/section-3.1.html` | 51 | "Section 3.5" linked to module-02/section-2.3 | OK in new numbering but file says Section 2.3. Pick. |
| `part-1-llm-building-blocks/module-03-transformer-architecture/section-3.1.html` | 59 | "Section 3.5" | Same. |
| `part-1-llm-building-blocks/module-03-transformer-architecture/section-3.2.html` | 48 | "Chapter 18" fine-tuning ref | Matches new numbering. |
| `part-1-llm-building-blocks/module-03-transformer-architecture/section-3.5.html` | 51 | "Chapter 09 ... Section 10.1" | Mixed numbering; pick one. |
| `part-1-llm-building-blocks/module-03-transformer-architecture/section-3.6.html` | 51 | "Section 10.1" / "Section 7.4" | New numbering. |
| `part-1-llm-building-blocks/module-03-transformer-architecture/section-3.7.html` | 49, 59, 211 | "Section 14.2 ... Section 8.3" | Mixed. |
| `part-1-llm-building-blocks/module-04-decoding-text-generation/section-4.1.html` | 47 | "Section 4.1" (self-ref via module-03/section-3.1.html, the Transformer section) | Confusing self-reference loop; should reference module-03 Section 4.1 explicitly. |
| `part-1-llm-building-blocks/module-04-decoding-text-generation/section-4.2.html` | 93 | "Chapter 13 ... Chapter 20" with link to `module-17-peft/section-17.5.html` for distillation | Distillation is now Section 19.6, not Chapter 20. |
| `part-1-llm-building-blocks/module-05-tools-of-the-trade/index.html` | 8 | title "Chapter 5" | Part-index calls this Chapter 6. |
| `part-1-llm-building-blocks/module-05-tools-of-the-trade/index.html` | 73 | "Chapter 12 closes Part II" | OK, but Chapter 12 in part-2 is buried in module-10. |
| `part-1-llm-building-blocks/module-05-tools-of-the-trade/section-5.1.html` | 30, 32, 39, 51 | h2 IDs `5-1-X`, visible `6.1.X` | Pick. |
| `part-1-llm-building-blocks/module-05-tools-of-the-trade/section-5.1.html` | 55 | "Section 12.1" / `module-10-interpretability/section-10.6.html` | The target is correct for new numbering but is a buried-tools-content link. |
| `part-1-llm-building-blocks/module-05-tools-of-the-trade/section-5.1.html` | 377, 443 | "Chapter 50.2 (Vibe-Coding)" | Stale; Ch 50 doesn't exist. |
| `part-1-llm-building-blocks/module-05-tools-of-the-trade/section-5.2.html` | 43 | "Chapter 7" tokenizers linked to module-01 (Chapter 1 in new numbering) | Wrong chapter number AND wrong target. |
| `part-1-llm-building-blocks/module-05-tools-of-the-trade/section-5.2.html` | 547 | "Section 20.1" DPO | Stale. |
| `part-1-llm-building-blocks/module-05-tools-of-the-trade/section-5.2.html` | 1058 | "Section H.6 and Section 16.1" | Verify H.6. |
| `part-2-understanding-llms/index.html` | 65 | duplicate Section 8.3 cards in Chapter 8 | Drop the cross-chapter card. |
| `part-2-understanding-llms/index.html` | 109-122 | Chapter 12 inflation | Demote anchors. |
| `part-2-understanding-llms/module-06-pretraining-scaling-laws/index.html` | 67 | "Chapter 18 Fine-Tuning" | New numbering, OK. |
| `part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.2.html` | 168 | "Chapter 14" prompt eng | OK in new numbering. |
| `part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.9.html` | 280 | "Chapter 15: Hybrid ML and LLM Systems" labeled as the *next* chapter | Wrong; next chapter is module-07 (Chapter 8 in part-index). |
| `part-2-understanding-llms/module-07-modern-llm-landscape/index.html` | 38 | "Chapter 7" referring to pretraining | OK in part-index numbering (pretraining = Ch 7). |
| `part-2-understanding-llms/module-07-modern-llm-landscape/index.html` | 53-57 | Body text has two "Section 7.4" mentions | Renumber one to 7.4. |
| `part-2-understanding-llms/module-07-modern-llm-landscape/index.html` | 97 | Section card 7.3 points to `module-08` (different chapter's index) | Drop or convert to "See also". |
| `part-2-understanding-llms/module-07-modern-llm-landscape/section-7.1.html` | 50, 91 | Stale ChXX refs (omitted lines) | Spot-fix. |
| `part-2-understanding-llms/module-07-modern-llm-landscape/section-7.3.html` | 475 | "Chapter 15" hybrid | OK. |
| `part-2-understanding-llms/module-07-modern-llm-landscape/section-7.4.html` | 66, 334 | "Chapter 18" fine-tuning | OK. |
| `part-2-understanding-llms/module-08-reasoning-test-time-compute/index.html` | 36 | "from Chapter 8" referring to self (self-recursion) | Should be Chapter 8 (Modern LLM Landscape, module-07), not self. |
| `part-2-understanding-llms/module-08-reasoning-test-time-compute/index.html` | 51 | "Section 8.3" referring to module-07's old 8.3 (now removed) | Drop. |
| `part-2-understanding-llms/module-08-reasoning-test-time-compute/section-8.1.html` | 63, 146 | "Chapter 20.1" RLHF | OK in new numbering. |
| `part-2-understanding-llms/module-09-inference-optimization/index.html` | 30 | concept-link to `module-26-ai-agents` with title "Chapter 26" | Verify Ch 26 is still correct after renumbering. |
| `part-2-understanding-llms/module-09-inference-optimization/index.html` | 42 | Anchor refs to `module-10-interpretability/section-10.6.html#12-2-...` for TGI / SGLang | Buried tools content. |
| `part-2-understanding-llms/module-09-inference-optimization/section-9.7.html` | 230 | Stale ref (omitted line) | Spot-fix. |
| `part-2-understanding-llms/module-09-inference-optimization/section-9.8.html` | 314 | "Chapter 11: Inference Optimization & Efficient Serving" referring to self via index.html. Chapter 11 in new numbering is Interpretability, not Inference. Wrong chapter title. |
| `part-2-understanding-llms/module-09-inference-optimization/section-9.8.html` | 327 | "Chapter 20" alignment | OK. |
| `part-2-understanding-llms/module-10-interpretability/index.html` | 33 | image src has double prefix `../../part-2-understanding-llms/module-10-interpretability/images/chapter-opener.png` | Unnecessary prefix; should be `images/chapter-opener.png`. |
| `part-2-understanding-llms/module-10-interpretability/index.html` | 52 | "interpretability methods for softmax" | Corruption; should be "for LLMs" or "for transformers". |
| `part-2-understanding-llms/module-10-interpretability/index.html` | 68 | "Chapters 17 and 32" | Old numbering. |
| `part-2-understanding-llms/module-10-interpretability/index.html` | 87 | prereq labeled "Chapter 05 Embeddings and Representation Learning" but Ch 5 in new numbering is Decoding | Wrong title. |
| `part-2-understanding-llms/module-10-interpretability/index.html` | 121 | next nav href = same page | Broken link. |
| `part-2-understanding-llms/module-10-interpretability/section-10.1.html` | 208 | "Chapter 20 ... Chapter 34 ... Chapter 37" | Old numbering. |
| `part-2-understanding-llms/module-10-interpretability/section-10.4.html` | 1069 | Stale ref (omitted line) | Spot-fix. |
| `part-2-understanding-llms/module-10-interpretability/section-10.6.html` | 28 | "Section 16.2's job in Part III" | OK. |
| `part-2-understanding-llms/module-10-interpretability/section-10.6.html` | 39 | "Appendix L" | Verify. |
| `part-2-understanding-llms/module-10-interpretability/section-10.6.html` | 46 | "Table 12.1.1" but heading id `10-5-4-...` | Dual numbering. |
| `part-2-understanding-llms/module-10-interpretability/section-10.6.html` | 858 | Stale ref (omitted line) | Spot-fix. |
| `part-3-working-with-llms/index.html` | 78 | Section 15.5 card jumps to Part 7 | See finding F. |
| `part-3-working-with-llms/module-11-llm-apis/index.html` | 7-8 | title "Chapter 11" | Part-index Chapter 13. |
| `part-3-working-with-llms/module-12-prompt-engineering/index.html` | 24 | breadcrumb "Chapter 12" | Part-index 14. |
| `part-3-working-with-llms/module-12-prompt-engineering/index.html` | 67 | "(Chapter 23) ... (Chapter 26) ... (Chapter 34)" | Old numbering. |
| `part-3-working-with-llms/module-12-prompt-engineering/index.html` | 77 | "Section 37.1" linked to `module-47/section-47.1.html` | Stale text label, new-numbering target. |
| `part-3-working-with-llms/module-13-hybrid-ml-llm/index.html` | 53 | "Chapter 23 on RAG" | Old numbering. |
| `part-3-working-with-llms/module-13-hybrid-ml-llm/index.html` | 65 | "Part VIII" | Verify part numbering after restructure. |
| `part-3-working-with-llms/module-13-hybrid-ml-llm/index.html` | 97 | section-desc starts with "Classical ML. " corruption | Remove cruft. |
| `part-3-working-with-llms/module-14-tools-of-the-trade/index.html` | 22 | breadcrumb "Chapter 14" | Part-index 16. |
| `part-4-training-adaptation/index.html` | 78, 110-125 | Section 15.5 + Chapter 21 inflation | See findings F and E. |
| `part-4-training-adaptation/module-15-synthetic-data/index.html` | 54 | "Chapters 14 and 15" should be "Chapters 18 and 19" | New numbering. |
| `part-4-training-adaptation/module-15-synthetic-data/section-15.7.html` | 45, 60 | id `15-7-1-...` vs visible "17.8.1" | Dual numbering. |
| `part-4-training-adaptation/module-15-synthetic-data/section-15.7.html` | 58 | "Sections 13.1 through 13.3" hrefs split between local `section-15.1` and `module-42/section-42.1.html` | Both should point inside Ch 15. |
| `part-4-training-adaptation/module-16-fine-tuning-fundamentals/index.html` | 24 | breadcrumb "Chapter 16" | Part-index 18. |
| `part-4-training-adaptation/module-17-peft/index.html` | 24 | breadcrumb "Chapter 17" | Part-index 19. |
| `part-4-training-adaptation/module-17-peft/index.html` | 87 | "Hugging Face softmax library" | Substitution corruption; should be "Transformers". |
| `part-4-training-adaptation/module-17-peft/index.html` | 131 | What's Next says "Chapter 20: Distillation and Model Merging" but Ch 20 is Alignment | Stale; update. |
| `part-4-training-adaptation/module-18-alignment-rlhf-dpo/index.html` | 24 | breadcrumb "Chapter 18" | Part-index 20. |
| `part-4-training-adaptation/module-18-alignment-rlhf-dpo/index.html` | 65 | "Chapter 37" safety | Old numbering. |
| `part-4-training-adaptation/module-18-alignment-rlhf-dpo/index.html` | 84-85 | Prereq labels for Ch 06 / Ch 07 with descriptions cribbed from wrong chapters | Rewrite descriptions to match the actual chapter content. |
| `part-4-training-adaptation/module-18-alignment-rlhf-dpo/index.html` | 112-123 | Section 18.7 listed twice | Drop duplicate. |
| `part-4-training-adaptation/module-18-alignment-rlhf-dpo/index.html` | 127 | What's Next: "Part V" but link goes to Part 7 | Update part label. |
| `part-4-training-adaptation/module-19-tools-of-the-trade/index.html` | 22 | breadcrumb "Chapter 19" | Part-index 21. |
| `part-4-training-adaptation/module-19-tools-of-the-trade/index.html` | 73 | "Part V ... Chapter 25 closes Part V" | Verify part numbering. |

---

## Top-Priority Fixes

Ranked by impact:

1. **Pick a single chapter-numbering scheme and apply it everywhere.** This is the single biggest source of confusion. Either the part-index numbering (0, 1, 2, ..., 21) or the module numbering (00, 01, ..., 19). Every breadcrumb, `<title>`, heading, prereq label, cross-reference, figure caption, code-fragment number, and `What's Next` paragraph needs to follow that scheme.
2. **Replace the global "A comprehensive chapter..." section-desc placeholders.** Every section card on every chapter index. Per-section proposed text above.
3. **Demote the Tools-of-the-Trade anchor sub-sections.** Part 1 Ch 6 (18 -> 5), Part 2 Ch 12 (10 -> 5), Part 3 Ch 16 (8 -> 5), Part 4 Ch 21 (20 -> 5). The anchor-only sub-sections should appear as sub-headings under their parent section card, not as siblings.
4. **Relocate Part 2's Tools content out of `module-10-interpretability/`.** Create a real `module-XX-tools-models-tokenizers/` directory and move sections 10.6-10.9 in. Update all links.
5. **Fix the Chapter 8 duplicate-section-3 bug** in `part-2-understanding-llms/index.html`. Drop the "8.3 Reasoning Models" cross-chapter card; renumber Multilingual cleanly as 8.3.
6. **Fix the Chapter 19 (PEFT) scope.** Either rename to reflect Distillation / Merging / Continual Learning, or split into two chapters.
7. **Resolve the Chapter 2 (Tokenization) physical-file split.** Either give it its own `module-02-tokenization/` directory or accept the in-module-01 layout and update every reference accordingly.
8. **Fix the Module 0 ordering in Part 1 index.** Move Chapter 0 to the top of the chapter cards.
9. **Fix `section-6.9.html` line 280 What's Next** ("Chapter 15 Hybrid ML" should be "Chapter 8 Modern LLM Landscape" or whatever the actual next chapter is).
10. **Fix `section-10.4.html` line 1069**, `section-10.6.html` line 858, `section-9.7.html` line 230, and other omitted-line stale refs found by grep but not displayed in this audit.

---

End of report.
