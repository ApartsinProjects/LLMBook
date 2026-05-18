"""Wave 34e: Remove unused KaTeX / Prism includes (UNUSED_VENDOR fix).

For each section/index page that loads KaTeX or Prism but has no math /
no code blocks: drop the relevant `<link>` and `<script>` tags from `<head>`.

Pages we touch are exactly the 28 the UNUSED_VENDOR plugin flags. Detection
logic mirrors the plugin: KaTeX is "unused" if there's no `$$...$$` or `$x$`
in the body; Prism is "unused" if there's no `<pre>` block.
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'.git', 'node_modules', 'KDP', 'build', 'source_fix_backups', 'pagefind',
        '.book-update', 'vendor', '.claude', '_archive', 'agents', 'templates',
        'docs', 'scripts'}

KATEX_LOAD = re.compile(r'(?:href|src)="[^"]*katex[^"]*"', re.IGNORECASE)
PRISM_LOAD = re.compile(r'(?:href|src)="[^"]*prism[^"]*"', re.IGNORECASE)
STRIP_SCRIPT = re.compile(r'<(?:script|style)[^>]*>.*?</(?:script|style)>', re.DOTALL | re.IGNORECASE)

# Tag patterns to remove. Each is a regex that matches one line (or multiline-script).
KATEX_TAGS = [
    re.compile(r'<link\s+href="[^"]*vendor/katex/[^"]*"\s+rel="stylesheet"\s*/?>\s*\n?', re.IGNORECASE),
    re.compile(r'<script\s+defer=""\s+src="[^"]*vendor/katex/katex\.min\.js"></script>\s*\n?', re.IGNORECASE),
    re.compile(r'<script\s+defer=""\s+onload="[^"]*renderMathInElement[\s\S]*?src="[^"]*vendor/katex/contrib/auto-render\.min\.js"></script>\s*\n?', re.IGNORECASE),
]
PRISM_TAGS = [
    re.compile(r'<link\s+href="[^"]*vendor/prism/[^"]*"\s+rel="stylesheet"\s*/?>\s*\n?', re.IGNORECASE),
    re.compile(r'<script\s+defer=""\s+src="[^"]*vendor/prism/prism-bundle\.min\.js"></script>\s*\n?', re.IGNORECASE),
]


def page_uses_katex(html: str) -> bool:
    body_m = re.search(r'<body[^>]*>(.*)</body>', html, re.DOTALL | re.IGNORECASE)
    if not body_m:
        return True  # be conservative
    body = STRIP_SCRIPT.sub('', body_m.group(1))
    return bool(re.search(r'\$\$', body) or re.search(r'\$[^$\s][^$]*\$', body))


def page_uses_prism(html: str) -> bool:
    body_m = re.search(r'<body[^>]*>(.*)</body>', html, re.DOTALL | re.IGNORECASE)
    if not body_m:
        return True
    body = STRIP_SCRIPT.sub('', body_m.group(1))
    return bool(re.search(r'<pre\b', body, re.IGNORECASE))


def main():
    n_files = 0
    n_katex_removed = 0
    n_prism_removed = 0
    for p in sorted(ROOT.rglob('*.html')):
        if set(p.parts) & SKIP:
            continue
        text = p.read_text(encoding='utf-8')
        loads_katex = bool(KATEX_LOAD.search(text))
        loads_prism = bool(PRISM_LOAD.search(text))
        if not (loads_katex or loads_prism):
            continue
        original = text
        if loads_katex and not page_uses_katex(text):
            for pat in KATEX_TAGS:
                text, n = pat.subn('', text)
                n_katex_removed += n
        if loads_prism and not page_uses_prism(text):
            for pat in PRISM_TAGS:
                text, n = pat.subn('', text)
                n_prism_removed += n
        if text != original:
            p.write_text(text, encoding='utf-8')
            n_files += 1
            print(f'  {p.relative_to(ROOT)}: katex_removed={loads_katex and not page_uses_katex(original)}, prism_removed={loads_prism and not page_uses_prism(original)}')
    print(f'\nFiles updated: {n_files}')
    print(f'  KaTeX tags removed: {n_katex_removed}')
    print(f'  Prism tags removed: {n_prism_removed}')


if __name__ == '__main__':
    main()
