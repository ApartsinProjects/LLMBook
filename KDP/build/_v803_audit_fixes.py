"""v803: Apply HTML fixes from the bookwide consistency audit.

Audits handled:
  F1-F4: 45 code blocks lacking `pygments-highlighted` class
  H1-H4: 4 empty callouts (title-only)
  B1:    1 prose-form "What Comes Next" violation
  A1:    1 typo "numerical-example" → "numeric-example"
  E1:    24 duplicate "Figure K.X.Y: Figure K.X.Y:" captions in appendix K

This script edits source HTML files in place. NO rebuild — run
publish.py separately after this.
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
n_fixed_total = 0


# ============================================================
# F1-F4: Add `pygments-highlighted` class to 45 unhighlighted code blocks
# ============================================================
print('=== F1-F4: Add pygments-highlighted to code blocks ===')

# Approach: find <code class="lang-X"> or <code class="language-X"> WITHOUT
# pygments-highlighted, and add the class. The pygments syntax-highlight
# hook in _html2epub_hooks.py runs at build time — we just need to mark
# them properly so the hook can process them.

n_f = 0
files_touched = set()
for html_path in ROOT.rglob('*.html'):
    sp = str(html_path).replace('\\', '/')
    if any(skip in sp for skip in ['node_modules', 'temp_epub', 'output', '.git',
                                    'pagefind', 'backup', 'agents/', 'templates/',
                                    'vendor/', 'KDP/']):
        continue
    try:
        s = html_path.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        continue
    orig = s

    # Pattern 1: class="lang-XXX" with NO pygments-highlighted
    def add_pyg(match):
        existing = match.group(1)
        lang = match.group(2)
        # Strip Prism-style language-none → lang-text
        if lang == 'language-none':
            return f'class="lang-text pygments-highlighted"'
        # Convert language-XXX → lang-XXX
        if lang.startswith('language-'):
            lang = 'lang-' + lang[len('language-'):]
        # Already has pygments?
        if 'pygments-highlighted' in existing:
            return match.group(0)
        return f'class="{lang} pygments-highlighted"'

    # Match code class="lang-X" or "language-X" without pygments-highlighted
    s = re.sub(
        r'class="((?:lang-|language-)[a-z-]+)"(?![^>]*pygments-highlighted)',
        lambda m: f'class="{m.group(1).replace("language-", "lang-")} pygments-highlighted"' if 'none' not in m.group(1) else 'class="lang-text pygments-highlighted"',
        s
    )

    # Pattern 2: <code> with no class attribute inside <pre>
    # (audit F4: 1 instance in 31.1.html)
    s = re.sub(
        r'<pre><code>(?!\s*<)',
        r'<pre><code class="lang-text pygments-highlighted">',
        s
    )

    if s != orig:
        html_path.write_text(s, encoding='utf-8')
        files_touched.add(html_path.name)
        n_f += 1
print(f'  Files touched: {n_f}; sample: {sorted(files_touched)[:5]}')
n_fixed_total += n_f


# ============================================================
# H1-H4: 4 empty callouts — REMOVE (insert content is author work)
# ============================================================
print('=== H1-H4: Remove 4 empty callouts ===')

empty_callouts = [
    ('part-2-understanding-llms/module-08-reasoning-test-time-compute/section-8.3.html',
     'Pseudocode 8.3.3'),
    ('part-9-safety-strategy/module-30-safety-ethics-regulation/section-30.1.html',
     'Algorithm: Multi-Layer Prompt Injection Detection'),
    ('part-9-safety-strategy/module-30-safety-ethics-regulation/section-30.11.html',
     'Key Insight'),
    ('part-9-safety-strategy/module-31-strategy-product-roi/section-31.7.html',
     'Key Insight'),
]
n_h = 0
for rel, title_text in empty_callouts:
    fp = ROOT / rel
    if not fp.exists():
        print(f'  MISSING: {rel}')
        continue
    s = fp.read_text(encoding='utf-8')
    # Find the empty callout: <div class="callout ..."><div class="callout-title">TITLE</div></div>
    pattern = re.compile(
        r'<div class="callout [^"]*">\s*<div class="callout-title">'
        + re.escape(title_text) + r'(?:[^<]*)</div>\s*</div>',
        re.DOTALL
    )
    new = pattern.sub('<!-- v803: removed empty callout -->', s)
    if new != s:
        fp.write_text(new, encoding='utf-8')
        n_h += 1
        print(f'  REMOVED empty "{title_text[:50]}" in {fp.name}')
    else:
        print(f'  NOT FOUND or no-op: "{title_text[:50]}" in {fp.name}')
n_fixed_total += n_h


# ============================================================
# B1: Wrap orphan "What Comes Next" in <div class="whats-next">
# ============================================================
print('=== B1: Wrap orphan What Comes Next ===')

b1_file = ROOT / 'part-1-foundations/module-00-ml-pytorch-foundations/section-0.4.html'
if b1_file.exists():
    s = b1_file.read_text(encoding='utf-8')
    # Find <h2>What Comes Next</h2> followed by <p>...</p> NOT already inside a whats-next div
    # Simple approach: find <h2>What Comes Next</h2> and look back/forward
    m = re.search(r'(<h2>What Comes Next</h2>\s*<p>.*?</p>)', s, re.DOTALL)
    if m and 'whats-next' not in s[max(0, m.start()-200):m.start()]:
        wrapped = '<div class="whats-next">' + m.group(1) + '</div>'
        s_new = s[:m.start()] + wrapped + s[m.end():]
        if s_new != s:
            b1_file.write_text(s_new, encoding='utf-8')
            n_fixed_total += 1
            print(f'  WRAPPED orphan What Comes Next in section-0.4.html')
        else:
            print(f'  no-op')
    else:
        print(f'  Pattern not found OR already wrapped')


# ============================================================
# A1: Typo numerical-example → numeric-example
# ============================================================
print('=== A1: Fix numerical-example typo ===')
a1_file = ROOT / 'part-1-foundations/module-02-tokenization-subword-models/section-2.2.html'
if a1_file.exists():
    s = a1_file.read_text(encoding='utf-8')
    s2 = s.replace('callout numerical-example', 'callout numeric-example')
    if s2 != s:
        a1_file.write_text(s2, encoding='utf-8')
        n_fixed_total += 1
        print(f'  FIXED in section-2.2.html')


# ============================================================
# E1: Duplicate "Figure K.X.Y: Figure K.X.Y: ..." captions
# ============================================================
print('=== E1: Fix duplicate Figure K.X.Y captions ===')
n_e = 0
for fp in (ROOT / 'appendices/appendix-k-huggingface-ecosystem').rglob('*.html'):
    s = fp.read_text(encoding='utf-8')
    # Pattern: <strong>Figure K.X.Y</strong>: Figure K.X.Y: …
    s2 = re.sub(
        r'(<strong>Figure ([A-Z]\.\d+(?:\.\d+)?)</strong>:)\s*Figure \2:\s*',
        r'\1 ',
        s
    )
    if s2 != s:
        fp.write_text(s2, encoding='utf-8')
        n_e += 1
        print(f'  FIXED duplicates in {fp.name}')
n_fixed_total += n_e

print()
print(f'TOTAL files/edits: {n_fixed_total}')
