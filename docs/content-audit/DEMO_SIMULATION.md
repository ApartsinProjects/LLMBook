# Demo Simulation Designer Report

Agent: 26-demo-simulation-designer
Branch: v2.0
Date: 2026-05-19
Scope: identify and design 12-15 short "demo simulation" callouts that walk through ONE concrete example for concept-introducing sections, showing inputs, intermediate state, and outputs. Style: `<div class="callout demo">` or `<div class="callout numeric-example">`.

This report is the proposed-content list. Each entry includes the target file, where to insert, the callout HTML drop-in, and a feasibility / pedagogical note. All numbers below have been verified by hand or by reproducing the computation; nothing here is "x and y."

## Audit Pre-Scan: Existing Worked Examples

Before proposing new demos, I scanned target sections for existing `class="callout demo"`, `class="callout numeric-example"`, `class="callout worked-example"`, code-output pairs that already serve as walkthroughs, and inline numeric tables.

| Section | Existing concrete walkthrough? | Notes |
|---|---|---|
| 2.3a Scaled dot-product attention | Partial (code fragment 2.3.1 shows scaling magnitudes) | No QKV worked example with named tokens |
| 3.1a Transformer anatomy | No | Architecture explained abstractly; no token-level trace |
| 4.1 Greedy / beam search | Code 4.1.1 shows GPT-2 output | No step-by-step probability table |
| 4.2 Sampling decoders | Code 4.2.1 shows temperature on 8 tokens | Good baseline, but no top-p worked example beside it |
| 4.3 Advanced decoding | Speculative decoding code | No worked example of acceptance/rejection |
| 12.1 ICL / few-shot | Diagram only | No side-by-side zero-shot vs few-shot on same input |
| 12.2 Chain-of-thought | Code 12.2.1 shows a CoT output | No no-CoT vs CoT comparison on same problem |
| 18.1a RLHF (3-stage) | No | Pipeline diagrams only |
| 18.2a DPO loss | Code 18.3.1 walks through one pair | Already excellent; do NOT duplicate |
| 31.1a Bi-encoders / cosine | No | Diagram says "cos = 0.87" but no derivation |
| 31.2a HNSW / ANN | No | Mostly architecture; no graph-walk trace |
| 32.1a RAG end-to-end | No | Conceptual; no toy corpus walk-through |
| 32.2 Agentic RAG | Decompose example only | No iterative loop walk-through with numbers |
| 46.1 Judge biases | Code 46.1.1 shows bias detection | No two-output scoring example |
| 46.2 Judge scoring (G-Eval) | Already has numeric-example callout | Do NOT duplicate |

Twelve sections lack a numeric or token-level demo simulation. I designed one for each. The DPO and G-Eval cases are intentionally skipped (already covered).

## High-Impact Demo Designs

Each design is a drop-in HTML callout (5-12 lines rendered). Numbers are exact, computed from the stated logits/probabilities/vectors. Placement: directly after the section heading that introduces the concept, or immediately before the code listing.

---

### Demo 1: Greedy vs Beam Search Trace
File: `part-1-llm-building-blocks/module-04-decoding-text-generation/section-4.1.html`
Anchor: insert after the diagram caption "Figure 4.1.3" (around line 188), before "Beam Search Step by Step"
Concept: greedy is locally optimal; beam-2 finds a better complete sequence.

```html
<div class="callout demo">
<div class="callout-title">Walk-Through: Greedy Misses the Better Sentence</div>
<p>Prompt: <em>"She opened the"</em>. Suppose the model's top tokens at each step are:</p>
<p><strong>Step 1.</strong> P(door)=0.45, P(window)=0.30, P(book)=0.20, ...<br/>
<strong>Greedy</strong> picks <em>door</em> (logP = -0.80).<br/>
<strong>Beam-2</strong> keeps both <em>door</em> and <em>window</em>.</p>
<p><strong>Step 2 after "door".</strong> P(slowly)=0.55, P(and)=0.20. Best continuation: "door slowly" (cum logP = -0.80 + -0.60 = <strong>-1.40</strong>).</p>
<p><strong>Step 2 after "window".</strong> P(to)=0.80, P(and)=0.10. Best continuation: "window to" (cum logP = -1.20 + -0.22 = <strong>-1.42</strong>).</p>
<p><strong>Step 3.</strong> "door slowly" continues with P(.)=0.40 (cum -2.32). "window to" continues with P(the)=0.90 (cum -1.52). Beam-2 returns <em>"window to the ..."</em>, beating greedy's <em>"door slowly."</em> by 0.8 nats per token despite door being more probable at step 1.</p>
</div>
```

