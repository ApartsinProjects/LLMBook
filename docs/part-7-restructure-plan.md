# Part 7 Restructure Plan — Multimodal Generation Split into Focused Topic Chapters

**Author**: Architecture planning pass, 2026-05-16
**Status**: DESIGN (no files moved yet)
**Scope**: Part VII (Chapters 31, 32, 33). Goal: split overpacked Chapters 31 and 32 into focused single-topic chapters.

---

## Section A — Current State Map

### Chapter 31 — Multimodal Generation (4 sections, ~28,000 words)

| Sec | Title | Words | Topic family | Proposed destination |
|-----|-------|------:|--------------|----------------------|
| 31.1 | Image Generation & Vision-Language Models | 8,096 | Diffusion, ControlNet, ViT/CLIP, VLMs | Split: Image Gen (new Ch 31) + VLMs (new Ch 35) |
| 31.2 | Audio, Music & Video Generation | 7,289 | TTS, real-time audio, MusicGen, video DiT, Sora/Veo | Split: Audio (Ch 32) + Video (Ch 33) + 3D-stub (Ch 36) |
| 31.3 | Document Understanding & OCR | 5,626 | TrOCR, LayoutLMv3, doc AI, VLM-based doc parsing | Ch 34 Document AI |
| 31.4 | Unified Multimodal Models & Omni-Architectures | 6,976 | Pipeline vs native, GPT-4o, Gemini, omni training | Split: Omni (Ch 37) + Streaming (Ch 38) |

### Chapter 32 — Embodied AI, World Models & Multimodal Reasoning (8 sections, ~17,000 words)

| Sec | Title | Words | Destination |
|-----|-------|------:|--------------|
| 32.1 | Embodied Multimodal Agents & VLA Models | 2,112 | Ch 39 VLA & Embodied AI |
| 32.2 | LLM-Powered Robotics | 2,196 | Ch 40 |
| 32.3 | 3D Gaussian Splatting & Neural Scene Representation | 2,093 | Ch 36 |
| 32.4 | World Models | 2,141 | Ch 41 |
| 32.5 | 3D Asset Generation | 2,223 | Ch 36 (merge with 32.3) |
| 32.6 | Multimodal Editing & Inpainting | 2,515 | Split: Ch 31/32/33/36 |
| 32.7 | Multimodal Reasoning & Cross-Modal Retrieval | 1,857 | Split: Ch 35 + Ch 42 |
| 32.8 | Robotics, Embodied AI & Scientific Discovery | 1,762 | Migrate to Part XI |

### Chapter 33 — Tools of the Trade (5 sections)

Restructure: split entries by topic into per-chapter "Tools" callouts; keep consolidated reference chapter for stack overview.

---

## Section B — Proposed New Part 7 Structure

**Title**: Part VII — Multimodal Generation (unchanged)
**Target chapter count**: 13 substantive + 1 Tools = 14 chapters (Ch 31–44 new numbering).

| New Ch | Title | Focus |
|--------|-------|-------|
| 31 | Image Generation | Diffusion, flow matching, SD/FLUX/Imagen, ControlNet, LoRA |
| 32 | Audio & Music Generation | TTS (VITS, Bark, F5), MusicGen, Suno/Udio, voice cloning |
| 33 | Video Generation | Video DiTs, Sora, Veo, Runway, Kling, AnimateDiff |
| 34 | Document Understanding & OCR | TrOCR, LayoutLMv3, Donut, VLM-based extraction |
| 35 | Vision-Language Models | ViT, CLIP, SigLIP, BLIP-3, LLaVA, GPT-4V |
| 36 | 3D Generation & Neural Scenes | 3DGS, NeRF, Stable Zero123, Trellis, 4D splats |
| 37 | Unified Multimodal & Omni Models | Native multimodal, GPT-4o, Gemini, Chameleon |
| 38 | Streaming & Real-Time Multimodal | Gemini Live, GPT-4o Realtime, Moshi |
| 39 | Vision-Language-Action Models | RT-2, OpenVLA, pi-0, action tokenization |
| 40 | LLM-Powered Robotics | SayCan, Code-as-Policies, VoxPoser |
| 41 | World Models & Simulation | Genie 3, V-JEPA 2, GAIA-2, DreamGen |
| 42 | Cross-Modal Reasoning & Multimodal RAG | Joint embeddings, multimodal RAG, retrieve-vs-reason |
| 43 | Tools of the Trade: Multimodal Stack | Platforms, libraries, datasets, reference |

