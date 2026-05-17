# Cycle 3 Audit, Parts 5-8

Audited 2026-05-17. Scope: Part 5 (modules 20-25), Part 6 (modules 26-30), Part 7 (modules 31-36), Part 8 (modules 37, 40, 41).

Cycle 2 left Parts 5-8 in a state where almost every visible chapter number, section number, figure caption, and chapter-nav prev/next link was stale. Waves 17a-h between cycles 2 and 3 fixed most of the bulk-renumbering layer and authored the previously-empty Ch 36. The audit below confirms what landed and lists what is still wrong.

## Resolved since cycle 2

- **Ch 36 (Retrieval Tools of the Trade) is now fully authored.** 195 KB across the index plus 5 sections (36.1 Platforms / 36.2 Libraries and Frameworks / 36.3 Datasets and Benchmarks / 36.4 Models / 36.5 External Reading). All concrete tools are present (Pinecone, Turbopuffer, Weaviate, Qdrant, Milvus, Chroma, pgvector, LanceDB, Marqo, Vald, FAISS, MongoDB Atlas Vector Search, Azure AI Search, Elasticsearch, OpenSearch, Vespa; LangChain, LlamaIndex, Haystack, DSPy; OpenAI text-embedding-3, Cohere Embed-4, Voyage, BGE-M3, NV-Embed, Stella, ColPali; MS MARCO, BEIR, MTEB, MIRACL, HotpotQA, FRAMES, RAGAS, RAGBench, CRAG, LongRAG). 193 mentions of these canonical tool names across the chapter. Decision trees, comparison tables, and code snippets present. This was the single biggest content gap in Parts 5-8 in cycle 2.
- **H2/H3 visible numbering now matches IDs in Chs 25, 31, 32, 33, 34, 35, 36, 37, 40, 41.** Programmatic scan of `<h2 id="N-M-K-..."> N.M.K ...` returns 0 mismatches across the entire Part 5-8 scope (one apparent outlier in Ch 30 is an H2 with a four-segment ID `30-1-2-5`, where the visible "30.1.2.5" matches the ID, not a renumber bug).
- **Figure / Table / Code Fragment chapter prefixes now match the section chapter.** Programmatic scan finds 0 captions where the figure number disagrees with the containing chapter directory. Cycle 2 listed dozens of stale "Figure 22.X.Y / 34.X.Y / 39.X.Y" captions across Chs 21, 22, 24, 31, 32, 35, 37, 40. All clean now.
- **Section-card descriptions for Ch 37 are no longer the "Conversational AI." placeholder.** 37.1 reads "Every conversational AI system makes fundamental architectural decisions...", 37.2 "Persona design transforms a generic language model...", 37.3 "Memory is what transforms a stateless LLM...", 37.4 "Real conversations are messy." Cycle 2 flagged all four as identical placeholders.
- **Chapter-nav prev/next is consistent for all 20 chapters in Parts 5-8.** Programmatic check of `nav-num` vs `href` chapter number across all `module-*/index.html` returns 0 mismatches. Cycle 2 had Ch 20 / 21 / 22 / 23 / 24 / 25 / 32 / 33 / 37 / 40 / 41 all broken; all clean now.
- **In-prose `<a href="section-N.M.html">Section X.Y</a>` mismatches resolved.** 0 hits where the visible Section X.Y disagrees with the href section-N.M (cycle 2 had dozens). Wave 17d worked.
- **Section 24.13 botched `T: VLA Models...` span fixed.** The orphan `<span>` artifact on line 27 is now a clean pagefind-meta tag.
- **Part-index sections-list pages (Parts 5, 7, 8) match current chapter and section titles.** Wave 17e rebuilt them; titles align with the actual H1 of every module.
- **Section 32.X "doesn't exist" cross-refs in prose mostly cleaned up.** Of the ~10 stale `Section 32.5 / 32.6 / 32.7 / 32.8 / 32.9` body-text references cycle 2 listed, only one survives (a code comment in 32.2, see below).
- **`Section 42.X` cross-refs from Parts 5-8 to Part 9 eval foundations are correct.** Spot-check confirms Ch 42 has sections 42.1-42.12 and the `Section 42.1 / 42.9 / 42.2` references in Parts 5-8 prose resolve.

## Remaining issues

### P1, presentation bugs

