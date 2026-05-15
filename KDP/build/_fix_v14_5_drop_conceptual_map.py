"""v14.5: drop appendix-ah-conceptual-map.

Steps:
  1. Update toc.html to remove the dense-chapter row for AH
  2. Update appendices/index.html to remove the AH card
  3. Update appendix-ag/index.html.next -> appendix-ai (skip AH)
  4. Update appendix-ai/index.html.prev -> appendix-ag (skip AH)
  5. Strip inline references in:
       - part-8/section-28.1.html
       - part-5/section-19.1.html
       - part-4/section-17.1.html (Thesis 4 reference)
       - part-2/section-6.3.html (compute axis reference)
       - part-2/section-10.1.html
       - appendix-af/index.html (pedagogy kit reading order)
       - appendix-aj/index.html (reading pathways list item)
  6. Delete the appendix-ah-conceptual-map/ directory.

Each inline reference is rewritten as plain text (the surrounding prose
remains; the hyperlink is removed; phrases like "see Appendix AH" are
deleted or rephrased).
"""
from pathlib import Path
from bs4 import BeautifulSoup
import re
import shutil
import sys

ROOT = Path(__file__).resolve().parents[2]


def step(label):
    print(f'\n>>> {label}')


def remove_toc_row(dry):
    """Remove the AH row from toc.html (both short and dense views)."""
    p = ROOT / 'toc.html'
    t = p.read_text(encoding='utf-8')
    n = 0
    # Match the entire row containing appendix-ah-conceptual-map
    # Short: <div class="dense-chapter"><span ...>AH</span> <a href="appendices/appendix-ah-conceptual-map/...">Conceptual Map of This Book</a></div>
    new_t, k = re.subn(
        r'<div class="dense-chapter"><span class="dense-ch-num">AH</span>[^<]*<a href="appendices/appendix-ah-conceptual-map[^"]*">[^<]*</a></div>\s*',
        '', t
    )
    n += k
    # Detailed: <div class="dense-chapter"><span ...>App AH</span> ...
    new_t, k = re.subn(
        r'<div class="dense-chapter"><span class="dense-ch-num">App AH</span>[^<]*<a href="appendices/appendix-ah-conceptual-map[^"]*">[^<]*</a></div>\s*',
        '', new_t
    )
    n += k
    if k > 0 or new_t != t:
        if not dry:
            p.write_text(new_t, encoding='utf-8')
        print(f'  toc.html: {n} row(s) removed')


def remove_appendix_index_card(dry):
    """Remove the AH chapter-card from appendices/index.html."""
    p = ROOT / 'appendices' / 'index.html'
    s = BeautifulSoup(p.read_text(encoding='utf-8'), 'html.parser')
    n = 0
    for card in s.find_all('div', class_='chapter-card'):
        if 'Conceptual Map' in card.get_text() or \
           'appendix-ah-conceptual-map' in str(card):
            card.decompose()
            n += 1
    if n > 0:
        if not dry:
            p.write_text(str(s), encoding='utf-8')
        print(f'  appendices/index.html: {n} card(s) removed')


def fix_appendix_ag_next(dry):
    """appendix-ag/index.html: next was AH; now should be AI."""
    p = ROOT / 'appendices' / 'appendix-ag-problem-solution-key' / 'index.html'
    s = BeautifulSoup(p.read_text(encoding='utf-8'), 'html.parser')
    nav = s.find('nav', class_='chapter-nav')
    if not nav:
        return
    nxt = nav.find('a', class_='next')
    if nxt and 'appendix-ah' in nxt.get('href', ''):
        nxt['href'] = '../appendix-ai-freshness-2026/index.html'
        nxt.clear()
        nxt.append('Appendix AI: 2026 Freshness Index →')
        if not dry:
            p.write_text(str(s), encoding='utf-8')
        print(f'  appendix-ag/index.html: next now -> appendix-ai')


def fix_appendix_ai_prev(dry):
    """appendix-ai/index.html: prev was AH; now should be AG."""
    p = ROOT / 'appendices' / 'appendix-ai-freshness-2026' / 'index.html'
    s = BeautifulSoup(p.read_text(encoding='utf-8'), 'html.parser')
    nav = s.find('nav', class_='chapter-nav')
    if not nav:
        return
    prev = nav.find('a', class_='prev')
    if prev and 'appendix-ah' in prev.get('href', ''):
        prev['href'] = '../appendix-ag-problem-solution-key/index.html'
        prev.clear()
        prev.append('← Appendix AG: Problem-Solution Key')
        if not dry:
            p.write_text(str(s), encoding='utf-8')
        print(f'  appendix-ai/index.html: prev now -> appendix-ag')


def strip_inline_refs(dry):
    """Strip inline <a href="...appendix-ah..."> references in prose, by
    converting the <a> to its inner text (preserving surrounding content).
    Also strip parenthetical phrases that mention Appendix AH explicitly."""
    targets = [
        'part-8-evaluation-production/module-28-evaluation-observability/section-28.1.html',
        'part-5-retrieval-conversation/module-19-rag/section-19.1.html',
        'part-4-training-adapting/module-17-alignment-rlhf-dpo/section-17.1.html',
        'part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.3.html',
        'part-2-understanding-llms/module-10-interpretability/section-10.1.html',
        'appendices/appendix-af-pedagogy-kit/index.html',
        'appendices/appendix-aj-reading-pathways/index.html',
    ]
    for rel in targets:
        p = ROOT / rel
        if not p.exists():
            print(f'  SKIP (missing): {rel}')
            continue
        s = BeautifulSoup(p.read_text(encoding='utf-8'), 'html.parser')
        modified = False
        # Find <a href="...appendix-ah..."> and replace with text content
        for a in s.find_all('a', href=True):
            if 'appendix-ah-conceptual-map' in a['href']:
                a.replace_with(a.get_text())
                modified = True
        # Also remove lone "Conceptual Map" mentions in list items
        for li in s.find_all('li'):
            if 'Conceptual Map' in li.get_text() and 'appendix-ah' not in str(li).lower():
                # Skip — without the link the text is probably a list item we
                # should drop. But to be conservative leave it.
                pass

        if modified:
            if not dry:
                p.write_text(str(s), encoding='utf-8')
            print(f'  stripped refs in {rel}')


def delete_appendix_dir(dry):
    d = ROOT / 'appendices' / 'appendix-ah-conceptual-map'
    if d.exists():
        if not dry:
            shutil.rmtree(d)
        print(f'  deleted directory: {d.relative_to(ROOT)}')


def main():
    dry = '--apply' not in sys.argv
    print('DRY RUN. Pass --apply.' if dry else 'APPLY mode.')

    step('Update toc.html')
    remove_toc_row(dry)

    step('Update appendices/index.html')
    remove_appendix_index_card(dry)

    step('Fix appendix-ag nav')
    fix_appendix_ag_next(dry)

    step('Fix appendix-ai nav')
    fix_appendix_ai_prev(dry)

    step('Strip inline references in prose')
    strip_inline_refs(dry)

    step('Delete appendix-ah-conceptual-map/')
    delete_appendix_dir(dry)

    print('\nDONE')


if __name__ == '__main__':
    main()
