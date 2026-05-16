# Header Style Consistency Audit

Generated against reference files:
- `part-12-frontiers/module-63-frontier-systems-hardware/index.html`
- `part-12-frontiers/module-63-frontier-systems-hardware/section-63.1.html`
- `appendices/appendix-a-mathematical-foundations/index.html`
- `appendices/appendix-a-mathematical-foundations/section-a.1.html`

## Summary

- Files scanned: **466**
- Files with header drift: **396** (84%)
- Clean files: **70**

Top drift codes:
- `TITLE_MISSING_SUFFIX` (336 files)
- `PAGEFIND_WRONG_CHAPTER` (131 files)
- `HEADER_MISSING_BOOK_LINK` (57 files)
- `PAGEFIND_MISSING_CHAPTER` (40 files)
- `MISSING_SUBTITLE` (40 files)
- `MISSING_BREADCRUMB` (20 files)
- `PAGEFIND_MISSING_PART` (15 files)
- `UNEXPECTED_SUBTITLE` (15 files)
- `PAGEFIND_WRONG_PART` (14 files)
- `MISSING_CHAPTER_NAV` (5 files)
- `MAIN_OPENS_WITH_OTHER` (4 files)
- `BOOK_LINK_HREF` (2 files)

**Note on reference standard:** the audit found drift in the *reference* files themselves; this is significant.

- `part-12-frontiers/module-63-frontier-systems-hardware/section-63.1.html`
  - `TITLE_MISSING_SUFFIX`: <title>='Section 63.1: Beyond NVIDIA: Groq, Cerebras, Tenstorrent, AMD MI355'
- `appendices/appendix-a-mathematical-foundations/index.html`
  - `HEADER_MISSING_BOOK_LINK`: no <a class='book-title-link'> in header
  - `TITLE_MISSING_SUFFIX`: <title>='Appendix A: Mathematical Foundations'
- `appendices/appendix-a-mathematical-foundations/section-a.1.html`
  - `TITLE_MISSING_SUFFIX`: <title>='Section A.1: Linear Algebra Essentials'

## P0: Structurally broken

None.

## P1: Drift in critical elements

### `TITLE_MISSING_SUFFIX` — 336 files
- example: _<title>='Section 25.4: Models'_
- example: _<title>='Section 17.1: Principles of Synthetic Data Generation'_
- example: _<title>='Section 45.1: What Makes AI Products Different'_
  Files by group (total 336):
  - **Appendix A** (7): see Per-group findings
  - **Appendix B** (5): see Per-group findings
  - **Appendix H** (5): see Per-group findings
  - **Appendix I** (7): see Per-group findings
  - **Appendix J** (5): see Per-group findings
  - **Part 1** (32): see Per-group findings
  - **Part 10** (36): see Per-group findings
  - **Part 11** (12): see Per-group findings
  - **Part 12** (24): see Per-group findings
  - **Part 2** (36): see Per-group findings
  - **Part 3** (20): see Per-group findings
  - **Part 4** (31): see Per-group findings
  - **Part 5** (24): see Per-group findings
  - **Part 6** (25): see Per-group findings
  - **Part 7** (20): see Per-group findings
  - **Part 8** (26): see Per-group findings
  - **Part 9** (21): see Per-group findings

### `HEADER_MISSING_BOOK_LINK` — 57 files
- example: _no <a class='book-title-link'> in header_
  Files by group (total 57):
  - **Appendix A** (1): see Per-group findings
  - **Appendix B** (1): see Per-group findings
  - **Appendix C** (1): see Per-group findings
  - **Appendix D** (1): see Per-group findings
  - **Appendix E** (1): see Per-group findings
  - **Appendix H** (1): see Per-group findings
  - **Appendix I** (1): see Per-group findings
  - **Appendix J** (1): see Per-group findings
  - **Appendix K** (1): see Per-group findings
  - **Appendix L** (1): see Per-group findings
  - **Appendix M** (1): see Per-group findings
  - **Appendix N** (1): see Per-group findings
  - **Front Matter** (1): see Per-group findings
  - **Part 1** (7): see Per-group findings
  - **Part 10** (3): see Per-group findings
  - **Part 11** (1): see Per-group findings
  - **Part 12** (2): see Per-group findings
  - **Part 2** (6): see Per-group findings
  - **Part 3** (4): see Per-group findings
  - **Part 4** (5): see Per-group findings
  - **Part 5** (4): see Per-group findings
  - **Part 6** (5): see Per-group findings
  - **Part 7** (2): see Per-group findings
  - **Part 8** (3): see Per-group findings
  - **Part 9** (2): see Per-group findings

