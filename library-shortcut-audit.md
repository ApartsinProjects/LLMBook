# Library Shortcut Opportunities Audit
Scanned: 2 files
Candidates: 2

## Summary by pattern

| Pattern | Library | Hits |
|---|---|---|
| `vector_nn_search` | faiss / scipy.spatial.cKDTree | 1 |
| `retry_backoff` | tenacity | 1 |

## Top candidates (highest score first)

### 1. `part-7-retrieval-information-extraction-with-llms\module-31-embeddings-vector-db\section-31.2.html` — Code Fragment 31.2.1 (28 lines, score=1.57)
- **Caption**: Brute-force k-NN search with NumPy
- **Pattern**: `vector_nn_search`
- **Library**: faiss / scipy.spatial.cKDTree
- **Suggestion**: use `faiss.IndexFlatIP` or `scipy.spatial.cKDTree.query` instead of this brute-force NN loop
- **Match snippet**: `th NumPy | import numpy as np | import time | def brute_force_knn(query, vectors, k=10, metric="cosine"): | """ | Exact nearest neighbor searc`

### 2. `part-1-llm-building-blocks\module-05-tools-of-the-trade\section-5.2.html` — Code Fragment (no caption) (20 lines, score=1.12)
- **Caption**: Code Fragment g.4.2: Implement call_with_retry.
- **Pattern**: `retry_backoff`
- **Library**: tenacity
- **Suggestion**: use `@tenacity.retry(stop=stop_after_attempt(5), wait=wait_exponential())` instead of hand-rolled retry/backoff
- **Match snippet**: `onential backoff on rate limits.""" | for attempt in range(max_retries): | try: | response = client.chat.completions.create`

