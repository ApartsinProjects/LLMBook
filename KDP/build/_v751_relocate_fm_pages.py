"""Relocate FM pages to where they structurally belong:
  fm-reference-tables.html    -> appendices/appendix-ad-master-reference-tables/index.html
  fm-production-patterns.html -> appendices/appendix-ae-production-patterns/index.html
  fm-pedagogy-kit.html        -> appendices/appendix-af-pedagogy-kit/index.html
  fm-what-2026-settled.html   -> part-10-frontiers/module-33-emerging-architectures/section-33.11.html

These pages are not "front-matter" by purpose: they are reference
material that readers consult on demand (the appendix model) or
frontier retrospective (the Frontiers chapter model). Moving them
removes the misclassification, frees the FM list to be the actual
reader-orientation pages only, and matches conventional book
architecture (front-matter for orientation, appendices for reference,
chapters for content).

Steps:
1. Create new directories.
2. Copy files to new locations. Adjust internal relative-path links
   (front-matter/... -> appendices/... means depth changes from 1
   level up to 2 levels up for any "../" references).
3. Update <title> tag prefixes.
4. Update page navs (h2, body, prev/next/up).
5. Sweep all *.html and *.json book-wide for the old paths.
6. Delete the old FM files.
"""
from __future__ import annotations
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
FM = ROOT / 'front-matter'

# (old_path_rel_to_root, new_path_rel_to_root, depth_old, depth_new,
#  new_title_prefix, new_breadcrumb_part, new_breadcrumb_chapter)
MOVES = [
    ('front-matter/fm-reference-tables.html',
     'appendices/appendix-ad-master-reference-tables/index.html',
     1, 2,
     'Appendix AD: Master Reference Tables',
     'Appendices',
     'Appendix AD'),
    ('front-matter/fm-production-patterns.html',
     'appendices/appendix-ae-production-patterns/index.html',
     1, 2,
     'Appendix AE: Production Patterns Reference',
     'Appendices',
     'Appendix AE'),
    ('front-matter/fm-pedagogy-kit.html',
     'appendices/appendix-af-pedagogy-kit/index.html',
     1, 2,
     'Appendix AF: Pedagogy Kit',
     'Appendices',
     'Appendix AF'),
    ('front-matter/fm-what-2026-settled.html',
     'part-10-frontiers/module-33-emerging-architectures/section-33.11.html',
     1, 2,
     'Section 33.11: What 2026 Settled',
     'Part X: Frontiers',
     'Chapter 33: Emerging Architectures & Scaling Frontiers'),
]


def adjust_relative_links(html: str, depth_delta: int) -> str:
    """Adjust ../path links by depth_delta levels deeper.
    depth_delta=1 means add one more "../" to every relative ref."""
    if depth_delta == 0:
        return html
    prefix = '../' * depth_delta
    # Update href="../..." and src="../..." that don't start with '..'
    # We want to deepen each relative ref. Easiest: replace 'href="../'
    # with 'href="' + extra '../' (one more level).
    # But also replace 'href="<file>"' (no ../ at all, same-dir links)
    # to add '../' prefix only when leaving the directory.

    # The pages live in front-matter/ at depth 1; they link relatives
    # like href="foreword.html" (same dir) or href="../part-1/...". For
    # depth 2 (appendices/appendix-XX/), same-dir front-matter peers
    # become "../front-matter/peer.html" and cross-dir become "../../".
    # We handle both.

    # For each href/src attribute, prepend '../' if relative.
    def fix_attr(m: re.Match) -> str:
        attr_name = m.group(1)
        url = m.group(2)
        if url.startswith(('http://', 'https://', '#', 'mailto:', '/')):
            return m.group(0)
        if url.startswith('javascript:') or url.startswith('data:'):
            return m.group(0)
        if url.startswith('../'):
            return f'{attr_name}="{prefix}{url}"'
        # Same-dir relative (e.g. "foreword.html") -> prepend
        # "../front-matter/" since the new home is one level deeper
        return f'{attr_name}="{prefix}front-matter/{url}"'

    return re.sub(
        r'(href|src)="([^"]+)"',
        fix_attr,
        html)


