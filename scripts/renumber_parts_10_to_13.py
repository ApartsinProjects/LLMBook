"""Canonical renumbering for Parts 10-13 modules.

Part 9 ends at chapter 60. Continue the sequence:
  Part 10 LLMOps          -> chapters 61-62
  Part 11 Designing       -> chapters 63-71
  Part 12 Applications    -> chapters 72-81
  Part 13 Frontiers       -> chapters 82-86

For each module:
  1. git mv module-{old}-{name} -> module-{new}-{name}
  2. git mv section-{old}.{X}.html -> section-{new}.{X}.html (inside dir)
  3. Rewrite in-file: chapter num spans, breadcrumbs, headings, body anchors
  4. Cross-file href rewrites across the whole book
"""
from __future__ import annotations
import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# (part_slug, old_module_name, new_module_name, old_ch, new_ch)
RENAMES = [
    ('part-10-llmops', 'module-50-compute-planning', 'module-61-compute-planning', 50, 61),
    ('part-10-llmops', 'module-53-production-engineering-core', 'module-62-production-engineering-core', 53, 62),
    ('part-11-designing-llm-products', 'module-58-ideation', 'module-63-ideation', 58, 63),
    ('part-11-designing-llm-products', 'module-59-product-management', 'module-64-product-management', 59, 64),
    ('part-11-designing-llm-products', 'module-60-strategy-prioritization', 'module-65-strategy-prioritization', 60, 65),
    ('part-11-designing-llm-products', 'module-61-vibe-coding', 'module-66-vibe-coding', 61, 66),
    ('part-11-designing-llm-products', 'module-62-mvp', 'module-67-mvp', 62, 67),
    ('part-11-designing-llm-products', 'module-63-prototype-to-production', 'module-68-prototype-to-production', 63, 68),
    ('part-11-designing-llm-products', 'module-64-llm-economics', 'module-69-llm-economics', 64, 69),
    ('part-11-designing-llm-products', 'module-65-shipping-products', 'module-70-shipping-products', 65, 70),
    ('part-11-designing-llm-products', 'module-66-tools-of-the-trade', 'module-71-tools-of-the-trade', 66, 71),
    ('part-12-applications-across-industries', 'module-51-legal-llms', 'module-72-legal-llms', 51, 72),
    ('part-12-applications-across-industries', 'module-52-finance-llms', 'module-73-finance-llms', 52, 73),
    ('part-12-applications-across-industries', 'module-53-healthcare-llms', 'module-74-healthcare-llms', 53, 74),
    ('part-12-applications-across-industries', 'module-54-education-llms', 'module-75-education-llms', 54, 75),
    ('part-12-applications-across-industries', 'module-55-cybersecurity-llms', 'module-76-cybersecurity-llms', 55, 76),
    ('part-12-applications-across-industries', 'module-56-government-llms', 'module-77-government-llms', 56, 77),
    ('part-12-applications-across-industries', 'module-57-manufacturing-llms', 'module-78-manufacturing-llms', 57, 78),
    ('part-12-applications-across-industries', 'module-58-creative-industries', 'module-79-creative-industries', 58, 79),
    ('part-12-applications-across-industries', 'module-59-recommendation-search', 'module-80-recommendation-search', 59, 80),
    ('part-12-applications-across-industries', 'module-60-tools-of-the-trade', 'module-81-tools-of-the-trade', 60, 81),
    ('part-13-frontiers', 'module-61-frontier-architectures', 'module-82-frontier-architectures', 61, 82),
    ('part-13-frontiers', 'module-62-frontier-theory', 'module-83-frontier-theory', 62, 83),
    ('part-13-frontiers', 'module-63-frontier-systems-hardware', 'module-84-frontier-systems-hardware', 63, 84),
    ('part-13-frontiers', 'module-64-agi-trajectories', 'module-85-agi-trajectories', 64, 85),
    ('part-13-frontiers', 'module-65-tools-of-the-trade', 'module-86-tools-of-the-trade', 65, 86),
]

