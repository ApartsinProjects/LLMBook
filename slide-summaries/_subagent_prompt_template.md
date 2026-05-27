# Subagent prompt: write a per-slide Markdown summary for one .pptx deck

You will write a verbose, per-slide Markdown summary for a single PowerPoint deck.
The deck has already been extracted by the PPTSummary pipeline; all you need to do
is read the structured JSON, visually inspect the slide PNGs that need it, and
write one Markdown file following a fixed template.

## Inputs (substitute when invoking)

* **DECK_STEM**: `{deck_stem}` (the title of the deck without extension)
* **FOLDER_PATH**: `{folder_path}` (the original Drive folder name, e.g. `0000_Common_Math`)
* **DRIVE_LINK**: `{drive_link}` (the original Drive view URL)
* **WORK_DIR** (absolute path): `{work_dir}` — contains `struct.json`, `slides/`, `images/`
* **OUTPUT_MD** (absolute path): `{output_md_abs}` — where you must write the final `.md`

## Your task, step by step

1. **Read `WORK_DIR/struct.json`.** It contains `slide_count` and a `slides` array.
   Each slide entry has: `index`, `title`, `body` (list of text blocks), `image_count`,
   `table_count`, `chart_count`, `notes`, `embedded_images` (paths under `images/`),
   and `slide_png` (path under `slides/`, e.g. `slides/slide_017.png`).

2. **Identify slides that need visual analysis.** A slide needs to be visually inspected
   (by reading its PNG with your multimodal Read tool) if ANY of these is true:
   * `body` is empty AND `image_count > 0` (pure-image slide; text frames don't tell the story).
   * The slide's title is cryptic and `image_count > 0` (e.g., a one-word title like "Example").
   * `image_count >= 3` AND the body text is short (likely a code-screenshot or diagram-heavy slide).
   For all other slides, the extracted text is usually enough.

3. **For each slide you flagged**, read `WORK_DIR/<slide_png>` (e.g.
   `WORK_DIR/slides/slide_017.png`) using your Read tool. The image is rendered exactly
   as PowerPoint shows it — including all embedded text, diagrams, formulas, code, etc.
   You can interpret diagrams ("a 5-petal AI chip diagram naming developer-workflow uses"),
   read formulas, transcribe code snippets, etc.

4. **Write the summary to `OUTPUT_MD`** following exactly the template below.

## Output template

```markdown
# {deck_stem} — Per-Slide Summary

**Source file:** `{deck_stem}.pptx`
**Source folder:** `SlidesPool/{folder_path}/`
**Drive link:** {drive_link}
**Slide count (exact, via python-pptx):** {slide_count}
**Extraction:** Local parse + slide PNG render. {one short sentence about what fraction of slides needed visual inspection}.

---

## Slide 1 — {slide_1_title or "(untitled)"}

{One verbose paragraph. Use the extracted body text if present; supplement with what you SEE in the PNG if you inspected it. Describe content + shape (list / two-column / timeline / diagram / code screenshot). For pure-image slides, describe the diagram structure and labels you read. For code screenshots, paraphrase what the code does and transcribe short snippets accurately; if a long block of code is too dense to transcribe reliably, say so explicitly and describe its purpose.}

## Slide 2 — {slide_2_title}

{...}

## Slide N — {slide_N_title}

{...}

---

## Deck-level takeaway

{One or two paragraphs summarizing the deck's overall arc and pedagogical signature.}
```

## Visual analysis policy

* **Diagrams**: prefer interpretation over transcription. "A 5-petal AI chip diagram naming the developer-workflow uses" is more useful than a flat list of label strings.
* **Code screenshots**: transcribe accurately for short snippets; for long blocks, paraphrase + name the function/structure and never invent code.
* **Formulas in images**: describe in words ("the EM lower-bound derivation via Jensen's inequality applied to log") unless transcription is brief and unambiguous.
* **Section dividers** (slides with only a title and no body): one sentence is enough.
* **Repeat title slides** (e.g., "Transformer" appearing twice as a divider): note it as a divider and move on.

## Style rules

* No em dashes (`—`) inside generated text. Use commas / semicolons / parens / sentence breaks instead. (Em dashes ARE OK in the headings rendered by the template above — those come from the template itself.)
* Use third-person describing the slide, e.g., "The slide defines X as Y" rather than "We define X as Y".
* Each `## Slide N` paragraph should be 3-8 sentences for ordinary slides; 1 sentence for dividers.
* Use exact technical vocabulary from the extracted text; do not paraphrase domain terms (BPE, RoPE, ResNet, DPR, etc.).

## Return

After writing the file, return a single short JSON line:
```
{"deck_stem": "<DECK_STEM>", "status": "ok", "output_md": "<OUTPUT_MD>", "slide_count": <N>, "visually_inspected": <K>}
```

If you hit any error you cannot resolve, return:
```
{"deck_stem": "<DECK_STEM>", "status": "fail", "reason": "<short>"}
```
