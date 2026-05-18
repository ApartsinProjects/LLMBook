"""Flag h2-bounded subsections with excessive bold density in prose.

User feedback (2026-05-18): "lot of bold text in 41.3.3, find root cause and
fix everywhere, need validation plugin".

Root cause: bullet lists that bold the LEADING LABEL of every <li>:
    <li><strong>Library/Benchmark name</strong> additional prose...</li>
    <li><strong>Another library</strong> ...</li>

When 6+ such bullets stack, the section reads as "wall of bold". This
plugin computes the bold-word-fraction per h2-bounded subsection (skipping
content inside callouts, since callout titles legitimately bold) and flags
when bold >25% of total words AND the section has 100+ words.
"""
import re
from collections import namedtuple
from pathlib import Path

PRIORITY = "P2"
CHECK_ID = "BOLD_DENSITY"
DESCRIPTION = "Subsection has excessive <strong> density (likely a bullet list with bolded labels)"

Issue = namedtuple("Issue", ["priority", "check_id", "filepath", "line", "message"])


def _strip_callouts(html: str) -> str:
    """Remove all <div class="callout ..."> ... </div> blocks (recursive nesting
    not handled; we use a naive depth tracker)."""
    out = []
    pos = 0
    while pos < len(html):
        m = re.search(r'<div\s+class="callout\s+[^"]+"', html[pos:])
        if not m:
            out.append(html[pos:])
            break
        # Append content up to callout
        out.append(html[pos:pos + m.start()])
        # Skip the callout via balanced div tracking
        scan = pos + m.end()
        depth = 1
        while scan < len(html) and depth > 0:
            o = html.find('<div', scan)
            c = html.find('</div>', scan)
            if c == -1:
                break
            if o != -1 and o < c:
                depth += 1
                scan = o + 4
            else:
                depth -= 1
                scan = c + 6
                if depth == 0:
                    break
        pos = scan
    return ''.join(out)


def run(filepath, html, context):
    issues = []
    if not filepath.name.startswith("section-"):
        return issues

    # Get content of <main>
    main_m = re.search(r'<main\b[^>]*>([\s\S]*?)</main>', html, re.IGNORECASE)
    if not main_m:
        return issues
    main = main_m.group(1)

    # Drop callouts from the bold-density measurement
    stripped = _strip_callouts(main)

    # Walk h2 subsections
    h2_matches = list(re.finditer(r'<h2[^>]*>([^<]+)</h2>', stripped))
    for i, m in enumerate(h2_matches):
        sec_start = m.start()
        sec_end = h2_matches[i + 1].start() if i + 1 < len(h2_matches) else len(stripped)
        section = stripped[sec_start:sec_end]

        # Compute words
        text_only = re.sub(r'<[^>]+>', ' ', section)
        total_words = len(text_only.split())
        if total_words < 100:
            continue

        bold_words = sum(
            len(b.group(1).split())
            for b in re.finditer(r'<strong>([^<]+)</strong>', section)
        )
        if total_words == 0:
            continue
        pct = bold_words / total_words * 100
        if pct > 25:
            title = m.group(1).strip()[:60]
            # Find original line number in full html
            offset_in_main = sec_start
            # Map offset_in_main back to original html: since we stripped
            # callouts, the offsets differ. Use the H2 text to locate.
            orig_m = re.search(re.escape(title), html)
            line = html.count('\n', 0, orig_m.start()) + 1 if orig_m else 1
            issues.append(Issue(
                PRIORITY, CHECK_ID, filepath, line,
                f'BOLD_DENSITY: subsection "{title}" is {pct:.0f}% bold ({bold_words}/{total_words} words); '
                f'consider de-bolding bullet-list labels',
            ))
    return issues
