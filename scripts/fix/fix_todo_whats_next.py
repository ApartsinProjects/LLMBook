#!/usr/bin/env python3
"""
fix_todo_whats_next.py
Finds all "What's Next" / "What Comes Next" sections containing TODO placeholders
and fills them with proper content based on section headings and next-section info.

Usage:
    python fix_todo_whats_next.py          # dry-run (default)
    python fix_todo_whats_next.py --fix    # apply changes
"""

import argparse
import re
from pathlib import Path

BOOK_ROOT = Path(r"E:/Projects/LLMCourse")
TODO_MARKER = "TODO: Add what comes next"

# Regex to extract section number from filename like section-4.2.html or section-k.1.html
SECTION_RE = re.compile(r"section-(\w+\.\d+)\.html$")

# Regex to extract h1 title (may have attributes)
H1_RE = re.compile(r"<h1[^>]*>(.*?)</h1>", re.DOTALL)

# Regex to extract h2 headings (content-level, not structural ones like Exercises)
H2_RE = re.compile(r"<h2[^>]*>(.*?)</h2>", re.DOTALL)

# Structural h2s to skip when summarizing topics
SKIP_H2S = {
    "exercises", "what comes next", "what's next", "what's next?",
    "references and further reading", "bibliography", "key takeaways",
    "self-check questions", "summary", "chapter summary",
}

# Regex to find the whats-next block with TODO
WHATS_NEXT_RE = re.compile(
    r'(<div class="whats-next">)\s*'
    r"(<h[23][^>]*>.*?</h[23]>)\s*"
    r"<p>\s*TODO: Add what comes next\.\s*</p>\s*"
    r"(</div>)",
    re.DOTALL,
)


def clean_html(text: str) -> str:
    """Strip HTML tags and extra whitespace from a string."""
    return re.sub(r"<[^>]+>", "", text).strip()


def get_h1_title(filepath: Path) -> str:
    """Extract the h1 title from an HTML file."""
    try:
        content = filepath.read_text(encoding="utf-8")
    except Exception:
        return ""
    m = H1_RE.search(content)
    if m:
        return clean_html(m.group(1))
    return ""


def get_h2_topics(content: str) -> list[str]:
    """Extract content h2 headings, skipping structural ones."""
    headings = []
    for m in H2_RE.finditer(content):
        raw = clean_html(m.group(1))
        # Strip leading numbers like "1. " or "4.2 "
        stripped = re.sub(r"^\d+[\.\)]\s*", "", raw).strip()
        if stripped.lower() not in SKIP_H2S and stripped:
            headings.append(stripped)
    return headings


def find_next_section(current_file: Path) -> Path | None:
    """Find the next section file in the same directory."""
    m = SECTION_RE.search(current_file.name)
    if not m:
        return None
    sec_id = m.group(1)  # e.g., "4.2" or "k.1"
    parts = sec_id.split(".")
    prefix = parts[0]       # e.g., "4" or "k"
    num = int(parts[1])     # e.g., 2

    next_num = num + 1
    next_name = f"section-{prefix}.{next_num}.html"
    next_path = current_file.parent / next_name
    if next_path.exists():
        return next_path
    return None


def format_section_label(sec_id: str) -> str:
    """Format a section id like '4.2' or 'k.1' into 'Section 4.2' or 'Section K.1'."""
    parts = sec_id.split(".")
    prefix = parts[0]
    num = parts[1]
    # Uppercase letter prefixes for appendices
    if prefix.isalpha():
        return f"Section {prefix.upper()}.{num}"
    return f"Section {prefix}.{num}"


def summarize_topics(headings: list[str]) -> str:
    """Create a brief summary phrase from h2 headings."""
    if not headings:
        return "the core concepts presented above"
    if len(headings) == 1:
        return headings[0].lower()
    if len(headings) == 2:
        return f"{headings[0].lower()} and {headings[1].lower()}"
    # For 3+ headings, pick first two and say "and more"
    return f"{headings[0].lower()}, {headings[1].lower()}, and related topics"


