"""Execute the appendix consolidation moves.

For each section_moves entry:
  1. git mv source -> destination (preserves history).
  2. Rewrite breadcrumb (Part / Chapter), page-current (Section N.M),
     title tag, h1, pagefind-meta to match new home.
  3. Rewrite same-folder section refs (siblings now different).

For each appendices_to_delete:
  1. Replace its index.html with a redirect stub linking to the new
     section URLs.
  2. Remove all other files (section-X.Y.html siblings should have moved).

DRY-RUN by default; --apply to execute.
"""
from __future__ import annotations
import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
MAP = HERE / "migration-map.json"

PART_META = {
    "part-1-foundations": ("I", "Foundations"),
    "part-2-understanding-llms": ("II", "Understanding LLMs"),
    "part-3-working-with-llms": ("III", "Working with LLMs"),
    "part-4-training-adapting": ("IV", "LLM Training and Adaptation"),
    "part-5-retrieval-conversation": ("V", "Retrieval and Conversation with LLMs and Agents"),
    "part-6-agentic-ai": ("VI", "Agentic AI"),
    "part-7-multimodal-generation": ("VII", "Multimodal Generation"),
    "part-8-evaluation-production": ("VIII", "Evaluation of LLM-Based Systems"),
    "part-10-idea-to-product": ("X", "Building LLM and Agent Products"),
}


def parse_section_num(filename: str) -> tuple[str, str] | None:
    """Parse 'section-X.Y.html' or 'section-a.B.html' (letter form)."""
    m = re.match(r"section-([a-zA-Z0-9]+)\.(\d+)\.html", filename)
    if not m:
        return None
    return m.group(1), m.group(2)


def get_chapter_title(mod_dir: Path) -> str:
    idx = mod_dir / "index.html"
    if not idx.exists():
        return "?"
    t = idx.read_text(encoding="utf-8")
    m = re.search(r"<h1>([^<]+)</h1>", t)
    return m.group(1) if m else "?"


def get_chapter_num_from_slug(slug: str) -> int | None:
    m = re.match(r"module-(\d+)-", slug)
    if m:
        return int(m.group(1))
    return None


