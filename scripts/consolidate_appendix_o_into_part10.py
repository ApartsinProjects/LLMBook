"""Consolidate Appendix O (Docker and Containers) into Part 10, Chapter 62.

Container content sits topically between Production Engineering reliability
patterns (62.6) and Kubernetes-Native LLM Operations (62.7).

Plan:
  - Rename the existing 62.7 (Kubernetes) to 62.11 (sit at end of the chapter)
  - Move Appendix O sections o.1-o.4 to Part 10 / Chapter 62 / sections 62.7-62.10:
      o.1 (Docker Fundamentals)                     -> 62.7
      o.2 (Writing Dockerfiles for ML)              -> 62.8
      o.3 (Docker Compose for Multi-Service Apps)   -> 62.9
      o.4 (Containerizing LLM Inference Servers)    -> 62.10
  - Rewrite each moved file's chapter/section numbers, breadcrumbs, page-current,
    title, meta description, anchor IDs (was o-X-Y, becomes 62-Z-Y).
  - Delete the appendix-o directory.
  - Rewrite cross-refs from appendix-o-docker-containers/section-o.X.html ->
    part-10-llmops/module-62-production-engineering-core/section-62.Y.html.
  - Remove Appendix O entry from toc.html and appendices/index.html.
  - Update Part 10 / Chapter 62 / part-10-llmops indexes.
"""
from __future__ import annotations
import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APPENDIX_DIR = ROOT / 'appendices' / 'appendix-o-docker-containers'
TARGET_DIR = ROOT / 'part-10-llmops' / 'module-62-production-engineering-core'

# (appendix_section_letter, appendix_section_y, new_y_in_ch62)
MOVES = [
    ('o', 1, 7),   # 62.7 Containerization Fundamentals (Docker)
    ('o', 2, 8),   # 62.8 Writing Dockerfiles
    ('o', 3, 9),   # 62.9 Docker Compose
    ('o', 4, 10),  # 62.10 Containerizing Inference Servers
]
EXISTING_K8S_SHIFT = (7, 11)  # 62.7 (K8s) -> 62.11

SKIP_DIRS = {"node_modules", ".git", "KDP", "build", "temp_ebook", "temp_epub",
             "source_fix_backups", "pagefind", "templates", ".claude",
             ".book-update", "vendor", "docs"}


def git_mv(src, dst):
    r = subprocess.run(['git', 'mv', str(src), str(dst)],
                       cwd=ROOT, capture_output=True, text=True)
    return r.returncode == 0


def git_rm(p):
    r = subprocess.run(['git', 'rm', '-rf', str(p)],
                       cwd=ROOT, capture_output=True, text=True)
    return r.returncode == 0


def rewrite_appendix_to_section(text, new_y):
    """Rewrite an appendix-O section's in-file metadata to match a Part-10/Ch-62/X section."""
    new_label = f'62.{new_y}'
    # Title tag
    text = re.sub(
        r'<title>Section O\.(\d+):',
        f'<title>Section {new_label}:',
        text
    )
    # Meta description prefix
    text = re.sub(
        r'(<meta content=")Section O\.(\d+):',
        rf'\1Section {new_label}:',
        text
    )
    # Page breadcrumb
    text = re.sub(
        r'<div class="page-breadcrumb"[^>]*>[\s\S]*?</div>',
        '<div class="page-breadcrumb" data-pagefind-meta="chapter">'
        '<a href="../index.html">Part X: LLM Operations and Production Infrastructure</a>'
        '<span class="bc-sep">›</span>'
        '<a href="index.html">Chapter 62: Production Engineering Core</a>'
        f'<span class="bc-sep">›</span>'
        f'<span class="bc-current">Section {new_label}</span>'
        '</div>',
        text,
        count=1
    )
    # page-current
    text = re.sub(
        r'<div class="page-current">Section [^<]+</div>',
        f'<div class="page-current">Section {new_label}</div>',
        text
    )
    # pagefind-meta-injected part/chapter
    text = re.sub(
        r'<span class="pagefind-meta-injected" data-pagefind-meta="part:[^"]*"[^>]*></span>',
        '<span class="pagefind-meta-injected" data-pagefind-meta="part:Part X: LLM Operations and Production Infrastructure" hidden=""></span>',
        text
    )
    text = re.sub(
        r'<span class="pagefind-meta-injected" data-pagefind-meta="chapter:[^"]*"[^>]*></span>',
        '<span class="pagefind-meta-injected" data-pagefind-meta="chapter:Chapter 62: Production Engineering Core" hidden=""></span>',
        text
    )
    # Anchor IDs: id="o-X-Y-..." -> id="62-Z-Y-..."
    text = re.sub(r'\bid="o-(\d+)-', lambda m: f'id="62-{new_y}-' if int(m.group(1)) == new_y or True else m.group(0), text)
    # Note: above will rewrite ALL o-X-Y where Y is any number, into 62-{new_y}-...
    # But the source section's H2 ids start with o-{src_y}-Z, so we want o-{src_y}-Z -> 62-{new_y}-Z.
    # The regex above doesn't differentiate src_y. Fix:
    return text


