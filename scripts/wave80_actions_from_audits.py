"""Wave 80: Convert ALL outstanding audit findings into actionable fixes.

Sources:
  - docs/content-audit/cycle_snapshots/cycle_54.json (latest audit)
  - docs/content-audit/MASTER_TODO_CONSOLIDATED.md (consolidated TODO)
  - docs/content-audit/REPEATED_CONTENT_AUDIT.md (179 dup blocks)
  - docs/content-audit/CRITICAL_READER_AUDIT.md (lame code/diagrams)

This wave is the "fix everything mechanical" pass:
  1. Remove the 4 "lame boilerplate" exact-text duplicate code-captions
     ("Code example", "Install the required packages for this lab.")
  2. Standardize all `<a href="../../toc.html">` to use the consistent
     `<span class="toc-icon">` HTML entity (some pages use the literal ☰
     character, others the `&#9776;` HTML entity).
  3. Drop "Title:" prefix duplication in callout titles where the type
     prefix matches the type word (e.g., "Warning: Warning content" — should be just "Warning: content")
  4. Convert remaining MISSING_OUTPUT print() calls to either add empty
     <div class="code-output">(output truncated)</div> stubs OR remove
     the print() if it's just a "look I'm running" gesture (skipped here;
     authoring work).

For complex per-file items (CALLOUT_ORDER duplicate-singletons, OVERLAP,
8 indent-bug fragments, FIGURE_SEQUENCE renumbering), leaves them to
authoring agents (dispatched in parallel).
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'.git', 'node_modules', 'KDP', 'build', 'source_fix_backups',
        'pagefind', '.book-update', 'vendor', '.claude', '_archive',
        'agents', 'templates', 'docs', 'scripts'}

# 1. Lame boilerplate caption removal
LAME_CAPTIONS = [
    'Code example',
    'Install the required packages for this lab.',
    'Run this code in your environment.',
    'See the implementation above.',
    'Example output',
]
# Match: <div class="code-caption"><strong>Code Fragment X.Y.Z:</strong> LAME_TEXT</div>
LAME_CAP_RE = re.compile(
    r'<div\s+class="code-caption">\s*<strong>\s*Code Fragment\s+[\d.]+\s*:?\s*</strong>\s*([^<]+)\s*</div>',
    re.IGNORECASE,
)


def is_lame_caption(text: str) -> bool:
    text = text.strip().rstrip('.').lower()
    for lame in LAME_CAPTIONS:
        if text == lame.strip().rstrip('.').lower():
            return True
    return False


# 2. Toc-icon standardization (use HTML entity, not literal character)
TOC_ICON_LITERAL = re.compile(r'<span class="toc-icon">☰</span>')


# 3. Double-prefix in titles (already handled by wave 57; this is a residual catch)
# e.g., "Warning: Warning about X" → "Warning: X"
TYPE_WORDS = ['Warning', 'Note', 'Tip', 'Caution', 'Important']
DOUBLE_PREFIX_RE = re.compile(
    rf'<div\s+class="callout-title"[^>]*>\s*({"|".join(TYPE_WORDS)}):\s*\1\s+',
    re.IGNORECASE,
)


def fix_file(p: Path) -> dict[str, int]:
    text = p.read_text(encoding='utf-8')
    orig = text
    counts = {'lame_caption': 0, 'toc_icon': 0, 'double_prefix': 0}

    # 1. Lame caption removal (drops the entire <div class="code-caption">...)
    # Actually: KEEP the caption but rewrite to placeholder marker so the audit
    # still surfaces it for authoring. Less risky than dropping outright.
    def lame_repl(m):
        cap_text = m.group(1).strip()
        if is_lame_caption(cap_text):
            counts['lame_caption'] += 1
            # Keep but mark as TODO for author
            return m.group(0).replace(cap_text, f'[TODO caption] {cap_text}')
        return m.group(0)
    text = LAME_CAP_RE.sub(lame_repl, text)

    # 2. Toc-icon: normalize ☰ → &#9776; (HTML entity is more robust)
    new, n = TOC_ICON_LITERAL.subn('<span class="toc-icon">&#9776;</span>', text)
    if n:
        counts['toc_icon'] = n
        text = new

    # 3. Double-prefix
    def dbl_repl(m):
        counts['double_prefix'] += 1
        return m.group(0).replace(f'{m.group(1)}: {m.group(1)} ', f'{m.group(1)}: ')
    text = DOUBLE_PREFIX_RE.sub(dbl_repl, text)

    if text != orig:
        p.write_text(text, encoding='utf-8')
    return counts


def main():
    totals = {'lame_caption': 0, 'toc_icon': 0, 'double_prefix': 0}
    files = 0
    for p in sorted(ROOT.rglob('*.html')):
        if set(p.parts) & SKIP:
            continue
        c = fix_file(p)
        if sum(c.values()) > 0:
            files += 1
            for k, v in c.items():
                totals[k] += v
    print(f'Lame captions flagged [TODO]:   {totals["lame_caption"]}')
    print(f'Toc-icon ☰ → &#9776;:           {totals["toc_icon"]}')
    print(f'Double-prefix removed:          {totals["double_prefix"]}')
    print(f'Files touched: {files}')


if __name__ == '__main__':
    main()
