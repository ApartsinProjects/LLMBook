"""
Generate per-deck subagent prompts from a manifest. Prints a JSON list
of {deck_stem, prompt} so the orchestrator can dispatch them.
"""
import json
import sys
from pathlib import Path

DRIVE_URL_BASE = "https://drive.google.com/file/d/{file_id}/view"

PROMPT_TEMPLATE = """You are writing a per-slide Markdown summary for one PowerPoint deck. The deck has already been extracted by the PPTSummary pipeline.

**Deck:** {deck_stem}
**Folder:** {folder_path}
**Drive link:** {drive_link}
**Work dir:** {work_dir}
**Output file:** {output_md}

## Steps
1. Read `<work_dir>/struct.json` (slide_count, slides[] with index, title, body, image_count, embedded_images, slide_png).
2. Visually inspect slides where (body empty AND image_count > 0) OR (cryptic title AND image_count > 0) OR (image_count >= 3 AND short body). Read each flagged PNG with your Read tool.
3. Write output following the template.

## Template
```markdown
# {deck_stem} — Per-Slide Summary

**Source file:** `{deck_stem}.pptx`
**Source folder:** `SlidesPool/{folder_path}/`
**Drive link:** {drive_link}
**Slide count (exact, via python-pptx):** <N>
**Extraction:** Local parse + slide PNG render. <one-sentence visual-inspection note>.

---

## Slide 1 — <title>
<2-5 sentence paragraph; 1 sentence for dividers; for LARGE decks (50+ slides) keep paragraphs concise>

## Slide 2 — <title>
...

---

## Deck-level takeaway
<1-2 paragraphs>
```

## Rules
- No em dashes (—) or `--` in generated text. Use commas, semicolons, parens, or sentence breaks.
- Third-person voice ("The slide defines X").
- Preserve domain terms exactly (BPE, RoPE, ResNet, DPR, attention, etc.).
- One sentence for section dividers.
- For pure-image slides describe what you SEE in the PNG: diagram structure, labels, equations.
- For code screenshots: paraphrase what the code does + transcribe short snippets accurately. For long code blocks, describe purpose rather than transcribe.

## Return
Single JSON line: `{{"deck_stem": "{deck_stem}", "status": "ok", "output_md": "<path>", "slide_count": <N>, "visually_inspected": <K>}}` or `{{"status": "fail", "reason": "<short>"}}`.
"""


def main():
    manifest_path = Path(sys.argv[1])
    targets_path = Path(sys.argv[2])
    output_root = Path(sys.argv[3]).resolve()
    work_root = Path(sys.argv[4]).resolve()

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    targets = json.loads(targets_path.read_text(encoding="utf-8"))

    stem_to_id = {v["deck_stem"]: k for k, v in targets.items()}

    prompts = []
    for entry in manifest:
        deck_stem = entry["deck_stem"]
        folder_path = entry["folder_path"]
        file_id = stem_to_id.get(deck_stem, "")
        drive_link = DRIVE_URL_BASE.format(file_id=file_id) if file_id else ""
        work_dir = work_root / folder_path / deck_stem
        output_md = output_root / folder_path / f"{deck_stem}.md"
        prompt = PROMPT_TEMPLATE.format(
            deck_stem=deck_stem,
            folder_path=folder_path,
            drive_link=drive_link,
            work_dir=str(work_dir).replace("/", "\\"),
            output_md=str(output_md).replace("/", "\\"),
        )
        prompts.append({"deck_stem": deck_stem, "folder_path": folder_path, "prompt": prompt})

    print(json.dumps(prompts, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
