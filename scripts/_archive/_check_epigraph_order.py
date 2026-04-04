"""Check for section files where epigraph/prerequisites appear before <main class="content">."""

import glob
import os

base = r"E:\Projects\LLMCourse"
pattern = os.path.join(base, "**", "section-*.html")
files = sorted(glob.glob(pattern, recursive=True))

flagged = []

for fpath in files:
    with open(fpath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    main_line = None
    epigraph_line = None
    prereq_line = None

    for i, line in enumerate(lines, 1):
        if '<main class="content">' in line and main_line is None:
            main_line = i
        if '<blockquote class="epigraph">' in line and epigraph_line is None:
            epigraph_line = i
        if '<div class="prerequisites">' in line and prereq_line is None:
            prereq_line = i

    issues = []
    if main_line is None:
        issues.append("NO <main> tag found")
    if epigraph_line and main_line and epigraph_line < main_line:
        issues.append(f"epigraph on line {epigraph_line} BEFORE main on line {main_line}")
    if prereq_line and main_line and prereq_line < main_line:
        issues.append(f"prerequisites on line {prereq_line} BEFORE main on line {main_line}")

    if issues:
        rel = os.path.relpath(fpath, base)
        flagged.append((rel, issues))

print(f"Scanned {len(files)} section files.\n")

if flagged:
    print(f"FLAGGED: {len(flagged)} files with wrong ordering:\n")
    for rel, issues in flagged:
        for issue in issues:
            print(f"  {rel}: {issue}")
else:
    print("All files have correct ordering.")
