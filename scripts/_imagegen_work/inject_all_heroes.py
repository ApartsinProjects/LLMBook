"""Inject <figure class="illustration chapter-opener"> into every landing
page lacking an opener figure, using the existing or freshly-generated
chapter-opener.png / part-opener.png / <stem>-opener.png on disk.

This is the v2 injector that handles all four landing-page categories
(part, chapter, appendix, front-matter), not just the freshly-generated
ones from results.json. It is idempotent: pages already referencing the
expected src are skipped.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path("E:/Projects/BookBlogsHome/LLMBook")
WORK = Path(__file__).parent
LOG_FILE = WORK / "inject_all_log.json"


def extract_h1_subtitle(html_text: str) -> tuple[str, str]:
    h1_match = re.search(r"<h1[^>]*>(.*?)</h1>", html_text, re.DOTALL | re.IGNORECASE)
    h1 = ""
    if h1_match:
        h1 = re.sub(r"<[^>]+>", "", h1_match.group(1))
        h1 = re.sub(r"&amp;", "&", h1)
        h1 = re.sub(r"&[a-z]+;", " ", h1)
        h1 = re.sub(r"\s+", " ", h1).strip()
    sub = ""
    for cls in ("chapter-subtitle", "subtitle", "deck", "lead"):
        m = re.search(
            rf"<p[^>]*class=[\"\'][^\"\']*\b{cls}\b[^\"\']*[\"\'][^>]*>(.*?)</p>",
            html_text, re.DOTALL | re.IGNORECASE,
        )
        if m:
            sub = re.sub(r"<[^>]+>", "", m.group(1))
            sub = re.sub(r"&amp;", "&", sub)
            sub = re.sub(r"\s+", " ", sub).strip()
            break
    return h1, sub


def build_alt(h1: str, subtitle: str, kind: str) -> str:
    label_map = {
        "part": "part",
        "chapter": "chapter",
        "appendix": "appendix",
        "appendix-index": "appendices section",
        "front-matter": "front-matter page",
    }
    label = label_map.get(kind, "section")
    base = (
        f"Warm cartoon-style hero illustration introducing {label} "
        f"'{h1}', a Kurzgesagt-meets-XKCD visual metaphor with friendly "
        f"characters and clear iconography"
    )
    if subtitle:
        sub = subtitle if len(subtitle) <= 90 else subtitle[:87] + "..."
        base = f"{base}, capturing the theme: {sub}"
    return base


def already_referenced(text: str, src_rel: str) -> bool:
    return (f'src="{src_rel}"' in text) or (f"src='{src_rel}'" in text)


def has_opener_already(text: str) -> bool:
    """Detect any <figure> or non-trivial <img> before the first <h2> inside
    <main>. We work on the raw text since BeautifulSoup is overkill here and
    we want to preserve exact formatting on rewrite."""
    main_match = re.search(r"<main[^>]*>", text, re.IGNORECASE)
    if not main_match:
        return False
    start = main_match.end()
    h2_match = re.search(r"<h2[^>]*>", text[start:], re.IGNORECASE)
    end = start + (h2_match.start() if h2_match else len(text) - start)
    region = text[start:end]
    if re.search(r"<figure[^>]*>", region, re.IGNORECASE):
        return True
    # ignore avatar imgs / tiny inline icons. We need to consider not just
    # the tag's own class but also the enclosing span.agent-avatar-inline.
    # Simple approach: walk forward and for each <img>, check the immediate
    # preceding ~120 chars for "agent-avatar-inline".
    for m in re.finditer(r"<img[^>]*>", region, re.IGNORECASE):
        tag = m.group(0)
        if "agent-avatar-inline" in tag:
            continue
        # Check preceding context for the wrapping span class.
        context_start = max(0, m.start() - 200)
        context = region[context_start:m.start()]
        # Look for an opening <span class*="agent-avatar-inline"> that has
        # not been closed before this img.
        spans_open = re.findall(r'<span[^>]*agent-avatar-inline', context)
        spans_close = re.findall(r'</span>', context)
        if len(spans_open) > len(spans_close):
            continue
        return True
    return False


def inject(html_path: Path, src_rel: str, alt: str) -> tuple[bool, str]:
    text = html_path.read_text(encoding="utf-8")
    if already_referenced(text, src_rel):
        return False, "already-referenced"
    if has_opener_already(text):
        return False, "has-other-opener"
    fig = (
        f'<figure class="illustration chapter-opener">'
        f'<img src="{src_rel}" alt="{alt}"/>'
        f'</figure>'
    )
    m = re.search(r"</header>", text, re.IGNORECASE)
    if not m:
        return False, "no-header"
    after = text[m.end():]
    main_match = re.match(r"\s*<main[^>]*>", after, re.IGNORECASE)
    if main_match:
        insert_pos = m.end() + main_match.end()
    else:
        insert_pos = m.end()
    new_text = text[:insert_pos] + "\n" + fig + "\n" + text[insert_pos:]
    html_path.write_text(new_text, encoding="utf-8")
    return True, "injected"


def gather_targets() -> list[dict]:
    """Return list of (html_path, png_path, src_rel, kind) for all landing
    pages that need a hero figure injected."""
    targets: list[dict] = []

    parts = sorted(
        [p for p in ROOT.iterdir() if p.is_dir() and re.match(r"^part-\d+-", p.name)],
        key=lambda p: int(re.match(r"^part-(\d+)-", p.name).group(1)),
    )

    # Part landings
    for part in parts:
        html = part / "index.html"
        if not html.exists():
            continue
        png = part / "images" / "part-opener.png"
        if not png.exists():
            continue
        targets.append({
            "html": html, "png": png,
            "src_rel": "images/part-opener.png",
            "kind": "part",
        })

    # Chapter landings
    for part in parts:
        for mod in sorted(part.glob("module-*")):
            html = mod / "index.html"
            if not html.exists():
                continue
            png = mod / "images" / "chapter-opener.png"
            if not png.exists():
                continue
            targets.append({
                "html": html, "png": png,
                "src_rel": "images/chapter-opener.png",
                "kind": "chapter",
            })

    # Appendix index + appendix pages
    app_root = ROOT / "appendices"
    if app_root.exists():
        html = app_root / "index.html"
        png = app_root / "images" / "chapter-opener.png"
        if html.exists() and png.exists():
            targets.append({
                "html": html, "png": png,
                "src_rel": "images/chapter-opener.png",
                "kind": "appendix-index",
            })
        for app in sorted(app_root.glob("appendix-*")):
            if not app.is_dir():
                continue
            html = app / "index.html"
            if not html.exists():
                continue
            png = app / "images" / "chapter-opener.png"
            if not png.exists():
                continue
            targets.append({
                "html": html, "png": png,
                "src_rel": "images/chapter-opener.png",
                "kind": "appendix",
            })

    # Front-matter pages
    fm_dir = ROOT / "front-matter"
    if fm_dir.exists():
        for fp in sorted(fm_dir.glob("*.html")):
            stem = fp.stem
            if stem == "about-authors":
                continue
            png = fm_dir / "images" / f"{stem}-opener.png"
            if not png.exists():
                continue
            targets.append({
                "html": fp, "png": png,
                "src_rel": f"images/{stem}-opener.png",
                "kind": "front-matter",
            })

    return targets


def main() -> int:
    targets = gather_targets()
    log: list[dict] = []
    injected = skipped = failed = 0
    for t in targets:
        html_path: Path = t["html"]
        text = html_path.read_text(encoding="utf-8")
        h1, sub = extract_h1_subtitle(text)
        alt = build_alt(h1, sub, t["kind"])
        ok, why = inject(html_path, t["src_rel"], alt)
        entry = {
            "html": str(html_path.relative_to(ROOT)).replace("\\", "/"),
            "src_rel": t["src_rel"],
            "kind": t["kind"],
            "result": why,
            "h1": h1,
        }
        log.append(entry)
        if ok:
            injected += 1
        elif why in ("already-referenced", "has-other-opener"):
            skipped += 1
        else:
            failed += 1
    LOG_FILE.write_text(json.dumps(log, indent=2), encoding="utf-8")
    print(f"Total candidates : {len(targets)}")
    print(f"Injected         : {injected}")
    print(f"Skipped          : {skipped}")
    print(f"Failed           : {failed}")
    print(f"Log              : {LOG_FILE}")
    if failed:
        print("\nFailures:")
        for e in log:
            if e["result"] not in ("injected", "already-referenced", "has-other-opener"):
                print(f"  {e['result']}: {e['html']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
