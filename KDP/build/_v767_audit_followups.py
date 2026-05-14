"""v767: Apply remaining audit follow-ups (toc, FM meta, appendix nav, etc.)."""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
fixes_applied = 0


def replace(p: Path, old: str, new: str, label: str) -> None:
    global fixes_applied
    if not p.exists():
        print(f'  SKIP missing {p}')
        return
    s = p.read_text(encoding='utf-8')
    if old in s:
        s = s.replace(old, new)
        p.write_text(s, encoding='utf-8')
        fixes_applied += 1
        print(f'  [{label}] {p.relative_to(ROOT)}')
    else:
        print(f'  [skip {label}: pattern not found] {p.relative_to(ROOT)}')


def regex_replace(p: Path, pat: str, rep: str, label: str) -> None:
    global fixes_applied
    if not p.exists():
        print(f'  SKIP missing {p}')
        return
    s = p.read_text(encoding='utf-8')
    new, n = re.subn(pat, rep, s)
    if n > 0:
        p.write_text(new, encoding='utf-8')
        fixes_applied += n
        print(f'  [{label} x{n}] {p.relative_to(ROOT)}')
    else:
        print(f'  [skip {label}: pattern not found] {p.relative_to(ROOT)}')


# 1. toc.html: stale meta + edition label
replace(ROOT / 'toc.html',
        '10 parts, 36 modules', '11 parts, 35 chapters',
        'toc meta count')
replace(ROOT / 'toc.html',
        'Industry-Specific Practitioner Guides (9th edition)',
        'Industry-Specific Practitioner Guides',
        'toc 9th-edition stale')

# 2. FM index meta description (currently generic)
replace(ROOT / 'front-matter' / 'index.html',
        '<meta name="description" content="Front Matter. A comprehensive chapter from the Building Conversational AI textbook.">',
        '<meta name="description" content="Front Matter: foreword, what the book covers, who it serves, how to use it, and copyright.">',
        'FM index meta')

# 3. about-authors meta
replace(ROOT / 'front-matter' / 'about-authors.html',
        '<meta name="description" content="About the Authors. A comprehensive chapter from the Building Conversational AI textbook.">',
        '<meta name="description" content="About the authors: Alexander (Sasha) Apartsin and Yehudit Aperstein, including backgrounds, research areas, and teaching experience.">',
        'about-authors meta')

# 4. FM.3 SVG label "through 37" -> "through 35"
replace(ROOT / 'front-matter' / 'fm-what-this-book-covers.html',
        'Chapters 26 through 37',
        'Chapters 26 through 35',
        'FM.3 SVG range')

# 5. FM.4 "Chapter 00.3" -> "Section 0.3"
replace(ROOT / 'front-matter' / 'fm-who-should-read.html',
        'Chapter 00.3 teaches PyTorch', 'Section 0.3 teaches PyTorch',
        'FM.4 chapter 00.3')

# 6. Add chapter-label divs to look-inside-preview and copyright
def add_chapter_label(p: Path, name: str) -> None:
    global fixes_applied
    if not p.exists():
        return
    s = p.read_text(encoding='utf-8')
    if 'class="chapter-label"' in s:
        print(f'  [skip {name}: chapter-label already present]')
        return
    # Inject after part-label
    new = re.sub(
        r'(<div class="part-label" data-pagefind-meta="part">[^<]*'
        r'(?:<a[^>]*>[^<]*</a>)?</div>)',
        r'\1\n    <div class="chapter-label" data-pagefind-meta="chapter">'
        r'<a href="index.html">Front Matter</a></div>',
        s, count=1)
    if new != s:
        p.write_text(new, encoding='utf-8')
        fixes_applied += 1
        print(f'  [add chapter-label] {p.relative_to(ROOT)}')

add_chapter_label(ROOT / 'front-matter' / 'look-inside-preview.html', 'look-inside')
add_chapter_label(ROOT / 'front-matter' / 'copyright.html', 'copyright')

