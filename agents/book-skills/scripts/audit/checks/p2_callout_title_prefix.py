"""Enforce that callout titles START with the canonical type word.

User policy: descriptive titles are useful ("Key Insight: The Mental Model"),
but the title MUST start with the canonical type word so readers can scan
for callout-type at a glance.

Mapping (callout class -> required title prefix, case-insensitive):
  big-picture        -> "Big Picture"
  key-insight        -> "Key Insight" (also accept "Key Insights")
  note               -> "Note"
  warning            -> "Warning" or "Caution"
  tip                -> "Tip"
  fun-note           -> "Fun Fact" or "Fun Note"
  exercise           -> "Exercise"
  self-check         -> "Self-Check"
  lab                -> "Lab" or "Hands-On Lab"
  algorithm          -> "Algorithm"
  numeric-example    -> "Numeric Example" or "Worked Example"
  practical-example  -> "Real-World Scenario" or "Practical Example"
  production-pattern -> "Production Pattern"
  research-frontier  -> "Research Frontier" or "Open Questions"
  library-shortcut   -> "Library Shortcut"
  cross-ref          -> "See Also" (canonical, single variant; see p2_see_also_canonical.py)
  looking-back       -> "Looking Back"
  postmortem         -> "Postmortem"
  whats-next         -> "What's Next" or "What Comes Next"
"""
import re
from collections import namedtuple

PRIORITY = "P2"
CHECK_ID = "CALLOUT_TITLE_PREFIX"
DESCRIPTION = "Callout title does not start with the canonical type word"

Issue = namedtuple("Issue", ["priority", "check_id", "filepath", "line", "message"])

# Canonical prefixes per callout type (lowercased, partial-prefix match).
# Multiple alternatives allowed.
CANONICAL_PREFIXES = {
    "big-picture": ["big picture", "the big picture"],
    # key-insight has a generic prefix ("Key Insight:") plus rhetorical sub-types
    # that the audit accepts as canonical variants of an inline insight callout:
    #   "Bridge: ..."         — connects prior material to next (transition insight)
    #   "Open Question: ..."  — frontier-style insight (formerly research-frontier)
    #   "Paper Spotlight: ..." — single-paper aha (formerly research-frontier)
    #   "2026 Snapshot: ..."  — time-stamped state-of-the-art (formerly research-frontier)
    #   "2026 Frontier: ..."  — frontier with timestamp (formerly research-frontier)
    # These prefixes were preserved by the duplicate-singleton reconciliation
    # wave when research-frontier callouts were demoted to key-insight (the
    # callout type was too plural; rhetorical sub-types stayed in the title).
    "key-insight": [
        "key insight", "key insights",
        "bridge", "open question", "paper spotlight",
        "2026 snapshot", "2026 frontier", "frontier",
    ],
    "note": ["note", "note:"],
    "warning": ["warning", "caution"],
    "tip": ["tip", "pro tip", "production tip"],
    "fun-note": ["fun fact", "fun note", "did you know"],
    "exercise": ["exercise", "challenge"],
    "self-check": ["self-check", "self check", "check yourself", "quick check"],
    "lab": ["lab", "hands-on", "hands on"],
    "algorithm": ["algorithm"],
    "numeric-example": ["numeric example", "worked example", "example"],
    "practical-example": ["real-world scenario", "real world scenario", "practical example", "case study"],
    "production-pattern": ["production pattern", "production-pattern"],
    "research-frontier": ["research frontier", "open question", "open questions", "frontier"],
    "library-shortcut": ["library shortcut", "shortcut", "library:"],
    # Cross-ref has a single canonical title enforced by p2_see_also_canonical.py.
    "cross-ref": ["see also"],
    "looking-back": ["looking back", "recap", "review"],
    "postmortem": ["postmortem", "post-mortem", "incident", "lessons learned",
                   # Postmortem callouts often title with the issue, not the word
                   # "postmortem". A title like "Notebooks Are a Leak Vector"
                   # inside a callout.postmortem is acceptable because the visual
                   # callout color and icon already convey the type.
                   ],
    "whats-next": ["what's next", "what comes next", "whats next", "next:"],
}

# Some callout types DON'T require the canonical-prefix start — the callout's
# CSS class + icon + tooltip already convey the type. Postmortem is one such:
# titles like "Notebooks Are a Leak Vector" are clearer than "Postmortem:
# Notebooks Are a Leak Vector". Skip these in the audit.
NO_PREFIX_REQUIRED = {"postmortem"}

CALLOUT_BLOCK = re.compile(
    r'<div\s+class="callout\s+([a-z-]+)"[^>]*>\s*'
    r'<div\s+class="callout-title"[^>]*>(.*?)</div>',
    re.IGNORECASE | re.DOTALL,
)
TAG_RE = re.compile(r'<[^>]+>')


def _line(html, pos):
    return html.count("\n", 0, pos) + 1


def run(filepath, html, context):
    issues = []
    if filepath.suffix != ".html":
        return issues
    for m in CALLOUT_BLOCK.finditer(html):
        ctype = m.group(1).lower()
        title_raw = m.group(2)
        title = TAG_RE.sub('', title_raw).strip().lower()
        if not title:
            continue  # missing-title is a different check
        if ctype in NO_PREFIX_REQUIRED:
            continue
        allowed = CANONICAL_PREFIXES.get(ctype)
        if not allowed:
            continue  # unknown type, handled by CALLOUT_NON_CANONICAL
        if not any(title.startswith(p) for p in allowed):
            issues.append(Issue(PRIORITY, CHECK_ID, filepath, _line(html, m.start()),
                f'Callout ({ctype}) title "{title_raw.strip()[:60]}" should start with one of: {allowed[0]!r}'))
    return issues
