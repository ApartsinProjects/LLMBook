# Module 33: LLM Strategy, Product Management & ROI

**Audit date**: 2026-05-11
**Sections reviewed**: 33.1, 33.2, 33.3, 33.4, 33.5, 33.6, 33.7 (7 actual section files; index advertises 8 sections 33.1-33.8)
**Total word count**: ~53,721 (1,003 index + 52,718 across 7 sections)

## Summary
Substantively the chapter is solid — practical frameworks (Four-Pillar readiness, ROI models, vendor scorecards, build-vs-buy, enterprise integration patterns, token economics). However the v3 deletion of the original 33.6 ("Build vs Buy duplicate") was only partially completed: the index still lists eight cards and the renumbering of 33.6 → "Enterprise Integration" and 33.7 → "Economic Design" was not propagated. Multiple cards point to the wrong files, several h2 headings are off-by-one, and the opening epigraph of 33.1 contains a stray cross-reference token.

## Inconsistencies
- **index.html lines 91-173**: index lists 8 cards (33.1 through 33.8) but only 7 actual section files exist. The mapping is broken:
  - "33.6 Build vs. Buy Decision Framework & TCO" card href = `section-33.4.html` (which is actually "LLM Vendor Evaluation & Build vs. Buy"). This appears to be the leftover phantom card the user mentioned.
  - "33.7 Enterprise Integration Patterns" card href = `section-33.6.html` (correct content, wrong number-to-file mapping).
  - "33.8 Economic Design of LLM Systems" card href = `section-33.7.html` (correct content, wrong number-to-file mapping).
- **section-33.1.html line 25 epigraph**: "Strategy without execution is a Section 32.2. Execution without strategy is a very expensive hallucination." — `Section 32.2` is a stray cross-reference placeholder that survived a find/replace; the original text presumably was "Strategy without execution is a hallucination."
- **section-33.6.html line 42**: h2 headings start at `33.7.1 Identity Integration for LLM Applications` — file is named 33.6 and chapter heading is "Enterprise Integration Patterns" but sub-heading numbering reflects the OLD plan where this section was 33.7.
- **section-33.6.html line 49**: figure caption "Figure 33.6.1" is correct, but earlier alt text says "fig-33.7.1-enterprise-auth-flow.png" (filename uses 33.7, caption uses 33.6) — image filename mismatch.
- **section-33.7.html (Economic Design)**: not yet directly inspected for h2 numbering, but by analogy probably has `33.8.x` h2 numbering inside a file labeled 33.7 — needs verification.
- **index.html line 7 / line 18**: title says "LLM Strategy, Product Management & ROI" but the part-label calls it "Part IX: Safety & Strategy"; not wrong, but the chapter overview prose (lines 35-49) frames the chapter as the product/business bridge, not safety.
- **index.html line 180**: prev nav points to `module-32-safety-ethics-regulation/section-32.11.html` ("Federated Learning for LLMs") — actual content of 32.11 is "Privacy Attacks & DP" (the FL section was merged in but is not the page title). Mismatched link text.
- **index.html line 177**: "What's Next?" says "Part X: Frontiers" — fine, but the chapter ordering after 33 includes the moved Module 18 (which is now in Part 10 alongside 34); index should at least mention that.
- **section-33.1.html line 27 epigraph cite**: agent name is "A Strategic Compass, Execution-Obsessed AI Agent" but on the chapter index (line 24) the same character is "Compass, Strategically Impatient AI Agent". Bio drift inside the chapter.

## Gaps
- The chapter overview promises "build-versus-buy decision trees that account for total cost of ownership over 12 to 36 months" (objective line 68), but with the original 33.6 card removed, this content lives only inside 33.4. Readers searching the index for "TCO" / "Build vs Buy" will see a card pointing to the wrong file.
- Section 33.7 (Economic Design, the actual file) does not cross-reference Chapter 32's environmental impact section (32.10) even though token-economics + carbon footprint is a natural pairing.
- No prereq link to Module 18 (interpretability) even though "interpretability for production debugging" came up in 32 and could inform 33's vendor evaluation.
- Section 33.5 (Compute Planning) lists GPU tiers A100/H100/L40S — the 2026-edition would benefit from a reference to B200 (mentioned in Module 32's compute-governance section).
- Section 33.6 (Enterprise Integration) is dense on auth + RBAC; a callout connecting it to Section 32.5 ("Risk Governance & Audit") would close a real-world loop.

## Errors
- **section-33.1.html line 25**: stray "Section 32.2" placeholder in epigraph text (not a hyperlink, just literal words). Reads as a copy-paste leak.
- **index.html lines 144, 154, 164**: hrefs in 33.6/33.7/33.8 cards are off-by-one relative to the file inventory; clicking 33.6 sends the reader to the 33.4 page.
- **section-33.6.html line 42-onwards**: h2 numbering scheme `33.7.x` does not match its containing file/section number `33.6`. Will confuse readers who try to cite a sub-section.
- **section-33.6.html line 48**: image filename `fig-33.7.1-enterprise-auth-flow.png` vs caption "Figure 33.6.1" — pick one.
- The chapter prereq list (index lines 80-86) still includes "Chapter 32" as a prereq labeled "Safety, Ethics, and Regulation" — the v3 restructure may have changed Ch 32's section count but not its number; verify.

## Improvements
- Delete the phantom `33.6` card (the duplicate Build-vs-Buy one) from the index, then renumber the remaining cards 33.6 = Enterprise Integration, 33.7 = Economic Design with correct hrefs.
- Renumber the h2 headings inside `section-33.6.html` and `section-33.7.html` to `33.6.x` / `33.7.x` respectively, and update any image filenames to match.
- Fix the 33.1 epigraph stray "Section 32.2" — remove or replace with intended text.
- Add a single Compass agent-bio reference and use it consistently across index + sections.
- Add cross-reference from 33.7 (Economic Design) to 32.10 (Environmental Impact / Green AI) for token-cost + carbon pairing.
- Verify 33.5 GPU list against 2026 hardware mention in Module 32 (B200, H200) and reconcile.

## One-thing-only fix
Remove the phantom 33.6 "Build vs. Buy / TCO" card from the index, renumber cards 33.6/33.7 to match the actual files (Enterprise Integration, Economic Design), and propagate the same numbering into the h2 headings of `section-33.6.html` (currently `33.7.x`). This single correction restores TOC navigation and stops readers from landing on the wrong page when they click "Build vs. Buy".
