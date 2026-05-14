"""v792: Audit 20 random EPUB pages rendered in two-page landscape
tablet layout. Each chapter is rendered with CSS column-count:2 +
landscape viewport (matching Kindle Fire / iPad landscape).

Outputs:
  E:/temp/epub_audit_v792/<n>_<slug>_landscape.png   - PNG of page 1
  E:/temp/epub_audit_v792/<n>_<slug>_landscape.pdf   - paginated PDF
  E:/temp/epub_audit_v792/audit_index.md             - manifest

Process:
  1. Extract EPUB
  2. Randomly sample 20 section XHTML files (excluding indexes)
  3. For each: copy XHTML + inline an extra <style> block forcing
     CSS column-count: 2, column-gap: 2em, column-fill: balance.
     Page size: 11in x 8.5in landscape (mimics Kindle Fire landscape).
  4. Render with Edge headless to PDF
  5. Extract first page as PNG (1.5x scale = ~1650 px wide)

Why this is a faithful audit:
  - Kindle landscape tablet view DOES paginate into two columns
  - It uses the same CSS we ship in epub_overrides.css
  - Two-page landscape is where the v786..v790 fixes were targeted
    (tables splitting, callouts not stretching, math alignment)
  - Random sample of 20 covers diverse content types: math, tables,
    callouts, code, headings, lists
"""
from __future__ import annotations
import argparse
import os
import random
import shutil
import subprocess
import sys
import tempfile
import time
import zipfile
from pathlib import Path

try:
    import fitz  # PyMuPDF
except ImportError:
    print("Install pymupdf: pip install pymupdf", file=sys.stderr)
    sys.exit(2)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
EPUB_PATH = PROJECT_ROOT / "KDP/output/building-conversational-ai-llms-agents.epub"
OUT_DIR = Path("E:/temp/epub_audit_v792")
EDGE = Path("C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe")

# CSS injection to force two-column landscape tablet rendering.
# Mimics what the Kindle reader does in landscape on a Kindle Fire.
LANDSCAPE_INJECT = """
<style id="audit-v792-landscape">
@page {
    size: 11in 8.5in;     /* landscape letter */
    margin: 0.5in 0.6in;
}
html, body {
    column-count: 2 !important;
    column-gap: 2em !important;
    column-fill: auto !important;
    max-width: none !important;
    width: 100% !important;
    font-size: 14px !important;  /* approximate Kindle landscape default */
}
/* Show a column divider to visualize page boundary */
body {
    column-rule: 1px dashed #c0c0c0 !important;
}
main.content {
    max-width: none !important;
    width: 100% !important;
    padding: 0 !important;
    margin: 0 !important;
}
/* Pin header to top of first column so multi-page chapters retain it */
.chapter-header {
    column-span: all !important;
}
</style>
"""


def extract_epub(target_dir: Path) -> tuple[Path, list[Path]]:
    """Unzip EPUB; return (root_path, list of chapter XHTML files)."""
    target_dir.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(EPUB_PATH) as zf:
        zf.extractall(target_dir)
    chapters_dir = target_dir / "EPUB" / "chapters"
    chapters = sorted(chapters_dir.glob("*.xhtml"))
    return target_dir / "EPUB", chapters


def inject_landscape_css(html_path: Path) -> Path:
    """Read XHTML, inject our landscape CSS before </head>, save .audit.xhtml next to it."""
    s = html_path.read_text(encoding="utf-8")
    if "</head>" in s:
        s = s.replace("</head>", LANDSCAPE_INJECT + "</head>", 1)
    else:
        s = LANDSCAPE_INJECT + s
    out = html_path.with_suffix(".audit.xhtml")
    out.write_text(s, encoding="utf-8")
    return out


def render_to_pdf(html: Path, output_pdf: Path) -> bool:
    output_pdf.parent.mkdir(parents=True, exist_ok=True)
    user_data_dir = tempfile.mkdtemp(prefix="audit_render_", dir="E:/temp")
    try:
        cmd = [
            str(EDGE),
            "--headless=new",
            "--disable-gpu",
            "--no-sandbox",
            "--no-pdf-header-footer",
            "--run-all-compositor-stages-before-draw",
            "--virtual-time-budget=15000",
            f"--user-data-dir={user_data_dir}",
            f"--print-to-pdf={str(output_pdf).replace('/', chr(92))}",
            html.resolve().as_uri(),
        ]
        subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        return output_pdf.exists() and output_pdf.stat().st_size > 1000
    finally:
        shutil.rmtree(user_data_dir, ignore_errors=True)


