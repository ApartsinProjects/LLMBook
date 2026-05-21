# Mental Model Opportunities: Execution Report

Date: 2026-05-20
Operator: mental-model agent (Claude Opus 4.7)
Source: `docs/content-audit/MENTAL_MODEL_OPPORTUNITIES.md` (95 opportunities flagged)
Target: top 8 HIGHEST-priority items, text-only round (no new figures)

## Summary

Executed 8 of 8 items. Total words added: ~1,677 (average 210 words per insertion). All eight inserted as `<div class="callout key-insight">` callouts directly after the math derivation or dense definition they motivate, so the reader hits the intuition while the symbols are still warm. Final audit (`P0+P1`) returned only 2 unrelated TODO placeholders in deep-dive agent files (sections 7.3 and 40.1); none of my edits introduced issues.

### Substitution from the user's list

Item 1 in the user's brief was **RoPE clock-hands (Section 3.5)**, but that file is in the deep-dive agent's no-touch list. Per the brief's instruction to "choose a different mental model from the report's longer list" when sections overlap, I substituted **Lost-in-the-Middle bored party guest (Section 32.1.4.1)**, which the audit also flags as HIGH priority and "the single most-cited RAG failure mode". All other selections matched the user's list.

## Per-item details

### 1. KL leash for PPO (Section 18.1.3.3)

- **File**: `part-4-training-adaptation/module-18-alignment-rlhf-dpo/section-18.1.html`
- **Anchor**: Immediately after the `<h3 id="18-1-3-3-kl-penalty-and-reward-shaping">` paragraph that introduces the shaped reward $r_{\text{shaped}} = r_{\text{RM}} - \beta \cdot \text{KL}(\pi \| \pi_{\text{ref}})$ and explains the adaptive KL controller.
- **Analogy**: Dog on an elastic leash. Policy = dog, reference model = handler, reward model = trail of treats winding through the park. Small β = long leash (dog wanders far chasing reward, risks hacking), large β = short leash (dog stays close, barely improves). Adaptive controller = handler tugging or releasing slack based on drift.
- **Callout type**: `key-insight`
- **Title**: "β as an elastic leash"
- **Word count**: ~192
- **Source**: Folk wisdom in the RLHF community; no citation needed.

### 2. PPO clip range as mountain pass (Section 18.1.3.2)

- **File**: `part-4-training-adaptation/module-18-alignment-rlhf-dpo/section-18.1.html`
- **Anchor**: Immediately after the paragraph that introduces $L^{\text{CLIP}}$, the clip range $\epsilon = 0.2$, and the "trust region" framing (before the numeric walkthrough code).
- **Analogy**: Surrogate objective as a mountain ridge. Each update is a step along the ridge; the terrain is only well-mapped near the current policy. The clip range is a fence on either side of the trail: push hard within $[1-\epsilon, 1+\epsilon]$, but step outside and the objective flattens (gradient evaporates). The flat shoulder is by design: outside the clip the surrogate stops being a faithful map of the true objective (the on-policy/off-policy gap).
- **Callout type**: `key-insight`
- **Title**: "The clip range as a mountain pass"
- **Word count**: ~183
- **Source**: Folk wisdom; the trust-region framing is original to Schulman et al., "Proximal Policy Optimization Algorithms," 2017 (already cited in the section).

### 3. GRPO grading on a curve (Section 18.2.1.1)

- **File**: `part-4-training-adaptation/module-18-alignment-rlhf-dpo/section-18.2.html`
- **Anchor**: Immediately after the paragraph explaining the z-score normalization advantage formula $A_i = (r_i - \text{mean}(\mathbf{r})) / (\text{std}(\mathbf{r}) + \epsilon)$, before the numeric walkthrough code fragment.
- **Analogy**: PPO's value network as a salaried TA who predicts what an average answer is worth. GRPO fires the TA and grades on a curve, prompt by prompt: for each prompt, generate G answers, compute group mean, every answer is now z-scored against its classmates. The same raw reward 0.8 stands out vs. classmates {0.2, 0.5, 0.3} but is unremarkable vs. {0.75, 0.8, 0.85}. Absolute reward scale drops out; only relative standing matters. Connects naturally to DeepSeek-R1's choice.
- **Callout type**: `key-insight`
- **Title**: "Grading on a curve, prompt by prompt"
- **Word count**: ~189
- **Source**: Original framing; the GRPO mechanism is from Shao et al., "DeepSeekMath," 2024 (already cited).

### 4. DPO scale-tilt margin (Section 18.3.1)

