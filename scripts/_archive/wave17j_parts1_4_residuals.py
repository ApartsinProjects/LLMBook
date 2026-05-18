"""Wave 17j: address residual cycle-3 findings for parts 1-4 (mechanical sweeps).

Per cycle-3 audit for parts 1-4:
1. Part-overview prose has stale chapter range: "Chapters: 7 (Chapters 0 through 6)"
   for Part I — fix to "Chapters: 6 (Chapters 0 through 5)"
2. Module-index <title> tags zero-padded with old numbers
3. Module-17 section files still say "Chapter 17: PEFT" (Wave 15 rename only got the
   chapter index, not the section files)
4. Section 6.9 duplicated in part-2 + module-06 indexes
5. Chapter-opener <figcaption> figures (Figure 5.0.1 etc.) use old chapter numbers
6. Non-href "Chapter XX" / "Section X.Y" mentions in looking-back / overview blocks
   that Wave 17d couldn't anchor on.
"""
from pathlib import Path
import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'.git', 'node_modules', 'KDP', 'build', 'temp_ebook', 'temp_epub',
        'source_fix_backups', 'pagefind', 'templates', '.claude',
        '.book-update', 'vendor', 'docs'}


def fix_part_overview_ranges():
    """Fix stale chapter range in part-N/index.html overview prose."""
    print('=== Fix 1: part-overview chapter ranges ===')
    fixes = {
        'part-1-llm-building-blocks': ('Chapters: 7 (Chapters 0 through 6)', 'Chapters: 6 (Chapters 0 through 5)'),
        'part-2-understanding-llms': ('Chapters: 6 (Chapters 7 through 12)', 'Chapters: 5 (Chapters 6 through 10)'),
        'part-3-working-with-llms': ('Chapters: 4 (Chapters 13 through 16)', 'Chapters: 4 (Chapters 11 through 14)'),
        'part-4-training-adaptation': ('Chapters: 5 (Chapters 17 through 21)', 'Chapters: 5 (Chapters 15 through 19)'),
    }
    for slug, (old, new) in fixes.items():
        p = ROOT / slug / 'index.html'
        if not p.exists():
            continue
        t = p.read_text(encoding='utf-8')
        if old in t:
            t = t.replace(old, new)
            p.write_text(t, encoding='utf-8')
            print(f'  Fixed {slug}/index.html')


def fix_module_index_titles():
    """Fix zero-padded module <title> tags with old numbers."""
    print('=== Fix 2: module-index <title> tags ===')
    # Walk each module dir; the <title> should match the actual chapter number
    # extracted from module-NN-slug
    n = 0
    for mod_dir in sorted(ROOT.rglob('module-*-*')):
        if not mod_dir.is_dir() or (set(mod_dir.parts) & SKIP):
            continue
        m = re.match(r'module-(\d+)-', mod_dir.name)
        if not m:
            continue
        ch_num = int(m.group(1))
        idx = mod_dir / 'index.html'
        if not idx.exists():
            continue
        text = idx.read_text(encoding='utf-8')
        orig = text
        # Fix <title>Chapter ZZ: ...</title> if ZZ != ch_num
        text = re.sub(
            r'<title>Chapter \d+:',
            f'<title>Chapter {ch_num}:',
            text
        )
        # Fix meta description
        text = re.sub(
            r'(<meta content=")Chapter \d+:',
            rf'\1Chapter {ch_num}:',
            text
        )
        # Fix breadcrumb current "Chapter ZZ" if != ch_num
        text = re.sub(
            r'<span class="bc-current">Chapter \d+</span>',
            f'<span class="bc-current">Chapter {ch_num}</span>',
            text
        )
        if text != orig:
            idx.write_text(text, encoding='utf-8')
            n += 1
    print(f'  Updated {n} module-index titles')


def fix_chapter_opener_figcaptions():
    """Fix chapter-opener <figcaption>Figure X.0.1 numbers to current chapter."""
    print('=== Fix 3: chapter-opener figcaptions ===')
    n = 0
    for mod_dir in sorted(ROOT.rglob('module-*-*')):
        if not mod_dir.is_dir() or (set(mod_dir.parts) & SKIP):
            continue
        m = re.match(r'module-(\d+)-', mod_dir.name)
        if not m:
            continue
        ch_num = int(m.group(1))
        idx = mod_dir / 'index.html'
        if not idx.exists():
            continue
        text = idx.read_text(encoding='utf-8')
        orig = text
        # Fix "Figure X.0.1" where X != ch_num to "Figure ch_num.0.1"
        text = re.sub(
            r'<strong>Figure \d+\.0\.1</strong>',
            f'<strong>Figure {ch_num}.0.1</strong>',
            text
        )
        if text != orig:
            idx.write_text(text, encoding='utf-8')
            n += 1
    print(f'  Updated {n} chapter-opener figcaptions')


def fix_module17_section_breadcrumbs():
    """Module-17 section files should say 'Chapter 17: Parameter-Efficient Fine-Tuning,
    Distillation & Model Merging' (the new title from Wave 15). They still say '(PEFT)'."""
    print('=== Fix 4: module-17 section breadcrumbs (PEFT rename propagation) ===')
    mod_dir = ROOT / 'part-4-training-adaptation' / 'module-17-peft'
    n = 0
    for f in sorted(mod_dir.glob('section-*.html')):
        text = f.read_text(encoding='utf-8')
        orig = text
        text = text.replace(
            'Chapter 17: Parameter-Efficient Fine-Tuning (PEFT)',
            'Chapter 17: Parameter-Efficient Fine-Tuning, Distillation &amp; Model Merging'
        )
        text = text.replace(
            'chapter:Chapter 17: Parameter-Efficient Fine-Tuning (PEFT)',
            'chapter:Chapter 17: Parameter-Efficient Fine-Tuning, Distillation &amp; Model Merging'
        )
        # Also fix nav-title in chapter-nav
        text = re.sub(
            r'<span class="nav-title">Parameter-Efficient Fine-Tuning \(PEFT\)</span>',
            '<span class="nav-title">Parameter-Efficient Fine-Tuning, Distillation &amp; Model Merging</span>',
            text
        )
        if text != orig:
            f.write_text(text, encoding='utf-8')
            n += 1
    print(f'  Updated {n} module-17 section files')


def fix_part2_module06_dup_section69():
    """Section 6.9 was reported as duplicated in part-2 and module-06 indexes.
    The fix is to remove the orphan duplicate card from module-06's index if present."""
    print('=== Fix 5: section 6.9 duplicate ===')
    # Wave 17e should have rebuilt module-06 index from filesystem.
    # Verify it now has only one 6.9 entry.
    p = ROOT / 'part-2-understanding-llms' / 'module-06-pretraining-scaling-laws' / 'index.html'
    if not p.exists():
        return
    text = p.read_text(encoding='utf-8')
    count = text.count('href="section-6.9.html"')
    if count > 1:
        # Strip duplicates beyond the first occurrence in sections-list
        # Find the section-grid block (if present) and remove it (the typical second-occurrence pattern)
        text2 = re.sub(
            r'<div class="section-grid">[\s\S]*?</div>\s*',
            '',
            text,
            count=1
        )
        if text2 != text:
            p.write_text(text2, encoding='utf-8')
            print('  Removed duplicate 6.9 card from module-06 index')


def main():
    fix_part_overview_ranges()
    fix_module_index_titles()
    fix_chapter_opener_figcaptions()
    fix_module17_section_breadcrumbs()
    fix_part2_module06_dup_section69()


if __name__ == '__main__':
    main()
