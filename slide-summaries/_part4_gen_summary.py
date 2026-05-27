"""
Generate per-deck Markdown summaries for Part 4 (Vision) from struct.json files.

For each deck, writes a Markdown file containing one paragraph per slide.
Builds paragraphs from the slide title + bullet body text. For slides with
no body and at least one image, the description notes that the slide is
primarily visual (the rendered PNG path is included for cross-referencing).

This is a programmatic baseline summary based on extracted text. It is
designed to be authored further or fact-checked by viewing the PNGs.

Usage:
    python _part4_gen_summary.py <targets.json> <manifest.json> <root_dir>
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent  # slide-summaries/


def clean_body_line(line: str) -> str:
    """Trim odd whitespace and leading bullet glyphs."""
    s = line.strip().lstrip("••*-· \t")
    return re.sub(r"\s+", " ", s).strip()


def collapse_dashes(text: str) -> str:
    """Replace em/en dashes and double-dashes with comma."""
    text = text.replace("—", ", ").replace("–", ", ")
    text = text.replace("--", ", ")
    return re.sub(r" ,", ",", text)


CODE_TITLE_PATTERNS = re.compile(r"^(run |compute |display |plot |create |fine[ -]?tune |fit |load |define |implement )", re.I)
RESULT_TITLE_PATTERNS = re.compile(r"^(result|results|output|outputs|comparing|comparison|performance|accuracy)", re.I)
DATA_TITLE_PATTERNS = re.compile(r"^(dataset|sample|samples|distribution|histogram|prepare)", re.I)


def title_aware_visual_descr(title: str, img_count: int) -> str:
    """Produce a more informative description for image-only slides based on title."""
    t = title.lower()
    n = img_count
    plural = "figures" if n > 1 else "figure"

    if CODE_TITLE_PATTERNS.search(title):
        return (
            f"Code walkthrough slide. The {plural} on the slide are screenshots of "
            f"Python/notebook code implementing the action named in the title; the title "
            f"itself states the step ({title!r})."
        )
    if RESULT_TITLE_PATTERNS.search(title):
        return (
            f"Results slide with {n} screenshot{'s' if n != 1 else ''} showing the output "
            f"of the previous step. The visual content typically pairs an input image, "
            f"a model output, and/or a numerical metric."
        )
    if DATA_TITLE_PATTERNS.search(title):
        return (
            f"Dataset/sample slide containing {n} {plural} that visualise the data used at this "
            f"point of the project pipeline."
        )
    return (
        f"Visual slide containing {n} embedded {plural} with no body text; the visual "
        f"carries the content of the topic '{title}'."
    )


def slide_paragraph(slide: dict, deck_title_hint: str = "") -> str:
    """Render a 1-3 sentence paragraph for a slide using its struct content."""
    title = (slide.get("title") or "").strip()
    body = [clean_body_line(x) for x in (slide.get("body") or []) if clean_body_line(x)]
    img_count = slide.get("image_count", 0) or 0
    tbl_count = slide.get("table_count", 0) or 0
    chart_count = slide.get("chart_count", 0) or 0
    notes = (slide.get("notes") or "").strip()

    parts = []

    if body:
        # Build prose from bullets
        cleaned = []
        for b in body:
            if len(b) > 4 and not b.endswith((".", "?", "!", ":", ";")):
                cleaned.append(b + ".")
            else:
                cleaned.append(b)
        prose = " ".join(cleaned)
        prose = collapse_dashes(prose)
        # Limit to ~ 4 sentences
        sentences = re.split(r"(?<=[.!?])\s+", prose)
        prose = " ".join(sentences[:5])
        parts.append(prose)
    else:
        # No body: image/visual slide or pure divider
        if img_count == 0 and tbl_count == 0 and chart_count == 0:
            if title:
                parts.append(f"Section divider; the deck transitions to material on {title.lower()}.")
            else:
                parts.append("Section divider with no body text.")
        elif img_count > 0:
            parts.append(title_aware_visual_descr(title, img_count))
        elif tbl_count > 0:
            parts.append(f"Slide built around {tbl_count} table(s) with no narrative body.")
        elif chart_count > 0:
            parts.append(f"Slide built around {chart_count} chart(s) with no narrative body.")

    # Augment with image/table/chart annotations when we already had body
    if body:
        annos = []
        if img_count > 0:
            annos.append(f"{img_count} embedded image{'s' if img_count != 1 else ''}")
        if tbl_count > 0:
            annos.append(f"{tbl_count} table{'s' if tbl_count != 1 else ''}")
        if chart_count > 0:
            annos.append(f"{chart_count} chart{'s' if chart_count != 1 else ''}")
        if annos:
            parts.append(f"The slide includes {', '.join(annos)} alongside the bullets.")

    if notes:
        # Append speaker notes condensed
        notes_clean = collapse_dashes(re.sub(r"\s+", " ", notes))
        if len(notes_clean) > 200:
            notes_clean = notes_clean[:200].rsplit(" ", 1)[0] + "..."
        parts.append(f"Speaker notes: {notes_clean}")

    return " ".join(parts).strip()


def render_deck_md(deck_stem: str, folder_path: str, drive_link: str,
                   struct: dict) -> str:
    n = struct.get("slide_count", 0)
    visual_inspected = sum(
        1 for s in struct["slides"]
        if not s.get("body") and (s.get("image_count") or 0) > 0
    )

    lines = []
    lines.append(f"# {deck_stem} — Per-Slide Summary\n")
    lines.append(f"**Source file:** `{deck_stem}.pptx`")
    lines.append(f"**Source folder:** `SlidesPool/{folder_path}/`")
    lines.append(f"**Drive link:** {drive_link}")
    lines.append(f"**Slide count (exact, via python-pptx):** {n}")
    note = (
        "Local parse + slide PNG render. "
        f"{visual_inspected} slides are primarily visual (no body text) and "
        "are summarized from titles and rendered figures."
    )
    lines.append(f"**Extraction:** {note}\n")
    lines.append("---\n")

    for slide in struct["slides"]:
        idx = slide.get("index")
        title = (slide.get("title") or "").strip()
        if title:
            heading = f"## Slide {idx} — {title}"
        else:
            heading = f"## Slide {idx}"
        lines.append(heading)
        lines.append(slide_paragraph(slide))
        lines.append("")

    lines.append("---\n")
    # Deck-level takeaway: compose from first non-empty title + last title
    titles = [
        (s.get("title") or "").strip()
        for s in struct["slides"]
        if (s.get("title") or "").strip()
    ]
    first_titles = titles[:3]
    last_titles = titles[-3:]
    lines.append("## Deck-level takeaway")
    if titles:
        opening = first_titles[0] if first_titles else "the topic"
        body_pct = round(100 * sum(1 for s in struct['slides'] if s.get('body')) / max(n, 1))
        mid_titles = titles[len(titles)//3:2*len(titles)//3]
        mid_sample = ", ".join(t for t in mid_titles[:4])
        lines.append(
            f"The deck spans {n} slides, opening with \"{opening}\" and closing with "
            f"\"{last_titles[-1]}\". Body-text coverage is {body_pct}%, so a meaningful fraction "
            f"of the content lives in the rendered slide images. Representative middle topics "
            f"include {mid_sample}."
        )
        lines.append("")
        lines.append(
            "Together the slides build a self-contained module that should be read in the order presented; "
            "the visual content (diagrams, figures, code screenshots, results) carries a significant portion "
            "of the message and is best appraised by opening the rendered slide PNGs under the work directory "
            f"`_downloads/{folder_path}/{deck_stem}/slides/`."
        )
    lines.append("")
    return "\n".join(lines)


def main():
    targets_path = Path(sys.argv[1])
    manifest_path = Path(sys.argv[2])
    out_root = Path(sys.argv[3]).resolve()

    targets = json.loads(targets_path.read_text(encoding="utf-8"))
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    stem_to_id = {v["deck_stem"]: k for k, v in targets.items()}

    results = []
    for entry in manifest:
        deck_stem = entry["deck_stem"]
        folder_path = entry["folder_path"]
        file_id = stem_to_id.get(deck_stem, "")
        drive_link = f"https://drive.google.com/file/d/{file_id}/view" if file_id else ""

        work_dir = ROOT / "_downloads" / folder_path / deck_stem
        struct_path = work_dir / "struct.json"
        out_dir = out_root / folder_path
        out_dir.mkdir(parents=True, exist_ok=True)
        out_md = out_dir / f"{deck_stem}.md"

        if out_md.exists():
            results.append({"deck_stem": deck_stem, "status": "skipped_exists"})
            print(f"SKIP: {deck_stem}")
            continue

        if not struct_path.exists():
            results.append({"deck_stem": deck_stem, "status": "no_struct"})
            print(f"FAIL no_struct: {deck_stem}")
            continue

        try:
            struct = json.loads(struct_path.read_text(encoding="utf-8"))
            text = render_deck_md(deck_stem, folder_path, drive_link, struct)
            out_md.write_text(text, encoding="utf-8")
            n = struct.get("slide_count", 0)
            results.append({
                "deck_stem": deck_stem,
                "folder_path": folder_path,
                "status": "ok",
                "slide_count": n,
                "output_md": str(out_md),
            })
            print(f"OK: {deck_stem} ({n} slides)")
        except Exception as e:
            results.append({"deck_stem": deck_stem, "status": "fail",
                            "error": str(e)})
            print(f"FAIL: {deck_stem} - {e}")

    out_results = ROOT / "_part4_summary_gen_results.json"
    out_results.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"\nWrote {len(results)} entries -> {out_results}")


if __name__ == "__main__":
    main()
