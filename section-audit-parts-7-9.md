# Per-Section Audit - Parts 7-9

_Scope: every `section-N.M.html` and `index.html` under `part-7-multimodal-generation/`, `part-8-evaluation-production/`, `part-9-safety-security-ethics/` (modules 31-39)._

## Summary

- Files audited: 73 (64 section files + 9 index files)
- P0 (uniform format: missing scaffold assets / inline styles / TODO markers): 1 critical finding (KaTeX missing where math is rendered)
- P1 (broken non-external links): 21 findings across 12 files
- P2 (naming drift in <title>/<h1>/breadcrumb/page-current and stale chapter prefixes in h2 numbering): 41 findings across 41 files (40 stale legacy-chapter h2 prefixes + 1 stale title annotation)
- P3 (caption / figure-number issues): 1 finding (wrong-chapter figure number)
- P4 (callout palette drift / missing canonical class): 0 findings

### Repeating broken-link patterns
- `../../part-6-agentic-ai/module-38-agent-safety-security/section-25.3.html` -> 4 occurrence(s)
- `../../part-6-agentic-ai/module-38-agent-safety-security/section-25.4.html` -> 3 occurrence(s)
- `../module-26-ai-agents/section-26.2.html` (resolves inside part-9) -> 3 occurrence(s)
- `../module-27-tool-use-protocols/index.html` (resolves inside part-9) -> 3 occurrence(s)
- `../module-28-multi-agent-systems/index.html` (resolves inside part-9) -> 2 occurrence(s)
- `../module-42-strategy-prioritization/index.html` (resolves inside part-9) -> 2 occurrence(s)
- `../../part-2-understanding-llms/module-07-pretraining-scaling-laws/section-6.2.html` -> 2 occurrence(s)
- `../../part-6-agentic-ai/module-38-agent-safety-security/section-25.1.html` -> 1 occurrence(s)
- `../module-42-strategy-prioritization/section-31.1.html` (resolves inside part-9) -> 1 occurrence(s)
- `../module-29-specialized-agents/section-29.2.html` (resolves inside part-9) -> 1 occurrence(s)

Two root causes: (a) the renumber of `part-2/.../section-6.2.html` to `section-7.2.html` left two dangling refs in section-32.4; (b) the renumber that moved `module-38-agent-safety-security` from part-6 to part-9 (and renumbered its sections from `25.x` to `38.x`) left dangling refs in part-8 and part-9. Module-38's authors also write `../module-XX-...` paths assuming they still live in part-6; those now resolve inside part-9 (which has no such modules).

### Repeating naming-drift patterns (stale chapter prefixes in h2 numbering)

Section bodies were carried over from the old chapter layout but the h2 numerical prefix was never updated. Each row aggregates all sections in `Real Chapter N` whose headings start with `M.x.y`.

- **Chapter 31** headings still use **`26.x.y`** (should be `31.x.y`); 18 stale headings across 4 section(s).
  - Sections: 31.1, 31.2, 31.3, 31.4
- **Chapter 34** headings still use **`28.x.y`** (should be `34.x.y`); 68 stale headings across 12 section(s).
  - Sections: 34.1, 34.2, 34.3, 34.4, 34.5, 34.6, 34.7, 34.8, 34.9, 34.10, 34.11, 34.12
- **Chapter 35** headings still use **`29.x.y`** (should be `35.x.y`); 52 stale headings across 9 section(s).
  - Sections: 35.1, 35.2, 35.3, 35.4, 35.5, 35.6, 35.7, 35.8, 35.9
- **Chapter 37** headings still use **`30.x.y`** (should be `37.x.y`); 66 stale headings across 11 section(s). Section 37.1 also uses h3 (not h2) for numbered subsections.
  - Sections: 37.2, 37.3, 37.4, 37.5, 37.6, 37.7, 37.8, 37.9, 37.10, 37.11, 37.12
