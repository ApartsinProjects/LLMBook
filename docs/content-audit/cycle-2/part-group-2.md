# Content Audit Cycle 2 - Parts 5-8

Audited 2026-05-17. Scope: Part 5 (modules 20-25), Part 6 (modules 26-30), Part 7 (modules 31-36), Part 8 (modules 37, 40, 41).

Cycle 1 fixed part-index breadcrumbs, second-half Ch 20/22/24 section breadcrumbs and pagefind-meta, Ch 41 stub content (Wave 14 rewrote it to cover Botpress/Rasa/Dialogflow/Voiceflow/LiveKit/Pipecat/etc., now solid). The chapter-index pages now show correct titles and section lists. Almost everything else is still stale.

The remaining problem set is **systemic and large**: nearly every prose cross-reference (in-body Chapter N / Section N.M citations), almost every figure caption, almost every code-fragment caption, almost every visible H2/H3 number, and most chapter-level next/prev nav buttons in Parts 5-8 still use the OLD numbering scheme (pre-renumber). Cycle 1 only fixed breadcrumbs and pagefind-meta on a subset of pages.

## Top remaining issues

1. **Visible H2/H3 numbers stale across nearly all of Parts 7 and 8**. The `id="32-1-1-..."` attribute is correct but the text content "23.1.1" / "24.1.1" / "23.2.1" / "42.1.1" is still the old numbering. Affects basically every section in modules 31-35 and modules 37/40, plus part of Ch 33 (uses old "42.X.X") and all of Ch 35 sec 35.1 (uses old "23.2.X"). Part 5 module 25 has BOTH the id stale (`id="33-..."`) AND text stale (`"43.1.1"`).

2. **Chapter-level next/prev nav widely wrong**. Sampled across Part 5/7/8:
   - Ch 20 index `class="next"` says "Chapter 33 Video Generation" but href self-loops to its own folder.
   - Ch 21 prev points to Ch 20 with label "Chapter 33 Video Generation" (Ch 33 in the current numbering is in Part 7).
   - Ch 22 prev "Ch 34 Document Understanding", next "Ch 36 3D Generation".
   - Ch 23 prev "Ch 35 Vision-Language Models", next "Ch 37 Unified Multimodal and Omni Models" but href loops back to Ch 22.
   - Ch 24 prev "Ch 38 Streaming and Real-Time Multimodal" links to Part 8 module-40 (wrong cross-part link); next "Ch 40 LLM-Powered Robotics" self-loops to module-24.
   - Ch 25 prev "Ch 42" goes to Ch 33 (wrong part), next "Ch 44 LLM Evaluation" goes to Part 9 module-42.
   - Ch 32 prev "Ch 22" / next "Ch 24" (numbers stale; href correct).
   - Ch 33 prev "Ch 41 Embodied AI..." links to Part 5 module-24 (wrong); next "Ch 43" links to module-25.
   - Ch 37 prev "Ch 23 RAG", next "Ch 25 Tools of the Trade: Retrieval & Conversation Stack" (Ch 25 in current scheme is Part 5 Multimodal Tools; this is the OLD merged-tools title from before the split).
   - Ch 40 and Ch 41 indexes have NO prev/next chapter nav at all (only the "in part" link).

