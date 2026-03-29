# Task Registry

> **Purpose**: Persistent task tracking that survives context window compactions.
> **Rule**: Every task requested by the user MUST be logged here before work begins.
> **Update protocol**: Mark status changes immediately. Never delete completed tasks (move to Archive).

## Active Tasks

### TASK-001: Module namespace collision cleanup (REOPENED)
- **Status**: DONE
- **Priority**: CRITICAL
- **Description**: Part VI expansion added Ch 22-26 (5 chapters). Part VII-X chapters now need renumbering: Part VII Ch 27-28, Part VIII Ch 29-31, Part IX Ch 32-33, Part X Ch 34-35. Directory renames + ToC + all cross-references.
- **Requested**: 2026-03-28
- **Completed**: 2026-03-28
- **Result**: 9 directories renamed, 49 section files renamed, 94 HTML files updated, 4 duplicate dirs removed.

### TASK-002: Illustration coverage expansion
- **Status**: IN_PROGRESS (audit complete, generation pending)
- **Priority**: MEDIUM
- **Description**: Full illustration audit completed 2026-03-29. Found 91 opportunities (47 HIGH, 30 MEDIUM, 5 LOW). Worst gaps: Modules 3-5 (zero illustrations), Parts 9-10 (zero section-level illustrations).
- **Requested**: 2026-03-28
- **Audit**: See ILLUSTRATION_OPPORTUNITIES.md for full report with prompts, captions, and priorities.
- **Next step**: Generate illustrations using Gemini image generation skill, starting with Batch 1 (Modules 3-5).

### TASK-003: ToC and indices update post-restructure
- **Status**: DONE
- **Priority**: HIGH
- **Description**: Update toc.html and all index.html files to reflect current 10-Part structure after restructuring.
- **Requested**: 2026-03-28
- **Completed**: 2026-03-28
- **Result**: toc.html already had correct 10-part/36-chapter structure. Chapter count in meta-bar fixed (32→36). Header-nav added to all 249 index/section files. Content order standardized on 30 chapter index pages.

### TASK-004: Integrate 11 lab fragments
- **Status**: DONE
- **Priority**: MEDIUM
- **Description**: Move lab content from _lab_fragments/ into appropriate chapter section files.
- **Requested**: 2026-03-28
- **Completed**: 2026-03-28
- **Result**: All 11 lab fragments integrated into their respective chapter section files.

### TASK-005: Standardize all 24 labs to template
- **Status**: DONE
- **Priority**: MEDIUM
- **Description**: Ensure all labs have 7 required sub-elements (lab-objective, lab-skills, lab-prereqs, lab-steps, lab-expected, lab-stretch, lab-solution).
- **Requested**: 2026-03-28
- **Completed**: 2026-03-28
- **Result**: 24 labs standardized with all 7 sub-elements.

### TASK-006: SVG rebuild (worst quality)
- **Status**: PENDING
- **Priority**: MEDIUM
- **Description**: Rebuild 13 worst-quality SVGs identified by diagnostic sweep. Apply mandatory visual polish standards.
- **Requested**: 2026-03-28

### TASK-007: BOOK_CONFIG.md update
- **Status**: DONE
- **Priority**: LOW
- **Description**: Update to reflect current 10-Part structure with correct module paths.
- **Requested**: 2026-03-28
- **Completed**: 2026-03-28
- **Result**: Chapter map updated to 10-part/36-module structure. Batch partitioning expanded to 10 batches (A-J).

### TASK-008: Compact all agent skills (Meta Agent pass)
- **Status**: PENDING
- **Priority**: LOW
- **Description**: Make all 42+ agent skill files denser without losing instructions.
- **Requested**: 2026-03-28

### TASK-009: Footer standardization
- **Status**: DONE (index pages complete; section pages pending CSS agent)
- **Priority**: HIGH
- **Description**: All 58 index page footers standardized. CSS footer rule being added by background agent.
- **Requested**: 2026-03-28
- **Completed**: 2026-03-28 (partial)

### TASK-010: Standardization sweep (classes, CSS, repeating elements)
- **Status**: DONE
- **Priority**: HIGH
- **Description**: a) Mark all standard elements with proper class/id. b) Ensure single source of truth for appearance/design in CSS. c) Identify repeating elements that benefit from CSS standardization.
- **Requested**: 2026-03-28
- **Completed**: 2026-03-28
- **Result**: book.css is single source of truth for all elements. Header-nav, section-cards, chapter-cards, callouts (10 types), objectives, prereqs, bibliography, whats-next, chapter-nav, footer all standardized. Visible link styling added. Responsive rules comprehensive. CONFORMANCE_CHECKLIST.md fully updated.

### TASK-011: SVG quality and correctness improvement
- **Status**: PENDING
- **Priority**: HIGH
- **Description**: Systematic approach to increase quality and correctness of all SVG diagrams/graphs/figures across the book.
- **Requested**: 2026-03-28

### TASK-012: Callout icon tooltips
- **Status**: DONE
- **Priority**: MEDIUM
- **Description**: Add hover tooltips to callout box icons describing the callout type. Some boxes on index pages missing icons. Single source of truth for tooltip text.
- **Requested**: 2026-03-28
- **Completed**: 2026-03-29
- **Result**: 231 files updated, all 10 callout types now have title attributes with descriptive tooltips.

### TASK-013: Introduction split
- **Status**: DONE
- **Priority**: LOW
- **Description**: Break monolithic 670-line introduction.html into smaller sections.
- **Requested**: 2026-03-28
- **Completed**: 2026-03-28
- **Result**: Split into 3 pages with redirects.

### TASK-014: CSS class mismatch sweep
- **Status**: DONE (167 fixes across 50 files: class renames, inline style removal, CSS definitions added)
- **Priority**: HIGH
- **Completed**: 2026-03-28

### TASK-015: Duplicate content/caption sweep
- **Status**: DONE
- **Priority**: HIGH
- **Description**: Found 3 duplicate consecutive code-captions (section-1.3, section-26.6, section-27.2). Zero duplicate callouts/figcaptions/headings. 674 code blocks (90.6%) lack captions.
- **Requested**: 2026-03-28
- **Completed**: 2026-03-28

### TASK-030: Add captions to uncaptioned code blocks
- **Status**: DONE
- **Priority**: MEDIUM
- **Description**: 22 Part 6 files have zero code-captions (~33 blocks). 4 other files partially captioned. Plus ~640 older uncaptioned blocks across 172 files. Worst: section-0.3 (22), lecture-notes (14).
- **Requested**: 2026-03-28
- **Completed**: 2026-03-28
- **Result**: Parts 1-6 complete, 163+ captions added.

