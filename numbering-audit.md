# Numbering Consistency Audit

Audit run: 567 content HTML pages scanned, 85 flagged with at least one issue. Section files: 443. Figure captions: 630. Code-fragment captions: 1273.

## 1. Summary

| Category | Count |
|---|---:|
| Phantom references | 28 |
| Drift / off-by-one | 62 |
| Letter mismatches (appendix) | 0 |
| Cross-ref href broken | 41 |
| Duplicate figure labels | 1 |
| Duplicate code-fragment labels | 3 |
| Gaps in figure sequences | 1 |
| Gaps in code-fragment sequences | 12 |

## 2. Phantom references

Prose cites a number that does not exist anywhere in the book.

| File:Line | Kind | Cited as | Nearest existing |
|---|---|---|---|
| `appendices/appendix-b-course-syllabi/index.html`:66 | appendix | `Appendix A` | (none) |
| `appendices/appendix-b-course-syllabi/index.html`:236 | appendix | `Appendix A` | (none) |
| `appendices/appendix-c-reading-pathways/index.html`:159 | appendix | `Appendix B` | (none) |
| `appendices/index.html`:43 | appendix | `Appendix A` | (none) |
| `appendices/index.html`:43 | appendix | `Appendix B` | (none) |
| `front-matter/fm-how-to-use.html`:52 | appendix | `Appendix B` | (none) |
| `front-matter/fm-how-to-use.html`:89 | appendix | `Appendix B` | (none) |
| `front-matter/fm-who-should-read.html`:56 | appendix | `Appendix B` | (none) |
| `part-1-llm-building-blocks/module-03-transformer-architecture/section-3.1.html`:115 | appendix | `Appendix A` | (none) |
| `part-10-llm-security-runtime-safety/module-47-adversarial-security-red-team/section-47.1.html`:358 | section | `Section 47.3.1.2` | (none) |
| `part-10-llm-security-runtime-safety/module-47-adversarial-security-red-team/section-47.1.html`:1077 | section | `Section 47.3.1.2` | (none) |
| `part-14-designing-llm-agent-products/module-71-tools-of-the-trade/section-71.1.html`:196 | appendix | `Appendix G` | (none) |
| `part-14-designing-llm-agent-products/module-71-tools-of-the-trade/section-71.1.html`:253 | appendix | `Appendix G` | (none) |
| `part-14-designing-llm-agent-products/module-71-tools-of-the-trade/section-71.1.html`:260 | appendix | `Appendix G` | (none) |
| `part-14-designing-llm-agent-products/module-71-tools-of-the-trade/section-71.2.html`:134 | appendix | `Appendix J` | (none) |
| `part-14-designing-llm-agent-products/module-71-tools-of-the-trade/section-71.2.html`:219 | appendix | `Appendix J` | (none) |
| `part-15-applications-of-llms-across-industries/module-75-education-llms/section-75.5.html`:62 | appendix | `Appendix A` | (none) |
| `part-2-understanding-llms/module-09-inference-optimization/section-9.4.html`:66 | appendix | `Appendix K` | (none) |
| `part-2-understanding-llms/module-10-interpretability/section-10.5.html`:50 | appendix | `Appendix L` | (none) |
| `part-4-training-adaptation/module-19-tools-of-the-trade/index.html`:53 | appendix | `Appendix L` | (none) |
| `part-4-training-adaptation/module-19-tools-of-the-trade/section-19.4.html`:106 | appendix | `Appendix L` | (none) |
| `part-4-training-adaptation/module-19-tools-of-the-trade/section-19.4.html`:109 | appendix | `Appendix O` | (none) |
| `part-5-multimodal-llms/module-20-audio-music-generation/section-20.7.html`:152 | figure | `Figure 20.7.1` | (none) |
| `part-6-agentic-ai/module-28-multi-agent-systems/section-28.1.html`:61 | appendix | `Appendix J` | (none) |
| `part-9-llm-evaluation-observability/module-44-online-eval-observability/section-44.1.html`:202 | appendix | `Appendix J` | (none) |
| `part-9-llm-evaluation-observability/module-44-online-eval-observability/section-44.1.html`:202 | appendix | `Appendix I` | (none) |
| `part-9-llm-evaluation-observability/module-44-online-eval-observability/section-44.3.html`:132 | appendix | `Appendix G` | (none) |
| `part-9-llm-evaluation-observability/module-44-online-eval-observability/section-44.3.html`:203 | appendix | `Appendix G` | (none) |

