"""Pedagogy audit V5 - uses the expanded technique inventory.

Loads _expanded_techniques.json (Cycle 10 inventory: 252 techniques) and runs
the same tier-based canonical-section selection + scoring as v4.
"""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path
from collections import defaultdict

sys.path.insert(0, str(Path(__file__).parent))
from _pedagogy_audit_v2 import parse_sections, score_html
from _pedagogy_audit_v4 import standalone_name_re, title_tier

ROOT = Path('E:/Projects/BookBlogsHome/LLMBook')
INVENTORY_PATH = ROOT / 'slide-summaries' / '_expanded_techniques.json'
OUT_PATH = ROOT / 'slide-summaries' / '_pedagogy_audit_v5.json'

# Same case-sensitive set as discover script (some patterns need case to avoid English-word matches).
CASE_SENSITIVE_NAMES = {
    'SuRe', 'Eagle', 'Falcon', 'Idefics', 'Pixtral', 'Molmo', 'Cambrian',
    'Tortoise', 'Voicebox', 'Llasa', 'Aider', 'Devin', 'OpenHands',
    'Marlin', 'Medusa', 'FLARE', 'CRAG', 'NPO', 'IPO', 'ORM', 'PRM',
    'PAL', 'PoT', 'KTO', 'ORPO', 'SimPO', 'BGE', 'GTE', 'E5',
    'MATH', 'GPQA', 'BBH', 'Bark', 'AGIEval', 'RA-DIT',
    'Best-of-N', 'Self-Refine', 'Self-RAG', 'OpenAI Swarm',
}


