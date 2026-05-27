# 1304_SentenceEmbedding — Per-Slide Summary

**Source file:** `1304_SentenceEmbedding.pptx`
**Source folder:** `SlidesPool/1300_LLM_TransformersInternals/`
**Drive link:** https://drive.google.com/file/d/1WM-Yo9pSKWFLVqBu8xa9YocDhYTfnadm/view
**Slide count (exact, via python-pptx):** 11
**Extraction:** Local parse + slide PNG render. The deck combines short conceptual bullets with code screenshots from the sentence-transformers library.

---

## Slide 1 — Finetune Representation Model for Sentence Embedding
Title slide for the deck on producing sentence embeddings from representation models.

## Slide 2 — Sentence Embedding
Sentence embeddings are needed for short text fragments to drive multiple downstream tasks, with semantically similar sentences placed nearby in embedding space (typically by cosine similarity). BERT's [CLS] token is trained for NSP, not for single-sentence representation. RoBERTa's better practice is mean pooling of context vectors.

## Slide 3 — Reminder
Recaps BERT's MLM plus NSP pretraining and the use of the [CLS] token as a sentence embedding.

## Slide 4 — SBERT: Sentence embedding BERT
BERT trained with Next Sentence Prediction does cross-encoder training: two sentences enter together, so the model is not forced to capture the standalone semantics of any single input. SBERT (Sentence-BERT) in the sentence-transformers library fine-tunes BERT to capture sentence semantics directly, yielding embeddings that are comparable via cosine similarity. The proxy task is Natural Language Inference (NLI); sentence representation is taken as the mean pooling of context vectors.

## Slide 5 — Data: Natural Language Inference
Multi-Genre NLI provides 397,702 annotated sentence pairs (premise, hypothesis, label in {entailment, contradiction, neutral}).

## Slide 6 — Bi-Encoder Training
Bi-encoder training represents premise and hypothesis individually through a siamese architecture with tied weights (each tower receives one sentence) and predicts the NLI relation. The objective encourages semantically similar sentences to cluster together in embedding space.

## Slide 7 — Finetuning SBERT in Python
Five code screenshots showing how to fine-tune SBERT in the sentence-transformers library: load a BERT-based backbone with pooling (not [CLS]) and train on sentence-pair datasets such as NLI.

## Slide 8 — Evaluate Representation: Text Similarity
STSB (Semantic Textual Similarity Benchmark) is a dataset of human-labeled sentence pairs ranked 1-5 for similarity, normalized to [0, 1]. The labels are Mean Opinion Scores from human annotators on 10-20 pairs per source sentence.

## Slide 9 — Similarity evaluation in Python
Code screenshots showing how to create a similarity evaluator and run it on many sentence pairs, computing average similarity and the correlation between predicted and ground-truth similarity scores.

## Slide 10 — Evaluate foundation sentence embedding model on multiple downstream task
The Massive Text Embedding Benchmark (MTEB) covers 8 tasks, 58 datasets, and 112 languages to evaluate foundation sentence embedding models broadly.

## Slide 11 — Multitask evaluation in Python
Two code screenshots showing how to run MTEB-style multitask evaluation in Python.

---

## Deck-level takeaway
The deck explains why a plain BERT [CLS] vector is a poor sentence embedding (it was trained as a cross-encoder for NSP) and how SBERT fixes this through a siamese bi-encoder fine-tuned on NLI sentence pairs with mean-pooled context vectors as the embedding. It then covers evaluation: STSB for semantic similarity (Spearman correlation against human Mean Opinion Scores) and MTEB for broad multitask coverage across 8 tasks, 58 datasets, and 112 languages, with the corresponding Python recipes from the sentence-transformers ecosystem.
