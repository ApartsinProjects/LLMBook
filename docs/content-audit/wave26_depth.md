# Wave 26: scientific / technical depth audit

This audit compares the "new" chapters (Ch 36, 41, 56, 59, 61 + Wave 17i
consolidated sections) against the depth bar set by canonical sections like 3.1
(Transformer block), 6.3 (Scaling Laws), 9.1 (Quantization), and 17.1 (LoRA).

## Calibrating the depth bar

The depth-bar sections share a distinctive signature, present in roughly this
density:

- **600-1100** inline math tokens (`class="math"` / `$$ math-block $$`) per section,
  derivations, complexity bounds, scaling formulas.
- **12-18** purpose-typed callouts (`key-insight`, `mental-model`, `note`,
  `warning`, `practical-example`, `fun-note`, `big-picture`) per section.
- An information-theoretic or systems-research cross-field connection at least
  once per section (information theory, classical IR, distributed systems,
  signal processing, statistics).
- At least one worked numeric example with explicit units and concrete numbers
  ("$M = 16P$ bytes for FP32 AdamW state, 1.12 TB for a 70B model").
- Forward / backward links to other chapters (4-12 internal cross-references).

By contrast, the new chapters cluster at:

| chapter | math tokens / sec | callouts / sec | worked numeric examples |
|---|---|---|---|
| Ch 36 (Retrieval Tools) | **0** | 2-4 | 1-2 narrative |
| Ch 41 (ConvAI Tools) | **0** | 3-4 | 1-2 case studies |
| Ch 56 (RAI Tools) | **0** | 3-5 | 1 case study |
| Ch 59 (Distributed Training) | 0-3 | 3-5 | 2-3 quantitative |
| Ch 61 (Scale Tools) | **0** | 2-3 | 1 case study |
| Wave 17i sections | **0** | varies | varies |

**Chapter 59 is the only one that clears the depth bar.** Sections 59.1, 59.2,
59.3, 59.4, 59.5 each contain genuine equations (memory accounting, ring
all-reduce bandwidth, BSP cost minimization, bubble-fraction $(P-1)/M$, MFU
formula, checkpoint-cadence optimum $T^*=\sqrt{2C\tau}$), worked examples with
numbers (Llama-3 405B, 419 failures / 54 days, 30 GB/s checkpoint), and
cross-field connections (BSP from Valiant 1990, async / Hogwild!, the Patarasuk
& Yuan bandwidth-optimality proof). They could be inserted into Part II
unaltered.

**The remaining four "tools" chapters (36, 41, 56, 61) are encyclopedic catalogs**
of vendors and libraries with strong relative-comparison prose (Pick X
when..., avoid when...) but almost no math, no derivations, no
recall-vs-latency curves, no Pareto frontiers, no Big-O complexity. They read
like very well-edited Awesome-list pages: useful, but the format does not
exercise the depth bar.

**Wave 17i consolidated sections** (24.6, 24.13, 26.6, 27.5, 29.1, 29.4, 35.2,
35.3, 37.3) are pedagogically substantive but also math-free. 35.2 (KG-RAG) and
29.1 (code-agent patterns) are the strongest of the Wave 17i set.

## Top remaining depth gaps (prioritized)

The 10 highest-impact gaps, ranked by reader-comprehension uplift per
paragraph added.

