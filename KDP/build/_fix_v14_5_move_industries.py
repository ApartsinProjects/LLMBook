"""v14.5: Move industry appendices to a new Part XII.

Restructuring:
  BEFORE: appendices/appendix-W-legal-llms/index.html  (Appendix W)
           appendices/appendix-X-finance-llms/index.html (Appendix X)
           ... appendices/appendix-AC-manufacturing-llms/  (Appendix AC)

  AFTER:  part-12-llm-applications-across-industries/
           index.html  (Part XII landing)
           module-36-legal-llms/index.html
           module-37-finance-llms/index.html
           module-38-healthcare-llms/index.html
           module-39-education-llms/index.html
           module-40-cybersecurity-llms/index.html
           module-41-government-llms/index.html
           module-42-manufacturing-llms/index.html

Rationale: these are industry-specific application chapters, not
reference appendices. They belong in the main reading path.

Updates:
  - Each moved file: 'Appendix W' → 'Chapter 36', section navigation
  - toc.html: remove rows from appendices, add Part XII rows
  - appendices/index.html: remove industry cards
  - Navigation chain:
    part-11/.../35.4.next → part-12/index
    part-12/index → module-36 → ... → module-42 → appendices/index
  - appendix-V/v.3.next: → appendix-AD (skip industries)
  - appendix-AD/index.prev: → module-42

Run --apply to write changes.
"""
from pathlib import Path
from bs4 import BeautifulSoup
import os
import re
import shutil
import sys

ROOT = Path(__file__).resolve().parents[2]

# Migration map: (old_appendix_dir, new_module_dir, chapter_num, appendix_letter)
MIGRATION = [
    ('appendix-w-legal-llms',           'module-36-legal-llms',           36, 'W'),
    ('appendix-x-finance-llms',         'module-37-finance-llms',         37, 'X'),
    ('appendix-y-healthcare-llms',      'module-38-healthcare-llms',      38, 'Y'),
    ('appendix-z-education-llms',       'module-39-education-llms',       39, 'Z'),
    ('appendix-aa-cybersecurity-llms',  'module-40-cybersecurity-llms',   40, 'AA'),
    ('appendix-ab-government-llms',     'module-41-government-llms',      41, 'AB'),
    ('appendix-ac-manufacturing-llms',  'module-42-manufacturing-llms',   42, 'AC'),
]

NEW_PART_DIR = 'part-12-llm-applications-across-industries'


def step(label):
    print(f'\n>>> {label}')


def move_dirs(dry):
    src_base = ROOT / 'appendices'
    dst_base = ROOT / NEW_PART_DIR
    if not dst_base.exists() and not dry:
        dst_base.mkdir(parents=True)
    for old, new, _ch, _letter in MIGRATION:
        src = src_base / old
        dst = dst_base / new
        if not src.exists():
            print(f'  SKIP (missing): {old}')
            continue
        if dst.exists():
            print(f'  SKIP (exists): {new}')
            continue
        if not dry:
            shutil.copytree(src, dst)
        print(f'  copied: appendices/{old} -> {NEW_PART_DIR}/{new}')


def update_moved_files_internal(dry):
    """For each newly-copied file, update internal markup:
       - Header 'Appendix W' -> 'Chapter 36'
       - <title>, <description>, <h1> etc
    """
    for old, new, ch, letter in MIGRATION:
        f = ROOT / NEW_PART_DIR / new / 'index.html'
        if not f.exists():
            print(f'  SKIP (missing dst): {new}')
            continue
        t = f.read_text(encoding='utf-8')
        # Map "Appendix W" -> "Chapter 36" (in title, headers, body)
        new_t = re.sub(
            rf'\bAppendix\s+{letter}\b',
            f'Chapter {ch}',
            t
        )
        # Map old appendix paths to new module paths (for sibling links)
        for o2, n2, _, _ in MIGRATION:
            new_t = new_t.replace(f'../{o2}/', f'../{n2}/')
        # Update path prefix: was 2 levels deep from `appendices/appendix-X/`,
        # new is 2 levels from `part-12-.../module-X/` — same depth, no change
        # for `../../...` paths.
        if new_t != t and not dry:
            f.write_text(new_t, encoding='utf-8')
            print(f'  updated internal markup: {new}/index.html')


