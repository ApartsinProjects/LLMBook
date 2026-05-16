# Book-Wide Callout Opportunities Audit

Scope: every section, chapter-index, part-index, and appendix HTML page under `E:/Projects/BookBlogsHome/LLMBook/` (excluding `node_modules`, `KDP`, `templates`, `pagefind`, `temp_ebook`, `temp_epub`, `source_fix_backups`, `.book-update`, `.claude`, `tmp_whats_next`). Read-only audit, no HTML modified.

Callouts in the count include `<div class="callout ...">`, `<aside class="callout ...">`, and `<section class="callout ...">`. Non-callout structural blocks like `<div class="objectives">`, `<section class="bibliography">`, `<div class="whats-next">`, `<div class="overview">`, and `<div class="prereqs">` are NOT counted as callouts. Bibliography-style structures may already exist in some chapter indexes as `<section class="bibliography">` outside the callout system; recommendations to "add a `bibliography` callout" therefore mean wrap or convert these into the standard callout class so they render consistently and are surfaced as callouts.

## Summary

- **Files scanned**: 460
- **WELL-ENRICHED (4+ callouts, no suggestions)**: 268
- **Under-enriched with recommendations**: 180
- **TODO scaffolds (skipped, need authoring first)**: 12

## By callout type (suggested additions, aggregate across whole audit)

These are rough totals reflecting the per-file pattern recommendations below:

- `pathway` (Learning Objectives): ~75 (most chapter indexes and all part indexes use a plain `<div class="objectives">` or no objectives block; the standard `callout pathway` class is rarely used)
- `key-insight` (incl Mental Model): ~140 (almost every Tools-of-the-Trade section, most appendix sections, and several chapter indexes)
- `practical-example` (Real-World Scenario): ~80 (most Tools sections, most appendix sections, several non-Tools sections)
- `bibliography`: ~55 (most chapter indexes in Parts 1-10/12 lack a `bibliography` callout, plus several appendix indexes)
- `key-takeaway`: ~40 (every part index lacks a Key Takeaways closer; some chapter indexes and appendix indexes too)
- `self-check`: ~60 (most appendix sections, most Tools sections, several regular sections)
- `exercise`: ~25 (a number of appendix sections and Tools sections could use a hands-on micro-exercise)
- `research-frontier`: ~15 (Part 12 frontier chapters and a few Part 2/7/9 sections describing 2024-2026 results)
- `big-picture`: ~12 (some Tools section pages and appendix sections do not have a top-of-page orientation)
- `fun-note`: ~15 (a few appendix sections and chapter indexes feel dry, would benefit from a memorable hook)
- `looking-back`: ~10 (Parts 11/12 chapter indexes and some appendix indexes lack `looking-back`)
- `production-pattern`: ~10 (a few sections describing architecture patterns without an explicit callout)

## Patterns and grouped recommendations

Several large groups of files share the same structural gap. To stay within the 1500-line cap, those groups are summarised first; each individual file in those groups is then listed underneath with file-specific anchor language where it differs from the group default. Per-file unique recommendations follow.

### PATTERN A: Standard chapter-index pages (Parts I-X)

These chapter indexes have **2 callouts** already (typically `looking-back` + `big-picture`) plus a non-callout `<div class="objectives">`, `<div class="prereqs">`, `<div class="whats-next">`, and a `<section class="bibliography">`. The standard gap is:

- The bibliography section is rendered as `<section class="bibliography">`, not as a `callout bibliography` div. For consistency with the callout palette and the Kindle-safe styling, wrap the bibliography content in `<div class="callout bibliography"><div class="callout-title">Bibliography and Further Reading</div>...</div>` or convert the existing `<section class="bibliography">` so the `bibliography` callout class applies. Per the audit count this would already lift these files from 2 callouts to 3.
- The non-callout `<div class="objectives">` block can be reformatted into a `<div class="callout pathway"><div class="callout-title">Learning Objectives</div><ul>...</ul></div>`, which uses the standard CSS-styled pathway callout and makes the Learning Objectives visually consistent across the book. This lifts the file to 4 callouts (well-enriched).
- Optional: add a single `key-insight` titled "Mental Model" near the top (after `big-picture`, before the section list) that captures the recurring mental model the chapter is teaching. This lifts the file to 5 callouts.

### PATTERN B: Standard part-index pages (Parts I-XII)

