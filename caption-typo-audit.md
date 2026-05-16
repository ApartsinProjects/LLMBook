# Caption typo audit

Scope: every `.html` page under the project root (KDP, scripts, node_modules, pagefind, templates, agents, vendor, temp_*, *backups* directories excluded). Only these caption containers are inspected: `<div class="comparison-table-title">`, `<figcaption>`, `<div class="code-caption">`, `<div class="diagram-caption">`.

- HTML files scanned: **389**
- Caption elements inspected: **2250**
- Files modified by auto-fix: **28**
- Total auto-fixes applied: **28**
- Unbalanced-paren captions (review queue): **0**
- Colon-style deviations (review queue): **14**

Audit produced by `scripts/_audit_caption_typos.py`. This report records the
state of the project **after** the auto-fix pass. The "Auto-fixes applied"
section preserves the list of edits performed during the first run; rerunning
the script is idempotent and will simply re-confirm that 0 new fixes are
needed.

## 1. Summary

| Category | Action | Count |
|---|---|---:|
| Missing space + opening paren (`Xas of YYYY)`) | AUTO-FIX | 28 |
| Unbalanced parentheses in caption text | REPORT | 0 |
| Colon-style deviations after Figure/Code/Table label | REPORT | 14 |
| Trailing punctuation variants (info only) | REPORT | 2250 |

## 2. Auto-fixes applied (Category 1)

All rewrites apply the rule `r"([A-Za-z])as of (\d{4})\)" -> r"\1 (as of \2)"`. The 'before' / 'after' snippets show a 40-char window around the match. All 28 affected captions were inside `<div class="comparison-table-title">` elements.

