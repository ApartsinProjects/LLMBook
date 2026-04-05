"""Audit section numbering consistency across the LLM Course textbook."""

import os
import re
import glob
from collections import defaultdict

BASE = r"E:\Projects\LLMCourse"

def find_section_files():
    """Find all section-*.html files in the expected locations."""
    patterns = [
        os.path.join(BASE, "part-*", "module-*", "section-*.html"),
        os.path.join(BASE, "appendices", "*", "section-*.html"),
        os.path.join(BASE, "front-matter", "section-*.html"),
    ]
    files = []
    for p in patterns:
        files.extend(glob.glob(p))
    return sorted(files)

def extract_section_from_filename(filepath):
    """Extract section number from filename, e.g. section-9.2.html -> '9.2'"""
    basename = os.path.basename(filepath)
    m = re.match(r"section-(.+)\.html$", basename)
    return m.group(1) if m else None

def extract_chapter_from_dir(filepath):
    """Extract chapter number from directory name.
    module-09-xxx -> '9', appendix-a-xxx -> 'a', front-matter -> 'fm'
    """
    parent = os.path.basename(os.path.dirname(filepath))
    # module directories
    m = re.match(r"module-(\d+)", parent)
    if m:
        return str(int(m.group(1)))  # strip leading zeros
    # appendix directories
    m = re.match(r"appendix-([a-z])", parent)
    if m:
        return m.group(1)
    # front-matter
    if parent == "front-matter":
        return "fm"
    return None

def extract_part_from_path(filepath):
    """Extract part number from path, e.g. part-3-xxx -> 3"""
    parts = filepath.replace("\\", "/").split("/")
    for p in parts:
        m = re.match(r"part-(\d+)", p)
        if m:
            return int(m.group(1))
    return None

def read_html(filepath):
    """Read file content."""
    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        return f.read()

def extract_title_section(html):
    """Extract section number from <title> tag. e.g. 'Section 1.2: ...' -> '1.2'"""
    m = re.search(r"<title>\s*Section\s+([\w.]+)\s*:", html)
    return m.group(1) if m else None

def extract_h1(html):
    """Extract h1 content."""
    m = re.search(r"<h1>(.*?)</h1>", html, re.DOTALL)
    return m.group(1).strip() if m else None

def extract_h1_section_number(h1_text):
    """If h1 starts with a section number like '9.2 ...', extract it."""
    if not h1_text:
        return None
    # Clean HTML entities and tags
    clean = re.sub(r"<[^>]+>", "", h1_text)
    clean = clean.replace("&amp;", "&").strip()
    m = re.match(r"^([\d]+\.[\d.]+)\s", clean)
    return m.group(1) if m else None

def extract_part_label(html):
    """Extract part number from <div class="part-label">"""
    m = re.search(r'class="part-label"[^>]*>.*?Part\s+(\d+)', html, re.DOTALL)
    return int(m.group(1)) if m else None

def extract_chapter_label(html):
    """Extract chapter number from <div class="chapter-label">"""
    m = re.search(r'class="chapter-label"[^>]*>.*?Chapter\s+(\d+)', html, re.DOTALL)
    if m:
        return str(int(m.group(1)))  # strip leading zeros
    # Check for appendix pattern
    m = re.search(r'class="chapter-label"[^>]*>.*?Appendix\s+([A-Za-z])', html, re.DOTALL)
    if m:
        return m.group(1).lower()
    return None

def extract_h2_numbers(html, section_prefix):
    """Extract sub-section numbers from h2 headings matching prefix like 9.2.1"""
    numbers = []
    for m in re.finditer(r"<h2[^>]*>(.*?)</h2>", html, re.DOTALL):
        h2_text = re.sub(r"<[^>]+>", "", m.group(1)).strip()
        # Look for sub-section numbers
        nm = re.match(r"^([\d]+\.[\d]+\.[\d]+)", h2_text)
        if nm:
            numbers.append(nm.group(1))
    return numbers

def get_section_prefix(section_id):
    """Get the chapter prefix from a section id. '9.2' -> '9', 'a.3' -> 'a', 'fm.1' -> 'fm'"""
    parts = section_id.split(".")
    return parts[0] if parts else None

