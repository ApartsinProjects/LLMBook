# 1327_LLMMerge — Per-Slide Summary

**Source file:** `1327_LLMMerge.pptx`
**Source folder:** `SlidesPool/1320_LLM_TransferLearning/`
**Drive link:** https://drive.google.com/file/d/1lDaPVloM_28skJ9QdOVC8Oe0BdbBCGEB/view
**Slide count (exact, via python-pptx):** 10
**Extraction:** Local parse + slide PNG render. Body bullets carry the conceptual content for five model-merging strategies and the MergeKit tool.

---

## Slide 1 — Merge LLM
Title slide for the deck on LLM merging.

## Slide 2 — Introduction
After fine-tuning or training multiple models, the standard practice is to compare results and select a single model, discarding the rest. Merging instead combines multiple LLMs into a single model to bring the best of several, cheaply. The limitation is that merging works only across models of the same size and architecture, or across multiple checkpoints of the same model (for example, two BERT models trained on different datasets or with different parameters).

## Slide 3 — Merging strategies
Two families. Parameter-space merging combines the parameters of the source models. Flow-space merging integrates the data flow paths of the source models.

## Slide 4 — 1. Model Soup
Average the weights from multiple models, either uniformly or with weights chosen by grid search or gradient-based training. Greedy soup iteratively selects the next best model to merge and averages only the selected set.

## Slide 5 — 2. SLERP: Spherical Linear Interpolation
SLERP merges only two models at a time. Linear interpolation in high-dimensional space follows a straight line and shrinks vector magnitude. Spherical interpolation walks along the sphere, changing direction instead of magnitude, which preserves geometry better for high-dim weight vectors.

## Slide 6 — 3. Task Arithmetic
Start from a generic pretrained model and fine-tune on a specific task (classification, summarization, etc.). The task vector is the difference between the source and the fine-tuned weights. Task vectors can be added or subtracted to manipulate model capability. Task analogy example: formality = Formal - Base, medical domain = Med, formal medical = Med + (Formal - Base).

## Slide 7 — 4. TIES: TRIM, Elect Sign and Merge
TIES has three steps. Trim identifies the top k% most significant changes during fine-tuning of each source model. Elect Sign handles the case where different deltas pull a weight in opposite directions (average effect can be zero) by creating a per-weight voting sign vector. Merge keeps only the model or models in the majority for each weight, and the choice can be made per layer (different source per layer).

## Slide 8 — 5. Frankenmerging
Frankenmerging stacks pieces of different models (layer stacking, pass-through), assembling parts from multiple donor models into a single architecture.

## Slide 9 — MergeKit
MergeKit is the practical tool: a configuration is defined in a YAML file and applied with a command-line invocation (`mergekit-yaml config.yaml merge --copy-tokenizer --allow-crimes --out-shard-size 1B --lazy-unpickle`). Configuration values support a progressive blend across depth, for example keeping early layers mostly from the base model.

## Slide 10 — Historical Perspective
Model merging was a novel, attractive idea (improve models for free), but it turned out not to be very helpful in practice. It survives mainly for checkpoint averaging (variance reduction during training) and as a hobbyist activity.

---

## Deck-level takeaway
The deck surveys LLM merging as a cheap alternative to fine-tuning or ensemble selection. Parameter-space strategies span simple uniform or greedy weight averaging (Model Soup), pairwise spherical interpolation (SLERP), arithmetic over task-vector deltas (Task Arithmetic), and a Trim + Elect-Sign + Merge pipeline (TIES). A flow-space strategy (Frankenmerging) stitches layers from different donor models into a new stack. MergeKit packages all these recipes behind a YAML configuration and a single command-line invocation. The deck closes honestly: despite its promise, merging proved less useful than hoped, and now survives mainly for checkpoint averaging and enthusiast experimentation.
