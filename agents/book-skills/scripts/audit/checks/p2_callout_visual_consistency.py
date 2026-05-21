"""Verify every canonical callout type has:
  - A `::before` icon rule (background-image or content) in book.css
  - A `::after` tooltip rule with non-trivial content (>20 chars)
  - The callout-title uses canonical typesetting (no inline style overrides)

User feedback (2026-05-18): "make sure all callouts have icons, tooltips
and they are used. Make sure all callout titles use same typesetting,
font size, style, capitalization."

This is a one-shot meta-check that scans book.css once and the HTML pages
once for each canonical callout type.
"""
import re
from collections import namedtuple
from pathlib import Path

PRIORITY = "P2"
CHECK_ID = "CALLOUT_VISUAL_CONSISTENCY"
DESCRIPTION = "Callout type missing canonical icon or tooltip, or title has inline style override"

Issue = namedtuple("Issue", ["priority", "check_id", "filepath", "line", "message"])

# The 20 canonical callout types (after pathway + thesis-thread retirement)
CANONICAL_TYPES = [
    "algorithm", "big-picture", "cross-ref", "exercise", "fun-note",
    "key-insight", "key-takeaway", "lab", "library-shortcut", "looking-back",
    "note", "numeric-example", "postmortem", "practical-example",
    "production-pattern", "research-frontier", "self-check", "tip",
    "warning", "whats-next",
]


def _check_css_rules(css: str) -> dict[str, dict]:
    """For each canonical type, check if it has ::before icon + ::after tooltip rules."""
    status = {}
    for t in CANONICAL_TYPES:
        has_icon = bool(re.search(
            rf'\.callout\.{re.escape(t)}\s+\.callout-title::before\s*\{{[^}}]*(?:background-image|content)',
            css,
        ))
        m = re.search(
            rf'\.callout\.{re.escape(t)}\s+\.callout-title::after\s*\{{[^}}]*content:\s*"([^"]+)"',
            css,
        )
        has_tooltip = bool(m and len(m.group(1)) > 20)
        tooltip_content = m.group(1) if m else None
        status[t] = {
            'icon': has_icon,
            'tooltip': has_tooltip,
            'tooltip_text': tooltip_content,
        }
    return status


_css_status_cache = None


def run(filepath, html, context):
    issues = []
    # Run the css-level meta-check once (cache result) and report against the
    # book.css file path, not every HTML page.
    global _css_status_cache
    book_root = context.get("book_root") if context else None
    if book_root is None:
        return issues
    css_path = Path(book_root) / 'styles' / 'book.css'
    if _css_status_cache is None:
        if not css_path.exists():
            return issues
        css_text = css_path.read_text(encoding='utf-8')
        _css_status_cache = _check_css_rules(css_text)

    # Report css-level issues ONCE (when the audited file is book.css itself,
    # or just emit once per audit run by checking filepath == css_path).
    if filepath == css_path:
        for t, st in _css_status_cache.items():
            if not st['icon']:
                issues.append(Issue(
                    PRIORITY, CHECK_ID, filepath, 1,
                    f'CALLOUT_VISUAL: type "{t}" missing ::before icon rule in book.css',
                ))
            if not st['tooltip']:
                issues.append(Issue(
                    PRIORITY, CHECK_ID, filepath, 1,
                    f'CALLOUT_VISUAL: type "{t}" missing ::after tooltip rule (or content too short)',
                ))
        return issues

    if filepath.suffix != ".html":
        return issues

    # HTML-level: check that each .callout-title in this file has no inline
    # style overriding the canonical typesetting (font-size / font-family /
    # text-transform / letter-spacing).
    TITLE_INLINE_STYLE = re.compile(
        r'<div\s+class="callout-title"[^>]*style="([^"]+)"',
        re.IGNORECASE,
    )
    for m in TITLE_INLINE_STYLE.finditer(html):
        style = m.group(1)
        # Flag if style touches typography props
        if re.search(r'font-(?:size|family|weight)|text-transform|letter-spacing', style, re.IGNORECASE):
            line = html.count('\n', 0, m.start()) + 1
            issues.append(Issue(
                PRIORITY, CHECK_ID, filepath, line,
                f'CALLOUT_VISUAL: callout-title has inline typography override style="{style[:80]}" '
                f'(should inherit from .callout-title canonical rule)',
            ))

    return issues
