# Chapter Plan: Module 03 - Sequence Models & the Attention Mechanism

## Scope

**What this chapter covers:**
The historical and conceptual arc from recurrent neural networks to the attention mechanism. The chapter begins with the workhorse of early sequence modeling (the RNN), exposes its mathematical and practical bottlenecks, introduces attention as the breakthrough solution, and culminates in the formalized query/key/value framework with multi-head attention. By the end, students will have implemented attention from scratch and will be fully prepared to study the Transformer architecture in Module 04.

**What this chapter does NOT cover:**
- The full Transformer architecture (Module 04)
- Positional encodings (introduced alongside the Transformer in Module 04)
- Efficient attention variants (linear attention, sparse attention, FlashAttention) beyond a brief mention that they exist
- Convolutional approaches to sequence modeling (TCN, WaveNet)
- Detailed training recipes or hyperparameter tuning for RNN-based models
- Production deployment of seq2seq systems

**Target length:** ~10,000 to 13,000 words across all three sections combined.

## Learning Objectives

1. Explain how RNNs process sequences step by step, including the role of the hidden state as a compressed memory
2. Describe the vanishing and exploding gradient problems, and explain why they limit RNN effectiveness on long sequences
3. Explain how LSTM and GRU gating mechanisms mitigate the vanishing gradient problem
4. Derive Bahdanau additive attention and Luong dot-product attention, explaining the motivation behind each design choice
5. Define the query, key, value abstraction and compute scaled dot-product attention from first principles
6. Implement multi-head self-attention in PyTorch, including causal masking for autoregressive generation
7. Analyze the O(n^2) time and memory complexity of self-attention and explain why it limits context length

## Prerequisites

Students should have completed:
- **Module 00 (Mathematical Foundations & PyTorch):** Backpropagation, chain rule, gradient descent, basic PyTorch tensor operations and `nn.Module`
- **Module 01 (Word Embeddings):** Distributional semantics, vector representations of words, embedding lookup layers
- **Module 02 (Tokenization & Subword Models):** How raw text becomes integer token IDs, subword vocabularies, the input representation pipeline

Additionally, students need comfort with:
- Matrix multiplication and dot products
- The softmax function and its derivatives
- Basic probability (weighted averages, distributions)

## Chapter Structure

### Section 3.1: Recurrent Neural Networks & Their Limitations (~3,500 words)

**Level:** Basic / Fundamentals

**Key concepts:**
- The sequence modeling problem: why order matters
- The vanilla RNN cell: hidden state update equation h_t = tanh(W_hh * h_{t-1} + W_xh * x_t + b)
- Unrolling through time and backpropagation through time (BPTT)
- Vanishing gradients: the repeated multiplication problem
- Exploding gradients and gradient clipping
- LSTM cell: forget gate, input gate, output gate, cell state
- GRU cell: update gate, reset gate (simplified alternative to LSTM)
- Bidirectional RNNs: reading sequences in both directions
- Encoder-decoder (seq2seq) architecture
- The information bottleneck: compressing an entire source sequence into a single fixed-length vector

**Diagrams (4 total, all present):**
1. Vanilla RNN cell unrolled through time (SVG)
2. Vanishing gradient visualization showing shrinking gradients across time steps (SVG)
3. LSTM cell architecture with gates labeled (SVG)
4. Encoder-decoder seq2seq architecture with bottleneck highlighted (SVG)

**Code examples (5 blocks, all present):**
1. Minimal vanilla RNN forward pass in PyTorch (manual implementation)
2. Gradient magnitude demonstration across time steps
3. LSTM cell walkthrough using `nn.LSTMCell`
4. GRU cell walkthrough using `nn.GRUCell`
5. Complete seq2seq translation model (putting-it-all-together example)

**Exercises:**
- Self-check quiz with 6 conceptual questions (present)

**Pedagogical notes:**
- Open with a concrete analogy: summarizing a book by reading one page at a time and only keeping a single sticky note of memory
- The bottleneck problem at the end of this section must create genuine tension that Section 3.2 resolves
- Bridge from Module 01 (embeddings) by showing how embedding vectors become the x_t inputs to the RNN

---

### Section 3.2: The Attention Mechanism (~3,000 words)

**Level:** Intermediate / Engineering / Lab

**Key concepts:**
- The "where to look" intuition: instead of one summary vector, let the decoder peek back at every encoder state
- Bahdanau (additive) attention: alignment model using a learned feedforward network
- The alignment score function: e_{ij} = v^T tanh(W_1 * s_{i-1} + W_2 * h_j)
- Softmax over alignment scores to produce attention weights alpha_{ij}
- Context vector as a weighted sum of encoder hidden states
- Attention as soft alignment (connection to word alignment in machine translation)
- Luong (dot-product) attention: three scoring variants (dot, general, concat)
- Attention as a differentiable dictionary lookup
- Backpropagation through attention: Jacobian of softmax, gradient flow through the context vector
- Full integration of attention into the seq2seq decoder

**Diagrams (3 total, all present):**
1. Bahdanau attention mechanism showing encoder states, alignment scores, and context vector (SVG)
2. Attention weight heatmap for a translation example (SVG)
3. Side-by-side comparison of Bahdanau vs. Luong attention (SVG)

**Code examples (4 blocks, all present):**
1. Bahdanau additive attention implementation from scratch
2. Luong dot-product attention implementation from scratch
3. Visualizing attention weights
4. Integrating attention into a seq2seq decoder

