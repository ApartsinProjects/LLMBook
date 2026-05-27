# 1322_PromptTuning — Per-Slide Summary

**Source file:** `1322_PromptTuning.pptx`
**Source folder:** `SlidesPool/1320_LLM_TransferLearning/`
**Drive link:** https://drive.google.com/file/d/1ze3Xi-fL5qJkCEnDILP_vlgaTAc4XUNL/view
**Slide count (exact, via python-pptx):** 12
**Extraction:** Local parse + slide PNG render. Bullets and code screenshots cover the soft-prompt mechanic and two HuggingFace examples.

---

## Slide 1 — P-Tuning
Title slide for the deck on prompt tuning (P-Tuning).

## Slide 2 — Reminder: Prompt Tuning
Prompts have a significant effect on LLM performance. Text-generation prompts are tokens used to give instructions or context; representation prompts are prefix tokens for BERT. Prompt search uses either manual trial-and-error with best practices and evaluation, or DSPy's Teleprompter that automatically rewrites the prompt via an LLM and evaluates against held-out examples.

## Slide 3 — Soft (Continuous) Prompt
A conventional prompt is a discrete token sequence (one-hot then embedded). A soft prompt directly supplies a sequence of embeddings, "virtual words" that have embeddings but no string in vocabulary. The question is whether soft prompts can be tuned per task to improve performance.

## Slide 4 — Prompt Encoder
A few trainable parameters are added to the model's input embedding layer (virtual tokens), placed not necessarily as a prefix but in any template position. The prompt encoder maps virtual tokens to the expected embedding before they feed into the frozen model. Training optimizes task-specific accuracy and saves the soft prompts per task.

## Slide 5 — Readability estimation
Section header for the first PyTorch example, where readability estimation is framed as a regression task.

## Slide 6 — Dataset for regression
Three screenshots showing the readability regression dataset (text with a numeric readability score).

## Slide 7 — Extend Embedding Layer with Soft Prompts
Initialize the soft prompts from random values or from existing embeddings (for example, the last n tokens in the vocabulary). The same prefix is applied to all batch examples by repeating B times along the batch dimension and once along sequence and embedding dimensions.

## Slide 8 — Replace embedding layer in BERT
The embedding layer in BERT is replaced with the prompt-extended version, then training proceeds while all weights except the prompt encoding are frozen.

## Slide 9 — Prompt Tuning for semantic similarity
Section header for the second HuggingFace example, prompt-tuning for sentence similarity.

## Slide 10 — Sentence Similarity Dataset
Screenshot of the sentence-similarity dataset used.

## Slide 11 — Base Model with Prompt Encoder
Two screenshots showing the HuggingFace PEFT configuration class for soft prompts; only 10*128 parameters are trained.

## Slide 12 — Training
Code screenshot running the training loop over the soft prompts.

---

## Deck-level takeaway
Prompt tuning (P-Tuning) freezes the entire base model and learns a small number of "virtual" continuous prompt embeddings that are prepended (or inserted) to the input. Two implementations illustrate the idea: a PyTorch readability-regression example that replaces BERT's embedding layer with a soft-prompt-extended version and trains only the prompt parameters, and a HuggingFace PEFT example on sentence similarity that trains just 10*128 prompt parameters. The deck positions prompt tuning as a complement to LoRA, useful when even LoRA is too costly and a per-task delta of a few thousand parameters suffices.
