"""Wave 34a: Auto-link `What's Next` paragraphs to the next section.

For each `<div class="whats-next">` block in section-X.Y.html that contains
no `<a href>`, insert a leading link to section-X.(Y+1).html. We don't
overwrite author prose; we prepend an "In the next section, <a>...</a>"
sentence so the reader has a clickable path forward.

If section-X.(Y+1).html doesn't exist (this was the chapter's last section),
we skip - the chapter-nav at the bottom already provides forward navigation.
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'.git', 'node_modules', 'KDP', 'build', 'source_fix_backups', 'pagefind',
        '.book-update', 'vendor', '.claude', '_archive', 'agents', 'templates',
        'docs', 'scripts'}

WHATS_NEXT_RE = re.compile(
    r'(<div\s+class="whats-next"[^>]*>)([\s\S]*?)(</div>\s*)'
    r'(?=<div|<h[1-6]|<nav|<details|<section)',
    re.IGNORECASE,
)
SECTION_FILE_RE = re.compile(r'section-(\d+)\.(\d+)\.html')
H2_RE = re.compile(r'<h[12][^>]*>([^<]+)</h[12]>')


def extract_next_title(next_file: Path) -> str:
    """Extract the first <h1> or main heading from the next section."""
    try:
        text = next_file.read_text(encoding='utf-8', errors='replace')
    except OSError:
        return 'the next section'
    # Get the <h1> immediately after </header>
    m = re.search(r'<h1[^>]*>([^<]+)</h1>', text)
    if m:
        return m.group(1).strip()
    return 'the next section'


def fix_file(p: Path) -> int:
    m_file = SECTION_FILE_RE.match(p.name)
    if not m_file:
        return 0
    chapter = m_file.group(1)
    section = int(m_file.group(2))
    next_file = p.parent / f'section-{chapter}.{section + 1}.html'

    if not next_file.exists():
        return 0

    text = p.read_text(encoding='utf-8')
    if 'whats-next' not in text:
        return 0

    next_title = extract_next_title(next_file)
    next_section_num = f'{chapter}.{section + 1}'

    def repl(m: re.Match) -> str:
        open_div, body, close_div = m.group(1), m.group(2), m.group(3)
        # If body already contains an <a href>, skip
        if '<a ' in body or '<a\t' in body:
            return m.group(0)
        # Inject a leading paragraph with the link
        link = (
            f'<p>In the next section, '
            f'<a href="section-{next_section_num}.html">'
            f'Section {next_section_num}: {next_title}</a>, '
            f'we continue.</p>\n'
        )
        # Find the end of the <h2> heading inside the block (canonical structure)
        # and inject AFTER the h2 but BEFORE the existing prose.
        h2m = re.search(r'(</h2>\s*)', body)
        if h2m:
            new_body = body[:h2m.end()] + link + body[h2m.end():]
        else:
            new_body = link + body
        return open_div + new_body + close_div

    new, n = WHATS_NEXT_RE.subn(repl, text)
    if n > 0 and new != text:
        p.write_text(new, encoding='utf-8')
    return n


def main():
    n_files = 0
    n_total = 0
    for p in sorted(ROOT.rglob('section-*.html')):
        if set(p.parts) & SKIP:
            continue
        n = fix_file(p)
        if n > 0:
            n_files += 1
            n_total += n
            print(f'  {p.relative_to(ROOT)}: linked')
    print(f'\nLinked {n_total} What\'s Next blocks in {n_files} files')


if __name__ == '__main__':
    main()
