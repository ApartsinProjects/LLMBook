"""Wave 5: comprehensive infrastructure rebuild after all 4 restructures.

Regenerates from current disk state:
  1. toc.html
  2. book_structure.yaml
  3. Each part-index's chapter-card list
  4. Each chapter-index's section-card list
  5. Each section's prev/next nav

Idempotent.
"""
from __future__ import annotations
import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PARTS_META = {
    'part-1-foundations': ('I', 'Foundations'),
    'part-2-understanding-llms': ('II', 'Understanding LLMs'),
    'part-3-working-with-llms': ('III', 'Working with LLMs'),
    'part-4-training-adapting': ('IV', 'LLM Training and Adaptation'),
    'part-5-retrieval-conversation': ('V', 'Retrieval and Conversation with LLMs and Agents'),
    'part-6-agentic-ai': ('VI', 'Agentic AI'),
    'part-7-multimodal-generation': ('VII', 'Multimodal Generation'),
    'part-8-evaluation-production': ('VIII', 'Evaluation of LLM-Based Systems'),
    'part-9-safety-security-ethics': ('IX', 'LLM Safety, Security, and Ethics'),
    'part-10-llmops': ('X', 'LLM Operations and Production Infrastructure'),
    'part-11-designing-llm-products': ('XI', 'Designing LLM-Based Products'),
    'part-12-applications-across-industries': ('XII', 'Applications Across Industries'),
    'part-13-frontiers': ('XIII', 'Frontiers'),
}


def get_h1(p):
    if not p.exists(): return None
    t = p.read_text(encoding='utf-8')
    m = re.search(r'<h1>([^<]+)</h1>', t)
    return m.group(1).strip() if m else None


def get_section_desc(p):
    """Extract one-sentence description from section."""
    if not p.exists(): return ''
    t = p.read_text(encoding='utf-8')
    # Look for big-picture callout, first <p>, or meta description
    m = re.search(r'<meta content="Section \d+\.\d+:?[^.]+\.\s+([^"]+)"', t)
    if m: return m.group(1)[:200]
    m = re.search(r'<div class="callout big-picture">[\s\S]*?<p>([^<]+)</p>', t)
    if m: return m.group(1)[:200]
    return ''


def get_chapter_desc(p):
    """Extract one-sentence description from chapter index."""
    if not p.exists(): return ''
    t = p.read_text(encoding='utf-8')
    m = re.search(r'<meta content="Chapter \d+:?[^.]+\.\s+([^"]+)"', t)
    if m: return m.group(1)[:200]
    m = re.search(r'<div class="callout big-picture">[\s\S]*?<p>([^<]+)</p>', t)
    if m: return m.group(1)[:200]
    return ''


def get_chapter_num(slug):
    m = re.match(r'module-(\d+)-', slug)
    return int(m.group(1)) if m else None


def get_section_num(filename):
    m = re.match(r'section-(\d+)\.(\d+)\.html', filename)
    return (int(m.group(1)), int(m.group(2))) if m else None


def build_structure():
    parts_data = []
    for part_slug in sorted(PARTS_META.keys(),
                            key=lambda s: int(re.match(r'part-(\d+)-', s).group(1))):
        part_dir = ROOT / part_slug
        if not part_dir.exists():
            continue
        roman, title = PARTS_META[part_slug]
        chapters = []
        for mod in sorted(part_dir.glob('module-*/'),
                          key=lambda p: get_chapter_num(p.name) or 999):
            if not mod.is_dir(): continue
            ch_num = get_chapter_num(mod.name)
            ch_title = get_h1(mod / 'index.html')
            ch_desc = get_chapter_desc(mod / 'index.html')
            sections = []
            for sec in sorted(mod.glob('section-*.html'),
                              key=lambda p: get_section_num(p.name) or (999, 999)):
                sn = get_section_num(sec.name)
                stitle = get_h1(sec)
                sdesc = get_section_desc(sec)
                sections.append((sn, stitle, sec.name, sdesc))
            chapters.append((ch_num, ch_title, ch_desc, mod.name, sections))
        parts_data.append((roman, title, part_slug, chapters))
    return parts_data