### `MISSING_BREADCRUMB` — 20 files
- example: _no <div class='page-breadcrumb'>_
  - `appendices/index.html`
  - `front-matter/about-authors.html`
  - `front-matter/copyright.html`
  - `front-matter/fm-how-to-use.html`
  - `front-matter/fm-what-this-book-covers.html`
  - `front-matter/fm-who-should-read.html`
  - `front-matter/foreword.html`
  - `front-matter/index.html`
  - `part-1-foundations/index.html`
  - `part-10-idea-to-product/index.html`
  - `part-11-applications-across-industries/index.html`
  - `part-12-frontiers/index.html`
  - `part-2-understanding-llms/index.html`
  - `part-3-working-with-llms/index.html`
  - `part-4-training-adapting/index.html`
  - `part-5-retrieval-conversation/index.html`
  - `part-6-agentic-ai/index.html`
  - `part-7-multimodal-generation/index.html`
  - `part-8-evaluation-production/index.html`
  - `part-9-safety-security-ethics/index.html`

### `MISSING_CHAPTER_NAV` — 5 files
- example: _no <nav class='chapter-nav'> at bottom_
  - `appendices/appendix-o-course-syllabi/index.html`
  - `appendices/appendix-p-reading-pathways/index.html`
  - `appendices/appendix-q-intermediate-projects/index.html`
  - `appendices/appendix-r-capstone-project/index.html`
  - `appendices/appendix-s-war-stories/index.html`

### `BOOK_LINK_HREF` — 2 files
- example: _expected '../../index.html' for depth 2, got '../index.html'_
  - `appendices/appendix-o-course-syllabi/index.html`
  - `appendices/appendix-p-reading-pathways/index.html`

## P2: Cosmetic drift

### `MISSING_SUBTITLE` — 40 files
- example: _appendix index missing <p class='chapter-subtitle'>_
- example: _chapter index missing <p class='chapter-subtitle'>_
  - **Appendix C** (1)
  - **Appendix D** (1)
  - **Appendix E** (1)
  - **Appendix K** (1)
  - **Appendix L** (1)
  - **Appendix M** (1)
  - **Appendix N** (1)
  - **Appendix O** (1)
  - **Part 1** (6)
  - **Part 10** (2)
  - **Part 12** (1)
  - **Part 2** (5)
  - **Part 3** (3)
  - **Part 4** (4)
  - **Part 5** (3)
  - **Part 6** (4)
  - **Part 7** (1)
  - **Part 8** (2)
  - **Part 9** (1)

### `UNEXPECTED_SUBTITLE` — 15 files
- example: _section page has chapter-subtitle: 'Ten debates the field resolved in 2026, and ten that remain genuinely open.'_
- example: _section page has chapter-subtitle: 'Building scalable pipelines for instruction data, conversations, and preference '_
- example: _section page has chapter-subtitle: 'Self-reflection, meta-prompting, prompt chaining, and programmatic optimization'_
  - `part-12-frontiers/module-61-frontier-architectures/section-33.11.html`
  - `part-3-working-with-llms/module-14-prompt-engineering/section-14.1.html`
  - `part-3-working-with-llms/module-14-prompt-engineering/section-14.2.html`
  - `part-3-working-with-llms/module-14-prompt-engineering/section-14.3.html`
  - `part-3-working-with-llms/module-14-prompt-engineering/section-14.4.html`
  - `part-3-working-with-llms/module-15-hybrid-ml-llm/section-15.6.html`
  - `part-4-training-adapting/module-17-synthetic-data/section-17.1.html`
  - `part-4-training-adapting/module-17-synthetic-data/section-17.2.html`
  - `part-4-training-adapting/module-17-synthetic-data/section-17.3.html`
  - `part-4-training-adapting/module-17-synthetic-data/section-17.4.html`
  - `part-4-training-adapting/module-17-synthetic-data/section-17.5.html`
  - `part-4-training-adapting/module-17-synthetic-data/section-17.6.html`
  - `part-4-training-adapting/module-17-synthetic-data/section-17.7.html`
  - `part-8-evaluation-production/module-35-production-engineering/section-35.8.html`
  - `part-8-evaluation-production/module-35-production-engineering/section-35.9.html`

