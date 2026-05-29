# Dropped-Resource References Cleanup Report

Sweep of HTML book sources for text-only references to resources deleted in v9 (Appendix N "Master Reference Tables", Appendix P/AD/AI/AE/AF "Freshness Index"/"Pedagogy Kit"/"Production-Patterns Playbook", and the Glossary). Audit `.md` files, migration scripts, and `KDP/html2epub/tests/fixtures/` were excluded per scope.

## Files Edited

- `appendices/appendix-p-reading-pathways/index.html` — deleted four list items referencing "Appendix AI (2026 Freshness Index)" and "Appendix AD (Master Reference Tables)" across pathways 4, 6, and 8; rewrote pathway-7 step pointing to nonexistent `appendix-p-course-syllabi` so it links to Appendix O (Course Syllabi) as the actual pedagogy resource.
- `appendices/appendix-o-course-syllabi/index.html` — removed "Appendix K (Glossary)" line item; replaced with a pointer to Appendix G (Problem-Solution Key). Fixed two stale per-appendix letters (Appendix D/K mislabeling on the HuggingFace/LangChain bullet).
- `appendices/appendix-g-problem-solution-key/index.html` — fixed previous-nav link from nonexistent `appendix-p-course-syllabi` to Appendix F (Agent Frameworks).
- `appendices/appendix-j-git-collaboration/section-j.4.html` — "Continue to Appendix K: Glossary" rewritten to point at Appendix K (Experiment Tracking); next-nav link `../glossary/index.html` retargeted to `../appendix-k-experiment-tracking/index.html`.
- `appendices/appendix-s-war-stories/index.html` — two prose references to "Appendix AE" rewritten as "Chapter 35's LLMOps coverage".
- `front-matter/index.html` — outdated migration note pointing to nonexistent `appendix-p-course-syllabi`; rewritten to point at Appendix O and Appendix P.
- `part-3-working-with-llms/module-13-llm-apis/section-13.2.html` — "Appendix AE: production-patterns playbook" rewritten to "Chapter 35's LLMOps coverage".
- `part-3-working-with-llms/module-16-tools-of-the-trade/section-16.5.html` — "Appendix P tracks the model-deprecation calendar" rewritten to reference provider blogs + status RSS.
- `part-5-retrieval-conversation/module-23-rag/section-23.1.html` — "the Knowledge Storage Spectrum (Appendix G: Master Reference Tables)" reworked to cite Section 18.1's adaptation decision tree (Appendix G is now Problem-Solution Key). Postmortem callout's "Pattern P2 in Appendix AE" rewritten to "Chapter 35's LLMOps coverage".
- `part-5-retrieval-conversation/module-23-rag/section-23.2.html` — Pattern-P1 catalogue link rewritten away from Appendix AE.
- `part-8-evaluation-production/module-34-evaluation-observability/section-34.5.html` — Pattern-P3 catalogue link rewritten away from Appendix AE.
- `part-8-evaluation-production/module-35-production-engineering/section-35.4.html` — two prose references to Appendix AE rewritten (Pattern P2 mid-callout and Pattern P5 catalogue).
- `part-9-safety-security-ethics/module-39-tools-of-the-trade/section-39.5.html` — "Appendix P tracks the calendar" rewritten to point at jurisdictional channels.
- `part-10-idea-to-product/module-46-compute-planning/section-46.3.html` — "Glossary" in end-of-book pointer replaced with link to Appendix G (Problem-Solution Key).
- `part-10-idea-to-product/module-48-shipping-deploying/section-48.5.html` — Pattern-P2 catalogue link rewritten away from Appendix AE.
- `part-11-applications-across-industries/index.html` — "and the 2026 freshness index" rewritten to list actually existing appendices.
- `part-11-applications-across-industries/module-54-education-llms/index.html` — "Appendix AF (Pedagogy Kit)" with `appendix-p-course-syllabi` link rewritten to Appendix O (Course Syllabi).
- `part-12-frontiers/module-61-frontier-architectures/section-33.11.html` — "Use the 2026 Freshness Index to keep up" rewritten to track arxiv + bibliography channels.
- `KDP/metadata/description.html` — "28 appendices" sentence listed Glossary and Master Reference Tables; rewritten to "19 appendices" with the current appendix lineup.

## Verification

Final sweep across the book HTML (excluding the test-fixture and audit reports) returned zero matches for `Master Reference Tables`, `Freshness Index`, `Appendix AD/AE/AI/AF`, `appendix-p-course-syllabi`, `glossary/index`, `the Glossary`, `see the Glossary`, or `Glossary entry`.
