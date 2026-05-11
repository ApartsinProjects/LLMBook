"""v3.7 R6-B: Unwrap in-prose `<a>Section X.Y</a>` links that originally
displayed a domain term.

Damage origin: the v3.4 nav-fix script's "label-vs-href" pass and v3.6
anchor-catastrophe undo BOTH replace anchor display text with `Section X.Y`
when the original was a domain noun. Reader sees nonsense like:
  "during Section 6.1"   (was "during pretraining")
  "multilingual Section 6.1"   (was "multilingual training")
  "The Section 22.1 sends..."   (was "The agent sends")

Cannot recover the original noun. Two options:
  (a) Unwrap the anchor entirely (keep "Section 6.1" but as plain text)
  (b) Replace anchor display text with the linked section's H1 title

Both lose information. (b) at least gives semantic content; (a) is safer.

Strategy: option (a) for clearly-broken cases (anchor inside running
prose where the displayed text is just "Section X.Y" - those reader-facing
"during Section 6.1" patterns). Leave anchors where the displayed text
is intentional (e.g., "see Section 6.1" sentences).

Heuristic for "clearly broken": the anchor sits in the middle of a
sentence, NOT preceded by "see ", "in ", "from ", "of ", etc. (those are
intentional "see Section X.Y" usages).
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
EXCLUDE = {"_archive", "KDP", "node_modules", "vendor", "scripts"}

# Match `<a ...>Section X.Y</a>` where displayed text is exactly "Section X.Y"
ANCHOR = re.compile(
    r'<a\s+[^>]*href="[^"]*section-(\d+\.\d+)\.html(?:#[^"]*)?"[^>]*>'
    r'Section\s+(\d+\.\d+)'
    r'</a>'
)

# Words that, when preceding the anchor, indicate INTENTIONAL "see Section X.Y" usage
INTENTIONAL_PRECEDING = re.compile(
    r'(?:see|in|from|to|of|chapter|cf\.|cf|under|via|covered\s+in|'
    r'discussed\s+in|introduced\s+in|presented\s+in|detailed\s+in|'
    r'explained\s+in|described\s+in|defined\s+in|including)\s+$',
    re.IGNORECASE,
)


def is_intentional(text: str, anchor_start: int) -> bool:
    """Look back ~30 chars to see if a 'see/in/from' word precedes."""
    chunk = text[max(0, anchor_start - 40):anchor_start]
    chunk = re.sub(r'<[^>]+>', '', chunk)  # strip surrounding tags
    return bool(INTENTIONAL_PRECEDING.search(chunk))


def is_in_chrome(text: str, anchor_start: int) -> bool:
    """True if anchor lives inside legitimate chrome (TOC, nav, headings)."""
    chunk = text[max(0, anchor_start - 600):anchor_start]
    for marker in [r"<h[1-6]\b",
                   r'class="[^"]*(?:toc|chapter-nav|whats-next|crumb|nav-footer|sidebar|chapter-card-title|module-card-title|prev|next|section-card)[^"]*"']:
        opens = list(re.finditer(marker, chunk))
        if opens and not re.search(r"</(?:h[1-6]|nav|aside|li|a)>", chunk[opens[-1].start():]):
            return True
    return False


def main() -> int:
    n_files = 0
    n_unwrapped = 0
    n_kept_intentional = 0
    n_kept_chrome = 0

    for p in ROOT.rglob("*.html"):
        if any(part in p.parts for part in EXCLUDE):
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        original = text

        # Iterate in reverse so positional offsets stay valid
        matches = list(ANCHOR.finditer(text))
        for m in reversed(matches):
            href_num = m.group(1)
            label_num = m.group(2)
            if is_in_chrome(text, m.start()):
                n_kept_chrome += 1
                continue
            if is_intentional(text, m.start()):
                n_kept_intentional += 1
                continue
            # Unwrap to plain "Section X.Y" text (keep the section number
            # as a hint, drop the link)
            text = text[:m.start()] + f"Section {href_num}" + text[m.end():]
            n_unwrapped += 1

        if text != original:
            p.write_text(text, encoding="utf-8")
            n_files += 1

    print(f"Unwrapped {n_unwrapped} in-prose 'Section X.Y' anchors across {n_files} files")
    print(f"Kept {n_kept_intentional} intentional 'see Section X.Y' uses")
    print(f"Kept {n_kept_chrome} chrome anchors (TOC/nav/cards)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
