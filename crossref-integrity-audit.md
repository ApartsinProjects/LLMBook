# Cross-reference Integrity Audit

Read-only audit of cross-reference integrity book-wide after the major restructuring (Waves 1-4: 
part renames, chapter renumbers, module dissolutions, appendix renumber).

Root: `E:/Projects/BookBlogsHome/LLMBook` | HTML pages scanned: 483

## 1. Summary

| Category | Audited | Broken |
|---|---:|---:|
| Chapter N references | 991 | 0 |
| Section X.Y references | 1751 | 15 |
| Part X (Roman) references | 171 | 0 |
| Appendix X references | 136 | 3 |
| Appendix X.N references | 4 | 3 |
| `<a href>` body links (non-external) | 8730 | 3820 |
|   ... target file missing | - | 3820 |
|   ... target ok, anchor missing | - | 0 |
| Figure caption chapter drift | - | 57 |
| Code Fragment caption chapter drift | - | 131 |
| Table caption chapter drift | - | 5 |
| Algorithm caption chapter drift | - | 0 |
| Pseudocode caption chapter drift | - | 11 |

**Grand total cross-refs audited:** 13722

**Grand total broken:** 4045

## 2. Top 15 broken cross-references

Sorted by file (alphabetical), then by line.

| # | File:Line | Kind | Cited as | Suggested fix |
|---|---|---|---|---|
| 1 | `front-matter/fm-reading-pathways.html:117` | Section | `Section 33.7` | Section 33.5 |
| 2 | `part-11-applications-across-industries/module-53-healthcare-llms/section-53.7.html:287` | Section | `Section 33.10` | Section 33.11 |
| 3 | `part-11-applications-across-industries/module-53-healthcare-llms/section-53.7.html:324` | Section | `Section 33.10` | Section 33.11 |
| 4 | `part-11-applications-across-industries/module-53-healthcare-llms/section-53.7.html:381` | Section | `Section 33.10` | Section 33.11 |
| 5 | `part-11-applications-across-industries/module-57-manufacturing-llms/index.html:157` | Section | `Section 27.7` | Section 27.6 |
| 6 | `part-11-applications-across-industries/module-58-creative-industries/section-58.2.html:659` | Section | `Section 27.7` | Section 27.6 |
| 7 | `part-12-frontiers/module-62-frontier-theory/section-62.1.html:320` | Section | `Section 33.6` | Section 33.5 |
| 8 | `part-12-frontiers/module-62-frontier-theory/section-62.2.html:317` | Section | `Section 33.7` | Section 33.5 |
| 9 | `part-12-frontiers/module-62-frontier-theory/section-62.3.html:292` | Section | `Section 33.8` | Section 33.11 |
| 10 | `part-12-frontiers/module-62-frontier-theory/section-62.4.html:69` | Section | `Section 33.6` | Section 33.5 |
| 11 | `part-12-frontiers/module-62-frontier-theory/section-62.4.html:183` | Section | `Section 33.7` | Section 33.5 |
| 12 | `part-12-frontiers/module-62-frontier-theory/section-62.4.html:245` | Section | `Section 33.9` | Section 33.11 |
| 13 | `part-12-frontiers/module-64-agi-trajectories/section-64.5.html:104` | Section | `Section 30.9` | Section 30.5 |
| 14 | `part-2-understanding-llms/module-10-inference-optimization/section-10.1.html:515` | AppendixSection | `Appendix P.4` | (no matching appendix) |
| 15 | `part-2-understanding-llms/module-10-inference-optimization/section-10.2.html:471` | AppendixSection | `Appendix P.1` | (no matching appendix) |

## 3. Caption-prefix drift (top 15)

A captioned block carries a chapter prefix that disagrees with its containing module.

