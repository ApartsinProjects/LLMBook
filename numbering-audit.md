# Numbering Consistency Audit

Audit run: 389 content HTML pages scanned, 42 flagged with at least one issue. Section files: 214. Figure captions: 546. Code-fragment captions: 1098.

## 1. Summary

| Category | Count |
|---|---:|
| Phantom references | 7 |
| Drift / off-by-one | 1 |
| Letter mismatches (appendix) | 70 |
| Cross-ref href broken | 1 |
| Duplicate figure labels | 1 |
| Duplicate code-fragment labels | 4 |
| Gaps in figure sequences | 0 |
| Gaps in code-fragment sequences | 0 |

## 2. Phantom references

Prose cites a number that does not exist anywhere in the book.

| File:Line | Kind | Cited as | Nearest existing |
|---|---|---|---|
| `appendices/appendix-m-inference-serving/index.html`:37 | appendix | `Appendix P` | (none) |
| `appendices/appendix-n-distributed-ml/index.html`:7 | appendix | `Appendix N` | (none) |
| `appendices/appendix-o-docker-containers/index.html`:41 | appendix | `Appendix N` | (none) |
| `appendices/appendix-p-tooling-ecosystem/index.html`:7 | appendix | `Appendix P` | (none) |
| `appendices/appendix-p-tooling-ecosystem/index.html`:41 | appendix | `Appendix M` | (none) |
| `appendices/appendix-p-tooling-ecosystem/index.html`:41 | appendix | `Appendix N` | (none) |
| `appendices/appendix-p-tooling-ecosystem/index.html`:41 | appendix | `Appendix O` | (none) |

## 3. Drift / off-by-one

Prose cites X.Y but only X.(Y-1) or X.(Y+1) exists. Likely a renumbering miss.

| File:Line | Kind | Cited as | Likely intended |
|---|---|---|---|
| `part-9-safety-strategy/module-30-safety-ethics-regulation/section-30.3.html`:158 | code_fragment | `Code Fragment 30.3.4` | 30.3.3, 30.3.2, 30.3.1 |

## 4. Duplicate labels

Same caption label appears on two or more pages.

### 4a. Figures

| Label | Files |
|---|---|
| Figure 4.1.1 | `appendices/appendix-a-mathematical-foundations/section-a.6.html`<br>`part-1-foundations/module-04-transformer-architecture/section-4.1.html` |

### 4b. Code Fragments

| Label | Files |
|---|---|
| Code Fragment 4.1.1 | `appendices/appendix-a-mathematical-foundations/section-a.6.html`<br>`part-1-foundations/module-04-transformer-architecture/section-4.1.html` |
| Code Fragment 6.5.1 | `part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.5.html`<br>`part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.9.html` |
| Code Fragment 6.5.2 | `part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.5.html`<br>`part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.9.html` |
| Code Fragment 6.5.3 | `part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.5.html`<br>`part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.9.html` |

## 5. Gaps in numbered sequences

A chapter has captions 1, 2, 4 but not 3.

### 5a. Figures

_None found._

### 5b. Code Fragments

_None found._

## 6. Letter mismatches (Appendix)

Prose says 'Appendix AD' but the target page's h1 renders differently.