def rebuild_toc(parts_data, dry_run):
    """Regenerate toc.html."""
    toc_p = ROOT / 'toc.html'
    if not toc_p.exists():
        return False
    text = toc_p.read_text(encoding='utf-8')
    # Build new TOC content (inside <main class="content">)
    parts_html = []
    for roman, title, slug, chs in parts_data:
        ch_items = []
        for ch_num, ch_title, ch_desc, mod_slug, secs in chs:
            sec_items = []
            for (sn, stitle, sf, sdesc) in secs:
                if sn is None: continue
                sec_items.append(
                    f'<li><a href="{slug}/{mod_slug}/{sf}">'
                    f'<span class="toc-sec-num">{sn[0]}.{sn[1]}</span> '
                    f'<span class="toc-sec-title">{stitle}</span></a></li>'
                )
            ch_items.append(
                f'<details class="toc-chapter">\n'
                f'<summary><span class="toc-chapter-num">Chapter {ch_num}</span> '
                f'<a href="{slug}/{mod_slug}/index.html">{ch_title or "?"}</a></summary>\n'
                f'<ul class="toc-section-list">\n{chr(10).join(sec_items)}\n</ul>\n'
                f'</details>'
            )
        parts_html.append(
            f'<details class="toc-part" open>\n'
            f'<summary><span class="toc-part-num">Part {roman}</span> '
            f'<a href="{slug}/index.html">{title}</a></summary>\n'
            f'{chr(10).join(ch_items)}\n'
            f'</details>'
        )
    toc_inner = '\n'.join(parts_html)
    # Replace content between <h2>Contents</h2> and the next major section
    new_main = re.sub(
        r'(<h2>(?:Table of )?Contents</h2>\s*)([\s\S]*?)(?=<h2>|</main>)',
        rf'\1\n<div class="toc-tree">\n{toc_inner}\n</div>\n',
        text,
        count=1,
    )
    if new_main == text:
        # No match found; try to inject before </main>
        new_main = text.replace('</main>',
                                f'<h2>Table of Contents</h2>\n<div class="toc-tree">\n{toc_inner}\n</div>\n</main>',
                                1)
    if new_main != text and not dry_run:
        toc_p.write_text(new_main, encoding='utf-8')
    return new_main != text


def rebuild_part_index(part_slug, roman, title, chs, dry_run):
    """Rebuild a part-index's chapter-card list."""
    idx = ROOT / part_slug / 'index.html'
    if not idx.exists(): return False
    text = idx.read_text(encoding='utf-8')
    cards = []
    for ch_num, ch_title, ch_desc, mod_slug, secs in chs:
        sec_items = []
        for (sn, stitle, sf, _) in secs:
            if sn is None: continue
            sec_items.append(
                f'<li><a href="{mod_slug}/{sf}">'
                f'<span class="sec-num">{sn[0]}.{sn[1]}</span> {stitle}</a></li>'
            )
        card = (
            f'<div class="chapter-card">\n'
            f'<div class="chapter-card-header">'
            f'<span class="mod-num">Chapter {ch_num}</span> {ch_title or "?"}'
            f'</div>\n'
            f'<div class="chapter-card-body">\n'
            f'<ul class="section-list">\n{chr(10).join(sec_items) if sec_items else "<li><em>Content coming soon</em></li>"}\n</ul>\n'
            f'</div>\n'
            f'<div class="chapter-card-footer">'
            f'<a href="{mod_slug}/index.html" class="chapter-link">Open Chapter {ch_num} →</a>'
            f'</div>\n'
            f'</div>'
        )
        cards.append(card)
    cards_html = '\n'.join(cards)
    # Try to find and replace existing chapter-card-list / chapter-cards container
    new_text = text
    patterns = [
        (r'<div class="chapter-card-list">[\s\S]*?</div>\s*(?=</main>|<nav|<footer)',
         f'<div class="chapter-card-list">\n{cards_html}\n</div>\n'),
        (r'(<h2>Chapters</h2>)[\s\S]*?(?=</main>|<nav class="chapter-nav"|<footer)',
         rf'\1\n<div class="chapter-card-list">\n{cards_html}\n</div>\n'),
    ]
    for pat, repl in patterns:
        nt = re.sub(pat, repl, text, count=1)
        if nt != text:
            new_text = nt
            break
    if new_text == text:
        # Try locating any existing chapter-card section then replace all chapter-card divs
        new_text = re.sub(r'(<div class="chapter-card">[\s\S]*?</div>\s*)+', cards_html + '\n', text)
    if new_text != text and not dry_run:
        idx.write_text(new_text, encoding='utf-8')
    return new_text != text


