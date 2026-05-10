"""Extract representative EPUB chapters, render each to PDF via Edge, then
to PNG images for visual quality inspection.

Outputs:
  E:/temp/epub_samples/{chapter}.png  (page 1 of each chapter, 1200 px wide)
  E:/temp/epub_samples/inspection_index.md  (manifest)

Usage:
  python KDP/build/render_epub_samples.py [--chapters 5]
"""
from __future__ import annotations
import argparse
import os
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
OUT_DIR = Path("E:/temp/epub_samples")
EDGE = Path("C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe")

# Representative chapters to render (mix of front matter, foundations,
# practical, agent, production, appendix - so we see different content types).
SAMPLE_TARGETS = [
    "front-matter-foreword",
    "front-matter-look-inside-preview",
    "part-1-foundations-module-04-transformer-architecture-section-4-1",  # math+code
    "part-1-foundations-module-04-transformer-architecture-section-4-3",  # math+diagrams
    "part-3-working-with-llms-module-11-prompt-engineering-section-11-1",  # callouts
    "part-5-retrieval-conversation-module-20-rag-section-20-3",  # diagrams + tables
    "part-6-agentic-ai-module-22-ai-agents-section-22-3",  # code-heavy
    "part-8-evaluation-production-module-29-evaluation-observability-section-29-1",  # tables
]


def extract_epub(target_dir: Path) -> dict[str, Path]:
    """Unzip EPUB to target_dir; return mapping of stem -> path for chapter XHTMLs."""
    target_dir.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(EPUB_PATH) as zf:
        zf.extractall(target_dir)
    chapters_dir = target_dir / "EPUB" / "chapters"
    chapters: dict[str, Path] = {}
    for f in chapters_dir.glob("*.xhtml"):
        # ch_NNNN_<slug>.xhtml -> map by slug
        parts = f.stem.split("_", 2)
        if len(parts) >= 3:
            chapters[parts[2]] = f
    return chapters


def render_to_pdf(html: Path, output_pdf: Path) -> bool:
    output_pdf.parent.mkdir(parents=True, exist_ok=True)
    user_data_dir = tempfile.mkdtemp(prefix="epub_render_", dir="E:/temp")
    try:
        cmd = [
            str(EDGE),
            "--headless=new",
            "--disable-gpu",
            "--no-sandbox",
            "--no-pdf-header-footer",
            "--run-all-compositor-stages-before-draw",
            "--virtual-time-budget=10000",
            f"--user-data-dir={user_data_dir}",
            f"--print-to-pdf={str(output_pdf).replace('/', chr(92))}",
            html.resolve().as_uri(),
        ]
        subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        return output_pdf.exists() and output_pdf.stat().st_size > 1000
    finally:
        shutil.rmtree(user_data_dir, ignore_errors=True)


def pdf_pages_to_pngs(pdf: Path, out_dir: Path, prefix: str, max_pages: int = 3) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    pngs = []
    doc = fitz.open(str(pdf))
    n = min(len(doc), max_pages)
    for i in range(n):
        page = doc.load_page(i)
        # Render at 1.5x for readability
        mat = fitz.Matrix(1.5, 1.5)
        pix = page.get_pixmap(matrix=mat, alpha=False)
        out_path = out_dir / f"{prefix}_p{i+1}.png"
        pix.save(str(out_path))
        pngs.append(out_path)
    doc.close()
    return pngs


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--max-pages", type=int, default=2,
                   help="Max pages per chapter to render (default 2)")
    p.add_argument("--random", type=int, default=0,
                   help="Random sample N chapters from EPUB (instead of fixed list)")
    p.add_argument("--seed", type=int, default=None,
                   help="Random seed (for reproducible sampling)")
    args = p.parse_args()

    if OUT_DIR.exists():
        shutil.rmtree(OUT_DIR, ignore_errors=True)
    OUT_DIR.mkdir(parents=True)

    print(f"Extracting EPUB to temp dir...")
    extract_dir = OUT_DIR / "_extracted"
    chapters = extract_epub(extract_dir)
    print(f"  Found {len(chapters)} chapter XHTMLs in EPUB")

    matched = []
    if args.random > 0:
        import random
        if args.seed is not None:
            random.seed(args.seed)
        # Filter: skip front-matter index pages and very small pages
        candidates = [(s, p) for s, p in chapters.items()
                      if not s.endswith("-index") and "section-" in s]
        sample = random.sample(candidates, min(args.random, len(candidates)))
        matched = sample
        print(f"  Random-sampled {len(sample)} chapters (seed={args.seed})")
    else:
        for target in SAMPLE_TARGETS:
            for slug, path in chapters.items():
                if slug == target or slug.startswith(target):
                    matched.append((target, path))
                    break
            else:
                print(f"  [skip] no match for {target}")

    print(f"\nRendering {len(matched)} chapters via Edge headless...")
    manifest = []
    for short_name, html_path in matched:
        print(f"  > {short_name}")
        pdf_path = OUT_DIR / f"{short_name}.pdf"
        if not render_to_pdf(html_path, pdf_path):
            print(f"    [FAIL] PDF not created")
            continue
        pngs = pdf_pages_to_pngs(pdf_path, OUT_DIR, short_name, max_pages=args.max_pages)
        print(f"    -> {len(pngs)} png(s), pdf={pdf_path.stat().st_size/1024:.0f} KB")
        manifest.append((short_name, pdf_path, pngs))

    # Write inspection index
    md = ["# EPUB Sample Pages — Visual Inspection\n",
          f"_Generated {time.strftime('%Y-%m-%d %H:%M:%S')}_\n",
          f"_EPUB source: {EPUB_PATH.relative_to(PROJECT_ROOT)} ({EPUB_PATH.stat().st_size/1024/1024:.2f} MB)_\n\n"]
    for short_name, pdf, pngs in manifest:
        md.append(f"## {short_name}\n")
        md.append(f"PDF: `{pdf.name}` ({pdf.stat().st_size/1024:.0f} KB)\n")
        for png in pngs:
            md.append(f"- ![](./{png.name})\n")
        md.append("\n")
    (OUT_DIR / "inspection_index.md").write_text("".join(md), encoding="utf-8")
    print(f"\n[OK] Samples in {OUT_DIR}")
    print(f"     Manifest: {OUT_DIR}/inspection_index.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