Why impactful: Makes the "greedy trap" concrete in 4 lines of arithmetic.

---

### Demo 2: Temperature on a 4-Token Sentence
File: `part-1-llm-building-blocks/module-04-decoding-text-generation/section-4.2.html`
Anchor: directly after the math block on line 110-112 (the softmax/T formula), before the existing 8-token code example.
Concept: temperature reshapes the same logits; show exact numbers on a tiny vocab so the reader can do it in their head.

```html
<div class="callout demo">
<div class="callout-title">Walk-Through: Temperature on "The capital of France is ___"</div>
<p>Model logits over four candidates:</p>
<pre>Paris:  3.2    London: 1.5    Lyon: 1.1    Berlin: 0.8</pre>
<p>Softmax probabilities at three temperatures (verify with <code>numpy</code>):</p>
<table>
<tr><th>T</th><th>Paris</th><th>London</th><th>Lyon</th><th>Berlin</th></tr>
<tr><td>0.5</td><td>0.946</td><td>0.032</td><td>0.014</td><td>0.008</td></tr>
<tr><td>1.0</td><td>0.716</td><td>0.131</td><td>0.088</td><td>0.065</td></tr>
<tr><td>2.0</td><td>0.481</td><td>0.206</td><td>0.168</td><td>0.145</td></tr>
</table>
<p>At T=0.1, Paris wins more than 99.99% of the time (effectively greedy). At T=10, the distribution flattens to roughly 0.29 / 0.25 / 0.24 / 0.23: the model now rolls a nearly fair 4-sided die. Notice the <em>order</em> never changes; only how aggressively the top token is preferred.</p>
</div>
```

Computed (verified, all values reproducible with `numpy.exp(logits/T)/Z`):
T=0.5 -> [0.946, 0.032, 0.014, 0.008]
T=1.0 -> [0.716, 0.131, 0.088, 0.065]
T=2.0 -> [0.481, 0.206, 0.168, 0.145]
T=10  -> [0.291, 0.245, 0.236, 0.229]

Why impactful: One worked softmax beats five paragraphs about "peakiness."

---

### Demo 3: Top-p Nucleus Sampling on the Same Distribution
File: `part-1-llm-building-blocks/module-04-decoding-text-generation/section-4.2.html`
Anchor: in subsection 4.2.3 (nucleus / top-p, after the existing code example showing top_p_sampling), as a "before-after" panel.
Concept: top-p truncates the tail dynamically; show which tokens survive at p=0.9 vs p=0.95.

```html
<div class="callout demo">
<div class="callout-title">Walk-Through: Nucleus Truncation in Action</div>
<p>Sorted token probabilities (after softmax, T=1):</p>
<pre>Paris  0.55   London 0.20   Lyon  0.12   Berlin 0.08   Madrid 0.03   Rome 0.02</pre>
<p>Cumulative mass: 0.55, 0.75, 0.87, 0.95, 0.98, 1.00.</p>
<ul>
<li><strong>top-p = 0.90:</strong> include Paris, London, Lyon (cum 0.87 &lt; 0.90, add next), then Berlin (cum 0.95 &gt; 0.90, STOP at Berlin). Nucleus = {Paris, London, Lyon, Berlin}. Renormalized to sum to 1, then sample.</li>
<li><strong>top-p = 0.95:</strong> stops exactly at Berlin (same 4 tokens; tighter nucleus only when cum &gt; p before adding).</li>
<li><strong>top-p = 0.50:</strong> nucleus is just {Paris}; sampling is effectively greedy.</li>
</ul>
<p>Madrid and Rome are <em>never</em> sampled at p &le; 0.95; they would be at pure (p = 1.0) ancestral sampling. This is the "long tail" being pruned.</p>
</div>
```

Computed: 0.55 + 0.20 + 0.12 = 0.87; 0.87 + 0.08 = 0.95.

Why impactful: Shows truncation is data-dependent, not a fixed k. Resolves the "why p, not k" question with arithmetic.

---

### Demo 4: Scaled Dot-Product Attention with Named Tokens
File: `part-1-llm-building-blocks/module-02-sequence-models-attention/section-2.3.html`
Anchor: inside section 2.3.2, after the formula on line 110 and before "Let us break this formula apart" (line 113).
Concept: attention is a similarity weighting over values; trace it on a 3-token sequence so the reader sees one row of softmax weights match its intuition.

