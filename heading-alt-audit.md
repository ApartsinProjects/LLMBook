# Heading hierarchy & alt-text accessibility audit

Total HTML files scanned: 389

## Summary

| Issue | Total | Pages affected |
|---|---:|---:|
| Heading: skipped level (h1->h3 etc) | 250 | 246 |
| Heading: multiple <h1> on page | 0 | 0 |
| Heading: <h1> after non-h1 (demoted) | 0 | 0 |
| Heading: empty heading | 0 | 0 |
| Heading: block element inside heading | 0 | 0 |
| Alt: missing alt attribute | 0 | 0 |
| Alt: empty alt inside <figure> | 0 | 0 |
| Alt: boilerplate text | 7 | 7 |
| Alt: too short (<8 chars in figure) | 4 | 4 |
| Alt: too long (>250 chars) | 62 | 55 |

## Heading hierarchy issues

Files with heading issues: **246**

### Bulk pattern: single h1 -> h3 skip (242 pages)

These pages share the same templating pattern: a single `<h1>` section title followed directly by `<h3>` subsections, with no intermediate `<h2>`. This is consistent across the section template and should be fixed at the template level by either re-leveling subsections to `<h2>` or by inserting an `<h2>` chapter banner.

| Directory | Pages affected |
|---|---:|
| `appendices/appendix-a-mathematical-foundations/` | 4 |
| `appendices/appendix-b-ml-essentials/` | 3 |
| `appendices/appendix-c-python-for-llm/` | 4 |
| `appendices/appendix-d-environment-setup/` | 5 |
| `appendices/appendix-e-git-collaboration/` | 3 |
| `appendices/appendix-g-model-cards/` | 2 |
| `appendices/appendix-h-prompt-templates/` | 8 |
| `appendices/appendix-i-datasets-benchmarks/` | 1 |
| `front-matter/` | 1 |
| `part-1-foundations/module-00-ml-pytorch-foundations/` | 4 |
| `part-1-foundations/module-01-foundations-nlp-text-representation/` | 4 |
| `part-1-foundations/module-02-tokenization-subword-models/` | 3 |
| `part-1-foundations/module-03-sequence-models-attention/` | 3 |
| `part-1-foundations/module-04-transformer-architecture/` | 5 |
| `part-1-foundations/module-05-decoding-text-generation/` | 4 |
| `part-10-frontiers/module-33-emerging-architectures/` | 10 |
| `part-11-idea-to-product/module-34-idea-to-product/` | 5 |
| `part-11-idea-to-product/module-35-shipping-scaling/` | 4 |
| `part-12-llm-applications-across-industries/module-36-legal-llms/` | 1 |
| `part-12-llm-applications-across-industries/module-37-finance-llms/` | 1 |
| `part-2-understanding-llms/module-06-pretraining-scaling-laws/` | 9 |
| `part-2-understanding-llms/module-07-modern-llm-landscape/` | 4 |
| `part-2-understanding-llms/module-08-reasoning-test-time-compute/` | 6 |
| `part-2-understanding-llms/module-09-inference-optimization/` | 7 |
| `part-2-understanding-llms/module-10-interpretability/` | 4 |
| `part-3-working-with-llms/module-11-llm-apis/` | 4 |
| `part-3-working-with-llms/module-12-prompt-engineering/` | 5 |
| `part-3-working-with-llms/module-13-hybrid-ml-llm/` | 5 |
| `part-4-training-adapting/module-14-synthetic-data/` | 7 |
| `part-4-training-adapting/module-15-fine-tuning-fundamentals/` | 7 |
| `part-4-training-adapting/module-16-peft/` | 7 |
| `part-4-training-adapting/module-17-alignment-rlhf-dpo/` | 5 |
| `part-5-retrieval-conversation/module-18-embeddings-vector-db/` | 5 |
| `part-5-retrieval-conversation/module-19-rag/` | 9 |
| `part-5-retrieval-conversation/module-20-conversational-ai/` | 5 |
| `part-6-agentic-ai/module-21-ai-agents/` | 6 |
| `part-6-agentic-ai/module-22-tool-use-protocols/` | 5 |
| `part-6-agentic-ai/module-23-multi-agent-systems/` | 3 |
| `part-6-agentic-ai/module-24-specialized-agents/` | 4 |
| `part-6-agentic-ai/module-25-agent-safety-production/` | 7 |
| `part-7-multimodal-applications/module-26-multimodal/` | 6 |
| `part-7-multimodal-applications/module-27-llm-applications/` | 7 |
| `part-8-evaluation-production/module-28-evaluation-observability/` | 12 |
| `part-8-evaluation-production/module-29-production-engineering/` | 9 |
| `part-9-safety-strategy/module-30-safety-ethics-regulation/` | 12 |
| `part-9-safety-strategy/module-31-strategy-product-roi/` | 7 |