### `MAIN_OPENS_WITH_OTHER` — 4 files
- example: _<main> opens with <p >_
- example: _<main> opens with <h2 >_
  - `appendices/appendix-g-problem-solution-key/index.html`
  - `appendices/appendix-q-intermediate-projects/index.html`
  - `appendices/appendix-r-capstone-project/index.html`
  - `appendices/appendix-s-war-stories/index.html`

## P3: Pagefind meta drift

### `PAGEFIND_WRONG_CHAPTER` — 131 files
- example: _chapter:'Chapter 17: Prompt Engineering &amp; Advanced Techniques' but path suggests 'Chapter 14'_
- example: _chapter:'Chapter 8: Pre-training, Scaling Laws &amp; Data Curation' but path suggests 'Chapter 7'_
- example: _chapter:'Chapter 9: Modern LLM Landscape &amp; Model Internals' but path suggests 'Chapter 8'_
- example: _chapter:'Chapter 23: Parameter-Efficient Fine-Tuning (PEFT)' but path suggests 'Chapter 19'_
- example: _chapter:'Chapter 31: AI Agent Foundations' but path suggests 'Chapter 26'_
  - **Appendix G** (1)
    - `appendices/appendix-g-problem-solution-key/index.html` — chapter:'Front Matter' but path suggests 'Appendix G'
  - **Part 12** (2)
    - `part-12-frontiers/module-61-frontier-architectures/section-33.11.html` — chapter:'Chapter 33: Emerging Architectures &amp; Scaling Frontiers' but path suggests 'Chapter 61'
    - `part-12-frontiers/module-61-frontier-architectures/section-33.4.html` — chapter:'Chapter 33: Emerging Architectures &amp; Scaling Frontiers' but path suggests 'Chapter 61'
  - **Part 2** (30)
    - `part-2-understanding-llms/module-07-pretraining-scaling-laws/index.html` — chapter:'Chapter 8: Pre-training, Scaling Laws &amp; Data Curation' but path suggests 'Chapter 7'
    - `part-2-understanding-llms/module-07-pretraining-scaling-laws/section-7.1.html` — chapter:'Chapter 8: Pre-training, Scaling Laws &amp; Data Curation' but path suggests 'Chapter 7'
    - `part-2-understanding-llms/module-07-pretraining-scaling-laws/section-7.2.html` — chapter:'Chapter 8: Pre-training, Scaling Laws &amp; Data Curation' but path suggests 'Chapter 7'
    - `part-2-understanding-llms/module-07-pretraining-scaling-laws/section-7.3.html` — chapter:'Chapter 8: Pre-training, Scaling Laws &amp; Data Curation' but path suggests 'Chapter 7'
    - `part-2-understanding-llms/module-07-pretraining-scaling-laws/section-7.4.html` — chapter:'Chapter 8: Pre-training, Scaling Laws &amp; Data Curation' but path suggests 'Chapter 7'
    - (and 25 more)
  - **Part 3** (14)
    - `part-3-working-with-llms/module-13-llm-apis/section-13.1.html` — chapter:'Chapter 15: Working with LLM APIs' but path suggests 'Chapter 13'
    - `part-3-working-with-llms/module-13-llm-apis/section-13.2.html` — chapter:'Chapter 15: Working with LLM APIs' but path suggests 'Chapter 13'
    - `part-3-working-with-llms/module-13-llm-apis/section-13.3.html` — chapter:'Chapter 15: Working with LLM APIs' but path suggests 'Chapter 13'
    - `part-3-working-with-llms/module-13-llm-apis/section-13.4.html` — chapter:'Chapter 15: Working with LLM APIs' but path suggests 'Chapter 13'
    - `part-3-working-with-llms/module-14-prompt-engineering/section-14.1.html` — chapter:'Chapter 17: Prompt Engineering &amp; Advanced Techniques' but path suggests 'Chapter 14'
    - (and 9 more)
  - **Part 4** (19)
    - `part-4-training-adapting/module-18-fine-tuning-fundamentals/section-18.1.html` — chapter:'Chapter 22: Fine-Tuning Fundamentals' but path suggests 'Chapter 18'
    - `part-4-training-adapting/module-18-fine-tuning-fundamentals/section-18.2.html` — chapter:'Chapter 22: Fine-Tuning Fundamentals' but path suggests 'Chapter 18'
    - `part-4-training-adapting/module-18-fine-tuning-fundamentals/section-18.3.html` — chapter:'Chapter 22: Fine-Tuning Fundamentals' but path suggests 'Chapter 18'
    - `part-4-training-adapting/module-18-fine-tuning-fundamentals/section-18.4.html` — chapter:'Chapter 22: Fine-Tuning Fundamentals' but path suggests 'Chapter 18'
    - `part-4-training-adapting/module-18-fine-tuning-fundamentals/section-18.5.html` — chapter:'Chapter 22: Fine-Tuning Fundamentals' but path suggests 'Chapter 18'
    - (and 14 more)
  - **Part 5** (19)
    - `part-5-retrieval-conversation/module-22-embeddings-vector-db/section-22.1.html` — chapter:'Chapter 27: Embeddings, Vector Databases &amp; Semantic Search' but path suggests 'Chapter 
    - `part-5-retrieval-conversation/module-22-embeddings-vector-db/section-22.2.html` — chapter:'Chapter 27: Embeddings, Vector Databases &amp; Semantic Search' but path suggests 'Chapter 
    - `part-5-retrieval-conversation/module-22-embeddings-vector-db/section-22.3.html` — chapter:'Chapter 27: Embeddings, Vector Databases &amp; Semantic Search' but path suggests 'Chapter 
    - `part-5-retrieval-conversation/module-22-embeddings-vector-db/section-22.4.html` — chapter:'Chapter 27: Embeddings, Vector Databases &amp; Semantic Search' but path suggests 'Chapter 
    - `part-5-retrieval-conversation/module-22-embeddings-vector-db/section-22.5.html` — chapter:'Chapter 27: Embeddings, Vector Databases &amp; Semantic Search' but path suggests 'Chapter 
    - (and 14 more)
  - **Part 6** (13)
    - `part-6-agentic-ai/module-26-ai-agents/section-26.1.html` — chapter:'Chapter 31: AI Agent Foundations' but path suggests 'Chapter 26'
    - `part-6-agentic-ai/module-26-ai-agents/section-26.2.html` — chapter:'Chapter 31: AI Agent Foundations' but path suggests 'Chapter 26'
    - `part-6-agentic-ai/module-26-ai-agents/section-26.3.html` — chapter:'Chapter 31: AI Agent Foundations' but path suggests 'Chapter 26'
    - `part-6-agentic-ai/module-26-ai-agents/section-26.4.html` — chapter:'Chapter 31: AI Agent Foundations' but path suggests 'Chapter 26'
    - `part-6-agentic-ai/module-26-ai-agents/section-26.5.html` — chapter:'Chapter 31: AI Agent Foundations' but path suggests 'Chapter 26'
    - (and 8 more)
  - **Part 8** (21)
    - `part-8-evaluation-production/module-34-evaluation-observability/section-34.1.html` — chapter:'Chapter 45: LLM Evaluation &amp; Quality Metrics' but path suggests 'Chapter 34'
    - `part-8-evaluation-production/module-34-evaluation-observability/section-34.10.html` — chapter:'Chapter 45: LLM Evaluation &amp; Quality Metrics' but path suggests 'Chapter 34'
    - `part-8-evaluation-production/module-34-evaluation-observability/section-34.11.html` — chapter:'Chapter 45: LLM Evaluation &amp; Quality Metrics' but path suggests 'Chapter 34'
    - `part-8-evaluation-production/module-34-evaluation-observability/section-34.12.html` — chapter:'Chapter 45: LLM Evaluation &amp; Quality Metrics' but path suggests 'Chapter 34'
    - `part-8-evaluation-production/module-34-evaluation-observability/section-34.2.html` — chapter:'Chapter 45: LLM Evaluation &amp; Quality Metrics' but path suggests 'Chapter 34'
    - (and 16 more)
  - **Part 9** (12)
    - `part-9-safety-security-ethics/module-37-safety-ethics-regulation/section-37.1.html` — chapter:'Chapter 52: Safety, Ethics &amp; Regulation' but path suggests 'Chapter 37'
    - `part-9-safety-security-ethics/module-37-safety-ethics-regulation/section-37.10.html` — chapter:'Chapter 52: Safety, Ethics &amp; Regulation' but path suggests 'Chapter 37'
    - `part-9-safety-security-ethics/module-37-safety-ethics-regulation/section-37.11.html` — chapter:'Chapter 52: Safety, Ethics &amp; Regulation' but path suggests 'Chapter 37'
    - `part-9-safety-security-ethics/module-37-safety-ethics-regulation/section-37.12.html` — chapter:'Chapter 52: Safety, Ethics &amp; Regulation' but path suggests 'Chapter 37'
    - `part-9-safety-security-ethics/module-37-safety-ethics-regulation/section-37.2.html` — chapter:'Chapter 52: Safety, Ethics &amp; Regulation' but path suggests 'Chapter 37'
    - (and 7 more)

