"""v6.3.3: Unify bibliography header — single "References & Further Reading" box.

USER REPORT
"section-29.2.html has both 'References' (empty) and 'References and
Further Reading' box, should be only 'References and Further Reading'
everywhere (box design)."

ROOT CAUSE
After v6.2 normalization, every bibliography has the structure:
  <details ... bibliography-collapsible>
    <summary><strong>References</strong></summary>      <-- HEADER 1
    <section class="bibliography">
      <div class="bibliography-title">References &amp; Further Reading</div>  <-- HEADER 2
      ...entries...
    </section>
  </details>

In the HTML, when expanded, the user sees both headers. In the EPUB,
where `<details>` is converted to `<div class="details-shim">` and
`<summary>` becomes `<p class="details-title">`, both headers render
as bold elements. Visually this looks like two separate label boxes.

FIX
Drop the inner `<div class="bibliography-title">` element entirely.
Promote the summary text to the canonical "References & Further
Reading" so the single visible header is informative.

After:
  <details ... bibliography-collapsible>
    <summary><strong>References &amp; Further Reading</strong></summary>
    <section class="bibliography">
      ...entries...
    </section>
  </details>

This is a strictly visual normalization; no content changes.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SKIP = {'agents', 'KDP', 'node_modules', 'scripts', '.git',
        'chapter_review', 'downloads', '_archive', '_lab_fragments',
        'templates'}

# A. Promote summary text
SUMMARY_PAT = re.compile(
    r'(<details[^>]*class="bibliography-collapsible"[^>]*>\s*'
    r'<summary[^>]*>\s*<strong>)\s*References\s*(</strong>\s*</summary>)',
    re.IGNORECASE,
)

# B. Drop inner bibliography-title <div>
INNER_TITLE_PAT = re.compile(
    r'\s*<div class="bibliography-title">[^<]+</div>\s*\n?'
)


def fix(p: Path) -> int:
    text = p.read_text(encoding='utf-8', errors='replace')
    if 'bibliography-collapsible' not in text:
        return 0
    edits = 0

    # A. Promote summary
    new_text, na = SUMMARY_PAT.subn(
        lambda m: m.group(1) + 'References &amp; Further Reading' + m.group(2),
        text,
    )
    if na:
        edits += na
        text = new_text

    # B. Strip inner title
    new_text, nb = INNER_TITLE_PAT.subn('\n', text)
    if nb:
        edits += nb
        text = new_text

    if edits and text != p.read_text(encoding='utf-8', errors='replace'):
        p.write_text(text, encoding='utf-8')
    return edits


def main() -> int:
    total = 0
    files = 0
    for p in sorted(ROOT.rglob('*.html')):
        rel = p.relative_to(ROOT)
        if rel.parts and rel.parts[0] in SKIP:
            continue
        n = fix(p)
        if n:
            files += 1
            total += n

    print(f'Edits: {total} across {files} files')

    # Verification: count remaining structures
    summaries = {'References': 0, 'References & Further Reading': 0}
    inner_titles = 0
    total_bibs = 0
    for p in sorted(ROOT.rglob('*.html')):
        rel = p.relative_to(ROOT)
        if rel.parts and rel.parts[0] in SKIP:
            continue
        text = p.read_text(encoding='utf-8', errors='replace')
        for m in re.finditer(
            r'<details[^>]*class="bibliography-collapsible"[^>]*>\s*<summary[^>]*>\s*<strong>([^<]+)</strong>',
            text,
        ):
            total_bibs += 1
            t = m.group(1).strip().replace('&amp;', '&')
            summaries[t] = summaries.get(t, 0) + 1
        inner_titles += len(re.findall(r'<div class="bibliography-title">', text))

    print(f'\nFinal state:')
    print(f'  Total bibliographies: {total_bibs}')
    print(f'  Summary text variants:')
    for k, v in summaries.items():
        print(f'    {v:>4}x  "{k}"')
    print(f'  Remaining <div class="bibliography-title">: {inner_titles}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
