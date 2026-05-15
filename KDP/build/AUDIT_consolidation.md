# HTML Consolidation Audit

**Scope**: 396 HTML files under `E:/Projects/BookBlogsHome/LLMBook/`, excluding
`node_modules/`, `.git/`, `KDP/output/`, `KDP/build/`, `KDP/html2pub/`,
`pagefind/`, `temp_epub/`, `*/backup/`, `*/source_fix_backups/`, and
`scripts/_exercise_payloads/`.

**Trigger**: A recent "Thirteenth Edition" -> "Fourteenth Edition" bump
touched 392 files. The canonical value lives in `html2pub.toml` and
`KDP/metadata/metadata.yaml` (`book.edition = "Fourteenth Edition"`,
`book.publication_year = 2026`) but every chapter hardcodes it.

## Headline numbers

| Metric                                     | Value |
| ------------------------------------------ | ----- |
| Files in scope                             | 396   |
| Files with hardcoded edition text          | 392   |
| Total occurrences of "Fourteenth Edition"  | 395   |
| Files with literal footer line             | 387   |
| Files with hardcoded book title            | 392   |
| Total occurrences of book title            | 639   |
| Files with inline `<script>` block         | 387   |
| Files with Pagefind init script            | 384   |
| Inline `<script>` bytes (total)            | 392,752 |
| Inline Pagefind script bytes (total)       | 389,694 |
| Avg Pagefind script bytes per file         | 1,014 |
| Files with inline `<style>` block          | 3     |
| Inline `<style>` bytes (total)             | 27,092 |

Inline `<style>` is a small footprint compared to the inline `<script>` and
header chrome problem.

## Top 10 most-duplicated patterns (file count)

| Rank | Pattern (verbatim snippet)                            | Files | Total occurrences |
| ---- | ----------------------------------------------------- | ----- | ----------------- |
| 1    | `<!DOCTYPE html>`                                     | 395   | 395               |
| 2    | `<html lang="en">`                                    | 395   | 395               |
| 3    | `<header class="chapter-header">`                     | 394   | 394               |
| 4    | `<nav class="header-nav">` ... `class="toc-link"`     | 394   | 394               |
| 5    | `<link rel="stylesheet" href=".../styles/book.css">`  | 394   | 394               |
| 6    | `Fourteenth Edition`                                  | 392   | 395               |
| 7    | `Building Conversational AI with LLMs and Agents`     | 392   | 639               |
| 8    | `pagefind/pagefind-ui.css` + `pagefind-ui.js`         | 389   | 389               |
| 9    | `<div id="search"></div>` + `<div class="header-search">` | 388 | 388            |
| 10   | `<footer><p>Fourteenth Edition, 2026 ...`             | 387   | 387               |

Honorable mentions: meta description short ("A comprehensive chapter from
the Building Conversational AI textbook.", 331 files), Prism CSS+JS (273
files), KaTeX CSS+JS (78 files), TOC icon "Contents" link label (129 files).

## Inline `<style>` blocks (3 files, 27,092 bytes)

| File                                                     | Bytes  | Contents                                                                                            |
| -------------------------------------------------------- | ------ | --------------------------------------------------------------------------------------------------- |
| `index.html`                                             | 23,028 | Landing-page chrome (Cinzel font import, hero animations). Not duplicated; bespoke to landing.      |
| `appendices/appendix-ag-problem-solution-key/index.html` | 1,720  | `.psk-table` rules. **Not in book.css** -> should move there.                                      |
| `front-matter/about-authors.html`                        | 2,344  | `.author-card`, `.author-photo`, layout for the bio cards. **Not in book.css** -> should move there. |

All three should be lifted into `styles/book.css` (or
`KDP/build/epub_overrides.css` if EPUB-only). Risk is low because each
pattern appears in exactly one source file.

## Inline `<script>` blocks (387 files, 392,752 bytes)

* 384 of 387 are the Pagefind UI initializer, copy-pasted by
  `KDP/build/_v610_pagefind_inject.py`. Each is ~1,014 bytes.
* Total duplicated payload: 389,694 bytes (~380 KB) repeating the same
  `new PagefindUI({...})` call.
* html2pub already strips `<script>`/`<noscript>` (UNWANTED_TAGS in
  `KDP/html2pub/src/html2pub/content.py`), so the script is only useful
  in the browse view. The fix is to extract a single
  `scripts/pagefind-init.js`, then write a single
  `<script defer src="../../scripts/pagefind-init.js"></script>` line.

## Recommended canonical home for each value