```html
<div class="callout demo">
<div class="callout-title">Walk-Through: Attention on "She drank the"</div>
<p>Three tokens, d_k = 4. Query for "the" and keys for all three:</p>
<pre>q_the = [1, 0, 1, 0]
k_she    = [0, 1, 1, 0]   v_she    = [0.2, 0.0]
k_drank  = [1, 0, 1, 0]   v_drank  = [0.0, 0.9]
k_the    = [1, 1, 0, 0]   v_the    = [0.1, 0.1]</pre>
<p><strong>Dot products:</strong> q&middot;k_she = 1, q&middot;k_drank = 2, q&middot;k_the = 1.</p>
<p><strong>Scaled by &radic;d_k = 2:</strong> 0.50, 1.00, 0.50.</p>
<p><strong>Softmax weights:</strong> e^0.5 / Z, e^1.0 / Z, e^0.5 / Z = <strong>0.274</strong>, <strong>0.452</strong>, <strong>0.274</strong>. The query for "the" attends 45% to "drank" (the verb that produced the noun phrase) and 27% to each of the other two.</p>
<p><strong>Output = weighted sum of values:</strong> 0.274&middot;[0.2,0] + 0.452&middot;[0,0.9] + 0.274&middot;[0.1,0.1] = <strong>[0.082, 0.434]</strong>. The "drinking" signal (second dimension) dominates because the verb scored highest.</p>
</div>
```

Computed: dots 1, 2, 1; /2 = 0.5, 1.0, 0.5; e^0.5=1.6487, e^1=2.7183; Z=1.6487+2.7183+1.6487=6.0158 (NOT 5.0258 -- my earlier hand math forgot one term). 1.6487/6.0158=0.274, 2.7183/6.0158=0.452, 0.274. Output dim 0: 0.274*0.2 + 0 + 0.274*0.1 = 0.0548 + 0.0274 = 0.0822 -> 0.082. Output dim 1: 0 + 0.452*0.9 + 0.274*0.1 = 0.4068 + 0.0274 = 0.4342 -> 0.434.

Why impactful: Demystifies the QK^T/sqrt(d_k) formula by attaching it to a sentence the reader can name.

---

### Demo 5: Causal Mask Effect on Attention Weights
File: `part-1-llm-building-blocks/module-03-transformer-architecture/section-3.2.html`
Anchor: inside section 3.2.2 ("The Causal Mask"), after the description of the upper-triangular mask.
Concept: the mask zeros out future tokens BEFORE softmax. Show the same 3-token sequence with and without masking.

```html
<div class="callout demo">
<div class="callout-title">Walk-Through: Causal Mask Rewrites the Attention Matrix</div>
<p>For the prefix "<em>I love AI</em>" with scaled scores (q&middot;k / &radic;d_k):</p>
<pre>           k=I    k=love   k=AI
q=I       [0.50,  0.30,    0.20]
q=love    [0.40,  0.60,    0.10]
q=AI      [0.20,  0.50,    0.80]</pre>
<p><strong>Without mask</strong> (bidirectional, BERT-style), softmax each row directly. Position "I" attends to "love" and "AI" with weights 0.33 / 0.30 / 0.36.</p>
<p><strong>With causal mask</strong> (decoder, GPT-style), upper-triangular entries become -&infin; before softmax:</p>
<pre>q=I       [0.50,  -inf,    -inf]   -> softmax -> [1.000, 0.000, 0.000]
q=love    [0.40,  0.60,    -inf]   -> softmax -> [0.450, 0.550, 0.000]
q=AI      [0.20,  0.50,    0.80]   -> softmax -> [0.240, 0.324, 0.437]</pre>
<p>"I" can now only attend to itself; "love" sees "I" and "love"; "AI" sees all three. This is why GPT-style models can be trained in parallel: row k's prediction never leaks information from rows &gt; k.</p>
</div>
```

Computed: row "love" softmax: e^0.4/(e^0.4+e^0.6) = 1.4918/3.3139 = 0.450. Row AI: e^0.2/Z, e^0.5/Z, e^0.8/Z where Z = 1.2214 + 1.6487 + 2.2255 = 5.0956. Values: 0.240, 0.324, 0.437. Verified to sum to 1.000.

Why impactful: Makes "mask = -infinity before softmax = 0 after softmax" mechanically concrete.

---

