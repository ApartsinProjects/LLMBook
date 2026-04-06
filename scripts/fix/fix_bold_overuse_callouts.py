#!/usr/bin/env python3
"""
Fix excessive bold usage in callouts across the book.

Rules:
1. In all callout types: trim <strong>...</strong> spans longer than 80 chars
   to the first natural break (comma, colon, semicolon, period, open paren).
2. In practical-example callouts: keep structural labels bold but remove bold
   from sentences following Lesson:/Result: labels if >40 chars.
3. In key-insight callouts: same trimming logic for long post-label bold text.
4. Skip: <pre>/<code> content, <figcaption>, callout-title divs,
   Figure/Code Fragment patterns, structural labels under 30 chars ending :</strong>.

Usage:
    python fix_bold_overuse_callouts.py          # dry run
    python fix_bold_overuse_callouts.py --fix    # apply changes
"""

import argparse
import re
import sys
from pathlib import Path

BOOK_ROOT = Path(r"E:/Projects/LLMCourse")

# Directories to skip
SKIP_DIRS = {"_archive", "node_modules", ".git", "agents", "templates",
             "capstone", "front-matter", "scripts"}

# Callout class prefixes we care about
CALLOUT_TYPES = [
    "key-insight", "warning", "tip", "note", "research-frontier",
    "library-shortcut", "big-picture", "practical-example",
    "fun-note",
]

# Patterns to never touch
FIGURE_CODE_RE = re.compile(
    r"<strong>\s*(Figure|Code Fragment|Pseudocode|Table)\s+[\d\w.]+", re.IGNORECASE
)

# Natural break characters for trimming
BREAK_CHARS = {",", ":", ";", ".", "("}

# Labels whose following bold text should be unbolded if too long
POST_LABEL_UNBOLD = ["Lesson:", "Result:"]
POST_LABEL_UNBOLD_KEY_INSIGHT = ["Lesson:", "Result:", "Key advantage:",
                                  "Key limitation:", "Concrete example:"]


def strip_html_tags(text: str) -> str:
    """Strip HTML tags, return plain text."""
    return re.sub(r"<[^>]+>", "", text)


def text_len(html_content: str) -> int:
    """Get the text length of HTML content (excluding tags)."""
    return len(strip_html_tags(html_content).strip())


def find_trim_point(inner_html: str, min_len: int = 10) -> int | None:
    """
    Find the best trim point in the inner HTML at a natural break.
    Returns the index in inner_html to trim at (keep everything before),
    or None if no good trim point exists.
    """
    plain = strip_html_tags(inner_html)

    # Build mapping from plain text index to HTML index
    plain_to_html = {}
    plain_idx = 0
    in_tag = False
    for hi, ch in enumerate(inner_html):
        if ch == "<":
            in_tag = True
            continue
        if in_tag:
            if ch == ">":
                in_tag = False
            continue
        plain_to_html[plain_idx] = hi
        plain_idx += 1

    # Find first break char in plain text after min_len chars
    for pi in range(min_len, len(plain)):
        if plain[pi] in BREAK_CHARS:
            html_pos = plain_to_html.get(pi)
            if html_pos is not None:
                if plain[pi] == "(":
                    return html_pos  # trim before the paren
                else:
                    return html_pos + 1  # include the break char
    return None


def find_callout_ranges(html: str) -> list[tuple[int, int, str]]:
    """
    Find all callout div ranges in the HTML.
    Returns list of (start, end, callout_type) tuples.
    """
    results = []
    for ctype in CALLOUT_TYPES:
        pattern = re.compile(
            rf'<div\s+class="callout\s+{re.escape(ctype)}"', re.IGNORECASE
        )
        for m in pattern.finditer(html):
            div_start = m.start()
            # Find the matching closing </div> by counting nesting
            depth = 0
            i = div_start
            div_end = len(html)
            while i < len(html):
                if html[i:i+4] == "<div":
                    # Check it's actually a div tag (not "divider" etc.)
                    rest = html[i+4:i+5] if i+4 < len(html) else ""
                    if rest in (" ", ">", "\t", "\n", "\r"):
                        depth += 1
                elif html[i:i+6] == "</div>":
                    depth -= 1
                    if depth == 0:
                        div_end = i + 6
                        break
                i += 1
            results.append((div_start, div_end, ctype))
    return results


def is_in_protected_zone(callout_html: str, pos: int) -> bool:
    """Check if position is inside <pre>, <code>, <figcaption>, or callout-title."""
    preceding = callout_html[:pos]
    for tag in ["pre", "code", "figcaption"]:
        last_open = preceding.rfind(f"<{tag}")
        last_close = preceding.rfind(f"</{tag}>")
        if last_open > last_close:
            return True
    # Check callout-title div
    last_title = preceding.rfind('class="callout-title"')
    if last_title != -1:
        # Find the closing </div> after that
        close_after = preceding.find("</div>", last_title)
        if close_after == -1:
            return True
    return False


