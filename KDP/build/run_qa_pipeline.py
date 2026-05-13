"""Canonical QA pipeline runner for the LLMBook.

Runs every active read-only detector in sequence. Each detector exits 0
on "clean" and prints any defects it finds. The pipeline is the single
source of truth for "is the book ready to ship?" — `python
run_qa_pipeline.py` returns 0 when every check passes.

This file is the runner; the detectors live next to it (`_v6xx_*.py`,
`_v7xx_*.py`). New detectors must be registered here to be part of CI.

USAGE
    python run_qa_pipeline.py            # run all, report summary
    python run_qa_pipeline.py --verbose  # also stream each detector's output
    python run_qa_pipeline.py --fast     # skip slow detectors (currently none)

CONVENTIONS
    * A detector must NOT modify any file when run without --fix.
    * A detector with auto-fix must accept --fix and be idempotent.
    * The runner does NOT pass --fix; it audits only.
"""
from __future__ import annotations
import argparse
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
BUILD = Path(__file__).resolve().parent

# (script_filename, friendly_name, severity) — run in this order.
# severity: 'fatal' (block ship), 'warn' (informational only).
DETECTORS: list[tuple[str, str, str]] = [
    ('_v651_audit_broken_img_refs.py',      'broken <img> references',                       'fatal'),
    ('_v653_check_broken_math.py',          'KaTeX heuristic math validation',               'fatal'),
    ('_v655_find_adjacent_figures.py',      'adjacent figure stacking (editorial)',          'warn'),
    ('_v660_audit_chapter_metadata.py',     'chapter metadata integrity',                    'fatal'),
    ('_v661_validate_python_blocks.py',     'Python AST validation',                         'fatal'),
    ('_v680_strip_keyops_metadata.py',      'auto-gen Key-operations metadata leak',         'fatal'),
    ('_v681_renumber_duplicate_figures.py', 'duplicate Figure labels',                       'fatal'),
    ('_v682_tag_wide_tables.py',            'wide-table tagging',                            'fatal'),
    ('_v692_audit_premature_main_close.py', 'premature </main> before bibliography',         'fatal'),
    ('_v693_audit_pygments_css_link.py',    'pygments.css stylesheet linkage',               'fatal'),
    ('_v696_verify_cross_refs.py',          'internal cross-reference resolution',           'fatal'),
    ('_v697_numbering_audit.py',            'section/figure/code-fragment numbering',        'fatal'),
    ('_v698_renumber_code_fragments.py',    'Code Fragment label sequencing',                'fatal'),
    ('_v699_renumber_figures.py',           'Figure label sequencing',                       'fatal'),
    ('_v700_revert_unparseable_lang_python.py', 'unparseable lang-python blocks',            'fatal'),
    ('_v701_audit_broken_navs.py',          'chapter-nav junk text (orphan anchors)',        'fatal'),
    ('_v702_bump_footer_edition.py',        'stale footer edition strings',                  'fatal'),
    ('_v703_audit_main_close_placement.py', '</main> placement (page-stretch bug)',          'fatal'),
    ('_v715_audit_unclosed_lab.py',         'unclosed <div class="lab"> containers',         'fatal'),
    ('_v716_audit_chapter_opener_in_header.py', 'chapter-opener <figure> inside <header>',   'fatal'),
    ('_v717_audit_page_layout.py',          'page layout (nav/footer placement, etc.)',      'fatal'),
    ('_v718_audit_prereqs.py',              'prerequisite boxes (P1/P2/P3/P4)',              'warn'),
    ('_v728_audit_self_referencing_navs.py', 'self-referencing chapter-nav links',           'fatal'),
    ('run_epubcheck.py',                    'EPUBCheck 5.2.1 (EPUB 3.3 conformance)',        'fatal'),
]


