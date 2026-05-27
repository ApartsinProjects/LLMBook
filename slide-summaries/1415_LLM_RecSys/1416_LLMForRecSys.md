# 1416_LLMForRecSys — Per-Slide Summary

**Source file:** `1416_LLMForRecSys.pptx`
**Source folder:** `SlidesPool/1415_LLM_RecSys/`
**Drive link:** https://drive.google.com/file/d/18OGhT1ixwAlkJ5tpSiSzTu8f_0x7vF7H/view
**Slide count (exact, via python-pptx):** 11
**Extraction:** Local parse + slide PNG render. Short conceptual deck; figures illustrate two LLM-powered ranking systems at the end.

---

## Slide 1 — LLM4RecSys
Title slide for the deck on applying LLMs to recommender systems.

## Slide 2 — Recommender Systems Applications
A figure surveying common recommender-system application domains.

## Slide 3 — Recommender Systems
A diagram of a classical recommender system, with users and items as inputs and ranked items as output.

## Slide 4 — Modern Recommendation Systems
A diagram of a modern recommendation system showing the candidate-generation, retrieval, and ranking stages.

## Slide 5 — Feature Extraction: Users and Items
LLMs are used to understand items and users and to extract textual features for classical recommender systems.

## Slide 6 — LLM in Feature Generation
A figure showing the LLM extracting features of users or items.

## Slide 7 — Feature Representation: Users and Items
LLMs can also act as representation models that encode users and items directly into embeddings.

## Slide 8 — Context-Based Candidate Retrieval
Use embedding / dense retrieval over textual representations: embed item descriptions and embed user profile or interaction history, then retrieve nearest items.

## Slide 9 — LLM for Scoring and Ranking
Section divider for LLM-based scoring and ranking.

## Slide 10 — BookGPT: Generative Text Ranking
BookGPT is a generative text-ranking example where the LLM is prompted to produce a ranked list of books.

## Slide 11 — PromptRec: Text2Score Regression
PromptRec frames recommendation as a binary question-answering task ("would the user like this item?"), turning the LLM's yes-probability into a score.

---

## Deck-level takeaway
The deck is a compact tour of three ways LLMs plug into recommender systems. First, as feature extractors that read item or user text and emit structured signals consumable by classical RecSys models. Second, as representation models that embed users and items into a shared dense space for candidate retrieval. Third, as direct scorers and rankers, either via generative ranking (BookGPT) or by framing recommendation as a binary yes/no question whose probability becomes the score (PromptRec).
