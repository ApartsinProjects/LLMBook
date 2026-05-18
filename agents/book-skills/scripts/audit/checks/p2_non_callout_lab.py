"""Detect h2/h3 headings that announce a Lab but the content that follows
is NOT wrapped in <div class="callout lab">.

Canonical lab structure is:
  <h2 id="X.Y.Z-lab-...">X.Y.Z Lab: Title</h2>
  <div class="callout lab">
    <div class="callout-title">Lab: Title</div>
    <h3>Objective</h3> ...
    <h3>Steps</h3> ...
  </div>

Catch headings matching "Lab:" or "Hands-On Lab" without a sibling
callout.lab nearby.
"""
import re
from collections import namedtuple

PRIORITY = "P2"
CHECK_ID = "NON_CALLOUT_LAB"
DESCRIPTION = "Lab heading not followed by a <callout lab> block"

Issue = namedtuple("Issue", ["priority", "check_id", "filepath", "line", "message"])

LAB_HEADING_RE = re.compile(
    r'<(?P<tag>h[23])\b[^>]*>(?P<text>[^<]*(?:Lab|Hands-On)[^<]*)</(?P=tag)>',
    re.IGNORECASE,
)


def run(filepath, html, context):
    issues = []
    if filepath.suffix != ".html":
        return issues
    if not filepath.name.startswith("section-"):
        return issues
    # Phrases that contain "Lab" but DO NOT refer to a hands-on coding
    # lab (so the heading is not expected to be followed by a lab
    # callout). These are noun-phrase uses of "lab" or "lab-" as a
    # research-org prefix (frontier lab, research lab, etc.).
    NON_LAB_PHRASES = (
        "lab blog",
        "lab discussion",
        "lab publication",
        "lab channel",
        "lab post",
        "frontier-lab",
        "frontier lab",
        "research lab",
        "industry lab",
        "lab infrastructure",
    )

    for m in LAB_HEADING_RE.finditer(html):
        heading_text = m.group("text").strip()
        heading_lower = heading_text.lower()
        # Must contain "Lab" (not just "Hands-On" alone)
        if not re.search(r'\bLab\b', heading_text, re.IGNORECASE):
            continue
        # Skip non-lab uses of the word
        if any(phrase in heading_lower for phrase in NON_LAB_PHRASES):
            continue
        # Look for <div class="callout lab"> within 600 chars after this heading
        window = html[m.end():m.end() + 600]
        if re.search(r'<div\s+class="callout\s+lab"', window, re.IGNORECASE):
            continue
        # Also check if THIS heading is inside a <callout lab> already
        # (lab callouts sometimes have inner h3 like "Lab: Setup")
        before = html[:m.start()]
        last_open = before.rfind('<div class="callout lab"')
        last_close = before.rfind('</div>')
        if last_open > last_close:
            # We're already inside a lab callout
            continue
        line = html.count("\n", 0, m.start()) + 1
        issues.append(Issue(
            PRIORITY, CHECK_ID, filepath, line,
            f'Lab heading "{heading_text[:60]}" is not followed by a '
            f'<div class="callout lab"> block within 600 chars; wrap '
            f'the lab content in the canonical lab callout.'
        ))
    return issues
