# html2pub

Convert a directory tree of source HTML files into a publishable EPUB 3.

## Quick start

```bash
pip install -e .
cd my-book/
html2pub build .
```

`html2pub` looks for `html2pub.toml` in the project directory and uses it to drive the conversion: source paths, metadata, stylesheets, fonts, math rendering, image policy, and output location.

## Minimal config

```toml
# html2pub.toml
[book]
title = "My Book"
authors = ["Jane Doe"]
language = "en"
identifier = "urn:isbn:978-0-00-000000-0"

[content]
source_dir = "."
spine = "auto"

[styling]
stylesheets = ["styles/book.css"]

[output]
epub = "output/my-book.epub"
```

Run `html2pub build .` and you get `output/my-book.epub`.

## Project layout

`spine = "auto"` (default) discovers HTML in this order:

1. `<front_matter_dir>/index.html` and other `*.html` (default `front-matter/`)
2. Each part matching `<parts_glob>` (default `part-*/`):
   - `<part>/index.html`
   - Each module/chapter matching `<module_glob>` (default `module-*/`):
     - `<module>/index.html`
     - `<module>/<section_glob>` (default `section-*.html`)
3. `<capstone_dir>/*.html` (default `capstone/`)
4. `<appendices_dir>/index.html` and each appendix subdirectory (default `appendices/`)

Override any of these with explicit globs or a JSON spine manifest:

```toml
[content]
spine = ["intro.html", "chapter-*.html", "outro.html"]
# or
spine = "build/spine_manifest.json"
```

## Full config reference

See `tests/fixtures/tiny_book/html2pub.toml` for a working example. Key sections:

- `[book]` — OPF metadata: `title`, `subtitle`, `authors`, `language`, `identifier`, `publisher`, `rights`, `publication_date`, `description`, `keywords`.
- `[content]` — `source_dir`, `spine`, and folder/glob conventions.
- `[styling]` — `stylesheets` (list of CSS files to bundle), `blitz` + `blitz_path` for an optional baseline, `epub_overrides` for project-specific EPUB tweaks. Built-in `default_overrides.css` ships if you don't supply one.
- `[fonts]` — `include = ["path/to/*.woff2"]` for fonts to bundle. Set `rewrite_katex_to_woff2_only = true` (default) to drop ttf/woff entries from KaTeX's CSS.
- `[math]` — `render = "katex"` to pre-render LaTeX math via Node + KaTeX. Requires `katex_path = "/path/to/node_modules"` (root containing `katex/`).
- `[images]` — `max_side` (default 1280), `jpeg_quality` (default 78). Images are deduplicated by content hash and JPEG-encoded when no transparency.
- `[cover]` — `path = "cover.jpg"` relative to project root.
- `[transforms]` — per-project HTML cleanup knobs:
   - `drop_selectors` — list of CSS selectors to remove entirely (site nav, social links, animated backgrounds).
   - `avatar_sizes = { "agent-avatar-inline" = [22, 22] }` — set explicit width/height on `<img>` inside the named class wrapper.
   - `wide_table_min_cols` — wrap tables with this many columns or more in a "complex table" callout (default 6).
   - `slim_index_lists` — remove redundant `<ul class="sections-list">` from chapter index pages.
   - `fragment_drop = { "wisdom-council" = ["agent-x", "rag"] }` — record IDs that will be removed during build; cross-doc hrefs to those fragments are stripped.
- `[output]` — `epub` path.
- `[optimize]` — wrappers for the external `epub-optimizer` Node tool and an entity-repair pass.

## CLI

```
html2pub build [PROJECT_DIR]    # build the EPUB (default: cwd)
html2pub build . --validate-only # validate config + assets, don't build
html2pub validate <epub>         # check an existing EPUB
```

## Troubleshooting (lessons from the LLMBook pipeline)

These are the foot-guns the tool deliberately avoids; if you hit them in custom downstream tooling, here's why:

1. **EPUB renders with browser default fonts / no CSS.** Cause: `ebooklib.epub.EpubHtml.set_content()` strips `<link rel="stylesheet">` tags from the head when wrapping HTML. Fix: register stylesheets via `ch.add_link()`. `html2pub` does this for every chapter; the smoke test in `tests/test_build.py` asserts each chapter ships with a stylesheet link.

2. **Math shows as raw `$$...$$` in EPUB readers.** Cause: EPUB readers strip JavaScript, so client-side KaTeX/MathJax never runs. Fix: pre-render server-side at build time. Set `[math].render = "katex"` and provide `katex_path`.

3. **EPUBCheck reports missing font files (RSC-007).** Cause: `@font-face` `src:` lists reference woff2/woff/ttf but only one is bundled. Fix: either bundle all 3 OR rewrite the CSS to reference only the format you bundle. `[fonts].rewrite_katex_to_woff2_only = true` does the latter for KaTeX.

4. **PDF preview shows raw filename text after every link.** Cause: web stylesheets often have `@media print { a[href]::after { content: attr(href) } }`; real EPUB readers use `screen` media but PDF preview triggers `print`. Fix: `default_overrides.css` blocks `attr(href)` in print media.

5. **Cross-document fragment links 404 after a build-time slim.** Cause: a transform removed an element id but other chapters still link to it. Fix: pre-record dropped IDs in `[transforms.fragment_drop]`; the builder rewrites cross-doc hrefs to drop the fragment so the link still lands at the top of the target page.

6. **Edge `--print-to-pdf` produces a 1-page error.** (Out of scope for html2pub itself, but if you build PDFs from the EPUB chapters): use `--headless=new` (not legacy `--headless`), escape `&` in the `<title>`, and don't `unlink()` the temp HTML in a `finally:` block.

## Architecture

See `DESIGN.md`. In short:

```
config.py    -- TOML parser + validation
spine.py     -- source dir -> ordered spine
content.py   -- per-chapter cleanup / sanitization / Pygments / wide-table wrapping
math_render.py -- Node + KaTeX bridge (extract math, batch-render, replace)
images.py    -- discovery, dedup, downscale, JPEG-encode
fonts.py     -- glob + bundle + KaTeX CSS rewrite
nav.py       -- TOC + EPUB 3 landmarks
builder.py   -- EpubBook assembly with ch.add_link() registered styles
validators.py -- pre/post-build invariants
cli.py       -- argparse entry point
```

## Tests

```bash
python tests/test_build.py
```

Builds the `tiny_book` fixture and asserts:
- output EPUB exists and is non-trivial size
- at least 3 chapters
- every chapter XHTML has a `<link rel="stylesheet">` in head (regression test)
- user stylesheet and default overrides are bundled

## License

MIT.
