"""Fix stale section/chapter numbers in h2/h3 display text where the id
already has the new number but display text has the old.

Pattern (BAD):
  <h2 id="75-4-1-the-universal-recipe">80.4.1 The Universal Recipe</h2>
                ^^^ new                  ^^^ stale

Fix: replace the stale number prefix in display text with the new number
from the id.

Also fixes the doubled-id pattern: id="75-4-80-4-2-..." (double-prepended).

And catches missing </h2> close tags (a related bug found in section-75.4).
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


# Match opening h2/h3 with id, then text content, then </h2>/</h3> OR
# UNCLOSED h2/h3 (missing close)
H_OPEN_RE = re.compile(
    r'<(h[23])\s+id="([^"]+)"[^>]*>([^<]*?)(?=<(?:h[1-6]|p|div|ul|ol|section|nav|/main|figure)|$)',
    re.DOTALL,
)


def number_from_id(hid: str) -> str | None:
    """Convert id 'NN-N-N-...' to display 'NN.N.N'."""
    m = re.match(r'^(\d+(?:-\d+)*)', hid)
    if not m:
        return None
    return m.group(1).replace('-', '.')


def fix_text(text: str, relpath: str) -> tuple[str, dict]:
    counts = {'stale_num': 0, 'unclosed_h': 0, 'doubled_id': 0}

    # First: fix doubled IDs like id="75-4-80-4-2-foo"
    def fix_doubled_id(m):
        full = m.group(0)
        hid = m.group(2)
        # Pattern: NN-N-NN-N-... where the first NN matches a NEW module
        # number AND NN-N appears again later. Detect and collapse.
        m2 = re.match(r'^(\d+)-(\d+)-(\d+)-(\d+)-(\d+)(.*)$', hid)
        if m2:
            a, b, c, d, e, rest = m2.groups()
            # If a.b is a valid prefix and c.d.e is the actual section sub-id
            # we want a-b-e<rest> — drop the doubled c-d
            # We only do this when c == OLD number for any module that was renumbered
            # to a; specifically, when {a: c} matches our renumber map.
            # Renumber map: 80->75, 81->76, 82->77, 83->78
            renumber = {'75': '80', '76': '81', '77': '82', '78': '83'}
            if a in renumber and renumber[a] == c and b == d:
                new_hid = f'{a}-{b}-{e}{rest}'
                counts['doubled_id'] += 1
                # Reconstruct the opening tag
                return f'<{m.group(1)} id="{new_hid}">'
        return full

    # Apply doubled-id fix as a pre-pass
    text = re.sub(
        r'<(h[23])\s+id="([^"]+)"[^>]*>',
        fix_doubled_id,
        text,
    )

    # Now fix stale display numbers
    # Iterate over all <h2>/<h3 id="..."> and check the FIRST text after the >
    out_parts = []
    last = 0
    h_re = re.compile(r'<(h[23])\s+id="([^"]+)"[^>]*>')
    for m in h_re.finditer(text):
        tag = m.group(1)
        hid = m.group(2)
        tag_end = m.end()
        # Find the closing </h2>/</h3> OR next opening tag
        close_re = re.compile(rf'</{tag}>', re.IGNORECASE)
        close_m = close_re.search(text, tag_end)
        next_open = re.search(r'<(?:h[1-6]|p|div|ul|ol|section|nav|figure|/main)\b', text[tag_end:])
        if close_m and (not next_open or close_m.start() < tag_end + next_open.start()):
            # h tag is properly closed
            display_text = text[tag_end:close_m.start()]
            close_ok = True
            text_end = close_m.start()
            full_end = close_m.end()
        else:
            # UNCLOSED — body extends until next block tag
            if next_open:
                display_text = text[tag_end:tag_end + next_open.start()]
                close_ok = False
                text_end = tag_end + next_open.start()
                full_end = text_end
                counts['unclosed_h'] += 1
            else:
                continue

        # Check for stale number in display_text
        new_num = number_from_id(hid)
        if not new_num:
            continue
        # Strip leading whitespace, then match leading number
        dt = display_text.lstrip()
        nm = re.match(r'^((\d+\.)+\d+)\s*', dt)
        if nm:
            stale_num = nm.group(1)
            # If stale_num != new_num and stale_num shares the same dotted depth, fix
            if stale_num != new_num:
                stale_parts = stale_num.split('.')
                new_parts = new_num.split('.')
                # Only proceed if depths match (same h-level granularity)
                if len(stale_parts) == len(new_parts):
                    # Replace the leading number
                    new_display = display_text.replace(stale_num, new_num, 1)
                    # Append closing tag if missing
                    if not close_ok:
                        new_display = new_display.rstrip() + f'</{tag}>'
                    # Splice back
                    out_parts.append(text[last:tag_end])
                    out_parts.append(new_display)
                    last = full_end
                    counts['stale_num'] += 1
                    continue
            elif not close_ok:
                # Number is OK but tag is unclosed
                new_display = display_text.rstrip() + f'</{tag}>'
                out_parts.append(text[last:tag_end])
                out_parts.append(new_display)
                last = full_end
                continue
        elif not close_ok:
            # Unclosed but no stale-num issue
            new_display = display_text.rstrip() + f'</{tag}>'
            out_parts.append(text[last:tag_end])
            out_parts.append(new_display)
            last = full_end

    out_parts.append(text[last:])
    return ''.join(out_parts), counts


def main():
    apply = '--apply' in sys.argv
    print(f"{'APPLY' if apply else 'DRY-RUN'}")
    totals = {'stale_num': 0, 'unclosed_h': 0, 'doubled_id': 0}
    files = 0
    for f in ROOT.rglob('*.html'):
        if any(s in f.parts for s in ('_archive', 'node_modules', '.git',
                                       'pagefind', 'KDP', 'build', 'vendor',
                                       '.claude', '__pycache__', 'templates')):
            continue
        if not f.name.startswith('section-'):
            continue
        text = f.read_text(encoding='utf-8')
        new_text, counts = fix_text(text, str(f.relative_to(ROOT)))
        if new_text != text:
            files += 1
            for k, v in counts.items():
                totals[k] += v
            if any(counts.values()):
                print(f'  {f.relative_to(ROOT)}: {counts}')
            if apply:
                f.write_text(new_text, encoding='utf-8')
    print(f'\nFiles: {files}, totals: {totals}')


if __name__ == '__main__':
    main()