def main():
    inv = json.loads(INVENTORY_PATH.read_text(encoding='utf-8'))
    techniques = inv['techniques']

    # Compile patterns
    compiled = []
    for t in techniques:
        flags = 0 if t['name'] in CASE_SENSITIVE_NAMES else re.IGNORECASE
        try:
            pat = re.compile(t['regex'], flags)
        except re.error as e:
            print(f"Bad regex for {t['name']}: {e}", file=sys.stderr)
            continue
        compiled.append((t['name'], pat, t['category'], t['weight'], t.get('source', 'unknown')))

    standalone_pats = {name: standalone_name_re(name) for name, _, _, _, _ in compiled}

    EXCLUDE_DIRS = {'_downloads', 'node_modules', '.book-update',
                    'source_fix_backups', '_archive', 'KDP', 'slide-summaries',
                    'agents', '.git', 'kdp'}

    candidates_per_tech: dict[str, list[dict]] = {n: [] for n, _, _, _, _ in compiled}
    n_files = 0
    for path in ROOT.glob('**/section-*.html'):
        if set(path.parts) & EXCLUDE_DIRS:
            continue
        n_files += 1
        try:
            html = path.read_text(encoding='utf-8', errors='ignore')
        except Exception:
            continue
        sections = parse_sections(html)
        for sec in sections:
            for name, pat, _, _, _ in compiled:
                in_title = bool(pat.search(sec['title']))
                body_hits = len(pat.findall(sec['body']))
                if not in_title and body_hits == 0:
                    continue
                tier = title_tier(sec['title'], name, pat, standalone_pats[name])
                if not in_title:
                    tier = 4
                candidates_per_tech[name].append({
                    'file': str(path),
                    'tag': sec['tag'],
                    'title': sec['title'],
                    'parent_h2': sec['parent_h2'],
                    'in_title': in_title,
                    'body_hits': body_hits,
                    'body_len': len(sec['body']),
                    'body': sec['body'],
                    'tier': tier,
                })

    def tier1_subkey(c, name):
        t = c['title'].strip().lower()
        n = name.lower()
        exact = 1 if t == n else 0
        colon = 1 if t.startswith(n + ':') else 0
        return (exact, colon, c['body_len'])

    best = {}
    for name, _, _, _, _ in compiled:
        cands = candidates_per_tech[name]
        if not cands:
            best[name] = None
            continue
        best_tier = min(c['tier'] for c in cands)
        tier_cands = [c for c in cands if c['tier'] == best_tier]
        if best_tier == 1:
            chosen = max(tier_cands, key=lambda c: tier1_subkey(c, name))
            if chosen['body_len'] < 600:
                t2_cands = [c for c in cands if c['tier'] == 2]
                if t2_cands:
                    t2_best = max(t2_cands, key=lambda c: c['body_len'])
                    if t2_best['body_len'] > 10 * chosen['body_len']:
                        chosen = t2_best
            chosen_score = score_html(chosen['body'])['score']
            if chosen_score == 0:
                t2_cands = [c for c in cands if c['tier'] == 2 and c['body_len'] > 3000]
                if t2_cands:
                    t2_best = max(t2_cands, key=lambda c: c['body_len'])
                    t2_score = score_html(t2_best['body'])['score']
                    if t2_score > 0 and t2_best['body_len'] > 5 * chosen['body_len']:
                        chosen = t2_best
        elif best_tier == 2:
            chosen = max(tier_cands, key=lambda c: c['body_len'])
        elif best_tier == 3:
            chosen = max(tier_cands, key=lambda c: (c['body_hits'], c['body_len']))
        else:
            chosen = max(tier_cands, key=lambda c: (c['body_hits'], c['body_len']))
        best[name] = chosen

    file_cache = {}
    results = []
    for name, pat, category, weight, source in compiled:
        b = best[name]
        if b is None:
            results.append({
                'name': name, 'category': category, 'weight': weight,
                'source': source, 'status': 'NOT_FOUND',
            })
            continue
        h3_score = score_html(b['body'])
        parent_h2_score = {'has_figure': False, 'has_math': False, 'has_code': False, 'has_example': False, 'score': 0}
        child_h3_score = {'has_figure': False, 'has_math': False, 'has_code': False, 'has_example': False, 'score': 0}
        if b['file'] not in file_cache:
            try:
                file_html = Path(b['file']).read_text(encoding='utf-8', errors='ignore')
                file_cache[b['file']] = parse_sections(file_html)
            except Exception:
                file_cache[b['file']] = []
        secs = file_cache[b['file']]
        if b['tag'] == 'h3' and b['parent_h2']:
            for s in secs:
                if s['tag'] == 'h2' and s['title'] == b['parent_h2']:
                    parent_h2_score = score_html(s['body'])
                    break
        elif b['tag'] == 'h2':
            for s in secs:
                if s['tag'] == 'h3' and s['parent_h2'] == b['title']:
                    sc = score_html(s['body'])
                    for k in ('has_figure', 'has_math', 'has_code', 'has_example'):
                        if sc[k]:
                            child_h3_score[k] = True
        agg = {
            'has_figure': h3_score['has_figure'] or parent_h2_score['has_figure'] or child_h3_score['has_figure'],
            'has_math': h3_score['has_math'] or parent_h2_score['has_math'] or child_h3_score['has_math'],
            'has_code': h3_score['has_code'] or parent_h2_score['has_code'] or child_h3_score['has_code'],
            'has_example': h3_score['has_example'] or parent_h2_score['has_example'] or child_h3_score['has_example'],
        }
        agg['score'] = sum([agg['has_figure'], agg['has_math'], agg['has_code'], agg['has_example']])
        loc_parts = b['file'].replace('\\', '/').split('/')
        results.append({
            'name': name, 'category': category, 'weight': weight, 'source': source,
            'status': 'FOUND',
            'canonical_file': '/'.join(loc_parts[-3:]),
            'canonical_file_abs': b['file'].replace('\\', '/'),
            'canonical_h3': b['title'] if b['tag'] == 'h3' else None,
            'canonical_h2': b['parent_h2'] if b['tag'] == 'h3' else b['title'],
            'in_title': b['in_title'],
            'body_hits': b['body_hits'],
            'body_len': b['body_len'],
            'tier': b['tier'],
            'h3_score_only': h3_score['score'],
            'agg_score': agg['score'],
            'agg': {k: v for k, v in agg.items() if k != 'score'},
        })

    OUT_PATH.write_text(json.dumps({
        'n_files_scanned': n_files,
        'n_techniques_inventoried': len(compiled),
        'techniques': results,
    }, indent=2), encoding='utf-8')

    found = [r for r in results if r['status'] == 'FOUND']
    not_found = [r for r in results if r['status'] == 'NOT_FOUND']
    print(f'Scanned {n_files} HTML files; checked {len(compiled)} techniques.')
    print(f'Found: {len(found)}, Not found: {len(not_found)}\n')

    print('Aggregated score histogram (h3 OR parent h2 has dimension):')
    hist = defaultdict(int)
    for r in found:
        hist[r['agg_score']] += 1
    for s in sorted(hist):
        bar = '#' * (60 * hist[s] // max(len(found), 1))
        print(f'  {s}/4: {hist[s]:3d}  {bar}')
    print()

    # NEW techniques (not in original 153) at score <=2
    new_at_low = [r for r in found
                  if r['source'] != 'curated-original' and r['agg_score'] <= 2]
    print(f'NEW techniques (not in original 153) at score <=2: {len(new_at_low)}\n')

    # By source
    src_hist = defaultdict(int)
    for r in found:
        src_hist[r['source']] += 1
    print('By source:')
    for s, n in src_hist.items():
        print(f'  {s}: {n}')
    print()

    print(f'=== NEW techniques scoring <=2 (top 40 by weight desc) ===\n')
    new_low_sorted = sorted(new_at_low, key=lambda r: (-r['weight'], r['agg_score'], -r['body_len']))
    for r in new_low_sorted[:40]:
        a = r['agg']
        m = ('Y' if a['has_figure'] else '.', 'Y' if a['has_math'] else '.',
             'Y' if a['has_code'] else '.', 'Y' if a['has_example'] else '.')
        sec = r['canonical_h3'] or r['canonical_h2']
        sec = (sec[:34] + '...') if len(sec) > 34 else sec
        print(f"  [w={r['weight']}] {r['name']:25s} {r['agg_score']}/4 T{r['tier']} {m[0]} {m[1]} {m[2]} {m[3]}  {sec:37s} {r['canonical_file']}")

    print(f'\n=== NOT FOUND ({len(not_found)}) ===')
    for r in not_found:
        print(f"  [{r['weight']}] {r['name']} ({r['category']}) [{r['source']}]")

    print(f'\nFull report: {OUT_PATH}')


if __name__ == '__main__':
    main()
