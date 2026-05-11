"""v3.6 R5 P3: Validate every prose mention of "Code Fragment N.M.x" /
"Figure N.M.x" against the captions that actually exist in the same file.

When a prose reference points to a non-existent caption, attempt a heuristic
fix: if a prose mention says "Code Fragment 17.2.5" but the file only has
captions 17.2.1, 17.2.2, 17.2.3, the closest valid caption (by content
proximity, e.g., the one immediately following the prose mention) is the
likely intended target.

Strategy: don't auto-rewrite (too risky for content semantics). Instead,
EMIT a report of every mismatch so an editorial pass can fix them by hand.

Then auto-fix the very-likely cases:
  - Prose mention ABOVE a code block: "Code Fragment X.Y.Z below" + actual
    next caption is X.Y.Z' -> rewrite mention to use Z'.
  - Prose mention's "X.Y" prefix matches the file but trailing index is
    wrong: snap to the closest existing index in the same file.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
EXCLUDE = {"_archive", "KDP", "node_modules", "vendor", "scripts"}

PROSE_REF = re.compile(r"\b(Code Fragment|Figure)\s+(\d+\.\d+\.\d+)\b")
CAPTION = re.compile(r'<div class="(?:code|figure|diagram)-caption"[^>]*>\s*<strong>\s*(Code Fragment|Figure)\s+(\d+\.\d+\.\d+):?\s*</strong>')


def main() -> int:
    n_mismatches = 0
    n_autofix = 0
    n_files = 0
    report_lines = []

    for p in ROOT.glob("part-*/module-*/section-*.html"):
        text = p.read_text(encoding="utf-8", errors="replace")
        # Existing captions in this file
        captions = set()
        for m in CAPTION.finditer(text):
            captions.add((m.group(1), m.group(2)))
        if not captions:
            continue
        # Find prose mentions
        original = text
        local_mismatches = []
        local_fixes = 0
        # Iterate from the end so positional rewrites don't shift earlier offsets
        for m in list(PROSE_REF.finditer(text))[::-1]:
            kind, ref_id = m.group(1), m.group(2)
            if (kind, ref_id) in captions:
                continue
            # Skip if the mention is INSIDE a caption itself (we're scanning prose)
            ctx_start = max(0, m.start() - 60)
            ctx_after = min(len(text), m.end() + 5)
            preceding = text[ctx_start:m.start()]
            if 'class="code-caption"' in preceding[-50:] or \
               'class="figure-caption"' in preceding[-50:] or \
               'class="diagram-caption"' in preceding[-50:]:
                continue
            # Attempt heuristic: closest caption with same X.Y prefix
            ref_parts = ref_id.split(".")
            ref_prefix = f"{ref_parts[0]}.{ref_parts[1]}"
            candidates = [(k, v) for (k, v) in captions
                          if k == kind and v.startswith(f"{ref_prefix}.")]
            if not candidates:
                local_mismatches.append((kind, ref_id, "no candidate"))
                continue
            # Prefer the caption that appears AFTER the mention (most common)
            # find index of next caption after this mention
            after_pos = text.find(f"{kind} {ref_prefix}.", m.end())
            if after_pos > 0:
                after_match = re.search(rf"{re.escape(kind)}\s+(\d+\.\d+\.\d+)", text[after_pos:])
                if after_match:
                    target = (kind, after_match.group(1))
                    if target in candidates:
                        # Auto-fix: rewrite the prose mention to use target's id
                        new_text = text[:m.start()] + f"{kind} {target[1]}" + text[m.end():]
                        text = new_text
                        local_fixes += 1
                        continue
            local_mismatches.append((kind, ref_id, ", ".join(c[1] for c in candidates)))

        if text != original:
            p.write_text(text, encoding="utf-8")
            n_autofix += local_fixes
            n_files += 1
        for kind, ref_id, hint in local_mismatches:
            n_mismatches += 1
            report_lines.append(f"  {p.relative_to(ROOT).as_posix()}: {kind} {ref_id} -> [candidates: {hint}]")

    print(f"Auto-fixed {n_autofix} prose caption refs in {n_files} files")
    print(f"Remaining mismatches needing manual review: {n_mismatches}")
    if report_lines:
        report = ROOT / "KDP/build/logs/caption_ref_mismatches.txt"
        report.parent.mkdir(parents=True, exist_ok=True)
        report.write_text("\n".join(report_lines), encoding="utf-8")
        print(f"Report saved to {report.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
