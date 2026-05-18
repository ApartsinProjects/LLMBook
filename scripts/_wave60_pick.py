"""Scratch: enumerate IMAGE_OPPORTUNITY (fun-note) candidates for wave60."""
import json
import re
from pathlib import Path
from collections import Counter

ROOT = Path(r"E:\Projects\BookBlogsHome\LLMBook")
SNAPSHOT = ROOT / "docs" / "content-audit" / "cycle_snapshots" / "cycle_21.json"

data = json.loads(SNAPSHOT.read_text(encoding="utf-8"))
target = [
    i for i in data["issues"]
    if i.get("check_id") == "IMAGE_OPPORTUNITY"
    and "fun-note" in i.get("message", "")
]
print("Total fun-note IMAGE_OPPORTUNITY:", len(target))


def norm(p):
    return p.replace("\\", "/")


focused = []
for t in target:
    f = norm(t["file"])
    if not any(part in f for part in [
        "part-4-", "part-5-", "part-6-", "part-7-", "part-8-", "part-9-"
    ]):
        continue
    if "tools-of-the-trade" in f.lower():
        continue
    if "/module-" not in f:
        continue
    focused.append((f, t))

print("Parts 4-9 main module candidates:", len(focused))
print()

# Group by file to dedupe
by_file = {}
for f, t in focused:
    by_file.setdefault(f, t)

# Sort lexicographically
ordered = sorted(by_file.items())

# Print all sections by part for review
by_part = {}
for f, t in ordered:
    part = f.split("/")[0]
    by_part.setdefault(part, []).append(f)

for part in sorted(by_part):
    print(f"\n=== {part} ({len(by_part[part])} sections) ===")
    for f in by_part[part]:
        print(" ", f)
