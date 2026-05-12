"""v6.38: Comprehensive chapter / section numbering audit.

Detects:
  A. Chapter-number gaps (e.g. 15 -> 17 means Ch 16 missing)
  B. Chapters in the WRONG part (number says X, location says Y)
  C. ToC label vs href mismatch (label says "33.6" but href is section-33.4.html)
  D. Section files whose section-number prefix in <h1> disagrees with filename
  E. Figure labels that don't match the section they're in
"""
from __future__ import annotations
import csv
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
OUT = ROOT / 'KDP' / 'validation' / 'numbering_audit.csv'

PARTS_ORDER = [
    'part-1-foundations', 'part-2-understanding-llms', 'part-3-working-with-llms',
    'part-4-training-adapting', 'part-5-retrieval-conversation', 'part-6-agentic-ai',
    'part-7-multimodal-applications', 'part-8-evaluation-production',
    'part-9-safety-strategy', 'part-10-frontiers', 'part-11-idea-to-product',
]
PART_LABEL = {
    'part-1-foundations':             'Part I',
    'part-2-understanding-llms':      'Part II',
    'part-3-working-with-llms':       'Part III',
    'part-4-training-adapting':       'Part IV',
    'part-5-retrieval-conversation':  'Part V',
    'part-6-agentic-ai':              'Part VI',
    'part-7-multimodal-applications': 'Part VII',
    'part-8-evaluation-production':   'Part VIII',
    'part-9-safety-strategy':         'Part IX',
    'part-10-frontiers':              'Part X',
    'part-11-idea-to-product':        'Part XI',
}


def chapter_num(mod_dir: str) -> int:
    m = re.match(r'module-0*(\d+)-', mod_dir)
    return int(m.group(1)) if m else -1


def main() -> int:
    issues = []

    # === A: chapter-number gaps + B: out-of-place chapters ===
    chs_by_part = defaultdict(list)
    all_chs = []
    for pdir in PARTS_ORDER:
        p = ROOT / pdir
        if not p.exists():
            continue
        for m in sorted(p.glob('module-*'), key=lambda d: chapter_num(d.name)):
            n = chapter_num(m.name)
            if n < 0:
                continue
            chs_by_part[pdir].append(n)
            all_chs.append((pdir, n, m.name))

    # Detect gaps in overall sequence
    overall_nums = sorted(n for _, n, _ in all_chs)
    expected = list(range(overall_nums[0], overall_nums[-1] + 1))
    missing = sorted(set(expected) - set(overall_nums))
    print(f'Overall chapter range: {overall_nums[0]}..{overall_nums[-1]}')
    print(f'Missing chapter numbers: {missing}')

    # Detect chapters appearing OUT OF ORDER inside their part
    for pdir, nums in chs_by_part.items():
        if nums != sorted(nums):
            issues.append({
                'kind': 'B_out_of_order_in_part',
                'detail': f'{pdir} chapters: {nums} (not monotonic)',
                'where': pdir, 'extra': '',
            })

    # Detect chapters whose number disagrees with its sequential position.
    # Build: in reading order, what would the "ideal" sequential chapter
    # number be? If actual differs, flag.
    for i, (pdir, n, mname) in enumerate(all_chs):
        # n_expected = i (since chapters are 0-indexed)
        if n != i:
            issues.append({
                'kind': 'A_chapter_number_gap',
                'detail': f'reading position {i} -> chapter number {n}  (gap of {n - i})',
                'where': f'{pdir}/{mname}', 'extra': '',
            })

    # === C: ToC label vs href mismatch ===
    toc = (ROOT / 'toc.html').read_text(encoding='utf-8')
    for m in re.finditer(
        r'<a href="([^"]+section-(\d+)\.(\d+)(?:\.\d+)?\.html)"[^>]*>(\d+\.\d+(?:\.\d+)?)\s+',
        toc,
    ):
        href, h_chap, h_sec, label = m.group(1), m.group(2), m.group(3), m.group(4)
        l_chap, l_sec = label.split('.')[:2]
        if h_chap != l_chap or h_sec != l_sec:
            issues.append({
                'kind': 'C_toc_label_href_mismatch',
                'detail': f'label "{label}" points to {href.split("/")[-1]}',
                'where': 'toc.html', 'extra': '',
            })

    # === D: section <h1> number vs filename ===
    for sec in sorted(ROOT.glob('part-*/module-*/section-*.html')):
        text = sec.read_text(encoding='utf-8', errors='replace')
        # filename pattern: section-N.M(.K)?.html
        fn_m = re.match(r'section-(\d+)\.(\d+)(?:\.(\d+))?', sec.stem)
        if not fn_m:
            continue
        # h1 typically: "<h1>Title</h1>" without number prefix in this book.
        # But some sections have numbered h2 like "5.4 Diffusion-Based ...";
        # the test is whether the section's first <h2> starts with the right
        # section number prefix.
        h2_m = re.search(r'<h2[^>]*>(\d+)\.(\d+)\s', text)
        if h2_m:
            h2_chap, h2_sec = h2_m.group(1), h2_m.group(2)
            if (h2_chap, h2_sec) != (fn_m.group(1), fn_m.group(2)):
                issues.append({
                    'kind': 'D_h2_number_filename_mismatch',
                    'detail': f'first H2 says {h2_chap}.{h2_sec} but file is section-{fn_m.group(1)}.{fn_m.group(2)}',
                    'where': str(sec.relative_to(ROOT)).replace('\\', '/'),
                    'extra': '',
                })

    # === E: figure label vs containing section ===
    for sec in sorted(ROOT.glob('part-*/module-*/section-*.html')):
        text = sec.read_text(encoding='utf-8', errors='replace')
        fn_m = re.match(r'section-(\d+)\.(\d+)', sec.stem)
        if not fn_m:
            continue
        chap, secn = fn_m.group(1), fn_m.group(2)
        for m in re.finditer(r'<strong>Figure\s+(\d+)\.(\d+)\.\d+</strong>', text):
            f_chap, f_sec = m.group(1), m.group(2)
            if (f_chap, f_sec) != (chap, secn):
                issues.append({
                    'kind': 'E_figure_label_section_mismatch',
                    'detail': f'Figure {f_chap}.{f_sec}.X in section-{chap}.{secn}',
                    'where': str(sec.relative_to(ROOT)).replace('\\', '/'),
                    'extra': '',
                })

    # Summary
    from collections import Counter
    by_kind = Counter(i['kind'] for i in issues)
    print(f'\nIssues found: {len(issues)}')
    for k, v in by_kind.most_common():
        print(f'  {k}: {v}')

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open('w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=['kind', 'where', 'detail', 'extra'])
        w.writeheader()
        w.writerows(issues)
    print(f'\nReport: {OUT}')

    print('\nFirst 15 issues:')
    for issue in issues[:15]:
        print(f'  [{issue["kind"]}] {issue["where"]}')
        print(f'         {issue["detail"]}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
