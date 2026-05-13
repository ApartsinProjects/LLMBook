# Session Backlog — Persistent Record

**Purpose**: durable record of every ask in this session and its status, so nothing is lost if the conversation context is compacted or summarized. This file is updated as items move between pending and done.

Last updated: **2026-05-10**

---

## Done (in this session)

### Foundational publishing package

- [x] Generate complete KDP publishing package in `KDP/` subfolder (EPUB + metadata + cover + validation + docs)
- [x] Build EPUB from 470 source HTML files (441 chapters, fonts, images, callouts)
- [x] Validate EPUB with both Python structural checker and IDPF epubcheck (0 errors / 0 warnings)
- [x] Cover image: process 896×1200 source to 1600×2560 sRGB JPEG
- [x] Generate cover variants via Gemini: artwork-only, with-text, image-to-image, thumbnail-optimized, minimalist
- [x] Install Java 17 + epubcheck 5.1 to `E:/Tools/epubcheck/`
- [x] Install Node.js 24 + epub-optimizer 2.1.1 to `E:/Tools/epub-optimizer/`
- [x] Wire epub-optimizer into pipeline as final step (with entity-repair pass for `&apos`)
- [x] Install fonts (Source Serif 4 + Source Code Pro), subset via FontTools, embed in EPUB
- [x] Integrate Blitz CSS framework
- [x] Strict source-fix policy: regex-based, BS-mangling-safe (with un-mangler tool)
- [x] Apply source fixes: avatar dimensions (323 imgs), Pygments pre-tokenize (1696 blocks), URL braces fix, duplicate SVG IDs dedup
- [x] Add EPUB 3 landmarks nav (cover, toc, foreword, bodymatter, capstone, backmatter)
- [x] Slim chapter-index pages (drop redundant Sections list, ~150 KB savings)
- [x] Drop fm-1 redirect orphan from spine
- [x] Add Pygments syntax highlighting in build script
- [x] Set explicit width/height on agent-avatar `<img>` tags

### Pipeline orchestration

- [x] `KDP/build/publish.py` orchestrator: clean / build / validate / optimize / re-validate / preview
- [x] `KDP/build/Makefile` and `publish.ps1` wrappers
- [x] `KDP/PIPELINE.md` documentation with decision matrix
- [x] Conservative image reduction defaults (1280px / Q78)
- [x] `--preview` flag launches Kindle Previewer 3 GUI

### Adoption / metadata

- [x] Foreword (`front-matter/foreword.html`) drafted
- [x] Foreword updated to use llmbook.apartsin.com, drop GitHub + newsletter
- [x] Description rewritten (leads with "Build Production AI Agents from First Principles")
- [x] Keywords refreshed (framework + model names instead of title restatements)
- [x] Categories refreshed (Programming Languages/Python instead of Programming/General)
- [x] Look Inside spine reorder (`look-inside-preview.html` + foreword early in spine)
- [x] Companion landing page (`KDP/landing-page/index.html` + README for deployment)
- [x] Adoption playbook (`KDP/ADOPTION_PLAYBOOK.md`) — Author Central setup, endorsement outreach, ARC strategy, multi-distribution

### Audits & reports (no source modified)

- [x] Quality audit: 4209 issues identified, 563 broken cross-refs auto-fixed, P0 dropped 605 → 43
- [x] Diagram audit: 1576 diagram-related issues categorized
- [x] Tables audit: 393 tables, 26 HIGH-severity, simplification patterns documented
- [x] Figure audit: Figure 4.2.2 root cause + 50+ similar problematic figures + Gemini regen prompt template
- [x] EPUB tools comparison (10 tools across 4 tiers)
- [x] Quality tools doc (epub-optimizer, Squoosh, Blitz, FontTools, etc.)
- [x] Review and opportunities (adoption levers + size reduction)

### Visual fixes

- [x] Wisdom-council slim (42 → 8 most-quoted agents) with cross-document fragment rewriter
- [x] Callout system improved with defense-in-depth (5 independent visual markers)
- [x] Image embedding preserved in cards (flex layout for author-card, agent-card)
- [x] Inline avatar sizing forced to 28px (immune to display:inline-flex stripping)

### Infrastructure

- [x] winget restored (Microsoft.DesktopAppInstaller re-registered, WindowsApps added to user PATH)
- [x] Disk space workarounds (TEMP redirected to E: for Java/subprocess output)
- [x] Backups for source modifications (`KDP/build/source_fix_backups/<TS>/`)

---

## In progress / pending

### Current session asks (this turn)

