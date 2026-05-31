"""Analyze EPUB file composition for size reduction opportunities."""
import zipfile
import os
import re
from collections import defaultdict

EPUB_PATH = r"E:\Projects\BookBlogsHome\LLMBook\KDP\output\building-conversational-ai-llms-agents.epub"

def categorize(name):
    n = name.lower()
    if n.startswith("epub/img/svg_") and n.endswith(".png"):
        return "img/svg_*.png (SVG-rasterized)"
    if n.startswith("epub/img/math_") and n.endswith(".png"):
        return "img/math_*.png (math equations)"
    if n.startswith("epub/img/") and n.endswith(".png"):
        return "img/*.png (other PNGs)"
    if n.startswith("epub/img/") and (n.endswith(".jpg") or n.endswith(".jpeg")):
        return "img/*.jpg (photos/illustrations)"
    if n.startswith("epub/img/") and n.endswith(".svg"):
        return "img/*.svg (vector)"
    if n.startswith("epub/img/"):
        return "img/* (other)"
    if n.startswith("epub/fonts/"):
        return "fonts/*"
    if n.startswith("epub/styles/") or n.endswith(".css"):
        return "styles/*.css"
    if n.startswith("epub/chapters/") and (n.endswith(".xhtml") or n.endswith(".html")):
        return "chapters/*.xhtml"
    if n.endswith(".xhtml") or n.endswith(".html"):
        return "other HTML"
    if n.endswith(".opf"):
        return "OPF"
    if n.endswith(".ncx"):
        return "NCX"
    if n == "mimetype" or n.endswith("container.xml"):
        return "EPUB metadata"
    return f"other: {os.path.splitext(name)[1] or '(no ext)'}"

cat_compressed = defaultdict(int)
cat_uncompressed = defaultdict(int)
cat_count = defaultdict(int)
all_files = []

with zipfile.ZipFile(EPUB_PATH, "r") as z:
    for info in z.infolist():
        cat = categorize(info.filename)
        cat_compressed[cat] += info.compress_size
        cat_uncompressed[cat] += info.file_size
        cat_count[cat] += 1
        all_files.append((info.filename, info.compress_size, info.file_size, cat))

total_compressed = sum(cat_compressed.values())
total_uncompressed = sum(cat_uncompressed.values())

print(f"=== EPUB TOTAL ===")
print(f"Total compressed:   {total_compressed:>12,} bytes ({total_compressed/1024/1024:.2f} MB)")
print(f"Total uncompressed: {total_uncompressed:>12,} bytes ({total_uncompressed/1024/1024:.2f} MB)")
print(f"Total files: {len(all_files)}")
print()

print(f"=== BY CATEGORY (sorted by compressed size) ===")
print(f"{'Category':<40} {'Count':>6} {'Compressed':>14} {'Uncompressed':>14} {'%':>6}")
for cat in sorted(cat_compressed, key=lambda c: -cat_compressed[c]):
    pct = 100 * cat_compressed[cat] / total_compressed
    print(f"{cat:<40} {cat_count[cat]:>6} {cat_compressed[cat]:>14,} {cat_uncompressed[cat]:>14,} {pct:>5.1f}%")

print()
print(f"=== TOP 30 LARGEST FILES (by compressed size) ===")
all_files.sort(key=lambda x: -x[1])
for fn, c, u, cat in all_files[:30]:
    print(f"  {c:>10,}  {u:>10,}  [{cat[:30]:<30}]  {fn}")
