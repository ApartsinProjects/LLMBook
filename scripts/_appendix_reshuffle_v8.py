"""V8 appendix reshuffle: Python -> R&D Infra, Pedagogy Kit split into 5.

Final 21-appendix structure A-U (was 17 A-Q):

  Foundations              A Math, B ML
  Framework Guides         C HF, D LangChain, E Orchestration, F Agents
  R&D Infrastructure       G Python, H Env Setup, I Git/DVC, J Experiments
  Production Infrastructure K Inference, L Distributed, M Docker
  Cross-Cutting References N Master Tables, O Problem-Solution, P Freshness
  For Instructors          Q Syllabi, R Pathways, S Projects,
                           T Capstone, U War Stories

Letter map (old -> new):
  C -> G   Python moves to R&D Infrastructure
  D -> C   HF shifts up (Framework Guides)
  E -> D   LangChain shifts up
  F -> E   Orchestration shifts up
  G -> F   Agent Frameworks shifts up
  Q -> P   Freshness shifts up (fills P slot vacated by Pedagogy split)
  P -> SPLIT into Q, R, S, T, U:
    section-p.6.html (Syllabi)   -> appendix-q-course-syllabi/index.html
    section-p.7.html (Pathways)  -> appendix-r-reading-pathways/index.html
    index.html Part 2 (Projects) -> appendix-s-intermediate-projects/index.html
    index.html Part 1 (Capstone) -> appendix-t-capstone-project/index.html
    index.html Part 3 (Stories)  -> appendix-u-war-stories/index.html
    index.html Part 4 (Pathways) -> dropped (duplicates Part 4 of p.7)

Idempotent. Run once.
"""
from __future__ import annotations
import argparse
import re
import subprocess
import sys
from pathlib import Path

try:
    from bs4 import BeautifulSoup
except ImportError:
    print("ERROR: pip install beautifulsoup4", file=sys.stderr)
    sys.exit(2)

ROOT = Path(__file__).resolve().parents[1]
APPS = ROOT / "appendices"
SKIP_PARTS = {"node_modules", ".git", "KDP", "build", "temp_ebook",
              "temp_epub", "source_fix_backups", "pagefind", "templates",
              ".claude"}

# Standard letter renames (P handled separately via SPLIT)
RENAMES = [
    ("C", "G", "python-for-llm"),
    ("D", "C", "huggingface-ecosystem"),
    ("E", "D", "langchain"),
    ("F", "E", "orchestration-frameworks"),
    ("G", "F", "agent-frameworks"),
    ("Q", "P", "freshness-2026"),
]

# Pedagogy Kit (P) -> 5 new appendices Q, R, S, T, U
# Each tuple: (letter, slug, title, subtitle, source_marker)
# source_marker tells us which Part heading to extract from old index.html,
# or "section-p.X" if content is in an existing section file.
SPLIT_NEW_APPS = [
    ("Q", "course-syllabi", "Course Syllabi",
     "Five tested course tracks (undergrad engineering, undergrad research, "
     "graduate engineering, graduate research, professional bootcamp) with "
     "week-by-week schedules.",
     "section-p.6"),
    ("R", "reading-pathways", "Reading Pathways",
     "Per-audience reading guides for engineers, researchers, "
     "founders/PMs, and self-study learners.",
     "section-p.7"),
    ("S", "intermediate-projects", "Intermediate Projects",
     "Three multi-week projects between the 60-minute chapter labs and "
     "the 6-week capstone.",
     "Part 2: Three Intermediate Projects"),
    ("T", "capstone-project", "Capstone Project",
     "Three-track capstone (full-stack, API-only, research replication) "
     "with a five-dimension grading rubric.",
     "Part 1: Capstone Rubric"),
    ("U", "war-stories", "War Stories for Discussion",
     "Five named production failures (Air Canada, Chevy of Watsonville, "
     "Bing/Sydney, Samsung leak, fintech runaway bill) with discussion "
     "prompts and chapter pairings.",
     "Part 3: Five Named Production War Stories"),
]


