# Prose Reference Audit

Audit run: **546** content HTML pages scanned. Inventories: 592 figure captions, 1199 code-fragment captions, 16 algorithm/pseudocode blocks, 425 section files, 82 chapters.

This audit complements the existing `numbering-audit.md`. The earlier pass walked PROSE only; this one scans inside code-fragment comments, inside `<img alt>` attributes, inside caption cross-references, and across plain-text prose mentions that could be hyperlinked.

**Headline:** 55 genuine reference problems found across 42 files (plus 1077 plain-text mentions that could be hyperlinks).

## 1. Summary

| Category | Problems found |
|---|---:|
| Cat. 1 — Phantom refs inside code comments | 2 |
| Cat. 2a — Plain-text mentions that should be hyperlinks | 1077 |
| Cat. 2b — Plain-text mentions whose target does not exist | 53 |
| Cat. 3a — `<img alt>` references with no matching target | 0 |
| Cat. 3b — `<img alt>` figure label disagrees with surrounding caption | 0 |
| Cat. 4 — Caption cross-refs to non-existent targets | 0 |
| **Total problems** (excluding Cat. 2a hyperlink suggestions) | **55** |

## 2. Category 1 — Phantom references inside code comments

References found inside `<pre><code>` comment spans whose target does not exist anywhere in the book.

| File:Line | Kind | Cited as | Comment context |
|---|---|---|---|
| `part-5-multimodal-llms/module-22-vision-language-models/section-22.9.html`:52 | section | `Section 38.2` | `# See Section 38.2 for the full protocol walkthrough.` |
| `part-7-retrieval-information-extraction-with-llms/module-32-rag/section-32.2.html`:192 | section | `Section 32.5` | `# Text-to-SQL pipeline (covered in Section 32.5)` |

## 3. Category 2 — Plain-text mentions that could be hyperlinks

Prose contains `Figure X.Y.Z` / `Section X.Y` etc. as plain text, but the target exists and is normally linked elsewhere. Highest-value candidates are labels mentioned unlinked **on three or more pages**; single-mention occurrences are common (e.g. when discussing two figures by name in the same paragraph) and lower priority.

Total non-low-priority plain-text mentions: **1072** across **557** distinct labels.

### Top 30 labels by un-linked-mention count

