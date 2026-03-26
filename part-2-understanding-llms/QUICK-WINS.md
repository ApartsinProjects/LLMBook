# Part II Quick Wins: Top 20 Small-Effort, High-Impact Fixes

**Date:** 2026-03-26
**Scope:** Modules 06, 07, 08 (15 sections total)

Each fix below can be completed in under 30 minutes. Where possible, exact text or HTML to insert is provided.

---

## 1. Add cross-reference to Module 04 at the top of Section 8.2 (KV Cache)

**File:** `module-08-inference-optimization/section-8.2.html`
**Where:** After the Big Picture callout, before the first content paragraph.
**Insert:**

```html
<div class="note-callout">
<strong>Prerequisite refresher:</strong> This section builds on the self-attention mechanism covered in Module 04 (Transformer Architecture). Recall that each attention layer computes query, key, and value projections for every token, and that keys and values from all previous tokens must be retained during autoregressive generation.
</div>
```

---

## 2. Add cross-reference to Section 6.3 in Section 7.3 (Reasoning Models)

**File:** `module-07-modern-llm-landscape/section-7.3.html`
**Where:** First mention of Chinchilla scaling laws or compute-optimal training.
**Find:** The sentence that references Chinchilla or Kaplan scaling laws.
**Insert after that sentence:**

```
(For the full derivation of compute-optimal scaling, see Section 6.3: Scaling Laws and Compute-Optimal Training.)
```

---

## 3. Add cross-reference to Section 7.2 in Section 8.2 for GQA/MLA

**File:** `module-08-inference-optimization/section-8.2.html`
**Where:** First mention of GQA (Grouped-Query Attention).
**Insert after the first sentence introducing GQA:**

```
(GQA's architectural design and its role in models like Llama 3 were introduced in Section 7.2; here we focus on its memory optimization implications.)
```

---

## 4. Add forward reference from Section 7.2 to Section 8.2 for GQA/MLA

**File:** `module-07-modern-llm-landscape/section-7.2.html`
**Where:** End of the GQA/MLA discussion subsection.
**Insert:**

```html
<div class="note-callout">
<strong>Looking ahead:</strong> We return to the memory optimization implications of GQA and MLA in Section 8.2, where we quantify the KV cache savings these architectures provide during inference.
</div>
```

---

## 5. Add "last updated" note to Section 7.1 pricing tables

**File:** `module-07-modern-llm-landscape/section-7.1.html`
**Where:** Immediately above each pricing comparison table.
**Insert:**

```html
<p class="note-callout"><strong>Note:</strong> Pricing as of early 2025. LLM API pricing changes frequently; check provider websites for current rates.</p>
```

---

## 6. Add MLA worked numerical example to Section 7.2

**File:** `module-07-modern-llm-landscape/section-7.2.html`
**Where:** In the MLA explanation subsection, before the code block.
**Insert:**

```html
<div class="key-insight-callout">
<strong>Making the numbers concrete:</strong> Standard multi-head attention with 128 heads and d_head = 128 caches 128 x 128 = 16,384 values per layer per token. MLA compresses all of this into a single 512-dimensional latent vector. Compression ratio: 512 / 16,384 = 3.1%, meaning a 97% reduction in per-token KV cache storage.
</div>
```

---

## 7. Add "optimizer is bigger than the model" aha-moment to Section 6.5

**File:** `module-06-pretraining-scaling-laws/section-6.5.html`
**Where:** After the Adam memory analysis paragraph (where 16 bytes/param is discussed).
**Insert:**

```html
<div class="key-insight-callout">
<strong>Key Insight: Your optimizer is bigger than your model.</strong> A 7B-parameter model in FP16 occupies 14 GB. But Adam stores two additional FP32 state tensors (momentum and variance) per parameter, consuming 7B x 4 x 2 = 56 GB. The optimizer states alone are 4x the model size. This is why memory-efficient optimizers and FSDP are not optional for large-scale training.
</div>
```

---

## 8. Add "97% of internet data is filtered out" aha-moment to Section 6.4

**File:** `module-06-pretraining-scaling-laws/section-6.4.html`
**Where:** After the data pipeline diagram or at the start of the quality filtering discussion.
**Insert:**

```html
<div class="key-insight-callout">
<strong>Key Insight: 97% of the internet is not worth training on.</strong> A typical web crawl starts at 100+ TB of raw HTML. After deduplication, quality filtering, and domain mixing, the final training dataset is often 3 TB or less. The vast majority of web content is boilerplate, spam, near-duplicates, or low-quality text that would degrade model performance.
</div>
```

