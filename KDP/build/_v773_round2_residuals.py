"""v773: Apply Round 2 audit residuals.

Quality audit (FM/Appendix/Part):
  A5. appendix-c-python-for-llms (extra "s") -> appendix-c-python-for-llm
  A6. part-11 "Three chapters" overview duplicate "(Chapter 34)"
  B2. "Module 28 (Observability sections)" still in 4 part-11 prereqs
  B3. data-merged-from="section-32.X" attributes (Ch 32 doesn't exist)
  B6. "Module 34" -> "Chapter 34" in module-35 prereq link

Math audit:
  C4 CRITICAL. appendix-ad pricing $/$$/$$$/$$$$ glyphs eaten by KaTeX
  B.1 7 more escaped-dollar bugs (17.1, 33.5, 9.7 missed in v768)
  A.1 b.2 row label "layer normalization" for cross-entropy (wrong)
  A.2 L_CLM/L_MLM/L_MTP missing minus signs (6.2)
  B.4 8 more \\Sigma -> \\sum
  C.3 1 remaining <p class="math-display"> (8.1)
"""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SKIP = ('KDP/build/source_fix_backups', 'KDP/html2epub/tests',
        'pagefind', 'node_modules', 'temp_epub', '.git', 'venv')


def should_skip(p: Path) -> bool:
    sp = str(p).replace('\\', '/')
    return any(s in sp for s in SKIP)


total = 0


def patch(p: Path, old: str, new: str, label: str) -> None:
    global total
    if not p.exists():
        print(f'  SKIP missing {p.relative_to(ROOT)}')
        return
    s = p.read_text(encoding='utf-8')
    if old in s:
        c = s.count(old)
        s = s.replace(old, new)
        p.write_text(s, encoding='utf-8')
        total += c
        print(f'  [{label} x{c}] {p.relative_to(ROOT)}')
    else:
        print(f'  [skip {label}: not found] {p.relative_to(ROOT)}')


def regex_patch(p: Path, pat: str, rep: str, label: str,
                flags: int = 0) -> None:
    global total
    if not p.exists():
        return
    s = p.read_text(encoding='utf-8')
    new, n = re.subn(pat, rep, s, flags=flags)
    if n:
        p.write_text(new, encoding='utf-8')
        total += n
        print(f'  [{label} x{n}] {p.relative_to(ROOT)}')


# ============================================================
# A5: appendix-c-python-for-llms (extra "s") -> appendix-c-python-for-llm
# ============================================================
ak = ROOT / 'appendices' / 'appendix-ak-course-syllabi' / 'index.html'
patch(ak, 'appendix-c-python-for-llms/index.html',
      'appendix-c-python-for-llm/index.html',
      'A5 appendix-c xref')

# ============================================================
# A6: part-11 "Three chapters" duplicated (Chapter 34)
# ============================================================
p11 = ROOT / 'part-11-idea-to-product' / 'index.html'
patch(p11,
      'Three chapters cover the full journey: framing the product hypothesis '
      'and assessing feasibility (Chapter 34), building with the observe-steer '
      'loop and crossing the prototype-to-MVP bridge (Chapter 34), and shipping '
      'with sound economics, provider portability, and post-launch monitoring '
      '(Chapter 35).',
      'Two chapters cover the full journey: framing the product hypothesis, '
      'assessing feasibility, and building with the observe-steer loop '
      '(Chapter 34), then shipping with sound economics, provider portability, '
      'and post-launch monitoring (Chapter 35).',
      'A6 part-11 Three chapters')

# ============================================================
# B2: "Module 28 (Observability sections)" residual in 4 part-11 prereqs
# Pattern: <a class="prereq-link" href="...">Module 28</a> (<a ...>Observability</a> sections)
# Fix: convert "Module 28" -> "Chapter 28" and drop the parenthetical "(Observability sections)"
# ============================================================
pat_mod28 = re.compile(
    r'<a class="prereq-link"\s+href="([^"]*module-28-evaluation-observability[^"]*)">'
    r'Module 28</a>\s*\(<a class="glossary-link" href="[^"]*"\s*'
    r'title="Glossary: Observability">Observability</a>\s*sections\)')
repl_mod28 = (r'<a class="prereq-link" href="\1">Chapter 28: Evaluation</a>')

