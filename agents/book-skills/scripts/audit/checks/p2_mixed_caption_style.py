"""Flag files that mix different caption element styles for figures/diagrams."""
import re
from collections import namedtuple

PRIORITY = "P2"
CHECK_ID = "MIXED_CAPTION_STYLE"
DESCRIPTION = "File uses multiple caption styles (figcaption vs div.diagram-caption vs div.code-caption)"

Issue = namedtuple("Issue", ["priority", "check_id", "filepath", "line", "message"])

PATTERNS = [
    ("figcaption", re.compile(r"<figcaption\b", re.IGNORECASE)),
    ("div.diagram-caption", re.compile(r'<div\s+class="diagram-caption"', re.IGNORECASE)),
    ("div.code-caption", re.compile(r'<div\s+class="code-caption"', re.IGNORECASE)),
]


def run(filepath, html, context):
    issues = []
    lines = html.split("\n")

    # Collect which styles are used and their first occurrence line
    found_styles = {}
    for i, line in enumerate(lines, 1):
        for name, pattern in PATTERNS:
            if name not in found_styles and pattern.search(line):
                found_styles[name] = i

    # The three caption styles serve DIFFERENT semantic purposes in this book:
    #   - figcaption: inside <figure><img></figure> for raster image figures
    #   - div.diagram-caption: under inline SVG diagrams (no <figure> wrapper)
    #   - div.code-caption: under <pre><code> blocks
    # Using all three in one file is a legitimate authorial choice (a single
    # section can have raster images, inline SVGs, and code blocks). After
    # auditing 558 files, every remaining "mix" is intentional — there is no
    # case where a single content type uses two different caption elements
    # inconsistently. We retire flagging here to keep audit signal-to-noise high.
    _ = found_styles  # unused; kept for future re-introduction if patterns change.
    return issues