## 3. Drift / off-by-one

Prose cites X.Y but only X.(Y-1) or X.(Y+1) exists. Likely a renumbering miss.

| File:Line | Kind | Cited as | Likely intended |
|---|---|---|---|
| `.book-update/v9-preserved-content/multimodal-reasoning-cross-modal-retrieval-section-41.7.html`:65 | section | `Section 41.8` | 41.1, 41.2, 41.3, 41.4, 41.5 |
| `appendices/appendix-c-reading-pathways/index.html`:130 | section | `Section 33.7` | 33.1, 33.2, 33.3, 33.4 |
| `part-1-llm-building-blocks/module-00-ml-pytorch-foundations/section-0.1.html`:506 | section | `Section 7.5` | 7.3, 7.1, 7.2 |
| `part-10-llm-security-runtime-safety/module-50-privacy-data-protection/section-50.1.html`:477 | section | `Section 49.7` | 49.5, 49.1, 49.2, 49.3, 49.4 |
| `part-10-llm-security-runtime-safety/module-50-privacy-data-protection/section-50.3.html`:88 | section | `Section 49.10` | 49.1, 49.2, 49.3, 49.4, 49.5 |
| `part-11-llm-ethics-trust-governance/module-52-bias-fairness/section-52.1.html`:170 | code_fragment | `Code Fragment 52.1.4` | 52.1.3, 52.1.2, 52.1.1 |
| `part-11-llm-ethics-trust-governance/module-54b-transparency-and-disclosure/section-54.9.html`:199 | section | `Section 57.5` | 57.4, 57.3, 57.1, 57.2 |
| `part-12-llm-systems-at-scale/module-59-distributed-training-systems/section-59.2.html`:61 | section | `Section 0.5` | 0.4, 0.3, 0.1, 0.2 |
| `part-12-llm-systems-at-scale/module-59-distributed-training-systems/section-59.4.html`:59 | section | `Section 0.5` | 0.4, 0.3, 0.1, 0.2 |
| `part-14-designing-llm-agent-products/module-67-ideation/section-67.4.html`:62 | section | `Section 66.2` | 66.1 |
| `part-14-designing-llm-agent-products/module-67-ideation/section-67.6.html`:41 | section | `Section 64.2` | 64.1 |
| `part-14-designing-llm-agent-products/module-69-llm-economics/section-69.2.html`:97 | section | `Section 69.4` | 69.3, 69.2, 69.1 |
| `part-14-designing-llm-agent-products/module-69-llm-economics/section-69.3.html`:110 | section | `Section 69.4` | 69.3, 69.2, 69.1 |
| `part-14-designing-llm-agent-products/module-70-shipping-products/section-70.2.html`:106 | section | `Section 66.2` | 66.1 |
| `part-14-designing-llm-agent-products/module-70-shipping-products/section-70.2.html`:201 | section | `Section 66.5` | 66.1 |
| `part-14-designing-llm-agent-products/module-70-shipping-products/section-70.2.html`:306 | section | `Section 66.6` | 66.1 |
| `part-14-designing-llm-agent-products/module-71-tools-of-the-trade/section-71.1.html`:235 | section | `Section 48.11` | 48.1, 48.2, 48.3, 48.4, 48.5 |
| `part-14-designing-llm-agent-products/module-71-tools-of-the-trade/section-71.1.html`:253 | section | `Section 48.11` | 48.1, 48.2, 48.3, 48.4, 48.5 |
| `part-15-applications-of-llms-across-industries/module-73-finance-llms/index.html`:43 | section | `Section 73.6` | 73.5, 73.4, 73.1, 73.2, 73.3 |
| `part-15-applications-of-llms-across-industries/module-74-healthcare-llms/index.html`:41 | section | `Section 74.6` | 74.5, 74.4, 74.1, 74.2, 74.3 |
| `part-15-applications-of-llms-across-industries/module-76-cybersecurity-llms/index.html`:41 | section | `Section 76.6` | 76.5, 76.4, 76.1, 76.2, 76.3 |
| `part-15-applications-of-llms-across-industries/module-78-manufacturing-llms/section-78.10.html`:81 | section | `Section 32.7` | 32.1, 32.2, 32.3, 32.4 |
| `part-15-applications-of-llms-across-industries/module-78-manufacturing-llms/section-78.4.html`:117 | section | `Section 32.7` | 32.1, 32.2, 32.3, 32.4 |
| `part-15-applications-of-llms-across-industries/module-78-manufacturing-llms/section-78.5.html`:65 | section | `Section 32.8` | 32.1, 32.2, 32.3, 32.4 |
| `part-15-applications-of-llms-across-industries/module-78-manufacturing-llms/section-78.6.html`:45 | section | `Section 32.6` | 32.4, 32.1, 32.2, 32.3 |
| `part-15-applications-of-llms-across-industries/module-78-manufacturing-llms/section-78.7.html`:72 | section | `Section 32.6` | 32.4, 32.1, 32.2, 32.3 |
| `part-15-applications-of-llms-across-industries/module-78-manufacturing-llms/section-78.8.html`:45 | section | `Section 32.7` | 32.1, 32.2, 32.3, 32.4 |
| `part-15-applications-of-llms-across-industries/module-78-manufacturing-llms/section-78.9.html`:696 | section | `Section 80.5` | 80.4, 80.3, 80.1, 80.2 |
| `part-16-llm-agentic-ai-research-frontiers/module-80-frontier-architectures/section-80.3.html`:701 | section | `Section 7.7` | 7.1, 7.2, 7.3 |
| `part-16-llm-agentic-ai-research-frontiers/module-81-frontier-theory/section-81.1.html`:334 | section | `Section 81.6` | 81.4, 81.1, 81.2, 81.3 |
| `part-16-llm-agentic-ai-research-frontiers/module-81-frontier-theory/section-81.2.html`:62 | section | `Section 81.5` | 81.4, 81.3, 81.1, 81.2 |
| `part-16-llm-agentic-ai-research-frontiers/module-81-frontier-theory/section-81.2.html`:329 | section | `Section 81.7` | 81.1, 81.2, 81.3, 81.4 |
| `part-16-llm-agentic-ai-research-frontiers/module-81-frontier-theory/section-81.3.html`:266 | section | `Section 81.5` | 81.4, 81.3, 81.1, 81.2 |
| `part-16-llm-agentic-ai-research-frontiers/module-81-frontier-theory/section-81.3.html`:304 | section | `Section 81.8` | 81.1, 81.2, 81.3, 81.4 |
| `part-16-llm-agentic-ai-research-frontiers/module-81-frontier-theory/section-81.4.html`:80 | section | `Section 81.6` | 81.4, 81.1, 81.2, 81.3 |
| `part-16-llm-agentic-ai-research-frontiers/module-81-frontier-theory/section-81.4.html`:194 | section | `Section 81.7` | 81.1, 81.2, 81.3, 81.4 |
| `part-16-llm-agentic-ai-research-frontiers/module-81-frontier-theory/section-81.4.html`:258 | section | `Section 81.9` | 81.1, 81.2, 81.3, 81.4 |
| `part-2-understanding-llms/module-08-reasoning-test-time-compute/section-8.1.html`:160 | section | `Section 23.9` | 23.1, 23.2, 23.3, 23.4, 23.5 |
| `part-2-understanding-llms/module-10-interpretability/section-10.4.html`:599 | section | `Section 10.4b` | 10.1, 10.2, 10.3, 10.4, 10.5 |
| `part-4-training-adaptation/module-18-alignment-rlhf-dpo/section-18.1.html`:123 | figure | `Figure 18.1.2b` | 18.1.1, 18.1.2a, 18.1.3 |
| `part-5-multimodal-llms/module-20-audio-music-generation/section-20.8.html`:153 | section | `Section 33.5` | 33.4, 33.3, 33.1, 33.2 |
| `part-5-multimodal-llms/module-20-audio-music-generation/section-20.8.html`:159 | section | `Section 33.5` | 33.4, 33.3, 33.1, 33.2 |
| `part-5-multimodal-llms/module-20-audio-music-generation/section-20.9.html`:167 | section | `Section 33.5` | 33.4, 33.3, 33.1, 33.2 |
| `part-5-multimodal-llms/module-21-document-understanding-ocr/section-21.4.html`:215 | figure | `Figure 21.4.2` | 21.4.1 |
| `part-5-multimodal-llms/module-24-vla-models/section-24.12.html`:176 | figure | `Figure 24.12.2` | 24.12.1 |
| `part-5-multimodal-llms/module-24-vla-models/section-24.12.html`:179 | figure | `Figure 24.12.2` | 24.12.1 |
| `part-5-multimodal-llms/module-24-vla-models/section-24.12.html`:186 | figure | `Figure 24.12.2` | 24.12.1 |
| `part-5-multimodal-llms/module-24-vla-models/section-24.5.html`:167 | figure | `Figure 24.5.2` | 24.5.1 |
| `part-5-multimodal-llms/module-25-tools-of-the-trade/index.html`:70 | section | `Section 7.4` | 7.3, 7.2, 7.1 |
| `part-5-multimodal-llms/module-25-tools-of-the-trade/section-25.3.html`:16 | section | `Section 7.4` | 7.3, 7.2, 7.1 |
| `part-6-agentic-ai/index.html`:47 | chapter | `Chapter 38` | Chapter 37, Chapter 36, Chapter 40 |
| `part-7-retrieval-information-extraction-with-llms/module-31-embeddings-vector-db/section-31.4.html`:659 | section | `Section 31.4b` | 31.1, 31.2, 31.3, 31.4, 31.5 |
| `part-7-retrieval-information-extraction-with-llms/module-33-cross-modal-reasoning-rag/section-33.4.html`:173 | chapter | `Chapter 38` | Chapter 37, Chapter 36, Chapter 40 |
| `part-7-retrieval-information-extraction-with-llms/module-34-structured-information-extraction-ner/section-34.2.html`:59 | code_fragment | `Code Fragment 34.2.10` | 34.2.1a, 34.2.2, 34.2.3, 34.2.4, 34.2.5 |
| `part-7-retrieval-information-extraction-with-llms/module-34-structured-information-extraction-ner/section-34.2.html`:123 | code_fragment | `Code Fragment 34.2.10` | 34.2.1a, 34.2.2, 34.2.3, 34.2.4, 34.2.5 |
| `part-7-retrieval-information-extraction-with-llms/module-34-structured-information-extraction-ner/section-34.3.html`:47 | code_fragment | `Code Fragment 34.3.10` | 34.3.1, 34.3.2 |
| `part-7-retrieval-information-extraction-with-llms/module-34-structured-information-extraction-ner/section-34.3.html`:128 | code_fragment | `Code Fragment 34.3.10` | 34.3.1, 34.3.2 |
| `part-8-conversational-ai-with-llms/module-40-voice-realtime-multimodal/section-40.5.html`:218 | chapter | `Chapter 39` | Chapter 40, Chapter 37, Chapter 41 |
| `part-8-conversational-ai-with-llms/module-41-conv-ai-tools/section-41.5.html`:213 | chapter | `Chapter 38` | Chapter 37, Chapter 36, Chapter 40 |
| `part-8-conversational-ai-with-llms/module-41-conv-ai-tools/section-41.5.html`:213 | chapter | `Chapter 39` | Chapter 40, Chapter 37, Chapter 41 |
| `part-9-llm-evaluation-observability/module-46-llm-as-judge-automated-evaluation/section-46.1.html`:68 | code_fragment | `Code Fragment 46.1.2` | 46.1.1 |
| `part-9-llm-evaluation-observability/module-46-llm-as-judge-automated-evaluation/section-46.2.html`:46 | code_fragment | `Code Fragment 46.2.6` | 46.2.1, 46.2.2 |