_DEFECT_NUMBER_RE = re.compile(
    r'(?:Errors?|Broken(?:\s+links?)?|Issues?|Defects?|Found|'
    r'Renumbered|Stripped|Tagged|Files\s+(?:touched|affected|changed|needing\s+change|'
    r'reverted(?:\s+lang-python.*?)?|with\s+(?:section-number\s+mismatch|'
    r'figure-label\s+issues|code-fragment-label\s+issues|junk\s+text\s+in\s+chapter-nav|'
    r'</main>-placement\s+issues))|Distinct\s+figure\s+relabels|'
    r'MISSING\s+pygments\.css)\s*[:\-]?\s*(\d+)',
    re.IGNORECASE)


def is_clean(stdout: str) -> bool:
    """A detector is 'clean' when every numeric-defect-count line in its
    final output reports 0."""
    tail = '\n'.join([ln for ln in stdout.splitlines() if ln.strip()][-15:])
    # Special-case the EPUBCheck wrapper which reports
    # "Fatals: N / Errors: N / Warnings: N / Infos: N".
    if 'Fatals:' in tail and 'Errors:' in tail:
        m1 = re.search(r'Fatals:\s*(\d+)', tail)
        m2 = re.search(r'Errors:\s*(\d+)', tail)
        if m1 and m2:
            return int(m1.group(1)) == 0 and int(m2.group(1)) == 0
    counts = _DEFECT_NUMBER_RE.findall(tail)
    if not counts:
        # No numeric report -> trust exit code (handled by caller).
        return True
    return all(int(n) == 0 for n in counts)


def run_detector(name: str, friendly: str, verbose: bool) -> tuple[bool, str, float]:
    script = BUILD / name
    if not script.exists():
        return False, f'SCRIPT MISSING: {script.relative_to(ROOT)}', 0.0
    t0 = time.monotonic()
    try:
        proc = subprocess.run(
            [sys.executable, str(script)],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            timeout=300,
        )
    except subprocess.TimeoutExpired:
        return False, 'TIMEOUT after 300s', time.monotonic() - t0
    dt = time.monotonic() - t0
    tail_lines = [ln for ln in proc.stdout.splitlines() if ln.strip()][-12:]
    clean = proc.returncode == 0 and is_clean(proc.stdout)
    if verbose:
        print(proc.stdout)
        if proc.stderr.strip():
            print('STDERR:', proc.stderr, file=sys.stderr)
    summary = tail_lines[-1] if tail_lines else '(no output)'
    if not clean:
        summary = ' / '.join(tail_lines[-3:])
    return clean, summary, dt


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--verbose', action='store_true',
                    help='stream each detector output')
    args = ap.parse_args()

    print(f'LLMBook QA pipeline -- {len(DETECTORS)} detectors')
    print('=' * 72)
    n_pass = 0
    n_warn = 0
    n_fatal = 0
    failures: list[tuple[str, str, str]] = []
    warns: list[tuple[str, str, str]] = []
    t_pipeline = time.monotonic()
    for script, friendly, severity in DETECTORS:
        ok, summary, dt = run_detector(script, friendly, args.verbose)
        if ok:
            print(f'  [PASS] [{dt:5.1f}s]  {friendly}')
            n_pass += 1
        elif severity == 'warn':
            print(f'  [WARN] [{dt:5.1f}s]  {friendly}')
            print(f'           -> {summary}')
            warns.append((script, friendly, summary))
            n_warn += 1
        else:
            print(f'  [FAIL] [{dt:5.1f}s]  {friendly}')
            print(f'           -> {summary}')
            failures.append((script, friendly, summary))
            n_fatal += 1
    dt_total = time.monotonic() - t_pipeline
    print('=' * 72)
    print(f'  {n_pass} passed, {n_warn} warned, {n_fatal} failed, '
          f'{dt_total:.1f}s total')
    if failures:
        print('\nFAILURES (block ship):')
        for script, friendly, summary in failures:
            print(f'  - {script}: {summary}')
        return 1
    if warns:
        print('\nWarnings (informational; editorial review):')
        for script, friendly, summary in warns:
            print(f'  - {script}: {summary}')
    print('\nAll fatal checks clean. Book is ready to ship.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
