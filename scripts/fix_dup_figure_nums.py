"""
Fix DUP_FIGURE_NUM P0 errors by renumbering the LATER occurrence of duplicate
captions to the next available number in the same section file.

Also updates in-prose references like "Figure X.Y.N" or "Code Fragment X.Y.N"
that appear AFTER the renumbered caption line (assumption: refs after the
duplicate point to the LATER occurrence; refs before point to the EARLIER one).

Usage:
    python scripts/fix_dup_figure_nums.py
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# (relative_path, label, line1, line2)
DUPS = [
    ("part-1-llm-building-blocks/module-00-ml-pytorch-foundations/section-0.2.html", "Code Fragment 0.2.4", 428, 578),
    ("part-1-llm-building-blocks/module-01-foundations-nlp-text-representation/section-1.3.html", "Figure 1.3.5", 335, 531),
    ("part-1-llm-building-blocks/module-03-transformer-architecture/section-3.5.html", "Figure 3.5.4", 359, 564),
    ("part-12-llm-systems-at-scale/module-58-frontier-systems-hardware/section-58.5.html", "Figure 58.5.2", 146, 182),
    ("part-12-llm-systems-at-scale/module-61-scale-tools/section-61.4.html", "Figure 61.4.1", 129, 368),
    ("part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.3.html", "Figure 6.3.4", 190, 320),
    ("part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.5.html", "Figure 6.5.3", 190, 480),
    ("part-4-training-adaptation/module-16-fine-tuning-fundamentals/section-16.7.html", "Figure 16.7.1", 80, 161),
    ("part-4-training-adaptation/module-17-peft/section-17.6.html", "Figure 17.6.3", 142, 180),
    ("part-4-training-adaptation/module-18-alignment-rlhf-dpo/section-18.2.html", "Figure 18.2.1", 65, 169),
    ("part-5-multimodal-llms/module-20-audio-music-generation/section-20.0.2.html", "Figure 20.0.2.0", 115, 210),
    ("part-5-multimodal-llms/module-20-audio-music-generation/section-20.0.4.html", "Figure 20.0.4.2", 141, 335),
    ("part-5-multimodal-llms/module-20-audio-music-generation/section-20.0.4.html", "Code Fragment 20.0.4.2", 177, 361),
    ("part-5-multimodal-llms/module-20-audio-music-generation/section-20.1.html", "Code Fragment 20.1.2", 163, 340),
    ("part-5-multimodal-llms/module-20-audio-music-generation/section-20.3.html", "Figure 20.3.2", 145, 312),
    ("part-5-multimodal-llms/module-23-3d-generation-neural-scenes/section-23.5.html", "Figure 23.5.1", 65, 185),
    ("part-5-multimodal-llms/module-23-3d-generation-neural-scenes/section-23.5.html", "Code Fragment 23.5.1", 117, 210),
    ("part-5-multimodal-llms/module-24-vla-models/section-24.1.html", "Figure 24.1.2", 131, 248),
    ("part-5-multimodal-llms/module-24-vla-models/section-24.13.html", "Table 24.13.1", 72, 172),
    ("part-6-agentic-ai/module-26-ai-agents/section-26.1.html", "Figure 26.1.6", 334, 581),
    ("part-7-retrieval-information-extraction-with-llms/module-31-embeddings-vector-db/section-31.7.html", "Code Fragment 31.7.3", 463, 530),
    ("part-7-retrieval-information-extraction-with-llms/module-32-rag/section-32.1.html", "Figure 32.1.2", 270, 455),
    ("part-7-retrieval-information-extraction-with-llms/module-35-advanced-rag/section-35.2.html", "Code Fragment 35.2.2", 301, 1153),
    ("part-7-retrieval-information-extraction-with-llms/module-35-advanced-rag/section-35.2.html", "Code Fragment 35.2.5", 489, 953),
    ("part-7-retrieval-information-extraction-with-llms/module-35-advanced-rag/section-35.2.html", "Code Fragment 35.2.3", 525, 821),
    ("part-7-retrieval-information-extraction-with-llms/module-35-advanced-rag/section-35.2.html", "Code Fragment 35.2.4", 670, 900),
    ("part-7-retrieval-information-extraction-with-llms/module-35-advanced-rag/section-35.6.html", "Figure 35.6.3", 319, 781),
]


def find_existing_numbers(text: str, kind: str, prefix: str) -> set:
    """Find all existing numbered captions of `kind` (Figure/Table/Code Fragment)
    with section prefix (e.g. '0.2', '20.0.4').
    Returns set of suffix tokens like '4', '4a', '6'.
    """
    # Match the label across the file. Match number after prefix.
    # Prefix may be like "0.2" or "20.0.4". Last component after final dot is the suffix.
    esc_prefix = re.escape(prefix)
    pattern = re.compile(rf"\b{re.escape(kind)}\s+{esc_prefix}\.([0-9]+[a-z]?)\b")
    return set(pattern.findall(text))


def next_available_suffix(used: set, start: int) -> str:
    """Find next free suffix starting from `start`. Try N, N+1, ... avoiding `used`."""
    n = start
    while str(n) in used:
        n += 1
    return str(n)


def renumber_in_lines(lines: list, kind: str, full_label: str, new_label: str, line2_idx: int) -> int:
    """Replace occurrences of `full_label` from line2_idx onward with `new_label`.
    Returns count of substitutions made.
    """
    count = 0
    # The duplicate caption text "Figure X.Y.N" or "Code Fragment X.Y.N" is what we replace.
    # Be word-boundary careful: not to match "Figure X.Y.N.0" etc.
    pattern = re.compile(rf"\b{re.escape(full_label)}\b(?![\d])")
    for i in range(line2_idx, len(lines)):
        new_line, n = pattern.subn(new_label, lines[i])
        if n:
            lines[i] = new_line
            count += n
    return count


def split_label(label: str):
    """ 'Figure 20.0.4.2' -> ('Figure', '20.0.4', 2)
        'Code Fragment 0.2.4' -> ('Code Fragment', '0.2', 4)
        'Table 24.13.1' -> ('Table', '24.13', 1)
    """
    m = re.match(r"^(Figure|Table|Code Fragment)\s+(.+)$", label)
    if not m:
        raise ValueError(f"Cannot parse label: {label}")
    kind = m.group(1)
    parts = m.group(2).split(".")
    # The number we are renumbering is the LAST component
    suffix = parts[-1]
    prefix = ".".join(parts[:-1])
    return kind, prefix, int(suffix)


def fix_file(rel_path: str, label: str, line1: int, line2: int) -> tuple:
    """Returns (success, message, old_label, new_label, refs_updated)."""
    path = ROOT / rel_path
    if not path.exists():
        return (False, f"file not found: {path}", None, None, 0)

    text = path.read_text(encoding="utf-8")
    lines = text.split("\n")

    kind, prefix, dup_num = split_label(label)
    # Existing suffixes for this kind+prefix in the file
    used = find_existing_numbers(text, kind, prefix)
    # Pick next available, starting AFTER dup_num
    new_suffix = next_available_suffix(used, dup_num + 1)
    new_label = f"{kind} {prefix}.{new_suffix}"

    if new_label == label:
        return (False, "no change computed", label, new_label, 0)

    # Verify line2 actually contains the label
    if line2 - 1 >= len(lines):
        return (False, f"line {line2} beyond file", label, new_label, 0)
    if label not in lines[line2 - 1]:
        # Could be that the line numbering shifted; try to find it near line2
        # by searching forward/backward
        found_line = None
        for offset in range(0, 20):
            for direction in (1, -1):
                idx = (line2 - 1) + direction * offset
                if 0 <= idx < len(lines) and label in lines[idx]:
                    found_line = idx
                    break
            if found_line is not None:
                break
        if found_line is None:
            return (False, f"label not at line {line2}", label, new_label, 0)
        line2 = found_line + 1

    # Renumber from line2 onward (replaces all occurrences after that point,
    # which catches both the caption and any in-prose refs that appear after it)
    refs = renumber_in_lines(lines, kind, label, new_label, line2 - 1)

    if refs == 0:
        return (False, "no replacement made", label, new_label, 0)

    new_text = "\n".join(lines)
    path.write_text(new_text, encoding="utf-8")
    return (True, "ok", label, new_label, refs)


def main():
    total_ok = 0
    total_fail = 0
    renumbered_files = set()
    for rel_path, label, line1, line2 in DUPS:
        ok, msg, old, new, refs = fix_file(rel_path, label, line1, line2)
        status = "OK" if ok else "FAIL"
        print(f"[{status}] {rel_path} :: {old} -> {new} ({refs} subs) {msg}")
        if ok:
            total_ok += 1
            renumbered_files.add(rel_path)
        else:
            total_fail += 1

    print()
    print(f"Summary: {total_ok} fixed, {total_fail} failed")
    print(f"Files renumbered: {len(renumbered_files)}")
    for f in sorted(renumbered_files):
        print(f"  {f}")
    return 0 if total_fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
