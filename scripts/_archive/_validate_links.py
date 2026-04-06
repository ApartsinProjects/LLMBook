"""Validate all internal links across HTML files in E:\Projects\LLMCourse."""

import os
import re
from pathlib import Path
from collections import defaultdict
from html.parser import HTMLParser

ROOT = Path(r"E:\Projects\LLMCourse")

class LinkExtractor(HTMLParser):
    """Extract href values from <a> tags with approximate line numbers."""
    def __init__(self):
        super().__init__()
        self.links = []  # list of (line, href)
        self._line = 0

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            for name, value in attrs:
                if name == "href" and value:
                    self.links.append((self.getpos()[0], value))

def find_html_files(root):
    result = []
    for dirpath, dirnames, filenames in os.walk(root):
        # skip hidden dirs and common non-content dirs
        dirnames[:] = [d for d in dirnames if not d.startswith('.') and d not in ('node_modules', '.git')]
        for f in filenames:
            if f.endswith('.html'):
                result.append(Path(dirpath) / f)
    return result

def is_internal(href):
    """Return True if href is an internal file link (not external, not anchor-only, not mailto)."""
    if not href:
        return False
    if href.startswith(('#', 'http://', 'https://', 'mailto:', 'javascript:', 'tel:')):
        return False
    return True

def resolve_link(source_file, href):
    """Resolve a relative href from the source file's directory to an absolute path."""
    # Strip fragment
    clean = href.split('#')[0]
    if not clean:
        return None  # was just an anchor like "page.html#section" where page is empty after split
    source_dir = source_file.parent
    target = (source_dir / clean).resolve()
    return target

def main():
    html_files = find_html_files(ROOT)
    print(f"Found {len(html_files)} HTML files\n")

    total_checked = 0
    broken = defaultdict(list)  # source_file -> [(line, href, resolved)]

    for fpath in sorted(html_files):
        try:
            text = fpath.read_text(encoding='utf-8', errors='replace')
        except Exception as e:
            print(f"ERROR reading {fpath}: {e}")
            continue

        parser = LinkExtractor()
        try:
            parser.feed(text)
        except Exception as e:
            print(f"ERROR parsing {fpath}: {e}")
            continue

        for line, href in parser.links:
            if not is_internal(href):
                continue

            # Strip fragment for file existence check
            clean_href = href.split('#')[0]
            if not clean_href:
                continue  # anchor-only after stripping query

            resolved = resolve_link(fpath, href)
            if resolved is None:
                continue

            total_checked += 1

            if not resolved.exists():
                rel_source = fpath.relative_to(ROOT)
                broken[str(rel_source)].append((line, href, str(resolved)))

    # Report
    total_broken = sum(len(v) for v in broken.values())

    print("=" * 80)
    print(f"LINK VALIDATION RESULTS")
    print(f"=" * 80)
    print(f"Total internal links checked: {total_checked}")
    print(f"Total broken links: {total_broken}")
    print(f"Files with broken links: {len(broken)}")
    print()

    if broken:
        print("BROKEN LINKS BY SOURCE FILE:")
        print("-" * 80)
        for src in sorted(broken.keys()):
            print(f"\n  {src}")
            for line, href, resolved in sorted(broken[src]):
                print(f"    Line ~{line}: href=\"{href}\"")
                print(f"             resolves to: {resolved}")
        print()
    else:
        print("No broken links found!")

if __name__ == "__main__":
    main()
