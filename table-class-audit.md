# Table-class consistency audit

Total `<table>` elements scanned: **452**

## Class distribution

| Class | Count |
|---|---|
| `complex-table` | 266 |
| `(no class)` | 182 |
| `comparison-table` | 4 |

## Caption mechanism distribution

| Mechanism | Count |
|---|---|
| `none` | 337 |
| `<figcaption>` | 76 |
| `<caption>` | 38 |
| `p.table-caption` | 1 |

- Tables with **no `<caption>` element**: 414
- Tables with **no `<thead>`**: 210
- Tables with **explicit `border=` attribute**: 0
- Tables with **inline `style=` attribute**: 1
- Tables wrapped in `<center>`: 0
- Tables **not** wrapped in `.table-container`: 444

## class=`data-table` instances (non-standard grid)  (0)

_None._

## class=`comparison-table` instances (gradient title bar; keep as-is)  (4)

| File | Line | Cols | thead | caption-mech | caption (truncated) |
|---|---:|---:|:-:|---|---|
| `part-11-llm-ethics-trust-governance/module-53-regulation-compliance/section-53.2.html` | 307 | 4 | Y | `<caption>` | Table 53.2.3: The EU AI Act does not exist in isolation. |
| `part-16-llm-agentic-ai-research-frontiers/module-80-frontier-architectures/section-80.3.html` | 492 | 5 | Y | `<caption>` | Table 80.3.2: Comparing architectures requires examining multiple dim… |
| `part-4-training-adaptation/module-17-peft/section-17.4.html` | 354 | 6 | Y | `<caption>` | Table 17.4.1: The table below summarizes the key characteristics of e… |
| `part-6-agentic-ai/module-29-specialized-agents/section-29.4.html` | 284 | 6 | Y | `<caption>` | Table 29.4.1: Comparing agentic coding tools requires evaluating them… |

## class=`psk-table` instances (appendix problem-solution; keep as-is)  (0)

_None._

## Sample: first 10 `class=complex-table` (the standard)  (10)

| File | Line | Cols | thead | caption-mech | caption (truncated) |
|---|---:|---:|:-:|---|---|
| `.book-update/v9-preserved-content/world-models-and-embodied-reasoning-section-41.4.html` | 66 | 5 | Y | `none` | _(no caption)_ |
| `appendices/appendix-a-mathematical-foundations/section-a.3.html` | 88 | 4 | n | `none` | _(no caption)_ |
| `appendices/appendix-a-mathematical-foundations/section-a.6.html` | 253 | 4 | n | `none` | _(no caption)_ |
| `appendices/appendix-b-course-syllabi/index.html` | 38 | 4 | Y | `none` | _(no caption)_ |
| `appendices/appendix-b-course-syllabi/index.html` | 58 | 3 | Y | `none` | _(no caption)_ |
| `appendices/appendix-b-course-syllabi/index.html` | 88 | 3 | Y | `none` | _(no caption)_ |
| `appendices/appendix-b-course-syllabi/index.html` | 118 | 3 | Y | `none` | _(no caption)_ |
| `appendices/appendix-b-course-syllabi/index.html` | 138 | 3 | Y | `none` | _(no caption)_ |
| `appendices/appendix-b-course-syllabi/index.html` | 166 | 3 | Y | `none` | _(no caption)_ |
| `appendices/appendix-b-course-syllabi/index.html` | 181 | 3 | Y | `none` | _(no caption)_ |

## Sample: first 10 tables with **no class**  (10)

| File | Line | Cols | thead | caption-mech | caption (truncated) |
|---|---:|---:|:-:|---|---|
| `appendices/appendix-a-mathematical-foundations/section-a.2.html` | 76 | 3 | n | `none` | _(no caption)_ |
| `capstone/requirements.html` | 324 | 2 | n | `none` | _(no caption)_ |
| `capstone/requirements.html` | 424 | 3 | n | `none` | _(no caption)_ |
| `capstone/requirements.html` | 463 | 3 | n | `none` | _(no caption)_ |
| `capstone/requirements.html` | 510 | 3 | n | `none` | _(no caption)_ |
| `front-matter/fm-who-should-read.html` | 47 | 2 | Y | `none` | _(no caption)_ |
| `part-1-llm-building-blocks/module-00-ml-pytorch-foundations/section-0.1.html` | 140 | 3 | n | `none` | _(no caption)_ |
| `part-1-llm-building-blocks/module-00-ml-pytorch-foundations/section-0.1.html` | 171 | 3 | Y | `none` | _(no caption)_ |
| `part-1-llm-building-blocks/module-00-ml-pytorch-foundations/section-0.2.html` | 214 | 3 | n | `none` | _(no caption)_ |
| `part-1-llm-building-blocks/module-00-ml-pytorch-foundations/section-0.3.html` | 532 | 3 | Y | `none` | _(no caption)_ |

## Inline `style=` attribute on `<table>`

| File | Line | class | style= |
|---|---:|---|---|
| `part-9-llm-evaluation-observability/module-44-online-eval-observability/section-44.7.html` | 125 | `(none)` | `border-collapse:collapse;width:100%;font-size:0.92em;` |

## Caption mechanism by table class

| Class | <caption> | preceding-p | p/div.table-caption | <figcaption> | none |
|---|---:|---:|---:|---:|---:|
| `complex-table` | 17 | 0 | 1 | 0 | 248 |
| `(no class)` | 17 | 0 | 0 | 76 | 89 |
| `comparison-table` | 4 | 0 | 0 | 0 | 0 |