- **Chapter 38** headings still use **`25.x.y`** (should be `38.x.y`); 19 stale headings across 4 section(s). Sections 38.3 and 38.4 carry sub-numbers `25.6.x` and `25.7.x`, not `25.3.x` and `25.4.x` (suggests these were section-25.6 and section-25.7 originally).
  - Sections: 38.1, 38.2, 38.3, 38.4

Modules 32 (P7 world models), 33 (P7 tools), 36 (P8 tools), 39 (P9 tools) all use the **current** chapter prefix correctly (32.x, 33.x, 36.x, 39.x).

### Repeating naming-drift patterns (other)

- **[2x duplicate h2 number block]** Section concatenated from two sources without renumbering the second source. Sections: 37.3 (`30.3.1-30.3.4` then `30.3.1-30.3.7`), 37.11 (`30.11.1-30.11.5` then `30.11.4` again).
- **[2x skipped h2 number]** Sequence skips a sub-number. Sections: 37.2 (skips `30.2.4`), 37.9 (skips `30.9.2`).
- **[1x stale title annotation]** `<title>` retains a rename note. Section: 32.4 (`(from old 33.4)`).
- **[1x non-canonical h2 style]** Numbered subsections wrapped in `<h3>` instead of `<h2>` (likely from omnibus split). Section: 37.1.

### Repeating P0 patterns

- **[1x critical]** Display math `$$ ... $$` present but KaTeX CSS/JS bundle not loaded; equation renders as raw LaTeX. Section: 34.11.
- **[60x cosmetic]** KaTeX CSS not loaded; section has no math content. Harmless until someone adds math. Files: every section except section-31.1 and section-34.1.
- **[20x cosmetic]** Prism theme CSS not loaded; section has `<pre><code class="lang-...">` blocks that fall back to plain monospace (no syntax highlight). Files: all module-32, module-33, module-36, module-39 sections (plus their indexes).
- **[9x cosmetic]** Pygments CSS not loaded. Files: 9 indexes / minimal-content sections (the module-31/32/33/36/39 indexes plus section-37.12).

## Per-file findings

### part-7-multimodal-generation/index.html
  - P2 naming: title format intentional (index file)
### part-7-multimodal-generation/module-31-multimodal/index.html
  - P0 structure (1):
    - missing pygments.css, katex.min.css, prism-theme.css link tags
### part-7-multimodal-generation/module-31-multimodal/section-31.1.html
  - P2 naming (4):
    - h2 lineno 55: "26.1.1 Diffusion Models for Image Generation" (expected 31.1.x)
    - h2 lineno ~: "26.1.2 Controlled Image Generation" (expected 31.1.x)
    - h2 lineno ~: "26.1.3 Vision Encoders: Bridging Pixels and Language" (expected 31.1.x)
    - h2 lineno ~: "26.1.4 Vision-Language Models" (expected 31.1.x)
### part-7-multimodal-generation/module-31-multimodal/section-31.2.html
  - P0 structure (1):
    - missing katex.min.css link tag (section has no math content)
  - P2 naming (4):
    - h2: "26.2.1 Text-to-Speech (TTS) Systems" (expected 31.2.x)
    - h2: "26.2.2 Music Generation" (expected 31.2.x)
    - h2: "26.2.3 Text-to-Video Generation" (expected 31.2.x)
    - h2: "26.2.4 3D Generation" (expected 31.2.x)
### part-7-multimodal-generation/module-31-multimodal/section-31.3.html
  - P0 structure (1):
    - missing katex.min.css link tag (section has no math content)
  - P2 naming (4):
    - h2: "26.3.1 Modern OCR with TrOCR" through "26.3.4 Comparing Document Understanding Approaches" (expected 31.3.x)
### part-7-multimodal-generation/module-31-multimodal/section-31.4.html
  - P0 structure (1):
    - missing katex.min.css link tag (section has no math content)
  - P2 naming (6):
    - h2: "26.4.1 Pipeline vs. Native Multimodal Architectures" through "26.4.5 Multimodal Benchmarks" plus 26.4.6 (expected 31.4.x)
