# Task Registry

> **Purpose**: Persistent task tracking that survives context window compactions.
> **Rule**: Every task requested by the user MUST be logged here before work begins.
> **Update protocol**: Mark status changes immediately. Never delete completed tasks (move to Archive).

## Active Tasks

### TASK-002: Illustration coverage expansion
- **Status**: IN_PROGRESS (audit complete, generation pending)
- **Priority**: MEDIUM
- **Description**: Full illustration audit completed 2026-03-29. Found 91 opportunities (47 HIGH, 30 MEDIUM, 5 LOW). Worst gaps: Modules 3-5 (zero illustrations), Parts 9-10 (zero section-level illustrations).
- **Requested**: 2026-03-28
- **Audit**: See ILLUSTRATION_OPPORTUNITIES.md for full report with prompts, captions, and priorities.
- **Next step**: Generate illustrations using Gemini image generation skill, starting with Batch 1 (Modules 3-5).

### TASK-006: SVG rebuild (worst quality)
- **Status**: PENDING
- **Priority**: MEDIUM
- **Description**: Rebuild 13 worst-quality SVGs identified by diagnostic sweep. Apply mandatory visual polish standards.
- **Requested**: 2026-03-28

### TASK-008: Compact all agent skills (Meta Agent pass)
- **Status**: PENDING
- **Priority**: LOW
- **Description**: Make all 42+ agent skill files denser without losing instructions.
- **Requested**: 2026-03-28

### TASK-011: SVG quality and correctness improvement
- **Status**: PENDING
- **Priority**: HIGH
- **Description**: Systematic approach to increase quality and correctness of all SVG diagrams/graphs/figures across the book.
- **Requested**: 2026-03-28

### TASK-025: Rebuild 13 worst-quality SVGs
- **Status**: PENDING
- **Priority**: MEDIUM
- **Description**: Manually redesign the 13 worst-quality SVGs identified by prior diagnostic sweep. Apply full visual polish standards (gradients, shadows, rounded corners, good typography, annotation lines).
- **Requested**: 2026-03-28

### TASK-026: SVG dashed annotation lines sweep
- **Status**: PENDING
- **Priority**: LOW
- **Description**: Add dashed stroke annotation lines where labels point to diagram elements. Currently 250 instances exist; many SVGs with labels lack connecting lines.
- **Requested**: 2026-03-28

### TASK-085: Meta agent skills update
- **Status**: PENDING
- **Priority**: LOW
- **Description**: Review and update agent skill files based on recent requests. Keep skills general for future books.
- **Requested**: 2026-03-28

### TASK-110: Illustration generation (remaining batches)
- **Status**: PENDING
- **Priority**: MEDIUM
- **Description**: Generate illustrations for Batches 2-4 from ILLUSTRATION_OPPORTUNITIES.md. Batch 1 (Modules 3-5, 14 illustrations) complete. Remaining: Batch 2 (Parts 9-10, 8 HIGH), Batch 3 (Chapters 20, 22, 24), Batch 4 (scattered gaps Parts 4-8).
- **Requested**: 2026-03-29

### TASK-115: Missing illustration images (146 placeholders)
- **Status**: PENDING (blocked on TASK-110)
- **Priority**: MEDIUM
- **Description**: 146 img tags reference images that don't exist on disk, across 83 files. Concentrated in Parts 3-7 (modules 08-26). These are illustration placeholders added to HTML but never generated. Requires Gemini image generation.
- **Requested**: 2026-03-29

### TASK-117: Deep philosophical key-insight sweep
- **Status**: DONE
- **Priority**: MEDIUM
- **Description**: Add thought-provoking key-insight callouts connecting concepts to information theory, cognitive science, physics, economics, etc. Targeting Parts 1-6.
- **Requested**: 2026-03-29
- **Completed**: 2026-03-29
- **Result**: Only 1 section (25.4) was missing a key-insight across Parts 2-10. Added. All main chapter sections now have key-insight callouts.

### TASK-120: Python library code examples sweep (round 2)
- **Status**: DONE
- **Priority**: MEDIUM
- **Description**: Fresh sweep for library code snippets covering tiktoken, datasets, accelerate, bitsandbytes, peft, vllm, guidance, ragas, chromadb, sentence-transformers, unsloth, mergekit, dspy, instructor, litellm, etc.
- **Requested**: 2026-03-29
- **Completed**: 2026-03-29
- **Result**: 1 deprecated OpenAI API updated (GPTCache), 2 LangChain imports fixed, ~100 code blocks retagged to correct language, 2 pip instructions updated.