---

## 9. Promote R1-Zero emergent reasoning to Key Insight callout in Section 7.3

**File:** `module-07-modern-llm-landscape/section-7.3.html`
**Where:** Find the existing Note callout about R1-Zero discovering chain-of-thought.
**Replace the `note-callout` class with `key-insight-callout` and strengthen:**

```html
<div class="key-insight-callout">
<strong>Key Insight: Reasoning from pure RL, zero human examples.</strong> DeepSeek-R1-Zero demonstrates that a language model trained with only reinforcement learning (no supervised chain-of-thought examples) spontaneously discovers structured reasoning behaviors, including self-verification and backtracking. This is arguably the most scientifically surprising finding in recent LLM research: complex reasoning can emerge from reward signals alone.
</div>
```

---

## 10. Promote MoE economics to Key Insight callout in Section 7.2

**File:** `module-07-modern-llm-landscape/section-7.2.html`
**Where:** Find the existing Note callout about MoE capacity vs. compute.
**Replace the `note-callout` class with `key-insight-callout` and strengthen:**

```html
<div class="key-insight-callout">
<strong>Key Insight: MoE decouples knowledge from compute.</strong> DeepSeek V3 stores 671B parameters of knowledge but activates only 37B parameters per token. This means it has the capacity of a 671B-parameter dense model while running at roughly the speed and cost of a 37B-parameter model. MoE lets you scale what the model knows without proportionally scaling what it costs to run.
</div>
```

---

## 11. Elevate "tokenization tax" to Key Insight in Section 7.4

**File:** `module-07-modern-llm-landscape/section-7.4.html`
**Where:** Find the existing Warning callout about tokenization cost disparity.
**Replace the `warning-callout` class with `key-insight-callout`:**

```html
<div class="key-insight-callout">
<strong>Key Insight: The tokenization tax.</strong> A Khmer user may need 6x more tokens than an English user to express the same meaning. This means they pay 6x more per API call, receive 6x shorter responses within the same token budget, and experience 6x slower generation. Tokenizer design is not a neutral technical choice; it directly determines who benefits from language model capabilities and who is underserved.
</div>
```

---

## 12. Add FLOPs vs. FLOPS inline note to Section 6.3

**File:** `module-06-pretraining-scaling-laws/section-6.3.html`
**Where:** First use of "FLOPs" in the section text.
**Insert parenthetical after the term:**

```
FLOPs (floating-point operations, a count; not to be confused with FLOPS, which measures operations per second)
```

---

## 13. Add TTT distinction from fine-tuning in Section 8.2

**File:** `module-08-inference-optimization/section-8.2.html`
**Where:** The TTT (Test-Time Training) paragraph in the Research Frontiers subsection.
**Append to existing paragraph:**

```
Unlike fine-tuning, which permanently updates model weights for reuse across many requests, TTT creates temporary weight updates for a single inference request. The model compresses long-context information into these ephemeral weights, then discards them entirely once generation is complete. This makes TTT a form of adaptive inference rather than a training procedure.
```

---

## 14. Add speculative decoding "draft and editor" analogy to Section 8.3

**File:** `module-08-inference-optimization/section-8.3.html`
**Where:** After the Big Picture callout, before the mathematical treatment.
**Insert:**

```html
<div class="note-callout">
<strong>Intuition:</strong> Think of speculative decoding like a junior writer drafting several paragraphs quickly, then handing them to a senior editor who reviews everything in one pass. The editor accepts most of the draft, fixes a few sentences, and the result is exactly what the editor would have written alone, just produced much faster because reviewing is cheaper than writing from scratch.
</div>
```

---

## 15. Add quantization "color depth" analogy to Section 8.1

**File:** `module-08-inference-optimization/section-8.1.html`
**Where:** After the Big Picture callout, before the mathematical treatment of quantization.
**Insert:**

```html
<div class="note-callout">
<strong>Intuition:</strong> Quantization is like reducing the color depth of an image. A photo in 24-bit color uses 16.7 million distinct colors. Reduce it to 8-bit (256 colors) and the image is 3x smaller with barely visible quality loss. Reduce further to 4-bit (16 colors) and you start to see artifacts, but the image remains recognizable. Model quantization works the same way: reducing the precision of each weight from 16-bit to 4-bit shrinks the model 4x, with a small and often acceptable quality tradeoff.
</div>
```

---

