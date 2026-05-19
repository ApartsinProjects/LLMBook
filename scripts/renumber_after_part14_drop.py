"""Renumber the book after Part 14 was dropped.

Phase 4 of the Part 14 drop sequence.

Mapping (old -> new):
  part-15-applications-of-llms-across-industries -> part-14-applications-of-llms-across-industries
  part-16-llm-agentic-ai-research-frontiers -> part-15-llm-agentic-ai-research-frontiers

  Module 72 -> 67  (legal-llms)
  Module 73 -> 68  (finance-llms)
  Module 74 -> 69  (healthcare-llms)
  Module 75 -> 70  (education-llms)
  Module 76 -> 71  (cybersecurity-llms)
  Module 77 -> 72  (government-llms)
  Module 78 -> 73  (manufacturing-llms)
  Module 79 -> 74  (tools-of-the-trade)
  Module 80 -> 75  (frontier-architectures)
  Module 81 -> 76  (frontier-theory)
  Module 82 -> 77  (agi-trajectories)
  Module 83 -> 78  (research-frontiers-tools)

Operations:
1. Build the full rename map.
2. Rename directories (parts, modules).
3. Rename section files inside modules.
4. Walk EVERY HTML in the book (sections, indexes, toc, front-matter, root index.html)
   and apply text substitutions:
   - File paths in href/src: part-15- -> part-14-, etc.
   - Module names in href/src: module-72- -> module-67-, etc.
   - Section/figure references in prose: 72.X -> 67.X, 73.X -> 68.X, etc.
   - Chapter references: Chapter 72 -> Chapter 67, etc.
   - "Part XV" / "Part XVI" -> "Part XIV" / "Part XV"
   - Roman numerals in toc / FM
5. Dry-run by default; pass --apply to write.

Safety:
- Section number patterns are anchored with word boundaries.
- Replacements happen in order: longer/more-specific first.
- Files in _archive/ are skipped.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
ROOT = Path(__file__).resolve().parent.parent

# Old -> New module mapping
MODULE_MAP = {
    72: 67, 73: 68, 74: 69, 75: 70, 76: 71, 77: 72,
    78: 73, 79: 74, 80: 75, 81: 76, 82: 77, 83: 78,
}

# Old -> New part dir
PART_DIR_MAP = {
    'part-15-applications-of-llms-across-industries':
        'part-14-applications-of-llms-across-industries',
    'part-16-llm-agentic-ai-research-frontiers':
        'part-15-llm-agentic-ai-research-frontiers',
}

# Module dir name fragments to remap (the "module-NN-" prefix portion)
# We keep the slug suffix and only swap the number.
def module_dir_pairs():
    pairs = []
    p15 = ROOT / 'part-15-applications-of-llms-across-industries'
    p16 = ROOT / 'part-16-llm-agentic-ai-research-frontiers'
    for part_dir in (p15, p16):
        if not part_dir.exists():
            continue
        for mod_dir in part_dir.iterdir():
            if not mod_dir.is_dir():
                continue
            m = re.match(r'^module-(\d+)-(.+)$', mod_dir.name)
            if not m:
                continue
            old_num = int(m.group(1))
            slug = m.group(2)
            if old_num in MODULE_MAP:
                new_num = MODULE_MAP[old_num]
                new_dir_name = f'module-{new_num}-{slug}'
                pairs.append((mod_dir, mod_dir.parent / new_dir_name, old_num, new_num))
    return pairs


# Skip these directories entirely when doing in-place text replacements
SKIP_TEXT_DIRS = {'_archive', 'node_modules', '.git', '.book-update', 'pagefind',
                  'KDP', 'build', 'vendor', '.claude', '__pycache__'}


# --- Text replacement rules (applied in this exact order) ---

# Roman numerals first (need to NOT match "XV" in "XVII" etc.)
ROMAN_REPLACEMENTS = [
    # Part XV -> Part XIV, Part XVI -> Part XV.
    # We do XVI first (longer match), then XV.
    (re.compile(r'\bPart\s+XVI\b'), 'Part XV'),
    (re.compile(r'\bPart\s+XV\b'),  'Part XIV'),  # note: must run AFTER XVI rule
    (re.compile(r'\bpart-16\b'),    'part-15'),  # short slug
    (re.compile(r'\bpart-15\b'),    'part-14'),  # short slug, after part-16
]

# Part dir names in URLs / paths (longer specific names — run after Roman shortest)
PART_PATH_REPLACEMENTS = [
    (re.compile(r'part-16-llm-agentic-ai-research-frontiers'),
     'part-15-llm-agentic-ai-research-frontiers'),
    (re.compile(r'part-15-applications-of-llms-across-industries'),
     'part-14-applications-of-llms-across-industries'),
]


# Context-anchored substitutions. The naive "(?<![\d.])72\.X" pattern matches
# benchmark percentages (72.6%), DOIs (10.1109/72.279181), and JSON timings —
# all false positives. We restrict to known section-reference contexts:
# - URL paths (section-NN.X.html, module-NN-, etc.)
# - HTML IDs (id="NN-X-..." or id="NN.X...")
# - Prose contexts ("Section 72.3", "Figure 72.3.1", "Table 72.3", etc.)
# - Filenames in href/src attributes
#
# Applied highest-to-lowest old number so 80.X rules don't pre-empt 72.X.
SECTION_CONTEXT_PREFIXES = [
    'Section', 'Sections', 'section', 'sections',
    'Figure', 'Figures', 'figure', 'figures',
    'Fig\\.', 'Fig',
    'Table', 'Tables', 'table', 'tables',
    'Code Fragment', 'Code fragment',
    'Exercise', 'Exercises', 'exercise', 'exercises',
    'Algorithm', 'Algorithms', 'algorithm', 'algorithms',
    'Lab', 'Labs', 'lab',
]


def build_number_rules():
    rules = []
    for old_num in sorted(MODULE_MAP.keys(), reverse=True):
        new_num = MODULE_MAP[old_num]
        # Rule A: prose context "Section NN.X" / "Figure NN.X" / etc.
        # Match the keyword + space + old_num + .X(.Y)?(letter)?
        for prefix in SECTION_CONTEXT_PREFIXES:
            pat = re.compile(rf'\b({prefix}\s+){old_num}(\.\d+(?:\.\d+)?[a-z]?)')
            rules.append((pat, rf'\g<1>{new_num}\g<2>', f'{prefix} {old_num}.X -> {new_num}.X'))
        # Rule B: filename references in href/src/url attributes
        # Matches `section-72.3.html`, `section-72.3a.html`
        pat_file = re.compile(rf'\bsection-{old_num}(\.\d+(?:\.\d+)?[a-z]?)\.html\b')
        rules.append((pat_file, rf'section-{new_num}\g<1>.html',
                      f'section-{old_num}.X.html -> section-{new_num}.X.html'))
        # Rule C: HTML id attributes (e.g., id="72-3-1-foo" or id="72.3.1")
        # The book uses BOTH dot-form ("72.3.1") and hyphen-form ("72-3-1")
        pat_id_dot = re.compile(rf'\b(id=")(?:{old_num})(\.\d+(?:\.\d+)?[a-z]?)')
        rules.append((pat_id_dot, rf'\g<1>{new_num}\g<2>', f'id="{old_num}.X" -> id="{new_num}.X"'))
        pat_id_hyphen = re.compile(rf'\b(id=")(?:{old_num})(-\d+(?:-\d+)?[a-z]?-)')
        rules.append((pat_id_hyphen, rf'\g<1>{new_num}\g<2>',
                      f'id="{old_num}-X-" -> id="{new_num}-X-"'))
        # Hyphen-form WITHOUT trailing hyphen (end of id)
        pat_id_hyphen_end = re.compile(rf'\b(id=")(?:{old_num})(-\d+(?:-\d+)?[a-z]?)(")')
        rules.append((pat_id_hyphen_end, rf'\g<1>{new_num}\g<2>\g<3>',
                      f'id="{old_num}-X" -> id="{new_num}-X"'))
        # Rule D: bare "Chapter NN" / "Chapters NN" references in prose
        rules.append((re.compile(rf'\bChapter\s+{old_num}\b'),
                      f'Chapter {new_num}', f'Chapter {old_num} -> Chapter {new_num}'))
        rules.append((re.compile(rf'\bChapters\s+{old_num}\b'),
                      f'Chapters {new_num}', None))
        # Rule E: module-NN- in paths
        rules.append((re.compile(rf'\bmodule-{old_num}-'),
                      f'module-{new_num}-', f'module-{old_num}- -> module-{new_num}-'))
        # Rule F: data-pagefind-meta="chapter:Chapter NN" / similar metadata
        rules.append((re.compile(rf'(chapter:Chapter\s+){old_num}\b'),
                      rf'\g<1>{new_num}', f'pagefind chapter:Chapter {old_num} -> {new_num}'))
    return rules

NUMBER_RULES = build_number_rules()


# --- Apply substitutions to a single file's content ---

def apply_replacements(text: str) -> tuple[str, dict]:
    counts: dict = {}
    # Phase 1: Roman numerals (XVI -> XV, XV -> XIV, part-16, part-15 short slug)
    # IMPORTANT: order matters. "XVI" must be replaced before "XV" to prevent
    # XV inside XVI from being rewritten as XIV first.
    for pat, repl in ROMAN_REPLACEMENTS:
        text, n = pat.subn(repl, text)
        if n:
            counts.setdefault(pat.pattern, 0)
            counts[pat.pattern] += n
    # Phase 2: full part-dir paths
    for pat, repl in PART_PATH_REPLACEMENTS:
        text, n = pat.subn(repl, text)
        if n:
            counts.setdefault(pat.pattern, 0)
            counts[pat.pattern] += n
    # Phase 3: number rules (highest module number first)
    for entry in NUMBER_RULES:
        pat, repl = entry[0], entry[1]
        text, n = pat.subn(repl, text)
        if n:
            counts.setdefault(pat.pattern, 0)
            counts[pat.pattern] += n
    return text, counts


def walk_files():
    """Yield every HTML file in the book that we should rewrite."""
    for path in ROOT.rglob('*.html'):
        if any(skip in path.parts for skip in SKIP_TEXT_DIRS):
            continue
        yield path
    # Also include any .json/.md inside docs/ that may reference parts
    for path in (ROOT / 'docs').rglob('*'):
        if path.is_file() and path.suffix in ('.md', '.json'):
            yield path


def main():
    apply = '--apply' in sys.argv
    print(f"{'APPLY MODE' if apply else 'DRY RUN'}\n")

    # === Step 1: rename module directories ===
    print("=== Step 1: rename module directories ===")
    mod_pairs = module_dir_pairs()
    for old_dir, new_dir, old_num, new_num in mod_pairs:
        if old_dir.exists():
            print(f"  module-{old_num} -> module-{new_num}: {old_dir.name} -> {new_dir.name}")
            if apply:
                old_dir.rename(new_dir)

    # === Step 2: rename section files inside (now-renamed) module dirs ===
    print("\n=== Step 2: rename section-NN.X.html files ===")
    section_renames = 0
    # Re-discover modules (they may have just been renamed)
    for part_dir in ROOT.glob('part-1*-*'):
        for mod_dir in part_dir.glob('module-*'):
            # Compute the chapter number from the directory name
            m = re.match(r'^module-(\d+)-', mod_dir.name)
            if not m:
                continue
            new_chap = int(m.group(1))
            # If this module was just renamed, the section files still have OLD chap numbers
            old_chap = None
            for old_num, target_new in MODULE_MAP.items():
                if target_new == new_chap:
                    old_chap = old_num
                    break
            if old_chap is None:
                continue
            for sec_file in mod_dir.glob(f'section-{old_chap}.*.html'):
                # Compute new filename
                rel_name = sec_file.name
                # section-NN.X.html or section-NN.Xa.html
                m2 = re.match(rf'^section-{old_chap}\.(.+)$', rel_name)
                if not m2:
                    continue
                new_name = f'section-{new_chap}.{m2.group(1)}'
                new_path = sec_file.parent / new_name
                print(f"  {sec_file.name} -> {new_name}")
                section_renames += 1
                if apply:
                    sec_file.rename(new_path)
    print(f"  Total: {section_renames} section file renames")

    # === Step 3: rename part directories ===
    print("\n=== Step 3: rename part directories ===")
    for old_name, new_name in PART_DIR_MAP.items():
        old_path = ROOT / old_name
        new_path = ROOT / new_name
        if old_path.exists():
            print(f"  {old_name} -> {new_name}")
            if apply:
                old_path.rename(new_path)

    # === Step 4: apply text substitutions across all HTML/MD/JSON ===
    print("\n=== Step 4: text substitutions across book ===")
    total_files = 0
    total_changes = 0
    per_pattern_counts: dict = {}
    for f in walk_files():
        try:
            text = f.read_text(encoding='utf-8')
        except Exception:
            continue
        new_text, counts = apply_replacements(text)
        if new_text != text:
            total_files += 1
            for k, v in counts.items():
                per_pattern_counts[k] = per_pattern_counts.get(k, 0) + v
                total_changes += v
            if apply:
                f.write_text(new_text, encoding='utf-8')
    print(f"  Files changed: {total_files}")
    print(f"  Total replacements: {total_changes}")
    print("\nPer-pattern counts:")
    for pat, n in sorted(per_pattern_counts.items(), key=lambda x: -x[1]):
        # truncate long patterns
        s = pat if len(pat) <= 60 else pat[:60] + '...'
        print(f"  {n:6d}  {s}")

    if not apply:
        print("\n(dry-run; pass --apply to actually write)")
    else:
        print("\nDone. Run audit next.")


if __name__ == '__main__':
    main()