for fp in [
    ROOT / 'part-11-idea-to-product/module-34-idea-to-product/section-34.5.html',
    ROOT / 'part-11-idea-to-product/module-34-idea-to-product/section-34.7.html',
    ROOT / 'part-11-idea-to-product/module-35-shipping-scaling/section-35.1.html',
    ROOT / 'part-11-idea-to-product/module-35-shipping-scaling/section-35.4.html',
]:
    if fp.exists():
        s = fp.read_text(encoding='utf-8')
        new, n = pat_mod28.subn(repl_mod28, s)
        if n:
            fp.write_text(new, encoding='utf-8')
            total += n
            print(f'  [B2 Module 28 prereq x{n}] {fp.relative_to(ROOT)}')

# ============================================================
# B3: Strip data-merged-from attributes (Ch 32 doesn't exist)
# ============================================================
n_dmf_files = 0
n_dmf_total = 0
for hp in ROOT.rglob('*.html'):
    if should_skip(hp):
        continue
    try:
        s = hp.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        continue
    new, n = re.subn(r'\s*data-merged-from="[^"]*"', '', s)
    if n:
        hp.write_text(new, encoding='utf-8')
        n_dmf_files += 1
        n_dmf_total += n
print(f'  [B3 data-merged-from x{n_dmf_total} across {n_dmf_files} files]')
total += n_dmf_total

# ============================================================
# B6: "Module 34" -> "Chapter 34" in module-35-shipping-scaling/index.html
# ============================================================
m35 = ROOT / 'part-11-idea-to-product' / 'module-35-shipping-scaling' / 'index.html'
if m35.exists():
    s = m35.read_text(encoding='utf-8')
    new, n = re.subn(
        r'<a class="prereq-link"\s+([^>]*href="[^"]*module-34[^"]*"[^>]*)>Module 34</a>',
        r'<a class="prereq-link" \1>Chapter 34</a>',
        s)
    if n:
        m35.write_text(new, encoding='utf-8')
        total += n
        print(f'  [B6 Module 34 link x{n}] {m35.relative_to(ROOT)}')

# ============================================================
# Math C4 CRITICAL: appendix-ad pricing $/$$/$$$/$$$$ glyphs
# Replace with HTML-entity dollar signs so KaTeX won't eat them.
# ============================================================
ad = ROOT / 'appendices' / 'appendix-ad-master-reference-tables' / 'index.html'
if ad.exists():
    s = ad.read_text(encoding='utf-8')
    # Convert literal $$, $$$, $$$$ sequences inside table cells
    # (only targeting these inside <td>...</td> to avoid affecting other math)
    def escape_dollars_in_td(m: re.Match) -> str:
        cell = m.group(0)
        # Replace $X with &#36;X (where X is non-math context: end of cell or whitespace)
        cell = cell.replace('$$$$', '&#36;&#36;&#36;&#36;')
        cell = cell.replace('$$$', '&#36;&#36;&#36;')
        cell = cell.replace('$$', '&#36;&#36;')
        return cell

    new = re.sub(r'<td[^>]*>[^<]*</td>', escape_dollars_in_td, s)
    if new != s:
        ad.write_text(new, encoding='utf-8')
        nfix = sum(s.count(x) - new.count(x) for x in ['$$', '$$$', '$$$$'])
        total += nfix
        print(f'  [C4 pricing $$ glyphs escaped] {ad.relative_to(ROOT)}')

# ============================================================
# Math A.1: appendix-b.2 cross-entropy mislabeled "layer normalization"
# ============================================================
b2 = ROOT / 'appendices' / 'appendix-b-ml-essentials' / 'section-b.2.html'
if b2.exists():
    s = b2.read_text(encoding='utf-8')
    # This was caused by the v765 over-replacement bug: glossary tooltip
    # for "Layer Normalization" was wrongly inserted into a Cross-Entropy
    # row. Replace specifically the cross-entropy row.
    # Look for "layer normalization" + cross-entropy formula proximity.
    pat = re.compile(
        r'<a class="glossary-link" href="[^"]*gl-layer-norm[^"]*"\s*'
        r'title="Glossary: Layer Normalization">layer normalization</a>'
        r'(\s*</td>\s*<td>\s*<span class="math">\$-\s*\\Sigma)')
    new, n = pat.subn(
        r'<a class="glossary-link" href="../appendix-f-glossary/section-f.4.html'
        r'#gl-cross-entropy" title="Glossary: Cross-Entropy">cross-entropy</a>\1',
        s)
    if n:
        b2.write_text(new, encoding='utf-8')
        total += n
        print(f'  [A.1 b.2 cross-entropy label x{n}] {b2.relative_to(ROOT)}')