### Non-template heading issues (4 pages)

#### `part-11-idea-to-product/module-34-idea-to-product/section-34.4.html`
- L40: skipped level (h1 -> h3)
- L56: skipped level (h2 -> h4)

#### `part-11-idea-to-product/module-34-idea-to-product/section-34.7.html`
- L40: skipped level (h1 -> h3)
- L53: skipped level (h2 -> h4)

#### `part-3-working-with-llms/module-13-hybrid-ml-llm/section-13.3.html`
- L40: skipped level (h1 -> h3)
- L55: skipped level (h2 -> h4)

#### `part-7-multimodal-applications/module-26-multimodal/section-26.5.html`
- L44: skipped level (h1 -> h3)
- L238: skipped level (h2 -> h4)

## Alt-text issues

### Missing `alt` attribute (0 total)

_None._

### Empty `alt=""` inside `<figure>` (0 total)

_None._

### Boilerplate alt text (7 total)

- `appendices/glossary/index.html` L32 [contains 'graphic']: alt="A vast magical library with floating holographic term cards glowing in different colors by category, browsed by friendl..."
- `part-1-foundations/module-01-foundations-nlp-text-representation/section-1.3.html` L168 [contains 'diagram of']: alt="Diagram of the Word2Vec Skip-gram architecture showing a center word as input, a hidden embedding layer, and output con..."
- `part-1-foundations/module-01-foundations-nlp-text-representation/section-1.4.html` L66 [contains 'illustration of']: alt="Illustration of the polysemy problem showing the word bank with multiple meanings (financial institution, river bank, t..."
- `part-1-foundations/module-02-tokenization-subword-models/section-2.3.html` L400 [contains 'image']: alt="Multimodal models convert images to token sequences via patch embedding"
- `part-3-working-with-llms/module-11-llm-apis/section-11.4.html` L230 [contains 'image']: alt="A robot with multiple sensory inputs (eyes for images, ears for audio, hands for text) representing multimodal APIs"
- `part-7-multimodal-applications/module-26-multimodal/index.html` L32 [contains 'image']: alt="Multimodal AI architecture: four input modalities (image of a cat on a bench, the matching text caption 'A fluffy orang..."
- `part-7-multimodal-applications/module-26-multimodal/section-26.1.html` L56 [contains 'image']: alt="A blurry, noisy image gradually becoming clear through the diffusion denoising process"

### Alt text too short (<8 chars, inside `<figure>`) (4 total)

- `appendices/appendix-k-langchain/section-k.1.html` L202: alt="Diagram" src=`images/section-l.1-svg1.png`
- `appendices/appendix-k-langchain/section-k.2.html` L191: alt="Diagram" src=`images/section-l.2-svg1.png`
- `appendices/appendix-k-langchain/section-k.3.html` L161: alt="Diagram" src=`images/section-l.3-svg1.png`
- `appendices/appendix-k-langchain/section-k.5.html` L147: alt="Diagram" src=`images/section-l.5-svg1.png`

### Alt text too long (>250 chars) (62 total)

