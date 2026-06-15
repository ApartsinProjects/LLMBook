# Graduate-Depth Audit: Part 7 (Retrieval & Information Extraction)

| Section | Title (short) | Verdict | Missing piece (only if not COURSE-READY) |
|---|---|---|---|
| 31.1 | Classical Embedding Foundations | COURSE-READY | |
| 31.2 | Modern Embedding Architectures & Selection | COURSE-READY | |
| 31.3 | ANN Search: HNSW and IVF | COURSE-READY | |
| 31.4 | Product Quantization, Composite Indexes, FAISS | COURSE-READY | |
| 31.5 | Vector Database Systems | CATALOG-OK | |
| 31.6 | Document Processing & Chunking | COURSE-READY | |
| 31.7 | Production RAG Pipelines, Evaluation & Topic Modeling | COURSE-READY | |
| 31.8 | Vision-Based Document Retrieval (ColPali) | COURSE-READY | |
| 32.1 | RAG Foundations: Pipeline & Why It Beats Fine-Tuning | COURSE-READY | |
| 32.2 | RAG Indexing, Evaluation & Long-Context | COURSE-READY | |
| 32.3 | Agentic RAG | COURSE-READY | |
| 32.3a | Deep Research Architectures | COURSE-READY | |
| 32.4 | Text-to-SQL & Structured-Data RAG | COURSE-READY | |
| 32.5 | Source Attribution & Citation Verification | COURSE-READY | |
| 33.1 | Joint Embedding Spaces (CLIP/SigLIP/ImageBind) | COURSE-READY | |
| 33.2 | Multimodal RAG Patterns | COURSE-READY | |
| 33.3 | When to Retrieve, When to Reason | COURSE-READY | |
| 33.4 | Multimodal Production Trade-offs | CATALOG-OK | |
| 34.1 | The Information Extraction Landscape (CRF) | COURSE-READY | |
| 34.2 | Classical & Encoder IE (spaCy, REBEL) | COURSE-READY | |
| 34.3 | Hybrid IE Architectures | COURSE-READY | |
| 34.4 | Production IE Deployment (grounding, degradation) | COURSE-READY | |
| 34.5 | Coreference Resolution | COURSE-READY | |
| 35.1 | Advanced RAG: Query Transform, Re-rank, Self-Corrective | COURSE-READY | |
| 35.2 | Advanced RAG: HyDE, Contextual Retrieval, CRAG/Self-RAG | COURSE-READY | |
| 35.2a | Fusion Retrieval & Multi-Modal RAG | COURSE-READY | |
| 35.3 | Knowledge Graphs for RAG (triples, RDF/property, Cypher) | COURSE-READY | |
| 35.4 | GraphRAG (Leiden communities, Lazy/DRIFT) | COURSE-READY | |
| 35.5 | RAG Ingestion Pipelines (connectors, chunking, orchestration) | COURSE-READY | |
| 35.6 | RAG Frameworks (LangChain, LlamaIndex, Haystack) | CATALOG-OK | |
| 35.7 | Production RAG, DSPy & Retrieval Security | DEPTH-GAP | DSPy compiler/teleprompter optimization and the retrieval-layer attack/defense (corpus poisoning, prompt injection via retrieved docs) are named in prose lists but neither mechanism is derived or worked; observability/caching/error-handling stay at the bullet-list level. |
| 36.1 | Retrieval Platforms | CATALOG-OK | |
| 36.2 | Retrieval Libraries | CATALOG-OK | |
| 36.3 | Retrieval Benchmarks | CATALOG-OK | |
| 36.4 | Embedding & Reranking Models | CATALOG-OK | |
| 36.5 | Retrieval Literature & Reading List | CATALOG-OK | |

## Summary
- COURSE-READY: 28 | DEPTH-GAP: 1 | NOT-SELF-CONTAINED: 0 | CATALOG-OK: 7
- Top sections most worth enriching:
  1. 35.7 (Production RAG, DSPy & Security): the only DEPTH-GAP. Add one worked DSPy compilation trace (signature -> bootstrapped few-shot -> metric-driven optimization) and a derived corpus-poisoning / retrieved-document-injection attack with its defense, so the section teaches mechanism instead of listing concerns.
  2. 35.2a (Fusion & Multi-Modal RAG): COURSE-READY but thinnest of the 35.x set. Promote RRF from a one-line mention to a worked rank-fusion example with the 1/(k+rank) constant and a tie-break trace; it currently leans on 35.1/35.6 for the actual fusion math.
  3. 33.2 (Multimodal RAG Patterns): solid but mechanism for video chunking and CLAP audio segmentation is asserted, not shown. A short worked segment-and-embed example would lift it from strong-practitioner to fully derivable.
  4. 31.5 (Vector DB Systems): correctly CATALOG-OK and explicitly flagged GIANT_SECTION, but the pre-vs-post-vs-integrated filtering subsection is the one place a graduate reader needs the recall-degradation mechanism stated quantitatively rather than narratively.
