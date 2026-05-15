# ToC and Navigation Audit

_Generated: 2026-05-15_

_Repository: `E:/Projects/BookBlogsHome/LLMBook`_

## Scope

- Total HTML pages scanned: **389**
- Section pages (section-*.html): 298
- Index pages (index.html): 82
- ToC source: `toc.html` (474 link entries indexed)

## Header Navigation Issues

- Pages missing `<nav class="header-nav">`: **1**

First missing:
  - `index.html`

- Broken header-nav anchor targets: **0**

## Chapter Navigation Issues

- Section/module-index pages missing `<nav class="chapter-nav">`: **0**

- Pages with partial chapter-nav (missing prev/up/next anchor): **0**

- Broken chapter-nav targets (prev/up/next -> 404): **0**

- Asymmetric prev/next chains (A.next != B and B.prev != A): **9**
  - prev/next: `appendices/appendix-a-mathematical-foundations/index.html` -> `part-4-training-adapting/module-17-alignment-rlhf-dpo/section-17.5.html` (back: `part-5-retrieval-conversation/module-18-embeddings-vector-db/index.html`)
  - next/prev: `appendices/appendix-ak-course-syllabi/index.html` -> `capstone/index.html` (back: `appendices/appendix-ai-freshness-2026/index.html`)
  - next/prev: `appendices/appendix-t-distributed-ml/section-t.7.html` -> `appendices/appendix-u-docker-containers/section-u.1.html` (back: `appendices/appendix-u-docker-containers/index.html`)
  - prev/next: `appendices/appendix-u-docker-containers/index.html` -> `appendices/appendix-t-distributed-ml/section-t.7.html` (back: `appendices/appendix-u-docker-containers/section-u.1.html`)
  - next/prev: `appendices/appendix-v-tooling-ecosystem/section-v.3.html` -> `appendices/appendix-w-legal-llms/index.html` (back: `appendices/appendix-v-tooling-ecosystem/index.html`)
  - prev/next: `appendices/appendix-w-legal-llms/index.html` -> `appendices/appendix-v-tooling-ecosystem/index.html` (back: `appendices/appendix-v-tooling-ecosystem/section-v.1.html`)
  - next/prev: `appendices/index.html` -> `appendices/appendix-a-mathematical-foundations/index.html` (back: `part-4-training-adapting/module-17-alignment-rlhf-dpo/section-17.5.html`)
  - prev/next: `capstone/index.html` -> `appendices/appendix-ai-freshness-2026/index.html` (back: `appendices/appendix-aj-reading-pathways/index.html`)
  - next/prev: `part-11-idea-to-product/module-35-shipping-scaling/section-35.4.html` -> `part-2-understanding-llms/module-06-pretraining-scaling-laws/index.html` (back: `part-1-foundations/module-05-decoding-text-generation/section-5.4.html`)

## Table of Contents Issues

- Broken ToC links (point to non-existent files): **0**

- Section files NOT referenced in ToC (orphaned sections): **1**
  - `appendices/appendix-a-mathematical-foundations/section-a.6.html`

- Module/Appendix index files NOT referenced in ToC: **0**

- Probable ToC title vs page-title mismatches: **3**

_(Heuristic: text shown in ToC does not overlap with the page h1/title.)_
  - [short] `appendices/appendix-l-langchain/index.html` chip="L"
    - ToC anchor : "LangChain (with LlamaIndex, LangGraph, CrewAI, Semantic Kernel, DSPy)"
    - Page title : "LangChain"
  - [short] `capstone/index.html` chip=""
    - ToC anchor : "Capstone Project"
    - Page title : "End-to-End LLM System"
  - [detailed] `appendices/appendix-l-langchain/index.html` chip="App L"
    - ToC anchor : "LangChain: Chains, Agents, and Retrieval"
    - Page title : "LangChain"

## Recommendation Priority

- Total issues detected: **14**

- **P1** Add missing `<nav class="header-nav">` to 1 page(s).
- **P2** Decide whether to add 1 unreferenced section file(s) to the ToC, or delete them.
- **P2** Reconcile 9 asymmetric prev/next chain(s).
- **P3** Review 3 probable ToC title vs page-title mismatch(es).
