"""Fix path-depth issues from Wave 1.5: try alternative depths to find correct resolution."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'.git', 'node_modules', 'KDP', 'build', 'temp_ebook', 'temp_epub',
        'source_fix_backups', 'pagefind', 'templates', '.claude',
        '.book-update', 'vendor', 'docs'}

PART_DIRS = sorted([d.name for d in ROOT.glob('part-*/') if d.is_dir()])


def try_paths(source_file, original_href):
    """Try resolving original_href; if broken, try paths with one fewer or one more `../`."""
    base = source_file.parent
    # Already valid?
    try:
        target = (base / original_href).resolve()
        if target.exists():
            return original_href
    except: pass
    # Try removing one ../
    if original_href.startswith('../'):
        try_href = original_href[3:]
        try:
            target = (base / try_href).resolve()
            if target.exists():
                return try_href
        except: pass
    # Try adding one ../
    try_href = '../' + original_href
    try:
        target = (base / try_href).resolve()
        if target.exists():
            return try_href
    except: pass
    # Try with part-X prefix (for cross-part refs that lost their part)
    m = re.match(r'((?:\.\./)+)(module-\d+-[\w-]+)(/.*)?', original_href)
    if m:
        up_part = m.group(1)
        mod_part = m.group(2)
        rest = m.group(3) or ''
        for part_dir in PART_DIRS:
            try_href = f'{up_part}{part_dir}/{mod_part}{rest}'
            try:
                target = (base / try_href).resolve()
                if target.exists():
                    return try_href
            except: pass
    return None


def main():
    n_files = 0
    counter = [0]

    for p in sorted(ROOT.rglob('*.html')):
        if set(p.parts) & SKIP: continue
        text = p.read_text(encoding='utf-8')
        orig = text

        def fix(m):
            href = m.group(1)
            if href.startswith('http') or href.startswith('#') or href.startswith('mailto:'):
                return m.group(0)
            try:
                target = (p.parent / href.split('#')[0]).resolve()
                if target.exists():
                    return m.group(0)
            except:
                return m.group(0)
            clean_href = href.split('#')[0]
            anchor = '#' + href.split('#', 1)[1] if '#' in href else ''
            fixed = try_paths(p, clean_href)
            if fixed:
                counter[0] += 1
                return f'href="{fixed}{anchor}"'
            return m.group(0)

        text = re.sub(r'href="([^"]+)"', fix, text)
        if text != orig:
            p.write_text(text, encoding='utf-8')
            n_files += 1

    print(f'Fixed paths in {n_files} files ({counter[0]} hrefs)')


if __name__ == '__main__':
    main()