1. **Botched pagefind-meta `<span>` artifacts in 15 Part 5 section files.** Same pattern as the Ch 24.13 issue waves 17 fixed, but the fix did not propagate. Wave 17h fixed exactly one file; the other 15 were missed. The leftover fragment renders as plain text immediately after the opening `<main>` tag, visible to readers.
   - `part-5-multimodal-llms/module-20-audio-music-generation/section-20.6.html` line 29: `></span>P: Audio, Music, and Video Generation" hidden=""></span>`
   - `.../section-20.7.html`, `.../section-20.8.html`, `.../section-20.9.html`, `.../section-20.10.html`: same `P:` fragment
   - `part-5-multimodal-llms/module-22-vision-language-models/section-22.6.html` through `section-22.9.html`: `R: Vision-Language and Omni Models" hidden="">` fragment (4 files)
   - `part-5-multimodal-llms/module-24-vla-models/section-24.7.html` through `section-24.12.html`: `T: VLA Models and LLM-Powered Robotics" hidden="">` fragment (6 files)
   The single-letter prefix is the surviving tail of "Cha**P**ter 20", "Chapte**R** 22", and "Chap**T**er 24" after a botched edit truncated the opening of the `data-pagefind-meta="chapter:Chapter NN: Title"` attribute.
2. **526 double-wrapped `<strong><strong>Figure / Table / Code Fragment</strong></strong>` tags across 108 files.** Waves 17 figure-caption renumber sweep wrapped the existing `<strong>` in another `<strong>`. Visually identical to single bold (CSS bold does not stack), but invalid HTML and noise in source. Affects basically every figure caption in every section of Chs 20-25, 31-35, 37, 40, 41.

### P2, in-prose stale chapter references

3. **In-section "What's Next" paragraphs still cite the OLD chapter numbering.** Wave 17 chapter-nav rebuild did not touch the in-page What's Next text. Affected:
   - `section-20.10.html`: "Chapter 33 ends here. The next chapters of Part 7 cover the rest of the multimodal-generation landscape: Chapter 34 covers document understanding..." (entire paragraph uses old 33/34/35/36/37-43 scheme; should be Ch 20/21/22/23/22/40/24/33/25 in current part).
   - `section-20.5.html`: "Chapter 33 opens on the modality with the steepest 2025-2026 capability gain: video..."
   - `section-22.9.html`: "Chapter 37 closes here. Chapter 40: Streaming and Real-Time Multimodal goes deeper..." (Ch 40 ref is correct; "Chapter 37 closes here" should be "Chapter 22 closes here").
   - `module-25-tools-of-the-trade/index.html`: "Part VIII turns to evaluation and production... Chapter 46 closes Part VIII with the eval and production stack." (Ch 46 does not exist; Part VIII is Conversational AI not eval; the next part after Part 5 is Part 6).
   - `module-27-tool-use-protocols/section-27.6.html`: "the next chapter, Chapter 47: Safety, Ethics & Regulation" (Ch 47 is in Part 10 Adversarial Security; the actual next chapter after Ch 27 is Ch 28 in the same Part 6).
   - `section-32.4.html`: "In Chapter 37: Building Conversational AI Systems..." (this one is correct, Ch 37 is the next chapter in flow).
   - `section-33.4.html`: "Chapter 33 closes Part VII's coverage of multimodal generation... The remaining chapters in Part... Chapter 25..." (Ch 25 is in Part 5 not Part 7; cross-part link confusion).
   - `section-40.1.html`: "Chapter 26: AI Agent..." and "Chapter 29..." in What's Next (Ch 26 / Ch 29 are in Part 6; from Ch 40 the next chapter is Ch 41).
   - `section-40.5.html`: "Chapter 39 closes here. The next chapters in Part VII (39, 40, 41) cover Vision-Language-Action models, LLM robotics, and world models, then we return to Chapter 33 for cross-modal retrieval..." (entire paragraph is the old Part-7 mega-chapter structure; the actual chapter is Ch 40 in Part 8 and the next chapter is Ch 41).
   - `module-37-conversational-ai/index.html`: "In the next part, Part VI: Agentic AI..." (Part VI is BEFORE Part VIII; the next chapter is Ch 40 in the same part).
   - `module-23-3d-generation-neural-scenes/section-23.5.html`: "Chapter 23 closes here. Chapter 22: Unified Multimodal..." (Ch 22 comes BEFORE Ch 23; the actual next chapter is Ch 24).
