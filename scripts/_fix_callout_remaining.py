"""Auto-fix the three mechanical callout-format issues remaining after the
bare-OL self-check sweep:

  (A) 28 self-checks have <details> blocks lacking the canonical
      <div class="answer"> wrapper. The answer text sits as a bare
      NavigableString inside <details>. Wrap it.

  (B) 19 exercise callouts titled just "Exercise" / "Exercises" /
      "Hands-On Lab" without the canonical "Exercise N.M.P:" sequence
      number. Insert the section number from the file path + a
      running per-section index.

  (C) 8 library-shortcut callouts titled "Appendix Reference" should
      really be cross-ref class. Swap the class.

Run from project root:
    python scripts/_fix_callout_remaining.py [--dry-run]
"""
from __future__ import annotations
import argparse
import re
import sys
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString

ROOT = Path(__file__).resolve().parents[1]
SKIP_PARTS = {"node_modules", ".git", "KDP", "build", "temp_ebook",
              "temp_epub", "source_fix_backups", "pagefind", "templates",
              ".claude"}


def should_skip(p: Path) -> bool:
    return bool(set(p.parts) & SKIP_PARTS)


# ----------------------------------------------------------------------
# Helper: parse section number from a file path. Returns "N.M.P" or None.
#   part-9-safety-strategy/module-30-X/section-30.4.html -> "30.4"
#   appendices/appendix-h-prompt-templates/section-h.3.html -> "H.3"
#   appendices/appendix-h-.../index.html -> "H"
# ----------------------------------------------------------------------
def section_id_from_path(p: Path) -> str | None:
    name = p.name
    m = re.match(r'^section-([0-9a-z]+(?:\.[0-9a-z]+)*)\.html$', name)
    if m:
        return m.group(1).upper()
    # chapter index pages
    if name == "index.html":
        # find module-NN-* in parents
        for part in p.parts[::-1]:
            mm = re.match(r'^module-(\d+)-', part)
            if mm:
                return mm.group(1).lstrip("0") or "0"
            mm = re.match(r'^appendix-([a-z])-', part)
            if mm:
                return mm.group(1).upper()
    return None


def fix_A_answer_wrapper(soup: BeautifulSoup) -> int:
    """Wrap bare text inside <details> in <div class="answer">.

    Pattern before: <details><summary>Show Answer</summary>The answer text...</details>
    Pattern after:  <details><summary>Show Answer</summary><div class="answer">The answer text...</div></details>
    Only applies inside .callout.self-check to avoid touching unrelated <details>.
    """
    n = 0
    for callout in soup.select(".callout.self-check"):
        for det in callout.find_all("details"):
            # If a .answer div is already present, skip
            if det.find("div", class_="answer"):
                continue
            summary = det.find("summary")
            if not summary:
                continue
            # Collect everything AFTER <summary> that isn't a <div.answer>
            answer_content = []
            for sib in list(summary.next_siblings):
                if (hasattr(sib, "name") and sib.name == "div" and
                        "answer" in (sib.get("class") or [])):
                    answer_content = []  # already wrapped, abort
                    break
                answer_content.append(sib)
            if not answer_content:
                continue
            # Wrap them in a new div.answer
            new_div = soup.new_tag("div")
            new_div["class"] = ["answer"]
            for c in answer_content:
                c.extract()
                new_div.append(c)
            det.append(new_div)
            n += 1
    return n


# Generic exercise titles to rewrite (case-insensitive exact match after strip)
GENERIC_EXERCISE_TITLES = {
    "exercise", "exercises", "hands-on lab", "lab", "practice",
    "practice exercise", "practice exercises", "try it yourself",
    "try this", "your turn",
}


def fix_B_exercise_seq_numbers(soup: BeautifulSoup, p: Path, idx_counter: dict) -> int:
    """Inject 'Exercise N.M.P:' prefix into exercise callout titles that
    only have a generic title. The N.M.P comes from the file's section id
    plus a running per-file counter for the exercise index."""
    section_id = section_id_from_path(p)
    if not section_id:
        return 0
    n = 0
    for callout in soup.select(".callout.exercise"):
        title_div = callout.find("div", class_="callout-title")
        if not title_div:
            continue
        # Don't touch titles that already have a number (e.g. "Exercise 12.1.3:")
        title_text = title_div.get_text(strip=True)
        if re.match(r'^Exercise\s+[\d.]+:', title_text):
            continue
        # Only retitle generic forms
        if title_text.lower().strip().rstrip(":") not in GENERIC_EXERCISE_TITLES:
            continue
        # Increment per-file exercise counter
        idx_counter[str(p)] = idx_counter.get(str(p), 0) + 1
        seq = f"{section_id}.{idx_counter[str(p)]}"
        # Preserve any inline children, just prefix the leading text
        new_text = f"Exercise {seq}: "
        # Wipe existing text content, keep child <span class="exercise-type">
        for c in list(title_div.contents):
            if isinstance(c, NavigableString):
                c.extract()
        # Insert new text at the start
        title_div.insert(0, NavigableString(new_text))
        # If the OLD title was something like "Hands-On Lab" (semantic), keep
        # it as a parenthetical to preserve intent
        if title_text.lower() not in ("exercise", "exercises"):
            title_div.append(NavigableString(f" ({title_text})"))
        n += 1
    return n


def fix_C_library_to_crossref(soup: BeautifulSoup) -> int:
    """Re-class library-shortcut callouts titled 'Appendix Reference' to cross-ref."""
    n = 0
    for callout in soup.select(".callout.library-shortcut"):
        title_div = callout.find("div", class_="callout-title")
        if not title_div:
            continue
        title_text = title_div.get_text(strip=True).rstrip(":").lower()
        if title_text in ("appendix reference", "appendix references", "see also"):
            # Swap class
            classes = callout.get("class") or []
            classes = [c for c in classes if c != "library-shortcut"]
            classes.append("cross-ref")
            callout["class"] = classes
            # Normalize title to "Canonical reference" (the canonical cross-ref title)
            title_div.clear()
            title_div.append(NavigableString("Canonical reference"))
            n += 1
    return n


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    total_A = total_B = total_C = 0
    files_touched = 0
    idx_counter: dict = {}

    for p in ROOT.rglob("*.html"):
        if should_skip(p):
            continue
        try:
            text = p.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        soup = BeautifulSoup(text, "html.parser")
        nA = fix_A_answer_wrapper(soup)
        nB = fix_B_exercise_seq_numbers(soup, p, idx_counter)
        nC = fix_C_library_to_crossref(soup)
        if nA + nB + nC == 0:
            continue
        rel = p.relative_to(ROOT)
        bits = []
        if nA: bits.append(f"A={nA}")
        if nB: bits.append(f"B={nB}")
        if nC: bits.append(f"C={nC}")
        print(f"  {rel}: {' '.join(bits)}")
        total_A += nA
        total_B += nB
        total_C += nC
        files_touched += 1
        if not args.dry_run:
            p.write_text(str(soup), encoding="utf-8")

    print()
    print(f"TOTAL: A={total_A} answer wrappers + B={total_B} exercise seq numbers + "
          f"C={total_C} class swaps  across {files_touched} files")
    if args.dry_run:
        print("(dry run; nothing written)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
