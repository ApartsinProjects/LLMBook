# Scientific Depth Additions

Pass conducted on branch `v2.0` (2026-05-18). Section-by-section audit of the
ten foundational chapters listed in the task brief, with **24 HIGH-priority
algorithm callouts authored in-place** and additional MED/LOW gaps recorded
here for follow-up.

The added callouts use the canonical structure
(`<div class="callout algorithm">` + `<div class="callout-title">Algorithm
N.M.P: Name</div>` + `<pre><code class="pygments-highlighted
lang-text">...</code></pre>` + commentary `<p>` with an arXiv or paper
citation). All math is canonical `$...$` / `$$...$$`; no em-dashes.

## 1. Summary

| Module | HIGH inserted | MED noted | LOW noted |
|---|---:|---:|---:|
| 3  (Transformer Architecture)        | 5 | 2 | 1 |
| 6  (Pretraining & Scaling Laws)      | 2 | 1 | 0 |
| 8  (Reasoning & Test-Time Compute)   | 2 | 1 | 0 |
| 9  (Inference Optimization)          | 2 | 2 | 1 |
| 18 (Alignment, RLHF, DPO)            | 3 | 1 | 0 |
| 31 (Embeddings & Vector DB)          | 5 | 0 | 1 |
| 35 (Advanced RAG)                    | 2 | 1 | 0 |
| 42 (Evaluation Foundations)          | 4 | 1 | 0 |
| 46 (LLM-as-Judge)                    | 1 (upgraded) | 1 | 0 |
| **Total**                            | **24+1 upgrade** | **10** | **3** |

Audit deltas after all insertions:
- `_audit_callout_format.py`: 5325 -> 5349 callouts (+24), non-standard
  unchanged at 822 then 821 (a previously unnumbered Algorithm callout in
  46.2 was fixed during this pass).
- `_audit_numbering_consistency.py`: 85 flagged files, identical breakdown
  to baseline (no new phantom refs, no new drift). FIGURE_SEQUENCE,
  DUP_FIGURE_NUM, CALLOUT_NON_CANONICAL: no regressions.

## 2. HIGH-priority additions (authored in-place)

### Module 3: Transformer Architecture

| File | Algorithm | Citation |
|---|---|---|
| `part-1-llm-building-blocks/module-03-transformer-architecture/section-3.1.html` | Algorithm 3.1.1: Scaled Dot-Product Attention (Forward Pass) | Vaswani et al., NeurIPS 2017, arXiv:1706.03762 |
| `part-1-llm-building-blocks/module-03-transformer-architecture/section-3.1.html` | Algorithm 3.1.2: Pre-LN Decoder-Only Transformer Forward Pass | Xiong et al., ICML 2020, arXiv:2002.04745 |
| `part-1-llm-building-blocks/module-03-transformer-architecture/section-3.5.html` | Algorithm 3.5.1: Rotary Position Embedding (RoPE) | Su et al., arXiv:2104.09864, 2021 |
| `part-1-llm-building-blocks/module-03-transformer-architecture/section-3.5.html` | Algorithm 3.5.2: MHA, GQA, MQA as a Single Parameter Family | Shazeer 2019 + Ainslie et al. 2023 |
| `part-1-llm-building-blocks/module-03-transformer-architecture/section-3.8.html` | Algorithm 3.8.1: Top-k MoE Routing with Load-Balancing Loss | Shazeer 2017 + Fedus et al. 2021 |

### Module 6: Pretraining & Scaling Laws

| File | Algorithm | Citation |
|---|---|---|
| `part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.3.html` | Algorithm 6.3.1: Chinchilla Compute-Optimal Allocation | Hoffmann et al., NeurIPS 2022, arXiv:2203.15556 |
| `part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.3.html` | Algorithm 6.3.2: Inference-Aware (Sardana-Frankle) Compute Allocation | Sardana et al., ICML 2024, arXiv:2401.00448 |

### Module 8: Reasoning & Test-Time Compute

| File | Algorithm | Citation |
|---|---|---|
| `part-2-understanding-llms/module-08-reasoning-test-time-compute/section-8.1.html` | Algorithm 8.1.1: Self-Consistency Decoding (Majority Vote over CoT Samples) | Wang et al., ICLR 2023, arXiv:2203.11171 |
| `part-2-understanding-llms/module-08-reasoning-test-time-compute/section-8.5.html` | Algorithm 8.5.1: Monte Carlo Tree Search for Reasoning (MCTS-LLM) | Zhou et al., LATS, arXiv:2310.04406; AlphaProof (DeepMind 2024) |

### Module 9: Inference Optimization

| File | Algorithm | Citation |
|---|---|---|
| `part-2-understanding-llms/module-09-inference-optimization/section-9.4.html` | Algorithm 9.4.1: Lossless Speculative Decoding (Modified Rejection Sampling) | Leviathan et al., ICML 2023, arXiv:2211.17192 + Chen et al., arXiv:2302.01318 |
| `part-2-understanding-llms/module-09-inference-optimization/section-9.9.html` | Algorithm 9.9.1: Online Softmax Recurrence | Milakov and Gimelshein, arXiv:1805.02867; used by FlashAttention, Dao 2022 |