### TASK-123: Code syntax highlighting (Prism.js/highlight.js)
- **Status**: IN_PROGRESS
- **Priority**: MEDIUM
- **Description**: Add JS-based syntax highlighting for all 726+ code blocks. Auto-colors Python, bash, JSON, SQL, YAML, JS, HTML. Local bundle in vendor/, single source of truth.
- **Requested**: 2026-03-29

### TASK-124: Connecting prose between consecutive math blocks
- **Status**: DONE
- **Completed**: 2026-03-29
- **Result**: 8 prose passages added across 7 files bridging consecutive math blocks.
- **Priority**: MEDIUM
- **Description**: 21 consecutive math-block pairs in 9 files have no connecting text. Adding brief explanatory phrases between formulas.
- **Requested**: 2026-03-29

### TASK-128: Short TOC redesign (compact, matching long TOC style)
- **Status**: IN_PROGRESS
- **Priority**: HIGH
- **Description**: Make short TOC more compact and readable, matching dense style of long/detailed TOC. Card-based layout felt too spacious.
- **Requested**: 2026-03-29

### TASK-129: Cover page animations (reproduce earlier version)
- **Status**: PENDING
- **Priority**: MEDIUM
- **Description**: Earlier sessions had cover with "magic book aesthetic, star burst animation, floating motes, Easter egg hover animations on key terms (engineers, researchers, leaders)". Current cover has basic particle animation. Need to enhance with richer animations.
- **Requested**: 2026-03-29

### TASK-130: Caption numbering standardization
- **Status**: IN_PROGRESS
- **Priority**: HIGH
- **Description**: All code captions use bare "Code Fragment 1:" instead of section-aligned "Code Fragment 4.2.1:". Standardize across all 250+ pages.
- **Requested**: 2026-03-29

### TASK-131: Non-standard callout titles fix
- **Status**: IN_PROGRESS
- **Priority**: MEDIUM
- **Description**: 14 instances in 9 files use bare <strong> instead of <div class="callout-title"> for callout titles.
- **Requested**: 2026-03-29

## Archive (Completed)

### TASK-C01: Fix Figure 0.1.1 global minima position
- **Completed**: 2026-03-28
- **Description**: Global min dot was at (455,272) on upslope; moved to (424,285) at valley bottom.

### TASK-C02: Glossary split (Appendix F)
- **Completed**: 2026-03-28
- **Description**: Split monolithic glossary into 5 categorized section files.

### TASK-C03: Callout icon CSS integration
- **Completed**: 2026-03-28
- **Description**: 10 PNG icons wired into CSS, 1643 HTML entity icons removed.

### TASK-C04: Caption quality fix
- **Completed**: 2026-03-28
- **Description**: Fixed 29 files with "Chapter opener illustration for..." captions.

### TASK-C05: Lab CSS rules
- **Completed**: 2026-03-28
- **Description**: Added lab-objective, lab-skills, lab-prereqs, lab-steps, lab-expected, lab-stretch, lab-solution CSS.

### TASK-C06: Parts 7-10 restructuring
- **Completed**: 2026-03-28
- **Description**: Reorganized from 7 to 10 parts.

### TASK-C07: Helper script archival
- **Completed**: 2026-03-28
- **Description**: Moved 20+ scripts to _scripts_archive/.

### TASK-C08: Wide layout fix (170+ files)
- **Completed**: 2026-03-28
- **Description**: Moved elements inside .content wrapper.

### TASK-C09: Book title bar addition
- **Completed**: 2026-03-28
- **Description**: Added .book-title-bar to 283 files.

### TASK-C10: Short ToC direct links
- **Completed**: 2026-03-28
- **Description**: Changed short ToC hrefs from #anchors to chapter page URLs.

### TASK-C11: Module namespace collision cleanup
- **Completed**: 2026-03-28
- **Description**: 9 directories renamed, 49 section files renamed, 94 HTML files updated, 4 duplicate dirs removed.

