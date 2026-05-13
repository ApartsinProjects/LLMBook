# Shallow Audit Plan: Part IV (Modules 13, 14, 15, 16/17)

**Scope:** Sections 13.1-13.7, 14.1-14.7, 15.1-15.7, 16.1-16.5 (formerly 17)
**Audit date:** 2026-05-12
**Findings cap:** 100
**Note:** Sections assessed as solid depth are marked GOOD. No HTML files were modified.

---

## MODULE 13: Synthetic Data

### GOOD: section-14.1.html
Multiple callout types (key-insight, warning, practical-example), concrete `QualityMetrics` dataclass, model collapse failure modes, legal/licensing table, full lifecycle diagram.

### GOOD: section-14.3.html
`QualityScore` dataclass, exact dedup via SHA-256, MinHash with `datasketch`, semantic dedup, paraphrase pipeline with goldilocks similarity band (0.85-0.97), composable `FilterPipeline`.

### GOOD: section-14.6.html
Verification-first framing, rejection sampling with n=64 justified, domain-specific verification strategy table, R1-style distillation pipeline.

---

**Finding 1** | section-13.2 | Code Fragment 14.2.3 caption says "Implement Evol-Instruct" but the function is persona-driven generation
Classification: **MISSING-EXAMPLE** (label/content mismatch)
Action: **NEW-WORKED-EXAMPLE** or fix caption — show one seed instruction passed through 2 depth + 1 breadth mutations.

**Finding 2** | section-13.4 | Annotation tools table (Label Studio, Prodigy, Argilla) with brief descriptions, no selection guidance.
Classification: **SHOPPING-LIST**
Action: **DROP-NAMING** or **ADD-CALLOUT-BOX: practical-example** — consolidate to one tool with integration code.

**Finding 3** | section-13.5 | "The label model estimates the latent true labels using a generative model that accounts for each LF's accuracy and correlations..."
Classification: **MISSING-INTUITION**
Action: **ADD-CALLOUT-BOX: algorithm** — show the generative model formally with a 3-LF example.

**Finding 4** | section-13.7 | Multi-turn augmentation listed but only described in prose, no code (single-turn has code).
Classification: **MISSING-EXAMPLE**
Action: **NEW-WORKED-EXAMPLE** — `augment_conversation` function + before/after 3-turn dialogue.

---

## MODULE 14: Fine-Tuning Fundamentals

### GOOD: section-15.3.html
Response masking diagram, full `SFTConfig`, scheduler visualization, "desirable difficulty" analogy.

---

**Finding 5** | section-14.1 | "SISA training... gradient ascent... membership inference attacks" — 4 distinct techniques in rapid succession.
Classification: **SHOPPING-LIST**
Action: **DEEPEN-HERE** — explain why naive gradient ascent destabilizes models and how bounded variant works.

**Finding 6** | section-14.1 | "adapting SISA to LLM pretraining remains an open challenge" — no explanation of WHY.
Classification: **MISSING-FAILURE-MODE**
Action: **ADD-FAILURE-MODE-NOTE** — SISA needs partition isolation, broken by dense attention's joint distribution dependency.

**Finding 7** | section-14.2 | "Microsoft showed that training Phi on just 6 billion tokens of carefully curated 'textbook quality' data achieved results comparable to models trained on 1 trillion tokens..."
Classification: **MISSING-INTUITION** (unjustified comparative claim)
Action: **DEEPEN-HERE** — cite Gunasekar et al. 2023, explain mechanism (high-density structured data vs surface-pattern web text).

**Finding 8** | section-14.4 | Vertex AI section is one-third the depth of OpenAI section.
Classification: **ONE-PARAGRAPH-INTRO**
Action: **DEEPEN-HERE** — add LoRA-by-default note, monitoring code, cost estimate to match OpenAI section.

**Finding 9** | section-14.5 | `CosineSimilarityLoss` vs `MultipleNegativesRankingLoss` introduced with code but no decision guidance.
Classification: **MISSING-EXAMPLE**
Action: **ADD-CALLOUT-BOX: key-insight** — explicit "use X when..." rule.

**Finding 10** | section-14.6 | "or a small MLP" mentioned as classification head alternative without explaining when justified.
Classification: **ONE-PARAGRAPH-INTRO**
Action: **DEEPEN-HERE** — explain when MLP head helps (rare) vs linear (default).

**Finding 11** | section-14.7 | YaRN named as "recommended default for context >4x training length" but no formula or code.
Classification: **ONE-PARAGRAPH-INTRO**
Action: **DEEPEN-HERE** — explain frequency-dependent scaling + temperature correction. Add config snippet.

---

## MODULE 15: PEFT

### GOOD sections: 15.1, 15.4, 15.5, 15.6, 15.7
LoRA full FT memory problem motivated, intrinsic dimensionality, init rationale (A=Gaussian, B=zeros), QLoRA NF4, multi-tenant serving, Prompt/Prefix/P-Tuning taxonomy, distillation with information-theoretic grounding, T^2 scaling, white-box vs black-box, model merging (linear mode connectivity, task vector arithmetic, SLERP, TIES, DARE), continual learning (EWC formula, rubber-band analogy, ReplayDataset).

