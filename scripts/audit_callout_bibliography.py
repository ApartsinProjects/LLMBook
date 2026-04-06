#!/usr/bin/env python3
"""Audit callout icons and bibliography format/placement across the book.

Checks:
1. Bibliography format: old <ul class="bibliography"> vs new <section class="bibliography">
2. Stray bibliography-title elements outside <section class="bibliography">
3. Bibliography position: must appear AFTER takeaways/self-check, BEFORE <nav class="chapter-nav">
4. Duplicate callout icons: inline emoji/img in callout-title when CSS already adds ::before icon
"""

import os
import re
import sys
from pathlib import Path

# ── Configuration ──────────────────────────────────────────────────────────

BOOK_ROOT = Path(__file__).resolve().parent.parent
SKIP_DIRS = {
    "_archive", "scripts", "agents", ".claude", ".git", "node_modules",
    "styles", "images", "__pycache__", "drift-detector",
}

# Emoji unicode ranges that could duplicate the CSS ::before icon
# Covers common emoji blocks: Miscellaneous Symbols, Dingbats, Emoticons,
# Transport, Supplemental Symbols, etc.
EMOJI_RE = re.compile(
    r"[\U0001F300-\U0001F9FF"   # Miscellaneous Symbols and Pictographs .. Supplemental
    r"\U00002600-\U000027BF"     # Misc symbols, Dingbats
    r"\U0000FE00-\U0000FE0F"     # Variation selectors
    r"\U0000200D"                 # Zero-width joiner
    r"\U00002702-\U000027B0"     # Dingbats
    r"\U0001FA00-\U0001FA6F"     # Chess symbols, extended-A
    r"\U0001FA70-\U0001FAFF"     # Symbols extended-A
    r"]"
)

# HTML numeric character references for emoji (&#128161; = light bulb, etc.)
HTML_ENTITY_EMOJI_RE = re.compile(r"&#(\d+);")


def collect_html_files(root: Path) -> list[Path]:
    """Recursively collect .html files, skipping non-content directories."""
    results = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for f in filenames:
            if f.endswith(".html"):
                results.append(Path(dirpath) / f)
    return sorted(results)


def relative(path: Path) -> str:
    try:
        return str(path.relative_to(BOOK_ROOT))
    except ValueError:
        return str(path)


# ── Check 1: Old vs new bibliography format ───────────────────────────────

def check_bibliography_format(files: list[Path]) -> tuple[list, list, list]:
    """Return (old_format_files, new_format_files, div_bibliography_files)."""
    old_fmt = []    # <ul class="bibliography">
    new_fmt = []    # <section class="bibliography">
    div_fmt = []    # <div class="bibliography"> (also old)

    ul_pat = re.compile(r'<ul\s[^>]*class="bibliography"', re.IGNORECASE)
    sec_pat = re.compile(r'<section\s[^>]*class="bibliography"', re.IGNORECASE)
    div_pat = re.compile(r'<div\s[^>]*class="bibliography"', re.IGNORECASE)

    for f in files:
        text = f.read_text(encoding="utf-8", errors="replace")
        has_ul = bool(ul_pat.search(text))
        has_sec = bool(sec_pat.search(text))
        has_div = bool(div_pat.search(text))
        if has_ul:
            old_fmt.append(f)
        if has_div:
            div_fmt.append(f)
        if has_sec:
            new_fmt.append(f)
    return old_fmt, new_fmt, div_fmt


# ── Check 2: Stray bibliography-title outside <section class="bibliography">

def check_stray_bib_titles(files: list[Path]) -> list[tuple[Path, int]]:
    """Find bibliography-title divs NOT inside a <section class="bibliography">."""
    results = []
    title_pat = re.compile(r'<div\s+class="bibliography-title"')
    sec_open = re.compile(r'<section\s[^>]*class="bibliography"')
    sec_close = re.compile(r'</section>')

    for f in files:
        text = f.read_text(encoding="utf-8", errors="replace")
        lines = text.split("\n")
        inside_bib_section = False
        for i, line in enumerate(lines, 1):
            if sec_open.search(line):
                inside_bib_section = True
            if sec_close.search(line) and inside_bib_section:
                inside_bib_section = False
            if title_pat.search(line) and not inside_bib_section:
                results.append((f, i))
    return results