| Pattern                                              | Canonical source                                | Suggested template variable     | Replicas to update |
| ---------------------------------------------------- | ----------------------------------------------- | -------------------------------- | ------------------ |
| Edition string (`"Fourteenth Edition"`)              | `html2pub.toml` `[book] edition`                | `{{book.edition}}`               | 392                |
| Publication year (`2026`)                            | `metadata.yaml` `book.publication_year`         | `{{book.publication_year}}`      | 387                |
| Combined footer (`Fourteenth Edition, 2026`)         | derived: `{{book.edition}}, {{book.publication_year}}` | `{{footer.edition_line}}`  | 387                |
| Book title                                           | `html2pub.toml` `[book] title`                  | `{{book.title}}`                 | 392 (639 occurrences) |
| Subtitle                                             | `html2pub.toml` `[book] subtitle`               | `{{book.subtitle}}`              | 1 (room to grow)   |
| Author names                                         | `[[book.authors]]` blocks                       | `{{book.authors[*].name}}`       | 10                 |
| Copyright line                                       | `metadata.yaml` `book.rights`                   | `{{book.rights}}`                | 6                  |
| Per-chapter `<meta name="description">`              | per-file front-matter (kept inline)             | n/a                              | 331                |
| `<nav class="header-nav">...</nav>` chrome           | `templates/_header.html` partial                | `{% include "_header.html" %}`   | 394                |
| `<footer>...</footer>` chrome                        | `templates/_footer.html` partial                | `{% include "_footer.html" %}`   | 387                |
| Pagefind init script                                 | `scripts/pagefind-init.js`                      | `<script src=".../scripts/pagefind-init.js">` | 384       |
| Asset link block (book.css, prism, katex, pagefind)  | `templates/_assets.html` partial                | `{% include "_assets.html" %}`   | 394                |
| `.psk-table`, `.author-card` rules                   | `styles/book.css`                               | n/a (CSS class)                  | 3                  |

## Inline `<style>` count and bytes that could move to book.css

- **Count**: 3 blocks across 3 files
- **Bytes**: 27,092 total
  - `index.html`: 23,028 (bespoke landing-page chrome; recommend keep or move to `styles/landing.css`)
  - `appendices/appendix-ag-problem-solution-key/index.html`: 1,720 (move to `styles/book.css`)
  - `front-matter/about-authors.html`: 2,344 (move to `styles/book.css`)

