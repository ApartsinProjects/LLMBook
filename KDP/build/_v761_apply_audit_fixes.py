"""v761: Apply targeted fixes from the v760 audit report.

Fixes:
  H1. Visible "Wave 15" prose -> drop the parenthetical entirely.
  H2. "Module 28 (Observability sections)" artifact -> "Chapter 28".
  C2. module-33 next-chapter links pointing to root index.html -> proper
      part-9 chapter-30 path.
  C4. appendix-ai-freshness-2026 meta description "seventh edition"
      -> "twelfth edition".
  H3. "Code Fragment X.Y.N: TODO: ..." caption with TODO leaking ->
      drop the "TODO:" prefix in the caption only (code stays).
  C3. fm-who-should-read meta description "FM.2: Who Should Read"
      -> "FM.4 Who Should Read".

Plus a global FM.0* sweep: every "FM.0", "FM.0a", ..., "FM.0d" reference
points at material now living in Appendix AD/AE/AF/AH (Master Reference
Tables, Production Patterns, Pedagogy Kit, Conceptual Map). Map:
  FM.0  -> Appendix AH (Conceptual Map)
  FM.0a -> Appendix AD (Master Reference Tables)
  FM.0b -> Appendix AE (Production Patterns)
  FM.0c -> Appendix AE (Production Patterns)  (was 0b/0c per draft)
  FM.0d -> Appendix AF (Pedagogy Kit)

Idempotent.
"""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

SKIP_DIRS = ('KDP/build/source_fix_backups', 'pagefind', 'node_modules',
             'temp_epub', '.git', 'venv')


def should_skip(p: Path) -> bool:
    sp = str(p).replace('\\', '/')
    return any(s in sp for s in SKIP_DIRS)


# (regex_pattern, replacement, description)
FIXES = [
    # H1. "Wave 15 fixed the broken example" parentheticals -> drop them
    # Drop the parenthetical " (Wave 15 ... )" wherever it appears in prose.
    (re.compile(r'\s*\(Wave\s+\d+[^)]*\)'), '',
     'drop "(Wave NN ...)" parentheticals'),

    # H2. "Module 28 (Observability sections)" artifact -> "Chapter 28"
    (re.compile(r'Module 28\s*\(Observability sections\)'),
     'Chapter 28',
     'Module 28 (Observability sections) -> Chapter 28'),

    # C4. seventh edition -> twelfth edition (in meta description)
    (re.compile(r'\bseventh edition\b', re.IGNORECASE),
     'twelfth edition',
     'seventh edition -> twelfth edition'),

    # C5. FM.2: Who Should Read -> FM.4 Who Should Read (description meta)
    # We avoid touching real prose by anchoring to the description tag
    (re.compile(
        r'(<meta name="description"[^>]*content="[^"]*?)FM\.2:\s+Who Should Read'),
     r'\1FM.4 Who Should Read',
     'meta description FM.2 -> FM.4'),

    # H3. "Code Fragment X.Y.Z: TODO:" -> "Code Fragment X.Y.Z:"
    (re.compile(r'(<strong>Code Fragment\s+[\d.]+:</strong>)\s*TODO:\s*'),
     r'\1 ',
     'drop TODO: prefix in code captions'),

    # FM.0* references -> Appendix AD/AE/AF/AH
    (re.compile(r'\bFM\.0d\b'), 'Appendix AF', 'FM.0d -> Appendix AF'),
    (re.compile(r'\bFM\.0c\b'), 'Appendix AE', 'FM.0c -> Appendix AE'),
    (re.compile(r'\bFM\.0b\b'), 'Appendix AE', 'FM.0b -> Appendix AE'),
    (re.compile(r'\bFM\.0a\b'), 'Appendix AD', 'FM.0a -> Appendix AD'),
    # Don't touch "FM.01", "FM.0.x" etc; require word boundary AFTER 0.
    (re.compile(r'\bFM\.0\b(?!\.)(?!\d)'), 'Appendix AH',
     'FM.0 -> Appendix AH'),
]

# C2. module-33 broken next-chapter links pointing to root index.html
# These are specific files; do an exact targeted replace.
TARGETED = [
    (
        ROOT / 'part-10-frontiers' / 'module-33-emerging-architectures'
             / 'section-33.9.html',
        '<a href="../../index.html">Module 30: Safety, Ethics &amp; Regulation</a>',
        '<a href="../../part-9-safety-strategy/module-30-safety-ethics-regulation/index.html">Chapter 30: Safety, Ethics &amp; Regulation</a>',
    ),
    (
        ROOT / 'part-10-frontiers' / 'module-33-emerging-architectures'
             / 'section-33.10.html',
        '<a href="../../index.html">Module 30: Safety, Ethics &amp; Regulation</a>',
        '<a href="../../part-9-safety-strategy/module-30-safety-ethics-regulation/index.html">Chapter 30: Safety, Ethics &amp; Regulation</a>',
    ),
]


def main() -> int:
    counts = {desc: 0 for _, _, desc in FIXES}
    n_files = 0
    for p in ROOT.rglob('*.html'):
        if should_skip(p):
            continue
        try:
            src = p.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            continue
        new = src
        any_change = False
        for pat, rep, desc in FIXES:
            new2, c = pat.subn(rep, new)
            if c:
                counts[desc] += c
                any_change = True
                new = new2
        if any_change:
            n_files += 1
            p.write_text(new, encoding='utf-8')
    print(f'Files changed by global rules: {n_files}')
    for desc, c in counts.items():
        print(f'  {c:>4}  {desc}')

    # Targeted fixes
    print('\nTargeted fixes:')
    for path, old, new_v in TARGETED:
        if not path.exists():
            print(f'  SKIP missing {path}')
            continue
        s = path.read_text(encoding='utf-8')
        if old in s:
            path.write_text(s.replace(old, new_v), encoding='utf-8')
            print(f'  fixed {path.relative_to(ROOT)}')
        else:
            print(f'  no match in {path.relative_to(ROOT)} (already fixed?)')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