### TASK-C12: ToC and indices update post-restructure
- **Completed**: 2026-03-28
- **Description**: toc.html verified correct 10-part/36-chapter structure. Chapter count fixed. Header-nav added to all 249 files.

### TASK-C13: Integrate 11 lab fragments
- **Completed**: 2026-03-28
- **Description**: All 11 lab fragments integrated into their respective chapter section files.

### TASK-C14: Standardize all 24 labs to template
- **Completed**: 2026-03-28
- **Description**: 24 labs standardized with all 7 required sub-elements.

### TASK-C15: BOOK_CONFIG.md update
- **Completed**: 2026-03-28
- **Description**: Chapter map updated to 10-part/36-module structure. Batch partitioning expanded to 10 batches.

### TASK-C16: Footer standardization
- **Completed**: 2026-03-28
- **Description**: All 58 index page footers standardized. CSS footer rule added.

### TASK-C17: Standardization sweep (classes, CSS, repeating elements)
- **Completed**: 2026-03-28
- **Description**: book.css is single source of truth. All structural elements standardized. CONFORMANCE_CHECKLIST.md updated.

### TASK-C18: Callout icon tooltips (TASK-012)
- **Completed**: 2026-03-29
- **Description**: 231 files updated, all 10 callout types now have title attributes with descriptive tooltips.

### TASK-C19: Introduction split
- **Completed**: 2026-03-28
- **Description**: Broke monolithic 670-line introduction.html into 3 pages with redirects.

### TASK-C20: CSS class mismatch sweep
- **Completed**: 2026-03-28
- **Description**: 167 fixes across 50 files: class renames, inline style removal, CSS definitions added.

### TASK-C21: Duplicate content/caption sweep
- **Completed**: 2026-03-28
- **Description**: Found 3 duplicate consecutive code-captions; fixed. 674 code blocks (90.6%) lacked captions.

### TASK-C22: Add captions to uncaptioned code blocks
- **Completed**: 2026-03-28
- **Description**: Parts 1-6 complete, 163+ captions added across files with zero code-captions.

### TASK-C23: Write 15 Tier-1 content gaps
- **Completed**: 2026-03-28
- **Description**: 13 of 15 items already existed. Section 10.5 and arena evaluation written. All Tier-1/Tier-2 expansions verified present.

### TASK-C24: Flesh out 5 skeleton sections in Parts 8-10
- **Completed**: 2026-03-28
- **Description**: 5 sections fleshed out, 3046 lines of content written.

### TASK-C25: Part VII application content scouting
- **Completed**: 2026-03-29
- **Description**: 11 production tips, 7 practical examples, 1 code example added across 11 section files in Chapters 27-28.

### TASK-C26: Standardize all page headers
- **Completed**: 2026-03-28
- **Description**: 241 files processed, inline styles removed, headers merged. Single source of truth for header structure.

### TASK-C27: Footer design and standardization (TASK-016)
- **Completed**: 2026-03-28
- **Description**: 46 index pages + section pages standardized. CSS footer rule in book.css.

### TASK-C28: Callout icon tooltips (TASK-017)
- **Completed**: 2026-03-28
- **Description**: 12 box types have Gemini-generated PNG icons and CSS tooltips.

### TASK-C29: Content scouting (Parts 1-6)
- **Completed**: 2026-03-28
- **Description**: CONTENT_UPDATE_PLAN.md created with 15 Tier-1 and additional Tier-2/3 items.

### TASK-C30: Big-picture callout coverage
- **Completed**: 2026-03-28
- **Description**: All 58 index pages covered with big-picture callouts.

### TASK-C31: Orphan/misspelled callout class cleanup
- **Completed**: 2026-03-28
- **Description**: 7 instances of key-idea to key-insight fixed in module-01/lecture-notes.html.

### TASK-C32: Part+chapter index page standardization
- **Completed**: 2026-03-28
- **Description**: 46 files modified (10 part + 36 chapter index pages). 200 inline styles removed.

### TASK-C33: Chapter/section listing format standardization
- **Completed**: 2026-03-28
- **Description**: CSS single source of truth for .sections-list/.section-card and .chapter-card. Content order standardized.

### TASK-C34: Callouts-inside-li width fix
- **Completed**: 2026-03-28
- **Description**: 4 files fixed. Fun-note callouts moved between split sections-list blocks.

