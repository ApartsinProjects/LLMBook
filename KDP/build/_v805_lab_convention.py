"""v805: Standardize 3 minor lab convention deviations from audit #49.

Audit findings:
  D1. <section class="lab"> → should be <div class="lab">
      part-9-safety-strategy/module-30-safety-ethics-regulation/section-30.1.html:806
  D2. Same
      part-9-safety-strategy/module-31-strategy-product-roi/section-31.3.html:534
  D3. <h2>Lab</h2> bare (no wrapper, no descriptor)
      part-1-foundations/module-02-tokenization-subword-models/section-2.3.html:523

Fixes:
  D1, D2: change <section class="lab"> → <div class="lab">
          (and matching </section> → </div>)
  D3: wrap <h2>Lab</h2> + immediate-following content in
      <div class="lab"> until next h2/h3 boundary
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
n_total = 0


# ---------- D1, D2: <section class="lab"> → <div class="lab"> ----------
for rel in [
    'part-9-safety-strategy/module-30-safety-ethics-regulation/section-30.1.html',
    'part-9-safety-strategy/module-31-strategy-product-roi/section-31.3.html',
]:
    fp = ROOT / rel
    if not fp.exists():
        print(f'  MISSING: {rel}')
        continue
    s = fp.read_text(encoding='utf-8')

    # Find each <section class="lab" ...> ... </section> and rewrite to div
    pattern = re.compile(
        r'(<section\b[^>]*\bclass="(?:[^"]*\b)?lab\b[^"]*"[^>]*>)(.*?)(</section>)',
        re.DOTALL
    )

    def replace(m):
        open_tag = m.group(1)
        body = m.group(2)
        # Replace 'section' with 'div' in the open tag
        new_open = re.sub(r'^<section\b', '<div', open_tag)
        return new_open + body + '</div>'

    new_s, n = pattern.subn(replace, s)
    if new_s != s:
        fp.write_text(new_s, encoding='utf-8')
        n_total += n
        print(f'  D1/D2: converted {n} <section class="lab"> in {rel.split("/")[-1]}')


# ---------- D3: unwrapped <h2>Lab: ...</h2> in section-2.3.html ----------
# The actual content is <h2>Lab: Comparing Tokenizers Head-to-Head</h2>
# (with descriptor) but lacks the <div class="lab"> wrapper that other
# labs use. Wrap from the h2 through to next h2/h3 boundary.
fp = ROOT / 'part-1-foundations/module-02-tokenization-subword-models/section-2.3.html'
if fp.exists():
    s = fp.read_text(encoding='utf-8')
    pattern = re.compile(
        r'(<h2>Lab:[^<]*</h2>)((?:(?!<h2|<h3|</main|<footer|<nav|<section).)*)',
        re.DOTALL
    )
    def wrap_d3(m):
        h2_tag = m.group(1)
        body = m.group(2)
        return f'<div class="lab">{h2_tag}{body}</div>'
    new_s, n = pattern.subn(wrap_d3, s, count=1)
    if new_s != s:
        fp.write_text(new_s, encoding='utf-8')
        n_total += n
        print(f'  D3: wrapped <h2>Lab: ...</h2> with <div class="lab"> in section-2.3.html')

print(f'\nTotal lab standardization edits: {n_total}')