- `front-matter/fm-what-this-book-covers.html` L69: alt length = 354 chars, src=`images/fm-3-1-dependency-diagram.png`
- `index.html` L691: alt length = 328 chars, src=`images/book-cover.png`
- `part-1-foundations/module-01-foundations-nlp-text-representation/section-1.3.html` L282: alt length = 435 chars, src=`images/fig-1.3.5-cosine-sim.png`
- `part-1-foundations/module-03-sequence-models-attention/section-3.2.html` L136: alt length = 252 chars, src=`images/fig-3.2.5-bahdanau-attention.png`
- `part-10-frontiers/module-33-emerging-architectures/section-33.10.html` L69: alt length = 451 chars, src=`images/fig-34.10-domain-tokenization.png`
- `part-10-frontiers/module-33-emerging-architectures/section-33.3.html` L53: alt length = 274 chars, src=`images/ch34-alternative-architectures-zoo.png`
- `part-10-frontiers/module-33-emerging-architectures/section-33.3.html` L99: alt length = 410 chars, src=`images/fig-33.3.2-mamba-vs-transformer.png`
- `part-10-frontiers/module-33-emerging-architectures/section-33.3.html` L299: alt length = 293 chars, src=`images/fig-33.3.3-attention-variants-taxonomy.png`
- `part-10-frontiers/module-33-emerging-architectures/section-33.4.html` L66: alt length = 383 chars, src=`images/fig-33.4.2-world-model-architecture.png`
- `part-10-frontiers/module-33-emerging-architectures/section-33.5.html` L53: alt length = 264 chars, src=`images/ch34-system1-system2-thinking.png`
- `part-10-frontiers/module-33-emerging-architectures/section-33.6.html` L53: alt length = 263 chars, src=`images/ch34-memory-filing-cabinet.png`
- `part-10-frontiers/module-33-emerging-architectures/section-33.9.html` L56: alt length = 425 chars, src=`images/fig-33.9.1-tool-orchestration-economy.png`
- `part-11-idea-to-product/module-34-idea-to-product/section-34.2.html` L135: alt length = 313 chars, src=`images/five-role-patterns.png`
- `part-11-idea-to-product/module-34-idea-to-product/section-34.3.html` L185: alt length = 314 chars, src=`images/feasibility-funnel.png`
- `part-11-idea-to-product/module-35-shipping-scaling/section-35.1.html` L71: alt length = 456 chars, src=`images/cost-engine-levers.png`
- `part-11-idea-to-product/module-35-shipping-scaling/section-35.3.html` L119: alt length = 472 chars, src=`images/cognitive-lockin-curves.png`
- `part-11-idea-to-product/module-35-shipping-scaling/section-35.3.html` L255: alt length = 275 chars, src=`images/fig-35.3.4-portable-monogamy-architecture.png`
- `part-11-idea-to-product/module-35-shipping-scaling/section-35.4.html` L218: alt length = 271 chars, src=`images/fig-35.4.6-continuous-steering-loop.png`
- `part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.4.html` L120: alt length = 269 chars, src=`images/fig-6.4.3-curation-funnel.png`
- `part-2-understanding-llms/module-08-reasoning-test-time-compute/section-8.4.html` L44: alt length = 253 chars, src=`images/ch08-prompting-reasoning-models.png`
- `part-3-working-with-llms/module-13-hybrid-ml-llm/section-13.6.html` L56: alt length = 264 chars, src=`images/fig-13.8.1-log-to-dataset-pipeline.png`
- `part-4-training-adapting/module-14-synthetic-data/section-14.1.html` L43: alt length = 303 chars, src=`images/fig-14.1.2-annotation-cost.png`
- `part-4-training-adapting/module-14-synthetic-data/section-14.2.html` L48: alt length = 945 chars, src=`images/fig-14.2.4-evol-instruct-operators.png`
- `part-4-training-adapting/module-15-fine-tuning-fundamentals/section-15.1.html` L46: alt length = 675 chars, src=`images/fig-15.1.2-fine-tune-decision-tree.png`
- `part-4-training-adapting/module-16-peft/section-16.1.html` L132: alt length = 547 chars, src=`images/fig-16.1.5-lora-decomposition.png`
- `part-4-training-adapting/module-17-alignment-rlhf-dpo/section-17.4.html` L66: alt length = 403 chars, src=`images/rlvr-auto-graded-exam.png`
- `part-5-retrieval-conversation/module-19-rag/section-19.3.html` L52: alt length = 679 chars, src=`images/fig-19.3.2-knowledge-graph-example.png`
- `part-5-retrieval-conversation/module-19-rag/section-19.3.html` L319: alt length = 410 chars, src=`images/fig-20.3-graphrag-pipeline.png`
- `part-5-retrieval-conversation/module-19-rag/section-19.7.html` L91: alt length = 290 chars, src=`images/fig-19.7.1-graphrag-pipeline.png`
- `part-5-retrieval-conversation/module-19-rag/section-19.8.html` L57: alt length = 344 chars, src=`images/fig-19.8.1-rag-ingestion-pipeline.png`
- `part-5-retrieval-conversation/module-20-conversational-ai/section-20.5.html` L53: alt length = 312 chars, src=`images/fig-20.6.1-voice-agent-architecture.png`
- `part-6-agentic-ai/module-22-tool-use-protocols/section-22.1.html` L72: alt length = 851 chars, src=`images/fig-22.1.2-function-calling-loop.png`
- `part-6-agentic-ai/module-23-multi-agent-systems/section-23.2.html` L44: alt length = 495 chars, src=`images/fig-23.2.1-multi-agent-topologies.png`
- `part-6-agentic-ai/module-24-specialized-agents/section-24.1.html` L44: alt length = 296 chars, src=`images/ch25-opener-specialist-robots.png`
- `part-6-agentic-ai/module-24-specialized-agents/section-24.3.html` L44: alt length = 349 chars, src=`images/ch25-research-agent-detective.png`
- `part-6-agentic-ai/module-24-specialized-agents/section-24.4.html` L51: alt length = 284 chars, src=`images/fig-24.7.1-coding-agent-generations.png`
- `part-6-agentic-ai/module-25-agent-safety-production/section-25.1.html` L44: alt length = 483 chars, src=`images/ch24-castle-defense-v3.png`
- `part-6-agentic-ai/module-25-agent-safety-production/section-25.1.html` L81: alt length = 370 chars, src=`images/fig-25.1.3-prompt-injection-defense-layers.png`
- `part-6-agentic-ai/module-25-agent-safety-production/section-25.2.html` L44: alt length = 280 chars, src=`images/ch26-sandbox-fishbowl.png`
- `part-6-agentic-ai/module-25-agent-safety-production/section-25.3.html` L44: alt length = 294 chars, src=`images/ch26-observability-dashboard.png`
- `part-6-agentic-ai/module-25-agent-safety-production/section-25.3.html` L65: alt length = 325 chars, src=`images/fig-25.3.2-agent-observability-stack.png`
- `part-7-multimodal-applications/module-26-multimodal/index.html` L32: alt length = 448 chars, src=`images/chapter-opener.png`
- `part-7-multimodal-applications/module-26-multimodal/section-26.1.html` L75: alt length = 561 chars, src=`images/fig-26.1.7-ddpm-forward-reverse.png`
- `part-7-multimodal-applications/module-26-multimodal/section-26.5.html` L51: alt length = 338 chars, src=`images/fig-26.5.1-vision-language-action-pipeline.png`
- `part-7-multimodal-applications/module-26-multimodal/section-26.6.html` L50: alt length = 329 chars, src=`images/fig-26.6.1-robot-cloud-edge-hierarchy.png`
- `part-7-multimodal-applications/module-26-multimodal/section-26.7.html` L73: alt length = 442 chars, src=`images/fig-26.7.2-gaussian-splatting-pipeline.png`
- `part-7-multimodal-applications/module-27-llm-applications/index.html` L32: alt length = 459 chars, src=`images/chapter-opener.png`
- `part-7-multimodal-applications/module-27-llm-applications/section-27.1.html` L65: alt length = 548 chars, src=`images/fig-27.1.2-fill-in-the-middle-fim-the-model-receives-prefix-and-suff.png`
- `part-8-evaluation-production/module-28-evaluation-observability/section-28.11.html` L59: alt length = 289 chars, src=`images/fig-28.13.1-experiment-design-flow.png`
- `part-8-evaluation-production/module-29-production-engineering/section-29.6.html` L399: alt length = 254 chars, src=`images/fig-29.6.2-framework-comparison.png`
- `part-8-evaluation-production/module-29-production-engineering/section-29.8.html` L54: alt length = 255 chars, src=`images/reliability-engineering-safety-net.png`
- `part-8-evaluation-production/module-29-production-engineering/section-29.9.html` L58: alt length = 307 chars, src=`images/fig-29.9.1-k8s-llm-stack.png`
- `part-9-safety-strategy/module-30-safety-ethics-regulation/section-30.10.html` L53: alt length = 273 chars, src=`images/green-ai-carbon-footprint.png`
- `part-9-safety-strategy/module-30-safety-ethics-regulation/section-30.11.html` L689: alt length = 280 chars, src=`images/federated-learning-distributed.png`
- `part-9-safety-strategy/module-30-safety-ethics-regulation/section-30.2.html` L52: alt length = 276 chars, src=`images/hallucination-wrong-treasure-map.png`
- `part-9-safety-strategy/module-30-safety-ethics-regulation/section-30.3.html` L43: alt length = 269 chars, src=`images/bias-fairness-scales.png`
- `part-9-safety-strategy/module-30-safety-ethics-regulation/section-30.9.html` L368: alt length = 361 chars, src=`images/fig-30.9.2-gpai-obligations.png`
- `part-9-safety-strategy/module-31-strategy-product-roi/section-31.4.html` L43: alt length = 286 chars, src=`images/vendor-evaluation-market.png`
- `part-9-safety-strategy/module-31-strategy-product-roi/section-31.5.html` L43: alt length = 268 chars, src=`images/compute-planning-blueprint.png`
- `part-9-safety-strategy/module-31-strategy-product-roi/section-31.6.html` L44: alt length = 274 chars, src=`images/enterprise-integration-plumbing.png`
- `part-9-safety-strategy/module-31-strategy-product-roi/section-31.6.html` L53: alt length = 309 chars, src=`images/fig-31.7.1-enterprise-auth-flow.png`
- `part-9-safety-strategy/module-31-strategy-product-roi/section-31.7.html` L44: alt length = 271 chars, src=`images/economic-design-token-kitchen.png`