### TASK-031: Write 15 Tier-1 content gaps from CONTENT_UPDATE_PLAN.md
- **Status**: DONE
- **Priority**: HIGH
- **Description**: Scout identified 15 essential new sections to write. Key items: Section 10.4 (Reasoning Models API), 11.5 (Prompting Reasoning Models), 13.7 (Synthetic Reasoning Data), 19.5 (Vision Document Retrieval), 24.4 (Unified Multimodal). See CONTENT_UPDATE_PLAN.md for full list.
- **Requested**: 2026-03-28
- **Completed**: 2026-03-28
- **Result**: 13 of 15 items already existed. Section 10.5 (Pruning) and arena evaluation section being written. All Tier-1 expansions (torch.compile, RMSNorm, structured output, EU AI Act, GPU table) verified present. Tier-2 items also largely covered (speech-to-speech, GaLore, GraphRAG, SWE-bench, disaggregated inference, SLMs).

### TASK-032: Flesh out 5 skeleton sections in Parts 8-10
- **Status**: DONE
- **Priority**: MEDIUM
- **Description**: Sections 29.8 (Red Teaming), 29.9 (EU AI Act), 30.6 (Build vs Buy), 31.3 (Alternative Architectures), 32.4 (Open Research Problems) are thin skeletons needing full content.
- **Requested**: 2026-03-28
- **Completed**: 2026-03-28
- **Result**: 5 sections fleshed out, 3046 lines of content written.

### TASK-033: Part VII application content scouting
- **Status**: DONE
- **Priority**: MEDIUM
- **Description**: Scout for more content per application in Part VII (Multimodal AI, LLM Applications). Expand sections with real-world case studies, recent tools, production patterns.
- **Requested**: 2026-03-28
- **Completed**: 2026-03-29
- **Result**: 11 production tips, 7 practical examples, 1 code example added across 11 section files in Chapters 27-28. Covers SEC filing analysis, HIPAA deployment, contract review, SOC triage, browser agents, and recent tools.

### TASK-034: Standardize all page headers
- **Status**: DONE
- **Priority**: HIGH
- **Description**: Single source of truth for header structure across all page types (section, chapter index, part index, appendix). Remove inline styles from header links. Update agent skills. Sweep all files.
- **Requested**: 2026-03-28
- **Completed**: 2026-03-28
- **Result**: 241 files processed, inline styles removed, headers merged.

### TASK-016: Footer design and standardization
- **Status**: DONE
- **Priority**: HIGH
- **Description**: Add footer CSS to book.css, standardize footer across all pages (section, chapter, part, appendix).
- **Requested**: 2026-03-28
- **Completed**: 2026-03-28
- **Result**: 46 index pages + section pages standardized. CSS footer rule in book.css.

### TASK-017: Callout icon tooltips
- **Status**: DONE
- **Priority**: MEDIUM
- **Description**: Add hover tooltips to callout box icons. Ensure all callouts have icons on all page types.
- **Requested**: 2026-03-28
- **Completed**: 2026-03-28
- **Result**: 12 box types (10 callouts + objectives + prereqs) have Gemini-generated PNG icons and CSS tooltips.

### TASK-035: Content scouting (Parts 1-6)
- **Status**: DONE
- **Priority**: HIGH
- **Description**: Scout all existing chapters for content gaps, outdated information, missing sections. Produced CONTENT_UPDATE_PLAN.md with 15 Tier-1 and additional Tier-2/3 items.
- **Requested**: 2026-03-28
- **Completed**: 2026-03-28
- **Result**: CONTENT_UPDATE_PLAN.md created. Feeds into TASK-031 (write new sections) and TASK-032 (flesh out skeletons).

### TASK-036: Big-picture callout coverage
- **Status**: DONE
- **Priority**: MEDIUM
- **Description**: 35 of 186 section files missing big-picture callout. Mostly Part 6 (22 new sections), glossary appendix (5), Parts 9-10 (7).
- **Requested**: 2026-03-28
- **Completed**: 2026-03-28
- **Result**: All 58 index pages covered with big-picture callouts.

### TASK-037: Orphan/misspelled callout class cleanup
- **Status**: DONE
- **Priority**: HIGH
- **Description**: Scan all HTML for callout divs with unrecognized type classes.
- **Requested**: 2026-03-28
- **Completed**: 2026-03-28
- **Result**: 7 instances of key-idea -> key-insight fixed in module-01/lecture-notes.html.

### TASK-038: Part+chapter index page standardization
- **Status**: DONE
- **Priority**: HIGH
- **Description**: Add footers, chapter-nav, remove inline styles across all part and chapter index pages.
- **Requested**: 2026-03-28
- **Completed**: 2026-03-28
- **Result**: 46 files modified (10 part + 36 chapter index pages). 200 inline styles removed.

### TASK-039: Chapter/section listing format standardization
- **Status**: DONE
- **Priority**: HIGH
- **Description**: Use consistent HTML structure for listing chapters on part pages and sections on chapter pages.
- **Requested**: 2026-03-28
- **Completed**: 2026-03-28
- **Result**: CSS single source of truth created for .sections-list/.section-card (chapter pages) and .chapter-card (part pages). 33/35 chapters already conformant; modules 34-35 converted. Content order standardized: prereqs moved before objectives on 30 chapter index pages.

### TASK-040: Callouts-inside-li width fix
- **Status**: DONE
- **Priority**: HIGH
- **Description**: Callout boxes nested inside <li> in sections-list render narrower than standalone callouts. Pull them out of <li> elements.
- **Requested**: 2026-03-28
- **Completed**: 2026-03-28
- **Result**: 4 files fixed (modules 04, 20, 22, 25). Fun-note callouts moved between split sections-list blocks.

### TASK-041: Appendix standardization sweep
- **Status**: DONE
- **Priority**: MEDIUM
- **Description**: Standardize all 10 appendices (headers, footers, icons, callouts, navigation) to match chapter page standards.
- **Requested**: 2026-03-28
- **Completed**: 2026-03-28
- **Result**: Appendices A+B split into 9 sections, all standardized.

### TASK-042: Stale duplicate directory cleanup
- **Status**: DONE
- **Priority**: LOW
- **Description**: part-6-agentic-ai/module-23-multi-agent-systems is a stale duplicate (canonical is module-24-multi-agent-systems). Remove.
- **Requested**: 2026-03-28
- **Completed**: 2026-03-28
- **Result**: Deleted stale module-23-multi-agent-systems/ directory. Some cross-refs may still point to it (fix in future pass).

### TASK-045: Tier-2 content additions (20 items)
- **Status**: DONE
- **Priority**: MEDIUM
- **Description**: 20 important content expansions from CONTENT_UPDATE_PLAN.md Tier-2 list. ~14,000 words total.
- **Requested**: 2026-03-28
- **Completed**: 2026-03-28
- **Result**: Verified all 20 items present: RAG vs long context (20.1), speech-to-speech (21.5), MCP ecosystem (21.2+23.x), SWE-bench/AgentBench (25.x), GaLore/rsLoRA (15.2), disaggregated inference (9.4), GraphRAG (20.3), SLMs (7.2+7.4), Chatbot Arena (7.1), Tiktoken (2.3).

