# PDF Generation Tools — Recommendation for Print-Quality Book PDF

If you want to ship a **print-quality** PDF (not just a screen-readable one), the choice depends on three things:
1. **Math fidelity** — this book has 279 display equations + 957 inline math expressions
2. **Code rendering** — Pygments-tokenized code blocks, callouts with backgrounds + icons
3. **Budget + complexity tolerance**

Current PDF in the pipeline (Edge headless `--print-to-pdf`) is **acceptable for screen reading**, but isn't print-publisher-grade — no real running headers, footnotes break across pages, image DPI is screen-grade.

---

## Tool comparison

### Tier 1 — Recommended for this book

| Tool | License | Output Quality | Math | Code | Complexity | Notes |
|------|---------|---------------|------|------|------------|-------|
| **WeasyPrint** | BSD (free) | Excellent CSS Paged Media | Good (KaTeX HTML) | Excellent (Pygments) | Low | Best free option; you already have all the inputs |
| **Pandoc + LaTeX** (XeLaTeX) | GPL (free) | Print-publisher grade | **Excellent** (native LaTeX) | Excellent | High (3 GB install) | Highest math quality; standard for academic books |
| **PrinceXML** | Commercial $1,950/yr | Industry gold standard | Excellent | Excellent | Low | What O'Reilly, MIT Press, etc. use |

### Tier 2 — Acceptable for screen sample

| Tool | License | Output Quality | Notes |
|------|---------|---------------|-------|
| **Edge / Chrome headless** (current) | Free | Good for screen, weak for print | Already wired into pipeline; produces 16 MB sample for chapter 11 |
| **Calibre `ebook-convert`** | GPL | Quick EPUB→PDF, "good enough" for proofing | Single command from existing EPUB; no further setup |
| **Vivliostyle CLI** | AGPL | CSS Paged Media support | Newer alternative to WeasyPrint, fewer plugins |

### Tier 3 — Not recommended

- **wkhtmltopdf** — abandoned upstream, ancient WebKit, no CSS Paged Media
- **PuppeteerSharp / pyppeteer** — same Chrome backend as Edge but more setup
- **DocRaptor / Cloud APIs** — uploads your manuscript to a third party (privacy + cost concerns)

---

## Recommendation for this book

### Path A: Quick, free, "good enough" → **WeasyPrint** (~2 hours setup)

Best for: a downloadable companion PDF on the landing page that looks polished but isn't aimed at print production.

```bash
pip install weasyprint
# On Windows: also install GTK runtime (https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer)
weasyprint chapter-source.html chapter.pdf
```

**Pros**: Pure Python, integrates cleanly with the existing pipeline, no LaTeX install.
**Cons**: Math via KaTeX HTML+CSS (works but visually less crisp than LaTeX); you'd add fonts manually.

### Path B: Print-publisher quality → **Pandoc + XeLaTeX** (~6 hours setup, ~12 hours tuning)

Best for: a real print edition you'd submit to KDP paperback / Lulu / IngramSpark.

```bash
# Install MacTeX / TeX Live / MiKTeX (~3 GB)
choco install miktex   # Windows via Chocolatey
# OR
winget install MiKTeX.MiKTeX

# Pandoc already on your PATH
pandoc chapter.html -o chapter.pdf \
    --pdf-engine=xelatex \
    --template=memoir.tex \
    -V geometry:margin=1in \
    -V documentclass=memoir \
    -V mainfont="Source Serif 4" \
    -V monofont="Source Code Pro"
```

**Pros**: Best math, hyphenation, microtype, page breaks, footnotes. Industry-standard for technical/academic books.
**Cons**: Heavy install, LaTeX template tuning is its own skill, error messages cryptic.

### Path C: If budget allows → **PrinceXML** (~$1,950/yr)

What O'Reilly, MIT Press, Manning publishers use internally. Best CSS Paged Media support.

```bash
# Free 30-day trial: https://www.princexml.com/
prince chapter.html -o chapter.pdf
```

**Pros**: Drop-in replacement for WeasyPrint with better edge-case handling. Excellent footnote support.
**Cons**: Annual subscription; vendor lock-in.

---

## Migration path

If you eventually want a print-quality PDF, the cleanest path:

1. **Today**: keep Edge headless for the sample chapter (16 MB, fast, screen-readable)
2. **Phase 2** (when you want a downloadable full-book PDF): add WeasyPrint as a parallel pipeline stage. Keep Edge as the "preview" output, add `pdf_print/` as the "publication-quality" output.
3. **Phase 3** (if you want a print paperback): switch the publication-quality stage to Pandoc + XeLaTeX, tune the template.

Stage 2 estimated effort: 4-8 hours for the WeasyPrint pipeline + CSS Paged Media tuning (`@page`, `@bottom-center`, `running-headers`, etc.).
Stage 3 estimated effort: 12-20 hours including a LaTeX template that mirrors the book's design system (callouts, code blocks, agent epigraphs, illustrations).

---

## Sample WeasyPrint config (drop-in)

`KDP/build/build_print_pdf.py` (sketch):

```python
from weasyprint import HTML, CSS
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

PRINT_CSS = """
@page {
    size: 7in 9in;  /* common technical-book trim size */
    margin: 0.75in 0.6in 0.85in 0.6in;
    @top-center { content: "Building Conversational AI with LLMs and Agents"; font-size: 9pt; color: #777; }
    @bottom-center { content: counter(page); font-size: 10pt; }
}
@page :first { @top-center { content: ""; } @bottom-center { content: ""; } }

h1 { page-break-before: always; }
h2, h3 { page-break-after: avoid; }
pre, table, figure, .callout { page-break-inside: avoid; }

img { max-width: 100%; }
"""

def build_print_pdf(source_html: Path, output_pdf: Path):
    HTML(filename=str(source_html), base_url=str(source_html.parent)).write_pdf(
        str(output_pdf),
        stylesheets=[CSS(string=PRINT_CSS), CSS(filename=str(PROJECT_ROOT / "styles" / "book.css"))],
        font_config=None,
    )
```

Then add as a step in `publish.py` gated on `--print-pdf` flag.

---

## What you do NOT want for this book

- **Inkscape PDF export** — only for SVG-only documents, no HTML support
- **Microsoft Word "Save as PDF"** — would require importing the book into Word first; loses code highlighting + math
- **Acrobat Pro print profiles** — useful for PDF post-processing, not generation
- **Adobe InDesign** — beautiful output but requires importing all 470 HTML files into IDML format manually

---

## Sources

- [Top 23 HTML to PDF Conversion Tools 2026 (IronSoftware)](https://ironsoftware.com/suite/blog/comparison/html-to-pdf-2026-guide/)
- [WeasyPrint](https://weasyprint.org/)
- [PrinceXML](https://www.princexml.com/)
- [Vivliostyle](https://vivliostyle.org/)
- [print-css.rocks (CSS Paged Media tutorial)](https://print-css.rocks/tools)
- [Pandoc vs WeasyPrint comparison (StackShare)](https://stackshare.io/stackups/pandoc-vs-weasyprint)
- [HTML to PDF benchmark 2026 (PDF4.dev)](https://pdf4.dev/blog/html-to-pdf-benchmark-2026)
- [Best wkhtmltopdf Alternatives (DocRaptor)](https://docraptor.com/wkhtmltopdf-alternatives)
