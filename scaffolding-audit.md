# Pedagogical Scaffolding Audit

Audit of the seven canonical scaffolding blocks on every chapter landing page (`part-N-*/module-NN-*/index.html`), plus a lighter audit of front-matter and appendix pages.

- Main chapters audited: **42**
- Front-matter pages audited: **10**
- Appendix pages audited: **22**

Legend (per-chapter table): `OK` = present, `MISS` = missing, `EMPTY` = present but <30 chars meaningful content, `ALT` = uses alternate class name (flagged for normalization).

## 1. Summary: Block Coverage Across Main Chapters

| Block | Total | Present | Missing | Empty | Alt-class |
|---|---:|---:|---:|---:|---:|
| Looking Back | 42 | 35 | 7 | 0 | 0 |
| Overview | 42 | 35 | 7 | 0 | 0 |
| Big Picture | 42 | 35 | 7 | 0 | 0 |
| Objectives | 42 | 33 | 9 | 0 | 0 |
| Prereqs | 42 | 35 | 7 | 0 | 0 |
| Sections | 42 | 35 | 7 | 0 | 0 |
| What's Next? | 42 | 35 | 7 | 0 | 0 |

**Headline missing-block counts (across all main chapters):**

- Looking Back: **7 missing**, 0 empty, 0 using alternate class
- Overview: **7 missing**, 0 empty, 0 using alternate class
- Big Picture: **7 missing**, 0 empty, 0 using alternate class
- Objectives: **9 missing**, 0 empty, 0 using alternate class
- Prereqs: **7 missing**, 0 empty, 0 using alternate class
- Sections: **7 missing**, 0 empty, 0 using alternate class
- What's Next?: **7 missing**, 0 empty, 0 using alternate class

## 2. Per-Chapter Checklist

