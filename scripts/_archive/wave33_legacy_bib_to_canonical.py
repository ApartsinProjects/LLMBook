"""Wave 33b: Convert legacy `<h2>Bibliography</h2><ul class="bibliography">`
to canonical `<details class="bibliography-collapsible" open>` structure.

Plugin LEGACY_BIBLIOGRAPHY flags 36 real files book-wide (mostly modules
48, 54, 59). Canonical format observed in section-42.2.html:770-784:

    <details class="bibliography-collapsible" open>
    <summary><strong>Further Reading</strong></summary>
    <section class="bibliography">
    <h3 id="...">Subsection</h3>
    <div class="bib-entry-card">
    <div class="bib-ref">Author (YYYY). "Title." <a href="...">venue</a></div>
    </div>
    ...
    </section>
    </details>

The legacy format we observed:
    <h2 id="bibliography">Bibliography</h2>
    <ul class="bibliography">
    <li>Author (YYYY). <em>Title.</em> https://...</li>
    ...
    </ul>

This script:
  1. Replaces the <h2> heading with the canonical <details><summary> wrapper open
  2. Converts <ul class="bibliography"> -> <section class="bibliography">
  3. Converts each <li>...</li> -> <div class="bib-entry-card"><div class="bib-ref">...</div></div>
  4. Closes with </section></details>
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'.git', 'node_modules', 'KDP', 'build', 'temp_ebook', 'temp_epub',
        'source_fix_backups', 'pagefind', '.book-update', 'vendor',
        '.claude', '_archive', 'agents', 'templates', 'docs'}


LEGACY_BLOCK_RE = re.compile(
    r'<h2\s+id="bibliography"[^>]*>\s*Bibliography\s*</h2>\s*'
    r'(<ul\s+class="bibliography"[^>]*>)([\s\S]*?)(</ul>)',
    re.IGNORECASE,
)

# Module-59 variant: <section class="bibliography"><h2>Bibliography</h2><ol>...</ol></section>
SECTION_BIB_RE = re.compile(
    r'<section\s+class="bibliography"[^>]*>\s*'
    r'<h2[^>]*>\s*Bibliography\s*</h2>\s*'
    r'(<ol[^>]*>)([\s\S]*?)(</ol>)\s*'
    r'</section>',
    re.IGNORECASE,
)


def convert_li_to_card(li_html: str) -> str:
    """Convert <li>...</li> to canonical <div class="bib-entry-card">."""
    inner = re.sub(r'^\s*<li[^>]*>', '', li_html).strip()
    inner = re.sub(r'</li>\s*$', '', inner).strip()
    # Convert bare URLs to anchors (basic)
    inner = re.sub(
        r'(?<![">])(https?://[^\s<]+)',
        lambda m: f'<a href="{m.group(1)}" rel="noopener" target="_blank">{m.group(1)}</a>',
        inner,
    )
    return f'<div class="bib-entry-card">\n<div class="bib-ref">{inner}</div>\n</div>'


def convert_block(match: re.Match) -> str:
    ul_open, ul_body, ul_close = match.group(1), match.group(2), match.group(3)
    # Extract <li> entries
    lis = re.findall(r'<li[^>]*>[\s\S]*?</li>', ul_body)
    cards = '\n'.join(convert_li_to_card(li) for li in lis)
    return (
        '<details class="bibliography-collapsible" open>\n'
        '<summary><strong>Further Reading</strong></summary>\n'
        '<section class="bibliography">\n'
        f'{cards}\n'
        '</section>\n'
        '</details>'
    )


def convert_section_block(match: re.Match) -> str:
    """Convert <section class="bibliography"><h2>Bibliography</h2><ol>...</ol></section>."""
    ol_body = match.group(2)
    lis = re.findall(r'<li[^>]*>[\s\S]*?</li>', ol_body)
    cards = '\n'.join(convert_li_to_card(li) for li in lis)
    return (
        '<details class="bibliography-collapsible" open>\n'
        '<summary><strong>Further Reading</strong></summary>\n'
        '<section class="bibliography">\n'
        f'{cards}\n'
        '</section>\n'
        '</details>'
    )


def fix(text: str) -> tuple[str, int]:
    new, n1 = LEGACY_BLOCK_RE.subn(convert_block, text)
    new, n2 = SECTION_BIB_RE.subn(convert_section_block, new)
    return new, n1 + n2


def main():
    n_files = 0
    n_total = 0
    for p in sorted(ROOT.rglob('*.html')):
        if set(p.parts) & SKIP:
            continue
        text = p.read_text(encoding='utf-8')
        new, n = fix(text)
        if n > 0:
            p.write_text(new, encoding='utf-8')
            n_files += 1
            n_total += n
            print(f'  {p.relative_to(ROOT)}: {n} legacy block(s) converted')
    print(f'\nConverted {n_total} legacy bibliography block(s) in {n_files} files')


if __name__ == '__main__':
    main()
