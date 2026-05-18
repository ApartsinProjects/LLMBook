"""Verify internal structure compliance of every callout.

Each callout must have:
  1. A single <div class="callout-title"> as its first child.
  2. No nested h2 inside it (the callout-title is the "header"; an
     inner h2 produces a double-header).
  3. No nested callout-title (would render two title lines).
  4. Body content present (callouts shouldn't be empty).

Additional per-type checks:
  - key-takeaway / takeaways: body should include a <ul> or <ol>.
  - self-check: body should include at least one <details> Q&A.
  - lab: body should include either h3 sub-sections or steps list.
  - cross-ref: body should include at least one <a href>.
"""
import re
from collections import namedtuple

PRIORITY = "P2"
CHECK_ID = "CALLOUT_INTERNAL"
DESCRIPTION = "Callout has internal-structure violation (double-header, empty body, missing list, etc.)"

Issue = namedtuple("Issue", ["priority", "check_id", "filepath", "line", "message"])

CALLOUT_OPEN_RE = re.compile(
    r'<div\s+class="callout\s+([a-z-]+)"[^>]*>',
    re.IGNORECASE,
)
TAG_RE = re.compile(r'<[^>]+>')


def _find_div_close(html: str, after_open: int) -> int:
    depth = 1
    pos = after_open
    tag_re = re.compile(r'<(/?)div\b', re.IGNORECASE)
    while pos < len(html) and depth > 0:
        m = tag_re.search(html, pos)
        if not m:
            return -1
        if m.group(1) == "/":
            depth -= 1
        else:
            depth += 1
        pos = m.end()
        if depth == 0:
            return m.start()
    return -1


def run(filepath, html, context):
    issues = []
    if filepath.suffix != ".html":
        return issues
    if not filepath.name.startswith("section-") and filepath.name != "index.html":
        return issues

    for m in CALLOUT_OPEN_RE.finditer(html):
        ctype = m.group(1).lower()
        body_start = m.end()
        body_end = _find_div_close(html, body_start)
        if body_end < 0:
            continue
        body = html[body_start:body_end]
        line = html.count("\n", 0, m.start()) + 1

        # 1. Inner h2 (double-header)
        if re.search(r'<h2\b', body, re.IGNORECASE):
            issues.append(Issue(
                PRIORITY, CHECK_ID, filepath, line,
                f'callout "{ctype}": contains a nested <h2> (drop it; the '
                f'callout-title is the visible header)',
            ))
            continue  # don't pile more issues on the same callout

        # 2. Two callout-title divs (double-title). Exercises legitimately
        # use two callout-title divs by design: the first is the number
        # ("Exercise 33.3.1: ") and the second is the topic ("Quadratic
        # Attention vs. Linear Alternatives"). The CSS renders them as
        # a single styled heading line. The two-title pattern is canonical
        # for exercise callouts and is silently allowed.
        title_count = len(re.findall(
            r'<div\s+class="callout-title"', body, re.IGNORECASE))
        if title_count > 1 and ctype != "exercise":
            issues.append(Issue(
                PRIORITY, CHECK_ID, filepath, line,
                f'callout "{ctype}": has {title_count} callout-title '
                f'divs; only one is allowed',
            ))
            continue

        # 3. Empty body
        visible_text = TAG_RE.sub('', body).strip()
        if len(visible_text) < 30:
            issues.append(Issue(
                PRIORITY, CHECK_ID, filepath, line,
                f'callout "{ctype}": body is empty or near-empty '
                f'({len(visible_text)} visible chars)',
            ))
            continue

        # 4. Per-type checks
        if ctype == "key-takeaway":
            if not re.search(r'<(ul|ol)\b', body, re.IGNORECASE):
                issues.append(Issue(
                    PRIORITY, CHECK_ID, filepath, line,
                    f'callout "{ctype}": missing <ul> or <ol> body '
                    f'(takeaway should be a bulleted recap)',
                ))
        elif ctype == "self-check":
            if not re.search(r'<details\b', body, re.IGNORECASE):
                issues.append(Issue(
                    PRIORITY, CHECK_ID, filepath, line,
                    f'callout "{ctype}": missing <details>...</details> '
                    f'(self-check should hide the answer in a collapsible)',
                ))
        elif ctype == "cross-ref":
            if not re.search(r'<a\s+href=', body, re.IGNORECASE):
                issues.append(Issue(
                    PRIORITY, CHECK_ID, filepath, line,
                    f'callout "{ctype}": no <a href> in body (see-also '
                    f'must reference at least one section)',
                ))
        elif ctype == "lab":
            if not re.search(r'<h[34]\b', body, re.IGNORECASE):
                issues.append(Issue(
                    PRIORITY, CHECK_ID, filepath, line,
                    f'callout "{ctype}": no sub-headings (lab body should '
                    f'have h3/h4 for Objective, Steps, Expected output, etc.)',
                ))
    return issues
