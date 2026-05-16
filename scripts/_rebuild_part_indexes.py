"""Rebuild the chapter-card block on every part-N/index.html using the
canonical Part-12 template, fed from book_structure.yaml + filesystem.

The template (Part-12-frontiers style):

  <div class="chapter-card">
    <div class="chapter-card-header">
      <span class="mod-num">Chapter N</span> Chapter Title
    </div>
    <div class="chapter-card-body">
      <p>Optional one-paragraph description (from chapter subtitle).</p>
      <ul class="section-list">
        <li>
          <a href="module-NN-slug/section-NN.M.html">
            <span class="sec-num">NN.M</span> Section Title
          </a>
        </li>
        ...
      </ul>
    </div>
  </div>

Preserves the rest of the part-index (header, part-label, h1 part-title,
chapter-subtitle, callout big-picture, part-overview prose, what's-next,
chapter-nav, footer) unchanged. Only replaces the block of contiguous
chapter-card divs.

Idempotent. Run with --apply.
"""
from __future__ import annotations
import argparse
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: pip install pyyaml", file=sys.stderr)
    sys.exit(2)

ROOT = Path(__file__).resolve().parents[1]


def _esc(s: str) -> str:
    return (s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _read_h1(p: Path) -> str | None:
    if not p.exists():
        return None
    text = p.read_text(encoding="utf-8")
    m = re.search(r"<h1[^>]*>([^<]+)</h1>", text)
    return m.group(1).strip() if m else None


def build_chapter_cards(part: dict, part_slug: str, part_num: int) -> str:
    """Build the chapter-card HTML block for a part."""
    lines: list[str] = []
    for chap in part.get("chapters", []):
        cnum = chap["num"]
        cslug = chap["slug"]
        ctitle = _esc(chap.get("title", f"Chapter {cnum}"))
        csubtitle = _esc(chap.get("subtitle", "") or "")
        chap_dir = ROOT / f"part-{part_num}-{part_slug}" / f"module-{cnum:02d}-{cslug}"

        # Build section list from filesystem (yaml + disk; prefer disk for completeness)
        # Find section-N.M.html files; sort by numeric M
        sec_files = []
        if chap_dir.exists():
            for sf in chap_dir.glob(f"section-{cnum}.*.html"):
                m = re.search(rf"section-{cnum}\.(\d+)\.html$", sf.name)
                if m:
                    sec_files.append((int(m.group(1)), sf))
        sec_files.sort(key=lambda t: t[0])

        # Build section <li> rows
        sec_lines: list[str] = []
        for sec_n, sec_path in sec_files:
            h1 = _read_h1(sec_path) or f"Section {cnum}.{sec_n}"
            href = f"module-{cnum:02d}-{cslug}/section-{cnum}.{sec_n}.html"
            sec_lines.append(
                f'<li><a href="{href}"><span class="sec-num">{cnum}.{sec_n}</span> {_esc(h1)}</a></li>'
            )

        # Chapter card
        lines.append('<div class="chapter-card">')
        lines.append('<div class="chapter-card-header">')
        lines.append(f'<span class="mod-num">Chapter {cnum}</span> {ctitle}')
        lines.append('</div>')
        lines.append('<div class="chapter-card-body">')
        if csubtitle:
            lines.append(f'<p>{csubtitle}</p>')
        if sec_lines:
            lines.append('<ul class="section-list">')
            lines.extend(sec_lines)
            lines.append('</ul>')
        else:
            lines.append('<p><em>Sections in authoring; chapter index page has the current section list.</em></p>')
        lines.append('</div>')
        lines.append('</div>')
    return "\n".join(lines)


def replace_chapter_card_block(text: str, new_block: str) -> tuple[str, bool]:
    """Replace the contiguous chapter-card block in the part-index HTML
    with the new markup. Returns (new_text, changed)."""
    # Find the first <div class="chapter-card"> and the last </div> of
    # the contiguous run. We treat the run as a sequence of <div class=
    # "chapter-card">...</div></div> blocks separated only by whitespace.
    first = re.search(r'<div class="chapter-card">', text)
    if not first:
        return text, False
    start = first.start()
    # Find the end: scan for the LAST </div> that closes a chapter-card
    # before the next non-chapter-card content. The simplest heuristic:
    # walk forward, balancing <div>...</div> within the chapter-card,
    # and detect end of run when a non-whitespace, non-chapter-card
    # block appears.
    # Pragmatic approach: find every </div>\s*</div> followed by
    # <div class="chapter-card"> OR by a non-chapter-card tag.
    # We collect the maximum end position where the next element is NOT
    # another chapter-card.
    pos = start
    end = pos
    while True:
        # Find next chapter-card opening after pos
        m = re.search(r'<div class="chapter-card">', text[pos:])
        if not m:
            break
        card_start = pos + m.start()
        # Find the closing </div></div> for this card. Each card has
        # exactly 2 nested closing divs. Walk balanced.
        depth = 1
        i = card_start + len('<div class="chapter-card">')
        while depth > 0 and i < len(text):
            next_open = text.find('<div', i)
            next_close = text.find('</div>', i)
            if next_close == -1:
                break
            if next_open != -1 and next_open < next_close:
                depth += 1
                i = next_open + 4
            else:
                depth -= 1
                i = next_close + 6
        if depth != 0:
            # Malformed; bail
            break
        end = i
        pos = end
        # Check if the very next non-whitespace is another chapter-card
        gap = text[end:end + 200]
        gap_stripped = gap.lstrip()
        if not gap_stripped.startswith('<div class="chapter-card">'):
            break

    new_text = text[:start] + new_block + "\n" + text[end:]
    return new_text, new_text != text


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    dry_run = not args.apply

    yaml_path = ROOT / "book_structure.yaml"
    struct = yaml.safe_load(yaml_path.read_text(encoding="utf-8"))

    n_changed = 0
    for part in struct.get("parts", []):
        pnum = part["num"]
        pslug = part["slug"]
        idx = ROOT / f"part-{pnum}-{pslug}" / "index.html"
        if not idx.exists():
            print(f"  SKIP: {idx} missing")
            continue
        text = idx.read_text(encoding="utf-8")
        cards = build_chapter_cards(part, pslug, pnum)
        new_text, changed = replace_chapter_card_block(text, cards)
        if changed:
            n_changed += 1
            print(f"  Part {pnum} ({pslug}): chapter cards rebuilt")
            if not dry_run:
                idx.write_text(new_text, encoding="utf-8")
        else:
            print(f"  Part {pnum} ({pslug}): no change needed")

    mode = "DRY-RUN" if dry_run else "APPLY"
    print(f"\n=== {mode} ===")
    print(f"Part indexes changed: {n_changed}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
