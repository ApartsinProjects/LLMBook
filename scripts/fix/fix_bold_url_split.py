#!/usr/bin/env python3
"""Fix </strong> incorrectly placed inside href URLs.

A previous bold-trimming script placed </strong> right after the URL scheme
(e.g., after "https:") instead of after the closing </a> tag. This breaks
the URL and causes the browser to render all subsequent text as bold.

Broken patterns found in the codebase:

  Pattern A (most common): <strong> wraps the <a> tag directly.
    <strong><a href="https:</strong>//domain.com/path" ...>Text</a>
    Fix: <strong><a href="https://domain.com/path" ...>Text</a></strong>

  Pattern B: <strong> wraps text before the <a> tag.
    <strong>Some text <a href="section-5.</strong>3.html">Link</a>
    Fix: <strong>Some text <a href="section-5.3.html">Link</a></strong>

  Pattern C: <strong> wraps text AND an <a> tag (mixed content).
    <strong>ShareGPT / <a href="https:</strong>//hf.co/..." ...>WildChat</a></td>
    Fix: <strong>ShareGPT / <a href="https://hf.co/..." ...>WildChat</a></strong></td>

Strategy (two-pass per occurrence):
  1. Remove </strong> from inside the href attribute (rejoin the URL).
  2. Find the next </a> after that href and insert </strong> right after it.

Usage:
  python scripts/fix/fix_bold_url_split.py          # dry run
  python scripts/fix/fix_bold_url_split.py --fix     # apply changes
"""

import argparse
import re
from pathlib import Path

BOOK_ROOT = Path(r"E:/Projects/LLMCourse")

SCAN_DIRS = [
    BOOK_ROOT / "part-1-foundations",
    BOOK_ROOT / "part-2-understanding-llms",
    BOOK_ROOT / "part-3-working-with-llms",
    BOOK_ROOT / "part-4-training-adapting",
    BOOK_ROOT / "part-5-retrieval-conversation",
    BOOK_ROOT / "part-6-agentic-ai",
    BOOK_ROOT / "part-7-multimodal-applications",
    BOOK_ROOT / "part-8-evaluation-production",
    BOOK_ROOT / "part-9-safety-strategy",
    BOOK_ROOT / "part-10-frontiers",
    BOOK_ROOT / "part-11-idea-to-product",
    BOOK_ROOT / "appendices",
    BOOK_ROOT / "front-matter",
]

# Matches </strong> sitting inside an href attribute value.
# Captures: (href_before_strong)(href_after_strong_to_quote)
BROKEN_HREF_RE = re.compile(
    r'href="([^"]*?)</strong>([^"]*?)"'
)


def find_html_files():
    """Yield all .html files under scan dirs, skipping _archive."""
    for scan_dir in SCAN_DIRS:
        if not scan_dir.exists():
            continue
        for path in sorted(scan_dir.rglob("*.html")):
            if "_archive" in path.parts:
                continue
            yield path


def fix_content(content: str) -> tuple[str, list[str]]:
    """Fix all broken </strong>-in-href occurrences. Returns (fixed, log_messages)."""
    messages = []

    # We process iteratively because each fix can shift positions.
    # Use a while loop to keep finding and fixing from the start.
    iterations = 0
    max_iterations = 200  # safety cap

    while iterations < max_iterations:
        iterations += 1
        m = BROKEN_HREF_RE.search(content)
        if not m:
            break

        href_before = m.group(1)
        href_after = m.group(2)
        fixed_href = f'href="{href_before}{href_after}"'

        # Where the match starts and ends in the content
        match_start = m.start()
        match_end = m.end()

        # Replace the broken href with the fixed one
        content = content[:match_start] + fixed_href + content[match_end:]

        # Now we have an unclosed <strong> (the </strong> was removed).
        # We need to find the </a> that closes the link containing this href,
        # then insert </strong> right after it.
        #
        # Search forward from the fixed href position for the next </a>.
        search_start = match_start + len(fixed_href)
        close_a_pos = content.find("</a>", search_start)

        if close_a_pos == -1:
            messages.append(
                f"  WARNING: Could not find </a> after fixed href at offset {match_start}"
            )
            continue

        insert_pos = close_a_pos + len("</a>")

        # Check if </strong> already follows (maybe from a previous fix or already present)
        after_close_a = content[insert_pos:insert_pos + 20].lstrip()
        if after_close_a.startswith("</strong>"):
            messages.append(
                f"  Fixed href at offset {match_start}: "
                f'"{href_before}</strong>{href_after}" -> "{href_before}{href_after}" '
                f"(</strong> already present after </a>)"
            )
            continue

        # Insert </strong> after </a>
        content = content[:insert_pos] + "</strong>" + content[insert_pos:]

        messages.append(
            f"  Fixed href at offset {match_start}: "
            f'removed </strong> from URL, added after </a>'
        )

    return content, messages


def main():
    parser = argparse.ArgumentParser(
        description="Fix </strong> incorrectly placed inside href URLs."
    )
    parser.add_argument(
        "--fix", action="store_true",
        help="Apply fixes (default is dry run)."
    )
    args = parser.parse_args()

    total_files = 0
    total_fixes = 0

    for path in find_html_files():
        content = path.read_text(encoding="utf-8")

        if not BROKEN_HREF_RE.search(content):
            continue

        fixed_content, messages = fix_content(content)
        num_fixes = len(messages)
        total_files += 1
        total_fixes += num_fixes

        rel = path.relative_to(BOOK_ROOT)
        print(f"\n{rel} ({num_fixes} fix{'es' if num_fixes != 1 else ''}):")
        for msg in messages:
            print(msg)

        if args.fix:
            path.write_text(fixed_content, encoding="utf-8")
            print(f"  -> Written.")

    mode = "APPLIED" if args.fix else "DRY RUN"
    print(f"\n[{mode}] {total_fixes} fixes across {total_files} files.")


if __name__ == "__main__":
    main()
