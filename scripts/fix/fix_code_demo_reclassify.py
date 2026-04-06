"""
Reclassify practical-example callouts that are really code demos as library-shortcut.

Logic: If a <div class="callout practical-example"> contains a <pre> tag, it is likely
a code demonstration, not a real-world scenario. Reclassify it as library-shortcut.

Exceptions (do NOT reclassify):
  - Contains narrative markers like <strong>Who:</strong> or <strong>Situation:</strong>
  - Title contains scenario-context words (team, company, engineer, debugging, etc.)

Usage:
  python fix_code_demo_reclassify.py          # dry run (report only)
  python fix_code_demo_reclassify.py --fix     # apply changes
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
]

# Narrative markers that indicate a genuine real-world scenario (even with code)
NARRATIVE_MARKERS = [
    r"<strong>\s*Who\s*:\s*</strong>",
    r"<strong>\s*Situation\s*:\s*</strong>",
    r"<strong>\s*Context\s*:\s*</strong>",
    r"<strong>\s*Background\s*:\s*</strong>",
    r"<strong>\s*Challenge\s*:\s*</strong>",
    r"<strong>\s*Setting\s*:\s*</strong>",
    r"<strong>\s*Company\s*:\s*</strong>",
    r"<strong>\s*Role\s*:\s*</strong>",
    r"<strong>\s*Team\s*:\s*</strong>",
]
NARRATIVE_RE = re.compile("|".join(NARRATIVE_MARKERS), re.IGNORECASE)

# Words in the title that indicate a genuine scenario
SCENARIO_WORDS = re.compile(
    r"\b(team|company|engineer|debugging|startup|production|incident|outage|migration"
    r"|developer|architect|manager|org|organization|deploy|postmortem|case\s+study)\b",
    re.IGNORECASE,
)

# Regex to find the full callout block.  We match the opening div, then grab
# everything up to the NEXT callout div or a closing </div> at the same depth.
# Because callouts can be deeply nested, we use a simpler strategy: find the
# opening tag, then count div depth to locate the matching </div>.
OPEN_RE = re.compile(
    r'<div\s+class="callout\s+practical-example">', re.IGNORECASE
)


def extract_block(html: str, match_start: int) -> tuple[str, int, int]:
    """Return (block_text, start, end) for the div starting at match_start."""
    depth = 0
    i = match_start
    while i < len(html):
        if html[i:].startswith("<div"):
            depth += 1
            i += 4
        elif html[i:].startswith("</div>"):
            depth -= 1
            if depth == 0:
                end = i + len("</div>")
                return html[match_start:end], match_start, end
            i += 6
        else:
            i += 1
    # If we never closed, return to end of file
    return html[match_start:], match_start, len(html)


def should_skip(block: str, title: str) -> str | None:
    """Return a reason string if this block should NOT be reclassified, else None."""
    if NARRATIVE_RE.search(block):
        return "has narrative markers"
    if SCENARIO_WORDS.search(title):
        return f"title has scenario word"
    return None


def reclassify_block(block: str) -> str:
    """Reclassify a practical-example block to library-shortcut."""
    # Change class
    new = block.replace(
        'class="callout practical-example"',
        'class="callout library-shortcut"',
        1,
    )
    # Change title: "Real-World Scenario: X" -> "Library Shortcut: X"
    # Handle both <div class="callout-title"> and <h4> patterns
    # Also handle "Real-World Scenario" with no subtitle
    for open_tag, close_tag in [
        (r'(<div\s+class="callout-title">)', r"(</div>)"),
        (r"(<h4>)", r"(</h4>)"),
    ]:
        new = re.sub(
            open_tag + r"\s*Real-World Scenario\s*:\s*",
            lambda m: m.group(1) + "Library Shortcut: ",
            new,
        )
        new = re.sub(
            open_tag + r"\s*Real-World Scenario\s*" + close_tag,
            lambda m: m.group(1) + "Library Shortcut" + m.group(2),
            new,
        )
    return new


def process_file(filepath: Path, fix: bool) -> list[dict]:
    """Process one HTML file. Returns list of findings."""
    html = filepath.read_text(encoding="utf-8")
    findings = []

    # Collect all matches first (so we can replace backwards to preserve offsets)
    matches = []
    for m in OPEN_RE.finditer(html):
        block, start, end = extract_block(html, m.start())
        matches.append((block, start, end))

    if not matches:
        return findings

    # Process in reverse order so replacements don't shift offsets
    new_html = html
    changed = False
    for block, start, end in reversed(matches):
        has_pre = "<pre" in block.lower()
        if not has_pre:
            continue

        # Extract title (callouts use <div class="callout-title"> or <h4>)
        title_m = re.search(r'<div\s+class="callout-title">(.*?)</div>', block, re.DOTALL)
        if not title_m:
            title_m = re.search(r"<h4>(.*?)</h4>", block, re.DOTALL)
        title = title_m.group(1).strip() if title_m else ""

        reason = should_skip(block, title)
        rel = filepath.relative_to(BOOK_ROOT)
        if reason:
            findings.append({
                "file": str(rel),
                "title": title,
                "action": "SKIP",
                "reason": reason,
            })
            continue

        findings.append({
            "file": str(rel),
            "title": title,
            "action": "RECLASSIFY",
            "reason": "contains <pre> without narrative markers",
        })

        if fix:
            replacement = reclassify_block(block)
            new_html = new_html[:start] + replacement + new_html[end:]
            changed = True

    if fix and changed:
        filepath.write_text(new_html, encoding="utf-8")

    return findings


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fix", action="store_true", help="Apply changes (default: dry run)")
    args = parser.parse_args()

    html_files = []
    for d in SCAN_DIRS:
        if not d.exists():
            continue
        for f in sorted(d.rglob("*.html")):
            if "_archive" in str(f):
                continue
            html_files.append(f)

    print(f"Scanning {len(html_files)} HTML files...")
    print(f"Mode: {'FIX' if args.fix else 'DRY RUN'}\n")

    all_findings = []
    for f in html_files:
        findings = process_file(f, fix=args.fix)
        all_findings.extend(findings)

    reclassified = [f for f in all_findings if f["action"] == "RECLASSIFY"]
    skipped = [f for f in all_findings if f["action"] == "SKIP"]

    if reclassified:
        print(f"=== RECLASSIFY ({len(reclassified)}) ===")
        for f in reclassified:
            print(f"  {f['file']}")
            print(f"    Title: {f['title']}")
            print(f"    Reason: {f['reason']}")
            print()

    if skipped:
        print(f"=== SKIPPED ({len(skipped)}) ===")
        for f in skipped:
            print(f"  {f['file']}")
            print(f"    Title: {f['title']}")
            print(f"    Reason: {f['reason']}")
            print()

    print(f"Summary: {len(reclassified)} to reclassify, {len(skipped)} skipped")
    if not args.fix and reclassified:
        print("Run with --fix to apply changes.")


if __name__ == "__main__":
    main()
