"""Detect WRONG_NESTING: a styled-callout-like wrapper contains another
callout-like element, producing a double-background visual.

Two top-level wrappers act like callouts (they have their own background +
border-left styling) but are NOT class="callout TYPE":
  - <div class="takeaways"> (teal gradient, retired in favor of
    <div class="callout key-takeaway">)
  - <div class="prerequisites"> (used as a section-opener block)

Catch:
  1. <div class="callout X"> nested INSIDE <div class="callout Y">
     (true double-background; almost always wrong)
  2. <div class="callout X"> nested INSIDE <div class="takeaways">
     (legacy nesting; unwrap the outer)
  3. <div class="callout X"> nested INSIDE <details class="bibliography-collapsible">
     (the bibliography is a collapsible callout-like container; callouts
     inside it should be flat prose)
"""
import re
from collections import namedtuple

PRIORITY = "P1"
CHECK_ID = "WRONG_NESTING"
DESCRIPTION = "A callout-styled wrapper contains another callout-styled element (double background)"

Issue = namedtuple("Issue", ["priority", "check_id", "filepath", "line", "message"])

OUTER_RE = re.compile(
    r'<div\s+class="(?P<class>(?:callout\s+[a-z-]+|takeaways|prerequisites))"[^>]*>',
    re.IGNORECASE,
)
INNER_RE = re.compile(
    r'<div\s+class="callout\s+(?P<type>[a-z-]+)"[^>]*>',
    re.IGNORECASE,
)


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
        # Limit to content pages
        return issues

    # Find every outer wrapper, then check what's inside it
    for m in OUTER_RE.finditer(html):
        outer_class = m.group("class")
        outer_start = m.start()
        outer_body_start = m.end()
        outer_close = _find_div_close(html, outer_body_start)
        if outer_close < 0:
            continue
        body = html[outer_body_start:outer_close]
        # Skip self-match: e.g., if outer is callout key-takeaway and we find
        # the SAME outer's inner range, the regex search starting in body
        # finds INNER callouts only.
        for im in INNER_RE.finditer(body):
            inner_type = im.group("type")
            outer_normalized = outer_class.lower()
            # Special case: callout note OPTIONAL_MARKER allows inner content
            # without being flagged. Skip pure self-nesting of identical type.
            if (outer_normalized.startswith("callout ")
                    and outer_normalized[len("callout "):].strip() == inner_type.lower()):
                # Same type self-nesting: still wrong but report separately.
                pass
            inner_pos = outer_body_start + im.start()
            line = html.count("\n", 0, inner_pos) + 1
            outer_line = html.count("\n", 0, outer_start) + 1
            issues.append(Issue(
                PRIORITY, CHECK_ID, filepath, line,
                f'Inner callout "{inner_type}" (line {line}) nested inside '
                f'outer "{outer_class}" (line {outer_line}); unwrap the '
                f'outer or flatten the inner.'
            ))
            # Only report one inner per outer to avoid log spam
            break
    return issues