def generate_replacement(
    current_file: Path,
    content: str,
    next_file: Path | None,
) -> str | None:
    """Generate the replacement whats-next block content, or None if no next section."""
    sec_match = SECTION_RE.search(current_file.name)
    if not sec_match:
        return None

    sec_id = sec_match.group(1)
    current_label = format_section_label(sec_id)

    # Get content topics from h2 headings
    h2s = get_h2_topics(content)
    topic_summary = summarize_topics(h2s)

    if next_file is None:
        # Last section in chapter: wrap up without a forward link
        chapter_dir = current_file.parent.name
        # Try to determine chapter name from the directory
        return (
            f'<div class="whats-next">\n'
            f'    <h2>What Comes Next</h2>\n'
            f'    <p>In this section we covered {topic_summary}. '
            f'This concludes the current chapter. '
            f'Return to the <a href="index.html">chapter overview</a> '
            f'to review the material or explore related chapters.</p>\n'
            f'</div>'
        )

    # Get next section info
    next_sec_match = SECTION_RE.search(next_file.name)
    if not next_sec_match:
        return None
    next_sec_id = next_sec_match.group(1)
    next_label = format_section_label(next_sec_id)
    next_title = get_h1_title(next_file)

    if not next_title:
        next_title_display = next_label
    else:
        # Strip leading section number from h1 if it duplicates our label
        # e.g., h1="A.2 Probability and Statistics" with label="Section A.2"
        # should become "Section A.2: Probability and Statistics" not "Section A.2: A.2 ..."
        stripped_title = re.sub(
            r"^[A-Za-z]?\d*\.?\d+\s+", "", next_title
        ).strip()
        if stripped_title:
            next_title_display = f"{next_label}: {stripped_title}"
        else:
            next_title_display = next_label

    # Get next section's h2 topics for a brief preview
    try:
        next_content = next_file.read_text(encoding="utf-8")
        next_h2s = get_h2_topics(next_content)
    except Exception:
        next_h2s = []

    if next_h2s:
        preview = next_h2s[0].lower()
        if len(next_h2s) > 1:
            preview_phrase = f"starting with {preview}"
        else:
            preview_phrase = f"focusing on {preview}"
    else:
        preview_phrase = f"building on the foundations established here"

    return (
        f'<div class="whats-next">\n'
        f'    <h2>What Comes Next</h2>\n'
        f'    <p>In this section we covered {topic_summary}. '
        f'In <a href="{next_file.name}">{next_title_display}</a>, '
        f'we continue {preview_phrase}.</p>\n'
        f'</div>'
    )


def find_target_files() -> list[Path]:
    """Find all section HTML files under part-*/ and appendices/ that have TODO whats-next."""
    targets = []
    for pattern in ["part-*/**/section-*.html", "appendices/**/section-*.html"]:
        for f in sorted(BOOK_ROOT.glob(pattern)):
            # Skip _archive directories
            if "_archive" in str(f):
                continue
            try:
                text = f.read_text(encoding="utf-8")
            except Exception:
                continue
            if TODO_MARKER in text and WHATS_NEXT_RE.search(text):
                targets.append(f)
    return targets


def main():
    parser = argparse.ArgumentParser(description="Fix TODO whats-next sections")
    parser.add_argument("--fix", action="store_true", help="Apply changes (default is dry-run)")
    args = parser.parse_args()

    targets = find_target_files()
    print(f"Found {len(targets)} files with TODO whats-next blocks.\n")

    fixed = 0
    skipped = 0

    for filepath in targets:
        content = filepath.read_text(encoding="utf-8")
        next_file = find_next_section(filepath)

        replacement = generate_replacement(filepath, content, next_file)
        if replacement is None:
            print(f"  SKIP  {filepath.relative_to(BOOK_ROOT)} (could not generate)")
            skipped += 1
            continue

        new_content = WHATS_NEXT_RE.sub(replacement, content)

        if new_content == content:
            print(f"  SKIP  {filepath.relative_to(BOOK_ROOT)} (no regex match)")
            skipped += 1
            continue

        rel = filepath.relative_to(BOOK_ROOT)
        next_label = next_file.name if next_file else "(end of chapter)"

        if args.fix:
            filepath.write_text(new_content, encoding="utf-8")
            print(f"  FIXED {rel}  ->  {next_label}")
        else:
            print(f"  WOULD FIX {rel}  ->  {next_label}")
            # Show the generated block
            # Extract just the <p> line for preview
            p_match = re.search(r"<p>(.*?)</p>", replacement, re.DOTALL)
            if p_match:
                preview = p_match.group(1).strip()
                # Truncate long previews
                if len(preview) > 200:
                    preview = preview[:200] + "..."
                print(f"            {preview}")
            print()

        fixed += 1

    print(f"\n{'Applied' if args.fix else 'Would apply'}: {fixed} fixes, {skipped} skipped")


if __name__ == "__main__":
    main()
