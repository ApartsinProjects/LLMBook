"""Wave 106: escape unescaped & in <title> tags + nav-title spans.

Newly-split section files have titles like "QKV, Scaled Dot-Product
& Causal Masking" with a literal `&`. HTML requires `&amp;`.

Also fixes <meta name="description" content="... & ..."> and
<span class="nav-title">...& ...</span> patterns where the splitter
left raw ampersands.
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
SKIP = {".git", "node_modules", "KDP", "build", "source_fix_backups",
        "pagefind", ".book-update", "vendor", ".claude", "_archive",
        "agents", "templates", "docs", "scripts"}

TITLE_RE = re.compile(r'<title>([^<]*)</title>', re.IGNORECASE)
NAV_TITLE_RE = re.compile(
    r'(<span\s+class="nav-title">)([^<]*)(</span>)',
    re.IGNORECASE,
)
META_DESC_RE = re.compile(
    r'(<meta\s+content=")([^"]*)("\s+name="description")',
    re.IGNORECASE,
)


def escape_bare_amp(s: str) -> str:
    """Replace lone & with &amp;, leaving existing entities alone."""
    return re.sub(r'&(?!(?:amp|lt|gt|quot|apos|#\d+|#x[\da-fA-F]+);)', '&amp;', s)


def fix(p: Path) -> int:
    text = p.read_text(encoding="utf-8")
    n = 0
    def replace_title(m):
        nonlocal n
        new = escape_bare_amp(m.group(1))
        if new != m.group(1):
            n += 1
        return f'<title>{new}</title>'
    def replace_nav(m):
        nonlocal n
        new = escape_bare_amp(m.group(2))
        if new != m.group(2):
            n += 1
        return f'{m.group(1)}{new}{m.group(3)}'
    def replace_meta(m):
        nonlocal n
        new = escape_bare_amp(m.group(2))
        if new != m.group(2):
            n += 1
        return f'{m.group(1)}{new}{m.group(3)}'

    text = TITLE_RE.sub(replace_title, text)
    text = NAV_TITLE_RE.sub(replace_nav, text)
    text = META_DESC_RE.sub(replace_meta, text)

    if n:
        p.write_text(text, encoding="utf-8")
    return n


def main():
    n_files = total = 0
    for p in sorted(ROOT.rglob("*.html")):
        if set(p.parts) & SKIP:
            continue
        n = fix(p)
        if n:
            n_files += 1
            total += n
            print(f"  + {p.relative_to(ROOT)}: {n} amp fixes")
    print(f"\nFiles touched: {n_files}, ampersand fixes: {total}")


if __name__ == "__main__":
    main()
