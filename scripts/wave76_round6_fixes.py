"""Wave 76: Round-6 structural fixes (user feedback 2026-05-18 cont).

1. URL overflow in code/anchor (40.3.3 pattern): long URLs in <code>...</code>
   blow past the page width on narrow screens because <code> has no
   overflow-wrap. Add CSS rule to wrap long URLs / paths.

2. Bare <svg> not inside a <figure> wrapper (41.1.7 pattern): wrap the SVG
   in <figure class="illustration"> so it gets the canonical figure styling
   and can carry a figcaption (which the user can author later).

3. Bibliography callout closed-state design: make the <details> summary look
   like other callout-titles (icon + bold + colored band) so the closed bib
   visually matches the rest of the callout grid.

CSS additions only; no HTML edits except the SVG wrapping.
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'.git', 'node_modules', 'KDP', 'build', 'source_fix_backups',
        'pagefind', '.book-update', 'vendor', '.claude', '_archive',
        'agents', 'templates', 'docs', 'scripts'}

# Match bare <svg ...> at the start of a line, NOT wrapped in <figure> or
# <div class="diagram-container">.
BARE_SVG_RE = re.compile(
    r'(?P<prefix>^(?:\s*)?</h2>\s*\n)?'
    r'(?P<svg><svg\b[^>]*>[\s\S]*?</svg>)',
    re.MULTILINE,
)


def wrap_bare_svg(text: str) -> tuple[str, int]:
    """Wrap each bare <svg> (not already inside <figure> or .diagram-container)
    in a <figure class="illustration"> tag."""
    n = 0
    out = []
    pos = 0
    for m in re.finditer(r'<svg\b[^>]*>', text, re.IGNORECASE):
        # Check if already inside <figure> or .diagram-container by looking
        # back 500 chars for opening tag
        window = text[max(0, m.start() - 500):m.start()]
        # Last <figure or <div class="diagram-container" vs last </figure> or </div>
        last_fig_open = max(
            window.rfind('<figure'),
            window.rfind('<div class="diagram-container'),
            window.rfind('<div class="comparison-grid'),
            window.rfind('<div class="comparison-table-content'),
        )
        last_fig_close = max(
            window.rfind('</figure>'),
            window.rfind('</div>'),
        )
        if last_fig_open > last_fig_close:
            continue  # already inside a wrapper
        # Find matching </svg>
        svg_close = text.find('</svg>', m.end())
        if svg_close == -1:
            continue
        svg_end = svg_close + len('</svg>')
        out.append(text[pos:m.start()])
        out.append('<figure class="illustration">\n')
        out.append(text[m.start():svg_end])
        out.append('\n</figure>')
        pos = svg_end
        n += 1
    out.append(text[pos:])
    return ''.join(out), n


def main():
    n_svg = 0
    files = 0
    for p in sorted(ROOT.rglob('*.html')):
        if set(p.parts) & SKIP:
            continue
        text = p.read_text(encoding='utf-8')
        new, n = wrap_bare_svg(text)
        if new != text:
            p.write_text(new, encoding='utf-8')
            files += 1
            n_svg += n
    print(f'Bare <svg> wrapped in <figure class="illustration">: {n_svg} in {files} files')


if __name__ == '__main__':
    main()