def git_mv(src: Path, dst: Path, dry_run: bool) -> str:
    if not src.exists():
        return f"  SKIP: {src.name} missing"
    if dst.exists():
        return f"  SKIP: {dst.name} exists"
    if dry_run:
        return f"  WOULD git mv {src.name} -> {dst.name}"
    dst.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["git", "mv", str(src), str(dst)], cwd=ROOT, check=False)
    return f"  git mv {src.name} -> {dst.name}"


def step1_move_pedagogy_aside(dry_run: bool) -> list[str]:
    """Move appendix-p-pedagogy-kit to _tmp-pedagogy-kit so Q->P can land."""
    msgs: list[str] = []
    src = APPS / "appendix-p-pedagogy-kit"
    dst = APPS / "_tmp-pedagogy-kit"
    msgs.append(git_mv(src, dst, dry_run))
    return msgs


def step2_letter_renames(dry_run: bool) -> list[str]:
    """Standard letter renames via temp prefix swap."""
    msgs: list[str] = []
    for old, new, slug in RENAMES:
        src = APPS / f"appendix-{old.lower()}-{slug}"
        dst = APPS / f"_tmp2-{new.lower()}-{slug}"
        msgs.append(git_mv(src, dst, dry_run))
    for old, new, slug in RENAMES:
        src = APPS / f"_tmp2-{new.lower()}-{slug}"
        dst = APPS / f"appendix-{new.lower()}-{slug}"
        msgs.append(git_mv(src, dst, dry_run))
    if not dry_run:
        for old, new, slug in RENAMES:
            d = APPS / f"appendix-{new.lower()}-{slug}"
            if not d.exists():
                continue
            for sec in sorted(d.glob(f"section-{old.lower()}.*.html")):
                new_name = sec.name.replace(
                    f"section-{old.lower()}.", f"section-{new.lower()}.")
                new_path = sec.parent / new_name
                if new_path == sec or new_path.exists():
                    continue
                subprocess.run(["git", "mv", str(sec), str(new_path)],
                                cwd=ROOT, check=False)
                msgs.append(f"  section {sec.name} -> {new_name}")
    return msgs


