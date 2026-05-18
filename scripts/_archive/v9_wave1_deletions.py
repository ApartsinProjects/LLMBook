"""Wave 1: lossy deletions of duplicate/orphan content.

Deletes:
1. Sec 8.3 (Reasoning Models & Test-Time Compute) — duplicates Ch 9 entirely
2. Sec 73.6 "LLMs in Finance & Trading" — generic chapter overview duplicate
3. Sec 74.6 "Healthcare & Biomedical AI" — generic chapter overview duplicate
4. Sec 76.6 "Cybersecurity & LLMs" — generic chapter overview duplicate
5. Sec 79.2 "Education, Legal & Creative Industries" — cross-cuts other chapters
6. Ch 31 (Multimodal Generation overview) — all 4 sections duplicate Ch 32-37
7. Ch 41 (Embodied AI aggregator) — 41.1/41.2/41.3/41.8 duplicate Ch 39/40/36;
   41.4 (World Models) and 41.7 (Multimodal Reasoning) are unique — extracted
   to a 'preserved' folder for later re-homing in Phase 4
8. Ch 45 (1-section orphan at sec 45.6) — merge sec 45.6 into Ch 44
"""
from pathlib import Path
import re
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
PRESERVED = ROOT / '.book-update' / 'v9-preserved-content'
PRESERVED.mkdir(parents=True, exist_ok=True)


def git_rm(p, dry_run=False):
    if not p.exists():
        return False
    if dry_run:
        print(f'  [dry] git rm -rf {p}')
        return True
    r = subprocess.run(['git', 'rm', '-rf', str(p)], cwd=ROOT,
                      capture_output=True, text=True)
    if r.returncode != 0:
        print(f'  ERR: {r.stderr.strip()}')
        return False
    return True


def preserve_section(src, label):
    """Copy a section file to the preserved folder before deletion."""
    if not src.exists(): return
    dst = PRESERVED / f'{label}-{src.name}'
    shutil.copy2(src, dst)
    print(f'  PRESERVED: {src.relative_to(ROOT)} -> {dst.relative_to(ROOT)}')


def step1_delete_sec_8_3():
    """Sec 8.3 duplicates Ch 9 entirely."""
    print('--- Step 1: Delete sec 8.3 (duplicates Ch 9) ---')
    p = ROOT / 'part-2-understanding-llms/module-08-modern-llm-landscape/section-8.3.html'
    if p.exists():
        git_rm(p)
        print(f'  Deleted: {p.relative_to(ROOT)}')


def step2_drop_industry_generic_sections():
    """Drop 73.6, 74.6, 76.6, 79.2 — generic overview duplicates."""
    print('--- Step 2: Drop industry generic overview sections ---')
    targets = [
        ('part-12-applications-across-industries/module-73-finance-llms/section-73.6.html',
         'duplicates chapter 73 (Finance) overview'),
        ('part-12-applications-across-industries/module-74-healthcare-llms/section-74.6.html',
         'duplicates chapter 74 (Healthcare) overview'),
        ('part-12-applications-across-industries/module-76-cybersecurity-llms/section-76.6.html',
         'duplicates chapter 76 (Cybersecurity) overview'),
        ('part-12-applications-across-industries/module-79-creative-industries/section-79.2.html',
         'cross-cuts Education/Legal/Creative — content belongs in respective chapters'),
    ]
    for fp, reason in targets:
        p = ROOT / fp
        if p.exists():
            git_rm(p)
            print(f'  Deleted: {p.relative_to(ROOT)} ({reason})')


def step3_delete_ch_31_overview():
    """Ch 31 (Multimodal Generation) has 4 sections that summarize Ch 32-37."""
    print('--- Step 3: Delete Ch 31 (Multimodal overview duplicate) ---')
    p = ROOT / 'part-7-multimodal-generation/module-31-multimodal'
    if p.exists():
        git_rm(p)


