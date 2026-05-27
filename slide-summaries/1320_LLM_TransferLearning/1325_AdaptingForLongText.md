# 1325_AdaptingForLongText — Per-Slide Summary

**Source file:** `1325_AdaptingForLongText.pptx`
**Source folder:** `SlidesPool/1320_LLM_TransferLearning/`
**Drive link:** https://drive.google.com/file/d/1FHTSiSP6AGqAQ6GPor9X3qEzwaKkN90c/view
**Slide count (exact, via python-pptx):** 26
**Extraction:** Local parse + slide PNG render. Body bullets and diagrams describe seven methods for handling long-text classification.

---

## Slide 1 — Long Text Representation and Classification
Title slide for the deck on long-text representation and classification.

## Slide 2 — Text classification using Representation Models
Recap diagram of the standard BERT classification pipeline that breaks down for inputs longer than 512 tokens.

## Slide 3 — Method 1: Truncate Text
Truncate the input to the maximum length and hope the first 512 tokens carry enough signal for classification.

## Slide 4 — Method 2: Sliding window and majority vote
Slide a window of size 512 (optionally overlapping), classify each chunk with a BERT-based classifier, and aggregate decisions by majority vote or by averaging logits.

## Slide 5 — Method 3: Hierarchical Transformers
Section divider for the hierarchical-transformer approach.

## Slide 6 — Hierarchical transformer
A three-stage architecture. Encoder: run a sliding window over the long text and embed each window or chunk. Combiner: combine the resulting embedding sequence (mean pooling, transform-then-pool, or RNN). Classifier: apply a small classifier (e.g., logistic regression) to the combined output. The difference from the sliding-window method is that hierarchical combines embeddings before classifying, while sliding-window combines classifier outputs.

## Slide 7 — Hierarchical Transformer Blueprint
A blueprint diagram of the full hierarchical pipeline.

## Slide 8 — Combiners
A diagram catalog of combiner choices (mean pool, transformer, RNN).

## Slide 9 — Classifier
Diagram of the classifier head on top of the combined embedding.

## Slide 10 — Hierarchical Transformer Module
Code screenshot showing the hierarchical transformer module assembled in PyTorch.

## Slide 11 — Inference
Code screenshot showing inference with the hierarchical module.

## Slide 12 — Method 4: Long Sequence Transformers
Section divider for long-sequence transformers.

## Slide 13 — Reminder: Attention Mechanism
Reminder that every token affects every other token by contributing its value vector weighted by the softmax-normalized dot product of key and query.

## Slide 14 — Attention mechanisms
Local sliding-window attention only attends to nearby tokens; dilated sliding window skips every second local token; global attention has a few special tokens (e.g., the first two) attend to all positions.

## Slide 15 — Longformer: Global+Sliding Attention
Longformer combines global attention (on a few special tokens) with local sliding-window attention, supporting up to 4096 tokens.

## Slide 16 — BigBird Transformer: Random Attention
BigBird adds random attention on top of sparse patterns. A batch-level random attention mask is used during training and fixed to a seed during inference. Variants support 4K and 16K tokens.

## Slide 17 — BigBird Transformer
A diagram of BigBird's attention pattern (global plus local plus random).

## Slide 18 — Method 5: Classification with summarization
Section divider for the summarization-first approach.

## Slide 19 — Classification with summarization
First summarize the long input with an LLM, then run representation-based classification on the summary.

## Slide 20 — Method 6: Prompt-based zero-shot classification
Section divider for zero-shot generative classification, dropping the representation phase entirely.

## Slide 21 — Zero-shot classification with OpenAI
Code screenshot showing zero-shot classification via an OpenAI prompt over the long document.

## Slide 22 — Zero-shot classification with T5
Code screenshot showing zero-shot classification using a T5-style prompt.

## Slide 23 — Text Generation with Long Prompts
Section divider for long-prompt text generation.

## Slide 24 — Perceiver Autoregressive
Perceiver-style autoregressive generation for long windows: the latest tokens cross-attend to the long history with complexity M-by-N (N is the last window). The architecture reduces size and dimension and then continues with causal attention only over N tokens in later layers.

## Slide 25 — Method 7: Retrieval Augmented classification
Section divider for retrieval-augmented classification.

## Slide 26 — Retrieval-augmented classification
Summarize and store documents through a RAG pipeline (chunk and embed). At classification time, fetch chunks relevant to the classification task and apply zero-shot generative classification only on the retrieved content.

---

## Deck-level takeaway
The deck catalogs seven ways to push representation-based classification past BERT's 512-token limit. The simplest fixes are surgical to the input: truncate, sliding-window plus aggregation, or summarize-first. The middle methods change the architecture: hierarchical transformers that combine per-chunk embeddings before classifying, and long-sequence transformers that change the attention pattern itself (Longformer's global plus sliding window up to 4K tokens, BigBird's random plus sparse pattern up to 16K). The closing methods sidestep representation entirely: zero-shot prompt-based classification with OpenAI or T5, Perceiver-style autoregressive long-context generation, and retrieval-augmented classification that only ever shows the LLM the relevant chunks.
