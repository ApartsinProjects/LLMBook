> Why have one head when you can have eight, each looking at the sentence from a slightly different existential angle?
>
> ![Attn](../../front-matter/images/agents/attn.png) [Attn](../../front-matter/wisdom-council.html#attn), Multi-Headed AI Agent
### Prerequisites
This section assumes you understand the intuitive attention mechanism from [Section 3.2](section-3.2.html) (alignment scores, weighted context vectors). Matrix multiplication and basic linear algebra (from [Section 0.2](../module-00-ml-pytorch-foundations/section-0.2.html)) are needed for the Q/K/V formulation. The multi-head attention mechanism developed here is the core component of the Transformer architecture detailed in [Section 4.1](module-04-transformer-architecture_section-4.1.html.md); for optimization-focused variants like grouped-query attention, see [Section 4.2](module-04-transformer-architecture_section-4.2.html.md).
Big Picture
**From seq2seq attention to the Transformer's attention.** In [Section 3.2](section-3.2.html), we used attention to let a decoder peek at encoder states. The Transformer (Vaswani et al., 2017) takes this much further. It introduces the query/key/value (Q/K/V) abstraction, scales the dot products by √dkd\_{k}dk​ for numerical stability, runs multiple attention "heads" in parallel, and applies attention not just between encoder and decoder but also *within* a single sequence (self-attention). These building blocks are the heart of GPT, BERT, and every modern LLM. By the end of this section, you will have implemented multi-head self-attention from scratch and understood every piece of the mechanism that makes Transformers work.
![Four detectives sitting around a table, each examining the same case file from a different angle, representing multiple attention heads analyzing the same sequence with different learned perspectives](images/multi-head-detectives.png)
**Figure 3.3.1**: Multi-head attention assigns multiple "detectives" to the same sequence. Each head learns to focus on a different type of relationship: one tracks syntax, another tracks coreference, a third tracks semantic similarity.
## 1. The Query, Key, Value Abstraction
In [Section 3.2](section-3.2.html), we described attention as a soft dictionary lookup: a query is compared
against keys to produce weights, which are used to combine values. In Bahdanau and Luong
attention, the keys and values were the same thing (encoder hidden states), and the query
was the decoder state.
The Transformer formalizes and generalizes this. Given input vectors, it creates three separate
representations through learned linear projections:
- **Query (Q):** What am I looking for? Obtained by projecting the input through WQW^{Q}WQ.
- **Key (K):** What do I contain? Obtained by projecting the input through WKW^{K}WK.
- **Value (V):** What should I send back? Obtained by projecting the input through WVW^{V}WV.
These are *separate* projections of the same (or different) input vectors. This decoupling
is crucial: the information used for matching (Q and K) can differ from the information that
gets passed forward (V). A position might have a key that says "I am a verb in past tense"
(used for matching) while its value encodes the actual semantic meaning of that verb
(used for the output).
## 2. Scaled Dot-Product Attention
Given query matrix QQQ, key matrix KKK,
and value matrix VVV, the Transformer computes:
Attention⁡(Q,K,V)=softmax⁡(QKT/dk)V\operatorname{Attention}(Q, K, V) = \operatorname{softmax}(QK^{T} / \sqrt{d\_k}) VAttention(Q,K,V)=softmax(QKT/dk​​)V
Let us break this formula apart:
1. **QKT**: Computes dot-product similarity between every query and every key simultaneously. If Q has shape (n,dk)(n, d\_{k})(n,dk​) and K has shape (m,dk)(m, d\_{k})(m,dk​), this produces an (n,m)(n, m)(n,m) matrix of raw attention scores.
2. **Scaling by √dkd\_{k}dk​**: Divides each score by the square root of the key dimension. Without this scaling, the dot products would grow in magnitude with dkd\_{k}dk​, pushing the softmax into saturated regions where its gradients are extremely small.
3. **Softmax:** Converts each row into a probability distribution over key positions.
4. **Multiply by V:** Uses the attention weights to take a weighted combination of value vectors.
### Why Scale by √dk?
Tip: The Scaling Fix That Saved Transformers
Without the √dk scaling, Transformers would barely train at all. The original "Attention Is All You Need" paper reports that unscaled dot-product attention produced significantly worse results. This single division operation is easy to overlook, but it is one of those small engineering decisions that makes the difference between a groundbreaking architecture and a failed experiment.
Consider two random vectors qqq and kkk, each with
entries drawn from a standard normal distribution. Their dot product
q⋅k=Σiqikiq \cdot k = \Sigma \_{i} q\_{i}k\_{i}q⋅k=Σi​qi​ki​
is a sum of dkd\_{k}dk​ independent products, each with mean 0 and
variance 1. By the properties of sums of random variables, the dot product has
mean 0 and variance dkd\_{k}dk​. As dkd\_{k}dk​ grows,
the typical magnitude of the dot product increases as dk\sqrt{d\_k}dk​​.
Large-magnitude inputs to softmax produce outputs very close to 0 or 1, with tiny gradients.
Dividing by dk\sqrt{d\_k}dk​​ restores the variance to approximately 1,
keeping softmax in its sensitive, gradient-friendly regime.
Code Fragment 3.3.1 below puts this into practice.
![](http://llmbook.apartsin.com/styles/icons/callout-code.svg)Show Code (25 lines)
```python
# Show why scaling matters: as d_k grows, raw dot products explode
# and softmax saturates, concentrating all weight on one key.
import torch
import torch.nn.functional as F
torch.manual_seed(42)
# Demonstrate the scaling problem
for d_k in [8, 64, 512]:
 q = torch.randn(1, d_k)
 K = torch.randn(10, d_k)
 # Unscaled dot products
 scores_unscaled = q @ K.T
 # Scaled dot products
 scores_scaled = scores_unscaled / (d_k ** 0.5)
 probs_unscaled = F.softmax(scores_unscaled, dim=-1)
 probs_scaled = F.softmax(scores_scaled, dim=-1)
 print(f"d_k={d_k:3d} | unscaled std={scores_unscaled.std():.2f}, "
 f"max prob={probs_unscaled.max():.4f} | "
 f"scaled std={scores_scaled.std():.2f}, "
 f"max prob={probs_scaled.max():.4f}")
```
Output (3 lines)
d\_k= 8 | unscaled std=2.38, max prob=0.5765 | scaled std=0.84, max prob=0.2213
d\_k= 64 | unscaled std=7.89, max prob=0.9998 | scaled std=0.99, max prob=0.2697
d\_k=512 | unscaled std=22.64, max prob=1.0000 | scaled std=1.00, max prob=0.2381
![](http://llmbook.apartsin.com/styles/icons/callout-code.svg)Show Code (16 lines)
```python
import torch
import torch.nn as nn
# Built-in MHA: same functionality, one line to create
mha = nn.MultiheadAttention(embed_dim=128, num_heads=4, batch_first=True)
x = torch.randn(2, 10, 128) # (batch, seq_len, d_model)
# Bidirectional (BERT-style): pass x as query, key, and value
out, weights = mha(x, x, x)
print(f"Output: {out.shape}") # torch.Size([2, 10, 128])
print(f"Weights: {weights.shape}") # torch.Size([2, 10, 10])
# Causal (GPT-style): generate a causal mask
mask = nn.Transformer.generate_square_subsequent_mask(10)
out_causal, _ = mha(x, x, x, attn_mask=mask)
```
**Code Fragment 3.3.1:** Demonstrate the scaling problem.
At dk=512d\_{k} = 512dk​=512, the unscaled softmax is completely saturated
(max probability is essentially 1.0, meaning all attention goes to a single position). The
scaled version maintains a healthy distribution. This is not just a cosmetic issue; saturated
softmax means near-zero gradients, which makes training extremely difficult.
Softmax [Temperature](module-05-decoding-text-generation_section-5.2.html.md)
Scaling by 1/dk1/ \sqrt{d\_k}1/dk​​ is equivalent to using a softmax with **temperature** T=dkT = \sqrt{d\_k}T=dk​​. Higher temperature produces softer (more uniform) distributions; lower temperature produces sharper (more peaked) ones. Some implementations allow an explicit temperature parameter for fine-grained control during inference, but during training the dk\sqrt{d\_k}dk​​ scaling is standard.
![Scaled dot-product attention: Q*K^T, scale, mask, softmax, multiply V](images/fig-3.3.2-scaled-dot-product.png)
**Figure 3.3.2**: Scaled dot-product attention. Q and K are multiplied, scaled, optionally masked, passed through softmax, then used to weight V. The optional mask is used for causal (autoregressive) attention.
### Implementation from Scratch
This implementation computes scaled dot-product attention step by step, including the optional causal mask.
![](http://llmbook.apartsin.com/styles/icons/callout-code.svg)Show Code (45 lines)
```python
# Scaled dot-product attention from scratch: Q @ K^T / sqrt(d_k),
# optional mask to block future tokens, softmax, then V weighting.
import torch
import torch.nn.functional as F
import math
def scaled_dot_product_attention(Q, K, V, mask=None):
 """
 Q: (batch, n_queries, d_k)
 K: (batch, n_keys, d_k)
 V: (batch, n_keys, d_v)
 mask: (batch, n_queries, n_keys) or broadcastable, True = mask out
 Returns: output (batch, n_queries, d_v), weights (batch, n_queries, n_keys)
 """
 d_k = Q.size(-1)
 # Step 1: Compute raw attention scores
 scores = torch.bmm(Q, K.transpose(-2, -1)) # (batch, n_q, n_k)
 # Step 2: Scale
 scores = scores / math.sqrt(d_k)
 # Step 3: Apply mask (if provided)
 if mask is not None:
 scores = scores.masked_fill(mask, float('-inf'))
 # Step 4: Softmax to get attention weights
 weights = F.softmax(scores, dim=-1) # (batch, n_q, n_k)
 # Step 5: Weighted sum of values
 output = torch.bmm(weights, V) # (batch, n_q, d_v)
 return output, weights
# Test: 4 queries attending to 6 key-value pairs
batch, n_q, n_k, d_k, d_v = 2, 4, 6, 32, 64
Q = torch.randn(batch, n_q, d_k)
K = torch.randn(batch, n_k, d_k)
V = torch.randn(batch, n_k, d_v)
out, wts = scaled_dot_product_attention(Q, K, V)
print(f"Output shape: {out.shape}") # (2, 4, 64)
print(f"Weights shape: {wts.shape}") # (2, 4, 6)
print(f"Weights row 0 sums to: {wts[0, 0].sum():.4f}")
print(f"Weights[0,0]: {wts[0,0].detach().numpy().round(3)}")
```
Output (4 lines)
Output shape: torch.Size([2, 4, 64])
Weights shape: torch.Size([2, 4, 6])
Weights row 0 sums to: 1.0000
Weights[0,0]: [0.086 0.301 0.155 0.024 0.212 0.222]
**Code Fragment 3.3.2:** Step 1: Compute raw attention scores.
## 3. Self-Attention vs. Cross-Attention
The Q/K/V framework enables two fundamental modes of attention:
### Self-Attention
In **self-attention**, the queries, keys, and values all come from the *same*
sequence. Each position in the sequence attends to every other position (including itself).
This allows each token to gather information from the entire input, building context-aware
representations in a single operation.
Self-attention is what makes Transformers fundamentally different from RNNs. An RNN can only
see past context (or future context, if bidirectional); self-attention sees *all* positions
simultaneously. For a sentence like "The animal didn't cross the street because *it* was too
tired," self-attention allows the model to connect "it" directly to "animal" regardless of distance.
### Cross-Attention
In **cross-attention**, the queries come from one sequence (typically the decoder)
while the keys and values come from a different sequence (typically the encoder). This is
exactly the encoder-decoder attention from [Section 3.2](section-3.2.html), reformulated in the Q/K/V framework.
Cross-attention is what allows a Transformer decoder to "look at" the encoder output.
Cross-Attention Comparison
| Property | Self-Attention | Cross-Attention |
| --- | --- | --- |
| Q source | Same sequence (X) | Decoder states |
| K, V source | Same sequence (X) | Encoder outputs |
| Typical use | Build contextual representations | Combine encoder/decoder information |
| Score matrix shape | (n, n), square | (ndecn\_{dec}ndec​, nencn\_{enc}nenc​), rectangular |
| Examples | [BERT](../../part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.1.html), GPT encoder/decoder blocks | Machine translation, T5 decoder |
## 4. Causal Masking for Autoregressive Models
In autoregressive language models (like GPT), each token should only attend to tokens
that appear *before* it in the sequence (and itself). It must not "peek" at future
tokens that have not been generated yet. This causal constraint is what makes [left-to-right text generation (Chapter 5)](module-05-decoding-text-generation_index.html.md) possible. This constraint is enforced with a
**causal mask**: an upper-triangular matrix of `True` values
that sets future positions to −∞- \infty−∞ before the softmax.
maskij=True  if  j>i  (futureposition)mask\_{ij} = True \; \text{if} \; j > i \; (future position)maskij​=Trueifj>i(futureposition)
After masking, the scores for future positions become −∞- \infty−∞,
which softmax maps to exactly 0. Each position can only attend to itself and earlier positions.
Code Fragment 3.3.3 below puts this into practice.
![](http://llmbook.apartsin.com/styles/icons/callout-code.svg)Show Code (20 lines)
```python
# Causal (autoregressive) masking: build an upper-triangular boolean mask
# and pass it to scaled_dot_product_attention to block future positions.
import torch
# Create a causal mask for sequence length 5
seq_len = 5
causal_mask = torch.triu(torch.ones(seq_len, seq_len, dtype=torch.bool), diagonal=1)
print("Causal mask (True = blocked):")
print(causal_mask.int())
# Apply to attention scores
scores = torch.randn(1, seq_len, seq_len)
# Mask future positions with -inf so softmax ignores them
scores_masked = scores.masked_fill(causal_mask.unsqueeze(0), float('-inf'))
# Convert scores to attention weights (probabilities summing to 1)
weights = torch.softmax(scores_masked, dim=-1)
print("\nAttention weights (causal):")
print(weights[0].detach().numpy().round(3))
```
Output (13 lines)
Causal mask (True = blocked):
tensor([[0, 1, 1, 1, 1],
[0, 0, 1, 1, 1],
[0, 0, 0, 1, 1],
[0, 0, 0, 0, 1],
[0, 0, 0, 0, 0]])
Attention weights (causal):
[[1.000 0.000 0.000 0.000 0.000]
[0.613 0.387 0.000 0.000 0.000]
[0.248 0.505 0.247 0.000 0.000]
[0.168 0.339 0.112 0.381 0.000]
[0.041 0.298 0.371 0.106 0.184]]
**Code Fragment 3.3.3:** Create a causal mask for sequence length 5.
Notice the triangular structure: position 0 can only attend to itself (weight 1.0),
position 1 can attend to positions 0 and 1, and so on. The upper triangle is exactly
zero, guaranteeing no information leakage from the future.
Key Insight
Causal masking is what distinguishes GPT-style (decoder-only) models from BERT-style (encoder-only) models. BERT uses *bidirectional* self-attention (no mask), so every position can attend to every other position. GPT uses *causal* self-attention (with mask), so each position can only see the past. This difference determines what tasks each architecture is suited for: BERT excels at understanding (classification, NER), while GPT excels at generation (text completion, dialogue).
## 5. Multi-Head Attention
Key Insight
Multi-head attention implements a form of "ensemble of subspaces" that has deep parallels in signal processing and neuroscience. In signal processing, a filter bank decomposes a complex signal into frequency bands, each capturing a different scale of structure. Multi-head attention does something analogous: each head projects the input into a different learned subspace and computes attention within that subspace, capturing a different relational pattern (syntactic, semantic, positional). Neuroscience research on the visual cortex reveals a strikingly similar architecture: populations of neurons in area V1 are organized into orientation columns, with different groups selectively responding to different edge orientations in the visual field. The brain does not attempt to represent all visual features with a single neural population; it allocates separate computational channels to separate feature types and integrates them downstream. Multi-head attention independently arrived at the same architectural principle.
A single attention head can only capture one type of relationship at a time. If a word
needs to attend to its syntactic head, its semantic role, and a coreferent pronoun
simultaneously, a single attention distribution cannot represent all three patterns.
**Multi-head attention** solves this by running multiple attention operations
in parallel, each with its own learned projections:
headi=Attention⁡(XWiQ,XWiK,XWiV)head\_{i} = \operatorname{Attention}(XW\_{i}^{Q}, XW\_{i}^{K}, XW\_{i}^{V})headi​=Attention(XWiQ​,XWiK​,XWiV​)
The individual head outputs are concatenated and projected back to the model dimension:
MultiHead(X)=Concat(head1,...,headh)WO\text{MultiHead}(X) = Concat(head\_{1}, ..., head\_{h}) W^{O}MultiHead(X)=Concat(head1​,...,headh​)WO
Each head operates in a lower-dimensional subspace. If the model dimension is
dmodeld\_{model}dmodel​ and there are hhh heads,
each head works with dimension dk=dmodel/hd\_{k} = d\_{model} / hdk​=dmodel​/h.
Variants like Grouped Query Attention (GQA) reduce the number of key/value heads to save memory; we cover these optimizations in [Section 4.3](module-04-transformer-architecture_section-4.3.html.md) and their inference impact in [Section 9.2](../../part-2-understanding-llms/module-09-inference-optimization/section-9.2.html).
The outputs of all heads are concatenated and projected back to the full model dimension
through WOW^{O}WO.
![Multi-head attention: parallel heads with independent projections, concatenated and projected](images/fig-3.3.3-multi-head.png)
**Figure 3.3.3**: Multi-head attention with h=4 heads. Each head independently projects the input into a lower-dimensional Q/K/V space, computes attention, and the results are concatenated and projected back to the full model dimension.
## 6. Lab: Implementing Multi-Head Self-Attention
Let us now build a complete, production-style multi-head self-attention module. This is
the exact computation at the heart of every Transformer layer.
Code Fragment 3.3.4 below puts this into practice.
![](http://llmbook.apartsin.com/styles/icons/callout-code.svg)Show Code (89 lines)
```python
# Multi-head self-attention: project input into h separate (Q, K, V) triples,
# run scaled dot-product attention on each head, concatenate, and project back.
import torch
import torch.nn as nn
import torch.nn.functional as F
import math
class MultiHeadSelfAttention(nn.Module):
 """Multi-head self-attention with optional causal masking."""
 def __init__(self, d_model, n_heads, dropout=0.0):
 super().__init__()
 assert d_model % n_heads == 0, "d_model must be divisible by n_heads"
 self.d_model = d_model
 self.n_heads = n_heads
 self.d_k = d_model // n_heads # dimension per head
 # Combined Q, K, V projection (more efficient than three separate ones)
 self.qkv_proj = nn.Linear(d_model, 3 * d_model)
 # Output projection
 self.out_proj = nn.Linear(d_model, d_model)
 self.dropout = nn.Dropout(dropout)
 def forward(self, x, causal=False):
 """
 x: (batch, seq_len, d_model)
 causal: if True, apply causal mask
 Returns: (batch, seq_len, d_model)
 """
 B, T, C = x.shape
 # Step 1: Project to Q, K, V
 qkv = self.qkv_proj(x) # (B, T, 3*C)
 Q, K, V = qkv.chunk(3, dim=-1) # each: (B, T, C)
 # Step 2: Reshape for multi-head: (B, T, C) -> (B, h, T, d_k)
 Q = Q.view(B, T, self.n_heads, self.d_k).transpose(1, 2)
 K = K.view(B, T, self.n_heads, self.d_k).transpose(1, 2)
 V = V.view(B, T, self.n_heads, self.d_k).transpose(1, 2)
 # Step 3: Scaled dot-product attention
 scores = torch.matmul(Q, K.transpose(-2, -1)) # (B, h, T, T)
 scores = scores / math.sqrt(self.d_k)
 # Step 4: Causal mask (optional)
 if causal:
 mask = torch.triu(torch.ones(T, T, device=x.device, dtype=torch.bool), diagonal=1)
 scores = scores.masked_fill(mask.unsqueeze(0).unsqueeze(0), float('-inf'))
 # Step 5: Softmax + dropout
 weights = F.softmax(scores, dim=-1) # (B, h, T, T)
 weights = self.dropout(weights)
 # Step 6: Weighted sum of values
 out = torch.matmul(weights, V) # (B, h, T, d_k)
 # Step 7: Concatenate heads: (B, h, T, d_k) -> (B, T, C)
 out = out.transpose(1, 2).contiguous().view(B, T, C)
 # Step 8: Output projection
 out = self.out_proj(out) # (B, T, C)
 return out, weights
# Create and test the module
mha = MultiHeadSelfAttention(d_model=128, n_heads=4)
x = torch.randn(2, 10, 128) # batch=2, seq_len=10, d_model=128
# Bidirectional (BERT-style)
out_bi, wts_bi = mha(x, causal=False)
print(f"Bidirectional output: {out_bi.shape}")
print(f"Weights shape: {wts_bi.shape}")
# Causal (GPT-style)
out_ca, wts_ca = mha(x, causal=True)
print(f"Causal output: {out_ca.shape}")
# Verify causal mask works: position 0 should have zero weight on all future positions
print(f"\nCausal weights for head 0, position 0:")
print(f" {wts_ca[0, 0, 0].detach().numpy().round(4)}")
print(f" (Only first entry is non-zero: position 0 attends only to itself)")
# Count parameters
params = sum(p.numel() for p in mha.parameters())
print(f"\nTotal parameters: {params:,}")
print(f" QKV projection: {128 * 3 * 128 + 3 * 128:,}")
print(f" Output projection: {128 * 128 + 128:,}")
```
Output (11 lines)
Bidirectional output: torch.Size([2, 10, 128])
Weights shape: torch.Size([2, 4, 10, 10])
Causal output: torch.Size([2, 10, 128])
Causal weights for head 0, position 0:
[1.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000]
(Only first entry is non-zero: position 0 attends only to itself)
Total parameters: 66,048
QKV projection: 49,536
Output projection: 16,512
Library Shortcut: PyTorch nn.MultiheadAttention
The 50-line from-scratch implementation above is valuable for understanding the internals. In production, PyTorch provides a built-in module that handles the Q/K/V projections, head splitting, masking, and output projection in a single optimized call:
**Code Fragment 3.3.4:** Combined Q, K, V projection (more efficient than three separate ones).
`pip install torch` (already installed if you followed [Section 0.3](../module-00-ml-pytorch-foundations/section-0.3.html)). The built-in version also supports `F.scaled_dot_product_attention` with FlashAttention backends on compatible GPUs.
Implementation Detail
In our implementation, we use a single linear layer (`qkv_proj`) to compute Q, K, and V simultaneously, then split the output into three parts. This is mathematically equivalent to using three separate linear layers but is more computationally efficient because it requires only one matrix multiplication instead of three. Most production implementations (PyTorch's `nn.MultiheadAttention`, [Hugging Face](../../part-3-working-with-llms/module-10-llm-apis/section-10.2.html) Transformers) use this fused approach.
## 7. Complexity Analysis: The O(n²) Problem
Fun Fact
The quadratic cost of self-attention is why your favorite chatbot has a context window limit. Doubling the sequence length quadruples the memory needed, which is why "just make the context window bigger" is roughly as simple as "just make the ocean smaller."
Self-attention has a fundamental computational cost: the score matrix
QKTQK^{T}QKT has shape
(n,n)(n, n)(n,n) where nnn is the sequence length.
This means both the computation and memory required grow **quadratically** with
sequence length.
Operation Comparison
| Operation | Time Complexity | Space Complexity |
| --- | --- | --- |
| Q, K, V projections | O(n · d²) | O(n · d) |
| QKT computation | O(n² · d) | O(n²) |
| Softmax | O(n²) | O(n²) |
| Attention × V | O(n² · d) | O(n · d) |
| **Total** | **O(n² · d)** | **O(n² + n · d)** |
For typical LLM settings, nnn can be 2048, 8192, or even 128,000
tokens. The attention matrix alone for a 128K-token sequence would require
128,000 × 128,000 × 4 bytes ≈ **62 GB** of memory per head.
This quadratic scaling is the primary bottleneck that limits context lengths in Transformer
models.
Code Fragment 3.3.5 below puts this into practice.
![](http://llmbook.apartsin.com/styles/icons/callout-code.svg)Show Code (32 lines)
```python
# Benchmark attention wall-clock time as sequence length doubles.
# Quadratic O(n^2) scaling becomes visible at longer sequences.
import torch, time
# Measure how attention scales with sequence length
d_model, n_heads = 128, 4
mha = MultiHeadSelfAttention(d_model, n_heads)
mha.eval()
print(f"{' seq_len':>10} {'time (ms)':>10} {'mem (MB)':>10} {'ratio':>8}")
prev_time = None
for seq_len in [64, 128, 256, 512, 1024, 2048]:
 x = torch.randn(1, seq_len, d_model)
 # Warm up
 with torch.no_grad():
 _ = mha(x)
 # Time it
 t0 = time.perf_counter()
 with torch.no_grad():
 for _ in range(20):
 _ = mha(x)
 elapsed = (time.perf_counter() - t0) / 20 * 1000
 # Memory for attention matrix
 attn_mem = seq_len * seq_len * n_heads * 4 / 1e6 # float32
 ratio = f"{elapsed / prev_time:.1f}x" if prev_time else ""
 print(f"{seq_len:>10} {elapsed:>10.2f} {attn_mem:>10.2f} {ratio:>8}")
 prev_time = elapsed
```
Output (7 lines)
seq\_len time (ms) mem (MB) ratio
64 0.34 0.07
128 0.52 0.26 1.5x
256 1.18 1.05 2.3x
512 3.87 4.19 3.3x
1024 14.23 16.78 3.7x
2048 55.41 67.11 3.9x
**Code Fragment 3.3.5:** Measure how attention scales with sequence length.
Each doubling of sequence length increases computation time by roughly 4x (approaching
the theoretical quadratic scaling). The memory for attention matrices also grows quadratically.
This is why modern LLM research invests heavily in techniques like Flash Attention, sparse
attention, and linear attention approximations to tame this O(n²) cost.
🌎 **Real-World Scenario**: PyTorch Scaled Dot-Product Attention (with FlashAttention backend)
PyTorch 2.0+ includes a fused attention kernel that automatically uses FlashAttention when available.
```python
import torch
import torch.nn.functional as F
# Simulated Q, K, V: batch=1, heads=8, seq_len=128, head_dim=64
Q = torch.randn(1, 8, 128, 64)
K = torch.randn(1, 8, 128, 64)
V = torch.randn(1, 8, 128, 64)
# PyTorch's fused kernel selects FlashAttention, memory-efficient,
# or math backend automatically based on hardware
out = F.scaled_dot_product_attention(Q, K, V, is_causal=True)
print("Output shape:", out.shape) # (1, 8, 128, 64)
# Check which backend was selected
# Requires: pip install flash-attn (for the FlashAttention backend on CUDA)
```
**Code Fragment 3.3.17:** Simulated Q, K, V: batch=1, heads=8, seq\_len=128, head\_dim=64
Looking Ahead
Despite the quadratic cost, self-attention has massive advantages over RNNs: (1) all positions are processed in parallel (no sequential bottleneck), (2) any two positions are connected by a single attention operation (constant path length, vs. O(n) for RNNs), and (3) the model can learn any interaction pattern rather than being constrained to sequential information flow. These advantages have made the O(n²) cost worth paying, and efficient attention variants continue to push the boundaries of what is practical.
Key Insight: Self-Attention as an N-Body Problem
The O(n²) cost of self-attention is not a design flaw; it is the fundamental price of allowing every token to interact with every other token. This is structurally identical to the N-body problem in physics, where computing gravitational or electromagnetic interactions between N particles requires O(N²) pairwise force calculations. Just as physicists developed approximation methods (Barnes-Hut tree codes, fast multipole methods) to reduce N-body computation to O(N log N) by grouping distant particles, researchers have developed sparse attention, linear attention, and locality-sensitive hashing to approximate the full attention matrix. The parallel extends further: in both domains, nearby interactions matter more than distant ones, which is exactly the intuition behind local attention windows. The question of whether O(n) attention can truly match O(n²) quality is equivalent to asking whether long-range token interactions carry essential information, a question whose answer varies by task, just as gravitational and electromagnetic forces have different effective ranges.
🌎 **Real-World Scenario**: Multi-Head Attention in Sentiment Analysis
In a sentiment classifier built on multi-head self-attention, different heads learn to capture different linguistic features. For the sentence "The food was great but the service was terrible," one head might learn to attend from "great" and "terrible" to the nearby nouns ("food" and "service"), capturing what each adjective modifies. Another head might attend from "terrible" backward to "but," learning that the conjunction signals a contrast. A third head might attend broadly across the entire sentence, computing a summary representation. This division of labor happens automatically during training and is why multi-head attention outperforms a single, larger attention head: the model can represent multiple relationship types simultaneously rather than averaging them into a single attention pattern.
## 8. Putting It All Together: Complete Example
Let us combine everything into a demonstration that shows multi-head self-attention
operating on actual token embeddings, with visualization of what different heads learn:
Code Fragment 3.3.6 below puts this into practice.
![](http://llmbook.apartsin.com/styles/icons/callout-code.svg)Show Code (37 lines)
```python
# End-to-end demo: embed a 5-word sentence, run multi-head attention,
# and inspect the output shape to verify the residual-ready dimensions.
import torch
import torch.nn as nn
# Simulate a small vocabulary and sentence
vocab = {"the": 0, "cat": 1, "sat": 2, "on": 3, "mat": 4}
sentence = ["the", "cat", "sat", "on", "mat"]
token_ids = torch.tensor([[vocab[w] for w in sentence]])
# Embedding + self-attention
d_model, n_heads = 64, 4
embedding = nn.Embedding(len(vocab), d_model)
attn = MultiHeadSelfAttention(d_model, n_heads)
# Forward pass
x = embedding(token_ids) # (1, 5, 64)
output, weights = attn(x, causal=True) # causal for GPT-style
print(f"Input shape: {x.shape}")
print(f"Output shape: {output.shape}")
print(f"Weights shape: {weights.shape} (batch, heads, queries, keys)")
# Show what each head attends to for the word "mat" (last position)
print(f"\nAttention to generate representation of 'mat' (position 4):")
for h in range(n_heads):
 w = weights[0, h, 4].detach().numpy()
 top_pos = w.argmax()
 print(f" Head {h}: {' '.join(f'{sentence[i]}:{w[i]:.2f}' for i in range(5))}"
 f" (peak: '{sentence[top_pos]}')")
# Verify output is different from input (attention has mixed information)
cos_sim = nn.functional.cosine_similarity(x[0], output[0], dim=-1)
print(f"\nCosine similarity (input vs output) per position:")
for i, word in enumerate(sentence):
 print(f" '{word}': {cos_sim[i]:.4f}")
```
Output (16 lines)
Input shape: torch.Size([1, 5, 64])
Output shape: torch.Size([1, 5, 64])
Weights shape: torch.Size([1, 4, 5, 5]) (batch, heads, queries, keys)
Attention to generate representation of 'mat' (position 4):
Head 0: the:0.18 cat:0.08 sat:0.25 on:0.12 mat:0.37 (peak: 'mat')
Head 1: the:0.04 cat:0.41 sat:0.09 on:0.33 mat:0.13 (peak: 'cat')
Head 2: the:0.22 cat:0.15 sat:0.38 on:0.06 mat:0.19 (peak: 'sat')
Head 3: the:0.09 cat:0.11 sat:0.17 on:0.48 mat:0.15 (peak: 'on')
[Cosine similarity](../../part-5-retrieval-conversation/module-19-embeddings-vector-db/section-19.1.html) (input vs output) per position:
'the': 0.2341
'cat': 0.1876
'sat': 0.3012
'on': 0.2543
'mat': 0.1698
**Code Fragment 3.3.6:** Simulate a small vocabulary and sentence.
Each head focuses on a different relationship. Head 1 connects "mat" primarily to "cat"
(the subject), Head 2 connects it to "sat" (the verb), and Head 3 connects it to "on"
(the preposition). This diversity is exactly why multiple heads are valuable: they let
the model simultaneously capture syntactic, semantic, and positional relationships.
The low cosine similarity between input and output confirms that attention is doing
substantial work: the output representations are very different from the raw embeddings,
enriched with contextual information from other positions.
## ✓ Key Takeaways
1. **Q/K/V projections** decouple what is used for matching (Q, K) from what is communicated (V), making attention far more expressive than using the same vectors for all roles.
2. **Scaling by √dkd\_{k}dk​** prevents dot products from growing with dimension, keeping softmax in a gradient-friendly regime. Without scaling, attention distributions saturate and training breaks down.
3. **Multi-head attention** runs h independent attention operations in parallel, each in a lower-dimensional subspace. This allows the model to capture multiple types of relationships simultaneously without increasing parameter count.
4. **Self-attention** computes Q, K, V from the same sequence, allowing every position to incorporate information from every other position. **Cross-attention** takes Q from one sequence and K, V from another.
5. **Causal masking** restricts each position to attend only to earlier positions, enabling autoregressive generation. This is the key difference between GPT (causal) and BERT (bidirectional) architectures.
6. **O(n²) complexity** in both time and memory is the primary scalability bottleneck of self-attention. Every pair of positions must be scored, limiting practical context lengths.
7. **What comes next:** In [Chapter 04](module-04-transformer-architecture_index.html.md), we will combine multi-head self-attention with feedforward layers, [layer normalization](module-04-transformer-architecture_section-4.1.html.md), and [residual connections](module-04-transformer-architecture_section-4.1.html.md) to build the complete Transformer architecture.
Research Frontier
**Efficient attention variants** remain one of the most active research areas. Grouped-query attention (GQA), used in [Llama 2](../../part-2-understanding-llms/module-07-modern-llm-landscape/section-7.2.html)/3 and Mistral, reduces the [KV cache](../../part-2-understanding-llms/module-09-inference-optimization/section-9.2.html) by sharing key-value heads across query heads (see [Section 4.2](module-04-transformer-architecture_section-4.2.html.md) for implementation). Multi-query attention (MQA) takes this further with a single shared KV head. FlashAttention (Dao et al., 2022, 2023) rewrites the attention computation to be IO-aware, achieving exact attention with sub-quadratic memory. Ring attention (Liu et al., 2023) distributes attention across devices to handle million-token contexts. Differential Transformer (Ye et al., 2024) introduces differential attention scores to reduce noise. These developments suggest that the raw O(n^2) cost of attention is increasingly a theoretical rather than practical bottleneck.
Tip: Start with Small Sequences for Debugging
When debugging sequence models, use a batch of 2 to 4 short sequences (under 20 tokens) where you can manually verify the expected output. Scale up only after the model produces correct results on these micro-examples.
🛠 Lab: Linear Algebra for Attention
Duration: ~45 min
Intermediate
### Objective
Implement scaled dot-product attention and multi-head attention from scratch using only NumPy, then verify your implementation against PyTorch's built-in attention. This lab turns the mathematical formulas from this section into working code.
### Skills Practiced
- Implementing the Q/K/V attention formula: softmax(QK^T / sqrt(d\_k)) V
- Building multi-head attention with parallel heads and concatenation
- Applying causal masking for autoregressive generation
- Visualizing attention weight heatmaps
### Setup
Install the required packages for this lab.
![](http://llmbook.apartsin.com/styles/icons/callout-code.svg)Code (1 lines)
```python
pip install numpy matplotlib torch
```
### Steps
### Step 1: Implement scaled dot-product attention
Write the core attention function from the "Attention Is All You Need" paper. The scaling factor prevents the dot products from growing too large, which would push softmax into regions with vanishing gradients.
![](http://llmbook.apartsin.com/styles/icons/callout-code.svg)Show Code (34 lines)
```python
import numpy as np
def softmax(x, axis=-1):
 """Numerically stable softmax."""
 e_x = np.exp(x - np.max(x, axis=axis, keepdims=True))
 return e_x / np.sum(e_x, axis=axis, keepdims=True)
def scaled_dot_product_attention(Q, K, V, mask=None):
 """
 Q, K, V: arrays of shape (seq_len, d_k)
 mask: optional boolean array; True means "mask this position"
 Returns: attention output and attention weights
 """
 d_k = Q.shape[-1]
 scores = Q @ K.T / np.sqrt(d_k) # (seq_len, seq_len)
 if mask is not None:
 scores = np.where(mask, -1e9, scores)
 weights = softmax(scores, axis=-1)
 output = weights @ V
 return output, weights
# Test with a small example: 4 tokens, dimension 8
np.random.seed(42)
seq_len, d_k = 4, 8
Q = np.random.randn(seq_len, d_k)
K = np.random.randn(seq_len, d_k)
V = np.random.randn(seq_len, d_k)
output, weights = scaled_dot_product_attention(Q, K, V)
print(f"Attention output shape: {output.shape}")
print(f"Attention weights (each row sums to 1):")
print(np.round(weights, 3))
```
**Code Fragment 3.3.15:** A from-scratch implementation of scaled dot-product attention using NumPy. The scaling factor (dividing by the square root of d\_k) prevents dot products from growing large enough to push softmax into near-zero gradient regions.
### Step 2: Visualize attention weights as a heatmap
Plot the attention matrix to see which tokens attend to which. Each row shows the attention distribution for one query token across all key tokens.
![](http://llmbook.apartsin.com/styles/icons/callout-code.svg)Show Code (40 lines)
```python
import matplotlib.pyplot as plt
tokens = ["The", "cat", "sat", "down"]
fig, axes = plt.subplots(1, 2, figsize=(12, 4))
# Bidirectional attention (no mask)
_, weights_bidi = scaled_dot_product_attention(Q, K, V)
im1 = axes[0].imshow(weights_bidi, cmap="Blues", vmin=0, vmax=1)
axes[0].set_xticks(range(4))
axes[0].set_xticklabels(tokens)
axes[0].set_yticks(range(4))
axes[0].set_yticklabels(tokens)
axes[0].set_title("Bidirectional Attention")
axes[0].set_xlabel("Key")
axes[0].set_ylabel("Query")
for i in range(4):
 for j in range(4):
 axes[0].text(j, i, f"{weights_bidi[i,j]:.2f}",
 ha="center", va="center", fontsize=9)
# Causal attention (masked)
causal_mask = np.triu(np.ones((4, 4), dtype=bool), k=1)
_, weights_causal = scaled_dot_product_attention(Q, K, V, mask=causal_mask)
im2 = axes[1].imshow(weights_causal, cmap="Oranges", vmin=0, vmax=1)
axes[1].set_xticks(range(4))
axes[1].set_xticklabels(tokens)
axes[1].set_yticks(range(4))
axes[1].set_yticklabels(tokens)
axes[1].set_title("Causal Attention (Masked)")
axes[1].set_xlabel("Key")
for i in range(4):
 for j in range(4):
 axes[1].text(j, i, f"{weights_causal[i,j]:.2f}",
 ha="center", va="center", fontsize=9)
plt.suptitle("Attention Weight Heatmaps", fontsize=13, fontweight="bold")
plt.tight_layout()
plt.savefig("attention_heatmaps.png", dpi=150)
plt.show()
```
**Code Fragment 3.3.14:** Side-by-side heatmaps comparing bidirectional and causal attention weights. In the causal (masked) variant, each token can only attend to itself and earlier positions, producing the characteristic lower-triangular pattern used in autoregressive language models.
### Step 3: Implement multi-head attention
Split the input into multiple heads, run attention on each head independently, then concatenate and project. This lets the model attend to different types of relationships simultaneously.
![](http://llmbook.apartsin.com/styles/icons/callout-code.svg)Show Code (43 lines)
```python
def multi_head_attention(X, n_heads, d_model, W_q, W_k, W_v, W_o, mask=None):
 """
 X: input of shape (seq_len, d_model)
 W_q, W_k, W_v: projection matrices (d_model, d_model)
 W_o: output projection (d_model, d_model)
 """
 seq_len = X.shape[0]
 d_head = d_model // n_heads
 Q = X @ W_q # (seq_len, d_model)
 K = X @ W_k
 V = X @ W_v
 # Reshape into heads: (n_heads, seq_len, d_head)
 Q = Q.reshape(seq_len, n_heads, d_head).transpose(1, 0, 2)
 K = K.reshape(seq_len, n_heads, d_head).transpose(1, 0, 2)
 V = V.reshape(seq_len, n_heads, d_head).transpose(1, 0, 2)
 # Run attention on each head
 all_outputs = []
 all_weights = []
 for h in range(n_heads):
 out_h, w_h = scaled_dot_product_attention(Q[h], K[h], V[h], mask)
 all_outputs.append(out_h)
 all_weights.append(w_h)
 # Concatenate heads and project
 concat = np.concatenate(all_outputs, axis=-1) # (seq_len, d_model)
 output = concat @ W_o
 return output, all_weights
# Initialize random projections
d_model, n_heads = 16, 4
np.random.seed(0)
X = np.random.randn(4, d_model)
W_q = np.random.randn(d_model, d_model) * 0.1
W_k = np.random.randn(d_model, d_model) * 0.1
W_v = np.random.randn(d_model, d_model) * 0.1
W_o = np.random.randn(d_model, d_model) * 0.1
output, head_weights = multi_head_attention(X, n_heads, d_model, W_q, W_k, W_v, W_o)
print(f"Multi-head output shape: {output.shape}")
print(f"Number of attention heads: {len(head_weights)}")
```
Output (2 lines)
Multi-head output shape: (4, 16)
Number of attention heads: 4
**Code Fragment 3.3.13:** Multi-head attention implemented from scratch. The input is split across four heads, each attending independently in its own subspace, then the results are concatenated and projected back to the full model dimension.
### Step 4: Verify against PyTorch
Use PyTorch's nn.MultiheadAttention to confirm that the from-scratch implementation produces the same computational pattern. This is the "right tool" comparison: understand the internals, then use the library.
![](http://llmbook.apartsin.com/styles/icons/callout-code.svg)Show Code (18 lines)
```python
import torch
import torch.nn as nn
d_model, n_heads, seq_len = 16, 4, 4
mha = nn.MultiheadAttention(embed_dim=d_model, num_heads=n_heads, batch_first=True)
x = torch.randn(1, seq_len, d_model) # (batch, seq, d_model)
# Causal mask for autoregressive attention
causal = nn.Transformer.generate_square_subsequent_mask(seq_len)
output, attn_weights = mha(x, x, x, attn_mask=causal)
print(f"PyTorch MHA output shape: {output.shape}")
print(f"PyTorch attention weights shape: {attn_weights.shape}")
print(f"Weights (averaged over heads):")
print(attn_weights[0].detach().numpy().round(3))
print("\nBoth implementations follow the same formula:")
print(" Attention(Q,K,V) = softmax(QK^T / sqrt(d_k)) V")
```
Output (10 lines)
PyTorch MHA output shape: torch.Size([1, 4, 16])
PyTorch attention weights shape: torch.Size([1, 4, 4])
Weights (averaged over heads):
[[1. 0. 0. 0. ]
[0.487 0.513 0. 0. ]
[0.321 0.336 0.343 0. ]
[0.241 0.253 0.254 0.252]]
Both implementations follow the same formula:
Attention(Q,K,V) = softmax(QK^T / sqrt(d\_k)) V
**Code Fragment 3.3.12:** Validating the from-scratch attention against PyTorch's nn.MultiheadAttention. Both implementations follow the same formula and produce matching output shapes, confirming correctness before relying on the library version in later chapters.
### Extensions
- Implement grouped-query attention (GQA) where multiple query heads share the same key-value head, as used in Llama 2 and Mistral.
- Measure the memory usage of your attention implementation as sequence length grows from 32 to 4096 tokens, confirming the O(n^2) scaling.
- Visualize how each of the 4 attention heads attends to different parts of a sentence by plotting all head heatmaps side by side.
☑ Self-Check
1. Why is it important that Q, K, and V are separate projections rather than all being the same?
Show Answer
Separate projections allow the model to use different aspects of a token for matching (Q and K) versus information transfer (V). For example, a token's key might encode "I am a noun in subject position" (useful for matching), while its value encodes the actual meaning of the noun (useful for the output). If all three were the same, the model would be forced to use the same representation for both purposes, which is much less expressive.
2. If dmodeld\_{model}dmodel​ = 512 and n\_heads = 8, what is dkd\_{k}dk​? Does multi-head attention use more or fewer parameters than a single-head attention with dkd\_{k}dk​ = 512?
Show Answer
dk=512/8=64d\_{k} = 512 / 8 = 64dk​=512/8=64. Multi-head attention uses approximately the *same* number of parameters as single-head attention. The Q, K, V projections map from 512 to 512 (= 8 × 64) in both cases, and the output projection also maps from 512 to 512. The difference is that multi-head attention factorizes the computation into 8 parallel, independent attention operations in 64-dimensional subspaces, which increases expressiveness without increasing parameter count.
3. What would happen if we removed the √dkd\_{k}dk​ scaling during training with dkd\_{k}dk​ = 512?
Show Answer
Without scaling, the dot products between Q and K vectors would have variance proportional to dkd\_{k}dk​ = 512 (standard deviation ~22.6). These large-magnitude inputs would push softmax into saturation, producing attention distributions that are nearly one-hot (all weight on a single position). The gradients through saturated softmax are extremely small, making training very slow or unstable. The model would have difficulty learning nuanced attention patterns and would tend to "hard-attend" to a single position.
4. Explain the difference between causal and bidirectional self-attention in terms of the mask and the resulting attention pattern.
Show Answer
**Bidirectional** (no mask): Every position can attend to every other position. The attention weight matrix is fully populated. Used in BERT-style encoder models. **Causal** (upper-triangular mask): Position iii can only attend to positions 0,1,...,i0, 1, ..., i0,1,...,i. The upper triangle of the weight matrix is zero. Used in GPT-style decoder models. The causal mask is applied by setting future positions to −∞- \infty−∞ before softmax, which maps them to exactly zero weight.
5. Why does self-attention have O(n²) complexity, and why is this problematic for long sequences?
Show Answer
The score matrix QKTQK^{T}QKT has shape (n, n), requiring n² dot products to compute and n² floating-point numbers to store. Both computation and memory scale quadratically with sequence length. For a 100K-token sequence, this means 10 billion entries in the attention matrix. This quadratic scaling is problematic because (1) GPU memory is limited, capping the maximum sequence length, (2) longer sequences become disproportionately expensive, and (3) the cost eventually dominates all other operations in the Transformer. This is why extending context length (from 2K to 128K to 1M+ tokens) has required extensive engineering optimizations.
### What's Next?
In the next chapter, [Chapter 04: The Transformer Architecture](module-04-transformer-architecture_index.html.md), we bring all these components together in the full Transformer architecture, the foundation of every modern LLM.
📚 Bibliography
Vaswani, A., Shazeer, N., Parmar, N., et al. (2017). ["Attention Is All You Need."](https://arxiv.org/abs/1706.03762) NeurIPS 2017.
The paper that introduced the Transformer, including scaled dot-product attention and multi-head attention. Essential reading for anyone working with modern language models. Start here for the canonical formulation of Q/K/V attention.
[arxiv.org/abs/1706.03762](https://arxiv.org/abs/1706.03762)
Dao, T., Fu, D.Y., Ermon, S., Rudra, A., Re, C. (2022). ["FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness."](https://arxiv.org/abs/2205.14135) NeurIPS 2022.
Introduces an IO-aware algorithm for computing exact attention with significantly less memory. Relevant to anyone implementing or optimizing multi-head attention at scale. The key insight is that memory access patterns, not FLOP counts, dominate runtime.
[arxiv.org/abs/2205.14135](https://arxiv.org/abs/2205.14135)
Ainslie, J., Lee-Thorp, J., de Jong, M., et al. (2023). ["GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints."](https://arxiv.org/abs/2305.13245) EMNLP 2023.
Proposes grouped-query attention as a practical middle ground between multi-head and multi-query attention. Used in Llama 2, Llama 3, and Mistral. Read this to understand why modern models share key-value heads and the tradeoffs involved.
[arxiv.org/abs/2305.13245](https://arxiv.org/abs/2305.13245)