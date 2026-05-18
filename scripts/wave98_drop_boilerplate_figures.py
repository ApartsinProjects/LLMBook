"""Wave 98: Drop all 93 Gemini boilerplate "three-panel overview" figures.

Reason for dropping (not fixing the captions):
  - All 93 were generated from the same template: "three labeled panels:
    (1) starting state, (2) key mechanism, (3) outcome or trade-off."
  - The prompt only passes the section TITLE, not section content.
  - The images have garbled labels (e.g. "BENCHBARKS", "EFICACY",
    "Tranermerrx", "Retriever-Augmented-Generation"). Gemini 2.5 Flash
    Image cannot render technical labels cleanly.
  - The captions are identical boilerplate that just describes the
    template, not the figure.
  - Many figures depict concepts that are NOT in the section's prose
    (e.g. section 42.8 figure shows "RAG" and "Transformers-XL", but
    the prose covers YaRN, NTK-aware, position interpolation).
  - Result: decorative noise that looks authoritative but adds nothing
    over the prose, and in some cases actively misleads.

What this script removes:
  - The "<!-- TODO: imagegen placeholder; ... -->" comment immediately
    before the figure.
  - The "<figure class="illustration">...</figure>" block whose alt
    text matches the "three-panel flat diagram" boilerplate.
  - The orphan "<!-- ===... ===-->" separator that sometimes precedes
    the TODO comment.

What it does NOT touch:
  - Non-Gemini figures (real diagrams, SVGs, charts, etc.)
  - Figures whose caption is hand-written and section-specific.

Run from the LLMBook root: it walks all section-*.html files.
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
SKIP = {".git", "node_modules", "KDP", "build", "source_fix_backups",
        "pagefind", ".book-update", "vendor", ".claude", "_archive",
        "agents", "templates", "docs", "scripts"}

# Match the boilerplate figure block. Strategy:
#   - Optional separator "<!-- ===...=== -->"
#   - The "<!-- TODO: imagegen placeholder ... -->" comment
#   - The <figure class="illustration"> ... </figure> block
# We match the figure block specifically when its alt text begins with
# "Three-panel flat diagram illustrating" — the signature of the batch.
BLOCK_RE = re.compile(
    r'(?:[ \t]*<!--\s*={3,}\s*-->\s*\n)?'      # optional separator
    r'[ \t]*<!--\s*TODO:\s*imagegen placeholder[^>]*-->\s*\n'
    r'[ \t]*<figure\s+class="illustration">\s*\n'
    r'[ \t]*<img\s+alt="Three-panel flat diagram illustrating[^"]*"'
    r'[^>]*data-imagegen-status="generated"[^>]*/>\s*\n'
    r'[ \t]*<figcaption><strong>Figure[^<]*</strong>:[^<]*</figcaption>\s*\n'
    r'[ \t]*</figure>\s*\n',
    re.IGNORECASE
)


def fix_file(p: Path) -> int:
    text = p.read_text(encoding="utf-8")
    new_text, n = BLOCK_RE.subn("", text)
    if n == 0:
        return 0
    p.write_text(new_text, encoding="utf-8")
    return n


def main():
    n_files = 0
    n_total = 0
    for p in sorted(ROOT.rglob("*.html")):
        if set(p.parts) & SKIP:
            continue
        n = fix_file(p)
        if n:
            n_files += 1
            n_total += n
            print(f"  - {p.relative_to(ROOT)}: dropped {n} boilerplate figure(s)")
    print(f"\nFiles touched: {n_files}, figures dropped: {n_total}")


if __name__ == "__main__":
    main()
