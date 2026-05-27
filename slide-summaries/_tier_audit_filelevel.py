"""Cycle 11 refinement: file-level aggregation.

For Tier A 'failures' under section-level audit, also check whether ALL 4
dimensions appear ANYWHERE in the same chapter (file) — because a graduate
textbook reader will navigate the chapter, not just the h3 subsection.

A Tier A technique passes the file-level test if its CANONICAL chapter file
(or any file where the technique appears as h2/h3 title) has all 4 dimensions.

This re-classifies true file-level fails for surgical enrichment.
"""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _pedagogy_audit_v2 import parse_sections, score_html

ROOT = Path('E:/Projects/BookBlogsHome/LLMBook')
IN = ROOT / 'slide-summaries' / '_tier_audit.json'
OUT = ROOT / 'slide-summaries' / '_tier_audit_filelevel.json'

CASE_SENSITIVE_NAMES = {
    'SuRe', 'Eagle', 'Falcon', 'Idefics', 'Pixtral', 'Molmo', 'Cambrian',
    'Tortoise', 'Voicebox', 'Llasa', 'Aider', 'Devin', 'OpenHands',
    'Marlin', 'Medusa', 'FLARE', 'CRAG', 'NPO', 'IPO', 'ORM', 'PRM',
    'PAL', 'PoT', 'KTO', 'ORPO', 'SimPO', 'BGE', 'GTE', 'E5',
    'MATH', 'GPQA', 'BBH', 'Bark', 'AGIEval', 'RA-DIT',
    'Best-of-N', 'Self-Refine', 'Self-RAG', 'OpenAI Swarm',
}
EXCLUDE_DIRS = {'_downloads', 'node_modules', '.book-update',
                'source_fix_backups', '_archive', 'KDP', 'slide-summaries',
                'agents', '.git', 'kdp', 'temp_epub', 'vendor', 'templates',
                'pagefind', '_concept-figs', 'capstone',
                'generated-images', 'images', '__pycache__'}


def file_level_dims(file_path: Path, pattern: re.Pattern) -> dict:
    """For a file mentioning the technique, scan the whole file for the
    4 dimensions; only count a dim if it's in a section whose title or
    body matches the technique pattern."""
    try:
        html = file_path.read_text(encoding='utf-8', errors='ignore')
    except Exception:
        return {'has_figure': False, 'has_math': False, 'has_code': False, 'has_example': False}
    sections = parse_sections(html)
    relevant_sections = [s for s in sections
                         if pattern.search(s['title']) or pattern.search(s['body'])]
    agg = {'has_figure': False, 'has_math': False, 'has_code': False, 'has_example': False}
    for s in relevant_sections:
        sc = score_html(s['body'])
        for k in agg:
            if sc[k]:
                agg[k] = True
    return agg


def main():
    audit = json.loads(IN.read_text(encoding='utf-8'))
    techniques = audit['techniques']

    # Re-eval Tier A failures using file-level aggregation
    promoted = []
    real_a_fails = []
    for r in techniques:
        if r['tier'] != 'A' or r['pass']:
            continue
        if r['status'] == 'NOT_FOUND':
            real_a_fails.append(r)
            continue
        # Use the canonical file
        fp = Path(r['canonical_file_abs'])
        try:
            pat = re.compile(r['name'].replace('+', r'\+').replace('-', r'[- ]?'),
                             0 if r['name'] in CASE_SENSITIVE_NAMES else re.IGNORECASE)
        except re.error:
            pat = re.compile(re.escape(r['name']),
                             0 if r['name'] in CASE_SENSITIVE_NAMES else re.IGNORECASE)
        agg = file_level_dims(fp, pat)
        score = sum(agg.values())
        r_new = {**r,
                 'file_level_agg': agg,
                 'file_level_score': score,
                 'file_level_pass': all(agg.values())}
        if r_new['file_level_pass']:
            promoted.append(r_new)
        else:
            real_a_fails.append(r_new)

    print(f'Tier A initial failures: {len(promoted) + len(real_a_fails)}')
    print(f'  Promoted at file-level (file has all 4 dims for the technique): {len(promoted)}')
    print(f'  TRUE Tier A failures (file lacks at least one dim): {len(real_a_fails)}')

    print('\n=== TRUE TIER A FAILURES (file-level, sorted by score desc) ===')
    real_a_fails.sort(key=lambda r: (r['status'] != 'NOT_FOUND',
                                      -(r.get('file_level_score', r.get('agg_score', 0)))))
    for r in real_a_fails:
        if r['status'] == 'NOT_FOUND':
            print(f"  NOT_FOUND  {r['name']:30s}  [{r['category']}]")
            continue
        a = r.get('file_level_agg', r['agg'])
        miss = [k.replace('has_', '') for k in ['has_figure','has_math','has_code','has_example'] if not a[k]]
        score = r.get('file_level_score', r['agg_score'])
        sec = r['canonical_h3'] or r['canonical_h2']
        print(f"  {score}/4 miss={','.join(miss):20s}  {r['name']:30s}  {sec[:35]:35s}  {r['canonical_file']}")

    OUT.write_text(json.dumps({
        'tier_a_promoted': [r['name'] for r in promoted],
        'tier_a_true_failures': [r['name'] for r in real_a_fails],
        'details_promoted': promoted,
        'details_true_failures': real_a_fails,
    }, indent=2), encoding='utf-8')
    print(f'\nSaved {OUT}')


if __name__ == '__main__':
    main()
