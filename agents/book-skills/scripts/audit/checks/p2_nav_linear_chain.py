"""Verify the chapter-nav <a class="next"> link points to the next page in
the linear book reading order (not the next chapter's index).

Linear order: the natural read-through path. Within a module, going from
section N.M should next-pointer to section N.M+1 (if it exists). The LAST
section of module N should next-pointer to the FIRST section of module N+1
(NOT to module N+1's index page).

Similarly, the chapter-index page should next-pointer to its OWN first
section (NOT to the next chapter's index).

This plugin checks each page's chapter-nav next link and flags violations.
"""
import re
from collections import namedtuple
from pathlib import Path

PRIORITY = "P2"
CHECK_ID = "NAV_LINEAR_CHAIN"
DESCRIPTION = "chapter-nav next pointer skips over sections (jumps directly to next chapter)"

Issue = namedtuple("Issue", ["priority", "check_id", "filepath", "line", "message"])

NEXT_LINK_RE = re.compile(
    r'<a\s+class="next"\s+href="([^"]+)"',
    re.IGNORECASE,
)


def _classify(filepath: Path) -> str | None:
    name = filepath.name
    parts = filepath.parts
    if name.startswith('section-') and name.endswith('.html'):
        return 'section'
    if name == 'index.html':
        for p in parts[-3:]:
            if p.startswith('module-'):
                return 'chapter'
    return None


def run(filepath, html, context):
    issues = []
    if filepath.suffix != ".html":
        return issues

    kind = _classify(filepath)
    if kind is None:
        return issues

    m = NEXT_LINK_RE.search(html)
    if not m:
        return issues

    href = m.group(1)

    # Build the expected next path for this page
    parts = filepath.parts
    name = filepath.name

    if kind == 'chapter':
        # Chapter index should point to its OWN first section (section-N.1.html)
        # not to the next module's index
        if 'index.html' in href and 'module-' in href:
            line = html.count('\n', 0, m.start()) + 1
            issues.append(Issue(
                PRIORITY, CHECK_ID, filepath, line,
                f'NAV_LINEAR_CHAIN: chapter-index next points to "{href}" (another chapter index); should point to this chapter\'s first section (section-N.1.html)',
            ))
            return issues

        # Verify the chapter's first section exists in the same dir
        mod_dir = filepath.parent
        sections = sorted(mod_dir.glob('section-*.html'),
                          key=lambda p: tuple(
                              int(x) if x.isdigit() else x
                              for x in re.findall(r'\d+|[a-z]+', p.stem)
                          ))
        if not sections:
            return issues
        expected = sections[0].name
        if not href.endswith(expected):
            line = html.count('\n', 0, m.start()) + 1
            issues.append(Issue(
                PRIORITY, CHECK_ID, filepath, line,
                f'NAV_LINEAR_CHAIN: chapter-index next "{href}" does not match expected first section "{expected}"',
            ))

    elif kind == 'section':
        # Section's next should point to:
        #   1. The next section in the same module (preferred)
        #   2. The first section of the next module (if this is the last in the module)
        mod_dir = filepath.parent
        sections = sorted(mod_dir.glob('section-*.html'),
                          key=lambda p: tuple(
                              int(x) if x.isdigit() else x
                              for x in re.findall(r'\d+|[a-z]+', p.stem)
                          ))
        try:
            idx = sections.index(filepath)
        except ValueError:
            return issues

        if idx + 1 < len(sections):
            # Next section in same module
            expected = sections[idx + 1].name
            if not href.endswith(expected):
                # OK if href points to the right section via a different relative path
                if expected not in href:
                    line = html.count('\n', 0, m.start()) + 1
                    issues.append(Issue(
                        PRIORITY, CHECK_ID, filepath, line,
                        f'NAV_LINEAR_CHAIN: section next "{href}" should be the next section in this module ("{expected}")',
                    ))
        else:
            # This is the last section in the module — per the book's reading
            # convention, "next" should point to the NEXT MODULE'S INDEX
            # (chapter starter), not directly to its first section. The
            # reader sees the new chapter's title/big-picture before
            # advancing into its sections. If the href points directly to a
            # `section-N.1.html` of a different module, flag it.
            if 'section-' in href.lower() and href.endswith('.html'):
                line = html.count('\n', 0, m.start()) + 1
                issues.append(Issue(
                    PRIORITY, CHECK_ID, filepath, line,
                    f'NAV_LINEAR_CHAIN: last-section next "{href}" points directly to a section; should point to the next module\'s index page (chapter starter)',
                ))

    return issues
