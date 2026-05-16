"""Fix stale <h2>NN.x in-body headings in industry chapter indexes."""
import re
from pathlib import Path

ROOT = Path(r"E:/Projects/BookBlogsHome/LLMBook/part-11-applications-across-industries")

# Each industry chapter uses some pre-renumbering chapter number for body h2s
# Discovered values: 36 (legal=51), 37 (finance=52), 38 (healthcare=53), 39 (education=54)
# Plus 55-57 likely have similar offsets. Will discover and fix.
TARGETS = {
    "module-51-legal-llms": (36, 51),
    "module-52-finance-llms": (37, 52),
    "module-53-healthcare-llms": (38, 53),
    "module-54-education-llms": (39, 54),
    "module-55-cybersecurity-llms": (40, 55),
    "module-56-government-llms": (41, 56),
    "module-57-manufacturing-llms": (42, 57),
}

count = 0
for slug, (stale, target) in TARGETS.items():
    path = ROOT / slug / "index.html"
    if not path.exists():
        continue
    text = path.read_text(encoding="utf-8")
    pattern = re.compile(r'(<h2>)' + str(stale) + r'(\.\d+)')
    new_text, n = pattern.subn(rf'\g<1>{target}\g<2>', text)
    if n > 0:
        path.write_text(new_text, encoding="utf-8")
        print(f"  {slug}: rewrote {n} <h2> prefixes ({stale}.x -> {target}.x)")
        count += n
    else:
        # Detect actual stale prefix
        m = re.search(r'<h2>(\d+)\.\d', text)
        if m and m.group(1) != str(target):
            actual = int(m.group(1))
            pattern2 = re.compile(r'(<h2>)' + str(actual) + r'(\.\d+)')
            new_text, n = pattern2.subn(rf'\g<1>{target}\g<2>', text)
            if n > 0:
                path.write_text(new_text, encoding="utf-8")
                print(f"  {slug}: rewrote {n} <h2> prefixes ({actual}.x -> {target}.x) [auto-detected]")
                count += n

print(f"\nTotal: {count} h2 prefixes rewritten")