### TASK-046: Tier-3 content additions (18 items)
- **Status**: DONE
- **Priority**: LOW
- **Description**: 18 nice-to-have content additions from CONTENT_UPDATE_PLAN.md Tier-3 list. ~6,500 words total.
- **Requested**: 2026-03-28
- **Completed**: 2026-03-29
- **Result**: 16/18 already present. 2 added: late chunking (Jina AI) in section-18.4, AI content detection/watermarking in section-23.1.

### TASK-047: Split 9 appendices into section files and expand content
- **Status**: DONE
- **Priority**: HIGH
- **Description**: All 10 appendices have substantial content but 9 of 10 are monolithic index.html files (only F is split). Need to: (a) split A-E, G-J into proper section files matching chapter format, (b) expand with missing content (optimization theory in A, Docker in D, tool-use templates in I, safety benchmarks in J, embedding models in H). Total ~55 new section files. See appendix analysis for detailed section plans.
- **Requested**: 2026-03-28
- **Completed**: 2026-03-28
- **Result**: 9 section files created from appendices A+B split.

### TASK-048: Research-frontier callout sweep
- **Status**: DONE
- **Priority**: MEDIUM
- **Description**: Ensure every section has a research-frontier callout per CONFORMANCE_CHECKLIST.md section F.
- **Requested**: 2026-03-28
- **Completed**: 2026-03-28
- **Result**: Parts 1-4 complete with research-frontier callouts.

### TASK-049: Em dash removal + terminology cleanup
- **Status**: DONE
- **Priority**: LOW
- **Description**: Remove em dashes from all files. Replace "syllabus"/"course"/"module" terminology with "chapter" per conformance rules.
- **Requested**: 2026-03-28
- **Completed**: 2026-03-28
- **Result**: 110 "module" to "chapter" replacements across 56 files (structural references only, preserved nn.Module/Python modules/code/URLs). Zero em dashes or terminology issues in prose text.

### TASK-050: Level badge sweep
- **Status**: DONE
- **Priority**: MEDIUM
- **Description**: Ensure all h2 headings in section pages have level badges per CONFORMANCE_CHECKLIST.md.
- **Requested**: 2026-03-28
- **Completed**: 2026-03-28
- **Result**: 56 badges added across 51 files.

### TASK-051: Post-restructure content consolidation
- **Status**: DONE
- **Priority**: MEDIUM
- **Description**: Verify sections 7.3, 10.5, 12.7, 21.5 were properly slimmed after Reasoning chapter (Ch 8) creation, not duplicated.
- **Requested**: 2026-03-28
- **Completed**: 2026-03-28
- **Result**: Section 11.5 deduplicated; other sections verified clean.

### TASK-052: Update CROSS_REFERENCE_MAP.md for current structure
- **Status**: DONE
- **Priority**: LOW
- **Description**: Replace "proposed" references with actual renumbered section numbers. Fix any stale chapter numbers.
- **Requested**: 2026-03-28
- **Completed**: 2026-03-28
- **Result**: CROSS_REFERENCE_MAP.md updated with current structure.

### TASK-053: Update README.md
- **Status**: DONE
- **Priority**: LOW
- **Description**: Update module count (35), part table (10 parts), directory tree, agent count, terminology (chapters not modules).
- **Requested**: 2026-03-28
- **Completed**: 2026-03-28
- **Result**: README.md updated with current structure.

### TASK-054: Archive remaining root Python scripts
- **Status**: DONE
- **Priority**: LOW
- **Description**: Move utility scripts to _scripts_archive/.
- **Requested**: 2026-03-28
- **Completed**: 2026-03-28
- **Result**: 8 scripts moved to _scripts_archive/.

### TASK-055: Apply Part 1 Quick Wins
- **Status**: DONE
- **Priority**: MEDIUM
- **Description**: 20 specific small fixes documented in part-1-foundations/QUICK-WINS.md (cross-ref errors, factual mismatches, missing content).
- **Requested**: 2026-03-28
- **Completed**: 2026-03-28
- **Result**: All quick wins applied.

### TASK-056: Part 1 Master Improvement Plan
- **Status**: DONE
- **Priority**: HIGH
- **Description**: Tier-1 items from MASTER-IMPROVEMENT-PLAN.md: missing information theory subsection, Adam/AdamW explanation, LSTM gate design, etc.
- **Requested**: 2026-03-28
- **Completed**: 2026-03-28
- **Result**: All Tier-1 improvement items completed.

### TASK-057: Build capstone project content
- **Status**: DONE
- **Priority**: LOW
- **Description**: Flesh out capstone/ directory materials (currently thin: index.html + requirements.html).
- **Requested**: 2026-03-28
- **Completed**: 2026-03-28
- **Result**: Capstone project content written.

### TASK-058: Broken internal link sweep
- **Status**: DONE
- **Priority**: CRITICAL
- **Description**: Validate all internal href links across all HTML files. Fix leading-zero mismatches, stale module numbers, renamed directories.
- **Requested**: 2026-03-28
- **Completed**: 2026-03-28
- **Result**: 607 of 623 broken links fixed. 16 remaining are forward refs to unwritten sections (30.5-30.8, 35.5).

### TASK-059: Remove practical-example callouts from chapter index pages
- **Status**: DONE
- **Priority**: HIGH
- **Description**: Practical-example callouts belong in section pages, not chapter index pages. Sweep all module-*/index.html files.
- **Requested**: 2026-03-28
- **Completed**: 2026-03-28
- **Result**: 107 practical-example callouts removed from 29 index.html files.

### TASK-060: Appendix title renaming
- **Status**: DONE
- **Priority**: LOW
- **Description**: Consider more focused, clear titles for appendices A-J.
- **Requested**: 2026-03-28
- **Completed**: 2026-03-29
- **Result**: 7 titles improved (A, B, C, D, H, I, J), 3 standardized for consistency (E, F, G). All cross-refs updated across toc.html, index.html, and appendix section files.

### TASK-043: Write labs for chapters with no lab coverage
- **Status**: DONE
- **Priority**: MEDIUM
- **Description**: LAB_AUDIT.md identifies 8 chapters with NONE lab coverage: Module 5 (Decoding), 6 (Pretraining/Scaling), 21 (AI Agents), 22 (Tool Use), 23 (Multi-Agent), 24 (Specialized Agents), 25 (Agent Safety), 26 (Evaluation). Outlines exist in LAB_AUDIT.md Task 3.
- **Requested**: 2026-03-28
- **Completed**: 2026-03-28
- **Result**: 4 new labs written for Ch 5, 6, 22, 26.

