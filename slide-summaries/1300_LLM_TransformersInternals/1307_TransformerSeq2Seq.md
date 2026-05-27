# 1307_TransformerSeq2Seq — Per-Slide Summary

**Source file:** `1307_TransformerSeq2Seq.pptx`
**Source folder:** `SlidesPool/1300_LLM_TransformersInternals/`
**Drive link:** https://drive.google.com/file/d/15IhZXEEBuEqIKvqfgQ851F4fJlxsasaS/view
**Slide count (exact, via python-pptx):** 14
**Extraction:** Local parse + slide PNG render. Bullets and code screenshots map directly onto an annotated PyTorch encoder-decoder reference implementation.

---

## Slide 1 — Seq2Seq Transformers
Title slide for the deck on training transformers for machine translation.

## Slide 2 — Reminder: Transformers
A reminder figure of the canonical transformer architecture.

## Slide 3 — Reminder: Cross-Attention
A reminder figure of the cross-attention pattern in which queries come from the decoder and keys / values come from the encoder.

## Slide 4 — Reminder: Autoregressive Decoder
A reminder figure of the autoregressive decoding loop.

## Slide 5 — Encoder-Decoder Use Case: Translation
For French-to-English translation, the encoder produces a context vector for each French token, and the decoder autoregressively generates English tokens using the French encoding via cross-attention.

## Slide 6 — Cross-Attention for Translation
Two diagrams showing how decoder queries attend to encoder keys and values during translation.

## Slide 7 — Encoder-Decoder Architecture
The full encoder-decoder transformer architecture diagram.

## Slide 8 — Encoder-Decoder Implementation
Section divider that introduces the code-level implementation that follows.

## Slide 9 — Residual Class
A standard residual connection class parametrized by the actual sublayer: run layer norm, run the sublayer, add dropout, return the residual sum.

## Slide 10 — Decoder Layer
A decoder layer has three residual blocks: self-attention, cross-attention, and feed-forward. Memory holds the source of K and V for cross-attention; tgt_mask is the causal mask for the decoder; src_mask blocks padding tokens.

## Slide 11 — Decoder
The decoder receives two masks (a causal mask for the target and a padding mask for the source) plus the encoder output as memory.

## Slide 12 — Mask functions
A figure of the helper mask functions (causal and padding masks) used by the decoder.

## Slide 13 — Encoder-Decoder Transformer
The top-level encoder-decoder transformer class assembled from the previous components.

## Slide 14 — Label Smoothing
Standard cross-entropy on a one-hot target encourages the model to assign all probability mass to a single class, leading to overconfidence and a kind of memorization. Label smoothing assigns a small probability to other classes in the ground truth, acting as regularization.

---

## Deck-level takeaway
The deck builds an encoder-decoder (seq2seq) transformer for machine translation step by step. After three reminders on attention, cross-attention, and autoregressive decoding, it walks through a reference PyTorch implementation: a generic Residual class, a Decoder Layer that wires self-attention, cross-attention, and feed-forward via residuals plus the two required masks (causal target mask, source padding mask), the full Decoder, the mask helpers, the assembled encoder-decoder transformer, and a closing slide on label smoothing as a regularizer against overconfident next-token predictions.
