# Module 36: From Idea to Product Hypothesis

**Audit date**: 2026-05-11
**Sections reviewed**: 36.1, 36.2, 36.3, 36.4, 36.5, 36.6, 36.7, 36.8, 36.9 (9 sections; index advertises only 4)
**Total word count**: ~42,658 (756 index + 41,902 across 9 sections)

## Summary
Module 36 absorbed all of the deleted Module 37 ("Building and Steering AI Products") as sections 36.5 through 36.9 during the v3.x consolidation, but the merge was structurally incomplete. The chapter index only advertises the original 36.1-36.4 cards. All five absorbed sections (36.5-36.9) still have Chapter-37 breadcrumbs, load their images from the now-deleted `module-37-building-steering/images/` directory (broken images), and use h2 numbering from the old Chapter 37 (`37.1.1` etc.). This is the most severely broken chapter in the batch.

## Inconsistencies
- **index.html lines 65-106**: section cards list only 36.1, 36.2, 36.3, 36.4. No cards for 36.5-36.9, even though those files exist and contain ~26,400 words of content (over 60 % of the chapter).
- **index.html line 110**: "What's Next?" says "In the next chapter, Chapter 37: Building and Steering AI Products, you will take your product hypothesis and learn the observe-steer development loop..." — but the observe-steer loop is now **already inside this chapter** as Section 36.5. Stale pointer.
- **index.html line 34 (chapter overview)**: "the thinking that happens before the build loop begins (covered in Chapter 37)". Same stale reference.
- **index.html line 40 (Big Picture)**: "feeding directly into the build loop of Chapter 37 and the shipping decisions of Chapter 38." Chapter 37 does not exist.
- **index.html line 114**: prev nav points to `../../part-9-safety-strategy/module-32-safety-ethics-regulation/section-17.5.html` — this is a malformed path (combines module-32 with section-17.5, neither of which is a coherent destination). Anchor text "AI, Society & Open Problems" suggests it was meant to point at the old Ch 35.
- **All five absorbed sections (36.5, 36.6, 36.7, 36.8, 36.9) line 20**: chapter-label reads `<a href="../module-37-building-steering/index.html">Chapter 37 · Section 36.X</a>` — links to a directory that does not exist on disk (confirmed: no `module-37-building-steering` folder).
- **Section 36.5 line 41**: h2 numbering `37.1.1 What Is Vibe Coding?` — should be `36.5.1` (or similar) under the new chapter.
- **Section 36.4 line 479 (next-nav)**: chains to `../module-37-building-steering/index.html` ("Building and Steering AI Products") — broken link.
- **All five absorbed sections — figure images**: load from `../module-37-building-steering/images/...` (e.g. `vibe-coding-loop.png`, `prototype-loop.png`, `documentation-control.png`, `ai-coding-trust-verify.png`, `prototype-to-mvp.png`). The directory does not exist, so every illustration in 36.5-36.9 is a broken image on the rendered page.
- **index.html part-label** says "Part 11: From Idea to AI Product" (with Arabic numeral "11"); other parts use Roman numerals ("Part IX", "Part X"). Module 38's index uses "Part 11" too — consistent within Part 11 but inconsistent with the rest of the book.
- **index.html line 27**: agent cite is "Compass, Cost Conscious AI Agent" but uses `chinchilla.png` for the avatar — Compass is normally `compass.png`. Avatar/character mismatch.
- **section-36.5.html line 26**: epigraph agent is "Deploy, Relentlessly Iterative AI Agent" using `dropout.png` avatar — different character image than the index.

## Gaps
- Index Learning Outcomes (lines 45-51) only enumerate hypothesis/feasibility skills. Skills from absorbed sections (Observe-Steer Loop, IEB, Founder's Prototype Loop, Documentation as Control Surface, AI Coding Trust-but-Verify, Prototype-to-MVP bridge) are entirely missing.
- Index prereqs (lines 56-61) list only Ch 10, 11, 33 + Python — missing prereqs for the absorbed dev-loop content (e.g. Chapter 29 evaluation, Git).
- No chapter-level bibliography spanning hypothesis + build content; bibliographies in 36.5-36.9 still reference the Ch 37 framing.
- Cross-references between original (36.1-36.4) and absorbed (36.5-36.9) sections are sparse — readers won't see hypothesis → build → MVP as one arc; it reads as two stitched-together chapters.
- Section 36.9 ("From Prototype to MVP") is a strong natural lead-in to Chapter 38 but does not link to 38.1 explicitly in any "What Comes Next" pointer.

## Errors
- **index.html line 114 prev href**: `../../part-9-safety-strategy/module-32-safety-ethics-regulation/section-17.5.html` is a 404 (mixes ch 32 path with ch 17 filename).
- **All 5 absorbed sections**: `<a href="../module-37-building-steering/index.html">` chapter-label is a 404.
- **All 5 absorbed sections**: `<img src="../module-37-building-steering/images/*.png">` are all 404s — visible as broken-image icons or alt-text-only on the rendered page. Confirmed via filesystem check.
- **Section 36.5 line 41**: h2 says `37.1.1` — wrong chapter number.
- **Section 36.9 line 507, Section 36.8 line 527, Section 36.7 line 603, Section 36.6 line 419, Section 36.5 lines 441-442**: footer up-nav links all point to `../module-37-building-steering/index.html`. All 404s.
- The `additional-illustrations.json` and `new-illustrations.json` files at the part level still target the `module-37-building-steering/` output path — content generation pipeline will keep regenerating images into a non-existent folder unless these are updated.
- **Section 36.5 line 20 chapter-label inner text**: "Chapter 37 · Section 36.5" — even if the link were repaired, the label text itself is wrong.

## Improvements
- Add cards for sections 36.5-36.9 to the chapter index, expand the Learning Outcomes and Prereqs lists, and rewrite the "What's Next?" pointer to chain directly to Chapter 38.
- Bulk find-and-replace `../module-37-building-steering/` with the correct in-chapter image path (move images from the (defunct) module-37 folder into `module-36-idea-to-product/images/` and update all references).
- If the module-37 images were never created on disk, regenerate them via `additional-illustrations.json` / `new-illustrations.json` after fixing the output paths.
- Renumber h2 headings inside 36.5-36.9 from `37.x.y` to `36.5.y`, `36.6.y`, etc.
- Repair the prev/next/up nav links in all five absorbed sections to point at `module-36-idea-to-product/index.html` and at sibling sections within 36.
- Replace the broken `section-17.5.html` prev link on the index with the correct prior chapter (Ch 34 last section: `module-34-emerging-architectures/section-34.10.html`).
- Reconcile Compass-vs-Deploy agent imagery and bios across the chapter; pick one Compass avatar (the index says `chinchilla.png` while elsewhere in the book the agent file is `compass.png`).
- Standardise "Part XI" Roman numeral or "Part 11" Arabic numeral with the rest of the book (the book mostly uses Roman).

## One-thing-only fix
Fix `../module-37-building-steering/` references across 36.5-36.9. The directory does not exist, which means every figure in five long sections renders as a broken image and every breadcrumb/up-link is a 404. This single repair (move the images into module-36 and bulk-rewrite the paths) restores the chapter to a readable state; the other issues (index cards, h2 numbering, learning-outcomes list) can follow.