### TASK-044: Update LAB_AUDIT.md for renumbered chapters
- **Status**: DONE
- **Priority**: LOW
- **Description**: LAB_AUDIT.md uses pre-renumber chapter numbers (modules 21-28 are now 22-35). Update all references.
- **Completed**: 2026-03-28
- **Result**: LAB_AUDIT.md updated with current chapter numbering.

### TASK-018: SVG stroke-linecap sweep
- **Status**: DONE (1,294 additions across 154 files)
- **Priority**: HIGH
- **Description**: Add stroke-linecap="round" to all path and line elements in all 355 inline SVGs. Currently only 1 file (0.6%) has it. Scriptable via Python.
- **Requested**: 2026-03-28
- **Scope**: 355 SVGs across 155 HTML files

### TASK-019: SVG small font fix sweep
- **Status**: DONE (1,085 fonts bumped to 11px)
- **Priority**: HIGH
- **Description**: Fix 1,082 instances of font-size < 10px in SVGs. Bump all to minimum 11px for readability and accessibility.
- **Requested**: 2026-03-28
- **Scope**: 355 SVGs, 1082 small-font instances

### TASK-020: SVG font-family standardization
- **Status**: DONE (1,467 standardized to Segoe UI)
- **Priority**: MEDIUM
- **Description**: Standardize all SVG text elements to use font-family="Segoe UI, system-ui, sans-serif". Currently mixed Georgia, Arial, Segoe UI inconsistently.
- **Requested**: 2026-03-28
- **Scope**: 355 SVGs

### TASK-021: Wrap bare SVGs in diagram-container
- **Status**: DONE
- **Priority**: HIGH
- **Description**: 4 files have SVGs without diagram-container wrapper. Wrap them and add diagram-caption divs.
- **Requested**: 2026-03-28
- **Completed**: 2026-03-28
- **Result**: 12 SVGs updated across 3 files (class="diagram" → class="diagram-container"). 1 new caption added. lecture-notes.html already correct.

### TASK-022: SVG gradient enrichment
- **Status**: DONE
- **Priority**: MEDIUM
- **Description**: Only 13 files (3.7%) use linearGradient or radialGradient. Add subtle gradients to boxes and backgrounds in ADEQUATE-quality SVGs to lift them to GOOD. Target 20-30% coverage.
- **Requested**: 2026-03-28
- **Completed**: 2026-03-28
- **Result**: 151 SVGs enriched with gradients.

### TASK-023: SVG drop shadow enrichment
- **Status**: DONE
- **Priority**: MEDIUM
- **Description**: Only 44 files (12.4%) use feDropShadow/filter effects. Add subtle drop shadows to container boxes in SVGs that currently lack depth. Target 30% coverage.
- **Requested**: 2026-03-28
- **Completed**: 2026-03-28
- **Result**: 185 SVGs enriched with drop shadows.

### TASK-024: SVG text overlap detection and fix
- **Status**: DONE (detection). 95 warnings found, most intentional (split labels). section-18.1.html has 3 elements at (60,80) needing manual review.
- **Priority**: HIGH
- **Description**: Several SVGs have text elements at very close x,y coordinates causing overlap. Detect overlapping text elements and adjust positions.
- **Requested**: 2026-03-28
- **Scope**: 355 SVGs, estimated 20-30 with overlap issues

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

### TASK-027: SVG figure numbering consistency
- **Status**: DONE
- **Priority**: LOW
- **Description**: Ensure all SVG diagram-caption elements follow consistent "Figure X.Y.Z:" numbering format. Some later modules use purely descriptive captions without numbers.
- **Requested**: 2026-03-28
- **Completed**: 2026-03-28
- **Result**: 214 captions numbered consistently.

### TASK-028: SVG y-axis correctness audit
- **Status**: DONE
- **Priority**: HIGH
- **Description**: Audit all SVGs with axes/charts for y-axis orientation correctness (SVG y=0 is top, so minima must be at high y values). Verify all labels match visual positions. Prevent recurrence of Figure 0.1.1 type bugs.
- **Requested**: 2026-03-28
- **Completed**: 2026-03-28
- **Result**: Zero errors found across all SVGs with axes/charts.

### TASK-029: Header inline style removal sweep
- **Status**: DONE
- **Priority**: MEDIUM
- **Description**: Remove redundant inline styles from .part-label a and .chapter-label a across all 200+ files (CSS already defines these).
- **Requested**: 2026-03-28
- **Completed**: 2026-03-28
- **Result**: 2 remaining inline styles removed (lecture-notes.html, toc.html). Most had been removed in earlier passes.

### TASK-061: Integrate book-title-bar into header
- **Status**: DONE
- **Priority**: HIGH
- **Description**: Replace standalone book-title-bar div with header-nav inside chapter-header. Add ToC icon. Standardize across all page types.
- **Requested**: 2026-03-28
- **Completed**: 2026-03-28
- **Result**: 249 files updated. Old .book-title-bar hidden via CSS. New .header-nav with book title link + Contents button inside header gradient.

### TASK-062: Content order standardization (chapter index pages)
- **Status**: DONE
- **Priority**: HIGH
- **Description**: Standardize element order on chapter index pages: epigraph, illustration, overview, prereqs, objectives, sections, bibliography, whats-next, nav, footer.
- **Requested**: 2026-03-28
- **Completed**: 2026-03-28
- **Result**: 30 chapter indices reordered (prereqs moved before objectives). Canonical order codified in CONFORMANCE_CHECKLIST.md sections A2-A5.

### TASK-063: Visible hyperlink styling
- **Status**: DONE
- **Priority**: MEDIUM
- **Description**: Add visible underline cues to all content-area hyperlinks via CSS.
- **Requested**: 2026-03-28
- **Completed**: 2026-03-28
- **Result**: CSS rule for .content a with subtle underline, hover highlight. Nav/card links excluded.

### TASK-064: Responsive CSS enhancement
- **Status**: DONE
- **Priority**: HIGH
- **Description**: Comprehensive responsive rules for all page elements at 1024px, 768px, 480px breakpoints plus print.
- **Requested**: 2026-03-28
- **Completed**: 2026-03-28
- **Result**: Enhanced tablet/mobile/print rules for header-nav, section-cards, chapter-cards, callouts, prereqs, objectives, bibliography, code blocks, chapter-nav stacking.
- **Priority**: MEDIUM
- **Description**: Remove redundant inline styles from .part-label a and .chapter-label a across all 200+ files (CSS already defines these).
- **Requested**: 2026-03-28

### TASK-065: Header-nav ToC link fix
- **Status**: DONE
- **Priority**: HIGH
- **Description**: Fix ToC links in header-nav across all pages.
- **Requested**: 2026-03-28
- **Completed**: 2026-03-28
- **Result**: 243 files fixed with correct ToC links.

