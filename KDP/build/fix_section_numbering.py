"""Renumber subsection H2s and H3s from flat (1, 2, 3 / 2.1) to hierarchical
(X.Y.1, X.Y.2 / X.Y.2.1, X.Y.2.2).

The book's source uses `<h2>1. Feature Engineering</h2>`, `<h2>2. Supervised
Learning</h2>` etc. inside section files like `section-0.1.html`. This is
confusing — readers can't tell whether "1." means chapter 1, section 1, or
sub-section 1 of section 0.1.

Convention chosen by the user (2026-05-10): hierarchical `0.1.1`, `0.1.2`
for subsections inside section file `section-0.1.html`. Same pattern for
all chapters: `section-X.Y.html` H2s become `X.Y.1`, `X.Y.2`, ...

Idempotent: if an H2 number already contains a dot (looks like it's already
hierarchical), skip it. Re-running is safe.

Coverage:
- 281 source files × ~6 H2s each = ~1700 H2s renumbered
- Skips front-matter, appendices, capstone (those have different schemes)
"""
from __future__ import annotations
import re
import shutil
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Pattern that matches files like section-0.1.html, section-32.10.html.
# Skips front-matter (section-fm.1a.html), appendices (section-c.2.html etc.).
SECTION_FILE_RE = re.compile(r"section-(\d+)\.(\d+[a-z]?)\.html$")

# H2 pattern: matches `<h2>1. Title</h2>` but NOT `<h2>1.2 Title</h2>` (already hierarchical).
# Allows H2 to have attributes (e.g., `<h2 id="foo">`).
H2_FLAT_RE = re.compile(
    r"(<h2[^>]*>\s*)"
    r"(\d+)"  # capture number
    r"(\.\s+)"  # require dot followed by space (NOT another digit)
    r"([^<]+?)"  # title
    r"(\s*</h2>)",
    re.IGNORECASE,
)


def renumber_h2s(content: str, section_prefix: str) -> tuple[str, int]:
    """Replace `<h2>N. Title</h2>` with `<h2>X.Y.N Title</h2>` (no dot after N)."""
    n_changed = 0

    def replace(m: re.Match) -> str:
        nonlocal n_changed
        prefix_html = m.group(1)
        num = m.group(2)
        title = m.group(4)
        suffix_html = m.group(5)
        n_changed += 1
        # Use space (not dot) before title to match common style "0.1.1 Title"
        return f"{prefix_html}{section_prefix}.{num} {title}{suffix_html}"

    new_content = H2_FLAT_RE.sub(replace, content)
    return new_content, n_changed


# Stale-hierarchical H2: looks like "<h2>3.6 Title</h2>" or "<h2>3.7.2 Title</h2>"
# where the leading number does NOT begin with the section's full prefix.
H2_HIER_ANY_RE = re.compile(
    r"(<h2[^>]*>\s*)"
    r"(\d+(?:\.\d+)+)"    # multi-part number like "3.6" or "2.2.1"
    r"(\s+)"              # whitespace separator (NOT a dot — distinguishes from "3.6.")
    r"([^<]+?)"
    r"(\s*</h2>)",
    re.IGNORECASE,
)


def renumber_stale_hier_h2s(content: str, section_prefix: str) -> tuple[str, int]:
    """Renumber H2s like `<h2>3.6 Title</h2>` when "3.6" doesn't match section_prefix.

    Walks H2s in document order. The first stale H2 encountered claims the next
    integer slot (max(correct_siblings)+1), and subsequent stale H2s continue
    incrementing. This preserves the order authors intended.
    """
    # Find every numbered H2 in order to compute the running counter.
    n_changed = 0
    h2_iter = list(H2_HIER_ANY_RE.finditer(content))
    if not h2_iter:
        return content, 0

    # Determine starting counter from any correctly-prefixed siblings already present.
    used = set()
    for m in h2_iter:
        num = m.group(2)
        if num.startswith(section_prefix + "."):
            tail = num[len(section_prefix) + 1:]
            head = tail.split(".")[0]
            if head.isdigit():
                used.add(int(head))
    counter = max(used) if used else 0

    edits: list[tuple[int, int, str]] = []
    for m in h2_iter:
        num = m.group(2)
        if num.startswith(section_prefix + "."):
            continue  # already correct
        counter += 1
        new_num = f"{section_prefix}.{counter}"
        prefix_html, _, sep_ws, title, suffix_html = m.group(1), m.group(2), m.group(3), m.group(4), m.group(5)
        new_h2 = f"{prefix_html}{new_num}{sep_ws}{title}{suffix_html}"
        edits.append((m.start(), m.end(), new_h2))
        n_changed += 1

    for start, end, repl in reversed(edits):
        content = content[:start] + repl + content[end:]
    return content, n_changed


# H2 with full hierarchical prefix (e.g., "4.4.2") — used to track current parent for H3s
H2_HIER_RE = re.compile(
    r"<h2[^>]*>\s*(\d+(?:\.\d+)+)\s+([^<]+?)\s*</h2>",
    re.IGNORECASE,
)

# Any heading tag (we walk in order to know which H2 a given H3 belongs to)
ANY_HEADING_RE = re.compile(r"<(h[1-6])([^>]*)>(.*?)</\1>", re.IGNORECASE | re.DOTALL)

