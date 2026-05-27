# 1401_VectorStores — Per-Slide Summary

**Source file:** `1401_VectorStores.pptx`
**Source folder:** `SlidesPool/1400_LLM_RAG/`
**Drive link:** https://drive.google.com/file/d/12vwm7XNDzGapvzOKGpXvmkju47JOfRB_/view
**Slide count (exact, via python-pptx):** 26
**Extraction:** Local parse + slide PNG render. Bullets carry the algorithmic content; code screenshots illustrate FAISS, HNSW, Annoy, and ChromaDB usage.

---

## Slide 1 — Vector Store
Title slide for the deck on vector stores and similarity search.

## Slide 2 — Reminder: Document Representation and Retrieval
Sparse representation uses TF-IDF vectors (vocabulary-length with many zeros) and is retrieved via inverted index, which returns candidate documents for TF-IDF scoring. Dense representation uses short (300-1K) sentence embeddings and is retrieved via a vector store or database.

## Slide 3 — Similarity Search: Distance Metrics
A figure listing the common distance metrics for similarity search (cosine, L2, inner product).

## Slide 4 — Vector store operations
Section divider for the basic vector-store operations.

## Slide 5 — Exact vs. Approximate Nearest Neighbor
Section divider contrasting exact kNN with approximate methods.

## Slide 6 — FAISS library
FAISS (Facebook AI Similarity Search) implements many index types, including exact kNN.

## Slide 7 — IVF: Inverted File Index
IVF clusters all indexed vectors and uses each cluster center as a Voronoi cell. At query time, find the nearest cell centers and compare the query only with vectors in nearby clusters.

## Slide 8 — IVFPQ: IVF + Product Quantization
Represent vectors within a cell as residual vectors (the difference from the cell centroid), which brings values into approximately the same range. Product quantization splits the residual into m sub-vectors and learns a k-quantizer per sub-vector, so each residual is m small integers. Search precomputes sub-space distances, encodes the query residual using the codebooks, and approximates the distance as a sum of sub-space distances.

## Slide 9 — IVFPQ in Python
Code screenshot of IVFPQ via FAISS, with IndexFlatL2 as the quantizer that looks for nearest neighbors in discrete values (default 100).

## Slide 10 — Hierarchical Navigable Small World
Section divider for HNSW.

## Slide 11 — HNSW
HNSW builds a layered graph: the bottom layer contains all elements, higher layers progressively fewer; each node is connected to its layer-mate neighbors (small-world). Top-down greedy search starts at the top entry, moves to a neighbor closer to the query, and drops down a layer when no closer neighbor exists. Beam search extends this for top-K.

## Slide 12 — Greedy Descent
A figure illustrating the greedy descent through HNSW layers.

## Slide 13 — HNSW Construction
For each point, randomly decide which layer it enters using an exponential distribution (so few points reach the top). Insert points one by one with the same greedy search and connect each to its neighbors.

## Slide 14 — HNSW in Code
Code screenshot configuring HNSW with the candidate-pool size parameter.

## Slide 15 — Annoy
Section divider for Annoy.

## Slide 16 — Annoy: Random Projection Trees
Annoy uses random projection trees: recursively split space by random hyperplanes. A forest is a collection of such trees, and search runs across multiple trees, picking the side of each splitting hyperplane and aggregating closest matches.

## Slide 17 — Annoy Library
Code screenshot showing the Annoy library API.

## Slide 18 — Vector Databases
Section divider for full vector databases (as opposed to in-memory index libraries).

## Slide 19 — ChromaDB: Lightweight Database
ChromaDB provides persistent storage with LLM toolchain integration.

## Slide 20 — LangChain and ChromaDB
LangChain treats embeddings, vector store, and LLM as plugin modules so each is easy to swap and compose. It also supports hybrid search using embeddings together with metadata.

## Slide 21 — Hybrid Search: Combine dense/sparse retrieval
Hybrid search fuses dense and sparse retrieval results; scores are usually normalized within each result set (min-max range) before combination.

## Slide 22 — LLM-based hierarchical index
Section divider for LLM-built hierarchical indices.

## Slide 23 — Hierarchical Indices
Organize documents and chunks in multi-level indices: top-level LLM-generated summaries / document abstracts, mid-level overviews / section abstracts, and detailed chunks. Search proceeds top-down, progressively refining.

## Slide 24 — RAPTOR
RAPTOR builds a hierarchical index by embedding documents, clustering embeddings, summarizing all docs in each cluster into a single document, embedding the summary, and continuing recursively to form a tree-structured index. Search traverses the tree with the query embedding.

## Slide 25 — RAPTOR Clustering
A figure showing the clustering step inside RAPTOR.

## Slide 26 — RAPTOR: Tree Traversal Retrieval
A figure showing tree-traversal retrieval against the RAPTOR index.

---

## Deck-level takeaway
The deck covers vector stores from theory to tooling. Approximate nearest-neighbor algorithms span three families: cell-based (IVF and IVF + product quantization in FAISS), graph-based (HNSW), and tree-based (Annoy random projection forests). Production needs are met by lightweight vector databases (ChromaDB) and orchestration libraries (LangChain), which also enable hybrid sparse-plus-dense search via score normalization. The closing arc covers LLM-assisted hierarchical indices, where summaries at multiple levels form a tree (RAPTOR), enabling progressive top-down retrieval that scales beyond flat embedding stores.
