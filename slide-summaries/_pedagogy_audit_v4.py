"""Pedagogy audit V4 - tiered canonical-section selector.

Improvement over v3: avoids picking sub-mention h3s (e.g. "rsLoRA: Rank-Stabilized LoRA"
when looking for "LoRA"). Uses a 4-tier selector:

  Tier 1: title EXACTLY equals the technique name OR starts with `<name>:`
  Tier 2: title contains the term as a standalone word (regex \\b{name}\\b),
          rejecting embedded matches like "rsLoRA" for "LoRA". Tie-break by
          longest body.
  Tier 3: in_title (any match, including the embedded sub-mention case).
          Tie-break by (body_hits, body_len).
  Tier 4: body-only match. Tie-break by body_hits.

Outputs the same JSON schema as v3 plus a `tier` field per technique.
"""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path
from collections import defaultdict

# Import the technique list from v2
sys.path.insert(0, str(Path(__file__).parent))
from _pedagogy_audit_v2 import TECHNIQUES, parse_sections, score_html


# Pre-compile patterns (case-insensitive so "KV cache" and "KV Cache" both match
# the same technique regex; the technique strings in TECHNIQUES were authored
# assuming the original case but the book mixes cases).
COMPILED = []
for name, pattern_str, category, weight in TECHNIQUES:
    try:
        COMPILED.append((name, re.compile(pattern_str, re.IGNORECASE), category, weight))
    except re.error as e:
        print(f"Bad regex for {name}: {e}", file=sys.stderr)


# A "standalone word" version of the technique name. We escape the display
# name for regex, then wrap in \b...\b boundaries. This catches "LoRA" but
# not "rsLoRA"; "DPO" but not "GDPO". For multi-token names like "Tree-of-Thoughts"
# we keep the same boundaries.
def standalone_name_re(display_name: str) -> re.Pattern | None:
    # Strip parenthetical disambiguation like "P5 (recsys)" -> "P5"
    clean = re.sub(r'\s*\([^)]*\)\s*$', '', display_name).strip()
    if not clean:
        return None
    try:
        return re.compile(r'\b' + re.escape(clean) + r'\b', re.IGNORECASE)
    except re.error:
        return None


def title_tier(title: str, display_name: str, technique_pat: re.Pattern,
               standalone_pat: re.Pattern | None) -> int:
    """Return 1, 2, 3, or 4 indicating the title-match tier (1 best, 4 = body only).

    Tier 1: title EXACTLY equals the technique name OR starts with `<name>:`
            (the strongest "this section IS about <name>" signal).
    Tier 2: title contains the term as a standalone word (\\b{name}\\b), not
            embedded in a longer identifier like "rsLoRA" or "GDPO".
    Tier 3: title matches the loose technique regex anywhere (catches embedded
            sub-mentions and alternate phrasings).
    Tier 4: no title match; body-only.
    """
    title_strip = title.strip()
    # Tier 1: exact title OR "<name>:" prefix (case-insensitive)
    if title_strip.lower() == display_name.lower():
        return 1
    if title_strip.lower().startswith(display_name.lower() + ":"):
        return 1
    # Tier 2: standalone word in title (not embedded in a larger identifier)
    if standalone_pat and standalone_pat.search(title_strip):
        return 2
    # Tier 3: any title hit via the original (loose) technique regex
    if technique_pat.search(title_strip):
        return 3
    # Tier 4: not in title
    return 4