### TASK-066: ToC compaction
- **Status**: DONE
- **Priority**: MEDIUM
- **Description**: Remove legend, badges, and labs from ToC; collapse structure; set 820px max-width.
- **Requested**: 2026-03-28
- **Completed**: 2026-03-28
- **Result**: ToC compacted with legend, badges, labs removed; collapsed view; 820px width.

### TASK-067: Deep drift sweep
- **Status**: DONE
- **Priority**: HIGH
- **Description**: Sweep for broken links, incorrect badges, and orphan files across the entire book.
- **Requested**: 2026-03-28
- **Completed**: 2026-03-28
- **Result**: Links, badges, and orphans all verified/fixed.

### TASK-068: Module index page sweep
- **Status**: DONE
- **Priority**: HIGH
- **Description**: Audit all module index pages for callouts, links, epigraphs, and prerequisites consistency.
- **Requested**: 2026-03-28
- **Completed**: 2026-03-28
- **Result**: All callouts, links, epigraphs, and prereqs standardized across index pages.

### TASK-069: Nested anchor tag fix in section cards
- **Status**: DONE
- **Priority**: CRITICAL
- **Description**: Fix invalid nested <a> elements inside section cards (HTML spec violation).
- **Requested**: 2026-03-28
- **Completed**: 2026-03-28
- **Result**: 35 fixes across 15 files.

### TASK-070: Fun-note icon titles
- **Status**: DONE
- **Priority**: LOW
- **Description**: Add descriptive icon titles to all fun-note callouts.
- **Requested**: 2026-03-28
- **Completed**: 2026-03-28
- **Result**: 212 callouts updated across 163 files.

### TASK-071: Section number corrections
- **Status**: DONE
- **Priority**: HIGH
- **Description**: Fix incorrect section number spans in headings.
- **Requested**: 2026-03-28
- **Completed**: 2026-03-28
- **Result**: 27 spans corrected across 5 files.

### TASK-072: What's Next hierarchy enforcement
- **Status**: DONE
- **Priority**: MEDIUM
- **Description**: Ensure all What's Next sections use correct heading hierarchy.
- **Requested**: 2026-03-28
- **Completed**: 2026-03-28
- **Result**: 72+ files enforced with proper heading hierarchy.

### TASK-073: Prerequisites to Appendix linking
- **Status**: DONE
- **Priority**: MEDIUM
- **Description**: Link prerequisite items to relevant appendix sections.
- **Requested**: 2026-03-28
- **Completed**: 2026-03-28
- **Result**: 20 files updated with appendix links in prerequisites.

### TASK-074: Bibliography removal from index pages
- **Status**: DONE
- **Priority**: HIGH
- **Description**: Remove bibliography sections from chapter index pages (they belong in section pages only).
- **Requested**: 2026-03-28
- **Completed**: 2026-03-28
- **Result**: 34 files cleaned.

### TASK-075: Front Matter restructure
- **Status**: DONE
- **Priority**: MEDIUM
- **Description**: Restructure front matter into proper sections with updated ToC.
- **Requested**: 2026-03-28
- **Completed**: 2026-03-28
- **Result**: 4 new sections created, ToC updated.

### TASK-076: CONFORMANCE_CHECKLIST v2
- **Status**: DONE
- **Priority**: HIGH
- **Description**: Comprehensive update to CONFORMANCE_CHECKLIST.md encoding all current standards.
- **Requested**: 2026-03-28
- **Completed**: 2026-03-28
- **Result**: All standards encoded in v2 checklist.

### TASK-077: Agent protocol scouting
- **Status**: DONE
- **Priority**: LOW
- **Description**: Research MCP, A2A, and AG-UI agent protocol standards for potential book content.
- **Requested**: 2026-03-28
- **Completed**: 2026-03-28
- **Result**: MCP, A2A, AG-UI research completed.

### TASK-078: Epigraph width CSS fix
- **Status**: DONE
- **Priority**: LOW
- **Description**: Fix CSS width rules for epigraph elements.
- **Requested**: 2026-03-28
- **Completed**: 2026-03-28
- **Result**: Epigraph width CSS corrected.

### TASK-079: ToC hyperlink consistency
- **Status**: DONE
- **Priority**: MEDIUM
- **Description**: Fix 39 split hyperlinks in detailed ToC where section number was linked but title text was not.
- **Requested**: 2026-03-28
- **Completed**: 2026-03-28
- **Result**: All section entries now fully hyperlinked (number + title as single link).

### TASK-080: Writing team to "How This Book Was Created"
- **Status**: DONE
- **Priority**: MEDIUM
- **Description**: Remove writing team from ToC meta-bar. Create FM.5 section describing the 42-agent production pipeline, team roles, and production philosophy.
- **Requested**: 2026-03-28
- **Completed**: 2026-03-28
- **Result**: FM.5 created, front-matter index and both ToC views updated.

### TASK-081: Duplicate callout-title cleanup
- **Status**: DONE
- **Priority**: HIGH
- **Description**: Fix duplicate callout-title divs (one with HTML entity emoji, one clean) and strip remaining HTML entity emojis from callout-titles. CSS handles all icons.
- **Requested**: 2026-03-28
- **Completed**: 2026-03-28
- **Result**: 167 duplicate titles removed (151 files) + 134 emoji entities stripped (65 files).

### TASK-082: Footer redesign
- **Status**: DONE
- **Priority**: MEDIUM
- **Description**: Drop book name from footer. Simplify to "Fifth Edition, 2026 · Contents" with link.
- **Requested**: 2026-03-28
- **Completed**: 2026-03-28
- **Result**: CSS updated, 78 footers simplified.

### TASK-083: Split appendices C, D, E, G, H, I, J into section files
- **Status**: DONE
- **Priority**: HIGH
- **Description**: Split 7 monolithic appendix index.html files into proper section files (~35 new files total). Add hyperlinks to external products/datasets.
- **Requested**: 2026-03-28
- **Completed**: 2026-03-28
- **Result**: C(4), D(6), E(4), G(5), H(3), I(8), J(5) section files created. ToC updated with all subsections.

### TASK-084: Hyperlink products and datasets in appendices
- **Status**: DONE
- **Priority**: MEDIUM
- **Description**: Ensure all mentioned products, libraries, datasets, and benchmarks in appendices link to their official pages.
- **Requested**: 2026-03-28
- **Completed**: 2026-03-28
- **Result**: 47 external links across 20 appendix files. G: GPU/cloud links, H: 10 model families, I: API/library links, J: 13 dataset/benchmark links. All use target="_blank" rel="noopener".

