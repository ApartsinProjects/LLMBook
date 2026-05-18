"""Migration step 2: rewrite book-wide cross-references to Parts whose
numbers / titles / hrefs changed in Step 1.

Three patterns to rewrite:

1. **Text references**: "Part X" / "Part XI" / "Part XII" in body text where
   the surrounding context refers to one of the renamed parts. We rewrite
   ALL three at once with temp tokens to avoid the 3-way swap collision:

       Part X      -> Part TMPX
       Part XI     -> Part TMPXI
       Part XII    -> Part TMPXII
       Part TMPX   -> Part XII   (was Frontiers)
       Part TMPXI  -> Part X     (was Idea to Product)
       Part TMPXII -> Part XI    (was Applications)

2. **Title text changes** (Parts VII and IX kept their roman numeral):

       "Part VII: AI Applications" -> "Part VII: Multimodal Generation"
       "Part VII: Multimodal Applications" -> "Part VII: Multimodal Generation"
       "Part IX: Safety and Strategy" -> "Part IX: Safety, Security & Ethics"

3. **Href paths**: any link that pointed at the old part dir should point at
   the new one:

       href=".../part-7-multimodal-applications/..." -> "part-7-multimodal-generation/"
       href=".../part-9-safety-strategy/..." -> "part-9-safety-security-ethics/"
       href=".../part-10-frontiers/..." -> "part-12-frontiers/"
       href=".../part-11-idea-to-product/..." -> "part-10-idea-to-product/"
       href=".../part-12-llm-applications-across-industries/..." -> "part-11-applications-across-industries/"

Skip the renamed part directories themselves (their internal references were
fixed in Step 1).

Idempotent.
"""
from __future__ import annotations
import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP_PARTS = {"node_modules", ".git", "KDP", "build", "temp_ebook",
              "temp_epub", "source_fix_backups", "pagefind", "templates",
              ".claude"}

# Path renames (always apply; safe regardless of context)
PATH_RENAMES = [
    ("part-7-multimodal-applications", "part-7-multimodal-generation"),
    ("part-9-safety-strategy", "part-9-safety-security-ethics"),
    ("part-10-frontiers", "part-12-frontiers"),
    ("part-11-idea-to-product", "part-10-idea-to-product"),
    ("part-12-llm-applications-across-industries",
        "part-11-applications-across-industries"),
]

# Title renames (apply to body text)
TITLE_RENAMES = [
    # Parts 7 + 9 kept their roman numeral; titles change.
    ("Part VII: AI Applications", "Part VII: Multimodal Generation"),
    ("Part VII: Multimodal Applications", "Part VII: Multimodal Generation"),
    ("Part IX: Safety and Strategy", "Part IX: Safety, Security & Ethics"),
    # 10/11/12 ordering swap is handled by ROMAN_REWRITES below.
]

# Roman-numeral text refs with 3-way swap (use temp tokens)
ROMAN_REWRITES = [
    # Step 1: introduce temp tokens
    (r"\bPart\s+X\b(?![IVXLCDM])", "Part TMPX"),
    (r"\bPart\s+XI\b(?!I)", "Part TMPXI"),
    (r"\bPart\s+XII\b", "Part TMPXII"),
    # Step 2: temp -> final
    (r"\bPart\s+TMPX\b(?![IVXLCDM])", "Part XII"),   # Frontiers
    (r"\bPart\s+TMPXI\b(?!I)", "Part X"),            # Idea to Product
    (r"\bPart\s+TMPXII\b", "Part XI"),               # Applications
]


def rewrite_file(p: Path, dry_run: bool) -> tuple[int, str]:
    """Return (n_changes, sample_diff_or_empty)."""
    text = p.read_text(encoding="utf-8")
    orig = text

    # Skip files INSIDE the renamed parts (internal metadata already fixed)
    rel_parts = set(p.relative_to(ROOT).parts)
    if any(part_slug in rel_parts for _, part_slug in PATH_RENAMES):
        # We still want to fix paths to OTHER parts from these files,
        # so don't skip outright; but skip the roman-numeral rewrites since
        # those are pre-fixed by step1 for in-part refs.
        skip_roman = True
    else:
        skip_roman = False

    # 1) Path renames (always safe)
    for old_slug, new_slug in PATH_RENAMES:
        text = text.replace(f"{old_slug}/", f"{new_slug}/")
        # Also handle href without trailing slash (defensive)
        text = re.sub(rf"\b{re.escape(old_slug)}\b(?![-/])",
                       new_slug, text)

    # 2) Title renames
    for old_t, new_t in TITLE_RENAMES:
        text = text.replace(old_t, new_t)

    # 3) Roman-numeral 3-way swap
    if not skip_roman:
        for pat, repl in ROMAN_REWRITES:
            text = re.sub(pat, repl, text)

    n = sum(1 for _ in re.finditer(r"part-", orig)) - sum(1 for _ in re.finditer(r"part-", text))
    n = abs(n)
    if text == orig:
        return 0, ""
    if not dry_run:
        p.write_text(text, encoding="utf-8")
    return 1, ""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    dry_run = not args.apply

    total_files = 0
    for p in sorted(ROOT.rglob("*.html")):
        if set(p.parts) & SKIP_PARTS:
            continue
        n, _ = rewrite_file(p, dry_run)
        if n:
            total_files += 1
    # Also touch toc.html, appendices/index.html, sitemap-like files at root
    for special in ("toc.html",):
        sp = ROOT / special
        if sp.exists():
            rewrite_file(sp, dry_run)

    mode = "DRY-RUN" if dry_run else "APPLY"
    print(f"{mode}: rewrote part-refs in {total_files} HTML files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
