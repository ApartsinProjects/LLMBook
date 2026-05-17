# Content Audit — Parts 5-8

This audit reviews titles, descriptions, section-home fit, ordering, and stale references across Parts 5-8 after waves 1-9 of the restructure. Read-only audit; no edits made.

## Top-level observations (apply throughout)

These appear systematically in every chapter / section file across parts 5, 6, 7, and 8 and dominate the findings list. Wherever individual entries below say "stale breadcrumb / placeholder desc", these patterns are the cause:

1. **Breadcrumbs / pagefind-meta still show old part names.** Every section in:
   - part-5 (modules 20-25) and part-7 modules 33 → breadcrumb says `Part VII: Multimodal Generation`.
   - part-7 modules 31, 32, 35 → breadcrumb says `Part V: Retrieval and Conversation with LLMs and Agents`.
   - part-8 modules 37, 40 (some sections), 41 → breadcrumb says `Part V: Retrieval and Conversation with LLMs and Agents` (37 + 41) or `Part VII: Multimodal Generation` (most of 40).
   - Many also have `<title>` `data-pagefind-meta="part:"` attributes pointing to the old part. These are search-index facing and should be fixed when sections are next touched.
2. **Section-card descriptions are still placeholders in many chapters.** Specifically:
   - `module-25-tools-of-the-trade` (Part 5) → 5/5 sections say "A chapter from the Building Conversational AI textbook."
   - `module-26-ai-agents` → 6/6 sections.
   - `module-27-tool-use-protocols` → 5/6 sections (27.6 is the only one with a real description).
   - `module-28-multi-agent-systems` → 4/4 sections.
   - `module-29-specialized-agents` → 4/4 sections.
   - `module-30-tools-of-the-trade` (Part 6) → 5/5 sections.
   - `module-31-embeddings-vector-db` → 5/5 sections.
   - `module-32-rag` → 4/4 sections say "RAG fundamentals."
   - `module-34-structured-information-extraction-ner` → 5/5 sections say "Promoted from old section 15.5."
   - `module-35-advanced-rag` → 5/5 sections say "Split from old Ch 32 RAG monster."
   - `module-37-conversational-ai` → 4/4 sections say "Conversational AI."
   - `module-40-voice-realtime-multimodal` → 5/5 sections say "Voice and realtime multimodal AI."
   - `module-41-conv-ai-tools` → 5/5 sections say "Conv AI tooling."
   These are all restructure artifacts that need real one-line section descriptions.
3. **Chapter-navigation (prev/next/up) is broken in many chapters.** Examples called out individually below; the pattern is that `<nav class="chapter-nav">` references neighbour chapters by the old numbering, the old chapter titles, or links to a sibling that no longer exists. A bulk pass would catch most of them.
4. **Part index pages (`part-N/index.html`) all show `<!-- Chapter cards added by rebuild script -->` placeholders.** The rebuild script never re-ran after the restructure, so:
   - Part 5 index has no chapter cards at all.
   - Part 6 index has chapter cards but the prose mentions "Chapter 38 within Part IX" for agent safety (stale).
   - Part 7 index only includes manually-pasted cards for Chapters 34, 35, 36; Chapters 31, 32, 33 are missing from the index.
   - Part 8 index only includes manually-pasted cards for Chapters 40 and 41; Chapter 37 is missing.
