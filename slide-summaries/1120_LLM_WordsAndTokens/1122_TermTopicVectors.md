# 1122_TermTopicVectors — Per-Slide Summary

**Source file:** `1122_TermTopicVectors.pptx`
**Source folder:** `SlidesPool/1120_LLM_WordsAndTokens/`
**Drive link:** https://drive.google.com/file/d/1Esgha9pceazkpSpO5IuV7Bg1GSO1yK0V/view
**Slide count (exact, via python-pptx):** 19
**Extraction:** Local parse + slide PNG render. Most slides carry illustrative figures or code rather than detailed body text; structural information comes from titles and short bullets.

---

## Slide 1 — Term and Topic Vectors
Title slide for the deck on classical document representations and topic models.

## Slide 2 — Reminder
A reminder slide showing a single illustration; serves as a context bridge from prior material on tokens and vocabulary.

## Slide 3 — Running example: Movie Review dataset
Introduces the running example, a movie-review dataset with text reviews and sentiment labels, used throughout the deck.

## Slide 4 — BoW: Bag of Words Representation using Counters
Defines bag-of-words as a vector of integers whose length equals the vocabulary size and whose entries are mostly zero. Accompanying images sketch the count-vectorizer output for a small toy vocabulary.

## Slide 5 — Text Classification using Naive Bayes
Frames sentiment classification with C in {pos, neg} on BoW features. The Naive Bayes intuition is that each word votes independently for a class according to its frequency within that class; the second image repeats the same computation for the other value of C.

## Slide 6 — TF-IDF Representation
Defines TF-IDF as a vocabulary-length vector built by fitting both vocabulary and IDF. Higher term frequency means the term matters more in the document; lower inverse-document frequency means the term is less informative because it appears in many documents.

## Slide 7 — Vector-Space Models
Treats the direction of a TF-IDF vector in N-dimensional space as the document's "subject". Document similarity is the angle between TF-IDF vectors. Retrieval applies the same representation to a query: classical search fetches documents through an inverted index and ranks them by TF-IDF similarity.

## Slide 8 — Running example: Wikipedia Comments Dataset
Introduces a second running dataset, Wikipedia comments, used to extend the toy examples.

## Slide 9 — Linear Discriminant Analysis Classifier
Defines LDA as finding a direction in N-dim space along which classes are maximally separated. Four illustrations show class clouds and the optimal projection axis.

## Slide 10 — Evaluating Classification with Confusion Matrix
Reviews the confusion matrix and the derived precision and recall measures through three small example matrices.

## Slide 11 — Topic-Based Document Representation
Critiques word-based features as long, sparse, and ambiguous (synonyms like "artist" and "painter" map to different features; "bank" has multiple senses). Topic vectors are presented as the ideal: shorter, denser, semantically meaningful representations (e.g., 80% sport, 20% news) useful for classification and retrieval. Topics are defined by word statistics where each word contributes to each topic with some weight, and automatic topic extraction is motivated by the observation that frequently co-occurring words belong to the same topic.

## Slide 12 — Automatic Extraction of Implicit Topics
Notes that good topic representations can be learned from data but that the resulting topics are implicit; we can only observe term weights, not assign clean human-readable names. Introduces the two methods covered next: LSA (Latent Semantic Analysis) and LDiA (Latent Dirichlet Allocation).

## Slide 13 — Document-Term Matrix
Defines the document-term matrix (DTM) as an N-by-K matrix with N vocabulary words and K documents, entries holding word-document affinity (presence, count, frequency, or TF-IDF).

## Slide 14 — LSA using DTM decomposition
LSA approximates the DTM by multiplying low-rank matrices, with the rank as a user-selected number of topics. The resulting factors are interpreted as a document-topic matrix and a topic-term matrix, and rows of the document-topic matrix serve as document features. The diagonal importance matrix gives relative topic importance in the corpus; low importance values correspond to noise or less coherent topics.

## Slide 15 — LSA using Truncated SVD
A code/diagram screenshot showing the scikit-learn TruncatedSVD implementation of LSA applied to the document-term matrix.

## Slide 16 — LDA classification using LSA topics
Uses LSA topic features as input to a linear discriminant classifier and reports an evaluation via a train-test split.

## Slide 17 — Latent Dirichlet Allocation
Defines LDiA: each topic is a distribution over words, giving the probability of each word in a document; each document is a mixture of these topic distributions.

## Slide 18 — LDiA for BoW-based DTM
Code screenshots showing how to fit LatentDirichletAllocation on a BoW-based DTM and inspect the resulting topic-word and document-topic distributions.

## Slide 19 — Treat # of topics as a Hyperparameter
Stresses that the number of topics is a hyperparameter and shows how to sweep it (typically via coherence or held-out perplexity) to pick a value that produces clean, interpretable topics.

---

## Deck-level takeaway
The deck walks from classical sparse word-count document representations to learned topic representations. It builds up bag-of-words, TF-IDF, vector-space retrieval, and a Naive Bayes baseline on a movie-review running example, then motivates topic vectors as denser and semantically meaningful alternatives. The second half introduces the document-term matrix and the two main techniques for extracting implicit topics: LSA via truncated SVD and LDiA as a probabilistic mixture-of-distributions model. Topic count is treated as a hyperparameter, and topic features are shown to work as input to standard classifiers like LDA, completing a full pre-neural pipeline for text representation and classification.
