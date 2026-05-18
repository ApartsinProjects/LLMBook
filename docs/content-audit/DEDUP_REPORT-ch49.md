# Duplicate-Content Detection Report

Scanned 6 sections.

## Top Hot Entities (mention count across sections)

| Entity | Total Mentions | Sections | Top Carriers |
|---|---:|---:|---|
| hallucination | 71 | 3 | S49.5(66), S49.1(3), M49.idx(2) |
| prompt injection | 34 | 5 | S49.1(25), S49.3(3), M49.idx(2), S49.2(2), S49.4(2) |
| Docker | 26 | 2 | S49.2(22), S49.4(4) |
| Self-Consistency | 23 | 2 | S49.5(22), M49.idx(1) |
| RAG | 15 | 1 | S49.5(15) |
| guardrail | 11 | 4 | S49.1(8), S49.3(1), S49.4(1), S49.5(1) |
| perplexity | 9 | 1 | S49.5(9) |
| OWASP | 4 | 4 | M49.idx(1), S49.1(1), S49.3(1), S49.4(1) |
| datasets | 4 | 3 | S49.5(2), M49.idx(1), S49.2(1) |
| Kubernetes | 4 | 2 | S49.4(3), S49.2(1) |
| pandas | 4 | 2 | S49.2(2), S49.4(2) |
| matplotlib | 4 | 2 | S49.2(2), S49.4(2) |
| drift | 4 | 1 | S49.4(4) |
| Llama Guard | 3 | 2 | S49.1(2), S49.3(1) |
| AWS | 3 | 1 | S49.2(3) |
| fine-tuning | 3 | 1 | S49.5(3) |
| jailbreak | 2 | 2 | M49.idx(1), S49.4(1) |
| OWASP Top 10 | 2 | 2 | S49.1(1), S49.3(1) |
| numpy | 2 | 1 | S49.2(2) |
| Hugging Face | 2 | 1 | S49.4(2) |
| guidance | 2 | 2 | S49.4(1), S49.5(1) |
| factuality | 2 | 1 | S49.5(2) |
| GDPR | 2 | 1 | S49.5(2) |
| anthropic | 1 | 1 | M49.idx(1) |
| MATH | 1 | 1 | S49.1(1) |
| ReAct | 1 | 1 | S49.1(1) |
| context window | 1 | 1 | S49.1(1) |
| Chain-of-Thought | 1 | 1 | S49.1(1) |
| openai | 1 | 1 | S49.1(1) |
| seaborn | 1 | 1 | S49.4(1) |
| Google Cloud | 1 | 1 | S49.4(1) |
| scikit-learn | 1 | 1 | S49.4(1) |
| Hugging Face Hub | 1 | 1 | S49.4(1) |
| HF Hub | 1 | 1 | S49.4(1) |
| ONNX | 1 | 1 | S49.4(1) |
| GPT-4 | 1 | 1 | S49.5(1) |
| RLHF | 1 | 1 | S49.5(1) |
| alignment | 1 | 1 | S49.5(1) |
| HIPAA | 1 | 1 | S49.5(1) |
| embedding | 1 | 1 | S49.5(1) |

## Multiple Introductions (entity bolded in >=2 sections)

Entities that appear in `<strong>` tags in 2+ sections likely have
multiple introductions. The book should pick ONE canonical home for each.

| Entity | # Sections | Sections |
|---|---:|---|

## High-Overlap Section Pairs (Jaccard on entities)

Pairs of sections whose entity sets overlap heavily are candidates
for content consolidation.

| A | B | Jaccard | Shared | Top Shared Entities |
|---|---|---:|---:|---|
| S49.1 | S49.3 | 0.455 | 5/11+5 | prompt injection, guardrail, Llama Guard, OWASP, OWASP Top 10 |

## Verbatim Paragraph Duplicates (60-word windows)

Pairs of sections that share verbatim 60-word chunks. High counts
indicate accidental copy-paste that should be deduplicated.

| A | B | Duplicate chunks |
|---|---|---:|