## 4. Duplicate labels

Same caption label appears on two or more pages.

### 4a. Figures

| Label | Files |
|---|---|
| Figure 41.4.1 | `.book-update/v9-preserved-content/world-models-and-embodied-reasoning-section-41.4.html`<br>`part-8-conversational-ai-with-llms/module-41-conv-ai-tools/section-41.4.html` |

### 4b. Code Fragments

| Label | Files |
|---|---|
| Code Fragment 10.4.7 | `part-2-understanding-llms/module-10-interpretability/section-10.4.html`<br>`part-2-understanding-llms/module-10-interpretability/section-10.4b.html` |
| Code Fragment 10.4.8 | `part-2-understanding-llms/module-10-interpretability/section-10.4.html`<br>`part-2-understanding-llms/module-10-interpretability/section-10.4b.html` |
| Code Fragment 4.1.1 | `appendices/appendix-a-mathematical-foundations/section-a.6.html`<br>`part-1-llm-building-blocks/module-04-decoding-text-generation/section-4.1.html` |

## 5. Gaps in numbered sequences

A chapter has captions 1, 2, 4 but not 3.

### 5a. Figures

| Prefix | Missing |
|---|---|
| Figure 18.1.* | 2 |

### 5b. Code Fragments

| Prefix | Missing |
|---|---|
| Code Fragment 12.2.* | 6 |
| Code Fragment 18.2.* | 3 |
| Code Fragment 26.1.* | 4 |
| Code Fragment 3.1.* | 7 |
| Code Fragment 32.2.* | 4 |
| Code Fragment 47.2.* | 2 |
| Code Fragment 57.4.* | 3, 6, 7 |
| Code Fragment 6.6.* | 5 |
| Code Fragment 6.8.* | 2 |
| Code Fragment 65.3.* | 4, 5 |
| Code Fragment 9.1.* | 4, 5, 8 |
| Code Fragment 9.3.* | 2 |

