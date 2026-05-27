# 1403_RAG_Evaluations — Per-Slide Summary

**Source file:** `1403_RAG_Evaluations.pptx`
**Source folder:** `SlidesPool/1400_LLM_RAG/`
**Drive link:** https://drive.google.com/file/d/1uWzJx369B30izF0kSmOqa75kKt770o2V/view
**Slide count (exact, via python-pptx):** 19
**Extraction:** Local parse + slide PNG render. The retrieval-metric table and the RAGAS code screenshots carry most of the content.

---

## Slide 1 — RAG Evaluation
Title slide for the deck on evaluating retrieval-augmented generation.

## Slide 2 — Dual Nature of RAG
A RAG system has two core components: retrieval (information-retrieval task) and a generator (NLG task). Evaluation is correspondingly intrinsic (the quality of the intermediate retrieval) and extrinsic (the quality of the final answer).

## Slide 3 — Key Evaluation Dimension
A figure laying out the key dimensions of RAG evaluation across both components.

## Slide 4 — RAG artifacts and quality measures
A figure mapping RAG artifacts (question, retrieved context, answer) to quality measures; groundedness is synonymous with faithfulness.

## Slide 5 — Intrinsic Metrics for Retrieval
A four-row table. Precision@k is the fraction of top-k retrieved documents that are relevant ("how many of the top-k are useful?"). Recall@k is the fraction of all relevant documents that appear in the top-k ("did we find all relevant documents?"). MRR (Mean Reciprocal Rank) is the average reciprocal rank of the first relevant document per query ("how early in the ranking do we find relevance?"). nDCG (Normalized Discounted Cumulative Gain) is a relevance-weighted ranking score discounted by position ("how well are relevant docs ranked overall?").

## Slide 6 — Normalized Discounted Cumulative Gain
DCG sums relevance discounted by log position; IDCG is the DCG for the best possible ranking; nDCG is DCG / IDCG. The underlying user model is exponential judgement of relevance and logarithmic attention decay with position.

## Slide 7 — Extrinsic Metrics For Generation
Reference-based text-generation metrics (BLEU, ROUGE, BERTScore, etc.) require a test set with correct generated responses.

## Slide 8 — Faithfulness metrics
Faithfulness measures whether the answer is grounded in the retrieved context, since an answer can be fluent, relevant, and even correct without being supported by the retrieved evidence. Metrics include token or phrase overlap between context and answer and semantic entailment score using an LLM model.

## Slide 9 — Faithfulness by entailment
Section divider introducing the entailment-based faithfulness recipe.

## Slide 10 — Reminder: Natural Language Inference Model
NLI is a BERT-style cross-encoder trained to predict contradiction, entailment, or neutral between two sentences.

## Slide 11 — Example
Two screenshots showing entailment-based faithfulness scoring on a worked example.

## Slide 12 — Advanced Entailment: Break Answer Into Statements
Two screenshots showing an advanced recipe that breaks the answer into atomic statements and entails each one separately against the context.

## Slide 13 — RAGAS library
RAGAS is a framework for evaluating RAG.

## Slide 14 — Faithfulness using RAGAS library
Three screenshots showing how to compute faithfulness with RAGAS, including the underlying LLM prompt the library uses internally.

## Slide 15 — (no title)
Two screenshots showing the answer relevance recipe RAGAS applies.

## Slide 16 — Answer Relevancy Using RAGAS
A code screenshot computing answer relevancy through RAGAS.

## Slide 17 — Context Relevance Recipe
Three screenshots showing how to evaluate each context chunk with an LLM, asking whether the chunk is relevant for answering the question.

## Slide 18 — Context Relevancy in RAGAS
Two screenshots showing the RAGAS API for context relevancy.

## Slide 19 — RAGAS: Multiple Metrics
Two screenshots showing RAGAS evaluating a RAG output across multiple metrics in one pass.

---

## Deck-level takeaway
The deck separates RAG evaluation into intrinsic retrieval metrics (Precision@k, Recall@k, MRR, nDCG) and extrinsic generation metrics, then focuses on the harder problem of faithfulness, which standard text-generation metrics miss. The recommended recipe uses NLI-style entailment, optionally after breaking the answer into atomic statements scored individually. RAGAS packages all of this (faithfulness, answer relevance, context relevance) behind one library that drives an LLM through carefully crafted prompts, enabling end-to-end RAG quality scoring without per-question gold labels.