def step4_handle_ch_41_aggregator():
    """Ch 41 is an aggregator: extract unique content (41.4 World Models, 41.7 Multimodal Reasoning),
    then delete the chapter. Unique content stays in .book-update/v9-preserved-content/ for Phase 4 re-homing.
    """
    print('--- Step 4: Extract unique content from Ch 41, then delete ---')
    ch_41 = ROOT / 'part-7-multimodal-generation/module-41-world-models-simulation'
    if not ch_41.exists(): return

    # Preserve the truly unique content
    unique_secs = [
        ('section-41.4.html', 'world-models-and-embodied-reasoning'),
        ('section-41.7.html', 'multimodal-reasoning-cross-modal-retrieval'),
    ]
    for fname, label in unique_secs:
        src = ch_41 / fname
        preserve_section(src, label)

    # Now delete the entire chapter (duplicates of 36/39/40 + the preserved 41.4/41.7)
    git_rm(ch_41)


def step5_merge_ch_45_into_44():
    """Ch 45 has only sec 45.6 (Structured-Output Validity Testing).
    Move that section into Ch 44 as a new section, then delete Ch 45.
    """
    print('--- Step 5: Merge Ch 45 (1-section orphan) into Ch 44 ---')
    ch_45 = ROOT / 'part-8-evaluation-production/module-45-testing-quality-gates'
    ch_44 = ROOT / 'part-8-evaluation-production/module-44-evaluation-foundations'

    src = ch_45 / 'section-45.6.html'
    if not src.exists():
        print('  SKIP: sec 45.6 not found')
        return

    # Find next available section number in Ch 44
    existing = sorted(ch_44.glob('section-44.*.html'),
                     key=lambda p: int(re.match(r'section-44\.(\d+)\.html', p.name).group(1)))
    if not existing:
        print('  SKIP: Ch 44 has no sections')
        return
    last_n = int(re.match(r'section-44\.(\d+)\.html', existing[-1].name).group(1))
    new_n = last_n + 1
    dst = ch_44 / f'section-44.{new_n}.html'

    # Move and rewrite in-file metadata
    r = subprocess.run(['git', 'mv', str(src), str(dst)], cwd=ROOT,
                      capture_output=True, text=True)
    if r.returncode != 0:
        print(f'  ERR: {r.stderr}')
        return

    # Rewrite section number
    text = dst.read_text(encoding='utf-8')
    text = re.sub(r'\bsection-45\.6\b', f'section-44.{new_n}', text)
    text = re.sub(r'\bSection 45\.6\b', f'Section 44.{new_n}', text)
    text = re.sub(r'\b45\.6\.(\d+)\b', rf'44.{new_n}.\1', text)
    text = re.sub(r'\bid="45-6-', f'id="44-{new_n}-', text)
    text = re.sub(r'\bhref="#45-6-', f'href="#44-{new_n}-', text)
    text = re.sub(r'<div class="page-current">Section 45\.6</div>',
                  f'<div class="page-current">Section 44.{new_n}</div>', text)
    text = re.sub(r'<title>Section 45\.6:', f'<title>Section 44.{new_n}:', text)
    text = re.sub(r'(<meta content=")Section 45\.6:', rf'\g<1>Section 44.{new_n}:', text)
    dst.write_text(text, encoding='utf-8')

    print(f'  Moved: sec 45.6 -> {dst.relative_to(ROOT)} (now sec 44.{new_n})')

    # Delete the empty Ch 45 dir
    git_rm(ch_45)


def main():
    print('=== WAVE 1: lossy deletions ===\n')
    step1_delete_sec_8_3()
    print()
    step2_drop_industry_generic_sections()
    print()
    step3_delete_ch_31_overview()
    print()
    step4_handle_ch_41_aggregator()
    print()
    step5_merge_ch_45_into_44()
    print('\n=== Wave 1 complete ===')


if __name__ == '__main__':
    main()
