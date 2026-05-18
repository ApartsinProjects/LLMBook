"""Detect Library Shortcut callouts that don't include a code fragment.

A Library Shortcut's purpose is to introduce a library with a minimal
working snippet. Without code, the callout reads as a paragraph
recommendation and the reader can't see what the library actually
does. The canonical shape is:
  <div class="callout library-shortcut">
    <div class="callout-title">Library Shortcut: name</div>
    <p>pip install <code>name</code>... brief description...</p>
    <div class="code-block-wrapper">
      <pre><code>...</code></pre>
    </div>
  </div>
"""
import re
from collections import namedtuple

PRIORITY = "P2"
CHECK_ID = "LIBRARY_SHORTCUT_HAS_CODE"
DESCRIPTION = "Library Shortcut callout missing inline code snippet"

Issue = namedtuple("Issue", ["priority", "check_id", "filepath", "line", "message"])

CALLOUT_OPEN_RE = re.compile(
    r'<div\s+class="callout\s+library-shortcut"[^>]*>',
    re.IGNORECASE,
)
CODE_BLOCK_RE = re.compile(
    r'<div\s+class="code-block-wrapper"|<pre\b[^>]*>',
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
    for m in CALLOUT_OPEN_RE.finditer(html):
        body_start = m.end()
        body_end = _find_div_close(html, body_start)
        if body_end < 0:
            continue
        body = html[body_start:body_end]
        if CODE_BLOCK_RE.search(body):
            continue
        line = html.count("\n", 0, m.start()) + 1
        # Get the library name from the title
        title_m = re.search(
            r'<div\s+class="callout-title"[^>]*>([^<]+)</div>',
            body, re.IGNORECASE,
        )
        title = (title_m.group(1).strip() if title_m else "(no title)")
        issues.append(Issue(
            PRIORITY, CHECK_ID, filepath, line,
            f'Library Shortcut "{title}" has no <pre><code> snippet; '
            f'add a minimal working example or convert to a regular tip.'
        ))
    return issues
