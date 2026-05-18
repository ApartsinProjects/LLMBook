"""Wave 38a: Remove inflated mid-content chapter-nav blocks.

Several section files have been forcibly merged from multiple tot-subsections,
each carrying their own `<nav class="chapter-nav">` + `<footer>` pair. The
result: a single section file with 5-10 chapter-nav blocks scattered through
the body, mostly pointing to non-existent old anchor IDs.

Fix: keep the FIRST canonical nav+footer pair (which has correct prev/next
for the actual section), remove all OTHER nav+footer pairs, and re-insert
the canonical pair just before `</main>` if it isn't already at the end.

Targets per cycle-3 audit:
  section-5.1.html (7 navs), section-5.2.html (8), section-10.6.html (5),
  section-10.8.html (2), section-14.2.html (3), section-19.2.html (10),
  section-19.3.html (5).

But we apply book-wide: any file with >2 chapter-nav blocks gets cleaned.
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'.git', 'node_modules', 'KDP', 'build', 'source_fix_backups',
        'pagefind', '.book-update', 'vendor', '.claude', '_archive',
        'agents', 'templates', 'docs', 'scripts'}

NAV_RE = re.compile(r'<nav\s+class="chapter-nav"[^>]*>[\s\S]*?</nav>', re.IGNORECASE)
FOOTER_RE = re.compile(r'<footer[^>]*>[\s\S]*?</footer>', re.IGNORECASE)
NAV_THEN_FOOTER = re.compile(
    r'<nav\s+class="chapter-nav"[^>]*>[\s\S]*?</nav>\s*<footer[^>]*>[\s\S]*?</footer>',
    re.IGNORECASE,
)
MAIN_CLOSE = re.compile(r'</main>', re.IGNORECASE)


def fix(text: str) -> tuple[str, int]:
    navs = NAV_RE.findall(text)
    if len(navs) <= 1:
        return text, 0

    # Capture the FIRST nav + the FIRST footer immediately after it (canonical pair)
    first_pair_m = NAV_THEN_FOOTER.search(text)
    if first_pair_m:
        canonical_pair = first_pair_m.group(0)
    else:
        # No adjacent footer; just keep the first nav
        canonical_pair = navs[0]

    # Remove ALL nav+footer pairs from the file
    new_text = NAV_THEN_FOOTER.sub('', text)
    # Also remove any orphaned chapter-nav blocks without adjacent footer
    new_text = NAV_RE.sub('', new_text)

    # Re-insert canonical pair just before </main>
    main_m = MAIN_CLOSE.search(new_text)
    if main_m:
        new_text = new_text[:main_m.start()] + canonical_pair + '\n' + new_text[main_m.start():]
    else:
        # No </main> -- append at the very end
        new_text = new_text.rstrip() + '\n' + canonical_pair + '\n'

    # Count removed pairs = original navs - 1 (we kept one)
    return new_text, len(navs) - 1


def main():
    n_files = 0
    n_total = 0
    for p in sorted(ROOT.rglob('*.html')):
        if set(p.parts) & SKIP:
            continue
        text = p.read_text(encoding='utf-8')
        new, removed = fix(text)
        if removed > 0 and new != text:
            p.write_text(new, encoding='utf-8')
            n_files += 1
            n_total += removed
            print(f'  {p.relative_to(ROOT)}: removed {removed} inflated nav block(s)')
    print(f'\nRemoved {n_total} inflated nav+footer pairs across {n_files} files')


if __name__ == '__main__':
    main()