4. **Standalone "Chapter NN" mentions in body prose still stale in roughly 30 spots.** Survivors from the cycle 2 list:
   - `section-22.9.html`: "Chapter 37 closes here." / "Chapter 40: Streaming and Real-Time Multimodal" (Ch 37/40 references reference old chapter numbering or wrong cross-link).
   - `section-24.3.html`: "Chapter 40" (in context of pi-0.5 split; Ch 40 was old LLM Robotics, now Ch 24's second half).
   - `section-24.6.html`: "(covered in Chapter 41)" (Ch 41 was old World Models; now Ch 24.13 covers world models).
   - `section-24.9.html`: "Gaussian-splat scenes (covered in Chapter 41)" (same problem; Gaussian-splat coverage is now in Ch 23).
   - `section-24.13.html`: "Chapter 40 closes the LLM-robotics arc that Chapter 24 began" (entire sentence assumes Ch 40 robotics, which is wrong now).
   - `section-33.4.html`: "Chapter 31 (multimodal LLMs), Chapter 37 (pipeline vs native), Chapter 38 (streaming)" (all three numbers stale: 31->22, 37->22, 38->40).
   - `section-26.4.html`: "Chapter 34" used for eval (Ch 34 is now Structured IE; eval is Ch 42).
   - `section-28.4.html`: "Chapter 34" similarly used for eval.
5. **`Chapters 21 through 24` / `Chapters 22 through 24` range references unchanged.** Three occurrences cycle 2 flagged are all still present, all semantically nonsensical in current numbering:
   - `module-26-ai-agents/index.html` Looking Back: "Parts I through V built up to ... the four-step pattern that everything in Chapters 21 through 24 specializes" (Ch 21-24 are document AI / VLMs / 3D / VLA, not agent specializations).
   - `module-29-specialized-agents/index.html` meta description AND body: "While Chapters 22 through 24 cover general agent principles" (Ch 22-24 are VLMs / 3D / VLA, not agents).
6. **Two leftover stale `Section 32.5 / 38.2` code-comment references.** Pure cosmetic but they leak old structure:
   - `section-32.2.html` line 192: `# Text-to-SQL pipeline (covered in Section 32.5)` (Text-to-SQL is now Sec 32.3 not 32.5).
   - `section-22.9.html`: `# See Section 38.2 for the full protocol walkthrough.` (Sec 38.2 does not exist; Ch 38 was the old Streaming chapter, now Ch 40).
7. **Section card descriptions for Ch 34 still partly placeholder / truncated.** Cycle 2 flagged:
   - 34.3 desc: "Why this matters for production pipelines." (placeholder-like generic).
   - 34.5 desc: "Consider the following passage: 'Dr." (truncated mid-sentence; auto-derived from body and never rewritten).

### P3, structural and consistency

8. **All 6 cycle-1 content-consolidation candidates still present.** None resolved:
   - **Agentic RAG**: `27.5` (29 KB, 7 hits on Corrective/CRAG/Self-RAG/Adaptive RAG) and `32.2` (94 KB, 15 hits) both still cover the same agentic-RAG techniques.
   - **Memory**: `26.6` (41 KB) "Memory Architecture for Agents" with five-layer taxonomy and `37.3` (209 KB, 55 hits on MemGPT / sliding window / summarization / Mem0). 37.3 is now significantly larger and well-developed.
   - **Sim-to-real**: `24.6` (22 KB) "VLA Limitations" with the Sim-to-Real Gap subsection and `24.13` (32 KB) "Sim-to-Real Gap" full section. Both in the same chapter; nearly verbatim overlap on the gap framing.
   - **GraphRAG**: `35.2` (70 KB, 66 hits on GraphRAG/knowledge graph) and `35.3` (67 KB, 65 hits). 35.2 now explicitly cross-references 35.3 as "the GraphRAG community-summarization technique itself lives in Section 35.3" (cycle-2 acknowledged overlap), which softens the redundancy but does not eliminate it: 35.2 still teaches KG-as-retrieval-substrate end-to-end and 35.3 reteaches the same primitives for GraphRAG.
   - **Code-gen agents**: `29.1` (41 KB, 13 hits Claude Code/Cursor/Devin) and `29.4` (75 KB, 37 hits). 29.4 grew the bigger of the two and is the deeper coverage.
   - **Tools Ch 36 vs Ch 41**: Now well-differentiated (Ch 36 = retrieval, Ch 41 = conv-AI). Light remaining overlap: LangChain mentioned 9 times in Ch 36 sec 36.2 (for retrieval chains) and 14 times in Ch 41 sec 41.2 (for conversational memory). The boundary is defensible because LangChain truly has both use cases, but the two sections do not cross-reference each other.
9. **Part 8 has a chapter-numbering gap.** Part 8 is `module-37`, `module-40`, `module-41` (skipping 38 and 39). Whether 38 and 39 were merged into 37/40 elsewhere or simply dropped is unclear; the gap is visible to anyone scrolling the part directory. Part-index renders only Chs 37 / 40 / 41 cleanly so most readers will not notice, but a future tool-of-record audit on the book structure should reconcile.
10. **256 H2 headings in Chs 20, 21, 22 (first half), 24 use bare `1, 2, 3, ...` numbering style instead of the book-wide `N.M.K` style.** Ch 23 and Ch 25 use proper `23.1.1` / `25.1.1` headings. This is a style inconsistency that survived all of cycle 2 and waves 17. The 32 affected sections span:
   - Ch 20: all 10 section files
   - Ch 21: all 4 section files
   - Ch 22: sections 22.1-22.5 (first 5 only; 22.6-22.9 also use bare numbering per a quick spot-check)
   - Ch 24: all 13 section files
   Programmatic transformation is straightforward (id `1-anatomy-of-the-gap` -> `24-13-1-anatomy-of-the-gap`, visible `1.` -> `24.13.1`).
11. **Inconsistent "Sections" heading on chapter index pages.** 7 chapter index pages use `<h2>Sections in This Chapter</h2>`, 13 use `<h2>Sections</h2>`. Minor but trivially fixable.

## Suggested cycle 4 actions

1. **Bulk script to fix the 15 botched pagefind-meta spans in Part 5.** Replace `</span>P: Audio, Music, and Video Generation" hidden=""></span>` (and the `R:` / `T:` variants) with the proper full `<span class="pagefind-meta-injected" data-pagefind-meta="chapter:Chapter NN: Title" hidden=""></span>` tag. The current Ch 24.13 file has the correct full form; copy that shape.
2. **Bulk script to collapse `<strong><strong>` to `<strong>` and `</strong></strong>` to `</strong>` in figure / table / code-fragment captions across 108 files.** Pure regex pass on `<strong><strong>(Figure|Table|Code Fragment)` and the matching close.
3. **In-section "What's Next" paragraph rewrite.** The chapter-nav rebuild in wave 17g touched the `<nav class="chapter-nav">` block but not the in-section `<div class="whats-next">` blocks. Each section's What's Next paragraph needs a rewrite that matches the actual next chapter in the current numbering. There are roughly 15 of these in the scope. Same for the section What Comes Next in chapter `index.html` files (Ch 25 index "Chapter 46" reference, Ch 37 index "Part VI next" reference).
4. **Standalone "Chapter NN" references in body prose, the remaining ~30 in the suspect list.** A mechanical sed pass mapped against the cycle 2 remap table will fix most of them; the ones that need rewriting (not just renumbering) are the Ch 26 looking-back "Chapters 21 through 24 specializes" sentence and the Ch 29 "Chapters 22 through 24 cover general agent principles" sentence in the meta description and body.
5. **The two code-comment stale section refs** (`# Text-to-SQL pipeline (covered in Section 32.5)` -> 32.3, `# See Section 38.2 for the full protocol walkthrough.` -> 40.2 or removal).
6. **Ch 34 section card descriptions for 34.3 and 34.5.** 34.3 should be a one-line summary of post-extraction / production patterns; 34.5 should be a one-line summary of advanced NER / grounding rather than the truncated "Consider the following passage: 'Dr." fragment.
7. **Consolidation decisions for the 5 content overlaps.** Recommended:
   - **Agentic RAG**: keep 32.2 as the deeper / longer treatment (94 KB vs 27.5's 29 KB), trim 27.5 to an agent-framing-only stub that cross-references 32.2 for technique details.
   - **Memory**: 37.3 is now the deeper section (209 KB); fold 26.6 into 37.3 OR keep 26.6 as the agent-specific framing and slim 37.3's MemGPT coverage to a `see 26.6` callout (the larger section subsuming the smaller is usually simpler).
   - **Sim-to-real**: 24.13 is the canonical section; trim 24.6's sub-bullet on sim-to-real to a one-paragraph forward pointer.
   - **GraphRAG 35.2 vs 35.3**: keep both, but rewrite 35.2 to be motivation-only (why KGs as retrieval substrate exist, when to consider them) and move all primitive-walkthroughs into 35.3. Currently both sections re-teach Cypher / triples / SPARQL.
   - **Code-gen agents 29.1 vs 29.4**: 29.4 is the deeper section; reposition 29.1 as the introductory "category overview + Self-Debugging Loop" piece and let 29.4 own the production-workflow deep dive.
8. **Bare H2 numbering in Chs 20, 21, 22, 24** (256 H2s). Decide whether to (a) renumber to the book-wide `N.M.K` style, or (b) accept the per-section local-numbering as a stylistic variant. If (a), the IDs and visible text both need rewriting; cross-references that already use `#1-anatomy-of-the-gap` style anchors are isolated within their own sections, so refactoring should be safe.
9. **Part 8 chapter-numbering gap (38 / 39 missing).** Document the structure decision in `book_structure.yaml` so future audits do not flag this as a bug. If 38 and 39 were content that got merged into 37 and 40, a note in the part index or in the book_structure file should explain.
10. **Trivial: standardize chapter-index "Sections" heading.** Replace `<h2>Sections in This Chapter</h2>` with `<h2>Sections</h2>` (or vice versa) across all 20 chapter indices for visual consistency.
