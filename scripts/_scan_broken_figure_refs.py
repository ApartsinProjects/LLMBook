#!/usr/bin/env python
"""Quick scan: find prose Figure X.Y.Z citations whose target does not exist."""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXCLUDE = {"KDP", "node_modules", "pagefind", "scripts", "agents", ".claude", "templates"}

# Collect all existing figure labels (Figure X.Y.Z from <strong>Figure ...</strong>
# or <strong>Figure X.Y.Z:</strong>).
labels: set[str] = set()
files: list[tuple[Path, str]] = []
for p in ROOT.rglob("*.html"):
    parts = set(p.relative_to(ROOT).parts[:1])
    if parts & EXCLUDE:
        continue
    if any(seg.startswith("temp_") or "backup" in seg.lower() for seg in p.parts):
        continue
    try:
        text = p.read_text(encoding="utf-8")
    except Exception:
        continue
    files.append((p, text))
    for m in re.finditer(r"<strong>\s*Figure\s+([A-Za-z0-9]+\.[0-9]+(?:\.[0-9]+[a-z]?)?)\s*:?\s*</strong>", text):
        labels.add(m.group(1))

# Find prose Figure citations.
cited: dict[str, list[tuple[Path, int]]] = {}
for p, text in files:
    # Match "Figure X.Y.Z" but require the number end with a non-digit, non-dot, non-alpha-after-digit boundary
    for m in re.finditer(r"\bFigure\s+([A-Za-z0-9]+\.[0-9]+(?:\.[0-9]+[a-z]?)?)(?![\.0-9a-zA-Z])", text):
        num = m.group(1)
        # Skip if it's inside the literal <strong>Figure X.Y.Z</strong>
        # (Could be the caption itself.)
        if num in labels:
            continue
        # Compute line number
        line = text[:m.start()].count("\n") + 1
        cited.setdefault(num, []).append((p, line))

# Output: each cited figure that doesn't exist as a target.
print(f"Existing labels: {len(labels)}")
print(f"Broken figure citations: {len(cited)}")
for num, locs in sorted(cited.items()):
    print(f"\nFigure {num}: {len(locs)} citations")
    for path, ln in locs[:5]:
        print(f"  {path.relative_to(ROOT)}:{ln}")
