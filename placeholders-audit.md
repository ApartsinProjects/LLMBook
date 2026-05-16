# LLMBook Placeholder Audit

**Summary: P0: 1, P1: 36, P2: 18**

Scanned 476 HTML files under `E:/Projects/BookBlogsHome/LLMBook/`. Skipped: KDP, .claude, build, node_modules, temp_*, source_fix_backups, vendor, pagefind.

---

## P0: Broken-looking

## Empty callouts (title but no body) (0)

_None found._

## Placeholder h1 (Jinja-style or punctuation-only) (0)

_None found._

## References to dropped appendices (production-patterns / hardware-compute) (1)

_Recommendation: Remove or redirect to the surviving appendix; these targets no longer exist._

- `appendices/index.html:117` -- appendix-i-hardware-compute

---

## P1: Missing content

## TODO author this section markers (28)

_Recommendation: Write the section or drop it from the TOC._

- `part-10-idea-to-product/module-40-ideation/index.html:29` -- TODO author this big-picture callout: why this chapter matters and how it connects to the broade
- `part-10-idea-to-product/module-40-ideation/index.html:37` -- TODO author this. Outline where this chapter sits in the narrative arc and what the next chapter
- `part-10-idea-to-product/module-41-product-management/index.html:29` -- TODO author this big-picture callout: why this chapter matters and how it connects to the broade
- `part-10-idea-to-product/module-41-product-management/index.html:37` -- TODO author this. Outline where this chapter sits in the narrative arc and what the next chapter
- `part-10-idea-to-product/module-42-strategy-prioritization/index.html:29` -- TODO author this big-picture callout: why this chapter matters and how it connects to the broade
- `part-10-idea-to-product/module-42-strategy-prioritization/index.html:38` -- TODO author this. Outline where this chapter sits in the narrative arc and what the next chapter
- `part-10-idea-to-product/module-43-vibe-coding/index.html:29` -- TODO author this big-picture callout: why this chapter matters and how it connects to the broade
- `part-10-idea-to-product/module-43-vibe-coding/index.html:37` -- TODO author this. Outline where this chapter sits in the narrative arc and what the next chapter
- `part-10-idea-to-product/module-44-mvp/index.html:29` -- TODO author this big-picture callout: why this chapter matters and how it connects to the broade
- `part-10-idea-to-product/module-44-mvp/index.html:37` -- TODO author this. Outline where this chapter sits in the narrative arc and what the next chapter
- `part-10-idea-to-product/module-46-compute-planning/index.html:29` -- TODO author this big-picture callout: why this chapter matters and how it connects to the broade
- `part-10-idea-to-product/module-46-compute-planning/index.html:38` -- TODO author this. Outline where this chapter sits in the narrative arc and what the next chapter
- `part-10-idea-to-product/module-46-compute-planning/section-46.2.html:28` -- TODO author this section. This is a scaffold; replace with chapter content authored in Phase E.
- `part-10-idea-to-product/module-47-scaling-economics/index.html:29` -- TODO author this big-picture callout: why this chapter matters and how it connects to the broade
- `part-10-idea-to-product/module-47-scaling-economics/index.html:38` -- TODO author this. Outline where this chapter sits in the narrative arc and what the next chapter
- `part-10-idea-to-product/module-47-scaling-economics/section-47.1.html:28` -- TODO author this section. This is a scaffold; replace with chapter content authored in Phase E.
- `part-10-idea-to-product/module-47-scaling-economics/section-47.2.html:28` -- TODO author this section. This is a scaffold; replace with chapter content authored in Phase E.
- `part-10-idea-to-product/module-49-post-launch-monitoring/index.html:29` -- TODO author this big-picture callout: why this chapter matters and how it connects to the broade
- `part-10-idea-to-product/module-49-post-launch-monitoring/index.html:37` -- TODO author this. Outline where this chapter sits in the narrative arc and what the next chapter
- `part-12-frontiers/module-64-agi-trajectories/section-64.5.html:28` -- TODO author this section. This is a scaffold; replace with chapter content authored in Phase E.
- `part-3-working-with-llms/module-16-tools-of-the-trade/index.html:29` -- TODO author this big-picture callout: why this chapter matters and how it connects to the broade
- `part-3-working-with-llms/module-16-tools-of-the-trade/index.html:41` -- TODO author this. Outline where this chapter sits in the narrative arc and what the next chapter
- `part-3-working-with-llms/module-16-tools-of-the-trade/section-16.1.html:28` -- TODO author this section. This is a scaffold; replace with chapter content authored in Phase E.
- `part-7-multimodal-generation/module-32-embodied-world-models/section-32.1.html:28` -- TODO author this section. This is a scaffold; replace with chapter content authored in Phase E.
- `part-7-multimodal-generation/module-32-embodied-world-models/section-32.2.html:28` -- TODO author this section. This is a scaffold; replace with chapter content authored in Phase E.
- `part-7-multimodal-generation/module-32-embodied-world-models/section-32.3.html:28` -- TODO author this section. This is a scaffold; replace with chapter content authored in Phase E.
- `part-7-multimodal-generation/module-32-embodied-world-models/section-32.4.html:28` -- TODO author this section. This is a scaffold; replace with chapter content authored in Phase E.
- `part-7-multimodal-generation/module-32-embodied-world-models/section-32.8.html:28` -- TODO author this section. This is a scaffold; replace with chapter content authored in Phase E.