Every part index has **1 callout** (the `big-picture` block describing the part's role in the book). The recurring gaps:

- After the chapter cards list, before `<div class="whats-next">`: add a `<div class="callout key-takeaway"><div class="callout-title">Key Takeaways</div><ul>...</ul></div>` with 3-5 bullets that summarise what readers should walk away from this part knowing. Anchor: "before the `whats-next` block at the bottom."
- After the `<h1>` and `<p class="chapter-subtitle">`, before the part-opener illustration: optionally add a `<div class="callout pathway"><div class="callout-title">Learning Objectives</div>...</div>` with 3-5 bullets enumerating the cross-chapter capabilities the reader will acquire by the end of this part.
- Optional: a `<div class="callout looking-back">` connecting back to the previous part (use "After Part N you can already do X; this part takes that further by Y"). Anchor: "at the very top of `<main>`, before the part-opener figure" (skip for Part I which has nothing to look back at).

### PATTERN C: "Tools of the Trade" chapter-index pages (Chapters 6, 12, 16, 21, 25, 30, 33, 36, 39, 50, 60, 65)

These chapter indexes already have **2 callouts** (`big-picture` + `library-shortcut`). The standard gaps:

- After `<h2>Sections in This Chapter</h2>` list and before `<div class="whats-next">`: add a `<div class="callout key-takeaway"><div class="callout-title">When to reach for what</div><ul>...</ul></div>` summarising the decision rule across the platform/library/dataset/model layers (one bullet per layer). This is the natural "summary heuristic" callout for a Tools chapter.
- Optional: a `<div class="callout fun-note">` after the epigraph with a memorable failure story or anecdote from the toolchain (every Tools chapter has at least one good "the bill was $12K because someone forgot pagination" story available, and these are highly engaging).
- Optional: convert the `<div class="whats-next">` block (which is structural prose, not a callout) into a `<div class="callout looking-back">` at the top, connecting back to the previous chapter; this is already the pattern for non-Tools chapter indexes.

### PATTERN D: "Tools of the Trade" section pages (sections X.1-X.5 inside Tools chapters)

Tools sections currently average **0-2 callouts**. The standard gaps:

- One `<div class="callout key-insight"><div class="callout-title">Mental Model</div>...</div>` near the top after the introductory paragraph. The mental-model headline should be the "if-then" heuristic for choosing among the listed tools (e.g., for a "Platforms" section, "If your task fits on a single T4 GPU, Colab is the default; if you need persistence or multi-GPU, move to Kaggle or Lightning Studios.").
- One `<div class="callout practical-example"><div class="callout-title">Real-World Scenario</div>...</div>` before the chapter-nav describing a concrete production use of the tool stack covered in this section. This wraps the "what you'd actually pick" narrative that most Tools sections already contain in prose.
- Optional: one `<div class="callout self-check"><div class="callout-title">Self-Check</div>...</div>` with 2 short questions before chapter-nav. Example: "Why is Colab a poor backup strategy?" / "Which framework should you reach for if a 24 GB GPU LoRA fine-tune is your constraint?"

### PATTERN E: Part-VII embodied-world-models sections 32.1-32.4, 32.7

These regular sections have **3 callouts** each (some combination of `key-insight`, `production-pattern`, `cross-ref`, `numeric-example`, `library-shortcut`, `warning`). To lift them to 4+:

- Add one `<div class="callout self-check">` before chapter-nav with 2 short questions checking the section's main concept. Example for 32.7: "Why do production multimodal systems pair contrastive embeddings with VLM reranking instead of using a VLM end-to-end?"
- Add one `<div class="callout bibliography">` at the bottom listing the 4-6 key papers/links the section already cites in prose (CLIP, SigLIP, BLIP-3, LLaVA, MMMU, etc.).

### PATTERN F: Appendix sections (most appendix HTML files)

Appendix sections currently average **1-3 callouts** (typically `key-insight` or `practical-example` or `note`). The standard gaps:

- Add one `<div class="callout self-check">` near the bottom (before chapter-nav) with 2 short questions checking section understanding. Appendices are reference material and self-check questions help readers verify they have retained the lookup material.
- Add one `<div class="callout practical-example">` if the section teaches a procedure but lacks a worked numeric example.
- Optional: a `<div class="callout exercise">` with 1 hands-on task (e.g., "Recreate the venv install for your own project and `pip freeze` it.").

---

## Per-file recommendations: Parts I-VI (LLM-foundations core)

### part-1-foundations/index.html (existing: 1 callout — `big-picture`)
- After paragraph 1 of `<div class="part-overview">` and before the `<div class="callout big-picture">` block: add a `<div class="callout pathway"><div class="callout-title">Learning Objectives</div>` listing 4-5 cross-chapter capabilities (e.g., "By the end of Part I you will be able to (1) write a forward-and-backward pass in PyTorch from memory, (2) explain why attention is O(N^2) and what FlashAttention does about it, (3) train a tokenizer on your own corpus, (4) build a 300-line decoder-only transformer.").
- Before `<div class="whats-next">` at the bottom: add a `<div class="callout key-takeaway"><div class="callout-title">Key Takeaways</div><ul>...</ul></div>` with 4-5 bullets summarising what foundations the reader now has.

### part-1-foundations/module-00-ml-pytorch-foundations/index.html (existing: 2 — `looking-back`, `big-picture`)
- Convert the existing `<div class="objectives">` block into a `<div class="callout pathway"><div class="callout-title">Learning Objectives</div>` (5 bullets, already drafted in the source).
- Convert the existing `<section class="bibliography">` at the bottom into a `<div class="callout bibliography">` so it renders as a styled bibliography callout.
- Optional: after `big-picture` and before `<h2>Sections</h2>`, add a `<div class="callout key-insight"><div class="callout-title">Mental Model</div>` with: "Every modern deep learning system is the same three loops: a forward pass that turns inputs into predictions, a loss that quantifies error, a backward pass that adjusts parameters. PyTorch's job is to make all three feel like ordinary Python."

### part-1-foundations/module-01-foundations-nlp-text-representation/index.html (existing: 2 — `looking-back`, `big-picture`)
- Apply PATTERN A: convert `<div class="objectives">` to `callout pathway`; convert the existing `<section class="bibliography">` to `callout bibliography`.
- Optional `key-insight` titled "Mental Model" after `big-picture`: "Every embedding method since Word2Vec is a different answer to the same question: given a word's context, what shared vector explains it. Bag-of-words throws away context, Word2Vec uses a 5-word window, BERT uses the entire sentence."

### part-1-foundations/module-02-tokenization-subword-models/index.html (existing: 2 — `looking-back`, `big-picture`)
- Apply PATTERN A as above.
- Optional `key-insight` "Mental Model": "Tokenization is a lossy compression problem. Larger vocabularies mean shorter sequences but more parameters in the embedding table; smaller vocabularies push the work to the model. BPE is the empirical sweet spot for most languages, but Unigram beats it for languages with rich morphology."

### part-1-foundations/module-03-sequence-models-attention/index.html (existing: 2 — `looking-back`, `big-picture`)
- Apply PATTERN A.
- Optional `key-insight` "Mental Model" after `big-picture`: "Attention is differentiable retrieval. The query is the request, the keys are the contents addresses, the values are what gets returned, the softmax is the soft argmax over relevance. Once you see attention as soft lookup, everything from KV caches to retrieval-augmented generation falls out as the same idea at different scales."

### part-1-foundations/module-04-transformer-architecture/index.html (existing: 2 — `looking-back`, `big-picture`)
- Apply PATTERN A: convert `<div class="objectives">` to `callout pathway`; convert the existing `<section class="bibliography">` (already present at lines 147-191) to a `<div class="callout bibliography">`.
- Strong recommendation: after `big-picture` and before `<div class="objectives">`, add a `<div class="callout key-insight"><div class="callout-title">Mental Model</div>` with: "Think of a transformer block as iterated attention plus MLP refinement. Each block takes the current representation, looks around at the other tokens, mixes information based on relevance, and then applies a position-wise nonlinearity. Stacked N times, this is the entire computation behind every modern LLM."

### part-1-foundations/module-05-decoding-text-generation/index.html (existing: 2 — `looking-back`, `big-picture`)
- Apply PATTERN A.
- Optional `key-insight` "Mental Model": "Decoding is the budgeting layer between the model's probability distribution and the user's experience. Greedy picks the highest-probability token at every step; sampling explores the long tail; nucleus and top-k clip the bottom of the distribution before sampling. Almost every quality complaint about an LLM is upstream of decoding, not downstream of it."

### part-1-foundations/module-06-tools-of-the-trade/index.html (existing: 2 — `big-picture`, `library-shortcut`)
- Apply PATTERN C: add a `<div class="callout key-takeaway"><div class="callout-title">When to reach for what</div>` summarising platform / library / dataset / model layer decisions in 4-5 bullets. Anchor: after `<div class="section-card-list">`, before `<div class="whats-next">`.
- Optional `<div class="callout looking-back">` at the very top (currently the chapter has none): "Part I just walked through the math, the linguistics, and the architecture. This chapter pulls all of that into the toolbox you actually open every day: PyTorch, NumPy, the canonical datasets, BERT-base and GPT-2."

### part-1-foundations/module-06-tools-of-the-trade/section-6.1.html (existing: 2 — `tip`, `warning`)
- Apply PATTERN D: after the introductory paragraph and before `<h2>6.1.1 Hardware tiers...</h2>`, add a `<div class="callout key-insight"><div class="callout-title">Mental Model</div>` with: "Platform choice is a three-axis problem: where the code runs (CPU/GPU/cloud), how state persists (ephemeral notebook vs persistent disk), and what the marginal cost of a mistake is. For Part I, the right default is whichever combination puts the smallest possible price tag on the lessons you have not learned yet."
- Before `<nav class="chapter-nav">`: add a `<div class="callout practical-example"><div class="callout-title">Real-World Scenario</div>` describing a concrete day-one workflow (e.g., "First read-through of Chapter 4 on Colab T4 free tier; second read-through on local RTX 4090 with the same code; only graduate to AWS when you are training the Part IV PEFT examples on a 70B model.")

### part-1-foundations/module-06-tools-of-the-trade/section-6.2.html (existing: 2 — `key-insight`, `practical-example`)
- Add one `<div class="callout self-check"><div class="callout-title">Self-Check</div>` before chapter-nav: "When would you reach for SciPy over NumPy?" / "Why does `tokenizers` ship as a Rust library rather than pure Python?"
- Add one `<div class="callout warning">` if a common-mistake hook fits the prose (e.g., "scikit-learn's MLP defaults are decade-old; do not benchmark a 2026 transformer against an MLPClassifier with default hyperparameters and conclude transformers are better.")

### part-1-foundations/module-06-tools-of-the-trade/section-6.3.html (existing: 2 — `warning`, `tip`)
- Apply PATTERN D: add a `<div class="callout key-insight"><div class="callout-title">Mental Model</div>` near the top with: "Benchmarks are not a model leaderboard; they are a contract about which capability is being measured. MNIST tests visual perception, SQuAD tests extractive QA, GLUE tests sentence-level classification. Picking the right benchmark is more important than beating an existing one on the wrong one."
- Add a `<div class="callout practical-example"><div class="callout-title">Real-World Scenario</div>` before chapter-nav describing a specific dataset choice (e.g., "When fine-tuning a tokenizer for a legal corpus, start by running fertility on SQuAD vs your own corpus to see how badly the off-the-shelf tokenizer fragments your domain terms.").

### part-1-foundations/module-06-tools-of-the-trade/section-6.4.html (existing: 2 — `key-insight`, `practical-example`)
- Add one `<div class="callout self-check">` before chapter-nav with 2 questions: "Why does the book use BERT-base and GPT-2 for the foundations exercises rather than larger 2026 models?" / "Which checkpoint would you reach for first when teaching the concept of MLM vs causal LM?"
- Add one `<div class="callout warning">` if there is a common-mistake hook (e.g., "Avoid loading GPT-2-XL on a 6 GB GPU even in fp16; the activation memory at sequence length 1024 alone will OOM during the backward pass.").

### part-1-foundations/module-06-tools-of-the-trade/section-6.5.html (existing: 2 — `tip`, `key-insight`)
- Add one `<div class="callout practical-example"><div class="callout-title">Real-World Scenario</div>` before chapter-nav describing how the listed reading sources fit a weekly habit (e.g., "Sunday-evening 30 minutes: read the new arXiv links on Andrej Karpathy's Twitter and one Hugging Face blog post.").
- Add one `<div class="callout bibliography"><div class="callout-title">Bibliography</div>` at the very bottom collecting the external links the section cites (or convert the existing list into the bibliography callout class).

### part-2-understanding-llms/index.html (existing: 1 — `big-picture`)
- Apply PATTERN B: add a `<div class="callout pathway"><div class="callout-title">Learning Objectives</div>` near the top and a `<div class="callout key-takeaway">` near the bottom (before `whats-next`). Pathway bullets should cover: scaling laws fluency, ability to read a model card and predict cost/latency, knowing the difference between pretraining and post-training.

### part-2-understanding-llms/module-07-pretraining-scaling-laws/index.html (existing: 2 — `looking-back`, `big-picture`)
- Apply PATTERN A: convert objectives to `callout pathway`; convert bibliography section to `callout bibliography`.
- Optional `key-insight` "Mental Model" after `big-picture`: "Pretraining is the act of buying a probability distribution over text with a credit card. Scaling laws tell you what the credit card buys per dollar. Everything after pretraining is the art of bending that distribution toward your task without paying for a new distribution."

### part-2-understanding-llms/module-07-pretraining-scaling-laws/section-7.9.html (existing: 1 — `note`)
- This is a hands-on **lab** with code blocks but only one note callout. Add at the top, after the existing `<aside class="callout note">`: `<div class="callout pathway"><div class="callout-title">Lab Objectives</div>` listing the four items from `<div class="lab-skills">` (which is currently a plain div). Alternatively, convert the existing `<div class="lab-skills">` into the `callout pathway` class.
- After Step 4 (training loop) and before the HuggingFace Trainer mini-section: add a `<div class="callout key-insight"><div class="callout-title">Key Insight</div>` with: "Notice how the loss curve does not move for the first 100 steps. Pretraining loss curves are 90% bookkeeping; the real learning happens after the warmup."
- Before chapter-nav: add a `<div class="callout self-check">` with 2 questions: "Why is weight tying (`self.lm_head.weight = self.token_emb.weight`) standard in language models?" / "What would happen if you removed gradient clipping from the training loop?"

### part-2-understanding-llms/module-08-modern-llm-landscape/index.html (existing: 2 — `looking-back`, `big-picture`)
- Apply PATTERN A.
- Optional `key-insight` "Mental Model": "The 2026 model landscape is a 2x2: open-weight vs closed, and dense vs MoE. The other axes (multimodal, reasoning, agent-tuned) are now table stakes for any frontier release. Picking a model is choosing which quadrant your product can tolerate."
- Optional `research-frontier` callout: "Frontier as of 2026: the gap between open-weight (DeepSeek-V3, Qwen-3, Llama-4) and closed (GPT-5, Claude Sonnet 4.6, Gemini 2.5 Ultra) has narrowed to 5-10 points on most benchmarks, with closed models still dominant on long-horizon agentic tasks."

### part-2-understanding-llms/module-09-reasoning-test-time-compute/index.html (existing: 2 — `looking-back`, `big-picture`)
- Apply PATTERN A.
- Optional `research-frontier` callout summarising o1, R1, and 2026 reasoning-model results: "The shift from 'better pretraining' to 'better inference compute' was the dominant 2024-2026 capability story; OpenAI's o-series, DeepSeek-R1, and Anthropic extended thinking made it standard."

### part-2-understanding-llms/module-10-inference-optimization/index.html (existing: 2 — `looking-back`, `big-picture`)
- Apply PATTERN A.
- Optional `key-insight` "Mental Model": "Inference is a memory-bandwidth problem dressed up as a compute problem. KV-cache management, batching, speculative decoding, and prefix caching all share one goal: keep the GPU's HBM2 saturated rather than its compute units."

### part-2-understanding-llms/module-11-interpretability/index.html (existing: 2 — `looking-back`, `big-picture`)
- Apply PATTERN A.
- Optional `research-frontier` callout summarising Anthropic's 2024-2026 attribution-graph and circuits-at-scale work.

### part-2-understanding-llms/module-12-tools-of-the-trade/index.html (existing: 2 — `big-picture`, `library-shortcut`)
- Apply PATTERN C: add a `<div class="callout key-takeaway"><div class="callout-title">When to reach for what</div>` summarising tokenizer-library, pretraining-corpus, and model-loading choices.
- Add `<div class="callout looking-back">` at the top: "Part II turned the math of Part I into models with names: GPT, BERT, Llama. Chapter 12 collects the libraries, datasets, and benchmarks you reach for when working with those models."

### part-2-understanding-llms/module-12-tools-of-the-trade/section-12.1.html (existing: 2 — `warning`, `tip`)
- Apply PATTERN D: add `key-insight` Mental Model near top; add `practical-example` Real-World Scenario before chapter-nav; optional `self-check` with 2 questions.

### part-2-understanding-llms/module-12-tools-of-the-trade/section-12.2.html (existing: 2 — `key-insight`, `practical-example`)
- Add one `<div class="callout self-check">` before chapter-nav with 2 questions about library trade-offs.
- Add one `<div class="callout bibliography">` if the section cites external resources.

### part-2-understanding-llms/module-12-tools-of-the-trade/section-12.3.html (existing: 2 — `warning`, `tip`)
- Apply PATTERN D: add `key-insight` Mental Model and `practical-example`.

### part-2-understanding-llms/module-12-tools-of-the-trade/section-12.4.html (existing: 2 — `key-insight`, `practical-example`)
- Add `<div class="callout self-check">` and optionally `<div class="callout warning">` for common pitfalls.

### part-2-understanding-llms/module-12-tools-of-the-trade/section-12.5.html (existing: 1 — `tip`)
- Apply PATTERN D: add `key-insight` Mental Model near top and `practical-example` Real-World Scenario before chapter-nav.

### part-3-working-with-llms/index.html (existing: 1 — `big-picture`)
- Apply PATTERN B: add `pathway` Learning Objectives near top, `key-takeaway` Key Takeaways near bottom.

### part-3-working-with-llms/module-13-llm-apis/index.html (existing: 2 — `looking-back`, `big-picture`)
- Apply PATTERN A.
- Optional `key-insight` Mental Model: "Working with an LLM API is the same as working with a database: latency, throughput, error handling, retries, and cost are first-class concerns. Treat 'the model returned tokens' as an SQL response, and the production patterns from Part X follow naturally."

### part-3-working-with-llms/module-14-prompt-engineering/index.html (existing: 2 — `looking-back`, `big-picture`)
- Apply PATTERN A.
- Optional `key-insight` Mental Model: "A prompt is a program written in a probabilistic language. Like any program, it has a signature (the system message), arguments (the user message), local variables (few-shot examples), and a return type (the structured output schema). The discipline of prompt engineering is treating those parts as real software."

### part-3-working-with-llms/module-15-hybrid-ml-llm/index.html (existing: 2 — `looking-back`, `big-picture`)
- Apply PATTERN A.
- Optional `practical-example` callout describing a hybrid ML+LLM production architecture (e.g., classical classifier as front-line filter, LLM for explanation).

### part-3-working-with-llms/module-16-tools-of-the-trade/index.html — **SKIP: TODO scaffold (12 callouts pattern only after authoring).**

### part-3-working-with-llms/module-16-tools-of-the-trade/section-16.1.html — **SKIP: TODO scaffold.**

### part-3-working-with-llms/module-16-tools-of-the-trade/section-16.2.html (existing: 2 — `key-insight`, `practical-example`)
- Add `<div class="callout self-check">` with 2 questions before chapter-nav.
- Optionally add `<div class="callout warning">` if there is a common-mistake hook.

### part-3-working-with-llms/module-16-tools-of-the-trade/section-16.3.html (existing: 2 — `warning`, `tip`)
- Apply PATTERN D: add `key-insight` Mental Model near top; add `practical-example` Real-World Scenario before chapter-nav.

### part-3-working-with-llms/module-16-tools-of-the-trade/section-16.4.html (existing: 2 — `key-insight`, `practical-example`)
- Add `<div class="callout self-check">` and optionally `<div class="callout warning">`.

### part-3-working-with-llms/module-16-tools-of-the-trade/section-16.5.html (existing: 1 — `tip`)
- Apply PATTERN D.

### part-4-training-adapting/index.html (existing: 1 — `big-picture`)
- Apply PATTERN B.

### part-4-training-adapting/module-17-synthetic-data/index.html (existing: 2 — `looking-back`, `big-picture`)
- Apply PATTERN A.
- Optional `research-frontier` callout summarising 2024-2026 synthetic-data state-of-the-art (Phi-4's "synthetic data is the new pretraining data" thesis, persona-prompted generation).

### part-4-training-adapting/module-18-fine-tuning-fundamentals/index.html (existing: 2 — `looking-back`, `big-picture`)
- Apply PATTERN A.
- Optional `key-insight` Mental Model: "Fine-tuning is debt repayment. Pretraining took on debt by ingesting noisy internet text; fine-tuning pays it down by aligning the distribution to your task. The amount of paydown you can afford is proportional to your data quality and your compute budget."

### part-4-training-adapting/module-19-peft/index.html (existing: 3 — `looking-back`, `cross-ref`, `big-picture`)
- One more callout needed to reach 4. Add `<div class="callout key-insight"><div class="callout-title">Mental Model</div>` after `big-picture`: "PEFT is a budget constraint problem: full fine-tuning needs O(parameters) gradient memory; LoRA needs O(rank * (d_in + d_out)); QLoRA pushes both weights and activations to 4-bit. The right method is the one that fits your GPU with a 25% margin for activations."
- Convert objectives div to `callout pathway` and bibliography section to `callout bibliography` as in PATTERN A.

### part-4-training-adapting/module-20-alignment-rlhf-dpo/index.html (existing: 2 — `looking-back`, `big-picture`)
- Apply PATTERN A.
- Optional `key-insight` Mental Model: "Alignment is fine-tuning with a preference dataset instead of a label dataset. RLHF treats the reward model as ground truth; DPO collapses the two stages into one loss; KTO simplifies further. All four (PPO, DPO, KTO, GRPO) are variants of 'make the model prefer what humans prefer' with different statistical machinery."

### part-4-training-adapting/module-21-tools-of-the-trade/index.html (existing: 2 — `big-picture`, `library-shortcut`)
- Apply PATTERN C.

### part-4-training-adapting/module-21-tools-of-the-trade/section-21.1.html (existing: 1 — `warning`)
- Apply PATTERN D: add `key-insight` Mental Model and `practical-example` Real-World Scenario.

### part-4-training-adapting/module-21-tools-of-the-trade/section-21.2.html (existing: 0)
- Apply PATTERN D in full: add `key-insight` Mental Model near top with the three-layer (engine / algorithm / recipe) decision rule (this is exactly the prose the section opens with); add `practical-example` describing a concrete fine-tune choice (e.g., "For a 7B Qwen LoRA on a single 24 GB GPU, Unsloth is the fastest start; for multi-GPU SFT with a config you want to share, axolotl is the right answer."); add `<div class="callout self-check">` with 2 questions: "Why is TRL's SFTTrainer preferred to writing a raw HuggingFace Trainer loop for RLHF?" / "When should you reach for OpenRLHF or verl instead of TRL?"

### part-4-training-adapting/module-21-tools-of-the-trade/section-21.3.html (existing: 1 — `warning`)
- Apply PATTERN D.

### part-4-training-adapting/module-21-tools-of-the-trade/section-21.4.html (existing: 1 — `key-insight`)
- Add `<div class="callout practical-example">` and `<div class="callout self-check">` before chapter-nav.

### part-4-training-adapting/module-21-tools-of-the-trade/section-21.5.html (existing: 1 — `tip`)
- Apply PATTERN D.

### part-5-retrieval-conversation/index.html (existing: 1 — `big-picture`)
- Apply PATTERN B.

### part-5-retrieval-conversation/module-22-embeddings-vector-db/index.html (existing: 2 — `looking-back`, `big-picture`)
- Apply PATTERN A.
- Optional `key-insight` Mental Model: "An embedding is a coordinate in a learned semantic space. Vector databases are spatial indexes over those coordinates. Retrieval is approximate nearest-neighbor search. Once you internalise this, the rest of RAG is just plumbing."

### part-5-retrieval-conversation/module-23-rag/index.html (existing: 2 — `looking-back`, `big-picture`)
- Apply PATTERN A.
- Optional `key-insight` Mental Model: "RAG is the answer to context-window economics: instead of putting everything the model needs in the prompt, you put a query that retrieves the relevant slice from a vector index. The retrieval layer becomes the model's working memory, the vector database becomes its long-term memory."

### part-5-retrieval-conversation/module-24-conversational-ai/index.html (existing: 2 — `looking-back`, `big-picture`)
- Apply PATTERN A.
- Optional `practical-example` callout describing a concrete conversational architecture (intent classifier + RAG + tone-control LLM).

### part-5-retrieval-conversation/module-25-tools-of-the-trade/index.html (existing: 2 — `big-picture`, `library-shortcut`)
- Apply PATTERN C.

### part-5-retrieval-conversation/module-25-tools-of-the-trade/section-25.1.html (existing: 1 — `note`)
- Apply PATTERN D: add `key-insight` Mental Model near top and `practical-example` Real-World Scenario before chapter-nav.

### part-5-retrieval-conversation/module-25-tools-of-the-trade/section-25.2.html (existing: 1 — `tip`)
- Apply PATTERN D.

### part-5-retrieval-conversation/module-25-tools-of-the-trade/section-25.3.html (existing: 1 — `note`)
- Apply PATTERN D.

### part-5-retrieval-conversation/module-25-tools-of-the-trade/section-25.4.html (existing: 1 — `key-insight`)
- Add `<div class="callout practical-example">` Real-World Scenario and `<div class="callout self-check">` with 2 questions before chapter-nav.

### part-5-retrieval-conversation/module-25-tools-of-the-trade/section-25.5.html (existing: 1 — `tip`)
- Apply PATTERN D.

### part-6-agentic-ai/index.html (existing: 1 — `big-picture`)
- Apply PATTERN B.

### part-6-agentic-ai/module-26-ai-agents/index.html (existing: 2 — `looking-back`, `big-picture`)
- Apply PATTERN A.
- Optional `key-insight` Mental Model: "An agent is a loop: observe, think, act, observe again. The 'observe' step pulls from the environment, 'think' is an LLM call, 'act' invokes a tool. Agent design is choosing how big each step is and how many you tolerate before declaring failure."

### part-6-agentic-ai/module-27-tool-use-protocols/index.html (existing: 2 — `looking-back`, `big-picture`)
- Apply PATTERN A.
- Optional `practical-example` callout: "MCP servers are the 2025-2026 standard interface for letting an LLM call external tools. Claude Desktop and the Anthropic API converged on it; Cursor and other agent surfaces adopted it. If you are designing a new tool, MCP is the protocol to target."

### part-6-agentic-ai/module-28-multi-agent-systems/index.html (existing: 2 — `looking-back`, `big-picture`)
- Apply PATTERN A.
- Optional `warning` callout: "Multi-agent systems are usually the wrong abstraction. Most 'multi-agent' designs are a single agent with multiple tools. Reach for true multi-agent only when independent agents must hold private state, negotiate, or vote."

### part-6-agentic-ai/module-29-specialized-agents/index.html (existing: 2 — `looking-back`, `big-picture`)
- Apply PATTERN A.
- Optional `practical-example` callout describing one named specialized agent (SWE-agent, Aider, Claude Code) with a concrete capability that comes from specialization.

### part-6-agentic-ai/module-30-tools-of-the-trade/index.html (existing: 2 — `big-picture`, `library-shortcut`)
- Apply PATTERN C.

### part-6-agentic-ai/module-30-tools-of-the-trade/section-30.1.html (existing: 1 — `note`)
- Apply PATTERN D.

### part-6-agentic-ai/module-30-tools-of-the-trade/section-30.2.html (existing: 1 — `key-insight`)
- Add `<div class="callout practical-example">` and `<div class="callout self-check">`.

### part-6-agentic-ai/module-30-tools-of-the-trade/section-30.3.html (existing: 1 — `warning`)
- Apply PATTERN D.

### part-6-agentic-ai/module-30-tools-of-the-trade/section-30.4.html (existing: 1 — `key-insight`)
- Add `<div class="callout practical-example">` and `<div class="callout self-check">`.

### part-6-agentic-ai/module-30-tools-of-the-trade/section-30.5.html (existing: 1 — `tip`)
- Apply PATTERN D.

---

## Per-file recommendations: Parts VII-XII

### part-7-multimodal-generation/index.html (existing: 2 — `big-picture`, `key-insight`)
- Apply PATTERN B: add `pathway` Learning Objectives near top and `key-takeaway` Key Takeaways near bottom. The existing `key-insight` is on multimodal alignment, which is a strong mental-model; keep it and add the pathway/takeaway pair to lift the file to 4 callouts.

### part-7-multimodal-generation/module-31-multimodal/index.html (existing: 2 — `looking-back`, `big-picture`)
- Apply PATTERN A.
- Optional `practical-example`: a named multimodal product (Gemini Live, GPT-4o vision, Claude with vision) and what it ships under the hood.

### part-7-multimodal-generation/module-32-embodied-world-models/section-32.1.html (existing: 3 — `key-insight`, `production-pattern`, `cross-ref`)
- Apply PATTERN E: add `<div class="callout self-check">` (2 questions) and `<div class="callout bibliography">` before chapter-nav. The section already cites several papers in prose; gather them into the bibliography callout.

### part-7-multimodal-generation/module-32-embodied-world-models/section-32.2.html (existing: 3 — `key-insight`, `warning`, `cross-ref`)
- Apply PATTERN E.

### part-7-multimodal-generation/module-32-embodied-world-models/section-32.3.html (existing: 3 — `key-insight`, `numeric-example`, `library-shortcut`)
- Apply PATTERN E.

### part-7-multimodal-generation/module-32-embodied-world-models/section-32.4.html — **SKIP: TODO scaffold (only 85 words).**

### part-7-multimodal-generation/module-32-embodied-world-models/section-32.7.html (existing: 3 — `big-picture`, `key-insight`, `tip`)
- Apply PATTERN E: add `<div class="callout self-check">` with 2 questions ("Why do production multimodal systems pair contrastive embeddings with VLM reranking instead of using a VLM end-to-end?", "What is the saturation problem in multimodal benchmarks?") and `<div class="callout bibliography">` listing CLIP, SigLIP, BLIP-3, LLaVA, MMMU papers cited in the prose.

### part-7-multimodal-generation/module-32-embodied-world-models/section-32.8.html — **SKIP: TODO scaffold (only 83 words).**

### part-7-multimodal-generation/module-33-tools-of-the-trade/index.html (existing: 2 — `big-picture`, `library-shortcut`)
- Apply PATTERN C.

### part-7-multimodal-generation/module-33-tools-of-the-trade/section-33.1.html (existing: 1 — `note`)
- Apply PATTERN D.

### part-7-multimodal-generation/module-33-tools-of-the-trade/section-33.2.html (existing: 0)
- Apply PATTERN D in full: `key-insight` Mental Model near top, `practical-example` Real-World Scenario before chapter-nav, `<div class="callout self-check">` with 2 questions.

### part-7-multimodal-generation/module-33-tools-of-the-trade/section-33.3.html (existing: 1 — `warning`)
- Apply PATTERN D.

### part-7-multimodal-generation/module-33-tools-of-the-trade/section-33.4.html (existing: 1 — `note`)
- Apply PATTERN D.

### part-7-multimodal-generation/module-33-tools-of-the-trade/section-33.5.html (existing: 0)
- Apply PATTERN D in full.

### part-8-evaluation-production/index.html (existing: 1 — `big-picture`)
- Apply PATTERN B.

### part-8-evaluation-production/module-34-evaluation-observability/index.html (existing: 2 — `looking-back`, `big-picture`)
- Apply PATTERN A.
- Optional `key-insight` Mental Model: "Evaluation is the slowest-feedback step in the LLM stack. A pretraining loss tells you in seconds whether the math runs; a downstream benchmark tells you in hours whether the model learned; an LLM-as-judge eval tells you in days whether the model is useful. Production observability is what closes that gap."

### part-8-evaluation-production/module-35-production-engineering/index.html (existing: 2 — `looking-back`, `big-picture`)
- Apply PATTERN A.
- Optional `practical-example` callout describing one production architecture (e.g., the request-router + model-fallback + audit-log pattern that all of Anthropic/OpenAI ship behind their APIs).

### part-8-evaluation-production/module-36-tools-of-the-trade/index.html (existing: 2 — `big-picture`, `library-shortcut`)
- Apply PATTERN C.

### part-8-evaluation-production/module-36-tools-of-the-trade/section-36.1.html (existing: 0)
- Apply PATTERN D in full.

### part-8-evaluation-production/module-36-tools-of-the-trade/section-36.2.html (existing: 0)
- Apply PATTERN D in full.

### part-8-evaluation-production/module-36-tools-of-the-trade/section-36.3.html (existing: 1 — `warning`)
- Apply PATTERN D.

### part-8-evaluation-production/module-36-tools-of-the-trade/section-36.4.html (existing: 1 — `key-insight`)
- Add `<div class="callout practical-example">` and `<div class="callout self-check">`.

### part-8-evaluation-production/module-36-tools-of-the-trade/section-36.5.html (existing: 1 — `tip`)
- Apply PATTERN D.

### part-9-safety-security-ethics/index.html (existing: 1 — `big-picture`)
- Apply PATTERN B.

### part-9-safety-security-ethics/module-37-safety-ethics-regulation/index.html (existing: 2 — `looking-back`, `big-picture`)
- Apply PATTERN A.
- Optional `research-frontier` callout summarising 2024-2026 regulatory state (EU AI Act timeline, US state-level laws, Anthropic's RSP, OpenAI's PF).

### part-9-safety-security-ethics/module-38-agent-safety-security/index.html (existing: 1 — `big-picture`)
- One callout only; add 3 more. After `<div class="overview">` and before `<h2>Sections in This Chapter</h2>`: add a `<div class="callout key-insight"><div class="callout-title">Mental Model</div>` with: "Agent security is web security plus prompt injection. Every web-security primitive (input validation, sandboxing, capability minimization, audit logging) still applies; prompt injection adds a new vector that classical web security never modelled, because it weaponizes the model's own helpfulness."
- Add a `<div class="callout pathway"><div class="callout-title">Learning Objectives</div>` listing 4-5 capabilities (write a threat model, implement defense-in-depth, choose a sandbox technology, run an agentic security benchmark, audit a dependency supply chain).
- At the bottom before `<nav class="chapter-nav">`: add a `<div class="callout bibliography">` listing the key references (Anthropic Constitutional AI, the OWASP LLM Top 10, AgentDojo, CYBERSECEVAL, ASB, IFEval, SafeAgentBench).

### part-9-safety-security-ethics/module-39-tools-of-the-trade/index.html (existing: 2 — `big-picture`, `library-shortcut`)
- Apply PATTERN C.

### part-9-safety-security-ethics/module-39-tools-of-the-trade/section-39.1.html (existing: 0)
- Apply PATTERN D in full.

### part-9-safety-security-ethics/module-39-tools-of-the-trade/section-39.2.html (existing: 0)
- Apply PATTERN D in full.

### part-9-safety-security-ethics/module-39-tools-of-the-trade/section-39.3.html (existing: 1 — `warning`)
- Apply PATTERN D.

### part-9-safety-security-ethics/module-39-tools-of-the-trade/section-39.4.html (existing: 1 — `note`)
- Apply PATTERN D.

### part-9-safety-security-ethics/module-39-tools-of-the-trade/section-39.5.html (existing: 1 — `tip`)
- Apply PATTERN D.

### part-10-idea-to-product/index.html (existing: 1 — `big-picture`)
- Apply PATTERN B.

### part-10-idea-to-product/module-40-ideation/index.html — **SKIP: TODO scaffold (137w).**
### part-10-idea-to-product/module-41-product-management/index.html — **SKIP: TODO scaffold (136w).**
### part-10-idea-to-product/module-42-strategy-prioritization/index.html — **SKIP: TODO scaffold (150w).**
### part-10-idea-to-product/module-43-vibe-coding/index.html — **SKIP: TODO scaffold (136w).**
### part-10-idea-to-product/module-44-mvp/index.html — **SKIP: TODO scaffold (135w).**

### part-10-idea-to-product/module-42-strategy-prioritization/section-42.1.html (existing: 3 — `key-insight`, `practical-example`, `warning`)
- Add one `<div class="callout self-check">` with 2 questions before chapter-nav to lift to 4.

### part-10-idea-to-product/module-42-strategy-prioritization/section-42.2.html (existing: 3 — `key-insight`, `warning`, `practical-example`)
- Add one `<div class="callout self-check">` before chapter-nav.

### part-10-idea-to-product/module-45-prototype-to-production/index.html (existing: 2 — `looking-back`, `big-picture`)
- Apply PATTERN A.
- Optional `practical-example` callout describing a concrete prototype-to-production handoff (e.g., the Cursor/Sourcegraph 2024-2025 case studies of how research demos became revenue-generating products).

### part-10-idea-to-product/module-46-compute-planning/index.html — **SKIP: TODO scaffold (147w).**
### part-10-idea-to-product/module-47-scaling-economics/index.html — **SKIP: TODO scaffold (150w).**
### part-10-idea-to-product/module-49-post-launch-monitoring/index.html — **SKIP: TODO scaffold (133w).**

### part-10-idea-to-product/module-46-compute-planning/section-46.1.html (existing: 3 — `key-insight`, `warning`, `tip`)
- Add one `<div class="callout self-check">` before chapter-nav.

### part-10-idea-to-product/module-46-compute-planning/section-46.2.html (existing: 3 — `key-insight`, `practical-example`, `warning`)
- Add one `<div class="callout self-check">` before chapter-nav.

### part-10-idea-to-product/module-47-scaling-economics/section-47.1.html (existing: 3 — `key-insight`, `warning`, `practical-example`)
- Add one `<div class="callout self-check">` before chapter-nav.

### part-10-idea-to-product/module-47-scaling-economics/section-47.2.html (existing: 3 — `key-insight`, `warning`, `practical-example`)
- Add one `<div class="callout self-check">` before chapter-nav.

### part-10-idea-to-product/module-48-shipping-deploying/index.html (existing: 2 — `looking-back`, `big-picture`)
- Apply PATTERN A.
- Optional `production-pattern` callout describing the canonical 2026 LLM-deployment topology (model server + router + cache + budget guard + monitor).

### part-10-idea-to-product/module-50-tools-of-the-trade/index.html (existing: 2 — `big-picture`, `library-shortcut`)
- Apply PATTERN C.

### part-10-idea-to-product/module-50-tools-of-the-trade/section-50.1.html (existing: 0)
- Apply PATTERN D in full.

### part-10-idea-to-product/module-50-tools-of-the-trade/section-50.2.html (existing: 0)
- Apply PATTERN D in full.

### part-10-idea-to-product/module-50-tools-of-the-trade/section-50.3.html (existing: 0)
- Apply PATTERN D in full.

### part-10-idea-to-product/module-50-tools-of-the-trade/section-50.4.html (existing: 0)
- Apply PATTERN D in full.

### part-10-idea-to-product/module-50-tools-of-the-trade/section-50.5.html (existing: 0)
- Apply PATTERN D in full.

### part-11-applications-across-industries/index.html (existing: 1 — `big-picture`)
- Apply PATTERN B.

### part-11-applications-across-industries/module-58-creative-industries/index.html (existing: 3 — `big-picture`, `practical-example`, `bibliography`)
- Add a `<div class="callout looking-back">` at the very top of `<main>`, before `big-picture`. The chapter currently has no `looking-back`. Use: "Chapter 57 closed the manufacturing arc with adoption case studies; Chapter 58 zooms into the most public-facing application surface for generative AI: the creative industries."
- Optional `key-insight` Mental Model about the new "AI floor / human ceiling" dynamic.

### part-11-applications-across-industries/module-59-recommendation-search/index.html (existing: 3 — `big-picture`, `practical-example`, `bibliography`)
- Add a `<div class="callout looking-back">` at the top.
- Optional `key-insight` Mental Model: "Recommendation and search have converged on a single architecture: a dual-encoder retriever followed by a cross-encoder reranker, with LLM-based explainers riding on top. The same template powers Pinterest visual search, Spotify track recommendations, and modern e-commerce discovery."

### part-11-applications-across-industries/module-60-tools-of-the-trade/index.html (existing: 2 — `big-picture`, `library-shortcut`)
- Apply PATTERN C.

### part-11-applications-across-industries/module-60-tools-of-the-trade/section-60.1.html (existing: 1 — `note`)
- Apply PATTERN D.

### part-11-applications-across-industries/module-60-tools-of-the-trade/section-60.2.html (existing: 0)
- Apply PATTERN D in full.

### part-11-applications-across-industries/module-60-tools-of-the-trade/section-60.3.html (existing: 0)
- Apply PATTERN D in full.

### part-11-applications-across-industries/module-60-tools-of-the-trade/section-60.4.html (existing: 1 — `key-insight`)
- Add `<div class="callout practical-example">` and `<div class="callout self-check">`.

### part-11-applications-across-industries/module-60-tools-of-the-trade/section-60.5.html (existing: 0)
- Apply PATTERN D in full.

### part-12-frontiers/index.html (existing: 1 — `big-picture`)
- Apply PATTERN B.
- Strong recommendation: `<div class="callout research-frontier"><div class="callout-title">Research Frontier</div>` summarising what makes this part different (the content is fast-moving and dates faster than the rest of the book; the 2026 snapshot should be treated as a reference for the open questions, not the final answers).

### part-12-frontiers/module-61-frontier-architectures/index.html (existing: 2 — `looking-back`, `big-picture`)
- Apply PATTERN A.
- Optional `research-frontier` callout listing the open architectural questions (MoE scaling, hybrid attention, latent reasoning, test-time compute).

### part-12-frontiers/module-62-frontier-theory/index.html (existing: 2 — `big-picture`, `key-insight`)
- Apply PATTERN A.
- Add a `<div class="callout looking-back">` at the very top (the chapter has none).
- Apply PATTERN A conversions: `objectives` to `pathway`; bibliography section to `bibliography` callout.

### part-12-frontiers/module-63-frontier-systems-hardware/index.html (existing: 2 — `big-picture`, `library-shortcut`)
- Apply PATTERN A: convert `objectives` to `pathway`; convert bibliography to `bibliography` callout; add a `<div class="callout looking-back">` at the top.

### part-12-frontiers/module-63-frontier-systems-hardware/section-63.1.html (existing: 2 — `key-insight`, `warning`)
- Add `<div class="callout practical-example">` Real-World Scenario and `<div class="callout self-check">` (2 questions) before chapter-nav.

### part-12-frontiers/module-63-frontier-systems-hardware/section-63.2.html (existing: 3 — `key-insight`, `practical-example`, `warning`)
- Add one `<div class="callout self-check">` before chapter-nav.

### part-12-frontiers/module-63-frontier-systems-hardware/section-63.3.html (existing: 3 — `key-insight`, `practical-example`, `tip`)
- Add one `<div class="callout self-check">` before chapter-nav.

### part-12-frontiers/module-63-frontier-systems-hardware/section-63.4.html (existing: 2 — `key-insight`, `warning`)
- Add `<div class="callout practical-example">` and `<div class="callout self-check">`.

### part-12-frontiers/module-63-frontier-systems-hardware/section-63.5.html (existing: 3 — `key-insight`, `practical-example`, `warning`)
- Add one `<div class="callout self-check">` before chapter-nav.

### part-12-frontiers/module-64-agi-trajectories/index.html (existing: 2 — `big-picture`, `library-shortcut`)
- Apply PATTERN A: convert `objectives` to `pathway`; convert bibliography to `bibliography` callout; add `<div class="callout looking-back">` at the top.

### part-12-frontiers/module-64-agi-trajectories/section-64.1.html (existing: 3 — `key-insight`, `warning`, `tip`)
- Add one `<div class="callout self-check">` before chapter-nav.

### part-12-frontiers/module-64-agi-trajectories/section-64.2.html (existing: 3 — `key-insight`, `warning`, `practical-example`)
- Add one `<div class="callout self-check">` before chapter-nav.

### part-12-frontiers/module-64-agi-trajectories/section-64.3.html (existing: 3 — `key-insight`, `warning`, `tip`)
- Add one `<div class="callout self-check">` before chapter-nav.

### part-12-frontiers/module-64-agi-trajectories/section-64.4.html (existing: 3 — `key-insight`, `warning`, `practical-example`)
- Add one `<div class="callout self-check">` before chapter-nav.

### part-12-frontiers/module-64-agi-trajectories/section-64.5.html — **SKIP: TODO scaffold (76w).**

### part-12-frontiers/module-65-tools-of-the-trade/index.html (existing: 2 — `big-picture`, `library-shortcut`)
- Apply PATTERN C.

### part-12-frontiers/module-65-tools-of-the-trade/section-65.1.html (existing: 0)
- Apply PATTERN D in full.

### part-12-frontiers/module-65-tools-of-the-trade/section-65.2.html (existing: 0)
- Apply PATTERN D in full.

### part-12-frontiers/module-65-tools-of-the-trade/section-65.3.html (existing: 1 — `note`)
- Apply PATTERN D.

### part-12-frontiers/module-65-tools-of-the-trade/section-65.4.html (existing: 1 — `key-insight`)
- Add `<div class="callout practical-example">` and `<div class="callout self-check">`.

### part-12-frontiers/module-65-tools-of-the-trade/section-65.5.html (existing: 1 — `tip`)
- Apply PATTERN D.

---

## Appendix recommendations

Appendix indexes and sections follow the appendix patterns (PATTERN F). The 39 under-enriched appendix files are listed below with their current callouts and the matching pattern suggestions.

### appendices/appendix-a-mathematical-foundations/index.html (existing: 3 — `big-picture`, `note`, `practical-example`)
- Apply PATTERN F: add one `<div class="callout self-check">` near the bottom (before the section list) with 2 questions like "Why does attention scale by sqrt(d_k)?" / "What is the role of cross-entropy in language modeling loss?". This lifts the file to 4.

### appendices/appendix-a-mathematical-foundations/section-a.1.html (existing: 2 — `key-insight`, `note`)
- Add `<div class="callout practical-example">` showing a concrete matrix-multiply on a 4x4 example.
- Add `<div class="callout self-check">` with 2 questions.

### appendices/appendix-a-mathematical-foundations/section-a.2.html (existing: 1 — `practical-example`)
- Add `<div class="callout key-insight"><div class="callout-title">Mental Model</div>` summarising "probability distributions as histograms vs densities."
- Add `<div class="callout self-check">` with 2 questions.
- Add `<div class="callout warning">` about common pitfalls (e.g., "max-likelihood estimates of small-sample variances are biased").

### appendices/appendix-a-mathematical-foundations/section-a.3.html (existing: 1 — `key-insight`)
- Add `<div class="callout practical-example">` showing a backprop trace by hand on a tiny network.
- Add `<div class="callout self-check">` with 2 questions.
- Add `<div class="callout warning">` about numerical-stability tricks (log-sum-exp, gradient clipping).

### appendices/appendix-a-mathematical-foundations/section-a.4.html (existing: 2 — `key-insight`, `fun-note`)
- Add `<div class="callout practical-example">` computing entropy/cross-entropy on a concrete 4-class distribution.
- Add `<div class="callout self-check">` with 2 questions.

### appendices/appendix-a-mathematical-foundations/section-a.5.html (existing: 1 — `big-picture`)
- Add `<div class="callout key-insight"><div class="callout-title">Mental Model</div>` for "how the four pieces connect."
- Add `<div class="callout practical-example">` walking through the connections in a small attention computation.
- Add `<div class="callout self-check">` with 2 questions.

### appendices/appendix-a-mathematical-foundations/section-a.6.html (existing: 3 — `note`, `key-insight`, `note`)
- Add one `<div class="callout self-check">` to lift to 4.

### appendices/appendix-b-ml-essentials/index.html (existing: 3 — `big-picture`, `note`, `practical-example`)
- Add one `<div class="callout self-check">` near the bottom.

### appendices/appendix-b-ml-essentials/section-b.1.html (existing: 2 — `note`, `key-insight`)
- Add `<div class="callout practical-example">` and `<div class="callout self-check">`.

### appendices/appendix-b-ml-essentials/section-b.2.html (existing: 2 — `note`, `note`)
- Add `<div class="callout key-insight"><div class="callout-title">Mental Model</div>` and `<div class="callout self-check">`.

### appendices/appendix-b-ml-essentials/section-b.3.html (existing: 2 — `note`, `warning`)
- Add `<div class="callout key-insight"><div class="callout-title">Mental Model</div>` and `<div class="callout self-check">`.

### appendices/appendix-c-huggingface-ecosystem/index.html (existing: WELL-ENRICHED in v2 audit) — no action.

### appendices/appendix-e-orchestration-frameworks/section-e.1.html (existing: 3 — `big-picture`, `key-insight`, `note`)
- Add one `<div class="callout practical-example">` showing an orchestration recipe and `<div class="callout self-check">` to lift to 5.

### appendices/appendix-f-agent-frameworks/index.html (existing: 3 — `big-picture`, `library-shortcut`, `tip`)
- Add one `<div class="callout self-check">` near the bottom.

### appendices/appendix-f-agent-frameworks/section-f.1.html (existing: 3 — `big-picture`, `key-insight`, `note`)
- Add `<div class="callout practical-example">` and `<div class="callout self-check">`.

### appendices/appendix-g-problem-solution-key/index.html (existing: 1 — `key-insight`)
- This is a long reference (2025w) of problem solutions. Add:
  - `<div class="callout big-picture">` at the top describing how to use the answer key (read after attempting, not before).
  - `<div class="callout practical-example">` showing one worked solution at full detail as a template for using the key.
  - `<div class="callout warning">` about pedagogy: "Reading the solution before attempting the problem deletes the learning signal. Attempt for at least 20 minutes before consulting."

### appendices/appendix-h-python-for-llm/index.html (existing: 3 — `big-picture`, `note`, `practical-example`)
- Add one `<div class="callout self-check">` near the bottom.

### appendices/appendix-h-python-for-llm/section-h.2.html (existing: 1 — `key-insight`)
- Add `<div class="callout practical-example">` showing a complete venv-to-pip-freeze workflow.
- Add `<div class="callout warning">` about CUDA/pip-vs-conda gotchas.
- Add `<div class="callout self-check">` with 2 questions ("Why is `pip freeze > requirements.txt` insufficient for true reproducibility?" / "When should you reach for conda over venv?").

### appendices/appendix-h-python-for-llm/section-h.3.html (existing: 1 — `warning`)
- Add `<div class="callout key-insight"><div class="callout-title">Mental Model</div>`, `<div class="callout practical-example">`, `<div class="callout self-check">`.

### appendices/appendix-h-python-for-llm/section-h.4.html (existing: 1 — `fun-note`)
- Add `<div class="callout key-insight"><div class="callout-title">Mental Model</div>`, `<div class="callout practical-example">`, `<div class="callout self-check">`.

### appendices/appendix-i-environment-setup/index.html (existing: 3 — `big-picture`, `note`, `practical-example`)
- Add one `<div class="callout self-check">` near the bottom.

### appendices/appendix-i-environment-setup/section-i.1.html (existing: 2 — `key-insight`, `note`)
- Add `<div class="callout practical-example">` showing a concrete machine setup and `<div class="callout self-check">`.

### appendices/appendix-i-environment-setup/section-i.2.html (existing: 2 — `note`, `warning`)
- Add `<div class="callout key-insight"><div class="callout-title">Mental Model</div>` and `<div class="callout self-check">`.

### appendices/appendix-i-environment-setup/section-i.3.html (existing: 3 — `cross-ref`, `warning`, `note`)
- Add one `<div class="callout self-check">` and one `<div class="callout practical-example">`.

### appendices/appendix-i-environment-setup/section-i.4.html (existing: 1 — `practical-example`)
- Add `<div class="callout key-insight"><div class="callout-title">Mental Model</div>`, `<div class="callout warning">`, `<div class="callout self-check">`.

### appendices/appendix-i-environment-setup/section-i.5.html (existing: 1 — `key-insight`)
- Add `<div class="callout practical-example">`, `<div class="callout warning">`, `<div class="callout self-check">`.

### appendices/appendix-i-environment-setup/section-i.6.html (existing: 1 — `fun-note`)
- Add `<div class="callout key-insight"><div class="callout-title">Mental Model</div>`, `<div class="callout practical-example">`, `<div class="callout self-check">`.

### appendices/appendix-i-environment-setup/section-i.8.html (existing: 1 — `fun-note`)
- Add `<div class="callout key-insight"><div class="callout-title">Mental Model</div>`, `<div class="callout practical-example">`, `<div class="callout self-check">`.

### appendices/appendix-j-git-collaboration/index.html (existing: 3 — `big-picture`, `note`, `practical-example`)
- Add one `<div class="callout self-check">` near the bottom.

### appendices/appendix-j-git-collaboration/section-j.1.html (existing: 1 — `warning`)
- Add `<div class="callout key-insight"><div class="callout-title">Mental Model</div>`, `<div class="callout practical-example">`, `<div class="callout self-check">`.

### appendices/appendix-j-git-collaboration/section-j.2.html (existing: 1 — `key-insight`)
- Add `<div class="callout practical-example">`, `<div class="callout warning">`, `<div class="callout self-check">`.

### appendices/appendix-j-git-collaboration/section-j.3.html (existing: 3 — `cross-ref`, `key-insight`, `note`)
- Add one `<div class="callout practical-example">` and one `<div class="callout self-check">`.

### appendices/appendix-j-git-collaboration/section-j.4.html (existing: 2 — `fun-note`, `big-picture`)
- Add `<div class="callout key-insight"><div class="callout-title">Mental Model</div>` and `<div class="callout practical-example">`.

### appendices/appendix-l-inference-serving/index.html (existing: 3 — `big-picture`, `note`, `practical-example`)
- Add one `<div class="callout self-check">` near the bottom.

### appendices/appendix-m-distributed-ml/index.html (existing: 3 — `big-picture`, `note`, `practical-example`)
- Add one `<div class="callout self-check">` near the bottom.

### appendices/appendix-o-course-syllabi/index.html (existing: 1 — `big-picture`)
- This is a long reference (1975w) of course syllabi. Add:
  - `<div class="callout practical-example"><div class="callout-title">Real-World Scenario</div>` showing how a specific instructor used the book in a 14-week semester.
  - `<div class="callout key-insight"><div class="callout-title">Mental Model</div>` summarising "the 4-track decision" (full-semester / quarter / bootcamp / self-study).
  - `<div class="callout self-check">` with 2 questions for instructors planning a syllabus.

### appendices/appendix-p-reading-pathways/index.html (existing: 2 — `big-picture`, `key-insight`)
- Add `<div class="callout practical-example"><div class="callout-title">Real-World Scenario</div>` describing one named reader's pathway through the book ("a 2026 mid-level ML engineer moving from PyTorch to LLM agents").
- Add `<div class="callout self-check">` with 2 questions about pathway selection.

### appendices/appendix-q-intermediate-projects/index.html (existing: 0)
- This is a project rubric file with 0 callouts. Add:
  - `<div class="callout big-picture"><div class="callout-title">Big Picture</div>` at the top of `<main>`: "The 60-minute chapter labs test single concepts; the capstone tests integration; these three projects fill the 1-2 week middle gap that determines whether someone graduates from 'I read the book' to 'I can ship an LLM product'."
  - `<div class="callout key-insight"><div class="callout-title">Pedagogical Principle</div>` near the top: "An intermediate project is not a lab plus more time; it is the smallest unit of work that forces the reader to combine concepts from two different parts of the book."
  - `<div class="callout exercise"><div class="callout-title">Exercise: Intermediate Project 1</div>` wrapping the tokenizer comparison memo prose so the project starts as a callout block, not just an `<h3>`. Similar `exercise` callouts can wrap the other two projects.
  - `<div class="callout self-check">` with 2 questions for instructors evaluating completed projects.

### appendices/appendix-r-capstone-project/index.html (existing: 0)
- This is a three-track capstone rubric with 0 callouts. Add:
  - `<div class="callout big-picture">` at the top of `<main>`: "The capstone is the integrating assessment that distinguishes a reader from a practitioner. The three tracks differ in compute requirements but share one rubric."
  - `<div class="callout key-insight"><div class="callout-title">Mental Model</div>`: "A capstone is graded on the five dimensions in the rubric, not on the elegance of the solution. The B+ project with honest limitations beats the A- project with hidden failures."
  - `<div class="callout warning"><div class="callout-title">Grading pitfall</div>` wrapping the existing "limitations dimension is where students most predictably underperform" sentence at the bottom.
  - `<div class="callout practical-example"><div class="callout-title">Real-World Scenario</div>` describing a named capstone success (e.g., "Student X's domain-adapted RAG over biomedical PDFs that became a published preprint").

### appendices/appendix-s-war-stories/index.html (existing: 0)
- This is a five-war-story discussion page with 0 callouts. Add:
  - `<div class="callout big-picture">` at the top of `<main>`: "Safety, evaluation, and ROI conversations work better when grounded in named, public failures. These five incidents from 2023-2024 are the canonical opening case studies for the corresponding chapters."
  - Convert each of the five `<h3>War story N: ...</h3>` blocks into a `<div class="callout postmortem"><div class="callout-title">War Story: ...</div>...</div>`. The `postmortem` callout class already exists in the book (14 uses elsewhere). This converts five `<h3>` headings into 5 callouts and lifts the file from 0 to 5 callouts in one stroke.
  - Add a `<div class="callout key-takeaway"><div class="callout-title">Cross-cutting lessons</div>` at the bottom listing 3-5 patterns that appear in multiple war stories (liability of chatbot statements, prompt injection ROI, conversational drift, data-residency policy, retry-bomb economics).

---

## Files marked WELL-ENRICHED (4+ callouts, no suggestions)

268 files in the book already have 4 or more callouts. They are not enumerated individually here. Examples of well-enriched files include:

- All of `module-04-transformer-architecture/section-4.1.html` through `section-4.5.html` (5-15 callouts each)
- Most regular sections in `module-13-llm-apis`, `module-14-prompt-engineering`, `module-18-fine-tuning-fundamentals`, `module-19-peft`, `module-20-alignment-rlhf-dpo`, `module-22-embeddings-vector-db`, `module-23-rag`, `module-26-ai-agents`, `module-34-evaluation-observability`, `module-35-production-engineering`, `module-37-safety-ethics-regulation`, `module-38-agent-safety-security`, `module-61-frontier-architectures`
- All section pages in `module-31-multimodal/`
- Most appendix sections in `appendix-c-huggingface-ecosystem`, `appendix-d-langchain`, `appendix-e-orchestration-frameworks/index`, `appendix-k-experiment-tracking`, `appendix-l-inference-serving/sections` and similar

A separate scan of WELL-ENRICHED files to check for **over-enrichment** (which the task brief warns against) would be a useful follow-on but is out of scope for this audit.

---

## TODO scaffold list (skipped, need authoring before adding callouts)

These 12 files are scaffolds with under ~200 words of body content and a `<p>TODO ...</p>` block. Adding callouts before the section is authored would be premature.

- `part-3-working-with-llms/module-16-tools-of-the-trade/index.html` (161w)
- `part-3-working-with-llms/module-16-tools-of-the-trade/section-16.1.html` (79w)
- `part-7-multimodal-generation/module-32-embodied-world-models/section-32.4.html` (85w)
- `part-7-multimodal-generation/module-32-embodied-world-models/section-32.8.html` (83w)
- `part-10-idea-to-product/module-40-ideation/index.html` (137w)
- `part-10-idea-to-product/module-41-product-management/index.html` (136w)
- `part-10-idea-to-product/module-42-strategy-prioritization/index.html` (150w)
- `part-10-idea-to-product/module-43-vibe-coding/index.html` (136w)
- `part-10-idea-to-product/module-44-mvp/index.html` (135w)
- `part-10-idea-to-product/module-46-compute-planning/index.html` (147w)
- `part-10-idea-to-product/module-47-scaling-economics/index.html` (150w)
- `part-10-idea-to-product/module-49-post-launch-monitoring/index.html` (133w)
- `part-12-frontiers/module-64-agi-trajectories/section-64.5.html` (76w)

(Note: 13 entries in original detection became 12 after manual review of the part-10 indexes; the audit script's TODO detector triggered on the short-body + `<p>TODO ...</p>` pattern.)

---

## Recommendations for the authoring agent

1. **Start with PATTERN A and PATTERN C conversions** (the `<div class="objectives">` to `callout pathway` and the `<section class="bibliography">` to `callout bibliography` conversions). These are mechanical and bring 70+ chapter indexes from 2 callouts to 4 callouts without writing new prose.
2. **PATTERN B (part indexes)** is the next-highest-leverage change: 12 part-index files each go from 1 callout to 3+ callouts with a `pathway` and a `key-takeaway` pair.
3. **PATTERN D (Tools of the Trade sections)** is the largest pure-authoring block: ~50 sections need new `key-insight` + `practical-example` callouts. Many of these sections are recently authored or being authored by parallel agents; coordinate to avoid clashing edits.
4. **Appendices Q, R, S** are zero-callout reference files where the suggested conversions (war stories to `postmortem` callouts, projects to `exercise` callouts) are the single largest improvement.
5. **Avoid over-enrichment**: the task brief explicitly warns against adding 5+ callouts where the section is short. The PATTERN F appendix recommendations cap at 4 callouts per section.

End of audit.
