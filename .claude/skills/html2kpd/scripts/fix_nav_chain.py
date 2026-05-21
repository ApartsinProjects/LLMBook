"""Rebuild navigation chains to be sequential.

For each module / appendix directory under <root>, rebuild prev/next
chain based on actual file numerical order:

    section-N.1.html:    prev=index.html,        next=section-N.2.html
    section-N.K.html:    prev=section-N.(K-1),  next=section-N.(K+1)
    section-N.last.html: prev=section-N.(last-1), next=NEXT_MODULE_INDEX

NEXT_MODULE_INDEX is determined from the sibling-dir order (with
letter-length sort for appendices: a < b < ... < z < aa < ab < ...).
Cross-part transitions are handled by walking up to part-*/ siblings.

Usage:
    python fix_nav_chain.py --root <book-root>           # dry-run
    python fix_nav_chain.py --root <book-root> --apply   # write changes

The "up" link in each section points to the module's index.html.

Idempotent: re-running on a clean tree produces no changes.
"""
from __future__ import annotations
import argparse
import os
import re
import sys
from pathlib import Path

from bs4 import BeautifulSoup


def get_section_files(mod_dir: Path) -> list[tuple[int, Path]]:
    """Sorted list of (number, path) for section files."""
    out = []
    for f in mod_dir.glob('section-*.html'):
        m = re.match(r'section-(\d+)\.(\d+)\.html', f.name, re.I)
        if m:
            out.append((int(m.group(2)), f))
            continue
        m = re.match(r'section-([a-z]+)\.(\d+)\.html', f.name, re.I)
        if m:
            out.append((int(m.group(2)), f))
    return sorted(out)


def _sort_key(dir_name: str) -> tuple:
    """Sort modules / appendices stably.

    appendix-aa goes AFTER appendix-z (length-then-lex).
    module-NN sorts by NN as int.
    part-NN sorts by NN as int.
    """
    m = re.match(r'appendix-([a-z]+)(?:-|$)', dir_name)
    if m:
        letters = m.group(1)
        return (len(letters), letters)
    m = re.match(r'module-(\d+)', dir_name)
    if m:
        return (int(m.group(1)),)
    m = re.match(r'part-(\d+)', dir_name)
    if m:
        return (int(m.group(1)),)
    return (999, dir_name)


def find_module(mod_dir: Path, direction: int) -> Path | None:
    """Find prev or next module dir. direction in {-1, +1}."""
    parent = mod_dir.parent
    sibs = sorted([d for d in parent.iterdir()
                    if d.is_dir() and (d / 'index.html').exists()],
                   key=lambda d: _sort_key(d.name))
    try:
        idx = sibs.index(mod_dir)
        new_idx = idx + direction
        if 0 <= new_idx < len(sibs):
            return sibs[new_idx]
    except ValueError:
        pass
    # Cross-part
    if parent.name.startswith('part-'):
        part_parent = parent.parent
        part_sibs = sorted([d for d in part_parent.iterdir()
                            if d.is_dir() and d.name.startswith('part-')],
                           key=lambda d: _sort_key(d.name))
        try:
            pidx = part_sibs.index(parent)
            new_pidx = pidx + direction
            if 0 <= new_pidx < len(part_sibs):
                other_part = part_sibs[new_pidx]
                other_mods = sorted([d for d in other_part.iterdir()
                                     if d.is_dir() and (d / 'index.html').exists()],
                                    key=lambda d: _sort_key(d.name))
                if other_mods:
                    return other_mods[-1] if direction == -1 else other_mods[0]
        except ValueError:
            pass
    return None