def rewrite_section_metadata(text: str, src_path: str, dst_path: str, title_new: str) -> str:
    """Rewrite section metadata for cross-section move."""
    src_name = src_path.split("/")[-1]
    dst_name = dst_path.split("/")[-1]
    src_num = parse_section_num(src_name)
    dst_num = parse_section_num(dst_name)
    if not (src_num and dst_num):
        return text

    src_ch, src_n = src_num  # may be letters like 'c' / 'g' or numbers
    dst_ch, dst_n = dst_num

    src_label_upper = src_ch.upper() if src_ch.isalpha() else src_ch

    # Determine new part metadata
    dst_part_slug = dst_path.split("/")[0]
    dst_part = PART_META.get(dst_part_slug, ("?", "?"))
    dst_roman, dst_part_title = dst_part

    # Determine new chapter title from destination module's index.html
    dst_mod_slug = dst_path.split("/")[1]
    dst_mod_dir = ROOT / dst_part_slug / dst_mod_slug
    new_chapter_title = get_chapter_title(dst_mod_dir)
    new_chapter_num = get_chapter_num_from_slug(dst_mod_slug) or 0

    # Replace "Section X.Y" or "Section X.Y" (X may be letter)
    text = re.sub(
        rf"\bSection {re.escape(src_label_upper)}\.{src_n}\b",
        f"Section {dst_ch}.{dst_n}",
        text,
    )
    # Lowercase form too
    text = re.sub(
        rf"\bSection {re.escape(src_ch.lower())}\.{src_n}\b",
        f"Section {dst_ch}.{dst_n}",
        text,
    )
    # Title tag
    text = re.sub(
        rf"<title>Section [a-zA-Z]\.{src_n}:?",
        f"<title>Section {dst_ch}.{dst_n}:",
        text,
    )
    # Update title text (use title_new)
    text = re.sub(
        rf"(<title>Section {dst_ch}\.{dst_n}:?\s*)([^<]+)(</title>)",
        rf"\g<1>{title_new}\g<3>",
        text,
        count=1,
    )
    # h1 — rewrite to title_new
    text = re.sub(
        r"<h1>[^<]+</h1>",
        f"<h1>{title_new}</h1>",
        text,
        count=1,
    )
    # page-current
    text = re.sub(
        rf'<div class="page-current">Section [a-zA-Z]\.{src_n}</div>',
        f'<div class="page-current">Section {dst_ch}.{dst_n}</div>',
        text,
    )
    # Breadcrumb part link
    text = re.sub(
        r'<a href="\.\./index\.html">Part [a-zA-Z\d]+(?:: [^<]+)?</a>',
        f'<a href="../index.html">Part {dst_roman}: {dst_part_title}</a>',
        text,
    )
    # Breadcrumb appendix link (was "Appendix X" — now Chapter N)
    text = re.sub(
        r'<a href="index\.html">Appendix [A-Za-z](?:: [^<]+)?</a>',
        f'<a href="index.html">Chapter {new_chapter_num}: {new_chapter_title}</a>',
        text,
    )
    # pagefind-meta part
    text = re.sub(
        r'data-pagefind-meta="part:Part [a-zA-Z\d]+(?:: [^"]+)?"',
        f'data-pagefind-meta="part:Part {dst_roman}: {dst_part_title}"',
        text,
    )
    # pagefind-meta chapter (was "Appendix" -> chapter)
    text = re.sub(
        r'data-pagefind-meta="chapter:Appendix [A-Za-z](?:: [^"]+)?"',
        f'data-pagefind-meta="chapter:Chapter {new_chapter_num}: {new_chapter_title}"',
        text,
    )
    # description meta
    text = re.sub(
        r'<meta content="Section [a-zA-Z]\.\d+:?[^"]+" name="description"/>',
        f'<meta content="Section {dst_ch}.{dst_n}: {title_new}. A comprehensive section from the Building Conversational AI textbook." name="description"/>',
        text,
        count=1,
    )

    return text


