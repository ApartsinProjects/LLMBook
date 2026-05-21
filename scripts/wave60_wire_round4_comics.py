"""Wave 60: Wire wave60_comic_round4 comic images into HTML sections.

For each entry in scripts/wave60_comic_round4.json, find the anchor (an existing
<h2>) inside the target section file and inject a canonical
<div class="callout fun-note"> ... </div> immediately after that line. Only
wires entries whose comic-*.png actually exists in the section's images/ dir
(skips silently otherwise).

Modelled on scripts/wave39c_wire_round2_comics.py.
"""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
PROMPTS_JSON = ROOT / "scripts" / "wave60_comic_round4.json"


def make_callout(callout_type: str, title: str, alt: str, src: str, caption_html: str) -> str:
    """Build the canonical fun-note callout HTML matching prior wave style."""
    return (
        f'<div class="callout {callout_type}">\n'
        f'<div class="callout-title">{title}</div>\n'
        f'<figure class="illustration">\n'
        f'<img alt="{alt}" src="{src}"/>\n'
        f'<figcaption>{caption_html}</figcaption>\n'
        f'</figure>\n'
        f'</div>\n'
    )


def slug_from_name(name: str) -> str:
    """Map 'ch16-3-catastrophic-forgetting-lr' -> 'catastrophic-forgetting-lr'."""
    parts = name.split("-")
    if parts and parts[0].startswith("ch") and len(parts) >= 3:
        return "-".join(parts[2:])
    return "-".join(parts)


def main():
    entries = json.loads(PROMPTS_JSON.read_text(encoding="utf-8"))
    print(f"Loaded {len(entries)} comic entries from {PROMPTS_JSON.name}")
    n_inserted = 0
    n_skipped_no_image = 0
    n_skipped_already = 0
    n_no_anchor = 0
    n_missing_file = 0

    for entry in entries:
        name = entry["name"]
        section_rel = entry["section_path"].replace("\\", "/")
        section_path = ROOT / section_rel
        image_filename = f"comic-{slug_from_name(name)}.png"
        image_relpath = f"images/{image_filename}"
        image_abspath = section_path.parent / "images" / image_filename

        if not section_path.exists():
            print(f"  MISS-FILE   {name}: section not found at {section_rel}")
            n_missing_file += 1
            continue

        if not image_abspath.exists():
            print(f"  SKIP-NOIMG  {name}: image not generated yet ({image_filename})")
            n_skipped_no_image += 1
            continue

        text = section_path.read_text(encoding="utf-8")
        if image_relpath in text:
            print(f"  SKIP-WIRED  {name}: image already referenced in section")
            n_skipped_already += 1
            continue

        anchor = entry["after_text"]
        idx = text.find(anchor)
        if idx == -1:
            print(f"  NO-ANCHOR   {name}: anchor not found: {anchor[:70]!r}")
            n_no_anchor += 1
            continue

        line_end = text.find("\n", idx + len(anchor))
        if line_end == -1:
            line_end = idx + len(anchor)
        insertion_pt = line_end + 1

        callout = make_callout(
            "fun-note",
            entry["callout_title"],
            entry["alt"],
            image_relpath,
            entry["caption_html"],
        )

        new_text = text[:insertion_pt] + callout + text[insertion_pt:]
        section_path.write_text(new_text, encoding="utf-8")
        print(f"  WIRED       {name} -> {section_rel}")
        n_inserted += 1

    print("\nSummary:")
    print(f"  wired:           {n_inserted}")
    print(f"  skip (no image): {n_skipped_no_image}")
    print(f"  skip (already):  {n_skipped_already}")
    print(f"  no anchor:       {n_no_anchor}")
    print(f"  missing file:    {n_missing_file}")


if __name__ == "__main__":
    main()
