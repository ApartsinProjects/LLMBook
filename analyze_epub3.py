"""Sample image dimensions to confirm headroom: JPEG quality, math PNG DPI, font subsetting potential."""
import zipfile
import io
import os
import re
import struct
from collections import defaultdict, Counter

EPUB_PATH = r"E:\Projects\BookBlogsHome\LLMBook\KDP\output\building-conversational-ai-llms-agents.epub"

def jpeg_dimensions(data):
    """Parse JPEG SOF marker to extract width/height."""
    i = 0
    if data[:2] != b"\xff\xd8":
        return None
    i = 2
    while i < len(data):
        if data[i] != 0xff:
            return None
        # skip fill bytes
        while data[i] == 0xff:
            i += 1
        marker = data[i]
        i += 1
        if marker in (0xd8, 0xd9):
            return None
        if 0xd0 <= marker <= 0xd7 or marker == 0x01:
            continue
        # length
        length = struct.unpack(">H", data[i:i+2])[0]
        if marker in (0xc0, 0xc1, 0xc2, 0xc3, 0xc5, 0xc6, 0xc7, 0xc9, 0xca, 0xcb, 0xcd, 0xce, 0xcf):
            # SOFn
            h = struct.unpack(">H", data[i+3:i+5])[0]
            w = struct.unpack(">H", data[i+5:i+7])[0]
            return (w, h)
        i += length
    return None

def png_dimensions(data):
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    # IHDR after 8-byte sig + 4-byte length + 4-byte 'IHDR'
    w = struct.unpack(">I", data[16:20])[0]
    h = struct.unpack(">I", data[20:24])[0]
    bit_depth = data[24]
    color_type = data[25]
    return (w, h, bit_depth, color_type)

jpg_dims = []
png_dims = []
math_dims = []
chapter_data_uri_check = []
css_data = b""
chapter_sample_first10 = []

with zipfile.ZipFile(EPUB_PATH, "r") as z:
    for info in z.infolist():
        n = info.filename
        ln = n.lower()
        if ln.startswith("epub/img/") and (ln.endswith(".jpg") or ln.endswith(".jpeg")):
            data = z.read(n)
            dims = jpeg_dimensions(data)
            if dims:
                jpg_dims.append((n, dims[0], dims[1], info.compress_size))
        elif ln.startswith("epub/img/math_") and ln.endswith(".png"):
            data = z.read(n)
            dims = png_dimensions(data)
            if dims:
                math_dims.append((n, dims[0], dims[1], dims[2], dims[3], info.compress_size))
        elif ln.startswith("epub/img/") and ln.endswith(".png"):
            data = z.read(n)
            dims = png_dimensions(data)
            if dims:
                png_dims.append((n, dims[0], dims[1], dims[2], dims[3], info.compress_size))
        elif ln.endswith(".css"):
            css_data += z.read(n) + b"\n"
        elif ln.startswith("epub/chapters/") and len(chapter_sample_first10) < 10:
            data = z.read(n)
            chapter_sample_first10.append((n, data))

# JPG dimension distribution
print("=== JPG dimensions ===")
widths = Counter(w for _, w, _, _ in jpg_dims)
print(f"  total JPGs analyzed: {len(jpg_dims)}")
print(f"  width distribution (top 10):")
for w, cnt in widths.most_common(10):
    print(f"    {w}px: {cnt} files")
print(f"  largest by pixels:")
jpg_dims.sort(key=lambda x: -(x[1]*x[2]))
for n, w, h, c in jpg_dims[:5]:
    print(f"    {w}x{h} ({c:,} bytes) {os.path.basename(n)}")

# bytes per pixel (rough quality proxy)
bpp = [(c / (w*h), n, w, h, c) for n, w, h, c in jpg_dims if w*h > 0]
bpp.sort()
print(f"  bytes-per-pixel: median={sorted(b[0] for b in bpp)[len(bpp)//2]:.3f}")
print(f"  smallest bpp (most compressed already): {bpp[0][0]:.3f} ({os.path.basename(bpp[0][1])})")
print(f"  largest bpp (least compressed): {bpp[-1][0]:.3f} ({os.path.basename(bpp[-1][1])} {bpp[-1][2]}x{bpp[-1][3]} {bpp[-1][4]:,}b)")

print()
print("=== Math PNG dimensions ===")
print(f"  total: {len(math_dims)}")
widths_m = Counter(w for _, w, _, _, _, _ in math_dims)
heights_m = Counter(h for _, _, h, _, _, _ in math_dims)
print(f"  width distribution (top 10):")
for w, cnt in sorted(widths_m.most_common(10)):
    print(f"    {w}px: {cnt} files")
print(f"  height distribution (top 5):")
for h, cnt in sorted(heights_m.most_common(5)):
    print(f"    {h}px: {cnt} files")
ct_counts = Counter(ct for _, _, _, _, ct, _ in math_dims)
bd_counts = Counter(bd for _, _, _, bd, _, _ in math_dims)
print(f"  color types: {dict(ct_counts)}  (0=gray,2=rgb,3=palette,4=gray+alpha,6=rgb+alpha)")
print(f"  bit depths: {dict(bd_counts)}")

print()
print("=== Non-math PNG dimensions ===")
print(f"  total: {len(png_dims)}")
widths_p = Counter(w for _, w, _, _, _, _ in png_dims)
print(f"  width distribution (top 10):")
for w, cnt in widths_p.most_common(10):
    print(f"    {w}px: {cnt} files")
ct_counts = Counter(ct for _, _, _, _, ct, _ in png_dims)
bd_counts = Counter(bd for _, _, _, bd, _, _ in png_dims)
print(f"  color types: {dict(ct_counts)}")
print(f"  bit depths: {dict(bd_counts)}")

print()
print("=== CSS total ===")
print(f"  combined CSS size: {len(css_data):,} bytes")

print()
print("=== Chapter inline content check ===")
# Look for data: URIs in a sampling of chapters
data_uri_count = 0
total_sample_bytes = 0
for n, data in chapter_sample_first10:
    total_sample_bytes += len(data)
    matches = re.findall(rb'data:[a-z/]+;base64,[A-Za-z0-9+/=]{100,}', data)
    if matches:
        data_uri_count += len(matches)
        print(f"  {n}: {len(matches)} data URIs found")
print(f"  sampled {len(chapter_sample_first10)} chapter files, total {total_sample_bytes:,} uncompressed bytes")
print(f"  total data URIs in sample: {data_uri_count}")

# also check for inline SVG and inline styles
inline_svg = 0
inline_style = 0
for n, data in chapter_sample_first10:
    inline_svg += len(re.findall(rb'<svg', data))
    inline_style += len(re.findall(rb'<style', data))
print(f"  inline <svg> tags in sample: {inline_svg}")
print(f"  inline <style> blocks in sample: {inline_style}")

# Glyph-set analysis for fonts: which chars appear in chapter text?
print()
print("=== Glyph coverage probe (sample chapters) ===")
all_text = b""
for n, data in chapter_sample_first10:
    # strip tags very roughly
    text = re.sub(rb'<[^>]+>', b' ', data)
    all_text += text
text_str = all_text.decode("utf-8", errors="replace")
unique_chars = set(text_str)
ascii_chars = {c for c in unique_chars if ord(c) < 128}
non_ascii = {c for c in unique_chars if ord(c) >= 128}
print(f"  unique chars in 10-chapter sample: {len(unique_chars)} ({len(ascii_chars)} ASCII + {len(non_ascii)} non-ASCII)")
print(f"  non-ASCII chars: {sorted(non_ascii)[:40]}")
