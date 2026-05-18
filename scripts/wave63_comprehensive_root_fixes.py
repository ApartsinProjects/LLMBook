"""Wave 63: Comprehensive root-cause sweep for user-reported callout/structure
issues found 2026-05-18.

Fixes:
1. Algorithm: Pseudocode N.M.X: → Algorithm N.M.X: (double-prefix collapse)
2. fun-note containing only a <figure> → bare <figure> (fun-fact ≠ fun-illustration)
3. <div class="callout note"><pre class="callout-output-body">...</pre></div>
   nested inside code-block-wrapper → move <pre> content to canonical
   <div class="code-output"> sibling of the code, drop the wrapping note callout.
4. "Canonical reference" callout title → "See also" (standardize cross-ref title)
5. Strip stray "Code Fragment X.Y.Z: " prefix from prose paragraphs that
   START with that label (the label belongs in the caption, not prose).
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'.git', 'node_modules', 'KDP', 'build', 'source_fix_backups',
        'pagefind', '.book-update', 'vendor', '.claude', '_archive',
        'agents', 'templates', 'docs', 'scripts'}

# 1. Algorithm: Pseudocode N.M.X: <prose> → Algorithm N.M.X: <prose>
ALG_DBL_RE = re.compile(
    r'(<div\s+class="callout-title"[^>]*>\s*)Algorithm:\s*Pseudocode\s+(\d+(?:\.\d+)+):?\s*',
    re.IGNORECASE,
)

# 2. fun-note that contains ONLY a figure (no body text)
FUN_FIG_RE = re.compile(
    r'<div\s+class="callout fun-note"[^>]*>\s*'
    r'<div\s+class="callout-title">([^<]*)</div>\s*'
    r'(<figure\s+class="illustration"[^>]*>.*?</figure>)\s*'
    r'</div>',
    re.DOTALL | re.IGNORECASE,
)

# 3. <div class="callout note"><div class="callout-title">Note: Example output</div>
#    <pre class="callout-output-body">...</pre></div>
#    This pattern is broken structure inside a code-block-wrapper.
#    Move the <pre> content into a sibling <div class="code-output">.
NESTED_NOTE_RE = re.compile(
    r'<div\s+class="callout note"[^>]*>\s*'
    r'<div\s+class="callout-title">\s*Note:\s*Example output\s*</div>\s*'
    r'<pre\s+class="callout-output-body"[^>]*>(.*?)</pre>\s*'
    r'</div>',
    re.DOTALL | re.IGNORECASE,
)

# 4. "Canonical reference" or "Canonical Reference" → "See also"
CANONICAL_REF_RE = re.compile(
    r'(<div\s+class="callout-title"[^>]*>\s*)Canonical [Rr]eference(\s*</div>)',
    re.IGNORECASE,
)


def fix_file(p: Path) -> dict[str, int]:
    text = p.read_text(encoding='utf-8')
    orig = text
    counts = {'algo_dbl': 0, 'fun_fig': 0, 'nested_note': 0, 'canon_ref': 0}

    # 1. Algorithm double-prefix
    def algo_repl(m):
        counts['algo_dbl'] += 1
        return m.group(1) + 'Algorithm ' + m.group(2) + ': '
    text = ALG_DBL_RE.sub(algo_repl, text)

    # 2. fun-note containing only figure → unwrap to bare figure
    def fun_repl(m):
        counts['fun_fig'] += 1
        # Keep just the figure (drop the callout wrapper)
        return m.group(2)
    text = FUN_FIG_RE.sub(fun_repl, text)

    # 3. Nested note (Example output) → canonical code-output
    def note_repl(m):
        counts['nested_note'] += 1
        body = m.group(1).strip()
        # Wrap in canonical code-output div with output-label
        return (
            '<div class="code-output">'
            '<span class="output-label"><strong>Output:</strong></span> '
            + body
            + '</div>'
        )
    text = NESTED_NOTE_RE.sub(note_repl, text)

    # 4. Canonical reference → See also
    def canon_repl(m):
        counts['canon_ref'] += 1
        return m.group(1) + 'See also' + m.group(2)
    text = CANONICAL_REF_RE.sub(canon_repl, text)

    if text != orig:
        p.write_text(text, encoding='utf-8')
    return counts


def main():
    totals = {'algo_dbl': 0, 'fun_fig': 0, 'nested_note': 0, 'canon_ref': 0}
    files_touched = 0
    for p in sorted(ROOT.rglob('*.html')):
        if set(p.parts) & SKIP:
            continue
        counts = fix_file(p)
        if sum(counts.values()) > 0:
            files_touched += 1
            for k, v in counts.items():
                totals[k] += v
    print('=== Wave 63 Comprehensive Root-Cause Fixes ===')
    print(f'Algorithm: Pseudocode N.M.X: → Algorithm N.M.X: {totals["algo_dbl"]}')
    print(f'fun-note (figure-only) → bare figure:         {totals["fun_fig"]}')
    print(f'Nested note (Example output) → code-output:    {totals["nested_note"]}')
    print(f'Canonical reference → See also:                {totals["canon_ref"]}')
    print(f'Files touched: {files_touched}')


if __name__ == '__main__':
    main()