# 7. Appendix L section-l.5 next: self-loop -> Appendix R
replace(ROOT / 'appendices' / 'appendix-l-langchain' / 'section-l.5.html',
        '<a class="next" href="../appendix-l-langchain/index.html">LangGraph</a>',
        '<a class="next" href="../appendix-r-experiment-tracking/index.html">Appendix R: Experiment Tracking</a>',
        'App L.5 next')

# 8. Appendix V section-v.3 missing next link
def add_v3_next(p: Path) -> None:
    global fixes_applied
    if not p.exists():
        return
    s = p.read_text(encoding='utf-8')
    if 'appendix-w-legal-llms' in s:
        print(f'  [skip v.3 next: already present]')
        return
    # Find chapter-nav and inject next if missing
    nav_m = re.search(r'<nav class="chapter-nav">(.*?)</nav>', s, re.DOTALL)
    if not nav_m:
        print(f'  [skip v.3: no chapter-nav]')
        return
    inner = nav_m.group(1)
    if 'class="next"' in inner:
        print(f'  [skip v.3 next: next link already present]')
        return
    # Append next link before </nav>
    new_nav = (nav_m.group(0).replace(
        '</nav>',
        '<a class="next" href="../appendix-w-legal-llms/index.html">'
        'Appendix W: LLMs in Legal Practice &rarr;</a>\n</nav>'))
    new_s = s.replace(nav_m.group(0), new_nav, 1)
    p.write_text(new_s, encoding='utf-8')
    fixes_applied += 1
    print(f'  [add v.3 next] {p.relative_to(ROOT)}')

add_v3_next(ROOT / 'appendices' / 'appendix-v-tooling-ecosystem' / 'section-v.3.html')

# 9. section-34.7 line 491 broken sentence
replace(ROOT / 'part-11-idea-to-product' / 'module-34-idea-to-product' / 'section-34.7.html',
        'This section concludes Module 34<a href="../module-35-shipping-scaling/index.html">Chapter 35:',
        'This section concludes Chapter 34. In <a href="../module-35-shipping-scaling/index.html">Chapter 35:',
        '34.7 broken sentence')

# 10. Module-prose -> Chapter-prose sweep (terminology rule)
def module_to_chapter_sweep() -> None:
    global fixes_applied
    SKIP = ('KDP/build/source_fix_backups', 'pagefind', 'node_modules',
            'temp_epub', '.git', 'venv')
    # Only replace " Module NN" or "(Module NN)" -> "Chapter NN" in body prose,
    # NOT inside <span class="mod-num">Module NN</span> labels (those will be
    # handled separately if needed) and NOT inside HTML comments.
    pat = re.compile(r'\bModule (\d{1,2})\b(?![<\d])')
    n_files = 0
    n_total = 0
    for hp in ROOT.rglob('*.html'):
        sp = str(hp).replace('\\', '/')
        if any(s in sp for s in SKIP):
            continue
        try:
            src = hp.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            continue
        # Don't touch label spans
        # Build replacements only outside <span class="mod-num">...</span>
        # Strategy: find spans, mask them out, do regex, unmask.
        spans = []
        def stash(m):
            spans.append(m.group(0))
            return f'\x00MODNUM{len(spans)-1}\x00'
        masked = re.sub(r'<span class="mod-num">[^<]*</span>',
                        stash, src)
        # Don't replace inside <!-- comments -->
        new_masked = pat.sub(r'Chapter \1', masked)
        # Unmask
        def unstash(m):
            i = int(m.group(1))
            return spans[i]
        new = re.sub(r'\x00MODNUM(\d+)\x00', unstash, new_masked)
        if new != src:
            n = sum(1 for _ in pat.finditer(masked))
            hp.write_text(new, encoding='utf-8')
            n_files += 1
            n_total += n
    print(f'  [Module->Chapter sweep] {n_total} replacements across {n_files} files')
    fixes_applied += n_total

module_to_chapter_sweep()

print(f'\ntotal fixes applied: {fixes_applied}')