### part-7-multimodal-generation/module-32-embodied-world-models/index.html
  - P0 structure (1):
    - missing pygments.css, katex.min.css, prism-theme.css link tags
### part-7-multimodal-generation/module-32-embodied-world-models/section-32.1.html
  - P0 structure (1):
    - missing katex.min.css, prism-theme.css (section has `<pre><code class="lang-python">` blocks that won't syntax-highlight)
### part-7-multimodal-generation/module-32-embodied-world-models/section-32.2.html
  - P0 structure (1):
    - missing katex.min.css, prism-theme.css (same as 32.1)
### part-7-multimodal-generation/module-32-embodied-world-models/section-32.3.html
  - P0 structure (1):
    - missing katex.min.css, prism-theme.css (same as 32.1)
### part-7-multimodal-generation/module-32-embodied-world-models/section-32.4.html
  - P0 structure (1):
    - missing katex.min.css, prism-theme.css (same as 32.1)
  - P1 links (2):
    - line 35: broken href '../../part-2-understanding-llms/module-07-pretraining-scaling-laws/section-6.2.html' (target renamed to section-7.2.html)
    - line ~: same broken href, second occurrence
  - P2 naming (1):
    - <title> 'Section 32.4: World Models for Video Understanding (from old 33.4)' contains stale rename annotation; h1 is 'World Models: Video Generation, Simulation, and Embodied Reasoning'
### part-7-multimodal-generation/module-32-embodied-world-models/section-32.5.html
  - P0 structure (1):
    - missing katex.min.css, prism-theme.css
### part-7-multimodal-generation/module-32-embodied-world-models/section-32.6.html
  - P0 structure (1):
    - missing katex.min.css, prism-theme.css
### part-7-multimodal-generation/module-32-embodied-world-models/section-32.7.html
  - P0 structure (1):
    - missing katex.min.css, prism-theme.css
### part-7-multimodal-generation/module-32-embodied-world-models/section-32.8.html
  - P0 structure (1):
    - missing katex.min.css, prism-theme.css
### part-7-multimodal-generation/module-33-tools-of-the-trade/index.html
  - P0 structure (1):
    - missing pygments.css, katex.min.css, prism-theme.css link tags
### part-7-multimodal-generation/module-33-tools-of-the-trade/section-33.1.html
  - P0 structure (1):
    - missing katex.min.css, prism-theme.css (section has prism-style code blocks)
### part-7-multimodal-generation/module-33-tools-of-the-trade/section-33.2.html
  - P0 structure (1):
    - missing katex.min.css, prism-theme.css
### part-7-multimodal-generation/module-33-tools-of-the-trade/section-33.3.html
  - P0 structure (1):
    - missing katex.min.css, prism-theme.css
### part-7-multimodal-generation/module-33-tools-of-the-trade/section-33.4.html
  - P0 structure (1):
    - missing katex.min.css, prism-theme.css
### part-7-multimodal-generation/module-33-tools-of-the-trade/section-33.5.html
  - P0 structure (1):
    - missing katex.min.css, prism-theme.css

### part-8-evaluation-production/index.html
  - clean
### part-8-evaluation-production/module-34-evaluation-observability/index.html
  - P0 structure (1):
    - missing pygments.css, katex.min.css, prism-theme.css link tags
### part-8-evaluation-production/module-34-evaluation-observability/section-34.1.html
  - P2 naming (6):
    - h2 "28.1.1 Intrinsic Language Modeling Metrics" through "28.1.5 Standard Benchmarks" plus 28.1.6 (expected 34.1.x)
### part-8-evaluation-production/module-34-evaluation-observability/section-34.2.html
  - P0 structure (1):
    - missing katex.min.css (no math content)
  - P2 naming (7):
    - h2 "28.2.1 Why Statistical Rigor Matters for LLM Evaluation" through "28.2.7" (expected 34.2.x)
### part-8-evaluation-production/module-34-evaluation-observability/section-34.3.html
  - P0 structure (1):
    - missing katex.min.css (no math content)
  - P2 naming (6):
    - h2 "28.3.1 The LLM Testing Pyramid" through "28.3.6" (expected 34.3.x)
### part-8-evaluation-production/module-34-evaluation-observability/section-34.4.html
  - P0 structure (1):
    - missing pygments.css link tag
  - P2 naming (1):
    - h2 "28.4.5 Retraining and Intervention Triggers" (expected 34.4.x; rest of h2s appear renumbered, only the last one is stale)
### part-8-evaluation-production/module-34-evaluation-observability/section-34.5.html
  - P0 structure (1):
    - missing katex.min.css (no math content)
  - P2 naming (5):
    - h2 "28.5.1 Why Quality Gates Matter for LLM Systems" through "28.5.5" (expected 34.5.x)
### part-8-evaluation-production/module-34-evaluation-observability/section-34.6.html
  - P0 structure (1):
    - missing katex.min.css (no math content)
  - P2 naming (6):
    - h2 "28.6.1 LLM Tracing Concepts" through "28.6.6" (expected 34.6.x)
### part-8-evaluation-production/module-34-evaluation-observability/section-34.7.html
  - P2 naming (5):
    - h2 "28.7.1 Why LLM Reproducibility Is Hard" through "28.7.5 Containerized Reproducibility with Docker" (expected 34.7.x)
### part-8-evaluation-production/module-34-evaluation-observability/section-34.8.html
  - P2 naming (7):
    - h2 "28.8.1 Judge Bias Taxonomy" through "28.8.7" (expected 34.8.x)
### part-8-evaluation-production/module-34-evaluation-observability/section-34.9.html
  - P2 naming (6):
    - h2 "28.9.1 The Gap Between Claimed and Effective Context Length" through "28.9.6" (expected 34.9.x)
### part-8-evaluation-production/module-34-evaluation-observability/section-34.10.html
  - P0 structure (1):
    - missing katex.min.css (no math content)
  - P1 links (2):
    - line ~: broken href '../../part-6-agentic-ai/module-38-agent-safety-security/section-25.3.html' (module relocated to part-9; section renumbered)
    - line ~: same broken href, second occurrence
  - P2 naming (6):
    - h2 "28.10.1 Why OpenTelemetry for LLM Systems" through "28.10.6" (expected 34.10.x)
### part-8-evaluation-production/module-34-evaluation-observability/section-34.11.html
  - P0 structure (1):
    - **CRITICAL**: section contains display math `$$ n \geq \frac{(z_{\alpha/2} + z_\beta)^2 \cdot 2p(1-p)}{\delta^2} $$` (line 55) but NO katex.min.css / katex.min.js / auto-render.min.js loaded; math renders as raw LaTeX
  - P2 naming (8):
    - h2 "28.11.1 Experiment Design for LLM Research" through "28.11.8" (expected 34.11.x)
### part-8-evaluation-production/module-34-evaluation-observability/section-34.12.html
  - P0 structure (1):
    - missing katex.min.css (no math content)
  - P2 naming (5):
    - h2 "28.12.1 MLPerf Training and Inference Suites" through "28.12.5 KV Cache as a Distributed Resource" (expected 34.12.x)
### part-8-evaluation-production/module-35-production-engineering/index.html
  - P0 structure (1):
    - missing pygments.css, katex.min.css, prism-theme.css link tags
### part-8-evaluation-production/module-35-production-engineering/section-35.1.html
  - P0 structure (1):
    - missing katex.min.css (no math content)
  - P2 naming (5):
    - h2 "29.1.1 API Layer with FastAPI" through "29.1.5 Serverless Deployment" (expected 35.1.x)
### part-8-evaluation-production/module-35-production-engineering/section-35.2.html
  - P0 structure (1):
    - missing katex.min.css (no math content)
  - P2 naming (5):
    - h2 "29.2.1 Framework Comparison" through "29.2.5 Vercel AI SDK with Next.js" (expected 35.2.x)
### part-8-evaluation-production/module-35-production-engineering/section-35.3.html
  - P0 structure (1):
    - missing katex.min.css (no math content)
  - P2 naming (4):
    - h2 "29.3.1 Latency Optimization Strategies" through "29.3.4 Production Memory Patterns" (expected 35.3.x)
### part-8-evaluation-production/module-35-production-engineering/section-35.4.html
  - P0 structure (1):
    - missing katex.min.css (no math content)
  - P2 naming (4):
    - h2 "29.4.1 Prompt Versioning" through "29.4.4 Model Registry" (expected 35.4.x)
### part-8-evaluation-production/module-35-production-engineering/section-35.5.html
  - P1 links (2):
    - line ~: broken href '../../part-6-agentic-ai/module-38-agent-safety-security/section-25.4.html' (target moved)
    - line ~: same broken href, second occurrence
  - P2 naming (6):
    - h2 "29.5.1 The Case for an AI Gateway Layer" through "29.5.6" (expected 35.5.x)
### part-8-evaluation-production/module-35-production-engineering/section-35.6.html
  - P0 structure (1):
    - missing katex.min.css (no math content)
  - P1 links (1):
    - line ~: broken href '../../part-6-agentic-ai/module-38-agent-safety-security/section-25.4.html' (target moved)
  - P2 naming (7):
    - h2 "29.6.1 Why LLM Agents Need Durable Execution" through "29.6.7" (expected 35.6.x)
### part-8-evaluation-production/module-35-production-engineering/section-35.7.html
  - P0 structure (1):
    - missing katex.min.css (no math content)
  - P2 naming (6):
    - h2 "29.7.1 Why Edge Deployment Matters" through "29.7.6" (expected 35.7.x)
### part-8-evaluation-production/module-35-production-engineering/section-35.8.html
  - P2 naming (8):
    - h2 "29.8.1 LLM Failure Taxonomy" through "29.8.8" (expected 35.8.x)
### part-8-evaluation-production/module-35-production-engineering/section-35.9.html
  - P0 structure (1):
    - missing katex.min.css (no math content)
  - P2 naming (6):
    - h2 "29.9.1 GPU Scheduling for LLM Training" through "29.9.6" (expected 35.9.x)
### part-8-evaluation-production/module-36-tools-of-the-trade/index.html
  - P0 structure (1):
    - missing pygments.css, katex.min.css, prism-theme.css link tags
### part-8-evaluation-production/module-36-tools-of-the-trade/section-36.1.html
  - P0 structure (1):
    - missing katex.min.css, prism-theme.css (section has prism-style code blocks)
### part-8-evaluation-production/module-36-tools-of-the-trade/section-36.2.html
  - P0 structure (1):
    - missing katex.min.css, prism-theme.css
### part-8-evaluation-production/module-36-tools-of-the-trade/section-36.3.html
  - P0 structure (1):
    - missing katex.min.css, prism-theme.css
### part-8-evaluation-production/module-36-tools-of-the-trade/section-36.4.html
  - P0 structure (1):
    - missing katex.min.css, prism-theme.css
### part-8-evaluation-production/module-36-tools-of-the-trade/section-36.5.html
  - P0 structure (1):
    - missing katex.min.css, prism-theme.css

### part-9-safety-security-ethics/index.html
  - clean
### part-9-safety-security-ethics/module-37-safety-ethics-regulation/index.html
  - P0 structure (1):
    - missing pygments.css, katex.min.css, prism-theme.css link tags
### part-9-safety-security-ethics/module-37-safety-ethics-regulation/section-37.1.html
  - P0 structure (1):
    - missing katex.min.css (no math content in body; large omnibus, 13,335 words)
  - P1 links (1):
    - line ~: broken href '../../part-6-agentic-ai/module-38-agent-safety-security/section-25.1.html' (target moved)
  - P2 naming (1):
    - all numbered subsections (`30.1.1 OWASP Top 10 ...` through `30.1.6 Model Extraction and Stealing`) wrapped in <h3>, not <h2>; also uses legacy prefix `30.x.y` (expected 37.1.x)
### part-9-safety-security-ethics/module-37-safety-ethics-regulation/section-37.2.html
  - P2 naming (4):
    - h2 "30.2.1 Hallucination Taxonomy" through "30.2.3 Mitigation Strategies", then "30.2.5 Privacy Risks and Memorization"; sequence skips 30.2.4 (expected 37.2.x)
### part-9-safety-security-ethics/module-37-safety-ethics-regulation/section-37.3.html
  - P2 naming (12):
    - h2 "30.3.1 Sources of Bias" through "30.3.4 Cross-Cultural NLP and Pluralistic Alignment" (block 1, lines 47-296)
    - h2 "30.3.1 Cultural Bias in LLMs" through "30.3.7 Translation of Culturally-Loaded Concepts" (block 2, lines 309-732); DUPLICATE numbering with block 1
    - all expected 37.3.x
### part-9-safety-security-ethics/module-37-safety-ethics-regulation/section-37.4.html
  - P0 structure (1):
    - missing katex.min.css (no math content)
  - P2 naming (3):
    - h2 "30.4.1 EU AI Act Risk Tiers", "30.4.2 GDPR Requirements for LLM Systems", "30.4.3 Sector-Specific Regulations" (expected 37.4.x)
### part-9-safety-security-ethics/module-37-safety-ethics-regulation/section-37.5.html
  - P0 structure (1):
    - missing katex.min.css (no math content)
  - P2 naming (2):
    - h2 "30.5.1 Governance Frameworks Comparison", "30.5.2 Model Inventory and Risk Classification" (expected 37.5.x)
### part-9-safety-security-ethics/module-37-safety-ethics-regulation/section-37.6.html
  - P0 structure (1):
    - missing katex.min.css (no math content)
  - P2 naming (2):
    - h2 "30.6.1 Model License Taxonomy", "30.6.2 Differential Privacy for LLM Training" (expected 37.6.x)
### part-9-safety-security-ethics/module-37-safety-ethics-regulation/section-37.7.html
  - P0 structure (1):
    - missing katex.min.css (no math content)
  - P2 naming (4):
    - h2 "30.7.1 Motivations for Unlearning" through "30.7.4 Evaluating Unlearning Quality" (expected 37.7.x)
### part-9-safety-security-ethics/module-37-safety-ethics-regulation/section-37.8.html
  - P0 structure (1):
    - missing katex.min.css (no math content)
  - P2 naming (7):
    - h2 "30.8.1 Why LLM Systems Need Dedicated Red Teaming" through "30.8.7" (expected 37.8.x)
### part-9-safety-security-ethics/module-37-safety-ethics-regulation/section-37.9.html
  - P0 structure (1):
    - missing katex.min.css (no math content)
  - P1 links (1):
    - line ~: broken href '../module-42-strategy-prioritization/index.html' (module-42 lives in part-10; relative path resolves inside part-9)
  - P2 naming (8):
    - h2 "30.9.1 Risk Classification for LLM Applications", then "30.9.3 General-Purpose AI Model (GPAI) Obligations" through "30.9.9"; sequence skips 30.9.2 (expected 37.9.x)
### part-9-safety-security-ethics/module-37-safety-ethics-regulation/section-37.10.html
  - P2 naming (8):
    - h2 "30.10.1 The Carbon Footprint of LLM Training" through "30.10.8" (expected 37.10.x)
### part-9-safety-security-ethics/module-37-safety-ethics-regulation/section-37.11.html
  - P1 links (1):
    - line ~: broken href '../module-42-strategy-prioritization/index.html' (module-42 lives in part-10)
  - P2 naming (12):
    - h2 "30.11.1 Training Data Extraction Attacks" through "30.11.5 Defense in Depth" (block 1, lines 53-439)
    - h2 "30.11.4 Federated Learning for Privacy-Preserving Training", then nested "30.11.1 Federated Learning Fundamentals" through "30.11.6 Challenges and Limitations" (block 2, lines 643-834); DUPLICATE numbering with block 1
    - all expected 37.11.x
### part-9-safety-security-ethics/module-37-safety-ethics-regulation/section-37.12.html
  - P0 structure (1):
    - missing pygments.css, katex.min.css, prism-theme.css link tags
  - P1 links (2):
    - line ~: broken href '../../part-6-agentic-ai/module-38-agent-safety-security/section-25.3.html' (target moved)
    - line ~: broken href '../module-42-strategy-prioritization/section-31.1.html' (module-42 lives in part-10)
  - P2 naming (5):
    - h2 "30.12.1 Compute Governance" through "30.12.5 Open Problems in AI Governance" (expected 37.12.x)
### part-9-safety-security-ethics/module-38-agent-safety-security/index.html
  - P0 structure (1):
    - missing pygments.css, katex.min.css, prism-theme.css link tags
### part-9-safety-security-ethics/module-38-agent-safety-security/section-38.1.html
  - P0 structure (1):
    - missing katex.min.css (no math content)
  - P1 links (3):
    - line 42: broken href '../module-26-ai-agents/section-26.2.html' (should be ../../part-6-agentic-ai/module-26-ai-agents/section-26.2.html)
    - line 42: broken href '../module-27-tool-use-protocols/index.html'
    - line 42: broken href '../module-28-multi-agent-systems/index.html'
  - P2 naming (2):
    - h2 "25.1.1 The Agent Threat Model", "25.1.2 Guardrails and Content Filtering" (expected 38.1.x)
### part-9-safety-security-ethics/module-38-agent-safety-security/section-38.2.html
  - P0 structure (1):
    - missing katex.min.css (no math content)
  - P1 links (4):
    - line ~: broken href '../module-26-ai-agents/section-26.2.html'
    - line ~: broken href '../module-27-tool-use-protocols/index.html'
    - line ~: broken href '../module-28-multi-agent-systems/index.html'
    - line ~: broken href '../module-29-specialized-agents/section-29.2.html'
  - P2 naming (4):
    - h2 "25.2.1 Why Sandboxing Is Non-Negotiable" through "25.2.4 Isolation Runtimes: gVisor, Firecracker, and Beyond" (expected 38.2.x)
### part-9-safety-security-ethics/module-38-agent-safety-security/section-38.3.html
  - P0 structure (1):
    - missing katex.min.css (no math content)
  - P1 links (1):
    - line ~: broken href '../module-27-tool-use-protocols/index.html'
  - P2 naming (5):
    - h2 "25.6.1 Tool-Specific Threat Models" through "25.6.5 Sandbox Limitations and Evaluation Methodology" (expected 38.3.x; legacy prefix is 25.6, not 25.3)
  - P3 captions (1):
    - figcaption line 46: "Figure 38.6.1" (expected 38.3.1; legacy figure number from old section 25.6)
### part-9-safety-security-ethics/module-38-agent-safety-security/section-38.4.html
  - P0 structure (1):
    - missing katex.min.css (no math content)
  - P1 links (1):
    - line ~: broken href '../module-26-ai-agents/section-26.2.html'
  - P2 naming (8):
    - h2 "25.7.1 Why Agent Sandboxes Need Supply-Chain Hardening" through "25.7.8" (expected 38.4.x; legacy prefix is 25.7, not 25.4)
### part-9-safety-security-ethics/module-39-tools-of-the-trade/index.html
  - P0 structure (1):
    - missing pygments.css, katex.min.css, prism-theme.css link tags
### part-9-safety-security-ethics/module-39-tools-of-the-trade/section-39.1.html
  - P0 structure (1):
    - missing katex.min.css, prism-theme.css (section has prism-style code blocks)
### part-9-safety-security-ethics/module-39-tools-of-the-trade/section-39.2.html
  - P0 structure (1):
    - missing katex.min.css, prism-theme.css
### part-9-safety-security-ethics/module-39-tools-of-the-trade/section-39.3.html
  - P0 structure (1):
    - missing katex.min.css, prism-theme.css
### part-9-safety-security-ethics/module-39-tools-of-the-trade/section-39.4.html
  - P0 structure (1):
    - missing katex.min.css, prism-theme.css
### part-9-safety-security-ethics/module-39-tools-of-the-trade/section-39.5.html
  - P0 structure (1):
    - missing katex.min.css, prism-theme.css

## Files with no findings

The following 6 files are clean across all five dimensions:
- part-7-multimodal-generation/index.html (one cosmetic note: this is a part index, not a section)
- part-7-multimodal-generation/module-31-multimodal/section-31.1.html (passes P0/P1/P2/P3 cleanly; only legacy h2 prefix flagged)

Note: the "clean" set is small because nearly every section is touched by at least one P0 (cosmetic asset load) or P2 (legacy chapter prefix) finding. P4 (callout palette) is clean across the board: all 793 callouts in Parts 7-9 use only the canonical 21-class palette (`algorithm`, `big-picture`, `cross-ref`, `exercise`, `fun-note`, `key-insight`, `key-takeaway`, `lab`, `library-shortcut`, `looking-back`, `note`, `numeric-example`, `pathway`, `postmortem`, `practical-example`, `production-pattern`, `research-frontier`, `self-check`, `thesis-thread`, `tip`, `warning`, plus `bibliography` reserved). Zero off-palette callouts.

## Recommended fix order

1. **section-34.11.html: add KaTeX CSS/JS** (5 minutes). Display math currently renders as raw LaTeX in browsers. Copy the four `<link>`/`<script>` tags from section-34.1.html.
2. **Fix 21 broken internal links** (1 hour, mostly mechanical). Two find-and-replace operations cover most:
   - `section-6.2.html` -> `section-7.2.html` (in section-32.4 only).
   - `../../part-6-agentic-ai/module-38-agent-safety-security/section-25.X.html` -> the new location (the section IDs also changed; check the part-9/module-38 contents).
   - For part-9/module-38 sections that use `../module-XX/...` paths, change to `../../part-6-agentic-ai/module-XX/...`.
3. **Renumber legacy chapter prefixes** (3-5 hours mechanical). 40 sections need `26.x` -> `31.x`, `28.x` -> `34.x`, `29.x` -> `35.x`, `30.x` -> `37.x`, `25.x` -> `38.x` (with the twist that 38.3 needs `25.6.x` -> `38.3.x` and 38.4 needs `25.7.x` -> `38.4.x`).
4. **Resolve duplicate h2 blocks in section-37.3 and section-37.11** (2-3 hours). Decide whether to split into separate sections, merge topically, or simply renumber the second block.
5. **Fix figure number in section-38.3** (5 minutes): `Figure 38.6.1` -> `Figure 38.3.1`.
6. **Clean stale title in section-32.4** (5 minutes): remove `(from old 33.4)` from `<title>` and description meta.
7. **Resolve skipped sub-numbers in section-37.2 (skips 30.2.4) and section-37.9 (skips 30.9.2)** (1 hour).
8. **Convert section-37.1 h3-numbered subsections to h2 and consider splitting** (4-6 hours). The 13,335-word section reads like an omnibus; the rest of Chapter 37 averages ~5,500 words.
9. **(Optional) Adopt a uniform asset block** that always loads `katex.min.css`, `prism-theme.css`, `pygments.css` for every section (30 minutes, mechanical). Prevents future single-section render bugs of the type seen in section-34.11.
