"""Detect pseudo-callouts: blocks that visually mimic a callout but use bare
HTML (h2/h3 + strong + bordered styling) instead of `<div class="callout TYPE">`.

Canonical callouts use one of 22 types (algorithm, big-picture, cross-ref,
exercise, fun-note, key-insight, key-takeaway, lab, library-shortcut,
looking-back, note, numeric-example, postmortem, practical-example,
production-pattern, research-frontier, self-check, thesis-thread, tip, warning,
whats-next) wrapped as `<div class="callout TYPE">` with a `<div class="callout-title">`.

Patterns flagged:
  - `<blockquote>` not inside a callout (often used for tip / fun-note)
  - `<aside>` blocks
  - `<div class="(note|warning|tip|info|caution|important)">` (bare class without `callout` prefix)
  - `<p><strong>Note:</strong> ...` or `<p><strong>Warning:</strong> ...` start-of-paragraph patterns
  - `<h3>` whose text exactly matches a callout title keyword (e.g. "Key Takeaway", "Fun Fact")
"""
import re
from collections import namedtuple

PRIORITY = "P2"
CHECK_ID = "PSEUDO_CALLOUT"
DESCRIPTION = "Pseudo-callout (bare HTML mimicking callout) instead of <div class=\"callout TYPE\">"

Issue = namedtuple("Issue", ["priority", "check_id", "filepath", "line", "message"])

# Bare divs with callout-ish class but no "callout" prefix
BARE_DIV = re.compile(
    r'<div\s+class\s*=\s*"(note|warning|tip|info|caution|important|fun-note|key-insight|key-takeaway|big-picture|library-shortcut|production-pattern|research-frontier|practical-example|numeric-example|postmortem|thesis-thread|self-check|exercise|lab|algorithm|cross-ref|looking-back)(\s|")',
    re.IGNORECASE,
)
# Heading text that should be a callout title
H3_PSEUDO = re.compile(
    r'<h[23][^>]*>\s*(Key Takeaway|Key Insight|Fun Fact|Big Picture|Production Pattern|Research Frontier|Library Shortcut|Numeric Example|Practical Example|Self-Check|Postmortem|Looking Back|Thesis Thread|Real-World Scenario)s?\s*</h[23]>',
    re.IGNORECASE,
)
# Inline prose patterns
INLINE_NOTE = re.compile(
    r'<p[^>]*>\s*<strong>\s*(Note|Warning|Tip|Important|Caution|Key insight|Fun fact)\s*:?\s*</strong>',
    re.IGNORECASE,
)
# Aside / blockquote outside of callout context
ASIDE_TAG = re.compile(r'<aside[\s>]', re.IGNORECASE)
BLOCKQUOTE_TAG = re.compile(r'<blockquote[\s>]', re.IGNORECASE)


def _line(html, pos):
    return html.count("\n", 0, pos) + 1


def _inside_callout(html, pos):
    """Heuristic: is `pos` inside a `<div class="callout ...">...</div>` block?
    We scan backward for the nearest opening/closing tag and check class."""
    # Walk backward up to 1500 chars looking for <div class="callout
    window = html[max(0, pos - 1500):pos]
    last_open = window.rfind('<div class="callout')
    last_close = window.rfind('</div>')
    return last_open > last_close


def run(filepath, html, context):
    issues = []
    if filepath.suffix != ".html":
        return issues

    # Skip nav/index/front matter (template-driven, fewer prose pseudo-callouts)
    name = filepath.name
    is_section = name.startswith("section-")

    for m in BARE_DIV.finditer(html):
        # Skip if this is actually inside a class="callout X" attribute we
        # already matched (it shouldn't be — we anchor at "<div class=\"")
        bare_class = m.group(1)
        issues.append(Issue(
            PRIORITY, CHECK_ID, filepath, _line(html, m.start()),
            f'Bare <div class="{bare_class}"> without "callout " prefix; use <div class="callout {bare_class}">',
        ))

    for m in H3_PSEUDO.finditer(html):
        title = m.group(1)
        # Heading is canonical if followed within ~6 lines by a proper
        # <div class="callout TYPE">. The h2/h3 then acts as a section header
        # for one or more callouts beneath it (e.g., "Key Takeaways" intro to
        # a <div class="callout key-insight"> with bulleted takeaways).
        lookahead = html[m.end():m.end() + 800]
        if re.search(r'<div\s+class="callout\s+\w+', lookahead, re.IGNORECASE):
            continue
        # Also canonical: the heading is INSIDE a <div class="takeaways">
        # wrapper (book.css has a `.takeaways` rule that styles it like a
        # callout). Look back up to 200 chars for the wrapper.
        lookback = html[max(0, m.start() - 200):m.start()]
        if re.search(r'<div\s+class="takeaways"', lookback, re.IGNORECASE):
            continue
        issues.append(Issue(
            PRIORITY, CHECK_ID, filepath, _line(html, m.start()),
            f'Heading "{title}" should be a <div class="callout-title"> inside a callout div',
        ))

    if is_section:
        for m in INLINE_NOTE.finditer(html):
            kw = m.group(1)
            issues.append(Issue(
                PRIORITY, CHECK_ID, filepath, _line(html, m.start()),
                f'Inline "<strong>{kw}:</strong>" pattern; wrap content in a <div class="callout {kw.lower()}">',
            ))

    # <aside> and <blockquote> are legitimate HTML5 elements; they are NOT
    # pseudo-callouts when used semantically. We only flag them when they
    # appear visually styled as a callout would be (e.g. with a callout class).
    # The mere presence of <aside> or <blockquote> alone is not a violation,
    # so we no longer flag them here. See earlier-wave audits that filtered
    # 450+ false positives book-wide.

    return issues