Rationale: each major topic in 2026 multimodal has its own model lineage, eval suite, library stack, and production gotchas. Wide split lets each go deep.

### Alternative A — Conservative 9-chapter split

Merge: Ch 32+33 (Audio+Video) → one chapter; Ch 37+38 (Unified+Streaming) → one; Ch 39+40 (VLA+Robotics) → one; Ch 41+42 (World+Cross-Modal) → one. Delta becomes +6 instead of +10.

---

## Section C — Per-Chapter Section Breakdown

### Chapter 31 — Image Generation (6 sections, ~9,500 words)

1. **31.1** Diffusion Models for Image Generation *(from 31.1.1 forward/reverse + latent diffusion)*
2. **31.2** Flow Matching & Rectified Flows *(from 31.1.1, expand with SD3/FLUX)*
3. **31.3** DALL-E, Midjourney, Stable Diffusion, FLUX, Imagen 4 *(from 31.1.1 + expansion)*
4. **31.4** ControlNet, IP-Adapter, LoRA for Images *(from 31.1.2 + NEW)*
5. **31.5** Image Editing & Instruction-Following *(from 32.6.1)*
6. **31.6** Production Image Pipelines & Cost *(NEW)*

### Chapter 32 — Audio & Music Generation (5 sections, ~7,500 words)

1. **32.1** TTS: VITS, Bark, F5-TTS *(from 31.2.1 minus real-time)*
2. **32.2** Voice Cloning, Zero-Shot TTS, Voice Conversion
3. **32.3** Music Generation: MusicLM, MusicGen, Suno, Udio *(from 31.2.2)*
4. **32.4** Audio Editing: Stems, Style Transfer, Remixing *(from 32.6.3)*
5. **32.5** Speech Recognition for the Multimodal Stack *(NEW — Whisper, faster-whisper, AssemblyAI)*

### Chapter 33 — Video Generation (5 sections, ~7,000 words)

1. **33.1** Video Diffusion Transformers (DiTs)
2. **33.2** Leading Video Models: Sora, Veo, Runway, Kling, Pika
3. **33.3** Camera Control, Motion Control & ControlNet for Video *(NEW)*
4. **33.4** Video Editing & Remixing
5. **33.5** Long-Form & Cinematic Video Generation *(NEW)*

### Chapter 34 — Document Understanding & OCR (4 sections)

1. **34.1** Modern OCR: TrOCR & End-to-End
2. **34.2** Layout-Aware Models: LayoutLM Family
3. **34.3** VLM-Based Document Understanding
4. **34.4** Building Document AI Pipelines

### Chapter 35 — Vision-Language Models (5 sections, ~8,000 words)

1. **35.1** ViT & Visual Tokenization
2. **35.2** Contrastive Vision-Language: CLIP & SigLIP
3. **35.3** Generative VLMs: LLaVA, BLIP-3, Qwen-VL
4. **35.4** Frontier VLMs: GPT-4V, Gemini, Claude Vision
5. **35.5** Evaluating Multimodal Reasoning: MMMU & Saturation *(cross-link to Part VIII Ch 36)*

### Chapter 36 — 3D Generation & Neural Scenes (6 sections, ~8,000 words)

1. **36.1** 3D Gaussian Splatting Fundamentals
2. **36.2** 4D & Dynamic Splats
3. **36.3** Image-to-3D: Stable Zero123 & Multi-View Diffusion
4. **36.4** Direct 3D Diffusion: Trellis & Structured Latents
5. **36.5** Scene Relighting & 3D Editing in 2D
6. **36.6** Format Question: Meshes, Splats, NeRFs, Latents