def step3_split_pedagogy(dry_run: bool) -> list[str]:
    """Split _tmp-pedagogy-kit into 5 new appendices Q, R, S, T, U."""
    msgs: list[str] = []
    src_dir = APPS / "_tmp-pedagogy-kit"
    if not src_dir.exists():
        return ["  SKIP: _tmp-pedagogy-kit missing"]

    # Read old index.html for inline Part extraction
    old_index = src_dir / "index.html"
    old_html = old_index.read_text(encoding="utf-8") if old_index.exists() else ""

    # Extract inline parts from old index.html
    inline_parts: dict[str, str] = {}
    if old_html:
        inline_parts = _extract_parts_from_index(old_html)

    for letter, slug, title, subtitle, src_marker in SPLIT_NEW_APPS:
        new_dir = APPS / f"appendix-{letter.lower()}-{slug}"
        if dry_run:
            msgs.append(f"  WOULD create {new_dir.name}/")
            msgs.append(f"    title: {title}")
            msgs.append(f"    source: {src_marker}")
            continue

        new_dir.mkdir(exist_ok=True)
        (new_dir / "images").mkdir(exist_ok=True)

        # Determine content for this new appendix
        if src_marker.startswith("section-p."):
            # Move existing section file -> new appendix index.html
            src_file = src_dir / f"{src_marker}.html"
            if not src_file.exists():
                msgs.append(f"  SKIP: {src_marker}.html missing")
                continue
            content_html = src_file.read_text(encoding="utf-8")
            new_html = _convert_section_to_appendix_index(
                content_html, letter, title, subtitle)
            (new_dir / "index.html").write_text(new_html, encoding="utf-8")
            # Stage the removal of the old section file
            subprocess.run(["git", "rm", "-f", str(src_file)],
                            cwd=ROOT, check=False)
            msgs.append(f"  created appendix-{letter.lower()}-{slug}/index.html"
                         f" from {src_marker}.html")
        else:
            # Extract from inline old index.html
            body_html = inline_parts.get(src_marker, "")
            if not body_html:
                msgs.append(f"  WARNING: inline part '{src_marker}' not found")
                body_html = (f"<p><em>TODO: migrate content from old "
                              f"Pedagogy Kit index Part: {src_marker}</em></p>")
            new_html = _wrap_as_appendix_index(letter, slug, title, subtitle,
                                                 body_html)
            (new_dir / "index.html").write_text(new_html, encoding="utf-8")
            msgs.append(f"  created appendix-{letter.lower()}-{slug}/index.html"
                         f" from inline '{src_marker}'")

    # Stage the deletion of the old index.html + pedagogy dir
    if not dry_run:
        if old_index.exists():
            subprocess.run(["git", "rm", "-f", str(old_index)],
                            cwd=ROOT, check=False)
            msgs.append("  removed _tmp-pedagogy-kit/index.html")
        # Move any leftover files (e.g. images/) somewhere safe -- otherwise
        # just remove the dir
        try:
            for leftover in list(src_dir.iterdir()):
                if leftover.is_dir() and leftover.name == "images":
                    # Skip empty dirs
                    if not any(leftover.iterdir()):
                        leftover.rmdir()
                        continue
                # Otherwise leave for manual review
                msgs.append(f"  LEFTOVER: {leftover.name}")
            if not any(src_dir.iterdir()):
                src_dir.rmdir()
                msgs.append("  Removed empty _tmp-pedagogy-kit/")
        except OSError as e:
            msgs.append(f"  WARNING: could not remove _tmp-pedagogy-kit: {e}")
    return msgs


def _extract_parts_from_index(html: str) -> dict[str, str]:
    """Find the 'Part 1: ...', 'Part 2: ...', 'Part 3: ...' h2 blocks in old
    Pedagogy Kit index.html and return them as {part_marker: inner_html}.

    Each Part is bounded by the next h2 (Part) heading or an <hr/> tag.
    """
    soup = BeautifulSoup(html, "html.parser")
    main = soup.find("main") or soup
    out: dict[str, str] = {}
    h2s = main.find_all("h2")
    for h2 in h2s:
        title = h2.get_text(strip=True)
        if not title.startswith("Part "):
            continue
        # Collect sibling content until next h2 or <hr/>
        chunks: list[str] = [str(h2)]
        for sib in h2.find_next_siblings():
            if sib.name == "h2" and sib.get_text(strip=True).startswith("Part "):
                break
            if sib.name == "hr":
                break
            chunks.append(str(sib))
        out[title] = "\n".join(chunks)
    return out


