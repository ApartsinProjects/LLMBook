# EPUB Quality, Layout & Typesetting Tools

A practical inventory of tools and libraries for improving EPUB quality beyond what `KDP/build/publish.py` already does, organized by how much each would move the needle for **this book**. Each entry has install commands, when to use, and how it would integrate with the existing pipeline.

For **validation** tools (epubcheck, Ace, Kindle Previewer) see [`validation/epub_tools_comparison.md`](validation/epub_tools_comparison.md).

---

## What this book needs most (ranked)

This book's current weak points (from your manual review and the diagram audit):

1. **File size**: 72 MB EPUB; KDP delivery fee ~$10/sale at 70% royalty. Every MB shaved is direct margin.
2. **Typography**: Reflowable EPUB, mostly default reader styling. Could improve readability with a real eBook CSS framework.
3. **Embedded fonts**: None. Currently relies on reader's default font. Embedding would standardize rendering.
4. **Image sizes**: ~500 raster images, average 681 KB. Build script does Lanczos resize + JPEG-82, but professional encoders (MozJPEG, AVIF) compress 30-50% better.
5. **Diagram quality**: 1,576 diagram-related issues from audit; many SVGs need redraw, some PNGs should be SVG.

The tools below address these in order.

---

## Tier 1: Would significantly improve THIS book

### 1. epub-optimizer (Node.js, MIT)