def update_internal_nav(dry):
    """Set sequential nav: module-36 → module-37 → ... → module-42 → appendices/index.
       module-36.prev → part-12/index.
       part-12/index.prev → part-11/35.4. .next → module-36."""
    for i, (_old, new, ch, _l) in enumerate(MIGRATION):
        f = ROOT / NEW_PART_DIR / new / 'index.html'
        if not f.exists():
            continue
        s = BeautifulSoup(f.read_text(encoding='utf-8'), 'html.parser')
        nav = s.find('nav', class_='chapter-nav')
        if not nav:
            continue

        # prev
        prev = nav.find('a', class_='prev')
        if prev:
            if i == 0:
                # First industry — prev is the part landing
                prev['href'] = '../index.html'
                prev.clear()
                prev.append('← Part XII Landing')
            else:
                _, prev_dir, prev_ch, _ = MIGRATION[i - 1]
                prev['href'] = f'../{prev_dir}/index.html'
                prev.clear()
                prev.append(f'← Chapter {prev_ch}')

        # next
        nxt = nav.find('a', class_='next')
        if nxt:
            if i == len(MIGRATION) - 1:
                # Last industry — next is appendices/index
                nxt['href'] = '../../appendices/index.html'
                nxt.clear()
                nxt.append('Appendices →')
            else:
                _, next_dir, next_ch, _ = MIGRATION[i + 1]
                nxt['href'] = f'../{next_dir}/index.html'
                nxt.clear()
                nxt.append(f'Chapter {next_ch} →')

        # up: was appendices/index, change to part-12/index
        up = nav.find('a', class_='up')
        if up:
            up['href'] = '../index.html'
            up.clear()
            up.append('Part XII: LLM Applications Across Industries')

        if not dry:
            f.write_text(str(s), encoding='utf-8')
        print(f'  updated nav: {new}/index.html')


def create_part_12_index(dry):
    """Create the part-12 landing page based on existing part templates."""
    # Use part-11/index.html as a model
    template = ROOT / 'part-11-idea-to-product' / 'index.html'
    if not template.exists():
        print(f'  ERROR: template missing: {template}')
        return
    t = template.read_text(encoding='utf-8')
    # Replace markers
    t = re.sub(r'Part XI:[^<]*<', 'Part XII: LLM Applications Across Industries<', t)
    t = re.sub(r'Part XI[^<:]*', 'Part XII', t)
    t = t.replace('part-11-idea-to-product', NEW_PART_DIR)

    # Build the chapter-card list for part-12. Each industry is a single page.
    cards_html = []
    for old, new, ch, _l in MIGRATION:
        industry = old.replace('appendix-', '').replace('-llms', '')
        # Capitalize: 'legal' → 'Legal', 'aa-cybersecurity' → 'AA-Cybersecurity'
        industry_label = industry.split('-', 1)[-1].title() if '-' in industry else industry.title()
        cards_html.append(f'''
    <div class="chapter-card">
        <div class="chapter-card-header">
            <span class="mod-num">Chapter {ch}</span> {industry_label} Applications of LLMs
        </div>
        <div class="chapter-card-body">
            <p>Industry-specific LLM applications, use cases, regulatory considerations, and production patterns for {industry_label.lower()}.</p>
            <p><a href="{new}/index.html">Read Chapter {ch} →</a></p>
        </div>
    </div>''')

    # Insert the cards into the body
    s = BeautifulSoup(t, 'html.parser')
    main = s.find('main', class_='content')
    if main:
        # Remove existing chapter cards
        for cc in main.find_all('div', class_='chapter-card'):
            cc.decompose()
        # Remove existing module list / overview text — replace with new
        h1 = main.find('h1')
        # Insert cards after the first <h2> or at end of overview
        cards_soup = BeautifulSoup('\n'.join(cards_html), 'html.parser')
        # Find a good insertion point: after .part-overview or .objectives or
        # at the end of main before any nav
        insertion = main.find('div', class_='part-overview')
        if insertion is None:
            insertion = main.find('div', class_='callout')
        if insertion is None:
            insertion = h1
        if insertion is not None:
            for tag in cards_soup.find_all('div', class_='chapter-card'):
                insertion.insert_after(tag.extract())

    # Update title
    title = s.find('title')
    if title:
        title.string = 'Part XII: LLM Applications Across Industries | Building Conversational AI with LLMs and Agents'
    h1 = s.find('h1')
    if h1:
        h1.string = 'Part XII: LLM Applications Across Industries'

    # Update nav: prev was Part XI (correct, keep), up = toc, next = first module
    nav = s.find('nav', class_='chapter-nav')
    if nav:
        prev = nav.find('a', class_='prev')
        if prev:
            prev['href'] = '../part-11-idea-to-product/index.html'
            prev.clear()
            prev.append('← Part XI: Idea-to-Product')
        nxt = nav.find('a', class_='next')
        if nxt:
            nxt['href'] = f'{MIGRATION[0][1]}/index.html'
            nxt.clear()
            nxt.append(f'Chapter {MIGRATION[0][2]} →')

    target = ROOT / NEW_PART_DIR / 'index.html'
    if not dry:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(str(s), encoding='utf-8')
    print(f'  created: {NEW_PART_DIR}/index.html')


