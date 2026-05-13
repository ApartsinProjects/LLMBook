"""8th edition Wave 23 / A.2: sharpen Part VIII chapter titles.

Ch 27 "Evaluation & Experiment Design" -> "LLM Evaluation & Quality Metrics"
Ch 28 "Production Engineering & Operations" -> "LLMOps & Deployment Engineering"

The senior-editor reviewer flagged that Part VIII over-segmented eval +
observability + production engineering across two chapters with
overlapping scope. The chapter titles already differed but lacked sharp
positioning. Renaming makes the boundary explicit: Ch 27 is *what to
measure* (evaluation, metrics, quality), Ch 28 is *how to operate*
(LLMOps, deployment, monitoring, rollback).

Idempotent. Touches every HTML file that references the old titles in
<title>, <h1>, chapter-label, data-pagefind-meta, prose, and TOC.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SKIP = ('node_modules', '.git/', 'pagefind/', 'KDP/build/', 'KDP/output/',
        'templates/', '_archive/', 'temp_epub/')

# Old -> new (use multiple variants because we have to catch HTML-entity
# escaped versions too)
RENAMES = [
    ('Evaluation &amp; Experiment Design', 'LLM Evaluation &amp; Quality Metrics'),
    ('Evaluation & Experiment Design', 'LLM Evaluation & Quality Metrics'),
    ('Production Engineering &amp; Operations', 'LLMOps &amp; Deployment Engineering'),
    ('Production Engineering & Operations', 'LLMOps & Deployment Engineering'),
]


def main() -> int:
    n_files = 0
    n_replacements = 0
    for p in sorted(ROOT.rglob('*.html')):
        sp = str(p).replace('\\', '/')
        if any(s in sp for s in SKIP):
            continue
        try:
            text = p.read_text(encoding='utf-8', errors='replace')
        except Exception:
            continue
        original = text
        local = 0
        for old, new in RENAMES:
            new_text = text.replace(old, new)
            if new_text != text:
                local += text.count(old)
                text = new_text
        if text != original:
            p.write_text(text, encoding='utf-8')
            n_files += 1
            n_replacements += local
            print(f'  renamed {local}x: {p.relative_to(ROOT)}')
    print(f'\nApplied {n_replacements} title replacements across {n_files} files.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
