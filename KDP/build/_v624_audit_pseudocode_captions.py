"""Audit Pseudocode N.N.N callout captions vs the code that follows.

Heuristic: if the caption mentions Python-specific things (@decorators, SDK,
import statements, library names) but the code immediately below is lang-text
(genuine pseudocode), the caption is probably misplaced — it belongs to a
different code block, likely a real Python listing in the same section.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

PSEUDO_HINTS = ['@server', '@app', '@router', 'sdk', ' class ', 'import ',
                'install', 'pip ', ' def ', 'async def', 'fastapi', 'flask',
                'numpy', 'pytorch', 'transformers', 'huggingface', 'langchain']

matches = []
for p in sorted(ROOT.glob('part-*/module-*/section-*.html')):
    text = p.read_text(encoding='utf-8', errors='replace')
    for m in re.finditer(
        r'<div class="callout-title">Pseudocode\s+(\d+\.\d+\.\d+)\s*:?\s*([^<]*)</div>',
        text,
    ):
        label = m.group(1)
        caption = m.group(2).strip()
        code_search = text[m.end():m.end() + 800]
        code_m = re.search(
            r'<pre><code class="[^"]*lang-(\w+)[^"]*"[^>]*>(.{0,400})',
            code_search,
            re.DOTALL,
        )
        if code_m:
            lang = code_m.group(1)
            code_preview = re.sub(r'<[^>]+>', '', code_m.group(2))[:160]
        else:
            lang = '???'
            code_preview = '???'
        matches.append({
            'file': str(p.relative_to(ROOT)).replace('\\', '/'),
            'label': label,
            'caption': caption,
            'lang': lang,
            'code_preview': code_preview.strip(),
        })

print(f'Found {len(matches)} Pseudocode callouts\n')

suspicious = 0
for it in matches:
    cap_l = it['caption'].lower()
    looks_python = any(kw in cap_l for kw in PSEUDO_HINTS)
    if it['lang'] == 'text' and looks_python:
        suspicious += 1
        print(f"SUSPICIOUS: {it['file']}")
        print(f"  Label: Pseudocode {it['label']}")
        print(f"  Caption: {it['caption'][:120]}")
        print(f"  Code (lang={it['lang']}): {it['code_preview'][:120]}")
        print()
print(f'Total suspicious: {suspicious} / {len(matches)}')