def rewrite_one_appendix_section(text, src_y, new_y):
    """Properly rewrite an appendix-O section file when moving to ch 62.new_y."""
    new_label = f'62.{new_y}'
    # Title
    text = re.sub(r'<title>Section O\.\d+:', f'<title>Section {new_label}:', text)
    # Meta
    text = re.sub(r'(<meta content=")Section O\.\d+:', rf'\1Section {new_label}:', text)
    # Page breadcrumb
    text = re.sub(
        r'<div class="page-breadcrumb"[^>]*>[\s\S]*?</div>',
        '<div class="page-breadcrumb" data-pagefind-meta="chapter">'
        '<a href="../index.html">Part X: LLM Operations and Production Infrastructure</a>'
        '<span class="bc-sep">›</span>'
        '<a href="index.html">Chapter 62: Production Engineering Core</a>'
        '<span class="bc-sep">›</span>'
        f'<span class="bc-current">Section {new_label}</span>'
        '</div>',
        text, count=1
    )
    # page-current
    text = re.sub(
        r'<div class="page-current">Section [^<]+</div>',
        f'<div class="page-current">Section {new_label}</div>',
        text
    )
    # pagefind meta
    text = re.sub(
        r'<span class="pagefind-meta-injected" data-pagefind-meta="part:[^"]*"[^>]*></span>',
        '<span class="pagefind-meta-injected" data-pagefind-meta="part:Part X: LLM Operations and Production Infrastructure" hidden=""></span>',
        text
    )
    text = re.sub(
        r'<span class="pagefind-meta-injected" data-pagefind-meta="chapter:[^"]*"[^>]*></span>',
        '<span class="pagefind-meta-injected" data-pagefind-meta="chapter:Chapter 62: Production Engineering Core" hidden=""></span>',
        text
    )
    # Anchor IDs: id="o-{src_y}-Z-..." -> id="62-{new_y}-Z-..."
    text = re.sub(
        rf'\bid="o-{src_y}-(\d+)-',
        rf'id="62-{new_y}-\1-',
        text
    )
    text = re.sub(
        rf'\bhref="#o-{src_y}-(\d+)-',
        rf'href="#62-{new_y}-\1-',
        text
    )
    # Inline body refs like "Section O.X" -> "Section 62.Y"
    text = re.sub(rf'\bSection O\.{src_y}\b', f'Section {new_label}', text)
    text = re.sub(rf'\bO\.{src_y}\.(\d+)\b', rf'{new_label}.\1', text)
    # Stylesheet/script paths: appendices/appendix-o-docker-containers depth is "../../styles" same as part-10-llmops/module-62.
    # No change needed there because both are 2 levels deep.
    # Within-file CSS class names / styling untouched.
    return text


def move_sections(dry_run):
    """Move appendix-O section files to ch 62. Shift existing 62.7 -> 62.11 first."""
    # Step 1: rename existing 62.7 -> 62.11 (via .tmp)
    src_k8s = TARGET_DIR / f'section-62.{EXISTING_K8S_SHIFT[0]}.html'
    tmp_k8s = TARGET_DIR / f'section-62.{EXISTING_K8S_SHIFT[1]}.html.__tmp__'
    dst_k8s = TARGET_DIR / f'section-62.{EXISTING_K8S_SHIFT[1]}.html'
    if src_k8s.exists() and not dst_k8s.exists():
        if dry_run:
            print(f'  [dry] would mv {src_k8s.name} -> {dst_k8s.name}')
        else:
            git_mv(src_k8s, tmp_k8s)
            git_mv(tmp_k8s, dst_k8s)
            # rewrite in-file metadata
            t = dst_k8s.read_text(encoding='utf-8')
            new_label = f'62.{EXISTING_K8S_SHIFT[1]}'
            t = re.sub(r'<title>Section 62\.\d+:', f'<title>Section {new_label}:', t)
            t = re.sub(r'(<meta content=")Section 62\.\d+:', rf'\1Section {new_label}:', t)
            t = re.sub(r'<div class="page-current">Section [^<]+</div>',
                       f'<div class="page-current">Section {new_label}</div>', t)
            t = re.sub(r'<span class="bc-current">Section 62\.\d+</span>',
                       f'<span class="bc-current">Section {new_label}</span>', t)
            # anchor IDs: id="62-7-Z-..." -> "62-11-Z-..."
            t = re.sub(r'\bid="62-7-(\d+)-', r'id="62-11-\1-', t)
            t = re.sub(r'\bhref="#62-7-(\d+)-', r'href="#62-11-\1-', t)
            # body refs Section 62.7 -> 62.11
            t = re.sub(r'\bSection 62\.7\b', 'Section 62.11', t)
            t = re.sub(r'\b62\.7\.(\d+)\b', r'62.11.\1', t)
            dst_k8s.write_text(t, encoding='utf-8')
            print(f'  Shifted: section-62.7.html -> section-62.11.html (K8s)')

    # Step 2: move appendix-o sections to ch 62 slots
    for letter, src_y, new_y in MOVES:
        src = APPENDIX_DIR / f'section-{letter}.{src_y}.html'
        dst = TARGET_DIR / f'section-62.{new_y}.html'
        if not src.exists():
            print(f'  SKIP: {src} missing')
            continue
        if dst.exists():
            print(f'  SKIP: {dst} already exists')
            continue
        if dry_run:
            print(f'  [dry] move {src.name} -> {dst.name}')
        else:
            git_mv(src, dst)
            # rewrite in-file metadata
            t = dst.read_text(encoding='utf-8')
            t = rewrite_one_appendix_section(t, src_y, new_y)
            dst.write_text(t, encoding='utf-8')
            print(f'  Moved: {src.name} -> {dst.name}')


