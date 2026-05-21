"""Wave 33: Consolidate `key-takeaway` callouts into `key-insight`.

Per agents/book-skills/scripts/audit/checks/p1_section_structure.py:107-109,
`key-takeaway` is deprecated. Canonical is `key-insight`.

User flagged section-82.1 having a `key-takeaway` callout as visually non-standard;
the plugin agrees.

Conservative replacement:
  <div class="callout key-takeaway">         -> <div class="callout key-insight">
  <div class="callout-title">Key Takeaway</div>  -> <div class="callout-title">Key Insight</div>
  <div class="callout-title">Key Takeaways</div> -> <div class="callout-title">Key Insights</div>
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'.git', 'node_modules', 'KDP', 'build', 'temp_ebook', 'temp_epub',
        'source_fix_backups', 'pagefind', '.book-update', 'vendor',
        '.claude', '_archive'}


def fix(text: str) -> tuple[str, int]:
    n = 0
    new = text
    # 1) class change
    m1 = re.subn(r'<div\s+class="callout\s+key-takeaway"', '<div class="callout key-insight"', new)
    new, c1 = m1[0], m1[1]
    n += c1
    # 2) title text change (only exact match of "Key Takeaway" / "Key Takeaways")
    m2 = re.subn(
        r'(<div\s+class="callout-title"[^>]*>)\s*Key Takeaways\s*(</div>)',
        r'\1Key Insights\2', new,
    )
    new, c2 = m2[0], m2[1]
    m3 = re.subn(
        r'(<div\s+class="callout-title"[^>]*>)\s*Key Takeaway\s*(</div>)',
        r'\1Key Insight\2', new,
    )
    new, c3 = m3[0], m3[1]
    return new, c1


def main():
    n_files = 0
    n_total = 0
    for p in sorted(ROOT.rglob('*.html')):
        if set(p.parts) & SKIP:
            continue
        # Skip templates (intentional patterns)
        if 'templates' in p.parts:
            continue
        text = p.read_text(encoding='utf-8')
        new, n = fix(text)
        if n > 0:
            p.write_text(new, encoding='utf-8')
            n_files += 1
            n_total += n
    print(f'Replaced {n_total} key-takeaway -> key-insight in {n_files} files')


if __name__ == '__main__':
    main()
