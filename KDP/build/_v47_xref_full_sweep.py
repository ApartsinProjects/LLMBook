"""v4.7: Deeper cross-reference validity sweep.

Beyond v4.6 (which validated href TARGETS exist), this checks:
  1. The 31 remaining unfixable hrefs - identify each, propose action
  2. Anchor-level (#fragment) validity - href="...html#some-id" where
     no element with id="some-id" exists in the target file
  3. Strip truly unfixable broken hrefs (replace with text-only label)
"""
from __future__ import annotations
import re
import sys
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parent.parent.parent
EXCLUDE = {"_archive", "KDP", "node_modules", "vendor", "scripts", "agents"}
MAX_FILE = 5_000_000

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


def safe_read(p: Path) -> str | None:
    try:
        if p.stat().st_size > MAX_FILE: return None
        return p.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return None


# Build filename -> [actual_paths] index AND id -> set(file) index
def build_indexes() -> tuple[dict, dict]:
    file_idx = {}
    id_idx = defaultdict(set)
    for p in ROOT.rglob("*.html"):
        if any(part in p.parts for part in EXCLUDE): continue
        file_idx.setdefault(p.name, []).append(p)
        text = safe_read(p)
        if text:
            for m in re.finditer(r'\bid="([^"]+)"', text):
                id_idx[(p.name, m.group(1))].add(p.name)
    return file_idx, id_idx


def main() -> int:
    file_idx, id_idx = build_indexes()
    href_re = re.compile(r'(<a\s+[^>]*href=")([^"]+\.html)(#[^"]*)?(")', re.IGNORECASE)

    n_files = 0
    n_unfixable_anchors = 0
    n_anchor_broken = 0
    n_unfixable_files = 0
    n_unwrapped = 0
    truly_unfixable = []

    for p in ROOT.rglob("*.html"):
        if any(part in p.parts for part in EXCLUDE): continue
        text = safe_read(p)
        if text is None: continue
        original = text
        parent = p.parent

        def maybe_fix(m: re.Match) -> str:
            nonlocal n_unfixable_files, n_anchor_broken, n_unwrapped
            prefix, href, anchor, suffix = m.group(1), m.group(2), m.group(3) or "", m.group(4)
            if href.startswith(("http://", "https://", "mailto:", "javascript:", "data:")):
                return m.group(0)
            try:
                target = (parent / href).resolve()
            except Exception:
                return m.group(0)
            if not target.exists():
                # File doesn't exist anywhere?
                filename = href.rsplit("/", 1)[-1]
                if filename not in file_idx:
                    n_unfixable_files += 1
                    truly_unfixable.append((str(p.relative_to(ROOT).as_posix()), href + anchor))
                    # Find the </a> and unwrap to plain text
                    # The full anchor pattern: <a ...>TEXT</a>
                    # We can't unwrap inside a sub() callback easily — just leave
                    return m.group(0)
                return m.group(0)
            # File exists - check anchor
            if anchor:
                anchor_id = anchor.lstrip("#")
                if (target.name, anchor_id) not in id_idx:
                    n_anchor_broken += 1
                    # Strip the anchor (keep file link)
                    return f"{prefix}{href}{suffix}"
            return m.group(0)

        text = href_re.sub(maybe_fix, text)
        if text != original:
            p.write_text(text, encoding="utf-8")
            n_files += 1

    # Now unwrap truly unfixable hrefs (where target file doesn't exist)
    print(f"Anchor-only mismatches stripped: {n_anchor_broken}")
    print(f"Files with anchor strips: {n_files}")
    print(f"\nTruly unfixable hrefs (target file doesn't exist anywhere): {n_unfixable_files}")
    print("Sample (up to 20):")
    for f, h in truly_unfixable[:20]:
        print(f"  {f}: {h}")

    # For unfixable, unwrap the anchor to plain text
    if truly_unfixable:
        print("\nUnwrapping unfixable anchors...")
        bad_targets = set(h.split("#")[0].rsplit("/", 1)[-1] for _, h in truly_unfixable)
        n_unwrap_files = 0
        for p in ROOT.rglob("*.html"):
            if any(part in p.parts for part in EXCLUDE): continue
            text = safe_read(p)
            if text is None: continue
            original = text
            for bad in bad_targets:
                # Strip <a href="...bad" ...>TEXT</a> -> TEXT
                pat = re.compile(
                    rf'<a\s+[^>]*href="[^"]*{re.escape(bad)}(?:#[^"]*)?"[^>]*>(.*?)</a>',
                    re.DOTALL,
                )
                text = pat.sub(r'\1', text)
            if text != original:
                p.write_text(text, encoding="utf-8")
                n_unwrap_files += 1
        print(f"  Unwrapped unfixable links in {n_unwrap_files} files")

    return 0


if __name__ == "__main__":
    sys.exit(main())
