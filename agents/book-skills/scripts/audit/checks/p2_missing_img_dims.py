"""Check for <img> tags missing width or height attributes (causes layout shift).

The img-tag regex must handle quoted attribute values that may contain
HTML/markup characters. For example, `<img alt="<strong>Figure 9.2.3</strong>: ..." src="...">`
must capture src correctly even though alt contains `>`. Naive
`<img\\b[^>]*>` matching truncates at the first `>` inside alt and the
audit reports `src="(unknown)"`. Robust regex respects quote boundaries.
"""
import re
from collections import namedtuple

PRIORITY = "P2"
CHECK_ID = "MISSING_IMG_DIMS"
DESCRIPTION = "<img> tag missing width or height attributes"

Issue = namedtuple("Issue", ["priority", "check_id", "filepath", "line", "message"])

# Match <img attr-list /?>, where attr-list is a sequence of:
#  - characters that aren't ">" or a quote, OR
#  - a "...." double-quoted attribute value, OR
#  - a '...' single-quoted attribute value.
# This lets alt="<strong>...</strong>" appear in attrs without truncating.
IMG_RE = re.compile(
    r'''<img\b((?:[^>"']|"[^"]*"|'[^']*')*)/?>''',
    re.IGNORECASE | re.DOTALL,
)
SRC_RE = re.compile(r'src=["\']([^"\']+)["\']')


def run(filepath, html, context):
    issues = []
    for m in IMG_RE.finditer(html):
        attrs = m.group(1)
        has_width = "width=" in attrs
        has_height = "height=" in attrs
        if not has_width or not has_height:
            src_m = SRC_RE.search(attrs)
            src = src_m.group(1)[:50] if src_m else "(unknown)"
            missing = []
            if not has_width:
                missing.append("width")
            if not has_height:
                missing.append("height")
            line_no = html.count("\n", 0, m.start()) + 1
            issues.append(Issue(PRIORITY, CHECK_ID, filepath, line_no,
                f'<img src="{src}"> missing {", ".join(missing)}'))
    return issues
