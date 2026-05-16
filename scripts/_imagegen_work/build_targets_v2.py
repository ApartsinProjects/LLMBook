"""Build the target list and prompts for hero/opener image generation.

v2: extends v1 to also cover appendix landings, the appendix index, and
front-matter pages, in addition to part and chapter landings. Idempotent:
skips targets whose output PNG already exists.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path("E:/Projects/BookBlogsHome/LLMBook")
OUT_JSON = Path(__file__).parent / "targets.json"
OUT_PROMPTS = Path(__file__).parent / "prompts.txt"

STYLE_SUFFIX = (
    "Style: Kurzgesagt meets XKCD, hand-drawn warmth, friendly characters, "
    "vibrant flat palette, clear visual metaphor, gentle textures, "
    "no text in image. Aspect 16:9."
)


def extract_h1_subtitle(html_path: Path) -> tuple[str, str]:
    text = html_path.read_text(encoding="utf-8", errors="ignore")
    h1_match = re.search(r"<h1[^>]*>(.*?)</h1>", text, re.DOTALL | re.IGNORECASE)
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
            text, re.DOTALL | re.IGNORECASE,
        )
        if m:
            sub = re.sub(r"<[^>]+>", "", m.group(1))
            sub = re.sub(r"&amp;", "&", sub)
            sub = re.sub(r"\s+", " ", sub).strip()
            break
    # description meta as fallback subtitle
    if not sub:
        m = re.search(
            r'<meta[^>]*name=["\']description["\'][^>]*content=["\']([^"\']+)["\']',
            text, re.IGNORECASE,
        )
        if m:
            sub = re.sub(r"\s+", " ", m.group(1)).strip()
    return h1, sub


def build_prompt(h1: str, subtitle: str, kind: str) -> str:
    label_map = {
        "part": "part",
        "chapter": "chapter",
        "appendix": "appendix",
        "appendix-index": "appendix section",
        "front-matter": "front-matter section",
    }
    label = label_map.get(kind, "section")
    if subtitle:
        core = (
            f"Warm cartoon-style illustration for a book {label} titled "
            f"'{h1}'. Subtitle: '{subtitle}'."
        )
    else:
        core = (
            f"Warm cartoon-style illustration for a book {label} titled "
            f"'{h1}'."
        )
    return f"{core} {STYLE_SUFFIX}"


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


def add_target(
    targets: list,
    kind: str,
    landing_dir: Path,
    index_path: Path,
    output_name: str,
    label_part: str,
    label_module: str | None,
):
    opener = landing_dir / "images" / output_name
    if opener.exists():
        return  # idempotent: skip
    h1, sub = extract_h1_subtitle(index_path)
    if not h1:
        print(f"WARN: no h1 in {index_path}", file=sys.stderr)
        return
    targets.append({
        "kind": kind,
        "part": label_part,
        "module": label_module,
        "index_path": str(index_path),
        "output_path": str(opener),
        "h1": h1,
        "subtitle": sub,
        "prompt": build_prompt(h1, sub, kind),
        "alt": build_alt(h1, sub, kind),
    })


def main() -> int:
    targets: list[dict] = []

    parts = sorted(
        [p for p in ROOT.iterdir() if p.is_dir() and re.match(r"^part-\d+-", p.name)],
        key=lambda p: int(re.match(r"^part-(\d+)-", p.name).group(1)),
    )

    # Part landings
    for part in parts:
        idx = part / "index.html"
        if not idx.exists():
            continue
        add_target(targets, "part", part, idx, "part-opener.png",
                   part.name, None)

    # Chapter landings
    for part in parts:
        for mod in sorted(part.glob("module-*"),
                          key=lambda m: int(re.match(r"^module-(\d+)", m.name).group(1))
                          if re.match(r"^module-(\d+)", m.name) else 9999):
            idx = mod / "index.html"
            if not idx.exists():
                continue
            add_target(targets, "chapter", mod, idx, "chapter-opener.png",
                       part.name, mod.name)

    # Appendices index
    app_root = ROOT / "appendices"
    if app_root.exists():
        app_idx = app_root / "index.html"
        if app_idx.exists():
            add_target(targets, "appendix-index", app_root, app_idx,
                       "chapter-opener.png", "appendices", None)
        # Individual appendices
        for app in sorted(app_root.glob("appendix-*")):
            if not app.is_dir():
                continue
            idx = app / "index.html"
            if not idx.exists():
                continue
            add_target(targets, "appendix", app, idx, "chapter-opener.png",
                       "appendices", app.name)

    # Front-matter pages: each is a top-level .html file in front-matter/
    fm_dir = ROOT / "front-matter"
    if fm_dir.exists():
        for fp in sorted(fm_dir.glob("*.html")):
            # Skip about-authors (has author cards) — but only if it already
            # had an opener; here we just rely on the "already has hero"
            # filter applied later via existence check. Skip if the existing
            # image is a portrait .jpg by checking for our PNG slot.
            stem = fp.stem
            opener_name = f"{stem}-opener.png"
            opener = fm_dir / "images" / opener_name
            if opener.exists():
                continue
            h1, sub = extract_h1_subtitle(fp)
            if not h1:
                print(f"WARN: no h1 in {fp}", file=sys.stderr)
                continue
            # Skip about-authors specifically (already has portraits).
            if stem == "about-authors":
                continue
            targets.append({
                "kind": "front-matter",
                "part": "front-matter",
                "module": stem,
                "index_path": str(fp),
                "output_path": str(opener),
                "h1": h1,
                "subtitle": sub,
                "prompt": build_prompt(h1, sub, "front-matter"),
                "alt": build_alt(h1, sub, "front-matter"),
            })

    OUT_JSON.write_text(json.dumps(targets, indent=2), encoding="utf-8")
    OUT_PROMPTS.write_text("\n".join(t["prompt"] for t in targets), encoding="utf-8")

    by_kind: dict[str, int] = {}
    for t in targets:
        by_kind[t["kind"]] = by_kind.get(t["kind"], 0) + 1
    print(f"Targets: {len(targets)} total")
    for k, n in sorted(by_kind.items()):
        print(f"  {k}: {n}")
    print(f"Wrote: {OUT_JSON}")
    print(f"Wrote: {OUT_PROMPTS}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