# ── Check 3: Bibliography position ────────────────────────────────────────

def check_bibliography_position(files: list[Path]) -> list[tuple[Path, str]]:
    """Check bibliography appears AFTER takeaways/self-check, BEFORE chapter-nav."""
    issues = []
    bib_pat = re.compile(r'class="bibliography"')
    nav_pat = re.compile(r'<nav\s[^>]*class="chapter-nav"')
    takeaway_pat = re.compile(r'class="callout\s+key-takeaway"')
    selfcheck_pat = re.compile(r'class="callout\s+self-check"')
    whatsnext_pat = re.compile(r'class="whats-next"')

    for f in files:
        text = f.read_text(encoding="utf-8", errors="replace")
        bib_match = bib_pat.search(text)
        if not bib_match:
            continue

        bib_pos = bib_match.start()
        nav_match = nav_pat.search(text)

        # Check: bibliography must come BEFORE chapter-nav
        if nav_match and bib_pos > nav_match.start():
            issues.append((f, "Bibliography appears AFTER <nav class='chapter-nav'>"))

        # Check: bibliography should come after key-takeaway if present
        takeaway_matches = list(takeaway_pat.finditer(text))
        if takeaway_matches:
            last_takeaway_pos = takeaway_matches[-1].start()
            if bib_pos < last_takeaway_pos:
                issues.append((f, "Bibliography appears BEFORE last key-takeaway callout"))

        # Check: bibliography should come after self-check if present
        selfcheck_matches = list(selfcheck_pat.finditer(text))
        if selfcheck_matches:
            last_sc_pos = selfcheck_matches[-1].start()
            if bib_pos < last_sc_pos:
                issues.append((f, "Bibliography appears BEFORE last self-check callout"))

        # Check: bibliography should come after whats-next if present
        whatsnext_matches = list(whatsnext_pat.finditer(text))
        if whatsnext_matches:
            last_wn_pos = whatsnext_matches[-1].start()
            if bib_pos < last_wn_pos:
                issues.append((f, "Bibliography appears BEFORE whats-next section"))

    return issues


# ── Check 4: Duplicate callout icons ──────────────────────────────────────

def is_emoji_codepoint(cp: int) -> bool:
    """Check if a Unicode codepoint is in common emoji ranges."""
    emoji_ranges = [
        (0x2600, 0x27BF),    # Misc Symbols, Dingbats
        (0x2702, 0x27B0),
        (0xFE00, 0xFE0F),    # Variation selectors
        (0x1F300, 0x1F9FF),   # Misc Symbols & Pictographs through Supplemental
        (0x1FA00, 0x1FA6F),
        (0x1FA70, 0x1FAFF),
        (0x2B50, 0x2B50),     # Star
        (0x2733, 0x2734),     # Eight-spoked asterisk
        (0x2122, 0x2122),     # TM
        (0x23F0, 0x23FA),     # Clocks
        (0x200D, 0x200D),     # ZWJ
    ]
    return any(lo <= cp <= hi for lo, hi in emoji_ranges)


def check_duplicate_callout_icons(files: list[Path]) -> list[tuple[Path, int, str]]:
    """Find callout-title elements with inline emoji or <img> that duplicate CSS icon."""
    results = []
    # Match the callout-title tag and capture its inner content up to closing tag
    title_pat = re.compile(
        r'<(?:div|h3)\s+class="callout-title"[^>]*>(.*?)</(?:div|h3)>',
        re.DOTALL | re.IGNORECASE
    )

    for f in files:
        text = f.read_text(encoding="utf-8", errors="replace")
        lines = text.split("\n")

        for i, line in enumerate(lines, 1):
            m = title_pat.search(line)
            if not m:
                continue
            inner = m.group(1).strip()
            has_inline_icon = False
            reason = ""

            # Check for <img> tag
            if re.search(r"<img\s", inner, re.IGNORECASE):
                has_inline_icon = True
                reason = "contains <img> tag"

            # Check for Unicode emoji at the start of the text
            if not has_inline_icon and inner:
                # Strip leading whitespace and HTML tags to get to the text
                text_start = re.sub(r"<[^>]+>", "", inner).strip()
                if text_start and EMOJI_RE.match(text_start):
                    has_inline_icon = True
                    reason = f"starts with emoji: {text_start[:4]}"

            # Check for HTML numeric entity emoji (&#128161; etc.)
            if not has_inline_icon:
                entity_match = HTML_ENTITY_EMOJI_RE.search(inner)
                if entity_match:
                    cp = int(entity_match.group(1))
                    if is_emoji_codepoint(cp):
                        has_inline_icon = True
                        reason = f"contains emoji entity &#{ cp};"

            if has_inline_icon:
                # Get a short preview of the title content
                preview = inner[:60].replace("\n", " ")
                results.append((f, i, f"{reason} | {preview}"))

    return results


