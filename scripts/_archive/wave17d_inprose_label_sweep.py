"""Wave 17d: rewrite in-prose visible labels for <a> elements where the href
points at a known target but the visible text uses an OLD chapter / section
number.

Patterns to fix:
  - <a href=".../module-NN-slug/index.html">Chapter OLD</a> → "Chapter NN"
  - <a href=".../module-NN-slug/section-A.B.html">Chapter OLD</a> → "Chapter NN"
  - <a href=".../module-NN-slug/section-A.B.html">Section X.Y</a> → "Section A.B"
  - <a href=".../module-NN-slug/section-A.B.html#anchor">Section X.Y</a> → "Section A.B"
  - title="Chapter OLD: ..." attributes (concept-link tooltips) → "Chapter NN: ..."

Source-of-truth: the href. We trust it (Waves 11-15 fixed hrefs); we rewrite
visible labels to match.
"""
from pathlib import Path
import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'.git', 'node_modules', 'KDP', 'build', 'temp_ebook', 'temp_epub',
        'source_fix_backups', 'pagefind', 'templates', '.claude',
        '.book-update', 'vendor', 'docs'}


# Regex to extract module number from href
HREF_MODULE_RE = re.compile(r'module-(\d+)-')
# Regex to extract section X.Y from filename in href
HREF_SECTION_RE = re.compile(r'section-(\d+)\.(\d+)\.html')


def sweep_file(file_path):
    text = file_path.read_text(encoding='utf-8')
    orig = text

    # Pattern 1: <a [attrs] href="HREF">VISIBLE</a> where VISIBLE has "Chapter X" or "Section X.Y"
    # The href can contain anchor and be relative or absolute.
    a_tag_re = re.compile(
        r'(<a\s[^>]*href=")([^"]+)("[^>]*>)([^<]+)(</a>)',
        re.DOTALL
    )

    def rewrite_a(m):
        prefix = m.group(1)
        href = m.group(2)
        attrs_end = m.group(3)
        visible = m.group(4)
        closer = m.group(5)

        # Parse module number from href
        mm = HREF_MODULE_RE.search(href)
        if not mm:
            return m.group(0)
        target_ch = mm.group(1).lstrip('0') or '0'

        # If href has section-X.Y, get target section
        sec_match = HREF_SECTION_RE.search(href)

        new_visible = visible

        if sec_match:
            target_sec = sec_match.group(2)
            # Match "Section X.Y" pattern (with optional sub-sections)
            new_visible_section = re.sub(
                r'\bSection\s+\d+\.\d+(?:\.\d+(?:\.\d+)?)?',
                f'Section {target_ch}.{target_sec}',
                new_visible
            )
            # Also match "Sections X.Y through X.Z" — but those are tricky; skip
            if new_visible_section != new_visible:
                new_visible = new_visible_section
            else:
                # If no "Section X.Y" match, maybe it's "Chapter X" pointing at a section
                new_visible = re.sub(
                    r'\bChapter\s+\d+\b',
                    f'Chapter {target_ch}',
                    new_visible
                )
        else:
            # href points at chapter index — match "Chapter X" pattern
            new_visible = re.sub(
                r'\bChapter\s+\d+\b',
                f'Chapter {target_ch}',
                new_visible
            )

        if new_visible == visible:
            return m.group(0)

        # Also rewrite title= attribute on concept-link if present
        attrs = attrs_end[:-1]  # strip trailing '>'
        new_attrs = re.sub(
            r'title="Chapter \d+(:[^"]*)?"',
            f'title="Chapter {target_ch}\\1"',
            attrs
        )
        new_attrs = re.sub(
            r'title="Section \d+\.\d+(:[^"]*)?"',
            lambda mm: (f'title="Section {target_ch}.{sec_match.group(2)}{mm.group(1) or ""}"'
                        if sec_match else mm.group(0)),
            new_attrs
        )
        return f'{prefix}{href}"{new_attrs[len("{prefix}"):]}{">"}{new_visible}{closer}' if False else \
               f'{prefix}{href}{new_attrs[len(attrs):] if new_attrs != attrs else ""}{attrs_end}'.replace(attrs_end, new_attrs + '>', 1) + new_visible + closer

    # Simpler: do the rewrite in stages

    def rewrite_simple(m):
        prefix = m.group(1)
        href = m.group(2)
        attrs_end = m.group(3)
        visible = m.group(4)
        closer = m.group(5)

        mm = HREF_MODULE_RE.search(href)
        if not mm:
            return m.group(0)
        target_ch = mm.group(1).lstrip('0') or '0'

        sec_match = HREF_SECTION_RE.search(href)
        new_visible = visible

        if sec_match:
            target_sec = sec_match.group(2)
            new_v = re.sub(
                r'\bSection\s+\d+\.\d+(?:\.\d+(?:\.\d+)?)?',
                f'Section {target_ch}.{target_sec}',
                new_visible
            )
            if new_v != new_visible:
                new_visible = new_v
            else:
                new_visible = re.sub(
                    r'\bChapter\s+\d+\b',
                    f'Chapter {target_ch}',
                    new_visible
                )
        else:
            new_visible = re.sub(
                r'\bChapter\s+\d+\b',
                f'Chapter {target_ch}',
                new_visible
            )

        if new_visible == visible:
            return m.group(0)
        return f'{prefix}{href}{attrs_end}{new_visible}{closer}'

    text = a_tag_re.sub(rewrite_simple, text)

    # Also fix title="Chapter X: ..." attributes
    def rewrite_title_attr(m):
        attrs_before = m.group(1)
        old_chap = m.group(2)
        title_rest = m.group(3)
        attrs_after_old_title = m.group(4)
        href = m.group(5) if len(m.groups()) >= 5 else ''
        # We don't have a structured way to extract href from this match; use a different pattern
        return m.group(0)

    # Pattern: title="Chapter X" or title="Chapter X: ..." inside <a> tags with href pointing to module-NN
    def rewrite_title_attrs(text):
        def replacer(m):
            full_tag = m.group(0)
            href = m.group('href')
            mm = HREF_MODULE_RE.search(href)
            if not mm:
                return full_tag
            target_ch = mm.group(1).lstrip('0') or '0'

            sec_match = HREF_SECTION_RE.search(href)

            # In the whole tag, rewrite title="Chapter X" or title="Chapter X: ..."
            new_tag = re.sub(
                r'title="Chapter \d+(:[^"]*)?"',
                lambda mm: f'title="Chapter {target_ch}{mm.group(1) or ""}"',
                full_tag
            )
            if sec_match:
                target_sec = sec_match.group(2)
                new_tag = re.sub(
                    r'title="Section \d+\.\d+(?:\.\d+)?(:[^"]*)?"',
                    lambda mm: f'title="Section {target_ch}.{target_sec}{mm.group(1) or ""}"',
                    new_tag
                )
            return new_tag

        return re.sub(
            r'<a\s[^>]*href="(?P<href>[^"]+)"[^>]*>',
            replacer,
            text
        )

    text = rewrite_title_attrs(text)

    if text != orig:
        file_path.write_text(text, encoding='utf-8')
        return True
    return False


def main():
    n_files = 0
    for p in sorted(ROOT.rglob('*.html')):
        if set(p.parts) & SKIP:
            continue
        if sweep_file(p):
            n_files += 1
    print(f'In-prose labels updated in {n_files} files')


if __name__ == '__main__':
    main()
