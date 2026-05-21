"""Wave 16c: replace placeholder text in toc.html toc-chapter-subtitle spans
and in part-N/index.html meta descriptions.
"""
from pathlib import Path
import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]


def extract_summary(text):
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
    first_sentence_match = re.match(r'^(.+?[.!?])(?:\s|$)', summary)
    first_sentence = first_sentence_match.group(1) if first_sentence_match else summary
    if len(first_sentence) > 200:
        first_sentence = first_sentence[:197].rsplit(' ', 1)[0] + '...'
    return first_sentence


def fix_toc():
    """For each toc-chapter entry, look up the chapter's big-picture for the subtitle."""
    p = ROOT / 'toc.html'
    text = p.read_text(encoding='utf-8')

    # Pattern: <a href="part-X-slug/module-NN-slug/index.html">
    #          <span class="toc-chapter-num"...>N</span>
    #          <span class="toc-chapter-title">TITLE</span>
    #          <span class="toc-chapter-subtitle">SUBTITLE</span>
    placeholder = re.compile(
        r'(<a href="(part-[^/]+/module-[^/]+)/index\.html">[\s\S]*?'
        r'<span class="toc-chapter-subtitle">)'
        r'A comprehensive chapter from the Building Conversational AI textbook\.'
        r'(</span>)'
    )

    def replace(m):
        prefix = m.group(1)
        module_path = m.group(2)
        suffix = m.group(3)
        chapter_idx = ROOT / module_path / 'index.html'
        if not chapter_idx.exists():
            return m.group(0)
        ch_text = chapter_idx.read_text(encoding='utf-8')
        summary = extract_summary(ch_text)
        if not summary:
            return m.group(0)
        return f'{prefix}{summary}{suffix}'

    new_text = placeholder.sub(replace, text)
    if new_text != text:
        p.write_text(new_text, encoding='utf-8')
        print(f'  Fixed toc.html chapter subtitles')


def fix_part_meta():
    """Each part-N/index.html has a placeholder in its <meta description>. Use part-overview text."""
    for part_dir in ROOT.iterdir():
        if not part_dir.is_dir() or not part_dir.name.startswith('part-'):
            continue
        idx = part_dir / 'index.html'
        if not idx.exists():
            continue
        text = idx.read_text(encoding='utf-8')
        # Find <meta description>
        m = re.search(r'<meta content="([^"]*?)" name="description"', text)
        if not m:
            continue
        old_content = m.group(1)
        if 'A comprehensive chapter from the Building Conversational AI textbook' not in old_content:
            continue
        # Use part-overview big-picture if present
        summary = extract_summary(text)
        if not summary:
            continue
        new_content = re.sub(
            r'A comprehensive chapter from the Building Conversational AI textbook\.?',
            summary,
            old_content,
            count=1
        ).strip()
        if not new_content.endswith('.'):
            new_content += '.'
        new_text = text.replace(
            f'<meta content="{old_content}" name="description"',
            f'<meta content="{new_content}" name="description"',
            1
        )
        if new_text != text:
            idx.write_text(new_text, encoding='utf-8')
            print(f'  Fixed {part_dir.name}/index.html meta description')


def fix_appendix_meta():
    """Fix appendices/appendix-a-*/index.html meta description placeholder."""
    p = ROOT / 'appendices' / 'appendix-a-mathematical-foundations' / 'index.html'
    if not p.exists():
        return
    text = p.read_text(encoding='utf-8')
    m = re.search(r'<meta content="([^"]*?)" name="description"', text)
    if not m:
        return
    old_content = m.group(1)
    if 'A comprehensive chapter from the Building Conversational AI textbook' not in old_content:
        return
    summary = extract_summary(text)
    if not summary:
        summary = 'The essential linear algebra, probability, calculus, and information theory that power every transformer'
    new_content = re.sub(
        r'A comprehensive chapter from the Building Conversational AI textbook\.?',
        summary,
        old_content
    ).strip()
    if not new_content.endswith('.'):
        new_content += '.'
    text = text.replace(
        f'<meta content="{old_content}" name="description"',
        f'<meta content="{new_content}" name="description"',
    )
    p.write_text(text, encoding='utf-8')
    print('  Fixed Apx A meta description')


def fix_capstone():
    """Fix capstone/requirements.html placeholder."""
    p = ROOT / 'capstone' / 'requirements.html'
    if not p.exists():
        return
    text = p.read_text(encoding='utf-8')
    # Replace the placeholder with a generic capstone description
    new_text = text.replace(
        'A comprehensive chapter from the Building Conversational AI textbook.',
        'A three-track capstone project with full-stack, API-only, and research-replication options.'
    )
    if new_text != text:
        p.write_text(new_text, encoding='utf-8')
        print('  Fixed capstone/requirements.html')


def main():
    fix_toc()
    fix_part_meta()
    fix_appendix_meta()
    fix_capstone()


if __name__ == '__main__':
    main()
