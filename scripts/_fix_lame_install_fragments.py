"""Drop all lame install-only Code Fragments and renumber subsequent
fragments in each affected section. Auto-discovers offenders by:

  Predicate: a <div class="code-caption"> whose
    (a) text matches "Code Fragment N.N.N:" or "Code Fragment N.NLM:", AND
    (b) one of:
        - the nearby <pre> body is a one-line `pip|npm|conda|apt|brew|curl|wget X` command, OR
        - the caption body text starts with "Install " (catches mislabel
          cases where the wrapper was already removed)

The script removes the .code-block-wrapper + the caption, then decrements
later N.N.X captions in the same section by 1 to keep numbering consecutive.

For non-standard caption ids like "N.NLM" we drop without renumbering
(those are typically Lab snippets and the lettered M suffix doesn't fit
into the regular numeric sequence).

Idempotent.
"""
from __future__ import annotations
import argparse
import re
import sys
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
SKIP_PARTS = {"node_modules", ".git", "KDP", "build", "temp_ebook",
              "temp_epub", "source_fix_backups", "pagefind", "templates",
              ".claude"}

CAPTION_NUM_RE = re.compile(
    r"Code Fragment\s+([A-Za-z]?[\d.]+(?:L\d+)?)\s*:?\s*", re.I
)
INSTALL_CMD_RE = re.compile(r"^(pip|npm|conda|apt|brew|curl|wget)\s+\S")


def _find_adjacent_wrapper(cap):
    """Return the <div class='code-block-wrapper'> containing or preceding
    this caption, or None."""
    parent = cap.parent
    if (parent is not None and getattr(parent, "name", None) == "div"
            and "code-block-wrapper" in (parent.get("class") or [])):
        return parent
    sib = cap.previous_sibling
    while sib is not None:
        name = getattr(sib, "name", None)
        if name == "div" and "code-block-wrapper" in (sib.get("class") or []):
            return sib
        if name and name not in ("br",):
            return None
        sib = sib.previous_sibling
    return None


def _is_lame_install_caption(cap) -> bool:
    """Return True if the caption labels a lame install fragment."""
    full = cap.get_text(" ", strip=True)
    body = CAPTION_NUM_RE.sub("", full, count=1).strip()

    # (a) associated <pre> body is a one-liner install command
    wrapper = _find_adjacent_wrapper(cap)
    if wrapper is not None:
        pre = wrapper.find("pre")
        if pre is not None:
            pre_text = pre.get_text(" ", strip=True)
            # One-liner = no newlines once normalized
            if "\n" not in pre.get_text() and INSTALL_CMD_RE.match(pre_text):
                return True

    # (b) caption body text starts with "Install <pkg>"
    if body.lower().startswith("install "):
        return True
    return False


def _renumber_section(text: str, sec_prefix: str, dropped_n: int) -> str:
    """Decrement Code Fragment numbers higher than dropped_n in section
    sec_prefix (e.g. "6.4."). Returns updated HTML."""
    pat = re.compile(rf"Code Fragment\s+{re.escape(sec_prefix)}(\d+)\b")

    def repl(m):
        n = int(m.group(1))
        if n > dropped_n:
            return f"Code Fragment {sec_prefix}{n - 1}"
        return m.group(0)

    return pat.sub(repl, text)


def process_file(p: Path, dry_run: bool) -> tuple[int, list[str]]:
    """Drop all lame install fragments in this file. Returns
    (n_dropped, list_of_messages)."""
    text = p.read_text(encoding="utf-8")
    messages: list[str] = []
    n = 0
    # Iterate; each drop modifies the HTML so reparse after each.
    while True:
        soup = BeautifulSoup(text, "html.parser")
        target = None
        target_num = None
        for cap in soup.find_all("div", class_="code-caption"):
            m = CAPTION_NUM_RE.search(cap.get_text(" ", strip=True))
            if not m:
                continue
            if _is_lame_install_caption(cap):
                target = cap
                target_num = m.group(1)
                break
        if target is None:
            break

        # Decide whether we'll renumber: only if id is N.N.N (all digits)
        parts = target_num.split(".")
        renumber_ok = (
            len(parts) >= 3
            and all(part.isdigit() for part in parts[:3])
        )

        wrapper = _find_adjacent_wrapper(target)
        removed = "caption only"
        if wrapper is not None:
            pre = wrapper.find("pre")
            if pre is not None:
                body_text = pre.get_text(" ", strip=True)
                if INSTALL_CMD_RE.match(body_text):
                    wrapper.decompose()
                    removed = "caption + wrapper"

        if target.parent is not None:
            target.decompose()

        new_html = str(soup)
        if renumber_ok:
            sec_prefix = f"{parts[0]}.{parts[1]}."
            dropped_n = int(parts[2])
            new_html = _renumber_section(new_html, sec_prefix, dropped_n)
            messages.append(f"  dropped Code Fragment {target_num} ({removed}); renumbered later {sec_prefix}X")
        else:
            messages.append(f"  dropped Code Fragment {target_num} ({removed}); no renumber")
        text = new_html
        n += 1

    if n and not dry_run:
        p.write_text(text, encoding="utf-8")
    return n, messages


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    total = 0
    files_touched = 0
    for p in sorted(ROOT.rglob("*.html")):
        if set(p.parts) & SKIP_PARTS:
            continue
        n, messages = process_file(p, args.dry_run)
        if n:
            files_touched += 1
            total += n
            print(f"{p.relative_to(ROOT)}:")
            for m in messages:
                print(m)
    print(f"\nTOTAL: {total} lame fragments dropped across {files_touched} files")
    if args.dry_run:
        print("(dry run; nothing written)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