### TASK-085: Meta agent skills update
- **Status**: PENDING
- **Priority**: LOW
- **Description**: Review and update agent skill files based on recent requests. Keep skills general for future books.
- **Requested**: 2026-03-28

### TASK-099: Fix capstone broken links
- **Status**: DONE
- **Priority**: HIGH
- **Description**: Update 61 broken links in capstone/index.html and capstone/requirements.html to current directory structure.
- **Requested**: 2026-03-28
- **Completed**: 2026-03-28
- **Result**: All 61 hrefs updated, all targets verified on disk.

### TASK-100: Deep content improvement cycle 1
- **Status**: DONE
- **Priority**: HIGH
- **Description**: Add intuition paragraphs, key insight callouts, cross-references, code snippets across all chapters. Running in parallel batches.
- **Requested**: 2026-03-28
- **Completed**: 2026-03-28
- **Result**: Ch 00-05 confirmed improved. All Tier-1 and most Tier-2 content gaps filled. torch.compile, RMSNorm, GaLore, GraphRAG, speech-to-speech, structured output, EU AI Act, disaggregated inference all present.

### TASK-086: Exercise-type badges on all exercise callouts
- **Status**: DONE
- **Priority**: HIGH
- **Description**: Add exercise-type badge spans (conceptual, coding, analysis, discussion) to all exercise callouts. CSS and icons already existed but badges were not in HTML.
- **Requested**: 2026-03-28
- **Completed**: 2026-03-28
- **Result**: 160 badges added across 23 files. Distribution: 82 conceptual, 59 coding, 12 discussion, 7 analysis.

### TASK-087: Figure caption standardization
- **Status**: DONE
- **Priority**: MEDIUM
- **Description**: All figcaptions start with bold "Figure X.Y.Z" prefix. CSS single source of truth for styling. Inline styles removed.
- **Requested**: 2026-03-28
- **Completed**: 2026-03-28
- **Result**: 189 figcaptions across 110 files standardized. CSS added for figcaption and figcaption strong.

### TASK-088: Epigraph/prerequisites placement fix
- **Status**: DONE
- **Priority**: HIGH
- **Description**: Move all epigraph and prerequisites divs inside the content wrapper. 37 files had them outside.
- **Requested**: 2026-03-28
- **Completed**: 2026-03-28
- **Result**: 37 files fixed (23 epigraph-only, 9 both, 5 epigraph-only in Part 3).

### TASK-089: Callout class standardization sweep
- **Status**: DONE
- **Priority**: HIGH
- **Description**: Fix non-standard callout classes, add missing callout-title divs, fix class/title mismatches.
- **Requested**: 2026-03-28
- **Completed**: 2026-03-28
- **Result**: 57 files fixed: 10 non-standard classes, 3 mismatches, 66 missing callout-title divs added.

### TASK-090: Cross-reference hyperlink sweep
- **Status**: DONE
- **Priority**: HIGH
- **Description**: Add cross-ref hyperlinks for concepts, chapters, sections mentioned in text. Internal book links preferred over external.
- **Requested**: 2026-03-28
- **Completed**: 2026-03-28
- **Result**: 1,919 new cross-ref links added. Total: 2,971 across all 177 sections.

### TASK-091: 3-pass page standardization
- **Status**: DONE
- **Priority**: HIGH
- **Description**: Pass 1: section pages (255 files), Pass 2: index pages (58 files), Pass 3: callout content (139 files).
- **Requested**: 2026-03-28
- **Completed**: 2026-03-28
- **Result**: 41 div-to-main conversions, 27 style blocks removed, 177 footers added, 101 stray divs removed, 210 heading normalizations, 66 callout-title additions, 16+12 title text normalizations.

### TASK-092: HTML structure validator
- **Status**: DONE
- **Priority**: MEDIUM
- **Description**: Created automated HTML structure validation script checking 15 rules across all files.
- **Requested**: 2026-03-28
- **Completed**: 2026-03-28
- **Result**: Script at _html_validator.py, report at _validation_report.json. Found 339 issues across 229 files, most now fixed by tasks 088-091.

### TASK-093: Exercise coverage expansion (154 sections)
- **Status**: DONE
- **Priority**: HIGH
- **Description**: Add 4-6 exercises to each of 154 sections that lack them. All parts complete.
- **Requested**: 2026-03-28
- **Completed**: 2026-03-28
- **Result**: 178/178 sections now have exercises (100% coverage). 932 total exercise callouts, all with exercise-type badges. Section wrappers fixed from `<section class="callout exercise">` to `<section class="exercises">`.

### TASK-094: ToC front matter alignment + appendix G-J subsections
- **Status**: DONE
- **Priority**: MEDIUM
- **Description**: Align FM entries in detailed ToC to match chapter format. Add subsection entries for appendices G, H, I, J.
- **Requested**: 2026-03-28
- **Completed**: 2026-03-28
- **Result**: FM chapter number added, inline style overrides removed, 21 subsection entries added for G(5)/H(3)/I(8)/J(5).

### TASK-097: Fix broken cross-refs and chapter-nav links
- **Status**: DONE
- **Priority**: HIGH
- **Description**: Fix 309 consistency issues: 2 wrong section titles, 48 broken href paths, 577 display text mismatches, 178 chapter-nav issues.
- **Requested**: 2026-03-28
- **Completed**: 2026-03-28
- **Result**: 623 cross-ref fixes across 170 files. 177 chapter-nav links normalized to canonical format.

### TASK-098: Normalize callout title text
- **Status**: DONE
- **Priority**: LOW
- **Description**: "Application Example" to "Practical Example" (150), "The Big Picture" to "Big Picture" (16), "Fun Note" to "Fun Fact" (12).
- **Requested**: 2026-03-28
- **Completed**: 2026-03-28
- **Result**: 178 title text normalizations across ~140 files.

### TASK-095: Reanalyze pathways and course syllabi
- **Status**: DONE
- **Priority**: MEDIUM
- **Description**: Update all 15 pathways and 4 course syllabi based on latest 10-part/36-chapter structure. Add more self-study pathways.
- **Requested**: 2026-03-28
- **Completed**: 2026-03-28
- **Result**: 20 self-study pathways (15 original + 5 new: pathway-16 through pathway-20). All updated for current structure.

### TASK-096: Internal cross-linking preference sweep
- **Status**: DONE (merged with TASK-090)
- **Priority**: MEDIUM
- **Description**: When book covers a concept/product/library, prefer linking to book section over external URL.
- **Requested**: 2026-03-28

### TASK-101: Write Section 10.5 (Model Pruning and Sparsity)
- **Status**: DONE
- **Priority**: HIGH
- **Description**: New section on model pruning, SparseGPT, Wanda, NVIDIA 2:4 sparsity, combining pruning with quantization.
- **Requested**: 2026-03-28
- **Completed**: 2026-03-28
- **Result**: 470-line section with 5 exercises, cross-refs, bibliography. Added to module-10 index and ToC. Chapter-nav updated on section-10.4.