### Chapter 37 — Unified Multimodal & Omni Models (5 sections)

1. **37.1** Pipeline vs Native Multimodal
2. **37.2** Early Fusion vs Late Fusion
3. **37.3** Any-to-Any Generation
4. **37.4** Training Unified Multimodal Models
5. **37.5** Frontier: GPT-4o, Gemini 2.5, Llama-4-Omni, Chameleon, Janus

### Chapter 38 — Streaming & Real-Time Multimodal (4 sections, ~6,000 words)

1. **38.1** Streaming Audio Architectures *(from 31.2.1 real-time)*
2. **38.2** Gemini Live & GPT-4o Realtime API *(NEW)*
3. **38.3** Audio Token Budget & Latency Engineering
4. **38.4** Open-Source Realtime: Moshi, Pipecat, LiveKit Agents *(NEW)*

### Chapter 39 — Vision-Language-Action Models (6 sections)

1. **39.1** VLA Architecture in One Equation
2. **39.2** OpenVLA-7B Reference Implementation
3. **39.3** Physical Intelligence pi-0 / pi-0.5
4. **39.4** RT-2-X & the Data-Scaling Story
5. **39.5** Comparing VLA Models
6. **39.6** VLA Limitations

### Chapter 40 — LLM-Powered Robotics (7 sections)

1. **40.1** SayCan: Grounding LLM Plans
2. **40.2** Code-as-Policies
3. **40.3** VoxPoser: Language as Spatial Cost Field
4. **40.4** Multi-Robot Dispatch via Shared LLM
5. **40.5** ROS 2 Integration
6. **40.6** Comparing the Planners
7. **40.7** Sim-to-Real Gap

### Chapter 41 — World Models & Simulation (6 sections)

1. **41.1** The Next-Frame as Next-Token Analogy
2. **41.2** Genie 3: Interactive Worlds from a Prompt
3. **41.3** V-JEPA 2: Representation Prediction
4. **41.4** GAIA-2: Domain-Specific World Models
5. **41.5** Synthetic Data for Robots: DreamGen
6. **41.6** World-Model Rollouts as Visual Chain-of-Thought

### Chapter 42 — Cross-Modal Reasoning & Multimodal RAG (4 sections, ~5,000 words)

1. **42.1** Joint Embedding Spaces for Multimodal Retrieval *(from 32.7.1)*
2. **42.2** Multimodal RAG *(NEW — image/audio/video RAG)*
3. **42.3** When to Retrieve, When to Reason *(from 32.7.4)*
4. **42.4** Multimodal Reasoning in Production *(NEW — cost/latency matrix)*

### Chapter 43 — Tools of the Trade: Multimodal Stack (5 sections)

Re-uses old 33.1–33.5 with entries re-tagged to the new chapter they reference.

---

## Section D — Content Extraction Map

(Per Section C — see plan source for full mapping table. Key splits:)

- 31.1.1 splits 4 ways (Diffusion + Latent + Flow Matching + Models)
- 31.1.3 splits 2 ways (ViT → Ch 35.1; CLIP → Ch 35.2)
- 31.1.4 splits 2 ways
- 31.2.1 splits 4 ways (TTS → Ch 32.1; Real-time → Ch 38.1; Token Budget → Ch 38.3; Whisper → Ch 32.5)
- 31.2.3 splits 2 ways (DiT arch → Ch 33.1; Models → Ch 33.2)
- 32.6 splits 4 ways (Image edit → Ch 31.5; Video remix → Ch 33.4; Audio edit → Ch 32.4; Relighting → Ch 36.5)
- 32.7.1 splits 2 ways (Encoder lineage → Ch 35.2; Retrieval framing → Ch 42.1)

Total new authoring requirement: ~25,000–35,000 words (P1+P2 in Section F).

---

## Section E — Cascade Renumbering

Part VII grows from 3 to 13–14 chapters: **+10 (or +6 under Alternative A)**.

