"""v3.4 #4: Wrap each <section class="bibliography"> in <details>.

Web behavior: collapsible by browser native; reader clicks "References"
to expand. Cleaner reading flow without lost content.

EPUB behavior: Kindle CSS sanitizer auto-converts <details>/<summary>
to a static <div class="details-shim">/<p class="details-title">. So
EPUB readers see a labelled, indented box - same content, no
collapsibility but visually delineated.

Idempotent: skips bib sections already wrapped in <details>.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
EXCLUDE = {"_archive", "KDP", "node_modules", "vendor", "scripts"}

# Match <section class="bibliography">...</section> not already inside details
BIB_RE = re.compile(
    r'(?<!<details[^>]>)\s*(<section\s+class="bibliography">.*?</section>)',
    re.DOTALL,
)


def wrap_bib(match: re.Match) -> str:
    inner = match.group(1)
    # Extract the <h2 class="bibliography-title">Bibliography</h2> if present
    title_match = re.search(
        r'<h2[^>]*class="bibliography-title"[^>]*>(.*?)</h2>',
        inner,
        re.DOTALL,
    )
    summary_text = "References"
    if title_match:
        # Use the existing title text (may be "Bibliography", "References", etc.)
        title_inner = re.sub(r"<[^>]+>", "", title_match.group(1)).strip()
        if title_inner:
            summary_text = title_inner
        # Remove the original h2 since summary takes its place
        inner = inner[:title_match.start()] + inner[title_match.end():]
    return (
        f'<details class="bibliography-collapsible" open>\n'
        f'<summary><strong>{summary_text}</strong></summary>\n'
        f'{inner}\n'
        f'</details>'
    )


def main() -> int:
    n_files = 0
    n_wrapped = 0
    for p in ROOT.rglob("*.html"):
        if any(part in p.parts for part in EXCLUDE):
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        if 'class="bibliography"' not in text:
            continue
        # Skip if already wrapped
        if 'class="bibliography-collapsible"' in text:
            continue
        new_text, count = BIB_RE.subn(wrap_bib, text)
        if count > 0 and new_text != text:
            p.write_text(new_text, encoding="utf-8")
            n_files += 1
            n_wrapped += count
    print(f"Wrapped {n_wrapped} bibliographies in <details> across {n_files} files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
