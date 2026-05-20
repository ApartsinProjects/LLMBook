# Table of Contents and Front Matter Audit Report

Date: 2026-05-19
Branch: v2.0
Auditor: cycle-B agent (7th)

## Scope

- `toc.html`
- `front-matter/foreword.html`
- `front-matter/fm-what-this-book-covers.html`
- `front-matter/fm-who-should-read.html`
- `front-matter/fm-how-to-use.html`
- `front-matter/look-inside-preview.html`
- `front-matter/about-authors.html`
- `front-matter/copyright.html`

## Ground truth

Extracted from `part-*/module-*/index.html` H1 tags. 16 parts, 83 chapters, 470 sections.
See `_book_structure.json`.

## Helper artifacts

- `_book_structure.json` - ground truth dump
- `_build_book_structure.py` - script that builds it
- `_audit_toc.py` - audits toc.html against ground truth
- `_audit_fm.py` - audits FM file hrefs

---

## 1. toc.html chapter title mismatches (fixed)

The TOC had 9 chapter title labels that no longer matched the module's `<h1>`. All updated to match the source-of-truth module index.

| Chapter | Old TOC title | New TOC title (matches module H1) |
|---------|--------------|-----------------------------------|
| 17 | Parameter-Efficient Fine-Tuning (PEFT) | Parameter-Efficient Fine-Tuning, Distillation & Model Merging |
| 20 | Audio and Music Generation | Audio, Music, and Video Generation |
| 22 | Vision-Language Models | Vision-Language and Omni Models |
| 24 | Vision-Language-Action Models | VLA Models and LLM-Powered Robotics |
| 52 | Bias, Fairness, and Disparate Impact | Bias, Fairness & Hallucinations |
| 54 | Watermarking, Provenance, and Deepfake Defense | Watermarking and Provenance |
| 55 | Environmental Impact and Sustainability | Environmental Impact & Green AI |
| 67 | Ideation: Finding LLM-Worthy Problems | From Idea to MVP |
| 78 | LLMs in Manufacturing & Supply Chain | Manufacturing, Creative Industries, Search & Recommendation |

## 2. toc.html subtitle leakage (fixed)

Chapters whose subtitle contained text actually written for a different chapter (text drifted across reordering). Replaced with subtitle text matching the chapter's own description meta or index. Source: the module's own `meta name="description"` content.

| Chapter | Stale subtitle (from previous owner) | Replacement |
|---------|--------------------------------------|-------------|
| 37 | "Joint embedding spaces, multimodal retrieval, when to retrieve vs reason..." (belonged to ch.33) | "Conversational AI brings together everything from prompt engineering to memory management to retrieval." |
| 42 | "Text chat is one mode; conversational AI also lives in voice, video..." (belonged to ch.40-area) | "You cannot improve what you cannot measure." |
| 47 | "Evaluation methodologies for the 2026 frontier: RAG faithfulness..." (belonged to ch.43) | "As LLMs become embedded in high-stakes decisions, safety and ethics move from nice-to-have to regulatory requirements." |

## 3. toc.html cross-reference stale chapter numbers (fixed)

| Chapter | Issue | Fix |
|---------|-------|-----|
| 29 | Subtitle said "While Chapters 22 through 24 cover general agent principles..." | Updated to "Chapters 26 through 28" - the actual general-agent chapters in Part VI |

## 4. toc.html appendix count (fixed)

- Appendix section showed "3 appendices" but lists Appendix A, B, C, and D (4).
- Fixed: "3 appendices" -> "4 appendices".

## 5. front-matter FM.X numbering inconsistency (fixed)

The documents internally use FM.X numbering. The chapter-nav flow (the actual sequential reading order) and toc F1-F7 labels agreed with each other, but disagreed with the FM.X numbers baked into document `<title>` tags and cross-reference text. Renumbered the documents' FM.X to match the chapter-nav reading order.

| File | Old FM.X | New FM.X |
|------|---------|---------|
| foreword.html | FM.1 | FM.1 (unchanged) |
| fm-what-this-book-covers.html | FM.3 | FM.2 |
| fm-who-should-read.html | FM.4 | FM.3 |
| look-inside-preview.html | FM.2 | FM.4 |
| fm-how-to-use.html | FM.5 | FM.5 (unchanged) |
| about-authors.html | FM.6 | FM.6 (unchanged) |
| copyright.html | FM.7 | FM.7 (unchanged) |

Touched: `<title>` tag, `<meta description>`, "What Comes Next" body paragraphs, "Proceed to FM.X" labels, the Figure FM.X.Y caption in look-inside-preview, and the Figure FM.3.1 -> Figure FM.2.1 in fm-what-this-book-covers.

Notes:
- The image filename `fm-3-1-dependency-diagram.png` was left as-is because the user instructed not to rename files; only the caption text now reads "Figure FM.2.1".
- The fm-who-should-read.html "What Comes Next" originally went to FM.5 directly. Updated to FM.4 (look-inside-preview) to match the actual chapter-nav next-link.
- The look-inside-preview.html "What Comes Next" originally went to FM.3 (fm-what-this-book-covers). Updated to FM.5 (fm-how-to-use) to match chapter-nav.

## 6. Stale chapter count "82 chapters" (fixed)

Three places said "82 chapters"; actual count is 83 (Chapter 0 through Chapter 78 with gaps at 38/39 plus 54b - net 83).

| File | Location | Fix |
|------|---------|-----|
| foreword.html | "The 82 chapters across sixteen parts..." | -> 83 chapters |
| fm-what-this-book-covers.html | "Sixteen parts and 82 chapters trace a single arc..." | -> 83 chapters |
| fm-how-to-use.html | "across 82 chapters" in the Linear callout | -> 83 chapters |

