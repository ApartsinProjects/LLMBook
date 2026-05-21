# Terminology Inconsistencies Audit (Wave 36, REPORT-ONLY)

Scan of all section HTML files for entity-name inconsistencies. Occurrences inside `<code>`, `<pre>`, code blocks, and bibliography lists are excluded (those are package names or intentional author casing).

- Section files scanned: **576**
- Canonical-term groups with at least one inconsistency: **45**
- Total inconsistent occurrences book-wide: **1444**

## Caveats and judgment calls for the next wave

Some canonical spellings recommended here are de jure (per the dedup_detector
entity dictionary) but the book's de-facto usage diverges. The next (fix-applying)
wave should make the final call before mass-replacing. Specific cases:

- **`pre-training` vs `pretraining`**: The dedup_detector dictionary does not
  pin this. The chapter 6 title and `<h1>` use `Pre-training` (hyphenated, 161
  body occurrences), but `pretraining` (one word) appears 445 times in body
  text and is used in the module directory name `module-06-pretraining-scaling-laws`.
  This is the largest cluster (414 hits). **Decision needed**: pick one of
  `pre-training` (matches chapter title) or `pretraining` (matches body-text
  majority and dir name). I recommend `pretraining` for the body; preserve
  `Pre-training` only in the chapter title and TOC because it is already used
  consistently there.