def write_redirect_stub(app_dir: Path, moves_for_this_app: list[dict], dry_run: bool) -> bool:
    """Write a redirect-stub index.html that lists where the appendix's
    sections have moved."""
    if not app_dir.exists():
        return False
    # Build the table
    rows = []
    for entry in moves_for_this_app:
        old_name = entry["from"].split("/")[-1]
        new_path = entry["to"]
        new_name = new_path.split("/")[-1]
        new_title = entry.get("title_new", new_name)
        # Compute relative path from app_dir (which is appendices/appendix-X-...)
        # to new_path (which is part-N-.../module-M-.../section-X.Y.html)
        rel = f"../../{new_path}"
        rows.append(
            f'<tr><td><code>{old_name}</code></td>'
            f'<td><a href="{rel}">{new_title}</a></td></tr>'
        )

    appendix_name = app_dir.name  # e.g. appendix-c-huggingface-ecosystem
    appendix_letter = appendix_name.split("-")[1].upper() if "-" in appendix_name else "?"

    # Build the rest of the appendix display title
    raw = appendix_name[len(f"appendix-{appendix_letter.lower()}-"):]
    title = raw.replace("-", " ").title()

    stub = f"""<!DOCTYPE html>

<html lang="en">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<meta content="Appendix {appendix_letter}: {title} (redirected). Content has been consolidated into part-specific Tools of the Trade chapters." name="description"/>
<title>Appendix {appendix_letter}: Content Moved | Building Conversational AI with LLMs and Agents</title>
<link href="../../styles/book.css" rel="stylesheet"/>
<script defer="" src="../../scripts/book.js"></script>
</head>
<body class="index-page appendix-redirect">
<header class="chapter-header">
<nav class="header-nav">
        <a class="book-title-link" href="../../index.html">Building Conversational AI with LLMs and Agents</a>
        <a class="toc-link" href="../../toc.html" title="Table of Contents"><span class="toc-icon">☰</span> Contents</a>
</nav>
<h1>Appendix {appendix_letter}: {title}</h1>
</header>
<main class="content">
<div class="callout note">
<div class="callout-title">This content has moved</div>
<p>In the v12 reorganization, the sections from this appendix were
consolidated into part-specific Tools of the Trade chapters so the
content lives near where it is first needed in the reading flow.</p>
<p>The table below maps each old section to its new home:</p>
</div>
<table class="content-moved-table">
<thead>
<tr><th>Old section</th><th>New home</th></tr>
</thead>
<tbody>
{chr(10).join(rows)}
</tbody>
</table>
</main>
<nav class="chapter-nav">
<a class="up" href="../index.html"><span class="nav-label">Up</span>
<span class="nav-num">Appendices</span><span class="nav-title">Index</span></a>
</nav>
<footer><p>Fifteenth Edition, 2026 · <a href="../../toc.html">Contents</a></p></footer>
</body>
</html>
"""
    idx = app_dir / "index.html"
    if not dry_run:
        idx.write_text(stub, encoding="utf-8")
    return True


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    dry_run = not args.apply
    data = json.loads(MAP.read_text(encoding="utf-8"))

    print("=== Appendix C-N Consolidation: Phase 10 (execute moves) ===")
    if dry_run:
        print("(DRY-RUN; pass --apply to execute)")
    print()

    # 1. git mv each section + rewrite content
    n_moved = 0
    for entry in data["section_moves"]:
        src = ROOT / entry["from"]
        dst = ROOT / entry["to"]
        if not src.exists():
            print(f"  SKIP (no source): {entry['from']}")
            continue
        if dst.exists():
            print(f"  SKIP (dst exists): {entry['to']}")
            continue
        print(f"  git mv {entry['from']} -> {entry['to']}")
        if not dry_run:
            dst.parent.mkdir(parents=True, exist_ok=True)
            result = subprocess.run(
                ["git", "mv", str(src), str(dst)],
                cwd=ROOT, capture_output=True, text=True,
            )
            if result.returncode != 0:
                print(f"  ERROR git mv: {result.stderr}")
                continue
            # Rewrite metadata
            text = dst.read_text(encoding="utf-8")
            text = rewrite_section_metadata(text, entry["from"], entry["to"], entry["title_new"])
            dst.write_text(text, encoding="utf-8")
        n_moved += 1

    # 2. Write redirect stubs for each deleted appendix
    print()
    print("--- Redirect stubs ---")
    n_stubs = 0
    by_appendix: dict[str, list[dict]] = {}
    for entry in data["section_moves"]:
        appendix = "/".join(entry["from"].split("/")[:2])  # appendices/appendix-X-...
        by_appendix.setdefault(appendix, []).append(entry)
    for appendix, entries in by_appendix.items():
        app_dir = ROOT / appendix
        if not app_dir.exists():
            continue
        if write_redirect_stub(app_dir, entries, dry_run):
            print(f"  STUB: {appendix}/index.html")
            n_stubs += 1
            # Remove orphan files (section-*.html should have been git mv'd; images/_section_split_plan remain)
            for orphan in list(app_dir.glob("*")):
                if orphan.name == "index.html":
                    continue
                if orphan.is_dir():
                    if not dry_run:
                        shutil.rmtree(orphan)
                    print(f"    rm -rf {orphan.relative_to(ROOT)}")
                else:
                    if not dry_run:
                        orphan.unlink()
                    print(f"    rm {orphan.relative_to(ROOT)}")

    print()
    print(f"=== Summary ===")
    print(f"Sections moved:    {n_moved}")
    print(f"Redirect stubs:    {n_stubs}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