| # | File:Line | Kind | Label | Label chapter | File chapter |
|---|---|---|---|---:|---:|
| 1 | `part-10-idea-to-product/module-41-product-management/section-41.2.html:45` | Figure | `Figure 31.2.1` | 31 | 41 |
| 2 | `part-10-idea-to-product/module-41-product-management/section-41.2.html:133` | Code | `Code 31.2.1` | 31 | 41 |
| 3 | `part-10-idea-to-product/module-41-product-management/section-41.2.html:177` | Code | `Code 31.2.2` | 31 | 41 |
| 4 | `part-10-idea-to-product/module-41-product-management/section-41.2.html:306` | Figure | `Figure 31.2.2` | 31 | 41 |
| 5 | `part-10-idea-to-product/module-41-product-management/section-41.2.html:338` | Figure | `Figure 31.2.3` | 31 | 41 |
| 6 | `part-10-idea-to-product/module-41-product-management/section-41.2.html:442` | Code | `Code 31.2.3` | 31 | 41 |
| 7 | `part-10-idea-to-product/module-41-product-management/section-41.2.html:506` | Code | `Code 31.2.4` | 31 | 41 |
| 8 | `part-10-idea-to-product/module-42-strategy-prioritization/section-42.3.html:45` | Figure | `Figure 31.1.1` | 31 | 42 |
| 9 | `part-10-idea-to-product/module-42-strategy-prioritization/section-42.3.html:147` | Code | `Code 31.1.1` | 31 | 42 |
| 10 | `part-10-idea-to-product/module-42-strategy-prioritization/section-42.3.html:196` | Code | `Code 31.1.2` | 31 | 42 |
| 11 | `part-10-idea-to-product/module-42-strategy-prioritization/section-42.3.html:201` | Figure | `Figure 31.1.2` | 31 | 42 |
| 12 | `part-10-idea-to-product/module-42-strategy-prioritization/section-42.3.html:316` | Figure | `Figure 31.1.3` | 31 | 42 |
| 13 | `part-10-idea-to-product/module-42-strategy-prioritization/section-42.3.html:369` | Figure | `Figure 31.1.4` | 31 | 42 |
| 14 | `part-10-idea-to-product/module-42-strategy-prioritization/section-42.3.html:406` | Code | `Code 31.1.3` | 31 | 42 |
| 15 | `part-10-idea-to-product/module-42-strategy-prioritization/section-42.3.html:467` | Code | `Code 31.1.4` | 31 | 42 |

## 4. Broken `<a href>` body links (top 15)

| # | File:Line | href | Resolved / issue |
|---|---|---|---|
| 1 | `appendices/appendix-a-mathematical-foundations/index.html:45` | `../glossary/section-i.2.html#gl-llm` | `appendices/glossary/section-i.2.html` |
| 2 | `appendices/appendix-a-mathematical-foundations/index.html:45` | `../glossary/section-i.3.html#gl-backpropagation` | `appendices/glossary/section-i.3.html` |
| 3 | `appendices/appendix-a-mathematical-foundations/index.html:45` | `../glossary/section-i.3.html#gl-cross-entropy` | `appendices/glossary/section-i.3.html` |
| 4 | `appendices/appendix-a-mathematical-foundations/index.html:46` | `../glossary/section-i.2.html#gl-transformer` | `appendices/glossary/section-i.2.html` |
| 5 | `appendices/appendix-a-mathematical-foundations/index.html:46` | `../glossary/section-i.4.html#gl-attention` | `appendices/glossary/section-i.4.html` |
| 6 | `appendices/appendix-a-mathematical-foundations/index.html:46` | `../glossary/section-i.3.html#gl-rlhf` | `appendices/glossary/section-i.3.html` |
| 7 | `appendices/appendix-a-mathematical-foundations/index.html:49` | `../glossary/section-i.3.html#gl-pretraining` | `appendices/glossary/section-i.3.html` |
| 8 | `appendices/appendix-a-mathematical-foundations/index.html:49` | `../glossary/section-i.3.html#gl-scaling-laws` | `appendices/glossary/section-i.3.html` |
| 9 | `appendices/appendix-a-mathematical-foundations/index.html:49` | `../glossary/section-i.4.html#gl-eval` | `appendices/glossary/section-i.4.html` |
| 10 | `appendices/appendix-a-mathematical-foundations/index.html:56` | `../glossary/section-i.4.html#gl-grounding` | `appendices/glossary/section-i.4.html` |
| 11 | `appendices/appendix-a-mathematical-foundations/index.html:56` | `../glossary/section-i.3.html#gl-peft` | `appendices/glossary/section-i.3.html` |
| 12 | `appendices/appendix-a-mathematical-foundations/section-a.1.html:41` | `../../appendices/glossary/section-i.2.html#gl-transformer` | `appendices/glossary/section-i.2.html` |
| 13 | `appendices/appendix-a-mathematical-foundations/section-a.1.html:43` | `../../appendices/glossary/section-i.4.html#gl-embedding` | `appendices/glossary/section-i.4.html` |
| 14 | `appendices/appendix-a-mathematical-foundations/section-a.1.html:60` | `../../appendices/glossary/section-i.4.html#gl-attention` | `appendices/glossary/section-i.4.html` |
| 15 | `appendices/appendix-a-mathematical-foundations/section-a.1.html:65` | `../../appendices/glossary/section-i.4.html#gl-cosine-similarity` | `appendices/glossary/section-i.4.html` |

