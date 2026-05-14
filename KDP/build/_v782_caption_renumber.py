"""v782: Bulk-renumber stale Figure/Table/Code Fragment captions.

Pages 200-300 audit found systematic stale captions where the section
file is N.M but the caption inside still references the OLD chapter
number from before the v6.40 renumber:

  - Section 30.X has "Table 29.X.*" or "Code Fragment 30.X+1.*" captions
  - Section 31.X has "Table 30.X.*" captions
  - Section 33.X has "Table 32.X.*" or "Code Fragment 30.X+1.*" captions
  - Section 34.X has "Code Fragment 34.X+1.*" captions (off-by-one)

Plus 2 unresolved "33.3.X" / "33.12.X" placeholder H2 headers that should
be 30.3.X / 30.11.X with X resolved (or just X = 1).

Plus 7 anchor-text-vs-href Chapter NN mismatches (mostly off-by-one from
the renumber).

Strategy: walk every section file. For each <strong>Caption N.M.K:</strong>
inside it, if N != actual chapter from filename, rewrite N to match.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SKIP = ('KDP/build/source_fix_backups', 'KDP/html2pub/tests',
        'pagefind', 'node_modules', 'temp_epub', '.git', 'venv')


def should_skip(p: Path) -> bool:
    sp = str(p).replace('\\', '/')
    return any(s in sp for s in SKIP)


# Map filename -> expected chapter prefix
def expected_chap(p: Path) -> int | None:
    m = re.match(r'section-(\d+)\.\d+\.html', p.name)
    if m:
        return int(m.group(1))
    return None


CAPTION_RE = re.compile(
    r'<strong>(Figure|Table|Code Fragment)\s+(\d+)\.(\d+)\.(\d+)([a-z]?):'
)

n_total = 0
n_files = 0

for hp in ROOT.rglob('section-*.html'):
    if should_skip(hp):
        continue
    chap = expected_chap(hp)
    if chap is None:
        continue
    try:
        s = hp.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        continue

    # File chapter and section
    fm = re.match(r'section-(\d+)\.(\d+)\.html', hp.name)
    fchap = int(fm.group(1))
    fsec = int(fm.group(2))

    counter = [0]

    def repl(m: re.Match) -> str:
        kind, n_str, m_str, k_str, suffix = m.groups()
        n_int = int(n_str)
        if n_int != fchap:
            counter[0] += 1
            return f'<strong>{kind} {fchap}.{m_str}.{k_str}{suffix}:'
        return m.group(0)

    new = CAPTION_RE.sub(repl, s)
    if new != s:
        hp.write_text(new, encoding='utf-8')
        n_files += 1
        n_total += counter[0]
        print(f'  [{hp.relative_to(ROOT)}] {counter[0]} caption renumbers')

# Critical: the 2 placeholder ".X" H2 headers in 30.3 and 30.11
sec303 = ROOT / 'part-9-safety-strategy/module-30-safety-ethics-regulation/section-30.3.html'
if sec303.exists():
    s = sec303.read_text(encoding='utf-8')
    new, n = re.subn(
        r'<h2>33\.3\.X Cross-Cultural NLP and Pluralistic Alignment</h2>',
        '<h2>30.3.4 Cross-Cultural NLP and Pluralistic Alignment</h2>',
        s)
    if n:
        sec303.write_text(new, encoding='utf-8')
        n_total += n
        print(f'  [30.3 placeholder header x{n}]')

sec3011 = ROOT / 'part-9-safety-strategy/module-30-safety-ethics-regulation/section-30.11.html'
if sec3011.exists():
    s = sec3011.read_text(encoding='utf-8')
    new, n = re.subn(
        r'<h2>33\.12\.X Federated Learning for Privacy-Preserving Training</h2>',
        '<h2>30.11.4 Federated Learning for Privacy-Preserving Training</h2>',
        s)
    if n:
        sec3011.write_text(new, encoding='utf-8')
        n_total += n
        print(f'  [30.11 placeholder header x{n}]')

# 7 anchor-text-vs-href Chapter NN mismatches from pages 200-300 audit
anchor_fixes = [
    # ch_0230 section-30.10: text "Chapter 17" -> module-16-peft (actually Ch 16)
    (ROOT / 'part-9-safety-strategy/module-30-safety-ethics-regulation/section-30.10.html',
     re.compile(r'<a([^>]*href="[^"]*module-16-peft[^"]*"[^>]*)>Chapter 17</a>'),
     r'<a\1>Chapter 16</a>',
     '30.10 Ch 17 -> 16'),
    # ch_0244 section-33.2: text "Chapter 17" -> module-16-peft (Ch 16)
    (ROOT / 'part-10-frontiers/module-33-emerging-architectures/section-33.2.html',
     re.compile(r'<a([^>]*href="[^"]*module-16-peft[^"]*"[^>]*)>Chapter 17</a>'),
     r'<a\1>Chapter 16</a>',
     '33.2 Ch 17 -> 16'),
    # ch_0248 section-33.6: "Chapter 14" -> module-20-conversational-ai (Ch 20)
    (ROOT / 'part-10-frontiers/module-33-emerging-architectures/section-33.6.html',
     re.compile(r'<a([^>]*href="[^"]*module-20-conversational-ai[^"]*"[^>]*)>Chapter 14</a>'),
     r'<a\1>Chapter 20</a>',
     '33.6 Ch 14 -> 20'),
    # ch_0248 section-33.6: "Chapter 17" -> module-19-rag (Ch 19)
    (ROOT / 'part-10-frontiers/module-33-emerging-architectures/section-33.6.html',
     re.compile(r'<a([^>]*href="[^"]*module-19-rag[^"]*"[^>]*)>Chapter 17</a>'),
     r'<a\1>Chapter 19</a>',
     '33.6 Ch 17 -> 19'),
    # ch_0249 section-33.7: "Chapter 18" -> module-15-fine-tuning-fundamentals (Ch 15)
    (ROOT / 'part-10-frontiers/module-33-emerging-architectures/section-33.7.html',
     re.compile(r'<a([^>]*href="[^"]*module-15-fine-tuning-fundamentals[^"]*"[^>]*)>Chapter 18</a>'),
     r'<a\1>Chapter 15</a>',
     '33.7 Ch 18 -> 15'),
    # ch_0251 section-33.9: "Chapter 05" -> module-04-transformer-architecture (Ch 4)
    (ROOT / 'part-10-frontiers/module-33-emerging-architectures/section-33.9.html',
     re.compile(r'<a([^>]*href="[^"]*module-04-transformer-architecture[^"]*"[^>]*)>Chapter 05</a>'),
     r'<a\1>Chapter 4</a>',
     '33.9 Ch 05 -> 4'),
    # ch_0277 appendix-a section-a.6: "Chapter 17" -> module-16-peft (Ch 16)
    (ROOT / 'appendices/appendix-a-mathematical-foundations/section-a.6.html',
     re.compile(r'<a([^>]*href="[^"]*module-16-peft[^"]*"[^>]*)>Chapter 17</a>'),
     r'<a\1>Chapter 16</a>',
     'a.6 Ch 17 -> 16'),
]
for fp, pat, rep, label in anchor_fixes:
    if not fp.exists():
        print(f'  [skip {label}: file missing]')
        continue
    s = fp.read_text(encoding='utf-8')
    new, n = pat.subn(rep, s)
    if n:
        fp.write_text(new, encoding='utf-8')
        n_total += n
        print(f'  [{label} x{n}]')

print(f'\nTotal v782 fixes: {n_total} across {n_files}+ files')
