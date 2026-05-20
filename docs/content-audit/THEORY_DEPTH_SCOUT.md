# Theory Depth Scout

Read-only scout (2026-05-19) of every section file under `part-*/module-*/section-*.html`
for opportunities to add deeper theory, named methods, algorithmic specificity,
and explicit mathematical formalism. No HTML was modified. The follow-on pass
selects which to apply.

The scout examines each section against five depth dimensions:

1. **Theory depth.** Does the section explain WHY a method works (e.g., the
   retrieval distillation objective for DPR, the Q/K/V derivation for attention,
   the Hessian-inverse update for SparseGPT), not just HOW?
2. **Algorithmic specificity.** Does the section show the actual algorithm
   (pseudocode, complexity bound, optimization tradeoff) or describe it only
   in prose?
3. **Named models / methods.** Are canonical implementations named? (RAG should
   name DPR + ColBERT + BGE + SPLADE; scaling laws should name Kaplan + Chinchilla
   + Sardana; reasoning should name o1 + R1 + GRPO + PRM.)
4. **Mathematical formalism.** Are key equations actually written out with
   proper notation (softmax temperature, KL divergence, cross-entropy,
   InfoNCE, log-likelihood, etc.)?
5. **Comparative depth.** Are alternative approaches compared with concrete
   metrics, or just mentioned?

A composite depth score (0-5) is computed per section from these signals.
**Depth 5** is research-paper depth (sections 3.1, 6.3, 8.1, 8.3, 8.5, 9.2,
9.3, 9.7, 18.1a, 18.2a, 31.2a, 49.1, 50.1, 53.2, 55.1, 75.3 are the
benchmarks). **Depth 0** is conversational prose with no formal content.

Skipped: every `module-*-tools-of-the-trade` and equivalent (Platforms,
Libraries, Datasets, Models, External Reading subsections of catalog modules:
05, 14, 19.x, 23 catalog, 25, 29, 30, 36, 41, 45, 46-judge, 51, 56, 61, 66
catalog, 74, 78). Application-vertical chapters (67-73) are also low-depth
by design; only the architecture sub-sections within them are flagged.

## 1. Executive Summary

| Bucket | Count | Notes |
|---|---:|---|
| Total section files scanned | 443 | matches `find part-*/module-*/section-*.html` |
| In-scope (non-tools-catalog, non-appendix) | 412 | scope for this scout |
| Depth 5 (research-paper, no upgrade needed) | 22 | benchmark sections |
| Depth 4 (one missing layer) | 31 | low-effort polish opportunities |
| Depth 3 (mid, often missing math or named comparators) | 32 | targeted theory boxes would lift each one band |
| Depth 2 (named methods mentioned, no derivation) | 116 | the biggest payoff bucket |
| Depth 1 (concept-level only) | 75 | second-biggest opportunity |
| Depth 0 (operations / catalog / survey, intentionally light) | 136 | most are correctly light; ~30 of these are mis-classified |

**Observed pattern.** The book has two characteristic shapes:

- *Spike-deep + valley-shallow.* Each Part has 2-4 marquee sections at
  depth 5 (the "deep dives") and the rest at depth 1-2. The deep dives are
  excellent; the shallow neighbors leave canonical theory un-stated and
  defer everything to citations.
- *Named without derived.* Many sections name 10-50+ canonical methods
  (`section-17.1` LoRA names 141 methods; `section-7.2` names 7+; `section-17.4`
  names 42) but include zero algorithm callouts and zero math blocks. The
  same is true in `section-9.5` (Pruning, names SparseGPT and Wanda but no
  formulas) and `section-22.1` (ViT, no patch-embedding equation).

The strongest single class of high-payoff upgrade is therefore a numbered
**Algorithm callout + 1-2 inline equations** added to ~30 to 50 sections that
already have the right scaffolding (named methods + figure + code example)
but no canonical formal statement.

## 2. Top 30 Highest-Payoff Candidates

Ranked by (gap severity x importance of topic x ease of adding depth).
"Topic importance" reflects how often the section is cited from other chapters
and how foundational it is to the book's curriculum.

