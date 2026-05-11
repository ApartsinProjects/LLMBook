"""v3.6: Execute R3#4 Option A (mechanical merge of Module 32 + move to 17).

Three operations:
  1. Append 32.10 (Cross-Cultural NLP) into 32.3 (Bias/Fairness) as a new H2
     'Cross-Cultural NLP and Pluralistic Alignment'.
  2. Append 32.13 (Federated Learning) into 32.12 (Privacy/DP) as a new H2
     'Federated Learning for Privacy-Preserving Training'.
  3. Move 32.14 (Alignment Frontiers) into Module 17 as section-17.5.

After this:
  Module 32: 15 -> 12 sections.
  Module 17: 4 -> 5 sections.

Each merge wraps the absorbed content in a `<section class="merged-section">`
boundary so a future editorial pass can find seams to smooth. Inbound
cross-references redirected to the new home.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
EXCLUDE = {"_archive", "KDP", "node_modules", "vendor", "scripts"}


def extract_main_content(text: str) -> str:
    """Pull the main content body (between <main> tags) minus chrome/nav."""
    m = re.search(r"<main[^>]*>(.*?)</main>", text, re.DOTALL)
    if m:
        return m.group(1).strip()
    # Fallback to body
    m = re.search(r"<body[^>]*>(.*?)</body>", text, re.DOTALL)
    return m.group(1).strip() if m else text


def strip_h1_block(text: str) -> str:
    """Remove the first <h1>...</h1> from the merged content (replaced by H2)."""
    return re.sub(r"<h1[^>]*>.*?</h1>", "", text, count=1, flags=re.DOTALL)


def strip_chapter_header(text: str) -> str:
    """Remove any leading chapter-header / breadcrumb chrome."""
    text = re.sub(r"<header\s+class=\"chapter-header\"[^>]*>.*?</header>",
                  "", text, count=1, flags=re.DOTALL)
    text = re.sub(r"<div\s+class=\"part-label\"[^>]*>.*?</div>",
                  "", text, count=1, flags=re.DOTALL)
    return text


def strip_bib_and_nav(text: str) -> str:
    """Remove inherited bibliography + 'what comes next' from the merged content."""
    text = re.sub(r"<details[^>]*class=\"bibliography-collapsible\".*?</details>",
                  "", text, flags=re.DOTALL)
    text = re.sub(r"<section[^>]*class=\"bibliography\".*?</section>",
                  "", text, flags=re.DOTALL)
    text = re.sub(r"<aside[^>]*class=\"whats-next\".*?</aside>",
                  "", text, flags=re.DOTALL)
    text = re.sub(r"<nav[^>]*class=\"chapter-nav\".*?</nav>",
                  "", text, flags=re.DOTALL)
    return text


def merge_section(src_path: Path, dst_path: Path, new_h2_title: str) -> None:
    """Append src_path's content into dst_path as a new H2 block, then delete src."""
    if not src_path.exists():
        print(f"  [skip] {src_path.name} already merged or missing")
        return
    src_text = src_path.read_text(encoding="utf-8", errors="replace")
    dst_text = dst_path.read_text(encoding="utf-8", errors="replace")

    src_body = extract_main_content(src_text)
    src_body = strip_h1_block(src_body)
    src_body = strip_chapter_header(src_body)
    src_body = strip_bib_and_nav(src_body)

    src_words = len(re.sub(r"<[^>]+>", " ", src_body).split())

    # Build merged block: a horizontal rule + new H2 + body
    src_basename = src_path.stem
    merged_block = (
        '\n\n<hr class="merged-section-divider"/>\n'
        f'<section class="merged-section" data-merged-from="{src_basename}">\n'
        f'<h2>{new_h2_title}</h2>\n'
        + src_body.strip()
        + '\n</section>\n'
    )

    # Insert before </main> in dst (use string-replace to avoid regex backref issues)
    if "</main>" in dst_text:
        idx = dst_text.find("</main>")
        dst_text_new = dst_text[:idx] + merged_block + dst_text[idx:]
    elif "</body>" in dst_text:
        idx = dst_text.find("</body>")
        dst_text_new = dst_text[:idx] + merged_block + dst_text[idx:]
    else:
        dst_text_new = dst_text + merged_block

    dst_path.write_text(dst_text_new, encoding="utf-8")
    src_path.unlink()
    print(f"  merged {src_path.name} -> {dst_path.name}  ({src_words} words appended)")


