"""Audit for near-duplicate callouts (fun-fact, key-insight, warning, etc.)
within the same section file or within the same chapter.

Symptom: section 10.1 has three Fun Fact callouts, all saying "OpenAI's
chat format became the de facto standard / every serving framework
adopts it." A second wave of fun-fact insertion did not check for prior
coverage on the same page.

Root cause: callout insertion scripts ran multiple times across editions
without de-duplication.

Detection: for each callout type, extract the inner <p> text, normalize
(lowercase + remove punctuation + stopwords), compare pairs within the
same file. Two callouts are 'near duplicates' if their normalized token
sets have Jaccard similarity >= 0.45 AND share a substantive keyword
(>=8 chars, not a stopword).

Read-only audit; reports per-file findings.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parent.parent.parent
SKIP = ('node_modules', '.git/', 'pagefind/', 'KDP/build/', 'KDP/output/',
        'templates/', '_archive/', 'temp_epub/', 'vendor/', '/agents/')

# Locate every `<div class="callout TYPE">` opening; we extract the
# next 1200 chars and pull <p> bodies from that window.
CALLOUT_OPEN = re.compile(
    r'<div\s+class="callout\s+([a-zA-Z\-]+)"[^>]*>',
    re.IGNORECASE)
INNER_P = re.compile(r'<p[^>]*>([\s\S]*?)</p>', re.IGNORECASE)
HTML_TAG = re.compile(r'<[^>]+>')

STOPWORDS = set('''
the a an and or but of to in is are was were be been being have has had
do does did this that these those it its on for with at by from as if then
than not no so we you they i he she them their our your his her you'll
this that these those when how why what who which where can could should
would will may might must any all some each every other another like also
just only even though although because while if since
'''.split())


def normalize_tokens(text: str) -> tuple[set, list, set]:
    text = HTML_TAG.sub(' ', text)
    text = re.sub(r"&[a-zA-Z#0-9]+;", ' ', text)
    text = text.lower()
    tokens = re.findall(r"[a-z][a-z\-]{2,}", text)
    content = [t for t in tokens if t not in STOPWORDS]
    # Bigrams over content tokens
    bigrams = {f'{content[i]}_{content[i+1]}' for i in range(len(content)-1)}
    return set(content), content, bigrams


def jaccard(a: set, b: set) -> float:
    if not a or not b:
        return 0.0
    inter = a & b
    union = a | b
    return len(inter) / len(union)


def containment(a: set, b: set) -> float:
    if not a or not b:
        return 0.0
    inter = a & b
    return len(inter) / min(len(a), len(b))


def main() -> int:
    n_files = 0
    n_pairs = 0
    for p in sorted(ROOT.rglob('*.html')):
        sp = str(p).replace('\\', '/')
        if any(s in sp for s in SKIP):
            continue
        try:
            text = p.read_text(encoding='utf-8', errors='replace')
        except Exception:
            continue
        # Strip <script>, <style>, <pre>, <code> first
        text_scan = re.sub(r'<script\b[\s\S]*?</script>', ' ', text,
                           flags=re.IGNORECASE)
        text_scan = re.sub(r'<style\b[\s\S]*?</style>', ' ', text_scan,
                           flags=re.IGNORECASE)

        # Collect callouts by type
        callouts_by_type: dict[str, list[tuple[int, set, str]]] = defaultdict(list)
        for m in CALLOUT_OPEN.finditer(text_scan):
            ctype = m.group(1).strip().lower()
            # Window: from the callout opening through the next 1500 chars
            # (typical callout is <300 chars; covers the inner <p>).
            inner = text_scan[m.end():m.end() + 1500]
            # Cut at the next callout opening or major section break
            cut = re.search(
                r'<div\s+class="callout\s+|<h[1-3]\b|<section\b',
                inner, re.IGNORECASE)
            if cut:
                inner = inner[:cut.start()]
            # Skip transient callout types we want to ignore for dedup
            if ctype in ('looking-back', 'cross-ref', 'self-check',
                         'exercise', 'thesis-thread', 'production-pattern',
                         'postmortem'):
                continue
            # Build a single text bag of all <p> children
            parts = [pm.group(1) for pm in INNER_P.finditer(inner)]
            if not parts:
                continue
            body = ' '.join(parts)
            tokens, _, bigrams = normalize_tokens(body)
            if len(tokens) < 8:
                continue
            line = text_scan.count('\n', 0, m.start()) + 1
            callouts_by_type[ctype].append((line, tokens, bigrams, body))

        file_hits: list[tuple[str, int, int, float, str, str]] = []
        for ctype, entries in callouts_by_type.items():
            for i in range(len(entries)):
                for j in range(i + 1, len(entries)):
                    li, ti, gi, bi = entries[i]
                    lj, tj, gj, bj = entries[j]
                    overlap = len(ti & tj)
                    bigram_overlap = len(gi & gj)
                    j_score = jaccard(ti, tj)
                    c_score = containment(ti, tj)
                    # Trigger: strong containment + sufficient overlap,
                    # OR many shared bigrams.
                    if ((c_score >= 0.30 and overlap >= 5) or
                            bigram_overlap >= 3 or
                            (j_score >= 0.45 and overlap >= 4)):
                        file_hits.append(
                            (ctype, li, lj, c_score,
                             HTML_TAG.sub('', bi)[:100],
                             HTML_TAG.sub('', bj)[:100]))
        if file_hits:
            n_files += 1
            n_pairs += len(file_hits)
            print(f'\n{p.relative_to(ROOT)}:')
            for ctype, li, lj, s, b1, b2 in file_hits:
                print(f'  [{ctype:18s}] L{li} <-> L{lj} '
                      f'(jaccard={s:.2f})')
                print(f'    A: {b1.strip()[:80]}')
                print(f'    B: {b2.strip()[:80]}')
    print(f'\nFiles with near-duplicate callouts: {n_files}')
    print(f'Near-duplicate pairs: {n_pairs}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