## 7. Stale "three reference appendices" (fixed)

`fm-what-this-book-covers.html` said "three reference appendices" (and H2 "Three Reference Appendices") but the book has 4 appendices (A, B, C, D). Updated:
- H2: "Three Reference Appendices" -> "Four Reference Appendices"
- Meta description: "three appendices" -> "four appendices"
- Body prose: appendices "organized into two groups" -> "three groups", and added the **Behind the Book** description for Appendix D (Agents That Helped to Write This Book) to mirror Foundations and For Instructors groups.

## 8. Stale section reference "Section 0.3" (fixed)

`fm-who-should-read.html` referenced "Section 0.3 teaches PyTorch in 90 minutes" but section 0.3 was split into 0.3a and 0.3b. Updated to "Sections 0.3 and 0.3b".

## 9. Stale Part V chapter descriptions in fm-what-this-book-covers.html (fixed)

Part V description listed chapters by their old titles. Updated:
- "Audio and music" (ch. 20) -> "Audio, music, and video generation (Suno v4, ElevenLabs, Veo 3, Sora 2)"
- "vision-language models" / "unified omni-architectures" (ch. 22) -> "vision-language and unified omni models"
- "vision-language-action models for robotics" (ch. 24) -> "VLA models and LLM-powered robotics"

## 10. Stale Part XIV chapter description (fixed)

In fm-what-this-book-covers.html, Part XIV's manufacturing chapter (ch. 78) was described as just "manufacturing and supply chain" but the chapter is now "Manufacturing, Creative Industries, Search & Recommendation". Updated text to "manufacturing plus creative industries and search/recommendation".

---

## Left as-is

### copyright.html

No chapter or section references; nothing to verify. Trademark list and edition statement are independent of book structure. No bug found; no edits.

### about-authors.html

Author bios reference "Parts III, V, VI, and IX" (Sasha) and "Part XIV" (Yehudit). These are part-level references and remain accurate (all those parts still exist). Per instructions, did not fabricate updates to author bios. No edits.

### Front-matter href integrity

`_audit_fm.py` confirms 0 broken hrefs across all FM files. Every linked module index, section, appendix, and asset resolves to an existing file.

### Toc href integrity

`_audit_toc.py` confirms 0 chapter-num/title/file mismatches after fixes. Every chapter listed in toc resolves to an existing module index.html and every module in the ground truth is listed in toc.

---

## Out of scope but worth flagging (not edited)

- **`index.html`** (book cover/home page) advertises "35 chapters across 11 parts" - extremely stale. Actual: 83 chapters across 16 parts. This is in the homepage, not in the audited file set.
- **Chapter 7 toc title**: "Modern LLM Landscape & Model Internals" matches H1 exactly, but module 07's slug is `modern-llm-landscape`. No problem; just an observation.
- **Part 8 chapter numbering**: Part 8 lists chapters 37, 40, 41 (gaps at 38 and 39). The toc correctly lists only these three. This is intentional structure, not a TOC bug.
- **Module 54b**: Part 11 has both module-54 (Watermarking and Provenance) and module-54b (Transparency and Disclosure). Toc lists both. The aria-label for module-54b reads "Chapter 54: Transparency and Disclosure" which is technically valid but unusual. Left unchanged - matches the existing intentional structure.

---

## Verification

After all edits:

```
/c/Python314/python docs/content-audit/_audit_toc.py
Found 0 TOC mismatch(es).

/c/Python314/python docs/content-audit/_audit_fm.py
Found 0 broken hrefs in FM files.
```

---

## 11. index.html homepage stale counts (fixed, 2026-05-19 follow-up)

The B.7 audit flagged `index.html` (the root book home page) as out of scope but extremely stale. Targeted fix performed:

| Location | Stale claim | Fix |
|----------|------------|-----|
| `<p class="ms-lede">` (line ~739) | "35 chapters across 11 parts, plus 22 framework appendices" | "83 chapters across 16 parts, plus 4 reference appendices" |
| Appendices tile tag (line ~777) | "Appendices A – AF" | "Appendices A – D" |
| Appendices tile title (line ~778) | "28 framework + reference appendices" | "4 reference appendices" |
| Appendices tile body (line ~779) | "Hugging Face, LangChain (with LangGraph, CrewAI, LlamaIndex, Semantic Kernel, DSPy), Docker, vLLM, plus 7 industry guides and 3 cross-cutting reference catalogs." | "Mathematical foundations, course syllabi, reading pathways, and the agent roster behind the book." (mirrors the actual A/B/C/D appendices that exist) |

toc.html re-verified: per-part counts (`6 chapters · 28 sections`, etc.) match the modules on disk. No top-level "X chapters across Y parts" summary present in toc.html, so nothing to update there. Sum of per-part chapter counts in toc = 82, which differs from the ground-truth 83 by exactly the module-54b split (Part XI shows 5 chapters but module-54 plus module-54b account for two listed entries with one shared chapter number). This matches the intentional structure noted in section "Module 54b" above; no toc edit needed.

### Out of scope on index.html (flagged, not edited to avoid fabrication)

The "What You Will Learn" tile grid (lines 743-782) lists only **Parts I–X and XII** (skipping Part XI, with Part numbering that no longer matches the current 16-part toc structure). Each tile body also describes content that maps to an older book skeleton. Fixing this is not a numeric count update; it would require authoring 6 new tiles and rewriting the existing 11 to match the current part titles in toc.html. Flagged here for a separate content-writing pass.
