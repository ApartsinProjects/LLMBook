# Library Shortcut Opportunities Audit
Scanned: 12 files
Candidates: 24

## Summary by pattern

| Pattern | Library | Hits |
|---|---|---|
| `cosine_similarity` | numpy or sklearn.metrics.pairwise.cosine_similarity | 9 |
| `vector_nn_search` | faiss / scipy.spatial.cKDTree | 8 |
| `retry_backoff` | tenacity | 4 |
| `text_splitter` | langchain.text_splitter.RecursiveCharacterTextSplitter | 2 |
| `attention_from_scratch` | torch.nn.functional.scaled_dot_product_attention | 1 |

## Top candidates (highest score first)

### 1. `part-5-retrieval-conversation\module-20-conversational-ai\section-20.3.html` — Code Fragment 20.3.3 (88 lines, score=4.50)
- **Caption**: Define MemoryEntry, VectorMemoryStore; implement __init__, store, retrieve
- **Pattern**: `cosine_similarity`
- **Library**: numpy or sklearn.metrics.pairwise.cosine_similarity
- **Suggestion**: use `sklearn.metrics.pairwise.cosine_similarity(A, B)` or `(A @ B.T) / (||A|| * ||B||)` from numpy
- **Match snippet**: `@staticmethod | def _cosine_sim(a: list[float], b: list[float]) -> float: | a, b = np.arra`

### 2. `part-5-retrieval-conversation\module-20-conversational-ai\section-20.3.html` — Code Fragment 20.3.11 (61 lines, score=3.66)
- **Caption**: Defining ShortTermMemory, Summarizer, LongTermMemory
- **Pattern**: `cosine_similarity`
- **Library**: numpy or sklearn.metrics.pairwise.cosine_similarity
- **Suggestion**: use `sklearn.metrics.pairwise.cosine_similarity(A, B)` or `(A @ B.T) / (||A|| * ||B||)` from numpy
- **Match snippet**: `qe = self.model.encode(q) | s = np.dot(self.embeddings, qe)/(np.linalg.norm(self.embeddings,axis=1)*np.linalg.norm(qe)) | idx = np.argsort(s)[::-1][:`

### 3. `part-7-multimodal-applications\module-26-multimodal\section-26.7.html` — Code Fragment 26.7.3 (58 lines, score=3.48)
- **Caption**: Language-embedded Gaussian editing: conceptual pipeline
- **Pattern**: `cosine_similarity`
- **Library**: numpy or sklearn.metrics.pairwise.cosine_similarity
- **Suggestion**: use `sklearn.metrics.pairwise.cosine_similarity(A, B)` or `(A @ B.T) / (||A|| * ||B||)` from numpy
- **Match snippet**: `sian language feature | sim = np.dot(query_embedding, g.language_feature) / ( | np.linalg.norm(query_embedding) | * np.linalg.norm(g.language_feature)`

### 4. `part-5-retrieval-conversation\module-20-conversational-ai\section-20.3.html` — Code Fragment 20.3.11 (61 lines, score=3.42)
- **Caption**: Defining ShortTermMemory, Summarizer, LongTermMemory
- **Pattern**: `vector_nn_search`
- **Library**: faiss / scipy.spatial.cKDTree
- **Suggestion**: use `faiss.IndexFlatIP` or `scipy.spatial.cKDTree.query` instead of this brute-force NN loop
- **Match snippet**: `ncode(self.facts) | return nf | def search(self, q, k=3): | if not self.facts: return [] | qe = self.model.enco`

### 5. `part-5-retrieval-conversation\module-18-embeddings-vector-db\section-18.4.html` — Code Fragment 18.4.11 (56 lines, score=3.36)
- **Caption**: Defines fixed_chunk and recursive_chunk
- **Pattern**: `cosine_similarity`
- **Library**: numpy or sklearn.metrics.pairwise.cosine_similarity
- **Suggestion**: use `sklearn.metrics.pairwise.cosine_similarity(A, B)` or `(A @ B.T) / (||A|| * ||B||)` from numpy
- **Match snippet**: `ce = model.encode(chunks) | scores = np.dot(ce,qe)/(np.linalg.norm(ce,axis=1)*np.linalg.norm(qe)) | i = np.argmax(scores) | return chunks[i],`

