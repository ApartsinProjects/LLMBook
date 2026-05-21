"""Wave 74: Drop the thesis-thread callout type.

Decisions:
- HTML: convert 8 <div class="callout thesis-thread"> → <div class="callout key-insight">
  (semantically closest; thesis-thread carried single conceptual observations
  tied to a recurring book-wide thesis — that's exactly the key-insight role)
- Title: drop "Thesis N in action: " or "Thesis N + Thesis M in action: " prefix,
  prepend "Key Insight: " to satisfy CALLOUT_TITLE_PREFIX for key-insight type.
- CSS: remove .callout.thesis-thread rules from book.css
- Plugins: remove "thesis-thread" / "Thesis Thread" from CANONICAL_TYPES,
  CANONICAL_PREFIXES, BARE_DIV regex, structural-violation titles.
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'.git', 'node_modules', 'KDP', 'build', 'source_fix_backups',
        'pagefind', '.book-update', 'vendor', '.claude', '_archive',
        'agents', 'templates', 'docs', 'scripts'}

# 1. Convert <div class="callout thesis-thread"> → <div class="callout key-insight">
THESIS_OPEN_RE = re.compile(
    r'<div\s+class="callout thesis-thread"([^>]*)>',
    re.IGNORECASE,
)
# 2. Title rewrite: "Thesis N in action:" or "Thesis N + Thesis M in action:" → "Key Insight:"
TITLE_REWRITE_RE = re.compile(
    r'(<div\s+class="callout-title"[^>]*>)\s*'
    r'Thesis\s+\d+(?:\s*[+&]\s*Thesis\s+\d+)*\s+in\s+action\s*:\s*'
    r'([^<]+)'
    r'(</div>)',
    re.IGNORECASE,
)


def fix_html(text: str) -> tuple[str, int]:
    n = 0
    new = THESIS_OPEN_RE.sub(
        lambda m: f'<div class="callout key-insight"{m.group(1)}>',
        text,
    )
    if new != text:
        # count occurrences
        n = len(THESIS_OPEN_RE.findall(text))
    # Rewrite titles
    def title_repl(m):
        return f'{m.group(1)}Key Insight: {m.group(2).strip()}{m.group(3)}'
    new = TITLE_REWRITE_RE.sub(title_repl, new)
    return new, n


def main():
    n_html = 0
    files = 0
    for p in sorted(ROOT.rglob('*.html')):
        if set(p.parts) & SKIP:
            continue
        text = p.read_text(encoding='utf-8')
        new, n = fix_html(text)
        if new != text:
            p.write_text(new, encoding='utf-8')
            files += 1
            n_html += n
    print(f'HTML: {n_html} thesis-thread → key-insight across {files} files')

    # CSS: remove .callout.thesis-thread rules
    css_path = ROOT / 'styles' / 'book.css'
    css = css_path.read_text(encoding='utf-8')
    orig = css
    patterns = [
        r'^\.callout\.thesis-thread\s*\{[^}]*\}\s*\n',
        r'^\.callout\.thesis-thread\s+\.callout-title\s*\{[^}]*\}\s*\n',
        r'^\.callout\.thesis-thread\s+\.callout-title::before\s*\{[^}]*\}\s*\n',
        r'^\.callout\.thesis-thread\s+\.callout-title::after\s*\{[^}]*\}\s*\n',
    ]
    for pat in patterns:
        css = re.sub(pat, '', css, flags=re.MULTILINE)
    if css != orig:
        css_path.write_text(css, encoding='utf-8')
        print('CSS: removed .callout.thesis-thread rules')

    # Plugins
    plugin_dir = ROOT / 'agents' / 'book-skills' / 'scripts' / 'audit' / 'checks'

    # p2_callout_canonical_structure.py: remove "thesis-thread"
    p = plugin_dir / 'p2_callout_canonical_structure.py'
    text = p.read_text(encoding='utf-8')
    new = re.sub(r'\s*"thesis-thread",', '', text)
    if new != text:
        p.write_text(new, encoding='utf-8')
        print('Plugin: removed "thesis-thread" from p2_callout_canonical_structure')

    # p2_callout_title_prefix.py
    p = plugin_dir / 'p2_callout_title_prefix.py'
    text = p.read_text(encoding='utf-8')
    new = re.sub(r'\s*"thesis-thread":\s*\[[^\]]*\],\s*\n', '\n', text)
    new = re.sub(r'\s*thesis-thread\s+->\s*"Thesis Thread"[^\n]*\n', '\n', new)
    if new != text:
        p.write_text(new, encoding='utf-8')
        print('Plugin: removed "thesis-thread" from p2_callout_title_prefix')

    # p2_pseudo_callout.py: remove thesis-thread alternative
    p = plugin_dir / 'p2_pseudo_callout.py'
    text = p.read_text(encoding='utf-8')
    new = text.replace('|thesis-thread', '').replace('thesis-thread|', '')
    new = re.sub(r'Thesis Thread\|', '', new)
    new = re.sub(r'\|Thesis Thread', '', new)
    if new != text:
        p.write_text(new, encoding='utf-8')
        print('Plugin: removed "thesis-thread" from p2_pseudo_callout')

    # p1_structural_violations.py: drop "Thesis Thread" title from CANONICAL_TITLES
    p = plugin_dir / 'p1_structural_violations.py'
    text = p.read_text(encoding='utf-8')
    new = re.sub(r"\s*'Thesis Thread',", '', text)
    if new != text:
        p.write_text(new, encoding='utf-8')
        print('Plugin: removed "Thesis Thread" from p1_structural_violations')


if __name__ == '__main__':
    main()
