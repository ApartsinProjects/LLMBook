"""Build the target list and prompts for hero/opener image generation.

Walks the LLMBook tree, identifies all parts and chapters lacking an opener
image, extracts the h1 + subtitle, and emits a JSON file of (output_path,
prompt, alt_text) triples for the batch generator.
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
    # h1
    h1_match = re.search(r"<h1[^>]*>(.*?)</h1>", text, re.DOTALL | re.IGNORECASE)
    h1 = ""
    if h1_match:
        h1 = re.sub(r"<[^>]+>", "", h1_match.group(1))
        h1 = re.sub(r"&amp;", "&", h1)
        h1 = re.sub(r"&[a-z]+;", " ", h1)
        h1 = re.sub(r"\s+", " ", h1).strip()
    # subtitle: try several classes
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
    return h1, sub


def build_prompt(h1: str, subtitle: str, kind: str) -> str:
    label = "part" if kind == "part" else "chapter"
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
    label = "Part" if kind == "part" else "Chapter"
    base = (
        f"Warm cartoon-style hero illustration introducing {label.lower()} "
        f"'{h1}', a Kurzgesagt-meets-XKCD visual metaphor with friendly "
        f"characters and clear iconography"
    )
    if subtitle:
        # add short context from subtitle (first ~80 chars)
        sub = subtitle if len(subtitle) <= 90 else subtitle[:87] + "..."
        base = f"{base}, capturing the theme: {sub}"
    return base


def main() -> int:
    targets: list[dict] = []

    parts = sorted(
        [p for p in ROOT.iterdir() if p.is_dir() and re.match(r"^part-\d+-", p.name)],
        key=lambda p: int(re.match(r"^part-(\d+)-", p.name).group(1)),
    )

    for part in parts:
        idx = part / "index.html"
        if not idx.exists():
            continue
        opener = part / "images" / "part-opener.png"
        if opener.exists():
            continue
        h1, sub = extract_h1_subtitle(idx)
        if not h1:
            print(f"WARN: no h1 in {idx}", file=sys.stderr)
            continue
        targets.append({
            "kind": "part",
            "part": part.name,
            "module": None,
            "index_path": str(idx),
            "output_path": str(opener),
            "h1": h1,
            "subtitle": sub,
            "prompt": build_prompt(h1, sub, "part"),
            "alt": build_alt(h1, sub, "part"),
        })

    for part in parts:
        for mod in sorted(part.glob("module-*"),
                          key=lambda m: int(re.match(r"^module-(\d+)", m.name).group(1))
                          if re.match(r"^module-(\d+)", m.name) else 9999):
            idx = mod / "index.html"
            if not idx.exists():
                continue
            opener = mod / "images" / "chapter-opener.png"
            if opener.exists():
                continue
            h1, sub = extract_h1_subtitle(idx)
            if not h1:
                print(f"WARN: no h1 in {idx}", file=sys.stderr)
                continue
            targets.append({
                "kind": "chapter",
                "part": part.name,
                "module": mod.name,
                "index_path": str(idx),
                "output_path": str(opener),
                "h1": h1,
                "subtitle": sub,
                "prompt": build_prompt(h1, sub, "chapter"),
                "alt": build_alt(h1, sub, "chapter"),
            })

    OUT_JSON.write_text(json.dumps(targets, indent=2), encoding="utf-8")
    OUT_PROMPTS.write_text("\n".join(t["prompt"] for t in targets), encoding="utf-8")

    n_parts = sum(1 for t in targets if t["kind"] == "part")
    n_chap = sum(1 for t in targets if t["kind"] == "chapter")
    print(f"Targets: {len(targets)} total ({n_parts} parts, {n_chap} chapters)")
    print(f"Wrote: {OUT_JSON}")
    print(f"Wrote: {OUT_PROMPTS}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
