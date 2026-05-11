"""v3.5 R3#4: Slim Module 32 (Safety, Ethics & Society) from 18 sections.

Audit finding: Module 32 absorbed Module 35 leftovers in v3.2 and now sits
at 18 sections (largest in book). 32.16-18 are essay-style scope-creep:

  32.16 Societal Impact and the Road Ahead       -> DELETE
  32.17 Open Research Problems                   -> DELETE
  32.18 The Future of Human-AI Collaboration     -> DELETE
  32.14 Alignment Research Frontiers             -> KEEP (real content)

These 3 essays don't match the technical-reference voice of the rest of
Module 32 (OWASP, Prompt Injection, PII, Hallucination, Privacy, etc.).

After deletion: Module 32 has 15 sections. Inbound xrefs redirect to
the closest surviving section.

(Audit also suggested merging 32.10 -> 32.3 and 32.13 -> 32.12 but those
require content merge; we defer those to a manual editorial pass.)
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
EXCLUDE = {"_archive", "KDP", "node_modules", "vendor", "scripts"}

DELETIONS = [
    ("part-9-safety-strategy/module-32-safety-ethics-regulation/section-32.16.html",
     "section-32.14"),  # alignment frontiers as nearest survivor
    ("part-9-safety-strategy/module-32-safety-ethics-regulation/section-32.17.html",
     "section-32.14"),
    ("part-9-safety-strategy/module-32-safety-ethics-regulation/section-32.18.html",
     "section-32.14"),
]


def main() -> int:
    n_files = 0
    n_links = 0
    delete_paths = {d[0] for d in DELETIONS}

    for p in ROOT.rglob("*.html"):
        if any(part in p.parts for part in EXCLUDE):
            continue
        if p.relative_to(ROOT).as_posix() in delete_paths:
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        original = text
        for delpath, target in DELETIONS:
            old_base = Path(delpath).stem
            text, n = re.subn(rf'\b{re.escape(old_base)}\.html', f'{target}.html', text)
            n_links += n
        if text != original:
            p.write_text(text, encoding="utf-8")
            n_files += 1

    print(f"Rewrote {n_links} links across {n_files} files")
    print("Deleting:")
    deleted_words = 0
    for delpath, _ in DELETIONS:
        f = ROOT / delpath
        if f.exists():
            words = len(re.sub(r"<[^>]+>", " ",
                f.read_text(encoding="utf-8", errors="replace")).split())
            deleted_words += words
            f.unlink()
            print(f"  rm {delpath}  ({words} words)")
    print(f"\nTotal words removed: {deleted_words:,}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