| Part | Ch | Title | Looking Back | Overview | Big Picture | Objectives | Prereqs | Sections | What's Next? |
|---:|---:|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| 1 | 0 | ML and PyTorch Foundations | OK | OK | MISS | OK | OK | OK | OK |
| 1 | 1 | Foundations of NLP & Text Representation | OK | OK | MISS | OK | OK | OK | OK |
| 1 | 2 | Tokenization and Subword Models | OK | OK | MISS | OK | OK | OK | OK |
| 1 | 3 | Sequence Models & the Attention Mechanism | OK | OK | MISS | OK | OK | OK | OK |
| 1 | 4 | The Transformer Architecture | OK | OK | MISS | OK | OK | OK | OK |
| 1 | 5 | Decoding Strategies & Text Generation | OK | OK | MISS | OK | OK | OK | OK |
| 2 | 6 | Pre-training, Scaling Laws & Data Curation | OK | OK | MISS | OK | OK | OK | OK |
| 2 | 7 | Modern LLM Landscape & Model Internals | OK | OK | OK | OK | OK | OK | OK |
| 2 | 8 | Reasoning Models & Test-Time Compute | OK | OK | OK | OK | OK | OK | OK |
| 2 | 9 | Inference Optimization & Efficient Serving | OK | OK | OK | OK | OK | OK | OK |
| 2 | 10 | Interpretability & Mechanistic Understanding | OK | OK | OK | OK | OK | OK | OK |
| 3 | 11 | Working with LLM APIs | OK | OK | OK | OK | OK | OK | OK |
| 3 | 12 | Prompt Engineering & Advanced Techniques | OK | OK | OK | OK | OK | OK | OK |
| 3 | 13 | Hybrid ML+LLM Architectures & Decision Frameworks | OK | OK | OK | OK | OK | OK | OK |
| 4 | 14 | Synthetic Data Generation & LLM Simulation | OK | OK | OK | OK | OK | OK | OK |
| 4 | 15 | Fine-Tuning Fundamentals | OK | OK | OK | OK | OK | OK | OK |
| 4 | 16 | Parameter-Efficient Fine-Tuning (PEFT) | OK | OK | OK | OK | OK | OK | OK |
| 4 | 17 | Alignment: RLHF, DPO & Preference Tuning | OK | OK | OK | OK | OK | OK | OK |
| 5 | 18 | Embeddings, Vector Databases & Semantic Search | OK | OK | OK | OK | OK | OK | OK |
| 5 | 19 | Retrieval-Augmented Generation (RAG) | OK | OK | OK | OK | OK | OK | OK |
| 5 | 20 | Building Conversational AI Systems | OK | OK | OK | OK | OK | OK | OK |
| 6 | 21 | AI Agent Foundations | OK | OK | OK | OK | OK | OK | OK |
| 6 | 22 | Tool Use, Function Calling & Protocols | OK | OK | OK | OK | OK | OK | OK |
| 6 | 23 | Multi-Agent Systems | OK | OK | OK | OK | OK | OK | OK |
| 6 | 24 | Specialized Agents | OK | OK | OK | OK | OK | OK | OK |
| 6 | 25 | Agent Safety, Production & Operations | OK | OK | OK | OK | OK | OK | OK |
| 7 | 26 | Multimodal Generation | OK | OK | OK | OK | OK | OK | OK |
| 7 | 27 | LLM Applications Across Industries | OK | OK | OK | OK | OK | OK | OK |
| 8 | 28 | LLM Evaluation & Quality Metrics | OK | OK | OK | OK | OK | OK | OK |
| 8 | 29 | LLMOps & Deployment Engineering | OK | OK | OK | OK | OK | OK | OK |
| 9 | 30 | Safety, Ethics & Regulation | OK | OK | OK | OK | OK | OK | OK |
| 9 | 31 | LLM Strategy, Product Management & ROI | OK | OK | OK | OK | OK | OK | OK |
| 10 | 33 | Emerging Architectures & Scaling Frontiers | OK | OK | OK | OK | OK | OK | OK |
| 11 | 34 | From Idea to Product Hypothesis | OK | OK | OK | MISS | OK | OK | OK |
| 11 | 35 | Shipping and Scaling AI Products | OK | OK | OK | MISS | OK | OK | OK |
| 12 | 36 | LLMs in Legal Practice | MISS | MISS | OK | MISS | MISS | MISS | MISS |
| 12 | 37 | LLMs in Finance | MISS | MISS | OK | MISS | MISS | MISS | MISS |
| 12 | 38 | LLMs in Healthcare & Biomedical | MISS | MISS | OK | MISS | MISS | MISS | MISS |
| 12 | 39 | LLMs in Education | MISS | MISS | OK | MISS | MISS | MISS | MISS |
| 12 | 40 | LLMs in Cybersecurity | MISS | MISS | OK | MISS | MISS | MISS | MISS |
| 12 | 41 | LLMs in Government & Public Sector | MISS | MISS | OK | MISS | MISS | MISS | MISS |
| 12 | 42 | LLMs in Manufacturing & Supply Chain | MISS | MISS | OK | MISS | MISS | MISS | MISS |

## 3. Empty / Near-Empty Blocks

_No empty blocks detected._

## 4. Out-of-Order Chapters

Expected order: Looking Back -> Overview -> Big Picture -> Objectives -> Prereqs -> Sections -> What's Next?

- **Ch 0** (part-1-foundations/module-00-ml-pytorch-foundations/index.html:36)
    - Actual order: looking_back -> overview -> prereqs -> objectives -> sections -> whats_next; expected: looking_back -> overview -> objectives -> prereqs -> sections -> whats_next
    - Line locations: Looking Back L36; Overview L40; Objectives L70; Prereqs L61; Sections L80; What's Next? L135
- **Ch 1** (part-1-foundations/module-01-foundations-nlp-text-representation/index.html:32)
    - Actual order: looking_back -> overview -> prereqs -> objectives -> sections -> whats_next; expected: looking_back -> overview -> objectives -> prereqs -> sections -> whats_next
    - Line locations: Looking Back L32; Overview L36; Objectives L67; Prereqs L58; Sections L80; What's Next? L132
- **Ch 2** (part-1-foundations/module-02-tokenization-subword-models/index.html:36)
    - Actual order: looking_back -> overview -> prereqs -> objectives -> sections -> whats_next; expected: looking_back -> overview -> objectives -> prereqs -> sections -> whats_next
    - Line locations: Looking Back L36; Overview L40; Objectives L68; Prereqs L59; Sections L80; What's Next? L120
- **Ch 3** (part-1-foundations/module-03-sequence-models-attention/index.html:45)
    - Actual order: looking_back -> overview -> prereqs -> objectives -> sections -> whats_next; expected: looking_back -> overview -> objectives -> prereqs -> sections -> whats_next
    - Line locations: Looking Back L45; Overview L49; Objectives L78; Prereqs L69; Sections L90; What's Next? L128
