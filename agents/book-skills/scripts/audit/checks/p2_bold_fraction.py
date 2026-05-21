"""Detect callouts where more than X% of the body text is bold.

A callout's body should be prose with key terms occasionally bolded.
When the bold fraction is high, the callout renders as a wall of
bold text which loses the emphasis signal and reads as shouty.

Threshold: > 40% of the visible text inside <strong> or <b> tags.
"""
import re
from collections import namedtuple

PRIORITY = "P2"
CHECK_ID = "BOLD_FRACTION"
DESCRIPTION = "Callout body has too much bold text (>40% of body characters)"

Issue = namedtuple("Issue", ["priority", "check_id", "filepath", "line", "message"])

CALLOUT_OPEN_RE = re.compile(
    r'<div\s+class="callout\s+([a-z-]+)"[^>]*>',
    re.IGNORECASE,
)
TAG_RE = re.compile(r'<[^>]+>')
STRONG_RE = re.compile(
    r'<(?:strong|b)\b[^>]*>(.*?)</(?:strong|b)>',
    re.IGNORECASE | re.DOTALL,
)

# Callout types where high bold density is structurally OK (titles + bullet
# leads like in algorithm pseudocode that uses <strong> on keywords).
EXEMPT_TYPES = {
    "algorithm",      # pseudocode <strong> on keywords is canonical
    "self-check",     # questions are often bolded
    "exercise",       # exercise body has bold for variables
    "library-shortcut",  # pip install + bold library name
}


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
        if ctype in EXEMPT_TYPES:
            continue
        body_start = m.end()
        body_end = _find_div_close(html, body_start)
        if body_end < 0:
            continue
        body = html[body_start:body_end]
        # Strip the callout-title (its bold is structural, not body emphasis)
        body_minus_title = re.sub(
            r'<div\s+class="callout-title"[^>]*>.*?</div>',
            '', body, count=1, flags=re.IGNORECASE | re.DOTALL,
        )
        # Compute bold-character count vs visible-character count
        bold_chars = 0
        for sm in STRONG_RE.finditer(body_minus_title):
            text = TAG_RE.sub('', sm.group(1)).strip()
            bold_chars += len(text)
        visible_text = TAG_RE.sub('', body_minus_title).strip()
        visible_chars = len(visible_text)
        if visible_chars < 80:
            continue  # Body too short to evaluate
        frac = bold_chars / visible_chars
        if frac > 0.40:
            line = html.count("\n", 0, m.start()) + 1
            issues.append(Issue(
                PRIORITY, CHECK_ID, filepath, line,
                f'Callout "{ctype}" has {bold_chars}/{visible_chars} bold '
                f'chars ({frac:.0%} > 40%); reduce bold for emphasis to land'
            ))
    return issues
