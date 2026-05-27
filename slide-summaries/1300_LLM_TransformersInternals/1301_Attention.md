# 1301_Attention — Per-Slide Summary

**Source file:** `1301_Attention.pptx`
**Source folder:** `SlidesPool/1300_LLM_TransformersInternals/`
**Drive link:** https://drive.google.com/file/d/1aT_7l1z0-FrYy5Rqc_DbfwP4CEtQlpU7/view
**Slide count (exact, via python-pptx):** 31
**Extraction:** Local parse + slide PNG render. Body text and the figure-label runs around the attention diagrams carry the conceptual content.

---

## Slide 1 — From Attention to Transformers
Title slide for the deck taking the reader from attention to full transformer blocks.

## Slide 2 — Reminder: Word2Vec
Recap that Word2Vec yields a single embedding per word, and that document representation falls back to mean pooling of word embeddings.

## Slide 3 — Word2vec and Context
Word2Vec assigns each word a single fixed embedding that captures an average meaning across contexts. This loses the contextual nuance of words like "mouse" (computer-and-keyboard vs. cat-and-mouse) or pronouns "he" and "she" whose referents depend on the surrounding text.

## Slide 4 — Attention: Contextualized Embedding
Attention moves the embedding of each word toward a context-dependent point in embedding space, so that the same surface word produces different vectors in different sentences.

## Slide 5 — Attention
A single diagram showing the attention pattern at a high level.

## Slide 6 — Contextualize embeddings of all tokens in a sentence
The toy example "User clicked Mouse" demonstrates that attention takes E1, E2, E3 (per-token embeddings) and produces C1, C2, C3 (contextualized embeddings), so that "Mouse" now represents a computer mouse that has been clicked.

## Slide 7 — Background: Soft lookup
Background diagram explaining attention as a soft (probability-weighted) lookup over value vectors.

## Slide 8 — Queries, Keys and Value Vectors
Each token has three derived vectors. The query asks what the token needs to know about its context ("Mouse" wants to know whether it is an alive creature or an inanimate object). The key advertises what the token can offer ("Clicked" provides action details on static objects). The value is the direction in semantic space that the token contributes to other tokens' context vectors.

## Slide 9 — Query, Key and Value Matrices
A diagram of the W_Q, W_K, W_V projection matrices that turn embeddings into queries, keys, and values.

## Slide 10 — Example: Attention Weight
A worked example computing one attention weight from a query-key dot product.

## Slide 11 — Attention Matrix
The full attention matrix laid out, with rows as queries and columns as keys.

## Slide 12 — Attention In Matrix Form
Two diagrams expressing the attention computation as softmax(QK^T / sqrt(d_k)) V in compact matrix form.

## Slide 13 — Matrix Dimensions
Diagram annotating the matrix dimensions of Q, K, V, and the resulting attention output.

## Slide 14 — Attention: Seq2Seq Embedding Contextualization
Repeats the "User clicked Mouse" example to show attention as a sequence-to-sequence embedding contextualizer.

## Slide 15 — Masked Language Modeling (MLM) Training
Diagram showing how attention plus a classifier head over the context vector of a masked token is used to reconstruct the original token during MLM training.

## Slide 16 — Drop-out layer
Dropout randomly zeros entries of the attention matrix during training, which prevents over-reliance on frequent word combinations.

## Slide 17 — Single Attention Block is Limited
A single attention block can contextualize only within one specific aspect, motivating multi-head attention.

## Slide 18 — Multiheaded Attention
Multi-head attention runs several attention blocks in parallel, each with its own Q, K, V projections, so different heads specialize on different relational aspects.

## Slide 19 — Weight-Splitting in Multiheaded Attention
Instead of separate per-head matrices, the implementation uses a single matrix and splits it along the embedding dimension, which is computationally cheaper while mathematically equivalent.

## Slide 20 — Simple PyTorch Class
A simple PyTorch class implementation of a single-head attention block.

## Slide 21 — Fusion tasks
For tasks like Spanish-to-English translation, the next English token must depend on the entire Spanish input and the English tokens generated so far. The architecture stacks self-attention (contextualize generated English tokens) and cross-attention (contextualize English tokens with Spanish tokens).

## Slide 22 — Cross-Attention vs. Self-Attention
Side-by-side diagrams showing that cross-attention queries the target (English) tokens against keys and values from the source (Spanish) tokens, while self-attention does Q, K, V all from the same sequence.

## Slide 23 — Training Casual Models, Next Token Prediction
Diagram repeating the "User clicked Mouse" example with the next-token prediction interpretation: each context vector feeds a head predicting the next token (clicked, Mouse, Twice).

## Slide 24 — Casual Attention
In autoregressive models, the next token is not yet available when contextualizing the last token. Causal attention trains the model to attend only to past tokens by masking future positions and renormalizing the remaining weights.

## Slide 25 — Dropout Attention Weights
Code-and-figure slide showing dropout applied specifically to the attention weights.

## Slide 26 — Causal Attention Class
A Python class implementing causal attention with the mask and renormalization steps.

## Slide 27 — Implementation
Implementation slide showing the causal attention forward pass.

## Slide 28 — With Weight Splitting
A causal multi-head implementation in which d_out is the desired output dimension and each head's output dimension is d_out / num_heads. The single-matrix-plus-view-and-transpose pattern reduces the number of matrix multiplications because view and transpose are inexpensive.

## Slide 29 — Attention Mechanism: Complexity Analysis
Two diagrams analyzing the time and memory complexity of attention, focusing on the quadratic dependence on sequence length.

## Slide 30 — Sparse attention
Sparse attention restricts the attention span to speed up long inputs and avoid the quadratic blow-up. Variants include full quadratic attention, sliding window (only nearby tokens), dilated sliding window (every second local token), and global attention (a few special tokens, such as the sentence beginning, attend to all positions).

## Slide 31 — Improvements: Add random attention
Adds random-token attention on top of sparse patterns; the intuition is that glancing at a few random tokens helps interpret the current token's semantics without restoring quadratic cost.

---

## Deck-level takeaway
The deck builds attention from first principles. It motivates the need for context-dependent embeddings by contrasting fixed Word2Vec vectors with the obvious contextual ambiguity of words like "mouse". It introduces the query-key-value triple, walks through the soft-lookup picture and the matrix form of scaled dot-product attention, then layers in the engineering necessities: dropout, multi-head splitting via a single matrix, cross-attention for sequence-to-sequence fusion, and causal masking for autoregressive next-token prediction. The closing arc tackles the quadratic-cost problem with sparse and random attention patterns, completing the picture needed to understand modern transformer blocks.