### `PAGEFIND_MISSING_CHAPTER` — 40 files
- example: _no pagefind-meta-injected span for chapter_
  - **Appendices** (1)
    - `appendices/index.html` — no pagefind-meta-injected span for chapter
  - **Appendix A** (1)
    - `appendices/appendix-a-mathematical-foundations/section-a.6.html` — no pagefind-meta-injected span for chapter
  - **Front Matter** (2)
    - `front-matter/copyright.html` — no pagefind-meta-injected span for chapter
    - `front-matter/index.html` — no pagefind-meta-injected span for chapter
  - **Part 1** (1)
    - `part-1-foundations/index.html` — no pagefind-meta-injected span for chapter
  - **Part 10** (1)
    - `part-10-idea-to-product/index.html` — no pagefind-meta-injected span for chapter
  - **Part 11** (1)
    - `part-11-applications-across-industries/index.html` — no pagefind-meta-injected span for chapter
  - **Part 12** (2)
    - `part-12-frontiers/index.html` — no pagefind-meta-injected span for chapter
    - `part-12-frontiers/module-61-frontier-architectures/index.html` — no pagefind-meta-injected span for chapter
  - **Part 2** (6)
    - `part-2-understanding-llms/index.html` — no pagefind-meta-injected span for chapter
    - `part-2-understanding-llms/module-07-pretraining-scaling-laws/section-7.9.html` — no pagefind-meta-injected span for chapter
    - `part-2-understanding-llms/module-08-modern-llm-landscape/index.html` — no pagefind-meta-injected span for chapter
    - `part-2-understanding-llms/module-09-reasoning-test-time-compute/index.html` — no pagefind-meta-injected span for chapter
    - `part-2-understanding-llms/module-10-inference-optimization/index.html` — no pagefind-meta-injected span for chapter
    - (and 1 more)
  - **Part 3** (4)
    - `part-3-working-with-llms/index.html` — no pagefind-meta-injected span for chapter
    - `part-3-working-with-llms/module-13-llm-apis/index.html` — no pagefind-meta-injected span for chapter
    - `part-3-working-with-llms/module-14-prompt-engineering/index.html` — no pagefind-meta-injected span for chapter
    - `part-3-working-with-llms/module-15-hybrid-ml-llm/index.html` — no pagefind-meta-injected span for chapter
  - **Part 4** (5)
    - `part-4-training-adapting/index.html` — no pagefind-meta-injected span for chapter
    - `part-4-training-adapting/module-17-synthetic-data/index.html` — no pagefind-meta-injected span for chapter
    - `part-4-training-adapting/module-18-fine-tuning-fundamentals/index.html` — no pagefind-meta-injected span for chapter
    - `part-4-training-adapting/module-19-peft/index.html` — no pagefind-meta-injected span for chapter
    - `part-4-training-adapting/module-20-alignment-rlhf-dpo/index.html` — no pagefind-meta-injected span for chapter
  - **Part 5** (4)
    - `part-5-retrieval-conversation/index.html` — no pagefind-meta-injected span for chapter
    - `part-5-retrieval-conversation/module-22-embeddings-vector-db/index.html` — no pagefind-meta-injected span for chapter
    - `part-5-retrieval-conversation/module-23-rag/index.html` — no pagefind-meta-injected span for chapter
    - `part-5-retrieval-conversation/module-24-conversational-ai/index.html` — no pagefind-meta-injected span for chapter
  - **Part 6** (5)
    - `part-6-agentic-ai/index.html` — no pagefind-meta-injected span for chapter
    - `part-6-agentic-ai/module-26-ai-agents/index.html` — no pagefind-meta-injected span for chapter
    - `part-6-agentic-ai/module-27-tool-use-protocols/index.html` — no pagefind-meta-injected span for chapter
    - `part-6-agentic-ai/module-28-multi-agent-systems/index.html` — no pagefind-meta-injected span for chapter
    - `part-6-agentic-ai/module-29-specialized-agents/index.html` — no pagefind-meta-injected span for chapter
  - **Part 7** (2)
    - `part-7-multimodal-generation/index.html` — no pagefind-meta-injected span for chapter
    - `part-7-multimodal-generation/module-31-multimodal/index.html` — no pagefind-meta-injected span for chapter
  - **Part 8** (3)
    - `part-8-evaluation-production/index.html` — no pagefind-meta-injected span for chapter
    - `part-8-evaluation-production/module-34-evaluation-observability/index.html` — no pagefind-meta-injected span for chapter
    - `part-8-evaluation-production/module-35-production-engineering/index.html` — no pagefind-meta-injected span for chapter
  - **Part 9** (2)
    - `part-9-safety-security-ethics/index.html` — no pagefind-meta-injected span for chapter
    - `part-9-safety-security-ethics/module-37-safety-ethics-regulation/index.html` — no pagefind-meta-injected span for chapter