Downstream parts shift:
- Part VIII (Eval): 34–36 → 44–46
- Part IX (Safety): 37–39 → 47–49
- Part X (Idea-to-Product): 40–50 → 50–60
- Part XI (Applications): 51–58 → 61–68
- Part XII (Frontiers): 59 → 69

Cross-link footprint: ~400–600 link sites across the book.

---

## Section F — Content Gaps Requiring NEW Authoring

### P1 — Required (~12,000 words)

| Section | Estimated words |
|---------|----------------:|
| 31.6 Production Image Pipelines & Cost | 1,500 |
| 32.5 Speech Recognition for the Multimodal Stack | 1,500 |
| 33.3 Camera Control, Motion Control, AnimateDiff | 1,800 |
| 33.5 Long-Form & Cinematic Video Generation | 1,800 |
| 38.2 Gemini Live & GPT-4o Realtime API | 1,800 |
| 38.4 Open-Source Realtime: Moshi, Pipecat, LiveKit | 1,500 |
| 42.2 Multimodal RAG | 2,200 |
| 42.4 Multimodal Reasoning in Production | 1,800 |

### P2 — Strongly desirable

- 31.2 Flow Matching & Rectified Flows (expand from ~30 lines)
- 32.2 Voice Cloning (currently scattered)
- 35.5 Multimodal Reasoning Evaluation (expand)
- 39.* VLA expansions (each ~250 → ~500-700 words)
- 40.* Robotics expansions (same)
- 41.6 Visual Chain-of-Thought (expand from callout to section)
- 36.6 Format Question (practitioner decision tree)

---

## Section G — Risks & Overlap

1. **Overlap with Part VI (Agents)**: Robotics is agents. Mitigation: opening callout "Robotics is agents, period" with cross-links to Ch 26/27.
2. **Overlap with Part VIII (Eval)**: Multimodal eval. Mitigation: Ch 35.5 gives capability landscape; Part VIII Ch 36 gives methodology.
3. **Overlap with Part II (Foundations)**: "Every modality becomes tokens" thesis. Mitigation: maintain unifying callouts; don't re-derive loss in each chapter.
4. **Tools fragmentation**: Splitting Ch 33 across 13 chapters loses "one place" property. Mitigation: keep Ch 43 as consolidated reference + per-chapter Tools callouts.
5. **Scientific Discovery migration (old 32.8)**: Not multimodal generation — migrate to Part XI Applications.
6. **13 chapters in one Part is unusual**: Consider Alternative A (9 chapters) if too many.
7. **32.x stub legacy**: Sections 32.1–32.4 are now ~2,100 words each but still thin for standalone chapters; need 2x expansion.

---

## Section H — Migration Script Outline

Same 10-phase template as `scripts/restructure_part8/`. Create `scripts/restructure_part7/`:

```
scripts/restructure_part7/
├── 00_validate_preconditions.py
├── 10_build_migration_map.py
├── 20_move_and_rename_dirs.py (mkdir new chapters, prepare 32.x → 39/40/41 promotions)
├── 30_split_sections.py (heaviest phase — 7 sections need splitting)
├── 40_rewrite_section_anchors.py
├── 50_rewrite_cross_links.py (book-wide for the +10 cascade)
├── 60_create_new_chapter_skeletons.py (12 new chapters)
├── 70_regenerate_yaml_and_toc.py (cascade Parts 8/9/10/11/12)
├── 80_generate_redirect_map.py
├── 85_image_assets.py (12 new chapter-opener.png via gemini-imagegen)
└── 90_verify_outcome.py
```

Estimated runtime: 60-90 seconds. Manual content phase after: author 8 P1 + 7 P2 sections.

**Coordination**: Run AFTER Part 9 restructure (Part 9 plan in docs/part-9-restructure-plan.md). Sequential migrations avoid directory collisions.

---

## Critical Files

- `book_structure.yaml`
- `part-7-multimodal-generation/index.html`
- `part-7-multimodal-generation/module-31-multimodal/index.html`
- `part-7-multimodal-generation/module-32-embodied-world-models/index.html`
- `toc.html`
