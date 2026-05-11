"""v6.2: Structural normalization based on the consistency audit.

Five separate normalizations:

A. Bibliography summary text -> "References" (was 27 outliers using "Bibliography")
B. Bibliography inner title  -> "References & Further Reading" (canonical, 107 already)
C. Chapter index h1 -> drop "Chapter NN:" prefix where present (matches the
   convention used in 10 chapters; the chapter-label below carries the number)
D. Section h1 -> drop "X.Y" prefix where present (the chapter-label/breadcrumb
   carries the section number)
E. Figure 28.2.2 -> convert from 3-column SVG (no arrows) into a 3-column
   <table> showing the requirement -> capability -> regulation mapping
   (the original SVG promised mapping but only shows parallel columns)
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SKIP = {'agents', 'KDP', 'node_modules', 'scripts', '.git',
        'chapter_review', 'downloads', '_archive', '_lab_fragments',
        'templates'}


def files() -> list[Path]:
    out = []
    for p in sorted(ROOT.rglob('*.html')):
        rel = p.relative_to(ROOT)
        if rel.parts and rel.parts[0] in SKIP:
            continue
        out.append(p)
    return out


# ----- A. summary -> "References" -----------------------------------

SUMMARY_PAT = re.compile(
    r'(<details[^>]*class="bibliography-collapsible"[^>]*>\s*'
    r'<summary[^>]*>\s*<strong>)(?P<text>[^<]+?)(</strong>\s*</summary>)',
    re.IGNORECASE,
)


def fix_summaries(p: Path) -> int:
    text = p.read_text(encoding='utf-8')
    new, n = SUMMARY_PAT.subn(
        lambda m: m.group(1) + 'References' + m.group(3),
        text,
    )
    if new != text and n:
        p.write_text(new, encoding='utf-8')
    return n


# ----- B. inner title -> "References & Further Reading" -------------

INNER_TITLE_PAT = re.compile(
    r'(<div class="bibliography-title">)([^<]+)(</div>)'
)


def fix_inner_titles(p: Path) -> int:
    text = p.read_text(encoding='utf-8')
    new, n = INNER_TITLE_PAT.subn(
        lambda m: m.group(1) + 'References &amp; Further Reading' + m.group(3),
        text,
    )
    if new != text and n:
        p.write_text(new, encoding='utf-8')
    return n


# ----- C. Chapter index h1 -> drop "Chapter NN:" prefix --------------

CHAPTER_H1_PAT = re.compile(
    r'(<h1[^>]*>)\s*Chapter\s+\d+:?\s*(?P<title>[^<]+?)\s*(</h1>)',
    re.IGNORECASE,
)


def fix_chapter_h1(p: Path) -> int:
    """Only run on chapter index files."""
    if p.name != 'index.html' or 'module-' not in str(p.parent):
        return 0
    text = p.read_text(encoding='utf-8')
    new, n = CHAPTER_H1_PAT.subn(
        lambda m: m.group(1) + m.group('title').strip() + m.group(3),
        text, count=1,
    )
    if new != text and n:
        p.write_text(new, encoding='utf-8')
    return n


# ----- D. Section h1 -> drop "X.Y" or "Letter.N" prefix --------------

SECTION_H1_PAT = re.compile(
    r'(<h1[^>]*>)\s*(?P<num>[A-Z]?\.?\d+(?:\.\d+)*)\s+(?P<title>[^<]+?)\s*(</h1>)'
)


def fix_section_h1(p: Path) -> int:
    """Only run on section files (not index.html)."""
    if not p.name.startswith('section-'):
        return 0
    text = p.read_text(encoding='utf-8')
    new, n = SECTION_H1_PAT.subn(
        lambda m: m.group(1) + m.group('title').strip() + m.group(4),
        text, count=1,
    )
    if new != text and n:
        p.write_text(new, encoding='utf-8')
    return n


# ----- E. Figure 28.2.2 SVG -> table ---------------------------------

FIG_28_2_2_OLD_PATTERN = re.compile(
    r'<div class="diagram-container">\s*<svg[^>]+viewBox="0 0 700 220"[^>]*>'
    r'(?:.|\n)*?</svg>\s*'
    r'<div class="diagram-caption"><strong>Figure 28\.2\.2</strong>:[^<]*</div>\s*'
    r'</div>',
    re.IGNORECASE,
)

NEW_FIG_28_2_2 = '''<div class="figure-container">
<table class="data-table" style="width:100%; max-width:60rem; margin: 1rem auto; border-collapse:collapse;">
<caption style="caption-side: bottom; padding-top: 0.5rem; font-style: italic; color: #555;"><strong>Figure 28.2.2 (Table):</strong> Regulatory landscape for financial LLM applications. Each row maps a regulatory requirement to the LLM capability that addresses it and the governing regulation that mandates it.</caption>
<thead>
<tr style="background: #f5f5f5;">
<th scope="col" style="padding: 0.6rem; text-align: left; border-bottom: 2px solid #c62828; color: #c62828;">Regulatory Requirement</th>
<th scope="col" style="padding: 0.6rem; text-align: left; border-bottom: 2px solid #27ae60; color: #27ae60;">LLM Capability</th>
<th scope="col" style="padding: 0.6rem; text-align: left; border-bottom: 2px solid #e65100; color: #e65100;">Key Regulation</th>
</tr>
</thead>
<tbody>
<tr><td style="padding: 0.5rem; border-bottom: 1px solid #eee;">Explainability</td><td style="padding: 0.5rem; border-bottom: 1px solid #eee;">Reasoning traces / chain-of-thought logging</td><td style="padding: 0.5rem; border-bottom: 1px solid #eee;">EU AI Act (Art. 13), GDPR Art. 22</td></tr>
<tr><td style="padding: 0.5rem; border-bottom: 1px solid #eee;">Auditability</td><td style="padding: 0.5rem; border-bottom: 1px solid #eee;">Structured logging of inputs, outputs, and model versions</td><td style="padding: 0.5rem; border-bottom: 1px solid #eee;">SEC / FINRA, MiFID II</td></tr>
<tr><td style="padding: 0.5rem; border-bottom: 1px solid #eee;">Bias testing</td><td style="padding: 0.5rem; border-bottom: 1px solid #eee;">Fairness evaluation on protected-class subgroups</td><td style="padding: 0.5rem; border-bottom: 1px solid #eee;">EU AI Act (Annex III high-risk), ECOA (US)</td></tr>
<tr><td style="padding: 0.5rem; border-bottom: 1px solid #eee;">Human oversight</td><td style="padding: 0.5rem; border-bottom: 1px solid #eee;">Confidence scores + escalation workflows</td><td style="padding: 0.5rem; border-bottom: 1px solid #eee;">EU AI Act (Art. 14), Basel III/IV (model risk)</td></tr>
<tr><td style="padding: 0.5rem;">Data privacy</td><td style="padding: 0.5rem;">On-premise or VPC deployment; no training-data leakage</td><td style="padding: 0.5rem;">GDPR, CCPA</td></tr>
</tbody>
</table>
</div>'''


def fix_fig_28_2_2() -> int:
    p = ROOT / 'part-7-multimodal-applications/module-28-llm-applications/section-28.2.html'
    if not p.exists():
        return 0
    text = p.read_text(encoding='utf-8')
    new, n = FIG_28_2_2_OLD_PATTERN.subn(NEW_FIG_28_2_2, text, count=1)
    if new != text and n:
        p.write_text(new, encoding='utf-8')
    return n


# ----- Driver -------------------------------------------------------

def main() -> int:
    print('A. Normalize bibliography <summary> to "References"')
    n_a = sum(fix_summaries(p) for p in files())
    print(f'   normalized {n_a} summaries')

    print('\nB. Normalize bibliography inner title to "References & Further Reading"')
    n_b = sum(fix_inner_titles(p) for p in files())
    print(f'   normalized {n_b} inner titles')

    print('\nC. Drop "Chapter NN:" prefix from chapter index <h1>')
    n_c = sum(fix_chapter_h1(p) for p in files())
    print(f'   normalized {n_c} chapter index h1')

    print('\nD. Drop "X.Y" prefix from section <h1>')
    n_d = sum(fix_section_h1(p) for p in files())
    print(f'   normalized {n_d} section h1')

    print('\nE. Convert Figure 28.2.2 SVG -> table')
    n_e = fix_fig_28_2_2()
    print(f'   converted {n_e} figure')

    print(f'\nTOTAL: A={n_a} B={n_b} C={n_c} D={n_d} E={n_e}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
