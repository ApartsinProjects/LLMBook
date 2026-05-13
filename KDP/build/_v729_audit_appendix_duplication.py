"""Audit appendices for content that duplicates main-book chapters.

User reported: "audit appendices, it seems that some just repeat main
content, either drop or rewrite/update" + "check if appendix covers
theory that already discussed in the book, if so cross-reference to it"

Strategy:
1. Build a bag of significant content keywords for each main chapter
   (top 50 distinctive terms per chapter, ignoring stopwords).
2. For each appendix, compute keyword overlap with each chapter.
3. Report appendices with >40% overlap to a single chapter as
   "potentially duplicates X" — these likely need rewrite or cross-ref.
4. Report appendices that already link extensively to chapters
   (high cross-ref density) as "well-integrated" — no action needed.
5. Print summary table.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parent.parent.parent
SKIP = ('node_modules', '.git/', 'pagefind/', 'KDP/build/', 'KDP/output/',
        'templates/', '_archive/', 'temp_epub/', 'vendor/', '/agents/')

HTML_TAG = re.compile(r'<[^>]+>')
SCRIPT_BLOCK = re.compile(r'<script\b[\s\S]*?</script>', re.IGNORECASE)
STYLE_BLOCK = re.compile(r'<style\b[\s\S]*?</style>', re.IGNORECASE)
PRE_BLOCK = re.compile(r'<pre\b[\s\S]*?</pre>', re.IGNORECASE)
CODE_BLOCK = re.compile(r'<code\b[\s\S]*?</code>', re.IGNORECASE)

STOPWORDS = set('''
the a an and or but of to in is are was were be been being have has had
do does did this that these those it its on for with at by from as if then
than not no so we you they i he she them their our your his her you'll
this that these those when how why what who which where can could should
would will may might must any all some each every other another like also
just only even though although because while if since via using upon over
about into within between through across against towards toward up down
many more most less few enough such same own here there now today
have having make made take takes taken come came goes going used use uses
new old high low full empty true false good bad large small big medium
section chapter book part module appendix figure code example
chapter chapters part parts section sections module modules
'''.split())


def clean_text(text: str) -> str:
    text = SCRIPT_BLOCK.sub(' ', text)
    text = STYLE_BLOCK.sub(' ', text)
    text = PRE_BLOCK.sub(' ', text)
    text = CODE_BLOCK.sub(' ', text)
    text = HTML_TAG.sub(' ', text)
    text = re.sub(r'&[a-zA-Z#0-9]+;', ' ', text)
    return text.lower()


def keyword_set(text: str, top_n: int = 80) -> set:
    cleaned = clean_text(text)
    tokens = re.findall(r"[a-z][a-z\-]{4,}", cleaned)
    counter = Counter(t for t in tokens if t not in STOPWORDS)
    # Distinctive = high count, but also not too common across all docs.
    # Simple heuristic: top-N by frequency.
    return {w for w, _ in counter.most_common(top_n)}


def gather_chapter_text(chap_dir: Path) -> str:
    parts = []
    for p in sorted(chap_dir.glob('section-*.html')):
        try:
            parts.append(p.read_text(encoding='utf-8', errors='replace'))
        except Exception:
            pass
    idx = chap_dir / 'index.html'
    if idx.exists():
        try:
            parts.append(idx.read_text(encoding='utf-8', errors='replace'))
        except Exception:
            pass
    return ' '.join(parts)


def gather_appendix_text(app_dir: Path) -> str:
    parts = []
    for p in sorted(app_dir.glob('*.html')):
        try:
            parts.append(p.read_text(encoding='utf-8', errors='replace'))
        except Exception:
            pass
    return ' '.join(parts)


def count_cross_refs(text: str) -> int:
    """Count <a href> links to part-X/ paths (chapter cross-refs)."""
    return len(re.findall(r'<a\s[^>]*href="[^"]*part-\d+', text, re.IGNORECASE))


def main() -> int:
    # Gather chapter keyword sets
    chap_keywords: dict[str, set] = {}
    chap_short: dict[str, str] = {}
    for chap_dir in sorted(ROOT.glob('part-*/module-*/')):
        if not chap_dir.is_dir():
            continue
        text = gather_chapter_text(chap_dir)
        kws = keyword_set(text)
        if not kws:
            continue
        rel = str(chap_dir.relative_to(ROOT)).replace('\\', '/')
        chap_keywords[rel] = kws
        # Friendly name: module-NN-name
        m = re.search(r'module-(\d+)-(.+)', chap_dir.name)
        if m:
            chap_short[rel] = f'Ch {m.group(1)} ({m.group(2)})'
        else:
            chap_short[rel] = chap_dir.name

    print(f'Indexed {len(chap_keywords)} chapters.')

    # For each appendix, find best chapter match
    print(f'\n{"Appendix":<50s} | {"Top match":<35s} | {"Overlap":>8s} | {"Cross-refs":>10s} | Action')
    print('-' * 130)
    for app_dir in sorted(ROOT.glob('appendices/appendix-*/')):
        if not app_dir.is_dir():
            continue
        text = gather_appendix_text(app_dir)
        if not text:
            continue
        app_kws = keyword_set(text)
        n_refs = count_cross_refs(text)
        # Compute overlap with each chapter
        best_chap = None
        best_overlap = 0
        best_overlap_count = 0
        for chap_rel, chap_kws in chap_keywords.items():
            overlap = app_kws & chap_kws
            ratio = len(overlap) / len(app_kws) if app_kws else 0
            if ratio > best_overlap:
                best_overlap = ratio
                best_chap = chap_rel
                best_overlap_count = len(overlap)
        app_name = app_dir.name
        # Action heuristic
        if best_overlap >= 0.40 and n_refs < 5:
            action = 'REWRITE or DROP (high overlap, few cross-refs)'
        elif best_overlap >= 0.40 and n_refs >= 5:
            action = 'OK (overlap but well-integrated)'
        elif best_overlap < 0.25:
            action = 'OK (distinct content)'
        else:
            action = 'ADD CROSS-REFS to canonical content'
        top = chap_short.get(best_chap, '(none)') if best_chap else '(none)'
        print(f'{app_name:<50s} | {top:<35s} | {best_overlap*100:>6.1f}% | {n_refs:>10d} | {action}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
