# Front-Matter Rewrite Report

Date: 2026-05-16. Scope: `front-matter/*.html`. Voice: substance-first, no marketing hype, second-person framing.

## Per-File Summary

### foreword.html (Why This Book Exists)
- Word count: 345 -> 730 words.
- Theme preserved: gap between research pace and practitioner needs; "no need to read in order".
- New: explicit 2026 model lineup (GPT-5-omni, Claude 4, Gemini 2 Pro Vision, Llama 4 Scout, DeepSeek-R1, Veo 3, Sora 2, Genie 3, pi-0.5, OpenVLA, MCP). Introduces the three unifying theses (alignment-thesis, agents-are-decoders, eval-is-the-product) as the through-lines that connect parts.
- Removed: stale "35 chapters" count and explicit ask-for-reviews paragraph (the latter moved to about-authors).
- Links added: Part IV alignment, Part VI agents, Part VII multimodal, Chapter 5 decoding, Chapter 34 eval, Part XII frontiers, Appendix R.

### look-inside-preview.html (What's Inside) [NEW FILE]
- Word count: 0 -> 715 words (file did not exist; was referenced by FM index).
- Shows three pages of the book's character: a Key Insight callout from Chapter 26 (the agents-are-decoders thesis), a LoRA from-scratch + Library Shortcut pair from Chapter 19, and the part-dependency diagram (Figure FM.2.1).
- Links added: Chapter 26 (agents), Chapter 5 (decoding), Chapter 19 (PEFT), Appendix R.

### fm-what-this-book-covers.html
- Word count: 1270 -> 1272 words (steady; structural integrity required all 12 part summaries).
- Theme preserved: 12 parts + reference appendices + dependency diagram; what is NOT covered.
- Updated: 11 parts -> 12 parts (corrected for v10 structure); 32 appendices -> 21 appendices (A-U); 35 chapters context dropped (now 65 chapter slots across 12 parts). Each part summary names a concrete 2025-2026 technique or model (DSPy, MCP, A2A, AG-UI, RLHF/DPO/KTO/IPO, OpenVLA, pi-0.5, Veo 3, Sora 2, Genie 3, Imagen 4, FLUX.1 Pro, HLE, ARC-AGI-2).
- Removed: "What Makes This Book Different" big-picture callout (was self-promotional).
- Links added: Chapter 7, Chapter 11, Chapter 20, Chapter 23, Chapter 26, Chapter 31, Chapter 32, Part XII, appendices index.

### fm-who-should-read.html
- Word count: 715 -> 942 words.
- Theme preserved: assumed background table.
- Restructured: six-bullet audience list -> three explicit personas (Software Engineer Adding LLMs, ML Engineer Crossing into LLMs, Researcher/Grad Student/Course Builder), each with a one-paragraph yes/no test. Routes per persona point at Appendix R pathways.
- Removed: vague "career changers" and "university students" sub-bullets folded into the three personas.
- Links added: Chapter 0, Appendix R, Appendix Q.

### fm-how-to-use.html
- Word count: 723 -> 869 words.
- Theme preserved: callout catalogue and code conventions.
- Restructured around the user's framing: "linear / reference / course / self-study" as four pathway callouts. Points at Appendix R (pathways), Appendix Q (syllabi), Appendix S (intermediate projects), Appendix T (capstone), Appendix U (war stories), Appendix G (problem-solution key) as the routing layer.
- Removed: lengthy callout-type catalogue trimmed to the five most consequential (Big Picture, Key Insight, Warning, Library Shortcut, Research Frontier); fun-fact and why-it-matters classes excluded per spec.
- Links added: appendices Q, R, S, T, U, G.

### about-authors.html
- Word count: 303 -> 462 words.
- Theme preserved: bios, photos, homepage links, CSS styling.
- Tightened factual claims; clarified the academic-to-industry-and-back arc for each author; tied each author's research to specific book parts (Pragmatic AI to Parts III/VI/IX; Yehudit's industry collaborations to Part XI). Added a closing note moving the review-request from the foreword.

### copyright.html
- Word count: 646 -> 646 words (no edits).
- Verified: Copyright 2026, Fifteenth Edition, ISBN-on-publication line. All correct per `book_structure.yaml`.

## Constraints Verified
- 0 em-dashes and 0 prose double-dashes across all seven files (only HTML comment `<!-- -->` delimiters and CSS `var(--*)` remain, both syntactic).
- 0 banned hype words (revolutionary, groundbreaking, definitive, must-read, world-class, comprehensive).
- Banned `fun-fact` and `why-it-matters` callout classes: none introduced.
- All FM links to former `fm-reading-pathways.html` and `fm-course-syllabi.html` redirected to `appendices/appendix-r-reading-pathways/index.html` and `appendices/appendix-q-course-syllabi/index.html`, including in `front-matter/index.html`.