- [x] Backup session backlog to durable file (this file)
- [x] Drop instructor copy / course adoption section from foreword.html
- [x] Drop instructor copy / course adoption section from landing-page/index.html (CSS + footer link too)
- [x] Copy cover image into landing-page/cover.jpg
- [x] Make foreword visible in HTML edition (added to front-matter/index.html as FM.0c card, linked in toc.html short and detailed views)
- [x] PDF generation: sample chapter built via `KDP/build/build_sample_pdf.py` using Edge headless; output at `downloads/sample-chapter-prompt-engineering.pdf` (16.4 MB, 64 pages, chapter 11 index + sections 11.1 and 11.2); wired into `publish.py` (use `--no-sample-pdf` to skip)
  - **Bug fixed 2026-05-10**: Edge silently emitted a 60 KB "ERR_FILE_NOT_FOUND" 1-page PDF for ~30 minutes of debugging. Three issues compounded:
    1. Legacy `--headless` flag silently fails on `file://` URLs - must use `--headless=new`
    2. Unescaped `&` in `<title>Chapter 12: Prompt Engineering & Advanced Techniques</title>` triggers Edge's strict entity parser and aborts page load — escape with `html.escape()` before insertion
    3. Inlining 742 KB of book.css produces a 511 KB temp HTML that Edge struggles with — replaced with `<link rel="stylesheet" href="../../styles/book.css">` (relative resolves correctly since temp file is inside chapter dir)
  - Also: don't `unlink()` the temp file in `finally:` — Edge's helper processes may still be reading it. Added to `.gitignore` instead.
- [x] PDF generation decision: see "Full-book PDF decision" below
- [x] Act on 26 HIGH-severity tables: build-script wraps any table with 6+ columns in a "Wide Table" callout note + applies `complex-table` class with reduced font/padding; source HTML untouched (preserves desktop website experience)
- [x] Final rebuild + validate: 40.15 MB EPUB, 0 epubcheck errors, 0 warnings

---

## Full-book PDF decision (KDP paperback path)

**Recommendation: defer until KDP eBook submission lands successfully**, then revisit if you want a paperback edition. Reasons:

