"""Wave 42: reorder section-1.4 callouts to satisfy CALLOUT_ORDER canonical
flow (lab -> key-takeaway -> self-check -> exercises).

We move the lab and key-takeaway blocks from after the exercises section to
before it, keeping the research-frontier callout right before the exercises.
"""
from pathlib import Path

FP = Path(r"E:/Projects/BookBlogsHome/LLMBook/part-1-llm-building-blocks/module-01-foundations-nlp-text-representation/section-1.4.html")

text = FP.read_text(encoding="utf-8")
lines = text.split("\n")

# Find boundaries
# Exercises section opens at line index 384 (1-based 385)
# Lab callout: lines 510-686 (1-based) -> indices 509-685 (0-based)
# Key-takeaway: lines 688-696 (1-based -> indices 687-695)
ex_start = None
lab_start = None
lab_end = None
kt_start = None
kt_end = None
for i, l in enumerate(lines):
    if ex_start is None and l.strip() == '<section class="exercises">':
        ex_start = i
    if lab_start is None and l.strip().startswith('<div class="callout lab"'):
        lab_start = i
    if kt_start is None and l.strip() == '<div class="callout key-takeaway">':
        kt_start = i

# Find lab end and key-takeaway end by depth counting
def block_end(lines, start, open_tag='<div', close_tag='</div>'):
    depth = 0
    for j in range(start, len(lines)):
        depth += lines[j].count(open_tag) - lines[j].count(close_tag)
        if depth == 0 and j > start:
            return j
    return None

lab_end = block_end(lines, lab_start)
kt_end = block_end(lines, kt_start)

print(f"Exercises start (line {ex_start+1}): {lines[ex_start].strip()[:80]}")
print(f"Lab block: line {lab_start+1} -> {lab_end+1}")
print(f"Key-takeaway block: line {kt_start+1} -> {kt_end+1}")

# Extract blocks (inclusive)
lab_block = lines[lab_start:lab_end + 1]
kt_block = lines[kt_start:kt_end + 1]

# Verify ex_start < lab_start < kt_start (current order)
assert ex_start < lab_start < kt_start

# Build new lines:
# 1) keep everything up to ex_start - 1 (exclusive of exercises)
# 2) insert lab_block + blank + kt_block + blank
# 3) keep ex_start to lab_start - 1 (the exercises section + anything between)
# 4) skip lab_start to lab_end (already moved)
# 5) skip anything between lab_end+1 and kt_start - 1 (if any) but we keep it
# 6) skip kt_start to kt_end (already moved)
# 7) keep everything after kt_end + 1

before_exercises = lines[:ex_start]
exercises_to_lab = lines[ex_start:lab_start]
between_lab_kt = lines[lab_end + 1:kt_start]
after_kt = lines[kt_end + 1:]

# Sanity: between_lab_kt should be 1 line (a blank or empty) since kt directly follows lab
assert kt_start - lab_end <= 2, f"Unexpected gap: lab_end={lab_end}, kt_start={kt_start}"

new_lines = (
    before_exercises
    + lab_block
    + kt_block
    + exercises_to_lab
    + between_lab_kt
    + after_kt
)

FP.write_text("\n".join(new_lines), encoding="utf-8")
print(f"Wrote {len(new_lines)} lines (was {len(lines)})")