---

**Finding 12** | section-15.2 | "IA3 adds learned rescaling vectors..." — operation never stated formally.
Classification: **MISSING-INTUITION**
Action: **ADD-CALLOUT-BOX: algorithm** — show $\text{Attention}(Q, K \odot l_k, V \odot l_v)$ formula.

**Finding 13** | section-15.3 | Axolotl YAML config shown without warning about common silent misconfigurations.
Classification: **MISSING-FAILURE-MODE**
Action: **ADD-FAILURE-MODE-NOTE** — sample_packing+pad_to_sequence_len double-padding, lora_alpha mismatch, missing trust_remote_code.

**Finding 14** | section-15.3 | LLaMA-Factory, torchtune, TRL named as alternatives without selection rules.
Classification: **SHOPPING-LIST** (creates 6-tool landscape: Unsloth, Axolotl, LLaMA-Factory, torchtune, TRL, plain transformers)
Action: **DROP-NAMING** or add decision paragraph for each.

**Finding 15** | section-15.2 | DoRA description: decomposes W into magnitude m and direction — formula and intuition not given.
Classification: **MISSING-INTUITION**
Action: **ADD-CALLOUT-BOX: algorithm** — show $W = m \cdot (V/||V||)$ + intuition for decoupling.

---

## MODULE 16: Alignment, RLHF, DPO (formerly 17)

### GOOD sections: 16.1, 16.2, 16.3, 16.4
Alignment-as-principal-agent motivation, full PPO pseudocode, KL penalty failure mode (reward hacking), Constitutional AI two-phase pipeline with diagram, alignment tax table (-2.1% MMLU, +35.3% TruthfulQA), RLVR vs RLHF reward signal contrast, GRPO with group normalization.

---

**Finding 16** | section-16.2 | ORPO described in 2 sentences with note callout but no formula.
Classification: **ONE-PARAGRAPH-INTRO**
Action: **DEEPEN-HERE** — show ORPO loss with odds ratio replacing log-prob ratio. Add `ORPOConfig` code.

**Finding 17** | section-16.2 | SimPO described in 3 sentences with no formula and no code.
Classification: **ONE-PARAGRAPH-INTRO**
Action: **DEEPEN-HERE** — show length-normalized loss with target margin γ. Explain length bias correction.

**Finding 18** | section-16.5 | Recursive reward modeling notes "principal risk is error accumulation" but no concrete failure example.
Classification: **MISSING-FAILURE-MODE**
Action: **ADD-FAILURE-MODE-NOTE** — sycophantic level-1 assistant misleads level-2 evaluators by confirming wrong assessments.

**Finding 19** | section-16.5 | "16.5.3 Interpretability-Based Alignment... Sparse Autoencoders" — feature-based intervention not concretely shown.
Classification: **MISSING-EXAMPLE**
Action: **NEW-WORKED-EXAMPLE** — "feature 742 = deceptive hedging; clamp via $h \leftarrow h - \alpha v_{742}$; Anthropic's sycophancy result: 40% reduction with minimal quality loss."

**Finding 20** | section-16.5 | "Ratio of capability researchers to alignment researchers heavily skewed toward capabilities" — claim without evidence.
Classification: **MISSING-INTUITION** (unjustified)
Action: **DEEPEN-HERE** — cite 80,000 Hours / Time reporting (5-15% range, depends on definition).

**Finding 21** | section-16.1 | Reward Model Training section: `RewardTrainer` shown but Bradley-Terry loss never stated.
Classification: **MISSING-INTUITION**
Action: **ADD-CALLOUT-BOX: algorithm** — show $L_{RM} = -\log \sigma(r(x, y_w) - r(x, y_l))$ with margin interpretation.

---

## SUMMARY

**Total findings: 21** (under 100 cap).

**Strongest:** Modules 15 (PEFT) and 16 (Alignment) — sections 15.1, 15.5, 15.6, 16.1, 16.2, 16.3 hit publication-grade depth.

**Most concentrated issues:** Module 15 (machine unlearning shopping-list, Phi claim, thin Vertex AI, three "or alternatively" without selection guidance).

**Priority order for remediation:**
1. Finding 1 (Evol-Instruct caption mismatch) — actively misleads
2. Finding 12 (IA3 formula missing) — entire mechanism
3. Finding 7 (Phi claim unjustified)
4. Finding 5 (gradient ascent mechanism)
5. Finding 3 (Snorkel label model math)
6. Findings 16-17 (ORPO/SimPO formulas)
7. Finding 21 (Bradley-Terry loss)
8. Findings 9, 10 (loss/head selection)
9. Finding 11 (YaRN no code)
10. Findings 13, 18, 6 (failure modes)
