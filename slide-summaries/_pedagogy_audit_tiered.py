"""Cycle 11 Step 3: Tier-appropriate pedagogy audit.

Loads _techniques_500_tiered.json and applies tier-appropriate standards:

  Tier A: requires ALL 4 dimensions (figure + math + code + example). FAIL if missing.
  Tier B: requires >=2 dimensions, AT LEAST ONE of which is figure or code.
  Tier C: requires >=50 words of body text + >=1 reference (bib entry or external link).
          NO requirement for figure/math/code.

Reuses canonical-section selection from v5 audit.
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
INV = ROOT / 'slide-summaries' / '_techniques_500_tiered.json'
OUT = ROOT / 'slide-summaries' / '_tier_audit.json'

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


def count_words(text: str) -> int:
    text = re.sub(r'<[^>]+>', ' ', text)
    return len(re.findall(r'\S+', text))


def tier_c_pass(body_around_mention: str) -> dict:
    """For Tier C, count words and check for >=1 reference near the mention."""
    n_words = count_words(body_around_mention)
    has_link = bool(re.search(r'<a\s[^>]*href="https?://[^"]+"', body_around_mention, re.IGNORECASE))
    has_bib_card = bool(re.search(r'bib-entry-card|bib-card|class="bib', body_around_mention, re.IGNORECASE))
    has_arxiv = bool(re.search(r'arxiv\.org/abs/|arXiv:\d', body_around_mention, re.IGNORECASE))
    has_ref = has_link or has_bib_card or has_arxiv
    return {
        'n_words': n_words,
        'has_link': has_link,
        'has_bib_card': has_bib_card,
        'has_arxiv': has_arxiv,
        'pass': (n_words >= 50 and has_ref),
    }


def tier_a_pass(agg: dict) -> bool:
    return all([agg['has_figure'], agg['has_math'], agg['has_code'], agg['has_example']])


def tier_b_pass(agg: dict) -> bool:
    score = sum([agg['has_figure'], agg['has_math'], agg['has_code'], agg['has_example']])
    has_fig_or_code = agg['has_figure'] or agg['has_code']
    return score >= 2 and has_fig_or_code


def main():
    inv = json.loads(INV.read_text(encoding='utf-8'))
    techniques = inv['techniques']

    compiled = []
    for t in techniques:
        flags = 0 if t['name'] in CASE_SENSITIVE_NAMES else re.IGNORECASE
        try:
            pat = re.compile(t['regex'], flags)
        except re.error as e:
            print(f"Bad regex {t['name']}: {e}", file=sys.stderr)
            continue
        compiled.append((t['name'], pat, t['category'], t['tier'], t.get('source', '')))

    standalone_pats = {name: standalone_name_re(name) for name, _, _, _, _ in compiled}

    candidates_per_tech: dict[str, list[dict]] = {n: [] for n, _, _, _, _ in compiled}
    n_files = 0
    section_files = [p for p in ROOT.rglob('section-*.html')
                     if not (set(p.parts) & EXCLUDE_DIRS)]

    for path in section_files:
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
                    'title_tier': tier,
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
        best_tier = min(c['title_tier'] for c in cands)
        tier_cands = [c for c in cands if c['title_tier'] == best_tier]
        if best_tier == 1:
            chosen = max(tier_cands, key=lambda c: tier1_subkey(c, name))
        elif best_tier == 2:
            chosen = max(tier_cands, key=lambda c: c['body_len'])
        elif best_tier == 3:
            chosen = max(tier_cands, key=lambda c: (c['body_hits'], c['body_len']))
        else:
            chosen = max(tier_cands, key=lambda c: (c['body_hits'], c['body_len']))
        best[name] = chosen

    file_cache = {}
    results = []
    for name, pat, category, tier_letter, source in compiled:
        b = best[name]
        if b is None:
            results.append({
                'name': name, 'category': category, 'tier': tier_letter,
                'source': source, 'status': 'NOT_FOUND',
                'pass': False,
            })
            continue
        h3_score = score_html(b['body'])
        parent_h2_score = {'has_figure': False, 'has_math': False, 'has_code': False, 'has_example': False}
        child_h3_score = {'has_figure': False, 'has_math': False, 'has_code': False, 'has_example': False}
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
        score = sum(agg.values())

        # Tier-specific pass check
        if tier_letter == 'A':
            passes = tier_a_pass(agg)
            tier_c_info = None
        elif tier_letter == 'B':
            passes = tier_b_pass(agg)
            tier_c_info = None
        else:  # Tier C
            # Use a 1000-char window around all mentions
            mentions_window = b['body'][:2000] if b['body_len'] <= 2000 else b['body'][:2000]
            tier_c_info = tier_c_pass(mentions_window)
            passes = tier_c_info['pass']

        loc_parts = b['file'].replace('\\', '/').split('/')
        results.append({
            'name': name, 'category': category, 'tier': tier_letter,
            'source': source, 'status': 'FOUND',
            'canonical_file': '/'.join(loc_parts[-3:]),
            'canonical_file_abs': b['file'].replace('\\', '/'),
            'canonical_h3': b['title'] if b['tag'] == 'h3' else None,
            'canonical_h2': b['parent_h2'] if b['tag'] == 'h3' else b['title'],
            'in_title': b['in_title'],
            'body_hits': b['body_hits'],
            'body_len': b['body_len'],
            'title_tier': b['title_tier'],
            'agg': agg,
            'agg_score': score,
            'tier_c_info': tier_c_info,
            'pass': passes,
        })

    OUT.write_text(json.dumps({
        'n_files_scanned': n_files,
        'n_techniques': len(compiled),
        'tier_counts_pass': {
            'A': sum(1 for r in results if r['tier'] == 'A' and r['pass']),
            'B': sum(1 for r in results if r['tier'] == 'B' and r['pass']),
            'C': sum(1 for r in results if r['tier'] == 'C' and r['pass']),
        },
        'tier_counts_fail': {
            'A': sum(1 for r in results if r['tier'] == 'A' and not r['pass']),
            'B': sum(1 for r in results if r['tier'] == 'B' and not r['pass']),
            'C': sum(1 for r in results if r['tier'] == 'C' and not r['pass']),
        },
        'tier_counts_not_found': {
            'A': sum(1 for r in results if r['tier'] == 'A' and r['status'] == 'NOT_FOUND'),
            'B': sum(1 for r in results if r['tier'] == 'B' and r['status'] == 'NOT_FOUND'),
            'C': sum(1 for r in results if r['tier'] == 'C' and r['status'] == 'NOT_FOUND'),
        },
        'techniques': results,
    }, indent=2), encoding='utf-8')

    print(f'Scanned {n_files} files; audited {len(compiled)} techniques.')
    for tier_letter in 'ABC':
        passes = sum(1 for r in results if r['tier'] == tier_letter and r['pass'])
        fails = sum(1 for r in results if r['tier'] == tier_letter and not r['pass'] and r['status'] == 'FOUND')
        notfound = sum(1 for r in results if r['tier'] == tier_letter and r['status'] == 'NOT_FOUND')
        total = passes + fails + notfound
        print(f'Tier {tier_letter}: {passes}/{total} pass  ({fails} fail, {notfound} not-found)')

    # Print Tier A failures in detail
    print('\n=== TIER A FAILURES (must have figure+math+code+example) ===')
    a_fails = sorted([r for r in results if r['tier'] == 'A' and not r['pass']],
                     key=lambda r: (r['status'] != 'NOT_FOUND', -r.get('agg_score', 0)))
    for r in a_fails:
        if r['status'] == 'NOT_FOUND':
            print(f"  NOT_FOUND  {r['name']:30s}  [{r['category']}]")
        else:
            a = r['agg']
            m = ('F' if a['has_figure'] else '.', 'M' if a['has_math'] else '.',
                 'C' if a['has_code'] else '.', 'E' if a['has_example'] else '.')
            sec = r['canonical_h3'] or r['canonical_h2']
            print(f"  {r['agg_score']}/4 {'-'.join(m):8s}  {r['name']:30s}  {sec[:35]:35s}  {r['canonical_file']}")

    # Tier B failures (top 30)
    print('\n=== TIER B FAILURES (need >=2 dims incl figure or code) [top 30] ===')
    b_fails = sorted([r for r in results if r['tier'] == 'B' and not r['pass']],
                     key=lambda r: (r['status'] != 'NOT_FOUND', -r.get('agg_score', 0)))
    for r in b_fails[:30]:
        if r['status'] == 'NOT_FOUND':
            print(f"  NOT_FOUND  {r['name']:30s}  [{r['category']}]")
        else:
            a = r['agg']
            m = ('F' if a['has_figure'] else '.', 'M' if a['has_math'] else '.',
                 'C' if a['has_code'] else '.', 'E' if a['has_example'] else '.')
            sec = r['canonical_h3'] or r['canonical_h2']
            print(f"  {r['agg_score']}/4 {'-'.join(m):8s}  {r['name']:30s}  {sec[:35]:35s}  {r['canonical_file']}")

    # Tier C orphans (not found at all)
    print('\n=== TIER C ORPHANS (not mentioned anywhere) ===')
    c_orphans = [r for r in results if r['tier'] == 'C' and r['status'] == 'NOT_FOUND']
    for r in c_orphans[:30]:
        print(f"  {r['name']:30s}  [{r['category']}]  [{r['source']}]")
    if len(c_orphans) > 30:
        print(f"  ... and {len(c_orphans) - 30} more.")

    print(f'\nFull report: {OUT}')


if __name__ == '__main__':
    main()
