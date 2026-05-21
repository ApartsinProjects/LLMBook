"""Prepend 'Warning:' canonical type prefix to misconception callout titles.

The 15 misconception callouts added in cycle 5.3 use class="warning" (correct)
but title starts with "Common Misconception:" instead of "Warning:". The
audit requires the canonical type prefix.

Fix: rewrite "<div class="callout-title">Common Misconception:" to
"<div class="callout-title">Warning: Common Misconception:" - keeps the
descriptive label, satisfies the prefix rule.

Also fixes 2 MATH_RENDERING bugs from $ in SVG text (currency context).
"""
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent

# Files with "Common Misconception:" callouts
TITLE_RE = re.compile(
    r'<div class="callout-title">Common Misconception:',
)


def fix_titles():
    fixed_files = []
    for part_dir in ROOT.glob('part-*'):
        if not part_dir.is_dir():
            continue
        for f in part_dir.rglob('section-*.html'):
            try:
                text = f.read_text(encoding='utf-8')
            except Exception:
                continue
            new_text, n = TITLE_RE.subn(
                '<div class="callout-title">Warning: Common Misconception:',
                text,
            )
            if n:
                f.write_text(new_text, encoding='utf-8')
                fixed_files.append((str(f.relative_to(ROOT)), n))
    return fixed_files


def fix_math_dollar():
    """Fix $ in SVG text (currency, breaks math detector)."""
    fixed_files = []
    targets = [
        ('part-6-agentic-ai/module-30-tools-of-the-trade/section-30.3.html',
         'SWE-Lancer ($-valued)', 'SWE-Lancer (USD-valued)'),
        ('part-9-llm-evaluation-observability/module-44-online-eval-observability/section-44.3.html',
         '$ per request', 'USD per request'),
    ]
    for relpath, old, new in targets:
        f = ROOT / relpath
        if f.exists():
            text = f.read_text(encoding='utf-8')
            if old in text:
                f.write_text(text.replace(old, new), encoding='utf-8')
                fixed_files.append(relpath)
    return fixed_files


def main():
    print("Fixing 'Common Misconception' callout titles...")
    title_fixes = fix_titles()
    for path, n in title_fixes:
        print(f"  {path}: {n}")
    print(f"\nTotal title fixes: {len(title_fixes)} files")

    print("\nFixing $ in SVG text (currency)...")
    math_fixes = fix_math_dollar()
    for p in math_fixes:
        print(f"  {p}")
    print(f"\nTotal math fixes: {len(math_fixes)} files")


if __name__ == '__main__':
    main()
