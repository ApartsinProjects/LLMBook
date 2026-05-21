"""Add the KaTeX renderer to any page that contains math but doesn't load it.

Root cause: content passes added `$...$` / `$$...$$` / <span class="math"> /
<div class="math-block"> math to sections whose <head> never included the
KaTeX auto-render script. Those pages show raw dollar-sign text instead of
rendered math.

This script:
  1. Detects pages that CONTAIN math markup.
  2. Detects pages that do NOT already load KaTeX (renderMathInElement).
  3. Inserts the canonical KaTeX <head> block with the correct relative
     path prefix for the file's depth.

Math detection signals (any one):
  - <div class="math-block">
  - <span class="math">
  - $$...$$  (display delimiters)
  - a bare $...$ span containing a LaTeX backslash command

Run:
  py -3 scripts/fix_missing_katex_include.py            # dry-run
  py -3 scripts/fix_missing_katex_include.py --apply
"""
from __future__ import annotations
import argparse, re, sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
ROOT = Path(__file__).resolve().parent.parent
SKIP_DIRS = {'_archive', 'node_modules', '.git', 'pagefind', 'KDP',
             'build', 'vendor', '.claude', '__pycache__', '.book-update'}

KATEX_PRESENT = re.compile(r'renderMathInElement|katex\.min\.js', re.I)

MATH_BLOCK = re.compile(r'class="math-block"')
MATH_SPAN = re.compile(r'class="math"')
DISPLAY_DD = re.compile(r'\$\$')
# Bare inline $...$ containing a backslash LaTeX command (e.g. $\mathbf{w}$).
INLINE_TEX = re.compile(r'\$[^$\n]*\\[A-Za-z]+[^$\n]*\$')

# Protect code/script/pre when scanning for bare $ (avoid false positives from
# shell prompts, prices in code, etc.). We strip those regions first.
STRIP = re.compile(r'<pre\b.*?</pre>|<code\b.*?</code>|<script\b.*?</script>',
                   re.DOTALL | re.IGNORECASE)


def has_math(html: str) -> bool:
    if MATH_BLOCK.search(html) or MATH_SPAN.search(html):
        return True
    body = STRIP.sub('', html)
    if DISPLAY_DD.search(body):
        return True
    if INLINE_TEX.search(body):
        return True
    return False


def katex_block(prefix: str) -> str:
    return (
        f'<link href="{prefix}vendor/katex/katex.min.css" rel="stylesheet"/>\n'
        f'<script defer="" src="{prefix}vendor/katex/katex.min.js"></script>\n'
        f'<script defer="" onload="renderMathInElement(document.body, {{\n'
        f' delimiters: [\n'
        f" {{left: '$$', right: '$$', display: true}},\n"
        f" {{left: '$', right: '$', display: false}}\n"
        f' ],\n'
        f' throwOnError: false\n'
        f' }});" src="{prefix}vendor/katex/contrib/auto-render.min.js"></script>\n'
    )


def rel_prefix(path: Path) -> str:
    # depth = number of dirs between ROOT and the file
    depth = len(path.relative_to(ROOT).parts) - 1
    return '../' * depth


def fix_file(path: Path, apply: bool) -> bool:
    html = path.read_text(encoding='utf-8')
    if not has_math(html):
        return False
    if KATEX_PRESENT.search(html):
        return False
    # Insert before </head>. Prefer right after the book.css link for tidiness.
    block = katex_block(rel_prefix(path))
    if '</head>' not in html:
        return False
    # Insert immediately before </head>
    new_html = html.replace('</head>', block + '</head>', 1)
    if apply:
        path.write_text(new_html, encoding='utf-8')
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--apply', action='store_true')
    args = ap.parse_args()
    fixed = []
    for p in ROOT.rglob('*.html'):
        if any(s in p.parts for s in SKIP_DIRS):
            continue
        if fix_file(p, args.apply):
            fixed.append(p.relative_to(ROOT))
    for f in fixed:
        print(f'  {f}')
    print(f"\n{len(fixed)} page(s) {'fixed' if args.apply else 'need KaTeX (dry-run)'}")
    if not args.apply:
        print('(pass --apply to write)')


if __name__ == '__main__':
    main()
