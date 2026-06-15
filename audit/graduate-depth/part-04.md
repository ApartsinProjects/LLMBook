# Graduate-Depth Audit: Part 4 (Training & Adaptation)

| Section | Title (short) | Verdict | Missing piece (only if not COURSE-READY) |
|---|---|---|---|
| 15.1 | Principles of Synthetic Data | COURSE-READY | |
| 15.2 | LLM-Powered Generation Pipelines | COURSE-READY | |
| 15.3 | Quality Assurance & Curation | COURSE-READY | |
| 15.4 | LLM-Assisted Labeling & Active Learning | DEPTH-GAP | Active-learning acquisition functions named but no uncertainty/entropy/BALD scoring math or stopping criterion |
| 15.5 | Weak Supervision & Programmatic Labeling | DEPTH-GAP | Snorkel label model (generative agreement model over LF outputs) stated conceptually; no derivation of how LF accuracies/correlations are estimated without ground truth |
| 15.6 | Synthetic Reasoning Data | COURSE-READY | |
| 15.7 | Data Augmentation for LLMs | COURSE-READY | |
| 16.1 | When and Why to Fine-Tune | COURSE-READY | |
| 16.2 | Data Preparation for Fine-Tuning | COURSE-READY | |
| 16.3 | Supervised Fine-Tuning (SFT) | COURSE-READY | |
| 16.4 | Fine-Tuning via Provider APIs | CATALOG-OK | |
| 16.5 | Fine-Tuning for Representation Learning | DEPTH-GAP | Contrastive objective discussed but InfoNCE/triplet loss not written as an equation; temperature and in-batch-negative mechanics under-derived |
| 16.6 | Fine-Tuning for Classification & Seq Tasks | COURSE-READY | |
| 16.7 | Adapting Models for Long Text | DEPTH-GAP | RoPE linear-interpolation scaling described; no derivation of the position-scaling factor or why NTK/YaRN beat naive interpolation |
| 17.1 | LoRA & QLoRA | COURSE-READY | |
| 17.2 | Advanced PEFT (DoRA, IA3, GaLore, rsLoRA) | COURSE-READY | |
| 17.3 | Training Platforms & Tools | CATALOG-OK | |
| 17.3a | Tool Comparison, Cloud, Workflows | CATALOG-OK | |
| 17.4 | Soft Prompts (Prompt/Prefix/P-Tuning) | COURSE-READY | |
| 17.5 | Knowledge Distillation: Foundations | COURSE-READY | |
| 17.6 | Distillation: Licensing, Speculative, Reasoning | COURSE-READY | |
| 17.7 | Model Merging & Composition | COURSE-READY | |
| 17.8 | Continual Learning & Domain Adaptation | COURSE-READY | |
| 18.1 | Alignment Problem & RLHF with PPO | COURSE-READY | |
| 18.2 | GRPO, Reward Hacking, Choosing a Method | COURSE-READY | |
| 18.3 | DPO: Derivation & Single-Model Alignment | COURSE-READY | |
| 18.4 | DPO Variants, Datasets & Iterative DPO | COURSE-READY | |
| 18.5 | Constitutional AI & Self-Alignment | COURSE-READY | |
| 18.6 | RLVR: Verifiable Rewards | COURSE-READY | |
| 18.7 | Alignment Research Frontiers | COURSE-READY | |
| 19.1 | Platforms | CATALOG-OK | |
| 19.2 | Libraries & Frameworks | CATALOG-OK | |
| 19.4 | (tools-of-the-trade) | CATALOG-OK | |
| 19.5 | (tools-of-the-trade) | CATALOG-OK | |
| 19.6 | (tools-of-the-trade) | CATALOG-OK | |
| 19.7 | (tools-of-the-trade) | CATALOG-OK | |
| 19.8 | (tools-of-the-trade) | CATALOG-OK | |
| 19.9 | (tools-of-the-trade) | CATALOG-OK | |
| 19.10 | Linking Experiment Runs to Git Commits | CATALOG-OK | |
| 19.11 | Weights & Biases Deep Dive | CATALOG-OK | |
| 19.12 | MLflow Deep Dive | CATALOG-OK | |
| 19.13 | Experiment Comparison & HPO | CATALOG-OK | |
| 19.14 | Distributed Training Deep Dive | CATALOG-OK | |
| 19.15 | Ray Train/Serve/Data | CATALOG-OK | |

## Summary
- COURSE-READY: 24 | DEPTH-GAP: 4 | NOT-SELF-CONTAINED: 0 | CATALOG-OK: 16

The math-heavy core of this part is strong. Every load-bearing alignment and PEFT mechanism is derived from its loss, not just described: 18.1 carries the SFT NLL, Bradley-Terry reward loss, PPO clipped surrogate with the explicit probability ratio, GAE via the TD residual, and the KL-shaped reward; 18.3 works the full DPO closed form including the Z(x) partition-function cancellation and the beta inverse-temperature/KL double-duty argument; 18.2 derives GRPO's group z-score advantage as a value-network replacement with a numeric example; 17.1 gives the LoRA forward/backward pass, alpha/r coupling, B=0 init, and the NF4 codebook; 17.5 carries the Hinton temperature-softened KL loss with the T-squared gradient-scaling factor. None of the four math-heavy modules has a derivation-free LoRA/RLHF/DPO/distillation section, so no hard penalty applies. The only depth gaps are in the data-labeling tail (15.4, 15.5) and two single-equation omissions (16.5 contrastive, 16.7 RoPE scaling).

Top sections most worth enriching:
1. 15.5 Weak Supervision: add the Snorkel label-model derivation (how LF accuracies and pairwise correlations are recovered from agreement statistics with no ground truth) so the "programmatic labels beat majority vote" claim is mechanistic, not asserted.
2. 16.5 Representation Learning: write the InfoNCE/triplet loss as an equation with the temperature term and in-batch-negative construction, so contrastive fine-tuning is derivable rather than narrated.
3. 16.7 Long Text: derive the RoPE linear-interpolation scaling factor and contrast it with NTK-aware/YaRN scaling, explaining why naive interpolation degrades high-frequency bands.
4. 15.4 LLM-Assisted Labeling: add at least one acquisition function (uncertainty/entropy or BALD) with its scoring formula plus a stopping criterion, so the active-learning loop is reproducible.