### 6. `part-3-working-with-llms\module-11-llm-apis\section-11.3.html` — Code Fragment 11.3.5 (50 lines, score=3.00)
- **Caption**: Build a semantic cache that hashes prompts to avoid redundant API calls
- **Pattern**: `cosine_similarity`
- **Library**: numpy or sklearn.metrics.pairwise.cosine_similarity
- **Suggestion**: use `sklearn.metrics.pairwise.cosine_similarity(A, B)` or `(A @ B.T) / (||A|| * ||B||)` from numpy
- **Match snippet**: `self.max_entries = max_entries | def _cosine_similarity(self, a: np.ndarray, b: np.ndarray) -> float: | return float(np.dot(a, b)`

### 7. `part-5-retrieval-conversation\module-18-embeddings-vector-db\section-18.4.html` — Code Fragment 18.4.11 (56 lines, score=2.91)
- **Caption**: Defines fixed_chunk and recursive_chunk
- **Pattern**: `text_splitter`
- **Library**: langchain.text_splitter.RecursiveCharacterTextSplitter
- **Suggestion**: use `RecursiveCharacterTextSplitter(chunk_size=..., chunk_overlap=...)` instead of this hand-rolled chunker
- **Match snippet**: `or hierarchical representations." | ) | def fixed_chunk(text, size=300, overlap=50): | chunks, s = [], 0 | while s < len(text):`

### 8. `part-5-retrieval-conversation\module-19-rag\section-19.2.html` — Code Fragment 19.2.10 (50 lines, score=2.80)
- **Caption**: Defines search and expand
- **Pattern**: `vector_nn_search`
- **Library**: faiss / scipy.spatial.cKDTree
- **Suggestion**: use `faiss.IndexFlatIP` or `scipy.spatial.cKDTree.query` instead of this brute-force NN loop
- **Match snippet**: `s) | norms = np.linalg.norm(embs, axis=1) | def search(q, k=5): | qe = bi.encode(q) | s = np.dot(embs, qe)/(norms*np.linalg.norm(qe`

### 9. `part-5-retrieval-conversation\module-18-embeddings-vector-db\section-18.1.html` — Code Fragment 18.1.11 (46 lines, score=2.76)
- **Caption**: Defines search and p_at_k
- **Pattern**: `cosine_similarity`
- **Library**: numpy or sklearn.metrics.pairwise.cosine_similarity
- **Suggestion**: use `sklearn.metrics.pairwise.cosine_similarity(A, B)` or `(A @ B.T) / (||A|| * ||B||)` from numpy
- **Match snippet**: `qe = model.encode(query) | scores = np.dot(embs, qe) / (np.linalg.norm(embs, axis=1) * np.linalg.norm(qe)) | idx = np.argsort(scores)[::-1][:k]`

### 10. `part-5-retrieval-conversation\module-18-embeddings-vector-db\section-18.4.html` — Code Fragment 18.4.9 (52 lines, score=2.70)
- **Caption**: Defines fixed_chunk and recursive_chunk
- **Pattern**: `text_splitter`
- **Library**: langchain.text_splitter.RecursiveCharacterTextSplitter
- **Suggestion**: use `RecursiveCharacterTextSplitter(chunk_size=..., chunk_overlap=...)` instead of this hand-rolled chunker
- **Match snippet**: `) | # Strategy 1: Fixed-size with overlap | def fixed_chunk(text, size=300, overlap=50): | chunks, start = [], 0 | while start < len(text):`

### 11. `part-5-retrieval-conversation\module-18-embeddings-vector-db\section-18.1.html` — Code Fragment 18.1.11 (46 lines, score=2.58)
- **Caption**: Defines search and p_at_k
- **Pattern**: `vector_nn_search`
- **Library**: faiss / scipy.spatial.cKDTree
- **Suggestion**: use `faiss.IndexFlatIP` or `scipy.spatial.cKDTree.query` instead of this brute-force NN loop
- **Match snippet**: `embs_l = model_large.encode(documents) | def search(query, model, embs, docs, k=3): | qe = model.encode(query) | scores = np.dot`