5. **Big-picture descriptions at the Part level are duplicated.** Part 5, 7, 8 all have an `<h2>Part Overview</h2>` paragraph followed by a `<div class="callout big-picture">` with the same sentence (sometimes word-for-word). Real big-picture text should expand beyond the one-line summary, or one of the two should be removed.
6. **Module-26 and chapter-index "what's-next" pointers are wrong** in several chapters (Module 29 says "Chapter 26: Agent Safety", but Chapter 26 is AI Agent Foundations; Module 30 says "Part VII turns to multimodal generation" but Part 6 comes after Part 5, not before Part 7's multimodal content; Module 32 says "next part is Chapter 24" but it should be Chapter 37 in Part 8; etc.).

The audit below highlights the *additional* issues per chapter beyond these systemic ones. If a chapter has only the systemic findings above, it gets a one-liner.

---

## Part 5: Multimodal LLMs

**Part-level findings.**
- Part index `part-5-multimodal-llms/index.html` has no chapter cards (only a placeholder comment). Add 6 cards for Chapters 20-25.
- The `<title>` tag still says "Part V: Multimodal LLMs". Spine is now Part 5 / Part V — that is consistent.
- Big-picture paragraph duplicates the meta description; expand it (e.g., "Part 5 covers everything outside text: how models read pixels, audio, video, and 3D scenes, how those modalities are tokenized, how they connect to the text transformers from Parts 1-4, and what production stacks look like for image, video, audio, music, document AI, vision-language reasoning, 3D, and robot policies.").

### Chapter 20: Audio and Music Generation

**MAJOR ISSUE — chapter is two chapters glued together.** Sections 20.1-20.5 are audio/TTS/music/ASR (the "audio and music generation" content the title promises); sections 20.6-20.10 are about **video generation** (Video DiTs, Sora/Veo/Runway, video control, video editing, long-form cinematic video). The breadcrumbs in 20.6-20.10 explicitly say "Chapter 33: Video Generation". The index file lists only sections 20.1-20.5 and ignores 20.6-20.10 entirely.

This is the most consequential structural problem in Part 5. Two options:

- **Option A (recommended):** Split into Chapter 20 "Audio, Speech, and Music Generation" (5 sections) and a new chapter "Video Generation" (5 sections, currently 20.6-20.10 → renumber). This restores the audio-only scope the title promises and gives video the chapter it deserves.
- **Option B:** Rename Chapter 20 to "Audio, Speech, Music, and Video Generation" (or "Generative Audio and Video") and update the index to list all ten sections. Less clean but minimally invasive.

Specific findings assuming the chapter stays merged for now:

- **Title**: PROPOSE "Audio, Speech, Music, and Video Generation" (current title hides the entire video half of the chapter).
- **Description (big-picture)**: PROPOSE expanding from "TTS, voice cloning, music generation, audio editing, and the production stack for synthetic audio." to cover the video half too: "Generative models for time-series media: TTS and voice cloning (VITS, Bark, F5-TTS), music generation (Suno, Udio, MusicGen), audio editing and ASR, and video generation (DiTs, Sora, Veo, Runway), camera control, video editing, and long-form cinematic synthesis."
- **Index file is missing 5 sections.** `module-20-audio-music-generation/index.html` lists only 20.1-20.5; sections 20.6-20.10 exist on disk and are linked into from elsewhere but have no card on the chapter index.
- **Section descriptions** in the index card list are real text for 20.1-20.5; need cards added for 20.6 (Video DiTs), 20.7 (Leading Video Models), 20.8 (Camera/Motion Control), 20.9 (Video Editing), 20.10 (Long-Form Video).
- **Ordering**: If kept merged, the obvious order is 20.1-20.5 audio then 20.6-20.10 video, which matches the current file numbering. Otherwise, propose moving 20.5 (ASR) to the end of the audio block (after generation, since it is the input modality, fits better as a hinge into video) or to Chapter 22 (it currently feels like a misfit beside TTS-and-music-generation).

**Stale refs (with file:line and fix):**
- `section-20.1.html:36` Big-picture says "This section is the foundation for everything that follows in Chapter 20: cloning (Section 20.2), music (Section 20.3), editing (Section 20.4), and ASR (Section 20.5)." That is correct for the audio half; mention video too, or rewrite as "for the audio half of Chapter 20".
- `section-20.4.html:36` Big-picture references "Sections 32.1-32.3" → should be Sections 20.1-20.3.
- `section-20.5.html:36` Big-picture: "the front door of every realtime conversational agent (Section 38 covers the realtime stack in detail)" → Section 38 no longer exists; should be **Chapter 40 (sections 40.2-40.5)** in Part 8.
- `section-20.6.html:35, 38` Breadcrumb says "Chapter 33: Video Generation" — should be Chapter 20.
- `section-20.7.html:35, 38` Same breadcrumb issue; also paragraph at line 36 says "the video DiT from Section 33.1" → should be Section 20.6.
- `section-20.8.html:35, 38` Same breadcrumb issue; "Section 33.3 covers in depth" → should be Section 20.8 (self-reference) or 20.10.
- `section-20.9.html:35, 38` Same breadcrumb issue; "DiT from Section 33.1" → 20.6; "Section 33.3" → 20.8.
- `section-20.10.html:35, 38, 40` Same breadcrumb issue; "Section 33.2 covered that frontier" → 20.7; "Part 7's later chapters on 3D and world models, especially Section 41.3" → this is now Section 23.x in Part 5. Also "Section 33.1" → 20.6.
- Figure numbering across the chapter still says `figure-32-X-Y` and `Figure 32.X.Y` (e.g., `section-20.1.html:48` "Figure 32.1.1"). Bulk-renumber to 20.X.Y.
- `nav.chapter-nav` in `index.html` says prev "Chapter 31 Multimodal Generation" and next "Chapter 33 Video Generation" — both stale.

### Chapter 21: Document Understanding and OCR

- **Title**: KEEP.
- **Big-picture**: PROPOSE expand. Current ("Modern OCR (TrOCR), layout-aware models, VLM-based document understanding, and document AI pipelines.") is a tag-list rather than a narrative. Suggested: "OCR has gone from a cascade pipeline to a single end-to-end transformer model. This chapter walks the journey from TrOCR through layout-aware encoders to frontier VLM-based document understanding and the production pipelines that compose them."
- **Section descriptions**: All four are real and acceptable. No placeholders.
- **Ordering**: KEEP (foundation → layout-aware → VLM → pipeline composition is a clean progression).
- **Stale refs:**
  - `section-21.4.html:40` Figure caption "Figure 34.4.1" — needs renumbering to 21.4.1.
  - Breadcrumbs throughout still say `Part VII: Multimodal Generation`.
  - `index.html:54-56` Chapter-nav says prev "Chapter 33 Video Generation" and next "Chapter 35 Vision-Language Models" — both stale.
- **Home fit**: Could argue that the VLM-based document understanding section (21.3) belongs more naturally in Chapter 22 (Vision-Language Models), and Chapter 21 should end with section 21.2 + 21.4 (the OCR/layout/pipeline track). But the current grouping reads coherently as "document AI at every level of abstraction" so KEEP unless a future Part 5 reorganization is on the table.

### Chapter 22: Vision-Language Models

**MAJOR ISSUE — chapter is two chapters glued together.** Sections 22.1-22.5 are vision-language models proper (ViT, CLIP, LLaVA, GPT-4V, MMMU). Sections 22.6-22.9 are about **Unified Multimodal / Omni Models**. The breadcrumbs in 22.6-22.9 explicitly say "Chapter 37: Unified Multimodal and Omni Models". The index lists only 22.1-22.5 and ignores 22.6-22.9.

- **Title**: PROPOSE "Vision-Language and Omni Models" (or split into Chapter 22 + new chapter "Unified Multimodal and Omni Models"; same trade-off as Chapter 20).
- **Big-picture**: PROPOSE expand. Current is the tag list "ViT, CLIP, SigLIP, BLIP-3, LLaVA, GPT-4V, and the multimodal reasoning landscape." Add a beat for omni models (pipeline vs native, early/late fusion, any-to-any, GPT-4o/Gemini 2/Llama-4-Omni/Chameleon).
- **Index file is missing 4 sections.** Add cards for 22.6 (Pipeline vs Native Multimodal), 22.7 (Early vs Late Fusion), 22.8 (Any-to-Any Generation), 22.9 (Frontier Omni Models).
- **Ordering**: VLMs → omni is the right order if kept merged. Within VLMs, 22.1 (ViT) → 22.2 (contrastive CLIP/SigLIP) → 22.3 (generative LLaVA) → 22.4 (frontier closed) → 22.5 (eval) is clean; within omni, 22.6 (pipeline vs native) → 22.7 (fusion spectrum) → 22.8 (any-to-any) → 22.9 (frontier omni) is clean.
- **Stale refs:**
  - `section-22.6.html:26, 29, 35` Breadcrumb still says "Chapter 37: Unified Multimodal and Omni Models". 
  - `section-22.6.html:40` Prerequisites: "the multimodal architectures from Section 31.1" → should be Section 20.1 or, more accurately, a vision-text section; "the transformer attention basics from Section 4.1" → Section 3.1; "Chapter 32" → Chapter 20.
  - `section-22.7.html:26, 29` Same breadcrumb issue. Section heading IDs say `22-7-1`, `22-7-2` but visible heading numbers say `37.2.1`, `37.2.2` (line 42, 49) — visible numbering is stale.
  - `section-22.7.html:39` Figure src `images/fig-37.2.1-fusion-spectrum.svg` and caption "Figure 37.2.1" → 22.7.1.
  - `section-22.7.html:47` "Section 42.1" → should be Section 33.1 (in Part 7 module-33).
  - `section-22.8.html:26, 29` Breadcrumb stale. Figure ID and caption "Figure 37.3.1" → 22.8.1.
  - `section-22.9.html:26, 29` Breadcrumb stale. Figure "Figure 37.4.1" → 22.9.1.
  - `section-22.6.html` Big-picture references `Section 31.1` (was multimodal arch) but in restructure the corresponding section is in module-20 or module-22 itself.

### Chapter 23: 3D Generation and Neural Scenes

- **Title**: KEEP.
- **Big-picture**: PROPOSE expand. "3D Gaussian Splatting, NeRF, Stable Zero123, Trellis, 4D splats, and scene relighting." is a tag list. Suggested: "Modern 3D generation has shifted from NeRF's slow rendering to 3D Gaussian Splatting's real-time radiance fields. This chapter covers the splatting math, dynamic and 4D extensions, image-to-3D via multi-view diffusion, native 3D diffusion (Trellis), and language-grounded scene editing and relighting."
- **Section descriptions**: All five are real and acceptable.
- **Ordering**: KEEP (fundamentals → dynamic extension → image-to-3D → native 3D diffusion → editing is a clean progression).
- **Stale refs:**
  - Breadcrumbs throughout still say "Part VII: Multimodal Generation".
  - `index.html:59-61` Chapter-nav prev says "Chapter 35 Vision-Language Models" and next says "Chapter 37 Unified Multimodal and Omni Models" — both stale.
  - Worth a quick grep for any "Section 41.3" or similar references that point to the 3D/world-model material now in 23.X.
- **Home fit**: Concerns. 3D and NeRF/Gaussian-splat material has a real connection to the world-model / VLA content in module-24, and section 23.5 (Scene Relighting & 3D Editing) is the kind of niche topic that might warrant a deeper Part 16 (research frontiers) home. But for an introductory pass keeping it in Part 5 is the right call.

### Chapter 24: Vision-Language-Action Models

**MAJOR ISSUE — chapter is two chapters glued together.** Sections 24.1-24.6 are VLA Models (RT-2, OpenVLA, pi-0, action tokenization, capability matrix, limitations). Sections 24.7-24.13 are about **LLM-Powered Robotics** (SayCan, Code-as-Policies, VoxPoser, multi-robot dispatch, ROS 2, planner comparison, sim-to-real). The breadcrumbs in 24.7-24.13 explicitly say "Chapter 40: LLM-Powered Robotics". The index lists only 24.1-24.6 and ignores 24.7-24.13.

- **Title**: PROPOSE "Vision-Language-Action Models and LLM Robotics" (or split into Chapter 24 + new chapter "LLM-Powered Robotics"). Same trade-off as chapters 20 and 22.
- **Big-picture**: PROPOSE expand. Current is the tag list "RT-2, OpenVLA, pi-0, action tokenization, cross-embodiment transfer, and VLA limitations.". Add the robotics-planning lineage if the chapter stays merged.
- **Index file is missing 7 sections.** Add cards for 24.7 (SayCan), 24.8 (Code-as-Policies), 24.9 (VoxPoser), 24.10 (Multi-Robot Dispatch), 24.11 (ROS 2 Integration), 24.12 (Comparing the Planners), 24.13 (Sim-to-Real Gap).
- **Section 24.3 description is a paragraph extraction error.** Index card text reads: "pi-0 is structurally a two-headed model. The first head is a vision-language model (a 2B-parameter PaliGemma-Mix-3B variant) that ingests one or more camera frames plus an instruction and emits a sequ" — clearly the description was auto-extracted from the first paragraph and truncated mid-word. Replace with a real one-liner: "Physical Intelligence's pi-0 / pi-0.5 architecture: PaliGemma backbone, flow-matching action head, dexterous-manipulation training mixture."
- **Section 24.13 vs 24.6 overlap.** Both sections cover the sim-to-real gap (24.6 is one paragraph as a "VLA limitation"; 24.13 is a full section on sim-to-real with a closing-the-gap playbook). When the chapter is split into two, this duplication is fine (one belongs to VLA, one to robotics). When kept merged, the 24.6 paragraph should be trimmed to a pointer to 24.13.
- **Ordering**: Within VLAs, 24.1 (equation) → 24.2 (OpenVLA) → 24.3 (pi-0) → 24.4 (RT-2-X data scaling) → 24.5 (comparison) → 24.6 (limitations) is fine. Within robotics, 24.7 (SayCan) → 24.8 (Code-as-Policies) → 24.9 (VoxPoser) → 24.10 (multi-robot) → 24.11 (ROS 2) → 24.12 (comparison) → 24.13 (sim-to-real) is chronologically and conceptually sound.
- **Stale refs:**
  - `section-24.1.html:37` Big-picture: "next-token factorization from Section 7.2" → that section number is now in Part 2 module-06 (likely Section 6.2). Verify in toc.
  - `section-24.7.html through 24.13` all have breadcrumbs and pagefind-meta saying "Chapter 40: LLM-Powered Robotics".
  - `section-24.10.html:31` Big-picture: "single-robot, single-LLM-planner stack from Sections 40.1-40.3" → these are now 24.7-24.9.
  - `section-24.12.html:31` Big-picture: "Sections 40.1-40.5" → these are now 24.7-24.11.
  - `section-24.13.html:31` Big-picture: "Sections 40.1-40.6" → these are now 24.7-24.12.
  - `index.html:64-66` Chapter-nav prev says "Chapter 38 Streaming and Real-Time Multimodal" (links to part-8 module-40) and next says "Chapter 40 LLM-Powered Robotics" (links back to module-24 itself — broken self-reference).

### Chapter 25: Tools of the Trade: Multimodal Stack

- **Title**: KEEP.
- **Big-picture**: KEEP. Current callout in `index.html` is a real narrative.
- **Section descriptions**: ALL 5 are placeholders ("A chapter from the Building Conversational AI textbook."). The chapter has decent content in the section bodies that can be summarized into one-liners. Suggested replacements:
  - 25.1 Platforms: "Hosted and open-source platforms for image, video, audio, and music generation: Midjourney, DALL-E, Imagen, FLUX, Sora, Veo, Runway, ElevenLabs, Suno."
  - 25.2 Libraries & Frameworks: "diffusers, transformers, ComfyUI, AudioCraft, the open-source multimodal toolbox."
  - 25.3 Datasets & Benchmarks: "LAION-5B, MMMU, AudioCaps, MUSDB18, the multimodal dataset and benchmark landscape."
  - 25.4 Models: "Open-weight image, video, audio, and music model checkpoints: which to pick at each capability tier."
  - 25.5 External Reading & Communities: "Conferences (CVPR, SIGGRAPH, NeurIPS), zines, Discords, blogs for staying current in multimodal AI."
- **Ordering**: Tools-of-the-trade chapters follow a fixed 5-section template across the book (Platforms → Libraries → Datasets → Models → External). KEEP.
- **Stale refs:**
  - All section breadcrumbs say "Part VII: Multimodal Generation".
  - `index.html:73` What-Comes-Next: "Part VIII turns to evaluation and production: how you measure what you have built and how you keep it running. Chapter 46 closes Part VIII with the eval and production stack." — multiple problems: Part 8 is now Conversational AI (not eval); the chapter that closes the eval part is Chapter 46? Need to verify; in the restructured book the evaluation part is Part 9 starting with Chapter 42.
  - `index.html:76-78` Chapter-nav says prev "Chapter 42 Cross-Modal Reasoning and Multimodal RAG" (links to part-7 module-33) and next "Chapter 44 LLM Evaluation & Quality Metrics" (links to part-9 module-42) — both stale chapter numbers, both wrong destinations for the canonical Part 5 → Part 6 transition.
  - `section-25.1.html:30` Key insight: "the way text-LLM platforms in Section 13.1 do" → Section 13.1 was old "LLM APIs"; current location is Part 3 module-11 (probably Section 11.1).
  - `section-25.1.html:30` Also "the stack from Section 16.1 transfer essentially unchanged" → check renumbering.
  - `section-25.2.html:30` Key insight: "the multimodal analog of transformers from Module 12" → old module-12 was Part 2 interpretability; modern HF transformers is referenced elsewhere. Also "Section 16.1" stale.
  - `section-25.4.html:30` Key insight: "the text model-zoo discussion in Module 12 and Section 8.1" → both stale.

---

## Part 6: Agentic AI

**Part-level findings.**
- Part index `part-6-agentic-ai/index.html` does have chapter cards (better than other parts). However:
  - Prose at line 40 says "Agent safety and security gets its own dedicated treatment in Chapter 38 within Part IX." — verify. In the restructure, agent safety is presumably in Part 10 or 11; "Chapter 38" is almost certainly stale (no Chapter 38 exists anymore).
  - The Chapter 30 card lists 8 sections (`30.1` through `30.8`) but only 5 section files exist on disk (30.1-30.5). Sections 30.6, 30.7, 30.8 are anchor links into `section-30.2.html`. Either remove them from the chapter card (they aren't real sections) or split them into their own files.
- Big-picture is real ("Building autonomous AI agents..." prose), no expansion needed.

### Chapter 26: AI Agent Foundations

- **Title**: KEEP.
- **Big-picture**: KEEP (real narrative).
- **Section descriptions**: ALL 6 are placeholders. Suggested:
  - 26.1: "Defining the agent loop (perceive-reason-act-observe), separating agents from chains and static workflows, and the four agentic design patterns."
  - 26.2: "Planning strategies for multi-step tasks: plan-and-execute, ReWOO, Tree of Thoughts, LATS tree search, and reflection loops."
  - 26.3: "Using reasoning models (o1/o3, Claude Extended Thinking, DeepSeek-R1) as agent backbones; thinking-budget tradeoffs."
  - 26.4: "SWE-bench, GAIA, WebArena, OSWorld and building custom evaluation harnesses for agent quality."
  - 26.5: "End-to-end production architecture: planner, tool router, memory, sandbox, evaluator, recovery, permissions, cost control."
  - 26.6: "A five-layer memory architecture for agents (working, episodic, semantic, procedural, transactional) with storage, retrieval, and forgetting policies."
- **Ordering**: PROPOSE moving 26.6 (Memory) up to 26.4 or 26.3. Memory is foundational to the planning and reasoning sections; the current order (planning → reasoning → eval → architecture → memory) puts the architecture/memory sections after eval, which is backwards. Better: 26.1 (definitions) → 26.2 (planning) → 26.3 (reasoning) → 26.4 (memory) → 26.5 (architecture) → 26.6 (eval). Or even: 26.1 → 26.4 (memory) → 26.2 (planning) → 26.3 (reasoning) → 26.5 (architecture) → 26.6 (eval).
- **Stale refs:**
  - `index.html:51` Chapter overview prose: "building on the vector database infrastructure from Chapter 22" → Chapter 22 is Vision-Language Models now; the embeddings/vector-DB content is in Chapter 31. Fix to "Chapter 31".
  - `index.html:59` Big-picture: "production agent deployment (Chapter 25)" → Chapter 25 is now Tools of the Trade: Multimodal Stack; production agent deployment is presumably elsewhere (probably the new Chapter 30 Tools chapter or in Part 10). The reference is stale.
  - `section-26.1.html:37` Big-picture: "The ReAct framework from Section 14.2 introduced..." → Section 14.2 is now Section 12.2 (prompt engineering) in Part 3 module-12. Verify.
  - `section-26.2.html:38` Big-picture: "The chain-of-thought from Chapter 08 provides the cognitive foundation that planning agents build upon." → Chapter 08 in the restructure is now Chapter 09 (Reasoning & Test-Time Compute) — verify; "chain of thought" coverage may have shifted.
  - `section-26.6.html:40` Prerequisites: "the MemGPT/Mem0 systems discussed in Section 26.6" — **circular self-reference**, should point to 26.1 or another section.
  - `section-26.6.html:40` "embeddings and vector databases from Chapter 22" → Chapter 31; "retrieval-augmented generation from Section 23.1" → Section 32.1; "conversation management from Chapter 22" → wrong chapter, conversation is Chapter 37.
- **Home fit / consolidation**: The agent-memory architectures here have strong overlap with the conversation-memory material in Chapter 37 (`module-37-conversational-ai/section-37.3.html` Memory and Context Management). Worth checking whether the two memory treatments fully complement each other or duplicate; if duplicate, decide which is canonical (likely 26.6 for the system-architecture treatment, 37.3 for the conversation-specific patterns).

### Chapter 27: Tool Use, Function Calling & Protocols

- **Title**: KEEP.
- **Big-picture**: KEEP (real narrative in index.html).
- **Section descriptions**: 5/6 placeholders. 27.6 (Efficient Multi-Tool Orchestration) is the only one with real text. Proposed replacements:
  - 27.1: "Function calling JSON schema, conversation flow, parallel calls, and the cross-provider portability problem."
  - 27.2: "Model Context Protocol (MCP) servers and clients: tools, resources, prompts, the 2024-25 standardization push."
  - 27.3: "Agent-to-Agent (A2A) protocol: Agent Cards, task lifecycle, the inter-agent communication standard."
  - 27.4: "Designing production-grade custom tools: parameter validation, error envelopes, rate limiting, security."
  - 27.5: "Agentic RAG: agents that decompose queries, retrieve iteratively, and synthesize from multiple sources."
- **Ordering**: KEEP. Provider function calling → MCP → A2A → custom tools → agentic RAG → orchestration economy is a clean foundation-to-application progression.
- **Stale refs:**
  - `index.html:58` Big-picture: "These capabilities are prerequisites for the specialized and multi-agent systems in Chapters 24 and 25." → wrong chapter numbers; should be Chapters 28 and 29.
  - `index.html:75` Prereq label "Chapter 23: Retrieval-Augmented Generation" → should be Chapter 32 (in the restructured numbering).
- **Home fit / consolidation**: Section 27.5 (Agentic RAG: Retrieval-Augmented Agents) is conceptually very close to Section 32.2 (Deep Research & Agentic RAG) in Part 7. **Worth deciding whether to keep both, merge them into one home, or differentiate them more sharply** (e.g., 27.5 = "agents as retrieval consumers, the tool-use pattern" and 32.2 = "iterative deep-research orchestration"). At present they overlap substantially.

### Chapter 28: Multi-Agent Systems

- **Title**: KEEP.
- **Big-picture**: KEEP.
- **Section descriptions**: ALL 4 are placeholders. Suggested:
  - 28.1: "Framework landscape: LangGraph, CrewAI, AutoGen, OpenAI Agents SDK, Google ADK — the 2026 production multi-agent stack."
  - 28.2: "Architecture patterns: supervisor, pipeline, mesh, swarm, hierarchical, debate, and when each topology fits."
  - 28.3: "Human-in-the-loop interaction points, graduated autonomy, trust calibration, and approval gates."
  - 28.4: "Testing multi-agent systems: scenario generation, deterministic replay, contract tests, and chaos injection."
- **Ordering**: KEEP.
- **Stale refs:**
  - `index.html:55` Chapter overview prose: "these patterns connect to the safety considerations in Chapter 25" → Chapter 25 is now Tools of the Trade: Multimodal Stack; safety is in Part 10/11. Fix.
  - `index.html:60` Big-picture: "connects to the safety considerations of Chapter 25" → same issue.
  - `section-28.1.html:38` Big-picture references "The agent foundations from Chapter 26 and the tool use protocols from Chapter 27 are prerequisites for all frameworks covered here." — that is correct; nice. Keep.

### Chapter 29: Specialized Agents

- **Title**: KEEP.
- **Big-picture**: KEEP. (`index.html` big-picture is real.)
- **Section descriptions**: ALL 4 are placeholders. Suggested:
  - 29.1: "Code generation agents: Claude Code, Cursor, Devin, GitHub Copilot Workspace, self-debugging loops, SWE-bench evaluation."
  - 29.2: "Browser and web agents: Playwright MCP, Stagehand, WebArena, computer-use agents with screenshot reasoning."
  - 29.3: "Research and data analysis agents: deep research, Open Deep Research, code-interpreter and data-analysis loops."
  - 29.4: "Production agentic coding systems: Claude Code, Cursor, Devin, Windsurf — terminal-first vs IDE vs autonomous."
- **Ordering and home fit**: PROPOSE merging 29.1 (Code Generation Agents) and 29.4 (Code/Work Workflows and Agentic Coding Systems) into one section. They cover overlapping ground (both mention Claude Code, Cursor, Devin). Either:
  - Combine into a single Section 29.1 "Code Generation Agents and Production Agentic Coding Systems" and move 29.2, 29.3 down (so the chapter becomes 3 sections total), OR
  - Differentiate 29.1 as "Code generation patterns and architectures" (SWE-bench, self-debugging) vs 29.4 as "The 2026 production landscape and emerging human-AI collaboration workflows" — but the current titles don't make this distinction clear.
- **Stale refs:**
  - `index.html:36` Looking Back: "Chapters 20-22 covered agents as a general pattern." → Chapters 20-22 are now Audio, Document, and VLM, not agents. Fix to "Chapters 26-28".
  - `index.html:57` Big-picture: "While Chapters 22 through 24 cover general agent principles..." → wrong chapter range; should be 26-28.
  - `index.html:104` What's-Next: "In the next chapter, Chapter 26: Agent Safety and Production..." — Chapter 26 is AI Agent Foundations (where this part started), not Agent Safety. Next chapter is Chapter 30 (Tools of the Trade: Agent Stack). Fix.
  - `index.html:109` Chapter-nav next says "Chapter 30 Tools of the Trade: Agent Stack" — correct destination, mismatch with the What's-Next prose.

### Chapter 30: Tools of the Trade: Agent Stack

- **Title**: KEEP.
- **Big-picture**: KEEP.
- **Section descriptions**: ALL 5 placeholders. Suggested:
  - 30.1: "Platforms: managed agent platforms (Anthropic Workbench, OpenAI Assistants, LangSmith) and self-hosted runtimes."
  - 30.2: "Libraries and frameworks: LangGraph, CrewAI, AutoGen, smolagents, PydanticAI — the orchestration shelf."
  - 30.3: "Datasets and benchmarks: SWE-bench, GAIA, WebArena, SWE-Lancer, AgentBench."
  - 30.4: "Models: which frontier and open models are agent-ready in 2026 (tool use quality, instruction following, cost)."
  - 30.5: "External reading and communities: agent-specific newsletters, repos, and conferences."
- **Ordering**: KEEP.
- **Stale refs:**
  - `index.html:73` What-Comes-Next: "Part VII turns to multimodal generation: image, video, audio, and music models." — but Part 7 is **Retrieval & Information Extraction**, not multimodal. Multimodal is Part 5 (which already preceded Part 6). The original intent was that the very next chapter is Chapter 31 (Embeddings in Part 7); say so.
  - `index.html:78` Chapter-nav next says "Chapter 31 Multimodal Generation" (links to part-5 module-20) — wrong destination and wrong description. Should be "Chapter 31 Embeddings, Vector Databases & Semantic Search" in part-7.
- **Section card 30.6 / 30.7 / 30.8 issue (in Part 6 index, not this chapter index):** Part-6 index lists 8 sections for module-30, but only 5 files exist; 30.6/30.7/30.8 are anchor links into `section-30.2.html`. Remove them from the part index or promote them into real sections.

---

## Part 7: Retrieval & Information Extraction with LLMs

**Part-level findings.**
- Part index `part-7-retrieval-information-extraction-with-llms/index.html` shows chapter cards for Chapters 34, 35, 36 but is **missing cards for Chapters 31, 32, 33** despite those chapters existing in subfolders. The rebuild-script placeholder comment on line 32 is still in place.
- Big-picture is duplicated with the Part overview ("Embeddings, structured information extraction & NER, RAG, knowledge graphs, cross-modal retrieval."); expand.

### Chapter 31: Embeddings, Vector Databases & Semantic Search

- **Title**: KEEP.
- **Big-picture**: KEEP (real narrative in index.html).
- **Section descriptions**: ALL 5 placeholders. Suggested:
  - 31.1: "Text embedding models from Word2Vec to E5-mistral: contrastive objectives, hard-negative mining, MTEB."
  - 31.2: "Vector index data structures: HNSW, IVF, Product Quantization, and the recall-vs-latency curve."
  - 31.3: "Vector database systems: Pinecone, Weaviate, Qdrant, Milvus, ChromaDB, pgvector — when each fits."
  - 31.4: "Document processing and chunking strategies (fixed, recursive, semantic, structure-aware) for retrieval quality."
  - 31.5: "Vision-based document retrieval: ColPali and the page-image-as-token paradigm."
- **Ordering**: KEEP.
- **Stale refs (systemic plus chapter-specific):**
  - `index.html:24, 27` Breadcrumb and pagefind-meta say "Part V: Retrieval and Conversation with LLMs and Agents" — outdated.
  - `index.html:34` Figure caption "Figure 22.0.1" → renumber 31.0.1.
  - `index.html:38` Looking Back: "Part IV adapted the model. Part V gives the model memory." → Part V is no longer the home; should say "Part 6 covered agents. Part 7 gives the model memory."
  - `index.html:38` "Everything in Chapter 23 (RAG) and Chapter 24 (Conversational AI)" → Chapter 32 and Chapter 37 respectively.
  - `index.html:71` Big-picture: "RAG systems in Chapter 23 and the conversational AI systems in Chapter 24" → Chapters 32 and 37.
  - `index.html:126` What's-Next: "Chapter 23: Retrieval-Augmented Generation" → Chapter 32.
  - `index.html:129-131` Chapter-nav prev "Chapter 21 Tools of the Trade: Training" and next "Chapter 23 RAG" — both stale chapter numbers (now 19 and 32 respectively).
  - `section-31.1.html:37` "embedding fine-tuning techniques from Section 18.5" → renumber; old Part 4 numbering preserved.
  - `section-31.1.html:40` "Section 1.3" and "Section 18.1" — many old-numbering links throughout.
  - `section-31.1.html:44` Figure caption "Figure 22.1.1" → renumber 31.1.1.

### Chapter 32: RAG Fundamentals

- **Title (h1)**: The `<h1>` in `index.html` says "RAG Fundamentals" but the document `<title>` and meta say "Retrieval-Augmented Generation (RAG)". After the RAG split (Ch 32 fundamentals + Ch 35 advanced), "RAG Fundamentals" is the better title. **PROPOSE** updating `<title>` and meta description to match the h1 — or, alternatively, propose "Retrieval-Augmented Generation: Fundamentals" everywhere.
- **Big-picture**: KEEP (real narrative).
- **Section descriptions**: ALL 4 placeholders ("RAG fundamentals."). Suggested:
  - 32.1: "The RAG retrieve-and-generate architecture, the storage spectrum (parametric / context / external), and the common failure modes."
  - 32.2: "Deep research and agentic RAG: query decomposition, iterative retrieval, and multi-source synthesis."
  - 32.3: "Structured data and Text-to-SQL: querying relational databases by natural language."
  - 32.4: "Source attribution and citation: designing RAG systems that show their work."
- **Section title mismatch (32.2):** The title is "Deep Research & Agentic RAG" but a `concept-link` from inside `section-32.2.html` (and from elsewhere) refers to "section 32.2 Advanced RAG Techniques" — "Advanced RAG Techniques" is actually now Section 35.1. The concept-link title is stale.
- **Ordering**: PROPOSE moving 32.2 (Deep Research & Agentic RAG) to last, after 32.4. The progression 32.1 (architecture) → 32.3 (text-to-SQL: another retrieval source) → 32.4 (citation: a property of every RAG system) → 32.2 (agentic: the most sophisticated pattern) is more pedagogically clean. Alternatively, move 32.2 to Chapter 35 (Advanced RAG) since "agentic RAG" is more "advanced RAG" than "fundamental RAG."
- **Home fit / consolidation**:
  - Section 32.2 (Deep Research & Agentic RAG) overlaps with Section 27.5 (Agentic RAG: Retrieval-Augmented Agents) in Part 6. Pick one canonical home.
  - Sections 32.1 (RAG fundamentals) and 35.1 (Advanced RAG Techniques) are split: fundamentals stayed in Chapter 32, advanced was promoted to Chapter 35. That's intentional and good.
- **Stale refs:**
  - `index.html:24, 27` Breadcrumb says "Part V: Retrieval and Conversation with LLMs and Agents".
  - `index.html:35` Figure caption "Figure 23.0.1" → 32.0.1.
  - `index.html:38` Looking Back: "You can find relevant chunks (Chapter 22)." → Chapter 31.
  - `index.html:47` Chapter overview: "Building on the embedding and vector database foundations from Chapter 22..." → Chapter 31.
  - `index.html:66` Big-picture: "This chapter is central to building the knowledge-intensive applications covered in Part VI and Part VIII." → check if Part VI/VIII still match (Part VI is Agentic, Part VIII is Conv AI — both consume RAG, so OK; but Part numbering should be consistent throughout).
  - `index.html:79` "Section 23.0.0 The Knowledge Storage Spectrum" inside section-32.1 — heading IDs say `32-1-0` but visible heading "23.1.0" — renumber.
  - `index.html:83` Prereq: "Chapter 22: Embeddings & Vector Databases" → Chapter 31.
  - `index.html:115` What's-Next: "Chapter 24: Conversational AI" → Chapter 37.
  - `index.html:118` Chapter-nav prev "Chapter 22 Embeddings" → 31.
  - `index.html:120` Chapter-nav next "Chapter 24 Building Conversational AI Systems" → 37.
  - `section-32.1.html:44` Heading text "23.1.0 The Knowledge Storage Spectrum" — old numbering visible.
  - `section-32.1.html:47` Reference: "Section 34.1: LLM Evaluation Fundamentals" — verify Chapter 34 in new layout; Chapter 34 is now Structured Information Extraction & NER, not LLM Evaluation Fundamentals. LLM Evaluation Fundamentals is Section 42.1 in Part 9.
  - `section-32.1.html:42` "see Appendix J (LangChain)" — verify Appendix J exists in current layout.
  - `section-32.2.html:38` Big-picture: "Building on the advanced retrieval techniques from Section 32.2..." — **self-reference; should be Section 35.1**.

### Chapter 33: Cross-Modal Reasoning and Multimodal RAG

- **Title**: KEEP.
- **Big-picture**: PROPOSE expand. "Joint embedding spaces, multimodal retrieval, when to retrieve vs reason, and production multimodal reasoning." is a tag list. Suggested: "Multimodal RAG extends text retrieval to images, audio, and video. This chapter covers joint embedding spaces (CLIP, ImageBind, SigLIP), retrieval-augmented generation across modalities, the decision rubric for retrieving vs reasoning directly, and production patterns."
- **Section descriptions**: All four are real and acceptable. No placeholders.
- **Ordering**: KEEP.
- **Stale refs:**
  - `index.html:20, 24` Breadcrumb says "Part VII: Multimodal Generation" — should be "Part VII: Retrieval & Information Extraction with LLMs" (or whatever the canonical Part 7 name is).
  - `index.html:53-56` Chapter-nav says prev "Chapter 41 Embodied AI" and next "Chapter 43 Tools of the Trade: Multimodal Stack" — both wrong: prev should be Chapter 32, next should be Chapter 34.
  - `section-33.1.html:35, 38` breadcrumb / pagefind-meta still say "Part VII: Multimodal Generation".
- **Home fit**: Multimodal RAG is a sensible chapter for the retrieval/IE part; cross-modal reasoning (especially 33.4 Multimodal Reasoning in Production) has plausible alternative homes in Part 5 (multimodal). But the retrieval framing is the right one — KEEP.

### Chapter 34: Structured Information Extraction & NER

- **Title**: KEEP.
- **Big-picture**: KEEP (real narrative).
- **Section descriptions**: ALL 5 placeholders ("Promoted from old section 15.5."). Suggested:
  - 34.1: "Information extraction landscape: NER, relation extraction, event extraction, and how each task maps to LLM + classical NLP hybrid pipelines."
  - 34.2: "Classical and Open IE: spaCy, CRF, Stanford OpenIE, OllIE — when the 30-year-old tool still wins."
  - 34.3: "Hybrid IE architectures: combining spaCy NER pre-processing with LLM extraction for accuracy and cost."
  - 34.4: "Production IE deployment patterns: schema versioning, schema migration, confidence calibration, and human-in-the-loop reviewers."
  - 34.5: "Coreference resolution and document-level pipelines: linking pronouns to entities, aggregating across paragraphs."
- **Ordering**: KEEP (landscape → classical → hybrid → production → coreference).
- **Stale refs (substantial — content was lifted from old Section 15.5):**
  - Internal section heading IDs say `34-1-1`, `34-2-2`, etc. but visible heading numbering still says "15.5.1.1", "Table 15.5.1", "Code Fragment 15.5.2", "Code Fragment 15.5.10". A bulk renumbering pass is needed.
  - `section-34.1.html:36` Comparison-table title "Table 15.5.1" → 34.1.1.
  - `section-34.2.html:32` "Code Fragment 15.5.10" → 34.2.X.
  - `section-34.2.html:33` "Code Fragment 15.5.2" → 34.2.X.
  - Similar issues throughout 34.3-34.5.
- **Home fit**: Chapter 34 sits in Part 7 (retrieval and IE) — that's correct. But coreference resolution and document pipelines could equally live in Part 1 (NLP foundations) or Part 5 (document understanding). Current home is defensible.

### Chapter 35: Advanced RAG: Knowledge Graphs, Ingestion & Frameworks

- **Title**: KEEP. (The chapter is the natural home for the "advanced" half of the RAG split.)
- **Big-picture**: KEEP.
- **Section descriptions**: ALL 5 placeholders ("Split from old Ch 32 RAG monster."). Suggested:
  - 35.1: "Advanced RAG techniques: query transformation (HyDE, multi-query), hybrid search, cross-encoder reranking, self-corrective RAG (CRAG, Self-RAG)."
  - 35.2: "Knowledge graphs as RAG: entity-relation stores, Cypher queries, KG-grounded retrieval."
  - 35.3: "GraphRAG: Microsoft's community-summarization approach to KG-augmented retrieval."
  - 35.4: "RAG ingestion pipelines and connectors: document loaders, parsers, schedulers, incremental indexing."
  - 35.5: "RAG frameworks and orchestration: LangChain, LlamaIndex, Haystack, DSPy."
- **Ordering**: KEEP. PROPOSE possibly moving 35.4 (ingestion) up: in a real-world build, ingestion comes before retrieval-time advanced techniques, so 35.4 → 35.1 → 35.2 → 35.3 → 35.5 might read more naturally. But the current order (advanced techniques → KG → graphRAG → ingestion → frameworks) treats it as "build out from the simplest cases", which is also defensible.
- **Home fit / consolidation**:
  - **Sections 35.2 (RAG with Knowledge Graphs) and 35.3 (GraphRAG) overlap.** 35.2's content note explicitly says "This topic is also discussed in Section 32.7: GraphRAG (full treatment)." Section 32.7 doesn't exist anymore (it's 35.3). Either merge 35.2 and 35.3 into a single section, or sharpen the distinction: 35.2 = "KGs as a separate retrieval substrate (build/query)" vs 35.3 = "GraphRAG's specific community-summarization technique." Current text reads like one section that got cut in half.
- **Stale refs:**
  - All section breadcrumbs say "Part V: Retrieval and Conversation".
  - `section-35.2.html:38` Note: "This topic is also discussed in Section 32.7: GraphRAG (full treatment)" → should be **Section 35.3**.

### Chapter 36: Retrieval Tools of the Trade

- **Title**: KEEP.
- **Big-picture**: KEEP. (Real content.)
- **Section descriptions**: All five have real (if generic) descriptions. They are acceptable but could be sharper. Suggested replacements:
  - 36.1: "Hosted (Pinecone, Weaviate Cloud, Qdrant Cloud, Turbopuffer) and self-hosted (Milvus, Chroma, pgvector) retrieval platforms."
  - 36.2: "Libraries: sentence-transformers, fastembed, infinity, FlagEmbedding (BGE), LangChain retrievers, LlamaIndex."
  - 36.3: "Datasets and benchmarks: MTEB, BEIR, MS MARCO, NQ-open, TriviaQA."
  - 36.4: "Models: OpenAI text-embedding-3, Cohere Embed v3, Voyage AI, BGE-M3, NV-Embed."
  - 36.5: "External reading and communities: ACL, EMNLP, the retrieval-focused subreddits and Discords."
- **Content density issue (36.1):** Section 36.1 ("Platforms") body is barely two paragraphs of stub content with three skeleton H2 headings ("Commercial Platforms", "Open-Source Platforms", "Selection Criteria") and one-line placeholder descriptions under each. Needs real content authored.
- **Ordering**: KEEP (standard Tools-of-the-Trade template).
- **Stale refs**: minimal so far, this chapter is newer and cleaner. Cross-check that all the embedded URLs still work (Turbopuffer, Chroma Cloud, etc.).

---

## Part 8: Conversational AI with LLMs

**Part-level findings.**
- Part index `part-8-conversational-ai-with-llms/index.html` is missing a chapter card for **Chapter 37 (Building Conversational AI Systems)**. Only Chapters 40 and 41 are listed. Chapter 37 exists on disk in `module-37-conversational-ai/`.
- Chapter numbering jumps from 37 to 40 in part-8 (no 38, no 39). After the wave-9 restructure that merged old 37.5 + old Chapter 39 into Chapter 40 (Voice & Realtime), and renumbered the Tools chapter to 41, this is intentional but visually surprising. **PROPOSE** renumbering to consecutive: Chapter 37 → 37, Chapter 40 → 38, Chapter 41 → 39 (the rest of the book may need to shift too, depending on book-wide numbering decisions). At minimum, the part-8 introduction should explain why the chapter numbers skip.
- Big-picture is duplicated with the Part overview; expand.

### Chapter 37: Building Conversational AI Systems

- **Title**: KEEP.
- **Big-picture**: KEEP.
- **Section descriptions**: ALL 4 placeholders ("Conversational AI."). Suggested:
  - 37.1: "Dialogue system architecture: task-oriented vs open-domain vs hybrid; selecting the right pattern."
  - 37.2: "Personas, companionship, and creative writing: system prompts, persona stability, the Replika-NEDA-ChatGPT case studies."
  - 37.3: "Memory and context management: sliding windows, summarization, vector-store memory, cross-session persistence."
  - 37.4: "Multi-turn dialogue and conversation flows: clarification, correction, topic switching, fallback strategies."
- **Ordering**: KEEP.
- **Home fit / consolidation**: 37.3 (Memory and Context Management) substantially overlaps with 26.6 (Memory Architecture for Agents). Decide on one canonical home for the "memory architecture" patterns.
- **Stale refs (heavy — this chapter has not been re-pointed):**
  - All section breadcrumbs say "Part V: Retrieval and Conversation with LLMs and Agents".
  - `index.html:34` Figure caption "Figure 24.0.1" → 37.0.1.
  - `index.html:48` Chapter overview: "The synthetic data techniques from Chapter 17 can help generate training examples..." → check current location of synthetic data chapter; old Chapter 17 was Part 4.
  - `index.html:89` Prereq: "Chapter 23: Retrieval-Augmented Generation" → Chapter 32.
  - `index.html:119` What's-Next: "Part VI: Agentic AI" — that is Part 6 in the book, which **comes before** Part 8 in the restructured spine. Either fix this to point forward (Part 9: Evaluation) or remove the "what's next" section.
  - `index.html:122` Chapter-nav prev "Chapter 23 RAG" → 32.
  - `index.html:124` Chapter-nav next "Chapter 25 Tools of the Trade: Retrieval & Conversation Stack" → the corresponding chapter is now Chapter 41 (Conversational AI Tools of the Trade) in part-8.

### Chapter 40: Voice and Realtime Multimodal Assistants

- **Title**: KEEP.
- **Big-picture**: KEEP (real narrative reflecting the wave-9 merge: "It merges material from the Conv AI Voice section and the Streaming/Realtime Multimodal chapter into one focused home.").
- **Section descriptions**: ALL 5 placeholders ("Voice and realtime multimodal AI."). Suggested:
  - 40.1: "Voice agents: production architectures, latency budgets, the speech-to-speech vs pipeline tradeoff, OpenAI Realtime / LiveKit / Pipecat."
  - 40.2: "Streaming audio architectures: VAD, codec choice, KV cache, interruption handling, TTFAT (time-to-first-audio-token)."
  - 40.3: "Gemini Live and GPT-4o Realtime APIs: protocols side-by-side, turn-detection semantics, function-calling shape."
  - 40.4: "Audio token budget and latency engineering: math behind cost, the 700ms wall, optimization patterns."
  - 40.5: "Open-source realtime stack: Moshi (Kyutai), Pipecat, LiveKit Agents — model layer, orchestration, transport."
- **Ordering**: KEEP. The progression voice agent overview → streaming architecture → frontier APIs → token budget → open-source stack is sensible.
- **Stale refs:**
  - `section-40.1.html:27, 31` breadcrumb says "Part V: Retrieval and Conversation".
  - `section-40.2.html:26, 29` breadcrumb says "Part VII: Multimodal Generation" — and pagefind-meta same.
  - `section-40.2.html:36` Big-picture references "GPT-4o Realtime (Section 39.2)" — old number. **Should be Section 40.3**.
  - `section-40.2.html:40` Prereq: "Section 37.1 (pipeline vs native)" → should be Section 22.6 (Pipeline vs Native Multimodal in Chapter 22).
  - `section-40.2.html:40` "Audio codec basics from Chapter 32" → should be Chapter 20.
  - `section-40.3.html:26, 29, 39` breadcrumb says "Part VII: Multimodal Generation"; figure caption "Figure 38.2.1" → 40.3.1.
  - `section-40.4.html:35, 38` breadcrumb says "Part VII: Multimodal Generation".
  - `section-40.5.html:26, 29, 39` breadcrumb says "Part VII: Multimodal Generation"; figure caption "Figure 38.4.1" → 40.5.1.
- **Home fit / consolidation**: Sections 40.3 (Gemini Live + GPT-4o Realtime) and 40.4 (Audio Token Budget) read smoothly together, and section 40.1 has substantial overlap with 40.2 (both are about pipeline architecture and latency). Worth a small consolidation pass.

### Chapter 41: Conversational AI Tools of the Trade

**MAJOR ISSUE — chapter contents are mostly the WRONG topic.** The chapter body in sections 41.1-41.4 is almost entirely about **retrieval / RAG tooling** (vector databases, embedding models, retrieval benchmarks). The chapter title says "Conversational AI Tools of the Trade" but the section bodies read as the old combined "Retrieval & Conversation Stack" chapter. After the wave-9 split (Part 7 got its own Chapter 36 Retrieval Tools, Part 8 retained Chapter 41 for Conv AI Tools), the Conv AI side was never rewritten, so the contents are misplaced.

Specifically:
- `section-41.1.html` (Platforms) opens with "The 'platforms' of Part V are the managed and self-hosted vector databases." and proceeds to discuss Pinecone, Weaviate, Qdrant, MongoDB Atlas Vector Search. **This is retrieval content** that belongs in Chapter 36. The Conv AI Tools chapter should cover platforms like **Botpress, Rasa, Dialogflow, Voiceflow, Microsoft Bot Framework, ChatGPT custom GPTs, Anthropic Projects, Character.AI**, etc.
- `section-41.2.html` (Libraries and Frameworks) discusses sentence-transformers, fastembed, BGE, OpenAI embeddings API. **Should cover** LangChain conversation memory, OpenAI Assistants API, Anthropic Conversations, Chainlit, Gradio, Streamlit for chat UIs, AG-UI protocol, voice frameworks.
- `section-41.3.html` (Datasets and Benchmarks) discusses MTEB, BEIR, retrieval benchmarks. **Should cover** PersonaChat, MultiWOZ, BlendedSkillTalk, SimpleDS, conversational benchmarks.
- `section-41.4.html` (Models) discusses embedding models and rerankers. **Should cover** chat-tuned models (GPT-4 turbo, Claude 3.5 Sonnet, Mistral, Llama-3 chat variants), realtime/voice-aware models (Sonic, GPT-4o-mini, Gemini Live), open dialogue models.

**Recommendation:** Either authoring a full rewrite of Sections 41.1-41.4 with conversation-stack-specific content (best), or accepting that Chapter 41 is duplicative of Chapter 36 and merging the two and removing Chapter 41 (cheaper).

Specific findings assuming a rewrite:

- **Title**: KEEP.
- **Big-picture**: KEEP (the chapter-index big-picture is correctly Conv AI-focused: "Botpress, Rasa, Dialogflow, LangChain conversation memory, OpenAI Assistants, Anthropic prompts, PersonaChat, MultiWOZ" — the prose is right, only the section bodies are wrong).
- **Section descriptions**: ALL 5 placeholders. Once content is rewritten, replace with conversation-stack-specific one-liners as listed above.
- **Stale refs:**
  - Every section breadcrumb says "Part V: Retrieval and Conversation".
  - `section-41.1.html:23, 27` "Part V: Retrieval and Conversation".
  - `section-41.1.html:28` Body text "The 'platforms' of Part V..." — **content reference to old part**.
  - `section-41.4.html:28` "Part V uses two model categories: embedding models..." — **content reference to old part / wrong topic**.
  - Anchor IDs use `25.1.1`, `25.2.1`, etc. (the old chapter-25 numbering) even though the file is now Chapter 41. Bulk-renumber.

---

## Cross-cutting consolidation candidates

Here are the most consequential cross-part consolidation moves the audit suggests:

1. **Agentic RAG: pick one canonical home.** Section 27.5 (Agentic RAG: Retrieval-Augmented Agents) in Part 6 vs Section 32.2 (Deep Research & Agentic RAG) in Part 7 cover very similar ground. Either merge into one section, or sharpen the differentiation.
2. **Memory architecture: pick one canonical home.** Section 26.6 (Memory Architecture for Agents) in Part 6 vs Section 37.3 (Memory and Context Management) in Part 8 overlap on layered-memory design and storage policies.
3. **Sim-to-real treatment: deduplicate.** Section 24.6 (VLA Limitations, includes sim-to-real paragraph) vs Section 24.13 (Sim-to-Real Gap, full section) in Chapter 24. Once the chapter is properly split into VLA-models + LLM-Robotics, this is fine; while merged, the 24.6 paragraph should be a pointer to 24.13.
4. **Knowledge graphs vs GraphRAG: pick a clear split.** Section 35.2 (RAG with Knowledge Graphs) and Section 35.3 (GraphRAG: Knowledge Graph-Augmented Retrieval) are awkwardly split right now; the prose in 35.2 even points to 35.3 as "full treatment". Merge or differentiate.
5. **Code-generation agents: pick a clear split.** Section 29.1 (Code Generation Agents) and Section 29.4 (Code/Work Workflows and Agentic Coding Systems) overlap substantially. Merge into one, or differentiate as architecture-focused vs landscape-focused.
6. **Chapter 41 vs Chapter 36 tools overlap.** As described above, Chapter 41's section bodies are duplicating retrieval content covered in Chapter 36. Rewrite or remove.

---

## Cross-cutting numbering and link issues

A non-exhaustive list of the bulk-renumbering work needed (these are the kinds of things a renumbering script should sweep up):

- All "Section 23.x" references in module-26-29, module-31-37 should become "Section 32.x" (RAG) or related new numbering.
- All "Chapter 22" references that mean "embeddings and vector DB" should become "Chapter 31".
- All "Chapter 24" / "Chapter 25" references that mean "Conversational AI" / "Tools of Retrieval+Conversation" should become "Chapter 37" / "Chapter 41".
- All "Section 14.x" references that mean prompt engineering should become "Section 12.x".
- All "Section 13.x" references for LLM APIs → "Section 11.x".
- All "Section 16.x" / "Section 18.x" old fine-tuning refs → re-point to current Part 4 numbering.
- All "Chapter 40 LLM-Powered Robotics" breadcrumbs in module-24 → "Chapter 24 Vision-Language-Action Models" (or whatever the merged chapter is named).
- All "Chapter 33 Video Generation" / "Chapter 37 Unified Multimodal and Omni Models" breadcrumbs in module-20 / module-22 → consolidated chapter names.
- All "Part V: Retrieval and Conversation with LLMs and Agents" and "Part VII: Multimodal Generation" breadcrumbs / pagefind-meta should be updated to current Part 5/6/7/8 names.
- All "Figure 22.X.Y", "Figure 23.0.1", "Figure 24.0.1", "Figure 32.X.Y", "Figure 33.X.Y", "Figure 34.X.Y", "Figure 37.X.Y", "Figure 38.X.Y" captions → renumber to current chapter.
- All `15.5.X.Y` heading numbers in Chapter 34 → renumber to `34.X.Y`.
- All "Code Fragment 15.5.X", "Code Fragment 32.5.1" captions → renumber to current chapter+section.
- The visible H2 headings throughout sections 22.7+, 24.10+, 32.1, 34.X, 41.1+ use old numbering (e.g., heading text shows "37.2.1" while the HTML id is `22-7-1`). The id and the visible text diverged; a renumbering pass should make them consistent.

---

## Summary statistics

- **Chapters audited:** 17 (5 in Part 5, 5 in Part 6, 6 in Part 7, 3 in Part 8).
- **Chapters with placeholder section descriptions:** 12 of 17 (Modules 25, 26, 27, 28, 29, 30, 31, 32, 34, 35, 37, 40, 41).
- **Chapters where the index is missing section cards that exist on disk:** 3 (Module 20 missing 20.6-20.10; Module 22 missing 22.6-22.9; Module 24 missing 24.7-24.13).
- **Chapters that are effectively two chapters glued together:** 3 (Chapter 20 audio+video; Chapter 22 VLM+omni; Chapter 24 VLA+robotics).
- **Chapters whose content does not match their title:** 1 (Chapter 41 — retrieval content under Conv AI Tools title).
- **Chapters with major stale breadcrumb / chapter-nav references:** ~all.
- **Chapters with no placeholder descriptions and substantially clean content:** Chapter 21 (Document Understanding), Chapter 23 (3D Generation), Chapter 33 (Cross-Modal RAG), Chapter 36 (Retrieval Tools, but content stubby).
