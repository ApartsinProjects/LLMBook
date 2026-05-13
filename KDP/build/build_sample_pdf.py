"""
Build a self-contained PDF of one chapter for the landing page's free download.

Strategy:
  1. Take a chapter (index + all sections), concatenate into one HTML doc
     with inlined book.css so it renders standalone.
  2. Convert to PDF using Edge / Chrome headless (no install needed).

Default chapter: 11 (Prompt Engineering & Advanced Techniques).
Output: KDP/landing-page/downloads/sample-chapter-prompt-engineering.pdf

Usage:
    python KDP/build/build_sample_pdf.py
    python KDP/build/build_sample_pdf.py --chapter 22 --slug ai-agents
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
import tempfile
from pathlib import Path

from bs4 import BeautifulSoup

PROJECT_ROOT = Path(__file__).resolve().parents[2]
# Sample PDFs are served by GitHub Pages from /downloads/ at the repo root,
# linked from the existing index.html cover page (no separate landing site).
DOWNLOADS_DIR = PROJECT_ROOT / "downloads"

# Chapter -> module folder mapping. Add more as needed.
CHAPTERS = {
    12: ("part-3-working-with-llms", "module-12-prompt-engineering"),
    11: ("part-3-working-with-llms", "module-11-llm-apis"),
    19: ("part-5-retrieval-conversation", "module-19-rag"),
    21: ("part-6-agentic-ai", "module-21-ai-agents"),
    4:  ("part-1-foundations", "module-04-transformer-architecture"),
}


def find_browser() -> Path | None:
    """Locate a Chromium-family browser for headless PDF rendering."""
    import os
    candidates = [
        Path("C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"),
        Path("C:/Program Files/Microsoft/Edge/Application/msedge.exe"),
        Path("C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"),
        Path("C:/Program Files/Google/Chrome/Application/chrome.exe"),
        Path(os.environ.get("LOCALAPPDATA", "")) / "Google/Chrome/Application/chrome.exe",
        Path(os.environ.get("LOCALAPPDATA", "")) / "Microsoft/Edge/Application/msedge.exe",
    ]
    for c in candidates:
        if c.exists():
            return c
    return None


def assemble_chapter_html_from_epub(chapter_num: int) -> tuple[str, Path | None]:
    """Render the sample chapter from EPUB chapter XHTML files.

    Why: the EPUB chapter XHTML has Pygments syntax highlighting AND
    server-side KaTeX math already baked in (build_epub.py applies both).
    Reading from source HTML would lose both because:
      - source has Prism.js for code (JS-based, doesn't run in headless print)
      - source has KaTeX JS for math (same problem)

    Returns: (html_string, extract_dir_for_cleanup)
    """
    import zipfile
    epub_path = PROJECT_ROOT / "KDP/output/building-conversational-ai-llms-agents.epub"
    if not epub_path.exists():
        raise FileNotFoundError(f"EPUB not built yet: {epub_path}. Run publish.py first.")

    if chapter_num not in CHAPTERS:
        raise ValueError(f"Chapter {chapter_num} not registered. Add to CHAPTERS dict.")
    part_folder, module_folder = CHAPTERS[chapter_num]

    # Extract EPUB to a temp dir on E:
    extract_dir = Path("E:/temp/sample_pdf_epub_extract")
    if extract_dir.exists():
        import shutil
        shutil.rmtree(extract_dir, ignore_errors=True)
    extract_dir.mkdir(parents=True)
    with zipfile.ZipFile(epub_path) as zf:
        zf.extractall(extract_dir)

    # Find chapter XHTML files matching the module slug
    chapters_dir = extract_dir / "EPUB" / "chapters"
    module_slug = module_folder  # e.g., "module-11-prompt-engineering"
    matching = sorted(chapters_dir.glob(f"ch_*{module_slug}*.xhtml"))
    if not matching:
        raise FileNotFoundError(f"No chapter XHTML in EPUB matches {module_slug}")

    # Filter: index file first, then the first SAMPLE_SECTION_LIMIT section files
    SAMPLE_SECTION_LIMIT = 2
    index_file = next((f for f in matching if "index" in f.name), None)
    section_files = sorted([f for f in matching if "section-" in f.name])[:SAMPLE_SECTION_LIMIT]
    files = ([index_file] if index_file else []) + section_files

    print(f"  Assembling {len(files)} EPUB-rendered files (with Pygments + KaTeX)")

    # Read each chapter's body and concatenate
    pieces: list[str] = []
    chapter_title = ""
    for f in files:
        text = f.read_text(encoding="utf-8")
        soup = BeautifulSoup(text, "lxml")
        if not chapter_title:
            h1 = soup.find("h1")
            if h1:
                chapter_title = h1.get_text(strip=True)
        # Extract body content (skip head)
        body = soup.find("body")
        if body:
            # Strip nav.chapter-nav (next/prev links inside body)
            for nav in body.find_all("nav", class_="chapter-nav"):
                nav.decompose()
            for footer in body.find_all("footer"):
                footer.decompose()
            pieces.append('<div class="pdf-section">\n' + "".join(str(c) for c in body.children) + "\n</div>")

    return _wrap_pdf_html(pieces, chapter_title, len(files), extract_dir), extract_dir


def _wrap_pdf_html(pieces: list[str], chapter_title: str, n_files: int, extract_dir: Path) -> str:
    """Wrap chapter pieces in a complete PDF-ready HTML doc.

    Uses RELATIVE paths to the EPUB extract dir's CSS so all the styling
    (Blitz + book.css + epub_overrides + KaTeX) applies.
    """
    from html import escape as html_escape
    safe_title = html_escape(chapter_title)
    # The temp HTML lives at extract_dir/sample.html, so CSS is at EPUB/styles/...
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{safe_title} - Sample Chapter | Building Conversational AI with LLMs and Agents</title>
<link rel="stylesheet" href="EPUB/styles/blitz.css">
<link rel="stylesheet" href="EPUB/styles/katex.min.css">
<link rel="stylesheet" href="EPUB/styles/book.css">
<link rel="stylesheet" href="EPUB/styles/epub_overrides.css">
<style>
@page {{ size: A4; margin: 1.8cm; }}
body {{ max-width: 100%; }}
.header-nav, .chapter-nav, .toc-link, .book-title-link {{ display: none !important; }}
.pdf-section + .pdf-section {{ page-break-before: always; }}
img {{ max-width: 100%; height: auto; }}
.callout, pre, table, figure {{ page-break-inside: avoid; }}
h1, h2, h3 {{ page-break-after: avoid; }}

.pdf-cover {{ text-align: center; padding: 6cm 0 2cm; page-break-after: always; }}
.pdf-cover-tag {{ font-family: 'Helvetica Neue', sans-serif; text-transform: uppercase; letter-spacing: 0.25em; font-size: 0.85em; color: #666; margin-bottom: 1.4em; }}
.pdf-cover-title {{ font-family: Georgia, serif; font-size: 2.4em; font-weight: bold; margin-bottom: 0.4em; color: #1a1a2e; }}
.pdf-cover-subtitle {{ font-family: Georgia, serif; font-style: italic; font-size: 1.1em; color: #555; margin-bottom: 2em; }}
.pdf-cover-meta {{ font-family: 'Helvetica Neue', sans-serif; font-size: 0.95em; color: #444; line-height: 1.8; }}
.pdf-cover-cta {{ margin-top: 3em; padding: 1em 2em; background: #f4f4f4; border-left: 4px solid #0f3460; text-align: left; font-size: 0.9em; }}
</style>
</head>
<body>

<div class="pdf-cover">
    <div class="pdf-cover-tag">Sample Chapter &middot; Free Preview</div>
    <div class="pdf-cover-title">{safe_title}</div>
    <div class="pdf-cover-subtitle">From <em>Building Conversational AI with LLMs and Agents</em></div>
    <div class="pdf-cover-meta">
        Alexander Apartsin, Ph.D. &amp; Yehudit Aperstein, Ph.D.<br>
        Fifth Edition &middot; 2026<br><br>
        <strong>{n_files} sections</strong> assembled with full code highlighting and rendered math.
    </div>
    <div class="pdf-cover-cta">
        <strong>Like what you read?</strong> The full book has 39 chapters and 22 appendices,
        covering everything from PyTorch foundations to production AI agents.
        Available at <strong>llmbook.apartsin.com</strong> and on Amazon.
    </div>
</div>

{chr(10).join(pieces)}

</body>
</html>
"""


def assemble_chapter_html(chapter_num: int) -> str:
    """LEGACY: read from source HTML (no Pygments, no rendered math).
    Kept for reference; new code uses assemble_chapter_html_from_epub."""
    if chapter_num not in CHAPTERS:
        raise ValueError(f"Chapter {chapter_num} not registered. Add to CHAPTERS dict.")
    part_folder, module_folder = CHAPTERS[chapter_num]
    chapter_dir = PROJECT_ROOT / part_folder / module_folder
    if not chapter_dir.exists():
        raise FileNotFoundError(f"Chapter dir not found: {chapter_dir}")

    # Chapter index
    files = [chapter_dir / "index.html"]
    # Section files in order. SAMPLE = limit to first 2 sections so the PDF
    # stays under ~10 MB (full chapter is 30+ MB which is too big for a
    # "free download" preview - barrier to actually downloading and reading).
    sections = sorted(chapter_dir.glob("section-*.html"), key=lambda p: _section_sort_key(p.stem))
    SAMPLE_SECTION_LIMIT = 2  # index + 2 sections = decent preview at ~5-10 MB
    files.extend(sections[:SAMPLE_SECTION_LIMIT])

    print(f"  Assembling {len(files)} files from {chapter_dir.relative_to(PROJECT_ROOT)} "
          f"(limited to {SAMPLE_SECTION_LIMIT} sections of {len(sections)} for sample)")

    # Read each, extract <main class="content"> contents
    pieces: list[str] = []
    chapter_title = ""
    for f in files:
        soup = BeautifulSoup(f.read_text(encoding="utf-8"), "lxml")
        if not chapter_title:
            h1 = soup.find("h1")
            if h1:
                chapter_title = h1.get_text(strip=True)
        # Extract just <main class="content"> innerHTML, plus any <header> H1
        header = soup.find("header")
        main = soup.find("main", class_="content")
        section_html_parts = []
        if header:
            # Keep just the H1 and the part-label spans
            for tag in header.find_all(["h1", "div"], recursive=True):
                if tag.name == "h1":
                    section_html_parts.append(str(tag))
        if main:
            # Strip the chapter-nav at the bottom (don't want page-break-style nav in PDF)
            for nav in main.find_all("nav", class_="chapter-nav"):
                nav.decompose()
            for footer in main.find_all("footer"):
                footer.decompose()
            section_html_parts.append("".join(str(c) for c in main.children))
        pieces.append('<div class="pdf-section">\n' + "\n".join(section_html_parts) + "\n</div>")

    # Reference book.css via <link> instead of inlining (Edge headless on
    # Windows silently fails to render HTML files >300 KB with massive
    # inlined <style> blocks; linking keeps the HTML small and lets the
    # browser load CSS as a separate resource).
    # HTML-escape the title for the <title> tag (raw `&` is invalid HTML)
    from html import escape as html_escape
    safe_title = html_escape(chapter_title)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{safe_title} - Sample Chapter | Building Conversational AI with LLMs and Agents</title>
<link rel="stylesheet" href="../../styles/book.css">
<link rel="stylesheet" href="../../vendor/katex/katex.min.css">
<style>
/* ===== PDF-specific layout overrides ===== */

@page {{
    size: 6in 9in;            /* trade-paperback trim size, more book-like than A4 */
    margin: 0.75in 0.7in 0.85in 0.7in;
    @bottom-center {{
        content: counter(page);
        font-family: Georgia, serif;
        font-size: 9pt;
        color: #888;
    }}
}}
@page :first {{
    margin: 0.75in;
    @bottom-center {{ content: ""; }}
}}

body {{
    font-family: "Source Serif 4", "Source Serif Pro", Georgia, serif;
    font-size: 10.5pt;
    line-height: 1.45;
    color: #1a1a1a;
    max-width: 100%;
}}

/* Hide nav chrome */
.header-nav, .chapter-nav, .toc-link, .book-title-link, footer {{ display: none !important; }}
.part-label, .chapter-label {{ display: none !important; }}

/* PDF section breaks */
.pdf-section {{ page-break-before: avoid; }}
.pdf-section + .pdf-section {{ page-break-before: always; }}

/* Image sizing - cap at 75% of column to avoid huge full-bleed renders */
img {{ max-width: 75% !important; height: auto !important; display: block !important; margin: 1em auto !important; }}
figure img {{ max-width: 90% !important; }}
.author-photo, .agent-avatar-inline img {{ display: inline !important; margin: 0 !important; max-width: 28px !important; vertical-align: middle !important; }}

/* Page-break behavior */
.callout {{ page-break-inside: avoid; }}
pre, table, figure {{ page-break-inside: avoid; }}
h1, h2, h3, h4 {{ page-break-after: avoid; break-after: avoid; }}
p {{ orphans: 2; widows: 2; }}

/* Headings */
h1 {{ font-size: 22pt; color: #0d1226; margin: 0.5em 0 0.4em; line-height: 1.2; }}
h2 {{ font-size: 16pt; color: #0d1226; margin: 1.2em 0 0.4em; line-height: 1.25; border-bottom: 1px solid #ddd; padding-bottom: 0.15em; }}
h3 {{ font-size: 13pt; color: #1a1a2e; margin: 1em 0 0.35em; }}
h4 {{ font-size: 11pt; color: #1a1a2e; margin: 0.9em 0 0.3em; }}

/* Code */
pre, code {{ font-family: "Source Code Pro", "Courier New", monospace; }}
pre {{
    background: #f6f6f4 !important;
    border: 1px solid #ccc !important;
    border-left: 3px solid #555 !important;
    padding: 0.6em !important;
    font-size: 8.5pt !important;
    line-height: 1.35 !important;
    overflow-wrap: break-word !important;
    white-space: pre-wrap !important;
}}
code {{ background: #f0f0f0 !important; padding: 0.05em 0.3em !important; font-size: 9pt; }}

/* Callouts: per-type colored left border (background prints OK in PDF) */
.callout {{
    border: 1px solid #444 !important;
    border-left-width: 5px !important;
    padding: 0.7em 0.9em !important;
    margin: 1em 0 !important;
    background: #fafaf6 !important;
    border-radius: 3px !important;
}}
.callout-title {{
    font-family: "Helvetica Neue", Helvetica, Arial, sans-serif !important;
    font-weight: bold !important;
    font-size: 10pt !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
    margin-bottom: 0.4em !important;
    border-bottom: 1px solid currentColor !important;
    padding-bottom: 0.2em !important;
}}
.callout.big-picture {{ background: #eef4fa !important; border-left-color: #2a6dba !important; }}
.callout.big-picture .callout-title {{ color: #1a4078 !important; }}
.callout.key-insight {{ background: #ecf6ee !important; border-left-color: #1f7a3a !important; }}
.callout.key-insight .callout-title {{ color: #134d24 !important; }}
.callout.warning {{ background: #fdeee8 !important; border-left-color: #b3401b !important; }}
.callout.warning .callout-title {{ color: #6e2510 !important; }}
.callout.tip {{ background: #ecf6ef !important; border-left-color: #237549 !important; }}
.callout.tip .callout-title {{ color: #154329 !important; }}
.callout.practical-example {{ background: #f4ecf7 !important; border-left-color: #722f8a !important; }}
.callout.practical-example .callout-title {{ color: #4a1d5a !important; }}
.callout.note {{ background: #f4f4f4 !important; border-left-color: #555 !important; }}
.callout.note .callout-title {{ color: #222 !important; }}
.callout.fun-note {{ background: #fbf3df !important; border-left-color: #b88200 !important; }}
.callout.fun-note .callout-title {{ color: #6e4f00 !important; }}

/* Figure captions */
.diagram-caption, figcaption {{
    font-size: 9pt !important;
    color: #555 !important;
    text-align: center !important;
    font-style: italic !important;
    margin-top: 0.4em !important;
}}
.code-caption {{
    font-size: 9pt !important;
    color: #555 !important;
    text-align: center !important;
    font-style: italic !important;
    margin: 0.3em 0 1em !important;
}}

/* Math: ensure KaTeX rendering looks right at print size */
.katex {{ font-size: 1em !important; }}
.math-block, .katex-display {{ text-align: center !important; margin: 1em 0 !important; page-break-inside: avoid !important; }}

/* PDF cover page */
.pdf-cover {{
    text-align: center;
    padding: 6cm 0 2cm;
    page-break-after: always;
}}
.pdf-cover-tag {{
    font-family: "Helvetica Neue", sans-serif;
    text-transform: uppercase;
    letter-spacing: 0.2em;
    font-size: 0.85em;
    color: #888;
    margin-bottom: 1em;
}}
.pdf-cover-title {{
    font-family: Georgia, serif;
    font-size: 2.4em;
    font-weight: bold;
    margin-bottom: 0.3em;
}}
.pdf-cover-subtitle {{
    font-family: Georgia, serif;
    font-style: italic;
    font-size: 1.2em;
    color: #555;
    margin-bottom: 2em;
}}
.pdf-cover-meta {{
    font-family: "Helvetica Neue", sans-serif;
    font-size: 0.95em;
    color: #444;
    line-height: 1.8;
}}
.pdf-cover-cta {{
    margin-top: 3em;
    padding: 1em 2em;
    background: #f4f4f4;
    border-left: 4px solid #0f3460;
    text-align: left;
    font-size: 0.9em;
}}
</style>
</head>
<body>

<div class="pdf-cover">
    <div class="pdf-cover-tag">Sample Chapter &middot; Free Preview</div>
    <div class="pdf-cover-title">{chapter_title}</div>
    <div class="pdf-cover-subtitle">From <em>Building Conversational AI with LLMs and Agents</em></div>
    <div class="pdf-cover-meta">
        Alexander Apartsin, Ph.D. &amp; Yehudit Aperstein, Ph.D.<br>
        Fifth Edition &middot; 2026<br><br>
        <strong>{len(files)} sections</strong> assembled into this preview.
    </div>
    <div class="pdf-cover-cta">
        <strong>Like what you read?</strong> The full book has 39 chapters and 22 appendices,
        covering everything from PyTorch foundations to production AI agents.
        Available at <strong>llmbook.apartsin.com</strong> and on Amazon.
    </div>
</div>

{chr(10).join(pieces)}

</body>
</html>
"""


def _section_sort_key(stem: str):
    m = re.match(r"section-(\d+)\.(\d+)([a-z]?)$", stem)
    if not m:
        return (999, 999, stem)
    return (int(m.group(1)), int(m.group(2)), m.group(3))


def html_to_pdf_from_extract(html: str, output_pdf: Path, browser: Path, extract_dir: Path) -> int:
    """Render HTML to PDF where the HTML lives at extract_dir/sample.html
    so that relative `EPUB/styles/...` CSS paths resolve.
    """
    output_pdf.parent.mkdir(parents=True, exist_ok=True)
    user_data_dir = tempfile.mkdtemp(prefix="pdf_browser_profile_", dir="E:/temp")
    tmp_html = extract_dir / "sample.html"
    try:
        tmp_html.write_text(html, encoding="utf-8")
        out_str = str(output_pdf).replace("/", "\\")
        url = tmp_html.resolve().as_uri()
        cmd = [
            str(browser),
            "--headless=new",
            "--disable-gpu",
            "--no-sandbox",
            "--no-pdf-header-footer",
            "--run-all-compositor-stages-before-draw",
            "--virtual-time-budget=10000",
            f"--user-data-dir={user_data_dir}",
            f"--print-to-pdf={out_str}",
            url,
        ]
        print(f"  Running: {browser.name} headless --print-to-pdf")
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
        if proc.returncode != 0 and proc.stderr.strip():
            print(f"  STDERR: {proc.stderr[:500]}")
        return proc.returncode
    finally:
        import shutil
        shutil.rmtree(user_data_dir, ignore_errors=True)


def html_to_pdf(html: str, output_pdf: Path, browser: Path, chapter_num: int = 11) -> int:
    """Use Chromium headless --print-to-pdf.

    The temp HTML must live INSIDE the chapter folder so relative image refs
    in the source (../../images/, ../../front-matter/images/agents) resolve.
    But the temp filename must be free of hyphens that confuse Edge's
    file:// URL parsing on Windows. Use a short ASCII filename.
    """
    output_pdf.parent.mkdir(parents=True, exist_ok=True)
    chapter_dir = CHAPTERS[chapter_num]
    tmp_html = PROJECT_ROOT / chapter_dir[0] / chapter_dir[1] / "tmppdf.html"
    # CRITICAL: dedicated --user-data-dir so Edge/Chrome doesn't hand off
    # rendering to an already-running browser. Place on E: drive (some Windows
    # systems have C: tight on space, which makes Edge fail to initialize its
    # profile dir and emit an error-page PDF).
    e_temp = Path("E:/temp")
    e_temp.mkdir(exist_ok=True)
    user_data_dir = tempfile.mkdtemp(prefix="pdf_browser_profile_", dir=str(e_temp))
    try:
        tmp_html.write_text(html, encoding="utf-8")
        out_str = str(output_pdf).replace("/", "\\")
        url = tmp_html.resolve().as_uri()
        cmd = [
            str(browser),
            # CRITICAL: --headless=new is required on modern Edge/Chrome.
            # The legacy --headless mode silently fails to load file:// URLs
            # and emits a 1-page "ERR_FILE_NOT_FOUND" PDF. The new mode (added
            # 2023, default in Chrome 132+) actually loads local files.
            "--headless=new",
            "--disable-gpu",
            "--no-sandbox",
            "--no-pdf-header-footer",
            "--run-all-compositor-stages-before-draw",
            "--virtual-time-budget=10000",
            # 6x9 trade-paperback trim size. Chrome headless ignores CSS
            # @page size, so we set it via CLI flags. Margins in inches.
            "--print-to-pdf-no-header",
            "--paper-width=6.0",
            "--paper-height=9.0",
            f"--user-data-dir={user_data_dir}",
            f"--print-to-pdf={out_str}",
            url,
        ]
        print(f"  Running: {browser.name} headless...")
        print(f"  URL:    {url}")
        print(f"  Output: {out_str}")
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
        print(f"  Exit code: {proc.returncode}")
        if proc.stderr.strip():
            print(f"  STDERR (first 500): {proc.stderr[:500]}")
        # Verify the PDF actually contains the chapter, not Edge's error page.
        # A "File not found" PDF is ~60 KB with 1 page; a real chapter PDF is
        # 500 KB+ with 20+ pages. Check size as a fast sanity check.
        if output_pdf.exists():
            size = output_pdf.stat().st_size
            if size < 200_000:
                print(f"  WARN: PDF is {size} bytes - suspiciously small (possible browser error page)")
        # CRITICAL: do NOT delete tmp_html in a `finally:`. Edge/Chrome's
        # main process exits immediately while helper processes continue
        # rendering. Deleting too soon = Edge logs ERR_FILE_NOT_FOUND and
        # writes a 60 KB error-page PDF. Let the temp file persist between
        # runs (each build overwrites). Add tmppdf.html to .gitignore to
        # keep it out of the repo.
        return proc.returncode
    finally:
        # Clean up the dedicated browser profile dir (it's huge - ~50 MB)
        import shutil
        shutil.rmtree(user_data_dir, ignore_errors=True)


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[1])
    p.add_argument("--chapter", type=int, default=12,
                   help="Chapter number to convert (default 11 = prompt engineering)")
    p.add_argument("--slug", default="prompt-engineering",
                   help="Filename slug for output PDF (default prompt-engineering)")
    args = p.parse_args()

    browser = find_browser()
    if browser is None:
        print("ERROR: No Chromium-family browser found (Edge or Chrome).", file=sys.stderr)
        return 3
    print(f"Browser: {browser}")

    print(f"\nAssembling chapter {args.chapter} from EPUB chapter XHTML (with Pygments + KaTeX)...")
    html, extract_dir = assemble_chapter_html_from_epub(args.chapter)
    print(f"  Length: {len(html):,} chars")

    output_pdf = DOWNLOADS_DIR / f"sample-chapter-{args.slug}.pdf"
    print(f"\nConverting to PDF -> {output_pdf.relative_to(PROJECT_ROOT)}")
    rc = html_to_pdf_from_extract(html, output_pdf, browser, extract_dir)
    if rc != 0:
        print(f"  Browser exited with code {rc}", file=sys.stderr)
        return rc
    if output_pdf.exists():
        size = output_pdf.stat().st_size
        print(f"  [OK] Wrote {output_pdf.name} ({size / 1024:.1f} KB)")
        return 0
    else:
        print(f"  [FAIL] PDF was not created")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
