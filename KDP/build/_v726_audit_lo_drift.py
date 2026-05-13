"""Audit learning-objective bullets against actual chapter content
for drift.

For each chapter's index.html:
  1. Extract <div class="objectives"><ul><li>...</li>...</ul></div>
  2. Extract section titles + descriptions from the chapter's
     <ul class="sections-list"><li><a><span class="section-title">...
     <span class="section-desc">...</a></li>
  3. Also read each section file's H1 + first paragraph as fallback content.
  4. For each LO bullet, compute a content-keyword score against the
     combined section content. Score = fraction of LO content tokens
     (>=4 chars, non-stopword) that appear in section content.
  5. LOs with score < 0.40 are flagged as "drift candidates".

Read-only audit. Reports per-chapter LO drift findings.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SKIP = ('node_modules', '.git/', 'pagefind/', 'KDP/build/', 'KDP/output/',
        'templates/', '_archive/', 'temp_epub/', 'vendor/', '/agents/')

OBJECTIVES_BLOCK = re.compile(
    r'<div\s+class="objectives"[^>]*>([\s\S]*?)</div>', re.IGNORECASE)
LI = re.compile(r'<li[^>]*>([\s\S]*?)</li>', re.IGNORECASE)
SECTION_CARD = re.compile(
    r'<a\s+href="(section-[^"]+\.html)"[^>]*>'
    r'\s*<span\s+class="section-num"[^>]*>[^<]*</span>'
    r'\s*<span\s+class="section-title"[^>]*>([^<]+)</span>'
    r'\s*<span\s+class="section-desc"[^>]*>([\s\S]*?)</span>',
    re.IGNORECASE)
HTML_TAG = re.compile(r'<[^>]+>')

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
'''.split())


def tokens(text: str) -> set:
    text = HTML_TAG.sub(' ', text)
    text = re.sub(r"&[a-zA-Z#0-9]+;", ' ', text)
    text = text.lower()
    toks = re.findall(r"[a-z][a-z\-]{3,}", text)
    return {t for t in toks if t not in STOPWORDS}


def score_lo(lo_tokens: set, content_tokens: set) -> float:
    if not lo_tokens:
        return 1.0
    return len(lo_tokens & content_tokens) / len(lo_tokens)


def main() -> int:
    n_chapters = 0
    n_drift = 0
    by_chapter: dict[str, list[tuple[str, float, set]]] = {}
    for index_p in sorted(ROOT.glob('part-*/module-*/index.html')):
        sp = str(index_p).replace('\\', '/')
        if any(s in sp for s in SKIP):
            continue
        try:
            text = index_p.read_text(encoding='utf-8', errors='replace')
        except Exception:
            continue
        ob = OBJECTIVES_BLOCK.search(text)
        if not ob:
            continue
        lo_bullets = [HTML_TAG.sub('', m.group(1)).strip()
                      for m in LI.finditer(ob.group(1))]
        if not lo_bullets:
            continue
        # Build chapter content bag: section title + desc + each section
        # file's H1 + first <p>
        content_text_parts: list[str] = []
        for sm in SECTION_CARD.finditer(text):
            content_text_parts.append(sm.group(2))  # title
            content_text_parts.append(sm.group(3))  # desc
        # Also pull H1 + h2 + first paragraph from each section file
        chapter_dir = index_p.parent
        for sec in sorted(chapter_dir.glob('section-*.html')):
            try:
                sec_text = sec.read_text(encoding='utf-8', errors='replace')
            except Exception:
                continue
            h1 = re.search(r'<h1[^>]*>([\s\S]*?)</h1>', sec_text, re.IGNORECASE)
            if h1:
                content_text_parts.append(h1.group(1))
            for hm in re.finditer(r'<h2[^>]*>([\s\S]*?)</h2>',
                                  sec_text, re.IGNORECASE):
                content_text_parts.append(hm.group(1))
            # First substantive <p> after <main>
            main_m = re.search(r'<main\b[^>]*>([\s\S]*?)</main>',
                               sec_text, re.IGNORECASE)
            if main_m:
                p_text = HTML_TAG.sub(' ', main_m.group(1))[:3000]
                content_text_parts.append(p_text)
        content_tokens = tokens(' '.join(content_text_parts))
        n_chapters += 1
        chapter_drift: list[tuple[str, float, set]] = []
        for lo in lo_bullets:
            lo_t = tokens(lo)
            if not lo_t:
                continue
            s = score_lo(lo_t, content_tokens)
            if s < 0.40:
                missing = lo_t - content_tokens
                chapter_drift.append((lo[:120], s, missing))
        if chapter_drift:
            n_drift += len(chapter_drift)
            by_chapter[str(index_p.relative_to(ROOT))] = chapter_drift
    print(f'Chapters scanned: {n_chapters}')
    print(f'LO drift candidates: {n_drift}')
    print()
    for fp in sorted(by_chapter.keys()):
        print(f'\n{fp}:')
        for lo, score, missing in by_chapter[fp]:
            print(f'  [score={score:.2f}] {lo}')
            print(f'    missing keywords: {", ".join(sorted(missing))[:200]}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
