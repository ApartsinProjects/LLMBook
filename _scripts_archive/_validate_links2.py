"""Validate all internal links across HTML files with categorized output."""

import os
import re
from pathlib import Path
from collections import defaultdict, Counter
from html.parser import HTMLParser

ROOT = Path(r"E:/Projects/LLMCourse")

class LinkExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
    def handle_starttag(self, tag, attrs):
        if tag == "a":
            for name, value in attrs:
                if name == "href" and value:
                    self.links.append((self.getpos()[0], value))

def find_html_files(root):
    result = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if not d.startswith('.') and d not in ('node_modules', '.git')]
        for f in filenames:
            if f.endswith('.html'):
                result.append(Path(dirpath) / f)
    return result

def is_internal(href):
    if not href:
        return False
    if href.startswith(('#', 'http://', 'https://', 'mailto:', 'javascript:', 'tel:')):
        return False
    return True

def resolve_link(source_file, href):
    clean = href.split('#')[0]
    if not clean:
        return None
    source_dir = source_file.parent
    target = (source_dir / clean).resolve()
    return target

def categorize_broken(href, resolved_str):
    """Attempt to categorize the type of breakage."""
    resolved = Path(resolved_str)
    target_name = resolved.name

    # Leading zero mismatch: section-08.1.html vs section-8.1.html
    m = re.search(r'section-0(\d+\.\d+)', target_name)
    if m:
        alt_name = target_name.replace(f'section-0{m.group(1)}', f'section-{m.group(1)}')
        alt_path = resolved.parent / alt_name
        if alt_path.exists():
            return "LEADING_ZERO", f"should be {alt_name}"

    # Reverse: section-X.Y but section-0X.Y exists
    m2 = re.search(r'section-(\d+\.\d+)', target_name)
    if m2 and not target_name.startswith('section-0'):
        alt_name2 = target_name.replace(f'section-{m2.group(1)}', f'section-0{m2.group(1)}')
        alt_path2 = resolved.parent / alt_name2
        if alt_path2.exists():
            return "MISSING_LEADING_ZERO", f"should be {alt_name2}"

    # Check if the parent directory doesn't exist (renamed module/directory)
    if not resolved.parent.exists():
        return "MISSING_DIRECTORY", f"directory {resolved.parent.name} not found"

    # File simply missing
    if resolved.parent.exists() and not resolved.exists():
        return "MISSING_FILE", f"{target_name} not found in {resolved.parent.name}"

    return "OTHER", ""

def main():
    html_files = find_html_files(ROOT)
    print(f"Found {len(html_files)} HTML files\n")

    total_checked = 0
    broken_all = []  # (source_rel, line, href, resolved, category, detail)
    categories = Counter()

    for fpath in sorted(html_files):
        try:
            text = fpath.read_text(encoding='utf-8', errors='replace')
        except Exception as e:
            continue

        parser = LinkExtractor()
        try:
            parser.feed(text)
        except Exception:
            continue

        for line, href in parser.links:
            if not is_internal(href):
                continue
            clean_href = href.split('#')[0]
            if not clean_href:
                continue
            resolved = resolve_link(fpath, href)
            if resolved is None:
                continue
            total_checked += 1
            if not resolved.exists():
                rel_source = str(fpath.relative_to(ROOT))
                cat, detail = categorize_broken(href, str(resolved))
                categories[cat] += 1
                broken_all.append((rel_source, line, href, str(resolved), cat, detail))

    total_broken = len(broken_all)

    print("=" * 90)
    print("LINK VALIDATION RESULTS")
    print("=" * 90)
    print(f"Total internal links checked: {total_checked}")
    print(f"Total broken links:           {total_broken}")
    print()

    # Category summary
    print("BROKEN LINK CATEGORIES:")
    print("-" * 50)
    for cat, count in categories.most_common():
        print(f"  {cat:30s} {count:5d}")
    print()

    # Group by source file
    by_source = defaultdict(list)
    for item in broken_all:
        by_source[item[0]].append(item[1:])

    print(f"FILES WITH BROKEN LINKS: {len(by_source)}")
    print("=" * 90)

    for src in sorted(by_source.keys()):
        items = by_source[src]
        print(f"\n  {src} ({len(items)} broken)")
        for line, href, resolved, cat, detail in sorted(items):
            extra = f" [{cat}] {detail}" if detail else f" [{cat}]"
            print(f"    Line ~{line}: {href}{extra}")
    print()

    # Also print unique broken targets
    unique_targets = set()
    for item in broken_all:
        # Get just the target filename
        t = Path(item[3])
        unique_targets.add(f"{t.parent.name}/{t.name}")

    print(f"\nUNIQUE BROKEN TARGETS ({len(unique_targets)}):")
    print("-" * 60)
    for t in sorted(unique_targets):
        print(f"  {t}")

if __name__ == "__main__":
    main()
