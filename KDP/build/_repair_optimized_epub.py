"""Repair entity-mangling done by epub-optimizer's HTML minifier.

The minifier strips trailing semicolons from named entities that look "safe"
to it (&apos, &quot, &amp, &gt, &lt) which then fail XML parsing.

This script: extracts the optimized EPUB, fixes affected entities in every
.xhtml file, and re-zips with proper EPUB structure (mimetype first, stored).
"""
from __future__ import annotations
import re, sys, shutil, zipfile
from pathlib import Path

BROKEN_ENTITY_RE = re.compile(r'&(apos|quot|amp|gt|lt|nbsp)(?![a-zA-Z;#])')

# Non-void HTML elements that ebooklib + lxml emit as self-closing
# (e.g. `<span class="vlist-s"/>`). HTML5 readers don't honor self-closing
# on these and treat them as opening-only tags, swallowing subsequent text.
# Word-boundary requirement (\s or no attrs) prevents matching <img/> as <i + mg.../>
SELF_CLOSING_RE = re.compile(
    r'<(span|div|p|a|td|th|li|strong|em|b|i|sub|sup|small|code|pre)(\s[^>]*|)/>'
)


def repair(in_path: Path, out_path: Path) -> tuple[int, int]:
    """Returns (files_changed, total_replacements)."""
    work_dir = in_path.parent / "_repair_temp"
    if work_dir.exists():
        shutil.rmtree(work_dir)
    work_dir.mkdir(parents=True)

    with zipfile.ZipFile(in_path) as z:
        z.extractall(work_dir)

    files_changed = 0
    total_repls = 0
    total_self_close = 0
    for p in work_dir.rglob("*.xhtml"):
        text = p.read_text(encoding="utf-8", errors="replace")
        new_text, n = BROKEN_ENTITY_RE.subn(lambda m: f"&{m.group(1)};", text)
        new_text, n_sc = SELF_CLOSING_RE.subn(r'<\1\2></\1>', new_text)
        if n or n_sc:
            p.write_text(new_text, encoding="utf-8")
            files_changed += 1
            total_repls += n
            total_self_close += n_sc
    if total_self_close:
        print(f"  [repair] expanded {total_self_close} self-closing non-void tags")

    # Repack: mimetype first uncompressed, everything else stored compressed
    if out_path.exists():
        out_path.unlink()
    mimetype_path = work_dir / "mimetype"
    with zipfile.ZipFile(out_path, "w") as z:
        if mimetype_path.exists():
            z.write(mimetype_path, "mimetype", compress_type=zipfile.ZIP_STORED)
        for p in sorted(work_dir.rglob("*")):
            if not p.is_file() or p == mimetype_path:
                continue
            arcname = str(p.relative_to(work_dir)).replace("\\", "/")
            z.write(p, arcname, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)

    shutil.rmtree(work_dir)
    return files_changed, total_repls


if __name__ == "__main__":
    in_p = Path(sys.argv[1])
    out_p = Path(sys.argv[2]) if len(sys.argv) > 2 else in_p
    fc, n = repair(in_p, out_p)
    print(f"Repaired {n} broken entities across {fc} files")
    print(f"Output: {out_p} ({out_p.stat().st_size / 1024 / 1024:.2f} MB)")
