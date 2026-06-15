# Graduate-Depth Audit: Part 14 (Applications Across Industries)
| Section | Title (short) | Verdict | Missing piece (only if not COURSE-READY) |
|---|---|---|---|
| 67.1 | Legal use cases that work | COURSE-READY | |
| 67.2 | Legal failure modes | COURSE-READY | |
| 67.3 | Bar association / regulatory rules | COURSE-READY | |
| 67.4 | Verified-RAG architecture (legal) | COURSE-READY | |
| 67.5 | Legal vendors and further reading | CATALOG-OK | |
| 68.1 | Finance use cases that ship | COURSE-READY | |
| 68.2 | Finance failure modes | COURSE-READY | |
| 68.3 | Finance regulatory framework | COURSE-READY | |
| 68.4 | Tiered LLM trust architecture | COURSE-READY | |
| 68.5 | Finance vendors and further reading | CATALOG-OK | |
| 69.1 | Healthcare use cases that work | COURSE-READY | |
| 69.2 | Healthcare failure modes | COURSE-READY | |
| 69.3 | Healthcare regulatory framework | COURSE-READY | |
| 69.4 | HIPAA-compliant deployment patterns | COURSE-READY | |
| 69.5 | Healthcare vendors and further reading | CATALOG-OK | |
| 70.1 | Education use cases that work | COURSE-READY | |
| 70.2 | Education failure modes | COURSE-READY | |
| 70.3 | Education regulatory/policy framework | COURSE-READY | |
| 70.4 | Pedagogically-scaffolded tutor architecture | COURSE-READY | |
| 70.5 | Education vendors and further reading | CATALOG-OK | |
| 71.1 | Defensive (blue team) use cases | COURSE-READY | |
| 71.2 | Offensive (red team) use cases | COURSE-READY | |
| 71.3 | LLM-specific attack surface | COURSE-READY | |
| 71.4 | Trust boundaries for LLM systems | COURSE-READY | |
| 71.5 | Cybersecurity vendors and further reading | CATALOG-OK | |
| 72.1 | Government use cases that work | COURSE-READY | |
| 72.2 | Government failure modes | COURSE-READY | |
| 72.3 | Government regulatory/policy framework | COURSE-READY | |
| 72.4 | Public-sector grounded assistant architecture | COURSE-READY | |
| 72.5 | Government vendors and postmortems | CATALOG-OK | |
| 73.1 | Manufacturing use cases that work | COURSE-READY | |
| 73.2 | Manufacturing failure modes | COURSE-READY | |
| 73.3 | Manufacturing regulatory/standards framework | COURSE-READY | |
| 73.4 | Plant-floor maintenance copilot architecture | COURSE-READY | |
| 73.5 | Manufacturing postmortems / named-vendor cases | COURSE-READY | |
| 73.6 | Music, video, design, marketing copy | DEPTH-GAP | Tool-by-tool capability survey; teaches the iterate-not-one-shot workflow and brand-consistency mechanism but lacks one end-to-end worked production case with the failure/eval loop the other chapters carry |
| 73.7 | Creative workflow, rights, licensing | COURSE-READY | |
| 73.8 | Ranking, retrieval, personalization | COURSE-READY | |
| 73.9 | LLM-powered recommendation and search | COURSE-READY | |
| 73.10 | Conversational discovery / named-vendor cases | COURSE-READY | |
| 74.1 | Platforms (industry solution stack) | CATALOG-OK | |
| 74.2 | Libraries and frameworks | CATALOG-OK | |
| 74.3 | Datasets and benchmarks | CATALOG-OK | |
| 74.4 | Models | CATALOG-OK | |
| 74.5 | External reading and communities | CATALOG-OK | |

## Summary
- COURSE-READY: 28 | DEPTH-GAP: 1 | NOT-SELF-CONTAINED: 0 | CATALOG-OK: 9
- Top sections most worth enriching:
  1. 73.6 (Music, video, design, marketing copy): the only true DEPTH-GAP. Add one end-to-end worked production case (e.g. a brand campaign or audiobook run) carried through the failure/eval loop, matching the postmortem-plus-architecture depth of 73.4, 73.5, and 73.7. The legal/IP machinery already lives next door in 73.7; this section is the lone vendor-capability survey in an otherwise mechanism-driven chapter.
  2. 73.10 (Conversational discovery): COURSE-READY and strong, but its "What's Next" link points back to 73.2 instead of forward to Chapter 74; a one-line nav fix would close the only structural seam found in the part.
  3. Cross-reference hygiene across Part 14: several sections carry stale link text from an earlier numbering scheme (e.g. 67.5 "Section 74.2 (Education, Legal & Creative)", 68.5 "Section 69.1 (LLMs in Finance & Trading)" and a bare "4," bullet, 72.5 bare "4," bullet, 73.8/73.9 "Section 75.x" references, 73.9 titled "Section 75.4" in its meta/H-tags). Content is COURSE-READY; the mislabeled xrefs are a publication-QA pass, not a depth gap.