def main():
    files = find_section_files()
    print(f"Found {len(files)} section files\n")

    issues = []
    # Group sections by chapter for gap detection
    chapters = defaultdict(list)

    for filepath in files:
        relpath = os.path.relpath(filepath, BASE).replace("\\", "/")
        fn_section = extract_section_from_filename(filepath)
        dir_chapter = extract_chapter_from_dir(filepath)
        path_part = extract_part_from_path(filepath)

        if fn_section is None:
            issues.append(("PARSE ERROR", relpath, "Could not extract section from filename"))
            continue

        html = read_html(filepath)
        title_section = extract_title_section(html)
        h1_text = extract_h1(html)
        h1_section = extract_h1_section_number(h1_text)
        part_label = extract_part_label(html)
        chapter_label = extract_chapter_label(html)

        # Determine the section prefix (chapter part)
        section_prefix = get_section_prefix(fn_section)

        # Track for gap detection
        chapters[section_prefix].append((fn_section, relpath))

        # CHECK 1: Filename section matches directory chapter
        if dir_chapter and section_prefix != dir_chapter:
            issues.append(("CHAPTER/DIRECTORY MISMATCH", relpath,
                f"File in directory for chapter '{dir_chapter}' but section number is '{fn_section}'"))

        # CHECK 2: Title tag section matches filename section
        if title_section and title_section != fn_section:
            issues.append(("FILENAME/TITLE MISMATCH", relpath,
                f"Filename says '{fn_section}' but <title> says '{title_section}'"))

        # CHECK 3: If h1 has a section number, it should match
        if h1_section and h1_section != fn_section:
            issues.append(("FILENAME/HEADING MISMATCH", relpath,
                f"Filename says '{fn_section}' but h1 says '{h1_section}'"))

        # CHECK 4: Part label matches actual part
        if path_part is not None and part_label is not None:
            if part_label != path_part:
                issues.append(("PART LABEL ERROR", relpath,
                    f"File is in part-{path_part} but header says Part {part_label}"))

        # CHECK 5: Chapter label matches section number
        if chapter_label is not None and section_prefix != chapter_label:
            # For numeric chapters, compare as strings
            issues.append(("CHAPTER LABEL MISMATCH", relpath,
                f"Chapter label says '{chapter_label}' but section is '{fn_section}'"))

        # CHECK 6: Title tag missing
        if title_section is None and not fn_section.startswith("fm"):
            issues.append(("MISSING TITLE SECTION", relpath,
                f"No 'Section X.Y:' pattern found in <title> tag"))

        # CHECK 7: Sub-section h2 numbering
        h2_numbers = extract_h2_numbers(html, fn_section)
        if h2_numbers:
            # Check prefix
            for num in h2_numbers:
                if not num.startswith(fn_section + "."):
                    issues.append(("H2 PREFIX MISMATCH", relpath,
                        f"Sub-section '{num}' doesn't match section '{fn_section}'"))
            # Check sequential
            sub_nums = []
            for num in h2_numbers:
                suffix = num.split(".")[-1]
                try:
                    sub_nums.append(int(suffix))
                except ValueError:
                    pass
            if sub_nums:
                expected = list(range(sub_nums[0], sub_nums[0] + len(sub_nums)))
                if sub_nums != expected:
                    issues.append(("SUB-SECTION GAPS", relpath,
                        f"h2 sub-section numbers: {h2_numbers} (not sequential)"))

    # CHECK 8: Missing sections within chapters (gap detection)
    print("=" * 80)
    print("SECTION GAP ANALYSIS (missing sections within a chapter)")
    print("=" * 80)
    gap_found = False
    for chapter_id in sorted(chapters.keys(), key=lambda x: (0, int(x)) if x.isdigit() else (1, x)):
        sections = chapters[chapter_id]
        # Extract the sub-number for each section
        sub_numbers = []
        for sec_id, relpath in sections:
            parts = sec_id.split(".")
            if len(parts) >= 2:
                try:
                    sub_numbers.append(int(parts[1]))
                except ValueError:
                    # Handle things like 'fm.1a'
                    m = re.match(r"(\d+)", parts[1])
                    if m:
                        sub_numbers.append(int(m.group(1)))
        if not sub_numbers:
            continue
        sub_numbers_sorted = sorted(set(sub_numbers))
        # Check for gaps (starting from 1 or the minimum)
        min_n = sub_numbers_sorted[0]
        max_n = sub_numbers_sorted[-1]
        expected = list(range(min_n, max_n + 1))
        missing = [n for n in expected if n not in sub_numbers_sorted]
        if missing:
            gap_found = True
            existing = [f"{chapter_id}.{n}" for n in sub_numbers_sorted]
            missing_ids = [f"{chapter_id}.{n}" for n in missing]
            print(f"  MISSING SECTIONS in chapter '{chapter_id}': have {existing}, missing {missing_ids}")
            issues.append(("MISSING SECTIONS", f"chapter {chapter_id}",
                f"Existing: {existing}, Missing: {missing_ids}"))
    if not gap_found:
        print("  No gaps detected.\n")

    # Print all issues
    print()
    print("=" * 80)
    print("DETAILED ISSUE REPORT")
    print("=" * 80)

    if not issues:
        print("  No issues found!")
    else:
        # Group by issue type
        by_type = defaultdict(list)
        for issue_type, location, detail in issues:
            by_type[issue_type].append((location, detail))

        for issue_type in sorted(by_type.keys()):
            items = by_type[issue_type]
            print(f"\n--- {issue_type} ({len(items)} issue(s)) ---")
            for location, detail in items:
                print(f"  [{location}]")
                print(f"    {detail}")

    print(f"\n{'=' * 80}")
    print(f"SUMMARY: {len(issues)} issue(s) found across {len(files)} section files")
    print(f"{'=' * 80}")

    # Also print a chapter inventory
    print(f"\nCHAPTER INVENTORY:")
    for chapter_id in sorted(chapters.keys(), key=lambda x: (0, int(x)) if x.isdigit() else (1, x)):
        sections = chapters[chapter_id]
        sec_ids = sorted([s[0] for s in sections])
        print(f"  Chapter {chapter_id}: {sec_ids}")

if __name__ == "__main__":
    main()
