"""Source-level fix for LEADING_BLANK code-block whitespace artifacts.

The audit `_audit_code_indent_detail.py` / `_audit_code_indent_detail2.py` flags
238 `<pre><code>` blocks across 110 HTML files in the LLMBook source tree that
have a visible blank line at the top of the rendered code block. The blank
comes from one of two source patterns:

  Pattern A (204 cases) - opening tag immediately followed by newline(s):
      <pre><code class="...">\\n
      <span ...

  Pattern B (30 cases) - opening tag followed by an empty c1 span + newline:
      <pre><code class="..."><span class="c1"></span>\\n
      <span ...

  Pattern C (4 cases) - multiple blank lines at top (variant of A):
      <pre><code class="...">\\n\\n
      <span ...

In every case the fix is the same: strip leading whitespace (and a leading
empty c1 span) so that the first non-blank token starts immediately after the
opening `<code ...>` tag. No internal indentation is touched. Pygments spans
inside the block are not disturbed. The bottom of the block (trailing newline
before `</code>`) is left alone.

Why a regex / surgical approach (not full BeautifulSoup re-serialisation):
BeautifulSoup re-serialises the entire document, which would normalise
quoting, attribute ordering, and self-closing markup across every other
element in these 110 files. We only want to touch the leading bytes of each
affected code block. A targeted regex anchored at `<pre><code ...>` keeps
every other byte of the source file identical.

Idempotency: after a successful run, none of the three patterns match any
more, so a second run is a no-op.

Usage
-----
  # Default: dry run (no files modified, just a report).
  python _fix_v13_17_source_blank_strip.py

  # Actually apply the fix and write `.bak` backups next to each modified
  # file:
  python _fix_v13_17_source_blank_strip.py --apply

Safety
------
- The script refuses to touch any file outside the LLMBook source tree.
- Skipped directories: node_modules, .git, KDP/output, KDP/build, KDP/html2pub,
  pagefind, temp_epub, backup, source_fix_backups.
- A `.bak` copy of each modified file is written before the new content
  replaces the original (only in --apply mode).
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path

# ---------------------------------------------------------------- configuration

LLM_ROOT = Path('E:/Projects/BookBlogsHome/LLMBook').resolve()
AUDIT_JSON = LLM_ROOT / 'KDP' / 'build' / 'AUDIT_code_indent.json'

INCLUDE_PREFIXES = ('part-', 'appendices', 'front-matter', 'capstone')
SKIP_FRAGMENTS = (
    'node_modules', '.git', 'KDP/output', 'KDP/build', 'KDP/html2pub',
    'pagefind', 'temp_epub', 'backup', 'source_fix_backups',
)

# ------------------------------------------------------------------- regex set

# Anchor: opening <pre><code ...> tag. We capture the opening tag (group 1)
# and require it to be followed by either:
#   - an empty c1 span and a newline (Pattern B), and/or
#   - one or more leading whitespace lines (Pattern A / C).
# We match the leading bytes (group 2) so we can drop them.
#
# The non-greedy alternation handles "empty span THEN whitespace lines" and
# pure "whitespace lines" with a single regex.
_LEADING_GARBAGE = (
    r'(?:<span class="c1"></span>)?'   # optional empty c1 span (Pattern B)
    r'(?:[ \t]*\n)+'                    # one or more whitespace-only lines
)

PAT_LEADING_BLANK = re.compile(
    r'(<pre><code\b[^>]*>)(' + _LEADING_GARBAGE + r')',
    re.DOTALL,
)


# ----------------------------------------------------------------- file filter

def in_source_scope(rel_posix: str) -> bool:
    """Return True if the path is inside the LLMBook source tree we care about."""
    if any(s in rel_posix for s in SKIP_FRAGMENTS):
        return False
    top = rel_posix.split('/', 1)[0]
    return top.startswith(INCLUDE_PREFIXES)


def list_target_files() -> list[Path]:
    """Read AUDIT_code_indent.json and return the unique files with LEADING_BLANK."""
    if not AUDIT_JSON.exists():
        sys.exit(f'audit JSON not found: {AUDIT_JSON}')
    with AUDIT_JSON.open('r', encoding='utf-8') as f:
        data = json.load(f)
    relpaths = sorted({
        i['file'] for i in data.get('issues', [])
        if i.get('type') == 'LEADING_BLANK'
    })
    out: list[Path] = []
    for rel in relpaths:
        rel_posix = rel.replace('\\', '/')
        if not in_source_scope(rel_posix):
            continue
        p = (LLM_ROOT / rel_posix).resolve()
        # Refuse to escape the source tree.
        try:
            p.relative_to(LLM_ROOT)
        except ValueError:
            continue
        if p.exists():
            out.append(p)
    return out


# ----------------------------------------------------------------- the fix fn

def fix_text(raw: str) -> tuple[str, int]:
    """Apply the leading-blank strip to every matching <pre><code> in `raw`.

    Returns (new_text, n_blocks_fixed).
    """
    n = 0

    def _sub(m: re.Match) -> str:
        nonlocal n
        n += 1
        # Keep the opening tag; drop the leading garbage (group 2).
        return m.group(1)

    new = PAT_LEADING_BLANK.sub(_sub, raw)
    return new, n


# ----------------------------------------------------------------- driver

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument(
        '--apply', action='store_true',
        help='Actually write changes (default is dry-run / preview only).',
    )
    args = ap.parse_args()

    files = list_target_files()
    print(f'Source tree: {LLM_ROOT}')
    print(f'Audit JSON : {AUDIT_JSON}')
    print(f'Candidate files (from audit, in source scope): {len(files)}')
    print(f'Mode: {"APPLY" if args.apply else "DRY RUN (use --apply to write)"}')
    print()

    n_files_changed = 0
    n_blocks_total = 0
    per_file: list[tuple[str, int]] = []

    for fpath in files:
        try:
            raw = fpath.read_text(encoding='utf-8')
        except Exception as e:
            print(f'  SKIP unreadable: {fpath} ({e})')
            continue

        new, n_blocks = fix_text(raw)
        if n_blocks == 0:
            # Already clean (idempotent). Nothing to do.
            continue
        if new == raw:
            # Defensive: should never happen when n_blocks > 0.
            continue

        n_files_changed += 1
        n_blocks_total += n_blocks
        rel = fpath.relative_to(LLM_ROOT).as_posix()
        per_file.append((rel, n_blocks))

        if args.apply:
            bak = fpath.with_suffix(fpath.suffix + '.bak')
            # Only write a backup on first apply; do not overwrite an existing
            # .bak that came from a previous run.
            if not bak.exists():
                shutil.copy2(fpath, bak)
            fpath.write_text(new, encoding='utf-8')

    print(f'Files {"modified" if args.apply else "that would be modified"}: {n_files_changed}')
    print(f'Code blocks {"fixed" if args.apply else "that would be fixed"}: {n_blocks_total}')
    print()
    print('Per-file detail:')
    for rel, n in per_file:
        print(f'  {n:3d}  {rel}')

    if not args.apply:
        print()
        print('Dry run complete. Re-run with --apply to write changes.')

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
