"""Wave 17e: rebuild module-N/index.html sections-list from filesystem reality.

The cycle-2 audit caught several module index files where the sections-list
was stale (e.g. module-42 lists section-42.9 twice because of a partial
renumber from when sec 42.8 was promoted to Ch 46).

For each module-NN-slug/index.html:
  - List actual section-N.M.html files on disk
  - Read each section's h1 for the title
  - Try to find a placeholder section-desc in the existing index for that
    section; if not present, use a brief description from the section's
    big-picture (if any) or fall back to "Section N.M."
  - Rewrite the sections-list with one entry per actual section file
"""
from pathlib import Path
import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'.git', 'node_modules', 'KDP', 'build', 'temp_ebook', 'temp_epub',
        'source_fix_backups', 'pagefind', 'templates', '.claude',
        '.book-update', 'vendor', 'docs'}


def extract_section_summary(section_file):
    """Extract a 1-line description from a section's big-picture or first <p>."""
    text = section_file.read_text(encoding='utf-8')
    m = re.search(
        r'<div class="callout big-picture">\s*<div class="callout-title">Big Picture</div>\s*<p>([\s\S]*?)</p>',
        text
    )
    if m:
        summary_html = m.group(1).strip()
    else:
        m = re.search(r'<h1>[^<]+</h1>\s*(?:<[^>]+>[\s\S]*?</[^>]+>\s*)*?<p>([\s\S]*?)</p>', text)
        summary_html = m.group(1).strip() if m else ''
    summary = re.sub(r'<[^>]+>', '', summary_html)
    summary = re.sub(r'\s+', ' ', summary).strip()
    if not summary:
        return ''
    fm = re.match(r'^(.+?[.!?])(?:\s|$)', summary)
    first = fm.group(1) if fm else summary
    if len(first) > 200:
        first = first[:197].rsplit(' ', 1)[0] + '...'
    return first.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('&amp;amp;', '&amp;').replace('&amp;lt;', '&lt;').replace('&amp;gt;', '&gt;')


def get_section_title(section_file):
    text = section_file.read_text(encoding='utf-8')
    m = re.search(r'<h1>([^<]+)</h1>', text)
    return m.group(1).strip() if m else section_file.stem


def rebuild_module_index(module_dir):
    idx = module_dir / 'index.html'
    if not idx.exists():
        return False

    # Get sorted list of section files
    section_files = sorted(
        module_dir.glob('section-*.html'),
        key=lambda p: [int(x) for x in re.findall(r'\d+', p.name)]
    )
    if not section_files:
        return False

    # Get existing descriptions (keep them if reasonable, override placeholders)
    text = idx.read_text(encoding='utf-8')
    existing_descs = {}
    for m in re.finditer(
        r'<a class="section-card" href="(section-[\d.]+\.html)"[^>]*>[\s\S]*?<span class="section-desc">([^<]*)</span>',
        text
    ):
        existing_descs[m.group(1)] = m.group(2)

    cards = []
    for sf in section_files:
        # Section number from filename
        sm = re.match(r'section-(\d+)\.(\d+)\.html', sf.name)
        if not sm:
            continue
        sec_num = f'{sm.group(1)}.{sm.group(2)}'
        title = get_section_title(sf)
        # Use existing desc if present and not a placeholder; otherwise derive
        existing = existing_descs.get(sf.name, '')
        is_placeholder = (
            not existing
            or 'A comprehensive chapter' in existing
            or 'A chapter from the Building' in existing
            or 'Promoted from old' in existing
            or 'Split from old' in existing
            or existing.startswith('Section ')
            or existing in ('RAG fundamentals.', 'Conv AI tooling.', 'Voice and realtime multimodal AI.',
                            'Core production engineering.', 'See section for details.',
                            'Conversational AI.', 'Section.', 'Promoted and expanded from old section 42.8.')
            or len(existing) < 30  # extremely short = likely placeholder
        )
        if is_placeholder:
            desc = extract_section_summary(sf)
            if not desc:
                desc = f'Section {sec_num}.'
        else:
            desc = existing

        cards.append(
            f'<li><a class="section-card" href="{sf.name}">\n'
            f'<span class="section-num">{sec_num}</span>\n'
            f'<span class="section-title">{title}</span>\n'
            f'<span class="section-desc">{desc}</span>\n'
            f'</a></li>'
        )

    # Replace the sections-list block
    if '<ul class="sections-list">' not in text:
        return False
    new_text = re.sub(
        r'<ul class="sections-list">[\s\S]*?</ul>',
        '<ul class="sections-list">\n' + '\n'.join(cards) + '\n</ul>',
        text,
        count=1
    )

    if new_text != text:
        idx.write_text(new_text, encoding='utf-8')
        return True
    return False


def main():
    n = 0
    for module_dir in sorted(ROOT.rglob('module-*-*')):
        if set(module_dir.parts) & SKIP:
            continue
        if not module_dir.is_dir():
            continue
        if rebuild_module_index(module_dir):
            n += 1
    print(f'Rebuilt sections-list in {n} module index files')


if __name__ == '__main__':
    main()
