"""Fix stale 'Appendix <OLD-letter>' prose references after v15 redesign.

The v15 redesign script renamed directories, section files, and href
attributes, but missed plain-prose references to "Appendix R", "Appendix
AD", etc. These are AMBIGUOUS in isolation: "Appendix R" now correctly
means Master Reference Tables (new letter), but in legacy prose it meant
Experiment Tracking (old letter).

Strategy: rewrite ONLY when the topic name follows the letter, and the
topic matches the OLD assignment.

Old → New letter mapping:
  R  (Experiment Tracking)        -> M
  S  (Inference Serving)          -> N
  T  (Distributed ML)             -> O
  U  (Docker)                     -> P
  V  (Tooling / LLM Tooling)      -> Q
  AD (Master Reference Tables)    -> R
  AE (Production Patterns)        -> S
  AF (Pedagogy Kit)               -> T
  AG (Problem-Solution Key)       -> U
  AI (Freshness)                  -> V
"""
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
SKIP = {"KDP", "node_modules", ".git", "pagefind", "scripts", "styles"}

# (old_letter, topic_substring_match, new_letter)
# topic_substring is case-insensitive partial match in following ~80 chars
RULES = [
    ("R",  ["experiment tracking", "tracking"],            "M"),
    ("S",  ["inference serving", "vllm", "tgi"],            "N"),
    ("T",  ["distributed ml", "distributed training"],      "O"),
    ("U",  ["docker", "container"],                          "P"),
    ("V",  ["tooling", "tooling ecosystem"],                "Q"),
    ("AD", ["master reference", "reference tables"],        "R"),
    ("AE", ["production patterns", "production reliab"],    "S"),
    ("AF", ["pedagogy"],                                     "T"),
    ("AG", ["problem-solution", "problem solution"],         "U"),
    ("AI", ["freshness", "2026"],                            "V"),
]


def fix_text(t: str, log: list) -> str:
    """Return rewritten text. Appends (old_ref, new_ref) tuples to log."""
    out = t
    for old, topics, new in RULES:
        # Match 'Appendix R' followed by space/punct/paren, not 'Reference'
        # We look at 0-80 chars after the match for a topic substring.
        pat = re.compile(rf'\bAppendix {old}\b(?=[\s:.,;)(\[])')
        def repl(m):
            tail = out[m.end():m.end() + 80].lower()
            for kw in topics:
                if kw in tail:
                    log.append((m.group(), f"Appendix {new}"))
                    return f"Appendix {new}"
            return m.group()  # no topic context, leave alone
        out = pat.sub(repl, out)
    return out


def main():
    apply = "--apply" in sys.argv
    total = 0
    files_touched = 0
    for p in ROOT.rglob("*.html"):
        if any(part in SKIP for part in p.parts):
            continue
        s = p.read_text(encoding="utf-8")
        if "Appendix " not in s:
            continue
        soup = BeautifulSoup(s, "html.parser")
        changed = False
        file_log = []
        for el in list(soup.find_all(string=True)):
            if el.parent and el.parent.name in ("a", "code", "pre", "script", "style", "title"):
                continue
            t = str(el)
            new_t = fix_text(t, file_log)
            if new_t != t:
                el.replace_with(NavigableString(new_t))
                changed = True
        if changed:
            total += len(file_log)
            files_touched += 1
            if apply:
                p.write_text(str(soup), encoding="utf-8")
            print(f"  {p.relative_to(ROOT)}: {len(file_log)} fixes")
            for old, new in file_log[:5]:
                print(f"      {old}  ->  {new}")

    print()
    print(f"Total: {total} refs across {files_touched} files {'(APPLIED)' if apply else '(DRY RUN; use --apply)'}")


if __name__ == "__main__":
    main()
