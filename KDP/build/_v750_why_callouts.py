"""Ship the WHY-insight callouts: 20 HIGH + 22 MEDIUM = 42 callouts.

Each callout is added right after the first <h2> of its target section,
matching the v738/v747 pattern. Idempotent via sentinel comments.

Duplicate-content safeguard: each entry includes a `dup_key`, a short
distinctive phrase from the proposed body (named principle, paper
citation, technical term unique to the WHY). If that phrase already
exists in the target file, the entry is skipped with a [DUP] tag.
This catches cases where the prior text already articulates the same
insight.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

# Each entry: (rel_path, sentinel_id, dup_key, title, body, priority)
ENTRIES = [
    # 1. SwiGLU/GeGLU
    ('part-1-foundations/module-04-transformer-architecture/section-4.1.html',
     'swiglu',
     'second-order Taylor',
     'Why SwiGLU and GeGLU beat ReLU at the same parameter count',
     'The improvement is not magic, it is a capacity-vs-stability tradeoff. The gating branch <code>SiLU(xW_gate)</code> lets each FFN unit decide multiplicatively whether to fire, so the layer represents a piecewise-linear function with sharper feature selectors than a single ReLU/GELU stack of the same width. Shazeer (2020, "GLU Variants Improve Transformer") frames this as the multiplicative interaction giving the FFN a second-order Taylor term that pure ReLU networks must learn through depth. Labs hold parameter count fixed (the gate steals one third of the hidden width), so the gain is "free" capacity along the most expressive direction, not added compute.',
     'HIGH'),

    # 2. RoPE
    ('part-1-foundations/module-04-transformer-architecture/section-4.3.html',
     'rope',
     'rotation rate',
     'Why RoPE extrapolates and sinusoidal embeddings do not',
     'The deeper reason RoPE wins is that it makes attention scores a function of position <em>difference</em>, not absolute position, so a context-length extension only requires extrapolating one scalar (the rotation rate) instead of teaching the model a new vocabulary of position vectors. Sinusoidal embeddings break at extrapolation because the absolute-position basis becomes out-of-distribution; learned embeddings cannot extrapolate at all. RoPE\'s frequencies form a geometric series, borrowed from Fourier analysis: low-frequency dimensions encode long-range position, high-frequency dimensions encode local position. NTK-aware scaling and YaRN exploit this by rescaling only the low-frequency band, preserving the local geometry the model was trained on.',
     'HIGH'),

    # 3. Chinchilla 20:1
    ('part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.3.html',
     'chinchilla-derived',
     'snapshot, not a law',
     'Why 20 tokens per parameter is a derived quantity, not a constant',
     'The 20:1 ratio is not a universal constant; it falls out of the specific exponents Hoffmann et al. fit (&alpha; &approx; 0.34, &beta; &approx; 0.28). Setting &part;L/&part;N = &part;L/&part;D under the compute constraint C = 6ND gives the optimal ratio D*/N* = (&alpha;A / &beta;B)^(1/(&alpha;+&beta;)). With Hoffmann\'s constants this evaluates near 20. The point worth stating: if the data exponent &beta; rises (better data), the ratio rises too, which is exactly why Llama 3 at ratio 1875 is not a contradiction but the <em>correct</em> response to improved data quality. The 20 is a snapshot, not a law of nature.',
     'HIGH'),

    # 4. BF16 vs FP16
    ('part-2-understanding-llms/module-09-inference-optimization/section-9.1.html',
     'bf16-range',
     'gradient underflow',
     'Why BF16 replaced FP16 in modern training pipelines',
     'BF16 has the same exponent width as FP32 (8 bits) but a truncated mantissa (7 bits vs FP16\'s 5 exponent + 10 mantissa). This is not arbitrary: in mixed-precision training the dangerous failure mode is gradient <em>underflow</em> into zero, not precision loss in the high-order bits. BF16 preserves the FP32 dynamic range, so loss scaling (the awkward hack required for FP16) becomes unnecessary. FP16\'s wider mantissa would only matter if activations were already near the same magnitude; in transformers they span many orders of magnitude across layers, so range beats precision. This is why every modern LLM training pipeline since GPT-NeoX uses BF16.',
     'HIGH'),

    # 5. Warmup
    ('part-4-training-adapting/module-15-fine-tuning-fundamentals/section-15.3.html',
     'adam-warmup',
     'unbounded variance',
     'Why warmup exists (and how long it should last)',
     'Warmup exists because Adam\'s per-parameter learning rate is <code>lr / (sqrt(v) + eps)</code>, and <code>v</code> is the running average of squared gradients. At step 0, <code>v</code> is essentially zero, so the effective step size is enormous and biased by whatever gradients happen to come through first. Liu et al. (2020, "On the Variance of the Adaptive Learning Rate") proved this formally: without warmup, early Adam updates have unbounded variance and can poison normalization layers permanently. Linear warmup is the practical fix that lets <code>v</code> accumulate enough samples for the variance to stabilize. The 10% figure is rough; theory says you need roughly 2/(1-&beta;<sub>2</sub>) steps, which is ~200 for Adam\'s default.',
     'HIGH'),

    # 6. SFT LR 2e-5
    ('part-4-training-adapting/module-15-fine-tuning-fundamentals/section-15.3.html',
     'sft-lr',
     'basin of attraction',
     'Why fine-tuning learning rates sit two orders of magnitude below pretraining',
     'The 2e-5 default is roughly 1/100 of typical pretraining rates, and the <em>ratio</em> matters more than the absolute number. Pretraining starts from random weights, so large steps explore the loss landscape productively. Fine-tuning starts inside a well-tuned local minimum: any step large enough to "leave" that minimum risks catastrophic forgetting, where the model degrades on capabilities it learned in pretraining. The empirical sweet spot keeps each step small enough that the cumulative drift stays within the basin of attraction. Rule of thumb: pretraining LR for 7B Llama-class models is around 3e-4, so SFT lives one to two orders of magnitude below it, and DPO/RLHF another order below that.',
     'MEDIUM'),

    # 7. HNSW
    ('part-5-retrieval-conversation/module-18-embeddings-vector-db/section-18.2.html',
     'hnsw-smallworld',
     'small-world',
     'Why HNSW achieves O(log N) search',
     'A multi-layer graph gives O(log N) search for the same reason a skip list does: each higher layer acts as an express lane that halves the expected number of hops. Malkov and Yashunin (2018) prove that if you assign layers by a geometric distribution with parameter 1/ln(M), the graph becomes a navigable small-world network (Milgram\'s six degrees, formalized). Greedy descent works because the small-world property guarantees that the nearest neighbor on layer &ell; is "close enough" to the true nearest neighbor on layer 0 to be a good entry point. M controls the in-degree, ef_construction controls how thoroughly you build each layer, and the log factor falls out for free.',
     'HIGH'),

    # 8. Product Quantization
    ('part-5-retrieval-conversation/module-18-embeddings-vector-db/section-18.2.html',
     'product-quant',
     'asymmetric distance computation',
     'Why product quantization beats brute-force k-means in 768 dimensions',
     'The word "product" is doing real work here: the effective codebook size is 256<sup>96</sup> &approx; 10<sup>231</sup>, but only 96 &times; 256 = 24,576 centroids ever need to be trained. This is the same trick (Cartesian product of small codebooks) that compressed video codecs use. Jegou, Douze, and Schmid (2011) showed that distances in R<sup>d</sup> approximately decompose across orthogonal subspaces, so squared L2 distance can be computed as a sum of m table lookups instead of d multiplications. The "asymmetric distance computation" further refines this by keeping the query in full precision and only quantizing the database. Without the decomposition, brute-force k-means in 768 dimensions would need an absurd number of centroids to cover the space.',
     'HIGH'),

    # 9. BM25
    ('part-5-retrieval-conversation/module-19-rag/section-19.2.html',
     'bm25-still-matters',
     'disjoint ways',
     'Why BM25 still matters alongside dense retrieval',
     'Embeddings learn smooth manifolds; rare strings (product SKUs, error codes, function names, drug names) sit at the embedding manifold\'s boundary where similarity collapses to noise. BM25 scores explicit token matches, which is the failure mode embeddings are mathematically guaranteed to handle worst. The famous BM25 constants k<sub>1</sub> &approx; 1.2 and b &approx; 0.75 come from Robertson and Walker\'s (1994) probabilistic relevance framework: k<sub>1</sub> saturates term frequency so that twenty occurrences of "diabetes" do not dominate one occurrence, and b controls how aggressively to penalize long documents. Hybrid search wins because dense and sparse retrievers fail in disjoint ways.',
     'HIGH'),

    # 10. Chunk size 512
    ('part-5-retrieval-conversation/module-19-rag/section-19.8.html',
     'chunk-512',
     'two failure modes cross',
     'Why 512 tokens is the default chunk size',
     'The 512-token default is downstream of two unrelated constraints that happen to collide. First, most production embedding models (E5, BGE, OpenAI text-embedding-3) were trained with max sequence length 512, so longer chunks get silently truncated. Second, average-pooled embeddings exhibit the "lost-in-the-middle" effect: the longer the chunk, the more averaged-out the semantic signal. Both push toward small chunks. The opposing force is the granularity penalty: a single sentence rarely carries enough context to answer a real question, so retrieval drags in the wrong neighbors. 512 is the empirical sweet spot only because that is where the two failure modes cross. With long-context embedders the right answer shifts toward 1024-2048.',
     'MEDIUM'),

    # 11. Sliding Window Attention
    ('part-2-understanding-llms/module-07-modern-llm-landscape/section-7.2.html',
     'swa-receptive-field',
     'receptive-field trick',
     'Why sliding window attention scales to 128K positions',
     'SWA is not just "cheaper attention", it is a layered receptive-field trick borrowed from CNNs. Each layer attends locally over W tokens, but stacked L deep the effective receptive field is L &times; W, so a 32-layer model with W=4096 can route information across 128K positions even though no single layer ever performs a 128K &times; 128K attention. The KV-cache memory therefore grows with W, not sequence length, which is the actual production win. The cost: dependencies more than W apart in a single layer cannot interact, so models compensate by interleaving SWA with full-attention layers (Gemma 2) or using register tokens. Mistral 7B v0.2 dropped SWA precisely because the depth penalty turned out to be real.',
     'HIGH'),

    # 12. NF4
    ('part-2-understanding-llms/module-09-inference-optimization/section-9.1.html',
     'nf4-quantile',
     'quantiles of a standard normal',
     'Why NF4 beats INT4 on the same bit budget',
     'NF4 ("4-bit NormalFloat") is the QLoRA paper\'s signature trick and a beautiful example of distribution-aware quantization. The insight: pretrained weight tensors are empirically near-Gaussian with mean 0 and known variance. Integer quantization spends equal precision on values that almost never occur (the tails) and values that occur constantly (near zero). NF4 instead places its 16 quantization levels at the quantiles of a standard normal, so each level carries equal <em>probability mass</em>. This is information-theoretically optimal for Gaussian data and beats INT4 by 0.5-1.0 perplexity points on the same bit budget. The lesson generalizes: every quantization scheme is implicitly a prior on the value distribution.',
     'HIGH'),

    # 13. GQA asymmetry
    ('part-2-understanding-llms/module-09-inference-optimization/section-9.2.html',
     'gqa-redundancy',
     'redundancy hypothesis',
     'Why GQA shares K and V but keeps separate Q heads',
     'The reason heads can be safely shared at all (GQA, MQA) is the "redundancy hypothesis": Ainslie et al. (2023) and Shazeer (2019) measured the rank of the K and V projections in trained MHA models and found they live in a much lower-dimensional subspace than their h &times; d_k allocation suggests. Most heads encode similar key patterns with minor rotations, so collapsing them costs little quality. The query side, by contrast, exhibits genuine functional specialization across heads (induction, copy, syntax), so reducing Q-heads is much more damaging. GQA exploits this asymmetry: many distinct queries against few shared keys, which is also the structure of database joins. The architecture matches the latent factorization of attention.',
     'MEDIUM'),

    # 14. DoRA
    ('part-4-training-adapting/module-16-peft/section-16.2.html',
     'dora-decouple',
     'unit-direction matrix',
     'Why DoRA at rank 16 outperforms LoRA at rank 32',
     'The asymmetry is mechanical, not empirical. LoRA learns &Delta;W = BA in a single low-rank subspace, which forces magnitude and direction updates to be entangled: scaling a column of B changes both the direction of the update and its norm. DoRA decomposes W = m &middot; V/&Vert;V&Vert; and updates the unit-direction matrix V with low-rank, while updating the magnitude vector m separately. This lets the optimizer move along the unit sphere without using rank capacity to also re-scale, so the same rank budget buys more directional expressivity. The framework generalizes the classical "decouple weight decay from gradient" trick (AdamW) one level deeper into the parameterization itself.',
     'MEDIUM'),

    # 15. Greedy degenerate repetition
    ('part-1-foundations/module-05-decoding-text-generation/section-5.1.html',
     'likelihood-quality-gap',
     'likelihood-quality gap',
     'Why greedy and beam search produce degenerate repetition',
     'Holtzman et al. (2020, "The Curious Case of Neural Text Degeneration") explained this with the "likelihood-quality gap": maximum-likelihood decoding finds a <em>self-reinforcing low-entropy attractor</em>. Once the model emits a phrase, that phrase is now in context, and the conditional probability of repeating it climbs because language statistics favor exact repetition over novel rephrasing in short windows. Greedy decoding cannot escape; beam search makes it worse by <em>pruning toward</em> the attractor. This is also why beam search dominates for translation (output bounded by source) and fails for open generation (nothing to anchor against). Sampling methods are not just creative; they are dynamically escaping a known mathematical trap.',
     'HIGH'),

    # 16. BPE greedy = Shannon
    ('part-1-foundations/module-02-tokenization-subword-models/section-2.2.html',
     'bpe-shannon',
     'Pareto front',
     'Why BPE\'s greedy merge approximates Shannon-optimal coding',
     'BPE\'s greedy merge rule (pick the most frequent adjacent pair, merge it, repeat) is doing something subtle: it performs approximate maximum-likelihood compression of the corpus under a unigram model over the evolving vocabulary. Shannon-style coding theory says the optimal code length for a symbol is -log p, and the greedy merge minimizes expected code length step-by-step. The reason BPE wins over character-level or word-level is Zipf\'s law: word frequencies decay as a power law, so a fixed vocabulary cannot cover the tail without UNK tokens, but characters force the model to do too much work learning that "ing" is one unit. Subword tokenization is the Pareto front of these two extremes.',
     'MEDIUM'),

    # 17. Plan-and-execute vs ReAct
    ('part-6-agentic-ai/module-21-ai-agents/section-21.2.html',
     'deliberative-reactive',
     'deliberative',
     'Why plan-and-execute and ReAct each win in different environments',
     'The plan-and-execute vs ReAct tradeoff is a special case of the classical AI distinction between <em>deliberative</em> and <em>reactive</em> planners (Russell &amp; Norvig, Ch 11). Deliberative planners commit early to a sequence of actions and pay the cost of replanning if the world diverges; reactive planners decide one step at a time and pay a per-step reasoning cost. The right choice depends on the <em>predictability</em> of the environment. Code migration is mostly predictable, so plan-and-execute amortizes its planning cost. Web research has high per-step novelty, so ReAct\'s adaptiveness wins. Hybrid agents (plan with replanning intervals) approximate the Bellman-optimal policy for partially observable environments.',
     'MEDIUM'),

    # 18. Function-calling = constrained decoding
    ('part-6-agentic-ai/module-22-tool-use-protocols/section-22.1.html',
     'constrained-decode-tools',
     'soft preference into a hard guarantee',
     'Why JSON tool-calls beat free-form ReAct text',
     'The reason JSON tool-call APIs work better than the early "ReAct in text" pattern is a constrained-decoding effect, not just a parsing convenience. When the provider\'s runtime constrains the model\'s logits to valid JSON-schema continuations during generation (via grammars, FSMs, or speculative resampling), the model never enters an invalid state and never has to "recover" from a malformed argument. Free-form parsing forces the model to do two jobs simultaneously: choose the action and produce well-formed syntax. Constrained decoding factors these. This is the same insight behind structured outputs and JSON mode: pushing constraints from the prompt down into the decoder turns a soft preference into a hard guarantee.',
     'MEDIUM'),

    # 19. Value model in PPO
    ('part-4-training-adapting/module-17-alignment-rlhf-dpo/section-17.1.html',
     'value-baseline-variance',
     'variance-reducing baseline',
     'Why PPO needs a value model (and GRPO can drop it)',
     'The value model is not optional optimization theater. Pure REINFORCE (policy gradient without baseline) has gradient variance proportional to the squared reward magnitude, which blows up for long sequences because rewards are accumulated. Subtracting a learned state-value baseline reduces this to <em>advantage</em> variance, and Williams (1992) proved this baseline is unbiased: it cancels in expectation while halving variance in practice. For LLMs, where each generated sequence is dozens of tokens long, the variance reduction is the difference between training that converges and training that diverges within 50 steps. This is also why GRPO replaces the value model with a group-mean baseline: it is a cheaper but still valid variance-reducing baseline.',
     'HIGH'),

    # 20. DPO beta
    ('part-4-training-adapting/module-17-alignment-rlhf-dpo/section-17.2.html',
     'dpo-beta-dual',
     'tuning two physical effects',
     'Why DPO\'s &beta; is doing two jobs at once',
     'The &beta; parameter is doing double duty. Mathematically, &beta; is the inverse temperature of the Bradley-Terry preference model <em>and</em> the KL-penalty strength against the reference policy. These are not independent: a high &beta; both sharpens the preference signal (steeper accept/reject decisions) and constrains the policy closer to the reference. The classic failure modes have orthogonal causes: too-low &beta; lets the policy drift into low-likelihood regions where the reference probabilities are noise, producing incoherent text; too-high &beta; underweights the preference signal and you get a model that is well-behaved but indistinguishable from the SFT model. The reader should understand they are tuning two physical effects with one number.',
     'HIGH'),

    # 21. MoE aux-loss coefficient
    ('part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.3.html',
     'moe-auxloss-range',
     'optimizer\'s noise floor',
     'Why the MoE load-balance coefficient lives in 1e-3 to 1e-2',
     'The narrow range is dictated by a tension visible in the loss landscape, not by trial-and-error. Fedus et al. (2022) measured the gradient norm of the load-balance loss vs the language-modeling loss across training and found the ratios that keep both gradients within an order of magnitude land in 1e-3 to 1e-2. Below 1e-3 the load-balance gradient is dominated by Adam\'s noise floor and the constraint stops being active. Above 1e-2 the balance loss overwhelms the LM signal and experts are forced into uniform routing, collapsing specialization. This is the same dynamic-range argument that governs auxiliary losses across the field: aux-loss coefficients are bounded above by the dominant gradient and below by the optimizer\'s noise floor.',
     'MEDIUM'),

    # 22. LLM-as-judge biases
    ('part-8-evaluation-production/module-28-evaluation-observability/section-28.5.html',
     'judge-biases',
     'position bias',
     'Why LLM-judges need order randomization, length normalization, and source diversity',
     'LLM-judges ship with three systematic biases (Zheng et al., 2024, "Judging LLM-as-a-Judge with MT-Bench"): (1) <em>position bias</em> (judges prefer whichever response is shown first, mitigated by random swapping), (2) <em>verbosity bias</em> (longer responses score higher even when judged on correctness, the GPT-4 effect), and (3) <em>self-preference</em> (a judge of family X scores responses from family X higher, the closest thing alignment has to a fingerprint). These are not edge cases; they swing benchmark rankings by 5-15 percentage points. The mitigation is structured: pairwise comparison with order randomization, length-normalized prompts, and judge-source diversity.',
     'HIGH'),

    # 23. Drift = covariate shift
    ('part-8-evaluation-production/module-28-evaluation-observability/section-28.4.html',
     'covariate-shift',
     'covariate shift',
     'Why all drift types are the same statistical phenomenon',
     'All three drift dimensions are instances of one principle: the deployed system is a learned approximation conditioned on a frozen distribution, and any change to the conditioning distribution invalidates the approximation. The formal name is <em>covariate shift</em> (Shimodaira, 2000), and the diagnostic is the same regardless of whether the input distribution shifted (user behavior), the embedding distribution shifted (model update), or the prompt-conditional distribution shifted (silent provider update): the joint distribution P(x, y) of evaluation triples drifts from the joint it was validated on. Every monitoring strategy in this section is approximating D<sub>KL</sub>(P<sub>prod</sub> &Vert; P<sub>val</sub>) along some marginal.',
     'MEDIUM'),

    # 24. p50/p95/p99 for LLM
    ('part-8-evaluation-production/module-29-production-engineering/section-29.9.html',
     'ttft-tpot',
     'harmonic mean of request lengths',
     'Why LLM p99 latency is dominated by output length, not queue depth',
     'In a stateless web service, p99 is set by outlier requests and queuing. In token-streaming LLM services, p99 is dominated by <em>long generations</em>: a 5% chance of a response 10x the median length, combined with autoregressive decoding, multiplies p99 by 10x even with a perfect server. This is also why TTFT (time to first token) and TPOT (time per output token) became the dominant SLOs instead of end-to-end latency: they decouple the queuing tail (TTFT) from the length tail (TPOT). Knowing which tail you are debugging tells you which fix applies: TTFT regressions need queue-and-batching attention; TPOT regressions need decoding-speed attention.',
     'MEDIUM'),

    # 26. XML delimiters
    ('part-3-working-with-llms/module-12-prompt-engineering/section-12.5.html',
     'xml-delim-prior',
     'structural anchors',
     'Why XML tags and markdown headers work as prompt delimiters',
     'XML-tag delimiters work in practice because Anthropic\'s RLHF data (and most modern SFT data) explicitly uses XML-like structure for tool calls, multi-turn agents, and system prompts. The model has been <em>trained</em> to treat <code>&lt;context&gt;</code> and <code>&lt;/context&gt;</code> as distinguished boundary tokens, not because there is anything magical about angle brackets. This is also why markdown headers, JSON keys, and triple-quote fences work: the pretraining corpus uses them as structural anchors. The general principle: prompt structure works to the extent it matches the structural priors the model learned from data. Inventing a novel delimiter (like <code>~~~SECTION_BEGIN~~~</code>) is empirically weaker than reusing one the model has seen ten million times.',
     'MEDIUM'),

    # 27. Synthetic data collapse
    ('part-4-training-adapting/module-14-synthetic-data/section-14.1.html',
     'variance-ladder',
     'variance ladder',
     'Why synthetic data sometimes catastrophically fails',
     'The Phi success is impressive but it elides why synthetic data sometimes catastrophically fails (Shumailov et al., 2024, "AI Models Collapse When Trained on Recursively Generated Data"). The principle is the variance ladder: each generation of synthetic data is a sample from a <em>narrower</em> distribution than its teacher, because sampling-based generation cuts off the long tail of low-probability outputs. Training on this narrower distribution produces a model that samples from a yet-narrower distribution, and the recursion converges to a delta function within a few generations. Phi worked because it used a strong external teacher (GPT-4) and high-quality filtering, not recursive self-distillation. Synthetic data is safe when the entropy budget is being <em>added</em>, not just recycled.',
     'HIGH'),

    # 28. Goodhart generalized
    ('part-4-training-adapting/module-17-alignment-rlhf-dpo/section-17.1.html',
     'adversarial-proxies',
     'adversarial proxies',
     'Why reward hacking, judge gaming, and benchmark overfit are the same phenomenon',
     'Any time you measure a <em>proxy</em> for what you actually want, the optimizer will find the gap between the proxy and the target. This is Goodhart\'s Law generalized: reward-hacking, judge-gaming, and benchmark-overfit are the same phenomenon with different names. The structural fix is <em>adversarial proxies</em>: instead of one reward model, train an ensemble whose members disagree on out-of-distribution responses, then trust only the consensus. This is the same insight behind ensemble Bayesian uncertainty, train/test splits, and held-out judges. Naming the principle once lets the reader recognize it in evals (Chapter 28), RAG (Chapter 19), and agent rewards (Chapter 25) alike.',
     'HIGH'),

    # 29. CoT extends compute
    ('part-2-understanding-llms/module-08-reasoning-test-time-compute/section-8.1.html',
     'cot-turing',
     'Merrill and Sabharwal',
     'Why chain-of-thought is a computational extension, not just a prompting trick',
     'Each generated reasoning token expands the model\'s effective compute by one forward pass without adding any parameters. The model is using its context window as scratch space, which means it can perform multi-step computations that are physically impossible to compute in a single forward pass (the depth of the network is fixed). This is Merrill and Sabharwal\'s (2024) "Expressive Power of Transformers with Chain of Thought" result: with T CoT tokens, a transformer can simulate a Turing machine for T steps. Without CoT, transformers are bounded by a uniform circuit class. CoT is not just a prompting trick; it is a computational extension that turns a fixed-depth network into a variable-depth one.',
     'HIGH'),

    # 30. Self-consistency assumption
    ('part-2-understanding-llms/module-08-reasoning-test-time-compute/section-8.4.html',
     'self-consistency-mode',
     'bimodal',
     'When self-consistency helps and when it does not',
     'Self-consistency works because the model\'s failure modes are <em>high-variance</em> but <em>centered on the correct answer</em>. Wang et al. (2023) showed that for chain-of-thought reasoning, the distribution of sampled answers is bimodal: a high-probability correct mode and a long tail of low-probability wrong modes with no single dominant error. Majority voting therefore approximates the mode of the posterior over reasoning paths, which is asymptotically the correct answer. This breaks down when the model has a <em>systematic</em> bias (a consistent wrong belief), in which case more samples reinforce the error. Knowing the assumption tells you when self-consistency will help (math, logic) and when it will not (factual recall from training data).',
     'HIGH'),

    # 31. Lost in the middle / history truncation
    ('part-5-retrieval-conversation/module-20-conversational-ai/section-20.3.html',
     'lost-in-middle-history',
     'Liu et al., 2024',
     'Why recency and relevance beat coverage in long conversation histories',
     'The "lost-in-the-middle" effect (Liu et al., 2024) means attention to the middle of a long context decays sharply, so just keeping more history does not help and may hurt. The mechanism is that during pretraining, most documents are shorter than the eventual deployed context, so the model never developed strong "middle attention". Effective conversation history management therefore optimizes <em>recency</em> and <em>relevance</em> rather than <em>coverage</em>: a salient three-turn snippet from twenty turns ago is better than five recent turns of small talk. Summarization works because it reformats far-context as near-context. This is also why agents use scratchpads instead of long unbounded histories.',
     'MEDIUM'),

    # 32. Multi-agent Conway
    ('part-6-agentic-ai/module-23-multi-agent-systems/section-23.2.html',
     'conway-multiagent',
     'Conway',
     'When multi-agent decomposition actually beats a single agent',
     'Multi-agent decomposition only beats a single agent when the <em>bandwidth between sub-problems</em> is lower than the <em>capacity cost of holding both in context</em>. If sub-agents need to share most of their reasoning, the inter-agent message-passing serializes what a single agent would do in parallel attention, and you lose. This is the Conway\'s-law cousin of microservices: distributing a system pays off only when interfaces are narrower than internals. Multi-agent debate, planner/executor splits, and tool-specialized agents are all instances of this; LLM-routing-to-LLM (where each agent solves a similar but slightly different problem) usually is not.',
     'MEDIUM'),

    # 34. CLIP + T5 in diffusion
    ('part-7-multimodal-applications/module-26-multimodal/section-26.2.html',
     'clip-t5-complement',
     'complementary encoders',
     'Why modern diffusion models use both CLIP and T5 text encoders',
     'The choice between CLIP and T5 as the text encoder in diffusion models is structural. CLIP was contrastively trained against images, so its text embeddings live in the same space as image embeddings and capture visual concepts well, but they lose fine-grained linguistic structure (CLIP famously cannot count or handle compositions). T5 was trained as a language model, so it preserves syntax and counting but does not encode visual-relevance priors. Modern systems (SDXL, FLUX) use <em>both</em> in parallel: T5 supplies the linguistic structure, CLIP supplies the visual grounding, and the diffusion model sees their concatenation. This is the canonical example of complementary encoders, mirrored by hybrid retrieval (BM25 + dense).',
     'MEDIUM'),

    # 35. Jailbreaks - superficial alignment
    ('part-9-safety-strategy/module-30-safety-ethics-regulation/section-30.4.html',
     'superficial-alignment',
     'superficial alignment hypothesis',
     'Why jailbreaks succeed (and why patching individual ones does not generalize)',
     'Jailbreaks succeed for one structural reason: alignment training is a thin layer of behavior on top of capabilities learned from a much larger and more diverse pretraining corpus. The pretraining distribution contains uncensored examples of every harmful behavior, and alignment essentially adds a refusal classifier near the output. Any prompt that takes the model out-of-distribution relative to the alignment training data (role-play, low-resource languages, base64, ASCII art) bypasses that thin layer and exposes the underlying capability. This is the "superficial alignment hypothesis" (Lin et al., 2024) and explains why patching individual jailbreaks does not generalize: the underlying capability never goes away, only the classifier\'s coverage expands.',
     'HIGH'),

    # 36. Continuous batching
    ('part-8-evaluation-production/module-29-production-engineering/section-29.5.html',
     'continuous-batching-harmonic',
     'harmonic mean',
     'Why continuous batching delivers 2-10x throughput gains',
     'In autoregressive LLM serving, different requests have wildly different output lengths, and static batching forces the entire batch to wait for the longest. Continuous batching (Yu et al., 2022; vLLM) lets each request leave the batch when it finishes and lets new requests join mid-flight, so the average batch utilization tracks the <em>harmonic mean</em> of request lengths instead of the <em>max</em>. The 2-10x throughput gain is exactly the gap between these two means for typical length distributions. The principle: batching with heterogeneous job sizes always benefits from preemptive scheduling, a result that predates LLMs by decades in operating-system literature.',
     'MEDIUM'),

    # 37. Flash Attention
    ('part-1-foundations/module-04-transformer-architecture/section-4.4.html',
     'flash-tiling',
     'online-softmax recurrence',
     'Why Flash Attention is faster despite computing the same math',
     'Flash Attention\'s speedup comes from a tiling reorder, not from any algebraic trick: standard attention reads the N &times; N score matrix to and from HBM twice (once to compute softmax, once to apply it to V). Dao et al. (2022) showed you can fuse softmax and the V-multiply into a single pass over tiles small enough to fit in SRAM, using an online-softmax recurrence (Milakov and Gimelshein, 2018) that updates the running max and sum incrementally. The wall-clock win is purely the HBM-vs-SRAM bandwidth ratio (typically 10-20x), and the math is bit-for-bit identical. This is a microcosm of modern GPU optimization: most "kernel improvements" are memory-hierarchy reorderings that the autograd framework cannot do for you.',
     'MEDIUM'),

    # 38. Mamba / SSM
    ('part-10-frontiers/module-33-emerging-architectures/section-33.3.html',
     'ssm-selective',
     'input-dependent',
     'Why selective SSMs (Mamba) recover attention-like quality',
     'SSMs are interesting not because they are "different from attention" but because they recover a specific tradeoff: linear time and constant memory per step, at the cost of a fixed-size hidden state that must summarize all past tokens. This is RNN territory, but Mamba and friends fix RNNs by making the state-update matrix <em>input-dependent</em>, which lets the model selectively forget or carry information. The classical RNN failure mode was that the state-update was fixed at train time; Mamba treats it like attention\'s K/V (data-conditioned). The architecture is mathematically a continuous-time linearization of attention\'s discrete recurrence, which is why SSM performance approaches transformer performance on benchmarks that do not require precise long-range recall.',
     'MEDIUM'),

    # 39. LLM canary deployment
    ('part-11-idea-to-product/module-35-shipping-scaling/section-35.4.html',
     'quality-canary',
     'quality-percentage canaries',
     'Why LLM canaries need quality budgets, not just traffic percentages',
     'LLM canary deployments need a different design than traditional canaries for one reason: LLM regressions are <em>latent</em>, not crash-loud. A bad model deployment will not throw exceptions; it will produce slightly worse responses that only show up in aggregate quality metrics days later. Traditional traffic-percentage canaries (start at 1%, ramp to 100%) therefore need to be paired with <em>quality-percentage canaries</em>: hold the canary at a fixed traffic percentage until you have collected enough quality-eval samples to detect a 2% regression with 95% confidence. This is essentially A/B-test sample-size math applied to model rollouts. Without it, canaries provide false confidence.',
     'MEDIUM'),

    # 40. Thinking-time tax
    ('part-9-safety-strategy/module-31-strategy-product-roi/section-31.3.html',
     'thinking-time-tax',
     'thinking-time tax',
     'Why token cost is not falling along Moore\'s-law lines',
     'Every doubling of model quality from frontier-class iteration has come with a 2-10x increase in token consumption per query (CoT, reasoning models, agentic loops). This breaks naive ROI projections that assume token cost falls along Moore\'s-law lines. The right framing is to model <em>quality per dollar</em> on a Pareto frontier and treat token cost as the price of a particular quality tier. A model that is 10x cheaper but generates 10x more tokens to achieve the same task quality has not actually gotten cheaper. Vendors will continue to externalize compute as inference scaling, so this "thinking-time tax" is a structural trend, not temporary.',
     'MEDIUM'),

    # 41. Residual stream / superposition
    ('part-2-understanding-llms/module-10-interpretability/section-10.1.html',
     'residual-superposition',
     'Johnson-Lindenstrauss',
     'Why the residual stream is the only communication channel between layers',
     'The residual stream framing is described as a metaphor but it is a load-bearing mechanical fact: because every sublayer reads and writes additively through a residual connection, the residual stream is the <em>only</em> communication channel between layers. Features must be encoded as directions in residual-stream space, and the model has an incentive to pack many features into the same dimensions ("superposition"). Elhage et al. (2022) showed that the resulting feature geometry obeys the Johnson-Lindenstrauss bound: d dimensions can encode roughly exp(d / &epsilon;<sup>2</sup>) near-orthogonal features. This is why MLP widths are typically 4x the attention dimension: the network needs the extra room to read superposed features cleanly before writing them back.',
     'MEDIUM'),

    # 42. LoRA target Q,V not FFN
    ('part-4-training-adapting/module-16-peft/section-16.1.html',
     'lora-target-attention',
     'task-specific routing',
     'Why LoRA targets attention by default, not FFNs',
     'The convention to target Q and V (and sometimes K and O) but rarely the FFN comes from Hu et al.\'s original ablation: attention projection matrices contributed most of the per-task gain at a fraction of the parameters, because attention is where task-specific <em>routing</em> lives (which tokens attend where), while FFNs hold <em>factual knowledge</em> learned during pretraining that fine-tuning should not disturb. This maps onto the Geva et al. (2021) finding that FFN layers behave like key-value memory stores. The principle: adapt the parts of the network that need to learn <em>new behavior</em>, freeze the parts that store <em>existing knowledge</em>. Targeting FFNs in LoRA can be useful for domain adaptation where new facts matter; targeting attention is better for new tasks.',
     'MEDIUM'),

    # 44. LLM vs traditional ML
    ('part-3-working-with-llms/module-13-hybrid-ml-llm/section-13.1.html',
     'bitter-lesson-app',
     'bitter lesson',
     'Why specialization wins for narrow tasks and LLMs win when conditions shift',
     'Traditional ML beats LLMs whenever the task has abundant labeled data, narrow scope, and a stable distribution, because under those conditions specialization is cheap and a small model can saturate the achievable accuracy. LLMs beat traditional ML when <em>any one</em> of those conditions fails: few labels (use in-context learning), broad scope (use the LLM\'s transfer), or shifting distribution (use the LLM\'s pretraining-time generality). This is the "bitter lesson" applied at the application layer: for any fixed task and abundant data, specialization wins, but for shifting tasks or scarce data, general-purpose models win. Naming this lets readers stop relitigating the choice case by case.',
     'MEDIUM'),

    # 45. PagedAttention = virtual memory
    ('part-2-understanding-llms/module-09-inference-optimization/section-9.4.html',
     'paged-virtual-memory',
     'copy-on-write, swapping',
     'Why PagedAttention is virtual memory for the KV cache',
     'PagedAttention works because the KV cache has the same access pattern as virtual memory: many concurrent requests of unknown final length, each growing one page at a time, all needing to share a fixed physical pool. Kwon et al. (2023) explicitly modeled this on the OS paging algorithms from the 1960s. The 2-4x throughput gain comes from eliminating two waste sources: internal fragmentation (preallocating worst-case KV lengths per request) and external fragmentation (free slots stranded between active requests). Stating that PagedAttention is "virtual memory for the KV cache" (not just an LLM-specific trick) lets readers transfer all their OS-paging intuitions (copy-on-write, swapping, page-sharing for prefix caching) directly.',
     'HIGH'),
]

H2_RE = re.compile(r'(<h2[^>]*>[^<]*</h2>)', re.IGNORECASE)


def render(sentinel: str, title: str, body: str) -> str:
    return (
        f'<div class="callout key-insight"><!-- v750-{sentinel} -->\n'
        f'<div class="callout-title">Why: {title}</div>\n'
        f'<p>{body}</p>\n'
        f'</div>\n'
    )


def main() -> int:
    inserted = 0
    skipped_dup = 0
    skipped_existing = 0
    not_found = []

    for rel_path, sentinel, dup_key, title, body, priority in ENTRIES:
        path = ROOT / rel_path
        if not path.exists():
            not_found.append(rel_path)
            continue
        html = path.read_text(encoding='utf-8')
        sentinel_marker = f'<!-- v750-{sentinel} -->'
        if sentinel_marker in html:
            skipped_existing += 1
            print(f'  = [{priority}] {sentinel} (already present)')
            continue
        # Duplicate-content guard: skip if dup_key already in file
        if dup_key.lower() in html.lower():
            skipped_dup += 1
            print(f'  [DUP {priority}] {sentinel} (dup_key "{dup_key}" already in {rel_path})')
            continue
        m = H2_RE.search(html)
        if not m:
            not_found.append(rel_path + ' (no h2)')
            continue
        callout = render(sentinel, title, body)
        ins = m.end()
        new_html = html[:ins] + '\n' + callout + html[ins:]
        path.write_text(new_html, encoding='utf-8')
        inserted += 1
        print(f'  + [{priority}] {sentinel}: {rel_path}')

    print(f'\nInserted: {inserted}')
    print(f'Skipped (dup_key in file): {skipped_dup}')
    print(f'Skipped (sentinel already present): {skipped_existing}')
    if not_found:
        print(f'NOT FOUND ({len(not_found)}):')
        for p in not_found:
            print(f'  ! {p}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
