"""Check that each section file has required structural elements.

Per FM.4 promises, every section should have:
  - Epigraph (blockquote.epigraph) - at section level
  - At least one callout (any type)
  - Takeaways or key-insight (at least one summarizing element)

Per module level (checked on index.html, aggregated across sections):
  - Bibliography / references section
  - What's Next / whats-next div
  - Big Picture callout (at least one)
  - Epigraph (at least one across all sections)

Also detects:
  - Unclosed callout divs (callout containing another callout or structural div)
  - Bibliography title with hardcoded emoji (double icon with CSS ::before)
  - key-takeaway callout (should be key-insight)
"""
import re
from collections import namedtuple
from pathlib import Path

PRIORITY = "P1"
CHECK_ID = "SECTION_STRUCTURE"
DESCRIPTION = "Section missing required structural element or has structural defect"

Issue = namedtuple("Issue", ["priority", "check_id", "filepath", "line", "message"])

# Emoji codepoints that duplicate CSS ::before icons
DOUBLE_ICON_PATTERNS = [
    (re.compile(r'class="bibliography-title"[^>]*>\s*(?:&#128218;|&#x1F4DA;|\U0001F4DA|📚)'),
     "bibliography-title has hardcoded emoji (CSS ::before already adds icon)"),
]

# Structural elements to check at section level
SECTION_CHECKS = {
    "epigraph": re.compile(r'class="epigraph"'),
    "any_callout": re.compile(r'class="callout '),
}

# Module-level checks (aggregated across all sections).
# whats-next has two valid forms: <div class="whats-next"> (legacy block)
# and <div class="callout whats-next"> (callout form). Both render the
# "What's Next" section; the check accepts either.
MODULE_REQUIRED = {
    "bibliography": re.compile(r'class="bibliography|class="references|Annotated Bibliography|Further Reading', re.I),
    "whats_next": re.compile(r'class="(?:callout\s+)?whats-next"'),
    "big_picture": re.compile(r'class="callout big-picture"'),
}


def _check_nesting(html, filepath):
    """Detect truly unclosed callout divs by tracking full div depth."""
    issues = []
    callout_open_re = re.compile(r'<div\s+class="callout\s+[^"]*"')
    structural_re = re.compile(r'<div\s+class="(takeaways|whats-next|prerequisites|objectives)"')
    div_open_re = re.compile(r'<div[\s>]')
    div_close_re = re.compile(r'</div>')

    lines = html.split('\n')
    callout_stack = []  # stack of (start_line, depth_at_open)
    global_depth = 0

    for i, line in enumerate(lines, 1):
        opens = len(div_open_re.findall(line))
        closes = len(div_close_re.findall(line))

        # Check if this line opens a callout
        if callout_open_re.search(line):
            callout_stack.append((i, global_depth))

        # Check if structural div appears while inside a callout
        if callout_stack and structural_re.search(line):
            m = structural_re.search(line)
            start_line, _ = callout_stack[-1]
            issues.append(Issue(
                PRIORITY, CHECK_ID, filepath, i,
                f"Structural div .{m.group(1)} inside callout (opened line {start_line}). Missing </div>."
            ))

        global_depth += opens - closes

        # Pop callouts that have closed
        while callout_stack and global_depth <= callout_stack[-1][1]:
            callout_stack.pop()

    return issues