> [github.com/kiki-le-singe/epub-optimizer](https://github.com/kiki-le-singe/epub-optimizer)

**The single most impactful tool we haven't used.** Node.js pipeline that minifies HTML/CSS/JS, compresses images (MozJPEG + OxiPNG + WebP + AVIF), subsets embedded fonts, optimizes inline SVGs, and re-packages the EPUB with optimal zip compression. Reported 70-90% size reductions are realistic.

**For this book**: should bring the 72 MB EPUB down to **20-30 MB**, which puts the 70% royalty plan back on the table (delivery fee drops from $10.61 to $3-4 per sale).

```bash
# Requires Node.js 18+
git clone https://github.com/kiki-le-singe/epub-optimizer
cd epub-optimizer && pnpm install && pnpm build
node dist/cli.js optimize \
    -i E:/Projects/BookBlogsHome/LLMBook/KDP/output/building-conversational-ai-llms-agents.epub \
    -o E:/Projects/BookBlogsHome/LLMBook/KDP/output/building-conversational-ai-llms-agents.optimized.epub
```

**Pipeline integration**: drop in as a final step in `publish.py` after `step_epubcheck`, gated by Node.js availability. Could shave 50 MB off every build.

### 2. Squoosh CLI (Node.js, Apache-2.0)

> [github.com/GoogleChromeLabs/squoosh](https://github.com/GoogleChromeLabs/squoosh) · [browser app](https://squoosh.app)

Google Chrome Labs' image compression toolkit. Bundles MozJPEG (JPEG), OxiPNG (PNG), libwebp (WebP), AVIF encoder, JPEG XL — all running via WebAssembly so no native deps. CLI is unmaintained as of 2024 but the WASM cores work fine.

**For this book**: better than our PIL-based JPEG re-encode for the 654 raster images. MozJPEG typically beats PIL/libjpeg quality at the same file size by 15-30%. Could shrink the image budget from 50 MB to 30 MB.

```bash
npm install --global @squoosh/cli@0.7.3   # last working version
squoosh-cli --mozjpeg '{"quality":75}' \
    --resize '{"enabled":true,"width":1200}' \
    -d compressed/ \
    images/*.png
```

**Better alternative for this project**: since you have Python and PIL, install `mozjpeg` as a CLI binary and pipe PIL output through it, OR use `pillow-heif` + AVIF for next-gen formats. AVIF support in Kindle is still spotty though, so stick with MozJPEG for now.

### 3. Blitz CSS Framework (LESS/CSS, MIT)

> [github.com/FriendsOfEpub/Blitz](https://github.com/FriendsOfEpub/Blitz) · [docs](https://friendsofepub.github.io/Blitz/) · [intro tutorial](https://medium.com/@jiminypan/blitzintrotutorial-270da9f853c0)

Battle-tested EPUB 3 CSS framework by Jiminy Panoz (a published EPUB-typography expert). Provides:
- Sensible vertical rhythm computed via LESS variables
- Cross-reader compatibility shims (EPUB 2.0.1, MOBI 7, modern Kindle, Kobo, Apple Books)
- Typography scale that handles user font-size adjustments gracefully
- Ready-made callout, code, blockquote, table, and figure styles
- `blitz-lite.css` (small, novels) and full `blitz.css` (technical books)

**For this book**: would replace much of [`KDP/build/epub_overrides.css`](KDP/build/epub_overrides.css). Right now I hand-rolled the CSS overrides; Blitz has solved 90% of those problems already, with edge cases tested across readers we don't have access to.

```bash
# No npm package; clone and bundle the CSS file
git clone https://github.com/FriendsOfEpub/Blitz
cp Blitz/Blitz_framework/CSS/blitz.css KDP/build/blitz.css
# Or use blitz-lite.css for novels
```

**Pipeline integration**: bundle `blitz.css` into the EPUB before `epub_overrides.css`. Reduce our overrides to just the agent-avatar / pygments / book-specific bits.

---

## Tier 2: Worth considering for v2

### 4. FontTools / pyftsubset (Python, MIT)

> [github.com/fonttools/fonttools](https://github.com/fonttools/fonttools) · [pyftsubset docs](https://fonttools.readthedocs.io/en/latest/subset/)

Industry-standard font manipulation library. The `pyftsubset` CLI subsets a font to only the glyphs actually used in your document, often shrinking a 200 KB serif font to 30-50 KB.

**For this book**: only relevant if you decide to **embed fonts** (currently you don't). Pros of embedding: consistent rendering across readers, better typography (e.g., proper italics, small caps, ligatures). Cons: +50-200 KB per font face, licensing complexity (commercial fonts need EPUB licenses).

If you go this route, the workflow:
1. Pick fonts (e.g., Source Serif Pro for body, Source Code Pro for code, Source Sans Pro for headings — all SIL OFL, safe for commercial use)
2. Subset with pyftsubset to only include code points used in the manuscript
3. Reference in CSS with `@font-face`
4. Bundle into the EPUB and update OPF manifest

```bash
pip install fonttools
pyftsubset SourceSerif.ttf \
    --text-file=all-book-text.txt \
    --output-file=SourceSerif-subset.woff2 \
    --flavor=woff2 \
    --layout-features=kern,liga,onum
```

### 5. epub-font-subsetter (Python, GPL)

> [github.com/transpect/epub-font-subsetter](https://github.com/transpect/epub-font-subsetter)

Specialized pipeline that takes an EPUB, walks all XHTML files, collects every used character per embedded font, and runs `pyftsubset` automatically. Wraps the workflow above into a single command.

**For this book**: if/when you embed fonts, this is the easiest way to keep them subsetted on every build. Adds Python deps; integrates cleanly into `publish.py`.

### 6. EbookLib successor: yael (Python, status unclear)

> Mentioned as PyEPUB's successor; very low activity in 2024-2026.

Skip for now — `ebooklib` is the actively maintained choice. If you ever need EPUB **reading** (not just writing) for advanced introspection, `ebooklib` covers it; `yael` doesn't add enough to justify migration.

### 7. Sigil EPUB Editor (free, GPL)

> [sigil-ebook.com](https://sigil-ebook.com)

Cross-platform desktop EPUB editor. Lets you open the built EPUB, inspect the OPF/spine/manifest, hand-edit any XHTML, run epubcheck inline, and re-save. Best for one-off surgery on a specific chapter that the build script can't easily fix.

**For this book**: not part of the pipeline, but useful for verifying changes look right after a build, or for hand-fixing a single problematic chapter without round-tripping through the build.

```bash
# Windows
winget install Sigil-Ebook.Sigil
```

(winget now works in your shell.)

### 8. Calibre (free, GPL)

> [calibre-ebook.com](https://calibre-ebook.com)

Heavyweight EPUB swiss-army-knife. Reader, editor, format converter (EPUB ↔ MOBI ↔ AZW3 ↔ PDF), library manager. Includes its own EPUB validator (which calls EPUBCheck under the hood).

**For this book**: most useful as a **device-rendering preview** — Calibre's reader emulates Kindle Paperwhite, Kobo Glo, etc. with reasonably accurate fonts and reflow. Faster than spinning up Kindle Previewer for quick checks.

```bash
winget install calibre.calibre
```

---

## Tier 3: Useful for specific scenarios

### 9. optibook (Perl)

> [github.com/fleger/optibook](https://github.com/fleger/optibook)

Older alternative to epub-optimizer. Same approach (image compression + CSS/HTML minification + font subsetting). Perl-based; install friction higher than Node.js. **Skip in favor of epub-optimizer.**

### 10. epubkit (web-based)

> [github.com/b1rdmania/epubkit](https://github.com/b1rdmania/epubkit)

Browser-based EPUB optimizer aimed at e-ink readers. Strips fonts, cleans CSS, fixes TOC. Similar to epub-optimizer but no install. **Useful for quick one-off optimization without setting up Node.js.**

### 11. Readium-js (JavaScript)

> [github.com/readium/readium-js](https://github.com/readium/readium-js)

Reference EPUB 3 processing engine in JavaScript. Used by the (deprecated) Readium Chrome reader. **Only relevant if you build a custom in-browser reader for the book**; not for KDP submission.

### 12. Pandoc (Haskell, GPL)

> [pandoc.org](https://pandoc.org) — already on your PATH (saw it in environment check)

Universal document converter. Can ingest Markdown, DOCX, LaTeX, HTML and emit EPUB 3, with reasonable defaults. Used by many self-publishers as the primary HTML→EPUB converter.

**For this book**: Pandoc would be a different architecture — collapsing source HTML through pandoc into one EPUB. Tradeoff: simpler one-liner, but loses the fine-grained control we have in `build_epub.py` (per-chapter spine ordering, image compression strategy, custom callout normalization, etc.). **Stick with the current pipeline.**

### 13. Vellum (commercial, Mac-only) / Atticus (commercial, web/desktop)

> [vellum.pub](https://vellum.pub) · [atticus.io](https://atticus.io)

Closed-source self-publishing tools. Beautiful default output, but require importing all content into their proprietary format. **Not worth the migration effort for an existing 470-file project.**

### 14. Adobe InDesign / Affinity Publisher / QuarkXPress

Professional desktop publishing software with EPUB export. **Worth considering only if you also want a print PDF** (these tools handle both); for EPUB-only, the build pipeline is more flexible.

### 15. Reedsy Book Editor (free, web)

> [reedsy.com/book-editor](https://reedsy.com/book-editor)

Web-based author tool with EPUB export. Markdown-based. **Same migration problem as Vellum** — would require restructuring an existing HTML-source project. Skip.

---

## CSS / typography references (not tools, but useful)

### BlitzTricks

> [friendsofepub.github.io/eBookTricks](https://friendsofepub.github.io/eBookTricks/)

Curated CSS recipes by the same Blitz authors. Covers tricky cross-reader problems (drop caps that work on Kindle, hyphenation that works on Kobo, table-of-contents styling for Apple Books, etc.). **Read this before tweaking [`epub_overrides.css`](KDP/build/epub_overrides.css)** — it'll save you hours of trial and error.

### EPUB 3 Best Practices (O'Reilly, free online)

> [oreilly.com/library/view/epub-3-best/9781449329129](https://www.oreilly.com/library/view/epub-3-best/9781449329129/)

Comprehensive book on EPUB 3, including font embedding chapter. Most chapters are free to read on the O'Reilly site.

### Accessible Publishing Best Practices

> [accessiblepublishing.ca PDF](https://www.accessiblepublishing.ca/wp-content/uploads/2019/08/AP-NNELS_Accessible_Publishing_Best_Practices_August_2019.pdf)

Free, ~80-page PDF guide. Important if you want to claim WCAG 2.1 / EU Accessibility Act compliance (which Amazon and EU retailers will increasingly require in 2025-2026).

---

## Recommended action plan for this book

If you want to invest 2-4 hours improving EPUB quality before launch, I'd do these in order:

| Step | Time | Impact |
|------|------|--------|
| 1. Install Node.js + run epub-optimizer on the existing build | 30 min | EPUB drops 70 MB → ~25 MB. Royalty math improves dramatically. |
| 2. Bundle Blitz CSS framework (replace `epub_overrides.css` with `blitz-lite.css` + the bits we need) | 60 min | Better cross-reader typography, fewer edge-case bugs |
| 3. Open in Calibre and Kindle Previewer; iterate on what looks bad | 60-90 min | Catch reader-specific rendering issues before KDP review |
| 4. (Optional) Embed Source Serif Pro + Source Code Pro fonts via FontTools | 60 min | Consistent typography across all reader devices |
| 5. Add epub-optimizer step to `publish.py` | 15 min | Optimization runs automatically on every build |

**Steps 1 and 5 alone would pay for themselves on the first 5 sales** through reduced delivery fees.

If I were doing this for you, I'd start with step 1 + 5 (most leverage, most automatable) and leave fonts/Blitz for v2 once you see real reader feedback.

Want me to wire up any of these? Specifically:

- **Install epub-optimizer and add it as a final pipeline step**? (Highest leverage)
- **Replace our CSS overrides with Blitz**? (Biggest typography improvement)
- **Embed open-source fonts**? (Most polished feel, adds 100-300 KB)

---

## Sources

**EPUB Optimizers**
- [epub-optimizer (kiki-le-singe)](https://github.com/kiki-le-singe/epub-optimizer)
- [optibook (fleger)](https://github.com/fleger/optibook)
- [epubkit (b1rdmania)](https://github.com/b1rdmania/epubkit)
- [DEV Community write-up on epub-optimizer](https://dev.to/boopykiki/epub-optimizer-1ek3)
- [Kite Metric: EPUB Optimizer 70-90% size reduction](https://kitemetric.com/blogs/epub-optimizer-streamline-your-ebook-workflow)

**Image Compression**
- [Squoosh (Google Chrome Labs)](https://squoosh.app/)
- [Squish - batch Squoosh fork (addyosmani)](https://github.com/addyosmani/squish)

**CSS Frameworks**
- [Blitz eBook Framework (FriendsOfEpub)](https://github.com/FriendsOfEpub/Blitz)
- [Blitz documentation](https://friendsofepub.github.io/Blitz/)
- [BlitzTricks - CSS recipes for ebooks](https://friendsofepub.github.io/eBookTricks/)
- [Blitz introductory tutorial (Medium)](https://medium.com/@jiminypan/blitzintrotutorial-270da9f853c0)

**Font Tools**
- [FontTools (Google Fonts team)](https://github.com/fonttools/fonttools)
- [epub-font-subsetter (transpect)](https://github.com/transpect/epub-font-subsetter)
- [O'Reilly EPUB 3 Best Practices: Font Embedding](https://www.oreilly.com/library/view/epub-3-best/9781449329129/ch04.html)

**Python EPUB Libraries**
- [EbookLib (aerkalov)](https://github.com/aerkalov/ebooklib)
- [EbookLib on PyPI](https://pypi.org/project/EbookLib/)
- [EbookLib documentation](https://docs.sourcefabric.org/projects/ebooklib/en/latest/)
- [pyepub (legacy, gabalese)](https://github.com/gabalese/pyepub)

**Editors**
- [Sigil EPUB Editor](https://sigil-ebook.com)
- [Calibre](https://calibre-ebook.com)

**Typography & Layout References**
- [DTPerfect: 3 CSS Tips for Reflowable e-books](https://dtperfect.com/3-css-tips-tricks-for-reflowable-ebooks/)
- [Mastering EPUB with HTML and CSS (tutorialpedia)](https://www.tutorialpedia.org/blog/epub-html-css/)
- [EPUB Knowledge: CSS General](https://epubknowledge.com/docs/css-general/)
- [Best Fonts for eBooks (Kitaboo, 2026)](https://kitaboo.com/best-fonts-for-ebooks/)
- [Accessible Publishing Best Practices (PDF)](https://www.accessiblepublishing.ca/wp-content/uploads/2019/08/AP-NNELS_Accessible_Publishing_Best_Practices_August_2019.pdf)

**Conversion Tools**
- [Pandoc](https://pandoc.org)
- [Reedsy Book Editor](https://reedsy.com/book-editor)
- [Vellum (Mac)](https://vellum.pub)
- [Atticus](https://atticus.io)
- [Kindlepreneur: Best Book Formatting Software 2026](https://kindlepreneur.com/book-formatting-software/)
- [SelfPublishing.com: 11 Book Formatting Software Options](https://selfpublishing.com/book-formatting-software/)
