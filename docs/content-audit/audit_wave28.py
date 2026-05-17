"""Wave 28 content audit. Reads book_content_index.jsonl and reports issues.

READ-ONLY. No HTML mutation.
"""
import json
import sys
import io
import os
import re
import statistics
from collections import defaultdict, Counter
from difflib import SequenceMatcher

# Force UTF-8 stdout for Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

INDEX = r"E:\Projects\BookBlogsHome\LLMBook\book_content_index.jsonl"
OUT = r"E:\Projects\BookBlogsHome\LLMBook\docs\content-audit\wave28_content_issues.md"

# ---------------------------------------------------------------------------
# Load
# ---------------------------------------------------------------------------
records = []
with open(INDEX, encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        records.append(json.loads(line))

print(f"Loaded {len(records)} records")

# Section-like content: real teaching pages
SECTION_TYPES = {'section', 'appendix-section', 'capstone'}
sections = [r for r in records if r['page_type'] in SECTION_TYPES]
print(f"Sections: {len(sections)}")

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
STOP = set("""a an the and or of to in for on with by as at from is are was were be been being this
that these those it its their there here we you i your our which what who whose how when where why
do does did done into about through over under above below also just only can may might should would
will not no nor than then while if so but""".split())


def short_id(rec):
    # Build a compact identifier
    if rec['page_type'] == 'section':
        return f"§{rec['section_num']} {rec['title']}"
    if rec['page_type'] == 'appendix-section':
        # path appendix-A/section-A.1.html etc
        return f"App {rec['section_num']} {rec['title']}"
    if rec['page_type'] == 'capstone':
        return f"Capstone: {rec['title']}"
    return rec.get('title') or rec['path']


def kb(rec):
    return (rec.get('byte_size') or 0) / 1024.0


def section_chapter_key(rec):
    # Used to group sections by chapter for per-chapter health
    if rec['page_type'] == 'section':
        return (rec['part_slug'], rec['chapter_num'])
    if rec['page_type'] == 'appendix-section':
        # path like appendices/appendix-a-...
        m = re.match(r"appendices/(appendix-[a-z0-9]+)-", rec['path'])
        if m:
            return ('appendices', m.group(1))
        return ('appendices', None)
    if rec['page_type'] == 'capstone':
        return ('capstone', rec['title'])
    return ('other', None)


def tokens_from_heading(h):
    """Lowercase substantive tokens from a heading text."""
    t = h.get('text') or ''
    t = re.sub(r"[^a-zA-Z0-9 ]+", ' ', t).lower()
    toks = [w for w in t.split() if w and w not in STOP and len(w) > 2]
    return toks


def heading_signature(rec):
    """Bag of lowercase tokens drawn from sub-headings (level 2/3) only."""
    bag = []
    for h in (rec.get('headings') or []):
        if isinstance(h, dict) and h.get('level', 2) >= 2:
            bag.extend(tokens_from_heading(h))
    return bag


def heading_text_set(rec, levels=(2, 3)):
    out = []
    for h in (rec.get('headings') or []):
        if isinstance(h, dict) and h.get('level', 2) in levels:
            text = h.get('text') or ''
            out.append(text)
    return out


def short_path(rec):
    return rec['path']


# ---------------------------------------------------------------------------
# 1. DUPLICATION DETECTION
# ---------------------------------------------------------------------------
# Strategy: build heading token bags per section. Compute Jaccard similarity on
# substantive tokens between every pair. Also compare big_picture/first_para
# via SequenceMatcher. Flag if heading Jaccard > 0.35 OR (jaccard > 0.20 AND
# big_picture similarity > 0.45).
#
# Tag certain section families as TEMPLATE so we can cluster their pairwise
# duplicates into a single template-row report rather than spamming every
# combination. Template families:
#   - "Tools of the Trade" closing sections (Platforms/Libraries/Datasets/Models/External Reading)
#   - "Vendors and Further Reading" closing section across Part-15 industry chapters
TEMPLATE_TITLE_TOKENS = {
    'platforms', 'libraries', 'frameworks', 'datasets', 'benchmarks',
    'models', 'external reading', 'communities', 'vendors', 'further reading',
    'tools of the trade',
}

TEMPLATE_PATH_PATTERNS = [
    re.compile(r"module-\d+-tools-of-the-trade/"),
    re.compile(r"module-\d+-[a-z]+-llms/section-\d+\.5\.html"),  # industry §N.5 vendor sections
]


LAB_TEMPLATE_HEADINGS = {'prerequisites', 'setup', 'objective', 'expected output', 'exercises'}


def is_template(rec):
    """True if this section appears to be a structural template (tools-of-the-trade,
    vendor-closing, or hands-on lab). Lab-pattern is the most common false-positive
    driver: every hands-on lab carries headings (Prerequisites, Setup, Objective,
    Expected Output, Exercises). When two sections share that scaffolding, the
    duplication is the *template*, not the content.
    """
    title = (rec.get('title') or '').lower()
    path = rec.get('path') or ''
    if any(t in title for t in ('external reading', 'platforms', 'libraries', 'datasets & benchmarks',
                                'vendors and further reading', 'vendors & further reading',
                                'libraries & frameworks')) and 'tools of the trade' not in title:
        if any(p.search(path) for p in TEMPLATE_PATH_PATTERNS):
            return True
    if 'vendors' in title and ('further reading' in title or 'postmortems' in title):
        return True
    # Lab template detection: at least 3 of the 5 canonical lab headings present
    heading_texts = set(
        (h.get('text') or '').lower().strip()
        for h in (rec.get('headings') or [])
        if isinstance(h, dict)
    )
    lab_overlap = len(heading_texts & LAB_TEMPLATE_HEADINGS)
    if lab_overlap >= 3:
        return True
    return False


print("Computing duplication candidates...")

# Pre-compute signatures
sigs = {}
sig_sets = {}
for s in sections:
    bag = heading_signature(s)
    if len(bag) < 4:
        continue  # too few headings to compare meaningfully
    sigs[s['path']] = bag
    sig_sets[s['path']] = set(bag)

# Pair scan
dup_pairs = []
template_pairs = []  # template-vs-template duplicates: grouped, not enumerated
keys = list(sigs.keys())
# Index by lookup
by_path = {r['path']: r for r in sections}
for i, p1 in enumerate(keys):
    s1 = sig_sets[p1]
    for p2 in keys[i+1:]:
        s2 = sig_sets[p2]
        if not s1 or not s2:
            continue
        inter = s1 & s2
        union = s1 | s2
        jac = len(inter) / len(union) if union else 0
        if jac < 0.20:
            continue
        # Compute big_picture / first_para textual similarity (cheap, only top candidates)
        r1 = by_path[p1]; r2 = by_path[p2]
        bp1 = (r1.get('big_picture') or r1.get('first_para') or '')[:600].lower()
        bp2 = (r2.get('big_picture') or r2.get('first_para') or '')[:600].lower()
        bp_sim = SequenceMatcher(None, bp1, bp2).ratio() if bp1 and bp2 else 0
        # Flag conditions
        flag = (jac >= 0.35) or (jac >= 0.20 and bp_sim >= 0.45)
        if not flag:
            continue
        pair = {
            'p1': p1, 'p2': p2,
            'jaccard': jac, 'bp_sim': bp_sim,
            'shared': sorted(inter, key=lambda t: -sum(1 for x in (sigs[p1]+sigs[p2]) if x == t))[:10],
        }
        # Both ends template? Cluster.
        if is_template(r1) and is_template(r2):
            template_pairs.append(pair)
        else:
            dup_pairs.append(pair)

dup_pairs.sort(key=lambda d: -(d['jaccard'] + 0.3 * d['bp_sim']))
print(f"  Found {len(dup_pairs)} non-template duplicate-candidate pairs, "
      f"{len(template_pairs)} template-vs-template duplicates clustered.")

# ---------------------------------------------------------------------------
# 2. LOSS OF FOCUS DETECTION
# ---------------------------------------------------------------------------
# Heuristic: sections whose sub-headings cover many distinct "topic clusters"
# without any cluster dominating. We approximate "topic clusters" by token
# frequency. If the top token within heading text appears in <20% of headings,
# and the section has >= 6 headings, flag it.
print("Computing loss-of-focus sections...")

# Some titles explicitly signal a broad survey - don't flag those as un-focused.
BROAD_SCOPE_PATTERNS = [
    re.compile(r"in \d+\s*minutes", re.I),
    re.compile(r"\b(foundations?|essentials?|primer|overview|landscape|tour|introduction|fundamentals?)\b", re.I),
    re.compile(r"\bwhat every .* needs\b", re.I),
    re.compile(r"\bend[-\s]to[-\s]end\b", re.I),
    re.compile(r"\bblueprint\b", re.I),
    re.compile(r"how a .* (works|computes)", re.I),
    re.compile(r"\bin practice\b", re.I),
]

def title_is_broad(rec):
    t = rec.get('title') or ''
    return any(p.search(t) for p in BROAD_SCOPE_PATTERNS)


focus_issues = []
for s in sections:
    headings = [h for h in (s.get('headings') or []) if isinstance(h, dict) and h.get('level', 2) >= 2]
    if len(headings) < 6:
        continue
    all_tokens = [t for h in headings for t in tokens_from_heading(h)]
    if not all_tokens:
        continue
    counter = Counter(all_tokens)
    top_token, top_count = counter.most_common(1)[0]
    n = len(headings)
    coherence = top_count / n
    distinct_themes = sum(1 for tok, c in counter.most_common(8) if c >= 2)
    # Promise check: keyword from first_para appearing in headings
    fp = (s.get('first_para') or '').lower()
    fp_tokens = set(w for w in re.split(r"[^a-z0-9]+", fp) if w and w not in STOP and len(w) > 4)
    heading_tokens = set(all_tokens)
    fp_match = len(fp_tokens & heading_tokens) / max(1, len(fp_tokens))
    score = 0
    reasons = []
    # Stricter thresholds + require small n to avoid flagging big primers
    if coherence < 0.15 and 7 <= n <= 25:
        score += 2
        reasons.append(f"top heading token '{top_token}' covers only {coherence:.0%} of {n} headings")
    if distinct_themes >= 6 and coherence < 0.20 and n <= 30:
        score += 1
        reasons.append(f"{distinct_themes} distinct recurring themes")
    if fp_match < 0.05 and fp_tokens and 8 <= n <= 30:
        score += 1
        reasons.append(f"first_para keywords overlap with only {fp_match:.0%} of heading tokens")
    # Broad-by-title sections get a -1 penalty (they're licensed to be broad)
    broad = title_is_broad(s)
    if broad:
        score -= 1
        reasons.append("(title signals broad-scope coverage, penalty applied)")
    if score >= 2:
        focus_issues.append({
            'rec': s,
            'score': score,
            'reasons': reasons,
            'n_headings': n,
            'top_themes': counter.most_common(6),
            'heading_samples': [h.get('text') for h in headings[:8]],
            'broad_title': broad,
        })

focus_issues.sort(key=lambda d: (-d['score'], -d['n_headings']))
print(f"  Found {len(focus_issues)} loss-of-focus candidates")

# ---------------------------------------------------------------------------
# 3. LACK OF CONTENT
# ---------------------------------------------------------------------------
print("Computing under-content sections...")
under = []
for s in sections:
    wc = s.get('word_count', 0) or 0
    h2_3 = [h for h in (s.get('headings') or []) if isinstance(h, dict) and h.get('level', 2) >= 2]
    n_head = len(h2_3)
    bp = (s.get('big_picture') or '').strip()
    callouts = s.get('callouts') or []
    n_callouts = len(callouts)
    flags = []
    if wc < 2000: flags.append(f"wc={wc}")
    if n_head < 3: flags.append(f"h2/3={n_head}")
    if not bp: flags.append("no big_picture")
    if n_callouts < 1: flags.append(f"callouts={n_callouts}")
    if flags:
        # Weight by how many criteria triggered
        under.append({'rec': s, 'flags': flags, 'wc': wc, 'n_head': n_head, 'n_callouts': n_callouts})

under.sort(key=lambda d: (-len(d['flags']), d['wc']))
print(f"  Found {len(under)} under-content sections")

# ---------------------------------------------------------------------------
# 4. PER-CHAPTER HEALTH + missing pieces
# ---------------------------------------------------------------------------
print("Computing per-chapter health...")
chapters = defaultdict(list)
for s in sections:
    chapters[section_chapter_key(s)].append(s)

chapter_rows = []
chapter_missing = []
for key, secs in sorted(chapters.items(), key=lambda kv: (str(kv[0][0]), str(kv[0][1]))):
    if not secs:
        continue
    n = len(secs)
    kbs = [kb(s) for s in secs]
    avg_kb = statistics.mean(kbs)
    callout_total = sum(len(s.get('callouts') or []) for s in secs)
    callouts_avg = callout_total / n
    bib_cov = sum(1 for s in secs if s.get('has_bibliography')) / n
    image_cov = sum(1 for s in secs if (s.get('images') or s.get('figures'))) / n
    # Per-chapter missing pieces
    if n >= 4:
        min_kb = min(kbs); max_kb = max(kbs)
        if min_kb * 3 < max_kb and min_kb < 20:
            smallest = min(secs, key=lambda s: kb(s))
            chapter_missing.append({
                'key': key, 'kind': 'small section in big chapter',
                'detail': f"smallest section {short_id(smallest)} = {min_kb:.1f}KB vs max {max_kb:.1f}KB",
            })
    if n >= 3 and bib_cov == 0:
        chapter_missing.append({
            'key': key, 'kind': 'no bibliography anywhere',
            'detail': f"{n} sections, 0 with bibliography",
        })
    if n >= 3 and image_cov < 1.0 and image_cov > 0:
        no_img = [s for s in secs if not (s.get('images') or s.get('figures'))]
        if no_img and len(no_img) <= 2:
            chapter_missing.append({
                'key': key, 'kind': 'section without image while siblings have',
                'detail': f"{', '.join(short_id(s) for s in no_img)} (others all illustrated)",
            })
    chapter_rows.append({
        'key': key, 'n': n, 'avg_kb': avg_kb,
        'callouts_avg': callouts_avg, 'bib_cov': bib_cov,
        'image_cov': image_cov,
        'min_kb': min(kbs), 'max_kb': max(kbs),
    })

# ---------------------------------------------------------------------------
# 5. MISMATCHED SCOPES (size band)
# ---------------------------------------------------------------------------
print("Computing size-band outliers...")
small_size = [s for s in sections if kb(s) < 5]
large_size = [s for s in sections if kb(s) > 150]
print(f"  Small (<5KB): {len(small_size)}; Large (>150KB): {len(large_size)}")

# ---------------------------------------------------------------------------
# Write report
# ---------------------------------------------------------------------------
lines = []
def w(*args):
    lines.append(' '.join(str(a) for a in args))

w("# Wave 28: content-issue audit (duplication, focus, lack)")
w("")
w(f"Index audited: {os.path.basename(INDEX)} ({len(records)} records, {len(sections)} teaching sections).")
w(f"Date: 2026-05-17.")
w("")
w("Heuristics used:")
w("- Duplication: Jaccard on substantive heading-token sets, augmented by")
w("  SequenceMatcher ratio on `big_picture` text. Flag at Jaccard >= 0.35 or")
w("  (Jaccard >= 0.20 and big_picture similarity >= 0.45). Pairs in which BOTH")
w("  ends are recognised structural templates (Tools-of-the-Trade closing,")
w("  Vendors & Further Reading, hands-on lab scaffolding with")
w("  Prerequisites/Setup/Objective/Expected Output/Exercises) are clustered")
w("  separately, since their similarity is by-design and not actionable.")
w("- Loss of focus: sections with 7-25 sub-headings where the top recurring")
w("  heading token covers less than 15% of headings, or >= 6 distinct themes")
w("  appear at frequency >= 2 with low coherence, plus a -1 penalty when the")
w("  section title explicitly signals a broad survey (e.g. 'foundations',")
w("  'in 90 minutes', 'landscape').")
w("- Under-content: word_count < 2000 OR sub-headings < 3 OR no big_picture")
w("  OR callouts < 1; severity = number of flags triggered.")
w("- Over-content: body byte_size > 150 KB.")
w("- Per-chapter health: imbalance when smallest section < one-third of")
w("  largest and < 20 KB; no bibliography on any section; one section without")
w("  images while every sibling has them.")
w("")
w("## Top issues")
w("")

# Compose top issues with a curated mix.
top = []

# T1: biggest over-content section is a systemic problem (single page > 300KB).
if large_size:
    biggest = max(large_size, key=kb)
    top.append((
        'over-content',
        short_id(biggest),
        f"{kb(biggest):.0f} KB body / {biggest.get('word_count')} words on a single page (`{biggest['path']}`). "
        f"Split into multiple sub-sections or move deep-dive material to appendix.",
    ))

# T2: Template-vs-template cluster (industry §N.5 vendors, tools-of-the-trade §M.5)
if template_pairs:
    # Identify the template family with the most pairs
    fam_pages = defaultdict(set)
    for tp in template_pairs:
        fam_pages['template'].add(tp['p1']); fam_pages['template'].add(tp['p2'])
    total_pages = len(fam_pages['template'])
    top.append((
        'duplication (template)',
        f"{len(template_pairs)} template-vs-template pairs across {total_pages} sections",
        f"Closing-section template (Tools of the Trade §N.5 + Part-15 'Vendors and Further Reading'). "
        f"Action: confirm intentional template (preserve), and ensure each instance customises content beyond boilerplate headings.",
    ))

# T3: Best non-template duplicate pair
real_dups = [d for d in dup_pairs if d['jaccard'] >= 0.40]
if real_dups:
    d = real_dups[0]
    r1 = by_path[d['p1']]; r2 = by_path[d['p2']]
    top.append((
        'duplication (substantive)',
        f"{short_id(r1)} ↔ {short_id(r2)}",
        f"Jaccard {d['jaccard']:.2f}, big_picture sim {d['bp_sim']:.2f}. Shared tokens: {', '.join(d['shared'][:6])}. "
        f"Paths: `{r1['path']}` and `{r2['path']}`. Verify cross-reference exists, otherwise consolidate.",
    ))

# T4 + T5: Worst loss-of-focus (after broad-title penalty)
for f in focus_issues[:3]:
    s = f['rec']
    top.append((
        'focus',
        short_id(s),
        f"{f['n_headings']} headings; top theme '{f['top_themes'][0][0]}' covers only "
        f"{f['top_themes'][0][1]}/{f['n_headings']}; themes: {', '.join(t for t,_ in f['top_themes'][:4])}. "
        f"`{s['path']}`",
    ))

# T6: Severe under-content (paths fold by chapter)
severe_under = [u for u in under if len(u['flags']) >= 3]
if severe_under:
    # Group by (part_slug, chapter_num) to show systemic pattern
    chap_cnt = Counter()
    for u in severe_under:
        chap_cnt[section_chapter_key(u['rec'])] += 1
    most_chap, most_n = chap_cnt.most_common(1)[0]
    if most_n >= 2:
        top.append((
            'under-content (systemic)',
            f"{most_n} sections in chapter {most_chap} flagged severe",
            "Multiple stub sections in the same chapter. Either expand each to median size or merge into siblings.",
        ))
    # Otherwise show the worst single one
    u = severe_under[0]
    top.append((
        'under-content',
        short_id(u['rec']),
        f"flags: {', '.join(u['flags'])}; `{u['rec']['path']}`",
    ))

# T7: Chapter with 0% bibliography coverage but >= 3 sections
zero_bib_chapters = [r for r in chapter_rows if r['bib_cov'] == 0 and r['n'] >= 3]
if zero_bib_chapters:
    zero_bib_chapters.sort(key=lambda r: -r['n'])
    keys_str = ', '.join(str(c['key']) for c in zero_bib_chapters[:4])
    top.append((
        'missing-bibliography',
        f"{len(zero_bib_chapters)} chapters with 0% bibliography coverage",
        f"Includes: {keys_str}. Add at least Further Reading callout on chapter-wrap section.",
    ))

# T8: Chapter with extreme imbalance (max KB > 10x min KB)
imbalanced = [r for r in chapter_rows if r['n'] >= 3 and r['min_kb'] > 0 and r['max_kb'] / r['min_kb'] >= 8]
imbalanced.sort(key=lambda r: -(r['max_kb'] / r['min_kb']))
if imbalanced:
    r = imbalanced[0]
    top.append((
        'mismatched-scopes',
        f"Chapter {r['key']} sections range {r['min_kb']:.1f}-{r['max_kb']:.1f} KB",
        f"Largest section is {r['max_kb']/r['min_kb']:.0f}x the smallest in the same chapter. Rebalance or split.",
    ))

# Emit top issues
for i, (cat, sid, detail) in enumerate(top[:10], 1):
    w(f"{i}. **[{cat}]** {sid}")
    w(f"   {detail}")
w("")

w("")
w("## Duplication candidates")
w("")

# First, the template cluster summary (one row, not 25)
if template_pairs:
    w("### Template clusters (deliberate scaffolding, audit but do not blindly merge)")
    w("")
    # Bucket by family
    tot_pages = set()
    for tp in template_pairs:
        tot_pages.add(tp['p1']); tot_pages.add(tp['p2'])
    w(f"- **Total template-vs-template pairs**: {len(template_pairs)} across {len(tot_pages)} sections.")
    # Split into two named clusters for readability
    closing_pairs = []
    lab_pairs = []
    for tp in template_pairs:
        r1 = by_path[tp['p1']]; r2 = by_path[tp['p2']]
        h1 = set((h.get('text') or '').lower().strip() for h in (r1.get('headings') or []) if isinstance(h, dict))
        h2 = set((h.get('text') or '').lower().strip() for h in (r2.get('headings') or []) if isinstance(h, dict))
        lab_overlap = len(h1 & h2 & LAB_TEMPLATE_HEADINGS)
        if lab_overlap >= 3:
            lab_pairs.append(tp)
        else:
            closing_pairs.append(tp)
    if closing_pairs:
        cp_paths = set()
        for tp in closing_pairs:
            cp_paths.add(tp['p1']); cp_paths.add(tp['p2'])
        w("")
        w(f"  - **Closing-section template** (`Tools of the Trade §N.5` + Part-15 `Vendors and Further Reading`):")
        w(f"    - {len(closing_pairs)} pairs across {len(cp_paths)} sections.")
        sample = sorted(cp_paths)[:4]
        w(f"    - Sample paths: " + '; '.join(f"`{p}`" for p in sample))
        w(f"    - Shared scaffolding headings: \"Communities\", \"Foundational Papers\", \"Canonical External References\", \"Cross-References Inside This Book\", \"What Comes Next\".")
        w(f"    - Verdict: by-design template, not uncoordinated duplication. **Do not merge.**")
        w(f"    - Action: audit each instance has 3-5 specific links beyond the boilerplate; decide whether `External Reading & Communities` should remain its own §N.5 or roll into §N.4 as a tail-callout.")
    if lab_pairs:
        lp_paths = set()
        for tp in lab_pairs:
            lp_paths.add(tp['p1']); lp_paths.add(tp['p2'])
        w("")
        w(f"  - **Hands-on lab template** (Prerequisites / Setup / Objective / Expected Output / Exercises):")
        w(f"    - {len(lab_pairs)} pairs across {len(lp_paths)} sections.")
        sample = sorted(lp_paths)[:4]
        w(f"    - Sample paths: " + '; '.join(f"`{p}`" for p in sample))
        w(f"    - Shared scaffolding headings: Prerequisites, Setup, Objective, Expected Output, Exercises.")
        w(f"    - Verdict: standard lab structure - intentional pedagogical pattern. **Do not merge.**")
        w(f"    - Action: confirm each lab actually delivers distinct content under those headings (different setup steps, different exercises, different expected output). Use this list as a checklist for lab quality review.")
    w("")
    w("### Substantive (non-template) duplication candidates")
    w("")

if not dup_pairs:
    w("_None above threshold (after template-cluster removal)._")
else:
    for d in dup_pairs[:25]:
        r1 = by_path[d['p1']]; r2 = by_path[d['p2']]
        # Find shared heading TEXTS (not just tokens) for richer report
        h1 = set(h.lower().strip() for h in heading_text_set(r1))
        h2 = set(h.lower().strip() for h in heading_text_set(r2))
        shared_h = sorted(h1 & h2)[:5]
        same_chapter = (r1.get('part_slug') == r2.get('part_slug') and r1.get('chapter_num') == r2.get('chapter_num'))
        verdict = ("INTRA-CHAPTER (likely deliberate split; check for cross-ref)" if same_chapter
                   else "CROSS-CHAPTER (check for uncoordinated duplication)")
        w(f"- **{short_id(r1)}** ↔ **{short_id(r2)}**")
        w(f"  - heading-Jaccard {d['jaccard']:.2f}; big_picture similarity {d['bp_sim']:.2f}; {verdict}")
        w(f"  - top shared tokens: `{', '.join(d['shared'][:8])}`")
        if shared_h:
            w(f"  - identical heading texts: {'; '.join(shared_h)}")
        w(f"  - paths: `{r1['path']}` , `{r2['path']}`")
        # Recommendation
        if d['jaccard'] >= 0.5:
            rec = "MERGE or pick one as canonical; convert the other to a stub with pointer."
        elif d['jaccard'] >= 0.35:
            rec = "Verify both sections explicitly cross-reference each other; otherwise consolidate."
        else:
            rec = "Light overlap; add explicit cross-references in both directions."
        w(f"  - action: {rec}")
        w("")

w("## Loss-of-focus sections")
w("")
if not focus_issues:
    w("_No sections triggered both focus criteria._")
else:
    for f in focus_issues[:25]:
        s = f['rec']
        w(f"- **{short_id(s)}** (`{s['path']}`)")
        w(f"  - {f['n_headings']} sub-headings; reasons: {'; '.join(f['reasons'])}")
        themes = ', '.join(f"{t} ({c})" for t, c in f['top_themes'][:6])
        w(f"  - top heading themes (token, freq): {themes}")
        sample_h = '; '.join(f['heading_samples'][:6])
        w(f"  - first 6 headings: _{sample_h}_")
        w(f"  - action: split into focused sub-sections, or rescope title + big_picture to honestly cover what is taught.")
        w("")

w("## Under-content sections")
w("")
w("_Pages whose content size is below threshold or missing structural elements._")
w("")
# Group by severity
sev3 = [u for u in under if len(u['flags']) >= 3]
sev2 = [u for u in under if len(u['flags']) == 2]
sev1 = [u for u in under if len(u['flags']) == 1]

def emit(severity_label, items, limit):
    w(f"### {severity_label} ({len(items)})")
    w("")
    if not items:
        w("_none_")
        w("")
        return
    for u in items[:limit]:
        s = u['rec']
        w(f"- **{short_id(s)}** (`{s['path']}`): wc {u['wc']}, h2/3 {u['n_head']}, callouts {u['n_callouts']}; flags: {', '.join(u['flags'])}")
        # Action heuristic
        if u['wc'] < 800:
            a = "EXPAND to ~3500 words or MERGE into a sibling section."
        elif u['wc'] < 1500 and u['n_head'] < 3:
            a = "EXPAND with at least one worked example and 2-3 sub-headings, or fold into adjacent section."
        else:
            a = "ADD missing pieces (big_picture, at least one callout, more headings)."
        w(f"  - action: {a}")
    w("")

emit("Severe (3+ flags)", sev3, 40)
emit("Moderate (2 flags)", sev2, 30)
emit("Mild (1 flag)", sev1, 15)

w("## Over-content sections")
w("")
if not large_size:
    w("_None above 150 KB threshold._")
else:
    for s in sorted(large_size, key=lambda r: -kb(r))[:15]:
        w(f"- **{short_id(s)}** (`{s['path']}`): {kb(s):.0f} KB body, {s.get('word_count')} words, "
          f"{len([h for h in (s.get('headings') or []) if isinstance(h, dict) and h.get('level',2) >= 2])} sub-headings")
        w(f"  - action: consider splitting at major H2 boundaries; or moving deep-dive material into an appendix/sidebar.")
w("")

w("## Per-chapter health")
w("")
w("| Chapter key | sections | avg KB | min KB | max KB | callouts/sec | bib coverage | image coverage |")
w("|-------------|---------:|------:|------:|------:|------------:|------------:|--------------:|")
for r in chapter_rows:
    key = r['key']
    if key[0] == 'appendices':
        keystr = f"App {key[1]}"
    elif key[0] == 'capstone':
        keystr = f"Capstone:{str(key[1])[:30]}"
    else:
        part = (key[0] or 'unknown').replace('part-', 'P').replace('-llm-building-blocks', '')
        part = part.replace('-training-llms', '').replace('-llm-systems-and-deployment', '').replace('-llms-in-the-real-world', '')
        part = part.replace('-modern-frontiers', '').replace('-applied-llm-engineering', '')
        keystr = f"{part} ch{key[1]}"
    w(f"| {keystr} | {r['n']} | {r['avg_kb']:.1f} | {r['min_kb']:.1f} | {r['max_kb']:.1f} | {r['callouts_avg']:.1f} | {r['bib_cov']*100:.0f}% | {r['image_cov']*100:.0f}% |")
w("")

if chapter_missing:
    w("### Per-chapter missing pieces")
    w("")
    for m in chapter_missing[:40]:
        key = m['key']
        if key[0] == 'appendices':
            keystr = f"App {key[1]}"
        elif key[0] == 'capstone':
            keystr = f"Capstone:{str(key[1])[:30]}"
        else:
            keystr = f"{key[0]} ch{key[1]}"
        w(f"- **{keystr}** [{m['kind']}]: {m['detail']}")
    w("")

w("## Suggested follow-ups")
w("")
w("Priority order for cleanup (rough one-PR-per-bullet sizing):")
w("")
w("1. **Split §19.2** (Libraries & Frameworks, 317 KB / 14,098 words). Single")
w("   biggest page in the book. Either split at H2 boundaries into §19.2a/b/c")
w("   or relocate the long appendix-style content into a separate appendix.")
w("2. **Industry chapters (Part 15, chs 72-77 + 79)** are uniformly thin (~10 KB,")
w("   0% images, 20% or less bibliography coverage). Either accept that these")
w("   are intentional 'short industry briefs' and document the design, or")
w("   commission a unified expansion: at minimum a hero image, big_picture")
w("   callout, and Further Reading section per chapter.")
w("3. **Chapter 46 (LLM-as-Judge) needs structural work**: every section under")
w("   the 'severe' threshold (no big_picture, 1 heading, no callouts). Either")
w("   expand each section to median size or consolidate ch46 into 2-3 longer")
w("   sections.")
w("4. **Tools-of-the-Trade modules (§5, §14, §19, §25, §30, §45, §51, §71,")
w("   §79, §83)** share a 5-section template (Platforms/Libraries/Datasets/")
w("   Models/External Reading). Almost all have no big_picture and missing")
w("   callouts. Decide between (a) consolidate into ONE 'Tools of the Trade'")
w("   page per part, or (b) standardize the template with big_picture +")
w("   1 callout per sub-section.")
w("5. **13 chapters with 0% bibliography coverage** (listed in per-chapter")
w("   missing pieces). Add a Further Reading callout to chapter-wrap section.")
w("6. **Loss-of-focus sections §9.3, §9.7, §31.3** have 25 sub-headings each")
w("   with no dominant theme. Consider splitting into 2-3 focused subsections")
w("   or rescoping the title + big_picture to honestly cover the breadth.")
w("7. **Non-template duplicates**: verify §10.8 ↔ §14.4 'Models' cross-ref")
w("   exists; for §25.x intra-chapter overlap, either consolidate or add")
w("   explicit cross-pointers.")
w("8. **Validation loop**: regenerate `book_content_index.jsonl` after fixes,")
w("   re-run `tmp_audit_wave28.py`, diff this report. Targets: substantive")
w("   duplicates -> 0, severe under-content -> < 5, over-content -> 0.")
w("")
w(f"Reference numbers: book median = {statistics.median([s.get('word_count', 0) or 0 for s in sections]):.0f} words / "
  f"{statistics.median([kb(s) for s in sections]):.1f} KB per section.")
w("")
w("---")
w("")
w(f"_Generated by `tmp_audit_wave28.py` from `book_content_index.jsonl` ({len(records)} records, {len(sections)} sections)._")

with open(OUT, 'w', encoding='utf-8') as f:
    f.write("\n".join(lines))

print(f"\nReport written to {OUT}")
print(f"Top issues: {len(top)}; dup_pairs: {len(dup_pairs)}; focus: {len(focus_issues)}; under: {len(under)} ({len(sev3)} severe, {len(sev2)} moderate, {len(sev1)} mild); over: {len(large_size)}")
print(f"Per-chapter rows: {len(chapter_rows)}; chapter missing-pieces flags: {len(chapter_missing)}")
