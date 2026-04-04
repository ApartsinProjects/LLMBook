"""Remove old-style exercise blocks (yellow gradient, <ol> numbered list, inline styles)
from files that have BOTH old and new exercise formats. Keep only the new callout-style exercises."""

import re
from pathlib import Path

BASE = Path(r"E:\Projects\LLMCourse")

# Files with DUPLICATE exercises (old + new)
DUPLICATE_FILES = [
    "part-1-foundations/module-01-foundations-nlp-text-representation/section-1.4.html",
    "part-8-evaluation-production/module-29-evaluation-observability/section-29.1.html",
    "part-8-evaluation-production/module-29-evaluation-observability/section-29.2.html",
    "part-8-evaluation-production/module-29-evaluation-observability/section-29.3.html",
    "part-8-evaluation-production/module-29-evaluation-observability/section-29.4.html",
    "part-8-evaluation-production/module-29-evaluation-observability/section-29.5.html",
    "part-8-evaluation-production/module-29-evaluation-observability/section-29.6.html",
    "part-8-evaluation-production/module-29-evaluation-observability/section-29.7.html",
    "part-8-evaluation-production/module-29-evaluation-observability/section-29.8.html",
    "part-8-evaluation-production/module-30-observability-monitoring/section-30.1.html",
    "part-8-evaluation-production/module-30-observability-monitoring/section-30.2.html",
    "part-8-evaluation-production/module-30-observability-monitoring/section-30.3.html",
    "part-8-evaluation-production/module-30-observability-monitoring/section-30.4.html",
]

# Pattern: old-style exercise block starts with <h2>Exercises: ... and ends with </details>
# after the answer sketches section
OLD_EXERCISE_PATTERN = re.compile(
    r'\n*\s*<h2>Exercises:.*?</h2>\s*'           # <h2>Exercises: Title <span>ADVANCED</span></h2>
    r'<div style="background: linear-gradient\(135deg, #ffeaa7, #fdcb6e\).*?</div>\s*'  # yellow gradient instruction box
    r'<ol>.*?</ol>\s*'                             # numbered exercise list
    r'<details.*?</details>\s*',                   # answer sketches details block
    re.DOTALL
)

fixed = 0
for rel_path in DUPLICATE_FILES:
    fpath = BASE / rel_path
    if not fpath.exists():
        print(f"  SKIP (not found): {rel_path}")
        continue

    content = fpath.read_text(encoding="utf-8")

    # Verify it has both old and new formats
    has_old = "linear-gradient(135deg, #ffeaa7, #fdcb6e)" in content
    has_new = '<div class="callout exercise">' in content

    if not has_old:
        print(f"  SKIP (no old exercises): {rel_path}")
        continue
    if not has_new:
        print(f"  SKIP (no new exercises, would delete all): {rel_path}")
        continue

    new_content = OLD_EXERCISE_PATTERN.sub('\n\n', content)

    if new_content == content:
        print(f"  WARN (pattern not matched): {rel_path}")
        # Try a more lenient approach
        # Find the old block boundaries manually
        start_marker = '<h2>Exercises:'
        end_marker_text = 'Answer Sketches'

        start_idx = content.find(start_marker)
        if start_idx == -1:
            print(f"    Could not find start marker")
            continue

        # Find the </details> that closes the answer sketches after start_idx
        details_search_start = content.find(end_marker_text, start_idx)
        if details_search_start == -1:
            print(f"    Could not find answer sketches")
            continue

        details_end = content.find('</details>', details_search_start)
        if details_end == -1:
            print(f"    Could not find closing details tag")
            continue

        details_end += len('</details>')

        # Also consume trailing whitespace/newlines
        while details_end < len(content) and content[details_end] in '\n\r\t ':
            details_end += 1

        # Go back from start_idx to consume leading whitespace
        while start_idx > 0 and content[start_idx - 1] in '\n\r\t ':
            start_idx -= 1

        new_content = content[:start_idx] + '\n\n' + content[details_end:]
        print(f"    Used manual extraction: removed chars {start_idx}-{details_end}")

    fpath.write_text(new_content, encoding="utf-8")
    fixed += 1
    print(f"  FIXED: {rel_path}")

print(f"\nDone. Fixed {fixed}/{len(DUPLICATE_FILES)} files.")
