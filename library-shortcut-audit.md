# Library Shortcut Opportunities Audit
Scanned: 2 files
Candidates: 2

## Summary by pattern

| Pattern | Library | Hits |
|---|---|---|
| `text_splitter` | langchain.text_splitter.RecursiveCharacterTextSplitter | 1 |
| `vector_nn_search` | faiss / scipy.spatial.cKDTree | 1 |

## Top candidates (highest score first)

### 1. `part-5-retrieval-conversation\module-22-embeddings-vector-db\section-22.4.html` — Code Fragment 22.4.11 (56 lines, score=2.91)
- **Caption**: Defines fixed_chunk and recursive_chunk
- **Pattern**: `text_splitter`
- **Library**: langchain.text_splitter.RecursiveCharacterTextSplitter
- **Suggestion**: use `RecursiveCharacterTextSplitter(chunk_size=..., chunk_overlap=...)` instead of this hand-rolled chunker
- **Match snippet**: `or hierarchical representations." | ) | def fixed_chunk(text, size=300, overlap=50): | chunks, s = [], 0 | while s < len(text):`

### 2. `part-5-retrieval-conversation\module-22-embeddings-vector-db\section-22.2.html` — Code Fragment 22.2.1 (28 lines, score=1.57)
- **Caption**: Brute-force k-NN search with NumPy
- **Pattern**: `vector_nn_search`
- **Library**: faiss / scipy.spatial.cKDTree
- **Suggestion**: use `faiss.IndexFlatIP` or `scipy.spatial.cKDTree.query` instead of this brute-force NN loop
- **Match snippet**: `th NumPy | import numpy as np | import time | def brute_force_knn(query, vectors, k=10, metric="cosine"): | """ | Exact nearest neighbor searc`