def delete_old_appendix_dirs(dry):
    for old, _new, _ch, _l in MIGRATION:
        src = ROOT / 'appendices' / old
        if src.exists():
            if not dry:
                shutil.rmtree(src)
            print(f'  deleted: appendices/{old}')


def update_toc_html(dry):
    p = ROOT / 'toc.html'
    t = p.read_text(encoding='utf-8')
    # Remove industry rows from toc (any row referencing appendix-w/x/y/z/aa/ab/ac)
    n = 0
    for old, _new, _ch, _l in MIGRATION:
        new_t, k = re.subn(
            rf'<div class="dense-chapter"><span class="dense-ch-num">(?:App\s+)?{re.escape(_l := old.split("-")[1].upper())}</span>[^<]*<a href="appendices/{old}[^"]*">[^<]*</a></div>\s*',
            '', t
        )
        t = new_t
        n += k
    print(f'  toc.html: {n} appendix rows removed')

    # Add new Part XII section (after Part XI block, before Appendices)
    part_xii_block = '<div class="dense-part-header"><span class="dense-pt-num">Part XII</span> <a href="part-12-llm-applications-across-industries/index.html">LLM Applications Across Industries</a></div>\n'
    for _old, new, ch, _l in MIGRATION:
        industry_name = new.replace('module-', '').split('-', 1)[1].replace('-llms', '').replace('-', ' ').title() + ' Applications of LLMs'
        part_xii_block += f'<div class="dense-chapter"><span class="dense-ch-num">{ch}</span> <a href="part-12-llm-applications-across-industries/{new}/index.html">{industry_name}</a></div>\n'

    # Insert before the first appendices block
    insertion_marker = '<div class="dense-part-header"><span class="dense-pt-num">Appendices</span>'
    if insertion_marker in t:
        t = t.replace(insertion_marker, part_xii_block + insertion_marker, 1)
        print(f'  toc.html: Part XII block inserted')

    if not dry:
        p.write_text(t, encoding='utf-8')


def update_appendices_index(dry):
    p = ROOT / 'appendices' / 'index.html'
    s = BeautifulSoup(p.read_text(encoding='utf-8'), 'html.parser')
    n = 0
    for card in list(s.find_all('div', class_='chapter-card')):
        txt = str(card)
        if any(ind in txt for ind, _, _, _ in MIGRATION):
            card.decompose()
            n += 1
    print(f'  appendices/index.html: {n} industry cards removed')
    # Update navigation: prev was part-11/35.4 — keep, next stays appendix-a
    # Wait — appendices/index.prev should now be the LAST industry chapter (module-42).
    nav = s.find('nav', class_='chapter-nav')
    if nav:
        prev = nav.find('a', class_='prev')
        if prev:
            prev['href'] = f'../{NEW_PART_DIR}/{MIGRATION[-1][1]}/index.html'
            prev.clear()
            prev.append(f'← Chapter {MIGRATION[-1][2]}')

    # Also remove any h2 "Industry Applications" group header that's now empty
    for h2 in list(s.find_all(['h2', 'h3'])):
        txt = h2.get_text(strip=True).lower()
        if 'industry' in txt or 'industries' in txt:
            # Check next sibling: if it's empty after card removal, drop heading
            nxt = h2.find_next_sibling()
            if nxt is None or (hasattr(nxt, 'get_text') and not nxt.get_text(strip=True)):
                h2.decompose()
                print(f'  removed empty group heading')

    if not dry:
        p.write_text(str(s), encoding='utf-8')


