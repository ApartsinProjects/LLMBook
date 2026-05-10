"""Audit practical-example callouts for missing Who/Situation/Problem/Decision/Result/Lesson fields."""
import glob, re, os, sys

html_files = sorted(glob.glob('**/*.html', recursive=True))

REQUIRED_FIELDS = ['Who:', 'Situation:', 'Problem:', 'Decision:', 'Result:', 'Lesson:']
SKIP_DIRS = {'vendor', 'node_modules', '_archive'}

results = []

for f in html_files:
    if any(d in f for d in SKIP_DIRS):
        continue
    with open(f, 'r', encoding='utf-8') as fh:
        content = fh.read()

    starts = [m.start() for m in re.finditer(r'class="callout practical-example"', content)]

    for start_pos in starts:
        block = content[start_pos:start_pos+3000]

        title_match = re.search(r'<div class="callout-title">(.*?)</div>', block)
        title = title_match.group(1) if title_match else "???"
        title = re.sub(r'<[^>]+>', '', title)  # strip HTML tags

        missing = [field for field in REQUIRED_FIELDS if field not in block]

        if missing:
            line_num = content[:start_pos].count('\n') + 1
            rel_path = f.replace(os.sep, '/')
            results.append((rel_path, line_num, title, missing))

# Separate categories
wrong_type = [r for r in results if len(r[3]) == 6]  # All fields missing = wrong callout type
partial = [r for r in results if 0 < len(r[3]) < 6]

print(f"Practical-Example Callout Audit")
print(f"Total non-standard: {len(results)}")
print(f"  Wrong callout type (0 of 6 fields): {len(wrong_type)}")
print(f"  Partial fields (some missing): {len(partial)}")
print()

if partial:
    print("=== PARTIAL FIELDS (fixable) ===")
    for path, line, title, missing in partial:
        print(f"  {path}:{line}")
        print(f"    Title: {title}")
        print(f"    Missing: {', '.join(missing)}")
        print()

if wrong_type:
    print("=== WRONG CALLOUT TYPE (should be library-shortcut, note, etc.) ===")
    for path, line, title, missing in wrong_type:
        print(f"  {path}:{line}  {title}")