| Rank | Label | Count | Distinct files | Example file:line |
|---:|---|---:|---:|---|
| 1 | `Chapter 20` | 19 | 14 | `appendices/appendix-a-mathematical-foundations/section-a.4.html`:89 |
| 2 | `Section 20.1` | 18 | 16 | `appendices/appendix-a-mathematical-foundations/section-a.4.html`:89 |
| 3 | `Chapter 26` | 16 | 13 | `part-1-llm-building-blocks/module-00-ml-pytorch-foundations/index.html`:49 |
| 4 | `Chapter 44` | 16 | 10 | `part-14-designing-llm-agent-products/module-67-ideation/section-67.10.html`:229 |
| 5 | `Chapter 34` | 11 | 10 | `appendices/appendix-a-mathematical-foundations/index.html`:49 |
| 6 | `Chapter 14` | 10 | 9 | `index.html`:779 |
| 7 | `Chapter 23` | 10 | 9 | `part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.3.html`:72 |
| 8 | `Chapter 04` | 9 | 8 | `appendices/appendix-a-mathematical-foundations/index.html`:49 |
| 9 | `Chapter 24` | 9 | 4 | `part-5-multimodal-llms/module-24-vla-models/section-24.10.html`:24 |
| 10 | `Section 4.1` | 8 | 7 | `appendices/appendix-a-mathematical-foundations/section-a.2.html`:105 |
| 11 | `Chapter 10` | 8 | 6 | `front-matter/fm-who-should-read.html`:45 |
| 12 | `Section 7.1` | 8 | 8 | `part-1-llm-building-blocks/module-00-ml-pytorch-foundations/section-0.1.html`:119 |
| 13 | `Chapter 11` | 8 | 7 | `part-1-llm-building-blocks/module-01-foundations-nlp-text-representation/section-1.4.html`:441 |
| 14 | `Chapter 45` | 8 | 7 | `part-10-llm-security-runtime-safety/module-47-adversarial-security-red-team/index.html`:43 |
| 15 | `Chapter 06` | 7 | 6 | `appendices/appendix-a-mathematical-foundations/index.html`:49 |
| 16 | `Chapter 18` | 7 | 7 | `appendices/appendix-a-mathematical-foundations/section-a.1.html`:111 |
| 17 | `Section 48.3` | 7 | 4 | `part-1-llm-building-blocks/module-01-foundations-nlp-text-representation/section-1.7.html`:696 |
| 18 | `Section 4.2` | 7 | 3 | `part-1-llm-building-blocks/module-04-decoding-text-generation/section-4.1.html`:71 |
| 19 | `Chapter 25` | 7 | 6 | `part-4-training-adaptation/module-18-alignment-rlhf-dpo/section-18.1.html`:59 |
| 20 | `Chapter 46` | 7 | 3 | `part-5-multimodal-llms/module-22-vision-language-models/section-22.4.html`:209 |
| 21 | `Section 3.2` | 6 | 5 | `part-1-llm-building-blocks/module-03-transformer-architecture/index.html`:38 |
| 22 | `Chapter 12` | 6 | 6 | `part-1-llm-building-blocks/module-05-tools-of-the-trade/index.html`:73 |
| 23 | `Chapter 31` | 6 | 6 | `part-10-llm-security-runtime-safety/module-47-adversarial-security-red-team/index.html`:56 |
| 24 | `Chapter 54` | 6 | 3 | `part-10-llm-security-runtime-safety/module-48-guardrails-runtime-safety/section-48.3.html`:42 |
| 25 | `Chapter 57` | 6 | 4 | `part-11-llm-ethics-trust-governance/module-54-watermarking-provenance/section-54.10.html`:138 |
| 26 | `Pseudocode 27.2.1` | 6 | 3 | `part-6-agentic-ai/module-27-tool-use-protocols/section-27.2.html`:69 |
| 27 | `Chapter 3` | 5 | 5 | `appendices/appendix-a-mathematical-foundations/section-a.6.html`:34 |
| 28 | `Chapter 27` | 5 | 5 | `appendices/appendix-c-reading-pathways/index.html`:64 |
| 29 | `Chapter 49` | 5 | 5 | `part-10-llm-security-runtime-safety/module-49-agent-safety-autonomy/index.html`:8 |
| 30 | `Section 59.5` | 5 | 4 | `part-12-llm-systems-at-scale/module-59-distributed-training-systems/index.html`:26 |

### Cat. 2b — Plain-text mentions whose target does not exist

Found **53** phantom plain-text mentions. Showing the first 60.