def update_part_11_next(dry):
    """part-11/index.next was → appendices/index. Change to part-12/index."""
    p = ROOT / 'part-11-idea-to-product' / 'index.html'
    s = BeautifulSoup(p.read_text(encoding='utf-8'), 'html.parser')
    nav = s.find('nav', class_='chapter-nav')
    if nav:
        nxt = nav.find('a', class_='next')
        if nxt:
            nxt['href'] = f'../{NEW_PART_DIR}/index.html'
            nxt.clear()
            nxt.append('Part XII: LLM Applications →')
            if not dry:
                p.write_text(str(s), encoding='utf-8')
            print(f'  updated part-11/index.next -> part-12/index')

    # Also update module-35/section-35.4.next
    p2 = ROOT / 'part-11-idea-to-product' / 'module-35-shipping-scaling' / 'section-35.4.html'
    if p2.exists():
        s2 = BeautifulSoup(p2.read_text(encoding='utf-8'), 'html.parser')
        nav = s2.find('nav', class_='chapter-nav')
        if nav:
            nxt = nav.find('a', class_='next')
            if nxt:
                nxt['href'] = f'../../{NEW_PART_DIR}/index.html'
                nxt.clear()
                nxt.append('Part XII →')
                if not dry:
                    p2.write_text(str(s2), encoding='utf-8')
                print(f'  updated module-35/35.4.next -> part-12/index')


def update_appendix_v_next(dry):
    """appendix-v/section-v.3.next was → appendix-w. Now skip to appendix-ad."""
    p = ROOT / 'appendices' / 'appendix-v-tooling-ecosystem' / 'section-v.3.html'
    if not p.exists():
        return
    s = BeautifulSoup(p.read_text(encoding='utf-8'), 'html.parser')
    nav = s.find('nav', class_='chapter-nav')
    if nav:
        nxt = nav.find('a', class_='next')
        if nxt:
            nxt['href'] = '../appendix-ad-master-reference-tables/index.html'
            nxt.clear()
            nxt.append('Appendix AD →')
            if not dry:
                p.write_text(str(s), encoding='utf-8')
            print(f'  updated v.3.next -> appendix-ad')


def update_appendix_ad_prev(dry):
    """appendix-AD/index.prev was → appendix-ac. Now → appendix-v.3."""
    p = ROOT / 'appendices' / 'appendix-ad-master-reference-tables' / 'index.html'
    if not p.exists():
        return
    s = BeautifulSoup(p.read_text(encoding='utf-8'), 'html.parser')
    nav = s.find('nav', class_='chapter-nav')
    if nav:
        prev = nav.find('a', class_='prev')
        if prev:
            prev['href'] = '../appendix-v-tooling-ecosystem/section-v.3.html'
            prev.clear()
            prev.append('← Appendix V')
            if not dry:
                p.write_text(str(s), encoding='utf-8')
            print(f'  updated appendix-ad.prev -> appendix-v.3')


def main():
    dry = '--apply' not in sys.argv
    print('DRY RUN.' if dry else 'APPLY mode.')

    step('Copy industry appendices to new part-12 location')
    move_dirs(dry)

    step('Update internal markup of moved files')
    update_moved_files_internal(dry)

    step('Create part-12/index.html landing page')
    create_part_12_index(dry)

    step('Update internal navigation of moved chapters')
    update_internal_nav(dry)

    step('Update toc.html')
    update_toc_html(dry)

    step('Update appendices/index.html')
    update_appendices_index(dry)

    step('Update part-11/index.next + module-35/35.4.next')
    update_part_11_next(dry)

    step('Update appendix-v/v.3.next -> appendix-ad')
    update_appendix_v_next(dry)

    step('Update appendix-ad.prev -> appendix-v.3')
    update_appendix_ad_prev(dry)

    step('Delete old appendix-w..ac directories')
    delete_old_appendix_dirs(dry)

    print('\nDONE')


if __name__ == '__main__':
    main()