def rewrite_external_refs(dry_run):
    """Rewrite all hrefs pointing at appendix-o-docker-containers/section-o.X.html
    to part-10-llmops/module-62-production-engineering-core/section-62.Y.html.
    """
    mapping = {}
    for letter, src_y, new_y in MOVES:
        old_path = f'appendices/appendix-o-docker-containers/section-{letter}.{src_y}.html'
        new_path = f'part-10-llmops/module-62-production-engineering-core/section-62.{new_y}.html'
        mapping[old_path] = new_path
    # Also the appendix index
    mapping['appendices/appendix-o-docker-containers/index.html'] = \
        'part-10-llmops/module-62-production-engineering-core/section-62.7.html'

    n_files = 0
    for p in sorted(ROOT.rglob('*.html')):
        if set(p.parts) & SKIP_DIRS: continue
        text = p.read_text(encoding='utf-8')
        orig = text

        def fix(m):
            href = m.group(1)
            for old, new in mapping.items():
                if href.endswith(old):
                    prefix = href[:-len(old)]
                    return f'href="{prefix}{new}"'
            return m.group(0)

        text = re.sub(r'href="([^"]+)"', fix, text)
        if text != orig:
            if not dry_run:
                p.write_text(text, encoding='utf-8')
            n_files += 1
    print(f'  Rewrote ext refs in {n_files} files')


def remove_appendix(dry_run):
    if APPENDIX_DIR.exists():
        if dry_run:
            print(f'  [dry] would git rm -rf {APPENDIX_DIR}')
        else:
            git_rm(APPENDIX_DIR)
            print(f'  Deleted {APPENDIX_DIR.name}')


def update_toc(dry_run):
    """Remove Appendix O entry + heading from toc.html."""
    toc = ROOT / 'toc.html'
    text = toc.read_text(encoding='utf-8')
    orig = text
    # Remove the <li class="toc-chapter toc-appendix"> for Appendix O
    text = re.sub(
        r'<li class="toc-chapter toc-appendix">\s*'
        r'<a [^>]*>\s*'
        r'<span class="toc-chapter-num"[^>]*>O</span>[\s\S]*?'
        r'</a>\s*</li>\s*',
        '', text
    )
    # Remove the "Production Infrastructure" group divider (was the only entry under it)
    text = re.sub(
        r'<li class="toc-group-divider">\s*<a [^>]*>Production Infrastructure</a>\s*</li>\s*',
        '', text
    )
    if text != orig and not dry_run:
        toc.write_text(text, encoding='utf-8')
    print(f'  toc.html updated: {orig != text}')


def update_appendices_index(dry_run):
    """Remove Appendix O chapter-card + Production Infrastructure h2 from appendices/index.html."""
    idx = ROOT / 'appendices' / 'index.html'
    text = idx.read_text(encoding='utf-8')
    orig = text
    # Remove the Appendix O chapter-card
    text = re.sub(
        r'<div class="chapter-card">\s*'
        r'<div class="chapter-card-header">\s*'
        r'<span class="mod-num">Appendix O</span>[^<]*'
        r'</div>\s*'
        r'<div class="chapter-card-body">[\s\S]*?</div>\s*'
        r'</div>\s*',
        '', text
    )
    # Remove the Production Infrastructure h2 if it's now empty
    text = re.sub(
        r'<h2 id="group-production-infrastructure">[^<]+</h2>\s*'
        r'(?=<h2|</main>)',
        '', text
    )
    if text != orig and not dry_run:
        idx.write_text(text, encoding='utf-8')
    print(f'  appendices/index.html updated: {orig != text}')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--apply', action='store_true')
    args = ap.parse_args()
    dry_run = not args.apply
    if dry_run:
        print('(DRY-RUN; pass --apply to execute)\n')

    print('=== Move section files ===')
    move_sections(dry_run)
    print('\n=== Rewrite external refs ===')
    rewrite_external_refs(dry_run)
    print('\n=== Update toc.html ===')
    update_toc(dry_run)
    print('\n=== Update appendices/index.html ===')
    update_appendices_index(dry_run)
    print('\n=== Remove appendix directory ===')
    remove_appendix(dry_run)


if __name__ == '__main__':
    sys.exit(main())
