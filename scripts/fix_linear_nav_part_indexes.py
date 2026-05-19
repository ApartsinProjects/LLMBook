"""Fix part-index 'next' to point to the FIRST CHAPTER of THIS part
(not to the next part). Linear-navigation rule:
  part-N index -> first chapter of part-N
  chapter-N index -> first section of chapter-N
  section -> next section (or next chapter's first section at boundary)
  part-N's last section -> first chapter of part-N+1
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def part_dirs():
    parts = [p for p in ROOT.iterdir()
             if p.is_dir() and p.name.startswith('part-')]
    # Sort by numeric part number
    def n(p):
        m = re.match(r'^part-(\d+)-', p.name)
        return int(m.group(1)) if m else 0
    return sorted(parts, key=n)


def first_module_dir(part_dir):
    mods = sorted([m for m in part_dir.iterdir()
                   if m.is_dir() and m.name.startswith('module-')],
                  key=lambda d: int(re.match(r'^module-(\d+)', d.name).group(1)))
    return mods[0] if mods else None


def chapter_title(module_dir):
    idx = module_dir / 'index.html'
    if not idx.exists():
        return module_dir.name
    text = idx.read_text(encoding='utf-8', errors='replace')
    m = re.search(r'<h1[^>]*>([^<]+)</h1>', text)
    return m.group(1).strip() if m else module_dir.name


def main():
    apply = '--apply' in sys.argv
    print(f"{'APPLY' if apply else 'DRY-RUN'}")
    parts = part_dirs()
    fixes = 0
    for part_dir in parts:
        idx_path = part_dir / 'index.html'
        if not idx_path.exists():
            continue
        text = idx_path.read_text(encoding='utf-8')
        # Find first chapter
        first_mod = first_module_dir(part_dir)
        if not first_mod:
            continue
        mod_num_m = re.match(r'^module-(\d+)-', first_mod.name)
        chap_num = mod_num_m.group(1) if mod_num_m else "?"
        chap_title = chapter_title(first_mod)
        new_href = f'{first_mod.name}/index.html'
        new_text_block = f'<a class="next" href="{new_href}"><span class="nav-label">Next</span><span class="nav-num">Chapter {chap_num}</span><span class="nav-title">{chap_title}</span></a>'
        # Replace existing next anchor (or add if missing)
        next_re = re.compile(
            r'<a\s+class="next"[^>]*?href="[^"]+"[^>]*>.*?</a>',
            re.DOTALL,
        )
        new_text, n = next_re.subn(new_text_block, text)
        if n == 0:
            # No next anchor — insert before </nav>
            new_text = text.replace('</nav>', new_text_block + '\n</nav>', 1)
            if new_text != text:
                n = 1
        if n:
            fixes += 1
            old_match = next_re.search(text)
            old_href = re.search(r'href="([^"]+)"', old_match.group(0)).group(1) if old_match else '(none)'
            print(f'  {part_dir.name}/index.html: next "{old_href}" -> "{new_href}"')
            if apply:
                idx_path.write_text(new_text, encoding='utf-8')
    print(f'\nTotal part-index next links fixed: {fixes}')


if __name__ == '__main__':
    main()
