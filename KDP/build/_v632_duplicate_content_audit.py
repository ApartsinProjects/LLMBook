"""v6.32: Detect duplicate / near-duplicate content across chapters.

Strategy:
  1. For each section page, extract paragraph blocks (<p>...</p> in <main>).
  2. Compute a normalized fingerprint for each paragraph (lowercased, stripped
     of punctuation, collapsed whitespace).
  3. Compute MinHash signatures for paragraphs > 200 chars.
  4. Find paragraph pairs with Jaccard similarity >= 0.7 across DIFFERENT files.
  5. Also detect "topic clusters" — h2/h3 headings that appear in multiple
     sections, signaling re-explanation of the same concept.

Output: KDP/validation/duplicate_content.csv with columns:
  fileA, fileB, similarity, paragraphA_first_80, paragraphB_first_80
"""
from __future__ import annotations
import csv
import hashlib
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
OUT_CSV = ROOT / 'KDP' / 'validation' / 'duplicate_content.csv'
HEADINGS_OUT = ROOT / 'KDP' / 'validation' / 'duplicate_headings.csv'

MIN_PARA_LEN = 220
SHINGLE_K = 5         # 5-word shingles
NUM_HASHES = 64       # MinHash signature size (small for speed)
SIM_THRESHOLD = 0.55


def normalize(text: str) -> str:
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'&[a-z]+;', ' ', text)
    text = re.sub(r'[^a-zA-Z0-9 ]', ' ', text.lower())
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def shingles(text: str, k: int = SHINGLE_K):
    words = text.split()
    if len(words) < k:
        return set()
    return {' '.join(words[i:i + k]) for i in range(len(words) - k + 1)}


def minhash(shingles_set: set[str], num_hashes: int = NUM_HASHES) -> list[int]:
    """Tiny pure-Python MinHash."""
    if not shingles_set:
        return [0] * num_hashes
    sig = [10**12] * num_hashes
    for s in shingles_set:
        h0 = int(hashlib.md5(s.encode('utf-8')).hexdigest(), 16)
        for i in range(num_hashes):
            # Different hash per slot via XOR with i
            h = (h0 ^ (i * 0x9e3779b97f4a7c15)) & 0xFFFFFFFFFFFFFFFF
            if h < sig[i]:
                sig[i] = h
    return sig


def jaccard_estimate(a: list[int], b: list[int]) -> float:
    if not a:
        return 0.0
    return sum(1 for x, y in zip(a, b) if x == y) / len(a)


def collect_paragraphs():
    """Yield (file_rel, para_idx, para_text) for sections + chapter index."""
    for p in sorted(list(ROOT.glob('part-*/module-*/section-*.html')) +
                    list(ROOT.glob('appendices/appendix-*/section-*.html'))):
        text = p.read_text(encoding='utf-8', errors='replace')
        # Limit to <main>
        main_m = re.search(r'<main[^>]*>(.*?)</main>', text, re.DOTALL)
        if not main_m:
            continue
        body = main_m.group(1)
        # Strip code blocks
        body = re.sub(r'<pre>.*?</pre>', ' ', body, flags=re.DOTALL)
        body = re.sub(r'<section class="bibliography">.*?</section>', ' ', body, flags=re.DOTALL)
        for i, m in enumerate(re.finditer(r'<p[^>]*>(.*?)</p>', body, re.DOTALL)):
            raw = m.group(1)
            norm = normalize(raw)
            if len(norm) < MIN_PARA_LEN:
                continue
            yield (str(p.relative_to(ROOT)).replace('\\', '/'), i, norm)


def collect_headings():
    """Yield (file_rel, heading_text)."""
    for p in sorted(list(ROOT.glob('part-*/module-*/section-*.html'))):
        text = p.read_text(encoding='utf-8', errors='replace')
        for m in re.finditer(r'<h[23][^>]*>(.+?)</h[23]>', text, re.DOTALL):
            raw = re.sub(r'<[^>]+>', '', m.group(1)).strip()
            # Drop section numbering prefix
            raw = re.sub(r'^\d+\.\d+(?:\.\d+)?\s+', '', raw)
            if len(raw) < 6 or len(raw) > 80:
                continue
            yield (str(p.relative_to(ROOT)).replace('\\', '/'), raw)


def main() -> int:
    print('Phase 1: collecting paragraphs...')
    paras = list(collect_paragraphs())
    print(f'  {len(paras)} paragraphs > {MIN_PARA_LEN} chars')

    print('Phase 2: computing MinHash signatures...')
    sigs = []
    for file_rel, i, norm in paras:
        sh = shingles(norm)
        sig = minhash(sh)
        sigs.append((file_rel, i, norm, sig))
    print(f'  signatures done')

    print('Phase 3: exact-prefix dedup (paragraphs sharing first 60 normalized chars)...')
    # Group paragraphs by their first 60 normalized chars. Two paragraphs in
    # the same bucket are CANDIDATES; we then compare them with the cheap
    # set-shingle Jaccard (exact, not MinHash, since each bucket is small).
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    PREFIX_LEN = 60
    by_prefix = defaultdict(list)
    for idx, (file_rel, i, norm, _sig) in enumerate(sigs):
        if len(norm) >= PREFIX_LEN:
            by_prefix[norm[:PREFIX_LEN]].append(idx)

    pairs = 0
    with OUT_CSV.open('w', encoding='utf-8', newline='') as f:
        w = csv.writer(f)
        w.writerow(['fileA', 'fileB', 'jaccard', 'paraA_idx', 'paraB_idx',
                    'paraA_preview', 'paraB_preview'])
        for prefix, members in by_prefix.items():
            if len(members) < 2:
                continue
            # Build shingle sets ONCE per member
            sh = {m: shingles(sigs[m][2], k=3) for m in members}
            for i in range(len(members)):
                for j in range(i + 1, len(members)):
                    a, b = members[i], members[j]
                    if sigs[a][0] == sigs[b][0]:
                        continue
                    sa, sb = sh[a], sh[b]
                    if not sa or not sb:
                        continue
                    inter = len(sa & sb)
                    union = len(sa | sb)
                    sim = inter / union if union else 0
                    if sim >= 0.6:
                        w.writerow([sigs[a][0], sigs[b][0], f'{sim:.2f}',
                                    sigs[a][1], sigs[b][1],
                                    sigs[a][2][:80], sigs[b][2][:80]])
                        pairs += 1
    print(f'  {pairs} duplicate-paragraph pairs (jaccard >= 0.60, sharing 60-char prefix)')

    print('Phase 4: detecting repeated headings across sections...')
    heading_files = defaultdict(set)
    for file_rel, h in collect_headings():
        norm_h = re.sub(r'\s+', ' ', h.lower()).strip()
        heading_files[norm_h].add(file_rel)
    repeated = [(h, files) for h, files in heading_files.items() if len(files) >= 2]
    repeated.sort(key=lambda x: -len(x[1]))
    with HEADINGS_OUT.open('w', encoding='utf-8', newline='') as f:
        w = csv.writer(f)
        w.writerow(['heading', 'num_files', 'files'])
        for h, files in repeated:
            w.writerow([h, len(files), '; '.join(sorted(files))])
    print(f'  {len(repeated)} headings appear in 2+ files')
    print(f'\nReports:\n  {OUT_CSV}\n  {HEADINGS_OUT}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
