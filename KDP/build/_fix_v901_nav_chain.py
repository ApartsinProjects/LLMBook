"""v901: Rebuild navigation chains to be sequential.

Root cause: many modules have prev/next pointing to wrong sections after
content was renumbered/reorganized. This rebuilds the chain based on
actual file numerical order.

For each module/appendix directory:
  - section-N.1.html: prev=index.html, next=section-N.2.html
  - section-N.K.html: prev=section-N.(K-1).html, next=section-N.(K+1).html
  - section-N.last.html: prev=section-N.(last-1).html, next=NEXT_MODULE_INDEX

The NEXT_MODULE_INDEX is determined from the existing last section's next link
(preserves cross-module transitions).
"""
from pathlib import Path
from bs4 import BeautifulSoup
import re


ROOT = Path(__file__).resolve().parents[2]


def get_section_files(mod_dir):
    """Return sorted list of (number, path) for section files.

    Handles both numeric (section-28.4.html) and alpha (section-t.1.html) prefixes.
    """
    out = []
    for f in mod_dir.glob('section-*.html'):
        # Try numeric prefix: section-NN.M.html
        m = re.match(r'section-(\d+)\.(\d+)\.html', f.name, re.I)
        if m:
            out.append((int(m.group(2)), f))
            continue
        # Try alpha prefix: section-X.M.html (X is letters)
        m = re.match(r'section-([a-z]+)\.(\d+)\.html', f.name, re.I)
        if m:
            out.append((int(m.group(2)), f))
    return sorted(out)


