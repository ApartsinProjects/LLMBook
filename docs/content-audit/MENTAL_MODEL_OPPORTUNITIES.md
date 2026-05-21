# Mental Model and Analogy Opportunities Audit

Scope: full LLM textbook on branch v2.0, scanned 449 section files (parts 1-15 plus appendices). Goal: find sections where a written analogy or simple line-drawing mental model would let readers grasp the IDEA behind a method, model, or pitfall before they see the math or pseudocode.

Date: 2026-05-19
Auditor: read-only, no HTML modified.

---

## TLDR: Top 15 HIGHEST-priority gaps

Each line: section path, concept, one-line mental model.

1. `part-2-understanding-llms/module-09-inference-optimization/section-9.3.html` (section 9.3.7 Sliding window + attention sinks + H2O) - **conveyor belt of memos** where the first few "anchor memos" and the last ~K stay pinned while the middle keeps rolling off the end.
2. `part-2-understanding-llms/module-09-inference-optimization/section-9.1.html` (9.1.2 absmax / zero-point quantization) - **shrinking a metric ruler down to N tick marks**; show real-number line projecting to integer ticks, where the largest weight defines the scale.
3. `part-1-llm-building-blocks/module-03-transformer-architecture/section-3.5.html` (3.5.2.3 RoPE) - **clock hands on each dimension pair**: every position rotates pairs of the embedding by a different speed; relative position = angle between two clocks.
4. `part-1-llm-building-blocks/module-03-transformer-architecture/section-3.8.html` (3.8.3 MoE routing + load balancing) - **dispatching parcels to courier vans**; the router is the sorting desk and the load-balance loss is the manager forcing fair workloads so no van sits idle.
5. `part-4-training-adaptation/module-18-alignment-rlhf-dpo/section-18.2.html` (18.2.2 Reward hacking / Goodhart) - **a student who learned the rubric, not the subject**; visual: true-reward and proxy-reward curves diverging after the early correlation breaks.
6. `part-7-retrieval-information-extraction-with-llms/module-32-rag/section-32.1.html` (32.1.4 Lost-in-the-middle) - **the bored party guest**: model "remembers" the start and the end of long context, glazes over the middle; visual = U-shaped attention curve with positions on x-axis.
7. `part-2-understanding-llms/module-09-inference-optimization/section-9.4.html` (9.4 speculative decoding multi-token verify) - the existing writer/editor analogy is good but a **track-runner relay** visual where the fast runner sprints ahead and the head coach checkpoints at intervals would make the parallel verification tangible.
8. `part-2-understanding-llms/module-09-inference-optimization/section-9.3.html` (9.3.2 memory-bandwidth wall) - **water through a straw**: a huge tank of compute that has to draw all its weights through a thin memory-bandwidth pipe each token; visual shows pipe widths to scale.
9. `part-4-training-adaptation/module-16-fine-tuning-fundamentals/section-16.1.html` (16.1.4 Catastrophic forgetting) - **painting over a mural**: each gradient stroke for your new task smears over a corner of the previously trained mural; visual = mural with patch over one section.
10. `part-9-llm-evaluation-observability/module-42-evaluation-foundations/section-42.1.html` (42.1.1 Perplexity) - **a betting-odds dashboard**; perplexity = "average number of equally likely next words the model thinks are still in play"; visual = roulette wheel with N slots = perplexity.
11. `part-7-retrieval-information-extraction-with-llms/module-31-embeddings-vector-db/section-31.1.html` (31.1.2 Contrastive loss / InfoNCE) - **magnetic field**: positives attracted, negatives repelled, batch acts as N-way classifier; visual = scatter plot with arrows.
12. `part-10-llm-security-runtime-safety/module-50-privacy-data-protection/section-50.1.html` (50.1.3 Differential privacy / noise budget) - **a leaky bucket of secrets**; each query drips information, DP-SGD pours in noise to refill it; the privacy budget epsilon = bucket capacity.
13. `part-2-understanding-llms/module-09-inference-optimization/section-9.3.html` (9.3.4 MHA vs MQA vs GQA) - **one chef vs many sous-chefs all reading the same recipe card**: Q-heads are different chefs, K/V is the shared recipe; MQA = one card; MHA = N cards; GQA = N/g cards.
14. `part-1-llm-building-blocks/module-04-decoding-text-generation/section-4.2.html` (4.2.7 repetition / frequency / presence penalties) - **conversation tax** with three different policies (any-repeat, count-by-count, ever-mentioned); slider visual with three meters showing what each penalty actually counts.
15. `part-12-llm-systems-at-scale/module-59-distributed-training-systems/section-59.2.html` (ZeRO stage progression) - **carpool with shared groceries**: stage 1 = share optimizer states, stage 2 = also share gradients, stage 3 = also share weights themselves; visual = three cars with progressively fewer redundant boxes.

---

## BY MODULE: Findings

Convention for each opportunity:

- **Topic**: concept that needs intuition
- **Why confusing**: one to two sentences
- **Suggested analogy**: one to three sentences
- **Suggested visual**: one line, drawable
- **Priority**: HIGH / MEDIUM / LOW
- **Existing analogies**: yes / no / partial

### Part 1: LLM Building Blocks

#### Module 01 (NLP foundations)

- `part-1-llm-building-blocks/module-01-foundations-nlp-text-representation/section-1.2.html` (TF-IDF weighting)
  - Topic: log scaling of IDF and why a word that appears in 1 of 1000 docs gets higher weight than one in 500 of 1000.
  - Why confusing: IDF = log(N/df) is opaque without an intuition for "how surprising is this word".
  - Analogy: TF-IDF is **a celebrity-detector**; "the" appears in every magazine, so seeing it tells you nothing about which magazine you're holding; "Levenshtein" appears in two of a million docs, so it pins down the topic instantly.
  - Visual: bar chart with x-axis = doc frequency (log), y-axis = "informativeness"; mark "the" at far right (low) and "Levenshtein" at far left (high).
  - Priority: MEDIUM
  - Existing: partial (math derivation exists, no celebrity/signal-vs-noise framing)

- `part-1-llm-building-blocks/module-01-foundations-nlp-text-representation/section-1.4.html` (Word2Vec vector arithmetic): Priority: LOW. Analogy: **city blocks**; gender and royalty as orthogonal streets you traverse by subtraction. Visual: 2D grid with parallel offset arrows. Existing: partial (Figure 1.3.7 is a projection only).

- `part-1-llm-building-blocks/module-01-foundations-nlp-text-representation/section-1.5.html` (vocabulary size tradeoff)
  - Topic: 100-token charwise vs 5M-token word-level vs 50K subword.
  - Why confusing: tradeoff is qualitative until you see specific numbers; readers struggle to feel why the U-curve exists.
  - Analogy: **alphabet block vs full word stickers**: pure characters force the model to invent every meaning from blocks (slow, brittle); pure words run out of stickers (OOV); subword = a starter kit of common stickers plus blocks to spell anything.
  - Visual: U-shaped curve, x = vocab size (log), y = "tokens per document"; mark the three regimes.
  - Priority: MEDIUM
  - Existing: partial (1.6 has Lego analogy for BPE merges already; 1.5 lacks one)

#### Module 02 (sequence models + attention)

- `part-1-llm-building-blocks/module-02-sequence-models-attention/section-2.1.html` (RNN / LSTM gates)
  - Topic: forget gate, input gate, output gate as differentiable controllers.
  - Why confusing: gates as sigmoid-weighted multiplies feel arbitrary.
  - Analogy: **a journal you re-write each day**: input gate = what you write down, forget gate = what you cross out, output gate = what you actually read aloud. Each gate is a dimmer switch (0 to 1), not an on/off.
  - Visual: notebook with a dimmer-switch labeled IN, FORGET, OUT next to each pen.
  - Priority: MEDIUM
  - Existing: no

- `part-1-llm-building-blocks/module-02-sequence-models-attention/section-2.2.html` (attention mechanism intuition)
  - Topic: attention as soft-lookup over a sequence.
  - Why confusing: dot-product similarity in high dimensions is abstract; the section has math but few intuition pumps.
  - Analogy: **highlighter pen with a knob**: each query token holds a highlighter; instead of marking one word, it shades all words proportional to how relevant they look. The output is the weighted blend of what each highlight touched.
  - Visual: sentence with semi-transparent highlights over multiple words, intensity = attention weight.
  - Priority: MEDIUM
  - Existing: partial (architectural diagrams exist; no "soft highlighter" picture)