| File:Line | Prose says | Target renders as |
|---|---|---|
| `appendices/appendix-b-ml-essentials/index.html`:45 | `Appendix G` | target renders as Appendix F |
| `appendices/appendix-c-python-for-llm/index.html`:40 | `Appendix K` | target renders as Appendix J |
| `appendices/appendix-d-environment-setup/index.html`:40 | `Appendix G` | target renders as Appendix F |
| `appendices/appendix-g-model-cards/index.html`:7 | `Appendix G` | target renders as Appendix F |
| `appendices/appendix-g-model-cards/index.html`:42 | `Appendix J` | target renders as Appendix I |
| `appendices/appendix-g-model-cards/index.html`:45 | `Appendix J` | target renders as Appendix I |
| `appendices/appendix-i-datasets-benchmarks/index.html`:38 | `Appendix H` | target renders as Appendix G |
| `appendices/appendix-j-huggingface-ecosystem/index.html`:48 | `Appendix L` | target renders as Appendix K |
| `appendices/appendix-j-huggingface-ecosystem/section-j.2.html`:27 | `Appendix J` | target renders as Appendix I |
| `appendices/appendix-k-langchain/index.html`:7 | `Appendix K` | target renders as Appendix J |
| `appendices/appendix-l-experiment-tracking/section-l.4.html`:110 | `Appendix S` | target renders as Appendix M |
| `appendices/appendix-l-experiment-tracking/section-l.4.html`:262 | `Appendix S` | target renders as Appendix M |
| `appendices/appendix-l-experiment-tracking/section-l.5.html`:27 | `Appendix L` | target renders as Appendix K |
| `appendices/appendix-m-inference-serving/index.html`:44 | `Appendix U` | target renders as Appendix O |
| `appendices/appendix-n-distributed-ml/index.html`:37 | `Appendix G` | target renders as Appendix F |
| `appendices/appendix-n-distributed-ml/index.html`:40 | `Appendix G` | target renders as Appendix F |
| `appendices/appendix-n-distributed-ml/section-n.1.html`:569 | `Appendix K` | target renders as Appendix J |
| `appendices/appendix-n-distributed-ml/section-n.3.html`:227 | `Appendix S` | target renders as Appendix M |
| `appendices/appendix-n-distributed-ml/section-n.4.html`:44 | `Appendix K` | target renders as Appendix J |
| `appendices/appendix-n-distributed-ml/section-n.4.html`:159 | `Appendix K` | target renders as Appendix J |
| `appendices/appendix-n-distributed-ml/section-n.4.html`:318 | `Appendix R` | target renders as Appendix L |
| `appendices/appendix-n-distributed-ml/section-n.4.html`:584 | `Appendix R` | target renders as Appendix L |
| `appendices/appendix-n-distributed-ml/section-n.5.html`:33 | `Appendix S` | target renders as Appendix M |
| `appendices/appendix-n-distributed-ml/section-n.5.html`:257 | `Appendix S` | target renders as Appendix M |
| `appendices/appendix-n-distributed-ml/section-n.7.html`:117 | `Appendix S` | target renders as Appendix M |
| `appendices/appendix-p-tooling-ecosystem/index.html`:38 | `Appendix K` | target renders as Appendix J |
| `appendices/appendix-p-tooling-ecosystem/index.html`:41 | `Appendix L` | target renders as Appendix K |
| `appendices/appendix-p-tooling-ecosystem/section-p.1.html`:375 | `Appendix R` | target renders as Appendix L |
| `appendices/appendix-p-tooling-ecosystem/section-p.1.html`:376 | `Appendix S` | target renders as Appendix M |
| `appendices/appendix-p-tooling-ecosystem/section-p.1.html`:377 | `Appendix K` | target renders as Appendix J |
| `appendices/appendix-p-tooling-ecosystem/section-p.3.html`:482 | `Appendix R` | target renders as Appendix L |
| `appendices/appendix-p-tooling-ecosystem/section-p.3.html`:483 | `Appendix S` | target renders as Appendix M |
| `appendices/appendix-p-tooling-ecosystem/section-p.3.html`:488 | `Appendix R` | target renders as Appendix L |
| `appendices/appendix-s-pedagogy-kit/index.html`:7 | `Appendix S` | target renders as Appendix M |
| `appendices/appendix-s-pedagogy-kit/index.html`:8 | `Appendix S` | target renders as Appendix M |
| `appendices/appendix-s-pedagogy-kit/index.html`:22 | `Appendix S` | target renders as Appendix M |
| `appendices/appendix-s-pedagogy-kit/index.html`:70 | `Appendix AE` | target renders as Appendix R |
| `appendices/appendix-s-pedagogy-kit/index.html`:82 | `Appendix AE` | target renders as Appendix R |
| `appendices/appendix-s-pedagogy-kit/index.html`:92 | `Appendix R` | target renders as Appendix L |
| `appendices/appendix-s-pedagogy-kit/index.html`:93 | `Appendix AD` | target renders as Appendix Q |
| `appendices/appendix-s-pedagogy-kit/index.html`:96 | `Appendix AE` | target renders as Appendix R |
| `appendices/appendix-s-pedagogy-kit/index.html`:101 | `Appendix AE` | target renders as Appendix R |
| `appendices/appendix-s-pedagogy-kit/index.html`:109 | `Appendix R` | target renders as Appendix L |
| `appendices/glossary/section-f.4.html`:86 | `Appendix G` | target renders as Appendix F |
| `front-matter/fm-course-syllabi.html`:225 | `Appendix K` | target renders as Appendix J |
| `front-matter/fm-course-syllabi.html`:225 | `Appendix L` | target renders as Appendix K |
| `front-matter/fm-reading-pathways.html`:100 | `Appendix AI` | target renders as Appendix U |
| `front-matter/fm-reading-pathways.html`:135 | `Appendix AD` | target renders as Appendix Q |
| `front-matter/fm-reading-pathways.html`:147 | `Appendix AF` | target renders as Appendix S |
| `front-matter/fm-reading-pathways.html`:162 | `Appendix AD` | target renders as Appendix Q |
| `part-12-llm-applications-across-industries/module-39-education-llms/index.html`:78 | `Appendix AF` | target renders as Appendix S |
| `part-2-understanding-llms/module-09-inference-optimization/section-9.1.html`:514 | `Appendix S` | target renders as Appendix M |
| `part-2-understanding-llms/module-09-inference-optimization/section-9.2.html`:54 | `Appendix G` | target renders as Appendix F |
| `part-2-understanding-llms/module-09-inference-optimization/section-9.2.html`:470 | `Appendix S` | target renders as Appendix M |
| `part-2-understanding-llms/module-09-inference-optimization/section-9.2.html`:470 | `Appendix S` | target renders as Appendix M |
| `part-2-understanding-llms/module-09-inference-optimization/section-9.4.html`:54 | `Appendix S` | target renders as Appendix M |
| `part-3-working-with-llms/module-11-llm-apis/section-11.2.html`:57 | `Appendix AE` | target renders as Appendix R |
| `part-4-training-adapting/module-15-fine-tuning-fundamentals/section-15.1.html`:43 | `Appendix K` | target renders as Appendix J |
| `part-4-training-adapting/module-16-peft/section-16.1.html`:46 | `Appendix K` | target renders as Appendix J |
| `part-5-retrieval-conversation/module-19-rag/section-19.1.html`:42 | `Appendix R` | target renders as Appendix L |
| `part-5-retrieval-conversation/module-19-rag/section-19.1.html`:43 | `Appendix L` | target renders as Appendix K |
| `part-5-retrieval-conversation/module-19-rag/section-19.1.html`:52 | `Appendix AE` | target renders as Appendix R |
| `part-5-retrieval-conversation/module-19-rag/section-19.2.html`:150 | `Appendix AE` | target renders as Appendix R |
| `part-6-agentic-ai/module-23-multi-agent-systems/section-23.1.html`:49 | `Appendix L` | target renders as Appendix K |
| `part-6-agentic-ai/module-25-agent-safety-production/section-25.3.html`:52 | `Appendix AE` | target renders as Appendix R |
| `part-8-evaluation-production/module-28-evaluation-observability/section-28.12.html`:41 | `Appendix G` | target renders as Appendix F |
| `part-8-evaluation-production/module-28-evaluation-observability/section-28.5.html`:55 | `Appendix AE` | target renders as Appendix R |
| `part-8-evaluation-production/module-29-production-engineering/section-29.4.html`:45 | `Appendix AE` | target renders as Appendix R |
| `part-8-evaluation-production/module-29-production-engineering/section-29.4.html`:56 | `Appendix AE` | target renders as Appendix R |
| `part-9-safety-strategy/module-30-safety-ethics-regulation/section-30.11.html`:686 | `Appendix T` | target renders as Appendix N |

## 7. Cross-reference href broken

An `<a href>` whose anchor text claims one section number but the href points to a different one.

| File:Line | Anchor says | Href resolves to |
|---|---|---|
| `part-4-training-adapting/module-16-peft/index.html`:104 | `Section 16.4` | href resolves to section-16.2.html |

## 8. Recommended fix priority

- **Drift / off-by-one (1 cases)**: highest yield. Each is a one-token edit in prose to match an adjacent caption number. Likely all from the same renumber pass.
- **Duplicate figure labels (1 cases)**: two pages claim the same Figure X.Y.Z. Renumber the later occurrence.
- **Duplicate code-fragment labels (4 cases)**: same problem as figures.
- **Phantom references (7 cases)**: prose cites a number that does not exist. Either the target was deleted or never created; decide per case.
- **Appendix letter mismatches (70 cases)**: book-wide letter drift. Do NOT fix piecemeal; this needs a coordinated pass.
- **Cross-ref href mismatches (1 cases)**: anchor text and href disagree. Either the anchor text is stale or the href is stale; the more recently edited side is usually correct.
