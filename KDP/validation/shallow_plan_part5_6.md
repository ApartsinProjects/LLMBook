# Shallow Audit Plan: Parts V and VI

**Scope:** Chapters 17-19 (Part V Retrieval/Conversation), 20-24 (Part VI Agentic AI) [new numbering]
**Date:** 2026-05-12
**Total findings: 36**

## Overall

**Part VI (Agentic AI) is the strongest part of the audit scope.** Nearly every section has working code, real-world scenarios with named stakeholders, Warning callouts addressing misconceptions, and Key Insight callouts. Sections on Agent Safety (26.1-26.7) and Tool Use Protocols (23.1-23.5) are publication-ready.

**Part V** (vector DBs, RAG, conversational AI) has strong foundational content but shows a consistent pattern: vector DB systems covers 5 systems adequately but treats 3 (Weaviate, Milvus, LanceDB) as one-paragraph intros while giving 4 others full code; Advanced RAG leaves Step-Back Prompting unpaired with code while HyDE and multi-query both have implementations; GraphRAG references technical concepts (Leiden, coreference) without explanation.

## TOP PRIORITY FIXES

1. **Broken cross-reference** in section-22.3: "internal Section 8.1" renders as literal text instead of "internal chain of thought (Section 8.1)" with a hyperlink. **Rendering bug, immediate fix**.
2. **Leiden algorithm** (GraphRAG, section-31.7): named without explanation. Add: "Leiden finds dense subgraphs (entity clusters); preferred over Louvain because Louvain can produce disconnected communities".
3. **MemGPT/Letta architecture** (section-19.3): promised in Big Picture, absent from body. Add: explicit memory tools (`write_memory`, `recall_memory`) for self-managed long-term memory.
4. **ScaNN** (section-17.2): one paragraph, no code, no comparison. Add anisotropic quantization explanation + 10x throughput claim with citation.
5. **Reciprocal Rank Fusion formula** (section-17.3): present but no term-by-term explanation. Why rank not score? `k=60` constant rationale?
6. **Self-RAG reflection tokens** (section-23.5): mechanism unexplained. Add: `[Retrieve]`, `[ISREL]`, `[ISSUP]`, `[ISUSE]` tokens are model-generated, not rule-based.
7. **Step-Back Prompting** (section-31.2): one paragraph, no code (HyDE/multi-query both have code). Add implementation example.
8. **Voice agent platforms** (section-19.5): OpenAI Realtime, LiveKit, Pipecat, Vapi, Bland.ai listed with no architectural differentiation.
9. **InfoNCE formula** (section-17.1): magnet metaphor in figure but text body explains math without connecting back. Add explicit mapping (numerator = attraction, denominator = repulsion).
10. **InfoNCE numeric trace** (section-17.1): formula present, no worked numbers.
11. **HNSW failure modes** (section-17.2): ghost vectors after deletion, ef_search<k recall collapse, high-dim degradation above 1200 dims.
12. **Citation hallucination** (section-31.1): subtle RAG failure (model cites a real document but claims it supports an answer it doesn't) — not separated from "RAG Eliminates Hallucination" Warning.

## SHOPPING-LIST violations

- Voice agents (5 platforms in one paragraph)
- RAG framework section (LangChain has code; LlamaIndex/Haystack possibly one paragraph)

## ONE-PARAGRAPH-INTRO violations

- LanceDB, Milvus, Weaviate (in section-17.3)
- IVF-HNSW composite index (in section-17.2)
- Apache Tika (in section-31.8 ingestion)
- Step-Back Prompting (in section-31.2)
- LATS (one sentence in section-22.2)

## MISSING-FAILURE-MODE

- HNSW (3 modes)
- RAG citation hallucination
- MCP server transport/auth/version mismatch (section-23.2)
- Multi-agent topology failures (section-24.2)

## MISSING-INTUITION

- Reciprocal Rank Fusion (rank vs score, k=60)
- HNSW layer counts (numeric example for 1M vectors)
- MaxSim scoring (numeric trace for vision RAG)
- Coreference resolution (1-paragraph definition needed)

## DANGLING-XREF

- Bare "Section 4.1" / "Section 8.1" placeholders (multiple) — same as Parts II+III pattern
- Section-22.1 re-explains ReAct from scratch instead of cross-referencing canonical home in 11.2

## SECTIONS RATED GOOD (23 of 30)

17.1, 17.2 (with caveats), 31.1, 31.2 (with caveats), 31.7 (with caveats), 19.1, 23.1, 23.2 (with caveats), 23.3, 23.4, 23.5 (with caveats), 24.2 (with caveats), 24.3, 25.1, 25.2, 25.3, 26.1-26.7.

(All chapter numbers above are the OLD numbering at audit time; v6.40 renumbered them to 17-24.)
