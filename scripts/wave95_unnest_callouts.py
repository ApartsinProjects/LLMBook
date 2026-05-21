"""Wave 95: Unnest WRONG_NESTING violations by moving the inner callout
OUT of its outer callout (placed AFTER the outer's closing tag).

Pattern detected by p1_wrong_nesting.py:
  <div class="callout OUTER">
    <div class="callout-title">...</div>
    <p>...</p>
    <div class="callout INNER">     <-- nested
      <div class="callout-title">...</div>
      <p>...</p>
    </div>
  </div>

becomes:
  <div class="callout OUTER">
    <div class="callout-title">...</div>
    <p>...</p>
  </div>
  <div class="callout INNER">
    <div class="callout-title">...</div>
    <p>...</p>
  </div>

Conservative: only handles ONE nested callout per outer; only when the
inner is the LAST child of the outer (so unwrapping doesn't leave a gap
in the middle of the outer's content).
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
SKIP = {".git", "node_modules", "KDP", "build", "source_fix_backups",
        "pagefind", ".book-update", "vendor", ".claude", "_archive",
        "agents", "templates", "docs", "scripts"}

OUTER_OPEN_RE = re.compile(
    r'<div\s+class="callout\s+([a-z-]+)"[^>]*>',
    re.IGNORECASE,
)


def _find_div_close(html: str, after_open: int) -> int:
    """Return index just after the matching </div> for a div opened at after_open."""
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
            # Find the closing >
            gt = html.find(">", pos)
            return gt + 1 if gt > 0 else pos
    return -1


def _find_div_close_start(html: str, after_open: int) -> int:
    """Return start index of the matching </div> tag."""
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
            return m.start()
    return -1


def fix_file(p: Path) -> int:
    text = p.read_text(encoding="utf-8")
    if 'class="callout' not in text:
        return 0
    out = []
    pos = 0
    n = 0
    for m in OUTER_OPEN_RE.finditer(text):
        if m.start() < pos:
            continue
        outer_type = m.group(1).lower()
        outer_body_start = m.end()
        outer_close_start = _find_div_close_start(text, outer_body_start)
        if outer_close_start < 0:
            continue
        body = text[outer_body_start:outer_close_start]
        # Find an inner <div class="callout ..."> in body
        inner_m = OUTER_OPEN_RE.search(body)
        if not inner_m:
            continue
        inner_type = inner_m.group(1).lower()
        inner_open_start_in_body = inner_m.start()
        inner_open_end_in_body = inner_m.end()
        # Find the matching </div> for inner
        inner_close_end_in_body = _find_div_close(body, inner_open_end_in_body)
        if inner_close_end_in_body < 0:
            continue
        # Check: is inner the LAST content in outer? (only whitespace after it)
        trailing = body[inner_close_end_in_body:].strip()
        if trailing:
            continue
        # Good. Extract inner block, rebuild outer without it.
        inner_block = body[inner_open_start_in_body:inner_close_end_in_body]
        outer_before_inner = body[:inner_open_start_in_body].rstrip() + "\n"
        # New layout: outer (without inner) </div> THEN inner </div>
        outer_open_tag = text[m.start():outer_body_start]
        outer_close_tag = "</div>"  # standard
        new_outer = outer_open_tag + outer_before_inner + outer_close_tag
        new_blocks = new_outer + "\n" + inner_block
        # Replace from m.start() to outer_close_start + len("</div>")
        outer_end = outer_close_start + len("</div>")
        out.append(text[pos:m.start()])
        out.append(new_blocks)
        pos = outer_end
        n += 1
    if n == 0:
        return 0
    out.append(text[pos:])
    new = "".join(out)
    p.write_text(new, encoding="utf-8")
    return n


def main():
    n_files = 0
    n_total = 0
    for p in sorted(ROOT.rglob("*.html")):
        if set(p.parts) & SKIP:
            continue
        if not (p.name.startswith("section-") or p.name == "index.html"):
            continue
        n = fix_file(p)
        if n:
            n_files += 1
            n_total += n
            print(f"  + {p.relative_to(ROOT)}: {n} callout(s) unnested")
    print(f"\nFiles touched: {n_files}, callouts unnested: {n_total}")


if __name__ == "__main__":
    main()
