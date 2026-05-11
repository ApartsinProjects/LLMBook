"""v6.3: Add Figure labels to the 22 remaining unlabeled figcaptions
that the v6.0 fixer's exact-string matcher missed.

Root cause: those figcaptions have multi-line whitespace formatting
like:
  <figcaption style="text-align: center; ...">
      No single security barrier...
  </figcaption>
The v6.0 fixer used `<figcaption{attrs}>{stripped_body}</figcaption>`
as the exact match string, but the actual HTML has whitespace + the
unstripped body. The find() returned -1 silently.

This v6.3 fixer uses regex replacement instead of exact-string matching.
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


# Match a <figcaption ...>BODY</figcaption> where BODY does NOT contain
# either "Figure" or "<strong>". This is the unlabeled case.
UNLABELED_PAT = re.compile(
    r'<figcaption([^>]*)>(?P<body>(?:(?!</figcaption>).)*?)</figcaption>',
    re.DOTALL,
)


def fix_file(p: Path) -> int:
    text = p.read_text(encoding='utf-8', errors='replace')
    prefix = section_prefix(p)
    if prefix is None:
        return 0

    # Find all <figcaption> in order; track existing K's and unlabeled positions
    figcaps = []
    for m in UNLABELED_PAT.finditer(text):
        body = m.group('body')
        # Has Figure label?
        existing = re.search(
            r'<strong>\s*(?:Figure|Fig\.)\s*([\d\.a-zA-Z]+)\s*</strong>',
            body, re.IGNORECASE,
        )
        figcaps.append({'span': (m.start(), m.end()),
                        'attrs': m.group(1),
                        'body': body,
                        'existing_k': existing,
                        'whole': m.group(0)})

    # Compute starting K
    existing_ks = []
    for fc in figcaps:
        if fc['existing_k']:
            try:
                num_str = fc['existing_k'].group(1)
                if num_str.startswith(prefix + '.'):
                    k = int(num_str[len(prefix) + 1:].split('.')[0])
                    existing_ks.append(k)
            except ValueError:
                pass
    next_k = (max(existing_ks) + 1) if existing_ks else 1

    # Apply edits in REVERSE order (preserve offsets)
    edits_count = 0
    new_text = text
    for fc in reversed(figcaps):
        if fc['existing_k']:
            continue
        # Construct new body
        body_text = fc['body'].lstrip().rstrip()
        new_body = f'<strong>Figure {prefix}.{next_k}</strong>: {body_text}'
        next_k += 1
        # Build replacement using the matched attrs
        new_whole = f'<figcaption{fc["attrs"]}>{new_body}</figcaption>'
        s, e = fc['span']
        new_text = new_text[:s] + new_whole + new_text[e:]
        edits_count += 1

    if edits_count and new_text != text:
        p.write_text(new_text, encoding='utf-8')
    return edits_count


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
            print(f'  + {n}  {rel}')
    print(f'\nLabeled {total} figures across {files} files')
    return 0


if __name__ == '__main__':
    sys.exit(main())
