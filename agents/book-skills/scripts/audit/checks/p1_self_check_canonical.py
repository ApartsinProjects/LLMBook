"""Detect non-canonical self-check callouts (no embedded answers).

Canonical (per section-42.2.html and other v9 sections):

    <div class="callout self-check">
    <div class="callout-title">Self-Check</div>
    <div class="quiz-question"><strong>Q1:</strong> Question?</div>
    <details>
    <summary>Show Answer</summary>
    <div class="answer">Answer text.</div>
    </details>
    ... repeat for Q2, Q3 ...
    </div>

Non-canonical patterns flagged:
  - `<ol><li>` list of questions, no answers
  - `<div class="quiz-question">` questions but no `<details>` answer toggles
"""
import re
from collections import namedtuple

PRIORITY = "P1"
CHECK_ID = "SELFCHECK_NON_CANONICAL"
DESCRIPTION = "Self-check callout missing embedded answers (no <details><summary>Show Answer</summary>)"

Issue = namedtuple("Issue", ["priority", "check_id", "filepath", "line", "message"])

# The self-check block uses <details> elements internally for "Show Answer"
# toggles, so we cannot treat <details> as a block terminator. Instead, find
# the FULL <div class="callout self-check"> ... </div> by balanced-div matching.
SELFCHECK_OPEN_RE = re.compile(
    r'<div\s+class="callout\s+self-check"[^>]*>',
    re.IGNORECASE,
)


def _line(html, pos):
    return html.count("\n", 0, pos) + 1


def _find_matching_close(html: str, open_end: int) -> int:
    """Given the position right after `<div ...>` opener, return position
    just past the matching `</div>` (using balanced-div tracking).
    Returns -1 if unbalanced."""
    depth = 1
    pos = open_end
    while pos < len(html):
        nxt_open = html.find('<div', pos)
        nxt_close = html.find('</div>', pos)
        if nxt_close == -1:
            return -1
        if nxt_open != -1 and nxt_open < nxt_close:
            depth += 1
            pos = nxt_open + 4
        else:
            depth -= 1
            pos = nxt_close + 6
            if depth == 0:
                return pos
    return -1


def run(filepath, html, context):
    issues = []
    if filepath.suffix != ".html":
        return issues
    for m in SELFCHECK_OPEN_RE.finditer(html):
        close_pos = _find_matching_close(html, m.end())
        if close_pos == -1:
            continue
        block = html[m.end():close_pos - len('</div>')]
        has_quiz_q = '<div class="quiz-question"' in block
        has_details = '<details>' in block or '<details ' in block
        has_ol = '<ol>' in block or '<ul>' in block
        if has_quiz_q and has_details:
            continue  # canonical
        line = _line(html, m.start())
        if has_quiz_q and not has_details:
            issues.append(Issue(
                PRIORITY, CHECK_ID, filepath, line,
                'Self-check has quiz-question divs but no <details><summary>Show Answer</summary> toggles',
            ))
        elif has_ol and not has_quiz_q:
            issues.append(Issue(
                PRIORITY, CHECK_ID, filepath, line,
                'Self-check uses <ol>/<ul> list instead of <div class="quiz-question"> + <details>Show Answer</details>',
            ))
    return issues