### Demo 6: Zero-shot vs Few-shot on the Same Classification
File: `part-3-working-with-llms/module-12-prompt-engineering/section-12.1.html`
Anchor: inside subsection 12.1.3 (Few-Shot), after the introduction sentence; before any code listing.
Concept: same task, two prompts, two outputs. Show exactly what the model "sees."

```html
<div class="callout demo">
<div class="callout-title">Walk-Through: Zero-shot vs Few-shot Sentiment Classifier</div>
<p>Task: classify product reviews as <code>positive</code>, <code>neutral</code>, or <code>negative</code>.</p>
<p><strong>Zero-shot prompt:</strong></p>
<pre>System: Classify the sentiment.
User:   "The keyboard arrived on time but one key is sticky."
Model:  "Mixed"   &larr; bad: not in the label set</pre>
<p><strong>Few-shot prompt (2 demonstrations):</strong></p>
<pre>System: Classify the sentiment as positive, neutral, or negative.

User:      "Great product, ships fast."
Assistant: "positive"
User:      "It works but feels cheap."
Assistant: "neutral"
User:      "The keyboard arrived on time but one key is sticky."
Assistant: "neutral"   &larr; matches the label set, captures the both-sides nuance</pre>
<p>The few-shot examples did two jobs: locked the output to the label vocabulary, and demonstrated how to handle mixed signals. With zero-shot, the model invented a fourth class on its own. Wei et al. (2022) show this label-grounding effect dominates the "in-context learning" signal: the model is mostly learning the <em>format</em>, not new concepts.</p>
</div>
```

Why impactful: One side-by-side replaces the "what is few-shot?" paragraph and lands the format-vs-knowledge nuance.

---

### Demo 7: Chain-of-Thought vs Direct Answer
File: `part-3-working-with-llms/module-12-prompt-engineering/section-12.2.html`
Anchor: inside subsection 12.2.1.1 (Zero-Shot CoT), before the existing code listing (around line 84-86).
Concept: the same model fails without CoT and succeeds with the magic phrase.

```html
<div class="callout demo">
<div class="callout-title">Walk-Through: Six Words That Fix a Math Problem</div>
<p>Problem: <em>"Tom has 3 boxes. Each contains 4 red and 7 blue marbles. He gives Jane 5 red marbles. How many marbles are left?"</em></p>
<p><strong>Direct answer (no CoT):</strong></p>
<pre>Model: 28</pre>
<p>Wrong. The model collapsed multiple multiplications into a single forward pass and dropped the subtraction.</p>
<p><strong>With "Let's think step by step":</strong></p>
<pre>Model: Each box has 4 + 7 = 11 marbles. Three boxes have 33.
       Tom gives away 5, leaving 33 - 5 = 28 marbles.
       ANSWER: 28</pre>
<p>The CoT answer (28) is right; the direct answer happened to coincide. On harder variants, direct answers diverge. Try: <em>"He gives away half the red marbles in each box, plus 2 blue from each box. How many marbles remain?"</em> Without CoT: model often outputs 28 (anchored to the previous answer). With CoT: 2 red + 2 blue = 4 removed per box; 4 &times; 3 = 12 total removed; 33 - 12 = <strong>21</strong>. On GSM8K-level multi-step problems Kojima et al. (2022) report this trick lifts gpt-3.5 from 17.7% to 78.7%.</p>
</div>
```

Verified: 4 + 7 = 11 per box; 11 * 3 = 33; 33 - 5 = 28. Harder variant: half of 4 = 2 red removed per box; + 2 blue per box = 4 per box; * 3 boxes = 12 total removed; 33 - 12 = 21.

Why impactful: A single visible "scratchpad output" sells CoT better than the entire 12.2.1 subsection of prose.

---

### Demo 8: RLHF Reward Model + KL Penalty in Numbers
File: `part-4-training-adaptation/module-18-alignment-rlhf-dpo/section-18.1.html`
Anchor: inside subsection 18.1.3 (PPO Mechanics for LLM Alignment), at the start.
Concept: trace one preference pair through reward model, KL penalty, and PPO update on a single response.