1. **[HIGH, Ch 36] No quantitative HNSW vs IVF-PQ recall-latency table.** The
   chapter discusses index types abstractly ("HNSW is the default", "PQ cuts
   memory 16-64x") but gives no public-benchmark numbers anchoring the trade-off.
   *Propose:* a callout-sized table (3-5 rows) with ANN-Benchmarks
   recall@10 / QPS for HNSW (M=16, ef=64), IVF-Flat (nlist=4096, nprobe=32),
   IVF-PQ-32 on a 1M-vector dataset. Insert in §36.1 between current §36.1.4 and
   §36.1.5. Size: 1 callout (~150 words) + 1 small table.

2. **[HIGH, Ch 36] No derivation of why Matryoshka representations work.**
   §36.4.7 says "MRL trains an embedder so that the first $k$ dimensions are
   themselves a useful embedding" but does not explain the nested-loss training
   objective $\mathcal{L}_{MRL} = \sum_{k \in K} c_k \cdot \mathcal{L}(z_{1:k},
   y)$ or why this yields a near-linear quality-vs-dim curve. *Propose:* a
   key-insight callout citing Kusupati et al. 2022 with the loss expression and
   one-paragraph explanation that nesting forces redundancy decay along
   coordinate order. Size: 1 callout (~200 words).

3. **[HIGH, Ch 36 / 41 / 56] No BM25 formula, no recall@k formula, no NDCG
   formula.** §36.3.10 enumerates metrics but never writes down the equation
   for NDCG@k = DCG@k / IDCG@k with $DCG@k = \sum_{i=1}^{k} \frac{2^{rel_i} -
   1}{\log_2(i+1)}$. Similarly RRF $\text{score}(d) = \sum_q \frac{1}{k +
   rank_q(d)}$ is referenced but not defined. *Propose:* a "Metrics
   primer" sub-section in §36.3 (or a new Appendix A.X reference) with NDCG,
   MRR, MAP, Recall@k formulas + the BM25 score $\text{BM25}(q, d) = \sum_t
   IDF(t) \cdot \frac{f(t,d)(k_1+1)}{f(t,d) + k_1(1 - b + b \cdot |d|/avgdl)}$
   with one numeric worked example. Size: 1 sub-section (~600 words) or 1
   appendix.

4. **[HIGH, Ch 56] No formal definition of any fairness metric.** §56.2
   discusses disparate impact, demographic parity, equalized odds, calibration
   conceptually, but never writes the formulas (e.g., demographic parity
   $P(\hat{Y}=1|A=0) = P(\hat{Y}=1|A=1)$, equalized odds adds $P(\hat{Y}=1|A=a,Y=y)$
   equality, the 4/5ths rule cutoff 0.80). §56.2.8 even notes that "different
   libraries disagree by 1-3 percentage points" without showing where the
   disagreement comes from (rounding, tie-breaking, NaN handling). *Propose:* a
   "Fairness metric primer" sub-section in §56.2 with the 4-6 canonical formulas
   plus a worked numeric example on a toy 1000-row dataset showing
   demographic-parity-vs-equalized-odds tension. Connection to Kleinberg /
   Chouldechova impossibility theorem. Size: 1 sub-section (~800 words).

5. **[HIGH, Ch 56] No mention of the fairness impossibility theorem.** §56.3
   mentions COMPAS teaches the "fairness-vs-calibration trade-off" but never
   states Kleinberg-Mullainathan-Raghavan / Chouldechova 2016 formally:
   calibration, balance-for-positive-class, and balance-for-negative-class
   cannot all hold simultaneously when base rates differ across groups. This is
   the most consequential theoretical result in the field and is missing.
   *Propose:* a key-insight callout in §56.3 (or §56.2) stating the theorem in
   plain prose with the 3-condition formulation and a one-paragraph sketch.
   Size: 1 callout (~250 words).

6. **[HIGH, Ch 56] No DP $(\epsilon, \delta)$ math.** §56.2.7 mentions DP-SGD
   and Opacus but never defines the $(\epsilon, \delta)$-DP bound
   $\Pr[M(D) \in S] \le e^\epsilon \Pr[M(D') \in S] + \delta$ or the Gaussian
   mechanism noise scale $\sigma \ge c \cdot \Delta_2 / \epsilon$ that Opacus
   actually applies. Practitioners will set $\epsilon$ without intuition for
   what it bounds. *Propose:* key-insight callout in §56.2 with the DP
   definition, Gaussian mechanism noise scale, and typical $\epsilon$ ranges
   in published LLM work (e.g., $\epsilon=8$ for production NLP per Apple/Google
   disclosures). Size: 1 callout (~250 words).

7. **[HIGH, Ch 41] No latency budget arithmetic for voice agents.** §41.1.3
   says GPT-4o Realtime "collapses the cascade's 500-1000ms turn cost to ~300ms"
   but the underlying budget (mic capture 10-30ms, VAD 100-200ms, network RTT
   50-100ms, STT 100-300ms, LLM TTFT 200-600ms, TTS first-audio 80-200ms,
   network return 50-100ms, jitter buffer 20-60ms) is never decomposed.
   *Propose:* a budget table + worked example in §41.1.3 (or §41.4.2) showing
   how a 300ms target gets allocated across pipeline stages, plus the
   speech-to-speech advantage (no intermediate text serialization). Connection
   to telephony industry's "300ms is the threshold of perceived turn-taking
   awkwardness" (Brady 1968, Heldner & Edlund 2010). Size: 1 callout + 1
   small table (~400 words).

8. **[HIGH, Ch 59 / 61] No FP8 numerical-precision math.** §59.5 mentions FP8
   training and TF-Engine; §61.2 mentions Transformer Engine. Neither shows
   what FP8 actually is (E4M3 vs E5M2 formats, per-tensor or per-block scale
   factors, why E4M3 forward and E5M2 backward), the loss curve sensitivity,
   or the relationship to BF16. This is a direct parallel to the §9.1
   quantization treatment that *does* show numeric precision math. *Propose:*
   a §59.5.X sub-section "What FP8 actually is" with the bit layouts, dynamic
   range, scaling-factor recipe, and a 2-3 row comparison table BF16 vs FP16
   vs FP8-E4M3 vs INT8. Size: 1 sub-section (~600 words).

9. **[MEDIUM, Ch 36] No connection between dense retrieval and classical IR's
   probabilistic foundation.** §36.3 surveys benchmarks but never connects
   modern bi-encoder retrieval to BM25's roots in the probabilistic relevance
   framework (Robertson 1976), or to LSA / LSI's SVD-based latent semantic
   space (Deerwester 1990) which is the actual mathematical ancestor of dense
   embeddings. Without this, a reader cannot place dense retrieval in the
   60-year IR lineage. *Propose:* a "History matters" key-insight callout in
   §36.1 connecting tf-idf -> BM25 -> LSI -> word2vec -> BERT-base-dense,
   showing the through-line. Size: 1 callout (~300 words).

10. **[MEDIUM, Ch 61 / 59] No memory-bandwidth roofline analysis.** §61.1
    discusses MFU but doesn't introduce the roofline model that explains
    *why* MFU on dense LLMs is capped at 35-55% on H100 BF16. The
    arithmetic intensity ratio (FLOPs per byte of memory traffic) for matmul
    is bounded by tile size, and below the machine balance ($M_b = $ peak
    FLOPs / peak HBM bandwidth $\approx 600$ FLOPs/byte for H100) you are
    bandwidth-bound. This is *the* fundamental constraint and is implicit
    everywhere. *Propose:* a roofline-model callout in §59.5 or §61.1 with the
    H100 roofline (peak BF16 ~989 TFLOPS, HBM3 bandwidth ~3.35 TB/s, machine
    balance ~295 FLOPs/byte) and Llama-3 70B's arithmetic intensity per layer.
    Size: 1 sub-section or large callout (~500 words).

## Per-chapter findings

### Chapter 36 - Retrieval Tools (Part VII)

Overall: comprehensive vendor coverage, strong relative-comparison prose,
strong selection criteria. **Depth bar: NOT MET on math, partially met on
worked examples.** 4 callouts/section, **0 math expressions per section** vs.
600+ in depth bar. Files: `E:\Projects\BookBlogsHome\LLMBook\part-7-retrieval-information-extraction-with-llms\module-36-retrieval-tools\section-36.*.html`.

- **section-36.1 (Platforms): depth-bar PARTIAL.**
  - Strong: 4-bucket taxonomy, decision tree, pricing-shape analysis, 12 platforms with crisp pick-when, ops/backup/DR discussion, table comparison.
  - Gap (HIGH): no quantitative recall-vs-latency curves. Pinecone vs Qdrant
    vs Weaviate is compared on capability axes, not on
    NDCG-vs-QPS. *Insert:* numeric callout from ANN-Benchmarks public results
    (e.g., HNSW M=16 efC=200 achieves 0.95 recall@10 at ~5000 QPS on Glove-100;
    IVF-Flat nprobe=8 achieves 0.85 recall at ~12000 QPS; IVF-PQ-16 achieves
    0.80 recall at ~30000 QPS at 8x memory savings). 1 paragraph.
  - Gap (HIGH): no big-O / complexity analysis. HNSW is $O(M \log N)$ insertion,
    $O(\log N)$ query; IVF-PQ is $O(N/n_{list} \cdot D + k \cdot D')$ per query.
    Neither stated. *Insert:* 1-paragraph "Complexity at a glance" callout
    with the three canonical bounds.
  - Gap (MEDIUM): no connection to classical IR. BM25 is described as a hybrid
    component but the formula is not given (HIGH gap 3 above).
  - Gap (MEDIUM): no quantization math. §36.1.8 says BQ cuts memory 32x but
    doesn't show that BQ stores `sign(x_i)` per dimension and recall is preserved
    because cosine similarity in BQ space approximates angular similarity in
    full precision (Charikar 2002 / SimHash). *Insert:* 1-paragraph callout.

- **section-36.2 (Libraries and Frameworks): depth-bar PARTIAL.**
  - Strong: clean stack-layering by family, thinnest-viable-stack section.
  - Gap (HIGH): no RRF formula. RRF default $k=60$ is mentioned 3 times but
    the equation $\text{score}(d) = \sum_q \frac{1}{k + \text{rank}_q(d)}$ never
    appears. *Insert:* 1 callout (~150 words) with the formula and a
    2-retriever worked example.
  - Gap (MEDIUM): no chunking ablation numbers. §36.2.10 says "structure-aware
    chunking gives 3-8 NDCG points over fixed-size" but doesn't cite the
    Anthropic contextual-retrieval blog's actual numbers (49% retrieval-failure
    reduction with contextual retrieval + BM25, 67% with rerank). *Insert:* a
    short numeric table with the Anthropic ablation results.

- **section-36.3 (Datasets and Benchmarks): depth-bar PARTIAL.**
  - Strong: 4-tier benchmark taxonomy, contamination warnings, in-domain eval
    methodology.
  - Gap (HIGH): no metric formulas (HIGH gap 3 above). NDCG, MRR, MAP, Recall@k,
    EM, F1, faithfulness are all named but only conceptually defined.
  - Gap (MEDIUM): no derivation of why BM25 + dense beats either alone. The
    "BM25 still beats half of dense retrievers on BEIR" callout is great but
    the why (lexical exact-match captures rare terms that dense models embed
    into the centroid of frequent neighbors) is not explained. *Insert:* a
    key-insight callout drawing on Thakur 2021 + Sciavolino 2021 (entity-rare
    questions).

- **section-36.4 (Models): depth-bar PARTIAL.**
  - Strong: model-by-model comparison with dimensions, context length, license;
    matryoshka discussion; license traps callout; fine-tuning recipe.
  - Gap (HIGH): no Matryoshka math (HIGH gap 2 above).
  - Gap (HIGH): no late-interaction MaxSim formula. ColBERT MaxSim
    $s(q,d) = \sum_{i \in |q|} \max_{j \in |d|} q_i \cdot d_j$ is referenced
    but never written. *Insert:* a callout with the formula and complexity
    analysis (storage $O(|d| \cdot d_{\text{tok}})$ vs single-vector $O(d)$;
    score $O(|q| \cdot |d|)$ per pair).
  - Gap (MEDIUM): contrastive-loss derivation absent. §36.4.10 fine-tuning recipe
    mentions "contrastive loss with hard negatives" without writing
    $\mathcal{L}_{\text{InfoNCE}} = -\log \frac{\exp(s(q, d^+)/\tau)}{\sum
    \exp(s(q, d_i)/\tau)}$ or explaining the role of temperature $\tau$ and
    hard-negative count. *Insert:* a key-insight callout with the InfoNCE
    formula.

- **section-36.5 (External Reading): purpose-appropriate.**
  - This section is curated bibliography by design; the depth-bar criteria don't
    fully apply. No changes needed.

### Chapter 41 - Conversational AI Tools (Part VIII)

Overall: similar shape to Ch 36, comprehensive vendor coverage, no math.
**Depth bar: NOT MET on math.** 3-4 callouts/section, **0 math expressions per
section**. Files: `E:\Projects\BookBlogsHome\LLMBook\part-8-conversational-ai-with-llms\module-41-conv-ai-tools\section-41.*.html`.

- **section-41.1 (Platforms): depth-bar PARTIAL.**
  - Strong: 4-bucket landscape, build-vs-buy 2022-vs-2026 evolution, vertical map.
  - Gap (HIGH): no latency budget arithmetic (HIGH gap 7 above). Voice agents
    are discussed without ever stating the budget breakdown.
  - Gap (MEDIUM): no formal grounding in dialog-state-tracking theory. CALM is
    summarized as "LLM understands, deterministic policy executes" but the
    underlying belief-state representation (POMDP for the classical era;
    structured-output command generation for the LLM era) is not connected to
    the dialogue-systems literature (Young et al. 2013 POMDP-SDS, Williams &
    Young 2007 partial-observability formulation). *Insert:* 1-paragraph
    callout linking modern command-generation back to POMDP belief tracking.
  - Gap (LOW): no Markov-vs-stateful comparison. The flat-intent vs state-machine
    debate is left implicit; making it explicit (intent classifier is an
    n=1 Markov assumption; flow-graph is full HMM) would help.

- **section-41.2 (Libraries and Frameworks): depth-bar PARTIAL.**
  - Strong: stack layering by family, framework abstraction warnings.
  - Gap (MEDIUM): conversation-memory architectures (ring buffer, summary,
    retrieval-augmented, episodic) not compared with capacity / latency math.
    A 100-turn conversation at 50 tokens/turn is 5K tokens of history; how
    that interacts with a 128K context window vs a summarizer should be
    quantified. *Insert:* 1 small table comparing memory strategies with
    storage costs and context-utilization trade-offs.
  - Gap (LOW): no async-event-loop architecture diagram for realtime voice
    agents. Pipecat/LiveKit Agents are described abstractly but the dataflow
    (mic frames -> VAD -> chunked STT -> LLM stream -> incremental TTS -> mux
    out) is left implicit.

- **section-41.3 (Datasets and Benchmarks): depth-bar PARTIAL.**
  - Strong: 5-era taxonomy of conversation eval, judge-bias discussion.
  - Gap (HIGH): no math on Elo / Bradley-Terry. LMSYS Arena is the headline
    benchmark; the Bradley-Terry model $P(i \succ j) = \sigma(r_i - r_j)$ and
    the Elo update rule are foundational. *Insert:* a key-insight callout
    with the Bradley-Terry formula and a sentence on why crowd ratings
    underestimate confidence intervals (need ~50k pairwise comparisons for
    stable top-10 ranking).
  - Gap (MEDIUM): no LLM-as-judge bias quantification. The chapter warns
    against length-bias / position-bias / self-enhancement bias but does not
    show that AlpacaEval-LC corrects length bias via length-controlled
    regression (Dubois et al. 2024 actually provides the formula). *Insert:*
    a callout summarizing the four canonical judge biases with
    correction methods.

- **section-41.4 (Models): depth-bar PARTIAL.**
  - Strong: 4-tier conversational-model taxonomy, character vs assistant split.
  - Gap (MEDIUM): no RLHF / DPO / Constitutional AI loss equations. Chat
    quality differences are attributed to "heavy RLHF" and "Constitutional AI
    fine-tuning" but the underlying objectives are not shown
    ($\mathcal{L}_{\text{DPO}} = -\log \sigma(\beta(\log \pi(y_w|x)/\pi_{\text{ref}}(y_w|x)
    - \log \pi(y_l|x)/\pi_{\text{ref}}(y_l|x)))$ for DPO; the
    constitutional-AI self-critique loop for CAI). *Insert:* a key-insight
    callout or pointer to Ch 18 (RLHF) with the DPO formula.
  - Gap (MEDIUM): voice-aware models discussion does not connect to the
    cascaded-vs-end-to-end speech recognition literature (Graves 2012, Chan
    et al. 2016 LAS, Radford 2022 Whisper). The architectural lineage is
    invisible.

- **section-41.5 (External Reading): purpose-appropriate.**

### Chapter 56 - Responsible AI Tools (Part XI)

Overall: comprehensive coverage of governance / observability / safety / OS
stacks; regulation-driven and well-organized. **Depth bar: NOT MET on math
or formal foundations.** 3-5 callouts/section, **0 math expressions per
section**. Files: `E:\Projects\BookBlogsHome\LLMBook\part-11-llm-ethics-trust-governance\module-56-responsible-ai-tools\section-56.*.html`.

- **section-56.1 (Platforms): depth-bar PARTIAL.**
  - Strong: 5-bucket taxonomy aligned to regulation, 4-buyer-persona map,
    vendor-stability warnings, vertical-specific recommendations.
  - Gap (MEDIUM): no NIST AI RMF / EU AI Act *quantitative* risk-tier
    examples. The risk categories (minimal / limited / high / unacceptable)
    are named but not anchored with example use cases and tier-specific
    obligations. *Insert:* a small table mapping concrete example use cases
    to risk tier + required artifacts (model card, FRIA, conformity assessment,
    post-market monitoring).

- **section-56.2 (Libraries and Frameworks): depth-bar PARTIAL.**
  - Strong: 6-layer library taxonomy, fairness-library-disagreement callout.
  - Gap (HIGH): no formal fairness definitions (HIGH gap 4 above). Disparate
    impact, demographic parity, equalized odds, equal opportunity, calibration
    are all named but never written down.
  - Gap (HIGH): no DP $(\epsilon, \delta)$ math (HIGH gap 6 above).
  - Gap (HIGH): SHAP / Shapley value formula absent. SHAP is named
    "mathematically principled" but the formula
    $\phi_i = \sum_{S \subseteq F \setminus \{i\}}
    \frac{|S|!(|F|-|S|-1)!}{|F|!} [v(S \cup \{i\}) - v(S)]$ never appears.
    *Insert:* a key-insight callout with the Shapley-value formula, the four
    axioms (efficiency, symmetry, dummy, additivity), and the KernelSHAP /
    TreeSHAP computational complexity contrast.
  - Gap (MEDIUM): no Kirchenbauer watermark math. The "green-list / red-list"
    is described conceptually; the actual scheme (for each token,
    pseudo-randomly partition vocab into green/red via a seed from previous
    token; bias logits by $\delta$ toward green; detect by counting green
    tokens via $z$-statistic) is opaque. *Insert:* 1 paragraph + formula
    callout.

- **section-56.3 (Datasets and Benchmarks): depth-bar PARTIAL.**
  - Strong: 6-family benchmark taxonomy, evaluation-stack recipe.
  - Gap (HIGH): impossibility theorem not stated (HIGH gap 5 above).
  - Gap (MEDIUM): no relation between toxicity benchmarks and the underlying
    classification metric noise (Civil Comments' Cohen's kappa, Perspective
    API's published precision/recall). The user does not learn that
    "toxicity score 0.7" depends on calibration and that thresholds are
    deployment-specific. *Insert:* 1 short callout on classifier
    calibration / kappa.

- **section-56.4 (Models): depth-bar PARTIAL.**
  - Strong: 5-family taxonomy of safety models, Llama Guard + Granite +
    ShieldGemma + WildGuard catalog, watermark-vs-stats-detection warning.
  - Gap (MEDIUM): no recall/precision numbers for safety classifiers. Llama
    Guard 3 / 4, Granite Guardian, ShieldGemma are compared on category
    coverage but the user does not see "Llama Guard 4 achieves F1=0.89 on
    HarmBench, Granite Guardian 0.85, ShieldGemma 0.83" or similar published
    numbers. *Insert:* a benchmark comparison table.
  - Gap (MEDIUM): no derivation of why statistical AI-detection fails. The
    warning is strong but the reason (Sadasivan et al. 2023 lower-bound:
    optimal detector AUC -> 0.5 as $\|\Delta_{\text{TV}}(p_{\text{AI}},
    p_{\text{human}})\| \to 0$, which paraphrasing achieves) is not given.
    *Insert:* a key-insight callout sketching the impossibility argument.

- **section-56.5 (External Reading): purpose-appropriate.**

### Chapter 59 - Distributed Training Systems (Part XII)

Overall: **this is the chapter that CLEARS the depth bar.** Files:
`E:\Projects\BookBlogsHome\LLMBook\part-12-llm-systems-at-scale\module-59-distributed-training-systems\section-59.*.html`.
Equations, code, diagrams, worked examples are present throughout. The
remaining gaps are polish, not structural.

- **section-59.1 (Distributed Training Fundamentals): depth-bar HIT.**
  - Strong: 3-axes-of-parallelism, collective primitives with bytes-moved
    table, ring all-reduce derivation $B_{\text{ring}} = 2(N-1)S/N \to 2S$,
    BSP-vs-async comparison, complete DDP code listing, memory accounting
    $M_{\text{state}} = 18P$ bytes for AdamW, McCandlish gradient-noise-scale
    reference, Valiant BSP 1990 citation. Information-theory and
    parallel-systems-research cross-field connection: present.
  - Minor gap (LOW): the tree all-reduce $O(\log N)$ alternative is mentioned
    but the actual crossover-point formula (latency $\alpha + \beta S$ for
    tree vs ring; switch when $\alpha N \gtrsim \beta S$) is not given.
    *Insert:* 1-sentence formula in §59.1.3.2.
  - Minor gap (LOW): SGD noise scale $B^* = \text{tr}(H \Sigma_g) / G^T H G$
    (McCandlish et al. 2018) is referenced informally; the formula is not
    stated. *Insert:* 1 key-insight callout (~150 words).

- **section-59.2 (ZeRO and FSDP): depth-bar HIT.**
  - Strong: per-rank memory accounting $16/N$ B/param by stage, hybrid-shard
    derivation, FSDP code listing, prefetching trick, FSDP-vs-TP trade-off
    matrix. Llama-3 405B worked example.
  - Minor gap (LOW): no discussion of FSDP's data-loader-sampler bookkeeping
    interaction with checkpoint resume (covered in §59.5 but a forward link
    would help).

- **section-59.3 (Megatron-LM and Tensor Parallelism): depth-bar HIT.**
  - Strong: column-/row-parallel matrix decomposition, $f$ and $g$ collective
    operators, MLP and attention block breakdowns, MQA/GQA interaction,
    minimal TP code listing.
  - Minor gap (LOW): sequence parallelism is mentioned but the activation
    memory reduction $A \to A/T$ via sequence sharding is not quantified
    end-to-end (it would close the analytic loop on TP + SP saving the full
    $T \times$ activation budget). *Insert:* 1 paragraph with explicit
    activation-memory before/after.
  - Minor gap (LOW): context parallelism (ring attention, DeepSpeed-Ulysses)
    is not differentiated from tensor parallelism. *Insert:* a 1-paragraph
    callout distinguishing the two axes.

- **section-59.4 (Pipeline Parallelism): depth-bar HIT.**
  - Strong: GPipe vs 1F1B vs interleaved-1F1B vs zero-bubble schedules with
    figure, bubble fraction $(P-1)/M$ formula, 3D-parallelism composition.
  - Minor gap (LOW): the zero-bubble schedule (Qi et al. 2023) is mentioned
    by name; the underlying trick (split backward into B-grad and B-weight,
    schedule independently) is not explained. *Insert:* 1 paragraph.

- **section-59.5 (Production Training Infrastructure): depth-bar HIT.**
  - Strong: real-world MTBF table (OPT, BLOOM, Llama-3), checkpoint-cadence
    optimization $T^* = \sqrt{2C\tau}$, MFU formula, NCCL flame-graph
    pathological patterns, three real post-mortems with specific findings.
  - Gap (MEDIUM): the FP8 numerical-precision math gap (HIGH gap 8 above) is
    most naturally inserted here. The §59.5.4.1 MFU formula mentions "FP8
    training lifts the ceiling" without explaining what FP8 is. *Insert:* a
    §59.5.X sub-section "What FP8 actually is" with E4M3 / E5M2 bit layouts,
    scaling-factor recipe, and BF16 / FP16 / FP8 / INT8 comparison table.
  - Minor gap (LOW): roofline model not introduced (HIGH gap 10 above; would
    fit in §59.5 or §61.1).

### Chapter 61 - Scale Tools (Part XII)

Overall: comprehensive coverage of cloud / scheduler / storage / framework
stack with real 2026 prices, MFU discussion, frontier-lab disclosures.
**Depth bar: NOT MET on math, partially met on numbers (pricing is concrete).**
2-3 callouts/section, **0 math expressions per section**. Files:
`E:\Projects\BookBlogsHome\LLMBook\part-12-llm-systems-at-scale\module-61-scale-tools\section-61.*.html`.

- **section-61.1 (Platforms): depth-bar PARTIAL.**
  - Strong: 4-bucket taxonomy of clouds, frontier-lab disclosures
    (Stargate, Colossus, Llama-3 cluster), pricing-shape analysis,
    parallel-storage taxonomy, training-vs-serving-platform split.
  - Gap (HIGH): no roofline model (HIGH gap 10 above). Most natural insertion
    point in §61.1 (or §59.5).
  - Gap (MEDIUM): InfiniBand vs RoCE vs Ethernet bandwidth math is informal
    ("InfiniBand HDR is 200 Gbps, NDR 400 Gbps") but the impact on MFU is
    discussed only qualitatively. *Insert:* a "scaling efficiency vs
    interconnect bandwidth" sub-callout showing how the per-step communication
    time $T_{\text{comm}} = \frac{2 P_{\text{shard}} \cdot 2}{B_{\text{eff}}}$
    relates to MFU loss, with 3-row table (100G Ethernet, 400G IB, 800G IB).
  - Gap (LOW): InfiniBand topology discussion (fat-tree, rail-optimized) is
    qualitative; the bisection-bandwidth formula $B_{\text{bisect}} = (N/2)
    \cdot B_{\text{link}}$ for non-oversubscribed fat-tree would anchor the
    "oversubscription 2:1 means cross-cluster all-reduce halves" intuition.

- **section-61.2 (Libraries and Frameworks): depth-bar PARTIAL.**
  - Strong: 6-layer library taxonomy, stack-composition patterns, MFU-as-
    success-metric callout.
  - Gap (HIGH): no FP8 math (HIGH gap 8 above). FP8 is mentioned in TE,
    MS-AMP, FA3, but the actual format never appears.
  - Gap (MEDIUM): Flash Attention's IO-aware tiling is summarized as "O(N^2)
    FLOPs, O(N) memory by tiling the softmax", but the actual block-wise
    online-softmax derivation (Dao et al. 2022 eq. 7-9) is not shown. *Insert:*
    a key-insight callout with the recurrence
    $m_i = \max(m_{i-1}, m_{S_i}^{\text{block}})$,
    $\ell_i = e^{m_{i-1} - m_i} \ell_{i-1} + e^{m_{S_i}^{\text{block}} - m_i}
    \ell_{S_i}^{\text{block}}$. This is one of the most important algorithmic
    contributions of 2022-2024 and is too important to leave at the marketing
    level.
  - Gap (LOW): Triton vs CUDA programming model comparison is qualitative; an
    example of a fused-softmax Triton kernel (~20 lines) would anchor the
    abstraction level.

- **section-61.3 (Datasets and Benchmarks): depth-bar PARTIAL.** (Scaling /
  systems benchmarks)
  - Reviewed lightly; appears similar in shape to 61.1/61.2: comprehensive
    catalog but no quantitative analysis of e.g. SPECfp-like compute benchmarks
    or MLPerf training scoring methodology.
  - Gap (LOW): MLPerf scoring formula (geomean across reference normalizations)
    not stated.

- **section-61.4 (Models): depth-bar PARTIAL.**
  - Reviewed lightly; covers scaling-relevant model catalog.
  - Gap (LOW): no scaling-law-derived guidance on which models fit at which
    cluster sizes. §6.3 already gives Chinchilla scaling; a forward link from
    §61.4 to §6.3 plus a one-table summary of compute-optimal model sizes
    for typical compute budgets would close the loop.

- **section-61.5 (External Reading): purpose-appropriate.**

### Wave 17i consolidated sections

These are substantive content sections (not tools-of-the-trade format), so the
depth bar applies more directly. Files reviewed:

- **section-24.6 (VLA models, Part V):** small (20 KB). Substantive but no
  math. Depth-bar PARTIAL.
- **section-24.13 (VLA models):** 32 KB. Substantive but no math. Depth-bar
  PARTIAL.
- **section-26.6 (Agent Safety, Part VI):** 42 KB. Substantive but no math.
  Depth-bar PARTIAL.
  - Gap (MEDIUM): formal threat-model definitions (CIA triad applied to
    agents; attack-tree formalism) are not given. *Insert:* a callout linking
    agent safety to classical computer-security formalism.
- **section-27.5 (Tool Use Protocols):** 30 KB. Substantive but no math.
  Depth-bar PARTIAL.
- **section-29.1 (Code Agents):** 44 KB. The strongest Wave 17i section.
  Strong on patterns (self-debug loop, plan-execute, tree-of-code), SWE-bench
  evaluation numbers, real generations. Depth-bar PARTIAL.
  - Gap (MEDIUM): no convergence-rate argument for self-debug loops. The
    empirical observation that "k=3-5 self-debug attempts saturates SWE-bench
    improvement" is given but not connected to a fixed-point convergence
    analysis or a martingale view of iterative correction.
- **section-29.4 (Production Coding Systems):** 75 KB. Largest. Comprehensive
  product survey with CLAUDE.md, hooks, sub-agents. Depth-bar PARTIAL.
- **section-35.2 (KG-RAG):** 64 KB. Substantive on RDF vs property graphs,
  Cypher, graph embeddings. Depth-bar PARTIAL.
  - Gap (MEDIUM): graph-embedding equations missing. TransE
    $\|h + r - t\|$ minimization, DistMult bilinear scoring, ComplEx complex
    embeddings are named but the loss functions are not given.
- **section-35.3 (GraphRAG):** 53 KB. Microsoft GraphRAG, community detection,
  Leiden. Depth-bar PARTIAL.
  - Gap (MEDIUM): Leiden community-detection algorithm (Traag et al. 2019)
    referenced but modularity Q definition missing. *Insert:* the modularity
    formula $Q = \frac{1}{2m} \sum_{ij}[A_{ij} - \frac{k_i k_j}{2m}]
    \delta(c_i, c_j)$ and a one-paragraph explanation.
- **section-37.3 (Building Steering):** 209 KB (very large). Reviewed lightly.
  This is comprehensive product/UX patterns; the math-content gap matches the
  other tools-of-the-trade sections.

## Cross-chapter patterns

Several systemic gaps recur across all the new tools chapters. Fixing them in
a coordinated way (e.g., as appendix references rather than per-chapter
inserts) would lift the whole batch.

1. **No metric formulas anywhere.** NDCG, MRR, Recall@k, BM25, RRF, Cohen's
   kappa, Krippendorff's alpha, MFU, Elo / Bradley-Terry, demographic parity,
   equalized odds, $(\epsilon, \delta)$-DP, attack success rate, faithfulness
   are *all named multiple times* but never defined. **Recommendation:**
   create or extend Appendix A.7 ("Evaluation Metrics Reference") with all the
   canonical formulas plus 1-row worked examples; replace per-chapter
   definitions with a single appendix cross-link.

2. **No theoretical-impossibility statements.** Fairness impossibility theorem
   (Kleinberg/Chouldechova), AI-detection impossibility (Sadasivan), the
   universal-approximation/expressivity bounds for transformers, the recall
   floor for sub-linear ANN: all are missing. **Recommendation:** a
   "Foundational impossibility results" sub-section in the appendix or in
   the relevant Part introduction.

3. **No connection to classical theory.** Classical IR (Robertson, Sparck-Jones,
   LSI), POMDP dialog (Young, Williams), parallel computing (Valiant BSP, Patarasuk-Yuan,
   Sutton & Barto for RLHF), differential privacy theory (Dwork), Shapley
   value (Shapley 1953) are mostly absent. The depth-bar sections routinely
   make these connections; the new chapters do not.

4. **Cross-references underweight.** Most tools chapters internally
   cross-reference (Section X.Y) but rarely reach into Part II (theory) or
   Part IV (training) where the canonical mathematical foundations live.
   Section 36.4 should cross-link to Section 17.1 (LoRA) when discussing
   fine-tuning, to Section 9.1 (quantization) when discussing matryoshka, to
   Section 8.x (information theory) for InfoNCE; etc. Similar pattern for 41
   and 56.

5. **The "Tools of the Trade" template itself is the design tension.** These
   chapters are *intended* as practitioner-facing catalogs. The depth-bar
   sections are *intended* as foundational pedagogy. A hybrid pattern would
   be: keep the catalog-prose body, add 1-2 "Foundations" callouts per section
   referencing the relevant Part II / Part IV mathematical material. This
   gives the catalog chapters a depth surface without rewriting their voice.

## Overall assessment of new content's depth vs canonical depth

- **Chapter 59 is at canonical depth.** All five sections clear the §3.1 /
  §6.3 / §9.1 / §17.1 bar. They could be moved to Part II / Part IV without
  embarrassment. Inserting them was a substantial uplift to the book.

- **Chapter 36 / 41 / 56 / 61 are intentionally shallower** by design, as
  practitioner catalogs. They are well-written *for that format*: clear pick-
  when guidance, vendor coverage current to mid-2026, decision trees, vertical-
  by-vertical maps, pricing-shape analyses. The depth shortfall is in
  *mathematical foundations* rather than in coverage, prose quality, or
  utility. The right remediation is targeted insertion of formal callouts
  (NDCG, BM25, RRF, fairness metrics, DP epsilon, MaxSim, Matryoshka loss,
  SHAP, Bradley-Terry, FP8 layouts, roofline) plus more aggressive cross-
  linking to the Part II / Part IV foundations.

- **Wave 17i consolidated sections** sit between: substantive content sections
  with the catalog-style avoidance of math. They benefit most from
  retrospective formula insertion (graph embeddings, modularity, self-debug
  convergence).

- A practical heuristic for prioritization: **insert math at the moment a
  practitioner would need it to make a decision.** "Pick HNSW vs IVF-PQ" is
  decision-shaped; here, recall-latency numbers and complexity bounds
  materially help. "Pick Llama Guard vs Granite Guardian" is also
  decision-shaped; F1 / FPR / FNR numbers materially help. The current
  chapters tell readers *which tool to pick*; the depth uplift is to also
  show *why* the trade-off curve has the shape it does.

## Estimated remediation effort

- Ch 36: 5 callouts + 1 sub-section (~3-4 days)
- Ch 41: 4 callouts + 1 sub-section (~2-3 days)
- Ch 56: 6 callouts + 2 sub-sections (~4-5 days)
- Ch 59: 3 callouts + 1 sub-section (~1-2 days)
- Ch 61: 3 callouts + 1 sub-section (~2-3 days)
- Appendix A.7 (Metrics Reference): 1 new appendix section (~3-4 days)
- Wave 17i selected inserts: 4-6 callouts (~2-3 days)
- Total: ~17-25 days of focused authoring for an experienced author
  comfortable with both the systems-research lineage and the pedagogical
  voice of the canonical depth-bar sections.
