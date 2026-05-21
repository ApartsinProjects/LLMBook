"""Wave 16b: replace placeholder text in section file <meta name="description"> tags.

Pattern:
  <meta content="Section X.Y: TITLE. A comprehensive chapter from the
   Building Conversational AI textbook." name="description"/>

Replace "A comprehensive chapter from the Building Conversational AI textbook"
with a summary derived from the big-picture text of the section.
"""
from pathlib import Path
import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'.git', 'node_modules', 'KDP', 'build', 'temp_ebook', 'temp_epub',
        'source_fix_backups', 'pagefind', 'templates', '.claude',
        '.book-update', 'vendor', 'docs'}

PLACEHOLDERS = [
    r'A comprehensive chapter from the Building Conversational AI textbook',
    r'A chapter from the Building Conversational AI textbook',
    r'Promoted from old Ch 62 monster',
    r'Split from old Ch 32 RAG monster',
    r'Promoted and expanded from old section 42\.8',
    r'Promoted from old section 15\.5',
    r'See section for details',
]
PLACEHOLDER_RE = re.compile(r'(?:' + r'|'.join(PLACEHOLDERS) + r')\.?')


def extract_summary(text):
    """Extract a summary from the page body."""
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

    # First sentence, max 200 chars
    first_sentence_match = re.match(r'^(.+?[.!?])(?:\s|$)', summary)
    first_sentence = first_sentence_match.group(1) if first_sentence_match else summary
    if len(first_sentence) > 200:
        first_sentence = first_sentence[:197].rsplit(' ', 1)[0] + '...'

    # HTML attribute safe: escape quotes, not other entities
    first_sentence = first_sentence.replace('"', '&quot;')
    return first_sentence


def main():
    n_files = 0
    n_replacements = 0
    for p in sorted(ROOT.rglob('section-*.html')):
        if set(p.parts) & SKIP:
            continue
        text = p.read_text(encoding='utf-8')
        m = re.search(r'<meta content="([^"]*?)" name="description"', text)
        if not m:
            continue
        old_content = m.group(1)
        if not PLACEHOLDER_RE.search(old_content):
            continue

        summary = extract_summary(text)
        if not summary:
            continue

        # Old format: "Section X.Y: TITLE. PLACEHOLDER" or just "TITLE. PLACEHOLDER"
        # Replace the placeholder portion with the summary
        new_content = PLACEHOLDER_RE.sub(summary, old_content, count=1)
        # Trim trailing whitespace and ensure period at end
        new_content = new_content.strip()
        if not new_content.endswith('.'):
            new_content += '.'

        new_text = text.replace(
            f'<meta content="{old_content}" name="description"',
            f'<meta content="{new_content}" name="description"',
            1
        )
        if new_text != text:
            p.write_text(new_text, encoding='utf-8')
            n_files += 1
            n_replacements += 1

    # Also fix the chapter index files (the meta description in module-X/index.html)
    for p in sorted(ROOT.rglob('module-*/index.html')):
        if set(p.parts) & SKIP:
            continue
        text = p.read_text(encoding='utf-8')
        m = re.search(r'<meta content="([^"]*?)" name="description"', text)
        if not m:
            continue
        old_content = m.group(1)
        if not PLACEHOLDER_RE.search(old_content):
            continue

        summary = extract_summary(text)
        if not summary:
            continue

        new_content = PLACEHOLDER_RE.sub(summary, old_content, count=1)
        new_content = new_content.strip()
        if not new_content.endswith('.'):
            new_content += '.'

        new_text = text.replace(
            f'<meta content="{old_content}" name="description"',
            f'<meta content="{new_content}" name="description"',
            1
        )
        if new_text != text:
            p.write_text(new_text, encoding='utf-8')
            n_files += 1
            n_replacements += 1

    print(f'Replaced placeholder meta descriptions in {n_files} files ({n_replacements} total)')


if __name__ == '__main__':
    main()
