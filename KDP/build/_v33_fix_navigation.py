"""v3.3 Tier 1: Fix broken hrefs from restructure + label-vs-href mismatches.

Three classes of bugs introduced by v3.x restructure scripts:

  1. Hrefs pointing to deleted module dirs (module-16/30/35).
     Fix: redirect to the absorbing module dir.

  2. Hrefs pointing to absorbed section paths but using the OLD module dir
     (e.g. module-30-observability-monitoring/section-29.1.html). Fix:
     swap dir to the new owner.

  3. <a href="...section-15.5.html">Section 16.1</a> mismatches: my v3.x
     scripts updated hrefs but left the displayed text. Fix: regenerate the
     `Section X.Y` text from the actual file number.

Also normalizes zero-padded labels (`Section 08.2` -> `Section 8.2`).

Run from project root:
    /c/Python314/python KDP/build/_v33_fix_navigation.py
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
EXCLUDE = {"_archive", "KDP", "node_modules", "vendor", "scripts"}

# Class 1+2: directory-level redirects for broken/moved modules.
# Pattern is on the URL path component name, not anchored to position.
DIR_REDIRECTS = [
    # Module 16 -> Module 15 (PEFT absorbed Distillation in v3.2)
    ("module-16-distillation-merging", "module-15-peft"),
    # Module 30 -> Module 29 (Evaluation absorbed Observability in v3.2)
    ("module-30-observability-monitoring", "module-29-evaluation-observability"),
    # Module 35 -> Module 32 (Safety absorbed AI&Society leftovers in v3.2)
    # NOTE: section-22.7 and section-26.X under module-35 actually live in
    # different modules; handle those explicitly below.
    ("module-35-ai-society", "module-32-safety-ethics-regulation"),
]

# Class 2 explicit overrides (file-level redirects where directory mapping
# above would land on the wrong module).
FILE_REDIRECTS = [
    # section-22.7 was the agent memory chapter; misfiled under module-35
    ("module-35-ai-society/section-22.7.html",
     "module-22-ai-agents/section-22.7.html"),
    # 26.8/9/10 (originally 35.5/6/8) belong in module-26
    ("module-35-ai-society/section-26.8.html",
     "module-26-agent-safety-production/section-26.8.html"),
    ("module-35-ai-society/section-26.9.html",
     "module-26-agent-safety-production/section-26.9.html"),
    ("module-35-ai-society/section-26.10.html",
     "module-26-agent-safety-production/section-26.10.html"),
]

# Anchor-text vs href fix: rewrite the displayed text to match the file.
# Catches: <a href="...section-15.5.html">Section 16.1</a> -> Section 15.5
LINK_LABEL_RE = re.compile(
    r'(<a[^>]*href="[^"]*section-(\d+(?:\.\d+)*)\.html(?:#[^"]*)?"[^>]*>)'
    r'(\s*Section\s+)(\d+(?:\.\d+)*)(\s*[A-Za-z()&;:,]?[^<]*)(</a>)',
    flags=re.IGNORECASE,
)


def fix_link_labels(text: str) -> tuple[str, int]:
    n = 0

    def _sub(m: re.Match) -> str:
        nonlocal n
        opening = m.group(1)
        file_num = m.group(2)
        prefix = m.group(3)
        label_num = m.group(4)
        suffix = m.group(5)
        closing = m.group(6)
        # Normalize: drop leading zeros in file_num parts to compare
        norm_file = ".".join(str(int(x)) for x in file_num.split("."))
        norm_label = ".".join(str(int(x)) for x in label_num.split("."))
        if norm_label == norm_file:
            return m.group(0)  # already matches
        n += 1
        return f"{opening}{prefix}{file_num}{suffix}{closing}"

    return LINK_LABEL_RE.sub(_sub, text), n


def main() -> int:
    n_dir_redirects = 0
    n_file_redirects = 0
    n_label_fixes = 0
    n_files_changed = 0

    for p in ROOT.rglob("*.html"):
        if any(part in p.parts for part in EXCLUDE):
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        original = text

        # File-level redirects FIRST (more specific than dir-level)
        for old, new in FILE_REDIRECTS:
            if old in text:
                count = text.count(old)
                text = text.replace(old, new)
                n_file_redirects += count

        # Dir-level redirects
        for old_dir, new_dir in DIR_REDIRECTS:
            # Use a non-greedy boundary: the directory name as a path component
            pattern = rf'(?<=[/"]){re.escape(old_dir)}(?=/)'
            text, count = re.subn(pattern, new_dir, text)
            n_dir_redirects += count

        # Label-vs-href fixes
        text, n = fix_link_labels(text)
        n_label_fixes += n

        if text != original:
            p.write_text(text, encoding="utf-8")
            n_files_changed += 1

    print(f"Files changed:        {n_files_changed}")
    print(f"Dir redirects:        {n_dir_redirects}")
    print(f"File redirects:       {n_file_redirects}")
    print(f"Label-vs-href fixes:  {n_label_fixes}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