| File | Kind | Before | After |
|---|---|---|---|
| `part-2-understanding-llms/module-08-reasoning-test-time-compute/section-8.2.html` | comparison-table-title | `"comparison-table-title">Comparison Tableas of 2026)</div> <ta` | `"comparison-table-title">Comparison Table (as of 2026)</div> <ta` |
| `part-2-understanding-llms/module-09-inference-optimization/section-9.4.html` | comparison-table-title | `parison-table-title">Framework Comparisonas of 2026)</div> <ta` | `parison-table-title">Framework Comparison (as of 2026)</div> <ta` |
| `part-2-understanding-llms/module-10-interpretability/section-10.4.html` | comparison-table-title | `-title">Evaluation of Explanation Qualityas of 2026)</div> <ta` | `-title">Evaluation of Explanation Quality (as of 2026)</div> <ta` |
| `part-3-working-with-llms/module-11-llm-apis/section-11.1.html` | comparison-table-title | `mparison-table-title">Provider Comparisonas of 2026)</div> <ta` | `mparison-table-title">Provider Comparison (as of 2026)</div> <ta` |
| `part-3-working-with-llms/module-11-llm-apis/section-11.2.html` | comparison-table-title | `title">Cross-Provider Tool Use Comparisonas of 2026)</div> <ta` | `title">Cross-Provider Tool Use Comparison (as of 2026)</div> <ta` |
| `part-3-working-with-llms/module-12-prompt-engineering/section-12.2.html` | comparison-table-title | `title">Comparison of Reasoning Techniquesas of 2026)</div> <ta` | `title">Comparison of Reasoning Techniques (as of 2026)</div> <ta` |
| `part-3-working-with-llms/module-12-prompt-engineering/section-12.3.html` | comparison-table-title | `le">Comparison of Optimization Approachesas of 2026)</div> <ta` | `le">Comparison of Optimization Approaches (as of 2026)</div> <ta` |
| `part-4-training-adapting/module-14-synthetic-data/section-14.1.html` | comparison-table-title | `e-title">Legal and Ethical Considerationsas of 2026)</div> <ta` | `e-title">Legal and Ethical Considerations (as of 2026)</div> <ta` |
| `part-4-training-adapting/module-14-synthetic-data/section-14.6.html` | comparison-table-title | `ble-title">Quality vs. Quantity Tradeoffsas of 2026)</div> <ta` | `ble-title">Quality vs. Quantity Tradeoffs (as of 2026)</div> <ta` |
| `part-4-training-adapting/module-16-peft/section-16.2.html` | comparison-table-title | `tle">Comprehensive PEFT Method Comparisonas of 2026)</div> <ta` | `tle">Comprehensive PEFT Method Comparison (as of 2026)</div> <ta` |
| `part-4-training-adapting/module-16-peft/section-16.3.html` | comparison-table-title | `rison-table-title">Tool Comparison Matrixas of 2026)</div> <ta` | `rison-table-title">Tool Comparison Matrix (as of 2026)</div> <ta` |
| `part-4-training-adapting/module-16-peft/section-16.5.html` | comparison-table-title | `tle">White-Box vs. Black-Box Distillationas of 2026)</div> <ta` | `tle">White-Box vs. Black-Box Distillation (as of 2026)</div> <ta` |
| `part-4-training-adapting/module-16-peft/section-16.6.html` | comparison-table-title | `on-table-title">Merging Method Comparisonas of 2026)</div> <ta` | `on-table-title">Merging Method Comparison (as of 2026)</div> <ta` |
| `part-5-retrieval-conversation/module-18-embeddings-vector-db/section-18.3.html` | comparison-table-title | `comparison-table-title">Comparison Matrixas of 2026)</div> <ta` | `comparison-table-title">Comparison Matrix (as of 2026)</div> <ta` |
| `part-5-retrieval-conversation/module-18-embeddings-vector-db/section-18.4.html` | comparison-table-title | `table-title">Chunking Strategy Comparisonas of 2026)</div> <ta` | `table-title">Chunking Strategy Comparison (as of 2026)</div> <ta` |
| `part-5-retrieval-conversation/module-19-rag/section-19.2.html` | comparison-table-title | `le">Comparison of Advanced RAG Techniquesas of 2026)</div> <ta` | `le">Comparison of Advanced RAG Techniques (as of 2026)</div> <ta` |
| `part-5-retrieval-conversation/module-19-rag/section-19.3.html` | comparison-table-title | `le-title">When to Use Knowledge Graph RAGas of 2026)</div> <ta` | `le-title">When to Use Knowledge Graph RAG (as of 2026)</div> <ta` |
| `part-5-retrieval-conversation/module-20-conversational-ai/section-20.1.html` | comparison-table-title | `e-title">Comparing Dialogue Architecturesas of 2026)</div> <ta` | `e-title">Comparing Dialogue Architectures (as of 2026)</div> <ta` |
| `part-5-retrieval-conversation/module-20-conversational-ai/section-20.3.html` | comparison-table-title | `-table-title">Comparing Memory Approachesas of 2026)</div> <ta` | `-table-title">Comparing Memory Approaches (as of 2026)</div> <ta` |
| `part-5-retrieval-conversation/module-20-conversational-ai/section-20.4.html` | comparison-table-title | `e">Comparing Conversation Flow Strategiesas of 2026)</div> <ta` | `e">Comparing Conversation Flow Strategies (as of 2026)</div> <ta` |
| `part-5-retrieval-conversation/module-20-conversational-ai/section-20.5.html` | comparison-table-title | `mparing Voice AI Orchestration Frameworksas of 2026)</div> <ta` | `mparing Voice AI Orchestration Frameworks (as of 2026)</div> <ta` |
| `part-7-multimodal-applications/module-26-multimodal/section-26.3.html` | comparison-table-title | `mparing Document Understanding Approachesas of 2026)</div> <ta` | `mparing Document Understanding Approaches (as of 2026)</div> <ta` |
| `part-7-multimodal-applications/module-27-llm-applications/section-27.1.html` | comparison-table-title | `tle">AI-Native IDEs and Coding Assistantsas of 2026)</div> <ta` | `tle">AI-Native IDEs and Coding Assistants (as of 2026)</div> <ta` |
| `part-8-evaluation-production/module-28-evaluation-observability/section-28.6.html` | comparison-table-title | `mparison-table-title">Platform Comparisonas of 2026)</div> <ta` | `mparison-table-title">Platform Comparison (as of 2026)</div> <ta` |
| `part-9-safety-strategy/module-30-safety-ethics-regulation/section-30.1.html` | comparison-table-title | `comparison-table-title">Attack Comparisonas of 2026)</div> <ta` | `comparison-table-title">Attack Comparison (as of 2026)</div> <ta` |
| `part-9-safety-strategy/module-30-safety-ethics-regulation/section-30.4.html` | comparison-table-title | `-title">GDPR Requirements for LLM Systemsas of 2026)</div> <ta` | `-title">GDPR Requirements for LLM Systems (as of 2026)</div> <ta` |
| `part-9-safety-strategy/module-30-safety-ethics-regulation/section-30.5.html` | comparison-table-title | `e-title">Governance Frameworks Comparisonas of 2026)</div> <ta` | `e-title">Governance Frameworks Comparison (as of 2026)</div> <ta` |
| `part-9-safety-strategy/module-31-strategy-product-roi/section-31.2.html` | comparison-table-title | `e-title">Success Metrics for LLM Productsas of 2026)</div> <ta` | `e-title">Success Metrics for LLM Products (as of 2026)</div> <ta` |

## 3. Unbalanced parentheses (manual review queue)

_All caption parentheses are balanced after the auto-fix pass._

## 4. Colon-style deviations after Figure/Code/Table label

Canonical forms (both accepted):

- `<strong>Figure X.Y.Z</strong>: caption text`
- `<strong>Figure X.Y.Z:</strong> caption text`

Deviation reasons: `missing-colon`, `double-colon`, `period-after-label`, `no-colon-no-text`, `label-tag-malformed`.

### label-tag-malformed (2)

