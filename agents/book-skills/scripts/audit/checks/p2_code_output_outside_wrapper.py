"""Detect <div class="code-output"> not inside <div class="code-block-wrapper">.

Pattern (BAD):
  <div class="code-block-wrapper">
  <pre><code>...</code></pre>
  <div class="code-caption">Code Fragment X: ...</div>
  </div>
  <div class="code-output">...</div>   <-- OUTSIDE wrapper

Browsers render this OK but the structural canonical form is:
  <div class="code-block-wrapper">
  <pre><code>...</code></pre>
  <div class="code-output">...</div>   <-- INSIDE wrapper
  <div class="code-caption">Code Fragment X: ...</div>
  </div>

Detection: find every <div class="code-output">; check whether it sits
inside a div.code-block-wrapper by walking back to the nearest unmatched
<div class="code-block-wrapper"> opening.
"""
import re
from collections import namedtuple

PRIORITY = "P2"
CHECK_ID = "CODE_OUTPUT_OUTSIDE_WRAPPER"
DESCRIPTION = '<div class="code-output"> placed outside the surrounding code-block-wrapper'

Issue = namedtuple("Issue", ["priority", "check_id", "filepath", "line", "message"])

OUTPUT_RE = re.compile(r'<div\s+class="code-output[\s"]', re.IGNORECASE)
DIV_OPEN_RE = re.compile(r'<div\b', re.IGNORECASE)
DIV_CLOSE_RE = re.compile(r'</div>', re.IGNORECASE)
WRAPPER_OPEN_RE = re.compile(r'<div\s+class="code-block-wrapper"', re.IGNORECASE)


def run(filepath, html, context):
    issues = []
    for m in OUTPUT_RE.finditer(html):
        # Walk backwards: count <div opens and </div> closes between
        # nearest <div class="code-block-wrapper"> and this <div class="code-output">.
        # If we are inside an open wrapper, the difference will be > 0.
        before = html[:m.start()]
        # Find the LAST wrapper-open before this output
        last_wrap_open = -1
        for wm in WRAPPER_OPEN_RE.finditer(before):
            last_wrap_open = wm.start()
        if last_wrap_open == -1:
            # Never been in a wrapper
            line = html[:m.start()].count('\n') + 1
            issues.append(Issue(
                PRIORITY, CHECK_ID, filepath, line,
                '<div class="code-output"> appears with no preceding <div class="code-block-wrapper">'
            ))
            continue
        # Count opens and closes between last_wrap_open and current position
        between = before[last_wrap_open:]
        opens = len(DIV_OPEN_RE.findall(between))
        closes = len(DIV_CLOSE_RE.findall(between))
        if opens <= closes:
            # Wrapper has already closed before this output
            line = html[:m.start()].count('\n') + 1
            issues.append(Issue(
                PRIORITY, CHECK_ID, filepath, line,
                '<div class="code-output"> sits outside the surrounding <div class="code-block-wrapper">'
            ))
    return issues
