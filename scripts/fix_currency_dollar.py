"""Fix currency dollar signs that KaTeX auto-render mis-renders as math.

Root cause: prose written with two `&#36;` (or `&dollar;`) entities on the same
text node, e.g. "as low as &#36;0.10 ... under &#36;100", decodes to two literal
`$` in the DOM. KaTeX's renderMathInElement then treats everything between them
as inline math, collapsing spaces into serif math text.

Fix (verified empirically against the book's KaTeX): wrap each currency entity in
a <span>, so the two `$` land in SEPARATE text nodes and KaTeX never pairs them.
The dollar still renders as a literal `$`. Escaping with `\\$` was rejected
because KaTeX auto-render leaves a visible backslash outside math.

Safety:
  - KaTeX already ignores <pre>/<code>/<script>/<style>, and those often contain
    legitimate `$VAR` shell/code dollars, so we DO NOT touch entities inside them.
  - We never touch entities inside HTML tags/attributes.
  - Idempotent: an entity already wrapped in <span>...</span> is left alone.

Run:  py -3 scripts/fix_currency_dollar.py            # dry-run (counts)
      py -3 scripts/fix_currency_dollar.py --apply
"""
from __future__ import annotations
import argparse, re, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parent.parent
SKIP = {"_archive", "node_modules", ".git", "pagefind", "KDP", "build", "vendor",
        ".claude", "__pycache__", ".book-update", ".tools", "temp_epub"}

# Protect code AND math contexts: some inline math is written with an entity-open
# delimiter, e.g. <span class="math">&#36;2 \cdot R$</span> or a bare
# &#36;\alpha$ run. Those &#36; are math delimiters, NOT currency, so must not be
# wrapped (wrapping would split the delimiter into its own text node and break
# KaTeX). We protect: code/pre/script/style, <span class="math">, math-block divs,
# $$...$$ display math, and bare entity-open inline math containing a LaTeX command.
PROTECT = re.compile(
    r"<(pre|code|script|style)\b.*?</\1>"
    r'|<span class="math">.*?</span>'
    r'|<div class="math-block">.*?</div>'
    r"|\$\$.*?\$\$"
    r"|&#36;[^\n$]*\\[A-Za-z][^\n$]*\$",
    re.S | re.I,
)
TAG = re.compile(r"<[^>]+>")
ENT = re.compile(r"&#36;|&dollar;")
ALREADY = re.compile(r"<span>(?:&#36;|&dollar;)</span>")


def fix(html: str):
    if "&#36;" not in html and "&dollar;" not in html:
        return html, 0
    # 1) stash protected blocks (code/pre/script/style)
    blocks = []
    def stash_b(m):
        blocks.append(m.group(0))
        return f"\x00B{len(blocks)-1}\x00"
    h = PROTECT.sub(stash_b, html)
    # 2) stash already-wrapped entities so we don't double-wrap
    already = []
    def stash_a(m):
        already.append(m.group(0))
        return f"\x00A{len(already)-1}\x00"
    h = ALREADY.sub(stash_a, h)
    # 3) stash tags (so we don't touch entities inside attributes)
    tags = []
    def stash_t(m):
        tags.append(m.group(0))
        return f"\x00T{len(tags)-1}\x00"
    h = TAG.sub(stash_t, h)
    # 4) wrap remaining (prose) currency entities
    n = len(ENT.findall(h))
    h = ENT.sub(lambda m: f"<span>{m.group(0)}</span>", h)
    # 5) restore tags, then already-wrapped, then blocks
    h = re.sub(r"\x00T(\d+)\x00", lambda m: tags[int(m.group(1))], h)
    h = re.sub(r"\x00A(\d+)\x00", lambda m: already[int(m.group(1))], h)
    h = re.sub(r"\x00B(\d+)\x00", lambda m: blocks[int(m.group(1))], h)
    return h, n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    total = 0
    files = 0
    for p in ROOT.rglob("*.html"):
        if any(s in p.parts for s in SKIP):
            continue
        html = p.read_text(encoding="utf-8", errors="ignore")
        new, n = fix(html)
        if n and new != html:
            files += 1
            total += n
            if args.apply:
                p.write_text(new, encoding="utf-8")
            else:
                print(f"  {n:4}  {p.relative_to(ROOT)}")
    print(f"\n{total} currency entities in {files} files "
          f"{'wrapped' if args.apply else '(dry-run)'}")
    if not args.apply:
        print("(pass --apply to write)")


if __name__ == "__main__":
    main()
