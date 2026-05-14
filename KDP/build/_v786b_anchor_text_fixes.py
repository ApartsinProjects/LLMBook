"""v786b: Fix anchor-text vs href mismatches identified by audit.

Manual triage (each href verified against destination's actual H1):

A. CROSS-CHAPTER ANCHOR TEXT WRONG (href correct):
   - 8.6: anchor "Section 10.1" -> destination is 18.1
   - 14.3: anchor "Section 17.1" -> destination is 16.5
   - 27.3: anchor "Section 24.5" -> destination is 24.1
   - 29.2: anchor "Section 21.2" -> destination is 21.6

B. CORRUPTED GLOSSARY LINK TEXT "Section 4.1 loss" should be "cross-entropy loss":
   - a.5 + 16.3 + f.3: link target is glossary entry #gl-cross-entropy

C. APPENDIX T HREFS WRONG (anchor text correct, href bulk-replaced badly):
   The destination titles tell us what the link SHOULD point to:
     - "Section T.1" anchor (href=t.4) means PySpark which IS section-t.1.html
       so href t.4 is wrong, should be t.1
     - "Section T.6" anchor (href=t.1) means feature stores which IS section-t.6.html
       so href t.1 should be t.6
     - "Section T.4" anchor (href=t.1) means Databricks AI which IS section-t.4.html
       so href t.1 should be t.4
     - "Section T.3" anchor (href=t.4) means Databricks workspace which IS section-t.3.html
       so href t.4 should be t.3
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

n_total = 0


def fix(path_rel, find_re, replace, label):
    global n_total
    fp = ROOT / path_rel
    if not fp.exists():
        print(f'  [skip {label}: file missing]')
        return
    s = fp.read_text(encoding='utf-8')
    new, n = re.subn(find_re, replace, s)
    if n:
        fp.write_text(new, encoding='utf-8')
        n_total += n
        print(f'  [{label} x{n}]')
    else:
        print(f'  [no match: {label}]')


# A. Cross-chapter anchor-text fixes
fix('part-2-understanding-llms/module-08-reasoning-test-time-compute/section-8.6.html',
    re.compile(
        r'(<a[^>]*href="[^"]*section-18\.1[^"]*"[^>]*>'
        r'embedding-based retrieval in Section )10\.1(</a>)'),
    r'\g<1>18.1\g<2>',
    '8.6: Section 10.1 -> 18.1')

fix('part-4-training-adapting/module-14-synthetic-data/section-14.3.html',
    re.compile(
        r'(<a[^>]*href="[^"]*section-16\.5[^"]*"[^>]*>'
        r'knowledge distillation \(Section )17\.1(\)</a>)'),
    r'\g<1>16.5\g<2>',
    '14.3: Section 17.1 -> 16.5')

fix('part-7-multimodal-applications/module-27-llm-applications/section-27.3.html',
    re.compile(
        r'(<a[^>]*href="[^"]*section-24\.1[^"]*"[^>]*>'
        r'healthcare agent patterns from Section )24\.5(</a>)'),
    r'\g<1>24.1\g<2>',
    '27.3: Section 24.5 -> 24.1')

fix('part-8-evaluation-production/module-29-production-engineering/section-29.2.html',
    re.compile(
        r'(<a[^>]*href="[^"]*section-21\.6[^"]*"[^>]*>'
        r'tool use patterns from Section )21\.2(</a>)'),
    r'\g<1>21.6\g<2>',
    '29.2: Section 21.2 -> 21.6')

# B. Corrupted glossary link text
for path in ['appendices/appendix-a-mathematical-foundations/section-a.5.html',
             'part-4-training-adapting/module-16-peft/section-16.3.html',
             'appendices/appendix-f-glossary/section-f.3.html']:
    fix(path,
        re.compile(r'Section 4\.1 [Ll]oss'),
        'cross-entropy loss',
        f'{path}: Section 4.1 loss -> cross-entropy loss')
    fix(path,
        re.compile(r'Glossary: Section 4\.1 [Ll]oss'),
        'Glossary: Cross-Entropy Loss',
        f'{path}: title attr fix')

# C. Appendix T href fixes (bulk badly-renumbered anchors)
T_DIR = 'appendices/appendix-t-distributed-ml'

# Map: (anchor_says, current_wrong_href, correct_href)
# Each per-file pattern: <a href="OLD">Section T.X</a> -> <a href="NEW">Section T.X</a>
T_FIXES = [
    # 'Section T.1' references that point to t.4 should point to t.1
    ('section-t.4.html', 'Section T.1', 'section-t.1.html'),
    # 'Section T.6' references that point to t.1 should point to t.6
    ('section-t.1.html', 'Section T.6', 'section-t.6.html'),
    # 'Section T.4' references that point to t.1 should point to t.4
    ('section-t.1.html', 'Section T.4', 'section-t.4.html'),
    # 'Section T.3' references that point to t.4 should point to t.3
    ('section-t.4.html', 'Section T.3', 'section-t.3.html'),
]

for fp in (ROOT / T_DIR).glob('section-t.*.html'):
    s = fp.read_text(encoding='utf-8')
    new = s
    for wrong_href, anchor_text, correct_href in T_FIXES:
        # Build pattern: <a href="WRONG_HREF">SECTION T.X</a>
        pat = re.compile(
            r'<a([^>]*?)href="' + re.escape(wrong_href) + r'"([^>]*)>'
            + re.escape(anchor_text) + r'</a>')
        rep = r'<a\1href="' + correct_href + r'"\2>' + anchor_text + r'</a>'
        new2, n = pat.subn(rep, new)
        if n:
            print(f'  [{fp.name}: "{anchor_text}" {wrong_href} -> {correct_href} x{n}]')
            n_total += n
            new = new2
    if new != s:
        fp.write_text(new, encoding='utf-8')

print(f'\nTotal v786b fixes: {n_total}')