def fix_module(mod_dir: Path, root: Path, dry_run: bool) -> int:
    sections = get_section_files(mod_dir)
    if not sections:
        return 0
    changes = 0
    idx_file = mod_dir / 'index.html'

    # Get module title (for "up" link text)
    idx_title = 'Module'
    if idx_file.exists():
        s = BeautifulSoup(idx_file.read_text(encoding='utf-8'), 'html.parser')
        h1 = s.find('h1')
        if h1:
            idx_title = h1.get_text(strip=True)

    # Get each section title
    titles = {}
    for num, p in sections:
        s = BeautifulSoup(p.read_text(encoding='utf-8'), 'html.parser')
        h1 = s.find('h1')
        titles[num] = h1.get_text(strip=True) if h1 else f'Section {num}'

    # Determine external next (where last section's next points)
    next_mod = find_module(mod_dir, +1)
    if next_mod:
        nm_idx = next_mod / 'index.html'
        rel_path = os.path.relpath(nm_idx, mod_dir).replace('\\', '/')
        nm_title = 'Next'
        if nm_idx.exists():
            nm_s = BeautifulSoup(nm_idx.read_text(encoding='utf-8'),
                                  'html.parser')
            h1 = nm_s.find('h1')
            if h1:
                nm_title = h1.get_text(strip=True)
        external_next = (rel_path, nm_title)
    else:
        external_next = None

    def build_nav(prev_href, prev_text, next_href, next_text,
                  up_href, up_text):
        def trunc(t, n=55):
            if not t:
                return t
            return t if len(t) <= n else t[:n - 3] + '...'
        return (
            f'<nav class="chapter-nav">\n'
            f'<a class="prev" href="{prev_href}">{trunc(prev_text)}</a>\n'
            f'<a class="up" href="{up_href}">{trunc(up_text)}</a>\n'
            f'<a class="next" href="{next_href}">{trunc(next_text)}</a>\n'
            f'</nav>'
        )

    for i, (num, p) in enumerate(sections):
        s = BeautifulSoup(p.read_text(encoding='utf-8'), 'html.parser')
        nav = s.find('nav', class_='chapter-nav')
        if not nav:
            continue

        if i == 0:
            new_prev_href = 'index.html'
            new_prev_text = idx_title
        else:
            prev_num = sections[i - 1][0]
            new_prev_href = sections[i - 1][1].name
            new_prev_text = titles[prev_num]

        if i == len(sections) - 1:
            if external_next:
                new_next_href, new_next_text = external_next
            else:
                new_next_href = '../index.html'
                new_next_text = 'Up'
        else:
            next_num = sections[i + 1][0]
            new_next_href = sections[i + 1][1].name
            new_next_text = titles[next_num]

        new_up_href = 'index.html'
        new_up_text = idx_title

        cur_prev = nav.find('a', class_='prev')
        cur_next = nav.find('a', class_='next')
        cur_up = nav.find('a', class_='up')

        cur_prev_href = cur_prev.get('href', '') if cur_prev else ''
        cur_next_href = cur_next.get('href', '') if cur_next else ''
        cur_up_href = cur_up.get('href', '') if cur_up else ''

        if (cur_prev_href != new_prev_href
                or cur_next_href != new_next_href
                or cur_up_href != new_up_href):
            new_nav_html = build_nav(
                new_prev_href, new_prev_text,
                new_next_href, new_next_text,
                new_up_href, new_up_text,
            )
            new_nav = BeautifulSoup(new_nav_html, 'html.parser')
            nav.replace_with(new_nav)
            changes += 1
            if dry_run:
                print(f'  WOULD FIX {p.relative_to(root)}:')
                print(f'    prev: {cur_prev_href} -> {new_prev_href}')
                print(f'    next: {cur_next_href} -> {new_next_href}')
            else:
                p.write_text(str(s), encoding='utf-8')

    # Fix index.html nav
    if idx_file.exists() and sections:
        s = BeautifulSoup(idx_file.read_text(encoding='utf-8'), 'html.parser')
        nav = s.find('nav', class_='chapter-nav')
        if nav:
            wrote = False
            cur_next = nav.find('a', class_='next')
            cur_prev = nav.find('a', class_='prev')

            first_name = sections[0][1].name
            first_title = titles[sections[0][0]]
            if cur_next and cur_next.get('href') != first_name:
                cur_next['href'] = first_name
                cur_next.clear()
                cur_next.append(first_title[:55])
                changes += 1
                wrote = True

            prev_mod = find_module(mod_dir, -1)
            if prev_mod and cur_prev:
                prev_sections = get_section_files(prev_mod)
                if prev_sections:
                    _, last_path = prev_sections[-1]
                    rel = os.path.relpath(last_path,
                                           idx_file.parent).replace('\\', '/')
                    ls_s = BeautifulSoup(last_path.read_text(encoding='utf-8'),
                                          'html.parser')
                    lh = ls_s.find('h1')
                    last_title = lh.get_text(strip=True) if lh else 'Previous'
                    if cur_prev.get('href') != rel:
                        cur_prev['href'] = rel
                        cur_prev.clear()
                        cur_prev.append(last_title[:55])
                        changes += 1
                        wrote = True

            if wrote and not dry_run:
                idx_file.write_text(str(s), encoding='utf-8')

    return changes


def find_modules(root: Path) -> list[Path]:
    """Find all module / appendix dirs with section files under root."""
    mods = []
    for part_dir in root.glob('part-*'):
        if not part_dir.is_dir():
            continue
        for mod_dir in part_dir.iterdir():
            if mod_dir.is_dir() and list(mod_dir.glob('section-*.html')):
                mods.append(mod_dir)
    app_root = root / 'appendices'
    if app_root.exists():
        for app_dir in app_root.iterdir():
            if app_dir.is_dir() and list(app_dir.glob('section-*.html')):
                mods.append(app_dir)
    return mods


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root', type=Path, required=True)
    ap.add_argument('--apply', action='store_true',
                    help='Write changes (default: dry-run)')
    args = ap.parse_args(argv)

    root: Path = args.root.resolve()
    if not root.exists():
        print(f'ERROR: root does not exist: {root}', file=sys.stderr)
        return 2

    dry = not args.apply
    if dry:
        print('DRY RUN. Pass --apply to write changes.')
    print()
    total = 0
    for mod in find_modules(root):
        n = fix_module(mod, root, dry)
        if n:
            print(f'{mod.relative_to(root)}: {n} nav fixes')
            total += n
    print(f'\nTotal nav fixes: {total}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
