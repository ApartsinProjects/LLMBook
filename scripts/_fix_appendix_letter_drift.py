"""Fix the appendix-letter off-by-one drift that resulted from inserting the
Glossary as "Appendix F" without renaming the lettered appendices on disk.

On disk: appendix-a, b, c, d, e, glossary, appendix-f, g, h, ..., u.
The Glossary uses section files named section-f.N (legacy internal numbering),
while appendix-f-hardware-compute uses section-f.N too — same prefix, different
directory. The user-visible labels (TOC, appendices/index.html, section h1s,
caption letters) drifted off-by-one because the Glossary was treated as
"Appendix F" in those visual labels, pushing the actual F (hardware-compute)
to "Appendix G", G to H, etc.

Canonical resolution adopted here:
  - On-disk letters are authoritative.
  - Glossary keeps the name "Glossary" (no appendix letter).
  - Every visual label, caption, anchor, and link is shifted to MATCH the
    on-disk letter.

This script:
  1. Inside each appendix-X section file, normalizes Code Fragment / Table
     / Figure / Pseudocode caption letters to the correct X.
  2. Fixes the Glossary's part-label that reads "Building Conversational AI
     with LLMs and Agents" -> "Appendices".

Step 3 (TOC / appendices/index.html label shifts) lives in a sibling script
because the right answer there is interactive (some labels skip letters,
e.g. V -> AD; those need manual decisions).

Idempotent.
"""
from __future__ import annotations
import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APPENDICES = ROOT / "appendices"


def fix_caption_letters(p: Path, expected_letter: str, dry_run: bool) -> tuple[int, list[str]]:
    """Within this file, find every `(Code Fragment|Table|Figure|Pseudocode) X.Y[.Z]`
    where X != expected_letter, and replace X with expected_letter."""
    text = p.read_text(encoding="utf-8")
    msgs: list[str] = []
    pat = re.compile(
        r"\b(Code Fragment|Table|Figure|Pseudocode)\s+([A-Z])\.(\d+(?:\.\d+)*)"
    )

    def repl(m: re.Match) -> str:
        kind, letter, rest = m.group(1), m.group(2), m.group(3)
        if letter == expected_letter:
            return m.group(0)
        msgs.append(f"  {kind} {letter}.{rest} -> {kind} {expected_letter}.{rest}")
        return f"{kind} {expected_letter}.{rest}"

    new = pat.sub(repl, text)
    if new == text:
        return 0, []
    if not dry_run:
        p.write_text(new, encoding="utf-8")
    # Dedupe messages (one line per shift kind is enough for the report)
    deduped: list[str] = []
    seen = set()
    for m in msgs:
        prefix = m.split(".")[0]
        if prefix not in seen:
            seen.add(prefix)
            deduped.append(f"{m}  (+ {sum(1 for x in msgs if x.split('.')[0] == prefix) - 1} more)")
    return len(msgs), deduped


def fix_glossary_part_label(dry_run: bool) -> tuple[int, str | None]:
    """Glossary's part-label currently says "Building Conversational AI with
    LLMs and Agents" — should be "Appendices" to match the other appendix
    landing pages."""
    p = APPENDICES / "glossary" / "index.html"
    if not p.exists():
        return 0, None
    text = p.read_text(encoding="utf-8")
    target = (
        '<div class="part-label" data-pagefind-meta="part">'
        'Building Conversational AI with LLMs and Agents'
        '</div>'
    )
    if target not in text:
        # Try the page-breadcrumb / part-label variants
        # Just look for the literal substring inside any part-label div
        pat = re.compile(
            r'(<div class="part-label"[^>]*>)Building Conversational AI with LLMs and Agents(</div>)'
        )
        m = pat.search(text)
        if not m:
            return 0, None
        new = pat.sub(r"\1Appendices\2", text)
    else:
        new = text.replace(target,
            '<div class="part-label" data-pagefind-meta="part">Appendices</div>')
    if new == text:
        return 0, None
    if not dry_run:
        p.write_text(new, encoding="utf-8")
    return 1, f"glossary/index.html: part-label -> 'Appendices'"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    total = 0
    files_touched = 0
    for d in sorted(APPENDICES.glob("appendix-*-*")):
        m = re.match(r"appendix-([a-z])-", d.name)
        if not m:
            continue
        expected = m.group(1).upper()
        for p in sorted(d.glob("*.html")):
            n, msgs = fix_caption_letters(p, expected, args.dry_run)
            if n:
                files_touched += 1
                total += n
                print(f"{p.relative_to(ROOT)}:")
                for line in msgs:
                    print(line)

    n_gloss, msg = fix_glossary_part_label(args.dry_run)
    if n_gloss:
        print(msg)
        total += n_gloss
        files_touched += 1

    print(f"\nTOTAL: {total} caption letter shifts across {files_touched} files")
    if args.dry_run:
        print("(dry run; nothing written)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