| File:Line | Kind | Cited as |
|---|---|---|
| `appendices/appendix-c-reading-pathways/index.html`:119 | section | `Section 33.7` |
| `part-1-llm-building-blocks/module-00-ml-pytorch-foundations/section-0.1.html`:487 | section | `Section 7.5` |
| `part-10-llm-security-runtime-safety/module-50-privacy-data-protection/section-50.1.html`:7 | section | `Section 49.10` |
| `part-10-llm-security-runtime-safety/module-50-privacy-data-protection/section-50.1.html`:464 | section | `Section 49.7` |
| `part-11-llm-ethics-trust-governance/module-54-watermarking-provenance/section-54.9.html`:172 | section | `Section 57.5` |
| `part-14-designing-llm-agent-products/module-67-ideation/section-67.4.html`:51 | section | `Section 66.2` |
| `part-14-designing-llm-agent-products/module-67-ideation/section-67.6.html`:30 | section | `Section 64.2` |
| `part-14-designing-llm-agent-products/module-69-llm-economics/section-69.2.html`:84 | section | `Section 69.4` |
| `part-14-designing-llm-agent-products/module-69-llm-economics/section-69.3.html`:97 | section | `Section 69.4` |
| `part-14-designing-llm-agent-products/module-70-shipping-products/section-70.2.html`:95 | section | `Section 66.2` |
| `part-14-designing-llm-agent-products/module-70-shipping-products/section-70.2.html`:190 | section | `Section 66.5` |
| `part-14-designing-llm-agent-products/module-70-shipping-products/section-70.2.html`:295 | section | `Section 66.6` |
| `part-14-designing-llm-agent-products/module-71-tools-of-the-trade/section-71.1.html`:232 | section | `Section 48.11` |
| `part-14-designing-llm-agent-products/module-71-tools-of-the-trade/section-71.1.html`:250 | section | `Section 48.11` |
| `part-15-applications-of-llms-across-industries/module-78-manufacturing-llms/section-78.9.html`:685 | section | `Section 80.5` |
| `part-16-llm-agentic-ai-research-frontiers/module-80-frontier-architectures/section-80.3.html`:690 | section | `Section 7.7` |
| `part-16-llm-agentic-ai-research-frontiers/module-81-frontier-theory/section-81.1.html`:320 | section | `Section 81.6` |
| `part-16-llm-agentic-ai-research-frontiers/module-81-frontier-theory/section-81.2.html`:51 | section | `Section 81.5` |
| `part-16-llm-agentic-ai-research-frontiers/module-81-frontier-theory/section-81.2.html`:317 | section | `Section 81.7` |
| `part-16-llm-agentic-ai-research-frontiers/module-81-frontier-theory/section-81.3.html`:255 | section | `Section 81.5` |
| `part-16-llm-agentic-ai-research-frontiers/module-81-frontier-theory/section-81.3.html`:292 | section | `Section 81.8` |
| `part-16-llm-agentic-ai-research-frontiers/module-81-frontier-theory/section-81.4.html`:69 | section | `Section 81.6` |
| `part-16-llm-agentic-ai-research-frontiers/module-81-frontier-theory/section-81.4.html`:183 | section | `Section 81.7` |
| `part-16-llm-agentic-ai-research-frontiers/module-81-frontier-theory/section-81.4.html`:245 | section | `Section 81.9` |
| `part-2-understanding-llms/module-08-reasoning-test-time-compute/section-8.1.html`:149 | section | `Section 23.9` |
| `part-4-training-adaptation/module-16-fine-tuning-fundamentals/index.html`:38 | figure | `Figure 18.1.3` |
| `part-5-multimodal-llms/module-20-audio-music-generation/section-20.7.html`:142 | figure | `Figure 20.7.1` |
| `part-5-multimodal-llms/module-20-audio-music-generation/section-20.8.html`:142 | section | `Section 33.5` |
| `part-5-multimodal-llms/module-20-audio-music-generation/section-20.8.html`:148 | section | `Section 33.5` |
| `part-5-multimodal-llms/module-20-audio-music-generation/section-20.9.html`:145 | section | `Section 33.5` |
| `part-5-multimodal-llms/module-21-document-understanding-ocr/section-21.1.html`:60 | figure | `Figure 21.1.1` |
| `part-5-multimodal-llms/module-21-document-understanding-ocr/section-21.4.html`:193 | figure | `Figure 21.4.2` |
| `part-5-multimodal-llms/module-22-vision-language-models/section-22.4.html`:181 | figure | `Figure 22.4.1` |
| `part-5-multimodal-llms/module-24-vla-models/section-24.12.html`:166 | figure | `Figure 24.12.2` |
| `part-5-multimodal-llms/module-24-vla-models/section-24.12.html`:168 | figure | `Figure 24.12.2` |
| `part-5-multimodal-llms/module-24-vla-models/section-24.13.html`:208 | figure | `Figure 24.13.1` |
| `part-5-multimodal-llms/module-24-vla-models/section-24.5.html`:124 | figure | `Figure 24.5.1` |
| `part-5-multimodal-llms/module-24-vla-models/section-24.5.html`:153 | figure | `Figure 24.5.2` |
| `part-5-multimodal-llms/module-24-vla-models/section-24.6.html`:132 | figure | `Figure 24.6.1` |
| `part-5-multimodal-llms/module-25-tools-of-the-trade/section-25.3.html`:7 | section | `Section 7.4` |
| `part-6-agentic-ai/index.html`:40 | chapter | `Chapter 38` |
| `part-7-retrieval-information-extraction-with-llms/module-33-cross-modal-reasoning-rag/section-33.4.html`:162 | chapter | `Chapter 38` |
| `part-7-retrieval-information-extraction-with-llms/module-34-structured-information-extraction-ner/section-34.2.html`:32 | code_fragment | `Code Fragment 34.2.10` |
| `part-7-retrieval-information-extraction-with-llms/module-34-structured-information-extraction-ner/section-34.2.html`:84 | code_fragment | `Code Fragment 34.2.10` |
| `part-7-retrieval-information-extraction-with-llms/module-34-structured-information-extraction-ner/section-34.3.html`:29 | code_fragment | `Code Fragment 34.3.10` |
| `part-7-retrieval-information-extraction-with-llms/module-34-structured-information-extraction-ner/section-34.3.html`:100 | code_fragment | `Code Fragment 34.3.10` |
| `part-8-conversational-ai-with-llms/module-40-voice-realtime-multimodal/section-40.5.html`:184 | chapter | `Chapter 39` |
| `part-9-llm-evaluation-observability/module-43-specialized-evaluation/section-43.3.html`:50 | section | `Section 44.1` |
| `part-9-llm-evaluation-observability/module-43-specialized-evaluation/section-43.4.html`:50 | section | `Section 44.1` |
| `part-9-llm-evaluation-observability/module-45-tools-of-the-trade/section-45.2.html`:936 | section | `Section 45.11` |
| `part-9-llm-evaluation-observability/module-46-llm-as-judge-automated-evaluation/section-46.1.html`:37 | code_fragment | `Code Fragment 46.1.2` |
| `part-9-llm-evaluation-observability/module-46-llm-as-judge-automated-evaluation/section-46.2.html`:28 | code_fragment | `Code Fragment 46.2.6` |
| `part-9-llm-evaluation-observability/module-46-llm-as-judge-automated-evaluation/section-46.5.html`:28 | code_fragment | `Code Fragment 46.5.6` |

