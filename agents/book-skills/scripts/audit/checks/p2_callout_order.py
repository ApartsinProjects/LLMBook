"""Check that callouts appear in the recommended order within a section.

Recommended order (from docs/content-audit/CALLOUT_CATALOGUE.md):

  epigraph -> big-picture -> prerequisites -> body callouts ->
  research-frontier -> lab -> key-takeaway -> self-check ->
  exercises -> whats-next -> bibliography -> chapter-nav

This check verifies the SINGLETON sentinels (the seven structural callouts
that should appear at most once and in a specific position):

  big-picture must come BEFORE prerequisites
  key-takeaway must come BEFORE self-check (when both present)
  self-check must come BEFORE exercises (when both present)
  exercises must come BEFORE whats-next (when both present)
  whats-next must come BEFORE bibliography (already checked by SECTION_ORDER)
  research-frontier should come BEFORE key-takeaway (when both present)

Plural callouts (key-insight, note, tip, warning, etc.) are not ordered.
"""
import re
from collections import namedtuple

PRIORITY = "P2"
CHECK_ID = "CALLOUT_ORDER"
DESCRIPTION = "Singleton callouts appear out of recommended order"

Issue = namedtuple("Issue", ["priority", "check_id", "filepath", "line", "message"])

# Order: lower index = earlier in section
SINGLETON_ORDER = [
    ('big-picture',         r'<div\s+class="callout big-picture"'),
    ('prerequisites',       r'<div\s+class="prerequisites"'),
    ('research-frontier',   r'<div\s+class="callout research-frontier"'),
    ('lab',                 r'<div\s+class="callout lab"'),
    ('key-takeaway',        r'<div\s+class="callout key-takeaway"'),
    ('self-check',          r'<div\s+class="callout self-check"'),
    ('exercises',           r'<section\s+class="exercises"|<h2\s+id="exercises"'),
    ('whats-next',          r'<div\s+class="(?:callout\s+)?whats-next"'),
    ('bibliography',        r'<details\s+class="bibliography-collapsible'),
]


def run(filepath, html, context):
    issues = []
    if not filepath.name.startswith("section-"):
        return issues

    # Tools-of-the-trade and appendix sections have non-canonical flows
    rel = str(filepath).lower().replace('\\', '/')
    if any(x in rel for x in (
        '/tools-of-the-trade/', '/appendices/', '/appendix-',
        'module-05-tools-of-the-trade', 'module-19-tools-of-the-trade',
        'module-30-tools-of-the-trade', 'module-45-tools-of-the-trade',
        'module-51-tools-of-the-trade', 'module-61-scale-tools',
        'module-71-tools-of-the-trade', 'module-79-tools-of-the-trade',
        'module-14-tools-of-the-trade', 'module-36-retrieval-tools',
        'module-41-conv-ai-tools', 'module-56-responsible-ai-tools',
    )):
        return issues

    # Find first occurrence of each singleton sentinel
    positions = {}
    for name, pat in SINGLETON_ORDER:
        m = re.search(pat, html, re.IGNORECASE)
        if m:
            positions[name] = m.start()

    # Check pairwise ordering
    order_seq = [(name, positions[name]) for name, _ in SINGLETON_ORDER if name in positions]
    for i in range(len(order_seq) - 1):
        prev_name, prev_pos = order_seq[i]
        for j in range(i + 1, len(order_seq)):
            next_name, next_pos = order_seq[j]
            if prev_pos > next_pos:
                line = html.count('\n', 0, prev_pos) + 1
                issues.append(Issue(
                    PRIORITY, CHECK_ID, filepath, line,
                    f'CALLOUT_ORDER: "{prev_name}" appears after "{next_name}" '
                    f'(canonical: {prev_name} should precede {next_name})',
                ))
                break  # one report per misplaced sentinel

    return issues