**Exercises:**
- Self-check quiz with 5 conceptual questions (present)

**Pedagogical notes:**
- Begin by explicitly referencing the bottleneck problem from Section 3.1 and framing attention as its solution
- Use the "searching a library" analogy: instead of asking a librarian to summarize all books into one sentence, you get to skim the shelf yourself
- The differentiable dictionary lookup framing sets up the query/key/value abstraction in Section 3.3
- Include a warning callout about the distinction between "attention" in this historical context vs. self-attention in Transformers

---

### Section 3.3: Scaled Dot-Product & Multi-Head Attention (~4,000 words)

**Level:** Intermediate / Engineering / Lab

**Key concepts:**
- The query, key, value (Q, K, V) abstraction: generalizing attention beyond encoder-decoder
- Scaled dot-product attention: Attention(Q, K, V) = softmax(QK^T / sqrt(d_k)) V
- Why scaling by sqrt(d_k) is necessary: variance analysis of dot products in high dimensions
- Softmax temperature and its effect on attention distributions (sharp vs. diffuse)
- Self-attention vs. cross-attention: when Q, K, V come from the same sequence vs. different sequences
- Causal (autoregressive) masking: preventing the model from attending to future tokens
- Multi-head attention: running multiple attention heads in parallel on different learned projections
- The intuition for multiple heads: different heads capture different types of relationships
- Concatenation and final linear projection
- O(n^2) time and memory complexity analysis
- Brief mention of why this complexity motivates efficient attention research

**Diagrams (3 total, all present):**
1. Scaled dot-product attention data flow (SVG)
2. Multi-head attention showing parallel heads, concat, and projection (SVG)
3. Causal mask visualization as a lower-triangular matrix (SVG)

**Code examples (6 blocks, all present):**
1. Scaled dot-product attention function from scratch
2. Softmax temperature demonstration
3. Causal mask construction
4. Full `MultiHeadSelfAttention` class in PyTorch (the Lab exercise)
5. Complete example combining embedding, multi-head attention, and output
6. Complexity measurement / benchmarking

**Exercises:**
- Self-check quiz with 6 conceptual questions (present)

**Pedagogical notes:**
- Bridge from Section 3.2 by showing how Luong dot-product attention naturally generalizes into the Q/K/V formulation
- The Lab (subsection 6) is the centerpiece of this section: students implement `MultiHeadSelfAttention` as a reusable `nn.Module`
- Emphasize that this is the exact same mechanism used inside every Transformer layer (forward reference to Module 04)
- End with the complexity analysis to create an honest picture: attention is powerful but quadratic cost is a real constraint

---

## Terminology Standards

The following terms should be used consistently throughout the chapter:

| Term | Usage |
|------|-------|
| **hidden state** | The recurrent state vector h_t (not "memory" except informally in analogies) |
| **cell state** | The LSTM-specific c_t vector (distinct from hidden state) |
| **context vector** | The weighted sum of encoder states produced by attention (not "attention output") |
| **attention weights** | The softmax-normalized scores alpha_{ij} (not "attention scores," which refers to the pre-softmax values) |
| **alignment scores** | The raw, pre-softmax compatibility scores e_{ij} |
| **query, key, value** | Always spelled out on first use, then abbreviated as Q, K, V |
| **self-attention** | Attention where Q, K, V all come from the same sequence |
| **cross-attention** | Attention where Q comes from one sequence and K, V come from another |
| **causal masking** | Preferred over "autoregressive masking" or "look-ahead masking" |
| **multi-head attention** | Hyphenated as "multi-head" (adjective), not "multihead" |
| **scaled dot-product attention** | Full phrase on first use, then "scaled attention" is acceptable |
| **seq2seq** | Preferred shorthand for "sequence-to-sequence" (define on first use) |
| **BPTT** | Abbreviation for backpropagation through time (define on first use) |
| **information bottleneck** | The problem of compressing a variable-length sequence into a fixed-length vector |

## Cross-References

### Builds on:
- **Module 00 (Mathematical Foundations & PyTorch):** Backpropagation and chain rule are essential for understanding BPTT and gradient flow through attention. PyTorch basics are needed for all code examples.
- **Module 01 (Word Embeddings):** Embedding vectors serve as the input representations (x_t) fed into RNNs. The concept of learned vector representations carries forward.
- **Module 02 (Tokenization & Subword Models):** Students need to understand how raw text is converted to token IDs before being embedded and fed to sequence models.

### Referenced by:
- **Module 04 (Transformer Architecture):** Multi-head self-attention from Section 3.3 is the core building block of the Transformer. Module 04 will directly import the Q/K/V framework, causal masking, and multi-head attention concepts.
- **Module 05 (Training at Scale):** Understanding attention complexity (O(n^2)) provides context for why efficient training strategies matter.
- **Module 06+ (GPT, BERT, etc.):** All decoder-only and encoder-only architectures rely on the attention mechanism developed here.

## Quality Checklist

For each section, verify:
- [ ] Opens with a motivating "why" that connects to the previous section
- [ ] Every concept has at least one concrete analogy or example
- [ ] All code blocks are self-contained and runnable (with imports)
- [ ] At least one SVG diagram per major concept
- [ ] A callout box for the single most important insight
- [ ] A self-check quiz at the end
- [ ] Key takeaways summary at the end
- [ ] Forward reference to the next section (or to Module 04 for Section 3.3)
- [ ] No em dashes or double dashes anywhere in the text
- [ ] Voice is warm, authoritative, and conversational