## 4. Category 3 — Image alt-text reference issues

### Cat. 3a — alt-text cites a number that does not exist

_None found._

### Cat. 3b — alt-text figure number disagrees with surrounding figcaption

_None found._

## 5. Category 4 — Caption cross-references to non-existent targets

`<figcaption>`, `<caption>`, `div.diagram-caption`, `div.code-caption` that reference another figure / section / code-fragment whose target does not exist.

_None found._

## 6. Recommended action plan

- **Review in-code comments (2 cases)** — Code-fragment comments like `# See Figure X.Y.Z` cite a non-existent figure. Comments are often ignored during renumber passes; update or remove.
- **Triage plain-text phantom mentions (53 cases)** — Prose mentions a figure/section/code-fragment number that does not exist anywhere. These were missed by the numbering audit because they live in code blocks or other excluded contexts; verify and rewrite each.
- **Optional hyperlinking pass (1072 plain-text mentions across 557 distinct labels; 105 labels mentioned 3+ times unlinked)** — The top labels in Section 3 are good candidates for a single search-and-replace pass that wraps `Figure X.Y.Z` in `<a href=...>Figure X.Y.Z</a>`. Skip cases where the paragraph already links the same label (Cat. 2a does NOT include those — they are flagged internally as low-priority and excluded from the top-30).
- **Note on Cat. 2a scope** — Cat. 2a includes plain-text `Chapter NN` references in module-overview and appendix introductions where the chapter is named alongside its title (e.g. 'Chapter 28 (Evaluation)') and is *already* linked elsewhere on the page. These are stylistic choices and may not be worth bulk-rewriting; review the top-30 list before deciding.
- **Re-run after fixes** — re-run `python scripts/_audit_prose_references.py` after any structural change (renumbering, deletion of figures, restructure of sections).