### TASK-C35: Appendix standardization sweep
- **Completed**: 2026-03-28
- **Description**: All 10 appendices standardized. Appendices A+B split into 9 sections.

### TASK-C36: Stale duplicate directory cleanup
- **Completed**: 2026-03-28
- **Description**: Deleted stale module-23-multi-agent-systems/ directory.

### TASK-C37: Tier-2 content additions (20 items)
- **Completed**: 2026-03-28
- **Description**: All 20 items verified present: RAG vs long context, speech-to-speech, MCP, SWE-bench, GaLore, and more.

### TASK-C38: Tier-3 content additions (18 items)
- **Completed**: 2026-03-29
- **Description**: 16/18 already present. 2 added: late chunking in section-18.4, AI content detection in section-23.1.

### TASK-C39: Split 9 appendices into section files and expand content
- **Completed**: 2026-03-28
- **Description**: 9 section files created from appendices A+B split.

### TASK-C40: Research-frontier callout sweep
- **Completed**: 2026-03-28
- **Description**: Parts 1-4 complete with research-frontier callouts.

### TASK-C41: Em dash removal + terminology cleanup
- **Completed**: 2026-03-28
- **Description**: 110 "module" to "chapter" replacements across 56 files. Zero em dashes in prose text.

### TASK-C42: Level badge sweep
- **Completed**: 2026-03-28
- **Description**: 56 badges added across 51 files for h2 headings in section pages.

### TASK-C43: Post-restructure content consolidation
- **Completed**: 2026-03-28
- **Description**: Section 11.5 deduplicated; other sections verified clean.

### TASK-C44: Update CROSS_REFERENCE_MAP.md
- **Completed**: 2026-03-28
- **Description**: Replaced "proposed" references with actual renumbered section numbers.

### TASK-C45: Update README.md
- **Completed**: 2026-03-28
- **Description**: Updated module count, part table, directory tree, agent count, terminology.

### TASK-C46: Archive remaining root Python scripts
- **Completed**: 2026-03-28
- **Description**: 8 scripts moved to _scripts_archive/.

### TASK-C47: Apply Part 1 Quick Wins
- **Completed**: 2026-03-28
- **Description**: All 20 specific small fixes from part-1-foundations/QUICK-WINS.md applied.

### TASK-C48: Part 1 Master Improvement Plan
- **Completed**: 2026-03-28
- **Description**: All Tier-1 improvement items completed (information theory, Adam/AdamW, LSTM gates, etc.).

### TASK-C49: Build capstone project content
- **Completed**: 2026-03-28
- **Description**: Capstone project content written for capstone/ directory.

### TASK-C50: Broken internal link sweep
- **Completed**: 2026-03-28
- **Description**: 607 of 623 broken links fixed. 16 remaining are forward refs to unwritten sections.

### TASK-C51: Remove practical-example callouts from chapter index pages
- **Completed**: 2026-03-28
- **Description**: 107 practical-example callouts removed from 29 index.html files.

### TASK-C52: Appendix title renaming
- **Completed**: 2026-03-29
- **Description**: 7 titles improved, 3 standardized. All cross-refs updated.

### TASK-C53: Write labs for chapters with no lab coverage
- **Completed**: 2026-03-28
- **Description**: 4 new labs written for Ch 5, 6, 22, 26.

### TASK-C54: Update LAB_AUDIT.md for renumbered chapters
- **Completed**: 2026-03-28
- **Description**: LAB_AUDIT.md updated with current chapter numbering.

### TASK-C55: SVG stroke-linecap sweep
- **Completed**: 2026-03-28
- **Description**: 1,294 stroke-linecap="round" additions across 154 files.

### TASK-C56: SVG small font fix sweep
- **Completed**: 2026-03-28
- **Description**: 1,085 fonts bumped to 11px minimum for readability.

### TASK-C57: SVG font-family standardization
- **Completed**: 2026-03-28
- **Description**: 1,467 text elements standardized to Segoe UI, system-ui, sans-serif.

### TASK-C58: Wrap bare SVGs in diagram-container
- **Completed**: 2026-03-28
- **Description**: 12 SVGs updated across 3 files with diagram-container wrappers and captions.

### TASK-C59: SVG gradient enrichment
- **Completed**: 2026-03-28
- **Description**: 151 SVGs enriched with gradients, lifting from ADEQUATE to GOOD quality.

