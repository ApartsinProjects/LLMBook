"""Add level badges to all h2 headings in section-*.html files."""

import re
import os
import glob

ROOT = r"E:\Projects\LLMCourse"

# Keyword rules for badge assignment (case-insensitive matching)
RULES = [
    ("basic", [
        r"\bintroduction\b", r"\bwhat is\b", r"\boverview\b", r"\bbasics\b",
        r"\bfoundation\b", r"\bfoundations\b", r"\bdefinition\b", r"\bdefining\b",
        r"\bwhy\b.*\bmatter", r"\bkey concepts\b", r"\bcore concepts\b",
        r"\bterminology\b", r"\bvocabulary\b", r"\banatomy\b",
        r"\bwhat are\b", r"\bmotivation\b", r"\bintuition\b",
    ]),
    ("intermediate", [
        r"\bimplementation\b", r"\bbuilding\b", r"\btraining\b",
        r"\bhow\b", r"\bworking with\b", r"\bpractical\b",
        r"\btechniques\b", r"\bmethods\b", r"\barchitecture\b",
        r"\bdesign\b", r"\bframework\b", r"\bpipeline\b",
        r"\bcomparison\b", r"\bcomparing\b", r"\bevaluation\b",
        r"\btools\b", r"\becosystem\b", r"\busing\b",
        r"\bapplying\b", r"\bapplications\b",
    ]),
    ("advanced", [
        r"\badvanced\b", r"\boptimization\b", r"\bproduction\b",
        r"\bscaling\b", r"\bperformance\b", r"\bedge cases\b",
        r"\bdeployment\b", r"\bmonitoring\b", r"\bguardrails\b",
        r"\bsecurity\b", r"\bcost\b", r"\blatency\b",
        r"\bdistributed\b", r"\bmemory management\b",
    ]),
    ("research", [
        r"\bresearch\b", r"\bfrontier\b", r"\bfrontiers\b",
        r"\bopen problems\b", r"\bfuture\b", r"\bemerging\b",
        r"\brecent\b", r"\bstate.of.the.art\b", r"\bnovel\b",
        r"\bbeyond\b", r"\bopen questions\b", r"\broad ahead\b",
    ]),
]

# Pattern to match h2 tags that do NOT already have a level-badge
H2_PATTERN = re.compile(r'(<h2[^>]*>)(.*?)(</h2>)', re.DOTALL)
BADGE_CHECK = re.compile(r'level-badge')

# Skip "Key Takeaways" headings and similar structural headings
SKIP_HEADINGS = re.compile(r'Key Takeaways|Summary|References|Bibliography|Further Reading', re.IGNORECASE)


def classify_heading(text):
    """Determine the badge level based on heading text."""
    clean = re.sub(r'<[^>]+>', '', text).strip()  # strip HTML tags
    clean = re.sub(r'^\d+[\.\)]\s*', '', clean)   # strip leading numbers like "1." or "2)"

    for level, patterns in RULES:
        for pat in patterns:
            if re.search(pat, clean, re.IGNORECASE):
                return level
    return "intermediate"  # default


def badge_html(level):
    """Generate the badge span HTML."""
    label = level.upper()
    return f' <span class="level-badge {level}" title="{label}">{label}</span>'


def process_file(filepath):
    """Process a single HTML file, adding badges to h2 elements."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    count = 0

    def replace_h2(match):
        nonlocal count
        open_tag = match.group(1)
        inner = match.group(2)
        close_tag = match.group(3)

        # Skip if already has a badge
        if BADGE_CHECK.search(inner):
            return match.group(0)

        # Skip structural headings
        clean_text = re.sub(r'<[^>]+>', '', inner).strip()
        if SKIP_HEADINGS.search(clean_text):
            return match.group(0)

        level = classify_heading(inner)
        count += 1
        return f'{open_tag}{inner.rstrip()}{badge_html(level)}{close_tag}'

    new_content = H2_PATTERN.sub(replace_h2, content)

    if count > 0:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)

    return count


def main():
    # Find all section-*.html files, excluding agents/
    all_files = []
    for part_dir in glob.glob(os.path.join(ROOT, "part-*")):
        for dirpath, dirnames, filenames in os.walk(part_dir):
            # Skip agents directories
            if "agents" in dirpath.split(os.sep):
                continue
            for fn in sorted(filenames):
                if fn.startswith("section-") and fn.endswith(".html"):
                    all_files.append(os.path.join(dirpath, fn))

    # Also check appendices and capstone
    for extra in ["appendices", "capstone", "capstone-conversational-ai-agent"]:
        extra_dir = os.path.join(ROOT, extra)
        if os.path.isdir(extra_dir):
            for dirpath, dirnames, filenames in os.walk(extra_dir):
                if "agents" in dirpath.split(os.sep):
                    continue
                for fn in sorted(filenames):
                    if fn.startswith("section-") and fn.endswith(".html"):
                        all_files.append(os.path.join(dirpath, fn))

    all_files.sort()
    total_badges = 0
    files_modified = 0

    for filepath in all_files:
        rel = os.path.relpath(filepath, ROOT)
        count = process_file(filepath)
        if count > 0:
            print(f"  {rel}: {count} badges added")
            total_badges += count
            files_modified += 1
        else:
            # Check if file already had badges
            with open(filepath, 'r', encoding='utf-8') as f:
                text = f.read()
            existing = len(BADGE_CHECK.findall(text))
            if existing > 0:
                print(f"  {rel}: already had {existing} badges (skipped)")

    print(f"\nTotal: {total_badges} badges added across {files_modified} files")
    print(f"Files scanned: {len(all_files)}")


if __name__ == "__main__":
    main()
