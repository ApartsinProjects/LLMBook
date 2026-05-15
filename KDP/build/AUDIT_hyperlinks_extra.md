# Extra-Concept Hyperlinking Audit (APPLIED)

- Files scanned: 383
- Aliases: 40
- Distinct concept-ids: 24
- Files modified: 33
- Total new links: 78
- Files skipped (cap/density): 289

## Top 25 files by new-link count

-   5  part-2-understanding-llms/module-09-inference-optimization/index.html
-   5  appendices/appendix-ag-problem-solution-key/index.html
-   5  appendices/appendix-s-inference-serving/index.html
-   4  part-2-understanding-llms/index.html
-   4  appendices/appendix-t-distributed-ml/section-t.5.html
-   4  appendices/appendix-u-docker-containers/section-u.4.html
-   3  part-9-safety-strategy/module-30-safety-ethics-regulation/index.html
-   3  part-8-evaluation-production/module-28-evaluation-observability/index.html
-   3  part-4-training-adapting/module-14-synthetic-data/index.html
-   3  part-3-working-with-llms/module-12-prompt-engineering/index.html
-   3  appendices/appendix-s-inference-serving/section-s.1.html
-   3  appendices/appendix-s-inference-serving/section-s.3.html
-   3  appendices/appendix-s-inference-serving/section-s.4.html
-   3  appendices/appendix-v-tooling-ecosystem/index.html
-   2  capstone/index.html
-   2  part-5-retrieval-conversation/index.html
-   2  part-6-agentic-ai/module-22-tool-use-protocols/index.html
-   2  part-6-agentic-ai/module-23-multi-agent-systems/index.html
-   2  part-5-retrieval-conversation/module-19-rag/index.html
-   2  part-1-foundations/module-02-tokenization-subword-models/index.html
-   2  appendices/appendix-b-ml-essentials/section-b.4.html
-   2  appendices/appendix-u-docker-containers/index.html
-   1  index.html
-   1  front-matter/foreword.html
-   1  front-matter/index.html

## Most-linked extra concepts

-   11  cx-agent  (Chapter 21: AI Agent Foundations)
-   10  cx-huggingface  (Appendix K: HuggingFace: Transformers, Datasets, and Hub)
-   10  cx-tgi  (Section S.2: Text Generation Inference (TGI))
-    6  cx-sglang  (Section S.3: SGLang: Structured Generation and RadixAttention)
-    5  cx-continuous-batching  (Section 9.4: Serving Infrastructure)
-    5  cx-red-teaming  (Section 30.8: Red Teaming Frameworks & LLM Security Testing)
-    4  cx-rerank  (Section 19.2: Advanced RAG Techniques)
-    4  cx-gptq  (Section S.4: Quantization for Serving (GPTQ, AWQ, GGUF))
-    4  cx-llm-judge  (Section 28.8: LLM-as-Judge)
-    3  cx-jailbreak  (Section 30.1: LLM Security Threats)
-    3  cx-react  (Section 21.1: What Makes an LLM an Agent (and What Doesn't))
-    3  cx-paged-attention  (Section 9.4: Serving Infrastructure)
-    2  cx-multi-agent  (Chapter 23: Multi-Agent Systems)
-    2  cx-agentic  (Chapter 21: AI Agent Foundations)
-    2  cx-gguf  (Section S.4: Quantization for Serving (GPTQ, AWQ, GGUF))
-    1  cx-bpe  (Section 2.2: Subword Tokenization Algorithms)
-    1  cx-hybrid-search  (Section 19.2: Advanced RAG Techniques)
-    1  cx-pruning  (Section 9.5: Model Pruning & Sparsity)
-    1  cx-mt-bench  (Section 28.8: LLM-as-Judge)

## Aliases that produced ZERO new links

(could mean term is rare in prose, already linked elsewhere, or used only in code/headings)

- `awq` -> cx-awq (matched only as part of "GPTQ, AWQ" phrase where "GPTQ" wins)
- `byte pair encoding` -> cx-bpe (variant "byte-pair encoding" took the slot)
- `dense retrieval` -> cx-dense-retrieval (BM25/hybrid took target-file slot first)
- `sparse retrieval` -> cx-sparse-retrieval (BM25 took target-file slot first)
- `react agent` -> cx-react (variant captured by main "ReAct" match elsewhere)
- `sglang` repeated terms past per-target-tail dedup

## Idempotency

A second invocation produced 0 new links, confirming the link insertion is idempotent.

## Notes

- Each concept gets at most ONE link per page (per-page dedup).
- A page that IS a target section never receives a link to itself (self-target guard).
- Same density floor (0.5 links per 1000 chars of prose) and per-page cap (20) as the phase-1 hyperlinker.
- The new links use CSS class "concept-link" to distinguish them from glossary links (class "glossary-link").
