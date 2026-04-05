#!/usr/bin/env python3
"""Detect unclosed HTML tags across all book pages.

Checks for mismatched open/close counts of inline and block tags
that commonly cause rendering issues when left unclosed.
Uses stack-based matching to identify the exact unclosed tag location.

Usage:
    python detect_unclosed_tags.py [--verbose]
"""

import re
import sys
import glob
import argparse
from pathlib import Path

# Tags to check: ones that cause visible rendering problems when unclosed
CHECKED_TAGS = ["a", "strong", "em", "code", "span", "div", "p", "li", "td", "th", "tr", "table",
                "pre", "blockquote", "section", "article", "aside", "details", "summary",
                "h1", "h2", "h3", "h4", "h5", "h6", "ul", "ol", "dl", "dt", "dd",
                "figure", "figcaption", "label", "button", "select", "textarea", "form"]

# Self-closing / void tags (never need a closing tag)
VOID_TAGS = {"br", "hr", "img", "input", "meta", "link", "source", "area", "base", "col", "embed",
             "param", "track", "wbr"}

FILE_GLOBS = [
    "front-matter/**/*.html",
    "part-*/module-*/**/*.html",
    "part-*/capstone*/**/*.html",
    "appendices/**/*.html",
    "index.html",
    "toc.html",
]


def find_unclosed_tags(filepath: Path, verbose: bool = False) -> list[dict]:
    """Find unclosed tags in an HTML file using stack-based matching."""
    issues = []
    try:
        content = filepath.read_text(encoding="utf-8")
    except Exception as e:
        issues.append({"file": str(filepath), "tag": "?", "line": 0, "msg": f"Read error: {e}"})
        return issues

    for tag in CHECKED_TAGS:
        # Find all open tags (not self-closing)
        open_pattern = re.compile(rf"<{tag}(\s[^>]*)?>", re.IGNORECASE)
        close_pattern = re.compile(rf"</{tag}\s*>", re.IGNORECASE)
        selfclose_pattern = re.compile(rf"<{tag}(\s[^>]*)?\s*/>", re.IGNORECASE)

        events = []
        for m in open_pattern.finditer(content):
            # Skip self-closing
            if selfclose_pattern.match(content[m.start():m.end() + 2]):
                continue
            line_num = content[:m.start()].count("\n") + 1
            events.append((m.start(), "open", line_num, m.group()[:100]))

        for m in close_pattern.finditer(content):
            line_num = content[:m.start()].count("\n") + 1
            events.append((m.start(), "close", line_num, m.group()))

        events.sort(key=lambda x: x[0])

        stack = []
        for pos, kind, line_num, text in events:
            if kind == "open":
                stack.append((pos, line_num, text))
            else:
                if stack:
                    stack.pop()
                else:
                    issues.append({
                        "file": str(filepath),
                        "tag": tag,
                        "line": line_num,
                        "msg": f"Extra </{tag}> at line {line_num}",
                    })

        for pos, line_num, text in stack:
            issues.append({
                "file": str(filepath),
                "tag": tag,
                "line": line_num,
                "msg": f"Unclosed <{tag}> at line {line_num}: {text}",
            })

    return issues


def main():
    parser = argparse.ArgumentParser(description="Detect unclosed HTML tags across the book")
    parser.add_argument("--verbose", "-v", action="store_true")
    args = parser.parse_args()

    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    root = Path(__file__).resolve().parents[3]  # LLMCourse root

    files = set()
    for pattern in FILE_GLOBS:
        files.update(root.glob(pattern))

    files = sorted(files)
    print(f"Scanning {len(files)} HTML files for unclosed tags...")

    all_issues = []
    for f in files:
        issues = find_unclosed_tags(f, args.verbose)
        all_issues.extend(issues)

    if not all_issues:
        print("No unclosed tag issues found!")
        return

    # Group by file
    by_file: dict[str, list] = {}
    for issue in all_issues:
        by_file.setdefault(issue["file"], []).append(issue)

    # Filter to only critical tags that cause rendering problems
    critical_tags = {"a", "strong", "em", "code", "span", "pre"}
    critical_issues = [i for i in all_issues if i["tag"] in critical_tags]
    other_issues = [i for i in all_issues if i["tag"] not in critical_tags]

    if critical_issues:
        print(f"\n=== CRITICAL: {len(critical_issues)} unclosed inline/formatting tags ===")
        for issue in critical_issues:
            rel = Path(issue["file"]).relative_to(root)
            print(f"  {rel}:{issue['line']} - {issue['msg']}")

    if other_issues and args.verbose:
        print(f"\n=== INFO: {len(other_issues)} unclosed block tags (may be intentional) ===")
        for issue in other_issues:
            rel = Path(issue["file"]).relative_to(root)
            print(f"  {rel}:{issue['line']} - {issue['msg']}")

    print(f"\nTotal: {len(critical_issues)} critical, {len(other_issues)} block-level")


if __name__ == "__main__":
    main()
