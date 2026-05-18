"""Check that each module has at least one hands-on lab.

FM.4 promises every chapter includes at least one lab exercise with
runnable code, realistic data, and clear success criteria (30-90 min).

Labs are identified by:
  - <div class="lab"> or <section class="lab"> blocks
  - class="callout exercise" with "Lab" in the title (substantial labs)

This check flags modules (via index.html) that lack any lab content.
"""
import re
from collections import namedtuple
from pathlib import Path

PRIORITY = "P2"
CHECK_ID = "LAB_COVERAGE"
DESCRIPTION = "Module has no hands-on lab (FM.4 promises at least one per chapter)"

Issue = namedtuple("Issue", ["priority", "check_id", "filepath", "line", "message"])

# Match canonical <div class="callout lab"> as well as legacy <div class="lab">,
# <section class="lab">, and <div class="callout exercise"> titled "Lab".
LAB_PATTERN = re.compile(
    r'class="(?:callout\s+lab|lab)[\s"]|class="callout\s+exercise"[^>]*>\s*<div\s+class="callout-title"[^>]*>\s*Lab\b',
    re.IGNORECASE,
)


def run(filepath, html, context):
    issues = []
    book_root = context["book_root"]

    # Only check module index files
    if filepath.name != "index.html":
        return []
    if "module-" not in str(filepath):
        return []

    # Reference-style modules (tools-of-the-trade, appendix) don't require
    # a hands-on lab; they're catalogs of libraries/tools.
    rel_lower = str(filepath).lower().replace("\\", "/")
    is_reference_module = (
        '/tools-of-the-trade/' in rel_lower
        or 'module-05-tools-of-the-trade' in rel_lower
        or 'module-19-tools-of-the-trade' in rel_lower
        or 'module-30-tools-of-the-trade' in rel_lower
        or 'module-45-tools-of-the-trade' in rel_lower
        or 'module-51-tools-of-the-trade' in rel_lower
        or 'module-61-scale-tools' in rel_lower
        or 'module-71-tools-of-the-trade' in rel_lower
        or 'module-79-tools-of-the-trade' in rel_lower
        or '/appendices/' in rel_lower
        or '/appendix-' in rel_lower
    )
    if is_reference_module:
        return []

    mod_dir = filepath.parent
    section_files = sorted(mod_dir.glob("section-*.html"))
    if not section_files:
        return []

    # Search all sections for lab content
    has_lab = False
    for sf in section_files:
        try:
            sf_html = sf.read_text(encoding="utf-8", errors="replace")
            if LAB_PATTERN.search(sf_html):
                has_lab = True
                break
        except Exception:
            pass

    if not has_lab:
        mod_label = mod_dir.relative_to(book_root)
        issues.append(Issue(
            PRIORITY, CHECK_ID, filepath, 0,
            f"{mod_label} has no hands-on lab (FM.4 promises >= 1 per chapter)"
        ))

    return issues
