"""v766: Targeted fix of Part-index chapter cards using on-disk truth.

The audit found Part index pages encode an OLD proposed renumbering
that was never applied. We fix:
  1. Each chapter-card-header `Chapter NN` label (canonical zero-pad).
  2. Each chapter-card-header chapter-title text (matches module h1).
  3. Each `<li>` section-list entry: sec-num and section title text
     come from the actual section-N.M.html files in document order.
  4. The href on each `<li>` always points at the actual existing file.

Preserves: the descriptive `<p>` paragraph for each chapter, the
Part header, the part-overview, the big-picture callout, the nav,
the footer, and any custom callouts.

Strategy: find every <div class="chapter-card"> ... </div></div> pair
in document order. Match them to module-NN-* dirs in document order
(both already 1:1). For each card:
  - Replace its <div class="chapter-card-header">...</div> with the
    canonical header.
  - Find the <ul class="section-list">...</ul> inside and replace
    with one <li> per actual section-N.M.html in chapter-number order.
If the card count doesn't match the module count, replace surplus
phantom cards or add a new card per missing module.

Idempotent.
"""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent


def read_h1(path: Path) -> str:
    if not path.exists():
        return ''
    s = path.read_text(encoding='utf-8')
    m = re.search(r'<h1[^>]*>([^<]+)</h1>', s)
    if not m:
        return ''
    text = m.group(1).strip()
    text = re.sub(r'^Chapter\s+\d+:\s*', '', text)
    text = re.sub(r'^\d+\.\d+:?\s*', '', text)
    return text  # leave HTML entities as-is


def chapter_num(p: Path) -> int:
    m = re.match(r'module-(\d+)', p.name)
    return int(m.group(1)) if m else 0


def section_num(f: Path) -> tuple[int, int]:
    m = re.match(r'section-(\d+)\.(\d+)\.html', f.name)
    return (int(m.group(1)), int(m.group(2))) if m else (0, 0)


def build_card_header(module_dir: Path) -> str:
    n = chapter_num(module_dir)
    title = read_h1(module_dir / 'index.html') or module_dir.name
    return (f'        <div class="chapter-card-header">\n'
            f'            <span class="mod-num">Chapter {n:02d}</span> '
            f'{title}\n'
            f'        </div>')


def build_section_list(module_dir: Path) -> str:
    sections = sorted(module_dir.glob('section-*.html'), key=section_num)
    if not sections:
        return '            <ul class="section-list"></ul>'
    lis = []
    for sf in sections:
        n, m = section_num(sf)
        title = read_h1(sf) or sf.stem
        href = f'{module_dir.name}/{sf.name}'
        lis.append(f'                <li><a href="{href}">'
                   f'<span class="sec-num">{n}.{m}</span> {title}</a></li>')
    return ('            <ul class="section-list">\n'
            + '\n'.join(lis)
            + '\n            </ul>')


CARD_RE = re.compile(
    r'(\s*<div class="chapter-card">.*?</div>\s*</div>)',
    re.DOTALL)
HEADER_RE = re.compile(
    r'<div class="chapter-card-header">.*?</div>', re.DOTALL)
SECTION_LIST_RE = re.compile(
    r'<ul class="section-list">.*?</ul>', re.DOTALL)


def fix_one_part(part_dir: Path) -> tuple[bool, int]:
    idx = part_dir / 'index.html'
    if not idx.exists():
        return False, 0
    s = idx.read_text(encoding='utf-8')
    cards = CARD_RE.findall(s)
    modules = sorted(
        [d for d in part_dir.iterdir()
         if d.is_dir() and d.name.startswith('module-')],
        key=chapter_num)

    if not modules:
        return False, 0

    # Strategy: rebuild each card by patching header and section-list.
    # If there are more cards than modules, drop the surplus.
    # If there are more modules than cards, append new fully-built cards.
    new_s = s
    fixes = 0

    # First, replace each existing card 1:1 with the matching module
    matched = list(zip(cards, modules))
    for old_card, mod in matched:
        new_card = old_card
        # Patch header
        new_card = HEADER_RE.sub(
            build_card_header(mod).lstrip(), new_card, count=1)
        # Patch section list
        new_card = SECTION_LIST_RE.sub(
            build_section_list(mod).lstrip(), new_card, count=1)
        if new_card != old_card:
            new_s = new_s.replace(old_card, new_card, 1)
            fixes += 1

    # Drop surplus cards (more cards than modules)
    surplus = cards[len(modules):]
    for sc in surplus:
        new_s = new_s.replace(sc, '', 1)
        fixes += 1
        print(f'    [drop phantom card] {part_dir.name}')

    # Append new cards for modules that lacked a card slot
    extras = modules[len(cards):]
    if extras:
        # Build full new cards (with placeholder description)
        new_cards_html = '\n\n'.join(
            f'    <div class="chapter-card">\n'
            f'{build_card_header(m)}\n'
            f'        <div class="chapter-card-body">\n'
            f'            <p><a href="{m.name}/index.html">'
            f'Read Chapter {chapter_num(m):02d} &rarr;</a></p>\n'
            f'{build_section_list(m)}\n'
            f'        </div>\n'
            f'    </div>'
            for m in extras
        )
        # Insert before the whats-next or chapter-nav
        anchor = '<div class="whats-next">' if '<div class="whats-next">' in new_s \
            else '<nav class="chapter-nav">'
        new_s = new_s.replace(
            anchor,
            new_cards_html + '\n\n' + anchor, 1)
        fixes += len(extras)
        print(f'    [add {len(extras)} cards] {part_dir.name}')

    if new_s != s:
        idx.write_text(new_s, encoding='utf-8')
        return True, fixes
    return False, 0


def main() -> int:
    parts = sorted(
        [d for d in ROOT.iterdir()
         if d.is_dir() and d.name.startswith('part-')],
        key=lambda d: int(re.search(r'part-(\d+)', d.name).group(1)))
    total_fixes = 0
    n_changed = 0
    for p in parts:
        changed, fixes = fix_one_part(p)
        if changed:
            n_changed += 1
            total_fixes += fixes
            print(f'  [{p.name}] {fixes} fixes')
    print(f'\nfixed: {n_changed} / {len(parts)} part indexes; '
          f'{total_fixes} card patches')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