## Worst-offender pages (3+ combined issues)

| Page | Heading issues | Alt issues | Total |
|---|---:|---:|---:|
| `part-10-frontiers/module-33-emerging-architectures/section-33.3.html` | 1 | 3 | 4 |
| `part-1-foundations/module-01-foundations-nlp-text-representation/section-1.3.html` | 1 | 2 | 3 |
| `part-11-idea-to-product/module-35-shipping-scaling/section-35.3.html` | 1 | 2 | 3 |
| `part-5-retrieval-conversation/module-19-rag/section-19.3.html` | 1 | 2 | 3 |
| `part-6-agentic-ai/module-25-agent-safety-production/section-25.1.html` | 1 | 2 | 3 |
| `part-6-agentic-ai/module-25-agent-safety-production/section-25.3.html` | 1 | 2 | 3 |
| `part-7-multimodal-applications/module-26-multimodal/section-26.1.html` | 1 | 2 | 3 |
| `part-7-multimodal-applications/module-26-multimodal/section-26.5.html` | 2 | 1 | 3 |
| `part-9-safety-strategy/module-31-strategy-product-roi/section-31.6.html` | 1 | 2 | 3 |

## Recommended fix priority

1. **Re-level 250 skipped-heading instances** (e.g. h1 -> h3). Fix at the section template by either inserting an `<h2>` chapter banner or demoting the section subheads from `<h3>` to `<h2>`.
2. **Rewrite 7 boilerplate and 4 ultra-short alts** with concrete descriptions. 'Image of X' and 'Diagram' add no information.
3. **Trim 62 overlong alts (>250 chars)** by moving detail to the figure caption.
