# Table-class consistency audit

Total `<table>` elements scanned: **398**

## Class distribution

| Class | Count |
|---|---|
| `complex-table` | 223 |
| `(no class)` | 147 |
| `data-table` | 12 |
| `psk-table` | 11 |
| `comparison-table` | 5 |

## Caption mechanism distribution

| Mechanism | Count |
|---|---|
| `none` | 366 |
| `<figcaption>` | 19 |
| `<caption>` | 12 |
| `p.table-caption` | 1 |

- Tables with **no `<caption>` element**: 386
- Tables with **no `<thead>`**: 195
- Tables with **explicit `border=` attribute**: 0
- Tables with **inline `style=` attribute**: 2
- Tables wrapped in `<center>`: 0
- Tables **not** wrapped in `.table-container`: 390

## class=`data-table` instances (non-standard grid)  (12)

| File | Line | Cols | thead | caption-mech | caption (truncated) |
|---|---:|---:|:-:|---|---|
| `part-1-foundations/module-01-foundations-nlp-text-representation/section-1.2.html` | 244 | 9 | Y | `<caption>` | : A Bag-of-Words count matrix. Each row is a document, each column is… |
| `part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.8.html` | 75 | 8 | Y | `<caption>` | Table 6.8.1 : Recommended Megatron parallelism configurations for H10… |
| `part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.8.html` | 189 | 4 | Y | `<caption>` | Table 6.8.2 : Attention kernel selection guide |
| `part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.8.html` | 278 | 4 | Y | `<caption>` | Table 6.8.3 : Failure types and recovery strategies in LLM training |
| `part-7-multimodal-applications/module-27-llm-applications/section-27.2.html` | 536 | 3 | Y | `<caption>` | Figure 27.2.2 (Table): Regulatory landscape for financial LLM applica… |
| `part-8-evaluation-production/module-28-evaluation-observability/section-28.12.html` | 62 | 4 | Y | `<caption>` | Table 27.14.1 : MLPerf Inference scenarios and their LLM relevance |
| `part-8-evaluation-production/module-28-evaluation-observability/section-28.12.html` | 338 | 5 | Y | `<caption>` | Table 27.14.3 : KV cache storage tiers and their characteristics |
| `part-8-evaluation-production/module-29-production-engineering/section-29.7.html` | 75 | 4 | Y | `none` | _(no caption)_ |
| `part-8-evaluation-production/module-29-production-engineering/section-29.7.html` | 166 | 5 | Y | `none` | _(no caption)_ |
| `part-8-evaluation-production/module-29-production-engineering/section-29.9.html` | 394 | 4 | Y | `<caption>` | Table 28.9.1 : H100 MIG partition profiles for LLM serving |
| `part-8-evaluation-production/module-29-production-engineering/section-29.9.html` | 456 | 4 | Y | `<caption>` | Table 28.9.2 : Autoscaling metrics for LLM serving |
| `part-9-safety-strategy/module-31-strategy-product-roi/section-31.7.html` | 406 | 3 | Y | `<caption>` | Table 31.7.1: Build vs. buy breakeven analysis. API-based Claude Sonn… |

## class=`comparison-table` instances (gradient title bar; keep as-is)  (5)

| File | Line | Cols | thead | caption-mech | caption (truncated) |
|---|---:|---:|:-:|---|---|
| `part-10-frontiers/module-33-emerging-architectures/section-33.3.html` | 499 | 5 | Y | `none` | _(no caption)_ |
| `part-10-frontiers/module-33-emerging-architectures/section-33.4.html` | 226 | 5 | Y | `none` | _(no caption)_ |
| `part-4-training-adapting/module-16-peft/section-16.4.html` | 357 | 6 | Y | `none` | _(no caption)_ |
| `part-6-agentic-ai/module-24-specialized-agents/section-24.4.html` | 287 | 6 | Y | `none` | _(no caption)_ |
| `part-9-safety-strategy/module-30-safety-ethics-regulation/section-30.9.html` | 310 | 4 | Y | `none` | _(no caption)_ |

## class=`psk-table` instances (appendix problem-solution; keep as-is)  (11)