1. **Kindle eBook is the priority** — current EPUB is ready for KDP upload today.
2. **Print PDF is much higher complexity than EPUB**:
   - KDP paperback requires a print-trim-size PDF (e.g., 6×9", 7×10", 8.5×11") with proper bleed (0.125" if illustrations extend to edge)
   - Page numbering, running headers/footers, ToC with real page numbers (not anchor links)
   - Embedded fonts in PDF/A or PDF/X-1a format (not just file references)
   - Image DPI ≥ 300 for the trim size (current 1280-px-max images may be too low for 8.5×11" pages)
   - Cover for print is a separate file: spine + back + barcode area, requires KDP's cover calculator
3. **Tools needed for full-book PDF generation** (in order of complexity):
   - **Pandoc + LaTeX** — most flexible, requires LaTeX install (~3 GB), best output. Existing pandoc on PATH.
   - **WeasyPrint** — Python, simpler install, less polished math/code rendering
   - **Edge headless `--print-to-pdf`** — quick (already proven for sample chapter), but no built-in pagination/headers, would need significant CSS work
   - **Calibre `ebook-convert epub pdf`** — quickest (just EPUB→PDF), result is "good enough" for proof-reading, not print-ready
4. **Realistic effort to ship a print-ready PDF**: 8-16 hours of CSS + manual proofreading. Worth doing as a v2 effort once Kindle reviews start landing.

**Quick-and-dirty approach** if you want a downloadable PDF on the landing page right now:
```bash
# Calibre ebook-convert (~30 sec, looks "fine" not "print-perfect")
ebook-convert KDP/output/building-conversational-ai-llms-agents.epub \
    KDP/landing-page/downloads/full-book-preview.pdf \
    --pdf-page-numbers --pdf-default-font-size 12
```
This produces a non-print-ready PDF good enough for cross-platform reading but NOT suitable for KDP paperback submission.

---

## Math, callouts, avatars, image-caption fixes (2026-05-10 turn)

### Math rendering
- KaTeX 0.16 installed at `E:/Tools/katex/`
- `KDP/build/render_math.js` — Node script that batch-renders LaTeX expressions to HTML+MathML via katex.renderToString
- `build_epub.py` `render_math_in_soup()` — extracts $$...$$, \\(...\\), and `<span class="math">$...$</span>` blocks per chapter, calls Node katex, replaces with rendered spans
- katex.min.css + 14 woff2 fonts bundled into EPUB; CSS strip-rewritten to remove woff/ttf src() entries (woff2 only)
- `epub_overrides.css` adds `.katex-rendered` styling for Kindle e-ink + reflowable readers
- 175 source HTML files contain math; all $$, \\(, and class="math" blocks now typeset in EPUB

### Wisdom avatars
- `epub_overrides.css` defense-in-depth: `width:22px !important; max-width:22px !important;` on the IMG itself (not just the wrapper) for `.agent-avatar-inline`; 56px for `.agent-avatar-large` and `.agent-avatar`. Even readers that ignore CSS class rules will honor px+max-width on the img tag.

### Image-caption alignment
- Background agent audit: `KDP/validation/image_caption_audit.md` — 26 misalignments across 14 files, root cause is "AI-illustration insertion pass added captions without producing matching image files; downstream IMG blocks shifted up one slot relative to their intended captions"
- `KDP/build/fix_diagram_image_pairs.py` — automated fixer: for each `<div class="diagram-container">` extracts the caption's "Figure N.M.K" number, looks for `images/fig-N.M.K-*` file, swaps src if mismatched
- 10 mechanical fixes applied (swapping IMG src to match caption number) including 2 in user-flagged section-4.1: Figure 4.1.4 (now correctly shows pos-encoding), Figure 4.1.7 (now correctly shows pre-post-ln)
- 16 diagrams have NO matching image file (caption text exists but image was never generated) - need manual generation:
  - section-4.1.html: Figures 4.1.3 (encoder-decoder Transformer) and 4.1.5 (Pre-LN vs Post-LN comparison) — the user-flagged ones
  - section-1.1.html: 2 missing
  - section-1.3.html, 1.4.html, 2.2.html, 3.1.html, 3.2.html, 5.2.html, 15.1.html, 15.4.html, 20.1.html, 20.3.html, 27.1.html, 34.10.html: each has 1 missing
- Source HTML modifications backed up to `KDP/build/source_fix_backups/diag_image_pair_<timestamp>/`

### Sample PDF redesign
- 6x9 inch trim size (real trade paperback dimensions; was A4 letterhead)
- Page numbers in footer, suppressed on cover page
- Source Serif 4 body font (matches the EPUB's embedded font)
- Page-break rules: `page-break-inside: avoid` on callouts, code, figures, tables; `orphans: 2; widows: 2`
- Callout backgrounds + colored left borders preserved in PDF
- KaTeX math via `<link rel="stylesheet" href="../../vendor/katex/katex.min.css">`
- Image cap at 75% column width (was full-bleed)
- Typography: 10.5pt body, 22/16/13/11pt h1-h4 with `border-bottom` separator on h2
- Result: 16.5 MB, 85 pages (up from 64 due to smaller trim, but more book-like)

### Tools recommendation docs
- `KDP/PDF_TOOLS.md` — three-tier comparison (WeasyPrint / Pandoc+LaTeX / PrinceXML), recommendation path for current Edge-based pipeline → WeasyPrint → Pandoc+LaTeX
- `KDP/DIAGRAM_WORKFLOW.md` — design + test process for high-quality Gemini-generated technical diagrams (avoid boxes-and-arrows, use visual metaphors of actual mechanism); 5-phase workflow (concept, prompt, generate, audit, iterate)

---

## Architecture decision: site landing page (Path A)

**Decision (2026-05-10)**: the existing `index.html` IS the book's landing page; the separate `KDP/landing-page/` was a duplicate that nobody would visit. **Path A** chosen:
- Marketing copy + structural elements (What You'll Learn grid, sample CTA, author bios, resources footer) merged INTO existing `index.html` as scrollable sections below the existing animated cover hero
- Single CTA "Enter the Journey →" replaced with three CTAs: "Read free →" (toc), "Buy on Amazon" (placeholder ASIN), "Free Chapter (PDF)" (downloads/sample-chapter-prompt-engineering.pdf)
- Sample chapter PDF moved from `KDP/landing-page/downloads/` to `/downloads/` at repo root (served by GitHub Pages at `llmbook.apartsin.com/downloads/...`)
- `.nojekyll` added at repo root (GitHub Pages serves all files as-is, KDP/ stays in repo as build artifacts but isn't user-facing site content)
- `KDP/landing-page/` directory **deleted** (superseded; copy/CSS migrated into index.html)
- `KDP/build/build_sample_pdf.py` updated to write directly to `/downloads/`

Visual design: marketing sections use the same dark navy + gold theme as the cover hero, with semi-transparent backgrounds so the animated stars are subtly visible scrolling past. New sections gracefully degrade to print stylesheet (white background + dark text).

---

## CRITICAL fix: ebooklib CSS link stripping (2026-05-10)

**Symptom**: visual quality of EPUB looked AWFUL — plain Times New Roman, no
callout boxes, no styled headings, all browser-default rendering. User reported
"all the original HTML beauty is preserved" - because it WASN'T.

**Root cause**: `ebooklib.epub.EpubHtml.set_content()` uses its own internal
template that **ignores `<link>` tags** in the HTML's `<head>`. Even though
build_epub.py was generating chapter XHTML with all 4 `<link rel="stylesheet">`
tags, ebooklib stripped them when wrapping into the EPUB. Chapters ended up
with just `<head><title>...</title></head>` — no styles, no fonts, no Pygments.

**Fix**: register stylesheets via the ebooklib API instead:
```python
ch = epub.EpubHtml(uid=info["id"], file_name=info["file"], ...)
ch.add_link(href="../styles/blitz.css", rel="stylesheet", type="text/css")
ch.add_link(href="../styles/katex.min.css", rel="stylesheet", type="text/css")
ch.add_link(href="../styles/book.css", rel="stylesheet", type="text/css")
ch.add_link(href="../styles/epub_overrides.css", rel="stylesheet", type="text/css")
```

**Impact**: rendered chapter PDF size went from 281 KB → 1661 KB (CSS, fonts,
backgrounds, borders all now applied). Visual recheck confirms callouts have
boxes + icons, epigraph is styled, headings have proper typography hierarchy.

This was the root cause of essentially ALL "EPUB looks bad" reports.

---

## Other fixes landed (2026-05-10)

### KaTeX server-side math rendering
- Installed `katex@0.16.45` to `E:/Tools/katex/`
- Added `KDP/build/render_math.js` (Node CLI batch renderer)
- Added `render_math_in_soup()` in build_epub.py — extracts math from
  `<span class="math">$...$</span>`, `$$...$$`, `\(...\)` and replaces with
  pre-rendered HTML+MathML
- Bundled `katex.min.css` + 60 KaTeX font files (woff2/woff/ttf) into EPUB
- Added overrides in epub_overrides.css for `.katex-rendered` / `.math-block`
  responsive sizing on narrow Kindle viewport

### Wisdom avatar sizing (defense in depth)
- Per-img px+max-width caps so unreliable EPUB readers can't show oversized images
- Inline epigraph avatars: 22px hard cap
- Wisdom-council card avatars: 56px hard cap

### Double-escaped HTML entities
- 7 instances across 5 files (`&amp;odot;`, `&amp;approx;`)
- Fixed via `KDP/build/fix_double_escaped_entities.py` (whitelist of known entities)
- Idempotent + creates backup at `KDP/build/source_fix_backups/entities_*`

### Print-stylesheet URL leak (fixed in epub_overrides.css)
- book.css `@media print { a[href]::after { content: attr(href) } }` was leaking
  raw filenames into rendered PDFs (chapter-header showed
  `(ch_0014_part-1-foundations-index.xhtml)`)
- Real EPUB readers use `screen` media so this never affected actual reading
- Override added for clean PDF preview output

### Image-caption misalignment - root cause documented
- Figure 4.1.3 caption "encoder-decoder Transformer" attached to img `fig-4.1.4-pos-encoding.png`
- Background agent running for full-book audit + mechanical fixes

### Tools added to E:/Tools
- `katex@0.16.45` for server-side math
- (existing) Temurin OpenJDK 17, EPUBCheck 5.1, epub-optimizer 2.1.1, fonts

---

## Visual quality verification

After CSS link fix + entity fix + KaTeX integration, sample chapter pages
rendered via `KDP/build/render_epub_samples.py` show:
- ✅ Proper typography (Cormorant Garamond headings, Source Serif body)
- ✅ Callouts with colored boxes + icons + titles
- ✅ Epigraph with red-bordered italic quote + small avatar
- ✅ Cross-references in dark red with proper underlines
- ✅ Page header breadcrumbs (chapter → part → book)

`KDP/build/render_epub_samples.py` is now part of the QA workflow:
```bash
python KDP/build/render_epub_samples.py --max-pages 2
# images at E:/temp/epub_samples/{chapter}_p{N}.png
```

---

## Wave: items 1-12 from pending tasks (2026-05-10 batch)

User asked: "do 1-7 / do 8 and 9 / background: do 10 / in the background: do 11 and 12"

### Foreground (DONE)

- **#1 Section numbering** `0.1.1` hierarchical: `KDP/build/fix_section_numbering.py` renumbered **1411 H2s in 236 section files**. Backups at `source_fix_backups/section_numbering_*`. Idempotent.
- **#2 PDF code highlighting** + **#3 inline math in PDF**: re-engineered `KDP/build/build_sample_pdf.py` to render FROM the EPUB chapter XHTML (which has Pygments tokens + KaTeX-rendered math baked in by `build_epub.py`). Result: sample PDF dropped from **16.4 MB → 3.15 MB** AND now has working code colors + rendered math.
- **#4 Random-sample 20-page audit**: extended `KDP/build/render_epub_samples.py` with `--random N --seed S` flags. 20 random chapters rendered for inspection. Now usable as: `python KDP/build/render_epub_samples.py --random 20 --seed 42`.
- **#5 Verify Kindle Previewer**: `find_kindle_previewer()` confirmed at `~/AppData/Local/Amazon/Kindle Previewer 3/Kindle Previewer 3.exe`. `--preview` flag launches GUI.
- **#6 Bibliography gaps**: 115 section files lack a bibliography. Decision: **NOT auto-fixed** — bibliography is content-authoring work, placeholder text adds no value to readers. Documented as deferred manual task. Authors can use the per-chapter unique-arxiv-IDs grep from copyright audit (649 IDs across the book) as starting input.
- **#7 Duplicate Code Fragment numbers**: `KDP/build/fix_code_fragment_numbering.py` (renumbered 63 to hierarchical) + `KDP/build/dedup_code_fragments.py` (suffixed 20 in-file dups with a/b/c). Cleaned tmppdf.html artifacts. Result: **0 duplicates** book-wide (down from 41).
- **#8 PDF tool comparison**: `KDP/PDF_TOOLS.md` written — full 4-tier comparison (Edge/Chrome, WeasyPrint/Vivliostyle/Pandoc+LaTeX, PrinceXML/Antenna House/PDFreactor, DocRaptor cloud). **Recommendation: keep Edge for sample, install WeasyPrint when committing to print PDF.** Did NOT install WeasyPrint (Windows GTK runtime is a 30-min install, not justified yet).
- **#9 Image compression** via `KDP/build/compress_images.py` (Pillow-based, no external tool deps): 1191 images → 9.32 MB saved (1.5%). **Marginal** — most images already optimized by `build_epub.py`'s default 1280px/Q78 setting. Compressed images at `KDP/build/compressed_images/` for swap-in if desired.

### Background (DONE)

- **#10 Copyright/legal validation**: `KDP/validation/copyright_audit.md` (~270 lines). All fonts SIL OFL 1.1. Code samples original. 0 quotes >50 words. Trademarks used nominatively. **3 RED FLAGS**:
  1. **No dedicated copyright/legal page** in front-matter (only `© 2026` footer line). Template provided in audit Section 6.
  2. **6 third-party diagrams reproduced with attribution but no documented permission**: `lora-weights-raschka.png` (15.1), `raschka-bpe-overview.jpg` (module-02), NVIDIA RAG diagram (20.1.3), Lambert/HF + Huyen RLHF (17.1.2a/b), Lilian Weng diffusion (27.1.3), Edge et al. GraphRAG (20.3.4). Recommend redrawing.
  3. **Cover is placeholder** pending Gemini-variant promotion.

  YELLOW: KDP asks an "AI image disclosure" question — answer YES (Gemini-generated cover + many illustrations).

- **#11 + #12 Diagram regeneration via Gemini Imagen 4**: 5 priority figures regenerated with 4 variants each = 20 PNG variants in `KDP/diagrams/regenerated/`. Per-figure recommendations in `KDP/diagrams/regenerated/_review.md`:
  - Figure 4.2.2 (decoder-only Transformer) → variant 3
  - Figure 4.1.5 (Pre-LN vs Post-LN) → variant 3
  - Figure 3.1.5 (LSTM cell) → variant 1
  - Figure 3.3.3 (multi-head attention) → variant 1
  - Figure 34.10 (domain tokenization) → variant 1

  Generation script: `KDP/build/regenerate_diagram.py`. Reusable for any diagram.

  **Note discovered**: `section-4.1.html` line 778 has a mislabelled `<img>` reference (separate tracking item).

- **Image-caption alignment audit** (still running per latest check) — will report when complete.

### Final EPUB metrics

| | |
|---|---|
| EPUB size | **40.99 MB** (essentially unchanged through all source fixes) |
| epubcheck | **0 fatals / 0 errors / 0 warnings** |
| Spine | 444 chapters |
| Source HTML changes | 6 fixers run, each idempotent + backed up |
| Sample PDF | 3.15 MB / 56 pages, with code highlighting + rendered math |

### Pipeline scripts added this batch

| Script | Purpose | Re-runnable? |
|--------|---------|---------------|
| `fix_section_numbering.py` | H2 → hierarchical N.M.K | ✅ idempotent |
| `fix_code_fragment_numbering.py` | Code Fragment N → X.Y.N | ✅ idempotent |
| `dedup_code_fragments.py` | Suffix in-file dups with a, b, c | ✅ idempotent |
| `fix_unicode_math.py` | Combining `̂` → LaTeX `\hat{}` | ✅ idempotent |
| `fix_double_escaped_entities.py` | `&amp;X;` → `&X;` | ✅ idempotent |
| `compress_images.py` | Pillow PNG/JPEG re-encode | ✅ idempotent (timestamp check) |
| `regenerate_diagram.py` | Gemini Imagen 4 diagram gen | ✅ caches by figure ID |
| `render_epub_samples.py --random N` | Random-sample visual QA | ✅ idempotent |

---

## Pending / deferred (work for follow-up sessions)

### Visual quality (further iteration)
- Render 20+ random pages, not just my 7 samples (for systematic coverage)
- Test on actual Kindle Previewer (Edge `--print-to-pdf` triggers print media,
  which is NOT what real EPUB readers do)
- Verify math rendering with KaTeX in a real Kindle-emulated environment
- Verify code highlighting (Pygments-tokenized in EPUB build script)

### Sample chapter PDF improvements
- Currently 16.4 MB / 64 pages (chapter index + 2 sections)
- **Code is NOT highlighted in the PDF** — Pygments runs in build_epub.py for
  EPUB but NOT in build_sample_pdf.py. Either:
   a. Process source HTML through the same Pygments step before PDF generation
   b. Render PDF FROM the EPUB's chapter XHTML (which has Pygments markup)
- Inline math may render incorrectly in PDF (KaTeX is server-side rendered in
  EPUB but the sample PDF script reads source HTML directly, so JS-dependent
  math doesn't render). Same fix as above (a).

### Publishing-quality PDF generation (long-form)
Recommendation tiers, free → paid:
1. **WeasyPrint** (free, Python) — closest free equivalent to PrinceXML for
   typography. No JS support but math can be pre-rendered. Best for
   technical books with code + math + figures. Install: `pip install weasyprint`
   (needs GTK runtime on Windows).
2. **Pandoc + LaTeX** (free) — best mathematical typesetting in the world.
   Install: pandoc (already on PATH) + MikTeX or TeX Live (~3 GB). Best for
   long technical books, especially with heavy math. Trade-off: requires
   LaTeX templates that need maintenance.
3. **Vivliostyle** (free, Node) — modern CSS Paged Media tool. Good for HTML
   sources where you want to keep CSS-only styling. Less mature than WeasyPrint.
4. **PrinceXML** (commercial, $1,900-7,000/year) — gold standard for
   typography. Used by O'Reilly, Manning, MIT Press. Worth the cost only
   if doing 5+ titles per year.
5. **DocRaptor** (cloud API, ~$20-200/month) — PrinceXML-as-a-service.
   Cheaper for occasional use.

For LLMBook specifically: I'd recommend WeasyPrint as the next investment.
Edge headless is fine for sample chapters but the typography (margins,
running heads, page numbers, cross-references with page numbers, footnotes)
is much better in WeasyPrint.

### Image compression strategy
Recommended tools (in order of safety):
1. **`oxipng`** — PNG lossless re-compression. Always safe, ~20-40% size reduction.
   Install: `cargo install oxipng` or download binary.
2. **`pngquant`** — PNG → 8-bit quantized PNG (lossy but visually identical
   for diagrams/illustrations at < 256 colors). 60-80% reduction.
   Install: download binary from pngquant.org.
3. **`mozjpeg`** / **`cjpeg-tran`** — JPEG re-compression with progressive
   encoding + better quantization tables. ~10-30% reduction, lossless OR
   lossy (configurable). Install: download mozjpeg binary.
4. **AVIF/WebP**: NOT supported by all EPUB readers. Stay with PNG/JPEG.

Recommended workflow: `oxipng -o max` on all PNGs, `mozjpeg -quality 80` on
all JPEGs. Test on actual Kindle Paperwhite (e-ink) before adopting:
illustrations should still look good at 60 DPI.

For diagrams specifically: at 1280×... resolution + lossy JPEG Q78,
diagrams already look fine on tablets. Going further (1024×Q70) saves
another 30% but risks visible compression artifacts on detailed diagrams.

### Copyright / legal validation checklist
For KDP submission:
- [ ] **Fonts**: confirm OFL/Apache license for Source Serif 4 and Source Code Pro
      (both Adobe Source family, OFL — embeddable). KaTeX fonts: KaTeX BSD-MIT
      hybrid (also embeddable).
- [ ] **Images**: confirm rights for all images. The cover artwork was generated
      via Gemini (your rights). Chapter illustrations: same. Agent avatars: same.
      Diagrams: most are Mermaid-rendered (yours).
- [ ] **Quoted text**: epigraphs are AI-character "Wisdom Council" quotes you
      authored — no third-party rights needed.
- [ ] **Code samples**: original code (yours) — confirm no copy-pasted snippets
      from blogs/papers without attribution. Audit recommended for chapters
      with substantial existing-library reproduction (Hugging Face docs, etc.)
- [ ] **Bibliography references**: titles + authors + DOIs are facts (not
      copyrightable). Quoted abstracts >50 words may need permission.
- [ ] **Trademarks**: GPT, Claude, Gemini, etc. are trademarks of their owners.
      Use as references is fair use; avoid implying endorsement.
- [ ] **Publishing imprint**: KDP requires authors to have rights to all content.
      Add explicit "All rights reserved" + author copyright in front matter.

### Diagram quality audit
Per `KDP/validation/figure_audit.md` — 130 fig-* PNG diagrams, ~50 are wide-
aspect Mermaid auto-renders that don't fit Kindle. Per-figure regen via Gemini
documented; not yet executed.

### "Better diagrams" workflow (Gemini, not Mermaid)
**Recommended approach**:
1. Identify diagram by section + concept (e.g. "Figure 4.1.3 - encoder-decoder data flow")
2. Write a prompt that:
   a. States the technical concept precisely (e.g., "Show data flowing through an
      encoder-decoder Transformer: input embeddings → encoder stack with N
      identical blocks → cross-attention to decoder stack → output projection
      → softmax → next-token probabilities")
   b. Specifies visual style: "technical infographic, isometric or schematic,
      flat colors with subtle gradients, sans-serif labels, max 6 distinct
      colors, white background"
   c. Specifies AVOID: "no clipart, no boxes-with-text-only, no labels exceeding
      4 words per box, no horizontal flow when concept is sequential"
   d. Specifies aspect: "portrait 3:4 for narrow Kindle viewport, OR landscape
      4:3 ONLY if concept is fundamentally horizontal"
3. Generate 4 variants via Imagen Ultra, pick best
4. Verify technical accuracy (is the encoder really BEFORE the decoder?
   are residuals shown? does the diagram match the chapter text?)
5. If needed: artwork-only generation + manual label overlay in graphics tool

Add to pipeline: `KDP/build/regenerate_diagram.py --section 4.1 --figure 4.1.3
--concept "encoder-decoder data flow"`. Caches to `KDP/diagrams/regenerated/`.

### Things to wire into pipeline (publish.py)
- `KDP/build/render_epub_samples.py --max-pages 2` step that warns if the
  rendered first-page sample shows fewer than N styled elements (sanity check
  for "did the CSS load")
- `KDP/build/fix_double_escaped_entities.py --check` (read-only mode, fails if
  any double-escaped entities found)
- Math rendering integrity check (assert all `$$...$$` blocks were converted to
  `katex-rendered` spans)
- Reference book.css rule audit (warn on any rule that uses `attr(href)` or
  `display: none` on `.callout` etc.)

### Image-caption alignment (background agent in flight)
Audit running. Will report findings + apply mechanical caption-number fixes
where safe.

### "&odot" type bugs
Fixed (7 entities across 5 files). One-shot script `fix_double_escaped_entities.py`
re-runnable any time.

### Visual contrast / layout fixes (2026-05-10, batch)

User reported these as visual issues during EPUB inspection:

1. **Code blocks bad contrast** (light cyan on dark navy = invisible).
   Root cause: `book.css` set `pre { background: var(--code-bg); color: var(--code-text); }` (dark theme) but our Pygments token rules in `epub_overrides.css` use DARK colors (`#007020` keyword green, `#4070a0` string blue) intended for LIGHT bg. Result: dark on dark.
   Fix: force light `#f6f8fa` bg + dark `#24292f` default text on all `pre` blocks in EPUB overrides; add `print-color-adjust: exact` so Edge `--print-to-pdf` doesn't strip the bg.

2. **Table headers low contrast** (gold on white).
   Fix: force `th { background: #2a3142; color: white; font-weight: bold }` for all `table th`, `.data-table th`, `.comparison-table th`, `.syllabus-table thead th`.

3. **Pathways cards 2-per-row too dense** for narrow Kindle viewport.
   Root cause: `grid-template-columns: repeat(auto-fit, minmax(280px, 1fr))` keeps 2 columns at ~600 px Kindle width.
   Fix: force single column for `.pathway-diagram, .pathway-row, .fm-cards, .fm-grid, .cards-grid, .pathway-grid` in EPUB.

4. **Code Fragment caption misaligned with code box**.
   Root cause: `<pre>` has 1 px border + radius; `.code-caption` div sits below with default margins → visually disconnected.
   Fix: caption now `margin-top: 0`, no top border, `border-radius: 0 0 4px 4px` so it visually attaches to the code block's bottom edge.

5. **MSE Y-hat displaced + math hats/superscripts not working**.
   Root cause: source uses combining diacritic `ŷ` (decomposed) instead of LaTeX `\hat{y}`. KaTeX cannot render combining accents reliably inside math mode — produces a y with floating circumflex offset.
   Fix: `KDP/build/fix_unicode_math.py` walks all source HTML, finds math blocks (`$$...$$`, `\(...\)`, `<span class="math">`), replaces `letter + combining mark` with proper LaTeX (`\hat{}`, `\bar{}`, `\tilde{}`, `\dot{}`, `\mathring{}`). Handles ASCII letters AND Greek letters (`θ̂` → `\hat{\theta}`). Idempotent. Also handles precomposed forms (U+0177 ŷ etc.) for completeness.
   Found 5 instances across 2 files (section-0.1, section-1.3).

6. **Section numbering flat "1, 2, 3" (chapter 0)** — confusing for readers.
   Root cause: source HTML uses `<h2>1. Feature Engineering</h2>`, `<h2>2. Supervised Learning</h2>` etc. This is a content/structure decision in source HTML, not a build-script issue. Recommendation: rewrite source headings to `<h2>0.1 Feature Engineering</h2>` etc., OR add CSS counter-based numbering (`h2::before { content: counter(section); }` + `body { counter-reset: section }` + `h2 { counter-increment: section }`). The CSS approach is the safer mechanical fix because it doesn't touch source content.

### Math inline with text
In source HTML inline math uses `<span class="math">$x^2$</span>`. After
KaTeX server-side rendering, this becomes `<span class="katex-rendered">...</span>`.
The CSS in epub_overrides.css uses `display: inline-block` for inline math
which keeps it flowing with text. Display math (`$$...$$` standalone) becomes
`.katex-display` block element with center-align.

Verification: render section-4.3 page 2+ to see math examples in context.


These were called out in audits or session asks but await direction or more work:

### Tables

- 26 HIGH-severity tables (8-9 columns, won't fit Kindle) — see [tables_audit.md](validation/tables_audit.md). Worst offenders:
  - `appendix-v-tooling-ecosystem` (2 HIGH 8-col tables)
  - `appendix-h-model-cards` (2 HIGH 8-col tables)
  - `module-08-reasoning` (2 HIGH 8-col tables)
  - `appendix-j-datasets-benchmarks` (multiple)
  - `front-matter/section-fm.8` (1 HIGH 9-col)
  - `part-9-safety-strategy/module-34-strategy-product-roi/section-33.4` (2 HIGH)
- 27 MEDIUM-severity tables — verify in Kindle Previewer

### Figures

- 50+ Mermaid-style diagrams flagged in [figure_audit.md](validation/figure_audit.md)
  - Highest-priority for Gemini regeneration (foundation chapters):
    - `fig-4.2.2-decoder-only.png` (the example user flagged)
    - `fig-3.1.5-lstm-cell.png`
    - `fig-3.1.6-encoder-decoder-seq2seq.png`
    - `fig-3.3.3-multi-head.png`
    - `fig-4.1.7-residual-stream.png`
    - `fig-4.3.6-pre-post-ln2.png`
  - Worst aspect outliers (won't render at all):
    - `fig-34.10-domain-tokenization.png` (6.58 aspect)
    - `fig-31.5.1-otel-llm-trace.png` (0.34 aspect)
- Mermaid source files in `scripts/mermaid/` may exist — re-render via Mermaid is faster than Gemini for any figure where source is available

### Quality audit residuals (from book_quality_report.md)

- 41 duplicate code-fragment numbers (part-8/9, section-22.7)
- 60 chapter pages missing bibliographies
- 106 of 108 appendix sections without bibliographies
- 1 stale module-slug link in part-4/section-13.8
- 18 source HTML files with well-formedness issues (build sanitizes them, source should be cleaned)
- 587 inline `style=` attributes in 5 files (wisdom-council, section-1.2, section-4.1)

### Adoption / external

- Author Central setup (both authors, ~1 hour each — manual, requires Amazon login)
- Endorsement outreach (3-5 industry figures via templates in ADOPTION_PLAYBOOK.md)
- Pre-launch ARC outreach (50 reviewers via BookSirens / direct)
- Multi-distribution: Draft2Digital for Apple Books / Kobo / Google Play
- Companion GitHub repository skeleton
- Cover thumbnail variants ready (`cover_gemini_thumbnail_*` and `cover_gemini_minimalist_*`) — not yet promoted to active `cover_kdp.jpg`

### Infrastructure

- Companion landing page deployment to llmbook.apartsin.com (DNS + hosting setup)
- Sample chapter PDF generation (currently linked from landing page, file not yet created)

---

## Cover variants — choices ready for promotion

| Variant file | Notes |
|--------------|-------|
| `cover_kdp.jpg` (current) | Upscaled placeholder from 896x1200 source |
| `cover_gemini_with_text_v20260510-090146.jpg` | Painterly tree + full title + subtitle |
| `cover_gemini_artwork_v20260510-090146.jpg` | Artwork only, overlay typography in graphics tool |
| `cover_gemini_thumbnail_v20260510-090146.jpg` | **Huge title, no subtitle, optimized for 250px Amazon thumbnail** |
| `cover_gemini_minimalist_v20260510-090146.jpg` | **O'Reilly/MIT-Press style, abstract tree icon** |
| `cover_gemini_with_text_i2i_v20260510-072934.jpg` | Image-to-image variant (preserves source composition) |

To promote any variant:
```bash
cp KDP/cover/cover_gemini_<variant>.jpg KDP/cover/cover_kdp.jpg
python KDP/build/publish.py --clean
```

---

## Tools installed locally

| Tool | Path | Purpose |
|------|------|---------|
| Temurin OpenJDK 17 JRE | `E:/Tools/epubcheck/jdk-17.0.19+10-jre/` | Run epubcheck |
| EPUBCheck 5.1.0 | `E:/Tools/epubcheck/epubcheck-5.1.0/epubcheck.jar` | EPUB schema validation |
| Node.js 24 + pnpm 11 | `C:/Program Files/nodejs/` | epub-optimizer runtime |
| epub-optimizer 2.1.1 | `E:/Tools/epub-optimizer/dist/src/pipeline.js` | Final-stage EPUB minification + image compression |
| Source Serif 4 + Source Code Pro fonts | `E:/Tools/fonts/` (sources), `KDP/build/fonts/` (subsets) | Embedded fonts |
| Kindle Previewer 3 | `~/AppData/Local/Amazon/Kindle Previewer 3/` | Visual preview (auto-detected by `--preview` flag) |

---

## Pipeline commands reference

```bash
# Default: build + validate + optimize + re-validate
python KDP/build/publish.py

# Clean rebuild from scratch (use after spine changes)
python KDP/build/publish.py --clean --regen-spine

# Quick iteration (smaller images, faster)
python KDP/build/publish.py --quick

# Validate-only (no rebuild)
python KDP/build/publish.py --validate-only

# Build + open Kindle Previewer GUI for visual inspection
python KDP/build/publish.py --preview

# Skip optimization (raw build only)
python KDP/build/publish.py --no-optimize

# Skip Java epubcheck (Python structural validator only)
python KDP/build/publish.py --no-epubcheck

# Apply source HTML fixes (regex-based, idempotent)
python KDP/build/apply_source_fixes.py

# Generate cover variants
python KDP/cover/generate_cover_gemini.py --all-variants

# Generate font subsets (re-run if vocabulary changes substantially)
python KDP/build/subset_fonts.py
```