### `PAGEFIND_MISSING_PART` — 15 files
- example: _no pagefind-meta-injected span for part_
  - `appendices/appendix-a-mathematical-foundations/section-a.6.html` — no pagefind-meta-injected span for part
  - `appendices/index.html` — no pagefind-meta-injected span for part
  - `part-1-foundations/index.html` — no pagefind-meta-injected span for part
  - `part-10-idea-to-product/index.html` — no pagefind-meta-injected span for part
  - `part-11-applications-across-industries/index.html` — no pagefind-meta-injected span for part
  - `part-12-frontiers/index.html` — no pagefind-meta-injected span for part
  - `part-2-understanding-llms/index.html` — no pagefind-meta-injected span for part
  - `part-2-understanding-llms/module-07-pretraining-scaling-laws/section-7.9.html` — no pagefind-meta-injected span for part
  - `part-3-working-with-llms/index.html` — no pagefind-meta-injected span for part
  - `part-4-training-adapting/index.html` — no pagefind-meta-injected span for part
  - `part-5-retrieval-conversation/index.html` — no pagefind-meta-injected span for part
  - `part-6-agentic-ai/index.html` — no pagefind-meta-injected span for part
  - `part-7-multimodal-generation/index.html` — no pagefind-meta-injected span for part
  - `part-8-evaluation-production/index.html` — no pagefind-meta-injected span for part
  - `part-9-safety-security-ethics/index.html` — no pagefind-meta-injected span for part