- **File**: `part-4-training-adaptation/module-18-alignment-rlhf-dpo/section-18.3.html`
- **Anchor**: Immediately after the DPO loss formula $L_{\text{DPO}} = -\mathbb{E}[\log \sigma(\beta(\dots))]$ derivation, before the "DPO vs PPO Loss Contrast" algorithm callout.
- **Analogy**: A kitchen balance scale. Left pan = chosen response $y_w$, right pan = rejected $y_l$, with each pan loaded by the log-ratio $\log \pi(y \mid x) - \log \pi_{\text{ref}}(y \mid x)$. The signed gap times $\beta$ is the margin; the sigmoid converts it to a probability of correct re-ranking. Training is the slow tilt: gradients concentrate on the borderline pairs near balance (saturated sigmoid kills gradient on already-tipped pairs). $\beta$ sets aggressiveness of the tilt.
- **Callout type**: `key-insight`
- **Title**: "Tilting the preference scale"
- **Word count**: ~219
- **Source**: Original; the DPO derivation is Rafailov et al., 2023 (already cited).

### 5. MoE routing parcels through a depot (Section 3.8.3.1)

- **File**: `part-1-llm-building-blocks/module-03-transformer-architecture/section-3.8.html`
- **Anchor**: Immediately after the `<div class="callout warning">` titled "Load Balancing" that introduces router collapse, and before "Algorithm 3.8.1: Top-k MoE Routing with Load-Balancing Loss".
- **Analogy**: Parcel depot at rush hour. Each token = parcel, router = dispatcher, $E$ experts = courier vans in numbered bays. Top-$k$ routing = dispatcher reads label and picks two best vans. Scaling argument: doubling vans doubles capacity without doubling per-parcel cost. Router collapse = dispatcher always picks vans 1 and 2 because they returned early reward; other vans idle. Auxiliary loss = depot manager with a clipboard penalizing the dispatcher whenever the hard statistic $f_i$ and the smooth statistic $p_i$ both concentrate on the same bay.
- **Callout type**: `key-insight`
- **Title**: "Routing parcels through a depot"
- **Word count**: ~216
- **Source**: Original framing; the load-balance loss is from Fedus et al., "Switch Transformer," 2021 (already cited).

### 6. KV-cache eviction as a conveyor belt of memos (Section 9.3.7.2)

- **File**: `part-2-understanding-llms/module-09-inference-optimization/section-9.3.html`
- **Anchor**: Immediately after the bulleted list defining H2O / Sliding Window / StreamingLLM, before the vLLM profiling code fragment.
- **Analogy**: Cache as a long conveyor belt of memos. Each new token drops a memo on the right end. Belt is too short to hold them all, so policies differ in what falls off the left end. **Sliding window** staples nothing (memos fall off freely). **H2O** walks the belt with a highlighter, pins the loudest (highest cumulative attention) memos in place. **StreamingLLM** staples the very first memos (attention sinks: softmax needs somewhere to dump probability mass) plus a recent window. Same belt, three staple policies; pick to match workload (streaming, long-range recall, simple chat).
- **Callout type**: `key-insight`
- **Title**: "A conveyor belt of memos"
- **Word count**: ~244
- **Source**: Original framing; the three policies are from Zhang et al. (H2O, 2023), Beltagy et al. (Longformer sliding window, 2020), and Xiao et al. (StreamingLLM/attention sinks, 2024).

### 7. Perplexity roulette wheel (Section 42.1.1 Perplexity subsection)

- **File**: `part-9-llm-evaluation-observability/module-42-evaluation-foundations/section-42.1.html`
- **Anchor**: Immediately after the PPL formula $\operatorname{PPL} = \exp(-\frac{1}{N} \sum \log P(\dots))$, before the "perplexity depends on the tokenizer" paragraph that motivates BPB.
- **Analogy**: Roulette wheel with $N$ equally-likely slots. PPL = the number of slots the wheel would need to deliver the same average surprise the model actually feels on real text. PPL 5 = narrowed to about 5 plausible choices; PPL 30 = about 30; PPL near vocab size = the wheel is the whole vocabulary (uniform-random baseline). Comparing PPL 12 to PPL 8 = shrunk the wheel from 12 slots to 8. Catch: the size of each slot depends on the tokenizer, which is exactly what BPB exists to fix; transitions naturally into the next subsection.
- **Callout type**: `key-insight`
- **Title**: "A roulette wheel with N slots"
- **Word count**: ~209
- **Source**: Original; "perplexity as effective branching factor" is folk wisdom in NLP textbooks (Jurafsky & Martin), no citation needed.

### 8. Lost-in-the-middle bored party guest (Section 32.1.4.1) [substituted for RoPE]

