"""Wave 90: Unwrap the legacy <div class="takeaways"> wrapper around
<div class="callout key-takeaway">.

Historically the book used .takeaways (with its own teal-gradient background)
to wrap a sub-callout. Now that .callout.key-takeaway is the canonical
callout class with its own complete styling, the outer .takeaways wrapper
creates a DOUBLE-BACKGROUND visual: a teal box containing another teal box
with its own border. Unwrap the outer.

Pattern (whitespace-tolerant):
  <div class="takeaways">
  <div class="callout key-takeaway">
  ...content...
  </div>
  </div>

becomes:
  <div class="callout key-takeaway">
  ...content...
  </div>

Some files have content INSIDE .takeaways but no inner callout (legacy
.takeaways-styled content). For those we KEEP the outer .takeaways and do
NOT unwrap; the script only acts on the nested-callout pattern.
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
SKIP = {".git", "node_modules", "KDP", "build", "source_fix_backups",
        "pagefind", ".book-update", "vendor", ".claude", "_archive",
        "agents", "templates", "docs", "scripts"}

# Find balanced <div class="takeaways"> that contains a <div class="callout
# key-takeaway"> as its only top-level child (modulo whitespace).
OPEN_TAKEAWAYS = re.compile(r'<div\s+class="takeaways"\s*>\s*', re.IGNORECASE)


def find_div_close(html: str, open_pos: int, after_open: int) -> int:
    """Given position right after a <div...> opening tag, find matching </div>."""
    depth = 1
    pos = after_open
    tag_re = re.compile(r'<(/?)div\b', re.IGNORECASE)
    while pos < len(html) and depth > 0:
        m = tag_re.search(html, pos)
        if not m:
            return -1
        if m.group(1) == "/":
            depth -= 1
        else:
            depth += 1
        pos = m.end()
        if depth == 0:
            # Find the closing > of this </div>
            gt = html.find(">", pos)
            return gt + 1 if gt > 0 else pos
    return -1


def unwrap_takeaways_in(html: str) -> tuple[str, int]:
    """Returns (new_html, n_unwrapped)."""
    out = []
    pos = 0
    n = 0
    while True:
        m = OPEN_TAKEAWAYS.search(html, pos)
        if not m:
            break
        # Locate the matching </div> for the outer .takeaways
        outer_end = find_div_close(html, m.start(), m.end())
        if outer_end < 0:
            break
        # The body between m.end() and the </div> token start
        # Find the last </div> position (just before outer_end)
        body_end = html.rfind("</div>", m.end(), outer_end)
        if body_end < 0:
            break
        inner = html[m.end():body_end].strip()
        # Check if inner is essentially ONE <div class="callout key-takeaway">
        # wrapper with optional surrounding whitespace.
        inner_open_m = re.match(
            r'<div\s+class="callout\s+key-takeaway"[^>]*>',
            inner, re.IGNORECASE,
        )
        if not inner_open_m:
            # Not the nested-callout pattern; skip
            out.append(html[pos:outer_end])
            pos = outer_end
            continue
        # Find the matching </div> of the inner callout
        after_inner_open = inner_open_m.end()
        inner_close = find_div_close(inner, 0, after_inner_open)
        if inner_close < 0:
            out.append(html[pos:outer_end])
            pos = outer_end
            continue
        # Confirm only whitespace AFTER the inner </div>
        trailing = inner[inner_close:].strip()
        if trailing:
            # There's other content beside the callout; keep wrapper
            out.append(html[pos:outer_end])
            pos = outer_end
            continue
        # Good. Replace the whole outer wrapper with just the inner callout.
        out.append(html[pos:m.start()])
        out.append(inner[:inner_close])
        pos = outer_end
        n += 1
    out.append(html[pos:])
    return "".join(out), n


def main():
    n_files = 0
    n_total = 0
    for p in sorted(ROOT.rglob("*.html")):
        if set(p.parts) & SKIP:
            continue
        text = p.read_text(encoding="utf-8")
        if '<div class="takeaways">' not in text:
            continue
        new, n = unwrap_takeaways_in(text)
        if n == 0:
            continue
        p.write_text(new, encoding="utf-8")
        n_files += 1
        n_total += n
        print(f"  + {p.relative_to(ROOT)}: {n} unwrap(s)")
    print(f"\nFiles touched: {n_files}, wrappers unwrapped: {n_total}")


if __name__ == "__main__":
    main()