SKIP_DIRS = {"node_modules", ".git", "KDP", "build", "temp_ebook",
             "temp_epub", "source_fix_backups", "pagefind", "templates",
             ".claude", ".book-update", "vendor", "docs"}


def git_mv(src, dst, dry_run):
    if not src.exists():
        print(f'  SKIP (no src): {src}')
        return False
    if dst.exists():
        print(f'  SKIP (dst exists): {dst}')
        return False
    if not dry_run:
        r = subprocess.run(['git', 'mv', str(src), str(dst)], cwd=ROOT,
                          capture_output=True, text=True)
        if r.returncode != 0:
            print(f'  ERR: {r.stderr}')
            return False
    return True


def step1_rename_module_dirs(dry_run):
    """Move each module dir to its new chapter-numbered name. Use intermediate suffix to avoid clobbering."""
    n_done = 0
    # Pass 1: rename to .tmp suffix to avoid collisions where new num matches another old num
    for part_slug, old_name, new_name, old_ch, new_ch in RENAMES:
        src = ROOT / part_slug / old_name
        tmp = ROOT / part_slug / (new_name + '.__tmp__')
        if git_mv(src, tmp, dry_run):
            n_done += 1
    print(f'  Step 1a (-> .tmp): {n_done} module dirs')

    # Pass 2: rename .tmp -> final name
    n_done2 = 0
    for part_slug, old_name, new_name, old_ch, new_ch in RENAMES:
        tmp = ROOT / part_slug / (new_name + '.__tmp__')
        dst = ROOT / part_slug / new_name
        if git_mv(tmp, dst, dry_run):
            n_done2 += 1
    print(f'  Step 1b (-> final): {n_done2} module dirs')
    return n_done2


def step2_rename_section_files(dry_run):
    """Rename section-{old}.X.html -> section-{new}.X.html inside each renamed module."""
    n_done = 0
    for part_slug, old_name, new_name, old_ch, new_ch in RENAMES:
        mod_dir = ROOT / part_slug / new_name
        if not mod_dir.exists():
            continue
        pat = re.compile(rf'^section-{old_ch}\.(\d+)\.html$')
        for sec in list(mod_dir.glob('section-*.html')):
            m = pat.match(sec.name)
            if not m: continue
            new_path = sec.parent / f'section-{new_ch}.{m.group(1)}.html'
            if new_path.exists(): continue
            if not dry_run:
                r = subprocess.run(['git', 'mv', str(sec), str(new_path)], cwd=ROOT,
                                  capture_output=True, text=True)
                if r.returncode == 0:
                    n_done += 1
            else:
                n_done += 1
    print(f'  Step 2: {n_done} section files renamed')
    return n_done


