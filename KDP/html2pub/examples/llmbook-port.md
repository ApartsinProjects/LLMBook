# Migrating LLMBook to html2pub

This guide shows how the existing `KDP/build/build_epub.py` + `KDP/metadata/metadata.yaml` configuration maps onto a single `KDP/html2pub.toml`.

## Equivalent config

Place this at `KDP/html2pub.toml`:

```toml
[book]
title = "Building Conversational AI with LLMs and Agents"
subtitle = "From the mathematics of attention to production agent systems"
authors = [
    { name = "Alexander Apartsin", file_as = "Apartsin, Alexander", role = "aut" },
    { name = "Yehudit Aperstein",  file_as = "Aperstein, Yehudit",  role = "aut" },
]
language = "en"
identifier = ""   # leave empty -> auto-uuid
publisher = ""
rights = "Copyright (c) 2026 Alexander Apartsin and Yehudit Aperstein. All rights reserved."
publication_date = "2026-05-10"
keywords = [
    "RAG vector database semantic search",
    "LangChain LangGraph CrewAI tutorial",
    "transformer architecture from scratch attention",
    "prompt engineering ChatGPT Claude Gemini",
    "LLM fine tuning LoRA QLoRA RLHF DPO",
    "AI agent multi-agent system LLM production",
    "MLOps LLM observability evaluation engineering",
]

[content]
# All HTML lives at the repo root; KDP/ is sibling tooling.
source_dir = "../"
# The LLMBook spine is order-sensitive (foreword early for "Look Inside"),
# so use the existing manifest rather than auto-discovery.
spine = "build/spine_manifest.json"
front_matter_dir = "front-matter"
parts_glob = "part-*"
module_glob = "module-*"
section_glob = "section-*.html"
capstone_dir = "capstone"
appendices_dir = "appendices"

[styling]
stylesheets = ["../styles/book.css"]
blitz = true
blitz_path = "build/blitz.css"
epub_overrides = "build/epub_overrides.css"

[fonts]
include = ["build/fonts/*.woff2"]
rewrite_katex_to_woff2_only = true

[math]
render = "katex"
katex_path = "E:/Tools/katex/node_modules"

[images]
max_side = 1280
jpeg_quality = 78
compress_pngs = true

[cover]
path = "cover/cover_kdp.jpg"

[transforms]
# Threshold for the wide-table callout (was 6 in build_epub.py)
wide_table_min_cols = 6
# The chapter-index "Sections" list is redundant with the EPUB nav
slim_index_lists = true
# Site chrome that has no place in an eBook
drop_selectors = [
    ".chapter-nav", ".header-nav", ".toc-toggle",
    ".toc-link", ".book-title-link", ".toc-icon",
    ".author-links",
    ".bg-motes", "#stars-canvas", ".glow-ring",
]

[transforms.avatar_sizes]
"agent-avatar-inline"  = [28, 28]
"agent-avatar-large"   = [80, 80]
"agent-avatar"         = [80, 80]
"agent-card-avatar"    = [52, 52]

# Cross-doc fragment hrefs to wisdom-council that point at slimmed agents.
# Listed explicitly here because the LLMBook slim happens via a custom
# transform in the existing pipeline; in html2pub you would either:
#   (a) keep using a project-specific pre-pass that drops the cards AND
#       declares the dropped ids here, OR
#   (b) drop this entirely and let those fragments resolve to the top of
#       the wisdom-council page (current behavior of older build_epub.py).
[transforms.fragment_drop]
wisdom-council = [
    # populate with all wc-card ids NOT in the keep list
    # ("synth", "scale", ...)
]

[output]
epub = "output/building-conversational-ai-llms-agents.epub"

[optimize]
epub_optimizer = true
epub_optimizer_path = "E:/Tools/epub-optimizer/dist/src/pipeline.js"
repair_entities = true
```

## What's NOT yet in html2pub vs. the LLMBook pipeline

These remain bespoke to the LLMBook pipeline and would need to be ported as separate scripts (or added to a future html2pub version):

- `wisdom-council` slim transform that drops the 34 less-quoted agent cards. Easiest: keep `KDP/build/apply_source_fixes.py` style pre-pass that mutates the source HTML, or add a `[transforms.slim_wisdom_council] keep = [...]` table to html2pub.
- `KDP/build/apply_source_fixes.py` regex source fixes (avatar dimensions, Pygments pre-tokenize, URL braces). Pygments is now built into `content.py`. Most others should be applied to source HTML once and committed.
- `KDP/build/fix_double_escaped_entities.py` (`&amp;X;` -> `&X;`). Move into a build pre-pass.
- `KDP/build/render_epub_samples.py` and `KDP/build/build_sample_pdf.py` (post-EPUB QA workflows). Out of scope for html2pub.
- `KDP/build/publish.py` orchestrator that chains build -> validate -> optimize -> re-validate -> preview. Replace with a small shell script or Makefile that calls `html2pub build .` then runs EPUBCheck and `epub-optimizer`.

## Migration steps

1. Copy the TOML above into `KDP/html2pub.toml`.
2. `cd KDP && pip install -e html2pub`
3. `html2pub build .`
4. Compare the produced EPUB to `KDP/output/building-conversational-ai-llms-agents.epub` (file sizes, chapter counts, spot-check a few chapters in Kindle Previewer).
5. Once parity is confirmed, retire `KDP/build/build_epub.py` and `KDP/build/generate_spine.py`. Keep the source-fix and QA scripts (they remain useful).
