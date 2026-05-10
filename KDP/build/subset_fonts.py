"""
Subset Source Serif 4 + Source Code Pro fonts for embedding in the EPUB.

Why subset:
  Full Source Serif 4 Regular OTF = 360 KB. After subsetting to only the
  characters actually used in the book (basic Latin + a few math symbols),
  the WOFF2 output is typically 30-50 KB. Same for Source Code Pro.

  Embedding 4 unsubsetted fonts adds 1.4 MB to the EPUB. Subsetted
  WOFF2 versions add ~150-250 KB total.

Inputs:
  - Source HTML at PROJECT_ROOT/{front-matter,part-*,appendices,capstone}/
    used to determine which characters are referenced
  - Font OTFs at E:/Tools/fonts/source-serif/.../OTF/
                E:/Tools/fonts/source-code/OTF/

Outputs:
  KDP/build/fonts/SourceSerif4-Regular.woff2
  KDP/build/fonts/SourceSerif4-It.woff2
  KDP/build/fonts/SourceSerif4-Bold.woff2
  KDP/build/fonts/SourceCodePro-Regular.woff2

The build_epub.py script picks up everything in KDP/build/fonts/ and
bundles into the EPUB at fonts/<name>.woff2 with corresponding
@font-face rules in the CSS.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
BUILD_DIR = PROJECT_ROOT / "KDP" / "build"
OUT_DIR = BUILD_DIR / "fonts"
FONT_SOURCE_DIR = Path("E:/Tools/fonts")

# Map output name -> source OTF path (relative to FONT_SOURCE_DIR)
FONT_MAPPING = {
    "SourceSerif4-Regular":  "source-serif/source-serif-4.005_Desktop/OTF/SourceSerif4-Regular.otf",
    "SourceSerif4-It":       "source-serif/source-serif-4.005_Desktop/OTF/SourceSerif4-It.otf",
    "SourceSerif4-Bold":     "source-serif/source-serif-4.005_Desktop/OTF/SourceSerif4-Bold.otf",
    "SourceCodePro-Regular": "source-code/OTF/SourceCodePro-Regular.otf",
}


def collect_text() -> str:
    """Concatenate the visible text from all source HTML files."""
    text_parts: list[str] = []
    for d in ("front-matter", "capstone", "appendices"):
        for p in (PROJECT_ROOT / d).rglob("*.html"):
            text_parts.append(p.read_text(encoding="utf-8", errors="replace"))
    for d in PROJECT_ROOT.glob("part-*"):
        for p in d.rglob("*.html"):
            text_parts.append(p.read_text(encoding="utf-8", errors="replace"))
    return "\n".join(text_parts)


def extract_codepoints(text: str) -> set[str]:
    """Strip HTML entities to characters and HTML tags, then collect uniques."""
    # Decode common entities into chars
    from html import unescape
    decoded = unescape(text)
    # Strip HTML tags
    no_tags = re.sub(r"<[^>]+>", "", decoded)
    return set(no_tags)


def subset_one(name: str, src_otf: Path, used_chars: set[str]) -> int:
    """Run pyftsubset on one font; return output file size in bytes."""
    out_path = OUT_DIR / f"{name}.woff2"
    # Build the subset spec: a string of characters to include
    # plus extra basic Latin / typography / common math / arrows
    extras = (
        " !\"#$%&'()*+,-./0123456789:;<=>?@"
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`"
        "abcdefghijklmnopqrstuvwxyz{|}~"
        " "  # non-breaking space
        "¡¢£¤¥¦§¨©ª«¬®¯"
        "°±²³´µ¶·¸¹º»"
        "¼½¾¿"
        # Smart quotes, dashes, ellipsis
        "‐‑‒–—―"
        "‘’‚‛“”„"
        "†‡•…"
        # Greek (math notation in this book)
        "αβγδεζηθικλμνξοπρστυφχψω"
        "ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ"
        # Math symbols
        "∀∂∃∅∇∈∉∋∏∑−∕√∞"
        "∧∨∩∪∴∵∶∷≃≈≠≡≤≥"
        "→←↑↓⇒⇔"
        # Other useful
        "×÷"  # multiplication / division
    )
    chars = used_chars | set(extras)
    text_arg = "".join(sorted(c for c in chars if c.isprintable() or c == " "))

    # pyftsubset CLI
    cmd = [
        sys.executable, "-m", "fontTools.subset",
        str(src_otf),
        f"--text={text_arg}",
        f"--output-file={out_path}",
        "--flavor=woff2",
        "--with-zopfli",
        "--layout-features=kern,liga,frac,sups,subs,onum",
        "--no-hinting",
        "--desubroutinize",
    ]
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        print(f"  ERROR subsetting {name}:", proc.stderr.strip()[:300])
        return 0
    return out_path.stat().st_size


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    p.add_argument("--clean", action="store_true", help="Wipe KDP/build/fonts/ before subsetting")
    args = p.parse_args()

    if args.clean and OUT_DIR.exists():
        for f in OUT_DIR.glob("*.woff2"):
            f.unlink()

    # Verify pyftsubset is installed
    try:
        import fontTools  # noqa: F401
    except ImportError:
        print("ERROR: fontTools not installed. Run: pip install fonttools brotli")
        return 3

    print("Collecting text from source HTML...")
    text = collect_text()
    print(f"  Total text size: {len(text):,} chars")
    used = extract_codepoints(text)
    print(f"  Unique codepoints: {len(used)}")

    print(f"\nSubsetting fonts to {OUT_DIR.relative_to(PROJECT_ROOT)}/")
    total_in = 0
    total_out = 0
    for name, rel_src in FONT_MAPPING.items():
        src = FONT_SOURCE_DIR / rel_src
        if not src.exists():
            print(f"  [skip] missing source: {src}")
            continue
        in_size = src.stat().st_size
        total_in += in_size
        out_size = subset_one(name, src, used)
        if out_size:
            total_out += out_size
            ratio = out_size / in_size * 100
            print(f"  {name:30s}  {in_size/1024:>6.1f} KB -> {out_size/1024:>6.1f} KB  ({ratio:.1f}%)")
        else:
            print(f"  {name:30s}  FAILED")

    print(f"\nTotal: {total_in/1024:.1f} KB -> {total_out/1024:.1f} KB"
          f" ({total_out/total_in*100:.1f}% of original)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