### TASK-C60: SVG drop shadow enrichment
- **Completed**: 2026-03-28
- **Description**: 185 SVGs enriched with drop shadows for depth.

### TASK-C61: SVG text overlap detection
- **Completed**: 2026-03-28
- **Description**: 95 warnings found, most intentional split labels. section-18.1 flagged for manual review.

### TASK-C62: SVG figure numbering consistency
- **Completed**: 2026-03-28
- **Description**: 214 captions numbered consistently in "Figure X.Y.Z:" format.

### TASK-C63: SVG y-axis correctness audit
- **Completed**: 2026-03-28
- **Description**: Zero errors found across all SVGs with axes/charts.

### TASK-C64: Header inline style removal sweep
- **Completed**: 2026-03-28
- **Description**: 2 remaining inline styles removed from lecture-notes.html and toc.html.

### TASK-C65: Integrate book-title-bar into header
- **Completed**: 2026-03-28
- **Description**: 249 files updated. New .header-nav with book title link + Contents button.

### TASK-C66: Content order standardization (chapter index pages)
- **Completed**: 2026-03-28
- **Description**: 30 chapter indices reordered. Canonical order codified in CONFORMANCE_CHECKLIST.md.

### TASK-C67: Visible hyperlink styling
- **Completed**: 2026-03-28
- **Description**: CSS rule for .content a with subtle underline, hover highlight. Nav/card links excluded.

### TASK-C68: Responsive CSS enhancement
- **Completed**: 2026-03-28
- **Description**: Enhanced tablet/mobile/print rules at 1024px, 768px, 480px breakpoints.

### TASK-C69: Header-nav ToC link fix
- **Completed**: 2026-03-28
- **Description**: 243 files fixed with correct ToC links.

### TASK-C70: ToC compaction
- **Completed**: 2026-03-28
- **Description**: Legend, badges, labs removed; collapsed view; 820px width.

### TASK-C71: Deep drift sweep
- **Completed**: 2026-03-28
- **Description**: Links, badges, and orphans all verified/fixed across entire book.

### TASK-C72: Module index page sweep
- **Completed**: 2026-03-28
- **Description**: All callouts, links, epigraphs, and prereqs standardized across index pages.

### TASK-C73: Nested anchor tag fix in section cards
- **Completed**: 2026-03-28
- **Description**: 35 fixes across 15 files for invalid nested anchor elements.

### TASK-C74: Fun-note icon titles
- **Completed**: 2026-03-28
- **Description**: 212 callouts updated across 163 files with descriptive icon titles.

### TASK-C75: Section number corrections
- **Completed**: 2026-03-28
- **Description**: 27 spans corrected across 5 files.

### TASK-C76: What's Next hierarchy enforcement
- **Completed**: 2026-03-28
- **Description**: 72+ files enforced with proper heading hierarchy.

### TASK-C77: Prerequisites to Appendix linking
- **Completed**: 2026-03-28
- **Description**: 20 files updated with appendix links in prerequisites.

### TASK-C78: Bibliography removal from index pages
- **Completed**: 2026-03-28
- **Description**: 34 files cleaned (bibliographies belong in section pages only).

### TASK-C79: Front Matter restructure
- **Completed**: 2026-03-28
- **Description**: 4 new sections created, ToC updated.

### TASK-C80: CONFORMANCE_CHECKLIST v2
- **Completed**: 2026-03-28
- **Description**: All current standards encoded in v2 checklist.

### TASK-C81: Agent protocol scouting
- **Completed**: 2026-03-28
- **Description**: MCP, A2A, AG-UI research completed for book content.

### TASK-C82: Epigraph width CSS fix
- **Completed**: 2026-03-28
- **Description**: Epigraph width CSS corrected.

### TASK-C83: ToC hyperlink consistency
- **Completed**: 2026-03-28
- **Description**: 39 split hyperlinks fixed; all section entries now fully hyperlinked.

### TASK-C84: Writing team to "How This Book Was Created"
- **Completed**: 2026-03-28
- **Description**: FM.5 created describing the 42-agent production pipeline. ToC views updated.

### TASK-C85: Duplicate callout-title cleanup
- **Completed**: 2026-03-28
- **Description**: 167 duplicate titles removed (151 files) + 134 emoji entities stripped (65 files).

