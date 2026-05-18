# Duplicate-Content Detection Report

Scanned 13 sections.

## Top Hot Entities (mention count across sections)

| Entity | Total Mentions | Sections | Top Carriers |
|---|---:|---:|---|
| drift | 54 | 8 | S42.4(39), M42.idx(5), S42.5(3), S42.6(3), S42.10(1) |
| perplexity | 42 | 3 | S42.1(23), S42.12(18), M42.idx(1) |
| BLEU | 39 | 4 | S42.1(25), S42.12(12), M42.idx(1), S42.11(1) |
| embedding | 39 | 10 | S42.4(16), S42.6(7), S42.7(5), S42.9(3), M42.idx(2) |
| MLflow | 37 | 2 | S42.7(20), S42.9(17) |
| OpenAI | 36 | 7 | S42.11(15), S42.6(9), S42.7(4), S42.4(3), S42.9(3) |
| RAG | 32 | 10 | S42.8(8), S42.6(5), S42.9(5), S42.10(4), M42.idx(3) |
| promptfoo | 32 | 4 | S42.3(16), S42.11(13), S42.1(2), M42.idx(1) |
| BERTScore | 30 | 5 | S42.1(20), S42.12(6), S42.2(2), M42.idx(1), S42.11(1) |
| Langfuse | 28 | 4 | S42.6(21), S42.9(4), S42.4(2), M42.idx(1) |
| attention | 28 | 3 | S42.8(25), S42.10(2), S42.12(1) |
| OpenTelemetry | 25 | 4 | S42.9(18), M42.idx(3), S42.6(3), S42.8(1) |
| prompt injection | 25 | 3 | S42.3(20), S42.6(4), M42.idx(1) |
| RULER | 25 | 2 | S42.8(23), M42.idx(2) |
| ROUGE | 23 | 5 | S42.12(12), S42.1(7), S42.2(2), M42.idx(1), S42.11(1) |
| OTel | 23 | 1 | S42.9(23) |
| context length | 22 | 3 | S42.8(20), M42.idx(1), S42.10(1) |
| LangSmith | 20 | 4 | S42.6(13), S42.9(5), M42.idx(1), S42.3(1) |
| YaRN | 20 | 1 | S42.8(20) |
| NIAH | 18 | 1 | S42.8(18) |
| fine-tuning | 15 | 4 | S42.8(11), S42.2(2), S42.10(1), S42.4(1) |
| langchain | 15 | 2 | S42.6(13), S42.9(2) |
| Docker | 14 | 2 | S42.7(12), S42.10(2) |
| MMLU | 13 | 4 | S42.1(8), S42.10(3), M42.idx(1), S42.2(1) |
| anthropic | 13 | 5 | S42.11(8), S42.9(2), S42.3(1), S42.7(1), S42.8(1) |
| position bias | 12 | 4 | S42.1(6), S42.8(4), M42.idx(1), S42.5(1) |
| Phoenix | 11 | 3 | S42.6(8), M42.idx(2), S42.9(1) |
| Needle-in-a-Haystack | 11 | 2 | S42.8(9), M42.idx(2) |
| GPT-4 | 11 | 3 | S42.1(5), S42.10(5), S42.5(1) |
| context window | 11 | 1 | S42.8(11) |
| Chatbot Arena | 10 | 2 | S42.1(9), M42.idx(1) |
| embeddings | 10 | 4 | S42.1(6), S42.12(2), S42.4(1), S42.7(1) |
| LongBench v2 | 10 | 1 | S42.8(10) |
| DeepEval | 9 | 5 | S42.1(5), M42.idx(1), S42.11(1), S42.3(1), S42.4(1) |
| BERT | 9 | 2 | S42.1(8), S42.12(1) |
| GPT-4o | 9 | 5 | S42.7(3), S42.2(2), S42.6(2), S42.1(1), S42.4(1) |
| datasets | 9 | 3 | S42.7(5), S42.10(3), S42.6(1) |
| NTK-aware | 9 | 1 | S42.8(9) |
| position interpolation | 9 | 1 | S42.8(9) |
| RoPE | 9 | 1 | S42.8(9) |

## Multiple Introductions (entity bolded in >=2 sections)

Entities that appear in `<strong>` tags in 2+ sections likely have
multiple introductions. The book should pick ONE canonical home for each.

| Entity | # Sections | Sections |
|---|---:|---|
| METEOR | 2 | S42.1, S42.12 |
| perplexity | 2 | S42.1, S42.12 |
| position bias | 2 | S42.1, S42.8 |

## High-Overlap Section Pairs (Jaccard on entities)

Pairs of sections whose entity sets overlap heavily are candidates
for content consolidation.

| A | B | Jaccard | Shared | Top Shared Entities |
|---|---|---:|---:|---|
| S42.6 | S42.9 | 0.438 | 14/21+25 | Langfuse, OpenTelemetry, LangSmith, langchain, OpenAI, embedding, RAG, Phoenix |

## Verbatim Paragraph Duplicates (60-word windows)

Pairs of sections that share verbatim 60-word chunks. High counts
indicate accidental copy-paste that should be deduplicated.

| A | B | Duplicate chunks |
|---|---|---:|