### Module 18: Alignment, RLHF, DPO

| File | Algorithm | Citation |
|---|---|---|
| `part-4-training-adaptation/module-18-alignment-rlhf-dpo/section-18.1.html` | Algorithm 18.1.1: Bradley-Terry Reward Model from Pairwise Preferences | Bradley and Terry 1952; Christiano et al. 2017; Ouyang et al. (InstructGPT) 2022 |
| `part-4-training-adaptation/module-18-alignment-rlhf-dpo/section-18.1.html` | Algorithm 18.1.2: PPO training loop for RLHF (renumbered from Algorithm 19.1.3) | Schulman et al. 2017 |
| `part-4-training-adaptation/module-18-alignment-rlhf-dpo/section-18.2.html` | Algorithm 18.3.1: DPO vs PPO Loss Contrast | Rafailov et al., NeurIPS 2023, arXiv:2305.18290 |

### Module 31: Embeddings & Vector DB

| File | Algorithm | Citation |
|---|---|---|
| `part-7-retrieval-information-extraction-with-llms/module-31-embeddings-vector-db/section-31.1.html` | Algorithm 31.1.1: Matryoshka Representation Learning (MRL) Training Objective | Kusupati et al., NeurIPS 2022, arXiv:2205.13147 |
| `part-7-retrieval-information-extraction-with-llms/module-31-embeddings-vector-db/section-31.2.html` | Algorithm 31.3.1: HNSW Approximate Nearest-Neighbor Search | Malkov and Yashunin, IEEE TPAMI 2020, arXiv:1603.09320 |
| `part-7-retrieval-information-extraction-with-llms/module-31-embeddings-vector-db/section-31.2.html` | Algorithm 31.3.2: IVF (Inverted-File) Two-Stage Search | Jegou, Douze, Schmid, IEEE TPAMI 2011 |
| `part-7-retrieval-information-extraction-with-llms/module-31-embeddings-vector-db/section-31.2.html` | Algorithm 31.3.3: Product Quantization: Encode and Asymmetric Distance Computation | Jegou, Douze, Schmid, IEEE TPAMI 2011 |
| `part-7-retrieval-information-extraction-with-llms/module-31-embeddings-vector-db/section-31.8.html` | Algorithm 31.8.1: ColBERT MaxSim (Late Interaction) Scoring | Khattab and Zaharia, SIGIR 2020, arXiv:2004.12832 |

### Module 35: Advanced RAG (chosen over Module 32 for the BM25/RRF math placement)

| File | Algorithm | Citation |
|---|---|---|
| `part-7-retrieval-information-extraction-with-llms/module-35-advanced-rag/section-35.1.html` | Algorithm 35.2.1: BM25 Term-Weighting and Document Scoring | Robertson and Walker, SIGIR 1994 |
| `part-7-retrieval-information-extraction-with-llms/module-35-advanced-rag/section-35.1.html` | Algorithm 35.1.2: Reciprocal Rank Fusion (RRF) for Hybrid Retrieval | Cormack, Clarke, Buettcher, SIGIR 2009 |

### Module 42: Evaluation Foundations

| File | Algorithm | Citation |
|---|---|---|
| `part-9-llm-evaluation-observability/module-42-evaluation-foundations/section-42.12.html` | Algorithm 42.12.1: BLEU-N | Papineni et al., ACL 2002 |
| `part-9-llm-evaluation-observability/module-42-evaluation-foundations/section-42.12.html` | Algorithm 42.12.2: ROUGE-N and ROUGE-L | Lin, ACL 2004 Workshop |
| `part-9-llm-evaluation-observability/module-42-evaluation-foundations/section-42.12.html` | Algorithm 42.12.3: Perplexity from Cross-Entropy | with Henighan et al., arXiv:2010.14701 (bits-per-byte for cross-tokenizer comparison) |
| `part-9-llm-evaluation-observability/module-42-evaluation-foundations/section-42.10.html` | Algorithm 42.10.1: Cohen's Kappa and Fleiss' Kappa for Inter-Rater Agreement | Cohen 1960; Fleiss 1971; Krippendorff 2018 |

### Module 46: LLM-as-Judge (upgrade)

| File | Algorithm | Citation |
|---|---|---|
| `part-9-llm-evaluation-observability/module-46-llm-as-judge-automated-evaluation/section-46.2.html` | Algorithm 46.2.1: G-Eval Probability-Weighted Scoring (added explicit pseudocode block; previously prose-only with the math identity) | Liu et al., EMNLP 2023, arXiv:2303.16634 |

## 3. Sample before/after (HIGH addition)