### TASK-C86: Footer redesign
- **Completed**: 2026-03-28
- **Description**: Simplified to "Fifth Edition, 2026, Contents" with link. 78 footers simplified.

### TASK-C87: Split appendices C, D, E, G, H, I, J into section files
- **Completed**: 2026-03-28
- **Description**: 35 section files created across 7 appendices. ToC updated with all subsections.

### TASK-C88: Hyperlink products and datasets in appendices
- **Completed**: 2026-03-28
- **Description**: 47 external links across 20 appendix files with target="_blank" rel="noopener".

### TASK-C89: Fix capstone broken links
- **Completed**: 2026-03-28
- **Description**: All 61 hrefs updated in capstone files, all targets verified on disk.

### TASK-C90: Deep content improvement cycle 1
- **Completed**: 2026-03-28
- **Description**: Ch 00-05 improved. All Tier-1 and most Tier-2 content gaps filled.

### TASK-C91: Exercise-type badges on all exercise callouts
- **Completed**: 2026-03-28
- **Description**: 160 badges added across 23 files (82 conceptual, 59 coding, 12 discussion, 7 analysis).

### TASK-C92: Figure caption standardization
- **Completed**: 2026-03-28
- **Description**: 189 figcaptions across 110 files standardized with bold "Figure X.Y.Z" prefix.

### TASK-C93: Epigraph/prerequisites placement fix
- **Completed**: 2026-03-28
- **Description**: 37 files fixed, moving epigraph and prerequisites divs inside content wrapper.

### TASK-C94: Callout class standardization sweep
- **Completed**: 2026-03-28
- **Description**: 57 files fixed: 10 non-standard classes, 3 mismatches, 66 missing callout-title divs added.

### TASK-C95: Cross-reference hyperlink sweep
- **Completed**: 2026-03-28
- **Description**: 1,919 new cross-ref links added. Total: 2,971 across all 177 sections.

### TASK-C96: 3-pass page standardization
- **Completed**: 2026-03-28
- **Description**: 41 div-to-main conversions, 27 style blocks removed, 177 footers added, 210 heading normalizations.

### TASK-C97: HTML structure validator
- **Completed**: 2026-03-28
- **Description**: Automated validator checking 15 rules. Found 339 issues across 229 files, most fixed.

### TASK-C98: Exercise coverage expansion (154 sections)
- **Completed**: 2026-03-28
- **Description**: 178/178 sections now have exercises (100% coverage). 932 total exercise callouts.

### TASK-C99: ToC front matter alignment + appendix G-J subsections
- **Completed**: 2026-03-28
- **Description**: FM chapter number added, inline style overrides removed, 21 subsection entries added.

### TASK-C100: Fix broken cross-refs and chapter-nav links
- **Completed**: 2026-03-28
- **Description**: 623 cross-ref fixes across 170 files. 177 chapter-nav links normalized.

### TASK-C101: Normalize callout title text
- **Completed**: 2026-03-28
- **Description**: 178 title text normalizations ("Application Example" to "Practical Example", etc.).

### TASK-C102: Reanalyze pathways and course syllabi
- **Completed**: 2026-03-28
- **Description**: 20 self-study pathways (15 original + 5 new). All updated for current structure.

### TASK-C103: Internal cross-linking preference sweep
- **Completed**: 2026-03-28
- **Description**: Merged with TASK-090. Prefer linking to book sections over external URLs.

### TASK-C104: Write Section 10.5 (Model Pruning and Sparsity)
- **Completed**: 2026-03-28
- **Description**: 470-line section with 5 exercises, cross-refs, bibliography. Added to module-10 index and ToC.

### TASK-C105: Final quality sweep
- **Completed**: 2026-03-28
- **Description**: 0 broken links, 932 exercises with badges, 100% coverage, 52 section wrappers fixed. Book: 360 HTML files, 153K lines.

### TASK-C106: Remove duplicate old-style exercises
- **Completed**: 2026-03-28
- **Description**: 13 files cleaned of old-style exercise blocks. New callout exercises preserved.

### TASK-C107: Python library references and code examples sweep
- **Completed**: 2026-03-29
- **Description**: 53 code fragment insertions + 22 Production Alternative callouts across the entire book.

