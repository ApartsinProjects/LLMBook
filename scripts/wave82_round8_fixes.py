"""Wave 82: Round-8 fixes for user feedback 2026-05-18 cont.

1. Empty callouts: <div class="callout TYPE"><div class="callout-title">X</div></div>
   with NO body content. Drop them (they render as empty boxes).
2. Chapter card title clickable: <div class="chapter-card-header"> on part
   index pages should be a link to that chapter's index.html.
3. Figure 3.3.2 + similar: diagram-caption present but the underlying
   image/SVG may have a key-idea annotation that should consolidate.
   This is per-file work; we just flag here.
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'.git', 'node_modules', 'KDP', 'build', 'source_fix_backups',
        'pagefind', '.book-update', 'vendor', '.claude', '_archive',
        'agents', 'templates', 'docs', 'scripts'}

# 1. Empty callout: <div class="callout TYPE"><div class="callout-title">...</div></div>
#    with optional whitespace between. Strict: no <p>, <ul>, <ol>, <details>,
#    <div>, <pre>, <table>, <figure>, <span>(text)>, or any other element
#    besides the title.
EMPTY_CALLOUT_RE = re.compile(
    r'<div\s+class="callout\s+[a-z-]+"[^>]*>\s*'
    r'<div\s+class="callout-title"[^>]*>[^<]+</div>\s*'
    r'</div>\s*\n?',
    re.IGNORECASE,
)

# 2. Chapter card header: <div class="chapter-card-header"><span class="mod-num">Chapter N</span> TITLE</div>
#    Convert to: <a class="chapter-card-header" href="module-NN-*/index.html"><span class="mod-num">Chapter N</span> TITLE</a>
CHAPTER_HEADER_RE = re.compile(
    r'<div\s+class="chapter-card-header">'
    r'(<span\s+class="mod-num">Chapter\s+\d+</span>)\s*'
    r'([^<]+)'
    r'</div>',
    re.IGNORECASE,
)


def is_part_index(p: Path) -> bool:
    return p.name == 'index.html' and any(
        part.startswith('part-') for part in p.parts[:-1]
    ) and not any(part.startswith('module-') for part in p.parts)


def fix_empty_callouts(text: str) -> tuple[str, int]:
    new, n = EMPTY_CALLOUT_RE.subn('', text)
    return new, n


def fix_chapter_cards(text: str, p: Path) -> tuple[str, int]:
    """Convert <div class="chapter-card-header"> to <a class="chapter-card-header" href="">.

    The href is the module's index.html. We look at the FOLLOWING
    <a href="module-NN-*/section-X.Y.html"> in the same .chapter-card to
    derive the module path.
    """
    n = 0

    def repl(m: re.Match) -> str:
        nonlocal n
        prefix = m.group(0)
        # Find the next <a href="module-NN-*/..."> in the surrounding text
        # to extract the module dir.
        # The card-header is followed by .chapter-card-body containing section links.
        # Find the position of m in text and scan forward up to 2000 chars for first <a href>
        return prefix  # placeholder; we'll do positional rewrite below

    # Iterate matches with positional context
    out = []
    pos = 0
    for m in CHAPTER_HEADER_RE.finditer(text):
        out.append(text[pos:m.start()])
        # Find the next <a href="module-NN-*/.../section-...">
        scan_to = min(len(text), m.end() + 2000)
        href_m = re.search(r'<a\s+href="(module-\d+[^/]*)/(?:section-[^"]+|index\.html)"', text[m.end():scan_to])
        if href_m:
            mod_dir = href_m.group(1)
            new_href = f'{mod_dir}/index.html'
            mod_num = m.group(1)
            title = m.group(2).strip()
            new_block = (
                f'<a class="chapter-card-header" href="{new_href}">'
                f'{mod_num} {title}</a>'
            )
            out.append(new_block)
            n += 1
        else:
            out.append(m.group(0))
        pos = m.end()
    out.append(text[pos:])
    return ''.join(out), n


def main():
    n_empty = 0
    n_cards = 0
    files = 0
    for p in sorted(ROOT.rglob('*.html')):
        if set(p.parts) & SKIP:
            continue
        text = p.read_text(encoding='utf-8')
        orig = text

        # 1. Empty callouts (all pages)
        text, ne = fix_empty_callouts(text)
        n_empty += ne

        # 2. Chapter card title clickable (part index pages only)
        if is_part_index(p):
            text, nc = fix_chapter_cards(text, p)
            n_cards += nc

        if text != orig:
            p.write_text(text, encoding='utf-8')
            files += 1

    print(f'Empty callouts removed: {n_empty}')
    print(f'Chapter-card headers made clickable: {n_cards}')
    print(f'Files touched: {files}')


if __name__ == '__main__':
    main()