def pdf_first_page_to_png(pdf: Path, out_path: Path, max_pages: int = 2) -> int:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(str(pdf))
    n = min(len(doc), max_pages)
    for i in range(n):
        page = doc.load_page(i)
        mat = fitz.Matrix(1.5, 1.5)
        pix = page.get_pixmap(matrix=mat, alpha=False)
        if n == 1:
            pix.save(str(out_path))
        else:
            stem = out_path.stem
            pix.save(str(out_path.parent / f"{stem}_p{i+1}.png"))
    doc.close()
    return n


def slug_from_chapter(p: Path) -> str:
    parts = p.stem.split("_", 2)
    return parts[2] if len(parts) >= 3 else p.stem


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=20, help="Number of pages to sample (default 20)")
    parser.add_argument("--seed", type=int, default=42, help="Random seed (default 42)")
    args = parser.parse_args()

    if OUT_DIR.exists():
        shutil.rmtree(OUT_DIR, ignore_errors=True)
    OUT_DIR.mkdir(parents=True)

    print(f"[1/4] Extracting EPUB to {OUT_DIR}/_extracted")
    extract_root, chapters = extract_epub(OUT_DIR / "_extracted")
    # Filter: only true content sections (skip indexes, copyright, TOC, etc.)
    section_chapters = [c for c in chapters
                        if "section" in c.stem.lower()
                        and "index" not in c.stem.lower()]
    print(f"      {len(section_chapters)} candidate section files")

    random.seed(args.seed)
    sample = random.sample(section_chapters, min(args.count, len(section_chapters)))
    sample.sort(key=lambda p: p.name)  # sort for stable index in manifest

    print(f"\n[2/4] Rendering {len(sample)} pages in landscape tablet layout (seed={args.seed})")
    manifest = []
    for i, ch in enumerate(sample, 1):
        slug = slug_from_chapter(ch)[:60]
        print(f"  [{i:>2}/{len(sample)}] {slug}")
        # Inject CSS, render to PDF, convert first 2 pages to PNG
        audit_html = inject_landscape_css(ch)
        pdf_path = OUT_DIR / f"{i:02d}_{slug}.pdf"
        if not render_to_pdf(audit_html, pdf_path):
            print(f"      [FAIL] PDF not created")
            continue
        png_path = OUT_DIR / f"{i:02d}_{slug}.png"
        n_pages = pdf_first_page_to_png(pdf_path, png_path, max_pages=2)
        manifest.append((i, slug, ch.name, pdf_path, png_path, n_pages))

    print(f"\n[3/4] Writing manifest")
    md = ["# EPUB Landscape Audit (v792)\n\n",
          f"_Generated {time.strftime('%Y-%m-%d %H:%M:%S')}_\n",
          f"_EPUB: {EPUB_PATH.relative_to(PROJECT_ROOT)} ({EPUB_PATH.stat().st_size/1024/1024:.2f} MB)_\n",
          f"_Sample: {args.count} random sections, seed={args.seed}_\n\n",
          "## Pages\n\n"]
    for i, slug, fn, pdf, png, n in manifest:
        md.append(f"### {i}. {slug}\n")
        md.append(f"- Source: `{fn}`\n")
        md.append(f"- PDF: `{pdf.name}` ({pdf.stat().st_size/1024:.0f} KB, {n} pages)\n")
        if n == 1:
            md.append(f"- ![](./{png.name})\n\n")
        else:
            stem = png.stem
            for p in range(1, n+1):
                md.append(f"- ![](./{stem}_p{p}.png)\n")
            md.append("\n")
    (OUT_DIR / "audit_index.md").write_text("".join(md), encoding="utf-8")

    print(f"\n[4/4] Done")
    print(f"  Output: {OUT_DIR}")
    print(f"  Manifest: {OUT_DIR}/audit_index.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
