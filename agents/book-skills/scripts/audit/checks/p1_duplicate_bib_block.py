"""Detect duplicate / nested bibliography blocks: more than one
`<details class="bibliography-collapsible">` on the same page, OR a bare
`<h2>References / Further Reading>` AND a canonical `<details>` block both present.

This catches the "double header" pattern the user reported on screenshots:
nested "References and Further Reading" headings stacked.
"""
import re
from collections import namedtuple

PRIORITY = "P1"
CHECK_ID = "DUP_BIB_BLOCK"
DESCRIPTION = "Duplicate bibliography blocks on same page (legacy <h2> + canonical <details>, or multiple <details>)"

Issue = namedtuple("Issue", ["priority", "check_id", "filepath", "line", "message"])

CANONICAL = re.compile(r'<details\s+class\s*=\s*"bibliography-collapsible"', re.IGNORECASE)
LEGACY_H2 = re.compile(
    r'<h2[^>]*>\s*(Bibliography|References|Further Reading|Bibliography and Further Reading|References and Further Reading)\s*</h2>',
    re.IGNORECASE,
)


def _line(html, pos):
    return html.count("\n", 0, pos) + 1


def run(filepath, html, context):
    issues = []
    if filepath.suffix != ".html":
        return issues

    canonicals = list(CANONICAL.finditer(html))
    if len(canonicals) > 1:
        for m in canonicals[1:]:
            issues.append(Issue(
                PRIORITY, CHECK_ID, filepath, _line(html, m.start()),
                f'Multiple <details class="bibliography-collapsible"> blocks ({len(canonicals)} total); merge into one',
            ))

    h2s = list(LEGACY_H2.finditer(html))
    if canonicals and h2s:
        for m in h2s:
            issues.append(Issue(
                PRIORITY, CHECK_ID, filepath, _line(html, m.start()),
                f'Bare <h2>{m.group(1)}</h2> alongside canonical <details>; remove the legacy <h2>',
            ))

    return issues
