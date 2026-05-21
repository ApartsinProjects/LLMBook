"""Wave 50: Add <a href> to What's Next blocks that lack one.

For each whats-next block:
  1. Extract the chapter-nav's <a class="next" href="..."> link
  2. Find the section number and title from the nav's nav-num + nav-title spans
  3. Inject a "Continue to <a href='...'>Section X.Y: Title</a>" sentence into
     the whats-next paragraph (or as a new paragraph if none exists)
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'.git', 'node_modules', 'KDP', 'build', 'source_fix_backups',
        'pagefind', '.book-update', 'vendor', '.claude', '_archive',
        'agents', 'templates', 'docs', 'scripts'}

# Match the canonical whats-next callout (or div, older variant)
WHATS_NEXT_BLOCK_RE = re.compile(
    r'(<div\s+class="(?:callout whats-next|whats-next)"[^>]*>.*?</div>)',
    re.DOTALL | re.IGNORECASE,
)
# Sometimes the block is just <div class="whats-next">...</div> (older form)

# Chapter-nav next link
NEXT_LINK_RE = re.compile(
    r'<a\s+class="next"\s+href="([^"]+)"[^>]*>'
    r'(?:.*?<span\s+class="nav-num">([^<]+)</span>\s*)?'
    r'(?:<span\s+class="nav-title">([^<]+)</span>)?',
    re.DOTALL | re.IGNORECASE,
)

# Detect if the whats-next block already has any <a href> link
HAS_HREF_RE = re.compile(r'<a\s+[^>]*href=', re.IGNORECASE)


def fix_file(p: Path) -> int:
    text = p.read_text(encoding='utf-8')
    orig = text
    n = 0

    # Get the chapter-nav next link
    nxt_m = NEXT_LINK_RE.search(text)
    if not nxt_m:
        return 0
    href = nxt_m.group(1)
    nav_num = (nxt_m.group(2) or '').strip()  # e.g. "Section 44.4"
    nav_title = (nxt_m.group(3) or '').strip()  # e.g. "Post-Launch Monitoring..."
    if not nav_num and not nav_title:
        return 0
    link_label = f'{nav_num}: {nav_title}' if (nav_num and nav_title) else (nav_num or nav_title)

    def replace_block(m: re.Match) -> str:
        nonlocal n
        block = m.group(1)
        if HAS_HREF_RE.search(block):
            return block
        # Inject link into the last <p>...</p> in the block, or add a new <p>
        # Find the last </p> before </div>
        end_div = block.rfind('</div>')
        last_p_close = block.rfind('</p>', 0, end_div)
        new_sentence = f' Continue to <a href="{href}">{link_label}</a>.'
        if last_p_close != -1:
            # Inject sentence before </p>
            new_block = (
                block[:last_p_close]
                + new_sentence
                + block[last_p_close:]
            )
        else:
            # No <p> inside — add a new one
            new_p = f'\n<p>Continue to <a href="{href}">{link_label}</a>.</p>\n'
            new_block = block[:end_div] + new_p + block[end_div:]
        n += 1
        return new_block

    new_text = WHATS_NEXT_BLOCK_RE.sub(replace_block, text)
    if new_text != orig:
        p.write_text(new_text, encoding='utf-8')
    return n


def main():
    n_total = 0
    files_touched = 0
    for p in sorted(ROOT.rglob('*.html')):
        if set(p.parts) & SKIP:
            continue
        n = fix_file(p)
        if n > 0:
            n_total += n
            files_touched += 1
    print(f'whats-next links added: {n_total}')
    print(f'Files touched: {files_touched}')


if __name__ == '__main__':
    main()