# Stale H3 leading number: matches "1.", "2.1", "3.7.1", "12.3.4" followed by space.
# Allows multi-level (1+ dot-digit groups) and an optional trailing alphabetic tag like "0b".
H3_STALE_LEAD_RE = re.compile(r"^\s*(\d+(?:\.\d+)*[a-z]?)[\.]?\s+(.*)$", re.DOTALL)


def renumber_h3s(content: str, section_prefix: str) -> tuple[str, int]:
    """For each H3 with a stale flat/sub number, replace with `{H2_hier}.{counter}`.

    Walks headings in document order. Tracks the most recent H2's full hierarchical
    number (e.g., "4.4.2"). Resets the H3 counter on each new H2. Only rewrites
    H3s whose title starts with a numeric pattern; H3s like "Prerequisites" or
    "Bibliography" are left untouched.
    """
    n_changed = 0
    current_h2_hier: str | None = None
    h3_counter = 0

    # Build list of (start, end, replacement) edits to apply in reverse.
    edits: list[tuple[int, int, str]] = []

    for m in ANY_HEADING_RE.finditer(content):
        tag = m.group(1).lower()
        attrs = m.group(2)
        inner = m.group(3)
        # Strip nested tags from title for parsing (but keep inner HTML on output).
        title_text = re.sub(r"<[^>]+>", "", inner).strip()

        if tag == "h2":
            # See if it has a hierarchical number already
            hm = re.match(r"^(\d+(?:\.\d+)+)\s+", title_text)
            if hm:
                current_h2_hier = hm.group(1)
                # Only renumber H3s under H2s that match this section's prefix
                # (avoids touching H2s in unrelated/embedded blocks)
                if not current_h2_hier.startswith(section_prefix + "."):
                    current_h2_hier = None
                h3_counter = 0
            else:
                current_h2_hier = None
                h3_counter = 0
        elif tag == "h3" and current_h2_hier:
            sm = H3_STALE_LEAD_RE.match(title_text)
            if not sm:
                continue  # Unnumbered H3 — leave alone
            old_num = sm.group(1)
            # Already correctly hierarchical?
            if title_text.startswith(current_h2_hier + "."):
                continue
            # Decide new number: increment counter
            h3_counter += 1
            new_num = f"{current_h2_hier}.{h3_counter}"
            # Replace inside the original inner HTML — only the leading "OLD " portion.
            # The leading number may live inside arbitrary inline tags; do a tolerant
            # text-level rewrite by reconstructing inner.
            # Strategy: find the first occurrence of `old_num` followed by `.` or whitespace
            # in inner and replace it once.
            pattern = re.compile(r"(\s*)(?:" + re.escape(old_num) + r")\.?\s+", re.DOTALL)
            def _repl(mm: re.Match) -> str:
                return mm.group(1) + new_num + " "
            new_inner, n_sub = pattern.subn(_repl, inner, count=1)
            if n_sub == 0:
                continue
            new_heading = f"<h3{attrs}>{new_inner}</h3>"
            edits.append((m.start(), m.end(), new_heading))
            n_changed += 1

    # Apply edits in reverse so offsets stay valid
    for start, end, repl in reversed(edits):
        content = content[:start] + repl + content[end:]
    return content, n_changed


def main() -> int:
    files_modified: list[tuple[str, str, int]] = []
    backup_dir = PROJECT_ROOT / "KDP/build/source_fix_backups" / time.strftime("section_numbering_%Y%m%d_%H%M%S")

    for path in PROJECT_ROOT.rglob("*.html"):
        if any(part in path.parts for part in ("KDP", "vendor", "scripts", "templates", "md", "node_modules")):
            continue
        m = SECTION_FILE_RE.search(path.name)
        if not m:
            continue
        section_prefix = f"{m.group(1)}.{m.group(2)}"

        text = path.read_text(encoding="utf-8", errors="replace")
        new_text, n_h2 = renumber_h2s(text, section_prefix)
        new_text, n_h2b = renumber_stale_hier_h2s(new_text, section_prefix)
        new_text, n_h3 = renumber_h3s(new_text, section_prefix)
        n = n_h2 + n_h2b + n_h3
        if n == 0:
            continue
        backup_dir.mkdir(parents=True, exist_ok=True)
        rel = path.relative_to(PROJECT_ROOT)
        backup = backup_dir / rel
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, backup)
        path.write_text(new_text, encoding="utf-8")
        files_modified.append((str(rel).replace("\\", "/"), section_prefix, n))

    total_h2 = sum(n for _, _, n in files_modified)
    print(f"Renumbered {total_h2} headings (H2+H3) in {len(files_modified)} section files")
    print(f"Hierarchical scheme: 0.1.1, 0.1.2, 0.2.1, ... (chapter.section.subsection)")
    if files_modified:
        print(f"\nBackups: {backup_dir.relative_to(PROJECT_ROOT)}")
        print(f"\nFirst 10 files:")
        for rel, prefix, n in files_modified[:10]:
            print(f"  {n:>2}x  [{prefix}] {rel}")
        if len(files_modified) > 10:
            print(f"  ... +{len(files_modified) - 10} more")
    return 0


if __name__ == "__main__":
    sys.exit(main())