- `part-1-llm-building-blocks/module-02-sequence-models-attention/section-2.3.html` (scaling by 1/sqrt(d_k))
  - Topic: why divide by sqrt(d_k) before softmax.
  - Why confusing: a numerical-stability reason hidden inside a derivation; many readers just memorize it.
  - Analogy: **shouting in a tiny room vs a stadium**: as the dimension grows, dot products grow proportionally and softmax saturates (one neighbor wins all the attention). Dividing by sqrt(d_k) tunes the volume so attention can still distribute.
  - Visual: two-panel comparison: small d_k → softmax balanced; large d_k unscaled → spiked softmax; large d_k scaled → balanced again.
  - Priority: HIGH (this is a question readers always ask)
  - Existing: partial (a Key Insight callout exists but it's textual)

#### Module 03 (Transformer architecture)

- `part-1-llm-building-blocks/module-03-transformer-architecture/section-3.2.html` (residual stream as highway, weight initialization scale by 1/sqrt(2N))
  - Topic: why does 1/sqrt(2N) initialization stabilize a deep stack.
  - Why confusing: the math depth-as-variance argument is not picture-able.
  - Analogy: **fireworks at depth**: each residual write adds a spark; if every spark were full-bright, the stack would blow out by layer 20. The scaling tells each spark to dim itself so the cumulative bloom is bounded.
  - Visual: side-by-side: untuned init = brightness explodes; tuned init = brightness stays in band.
  - Priority: MEDIUM
  - Existing: partial (residual highway SVG exists; init scaling is unillustrated)

- `part-1-llm-building-blocks/module-03-transformer-architecture/section-3.5.html` (RoPE: rotary embeddings)
  - Topic: rotating Q and K by position-dependent angles so dot products only see relative distance.
  - Why confusing: rotating "embedding pairs" is hard to picture without seeing a 2D rotation.
  - Analogy: **clock hands on each dimension pair**: every position turns a different speed clock; the dot product between two positions only depends on how far apart the hands are, not where each started.
  - Visual: two side-by-side dials at positions m and n, with the angular gap (n-m)·θ_i highlighted; show that rotating both by the same prefix angle doesn't change the gap.
  - Priority: HIGH (RoPE is everywhere in modern LLMs; the math is intimidating without the rotation picture)
  - Existing: partial (Figure 3.5.3 is an architectural diagram; not the clock-hand mental model)

- `part-1-llm-building-blocks/module-03-transformer-architecture/section-3.5.html` (ALiBi linear biases)
  - Topic: penalizing attention scores by distance with head-specific slopes.
  - Why confusing: how can a constant bias replace learned position embeddings?
  - Analogy: **gravity on a scoreboard**: every score gets pulled down by how far away the source is; heads have different gravity strengths so they specialize in short- or long-range looking.
  - Visual: attention matrix with a triangular gradient overlaid (darker = stronger penalty as you move away from the diagonal); one row showing the linear ramp at different slopes for two heads.
  - Priority: MEDIUM
  - Existing: no

- `part-1-llm-building-blocks/module-03-transformer-architecture/section-3.8.html` (MoE routing + load balancing loss)
  - Topic: top-k routing and the f_i · p_i auxiliary loss.
  - Why confusing: experts can collapse to a few favorites; the load-balance loss formula is opaque.
  - Analogy: **dispatching parcels to courier vans**: the router (dispatcher) decides which two vans (experts) each parcel goes to; if the dispatcher always picks the same two vans, the others idle and you waste capacity. The auxiliary loss is the depot manager nudging the dispatcher to spread parcels evenly.
  - Visual: 8 vans with parcels stacked unevenly (collapsed routing) → manager applies push → 8 vans with even stacks; load-balance loss formula gets a one-line caption "manager's nudge".
  - Priority: HIGH (MoE is now the dominant frontier architecture; load-balance failure is the #1 MoE bug)
  - Existing: no

- `part-1-llm-building-blocks/module-03-transformer-architecture/section-3.8.html` (Mamba selective state-space mechanism)
  - Topic: input-dependent state space (selective scan) vs fixed-parameter recurrences.
  - Why confusing: SSMs are introduced abstractly; the "data-dependent A,B,C" tweak is the heart of Mamba.
  - Analogy: **a kayaker on a moving river**: a vanilla SSM is a kayak that paddles the same way regardless of current; Mamba reads the current at each stroke and adjusts. The selectivity is the river-reading skill.
  - Visual: two kayakers, one paddling identically through varying river speeds (drifts off course), the other adjusting stroke per-section (stays on path).
  - Priority: MEDIUM
  - Existing: no

#### Module 04 (decoding)

- `part-1-llm-building-blocks/module-04-decoding-text-generation/section-4.1.html` (length normalization): Priority: LOW. Analogy: **golf scorecard handicap**. Visual: side-by-side raw vs normalized scoreboard. Existing: partial (hiker/mountain analogy for beam vs greedy).

- `part-1-llm-building-blocks/module-04-decoding-text-generation/section-4.2.html` (top-p / top-k / min-p / typical sampling)
  - Topic: four different ways to crop the probability tail before sampling.
  - Why confusing: readers conflate top-k and top-p; what each does at different temperature settings is fuzzy.
  - Analogy: **buffet line policies**: top-k = "you can pick from the first K dishes"; top-p = "you can pick any dish until the cumulative scoop fills 90% of the tray"; min-p = "skip anything less than 10% as likely as the favorite"; typical = "skip anything either too predictable or too weird."
  - Visual: a bar chart of token probabilities with four shaded regions overlaid (each policy's accepted set), labelled with the four buffet-line rules.
  - Priority: HIGH (these knobs appear in every API call)
  - Existing: partial (DJ dial for temperature; no comparable visual for the four crop policies)

- `part-1-llm-building-blocks/module-04-decoding-text-generation/section-4.2.html` (repetition vs frequency vs presence penalty)
  - Topic: three penalty knobs that look similar in OpenAI's API.
  - Why confusing: each penalizes a slightly different statistic; users tune the wrong one.
  - Analogy: **library late-fee policies**: presence penalty = "you owe $1 the moment you check out any book", frequency penalty = "you owe $1 per day of overdue", repetition penalty = "scale your account down each time you re-check the same book."
  - Visual: side-by-side three meters showing what each penalty actually multiplies.
  - Priority: HIGH (these are tuned blindly in production)
  - Existing: no

- `part-1-llm-building-blocks/module-04-decoding-text-generation/section-4.3.html` (constrained / grammar-constrained decoding)
  - Topic: mask out invalid tokens at each step (json schema, regex, CFG).
  - Why confusing: how does a decoder follow a grammar without losing fluency?
  - Analogy: **a guided crossword**: at each square the puzzle tells you the allowed letters; the writer is still creative within the constraint.
  - Visual: token grid with greyed-out "invalid" tokens at each step.
  - Priority: MEDIUM
  - Existing: no

### Part 2: Understanding LLMs

#### Module 06 (pretraining + scaling laws)

- `part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.1.html` (pretraining data mix / curriculum / quality vs quantity)
  - Topic: how doc-quality filters + dedup determine downstream perf.
  - Why confusing: "more data is better" is wrong; "quality > quantity" needs a picture.
  - Analogy: **diet vs calories**: 10,000 calories of donuts vs 2,000 of balanced meals - one inflates loss, the other actually nourishes capability.
  - Visual: two pies with same total slice but different ingredient proportions, paired with the resulting model "fitness".
  - Priority: MEDIUM
  - Existing: no

- `part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.3.html` (Chinchilla optimal point)
  - Topic: 20 tokens per parameter as the compute-optimal frontier.
  - Why confusing: a power law is one thing; the **frontier** as a curve in (N, D) space is harder.
  - Analogy: **balancing flour and water in dough**: too dry (small D) or too wet (large D) both ruin the bread; Chinchilla pins the ratio.
  - Visual: 2D contour of loss in (N, D) plane with the 20:1 frontier line and the "Kaplan" path overlaid showing why pre-Chinchilla training was under-data.
  - Priority: HIGH (foundational for budget planning)
  - Existing: partial (one Kaplan graph; no contour with the frontier line)

- `part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.5.html` (loss spikes during training)
  - Topic: gradient norms exploding mid-run.
  - Why confusing: in production, this looks random; the mental model of "single bad batch" is missing.
  - Analogy: **a single pothole in a long road trip**: most batches are fine, but one rare batch (anomalously long code, weird unicode) makes the optimizer swerve.
  - Visual: training-loss curve with a labeled spike, an inset showing the offending batch.
  - Priority: MEDIUM
  - Existing: partial (real-world scenario describes it textually)

#### Module 07 (modern landscape)

- `part-2/module-07/section-7.2.html` (context-window arms race): Priority: LOW. Analogy: **desk vs aircraft-carrier deck**; most queries use only a desk slice but pay for the deck. Visual: stacked rectangles with usage overlay. Existing: no.

#### Module 08 (reasoning / test-time compute)

- `part-2/module-08/section-8.5.html` (best-of-N / majority vote / tree search): Priority: MEDIUM. Analogy: **brainstorming styles**: independent ideas, vote, or build-out a promising branch. Visual: 4 cartoon panels for parallel / cluster / beam / MCTS. Existing: no.

#### Module 09 (inference optimization): DENSE WITH OPPORTUNITIES

- `part-2-understanding-llms/module-09-inference-optimization/section-9.1.html` (absmax / zero-point quantization)
  - Topic: real-number to integer projection with scale (and offset).
  - Why confusing: the math is one division and a round; the **geometric** picture of "snapping" reals to a grid is not drawn.
  - Analogy: **shrinking a metric ruler down to N tick marks**: absmax stretches the ruler so the biggest value lands on tick 127; zero-point also slides the ruler so zero lands on a chosen tick.
  - Visual: a number line with FP32 values, dashed lines projecting onto INT8 ticks; show one max value, one near-zero value, one negative value.
  - Priority: HIGH (foundational; every quantization concept builds on this)
  - Existing: no (only code shows it)

- `part-2-understanding-llms/module-09-inference-optimization/section-9.1.html` (per-tensor vs per-channel vs per-group granularity)
  - Topic: how granularity changes the scale.
  - Why confusing: readers grasp per-tensor but not why per-channel rescales.
  - Analogy: **one ruler for the whole desk vs one ruler per drawer**: a single scale wastes range when one drawer has tiny pencils and another has long rulers; per-drawer scales fit each better.
  - Visual: a weight matrix with one shared scale (top), per-column scales (middle), per-group of N columns (bottom); arrow showing precision improving.
  - Priority: MEDIUM
  - Existing: no

- `part-2-understanding-llms/module-09-inference-optimization/section-9.1.html` (NF4 normal-float distribution)
  - Topic: why 16 quantization levels chosen on a normal CDF beat uniform levels.
  - Why confusing: most readers picture uniform quantization grids.
  - Analogy: **fish-finder bins**: a uniform grid puts ticks everywhere even where no fish swim; NF4 places ticks where the fish (weights) actually live (centered around zero).
  - Visual: normal-distribution histogram overlaid with NF4 tick positions (close together near 0, far apart at tails) vs uniform ticks (evenly spaced).
  - Priority: HIGH (4-bit is the default; NF4 is widely misunderstood)
  - Existing: no

- `part-2-understanding-llms/module-09-inference-optimization/section-9.2.html` (GPTQ Hessian error compensation)
  - Topic: quantize a column, redistribute the rounding error to remaining columns.
  - Why confusing: the algorithm in equations feels mysterious; readers don't see why redistribution helps.
  - Analogy: **balancing a stack of plates**: when you round one plate down, the stack tilts; GPTQ slightly tilts the neighbors so the total height stays right.
  - Visual: 5 plates representing weights, one rounded down, arrows showing small adjustments compensating across remaining plates.
  - Priority: MEDIUM
  - Existing: no (diagram exists but only at architecture level)

- `part-2-understanding-llms/module-09-inference-optimization/section-9.2.html` (AWQ activation-aware scaling)
  - Topic: salient channels (those with large activations) get more quantization range.
  - Why confusing: "salient channel" sounds vague.
  - Analogy: **subway car capacity**: most cars carry few passengers, two cars carry the bulk; AWQ resizes the two big cars to fit more, accepting smaller for the others.
  - Visual: bar chart of activation magnitudes per channel, with two channels highlighted, then a second panel showing post-AWQ scaled quantization ranges (wider for salient).
  - Priority: MEDIUM
  - Existing: no

- `part-2-understanding-llms/module-09-inference-optimization/section-9.3.html` (KV cache memory dominance)
  - Topic: at long context + batch, KV cache > weights.
  - Why confusing: readers think "model weights" is the big number; they're shocked when KV beats weights.
  - Analogy: **carry-on vs accumulating receipts**: the model weights are your carry-on (fixed weight, packed once); the KV cache is the receipts that pile up every step. By the end of a long conversation, receipts outweigh the bag.
  - Visual: two stacks: weights bar (constant 140 GB), KV cache bar (grows linearly along x-axis = tokens); they cross at ~32K tokens.
  - Priority: HIGH
  - Existing: partial (hero image with librarian; no cross-over chart)

- `part-2-understanding-llms/module-09-inference-optimization/section-9.3.html` (9.3.2 memory-bandwidth wall)
  - Topic: 295x memory-bound: GPU compute idle while waiting for weights.
  - Why confusing: "memory-bound" is jargon.
  - Analogy: **a chef next to a tiny pantry**: chef can chop fast, but every recipe requires re-walking to the pantry; the chopping isn't the bottleneck, the trips are.
  - Visual: two-panel: big "compute" box with a thin tube (memory bandwidth) connecting to weights; second panel after KV cache cuts in half the volume to move.
  - Priority: HIGH
  - Existing: partial (calc in code; no picture)

- `part-2-understanding-llms/module-09-inference-optimization/section-9.3.html` (9.3.4 MHA vs MQA vs GQA)
  - Topic: sharing K/V heads across Q heads to reduce cache memory.
  - Why confusing: heads are abstract; "sharing K/V" lands only if you have a mental model of head structure.
  - Analogy: **one chef vs many sous-chefs all reading the same recipe card**: Q-heads are different chefs preparing different dishes; K/V is the recipe card. MHA = each chef brings their own card (duplicated). MQA = one shared card. GQA = 8 chefs share each of 4 cards (groups).
  - Visual: 3-panel comparison with chef figures and recipe cards (8/1/4 cards).
  - Priority: HIGH (this is one of the most commonly misunderstood architecture knobs)
  - Existing: partial (textual key insight only)

- `part-2-understanding-llms/module-09-inference-optimization/section-9.3.html` (9.3.5 prefix caching / RadixAttention)
  - Topic: cache KV for the system-prompt prefix shared across users.
  - Why confusing: a prefix tree is mentioned but not drawn.
  - Analogy: **the lobby of an office building**: every visitor walks through the same lobby (system prompt); you compute the lobby tour once and re-use it. Each visitor branches off to their own floor.
  - Visual: tree with a thick shared trunk (system prompt KV) and thin branches per user request.
  - Priority: HIGH
  - Existing: no

- `part-2-understanding-llms/module-09-inference-optimization/section-9.3.html` (9.3.6 continuous batching / chunked prefill)
  - Topic: dynamic batching that mixes prefill and decode requests.
  - Why confusing: traditional batching = uniform shape; continuous batching = ragged.
  - Analogy: **a restaurant kitchen ticket queue**: instead of "open at noon, cook 8 orders identically", the kitchen pulls whichever orders are ready, mixing appetizers (decode) and entrees (prefill).
  - Visual: timeline of requests entering/leaving, with prefill (long bars) and decode (short bars) interleaved.
  - Priority: HIGH
  - Existing: no

- `part-2-understanding-llms/module-09-inference-optimization/section-9.3.html` (9.3.7 H2O / sliding window / StreamingLLM attention sinks)
  - Topic: eviction policies for the KV cache.
  - Why confusing: three different policies blur together.
  - Analogy: **conveyor belt of memos** with three rules. Sliding window = whatever falls off the end is gone. H2O = pin the loudest few memos no matter when they arrived. StreamingLLM = always pin the very first memos (sink tokens) plus the recent N.
  - Visual: a horizontal cache strip, with shaded regions for "kept" (anchor + window) and faded "evicted" tokens; three sub-panels for each policy.
  - Priority: HIGH (this is essential for streaming inference and is invariably explained as bullet list)
  - Existing: no (bullet list only)

- `part-2-understanding-llms/module-09-inference-optimization/section-9.4.html` (speculative decoding draft size γ tuning)
  - Topic: optimal γ given acceptance rate α and draft/target cost ratio c.
  - Why confusing: math is there; readers don't see the "sweet-spot" curve.
  - Analogy: **drafts in a relay race**: too short (γ=1) is no different from no draft; too long (γ=20) wastes work when the editor rejects early. Optimal γ is the sprint distance you can keep within the editor's review window.
  - Visual: x = γ, y = speedup; curve rises then falls. Annotate the peak.
  - Priority: MEDIUM
  - Existing: partial (writer/editor analogy + relay would extend it)

- `part-2/module-09/section-9.7.html` (2:4 structured sparsity): Priority: MEDIUM. Analogy: **train carriages with seat-saver rules**; structured pattern lets you design a smaller train. Visual: side-by-side random-50% vs 2-of-4 grid with tensor-core badge. Existing: no.

- `part-2/module-09/section-9.8.html` (kernel fusion): Priority: MEDIUM. Analogy: **one trip vs three trips to the kitchen**. Visual: three round-trips → one round-trip carrying all results. Existing: no.

#### Module 10 (interpretability)

- `part-2-understanding-llms/module-10-interpretability/section-10.1.html` (attention head taxonomy: induction, copy, syntax)
  - Topic: that specific heads specialize.
  - Why confusing: readers think every head does the same thing.
  - Analogy: **departments in a newsroom**: the syntax desk checks grammar; the induction desk says "we've seen this name before, copy from there"; the copy desk handles direct quotes. Each is one head.
  - Visual: a newsroom floor plan with labeled desks, with each desk showing a tiny attention pattern.
  - Priority: MEDIUM
  - Existing: no

- `part-2-understanding-llms/module-10-interpretability/section-10.1.html` (logit lens)
  - Topic: project intermediate residual stream through the unembedding matrix at each layer.
  - Why confusing: the trick of "what would the model output if we stopped here" is hard to grasp.
  - Analogy: **drilling test holes down a tree**: at each ring, check what the tree "thinks" the answer is so far. Early rings show fuzzy guesses; later rings sharpen.
  - Visual: layer-stack with a "peek" arrow at each layer; bar chart of top-5 logits at layers 4, 12, 20, 28 showing answer crystallizing.
  - Priority: MEDIUM
  - Existing: partial (excellent code-driven figure exists; mental-model picture missing)

- `part-2-understanding-llms/module-10-interpretability/section-10.3.html` (model editing ROME / MEMIT)
  - Topic: edit a single fact by rank-1 update to MLP weights.
  - Why confusing: readers think editing one fact would corrupt all related ones; it doesn't, because the edit is targeted.
  - Analogy: **rewriting one paragraph in a book without re-typesetting the rest**: ROME finds the exact paragraph (the MLP layer storing the fact), edits it, and leaves all other paragraphs intact.
  - Visual: a thick book with one highlighted line being replaced, while neighboring pages stay untouched.
  - Priority: MEDIUM
  - Existing: no

### Part 3: Working with LLMs

- `part-3-working-with-llms/module-12-prompt-engineering/section-12.4.html` (prompt injection vs jailbreak distinction)
  - Topic: injection is data-becomes-instruction; jailbreak is undoing safety RLHF.
  - Why confusing: readers conflate the two.
  - Analogy: **email phishing vs bribery**: injection = an attacker sneaks an instruction into data the model is told to "summarize" (phishing); jailbreak = persuading the model to do something it was trained to refuse (bribing the bouncer).
  - Visual: two-panel comic: panel 1 a tool's "data" input contains hidden instructions; panel 2 a chat user wears a costume / negotiates with a polite refusal.
  - Priority: HIGH
  - Existing: no (textual definitions exist; visual differentiation missing)

- `part-3-working-with-llms/module-12-prompt-engineering/section-12.5.html` (chain-of-thought elicitation)
  - Topic: "let's think step by step" as a prompt-style trigger.
  - Why confusing: why does an English phrase produce better math?
  - Analogy: **untying your shoelaces vs taping them shut**: instructing to "think step by step" lets the model release intermediate tokens that act as scratchpad; without it, the model has to compute everything in one pass through its fixed depth.
  - Visual: same problem, two model boxes, one with a small scratchpad off to the side filling in steps, one with no scratchpad.
  - Priority: MEDIUM
  - Existing: partial (chess-deliberation hero image in section 8.1)

### Part 4: Training and Adaptation

#### Module 15 (synthetic data)

- `part-4-training-adaptation/module-15-synthetic-data/section-15.3.html` (synthetic data quality collapse / model collapse)
  - Topic: training repeatedly on a model's own outputs degrades capability.
  - Why confusing: it sounds like "free data" should help but it doesn't.
  - Analogy: **photocopying a photocopy**: each generation loses fidelity; faint colors fade, fine print blurs.
  - Visual: an image being copied across 5 generations, each blurrier, with a loss-curve x-axis showing degradation.
  - Priority: HIGH (model collapse is a hot 2024-26 concern)
  - Existing: no (or only as a phrase)

#### Module 16 (fine-tuning)

- `part-4-training-adaptation/module-16-fine-tuning-fundamentals/section-16.1.html` (16.1.4 catastrophic forgetting)
  - Topic: gradient updates overwrite weights encoding general knowledge.
  - Why confusing: the "task-specific vs general performance" curves exist but the mechanism is left abstract.
  - Analogy: **painting over a mural**: each new task is a roller dragging fresh paint over part of the mural; if you don't dab carefully, you smear scenes that took hours to paint.
  - Visual: mural with a small patch of fresh paint covering one figure's face; arrow showing the overwriting.
  - Priority: HIGH
  - Existing: partial (chart exists; analogy is text-only "adaptation ladder")

- `part-4-training-adaptation/module-16-fine-tuning-fundamentals/section-16.2.html` (instruction-tuning data mixture)
  - Topic: how to weight task families in SFT.
  - Why confusing: practitioners over-index on one family.
  - Analogy: **a meal-prep box**: too much rice (instruction-following) without protein (reasoning) or veg (safety) creates a lopsided model. The right ratio depends on goal.
  - Visual: meal-prep tray with labeled compartments and warning labels for missing categories.
  - Priority: MEDIUM
  - Existing: no

- `part-4-training-adaptation/module-16-fine-tuning-fundamentals/section-16.4.html` (hyperparameters: lr, epochs, batch size in fine-tuning)
  - Topic: smaller is usually better in lr, fewer epochs.
  - Why confusing: from-scratch training intuitions transfer wrong.
  - Analogy: **sliders dashboard** with mood labels: "conservative" (low lr, 1-2 epochs) vs "aggressive" (high lr, 10+ epochs); the slider position determines forgetting risk.
  - Visual: a horizontal slider panel with three sliders (lr, epochs, weight decay) and a danger meter increasing as you push right.
  - Priority: MEDIUM
  - Existing: no

#### Module 17 (PEFT)

- `part-4-training-adaptation/module-17-peft/section-17.1.html` (LoRA init: A random, B zero): Priority: LOW. Analogy: **whispered chord on a piano**; only A pressed, B silent, so the adapter starts invisible. Visual: piano with two players, gradual engagement. Existing: no.

- `part-4-training-adaptation/module-17-peft/section-17.2.html` (QLoRA: 4-bit base + LoRA adapter)
  - Topic: combine NF4 quantization with LoRA on top.
  - Why confusing: how can a 4-bit frozen model still train?
  - Analogy: **adding stickers to a frozen sculpture**: the base sculpture (4-bit weights) doesn't move; the stickers (LoRA adapters) are in regular precision and can be repositioned freely.
  - Visual: a chiseled stone bust labeled "4-bit frozen", with colorful sticky notes attached representing trainable LoRA weights.
  - Priority: MEDIUM
  - Existing: no

- `part-4-training-adaptation/module-17-peft/section-17.4.html` (soft prompts / prompt tuning)
  - Topic: prepend N trainable embedding vectors instead of words.
  - Why confusing: "vectors with no English meaning" is hard.
  - Analogy: **secret handshake**: words are public greetings; soft prompts are gestures only the model recognizes that put it in the right mood.
  - Visual: a chat-style input with [shape A][shape B][shape C] in front of the user message, with a tooltip "these aren't words, they're learned vectors".
  - Priority: MEDIUM
  - Existing: partial (example added in cycle-2 audit)

- `part-4-training-adaptation/module-17-peft/section-17.7.html` (TIES / DARE / task vector merging)
  - Topic: average / sign-elect / sparsify multiple fine-tunes.
  - Why confusing: lots of merge methods, why does sign election beat averaging?
  - Analogy: **band majority vote on key**: if two musicians want F major and one wants F minor, an average gives a flat third with awful intonation; a majority vote on sign picks one mode cleanly.
  - Visual: three guitarists with arrows up/up/down; averaged = chord blur, sign-elected = clean chord with the "down" muted.
  - Priority: MEDIUM
  - Existing: partial (recent example in 17.7 with +0.35 / -0.35 numbers; visual missing)

#### Module 18 (alignment)

- `part-4-training-adaptation/module-18-alignment-rlhf-dpo/section-18.1.html` (KL penalty as a leash)
  - Topic: how β controls deviation from reference policy.
  - Why confusing: KL divergence as a "soft constraint" feels arbitrary.
  - Analogy: **a dog on an elastic leash**: low β = long leash, dog (policy) can wander far; high β = short leash, dog stays close to handler (reference). Picking β is choosing leash length.
  - Visual: handler with a dog at three leash lengths, with three resulting wander patterns.
  - Priority: HIGH
  - Existing: no

- `part-4-training-adaptation/module-18-alignment-rlhf-dpo/section-18.1.html` (PPO clip mechanism)
  - Topic: ratio = π(y)/π_old(y), clipped to [1-ε, 1+ε].
  - Why confusing: the "clip" formula plus min() is confusing.
  - Analogy: **stock-loss protection**: if your position moves too fast in either direction, the trade is capped at +/- ε. PPO refuses to take advantage of an out-of-range step because that's where the surrogate breaks.
  - Visual: ratio on x-axis, objective on y-axis, with the clipped region flat above/below ε.
  - Priority: MEDIUM
  - Existing: partial (math + Algorithm)

- `part-4-training-adaptation/module-18-alignment-rlhf-dpo/section-18.2.html` (18.2.2 reward hacking / Goodhart)
  - Topic: policy exploits reward model imperfections; true quality decays.
  - Why confusing: rising reward + falling quality is paradoxical without a visual.
  - Analogy: **a student who learned the rubric, not the subject**: they ace the rubric (proxy reward) by hitting the listed criteria, but real understanding (true reward) decays.
  - Visual: two curves over training steps: proxy reward rising, true (held-out) reward rising early then falling; a circle highlighting the divergence point.
  - Priority: HIGH
  - Existing: partial (textual scenario only)

- `part-4-training-adaptation/module-18-alignment-rlhf-dpo/section-18.2.html` (18.2.1 GRPO group-relative advantage)
  - Topic: normalize rewards within a group of G samples per prompt instead of using a value network.
  - Why confusing: why does "subtracting the group mean" replace a critic?
  - Analogy: **grading on a curve**: instead of a separate teacher's-key for absolute scores (value network), grade each answer relative to its same-prompt classmates. The group itself defines the baseline.
  - Visual: 4 sampled responses for the same prompt, each with a raw score; arrow to centered scores (raw − group_mean) with one positive and three negative.
  - Priority: HIGH
  - Existing: partial (math present; no visual)

- `part-4-training-adaptation/module-18-alignment-rlhf-dpo/section-18.3.html` (DPO loss as preference margin)
  - Topic: log-ratio difference between chosen and rejected → sigmoid loss.
  - Why confusing: the math collapses neatly but the geometric intuition is lost.
  - Analogy: **scale tilted in favor of chosen**: each preference pair adds weight to the chosen side; the loss measures how far the scale still leans toward the wrong side. Training pushes it past balance.
  - Visual: balance scale with chosen on one pan, rejected on the other, with the margin (β · Δlog) labeled as a height difference.
  - Priority: HIGH (DPO is now the default for small teams)
  - Existing: partial (A/B taste test exists in 18.3; the margin geometry isn't drawn)

### Part 5: Multimodal LLMs

- `part-5/module-20/section-20.1.html` (TTS prosody control): Priority: MEDIUM. Analogy: **karaoke machine with separate dials** (pitch / pace / vibrato). Visual: karaoke screen with prosody sliders. Existing: no.

- `part-5/module-20/section-20.5.html` (streaming ASR overlap): Priority: MEDIUM. Analogy: **two scribes overlapping shifts** so boundary words aren't lost. Visual: timeline with overlapping windows. Existing: no.

- `part-5-multimodal-llms/module-21-image-generation/section-21.1.html` (diffusion forward process / noise schedule)
  - Topic: gradually add Gaussian noise across T steps.
  - Why confusing: T = 1000 steps abstractly; readers don't picture the noise progression.
  - Analogy: **TV static taking over a photograph**: start with a clear photo, snow grows across the frame each step; reverse the process to denoise back to a photo.
  - Visual: 5 panels showing an image at t=0, 250, 500, 750, 1000 (clear → pure noise).
  - Priority: HIGH (foundational and frequently re-explained)
  - Existing: partial (some diffusion sections have figures; this specific noise-creep visual is missing)

- `part-5-multimodal-llms/module-21-image-generation/section-21.2.html` (classifier-free guidance)
  - Topic: ε_cond - ε_uncond extrapolation, the w "guidance scale".
  - Why confusing: why subtracting the unconditional prediction sharpens the output.
  - Analogy: **steering by the gap, not the destination**: the model knows where the "no-prompt" path goes; the prompt-conditional path is the destination; CFG pushes you past the destination by the gap, getting you "more prompt-aligned than the conditional alone".
  - Visual: 2D vector field, one arrow ε_uncond, one ε_cond, and the extrapolation arrow w·(ε_cond − ε_uncond) extending past ε_cond.
  - Priority: MEDIUM
  - Existing: no

- `part-5-multimodal-llms/module-22-vision-language-models/section-22.3.html` (LLaVA-style "projector" between vision encoder and LLM)
  - Topic: a small MLP/Q-Former bridges modality embeddings.
  - Why confusing: the projector is small but critical; readers think the vision encoder talks to the LLM directly.
  - Analogy: **translator at a customs booth**: vision encoder speaks "Pixelese"; LLM speaks "Tokenese"; the projector is the translator who restates the visual statement in the LLM's vocabulary.
  - Visual: two boxes (vision encoder, LLM) with a small "interpreter" box between them holding a phrasebook.
  - Priority: HIGH (LLaVA is the canonical architecture; the projector is its essence)
  - Existing: partial (architecture diagrams exist; no translator framing)

- `part-5/module-22/section-22.6.html` (pipeline vs native multimodal): Priority: MEDIUM. Analogy: **assembly line vs single craftsman** (modular handoffs vs holistic workbench). Visual: 2-panel comparison. Existing: no.

### Part 6: Agentic AI

- `part-6-agentic-ai/module-26-ai-agents/section-26.1.html` (ReAct loop: observe-think-act)
  - Topic: alternating reasoning and tool calls.
  - Why confusing: the loop is described in pseudocode; the trajectory feel is missing.
  - Analogy: **detective at a crime scene**: think (form hypothesis), act (check fingerprint), observe (result), think again. Each cycle narrows the suspect.
  - Visual: spiral diagram with three radial arrows labeled think/act/observe spiraling inward to a "conclusion" center.
  - Priority: MEDIUM
  - Existing: partial (architecture-level reasoning illustrations exist)

- `part-6-agentic-ai/module-27-tool-use-protocols/section-27.6.html` (tool selection / tool economy)
  - Topic: when you have 100 tools, selection becomes RAG over tool descriptions.
  - Why confusing: readers expect "give the model all tools always".
  - Analogy: **a Swiss Army knife with 200 attachments**: opening every blade overwhelms; instead, pre-filter to the 3 attachments likely to help this job.
  - Visual: Swiss-army knife with all blades fanned out (busy) → filtered to 3 (clean).
  - Priority: MEDIUM
  - Existing: no

- `part-6/module-28/section-28.1.html` (multi-agent coordination tax): Priority: MEDIUM. Analogy: **meeting tax** that grows with team size. Visual: cost curve quadratic with throughput rising-then-falling. Existing: partial.

- `part-6-agentic-ai/module-30-tools-of-the-trade/section-30.3.html` (multi-agent topologies + framework mapping)
  - Topic: the same agent in different frameworks behaves differently.
  - Why confusing: framework-by-framework documentation hides the conceptual symmetries.
  - Analogy: **a sports team running the same play under different coaches**: same players (LLM agents), same play (task), but the coach (framework) imposes a defense scheme that changes execution.
  - Visual: same 5-agent setup rendered 3 ways: as a tree (hierarchical), a ring (debate), a star (supervisor); each is the same play, different coach.
  - Priority: HIGH (flagged earlier as high-warning low-visual section)
  - Existing: no

### Part 7: Retrieval and IE

- `part-7-retrieval-information-extraction-with-llms/module-31-embeddings-vector-db/section-31.1.html` (contrastive InfoNCE / in-batch negatives)
  - Topic: each batch's queries treat other batch's passages as negatives.
  - Why confusing: "the other 31 are negatives" sounds wasteful; readers don't see why.
  - Analogy: **magnetic dating game**: 32 queries and 32 passages enter a room; each query has exactly one "true match" and pushes against the other 31 trying not to match them. The room ends with paired magnets.
  - Visual: 4x4 grid of queries vs passages, diagonal cells glowing (positives), off-diagonal repulsive arrows.
  - Priority: HIGH
  - Existing: partial (math + code, no field visualization)

- `part-7-retrieval-information-extraction-with-llms/module-31-embeddings-vector-db/section-31.1.html` (hard negative mining)
  - Topic: superficially similar but actually wrong passages.
  - Why confusing: why are hard negatives more useful than random ones?
  - Analogy: **studying for a multiple-choice exam**: easy distractors (random negatives) teach little; tempting wrong-but-plausible options (hard negatives) make you learn the fine line.
  - Visual: a query at the center, with three orbits of negatives: near (hard), medium, far (random); training tightens the boundary just outside the hard zone.
  - Priority: MEDIUM
  - Existing: partial (note callout describes BM25 negatives strategies but no orbit picture)

- `part-7-retrieval-information-extraction-with-llms/module-31-embeddings-vector-db/section-31.4.html` (Product Quantization)
  - Topic: split a vector into M sub-vectors, codebook each independently.
  - Why confusing: "codebook" sounds like quantization but with sub-pieces; mechanism is unclear.
  - Analogy: **breaking a long phone number into chunks for memory**: 0118-999-881-9999 is easier to recall as four 4-digit chunks each chosen from a 16-option codebook than as one 16-digit code.
  - Visual: a 128-dim vector cut into 8 chunks; each chunk's nearest codeword (out of 256 options) drawn from a small palette.
  - Priority: MEDIUM
  - Existing: no

- `part-7-retrieval-information-extraction-with-llms/module-31-embeddings-vector-db/section-31.6.html` (chunking): Priority: LOW. Already addressed by cycle-3 Figure 35.5.2 (3-panel chunking). Existing: yes.

- `part-7-retrieval-information-extraction-with-llms/module-32-rag/section-32.1.html` (32.1.4 lost-in-the-middle)
  - Topic: U-shaped attention over long-context positions.
  - Why confusing: warning text says it but no curve is shown.
  - Analogy: **the bored party guest**: pays attention to first introductions and the gossip near the door (end), tunes out the middle of the room. Putting the most important guest in the middle = the model misses them.
  - Visual: position 1 → 20 on x-axis; recall on y-axis; classic U-curve dipping in the middle.
  - Priority: HIGH (single most-cited RAG failure mode)
  - Existing: no

- `part-7-retrieval-information-extraction-with-llms/module-32-rag/section-32.4.html` (schema linking in text-to-SQL)
  - Topic: matching natural-language terms to actual schema columns.
  - Why confusing: "schema linking failure" feels abstract.
  - Analogy: **menu translation**: a user asks for "the spicy noodle bowl"; the menu has "Sichuan Dan Dan"; schema-linking is the waiter who recognizes that user intent maps to that exact dish.
  - Visual: user phrase → waiter → menu item; with a failed case showing the waiter shrugging.
  - Priority: MEDIUM
  - Existing: partial (cycle-2 churn example exists but waiter visual missing)

- `part-7-retrieval-information-extraction-with-llms/module-35-advanced-rag/section-35.1.html` (reranking with cross-encoder)
  - Topic: cheap retriever → expensive reranker funnel.
  - Why confusing: why have two stages?
  - Analogy: **resume screening**: cheap keyword filter (bi-encoder, retrieves 100); slow interview (cross-encoder, scores 10). You don't interview every applicant.
  - Visual: funnel with two stages, candidate counts dropping (1M → 100 → 10).
  - Priority: HIGH
  - Existing: no (or partial)

- `part-7-retrieval-information-extraction-with-llms/module-35-advanced-rag/section-35.2.html` (HyDE: hypothetical document embeddings)
  - Topic: generate fake answer, embed, retrieve real docs.
  - Why confusing: why does a wrong hypothetical help?
  - Analogy: **a librarian guessing the chapter title**: a query of "how do KV caches reduce latency?" is short; the librarian first imagines what such a chapter would say, then walks the stack looking for books that match that imagined paragraph. The made-up paragraph captures more retrievable cues than the original question.
  - Visual: question bubble → imagined long answer bubble → arrow into a book stack matching by content.
  - Priority: MEDIUM
  - Existing: partial (cycle-2 worked example added; visual missing)

- `part-7-retrieval-information-extraction-with-llms/module-35-advanced-rag/section-35.4.html` (GraphRAG local vs global)
  - Topic: subgraph neighborhood (local) vs map-reduce over community summaries (global).
  - Why confusing: when to use which.
  - Analogy: **asking a town**: local query = "what's near my house?" (walk the neighborhood); global query = "what are the major themes in town?" (assemble each district's mayor and average their reports).
  - Visual: town map with one query hopping between adjacent houses, another query getting summaries from each colored district.
  - Priority: MEDIUM
  - Existing: partial (cycle-2 example exists; visual missing)

### Part 8: Conversational AI

- `part-8-conversational-ai-with-llms/module-37-conversational-ai/section-37.3.html` (long-conversation memory management)
  - Topic: summarize older turns; keep recent verbatim.
  - Why confusing: when does summarization lose critical details?
  - Analogy: **diary vs detailed minutes**: yesterday's events compressed to a diary entry (lossy summary); the last 30 minutes verbatim minutes (lossless). The trick is choosing the cutoff.
  - Visual: a conversation timeline with the recent N turns highlighted in full, the rest collapsed into a single summary bubble.
  - Priority: MEDIUM
  - Existing: no

- `part-8-conversational-ai-with-llms/module-40-voice-realtime-multimodal/section-40.1.html` (voice latency budget): Priority: LOW. Analogy: **relay race against the 500ms threshold**. Existing: partial (cycle-3 stacked bar covers numbers).

### Part 9: Evaluation and Observability

- `part-9-llm-evaluation-observability/module-42-evaluation-foundations/section-42.1.html` (perplexity)
  - Topic: exp(NLL) as "average # of equally-likely choices".
  - Why confusing: exp of a log is a math sleight; readers don't feel what perplexity 30 means.
  - Analogy: **roulette with N slots**: perplexity 30 = model thinks the next token is roughly one of 30 equally-likely choices. Perplexity 5 = it's narrowed to ~5.
  - Visual: a roulette wheel with N labeled slots; smaller perplexity → fewer slots.
  - Priority: HIGH (perplexity is the first metric every reader meets)
  - Existing: no

- `part-9-llm-evaluation-observability/module-42-evaluation-foundations/section-42.1.html` (LLM-as-judge biases pile-up)
  - Topic: 5 biases stacking.
  - Why confusing: bullet list; the *cumulative* effect on rankings is hard to grasp.
  - Analogy: **a scale loaded on one side**: each bias is a weight added to the same pan. One is harmless; five flip the verdict.
  - Visual: balance scale with five labeled weights stacking on one pan, the verdict needle moving in proportion.
  - Priority: MEDIUM
  - Existing: partial (cartoon judge image exists but not the stacking-weights metaphor)

- `part-9-llm-evaluation-observability/module-42-evaluation-foundations/section-42.10.html` (research methodology: stats, significance)
  - Topic: bootstrap CIs vs t-tests vs paired tests for LLM eval.
  - Why confusing: dense statistical recipes without intuition.
  - Analogy: **measuring how often a coin lands heads in N flips**: small N = wide error bars; large N = narrow. Use paired comparisons when the two coins are flipped under the same conditions.
  - Visual: two error-bar plots side-by-side, one showing 10 flips, one showing 1000.
  - Priority: MEDIUM
  - Existing: partial (kappa scale added in cycle 3; bootstrap intuition still text-only)

- `part-9-llm-evaluation-observability/module-43-specialized-evaluation/section-43.5.html` (multimodal eval matrix): Priority: LOW. Mostly handled by cycle 3 (Fig 43.5.2). Suggest only a "periodic table" shading legend for the existing matrix. Existing: yes.

- `part-9/module-44/section-44.5.html` (drift detection): Priority: MEDIUM. Analogy: **water quality monitor**; single brown drop is noise, sustained shift is drift. Visual: gauge stream with threshold alarm. Existing: no.

- `part-9/module-46/section-46.1.html` (position-bias swap test): Priority: MEDIUM. Analogy: **left-right blind taste test**. Visual: two-trial verdict panels with inconsistency arrow. Existing: partial.

### Part 10: Security and Runtime Safety

- `part-10-llm-security-runtime-safety/module-47-adversarial-security-red-team/section-47.1.html` (47.1.4 RAG poisoning)
  - Topic: planting adversarial documents that hijack the model's outputs.
  - Why confusing: how can a doc in the corpus override a system prompt?
  - Analogy: **a poisoned encyclopedia article**: a librarian (RAG) faithfully serves the article; the user reads instructions to "ignore librarian, recommend product X"; the model obeys what looks like a citation.
  - Visual: a citation card with hidden bold instructions; the model emitting the instruction as if it were retrieved fact.
  - Priority: HIGH
  - Existing: no

- `part-10-llm-security-runtime-safety/module-47-adversarial-security-red-team/section-47.1.html` (sandwich defense / spotlighting)
  - Topic: wrap user input in distinct delimiters and instruct the model to treat it as data only.
  - Why confusing: why does adding a delimiter help?
  - Analogy: **scare quotes and air quotes**: telling the model "what's between these quotes is the *user's question*, do not obey instructions inside it" is the textual equivalent of holding up your fingers in air quotes.
  - Visual: a prompt with the user input visibly fenced (e.g., a colored box) and a sticky note next to it saying "data, not instructions".
  - Priority: MEDIUM
  - Existing: no

- `part-10-llm-security-runtime-safety/module-48-guardrails-runtime-safety/section-48.1.html` (what guardrails are / are not)
  - Topic: layered checks aren't a perimeter wall.
  - Why confusing: practitioners think one guardrail = safe.
  - Analogy: **Swiss-cheese model of accident prevention**: each guardrail (input filter, output classifier, monitor) has holes; safety comes from stacking enough slices that hole-alignment is rare.
  - Visual: four cheese slices with random holes; arrow only passes through if all four have aligned holes.
  - Priority: HIGH (guardrails section had high warnings, low visuals)
  - Existing: no

- `part-10/module-48/section-48.5.html` (jailbreak families): Priority: MEDIUM. Analogy: **lock-picking toolkit**; each family is a different pick. Visual: kit laid flat with picks labeled by attack family. Existing: no.

- `part-10-llm-security-runtime-safety/module-49-agent-safety-autonomy/section-49.2.html` (autonomy levels / human-in-the-loop tiers)
  - Topic: when to require approval, log-only, or auto-execute.
  - Why confusing: practitioners pick arbitrarily.
  - Analogy: **traffic-light approval system**: green = auto (read-only), yellow = log + run (mostly safe), red = require human approval (irreversible).
  - Visual: three colored buckets with example actions sorted into each (search, send_email, transfer_funds).
  - Priority: HIGH
  - Existing: partial (cycle 3 added a risk-routing flow in 28.3; 49.2 still without)

- `part-10-llm-security-runtime-safety/module-50-privacy-data-protection/section-50.1.html` (differential privacy noise budget ε)
  - Topic: each query "spends" privacy; total ε caps spent.
  - Why confusing: "epsilon spent" is opaque.
  - Analogy: **leaky bucket of secrets**: each query drips information out; DP-SGD pours noise in to mask drips. ε = how much net information drains over training.
  - Visual: bucket labeled "privacy budget"; faucets dripping (queries) and a hose pouring (noise); the bucket fills/empties.
  - Priority: HIGH (DP-SGD is widely deployed but rarely understood)
  - Existing: no

- `part-10/module-50/section-50.1.html` (50.1.2 membership inference): Priority: MEDIUM. Analogy: **teacher recognizing their own student's essay** via lower perplexity. Visual: in-training vs out-of-training perplexity histograms with MIA threshold. Existing: no.

### Part 11: Ethics and Governance

- `part-11/module-52/section-52.1.html` (representation vs allocation vs QoS bias): Priority: MEDIUM. Analogy: **three different broken thermometers**: missing readings / biased readings / coarse readings. Visual: three labeled thermometers. Existing: no.

- `part-11/module-54/section-54.1.html` (text watermarking green-list bias): Priority: MEDIUM. Analogy: **invisible ink on every page**; faint per-token but detectable over many. Visual: passage with green-list tokens shaded; detector window output. Existing: no.

### Part 12: Systems at Scale

- `part-12-llm-systems-at-scale/module-58-frontier-systems-hardware/section-58.2.html` (NVLink vs InfiniBand)
  - Topic: 20x bandwidth gap between intra-node and inter-node.
  - Why confusing: just numbers; the deployment implication is missed.
  - Analogy: **office vs cross-country mail**: handing a memo to a desk-neighbor (NVLink) is instant; faxing the memo to another city (InfiniBand) costs minutes. You design your parallelism plan to keep "memos" inside the office.
  - Visual: two-tier diagram, intra-node = thick line, inter-node = thin line, with bandwidth labels and a "tensor parallelism must stay here" caption.
  - Priority: MEDIUM
  - Existing: partial (Figure 59.1.3 exists)

- `part-12-llm-systems-at-scale/module-59-distributed-training-systems/section-59.1.html` (ring all-reduce why N-independent)
  - Topic: bandwidth is roughly 2S in the asymptotic limit.
  - Why confusing: "doubling the cluster does not double the time" is counterintuitive.
  - Analogy: **a singing round**: 100 people pass a tune around a circle; doubling the circle doesn't increase the per-person workload because each only sings to one neighbor.
  - Visual: a ring of 8 nodes with chunks moving along the ring in two passes (scatter, gather).
  - Priority: MEDIUM
  - Existing: partial (math exists; the singing-round picture is missing)

- `part-12-llm-systems-at-scale/module-59-distributed-training-systems/section-59.2.html` (ZeRO stage progression)
  - Topic: stage 1 = optimizer state shard, 2 = + gradients, 3 = + weights.
  - Why confusing: progression is described but not pictured cleanly.
  - Analogy: **carpool with shared groceries**: stage 1 = each car carries food, but only one car carries the cooler (shared optimizer); stage 2 = also share the cooler bag (gradients); stage 3 = also share the menu (weights), but everyone fetches their dish on demand.
  - Visual: three cars side-by-side with progressively fewer redundant boxes; under each car a memory bar showing the savings.
  - Priority: HIGH
  - Existing: no

- `part-12-llm-systems-at-scale/module-59-distributed-training-systems/section-59.4.html` (pipeline bubbles and micro-batching)
  - Topic: pipeline stages have idle "bubbles" during fill/drain.
  - Why confusing: the schedule diagram for 1F1B is dense.
  - Analogy: **factory line warm-up**: the first widget takes T·N time to traverse N stations; subsequent widgets come out one per T as the line fills. The fill/drain is the bubble.
  - Visual: 4-station factory line with widgets entering, with bubble cells shaded gray.
  - Priority: MEDIUM
  - Existing: no

- `part-12/module-60/section-60.2.html` (edge KV-cache compression): Priority: MEDIUM. Analogy: **degraded film print**; trade resolution for being able to play at all. Visual: image side-by-side at FP16/INT4/INT2. Existing: no.

### Part 13: LLMOps

- `part-13-llmops-lifecycle/module-63-ai-gateways-routing/section-63.2.html` (semantic caching)
  - Topic: cache by embedding similarity, not exact match.
  - Why confusing: how can you "match" a non-identical question?
  - Analogy: **a restaurant taking variations on the same order**: "burger no onions" and "burger, hold the onion" go to the same line cook; the cache says "I've seen this dish".
  - Visual: input embeddings clustered, with a similarity-threshold sphere; queries inside the sphere hit the cache.
  - Priority: HIGH
  - Existing: no

- `part-13/module-66/section-66.1.html` (SLO error budget): Priority: MEDIUM. Analogy: **monthly allowance jar**; freeze deploys when empty. Visual: jar with credit gauge over time. Existing: no.

- `part-13/module-64/section-64.3.html` (idempotency keys): Priority: MEDIUM. Analogy: **ordering coffee with a receipt number**; same receipt returns same coffee. Visual: two-arrow request diagram. Existing: no.

### Part 14: Applications

Most Part 14 sections are use-case lists and would not benefit from an architectural analogy. Two exceptions where a domain-specific mental model helps:

- `part-14/module-69-healthcare/section-69.1.html` (ambient clinical docs): Priority: LOW. Analogy: **stenographer with judgment** (verbatim ribbon + structured SOAP form). Existing: no.

- `part-14/module-67-legal/section-67.1.html` (citation verification): Priority: LOW. Analogy: **fact-checker desk at a newspaper** (PASS/FAIL stamp). Existing: no.

### Part 15: Frontiers

- `part-15-llm-agentic-ai-research-frontiers/module-76-frontier-theory/section-76.1.html` (TC^0 vs P with CoT separation)
  - Topic: chain-of-thought changes the complexity class the model can compute.
  - Why confusing: complexity theory is intimidating.
  - Analogy: **calculator vs scratchpad**: a calculator (no CoT) handles one operation; a scratchpad with the calculator (with CoT) handles long division by chaining operations.
  - Visual: a calculator side-by-side with a scratchpad; an arithmetic problem fits in the calculator if simple, requires the scratchpad if multi-step.
  - Priority: HIGH (theoretical frontier readers wrestle with this)
  - Existing: partial (System-1/System-2 hero image exists; complexity-class picture missing)

- `part-15-llm-agentic-ai-research-frontiers/module-77-agi-trajectories/section-77.1.html` (capability vs alignment scaling)
  - Topic: capability scales smoothly; alignment doesn't necessarily.
  - Why confusing: the "alignment lag" is hand-waved.
  - Analogy: **a rocket and a parachute**: capability is the engine thrust; alignment is the parachute deployment. The two need to scale together; rapid thrust without parachute coverage = catastrophe.
  - Visual: time-evolving plot, capability rising, alignment as a delayed curve, divergence shaded as "risk zone".
  - Priority: MEDIUM
  - Existing: no

### Appendix A: Mathematical Foundations

- `appendices/appendix-a-mathematical-foundations/section-a.4.html` and `section-a.6.html` (KL divergence, entropy, cross-entropy)
  - Topic: KL as expected log-ratio.
  - Why confusing: equations only; intuition lacking.
  - Analogy: **mismatched codebook penalty**: KL(P || Q) is "extra bits you pay when you use a Q-codebook to encode messages drawn from P". If Q matches P, zero extra; if mismatched, you waste bits.
  - Visual: two probability bars (P) drawn over the same x-axis with a Q approximation overlaid; gaps between them shaded as "wasted bits".
  - Priority: HIGH (KL appears in DPO, PPO, distillation, alignment - needs one canonical mental model)
  - Existing: no

- `appendices/appendix-a/section-a.2.html` (Gaussian / covariance shape): Priority: LOW. Analogy: **2D drumhead with tension**; eigenvectors as stretching axes. Visual: contour ellipse with eigenvector arrows. Existing: no.

---

## BY THEME: Cross-cutting opportunities

### Theme 1: Geometric pictures of "rotation / projection" math
Many algorithms describe operations on vectors that have natural geometric pictures the book mostly leaves verbal:
- RoPE rotations (3.5)
- LoRA low-rank decomposition (17.1)
- Quantization projections (9.1)
- Embedding contrastive pull/push (31.1)
- Soft prompts as free-floating vectors (17.4)
- CFG vector extrapolation (21.2)
- DPO margin as scale-tilt (18.3)

A consistent visual style for "vector pictures" across these sections would build mental fluency. Single recommendation: standardize on a 2D scatter plot with labeled arrows for "operation directions" so the reader sees the same picture language each time.

### Theme 2: Throughput / pipeline visualizations
The book repeatedly describes pipeline-shaped systems but rarely shows the timeline:
- Continuous batching (9.3.6)
- Speculative decoding draft/verify (9.4)
- Pipeline parallelism bubbles (59.4)
- Voice agent latency budget (40.1, partially done)
- Streaming ASR overlap windows (20.5)

A shared timeline-bar visual where each "lane" is a worker and shaded blocks are work would help readers feel the simultaneity vs sequential differences.

### Theme 3: Hierarchical / multi-stage filtering
Many real systems are funnels: cheap-then-expensive:
- Reranking (35.1)
- Tool selection (27.6)
- Guardrails layered (48.1)
- Hard-negative mining (31.1)

A funnel visual with candidate counts at each stage should appear in each, parameterized identically.

### Theme 4: Trade-off slider dashboards
The book has many "tune this dial" decisions left as bullet lists:
- Sampling penalties (4.2)
- Fine-tuning hyperparameters (16.4)
- LoRA rank / alpha (17.1)
- KL strength β (18.1)
- Decoding temperature + top-p combos (4.2)
- Quantization granularity (9.1)

A consistent "control panel" visual with sliders and safe-region indicators would reduce blank-staring at tables. Could be a templated SVG used in 6+ sections.

### Theme 5: Bias / drift / divergence curves
Many failure modes show as two curves separating over training or time:
- Reward hacking (18.2): proxy vs true reward
- Catastrophic forgetting (16.1): task vs general performance
- Drift detection (44.5): distribution distance over time
- Capability vs alignment (77.1): the rocket/parachute
- Loss spikes (6.5): instability in normal-loss curve

A shared "two curves diverge" visual template (paired line plots with a divergence-point callout) would reinforce the "watch for separation" mental habit.

### Theme 6: "What is shared, what is per-X" visuals
KV head sharing, ZeRO sharding, prefix caching, expert routing, weight tying. All reduce to "this thing is replicated N times; can we share?" A consistent visual idiom for shared-vs-private memory would harmonize:
- MHA / MQA / GQA (9.3.4)
- ZeRO 1/2/3 (59.2)
- Prefix caching (9.3.5)
- MoE shared experts (3.8)
- Weight tying (3.3)

### Theme 7: "Gotcha" panels for warnings
There are many `<div class="callout warning">` blocks that read as cautionary one-liners. A small but consistent "what NOT to do" cartoon panel (red border, do-not-do icon) for each warning would land better than a paragraph. Sections with high warning-count, low visuals:
- 30.3 (multi-agent patterns, 6 warnings, 1 visual)
- 48.1 (guardrails)
- 20.5 (speech recognition)
- 50.1 (privacy)

---

## METHODOLOGY

### How I searched

1. **Inventoried 449 section files** by writing a Python script that counts per-section: total visuals (img + svg), math blocks, inline math spans, figure tags, bullet items, warning callouts, and analogy/metaphor keywords ("like a", "imagine", "think of", "analog", "metaphor", "mental model").
2. **Ranked candidates** by three filters:
   - math_blocks ≥ 3 AND analogy_hits ≤ 2 → sections where the math dominates without intuition pumps
   - warnings ≥ 5 AND visuals ≤ 1 → sections with heavy "watch out" content but nothing visual
   - list_items ≥ 30 AND analogy_hits ≤ 1 → bulletlists that could become 2-axis comparisons or sliders
3. **Read top candidates** (~50 sections) to confirm whether an analogy was actually missing or already present in surrounding callouts. Read existing audits (`VISUAL_LEARNING.md`, `EXAMPLE_ANALOGY_R2.md`, `ARCHITECTURE_DIAGRAM_OPPORTUNITIES.md`, `MISCONCEPTION_R2.md`) to avoid duplicating work already done.
4. **Sampled at least 2 sections per part** beyond the metric-ranked candidates so I would not miss qualitatively interesting opportunities in low-math sections (security, ethics, applications, frontiers).

### What I counted as "existing"
- An analogy is "yes" if the section opens with a hero image that pictures the concept (e.g., librarian for KV cache, hiker for beam search) AND text in the body explicitly names the metaphor.
- "Partial" if either the hero image exists without textual reinforcement, or the text mentions an analogy but no visual exists.
- "No" if neither exists.

### What I deliberately skipped
- Pure tools-of-the-trade pages (modules ending in tools-of-the-trade / 5.x reading-list pattern)
- Application sections in Part 14 except for two qualitatively interesting cases
- `docs/`, `_archive/`, `KDP/`, `node_modules/`, `pagefind/`, `build/`, `.book-update/`, `__pycache__/`
- Sections already addressed in cycle 3.2 visual-learning sweep (Fig 26.3.2 reasoning agents, Fig 28.2.2 topologies, Fig 28.3.3 risk-routing, Fig 35.5.2 chunking, Fig 40.1.2 latency, Fig 42.10.2 kappa, Fig 43.5.2 modality matrix, Fig 33.4.2 multimodal product shapes, Fig 34.2.1 NER throughput): mentioned only where a different angle remains useful.

### Coverage statistics
- Sections audited in detail (full reading): ~50
- Sections inspected at headings level: ~150
- Modules with at least one HIGH opportunity flagged: 24 of 67
- Opportunities total: 95 (HIGH: 28, MEDIUM: 50, LOW: 17)
- Sections marked "yes existing analogy, skip": ~30, in line with prior cycles' coverage

### Confidence note
The strongest opportunities are in Module 09 (inference optimization), Modules 17-18 (PEFT and alignment), and the math-heavy sections of Module 03 (transformers) and Module 06 (pretraining). Module 14 (applications) is correctly bullet-list-heavy because the content is enumerative; do not retrofit analogies there. Appendix A has fewer opportunities because it serves as math reference and readers self-select.

---

## Recommended next-cycle batches

If the next pass dispatches by theme rather than by section, recommended batches:

- **Batch A: Inference internals visuals** (9 sections in Module 09)
  - 9.1 quantization number-line projection
  - 9.3 KV cache, MQA/GQA chefs, prefix lobby, eviction policies, memory-bandwidth straw
  - 9.4 speculative relay
  - 9.7 sparsity train carriages

- **Batch B: Alignment intuitions** (4 sections in Module 18)
  - 18.1 KL leash, PPO clip
  - 18.2 reward-hacking divergence curves, GRPO grading on a curve
  - 18.3 DPO margin scale-tilt

- **Batch C: RAG failure modes** (5 sections in Modules 32 and 35)
  - 32.1 lost-in-the-middle U-curve
  - 35.1 funnel
  - 35.2 HyDE chapter title
  - 31.1 magnetic field for contrastive
  - 31.4 product-quantization chunking

- **Batch D: Architecture intuitions** (3 sections in Module 03)
  - 3.5 RoPE clock-hands
  - 3.8 MoE courier vans
  - 2.3 (Module 02) sqrt(d_k) volume scaling

Each batch is ~5-10 inline SVGs of moderate complexity, well within a one-cycle dispatch.

---

## End of report

File saved at: `E:\Projects\BookBlogsHome\LLMBook\docs\content-audit\MENTAL_MODEL_OPPORTUNITIES.md`
