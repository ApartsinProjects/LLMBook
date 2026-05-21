"""Wave 42 fix: add canonical type-word prefix to callout titles flagged by
CALLOUT_TITLE_PREFIX. Operates surgically: only rewrites titles that fail the
prefix check and only inside callouts whose class is in the known set.

Rules:
  warning + "Common Misconception"           -> "Warning: Common Misconception"
  note    + "Why This Surprises ..."          -> "Note: Why This Surprises ..."
  key-insight + "[lightbulb] Aha Moment: ..." -> "Key Insight: Aha Moment ..."
  key-insight + "[lightbulb] Worked Example:" -> "Key Insight: Worked Example..."
  key-insight + "[lightbulb] Mental Model:"   -> "Key Insight: Mental Model..."
  (general) key-insight starting with literal lightbulb entity but no prefix
     -> "Key Insight: <rest>"

Style rules: no em-dashes, no double-dashes.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(r"E:/Projects/BookBlogsHome/LLMBook")
PY = r"C:/Python314/python.exe"


def get_issues():
    out = subprocess.run(
        [PY, str(REPO_ROOT / "scripts/run_book_audit.py"),
         "--checks", "CALLOUT_TITLE_PREFIX", "--json"],
        capture_output=True, text=True, cwd=str(REPO_ROOT),
    )
    data = json.loads(out.stdout)
    return data["issues"]


# Map callout type -> default prefix to inject.
PREFIX_BY_TYPE = {
    "warning": "Warning",
    "note": "Note",
    "key-insight": "Key Insight",
    "tip": "Tip",
    "fun-note": "Fun Note",
    "exercise": "Exercise",
    "lab": "Lab",
    "self-check": "Self-Check",
}


def fix_callout_title(html: str, ctype: str, raw_title: str) -> str | None:
    """Return new title text (no tags) or None if cannot fix safely."""
    # Strip outer whitespace.
    raw_title = raw_title.strip()
    # Strip leading lightbulb entity + optional space.
    body = re.sub(r"^&#128161;\s*", "", raw_title)
    body = body.strip()
    if not body:
        return None
    prefix = PREFIX_BY_TYPE.get(ctype)
    if not prefix:
        return None
    # If body already starts with the prefix (case-insensitive), return as-is.
    if body.lower().startswith(prefix.lower()):
        return body
    return f"{prefix}: {body}"


def apply_fix(filepath: Path, line_num: int) -> bool:
    text = filepath.read_text(encoding="utf-8")
    lines = text.split("\n")
    # The audit reports the line where the callout div *starts*, so the title is on the next line.
    # But the regex spans both lines. Find the callout-block on or near line_num.
    # Find next <div class="callout-title"> after line_num-1.
    idx = max(0, line_num - 1)
    target_line = None
    for j in range(idx, min(idx + 5, len(lines))):
        if "callout-title" in lines[j]:
            target_line = j
            break
    if target_line is None:
        return False
    # Detect the ctype from the preceding callout div (search up to 4 lines back).
    ctype = None
    for k in range(target_line, max(target_line - 5, -1), -1):
        m = re.search(r'class="callout\s+([a-z-]+)"', lines[k])
        if m:
            ctype = m.group(1).lower()
            break
    if not ctype:
        return False
    # Extract title content via regex on the single line (or span lines).
    title_re = re.compile(
        r'(<div\s+class="callout-title"[^>]*>)(.*?)(</div>)',
        re.IGNORECASE,
    )
    m = title_re.search(lines[target_line])
    if not m:
        # title may span lines; reconstruct via 2-3 line join.
        joined = "\n".join(lines[target_line:target_line + 4])
        m = title_re.search(joined)
        if not m:
            return False
        # bail on multi-line edits (rare; do nothing).
        return False
    raw_title = m.group(2)
    new_title = fix_callout_title(text, ctype, raw_title)
    if new_title is None:
        return False
    if new_title.strip() == raw_title.strip():
        return False
    old_full = m.group(0)
    new_full = f"{m.group(1)}{new_title}{m.group(3)}"
    new_line = lines[target_line].replace(old_full, new_full, 1)
    if new_line == lines[target_line]:
        return False
    lines[target_line] = new_line
    filepath.write_text("\n".join(lines), encoding="utf-8")
    return True


def main():
    issues = get_issues()
    print(f"Found {len(issues)} CALLOUT_TITLE_PREFIX issues")
    fixed = 0
    skipped = []
    for iss in issues:
        rel = iss["file"]
        fp = REPO_ROOT / rel.replace("\\", "/")
        if not fp.exists():
            skipped.append((rel, "missing"))
            continue
        ok = apply_fix(fp, iss["line"])
        if ok:
            fixed += 1
        else:
            skipped.append((rel + ":" + str(iss["line"]), "no-match"))
    print(f"Fixed {fixed} / {len(issues)}")
    if skipped:
        print("Skipped:")
        for s in skipped:
            print("  ", s)


if __name__ == "__main__":
    main()