### `PAGEFIND_WRONG_PART` — 14 files
- example: _part:'Part XI: From Idea to Product' but path suggests 'Part X'_
- example: _part:'Part XII: Frontiers' but path suggests 'Part VI'_
  - `part-10-idea-to-product/module-45-prototype-to-production/index.html` — part:'Part XI: From Idea to Product' but path suggests 'Part X'
  - `part-10-idea-to-product/module-45-prototype-to-production/section-45.1.html` — part:'Part XI: From Idea to Product' but path suggests 'Part X'
  - `part-10-idea-to-product/module-45-prototype-to-production/section-45.2.html` — part:'Part XI: From Idea to Product' but path suggests 'Part X'
  - `part-10-idea-to-product/module-45-prototype-to-production/section-45.3.html` — part:'Part XI: From Idea to Product' but path suggests 'Part X'
  - `part-10-idea-to-product/module-45-prototype-to-production/section-45.4.html` — part:'Part XI: From Idea to Product' but path suggests 'Part X'
  - `part-10-idea-to-product/module-45-prototype-to-production/section-45.5.html` — part:'Part XI: From Idea to Product' but path suggests 'Part X'
  - `part-10-idea-to-product/module-45-prototype-to-production/section-45.6.html` — part:'Part XI: From Idea to Product' but path suggests 'Part X'
  - `part-10-idea-to-product/module-45-prototype-to-production/section-45.7.html` — part:'Part XI: From Idea to Product' but path suggests 'Part X'
  - `part-10-idea-to-product/module-48-shipping-deploying/index.html` — part:'Part XI: From Idea to Product' but path suggests 'Part X'
  - `part-10-idea-to-product/module-48-shipping-deploying/section-48.1.html` — part:'Part XI: From Idea to Product' but path suggests 'Part X'
  - `part-10-idea-to-product/module-48-shipping-deploying/section-48.2.html` — part:'Part XI: From Idea to Product' but path suggests 'Part X'
  - `part-10-idea-to-product/module-48-shipping-deploying/section-48.3.html` — part:'Part XI: From Idea to Product' but path suggests 'Part X'
  - `part-10-idea-to-product/module-48-shipping-deploying/section-48.4.html` — part:'Part XI: From Idea to Product' but path suggests 'Part X'
  - `part-6-agentic-ai/module-27-tool-use-protocols/section-27.6.html` — part:'Part XII: Frontiers' but path suggests 'Part VI'

## Per-group findings

### Front Matter
- Files: 7, with drift: 7
- Top issues: `MISSING_BREADCRUMB` (7), `PAGEFIND_MISSING_CHAPTER` (2), `HEADER_MISSING_BOOK_LINK` (1)

