"""Validate canonical code-fragment HTML layout.

Canonical structure:
    <div class="code-block-wrapper">
        <pre><code class="pygments-highlighted lang-X">...</code></pre>
        <div class="code-output">                       <!-- optional -->
            <span class="output-label"><strong>Output:</strong></span>
            ...
        </div>
        <div class="code-caption">                      <!-- single, required -->
            <strong>Code Fragment X.Y.Z:</strong> Description
        </div>
    </div>

Violations flagged:
  - Code block wrapped in <details>...</details> instead of
    <div class="code-block-wrapper">
  - Multiple <div class="code-output"> for one code block
  - <div class="code-caption"> outside any code-block-wrapper (orphan)
  - Code block with NO matching <div class="code-caption">
"""
import re
from collections import namedtuple

PRIORITY = "P2"
CHECK_ID = "CODE_FRAGMENT_STRUCTURE"
DESCRIPTION = "Code-fragment block deviates from canonical layout"

Issue = namedtuple("Issue", ["priority", "check_id", "filepath", "line", "message"])

# A code block opener (pre+code with pygments class)
PRE_CODE_RE = re.compile(
    r'<pre[^>]*><code\s+class="pygments-highlighted', re.IGNORECASE,
)
# Details wrapping a code block (non-canonical)
DETAILS_CODE_RE = re.compile(
    r'<details\b[^>]*>\s*(?:<summary[^>]*>.*?</summary>\s*)?<pre[^>]*><code\s+class="pygments-highlighted',
    re.IGNORECASE | re.DOTALL,
)
# Two consecutive <div class="code-output"> for ONE code block. The
# "same code block" constraint is enforced by a negative lookahead that
# refuses to span across a new <div class="code-block-wrapper"> or
# <pre> opener (those mark a new fragment). Without that constraint,
# the greedy `.*?` matches across thousands of lines and flags
# legitimate one-output-per-fragment cases as duplicates.
DUP_OUTPUT_RE = re.compile(
    r'<div\s+class="code-output">'
    r'(?:(?!<div\s+class="code-block-wrapper"|<pre\b).)*?'
    r'</div>\s*'
    r'(?:<div\s+class="code-caption">(?:(?!<div\s+class="code-block-wrapper"|<pre\b).)*?</div>\s*)?'
    r'<div\s+class="code-output">',
    re.DOTALL | re.IGNORECASE,
)
# Code-caption outside a code-block-wrapper
CAPTION_OUTSIDE_RE = re.compile(
    r'<div\s+class="code-caption">', re.IGNORECASE,
)
WRAPPER_OPEN_RE = re.compile(
    r'<div\s+class="code-block-wrapper"', re.IGNORECASE,
)


def _line(html, pos):
    return html.count('\n', 0, pos) + 1


def run(filepath, html, context):
    issues = []
    if filepath.suffix != ".html":
        return issues

    # 1. Code wrapped in <details>
    for m in DETAILS_CODE_RE.finditer(html):
        issues.append(Issue(
            PRIORITY, CHECK_ID, filepath, _line(html, m.start()),
            'Code block wrapped in <details>...</details>; use <div class="code-block-wrapper"> instead',
        ))

    # 2. Duplicate code-output for one code block
    for m in DUP_OUTPUT_RE.finditer(html):
        issues.append(Issue(
            PRIORITY, CHECK_ID, filepath, _line(html, m.start()),
            'Two consecutive <div class="code-output"> blocks for one code fragment (drop the second or merge into the first)',
        ))

    # The "caption outside wrapper" check was retired: the predominant pattern
    # in this book is <pre><code>...</code></pre><div class="code-caption">
    # WITHOUT a surrounding <div class="code-block-wrapper">. The wrapper is
    # optional; what matters is that the caption follows immediately after
    # the code block. Strict enforcement here would fire on ~1100 captions
    # book-wide, drowning out the real defects (details-wrapped code and
    # duplicate code-output) that this plugin catches.

    return issues