- **`Chain-of-Thought` vs `chain-of-thought`**: Body usage is mostly lowercase
  (`chain-of-thought`, 220 hits) vs the title-case form (44 hits). For
  technical-method names a reasonable rule is title-case when introducing the
  method by name, lowercase when used adjectivally ("a chain-of-thought
  prompt"). The fix wave should preserve this distinction rather than blindly
  upper-casing every occurrence.
- **`Llama-3` vs `Llama 3`**: Canonical wins (264 vs 179) but the
  no-hyphen variant `Llama 3` is the form Meta uses in their own paper titles.
  Recommend `Llama-3` in running prose and `Llama 3` only inside direct
  quotations of paper or release-blog titles.
- **`Hugging Face` vs `HuggingFace`**: Canonical wins (341 vs 216) but the
  product `HuggingFace Hub` is sometimes spelled `Hugging Face Hub` and
  sometimes `HuggingFace Hub`; the company prefers the two-word "Hugging Face"
  for the entity and "Hugging Face Hub" for the product.
- **`fine-tuning` vs `finetuning` vs `fine tuning`**: Canonical is `fine-tuning`
  (hyphen). Only 9 inconsistent hits; safe to mass-replace.
- **`openai` and `anthropic` lowercase in prose**: 14 hits for `openai` and
  10 hits for `anthropic` were flagged, but on inspection most are intentional
  package-name references (e.g. "the openai SDK", "the anthropic Python
  package"). These should be wrapped in `<code>` rather than upper-cased. The
  fix wave should hand-inspect each occurrence; do NOT blanket-replace lowercase
  to title case.

For terms where the canonical and the book's body usage agree (KV cache,
PyTorch, LoRA, RLHF, MMLU, etc.), the fix wave can mass-replace without
hesitation.

## Top inconsistency clusters (ranked by total non-canonical hits)

| Rank | Canonical term | Non-canonical hits | Sections affected |
|---:|---|---:|---:|
| 1 | `pre-training` (Pre-training (concept)) | 414 | 146 |
| 2 | `Chain-of-Thought` (Chain-of-Thought (method)) | 242 | 72 |
| 3 | `Hugging Face` (Hugging Face (vendor/library)) | 216 | 91 |
| 4 | `Llama-3` (Llama-3 (model family)) | 179 | 64 |
| 5 | `KV cache` (KV cache (concept)) | 99 | 44 |
| 6 | `FlashAttention` (FlashAttention (method)) | 42 | 11 |
| 7 | `Llama-2` (Llama-2 (model family)) | 35 | 18 |
| 8 | `scikit-learn` (scikit-learn (library)) | 28 | 14 |
| 9 | `instruction tuning` (Instruction tuning (concept)) | 22 | 10 |
| 10 | `Mixture-of-Experts` (Mixture-of-Experts (method)) | 19 | 13 |
| 11 | `OpenAI` (OpenAI (vendor)) | 14 | 9 |
| 12 | `context window` (Context window (concept)) | 12 | 12 |
| 13 | `SOC 2` (SOC 2 (certification)) | 12 | 7 |
| 14 | `Claude` (Claude (model)) | 11 | 3 |
| 15 | `Anthropic` (Anthropic (vendor)) | 10 | 5 |
| 16 | `fine-tuning` (Fine-tuning (concept)) | 9 | 5 |
| 17 | `pandas` (Pandas (library)) | 8 | 4 |
| 18 | `hallucination` (Hallucination (concept)) | 8 | 8 |
| 19 | `NumPy` (NumPy (library)) | 7 | 7 |
| 20 | `RAG` (RAG (method)) | 6 | 4 |
| 21 | `PagedAttention` (PagedAttention (method)) | 5 | 4 |
| 22 | `BERT` (BERT (model)) | 5 | 5 |
| 23 | `LangChain` (LangChain (library)) | 4 | 4 |
| 24 | `context length` (Context length (concept)) | 4 | 4 |
| 25 | `NIST AI RMF` (NIST AI RMF (framework)) | 4 | 3 |
| 26 | `vLLM` (vLLM (library)) | 3 | 3 |
| 27 | `cross-attention` (Cross-attention (concept)) | 2 | 2 |
| 28 | `Attention Is All You Need` ("Attention Is All You Need" (paper title)) | 2 | 2 |
| 29 | `PyTorch` (PyTorch (library)) | 2 | 2 |
| 30 | `RLHF` (RLHF (method)) | 2 | 2 |

---

## Per-term detail

### Pre-training (concept)

- **Recommended canonical spelling**: `pre-training`
- **Total non-canonical occurrences**: 414
- **Sections affected**: 146
- **Non-canonical variants observed:**
  - `pretraining`: 366 occurrence(s)
  - `Pretraining`: 48 occurrence(s)

- **Top offending files (up to 10):**
  - `part-12-llm-systems-at-scale/module-61-scale-tools/section-61.3.html`: 37 hit(s); pretraining=36, Pretraining=1
  - `part-12-llm-systems-at-scale/module-61-scale-tools/section-61.2.html`: 17 hit(s); pretraining=16, Pretraining=1
  - `part-2-understanding-llms/module-10-interpretability/section-10.9.html`: 15 hit(s); pretraining=10, Pretraining=5
  - `part-15-llm-agentic-ai-research-frontiers/module-75-frontier-architectures/section-75.2.html`: 13 hit(s); pretraining=9, Pretraining=4
  - `part-11-llm-ethics-trust-governance/module-55-environmental-sustainability/section-55.1.html`: 12 hit(s); pretraining=10, Pretraining=2
  - `part-12-llm-systems-at-scale/module-61-scale-tools/section-61.1.html`: 11 hit(s); pretraining=11
  - `part-5-multimodal-llms/module-22-vision-language-models/section-22.1.html`: 11 hit(s); pretraining=8, Pretraining=3
  - `part-4-training-adaptation/module-16-fine-tuning-fundamentals/section-16.3.html`: 10 hit(s); pretraining=9, Pretraining=1
  - `part-5-multimodal-llms/module-21-document-understanding-ocr/section-21.2.html`: 10 hit(s); pretraining=9, Pretraining=1
  - `part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.8.html`: 9 hit(s); pretraining=9

### Chain-of-Thought (method)

- **Recommended canonical spelling**: `Chain-of-Thought`
- **Total non-canonical occurrences**: 242
- **Sections affected**: 72
- **Non-canonical variants observed:**
  - `chain-of-thought`: 220 occurrence(s)
  - `Chain-of-thought (lower t)`: 18 occurrence(s)
  - `Chain of Thought (use hyphens)`: 4 occurrence(s)

- **Top offending files (up to 10):**
  - `part-1-llm-building-blocks/module-03-transformer-architecture/section-3.7.html`: 21 hit(s); chain-of-thought=18, Chain-of-thought (lower t)=3
  - `part-2-understanding-llms/module-08-reasoning-test-time-compute/section-8.1.html`: 17 hit(s); chain-of-thought=12, Chain-of-thought (lower t)=3, Chain of Thought (use hyphens)=2
  - `part-15-llm-agentic-ai-research-frontiers/module-76-frontier-theory/section-76.1.html`: 13 hit(s); chain-of-thought=10, Chain-of-thought (lower t)=3
  - `part-3-working-with-llms/module-12-prompt-engineering/section-12.2.html`: 11 hit(s); chain-of-thought=9, Chain-of-thought (lower t)=1, Chain of Thought (use hyphens)=1
  - `part-4-training-adaptation/module-15-synthetic-data/section-15.6.html`: 11 hit(s); chain-of-thought=11
  - `part-4-training-adaptation/module-17-peft/section-17.6.html`: 10 hit(s); chain-of-thought=8, Chain-of-thought (lower t)=2
  - `part-2-understanding-llms/module-08-reasoning-test-time-compute/section-8.2.html`: 9 hit(s); chain-of-thought=9
  - `part-2-understanding-llms/module-08-reasoning-test-time-compute/section-8.4.html`: 8 hit(s); chain-of-thought=8
  - `part-4-training-adaptation/module-18-alignment-rlhf-dpo/section-18.6.html`: 7 hit(s); chain-of-thought=7
  - `part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.1.html`: 6 hit(s); chain-of-thought=5, Chain-of-thought (lower t)=1

### Hugging Face (vendor/library)

- **Recommended canonical spelling**: `Hugging Face`
- **Total non-canonical occurrences**: 216
- **Sections affected**: 91
- **Non-canonical variants observed:**
  - `HuggingFace (one word)`: 214 occurrence(s)
  - `huggingface`: 2 occurrence(s)

- **Top offending files (up to 10):**
  - `part-2-understanding-llms/module-10-interpretability/section-10.8.html`: 14 hit(s); HuggingFace (one word)=14
  - `part-13-llmops-lifecycle/module-66-reliability-slos-registry/section-66.2.html`: 8 hit(s); HuggingFace (one word)=8
  - `part-4-training-adaptation/module-19-tools-of-the-trade/index.html`: 8 hit(s); HuggingFace (one word)=8
  - `part-4-training-adaptation/module-19-tools-of-the-trade/section-19.4.html`: 7 hit(s); HuggingFace (one word)=7
  - `part-4-training-adaptation/module-19-tools-of-the-trade/section-19.7.html`: 7 hit(s); HuggingFace (one word)=7
  - `part-11-llm-ethics-trust-governance/module-56-responsible-ai-tools/section-56.2.html`: 6 hit(s); HuggingFace (one word)=6
  - `part-5-multimodal-llms/module-24-vla-models/section-24.2.html`: 6 hit(s); HuggingFace (one word)=6
  - `part-5-multimodal-llms/module-25-tools-of-the-trade/section-25.2.html`: 6 hit(s); HuggingFace (one word)=6
  - `part-1-llm-building-blocks/module-05-tools-of-the-trade/section-5.1.html`: 5 hit(s); HuggingFace (one word)=5
  - `part-1-llm-building-blocks/module-05-tools-of-the-trade/section-5.2.html`: 5 hit(s); HuggingFace (one word)=5

### Llama-3 (model family)

- **Recommended canonical spelling**: `Llama-3`
- **Total non-canonical occurrences**: 179
- **Sections affected**: 64
- **Non-canonical variants observed:**
  - `Llama 3 (use hyphen: Llama-3)`: 170 occurrence(s)
  - `LLaMA 3`: 5 occurrence(s)
  - `LLaMA-3`: 4 occurrence(s)

- **Top offending files (up to 10):**
  - `part-2-understanding-llms/module-09-inference-optimization/section-9.3.html`: 26 hit(s); Llama 3 (use hyphen: Llama-3)=26
  - `part-2-understanding-llms/module-07-modern-llm-landscape/section-7.3.html`: 19 hit(s); Llama 3 (use hyphen: Llama-3)=19
  - `part-1-llm-building-blocks/module-01-foundations-nlp-text-representation/section-1.7.html`: 12 hit(s); Llama 3 (use hyphen: Llama-3)=12
  - `part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.3.html`: 10 hit(s); Llama 3 (use hyphen: Llama-3)=8, LLaMA 3=2
  - `part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.8.html`: 6 hit(s); Llama 3 (use hyphen: Llama-3)=6
  - `part-12-llm-systems-at-scale/module-61-scale-tools/section-61.5.html`: 5 hit(s); Llama 3 (use hyphen: Llama-3)=5
  - `part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.1.html`: 5 hit(s); Llama 3 (use hyphen: Llama-3)=5
  - `part-11-llm-ethics-trust-governance/module-54b-transparency-and-disclosure/section-54.6.html`: 4 hit(s); Llama 3 (use hyphen: Llama-3)=4
  - `part-11-llm-ethics-trust-governance/module-55-environmental-sustainability/section-55.1.html`: 4 hit(s); Llama 3 (use hyphen: Llama-3)=4
  - `part-13-llmops-lifecycle/module-65-containers-kubernetes/section-65.5.html`: 4 hit(s); Llama 3 (use hyphen: Llama-3)=4

### KV cache (concept)

- **Recommended canonical spelling**: `KV cache`
- **Total non-canonical occurrences**: 99
- **Sections affected**: 44
- **Non-canonical variants observed:**
  - `KV-cache (use space)`: 70 occurrence(s)
  - `KV Cache (lower 'cache')`: 29 occurrence(s)

- **Top offending files (up to 10):**
  - `part-2-understanding-llms/module-09-inference-optimization/section-9.4.html`: 22 hit(s); KV-cache (use space)=21, KV Cache (lower 'cache')=1
  - `part-2-understanding-llms/module-09-inference-optimization/section-9.3.html`: 8 hit(s); KV Cache (lower 'cache')=8
  - `part-2-understanding-llms/module-09-inference-optimization/section-9.2.html`: 7 hit(s); KV-cache (use space)=6, KV Cache (lower 'cache')=1
  - `part-2-understanding-llms/module-10-interpretability/section-10.8.html`: 5 hit(s); KV Cache (lower 'cache')=3, KV-cache (use space)=2
  - `part-12-llm-systems-at-scale/module-57-compute-planning/section-57.4.html`: 4 hit(s); KV Cache (lower 'cache')=4
  - `part-2-understanding-llms/module-09-inference-optimization/section-9.7.html`: 4 hit(s); KV-cache (use space)=3, KV Cache (lower 'cache')=1
  - `part-1-llm-building-blocks/module-03-transformer-architecture/section-3.5.html`: 3 hit(s); KV-cache (use space)=2, KV Cache (lower 'cache')=1
  - `part-2-understanding-llms/module-09-inference-optimization/index.html`: 3 hit(s); KV-cache (use space)=2, KV Cache (lower 'cache')=1
  - `part-1-llm-building-blocks/module-03-transformer-architecture/section-3.2.html`: 2 hit(s); KV Cache (lower 'cache')=2
  - `part-12-llm-systems-at-scale/module-58-frontier-systems-hardware/section-58.4.html`: 2 hit(s); KV-cache (use space)=2

### FlashAttention (method)

- **Recommended canonical spelling**: `FlashAttention`
- **Total non-canonical occurrences**: 42
- **Sections affected**: 11
- **Non-canonical variants observed:**
  - `Flash Attention`: 42 occurrence(s)

- **Top offending files (up to 10):**
  - `part-12-llm-systems-at-scale/module-61-scale-tools/section-61.2.html`: 23 hit(s); Flash Attention=23
  - `part-4-training-adaptation/module-16-fine-tuning-fundamentals/section-16.7.html`: 5 hit(s); Flash Attention=5
  - `part-1-llm-building-blocks/module-03-transformer-architecture/section-3.4.html`: 2 hit(s); Flash Attention=2
  - `part-1-llm-building-blocks/module-03-transformer-architecture/section-3.6.html`: 2 hit(s); Flash Attention=2
  - `part-12-llm-systems-at-scale/module-61-scale-tools/index.html`: 2 hit(s); Flash Attention=2
  - `part-12-llm-systems-at-scale/module-61-scale-tools/section-61.5.html`: 2 hit(s); Flash Attention=2
  - `part-13-llmops-lifecycle/module-65-containers-kubernetes/section-65.4.html`: 2 hit(s); Flash Attention=2
  - `part-1-llm-building-blocks/module-02-sequence-models-attention/section-2.4.html`: 1 hit(s); Flash Attention=1
  - `part-12-llm-systems-at-scale/module-61-scale-tools/section-61.3.html`: 1 hit(s); Flash Attention=1
  - `part-2-understanding-llms/module-08-reasoning-test-time-compute/section-8.1.html`: 1 hit(s); Flash Attention=1

### Llama-2 (model family)

- **Recommended canonical spelling**: `Llama-2`
- **Total non-canonical occurrences**: 35
- **Sections affected**: 18
- **Non-canonical variants observed:**
  - `Llama 2 (use hyphen: Llama-2)`: 32 occurrence(s)
  - `LLaMA 2`: 3 occurrence(s)

- **Top offending files (up to 10):**
  - `part-2-understanding-llms/module-09-inference-optimization/section-9.3.html`: 6 hit(s); Llama 2 (use hyphen: Llama-2)=6
  - `part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.1.html`: 5 hit(s); Llama 2 (use hyphen: Llama-2)=5
  - `part-2-understanding-llms/module-07-modern-llm-landscape/section-7.3.html`: 4 hit(s); Llama 2 (use hyphen: Llama-2)=4
  - `part-4-training-adaptation/module-16-fine-tuning-fundamentals/section-16.7.html`: 3 hit(s); Llama 2 (use hyphen: Llama-2)=3
  - `part-1-llm-building-blocks/module-02-sequence-models-attention/section-2.4.html`: 2 hit(s); Llama 2 (use hyphen: Llama-2)=2
  - `part-1-llm-building-blocks/module-03-transformer-architecture/section-3.5.html`: 2 hit(s); LLaMA 2=1, Llama 2 (use hyphen: Llama-2)=1
  - `part-12-llm-systems-at-scale/module-57-compute-planning/section-57.4.html`: 2 hit(s); Llama 2 (use hyphen: Llama-2)=2
  - `part-1-llm-building-blocks/module-01-foundations-nlp-text-representation/section-1.6.html`: 1 hit(s); Llama 2 (use hyphen: Llama-2)=1
  - `part-1-llm-building-blocks/module-03-transformer-architecture/section-3.6.html`: 1 hit(s); Llama 2 (use hyphen: Llama-2)=1
  - `part-12-llm-systems-at-scale/module-61-scale-tools/section-61.3.html`: 1 hit(s); Llama 2 (use hyphen: Llama-2)=1

### scikit-learn (library)

- **Recommended canonical spelling**: `scikit-learn`
- **Total non-canonical occurrences**: 28
- **Sections affected**: 14
- **Non-canonical variants observed:**
  - `sklearn (use 'scikit-learn' in prose)`: 28 occurrence(s)

- **Top offending files (up to 10):**
  - `part-11-llm-ethics-trust-governance/module-56-responsible-ai-tools/section-56.2.html`: 8 hit(s); sklearn (use 'scikit-learn' in prose)=8
  - `part-3-working-with-llms/module-13-hybrid-ml-llm/section-13.1.html`: 3 hit(s); sklearn (use 'scikit-learn' in prose)=3
  - `part-7-retrieval-information-extraction-with-llms/module-31-embeddings-vector-db/section-31.7.html`: 3 hit(s); sklearn (use 'scikit-learn' in prose)=3
  - `part-11-llm-ethics-trust-governance/module-56-responsible-ai-tools/section-56.1.html`: 2 hit(s); sklearn (use 'scikit-learn' in prose)=2
  - `part-13-llmops-lifecycle/module-63-ai-gateways-routing/section-63.1.html`: 2 hit(s); sklearn (use 'scikit-learn' in prose)=2
  - `part-8-conversational-ai-with-llms/module-37-conversational-ai/section-37.6.html`: 2 hit(s); sklearn (use 'scikit-learn' in prose)=2
  - `part-1-llm-building-blocks/module-01-foundations-nlp-text-representation/section-1.2.html`: 1 hit(s); sklearn (use 'scikit-learn' in prose)=1
  - `part-1-llm-building-blocks/module-01-foundations-nlp-text-representation/section-1.4.html`: 1 hit(s); sklearn (use 'scikit-learn' in prose)=1
  - `part-1-llm-building-blocks/module-05-tools-of-the-trade/section-5.1.html`: 1 hit(s); sklearn (use 'scikit-learn' in prose)=1
  - `part-11-llm-ethics-trust-governance/module-56-responsible-ai-tools/section-56.3.html`: 1 hit(s); sklearn (use 'scikit-learn' in prose)=1

### Instruction tuning (concept)

- **Recommended canonical spelling**: `instruction tuning`
- **Total non-canonical occurrences**: 22
- **Sections affected**: 10
- **Non-canonical variants observed:**
  - `instruction-tuning`: 20 occurrence(s)
  - `Instruction-tuning`: 2 occurrence(s)

- **Top offending files (up to 10):**
  - `part-12-llm-systems-at-scale/module-61-scale-tools/section-61.3.html`: 7 hit(s); instruction-tuning=6, Instruction-tuning=1
  - `part-4-training-adaptation/module-19-tools-of-the-trade/section-19.3.html`: 3 hit(s); instruction-tuning=2, Instruction-tuning=1
  - `part-5-multimodal-llms/module-22-vision-language-models/section-22.3.html`: 3 hit(s); instruction-tuning=3
  - `part-3-working-with-llms/module-14-tools-of-the-trade/section-14.3.html`: 2 hit(s); instruction-tuning=2
  - `part-4-training-adaptation/module-16-fine-tuning-fundamentals/section-16.2.html`: 2 hit(s); instruction-tuning=2
  - `part-1-llm-building-blocks/module-01-foundations-nlp-text-representation/section-1.7.html`: 1 hit(s); instruction-tuning=1
  - `part-10-llm-security-runtime-safety/module-50-privacy-data-protection/section-50.3.html`: 1 hit(s); instruction-tuning=1
  - `part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.1.html`: 1 hit(s); instruction-tuning=1
  - `part-4-training-adaptation/module-15-synthetic-data/section-15.2.html`: 1 hit(s); instruction-tuning=1
  - `part-4-training-adaptation/module-15-synthetic-data/section-15.3.html`: 1 hit(s); instruction-tuning=1

### Mixture-of-Experts (method)

- **Recommended canonical spelling**: `Mixture-of-Experts`
- **Total non-canonical occurrences**: 19
- **Sections affected**: 13
- **Non-canonical variants observed:**
  - `Mixture of Experts`: 10 occurrence(s)
  - `mixture-of-experts`: 7 occurrence(s)
  - `mixture of experts`: 2 occurrence(s)

- **Top offending files (up to 10):**
  - `part-2-understanding-llms/module-07-modern-llm-landscape/section-7.3.html`: 5 hit(s); Mixture of Experts=5
  - `part-15-llm-agentic-ai-research-frontiers/module-75-frontier-architectures/section-75.3.html`: 3 hit(s); Mixture of Experts=1, mixture of experts=1, mixture-of-experts=1
  - `part-1-llm-building-blocks/module-03-transformer-architecture/section-3.8.html`: 1 hit(s); mixture-of-experts=1
  - `part-11-llm-ethics-trust-governance/module-55-environmental-sustainability/section-55.1.html`: 1 hit(s); Mixture of Experts=1
  - `part-12-llm-systems-at-scale/module-61-scale-tools/section-61.4.html`: 1 hit(s); mixture-of-experts=1
  - `part-15-llm-agentic-ai-research-frontiers/module-75-frontier-architectures/index.html`: 1 hit(s); mixture-of-experts=1
  - `part-15-llm-agentic-ai-research-frontiers/module-75-frontier-architectures/section-75.1.html`: 1 hit(s); mixture-of-experts=1
  - `part-15-llm-agentic-ai-research-frontiers/module-75-frontier-architectures/section-75.2.html`: 1 hit(s); Mixture of Experts=1
  - `part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.3.html`: 1 hit(s); mixture-of-experts=1
  - `part-2-understanding-llms/module-07-modern-llm-landscape/index.html`: 1 hit(s); Mixture of Experts=1

### OpenAI (vendor)

- **Recommended canonical spelling**: `OpenAI`
- **Total non-canonical occurrences**: 14
- **Sections affected**: 9
- **Non-canonical variants observed:**
  - `openai (in prose, use 'OpenAI')`: 14 occurrence(s)

- **Top offending files (up to 10):**
  - `part-3-working-with-llms/module-14-tools-of-the-trade/section-14.2.html`: 6 hit(s); openai (in prose, use 'OpenAI')=6
  - `part-12-llm-systems-at-scale/module-57-compute-planning/section-57.2.html`: 1 hit(s); openai (in prose, use 'OpenAI')=1
  - `part-14-designing-llm-agent-products/module-69-llm-economics/section-69.3.html`: 1 hit(s); openai (in prose, use 'OpenAI')=1
  - `part-2-understanding-llms/module-07-modern-llm-landscape/section-7.1.html`: 1 hit(s); openai (in prose, use 'OpenAI')=1
  - `part-5-multimodal-llms/module-25-tools-of-the-trade/section-25.2.html`: 1 hit(s); openai (in prose, use 'OpenAI')=1
  - `part-6-agentic-ai/module-30-tools-of-the-trade/section-30.2.html`: 1 hit(s); openai (in prose, use 'OpenAI')=1
  - `part-7-retrieval-information-extraction-with-llms/module-36-retrieval-tools/section-36.5.html`: 1 hit(s); openai (in prose, use 'OpenAI')=1
  - `part-9-llm-evaluation-observability/module-43-specialized-evaluation/section-43.4.html`: 1 hit(s); openai (in prose, use 'OpenAI')=1
  - `part-9-llm-evaluation-observability/module-45-tools-of-the-trade/section-45.2.html`: 1 hit(s); openai (in prose, use 'OpenAI')=1

### Context window (concept)

- **Recommended canonical spelling**: `context window`
- **Total non-canonical occurrences**: 12
- **Sections affected**: 12
- **Non-canonical variants observed:**
  - `Context Window (title case in prose)`: 6 occurrence(s)
  - `context-window (use space)`: 6 occurrence(s)

- **Top offending files (up to 10):**
  - `part-1-llm-building-blocks/module-01-foundations-nlp-text-representation/section-1.5.html`: 1 hit(s); Context Window (title case in prose)=1
  - `part-1-llm-building-blocks/module-03-transformer-architecture/section-3.5.html`: 1 hit(s); context-window (use space)=1
  - `part-12-llm-systems-at-scale/module-61-scale-tools/section-61.4.html`: 1 hit(s); context-window (use space)=1
  - `part-2-understanding-llms/module-07-modern-llm-landscape/section-7.2.html`: 1 hit(s); Context Window (title case in prose)=1
  - `part-5-multimodal-llms/module-22-vision-language-models/section-22.3.html`: 1 hit(s); context-window (use space)=1
  - `part-5-multimodal-llms/module-22-vision-language-models/section-22.4.html`: 1 hit(s); Context Window (title case in prose)=1
  - `part-5-multimodal-llms/module-24-vla-models/section-24.10.html`: 1 hit(s); context-window (use space)=1
  - `part-7-retrieval-information-extraction-with-llms/module-32-rag/index.html`: 1 hit(s); context-window (use space)=1
  - `part-7-retrieval-information-extraction-with-llms/module-32-rag/section-32.1.html`: 1 hit(s); Context Window (title case in prose)=1
  - `part-8-conversational-ai-with-llms/module-37-conversational-ai/section-37.3.html`: 1 hit(s); Context Window (title case in prose)=1

### SOC 2 (certification)

- **Recommended canonical spelling**: `SOC 2`
- **Total non-canonical occurrences**: 12
- **Sections affected**: 7
- **Non-canonical variants observed:**
  - `SOC2 (no space)`: 10 occurrence(s)
  - `SOC-2`: 2 occurrence(s)

- **Top offending files (up to 10):**
  - `part-3-working-with-llms/module-14-tools-of-the-trade/section-14.1.html`: 5 hit(s); SOC2 (no space)=5
  - `part-9-llm-evaluation-observability/module-44-online-eval-observability/section-44.7.html`: 2 hit(s); SOC-2=2
  - `part-10-llm-security-runtime-safety/module-51-tools-of-the-trade/section-51.1.html`: 1 hit(s); SOC2 (no space)=1
  - `part-12-llm-systems-at-scale/module-57-compute-planning/section-57.2.html`: 1 hit(s); SOC2 (no space)=1
  - `part-14-designing-llm-agent-products/module-67-ideation/section-67.8.html`: 1 hit(s); SOC2 (no space)=1
  - `part-14-designing-llm-agent-products/module-69-llm-economics/section-69.3.html`: 1 hit(s); SOC2 (no space)=1
  - `part-14-applications-of-llms-across-industries/module-74-tools-of-the-trade/section-74.1.html`: 1 hit(s); SOC2 (no space)=1

### Claude (model)

- **Recommended canonical spelling**: `Claude`
- **Total non-canonical occurrences**: 11
- **Sections affected**: 3
- **Non-canonical variants observed:**
  - `CLAUDE`: 11 occurrence(s)

- **Top offending files (up to 10):**
  - `part-6-agentic-ai/module-29-specialized-agents/section-29.4.html`: 6 hit(s); CLAUDE=6
  - `part-14-designing-llm-agent-products/module-68-vibe-coding/section-68.2.html`: 3 hit(s); CLAUDE=3
  - `part-14-designing-llm-agent-products/module-67-ideation/section-67.14.html`: 2 hit(s); CLAUDE=2

### Anthropic (vendor)

- **Recommended canonical spelling**: `Anthropic`
- **Total non-canonical occurrences**: 10
- **Sections affected**: 5
- **Non-canonical variants observed:**
  - `anthropic (in prose, use 'Anthropic')`: 10 occurrence(s)

- **Top offending files (up to 10):**
  - `part-3-working-with-llms/module-14-tools-of-the-trade/section-14.2.html`: 5 hit(s); anthropic (in prose, use 'Anthropic')=5
  - `part-3-working-with-llms/module-11-llm-apis/section-11.3.html`: 2 hit(s); anthropic (in prose, use 'Anthropic')=2
  - `part-12-llm-systems-at-scale/module-57-compute-planning/section-57.2.html`: 1 hit(s); anthropic (in prose, use 'Anthropic')=1
  - `part-2-understanding-llms/module-07-modern-llm-landscape/section-7.1.html`: 1 hit(s); anthropic (in prose, use 'Anthropic')=1
  - `part-6-agentic-ai/module-26-ai-agents/section-26.3.html`: 1 hit(s); anthropic (in prose, use 'Anthropic')=1

### Fine-tuning (concept)

- **Recommended canonical spelling**: `fine-tuning`
- **Total non-canonical occurrences**: 9
- **Sections affected**: 5
- **Non-canonical variants observed:**
  - `finetuning`: 6 occurrence(s)
  - `Finetuning`: 3 occurrence(s)

- **Top offending files (up to 10):**
  - `part-5-multimodal-llms/module-24-vla-models/section-24.1.html`: 3 hit(s); finetuning=2, Finetuning=1
  - `part-5-multimodal-llms/module-24-vla-models/section-24.2.html`: 3 hit(s); Finetuning=2, finetuning=1
  - `part-3-working-with-llms/module-12-prompt-engineering/section-12.3.html`: 1 hit(s); finetuning=1
  - `part-5-multimodal-llms/module-24-vla-models/section-24.3.html`: 1 hit(s); finetuning=1
  - `part-5-multimodal-llms/module-24-vla-models/section-24.4.html`: 1 hit(s); finetuning=1

### Pandas (library)

- **Recommended canonical spelling**: `pandas`
- **Total non-canonical occurrences**: 8
- **Sections affected**: 4
- **Non-canonical variants observed:**
  - `Pandas (canonical is lowercase 'pandas')`: 8 occurrence(s)

- **Top offending files (up to 10):**
  - `part-1-llm-building-blocks/module-05-tools-of-the-trade/section-5.2.html`: 3 hit(s); Pandas (canonical is lowercase 'pandas')=3
  - `part-1-llm-building-blocks/module-00-ml-pytorch-foundations/section-0.3.html`: 2 hit(s); Pandas (canonical is lowercase 'pandas')=2
  - `part-4-training-adaptation/module-19-tools-of-the-trade/section-19.13.html`: 2 hit(s); Pandas (canonical is lowercase 'pandas')=2
  - `part-9-llm-evaluation-observability/module-43-specialized-evaluation/section-43.4.html`: 1 hit(s); Pandas (canonical is lowercase 'pandas')=1

### Hallucination (concept)

- **Recommended canonical spelling**: `hallucination`
- **Total non-canonical occurrences**: 8
- **Sections affected**: 8
- **Non-canonical variants observed:**
  - `Hallucinations (mid-sentence)`: 8 occurrence(s)

- **Top offending files (up to 10):**
  - `part-10-llm-security-runtime-safety/module-49-agent-safety-autonomy/section-49.5.html`: 1 hit(s); Hallucinations (mid-sentence)=1
  - `part-10-llm-security-runtime-safety/module-51-tools-of-the-trade/index.html`: 1 hit(s); Hallucinations (mid-sentence)=1
  - `part-11-llm-ethics-trust-governance/index.html`: 1 hit(s); Hallucinations (mid-sentence)=1
  - `part-11-llm-ethics-trust-governance/module-52-bias-fairness/index.html`: 1 hit(s); Hallucinations (mid-sentence)=1
  - `part-11-llm-ethics-trust-governance/module-54b-transparency-and-disclosure/section-54.8.html`: 1 hit(s); Hallucinations (mid-sentence)=1
  - `part-14-designing-llm-agent-products/module-67-ideation/section-67.9.html`: 1 hit(s); Hallucinations (mid-sentence)=1
  - `part-3-working-with-llms/module-12-prompt-engineering/section-12.1.html`: 1 hit(s); Hallucinations (mid-sentence)=1
  - `part-6-agentic-ai/module-30-tools-of-the-trade/section-30.3.html`: 1 hit(s); Hallucinations (mid-sentence)=1

### NumPy (library)

- **Recommended canonical spelling**: `NumPy`
- **Total non-canonical occurrences**: 7
- **Sections affected**: 7
- **Non-canonical variants observed:**
  - `numpy`: 6 occurrence(s)
  - `Numpy`: 1 occurrence(s)

- **Top offending files (up to 10):**
  - `part-1-llm-building-blocks/module-01-foundations-nlp-text-representation/section-1.2.html`: 1 hit(s); numpy=1
  - `part-1-llm-building-blocks/module-05-tools-of-the-trade/index.html`: 1 hit(s); numpy=1
  - `part-1-llm-building-blocks/module-05-tools-of-the-trade/section-5.2.html`: 1 hit(s); Numpy=1
  - `part-10-llm-security-runtime-safety/module-49-agent-safety-autonomy/section-49.2.html`: 1 hit(s); numpy=1
  - `part-4-training-adaptation/module-15-synthetic-data/section-15.4.html`: 1 hit(s); numpy=1
  - `part-4-training-adaptation/module-16-fine-tuning-fundamentals/section-16.5.html`: 1 hit(s); numpy=1
  - `part-7-retrieval-information-extraction-with-llms/module-32-rag/section-32.2.html`: 1 hit(s); numpy=1

### RAG (method)

- **Recommended canonical spelling**: `RAG`
- **Total non-canonical occurrences**: 6
- **Sections affected**: 4
- **Non-canonical variants observed:**
  - `Rag`: 6 occurrence(s)

- **Top offending files (up to 10):**
  - `part-7-retrieval-information-extraction-with-llms/module-36-retrieval-tools/section-36.5.html`: 3 hit(s); Rag=3
  - `part-14-applications-of-llms-across-industries/module-67-legal-llms/section-67.4.html`: 1 hit(s); Rag=1
  - `part-14-applications-of-llms-across-industries/module-72-government-llms/section-72.4.html`: 1 hit(s); Rag=1
  - `part-14-applications-of-llms-across-industries/module-73-manufacturing-llms/section-73.4.html`: 1 hit(s); Rag=1

### PagedAttention (method)

- **Recommended canonical spelling**: `PagedAttention`
- **Total non-canonical occurrences**: 5
- **Sections affected**: 4
- **Non-canonical variants observed:**
  - `paged attention`: 4 occurrence(s)
  - `paged-attention`: 1 occurrence(s)

- **Top offending files (up to 10):**
  - `part-2-understanding-llms/module-09-inference-optimization/section-9.3.html`: 2 hit(s); paged attention=2
  - `part-1-llm-building-blocks/module-03-transformer-architecture/section-3.2.html`: 1 hit(s); paged attention=1
  - `part-11-llm-ethics-trust-governance/module-56-responsible-ai-tools/section-56.5.html`: 1 hit(s); paged attention=1
  - `part-4-training-adaptation/module-16-fine-tuning-fundamentals/section-16.7.html`: 1 hit(s); paged-attention=1

### BERT (model)

- **Recommended canonical spelling**: `BERT`
- **Total non-canonical occurrences**: 5
- **Sections affected**: 5
- **Non-canonical variants observed:**
  - `Bert`: 5 occurrence(s)

- **Top offending files (up to 10):**
  - `part-14-applications-of-llms-across-industries/module-70-education-llms/section-70.1.html`: 1 hit(s); Bert=1
  - `part-2-understanding-llms/module-07-modern-llm-landscape/section-7.1.html`: 1 hit(s); Bert=1
  - `part-2-understanding-llms/module-07-modern-llm-landscape/section-7.2.html`: 1 hit(s); Bert=1
  - `part-2-understanding-llms/module-07-modern-llm-landscape/section-7.3.html`: 1 hit(s); Bert=1
  - `part-2-understanding-llms/module-07-modern-llm-landscape/section-7.4.html`: 1 hit(s); Bert=1

### LangChain (library)

- **Recommended canonical spelling**: `LangChain`
- **Total non-canonical occurrences**: 4
- **Sections affected**: 4
- **Non-canonical variants observed:**
  - `langchain`: 3 occurrence(s)
  - `Langchain`: 1 occurrence(s)

- **Top offending files (up to 10):**
  - `part-1-llm-building-blocks/module-01-foundations-nlp-text-representation/section-1.7.html`: 1 hit(s); Langchain=1
  - `part-1-llm-building-blocks/module-05-tools-of-the-trade/section-5.2.html`: 1 hit(s); langchain=1
  - `part-6-agentic-ai/module-30-tools-of-the-trade/section-30.6.html`: 1 hit(s); langchain=1
  - `part-7-retrieval-information-extraction-with-llms/module-36-retrieval-tools/section-36.5.html`: 1 hit(s); langchain=1

### Context length (concept)

- **Recommended canonical spelling**: `context length`
- **Total non-canonical occurrences**: 4
- **Sections affected**: 4
- **Non-canonical variants observed:**
  - `context-length`: 4 occurrence(s)

- **Top offending files (up to 10):**
  - `part-1-llm-building-blocks/module-03-transformer-architecture/section-3.5.html`: 1 hit(s); context-length=1
  - `part-12-llm-systems-at-scale/module-60-edge-on-device-llms/section-60.1.html`: 1 hit(s); context-length=1
  - `part-5-multimodal-llms/module-22-vision-language-models/section-22.7.html`: 1 hit(s); context-length=1
  - `part-5-multimodal-llms/module-24-vla-models/section-24.10.html`: 1 hit(s); context-length=1

### NIST AI RMF (framework)

- **Recommended canonical spelling**: `NIST AI RMF`
- **Total non-canonical occurrences**: 4
- **Sections affected**: 3
- **Non-canonical variants observed:**
  - `NIST RMF (missing 'AI')`: 4 occurrence(s)

- **Top offending files (up to 10):**
  - `part-11-llm-ethics-trust-governance/module-56-responsible-ai-tools/section-56.1.html`: 2 hit(s); NIST RMF (missing 'AI')=2
  - `part-11-llm-ethics-trust-governance/module-55-environmental-sustainability/index.html`: 1 hit(s); NIST RMF (missing 'AI')=1
  - `part-11-llm-ethics-trust-governance/module-56-responsible-ai-tools/section-56.5.html`: 1 hit(s); NIST RMF (missing 'AI')=1

### vLLM (library)

- **Recommended canonical spelling**: `vLLM`
- **Total non-canonical occurrences**: 3
- **Sections affected**: 3
- **Non-canonical variants observed:**
  - `vllm`: 3 occurrence(s)

- **Top offending files (up to 10):**
  - `part-13-llmops-lifecycle/module-65-containers-kubernetes/section-65.4.html`: 1 hit(s); vllm=1
  - `part-13-llmops-lifecycle/module-65-containers-kubernetes/section-65.5.html`: 1 hit(s); vllm=1
  - `part-2-understanding-llms/module-09-inference-optimization/section-9.5.html`: 1 hit(s); vllm=1

### Cross-attention (concept)

- **Recommended canonical spelling**: `cross-attention`
- **Total non-canonical occurrences**: 2
- **Sections affected**: 2
- **Non-canonical variants observed:**
  - `cross attention`: 2 occurrence(s)

- **Top offending files (up to 10):**
  - `part-1-llm-building-blocks/module-02-sequence-models-attention/index.html`: 1 hit(s); cross attention=1
  - `part-1-llm-building-blocks/module-02-sequence-models-attention/section-2.3.html`: 1 hit(s); cross attention=1

### "Attention Is All You Need" (paper title)

- **Recommended canonical spelling**: `Attention Is All You Need`
- **Total non-canonical occurrences**: 2
- **Sections affected**: 2
- **Non-canonical variants observed:**
  - `Attention is all you need`: 2 occurrence(s)

- **Top offending files (up to 10):**
  - `part-1-llm-building-blocks/module-03-transformer-architecture/index.html`: 1 hit(s); Attention is all you need=1
  - `part-1-llm-building-blocks/module-03-transformer-architecture/section-3.8.html`: 1 hit(s); Attention is all you need=1

### PyTorch (library)

- **Recommended canonical spelling**: `PyTorch`
- **Total non-canonical occurrences**: 2
- **Sections affected**: 2
- **Non-canonical variants observed:**
  - `pytorch`: 1 occurrence(s)
  - `Pytorch`: 1 occurrence(s)

- **Top offending files (up to 10):**
  - `part-1-llm-building-blocks/module-03-transformer-architecture/section-3.3.html`: 1 hit(s); pytorch=1
  - `part-12-llm-systems-at-scale/module-61-scale-tools/section-61.2.html`: 1 hit(s); Pytorch=1

### RLHF (method)

- **Recommended canonical spelling**: `RLHF`
- **Total non-canonical occurrences**: 2
- **Sections affected**: 2
- **Non-canonical variants observed:**
  - `rlhf`: 2 occurrence(s)

- **Top offending files (up to 10):**
  - `part-4-training-adaptation/module-18-alignment-rlhf-dpo/section-18.3.html`: 1 hit(s); rlhf=1
  - `part-4-training-adaptation/module-18-alignment-rlhf-dpo/section-18.5.html`: 1 hit(s); rlhf=1

### DPO (method)

- **Recommended canonical spelling**: `DPO`
- **Total non-canonical occurrences**: 2
- **Sections affected**: 2
- **Non-canonical variants observed:**
  - `dpo`: 2 occurrence(s)

- **Top offending files (up to 10):**
  - `part-4-training-adaptation/module-18-alignment-rlhf-dpo/section-18.3.html`: 1 hit(s); dpo=1
  - `part-4-training-adaptation/module-18-alignment-rlhf-dpo/section-18.5.html`: 1 hit(s); dpo=1

### GPT-4 (model)

- **Recommended canonical spelling**: `GPT-4`
- **Total non-canonical occurrences**: 2
- **Sections affected**: 2
- **Non-canonical variants observed:**
  - `gpt-4`: 2 occurrence(s)

- **Top offending files (up to 10):**
  - `part-9-llm-evaluation-observability/module-44-online-eval-observability/section-44.2.html`: 1 hit(s); gpt-4=1
  - `part-9-llm-evaluation-observability/module-44-online-eval-observability/section-44.6.html`: 1 hit(s); gpt-4=1

### HumanEval (benchmark)

- **Recommended canonical spelling**: `HumanEval`
- **Total non-canonical occurrences**: 2
- **Sections affected**: 2
- **Non-canonical variants observed:**
  - `human eval`: 2 occurrence(s)

- **Top offending files (up to 10):**
  - `part-9-llm-evaluation-observability/module-45-tools-of-the-trade/section-45.4.html`: 1 hit(s); human eval=1
  - `part-9-llm-evaluation-observability/module-46-llm-as-judge-automated-evaluation/index.html`: 1 hit(s); human eval=1

### Docker (platform)

- **Recommended canonical spelling**: `Docker`
- **Total non-canonical occurrences**: 1
- **Sections affected**: 1
- **Non-canonical variants observed:**
  - `docker (in prose)`: 1 occurrence(s)

- **Top offending files (up to 10):**
  - `part-10-llm-security-runtime-safety/module-49-agent-safety-autonomy/section-49.4.html`: 1 hit(s); docker (in prose)=1

### Triton (library)

- **Recommended canonical spelling**: `Triton`
- **Total non-canonical occurrences**: 1
- **Sections affected**: 1
- **Non-canonical variants observed:**
  - `triton`: 1 occurrence(s)

- **Top offending files (up to 10):**
  - `part-12-llm-systems-at-scale/module-61-scale-tools/section-61.2.html`: 1 hit(s); triton=1

### Gemini (model)

- **Recommended canonical spelling**: `Gemini`
- **Total non-canonical occurrences**: 1
- **Sections affected**: 1
- **Non-canonical variants observed:**
  - `gemini`: 1 occurrence(s)

- **Top offending files (up to 10):**
  - `part-3-working-with-llms/module-11-llm-apis/section-11.3.html`: 1 hit(s); gemini=1

### LlamaIndex (library)

- **Recommended canonical spelling**: `LlamaIndex`
- **Total non-canonical occurrences**: 1
- **Sections affected**: 1
- **Non-canonical variants observed:**
  - `llamaindex`: 1 occurrence(s)

- **Top offending files (up to 10):**
  - `part-7-retrieval-information-extraction-with-llms/module-36-retrieval-tools/section-36.5.html`: 1 hit(s); llamaindex=1

### Pinecone (vendor/library)

- **Recommended canonical spelling**: `Pinecone`
- **Total non-canonical occurrences**: 1
- **Sections affected**: 1
- **Non-canonical variants observed:**
  - `pinecone`: 1 occurrence(s)

- **Top offending files (up to 10):**
  - `part-7-retrieval-information-extraction-with-llms/module-36-retrieval-tools/section-36.5.html`: 1 hit(s); pinecone=1

### Weaviate (library)

- **Recommended canonical spelling**: `Weaviate`
- **Total non-canonical occurrences**: 1
- **Sections affected**: 1
- **Non-canonical variants observed:**
  - `weaviate`: 1 occurrence(s)

- **Top offending files (up to 10):**
  - `part-7-retrieval-information-extraction-with-llms/module-36-retrieval-tools/section-36.5.html`: 1 hit(s); weaviate=1

### Qdrant (library)

- **Recommended canonical spelling**: `Qdrant`
- **Total non-canonical occurrences**: 1
- **Sections affected**: 1
- **Non-canonical variants observed:**
  - `qdrant`: 1 occurrence(s)

- **Top offending files (up to 10):**
  - `part-7-retrieval-information-extraction-with-llms/module-36-retrieval-tools/section-36.5.html`: 1 hit(s); qdrant=1

### Elasticsearch (library)

- **Recommended canonical spelling**: `Elasticsearch`
- **Total non-canonical occurrences**: 1
- **Sections affected**: 1
- **Non-canonical variants observed:**
  - `Elastic Search`: 1 occurrence(s)

- **Top offending files (up to 10):**
  - `part-7-retrieval-information-extraction-with-llms/module-36-retrieval-tools/section-36.5.html`: 1 hit(s); Elastic Search=1

### BIG-bench (benchmark)

- **Recommended canonical spelling**: `BIG-bench`
- **Total non-canonical occurrences**: 1
- **Sections affected**: 1
- **Non-canonical variants observed:**
  - `BigBench`: 1 occurrence(s)

- **Top offending files (up to 10):**
  - `part-9-llm-evaluation-observability/module-42-evaluation-foundations/index.html`: 1 hit(s); BigBench=1

### OpenTelemetry (standard)

- **Recommended canonical spelling**: `OpenTelemetry`
- **Total non-canonical occurrences**: 1
- **Sections affected**: 1
- **Non-canonical variants observed:**
  - `opentelemetry`: 1 occurrence(s)

- **Top offending files (up to 10):**
  - `part-9-llm-evaluation-observability/module-42-evaluation-foundations/section-42.9.html`: 1 hit(s); opentelemetry=1

### Tokenizer (concept)

- **Recommended canonical spelling**: `tokenizer`
- **Total non-canonical occurrences**: 1
- **Sections affected**: 1
- **Non-canonical variants observed:**
  - `tokeniser`: 1 occurrence(s)

- **Top offending files (up to 10):**
  - `part-9-llm-evaluation-observability/module-44-online-eval-observability/section-44.4.html`: 1 hit(s); tokeniser=1

### GPT-3.5 (model)

- **Recommended canonical spelling**: `GPT-3.5`
- **Total non-canonical occurrences**: 1
- **Sections affected**: 1
- **Non-canonical variants observed:**
  - `gpt-3.5`: 1 occurrence(s)

- **Top offending files (up to 10):**
  - `part-9-llm-evaluation-observability/module-44-online-eval-observability/section-44.6.html`: 1 hit(s); gpt-3.5=1
