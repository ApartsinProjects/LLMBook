"""Fix caption numbers that use a placeholder LETTER prefix.

ROOT CAUSE
  A content-generation pass left captions like:
    <strong>Table g.1.1:</strong>
    <strong>Code Fragment k.5.1:</strong>
    <strong>Figure G.1.1:</strong>
    <strong>Diagram h.6.1:</strong>
  The leading letter was a template slug intended to be replaced with
  the proper section number. The substitution never happened, so the
  reader sees nonsense like "Table g.1.1" inside what is actually
  section 5.2.

DETECTION
  Pattern: <strong>(Table|Code Fragment|Figure|Diagram) [A-Za-z]\\.\\d+\\.\\d+[a-z]?:?</strong>
  Also handled inside <caption>...</caption> (HTML table captions) and
  <figcaption>...</figcaption>.

FIX
  Renumber each broken caption with the proper {section_id}.{N} format,
  where section_id comes from the filename (section-X.Y.html -> "X.Y")
  and N is the next available sequential counter PER caption type within
  the file (preserving any correctly-numbered captions already present).

  Example: in part-1-llm-building-blocks/module-05-tools-of-the-trade/section-5.2.html
    Code Fragment 5.2.1   (already correct, keep)
    Code Fragment k.5.1   -> Code Fragment 5.2.2
    Code Fragment k.5.2   -> Code Fragment 5.2.3
    ...
    Table g.1.1           -> Table 5.2.1
    Figure G.1.1          -> Figure 5.2.1

Idempotent. Safe (only touches patterns matching the placeholder shape;
already-correct captions are preserved verbatim).
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

# Section-id extraction from filename
SECTION_FILENAME_RE = re.compile(r'section-([A-Za-z]+|\d+)\.(\d+[a-z]?)\.html', re.IGNORECASE)

# Placeholder caption: <strong>Type [Letter].N.N[letter][:?]</strong>
# Letter MUST be a single A-Z or a-z (real section numbers start with digit).
PLACEHOLDER_RE = re.compile(
    r'<strong>(Table|Code Fragment|Figure|Diagram)\s+([A-Za-z])\.(\d+)\.(\d+)([a-z]?)\s*(:?)\s*</strong>',
    re.IGNORECASE,
)

# Properly-numbered caption: <strong>Type N.N.N[letter][:?]</strong>
# (Sequential counter for that type within this section)
CORRECT_RE_TPL = r'<strong>{type}\s+([0-9]+(?:\.[0-9]+)+)([a-z]?)\s*(:?)\s*</strong>'

# Same patterns inside <caption>...</caption> or <figcaption>...</figcaption>
# We allow Table/Code Fragment/Figure/Diagram only; the leading "Table"
# etc. is captured by the same PLACEHOLDER_RE above (re-applied per file).


def extract_section_id(path: Path) -> str | None:
    m = SECTION_FILENAME_RE.match(path.name)
    if not m:
        return None
    prefix, sec = m.group(1), m.group(2)
    if prefix.isdigit():
        return f"{prefix}.{sec}"
    return f"{prefix.upper()}.{sec}"  # e.g. A.1 for appendices


def collect_correct_max_per_type(text: str) -> dict[str, int]:
    """Return the max sequential counter already used by CORRECT captions."""
    out: dict[str, int] = {}
    for typ in ("Table", "Code Fragment", "Figure", "Diagram"):
        pat = re.compile(CORRECT_RE_TPL.format(type=re.escape(typ)), re.IGNORECASE)
        nums = []
        for m in pat.finditer(text):
            num_str = m.group(1)
            # Take the last dotted segment as the counter
            try:
                last = int(num_str.rsplit(".", 1)[-1])
                nums.append(last)
            except ValueError:
                continue
        out[typ] = max(nums) if nums else 0
    return out


def patch_file(path: Path) -> tuple[int, dict[str, list[str]]]:
    section_id = extract_section_id(path)
    if section_id is None:
        return 0, {}
    text = path.read_text(encoding="utf-8", errors="replace")
    next_n = collect_correct_max_per_type(text)
    # Bump base by 1 to get next free counter
    for k in next_n:
        next_n[k] += 1

    changes: dict[str, list[str]] = {}

    def repl(m: re.Match) -> str:
        typ_in = m.group(1)
        # Normalize type capitalization
        typ = {
            "table": "Table",
            "code fragment": "Code Fragment",
            "figure": "Figure",
            "diagram": "Diagram",
        }[typ_in.lower()]
        n = next_n[typ]
        next_n[typ] += 1
        old = m.group(0)
        # Preserve trailing colon if present, else add none
        colon = m.group(6) or ""
        new = f"<strong>{typ} {section_id}.{n}{colon}</strong>"
        changes.setdefault(typ, []).append(f"{m.group(2)}.{m.group(3)}.{m.group(4)}{m.group(5)} -> {section_id}.{n}")
        return new

    new_text = PLACEHOLDER_RE.sub(repl, text)
    if new_text != text:
        path.write_text(new_text, encoding="utf-8")
        return sum(len(v) for v in changes.values()), changes
    return 0, {}


def main() -> int:
    skip_dirs = {"KDP", "node_modules", ".git", "source_fix_backups", "_archive"}
    total_files = 0
    total_modified = 0
    total_fixes = 0
    for path in ROOT.rglob("section-*.html"):
        rel = path.relative_to(ROOT)
        if any(part in skip_dirs for part in rel.parts):
            continue
        total_files += 1
        try:
            n, changes = patch_file(path)
        except Exception as e:
            print(f"ERR {rel}: {e}", file=sys.stderr)
            continue
        if n:
            total_modified += 1
            total_fixes += n
            print(f"  {n:3d}  {rel}")
            for typ, lst in sorted(changes.items()):
                for line in lst:
                    print(f"        {typ}: {line}")

    print()
    print(f"Files scanned:  {total_files}")
    print(f"Files modified: {total_modified}")
    print(f"Total fixes:    {total_fixes}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
