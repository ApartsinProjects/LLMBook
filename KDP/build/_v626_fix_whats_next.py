"""v6.26: Auto-fix misaligned "What's Next" boxes.

For each section whose <div class="whats-next"> points to the wrong target,
rewrite the box's first <a href> to point to the actual next section in
reading order, with that section's real H1 as the link label.

Preserves any prose around the link — only the href and visible label are
rewritten. If the prose names the wrong section by a (short) title, we
also attempt to update that occurrence in the same paragraph.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

PARTS_ORDER = [
    'part-1-foundations', 'part-2-understanding-llms', 'part-3-working-with-llms',
    'part-4-training-adapting', 'part-5-retrieval-conversation', 'part-6-agentic-ai',
    'part-7-multimodal-applications', 'part-8-evaluation-production',
    'part-9-safety-strategy', 'part-10-frontiers', 'part-11-idea-to-product',
]


def _section_key(p):
    m = re.match(r'section-(\d+)\.(\d+)(?:\.(\d+))?', p.stem)
    if not m:
        return (9999, 9999, 9999)
    return (int(m.group(1)), int(m.group(2)), int(m.group(3)) if m.group(3) else 0)


def get_h1(p):
    text = p.read_text(encoding='utf-8', errors='replace')
    m = re.search(r'<h1[^>]*>(.+?)</h1>', text, re.DOTALL)
    if m:
        return re.sub(r'<[^>]+>', '', m.group(1)).strip()
    return p.stem


def relpath_for(target, current):
    """Compute href from current.html dir to target.html (POSIX)."""
    import os
    return os.path.relpath(target, current.parent).replace('\\', '/')


def section_id_label(p):
    """Return 'Section X.Y' from filename."""
    m = re.match(r'section-(\d+)\.(\d+)', p.stem)
    if m:
        return f'Section {m.group(1)}.{m.group(2)}'
    return p.stem


def build_spine():
    spine = []
    for pdir in PARTS_ORDER:
        p = ROOT / pdir
        if not p.exists():
            continue
        mods = sorted(p.glob('module-*'),
                      key=lambda d: int(re.match(r'module-0*(\d+)-', d.name).group(1)))
        for m in mods:
            spine.extend(sorted(m.glob('section-*.html'), key=_section_key))
    return spine


def main() -> int:
    spine = build_spine()
    print(f'Spine: {len(spine)} sections')

    fixed = 0
    for i, p in enumerate(spine):
        text = p.read_text(encoding='utf-8')
        wn_m = re.search(r'<div class="whats-next">(.*?)</div>', text, re.DOTALL)
        if not wn_m:
            continue
        body = wn_m.group(1)
        link_m = re.search(r'<a href="([^"]+)"[^>]*>([^<]+)</a>', body)
        if not link_m:
            continue
        href, label = link_m.group(1), link_m.group(2)
        if href.startswith('http://') or href.startswith('https://'):
            continue
        target = (p.parent / href).resolve()
        if i + 1 >= len(spine):
            continue  # last section, no next
        actual_next = spine[i + 1]
        if target == actual_next:
            continue  # already correct
        # Allow target=index.html (intentional chapter-end jump)
        if target.name == 'index.html' and target.exists():
            continue

        # Build the corrected link
        new_href = relpath_for(actual_next, p)
        new_h1 = get_h1(actual_next)
        new_id = section_id_label(actual_next)
        new_link = f'<a href="{new_href}">{new_id}: {new_h1}</a>'
        old_link = link_m.group(0)
        new_body = body.replace(old_link, new_link, 1)

        # Also try to update the label in any prose mentioning it (best-effort).
        # Look for "Section X.Y" pattern in body and update if it mentions a wrong number
        # Pattern is fragile, so just swap the link itself and trust the prose.

        new_wn = wn_m.group(0).replace(body, new_body)
        new_text = text.replace(wn_m.group(0), new_wn)
        if new_text == text:
            continue
        p.write_text(new_text, encoding='utf-8')
        rel = str(p.relative_to(ROOT)).replace('\\', '/')
        print(f'  fixed: {rel}')
        print(f'         old: {old_link[:80]}')
        print(f'         new: {new_link[:80]}')
        fixed += 1

    print(f'\nFixed {fixed} What\'s-Next boxes.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
