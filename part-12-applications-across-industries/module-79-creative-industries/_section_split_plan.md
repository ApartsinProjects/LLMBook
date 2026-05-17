# Chapter 58 (Creative Industries) - Section Split Plan

## Audit status
- Existing sections: 2
  - `section-58.1.html`: "Music, Video, Design & Marketing Copy" - **~1,743 words, 4 modern h2 (58.1.x)**
  - `section-58.2.html`: "Education, Legal & Creative Industries" - **~5,711 words, legacy 27.6.x content covering many off-topic areas**
- `index.html` body: 482 words (mostly TOC; some intro)
- Pattern: **Hybrid: keep + split 58.1; retire 58.2 (off-topic for this chapter)**
- Effort: ~4-5 hours

## Plan: split 58.1 into per-medium sections + retire 58.2

### Split `section-58.1.html` into 4-5 medium-specific sections

| New file              | Title                                                  | Source                |
| --------------------- | ------------------------------------------------------ | --------------------- |
| `section-58.1.html`   | Image and Design Tools (Firefly, Midjourney, Canva)    | 58.1.1                |
| `section-58.2.html`   | Video Generation (Runway, Pika, Sora) & Production     | 58.1.2                |
| `section-58.3.html`   | Music and Audio (Suno, Udio, ElevenLabs)               | 58.1.3                |
| `section-58.4.html`   | Marketing Copy and Brand Voice                         | 58.1.4                |
| `section-58.5.html`   | Workflow Patterns & Rights/Licensing (new content)     | NEW - extract from 58.2 + write fresh |

### Fate of legacy `section-58.2.html`
Current 58.2 covers Education, Legal, Customer Support, Gaming, Style Transfer, GEC, Data-to-Text. The Education/Legal parts belong in Ch 54/51; Style Transfer/GEC/Data-to-Text belong in Part-7 (Multimodal Generation). Recommend:
1. **Migrate** Creative-Writing/Co-Authorship + Customer Support/Gaming content -> new `section-58.5.html`.
2. **Cross-link** the misfiled topics to their proper chapters (51, 54, Part 7).
3. **Delete** `section-58.2.html`.

## Steps
1. Split 58.1's 4 medium sub-sections into 4 dedicated sections.
2. Write fresh `section-58.5.html` on creative-workflow patterns + rights/licensing.
3. Migrate creative-writing/co-authorship from 58.2 into 58.5.
4. Cross-link misfiled topics to their canonical chapters.
5. Delete `section-58.2.html`; update `book_structure.yaml`.