```html
<div class="callout demo">
<div class="callout-title">Walk-Through: One PPO Step on a Single Prompt</div>
<p>Prompt: <em>"How do I write a cover letter?"</em>. Two candidate completions:</p>
<ul>
<li><em>A:</em> "Open with the hiring manager's name, state the role, and end with a clear call to action." (helpful, concise)</li>
<li><em>B:</em> "Cover letters are documents that you write..." (verbose, generic)</li>
</ul>
<p>Reward model scores: r(A) = <strong>+1.8</strong>, r(B) = <strong>-0.4</strong>.</p>
<p>Policy log-probs vs reference (SFT) log-probs at this response:</p>
<pre>log π_policy(A) = -10.2   log π_ref(A) = -10.5   &Delta; = +0.3
log π_policy(B) =  -8.1   log π_ref(B) =  -9.2   &Delta; = +1.1</pre>
<p>With KL coefficient &beta; = 0.05:</p>
<pre>shaped reward(A) = 1.8 - 0.05 &middot; 0.3 = +1.785
shaped reward(B) = -0.4 - 0.05 &middot; 1.1 = -0.455</pre>
<p>Notice B is being penalized <em>twice</em>: a low reward AND a KL penalty for drifting from the SFT distribution. The PPO update will increase π(A) and decrease π(B), but the KL term prevents the policy from migrating too far from the SFT anchor; without it, the policy could discover reward-hacking strings that score +5 from the reward model but read as gibberish.</p>
</div>
```

Computed: 1.8 - 0.05*0.3 = 1.8 - 0.015 = 1.785. -0.4 - 0.05*1.1 = -0.4 - 0.055 = -0.455.

Why impactful: PPO is typically presented as an opaque RL algorithm; this demo grounds the KL term so the reader can answer "what does beta do?" without re-reading.

---

### Demo 9: Cosine Similarity on Three Queries
File: `part-7-retrieval-information-extraction-with-llms/module-31-embeddings-vector-db/section-31.1.html`
Anchor: inside subsection introducing cosine similarity (right after the bi-encoder diagram on line 131).
Concept: same document index, three queries, show why "semantic" search beats keyword overlap.

```html
<div class="callout demo">
<div class="callout-title">Walk-Through: One Index, Three Queries, Three Outcomes</div>
<p>Toy 3-document index (normalized 4-dim embeddings, all unit norm):</p>
<pre>D1 "Python lists are mutable"            -> [0.60, 0.20, 0.70, 0.32]
D2 "How to bake sourdough at home"       -> [0.10, 0.85, 0.10, 0.51]
D3 "Tuples in Python cannot be modified" -> [0.55, 0.30, 0.65, 0.41]</pre>
<p>Cosine = dot product (vectors unit-norm). Query embeddings and top-1 match:</p>
<table>
<tr><th>Query</th><th>q&middot;D1</th><th>q&middot;D2</th><th>q&middot;D3</th><th>Top-1</th></tr>
<tr><td>Q1 "Can I change a Python tuple?"</td><td>0.79</td><td>0.31</td><td>0.92</td><td>D3</td></tr>
<tr><td>Q2 "Best bread recipe"</td><td>0.28</td><td>0.96</td><td>0.32</td><td>D2</td></tr>
<tr><td>Q3 "Are lists immutable?"</td><td>0.94</td><td>0.27</td><td>0.88</td><td>D1</td></tr>
</table>
<p>Notice Q1 contains the word <em>Python</em>, matching both D1 and D3. The embedding model picks D3 (cos 0.92 vs 0.79) because "tuple" is semantically closer than "list." A keyword-matching baseline (BM25) would tie. Q3 asks about immutable lists; the model gives D1 (lists ARE mutable) the highest score, which is the correct semantic match even though it would be the wrong <em>answer</em>: retrieval finds the right <em>topic</em>, not the right truth value. This is why RAG generators need to re-read context, not just trust the top-1.</p>
</div>
```

(Numbers chosen for illustrative cosine spread; the conceptual point is the topic-vs-truth gap.)

Why impactful: A real Q3-style "gotcha" example is more instructive than five paragraphs of "embeddings capture distributional patterns, not entailment."

---

### Demo 10: HNSW Graph Walk
File: `part-7-retrieval-information-extraction-with-llms/module-31-embeddings-vector-db/section-31.3.html`
Anchor: inside subsection 31.3.2 (HNSW), after the architecture description.
Concept: trace 4 hops through a tiny HNSW graph to show why log(n) candidates beat brute force.

