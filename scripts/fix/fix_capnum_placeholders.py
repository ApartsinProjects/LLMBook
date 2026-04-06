#!/usr/bin/env python3
"""Fix @@CAPNUM_XX@@ placeholders by replacing them with the correct Code Fragment number.

For each placeholder, finds the nearest code-caption element and uses its number.
Placeholders in prose nearly always introduce the next code block, so we default
to using the next caption. Special handling for captions that contain a redundant
"Code Fragment @@CAPNUM_XX@@: " prefix after the already-correct number.

Usage:
    python fix_capnum_placeholders.py          # dry-run (report only)
    python fix_capnum_placeholders.py --fix     # apply replacements
    python fix_capnum_placeholders.py --file X  # process a single file (dry-run)
    python fix_capnum_placeholders.py --file X --fix  # process a single file and apply
"""

import argparse
import os
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]  # E:/Projects/LLMCourse

# Regex to find @@CAPNUM_XX@@ placeholders
CAPNUM_RE = re.compile(r'@@CAPNUM_\d+@@')

# Regex to find code-caption elements with Code Fragment numbers
# Matches both <div class="code-caption"> and <p class="code-caption">
CAPTION_RE = re.compile(
    r'<(?:div|p)\s+class="code-caption">\s*<strong>\s*Code Fragment\s+([\d.]+):?\s*</strong>',
    re.IGNORECASE
)

# Regex for the redundant "Code Fragment @@CAPNUM_XX@@: " inside captions
# e.g. "Code Fragment 20.7.2:</strong> Code Fragment @@CAPNUM_8@@: Querying with..."
# should become "Code Fragment 20.7.2:</strong> Querying with..."
REDUNDANT_CAPTION_RE = re.compile(r'Code Fragment @@CAPNUM_\d+@@:\s*')


def find_all_files_with_placeholders():
    """Walk the repo and find all HTML files containing @@CAPNUM_ placeholders."""
    results = []
    for dirpath, _dirnames, filenames in os.walk(ROOT):
        # Skip archive and hidden directories
        rel = os.path.relpath(dirpath, ROOT)
        if rel.startswith('_archive') or rel.startswith('.git') or rel.startswith('node_modules'):
            continue
        for fn in filenames:
            if not fn.endswith('.html'):
                continue
            fpath = Path(dirpath) / fn
            try:
                text = fpath.read_text(encoding='utf-8')
            except Exception:
                continue
            if '@@CAPNUM_' in text:
                results.append(fpath)
    return sorted(results)


