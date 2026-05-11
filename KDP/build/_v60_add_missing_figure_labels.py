"""v6.0: Add <strong>Figure N.M.K</strong>: prefix to figcaptions that
have prose but no figure label at all.

Distinct from the v5.8 figcaption fixer, which filled empty
<strong></strong> tags. THIS fixer handles a different case:
  <figcaption>plain prose, no <strong>, no Figure label</figcaption>

Audit found 40 such figcaptions across the book:
  - 17 appendix index pages (chapter-opener illustrations)
  - 15 module-29/31/32 section figures (illustration-style figures)
  - A few others

Fix strategy mirrors the v5.8 logic: walk figures in order, track
existing K's, assign next-available K to unlabeled ones with the
section's canonical prefix.

Also re-center the Figure 11.1.7 SVG in section-11.1.html. The current
SVG has boxes at x=30 with width=660 on a viewBox of 950x340, leaving
~260px of white space on the right. We shift them to be horizontally
centered.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SKIP = {'agents', 'KDP', 'node_modules', 'scripts', '.git',
        'chapter_review', 'downloads', '_archive', '_lab_fragments',
        'templates'}


def section_prefix(p: Path) -> str | None:
    name = p.name
    m = re.match(r'section-([0-9a-zA-Z]+(?:\.[0-9a-zA-Z]+)*)\.html$', name)
    if m:
        prefix = m.group(1)
        return prefix.upper() if prefix[0].isalpha() else prefix
    if name == 'index.html':
        parent = p.parent.name
        mm = re.match(r'module-0*(\d+)-', parent)
        if mm:
            return f'{int(mm.group(1))}.0'
        ma = re.match(r'appendix-([a-z])-', parent)
        if ma:
            return f'{ma.group(1).upper()}.0'
    return None


def fix_file(p: Path) -> int:
    text = p.read_text(encoding='utf-8', errors='replace')

    prefix = section_prefix(p)
    if prefix is None:
        return 0

    # Find all figures in order with their existing labels
    fig_iter = []
    for m in re.finditer(r'<figure[^>]*>(.*?)</figure>', text, re.DOTALL):
        body = m.group(1)
        fc = re.search(r'<figcaption([^>]*)>(.*?)</figcaption>', body, re.DOTALL)
        if not fc:
            continue
        fc_attrs = fc.group(1)
        fc_body = fc.group(2).strip()
        # Position of <figcaption opening tag inside the full text
        fc_open_pos = m.start() + fc.start()
        existing = re.search(
            r'<strong>\s*(?:Figure|Fig\.)\s*([\d\.a-zA-Z]+)\s*</strong>',
            fc_body, re.IGNORECASE,
        )
        if existing:
            try:
                k = int(existing.group(1).split('.')[-1])
            except ValueError:
                k = 0
            fig_iter.append(('numbered', fc_open_pos, fc_attrs, fc_body, k))
        else:
            fig_iter.append(('unlabeled', fc_open_pos, fc_attrs, fc_body, None))

    if not any(kind == 'unlabeled' for kind, *_ in fig_iter):
        return 0

    # Determine next K (max existing K for this prefix, +1)
    existing_ks = [k for kind, _, _, _, k in fig_iter
                   if kind == 'numbered' and k]
    next_k = (max(existing_ks) + 1) if existing_ks else 1

    # Build edits: for each unlabeled, prepend <strong>Figure prefix.K</strong>: to the figcaption body
    edits = []
    for kind, fc_open_pos, attrs, body, _ in fig_iter:
        if kind != 'unlabeled':
            continue
        new_k = next_k
        next_k += 1
        new_body = f'<strong>Figure {prefix}.{new_k}</strong>: {body}'
        # Build the new figcaption opening tag (preserve original attrs)
        # We will replace the old <figcaption ...>old_body</figcaption> with
        # <figcaption ...>new_body</figcaption> via exact-string at fc_open_pos.
        old_fc_full = f'<figcaption{attrs}>{body}</figcaption>'
        new_fc_full = f'<figcaption{attrs}>{new_body}</figcaption>'
        edits.append((fc_open_pos, old_fc_full, new_fc_full))

    # Apply in reverse offset order
    edits.sort(reverse=True)
    new_text = text
    n_done = 0
    for pos, old, new in edits:
        idx = new_text.find(old, max(0, pos - 200))
        if idx == -1:
            # Try anywhere
            idx = new_text.find(old)
        if idx == -1:
            continue
        new_text = new_text[:idx] + new + new_text[idx + len(old):]
        n_done += 1

    if new_text != text:
        p.write_text(new_text, encoding='utf-8')
    return n_done


# ----- Re-center Figure 11.1.7 SVG ----------------------------------

def fix_fig_11_1_7() -> int:
    """Shift all SVG elements in Figure 11.1.7 so the 660-wide boxes are
    centered on the 950-wide viewBox. Offset = (950 - 660) / 2 - 30 = +115."""
    p = ROOT / 'part-3-working-with-llms/module-11-prompt-engineering/section-11.1.html'
    text = p.read_text(encoding='utf-8')
    # Find the SVG block belonging to Figure 11.1.7
    m = re.search(
        r'(<svg[^>]+viewBox="0 0 950 340"[^>]*>)(?P<body>(?:.|\n)*?)(</svg>\s*<div class="diagram-caption"><strong>Figure 11\.1\.7</strong>)',
        text,
    )
    if not m:
        print('  WARN: Figure 11.1.7 SVG not found')
        return 0

    svg_body = m.group('body')

    # Idempotent check: if we've already centered, the first <rect> will have
    # x="145" rather than x="30"
    if 'rect fill="url(#grad_cb1cd4_f0e6ff)"' in svg_body and 'x="145"' in svg_body:
        print('  Figure 11.1.7 already centered; skipping (idempotent).')
        return 0

    # Shift specific x= values used in this SVG by +115 to center the 660px-wide
    # content on the 950px viewBox.
    OFFSET = 115
    shift_map = {
        # Main boxes (3 rects of width 660): x=30 -> 145
        ' x="30" y="50"':  ' x="145" y="50"',
        ' x="30" y="160"': ' x="145" y="160"',
        ' x="30" y="245"': ' x="145" y="245"',
        # Sub-boxes inside SYSTEM (x=50, 195, 340, 485 -> +115)
        ' x="50" y="82"':  ' x="165" y="82"',
        ' x="195" y="82"': ' x="310" y="82"',
        ' x="340" y="82"': ' x="455" y="82"',
        ' x="485" y="82"': ' x="600" y="82"',
        # System message labels (x=50 prefix, 115/260/405/550 text)
        ' x="50" y="72"':  ' x="165" y="72"',
        ' x="115" y="100"':' x="230" y="100"',
        ' x="260" y="100"':' x="375" y="100"',
        ' x="405" y="100"':' x="520" y="100"',
        ' x="550" y="100"':' x="665" y="100"',
        ' x="50" y="135"': ' x="165" y="135"',
        # Few-shot row
        ' x="50" y="182"': ' x="165" y="182"',
        ' x="50" y="192"': ' x="165" y="192"',
        ' x="195" y="210"':' x="310" y="210"',
        ' x="360" y="192"':' x="475" y="192"',
        ' x="515" y="210"':' x="630" y="210"',
        # User message row
        ' x="50" y="267"': ' x="165" y="267"',
        ' x="50" y="277"': ' x="165" y="277"',
        ' x="150" y="295"':' x="265" y="295"',
        ' x="270" y="277"':' x="385" y="277"',
        ' x="370" y="295"':' x="485" y="295"',
        # Arrows (x1=x2=360 -> 475)
        ' x1="360" x2="360"':' x1="475" x2="475"',
    }
    new_body = svg_body
    for old, new in shift_map.items():
        new_body = new_body.replace(old, new)

    if new_body == svg_body:
        print('  WARN: no shifts applied to Figure 11.1.7 SVG')
        return 0

    new_text = text[:m.start('body')] + new_body + text[m.end('body'):]
    p.write_text(new_text, encoding='utf-8')
    print('  Figure 11.1.7 SVG: shifted content +115px to center on viewBox.')
    return 1


def main() -> int:
    # A. Add Figure labels to unlabeled figcaptions
    print('A. Add missing Figure labels')
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
    print(f'   Labeled {total} figures across {files} files\n')

    # B. Re-center Figure 11.1.7
    print('B. Re-center Figure 11.1.7 SVG')
    fix_fig_11_1_7()
    return 0


if __name__ == '__main__':
    sys.exit(main())