def main():
    root = Path('.')
    # For each technique, collect all candidates (in any section), tagged with tier.
    candidates_per_tech: dict[str, list[dict]] = {name: [] for name, _, _, _ in COMPILED}

    standalone_pats = {name: standalone_name_re(name) for name, _, _, _ in COMPILED}

    n_files = 0
    for path in root.glob('**/section-*.html'):
        if any(p in path.parts for p in ('_downloads', 'node_modules', '.book-update',
                                           'source_fix_backups', '_archive', 'KDP')):
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
                tier = title_tier(sec['title'], name, pat, standalone_pats[name])
                # If not in_title, tier should be 4 regardless.
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

    # Tier-based selection per technique.
    def tier1_subkey(c, name):
        """Within Tier 1, prefer: (exact-match==1, has-colon-prefix==1, body_len)."""
        t = c['title'].strip().lower()
        n = name.lower()
        exact = 1 if t == n else 0
        colon = 1 if t.startswith(n + ':') else 0
        return (exact, colon, c['body_len'])

    best = {}
    for name, _, _, _ in COMPILED:
        cands = candidates_per_tech[name]
        if not cands:
            best[name] = None
            continue
        best_tier = min(c['tier'] for c in cands)
        tier_cands = [c for c in cands if c['tier'] == best_tier]
        if best_tier == 1:
            chosen = max(tier_cands, key=lambda c: tier1_subkey(c, name))
            # If the chosen Tier 1 body is unusually small (likely a "What Comes Next"
            # mention) and a Tier 2 candidate has a much larger body, prefer the
            # substantive Tier 2 candidate instead.
            if chosen['body_len'] < 600:
                t2_cands = [c for c in cands if c['tier'] == 2]
                if t2_cands:
                    t2_best = max(t2_cands, key=lambda c: c['body_len'])
                    if t2_best['body_len'] > 10 * chosen['body_len']:
                        chosen = t2_best
            # Tier 1 scoring sanity check: if the chosen section's own body has
            # ZERO pedagogy dimensions but a sibling Tier 2 candidate is much
            # larger and likely substantive, prefer the substantive one.
            chosen_score = score_html(chosen['body'])['score']
            if chosen_score == 0:
                t2_cands = [c for c in cands if c['tier'] == 2 and c['body_len'] > 3000]
                if t2_cands:
                    t2_best = max(t2_cands, key=lambda c: c['body_len'])
                    t2_score = score_html(t2_best['body'])['score']
                    if t2_score > 0 and t2_best['body_len'] > 5 * chosen['body_len']:
                        chosen = t2_best
        elif best_tier == 2:
            # Prefer longest body
            chosen = max(tier_cands, key=lambda c: c['body_len'])
        elif best_tier == 3:
            chosen = max(tier_cands, key=lambda c: (c['body_hits'], c['body_len']))
        else:  # 4
            chosen = max(tier_cands, key=lambda c: (c['body_hits'], c['body_len']))
        best[name] = chosen

    # Score / aggregate per technique
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
        parent_h2_score = {'has_figure': False, 'has_math': False, 'has_code': False, 'has_example': False, 'score': 0}
        child_h3_score = {'has_figure': False, 'has_math': False, 'has_code': False, 'has_example': False, 'score': 0}
        # Lazy-load the file's section list once
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
            # Aggregate all direct child h3s for this h2
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
            'name': name, 'category': category, 'weight': weight, 'status': 'FOUND',
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

    out = Path('slide-summaries/_pedagogy_audit_v4.json')
    out.write_text(json.dumps({
        'n_files_scanned': n_files,
        'n_techniques_inventoried': len(COMPILED),
        'techniques': results,
    }, indent=2), encoding='utf-8')

    found = [r for r in results if r['status'] == 'FOUND']
    not_found = [r for r in results if r['status'] == 'NOT_FOUND']
    print(f"Scanned {n_files} HTML files; checked {len(COMPILED)} techniques.")
    print(f"Found: {len(found)}, Not found: {len(not_found)}\n")

    # Tier distribution
    tier_hist = defaultdict(int)
    for r in found:
        tier_hist[r['tier']] += 1
    print("Canonical pick tier distribution:")
    for t in sorted(tier_hist):
        print(f"  Tier {t}: {tier_hist[t]:3d}")
    print()

    print("Aggregated score histogram (h3 OR parent h2 has dimension):")
    hist = defaultdict(int)
    for r in found:
        hist[r['agg_score']] += 1
    for s in sorted(hist):
        bar = '#' * (60 * hist[s] // max(len(found), 1))
        print(f"  {s}/4: {hist[s]:3d}  {bar}")
    print()

    high_pri = sorted(
        [r for r in found if r['weight'] >= 1.0 and r['agg_score'] <= 2],
        key=lambda r: (r['agg_score'], -r['body_len'])
    )
    print(f"=== TOP ENRICHMENT PUNCH LIST: {len(high_pri)} load-bearing techniques scoring <=2 ===\n")
    print(f"{'Technique':25s} {'Score':6s} {'Tier':4s} F M C E  Section title (file)")
    print("-" * 130)
    for r in high_pri:
        a = r['agg']
        m = ('Y' if a['has_figure'] else '.', 'Y' if a['has_math'] else '.',
             'Y' if a['has_code'] else '.', 'Y' if a['has_example'] else '.')
        sec = r['canonical_h3'] or r['canonical_h2']
        sec = (sec[:38] + '...') if len(sec) > 38 else sec
        print(f"  {r['name']:25s} {r['agg_score']}/4    T{r['tier']}   {m[0]} {m[1]} {m[2]} {m[3]}  {sec:41s} {r['canonical_file']}")

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
        print(f"  {r['name']:25s} {r['agg_score']}/4    T{r['tier']}   {m[0]} {m[1]} {m[2]} {m[3]}  {sec:41s} {r['canonical_file']}")

    print(f"\n=== NOT FOUND ({len(not_found)}) ===")
    for r in not_found:
        print(f"  [{r['weight']}] {r['name']} ({r['category']})")

    print(f"\nFull report: {out}")


if __name__ == '__main__':
    main()