def move_section(src_path: Path, dst_path: Path, old_num: str, new_num: str) -> None:
    """Move whole section file to a different module + renumber H1/title etc."""
    import os
    import shutil
    text = src_path.read_text(encoding="utf-8", errors="replace")
    # Re-root relative paths
    src_parent = src_path.parent
    dst_parent = dst_path.parent

    def _rewrite(match: re.Match) -> str:
        attr = match.group(1)
        url = match.group(2)
        if url.startswith(("http://", "https://", "mailto:", "javascript:", "#", "data:")):
            return match.group(0)
        try:
            anchor = ""
            if "#" in url:
                url_clean, anchor = url.split("#", 1)
                anchor = "#" + anchor
            else:
                url_clean = url
            if not url_clean:
                return match.group(0)
            target = (src_parent / url_clean).resolve()
            new_rel = os.path.relpath(str(target), str(dst_parent.resolve())).replace("\\", "/")
            return f'{attr}="{new_rel}{anchor}"'
        except Exception:
            return match.group(0)

    text = re.sub(r'(href|src)="([^"]+)"', _rewrite, text)
    # Renumber labels
    text = re.sub(rf'>{re.escape(old_num)}(\s+|&nbsp;)', f'>{new_num}\\1', text)
    text = re.sub(rf'\bSection {re.escape(old_num)}\b', f'Section {new_num}', text)
    text = re.sub(rf'(?<![\d.]){re.escape(old_num)}(?![\d.])', new_num, text)

    dst_path.write_text(text, encoding="utf-8")
    src_path.unlink()
    print(f"  mv  {src_path.name} -> {dst_path.relative_to(ROOT).as_posix()}")


def update_inbound_refs(redirects: list[tuple[str, str]]) -> int:
    """Rewrite href and 'Section X.Y' mentions across the book.

    redirects: list of (old_basename, new_basename_or_path).
    """
    n_files = 0
    for p in ROOT.rglob("*.html"):
        if any(part in p.parts for part in EXCLUDE):
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        original = text
        for old, new in redirects:
            text = re.sub(rf'\b{re.escape(old)}\.html', f'{new}.html', text)
        if text != original:
            p.write_text(text, encoding="utf-8")
            n_files += 1
    return n_files


def main() -> int:
    base = ROOT / "part-9-safety-strategy/module-32-safety-ethics-regulation"

    # Operation 1: 32.10 -> 32.3
    print("\n=== Op 1: 32.10 (Cross-Cultural NLP) -> 32.3 (Bias/Fairness) ===")
    merge_section(
        src_path=base / "section-32.10.html",
        dst_path=base / "section-32.3.html",
        new_h2_title="32.3.X Cross-Cultural NLP and Pluralistic Alignment",
    )

    # Operation 2: 32.13 -> 32.12
    print("\n=== Op 2: 32.13 (Federated Learning) -> 32.12 (Privacy/DP) ===")
    merge_section(
        src_path=base / "section-32.13.html",
        dst_path=base / "section-32.12.html",
        new_h2_title="32.12.X Federated Learning for Privacy-Preserving Training",
    )

    # Operation 3: 32.14 -> Module 17 as 17.5
    print("\n=== Op 3: 32.14 (Alignment Frontiers) -> Module 17 as 17.5 ===")
    src_14 = base / "section-32.14.html"
    dst_17_5 = ROOT / "part-4-training-adapting/module-17-alignment-rlhf-dpo/section-17.5.html"
    if src_14.exists() and not dst_17_5.exists():
        move_section(src_14, dst_17_5, old_num="32.14", new_num="17.5")
    else:
        print(f"  [skip] src exists={src_14.exists()}, dst exists={dst_17_5.exists()}")

    # Update inbound refs
    print("\n=== Updating inbound cross-references ===")
    redirects = [
        ("section-32.10", "section-32.3"),
        ("section-32.13", "section-32.12"),
        ("section-32.14", "section-17.5"),
    ]
    n = update_inbound_refs(redirects)
    print(f"  Updated {n} files with inbound href rewrites")

    # Renumber 32.15 -> 32.10 (close the gap from deleted 32.10/13/14, keep numbering tight)
    print("\n=== Renumbering 32.15 -> 32.13 (close gaps) ===")
    src_15 = base / "section-32.15.html"
    dst_13 = base / "section-32.13.html"
    if src_15.exists() and not dst_13.exists():
        text = src_15.read_text(encoding="utf-8", errors="replace")
        text = re.sub(r'>32\.15(\s+|&nbsp;)', r'>32.13\1', text)
        text = re.sub(r'\bSection 32\.15\b', 'Section 32.13', text)
        dst_13.write_text(text, encoding="utf-8")
        src_15.unlink()
        print("  mv section-32.15.html -> section-32.13.html (renumber)")
        # Update inbound
        n = update_inbound_refs([("section-32.15", "section-32.13")])
        print(f"  Updated {n} files for 32.15->32.13 renumber")
    return 0


if __name__ == "__main__":
    sys.exit(main())