| File | Line | Cols | thead | caption-mech | caption (truncated) |
|---|---:|---:|:-:|---|---|
| `appendices/appendix-t-problem-solution-key/index.html` | 104 | 4 | Y | `none` | _(no caption)_ |
| `appendices/appendix-t-problem-solution-key/index.html` | 164 | 4 | Y | `none` | _(no caption)_ |
| `appendices/appendix-t-problem-solution-key/index.html` | 222 | 4 | Y | `none` | _(no caption)_ |
| `appendices/appendix-t-problem-solution-key/index.html` | 300 | 4 | Y | `none` | _(no caption)_ |
| `appendices/appendix-t-problem-solution-key/index.html` | 360 | 4 | Y | `none` | _(no caption)_ |
| `appendices/appendix-t-problem-solution-key/index.html` | 409 | 4 | Y | `none` | _(no caption)_ |
| `appendices/appendix-t-problem-solution-key/index.html` | 477 | 4 | Y | `none` | _(no caption)_ |
| `appendices/appendix-t-problem-solution-key/index.html` | 564 | 4 | Y | `none` | _(no caption)_ |
| `appendices/appendix-t-problem-solution-key/index.html` | 631 | 4 | Y | `none` | _(no caption)_ |
| `appendices/appendix-t-problem-solution-key/index.html` | 691 | 4 | Y | `none` | _(no caption)_ |
| `appendices/appendix-t-problem-solution-key/index.html` | 775 | 4 | Y | `none` | _(no caption)_ |

## Sample: first 10 `class=complex-table` (the standard)  (10)

| File | Line | Cols | thead | caption-mech | caption (truncated) |
|---|---:|---:|:-:|---|---|
| `appendices/appendix-a-mathematical-foundations/section-a.3.html` | 91 | 4 | n | `none` | _(no caption)_ |
| `appendices/appendix-a-mathematical-foundations/section-a.6.html` | 256 | 4 | n | `none` | _(no caption)_ |
| `appendices/appendix-b-ml-essentials/section-b.1.html` | 39 | 4 | n | `none` | _(no caption)_ |
| `appendices/appendix-b-ml-essentials/section-b.4.html` | 83 | 4 | n | `none` | _(no caption)_ |
| `appendices/appendix-d-environment-setup/section-d.5.html` | 38 | 4 | n | `none` | _(no caption)_ |
| `appendices/appendix-f-hardware-compute/section-f.1.html` | 35 | 8 | Y | `none` | _(no caption)_ |
| `appendices/appendix-f-hardware-compute/section-f.2.html` | 35 | 6 | Y | `none` | _(no caption)_ |
| `appendices/appendix-f-hardware-compute/section-f.3.html` | 37 | 4 | Y | `none` | _(no caption)_ |
| `appendices/appendix-f-hardware-compute/section-f.3.html` | 90 | 4 | Y | `none` | _(no caption)_ |
| `appendices/appendix-f-hardware-compute/section-f.3.html` | 131 | 4 | Y | `none` | _(no caption)_ |

## Sample: first 10 tables with **no class**  (10)

| File | Line | Cols | thead | caption-mech | caption (truncated) |
|---|---:|---:|:-:|---|---|
| `appendices/appendix-a-mathematical-foundations/section-a.2.html` | 79 | 3 | n | `none` | _(no caption)_ |
| `appendices/appendix-b-ml-essentials/section-b.2.html` | 49 | 3 | n | `none` | _(no caption)_ |
| `appendices/appendix-b-ml-essentials/section-b.2.html` | 85 | 3 | n | `none` | _(no caption)_ |
| `appendices/appendix-b-ml-essentials/section-b.3.html` | 40 | 3 | n | `none` | _(no caption)_ |
| `appendices/appendix-b-ml-essentials/section-b.3.html` | 76 | 3 | n | `none` | _(no caption)_ |
| `appendices/appendix-b-ml-essentials/section-b.4.html` | 52 | 3 | n | `none` | _(no caption)_ |
| `appendices/appendix-c-python-for-llm/section-c.1.html` | 179 | 3 | n | `none` | _(no caption)_ |
| `appendices/appendix-d-environment-setup/section-d.1.html` | 37 | 3 | n | `none` | _(no caption)_ |
| `appendices/appendix-e-git-collaboration/section-e.3.html` | 90 | 3 | n | `none` | _(no caption)_ |
| `appendices/appendix-g-model-cards/section-g.1.html` | 41 | 2 | n | `none` | _(no caption)_ |

## Inline `style=` attribute on `<table>`

| File | Line | class | style= |
|---|---:|---|---|
| `part-1-foundations/module-01-foundations-nlp-text-representation/section-1.2.html` | 244 | `data-table` | `text-align: center; font-size: 0.95rem;` |
| `part-7-multimodal-applications/module-27-llm-applications/section-27.2.html` | 536 | `data-table` | `width:100%; max-width:60rem; margin: 1rem auto; border-collapse:collapse;` |

## Caption mechanism by table class

| Class | <caption> | preceding-p | p/div.table-caption | <figcaption> | none |
|---|---:|---:|---:|---:|---:|
| `complex-table` | 0 | 0 | 1 | 0 | 222 |
| `(no class)` | 2 | 0 | 0 | 19 | 126 |
| `data-table` | 10 | 0 | 0 | 0 | 2 |
| `psk-table` | 0 | 0 | 0 | 0 | 11 |
| `comparison-table` | 0 | 0 | 0 | 0 | 5 |