def run(filepath, html, context):
    issues = []
    book_root = context["book_root"]
    rel = str(filepath.relative_to(book_root))

    # Skip non-section, non-index files
    is_section = "section-" in filepath.name
    is_module_index = filepath.name == "index.html" and "module-" in str(filepath)

    # --- Double-icon check (all files) ---
    for pattern, msg in DOUBLE_ICON_PATTERNS:
        if pattern.search(html):
            line = 0
            for i, l in enumerate(html.split('\n'), 1):
                if 'bibliography-title' in l and ('&#128218;' in l or '&#x1F4DA;' in l or '📚' in l):
                    line = i
                    break
            issues.append(Issue(PRIORITY, CHECK_ID, filepath, line, msg))

    # key-takeaway is a canonical callout type (has its own ::before icon in
    # book.css). It was historically called out as "consolidate to key-insight"
    # but the design later split them: key-insight is for one-sentence
    # observations within a section; key-takeaway is for a bulleted summary
    # box at the end. Both are valid. No issue.

    # --- Nesting check (all files) ---
    issues.extend(_check_nesting(html, filepath))

    # --- Section-level checks ---
    if is_section:
        # Tools-of-the-trade and appendix sections are reference-style: they
        # catalog libraries/tools/math/glossary rather than build a narrative.
        # An epigraph (a literary opening quote) is editorially out-of-place
        # in those, so we skip the epigraph requirement for them.
        rel_lower = rel.lower().replace('\\', '/')
        # Match any "-tools-of-the-trade/" / "-scale-tools/" /
        # "-retrieval-tools/" / "-conv-ai-tools/" / "-responsible-ai-tools/"
        # module dir (number-agnostic, survives book renumbers).
        is_reference_section = (
            bool(re.search(r'/module-\d+[ab]?-tools-of-the-trade/', rel_lower))
            or bool(re.search(r'/module-\d+[ab]?-(?:scale|retrieval|conv-ai|responsible-ai)-tools/', rel_lower))
            or '/appendices/' in rel_lower
            or '/appendix-' in rel_lower
        )
        if not is_reference_section and not SECTION_CHECKS["epigraph"].search(html):
            issues.append(Issue("P2", CHECK_ID, filepath, 0, "Section has no epigraph"))
        # Tools-of-the-trade sections often catalog library tables without
        # any narrative callouts; treat the lack of callouts as canonical.
        if (not is_reference_section
                and not SECTION_CHECKS["any_callout"].search(html)):
            issues.append(Issue(PRIORITY, CHECK_ID, filepath, 0, "Section has no callouts"))
        # Each section should have takeaways or at least one key-insight
        # OR a key-takeaway (the bulleted-summary form). Skip for reference
        # sections that are catalog-style.
        has_takeaways = 'class="takeaways"' in html
        has_key_insight = 'class="callout key-insight"' in html
        has_key_takeaway = 'class="callout key-takeaway"' in html
        if (not is_reference_section
                and not has_takeaways
                and not has_key_insight
                and not has_key_takeaway):
            issues.append(Issue("P2", CHECK_ID, filepath, 0,
                                "Section has no takeaways and no key-insight callout"))

    # --- Module-level checks (only on index.html) ---
    if is_module_index:
        mod_dir = filepath.parent
        section_files = sorted(mod_dir.glob("section-*.html"))
        if not section_files:
            return issues

        all_html = html
        section_htmls = {}
        for sf in sorted(section_files):
            try:
                sf_html = sf.read_text(encoding="utf-8", errors="replace")
                all_html += sf_html
                section_htmls[sf] = sf_html
            except Exception:
                pass

        mod_label = mod_dir.relative_to(book_root)

        # Required at module level
        for key, pattern in MODULE_REQUIRED.items():
            if not pattern.search(all_html):
                label = key.replace("_", " ").replace("whats next", "What's Next section")
                issues.append(Issue(PRIORITY, CHECK_ID, filepath, 0,
                                    f"{mod_label} has no {label}"))

        # At least one key-insight across all sections.
        # Tools-of-the-trade modules are catalog-style; key-insight is
        # editorially out of place there, so the requirement is waived.
        mod_lower = str(mod_label).lower().replace('\\', '/')
        is_reference_module = (
            'tools-of-the-trade' in mod_lower
            or 'module-61-scale-tools' in mod_lower
            or 'module-36-retrieval-tools' in mod_lower
            or 'module-41-conv-ai-tools' in mod_lower
            or 'module-56-responsible-ai-tools' in mod_lower
        )
        if (not is_reference_module
                and 'class="callout key-insight"' not in all_html):
            issues.append(Issue(PRIORITY, CHECK_ID, filepath, 0,
                                f"{mod_label} has no key-insight callout in any section"))

        # Last section should have whats-next (accept either form:
        # legacy <div class="whats-next"> or canonical callout form).
        if section_htmls:
            last_section = max(section_htmls.keys())
            last_html = section_htmls[last_section]
            if ('class="whats-next"' not in last_html
                    and 'class="callout whats-next"' not in last_html):
                last_rel = last_section.relative_to(book_root)
                issues.append(Issue("P2", CHECK_ID, filepath, 0,
                                    f"Last section {last_rel} has no What's Next box"))

    return issues
