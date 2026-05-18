"""Apply unlinked cross-references for the cycle-4 agent.

For each candidate finding:
1. Read source HTML
2. Search for the bare text "Section X.Y" or "Chapter NN" in the surrounding context
3. Verify the target path exists on disk
4. Verify the bare text is inside a <p> element (not <pre>, <code>, <nav>)
5. Replace with <a href="...">Section X.Y</a> using class="cross-ref" for cross-chapter

Usage:
  python _apply_xrefs.py --slice <prefix1,prefix2,...> [--dry-run]
"""
import argparse
import json
import os
import re
import sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _xref_resolver import (
    resolve_section,
    resolve_chapter,
    verify_path_exists,
    sections,
    modules,
)

ROOT = r'E:\Projects\BookBlogsHome\LLMBook'


def is_inside_problem_tag(content, start_idx):
    """Check if position start_idx is inside <pre>, <code>, <nav>, or <h1>-<h6>."""
    # Find nearest preceding tag boundaries
    prefix = content[:start_idx]
    # Check if we're inside a <pre>...</pre> or <code>...</code> or <nav>...</nav>
    for tag in ('pre', 'code', 'nav', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
        open_re = re.compile(rf'<{tag}\b[^>]*>', re.IGNORECASE)
        close_re = re.compile(rf'</{tag}\s*>', re.IGNORECASE)
        opens = list(open_re.finditer(prefix))
        if not opens:
            continue
        last_open = opens[-1].end()
        # Find first close after last_open
        m = close_re.search(prefix, last_open)
        if not m or m.end() > start_idx:
            # Check if close is before start_idx in full content
            close_after = close_re.search(content, last_open)
            if not close_after or close_after.start() > start_idx:
                return True
    return False


def is_inside_link(content, start_idx):
    """Check if position start_idx is inside an existing <a>...</a>."""
    prefix = content[:start_idx]
    open_re = re.compile(r'<a\b[^>]*>', re.IGNORECASE)
    close_re = re.compile(r'</a\s*>', re.IGNORECASE)
    opens = list(open_re.finditer(prefix))
    if not opens:
        return False
    last_open = opens[-1].end()
    m = close_re.search(content, last_open)
    if m and m.start() <= start_idx:
        return False
    return last_open <= start_idx


def find_unlinked_match(content, pattern):
    """Find first occurrence of pattern that is NOT inside <a>, <pre>, <code>, <nav>, <h*>."""
    for m in re.finditer(pattern, content):
        s = m.start()
        if is_inside_link(content, s):
            continue
        if is_inside_problem_tag(content, s):
            continue
        return m
    return None


def apply_section_link(content, target_section, href, is_cross_chapter):
    """Replace bare 'Section X.Y' with linked version. Returns (new_content, applied)."""
    # The visible text should match the actual target section number
    # Build alt patterns: "Section X.Y", "Section X.Ya" (if appropriate)
    # Use regex that matches " Section X.Y " followed by non-letter (so "Section 7.5" doesn't match "Section 7.50")
    pattern = re.compile(rf'(?<![a-zA-Z0-9.])Section\s+{re.escape(target_section)}(?![a-zA-Z0-9])')
    m = find_unlinked_match(content, pattern)
    if not m:
        return content, False
    cls = ' class="cross-ref"' if is_cross_chapter else ''
    replacement = f'<a href="{href}"{cls}>Section {target_section}</a>'
    new_content = content[:m.start()] + replacement + content[m.end():]
    return new_content, True


def apply_chapter_link(content, chapter_num, href, is_cross_chapter):
    """Replace bare 'Chapter NN' with linked version. Returns (new_content, applied)."""
    pattern = re.compile(rf'(?<![a-zA-Z0-9])Chapter\s+{re.escape(chapter_num)}(?![a-zA-Z0-9.])')
    m = find_unlinked_match(content, pattern)
    if not m:
        return content, False
    cls = ' class="cross-ref"' if is_cross_chapter else ''
    replacement = f'<a href="{href}"{cls}>Chapter {chapter_num}</a>'
    new_content = content[:m.start()] + replacement + content[m.end():]
    return new_content, True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--slice', required=True, help='comma-separated path prefixes')
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--limit', type=int, default=10000)
    parser.add_argument('--max-per-file', type=int, default=8)
    args = parser.parse_args()

    findings = json.load(open(os.path.join(ROOT, 'docs', 'content-audit', '_xref_findings.json')))
    prefixes = [p.strip() for p in args.slice.split(',') if p.strip()]

    by_file = defaultdict(lambda: {'sections': [], 'chapters': []})
    for r in findings['unlinked_section_refs']:
        by_file[r['file']]['sections'].append(r)
    for r in findings['unlinked_chapter_refs']:
        by_file[r['file']]['chapters'].append(r)

    def matches(f):
        f_norm = f.replace('\\', '/')
        return any(f_norm.startswith(p) for p in prefixes)

    total_added = 0
    skipped = []
    by_chapter_added = defaultdict(int)
    by_file_added = defaultdict(int)

    for f in sorted(by_file.keys()):
        if not matches(f):
            continue
        if total_added >= args.limit:
            break
        full_path = os.path.join(ROOT, f)
        if not os.path.isfile(full_path):
            continue
        with open(full_path, 'r', encoding='utf-8') as fh:
            content = fh.read()
        original = content
        src_part_dir = f.replace('\\', '/').split('/')[0]
        # Determine current chapter from source file path
        src_module = f.replace('\\', '/').split('/')[1]
        src_module_num = src_module.split('-')[1] if src_module.startswith('module-') else ''
        per_file_count = 0

        # Sections first
        seen_section_keys = set()
        for r in by_file[f]['sections']:
            if per_file_count >= args.max_per_file:
                break
            sec = r['section']
            # Determine if cross-chapter
            href, verified, actual = resolve_section(f, sec)
            if not href or not verified:
                skipped.append((f, 'section', sec, 'no target'))
                continue
            if not verify_path_exists(f, href):
                skipped.append((f, 'section', sec, f'path does not exist: {href}'))
                continue
            # cross-chapter if section number's chapter part differs from src_module_num
            sec_chap = sec.split('.')[0]
            is_cross = sec_chap.zfill(2) != src_module_num.zfill(2)
            new_content, applied = apply_section_link(content, sec, href, is_cross)
            if applied:
                content = new_content
                total_added += 1
                per_file_count += 1
                by_file_added[f] += 1
                by_chapter_added[src_module_num] += 1
            else:
                skipped.append((f, 'section', sec, 'pattern not found in unlinked position'))

        # Chapters
        for r in by_file[f]['chapters']:
            if per_file_count >= args.max_per_file:
                break
            ch = r['chapter']
            href, verified = resolve_chapter(f, ch)
            if not href or not verified:
                skipped.append((f, 'chapter', ch, 'no target'))
                continue
            if not verify_path_exists(f, href):
                skipped.append((f, 'chapter', ch, f'path does not exist: {href}'))
                continue
            ch_strip = ch.lstrip('0') or '0'
            src_strip = src_module_num.lstrip('0') or '0'
            is_cross = ch_strip != src_strip
            new_content, applied = apply_chapter_link(content, ch, href, is_cross)
            if applied:
                content = new_content
                total_added += 1
                per_file_count += 1
                by_file_added[f] += 1
                by_chapter_added[src_module_num] += 1
            else:
                skipped.append((f, 'chapter', ch, 'pattern not found in unlinked position'))

        if content != original and not args.dry_run:
            with open(full_path, 'w', encoding='utf-8', newline='') as fh:
                fh.write(content)

    print(f'\nTotal links added: {total_added}')
    print(f'Files modified: {len(by_file_added)}')
    print(f'Skipped: {len(skipped)}')
    print('\nBy chapter:')
    for ch, c in sorted(by_chapter_added.items()):
        print(f'  module {ch}: {c}')
    print('\nTop skip reasons:')
    skip_reasons = defaultdict(int)
    for s in skipped:
        skip_reasons[s[3].split(':')[0]] += 1
    for r, c in sorted(skip_reasons.items(), key=lambda x: -x[1]):
        print(f'  {c} -- {r}')
    if args.dry_run:
        print('\n[DRY RUN] No files modified')

    # save skip log
    with open(os.path.join(ROOT, 'docs', 'content-audit', '_apply_xrefs_skipped.json'), 'w') as fh:
        json.dump({'skipped': skipped, 'by_file': dict(by_file_added)}, fh, indent=2)

    return total_added, skipped


if __name__ == '__main__':
    main()
