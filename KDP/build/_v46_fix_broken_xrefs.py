"""v4.6: Auto-fix the 106 broken xrefs found by validation.

Most fall into a few categories:
  1. `module-XX/section-29.1.html` — section 29.1 lives in Module 29
     (part-8), not in the source module
  2. `module-09-inference-optimization/section-18.1.html` — section 18.1
     moved to Module 18 in part-10 (Frontiers)
  3. `module-32/section-17.5.html` — section 17.5 moved from 32 to 17
  4. `module-12-hybrid-ml-llm/index.html` (path-not-found) — wrong
     relative depth
  5. `part-2/index.html` lists module-18 sections that no longer exist
     under part-2 (module moved to part-10)

Strategy: build a redirect map from filename to actual location on disk.
For every broken xref, look up where the target file ACTUALLY lives.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
EXCLUDE = {"_archive", "KDP", "node_modules", "vendor", "scripts", "agents"}
MAX_FILE = 5_000_000

import os


def safe_read(p: Path) -> str | None:
    try:
        if p.stat().st_size > MAX_FILE: return None
        return p.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return None


# Build filename -> [actual_paths] map
def build_filename_index() -> dict:
    idx = {}
    for p in ROOT.rglob("*.html"):
        if any(part in p.parts for part in EXCLUDE): continue
        idx.setdefault(p.name, []).append(p)
    return idx


def fix_xref_in_file(p: Path, file_index: dict) -> int:
    text = safe_read(p)
    if text is None: return 0
    original = text
    n_fixed = 0
    parent = p.parent

    # For every broken href, try to find the actual location
    href_re = re.compile(r'(<a\s+[^>]*href=")([^"]+\.html)((?:#[^"]*)?")', re.IGNORECASE)
    def maybe_fix(m: re.Match) -> str:
        nonlocal n_fixed
        prefix, href, suffix = m.group(1), m.group(2), m.group(3)
        if href.startswith(("http://", "https://", "mailto:", "javascript:", "data:")):
            return m.group(0)
        try:
            target = (parent / href).resolve()
            if target.exists():
                return m.group(0)  # OK
        except Exception:
            return m.group(0)

        # Broken — look up filename in the index
        filename = href.rsplit("/", 1)[-1]
        candidates = file_index.get(filename, [])
        if len(candidates) == 1:
            new_target = candidates[0]
            new_rel = os.path.relpath(str(new_target), str(parent.resolve())).replace("\\", "/")
            n_fixed += 1
            return f'{prefix}{new_rel}{suffix}'
        elif len(candidates) > 1:
            # Multiple candidates - pick the one in the same part if possible
            for c in candidates:
                if c.parts[0] == p.parts[0]:
                    new_rel = os.path.relpath(str(c), str(parent.resolve())).replace("\\", "/")
                    n_fixed += 1
                    return f'{prefix}{new_rel}{suffix}'
            # Otherwise pick the first
            new_rel = os.path.relpath(str(candidates[0]), str(parent.resolve())).replace("\\", "/")
            n_fixed += 1
            return f'{prefix}{new_rel}{suffix}'
        # No candidate found - leave as-is (will be reported as unfixable)
        return m.group(0)

    text = href_re.sub(maybe_fix, text)
    if text != original:
        p.write_text(text, encoding="utf-8")
    return n_fixed


def main() -> int:
    file_index = build_filename_index()
    n_files = 0
    n_total_fixed = 0
    for p in ROOT.rglob("*.html"):
        if any(part in p.parts for part in EXCLUDE): continue
        fixed = fix_xref_in_file(p, file_index)
        if fixed > 0:
            n_files += 1
            n_total_fixed += fixed
    print(f"\nFixed {n_total_fixed} broken xrefs across {n_files} files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