## 5. References that point OUTSIDE the target structure

These are not declared in `book_structure.target.yaml`. Anything here is a candidate 
for a stale reference that did not get rewritten when the restructuring (Waves 1-4) ran.

### 5.1 Most common stale references

| Occurrences | Reference |
|---:|---|
| 5 | `Section 31.6` |
| 4 | `Section 27.6` |
| 4 | `Section 27.7` |
| 3 | `Section 33.7` |
| 3 | `Section 33.10` |
| 2 | `Section 31.7` |
| 2 | `Section 33.6` |
| 1 | `Section 43.2` |
| 1 | `Section 41.2` |
| 1 | `Section 33.8` |
| 1 | `Section 33.9` |
| 1 | `Section 30.9` |
| 1 | `Appendix P.4` |
| 1 | `Appendix S` |
| 1 | `Appendix T` |
| 1 | `Appendix U` |

### 5.2 First 30 suspect references (file:line)

| File:Line | Reference | Why |
|---|---|---|
| `front-matter/fm-reading-pathways.html:117` | `Section 33.7` | not declared in target.yaml |
| `part-10-idea-to-product/module-40-ideation/section-40.1.html:156` | `Section 43.2` | not declared in target.yaml |
| `part-10-idea-to-product/module-41-product-management/section-41.1.html:137` | `Section 41.2` | not declared in target.yaml |
| `part-10-idea-to-product/module-43-vibe-coding/section-43.2.html:38` | `Section 31.6` | not declared in target.yaml |
| `part-10-idea-to-product/module-46-compute-planning/section-46.4.html:846` | `Section 31.7` | not declared in target.yaml |
| `part-11-applications-across-industries/module-51-legal-llms/index.html:134` | `Section 27.6` | not declared in target.yaml |
| `part-11-applications-across-industries/module-53-healthcare-llms/section-53.7.html:287` | `Section 33.10` | not declared in target.yaml |
| `part-11-applications-across-industries/module-53-healthcare-llms/section-53.7.html:324` | `Section 33.10` | not declared in target.yaml |
| `part-11-applications-across-industries/module-53-healthcare-llms/section-53.7.html:381` | `Section 33.10` | not declared in target.yaml |
| `part-11-applications-across-industries/module-54-education-llms/index.html:131` | `Section 27.6` | not declared in target.yaml |
| `part-11-applications-across-industries/module-55-cybersecurity-llms/section-55.7.html:362` | `Section 27.6` | not declared in target.yaml |
| `part-11-applications-across-industries/module-57-manufacturing-llms/index.html:157` | `Section 27.7` | not declared in target.yaml |
| `part-11-applications-across-industries/module-57-manufacturing-llms/index.html:160` | `Section 31.6` | not declared in target.yaml |
| `part-11-applications-across-industries/module-58-creative-industries/section-58.2.html:690` | `Section 27.7` | not declared in target.yaml |
| `part-12-frontiers/module-61-frontier-architectures/section-61.4.html:311` | `Section 31.6` | not declared in target.yaml |
| `part-12-frontiers/module-62-frontier-theory/section-62.1.html:380` | `Section 33.6` | not declared in target.yaml |
| `part-12-frontiers/module-62-frontier-theory/section-62.2.html:361` | `Section 33.7` | not declared in target.yaml |
| `part-12-frontiers/module-62-frontier-theory/section-62.3.html:337` | `Section 33.8` | not declared in target.yaml |
| `part-12-frontiers/module-62-frontier-theory/section-62.4.html:69` | `Section 33.6` | not declared in target.yaml |
| `part-12-frontiers/module-62-frontier-theory/section-62.4.html:293` | `Section 33.7` | not declared in target.yaml |
| `part-12-frontiers/module-62-frontier-theory/section-62.4.html:295` | `Section 33.9` | not declared in target.yaml |
| `part-12-frontiers/module-64-agi-trajectories/section-64.5.html:104` | `Section 30.9` | not declared in target.yaml |
| `part-2-understanding-llms/module-10-inference-optimization/section-10.1.html:515` | `Appendix P.4` | not declared in target.yaml |
| `part-4-training-adapting/module-17-synthetic-data/section-17.3.html:520` | `Section 27.7` | not declared in target.yaml |
| `part-7-multimodal-generation/module-31-multimodal/section-31.1.html:604` | `Section 27.7` | not declared in target.yaml |
| `part-7-multimodal-generation/module-31-multimodal/section-31.5.html:38` | `Section 31.6` | not declared in target.yaml |
| `part-7-multimodal-generation/module-31-multimodal/section-31.5.html:572` | `Section 31.6` | not declared in target.yaml |
| `part-7-multimodal-generation/module-31-multimodal/section-31.6.html:646` | `Section 31.7` | not declared in target.yaml |
| `part-7-multimodal-generation/module-32-embodied-world-models/section-32.8.html:42` | `Section 27.6` | not declared in target.yaml |
| `toc.html:580` | `Appendix S` | not declared in target.yaml |