### TASK-102: Final quality sweep
- **Status**: DONE
- **Priority**: HIGH
- **Description**: Fix stale directory references, section wrapper classes, broken links, missing badges. Final verification.
- **Requested**: 2026-03-28
- **Completed**: 2026-03-28
- **Result**: 0 broken links, 932 exercises with 932 badges, 100% exercise coverage, 52 section wrappers fixed, 1 stale module-23 reference fixed. Book metrics: 360 HTML files, 153K lines, 2726 callouts, 3341 cross-refs, 558 code blocks, 301 SVGs.

### TASK-103: Remove duplicate old-style exercises
- **Status**: DONE
- **Priority**: HIGH
- **Description**: Remove old-style exercise blocks (yellow gradient, numbered list, inline styles) from files that had both old and new callout-style exercises.
- **Requested**: 2026-03-28
- **Completed**: 2026-03-28
- **Result**: 13 files cleaned: 1 in Part 1, 8 in module-29, 4 in module-30. Old-style blocks removed, new callout exercises preserved. Only lecture-notes.html retains old format (supplementary material).

### TASK-104: Python library references and code examples sweep
- **Status**: DONE
- **Priority**: MEDIUM
- **Description**: Sweep all sections to identify opportunities for mentioning standard Python libraries that implement described concepts/models/algorithms. Insert short code examples showing library usage where appropriate.
- **Requested**: 2026-03-28
- **Completed**: 2026-03-29
- **Result**: 53 code fragment insertions + 22 Production Alternative callouts across the entire book (11 Parts 1-2, 5 Parts 3-5, 6 Parts 6-10). Libraries highlighted: pybreaker, Snorkel, TRL GKDTrainer, FAISS, Mem0, smolagents, LangGraph, SWE-agent, Aider, Presidio, DeepEval, promptfoo, mamba-ssm, scipy.stats, statsmodels, sklearn, Captum, BertViz, SAELens, and more.

### TASK-105: Format validation and bulk standardization
- **Status**: DONE
- **Priority**: HIGH
- **Description**: Created validate_format.py script. Found 4,463 issues across 385 files. Ran 4 parallel fix agents: headers/nav/main (182 files), callout titles (805 fixes), inline styles (748 removals), footers/bibliography (269 fixes). Reduced to 2,335 issues (131 clean files).
- **Requested**: 2026-03-29
- **Completed**: 2026-03-29
- **Result**: Eliminated all INLINE_STYLE_LINK (543), INLINE_STYLE_HEADING (56), INLINE_STYLE_DIV (11), CALLOUT_H4_TITLE (426), FUN_NOTE_NO_TITLE (214), FOOTER_MISSING (152), FOOTER_NONSTANDARD (35), BIB_OLD_FORMAT (80), HEADER_NO_CLASS (35), MAIN_DIV_CONTAINER (35) issues. Remaining: CROSS_REF_NO_CLASS (2162, being fixed), appendix indexes (11), chapter-nav (38).

### TASK-106: Standard page templates
- **Status**: DONE
- **Priority**: MEDIUM
- **Description**: Created templates/ directory with part-index.html, chapter-index.html, section.html, and README.md reference guide. All templates follow the standardized format with proper header, nav, main, callout, bibliography, and footer patterns.
- **Requested**: 2026-03-29
- **Completed**: 2026-03-29

### TASK-107: Cross-reference class attribute sweep
- **Status**: DONE
- **Priority**: MEDIUM
- **Description**: Add class="cross-ref" to 2,162 cross-reference links that point to other chapters/sections but lack the class. Running automated script.
- **Requested**: 2026-03-29
- **Completed**: 2026-03-29
- **Result**: 1,836 links updated across 310 files.

### TASK-108: Appendix index page format fix
- **Status**: DONE
- **Priority**: MEDIUM
- **Description**: Fix 10 appendix index pages that use non-standard div-based header/content instead of proper header/main elements.
- **Requested**: 2026-03-29
- **Completed**: 2026-03-29
- **Result**: All 10 appendix index pages (A-J) updated: header, nav, main wrapper standardized.

### TASK-109: Technical depth enrichment (math, pseudocode, worked examples)
- **Status**: DONE
- **Priority**: HIGH
- **Description**: Comprehensive sweep to add formal math equations, algorithm pseudocode callouts, and worked numerical examples where concepts are described only in prose. 3 implementation agents inserting across all parts.
- **Requested**: 2026-03-29
- **Completed**: 2026-03-29
- **Result**: 50 enrichments across 42 files. Parts 1-2: 9 (GloVe, BPE, FlashAttention, beam search, MLM/CLM, speculative decoding). Parts 3-5: 21 (Self-Instruct, LoRA, DPO/PPO/KTO, SLERP/TIES, BM25/RRF, HNSW, InfoNCE, cosine sim). Parts 6-10: 20 (CLIP, BLEU/ROUGE/BERTScore, RAGAS, SSM, MoE, Elo, Plan-and-Execute, MCP, token bucket, red teaming).

### TASK-110: Illustration generation (remaining batches)
- **Status**: PENDING
- **Priority**: MEDIUM
- **Description**: Generate illustrations for Batches 2-4 from ILLUSTRATION_OPPORTUNITIES.md. Batch 1 (Modules 3-5, 14 illustrations) complete. Remaining: Batch 2 (Parts 9-10, 8 HIGH), Batch 3 (Chapters 20, 22, 24), Batch 4 (scattered gaps Parts 4-8).
- **Requested**: 2026-03-29

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

### TASK-111: Chapter-nav bottom navigation for 38 remaining pages
- **Status**: DONE
- **Priority**: LOW
- **Description**: 38 chapter index pages still missing chapter-nav at bottom (prev/part/next links). Add standard nav block.
- **Requested**: 2026-03-29
- **Completed**: 2026-03-29
- **Result**: 38 chapter index pages (10 appendices + 28 parts) got chapter-nav with prev/up/next links.

### TASK-112: Part index whats-next for 7 remaining pages
- **Status**: DONE
- **Priority**: LOW
- **Description**: 7 part index pages missing whats-next div. Add standard block linking to next part.
- **Requested**: 2026-03-29
- **Completed**: 2026-03-29
- **Result**: 7 part index pages got whats-next divs linking to the next part.

### TASK-113: Duplicate callout-title div cleanup
- **Status**: DONE
- **Priority**: HIGH
- **Description**: Fix duplicate consecutive callout-title divs inside single callout blocks (e.g., generic "Fun Fact" + specific "Fun Fact: Shannon's Guessing Game"). Caused by earlier fix scripts adding titles without checking for existing ones.
- **Requested**: 2026-03-29
- **Completed**: 2026-03-29
- **Result**: 622 duplicate pairs merged across 288 files. Kept more specific title in each case.

