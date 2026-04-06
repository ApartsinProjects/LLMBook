import re
from pathlib import Path

BOOK_ROOT = Path(r"E:/Projects/LLMCourse")
chapters = {}
for f in sorted(BOOK_ROOT.rglob("section-*.html")):
    s = str(f).replace("\\", "/")
    if any(x in s for x in ["_archive", "agents", "appendices", "front-matter"]):
        continue
    text = f.read_text(encoding="utf-8")
    if 'http-equiv="refresh"' in text:
        continue
    # Get chapter dir
    chapter_dir = str(f.parent).replace("\\", "/")
    rel_chapter = str(f.parent.relative_to(BOOK_ROOT)).replace("\\", "/")
    count = len(re.findall(r'<figure class="illustration">', text))
    has_illust = count > 0
    rel_file = str(f.relative_to(BOOK_ROOT)).replace("\\", "/")
    if rel_chapter not in chapters:
        chapters[rel_chapter] = {"total": 0, "sections": [], "missing": []}
    chapters[rel_chapter]["total"] += count
    if has_illust:
        chapters[rel_chapter]["sections"].append((rel_file, count))
    else:
        chapters[rel_chapter]["missing"].append(rel_file)

# Focus on parts 8, 9, 10, 11
for ch in sorted(chapters):
    if any(x in ch for x in ["part-8", "part-9", "part-10", "part-11"]):
        info = chapters[ch]
        print(f"\n{ch}: {info['total']} illustrations")
        for sf, c in info["sections"]:
            print(f"  HAS: {sf} ({c})")
        for sf in info["missing"]:
            print(f"  MISSING: {sf}")
