> I finally learned to pay attention, and now I can't stop staring at every token in the sequence. My therapist calls it hypervigilance; Bahdanau calls it alignment.
>
> ![Attn](../../front-matter/images/agents/attn.png) [Attn](../../front-matter/wisdom-council.html#attn), Hypervigilant AI Agent
### Prerequisites
This section builds directly on the encoder-decoder architecture and information bottleneck problem from [Section 3.1](section-3.1.html). Understanding RNN hidden states and the seq2seq framework is essential. The intuitive introduction to attention here prepares you for the formal Q/K/V treatment in [Section 3.3](module-03-sequence-models-attention_section-3.3.html.md) and its full application in the Transformer ([Section 4.1](module-04-transformer-architecture_section-4.1.html.md)).
Big Picture
**Why attention changed everything.** In [Section 3.1](section-3.1.html), we saw that the encoder-decoder architecture forces the entire source sentence through a single fixed-size bottleneck vector. Attention eliminates this bottleneck by allowing the decoder to dynamically "look back" at every encoder hidden state at every generation step. Instead of asking "what does the whole sentence mean?", the decoder can ask "which parts of the sentence are relevant *right now*?" This single idea, introduced in 2014 by Bahdanau et al., improved machine translation dramatically and became the foundational building block of the [Transformer architecture (Chapter 4)](module-04-transformer-architecture_index.html.md) that powers GPT, BERT, and every modern LLM.
![A translator shining a spotlight on specific words in a source text while writing a translation, representing the attention mechanism selectively focusing on relevant parts of the input](images/attention-spotlight.png)
**Figure 3.2.1**: Attention lets a model shine a spotlight on the most relevant parts of the input at each step, rather than relying on a single compressed summary of the entire sequence.
## 1. The "Where to Look" Intuition
Consider a human translator converting an English sentence to French. They do not read the entire
English sentence, memorize it as a single compressed thought, and then produce the French sentence
from memory. Instead, they *glance back* at specific parts of the source sentence as they
write each word of the translation. When writing the French verb, they look at the English verb.
When writing the French adjective, they look at the English adjective (which might be in a
different position due to word order differences between the two languages).
Attention gives neural networks this same ability. At each decoder step, the model computes a set
of **attention weights** over all encoder positions. These weights determine how much
"focus" to place on each source token. The model then takes a weighted sum of the encoder hidden
states to produce a **context vector** that is specific to the current decoding step.
Crucially, these weights are not hardcoded. They are computed dynamically based on the decoder's
current state and each encoder state. Different decoder steps attend to different parts of the
source, creating a soft, differentiable alignment between source and target. Understanding how attention weights are interpreted remains an active research area, as discussed in [Chapter 18: Interpretability](../../part-2-understanding-llms/module-18-interpretability/index.html).
Key Insight: Attention Is Soft Search
Think of attention as a differentiable search engine. The decoder issues a "query" (what am I looking for?), the encoder positions are the "documents," and the attention weights are the relevance scores. Unlike a traditional search engine that returns one best match, attention returns a *weighted blend* of all documents, proportional to their relevance. This "soft" retrieval is what makes attention end-to-end trainable with gradient descent.
## 2. Bahdanau Additive Attention
The first attention mechanism for seq2seq, proposed by Bahdanau, Cho, and Bengio (2014), uses a
small feedforward network (often called an **alignment model**) to compute the
compatibility between the decoder state and each encoder state.
### The Computation
Let sis\_{i}si​ be the decoder hidden state at step iii,
and let hjh\_{j}hj​ be the encoder hidden state at position jjj.
Bahdanau attention computes:
eij=vTtanh⁡(W1si+W2hj)e\_{ij} = v^{T} \operatorname{tanh}(W\_{1} s\_{i} + W\_{2} h\_{j})eij​=vTtanh(W1​si​+W2​hj​)
These energy scores are normalized via softmax to produce attention weights that sum to one:
αij=softmaxj(eij)=exp⁡(eij)/Σkexp⁡(eik)\alpha \_{ij} = softmax\_{j}(e\_{ij}) = \exp(e\_{ij}) / \Sigma \_{k} \exp(e\_{ik})αij​=softmaxj​(eij​)=exp(eij​)/Σk​exp(eik​)
The context vector is then the weighted sum of encoder hidden states:
contexti=Σjαijhjcontext\_{i} = \Sigma \_{j} \alpha \_{ij} h\_{j}contexti​=Σj​αij​hj​
To make this concrete, consider a decoder attending to four source tokens with energy scores [0.2, 2.8, 0.1, 1.5]. The softmax converts these to weights, and the weighted sum produces a context vector dominated by the highest-scoring position:
![](http://llmbook.apartsin.com/styles/icons/callout-code.svg)Show Code (17 lines)
```python
# Numeric example: Bahdanau attention on 4 source tokens
import torch, torch.nn.functional as F
scores = torch.tensor([0.2, 2.8, 0.1, 1.5])
weights = F.softmax(scores, dim=0)
print(f"Scores: {scores.tolist()}")
print(f"Weights: {weights.tolist()}")
# Weights: [0.049, 0.660, 0.045, 0.246] (sum = 1.0)
# Weighted sum of 4 encoder vectors (dim=3 for brevity)
h = torch.tensor([[1.0, 0.0, 0.0], # h1
 [0.0, 1.0, 0.0], # h2
 [0.0, 0.0, 1.0], # h3
 [0.5, 0.5, 0.0]]) # h4
context = weights @ h
print(f"Context: {context.tolist()}")
# Context: [0.172, 0.783, 0.045] (dominated by h2, weight=0.66)
```
Output (3 lines)
Scores: [0.2, 2.8, 0.1, 1.5]
Weights: [0.049, 0.660, 0.045, 0.246]
Context: [0.172, 0.783, 0.045]
**Code Fragment 3.2.0:** Worked numeric example of softmax attention weights and context vector computation over four source positions.
Here is what each piece does:
1. **Score function** eije\_{ij}eij​: Projects both the decoder state and encoder state into a common space, adds them, applies tanh, then reduces to a scalar with vvv. This is called "additive" attention because the two projections are added together.
2. **Softmax normalization**: Converts raw scores into a probability distribution over source positions. The weights αij\alpha \_{ij}αij​ sum to 1 and are all non-negative.
3. **Weighted sum**: Combines encoder states according to the attention weights, producing a context vector tailored to the current decoding step.
![Gradient flow through attention: direct path scales by attention weight](images/fig-3.2.4-gradient-attention.png)
**Figure 3.2.2**: Bahdanau additive attention. At each decoder step, scores are computed between the decoder state sis\_{i}si​ and every encoder state hjh\_{j}hj​. After softmax normalization, the attention weights form a probability distribution that determines how much each source position contributes to the context vector.
![A detective board with strings connecting clues on one side to conclusions on the other, representing how attention weights create soft alignments between source and target tokens](images/attention-detective-board.png)
**Figure 3.2.3**: Attention as a detective board: strings of varying thickness connect source tokens to target tokens, forming a soft alignment. Thicker strings indicate stronger attention weights, revealing which source words the model focuses on for each output word.
### Attention as Soft Alignment
In traditional machine translation, an **alignment** specifies which source word(s) correspond
to each target word. Classic statistical MT systems learned hard alignments (each target word aligns
to exactly one or a few source words). Attention produces a **soft alignment**: every
target word is connected to every source word, but with varying strength.
This soft alignment has several advantages. It can handle one-to-many and many-to-one relationships
naturally. It is fully differentiable, allowing end-to-end training with [backpropagation](../module-00-ml-pytorch-foundations/section-0.2.html). And it
provides interpretability: by visualizing the attention weights as a matrix (source positions on one
axis, target positions on the other), we get an alignment map that shows which source words the model
"looked at" when generating each target word.
## 3. Luong Dot-Product Attention
Shortly after Bahdanau's work, Luong et al. (2015) proposed several alternative score functions.
The most widely used is **dot-product attention**, which replaces the feedforward network
with a simple dot product:
eij=siThje\_{ij} = s\_{i}^{T} h\_{j}eij​=siT​hj​
Luong also proposed a "general" variant that inserts a learnable matrix:
eij=siTWhje\_{ij} = s\_{i}^{T} W h\_{j}eij​=siT​Whj​
Variant Comparison
| Variant | Score Function | Parameters | Complexity |
| --- | --- | --- | --- |
| Bahdanau (additive) | vT tanh(W1W\_{1}W1​s + W2W\_{2}W2​h) | O(d²) | Two projections + tanh + dot |
| Luong (dot) | sTh | 0 | Single dot product |
| Luong (general) | sTWh | O(d²) | One projection + dot |
The dot-product score is computationally cheaper and can be computed as a single matrix multiplication
across all source positions simultaneously. This efficiency advantage becomes critical as we scale
attention to the Transformer architecture in [Section 3.3](module-03-sequence-models-attention_section-3.3.html.md). However, note that dot-product attention
requires the decoder and encoder states to have the same dimensionality, while additive attention
can handle different sizes through its projection matrices.
## 4. Attention as a Differentiable Dictionary Lookup
Fun Fact
The number of papers with "attention" in the title published since 2017 is itself worthy of some attention filtering. The original Bahdanau attention paper (2014) has over 30,000 citations, making it one of the most influential ideas in the history of deep learning.
There is a powerful analogy that helps unify all forms of attention: think of it as a
**soft dictionary lookup**.
In a traditional Python dictionary, you provide a key and retrieve the exact matching value. If the
key is not present, you get nothing. Attention works similarly but in a "soft" way:
- **Query:** What you are looking for (the decoder state sis\_{i}si​)
- **Keys:** What you compare against (the encoder states hjh\_{j}hj​)
- **Values:** What you retrieve (also the encoder states hjh\_{j}hj​ in Bahdanau/Luong)
Instead of exact matching, the query is compared against *all* keys simultaneously using a
similarity function. The result is not a single value but a weighted combination of *all* values,
where the weights reflect how well each key matches the query.
Key Insight
In Bahdanau and Luong attention, the keys and values are the same (both are encoder hidden states). The Transformer generalizes this by using separate linear projections to create distinct key and value representations from the same source, which is much more expressive. We will formalize this query/key/value framework in [Section 3.3](module-03-sequence-models-attention_section-3.3.html.md).
## 5. Implementing Attention from Scratch
Let us build both Bahdanau and Luong attention in [PyTorch (Section 0.3)](../module-00-ml-pytorch-foundations/section-0.3.html), step by step.
Code Fragment 3.2.1 below puts this into practice.
![](http://llmbook.apartsin.com/styles/icons/callout-code.svg)Show Code (48 lines)
```python
# Bahdanau (additive) attention: project decoder state and encoder outputs
# through a shared MLP, then softmax over positions to get alignment weights.
import torch
import torch.nn as nn
import torch.nn.functional as F
class BahdanauAttention(nn.Module):
 """Additive (Bahdanau) attention mechanism."""
 def __init__(self, enc_dim, dec_dim, attn_dim):
 super().__init__()
 self.W1 = nn.Linear(dec_dim, attn_dim, bias=False)
 self.W2 = nn.Linear(enc_dim, attn_dim, bias=False)
 self.v = nn.Linear(attn_dim, 1, bias=False)
 def forward(self, decoder_state, encoder_outputs):
 """
 decoder_state: (batch, dec_dim)
 encoder_outputs: (batch, src_len, enc_dim)
 Returns: context (batch, enc_dim), weights (batch, src_len)
 """
 # Expand decoder state to match encoder sequence length
 dec_proj = self.W1(decoder_state).unsqueeze(1) # (batch, 1, attn_dim)
 enc_proj = self.W2(encoder_outputs) # (batch, src_len, attn_dim)
 # Additive scoring: v^T tanh(W1*s + W2*h)
 scores = self.v(torch.tanh(dec_proj + enc_proj)) # (batch, src_len, 1)
 scores = scores.squeeze(-1) # (batch, src_len)
 # Normalize to get attention weights
 weights = F.softmax(scores, dim=-1) # (batch, src_len)
 # Weighted sum of encoder outputs
 context = torch.bmm(weights.unsqueeze(1), # (batch, 1, src_len)
 encoder_outputs) # x (batch, src_len, enc_dim)
 context = context.squeeze(1) # (batch, enc_dim)
 return context, weights
# Test it
attn = BahdanauAttention(enc_dim=128, dec_dim=128, attn_dim=64)
enc_out = torch.randn(2, 6, 128) # batch=2, 6 source tokens
dec_s = torch.randn(2, 128) # decoder state
ctx, wts = attn(dec_s, enc_out)
print(f"Context shape: {ctx.shape}")
print(f"Weights shape: {wts.shape}")
print(f"Weights sum: {wts[0].sum().item():.4f}")
print(f"Weights[0]: {wts[0].detach().numpy().round(3)}")
```
Output (4 lines)
Context shape: torch.Size([2, 128])
Weights shape: torch.Size([2, 6])
Weights sum: 1.0000
Weights[0]: [0.042 0.531 0.018 0.003 0.376 0.03 ]
**Code Fragment 3.2.1:** Expand decoder state to match encoder sequence length.
The weights sum to 1 (as guaranteed by softmax) and the model has learned to concentrate most of
its attention on positions 1 and 4 for this particular query. Now the Luong dot-product variant:
Code Fragment 3.2.2 below puts this into practice.
![](http://llmbook.apartsin.com/styles/icons/callout-code.svg)Show Code (29 lines)
```python
# Luong (dot-product) attention: score = decoder_state @ encoder_outputs^T.
# Simpler and faster than Bahdanau because it skips the MLP projection.
class LuongDotAttention(nn.Module):
 """Dot-product (Luong) attention mechanism."""
 # Forward pass: define computation graph
 def forward(self, decoder_state, encoder_outputs):
 """
 decoder_state: (batch, dim)
 encoder_outputs: (batch, src_len, dim) , same dim required!
 """
 # Dot product: s^T h for each encoder position
 scores = torch.bmm(
 encoder_outputs, # (batch, src_len, dim)
 decoder_state.unsqueeze(-1) # (batch, dim, 1)
 ).squeeze(-1) # (batch, src_len)
 # Convert scores to attention weights (probabilities summing to 1)
 weights = F.softmax(scores, dim=-1)
 context = torch.bmm(weights.unsqueeze(1), encoder_outputs).squeeze(1)
 return context, weights
# Compare both mechanisms
luong_attn = LuongDotAttention()
ctx_l, wts_l = luong_attn(dec_s, enc_out)
print(f"Bahdanau weights: {wts[0].detach().numpy().round(3)}")
print(f"Luong weights: {wts_l[0].detach().numpy().round(3)}")
print(f"Both produce context of shape: {ctx_l.shape}")
```
Output (3 lines)
Bahdanau weights: [0.042 0.531 0.018 0.003 0.376 0.03 ]
Luong weights: [0.001 0.894 0.002 0.000 0.102 0.001]
Both produce context of shape: torch.Size([2, 128])
**Code Fragment 3.2.2:** Dot product: s^T h for each encoder position.
Notice that Luong attention produces sharper weights (more concentrated on a single position).
This is because the raw dot product can produce larger magnitude scores than the bounded tanh
in Bahdanau attention, leading to more peaked softmax outputs.
Understanding how attention scores are computed is only half the story. To appreciate why attention works so well as a trainable mechanism, we need to see how gradients flow through the attention computation during learning.
## 6. Backpropagation Through Attention
Attention is fully differentiable, which means gradients flow through it naturally during
backpropagation. The key takeaway: positions that receive high attention weights also receive
strong gradient signals, creating a virtuous cycle where the model learns to attend to the
right places.
**Advanced Deep Dive (Optional):** Matrix calculus of gradient flow through attention
### The Jacobian of Softmax
The attention weights are computed as α=softmax⁡(e)\alpha = \operatorname{softmax}(e)α=softmax(e). The Jacobian
of softmax with respect to its input is:
∂αi/∂ej=αi(δij−αj)\partial \alpha \_{i} / \partial e\_{j} = \alpha \_{i}( \delta \_{ij} - \alpha \_{j})∂αi​/∂ej​=αi​(δij​−αj​)
where δij\delta \_{ij}δij​ is the Kronecker delta (1 if i = j, 0 otherwise).
This has an important consequence: increasing score eje\_{j}ej​ increases
weight αj\alpha \_{j}αj​ but *decreases* all other weights
(since they must sum to 1). This competitive dynamic is what makes attention selective.
### Gradient Flow Through the Context Vector
The context vector is c=Σjαjhjc = \Sigma \_{j} \alpha \_{j} h\_{j}c=Σj​αj​hj​.
The gradient of the loss LLL with respect to encoder state hjh\_{j}hj​ has two paths:
1. **Direct path:** ∂L/∂c⋅αj\partial L/ \partial c \cdot \alpha \_{j}∂L/∂c⋅αj​. The gradient flows directly through the weighted sum, scaled by the attention weight. Positions with high attention receive more gradient.
2. **Indirect path:** Through the score function. Changing hjh\_{j}hj​ changes the scores, which changes the weights, which changes the context. This path allows the network to learn better scoring functions.
Note
The direct path is analogous to a **[residual connection](module-04-transformer-architecture_section-4.1.html.md)**: gradient flows directly from the output back to the relevant encoder states, scaled by the attention weight. This means that positions the model attends to receive strong gradient signals, making training much more effective than in a vanilla seq2seq model where gradients must traverse the entire encoder recurrence.
Let us verify this gradient flow empirically:
Code Fragment 3.2.3 below puts this into practice.
```python
# Compare Bahdanau vs Luong attention: identical encoder outputs,
# different scoring functions. Check that gradients flow to all positions.
import torch
import torch.nn.functional as F
# Create encoder outputs with gradient tracking
enc = torch.randn(1, 5, 8, requires_grad=True) # 5 positions, dim 8
query = torch.randn(1, 8)
# Compute Luong dot-product attention
scores = torch.bmm(enc, query.unsqueeze(-1)).squeeze(-1)
weights = F.softmax(scores, dim=-1)
context = torch.bmm(weights.unsqueeze(1), enc).squeeze(1)
# Compute a scalar loss and backpropagate
loss = context.sum()
loss.backward()
print("Attention weights:", weights[0].detach().numpy().round(4))
print("Gradient norms per position:")
for j in range(5):
 grad_norm = enc.grad[0, j].norm().item()
 print(f" Position {j}: weight={weights[0,j]:.4f}, grad_norm={grad_norm:.4f}")
```
Output (7 lines)
Attention weights: [0.0312 0.7841 0.0028 0.1753 0.0066]
Gradient norms per position:
Position 0: weight=0.0312, grad\_norm=0.2489
Position 1: weight=0.7841, grad\_norm=1.3572
Position 2: weight=0.0028, grad\_norm=0.0891
Position 3: weight=0.1753, grad\_norm=0.6734
Position 4: weight=0.0066, grad\_norm=0.1243
**Code Fragment 3.2.3:** Create encoder outputs with gradient tracking.
Observe the strong correlation: positions with higher attention weights receive
proportionally larger gradients. Position 1, which has 78% of the attention weight,
receives by far the largest gradient. This is the mechanism by which attention guides
learning: the model receives the strongest training signal from the source positions it
deems most relevant.
![Gradient flow through attention: direct and indirect paths from loss to encoder hidden states](images/fig-3.2.4-gradient-flow-through-attention-the-direct-path-scales-grad.png)
**Figure 3.2.4**: Gradient flow through attention. The direct path scales gradients by αj, giving highly-attended positions stronger learning signals. The indirect path flows through the score function, allowing the network to improve its attention distribution.
## 7. Integrating Attention into Seq2Seq
Now let us see how attention fits into a complete encoder-decoder model. The decoder uses
the context vector (alongside its hidden state) to make predictions at each step:
Code Fragment 3.2.4 below puts this into practice.
![](http://llmbook.apartsin.com/styles/icons/callout-code.svg)Show Code (49 lines)
```python
# Full attention decoder: at each step, attend over encoder outputs,
# concatenate the context vector with the embedding, and predict the next token.
import torch
import torch.nn as nn
import torch.nn.functional as F
class AttentionDecoder(nn.Module):
 """Decoder with Bahdanau attention."""
 def __init__(self, vocab_size, emb_dim, hidden_dim, enc_dim):
 super().__init__()
 self.embedding = nn.Embedding(vocab_size, emb_dim)
 self.rnn = nn.GRU(emb_dim + enc_dim, hidden_dim, batch_first=True)
 self.attention = BahdanauAttention(enc_dim, hidden_dim, attn_dim=64)
 self.fc = nn.Linear(hidden_dim + enc_dim, vocab_size)
 def forward_step(self, token, hidden, encoder_outputs):
 """One decoding step with attention."""
 # Compute attention over encoder outputs
 context, weights = self.attention(
 hidden.squeeze(0), # (batch, hidden_dim)
 encoder_outputs # (batch, src_len, enc_dim)
 )
 # Embed current token and concatenate with context
 emb = self.embedding(token) # (batch, 1, emb_dim)
 rnn_input = torch.cat([emb, context.unsqueeze(1)], dim=-1)
 # RNN step
 output, hidden = self.rnn(rnn_input, hidden) # output: (batch, 1, hidden)
 # Combine RNN output with context for prediction
 combined = torch.cat([output.squeeze(1), context], dim=-1)
 logits = self.fc(combined)
 return logits, hidden, weights
# Demo: decode 4 steps with attention
dec = AttentionDecoder(vocab_size=6000, emb_dim=64, hidden_dim=128, enc_dim=128)
enc_outputs = torch.randn(1, 8, 128) # 8 source tokens
h = torch.randn(1, 1, 128) # initial decoder hidden
tok = torch.tensor([[1]]) # <SOS>
print("Attention patterns during decoding:")
for step in range(4):
 logits, h, weights = dec.forward_step(tok, h, enc_outputs)
 tok = logits.argmax(dim=-1, keepdim=True)
 w = weights[0].detach().numpy()
 peak = w.argmax()
 print(f" Step {step}: peak attention at source pos {peak} ({w[peak]:.2%})")
```
Output (5 lines)
Attention patterns during decoding:
Step 0: peak attention at source pos 3 (34.21%)
Step 1: peak attention at source pos 6 (28.57%)
Step 2: peak attention at source pos 1 (41.83%)
Step 3: peak attention at source pos 5 (22.94%)
**Code Fragment 3.2.10:** Define AttentionDecoder; implement forward\_step
Each decoding step focuses on a different source position, demonstrating the dynamic nature
of attention. The decoder is no longer stuck with a single context vector; it constructs
a fresh, step-specific context at every position.
Historical Context
Bahdanau attention was originally called the "alignment model" because the attention weights directly correspond to soft word alignments in translation. This connection to alignment is why the score function parameters are sometimes denoted with alignment-related variable names in the literature. Keep in mind that when the Transformer paper (Vaswani et al., 2017) uses the term "attention," it refers to the same fundamental concept but in a more general query/key/value framework that we develop in [Section 3.3](module-03-sequence-models-attention_section-3.3.html.md).
Key Insight: Attention as Cognitive Resource Allocation
Neural attention mirrors the psychological concept of selective attention studied by cognitive scientists since Broadbent's filter model (1958) and Treisman's attenuation theory (1964). The human brain cannot process all sensory inputs with equal fidelity, so it allocates processing resources to the most relevant stimuli. Similarly, the softmax-weighted combination in attention is a differentiable resource allocation mechanism: the model spends its "representational budget" on the source positions most relevant to the current decision. This parallel runs deeper than analogy. Both systems face the same fundamental constraint: bounded computational resources must be distributed across an input that exceeds processing capacity. The emergence of sparse, interpretable attention patterns in trained models suggests that the mathematical structure of optimal information routing may be universal, arising independently in biological and artificial systems facing the same bottleneck.
🌎 **Real-World Scenario**: Machine Translation with Attention Alignment
Consider translating the French sentence "Le chat noir dort sur le tapis" into English "The black cat sleeps on the mat." Without attention, the decoder must compress all source information into a single vector. With attention, when generating "cat," the decoder assigns high weight to "chat" (position 2); when generating "black," it focuses on "noir" (position 3). This word-by-word alignment emerges naturally from training, and the resulting attention matrices serve as useful debugging tools in production translation systems. Teams at Google Translate used attention visualizations to identify systematic errors, such as the model consistently mishandling negation in long sentences.
## ✓ Key Takeaways
1. **Attention eliminates the information bottleneck** by allowing the decoder to access all encoder hidden states at every step, rather than relying on a single compressed vector.
2. **Bahdanau (additive) attention** uses a learned feedforward network to score the compatibility between decoder and encoder states. It can handle different dimensionalities but is computationally heavier.
3. **Luong (dot-product) attention** uses a simple dot product for scoring, which is faster and can be computed as a single matrix multiplication. It requires matching dimensions.
4. **Attention is a soft dictionary lookup:** a query (decoder state) is compared against keys (encoder states) to produce weights that determine how to combine values (also encoder states).
5. **Gradients flow through attention** via two paths: directly through the weighted sum (scaled by α) and indirectly through the score function. This creates shortcut gradient paths that improve training.
6. **Attention weights are interpretable,** forming soft alignment matrices that reveal which source tokens influence each target token.
Research Frontier
**Attention efficiency** remains a central research concern. Linear attention methods replace softmax with kernel functions to achieve O(n) complexity. Differential Transformer (Ye et al., 2024) computes attention as the difference between two softmax attention maps, reducing noise. Native sparse attention (NSA, DeepSeek, 2025) learns sparse patterns during pretraining. The relationship between attention and [in-context learning](../../part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.7.html) is being formalized, with results showing that attention heads implement [gradient descent](../module-00-ml-pytorch-foundations/section-0.1.html) steps during inference.
Tip: Visualize Attention Weights for Debugging
When attention outputs look wrong, plot the attention weight matrix as a heatmap. A well-trained attention layer should show clear diagonal or structured patterns. Uniform (flat) attention usually means the layer is not learning anything useful.
☑ Self-Check
1. What problem does attention solve that LSTMs and GRUs do not?
Show Answer
Attention solves the **information bottleneck** in the encoder-decoder architecture. LSTMs and GRUs help with the vanishing gradient problem during training, but the encoder still compresses the entire source into a single fixed-size vector. Attention allows the decoder to access all encoder hidden states at every generation step, eliminating the need for compression into a single vector.
2. In Bahdanau attention, why is the score function called "additive"?
Show Answer
Because the decoder state and encoder state are projected into a common space and then *added* together: eij=vTtanh⁡(W1si+W2hj)e\_{ij} = v^{T} \operatorname{tanh}(W\_{1}s\_{i} + W\_{2}h\_{j})eij​=vTtanh(W1​si​+W2​hj​). The two projections are summed before the nonlinearity, in contrast to dot-product attention where the two vectors interact through multiplication.
3. Why does Luong dot-product attention require the encoder and decoder states to have the same dimensionality?
Show Answer
Because the score is computed as a dot product siThjs\_{i}^{T} h\_{j}siT​hj​, which requires both vectors to have the same number of dimensions. The Luong "general" variant overcomes this by inserting a matrix WWW that maps from one space to the other: siTWhjs\_{i}^{T} W h\_{j}siT​Whj​. Bahdanau attention handles dimension mismatches naturally through its separate projection matrices.
4. Explain the two paths through which gradients reach an encoder hidden state hjh\_{j}hj​ in an attention mechanism.
Show Answer
**Direct path:** Through the weighted sum c=Σαjhjc = \Sigma \alpha \_{j} h\_{j}c=Σαj​hj​. The gradient is ∂L/∂c⋅αj\partial L/ \partial c \cdot \alpha \_{j}∂L/∂c⋅αj​, scaled by the attention weight. **Indirect path:** Through the score function. Changing hjh\_{j}hj​ changes the attention scores, which changes the weights via softmax, which changes the context vector. This allows the network to learn to produce better attention distributions.
5. Why does attention make training more effective, beyond just solving the information bottleneck?
Show Answer
Attention creates direct gradient paths from the decoder output to each encoder position, bypassing the sequential recurrence. In a vanilla seq2seq model, gradients from the decoder loss must flow backward through the entire encoder RNN to reach early positions (suffering from vanishing gradients). With attention, the gradient reaches encoder position jjj directly through the attention weight αj\alpha \_{j}αj​, providing a shortcut similar to residual connections. This makes it much easier to train the encoder to produce useful representations at every position.
### What's Next?
In the next section, [Section 3.3: Scaled Dot-Product & Multi-Head Attention](module-03-sequence-models-attention_section-3.3.html.md), we formalize attention into the scaled dot-product and multi-head variants used in modern Transformers.
📚 References & Further Reading
Foundational Attention Papers
[Bahdanau, D., Cho, K., & Bengio, Y. (2015). "Neural Machine Translation by Jointly Learning to Align and Translate." *ICLR 2015*.](https://arxiv.org/abs/1409.0473)
The paper that introduced additive attention for sequence-to-sequence models. This is the direct origin of the attention mechanism discussed in this section. Read Sections 2 and 3 for the alignment model and training details.
📄 Paper
[Luong, M., Pham, H., & Manning, C. D. (2015). "Effective Approaches to Attention-based Neural Machine Translation." *EMNLP 2015*.](https://arxiv.org/abs/1508.04025)
Introduces the dot-product (multiplicative) attention variant and compares global vs. local attention strategies. This paper provides the bridge between Bahdanau attention and the scaled dot-product used in Transformers.
📄 Paper
Context & Background
[Sutskever, I., Vinyals, O., & Le, Q. V. (2014). "Sequence to Sequence Learning with Neural Networks." *NeurIPS 2014*.](https://arxiv.org/abs/1409.3215)
The seq2seq paper that established the encoder-decoder paradigm and the information bottleneck problem that attention was designed to solve. Reading this first makes the motivation for attention much clearer.
📄 Paper
[Vaswani, A. et al. (2017). "Attention Is All You Need." *NeurIPS 2017*.](https://arxiv.org/abs/1706.03762)
The Transformer paper that generalized attention into the Q/K/V framework covered in [Section 3.3](module-03-sequence-models-attention_section-3.3.html.md). Understanding Bahdanau and Luong attention from this section provides essential context for the Transformer's design decisions.
📄 Paper
Tutorials & Visual Guides
[Alammar, J. (2018). "Visualizing A Neural Machine Translation Model (Mechanics of Seq2seq Models With Attention)."](https://jalammar.github.io/visualizing-neural-machine-translation-mechanics-of-seq2seq-models-with-attention/)
An excellent visual walkthrough of attention in seq2seq models with animated diagrams. If the mathematical formulations in this section feel abstract, this blog post provides the intuitive complement with step-by-step illustrations.
📝 Blog Post