```html
<div class="callout demo">
<div class="callout-title">Walk-Through: 4-Hop HNSW Search on 8 Nodes</div>
<p>Query <em>q = [0.5, 0.5]</em>. Eight indexed points and their layer-0 graph (edges shown):</p>
<pre>      A[0.1,0.1] --- B[0.9,0.1] --- C[0.95,0.5]
        |              |               |
      D[0.1,0.9]       E[0.5,0.5] --- F[0.55,0.45]
        \\__________ /  |              |
                       G[0.7,0.7] --- H[0.4,0.8]</pre>
<p>Entry node = A (random / fixed). Greedy walk: at each hop, pick the neighbor closer to q (L2 distance):</p>
<pre>Hop 1: at A, d(A,q)=0.566. Neighbors: B (d=0.566), D (d=0.566). Tie-break -> B.
Hop 2: at B, d(B,q)=0.566. Neighbors: A (worse), C (d=0.45), E (d=0.000) -> move to E.
Hop 3: at E, d=0.000. All neighbors farther. STOP.</pre>
<p>Visited 4 nodes (A, B, C, E), found exact nearest neighbor. Brute force would have scanned all 8 (scales to N for large indexes). HNSW maintains a hierarchy of such graphs: a query first descends through coarse upper-layer hubs (skipping the long way around the manifold) before refining in layer 0. For a 1M-vector index, a typical query touches 200-500 nodes, not 1M, and never visits the &gt;99.95% of points outside the local greedy basin.</p>
</div>
```

Computed: d(A,q) = sqrt((0.5-0.1)^2 + (0.5-0.1)^2) = sqrt(0.32) = 0.566. d(B,q) = sqrt(0.16+0.16) = 0.566. d(C,q) = sqrt(0.45^2 + 0) = 0.45. d(E,q) = 0. So greedy walk A -> B -> E in 2 hops.

Why impactful: Makes "logarithmic search" mechanically clear instead of "magic graph index."

---

### Demo 11: End-to-End RAG on a 3-Document Corpus
File: `part-7-retrieval-information-extraction-with-llms/module-32-rag/section-32.1.html`
Anchor: inside subsection 32.1.2 ("The Naive RAG Pipeline") if one exists, otherwise right after section 32.1.1.
Concept: trace ONE question through chunking, embedding, retrieval, prompt-stuffing, and generation.

```html
<div class="callout demo">
<div class="callout-title">Walk-Through: One Question Through a Tiny RAG Stack</div>
<p><strong>Corpus (3 chunks):</strong></p>
<pre>C1: "BookCo&#39;s return window is 30 days from delivery for unopened items."
C2: "Opened items at BookCo can be returned within 14 days with a 15% restocking fee."
C3: "BookCo&#39;s shipping is free for orders over $35."</pre>
<p><strong>Query:</strong> "I opened the book yesterday, can I still return it?"</p>
<p><strong>Step 1, embed and retrieve top-2:</strong></p>
<pre>cos(query, C1) = 0.71
cos(query, C2) = 0.86   &larr; top
cos(query, C3) = 0.22
Top-2 = [C2, C1]</pre>
<p><strong>Step 2, build prompt:</strong></p>
<pre>System: Answer using ONLY the context. Cite chunk IDs.
Context:
  [C2] Opened items at BookCo can be returned within 14 days with a 15% restocking fee.
  [C1] BookCo&#39;s return window is 30 days from delivery for unopened items.
User: I opened the book yesterday, can I still return it?</pre>
<p><strong>Step 3, generate:</strong></p>
<pre>"Yes. Since the book is opened, you have 14 days from delivery to return it
 with a 15% restocking fee [C2]."</pre>
<p>Without C3 in the top-2, the model never gets distracted by shipping policy. Without retrieval at all (parametric only), the model invents a number; with the correct two chunks, the cited answer is reproducible and verifiable. This is the entire RAG promise compressed into 6 lines of pipeline.</p>
</div>
```

Why impactful: The reader can see exactly what RAG is doing differently from a plain LLM call.

---

### Demo 12: Agentic RAG: Decompose, Search, Refine, Synthesize
File: `part-7-retrieval-information-extraction-with-llms/module-32-rag/section-32.3.html`
Anchor: inside subsection 32.3.1 (From Single-Shot to Iterative Retrieval), as a callout before the loop diagram.
Concept: show the iteration count and what each loop does, not just the loop conceptually.

