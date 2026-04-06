"""Scan HTML files for <img> tags referencing images that don't exist on disk."""

import os
import re
import glob
from collections import defaultdict
from pathlib import Path

ROOT = Path(os.path.dirname(os.path.abspath(__file__)))

# Patterns to find HTML files
HTML_GLOBS = [
    "part-*/module-*/**/*.html",
    "part-*/index.html",
    "appendices/**/*.html",
    "front-matter/**/*.html",
]

# Regex to extract img tags (src and alt)
IMG_RE = re.compile(
    r'<img\s[^>]*?src=["\']([^"\']+)["\'][^>]*?>',
    re.IGNORECASE | re.DOTALL,
)
ALT_RE = re.compile(r'alt=["\']([^"\']*)["\']', re.IGNORECASE)


def find_html_files():
    files = set()
    for pattern in HTML_GLOBS:
        for path in ROOT.glob(pattern):
            files.add(path)
    return sorted(files)


def extract_images(html_path):
    """Return list of (src, alt) tuples from img tags in the file."""
    try:
        text = html_path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return []
    results = []
    for match in IMG_RE.finditer(text):
        src = match.group(1)
        alt_match = ALT_RE.search(match.group(0))
        alt = alt_match.group(1) if alt_match else "(no alt text)"
        results.append((src, alt))
    return results


def resolve_src(html_path, src):
    """Resolve an img src relative to the HTML file's directory."""
    # Skip external URLs and data URIs
    if src.startswith(("http://", "https://", "data:", "//", "mailto:")):
        return None
    html_dir = html_path.parent
    resolved = (html_dir / src).resolve()
    return resolved


def main():
    html_files = find_html_files()
    print(f"Scanning {len(html_files)} HTML files...\n")

    # Group missing images by directory
    # key: directory relative to ROOT, value: list of (html_file, src, alt, resolved)
    missing_by_dir = defaultdict(list)
    total_images = 0
    total_missing = 0

    for html_path in html_files:
        images = extract_images(html_path)
        for src, alt in images:
            resolved = resolve_src(html_path, src)
            if resolved is None:
                continue  # external URL
            total_images += 1
            if not resolved.exists():
                total_missing += 1
                rel_html = html_path.relative_to(ROOT)
                rel_dir = rel_html.parent
                missing_by_dir[str(rel_dir)].append({
                    "html": str(rel_html),
                    "src": src,
                    "alt": alt,
                    "resolved": str(resolved.relative_to(ROOT)) if resolved.is_relative_to(ROOT) else str(resolved),
                })

    # Sort directories by part/module number
    def sort_key(dirname):
        parts = dirname.replace("\\", "/").split("/")
        nums = []
        for p in parts:
            m = re.search(r'(\d+)', p)
            nums.append(int(m.group(1)) if m else 999)
        return nums

    sorted_dirs = sorted(missing_by_dir.keys(), key=sort_key)

    # Print report
    print("=" * 80)
    print(f"MISSING IMAGE REPORT")
    print(f"Total images found in HTML: {total_images}")
    print(f"Total missing images: {total_missing}")
    print("=" * 80)

    for dirname in sorted_dirs:
        entries = missing_by_dir[dirname]
        print(f"\n{'-' * 80}")
        print(f"  [{dirname}]  ({len(entries)} missing)")
        print(f"{'-' * 80}")
        for e in entries:
            print(f"  File: {e['html']}")
            print(f"    src:  {e['src']}")
            print(f"    alt:  {e['alt']}")
            print(f"    expected at: {e['resolved']}")
            print()

    # Summary table
    print("\n" + "=" * 80)
    print("SUMMARY BY DIRECTORY")
    print("=" * 80)
    for dirname in sorted_dirs:
        count = len(missing_by_dir[dirname])
        print(f"  {count:4d}  {dirname}")
    print(f"  {'-' * 40}")
    print(f"  {total_missing:4d}  TOTAL")


if __name__ == "__main__":
    main()
