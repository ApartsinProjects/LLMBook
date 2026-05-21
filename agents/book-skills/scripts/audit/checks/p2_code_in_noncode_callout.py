"""Detect <pre><code> code blocks nested inside callouts that aren't
designed to wrap code.

Code-friendly callouts: lab, library-shortcut, algorithm, key-insight,
hands-on, production-pattern, numeric-example, exercise, demo.

Bad callouts: note, warning, tip, fun-note, big-picture, cross-ref,
key-takeaway, see-also, looking-back. These should NOT contain raw
<pre> blocks; code there causes visual nesting confusion.

Detection: when a <div class="callout TYPE"> opens for a non-code-friendly
TYPE, check whether any <pre> appears before the matching </div>.
"""
import re
from collections import namedtuple

PRIORITY = "P2"
CHECK_ID = "CODE_IN_NONCODE_CALLOUT"
DESCRIPTION = "<pre><code> code block placed inside a callout type that should not wrap code"

Issue = namedtuple("Issue", ["priority", "check_id", "filepath", "line", "message"])

CODE_FRIENDLY = {
    'lab', 'library-shortcut', 'algorithm', 'key-insight', 'hands-on',
    'production-pattern', 'numeric-example', 'exercise', 'demo',
    'postmortem',  # postmortem callouts often quote logs / code
}


def run(filepath, html, context):
    issues = []
    if not filepath.name.endswith('.html'):
        return issues

    callout_open_re = re.compile(
        r'<div\s+class="callout\s+([\w-]+)"',
        re.IGNORECASE,
    )
    div_open_re = re.compile(r'<div\b', re.IGNORECASE)
    div_close_re = re.compile(r'</div>', re.IGNORECASE)
    pre_re = re.compile(r'<pre\b', re.IGNORECASE)

    for m in callout_open_re.finditer(html):
        ctype = m.group(1).lower()
        if ctype in CODE_FRIENDLY:
            continue
        # Walk forward to find matching </div>
        i = m.end()
        depth = 1
        while i < len(html) and depth > 0:
            o = div_open_re.search(html, i)
            c = div_close_re.search(html, i)
            if not c:
                break
            if o and o.start() < c.start():
                depth += 1
                i = o.end()
            else:
                depth -= 1
                i = c.end()
        callout_end = i
        # Check for <pre> within this callout
        between = html[m.start():callout_end]
        pre_m = pre_re.search(between)
        if pre_m:
            line = html[:m.start() + pre_m.start()].count('\n') + 1
            issues.append(Issue(
                PRIORITY, CHECK_ID, filepath, line,
                f'<pre> code block inside callout type "{ctype}" '
                f'(open at line {html[:m.start()].count(chr(10)) + 1}); move out or use a code-friendly callout type'
            ))
    return issues
