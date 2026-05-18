"""Analyze findings for wave 33: produce sorted top-N for each category."""
import json
import os
from collections import Counter, defaultdict

ROOT = r"E:\Projects\BookBlogsHome\LLMBook"
with open(os.path.join(ROOT, "docs", "content-audit", "_xref_findings.json"), "r", encoding="utf-8") as fh:
    data = json.load(fh)


def show(cat, n=40):
    print(f"\n=== {cat} (total={len(data[cat])}) ===")
    for i, item in enumerate(data[cat][:n]):
        print(f"  {i+1}. {item}")


# 1. Bad anchor text
print("\n--- BAD ANCHOR TEXT analysis ---")
print(f"Total: {len(data['bad_anchor_text'])}")
# Count distinct patterns
patterns = Counter()
for it in data["bad_anchor_text"]:
    patterns[(it["cited_section"], it["target_section"])] += 1

print("Top (cited -> target) patterns:")
for (c, t), n in patterns.most_common(30):
    print(f"  {n:5d}: {c!r} -> {t!r}")


# 2. Stale section labels
print("\n--- STALE SECTION LABELS ---")
print(f"Total: {len(data['stale_section_labels'])}")
for i, it in enumerate(data["stale_section_labels"]):
    print(f"  {i+1}. {it['file']}: '{it['cited_section']}' -> target {it['target_section']} (text: {it['text'][:80]})")


# 3. Distribution of unlinked refs
print("\n--- UNLINKED SECTION REFS ---")
print(f"Total: {len(data['unlinked_section_refs'])}")
file_counts = Counter(it["file"] for it in data["unlinked_section_refs"])
print("Top files:")
for f, n in file_counts.most_common(20):
    print(f"  {n:4d}: {f}")


# 4. Unlinked chapter refs
print("\n--- UNLINKED CHAPTER REFS ---")
print(f"Total: {len(data['unlinked_chapter_refs'])}")
file_counts2 = Counter(it["file"] for it in data["unlinked_chapter_refs"])
print("Top files:")
for f, n in file_counts2.most_common(20):
    print(f"  {n:4d}: {f}")


# 5. Mismatched concept-link
print("\n--- MISMATCHED CONCEPT-LINK ---")
print(f"Total: {len(data['mismatched_concept_link'])}")
for it in data["mismatched_concept_link"][:15]:
    print(f"  {it['file']}: '{it['text']}' -> target heading '{it['target_heading']}'")