Net consolidation gain: ~4 KB into `book.css`, ~23 KB into a new
`styles/landing.css` (or kept inline since it's a single file).

## Inline `<script>` blocks count

- **Total inline scripts**: 390 blocks across 387 files (392,752 bytes)
- **Pagefind init copies**: 384 (389,694 bytes / ~380 KB)
- **Non-Pagefind**: 6 (KaTeX renderer `onload` snippet on 78 files is an attribute, not a script block; the small inline scripts are mostly the landing page and 1-2 chapter idiosyncrasies)

## Recommended consolidation actions (priority order)

1. **(P0) Stop hardcoding edition + year in 392 files.** Add build-time
   templating to html2pub. Replace the footer literal with
   `<footer><p>{{book.edition}}, {{book.publication_year}} &middot; ...`.
   `html2pub.toml` and `metadata.yaml` already carry both fields; the
   build pre-flight already cross-checks them.
2. **(P0) Detect and fail loudly when source HTML hardcodes a stale
   edition.** A linter in `publish.py` that greps the source tree for
   "Edition" tokens and compares to `book.edition` would have caught the
   recent 392-file flag-day.
3. **(P1) Move the Pagefind init block into `scripts/pagefind-init.js`** and
   ship a one-liner `<script src>` from each chapter. ~380 KB delta in the
   browse tree; zero effect on EPUB since html2pub strips scripts.
4. **(P1) Lift inline `<style>` rules from `about-authors.html` and
   `appendix-ag-problem-solution-key/index.html` into `styles/book.css`.**
   Single source of truth and consistent visual treatment.
5. **(P2) Header/footer partials.** A `templates/_header.html` and
   `templates/_footer.html` plus a Jinja-style include pass in
   `html2pub` collapses 394 hand-replicated header blocks and 387
   footers into one each. Required for any future structural change
   (e.g., adding a "buy on Amazon" CTA, swapping the search icon).
6. **(P2) Asset link partial.** `<link rel="stylesheet">`,
   `<script defer src="...prism...">`, and KaTeX boilerplate go into
   `templates/_assets.html`. Path-prefix template variable (`{{rel}}`)
   solves the `../` vs `../../` depth problem.
7. **(P3) Update stale docs.** `templates/README.md` line 30 still says
   "Fifth Edition, 2026". Mark templates/* as build-time-only or move
   them to `KDP/build/templates/`. The stale string in the README is
   the canary that proves this audit is needed.

## Suggested architecture

```
KDP/metadata/metadata.yaml          # Single source of truth (already exists)
html2pub.toml                       # Build config (already mirrors metadata)
KDP/build/templates/
    _header.html                    # NEW: chapter-header chrome partial
    _footer.html                    # NEW: footer chrome partial
    _assets.html                    # NEW: <link>/<script> chrome partial
    _pagefind_init.html             # NEW: <script src=...> stub
scripts/pagefind-init.js            # NEW: extracted init block
styles/book.css                     # ABSORB: .psk-table, .author-card
styles/landing.css                  # NEW (optional): index.html chrome
```

Build flow (build-time substitution):
1. html2pub reads `metadata.yaml` -> `{book: {edition, publication_year, ...}}`.
2. A new pre-pass in `KDP/build/_html2pub_hooks.py.post_process` walks the
   soup and substitutes `{{book.edition}}` / `{{book.publication_year}}` /
   `{{book.title}}` tokens.
3. The same hook can `include` header/footer/asset partials, reading them
   from `KDP/build/templates/` and inserting the rendered HTML.

For the browse-only view (the source tree readers see on the web), a
nightly script (`scripts/rebuild_chrome.py`) regenerates header/footer
chrome from the partials whenever `metadata.yaml` or any partial
changes. This eliminates the "392 files to bump" problem.

## What html2pub can already template at build time

Right now html2pub **does not** template HTML content; it only reads
config-level metadata (edition, title, rights, dates) and applies them to
the OPF/NCX/nav.xhtml output. Source HTML body content is passed through
verbatim except for the transforms in `content.py` (script stripping,
fragment-id sanitization, syntax highlighting, KaTeX render, image
rewrite). Adding a template substitution pass to `content.py` is the
smallest viable change:

| Already templated in html2pub | NOT templated (currently hardcoded in HTML body) |
| ----------------------------- | ------------------------------------------------ |
| `<dc:title>`, `<dc:creator>`, `<dc:rights>`, `<dc:date>`, `<dc:identifier>`, `<dc:subject>` (OPF metadata) | Edition text in `<footer>` (392 files) |
| `<title>` (per-chapter)       | Book title in `<title>` and `<a class="book-title-link">` |
| Cover image                   | Author names in `<p class="author">` blocks       |
| KaTeX CSS bundling            | Year, copyright line                              |
| Stylesheet list (from toml)   | Header/footer chrome (394/387 files)              |
| Spine ordering                | Pagefind script blocks                            |

## Recommended split: template at build time vs. stay as-is

**Template at build time** (build-pass substitutes from `metadata.yaml`):
- `{{book.edition}}` -> footer + any landing-page mentions
- `{{book.publication_year}}` -> footer, copyright, any "Updated for 2026" text
- `{{book.title}}` -> `<title>`, `<a class="book-title-link">`, `<div class="part-label">`, `<meta property="og:title">`
- `{{book.subtitle}}` -> subtitle wherever the full title appears
- `{{book.rights}}` -> copyright pages, landing footer
- `{{book.authors}}` -> author bylines (about-authors.html, copyright.html, index.html)
- `{{rel}}` -> path prefix for asset includes (replaces `../`/`../../` hand-counting)

**Stay as-is** (per-file content):
- Chapter / appendix / section headings (these are content, not metadata)
- Per-chapter `<meta name="description">` strings (each describes its own chapter)
- Big-picture callouts, prose, callouts, code samples, exercises, figures
- KaTeX delimiters and math source
- `<a class="prev">` / `<a class="next">` chapter-nav links (already file-specific)

**Move to a CSS partial or external asset** (not templated, just deduplicated):
- Pagefind init `<script>` -> `scripts/pagefind-init.js`
- `.psk-table`, `.author-card`, `.author-photo` rules -> `styles/book.css`
- Header / footer / assets chrome -> `templates/_*.html` partials
- Inline KaTeX `onload` attribute (78 files) -> `scripts/katex-init.js`

## File pointers (absolute paths)

- Single source of truth (already exists): `E:/Projects/BookBlogsHome/LLMBook/KDP/metadata/metadata.yaml`
- Build config (mirrors metadata): `E:/Projects/BookBlogsHome/LLMBook/html2pub.toml`
- Build script (where templating pass should land): `E:/Projects/BookBlogsHome/LLMBook/KDP/build/_html2pub_hooks.py`
- html2pub content transforms (where token substitution should hook in): `E:/Projects/BookBlogsHome/LLMBook/KDP/html2pub/src/html2pub/content.py`
- Legacy edition-bump script (proves the pain): `E:/Projects/BookBlogsHome/LLMBook/KDP/build/_v702_bump_footer_edition.py`
- Pagefind injection script (proves we already template chrome programmatically): `E:/Projects/BookBlogsHome/LLMBook/KDP/build/_v610_pagefind_inject.py`
- Source HTML templates (stale, says "Fifth Edition, 2026"): `E:/Projects/BookBlogsHome/LLMBook/templates/`
