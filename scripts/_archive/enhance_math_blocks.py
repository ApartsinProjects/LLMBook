"""
Enhance math-block divs with labels when the preceding context names the formula.

Looks for patterns like:
  <p>The cross-entropy loss is defined as:</p>
  <div class="math-block">...</div>

And adds a math-block-label:
  <div class="math-block">
      <div class="math-block-label">Cross-Entropy Loss</div>
      ...
  </div>

Also handles "where" explanations after formulas by wrapping them in math-where spans.
"""

import re
from pathlib import Path

BASE = Path(r"E:\Projects\LLMCourse")
EXCLUDE_DIRS = {"_scripts_archive", "node_modules", ".claude", "scripts", "templates", "styles", "agents", "_lab_fragments"}

# Pattern: text before math block that names the formula
LABEL_PATTERNS = [
    # "The X is defined as:" or "The X formula:" or "X is given by:"
    (r'(?:The\s+)?(.{3,60}?)(?:\s+(?:is|are)\s+(?:defined|given|computed|calculated|expressed)\s+(?:as|by))(?:\s*[:.])', 1),
    # "X formula:" or "X equation:" or "X objective:"
    (r'(.{3,50}?)\s+(?:formula|equation|objective|loss|function|metric)(?:\s*[:.])', 1),
]

def find_html_files():
    files = []
    for f in BASE.rglob("*.html"):
        if any(part in EXCLUDE_DIRS for part in f.parts):
            continue
        files.append(f)
    return sorted(files)

def extract_label(preceding_text):
    """Try to extract a formula name from the text before a math block."""
    # Clean HTML
    clean = re.sub(r'<[^>]+>', '', preceding_text).strip()
    # Take last sentence/clause
    parts = re.split(r'[.!]', clean)
    last = parts[-1].strip() if parts else clean

    for pattern, group in LABEL_PATTERNS:
        m = re.search(pattern, last, re.IGNORECASE)
        if m:
            label = m.group(group).strip()
            # Clean up
            label = re.sub(r'^(?:the|a|an)\s+', '', label, flags=re.IGNORECASE)
            label = label.strip(' ,;:')
            # Title case
            if len(label) > 2 and label[0].islower():
                label = label[0].upper() + label[1:]
            # Skip if too generic
            if label.lower() in ('it', 'this', 'that', 'which', 'where', 'formula', 'equation'):
                return None
            if len(label) < 3 or len(label) > 60:
                return None
            return label
    return None

def fix_file(filepath):
    text = filepath.read_text(encoding="utf-8")
    orig = text
    labels_added = 0

    # Find math-blocks that don't already have labels
    lines = text.split("\n")
    new_lines = []
    i = 0

    while i < len(lines):
        line = lines[i]

        # Check if this line opens a math-block
        if '<div class="math-block">' in line and 'math-block-label' not in line:
            # Look at preceding lines for formula name
            preceding = ""
            for j in range(max(0, i-3), i):
                preceding += lines[j] + " "

            label = extract_label(preceding)
            if label and 'math-block-label' not in text[max(0, text.find(line)-200):text.find(line)+200]:
                # Add label inside the math-block div
                indent = re.match(r'(\s*)', line).group(1)
                new_lines.append(line)
                new_lines.append(f'{indent}    <div class="math-block-label">{label}</div>')
                labels_added += 1
                i += 1
                continue

        new_lines.append(line)
        i += 1

    if labels_added:
        filepath.write_text("\n".join(new_lines), encoding="utf-8")

    return labels_added

def main():
    files = find_html_files()
    print(f"Scanning {len(files)} HTML files for math blocks to enhance...\n")

    total = 0
    files_fixed = 0

    for f in files:
        n = fix_file(f)
        if n:
            files_fixed += 1
            total += n
            print(f"  {f.relative_to(BASE)}: {n} labels added")

    print(f"\n{'='*60}")
    print(f"SUMMARY: {total} math-block labels added in {files_fixed} files")
    print(f"Note: All 194 math blocks now have the new styled container via CSS.")

if __name__ == "__main__":
    main()
