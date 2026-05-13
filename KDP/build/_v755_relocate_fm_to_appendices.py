"""Relocate 3 more FM pages to the Cross-Cutting Reference Catalogs
appendix group, matching the AD/AE/AF precedent.

  fm-problem-solution-key.html  -> appendix-ag-problem-solution-key/index.html
  fm-conceptual-map.html        -> appendix-ah-conceptual-map/index.html
  fm-freshness-2026.html        -> appendix-ai-freshness-2026/index.html

After this move, FM contains only the 9 reader-orientation pages it
should hold; everything reference-shaped lives in the Appendices.

Mirrors v751 mechanics:
  1. Create new dirs, move files.
  2. Adjust relative-path depth (front-matter is depth 1, appendix is
     depth 2 = +1 ../ per relative ref).
  3. Fix <title> tag prefix.
  4. Update part-label / chapter-label breadcrumbs.
  5. Book-wide sweep of inbound refs (HTML + JSON).
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
FM = ROOT / 'front-matter'
SKIP = ('node_modules', '.git/', 'pagefind/', 'KDP/output/',
        'templates/', '_archive/', 'temp_epub/', 'vendor/', '/agents/')

MOVES = [
    ('front-matter/fm-problem-solution-key.html',
     'appendices/appendix-ag-problem-solution-key/index.html',
     'Appendix AG: Problem-Solution Key',
     'Appendices',
     'Appendix AG'),
    ('front-matter/fm-conceptual-map.html',
     'appendices/appendix-ah-conceptual-map/index.html',
     'Appendix AH: Conceptual Map of This Book',
     'Appendices',
     'Appendix AH'),
    ('front-matter/fm-freshness-2026.html',
     'appendices/appendix-ai-freshness-2026/index.html',
     'Appendix AI: 2026 Freshness Index',
     'Appendices',
     'Appendix AI'),
]


def adjust_relative_links(html: str) -> str:
    """front-matter (depth 1) -> appendix (depth 2): every relative
    href/src needs one more '../'. Same-dir 'foreword.html' becomes
    '../front-matter/foreword.html'."""
    def fix_attr(m: re.Match) -> str:
        attr_name = m.group(1)
        url = m.group(2)
        if url.startswith(('http://', 'https://', '#', 'mailto:', '/')):
            return m.group(0)
        if url.startswith('javascript:') or url.startswith('data:'):
            return m.group(0)
        if url.startswith('../'):
            return f'{attr_name}="../{url}"'
        return f'{attr_name}="../front-matter/{url}"'
    return re.sub(r'(href|src)="([^"]+)"', fix_attr, html)


def fix_title(html: str, new_prefix: str) -> str:
    suffix = ' | Building Conversational AI with LLMs and Agents'
    return re.sub(r'<title>[^<]*</title>',
                  f'<title>{new_prefix}{suffix}</title>',
                  html, count=1)


def fix_breadcrumbs(html: str, part: str, chapter: str) -> str:
    html = re.sub(r'(<div class="part-label"[^>]*>)[\s\S]*?(</div>)',
                  rf'\1{part}\2', html, count=1)
    html = re.sub(r'(<div class="chapter-label"[^>]*>)[\s\S]*?(</div>)',
                  rf'\1{chapter}\2', html, count=1)
    return html


def move_file(old_rel, new_rel, title_prefix, breadcrumb_part, breadcrumb_chapter, fix):
    old_path = ROOT / old_rel
    new_path = ROOT / new_rel
    if not old_path.exists() and new_path.exists():
        print(f'  = already moved: {old_rel}')
        return True
    if not old_path.exists():
        print(f'  ! missing: {old_rel}')
        return False
    if new_path.exists():
        print(f'  ! collision: {new_rel} already exists')
        return False
    text = old_path.read_text(encoding='utf-8')
    text = adjust_relative_links(text)
    text = fix_title(text, title_prefix)
    text = fix_breadcrumbs(text, breadcrumb_part, breadcrumb_chapter)
    print(f'  + {old_rel} -> {new_rel}')
    if fix:
        new_path.parent.mkdir(parents=True, exist_ok=True)
        new_path.write_text(text, encoding='utf-8')
        old_path.unlink()
    return True


def sweep_references(fix):
    sub_map = {old: new for old, new, *_ in MOVES}
    files_touched = 0
    total_subs = 0
    for p in sorted(ROOT.rglob('*.html')):
        sp = str(p).replace('\\', '/')
        if any(s in sp for s in SKIP):
            continue
        try:
            text = p.read_text(encoding='utf-8', errors='replace')
        except Exception:
            continue
        new_text = text
        for old_rel, new_rel in sub_map.items():
            if old_rel in new_text:
                new_text = new_text.replace(old_rel, new_rel)
            old_name = old_rel.rsplit('/', 1)[-1]
            new_full_rel_from_fm = '../' + new_rel
            new_text = re.sub(
                rf'(href|src)="{re.escape(old_name)}"',
                rf'\1="{new_full_rel_from_fm}"',
                new_text)
        if new_text != text:
            files_touched += 1
            total_subs += sum(text.count(o) for o in sub_map)
            if fix:
                p.write_text(new_text, encoding='utf-8')
    for p in sorted(ROOT.rglob('*.json')):
        sp = str(p).replace('\\', '/')
        if any(s in sp for s in SKIP):
            continue
        try:
            text = p.read_text(encoding='utf-8', errors='replace')
        except Exception:
            continue
        new_text = text
        for old_rel, new_rel in sub_map.items():
            if old_rel in new_text:
                new_text = new_text.replace(old_rel, new_rel)
        if new_text != text:
            files_touched += 1
            total_subs += sum(text.count(o) for o in sub_map)
            if fix:
                p.write_text(new_text, encoding='utf-8')
    return files_touched, total_subs


def main():
    fix = '--fix' in sys.argv
    print('=== File moves ===')
    for move in MOVES:
        move_file(*move, fix=fix)
    print('\n=== Reference sweep ===')
    files, subs = sweep_references(fix=fix)
    print(f'[{"APPLIED" if fix else "DRY-RUN"}] {files} files, {subs} substitutions')
    if not fix:
        print('Re-run with --fix to apply.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
