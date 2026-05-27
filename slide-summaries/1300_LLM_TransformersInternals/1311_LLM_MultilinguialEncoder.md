# 1311_LLM_MultilinguialEncoder — Per-Slide Summary

**Source file:** `1311_LLM_MultilinguialEncoder.pptx`
**Source folder:** `SlidesPool/1300_LLM_TransformersInternals/`
**Drive link:** https://drive.google.com/file/d/17W5YSzcb0iF_RHUtHh85UxsYElpfQhgx/view
**Slide count (exact, via python-pptx):** 12
**Extraction:** Local parse + slide PNG render. Bullets and code screenshots describe the XLM training pipeline and the Noam learning-rate schedule.

---

## Slide 1 — Multilingual Encoders
Title slide for the deck on multilingual encoder models.

## Slide 2 — XLM Model
XLM is similar to BERT, an encoder model that ingests multilingual input. It is trained on a parallel multilingual corpus, alternating between multilingual pairs (source plus translation) and single sentences across two or many languages. It combines three losses: MLM (Masked Language Modeling on single sentences), CLM (Causal Language Modeling, next-token prediction on single sentences), and TLM (Translation Language Modeling, in which a token in one language is masked and the other language's content is used to recover it, like MLM but cross-lingual).

## Slide 3 — MLM vs. TLM loss
A figure contrasting MLM (recover a masked token using the same sentence) with TLM (recover a masked token using multilingual context).

## Slide 4 — Cross-language pretrained tokenizer
A cross-language tokenizer uses \\w as the token separator unless the token is part of a word, allowing the same vocabulary to handle multiple languages.

## Slide 5 — Noam Optimizer
Section divider for the Noam learning-rate scheduler.

## Slide 6 — Optimizer scheduler: Noam Shazeer's Paper
The Noam schedule increases the learning rate linearly during a warm-up phase, then decreases it proportionally to the inverse square root of the training step number.

## Slide 7 — Noam optimizer
Two screenshots showing the Noam scheduler implementation.

## Slide 8 — Training
Section divider for the training-loop implementation.

## Slide 9 — Batch Class
Three screenshots showing a Batch class that bundles source, target, and masks for the training loop.

## Slide 10 — Training Loop
A code screenshot showing the multilingual training loop using the Batch class and Noam optimizer.

## Slide 11 — Running Translation
A code screenshot running translation inference with the trained model.

## Slide 12 — Example
Four screenshots showing concrete translation examples produced by the model.

---

## Deck-level takeaway
The deck explains XLM, a multilingual encoder trained with three jointly optimized losses (MLM, CLM, and a cross-lingual TLM that masks a token in one language and asks the model to recover it from the other language's content), supported by a shared cross-language tokenizer. The training-loop section covers the Noam learning-rate schedule (linear warm-up then inverse-square-root decay) and walks through a reference PyTorch implementation with a Batch class, training loop, and translation inference, illustrated with end-to-end examples.
