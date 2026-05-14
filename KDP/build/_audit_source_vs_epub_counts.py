"""Compare element counts in source HTML vs built EPUB to verify
nothing is silently dropped by the build pipeline.

Counts <p>, <h1-h6>, <table>, <tr>, <td>, <pre>, <code>, <img>,
<li>, <figure>, <details>, callouts, and total words. Reports any
significant discrepancies.
"""
import os
import re
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EPUB = ROOT / 'KDP/output/building-conversational-ai-llms-agents.epub'

ELEMENTS = ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
            'table', 'tr', 'td', 'th', 'pre', 'code',
            'img', 'li', 'ul', 'ol', 'figure', 'figcaption',
            'details', 'summary', 'blockquote',
            'sub', 'sup', 'math', 'a']


def count_in_html(html: str) -> dict:
    counts = {}
    for tag in ELEMENTS:
        # <tag ...> or <tag> but not <tag/> self-closed
        n = len(re.findall(rf'<{tag}(?:\s[^>]*)?>', html))
        counts[tag] = n
    # Self-closed img
    counts['img'] += len(re.findall(r'<img(?:\s[^>]*)?/>', html))
    # Callout types
    counts['callout'] = len(re.findall(r'<div class="[^"]*\bcallout\b', html))
    # Plain text word count (rough)
    text = re.sub(r'<[^>]+>', ' ', html)
    text = re.sub(r'&[#a-z0-9]+;', ' ', text)
    counts['words'] = len(text.split())
    return counts


def aggregate_dirs(dirs):
    total = {e: 0 for e in ELEMENTS + ['callout', 'words']}
    n_files = 0
    for d in dirs:
        for p in d.rglob('*.html'):
            sp = str(p).replace('\\', '/')
            if any(s in sp for s in ['node_modules', 'temp_epub', 'output',
                                      'backup', 'agents/', 'templates/',
                                      'KDP/html2pub/', 'KDP/build/']):
                continue
            try:
                c = p.read_text(encoding='utf-8')
            except UnicodeDecodeError:
                continue
            counts = count_in_html(c)
            for k, v in counts.items():
                total[k] = total.get(k, 0) + v
            n_files += 1
    return total, n_files


def aggregate_epub() -> tuple[dict, int]:
    total = {e: 0 for e in ELEMENTS + ['callout', 'words']}
    n_files = 0
    with zipfile.ZipFile(EPUB) as z:
        for name in z.namelist():
            if not name.endswith('.xhtml'):
                continue
            c = z.read(name).decode('utf-8')
            counts = count_in_html(c)
            for k, v in counts.items():
                total[k] = total.get(k, 0) + v
            n_files += 1
    return total, n_files


print('Counting source HTML...')
src_dirs = [ROOT / 'part-1-foundations', ROOT / 'part-2-understanding-llms',
            ROOT / 'part-3-working-with-llms', ROOT / 'part-4-training-adapting',
            ROOT / 'part-5-retrieval-conversation', ROOT / 'part-6-agentic-ai',
            ROOT / 'part-7-multimodal-applications', ROOT / 'part-8-evaluation-production',
            ROOT / 'part-9-safety-strategy', ROOT / 'part-10-frontiers',
            ROOT / 'part-11-idea-to-product', ROOT / 'appendices',
            ROOT / 'front-matter', ROOT / 'capstone']
src_counts, src_files = aggregate_dirs(src_dirs)
print(f'  Source: {src_files} HTML files')

print('Counting EPUB...')
epub_counts, epub_files = aggregate_epub()
print(f'  EPUB: {epub_files} XHTML files')

# v802 conversion: inline math <math> is converted to <span class="inline-math">
# with <sub>/<sup>. So <math> count drops, <sub>/<sup>/<span> increases.
# Account for this in the comparison.
import zipfile
with zipfile.ZipFile(EPUB) as z:
    inline_math_html = 0
    for name in z.namelist():
        if name.endswith('.xhtml'):
            inline_math_html += z.read(name).decode('utf-8').count('class="inline-math"')

print()
print('Element                     Source        EPUB        Diff      Status')
print('-' * 75)
for tag in ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
            'table', 'tr', 'td', 'th', 'pre', 'code',
            'img', 'li', 'ul', 'ol', 'figure', 'figcaption',
            'details', 'summary', 'blockquote',
            'sub', 'sup', 'math', 'a',
            'callout']:
    s = src_counts.get(tag, 0)
    e = epub_counts.get(tag, 0)
    d = e - s
    if tag == 'math':
        # Adjust: v802 conversion replaced 661 inline math with HTML
        # If e + 661 ≈ s, math is preserved
        expected_loss = inline_math_html
        adjusted_diff = (s - e) - expected_loss
        status = 'OK' if abs(adjusted_diff) < 20 else 'CHECK'
        status += f' (v802 converted {inline_math_html})'
    elif tag in ('sub', 'sup'):
        status = 'OK (v802 expected)'
    elif d < -10:
        status = 'LOSS'
    elif d > 50:
        status = 'GAINED (build adds wrappers)'
    elif abs(d) < 10:
        status = 'OK'
    else:
        status = '~ok'
    print(f'  {tag:24}  {s:>8}  {e:>8}    {d:>+6}    {status}')

print()
print(f'Total source words: {src_counts["words"]:,}')
print(f'Total EPUB words:   {epub_counts["words"]:,}')
print(f'Word delta:         {epub_counts["words"] - src_counts["words"]:+,}')