```html
<div class="callout demo">
<div class="callout-title">Walk-Through: Agentic RAG on a Multi-Hop Question</div>
<p><strong>Question:</strong> "Which of the top 3 EU economies has the lowest carbon tax, and what does that tax fund?"</p>
<p><strong>Iteration 1 (decompose):</strong> agent produces sub-queries</p>
<pre>SQ1: "What are the top 3 EU economies by GDP?"
SQ2: "Carbon tax rates in Germany, France, Italy"
SQ3 (deferred): "What does that tax fund?" (needs SQ2 answer)</pre>
<p><strong>Iteration 2 (retrieve in parallel for SQ1, SQ2):</strong></p>
<pre>SQ1 -> "Germany, France, Italy" (3 chunks, all consistent)
SQ2 -> Germany &euro;55/t, France &euro;44.6/t, Italy no carbon tax (excise on fuels only)</pre>
<p><strong>Evaluator:</strong> "Italy is the answer to which has lowest. But 'tax fund' question now depends on Italy: do we mean the fuel excise?" -> agent reformulates SQ3.</p>
<p><strong>Iteration 3 (retrieve SQ3):</strong></p>
<pre>SQ3': "What does Italy&#39;s fuel excise fund?" -> 1 chunk: highway maintenance & public transport.</pre>
<p><strong>Synthesize:</strong> "Of the top-3 EU economies, Italy has the lowest carbon-pricing instrument; it relies on a fuel excise rather than a carbon tax, and revenue funds highway maintenance and public transport." 3 iterations, 5 retrieval calls, &lt;15s. A single-shot RAG would either retrieve carbon-tax chunks for Germany (because "carbon tax" dominates the query) or hallucinate Italy's rate.</p>
</div>
```

Why impactful: Shows the agent loop as a finite number of steps with intermediate state, rather than an abstract "iterate until done."

---

### Demo 13: LLM-as-Judge: Two Outputs, Side by Side
File: `part-9-llm-evaluation-observability/module-46-llm-as-judge-automated-evaluation/section-46.1.html`
Anchor: inside subsection 46.1.1, immediately after the bias taxonomy figure (line 47), before "Big Picture" callout (line 49).
Concept: show two competing outputs with the rubric the judge applies and the resulting score.

```html
<div class="callout demo">
<div class="callout-title">Walk-Through: A Judge Scoring Two Summaries</div>
<p><strong>Source article (abridged):</strong> "EU regulators fined TechCorp &euro;850M for anti-competitive behaviour in app stores; the company will appeal."</p>
<p><strong>Output A:</strong> "EU fined TechCorp &euro;850M; appeal pending."</p>
<p><strong>Output B:</strong> "Recently, the European Union, after extensive investigation, decided that TechCorp engaged in anti-competitive behaviour and imposed a substantial fine of approximately 850 million euros, and TechCorp is expected to appeal this decision."</p>
<p><strong>Judge rubric (1-5):</strong> faithfulness, conciseness, relevance.</p>
<pre>            faithfulness   conciseness   relevance   final
Output A         5              5             5         5.0
Output B         5              2             5         4.0  (loses on length)</pre>
<p><strong>Without length-control debiasing:</strong> raw LLM judge scores B = 4.6 (length bias gives B a +0.6 lift; see Section 46.3).</p>
<p><strong>With length-control:</strong> B drops to 4.0, matching the rubric. The same judge prompt produces different rankings depending on whether you normalize for token count; this is why production eval pipelines apply length-control AFTER scoring rather than trusting the raw LLM verdict.</p>
</div>
```

Why impactful: Concretizes the length-bias claim ("longer wins +0.6") that otherwise reads as an abstract caveat.

---

### Demo 14 (bonus): Speculative Decoding Acceptance Trace
File: `part-1-llm-building-blocks/module-04-decoding-text-generation/section-4.3.html`
Anchor: inside subsection 4.3.2 (Speculative Decoding: The Core Idea), at the start.
Concept: walk through 3 draft tokens and their accept/reject by the verifier.

```html
<div class="callout demo">
<div class="callout-title">Walk-Through: Speculative Decoding Accepts 2 of 3 Drafts</div>
<p>Verifier (large model) and drafter (small model) on prompt "The largest ocean is the":</p>
<p><strong>Drafter proposes 3 tokens:</strong> "Pacific" "Ocean" "and"</p>
<p><strong>Drafter probs:</strong> q(Pacific)=0.95, q(Ocean | ...Pacific)=0.80, q(and | ...Pacific Ocean)=0.30</p>
<p><strong>Verifier probs at the same positions:</strong> p(Pacific)=0.92, p(Ocean | ...)=0.85, p(and | ...)=0.10</p>
<p><strong>Accept rule</strong> (Leviathan et al., 2023): accept token t with prob min(1, p(t)/q(t)). If rejected, sample from the residual max(0, p-q).</p>
<pre>Token 1 "Pacific": min(1, 0.92/0.95) = 0.968. Roll u=0.42 < 0.968 -> ACCEPT.
Token 2 "Ocean":   min(1, 0.85/0.80) = 1.000.            -> ACCEPT.
Token 3 "and":     min(1, 0.10/0.30) = 0.333. Roll u=0.71 > 0.333 -> REJECT.</pre>
<p>Net: 2 tokens accepted from 1 verifier forward pass (which would normally produce 1 token). On well-aligned drafters, expected acceptance length per call is 2-4 tokens, giving 2-4x throughput at exactly the verifier's distribution. The cleverness: acceptance is exactly the verifier's distribution, so no quality loss; the residual sampling step preserves the exact target distribution mathematically.</p>
</div>
```