| # | Section | Current depth | Top depth add (1-line) |
|---:|---|---:|---|
| 1 | `part-1-llm-building-blocks/module-01-foundations-nlp-text-representation/section-1.6.html` (Subword Tokenization Algorithms) | 2.5 | Algorithm callouts for BPE training (merge loop), WordPiece (likelihood-based merge), and Viterbi segmentation under Unigram; explicit Shannon code-length argument |
| 2 | `part-1-llm-building-blocks/module-04-decoding-text-generation/section-4.2.html` (Stochastic Sampling) | 2.0 | Algorithm callouts for top-p, top-k, min-p, temperature-shifted softmax, repetition/frequency/presence penalties (formulas already in `SCIENTIFIC_DEPTH_OPPORTUNITIES.md` from 2024) |
| 3 | `part-2-understanding-llms/module-08-reasoning-test-time-compute/section-8.2.html` (o1, o3, R1, QwQ) | 1.25 | Add the GRPO objective restatement next to R1 description; show the difference between hidden-CoT (o-series) and visible-CoT (R1) at training-objective level; PRM vs ORM contrast box |
| 4 | `part-2-understanding-llms/module-09-inference-optimization/section-9.7.html` (Pruning & Sparsity) | 1.5 | Algorithm callout for SparseGPT (Hessian-inverse weight update across columns) and Wanda (importance = `|w_ij| * ‖x_j‖`); 2:4 sparsity mask construction |
| 5 | `part-2-understanding-llms/module-09-inference-optimization/section-9.5.html` (vLLM/Serving Stack) | 1.5 | Algorithm callout for continuous batching scheduler and PagedAttention block-table lookup; throughput-vs-latency trade-off equation |
| 6 | `part-2-understanding-llms/module-10-interpretability/section-10.2.html` (Mechanistic Interp) | 1.25 | SAE encoder-decoder math (`f = ReLU(W_enc(x-b_dec))`, reconstruction loss + L1), TopK variant, activation-patching causal-mediation formula |
| 7 | `part-4-training-adaptation/module-17-peft/section-17.1.html` (LoRA & QLoRA) | 3.25 (close to deep) | Add the rank-stabilized scaling derivation `alpha / sqrt(r)` (rsLoRA), the QLoRA NF4 quantization quantile formula, and a unified parameter-budget equation across LoRA / DoRA / GaLore / VeRA |
| 8 | `part-4-training-adaptation/module-17-peft/section-17.2.html` (Advanced PEFT) | 1.75 | Algorithm callouts for DoRA (`W = m · V/‖V‖`), GaLore (low-rank gradient projection via SVD), VeRA (shared random matrices, scalar adapter), Pissa (init from SVD of W) |
| 9 | `part-4-training-adaptation/module-17-peft/section-17.4.html` (Soft Prompts) | 1.75 | Loss-gradient explanation: why gradient flows only into prompt embeddings; per-layer prefix-tuning KV-cache injection; P-Tuning v2 deep prefix re-parameterization |
| 10 | `part-4-training-adaptation/module-18-alignment-rlhf-dpo/section-18.4.html` (DPO Variants) | 1.75 | Equations for IPO (length-regularized), KTO (Kahneman-Tversky, unpaired), SimPO (length-normalized), ORPO (combined SFT+preference); when each one beats vanilla DPO |
| 11 | `part-5-multimodal-llms/module-22-vision-language-models/section-22.1.html` (ViT) | 1.0 | Patch-embedding equation `x_p = Linear(Flatten(Reshape(image)))`, position-embedding addition, [CLS]-token math, sequence length = 1 + (HW)/(P^2) |
| 12 | `part-5-multimodal-llms/module-22-vision-language-models/section-22.2.html` (CLIP/SigLIP) | 2.0 | Symmetric InfoNCE loss with temperature `tau`, batch-size sensitivity discussion, SigLIP's pairwise sigmoid loss replacing softmax |
| 13 | `part-5-multimodal-llms/module-22-vision-language-models/section-22.3.html` (LLaVA, BLIP-3, Qwen-VL) | 2.0 | Connector projection math (`[B, N_patch, D_vision] → [B, N_patch, D_llm]`), instruction-tuning loss, Q-Former cross-attention vs MLP connector |
| 14 | `part-6-agentic-ai/module-26-ai-agents/section-26.1.html` (What Makes an Agent) | 4.0 | Has 3 algo callouts; add formal ReAct loop as numbered Algorithm with halt-condition and max-step guard; OODA loop analogue |
| 15 | `part-6-agentic-ai/module-26-ai-agents/section-26.2.html` (Planning & Agentic Reasoning) | 3.0 | Algorithm callouts for Plan-and-Execute, Tree-of-Thoughts BFS+self-eval+prune, LATS with UCB selection, Reflexion attempt/critique/revise |
| 16 | `part-7-retrieval-information-extraction-with-llms/module-31-embeddings-vector-db/section-31.2.html` (Modern Embeddings) | 3.75 | Add explicit DPR loss `L = -log(exp(sim(q,p+)/tau) / sum_p exp(sim(q,p)/tau))`, ColBERT MaxSim formula, BGE 2-stage training (RetroMAE + contrastive), Matryoshka loss for nested dims |
| 17 | `part-7-retrieval-information-extraction-with-llms/module-32-rag/section-32.2.html` (RAG Long-Context) | 1.25 | Lost-in-the-middle quantitative analysis; long-context attention dilution math; chunking-vs-long-context Pareto frontier with metric examples |
| 18 | `part-7-retrieval-information-extraction-with-llms/module-33-cross-modal-reasoning-rag/section-33.1.html` (Joint Embedding Spaces) | 2.0 | Equations for ImageBind (binding modality to image space via contrastive learning), AudioCLIP (audio-image-text triplet loss), CLIP-as-prior derivation |
| 19 | `part-7-retrieval-information-extraction-with-llms/module-35-advanced-rag/section-35.2.html` (Query Transformation, HyDE, Multi-step) | 2.0 | Algorithm callouts for HyDE (hypothetical doc generation + embed), Step-back prompting, Multi-Query decomposition, Multi-step retrieval loop with termination criterion |
| 20 | `part-9-llm-evaluation-observability/module-43-specialized-evaluation/section-43.1.html` (RAG Eval: Ragas, BEIR) | 2.0 | Explicit Ragas formulas: faithfulness (claim-coverage), answer-relevance (cosine of generated question to original), context-precision (rank-weighted). nDCG with logarithmic discount formula |
| 21 | `part-9-llm-evaluation-observability/module-44-online-eval-observability/section-44.5.html` (Drift Detection) | 0.0 | KL-divergence drift detection, KS test for univariate features, PSI (Population Stability Index) formula, sequential change-point methods (CUSUM) for online detection |
| 22 | `part-10-llm-security-runtime-safety/module-49-agent-safety-autonomy/section-49.5.html` (Why LLMs Hallucinate) | 1.25 | Formal definition of factuality from Manakul SelfCheckGPT (token-level uncertainty), Chen et al. hallucination detection via self-consistency; Jaccard hallucination metric |
| 23 | `part-11-llm-ethics-trust-governance/module-52-bias-fairness/section-52.3.html` (Cross-Cultural NLP) | 1.5 | Pluralistic alignment math (multi-objective RLHF), the cultural-distance score from CDIAL, language-equity metric calculation |
| 24 | `part-11-llm-ethics-trust-governance/module-54b-transparency-and-disclosure/section-54.10.html` (Explainability) | 0.5 | LIME local linear approximation, SHAP additive feature attribution, integrated gradients formula, counterfactual explanation framework (Wachter et al.) |
| 25 | `part-12-llm-systems-at-scale/module-58-frontier-systems-hardware/section-58.4.html` (FlashAttention-4) | 1.5 | The IO-aware tiling pseudocode (already in FA-1 paper), online softmax recurrence (`m_new = max(m_old, m_tile); l_new = exp(m_old - m_new)*l_old + sum_tile`), FA-4 asymmetric-pipeline schedule |
| 26 | `part-12-llm-systems-at-scale/module-58-frontier-systems-hardware/section-58.5.html` (Training-Inference Co-Design) | 1.5 | Sardana 2024 inference-aware optimum equation `C_total = C_train(N,D) + V·C_inference(N)` with V = serving volume; co-optimal solution |
| 27 | `part-13-llmops-lifecycle/module-63-ai-gateways-routing/section-63.2.html` (Routing & Reliability) | 1.75 | RouteLLM threshold-based routing, cost-aware bandit model selection, queue-theory M/M/c for backpressure, exponential-backoff with jitter formula |
| 28 | `part-15-llm-agentic-ai-research-frontiers/module-75-frontier-architectures/section-75.1.html` (Emergent Abilities) | 2.0 | Schaeffer et al. "Emergent Abilities are a Mirage" derivation (linear-in-log-scale metric vs discontinuous-metric), Wei et al. counter-evidence, formal scale-vs-capability curve |
| 29 | `part-15-llm-agentic-ai-research-frontiers/module-76-frontier-theory/section-76.1.html` (Theory of Reasoning) | 3.5 | Add Merrill-Sabharwal expressiveness bound for log-depth CoT, depth-vs-width formal results, transformer-as-circuit (TC^0) limits |
| 30 | `part-15-llm-agentic-ai-research-frontiers/module-77-agi-trajectories/section-77.2.html` (Alignment at Frontier Scale) | 1.5 | Formal weak-to-strong generalization setup (Burns et al. 2023): supervisor labels y_s, student trains on y_s, gap measured against ground truth y*; PGR formula; SAE-steering as feature clamping |

## 3. Patterns Observed: Which Topics Are Systematically Under-Depthed

Three recurring patterns explain most of the gap:

**Pattern A: Survey sections that name canonical methods but never derive
any of them.** The clearest cases are section 8.2 (lists o1/o3/R1/QwQ with
17 named methods but 0 math/algo), section 17.4 (lists 42 soft-prompt methods),
section 22.1 (ViT, lists all variants but no patch-embedding equation), and
section 9.7 (SparseGPT/Wanda named but Hessian-inverse update never written
out). The pattern is "we named everything; we derived nothing." Fix: a
single numbered Algorithm callout with the canonical formal statement
per named method.

**Pattern B: Operational / drift / monitoring sections that have a rich
statistical literature but stay in prose.** Sections 44.5 (Drift Detection),
44.6 (Model-Rotation), 54.10 (Explainability), 47.1a (Prompt Injection),
49.5 (Hallucination Detection), 50.4 (Federated Learning), 66.1 (Reliability
SLOs). Each one has well-established formal apparatus (KL/KS/PSI tests for
drift; LIME/SHAP/IG for explainability; FedAvg/FedProx for federated; PI/QPS
bandwidth-product for SLO budgeting) that is currently invisible in the
prose. Fix: a "Theory Box" with the relevant equation alongside the operations
narrative.

**Pattern C: Mid-depth core-curriculum sections that lack the canonical
algorithm pseudocode.** Despite the `SCIENTIFIC_DEPTH_ADDITIONS.md` round
having added 24 Algorithm callouts in May 2026, several core sections are
still in the "described in prose only" state: 4.2 (Stochastic Sampling),
26.1 (ReAct), 26.2 (TOT/LATS/Reflexion), 31.1b (DPR/ColBERT/BGE), 35.1b
(HyDE), 17.2 (DoRA/GaLore/VeRA), 22.2 (CLIP InfoNCE). These are
high-leverage because they are referenced by name from dozens of other
sections. Fix: numbered Algorithm callouts that match the section
heading, modeled on the 24 already authored in the May 2026 pass.

**Pattern D (minor): Theory-light epigraphs and big-picture callouts repeat
the same intuition five different ways before introducing any formal
content.** This is a writing-flow problem, not a content gap, and the
existing `PROSE_CLARITY_R2.md` audit covers it.

**Pattern E (minor, ignore for this scout): Tools-of-the-trade catalogs
intentionally shallow.** Modules 05, 14, 19-tools, 25, 29, 30, 36 (Retrieval
Tools), 41 (Conv AI Tools), 45, 51, 56 (Responsible AI Tools), 61 (Scale
Tools), 66 (LLMOps), 74, 78. These are catalog-style by design and should
stay so. Several rank high-depth by accident because they cite many named
models; that does not reflect theoretical depth and should not be a target.

## 4. Per-Section Table

The full sortable table is below. Columns: section path | current depth (0-5)
| inline-math count | algo-callout count | named-method count | top 1-2 depth
additions. Sorted by Part → Module → Section number.

Tools-of-the-trade catalog sections and pure-application chapter sections
(67-73 use-case lists) are omitted from this table; they were scouted but
flagged out-of-scope.

### Part I: LLM Building Blocks

