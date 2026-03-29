"""Fix CSS class mismatches across all HTML files in the LLMCourse project."""

import os
import re
import glob
from collections import defaultdict

ROOT = os.path.dirname(os.path.abspath(__file__))
counts = defaultdict(int)
modified_files = set()


def process_file(filepath, patterns):
    """Apply a list of (compiled_regex, replacement, label) to a file."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    original = content
    for regex, replacement, label in patterns:
        content, n = regex.subn(replacement, content)
        if n > 0:
            counts[label] += n

    if content != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        modified_files.add(filepath)
        return True
    return False


def find_html_files(subdir=""):
    """Find all .html files under ROOT/subdir."""
    search_path = os.path.join(ROOT, subdir, "**", "*.html")
    return glob.glob(search_path, recursive=True)


def main():
    # === Fix 1: callout insight -> callout key-insight (lecture-notes.html in module-01) ===
    fix1_file = os.path.join(
        ROOT,
        "part-1-foundations",
        "module-01-foundations-nlp-text-representation",
        "lecture-notes.html",
    )
    if os.path.exists(fix1_file):
        process_file(fix1_file, [
            (
                re.compile(r'class="callout insight"'),
                'class="callout key-insight"',
                "Fix 1: callout insight -> callout key-insight",
            ),
        ])

    # === Fix 2: callout callout-info -> callout note (section-7.3.html), remove inline style ===
    fix2_file = os.path.join(
        ROOT,
        "part-2-understanding-llms",
        "module-07-modern-llm-landscape",
        "section-7.3.html",
    )
    if os.path.exists(fix2_file):
        process_file(fix2_file, [
            (
                re.compile(
                    r'class="callout callout-info"\s*style="[^"]*"'
                ),
                'class="callout note"',
                "Fix 2: callout callout-info -> callout note (+ remove inline style)",
            ),
        ])

    # === Fix 3: exercises -> callout exercise (section elements in part-5) ===
    for filepath in find_html_files("part-5-retrieval-conversation"):
        process_file(filepath, [
            (
                re.compile(r'(<section\s+)class="exercises"'),
                r'\1class="callout exercise"',
                "Fix 3: exercises -> callout exercise",
            ),
        ])

    # === Fix 4: quiz-section -> quiz (section-0.2.html) ===
    fix4_file = os.path.join(
        ROOT,
        "part-1-foundations",
        "module-00-ml-pytorch-foundations",
        "section-0.2.html",
    )
    if os.path.exists(fix4_file):
        process_file(fix4_file, [
            (
                re.compile(r'class="quiz-section"'),
                'class="quiz"',
                "Fix 4: quiz-section -> quiz",
            ),
        ])

    # === Fix 5: frontier-box -> callout research-frontier (section-0.4.html) ===
    fix5_file = os.path.join(
        ROOT,
        "part-1-foundations",
        "module-00-ml-pytorch-foundations",
        "section-0.4.html",
    )
    if os.path.exists(fix5_file):
        process_file(fix5_file, [
            (
                re.compile(r'class="frontier-box"'),
                'class="callout research-frontier"',
                "Fix 5: frontier-box -> callout research-frontier",
            ),
        ])

    # === Fix 6: output -> code-output in section-0.3.html (but not already code-output) ===
    fix6_file = os.path.join(
        ROOT,
        "part-1-foundations",
        "module-00-ml-pytorch-foundations",
        "section-0.3.html",
    )
    if os.path.exists(fix6_file):
        process_file(fix6_file, [
            (
                # Match class="output" exactly, not class="code-output" or class="output-something"
                re.compile(r'class="output"'),
                'class="code-output"',
                "Fix 6: output -> code-output",
            ),
        ])

    # === Fix 7: output-block -> code-output in section-0.2.html ===
    if os.path.exists(fix4_file):
        process_file(fix4_file, [
            (
                re.compile(r'class="output-block"'),
                'class="code-output"',
                "Fix 7: output-block -> code-output",
            ),
        ])

    # === Fix 8: diagram -> diagram-container in lecture-notes.html ===
    if os.path.exists(fix1_file):
        process_file(fix1_file, [
            (
                # Match class="diagram" exactly, not class="diagram-container" etc.
                re.compile(r'class="diagram"'),
                'class="diagram-container"',
                "Fix 8: diagram -> diagram-container",
            ),
        ])

    # === Fix 9: figure -> illustration in lecture-notes.html (on div/figure elements only) ===
    if os.path.exists(fix1_file):
        process_file(fix1_file, [
            (
                # Match class="figure" exactly (not class="figure-caption" etc.)
                re.compile(r'class="figure"'),
                'class="illustration"',
                "Fix 9: figure -> illustration",
            ),
        ])

    # === Fix 10: key-idea -> callout key-insight in lecture-notes.html ===
    if os.path.exists(fix1_file):
        process_file(fix1_file, [
            (
                re.compile(r'class="key-idea"'),
                'class="callout key-insight"',
                "Fix 10: key-idea -> callout key-insight",
            ),
        ])

    # === Fix 11: learning-objectives -> objectives in part-10 module indexes ===
    for filepath in find_html_files("part-10-frontiers"):
        process_file(filepath, [
            (
                re.compile(r'class="learning-objectives"'),
                'class="objectives"',
                "Fix 11: learning-objectives -> objectives",
            ),
        ])

    # === Fix 12: lab-container -> lab in part-6 section files ===
    for filepath in find_html_files("part-6-agentic-ai"):
        process_file(filepath, [
            (
                re.compile(r'class="lab-container"'),
                'class="lab"',
                "Fix 12: lab-container -> lab",
            ),
        ])

    # === Fix 13: Remove inline styles from .whats-next divs ===
    whats_next_style = re.compile(
        r'(<div\s+class="whats-next")\s+style="background:\s*linear-gradient\(135deg,\s*#e3f2fd,\s*#e8eaf6\);\s*border:\s*1px solid #90caf9;\s*border-radius:\s*10px;\s*padding:\s*1\.5rem\s*1\.8rem;\s*margin:\s*2rem\s*0;"'
    )
    for filepath in find_html_files():
        process_file(filepath, [
            (
                whats_next_style,
                r'\1',
                "Fix 13: remove inline style from .whats-next",
            ),
        ])

    # === Fix 14: Remove inline styles from .cross-ref links ===
    # The style attr comes after href, so match: class="cross-ref" href="..." style="..."
    cross_ref_style = re.compile(
        r'(class="cross-ref"\s+href="[^"]*")\s+style="[^"]*"'
    )
    for filepath in find_html_files():
        process_file(filepath, [
            (
                cross_ref_style,
                r'\1',
                "Fix 14: remove inline style from .cross-ref",
            ),
        ])

    # === Report ===
    print("=" * 60)
    print("CSS Class Fix Report")
    print("=" * 60)
    total_changes = 0
    for label in sorted(counts.keys()):
        print(f"  {label}: {counts[label]}")
        total_changes += counts[label]
    print("-" * 60)
    print(f"  Total changes: {total_changes}")
    print(f"  Total files modified: {len(modified_files)}")
    print("=" * 60)


if __name__ == "__main__":
    main()
