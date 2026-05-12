# Shallow-Content Audit — Highlights

Six deep-explanation agents read every section of the book line-by-line and
produced per-part plans. Below is a consolidated summary of the **most
actionable findings** distilled across all 268 findings.

Full reports: `KDP/validation/shallow_plan_part1.md` (74 findings),
`shallow_plan_part2_3.md` (21), `shallow_plan_part4.md` (21),
`shallow_plan_part5_6.md` (36), `shallow_plan_part7_8.md` (29),
`shallow_plan_part9_10_11.md` (87).

---

## 1. Most-cited dominant finding: **bare "Section X.Y" placeholders**

**Pattern**: prose where a concept name should appear but a literal "Section
X.Y" cross-reference label was left behind by a previous auto-linker pass.
Examples:

> "Temperature scales the logits before **Section 4.1**." → should be "the softmax operation"
> "the standard is **Section 4.1** Loss" → "Cross-Entropy Loss"
> "Pluralistic alignment extends the **Section 16.1** to represent diverse value systems" → "preference modeling"
> "Strategy without execution is a **Section 29.2**" → "hallucination"

**Cross-cuts EVERY PART** (50+ instances in Part I alone, 9 each in Parts IX-X-XI).
**Fixed in v6.41 and v6.45**: 263 substitutions applied; 0 remain.

## 2. Second dominant finding: **HTML pre-block indentation rendering bug**

**Pattern**: Python code blocks where each new `def`/`class` after the first
appears indented one level deeper than it should. Methods become unreachable
closures rather than class members. Example:

```python
class TriageRouter:
    def __init__(self, ...):
        self.x = ...
        def fit(self, ...):       # WRONG: should be indent 4, sibling of __init__
            ...
            def predict(self, ...):   # WRONG
                ...
```

**Found in 263 of 1039 Python code blocks book-wide.**
**Fixed in v6.44**: 299 dedents applied with ast.parse-validation on each;
70 detections preserved (legitimate inner functions: PyTorch hooks, decorators,
factory closures).

---

## 3. Top by chapter — what's actually shallow

### Part I — Foundations (74 findings)

**Highest impact:**
- **§0.1** — Cross-entropy formula contains `y_i` but the variable is never defined. Reader cannot tell that it's a one-hot label that collapses the sum.
- **§0.4** — PPO `L^CLIP` formula entirely absent. The prose describes the ratio clipping but never shows the equation that practitioners need to implement.
- **§0.4** — KL penalty in RLHF described in one sentence; the formula `r = r_RM(x,y) - β·KL[π_θ || π_SFT]` and how β is tuned never appears.
- **§3.3** (multi-head attention) — Lacks a tensor-shape trace through Q/K/V split → attention → concat. Readers can't follow `(B, T, d) → (B, h, T, d_k) → ...`.
- **§4.1** — Information theory (perplexity, KL divergence, cross-entropy) referred via "see Appendix A.6" without inline primer. Perplexity is used throughout the book; needs at least a one-sentence inline definition.

**Lower-impact but worth noting:**
- §1.3 — Word2Vec analogies presented as-it-just-works without WEAT bias warning.
- §2.2 — WordPiece scoring formula (`freq(AB)/freq(A)freq(B)`) absent; only prose description.
- §3.1 — GRU update gate's *simplification* over LSTM (forget+input merged into one z_t) needs a one-paragraph intuition.
- §5.1 — "Beam search curse" (quality degrades with very wide beams in open-ended generation) mentioned but mechanism not explained.
- §5.2 — Repetition penalty failure mode at extreme values (function words like "the" suppressed → telegraphic prose) absent.

### Part II + III — Understanding LLMs + Working with LLMs (21 findings)

**Mostly solid.** Modules 6, 8, 9 are publication-ready: math + worked code + warnings throughout. Real issues:

- **§7.3** — Three PRM (Process Reward Model) training strategies (human annotation, Monte Carlo, automated verification) named in 1-2 sentences each. No worked numeric trace of Monte Carlo step labeling (rollout 8 trajectories → step gets correctness = k/8).
- **§11.4** — "Sandwich defense" introduces the concept but the code block shown is actually LLMLingua compression. Add a real sandwich-prompt template example.
- Multiple sections have **HTML pre-block indentation artifact** (sections 9.7, 10.2, 10.3, 12.3) — fixed in v6.44.

### Part IV — Training & Adapting (21 findings)

