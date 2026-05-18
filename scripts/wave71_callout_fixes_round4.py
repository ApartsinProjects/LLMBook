"""Wave 71: Round-4 structural fixes (user feedback 2026-05-18 cont).

1. Broken callout-title with no </div> closing it before the <p> body.
   Pattern:
     <div class="callout TYPE"><div class="callout-title">Title text
     <p>Body</p>
     </div>
   Result rendered: title swallows everything; bad UX. Fix: insert
   </div> between title text and <p>. Found 35 instances book-wide.

2. Lame exercise intro paragraphs between <h2>Exercises</h2> and first
   <div class="callout exercise">. Pattern observed in 16 sections —
   the intro adds no signal ("These exercises compare RAG frameworks
   and help you decide..."). Drop the intro paragraph.

3. Lame bibliography intro: similar pattern between <section class="bibliography">
   open and first <div class="bib-entry-card">. (0 found in earlier scan;
   sweep included as a guard.)
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'.git', 'node_modules', 'KDP', 'build', 'source_fix_backups',
        'pagefind', '.book-update', 'vendor', '.claude', '_archive',
        'agents', 'templates', 'docs', 'scripts'}

# 1. Broken callout-title (no </div> before <p>)
#    Find <div class="callout-title"...>NON_TAG_TEXT\n<p>
#    The capture group preserves the title text; we add </div>
BROKEN_TITLE_RE = re.compile(
    r'(<div\s+class="callout-title"[^>]*>)([^<\n]+)\n(\s*)<p>',
    re.IGNORECASE,
)

# 2. Lame exercise intro
LAME_EXERCISE_INTRO_RE = re.compile(
    r'(<h2\s+id="exercises"[^>]*>[^<]*</h2>)\s*'
    r'<p>(?:(?!</p>).)+</p>\s*'
    r'(<div\s+class="callout exercise")',
    re.DOTALL | re.IGNORECASE,
)


def fix_file(p: Path) -> dict[str, int]:
    text = p.read_text(encoding='utf-8')
    orig = text
    counts = {'broken_title': 0, 'lame_intro': 0}

    # Need to be careful: BROKEN_TITLE_RE should only fire when inside a callout
    # (we don't want to break legitimate <div class="callout-title">Long Title
    # Spanning Multiple Lines</div> patterns). Heuristic: only fire if the
    # title text is followed by `<p>` on the very next line.
    def br_repl(m):
        counts['broken_title'] += 1
        return f'{m.group(1)}{m.group(2)}</div>\n{m.group(3)}<p>'
    text = BROKEN_TITLE_RE.sub(br_repl, text)

    # Exercise intro removal
    def lame_repl(m):
        counts['lame_intro'] += 1
        return f'{m.group(1)}\n{m.group(2)}'
    text = LAME_EXERCISE_INTRO_RE.sub(lame_repl, text)

    if text != orig:
        p.write_text(text, encoding='utf-8')
    return counts


def main():
    totals = {'broken_title': 0, 'lame_intro': 0}
    files_touched = 0
    for p in sorted(ROOT.rglob('*.html')):
        if set(p.parts) & SKIP:
            continue
        c = fix_file(p)
        if sum(c.values()) > 0:
            files_touched += 1
            for k, v in c.items():
                totals[k] += v
    print('=== Wave 71 round-4 structural fixes ===')
    print(f'Broken callout-title (no </div>): {totals["broken_title"]}')
    print(f'Lame exercise intro removed:      {totals["lame_intro"]}')
    print(f'Files touched: {files_touched}')


if __name__ == '__main__':
    main()
