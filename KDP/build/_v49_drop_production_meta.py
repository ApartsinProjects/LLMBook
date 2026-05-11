"""v4.9: Drop production-meta from front matter.

Removes:
  1. front-matter/section-fm.5.html (How This Book Was Created)
  2. front-matter/wisdom-council.json (orphan after wisdom-council.html
     was deleted in v3.x)
  3. Production-meta references in other front-matter files:
     - about-book.html: 'Wisdom Council' / 'Writing Team' paragraph and
       'How This Book Was Created' H2 + content
     - foreword.html: link to FM.7 'How This Book Was Created'
     - copyright.html: 'Wisdom Council were generated using Gemini' bullet
     - index.html: cards for 'The Wisdom Council' and 'How This Book Was
       Created'
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
EXCLUDE = {"_archive", "KDP", "node_modules", "vendor", "scripts"}


def safe_read(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="replace")


def main() -> int:
    # 1. Delete files
    fm5 = ROOT / "front-matter/section-fm.5.html"
    if fm5.exists():
        words = len(re.sub(r"<[^>]+>", " ", safe_read(fm5)).split())
        fm5.unlink()
        print(f"  rm front-matter/section-fm.5.html ({words} words)")

    wc_json = ROOT / "front-matter/wisdom-council.json"
    if wc_json.exists():
        wc_json.unlink()
        print(f"  rm front-matter/wisdom-council.json (orphan metadata)")

    # 2. Strip production-meta paragraphs from about-book.html
    p = ROOT / "front-matter/about-book.html"
    if p.exists():
        text = safe_read(p)
        original = text
        # Strip the 'How This Book Was Created' H2 and following content up to next H2 or </main>
        text = re.sub(
            r'<h2[^>]*>\s*How This Book Was Created\s*</h2>.*?(?=<h2|</main>)',
            '', text, flags=re.DOTALL,
        )
        # Strip the Writing Team / Wisdom Council paragraph
        text = re.sub(
            r'\s*<p>To meet the specialized agents,\s*see The Writing Team[^<]*'
            r'(?:<a[^>]*>[^<]*</a>[^<]*)*\.</p>',
            '', text, flags=re.DOTALL,
        )
        # Also strip standalone 'For the 42 fictional AI characters' paragraphs
        text = re.sub(
            r'\s*<p>For the 42 fictional AI characters[^<]*(?:<a[^>]*>[^<]*</a>[^<]*)*\.</p>',
            '', text, flags=re.DOTALL,
        )
        if text != original:
            p.write_text(text, encoding="utf-8")
            print(f"  cleaned about-book.html (production-meta stripped)")

    # 3. Strip cross-ref to FM.7 in foreword
    p = ROOT / "front-matter/foreword.html"
    if p.exists():
        text = safe_read(p)
        original = text
        # Strip 'and <a href="section-fm.5.html">FM.7: How This Book Was Created</a>' prefix
        text = re.sub(
            r'\s*and\s*<a\s+href="section-fm\.5\.html">[^<]+</a>\.?',
            '.', text,
        )
        # Also strip "<a href=...fm.5...>...</a>" on its own
        text = re.sub(
            r'<a\s+href="section-fm\.5\.html">[^<]+</a>\.?',
            '', text,
        )
        if text != original:
            p.write_text(text, encoding="utf-8")
            print(f"  cleaned foreword.html (FM.5 reference removed)")

    # 4. Strip 'Wisdom Council were generated using Gemini' bullet from copyright
    p = ROOT / "front-matter/copyright.html"
    if p.exists():
        text = safe_read(p)
        original = text
        text = re.sub(
            r'<li>[^<]*(?:<strong>[^<]*</strong>[^<]*)*Wisdom Council[^<]*'
            r'(?:<strong>[^<]*</strong>[^<]*)*</li>',
            '', text, flags=re.DOTALL,
        )
        if text != original:
            p.write_text(text, encoding="utf-8")
            print(f"  cleaned copyright.html (Wisdom Council bullet removed)")

    # 5. Strip 'Wisdom Council' and 'How This Book Was Created' cards from index
    p = ROOT / "front-matter/index.html"
    if p.exists():
        text = safe_read(p)
        original = text
        # Strip whole <a class="section-card">...The Wisdom Council...</a> block
        text = re.sub(
            r'<a[^>]*class="section-card"[^>]*>(?:[^<]|<(?!/a>))*?The Wisdom Council(?:[^<]|<(?!/a>))*?</a>',
            '', text, flags=re.DOTALL,
        )
        text = re.sub(
            r'<a[^>]*class="section-card"[^>]*>(?:[^<]|<(?!/a>))*?How This Book Was Created(?:[^<]|<(?!/a>))*?</a>',
            '', text, flags=re.DOTALL,
        )
        # Also strip simple href to section-fm.5 and wisdom-council
        text = re.sub(
            r'<a\s+[^>]*href="(?:section-fm\.5\.html|wisdom-council\.html)"[^>]*>[^<]*</a>',
            '', text,
        )
        if text != original:
            p.write_text(text, encoding="utf-8")
            print(f"  cleaned index.html (Wisdom Council + Creation cards removed)")

    # 6. Inbound xref cleanup: any remaining link to section-fm.5 -> remove
    n_inbound = 0
    for fp in ROOT.rglob("*.html"):
        if any(part in fp.parts for part in EXCLUDE): continue
        try:
            text = fp.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        original = text
        # Unwrap any remaining link to section-fm.5
        text = re.sub(
            r'<a\s+[^>]*href="[^"]*section-fm\.5\.html(?:#[^"]*)?"[^>]*>(.*?)</a>',
            r'\1', text, flags=re.DOTALL,
        )
        # Unwrap any remaining link to wisdom-council.html (was already deleted)
        text = re.sub(
            r'<a\s+[^>]*href="[^"]*wisdom-council\.html(?:#[^"]*)?"[^>]*>(.*?)</a>',
            r'\1', text, flags=re.DOTALL,
        )
        if text != original:
            fp.write_text(text, encoding="utf-8")
            n_inbound += 1
    print(f"  Unwrapped fm.5 / wisdom-council.html links in {n_inbound} other files")

    return 0


if __name__ == "__main__":
    sys.exit(main())
