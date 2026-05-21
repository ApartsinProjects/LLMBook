"""Audit hyperlinks in the appendices and chapter/section card lists.

Checks every internal <a href> in:
  - appendices/**.html  (syllabi, reading pathways, math foundations, index)
  - **/index.html part/module landing pages (chapter & section card lists)

For each link, flags:
  1. BROKEN     - target file does not exist
  2. NUM_MISMATCH - anchor text says "Section X.Y" / "Chapter N" but the target
                    file's number is different (stale after the restructure)
  3. FRAG_BROKEN  - href has a #fragment that is not an id/name in the target
"""
from __future__ import annotations
import re
from pathlib import Path
from urllib.parse import urldefrag

ROOT = Path(__file__).resolve().parent.parent
SKIP = ("_archive/", "KDP/", "node_modules/", "pagefind/", "temp_epub/",
        "templates/", ".git/", ".book-update/", "scripts/")

A_RE = re.compile(r'<a\b[^>]*href="([^"]+)"[^>]*>(.*?)</a>', re.S | re.I)
SEC_IN_NAME = re.compile(r'section-(?:fm\.)?([0-9a-z]+\.[0-9a-z]+)', re.I)
SEC_IN_TEXT = re.compile(r'\bSection\s+([0-9A-Z]+\.[0-9]+[a-z]?)\b')
CH_IN_TEXT = re.compile(r'\bChapter\s+([0-9]+)\b')
MOD_NUM = re.compile(r'module-(\d+)')


def targets_set(html: str) -> set:
    ids = set(re.findall(r'\bid="([^"]+)"', html))
    ids |= set(re.findall(r'\bname="([^"]+)"', html))
    return ids


def should_skip(p: Path) -> bool:
    s = str(p).replace("\\", "/") + "/"
    return any(k in s for k in SKIP)


def scan_targets() -> set:
    files = set()
    for p in ROOT.rglob("*.html"):
        if not should_skip(p):
            files.add(p.resolve())
    return files


def main():
    files = scan_targets()
    # Pages to audit: all appendix pages + every index.html (card lists)
    audit_pages = []
    for p in files:
        rel = str(p.relative_to(ROOT)).replace("\\", "/")
        if rel.startswith("appendices/") or p.name == "index.html":
            audit_pages.append(p)

    broken, num_mismatch, frag_broken = [], [], []
    frag_cache: dict = {}
    for p in sorted(audit_pages):
        rel = str(p.relative_to(ROOT)).replace("\\", "/")
        html = p.read_text(encoding="utf-8", errors="replace")
        for href, text in A_RE.findall(html):
            if href.startswith(("http://", "https://", "mailto:", "tel:", "javascript:", "data:")):
                continue
            base, frag = urldefrag(href)
            if not base:
                continue  # pure in-page anchor
            tgt = (p.parent / base).resolve()
            anchor_text = re.sub(r"<[^>]+>", "", text).strip()
            if tgt not in files:
                broken.append((rel, href, anchor_text[:50]))
                continue
            # number alignment: anchor text "Section X.Y" vs file section-X.Y
            mt = SEC_IN_TEXT.search(anchor_text)
            mn = SEC_IN_NAME.search(base)
            if mt and mn and mt.group(1).lower() != mn.group(1).lower():
                num_mismatch.append((rel, href, anchor_text[:50],
                                     f"text={mt.group(1)} file={mn.group(1)}"))
            # fragment check
            if frag:
                if tgt not in frag_cache:
                    frag_cache[tgt] = targets_set(tgt.read_text(encoding="utf-8", errors="replace"))
                if frag not in frag_cache[tgt]:
                    frag_broken.append((rel, href, anchor_text[:50]))

    print(f"Audited {len(audit_pages)} pages (appendices + index card lists)\n")
    print(f"BROKEN targets: {len(broken)}")
    for r, h, t in broken[:40]:
        print(f"  {r}\n     -> {h}   [{t}]")
    print(f"\nNUMBER MISMATCH (text vs file): {len(num_mismatch)}")
    for r, h, t, d in num_mismatch[:40]:
        print(f"  {r}\n     -> {h}   [{t}]  ({d})")
    print(f"\nFRAGMENT BROKEN (#id not in target): {len(frag_broken)}")
    for r, h, t in frag_broken[:60]:
        print(f"  {r}\n     -> {h}   [{t}]")


if __name__ == "__main__":
    main()