### 12. `part-8-evaluation-production\module-29-production-engineering\section-29.6.html` — Code Fragment 29.6.5 (44 lines, score=2.46)
- **Caption**: Budget-aware retry with jittered exponential backoff. The function checks cumulative cost before each attempt, preventing runaway spend when partial failures consume tokens. Context window overflow is treated as a non-transient error and raised immediately, since retrying the same oversized input will always fail. The Retry-After header from rate-limit responses is respected to avoid hammering a provider that has explicitly requested a cooldown period.
- **Pattern**: `retry_backoff`
- **Library**: tenacity
- **Suggestion**: use `@tenacity.retry(stop=stop_after_attempt(5), wait=wait_exponential())` instead of hand-rolled retry/backoff
- **Match snippet**: `al_delay | last_exception = None | | for attempt in range(1, max_attempts + 1): | # Budget gate: stop if we have already spent too m`

### 13. `part-6-agentic-ai\module-25-agent-safety-production\section-25.4.html` — Code Fragment (no caption) (43 lines, score=2.41)
- **Pattern**: `retry_backoff`
- **Library**: tenacity
- **Suggestion**: use `@tenacity.retry(stop=stop_after_attempt(5), wait=wait_exponential())` instead of hand-rolled retry/backoff
- **Match snippet**: `ker open; cool-down in effect") | for attempt in range(self.max_retries): | try: | result = await asyncio.wait_`

### 14. `part-8-evaluation-production\module-29-production-engineering\section-29.5.html` — Code Fragment 29.5.5 (40 lines, score=2.40)
- **Caption**: A semantic cache that uses embedding similarity to match incoming queries against cached responses. When the cosine similarity exceeds the threshold (0.95), the cached response is returned without making an LLM call. In production, replace the list-based cache with a vector database like Pinecone or Qdrant for efficient similarity search at scale.
- **Pattern**: `cosine_similarity`
- **Library**: numpy or sklearn.metrics.pairwise.cosine_similarity
- **Suggestion**: use `sklearn.metrics.pairwise.cosine_similarity(A, B)` or `(A @ B.T) / (||A|| * ||B||)` from numpy
- **Match snippet**: `ages.""" | return messages[-1]["content"] | def _cosine_similarity(self, a, b) -> float: | return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg`

### 15. `part-5-retrieval-conversation\module-20-conversational-ai\section-20.3.html` — Code Fragment 20.3.9 (38 lines, score=2.28)
- **Caption**: Defining LongTermMemory
- **Pattern**: `cosine_similarity`
- **Library**: numpy or sklearn.metrics.pairwise.cosine_similarity
- **Suggestion**: use `sklearn.metrics.pairwise.cosine_similarity(A, B)` or `(A @ B.T) / (||A|| * ||B||)` from numpy
- **Match snippet**: `.encode(query) | scores = np.dot(self.embeddings, qe) / ( | np.linalg.norm(self.embeddings, axis=1) * np.linalg.norm(qe)) | idx = np.argsort`

### 16. `part-5-retrieval-conversation\module-20-conversational-ai\section-20.3.html` — Code Fragment 20.3.9 (38 lines, score=2.13)
- **Caption**: Defining LongTermMemory
- **Pattern**: `vector_nn_search`
- **Library**: faiss / scipy.spatial.cKDTree
- **Suggestion**: use `faiss.IndexFlatIP` or `scipy.spatial.cKDTree.query` instead of this brute-force NN loop
- **Match snippet**: `s) | return new_facts | def search(self, query, top_k=3): | if not self.facts or self.embeddings is None:`

### 17. `part-6-agentic-ai\module-25-agent-safety-production\section-25.4.html` — Code Fragment 25.4.1 (38 lines, score=2.13)
- **Caption**: Defining ResilientAgent
- **Pattern**: `retry_backoff`
- **Library**: tenacity
- **Suggestion**: use `@tenacity.retry(stop=stop_after_attempt(5), wait=wait_exponential())` instead of hand-rolled retry/backoff
- **Match snippet**: `elf.fallback_llm, "fallback")]: | for attempt in range(3): | try: | response = await llm.ainvoke(prompt)`

### 18. `part-5-retrieval-conversation\module-19-rag\section-19.2.html` — Code Fragment 19.2.6 (30 lines, score=1.68)
- **Caption**: Implementation of baseline_search
- **Pattern**: `vector_nn_search`
- **Library**: faiss / scipy.spatial.cKDTree
- **Suggestion**: use `faiss.IndexFlatIP` or `scipy.spatial.cKDTree.query` instead of this brute-force NN loop
- **Match snippet**: `orms = np.linalg.norm(doc_embs, axis=1) | def baseline_search(query, top_k=5): | qe = bi_encoder.encode(query) | scores = np.dot(doc_embs,`