### TASK-114: Illustration caption standardization
- **Status**: DONE
- **Priority**: MEDIUM
- **Description**: Remove inline styles from figcaption and figure elements. Add class="illustration" to bare figure tags. Add loading="lazy" to all figure images. CSS is single source of truth.
- **Requested**: 2026-03-29
- **Completed**: 2026-03-29
- **Result**: 5 figcaption inline styles removed, 1 bare figure fixed, loading="lazy" added across 213 files.

### TASK-115: Missing illustration images (146 placeholders)
- **Status**: PENDING (blocked on TASK-110)
- **Priority**: MEDIUM
- **Description**: 146 img tags reference images that don't exist on disk, across 83 files. Concentrated in Parts 3-7 (modules 08-26). These are illustration placeholders added to HTML but never generated. Requires Gemini image generation.
- **Requested**: 2026-03-29

### TASK-116: Deep standardization (code language classes, heading hierarchy, callout title attrs)
- **Status**: DONE
- **Priority**: MEDIUM
- **Description**: Deep audit found 1,400 remaining issues. Fixed: CODE_NO_LANGUAGE (726 code blocks in 214 files), DEEP_HEADING (303 h4/h5/h6 in 63 files), CALLOUT_NO_TITLE_ATTR (100 in 70 files), EM_DASH/DOUBLE_DASH (10 in 5 files). Remaining 271 issues are mostly in non-content files (agents/, _lab_fragments/) or multi-line false positives.
- **Requested**: 2026-03-29
- **Completed**: 2026-03-29

### TASK-117: Deep philosophical key-insight sweep
- **Status**: IN_PROGRESS
- **Priority**: MEDIUM
- **Description**: Add thought-provoking key-insight callouts connecting concepts to information theory, cognitive science, physics, economics, etc. Targeting Parts 1-6.
- **Requested**: 2026-03-29

### TASK-118: Tip callout expansion
- **Status**: DONE
- **Priority**: MEDIUM
- **Description**: Only 2 tip callouts in entire book. Sweep all sections to add practical practitioner tips (debugging shortcuts, parameter settings, rules of thumb).
- **Requested**: 2026-03-29
- **Completed**: 2026-03-29
- **Result**: 114 tip callouts added across all parts (Part 1: 21, Part 2: 15, Part 3: 11, Part 4: 16, Part 5: 12, Part 6: 12, Part 7: 7, Part 8: 10, Part 9: 6, Part 10: 2). Total tips now: 116.

### TASK-119: Cross-reference unlinked technical terms
- **Status**: DONE
- **Priority**: MEDIUM
- **Description**: 38 key terms (softmax, perplexity, temperature, cross-entropy, etc.) used in 5-141 files but rarely or never cross-referenced to their explanation chapters.
- **Requested**: 2026-03-29
- **Completed**: 2026-03-29
- **Result**: 657 cross-reference links added across 237 files. First-occurrence linking for 38 terms with safeguards (no self-linking, skips code/pre/svg/headings, context-aware for ambiguous terms).

### TASK-120: Python library code examples sweep (round 2)
- **Status**: IN_PROGRESS
- **Priority**: MEDIUM
- **Description**: Fresh sweep for library code snippets covering tiktoken, datasets, accelerate, bitsandbytes, peft, vllm, guidance, ragas, chromadb, sentence-transformers, unsloth, mergekit, dspy, instructor, litellm, etc.
- **Requested**: 2026-03-29

### TASK-121: Math typesetting with KaTeX
- **Status**: DONE
- **Priority**: MEDIUM
- **Description**: Researched MathML, KaTeX, MathJax, CSS-only. Selected KaTeX (lightweight, offline, textbook-quality). Downloaded v0.16.21 to vendor/katex/. Converted all formulas from HTML entities to LaTeX. Updated CSS for KaTeX integration.
- **Requested**: 2026-03-29
- **Completed**: 2026-03-29
- **Result**: KaTeX tags added to 458 files. 194 math blocks + 608 inline math converted to LaTeX. CSS updated (removed font overrides, added KaTeX display rules). Formulas now render with proper fractions, summation limits, square roots, and auto-sizing delimiters.

### TASK-123: Code syntax highlighting (Prism.js/highlight.js)
- **Status**: IN_PROGRESS
- **Priority**: MEDIUM
- **Description**: Add JS-based syntax highlighting for all 726+ code blocks. Auto-colors Python, bash, JSON, SQL, YAML, JS, HTML. Local bundle in vendor/, single source of truth.
- **Requested**: 2026-03-29

### TASK-124: Connecting prose between consecutive math blocks
- **Status**: IN_PROGRESS
- **Priority**: MEDIUM
- **Description**: 21 consecutive math-block pairs in 9 files have no connecting text. Adding brief explanatory phrases between formulas.
- **Requested**: 2026-03-29

### TASK-125: Inline math wrapping and cleanup
- **Status**: DONE
- **Priority**: MEDIUM
- **Description**: Wrap unwrapped inline math expressions (variables with sub/superscripts) in span.math. Fix nested math spans.
- **Requested**: 2026-03-29
- **Completed**: 2026-03-29
- **Result**: 245 expressions wrapped in 48 files. 31 nested spans fixed in 17 files.

### TASK-122: Math container CSS design
- **Status**: DONE
- **Priority**: MEDIUM
- **Description**: Designed standardized math-block container in book.css: gradient background, left accent border, serif fonts, label support, where-clause support, responsive and print rules.
- **Requested**: 2026-03-29
- **Completed**: 2026-03-29
- **Result**: CSS updated for .math-block (styled container), .math-block-label (formula names), .math-where (variable definitions). All 194 existing math blocks automatically styled.

### TASK-126: Fix empty space in content boxes (whats-next, callout, prereqs)
- **Status**: DONE
- **Priority**: HIGH
- **Description**: h2 elements inside .whats-next, .callout, .prereqs, .objectives, .outcomes had 3rem top margin from generic h2 rule, creating excessive empty space. Added CSS overrides to reset heading margins inside content boxes.
- **Requested**: 2026-03-29
- **Completed**: 2026-03-29
- **Result**: CSS rules added to book.css resetting h2/h3 top margins inside all content box types.

### TASK-127: TOC header and box cleanup
- **Status**: DONE
- **Priority**: HIGH
- **Description**: Remove prereqs/outcomes boxes from toc.html. Simplify header (drop subtitle). Remove header-nav border-bottom separation line globally.
- **Requested**: 2026-03-29
- **Completed**: 2026-03-29
- **Result**: 3 boxes removed from toc.html, header simplified to "Table of Contents", border-bottom removed from .header-nav.

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
