"""Detect code blocks without an associated caption.

Book convention: every <pre><code> block in a section should be followed
(within ~5 lines) by a <div class="code-caption"> or <figcaption>
explaining what the code does. Bare <pre><code>...</code></pre> with
only a code-output div after it is the bug.

Skips:
  - <pre> blocks inside callouts (lab, key-insight, library-shortcut)
    where the callout's title serves as the caption
  - Section pages with <h1 class="page-title"> Code or Code Fragment
    style (rare)
  - Tools-of-the-trade catalogs (intentionally dense reference)
  - Inline <code> (only block-level <pre><code> is checked)
"""
import re
from collections import namedtuple

PRIORITY = "P2"
CHECK_ID = "CODE_NO_CAPTION"
DESCRIPTION = "Code block has no associated <div class=\"code-caption\">"

Issue = namedtuple("Issue", ["priority", "check_id", "filepath", "line", "message"])

PRE_RE = re.compile(r'<pre\b[^>]*>(.*?)</pre>', re.DOTALL | re.IGNORECASE)
# Accept either of the historically used caption forms (both ship valid
# captions; only true MISSING cases should flag):
#   <div class="code-caption">  (canonical)
#   <p class="figure-caption">  (legacy form from earlier editions; the
#                                build pipeline keeps it as-is)
#   <figcaption>                (semantic HTML5 form)
CAPTION_RE = re.compile(
    r'class="(?:code-caption|figure-caption)"|<figcaption\b',
    re.IGNORECASE,
)
CALLOUT_OPEN_RE = re.compile(
    r'<div\s+class="callout\s+(lab|key-insight|library-shortcut|hands-on|production-pattern|numeric-example|exercise)"',
    re.IGNORECASE,
)


def run(filepath, html, context):
    issues = []
    if not filepath.name.startswith("section-"):
        return issues

    book_root = context["book_root"]
    rel = str(filepath.relative_to(book_root)).replace("\\", "/").lower()
    # Skip tools-of-the-trade catalogs and appendices
    if (re.search(r'/module-\d+[ab]?-tools-of-the-trade/', rel)
            or re.search(r'/module-\d+[ab]?-(?:scale|retrieval|conv-ai|responsible-ai)-tools/', rel)
            or '/appendices/' in rel
            or '/appendix-' in rel):
        return issues

    for m in PRE_RE.finditer(html):
        pre_start = m.start()
        pre_end = m.end()
        # Skip if inside a callout that legitimately wraps code (lab, etc.)
        before = html[:pre_start]
        # Walk back to find the closest unclosed callout opening
        # (depth-aware would be ideal; this is a heuristic)
        last_callout_open = -1
        for cm in CALLOUT_OPEN_RE.finditer(before):
            last_callout_open = cm.start()
        if last_callout_open != -1:
            # Check whether </div> closes the callout before our <pre>
            between = before[last_callout_open:pre_start]
            opens = len(re.findall(r'<div\b', between))
            closes = len(re.findall(r'</div>', between))
            if opens > closes:
                # We're still inside a callout that legitimately wraps code
                continue

        # Look for code-caption within ~600 chars after </pre>
        window = html[pre_end:pre_end + 600]
        if CAPTION_RE.search(window):
            continue

        line_num = html[:pre_start].count('\n') + 1
        issues.append(Issue(
            PRIORITY, CHECK_ID, filepath, line_num,
            "Code block has no <div class=\"code-caption\"> within 600 chars after </pre>"
        ))
    return issues