def fix_title(html: str, new_prefix: str) -> str:
    suffix = ' | Building Conversational AI with LLMs and Agents'
    return re.sub(
        r'<title>[^<]*</title>',
        f'<title>{new_prefix}{suffix}</title>',
        html,
        count=1)


def fix_breadcrumbs(html: str, part: str, chapter: str) -> str:
    """Replace the 'Front Matter' part-label and chapter-label with new
    breadcrumb anchors. The page's new home is not in front-matter, so
    these need to point at appropriate parents."""
    # Replace data-pagefind-meta="part" and chapter values too.
    html = re.sub(
        r'(<div class="part-label"[^>]*>)[\s\S]*?(</div>)',
        rf'\1{part}\2',
        html, count=1)
    html = re.sub(
        r'(<div class="chapter-label"[^>]*>)[\s\S]*?(</div>)',
        rf'\1{chapter}\2',
        html, count=1)
    return html


def move_file(old_rel: str, new_rel: str, depth_old: int, depth_new: int,
              title_prefix: str, breadcrumb_part: str, breadcrumb_chapter: str,
              fix: bool) -> bool:
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
    # Adjust depth
    depth_delta = depth_new - depth_old
    text = adjust_relative_links(text, depth_delta)
    # Fix title
    text = fix_title(text, title_prefix)
    # Fix breadcrumbs
    text = fix_breadcrumbs(text, breadcrumb_part, breadcrumb_chapter)
    print(f'  + {old_rel} -> {new_rel}')
    if fix:
        new_path.parent.mkdir(parents=True, exist_ok=True)
        new_path.write_text(text, encoding='utf-8')
        old_path.unlink()
    return True


def sweep_references(fix: bool) -> tuple[int, int]:
    """Replace all inbound refs to old paths with new paths."""
    SKIP = ('node_modules', '.git/', 'pagefind/', 'KDP/build/',
            'KDP/output/', 'templates/', '_archive/', 'temp_epub/',
            'vendor/', '/agents/')
    sub_map = {}
    for old_rel, new_rel, *_ in MOVES:
        old_name = old_rel.rsplit('/', 1)[-1]
        # Substitute the LEAF filename references first (any context)
        # since those appear in href="fm-XXX.html" and href="../front-matter/fm-XXX.html"
        # We'll do a more targeted substitution: replace old_rel substring with new_rel
        # AND replace just the bare filename in case of same-dir refs.
        sub_map[old_rel] = new_rel
        # Also substitute the bare filename if appears in href as "front-matter/<file>"
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
            # Also replace bare filename references like
            # href="fm-pedagogy-kit.html" inside front-matter peers
            old_name = old_rel.rsplit('/', 1)[-1]
            new_full_rel_from_fm = '../' + new_rel  # leaves front-matter
            # Only sub when the bare filename appears in href/src context
            # (avoid replacing the same string twice)
            new_text = re.sub(
                rf'(href|src)="{re.escape(old_name)}"',
                rf'\1="{new_full_rel_from_fm}"',
                new_text)
        if new_text != text:
            files_touched += 1
            total_subs += sum(text.count(o) for o in sub_map)
            if fix:
                p.write_text(new_text, encoding='utf-8')
    # JSON too (spine manifest)
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


def main() -> int:
    fix = '--fix' in sys.argv
    print('=== File moves ===')
    for move in MOVES:
        move_file(*move, fix=fix)
    print('\n=== Reference sweep ===')
    files, subs = sweep_references(fix=fix)
    mode = 'APPLIED' if fix else 'DRY-RUN'
    print(f'[{mode}] {files} files, {subs} substitutions')
    if not fix:
        print('\nRe-run with --fix to apply.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
