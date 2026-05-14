"""v779: Apply next-100 audit critical + high fixes."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
total = 0


def patch(p, old, new, label):
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


# ============================================================
# CRITICAL: Section 17.5 stray </a> after part-label
# ============================================================
sec175 = ROOT / 'part-4-training-adapting/module-17-alignment-rlhf-dpo/section-17.5.html'
if sec175.exists():
    s = sec175.read_text(encoding='utf-8')
    new, n = re.subn(
        r'<div class="part-label" data-pagefind-meta="part">Part 4</a></div>',
        '<div class="part-label" data-pagefind-meta="part">Part IV: Training &amp; Adapting</div>',
        s)
    if n:
        sec175.write_text(new, encoding='utf-8')
        total += n
        print(f'  [17.5 stray </a> x{n}]')

# ============================================================
# CRITICAL: Section 19.1 broken "Section 19.0" reference
# ============================================================
sec191 = ROOT / 'part-5-retrieval-conversation/module-19-rag/section-19.1.html'
patch(sec191,
      'Section 19.0 (the Knowledge Storage Spectrum)',
      'the Knowledge Storage Spectrum (Appendix AD: Master Reference Tables)',
      '19.1 Section 19.0')

# ============================================================
# CRITICAL: Section 25.5 lab content swallowed by warning callout
# Need to insert closing </div> after the warning <p>
# ============================================================
sec255 = ROOT / 'part-6-agentic-ai/module-25-agent-safety-production/section-25.5.html'
if sec255.exists():
    s = sec255.read_text(encoding='utf-8')
    # Look for: <div class="callout warning"> ... <p>...</p> followed
    # by <div class="lab-objective"> (without intervening </div>)
    pat = re.compile(
        r'(<div class="callout warning">\s*'
        r'<div class="callout-title">[^<]*</div>\s*'
        r'<p>[^<]*</p>)\s*'
        r'(<div class="lab-objective">)',
        re.DOTALL)
    new, n = pat.subn(r'\1\n</div>\n\2', s)
    if n:
        sec255.write_text(new, encoding='utf-8')
        total += n
        print(f'  [25.5 warning callout close x{n}]')

# ============================================================
# HIGH: Section 16.3, 16.4 wrong "Chapter 17: Knowledge Distillation"
# Ch 17 is alignment; distillation is in sections 16.5/16.6 of THIS chapter
# ============================================================
for fp in [
    ROOT / 'part-4-training-adapting/module-16-peft/section-16.3.html',
    ROOT / 'part-4-training-adapting/module-16-peft/section-16.4.html',
]:
    if not fp.exists():
        continue
    s = fp.read_text(encoding='utf-8')
    # Replace href to bogus "module-17-distillation" with explicit
    # forward pointer to section-16.5
    new = s
    for old, new_v in [
        ('Chapter 17: Knowledge Distillation &amp; Model Merging',
         'Section 16.5: Knowledge Distillation'),
        ('Chapter 17: Knowledge Distillation & Model Merging',
         'Section 16.5: Knowledge Distillation'),
    ]:
        c = new.count(old)
        if c:
            new = new.replace(old, new_v)
            total += c
            print(f'  [{fp.name} Ch 17 -> Sec 16.5 x{c}]')
    if new != s:
        fp.write_text(new, encoding='utf-8')

# ============================================================
# HIGH: Section 15.4 anchor "Chapter 09" -> "Chapter 11"
# ============================================================
sec154 = ROOT / 'part-4-training-adapting/module-15-fine-tuning-fundamentals/section-15.4.html'
if sec154.exists():
    s = sec154.read_text(encoding='utf-8')
    # Find the specific anchor
    pat = re.compile(
        r'<a([^>]*href="[^"]*module-11-llm-apis[^"]*"[^>]*)>Chapter 09</a>')
    new, n = pat.subn(r'<a\1>Chapter 11</a>', s)
    if n:
        sec154.write_text(new, encoding='utf-8')
        total += n
        print(f'  [15.4 Chapter 09 -> 11 x{n}]')

# ============================================================
# HIGH: Section 14.1 anchor "Chapter 24" -> "Chapter 28"
# ============================================================
sec141 = ROOT / 'part-4-training-adapting/module-14-synthetic-data/section-14.1.html'
if sec141.exists():
    s = sec141.read_text(encoding='utf-8')
    pat = re.compile(
        r'<a([^>]*href="[^"]*module-28[^"]*"[^>]*)>Chapter 24</a>')
    new, n = pat.subn(r'<a\1>Chapter 28</a>', s)
    if n:
        sec141.write_text(new, encoding='utf-8')
        total += n
        print(f'  [14.1 Chapter 24 -> 28 x{n}]')

# ============================================================
# HIGH: Section 17.1 anchor "Chapter 25" -> "Chapter 30"
# ============================================================
sec171 = ROOT / 'part-4-training-adapting/module-17-alignment-rlhf-dpo/section-17.1.html'
if sec171.exists():
    s = sec171.read_text(encoding='utf-8')
    pat = re.compile(
        r'<a([^>]*href="[^"]*module-30[^"]*"[^>]*)>Chapter 25</a>')
    new, n = pat.subn(r'<a\1>Chapter 30</a>', s)
    if n:
        sec171.write_text(new, encoding='utf-8')
        total += n
        print(f'  [17.1 Chapter 25 -> 30 x{n}]')

# ============================================================
# HIGH: Stale Figure/Table caption numbers
# ============================================================
caption_fixes = [
    (ROOT / 'part-4-training-adapting/module-14-synthetic-data/section-14.7.html',
     '<strong>Table 13.8.1:</strong>',
     '<strong>Table 14.7.1:</strong>',
     '14.7 Table 13.8.1'),
    (ROOT / 'part-4-training-adapting/module-17-alignment-rlhf-dpo/section-17.1.html',
     '<strong>Figure 16.1.1a</strong>', '<strong>Figure 17.1.1a</strong>',
     '17.1 Figure 16.1.1a'),
    (ROOT / 'part-4-training-adapting/module-17-alignment-rlhf-dpo/section-17.1.html',
     '<strong>Figure 16.1.1b</strong>', '<strong>Figure 17.1.1b</strong>',
     '17.1 Figure 16.1.1b'),
    (ROOT / 'part-4-training-adapting/module-17-alignment-rlhf-dpo/section-17.1.html',
     '<strong>Figure 16.1.1</strong>', '<strong>Figure 17.1.1</strong>',
     '17.1 Figure 16.1.1'),
    (ROOT / 'part-4-training-adapting/module-17-alignment-rlhf-dpo/section-17.4.html',
     '<strong>Figure 16.4.1a</strong>', '<strong>Figure 17.4.1a</strong>',
     '17.4 Figure 16.4.1a'),
    (ROOT / 'part-4-training-adapting/module-17-alignment-rlhf-dpo/section-17.4.html',
     '<strong>Figure 16.4.1</strong>', '<strong>Figure 17.4.1</strong>',
     '17.4 Figure 16.4.1'),
    (ROOT / 'part-5-retrieval-conversation/module-19-rag/section-19.9.html',
     '<strong>Table 18.9.1:</strong>', '<strong>Table 19.9.1:</strong>',
     '19.9 Table 18.9.1'),
]
for p, old, new, lbl in caption_fixes:
    patch(p, old, new, lbl)

# ============================================================
# HIGH: Section 23.1 leaked subsection title in lab boilerplate
# ============================================================
sec231 = ROOT / 'part-6-agentic-ai/module-23-multi-agent-systems/section-23.1.html'
if sec231.exists():
    s = sec231.read_text(encoding='utf-8')
    # "for 2. Framework Selection Guide" -> "for the Framework Selection Guide lab"
    fixes = [
        ('for 2. Framework Selection Guide',
         'for the Framework Selection Guide lab'),
        ('demonstrating 2. Framework Selection Guide',
         'demonstrating the Framework Selection Guide lab'),
        ('Complete solution for 2. Framework Selection Guide',
         'Complete solution for the Framework Selection Guide lab'),
    ]
    n = 0
    for old, new in fixes:
        c = s.count(old)
        if c:
            s = s.replace(old, new)
            n += c
    if n:
        sec231.write_text(s, encoding='utf-8')
        total += n
        print(f'  [23.1 lab boilerplate "2." prefix x{n}]')

# ============================================================
# CRITICAL: 3 lab "# TODO: Full implementation here" boilerplate
# (might have regressed since v773; verify and fix)
# ============================================================
todo_files = [
    ROOT / 'part-6-agentic-ai/module-22-tool-use-protocols/section-22.2.html',
    ROOT / 'part-6-agentic-ai/module-23-multi-agent-systems/section-23.1.html',
    ROOT / 'part-6-agentic-ai/module-25-agent-safety-production/section-25.5.html',
]
todo_pat = re.compile(
    r'<span[^>]*>#</span>\s*<span[^>]*>\s*'
    r'(TODO:\s*(?:Implement setup code here|Full implementation here))'
    r'\s*</span>')
for fp in todo_files:
    if not fp.exists():
        continue
    s = fp.read_text(encoding='utf-8')
    new, n = todo_pat.subn(
        '<span class="c1"># implementation goes here</span>', s)
    if n:
        fp.write_text(new, encoding='utf-8')
        total += n
        print(f'  [{fp.name} TODO boilerplate x{n}]')

print(f'\nTotal next-100 fixes: {total}')
