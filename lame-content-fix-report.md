# Lame Content Fix Report, May 2026

Applied recommendations from `lame-content-audit.md` across Tools-of-the-Trade chapters and `appendix-p`.

## Stripped (Comparing-X tables + table wrappers + h2 heading)

| File | Sub-section dropped |
|---|---|
| `part-1-foundations/module-06-tools-of-the-trade/section-6.1.html` | 6.1.4 Comparing the platforms |
| `part-1-foundations/module-06-tools-of-the-trade/section-6.2.html` | 6.2.4 Comparing the engines |
| `part-1-foundations/module-06-tools-of-the-trade/section-6.5.html` | 6.5.4 Comparing the reading sources |
| `part-2-understanding-llms/module-12-tools-of-the-trade/section-12.2.html` | 12.2.4 Comparing the tokenizer libraries |
| `part-2-understanding-llms/module-12-tools-of-the-trade/section-12.5.html` | 12.5.5 Comparing the tracking sources |
| `part-3-working-with-llms/module-16-tools-of-the-trade/section-16.5.html` | 16.5.5 Comparing the venues |
| `part-4-training-adapting/module-21-tools-of-the-trade/section-21.1.html` | 21.1.4 Comparing the platforms |
| `part-4-training-adapting/module-21-tools-of-the-trade/section-21.2.html` | 21.2.4 Comparing the libraries |
| `part-4-training-adapting/module-21-tools-of-the-trade/section-21.5.html` | 21.5.4 Comparing the venues |
| `part-5-retrieval-conversation/module-25-tools-of-the-trade/section-25.1.html` | 25.1.3 Comparing the platforms |
| `part-5-retrieval-conversation/module-25-tools-of-the-trade/section-25.2.html` | 25.2.4 Comparing the libraries |
| `part-5-retrieval-conversation/module-25-tools-of-the-trade/section-25.5.html` | 25.5.4 Comparing the venues |
| `part-7-multimodal-generation/module-33-tools-of-the-trade/section-33.1.html` | 33.1.4 Comparing the platforms |
| `part-7-multimodal-generation/module-33-tools-of-the-trade/section-33.2.html` | 33.2.4 Comparing the libraries |
| `part-7-multimodal-generation/module-33-tools-of-the-trade/section-33.5.html` | 33.5.4 Comparing the venues |
| `part-8-evaluation-production/module-36-tools-of-the-trade/section-36.1.html` | 36.1.4 Comparing the platforms |
| `part-8-evaluation-production/module-36-tools-of-the-trade/section-36.2.html` | 36.2.4 Comparing the libraries |
| `part-8-evaluation-production/module-36-tools-of-the-trade/section-36.4.html` | 36.4.3 Comparing the options |
| `part-8-evaluation-production/module-36-tools-of-the-trade/section-36.5.html` | 36.5.4 Comparing the venues |
| `part-10-idea-to-product/module-50-tools-of-the-trade/section-50.1.html` | 50.1.5 Comparing the platforms |
| `part-10-idea-to-product/module-50-tools-of-the-trade/section-50.2.html` | 50.2.4 Comparing the libraries |
| `part-10-idea-to-product/module-50-tools-of-the-trade/section-50.3.html` | 50.3.3 Comparing the resources |
| `part-10-idea-to-product/module-50-tools-of-the-trade/section-50.4.html` | 50.4.3 Comparing the models in context |
| `part-10-idea-to-product/module-50-tools-of-the-trade/section-50.5.html` | 50.5.4 Comparing the venues |
| `part-11-applications-across-industries/module-60-tools-of-the-trade/section-60.1.html` | 60.1.6 Comparing the verticals |
| `part-11-applications-across-industries/module-60-tools-of-the-trade/section-60.2.html` | 60.2.5 Comparing the libraries |
| `part-11-applications-across-industries/module-60-tools-of-the-trade/section-60.5.html` | 60.5.3 Comparing the venues |
| `part-12-frontiers/module-65-tools-of-the-trade/section-65.1.html` | 65.1.5 Comparing the platforms |
| `part-12-frontiers/module-65-tools-of-the-trade/section-65.2.html` | 65.2.4 Comparing the libraries |
| `part-12-frontiers/module-65-tools-of-the-trade/section-65.5.html` | 65.5.4 Comparing the venues |

## Also stripped: filler intros and transition closings
- Trimmed two-paragraph chapter-intro filler in 6.2, 6.5, 12.1, 12.2, 12.5
- Removed closing "Section X.Y picks up Z" transition prose from 6.1, 6.2, 6.3, 6.4, 6.5, 12.1, 12.2, 12.3, 12.4, 12.5 (graduation-speech "What comes next" closing also dropped), 16.2, 16.3, 16.4
- Dropped intro filler paragraphs in 33.5, 50.1, 50.4 (rewrote to one sentence), 60.1, 60.4, 60.5 (trimmed), 65.1, 65.2, 65.3, 65.4 (filler cut), 65.5 (filler cut)
- Rewrote 50.3 intro from "Part X is unusually light..." apology to positive framing
- Promoted "When your app fails at 2 AM" filler sentence in 16.5 inside the Status & incident pages section as an opener
- Replaced "Welcome to the working day" graduation-speech callout in 65.5 with a concrete "Three papers to read first" recommendation
- Dropped redundant "Reading discipline scales" key-insight callout in 12.5

## Preserved (KEEP) tables
- 16.4.4 API-callable model lineup (explicit user exception)
- 6.3.3, 6.4.4 (kept; dropped redundant "Best for" column in 6.4.4)
- 12.1.4, 12.3.3, 12.4.4 (price/size/context data)
- 16.2.5, 16.3.4 (Layer/Format/Judge framing carries data)
- 21.3.4, 21.4.3 (size + license)
- 25.3.4, 25.4.4 (caveat / access info)
- 33.3.4, 33.4.4 (scale + speed-focused col)
- 36.3.4 (Status-in-2026 col)
- 60.3.3, 60.4.2 (frontier score, analytical Notes col)
- 65.3.3, 65.4.4 (frontier score, distinctive Notes col)

## Appendix P bug fixes
- Pathway 7 line 147 (now 143 after edit): fixed mislabeled "FM.7 Copyright & Legal(Course Syllabi)" to "FM.7 Copyright & Legal" and corrected link to `../front-matter/copyright.html`
- Pathway 8 line 162: removed the orphan bullet `<li> · 1 hr <em>(read the 5 unifying theses and 3 tensions)</em></li>` (no matching content found anywhere in book/front-matter)

## Note
- Section 16.1 remains a TODO scaffold ("TODO author this section..."). Out of scope for a strip pass; left as-is.
- The Comparing-X drop excluded Part 6 (module 30) and Part 9 (module 39) per the user's explicit scope, even though the audit covered them.
- Module 64 Comparing subsections were not touched (out of scope).
