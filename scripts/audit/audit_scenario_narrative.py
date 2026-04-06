"""Audit real-world scenario callouts for conformance to standard narrative structure.

Standard markers (in order):
  Who, Situation, Problem, Decision/Dilemma, Result, Lesson

Minimum conformance: Who + Problem + Result + Lesson
Optional accepted markers: How, Scenario, Approach

Classifications:
  CONFORMING    - has at least the minimum required markers
  CODE_DEMO     - contains a <pre> tag (likely should be library-shortcut)
  NON_NARRATIVE - missing required markers
"""

from __future__ import annotations

import re
import sys
from html.parser import HTMLParser
from pathlib import Path

BOOK_ROOT = Path(r"E:/Projects/LLMCourse")

REQUIRED_MARKERS = {"Who", "Problem", "Result", "Lesson"}
FULL_MARKERS = {"Who", "Situation", "Problem", "Decision", "Dilemma", "Result", "Lesson"}
OPTIONAL_MARKERS = {"How", "Scenario", "Approach"}
ALL_KNOWN = FULL_MARKERS | OPTIONAL_MARKERS

# Regex to find <strong>Marker:</strong> patterns
MARKER_RE = re.compile(r"<strong>\s*([\w/]+)\s*:\s*</strong>", re.IGNORECASE)

# Regex to find the callout div opening
CALLOUT_OPEN_RE = re.compile(r'<div\s+class="callout\s+practical-example"', re.IGNORECASE)

# Regex to strip HTML tags
STRIP_HTML_RE = re.compile(r"<[^>]+>")


class TextExtractor(HTMLParser):
    """Simple HTML-to-text extractor."""

    def __init__(self):
        super().__init__()
        self.parts: list[str] = []

    def handle_data(self, data: str):
        self.parts.append(data)

    def get_text(self) -> str:
        return " ".join(self.parts)


def extract_text(html: str) -> str:
    ext = TextExtractor()
    ext.feed(html)
    return re.sub(r"\s+", " ", ext.get_text()).strip()


def extract_callout_blocks(file_path: Path) -> list[tuple[int, str]]:
    """Return list of (line_number, block_html) for each practical-example callout."""
    text = file_path.read_text(encoding="utf-8", errors="replace")
    lines = text.split("\n")
    blocks: list[tuple[int, str]] = []

    i = 0
    while i < len(lines):
        if CALLOUT_OPEN_RE.search(lines[i]):
            start_line = i + 1  # 1-indexed
            depth = 0
            block_lines: list[str] = []
            j = i
            while j < len(lines):
                line = lines[j]
                block_lines.append(line)
                depth += line.count("<div") - line.count("</div")
                if depth <= 0:
                    break
                j += 1
            blocks.append((start_line, "\n".join(block_lines)))
            i = j + 1
        else:
            i += 1

    return blocks


def extract_title(block_html: str) -> str:
    m = re.search(r'<div\s+class="callout-title">\s*(.*?)\s*</div>', block_html, re.DOTALL)
    if m:
        return extract_text(m.group(1))
    return "(no title)"


def classify_block(block_html: str) -> tuple[str, set[str], set[str]]:
    """Classify a block. Returns (classification, present_markers, missing_markers)."""
    markers_found: set[str] = set()
    for m in MARKER_RE.finditer(block_html):
        label = m.group(1).strip().title()
        if label in ALL_KNOWN:
            markers_found.add(label)
        # Handle Decision/Dilemma as equivalent
        if label == "Dilemma":
            markers_found.add("Decision")

    has_pre = "<pre" in block_html.lower()

    if has_pre and not markers_found:
        return "CODE_DEMO", markers_found, set()

    # Check minimum conformance: Who + Problem + Result + Lesson
    missing = REQUIRED_MARKERS - markers_found
    if not missing:
        return "CONFORMING", markers_found, set()

    return "NON_NARRATIVE", markers_found, missing


def main():
    scan_dirs = [
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
    ]

    html_files: list[Path] = []
    for d in scan_dirs:
        if d.exists():
            for f in sorted(d.rglob("*.html")):
                if "_archive" in str(f):
                    continue
                html_files.append(f)

    conforming: list[tuple[Path, int, str]] = []
    code_demo: list[tuple[Path, int, str]] = []
    non_narrative: list[tuple[Path, int, str, set[str], set[str], str]] = []

    total_blocks = 0
    for fp in html_files:
        blocks = extract_callout_blocks(fp)
        for line_no, block_html in blocks:
            total_blocks += 1
            title = extract_title(block_html)
            classification, present, missing = classify_block(block_html)
            rel = fp.relative_to(BOOK_ROOT)

            if classification == "CONFORMING":
                conforming.append((fp, line_no, title))
            elif classification == "CODE_DEMO":
                code_demo.append((fp, line_no, title))
            else:
                text_content = extract_text(block_html)
                non_narrative.append((fp, line_no, title, present, missing, text_content))

    # Print summary
    print("=" * 80)
    print("SCENARIO NARRATIVE AUDIT")
    print("=" * 80)
    print(f"Files scanned:        {len(html_files)}")
    print(f"Total callout blocks: {total_blocks}")
    print(f"  CONFORMING:         {len(conforming)}")
    print(f"  CODE_DEMO:          {len(code_demo)}")
    print(f"  NON_NARRATIVE:      {len(non_narrative)}")
    print()

    if code_demo:
        print("-" * 80)
        print("CODE_DEMO (contain <pre> but no narrative markers, likely should be library-shortcut)")
        print("-" * 80)
        for fp, line_no, title in code_demo:
            rel = fp.relative_to(BOOK_ROOT)
            print(f"  [{rel}:{line_no}] {title}")
        print()

    if non_narrative:
        print("-" * 80)
        print("NON_NARRATIVE (missing required markers)")
        print("-" * 80)
        for fp, line_no, title, present, missing, text_content in non_narrative:
            rel = fp.relative_to(BOOK_ROOT)
            present_str = ", ".join(sorted(present)) if present else "(none)"
            missing_str = ", ".join(sorted(missing))
            snippet = text_content[:200]
            print(f"\n  [{rel}:{line_no}]")
            print(f"  Title:   {title}")
            print(f"  Present: {present_str}")
            print(f"  Missing: {missing_str}")
            print(f"  Text:    {snippet}...")
        print()

    if conforming:
        print("-" * 80)
        print("CONFORMING (for reference)")
        print("-" * 80)
        for fp, line_no, title in conforming:
            rel = fp.relative_to(BOOK_ROOT)
            print(f"  [{rel}:{line_no}] {title}")
        print()

    # Exit code
    if non_narrative or code_demo:
        print(f"RESULT: {len(non_narrative)} non-narrative + {len(code_demo)} code-demo issues found.")
        sys.exit(1)
    else:
        print("RESULT: All scenarios conform to narrative structure.")
        sys.exit(0)


if __name__ == "__main__":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    main()