- **Ch 4** (part-1-foundations/module-04-transformer-architecture/index.html:36)
    - Actual order: looking_back -> overview -> prereqs -> objectives -> sections -> whats_next; expected: looking_back -> overview -> objectives -> prereqs -> sections -> whats_next
    - Line locations: Looking Back L36; Overview L40; Objectives L66; Prereqs L56; Sections L79; What's Next? L145
- **Ch 5** (part-1-foundations/module-05-decoding-text-generation/index.html:36)
    - Actual order: looking_back -> overview -> prereqs -> objectives -> sections -> whats_next; expected: looking_back -> overview -> objectives -> prereqs -> sections -> whats_next
    - Line locations: Looking Back L36; Overview L40; Objectives L64; Prereqs L56; Sections L76; What's Next? L127
- **Ch 6** (part-2-understanding-llms/module-06-pretraining-scaling-laws/index.html:36)
    - Actual order: looking_back -> overview -> prereqs -> objectives -> sections -> whats_next; expected: looking_back -> overview -> objectives -> prereqs -> sections -> whats_next
    - Line locations: Looking Back L36; Overview L40; Objectives L69; Prereqs L59; Sections L82; What's Next? L174
- **Ch 7** (part-2-understanding-llms/module-07-modern-llm-landscape/index.html:35)
    - Actual order: looking_back -> overview -> big_picture -> prereqs -> objectives -> sections -> whats_next; expected: looking_back -> overview -> big_picture -> objectives -> prereqs -> sections -> whats_next
    - Line locations: Looking Back L35; Overview L39; Big Picture L60; Objectives L73; Prereqs L64; Sections L86; What's Next? L126
- **Ch 8** (part-2-understanding-llms/module-08-reasoning-test-time-compute/index.html:31)
    - Actual order: looking_back -> overview -> big_picture -> prereqs -> objectives -> sections -> whats_next; expected: looking_back -> overview -> big_picture -> objectives -> prereqs -> sections -> whats_next
    - Line locations: Looking Back L31; Overview L35; Big Picture L60; Objectives L73; Prereqs L63; Sections L86; What's Next? L130
- **Ch 9** (part-2-understanding-llms/module-09-inference-optimization/index.html:39)
    - Actual order: looking_back -> overview -> big_picture -> prereqs -> objectives -> sections -> whats_next; expected: looking_back -> overview -> big_picture -> objectives -> prereqs -> sections -> whats_next
    - Line locations: Looking Back L39; Overview L43; Big Picture L66; Objectives L80; Prereqs L70; Sections L93; What's Next? L172
- **Ch 10** (part-2-understanding-llms/module-10-interpretability/index.html:35)
    - Actual order: looking_back -> overview -> big_picture -> prereqs -> objectives -> sections -> whats_next; expected: looking_back -> overview -> big_picture -> objectives -> prereqs -> sections -> whats_next
    - Line locations: Looking Back L35; Overview L39; Big Picture L65; Objectives L78; Prereqs L68; Sections L93; What's Next? L138

## 5. Alternate Class Names (Flagged for Normalization)

_No chapters using alternate class names._

## 6. Front Matter + Appendices (Lighter Criteria)

Lighter criteria: each page should have an `<h1>` plus an intro paragraph (>= 30 chars). Bare pages (h1 with no intro and no sections list) are flagged.

### Front Matter

| File | H1 | Intro (chars) | Sections list | Chapter-nav | Bare? |
|---|:-:|---:|:-:|:-:|:-:|
| front-matter/about-authors.html | OK | 542 | - | OK | - |
| front-matter/copyright.html | OK | 449 | - | OK | - |
| front-matter/fm-course-syllabi.html | OK | 392 | - | OK | - |
| front-matter/fm-how-to-use.html | OK | 668 | - | OK | - |
| front-matter/fm-reading-pathways.html | OK | 265 | - | OK | - |
| front-matter/fm-what-this-book-covers.html | OK | 630 | - | OK | - |
| front-matter/fm-who-should-read.html | OK | 628 | - | OK | - |
| front-matter/foreword.html | OK | 574 | - | OK | - |
| front-matter/index.html | OK | 263 | OK | OK | - |
| front-matter/look-inside-preview.html | OK | 371 | - | OK | - |

