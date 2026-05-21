"""Delete fig-*.jpg files that are no longer referenced by any HTML.

Companion to wave 98 (drop boilerplate figures). After the figure tags
were removed, the underlying JPGs are orphans on disk. They are also
known to contain garbled Gemini-generated labels, so there is no value
in keeping them.

Strategy:
  - Walk every section-*.html and index.html, collect every fig-*.jpg
    path mentioned in src="..." or url(...).
  - Walk every */images/fig-*.jpg on disk.
  - Delete files that are NOT referenced.
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
SKIP = {".git", "node_modules", "KDP", "build", "source_fix_backups",
        "pagefind", ".book-update", "vendor", ".claude", "_archive",
        "agents", "templates", "docs", "scripts"}

REF_RE = re.compile(r'fig-[\w.-]+\.jpg', re.IGNORECASE)


def collect_referenced() -> set[str]:
    refs: set[str] = set()
    for p in ROOT.rglob("*.html"):
        if set(p.parts) & SKIP:
            continue
        try:
            text = p.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        for m in REF_RE.findall(text):
            refs.add(m.lower())
    return refs


def main():
    referenced = collect_referenced()
    print(f"Referenced JPGs in HTML: {len(referenced)}")

    deleted = 0
    kept = 0
    for jpg in sorted(ROOT.rglob("fig-*.jpg")):
        if set(jpg.parts) & SKIP:
            continue
        if jpg.name.lower() in referenced:
            kept += 1
            continue
        try:
            jpg.unlink()
            deleted += 1
            print(f"  - {jpg.relative_to(ROOT)}")
        except OSError as e:
            print(f"  ! could not delete {jpg}: {e}")
    print(f"\nDeleted: {deleted}, kept: {kept}")


if __name__ == "__main__":
    main()
