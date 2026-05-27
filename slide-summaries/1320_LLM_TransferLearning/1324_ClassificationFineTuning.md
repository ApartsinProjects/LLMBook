# 1324_ClassificationFineTuning — Per-Slide Summary

**Source file:** `1324_ClassificationFineTuning.pptx`
**Source folder:** `SlidesPool/1320_LLM_TransferLearning/`
**Drive link:** https://drive.google.com/file/d/16OW5BqfSh4bnoQcfK2OlnxQPDiQ6uAxn/view
**Slide count (exact, via python-pptx):** 27
**Extraction:** Local parse + slide PNG render. Bullets and code screenshots walk through four fine-tuning recipes for classification.

---

## Slide 1 — Classification-task adaptation of representation models
Title slide for the deck on adapting representation models to classification tasks.

## Slide 2 — Reminder
Two options: keep the representation frozen and train a classification head, or jointly fine-tune the representation and the classification head.

## Slide 3 — Motivation
Lists the four methods covered: joint fine-tuning of representation and classification head, partial fine-tuning with frozen layers, token-level NER fine-tuning, and few-shot SetFit.

## Slide 4 — 1. Joint representation and classification fine-tuning
Section divider for joint fine-tuning.

## Slide 5 — Prepare dataset
Three screenshots showing how to select the underlying model and prepare a batched, padded dataset.

## Slide 6 — Define metrics
Four screenshots defining metrics, preparing the Trainer, and calling trainer.train() for joint fine-tuning.

## Slide 7 — 2. Partial finetuning
Section divider for partial fine-tuning.

## Slide 8 — Partial finetuning
BERT has many layered parameters. Freezing some layers while fine-tuning others is useful because early layers usually capture general features, not task-dependent ones. This reduces training time, compute, and overfitting.

## Slide 9 — Layer Freezing in Python
Five screenshots showing how to print parameters, freeze early layers, and train just the rest.

## Slide 10 — Iteratively adding earlier encoder blocks
Result: iteratively unfreezing earlier encoder blocks shows that the earliest layers do not improve task-specific performance.

## Slide 11 — 3. Fine-Tune BERT for NER
Section divider for NER, a token-level classification task.

## Slide 12 — Named-Entity Recognition
NER identifies tokens belonging to entities: Person (e.g., "Elon Musk"), Organization (e.g., "xAI"), Location (e.g., "California").

## Slide 13 — Need a token-level classification
Diagram showing that NER attaches a classification head per token rather than per sequence.

## Slide 14 — Data preparation
Five screenshots showing the CoNLL-2003 dataset (text token list plus tags per token) and the B/I tagging convention: the first token in the entity is B-Per (begin), other tokens are I-Per (inside), e.g., "Elon Musk" becomes B-Per for "Elon" and I-Per for "Musk".

## Slide 15 — Example tagging
A figure showing example tagged sentences in B/I format.

## Slide 16 — From word labels to token labels
Data is labeled at the word level with no knowledge of the specific tokenizer; subword tokenizers split words (especially unseen named entities, e.g., "Marteen" becomes "Ma + arte + n"). Each subword inherits the parent word's label.

## Slide 17 — Implementation
Three screenshots implementing the word-to-token label mapping.

## Slide 18 — Metrics
Three screenshots showing the seqeval metric for entity-level evaluation, which matches entire tag spans (from B-PER to I-PER) precisely.

## Slide 19 — Fine-Tuning
Four screenshots running the NER fine-tuning loop.

## Slide 20 — Inferencing
Two screenshots running NER inference and post-processing the token-level predictions back into entity spans.

## Slide 21 — End2End classification finetuning with SetFit framework
Section divider for SetFit, an efficient few-shot learning method using sentence transformers.

## Slide 22 — Motivation
With many classes and few training examples per class, fine-tuning multiclass classification directly is hard. SetFit instead generates a binary classification task on pairs (same class vs. different class), fine-tunes the existing sentence transformer, and then uses the fine-tuned representation as features for a multiclass classification head.

## Slide 23 — Step 1: Generate pairs for binary classification
Two screenshots showing the generation of positive (same class) and negative (different class) pairs from the few-shot examples.

## Slide 24 — Step 2: Finetune Using Contrastive Learning
Two screenshots fine-tuning the sentence transformer with contrastive loss on the generated pairs.

## Slide 25 — Step 3: Train a classifier head on finetuned representation
A scikit-learn model or a classification head is trained on top of the fine-tuned embeddings.

## Slide 26 — SetFit Framework: All-in-one
The SetFit framework packages all three steps into one trainer.

## Slide 27 — (no title)
Five screenshots showing an end-to-end SetFit example: 8500 movie reviews total, fine-tuning with 16 documents per class (32 documents total), and a trainer that for each sample generates 20 same-class and 20 different-class pairs, giving 32*40 = 1280 (oversampled) training pairs (or 32*31 = 992 unique ordered pairs, 496 unordered). Logistic regression is used as the default classification head.

---

## Deck-level takeaway
The deck assembles four complementary recipes for adapting representation models to classification. Joint fine-tuning trains everything end-to-end. Partial fine-tuning freezes early layers (which carry general features) to cut compute and overfitting. NER demonstrates token-level classification with the B/I tagging scheme, the word-to-subword label mapping, and the seqeval entity-level metric. SetFit handles the many-classes, few-examples regime by recasting the problem as same-class vs. different-class binary classification on pairs, fine-tuning the sentence transformer with contrastive loss, and finally training a small classifier head on the resulting embeddings.
