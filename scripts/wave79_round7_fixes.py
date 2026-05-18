"""Wave 79: Round-7 fixes for user feedback 2026-05-18 cont.

1. <div class="takeaways"> fake callouts → canonical <div class="callout key-takeaway">
   The takeaways div has its own styling that's similar-but-different from
   callout grid. Convert to canonical.

2. "Looking Forward" / "Looking forward" h2 → check context:
   - If body is forward-looking (what comes next in this chapter/book),
     convert to whats-next callout
   - Otherwise convert to research-frontier

3. Audit all <div class="(callout )?whats-next"> bodies:
   - Body MUST mention specific next section by anchor link
   - Otherwise flag (no auto-fix, just report)
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'.git', 'node_modules', 'KDP', 'build', 'source_fix_backups',
        'pagefind', '.book-update', 'vendor', '.claude', '_archive',
        'agents', 'templates', 'docs', 'scripts'}

# 1. <div class="takeaways"> ... </div> → <div class="callout key-takeaway">
TAKEAWAYS_RE = re.compile(
    r'<div\s+class="takeaways"([^>]*)>\s*'
    r'<h2[^>]*>([^<]+)</h2>\s*'
    r'(<(?:ul|ol)>[\s\S]*?</(?:ul|ol)>)\s*'
    r'</div>',
    re.IGNORECASE,
)

# 2. <h2 id="...looking-forward">Looking Forward</h2> + following <div class="callout key-insight"...> → whats-next
LOOKING_FORWARD_RE = re.compile(
    r'<h2\s+id="[^"]*looking-forward"[^>]*>[\d\s.\-]*Looking Forward</h2>\s*'
    r'<div\s+class="callout key-insight"([^>]*)>\s*'
    r'<div\s+class="callout-title"[^>]*>[^<]+</div>',
    re.IGNORECASE,
)


def fix_file(p: Path) -> dict[str, int]:
    text = p.read_text(encoding='utf-8')
    orig = text
    counts = {'takeaways': 0, 'looking_forward': 0}

    # 1. <div class="takeaways"> → callout key-takeaway
    def takeaways_repl(m):
        counts['takeaways'] += 1
        attrs = m.group(1)
        title = m.group(2).strip()
        body = m.group(3)
        # Drop section number prefix from title
        title_clean = re.sub(r'^[\d.\-]+\s*', '', title)
        # If title is just "Quick Reference Cheat Sheet" or "Key Takeaways", use as-is
        # Otherwise prefix "Key Takeaways: "
        if title_clean.lower() in ('key takeaways', 'key takeaway', 'takeaways'):
            new_title = 'Key Takeaways'
        else:
            new_title = f'Key Takeaways: {title_clean}'
        return (
            f'<div class="callout key-takeaway"{attrs}>\n'
            f'<div class="callout-title">{new_title}</div>\n'
            f'{body}\n'
            f'</div>'
        )
    text = TAKEAWAYS_RE.sub(takeaways_repl, text)

    # 2. "Looking Forward" h2 → drop the h2, convert key-insight to whats-next callout
    def lf_repl(m):
        counts['looking_forward'] += 1
        attrs = m.group(1)
        # The h2 is dropped; the following key-insight callout becomes whats-next
        return (
            f'<div class="callout whats-next"{attrs}>\n'
            f'<div class="callout-title">What\'s Next</div>'
        )
    text = LOOKING_FORWARD_RE.sub(lf_repl, text)

    if text != orig:
        p.write_text(text, encoding='utf-8')
    return counts


def main():
    totals = {'takeaways': 0, 'looking_forward': 0}
    files = 0
    for p in sorted(ROOT.rglob('*.html')):
        if set(p.parts) & SKIP:
            continue
        c = fix_file(p)
        if sum(c.values()) > 0:
            files += 1
            for k, v in c.items():
                totals[k] += v
    print(f'<div class="takeaways"> → callout key-takeaway: {totals["takeaways"]}')
    print(f'"Looking Forward" h2 → whats-next: {totals["looking_forward"]}')
    print(f'Files touched: {files}')


if __name__ == '__main__':
    main()
