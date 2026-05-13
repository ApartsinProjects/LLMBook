"""Audit Problem-Solution Key (front-matter/section-fm.8.html):
- Every <a href> target is reachable
- Every "X.Y Title" display text matches the URL's section number
- Report tools that link to wrong appendix paths
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
PSK = ROOT / 'front-matter' / 'section-fm.8.html'

LINK_RE = re.compile(
    r'<a\s+[^>]*href="([^"]+)"[^>]*>([^<]+)</a>',
    re.IGNORECASE)


def main() -> int:
    text = PSK.read_text(encoding='utf-8')
    base = PSK.parent.resolve()
    broken: list[str] = []
    mismatched: list[tuple[str, str, str]] = []  # (url, display, expected)
    tool_appendix_mismatches: list[tuple[str, str]] = []
    total = 0

    for m in LINK_RE.finditer(text):
        url = m.group(1)
        disp = m.group(2).strip()
        if url.startswith('#') or url.startswith('http') or url.startswith('mailto:'):
            continue
        total += 1
        target = (base / url).resolve()
        if not target.exists():
            broken.append(f'{url}  ({disp})')
            continue
        # Display-text check for "N.M ..." vs URL section-X.Y
        sm = re.search(r'section-(\d+)\.(\d+)(?:\.(\d+))?\.html', url)
        if sm:
            url_ch, url_sec = sm.group(1), sm.group(2)
            dm = re.match(r'^(\d+)\.(\d+)', disp)
            if dm:
                disp_ch, disp_sec = dm.group(1), dm.group(2)
                if disp_ch != url_ch or disp_sec != url_sec:
                    mismatched.append((url, disp, f'{url_ch}.{url_sec}'))
        # Tools column: appendix link text doesn't match appendix letter
        am = re.search(r'appendix-([a-z]+)-', url)
        if am:
            letter = am.group(1)
            # Display text vs canonical name expected
            disp_low = disp.lower()
            tool_keywords = {
                'k': ['huggingface', 'hugging face', 'transformers', 'datasets', 'dspy'],
                'l': ['langchain', 'langgraph', 'crewai', 'semantic kernel'],
                'r': ['w&b', 'mlflow', 'weights'],
                's': ['vllm', 'tgi', 'sglang', 'inference serving'],
                't': ['pyspark', 'ray', 'distributed'],
                'i': ['prompt template'],
                'j': ['dataset', 'benchmark'],
                'g': ['hardware', 'gpu'],
                'h': ['model card'],
                'd': ['env', 'environment'],
            }
            keys = tool_keywords.get(letter, [])
            if keys:
                if not any(k in disp_low for k in keys):
                    tool_appendix_mismatches.append((url, disp))

    print(f'Total internal links: {total}')
    print(f'Broken target files : {len(broken)}')
    for b in broken[:30]:
        print(f'  ! {b}')
    print(f'Display vs URL mismatch: {len(mismatched)}')
    for u, d, e in mismatched[:30]:
        print(f'  ! {d}  ->  URL says section {e}  ({u})')
    print(f'Tool col label vs appendix link mismatches: {len(tool_appendix_mismatches)}')
    for u, d in tool_appendix_mismatches[:30]:
        print(f'  ? {d:30s}  ->  {u}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