### 19. `part-5-retrieval-conversation\module-18-embeddings-vector-db\section-18.2.html` — Code Fragment 18.2.1 (28 lines, score=1.57)
- **Caption**: Brute-force k-NN search with NumPy
- **Pattern**: `vector_nn_search`
- **Library**: faiss / scipy.spatial.cKDTree
- **Suggestion**: use `faiss.IndexFlatIP` or `scipy.spatial.cKDTree.query` instead of this brute-force NN loop
- **Match snippet**: `th NumPy | import numpy as np | import time | def brute_force_knn(query, vectors, k=10, metric="cosine"): | """ | Exact nearest neighbor searc`

### 20. `part-1-foundations\module-04-transformer-architecture\section-4.1.html` — Code Fragment (no caption) (29 lines, score=1.51)
- **Pattern**: `attention_from_scratch`
- **Library**: torch.nn.functional.scaled_dot_product_attention
- **Suggestion**: use `F.scaled_dot_product_attention(q, k, v, is_causal=True)` for the kernel-fused, flash-attention-backed version
- **Match snippet**: `dot-product attention | scores = (q @ k.transpose(-2, -1)) / (self.head_dim ** 0.5) | if mask is not None: | scor`

### 21. `part-11-idea-to-product\module-34-idea-to-product\section-34.1.html` — Code Fragment 34.1.2 (23 lines, score=1.29)
- **Caption**: A retry-with-fallback wrapper that prevents agents from crashing or hallucinating when a tool call fails. Production systems should log each attempt to the observability stack (Chapter 28).
- **Pattern**: `retry_backoff`
- **Library**: tenacity
- **Suggestion**: use `@tenacity.retry(stop=stop_after_attempt(5), wait=wait_exponential())` instead of hand-rolled retry/backoff
- **Match snippet**: `lt', and 'attempts' fields. | """ | for attempt in range(1, max_retries + 1): | try: | result = tool_fn(**args)`

### 22. `part-5-retrieval-conversation\module-18-embeddings-vector-db\section-18.4.html` — Code Fragment 18.4.10 (20 lines, score=1.20)
- **Caption**: Implementation of search_chunks
- **Pattern**: `cosine_similarity`
- **Library**: numpy or sklearn.metrics.pairwise.cosine_similarity
- **Suggestion**: use `sklearn.metrics.pairwise.cosine_similarity(A, B)` or `(A @ B.T) / (||A|| * ||B||)` from numpy
- **Match snippet**: `ery) | ce = model.encode(chunks) | scores = np.dot(ce, qe) / (np.linalg.norm(ce, axis=1) * np.linalg.norm(qe)) | idx = np.argsort(scores)[::-1][:top_k] | return`

### 23. `part-5-retrieval-conversation\module-18-embeddings-vector-db\section-18.4.html` — Code Fragment 18.4.10 (20 lines, score=1.12)
- **Caption**: Implementation of search_chunks
- **Pattern**: `vector_nn_search`
- **Library**: faiss / scipy.spatial.cKDTree
- **Suggestion**: use `faiss.IndexFlatIP` or `scipy.spatial.cKDTree.query` instead of this brute-force NN loop
- **Match snippet**: `is deep learning?", "deep learning"), | ] | def search_chunks(query, chunks, model, top_k=1): | qe = model.encode(query) | ce = model.encode(chunk`

### 24. `part-5-retrieval-conversation\module-18-embeddings-vector-db\section-18.1.html` — Code Fragment 18.1.9 (18 lines, score=1.01)
- **Caption**: Encode the query, compute cosine similarity, return top-k
- **Pattern**: `vector_nn_search`
- **Library**: faiss / scipy.spatial.cKDTree
- **Suggestion**: use `faiss.IndexFlatIP` or `scipy.spatial.cKDTree.query` instead of this brute-force NN loop
- **Match snippet**: `import numpy as np | def semantic_search(query, model, doc_embeddings, documents, top_k=3): | """Find the top-k most simil`

