"""Wave 38c: Propagate canonical chapter title to all section breadcrumbs.

For each `module-N-slug/index.html`:
  1. Read the canonical chapter title from its `<h1>...</h1>`
  2. For every `section-N.M.html` in that module:
     - Rewrite the breadcrumb anchor:
       `<a href="index.html">Chapter XX: STALE_TITLE</a>`
       -> `<a href="index.html">Chapter N: CANONICAL_TITLE</a>`
     - Also rewrite chapter-nav `<a class="up" href="index.html">` nav-title

This addresses cycle-3 findings:
- Module-67 sections 67.4-67.15 say "Chapter 64: LLM Product Management" / "Chapter 65: LLM Strategy" / "Chapter 68: From Idea to Product Hypothesis"
- Module-78 sections 78.1-78.10 say wrong chapter titles
- Ch 47 chapter-index title/meta say "Safety, Ethics & Regulation"
- 43 section files across Ch 42/43/44/47/52/54/55/57/60 with stale breadcrumb titles
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'.git', 'node_modules', 'KDP', 'build', 'source_fix_backups',
        'pagefind', '.book-update', 'vendor', '.claude', '_archive',
        'agents', 'templates', 'docs', 'scripts'}

MODULE_DIR_RE = re.compile(r'module-(\d+)-')


def get_chapter_num(path: Path) -> int | None:
    for part in path.parts:
        m = MODULE_DIR_RE.match(part)
        if m:
            return int(m.group(1))
    return None


def get_canonical_title(index_html: str) -> str | None:
    """Extract the chapter title from <h1>...</h1> of the chapter index page."""
    m = re.search(r'<h1[^>]*>([^<]+)</h1>', index_html)
    if not m:
        return None
    return m.group(1).strip()


def propagate_chapter_title(section_html: str, chapter_num: int, canonical_title: str) -> tuple[str, int]:
    """Rewrite breadcrumb and chapter-nav up-link to canonical chapter title."""
    n_changes = 0
    canonical_full = f'Chapter {chapter_num}: {canonical_title}'
    canonical_full_with_amp = canonical_full.replace('&', '&amp;')  # for HTML escape

    # Pattern 1: breadcrumb <a href="index.html">Chapter XX: ANY_TITLE</a>
    # Note: title may contain `&amp;` etc.
    bc_pattern = re.compile(
        r'(<a\s+href="index\.html">)Chapter\s+(\d+):\s*([^<]+?)(</a>)',
        re.IGNORECASE,
    )

    def bc_repl(m: re.Match) -> str:
        nonlocal n_changes
        old_num = m.group(2)
        old_title = m.group(3).strip()
        if old_num == str(chapter_num) and old_title == canonical_full_with_amp.split(": ", 1)[1]:
            return m.group(0)  # already canonical
        n_changes += 1
        return f'{m.group(1)}{canonical_full_with_amp}{m.group(4)}'
    section_html = bc_pattern.sub(bc_repl, section_html)

    # Pattern 2: chapter-nav <a class="up" href="index.html">
    # <span class="nav-title">CHAPTER_TITLE_ONLY</span>
    # The nav-title contains just the chapter title, no "Chapter N:" prefix.
    nav_title_pattern = re.compile(
        r'(<a\s+class="up"\s+href="index\.html"[^>]*>[\s\S]*?<span\s+class="nav-title">)([^<]+)(</span>)',
        re.IGNORECASE,
    )

    def nav_title_repl(m: re.Match) -> str:
        nonlocal n_changes
        old_title = m.group(2).strip()
        if old_title == canonical_title.replace('&', '&amp;'):
            return m.group(0)
        n_changes += 1
        return f'{m.group(1)}{canonical_title.replace("&", "&amp;")}{m.group(3)}'
    section_html = nav_title_pattern.sub(nav_title_repl, section_html)

    return section_html, n_changes


def main():
    # Step 1: build a map module_num -> canonical_title from all index.html files
    module_titles = {}
    for index_path in sorted(ROOT.glob('part-*/module-*/index.html')):
        if set(index_path.parts) & SKIP:
            continue
        ch_num = get_chapter_num(index_path)
        if ch_num is None:
            continue
        text = index_path.read_text(encoding='utf-8')
        canonical = get_canonical_title(text)
        if canonical:
            module_titles[ch_num] = canonical

    print(f'Detected canonical titles for {len(module_titles)} modules')

    # Step 2: for each section file, propagate its module's canonical title
    n_files = 0
    n_changes = 0
    for section_path in sorted(ROOT.rglob('section-*.html')):
        if set(section_path.parts) & SKIP:
            continue
        ch_num = get_chapter_num(section_path)
        if ch_num is None or ch_num not in module_titles:
            continue
        canonical = module_titles[ch_num]
        text = section_path.read_text(encoding='utf-8')
        new, changes = propagate_chapter_title(text, ch_num, canonical)
        if changes > 0 and new != text:
            section_path.write_text(new, encoding='utf-8')
            n_files += 1
            n_changes += changes

    print(f'\nUpdated {n_files} section files with {n_changes} breadcrumb / nav-title fixes')


if __name__ == '__main__':
    main()