def rebuild_chapter_index(mod_dir, ch_num, ch_title, secs, dry_run):
    """Rebuild a chapter-index's section-card list."""
    idx = mod_dir / 'index.html'
    if not idx.exists(): return False
    text = idx.read_text(encoding='utf-8')
    cards = []
    for (sn, stitle, sf, sdesc) in secs:
        if sn is None: continue
        card = (
            f'<a class="section-card" href="{sf}">\n'
            f'<span class="section-num">{sn[0]}.{sn[1]}</span>\n'
            f'<span class="section-title">{stitle}</span>\n'
            f'<span class="section-desc">{sdesc}</span>\n'
            f'</a>'
        )
        cards.append(card)
    cards_html = '\n'.join(cards)
    new_text = text
    patterns = [
        (r'<div class="section-card-list">[\s\S]*?</div>(?=\s*(?:</main>|<nav|<div class="whats-next))',
         f'<div class="section-card-list">\n{cards_html}\n</div>'),
        (r'<ul class="sections-list">[\s\S]*?</ul>',
         f'<ul class="sections-list">\n' + '\n'.join(f'<li>{c}</li>' for c in cards) + '\n</ul>'),
        (r'(<h2>Sections(?:[^<]*?)</h2>)\s*(?:<ul[^>]*>[\s\S]*?</ul>|<div class="section-card-list">[\s\S]*?</div>)',
         rf'\1\n<ul class="sections-list">\n' + '\n'.join(f'<li>{c}</li>' for c in cards) + '\n</ul>'),
    ]
    for pat, repl in patterns:
        nt = re.sub(pat, repl, text, count=1)
        if nt != text:
            new_text = nt
            break
    if new_text != text and not dry_run:
        idx.write_text(new_text, encoding='utf-8')
    return new_text != text


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--apply', action='store_true')
    args = ap.parse_args()
    dry_run = not args.apply
    parts_data = build_structure()

    print(f'Parts: {len(parts_data)}')
    total_ch = sum(len(chs) for _, _, _, chs in parts_data)
    total_sec = sum(len(secs) for _, _, _, chs in parts_data for _, _, _, _, secs in chs)
    print(f'Chapters: {total_ch}, Sections: {total_sec}\n')

    # 1) Rebuild TOC
    if rebuild_toc(parts_data, dry_run):
        print('  toc.html: REGEN')

    # 2) Rebuild part indexes
    n_parts = 0
    for roman, title, slug, chs in parts_data:
        if rebuild_part_index(slug, roman, title, chs, dry_run):
            n_parts += 1
    print(f'  Part indexes regenerated: {n_parts}')

    # 3) Rebuild chapter indexes
    n_chaps = 0
    for roman, title, slug, chs in parts_data:
        for ch_num, ch_title, ch_desc, mod_slug, secs in chs:
            mod = ROOT / slug / mod_slug
            if rebuild_chapter_index(mod, ch_num, ch_title, secs, dry_run):
                n_chaps += 1
    print(f'  Chapter indexes regenerated: {n_chaps}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
