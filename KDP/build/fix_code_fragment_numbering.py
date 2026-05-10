"""Renumber `Code Fragment N: ...` captions in section files to use the
hierarchical scheme `X.Y.N` (where X.Y is the section, N is the local index).

Same logic as fix_section_numbering.py but applied to `<strong>Code Fragment N:`
inside `<div class="code-caption">` blocks. Affects appendices and chapters
where authors used flat numbering.

After cleaning up `tmppdf.html` artifacts, the real duplicates are:
- 10 instances of "Code Fragment 1" across 10 appendix sections
- 11 instances of "Code Fragment 2" across 11 chapter+appendix sections
- ... etc.

Idempotent: skip if number already contains a dot.
"""
from __future__ import annotations
import re
import shutil
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Match section-X.Y.html OR section-{letter}.N.html (appendix sections)
SECTION_FILE_RE = re.compile(r"section-([\d\w]+)\.([\d\w]+)\.html$", re.IGNORECASE)

# `<strong>Code Fragment 5:` (flat) but NOT `<strong>Code Fragment 0.1.5:` (hierarchical)
CF_FLAT_RE = re.compile(
    r"(<strong>Code Fragment\s+)"
    r"(\d+)"          # capture flat number
    r"(:\s*</strong>)",
    re.IGNORECASE,
)


def renumber_code_fragments(content: str, section_prefix: str) -> tuple[str, int]:
    n_changed = 0
    def replace(m: re.Match) -> str:
        nonlocal n_changed
        n_changed += 1
        return f"{m.group(1)}{section_prefix}.{m.group(2)}{m.group(3)}"
    new_content = CF_FLAT_RE.sub(replace, content)
    return new_content, n_changed


def main() -> int:
    files_modified: list[tuple[str, str, int]] = []
    backup_dir = PROJECT_ROOT / "KDP/build/source_fix_backups" / time.strftime("code_fragments_%Y%m%d_%H%M%S")

    for path in PROJECT_ROOT.rglob("*.html"):
        if any(part in path.parts for part in ("KDP", "vendor", "scripts", "templates", "md", "node_modules")):
            continue
        m = SECTION_FILE_RE.search(path.name)
        if not m:
            continue
        section_prefix = f"{m.group(1)}.{m.group(2)}"

        text = path.read_text(encoding="utf-8", errors="replace")
        new_text, n = renumber_code_fragments(text, section_prefix)
        if n == 0:
            continue
        backup_dir.mkdir(parents=True, exist_ok=True)
        rel = path.relative_to(PROJECT_ROOT)
        backup = backup_dir / rel
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, backup)
        path.write_text(new_text, encoding="utf-8")
        files_modified.append((str(rel).replace("\\", "/"), section_prefix, n))

    total = sum(n for _, _, n in files_modified)
    print(f"Renumbered {total} Code Fragment captions in {len(files_modified)} files")
    if files_modified:
        print(f"Backups: {backup_dir.relative_to(PROJECT_ROOT)}")
        for rel, prefix, n in files_modified[:15]:
            print(f"  {n:>2}x  [{prefix}] {rel}")
        if len(files_modified) > 15:
            print(f"  ... +{len(files_modified) - 15} more")
    return 0


if __name__ == "__main__":
    sys.exit(main())
