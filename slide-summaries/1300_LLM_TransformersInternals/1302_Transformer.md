# 1302_Transformer — Per-Slide Summary

**Source file:** `1302_Transformer.pptx`
**Source folder:** `SlidesPool/1300_LLM_TransformersInternals/`
**Drive link:** https://drive.google.com/file/d/1YGMM-8BDmvWVqJ3pj96JXyTA0k9FLqKK/view
**Slide count (exact, via python-pptx):** 22
**Extraction:** Local parse + slide PNG render. Code/diagram-heavy.

---

## Slide 1 — Transformers
Title slide for the lecture that builds a transformer block from its parts and then stacks blocks into the full architecture.

## Slide 2 — Reminder
Recap of *multi-headed attention* from the previous lecture, the attention mechanism this deck assumes the reader already understands.

## Slide 3 — Building Transformer
Roadmap slide listing what the deck will assemble: a *transformer block* (multi-headed attention — both causal and non-causal — plus a feed-forward network, normalization, and residual connections) and the *encoding* layer (learnable embeddings plus position encoding).

## Slide 4 — Transformer Block
Section divider before the block walkthrough.

## Slide 5 — Feedforward layer
The first new component after attention. Multi-headed attention outputs a concatenated context vector per token; the feed-forward layer blends information across heads and is applied *individually to each output token*. Structure: expand (a linear up-projection), nonlinear transform, contract (a linear down-projection) — the canonical "wide hidden, narrow input/output" MLP shape.

## Slide 6 — Activation function
The nonlinearity inside the feed-forward layer. Two prose intuitions are given. ReLU: "pass the input if positive (above threshold)". GeLU: "smooth gating, scale by the 'positiveness'; keep information on small negative values." This is the classical motivation for why GeLU is now the default in transformer FFNs.

## Slide 7 — Feed Forward Python
Two code screenshots implementing the FFN in PyTorch — the expand-act-contract MLP from slides 5–6 made concrete.

## Slide 8 — Residual Connections
Output of the block is the sum of layer input and layer output. The motivation is stabilizing training by preventing vanishing gradients.

## Slide 9 — Layer Normalization
Normalize each output token's content vector to zero mean and unit variance, then apply a learnable shift (β) and scale (γ). Mean and variance are computed *per output token* (per-position, per-layer); γ and β are per-layer parameters. The motivation is stabilizing training by preventing exploding gradients — paired with residuals (slide 8), this gives the gradient-stable training behavior transformers rely on.

## Slide 10 — Transformer block (assembled)
The MLP is applied independently to each token vector. A composite diagram (one embedded image) shows the assembled block with attention + FFN + residuals + norms.

## Slide 11 — Pre-Norm vs. Post-Norm Blocks
A subtle but important architectural choice. In *pre-norm*, normalization is applied before each sub-layer and residual connections form a clear identity path for gradients ("identity + the rest"); norms live on the residual path. Pre-norm is easier to train precisely because gradients can flow through the identity path without crossing a layer-norm. This is now the dominant choice in modern LLMs.

## Slide 12 — Transformer Block in Python
Two code screenshots assembling the full transformer block in PyTorch — the conceptual block from slide 10 in actual code.

## Slide 13 — Input Embeddings
Section divider before the embedding/positional-encoding layer.

## Slide 14 — Learnable embeddings
The transformer block receives a *sequence of embedding vectors*. A single embedding matrix (shape vocab × d_model), learned jointly with the model, transforms each token ID into its vector. Represented as a single matrix multiply on a one-hot row.

## Slide 15 — Positional Embedding
The embedding layer maps each token ID to a single vector regardless of where it sits in the sequence — but position obviously matters: "Cats love dogs" ≠ "Dogs love cats". The fix is to add a *position embedding* to the token embedding. The position embedding learns a vector for each position index in the sequence.

## Slide 16 — Relative Position Embedding
Absolute position embedding forces a maximum sequence length at training time. *Relative* position embedding encodes the offset between two tokens instead of their absolute index, making nearby positions similar by construction and allowing generalization to sequences longer than those seen during training.

## Slide 17 — Transformer
Section divider before stacking blocks into the full network.

## Slide 18 — Transformer (stacked)
A series of transformer blocks (GPT-1 used 12). The diagram shows the stack from input embeddings up through the blocks to the output.

## Slide 19 — Transformers Architectures
Three flavors of transformer assembly. *Encoder-only* (BERT-style): representation models. *Decoder-only* (GPT-style): autoregressive text generation, based on causal attention. *Encoder-Decoder* (T5-style): text-to-text models based on cross-attention between encoder outputs and decoder inputs.

## Slide 20 — Pretraining of transformer models
The corresponding pretraining objectives. *Autoregressive* (GPT = Generative Pretrained Transformer): decoder-only, pretrained with next-token prediction. *Bidirectional* (BERT = Bidirectional Encoder Representation): encoder-only, pretrained with Masked Language Modeling and Next Sentence Prediction.

## Slide 21 — Training with token classification head
The training-time setup: predict the next token (autoregressive decoder) or reconstruct masked tokens (encoder). The diagram shows the classification head sitting on top of the per-token output vectors.

## Slide 22 — Transformer Decoder in Python with the next-token prediction head
Concluding code screenshot: the full decoder stack plus the next-token-prediction head as a PyTorch model — the artifact built up across the whole deck.

---

## Deck-level takeaway

A 22-slide constructive build of the transformer from its components: feed-forward + activation + residuals + norms (with the Pre-Norm vs. Post-Norm choice called out as a load-bearing decision) for the *block*, learnable + positional (absolute / relative) embeddings for the *input*, and three flavors (encoder-only / decoder-only / encoder-decoder) for the *full architecture*. Each conceptual slide is paired with a Python code screenshot so the reader sees both the diagram and the working implementation. The pedagogical signature is "every architectural choice is traced to the optimization problem it solves": residuals → vanishing gradients, layer-norm → exploding gradients, pre-norm → cleaner gradient paths, relative-position → variable-length generalization.