def step3_rewrite_in_file_content(dry_run):
    """For each renamed section file + chapter index, rewrite in-file chapter/section numbers.

    Patterns to rewrite (only within affected files):
      - <span class="mod-num">Chapter {old}</span> -> Chapter {new}
      - <span class="sec-num">{old}.X</span> -> {new}.X
      - <span class="nav-num">Chapter {old}</span> -> Chapter {new}
      - <span class="nav-num">Section {old}.X</span> -> Section {new}.X
      - <span class="toc-chapter-num">Chapter {old}</span> -> Chapter {new}
      - Chapter {old}: in headings, breadcrumbs
      - <h1>Chapter {old}: -> Chapter {new}:
      - data-pagefind-meta="chapter:Chapter {old}: ... -> Chapter {new}:
      - Section {old}.X anywhere
      - id="{old}-X-..." anchors
      - section-{old}.X.html -> section-{new}.X.html (in-file refs)
    """
    n_files = 0
    n_subs = 0
    for part_slug, old_name, new_name, old_ch, new_ch in RENAMES:
        mod_dir = ROOT / part_slug / new_name
        if not mod_dir.exists():
            continue
        for f in list(mod_dir.glob('*.html')):
            text = f.read_text(encoding='utf-8')
            orig = text
            # In-file section refs (same dir)
            text = re.sub(rf'\bsection-{old_ch}\.(\d+)\.html\b',
                         rf'section-{new_ch}.\1.html', text)
            # Chapter num
            text = re.sub(rf'\bChapter {old_ch}(?!\d)', f'Chapter {new_ch}', text)
            # Section X.Y in various contexts
            text = re.sub(rf'\bSection {old_ch}\.(\d+)\b', rf'Section {new_ch}.\1', text)
            # Bare X.Y numbers in spans (sec-num, toc-sec-num)
            text = re.sub(rf'(<span class="(?:sec-num|toc-sec-num|nav-num|section-num)"[^>]*>){old_ch}\.(\d+)(</span>)',
                         rf'\g<1>{new_ch}.\2\3', text)
            # mod-num span content
            text = re.sub(rf'(<span class="mod-num"[^>]*>Chapter ){old_ch}(</span>)',
                         rf'\g<1>{new_ch}\2', text)
            # id="X-Y-..." -> "newch-Y-..."
            text = re.sub(rf'\bid="{old_ch}-(\d+)-', rf'id="{new_ch}-\1-', text)
            # href="#X-Y-..." anchor refs
            text = re.sub(rf'href="#{old_ch}-(\d+)-', rf'href="#{new_ch}-\1-', text)
            if text != orig:
                n_subs += sum(1 for _ in re.finditer(r'.', orig)) - sum(1 for _ in re.finditer(r'.', text))
                if not dry_run:
                    f.write_text(text, encoding='utf-8')
                n_files += 1
    print(f'  Step 3: {n_files} in-file content updates')
    return n_files


def step4_cross_file_href_rewrite(dry_run):
    """Walk every HTML in the book; rewrite hrefs from old paths to new paths."""
    # Build path mapping: old href fragment -> new href fragment
    # Patterns:
    #   module-{old_num}-{name}/index.html -> module-{new_num}-{name}/index.html
    #   module-{old_num}-{name}/section-{old_num}.X.html -> module-{new_num}-{name}/section-{new_num}.X.html
    mapping = {}
    for part_slug, old_name, new_name, old_ch, new_ch in RENAMES:
        # Full dir paths
        mapping[f'{part_slug}/{old_name}/'] = f'{part_slug}/{new_name}/'
        # And within-part paths (just module name)
        mapping[f'/{old_name}/'] = f'/{new_name}/'
        # Section files within those modules
        mod_dir = ROOT / part_slug / new_name
        if mod_dir.exists():
            for sec in mod_dir.glob('section-*.html'):
                m = re.match(rf'section-{new_ch}\.(\d+)\.html', sec.name)
                if m:
                    y = m.group(1)
                    old_sec = f'section-{old_ch}.{y}.html'
                    new_sec = sec.name
                    mapping[f'{old_name}/{old_sec}'] = f'{new_name}/{new_sec}'

    n_files = 0
    n_subs = 0
    for p in sorted(ROOT.rglob('*.html')):
        if set(p.parts) & SKIP_DIRS:
            continue
        text = p.read_text(encoding='utf-8')
        orig = text
        for old_frag, new_frag in mapping.items():
            text = text.replace(old_frag, new_frag)
            n_subs += orig.count(old_frag)
        if text != orig:
            if not dry_run:
                p.write_text(text, encoding='utf-8')
            n_files += 1
    print(f'  Step 4: {n_files} files had cross-refs rewritten')
    return n_files


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--apply', action='store_true')
    args = ap.parse_args()
    dry_run = not args.apply
    print(f'=== Parts 10-13 canonical renumbering ===')
    print(f'Renames planned: {len(RENAMES)}')
    if dry_run:
        print('(DRY-RUN; pass --apply to execute)\n')

    step1_rename_module_dirs(dry_run)
    step2_rename_section_files(dry_run)
    step3_rewrite_in_file_content(dry_run)
    step4_cross_file_href_rewrite(dry_run)
    return 0


if __name__ == '__main__':
    sys.exit(main())
