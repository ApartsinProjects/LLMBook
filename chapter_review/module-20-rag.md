# Module 20: Retrieval-Augmented Generation (RAG)

**Audit date**: 2026-05-11
**Sections reviewed**: 20.1, 20.2, 20.3, 20.4, 20.5, 20.6, 20.7, 20.8, 20.9
**Total word count**: ~62,600 (includes HTML markup)

## Summary
Comprehensive coverage of the RAG ecosystem with strong code support and modern citations (HyDE, CRAG, Self-RAG, Contextual Retrieval, GraphRAG, ALCE). Two structural problems hurt this chapter most: (1) substantial duplication between 20.3 (which contains a full 20.3.4 "GraphRAG" subsection with the same Microsoft pipeline) and the entire 20.7 ("GraphRAG: Knowledge Graph-Augmented Retrieval") section, and (2) the same multi-figure-collision bug seen in module 19. Code captions in 20.7 are also corrupted (caption labels do not match their numbers).

## Inconsistencies
- **Major content duplication 20.3 vs 20.7**: Section 20.3.4 "GraphRAG" (lines 294 onward) and Section 20.7 cover nearly the same Microsoft GraphRAG pipeline (entity extraction, Leiden community detection, hierarchical summaries, local vs global search). The chapter should either fold 20.3.4 into 20.7 (leaving 20.3 as KG-only fundamentals + graph embeddings) or merge them entirely. Reader currently reads the same pipeline description twice.
- **section-20.1**: Three illustrations + one diagram all labeled "Figure 20.1.3" (lines 37, 45, 99, 107). Following diagrams jump to 20.1.4 and 20.1.5 (lines 277, 491).
- **section-20.2**: Four illustrations all labeled "Figure 20.2.5" (lines 36, 40, 57, 108). Diagrams then go 20.2.5, 20.2.6, 20.2.7.
- **section-20.3**: Three illustrations all labeled "Figure 20.3.4" (lines 36, 40, 65); diagram is also 20.3.4 (line 107).
- **section-20.7 line 129**: Code caption reads `<strong>Code Fragment 20.7.1:</strong> Code Fragment 20.7.2: Microsoft GraphRAG indexing pipeline` - the inline `# Code Fragment 20.7.2` comment from the source got concatenated into the caption text, doubling the label.
- **section-20.7 line 359**: Same bug. `<strong>Code Fragment 20.7.5:</strong> Code Fragment 20.7.6: Hybrid graph + vector + full-text retrieval`.
- **section-20.7 Code Fragments numbering**: The numeric labels skip and collide. Frag labelled 20.7.1 has body comment `Code Fragment 20.7.2`, Frag 20.7.5 wraps body `Code Fragment 20.7.6`, Frag 20.7.6 (Evaluating GraphRAG) duplicates label 20.7.6 used both at line 416 (comment) and line 460 (caption). The original numeric ordering (1,2,3,4,5,6) appears intended but the rendered captions are off-by-N.
- **Chapter index** (`module-20-rag/index.html` line 23): epigraph attributes RAG agent as "Bookishly Wise AI Agent"; section 20.7 attributes the same agent as "Fact-Hoarding AI Agent" (line 35). Other sections may use other variants.
- **Section title mismatch**: index.html section card for 20.6 says "RAG Frameworks & Orchestration" but section text discusses LangChain/LlamaIndex/Haystack/DSPy plus "RAG security, poisoning attacks, and production deployment" per the index (line 154); the safety/security topics also appear in module 26, raising overlap.

## Gaps
- **section-20.7 prereqs** point only to 20.3 and 20.2; should also forward-reference module 22-23 (agentic RAG) since GraphRAG global-search is essentially an agentic pattern.
- The chapter index lists 9 sections but the original part-V index page (already read) shows only 4 section cards in `module-20-rag/index.html` followed by another `<ul class="sections-list">` containing the rest (line 134). This split list is unusual; likely a render-time bug from a renumber/insert.
- **section-20.5 (Text-to-SQL)**: Spider/BIRD benchmark mentions but no actual benchmark numbers or model recommendations as of 2025-2026 (e.g., DAIL-SQL, MAC-SQL).
- **section-20.6**: No mention of newer orchestration frameworks introduced post-DSPy (e.g., agno, CrewAI for RAG-flavored agents, or Pydantic AI). DSPy alone is shown but compound AI systems framing is brief.
- **section-20.4 (Deep Research)**: No mention of OpenAI Deep Research, Perplexity, or Google's Gemini Deep Research products as concrete examples of agentic RAG, despite them being the canonical 2024-2025 examples.

## Errors
- **section-20.7 line 86-129**: Code uses `from graphrag.config import GraphRagConfig` and `from graphrag.index import run_pipeline`. Microsoft's `graphrag` package as of 2024-2025 actually exposes `graphrag.config.create_graphrag_config` and the CLI entrypoint `graphrag.index.run` (or `python -m graphrag.index`). The shown imports likely will not run as-is. Verify against the current package API.
- **section-20.7 line 98**: `"api_key": os.environ["OPENAI_API_KEY"]` is referenced without `import os` - the snippet starts with `import graphrag` then uses `os.environ`. NameError as written.
- **section-20.5**: Without seeing the section file in detail, the index promises "Spider, BIRD benchmarks" - SQL Spider 1 leaderboard largely closed in favor of BIRD; recommend confirming the benchmark coverage is current.
- **section-20.6 (RAG security)**: Per the index card, this section covers "RAG security, poisoning attacks, and production deployment". This subject matter overlaps with Module 26 (Agent Safety & Production). Risk of duplicate or contradictory advice across the two chapters.
- **section-20.1 line 107**: Cites "Source: NVIDIA, 2023" for the RAG diagram; ensure the URL still resolves and that attribution date is correct (the linked NVIDIA blog dates from late 2023).
- **All sections**: Multiple "Figure 20.X.Y" inline references (e.g., "Figure 20.1.3 illustrates the four stages") become ambiguous because three figures share that number per section.

## Improvements
- **Resolve the GraphRAG duplication**: Remove subsection 20.3.4 entirely or compress it to a one-paragraph teaser that explicitly forwards to 20.7. The current setup buries the deep treatment behind a partial preview and confuses readers.
- **Fix the code-caption double-prefix bug** in 20.7: strip the `# Code Fragment X.Y.Z` comment from the visible caption (it should remain in source code as a comment, not appear twice in the rendered caption).
- **Renumber figures sequentially per section** as recommended in module 19 review.
- **Standardize "Big Picture" callout style** between the chapter index and section files - module 20's index has only one Big Picture, while sections each have their own with different framing.
- **Add OpenAI Deep Research / Perplexity examples** to 20.4 to anchor agentic RAG in concrete user-facing products.
- **Cross-reference 20.6's RAG security with module 26** to avoid duplication: pick one location for prompt-injection, poisoning, and deployment hardening.
- **Add a "as of date" footnote** to the comparison tables in 20.6 (LangChain vs LlamaIndex vs Haystack), which change rapidly.
- **In 20.5**, add a one-paragraph note on schema RAG vs vector RAG for tables, and reference DuckDB / Spider 2 benchmarks if current.
- **Standardize agent epigraph descriptors** (Bookishly Wise vs Fact-Hoarding) across all 9 sections.

## One-thing-only fix
Resolve the 20.3 vs 20.7 GraphRAG duplication: collapse 20.3.4 into a single paragraph that forwards to 20.7, leaving 20.3 to focus on KG fundamentals (entities, RDF, property graphs, embeddings). This eliminates the most jarring redundancy in the chapter and tightens the narrative.
