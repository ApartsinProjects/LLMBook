# Wide-cell tables and oversized image audit

Scanned 389 HTML files and 2013 image files. Wide-table heuristic: table has at least 3 columns AND one column's longest cell is at least 3x the next-largest column's longest cell AND that longest cell has at least 60 characters of rendered text.

## 1. Summary

| Category | Count |
| --- | ---: |
| Wide-cell table findings | 14 |
| Files with at least one wide-cell finding | 12 |
| Oversized raster images | 242 |
| Oversized / problematic SVGs | 7 |
| SVGs with embedded base64 raster | 0 |

## 2. Wide-cell tables

| File:Line | Cols | Outlier column | Outlier max | Next max | Ratio |
| --- | ---: | --- | ---: | ---: | ---: |
| part-11-idea-to-product/module-35-shipping-scaling/section-35.1.html:293 | 4 | #2 Requirement | 188 | 15 | 12.5x |
| part-9-safety-strategy/module-30-safety-ethics-regulation/section-30.4.html:90 | 4 | #4 Key Requirements | 261 | 29 | 9.0x |
| part-4-training-adapting/module-14-synthetic-data/section-14.1.html:335 | 3 | #3 Mitigation | 158 | 21 | 7.5x |
| part-4-training-adapting/module-16-peft/section-16.5.html:599 | 3 | #3 Key Restriction | 167 | 31 | 5.4x |
| appendices/appendix-m-inference-serving/section-m.1.html:109 | 3 | #3 Description | 87 | 17 | 5.1x |
| part-1-foundations/module-00-ml-pytorch-foundations/section-0.2.html:213 | 3 | #3 How It Works | 83 | 17 | 4.9x |
| appendices/appendix-a-mathematical-foundations/section-a.2.html:75 | 3 | #3 LLM Relevance | 67 | 17 | 3.9x |
| appendices/appendix-u-freshness-2026/index.html:32 | 4 | #3 Why it matters | 213 | 57 | 3.7x |
| part-9-safety-strategy/module-31-strategy-product-roi/section-31.5.html:59 | 6 | #6 Best For | 61 | 17 | 3.6x |
| appendices/appendix-u-freshness-2026/index.html:44 | 4 | #3 What it solves | 111 | 32 | 3.5x |
| capstone/requirements.html:463 | 3 | #3 What Evaluators Look For | 67 | 20 | 3.4x |
| part-2-understanding-llms/module-08-reasoning-test-time-compute/section-8.1.html:98 | 4 | #4 Rationale | 90 | 27 | 3.3x |
| part-3-working-with-llms/module-13-hybrid-ml-llm/section-13.5.html:1079 | 4 | #4 Best For | 66 | 20 | 3.3x |
| capstone/requirements.html:510 | 3 | #3 Key Technical Challenges | 72 | 24 | 3.0x |

### Wide-cell findings (offending text)

- `part-11-idea-to-product/module-35-shipping-scaling/section-35.1.html:293` col #2 `Requirement` (ratio 12.5x, 188 vs 15 chars):
  > Regulatory posture is understood. AI transparency labels are in the UI. Data processing agreements are signed with model providers. Risk tier under EU AI Act (or equivalent) is documented.
- `part-9-safety-strategy/module-30-safety-ethics-regulation/section-30.4.html:90` col #4 `Key Requirements` (ratio 9.0x, 261 vs 29 chars):
  > General-purpose AI model providers must publish technical documentation, comply with EU copyright law, and provide training data summaries. Systemic risk models (over 10 25 FLOPs ) face additional obl...
- `part-4-training-adapting/module-14-synthetic-data/section-14.1.html:335` col #3 `Mitigation` (ratio 7.5x, 158 vs 21 chars):
  > Check provider ToS for training data generation permissions. OpenAI's ToS permit using outputs to train models (with some restrictions on competing services).
- `part-4-training-adapting/module-16-peft/section-16.5.html:599` col #3 `Key Restriction` (ratio 5.4x, 167 vs 31 chars):
  > You may not use outputs to "develop any artificial intelligence models that compete with our Products and Services." Fine-tuning through OpenAI's own API is permitted.
- `appendices/appendix-m-inference-serving/section-m.1.html:109` col #3 `Description` (ratio 5.1x, 87 vs 17 chars):
  > Nucleus sampling ; considers tokens whose cumulative probability reaches this threshold
- `part-1-foundations/module-00-ml-pytorch-foundations/section-0.2.html:213` col #3 `How It Works` (ratio 4.9x, 83 vs 17 chars):
  > Scales weights by √(2/ $n_{in}$ ), accounting for ReLU zeroing out half the values.
- `appendices/appendix-a-mathematical-foundations/section-a.2.html:75` col #3 `LLM Relevance` (ratio 3.9x, 67 vs 17 chars):
  > Weight initialization, noise in diffusion models, VAE latent spaces
- `appendices/appendix-u-freshness-2026/index.html:32` col #3 `Why it matters` (ratio 3.7x, 213 vs 57 chars):
  > R1 is the first open-weights reasoning model competitive with frontier. The 4-stage training pipeline (cold-start SFT + RLVR + rejection-sampling SFT + final DPO ) is the only public blueprint for o1-...
- `part-9-safety-strategy/module-31-strategy-product-roi/section-31.5.html:59` col #6 `Best For` (ratio 3.6x, 61 vs 17 chars):
  > Cost-competitive training; integrated in Intel cloud partners
- `appendices/appendix-u-freshness-2026/index.html:44` col #3 `What it solves` (ratio 3.5x, 111 vs 32 chars):
  > Standardizes how streaming agent events are surfaced to frontends. The third leg of the agentic protocol stack.
- `capstone/requirements.html:463` col #3 `What Evaluators Look For` (ratio 3.4x, 67 vs 20 chars):
  > Multiple evaluation methods; statistical analysis; honest reporting
