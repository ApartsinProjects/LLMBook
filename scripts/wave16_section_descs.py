"""Wave 16: replace placeholder section descriptions in every chapter index by
auto-deriving from each section's big-picture (or first paragraph of body).

The audit found placeholders like:
  - "A comprehensive chapter from the Building Conversational AI textbook." (~hundreds)
  - "Promoted from old Ch 62 monster."
  - "Split from old Ch 32 RAG monster."
  - "RAG fundamentals."
  - "Voice and realtime multimodal AI."
  - "Conv AI tooling."
  - "Core production engineering."
  - "Promoted and expanded from old section 42.8"
  - "Promoted from old section 15.5."
  - "Section X.Y."

For each chapter's index.html, find each section card, read the section
file's big-picture (or first body paragraph), extract a one-line summary
(first sentence, up to 160 chars), and replace the section-desc.
"""
from pathlib import Path
import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]

PLACEHOLDER_PATTERNS = [
    r'A comprehensive chapter from the Building Conversational AI textbook\.',
    r'A chapter from the Building Conversational AI textbook\.',
    r'Promoted from old Ch 62 monster\.',
    r'Split from old Ch 32 RAG monster\.',
    r'RAG fundamentals\.',
    r'Voice and realtime multimodal AI\.',
    r'Conv AI tooling\.',
    r'Core production engineering\.',
    r'Promoted and expanded from old section 42\.8',
    r'Promoted from old section 15\.5\.',
    r'Classical ML\. A comprehensive[^<]*',  # truncated cruft prefix
    r'See section for details\.',
    r'Section \d+\.\d+\.',  # generic auto-placeholder
]

# Combined pattern for matching any placeholder
PLACEHOLDER_RE = re.compile(r'^(?:' + r'|'.join(PLACEHOLDER_PATTERNS) + r')$')

SKIP = {'.git', 'node_modules', 'KDP', 'build', 'temp_ebook', 'temp_epub',
        'source_fix_backups', 'pagefind', 'templates', '.claude',
        '.book-update', 'vendor', 'docs'}


def extract_section_summary(section_file):
    """Extract a 1-line summary from a section file's big-picture or first body paragraph."""
    text = section_file.read_text(encoding='utf-8')

    # Try big-picture first; allow inner tags by capturing then stripping
    m = re.search(
        r'<div class="callout big-picture">\s*<div class="callout-title">Big Picture</div>\s*<p>([\s\S]*?)</p>',
        text
    )
    if m:
        summary_html = m.group(1).strip()
    else:
        # Try first <p> after h1
        m = re.search(r'<h1>[^<]+</h1>\s*(?:<[^>]+>[\s\S]*?</[^>]+>\s*)*?<p>([\s\S]*?)</p>', text)
        summary_html = m.group(1).strip() if m else ''

    # Strip inner HTML tags
    summary = re.sub(r'<[^>]+>', '', summary_html)
    # Collapse whitespace
    summary = re.sub(r'\s+', ' ', summary).strip()

    if not summary:
        return ''

    # Extract first sentence, max 200 chars
    # Find first period followed by space or end
    first_sentence_match = re.match(r'^(.+?[.!?])(?:\s|$)', summary)
    if first_sentence_match:
        first_sentence = first_sentence_match.group(1)
    else:
        first_sentence = summary

    # Trim to max 200 chars
    if len(first_sentence) > 200:
        first_sentence = first_sentence[:197].rsplit(' ', 1)[0] + '...'

    # Escape HTML entities
    first_sentence = first_sentence.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    # But preserve already-encoded entities; undo the double-escape for &amp;amp;
    first_sentence = first_sentence.replace('&amp;amp;', '&amp;').replace('&amp;lt;', '&lt;').replace('&amp;gt;', '&gt;')

    return first_sentence


def fix_chapter_index(idx_path):
    """For each section card in this chapter index, replace placeholder desc."""
    text = idx_path.read_text(encoding='utf-8')
    n_changed = 0

    # Find each section-card and its desc
    def replace_section_desc(m):
        nonlocal n_changed
        prefix = m.group(1)
        href = m.group(2)
        middle = m.group(3)
        current_desc = m.group(4)
        suffix = m.group(5)

        # Only replace if current_desc matches a known placeholder
        if not PLACEHOLDER_RE.match(current_desc.strip()):
            return m.group(0)

        # Find the section file
        section_file = idx_path.parent / href
        if not section_file.exists():
            return m.group(0)

        new_desc = extract_section_summary(section_file)
        if not new_desc:
            return m.group(0)

        n_changed += 1
        return f'{prefix}{href}{middle}{new_desc}{suffix}'

    # Pattern matches the whole section-card structure to get the desc within
    # <a class="section-card" href="section-X.Y.html">...<span class="section-desc">DESC</span></a>
    text = re.sub(
        r'(<a class="section-card" href=")([^"]+)("[^>]*>[\s\S]*?<span class="section-desc">)([^<]*)(</span>)',
        replace_section_desc,
        text
    )

    if n_changed > 0:
        idx_path.write_text(text, encoding='utf-8')
    return n_changed


def main():
    total = 0
    for chapter_idx in sorted(ROOT.rglob('module-*/index.html')):
        if set(chapter_idx.parts) & SKIP:
            continue
        n = fix_chapter_index(chapter_idx)
        if n > 0:
            print(f'  {chapter_idx.relative_to(ROOT)}: {n} descriptions replaced')
            total += n
    print(f'TOTAL: {total} section descriptions replaced')


if __name__ == '__main__':
    main()
