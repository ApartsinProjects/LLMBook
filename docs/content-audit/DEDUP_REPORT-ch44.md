# Duplicate-Content Detection Report

Scanned 7 sections.

## Top Hot Entities (mention count across sections)

| Entity | Total Mentions | Sections | Top Carriers |
|---|---:|---:|---|
| drift | 115 | 7 | S44.5(40), S44.3(34), S44.4(15), M44.idx(12), S44.2(7) |
| LangSmith | 21 | 6 | S44.3(9), S44.7(7), S44.4(2), M44.idx(1), S44.2(1) |
| MLflow | 19 | 4 | S44.2(13), M44.idx(3), S44.7(2), S44.3(1) |
| openai | 19 | 5 | S44.7(8), S44.3(6), S44.2(2), S44.6(2), S44.5(1) |
| W&B | 16 | 4 | S44.2(10), M44.idx(3), S44.7(2), S44.3(1) |
| Helicone | 15 | 3 | S44.3(8), S44.7(6), M44.idx(1) |
| Phoenix | 14 | 3 | S44.3(9), S44.7(4), M44.idx(1) |
| Langfuse | 14 | 3 | S44.3(9), S44.7(4), M44.idx(1) |
| langchain | 13 | 5 | S44.3(7), S44.2(2), S44.7(2), S44.4(1), S44.6(1) |
| OpenTelemetry | 12 | 3 | S44.3(7), S44.7(3), M44.idx(2) |
| anthropic | 9 | 4 | S44.3(5), S44.7(2), S44.5(1), S44.6(1) |
| RAG | 8 | 2 | S44.2(4), S44.3(4) |
| GPT-4o | 8 | 3 | S44.3(6), S44.2(1), S44.7(1) |
| OTel | 8 | 2 | S44.3(6), S44.7(2) |
| GenAI Semantic Conventions | 6 | 3 | S44.3(3), M44.idx(2), S44.7(1) |
| datasets | 6 | 2 | S44.7(4), S44.2(2) |
| Ragas | 6 | 1 | S44.3(6) |
| DeepEval | 6 | 2 | S44.3(5), S44.7(1) |
| Prometheus | 5 | 3 | S44.3(3), M44.idx(1), S44.4(1) |
| vLLM | 5 | 1 | S44.3(5) |
| ROUGE | 4 | 1 | S44.2(4) |
| hallucination | 4 | 3 | S44.2(2), S44.4(1), S44.5(1) |
| GPT-4 | 4 | 2 | S44.2(3), S44.6(1) |
| BLEU | 3 | 1 | S44.2(3) |
| Weights & Biases | 3 | 2 | S44.7(2), S44.2(1) |
| promptfoo | 3 | 1 | S44.7(3) |
| Datadog | 2 | 2 | M44.idx(1), S44.3(1) |
| BERTScore | 2 | 1 | S44.2(2) |
| LlamaIndex | 2 | 2 | S44.2(1), S44.3(1) |
| MT-Bench | 2 | 2 | S44.2(1), S44.7(1) |
| Chatbot Arena | 2 | 2 | S44.2(1), S44.7(1) |
| Honeycomb | 2 | 2 | S44.3(1), S44.7(1) |
| groundedness | 2 | 1 | S44.3(2) |
| TGI | 2 | 1 | S44.3(2) |
| embedding | 2 | 2 | S44.3(1), S44.7(1) |
| distribution shift | 2 | 2 | S44.4(1), S44.5(1) |
| fine-tuning | 2 | 2 | S44.4(1), S44.7(1) |
| EU AI Act | 2 | 1 | S44.6(2) |
| GPT-4o-mini | 1 | 1 | S44.2(1) |
| Chain-of-Thought | 1 | 1 | S44.2(1) |

## Multiple Introductions (entity bolded in >=2 sections)

Entities that appear in `<strong>` tags in 2+ sections likely have
multiple introductions. The book should pick ONE canonical home for each.

| Entity | # Sections | Sections |
|---|---:|---|
| drift | 3 | S44.3, S44.4, S44.5 |
| anthropic | 2 | S44.6, S44.7 |
| openai | 2 | S44.6, S44.7 |

## High-Overlap Section Pairs (Jaccard on entities)

Pairs of sections whose entity sets overlap heavily are candidates
for content consolidation.

| A | B | Jaccard | Shared | Top Shared Entities |
|---|---|---:|---:|---|
| S44.4 | S44.5 | 0.364 | 4/9+6 | drift, LangSmith, hallucination, distribution shift |

## Verbatim Paragraph Duplicates (60-word windows)

Pairs of sections that share verbatim 60-word chunks. High counts
indicate accidental copy-paste that should be deduplicated.

| A | B | Duplicate chunks |
|---|---|---:|
