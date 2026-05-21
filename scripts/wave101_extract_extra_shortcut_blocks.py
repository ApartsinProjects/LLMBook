"""Wave 101: Extract non-primary code-block-wrappers from library-shortcut.

A library-shortcut is supposed to demonstrate ONE library call in a
single focused snippet. The audit flags shortcuts with 2+
code-block-wrappers. Investigation across the 6 flagged files shows
the secondary blocks are always cases where unrelated material got
absorbed by accident (a comparison demo, a pseudocode algorithm, a
duplicate of code that lives elsewhere in the section).

This script keeps the FIRST code-block-wrapper inside the shortcut
and moves any subsequent ones OUT, placing them right after the
shortcut's closing tag. The visual result: shortcut shows its
focused 8-line snippet under "Show code"; the extra blocks render
as normal code blocks below the callout.

We do NOT delete content. Authors can re-home the extracted blocks
into their natural section position in a follow-up pass.
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
SKIP = {".git", "node_modules", "KDP", "build", "source_fix_backups",
        "pagefind", ".book-update", "vendor", ".claude", "_archive",
        "agents", "templates", "docs", "scripts"}

LIB_OPEN_RE = re.compile(
    r'<div\s+class="callout\s+library-shortcut"[^>]*>',
    re.IGNORECASE,
)


def _matching_div_end(text: str, after_open: int) -> int:
    """Return position AFTER matching </div>. Depth-aware."""
    open_re = re.compile(r'<div\b', re.IGNORECASE)
    close_re = re.compile(r'</div>', re.IGNORECASE)
    depth = 1
    pos = after_open
    while depth > 0 and pos < len(text):
        no = open_re.search(text, pos)
        nc = close_re.search(text, pos)
        if not nc:
            return -1
        if no and no.start() < nc.start():
            depth += 1
            pos = no.end()
        else:
            depth -= 1
            pos = nc.end()
    return pos if depth == 0 else -1


def _find_codeblock_block(text: str, start: int) -> tuple[int, int] | None:
    """Locate the next <div class="code-block-wrapper">...</div> block
    inside text[start:]. Return (block_start, block_end_excl)."""
    m = re.search(
        r'<div\s+class="code-block-wrapper"[^>]*>',
        text[start:],
        re.IGNORECASE,
    )
    if not m:
        return None
    block_start = start + m.start()
    after_open = start + m.end()
    end = _matching_div_end(text, after_open)
    if end < 0:
        return None
    return block_start, end


def fix_file(p: Path) -> int:
    text = p.read_text(encoding="utf-8")
    if 'class="callout library-shortcut"' not in text:
        return 0
    n_extractions = 0
    # Re-scan after each fix because positions shift.
    max_iter = 30
    for _ in range(max_iter):
        m = LIB_OPEN_RE.search(text)
        # We need to find the FIRST library-shortcut that still has 2+ blocks
        found = None
        for m in LIB_OPEN_RE.finditer(text):
            ls_body_start = m.end()
            ls_end = _matching_div_end(text, ls_body_start)
            if ls_end < 0:
                continue
            body = text[ls_body_start:ls_end]
            n_blocks = len(re.findall(
                r'<div\s+class="code-block-wrapper"', body, re.IGNORECASE,
            ))
            if n_blocks >= 2:
                found = (m.start(), ls_body_start, ls_end)
                break
        if not found:
            break
        ls_start, ls_body_start, ls_end = found
        body = text[ls_body_start:ls_end]
        # Locate the FIRST code-block-wrapper inside body
        first_loc = _find_codeblock_block(body, 0)
        if not first_loc:
            break
        first_block_end_in_body = first_loc[1]
        # Locate the SECOND code-block-wrapper inside body
        second_loc = _find_codeblock_block(body, first_block_end_in_body)
        if not second_loc:
            break
        second_block_start_in_body, second_block_end_in_body = second_loc

        # Extract the second block (we will move it OUT of the shortcut)
        extracted = body[second_block_start_in_body:second_block_end_in_body]
        # Body without the extracted block
        new_body = (
            body[:second_block_start_in_body].rstrip()
            + "\n"
            + body[second_block_end_in_body:].lstrip()
        )
        # The shortcut closes at the </div> right before ls_end.
        # ls_end is position AFTER the closing </div>. We insert
        # `extracted` right after ls_end.
        new_text = (
            text[:ls_body_start]
            + new_body
            + text[ls_end - 0:ls_end]  # noop: positions
        )
        # Construct: text up to ls_body_start, new_body, the closing
        # </div> + post-shortcut prelude... but body already drops
        # the trailing newline of inner. Easier: rebuild by full slice
        # arithmetic with ls_start.
        # Use: full text reconstruction
        new_text = (
            text[:ls_body_start]
            + new_body
            + text[ls_end - len("</div>"):ls_end]
            + "\n"
            + extracted
            + "\n"
            + text[ls_end:]
        )
        # But the above inserts the closing </div> twice. Let me just
        # split clean: take everything UP TO the </div> close, then
        # append the closing </div>, then the extracted block, then
        # the rest.
        # Easier approach: rebuild the whole library-shortcut
        ls_open_tag = text[ls_start:ls_body_start]
        rebuilt = ls_open_tag + new_body + "</div>"
        new_text = (
            text[:ls_start]
            + rebuilt
            + "\n"
            + extracted
            + "\n"
            + text[ls_end:]
        )
        text = new_text
        n_extractions += 1
    if n_extractions == 0:
        return 0
    p.write_text(text, encoding="utf-8")
    return n_extractions


def main():
    n_files = n_total = 0
    for p in sorted(ROOT.rglob("section-*.html")):
        if set(p.parts) & SKIP:
            continue
        n = fix_file(p)
        if n:
            n_files += 1
            n_total += n
            print(f"  + {p.relative_to(ROOT)}: extracted {n} block(s)")
    print(f"\nFiles touched: {n_files}, extractions: {n_total}")


if __name__ == "__main__":
    main()
