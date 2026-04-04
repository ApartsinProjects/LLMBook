"""
Generate _status.md files for every chapter directory in the textbook.

Scans all part-*/module-*/ directories, inspects HTML files for key elements,
and writes a per-chapter status file with the results.
"""

import os
import re
import glob

AUDIT_DATE = "2026-03-28"
AUDIT_AGENT = "automated scan"

ROOT = os.path.dirname(os.path.abspath(__file__))


def find_chapter_dirs():
    """Find all module directories matching part-*/module-*/."""
    pattern = os.path.join(ROOT, "part-*", "module-*")
    dirs = sorted(glob.glob(pattern))
    return [d for d in dirs if os.path.isdir(d)]


def get_html_files(chapter_dir):
    """Return list of index.html and section-*.html files in a chapter directory."""
    files = []
    index = os.path.join(chapter_dir, "index.html")
    if os.path.isfile(index):
        files.append(index)
    section_pattern = os.path.join(chapter_dir, "section-*.html")
    files.extend(sorted(glob.glob(section_pattern)))
    return files


def check_file(filepath):
    """Check a single HTML file for key elements. Returns a dict of results."""
    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()

    # Remove nav-footer region for cross-ref counting
    # Find the nav-footer and strip it out for cross-ref analysis
    nav_footer_pattern = re.compile(r'<nav\s+class="nav-footer".*?</nav>', re.DOTALL)
    content_no_nav = nav_footer_pattern.sub("", content)

    results = {}

    # Boolean checks (present/absent)
    results["epigraph"] = 'class="epigraph"' in content
    results["prerequisites"] = 'class="prerequisites"' in content
    results["key_insight"] = 'class="callout key-insight"' in content
    results["practical_example"] = 'class="callout practical-example"' in content
    results["fun_note"] = 'class="callout fun-note"' in content
    results["research_frontier"] = (
        'class="callout research-frontier"' in content
        or 'class="research-frontier"' in content
    )
    results["labs"] = 'class="lab"' in content
    results["whats_next"] = 'class="whats-next"' in content
    results["bibliography"] = 'class="bibliography"' in content
    results["nav_footer"] = 'class="nav-footer"' in content

    # Count checks
    results["code_captions"] = len(re.findall(r'class="code-caption"', content))
    results["illustrations"] = len(re.findall(r'class="illustration"|<figure', content))

    # Cross-refs: count href= links to other chapters, excluding nav-footer links
    # Look for hrefs pointing to other module directories or sections
    cross_ref_links = re.findall(r'href="[^"]*"', content_no_nav)
    cross_chapter_count = 0
    for link in cross_ref_links:
        href = link[6:-1]  # strip href=" and trailing "
        # Count links that go to other modules (contain "module-" or "../module-" or "part-")
        if re.search(r'module-|part-\d|section-\d', href):
            # Exclude self-references (same directory)
            if ".." in href or "part-" in href:
                cross_chapter_count += 1
    results["cross_refs"] = cross_chapter_count

    return results


def bool_to_mark(val):
    """Convert boolean to status mark."""
    return "\u2713" if val else "\u2717"


def extract_chapter_info(chapter_dir):
    """Extract chapter number and title from the directory name and index.html."""
    dirname = os.path.basename(chapter_dir)
    # Extract module number from directory name like "module-05-decoding-text-generation"
    match = re.match(r"module-(\d+)-(.*)", dirname)
    if match:
        num = int(match.group(1))
        slug = match.group(2).replace("-", " ").title()
    else:
        num = 0
        slug = dirname

    # Try to get actual title from index.html
    index_path = os.path.join(chapter_dir, "index.html")
    title = slug
    if os.path.isfile(index_path):
        with open(index_path, "r", encoding="utf-8", errors="replace") as f:
            html = f.read()
        # Look for <h1> or <title> to get a better title
        h1_match = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.DOTALL)
        if h1_match:
            raw = h1_match.group(1)
            # Strip HTML tags from the title
            title = re.sub(r"<[^>]+>", "", raw).strip()

    return num, title


def generate_status(chapter_dir):
    """Generate and write _status.md for a chapter directory."""
    num, title = extract_chapter_info(chapter_dir)
    html_files = get_html_files(chapter_dir)

    if not html_files:
        return

    # Collect results per file
    file_results = []
    for filepath in html_files:
        fname = os.path.basename(filepath)
        results = check_file(filepath)
        file_results.append((fname, results))

    # Build the status table
    header = "| File | Epigraph | Prerequisites | Key-Insight | Practical-Example | Fun-Note | Research-Frontier | Code-Captions | Cross-Refs | Illustrations | Labs | What's-Next | Bibliography | Nav-Footer |"
    separator = "|------|----------|---------------|-------------|-------------------|----------|-------------------|---------------|------------|---------------|------|-------------|--------------|------------|"

    rows = []
    for fname, r in file_results:
        row = "| {} | {} | {} | {} | {} | {} | {} | {} | {} | {} | {} | {} | {} | {} |".format(
            fname,
            bool_to_mark(r["epigraph"]),
            bool_to_mark(r["prerequisites"]),
            bool_to_mark(r["key_insight"]),
            bool_to_mark(r["practical_example"]),
            bool_to_mark(r["fun_note"]),
            bool_to_mark(r["research_frontier"]),
            r["code_captions"],
            r["cross_refs"],
            r["illustrations"],
            bool_to_mark(r["labs"]),
            bool_to_mark(r["whats_next"]),
            bool_to_mark(r["bibliography"]),
            bool_to_mark(r["nav_footer"]),
        )
        rows.append(row)

    table = "\n".join([header, separator] + rows)

    status_content = """# Chapter Status: Chapter {num}, {title}

**Last Audit:** {date} by {agent}

## Per-File Status

{table}

Legend: \u2713 = pass, \u2717 = absent/fail, number = count of occurrences

## Backlog

<!-- Add checkbox items for issues that need specialist dispatch -->

## Audit History

- {date}: Initial status generated by automated scan
""".format(
        num=num,
        title=title,
        date=AUDIT_DATE,
        agent=AUDIT_AGENT,
        table=table,
    )

    output_path = os.path.join(chapter_dir, "_status.md")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(status_content)

    print(f"  Wrote: {output_path}")


def main():
    chapter_dirs = find_chapter_dirs()
    print(f"Found {len(chapter_dirs)} chapter directories.\n")

    for chapter_dir in chapter_dirs:
        rel = os.path.relpath(chapter_dir, ROOT)
        print(f"Processing: {rel}")
        generate_status(chapter_dir)

    print(f"\nDone. Generated _status.md for {len(chapter_dirs)} chapters.")


if __name__ == "__main__":
    main()