def _convert_section_to_appendix_index(html: str, letter: str, title: str,
                                          subtitle: str) -> str:
    """Take an old section-p.X.html (a section page) and rewrite its header
    metadata so it works as an appendix index.html.

    Changes:
      <title>Section P.X: Title | ...</title>  -> <title>Appendix L: Title | ...</title>
      breadcrumb 'Appendices > Appendix P: ...' -> 'Appendices > Appendix L'
      <h1>Title</h1><div class="page-current">Section P.X</div> -> just <h1>
      Path prefixes: ../../  in section files becomes the same in the new
      appendix index (both are at appendices/appendix-*/<file>.html level)
    """
    soup = BeautifulSoup(html, "html.parser")

    # 1. <title>
    if soup.title:
        soup.title.string = (
            f"Appendix {letter}: {title} | "
            f"Building Conversational AI with LLMs and Agents"
        )

    # 2. <meta name="description">
    desc = soup.find("meta", attrs={"name": "description"})
    if desc:
        desc["content"] = f"Appendix {letter}: {title}. {subtitle}"

    # 3. breadcrumb
    bc = soup.find("div", class_="page-breadcrumb")
    if bc:
        bc.clear()
        a1 = soup.new_tag("a", href="../index.html")
        a1.string = "Appendices"
        bc.append(a1)
        sep = soup.new_tag("span")
        sep["class"] = "bc-sep"
        sep.string = "›"
        bc.append(sep)
        cur = soup.new_tag("span")
        cur["class"] = "bc-current"
        cur.string = f"Appendix {letter}"
        bc.append(cur)

    # 4. <h1> + remove the "Section P.X" subtitle div
    h1 = soup.find("h1")
    if h1:
        h1.string = title
        # Look for the page-current div right after h1 and remove it
        nxt = h1.find_next_sibling()
        if nxt and nxt.name == "div" and "page-current" in (nxt.get("class") or []):
            nxt.decompose()

    # 5. pagefind meta -> change chapter to "Appendix L: Title"
    for pm in soup.find_all("span", class_="pagefind-meta-injected"):
        m = pm.get("data-pagefind-meta", "")
        if m.startswith("chapter:"):
            pm["data-pagefind-meta"] = f"chapter:Appendix {letter}: {title}"

    # 6. Remove any chapter-nav prev/next from the bottom (old section nav)
    nav = soup.find("nav", class_="chapter-nav")
    if nav:
        nav.decompose()

    return str(soup)


def _wrap_as_appendix_index(letter: str, slug: str, title: str,
                              subtitle: str, body_html: str) -> str:
    """Wrap inline-extracted Pedagogy Kit body content as a new appendix
    index.html with proper header, breadcrumb, h1, etc."""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<meta content="Appendix {letter}: {title}. {subtitle}" name="description"/>