- **File**: `part-7-retrieval-information-extraction-with-llms/module-32-rag/section-32.1.html`
- **Anchor**: Immediately after the paragraph that introduces Liu et al. (2024) and the U-shaped attention pattern, before the existing `<div class="callout warning">` that lists mitigation strategies.
- **Analogy**: Model as a guest at a long dinner party with twenty people around the table. Listens attentively during introductions (start of context), perks up for the dessert chat next to it (end of context), zones out in the middle while seats 8-12 give their elevator pitches. Concrete numbers from Liu et al.: ~80% recall at head/tail, ~60% at positions 8-12. Three habits follow: retrieve fewer documents (3-5), sort by relevance and place top chunk first, rerank and push marginal chunks to the middle.
- **Callout type**: `key-insight`
- **Title**: "The bored party guest"
- **Word count**: ~225
- **Source**: Liu et al., "Lost in the Middle: How Language Models Use Long Contexts," 2024 (already cited in the section).

## Word-count totals

| # | Title | File | Words |
|---|-------|------|-------|
| 1 | β as an elastic leash | 18.1.html | 192 |
| 2 | The clip range as a mountain pass | 18.1.html | 183 |
| 3 | Grading on a curve, prompt by prompt | 18.2.html | 189 |
| 4 | Tilting the preference scale | 18.3.html | 219 |
| 5 | Routing parcels through a depot | 3.8.html | 216 |
| 6 | A conveyor belt of memos | 9.3.html | 244 |
| 7 | A roulette wheel with N slots | 42.1.html | 209 |
| 8 | The bored party guest | 32.1.html | 225 |
| | **TOTAL** | | **1,677** |

Average: 210 words/insertion. Items 6 and 8 ran slightly over the 200-word target because both required visualizing a three-way comparison (three eviction policies; three RAG mitigation habits) and a numeric anchor (recall percentages, staple positions).

## Choice of callout type

All eight inserts used `<div class="callout key-insight">`, because each analogy is meant to unlock understanding of a math derivation or dense definition the reader has just walked through (the brief's first option). No `fun-note` callouts were used: these are foundational concepts (PPO, DPO, GRPO, MoE, KV cache eviction, perplexity, lost-in-the-middle, RLHF leash) where the analogy is doing didactic work, not comic relief.

## Editorial constraints honored

- **No em dashes**: All analogies use commas, semicolons, colons, or parentheses for pauses. Verified by spot-check.
- **No new figures**: This was a text-only round; every insert is prose inside a callout.
- **No file conflicts with deep-dive agent**: Avoided 3.5 (RoPE), 22.1 (ViT), 22.3 (Q-Former), 75.2 (Mamba), 7.3 (DeepSeek), 26.2 (MCTS), 32.4 (RAG self-correction), 59.2/59.3 (ZeRO), 2.3 (attention), 40.1 (S2S). Substituted lost-in-the-middle (32.1) for RoPE clock-hands per brief.
- **Citations**: Folk metaphors (leash, mountain pass, courier vans, conveyor belt, roulette, dinner party) carry no citation; the underlying mechanisms (PPO, GRPO, DPO, MoE load balance, H2O/StreamingLLM, lost-in-the-middle) are already cited in their host sections.
- **Anchor stability**: All eight inserts target unique `<h3>` IDs (`18-1-3-2`, `18-1-3-3`, `18-2-1-1`, `18-3-1`, `9-3-7-2`, `32-1-4-1`) or unique callout siblings, so future automated edits will not collide.

## Audit verification

Final run of `agents.book-skills.scripts.audit.run --priority P0+P1 --root .` returned only 2 unrelated TODO placeholders, both in deep-dive agent files (`section-7.3.html:98`, `section-40.1.html:113`). No new issues introduced by this round.

## Notes on the 7 items NOT executed

From the TLDR's top-15, the seven HIGH-priority items not executed this round are good candidates for a follow-up round (they were ranked below the user's top-8 selection, or, in one case, conflict with the deep-dive agent):

- RoPE clock-hands (3.5) [deep-dive conflict]
- Sliding-window/H2O/StreamingLLM as a system (9.3.7) [partly addressed by item 6]
- Absmax/zero-point quantization shrinking-ruler (9.1.2)
- Reward hacking student-rubric divergence (18.2.2) [the existing "Key Insight" callout already covers the metaphor at a basic level]
- Speculative decoding relay-race (9.4) [partial visual already exists]
- MHA/MQA/GQA recipe-card chefs (9.3.4)
- ZeRO carpool stages (59.2) [deep-dive conflict]

These are listed in the original `MENTAL_MODEL_OPPORTUNITIES.md` for whoever picks up the next round.
