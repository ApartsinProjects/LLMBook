# 1303_TransformerPretraining — Per-Slide Summary

**Source file:** `1303_TransformerPretraining.pptx`
**Source folder:** `SlidesPool/1300_LLM_TransformersInternals/`
**Drive link:** https://drive.google.com/file/d/1FoD0zcHgdHu3HlrANSIP-y1TOfwaqqgb/view
**Slide count (exact, via python-pptx):** 15
**Extraction:** Local parse + slide PNG render. Bullets and inline architecture diagrams carry the conceptual content.

---

## Slide 1 — Pretraining
Title slide announcing pretraining of text generation and representation models.

## Slide 2 — Reminder: Encoder-Only Transformer
Encoder-only transformers like BERT take a fixed-length window (512 for BERT) and pad shorter sequences with a special [PAD] token. The diagram shows T1..T4 tokens going into a transformer-based encoder and yielding C1..C4 context vectors.

## Slide 3 — Pretraining techniques
Two BERT-era pretraining objectives. Masked Language Modeling (MLM) replaces some tokens with [MASK], attaches a classifier head per token output, and asks the model to reconstruct the original tokens. Next Sentence Prediction (NSP) adds a special [CLS] token, encodes a pair of sequences separated by [SEP], and uses a single classifier head over the [CLS] context vector to predict whether the two sentences are related; this forces the [CLS] vector to represent the entire input.

## Slide 4 — Masked Language Modeling
A good token context vector should encode all aspects of the surrounding context. MLM operationalizes that by enabling token recovery from the token context vector.

## Slide 5 — Next Sentence Prediction
NSP forces the [CLS] context vector to summarize the entire input, enabling its use as a text or sentence embedding. An alternative input representation is mean pooling of all context vectors.

## Slide 6 — Class Token as Sentence Embedding
Once trained, the [CLS] token's context vector is used as a sentence embedding for various downstream tasks.

## Slide 7 — Joint training on MLM and NSP
BERT optimizes a combined loss that adds the MLM token-reconstruction loss and the NSP binary classification loss.

## Slide 8 — RoBERTa
RoBERTa (A Robustly Optimized BERT Pretraining Approach) trains only on MLM (no NSP), uses a BPE tokenizer, and is pretrained both on single sentences and sentence pairs. It outperforms BERT.

## Slide 9 — GPT (Decoder-only) Pretraining
Section divider pivoting to decoder-only pretraining.

## Slide 10 — Reminder: Autoregressive Text Generation
Reminder diagram of the autoregressive generation loop: predict next token, append, repeat.

## Slide 11 — GPT Decoder
In a GPT decoder, the per-token context vector is used to predict the next token. A token classification head is attached to each output embedding. The toy example "LLM is Cool" shows C1 from "LLM" feeding a classifier that predicts "is", and C2 from "is" feeding a classifier that predicts "Cool".

## Slide 12 — Dataset Preparation
Training data are shifted text pairs: input is tokens (1..n) and target is tokens (2..n+1), one position ahead.

## Slide 13 — Casual Attention
Without causal masking, attention would use future tokens to contextualize earlier ones, which is inconsistent with autoregressive generation. The attention matrix is masked so that each position can only attend to itself and earlier positions, forcing the model to learn to predict from prior tokens.

## Slide 14 — Casual Attention in Python
A Python code screenshot implementing causal attention masking via a triangular mask plus softmax.

## Slide 15 — Text Generation in Python
A Python code screenshot showing the inference loop that uses the trained decoder to generate text token by token.

---

## Deck-level takeaway
The deck explains the two foundational pretraining recipes that underlie modern LLMs. For encoder-only models (BERT, RoBERTa), the objectives are MLM (reconstruct masked tokens from context) and optionally NSP (predict whether two segments are consecutive), which together force the model to build context vectors rich enough to recover masked content and to summarize the whole input through the [CLS] token. For decoder-only models (GPT), pretraining is autoregressive next-token prediction trained on shifted text pairs with causal attention masking that prevents the model from peeking at future positions, mirroring the inference loop exactly.
