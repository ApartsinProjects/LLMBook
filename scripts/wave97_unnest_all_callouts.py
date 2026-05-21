"""Wave 97: Comprehensive unnest of WRONG_NESTING violations.

Wave 95 only handled inner callouts at the TRAILING position of the
outer. This wave handles ALL nested-callout cases by extracting the
inner OUT of the outer and placing it AFTER the outer's closing tag.

Before:
  <div class="callout OUTER">
    <div class="callout-title">Outer</div>
    <p>A</p>
    <div class="callout INNER">         <-- nested, middle position
      <div class="callout-title">Inner</div>
      <p>X</p>
    </div>
    <p>B</p>
  </div>

After:
  <div class="callout OUTER">
    <div class="callout-title">Outer</div>
    <p>A</p>
    <p>B</p>
  </div>
  <div class="callout INNER">
    <div class="callout-title">Inner</div>
    <p>X</p>
  </div>

The outer keeps all its content except the inner. The inner moves out
to a flat sibling position. This eliminates the double-background
visual without losing content; authors can edit the prose flow later
if the inner needs to land in a specific spot.
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
    r'<div\s+class="callout\s+([a-z-]+)"[^>]*>', re.IGNORECASE
)


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

    n_fixes = 0
    # Loop because each fix changes positions; restart from beginning.
    max_iter = 50
    iteration = 0
    while iteration < max_iter:
        iteration += 1
        # Find every outer callout
        found_one = False
        for m in OUTER_OPEN_RE.finditer(text):
            outer_open_start = m.start()
            outer_body_start = m.end()
            outer_close_start = _find_div_close_start(text, outer_body_start)
            if outer_close_start < 0:
                continue
            outer_body = text[outer_body_start:outer_close_start]
            # Find an inner callout open within the body
            inner_m = OUTER_OPEN_RE.search(outer_body)
            if not inner_m:
                continue
            inner_open_start_in_body = inner_m.start()
            inner_open_end_in_body = inner_m.end()
            inner_close_start_in_body = _find_div_close_start(
                outer_body, inner_open_end_in_body
            )
            if inner_close_start_in_body < 0:
                continue
            inner_close_end_in_body = inner_close_start_in_body + len("</div>")

            # Inner block (full)
            inner_block = outer_body[
                inner_open_start_in_body:inner_close_end_in_body
            ]

            # Outer body without the inner
            new_outer_body = (
                outer_body[:inner_open_start_in_body].rstrip()
                + "\n"
                + outer_body[inner_close_end_in_body:].lstrip()
            )

            # Reconstruct outer block
            outer_open_tag = text[outer_open_start:outer_body_start]
            new_outer = outer_open_tag + new_outer_body + "</div>"

            # Replace: outer (containing inner) -> new_outer + \n + inner
            outer_end = outer_close_start + len("</div>")
            text = (
                text[:outer_open_start]
                + new_outer
                + "\n"
                + inner_block
                + text[outer_end:]
            )
            n_fixes += 1
            found_one = True
            break  # restart scan
        if not found_one:
            break

    if n_fixes == 0:
        return 0
    p.write_text(text, encoding="utf-8")
    return n_fixes


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
            print(f"  + {p.relative_to(ROOT)}: {n} callout(s) extracted")
    print(f"\nFiles touched: {n_files}, callouts extracted: {n_total}")


if __name__ == "__main__":
    main()
