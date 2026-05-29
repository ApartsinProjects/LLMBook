# html2epub — Design

`html2epub` is a generalized, reusable Python tool that converts a directory tree of source HTML files into a publishable EPUB 3. It is extracted from the LLMBook KDP build pipeline (`KDP/build/build_epub.py`) and made generic so any HTML book can be converted with a single TOML config and one CLI invocation.

## Architecture overview

The tool is a single Python package with one CLI entry point:

```
html2epub build <project-dir>
```

It reads `html2epub.toml` from the project directory, discovers source HTML files (either via an explicit spine manifest or via configurable glob patterns), processes each chapter, then assembles a valid EPUB 3 using `ebooklib`. The pipeline is deliberately linear so that intermediate failures are diagnosable.

Pipeline phases:

1. **Config** (`config.py`) — load and validate `html2epub.toml`; resolve all paths relative to the project root.
2. **Spine** (`spine.py`) — produce an ordered list of HTML file paths from either an explicit manifest, a list of file globs, or auto-discovery (front-matter / parts / capstone / appendices).
3. **Per-chapter cleanup** (`content.py`) — for each HTML file: strip `<script>`/`<noscript>`, drop oversized inline `<style>` blocks, sanitize illegal URL characters in id attributes and url() refs, dedupe element IDs, drop orphan fragment refs, normalize code-block contents, apply Pygments highlighting, render math.
4. **Math** (`math_render.py`) — extract `$$...$$`, `\(...\)`, `\[...\]`, and `<span class="math">` blocks; batch-render via Node + KaTeX (`render_math.js`); replace originals with rendered HTML+MathML.
5. **Images** (`images.py`) — collect every referenced image, deduplicate by content hash, downscale + JPEG-encode where alpha is absent.
6. **Fonts** (`fonts.py`) — bundle subset woff2 fonts (and optionally woff / ttf for KaTeX `@font-face` lists, since EPUBCheck flags missing format files).
7. **Nav** (`nav.py`) — hierarchical TOC + EPUB 3 landmarks (`cover`, `toc`, `frontmatter`, `bodymatter`, `afterword`, `backmatter`).
8. **Builder** (`builder.py`) — assemble `EpubBook`, register stylesheets via `ch.add_link()` (the critical lesson — see below), bundle CSS/fonts/images, write the EPUB.
9. **Validation** (`validators.py`) — pre-flight checks (config sanity, missing assets) and post-build structural checks (file present, chapters all have stylesheet links, no raw `$$...$$` remaining).

## Config schema (rationale)

The TOML schema is split into intent-grouped sections so config files are readable. Critical sections:

- `[book]` — OPF metadata (title, subtitle, authors with file_as / role, language, identifier, publisher, rights, date).
- `[content]` — `source_dir`, `spine` (auto / manifest path / explicit list), and configurable folder names for `front_matter`, `parts`, `capstone`, `appendices`. **Every LLMBook-specific path is configurable**, not hardcoded.
- `[styling]` — list of project stylesheets to bundle, optional Blitz baseline, optional EPUB overrides path. Tool ships a `default_overrides.css` if user doesn't supply one.
- `[fonts]` — glob list of font files to subset and bundle.
- `[math]` — `render = "katex" | "off"`, `katex_path` for the Node modules root.
- `[images]` — `max_side`, `jpeg_quality`, `compress_pngs`.
- `[cover]` — single image path (auto-creates `cover.xhtml` via ebooklib's `set_cover()`).
- `[transforms]` — **the LLMBook-specific knobs are exposed here**: `wide_table_cols` (default 6), `slim_index_lists = true|false`, `avatar_classes = { "agent-avatar-inline" = [22, 22], ... }`, `drop_classes = ["chapter-nav", "header-nav", ...]`. Defaults match common patterns; users override per project.
- `[output]` — `epub` path.
- `[optimize]` — wrapper around external `epub-optimizer` and an entity-repair pass (the `&apos` regression fix).

## LLMBook-specific things now configurable

The original `build_epub.py` hardcoded:

- `wisdom-council.html` slim and the 8-agent keep list (now generic via `[transforms.fragment_drop]` table that records dropped IDs from any source page and rewrites cross-doc hrefs).
- `agent-avatar-inline` / `agent-avatar-large` / `agent-card-avatar` sizes (now `[transforms.avatar_sizes]` map).
- `chapter-nav` / `bg-motes` / `#stars-canvas` selectors (now `[transforms.drop_selectors]` list, baked into a generated overrides CSS rule).
- `book.css` paths and Blitz absolute paths (now relative to `source_dir`).
- The 6-column wide-table threshold (now `[transforms.wide_table_min_cols]`).

## Migration path

Replacing the LLMBook `KDP/build/*` set with `html2epub` is a one-file change for the user: write `KDP/html2epub.toml` with the LLMBook's existing metadata + content paths + transform knobs, then run `html2epub build KDP/`. The original Python files become reference-only. See `examples/llmbook-port.md` for a worked example.

## Lessons baked into the generic code

1. **`ebooklib.EpubHtml.set_content()` strips `<link>` from head** — `builder.py` registers stylesheets via `ch.add_link()` for every chapter. There is a regression test for this (asserts each chapter XHTML has the link tags after build).
2. **Math must be pre-rendered server-side** — KaTeX bridge runs at build time; if `[math].render = "off"`, the tool warns when raw `$$...$$` is seen.
3. **Font @font-face src lists must include all 3 formats they reference** — `fonts.py` either bundles all 3 (woff2, woff, ttf) OR rewrites the CSS to drop the unbundled ones. Default is "rewrite to woff2-only" because subsetted woff2 is smallest.
4. **EPUB readers honor `screen` media, not `print`** — `default_overrides.css` includes a guard for any `attr(href)` rule under `@media print` so PDF preview doesn't leak filenames.
5. **Cross-doc fragment rewriting** — generic pre-pass scans all spine files for IDs that will be dropped during build, then rewrites cross-doc hrefs to drop those fragments.

## Bug noted in the LLMBook pipeline (not fixed there)

In `KDP/build/build_epub.py` `build_toc()`, the function shadows the outer `parts` (the chapter map) with a local `parts = src_rel.split("/")` inside the elif branches — this could subtly corrupt the TOC for chapters where the path-split disagrees with the by-part bucket. The hierarchical nav.xhtml builder is unaffected because it uses different variable names. `html2epub` uses unique local names throughout.