### TASK-C108: Format validation and bulk standardization
- **Completed**: 2026-03-29
- **Description**: Created validate_format.py. 4,463 issues found, reduced to 2,335 via 4 parallel fix agents.

### TASK-C109: Standard page templates
- **Completed**: 2026-03-29
- **Description**: Created templates/ directory with part-index, chapter-index, section templates and README.

### TASK-C110: Cross-reference class attribute sweep
- **Completed**: 2026-03-29
- **Description**: 1,836 links updated across 310 files with class="cross-ref".

### TASK-C111: Appendix index page format fix
- **Completed**: 2026-03-29
- **Description**: All 10 appendix index pages updated with standard header/nav/main wrapper.

### TASK-C112: Technical depth enrichment (math, pseudocode, worked examples)
- **Completed**: 2026-03-29
- **Description**: 50 enrichments across 42 files covering GloVe, BPE, FlashAttention, LoRA, DPO, CLIP, and more.

### TASK-C113: Chapter-nav bottom navigation for 38 remaining pages
- **Completed**: 2026-03-29
- **Description**: 38 chapter index pages got chapter-nav with prev/up/next links.

### TASK-C114: Part index whats-next for 7 remaining pages
- **Completed**: 2026-03-29
- **Description**: 7 part index pages got whats-next divs linking to the next part.

### TASK-C115: Duplicate callout-title div cleanup
- **Completed**: 2026-03-29
- **Description**: 622 duplicate pairs merged across 288 files. Kept more specific title in each case.

### TASK-C116: Illustration caption standardization
- **Completed**: 2026-03-29
- **Description**: 5 figcaption inline styles removed, loading="lazy" added across 213 files.

### TASK-C117: Deep standardization (code language classes, heading hierarchy, callout title attrs)
- **Completed**: 2026-03-29
- **Description**: Fixed 726 code blocks, 303 deep headings, 100 callout attrs, 10 em dashes. 1,400 issues resolved.

### TASK-C118: Tip callout expansion
- **Completed**: 2026-03-29
- **Description**: 114 tip callouts added across all parts. Total tips: 116.

### TASK-C119: Cross-reference unlinked technical terms
- **Completed**: 2026-03-29
- **Description**: 657 cross-reference links added across 237 files for 38 key terms.

### TASK-C120: Math typesetting with KaTeX
- **Completed**: 2026-03-29
- **Description**: KaTeX v0.16.21 installed. 458 files tagged. 194 math blocks + 608 inline math converted to LaTeX.

### TASK-C121: Inline math wrapping and cleanup
- **Completed**: 2026-03-29
- **Description**: 245 expressions wrapped in 48 files. 31 nested spans fixed in 17 files.

### TASK-C122: Math container CSS design
- **Completed**: 2026-03-29
- **Description**: Standardized math-block container in book.css with gradient, accent border, label/where-clause support.

### TASK-C123: Fix empty space in content boxes
- **Completed**: 2026-03-29
- **Description**: CSS overrides added to reset h2/h3 top margins inside whats-next, callout, prereqs, objectives.

### TASK-C124: TOC header and box cleanup
- **Completed**: 2026-03-29
- **Description**: 3 boxes removed from toc.html, header simplified, border-bottom removed from .header-nav.

### TASK-C125: Fix nested anchor tags inside section cards
- **Completed**: 2026-03-29
- **Description**: 38 nested anchors removed from 18 files.

### TASK-C126: Standardize callout title typography
- **Completed**: 2026-03-29
- **Description**: Unified callout, bibliography, and whats-next heading typography in book.css.

### TASK-C127: Convert non-standard content boxes to callouts
- **Completed**: 2026-03-29
- **Description**: 21 tip-box/highlight-box elements converted to standard callout format.

### TASK-C128: Reduce What's Next and callout spacing
- **Completed**: 2026-03-29
- **Description**: Padding and margin tightened in book.css for whats-next blocks.

### TASK-C129: Fix remaining SVG text issues (6 files)
- **Completed**: 2026-03-29
- **Description**: SVG text elements cleaned of math span wrappers and $ signs in 6 files.

### TASK-C130: Audit for non-callout content boxes
- **Completed**: 2026-03-29
- **Description**: 82 suspected boxes audited. 21 converted, 42 false positives dismissed, ~15 legacy boxes remain.
