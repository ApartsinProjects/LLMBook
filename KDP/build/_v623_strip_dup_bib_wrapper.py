"""v6.23: Strip duplicate <details class="bibliography-collapsible"> wrapper.

USER REPORT
"in some pages I see the References & Further Reading section [outer header]
 with a card [inner with book emoji] — I need only the card. See section-23.1.html"

ROOT CAUSE
The HTML files have:
   <details class="bibliography-collapsible" open>
     <summary><strong>References & Further Reading</strong></summary>
     <section class="bibliography">...</section>
   </details>

But scripts/book.js (#8) ALSO wraps every <section class="bibliography"> in a
fresh <details class="bib-collapse"> at runtime, with a 📚 emoji summary.
Result: TWO toggles. The user sees:
   ▼ References & Further Reading        (the HTML wrapper, open by default)
   ▶ 📚 References and Further Reading   (the JS-injected card, closed)

FIX
Strip the outer HTML <details class="bibliography-collapsible"> wrapper.
Keep the inner <section class="bibliography"> intact — book.js will wrap it
properly at runtime, producing a single clean card.

Idempotent: skip files where the wrapper is already gone.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

# Match: opening tag, optional whitespace, summary, optional whitespace, then
# everything up to and including </details>. We extract the inner content
# (typically <section class="bibliography">...</section>) and replace the whole
# block with just that.
WRAPPER_RE = re.compile(
    r'<details class="bibliography-collapsible"[^>]*>\s*'
    r'<summary>[^<]*<strong>[^<]*</strong>[^<]*</summary>\s*'
    r'(<section class="bibliography">.*?</section>)\s*'
    r'</details>',
    re.DOTALL,
)


def fix_file(p: Path) -> bool:
    text = p.read_text(encoding='utf-8')
    new_text, n = WRAPPER_RE.subn(r'\1', text, count=1)
    if n == 0:
        return False
    p.write_text(new_text, encoding='utf-8')
    return True


def main() -> int:
    fixed = 0
    files = sorted({
        *ROOT.glob('part-*/module-*/section-*.html'),
        *ROOT.glob('part-*/module-*/index.html'),
        *ROOT.glob('appendices/appendix-*/section-*.html'),
        *ROOT.glob('appendices/appendix-*/index.html'),
    })
    for p in files:
        if fix_file(p):
            fixed += 1
    print(f'Stripped duplicate bibliography-collapsible wrapper from {fixed} files')
    return 0


if __name__ == '__main__':
    sys.exit(main())