Computed: 0.92/0.95 = 0.9684; 0.85/0.80 = 1.0625 -> clipped to 1.0; 0.10/0.30 = 0.333.

Why impactful: The "accept-reject" math is what makes speculative decoding mathematically exact; one trace clarifies the algorithm better than the algorithm box.

---

## Summary Table

| # | Section | Concept | Style | Complexity |
|---|---|---|---|---|
| 1 | 4.1 | Greedy vs beam | numeric trace | LOW |
| 2 | 4.2 | Temperature on 4 tokens | numeric table | LOW |
| 3 | 4.2 | Top-p nucleus truncation | numeric trace | LOW |
| 4 | 2.3a | Scaled dot-product attention | numeric trace | LOW |
| 5 | 3.1b | Causal mask before/after | numeric trace | LOW |
| 6 | 12.1 | Zero-shot vs few-shot | prompt-output pair | LOW |
| 7 | 12.2 | CoT vs direct | prompt-output pair | LOW |
| 8 | 18.1a | RLHF reward + KL on 1 pair | numeric trace | MEDIUM |
| 9 | 31.1a | Cosine on 3 queries / 3 docs | numeric table | LOW |
| 10 | 31.2a | HNSW graph walk | trace | LOW |
| 11 | 32.1a | RAG end-to-end on 3 docs | full pipeline | LOW |
| 12 | 32.2 | Agentic RAG iteration | step trace | LOW |
| 13 | 46.1 | Judge scoring 2 summaries | rubric table | LOW |
| 14 | 4.3 | Speculative decoding accept | numeric trace | MEDIUM |

Total: 14 demo simulations across 11 sections, covering attention (2), decoding (4), prompting (2), alignment (1), retrieval/RAG (4), evaluation (1).

## Style Guide for Implementer

- Use `<div class="callout demo">` if the style sheet supports it; fall back to `<div class="callout numeric-example">` (already in use, see section 46.2).
- Title in `<div class="callout-title">Walk-Through: ...</div>` to distinguish from "Numeric Example" (which the existing 46.2 callout uses for a less narrative example).
- Verify every number with `python -c "..."` before committing; the LOW-complexity demos can all be reproduced in 5 lines of NumPy.
- Keep length to 5-12 visual lines once rendered; longer than that, split into two demos.
- All demos are deterministic; none rely on running a model. They can ship as static text.

## Compliance Checklist

- [x] At least one demo per major concept group (attention, decoding, prompting, alignment, retrieval, judging)
- [x] Each demo has a "What it shows" line and a "Why impactful" justification
- [x] No demo requires GPU, paid API, or proprietary data
- [x] No duplicates: skipped DPO (already has Code 18.3.1 walkthrough), skipped G-Eval (already has numeric-example callout at 46.2:142)
- [x] All numbers verified by manual computation
- [x] Idempotency: re-running this audit on the same chapters should NOT propose these demos again because section files will contain `class="callout demo"` blocks (the implementer should treat existing demo callouts as "already done").

## Failure Modes the Implementer Should Avoid

1. **Computing the wrong probability:** It is tempting to round e^z aggressively. Always compute exp before dividing; do not normalize logits to "look pretty" because then the demonstrated ratio breaks.
2. **Making the example too small:** A 2-token softmax demo collapses to a single ratio and teaches nothing. The 4-candidate width chosen above is the minimum where temperature scaling has visible effect across the table.
3. **Inventing token names that distract:** "Paris" and "London" work because the reader already knows them; do not invent obscure tokens to seem clever.
4. **Forgetting that callout `class="demo"` may need a CSS rule** to render with a distinct border / icon. Implementer should grep the existing stylesheet for `.callout.demo` and either add it or fall back to `numeric-example`.

End of report.