3. **Body-text "Chapter NN" citations are wrong nearly everywhere**. The full set of mappings I observed still unfixed:
   - "Chapter 22" used for Embeddings/VDB content (current Ch 31) - appears in `index.html` looking-back, sections 32.1, 31.1, 33.1, 33.2, etc.
   - "Chapter 23" used for RAG content (current Ch 32) - sections 31.8, 32.4, 33.2, 34.5, 34.2, 35.5, 37.1, 37.3, etc.
   - "Chapter 24" used for Conversational AI (current Ch 37) - sections 32.5, 35.5, 37.x index, 37.3, etc.; also the "Looking Back" callout of Ch 26 references "Chapters 22 through 24" for "general agent principles", which is doubly wrong (current Ch 22 is now VLMs).
   - "Chapter 25" used for "Tools of the Trade: Retrieval & Conversation Stack" (no such chapter exists; tools are split into Ch 30, 36, 41).
   - "Chapter 33" used for Video Generation (now Ch 20 sec 20.6-20.10) - sections 20.5, 20.10, 23.2, 21 index.
   - "Chapter 37" used for Unified Multimodal / Omni Models (now Ch 22 sec 22.6-22.9) - sections 22.9, 33.2, 33.4.
   - "Chapter 38" used for Streaming and Real-Time Multimodal (now Ch 40 sec 40.2-40.5) - sections 22.9, 33.4, Ch 24 index, 33.4.
   - "Chapter 39" used for VLA (now Ch 24 sec 24.1-24.6) - section 40.5.
   - "Chapter 40" used for LLM-Powered Robotics (now Ch 24 sec 24.7-24.13) - sections 24.1, 24.6, 24.13.
   - "Chapter 41" used for World Models (now Ch 24 sec 24.13 plus scattered) - sections 23.2 (x2), 24.6, 24.9, 24.13.
   - "Chapter 42" used for Cross-Modal RAG (now Ch 33) - section 40.5.
   - "Chapter 43" used for Multimodal Tools of the Trade (now Ch 25) - section 40.5.
   - "Chapter 13" used for LLM APIs (now Ch 11) - all Part 6/7/8 chapter index prereq lists, sections 27.1-27.5, 29.1 prereqs, 35.5, 37.2, 32.x.
   - "Chapter 14" used for Prompt Engineering (now Ch 12) - all chapter prereq lists, section 26.1.
   - "Chapter 15" used for some Part 3 topic (now Ch 13 Hybrid ML/LLM) - section 24.1, 26.1.
   - "Chapter 16" used for QLoRA / fine-tuning (now Ch 14 or 16 depending) - sections 24.2, 30.1, 30 index.
   - "Chapter 17" used for synthetic data - Ch 37 overview.
   - "Chapter 19" used in body bib ref - Ch 37 (Jurafsky textbook chapter 19, may have been older edition's chapter; current edition uses Ch 24, see Ch 41.5).

4. **Body-text "Section X.Y" citations stale in proportion**. Spot-check sample:
   - "Section 13.1" / "Section 14.1" / "Section 16.7" / "Section 18.7" used for old Part 3 / Part 4 sections (now 11.1, 12.1, etc.) - sections 25.1, 37.1, 37.3.
   - "Section 22.1" / "22.2" / "22.3" / "22.4" used for embeddings/VDB sections (now 31.1-31.5) - sections 32.1 (multiple), 33.1 (x3), 34.2, 34.5, 35.1, 35.2, 37.3, 32.3.
   - "Section 23.1" / "23.2" / "23.3" / "23.4" used for RAG sections (now 32.1, 32.2, 35.1, etc.) - sections 31.6, 33.2, 34.2, 34.5, 35.2, 32.3, 32.2 (prereqs), 32.2 figure caption "Figure 23.4.1".
   - "Section 24.1" / "24.3.1" used for conv AI sections - 33.3, 37.3 (visible H2 "24.3.1").
   - "Section 31.1" used in 33.1 (should be "Section 22.1" or "Section 22.6"... actually this is bizarre - 33.1 refers to "Section 31.1" for "vision-language patterns" but Section 31.1 is "Embedding Models" in current numbering).
   - "Section 32.5"/"32.6"/"32.7"/"32.8"/"32.9" - these DO NOT EXIST after the RAG split. Used in section 32.1 (link to "32.9" for citation), 32.2 ("see Section 32.5" comment in code), 32.2 (next-section link to "Section 32.5"), 32.3 (next-section "Section 32.6" linking to 35.5), 35.2 (cross-ref to "Section 32.7" linking to 35.3), 35.3 (cross-ref "Section 32.8" linking to 35.4 / "Section 32.5" linking to 32.2), 35.4 (cross-ref "Section 32.9" linking to 32.4), 34.5 (cross-ref "Section 23.3").
   - "Section 33.5" - referenced in 20.7, 20.8 (x2), 20.9 for "long-form / cinematic video"; current Ch 20 has section 20.10 covering this, not 33.5.
   - "Section 34.1" / "34.2" - used in 32.4 and 35.4 for "RAG & Agent Evaluation"; in current numbering eval lives in Part 9 Ch 42.
   - "Section 37.2" / "Section 37.4" - referenced for "fusion" topics that are now Ch 22 sec 22.6/22.7/22.8 (used in 33.1).
   - "Section 38.1" / "38.2" - referenced for streaming sections that are now Ch 40 sec 40.2/40.3 (used in 22.6, 22.9, 33.4).
   - "Section 40.1" / "40.2" / "40.1-40.6" - used for SayCan / Code-as-Policies / LLM-powered robotics (now Ch 24 sec 24.7+); appears in 24.1 (x2), 24.13.
   - "Section 42.1" / "42.2" - used for embeddings/eval in 32.4, 33.x.

5. **Figure captions still use OLD chapter numbers across many sections**. Cycle 1 fixed only Ch 20.6-20.10 / Ch 22.6-22.9 / Ch 24.7-24.13. Still stale:
   - Ch 21 (Document Understanding) sections 21.1-21.4: 11 captions of form "Figure 34.X.Y" (Ch 21 was previously Ch 34). Image src files also point to `images/figure-34-1-1.svg` etc., so the file references are also stale at the asset level.
   - Ch 22 sections 22.1-22.5: 9 captions of form "Figure 35.X.Y". Image src `images/figure-35-1-1.svg` etc.
   - Ch 23 sections 23.1-23.5: 11 captions of form "Figure 36.X.Y".
   - Ch 24 sections 24.1-24.6 (FIRST HALF, not yet fixed): 17 captions of form "Figure 39.X.Y".
   - Ch 24 section 24.12, 24.13: 3 more stale "Figure 39/40/41.X.Y".
   - Ch 31 all sections (31.1-31.5): 29 captions of form "Figure 22.X.Y".
   - Ch 32 sections 32.1-32.3: multiple stale "Figure 23.X.Y".
   - Ch 32 sec 32.2 has "Figure 23.4.1" in the agentic-RAG figure caption.
   - Ch 33: figures may need checking (didn't get explicit count).
   - Ch 35 sections 35.1-35.5: stale Figure 23.X.Y.
   - Ch 37 index & sections 37.1-37.4: 10+ captions of form "Figure 24.X.Y".
   - Ch 40 sections 40.2-40.5: 9 captions of form "Figure 38.X.Y".
   - Plus stray "Figure 33.2.1" in Ch 20.7.

6. **Code-fragment captions equally stale**. Sampled "Code Fragment 39.X.Y" across all of Ch 24 (including sec 24.7-24.13 that cycle 1 supposedly fixed, so check status), "Code Fragment 37.4.1" in 22.9, "Code Fragment 22-25.X" in Ch 31, 32, etc. Affects every code-block caption in Ch 24, Ch 31-32, parts of others.

7. **Chapter 25 (Multimodal Tools of the Trade) has the wildest mismatches**. Every H2 has BOTH a stale ID (`id="33-1-1-image-platforms"` - Ch 33 was old Video Generation) AND stale visible text (`43.1.1 Image platforms` - the chapter was at some point called Ch 43). So a reader sees "43.1.1" but a `#33-1-1-image-platforms` anchor link from elsewhere is what works. Affects all 5 sections, 17 H2s total.

8. **Chapter 36 (Retrieval Tools) is mostly EMPTY STUBS**. Sections 36.1-36.5 each contain ~3 placeholder H2s ("Foundation Libraries", "Orchestration and Glue", "Utility Packages" / "Commercial Platforms", "Open-Source Platforms", "Selection Criteria" / etc.) with one-sentence body paragraphs, no concrete tool names, no comparison tables, no code, no bibliography beyond a stock 3-entry list ("Building Effective Agents 2024 / Karpathy State of GPT / Open LLM Leaderboard"). Contrasts sharply with Ch 41 (Wave 14 rewrite) and Ch 30 (Agent tools) which are fully fleshed. This is the single biggest content gap in Parts 5-8.

9. **Ch 37 (Conv AI) all four section-card descriptions are still the generic "Conversational AI." placeholder** - same problem cycle 1 was meant to fix. So Ch 37 index sec cards now show:
   ```
   37.1 Dialogue System Architecture - "Conversational AI."
   37.2 Personas, Companionship and Creative Writing - "Conversational AI."
   37.3 Memory and Context Management - "Conversational AI."
   37.4 Multi-Turn Dialogue and Conversation Flows - "Conversational AI."
   ```

10. **Consolidation candidates from cycle 1 are ALL still present unchanged**:
    - Agentic RAG: 27.5 ("Agentic RAG: Retrieval-Augmented Agents") and 32.2 ("Deep Research & Agentic RAG") both cover Corrective RAG / Adaptive-RAG / Self-RAG. 27.5 explicitly says it "builds on the agentic RAG foundations from Section 23.4" (i.e., 32.2).
    - Memory: 26.6 ("Memory Architecture for Agents: Taxonomy, Storage, and Policies") with five-layer taxonomy vs 37.3 ("Memory & Context Management") with sliding window/summarization/MemGPT. Considerable overlap in MemGPT/Letta discussion.
    - Sim-to-real: 24.6 ("VLA Limitations" - has dedicated H2 "The Sim-to-Real Gap" with quantitative tables) and 24.13 ("Sim-to-Real Gap" - full section). 24.13 even references the Sim-to-Real Gap section by saying it bridges "Sections 40.1-40.6 and the actual deployment" (stale numbers).
    - GraphRAG: 35.2 ("RAG with Knowledge Graphs") has an explicit "Related coverage" callout saying "This topic is also discussed in Section 35.4 ('Section 32.7: GraphRAG (full treatment)')" - so the duplication is acknowledged in-text but not resolved.
    - Code-gen agents: 29.1 ("Code Generation Agents") opens with "29.1.1 The Rise of Code Agents", 29.4 ("Code/Work Workflows and Agentic Coding Systems") opens with "29.4.1 The Rise of Agentic Coding" and covers Claude Code, Cursor, Devin in depth. Heavy overlap.
    - Tools overlap: Ch 36 (retrieval tools, currently stubs) vs Ch 41 (conv-AI tools, now well-developed). Ch 41.2 includes LangChain/LangGraph/LlamaIndex as conversation orchestration; if Ch 36 ever gets filled in, the LangChain coverage in particular will be split awkwardly between the two.

## Per-chapter findings

### Ch 20 (Audio, Music, and Video Generation)
- Section 20.5 body: "Chapter 33 opens on the modality with the steepest 2025-2026 capability gain: video. Same flow-matching DiT..." - the "Chapter 33" here means the OLD Chapter 33 (Video Generation, now sec 20.6-20.10 of the same chapter). Fix to "The next part of this chapter" or similar.
- Section 20.7 body: "the capability matrix in Figure 33.2.1" - stale figure number.
- Section 20.8/20.9 body: "Section 33.5 covers long-form..." (x3 across these two files) - target is current sec 20.10.
- Section 20.10 body: "Chapter 33 ends here. The next chapters of Part 7 cover the rest of the multimodal-generation landscape: Chapter 34 covers document understanding, Chapter 35 covers vision-language models, Chapter 36 covers 3D and neural scene generation, and the later chapters (37 through 43) cover unified multimodal models, real-time streaming, vision-language-action models, robotics, world models, cross-modal RAG, and the production toolchain." - the entire what's-next paragraph is the OLD numbering: 34 -> 21, 35 -> 22, 36 -> 23, 37-43 -> 22 (omni)/40/24/24/33/25. Also "Part 7" should be "Part 5".
- Ch 20 index next-chapter nav: "Chapter 33 Video Generation" linking to self.

### Ch 21 (Document Understanding and OCR)
- Ch 21 index prev-nav: "Chapter 33 Video Generation" (should be Ch 20).
- Figures 34.1.1 to 34.4.2 stale (12 figures across 21.1-21.4). Some image filenames (`figure-34-1-1.svg`, `figure-34-2-1.svg`, etc.) also encode the stale chapter; renumbering would need either a filename rename or accepting filename mismatch.

### Ch 22 (Vision-Language and Omni Models)
- Ch 22 index nav: prev "Ch 34 Document Understanding" / next "Ch 36 3D Generation". Numbers stale.
- Section 22.1-22.5: figures captioned "Figure 35.X.Y" (9 captions). Image srcs `figure-35-1-1.svg` etc.
- Section 22.9 (Omni Models): body says "Chapter 37 closes here. Chapter 38: Streaming and Real-Time Multimodal goes deeper..." - both numbers stale (current Ch 22 / Ch 40). Plus a code comment "# See Section 38.2 for the full protocol walkthrough." (stale), and code-fragment caption "Code Fragment 37.4.1" (stale). Section 22.6 references "Section 38.1" (stale).

### Ch 23 (3D Generation and Neural Scenes)
- Ch 23 index nav: prev "Ch 35 Vision-Language Models" / next "Ch 37 Unified Multimodal and Omni Models" but href loops to module-22.
- All 5 sections: figures captioned "Figure 36.X.Y" (11 figures).
- Section 23.2 body: "world models in Chapter 41" (x2), "video diffusion model (see Chapter 33)" (x2) - all stale.
- Section 23.5 body: "Chapter 23 closes here. Chapter 37: Unified Multimodal and Omni Models shifts gears..." - first number is CORRECT (we're in Ch 23), second is stale.

### Ch 24 (VLA Models and LLM-Powered Robotics)
- Ch 24 index nav: prev "Ch 38 Streaming and Real-Time Multimodal" pointing to Part 8 module-40 (cross-part wrong), next "Ch 40 LLM-Powered Robotics" self-loops.
- Section 24.1 body: "three-tier robotics stack that you will see repeatedly through Chapters 39 and 40" (now: all part of Ch 24); "covered in Section 40.1 on SayCan and Section 40.2 on Code-as-Policies" (now: 24.7 / 24.8); "the top layer is Chapter 40's job" (now: this same chapter's second half). All in the same paragraph.
- Section 24.3 body: "Physical Intelligence and the SayCan school (Chapter 40)".
- Section 24.6 body: "world-model integration (covered in Chapter 41)", and the section closes with "Chapter 24 covered the policy layer... Chapter 40 moves up one layer to the planner..."
- Section 24.9 body: "Gaussian-splat scenes (covered in Chapter 41)".
- Section 24.13 body: "Chapter 40 closes the LLM-robotics arc that Chapter 24 began. Chapter 41 moves to world models..." and "bridge between the architectural content of Sections 40.1-40.6".
- Section 24.13 has a broken pagefind-meta tag on line 27: `<span class="pagefind-meta-injected" data-pagefind-meta="part:Part V: Multimodal LLMs" hidden=""></span>T: VLA Models and LLM-Powered Robotics" hidden=""></span>` - the `T:` artifact suggests a botched edit dropped the opening `<span ... data-pagefind-meta="chapter:Chapter 24`.
- Sections 24.1-24.6: stale "Figure 39.X.Y" captions (17 total). Sections 24.12-24.13: stale figs too. Code-fragment captions all stale "Code Fragment 39.X.Y".

### Ch 25 (Multimodal Tools of the Trade)
- All sections: H2 IDs `id="33-X-Y-..."` (33 was old Video Generation), visible text `43.1.1` / `43.1.2` etc. (43 was something else). Neither matches the current chapter number. 17 H2s affected across 5 sections.
- Section 25.1 body: references "Section 13.1" (x2) for LLM APIs (now 11.1) and "Section 16.1" for tools-of-the-trade Part 3 (now 14.1). Linked correctly (href is right) but the visible "Section 13.1" / "Section 16.1" text is stale.

### Ch 26 (AI Agent Foundations)
- Ch 26 index looking-back: "Parts I through V built up to 'an LLM that retrieves, fine-tunes, and converses.' Part VI takes the final step: an LLM that acts. This chapter is the canonical home for the agent loop... that everything in Chapters 21 through 24 specializes." - "Chapters 21 through 24" was the old numbering for downstream agent specializations; in current numbering Ch 21-24 are document AI / VLMs / 3D / VLA, so this is nonsense.
- Ch 26 prereq references "Chapter 13" / "Chapter 14" (stale).
- Section 26.1 body: "the prompt patterns from Chapter 14 become full systems" (stale -> 12); "Chapter 15" reference to hybrid ML/LLM (stale -> 13).
- Section 26.6 prereqs say: "the memory overview in Section 26.1 and the MemGPT/Mem0 systems discussed in Section 26.6" - 26.6 IS this section, so it's a self-reference. "Embeddings and VDB from Chapter 22" (-> 31) and "RAG from Section 23.1" (-> 32.1).

### Ch 27 (Tool Use, Function Calling & Protocols)
- All sections 27.1-27.5 (and 27.6): boilerplate prereq paragraph at top says "builds on agent foundations from Chapter 26 and LLM API basics from Chapter 13" - "Chapter 13" stale.
- Section 27.5 (Agentic RAG): callout text refs "the agentic RAG foundations from Section 23.4" (stale - target is now 32.2). Big-picture text says "covers Corrective RAG (CRAG), Adaptive-RAG, and Self-RAG" - confirming overlap with 32.2.
- Section 27.6 prereqs: references "Chapter 11" for interpretability (currently Ch 10, possibly correct... need verification).

### Ch 28 (Multi-Agent Systems)
- Prereq list: "Chapter 14: Prompt Engineering" stale.

### Ch 29 (Specialized Agents)
- Index `<meta description>` text: "While Chapters 22 through 24 cover general agent principles..." STALE - Ch 22-24 are not agents in current numbering.
- Looking-back: "Chapters 20-22 covered agents as a general pattern" - STALE.
- Big-picture callout body: "While Chapters 22 through 24 cover general agent principles" - STALE.
- Prereq: "Chapter 13: LLM APIs" - STALE.
- What's Next: "In the next chapter, Chapter 26: Agent Safety and Production" but the href goes back to module-26-ai-agents (which is THIS Chapter 26 = AI Agent Foundations). Either the link or the text is wrong. There's no "Agent Safety and Production" chapter in Part 6 (chapters are 26-30 = Agents, Tools, Multi-Agent, Specialized, Tools-of-Trade).
- Section 29.1 vs 29.4: heavy code-agent overlap; consolidation candidate.

### Ch 30 (Tools of the Trade: Agent Stack)
- Index section-desc: "Agentic systems run on top of LLM API platforms (Chapter 16)" - "Chapter 16" stale (was Tools of the Trade in Part 3, now Ch 14).
- Section 30.1 body and `<meta description>` repeat the same Chapter 16 reference.
- Other sections OK (didn't find more).

### Ch 31 (Embeddings, Vector Databases & Semantic Search)
- Ch 31 index next-chapter nav: "Chapter 23 RAG" (stale -> 32).
- Ch 31 overview body: "Everything in Chapter 23 (RAG) and Chapter 24 (Conversational AI) sits on this layer." and "This chapter provides the retrieval infrastructure that powers RAG systems in Chapter 23 and grounds the conversational AI systems in Chapter 24." - both stale.
- Ch 31 prereq: "Chapter 13: LLM APIs" - stale.
- Ch 31 index figure caption: "Figure 22.0.1" (chapter opener).
- All 5 sections: 29 stale "Figure 22.X.Y" captions, 5 stale H2 IDs `id="31-X-Y-..."` but visible text "22.1.X" (cycle 1 likely fixed the id-side but not the displayed h2 text).
- Section 31.8 closing What's Next: "In the next chapter, Chapter 23: RAG..." (stale).

### Ch 32 (RAG Fundamentals)
- Ch 32 index nav: prev "Ch 22 Embeddings VDB" (-> 31), next "Ch 24 Building Conversational AI" (-> 37). Numbers stale.
- Ch 32 index: figure caption "Figure 23.0.1", body "Building on the embedding and vector database foundations from Chapter 22", prereq "Chapter 22... Chapter 13... Chapter 14".
- Ch 32 index What's Next: "In the next chapter, Chapter 24: Conversational AI".
- Sections 32.1-32.4 all have "Chapter 22" / "Chapter 23" / "Section 22.X" / "Section 23.X" cross-refs.
- Section 32.1 body: bizarre stale ref - "(citation hallucination, covered in Section 32.9)" but the link target is section-32.5.html. So the displayed "Section 32.9" is also stale, AND there's no 32.9 (the chapter only goes to 32.4).
- Section 32.3 (Agentic RAG): all H2/H3 visible numbers start "23.4.1", "23.4.2" etc. Figure "Figure 23.4.1". Prereqs reference "Section 14.1" / "Section 26.1" / "Section 32.3" (self).
- Section 32.3: contains code comment "# Text-to-SQL pipeline (covered in Section 32.5)" - 32.5 doesn't exist (text-to-SQL is now 32.3).
- Section 32.3 What's Next: "In the next section, Section 32.5: Structured Data & Text-to-SQL" - link goes to 32.3.html. Number stale.
- Section 32.4 What's Next: "In the next section, Section 32.6: RAG Frameworks & Orchestration" - link goes to module-35-advanced-rag/section-35.5.html (cross-chapter), but text says "Section 32.6". So the user reads "Section 32.6 in this chapter" but is moved to Section 35.5 in the next chapter.
- Section 32.5 closing: "In Chapter 24: Building Conversational AI Systems, we apply the retrieval and generation techniques..." (stale).

### Ch 33 (Cross-Modal Reasoning and Multimodal RAG)
- Ch 33 index nav: prev "Ch 41 Embodied AI, World Models & Multimodal Reasoning" linking to part-5 module-24 (catastrophic cross-part wrong link), next "Ch 43 Tools of the Trade: Multimodal Stack" linking to part-5 module-25.
- Section 33.1: H2/H3 numbering "42.1.1", "42.1.2", etc.
- Section 33.1 body: refers to "Section 22.1", "Section 31.1", "Section 37.2" all stale.
- Section 33.2 (Multimodal RAG): refers to "Chapter 23" for RAG and "Section 31.1" for VLMs and "Section 37.4" for omni - all stale; also "Section 23.1" for retrieve-then-rerank.
- Section 33.3: "Section 24.1" for agent patterns (stale).
- Section 33.4 body: "the integrated product of every chapter in Part VII. The right architecture is a composition of patterns from Chapter 31 (multimodal LLMs), Chapter 37 (pipeline vs native), Chapter 38 (streaming), and this chapter" - "Part VII" is correct, "Chapter 31" / "Chapter 37" / "Chapter 38" all stale (-> 22 / 22 / 40).
- Section 33.4 body: "Section 38.2" reference.

### Ch 34 (Structured Information Extraction & NER)
- Section 34.2 body: "RAG systems (Section 23.4)" (stale -> 32.2), "Section 22.3" for entity linking (stale -> 31.3).
- Section 34.5 body: "RAG systems (Chapter 23)" (stale, x2 occurrences); "Section 22.3" (stale, x3); "Section 22.1" (stale); "RAG pipelines (Section 23.3)" (stale - 23.3 was old chunking section).
- Section card description in Ch 34 index: 34.3 desc is "Why this matters for production pipelines." (placeholder-like); 34.5 desc is "Consider the following passage: 'Dr." (mid-sentence truncation, likely auto-derived from body).

### Ch 35 (Advanced RAG)
- Section 35.1: visible H2/H3 text uses "23.2.1", "23.2.2", etc. (old Ch 23 sec 2 numbering). IDs correctly use 35-1-X.
- Section 35.1 body: prereqs reference "Section 22.1" / "Section 22.4" (stale -> 31.X).
- Section 35.3: "Related coverage" callout points to "Section 32.7: GraphRAG (full treatment)" but link goes to 35.3. "Section 22.2" / "Section 22.4" / "Section 32.3" body refs.
- Section 35.4 body: cross-ref "Section 32.8: RAG Ingestion Pipelines and Connectors" linking to 35.4 (so prose number stale); "Section 32.5: Deep Research & Agentic RAG" linking to 32.2 (the visible number is stale for this rename - 32.2 is current).
- Section 35.5 body: "Section 32.9: Source Attribution and Citation in RAG" linking to 32.4; "Section 34.1: RAG & Agent Evaluation" linking to part-9 42.1.
- Section 35.5: cross-ref to "Chapter 13" (hybrid ML/LLM, stale).
- Section 35.5 What's Next: "Chapter 24: Building Conversational AI Systems".

### Ch 36 (Retrieval Tools of the Trade)
- **Critical: Empty stub chapter**. All 5 sections (36.1-36.5) have:
  - 3 placeholder H2s with one-line body text.
  - Generic big-picture callouts that just repeat the section description.
  - A boilerplate 3-entry bibliography (Anthropic / Karpathy / Open LLM Leaderboard) identical across all 5 sections.
  - No tool comparisons, no specific platform names, no code, no quantitative tables.
- Chapter index section-desc texts ("Hosted and open-source platforms..." etc.) are equally generic.
- Authoring needed: this chapter should mirror Ch 41's structure with concrete tools (Pinecone, Weaviate, Qdrant, Milvus, Chroma, Vespa, LanceDB, FAISS, etc. for platforms; LangChain, LlamaIndex, Haystack, dspy, etc. for libraries; BEIR, MTEB, MS MARCO, FiQA, etc. for benchmarks).

### Ch 37 (Building Conversational AI Systems)
- All 4 section cards have generic "Conversational AI." description (placeholder).
- Looking-back: "RAG (Chapter 23)" (stale).
- Overview body: "synthetic data techniques from Chapter 17" (Ch 17 is now LLM Alignment, the synthetic data ch is somewhere else - verify).
- Big-picture body: "chat, skills that connect directly to the agent architectures in Part VI" - actually fine (Part 6 = agents).
- Prereq list: Chapter 13 / 14 / 23 - all stale.
- What's Next: "In the next part, Part VI: Agentic AI..." which is incorrect (Part 6 came BEFORE Part 8 in current ordering; next should be Ch 40 Voice & Realtime Multimodal in the same Part 8).
- Chapter nav: prev "Ch 23 RAG" (stale text, href correct), next "Ch 25 Tools of the Trade: Retrieval & Conversation Stack" (the title is also stale; there's no merged retrieval+conversation tools chapter, only Ch 41 conv tools).
- Section 37.1 figures all "Figure 24.X.Y" (stale, 3 figs). Visible H2s "24.1.1" through "24.1.7" (IDs correct).
- Section 37.1 body: "Section 14.1" (stale), "Chapter 23 RAG patterns" (stale).
- Section 37.2 figures "Figure 24.2.X" (3 stale).
- Section 37.2 body: "system prompt design principles from Section 12.1 (in Chapter 13)" (text says "Chapter 13" but link is to module-11; the visible "13" is stale).
- Section 37.3 figure "Figure 24.3.1", H2 "24.3.1".
- Section 37.3 big-picture: "Section 18.7" (stale - should be 16.7 or similar).
- Section 37.3 prereq: "Section 22.1" (stale), "Section 13.2" (stale).
- Section 37.3 body: "Chapter 22" for embeddings (stale).
- Section 37.1 bib: "Jurafsky & Martin Chapter 19: Chatbots and Dialogue Systems" but Ch 41.5 cites Chapter 24 of the same book. One of these external refs is to an older edition; pick one and standardize. The 3rd-edition Jurafsky online uses Ch 24, so 37.1 should say Ch 24.

### Ch 40 (Voice and Realtime Multimodal Assistants)
- Sections 40.2-40.5: 9 figures captioned "Figure 38.X.Y" (Ch 40 was previously Ch 38).
- Section 40.1: H2 IDs use `id="37-6-1-..."` to `id="37-6-3-..."` (the numbering when Ch 40 was sec 6 of old Ch 37 Conv AI). Visible H2 text "24.6.1" / "24.6.2" / "24.6.3" (even older numbering).
- Section 40.5 closing: "Chapter 39 closes here. The next chapters in Part VII (39, 40, 41) cover Vision-Language-Action models, LLM robotics, and world models, then we return to Chapter 42 for cross-modal RAG." - this entire paragraph is the OLD Part 7 mega-chapter structure. None of these chapters exist in Part 8 / current numbering.

### Ch 41 (Conversational AI Tools of the Trade)
- **Largely solid (Wave 14 rewrite worked).** Content fully covers Botpress, Rasa, Dialogflow CX, Lex, Voiceflow, OpenAI Custom GPTs, Anthropic Projects, LiveKit, Pipecat, Vocode, Retell, Bland, etc. (sec 41.1); LangChain conv memory, LangGraph, OpenAI Assistants, Chainlit, etc. (sec 41.2); MultiWOZ, PersonaChat, MT-Bench, LMSYS Chatbot Arena (sec 41.3); models (sec 41.4); reading & communities (sec 41.5).
- Only stale ref I found: 41.1 sec, line 144 - "(Section 31 in Part VII covers the relevant tooling)". This is grammatically odd ("Section 31") and the numbering is stale. Should be Section 36.X or just removed.
- 41.5 cites "Jurafsky & Martin Chapter 24" correctly.
- Heading IDs use 41-X-Y correctly. Visible H2 text uses 41.X.Y correctly. Figures: none in this chapter (mostly text).

## Suggested cycle 3 actions

These can be tackled by a scripted sweep rather than per-section manual edits, since the patterns are mechanical.

1. **Body-text Chapter/Section renumbering sweep**. Build a global remap:
   - "Chapter 13" -> 11, "Chapter 14" -> 12, "Chapter 15" -> 13, "Chapter 16" -> 14 (Part 3 tools), "Chapter 17" -> verify, "Chapter 19" (Jurafsky cite) -> 24.
   - "Chapter 22" -> 31, "Chapter 23" -> 32, "Chapter 24" -> 37, "Chapter 25" -> (delete, no such chapter; usually means Ch 30/36/41).
   - "Chapter 33" -> 20 (second half), "Chapter 34" -> 21, "Chapter 35" -> 22 (first half), "Chapter 36" -> 23.
   - "Chapter 37" -> 22 (second half / omni), "Chapter 38" -> 40, "Chapter 39" -> 24 (first half), "Chapter 40" -> 24 (second half), "Chapter 41" -> 24 (world-model parts) or removal where it refers to a no-longer-existent world-models chapter, "Chapter 42" -> 33, "Chapter 43" -> 25, "Chapter 44" -> 42 (Part 9 eval foundations).
   - Apply to in-body prose and to `class="nav-num"` text. Cross-check by inspecting the `href` and using THAT as the source of truth.

2. **Section X.Y renumbering sweep**. Treat each link as `(visible_text, href)`. If the href points to `section-N.M.html` and the visible text says "Section A.B" with A.B != N.M, replace the visible text with the href-derived number. This is a deterministic transformation. Apply across all of Parts 5-8.

3. **Visible H2/H3 text renumbering**. For each `<h2 id="N-M-K-..."> ...visible text X.Y.Z ...`, where N.M.K and X.Y.Z differ, replace X.Y.Z with N.M.K (with dots). Same for H3. The ids are authoritative.

4. **Figure & Code Fragment caption renumbering**. Rewrite every `<strong>Figure A.B.C</strong>` and `<strong>Code Fragment A.B.C</strong>` to use the chapter number of the containing section (`section-N.M.html` -> chapter N). Counter order can be preserved. Note: image filenames like `figure-34-1-1.svg` are file-system level and can stay as-is (link integrity), but if a cleanup pass is desired they could be renamed in parallel.

5. **Chapter nav prev/next reconstruction**. For each chapter's `index.html`, set:
   - prev = chapter (N-1) (or last chapter of previous part if N is first in part).
   - next = chapter (N+1) (or first chapter of next part).
   - Make the visible `nav-num` and `nav-title` match the actual target. Ch 40 and Ch 41 indexes need prev/next added (currently missing).

6. **Section card descriptions for Ch 37 index**. Replace four "Conversational AI." stubs with proper per-section descriptions drawn from each section's big-picture callout (37.1 dialogue architecture spectrum, 37.2 persona/companionship/co-writing, 37.3 memory/summarization/MemGPT, 37.4 multi-turn flows/clarification/recovery).

7. **Section card descriptions for Ch 34 index**. Rewrite 34.3 and 34.5 (currently auto-truncated junk) with proper one-line summaries.

8. **Ch 36 is a content gap, not a numbering bug**. Cycle 3 should either (a) author Ch 36 with concrete content paralleling Ch 30 / Ch 41, OR (b) consolidate Ch 36 into Ch 31/32/35 as "Tools" callouts and drop Ch 36 as a standalone chapter (the chapter index already says "Part VII Retrieval & IE" includes Ch 31-36, so dropping it requires a part-index update too).

9. **Ch 25 double-numbering**. Heading IDs (`id="33-X-Y"`) AND visible text (`43.X.Y`) BOTH need to be rewritten to `25-X-Y` / `25.X.Y`. Any inbound anchor links from elsewhere using `#33-1-1-image-platforms` will break - audit those before/after.

10. **Section 32.X "doesn't exist" cleanup**. After the RAG split, section 32 only has 4 sections (32.1-32.4). Yet body prose still references Section 32.5, 32.6, 32.7, 32.8, 32.9 (sometimes pointing to other chapters via href). Each reference needs an explicit decision:
    - If the topic moved to Ch 35: rewrite as "Section 35.X" and update href.
    - If consolidated into 32.1-32.4: rewrite as the appropriate current section.
    - If dropped entirely: remove the reference.

11. **Consolidation candidates from cycle 1 - decide and execute**:
    - Agentic RAG: keep one canonical home (probably 27.5 in Part 6, since "agentic" is the framing), and trim 32.2 to a brief "see Section 27.5 for the agent loop" callout while keeping the deep-research / corpus synthesis angle.
    - Memory: keep 26.6 (agent memory taxonomy) as the deep treatment, trim 37.3 to a "conversation memory specializations" callout that references 26.6.
    - Sim-to-real: 24.6 already says "this is one of three structural limitations"; 24.13 is the deep section. Trim 24.6's sim-to-real subsection to a paragraph forward-pointing to 24.13.
    - GraphRAG: 35.2 already explicitly says "see 35.4 for full treatment"; either fold 35.2 into 35.1 (as a sub-pattern of advanced RAG) or rewrite 35.2 as motivation-only and let 35.3 do the work.
    - Code-gen agents: 29.1 and 29.4 are both substantial. Possibly retain 29.1 as the introductory "code agents as a category" + Self-Debugging Loop + Cursor-vs-Devin overview, and recast 29.4 as a "production agentic-coding workflow patterns" deep dive (it already covers Claude Code / IDE agents / fully autonomous in distinct H2s). Or merge into one larger section.
    - Tools overlap Ch 36 vs Ch 41: this is conditioned on whether Ch 36 ever gets authored (action 8 above).

12. **Fix the broken `<span>` in section-24.13.html line 27** (the leftover `T:` artifact from a botched edit).

13. **Stale image filenames** (`figure-34-1-1.svg`, `figure-35-X-Y.svg`, etc.) - optional cosmetic cleanup. Functionally fine; cosmetically misleading.

14. **Ch 26 looking-back text "everything in Chapters 21 through 24 specializes" makes no semantic sense in current numbering** (Ch 21-24 = doc AI, VLMs, 3D, VLA - none about agents). The full callout text needs rewriting, not just a number swap.

15. **Ch 29 What's Next link/text mismatch**: "Chapter 26: Agent Safety and Production" linking to module-26-ai-agents (which IS Ch 26, but its title is "AI Agent Foundations" not "Agent Safety"). Either the next chapter is Ch 30 (Tools of the Trade), which the chapter nav says, or there's a missing/dropped "Agent Safety" chapter that the What's Next text expects. Reconcile.