- `part-2-understanding-llms/module-08-reasoning-test-time-compute/section-8.1.html:98` col #4 `Rationale` (ratio 3.3x, 90 vs 27 chars):
  > Structured reasoning explores the solution space more efficiently than independent samples
- `part-3-working-with-llms/module-13-hybrid-ml-llm/section-13.5.html:1079` col #4 `Best For` (ratio 3.3x, 66 vs 20 chars):
  > Abstractive keyphrases, categorization, domain-specific extraction
- `capstone/requirements.html:510` col #3 `Key Technical Challenges` (ratio 3.0x, 72 vs 24 chars):
  > Safety-critical outputs, evidence-based citations, regulatory compliance

## 3. Oversized images

| Path | Size | Dimensions | Flags | Suggested action |
| --- | ---: | --- | --- | --- |
| part-8-evaluation-production/module-29-production-engineering/images/restaurant-kitchen-architecture.png | 2.34 MB | 1500x1120 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-5-retrieval-conversation/module-18-embeddings-vector-db/images/hnsw-express-lanes.png | 2.30 MB | 1500x1120 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-3-working-with-llms/module-12-prompt-engineering/images/system-prompt-director.png | 2.28 MB | 1500x1120 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-3-working-with-llms/module-13-hybrid-ml-llm/images/hybrid-pipeline-assembly.png | 2.21 MB | 1500x1120 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-9-safety-strategy/module-30-safety-ethics-regulation/images/regulation-traffic-lights.png | 2.19 MB | 1500x1120 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-4-training-adapting/module-14-synthetic-data/images/synthetic-data-factory.png | 2.18 MB | 1500x1120 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-4-training-adapting/module-16-peft/images/qlora-truck-decals.png | 2.17 MB | 1500x1120 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-4-training-adapting/module-16-peft/images/lora-sticky-note.png | 2.12 MB | 1500x1120 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-5-retrieval-conversation/module-18-embeddings-vector-db/images/vector-db-librarian.png | 2.09 MB | 1500x1120 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-5-retrieval-conversation/module-19-rag/images/knowledge-graph-islands.png | 2.08 MB | 1500x1120 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-3-working-with-llms/module-12-prompt-engineering/images/prompt-chaining-relay.png | 2.07 MB | 1500x1120 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-3-working-with-llms/module-11-llm-apis/images/reasoning-model-thinker.png | 2.06 MB | 1500x1120 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-9-safety-strategy/module-30-safety-ethics-regulation/images/governance-control-tower.png | 2.05 MB | 1500x1120 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-2-understanding-llms/module-06-pretraining-scaling-laws/images/distributed-training-orchestra.png | 2.05 MB | 1500x1120 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-1-foundations/module-02-tokenization-subword-models/images/special-tokens-traffic.png | 2.03 MB | 1500x1120 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-3-working-with-llms/module-11-llm-apis/images/api-ecosystem-market.png | 2.01 MB | 1500x1120 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-9-safety-strategy/module-30-safety-ethics-regulation/images/embassy-security-layers.png | 2.01 MB | 1500x1120 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-9-safety-strategy/module-30-safety-ethics-regulation/images/fact-checking-detective.png | 2.01 MB | 1500x1120 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-3-working-with-llms/module-11-llm-apis/images/rate-limit-bouncer.png | 2.00 MB | 1500x1120 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-2-understanding-llms/module-06-pretraining-scaling-laws/images/adam-optimizer-navigator.png | 1.99 MB | 1500x1120 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-5-retrieval-conversation/module-18-embeddings-vector-db/images/product-quantization-paint.png | 1.97 MB | 1500x1120 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-1-foundations/module-00-ml-pytorch-foundations/images/dropout-sleeping-neurons.png | 1.97 MB | 1500x1120 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-5-retrieval-conversation/module-19-rag/images/rag-open-book-exam.png | 1.95 MB | 1500x1120 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-1-foundations/module-02-tokenization-subword-models/images/bpe-puzzle-factory.png | 1.94 MB | 1500x1120 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-7-multimodal-applications/module-26-multimodal/images/pipeline-vs-native-multimodal.png | 1.94 MB | 1500x1114 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-3-working-with-llms/module-11-llm-apis/images/structured-output-mold.png | 1.93 MB | 1500x1120 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-3-working-with-llms/module-12-prompt-engineering/images/chain-of-thought-math-test.png | 1.93 MB | 1500x1120 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-9-safety-strategy/module-30-safety-ethics-regulation/images/zoning-code-buildings.png | 1.92 MB | 1500x1120 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-3-working-with-llms/module-11-llm-apis/images/tool-use-swiss-army.png | 1.92 MB | 1500x1120 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-3-working-with-llms/module-11-llm-apis/images/api-hotel-receptionist.png | 1.92 MB | 1500x1120 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-2-understanding-llms/module-06-pretraining-scaling-laws/images/data-curation-gold-panning.png | 1.92 MB | 1500x1120 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-6-agentic-ai/module-21-ai-agents/images/tree-search-forest.png | 1.91 MB | 1500x1120 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-8-evaluation-production/module-29-production-engineering/images/prompt-recipe-binder.png | 1.91 MB | 1500x1120 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-1-foundations/module-00-ml-pytorch-foundations/images/training-loop-racetrack.png | 1.91 MB | 1500x1120 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-8-evaluation-production/module-29-production-engineering/images/missing-steering-wheel.png | 1.89 MB | 1500x1120 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-2-understanding-llms/module-07-modern-llm-landscape/images/frontier-models-race.png | 1.89 MB | 1500x1120 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-8-evaluation-production/module-28-evaluation-observability/images/drift-monitoring-dashboard.png | 1.88 MB | 1500x1095 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-3-working-with-llms/module-12-prompt-engineering/images/meta-prompt-inception.png | 1.87 MB | 1500x1120 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-1-foundations/module-00-ml-pytorch-foundations/images/tensor-building-blocks.png | 1.87 MB | 1500x1120 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-3-working-with-llms/module-12-prompt-engineering/images/prompt-template-madlibs.png | 1.86 MB | 1500x1120 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-8-evaluation-production/module-28-evaluation-observability/images/quality-inspector.png | 1.86 MB | 1500x1120 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-2-understanding-llms/module-06-pretraining-scaling-laws/images/deduplication-clone-detector.png | 1.85 MB | 1500x1120 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-8-evaluation-production/module-29-production-engineering/images/guardrails-highway.png | 1.85 MB | 1500x1120 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-3-working-with-llms/module-11-llm-apis/images/streaming-sse-conveyor.png | 1.84 MB | 1500x1120 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-5-retrieval-conversation/module-18-embeddings-vector-db/images/chunking-baguette.png | 1.83 MB | 1500x1120 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-8-evaluation-production/module-29-production-engineering/images/ab-testing-taste-test.png | 1.82 MB | 1500x1120 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-8-evaluation-production/module-29-production-engineering/images/framework-toolbox.png | 1.82 MB | 1500x1120 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-5-retrieval-conversation/module-18-embeddings-vector-db/images/chunking-sushi-chef.png | 1.81 MB | 1500x1120 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-3-working-with-llms/module-12-prompt-engineering/images/prompt-injection-trojan.png | 1.81 MB | 1500x1120 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-7-multimodal-applications/module-27-llm-applications/images/pair-programming-robot.png | 1.80 MB | 1500x1120 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-5-retrieval-conversation/module-19-rag/images/rag-open-book-student.png | 1.80 MB | 1500x1120 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-8-evaluation-production/module-29-production-engineering/images/autoscaling-accordion.png | 1.80 MB | 1500x1120 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-5-retrieval-conversation/module-18-embeddings-vector-db/images/contrastive-learning-magnets.png | 1.79 MB | 1500x1120 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-5-retrieval-conversation/module-19-rag/images/advanced-rag-treasure-hunt.png | 1.79 MB | 1500x1095 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-1-foundations/module-00-ml-pytorch-foundations/images/ppo-careful-chef.png | 1.78 MB | 1500x1120 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-6-agentic-ai/module-21-ai-agents/images/tool-use-vending-machine.png | 1.77 MB | 1500x1120 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-2-understanding-llms/module-06-pretraining-scaling-laws/images/bert-reads-both-ways.png | 1.76 MB | 1500x1120 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-2-understanding-llms/module-06-pretraining-scaling-laws/images/emergent-abilities-butterfly.png | 1.75 MB | 1500x1120 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-3-working-with-llms/module-12-prompt-engineering/images/zero-vs-few-shot-chef.png | 1.75 MB | 1500x1120 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-8-evaluation-production/module-29-production-engineering/images/deployment-rocket-launch.png | 1.74 MB | 1500x1120 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-2-understanding-llms/module-06-pretraining-scaling-laws/images/icl-open-book-exam.png | 1.74 MB | 1500x1120 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-9-safety-strategy/module-30-safety-ethics-regulation/images/model-card-nutrition-label.png | 1.74 MB | 1500x1120 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-1-foundations/module-00-ml-pytorch-foundations/images/rl-dog-training.png | 1.74 MB | 1500x1120 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-5-retrieval-conversation/module-18-embeddings-vector-db/images/colpali-xray-vision.png | 1.73 MB | 1500x1120 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-1-foundations/module-00-ml-pytorch-foundations/images/backprop-assembly-line.png | 1.73 MB | 1500x1120 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-3-working-with-llms/module-11-llm-apis/images/multimodal-senses-robot.png | 1.73 MB | 1500x1139 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-9-safety-strategy/module-30-safety-ethics-regulation/images/trojan-horse-injection.png | 1.72 MB | 1500x1120 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-5-retrieval-conversation/module-19-rag/images/graphrag-detective-board.png | 1.72 MB | 1500x1120 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-9-safety-strategy/module-30-safety-ethics-regulation/images/confident-witness.png | 1.72 MB | 1500x1120 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-5-retrieval-conversation/module-19-rag/images/reranking-judges-panel.png | 1.72 MB | 1500x1120 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-2-understanding-llms/module-09-inference-optimization/images/paged-attention-memory.png | 1.71 MB | 1500x1120 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-2-understanding-llms/module-08-reasoning-test-time-compute/images/ch08-reasoning-model-landscape.png | 1.71 MB | 1024x1024 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-2-understanding-llms/module-06-pretraining-scaling-laws/images/span-corruption-cheese.png | 1.70 MB | 1500x1120 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-8-evaluation-production/module-28-evaluation-observability/images/llm-judge-courtroom.png | 1.70 MB | 1500x1109 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-1-foundations/module-02-tokenization-subword-models/images/multilingual-fertility-buffet.png | 1.70 MB | 1500x1120 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-5-retrieval-conversation/module-18-embeddings-vector-db/images/matryoshka-embeddings-nesting.png | 1.69 MB | 1500x1090 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-1-foundations/module-01-foundations-nlp-text-representation/images/language-is-hard-robot.png | 1.69 MB | 1500x1079 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| appendices/appendix-m-inference-serving/images/chapter-opener.png | 1.69 MB | 1024x1024 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-3-working-with-llms/module-12-prompt-engineering/images/self-consistency-jury.png | 1.68 MB | 1500x1120 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-5-retrieval-conversation/module-19-rag/images/hyde-crystal-ball.png | 1.68 MB | 1500x1110 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-2-understanding-llms/module-06-pretraining-scaling-laws/images/learning-rate-warmup.png | 1.68 MB | 1500x1120 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-3-working-with-llms/module-13-hybrid-ml-llm/images/latency-cost-race.png | 1.68 MB | 1500x1120 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-2-understanding-llms/module-06-pretraining-scaling-laws/images/mesa-optimization-russian-doll.png | 1.68 MB | 1500x1120 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-1-foundations/module-02-tokenization-subword-models/images/tokenizer-sushi-chef.png | 1.68 MB | 1500x1120 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-2-understanding-llms/module-06-pretraining-scaling-laws/images/gpt-scaling-rocket.png | 1.67 MB | 1500x1120 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-6-agentic-ai/module-21-ai-agents/images/agent-loop-detective.png | 1.66 MB | 1500x837 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-9-safety-strategy/module-30-safety-ethics-regulation/images/bias-sediment-layers.png | 1.65 MB | 1500x1120 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-3-working-with-llms/module-11-llm-apis/images/retry-backoff-trampoline.png | 1.65 MB | 1500x1120 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-5-retrieval-conversation/module-18-embeddings-vector-db/images/metadata-filtering-bouncer.png | 1.64 MB | 1500x1002 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-2-understanding-llms/module-06-pretraining-scaling-laws/images/clm-vs-mlm-puzzle.png | 1.62 MB | 1500x1120 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-2-understanding-llms/module-06-pretraining-scaling-laws/images/mixed-precision-suitcase.png | 1.61 MB | 1500x1120 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| appendices/appendix-f-hardware-compute/images/gpu-datacenter-crosssection.png | 1.60 MB | 1500x837 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-6-agentic-ai/module-24-specialized-agents/images/ch25-research-agent-detective.png | 1.59 MB | 1024x1024 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-4-training-adapting/module-14-synthetic-data/images/deduplication-twins.png | 1.59 MB | 1500x837 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| appendices/glossary/images/glossary-library.png | 1.58 MB | 1500x837 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-5-retrieval-conversation/module-20-conversational-ai/images/memory-management-containers.png | 1.56 MB | 1500x1024 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-4-training-adapting/module-14-synthetic-data/images/rejection-sampling-panning.png | 1.55 MB | 1500x837 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-6-agentic-ai/module-24-specialized-agents/images/ch25-swebench-obstacle-course.png | 1.55 MB | 1024x1024 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-1-foundations/module-02-tokenization-subword-models/images/bottomup-vs-topdown-tokenization.png | 1.54 MB | 1500x1120 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-3-working-with-llms/module-13-hybrid-ml-llm/images/ml-vs-llm-toolbox.png | 1.53 MB | 1500x928 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-1-foundations/module-02-tokenization-subword-models/images/tokenization-artifacts-telephone.png | 1.53 MB | 1500x1120 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-5-retrieval-conversation/module-18-embeddings-vector-db/images/parent-child-retrieval-telescope.png | 1.52 MB | 1500x960 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| appendices/appendix-i-datasets-benchmarks/images/benchmark-olympics.png | 1.52 MB | 1500x837 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-2-understanding-llms/module-10-interpretability/images/superposition-coat-rack.png | 1.51 MB | 1500x1004 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-6-agentic-ai/module-21-ai-agents/images/four-patterns-toolbelt.png | 1.50 MB | 1500x837 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-3-working-with-llms/module-11-llm-apis/images/circuit-breaker-pattern.png | 1.50 MB | 1500x1120 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-6-agentic-ai/module-21-ai-agents/images/function-calling-waiter.png | 1.50 MB | 1500x837 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-4-training-adapting/module-14-synthetic-data/images/seed-data-garden.png | 1.48 MB | 1500x837 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-11-idea-to-product/module-35-shipping-scaling/images/post-launch-monitoring.png | 1.48 MB | 1024x1024 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-4-training-adapting/module-14-synthetic-data/images/active-learning-fishing.png | 1.48 MB | 1500x837 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| appendices/appendix-b-ml-essentials/images/chapter-opener.png | 1.47 MB | 1500x837 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-6-agentic-ai/module-21-ai-agents/images/plan-execute-general.png | 1.47 MB | 1500x837 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-6-agentic-ai/module-24-specialized-agents/images/ch25-computer-use-desktop.png | 1.47 MB | 1024x1024 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-5-retrieval-conversation/module-19-rag/images/lost-in-middle-sandwich.png | 1.46 MB | 1500x1120 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-4-training-adapting/module-17-alignment-rlhf-dpo/images/dpo-vs-rlhf-comparison.png | 1.46 MB | 1500x1137 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| appendices/appendix-c-python-for-llm/images/chapter-opener.png | 1.46 MB | 1500x837 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-6-agentic-ai/module-25-agent-safety-production/images/ch26-observability-dashboard.png | 1.45 MB | 1024x1024 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-6-agentic-ai/module-21-ai-agents/images/thinking-budget-dial.png | 1.45 MB | 1500x837 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-10-frontiers/module-33-emerging-architectures/images/ch34-memory-filing-cabinet.png | 1.45 MB | 1024x1024 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-4-training-adapting/module-14-synthetic-data/images/llm-assembly-line.png | 1.44 MB | 1500x837 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-6-agentic-ai/module-21-ai-agents/images/hybrid-agent-relay.png | 1.43 MB | 1500x837 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| appendices/appendix-g-model-cards/images/model-card-presentation.png | 1.43 MB | 1500x837 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-4-training-adapting/module-14-synthetic-data/images/llm-actor-stage.png | 1.42 MB | 1500x837 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-11-idea-to-product/module-34-idea-to-product/images/case-studies-roles.png | 1.40 MB | 1024x1024 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| appendices/appendix-e-git-collaboration/images/chapter-opener.png | 1.40 MB | 1500x837 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-4-training-adapting/module-14-synthetic-data/images/weak-supervision-jury.png | 1.39 MB | 1500x837 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-6-agentic-ai/module-21-ai-agents/images/mcp-universal-adapter.png | 1.39 MB | 1500x837 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-4-training-adapting/module-14-synthetic-data/images/prompt-template-cookie-cutter.png | 1.39 MB | 1500x837 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-6-agentic-ai/module-21-ai-agents/images/self-debugging-loop.png | 1.39 MB | 1500x837 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-2-understanding-llms/module-08-reasoning-test-time-compute/images/ch08-proof-assistant-handshake.png | 1.39 MB | 1024x1024 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| appendices/appendix-k-langchain/images/chapter-opener.png | 1.38 MB | 1024x1024 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-6-agentic-ai/module-21-ai-agents/images/code-sandbox-playground.png | 1.38 MB | 1500x837 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-4-training-adapting/module-14-synthetic-data/images/red-team-boxing-ring.png | 1.37 MB | 1500x837 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-5-retrieval-conversation/module-18-embeddings-vector-db/images/late-interaction-judges.png | 1.37 MB | 1500x978 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-6-agentic-ai/module-23-multi-agent-systems/images/ch24-opener-agent-orchestra.png | 1.36 MB | 1024x1024 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-11-idea-to-product/module-35-shipping-scaling/images/launch-economics.png | 1.35 MB | 1024x1024 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| appendices/appendix-d-environment-setup/images/chapter-opener.png | 1.35 MB | 1500x837 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-6-agentic-ai/module-21-ai-agents/images/tree-search-maze.png | 1.34 MB | 1500x837 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| appendices/appendix-h-prompt-templates/images/prompt-recipe-kitchen.png | 1.34 MB | 1500x837 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| appendices/appendix-a-mathematical-foundations/images/chapter-opener.png | 1.33 MB | 1500x837 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-11-idea-to-product/module-35-shipping-scaling/images/lock-in-portability.png | 1.33 MB | 1024x1024 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-4-training-adapting/module-14-synthetic-data/images/reasoning-chain-dominos.png | 1.32 MB | 1500x837 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| appendices/appendix-j-huggingface-ecosystem/images/chapter-opener.png | 1.31 MB | 934x921 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-4-training-adapting/module-14-synthetic-data/images/data-quality-inspector.png | 1.31 MB | 1500x837 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-2-understanding-llms/module-09-inference-optimization/images/quantization-diet.png | 1.29 MB | 1160x896 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-11-idea-to-product/module-34-idea-to-product/images/ai-product-differences.png | 1.29 MB | 1024x1024 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-2-understanding-llms/module-07-modern-llm-landscape/images/open-weight-market.png | 1.28 MB | 1200x896 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-1-foundations/module-01-foundations-nlp-text-representation/images/analogy-gps-words.png | 1.28 MB | 1319x745 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-6-agentic-ai/module-25-agent-safety-production/images/ch26-supply-chain-security.png | 1.27 MB | 1024x1024 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-11-idea-to-product/module-35-shipping-scaling/images/cost-engine-levers.png | 1.26 MB | 1024x1024 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-1-foundations/module-04-transformer-architecture/images/gpu-city-memory-hierarchy.png | 1.25 MB | 1200x896 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-2-understanding-llms/module-09-inference-optimization/images/kv-cache-filing-cabinet.png | 1.24 MB | 1200x896 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| appendices/appendix-n-distributed-ml/images/chapter-opener.png | 1.24 MB | 1001x918 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-4-training-adapting/module-14-synthetic-data/images/data-diversity-spectrum.png | 1.23 MB | 1500x837 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| appendices/appendix-p-tooling-ecosystem/images/chapter-opener.png | 1.23 MB | 897x892 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-6-agentic-ai/module-22-tool-use-protocols/images/ch23-opener-tool-belt.png | 1.22 MB | 1024x1024 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-6-agentic-ai/module-24-specialized-agents/images/ch25-code-agent-debug-loop.png | 1.21 MB | 1024x1024 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-10-frontiers/module-33-emerging-architectures/images/ch34-emergence-mirage.png | 1.20 MB | 1024x1024 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-6-agentic-ai/module-22-tool-use-protocols/images/ch23-agentic-rag-librarian.png | 1.20 MB | 934x926 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-11-idea-to-product/module-34-idea-to-product/images/risk-feasibility.png | 1.18 MB | 1024x1024 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-4-training-adapting/module-16-peft/images/chapter-opener.png | 1.17 MB | 1600x873 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-1-foundations/module-01-foundations-nlp-text-representation/images/evolution-staircase.png | 1.15 MB | 1348x768 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| appendices/appendix-o-docker-containers/images/chapter-opener.png | 1.15 MB | 923x856 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-4-training-adapting/module-14-synthetic-data/images/chapter-opener.png | 1.14 MB | 1600x873 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-6-agentic-ai/module-24-specialized-agents/images/ch25-opener-specialist-robots.png | 1.13 MB | 1024x1024 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-6-agentic-ai/module-25-agent-safety-production/images/ch26-sandbox-fishbowl.png | 1.13 MB | 1024x1024 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-1-foundations/module-01-foundations-nlp-text-representation/images/analogy-filing-cabinet.png | 1.12 MB | 1334x768 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-6-agentic-ai/module-24-specialized-agents/images/ch25-browser-agent-navigation.png | 1.12 MB | 1024x1024 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-4-training-adapting/module-15-fine-tuning-fundamentals/images/embedding-finetuning-translator.png | 1.10 MB | 1147x803 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-11-idea-to-product/module-35-shipping-scaling/images/copilots-every-stage.png | 1.10 MB | 1024x1024 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-10-frontiers/module-33-emerging-architectures/images/ch34-opener-frontier-telescope.png | 1.10 MB | 905x903 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-9-safety-strategy/module-31-strategy-product-roi/images/gpu-selection-hardware-store.png | 1.10 MB | 1200x869 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-11-idea-to-product/module-34-idea-to-product/images/model-role-spectrum.png | 1.09 MB | 1024x1024 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-11-idea-to-product/module-34-idea-to-product/images/feasibility-funnel.png | 1.09 MB | 979x994 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-1-foundations/module-03-sequence-models-attention/images/multi-head-attention-dragon.png | 1.08 MB | 1200x896 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-10-frontiers/module-33-emerging-architectures/images/ch34-alternative-architectures-zoo.png | 1.07 MB | 1000x972 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-1-foundations/module-04-transformer-architecture/images/build-transformer-workshop.png | 1.07 MB | 1200x896 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-5-retrieval-conversation/module-20-conversational-ai/images/persona-dressing-room.png | 1.07 MB | 1200x896 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-6-agentic-ai/module-22-tool-use-protocols/images/ch23-a2a-agents-talking.png | 1.06 MB | 1024x1024 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-4-training-adapting/module-14-synthetic-data/images/model-collapse-spiral.png | 1.05 MB | 1048x896 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-1-foundations/module-01-foundations-nlp-text-representation/images/analogy-polysemy-bank.png | 1.05 MB | 1376x740 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-6-agentic-ai/module-22-tool-use-protocols/images/ch23-mcp-usb-analogy.png | 1.03 MB | 1024x1024 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-3-working-with-llms/module-12-prompt-engineering/images/reflection-loop.png | 1.01 MB | 1108x814 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-1-foundations/module-05-decoding-text-generation/images/greedy-vs-beam-search-hiker.png | 1.01 MB | 1200x896 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| part-2-understanding-llms/module-08-reasoning-test-time-compute/images/test-time-compute-chess.png | 1.01 MB | 1200x896 | raster-bytes>1.00 MB | re-encode (pngquant / cwebp) |
| downloads/cover.jpg | 722.7 KB | 1600x2560 | raster-edge>2000px | resize to <= 2000px on longest edge |
| part-2-understanding-llms/module-06-pretraining-scaling-laws/images/fig-6.5.1-sgd-vs-adam.png | 493.3 KB | 4510x1659 | raster-edge>2000px | resize to <= 2000px on longest edge |
| part-1-foundations/module-03-sequence-models-attention/images/fig-3.2.5-bahdanau-attention.png | 343.2 KB | 4626x2115 | raster-edge>2000px | resize to <= 2000px on longest edge |
| part-2-understanding-llms/module-06-pretraining-scaling-laws/images/fig-6.4.3-curation-funnel.png | 307.4 KB | 4261x1816 | raster-edge>2000px | resize to <= 2000px on longest edge |
| part-4-training-adapting/module-17-alignment-rlhf-dpo/images/huyenchip-rlhf-pipeline.png | 285.1 KB | 2498x1316 | raster-edge>2000px | resize to <= 2000px on longest edge |
| part-2-understanding-llms/module-06-pretraining-scaling-laws/images/fig-6.3.3-chinchilla-vs-kaplan.png | 278.5 KB | 2764x1796 | raster-edge>2000px | resize to <= 2000px on longest edge |
| part-8-evaluation-production/_concept-figs/fig-W19-F04-goodhart-proxy-failures.png | 274.9 KB | 4548x1134 | raster-edge>2000px | resize to <= 2000px on longest edge |
| part-6-agentic-ai/module-25-agent-safety-production/images/fig-25.9.1-agent-eval-framework.png | 249.2 KB | 4875x2226 | raster-edge>2000px | resize to <= 2000px on longest edge |
| part-5-retrieval-conversation/module-19-rag/images/fig-19.3.2-knowledge-graph-example.png | 245.4 KB | 2232x2226 | raster-edge>2000px | resize to <= 2000px on longest edge |
| part-2-understanding-llms/module-06-pretraining-scaling-laws/images/production-training-architecture.png | 244.3 KB | 4218x3570 | raster-edge>2000px | resize to <= 2000px on longest edge |
| part-4-training-adapting/module-14-synthetic-data/images/fig-14.2.4-evol-instruct-operators.png | 242.6 KB | 5835x1347 | raster-edge>2000px | resize to <= 2000px on longest edge |
| part-2-understanding-llms/module-06-pretraining-scaling-laws/images/fig-6.5.2-lr-schedules.png | 239.8 KB | 2682x1560 | raster-edge>2000px | resize to <= 2000px on longest edge |
| part-10-frontiers/module-33-emerging-architectures/images/fig-33.3.3-attention-variants-taxonomy.png | 234.2 KB | 6456x1059 | raster-edge>2000px | resize to <= 2000px on longest edge |
| part-1-foundations/module-03-sequence-models-attention/images/lstm-cell-colah2015.png | 224.3 KB | 2233x839 | raster-edge>2000px | resize to <= 2000px on longest edge |
| part-6-agentic-ai/module-22-tool-use-protocols/images/fig-22.1.2-function-calling-loop.png | 223.0 KB | 2415x2667 | raster-edge>2000px | resize to <= 2000px on longest edge |
| part-10-frontiers/module-33-emerging-architectures/images/fig-33.9.1-tool-orchestration-economy.png | 218.1 KB | 4053x2547 | raster-edge>2000px | resize to <= 2000px on longest edge |
| part-4-training-adapting/module-14-synthetic-data/images/fig-14.1.2-annotation-cost.png | 215.3 KB | 2988x1612 | raster-edge>2000px | resize to <= 2000px on longest edge |
| part-3-working-with-llms/module-13-hybrid-ml-llm/images/figure-12.4.2.png | 214.1 KB | 2563x1819 | raster-edge>2000px | resize to <= 2000px on longest edge |
| part-1-foundations/module-03-sequence-models-attention/images/fig-3.1.7-rnn-unrolled.png | 213.8 KB | 4722x1350 | raster-edge>2000px | resize to <= 2000px on longest edge |
| part-2-understanding-llms/module-07-modern-llm-landscape/images/fig-7.4.3-multilingual-gap.png | 210.3 KB | 2809x1675 | raster-edge>2000px | resize to <= 2000px on longest edge |
| part-2-understanding-llms/module-06-pretraining-scaling-laws/images/fig-6.3.2-power-law.png | 206.0 KB | 3841x1476 | raster-edge>2000px | resize to <= 2000px on longest edge |
| part-1-foundations/module-00-ml-pytorch-foundations/images/fig-0.3.5-training-loop.png | 198.6 KB | 2800x1616 | raster-edge>2000px | resize to <= 2000px on longest edge |
| part-8-evaluation-production/_concept-figs/fig-W19-F14-eval-taxonomy-with-failures.png | 172.4 KB | 4674x1236 | raster-edge>2000px | resize to <= 2000px on longest edge |
| part-6-agentic-ai/module-25-agent-safety-production/images/fig-25.3.2-agent-observability-stack.png | 172.1 KB | 2244x2241 | raster-edge>2000px | resize to <= 2000px on longest edge |
| part-1-foundations/module-00-ml-pytorch-foundations/images/figure-0.1.4.png | 170.2 KB | 2423x1510 | raster-edge>2000px | resize to <= 2000px on longest edge |
| part-6-agentic-ai/module-23-multi-agent-systems/images/fig-23.2.1-multi-agent-topologies.png | 169.3 KB | 5571x1560 | raster-edge>2000px | resize to <= 2000px on longest edge |
| part-1-foundations/module-05-decoding-text-generation/images/figure-5.2.2.png | 169.2 KB | 2534x1583 | raster-edge>2000px | resize to <= 2000px on longest edge |
| part-1-foundations/module-05-decoding-text-generation/images/fig-5.2.4-temperature.png | 169.2 KB | 3252x1527 | raster-edge>2000px | resize to <= 2000px on longest edge |
| part-9-safety-strategy/module-31-strategy-product-roi/images/fig-31.1.1-ai-readiness-bars.png | 162.6 KB | 3247x1560 | raster-edge>2000px | resize to <= 2000px on longest edge |
| part-4-training-adapting/module-15-fine-tuning-fundamentals/images/figure-14.7.1.png | 162.0 KB | 2542x1675 | raster-edge>2000px | resize to <= 2000px on longest edge |
| part-2-understanding-llms/module-06-pretraining-scaling-laws/images/fig-6.5.1-sgd-vs-adam.svg | 156.4 KB | (svg) | svg-bytes>100.0 KB | minify / simplify paths (svgo) |
| part-10-frontiers/module-33-emerging-architectures/images/fig-33.3.2-mamba-vs-transformer.png | 153.0 KB | 6288x1092 | raster-edge>2000px | resize to <= 2000px on longest edge |
| part-3-working-with-llms/_concept-figs/fig-W19-F01-four-tier-intervention.png | 151.9 KB | 1758x2055 | raster-edge>2000px | resize to <= 2000px on longest edge |
| part-11-idea-to-product/module-35-shipping-scaling/images/fig-35.4.6-continuous-steering-loop.png | 150.1 KB | 6093x852 | raster-edge>2000px | resize to <= 2000px on longest edge |
| part-2-understanding-llms/_concept-figs/fig-W19-F08-moe-routing-modularity.png | 147.4 KB | 2631x1728 | raster-edge>2000px | resize to <= 2000px on longest edge |
| part-11-idea-to-product/module-35-shipping-scaling/images/fig-35.3.4-portable-monogamy-architecture.png | 143.1 KB | 2742x1752 | raster-edge>2000px | resize to <= 2000px on longest edge |
| part-5-retrieval-conversation/module-19-rag/images/rag-pipeline-nvidia.png | 141.1 KB | 2030x909 | raster-edge>2000px | resize to <= 2000px on longest edge |
| part-2-understanding-llms/module-06-pretraining-scaling-laws/images/figure-6.3.6.png | 139.0 KB | 3527x1412 | raster-edge>2000px | resize to <= 2000px on longest edge |
| part-10-frontiers/module-33-emerging-architectures/images/fig-33.4.2-world-model-architecture.png | 135.8 KB | 4125x1299 | raster-edge>2000px | resize to <= 2000px on longest edge |
| part-1-foundations/_concept-figs/fig-W19-F07-residual-stream.png | 135.6 KB | 5598x1107 | raster-edge>2000px | resize to <= 2000px on longest edge |
| part-1-foundations/module-00-ml-pytorch-foundations/images/figure-0.1.2.png | 134.6 KB | 2457x1373 | raster-edge>2000px | resize to <= 2000px on longest edge |
| part-2-understanding-llms/module-06-pretraining-scaling-laws/images/figure-6.5.3.png | 131.8 KB | 2600x1510 | raster-edge>2000px | resize to <= 2000px on longest edge |
| part-10-frontiers/_concept-figs/fig-W19-F11-induction-heads-circuit.png | 129.4 KB | 3267x996 | raster-edge>2000px | resize to <= 2000px on longest edge |
| part-2-understanding-llms/module-06-pretraining-scaling-laws/images/fig-6.4.3-curation-funnel.svg | 127.7 KB | (svg) | svg-bytes>100.0 KB | minify / simplify paths (svgo) |
| part-4-training-adapting/module-15-fine-tuning-fundamentals/images/figure-14.1.3.png | 125.0 KB | 2425x1510 | raster-edge>2000px | resize to <= 2000px on longest edge |
| part-2-understanding-llms/_concept-figs/fig-W19-F06-generator-verifier-asymmetry.png | 118.5 KB | 3723x390 | raster-edge>2000px | resize to <= 2000px on longest edge |
| part-7-multimodal-applications/module-26-multimodal/images/fig-26.5.1-vision-language-action-pipeline.png | 114.0 KB | 4050x768 | raster-edge>2000px | resize to <= 2000px on longest edge |
| part-2-understanding-llms/module-06-pretraining-scaling-laws/images/fig-6.3.3-chinchilla-vs-kaplan.svg | 113.9 KB | (svg) | svg-bytes>100.0 KB | minify / simplify paths (svgo) |
| part-9-safety-strategy/module-31-strategy-product-roi/images/figure-30.5.1.png | 113.1 KB | 2555x1586 | raster-edge>2000px | resize to <= 2000px on longest edge |
| part-1-foundations/module-03-sequence-models-attention/images/d2l-bahdanau-attention.svg | 111.6 KB | (svg) | svg-bytes>100.0 KB | minify / simplify paths (svgo) |
| part-1-foundations/module-05-decoding-text-generation/images/fig-5.2.4-temperature.svg | 108.9 KB | (svg) | svg-bytes>100.0 KB | minify / simplify paths (svgo) |
| part-2-understanding-llms/module-07-modern-llm-landscape/images/reasoning-token-flow.png | 107.5 KB | 2445x1122 | raster-edge>2000px | resize to <= 2000px on longest edge |
| part-4-training-adapting/module-14-synthetic-data/images/fig-14.1.2-annotation-cost.svg | 107.3 KB | (svg) | svg-bytes>100.0 KB | minify / simplify paths (svgo) |
| part-1-foundations/module-04-transformer-architecture/images/fig-4.2.2-decoder-only.png | 106.8 KB | 3288x2442 | raster-edge>2000px | resize to <= 2000px on longest edge |
| part-2-understanding-llms/_concept-figs/fig-W19-F10-scaling-laws-resolution.png | 106.8 KB | 2100x1500 | raster-edge>2000px | resize to <= 2000px on longest edge |
| part-10-frontiers/_concept-figs/fig-W19-F05-alignment-verification-gap.png | 101.3 KB | 2100x1500 | raster-edge>2000px | resize to <= 2000px on longest edge |
| part-2-understanding-llms/module-06-pretraining-scaling-laws/images/fig-6.3.2-power-law.svg | 100.5 KB | (svg) | svg-bytes>100.0 KB | minify / simplify paths (svgo) |
| part-11-idea-to-product/module-35-shipping-scaling/images/fig-35.1.1-token-to-dollar-pipeline.png | 97.9 KB | 5427x432 | raster-edge>2000px | resize to <= 2000px on longest edge |
| part-10-frontiers/_concept-figs/fig-W19-F15-capability-interpretability-gap.png | 97.6 KB | 2100x1500 | raster-edge>2000px | resize to <= 2000px on longest edge |
| part-7-multimodal-applications/module-26-multimodal/images/fig-26.1.7-ddpm-forward-reverse.png | 95.8 KB | 6210x474 | raster-edge>2000px | resize to <= 2000px on longest edge |
| part-1-foundations/module-01-foundations-nlp-text-representation/images/fig-1.3.2-skipgram-network.png | 90.9 KB | 3483x537 | raster-edge>2000px | resize to <= 2000px on longest edge |
| part-2-understanding-llms/module-08-reasoning-test-time-compute/images/fig-8.1.2-performance-as-a-function-of-total-compute-under-three-scali.png | 73.1 KB | 2520x918 | raster-edge>2000px | resize to <= 2000px on longest edge |
| part-2-understanding-llms/module-08-reasoning-test-time-compute/images/fig-8.5.1-compute-optimal-inference-frontier-on-easy-tasks-green-l.png | 69.4 KB | 2463x954 | raster-edge>2000px | resize to <= 2000px on longest edge |
| part-1-foundations/module-01-foundations-nlp-text-representation/images/fig-1.3.6-fasttext-subword-decomposition-the-word-running-is-split.png | 67.6 KB | 3051x2229 | raster-edge>2000px | resize to <= 2000px on longest edge |