## 6. Did the restructure introduce broken references?

Any reference whose target is NOT in `book_structure.target.yaml` is a strong 
indicator that it pre-dates the restructure and never got rewritten. Conversely, 
a broken reference whose target IS declared in target.yaml means the disk layout 
never caught up to the plan (file missing).

- Broken refs whose target IS declared in target.yaml (disk layout did not catch up): **8**
- Broken refs whose target is NOT in target.yaml (stale reference pre-restructure or phantom): **13**

These are post-restructure suspects (target declared but file missing). Top 10:

| File:Line | Kind | Cited as | Suggested fix |
|---|---|---|---|
| `part-11-applications-across-industries/module-58-creative-industries/section-58.2.html:659` | Section | `Section 27.7` | Section 27.6 |
| `part-12-frontiers/module-62-frontier-theory/section-62.1.html:320` | Section | `Section 33.6` | Section 33.5 |
| `part-12-frontiers/module-62-frontier-theory/section-62.2.html:317` | Section | `Section 33.7` | Section 33.5 |
| `part-12-frontiers/module-62-frontier-theory/section-62.3.html:292` | Section | `Section 33.8` | Section 33.11 |
| `part-12-frontiers/module-62-frontier-theory/section-62.4.html:183` | Section | `Section 33.7` | Section 33.5 |
| `part-12-frontiers/module-62-frontier-theory/section-62.4.html:245` | Section | `Section 33.9` | Section 33.11 |
| `part-2-understanding-llms/module-10-inference-optimization/section-10.2.html:471` | AppendixSection | `Appendix P.1` | (no matching appendix) |
| `part-2-understanding-llms/module-10-inference-optimization/section-10.2.html:471` | AppendixSection | `Appendix P.3` | (no matching appendix) |

## 7. Disk vs target structure gaps

- Chapters declared in target.yaml are all present on disk.
- All declared appendix letters are present on disk.

---

Audit generated by `scripts/_audit_crossref_integrity.py` (read-only).
