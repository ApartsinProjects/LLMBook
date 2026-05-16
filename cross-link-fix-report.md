# Cross-Link Integrity Fix Report

## P1 (number drift) - mechanical text rewrites

- Chapter 09 -> Chapter 10 (Inference Optimization): 12 anchor/prose rewrites (across part-12 module-61 index, module-09 reasoning index, module-13 apis index, module-15 hybrid index, module-19 peft index, appendix-l/section-l.4, module-10 title-meta)
- Chapter 7 -> Chapter 5 (appendix-c-huggingface section-c.1): 1
- Chapter 9 -> Chapter 18 (appendix-c-huggingface section-c.3): 1
- Chapter 13 -> Chapter 20 (appendix-c-huggingface section-c.4): 1
- Chapter 13 -> Chapter 14 (module-07 section-7.2): 1
- Chapter 15 -> Chapter 17 (module-07 section-7.4): 1
- Chapter 17 -> Chapter 18 (module-07 section-7.5): 1
- Chapter 20 -> Chapter 11 (module-07 section-7.7): 1
- Chapter 24 -> Chapter 20 (module-20 section-20.5): 1
- Chapter 25 -> Chapter 26 (module-29 index + section-29.4): 1
- Chapter 27 -> Chapter 31 (module-07 section-7.1): 1
- Chapter 29 -> Chapter 34 (module-07 section-7.3): 1
- Chapter 52 -> Chapter 37 (module-37 section-37.11 + 37.12): 2
- Section 9.5 -> Section 10.5 (module-10 section-10.3 + 10.6): pattern fired but text already aligned in some files
- Appendix M.x -> Appendix L.x in appendix-l/index.html section cards: 5 (plus title-attr cleanups: 3)
- Appendix O.x -> Appendix P.x in appendix-p-docker-containers/index.html section cards: 4
- Appendix P -> Appendix L in appendix-k/section-k.4: 0 (already showed Appendix L)
- Chapter 09 (Inference) prose fix in appendix-l/index.html prerequisites + introduction: 2

Total P1 unique-occurrence fixes applied: ~46 (counting card relabel batches as one each). Many additional Chapter 9/10, Chapter 6/7, Chapter 7/8, Chapter 8/9 occurrences were SKIPPED because their host files are in scope of concurrent agents (see below).

## P0 (mismatched topic) - href re-targets

- "Hugging Face" / "HuggingFace" -> Appendix C index: 37 href retargets across the book (anchor text preserved)
- "structured output" / "structured outputs" -> section-13.2.html: 11 href retargets (9 by script + 2 manual stragglers in section-10.3 and section-10.4 and 35.2)
- "open-weight model(s)" / "Mixture-of-Experts" -> section-8.2.html: 8 href retargets (6 by script + 2 manual stragglers in section-37.1, section-18.4)
- "knowledge graph(s)" pointing to module-23-rag/section-23.4.html: 2 plain-text downgrades (no canonical home; left text without link)

Plain-text downgrades (no canonical home): 2 (knowledge graph)

## Skipped (in-flight)

Per task instructions, files within scope of concurrently running agents were skipped. The skip rule combined two signals: (a) path matched an agent's declared scope, (b) file mtime within 60 seconds (active write). Aggregate:

- 57 files under Part 10 review (a302d781ffcca698c)
- 54 files under Tools enrichment (a7f5ae77364056772 - tools-of-the-trade directories)
- 53 files actively being written (mtime within 60s)
- 32 files under Part 11 review (ac85d7336912c84bf)
- 18 files under Part 12 comprehensive (a6a59411b8cb8e555 - modules 63/64/65)
- 14 files under Ch 31/32 dup resolution (af19ea3764d791b97)
- 11 files under MLOps authoring (affba95967a5af327 - appendix-n/o)
- 8 files in front-matter/ under FM rewrite (a92273d913adbd64a)
- 3 files under E.2/E.3 stub authoring (ad70ce3c847429e81)
- 2 files under F.2/F.3 stub authoring
- 2 files under I.6/I.7 stub authoring

Skipped P0/P1 work that intersects with these agent scopes (to be re-run after they complete):
- All Hugging Face href retargets in Part 1 modules 0-5, Part 2 modules 7/8/10/11, Part 4 modules 17/18, Part 8/9 sections, capstone, appendix-b/h - 19+ files were in-flight at script-run time
- structured output / open-weight retargets in Part 10/11/12 modules
- Number drift in Part 1 modules 0-5 (Chapter 6/7/8/9 references)
- Number drift in Part 10 module-46/47 sections
- Number drift in front-matter (fm-how-to-use.html)
- Section 30.x -> Section 37.x in module-37 (Part 9 was modified by another writer; some sections still showed Section 30 labels)

## Manual review

- `appendices/appendix-g-problem-solution-key/index.html:598` - "10.3 Hardware Landscape" with href to section-10.3.html (Speculative Decoding). Module-10 has no "Hardware Landscape" section. Ambiguous: text may refer to a removed section. Defer.
- "catastrophic forgetting" -> section-18.3.html (SFT): destination DOES mention catastrophic forgetting; left link as-is since no dedicated section exists. Audit P0 was a false positive driven by topic-overlap heuristic.
- "Instructor library" -> section-13.2.html (Structured Output & Tool Integration): destination IS correct (Instructor is documented in that section); audit P0 was a false positive.
- "Error Recovery, Resilience and Graceful Degradation" in section-48.5.html: no section in module-48 matched the title; left unmodified pending content authoring.
- "Production Observability and Cost Control" in section-38.2.html: no section in module-38 matched the title; left unmodified.
- "rate limit(ing)" -> module-35 section: no section title in module-35 contains "rate limit" or "throttle"; current pointer is to section-35.2.html (Frontend & UIs). Left as-is pending a dedicated rate-limiting section.
- "Section 30.x -> Section 37.x" in module-37: the module-37 section files were in-flight when the script ran. Defer until Part 9 review completes.
- "Section 11.2" -> "Section 14.2" in section-14.3 of prompt engineering: applied but section-14.3 was modified at 184s before run; recheck after Part 3 tools-of-the-trade completes.

## Summary

- Total files modified: 60 (script) + 6 (manual) = 66 files
- Total replacements applied: ~95 (54 P0 + ~41 P1)
- Audit-cataloged total: 132 P0 + 125 P1 = 257
- Coverage: ~37% of audit (limited by heavy concurrent-agent overlap; the audit ran before the v10 reshuffle and before this round of write tasks)
- All eligible P0 patterns for "Hugging Face", "structured output", "open-weight" were fixed in non-in-flight files
- The remaining ~160 occurrences are spread across files currently being edited by the named concurrent agents and should be re-attacked when those agents complete

The audit and the v10 directory reshuffle (appendix-m -> appendix-n distributed-ml, appendix-n -> appendix-p docker, new appendix-m-data-engineering) interact: many audit references to "Appendix M Distributed ML" or "Appendix N Docker" are now pointing at the renamed appendices. The label fixes applied here use the new v10 letter assignments (M -> L, M -> M-data, N -> N-distributed, O -> P-docker) for the index.html section cards. Section-level "Appendix X" prose mentions in audit files that are in-flight remain to be cleaned in a follow-up pass.