# ── Main ──────────────────────────────────────────────────────────────────

def main():
    print("=" * 78)
    print("  CALLOUT & BIBLIOGRAPHY AUDIT")
    print(f"  Book root: {BOOK_ROOT}")
    print("=" * 78)

    files = collect_html_files(BOOK_ROOT)
    print(f"\nScanned {len(files)} HTML files.\n")

    # ── Check 1 ──
    print("-" * 78)
    print("CHECK 1: Bibliography Format (old plain-list vs new card format)")
    print("-" * 78)
    old_ul, new_sec, old_div = check_bibliography_format(files)

    if old_ul:
        print(f"\n  [FAIL] {len(old_ul)} file(s) use OLD <ul class='bibliography'> format:")
        for f in old_ul:
            print(f"    - {relative(f)}")
    else:
        print("\n  [OK] No files use <ul class='bibliography'> (old plain-list format).")

    if old_div:
        print(f"\n  [WARN] {len(old_div)} file(s) use <div class='bibliography'> (should be <section>):")
        for f in old_div:
            print(f"    - {relative(f)}")
    else:
        print("\n  [OK] No files use <div class='bibliography'> (all use <section>).")

    print(f"\n  [INFO] {len(new_sec)} file(s) use correct <section class='bibliography'> format.")

    # ── Check 2 ──
    print("\n" + "-" * 78)
    print("CHECK 2: Stray bibliography-title Elements (orphaned, outside <section>)")
    print("-" * 78)
    stray = check_stray_bib_titles(files)
    if stray:
        print(f"\n  [FAIL] {len(stray)} orphaned bibliography-title element(s) found:")
        for f, line in stray:
            print(f"    - {relative(f)}  (line {line})")
    else:
        print("\n  [OK] All bibliography-title elements are inside <section class='bibliography'>.")

    # ── Check 3 ──
    print("\n" + "-" * 78)
    print("CHECK 3: Bibliography Position (after takeaways/self-check, before nav)")
    print("-" * 78)
    pos_issues = check_bibliography_position(files)
    if pos_issues:
        print(f"\n  [FAIL] {len(pos_issues)} position issue(s) found:")
        for f, msg in pos_issues:
            print(f"    - {relative(f)}: {msg}")
    else:
        print("\n  [OK] All bibliographies are correctly positioned.")

    # ── Check 4 ──
    print("\n" + "-" * 78)
    print("CHECK 4: Duplicate Callout Icons (inline icon + CSS ::before icon)")
    print("-" * 78)
    dup_icons = check_duplicate_callout_icons(files)
    if dup_icons:
        print(f"\n  [FAIL] {len(dup_icons)} callout-title(s) with inline icons (duplicates CSS ::before):")
        for f, line, detail in dup_icons:
            print(f"    - {relative(f)}  (line {line}): {detail}")
    else:
        print("\n  [OK] No duplicate callout icons found in content HTML files.")

    # ── Summary ──
    print("\n" + "=" * 78)
    print("  SUMMARY")
    print("=" * 78)
    total_issues = len(old_ul) + len(old_div) + len(stray) + len(pos_issues) + len(dup_icons)
    print(f"  Old <ul> bibliographies:      {len(old_ul)}")
    print(f"  Old <div> bibliographies:      {len(old_div)}")
    print(f"  New <section> bibliographies:  {len(new_sec)}")
    print(f"  Stray bibliography-titles:     {len(stray)}")
    print(f"  Position issues:               {len(pos_issues)}")
    print(f"  Duplicate callout icons:       {len(dup_icons)}")
    print(f"  TOTAL ISSUES:                  {total_issues}")
    print("=" * 78)

    return 1 if total_issues > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
