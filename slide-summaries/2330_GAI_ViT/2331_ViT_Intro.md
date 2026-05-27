# 2331_ViT_Intro — Per-Slide Summary

**Source file:** `2331_ViT_Intro.pptx`
**Source folder:** `SlidesPool/2330_GAI_ViT/`
**Drive link:** https://drive.google.com/file/d/1pOSVQEXiJENohTdbSmvY8EscGiRFfgoF/view
**Slide count (exact, via python-pptx):** 5
**Extraction:** Local parse + slide PNG render. Text bodies were captured directly; the final classification application slide was visually inspected.

---

## Slide 1 — Vision Transformer
Title slide that introduces the Vision Transformer (ViT) family.

## Slide 2 — Tokenizing Image
The slide contrasts how LLMs and ViTs tokenize their inputs. In an LLM, tokens are words or subwords drawn from a finite vocabulary, one-hot encoded at the vocabulary size, then passed through an embedding layer that maps them to dense vectors of fixed size. In ViT, tokens are image patches drawn from a near-infinite vocabulary; the flattened pixels (256 dimensions for a 16x16 patch, or 256x3 for color) are similarly mapped through an embedding layer to fixed-size dense vectors.

## Slide 3 — Patch Embedding
Patch embedding is described as a linear projection W*x, where x is the flattened patch and W is an L-by-256 matrix (L being the embedding dimension); for color 16x16 patches W is L-by-768. The slide makes explicit that the projection is the only learned step between raw patch pixels and the transformer token space.

## Slide 4 — ViT Training
The slide enumerates training regimes. Original ViT is trained supervised on labeled ImageNet, attaching a classification head to the CLS token. Self-supervised regimes include masked autoencoding (reconstructing masked patches via a reconstruction head) and self-distillation as in DINO (cross-entropy between a teacher and a student). The slide notes that there is no semantic relation to text embeddings in these regimes, and the trained model produces both CLS and per-patch token embeddings.

## Slide 5 — ViT Applications: Classification
The slide visually summarizes ViT applied to classification: an input image is split into patches, embedded with positional information, fed through transformer blocks, and the CLS token's embedding is passed to a classification head to produce class probabilities.

---

## Deck-level takeaway
The Vision Transformer reframes image recognition as language modeling over patch tokens. Once patches are flattened, linearly projected, and given positional embeddings, the standard transformer architecture applies. Training can be supervised on ImageNet, self-supervised via masked autoencoding, or self-distilled as in DINO, and downstream classification simply attaches a head to the CLS token.
