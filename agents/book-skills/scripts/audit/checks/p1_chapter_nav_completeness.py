"""Detect chapter-nav (footer navigation) that's incomplete or non-canonical.

Canonical:
    <nav class="chapter-nav">
    <a class="prev" href="..."><span class="nav-label">Previous</span><span class="nav-num">...</span><span class="nav-title">...</span></a>
    <a class="up"   href="..."><span class="nav-label">In Chapter</span><span class="nav-num">...</span><span class="nav-title">...</span></a>
    <a class="next" href="..."><span class="nav-label">Next</span><span class="nav-num">...</span><span class="nav-title">...</span></a>
    </nav>

Exceptions:
  - First section of book: no prev allowed
  - Last section of book: no next allowed
  - Module/part index pages: don't need this nav (they have card grids)

Flag a section page that's:
  - missing the chapter-nav entirely
  - missing prev/up/next when it should have them
  - has block but wrong order (next before prev, etc.)
"""
import re
from collections import namedtuple

PRIORITY = "P1"
CHECK_ID = "CHAPTER_NAV_INCOMPLETE"
DESCRIPTION = "Chapter-nav (footer prev/up/next) missing, incomplete, or non-canonical"

Issue = namedtuple("Issue", ["priority", "check_id", "filepath", "line", "message"])

NAV_RE = re.compile(r'<nav\s+class="chapter-nav"[^>]*>([\s\S]*?)</nav>', re.IGNORECASE)
LINK_RE = re.compile(
    r'<a\s+class="(prev|up|next)"[^>]*href="[^"]*"[^>]*>[\s\S]*?</a>',
    re.IGNORECASE,
)


def _line(html, pos):
    return html.count("\n", 0, pos) + 1


def run(filepath, html, context):
    issues = []
    if filepath.suffix != ".html":
        return issues
    if not filepath.name.startswith("section-"):
        return issues

    nav = NAV_RE.search(html)
    if not nav:
        issues.append(Issue(
            PRIORITY, CHECK_ID, filepath, 0,
            'Section missing <nav class="chapter-nav"> (prev/up/next footer navigation)',
        ))
        return issues

    body = nav.group(1)
    links = LINK_RE.findall(body)
    classes = set(links)
    line = _line(html, nav.start())

    if 'up' not in classes:
        issues.append(Issue(
            PRIORITY, CHECK_ID, filepath, line,
            'Chapter-nav missing <a class="up"> link to chapter index',
        ))

    # Check ordering: prev should come before up, up before next.
    ordered = [c for c in links if c in ('prev', 'up', 'next')]
    if ordered != sorted(ordered, key=lambda c: ['prev', 'up', 'next'].index(c)):
        issues.append(Issue(
            PRIORITY, CHECK_ID, filepath, line,
            f'Chapter-nav link order is {ordered}; canonical is [prev?, up, next?]',
        ))

    # Detect missing prev for non-first sections (heuristic: section-N.M where M>1 should have prev)
    m = re.match(r'section-(\d+)\.(\d+)\.html', filepath.name)
    if m and 'prev' not in classes:
        section_num = int(m.group(2))
        if section_num > 1:
            issues.append(Issue(
                PRIORITY, CHECK_ID, filepath, line,
                f'Section {m.group(1)}.{section_num} should have <a class="prev"> link (not first section in chapter)',
            ))

    return issues