## 4. Embedded-raster SVGs

None found.

## 5. Recommended fix priority

1. **Embedded-raster SVGs first**: these are 'silent' bloat. extract the base64 payload to an external .png/.webp and reference it. Currently 0 SVG(s) contain a base64 data URI.
2. **Re-encode the largest rasters** (start with `part-8-evaluation-production/module-29-production-engineering/images/restaurant-kitchen-architecture.png` at 2.34 MB). Use `pngquant --quality=70-90 in.png` or convert to `.webp` (`cwebp -q 80`); aim to halve the bytes per image.
3. **Downscale anything wider/taller than 2000px** before re-encoding; Kindle/EPUB readers cap effective resolution near 1200-1600px so larger images just waste bytes.
4. **Minify oversized SVGs** (start with `part-2-understanding-llms/module-06-pretraining-scaling-laws/images/fig-6.5.1-sgd-vs-adam.svg` at 156.4 KB). Run through `svgo --multipass`, then re-check for any leftover embedded raster.
5. **Tackle the worst column-imbalance table next**: `part-11-idea-to-product/module-35-shipping-scaling/section-35.1.html:293` (column #2, ratio 12.5x). Options: shorten the cell, wrap it in `<div style="max-width: 36ch">`, or split the content into a follow-up paragraph below the table.
6. **Adopt a CSS guardrail** for newly-authored tables: add a sensible `max-width` (e.g. `36ch`-`60ch`) on `<td>`/`<th>` that hold long prose, so future content-aware layouts don't collapse the other columns.
7. **Lock the budget**: keep the per-image ceiling at 1 MB raster / 100 KB SVG, and re-run this audit in CI so regressions surface before the EPUB build trips the ~50 MB KDP cap.

_Report generated by `scripts/_audit_wide_tables_image_sizes.py`._