### Part 1
- Files: 36, with drift: 33
- Top issues: `TITLE_MISSING_SUFFIX` (32), `HEADER_MISSING_BOOK_LINK` (7), `MISSING_SUBTITLE` (6), `MISSING_BREADCRUMB` (1), `PAGEFIND_MISSING_PART` (1), `PAGEFIND_MISSING_CHAPTER` (1)

### Part 2
- Files: 42, with drift: 41
- Top issues: `TITLE_MISSING_SUFFIX` (36), `PAGEFIND_WRONG_CHAPTER` (30), `HEADER_MISSING_BOOK_LINK` (6), `PAGEFIND_MISSING_CHAPTER` (6), `MISSING_SUBTITLE` (5), `PAGEFIND_MISSING_PART` (2), `MISSING_BREADCRUMB` (1)

### Part 3
- Files: 25, with drift: 24
- Top issues: `TITLE_MISSING_SUFFIX` (20), `PAGEFIND_WRONG_CHAPTER` (14), `UNEXPECTED_SUBTITLE` (5), `HEADER_MISSING_BOOK_LINK` (4), `PAGEFIND_MISSING_CHAPTER` (4), `MISSING_SUBTITLE` (3), `MISSING_BREADCRUMB` (1), `PAGEFIND_MISSING_PART` (1)

### Part 4
- Files: 37, with drift: 36
- Top issues: `TITLE_MISSING_SUFFIX` (31), `PAGEFIND_WRONG_CHAPTER` (19), `UNEXPECTED_SUBTITLE` (7), `HEADER_MISSING_BOOK_LINK` (5), `PAGEFIND_MISSING_CHAPTER` (5), `MISSING_SUBTITLE` (4), `MISSING_BREADCRUMB` (1), `PAGEFIND_MISSING_PART` (1)

### Part 5
- Files: 29, with drift: 28
- Top issues: `TITLE_MISSING_SUFFIX` (24), `PAGEFIND_WRONG_CHAPTER` (19), `HEADER_MISSING_BOOK_LINK` (4), `PAGEFIND_MISSING_CHAPTER` (4), `MISSING_SUBTITLE` (3), `MISSING_BREADCRUMB` (1), `PAGEFIND_MISSING_PART` (1)

### Part 6
- Files: 31, with drift: 30
- Top issues: `TITLE_MISSING_SUFFIX` (25), `PAGEFIND_WRONG_CHAPTER` (13), `HEADER_MISSING_BOOK_LINK` (5), `PAGEFIND_MISSING_CHAPTER` (5), `MISSING_SUBTITLE` (4), `MISSING_BREADCRUMB` (1), `PAGEFIND_MISSING_PART` (1), `PAGEFIND_WRONG_PART` (1)

### Part 7
- Files: 24, with drift: 22
- Top issues: `TITLE_MISSING_SUFFIX` (20), `HEADER_MISSING_BOOK_LINK` (2), `PAGEFIND_MISSING_CHAPTER` (2), `MISSING_BREADCRUMB` (1), `PAGEFIND_MISSING_PART` (1), `MISSING_SUBTITLE` (1)

### Part 8
- Files: 30, with drift: 29
- Top issues: `TITLE_MISSING_SUFFIX` (26), `PAGEFIND_WRONG_CHAPTER` (21), `HEADER_MISSING_BOOK_LINK` (3), `PAGEFIND_MISSING_CHAPTER` (3), `MISSING_SUBTITLE` (2), `UNEXPECTED_SUBTITLE` (2), `MISSING_BREADCRUMB` (1), `PAGEFIND_MISSING_PART` (1)

### Part 9
- Files: 25, with drift: 23
- Top issues: `TITLE_MISSING_SUFFIX` (21), `PAGEFIND_WRONG_CHAPTER` (12), `HEADER_MISSING_BOOK_LINK` (2), `PAGEFIND_MISSING_CHAPTER` (2), `MISSING_BREADCRUMB` (1), `PAGEFIND_MISSING_PART` (1), `MISSING_SUBTITLE` (1)

### Part 10
- Files: 49, with drift: 40
- Top issues: `TITLE_MISSING_SUFFIX` (36), `PAGEFIND_WRONG_PART` (13), `HEADER_MISSING_BOOK_LINK` (3), `MISSING_SUBTITLE` (2), `MISSING_BREADCRUMB` (1), `PAGEFIND_MISSING_PART` (1), `PAGEFIND_MISSING_CHAPTER` (1)