The cleanest illustrative case is **Algorithm 3.1.1** in
`part-1-llm-building-blocks/module-03-transformer-architecture/section-3.1.html`.
Before: the section opened with the closed-form
$\operatorname{Attention}(Q, K, V) = \operatorname{softmax}(QK^T/\sqrt{d_k}) V$
and a Key Insight callout about the $\sqrt{d_k}$ scaling, but the canonical
**six-step procedural form** (project to Q/K/V, score, mask, softmax,
weighted sum, output projection) did not appear anywhere in the chapter.
The textbook treatment of attention thus lacked the formal algorithm
callout that any reader would expect to cite.

After: a numbered Algorithm 3.1.1 with explicit pseudocode, tensor shapes,
arxiv citation, and a forward pointer to FlashAttention. The callout uses
`<pre><code class="pygments-highlighted lang-text">` (not `lang-python`),
keyword capitalization, and concludes with a one-line commentary plus the
arxiv link to Vaswani et al. 2017.

Two more illustrative additions:

- **Algorithm 18.3.1 (DPO vs PPO Loss Contrast)** in section-18.2.html.
  Before: each loss appeared on its own page with $L_\text{DPO}$ derived
  symbolically but no side-by-side update rule. After: a single Algorithm
  callout shows the PPO inner loop (sample, KL-shaped reward, GAE,
  clipped surrogate, value + entropy terms; 4 models in GPU) directly
  alongside the DPO step (offline pair, implicit reward via log-ratio, BT
  loss; 2 models in GPU), with the Rafailov et al. equivalence theorem and
  the trade-offs (on-policy vs offline, reusable reward vs implicit).

- **Algorithm 31.3.1 (HNSW search)** in section-31.2.html.
  Before: prose described "start at the top layer, descend, beam search at
  layer 0" but the explicit greedy-descent + ef-beam-search structure was
  not given in a callout. After: a numbered Algorithm callout with
  SEARCH-LAYER-GREEDY and SEARCH-LAYER-BEAM expanded, the min-heap /
  max-heap invariants, complexity analysis O(log N) expected, and the
  Malkov-Yashunin TPAMI 2020 citation.

## 4. Med-priority gaps noted (not inserted)

These are real depth gaps but lower pedagogical leverage; recommend
authoring in a follow-up pass.

- **3.1.6 Position-Wise FFN**: needs an explicit Algorithm callout
  contrasting ReLU FFN vs SwiGLU FFN with shape annotations
  `[B, T, d] -> [B, T, 4d] -> [B, T, d]`.
- **3.1.8 LayerNorm / RMSNorm**: needs Algorithm callout for the
  two normalizations side-by-side (mean+variance vs RMS-only).
- **6.3.5 Data-Constrained Scaling**: needs an Algorithm callout for the
  Muennighoff et al. 2024 effective-token formula
  $D_\text{eff} \approx D_\max (1 - e^{-R})$ with a worked example.
- **8.3.2 GRPO**: needs Algorithm callout for DeepSeek's
  Group Relative Policy Optimization (the GRPO advantage = (r - mean(r)) /
  std(r) over a group of N completions, PPO-style clip).
- **9.2.1 GPTQ + AWQ**: needs Algorithm callouts for GPTQ's Hessian-based
  weight update (block iteration with error compensation) and AWQ's
  activation-aware per-channel scaling.
- **9.3.4 MHA/MQA/GQA architectural deep dive**: redundant with
  Algorithm 3.5.2 above; cross-reference rather than duplicate.
- **18.3 KTO/IPO/ORPO/SimPO**: these are DPO variants and could share
  one Algorithm callout that parameterizes the family by their margin /
  reference treatment.
- **35.1.3 Cross-encoder reranking**: needs a small Algorithm callout for
  the cross-encoder forward pass and the two-stage retrieve-then-rerank
  pattern.
- **42.2 Bootstrap / paired tests**: paired bootstrap test could be lifted
  into an Algorithm callout (currently in prose + code).
- **46.3 Pairwise Bradley-Terry from LLM judge comparisons**: needs an
  Algorithm callout (reuse the BT objective from 18.1.1).

## 5. Low-priority gaps noted (not inserted)

- **3.5.3 Sliding-window + sink-token attention**: nice-to-have Algorithm
  callout for the mask construction.
- **9.4.4 EAGLE / 9.4.5 Medusa**: tree-attention verification could get an
  Algorithm callout if the chapter expands.
- **31.4 Embedding model distillation**: KD objective is generic, not
  specific to embeddings; lower leverage.

## 6. Notes on the canonical format

All inserted callouts follow the structure required by `_audit_callout_format.py`:
- title text starts `Algorithm N.M.P:` (regex enforced)
- body uses a single `<pre><code class="pygments-highlighted lang-text">`
  pseudocode block (per CONTENT_GUIDELINES section 8.1, real Python is
  Code-Fragment territory)
- pseudocode uses capitalized keywords (`Algorithm:`, `Input:`, `Output:`,
  `For`, `If`, `Return`) and ASCII pseudo-math (`sum_i`, `argmax`)
- one short commentary `<p>` immediately follows, containing the citation
  link (arxiv `arXiv:NNNN.NNNNN` with anchor to abs page, or a
  `https://doi.org/...` link).
- no em-dashes; commas, semicolons, colons, parens only.