# ============================================================
# Math A.2: L_CLM/L_MLM/L_MTP missing minus in 6.2
# Try several whitespace variants
# ============================================================
sec62 = ROOT / 'part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.2.html'
if sec62.exists():
    s = sec62.read_text(encoding='utf-8')
    n_total = 0
    # L_CLM with various whitespace
    for old, new in [
        ('$L_{CLM} = \\sum', '$L_{CLM} = -\\sum'),
        ('$L_{MLM} = \\sum', '$L_{MLM} = -\\sum'),
        ('$L_{MTP} = \\sum', '$L_{MTP} = -\\sum'),
        ('$$L_{CLM} = \\sum', '$$L_{CLM} = -\\sum'),
        ('$$L_{MLM} = \\sum', '$$L_{MLM} = -\\sum'),
        ('$$L_{MTP} = \\sum', '$$L_{MTP} = -\\sum'),
    ]:
        if old in s:
            s = s.replace(old, new)
            n_total += 1
    if n_total:
        sec62.write_text(s, encoding='utf-8')
        total += n_total
        print(f'  [A.2 L_X minus signs x{n_total}] {sec62.relative_to(ROOT)}')

# ============================================================
# Math B.1: 7 more escaped-dollar bugs (17.1, 33.5, 9.7)
# Pattern: \$<math-content>$  ->  $<math-content>$
# ============================================================
files = [
    ROOT / 'part-4-training-adapting/module-17-alignment-rlhf-dpo/section-17.1.html',
    ROOT / 'part-10-frontiers/module-33-emerging-architectures/section-33.5.html',
    ROOT / 'part-2-understanding-llms/module-09-inference-optimization/section-9.7.html',
]
pat = re.compile(r'\\(\$[A-Za-z0-9_\\^{}\(\)\+\-\*\/\.\, ]{1,120}\$)')
for fp in files:
    if not fp.exists():
        continue
    s = fp.read_text(encoding='utf-8')
    # Track replacements; skip pure-currency forms
    def repl(m):
        inner = m.group(1)[1:-1]
        if re.fullmatch(r'[\d,\.]+', inner):
            return m.group(0)  # legitimate currency
        return m.group(1)
    new, _ = pat.subn(repl, s)
    if new != s:
        c = sum(1 for _ in pat.finditer(s)) - sum(1 for _ in pat.finditer(new))
        fp.write_text(new, encoding='utf-8')
        total += c
        print(f'  [B.1 escaped-dollar x{c}] {fp.relative_to(ROOT)}')

# ============================================================
# Math B.4: 8 more \Sigma -> \sum (Round 1 caught some, more remain)
# ============================================================
sigma_files = [
    'part-1-foundations/module-03-sequence-models-attention/section-3.2.html',
    'part-1-foundations/module-03-sequence-models-attention/section-3.3.html',
    'part-4-training-adapting/module-16-peft/section-16.5.html',
    'part-4-training-adapting/module-16-peft/section-16.7.html',
    'appendices/appendix-a-mathematical-foundations/section-a.2.html',
    'appendices/appendix-b-ml-essentials/section-b.2.html',
]
sigma_total = 0
for f in sigma_files:
    fp = ROOT / f
    if not fp.exists():
        continue
    s = fp.read_text(encoding='utf-8')
    # Replace \Sigma inside any math block
    def block_repl(m):
        return m.group(0).replace('\\Sigma', '\\sum')
    new = re.sub(r'\$\$.*?\$\$', block_repl, s, flags=re.DOTALL)
    new = re.sub(r'\$[^$\n]+\$', block_repl, new)
    if new != s:
        c = s.count('\\Sigma') - new.count('\\Sigma')
        fp.write_text(new, encoding='utf-8')
        sigma_total += c
print(f'  [B.4 \\Sigma -> \\sum x{sigma_total}]')
total += sigma_total

# ============================================================
# Quality audit B5: section-12.5 "Lab moved to Module 06" -> "Chapter 0"
# ============================================================
sec125 = ROOT / 'part-3-working-with-llms/module-12-prompt-engineering/section-12.5.html'
patch(sec125, 'Lab moved to Module 06', 'Lab moved to Chapter 0',
      'B5 section-12.5 Module 06 label')

print(f'\ntotal Round 2 residuals fixed: {total}')
