"""Wave 38b: Fix zero-padded chapter labels + specific wrong-chapter breadcrumbs.

Affects:
- All module-N/index.html with zero-padded "Chapter 00/01/.../09" in <title>, <meta>, pagefind-meta, breadcrumb, nav-num
- All section-N.M.html under module-N/ with zero-padded nav-num "Chapter 00/01/.../09"
- Module-67 section-67.4-67.15 breadcrumbs say "Chapter 64/65/68"; canonical is Chapter 67
- Module-78 section-78.1-78.10 breadcrumbs say "Chapter 78/79/80"; canonical is Chapter 78 (already correct for 78.1-78.5 if title was renamed; sweep blank-slate)
- section-49.3 <title> says "Section 49.6"; section-49.4 <title> says "Section 49.7"
- U+FFFD replacement chars in body content

Strategy: per file we trust the directory name (`module-NN-...`) to give the
canonical chapter number, then enforce that number throughout the file's
structural HTML elements (title, meta-desc, breadcrumb, pagefind-meta,
chapter-nav nav-num). Prose references are NOT touched (too risky).
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


# Patterns where we can SAFELY replace "Chapter NN" with the canonical
# (we constrain to structural locations: meta, title, breadcrumb, pagefind, nav-num)
STRUCTURAL_PATTERNS = [
    # <meta content="Chapter NN: ..." name="description"/>
    re.compile(r'(<meta\s+content="Chapter\s+)(\d+)(:[^"]*"\s+name="description")', re.IGNORECASE),
    # <title>Chapter NN: ...</title>
    re.compile(r'(<title>Chapter\s+)(\d+)(:)', re.IGNORECASE),
    # <span class="bc-current">Chapter NN</span>  OR  <a ...>Chapter NN: ...</a> in breadcrumb
    re.compile(r'(<span\s+class="bc-current">Chapter\s+)(\d+)(\s*</span>)', re.IGNORECASE),
    # <a href="index.html">Chapter NN: ...</a> in breadcrumb
    # (only modify if the href is index.html or ../module-NN-... matches our chapter)
    # Skip this pattern for now -- too easy to mis-rewrite cross-chapter links.

    # data-pagefind-meta="chapter:Chapter NN: ..."
    re.compile(r'(data-pagefind-meta="chapter:Chapter\s+)(\d+)(:[^"]*")', re.IGNORECASE),
    # <span class="nav-num">Chapter NN</span> in chapter-nav (only when surrounding "up" class)
    re.compile(r'(<a\s+class="up"\s+href="index\.html"[^>]*>[\s\S]*?<span\s+class="nav-num">Chapter\s+)(\d+)(\s*</span>)', re.IGNORECASE),
]

# U+FFFD replacement-character cleanup
FFFD_RE = re.compile(r'�')

# Section-49.3 / 49.4 title off-by-3 (need explicit fix)
SECTION_TITLE_PATTERNS = {
    'section-49.3.html': ('Section 49.6', 'Section 49.3'),
    'section-49.4.html': ('Section 49.7', 'Section 49.4'),
}


def fix_chapter_label(text: str, canonical_chapter: int) -> tuple[str, int]:
    """Rewrite zero-padded or off-by-one Chapter NN in structural locations to canonical."""
    n_changes = 0
    canonical_str = str(canonical_chapter)
    for pat in STRUCTURAL_PATTERNS:
        def repl(m: re.Match) -> str:
            nonlocal n_changes
            old = m.group(2)
            if old == canonical_str:
                return m.group(0)  # already correct
            # Don't auto-fix big drift (e.g., "Chapter 60" should not become "Chapter 6"); skip when diff > 10
            try:
                old_n = int(old)
                if abs(old_n - canonical_chapter) > 12 and canonical_chapter != 0:
                    # Big drift; needs author review
                    return m.group(0)
            except ValueError:
                return m.group(0)
            n_changes += 1
            return f'{m.group(1)}{canonical_str}{m.group(3)}'
        text = pat.sub(repl, text)
    return text, n_changes


def fix_section_title(text: str, filename: str) -> tuple[str, int]:
    if filename in SECTION_TITLE_PATTERNS:
        old, new = SECTION_TITLE_PATTERNS[filename]
        if old in text:
            return text.replace(old, new), 1
    return text, 0


def fix_fffd(text: str) -> tuple[str, int]:
    n = len(FFFD_RE.findall(text))
    if n == 0:
        return text, 0
    return FFFD_RE.sub('?', text), n


def main():
    n_files = 0
    n_chap = 0
    n_title = 0
    n_fffd = 0
    for p in sorted(ROOT.rglob('*.html')):
        if set(p.parts) & SKIP:
            continue
        ch = get_chapter_num(p)
        text = p.read_text(encoding='utf-8')
        original = text

        if ch is not None:
            text, c1 = fix_chapter_label(text, ch)
            n_chap += c1
        text, c2 = fix_section_title(text, p.name)
        n_title += c2
        text, c3 = fix_fffd(text)
        n_fffd += c3

        if text != original:
            p.write_text(text, encoding='utf-8')
            n_files += 1

    print(f'Files updated: {n_files}')
    print(f'  Chapter-label fixes: {n_chap}')
    print(f'  Section-title fixes: {n_title}')
    print(f'  U+FFFD removed: {n_fffd}')


if __name__ == '__main__':
    main()