| Section | Depth | Math | Algo | Named | Suggested additions |
|---|---:|---:|---:|---:|---|
| `module-00/section-0.1.html` (Classical ML) | 2.25 | 28 | 0 | 1 | Algorithm callouts for SGD vs Adam vs AdamW updates; bias-variance decomposition equation |
| `module-00/section-0.2.html` (Deep Learning Essentials) | 2.75 | 29 | 0 | 0 | Backprop chain-rule derivation, vanishing/exploding-gradient math, Glorot vs He init formulas |
| `module-00/section-0.3.html` (PyTorch Tensors, Autograd) | 0.25 | 0 | 0 | 0 | Intentionally light tutorial; OK |
| `module-00/section-0.4.html` (PyTorch Debugging) | 0.25 | 0 | 0 | 0 | OK (operational) |
| `module-00/section-0.5.html` (RL Foundations) | 4.25 | 6 | 0 | 45 | Has named methods; add Bellman equation + value iteration pseudocode |
| `module-01/section-1.1.html` (Intro to NLP) | 1.25 | 0 | 0 | 0 | Intentionally gentle; OK |
| `module-01/section-1.2.html` (Text Preprocessing) | 3.00 | 14 | 0 | 9 | OK |
| `module-01/section-1.3.html` (Word2Vec, GloVe, FastText) | 2.75 | 26 | 0 | 1 | Algorithm callouts for SGNS (skip-gram negative sampling), GloVe co-occurrence factorization, FastText subword averaging |
| `module-01/section-1.4.html` (ELMo, contextual embeddings) | 1.50 | 0 | 0 | 0 | Bi-LSTM language-model objective equation; layer-weighted ELMo combination formula |
| `module-01/section-1.5.html` (Why Tokenization Matters) | 1.25 | 4 | 0 | 0 | Shannon code-length bound on optimal vocabulary; Zipf's law connection (already mentioned but not formal) |
| `module-01/section-1.6.html` (Subword Algorithms) | 2.50 | 10 | 0 | 0 | **Top-30 #1**: Algorithm callouts for BPE training (merge loop), WordPiece, Unigram with Viterbi; explicit corpus-likelihood objective |
| `module-01/section-1.7.html` (Special Tokens, Tiktoken) | 0.50 | 0 | 0 | 0 | OK (operational) |
| `module-01/section-1.8.html` (Multilingual / Multimodal Tokens) | 0.50 | 0 | 0 | 0 | Add normalized-byte-rate calculation across languages; multimodal token chunking math (image patches → tokens) |
| `module-02/section-2.1.html` (Why RNNs Couldn't Scale) | 3.75 | 64 | 0 | 0 | Already deep; OK |
| `module-02/section-2.2.html` (Attention Mechanism) | 2.75 | 69 | 0 | 0 | Numbered Algorithm callout for additive vs scaled dot-product attention contrast |
| `module-02/section-2.3.html` (QKV, Causal Masking) | 3.00 | 36 | 0 | 0 | Algorithm callout consolidating Q/K/V derivation + sqrt(d_k) scale + softmax + V multiplication |
| `module-02/section-2.4.html` (Multi-Head, Complexity, Lab) | 3.75 | 52 | 0 | 0 | Already deep; OK |
| `module-03/section-3.1.html` (Transformer Anatomy) | 5.00 | 51 | 2 | 0 | Benchmark; OK |
| `module-03/section-3.2.html` (Transformer Init, Causal Mask) | 5.00 | 42 | 3 | 1 | OK |
| `module-03/section-3.3.html` (Build a Transformer Architecture) | 1.25 | 0 | 0 | 0 | Lab section; could add gradient-flow diagram and per-layer parameter counting formula |
| `module-03/section-3.4.html` (Training Loop, Shapes) | 1.25 | 2 | 0 | 0 | Could add memory-usage formula (`activations + params + grads + optimizer-states`) |
| `module-03/section-3.5.html` (Transformer Variants & Efficiency) | 5.00 | 45 | 5 | 0 | Benchmark; OK |
| `module-03/section-3.6.html` (GPU Fundamentals) | 5.00 | 16 | 1 | 2 | OK |
| `module-03/section-3.7.html` (Transformer Expressiveness Theory) | 3.75 | 35 | 0 | 0 | Could add Merrill-Sabharwal TC^0 vs log-depth formal bounds |
| `module-03/section-3.8.html` (SSMs, MoE, Modern Variants) | 5.00 | 28 | 2 | 0 | OK |
| `module-04/section-4.1.html` (Deterministic Decoding) | 4.00 | 17 | 2 | 0 | Could add beam-search complexity (`O(B*V)` per step), length-penalty derivation |
| `module-04/section-4.2.html` (Stochastic Sampling) | 2.00 | 23 | 0 | 0 | **Top-30 #2**: Algorithm callouts for top-p, top-k, min-p, temperature-shifted softmax, repetition penalty (formulas mostly present in prose, need to be lifted into Algorithm boxes) |
| `module-04/section-4.3.html` (Advanced Decoding, Structured) | 3.00 | 11 | 0 | 0 | Algorithm callout for constrained decoding (grammar-state automaton), JSON-mode token-masking |
| `module-04/section-4.4.html` (Diffusion-Based LMs) | 2.25 | 0 | 0 | 5 | Forward/reverse diffusion equation (`x_t = sqrt(alpha_t) x_0 + sqrt(1-alpha_t) eps`), score-matching loss, discrete-diffusion variant |

### Part II: Understanding LLMs

| Section | Depth | Math | Algo | Named | Suggested additions |
|---|---:|---:|---:|---:|---|
| `module-06/section-6.1.html` (BERT, GPT, T5) | 3.75 | 8 | 0 | 7 | Could add MLM/CLM/seq2seq objectives side-by-side as Algorithm |
| `module-06/section-6.2.html` (Pre-training Objectives) | 3.75 | 16 | 0 | 0 | Already strong |
| `module-06/section-6.3.html` (Scaling Laws) | 5.00 | 59 | 5 | 95 | Benchmark; OK |
| `module-06/section-6.4.html` (Data Curation) | 3.50 | 14 | 0 | 3 | Could add deduplication algorithm (MinHash-LSH), quality-filter perplexity threshold derivation |
| `module-06/section-6.5.html` (Optimizers & Training Dynamics) | 3.25 | 36 | 0 | 1 | Add AdamW update with formal weight-decay decoupling, Sophia second-moment update, Muon orthogonalized momentum |
| `module-06/section-6.6.html` (Distributed Training) | 3.25 | 32 | 0 | 0 | Ring all-reduce pseudocode (scatter-reduce + all-gather), 1F1B pipeline schedule |
| `module-06/section-6.7.html` (In-Context Learning Theory) | 3.25 | 13 | 0 | 0 | Add Xie et al. Bayesian framing of ICL, Garg et al. linear-regression-as-task formalization |
| `module-06/section-6.8.html` (Megatron, Elastic, k8s) | 3.00 | 37 | 0 | 0 | Already strong |
| `module-06/section-6.9.html` (Lab: Tiny LM) | 1.75 | 0 | 0 | 4 | Lab; OK |
| `module-07/section-7.1.html` (Frontier Models: OpenAI/Anthropic) | 2.00 | 0 | 0 | 1 | Survey; could add tokens-per-param ratio across all named models as comparative table |
| `module-07/section-7.2.html` (Frontier: Gemini) | 2.00 | 0 | 0 | 1 | Same as 7.1a |
| `module-07/section-7.3.html` (Open Models) | 3.25 | 6 | 0 | 7 | Already strong |
| `module-07/section-7.4.html` (Multilingual / Cross-Cultural) | 1.25 | 5 | 0 | 0 | Add cross-lingual transfer math (XLM objective), tokenizer-coverage formula for low-resource languages |
| `module-08/section-8.1.html` (Test-Time Compute) | 5.00 | 28 | 2 | 21 | OK |
| `module-08/section-8.2.html` (o1, o3, R1, QwQ) | 1.25 | 0 | 0 | 17 | **Top-30 #3**: forward-link GRPO objective inline, contrast hidden-CoT vs visible-CoT training objectives, PRM vs ORM box |
| `module-08/section-8.3.html` (RLVR, GRPO, PRM) | 5.00 | 4 | 4 | 75 | OK (deep, but only 4 inline math; could augment GRPO group-advantage normalization formula) |
| `module-08/section-8.4.html` (Prompting Reasoning Models) | 2.50 | 0 | 0 | 4 | Could add cost-vs-quality Pareto curve formula |
| `module-08/section-8.5.html` (Compute-Optimal Inference) | 5.00 | 20 | 2 | 3 | OK |
| `module-08/section-8.6.html` (Formal & Verifiable Reasoning) | 2.50 | 1 | 0 | 4 | Add LEAN/Coq proof-search algorithm, prover-verifier interaction loop |
| `module-09/section-9.1.html` (Quantization: Math) | 3.00 | 23 | 0 | 26 | Add explicit linear-quant equation `q = round(x/s) + z`, log-quant (NF4) quantile derivation |
| `module-09/section-9.2.html` (Quant Algorithms, QAT) | 3.25 | 15 | 0 | 70 | Algorithm callouts for GPTQ Hessian-based weight update, AWQ activation-aware scaling, SmoothQuant per-channel rescale |
| `module-09/section-9.3.html` (KV Cache, Memory Opt) | 5.00 | 14 | 1 | 15 | OK |
| `module-09/section-9.4.html` (Speculative Decoding) | 5.00 | 77 | 3 | 1 | OK |
| `module-09/section-9.5.html` (Serving Stack, vLLM Deep Dive) | 1.50 | 0 | 0 | 2 | **Top-30 #5**: Algorithm callout for continuous-batching scheduler, PagedAttention block-table mapping, throughput-vs-latency M/M/c formula |
| `module-09/section-9.6.html` (Serving Runtimes) | 3.25 | 5 | 0 | 27 | OK |
| `module-09/section-9.7.html` (Pruning & Sparsity) | 1.50 | 0 | 0 | 14 | **Top-30 #4**: Algorithm callouts for SparseGPT (Hessian-inverse), Wanda (`|w_ij| * ‖x_j‖`), 2:4 sparsity mask |
| `module-09/section-9.8.html` (Test-Time Compute & Reasoning) | 2.00 | 0 | 0 | 4 | Algorithm callout for best-of-N + verifier, self-consistency majority vote |
| `module-09/section-9.9.html` (GPU Kernel Programming) | 5.00 | 17 | 2 | 0 | OK |
| `module-10/section-10.1.html` (Attention Analysis & Probing) | 0.75 | 0 | 0 | 0 | Probing-classifier accuracy as proxy for representation quality; logit-lens unembed projection |
| `module-10/section-10.2.html` (Mechanistic Interp) | 1.25 | 0 | 0 | 0 | **Top-30 #6**: SAE encoder-decoder equations, TopK variant, activation-patching causal-mediation formula |
| `module-10/section-10.3.html` (Practical Interp) | 1.75 | 0 | 0 | 0 | Could add unified pipeline pseudocode for SAE-feature discovery |
| `module-10/section-10.4.html` (Explaining Transformers) | 0.75 | 0 | 0 | 0 | Layer-wise-relevance-propagation, integrated-gradients formal definition |
| `module-10/section-10.5.html` (Interp Tooling, LLM-Assisted) | 0.75 | 0 | 0 | 0 | Could add automated-circuit-discovery loop pseudocode |
| `module-10/section-10.6.html` (Platforms - interp) | 1.00 | 1 | 0 | 0 | Catalog; OK |
| `module-10/section-10.7.html` (Interp Tools, TransformerLens) | 1.50 | 0 | 0 | 0 | Could add HookPoint mechanism formalization |

### Part III: Working with LLMs

| Section | Depth | Math | Algo | Named | Suggested additions |
|---|---:|---:|---:|---:|---|
| `module-11/section-11.1.html` (API Landscape) | 1.00 | 0 | 0 | 0 | Operational; OK |
| `module-11/section-11.2.html` (Structured Output, Tools) | 0.00 | 0 | 0 | 0 | Could add JSON-mode grammar automaton, constrained-decoding token-mask construction |
| `module-11/section-11.3.html` (API Engineering Best Practices) | 0.50 | 0 | 0 | 0 | Could add exponential-backoff with jitter, idempotency-key uniqueness math |
| `module-11/section-11.4.html` (Reasoning + Multimodal APIs) | 2.00 | 0 | 0 | 1 | OK |
| `module-12/section-12.1.html` (Foundational Prompt Design) | 1.00 | 0 | 0 | 0 | Could add prompt-template entropy reduction formula |
| `module-12/section-12.2.html` (CoT & Reasoning) | 2.25 | 3 | 0 | 0 | Self-consistency aggregation rule, CoT length-vs-accuracy curve |
| `module-12/section-12.3.html` (Advanced Prompt Patterns) | 2.00 | 0 | 0 | 0 | Could add Plan-and-Solve, Generated-Knowledge prompting algorithm boxes |
| `module-12/section-12.4.html` (Prompt Security & Optimization) | 1.50 | 0 | 0 | 1 | Adversarial-prefix optimization (Zou et al. GCG) gradient descent in token space |
| `module-12/section-12.5.html` (Auto Prompt Engineering) | 1.75 | 1 | 0 | 2 | APE, OPRO, DSPy compiler search-space formulation |
| `module-13/section-13.1.html` (When LLM vs Classical ML) | 3.75 | 5 | 0 | 0 | OK |
| `module-13/section-13.2.html` (LLM as Feature Extractor) | 1.50 | 0 | 0 | 1 | Could add probing-classifier convergence rate, pooling-strategy comparison (mean/max/CLS) |
| `module-13/section-13.3.html` (Hybrid Pipeline Patterns) | 1.75 | 2 | 0 | 0 | Cost-routing decision formula |
| `module-13/section-13.4.html` (Cost-Performance Opt at Scale) | 2.00 | 0 | 0 | 2 | Algorithm callout for cascading models (Chen et al. FrugalGPT) |
| `module-13/section-13.5a/b.html` (Dataset Engineering) | 2.25/1.75 | 3/0 | 0/0 | 12/50 | Already broad; could add concrete entropy-based diversity sampling formulas |

### Part IV: Training & Adaptation

| Section | Depth | Math | Algo | Named | Suggested additions |
|---|---:|---:|---:|---:|---|
| `module-15/section-15.1.html` (Synthetic Data Principles) | 1.25 | 5 | 0 | 1 | Generative-discriminative gap, label-noise rate equation |
| `module-15/section-15.2.html` (LLM Data Generation Pipelines) | 1.50 | 1 | 0 | 3 | Self-Instruct seed-expansion algorithm, Evol-Instruct prompt-mutation operator set |
| `module-15/section-15.3.html` (QA & Data Curation) | 1.00 | 1 | 0 | 1 | Cleanlab confidence-based mislabeling detection, deduplication via MinHash-LSH |
| `module-15/section-15.4.html` (LLM Labeling & Active Learning) | 0.00 | 0 | 0 | 0 | **Big gap.** Active-learning acquisition functions: uncertainty sampling (`H(p)`), expected-model-change, query-by-committee (Kullback-Leibler-disagreement), BALD |
| `module-15/section-15.5.html` (Weak Supervision & Programmatic) | 0.50 | 0 | 0 | 0 | Snorkel data-programming model, label-model loss derivation, generative-discriminative two-stage formulation |
| `module-15/section-15.6.html` (Synthetic Reasoning Data) | 2.25 | 2 | 0 | 17 | Algorithm callout for STaR self-taught rationales, ReST loop, RFT (Rejection Fine-Tuning) |
| `module-15/section-15.7.html` (Data Augmentation) | 0.50 | 0 | 0 | 0 | EDA operations math, mixup formula (`x = lambda x_a + (1-lambda) x_b`), back-translation cycle |
| `module-16/section-16.1.html` (When to Fine-Tune) | 1.75 | 0 | 0 | 12 | Decision-tree formula vs RAG vs prompting, transfer-learning prerequisite (target-domain data lower bound) |
| `module-16/section-16.2.html` (Data Prep for FT) | 0.50 | 0 | 0 | 1 | Could add data-quality heuristics: instruction-coverage entropy, deduplication threshold |
| `module-16/section-16.3.html` (SFT) | 1.75 | 0 | 0 | 3 | Standard cross-entropy SFT loss explicitly, instruction-tuning packing-vs-truncation tradeoff |
| `module-16/section-16.4.html` (FT via Provider APIs) | 1.00 | 0 | 0 | 15 | OK (operational) |
| `module-16/section-16.5.html` (FT for Representation Learning) | 2.00 | 0 | 0 | 2 | Add contrastive loss (CoSENT, MultiNeg) for embedding fine-tuning |
| `module-16/section-16.6.html` (FT for Classification/Sequence) | 0.75 | 0 | 0 | 0 | Linear-head vs adapter-head trade-off; BIO tagging F1 derivation |
| `module-16/section-16.7.html` (Adapting for Long Text) | 2.00 | 2 | 0 | 4 | Position-interpolation (PI), YaRN extrapolation factor, NTK-aware scaling formula |
| `module-17/section-17.1.html` (LoRA & QLoRA) | 3.25 | 0 | 1 | 141 | **Top-30 #7**: rsLoRA scaling derivation `alpha / sqrt(r)`, QLoRA NF4 quantile formula, unified parameter-budget equation |
| `module-17/section-17.2.html` (Advanced PEFT) | 1.75 | 0 | 0 | 133 | **Top-30 #8**: Algorithm callouts for DoRA, GaLore, VeRA, Pissa |
| `module-17/section-17.3.html` (Training Platforms) | 2.25 | 1 | 0 | 58 | Catalog; OK |
| `module-17/section-17.4.html` (Soft Prompts) | 1.75 | 0 | 0 | 42 | **Top-30 #9**: per-layer prefix KV injection equations, gradient-flow derivation |
| `module-17/section-17.5.html` (KD Foundations) | 3.25 | 6 | 0 | 4 | Already strong |
| `module-17/section-17.6.html` (Distillation: Licensing, Speculative) | 1.75 | 0 | 0 | 2 | Reasoning-trace distillation loss formula |
| `module-17/section-17.7.html` (Model Merging) | 3.50 | 12 | 0 | 5 | OK (Task Arithmetic, TIES, DARE formulas mostly present) |
| `module-17/section-17.8.html` (Continual Learning) | 3.25 | 7 | 0 | 16 | EWC Fisher matrix formula, LwF distillation regularizer, gradient projection methods |
| `module-18/section-18.1.html` (RLHF with PPO) | 5.00 | 14 | 5 | 80 | Benchmark; OK |
| `module-18/section-18.2.html` (GRPO, Reward Hacking) | 3.25 | 9 | 0 | 115 | Could add explicit GRPO group-relative advantage formula `A_i = (r_i - mean(r)) / std(r)` |
| `module-18/section-18.3.html` (DPO Derivation) | 5.00 | 19 | 4 | 91 | Benchmark; OK |
| `module-18/section-18.4.html` (DPO Variants, Iterative) | 1.75 | 0 | 0 | 139 | **Top-30 #10**: equations for IPO, KTO, SimPO, ORPO with when-each-wins |
| `module-18/section-18.5.html` (Constitutional AI) | 2.25 | 0 | 0 | 17 | CAI two-stage loop pseudocode (critique-revise with constitution), RLAIF reward derivation |
| `module-18/section-18.6.html` (RLVR) | 2.75 | 2 | 0 | 28 | Verifiable-reward objective formal statement; outcome vs process reward distinction equation |
| `module-18/section-18.7.html` (Alignment Frontiers) | 4.00 | 0 | 2 | 9 | Has algos; could add weak-to-strong PGR formula |

### Part V: Multimodal LLMs

| Section | Depth | Math | Algo | Named | Suggested additions |
|---|---:|---:|---:|---:|---|
| `module-20/section-20.1.html` (TTS: VITS, Bark, F5-TTS) | 1.75 | 0 | 0 | 0 | VITS flow-based posterior, F5-TTS diffusion-based STT objective |
| `module-20/section-20.2.html` (Voice Cloning, Zero-Shot TTS) | 0.50 | 0 | 0 | 0 | Speaker embedding similarity loss; flow-matching for zero-shot voice |
| `module-20/section-20.3.html` (Music Generation) | 0.50 | 0 | 0 | 0 | Hierarchical token modeling (MusicLM SoundStream tokens), MusicGen single-stage formulation |
| `module-20/section-20.4.html` (Audio Editing) | 0.50 | 0 | 0 | 0 | Source separation as masking, AudioLDM diffusion objective |
| `module-20/section-20.5.html` (Speech Recognition) | 0.50 | 0 | 0 | 0 | Whisper encoder-decoder loss, CTC vs attention objectives |
| `module-20/section-20.6.html` (Video DiTs) | 3.00 | 29 | 0 | 0 | Already strong |
| `module-20/section-20.7.html` (Sora, Veo, Runway, Kling) | 0.50 | 0 | 0 | 0 | Comparative model-quality metric (FVD, IS-V); training-data scale comparison |
| `module-20/section-20.8.html` (Camera Control, ControlNet for Video) | 0.50 | 0 | 0 | 1 | ControlNet's zero-conv warm-start, camera-pose embedding formulation |
| `module-20/section-20.9.html` (Video Editing) | 0.50 | 0 | 0 | 0 | Operational; OK |
| `module-20/section-20.10.html` (Long-Form Video) | 0.50 | 0 | 0 | 0 | Temporal-consistency loss, segment-stitching algorithm |
| `module-21/section-21.1.html` (TrOCR) | 0.50 | 0 | 0 | 0 | Encoder-decoder architecture, CER vs WER metrics |
| `module-21/section-21.2.html` (LayoutLM Family) | 0.50 | 0 | 0 | 0 | 2D position encoding, masked-visual-language modeling objective |
| `module-21/section-21.3.html` (VLM-Based Document) | 1.50 | 0 | 0 | 1 | OK |
| `module-21/section-21.4.html` (Doc AI Pipelines) | 0.50 | 0 | 0 | 0 | Operational; OK |
| `module-22/section-22.1.html` (ViT, Visual Tokenization) | 1.00 | 0 | 0 | 0 | **Top-30 #11**: patch-embedding equation, sequence-length formula, [CLS] token math |
| `module-22/section-22.2.html` (CLIP, SigLIP) | 2.00 | 5 | 0 | 2 | **Top-30 #12**: symmetric InfoNCE loss derivation, batch-size sensitivity, SigLIP's pairwise sigmoid replacement |
| `module-22/section-22.3.html` (LLaVA, BLIP-3, Qwen-VL) | 2.00 | 0 | 0 | 0 | **Top-30 #13**: connector projection math; Q-Former vs MLP comparison |
| `module-22/section-22.4.html` (Frontier VLMs: GPT-4V, Gemini, Claude) | 2.50 | 8 | 0 | 0 | Already strong |
| `module-22/section-22.5.html` (Evaluating MMMU) | 1.50 | 2 | 0 | 0 | Could add benchmark-construction methodology, item-response-theory for saturation |
| `module-22/section-22.6.html` (Pipeline vs Native Multimodal) | 1.25 | 3 | 0 | 0 | Could add end-to-end joint-loss formulation vs cascaded pipeline error rate |
| `module-22/section-22.7.html` (Early vs Late Fusion) | 1.25 | 0 | 0 | 2 | Early/late/hybrid fusion as gating equations |
| `module-22/section-22.8.html` (Any-to-Any Generation) | 0.50 | 0 | 0 | 0 | Cross-modal autoregression formal setup |
| `module-22/section-22.9.html` (Frontier Omni: GPT-4o, Llama-4-Omni) | 1.50 | 1 | 0 | 0 | Could add per-modality token budget table; cross-modal-attention pattern |
| `module-23/section-23.x` (3D Generation, Splats) | 1.25 to 2.75 | 4 to 23 | 0 | 0 | Mostly strong; one outlier (`23.4` Direct 3D Diffusion at 1.25) needs Trellis structured-latent equation |
| `module-24/section-24.1.html` (VLA Architecture) | 1.75 | 0 | 0 | 0 | VLA objective formal statement: `pi(a|o,l) = argmax LM(action_tokens | obs_tokens, lang_tokens)` |
| `module-24/section-24.2.html` (OpenVLA-7B Reference) | 1.50 | 0 | 0 | 7 | Could add action-token discretization (256 bins per joint) |
| `module-24/section-24.3.html` (Pi-0 / Pi-0.5) | 3.00 | 7 | 0 | 3 | Already strong |
| `module-24/section-24.4.html` (RT-2-X, Data Scaling) | 2.75 | 13 | 0 | 1 | Strong |
| `module-24/section-24.5-24.13` (VLA limitations etc.) | 0.5 to 1.25 | 0 to 4 | 0 | 0-2 | Sim-to-real domain randomization formula, SayCan affordance prior P(a is_possible) |

### Part VI: Agentic AI

| Section | Depth | Math | Algo | Named | Suggested additions |
|---|---:|---:|---:|---:|---|
| `module-26/section-26.1.html` (What Makes an Agent) | 4.00 | 0 | 3 | 0 | **Top-30 #14**: formal ReAct loop as numbered Algorithm with halt-condition + max-step guard |
| `module-26/section-26.2.html` (Planning, Reasoning) | 3.00 | 0 | 2 | 0 | **Top-30 #15**: Algorithm callouts for Plan-and-Execute, ToT BFS+self-eval+prune, LATS UCB, Reflexion |
| `module-26/section-26.3.html` (Reasoning Models as Backbones) | 2.00 | 0 | 0 | 0 | Cost-aware hybrid agent routing decision rule |
| `module-26/section-26.4.html` (Agent Eval, Benchmarks) | 0.50 | 0 | 0 | 0 | Pass@k formula, tool-call F1; AgentBench task-success metric |
| `module-26/section-26.5.html` (End-to-End Agent System) | 0.50 | 1 | 0 | 0 | Operational; OK |
| `module-26/section-26.6.html` (Memory Architecture) | 1.00 | 0 | 0 | 0 | Long-term retrieval scoring, episodic vs semantic memory consolidation rule |
| `module-27/section-27.1.html` (Function Calling) | 3.50 | 0 | 2 | 0 | Strong |
| `module-27/section-27.2.html` (MCP) | 2.50 | 0 | 2 | 0 | OK |
| `module-27/section-27.3.html` (A2A Protocol) | 0.50 | 0 | 0 | 0 | Protocol state-machine pseudocode |
| `module-27/section-27.4.html` (Custom Tool Design) | 0.50 | 0 | 0 | 0 | Operational; OK |
| `module-27/section-27.5.html` (Retrieval as Tool Call) | 1.00 | 0 | 0 | 0 | Could add tool-selection multinomial under attention scores |
| `module-27/section-27.6.html` (Multi-Tool Orchestration, Tool Econom.) | 2.50 | 18 | 0 | 0 | Already has math; could add tool-call-graph cost optimization |
| `module-28/section-28.1.html` (Multi-Agent Framework Landscape) | 1.00 | 0 | 0 | 1 | OK (survey) |
| `module-28/section-28.2.html` (Architecture Patterns) | 2.00 | 0 | 2 | 0 | Could add orchestrator-worker coordination protocol, AutoGen group-chat termination rule |
| `module-28/section-28.3.html` (Human-in-the-Loop) | 0.50 | 0 | 0 | 0 | Confidence threshold for human-handoff; HITL latency vs accuracy curve |
| `module-28/section-28.4.html` (Testing Multi-Agent) | 0.50 | 0 | 0 | 0 | Trace-replay testing pseudocode |
| `module-29/section-29.x` (Specialized Agents) | 0.5 to 1.5 | 0 | 0 | 0 | Browser-agent action space DOM-querying formalization; data-analysis agent verifiable-step rubric |

### Part VII: Retrieval & Information Extraction

| Section | Depth | Math | Algo | Named | Suggested additions |
|---|---:|---:|---:|---:|---|
| `module-31/section-31.1.html` (Classical Embeddings) | 2.25 | 0 | 0 | 6 | Word2Vec SGNS loss, GloVe co-occurrence factorization, FastText subword sum |
| `module-31/section-31.2.html` (Modern Embeddings) | 3.75 | 1 | 2 | 21 | **Top-30 #16**: explicit DPR contrastive loss, ColBERT MaxSim, BGE 2-stage training, Matryoshka nested-dim loss |
| `module-31/section-31.3.html` (HNSW, IVF) | 5.00 | 11 | 5 | 102 | Benchmark; OK |
| `module-31/section-31.4.html` (PQ, Composite, FAISS) | 3.50 | 2 | 2 | 95 | Already strong |
| `module-31/section-31.5.html` (Vector DB Systems) | 1.50 | 0 | 0 | 51 | Catalog; OK (intentionally shallow) |
| `module-31/section-31.4a.html` (Document Processing, Chunking) | 2.50 | 8 | 0 | 5 | Could add explicit chunk-size optimization curve |
| `module-31/section-31.7.html` (Production RAG, Topic Modeling) | 1.75 | 3 | 0 | 2 | BERTopic clustering pseudocode; LDA likelihood as comparison |
| `module-31/section-31.8.html` (Vision-Based Doc Retrieval) | 5.00 | 9 | 2 | 20 | OK |
| `module-32/section-32.1.html` (RAG Foundations) | 3.00 | 0 | 3 | 0 | Strong |
| `module-32/section-32.2.html` (RAG Indexing, Long-Context) | 1.25 | 4 | 0 | 1 | **Top-30 #17**: lost-in-the-middle quantitative analysis, long-context attention dilution, chunking-vs-long-context tradeoff |
| `module-32/section-32.3.html` (Deep Research, Agentic RAG) | 2.00 | 0 | 0 | 4 | Could add iterative-query-refinement loop with termination criterion |
| `module-32/section-32.4.html` (Structured Data, Text-to-SQL) | 1.50 | 0 | 0 | 1 | Spider/BIRD scoring math, semantic-parsing exact-match formula |
| `module-32/section-32.5.html` (Source Attribution) | 1.00 | 0 | 0 | 0 | Could add attention-attribution vs gradient-attribution, F1 of citations |
| `module-33/section-33.1.html` (Joint Embedding Spaces) | 2.00 | 15 | 0 | 0 | **Top-30 #18**: ImageBind / AudioCLIP / multi-modal contrastive setup formal |
| `module-33/section-33.2.html` (Multimodal RAG) | 1.50 | 1 | 0 | 4 | Cross-modal retrieval Recall@k formula |
| `module-33/section-33.3.html` (When to Retrieve, When to Reason) | 1.25 | 5 | 0 | 0 | Decision rule formalization (entropy of model's prior over answers) |
| `module-33/section-33.4.html` (Multimodal in Production) | 0.50 | 0 | 0 | 1 | Operational; OK |
| `module-34/section-34.1.html` (IE Landscape) | 0.50 | 0 | 0 | 0 | Could add precision/recall/F1 derivation for IE-specific metrics |
| `module-34/section-34.2.html` (Classical/Open IE) | 0.50 | 0 | 0 | 0 | OpenIE relation-extraction triplet-scoring rule |
| `module-34/section-34.3.html` (Hybrid IE) | 1.00 | 1 | 0 | 0 | Hybrid rule+LLM precision-recall combination |
| `module-34/section-34.4.html` (Production IE) | 0.50 | 0 | 0 | 0 | Operational; OK |
| `module-34/section-34.5.html` (Coreference) | 1.00 | 0 | 0 | 0 | Mention-pair/span-ranking objective, CoNLL F1 |
| `module-35/section-35.1.html` (Hybrid Retrieval, Re-Ranking) | 3.50 | 0 | 4 | 52 | Strong; could add cross-encoder vs bi-encoder asymptotic-cost trade-off |
| `module-35/section-35.2.html` (Query Transformation, HyDE) | 2.00 | 0 | 0 | 18 | **Top-30 #19**: HyDE / Step-back / Multi-Query / Multi-step retrieval Algorithm callouts |
| `module-35/section-35.3.html` (RAG with Knowledge Graphs) | 0.50 | 1 | 0 | 0 | Could add subgraph-extraction pseudocode, KG-RAG joint scoring |
| `module-35/section-35.4.html` (GraphRAG) | 2.25 | 6 | 0 | 5 | Already strong (community-detection-Leiden pseudocode would complete) |
| `module-35/section-35.5.html` (RAG Ingestion Pipelines) | 0.00 | 1 | 0 | 0 | Operational; OK |
| `module-35/section-35.6.html` (RAG Frameworks) | 0.50 | 0 | 0 | 1 | Catalog; OK |
| `module-35/section-35.7.html` (RAG Production, DSPy, Hardening) | 1.50 | 0 | 0 | 3 | DSPy compiler objective formal statement |

### Part VIII: Conversational AI

| Section | Depth | Math | Algo | Named | Suggested additions |
|---|---:|---:|---:|---:|---|
| `module-37/section-37.1.html` (Dialogue System Architecture) | 0.50 | 0 | 0 | 0 | Could add NLU-DM-NLG architecture diagram with module interfaces |
| `module-37/section-37.2.html` (Personas, Companionship) | 0.50 | 0 | 0 | 0 | Persona-consistency loss (PersonaChat F1), engagement-metric formulation |
| `module-37/section-37.3.html` (Short-Term Memory) | 0.50 | 0 | 0 | 0 | Sliding-window vs summary memory token-budget formula |
| `module-37/section-37.4.html` (Multi-Turn Dialogue) | 1.00 | 0 | 0 | 0 | Coherence metric (LCC, BERTScore for dialogue) |
| `module-37/section-37.5a/b.html` (Long-Term Memory: MemGPT) | 0.50/0.50 | 0/0 | 0/0 | 0/0 | MemGPT page-fault/swap algorithm pseudocode, profile-consolidation rule |
| `module-40/section-40.1.html` (Voice Agents) | 0.50 | 0 | 0 | 0 | Voice-pipeline latency stack (STT + LM + TTS) sum-formula |
| `module-40/section-40.2.html` (Streaming Audio) | 0.50 | 0 | 0 | 0 | Streaming chunked-attention math |
| `module-40/section-40.3.html` (Gemini Live, GPT-4o Realtime) | 0.00 | 0 | 0 | 0 | Operational; OK |
| `module-40/section-40.4.html` (Audio Token Budget) | 2.00 | 19 | 0 | 0 | Already strong |
| `module-40/section-40.5.html` (OSS Realtime) | 0.50 | 0 | 0 | 0 | Catalog; OK |
| `module-40/section-40.6a/b.html` (Voice AI STT/TTS) | 0.50/0.50 | 0/0 | 0/0 | 0/0 | Whisper / Parakeet objective, F5-TTS flow-matching diffusion eq |

### Part IX: Evaluation & Observability

| Section | Depth | Math | Algo | Named | Suggested additions |
|---|---:|---:|---:|---:|---|
| `module-42/section-42.1.html` (Eval Fundamentals) | 4.25 | 15 | 1 | 0 | OK |
| `module-42/section-42.2.html` (Experimental Design) | 3.50 | 0 | 2 | 0 | Strong |
| `module-42/section-42.3.html` (Testing LLM Apps) | 1.00 | 0 | 0 | 0 | Add unit-test taxonomy, golden-set-construction lower bound |
| `module-42/section-42.4.html` (LLM-Specific Monitoring) | 0.50 | 0 | 0 | 0 | KL-drift, perplexity-drift, custom-eval-drift formulas |
| `module-42/section-42.5.html` (Eval-Driven Quality Gates) | 0.50 | 0 | 0 | 0 | Operational; OK |
| `module-42/section-42.6.html` (Observability & Tracing) | 0.00 | 0 | 0 | 0 | Operational; OK |
| `module-42/section-42.7.html` (Experiment Reproducibility) | 1.25 | 4 | 0 | 0 | Random-seed control, deterministic-vs-stochastic decoding |
| `module-42/section-42.8.html` (Long-Context Benchmarks) | 3.50 | 11 | 0 | 0 | Strong |
| `module-42/section-42.9.html` (OpenTelemetry) | 0.00 | 0 | 0 | 0 | Operational; OK |
| `module-42/section-42.10.html` (Research Methodology) | 4.25 | 5 | 2 | 3 | OK |
| `module-42/section-42.11.html` (Structured Output Testing) | 1.50 | 0 | 1 | 0 | Has 1 algo; could add JSON-schema validation formal grammar |
| `module-42/section-42.12.html` (Classical ML Metrics) | 4.75 | 7 | 6 | 2 | OK |
| `module-43/section-43.1.html` (RAG Eval: Ragas, BEIR) | 2.00 | 7 | 0 | 0 | **Top-30 #20**: explicit Ragas faithfulness/answer-relevance/context-precision formulas; nDCG with log discount |
| `module-43/section-43.2.html` (Agentic Eval) | 0.50 | 0 | 0 | 0 | tau-bench pass-rate, AgentBench scoring rubric |
| `module-43/section-43.3.html` (Simulation-Based Eval, tau-bench) | 2.50 | 1 | 1 | 0 | Could deepen with simulator state-action transition formal |
| `module-43/section-43.4.html` (Code-Gen Eval) | 3.25 | 5 | 1 | 0 | Strong |
| `module-43/section-43.5.html` (Multimodal Eval) | 2.50 | 0 | 1 | 0 | Could add per-modality metric weighting |
| `module-44/section-44.1.html` (Eval Dashboards) | 0.50 | 0 | 0 | 0 | Operational; OK |
| `module-44/section-44.2.html` (Eval Dashboards p2) | 0.50 | 0 | 0 | 0 | OK |
| `module-44/section-44.3.html` (Observability, Drift) | 1.00 | 0 | 0 | 0 | Could add drift-test (KS, PSI) formulas alongside narrative |
| `module-44/section-44.4.html` (Post-Launch Monitoring) | 0.00 | 0 | 0 | 1 | Operational; OK |
| `module-44/section-44.5.html` (Drift Detection in Prod) | 0.00 | 1 | 0 | 0 | **Top-30 #21**: KL/KS/PSI, CUSUM, two-sample MMD, sliding-window EWMA for online detection |
| `module-44/section-44.6.html` (Model-Rotation) | 0.00 | 0 | 0 | 0 | Operational; OK |
| `module-44/section-44.7.html` (Eval-as-Product) | 0.00 | 0 | 0 | 0 | Catalog; OK |

### Part X: Security & Runtime Safety

| Section | Depth | Math | Algo | Named | Suggested additions |
|---|---:|---:|---:|---:|---|
| `module-47/section-47.1.html` (Prompt Injection Part 1) | 1.00 | 1 | 0 | 0 | Adversarial-suffix optimization (GCG) gradient steps, prefix-tuning attack vector |
| `module-47/section-47.2.html` (Data Poisoning, Extraction Part 2) | 4.25 | 9 | 4 | 0 | OK |
| `module-47/section-47.3.html` (Red Teaming Frameworks) | 4.00 | 13 | 2 | 0 | OK |
| `module-47/section-47.4.html` (Supply Chain, Conf Compute) | 1.50 | 0 | 0 | 0 | TEE attestation flow pseudocode |
| `module-48/section-48.1.html` (What Guardrails Are) | 1.00 | 0 | 0 | 3 | Could add classification taxonomy formal |
| `module-48/section-48.2.html` (Input Guardrails) | 4.00 | 17 | 2 | 0 | OK |
| `module-48/section-48.3.html` (Output Guardrails: Llama Guard, NeMo) | 4.25 | 14 | 2 | 0 | OK |
| `module-48/section-48.4.html` (Policy DSL, Constrained Decoding) | 1.25 | 4 | 0 | 0 | Could add formal constrained-decoding masking equation (token logit masking) |
| `module-48/section-48.5.html` (Multimodal Guardrails) | 0.50 | 0 | 0 | 0 | Image / audio classifier-cascade rule |
| `module-49/section-49.1.html` (Agent Safety, Prompt Injection Defense) | 5.00 | 13 | 4 | 0 | OK |
| `module-49/section-49.2.html` (Sandboxed Execution) | 0.50 | 0 | 0 | 0 | Capability-based security model, seccomp filter formal |
| `module-49/section-49.3.html` (Agentic Security Benchmarks) | 0.50 | 0 | 0 | 0 | InjecAgent / AgentDojo scoring formal |
| `module-49/section-49.4.html` (Supply-Chain Security) | 0.75 | 0 | 0 | 0 | SBOM verification, provenance graph formal |
| `module-49/section-49.5.html` (Why LLMs Hallucinate) | 1.25 | 5 | 0 | 0 | **Top-30 #22**: SelfCheckGPT token-level uncertainty, Chen self-consistency, hallucination-detection Jaccard |
| `module-50/section-50.1.html` (Privacy Attacks, DP) | 4.75 | 60 | 2 | 3 | Benchmark; OK |
| `module-50/section-50.2.html` (Machine Unlearning) | 4.25 | 21 | 2 | 1 | OK |
| `module-50/section-50.3.html` (Federated Learning) | 3.25 | 13 | 0 | 16 | Could add FedAvg + FedProx + SCAFFOLD update equations |

### Part XI: Ethics & Governance

| Section | Depth | Math | Algo | Named | Suggested additions |
|---|---:|---:|---:|---:|---|
| `module-52/section-52.2.html` (Bias, Fairness, Ethics) | 4.00 | 23 | 3 | 0 | OK |
| `module-52/section-52.3.html` (Cross-Cultural NLP) | 1.50 | 0 | 0 | 6 | **Top-30 #23**: pluralistic-alignment multi-objective RLHF, cultural-distance CDIAL score, language-equity metric |
| `module-53/section-53.1.html` (Global Regulatory) | 0.00 | 0 | 0 | 0 | Intentionally policy-only; OK |
| `module-53/section-53.2.html` (EU AI Act) | 5.00 | 12 | 2 | 3 | OK |
| `module-53/section-53.3.html` (Risk Governance) | 0.50 | 1 | 0 | 0 | Policy; OK |
| `module-53/section-53.4.html` (Licensing, IP, Privacy) | 0.75 | 0 | 0 | 0 | Policy; OK |
| `module-53/section-53.5.html` (Open Problems in Governance) | 1.00 | 0 | 0 | 1 | OK |
| `module-54/section-54.1.html` (Why Provenance) | 0.00 | 0 | 0 | 0 | Policy; OK |
| `module-54/section-54.2.html` (Text Watermarking: Green-List) | 4.00 | 22 | 2 | 0 | OK |
| `module-54/section-54.3.html` (Image/Video Provenance) | 3.50 | 13 | 2 | 0 | Strong |
| `module-54/section-54.4.html` (Deepfake Detection) | 0.50 | 0 | 0 | 0 | Adversarial-frequency-domain detection equations |
| `module-54/section-54.5.html` (Watermark Removal) | 1.00 | 0 | 0 | 0 | Removal-cost vs detectability trade-off |
| `module-54b/section-54.6.html` (Model Cards) | 2.00 | 12 | 0 | 0 | OK |
| `module-54b/section-54.7.html` (Datasheets) | 0.50 | 0 | 0 | 0 | Policy framework; OK |
| `module-54b/section-54.8.html` (System Cards) | 1.00 | 0 | 0 | 0 | OK |
| `module-54b/section-54.9.html` (Audit Trails) | 0.00 | 0 | 0 | 0 | Operational; OK |
| `module-54b/section-54.10.html` (Explainability) | 0.50 | 0 | 0 | 0 | **Top-30 #24**: LIME, SHAP, integrated gradients, counterfactual explanation formal |
| `module-55/section-55.1.html` (Environmental Cost) | 5.00 | 28 | 2 | 12 | OK |
| `module-55/section-55.2.html` (Reducing Footprint) | 1.50 | 0 | 0 | 5 | Could add carbon-aware scheduling formula, PUE-weighted FLOP accounting |
| `module-55/section-55.3.html` (Operating Under Compliance) | 1.75 | 4 | 0 | 6 | Could add ISO 14040 LCA framework computation |

### Part XII: Systems at Scale

| Section | Depth | Math | Algo | Named | Suggested additions |
|---|---:|---:|---:|---:|---|
| `module-57/section-57.1.html` (Compute Planning, Infra) | 1.75 | 4 | 0 | 0 | Could add explicit GPU-hour calculation from N + D + algorithmic FLOPs |
| `module-57/section-57.2.html` (Enterprise Integration) | 0.50 | 0 | 0 | 0 | Operational; OK |
| `module-57/section-57.3.html` (GPU Procurement, Spot/Reserved) | 2.00 | 8 | 0 | 0 | Already has math; could add capacity-vs-cost Pareto |
| `module-57/section-57.4.html` (LLM Perf Benchmarking) | 1.50 | 2 | 0 | 2 | MFU (model FLOPs utilization), throughput formula, latency tail derivation |
| `module-58/section-58.1.html` (Beyond NVIDIA: Groq, Cerebras) | 0.50 | 0 | 0 | 0 | Could add roofline-model comparison across silicon |
| `module-58/section-58.2.html` (Decentralized Training: Nous Psyche) | 1.75 | 0 | 0 | 4 | DiLoCo/DeMo communication-compression formal |
| `module-58/section-58.3.html` (Edge: MLX, Apple Intelligence) | 1.50 | 0 | 0 | 0 | Could add on-device latency vs energy formula |
| `module-58/section-58.4.html` (FlashAttention-4) | 1.50 | 0 | 0 | 0 | **Top-30 #25**: IO-aware tiling pseudocode, online-softmax recurrence, FA-4 asymmetric pipeline |
| `module-58/section-58.5.html` (Training-Inference Co-Design) | 1.50 | 1 | 0 | 9 | **Top-30 #26**: Sardana 2024 inference-aware optimum equation `C_total = C_train + V * C_inf`, co-optimal solution |
| `module-59/section-59.1.html` (Distributed Training Fundamentals) | 2.25 | 90 | 0 | 1 | Has lots of math; could add 1F1B numbered Algorithm |
| `module-59/section-59.2.html` (ZeRO, FSDP) | 2.75 | 68 | 0 | 0 | OK; could add per-stage memory-budget table |
| `module-59/section-59.3.html` (Megatron, Tensor Parallelism) | 3.25 | 118 | 0 | 0 | Strong |
| `module-59/section-59.4.html` (Pipeline Parallelism) | 3.25 | 96 | 0 | 0 | Strong |
| `module-59/section-59.5.html` (Production Training Infra) | 3.75 | 91 | 1 | 0 | Strong |
| `module-60/section-60.1.html` (Why Edge Deployment) | 1.50 | 10 | 0 | 0 | Already has math |
| `module-60/section-60.2.html` (Edge Framework Landscape) | 1.00 | 0 | 0 | 0 | Catalog; OK |
| `module-60/section-60.3.html` (Hardware Constraints) | 1.50 | 0 | 0 | 3 | Memory-bound vs compute-bound formal regime split |

### Part XIII: LLMOps Lifecycle

| Section | Depth | Math | Algo | Named | Suggested additions |
|---|---:|---:|---:|---:|---|
| `module-62/section-62.1.html` (Scaling, Performance, Production Guardrails) | 3.50 | 0 | 2 | 2 | Strong |
| `module-62/section-62.2.html` (LLMOps, Continuous Improvement) | 0.50 | 0 | 0 | 0 | Operational; OK |
| `module-63/section-63.1.html` (Gateway Pattern) | 0.50 | 0 | 0 | 0 | Operational; OK |
| `module-63/section-63.2.html` (Routing, Reliability) | 1.75 | 3 | 0 | 0 | **Top-30 #27**: RouteLLM threshold-routing, cost-aware bandit, queue M/M/c backpressure, exp-backoff with jitter |
| `module-63/section-63.3.html` (Caching, Cost Mgmt) | 1.25 | 4 | 0 | 0 | Could add cache-hit-rate vs cost-saving Bayesian formulation |
| `module-64/section-64.1-4.html` (Durable Execution, Workflow Frameworks) | 0.0 to 0.5 | 0 | 0 | 0 | Operational by design; OK (all four sections) |
| `module-65/section-65.x` (Docker, Kubernetes) | 0.0 to 1.0 | 0-1 | 0 | 0-15 | Operational; OK |
| `module-66/section-66.1.html` (Reliability Engineering) | 1.25 | 3 | 0 | 0 | SLO error-budget burndown, availability product (`A_1 * A_2 * ...`) |
| `module-66/section-66.2.html` (Model Registry) | 1.50 | 0 | 0 | 10 | Operational; OK |

### Part XV: Frontiers (XV labeling - XIV is industries-of-applications, mostly skipped)

| Section | Depth | Math | Algo | Named | Suggested additions |
|---|---:|---:|---:|---:|---|
| `module-75/section-75.1.html` (Emergent Abilities) | 2.00 | 0 | 0 | 0 | **Top-30 #28**: Schaeffer "Mirage" derivation (linear vs discontinuous metric scaling), Wei counter-evidence, formal scale-vs-capability |
| `module-75/section-75.2.html` (Scaling Frontiers) | 2.75 | 5 | 0 | 15 | Already strong |
| `module-75/section-75.3.html` (Alt Architectures: Mamba, RWKV) | 5.00 | 43 | 2 | 0 | OK |
| `module-75/section-75.4.html` (Beyond Text) | 2.25 | 0 | 0 | 3 | Sequence-modeling-as-universal-prior framing |
| `module-76/section-76.1.html` (Theory of Reasoning) | 3.50 | 39 | 0 | 0 | **Top-30 #29**: Merrill-Sabharwal expressiveness, depth-vs-width formal, TC^0 limits |
| `module-76/section-76.2.html` (Memory as Computation Primitive) | 2.50 | 13 | 0 | 0 | Could add associative memory capacity (Hopfield N/log N) |
| `module-76/section-76.3.html` (Mech Interp at Scale) | 3.00 | 24 | 0 | 0 | Already strong |
| `module-76/section-76.4.html` (Nature of Agency) | 2.00 | 0 | 0 | 0 | Could add bounded-rationality / utility-function elicitation formalization |
| `module-77/section-77.1.html` (Frontier Benchmarks) | 1.50 | 0 | 0 | 5 | Could add IRT (item response theory) scoring for HLE / ARC-AGI-2 |
| `module-77/section-77.2.html` (Alignment at Frontier Scale) | 1.50 | 0 | 0 | 23 | **Top-30 #30**: weak-to-strong PGR formula, SAE-steering as feature clamping, formal Burns et al. setup |
| `module-77/section-77.3.html` (AGI Timelines) | 0.00 | 0 | 0 | 0 | Survey by design; OK |
| `module-77/section-77.4.html` (Economic Implications) | 0.50 | 0 | 0 | 0 | Survey by design; OK |
| `module-77/section-77.5.html` (What 2026 Settled) | 2.00 | 0 | 0 | 3 | Closing synthesis; OK |

### Sections explicitly judged OK at current depth (no upgrade needed)

22 sections currently scored at depth 5.0 and 31 at depth 4+ are at or near
research-paper depth and require no upgrade for theory content. They are the
benchmark for what "depth 5" means in this book: sections 3.1, 3.1b, 3.3, 3.4,
3.6, 6.3, 8.1, 8.3, 8.5, 9.2, 9.3, 9.7, 18.1a, 18.2a, 31.2a, 31.5, 49.1,
50.1, 53.2, 55.1, 75.3.

## 5. Suggested Wave Plan (Optional)

A single follow-on wave that picks 30 sections from the Top-30 list above
and authors one Algorithm callout + 1-2 inline math equations per section
would land approximately 50 to 60 numbered algorithms and 60+ formal
statements across the book. That delta would lift the mean depth of the
in-scope sections from ~1.8 to ~2.5 and the share of sections at depth >= 3
from 21% to ~35%, putting the book solidly in the "graduate textbook" tier
rather than its current "advanced-practitioner" position. The work
naturally chunks by Part: Part I-II (~10 sections), Part IV-V (~7), Part
VII-IX (~8), Part X-XII (~4), Part XV (~3).

Lower-priority Pattern B and Pattern C additions could be authored in a
second wave at the same per-section effort and would raise the same metric
to ~2.9 and ~50% respectively.
