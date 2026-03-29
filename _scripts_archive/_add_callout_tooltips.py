"""Add title attributes to callout divs for hover tooltips.
Also fixes any broken title attributes (missing closing quote)."""
import os
import re

ROOT = r"E:\Projects\LLMCourse"
EXCLUDE = {"_scripts_archive", ".git", "node_modules"}

TOOLTIPS = {
    "big-picture": "Big Picture: Core concept overview",
    "key-insight": "Key Insight: Important takeaway",
    "note": "Note: Additional context",
    "warning": "Warning: Common pitfall or caution",
    "practical-example": "Practical Example: Hands-on demonstration",
    "fun-note": "Fun Fact: Interesting trivia",
    "research-frontier": "Research Frontier: Cutting-edge developments",
    "algorithm": "Algorithm: Step-by-step procedure",
    "tip": "Tip: Helpful suggestion",
    "exercise": "Exercise: Practice problem",
}

TYPE_ALTERNATION = "|".join(re.escape(k) for k in TOOLTIPS)

# Pattern 1: Fix broken titles from previous run (missing closing quote)
# e.g. title="Exercise: Practice problem> -> title="Exercise: Practice problem">
FIX_PATTERN = re.compile(
    r'(<(?:div|section)\s+class="callout\s+(?:' + TYPE_ALTERNATION + r')"\s+title="[^"]*?)>'
)

# Pattern 2: Add title to callout divs that don't have one
# Matches <div class="callout TYPE"> or <div class="callout TYPE" ...> without title=
ADD_PATTERN = re.compile(
    r'(<(?:div|section)\s+class="callout\s+(' + TYPE_ALTERNATION + r')")(?!\s+title=)'
)

files_changed = 0
fixes = 0
additions = 0
type_counts = {k: 0 for k in TOOLTIPS}

for dirpath, dirnames, filenames in os.walk(ROOT):
    dirnames[:] = [d for d in dirnames if d not in EXCLUDE and not d.startswith(".")]
    for fname in filenames:
        if not fname.endswith(".html"):
            continue
        fpath = os.path.join(dirpath, fname)
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()

        new_content = content

        # Step 1: Fix broken titles (add closing quote before >)
        def fix_broken(m):
            global fixes
            text = m.group(1)
            # Check if it already ends with a proper closing quote
            if text.endswith('"'):
                return text + ">"
            fixes += 1
            return text + '">'

        new_content = FIX_PATTERN.sub(fix_broken, new_content)

        # Step 2: Add missing titles
        def add_title(m):
            global additions
            full_match = m.group(1)
            ctype = m.group(2)
            title = TOOLTIPS[ctype]
            type_counts[ctype] += 1
            additions += 1
            return f'{full_match} title="{title}"'

        new_content = ADD_PATTERN.sub(add_title, new_content)

        if new_content != content:
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(new_content)
            files_changed += 1

print(f"Files modified: {files_changed}")
print(f"Broken titles fixed: {fixes}")
print(f"New titles added: {additions}")
print(f"\nBreakdown of new titles by type:")
for ctype, count in sorted(type_counts.items(), key=lambda x: -x[1]):
    if count > 0:
        print(f"  {ctype}: {count}")