## Stub-shape chapter index.html files (< 1500 bytes) (2)

_Recommendation: Author the chapter intro/big-picture/section-cards._

- `appendices/appendix-g-agent-frameworks/index.html:1` -- size=1084B (stub-shape)
- `part-12-frontiers/module-62-frontier-theory/index.html:1` -- size=1444B (stub-shape)

## Empty section files (< 2000 bytes) (0)

_None found._

## <p class='figure-replaced'> placeholders (6)

_Recommendation: Replace with actual figure (image, diagram, or remove caption)._

- `part-10-idea-to-product/module-41-product-management/section-41.2.html:449` -- <p class="figure-replaced"><em>The LLM product iteration cycle runs in 1-2 week loops. Each loop has four stages: <strong>(1) evaluate</strong> the current build against a fresh quality eval set; <str
- `part-9-safety-security-ethics/module-37-safety-ethics-regulation/section-37.2.html:227` -- <p class="figure-replaced"><em>A production hallucination pipeline routes LLM output through detection checks (consistency, citation, NLI) and selects a response strategy: emit grounded answer, abstai
- `part-9-safety-security-ethics/module-37-safety-ethics-regulation/section-37.3.html:270` -- <p class="figure-replaced"><em>Three complementary documentation standards cover progressively broader scope: a <strong>model card</strong> documents the model itself (intended use, performance, known
- `part-9-safety-security-ethics/module-37-safety-ethics-regulation/section-37.4.html:347` -- <p class="figure-replaced"><em>Regulatory approaches vary by jurisdiction: the EU enforces binding obligations via the AI Act (with conformity assessments for high-risk systems); the US currently reli
- `part-9-safety-security-ethics/module-37-safety-ethics-regulation/section-37.5.html:303` -- <p class="figure-replaced"><em><strong>SR 11-7's three lines of defense</strong> separate concerns to prevent any single team from grading its own work. The <strong>first line</strong> (model owners a
- `part-9-safety-security-ethics/module-37-safety-ethics-regulation/section-37.6.html:173` -- <p class="figure-replaced"><em><strong>Differentially-private SGD (DP-SGD)</strong> protects training-data privacy through two coordinated mechanisms: (1) per-example gradient clipping bounds any sing

---

## P2: Drift

## Mismatched caption chapter prefixes (post-renumber drift) (11)

_Recommendation: Rewrite caption numbers to match the current chapter index._

- `part-10-idea-to-product/module-45-prototype-to-production/section-45.3.html:90` -- caption 'Table 33.3.1' but parent is module-45: Table 33.3.1: Error Tolerance by Domain
- `part-12-frontiers/module-61-frontier-architectures/section-33.4.html:55` -- caption 'Figure 33.4.1' but parent is module-61: Figure 33.4.1 : World models as internal simulations: the AI builds a miniature model of reality, predicts what will hap
- `part-12-frontiers/module-61-frontier-architectures/section-33.4.html:68` -- caption 'Figure 33.4.2' but parent is module-61: Figure 33.4.2 : A world-model agent in the Ha-Schmidhuber lineage. An encoder compresses observations into latents; a dy
- `part-12-frontiers/module-61-frontier-architectures/section-33.4.html:264` -- caption 'Table 33.4.1' but parent is module-61: Table 33.4.1: Comparison of major autonomous driving world models. Parameter counts are approximate and reflect the worl
- `part-12-frontiers/module-61-frontier-architectures/section-33.4.html:638` -- caption 'Code Fragment 33.4.1' but parent is module-61: Code Fragment 33.4.1: world_model_lab.py
- `part-12-frontiers/module-61-frontier-architectures/section-33.4.html:722` -- caption 'Code Fragment 33.4.2' but parent is module-61: Code Fragment 33.4.2: Training loop (simplified)
- `part-2-understanding-llms/module-07-pretraining-scaling-laws/section-7.1.html:103` -- caption 'Listing 6.1' but parent is module-7: Listing 6.1. BERT fill-mask in two lines using HuggingFace's pipeline API. The encoder produces a probability distributi
- `part-8-evaluation-production/module-35-production-engineering/section-35.9.html:645` -- caption 'Code Fragment 34.9' but parent is module-35: Code Fragment 34.9.L2: Launch vLLM serving TinyLlama. For larger models, add --tensor-parallel-size N to shard across mu
- `part-9-safety-security-ethics/module-37-safety-ethics-regulation/section-37.1.html:420` -- caption 'Table 35.1.3' but parent is module-37: Table 35.1.3 : Comparison of watermarking and provenance methods across modalities, showing the tradeoff between robustn
- `part-9-safety-security-ethics/module-37-safety-ethics-regulation/section-37.1.html:600` -- caption 'Table 35.1.4' but parent is module-37: Table 35.1.4 : SLSA framework levels mapped from software build artifacts to ML model artifacts, showing how each level 
- `part-9-safety-security-ethics/module-37-safety-ethics-regulation/section-37.1.html:677` -- caption 'Table 35.1.2' but parent is module-37: Table 35.1.2 : Comparison of LLM attack types by threat model, attacker skill requirements, and recommended defensive st

## TODO(audit) HTML comments (7)

_Recommendation: Resolve the audit note and remove the comment._

- `part-10-idea-to-product/module-41-product-management/section-41.2.html:445` -- <!-- TODO(audit): broken figure ref "Figure 41.2.4": target figure does not exist; either author the diagram or remove t
- `part-11-applications-across-industries/module-52-finance-llms/section-52.7.html:421` -- <!-- TODO(audit): broken figure ref "Figure 52.2.2": target figure does not exist; either author the diagram or remove t
- `part-9-safety-security-ethics/module-37-safety-ethics-regulation/section-37.2.html:225` -- <!-- TODO(audit): broken figure ref "Figure 37.2.3": target figure does not exist; either author the diagram or remove t
- `part-9-safety-security-ethics/module-37-safety-ethics-regulation/section-37.3.html:269` -- <!-- TODO(audit): broken figure ref "Figure 37.3.3": target figure does not exist; either author the diagram or remove t
- `part-9-safety-security-ethics/module-37-safety-ethics-regulation/section-37.4.html:346` -- <!-- TODO(audit): broken figure ref "Figure 37.4.3": target figure does not exist; either author the diagram or remove t
- `part-9-safety-security-ethics/module-37-safety-ethics-regulation/section-37.5.html:302` -- <!-- TODO(audit): broken figure ref "Figure 37.5.2": target figure does not exist; either author the diagram or remove t
- `part-9-safety-security-ethics/module-37-safety-ethics-regulation/section-37.6.html:172` -- <!-- TODO(audit): broken figure ref "Figure 37.6.2": target figure does not exist; either author the diagram or remove t

---

## Follow-up TODO list (for authoring agent)

Organized by priority. Each item is self-contained; an agent can pick one and run it.

### Stale appendix references (P0)

- [ ] **1.** Remove/redirect dropped-appendix link(s) in `appendices/index.html` (lines 117).

### TODO author markers (P1)

- [ ] **2.** Author the section(s) marked 'TODO author this section' in `part-10-idea-to-product/module-40-ideation/index.html` (2 marker(s)).
- [ ] **3.** Author the section(s) marked 'TODO author this section' in `part-10-idea-to-product/module-41-product-management/index.html` (2 marker(s)).
- [ ] **4.** Author the section(s) marked 'TODO author this section' in `part-10-idea-to-product/module-42-strategy-prioritization/index.html` (2 marker(s)).
- [ ] **5.** Author the section(s) marked 'TODO author this section' in `part-10-idea-to-product/module-43-vibe-coding/index.html` (2 marker(s)).
- [ ] **6.** Author the section(s) marked 'TODO author this section' in `part-10-idea-to-product/module-44-mvp/index.html` (2 marker(s)).
- [ ] **7.** Author the section(s) marked 'TODO author this section' in `part-10-idea-to-product/module-46-compute-planning/index.html` (2 marker(s)).
- [ ] **8.** Author the section(s) marked 'TODO author this section' in `part-10-idea-to-product/module-46-compute-planning/section-46.2.html` (1 marker(s)).
- [ ] **9.** Author the section(s) marked 'TODO author this section' in `part-10-idea-to-product/module-47-scaling-economics/index.html` (2 marker(s)).
- [ ] **10.** Author the section(s) marked 'TODO author this section' in `part-10-idea-to-product/module-47-scaling-economics/section-47.1.html` (1 marker(s)).
- [ ] **11.** Author the section(s) marked 'TODO author this section' in `part-10-idea-to-product/module-47-scaling-economics/section-47.2.html` (1 marker(s)).
- [ ] **12.** Author the section(s) marked 'TODO author this section' in `part-10-idea-to-product/module-49-post-launch-monitoring/index.html` (2 marker(s)).
- [ ] **13.** Author the section(s) marked 'TODO author this section' in `part-12-frontiers/module-64-agi-trajectories/section-64.5.html` (1 marker(s)).
- [ ] **14.** Author the section(s) marked 'TODO author this section' in `part-3-working-with-llms/module-16-tools-of-the-trade/index.html` (2 marker(s)).
- [ ] **15.** Author the section(s) marked 'TODO author this section' in `part-3-working-with-llms/module-16-tools-of-the-trade/section-16.1.html` (1 marker(s)).
- [ ] **16.** Author the section(s) marked 'TODO author this section' in `part-7-multimodal-generation/module-32-embodied-world-models/section-32.1.html` (1 marker(s)).
- [ ] **17.** Author the section(s) marked 'TODO author this section' in `part-7-multimodal-generation/module-32-embodied-world-models/section-32.2.html` (1 marker(s)).
- [ ] **18.** Author the section(s) marked 'TODO author this section' in `part-7-multimodal-generation/module-32-embodied-world-models/section-32.3.html` (1 marker(s)).
- [ ] **19.** Author the section(s) marked 'TODO author this section' in `part-7-multimodal-generation/module-32-embodied-world-models/section-32.4.html` (1 marker(s)).
- [ ] **20.** Author the section(s) marked 'TODO author this section' in `part-7-multimodal-generation/module-32-embodied-world-models/section-32.8.html` (1 marker(s)).

### Stub chapter index.html (P1)

- [ ] **21.** Author the chapter intro/big-picture/section-cards for `appendices/appendix-g-agent-frameworks/index.html` (size=1084B (stub-shape)).
- [ ] **22.** Author the chapter intro/big-picture/section-cards for `part-12-frontiers/module-62-frontier-theory/index.html` (size=1444B (stub-shape)).

### Replaced figure placeholders (P1)

- [ ] **23.** Replace `<p class="figure-replaced">` placeholder(s) in `part-10-idea-to-product/module-41-product-management/section-41.2.html` with actual figure (1 site(s)).
- [ ] **24.** Replace `<p class="figure-replaced">` placeholder(s) in `part-9-safety-security-ethics/module-37-safety-ethics-regulation/section-37.2.html` with actual figure (1 site(s)).
- [ ] **25.** Replace `<p class="figure-replaced">` placeholder(s) in `part-9-safety-security-ethics/module-37-safety-ethics-regulation/section-37.3.html` with actual figure (1 site(s)).
- [ ] **26.** Replace `<p class="figure-replaced">` placeholder(s) in `part-9-safety-security-ethics/module-37-safety-ethics-regulation/section-37.4.html` with actual figure (1 site(s)).
- [ ] **27.** Replace `<p class="figure-replaced">` placeholder(s) in `part-9-safety-security-ethics/module-37-safety-ethics-regulation/section-37.5.html` with actual figure (1 site(s)).
- [ ] **28.** Replace `<p class="figure-replaced">` placeholder(s) in `part-9-safety-security-ethics/module-37-safety-ethics-regulation/section-37.6.html` with actual figure (1 site(s)).

