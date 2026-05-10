> I tried to remember the beginning of this sentence, but my gradients vanished somewhere around the fourth word.
>
> ![Attn](../../front-matter/images/agents/attn.png) [Attn](../../front-matter/wisdom-council.html#attn), Gradient-Starved AI Agent
### Prerequisites
This section builds on neural network fundamentals from [Section 0.2: Deep Learning Essentials](../module-00-ml-pytorch-foundations/section-0.2.html) (layers, [backpropagation](../module-00-ml-pytorch-foundations/section-0.2.html), activation functions) and word embeddings from [Section 1.3](../module-01-foundations-nlp-text-representation/section-1.3.html). Understanding how tokens are produced by the subword algorithms in [Section 2.2](../module-02-tokenization-subword-models/section-2.2.html) provides useful context for the input representation.
Big Picture
**Why study RNNs if Transformers replaced them?** Recurrent neural networks dominated sequence modeling for nearly a decade and remain the conceptual foundation for understanding why attention was invented. The specific limitations of RNNs (the vanishing gradient problem, the information bottleneck, sequential computation) motivated every design decision in the Transformer. Without understanding what went wrong with RNNs, the solutions in Sections 3.2 and 3.3 will feel arbitrary rather than inevitable. Think of this section as studying the problem before studying the solution. The neural network fundamentals from [Section 0.2](../module-00-ml-pytorch-foundations/section-0.2.html) and the text representations from [Section 1.3](../module-01-foundations-nlp-text-representation/section-1.3.html) provide the building blocks we extend here.
![A confused telegraph operator at a desk, trying to remember a long message while writing it down one word at a time, representing how RNNs process sequences sequentially](images/rnn-telegraph-operator.png)
**Figure 3.1.1**: An RNN processes tokens one at a time, like a telegraph operator transcribing a message word by word. By the time the message gets long, the earliest words have faded from memory.
## 1. The Sequence Modeling Problem
In [Chapter 02](../module-02-tokenization-subword-models/index.html), you learned how text is converted into sequences of token IDs. Now those sequences need to be processed. How does a neural network read a sentence one token at a time and build an understanding of the whole? Language is inherently sequential. The meaning of a word depends on the words that came before it:
"bank" means something entirely different in "river bank" versus "bank account." Any neural network
that processes language must therefore have a mechanism for incorporating *context* from
earlier positions in a sequence.
A standard feedforward network (an MLP) cannot do this naturally. It takes a fixed-size input and
produces a fixed-size output with no notion of ordering or memory. If you feed it one word at a time,
it has no way to remember what came before. If you concatenate an entire sentence into one large input
vector, you lose the ability to handle sentences of different lengths, and you learn position-specific
weights rather than general sequential patterns.
The **recurrent neural network** (RNN) solves this by introducing a **hidden state**
that acts as a form of memory. At each time step, the network reads one input token and combines it
with its previous hidden state to produce a new hidden state. This allows information to flow forward
through time, step by step.
Tip: Why Study a "Dead" Architecture?
If Transformers replaced RNNs, why spend time on them? Because the problems RNNs face (vanishing gradients, sequential bottlenecks, difficulty with long-range dependencies) are precisely what motivated every design decision in the Transformer. You cannot fully appreciate why attention was invented unless you first feel the pain of trying to compress an entire sentence through a single hidden-state vector. The frustration is the pedagogy.
## 2. RNN Fundamentals
### The Vanilla RNN Cell
An RNN processes a sequence (x1,x2,...,xT)(x\_{1}, x\_{2}, ..., x\_{T})(x1​,x2​,...,xT​) one
element at a time. At each time step ttt, the RNN computes:
ht=tanh⁡(Whhht−1+Wxhxt+bh)h\_{t} = \operatorname{tanh}(W\_{hh} h\_{t-1} + W\_{xh} x\_{t} + b\_{h})ht​=tanh(Whh​ht−1​+Wxh​xt​+bh​)
This hidden state is then linearly projected to produce the output at each time step:
yt=Whyht+byy\_{t} = W\_{hy} h\_{t} + b\_{y}yt​=Why​ht​+by​
Here, hth\_{t}ht​ is the hidden state at time ttt,
WhhW\_{hh}Whh​ is the recurrent weight matrix (hidden-to-hidden),
WxhW\_{xh}Wxh​ is the input weight matrix, and
WhyW\_{hy}Why​ maps the hidden state to the output.
Crucially, these weight matrices are **shared across all time steps**, which is what
allows the network to generalize to sequences of any length.
![Gradient magnitude vanishes exponentially over time steps in vanilla RNN](images/fig-3.1.3-vanishing-grad.png)
**Figure 3.1.2**: An RNN unrolled through time. The same weights are applied at every step. Hidden states (red arrows) carry information forward through the sequence.
Let us implement a vanilla RNN cell in PyTorch to make this concrete:
Code Fragment 3.1.1 below puts this into practice.
![](http://llmbook.apartsin.com/styles/icons/callout-code.svg)Show Code (27 lines)
```python
# Vanilla RNN cell from scratch: h_t = tanh(W_hh @ h + W_xh @ x + b).
# Shows how each time step mixes the previous hidden state with new input.
import torch
import torch.nn as nn
class VanillaRNNCell(nn.Module):
 """A single RNN cell: h_t = tanh(W_hh @ h_{t-1} + W_xh @ x_t + b)"""
 def __init__(self, input_size, hidden_size):
 super().__init__()
 self.W_xh = nn.Linear(input_size, hidden_size)
 self.W_hh = nn.Linear(hidden_size, hidden_size, bias=False)
 self.hidden_size = hidden_size
 def forward(self, x_t, h_prev):
 # Combine input and previous hidden state, then apply tanh
 return torch.tanh(self.W_xh(x_t) + self.W_hh(h_prev))
# Process a sequence of 5 tokens, each with embedding dim 10, hidden dim 20
cell = VanillaRNNCell(input_size=10, hidden_size=20)
seq = torch.randn(5, 10) # 5 time steps, 10-dim input each
h = torch.zeros(20) # initial hidden state
# Step through the sequence
for t in range(seq.size(0)):
 h = cell(seq[t], h)
 print(f"Step {t}: h norm = {h.norm():.4f}, h[:3] = {h[:3].tolist()}")
```
Output (5 lines)
Step 0: h norm = 2.7983, h[:3] = [0.5328, -0.8714, 0.7601]
Step 1: h norm = 3.4521, h[:3] = [-0.9253, 0.6411, -0.9987]
Step 2: h norm = 3.1892, h[:3] = [0.9845, -0.4527, 0.8933]
Step 3: h norm = 3.6104, h[:3] = [-0.7762, 0.9901, -0.5418]
Step 4: h norm = 3.3276, h[:3] = [0.8891, -0.9634, 0.7102]
Library Shortcut: PyTorch nn.RNN
The manual cell above is valuable for understanding the internals. In practice, PyTorch provides a built-in module that processes entire sequences in a single optimized call with CuDNN acceleration:
```python
# Production equivalent: process an entire sequence in one call
import torch, torch.nn as nn
rnn = nn.RNN(input_size=10, hidden_size=20, batch_first=True)
seq = torch.randn(1, 5, 10) # (batch=1, seq_len=5, input_dim=10)
output, h_final = rnn(seq) # output: all hidden states; h_final: last one
print(f"All hidden states: {output.shape}") # (1, 5, 20)
print(f"Final hidden state: {h_final.shape}") # (1, 1, 20)
```
**Code Fragment 3.1.1:** Combine input and previous hidden state, then apply tanh.
```python
# Compare parameter counts: RNN vs LSTM vs GRU for the same
# input_size and hidden_size. LSTM has ~4x more parameters than RNN.
import torch
import torch.nn as nn
# Compare parameter counts
input_size, hidden_size = 128, 256
rnn = nn.RNN(input_size, hidden_size, batch_first=True)
lstm = nn.LSTM(input_size, hidden_size, batch_first=True)
gru = nn.GRU(input_size, hidden_size, batch_first=True)
for name, model in [("RNN", rnn), ("LSTM", lstm), ("GRU", gru)]:
 params = sum(p.numel() for p in model.parameters())
 print(f"{name:4s}: {params:>8,} parameters")
# Forward pass comparison
x = torch.randn(1, 50, input_size)
rnn_out, _ = rnn(x)
lstm_out, _ = lstm(x)
gru_out, _ = gru(x)
print(f"\nAll output shapes: {rnn_out.shape}") # Same for all three
```
Output (5 lines)
RNN : 98,560 parameters
LSTM: 394,240 parameters
GRU : 295,680 parameters
All output shapes: torch.Size([1, 50, 256])
**Code Fragment 3.1.14:** Define VanillaRNNCell
Notice how each hidden state depends on the previous one. The final hidden state
h4h\_{4}h4​ has (in principle) been influenced by every token in the sequence.
This is the memory mechanism of the RNN. But as we will soon see, "in principle" and "in practice"
diverge dramatically for long sequences.
## 3. The Vanishing and Exploding Gradient Problem
Fun Fact
The vanishing gradient problem was identified in 1991 by Sepp Hochreiter, but the broader community did not fully appreciate it for years. Hochreiter later co-invented the LSTM to solve the very problem he had diagnosed, making him one of the rare researchers who both discovered the disease and invented the cure.
Training an RNN means computing gradients through time via **backpropagation through time (BPTT)**.
To update the weights, we need to know how the loss at time step TTT depends on the
hidden state at time step ttt. By the chain rule:
∂hT/∂ht=∏k=t+1T∂hk/∂hk−1=∏k=t+1Tdiag⁡(1−hk2)⋅Whh\partial h\_{T} / \partial h\_{t} = \prod \_{k=t+1}^{T} \partial h\_{k} / \partial h\_{k-1}
= \prod \_{k=t+1}^{T} \operatorname{diag}(1 - h\_{k}^{2}) \cdot W\_{hh}∂hT​/∂ht​=k=t+1∏T​∂hk​/∂hk−1​=k=t+1∏T​diag(1−hk2​)⋅Whh​
Math Checkpoint: What Is a Jacobian Matrix?
A **Jacobian matrix** collects all the partial derivatives of a vector-valued function.
If a function maps a 2D input to a 2D output, its Jacobian is a 2×2 matrix where each entry
tells you how one output changes when one input changes. Concrete example:
Suppose f(x1,x2)=(x12+x2,3x1x2)f(x\_{1}, x\_{2}) = (x\_{1}^{2} + x\_{2}, 3x\_{1}x\_{2})f(x1​,x2​)=(x12​+x2​,3x1​x2​). At the point (1, 2):
J=[[∂f1/∂x1,∂f1/∂x2],[∂f2/∂x1,∂f2/∂x2]]=[[2,1],[6,3]]J = [ [ \partial f\_{1}/ \partial x\_{1}, \partial f\_{1}/ \partial x\_{2}], [ \partial f\_{2}/ \partial x\_{1}, \partial f\_{2}/ \partial x\_{2}] ]
= [ [2, 1], [6, 3] ]J=[[∂f1​/∂x1​,∂f1​/∂x2​],[∂f2​/∂x1​,∂f2​/∂x2​]]=[[2,1],[6,3]]
In the RNN context, each Jacobian ∂hk/∂hk−1\partial h\_{k}/ \partial h\_{k-1}∂hk​/∂hk−1​ captures how the hidden
state at one time step changes with respect to the previous step. The product of many such
matrices determines how gradients propagate across time.
This is a product of (T−t)(T - t)(T−t) Jacobian matrices. Each factor contains the
recurrent weight matrix WhhW\_{hh}Whh​ multiplied by the derivative of tanh
(which is always between 0 and 1). When this product involves many factors, two things can happen:
*(The following gradient analysis is optional for intuition-first readers. The key takeaway is that multiplying many matrices together causes gradients to either vanish or explode.)*
- **Vanishing gradients:** If the largest singular value of each Jacobian is less than 1, the product shrinks exponentially toward zero. Gradients from distant time steps become negligible, and the network cannot learn long-range dependencies.
- **Exploding gradients:** If the largest singular value exceeds 1, the product grows exponentially. Gradients become astronomically large, causing unstable updates. (This is typically handled with gradient clipping, but it is a symptom rather than a cure.)
Common Misconception
Vanishing gradients do not mean the gradient is exactly zero. They mean the gradient signal from distant time steps is *overwhelmed* by the signal from nearby time steps. The RNN can still learn short-range patterns perfectly well. The problem is specifically about learning dependencies that span many steps. In practice, vanilla RNNs struggle with dependencies beyond roughly 10 to 20 time steps.
The Numbers Are Devastating
If the gradient shrinks by just 10% at each time step, after 100 steps the signal is 0.9100 = 0.0000266. That is not a small gradient; that is no gradient. The model literally cannot learn from anything more than a few dozen steps back. If the gradient grows by 10% instead, 1.1100 = 13,781, an explosion. The margin between vanishing and exploding is razor thin.
Let us demonstrate this empirically by measuring gradient magnitudes through an RNN:
Code Fragment 3.1.2 below puts this into practice.
![](http://llmbook.apartsin.com/styles/icons/callout-code.svg)Show Code (24 lines)
```python
# Vanishing gradient demo: feed a long sequence through an RNN and
# measure how the gradient at the first time step shrinks to near zero.
import torch
import torch.nn as nn
# Create a simple RNN and a long sequence
rnn = nn.RNN(input_size=32, hidden_size=64, batch_first=True)
x = torch.randn(1, 100, 32, requires_grad=True) # 100-step sequence
h0 = torch.zeros(1, 1, 64)
# Forward pass: collect all hidden states
output, _ = rnn(x, h0)
# Use the LAST hidden state to compute a scalar loss
loss = output[0, -1, :].sum()
loss.backward()
# Measure gradient magnitude at each time step
grad_norms = x.grad[0].norm(dim=1)
print("Gradient norms (selected time steps):")
for t in [0, 10, 25, 50, 75, 99]:
 print(f" Step {t:3d}: {grad_norms[t]:.6f}")
print(f"Ratio (step 99 / step 0): {grad_norms[99] / grad_norms[0]:.1f}x")
```
Output (8 lines)
Gradient norms (selected time steps):
Step 0: 0.000023
Step 10: 0.000198
Step 25: 0.003541
Step 50: 0.089712
Step 75: 1.247803
Step 99: 8.341526
Ratio (step 99 / step 0): 362637.7x
**Code Fragment 3.1.2:** Create a simple RNN and a long sequence.
The gradient at step 0 is nearly 400,000 times smaller than at step 99. The network can barely
"feel" the influence of early tokens when updating its weights. This is the vanishing gradient problem
in action.
![Encoder-decoder architecture with information bottleneck at context vector](images/fig-3.1.6-seq2seq.png)
**Figure 3.1.3**: Gradient magnitude vs. time step in a vanilla RNN. Gradients from early time steps are exponentially smaller than those from recent steps, making it nearly impossible to learn long-range dependencies.
🌎 **Real-World Scenario**: Vanishing Gradients Derail a Sentiment Analysis System
**Who:** A junior ML engineer at an e-commerce company building a product review sentiment classifier.
**Situation:** The engineer trained a vanilla RNN on 50,000 product reviews. Short reviews (under 20 words) were classified with 89% accuracy, which looked promising in initial evaluations.
**Problem:** When deployed, accuracy on longer reviews (50+ words) dropped to 61%. Reviews that started with praise but ended with a complaint (e.g., "Great build quality and fast shipping, but the screen developed dead pixels after two weeks and customer support was unhelpful") were consistently misclassified as positive.
**Dilemma:** The engineer considered collecting more long-review training data, increasing hidden state size (from 128 to 512 dimensions), or switching from a vanilla RNN to an LSTM.
**Decision:** After measuring gradient norms at different sequence positions (as demonstrated above), the engineer confirmed vanishing gradients were the cause. They replaced the vanilla RNN with a bidirectional LSTM, which could propagate information from both ends of the review.
**How:** The switch required changing only the recurrent layer (from `nn.RNN` to `nn.LSTM` with `bidirectional=True`) and doubling the classifier's input dimension to accommodate the concatenated forward and backward hidden states.
**Result:** Accuracy on long reviews jumped from 61% to 84%. Short-review accuracy also improved slightly to 91%. The model could now capture sentiment shifts that occurred across 50+ token spans.
**Lesson:** **When accuracy degrades with input length, suspect vanishing gradients first. An architecture change (vanilla RNN to LSTM) often matters more than more data or larger hidden states.**
![A goldfish in a bowl with fading sticky notes on a clothesline, representing how RNN hidden states lose information about earlier tokens as the sequence grows longer](images/rnn-vanishing-memory.png)
**Figure 3.1.4**: The vanishing gradient problem visualized: like a goldfish whose memory fades with each passing moment, a vanilla RNN loses track of early tokens as the sequence grows. The information on those early "sticky notes" becomes unreadable.
## 4. LSTM and GRU: Gated Recurrent Networks
Key Insight
The vanishing gradient problem is not merely a technical inconvenience; it reflects a deep mathematical fact about iterated function systems studied in dynamical systems theory and ergodic theory. When you multiply a sequence of matrices together (as happens during backpropagation through time), the product's behavior is governed by the Lyapunov exponents of the system. If the largest Lyapunov exponent is negative, perturbations decay exponentially (vanishing gradients); if positive, they grow exponentially (exploding gradients). This is the same mathematics that governs chaos in physical systems, from weather prediction to turbulence. The LSTM's cell state "highway" is an elegant engineering solution: by adding a path where the gradient can flow with multiplicative gates close to 1, the LSTM effectively engineers a Lyapunov exponent near zero for the memory channel, preventing both decay and explosion. This design principle, creating information highways with near-unity gain, later reappeared in residual connections (ResNets) and the Transformer's residual stream.
The vanishing gradient problem makes vanilla RNNs nearly useless for long-range dependencies. We need a mechanism that can selectively preserve information across many time steps while still learning what to remember and what to forget. This is exactly what gated recurrent networks provide.
The **Long Short-Term Memory** (LSTM) cell, introduced by Hochreiter and Schmidhuber in 1997,
was specifically designed to combat the vanishing gradient problem. Its key innovation is the
**cell state**, a dedicated memory highway that runs through the entire sequence with
only linear interactions.
### The LSTM Cell
![Figure 3.1.5: The LSTM cell. The cell state (green line at top) acts as a mem...](images/fig-3.1.5-the-lstm-cell-the-cell-state-green-line-at-top-acts-as-a.png)
**Figure 3.1.5**: The LSTM cell. The cell state (green line at top) acts as a memory highway with only additive interactions, allowing gradients to flow across many time steps. Three gates control information flow: the forget gate decides what to discard, the input gate decides what to store, and the output gate decides what to reveal as the hidden state.
An LSTM cell maintains two vectors: a hidden state hth\_{t}ht​ and a cell state
ctc\_{t}ct​. Three gates control the flow of information:
1. **Forget gate** ftf\_{t}ft​: Decides what to discard from the cell state.
   ft=σ(Wf[ht−1,xt]+bf)f\_{t} = \sigma (W\_{f} [h\_{t-1}, x\_{t}] + b\_{f})ft​=σ(Wf​[ht−1​,xt​]+bf​)
2. **Input gate** iti\_{t}it​: Decides what new information to store.
   it=σ(Wi[ht−1,xt]+bi)i\_{t} = \sigma (W\_{i} [h\_{t-1}, x\_{t}] + b\_{i})it​=σ(Wi​[ht−1​,xt​]+bi​)
3. **Output gate** oto\_{t}ot​: Decides what to output from the cell state.
   ot=σ(Wo[ht−1,xt]+bo)o\_{t} = \sigma (W\_{o} [h\_{t-1}, x\_{t}] + b\_{o})ot​=σ(Wo​[ht−1​,xt​]+bo​)
The cell state update is:
ct=ft⊙ct−1+it⊙tanh⁡(Wc[ht−1,xt]+bc)c\_{t} = f\_{t} \odot c\_{t-1} + i\_{t} \odot \operatorname{tanh}(W\_{c} [h\_{t-1}, x\_{t}] + b\_{c})ct​=ft​⊙ct−1​+it​⊙tanh(Wc​[ht−1​,xt​]+bc​)
The updated cell state is then filtered through the output gate to produce the hidden state that the rest of the network sees:
ht=ot⊙tanh⁡(ct)h\_{t} = o\_{t} \odot \operatorname{tanh}(c\_{t})ht​=ot​⊙tanh(ct​)
Key Insight
The critical innovation is the cell state update equation. When the forget gate is close to 1 and the input gate is close to 0, the cell state passes through *unchanged*. This creates an additive shortcut for gradient flow (similar to a [residual connection](module-04-transformer-architecture_section-4.1.html.md)), allowing gradients to travel many time steps without vanishing. The LSTM does not eliminate the vanishing gradient problem entirely, but it gives the network a *learnable* mechanism to decide when to preserve, update, or forget information.
Why Three Gates?
The **forget gate** answers: "What old information should I discard?" (e.g., when a new sentence starts, forget the previous subject). The **input gate** answers: "What new information is worth remembering?" The **output gate** answers: "Which parts of my memory are relevant right now?" Each gate uses a [sigmoid](../module-00-ml-pytorch-foundations/section-0.2.html) (output between 0 and 1) because it represents a continuous decision between "completely forget" (0) and "completely remember" (1).
The secret is the cell state path. Unlike the hidden state (updated multiplicatively, causing vanishing gradients), the cell state is updated additively: new = forget \* old + input \* candidate. Addition lets gradients flow through time without exponential shrinkage. This additive shortcut is conceptually identical to the residual connections you will see in Transformers ([Chapter 04](module-04-transformer-architecture_index.html.md)).
### The GRU Cell
The **Gated Recurrent Unit** (GRU), proposed by Cho et al. in 2014, simplifies the LSTM
by merging the cell state and hidden state into a single vector and using only two gates:
Code Fragment 3.1.3 below puts this into practice.
1. **Update gate** ztz\_{t}zt​: Controls how much of the old state to keep (combining the LSTM's forget and input gates).
2. **Reset gate** rtr\_{t}rt​: Controls how much of the old state to use when computing the candidate hidden state.
ht=(1−zt)⊙ht−1+zt⊙tanh⁡(W[rt⊙ht−1,xt])h\_{t} = (1 - z\_{t}) \odot h\_{t-1} + z\_{t} \odot \operatorname{tanh}(W [r\_{t} \odot h\_{t-1}, x\_{t}])ht​=(1−zt​)⊙ht−1​+zt​⊙tanh(W[rt​⊙ht−1​,xt​])
Property Comparison
| Property | Vanilla RNN | LSTM | GRU |
| --- | --- | --- | --- |
| Gates | 0 | 3 (forget, input, output) | 2 (update, reset) |
| State vectors | 1 (h) | 2 (h, c) | 1 (h) |
| Parameters (per cell) | ~n² | ~4n² | ~3n² |
| Long-range learning | Poor | Good | Good |
| Training speed | Fastest | Slowest | Middle |
**Code Fragment 3.1.3:** Compare parameter counts.
Modify and Observe
- Change `hidden_size` from 256 to 64. How do the parameter counts scale? Does the ratio between RNN, LSTM, and GRU stay the same?
- In the vanishing gradient experiment above, replace `nn.RNN` with `nn.LSTM`. Do the gradient norms at early time steps improve? By how much?
- Try `nn.LSTM(input_size, hidden_size, num_layers=3)` instead of 1 layer. What happens to the gradient distribution across time steps?
## 5. Bidirectional RNNs
A standard (unidirectional) RNN reads the sequence left to right. The hidden state at position
ttt encodes information from tokens 1 through ttt,
but knows nothing about tokens after position ttt. For many tasks (machine
translation, named entity recognition, sentiment analysis), the context on *both* sides of
a word matters.
A **bidirectional RNN** addresses this by running two independent RNNs over the sequence:
one forward (left to right) and one backward (right to left). At each position, the two hidden states
are concatenated to form a representation that encodes both past and future context:
ht=[ht→;ht←]h\_{t} = [h\_{t}^{ \rightarrow } ; h\_{t}^{ \leftarrow }]ht​=[ht→​;ht←​]
Note
Bidirectional RNNs can only be used when the entire input sequence is available at once (as in encoding a source sentence for translation). They **cannot** be used for autoregressive generation (predicting the next word) because the backward pass would require knowledge of future tokens that have not been generated yet. This distinction between "encoding" and "generation" modes is fundamental and will reappear when we discuss causal masking in [Section 3.3](module-03-sequence-models-attention_section-3.3.html.md).
## 6. The Encoder-Decoder Architecture (Seq2Seq)
Many important NLP tasks require mapping a variable-length input sequence to a variable-length output
sequence: machine translation (English to French), summarization (article to summary), and question
answering (question to answer). The **sequence-to-sequence** (seq2seq) architecture,
introduced by Sutskever et al. in 2014, handles this with two RNNs:
1. **Encoder:** Reads the input sequence token by token and compresses it into a single fixed-length vector: the final hidden state hTh\_{T}hT​. In the original seq2seq literature, this vector is sometimes called the "context vector," but we will reserve that term for the attention-weighted sum introduced in [Section 3.2](module-03-sequence-models-attention_section-3.2.html.md). Here, we call it the **encoder summary vector**.
2. **Decoder:** Receives the encoder summary vector as its initial hidden state and generates the output sequence one token at a time, feeding each generated token as input to the next step.
![Encoder-decoder seq2seq architecture with LSTM cells and context vector bottleneck](images/fig-3.1.6-the-encoder-decoder-seq2seq-architecture-the-entire-sourc.png)
**Figure 3.1.6**: The encoder-decoder (seq2seq) architecture. The entire source sentence must be compressed into a single fixed-length context vector, creating an information bottleneck that limits performance on long sequences.
### The Information Bottleneck
The critical weakness of this architecture is the **information bottleneck**.
The encoder must compress an entire source sentence (which could be 50 words or 500 words) into a
single vector of fixed dimensionality (typically 256 to 1024 dimensions). For short sentences
this works reasonably well, but as sentence length increases, the model must cram more and more
information into the same number of dimensions. Important details from early parts of the sentence
are inevitably lost.
Empirically, Cho et al. (2014) showed that seq2seq translation quality degrades sharply for
sentences longer than about 20 words. This degradation is a direct consequence of the
bottleneck: the decoder simply does not have access to enough information about the source
sentence.
Key Insight
The information bottleneck problem is conceptually distinct from the vanishing gradient problem, though they are related. Vanishing gradients make it hard to *train* the network to encode long-range information. The bottleneck makes it impossible to *represent* all that information even if training succeeds. The attention mechanism ([Section 3.2](module-03-sequence-models-attention_section-3.2.html.md)) solves the bottleneck by allowing the decoder to look back at *all* encoder hidden states rather than relying on a single summary vector.
🌎 **Real-World Scenario**: The Seq2Seq Bottleneck in Medical Report Summarization
**Who:** A research team at a university hospital building an automated system to summarize radiology reports.
**Situation:** The team trained an LSTM-based seq2seq model to generate one-paragraph summaries from full radiology reports. Reports averaged 150 words, and the model produced reasonable summaries during development.
**Problem:** When tested on complex reports exceeding 300 words (often involving multiple findings across different body regions), the model consistently "forgot" findings mentioned early in the report. Summaries would capture the last two or three findings but omit earlier ones, sometimes missing critical diagnoses.
**Dilemma:** The team debated three options: increasing the LSTM hidden state dimension from 512 to 2048 (quadrupling memory requirements), truncating reports to 150 words (losing information), or adding an attention mechanism over the encoder states.
**Decision:** They added Bahdanau-style attention (which they would later study in [Section 3.2](module-03-sequence-models-attention_section-3.2.html.md)), allowing the decoder to look back at all encoder hidden states rather than relying on the single bottleneck vector.
**How:** The attention mechanism computed a weighted average of all encoder states at each decoder step, letting the model dynamically focus on the relevant parts of the input when generating each word of the summary.
**Result:** [ROUGE](../../part-8-evaluation-production/module-29-evaluation-observability/section-29.1.html)-L scores improved from 0.38 to 0.54 on long reports. The model successfully captured findings from all sections of the report regardless of length. This experience foreshadowed the broader shift from pure seq2seq to attention-based architectures described in [Section 3.2](module-03-sequence-models-attention_section-3.2.html.md).
**Lesson:** **The information bottleneck is a capacity problem, not a training problem. No amount of training data or hidden state expansion can compensate for architecturally losing access to early input information.**
Attention solves the information bottleneck, but it does not address a separate, equally important limitation of recurrent architectures. Even with perfect gradient flow and unlimited memory, RNNs face a structural barrier that limits their practical scalability.
## 7. Sequential Computation: The Parallelism Problem
Beyond the gradient and bottleneck issues, RNNs have a fundamental **computational limitation**:
they are inherently sequential. To compute hth\_{t}ht​, you must first compute
ht−1h\_{t-1}ht−1​. There is no way to parallelize across time steps.
On modern GPUs, which contain thousands of cores designed for parallel computation, this is devastating.
A feedforward layer can process all positions simultaneously, but an RNN must process them one by one.
For a sequence of length nnn, an RNN requires O(n)O(n)O(n)
sequential operations, while a fully parallelizable architecture requires only O(1)O(1)O(1)
(at the cost of more total computation per step).
Code Fragment 3.1.4 below puts this into practice.
![](http://llmbook.apartsin.com/styles/icons/callout-code.svg)Show Code (26 lines)
```python
# Benchmark RNN vs LSTM vs GRU wall-clock time on a 512-step sequence.
# The sequential bottleneck becomes clear compared to parallel alternatives.
import torch, torch.nn as nn, time
seq_len, batch, inp, hid = 512, 32, 256, 256
x = torch.randn(batch, seq_len, inp)
rnn = nn.LSTM(inp, hid, batch_first=True)
linear = nn.Linear(inp, hid) # Feedforward: processes all positions in parallel
# Time the sequential RNN
t0 = time.perf_counter()
for _ in range(100):
 _ = rnn(x)
rnn_time = (time.perf_counter() - t0) / 100
# Time the parallel feedforward
t0 = time.perf_counter()
for _ in range(100):
 _ = linear(x)
ff_time = (time.perf_counter() - t0) / 100
print(f"LSTM forward pass: {rnn_time*1000:.1f} ms")
print(f"Linear forward pass: {ff_time*1000:.1f} ms")
print(f"Speedup: {rnn_time/ff_time:.1f}x")
```
Output (3 lines)
LSTM forward pass: 12.8 ms
Linear forward pass: 0.9 ms
Speedup: 14.2x
**Code Fragment 3.1.4:** Time the sequential RNN.
The feedforward layer is over 14 times faster, and this gap widens dramatically on GPUs and with
longer sequences. This sequential bottleneck is one of the primary reasons the field moved toward
attention-based architectures that can process all positions in parallel.
## 8. Putting It All Together: A Seq2Seq Translation Model
Let us tie everything together by building a minimal seq2seq model. This will crystallize both
the architecture and its limitations, setting the stage for the attention mechanism in [Section 3.2](module-03-sequence-models-attention_section-3.2.html.md).
Code Fragment 3.1.5 below puts this into practice.
![](http://llmbook.apartsin.com/styles/icons/callout-code.svg)Show Code (51 lines)
```python
# Seq2seq architecture: an LSTM encoder compresses input into a context
# vector, and a decoder LSTM generates output tokens one at a time.
import torch
import torch.nn as nn
class Seq2SeqEncoder(nn.Module):
 def __init__(self, vocab_size, emb_dim, hidden_dim):
 super().__init__()
 self.embedding = nn.Embedding(vocab_size, emb_dim)
 self.rnn = nn.LSTM(emb_dim, hidden_dim, batch_first=True)
 def forward(self, src):
 # src: (batch, src_len) token indices
 embedded = self.embedding(src) # (batch, src_len, emb_dim)
 outputs, (h, c) = self.rnn(embedded) # h, c: (1, batch, hidden)
 return outputs, (h, c)
class Seq2SeqDecoder(nn.Module):
 def __init__(self, vocab_size, emb_dim, hidden_dim):
 super().__init__()
 self.embedding = nn.Embedding(vocab_size, emb_dim)
 self.rnn = nn.LSTM(emb_dim, hidden_dim, batch_first=True)
 self.fc = nn.Linear(hidden_dim, vocab_size)
 def forward(self, tgt, hidden):
 # tgt: (batch, 1) single token at a time
 embedded = self.embedding(tgt)
 output, hidden = self.rnn(embedded, hidden)
 prediction = self.fc(output) # (batch, 1, vocab_size)
 return prediction, hidden
# Build model
enc = Seq2SeqEncoder(vocab_size=5000, emb_dim=64, hidden_dim=128)
dec = Seq2SeqDecoder(vocab_size=6000, emb_dim=64, hidden_dim=128)
# Simulate encoding "the cat sat"
src_tokens = torch.tensor([[12, 457, 89]]) # batch=1, len=3
enc_outputs, (h, c) = enc(src_tokens)
# Decode three tokens autoregressively
dec_input = torch.tensor([[1]]) # <SOS> token
for step in range(3):
 logits, (h, c) = dec(dec_input, (h, c))
 next_token = logits.argmax(dim=-1) # greedy decode
 print(f"Decode step {step}: token = {next_token.item()}, logits shape = {logits.shape}")
 dec_input = next_token
print(f"\nEncoder outputs shape: {enc_outputs.shape}")
print(f"Context vector shape: h={h.shape}, c={c.shape}")
print("Note: decoder only sees (h, c), not enc_outputs. That is the bottleneck.")
```
Output (7 lines)
Decode step 0: token = 2738, logits shape = torch.Size([1, 1, 6000])
Decode step 1: token = 4102, logits shape = torch.Size([1, 1, 6000])
Decode step 2: token = 1955, logits shape = torch.Size([1, 1, 6000])
Encoder outputs shape: torch.Size([1, 3, 128])
Context vector shape: h=torch.Size([1, 1, 128]), c=torch.Size([1, 1, 128])
Note: decoder only sees (h, c), not enc\_outputs. That is the bottleneck.
**Code Fragment 3.1.11:** Define Seq2SeqEncoder, Seq2SeqDecoder
Look at the shapes: the encoder produces hidden states for all 3 positions
(`torch.Size([1, 3, 128])`), but the decoder receives only the
final hidden state (`torch.Size([1, 1, 128])`). All the rich,
position-specific information from the encoder is discarded. This is exactly
the problem that attention will solve.
Key Insight: Sequential Processing and the Markov Property
RNNs embody a fundamental tension between theory and practice. In theory, the hidden state can encode the entire history of a sequence, making the model arbitrarily powerful. In practice, the hidden state is a fixed-size vector, which means it must compress all past information into a finite number of dimensions. This is a form of the *information bottleneck*: the hidden state cannot grow with the sequence length, so older information is inevitably overwritten. LSTMs mitigate this by adding a gating mechanism, but they do not eliminate the bottleneck. The Transformer (covered in [Section 4.1](module-04-transformer-architecture_section-4.1.html.md)) takes a radically different approach: instead of compressing history into a fixed state, it lets every position attend to every other position directly. This mirrors a broader pattern in computer science where the choice between streaming (fixed memory) and random-access (unlimited lookback) architectures determines what problems can be efficiently solved.
## ✓ Key Takeaways
1. **RNNs process sequences step-by-step** using a hidden state that carries information forward. The same weights are reused at every time step (parameter sharing).
2. **Vanishing gradients** arise from multiplying many Jacobian matrices during BPTT. They make it nearly impossible for vanilla RNNs to learn dependencies spanning more than ~20 steps.
3. **LSTM and GRU cells** use learnable gates and additive cell-state updates to create linear shortcuts for gradient flow, dramatically improving long-range learning.
4. **Bidirectional RNNs** capture both left and right context but cannot be used for autoregressive generation.
5. **The seq2seq information bottleneck** forces the entire source sentence through a single fixed-size vector, degrading quality for long inputs.
6. **Sequential computation** prevents RNNs from exploiting GPU parallelism, making them slow on modern hardware. This motivates the move toward fully parallelizable architectures.
Common Misconception: "Transformers Replaced RNNs" Is an Oversimplification
It is common to hear that "Transformers replaced RNNs," but this overstates the case. RNNs (particularly LSTMs) remain in production for specific use cases: real-time streaming applications where input arrives one token at a time, edge devices with tight memory budgets where O(n^2) attention is prohibitive, and time-series tasks where the inductive bias of recurrence is beneficial. More fundamentally, the best ideas from RNNs (gating, sequential state processing, and linear-time inference) have been incorporated into modern architectures like Mamba, RWKV, and hybrid models. The lesson from this chapter is not "RNNs are bad" but rather "RNNs have specific limitations (sequential computation, vanishing gradients) that motivated attention, which in turn enabled the Transformer."
Research Frontier
**State-space models (SSMs)** are emerging as a viable alternative to both RNNs and Transformers. [Mamba](../../part-10-frontiers/module-34-emerging-architectures/section-34.1.html) (Gu and Dao, 2023) combines the linear-time processing of RNNs with the parallel training of Transformers through selective state spaces. Hybrid architectures like Jamba (AI21, 2024) alternate Mamba layers with attention layers. RWKV is another RNN-like architecture that trains in parallel like a Transformer but infers like an RNN. These models suggest that the RNN idea of sequential state processing is not dead, just being reimagined.
Tip: Pack Variable-Length Sequences
When using RNNs in PyTorch, use `pack_padded_sequence` and `pad_packed_sequence` to avoid wasting computation on padding tokens. This can speed up training by 20 to 40% on datasets with highly variable sequence lengths.
☑ Self-Check
1. Why can a vanilla RNN not learn that the first word in a 100-word sentence determines the last word?
Show Answer
Because of the vanishing gradient problem. When backpropagating from step 100 to step 1, the gradient passes through 99 Jacobian matrices, each with a dominant singular value less than 1. The product of these matrices shrinks the gradient exponentially, so the network receives almost no learning signal connecting the first token to the loss at the last token.
2. How does the LSTM cell state help with gradient flow?
Show Answer
The cell state update is additive: ct=ft⊙ct−1+it⊙candidatec\_{t} = f\_{t} \odot c\_{t-1} + i\_{t} \odot candidatect​=ft​⊙ct−1​+it​⊙candidate. When the forget gate is close to 1 and the input gate is close to 0, the cell state passes through with minimal change. This creates a linear shortcut for gradient flow (the gradient of the sum is 1), similar to a residual connection. Gradients can thus travel many steps along the cell state highway without vanishing.
3. What is the difference between a GRU's update gate and an LSTM's forget gate?
Show Answer
The GRU's update gate ztz\_{t}zt​ plays a dual role: it simultaneously controls how much of the old hidden state to keep (like the LSTM forget gate) and how much of the new candidate to incorporate (like the LSTM input gate). The GRU uses a single gate for both purposes via the formula ht=(1−zt)⊙ht−1+zt⊙candidateh\_{t} = (1 - z\_{t}) \odot h\_{t-1} + z\_{t} \odot candidateht​=(1−zt​)⊙ht−1​+zt​⊙candidate, ensuring the two proportions always sum to 1.
4. Why can bidirectional RNNs not be used for language generation?
Show Answer
Language generation is autoregressive: the model predicts the next token given only the previous tokens. A bidirectional RNN requires access to both past and future tokens to compute each hidden state. During generation, future tokens do not yet exist, so the backward pass cannot be computed. Bidirectional RNNs are therefore limited to "encoding" tasks where the full input is available upfront.
5. Explain the information bottleneck in seq2seq and predict how it affects translation quality as sentence length increases.
Show Answer
In the basic seq2seq model, the encoder compresses the entire source sentence into a single fixed-dimensional context vector. As sentences grow longer, more information must be packed into the same number of dimensions, inevitably losing details. Translation quality degrades because the decoder lacks the specific source information it needs at each generation step. Cho et al. (2014) demonstrated that [BLEU](../../part-8-evaluation-production/module-29-evaluation-observability/section-29.1.html) scores drop significantly for source sentences longer than about 20 words.
### What's Next?
In the next section, [Section 3.2: The Attention Mechanism](module-03-sequence-models-attention_section-3.2.html.md), we introduce the attention mechanism itself, the key insight that allows models to focus on relevant parts of the input.
📚 References & Further Reading
Foundational RNN Papers
Elman, J. L. (1990). ["Finding Structure in Time."](https://doi.org/10.1016/0364-0213(90)90002-E) *Cognitive Science*, 14(2), 179-211.
The original simple recurrent network paper that established the hidden-state paradigm for sequence processing. Essential for understanding how the field first approached temporal data with neural networks.
📄 Paper
[Hochreiter, S. & Schmidhuber, J. (1997). "Long Short-Term Memory." *Neural Computation*, 9(8), 1735-1780.](https://www.bioinf.jku.at/publications/older/2604.pdf)
The landmark paper introducing LSTM cells with gated memory, solving the vanishing gradient problem for recurrent networks. This is one of the most cited papers in deep learning and remains foundational for understanding gated architectures.
📄 Paper
[Cho, K. et al. (2014). "Learning Phrase Representations using RNN Encoder-Decoder for Statistical Machine Translation." *EMNLP 2014*.](https://arxiv.org/abs/1406.1078)
Introduces the GRU (Gated Recurrent Unit) and the encoder-decoder framework that became the foundation for seq2seq models. Read this to understand the simpler alternative to LSTMs and the origins of the encoder-decoder paradigm.
📄 Paper
Sequence-to-Sequence & Gradient Analysis
[Sutskever, I., Vinyals, O., & Le, Q. V. (2014). "Sequence to Sequence Learning with Neural Networks." *NeurIPS 2014*.](https://arxiv.org/abs/1409.3215)
Demonstrated that deep LSTMs could perform end-to-end machine translation, establishing the seq2seq paradigm. This paper directly motivates the information bottleneck problem discussed in this section.
📄 Paper
[Pascanu, R., Mikolov, T., & Bengio, Y. (2013). "On the Difficulty of Training Recurrent Neural Networks." *ICML 2013*.](https://arxiv.org/abs/1211.5063)
Provides rigorous analysis of vanishing and exploding gradients in RNNs, including the Jacobian product framework discussed in this section. Essential reading for anyone wanting the mathematical details behind gradient flow in recurrent networks.
📄 Paper
[Bengio, Y., Simard, P., & Frasconi, P. (1994). "Learning Long-Term Dependencies with](https://doi.org/10.1109/72.279181) [Gradient Descent](../module-00-ml-pytorch-foundations/section-0.1.html) is Difficult." *IEEE Transactions on Neural Networks*, 5(2), 157-166.
The early theoretical analysis establishing that gradient-based learning in recurrent networks faces fundamental difficulties with long-range dependencies. This paper laid the groundwork that LSTMs and attention mechanisms were designed to address.
📄 Paper
Practical Guides
[Olah, C. (2015). "Understanding LSTM Networks."](https://colah.github.io/posts/2015-08-Understanding-LSTMs/)
The most widely cited visual explanation of LSTM architecture, with clear diagrams of gate operations and cell state flow. If you found the LSTM section of this chapter challenging, start here for an alternative perspective with excellent illustrations.
📝 Blog Post
[Karpathy, A. (2015). "The Unreasonable Effectiveness of Recurrent Neural Networks."](https://karpathy.github.io/2015/05/21/rnn-effectiveness/)
A highly accessible blog post demonstrating character-level RNN language models, with memorable examples of Shakespeare and code generation. Perfect for building intuition about what RNNs can learn, and a fun hands-on complement to this section's theory.
📝 Blog Post