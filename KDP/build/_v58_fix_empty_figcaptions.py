"""v5.8: Fill empty <strong></strong> in <figcaption> with proper figure numbers.

Audit found 229 empty <figcaption><strong></strong>: ...</figcaption> across
132 files. The user spotted "10.3.4.2 Semantic Caching" — the figure
beneath it had `<strong></strong>:` instead of `<strong>Figure N.M.K</strong>:`.

Fix strategy: PER section file:
  1. Determine the section number prefix from the filename:
       section-N.M.html        -> "N.M"
       section-N.html          -> "N"
       section-X.M.html (appx) -> "X.M"
       index.html (in module-N-...) -> "N.0"
  2. Walk all <figure> blocks IN DOCUMENT ORDER.
  3. Track existing numbered figures: if a <figcaption> contains
     "Figure {prefix}.K", record K and continue.
  4. For each empty <figcaption><strong></strong>:</figcaption>, assign the
     next sequential K (max(seen)+1).
  5. Replace the empty <strong></strong> with <strong>Figure {prefix}.K</strong>.

This avoids renumbering existing figures (which would break cross-refs)
while still filling in the gaps.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

SKIP = {'agents', 'KDP', 'node_modules', 'scripts', '.git',
        'chapter_review', 'downloads', '_archive', '_lab_fragments',
        'templates'}

# Match figcaption with empty <strong></strong>
EMPTY_FIGCAP = re.compile(
    r'(?P<head><figcaption[^>]*>\s*<strong>)\s*(?P<tail></strong>\s*:)'
)
# Match a figcaption with an EXISTING figure number
EXISTING_FIGCAP = re.compile(
    r'<figcaption[^>]*>\s*<strong>\s*(?:Figure|Fig\.)\s*(?P<num>[\d\.a-z]+)\s*</strong>',
    re.IGNORECASE,
)


def section_prefix(p: Path) -> str | None:
    """Determine the figure-number prefix for this file."""
    name = p.name
    m = re.match(r'section-([0-9a-zA-Z]+(?:\.[0-9a-zA-Z]+)*)\.html$', name)
    if m:
        return m.group(1).upper() if m.group(1)[0].isalpha() else m.group(1)
    if name == 'index.html':
        # try to derive from parent module-NN-... directory
        parent = p.parent.name
        mm = re.match(r'module-0*(\d+)-', parent)
        if mm:
            return f'{int(mm.group(1))}.0'
        # appendix
        ma = re.match(r'appendix-([a-z])-', parent)
        if ma:
            return f'{ma.group(1).upper()}.0'
    return None


def fix_file(p: Path) -> int:
    text = p.read_text(encoding='utf-8', errors='replace')
    if '<figcaption><strong></strong>:' not in text and '<figcaption><strong> </strong>:' not in text:
        # Quick reject if no exact-match empty pattern
        if not EMPTY_FIGCAP.search(text):
            return 0

    prefix = section_prefix(p)
    if prefix is None:
        return 0  # unrecognized location

    # First pass: enumerate ALL figure occurrences in order, recording existing K's
    # We need the ORDER of all <figcaption>s so we know "where" each empty one sits.
    fig_iter = []
    pos = 0
    pat_fig = re.compile(r'<figcaption[^>]*>')
    for m in pat_fig.finditer(text):
        # Determine if numbered or empty
        snippet = text[m.start():m.start() + 300]
        em = re.match(
            r'<figcaption[^>]*>\s*<strong>\s*(?:Figure|Fig\.)\s*(?P<num>[\d\.a-zA-Z]+)\s*</strong>',
            snippet, re.IGNORECASE,
        )
        if em:
            fig_iter.append(('numbered', m.start(), em.group('num')))
        elif EMPTY_FIGCAP.match(snippet):
            fig_iter.append(('empty', m.start(), None))
        else:
            fig_iter.append(('other', m.start(), None))

    # Determine starting K = max existing K (matching prefix) + 1
    existing_ks = []
    for kind, _, num in fig_iter:
        if kind == 'numbered' and num and num.startswith(prefix + '.'):
            try:
                k = int(num[len(prefix) + 1:].split('.')[0])
                existing_ks.append(k)
            except ValueError:
                pass
    next_k = (max(existing_ks) + 1) if existing_ks else 1

    # Apply replacements in REVERSE order (so offsets don't shift)
    edits = []
    for kind, pos_start, _ in fig_iter:
        if kind != 'empty':
            continue
        # Compute the new figure number; reserve next_k
        new_num = f'{prefix}.{next_k}'
        next_k += 1
        edits.append((pos_start, new_num))
        existing_ks.append(int(new_num.rsplit('.', 1)[1]))

    if not edits:
        return 0

    # Apply in reverse order
    edits.sort(reverse=True)
    new_text = text
    n_done = 0
    for pos_start, new_num in edits:
        # Find the empty pattern starting at pos_start and substitute once
        local_pat = re.compile(
            r'(<figcaption[^>]*>\s*<strong>)\s*(</strong>\s*:)'
        )
        # Substitute the FIRST match starting at >= pos_start
        sub_done = False
        def repl(m: re.Match) -> str:
            nonlocal sub_done
            if sub_done:
                return m.group(0)
            sub_done = True
            return f'{m.group(1)}Figure {new_num}{m.group(2)}'

        # Apply to the slice starting at pos_start
        slice_before = new_text[:pos_start]
        slice_after = new_text[pos_start:]
        slice_after_new = local_pat.sub(repl, slice_after, count=1)
        if sub_done:
            new_text = slice_before + slice_after_new
            n_done += 1

    if new_text != text:
        p.write_text(new_text, encoding='utf-8')
    return n_done


def main() -> int:
    total = 0
    files = 0
    for p in sorted(ROOT.rglob('*.html')):
        rel = p.relative_to(ROOT)
        if rel.parts and rel.parts[0] in SKIP:
            continue
        n = fix_file(p)
        if n:
            files += 1
            total += n
    print(f'Filled {total} empty <figcaption><strong></strong> across {files} files')
    return 0


if __name__ == '__main__':
    sys.exit(main())
