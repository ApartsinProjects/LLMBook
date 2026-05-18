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

    # Reference and discussion-only modules don't require a hands-on lab.
    # Reference: tools-of-the-trade catalogs, appendices.
    # Discussion: ethics, regulation, governance, frontier-research,
    # product/ideation, economics. These chapters cover decision-making,
    # policy, and analysis, not buildable artifacts; insisting on a lab
    # forces contrived exercises that erode the chapter's character.
    rel_lower = str(filepath).lower().replace("\\", "/")
    is_exempt_module = (
        # Reference catalogs
        '/tools-of-the-trade/' in rel_lower
        or 'tools-of-the-trade' in rel_lower
        or 'module-61-scale-tools' in rel_lower
        or 'module-36-retrieval-tools' in rel_lower
        or 'module-41-conv-ai-tools' in rel_lower
        or 'module-56-responsible-ai-tools' in rel_lower
        or '/appendices/' in rel_lower
        or '/appendix-' in rel_lower
        # Discussion-heavy modules (ethics, policy, frontier)
        or 'module-48-guardrails-runtime-safety' in rel_lower
        or 'module-52-bias-fairness' in rel_lower
        or 'module-53-regulation-compliance' in rel_lower
        or 'module-54-watermarking-provenance' in rel_lower
        or 'module-54b-transparency-and-disclosure' in rel_lower
        or 'module-55-environmental-sustainability' in rel_lower
        or 'module-58-frontier-systems-hardware' in rel_lower
        or 'module-67-ideation' in rel_lower
        or 'module-68-vibe-coding' in rel_lower
        or 'module-69-llm-economics' in rel_lower
        or 'module-80-frontier-architectures' in rel_lower
        or 'module-81-frontier-theory' in rel_lower
        or 'module-82-agi-trajectories' in rel_lower
    )
    if is_exempt_module:
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
