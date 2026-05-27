# 1123_WordEmbeddings — Per-Slide Summary

**Source file:** `1123_WordEmbeddings.pptx`
**Source folder:** `SlidesPool/1120_LLM_WordsAndTokens/`
**Drive link:** https://drive.google.com/file/d/1XrT2lCSIO_rwyo-94J9TWvPNE8qrXxiB/view
**Slide count (exact, via python-pptx):** 21
**Extraction:** Local parse + slide PNG render. Code-screenshot slides (Gensim usage, song-embedding training) carry illustrative figures while the conceptual content is captured in titles and bullets.

---

## Slide 1 — Word Embedding
Title slide for the lecture on dense word representations.

## Slide 2 — Reminder: One-Hot Word Representation
Recaps the tokenize then build-vocabulary pipeline. A token can be represented by its integer ID or by a one-hot vector at that position.

## Slide 3 — Good representations for ML
Argues that semantically similar inputs (images with similar content, documents on similar topics, words with similar meaning) should have similar representations, and that representations should be dense, keeping length small while preserving semantics. One-hot encoded word representations are sparse and long, and proximity in token ID space has no semantic meaning.

## Slide 4 — Dense word representation / Embedding
Defines an embedding as a real-valued vector of fixed length (for example 700) much smaller than vocabulary size (around 20K), with mostly non-zero entries. Semantically similar words should have similar embeddings, so "dog" should be closer to "cat" than to "car".

## Slide 5 — Idea: Distribution Hypothesis
States the distributional hypothesis: a word is characterized by the company it keeps.

## Slide 6 — Word2Vec: CBOW model
Describes CBOW: start with random embeddings for all words, use the embeddings of surrounding context words to predict the masked center word, and train by minimizing word-classification error.

## Slide 7 — Self-supervised training using large text corpus
Notes that training samples are drawn from a large text corpus, with sampling that respects sentence boundaries to avoid contaminating contexts across sentences.

## Slide 8 — Word2Vec CBOW Model
Walks through the toy example "A cat catches a mouse", showing how the context-to-center prediction is structured and the embedding lookup plus softmax classifier head.

## Slide 9 — Semantic analogies in embeddings space
Demonstrates that arithmetic over embeddings has semantic meaning (king minus man plus woman approx queen) and that directions in embedding space carry meaning (gender, plurality, country-capital).

## Slide 10 — Pretrained Word2Vec in Gensim library
Code screenshots showing how to load pretrained Word2Vec via Gensim and query nearest neighbors.

## Slide 11 — Measuring Similarity in Embedding Space
Defines cosine similarity (angle between query and reference embeddings) and cosmul similarity, which takes positive and negative references and scores by the ratio of products of positive to negative cosine distances.

## Slide 12 — Compare similarity measures
Side-by-side outputs comparing nearest-neighbor results returned by cosine and cosmul similarity.

## Slide 13 — Classification using word embeddings
Document classification via mean-pooled (averaged) word embeddings; works for very short documents like tweets, but better methods using sentence embeddings exist.

## Slide 14 — Word2Vec: Skip-Gram
Skip-Gram inverts CBOW: predict each context word from the target word, creating (context, target) pairs over context windows of 5-15 words. Variants include negative sampling to avoid full-vocabulary softmax, with wrong words receiving low predicted probability.

## Slide 15 — CBOW vs. skip-gram
A side-by-side architecture diagram comparing the two Word2Vec variants.

## Slide 16 — GloVe Embedding
GloVe (Global Vectors for Word Representation) finds embeddings that predict whether two words are frequent neighbors, working from a co-occurrence matrix that counts co-occurrences in a fixed window.

## Slide 17 — GloVe loss
GloVe learns embeddings whose cosine similarity is proportional to log co-occurrence count, minimized through the standard GloVe loss J shown in the figure.

## Slide 18 — Generalized Embeddings
Word2Vec is trained on sequences of tokens, which generalizes beyond language: graphs (tokens are nodes, sequences are walks), music (tokens are chords, sequences are songs), and other token-sequence domains.

## Slide 19 — Example: Song Recommendation
Frames a song-recommendation example: the dataset is playlists of song IDs (no song metadata required), the embedding treats song ID as token and playlist as sequence, and the application recommends songs with similar embeddings.

## Slide 20 — Playlist dataset
Screenshots showing the playlist dataset's row structure and a sample of the song-ID sequences.

## Slide 21 — Train and apply songs embedding model
Five code screenshots showing the full song-embedding pipeline: build the corpus from playlists, train Word2Vec via Gensim, persist the model, query nearest songs to a seed track, and pull recommendation lists.

---

## Deck-level takeaway
The deck introduces dense word embeddings as the alternative to sparse one-hot or count-based representations, motivated by the distributional hypothesis. It covers the two Word2Vec variants (CBOW and Skip-Gram) with negative-sampling, then GloVe as a co-occurrence-matrix-factorization approach. Practical material includes Gensim usage, cosine and cosmul similarity, simple pooled-embedding classification, and the geometric arithmetic that makes analogies work. The closing arc generalizes "embedding a token sequence" beyond language to graph walks and music, illustrating the idea concretely with a song-recommendation pipeline trained on playlists with no audio metadata.