### Part 11
- Files: 23, with drift: 13
- Top issues: `TITLE_MISSING_SUFFIX` (12), `HEADER_MISSING_BOOK_LINK` (1), `MISSING_BREADCRUMB` (1), `PAGEFIND_MISSING_PART` (1), `PAGEFIND_MISSING_CHAPTER` (1)

### Part 12
- Files: 31, with drift: 27
- Top issues: `TITLE_MISSING_SUFFIX` (24), `HEADER_MISSING_BOOK_LINK` (2), `PAGEFIND_MISSING_CHAPTER` (2), `PAGEFIND_WRONG_CHAPTER` (2), `MISSING_BREADCRUMB` (1), `PAGEFIND_MISSING_PART` (1), `MISSING_SUBTITLE` (1), `UNEXPECTED_SUBTITLE` (1)

### Appendix A
- Files: 7, with drift: 7
- Top issues: `TITLE_MISSING_SUFFIX` (7), `HEADER_MISSING_BOOK_LINK` (1), `PAGEFIND_MISSING_PART` (1), `PAGEFIND_MISSING_CHAPTER` (1)

### Appendix B
- Files: 5, with drift: 5
- Top issues: `TITLE_MISSING_SUFFIX` (5), `HEADER_MISSING_BOOK_LINK` (1)

### Appendix C
- Files: 6, with drift: 1
- Top issues: `HEADER_MISSING_BOOK_LINK` (1), `MISSING_SUBTITLE` (1)

### Appendix D
- Files: 6, with drift: 1
- Top issues: `HEADER_MISSING_BOOK_LINK` (1), `MISSING_SUBTITLE` (1)

### Appendix E
- Files: 2, with drift: 1
- Top issues: `HEADER_MISSING_BOOK_LINK` (1), `MISSING_SUBTITLE` (1)

### Appendix F
- Files: 2, with drift: 0

### Appendix G
- Files: 1, with drift: 1
- Top issues: `MAIN_OPENS_WITH_OTHER` (1), `PAGEFIND_WRONG_CHAPTER` (1)

### Appendix H
- Files: 5, with drift: 5
- Top issues: `TITLE_MISSING_SUFFIX` (5), `HEADER_MISSING_BOOK_LINK` (1)

### Appendix I
- Files: 7, with drift: 7
- Top issues: `TITLE_MISSING_SUFFIX` (7), `HEADER_MISSING_BOOK_LINK` (1)

### Appendix J
- Files: 5, with drift: 5
- Top issues: `TITLE_MISSING_SUFFIX` (5), `HEADER_MISSING_BOOK_LINK` (1)

### Appendix K
- Files: 6, with drift: 1
- Top issues: `HEADER_MISSING_BOOK_LINK` (1), `MISSING_SUBTITLE` (1)

### Appendix L
- Files: 6, with drift: 1
- Top issues: `HEADER_MISSING_BOOK_LINK` (1), `MISSING_SUBTITLE` (1)

### Appendix M
- Files: 8, with drift: 1
- Top issues: `HEADER_MISSING_BOOK_LINK` (1), `MISSING_SUBTITLE` (1)

### Appendix N
- Files: 5, with drift: 1
- Top issues: `HEADER_MISSING_BOOK_LINK` (1), `MISSING_SUBTITLE` (1)

### Appendix O
- Files: 1, with drift: 1
- Top issues: `BOOK_LINK_HREF` (1), `MISSING_SUBTITLE` (1), `MISSING_CHAPTER_NAV` (1)

### Appendix P
- Files: 1, with drift: 1
- Top issues: `BOOK_LINK_HREF` (1), `MISSING_CHAPTER_NAV` (1)

### Appendix Q
- Files: 1, with drift: 1
- Top issues: `MAIN_OPENS_WITH_OTHER` (1), `MISSING_CHAPTER_NAV` (1)

### Appendix R
- Files: 1, with drift: 1
- Top issues: `MAIN_OPENS_WITH_OTHER` (1), `MISSING_CHAPTER_NAV` (1)

### Appendix S
- Files: 1, with drift: 1
- Top issues: `MAIN_OPENS_WITH_OTHER` (1), `MISSING_CHAPTER_NAV` (1)

### Appendices
- Files: 1, with drift: 1
- Top issues: `MISSING_BREADCRUMB` (1), `PAGEFIND_MISSING_PART` (1), `PAGEFIND_MISSING_CHAPTER` (1)
