"""Wave 93: Drop the stray <h2 id="key-takeaways">[emoji] Key Takeaways</h2>
that lives INSIDE a <div class="callout key-takeaway"> right after the
canonical <div class="callout-title">Key Takeaways</div>.

The double header (callout-title + inner h2) produces:
  ICON Key Takeaways
  ICON ✅ Key Takeaways  <- the duplicate

Drop the inner h2 so only the canonical callout-title remains. The pattern
covers 9 files identified across the book.
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
SKIP = {".git", "node_modules", "KDP", "build", "source_fix_backups",
        "pagefind", ".book-update", "vendor", ".claude", "_archive",
        "agents", "templates", "docs", "scripts"}

# Match the pattern:
#   <div class="callout key-takeaway">
#   <div class="callout-title">Key Takeaways[...]</div>
#   <h2 id="key-takeaways">[optional emoji+space] Key Takeaways</h2>
#
# Replace with just the callout open + callout-title (drop the inner h2).
PATTERN = re.compile(
    r'(<div\s+class="callout\s+key-takeaway"[^>]*>\s*'
    r'<div\s+class="callout-title"[^>]*>[^<]*</div>\s*)'
    r'<h2\s+id="key-takeaways"[^>]*>[^<]*</h2>\s*',
    re.IGNORECASE,
)

# Some files use <h2 id="X-Y-Z-key-takeaways"> (section-numbered ids).
PATTERN_NUMBERED = re.compile(
    r'(<div\s+class="callout\s+key-takeaway"[^>]*>\s*'
    r'<div\s+class="callout-title"[^>]*>[^<]*</div>\s*)'
    r'<h2\s+id="[0-9-]*key-takeaways"[^>]*>[^<]*</h2>\s*',
    re.IGNORECASE,
)


def fix_file(p: Path) -> int:
    text = p.read_text(encoding="utf-8")
    new, n1 = PATTERN.subn(r'\1', text)
    new, n2 = PATTERN_NUMBERED.subn(r'\1', new)
    n = n1 + n2
    if n == 0:
        return 0
    p.write_text(new, encoding="utf-8")
    return n


def main():
    n_files = 0
    n_total = 0
    for p in sorted(ROOT.rglob("*.html")):
        if set(p.parts) & SKIP:
            continue
        n = fix_file(p)
        if n:
            n_files += 1
            n_total += n
            print(f"  + {p.relative_to(ROOT)}: {n} double-header(s) dropped")
    print(f"\nFiles touched: {n_files}, headers dropped: {n_total}")


if __name__ == "__main__":
    main()