def process_file(filepath: Path, fix: bool = False) -> list[dict]:
    """Process a single HTML file, returning list of changes."""
    changes = []
    html = filepath.read_text(encoding="utf-8")

    # Find all callout ranges
    callout_ranges = find_callout_ranges(html)
    if not callout_ranges:
        return []

    # Collect all replacements as (start, end, replacement) tuples
    replacements = []

    strong_re = re.compile(r"<strong>(.*?)</strong>", re.DOTALL)

    for c_start, c_end, c_type in callout_ranges:
        callout_html = html[c_start:c_end]

        for m in strong_re.finditer(callout_html):
            inner = m.group(1)
            full = m.group(0)
            local_start = m.start()
            local_end = m.end()
            abs_start = c_start + local_start
            abs_end = c_start + local_end

            # Skip if in protected zone
            if is_in_protected_zone(callout_html, local_start):
                continue

            # Skip Figure/Code Fragment/Pseudocode patterns
            if FIGURE_CODE_RE.match(full):
                continue

            plain = strip_html_tags(inner).strip()
            tlen = len(plain)

            # Rule 4: Skip structural labels under 30 chars ending with :
            if tlen < 30 and inner.rstrip().endswith(":"):
                continue

            # Check if this bold span immediately follows a label like Lesson:
            # Look at callout HTML before this match
            preceding = callout_html[:local_start].rstrip()
            labels_to_check = (POST_LABEL_UNBOLD_KEY_INSIGHT
                               if c_type == "key-insight"
                               else POST_LABEL_UNBOLD)

            is_post_label = False
            for label in labels_to_check:
                label_tag = f"<strong>{label}</strong>"
                if preceding.endswith(label_tag):
                    if tlen > 40:
                        replacement = inner  # remove bold tags, keep content
                        changes.append({
                            "file": str(filepath.relative_to(BOOK_ROOT)),
                            "text_preview": plain[:80] + ("..." if tlen > 80 else ""),
                            "chars": tlen,
                            "action": f"unbold post-{label} sentence",
                            "callout": c_type,
                        })
                        replacements.append((abs_start, abs_end, replacement))
                        is_post_label = True
                        break
            if is_post_label:
                continue

            # Rule 1: Trim if >80 chars and not a short structural label
            if tlen > 80:
                trim_pos = find_trim_point(inner)
                if trim_pos is not None and text_len(inner[:trim_pos]) >= 10:
                    trimmed_bold = inner[:trim_pos]
                    rest = inner[trim_pos:]
                    replacement = f"<strong>{trimmed_bold}</strong>{rest}"
                    changes.append({
                        "file": str(filepath.relative_to(BOOK_ROOT)),
                        "text_preview": plain[:80] + "...",
                        "chars": tlen,
                        "action": f"trim bold at char ~{text_len(trimmed_bold)}",
                        "callout": c_type,
                    })
                    replacements.append((abs_start, abs_end, replacement))

    # Apply replacements in reverse order to preserve positions
    if fix and replacements:
        replacements.sort(key=lambda r: r[0], reverse=True)
        for start, end, repl in replacements:
            html = html[:start] + repl + html[end:]
        filepath.write_text(html, encoding="utf-8")

    return changes


def collect_html_files() -> list[Path]:
    """Collect all HTML files in content directories."""
    files = []
    for pattern_dir in ["part-*", "appendices"]:
        for f in BOOK_ROOT.glob(f"{pattern_dir}/**/*.html"):
            parts = f.relative_to(BOOK_ROOT).parts
            if any(p in SKIP_DIRS or p.startswith("_") for p in parts):
                continue
            files.append(f)
    return sorted(files)


def main():
    parser = argparse.ArgumentParser(description="Fix excessive bold in callouts")
    parser.add_argument("--fix", action="store_true",
                        help="Apply fixes (default: dry run)")
    args = parser.parse_args()

    files = collect_html_files()
    print(f"Scanning {len(files)} HTML files...")
    if not args.fix:
        print("DRY RUN (use --fix to apply changes)\n")

    all_changes = []
    files_affected = set()

    for f in files:
        file_changes = process_file(f, fix=args.fix)
        if file_changes:
            all_changes.extend(file_changes)
            files_affected.add(file_changes[0]["file"])

    # Summary
    action_word = "APPLIED" if args.fix else "WOULD APPLY"
    print(f"\n{action_word} {len(all_changes)} changes in {len(files_affected)} files\n")

    # Group by action type
    by_action = {}
    for c in all_changes:
        key = c["action"].split(" ")[0]  # "trim" or "unbold"
        by_action.setdefault(key, []).append(c)

    for action_key, items in sorted(by_action.items()):
        print(f"  {action_key}: {len(items)}")

    # Details
    if all_changes:
        print(f"\n{'='*90}")
        for c in all_changes:
            print(f"  [{c['callout']:20s}] {c['file']}")
            print(f"    {c['action']} ({c['chars']} chars): {c['text_preview']}")
            print()


if __name__ == "__main__":
    main()