def resolve_placeholders(text, filepath, verbose=True):
    """Resolve all @@CAPNUM_XX@@ placeholders in a file's text.

    Returns (new_text, list_of_replacements) where each replacement is
    (placeholder, resolved_number, line_number, direction).
    """
    # Step 1: Remove redundant "Code Fragment @@CAPNUM_XX@@: " inside captions.
    # These captions already have the correct number, so we just strip the duplicate.
    redundant_matches = list(REDUNDANT_CAPTION_RE.finditer(text))
    redundant_removals = []
    for rm in redundant_matches:
        # Check if this is inside a code-caption element (not in a code block or prose).
        # Look backward for the opening tag of a code-caption div/p, and verify
        # there is no intervening </div>, </p>, <pre>, or <code> tag.
        lookback = text[max(0, rm.start() - 200):rm.start()]
        if 'code-caption' in lookback:
            # Find the last occurrence of 'code-caption' in lookback
            idx = lookback.rfind('code-caption')
            between = lookback[idx:]
            # If there is a closing tag or a <pre>/<code> between, this is NOT inside a caption
            if not re.search(r'</(?:div|p)>|<pre|<code', between):
                line_num = text[:rm.start()].count('\n') + 1
                redundant_removals.append((rm.start(), rm.end(), rm.group(0), line_num))

    # Apply redundant removals in reverse order
    new_text = text
    for start, end, matched, line_num in reversed(redundant_removals):
        new_text = new_text[:start] + new_text[end:]
        if verbose:
            pass  # reported below

    # Step 2: Find remaining @@CAPNUM@@ placeholders in the updated text
    # Rebuild caption list from updated text
    captions = []
    for m in CAPTION_RE.finditer(new_text):
        captions.append((m.start(), m.group(1)))

    if not captions and CAPNUM_RE.search(new_text):
        if verbose:
            print(f"  WARNING: {filepath.relative_to(ROOT)} has placeholders but no code-captions!")
        return new_text, redundant_removals

    # Find remaining placeholder positions and resolve them
    replacements = []
    matches = list(CAPNUM_RE.finditer(new_text))

    for m in matches:
        pos = m.start()
        placeholder = m.group(0)

        # Separate into before and after captions
        before_captions = [(cpos, cnum) for cpos, cnum in captions if cpos < pos]
        after_captions = [(cpos, cnum) for cpos, cnum in captions if cpos > pos]

        best_caption = None
        best_dir = None

        if after_captions:
            # Default: prose introduces the next code block.
            # In textbook writing, placeholders nearly always appear in text
            # that introduces an upcoming code example.
            best_caption = after_captions[0][1]
            best_dir = 'next'
        elif before_captions:
            # No next caption available; use the most recent previous one
            best_caption = before_captions[-1][1]
            best_dir = 'prev (last resort)'

        if best_caption:
            line_num = new_text[:pos].count('\n') + 1
            replacements.append((placeholder, best_caption, line_num, best_dir))

    # Apply placeholder replacements in reverse to preserve positions
    for i in range(len(matches) - 1, -1, -1):
        m_obj = matches[i]
        if i < len(replacements):
            _, number, _, _ = replacements[i]
            new_text = new_text[:m_obj.start()] + number + new_text[m_obj.end():]

    # Build combined report
    all_changes = []
    for start, end, matched, line_num in redundant_removals:
        all_changes.append(('REMOVE', matched.strip(), '', line_num, 'redundant caption prefix'))
    for placeholder, number, line_num, direction in replacements:
        all_changes.append(('REPLACE', placeholder, number, line_num, direction))

    return new_text, all_changes


def process_file(fpath, fix=False, verbose=True):
    """Process a single file. Returns (num_changes, changes_list)."""
    text = fpath.read_text(encoding='utf-8')
    new_text, changes = resolve_placeholders(text, fpath, verbose=verbose)

    if verbose and changes:
        rel = fpath.relative_to(ROOT)
        print(f"\n  {rel}:")
        for action, old, new, line_num, info in changes:
            if action == 'REMOVE':
                print(f"    Line {line_num}: REMOVE '{old}' ({info})")
            else:
                print(f"    Line {line_num}: {old} -> {new} ({info})")

    if fix and changes and new_text != text:
        fpath.write_text(new_text, encoding='utf-8')
        if verbose:
            print(f"    [FIXED] {len(changes)} change(s) applied")

    return len(changes), changes


def main():
    parser = argparse.ArgumentParser(description='Fix @@CAPNUM_XX@@ placeholders')
    parser.add_argument('--fix', action='store_true', help='Apply replacements (default: dry-run)')
    parser.add_argument('--file', type=str, help='Process a single file instead of all')
    args = parser.parse_args()

    if args.file:
        fpath = Path(args.file).resolve()
        if not fpath.exists():
            print(f"File not found: {fpath}")
            sys.exit(1)
        files = [fpath]
    else:
        files = find_all_files_with_placeholders()

    mode = "FIX" if args.fix else "DRY-RUN"
    print(f"=== @@CAPNUM@@ Placeholder Fixer ({mode}) ===")
    print(f"Found {len(files)} file(s) with placeholders\n")

    total_changes = 0
    total_files = 0

    for fpath in files:
        count, _ = process_file(fpath, fix=args.fix)
        if count > 0:
            total_changes += count
            total_files += 1

    print(f"\n{'=' * 50}")
    print(f"Total: {total_changes} change(s) across {total_files} file(s)")
    if not args.fix:
        print("Run with --fix to apply changes.")


if __name__ == '__main__':
    main()
