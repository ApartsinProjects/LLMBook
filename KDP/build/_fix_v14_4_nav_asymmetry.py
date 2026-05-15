"""v14.4: fix the 10 cross-boundary navigation asymmetries.

Pattern: when section N.last.next points to module-K/index, the
module-K/index.prev should point back to N.last. After section
additions (28.10-12, 30.10-12) and module renumbers, several
boundary pages still reference older neighbor anchors.

Strategy: for each module-index that's the FIRST in its part OR
follows a different module, recompute its prev to point to the
previous module's LAST section (numerically sorted).

Also fix the symmetric case: section.next should point at the next
module's first page (its index.html).
"""
from pathlib import Path
from bs4 import BeautifulSoup
import os
import re
import sys

ROOT = Path(__file__).resolve().parents[2]


def _appendix_sort_key(name):
    m = re.match(r'appendix-([a-z]+)(?:-|$)', name)
    if m:
        letters = m.group(1)
        return (len(letters), letters)
    m = re.match(r'module-(\d+)', name)
    if m:
        return (int(m.group(1)),)
    m = re.match(r'part-(\d+)', name)
    if m:
        return (int(m.group(1)),)
    return (999, name)


def get_section_files(mod_dir):
    """Return sorted list of (number, path) for section files."""
    out = []
    for f in mod_dir.glob('section-*.html'):
        m = re.match(r'section-(\d+)\.(\d+)\.html', f.name)
        if m:
            out.append((int(m.group(2)), f))
            continue
        m = re.match(r'section-([a-z]+)\.(\d+)\.html', f.name)
        if m:
            out.append((int(m.group(2)), f))
    return sorted(out)


def find_prev_module(mod_dir):
    parent = mod_dir.parent
    sibs = sorted([d for d in parent.iterdir() if d.is_dir()
                   and (d / 'index.html').exists()],
                  key=lambda d: _appendix_sort_key(d.name))
    try:
        idx = sibs.index(mod_dir)
        if idx > 0:
            return sibs[idx - 1]
    except ValueError:
        pass
    # Cross-part: try previous part's last module
    if parent.name.startswith('part-'):
        part_parent = parent.parent
        part_sibs = sorted([d for d in part_parent.iterdir() if d.is_dir()
                            and d.name.startswith('part-')],
                           key=lambda d: _appendix_sort_key(d.name))
        try:
            pidx = part_sibs.index(parent)
            if pidx > 0:
                prev_part = part_sibs[pidx - 1]
                prev_mods = sorted([d for d in prev_part.iterdir()
                                    if d.is_dir() and (d / 'index.html').exists()],
                                   key=lambda d: _appendix_sort_key(d.name))
                if prev_mods:
                    return prev_mods[-1]
        except ValueError:
            pass
    return None


def find_next_module(mod_dir):
    parent = mod_dir.parent
    sibs = sorted([d for d in parent.iterdir() if d.is_dir()
                   and (d / 'index.html').exists()],
                  key=lambda d: _appendix_sort_key(d.name))
    try:
        idx = sibs.index(mod_dir)
        if idx + 1 < len(sibs):
            return sibs[idx + 1]
    except ValueError:
        pass
    if parent.name.startswith('part-'):
        part_parent = parent.parent
        part_sibs = sorted([d for d in part_parent.iterdir() if d.is_dir()
                            and d.name.startswith('part-')],
                           key=lambda d: _appendix_sort_key(d.name))
        try:
            pidx = part_sibs.index(parent)
            if pidx + 1 < len(part_sibs):
                next_part = part_sibs[pidx + 1]
                next_mods = sorted([d for d in next_part.iterdir()
                                    if d.is_dir() and (d / 'index.html').exists()],
                                   key=lambda d: _appendix_sort_key(d.name))
                if next_mods:
                    return next_mods[0]
        except ValueError:
            pass
    return None


def get_h1_title(p):
    if not p.exists():
        return None
    try:
        s = BeautifulSoup(p.read_text(encoding='utf-8'), 'html.parser')
        h1 = s.find('h1')
        return h1.get_text(strip=True) if h1 else None
    except Exception:
        return None


def fix_module_index_prev(mod_dir, dry):
    """Ensure mod_dir/index.html.prev points to the previous module's last section."""
    idx_file = mod_dir / 'index.html'
    if not idx_file.exists():
        return False
    prev_mod = find_prev_module(mod_dir)
    if not prev_mod:
        return False  # No previous, leave as-is

    prev_sections = get_section_files(prev_mod)
    if not prev_sections:
        # Previous module is a single-page appendix; point to its index
        target = prev_mod / 'index.html'
    else:
        _, target = prev_sections[-1]

    s = BeautifulSoup(idx_file.read_text(encoding='utf-8'), 'html.parser')
    nav = s.find('nav', class_='chapter-nav')
    if not nav:
        return False
    prev_a = nav.find('a', class_='prev')
    if not prev_a:
        return False

    rel = os.path.relpath(target, idx_file.parent).replace('\\', '/')
    if prev_a.get('href') == rel:
        return False  # already correct

    new_title = get_h1_title(target) or 'Previous'
    prev_a['href'] = rel
    prev_a.clear()
    prev_a.append(new_title[:55])

    if not dry:
        idx_file.write_text(str(s), encoding='utf-8')
    return True


def fix_last_section_next(mod_dir, dry):
    """Ensure mod_dir/section-N.last.next points to next module's index."""
    sections = get_section_files(mod_dir)
    if not sections:
        return False
    _, last_path = sections[-1]
    next_mod = find_next_module(mod_dir)
    if not next_mod:
        return False

    target = next_mod / 'index.html'
    s = BeautifulSoup(last_path.read_text(encoding='utf-8'), 'html.parser')
    nav = s.find('nav', class_='chapter-nav')
    if not nav:
        return False
    next_a = nav.find('a', class_='next')
    if not next_a:
        return False

    rel = os.path.relpath(target, last_path.parent).replace('\\', '/')
    if next_a.get('href') == rel:
        return False  # already correct

    new_title = get_h1_title(target) or 'Next'
    next_a['href'] = rel
    next_a.clear()
    next_a.append(new_title[:55])

    if not dry:
        last_path.write_text(str(s), encoding='utf-8')
    return True


def find_modules():
    mods = []
    for part_dir in ROOT.glob('part-*'):
        if not part_dir.is_dir():
            continue
        for mod_dir in part_dir.iterdir():
            if mod_dir.is_dir() and (mod_dir / 'index.html').exists():
                mods.append(mod_dir)
    for app_dir in (ROOT / 'appendices').iterdir():
        if app_dir.is_dir() and (app_dir / 'index.html').exists():
            mods.append(app_dir)
    return mods


if __name__ == '__main__':
    dry = '--apply' not in sys.argv
    print('DRY RUN. Pass --apply to write changes.' if dry else 'APPLY mode.')
    print()
    n_total = 0
    for mod in find_modules():
        a = fix_module_index_prev(mod, dry)
        b = fix_last_section_next(mod, dry)
        if a:
            print(f'  fix index.prev: {mod.relative_to(ROOT)}')
            n_total += 1
        if b:
            print(f'  fix last.next:  {mod.relative_to(ROOT)}')
            n_total += 1
    print(f'\nTotal nav fixes: {n_total}')
