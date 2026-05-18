"""Wave 92: Replace &amp;amp; with &amp; book-wide.

Multiple section/chapter/part pages contain `&amp;amp;` in headers,
breadcrumbs, and chapter-nav. The browser renders this as the literal
text `&amp;`, not as `&`. Probably happened when a script HTML-escaped
already-escaped strings.

The fix: replace `&amp;amp;` with `&amp;` everywhere except inside
<pre>, <code>, and CDATA blocks (where the literal `&amp;amp;` may be
intentional code).
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
SKIP = {".git", "node_modules", "KDP", "build", "source_fix_backups",
        "pagefind", ".book-update", "vendor", ".claude", "_archive",
        "agents", "templates", "docs", "scripts"}

# Match <pre>...</pre>, <code>...</code>, or whole-file body. We mask
# code/pre blocks during the replace, then unmask.
CODE_BLOCK_RE = re.compile(
    r'<pre\b[^>]*>.*?</pre>|<code\b[^>]*>.*?</code>',
    re.IGNORECASE | re.DOTALL,
)


def fix_file(p: Path) -> int:
    text = p.read_text(encoding="utf-8")
    if '&amp;amp;' not in text:
        return 0
    # Mask code/pre blocks
    masks = []
    def mask(m):
        masks.append(m.group(0))
        return f'__CODEMASK_{len(masks)-1}__'
    masked = CODE_BLOCK_RE.sub(mask, text)
    # Replace &amp;amp; with &amp; outside of masked blocks
    fixed = masked.replace('&amp;amp;', '&amp;')
    # Unmask
    def unmask(m):
        idx = int(m.group(1))
        return masks[idx]
    new = re.sub(r'__CODEMASK_(\d+)__', unmask, fixed)
    if new == text:
        return 0
    p.write_text(new, encoding="utf-8")
    return 1


def main():
    n = 0
    for p in sorted(ROOT.rglob("*.html")):
        if set(p.parts) & SKIP:
            continue
        if fix_file(p):
            n += 1
            print(f"  + {p.relative_to(ROOT)}")
    print(f"\nFiles touched: {n}")


if __name__ == "__main__":
    main()