### Appendices + Glossary

| File | H1 | Intro (chars) | Sections list | Chapter-nav | Bare? |
|---|:-:|---:|:-:|:-:|:-:|
| appendices/appendix-a-mathematical-foundations/index.html | OK | 550 | OK | OK | - |
| appendices/appendix-b-ml-essentials/index.html | OK | 408 | OK | OK | - |
| appendices/appendix-c-python-for-llm/index.html | OK | 476 | OK | OK | - |
| appendices/appendix-d-environment-setup/index.html | OK | 449 | OK | OK | - |
| appendices/appendix-e-git-collaboration/index.html | OK | 558 | OK | OK | - |
| appendices/appendix-f-hardware-compute/index.html | OK | 452 | OK | OK | - |
| appendices/appendix-g-model-cards/index.html | OK | 477 | OK | OK | - |
| appendices/appendix-h-prompt-templates/index.html | OK | 441 | OK | OK | - |
| appendices/appendix-i-datasets-benchmarks/index.html | OK | 503 | OK | OK | - |
| appendices/appendix-j-huggingface-ecosystem/index.html | OK | 455 | OK | OK | - |
| appendices/appendix-k-langchain/index.html | OK | 444 | OK | OK | - |
| appendices/appendix-l-experiment-tracking/index.html | OK | 461 | OK | OK | - |
| appendices/appendix-m-inference-serving/index.html | OK | 613 | OK | OK | - |
| appendices/appendix-n-distributed-ml/index.html | OK | 580 | OK | OK | - |
| appendices/appendix-o-docker-containers/index.html | OK | 502 | OK | OK | - |
| appendices/appendix-p-tooling-ecosystem/index.html | OK | 558 | OK | OK | - |
| appendices/appendix-q-master-reference-tables/index.html | OK | 443 | - | OK | - |
| appendices/appendix-r-production-patterns/index.html | OK | 359 | - | OK | - |
| appendices/appendix-s-pedagogy-kit/index.html | OK | 397 | - | OK | - |
| appendices/appendix-t-problem-solution-key/index.html | OK | 369 | - | OK | - |
| appendices/appendix-u-freshness-2026/index.html | OK | 349 | - | OK | - |
| appendices/glossary/index.html | OK | 497 | OK | OK | - |

## 7. Recommended Fix Priority

- **Add the most commonly missing block first:** top three deficits are Objectives (9 chapters); Looking Back (7 chapters); Overview (7 chapters). Adding Big Picture (missing on Part 1 chapters 0 to 5 plus Chapter 6) and re-adding the five missing blocks on Part 12 industry chapters delivers the largest per-chapter improvement.
- **Re-order misordered scaffolding** in 11 chapter(s). Convention: Looking Back -> Overview -> Big Picture -> Objectives -> Prereqs -> Sections -> What's Next?
- **Treat Part 12 (industry chapters) as a distinct template.** Chapters 36-42 follow a Big Picture + use-cases + failure-modes pattern that intentionally skips Looking Back, Overview, Objectives, Prereqs, and What's Next. Decide explicitly whether this is the documented convention or a drift to be harmonised with the rest of the book.
- **Reconcile the chapter template with current convention.** `templates/chapter-index.html` already exists, but it does NOT include the `callout looking-back` block and orders objectives BEFORE prereqs. The 11 out-of-order chapters (all in Parts 1 and 2) match a slightly older convention with prereqs BEFORE objectives. Decide which order is canonical, then update the template AND the drifted chapters to match.
- **Run this audit as part of CI** (`scripts/_audit_scaffolding.py`). The summary table at the top of the report is the regression check; fail the build when any block's missing count increases.
- **Add the missing Big Picture callout to the seven Part 1 / 2 chapters** first. These are core foundational chapters whose pedagogical value benefits most from a single-paragraph why-this-matters block; the rest of the convention is already in place.
- **Decide whether the missing Learning Objectives in chapters 34 and 35 (Part 11) are intentional.** Both chapters jump directly from the Big Picture callout to Prerequisites, skipping Learning Objectives. These two chapters are short enough that adding 3-4 bullet objectives would noticeably improve scannability.

---

_Generated by `scripts/_audit_scaffolding.py`. Re-run with `/c/Python314/python scripts/_audit_scaffolding.py`._