def _appendix_sort_key(dir_name):
    """Sort appendix dirs: a, b, c, ..., z, aa, ab, ..., ak.

    For 'appendix-X-rest', extract X. Sort by (length(X), X).
    For module dirs (module-NN-rest), extract NN as int.
    For part dirs (part-NN-rest), extract NN as int.
    Returns a tuple compatible with stable sorting.
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


def find_prev_module(mod_dir):
    """Find the previous module directory based on sibling ordering."""
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
    """Find the next module directory based on sibling ordering."""
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
    # Cross-part: try next part
    if parent.name.startswith('part-'):
        part_parent = parent.parent
        part_sibs = sorted([d for d in part_parent.iterdir() if d.is_dir()
                            and d.name.startswith('part-')],
                           key=lambda d: _appendix_sort_key(d.name))
        try:
            pidx = part_sibs.index(parent)
            if pidx + 1 < len(part_sibs):
                next_part = part_sibs[pidx + 1]
                # First module in next part
                next_mods = sorted([d for d in next_part.iterdir()
                                    if d.is_dir() and (d / 'index.html').exists()],
                                   key=lambda d: _appendix_sort_key(d.name))
                if next_mods:
                    return next_mods[0]
        except ValueError:
            pass
    return None


def fix_module(mod_dir, dry_run=True):
    """Fix navigation for one module/appendix directory."""
    sections = get_section_files(mod_dir)
    if not sections:
        return 0
    changes = 0
    idx_file = mod_dir / 'index.html'

    # Read each file's existing nav to extract the external transitions
    # (from index.prev and last.next which we'll preserve)
    external_prev = None  # what comes before the index
    external_next = None  # what comes after the last section
    external_up = None  # parent (e.g., appendices/index.html)

    if idx_file.exists():
        s = BeautifulSoup(idx_file.read_text(encoding='utf-8'), 'html.parser')
        nav = s.find('nav', class_='chapter-nav')
        if nav:
            prev = nav.find('a', class_='prev')
            up = nav.find('a', class_='up')
            if prev:
                external_prev = (prev.get('href'), prev.get_text(strip=True))
            if up:
                external_up = (up.get('href'), up.get_text(strip=True))

    # Get external_next from the last section's existing next link.
    # If the existing next is suspicious (points to a different module
    # going backwards, or points inside this module), use the directory
    # sibling order to find the real next module.
    last_section = sections[-1][1]
    s_last = BeautifulSoup(last_section.read_text(encoding='utf-8'), 'html.parser')
    nav = s_last.find('nav', class_='chapter-nav')
    candidate_external = None
    if nav:
        nxt = nav.find('a', class_='next')
        if nxt and not nxt.get('href', '').startswith('section-'):
            candidate_external = (nxt.get('href'), nxt.get_text(strip=True))

    # Validate candidate: it should point to either the immediate next sibling
    # module or the first module of the next part. Anything else is suspect.
    needs_recompute = False
    if candidate_external is None:
        needs_recompute = True
    else:
        expected_next_mod = find_next_module(mod_dir)
        if expected_next_mod is None:
            # End of book; trust whatever candidate is
            pass
        else:
            href = candidate_external[0]
            try:
                tgt = (last_section.parent / href).resolve()
                expected_idx = (expected_next_mod / 'index.html').resolve()
                # Accept the candidate if it points to that module's index
                # OR to first section of that module
                if tgt == expected_idx:
                    pass  # OK
                else:
                    # Check if it points into expected_next_mod at all
                    try:
                        tgt.relative_to(expected_next_mod.resolve())
                        # It's inside the next module, accept
                    except ValueError:
                        # Points elsewhere — recompute
                        needs_recompute = True
            except Exception:
                needs_recompute = True

    if needs_recompute:
        next_mod = find_next_module(mod_dir)
        if next_mod:
            # Build relative path from last_section to next_mod/index.html
            try:
                rel = Path(*['..'] * (len(last_section.parent.relative_to(ROOT).parts)))
                # Easier: just use os.path.relpath
                import os
                rel_path = os.path.relpath(
                    next_mod / 'index.html', last_section.parent
                ).replace('\\', '/')
                # Read next module's index title
                nm_idx = next_mod / 'index.html'
                if nm_idx.exists():
                    nm_s = BeautifulSoup(nm_idx.read_text(encoding='utf-8'),
                                          'html.parser')
                    h1 = nm_s.find('h1')
                    nm_title = h1.get_text(strip=True) if h1 else 'Next'
                else:
                    nm_title = 'Next'
                external_next = (rel_path, nm_title)
            except Exception:
                external_next = candidate_external
        else:
            external_next = candidate_external
    else:
        external_next = candidate_external

    # Title for each section (for use in nav link text)
    titles = {}
    for num, p in sections:
        s = BeautifulSoup(p.read_text(encoding='utf-8'), 'html.parser')
        h1 = s.find('h1')
        titles[num] = h1.get_text(strip=True) if h1 else f'Section {num}'

    # Get index title for "up" link text
    idx_title = 'Module'
    if idx_file.exists():
        s = BeautifulSoup(idx_file.read_text(encoding='utf-8'), 'html.parser')
        h1 = s.find('h1')
        if h1:
            idx_title = h1.get_text(strip=True)

    def build_nav(prev_href, prev_text, next_href, next_text, up_href, up_text):
        # Truncate long titles for nav display
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

    # Fix each section file
    for i, (num, p) in enumerate(sections):
        s = BeautifulSoup(p.read_text(encoding='utf-8'), 'html.parser')
        nav = s.find('nav', class_='chapter-nav')
        if not nav:
            continue

        # Determine expected prev/next
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
                # No external, default to parent index
                new_next_href = '../index.html'
                new_next_text = 'Up'
        else:
            next_num = sections[i + 1][0]
            new_next_href = sections[i + 1][1].name
            new_next_text = titles[next_num]

        new_up_href = 'index.html'
        new_up_text = idx_title

        # Get current nav
        cur_prev = nav.find('a', class_='prev')
        cur_next = nav.find('a', class_='next')
        cur_up = nav.find('a', class_='up')

        cur_prev_href = cur_prev.get('href', '') if cur_prev else ''
        cur_next_href = cur_next.get('href', '') if cur_next else ''
        cur_up_href = cur_up.get('href', '') if cur_up else ''

        if (cur_prev_href != new_prev_href or
                cur_next_href != new_next_href or
                cur_up_href != new_up_href):
            new_nav_html = build_nav(
                new_prev_href, new_prev_text,
                new_next_href, new_next_text,
                new_up_href, new_up_text,
            )
            new_nav = BeautifulSoup(new_nav_html, 'html.parser')
            nav.replace_with(new_nav)
            changes += 1
            if not dry_run:
                p.write_text(str(s), encoding='utf-8')
            else:
                print(f'  WOULD FIX {p.relative_to(ROOT)}:')
                print(f'    prev: {cur_prev_href} -> {new_prev_href}')
                print(f'    next: {cur_next_href} -> {new_next_href}')

    # Fix index.html nav: next should be first section; prev should be
    # previous module's LAST section
    if idx_file.exists() and sections:
        s = BeautifulSoup(idx_file.read_text(encoding='utf-8'), 'html.parser')
        nav = s.find('nav', class_='chapter-nav')
        if nav:
            wrote = False
            cur_next = nav.find('a', class_='next')
            cur_prev = nav.find('a', class_='prev')

            first_section_name = sections[0][1].name
            first_section_title = titles[sections[0][0]]
            if cur_next and cur_next.get('href') != first_section_name:
                cur_next['href'] = first_section_name
                cur_next.clear()
                cur_next.append(first_section_title[:55])
                changes += 1
                wrote = True

            # Determine previous module's last section
            prev_mod = find_prev_module(mod_dir)
            if prev_mod and cur_prev:
                prev_sections = get_section_files(prev_mod)
                if prev_sections:
                    last_num, last_path = prev_sections[-1]
                    import os
                    rel = os.path.relpath(last_path, idx_file.parent).replace('\\', '/')
                    # Get title
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


def find_modules():
    """Find all module/appendix directories with section files."""
    mods = []
    for part_dir in ROOT.glob('part-*'):
        if not part_dir.is_dir():
            continue
        for mod_dir in part_dir.iterdir():
            if mod_dir.is_dir() and list(mod_dir.glob('section-*.html')):
                mods.append(mod_dir)
    for app_dir in (ROOT / 'appendices').iterdir():
        if app_dir.is_dir() and list(app_dir.glob('section-*.html')):
            mods.append(app_dir)
    return mods


if __name__ == '__main__':
    import sys
    DRY = '--apply' not in sys.argv
    if DRY:
        print('DRY RUN. Pass --apply to write changes.')
    print()
    total = 0
    for mod in find_modules():
        n = fix_module(mod, dry_run=DRY)
        if n:
            print(f'{mod.relative_to(ROOT)}: {n} nav fixes')
            total += n
    print(f'\nTotal nav fixes: {total}')
