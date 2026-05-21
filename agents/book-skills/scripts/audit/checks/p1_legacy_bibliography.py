"""Detect legacy bibliography format: `<h2>Bibliography</h2><ul class="bibliography">`.

The current canonical is `<details class="bibliography-collapsible" open>`
with `<summary><strong>Further Reading</strong></summary>`, `<section class="bibliography">`,
and `<div class="bib-entry-card"><div class="bib-ref">...</div></div>` cards.

Files still using `<h2 id="bibliography">Bibliography</h2>` followed by
`<ul class="bibliography">` need conversion. Often appears as a bare `<h2>`
right before another `<details>` block, producing the visual "double header"
the user reported.
"""
import re
from collections import namedtuple

PRIORITY = "P1"
CHECK_ID = "LEGACY_BIBLIOGRAPHY"
DESCRIPTION = "Legacy bibliography format (<h2>Bibliography</h2> + <ul class=\"bibliography\">) instead of <details class=\"bibliography-collapsible\">"

Issue = namedtuple("Issue", ["priority", "check_id", "filepath", "line", "message"])

# Legacy heading inside content area. Only h2 (h3 inside <details> is a legitimate
# sub-category like "Statistical Methods" / "Textbooks" within the bibliography).
H2_LEGACY = re.compile(
    r'<h2[^>]*>\s*(Bibliography|References|Further Reading|Bibliography and Further Reading|References and Further Reading|Annotated Bibliography)\s*</h2>',
    re.IGNORECASE,
)
# Legacy <ul class="bibliography"> or <ol class="bib-list">
UL_LEGACY = re.compile(r'<(ul|ol)\s+class\s*=\s*"(bibliography|bib-list)[^"]*"', re.IGNORECASE)
# Canonical collapsible details block
CANONICAL = re.compile(r'<details\s+class\s*=\s*"bibliography-collapsible"', re.IGNORECASE)


def _line(html, pos):
    return html.count("\n", 0, pos) + 1


def run(filepath, html, context):
    issues = []
    if filepath.suffix != ".html":
        return issues

    # Skip files that have no bibliography at all
    has_canonical = bool(CANONICAL.search(html))
    h2_m = H2_LEGACY.search(html)
    ul_m = UL_LEGACY.search(html)

    if not h2_m and not ul_m:
        return issues

    if h2_m and not has_canonical:
        issues.append(Issue(
            PRIORITY, CHECK_ID, filepath, _line(html, h2_m.start()),
            f'Legacy bibliography heading <h2>{h2_m.group(1)}</h2>; convert to <details class="bibliography-collapsible">',
        ))
    elif h2_m and has_canonical:
        # Both exist on same page -- duplicate / double-header
        issues.append(Issue(
            PRIORITY, CHECK_ID, filepath, _line(html, h2_m.start()),
            f'Duplicate bibliography header: bare <h2>{h2_m.group(1)}</h2> AND <details class="bibliography-collapsible"> on same page',
        ))

    if ul_m and not has_canonical:
        issues.append(Issue(
            PRIORITY, CHECK_ID, filepath, _line(html, ul_m.start()),
            f'Legacy <{ul_m.group(1)} class="{ul_m.group(2)}">; convert entries to <div class="bib-entry-card"><div class="bib-ref">',
        ))

    return issues