**Modules 15 and 16 are exemplary.** LoRA (§15.1), distillation (§15.5), merging (§15.6), RLHF (§16.1), DPO (§16.2), Constitutional AI (§16.3) all pass the four-question test.

**Real gaps:**
- **§13.2** — Code Fragment 13.2.3 titled "Implement Evol-Instruct" actually implements persona-driven generation. Caption/content mismatch.
- **§14.2** — "Phi on 6B textbook-quality tokens matches 1T tokens" stated without mechanism or Gunasekar et al. citation.
- **§14.7** — YaRN named as "recommended default beyond 4× training length" but no formula, no code, no temperature-correction explanation. Linear and NTK get full treatment; YaRN doesn't.
- **§15.2** — IA3 method described but the actual operation `Attention(Q, K⊙l_k, V⊙l_v)` is never stated.
- **§16.1** — Bradley-Terry loss for reward model training never written down. The `RewardTrainer` code is shown without the loss it optimizes.
- **§16.2** — ORPO and SimPO mentioned as DPO variants in 2-3 sentences each with no formula and no code. DPO gets full derivation; its variants do not.

### Part V + VI — Retrieval + Agents (36 findings)

**Part VI Agentic AI is the strongest content in the book.** Sections 23.x, 24.x, 25.x, 26.x are publication-ready.

**Real Part V gaps:**
- **§17.1** — InfoNCE loss formula present but the magnet metaphor in the figure isn't connected back to the formula in prose. Plus no numeric trace.
- **§17.2** — HNSW failure modes never discussed: (1) ghost vectors after deletion, (2) ef_search < k → recall collapse, (3) high-dim degradation above ~1,200 dims.
- **§17.2** — ScaNN gets one paragraph and no code while HNSW/IVF/PQ get full treatment.
- **§17.3** — Reciprocal Rank Fusion formula present but `k=60` constant rationale missing.
- **§18.2** — Step-Back Prompting (advanced RAG): one paragraph, no code (HyDE and multi-query both have implementations).
- **§18.7** — GraphRAG references Leiden community detection algorithm with no explanation of what community detection means or why Leiden over Louvain.
- **§19.3** — MemGPT/Letta architecture is promised in the Big Picture callout but the body cuts off before covering it. The most important "long-term memory for agents" technique is absent.
- **§19.5** — Voice agents: 5 platforms listed (OpenAI Realtime, LiveKit, Pipecat, Vapi, Bland.ai) in one shopping-list paragraph. No architectural differentiation.
- **§21.5** — Self-RAG mentioned as a technique but the actual reflection-token mechanism ([Retrieve], [ISREL], [ISSUP], [ISUSE]) never explained.

### Part VII + VIII — Multimodal + Production (29 findings)

**Section 27.x (Evaluation) is excellent.** Strong on rigor, statistical methods, contamination, observability.

**Real gaps:**
- **§25.2** — Video models (Sora, Runway, Kling, Veo, CogVideoX, Wan) listed in 70 words with no explanation of how they differ (architecture? temporal coherence approach?).
- **§25.2** — 3D generation introduced without first explaining what 2D approaches fail at (the *why* before the *how*).
- **§25.5** — Sim-to-real gap (the entire reason robotic simulation exists) never named or explained when introducing Habitat 3.0 / EmbodiedBench.
- **§25.7** — Janus problem (3D objects growing faces on multiple sides) mentioned in one clause; needs a dedicated callout since it's the most important failure mode of Score Distillation Sampling.
- **§26.2** — Financial LLM table (FinBERT, BloombergGPT, FinGPT, FinMA) lists names without explaining what makes financial text fundamentally different from web text.
- **§26.3** — Same shopping-list pattern for medical LLMs (Med-PaLM 2, PMC-LLaMA, BioMistral, Meditron) without the unique-failure-mode context (hallucinated drug dosages harm patients).
- **§28.3** — Semantic caching layer mentioned but its key failure mode (semantically similar but answer-divergent queries like "Apple stock today" vs "Apple stock yesterday") absent.
- **§28.8** — Error amplification through chained agents shown with `0.95^3 = 0.857` but the *correlated* failure mode (provider-wide degradation hits all agents simultaneously) absent.

**Code-output mismatches (6 instances)**: code blocks in Part VII/VIII whose output line shows results from a completely different code example. Affects sections 26.4, 26.5, 26.6, 27.10, 27.12, 28.3, 28.5, 28.9. Production-critical — readers tracing code-to-output get confused.

### Part IX + X + XI — Safety + Frontiers + Idea-to-Product (87 findings)