## 16. Add forward pointer from Section 6.3 to inference-time scaling in 7.3

**File:** `module-06-pretraining-scaling-laws/section-6.3.html`
**Where:** At the end of the section, in or after the Key Takeaways.
**Insert:**

```html
<div class="note-callout">
<strong>Where this leads next:</strong> The scaling laws in this section govern training-time compute allocation. But scaling laws also apply at inference time: spending more compute during generation (via search, verification, and chain-of-thought) can dramatically improve output quality. We explore this frontier in Section 7.3 (Reasoning Models and Test-Time Compute).
</div>
```

---

## 17. Add transition paragraph from Section 7.3 to 7.4

**File:** `module-07-modern-llm-landscape/section-7.3.html`
**Where:** At the very end of the section, after Key Takeaways but before the bottom navigation.
**Insert:**

```html
<div class="note-callout">
<strong>What comes next:</strong> Having surveyed the cutting-edge reasoning capabilities of modern LLMs, we now ask a critical question: who benefits from these advances? Section 7.4 examines the multilingual landscape, revealing how tokenizer design, training data composition, and evaluation methodology determine whether 6.5 billion non-English speakers receive equitable access to language model capabilities.
</div>
```

---

## 18. Add Section 8.2 opening hook improvement

**File:** `module-08-inference-optimization/section-8.2.html`
**Where:** The opening paragraph of the section (after the Big Picture callout).
**Prepend to existing opening paragraph:**

```
You quantized your model to 4-bit and slashed its memory footprint by 4x. But inference is still slow, and GPU memory is still filling up. Why? Because the KV cache, not the model weights, has become your bottleneck.
```

---

## 19. Add code output note to Section 6.7 task vector code

**File:** `module-06-pretraining-scaling-laws/section-6.7.html`
**Where:** Before or after the task vector extraction code block.
**Insert:**

```html
<div class="warning-callout">
<strong>Note:</strong> This code example is conceptual and requires downloading a language model (e.g., GPT-2) to run. The purpose is to illustrate the task vector extraction logic, not to provide a standalone runnable script. A full working version would need approximately 500 MB of model weights.
</div>
```

---

## 20. Add model size note to Section 7.3 DeepSeek-R1-Distill code

**File:** `module-07-modern-llm-landscape/section-7.3.html`
**Where:** Before or as a comment in the code block that uses `deepseek-ai/DeepSeek-R1-Distill-Qwen-7B`.
**Insert as a note above the code block:**

```html
<div class="note-callout">
<strong>Resource requirements:</strong> The DeepSeek-R1-Distill-Qwen-7B model requires approximately 14 GB of disk space (BF16 weights) and at least 16 GB of GPU memory for inference. On first run, the model will be downloaded from Hugging Face Hub.
</div>
```

---

## Summary

| # | Section | Type | Effort |
|---|---------|------|--------|
| 1 | 8.2 | Cross-reference to Module 04 | 5 min |
| 2 | 7.3 | Cross-reference to Section 6.3 | 5 min |
| 3 | 8.2 | Cross-reference to Section 7.2 (GQA) | 5 min |
| 4 | 7.2 | Forward reference to Section 8.2 (GQA) | 5 min |
| 5 | 7.1 | "Last updated" note on pricing | 5 min |
| 6 | 7.2 | MLA numerical example | 10 min |
| 7 | 6.5 | Optimizer memory aha-moment | 10 min |
| 8 | 6.4 | Data filtering aha-moment | 5 min |
| 9 | 7.3 | R1-Zero promoted to Key Insight | 10 min |
| 10 | 7.2 | MoE economics promoted to Key Insight | 10 min |
| 11 | 7.4 | Tokenization tax promoted to Key Insight | 10 min |
| 12 | 6.3 | FLOPs vs. FLOPS note | 2 min |
| 13 | 8.2 | TTT vs. fine-tuning distinction | 10 min |
| 14 | 8.3 | Speculative decoding analogy | 5 min |
| 15 | 8.1 | Quantization analogy | 5 min |
| 16 | 6.3 | Forward pointer to inference scaling | 5 min |
| 17 | 7.3 | Transition paragraph to 7.4 | 5 min |
| 18 | 8.2 | Opening hook improvement | 5 min |
| 19 | 6.7 | Code example resource note | 5 min |
| 20 | 7.3 | Model size requirement note | 5 min |

**Total estimated time for all 20 fixes: approximately 2.5 hours**
**Impact: addresses findings from all 5 review reports; touches 12 of 15 sections**