<title>Appendix {letter}: {title} | Building Conversational AI with LLMs and Agents</title>
<link href="../../styles/book.css" rel="stylesheet"/>
<link href="../../pagefind/pagefind-ui.css" rel="stylesheet"/>
<script defer="" src="../../pagefind/pagefind-ui.js"></script>
<script defer="" src="../../scripts/book.js"></script>
</head>
<body>
<header class="chapter-header">
<nav class="header-nav">
<a class="book-title-link" href="../../index.html">Building Conversational AI with LLMs and Agents</a>
<a class="toc-link" href="../../toc.html" title="Table of Contents"><span class="toc-icon">☰</span> Contents</a>
</nav>
<div class="header-search"><div id="search"></div></div>
<div class="page-breadcrumb" data-pagefind-meta="chapter"><a href="../index.html">Appendices</a><span class="bc-sep">›</span><span class="bc-current">Appendix {letter}</span></div>
<h1>Appendix {letter}: {title}</h1>
<p class="chapter-subtitle">{subtitle}</p>
</header>
<main class="content"><span class="pagefind-meta-injected" data-pagefind-meta="part:Appendices" hidden=""></span><span class="pagefind-meta-injected" data-pagefind-meta="chapter:Appendix {letter}: {title}" hidden=""></span>
{body_html}
</main>
<footer><p>Fifteenth Edition, 2026 &middot; <a href="../../toc.html">Contents</a></p></footer>
</body>
</html>
"""


def step4_book_wide_rewrite(dry_run: bool) -> int:
    """Rewrite cross-refs book-wide. Two passes to avoid double-substitution:
    1. Mark old letters with §X§ tokens
    2. Replace tokens with new letters

    Also handle Pedagogy Kit special cases (P -> Q/R/S/T/U).
    """
    # Standard letter renames (excluding P-pedagogy, handled separately)
    forward = {old: new for old, new, _ in RENAMES}

    # Pedagogy Kit special mappings (URL-level)
    pedagogy_url_map = [
        # Specific section files map directly to their new appendices
        ("appendix-p-pedagogy-kit/section-p.6.html",
         "appendix-q-course-syllabi/index.html"),
        ("appendix-p-pedagogy-kit/section-p.7.html",
         "appendix-r-reading-pathways/index.html"),
        # Generic links default to Q (Syllabi) -- the most likely intent
        ("appendix-p-pedagogy-kit/index.html",
         "appendix-q-course-syllabi/index.html"),
        ("appendix-p-pedagogy-kit/",
         "appendix-q-course-syllabi/"),
    ]

    n_files = 0
    for p in sorted(ROOT.rglob("*.html")):
        if set(p.parts) & SKIP_PARTS:
            continue
        text = p.read_text(encoding="utf-8")
        orig = text

        # --- Pedagogy Kit URL rewrites (do first, before letter renames
        # touch 'p' patterns) ---
        for old_url, new_url in pedagogy_url_map:
            text = text.replace(old_url, new_url)

        # --- Standard letter renames via § tokens ---
        for old in forward:
            text = re.sub(rf"\bAppendix\s+{old}\b",
                           f"Appendix §{old}§", text)
            for kind in ("Code Fragment", "Figure", "Table", "Pseudocode",
                          "Listing"):
                text = re.sub(rf"\b{kind}\s+{old}\.(\d+(?:\.\d+)?)\b",
                               rf"{kind} §{old}§.\1", text)
            text = re.sub(rf"\bSection\s+{old}\.(\d+(?:\.\d+)?)\b",
                           rf"Section §{old}§.\1", text)
            text = re.sub(rf"appendix-{old.lower()}-",
                           f"appendix-§{old}§-", text)
            text = re.sub(rf"section-{old.lower()}\.(\d+(?:\.\d+)?)\.html",
                           rf"section-§{old}§.\1.html", text)
            text = re.sub(rf"section-{old.lower()}\.(\d+(?:\.\d+)?)#",
                           rf"section-§{old}§.\1#", text)
        for old, new in forward.items():
            text = text.replace(f"§{old}§", new)
        # Normalize: lowercase the letter in slugs and section file names
        for old, new in forward.items():
            text = text.replace(f"appendix-{new}-", f"appendix-{new.lower()}-")
            text = text.replace(f"section-{new}.", f"section-{new.lower()}.")

        # --- Pedagogy Kit text references (P -> distributed) ---
        # "Appendix P" (Pedagogy Kit) default -> "Appendix Q" (Syllabi)
        # But ONLY if not already remapped via P->Q from above (it isn't,
        # because P is in RENAMES). Actually wait: Q -> P is in RENAMES, so
        # at this point §Q§ has been replaced with P. So leftover "Appendix
        # P" references must mean Pedagogy Kit. Default to Q (Syllabi).
        # Skip this -- the URL rewrites above handle the actual links,
        # and the user can manually re-target prose mentions if needed.
        # (Aggressive auto-rewriting would mis-target chapters mentioning
        # the new Freshness Q/P switch.)

        if text != orig:
            n_files += 1
            if not dry_run:
                p.write_text(text, encoding="utf-8")
    return n_files


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    dry_run = not args.apply
    mode = "DRY-RUN" if dry_run else "APPLY"

    print(f"=== {mode}: Step 1 - Move Pedagogy Kit aside ===")
    for m in step1_move_pedagogy_aside(dry_run):
        print(m)

    print(f"\n=== {mode}: Step 2 - Letter renames (C->G, D-G shift, Q->P) ===")
    for m in step2_letter_renames(dry_run):
        print(m)

    print(f"\n=== {mode}: Step 3 - Split Pedagogy Kit into Q/R/S/T/U ===")
    for m in step3_split_pedagogy(dry_run):
        print(m)

    print(f"\n=== {mode}: Step 4 - Book-wide cross-ref rewrite ===")
    n = step4_book_wide_rewrite(dry_run)
    print(f"  {n} files updated")
    return 0


if __name__ == "__main__":
    sys.exit(main())