| File | Line | Kind | Caption text |
|---|---:|---|---|
| `appendices/glossary/index.html` | 33 | figcaption | Figure Glossary Section 0.1 : A vast magical library with floating holographic term cards glowing in different colors by category,.... |
| `part-9-safety-strategy/module-30-safety-ethics-regulation/section-30.3.html` | 159 | code-caption | Pseudocode 29.3.2: Measuring toxicity disparity across demographic groups using an automated toxicity classifier . The function averages toxicity scores per gr... |

### no-colon-no-text (12)

| File | Line | Kind | Caption text |
|---|---:|---|---|
| `part-8-evaluation-production/module-29-production-engineering/section-29.1.html` | 142 | diagram-caption | Figure 29.1.2 The three-layer architecture separates API concerns, application logic, and model inference so each layer can evolve independently. |
| `part-8-evaluation-production/module-29-production-engineering/section-29.2.html` | 165 | diagram-caption | Figure 29.2.3 Token streaming pipeline and how each frontend framework implements it, from server-side generation to client-side rendering. |
| `part-8-evaluation-production/module-29-production-engineering/section-29.3.html` | 285 | diagram-caption | Figure 29.3.2 Complete request flow with rate limiting, backpressure queue, auto-scaling GPU workers, and metrics collection. Rejected requests receive immedia... |
| `part-8-evaluation-production/module-29-production-engineering/section-29.4.html` | 160 | diagram-caption | Figure 29.4.1 The LLMOps lifecycle connects four phases (develop, test, deploy, monitor) through a continuous feedback loop, with a shared registry tracking al... |
| `part-9-safety-strategy/module-30-safety-ethics-regulation/section-30.1.html` | 124 | diagram-caption | Figure 30.1.2 The OWASP Top 10 for LLM applications organized into three threat families, each with corresponding defensive strategies. |
| `part-9-safety-strategy/module-30-safety-ethics-regulation/section-30.2.html` | 257 | diagram-caption | Figure 30.2.4 A production hallucination pipeline routes LLM output through detection checks and selects the response strategy based on confidence score and ap... |
| `part-9-safety-strategy/module-30-safety-ethics-regulation/section-30.7.html` | 272 | diagram-caption | Figure 30.7.3 Two geometric views of unlearning in weight space. Gradient ascent (left) moves away from the forget set's loss minimum. Task vector negation (ri... |
| `part-9-safety-strategy/module-31-strategy-product-roi/section-31.1.html` | 315 | diagram-caption | Figure 31.1.3 The four-phase Use Case Discovery Workshop progressively filters raw pain points into ranked, data-ready LLM use cases. |
| `part-9-safety-strategy/module-31-strategy-product-roi/section-31.2.html` | 305 | diagram-caption | Figure 31.2.2 The LLM Product Metrics Pyramid showing three measurement layers from model internals to business outcomes. |
| `part-9-safety-strategy/module-31-strategy-product-roi/section-31.3.html` | 323 | diagram-caption | Figure 31.3.3 Side-by-side ROI comparison showing how SaaS deployments and custom-built RAG systems have fundamentally different payback profiles |
| `part-9-safety-strategy/module-31-strategy-product-roi/section-31.4.html` | 279 | diagram-caption | Figure 31.4.2 The LLM technology stack with build vs. buy recommendations at each layer, from commodity infrastructure to differentiating application logic |
| `part-9-safety-strategy/module-31-strategy-product-roi/section-31.5.html` | 421 | diagram-caption | Figure 31.5.3 Monthly compute budget breakdown showing how inference dominates spend, guiding optimization priorities |

## 5. Trailing punctuation summary (info only)

Overall mix:

| Trailing char | Captions | % |
|---|---:|---:|
| `.` | 1211 | 53.8% |
| `none` | 1037 | 46.1% |
| `?` | 2 | 0.1% |

**Dominant style:** `.` (1211 of 2250 captions, 53.8%). Captions predominantly end with a period before `</...>`.

Per caption-kind mix:

| Kind | Period `.` | Question `?` | Exclaim `!` | None |
|---|---:|---:|---:|---:|
| comparison-table-title | 0 | 0 | 0 | 291 |
| figcaption | 269 | 2 | 0 | 5 |
| code-caption | 648 | 0 | 0 | 721 |
| diagram-caption | 294 | 0 | 0 | 20 |

Notable per-kind observations:

- **`comparison-table-title`** is uniformly **no terminal punctuation** (291 of 291, 100%). The 28 typo fixes all live in this kind and now match the canonical `Title (as of 2026)` form with no trailing dot.
- **`figcaption`** strongly favours the **period** (269 of 276, 97.5%).
- **`code-caption`** is split roughly 47/53 between period and no terminal punctuation (648 vs. 721). There is no single dominant style here; flag for human review if standardisation is desired.
- **`diagram-caption`** strongly favours the **period** (294 of 314, 93.6%); the 12 "no-colon-no-text" deviations listed above also happen to lack a trailing period.

---

Audit produced by `scripts/_audit_caption_typos.py`.
