# 1411_BERTTopics — Per-Slide Summary

**Source file:** `1411_BERTTopics.pptx`
**Source folder:** `SlidesPool/1410_LLM_TopicModeling/`
**Drive link:** https://drive.google.com/file/d/1dfvJvmsyAVNmN_dcsS_y3lK0q2ke6gDH/view
**Slide count (exact, via python-pptx):** 37
**Extraction:** Local parse + slide PNG render. Bullets describe BERTopic's four-stage pipeline and the reranking and visualization tools.

---

## Slide 1 — Text Clustering and Topic Modeling
Title slide for the deck on text clustering and topic modeling.

## Slide 2 — Text Clustering and topic modeling
Group similar texts by meaning and describe each cluster.

## Slide 3 — Topic Modeling Pipeline
The pipeline: embed, reduce dimensionality, cluster, and finally describe clusters with keywords or text.

## Slide 4 — Example: ArXiv Paper Abstracts
Three screenshots introducing the ArXiv abstracts running example.

## Slide 5 — Dimensionality Reduction
Section divider; UMAP (Uniform Manifold Approximation and Projection) is the chosen method.

## Slide 6 — Dimensionality Reduction Methods
A figure listing dimensionality reduction methods; LDA is supervised, the rest are unsupervised.

## Slide 7 — UMAP
UMAP constructs a graph between points by choosing a radius for each point (based on the distance to its n-th nearest neighbor) and connecting two points when their balls overlap in high-dim space. The low-dim graph is then generated to preserve that structure.

## Slide 8 — Clustering
Section divider for clustering.

## Slide 9 — Clustering algorithms
Centroid-based k-means requires a predefined number of clusters. Density-based HDBSCAN does not, and may leave some points as outliers (Hierarchical Density-Based Spatial Clustering of Applications with Noise).

## Slide 10 — HDBSCAN
Two diagrams illustrating HDBSCAN cluster structure.

## Slide 11 — Visualization
Section divider.

## Slide 12 — Visualize in 2D
Cluster in 5D and plot in 2D for visualization.

## Slide 13 — Topic Representation
Section divider.

## Slide 14 — Represent topics by list of keywords
Each topic is represented by a ranked list of keywords.

## Slide 15 — Reminder: Vanilla TF-IDF
TF-IDF downweights very common words ("the", "I") by multiplying counts with an inverse document-frequency weight.

## Slide 16 — Topic representation using c-TF-IDF
Class-based TF-IDF: count term frequency in each cluster, and define cluster representation terms as those frequent in the cluster but infrequent across clusters (highest c-TF-IDF values).

## Slide 17 — IDF for clusters: IDF weighting
Vanilla IDF generalized to clusters. The worked example for 2 clusters computes the average frequency 29 = (9 + 9 + 7 + 22 + 1 + 9 + 1) / 2.

## Slide 18 — Summary: Clustering Pipeline
A figure summarizing the four-stage pipeline plus topic-representation keywords.

## Slide 19 — BERTopic Pipeline
Section divider for the BERTopic library.

## Slide 20 — Modular BERTopic Pipeline
BERTopic is modular with swappable stages: embedding, dimensionality reduction, clustering, and topic representation.

## Slide 21 — Implementation
Three screenshots showing a basic BERTopic implementation.

## Slide 22 — Inspect Topic (Keywords + Their Score)
Three screenshots showing how to inspect topic keywords with scores, find the topic of specific documents, and find similar clusters by similarity.

## Slide 23 — Keyword Reranking
Section divider for keyword reranking (KeyBERT, MMR, LLM Summarization).

## Slide 24 — Topic keyword reranking
The original topic representation is bag-of-words c-TF-IDF, which ignores word semantics. Reranking selects a better representation.

## Slide 25 — Plugin/Stack multiple topic representation blocks
Section divider for stacking multiple representation blocks.

## Slide 26 — KeyBERTInspired
Sub-section divider for KeyBERTInspired.

## Slide 27 — Representation Model: KeyBERTInspired
Embed documents and c-TF-IDF keywords. The cluster embedding is the average of its document embeddings. Compute keyword embeddings (from c-TF-IDF) and rank keywords by similarity to the cluster embedding.

## Slide 28 — Results: KeyBERTInspired
A figure of the resulting reranked keywords.

## Slide 29 — Maximal Marginal Relevance
Sub-section divider for MMR.

## Slide 30 — Maximal Marginal Relevance (MMR)
The previous model may return semantically similar words ("summary" and "summaries"). MMR iteratively selects a word that is similar to the cluster but different from previously selected words.

## Slide 31 — LLM Summarization
Sub-section divider for LLM summarization as topic representation.

## Slide 32 — Implementation
Four screenshots showing an LLM-based topic-summarization implementation.

## Slide 33 — Using OpenAI as a generator
Two screenshots using OpenAI as the summarization generator for topic labels.

## Slide 34 — BERTopic Visualizations
Section divider for visualizations.

## Slide 35 — Interactive Visualization: Documents
Two screenshots of interactive document visualization driven by c-TF-IDF representation.

## Slide 36 — Visualization: Topics
Three screenshots of topic-level visualization. The deck notes that BERTopic can automatically reduce the number of topics based on their embeddings.

## Slide 37 — Visualization with labels
Two screenshots showing topic visualization with human-readable labels.

---

## Deck-level takeaway
The deck explains BERTopic as a modular four-stage pipeline: embed (e.g., with a sentence transformer), reduce dimensionality (UMAP), cluster (HDBSCAN), and represent each topic with keywords (c-TF-IDF, a class-based generalization of TF-IDF). On top of this baseline, several plug-in reranking modules improve keyword quality: KeyBERTInspired (rank by cluster-embedding similarity), MMR (enforce keyword diversity), and LLM-based summarization (e.g., OpenAI generating human-readable labels). The closing section covers BERTopic's interactive document and topic visualizations, including automatic topic-count reduction.
