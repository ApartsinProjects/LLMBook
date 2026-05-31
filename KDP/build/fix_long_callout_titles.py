"""Split overly long callout titles into title + body paragraph.

ROOT CAUSE
  Some Algorithm (and similar) callouts have a 1-3 sentence description
  inside <div class="callout-title">. Because the CSS makes the whole
  title element bold, the reader sees a wall of bold text where only
  the short label "Algorithm N.N.N" should be bold.

DETECTION
  <div class="callout-title">Algorithm N.N.N[a-z]?: <long descriptive
  sentence ending in a period>.</div>
  where the descriptive text exceeds 60 characters.

FIX
  Split into:
    <div class="callout-title">Algorithm N.N.N</div>
    <p>The long descriptive sentence ...</p>
  preserving the trailing newline.

  Additionally: if the algorithm number doesn't match the section file
  (e.g. "Algorithm 48.1.1" inside section-18.7.html), renumber to use
  the section_id from the filename.

Idempotent.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

SECTION_FILENAME_RE = re.compile(r'section-([A-Za-z]+|\d+)\.(\d+[a-z]?)\.html', re.IGNORECASE)

# <div class="callout-title">LABEL N.N.N[suffix]: BODY...</div>
# LABEL is the callout type word: Algorithm, Theorem, Definition, etc.
# Capture so we can rebuild.
TITLE_RE = re.compile(
    r'(<div class="callout-title">)(Algorithm|Theorem|Definition|Proposition|Lemma|Proof|Example|Claim)\s+([0-9]+(?:\.[0-9]+)+|[A-Za-z]+\.[0-9]+(?:\.[0-9]+)*)([a-z]?)\s*:\s*(.+?)(</div>)',
    re.IGNORECASE | re.DOTALL,
)


def extract_section_id(path: Path) -> str | None:
    m = SECTION_FILENAME_RE.match(path.name)
    if not m:
        return None
    prefix, sec = m.group(1), m.group(2)
    if prefix.isdigit():
        return f"{prefix}.{sec}"
    return f"{prefix.upper()}.{sec}"


def patch_file(path: Path) -> tuple[int, list[str]]:
    section_id = extract_section_id(path)
    if section_id is None:
        return 0, []
    text = path.read_text(encoding="utf-8", errors="replace")
    changes: list[str] = []
    # Track next sequential counter per (file, type) for renumbering
    counters: dict[str, int] = {}

    def already_used(typ: str, num: str) -> set[int]:
        """Find existing correct numbers of form section_id.N for this type."""
        pat = re.compile(
            rf'<div class="callout-title">{re.escape(typ)}\s+{re.escape(section_id)}\.([0-9]+)',
            re.IGNORECASE,
        )
        return set(int(m.group(1)) for m in pat.finditer(text))

    def next_counter(typ: str) -> int:
        if typ not in counters:
            used = already_used(typ, "")
            counters[typ] = max(used) + 1 if used else 1
        else:
            counters[typ] += 1
        return counters[typ]

    def repl(m: re.Match) -> str:
        prefix = m.group(1)
        typ_in = m.group(2)
        num_str = m.group(3)
        suffix = m.group(4) or ""
        body = m.group(5).strip()
        close = m.group(6)

        # Normalize type capitalization
        typ = typ_in.capitalize()

        # Only act if body is "long" (>60 chars) AND ends with a period or contains '.'
        if len(body) < 60:
            return m.group(0)
        if "." not in body:
            return m.group(0)

        # Decide whether to renumber: if num_str doesn't start with section_id
        num_main = num_str.split(".", 1)[0]
        sec_main = section_id.split(".", 1)[0]
        if num_main != sec_main:
            # Wrong section prefix — renumber
            n = next_counter(typ)
            new_num = f"{section_id}.{n}"
            changes.append(f"renumber: {typ} {num_str}{suffix} -> {new_num}")
        else:
            new_num = num_str + suffix

        # Body: keep as paragraph. Strip trailing period if it looks like the
        # callout-title was constructed as "Type N: Long sentence." — preserve
        # the period in the body paragraph.
        body_clean = body.strip()
        # Ensure body sentence ends with period
        if not body_clean.endswith((".", "!", "?")):
            body_clean += "."

        new_html = (
            f'{prefix}{typ} {new_num}{close}\n'
            f'<p>{body_clean}</p>'
        )
        changes.append(f"split: {typ} {new_num} (body {len(body_clean)} chars)")
        return new_html

    new_text = TITLE_RE.sub(repl, text)
    if new_text != text:
        path.write_text(new_text, encoding="utf-8")
        return len(changes), changes
    return 0, []


def main() -> int:
    skip_dirs = {"KDP", "node_modules", ".git", "source_fix_backups", "_archive"}
    total_files = 0
    total_mod = 0
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
            total_mod += 1
            total_fixes += n
            print(f"  {n:2d}  {rel}")
            for c in changes:
                print(f"        {c}")
    print()
    print(f"Files scanned:  {total_files}")
    print(f"Files modified: {total_mod}")
    print(f"Total fixes:    {total_fixes}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
