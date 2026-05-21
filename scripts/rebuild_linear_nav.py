"""Rebuild the linear nav chain across all sections.

Walks sections in linear order (part -> module -> section) and writes
correct prev / up / next anchors in each <nav class="chapter-nav">.
"""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]


def section_sort_key(p):
    m = re.match(r'section-(\d+)\.(\d+)\.html', p.name)
    if m: return (int(m.group(1)), int(m.group(2)))
    return (999, 999)


def get_sections_linear():
    sections = []
    for part_dir in sorted(ROOT.glob('part-*/'),
                          key=lambda p: int(re.match(r'part-(\d+)-', p.name).group(1))):
        for mod_dir in sorted(part_dir.glob('module-*/'),
                             key=lambda p: int(re.match(r'module-(\d+)-', p.name).group(1))):
            for sec in sorted(mod_dir.glob('section-*.html'), key=section_sort_key):
                sections.append(sec)
    return sections


def rel_path(from_p, to_p):
    from_parts = from_p.parent.parts
    to_parts = to_p.parts
    i = 0
    while i < min(len(from_parts), len(to_parts)) and from_parts[i] == to_parts[i]:
        i += 1
    ups = ['..'] * (len(from_parts) - i)
    downs = list(to_parts[i:])
    return '/'.join(ups + downs)


def get_h1_title(p):
    text = p.read_text(encoding='utf-8')
    m = re.search(r'<h1[^>]*>([^<]+)</h1>', text)
    return m.group(1).strip() if m else ''


def get_section_num(p):
    m = re.match(r'section-(\d+)\.(\d+)\.html', p.name)
    return f'{m.group(1)}.{m.group(2)}' if m else '?'


def get_chapter_num(p):
    m = re.match(r'module-(\d+)-', p.parent.name)
    return m.group(1) if m else '?'


def get_chapter_title(p):
    idx = p.parent / 'index.html'
    if idx.exists():
        text = idx.read_text(encoding='utf-8')
        m = re.search(r'<h1[^>]*>([^<]+)</h1>', text)
        if m:
            t = m.group(1).strip()
            # Strip "Chapter N: " prefix
            t = re.sub(r'^Chapter\s+\d+:?\s*', '', t)
            return t
    return ''


def main():
    sections = get_sections_linear()
    print(f'Linear sections: {len(sections)}')

    n_rewritten = 0
    for i, sec in enumerate(sections):
        text = sec.read_text(encoding='utf-8')
        nav_items = []

        # PREV
        if i > 0:
            prev = sections[i-1]
            prev_rel = rel_path(sec, prev)
            nav_items.append(
                f'<a class="prev" href="{prev_rel}"><span class="nav-label">Previous</span>'
                f'<span class="nav-num">Section {get_section_num(prev)}</span>'
                f'<span class="nav-title">{get_h1_title(prev)}</span></a>'
            )

        # UP: chapter index
        ch_num = get_chapter_num(sec)
        ch_title = get_chapter_title(sec)
        nav_items.append(
            f'<a class="up" href="index.html"><span class="nav-label">In Chapter</span>'
            f'<span class="nav-num">Chapter {ch_num}</span>'
            f'<span class="nav-title">{ch_title}</span></a>'
        )

        # NEXT
        if i < len(sections) - 1:
            nxt = sections[i+1]
            nxt_rel = rel_path(sec, nxt)
            nav_items.append(
                f'<a class="next" href="{nxt_rel}"><span class="nav-label">Next</span>'
                f'<span class="nav-num">Section {get_section_num(nxt)}</span>'
                f'<span class="nav-title">{get_h1_title(nxt)}</span></a>'
            )

        new_nav = '<nav class="chapter-nav">\n' + '\n'.join(nav_items) + '\n</nav>'

        # Replace existing nav (use lambda to avoid backref interpretation)
        if re.search(r'<nav class="chapter-nav">', text):
            new_text = re.sub(
                r'<nav class="chapter-nav">[\s\S]*?</nav>',
                lambda m: new_nav,
                text,
                count=1
            )
        else:
            new_text = text.replace('</main>', f'{new_nav}\n</main>', 1)

        if new_text != text:
            sec.write_text(new_text, encoding='utf-8')
            n_rewritten += 1

    print(f'Sections nav rewritten: {n_rewritten}')


if __name__ == '__main__':
    main()
