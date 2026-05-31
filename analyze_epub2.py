"""Deeper analysis: PNG naming patterns, JPG distribution, font usage."""
import zipfile
import os
import re
import statistics
from collections import defaultdict

EPUB_PATH = r"E:\Projects\BookBlogsHome\LLMBook\KDP\output\building-conversational-ai-llms-agents.epub"

png_files = []
jpg_files = []
math_files = []
font_files = []
chapter_files = []

with zipfile.ZipFile(EPUB_PATH, "r") as z:
    for info in z.infolist():
        n = info.filename
        ln = n.lower()
        if ln.startswith("epub/img/math_") and ln.endswith(".png"):
            math_files.append((n, info.compress_size, info.file_size))
        elif ln.startswith("epub/img/") and ln.endswith(".png"):
            png_files.append((n, info.compress_size, info.file_size))
        elif ln.startswith("epub/img/") and (ln.endswith(".jpg") or ln.endswith(".jpeg")):
            jpg_files.append((n, info.compress_size, info.file_size))
        elif ln.startswith("epub/fonts/"):
            font_files.append((n, info.compress_size, info.file_size))
        elif ln.startswith("epub/chapters/"):
            chapter_files.append((n, info.compress_size, info.file_size))

print("=== PNG naming patterns (non-math) ===")
patterns = defaultdict(lambda: [0, 0, 0])  # count, compressed, uncompressed
for n, c, u in png_files:
    base = os.path.basename(n)
    # extract leading token before _ or first hyphen
    m = re.match(r"^([a-z]+)[_-]", base)
    if m:
        prefix = m.group(1)
    else:
        prefix = "(no prefix)"
    patterns[prefix][0] += 1
    patterns[prefix][1] += c
    patterns[prefix][2] += u

for prefix in sorted(patterns, key=lambda p: -patterns[p][1])[:20]:
    cnt, csum, usum = patterns[prefix]
    print(f"  prefix '{prefix}': {cnt} files, {csum:,} compressed bytes ({csum/1024/1024:.2f} MB)")

print()
print("=== Top 15 largest PNGs (non-math) ===")
png_files.sort(key=lambda x: -x[1])
for n, c, u in png_files[:15]:
    print(f"  {c:>9,}  {os.path.basename(n)}")

print()
print("=== Math PNG stats ===")
sizes = [c for _, c, _ in math_files]
print(f"  count: {len(math_files)}")
print(f"  total compressed: {sum(sizes):,} bytes ({sum(sizes)/1024/1024:.2f} MB)")
print(f"  mean: {statistics.mean(sizes):.0f}, median: {statistics.median(sizes):.0f}")
print(f"  min: {min(sizes)}, max: {max(sizes)}")
print(f"  largest 10:")
math_files.sort(key=lambda x: -x[1])
for n, c, u in math_files[:10]:
    print(f"    {c:>7,}  {os.path.basename(n)}")

print()
print("=== JPG stats ===")
sizes = [c for _, c, _ in jpg_files]
print(f"  count: {len(jpg_files)}")
print(f"  total compressed: {sum(sizes):,} bytes ({sum(sizes)/1024/1024:.2f} MB)")
print(f"  mean: {statistics.mean(sizes):.0f}, median: {statistics.median(sizes):.0f}")
print(f"  min: {min(sizes)}, max: {max(sizes)}")
# histogram
buckets = defaultdict(int)
bucket_bytes = defaultdict(int)
for n, c, u in jpg_files:
    kb = c // 1024
    if kb < 10: bucket = "<10KB"
    elif kb < 25: bucket = "10-25KB"
    elif kb < 50: bucket = "25-50KB"
    elif kb < 75: bucket = "50-75KB"
    elif kb < 100: bucket = "75-100KB"
    elif kb < 150: bucket = "100-150KB"
    else: bucket = ">=150KB"
    buckets[bucket] += 1
    bucket_bytes[bucket] += c
print("  histogram:")
for b in ["<10KB","10-25KB","25-50KB","50-75KB","75-100KB","100-150KB",">=150KB"]:
    print(f"    {b:>12}: {buckets[b]:>4} files, {bucket_bytes[b]:>11,} bytes ({bucket_bytes[b]/1024/1024:.2f} MB)")

print()
print("=== Fonts ===")
for n, c, u in sorted(font_files, key=lambda x: -x[1]):
    print(f"  {c:>9,} compressed, {u:>9,} uncompressed  {os.path.basename(n)}")

print()
print("=== Chapter file stats ===")
sizes_c = [c for _, c, _ in chapter_files]
sizes_u = [u for _, _, u in chapter_files]
print(f"  count: {len(chapter_files)}")
print(f"  total compressed: {sum(sizes_c):,} ({sum(sizes_c)/1024/1024:.2f} MB)")
print(f"  total uncompressed: {sum(sizes_u):,} ({sum(sizes_u)/1024/1024:.2f} MB)")
print(f"  compression ratio: {sum(sizes_u)/sum(sizes_c):.2f}x")
print(f"  largest 5:")
chapter_files.sort(key=lambda x: -x[1])
for n, c, u in chapter_files[:5]:
    print(f"    {c:>7,} comp, {u:>7,} uncomp  {os.path.basename(n)}")
