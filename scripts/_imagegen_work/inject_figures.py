"""Inject <figure class="illustration chapter-opener"> into each landing page.

For each accepted image in qa_report.json, edit the index.html to add a figure
right after </header>, unless an image at the same src is already referenced.
Uses chapter-opener.png for chapters and part-opener.png for parts.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

WORK = Path(__file__).parent
QA_FILE = WORK / "qa_report.json"


def inject(html_path: Path, src_rel: str, alt: str) -> tuple[bool, str]:
    text = html_path.read_text(encoding="utf-8")
    # If the same src is already referenced anywhere, skip
    if f'src="{src_rel}"' in text or f"src='{src_rel}'" in text:
        return False, "already-referenced"
    # Build figure
    fig = (
        f'<figure class="illustration chapter-opener">'
        f'<img src="{src_rel}" alt="{alt}"/>'
        f'</figure>'
    )
    # Insert after first </header> tag
    m = re.search(r"</header>", text, re.IGNORECASE)
    if not m:
        return False, "no-header"
    # Look for the <main ...> tag right after header (typical pattern)
    after = text[m.end():]
    main_match = re.match(r"\s*<main[^>]*>", after, re.IGNORECASE)
    if main_match:
        insert_pos = m.end() + main_match.end()
    else:
        insert_pos = m.end()
    new_text = text[:insert_pos] + "\n" + fig + "\n" + text[insert_pos:]
    html_path.write_text(new_text, encoding="utf-8")
    return True, "injected"


def main() -> int:
    if not QA_FILE.exists():
        print("Run compress_and_qa.py first.")
        return 1
    report = json.loads(QA_FILE.read_text(encoding="utf-8"))
    injected = skipped = failed = 0
    log = []
    for r in report:
        if r.get("qa") != "accepted":
            log.append({**r, "inject": "skip-qa"})
            skipped += 1
            continue
        out = Path(r["output_path"])
        kind = r["kind"]
        landing = Path("E:/Projects/BookBlogsHome/LLMBook") / r["part"]
        if kind == "chapter":
            landing = landing / r["module"]
        index_html = landing / "index.html"
        if not index_html.exists():
            log.append({**r, "inject": "no-index"})
            failed += 1
            continue
        # Relative src from the index.html's directory
        rel = "images/" + out.name
        ok, why = inject(index_html, rel, r["alt"])
        if ok:
            injected += 1
            log.append({**r, "inject": "ok"})
        else:
            log.append({**r, "inject": why})
            if why == "already-referenced":
                skipped += 1
            else:
                failed += 1
    (WORK / "inject_log.json").write_text(json.dumps(log, indent=2), encoding="utf-8")
    print(f"Injected: {injected}, Skipped: {skipped}, Failed: {failed}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
