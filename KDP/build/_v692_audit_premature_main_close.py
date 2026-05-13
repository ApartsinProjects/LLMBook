"""8th edition: detect HTML files where </main> is closed BEFORE the
bibliography <section>, leaving bib + Exercises + What-Next outside the
page-width-constrained <main class="content"> container.

Symptom: the bottom cards stretch to the full viewport width because they
inherit no max-width / padding from <main class="content">.

Root cause: bibliography insertion script wrapped its content in
'</main><section class="bibliography">...</section>' with no
re-opening of <main>, then the exercises + whats-next blocks were
appended further down OUTSIDE <main>.

Fix mode: --fix
  Two-step rewrite per affected file:
  1. Replace `</main><section class="bibliography"` with
     `<section class="bibliography"` (drop the premature close).
  2. Find the LAST `</body>` and ensure a `</main>` exists right before
     it (just before the trailing pagefind <script>).
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SKIP = ('node_modules', '.git/', 'pagefind/', 'KDP/build/', 'KDP/output/',
        'templates/', '_archive/', 'temp_epub/')

PAT_PREMATURE = re.compile(r'</main>\s*<section[^>]*class="bibliography', re.IGNORECASE)
PAT_DROP = re.compile(r'</main>\s*(<section[^>]*class="bibliography)', re.IGNORECASE)


def fix_file(text: str) -> tuple[str, bool]:
    if not PAT_PREMATURE.search(text):
        return text, False
    # Drop the premature </main>
    new = PAT_DROP.sub(r'\1', text, count=1)
    # Insert </main> right before the final </body>
    # Be careful: file should not already have a </main> at the end.
    # If a </main> exists between bibliography and </body>, don't add another.
    bib_idx = new.lower().find('<section')
    body_idx = new.lower().rfind('</body>')
    if bib_idx == -1 or body_idx == -1:
        return text, False
    tail = new[bib_idx:body_idx]
    if '</main>' in tail.lower():
        # Already closed somewhere in tail -- bug pattern doesn't apply
        return new, True
    new = new[:body_idx] + '</main>\n' + new[body_idx:]
    return new, True


def main() -> int:
    fix = '--fix' in sys.argv
    n_hits = 0
    n_fixed = 0
    fixed_paths: list[str] = []
    for p in sorted(ROOT.rglob('*.html')):
        sp = str(p).replace('\\', '/')
        if any(s in sp for s in SKIP):
            continue
        try:
            text = p.read_text(encoding='utf-8', errors='replace')
        except Exception:
            continue
        if not PAT_PREMATURE.search(text):
            continue
        n_hits += 1
        if fix:
            new, changed = fix_file(text)
            if changed and new != text:
                p.write_text(new, encoding='utf-8')
                n_fixed += 1
                fixed_paths.append(str(p.relative_to(ROOT)))
        else:
            print(f'  premature </main>: {p.relative_to(ROOT)}')
    if fix:
        print(f'\nFixed {n_fixed} files (rewrote </main> placement).')
        for fp in fixed_paths[:20]:
            print(f'  {fp}')
        if len(fixed_paths) > 20:
            print(f'  ... and {len(fixed_paths)-20} more')
    else:
        print(f'\nFound {n_hits} files with premature </main> before bibliography.')
        if n_hits:
            print('Re-run with --fix to repair.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
