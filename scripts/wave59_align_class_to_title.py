"""Wave 59: Align callout class to its title.

After Wave 57 collapsed "Key Insight: Key Takeaways" → "Key Takeaways", the
class stayed as `key-insight` while the title became "Key Takeaways". The
class/title mismatch is the more meaningful issue, not the title. Fix: when
the title is "Key Takeaway(s)", change the class to `key-takeaway`.

Generalizes to any callout class/title mismatch where the title clearly names
a different canonical type.
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'.git', 'node_modules', 'KDP', 'build', 'source_fix_backups',
        'pagefind', '.book-update', 'vendor', '.claude', '_archive',
        'agents', 'templates', 'docs', 'scripts'}

# Map: title-keyword (lowercase) -> canonical callout class
TITLE_TO_CLASS = {
    'key takeaway': 'key-takeaway',
    'key takeaways': 'key-takeaway',
    'big picture': 'big-picture',
    'looking back': 'looking-back',
    "what's next": 'whats-next',
    'what comes next': 'whats-next',
    'real-world scenario': 'practical-example',
    'practical example': 'practical-example',
    'production pattern': 'production-pattern',
    'research frontier': 'research-frontier',
    'library shortcut': 'library-shortcut',
    'numeric example': 'numeric-example',
    'postmortem': 'postmortem',
    'self-check': 'self-check',
    'cross-reference': 'cross-ref',
    'fun fact': 'fun-note',
    'thesis thread': 'thesis-thread',
}

# Match a callout with its current class and title, capturing both
CALLOUT_RE = re.compile(
    r'(<div\s+class="callout\s+)([a-z-]+)(")([^>]*>\s*<div\s+class="callout-title"[^>]*>)([^<]+)(</div>)',
    re.IGNORECASE,
)


def fix_file(p: Path) -> int:
    text = p.read_text(encoding='utf-8')
    n = 0

    def repl(m: re.Match) -> str:
        nonlocal n
        prefix1 = m.group(1)
        cur_class = m.group(2).lower()
        prefix2 = m.group(3)
        prefix3 = m.group(4)
        title = m.group(5).strip()
        closer = m.group(6)

        title_lower = title.lower().strip().rstrip(':').strip()
        # Drop leading "TYPE: " prefix when checking
        if ':' in title_lower:
            title_lower = title_lower.split(':', 1)[1].strip()

        target_class = None
        for kw, cls in TITLE_TO_CLASS.items():
            if title_lower.startswith(kw):
                target_class = cls
                break

        if target_class and target_class != cur_class:
            n += 1
            return f'{prefix1}{target_class}{prefix2}{prefix3}{title}{closer}'
        return m.group()

    new_text = CALLOUT_RE.sub(repl, text)
    if new_text != text:
        p.write_text(new_text, encoding='utf-8')
    return n


def main():
    n_total = 0
    files_touched = 0
    for p in sorted(ROOT.rglob('*.html')):
        if set(p.parts) & SKIP:
            continue
        n = fix_file(p)
        if n > 0:
            n_total += n
            files_touched += 1
    print(f'Callout class realigned to title: {n_total}')
    print(f'Files touched: {files_touched}')


if __name__ == '__main__':
    main()