**Strongest sections in the book**: §29.2 (hallucination taxonomy), §29.8 (red teaming), §31.2 (mechanistic interpretability with sparse autoencoders), §32.5 (System 1/System 2 with formal complexity-theoretic separation), §33.1 (Two Teams scenario), §34.3 (cognitive vs vendor lock-in).

**Real gaps:**
- **§29.1** — OWASP Top 10 LLM threats table: 10 entries, only 3 have worked attack scenarios. The other 7 are descriptions without mechanism.
- **§29.4** — GDPR Article 17 (right-to-erasure) said to "require deletion capability" with no acknowledgment that this is *technically impossible* for LLMs trained on the data (you can't delete from neural network weights without retraining).
- **§29.5** — Governance frameworks (SR 11-7, NIST AI RMF, ISO 42001, EU AI Act) listed with one-sentence "Key Contribution" each. No when-to-choose-which guidance.
- **§29.6** — Differential Privacy ε and δ parameters introduced in code without explaining what values mean. ε=1.0 vs ε=10 — readers can't calibrate.
- **§29.7** — Gradient ascent for machine unlearning shown without its critical failure mode (catastrophic forgetting on retain set requires dual-constraint optimization).
- **§29.9** — EU AI Act risk tiers (Prohibited / High-Risk / Limited / Minimal) each get 1-3 paragraphs but no worked example of classifying a real use case (e.g. "hiring screening LLM").
- **§30.7** — Cascade routing claim of "60-80% cost reduction" stated without derivation. The arithmetic (70% simple queries to cheap model + 30% to frontier) should be shown.
- **§33.3** — Risk-feasibility matrix doesn't acknowledge the most dangerous misclassification: "low-risk-looking but high-consequence with delayed detection" (e.g. email summarizer in legal context).
- **§34.4** — A/B testing for AI features misses the **novelty effect** failure mode (week-1 enthusiasm reverses by week-4).

**Wrong-prefix sub-headings (~9 cases)** in Parts IX-XI: e.g. `<h3>32.9.1.1</h3>` inside section-29.9.html. Fixed in v6.43 (389 prefix corrections book-wide).

**4 missing figure images** in sections 33.4-33.7 (now 30.4-30.7) — captions present but no `<img>` tag. Fixed in v6.43 (empty figures stripped).

---

## What's been fixed (v6.41 — v6.44)

| Issue class | Found | Fixed | Method |
|---|---|---|---|
| Bare "Section X.Y" placeholders | 263 | ✅ 263 | Per-file + bulk context-aware lookup |
| ToC label/href mismatch | 157 | ✅ 157 | Regenerated dense-sections from disk truth |
| H3/H4 sub-heading prefix | 389 | ✅ 389 | Regex normalize prefix to section file |
| Figure label/section mismatch | 4 | ✅ 3 (1 was false-positive cross-ref) | Manual relabel |
| Empty `<figure>` with caption | 7 | ✅ 7 | Stripped |
| Python over-indentation | 263 | ✅ 299 (cascading) | ast.parse-validated dedent |
| Dead bibliography URLs | 40 | ✅ ~25 (HTTP 404s replaced) | Wayback + alternate URLs |

## What remains (deferred to v7.x content audit)

| Issue | Effort | Tracked in |
|---|---|---|
| Add missing concept formulas (PPO L^CLIP, KL penalty, Bradley-Terry, IA3, ORPO, SimPO, RRF) | ~8 hrs | this doc, see Part IV |
| Add missing failure modes (HNSW edge cases, semantic cache drift, novelty effect, etc.) | ~10 hrs | Parts V-X |
| Deepen shopping-list sections (frameworks/models tables with no selection guidance) | ~12 hrs | Parts I, IV, V, VII, IX |
| Add missing concepts that are referenced but undefined (MemGPT, ScaNN, Self-RAG tokens, Leiden, sim-to-real gap, Janus problem) | ~6 hrs | Parts V-VII |
| Fix code-output mismatches in Parts VII-VIII (6 instances) | ~2 hrs | Part VII-VIII |
| Reconcile Phi-1 "6B = 1T tokens" claim with sources | ~1 hr | §14.2 |
| Complete shallow-content fixes per per-part plan files | ~30 hrs total | All 6 plan files |

**Recommendation**: tackle Part IV first (lowest-effort, highest-impact additions of missing formulas), then Part V (the deferred concepts: MemGPT, Self-RAG, Leiden, ScaNN). Both are areas where one focused session per section can close the depth gap.
