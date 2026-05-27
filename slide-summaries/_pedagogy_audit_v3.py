"""Pedagogy audit V3 - efficient single-pass version."""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path
from collections import defaultdict

# Import the technique list from v2
sys.path.insert(0, str(Path(__file__).parent))
from _pedagogy_audit_v2 import TECHNIQUES, parse_sections, score_html

# Pre-compile all patterns once
COMPILED = []
for name, pattern_str, category, weight in TECHNIQUES:
    try:
        COMPILED.append((name, re.compile(pattern_str), category, weight))
    except re.error as e:
        print(f"Bad regex for {name}: {e}", file=sys.stderr)


def main():
    root = Path('.')
    # Per-technique best canonical candidate
    best = {name: None for name, _, _, _ in COMPILED}
    n_files = 0
    for path in root.glob('**/section-*.html'):
        if any(p in path.parts for p in ('_downloads', 'node_modules', '.book-update')):
            continue
        n_files += 1
        try:
            html = path.read_text(encoding='utf-8', errors='ignore')
        except Exception:
            continue
        sections = parse_sections(html)
        for sec in sections:
            for name, pat, category, weight in COMPILED:
                in_title = bool(pat.search(sec['title']))
                body_hits = len(pat.findall(sec['body']))
                if not in_title and body_hits == 0:
                    continue
                rank = (1 if in_title else 0, body_hits, len(sec['body']))
                cur = best[name]
                cur_rank = (
                    (1 if cur['in_title'] else 0, cur['body_hits'], cur['body_len'])
                    if cur else (0, 0, 0)
                )
                if rank > cur_rank:
                    best[name] = {
                        'file': str(path),
                        'tag': sec['tag'],
                        'title': sec['title'],
                        'parent_h2': sec['parent_h2'],
                        'in_title': in_title,
                        'body_hits': body_hits,
                        'body_len': len(sec['body']),
                        'body': sec['body'],
                    }

    # Now aggregate scoring per technique (h3 + parent h2 if applicable)
    file_cache = {}
    results = []
    for name, pat, category, weight in COMPILED:
        b = best[name]
        if b is None:
            results.append({
                'name': name, 'category': category, 'weight': weight,
                'status': 'NOT_FOUND'
            })
            continue
        h3_score = score_html(b['body'])
        # Get parent h2 body if relevant
        parent_h2_score = {'has_figure': False, 'has_math': False, 'has_code': False, 'has_example': False, 'score': 0}
        if b['tag'] == 'h3' and b['parent_h2']:
            if b['file'] not in file_cache:
                try:
                    file_html = Path(b['file']).read_text(encoding='utf-8', errors='ignore')
                    file_cache[b['file']] = parse_sections(file_html)
                except Exception:
                    file_cache[b['file']] = []
            for s in file_cache[b['file']]:
                if s['tag'] == 'h2' and s['title'] == b['parent_h2']:
                    parent_h2_score = score_html(s['body'])
                    break
        agg = {
            'has_figure': h3_score['has_figure'] or parent_h2_score['has_figure'],
            'has_math': h3_score['has_math'] or parent_h2_score['has_math'],
            'has_code': h3_score['has_code'] or parent_h2_score['has_code'],
            'has_example': h3_score['has_example'] or parent_h2_score['has_example'],
        }
        agg['score'] = sum([agg['has_figure'], agg['has_math'], agg['has_code'], agg['has_example']])
        loc_parts = b['file'].replace('\\', '/').split('/')
        results.append({
            'name': name, 'category': category, 'weight': weight, 'status': 'FOUND',
            'canonical_file': '/'.join(loc_parts[-3:]),
            'canonical_h3': b['title'] if b['tag'] == 'h3' else None,
            'canonical_h2': b['parent_h2'] if b['tag'] == 'h3' else b['title'],
            'in_title': b['in_title'],
            'body_hits': b['body_hits'],
            'body_len': b['body_len'],
            'h3_score_only': h3_score['score'],
            'agg_score': agg['score'],
            'agg': {k: v for k, v in agg.items() if k != 'score'},
        })

    # Save
    out = Path('slide-summaries/_pedagogy_audit_v3.json')
    out.write_text(json.dumps({
        'n_files_scanned': n_files,
        'n_techniques_inventoried': len(COMPILED),
        'techniques': results,
    }, indent=2), encoding='utf-8')

    # Print summary
    found = [r for r in results if r['status'] == 'FOUND']
    not_found = [r for r in results if r['status'] == 'NOT_FOUND']
    print(f"Scanned {n_files} HTML files; checked {len(COMPILED)} techniques.")
    print(f"Found: {len(found)}, Not found: {len(not_found)}\n")

    print("Aggregated score histogram (h3 OR parent h2 has dimension):")
    hist = defaultdict(int)
    for r in found:
        hist[r['agg_score']] += 1
    for s in sorted(hist):
        bar = '#' * (60 * hist[s] // max(len(found), 1))
        print(f"  {s}/4: {hist[s]:3d}  {bar}")
    print()

    # Punch list: load-bearing (weight>=1) and score <= 2
    high_pri = sorted(
        [r for r in found if r['weight'] >= 1.0 and r['agg_score'] <= 2],
        key=lambda r: (r['agg_score'], -r['body_len'])
    )
    print(f"=== TOP ENRICHMENT PUNCH LIST: {len(high_pri)} load-bearing techniques scoring <=2 ===\n")
    print(f"{'Technique':25s} {'Score':6s} F M C E  Section title (file)")
    print("-" * 120)
    for r in high_pri:
        a = r['agg']
        m = ('Y' if a['has_figure'] else '.', 'Y' if a['has_math'] else '.',
             'Y' if a['has_code'] else '.', 'Y' if a['has_example'] else '.')
        sec = r['canonical_h3'] or r['canonical_h2']
        sec = (sec[:38] + '...') if len(sec) > 38 else sec
        print(f"  {r['name']:25s} {r['agg_score']}/4    {m[0]} {m[1]} {m[2]} {m[3]}  {sec:41s} {r['canonical_file']}")

    # Medium priority too
    med_pri = sorted(
        [r for r in found if 0.5 <= r['weight'] < 1.0 and r['agg_score'] <= 1],
        key=lambda r: (r['agg_score'], -r['body_len'])
    )
    print(f"\n=== MEDIUM PRIORITY (weight 0.6, score <=1): {len(med_pri)} techniques ===")
    for r in med_pri[:25]:
        a = r['agg']
        m = ('Y' if a['has_figure'] else '.', 'Y' if a['has_math'] else '.',
             'Y' if a['has_code'] else '.', 'Y' if a['has_example'] else '.')
        sec = (r['canonical_h3'] or r['canonical_h2'])[:38]
        print(f"  {r['name']:25s} {r['agg_score']}/4    {m[0]} {m[1]} {m[2]} {m[3]}  {sec:41s} {r['canonical_file']}")

    print(f"\n=== NOT FOUND in any h2/h3 across the book ({len(not_found)}) ===")
    for r in not_found:
        print(f"  [{r['weight']}] {r['name']} ({r['category']})")

    print(f"\nFull report: {out}")


if __name__ == '__main__':
    main()
