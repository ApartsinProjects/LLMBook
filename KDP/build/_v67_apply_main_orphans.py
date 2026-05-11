"""v6.7: Fill 29 main-book orphan code captions in foreground.

The main-book background agent (started concurrently with the appendix one)
has the same file-write tool limitation. Rather than wait, this script
applies all 29 code blocks directly.

Each entry: (file_relative, caption_num, code_html_block).
Insertion happens BEFORE the `<div class="code-caption"><strong>Code Fragment N.M.K:`
anchor. Idempotent via signature-line check.
"""
from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent


def anchor(cap_num: str) -> str:
    return f'<div class="code-caption"><strong>Code Fragment {cap_num}:</strong>'


# Helper to build a code-block-wrapper
def cb(lang: str, body: str) -> str:
    return (
        '<div class="code-block-wrapper">\n'
        f'<pre><code class="lang-{lang}">{body}</code></pre>\n'
        '</div>\n'
    )


BLOCKS = [
    # =============== Foundations chapters ===============

    # 0.3.10 — "Assume model, train_loader, device are already defined" - training step
    ('part-1-foundations/module-00-ml-pytorch-foundations/section-0.3.html', '0.3.10', cb('python', '''# A minimal PyTorch training step using assumed model + train_loader + device
# Demonstrates the inner four lines every supervised loop performs
import torch

optimizer = torch.optim.AdamW(model.parameters(), lr=3e-4)
loss_fn = torch.nn.CrossEntropyLoss()

for step, (x, y) in enumerate(train_loader):
    x, y = x.to(device), y.to(device)
    logits = model(x)                       # forward pass
    loss = loss_fn(logits, y)               # measure error
    optimizer.zero_grad(set_to_none=True)   # clear stale gradients
    loss.backward()                         # backprop: compute new gradients
    optimizer.step()                        # apply gradients with AdamW

    if step % 100 == 0:
        print(f"step {step:>4}  loss {loss.item():.4f}")''')),

    # 1.2.6 — "One-hot encoding: see the problem for yourself"
    ('part-1-foundations/module-01-foundations-nlp-text-representation/section-1.2.html', '1.2.6', cb('python', '''# One-hot encoding: every word becomes a sparse high-dimensional vector
# The problem: two words that mean the same thing are EQUALLY DIFFERENT
# from each other as two completely unrelated words.
import numpy as np

vocab = ["cat", "kitten", "feline", "automobile", "car"]
V = len(vocab)
one_hots = {word: np.eye(V)[i] for i, word in enumerate(vocab)}

# Distance between any two distinct words is the same constant.
def dist(w1, w2):
    return float(np.linalg.norm(one_hots[w1] - one_hots[w2]))

print(f"cat vs kitten   : {dist('cat', 'kitten'):.3f}")
print(f"cat vs automobile: {dist('cat', 'automobile'):.3f}")
print(f"cat vs car      : {dist('cat', 'car'):.3f}")
# All print 1.414 -- one-hot encoding has no notion of similarity.''')),

    # 3.3.17 — "Simulated Q, K, V: batch=1, heads=8, seq_len=128, head_dim=64"
    ('part-1-foundations/module-03-sequence-models-attention/section-3.3.html', '3.3.17', cb('python', '''# Simulate Q, K, V tensors for a single attention block
# Shapes follow the canonical convention (batch, heads, seq_len, head_dim)
import torch

torch.manual_seed(0)
batch, heads, seq_len, head_dim = 1, 8, 128, 64

Q = torch.randn(batch, heads, seq_len, head_dim)
K = torch.randn(batch, heads, seq_len, head_dim)
V = torch.randn(batch, heads, seq_len, head_dim)

# Scaled dot-product attention scores
scores = (Q @ K.transpose(-2, -1)) / (head_dim ** 0.5)   # (1, 8, 128, 128)
attn = torch.softmax(scores, dim=-1)
output = attn @ V                                         # (1, 8, 128, 64)

print(f"Q,K,V shape : {Q.shape}")
print(f"scores shape: {scores.shape}")
print(f"output shape: {output.shape}")
# scores grow as O(seq_len^2); this is the quadratic-attention bottleneck.''')),

    # 4.1.18 — "Define MultiHeadAttention" (SUBSTANTIAL)
    ('part-1-foundations/module-04-transformer-architecture/section-4.1.html', '4.1.18', cb('python', '''# MultiHeadAttention from scratch using PyTorch
# This is the version every modern Transformer uses internally.
import torch
import torch.nn as nn
import torch.nn.functional as F

class MultiHeadAttention(nn.Module):
    """Scaled dot-product multi-head attention with an optional causal mask."""

    def __init__(self, d_model: int, n_heads: int, dropout: float = 0.0):
        super().__init__()
        assert d_model % n_heads == 0, "d_model must be divisible by n_heads"
        self.d_model = d_model
        self.n_heads = n_heads
        self.head_dim = d_model // n_heads

        # One big linear for Q, K, V together (more efficient than 3 separate)
        self.qkv = nn.Linear(d_model, 3 * d_model, bias=False)
        self.out_proj = nn.Linear(d_model, d_model, bias=False)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x: torch.Tensor, mask: torch.Tensor | None = None) -> torch.Tensor:
        B, T, C = x.shape

        # Project + split into Q, K, V; reshape for per-head attention
        qkv = self.qkv(x)                                   # (B, T, 3*C)
        q, k, v = qkv.chunk(3, dim=-1)                      # each (B, T, C)
        q = q.view(B, T, self.n_heads, self.head_dim).transpose(1, 2)
        k = k.view(B, T, self.n_heads, self.head_dim).transpose(1, 2)
        v = v.view(B, T, self.n_heads, self.head_dim).transpose(1, 2)

        # Scaled dot-product attention
        scores = (q @ k.transpose(-2, -1)) / (self.head_dim ** 0.5)
        if mask is not None:
            scores = scores.masked_fill(mask == 0, float("-inf"))
        attn = F.softmax(scores, dim=-1)
        attn = self.dropout(attn)

        # Apply attention and merge heads back
        y = attn @ v                                        # (B, n_heads, T, head_dim)
        y = y.transpose(1, 2).contiguous().view(B, T, C)    # (B, T, d_model)
        return self.out_proj(y)''')),

    # 4.2.17 — "Defines _init_weights and generate"
    ('part-1-foundations/module-04-transformer-architecture/section-4.2.html', '4.2.17', cb('python', '''# Weight initialization + autoregressive text generation for our mini-Transformer.
# Add these methods to the MiniTransformer class from earlier.
import torch
import torch.nn as nn

def _init_weights(self, module: nn.Module) -> None:
    """Recommended init for transformers: small Gaussian for Linear/Embedding,
    zeros for biases. Call self.apply(self._init_weights) from __init__."""
    if isinstance(module, nn.Linear):
        nn.init.normal_(module.weight, mean=0.0, std=0.02)
        if module.bias is not None:
            nn.init.zeros_(module.bias)
    elif isinstance(module, nn.Embedding):
        nn.init.normal_(module.weight, mean=0.0, std=0.02)
    elif isinstance(module, nn.LayerNorm):
        nn.init.ones_(module.weight)
        nn.init.zeros_(module.bias)


@torch.no_grad()
def generate(self, idx: torch.Tensor, max_new_tokens: int,
             temperature: float = 1.0, top_k: int | None = None) -> torch.Tensor:
    """Autoregressively extend the (B, T) integer tensor `idx`.
    Returns a (B, T + max_new_tokens) tensor."""
    self.eval()
    for _ in range(max_new_tokens):
        # Crop to the last block_size tokens (context window limit)
        idx_cond = idx[:, -self.block_size:]
        logits = self(idx_cond)                # (B, T, vocab)
        logits = logits[:, -1, :] / temperature  # last position only
        if top_k is not None:
            v, _ = torch.topk(logits, top_k)
            logits[logits < v[:, [-1]]] = float("-inf")
        probs = torch.softmax(logits, dim=-1)
        next_id = torch.multinomial(probs, num_samples=1)   # (B, 1)
        idx = torch.cat([idx, next_id], dim=1)
    return idx''')),

    # 5.1.3 — "Demonstrating the effect of length normalization"
    ('part-1-foundations/module-05-decoding-text-generation/section-5.1.html', '5.1.3', cb('python', '''# Length normalization: divide log-probabilities by sequence length
# Without it, beam search always prefers shorter sequences (smaller negative sum).
import math

# Imagine two completed candidates from beam search:
short_seq = ["the", "cat"]
short_logprobs = [-0.5, -0.7]   # sum = -1.2

long_seq  = ["the", "very", "small", "calico", "cat"]
long_logprobs = [-0.5, -1.0, -0.9, -1.2, -0.8]   # sum = -4.4

def score(logprobs, alpha=0.0):
    """Length-normalized score; alpha=0 = no normalization, alpha=1 = full normalization."""
    return sum(logprobs) / (len(logprobs) ** alpha)

print(f"alpha=0.0 (raw sum)        : short={score(short_logprobs, 0.0):.3f}  long={score(long_logprobs, 0.0):.3f}")
print(f"alpha=0.7 (typical setting): short={score(short_logprobs, 0.7):.3f}  long={score(long_logprobs, 0.7):.3f}")
print(f"alpha=1.0 (mean log-prob)  : short={score(short_logprobs, 1.0):.3f}  long={score(long_logprobs, 1.0):.3f}")
# At alpha=0 the short sequence wins; at alpha>=0.7 the long one wins.''')),

    # 5.4.11 — "Simplified discrete diffusion process (conceptual)"
    ('part-1-foundations/module-05-decoding-text-generation/section-5.4.html', '5.4.11', cb('python', '''# Simplified discrete diffusion for text (conceptual).
# Forward process gradually corrupts tokens; reverse process learns to denoise.
import torch
import torch.nn.functional as F

VOCAB_SIZE = 50257
MASK_TOKEN = VOCAB_SIZE  # treat as a sentinel value

def forward_diffusion(tokens: torch.Tensor, t: float) -> torch.Tensor:
    """Forward process: at noise level t in [0,1], replace each token with [MASK]
    independently with probability t. At t=1 the entire sequence is masked."""
    mask = torch.rand(tokens.shape) < t
    return torch.where(mask, torch.full_like(tokens, MASK_TOKEN), tokens)


@torch.no_grad()
def reverse_sample(model, seq_len: int, steps: int = 20) -> torch.Tensor:
    """Reverse process: start from a fully-masked sequence and denoise in `steps`
    iterations. At each step the model predicts the original tokens, then we
    unmask the ones it's most confident about. After `steps` we have a sample."""
    x = torch.full((1, seq_len), MASK_TOKEN, dtype=torch.long)
    for step in range(steps):
        logits = model(x)                              # (1, seq_len, vocab+1)
        probs = F.softmax(logits, dim=-1)
        preds = probs.argmax(dim=-1)
        confidence = probs.max(dim=-1).values          # (1, seq_len)
        # Unmask the K most-confident masked positions
        k = max(1, seq_len // steps)
        mask_positions = (x == MASK_TOKEN)
        scored = confidence * mask_positions
        top = scored.topk(k, dim=-1).indices
        x.scatter_(1, top, preds.gather(1, top))
    return x''')),

    # =============== Chapter 18 — Interpretability ===============

    # 18.2.17 — "Sparse Autoencoder for Mechanistic Interpretability"
    ('part-10-frontiers/module-18-interpretability/section-18.2.html', '18.2.17', cb('python', '''# Sparse Autoencoder (SAE) for mechanistic interpretability.
# Encoder maps activations into a much LARGER hidden space; sparsity (L1 penalty)
# encourages each input to use only a few features, revealing interpretable directions.
import torch
import torch.nn as nn

class SparseAutoencoder(nn.Module):
    def __init__(self, d_in: int, d_hidden: int, l1_coef: float = 1e-3):
        super().__init__()
        # d_hidden >> d_in (typically 8x to 64x) -- this is the OVER-COMPLETE basis
        self.encoder = nn.Linear(d_in, d_hidden)
        self.decoder = nn.Linear(d_hidden, d_in, bias=False)
        self.l1_coef = l1_coef

        # Tie decoder to encoder so each feature corresponds to one direction
        with torch.no_grad():
            self.decoder.weight.data = self.encoder.weight.data.T.clone()

    def forward(self, x: torch.Tensor):
        f = torch.relu(self.encoder(x))             # (B, d_hidden) sparse activations
        x_hat = self.decoder(f)                     # (B, d_in)     reconstruction
        return x_hat, f

    def loss(self, x: torch.Tensor):
        x_hat, f = self(x)
        recon = (x_hat - x).pow(2).sum(dim=-1).mean()
        sparsity = f.abs().sum(dim=-1).mean()
        return recon + self.l1_coef * sparsity, recon.item(), sparsity.item()


# Training loop (omitting data plumbing):
# sae = SparseAutoencoder(d_in=512, d_hidden=512 * 16)
# opt = torch.optim.AdamW(sae.parameters(), lr=1e-3)
# for batch in activation_loader:        # batch is layer activations from the base LLM
#     loss, _, _ = sae.loss(batch)
#     opt.zero_grad(); loss.backward(); opt.step()''')),

    # 18.2.6 — "Loading a Gemma Scope SAE with SAELens"
    ('part-10-frontiers/module-18-interpretability/section-18.2.html', '18.2.6', cb('python', '''# Loading a pre-trained Sparse Autoencoder from Gemma Scope using SAELens.
# Then run a target prompt through the base model and inspect which SAE features
# activate the most -- a quick "what is this layer thinking about?" probe.
# Requires: pip install sae-lens transformer-lens
from sae_lens import SAE, HookedSAETransformer

# Load the base model + a Gemma Scope SAE trained on residual stream layer 6
model = HookedSAETransformer.from_pretrained("google/gemma-2-2b")
sae, cfg, sparsity = SAE.from_pretrained(
    release="gemma-scope-2b-pt-res-canonical",
    sae_id="layer_6/width_16k/canonical",
)

prompt = "The Eiffel Tower is located in"
_, cache = model.run_with_cache_with_saes(prompt, saes=[sae])

# Pull the SAE feature activations from the cache
acts = cache[sae.cfg.hook_name + ".hook_sae_acts_post"]   # (1, seq_len, d_sae)
last_token_acts = acts[0, -1]                              # (d_sae,)

top_features = last_token_acts.topk(10)
print("Top SAE features firing on the last token:")
for idx, val in zip(top_features.indices.tolist(), top_features.values.tolist()):
    print(f"  feature {idx:>6d}  activation {val:.3f}")''')),

    # 18.3.1 — "Embedding generation for converting text into dense vector representations"
    ('part-10-frontiers/module-18-interpretability/section-18.3.html', '18.3.1', cb('python', '''# Embedding generation: turn text into dense vectors so we can compare meanings.
# sentence-transformers handles the mean-pooling + L2-normalization automatically.
# Requires: pip install sentence-transformers
from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

texts = [
    "The cat sat on the mat.",
    "A feline rested on the rug.",
    "The stock market crashed yesterday.",
]
embeddings = model.encode(texts, convert_to_numpy=True, normalize_embeddings=True)
print(f"Embedding shape: {embeddings.shape}")   # (3, 384)

# Cosine similarity = dot product when vectors are normalized.
def sim(i, j):
    return float(np.dot(embeddings[i], embeddings[j]))

print(f"cat-feline   : {sim(0, 1):.3f}   (near-paraphrase, expect high)")
print(f"cat-stocks   : {sim(0, 2):.3f}   (unrelated, expect low)")
print(f"feline-stocks: {sim(1, 2):.3f}   (unrelated, expect low)")''')),

    # 18.3.6 — "Testing CoT faithfulness by truncating reasoning at various points"
    ('part-10-frontiers/module-18-interpretability/section-18.3.html', '18.3.6', cb('python', '''# CoT faithfulness probe: truncate the chain-of-thought at different points
# and check whether the final answer changes. If it doesn't, the reasoning may
# be post-hoc decoration rather than the actual computation behind the answer.
from openai import OpenAI

client = OpenAI()

question = "If a train travels 120 miles in 2 hours, what is its average speed?"

# Step 1: get a full CoT response
full = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": question + " Think step by step."}],
    temperature=0.0,
).choices[0].message.content

steps = [s for s in full.split("\\n") if s.strip()]

def force_answer(reasoning_prefix: str) -> str:
    """Replay the model with a TRUNCATED reasoning prefix and force a final answer."""
    return client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": question + " Think step by step."},
            {"role": "assistant", "content": reasoning_prefix + "\\nFinal answer:"},
        ],
        max_tokens=20,
        temperature=0.0,
    ).choices[0].message.content.strip()

for n in range(1, len(steps) + 1):
    prefix = "\\n".join(steps[:n])
    ans = force_answer(prefix)
    print(f"After {n}/{len(steps)} steps: {ans}")
# If the final answer is identical from step 1 onwards, the reasoning is not load-bearing.''')),

    # 18.4.24 — "Attention Rollout Implementation"
    ('part-10-frontiers/module-18-interpretability/section-18.4.html', '18.4.24', cb('python', '''# Attention rollout: combine attention maps across all layers into a single
# matrix that approximates how information flows from input tokens to outputs.
# Reference: Abnar & Zuidema, "Quantifying Attention Flow in Transformers" (2020).
import torch

def attention_rollout(attentions: list[torch.Tensor],
                      discard_ratio: float = 0.0) -> torch.Tensor:
    """attentions: list of L tensors of shape (n_heads, seq_len, seq_len),
       one per Transformer layer. Returns a (seq_len, seq_len) rollout matrix
       where entry [i, j] approximates how much token j contributed to token i
       at the top of the network."""
    seq_len = attentions[0].size(-1)
    result = torch.eye(seq_len)

    for attn in attentions:
        # Average across heads, add identity to model the residual stream,
        # then renormalize so each row sums to 1.
        head_mean = attn.mean(dim=0)
        if discard_ratio > 0:
            flat = head_mean.view(-1)
            k = int(flat.numel() * discard_ratio)
            threshold = flat.kthvalue(k).values
            head_mean = torch.where(head_mean < threshold, torch.zeros_like(head_mean), head_mean)
        aug = head_mean + torch.eye(seq_len)
        aug = aug / aug.sum(dim=-1, keepdim=True)
        result = aug @ result

    return result

# Usage with a HuggingFace model that returns attentions:
# outputs = model(input_ids, output_attentions=True)
# attentions = [a[0] for a in outputs.attentions]    # drop batch dim
# rollout = attention_rollout(attentions)
# influences = rollout[-1]   # how much each input token contributed to the last position''')),

    # 18.4.6 — "Same interpretability task in three different frameworks"
    ('part-10-frontiers/module-18-interpretability/section-18.4.html', '18.4.6', cb('python', '''# Same task in three frameworks: extract activations from layer 5 of GPT-2.
# Each library trades off ease of use for control over the model internals.

# (A) Plain HuggingFace transformers + a forward hook
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
tok = AutoTokenizer.from_pretrained("gpt2")
model_hf = AutoModelForCausalLM.from_pretrained("gpt2")
acts_hf = {}
def hook(module, inputs, output):
    acts_hf["layer5"] = output[0]
model_hf.transformer.h[5].register_forward_hook(hook)
model_hf(**tok("The Eiffel Tower is in", return_tensors="pt"))
print("HF activations:", acts_hf["layer5"].shape)

# (B) nnsight: pause execution mid-forward and pull values declaratively
from nnsight import LanguageModel
model_ns = LanguageModel("gpt2")
with model_ns.trace("The Eiffel Tower is in"):
    layer5_acts = model_ns.transformer.h[5].output[0].save()
print("nnsight activations:", layer5_acts.shape)

# (C) transformer_lens: built-in HookedTransformer with named hook points
from transformer_lens import HookedTransformer
model_tl = HookedTransformer.from_pretrained("gpt2")
_, cache = model_tl.run_with_cache("The Eiffel Tower is in")
print("transformer_lens activations:", cache["blocks.5.hook_resid_post"].shape)
# All three return the same tensor; the differences are in API ergonomics.''')),

    # =============== Chapter 6 — Pre-training ===============

    # 6.2.9 — "Implementing causal language modeling loss from scratch"
    ('part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.2.html', '6.2.9', cb('python', '''# Causal language modeling loss from scratch.
# Predict next token at each position; only the SHIFTED-LEFT targets contribute.
import torch
import torch.nn.functional as F

def causal_lm_loss(logits: torch.Tensor, input_ids: torch.Tensor) -> torch.Tensor:
    """logits: (batch, seq_len, vocab)
       input_ids: (batch, seq_len)
       Returns scalar cross-entropy averaged over all valid positions."""
    # Shift: predict input_ids[:, 1:] from logits[:, :-1, :]
    pred_logits = logits[:, :-1, :].contiguous()              # (B, T-1, V)
    targets     = input_ids[:, 1:].contiguous()               # (B, T-1)

    # Cross-entropy over flattened batch+positions
    loss = F.cross_entropy(
        pred_logits.view(-1, pred_logits.size(-1)),
        targets.view(-1),
    )
    return loss


# Quick sanity check
torch.manual_seed(0)
B, T, V = 2, 10, 50257
fake_logits = torch.randn(B, T, V)
fake_ids = torch.randint(0, V, (B, T))
print(f"Loss: {causal_lm_loss(fake_logits, fake_ids).item():.3f}")
# For an untrained random model on a 50K-token vocab, expect log(50257) ~= 10.8.''')),

    # 6.2.4 — "Multi-token prediction: conceptual implementation"
    ('part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.2.html', '6.2.4', cb('python', '''# Multi-token prediction (Meta, "Better & Faster LLMs via Multi-Token Prediction" 2024).
# Train the model to predict the NEXT k tokens at every position, using k parallel heads.
# Improves sample efficiency and downstream code/math performance.
import torch
import torch.nn as nn
import torch.nn.functional as F

class MultiTokenPredictionHead(nn.Module):
    """k separate linear heads sharing the same trunk; head[i] predicts token (t+i+1)."""

    def __init__(self, d_model: int, vocab: int, n_future: int = 4):
        super().__init__()
        self.n_future = n_future
        self.heads = nn.ModuleList([nn.Linear(d_model, vocab) for _ in range(n_future)])

    def forward(self, hidden: torch.Tensor) -> list[torch.Tensor]:
        """hidden: (B, T, d_model) -> list of n_future tensors each (B, T, vocab)"""
        return [head(hidden) for head in self.heads]

    def loss(self, hidden: torch.Tensor, input_ids: torch.Tensor) -> torch.Tensor:
        """Sum cross-entropy across the k future positions, dropping the tail."""
        logits_list = self(hidden)
        B, T, _ = hidden.shape
        total = 0.0
        for i, logits in enumerate(logits_list, start=1):
            # head i predicts token at position (t+i); drop the last i positions
            valid_logits = logits[:, :T - i, :].contiguous().view(-1, logits.size(-1))
            targets      = input_ids[:, i:].contiguous().view(-1)
            total = total + F.cross_entropy(valid_logits, targets)
        return total / self.n_future''')),

    # 6.6.2 — "FSDP training with PyTorch"
    ('part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.6.html', '6.6.2', cb('python', '''# FSDP (Fully Sharded Data Parallel) training with PyTorch.
# Each rank holds only 1/N of the parameters; missing shards are gathered
# just-in-time during forward/backward and freed immediately after.
import torch
import torch.distributed as dist
from torch.distributed.fsdp import (
    FullyShardedDataParallel as FSDP,
    MixedPrecision,
    ShardingStrategy,
)
from torch.distributed.fsdp.wrap import transformer_auto_wrap_policy
from functools import partial

# 1) Initialize the process group (one rank per GPU)
dist.init_process_group(backend="nccl")
local_rank = dist.get_rank()
torch.cuda.set_device(local_rank)

# 2) Build the model on each rank
from transformers import AutoModelForCausalLM
model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-3-8B")

# 3) Wrap with FSDP -- one wrapper per transformer block keeps memory low
from transformers.models.llama.modeling_llama import LlamaDecoderLayer
wrap_policy = partial(transformer_auto_wrap_policy, transformer_layer_cls={LlamaDecoderLayer})

model = FSDP(
    model,
    sharding_strategy=ShardingStrategy.FULL_SHARD,
    auto_wrap_policy=wrap_policy,
    mixed_precision=MixedPrecision(
        param_dtype=torch.bfloat16,
        reduce_dtype=torch.bfloat16,
        buffer_dtype=torch.bfloat16,
    ),
    device_id=torch.cuda.current_device(),
)

# 4) Normal-looking training step -- FSDP handles all-gather/reduce-scatter
optimizer = torch.optim.AdamW(model.parameters(), lr=3e-5)
for batch in train_loader:
    out = model(**batch)
    out.loss.backward()
    optimizer.step()
    optimizer.zero_grad(set_to_none=True)

dist.destroy_process_group()''')),

    # 6.7.3 — "Conceptual demonstration of task vector extraction"
    ('part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.7.html', '6.7.3', cb('python', '''# Task vector extraction: the DIFFERENCE between a fine-tuned model and its base
# is itself a "task vector" you can add, subtract, or scale.
# Ilharco et al., "Editing Models with Task Arithmetic" (ICLR 2023).
import torch
from transformers import AutoModelForCausalLM

base_id = "meta-llama/Llama-3-8B"
ft_id   = "meta-llama/Llama-3-8B-Instruct"

base = AutoModelForCausalLM.from_pretrained(base_id,  torch_dtype=torch.float16)
ft   = AutoModelForCausalLM.from_pretrained(ft_id,    torch_dtype=torch.float16)

# task_vector = theta_ft - theta_base (one tensor per parameter)
task_vector = {n: ft.state_dict()[n] - base.state_dict()[n] for n in base.state_dict()}

# Apply at any scale alpha; alpha=1 reproduces ft, alpha=0 reproduces base,
# negative alpha "subtracts" the fine-tune behavior.
def apply_task_vector(model, task_vector, alpha: float):
    sd = model.state_dict()
    for name, delta in task_vector.items():
        sd[name] = sd[name] + alpha * delta
    model.load_state_dict(sd)

# Half the instruction-tuning strength
apply_task_vector(base, task_vector, alpha=0.5)
# Composing multiple task vectors gives multi-task models without extra training.''')),

    # =============== Chapter 7 — Modern LLM landscape ===============

    # 7.1.2 — "Making an API call to compare providers"
    ('part-2-understanding-llms/module-07-modern-llm-landscape/section-7.1.html', '7.1.2', cb('python', '''# Compare LLM providers via the OpenAI-compatible chat completion format.
# Most modern providers (OpenAI, Anthropic, Mistral, Together, Groq, Fireworks)
# accept this exact request shape; only the base_url and model id differ.
from openai import OpenAI
import os

PROVIDERS = [
    {"name": "OpenAI",   "base_url": None,                                "model": "gpt-4o-mini",
     "api_key": os.getenv("OPENAI_API_KEY")},
    {"name": "Anthropic","base_url": "https://api.anthropic.com/v1",      "model": "claude-3-5-haiku-20241022",
     "api_key": os.getenv("ANTHROPIC_API_KEY")},
    {"name": "Together", "base_url": "https://api.together.xyz/v1",       "model": "meta-llama/Llama-3.1-8B-Instruct-Turbo",
     "api_key": os.getenv("TOGETHER_API_KEY")},
    {"name": "Groq",     "base_url": "https://api.groq.com/openai/v1",    "model": "llama-3.1-8b-instant",
     "api_key": os.getenv("GROQ_API_KEY")},
]

prompt = "Define entropy in one sentence."
for p in PROVIDERS:
    if not p["api_key"]:
        continue
    client = OpenAI(api_key=p["api_key"], base_url=p["base_url"])
    resp = client.chat.completions.create(
        model=p["model"],
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0,
    )
    print(f"--- {p['name']} ({p['model']}) ---")
    print(resp.choices[0].message.content.strip())''')),

    # 7.2.4 — "Comparing general-purpose and domain-specific sentiment models"
    ('part-2-understanding-llms/module-07-modern-llm-landscape/section-7.2.html', '7.2.4', cb('python', '''# Compare a general-purpose sentiment model vs a finance-tuned one on financial text.
# Domain pretraining (FinBERT) often beats much larger general models on niche jargon.
from transformers import pipeline

general = pipeline("text-classification",
                   model="distilbert-base-uncased-finetuned-sst-2-english")
finbert = pipeline("text-classification",
                   model="ProsusAI/finbert")

examples = [
    "The company beat revenue expectations and raised guidance.",
    "Quarterly losses widened despite analyst projections.",
    "The stock plunged after the earnings call.",
    "The bond yields tightened sharply on the dovish Fed pivot.",
]

for text in examples:
    g = general(text)[0]
    f = finbert(text)[0]
    print(f"{text!r}")
    print(f"  general : {g['label']:>8s}  ({g['score']:.2f})")
    print(f"  finbert : {f['label']:>8s}  ({f['score']:.2f})")
# Note: on the last example, general models often miss "dovish pivot" but FinBERT catches it.''')),

    # 7.3.4 — "Compute-optimal inference: choosing strategy based on difficulty"
    ('part-2-understanding-llms/module-07-modern-llm-landscape/section-7.3.html', '7.3.4', cb('python', '''# Compute-optimal inference: spend more tokens on harder problems.
# Cheap classifier picks the strategy; expensive strategy only fires when justified.
from openai import OpenAI

client = OpenAI()

def estimate_difficulty(prompt: str) -> float:
    """Lightweight call to a small model to score 0.0-1.0 difficulty."""
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Rate task difficulty 0.0 (trivial) to 1.0 (very hard). Return ONLY a float."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.0,
        max_tokens=4,
    )
    try:
        return float(resp.choices[0].message.content.strip())
    except ValueError:
        return 0.5


def answer(prompt: str) -> str:
    """Cheap path for easy questions; chain-of-thought + self-consistency for hard ones."""
    difficulty = estimate_difficulty(prompt)

    if difficulty < 0.3:
        # Greedy, single shot
        return client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
        ).choices[0].message.content

    # Reasoning model with explicit chain-of-thought
    return client.chat.completions.create(
        model="o4-mini",
        messages=[{"role": "user", "content": prompt + "\\nThink step by step."}],
    ).choices[0].message.content


print(answer("What is 2 + 2?"))
print(answer("Prove that there are infinitely many primes."))''')),

    # =============== Chapter 9 — Inference Optimization ===============

    # 9.1.11 — "Example 4: Benchmarking quantization quality"
    ('part-2-understanding-llms/module-09-inference-optimization/section-9.1.html', '9.1.11', cb('python', '''# Benchmark how INT8/INT4 quantization degrades perplexity vs the FP16 baseline.
# Lower perplexity on a held-out set means the quantized model still predicts well.
import torch
import math
from transformers import AutoModelForCausalLM, AutoTokenizer
from datasets import load_dataset

tok = AutoTokenizer.from_pretrained("meta-llama/Llama-3.2-1B")
texts = load_dataset("wikitext", "wikitext-2-raw-v1", split="test[:200]")
encodings = tok("\\n\\n".join(t["text"] for t in texts), return_tensors="pt")

def perplexity(model, encodings, max_length: int = 1024) -> float:
    nlls = []
    seq_len = encodings.input_ids.size(1)
    for begin in range(0, seq_len, max_length):
        end = min(begin + max_length, seq_len)
        input_ids = encodings.input_ids[:, begin:end].to(model.device)
        with torch.no_grad():
            nlls.append(model(input_ids, labels=input_ids).loss * (end - begin))
    return math.exp(torch.stack(nlls).sum().item() / seq_len)

# FP16 baseline
fp16 = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-3.2-1B", torch_dtype=torch.float16, device_map="cuda")
print(f"FP16 perplexity: {perplexity(fp16, encodings):.3f}")

# INT8 via bitsandbytes (one-line quantization)
int8 = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-3.2-1B", load_in_8bit=True, device_map="cuda")
print(f"INT8 perplexity: {perplexity(int8, encodings):.3f}")

# INT4 (NF4) via bitsandbytes
int4 = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-3.2-1B", load_in_4bit=True, device_map="cuda")
print(f"INT4 perplexity: {perplexity(int4, encodings):.3f}")''')),

    # 9.2.1 — "Using a key-value cache to avoid redundant computation"
    ('part-2-understanding-llms/module-09-inference-optimization/section-9.2.html', '9.2.1', cb('python', '''# KV cache: store the K and V projections of every past position so we never
# recompute them. HuggingFace exposes this via the `past_key_values` argument.
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

tok = AutoTokenizer.from_pretrained("gpt2")
model = AutoModelForCausalLM.from_pretrained("gpt2")
model.eval()

input_ids = tok("The Eiffel Tower is", return_tensors="pt").input_ids

past_key_values = None
generated = input_ids
with torch.no_grad():
    for _ in range(20):
        # Only the LAST token participates in the new forward pass;
        # the KV cache provides everything before it for free.
        feed = generated if past_key_values is None else generated[:, -1:]
        out = model(feed, past_key_values=past_key_values, use_cache=True)
        past_key_values = out.past_key_values             # carry forward
        next_id = out.logits[:, -1, :].argmax(dim=-1, keepdim=True)
        generated = torch.cat([generated, next_id], dim=1)

print(tok.decode(generated[0]))
# Without KV cache, generating n tokens is O(n^2); with it, generation is O(n).''')),

    # 9.4.13 — "Example 4: Comprehensive benchmarking script"
    ('part-2-understanding-llms/module-09-inference-optimization/section-9.4.html', '9.4.13', cb('python', '''# Comprehensive serving benchmark: measure TTFT, throughput, and TBT under load.
# Drives a running vLLM (or any OpenAI-compatible) server with concurrent requests.
import asyncio
import time
import statistics
from openai import AsyncOpenAI

client = AsyncOpenAI(base_url="http://localhost:8000/v1", api_key="not-used")

async def run_request(prompt: str) -> dict:
    t0 = time.perf_counter()
    first_token_t = None
    tokens = 0
    stream = await client.chat.completions.create(
        model="meta-llama/Llama-3.1-8B-Instruct",
        messages=[{"role": "user", "content": prompt}],
        stream=True,
        max_tokens=128,
    )
    async for chunk in stream:
        if chunk.choices[0].delta.content:
            if first_token_t is None:
                first_token_t = time.perf_counter()
            tokens += 1
    t1 = time.perf_counter()
    return {
        "ttft_ms":      (first_token_t - t0) * 1000 if first_token_t else None,
        "total_ms":     (t1 - t0) * 1000,
        "tokens":       tokens,
        "tbt_ms":       (t1 - first_token_t) / max(1, tokens - 1) * 1000 if first_token_t else None,
    }


async def benchmark(prompts: list[str], concurrency: int = 8):
    sem = asyncio.Semaphore(concurrency)
    async def bounded(p):
        async with sem: return await run_request(p)
    return await asyncio.gather(*[bounded(p) for p in prompts])


prompts = ["Explain quantization in one paragraph."] * 64
results = asyncio.run(benchmark(prompts, concurrency=8))
ttft = [r["ttft_ms"] for r in results if r["ttft_ms"]]
tbt  = [r["tbt_ms"]  for r in results if r["tbt_ms"]]
print(f"TTFT p50/p95: {statistics.median(ttft):.0f}/{statistics.quantiles(ttft, n=20)[-1]:.0f} ms")
print(f"TBT  p50/p95: {statistics.median(tbt):.1f}/{statistics.quantiles(tbt,  n=20)[-1]:.1f} ms")''')),

    # =============== Chapter 24 + 26 — Lab starter/solutions ===============

    # 24.1.4 — "Installs torch, transformers, and numpy for the multi-agent framework selection lab"
    ('part-6-agentic-ai/module-24-multi-agent-systems/section-24.1.html', '24.1.4', cb('bash', '''# Install dependencies for the multi-agent framework selection lab
# torch + transformers cover the LLM backbone; numpy supports the scoring helpers
pip install torch transformers numpy''')),

    # 24.1.5 — "Lab step (starter code) : load the required libraries and prepare data"
    ('part-6-agentic-ai/module-24-multi-agent-systems/section-24.1.html', '24.1.5', cb('python', '''# Lab starter: framework selection skeleton. Students fill in the TODOs.
# Goal: given a list of candidate frameworks and a task description, score them.
from typing import Iterable
import numpy as np

FRAMEWORKS = ["LangGraph", "AutoGen", "CrewAI", "Swarm"]

def load_task_description() -> str:
    """TODO: load the task description from prompt.txt or your dataset."""
    raise NotImplementedError

def score_framework(name: str, description: str) -> float:
    """TODO: call your LLM with a scoring prompt; return a 0.0-1.0 fit score.
    Hints:
      - Build a small prompt template that lists the framework's strengths
      - Ask the model to rate task fit on a 0-10 scale, then divide by 10
    """
    raise NotImplementedError

def rank(frameworks: Iterable[str], description: str) -> list[tuple[str, float]]:
    """Score each candidate and return them sorted high-to-low."""
    scored = [(name, score_framework(name, description)) for name in frameworks]
    return sorted(scored, key=lambda x: -x[1])

if __name__ == "__main__":
    task = load_task_description()
    for name, fit in rank(FRAMEWORKS, task):
        print(f"  {name:>10s}: {fit:.2f}")''')),

    # 24.1.6 — "Complete solution for the multi-agent framework selection lab exercise"
    ('part-6-agentic-ai/module-24-multi-agent-systems/section-24.1.html', '24.1.6', cb('python', '''# Full solution for the framework-selection lab.
# Uses an LLM judge to score each candidate on the task description.
from openai import OpenAI
from pathlib import Path

client = OpenAI()

FRAMEWORKS = {
    "LangGraph": "Strong for explicit graph-based control flow; good with cycles and conditional edges; native LangChain integration.",
    "AutoGen":   "Optimized for conversational multi-agent systems; group chat patterns; human-in-the-loop friendly.",
    "CrewAI":    "Role-based agents (manager, researcher, writer); sequential or hierarchical processes; simple API.",
    "Swarm":     "Minimal, stateless agent routing primitives; good for tool-handoff patterns; easy to inspect.",
}

JUDGE_PROMPT = """Rate how well the framework below fits the task on a 0-10 scale.
Return ONLY a number between 0 and 10.

Framework: {name}
Description: {desc}

Task: {task}

Score:"""

def load_task_description() -> str:
    p = Path("prompt.txt")
    if p.exists(): return p.read_text(encoding="utf-8")
    return "Build a 3-agent pipeline for researching, drafting, and editing news articles."

def score_framework(name: str, task: str) -> float:
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": JUDGE_PROMPT.format(name=name, desc=FRAMEWORKS[name], task=task)}],
        temperature=0.0,
        max_tokens=4,
    )
    try:
        return float(resp.choices[0].message.content.strip()) / 10.0
    except ValueError:
        return 0.5

if __name__ == "__main__":
    task = load_task_description()
    scored = sorted(((n, score_framework(n, task)) for n in FRAMEWORKS), key=lambda x: -x[1])
    print(f"Task: {task!r}\\n")
    for name, fit in scored:
        print(f"  {name:>10s}: {fit:.2f}")''')),

    # =============== Chapter 26 — Lab starter/solutions ===============

    # 26.5.3 — "Installs torch, transformers, and numpy for the agent testing lab"
    ('part-6-agentic-ai/module-26-agent-safety-production/section-26.5.html', '26.5.3', cb('bash', '''# Install dependencies for the agent testing + contract validation lab
# pydantic supports tool-call schema validation; pytest runs the test suite
pip install torch transformers numpy pydantic pytest''')),

    # 26.5.4 — "Lab step (starter code) : load the required libraries and prepare data"
    ('part-6-agentic-ai/module-26-agent-safety-production/section-26.5.html', '26.5.4', cb('python', '''# Lab starter: agent contract validation. Students fill in the TODOs.
from pydantic import BaseModel, Field
from typing import Literal

# 1) Define the contract the agent's tool calls must satisfy
class WeatherQuery(BaseModel):
    """TODO: extend with required and optional fields the agent must produce."""
    city: str = Field(..., description="City name; non-empty")
    units: Literal["c", "f"] = "c"

def call_agent(prompt: str) -> dict:
    """TODO: call your agent and return its parsed JSON tool-call payload."""
    raise NotImplementedError

def validate_tool_call(payload: dict) -> WeatherQuery:
    """TODO: parse `payload` into the WeatherQuery contract.
    Hint: use WeatherQuery.model_validate; let it raise on failure."""
    raise NotImplementedError

if __name__ == "__main__":
    prompt = "What's the weather in Tokyo in Fahrenheit?"
    payload = call_agent(prompt)
    contract = validate_tool_call(payload)
    print(f"Validated: {contract.model_dump()}")''')),

    # 26.5.5 — "Complete solution for the agent testing lab exercise"
    ('part-6-agentic-ai/module-26-agent-safety-production/section-26.5.html', '26.5.5', cb('python', '''# Full solution for the agent contract validation lab.
import json
from pydantic import BaseModel, Field, ValidationError
from typing import Literal
from openai import OpenAI

client = OpenAI()

class WeatherQuery(BaseModel):
    city: str = Field(..., min_length=1, description="City name; non-empty")
    country_code: str | None = Field(None, pattern=r"^[A-Z]{2}$",
                                      description="Optional ISO 3166-1 alpha-2 country code")
    units: Literal["c", "f"] = "c"


SYSTEM_PROMPT = (
    "You are a weather assistant. When the user asks about weather, respond with "
    "a JSON object {\\"city\\": ..., \\"country_code\\": ..., \\"units\\": \\"c\\" or \\"f\\"}. "
    "Nothing else."
)


def call_agent(prompt: str) -> dict:
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        response_format={"type": "json_object"},
        temperature=0.0,
    )
    return json.loads(resp.choices[0].message.content)


def validate_tool_call(payload: dict) -> WeatherQuery:
    try:
        return WeatherQuery.model_validate(payload)
    except ValidationError as e:
        # In production: log payload, return a structured error, ask agent to retry
        raise


def test_basic_call():
    payload = call_agent("What's the weather in Tokyo in Fahrenheit?")
    contract = validate_tool_call(payload)
    assert contract.city.lower() == "tokyo"
    assert contract.units == "f"


if __name__ == "__main__":
    test_basic_call()
    print("contract validated; tests passed")''')),
]


def main() -> int:
    fixed = skipped = 0
    for rel, cap_num, block in BLOCKS:
        p = ROOT / rel
        if not p.exists():
            print(f'  MISSING file: {rel}')
            continue
        text = p.read_text(encoding='utf-8')
        anc = anchor(cap_num)
        if anc not in text:
            print(f'  NO ANCHOR for CF {cap_num} in {rel}')
            continue
        # Idempotent: skip if block already present
        # Use a stable signature line (2nd line, first 50 chars)
        sig = block.split('\n', 2)[1][:50]
        if sig in text:
            print(f'  already inserted: CF {cap_num}')
            skipped += 1
            continue
        new_text = text.replace(anc, block + anc, 1)
        p.write_text(new_text, encoding='utf-8')
        print(f'  + CF {cap_num} in {rel.rsplit("/", 1)[-1]}')
        fixed += 1
    print(f'\nInserted {fixed} blocks; skipped {skipped} already-present.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
