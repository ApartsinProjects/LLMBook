"""Probe singleton callout markup variants across the book."""
from pathlib import Path
import re

ROOT = Path('E:/Projects/BookBlogsHome/LLMBook')
SKIP_HINTS = ('/tools-of-the-trade/', '/appendices/', '/kdp/', '/build/',
              'module-05-tools', 'module-14-tools', 'module-19-tools',
              'module-30-tools', 'module-36-retrieval-tools', 'module-41-conv-ai',
              'module-45-tools', 'module-51-tools', 'module-56-responsible-ai',
              'module-61-scale', 'module-71-tools', 'module-79-tools')


def norm(p: Path) -> str:
    return str(p).lower().replace('\\', '/')


def should_skip(p: Path) -> bool:
    s = norm(p)
    return any(x in s for x in SKIP_HINTS)


files = [fp for fp in ROOT.rglob('section-*.html')
         if not should_skip(fp) and fp.is_file()]
print(f'Section files: {len(files)}')

# Probe exercises markup
section_excs = 0
h2_excs = 0
both = 0
none = 0
for fp in files:
    try:
        h = fp.read_text(encoding='utf-8', errors='ignore')
    except Exception:
        continue
    a = bool(re.search(r'<section\s+class="exercises"', h, re.IGNORECASE))
    b = bool(re.search(r'<h2\s+id="exercises"', h, re.IGNORECASE))
    if a and b:
        both += 1
    elif a:
        section_excs += 1
    elif b:
        h2_excs += 1
    else:
        none += 1
print(f'section.exercises only: {section_excs}')
print(f'h2#exercises only: {h2_excs}')
print(f'both: {both}')
print(f'none: {none}')

# Probe whats-next markup
wn_callout = 0
wn_div = 0
wn_both = 0
for fp in files:
    try:
        h = fp.read_text(encoding='utf-8', errors='ignore')
    except Exception:
        continue
    a = bool(re.search(r'<div\s+class="callout\s+whats-next"', h, re.IGNORECASE))
    b = bool(re.search(r'<div\s+class="whats-next"', h, re.IGNORECASE))
    if a and b:
        wn_both += 1
    elif a:
        wn_callout += 1
    elif b:
        wn_div += 1
print(f'whats-next callout: {wn_callout}, div: {wn_div}, both: {wn_both}')
