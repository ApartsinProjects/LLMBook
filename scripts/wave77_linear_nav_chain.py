"""Wave 77: Fix the chapter-nav next pointer to follow the linear reading
order across the book.

Two violation patterns:
1. Chapter-index page's <a class="next"> points to the NEXT chapter's
   index.html — should point to its OWN first section (section-N.1.html).
2. The LAST section of a chapter has next pointing to the next chapter's
   index.html — should point to the next chapter's FIRST section
   (section-N+1.1.html).
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'.git', 'node_modules', 'KDP', 'build', 'source_fix_backups',
        'pagefind', '.book-update', 'vendor', '.claude', '_archive',
        'agents', 'templates', 'docs', 'scripts'}


def _classify(filepath: Path) -> str | None:
    name = filepath.name
    parts = filepath.parts
    if name.startswith('section-') and name.endswith('.html'):
        return 'section'
    if name == 'index.html':
        for p in parts[-3:]:
            if p.startswith('module-'):
                return 'chapter'
    return None


def _first_section_of_module(mod_dir: Path) -> Path | None:
    sections = sorted(mod_dir.glob('section-*.html'),
                      key=lambda p: tuple(
                          int(x) if x.isdigit() else x
                          for x in re.findall(r'\d+|[a-z]+', p.stem)
                      ))
    return sections[0] if sections else None


def _all_sections(mod_dir: Path) -> list[Path]:
    return sorted(mod_dir.glob('section-*.html'),
                  key=lambda p: tuple(
                      int(x) if x.isdigit() else x
                      for x in re.findall(r'\d+|[a-z]+', p.stem)
                  ))


def fix_file(p: Path) -> int:
    text = p.read_text(encoding='utf-8')
    orig = text
    kind = _classify(p)
    if kind is None:
        return 0

    # Find next link
    m = re.search(r'<a\s+class="next"\s+href="([^"]+)"', text)
    if not m:
        return 0

    href = m.group(1)
    new_href = None

    if kind == 'chapter':
        # If next points to a sibling module's index, redirect to OWN first section
        if 'index.html' in href and 'module-' in href:
            first_sec = _first_section_of_module(p.parent)
            if first_sec:
                new_href = first_sec.name

    elif kind == 'section':
        sections = _all_sections(p.parent)
        try:
            idx = sections.index(p)
        except ValueError:
            return 0
        if idx == len(sections) - 1:
            # LAST section in module — should point to next module's first section
            # Currently: href might be "../module-NN+1-*/index.html"
            if href.endswith('index.html') and 'module-' in href:
                # Replace 'index.html' with the next module's first section name
                # We need to resolve the target module to find its first section
                # href is relative; resolve relative to p
                target = (p.parent / href).resolve()
                if target.exists() and target.parent.is_dir():
                    first_sec = _first_section_of_module(target.parent)
                    if first_sec:
                        # Rebuild href with first_sec.name in place of index.html
                        new_href = href.replace('index.html', first_sec.name)

    if not new_href or new_href == href:
        return 0

    # Replace the next link href
    new_text = text.replace(
        f'<a class="next" href="{href}"',
        f'<a class="next" href="{new_href}"',
        1,
    )
    if new_text == text:
        return 0
    p.write_text(new_text, encoding='utf-8')
    return 1


def main():
    n = 0
    for p in sorted(ROOT.rglob('*.html')):
        if set(p.parts) & SKIP:
            continue
        if fix_file(p):
            n += 1
    print(f'NAV_LINEAR_CHAIN fixes applied: {n}')


if __name__ == '__main__':
    main()