## 6. Letter mismatches (Appendix)

Prose says 'Appendix AD' but the target page's h1 renders differently.

_None found._

## 7. Cross-reference href broken

An `<a href>` whose anchor text claims one section number but the href points to a different one.

| File:Line | Anchor says | Href resolves to |
|---|---|---|
| `.book-update/v9-preserved-content/world-models-and-embodied-reasoning-section-41.4.html`:39 | `Section 6.2` | href resolves to section-7.2.html |
| `.book-update/v9-preserved-content/world-models-and-embodied-reasoning-section-41.4.html`:39 | `Section 6.2` | href resolves to section-7.2.html |
| `part-1-llm-building-blocks/module-00-ml-pytorch-foundations/index.html`:96 | `Section 0.1` | href resolves to section-0.2.html |
| `part-1-llm-building-blocks/module-01-foundations-nlp-text-representation/index.html`:105 | `Section 1.2` | href resolves to section-1.3.html |
| `part-1-llm-building-blocks/module-01-foundations-nlp-text-representation/index.html`:111 | `Section 1.3` | href resolves to section-1.4.html |
| `part-1-llm-building-blocks/module-01-foundations-nlp-text-representation/index.html`:123 | `Section 2.1` | href resolves to section-1.6.html |
| `part-1-llm-building-blocks/module-01-foundations-nlp-text-representation/index.html`:129 | `Section 2.2` | href resolves to section-1.7.html |
| `part-1-llm-building-blocks/module-03-transformer-architecture/index.html`:98 | `Section 3.1` | href resolves to section-3.2.html |
| `part-1-llm-building-blocks/module-04-decoding-text-generation/index.html`:104 | `Section 4.1` | href resolves to section-4.4.html |
| `part-1-llm-building-blocks/module-05-tools-of-the-trade/section-5.2.html`:644 | `Section 19.2` | href resolves to section-19.10.html |
| `part-1-llm-building-blocks/module-05-tools-of-the-trade/section-5.2.html`:644 | `Section 19.2` | href resolves to section-19.10.html |
| `part-14-designing-llm-agent-products/module-68-vibe-coding/index.html`:67 | `Section 67.1` | href resolves to section-68.5.html |
| `part-14-designing-llm-agent-products/module-69-llm-economics/index.html`:57 | `Section 69.2` | href resolves to section-69.3.html |
| `part-14-designing-llm-agent-products/module-71-tools-of-the-trade/section-71.2.html`:137 | `Section 19.2` | href resolves to section-19.10.html |
| `part-2-understanding-llms/module-06-pretraining-scaling-laws/index.html`:133 | `Section 6.6` | href resolves to section-6.8.html |
| `part-2-understanding-llms/module-09-inference-optimization/index.html`:129 | `Section 9.1` | href resolves to section-9.5.html |
| `part-4-training-adaptation/module-19-tools-of-the-trade/section-19.13.html`:43 | `Section 19.2` | href resolves to section-19.10.html |
| `part-4-training-adaptation/module-19-tools-of-the-trade/section-19.13.html`:43 | `Section 19.2` | href resolves to section-19.10.html |
| `part-4-training-adaptation/module-19-tools-of-the-trade/section-19.13.html`:141 | `Section 19.2` | href resolves to section-19.14.html |
| `part-4-training-adaptation/module-19-tools-of-the-trade/section-19.9.html`:42 | `Section 19.2` | href resolves to section-19.10.html |
| `part-5-multimodal-llms/module-20-audio-music-generation/index.html`:88 | `Section 33.2` | href resolves to section-20.8.html |
| `part-5-multimodal-llms/module-20-audio-music-generation/index.html`:100 | `Section 33.2` | href resolves to section-20.10.html |
| `part-5-multimodal-llms/module-22-vision-language-models/index.html`:82 | `Section 37.1` | href resolves to section-22.7.html |
| `part-5-multimodal-llms/module-25-tools-of-the-trade/index.html`:57 | `Section 13.1` | href resolves to section-25.1.html |
| `part-5-multimodal-llms/module-25-tools-of-the-trade/index.html`:67 | `Section 7.4` | href resolves to section-25.3.html |
| `part-5-multimodal-llms/module-25-tools-of-the-trade/index.html`:72 | `Section 8.1` | href resolves to section-25.4.html |
| `part-5-multimodal-llms/module-25-tools-of-the-trade/index.html`:77 | `Section 16.5` | href resolves to section-25.5.html |
| `part-6-agentic-ai/module-26-ai-agents/index.html`:125 | `Section 37.3` | href resolves to section-26.6.html |
| `part-6-agentic-ai/module-27-tool-use-protocols/index.html`:117 | `Section 32.2` | href resolves to section-27.5.html |
| `part-7-retrieval-information-extraction-with-llms/module-35-advanced-rag/index.html`:57 | `Section 35.2` | href resolves to section-35.3.html |
| `part-9-llm-evaluation-observability/module-42-evaluation-foundations/index.html`:177 | `Section 0.1` | href resolves to section-42.12.html |
| `part-9-llm-evaluation-observability/module-44-online-eval-observability/section-44.1.html`:54 | `Section 19.2` | href resolves to section-19.10.html |
| `part-9-llm-evaluation-observability/module-44-online-eval-observability/section-44.1.html`:54 | `Section 19.2` | href resolves to section-19.10.html |
| `part-9-llm-evaluation-observability/module-44-online-eval-observability/section-44.1.html`:54 | `Section 19.2` | href resolves to section-19.10.html |
| `part-9-llm-evaluation-observability/module-44-online-eval-observability/section-44.1.html`:117 | `Section 19.2` | href resolves to section-19.11.html |
| `part-9-llm-evaluation-observability/module-44-online-eval-observability/section-44.2.html`:44 | `Section 19.2` | href resolves to section-19.12.html |
| `part-9-llm-evaluation-observability/module-44-online-eval-observability/section-44.3.html`:45 | `Section 19.2` | href resolves to section-19.10.html |
| `part-9-llm-evaluation-observability/module-44-online-eval-observability/section-44.3.html`:45 | `Section 19.2` | href resolves to section-19.10.html |
| `part-9-llm-evaluation-observability/module-44-online-eval-observability/section-44.3.html`:45 | `Section 19.2` | href resolves to section-19.10.html |
| `part-9-llm-evaluation-observability/module-44-online-eval-observability/section-44.3.html`:45 | `Section 19.2` | href resolves to section-19.10.html |
| `part-9-llm-evaluation-observability/module-45-tools-of-the-trade/section-45.2.html`:70 | `Section 45.2` | href resolves to section-44.3.html |

## 8. Recommended fix priority

- **Drift / off-by-one (62 cases)**: highest yield. Each is a one-token edit in prose to match an adjacent caption number. Likely all from the same renumber pass.
- **Duplicate figure labels (1 cases)**: two pages claim the same Figure X.Y.Z. Renumber the later occurrence.
- **Duplicate code-fragment labels (3 cases)**: same problem as figures.
- **Phantom references (28 cases)**: prose cites a number that does not exist. Either the target was deleted or never created; decide per case.
- **Sequence gaps (1 figure, 12 code)**: a missing number in a chapter's sequence. Either a caption was deleted without renumbering, or a number was skipped intentionally.
- **Cross-ref href mismatches (41 cases)**: anchor text and href disagree. Either the anchor text is stale or the href is stale; the more recently edited side is usually correct.
