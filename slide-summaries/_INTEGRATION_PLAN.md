# Slide → Book Integration Plan

**Scope:** integrate content from 163 slide-deck summaries (`slide-summaries/<folder>/*.md`) into the LLMBook (`part-*/module-*` + `appendices/`). LLM-first, audio/speech second, multimodal third. Exclude course-admin and pure-vision material. Do NOT duplicate; deepen where the book is shallower.

**Status:** PLAN ONLY — no book edits yet. This document is the input to a follow-up edit pass that will spawn one subagent per chapter where edits are needed.

---

## 1. Executive summary

The book is genuinely deep. After cross-referencing every in-scope slide deck against the 15-Part / 79-module on-disk structure, the actual integration footprint is much smaller than the raw slide count suggests:

| Action | Decks |
|---|---|
| **SKIP entirely** (course admin / pure vision / pure RL theory / stable-diffusion / already covered at equal-or-greater depth) | 101 |
| **Deepen existing section** (book has the topic; slide adds a useful angle, citation, code sample, or pedagogy) | 34 |
| **New sub-section inside existing chapter** (book chapter exists but the specific topic is missing) | 19 |
| **New chapter or appendix** (no current home) | 4 |
| Reference-only (mine for callouts / examples but no structural change) | 5 |
| **TOTAL in-scope** | **62 decks** → ~57 concrete edits |

**Major new content that the book lacks today (high priority):**
1. **Signal-processing primer for audio** (DFT, Z-transform, sampling) → new Appendix A section, or new sub-section in Ch 20.
2. **Audio data, vector quantization, codec models** (SoundStream, EnCodec, RVQ) → new sub-sections in Ch 20.
3. **Self-supervised audio encoders** (wav2vec 2.0, HuBERT, WavLM) → new sub-section in Ch 20.
4. **PyTorch advanced topics** (the 96-slide PyTorch tutorial covers many things; promote into a new Appendix E "PyTorch Reference" + add `torch.compile`, mixed precision, hooks, profiler depth).
5. **LangGraph as a first-class section** in Ch 30 (currently only LangChain is named).
6. **LLM-as-Recommender-System** new sub-section in Ch 14 (industry applications).
7. **BERTopic** as a topic-modeling sub-section in Ch 31 (Section 31.7 mentions "Topic Modeling" but BERTopic is the modern default).

**Major deepening opportunities (the book has the topic; slides add depth):**
1. **MoE architectures** (slide 1308) — Section 3.8 mentions MoE; deepen with routing math, expert balancing, GShard/Switch/Mixtral lineage.
2. **Multilingual encoders** (slide 1311) — Section 7.4 mentions; deepen with mBERT/XLM-R/mT5 internals and tokenization tradeoffs.
3. **Attention mathematics** (slide 1301) — Ch 2 covers; cross-check slide's worked numerical example and add if missing.
4. **Long-context adaptation** (slide 1325) — Section 16.7 covers; add RoPE scaling, YaRN, NTK, position-interpolation as a unified section.
5. **Sentence embeddings** (slide 1304) — Section 16.5 + Ch 31; cross-check SBERT/contrastive depth.

**Asset creation needs (during edit phase):**
- **Diagrams (Mermaid):** ~12 (MoE router, MCP architecture, agentic-RAG loop, audio codec pipeline, wav2vec contrastive task, RoPE position rotation, LoRA delta math, etc.)
- **Illustrations (Gemini):** ~6 (whimsical metaphors: "tokens as Lego bricks", "MoE as a panel of experts", "an audio codec as a translator", "RAG citation trail", etc.)
- **Code callouts:** ~25 (one per new sub-section that introduces an API; HF Transformers + datasets + accelerate)
- **Standard callout boxes:** primarily **Practical Example**, **Key Takeaway**, **Note**, and **Big Picture** for new material; **Warning** for footguns (e.g., RVQ codebook collapse, MoE expert imbalance).

**Web research needs (during edit phase):**
- Currency check: MCP spec (2025–2026 versions), MoE state of the art (Mixtral, DeepSeek-V3, Qwen-MoE), audio codecs (Mimi from Moshi, OpenAI's spec), LangGraph latest API, BERTopic 0.16+, Whisper v3 / Distil-Whisper / WhisperX.
- Cross-validation: numerical claims from slides (parameter counts, FLOPs comparisons, benchmark numbers) before quoting them in the book.
- Citation gathering: ensure each new sub-section has 2–4 primary references (arXiv / official docs / canonical blog post).

---

## 2. Scope filter (what is and isn't being integrated)

### Explicitly EXCLUDED (per user instruction)
- **Course administration:** `1011`, `1022`, `1023`, `1024`, `1025`, `2011`, `2041`, `1041`, `1042` (8 decks).
- **Pure classical computer vision:** all of `Part 4 (Vision)` slide-summaries — 42 decks (3xxx / 4xxx that are not multimodal-adjacent).
- **Pure RL theory not connecting to RLHF:** `40093_DeepReinforce_DQN`, `45002_MARL_RL`, `45003_MARL_Games` (3 decks).
- **Vision-only generative apps:** `1623_ZeroShort_ClipSeg`, `1624_SegmentAnything`, `2222_VisionTaskModels`, `2225_VisionGeneration`, `2333_EncoderDecoder_DETR`, `2334_GenerativeImage_ImageGPT`, `2441-2448` (most Stable Diffusion apps), `2501-2507` (GAN history) (~22 decks).
- **Stable/Latent Diffusion entirely (user decision):** `2421_StableDiffusion_Model`, `2422_StableDiffusion_Guidance`, `2423_StableDiffusion_LongPrompts`, `2424_StableDiffusion_SDXL_SDXLTurbo`, `2447_StableDiffusion_ControlNet`, `2461-2465` (SD fine-tuning incl. LoRA, Textual Inversion, DreamBooth, IP-Adapter) — 9 decks. The book is not pivoting to image-generation depth; these are referenced only where they originally connected to a non-diffusion topic (e.g., LoRA in Section 17.1 stays text-only).
- **Classical pre-LLM ML topics already handled at sufficient depth in Ch 0 + Appendix A:** `0005_HiddenMarkovModels`, `0007_ExpectationMaximization`, `0011_MLConcepts`, `0014_Generalization`, `0015_DLConcepts` (5 decks).

### IN scope (62 decks)
- **Background relevant to LLMs:** `0004_InformationTheory`, `0006_GibbsSampling`, `0008_JointGuassian`, `0013_Optimization`, `0016_PyTorchTutorial`, `0017_GenerativeModels`, `0002_DFT`, `0003_LaplaceAndZTransform` (8 decks — last 2 for audio appendix only).
- **NLP / LLM core:** `1012`, `1121-1123`, `1141-1143`, `1201-1205`, `1301-1311`, `1321-1327`, `1401-1404`, `1411`, `1416` (35 decks).
- **Agents:** `1421-1428` (8 decks).
- **Multimodal / VLM (excluding stable diffusion):** `1621`, `1622`, `2221`, `2223`, `2224`, `2331`, `2332` (7 decks, light touch).
- **Audio (primary):** `5011-5041` (9 decks).
- **RL foundations for RLHF:** `40001`, `40002`, `40004`, `40005`, `45001_MARL_Introduction` (5 decks, modest deepening).

---

## 3. Cross-reference map (slide deck → target chapter/section)

The table below is the **master integration map**. `[SKIP]` = no action; `[D]` = deepen existing section; `[NS]` = add new sub-section; `[NC]` = add new chapter or appendix.

### Foundations slides → Part 1 + Appendix A

| Slide deck | Target location | Action | Notes |
|---|---|---|---|
| 0002_DFT | new Appendix Sec G.1 (Signal Processing for Audio) OR Ch 20 prelude | [NS] | Only useful for audio chapter context; create a small primer appendix. |
| 0003_LaplaceAndZTransform | new Appendix Sec G.2 | [NS] | Same as above; pair with G.1. |
| 0004_InformationTheory | Appendix A.4 + A.6 | [D] | Slides have 42 slides; book has 4200 words. Add: cross-entropy as LM training loss derivation worked through, KL on logits (used in distillation/DPO), mutual information for embedding evaluation. |
| 0006_GibbsSampling | Ch 4.4 (Diffusion Language Models) + Ch 26.3 footnote | [D] | Ch 4.4 already covers diffusion LMs. Add Gibbs as the historical precursor for discrete diffusion in an aside-callout. |
| 0008_JointGuassian | Appendix A.2 (Probability) | [D] | Add joint Gaussian conditioning identity; useful for VAE/diffusion latent math. |
| 0013_Optimization | Ch 0.2 + Appendix A.3 (Calculus) | [D] | Likely already covered; spot-check for momentum, Adam variants (AdamW depth), warmup/cosine schedules used by LLMs. |
| 0016_PyTorchTutorial | Sections 0.3 + 0.4 + **new Appendix E (PyTorch Reference)** — full mini-book per user decision | [NC] | 96 slides far exceed sections 0.3/0.4 (~6000 + 4000 words). Build Appendix E as a complete standalone mini-book (~25 pages, narrative style) that reteaches PyTorch end-to-end using the slide deck as the backbone. Suggested sections: E.1 Tensors (creation, dtypes, devices, reshaping, broadcasting); E.2 Autograd internals (computational graph, gradient accumulation, detach, no_grad, hooks); E.3 nn.Module patterns (parameters, buffers, state_dict, freezing); E.4 Data pipeline (Dataset, IterableDataset, DataLoader, collate_fn, samplers); E.5 Training loop deep dive (loss scaling, gradient clipping, scheduler, checkpointing); E.6 Mixed precision (AMP, bfloat16, fp16 vs bf16 tradeoffs); E.7 Distributed training (DataParallel deprecated, DistributedDataParallel, FSDP1 vs FSDP2, accelerate launcher); E.8 Performance (`torch.compile`, profiler, memory snapshot, common bottlenecks); E.9 Debugging recipes (NaN hunt, OOM diagnosis, shape mismatches, common autograd errors); E.10 Saving, loading, and deployment (state_dict vs full save, ONNX export, TorchScript, mobile). Reader should leave Appendix E able to write production PyTorch without external help. |
| 0017_GenerativeModels | Ch 22 intro + Ch 26 intro | [D] | A short "tour of the generative-model landscape" callout works at the top of both chapters. |

### Part 1 modules — language foundations

| Slide deck | Target location | Action | Notes |
|---|---|---|---|
| 1012_TypicalLanguageTasks | Section 1.1 (Intro to NLP & the LLM Revolution) | [D] | Add a compact "task taxonomy" table (19 classical NLP tasks → LLM equivalents) as a callout box. Source the comparison from the slide. |
| 1121_TextTokenization | Sections 1.5–1.8 (already covers BPE, WordPiece, multilingual) | [SKIP] | Confirmed equal-or-greater depth. |
| 1122_TermTopicVectors | Section 1.2 (Classical Representations) | [D] | Verify the section covers TF-IDF, LSA/LSI. If not present, add a tight sub-section "Term-document matrices, TF-IDF, and LSA" before word embeddings. |
| 1123_WordEmbeddings | Section 1.3 | [SKIP] | Section already covers Word2Vec, GloVe, FastText at depth (8700 words). |
| 1201_LLMForLangRepresentation | Section 16.5 (Representation Fine-Tuning) + Ch 31 | [D] | Slide focuses on BERT-style representation use cases. Verify Section 31.2 has the encoder vs decoder embedding contrast; add a callout matrix if not. |
| 1202_LLMForLangGeneration | Section 4.x (decoding) + Ch 7 intro | [SKIP] | Generation tasks taxonomy is implicit in the book. No new content. |
| 1203_TextDecodingStrategies | Sections 4.1–4.3 | [SKIP] | Already covers greedy, beam, top-k, top-p, temperature, repetition penalty. |

### Ch 2 (Sequence Models & Attention)

| Slide deck | Target location | Action | Notes |
|---|---|---|---|
| 1301_Attention | Sections 2.2–2.4 | [D] (verify) | Likely covered. Spot-check that the **worked numerical attention example** from the slides is present; if not, add as a Practical Example callout in 2.3. |

### Ch 3 (Transformer Architecture)

| Slide deck | Target location | Action | Notes |
|---|---|---|---|
| 1302_Transformer | Sections 3.1–3.4 | [D] (verify) | Cross-check that Pre-Norm vs Post-Norm is discussed, GeLU vs ReLU, relative vs absolute positional embeddings. |
| 1303_TransformerPretraining | Section 6.2 (Pretraining Objectives) | [SKIP] | Section 6.2 covers MLM/NSP/CLM in depth. |
| 1307_TransformerSeq2Seq | Section 3.1 / 3.5 (Transformer Anatomy & Variants) | [D] | Add a single sub-section "Encoder-decoder transformers and cross-attention" if missing. T5, BART motivation. |
| 1308_TransfomerMixtureOfExperts | Section 3.8 (Beyond Attention — SSMs, MoE, Modern Variants) | [D] **(priority)** | Section 3.8 mentions MoE; the slide deck has substantial routing math. Expand to a full MoE sub-section: gating function, top-k routing, load balancing loss, expert parallelism, GShard → Switch → Mixtral → DeepSeek-V3 lineage. Add a Mermaid router diagram. |
| 1310_LLM_ExplainingTransformer | Section 10.4 (Explaining Transformers) | [SKIP] | Already covered. |
| 1311_LLM_MultilinguialEncoder | **Section 7.4 (single deep section)** + back-pointer from Section 1.8 — per user decision | [D] | Single deep section in 7.4 covering: mBERT → XLM → XLM-R → mT5 → NLLB-200 → Aya 23 lineage with architectures and training-corpora composition; the curse of multilinguality (adding languages can hurt existing ones once vocabulary budget runs out); shared subword vocab tradeoffs; tokenization fertility (avg tokens-per-word: English ~1.3 vs Burmese 5+) and the resulting per-token cost asymmetry; tokenizer choices (BPE-vs-Unigram, especially for non-Latin scripts); language adapters as a mitigation. Section 1.8 (multilingual tokenization) gets a one-paragraph back-pointer at the end: "Tokenization is one of three load-bearing decisions in multilingual model design. The other two — shared encoder weights and pretraining-corpus composition — are covered in Section 7.4." |

### Ch 4–5 (Decoding, Generation, Tools)

| Slide deck | Target location | Action | Notes |
|---|---|---|---|
| 1141_FM_Intro | Section 7.1 / 6.1 (Foundation Model overview) | [SKIP] | Already covered. |
| 1142_HuggingFace_intro | Section 5.2 (Library Catalog) + Section 19.2 (Tools) | [SKIP] | Both already have HF coverage. |
| 1143_HF_accelerate | Sections 19.8 + 19.14 (Distributed Training Deep Dive) | [SKIP/verify] | Already covers Accelerate. Spot-check that `accelerate config`, `notebook_launcher`, and `FSDP via Accelerate` are present. |

### Ch 6 (Pretraining & Scaling)

| Slide deck | Target location | Action | Notes |
|---|---|---|---|
| 1303_TransformerPretraining | Section 6.2 | [SKIP] | Already deep. |
| (1141 again) | Section 6.1 | [SKIP] | Already deep. |

### Ch 7 (Modern LLM Landscape)

| Slide deck | Target location | Action | Notes |
|---|---|---|---|
| 1311_LLM_MultilinguialEncoder | Section 7.4 | [D] | See above. |

### Ch 16 (Fine-Tuning Fundamentals)

| Slide deck | Target location | Action | Notes |
|---|---|---|---|
| 1205_LLMFineTuningIntro | Section 16.1, 16.3 | [SKIP] | Covered. |
| 1304_SentenceEmbedding | Section 16.5 + 31.2 | [D] | Confirm SBERT, MTEB benchmark, contrastive losses (multiple-negatives, triplet, InfoNCE) are present. Add a small comparison table if missing. |
| 1305_InstructionFollowing | Section 16.3 + 18.x | [SKIP] | SFT covers instruction-following. |
| 1323_RepresentationFineTuning | Section 16.5 | [SKIP] | Already covered. |
| 1324_ClassificationFineTuning | Section 16.6 | [SKIP] | Already covered. |
| 1325_AdaptingForLongText | Section 16.7 | [D] | Section 16.7 covers; verify RoPE scaling, YaRN, NTK-aware interpolation, position interpolation (Su et al.), LongLoRA, and the "needle-in-haystack" eval are all there. If patchy, add a Long-Context Techniques cheat-sheet callout. |

### Ch 17 (PEFT, Distillation, Merging)

| Slide deck | Target location | Action | Notes |
|---|---|---|---|
| 1321_PEFT | Sections 17.1, 17.2 | [SKIP] | Already covers LoRA, QLoRA, adapters. |
| 1322_PromptTuning | Section 17.4 | [SKIP] | Soft prompts already covered. |
| 1326_LLMDistilation | Sections 17.5, 17.6 | [SKIP] | Already covered. |
| 1327_LLMMerge | Section 17.7 | [SKIP] | Already covered. |

### Ch 18 (Alignment: RLHF / DPO)

| Slide deck | Target location | Action | Notes |
|---|---|---|---|
| 1306_FinetuningHumanFeedback | Sections 18.1–18.2 | [SKIP] | RLHF + PPO covered deeply. |
| 40001_DeepReinforce_Intro | Section 0.5 (RL Foundations) | [SKIP] | Section 0.5 (8400 words) covers RL framework already. |
| 40002_DeepReinforce_MDP | Section 0.5.1–0.5.3 | [SKIP] | Same. |
| 40004_DeepReinforce_PolicyGradient | Section 0.5.4 | [SKIP] | Already there. |
| 40005_DeepReinforce_ActorCritic | Section 0.5.4 + 18.1 | [D] | Slight deepening: add a one-paragraph "Actor-Critic in the RLHF context: the critic is the value head sharing the policy backbone." in Section 18.1. |

### Ch 20 (Audio, Music, Video Generation) — PRIMARY AUDIO HOME

| Slide deck | Target location | Action | Notes |
|---|---|---|---|
| 5011_Audio_TypicalTasks | Section 20 intro / new Section 20.0 | [D] | A landscape callout / table at top of Ch 20 listing audio task families (classification, ASR, TTS, music gen, source sep, codec). |
| 5012_Audio_Data | **new Section 20.0.1: Audio Data & Representations** | [NS] | Waveforms, sample rates, mel-spectrograms, MFCC, framing, windowing. References to new Appendix G (signal processing). |
| 5013_Audio_VectorQuant | **new Section 20.0.2: Audio Codec Models & Vector Quantization** | [NS] | RVQ, SoundStream, EnCodec, DAC (Descript Audio Codec), Mimi (from Moshi). This is the bridge between raw audio and LLM token streams. |
| 5014_AudioSpeechTransformers | **new Section 20.0.3: Audio & Speech Transformer Architectures** | [NS] | AST, Audio Spectrogram Transformer, Whisper architecture, Conformer, attention adaptations for long audio. |
| 5015_PretrainedAudioModels | Section 20.5 + Section 25.4 (Models catalog) | [D] | Cross-check Whisper, Whisper v3, Distil-Whisper, WhisperX, Canary, SeamlessM4T. |
| 5021_Audio_Encoders | **new Section 20.0.4: Self-Supervised Audio Encoders** | [NS] | wav2vec 2.0, HuBERT, WavLM, BEATs. Contrastive + masked-prediction objectives. Pair with a Mermaid diagram of the wav2vec 2.0 contrastive task. |
| 5021_MultimodalAudio (5025) | Section 33.2 (Multimodal RAG, audio) + Ch 26/22 intro | [D] | Audio-text contrastive (CLAP, AudioCLIP), audio embedding stores. Add a sub-section "Audio-Text Joint Embedding Spaces" in Section 33.1 if missing. |
| 5031_Audio_Classification | new Section 20.x.5 or in Ch 14 (industry: ESC-50, AudioSet) | [NS] | Smaller. Add as a sub-section of Ch 20 with a HF pipeline code callout. |
| 5041_Audio_Speech2Text | Section 20.5 | [SKIP/verify] | Likely covered. Check that Whisper code example and streaming Whisper are present. |

### Ch 22 (Vision-Language Models)

| Slide deck | Target location | Action | Notes |
|---|---|---|---|
| 1621_MultimodalRepresentationClip | Section 22.2 (CLIP / SigLIP) | [SKIP] | Already deep. |
| 1622_Multimodal_Generation_BLIP | Section 22.3 (LLaVA, BLIP-3, Qwen-VL) | [SKIP] | Already covered. |
| 2221_VisionModelsIntro | Section 22.1 / Ch 22 intro | [SKIP] | Already covered. |
| 2223_VisionRepresentationModels | Section 22.1 (ViT) | [D] | Add explicit DINO / DINOv2 mention if missing (self-supervised vision encoder used as backbone in many VLMs). |
| 2224_VisionMultimodall | Section 22.6–22.9 | [SKIP] | Already covers pipeline vs native multimodal, fusion, any-to-any. |
| 2331_ViT_Intro | Section 22.1 | [SKIP] | Covered. |
| 2332_VIT_DeIT_DINO_SWIN | Section 22.1 | [D] | Add a one-paragraph each on DeiT (data-efficient ViT) and Swin (hierarchical windows). DINO already noted above. |
| 2421–2424, 2447, 2461–2465 (Stable Diffusion family) | — | [SKIP] | **All Stable/Latent Diffusion content is out of scope per user instruction.** Book does not pivot to image-generation depth. |

### Ch 26–29 (Agents)

| Slide deck | Target location | Action | Notes |
|---|---|---|---|
| 1421_Tools_FunctionCalls | Section 27.1 | [SKIP] | Covered. |
| 1422_Tools_MCP | Section 27.2 | [D] | Section already deep; verify currency (MCP spec 2025-06-18+ revisions, Anthropic, OpenAI, and Google adoption). |
| 1423_Memory_Intro | Section 26.6 + Sections 37.3–37.5 | [SKIP] | Memory covered in 26.6 (agents) and 37.x (conversation). |
| 1424_LangGraph_Intro | **new Section 30.2.x: LangGraph** | [NS] | Section 30.2 covers LangChain Legacy + Framework Deep Dive; LangGraph specifically (stateful graph orchestration) deserves its own sub-section with a worked agent-graph example. |
| 1425_Memory_MemGPT | Section 26.6 + 37.5 | [SKIP] | Letta/MemGPT covered. |
| 1426_Agents_Flows | Section 26.5 / 28.2 | [SKIP] | Architectural patterns covered. |
| 1427_Agents_AgenticRAG | Section 32.3 (Deep Research & Agentic RAG) | [SKIP] | Covered. |
| 1428_Agents_Planning | Section 26.2 (Planning & Agentic Reasoning) | [SKIP] | Covered. |
| 45001_MARL_Introduction | Section 28.1–28.2 footnote | [D] | One-paragraph callout: "Cooperative vs competitive multi-agent settings; MARL inspirations for LLM debate, swarm, and negotiation patterns." |

### Ch 31 (Embeddings & Vector Search)

| Slide deck | Target location | Action | Notes |
|---|---|---|---|
| 1304_SentenceEmbedding | Section 31.2 | [D] | See Ch 16 entry. |
| 1411_BERTTopics | **new Section 31.7.x: BERTopic** | [NS] | Section 31.7 mentions topic modeling generically. Add a dedicated BERTopic sub-section: pipeline (embed → UMAP → HDBSCAN → c-TF-IDF), use cases, comparison to LDA. |

### Ch 32, 35 (RAG)

| Slide deck | Target location | Action | Notes |
|---|---|---|---|
| 1401_VectorStores | Section 31.5 | [SKIP] | Covered. |
| 1402_RAG_Intro | Section 32.1 | [SKIP] | Covered. |
| 1403_RAG_Evaluations | Section 32.2 + 35.x (RAG eval frameworks: RAGAS, ARES) | [D] | Add explicit RAGAS / ARES / TruLens names if missing. |
| 1404_AdvancedRAG | Sections 35.1–35.7 | [SKIP] | Already deep. |

### Part 8 (Conversational AI) — NEW chapter for RecSys (per user decision)

| Slide deck | Target location | Action | Notes |
|---|---|---|---|
| 1416_LLMForRecSys | **NEW Chapter 38 (Part 8): LLM-Powered Recommender Systems** | [NC] | Goes between Ch 37 (Conversational AI Systems) and Ch 40 (Voice/Realtime). Fits Part 8 well because modern conversational AI surfaces are inseparable from personalization. Suggested sections: 38.1 The Recsys Landscape (cold-start, sparsity, novelty); 38.2 LLMs for Query & Intent Understanding; 38.3 LLMs for Item-Side Enrichment (synthetic descriptions, multi-modal embeddings); 38.4 Conversational Recsys (turn-taking, preference elicitation, justification); 38.5 Generative Recsys (TIGER, LLaRA, P5, semantic IDs); 38.6 Eval + production patterns (recall@k vs LLM-judged diversity, A/B vs offline). Cross-references: Ch 31 (embeddings), Ch 32/35 (retrieval), Ch 37 (conv-AI memory). |

### Multimodal & Audio chapter index references

| Slide deck | Target location | Action | Notes |
|---|---|---|---|
| 1309_MusicTransformer | Section 20.3 (Music Generation) | [D] | Verify Music Transformer (Huang et al.), MusicLM/MusicGen are present. Likely yes; verify lineage paragraph. |

---

## 4. Part-by-part edit roadmap

The follow-up edit pass will spawn one subagent per chapter that has edits. Each subagent receives: the relevant slide-summary `.md` files, the existing chapter HTML sections, the integration plan rows above, and the book style guide.

### Part 1: LLM Building Blocks
- **Ch 0 (ML & PyTorch Foundations):** Deepen Sections 0.2 (optimization) and 0.3/0.4 (PyTorch). Coordinate with new Appendix E.
- **Ch 1 (NLP Foundations):** Add Section 1.1 task-taxonomy callout (slide 1012). Verify Section 1.2 covers TF-IDF/LSA (slide 1122).
- **Ch 2 (Attention):** Verify worked numerical example (slide 1301).
- **Ch 3 (Transformer):** Add encoder-decoder sub-section if missing (slide 1307). **MAJOR DEEPENING** of Section 3.8 with MoE math + diagram (slide 1308).
- **Ch 4 (Decoding):** Slide 0006_GibbsSampling adds historical-precursor aside in Section 4.4.
- **Ch 5 (Tools):** No edits.

### Part 2: Understanding LLMs
- **Ch 6 (Pretraining):** No major edits.
- **Ch 7 (Modern LLM Landscape):** Major deepening of Section 7.4 (multilingual) with mBERT/XLM-R/mT5/NLLB-200, curse of multilinguality (slide 1311).
- **Ch 8 (Reasoning):** No edits.
- **Ch 9 (Inference):** No edits.
- **Ch 10 (Interpretability):** No edits (slide 1310 already covered).

### Part 3: Working with LLMs
- **Ch 11, 12, 13, 14 (tools):** No edits.

### Part 4: Training & Adaptation
- **Ch 15 (Synthetic Data):** No edits.
- **Ch 16 (Fine-Tuning Fundamentals):** Deepening of 16.5 (sentence embeddings — slide 1304) and 16.7 (long context — slide 1325).
- **Ch 17 (PEFT, Distillation, Merging):** No edits (diffusion personalization dropped per user instruction).
- **Ch 18 (Alignment):** Minor: one-paragraph actor-critic context in 18.1 (slide 40005).
- **Ch 19 (Tools):** No edits.

### Part 5: Multimodal LLMs
- **Ch 20 (Audio):** **Major expansion** at top of chapter — new Sections 20.0.1 (Audio Data), 20.0.2 (Codec & VQ), 20.0.3 (Audio Transformers), 20.0.4 (Self-Supervised Audio Encoders). New Section 20.x.5 for audio classification with HF pipeline. Use slides 5012, 5013, 5014, 5015, 5021, 5031.
- **Ch 21 (Document Understanding):** No edits.
- **Ch 22 (VLM):** Minor deepening only — add DeiT / Swin / DINO mentions in Section 22.1. No Stable-Diffusion content per user instruction.
- **Ch 23 (3D), Ch 24 (VLA):** No edits.
- **Ch 25 (Tools):** Update model catalog (Section 25.4) with audio codecs + Whisper variants.

### Part 6: Agentic AI
- **Ch 26 (Agent Foundations):** No edits.
- **Ch 27 (Tools & Protocols):** Currency check for MCP section (slide 1422).
- **Ch 28 (Multi-Agent):** MARL one-paragraph callout (slide 45001).
- **Ch 29 (Specialized Agents):** No edits unless LLM-RecSys lands here (open question).
- **Ch 30 (Tools of Trade):** **Add Section 30.2.x: LangGraph** (slide 1424). 1-2 page worked example.

### Part 7: Retrieval & Info Extraction
- **Ch 31:** Add Section 31.7.x: BERTopic (slide 1411). Small.
- **Ch 32:** Minor: name-check RAGAS/ARES/TruLens for slide 1403.
- **Ch 33, 34, 35, 36:** No structural edits. Add "Audio-Text Joint Embeddings" sub-section in 33.1 (slide 5021_MultimodalAudio).

### Part 8: Conversational AI
- **Ch 37 (Conversational AI Systems):** No edits.
- **NEW Ch 38: LLM-Powered Recommender Systems** — full new chapter per user decision. Slide source: 1416. ~6 sections (see §3 for the section breakdown). Will need its own bibliography and at least one diagram (the LLM-Recsys patterns Mermaid).
- **Ch 40 (Voice & Realtime):** No edits.
- **Ch 41 (Conv AI Tools):** Add LangChain/LlamaIndex recsys integrations and named open-source projects (e.g., LangFair, RecBole-LLM) to the catalog if relevant.

### Part 9: Evaluation
- No edits.

### Part 10–13: Security / Ethics / Scale / LLMOps
- No edits.

### Part 14: Applications Across Industries
- No edits. (Recsys moved to Part 8 per user decision.)

### Part 15: Research Frontiers
- No edits.

### Appendices
- **Appendix A (Math):** Deepen A.2 (joint Gaussian, slide 0008), A.3 (optimization for LLMs, slide 0013), A.4/A.6 (information theory, slide 0004).
- **New Appendix E: PyTorch Reference** (96-slide PyTorch tutorial 0016). Reference-style, not narrative.
- **New Appendix G: Signal Processing for Audio** (slides 0002 DFT, 0003 Laplace/Z) — small, ~2 pages, cross-referenced from Ch 20.

---

## 5. Asset creation plan

### Diagrams (Mermaid, render via `scripts/mermaid/generate_mermaid_diagrams.py`)
| # | Diagram | Target location | Source slide |
|---|---|---|---|
| 1 | MoE router top-k gating + expert balancing | Section 3.8 | 1308 |
| 2 | Encoder-decoder transformer cross-attention flow | Section 3.1 or 3.5 | 1307 |
| 3 | RoPE position rotation in 2D | Section 16.7 | 1325 |
| 4 | Audio codec pipeline (encoder → RVQ → decoder) | Section 20.0.2 | 5013 |
| 5 | wav2vec 2.0 contrastive task (mask → context → quantized targets) | Section 20.0.4 | 5021 |
| 6 | Whisper architecture (mel → encoder → decoder) | Section 20.0.3 | 5014 |
| 7 | BERTopic pipeline (embed → UMAP → HDBSCAN → c-TF-IDF) | Section 31.7.x | 1411 |
| 8 | LangGraph stateful agent graph (nodes, edges, state) | Section 30.2.x | 1424 |
| 9 | LLM-RecSys patterns (query-side / item-side / generative) | TBD | 1416 |
| 10 | Multilingual encoder tokenization tradeoffs (English vs low-resource fertility) | Section 7.4 | 1311 |

### Illustrations (Gemini, via `agents/book-skills/scripts/generate_icons_gemini.py`)
| # | Concept | Style |
|---|---|---|
| 1 | "MoE as a panel of expert advisors" | Whimsical cartoon, 4-5 experts at a table with a router |
| 2 | "Audio codec as a translator" | Codec robot turning waveform into discrete tokens |
| 3 | "Tokens as Lego bricks" (revival for multilingual fertility discussion) | Lego-style |
| 4 | "wav2vec student listening to the masked teacher" | Self-supervised audio |
| 5 | "BERTopic as a librarian clustering books" | Library scene |
| 6 | "LangGraph as a board-game director" | Graph nodes as game squares |

### Code callouts
~25 small Python callouts. Highest priority:
1. `transformers` snippet for Whisper inference (Section 20.5).
2. `audiocraft` / `encodec` snippet for codec encode-decode (Section 20.0.2).
3. `transformers` snippet for wav2vec 2.0 feature extraction (Section 20.0.4).
4. `bertopic` snippet for topic discovery (Section 31.7.x).
5. `langgraph` state-graph definition (Section 30.2.x).
6. `transformers` MoE inference snippet using Mixtral (Section 3.8).
7. `mergekit` snippet for model merging (only if Section 17.7 doesn't have one).
8. PyTorch `torch.compile`, AMP, profiler snippets (new Appendix E).

### Standard callouts
- **Practical Example:** for every new technique that ships with a code snippet.
- **Key Takeaway:** at end of each new sub-section.
- **Note / Warning:** for footguns (e.g., MoE expert imbalance during training; RVQ codebook collapse; CFG scale tradeoffs; long-context "lost in middle"; multilingual token-fertility cost).
- **Big Picture:** at the head of each Ch 20 new sub-section to orient readers.

---

## 6. Web research tasks (to run during editing, not now)

Before writing each new sub-section, the editing subagent must run targeted web research for currency and citations. Concrete queries:

| Topic | Queries (run via WebSearch) | What to capture |
|---|---|---|
| MoE state of the art | "Mixtral 8x22B", "DeepSeek-V3 MoE", "Qwen2-MoE", "Switch Transformer latest" | Latest models + load-balancing approaches + parameter counts |
| Audio codecs | "EnCodec 2025", "Mimi codec Moshi", "Descript Audio Codec", "Stable Audio Open" | Sample rates, RVQ ranks, bitrates |
| Audio SSL | "WavLM 2026", "BEATs audio", "Dasheng audio encoder" | Pretrain corpus size, downstream benchmarks |
| RoPE scaling | "YaRN long context 2025", "NTK-by-parts", "LongRoPE" | Math + empirical needle-in-haystack numbers |
| LangGraph | "LangGraph 0.2", "LangGraph supervisor pattern", "LangGraph studio" | Current API surface |
| BERTopic | "BERTopic 0.16", "BERTopic vs LDA recent", "supervised BERTopic" | API + comparison data |
| LLM-RecSys | "TIGER recsys", "LLaRA recsys", "P5 recsys", "generative recsys 2026" | Methods overview + benchmarks |
| Multilingual | "NLLB-200 update", "Aya 23", "Marian translator current" | Language coverage |
| MCP currency | "MCP specification 2026", "MCP Streamable HTTP", "Anthropic MCP SDK current" | Latest spec rev + transport changes |
| Whisper variants | "Whisper v4", "Distil-Whisper 2026", "WhisperX latest", "Canary NeMo" | Latency / WER tradeoffs |
| ~~Diffusion personalization~~ | (DROPPED — Stable/Latent Diffusion out of scope.) | — |
| ~~ControlNet~~ | (DROPPED — Stable/Latent Diffusion out of scope.) | — |

---

## 7. Style & consistency requirements (carried into edit phase)

Each editing subagent MUST follow:
- **Book tone:** technical, practitioner-oriented, occasionally witty (per BOOK_CONFIG epigraph examples). No marketing fluff.
- **No em dashes (—) or double-dashes (--)** anywhere in generated prose. Use commas, semicolons, parens, or sentence breaks. (Project rule from `CLAUDE.md`.)
- **Vocabulary:** "book / part / chapter / section / reader". Never "course / module / lecture / student" in prose. (Module is fine as a directory name; not as reader-facing text.)
- **Cross-references:** every new section must add forward + backward `<a href>` links into the existing chapter navigation, and update the parent module `index.html` table of contents. Use the `book-13-cross-reference` agent style.
- **Code blocks:** captions BELOW (per `agents/book-skills/agents/40-code-caption-agent.md`).
- **Figures:** captioned in surrounding prose (per project rules). Every figure / code block / callout referenced.
- **Citations:** each new sub-section gets 2–4 bibliography entries appended to the chapter bibliography via `book-35-bibliography` agent style.

---

## 8. Execution plan (when edits are approved)

Total estimated edit footprint: ~25 chapters touched, ~63 concrete edits.

Recommended pipeline (mirrors the Part 1–6 slide-summary autonomous pattern that already worked):

1. **Phase 0 (now):** Review this document with the user. Approve / adjust scope. Decide LLM-RecSys home (Ch 29 vs Part 14 vs standalone).
2. **Phase 1: Appendix E (PyTorch Reference)** — single dedicated subagent. Highest-leverage new artifact. Source: slide `0016`.
3. **Phase 2: Appendix G (Signal Processing for Audio)** — single subagent. Source: slides `0002`, `0003`. Pair with Phase 1.
4. **Phase 3: Audio chapter expansion** — one subagent for Ch 20 with all audio slides as input.
5. **Phase 4: Deepenings inside existing chapters** — one subagent per chapter family, dispatched in parallel:
   - Family A: Part 1 (Ch 1, 2, 3, 4) — slides 1012, 1122, 1301, 1307, 1308.
   - Family B: Part 2 (Ch 7) — slide 1311.
   - Family C: Part 4 (Chs 16, 17, 18) — slides 1304, 1325, 2463, 2464, 40005.
   - Family D: Part 5 (Ch 22) — slides 2223, 2332 only (DeiT / Swin / DINO mentions). All Stable-Diffusion slides dropped.
   - Family E: Part 6 (Chs 27, 28, 30) — slides 1422, 45001, 1424.
   - Family F: Part 7 (Chs 31, 32, 33) — slides 1411, 1403, 5025_MultimodalAudio.
6. **Phase 5: LLM-RecSys (slide 1416)** — needs scope decision first.
7. **Phase 6: Asset generation** — Mermaid + Gemini illustrations after prose lands.
8. **Phase 7: Cross-reference + bibliography sweep** — run `book-13-cross-reference` and `book-35-bibliography` agents over the touched chapters.
9. **Phase 8: Controller QA** — run `book-37-controller` to verify no broken links, all figures referenced, all code captioned.
10. **Phase 9: Audit gate** — `python -m agents.book-skills.scripts.audit.run --priority P0+P1+P2 --root .` per project memory.
11. **Phase 10: Commit on `slide-integration` branch** — one commit per phase for reviewable diff.

---

## 9. Decisions resolved + open questions

**Resolved:**
1. ✅ **LLM-RecSys home:** new **Chapter 38 in Part 8** (Conversational AI), sitting between Ch 37 (Conv-AI Systems) and Ch 40 (Voice/Realtime).
2. ✅ **Audio signal processing:** standalone **Appendix G** (~2 pages, DFT + Z-transform + sampling primer).
3. ✅ **Stable / Latent Diffusion:** out of scope. All SD slides dropped.
4. ✅ **Multilingual coverage:** **split** across Section 1.8 (tokenization angle) and Section 7.4 (model lineage), with back-pointers.

**Resolved:**
5. ✅ **PyTorch Appendix E:** **full mini-book** (~25 pages, narrative style). Reteaches PyTorch end-to-end using the 96-slide tutorial as the backbone, plus topics Ch 0 omits (distributed/FSDP, AMP, hooks, profiler, `torch.compile`, advanced DataLoader patterns, debugging recipes). Standalone resource a reader can use without needing Ch 0.

**All open questions resolved. Plan is ready to execute.**

---

## 10. Source files inventory (for the editing phase)

All slide summaries live under `slide-summaries/<folder>/<deck_stem>.md`. The 71 in-scope `.md` files are listed in §3 above by chapter target. The full extracted-content cache (struct.json + slide PNGs + embedded images) lives under `slide-summaries/_downloads/` and is gitignored; an editing subagent can re-read any slide PNG via the path `slide-summaries/_downloads/<folder>/<deck_stem>/slides/slide_NNN.png` if it needs to visually confirm a diagram, code screenshot, or formula image.

---

## 11. Gap-audit results (deep verification of slide → book coverage)

The original §3 plan was built from slide titles + my domain knowledge. To verify it, **8 parallel gap-auditor subagents** each read their full slide .md files + matching book section HTMLs end-to-end and produced a structured present/partial/missing report. Total: **405 items inventoried from slides, evaluated against the book**.

### Headline numbers

| Family | Chapters audited | Items | Present | Partial | Missing |
|---|---|---|---|---|---|
| A | Part 1 (Ch 1, 2, 3, 4) | 56 | 22 | 15 | 19 |
| B | Part 2 (Ch 6, 7, 10) | 38 | 11 | 11 | 16 |
| C | Part 4 (Ch 16, 17, 18) + Section 0.5 (RL) | 82 | 32 | 19 | 31 |
| D | Part 5 VLM (Ch 22) | 27 | 12 | 10 | 5 |
| E | Part 5 Audio (Ch 20) | 73 | 4 | 16 | **53** |
| F | Part 6 Agents (Ch 26-30) | 33 | 7 | 13 | 13 |
| G | Part 7 Retrieval (Ch 31-35) | 56 | 31 | 8 | 17 |
| H | Appendix A + Ch 0 + Section 1.1 | 40 | 22 | 9 | 9 |
| **TOTAL** | | **405** | **141 (35%)** | **101 (25%)** | **163 (40%)** |

**~264 items need work** (partial + missing). The original plan dramatically understated the scope; the actual content debt is much larger.

### Highest-priority new content (must-add)

Each family produced a top-5 (top-10 for Audio). The cross-family priority order:

1. **(E)** Ch 20 audio expansion: 4 new sections (20.0.1 Audio Data, 20.0.2 Codec+VQ, 20.0.3 Audio/Speech Transformers, 20.0.4 Self-Supervised Audio Encoders) + Section 20.x.5 Audio Classification. Absorbs ~50 missing items. **This is the single largest expansion in the book.**
2. **(F)** New Section 30.2.5: LangGraph end-to-end tutorial (state+reducer, chain graph, tools_condition router, ReAct agent, checkpoints+threads, streaming, HITL interrupt, Studio).
3. **(C)** Section 0.5 RL: insert Actor-Critic + advantage baseline + Markov property + MAB/contextual-bandit progression. Without this, the PPO four-model setup in 18.1.3 has no pedagogical bridge.
4. **(A)** Section 3.8 MoE expansion: full router math, top-k gating, load-balancing auxiliary loss, parameter-arithmetic worked example (dense 2M → 16 experts of 130K).
5. **(C)** Section 16.5 sentence-embedding recipes: SBERT (named), bootstrapping with silver datasets, SDAE, SimCSE, MTEB benchmark.
6. **(A)** Section 1.2 topic-models bridge: BoW → topic vectors → LSA via truncated SVD → LDiA as Bayesian mixture (deck 1122).
7. **(A)** Section 1.4 BERT pretraining walkthrough: MLM + NSP + [CLS] sentence-embedding + RoBERTa variant.
8. **(B)** Section 7.4 multilingual: full XLM (3 losses: MLM + CLM + TLM), curse of multilinguality, Noam learning-rate schedule.
9. **(C)** Section 16.6 NER + SetFit sub-sections.
10. **(C)** Section 16.7 long-document **classification** strategy catalog (7 strategies: truncate / sliding window / hierarchical / Longformer/BigBird / summarize-first / zero-shot generative / retrieval-augmented).
11. **(G)** New Section 31.7.x BERTopic full coverage including UMAP, HDBSCAN, c-TF-IDF, KeyBERTInspired / MMR / LLM representation models, visualizations.
12. **(G)** Section 33.1 audio-text joint embeddings: CLAP architecture + symmetric InfoNCE + chunk-and-fuse + T5 keyword augmentation + zero-shot pipeline code; also AudioCLIP.
13. **(D)** Section 22.1 add Swin Transformer (W-MSA/SW-MSA, hierarchical patch merging), DeiT distillation token, VisualBERT R-CNN lineage, original DINO multi-crop strategy, four-bucket pretrained-vision taxonomy table.
14. **(F)** Section 27.2 MCP: add the fourth primitive (Sampling) and the controller-taxonomy table; refresh transport to Streamable HTTP.
15. **(F)** Section 27.1 Toolformer + ToolkenGPT body coverage (currently bibliography-only).
16. **(F)** Section 26.2 ReWoo (single-pass plan with $E1/$E2 variables) + Baby-AGI historical anchor + RefleXion worked example (Responder+Revisor + structured JSON + tool-augmented citations).
17. **(G)** Section 32.2 RAPTOR (recursive cluster-and-summarize tree retrieval), RAFT (distractor-aware CoT fine-tuning), MMR, CAG (cache-augmented generation).
18. **(B)** Section 10.3 SHAP deep walkthrough ("not bad" single-token-masking, waterfall plot, beeswarm).
19. **(H)** Appendix A.2: multivariate Gaussian density + joint Gaussian conditioning identity (Schur complement). Needed for VAE / diffusion / GP retrieval.
20. **(H)** Section 1.1: expand the NLP task taxonomy table from 9 to 19 task families (slide 1012).
21. **(B)** Section 6.1 add a "Foundation Models" framing callout (one-FM-many-tasks vs one-model-per-task; three adaptation strategies).
22. **(H)** Section 0.2.5: AdamW genealogy (SGD → Momentum → Adagrad → RMSprop → Adam → AdamW with decoupled weight decay).
23. **(C)** Section 17.1 add NF4 anchor values + blockwise + double quantization mechanics for QLoRA.
24. **(A)** Section 3.3 add encoder-decoder reference implementation (Residual class, DecoderLayer with three residual blocks, dual mask helpers).

### Source files (must-include checklist)

Each editing subagent receives both `_INTEGRATION_PLAN.md` AND its family's gap-audit JSON:
- `slide-summaries/_gap_audit_A.json` (Part 1)
- `slide-summaries/_gap_audit_B.json` (Part 2)
- `slide-summaries/_gap_audit_C.json` (Part 4 + RL)
- `slide-summaries/_gap_audit_D.json` (Part 5 VLM)
- `slide-summaries/_gap_audit_E.json` (Part 5 Audio)
- `slide-summaries/_gap_audit_F.json` (Part 6 Agents)
- `slide-summaries/_gap_audit_G.json` (Part 7 Retrieval)
- `slide-summaries/_gap_audit_H.json` (Appendix A + Ch 0)
- Consolidated human-readable summary: `slide-summaries/_GAP_AUDIT_SUMMARY.md`

The JSON files list EVERY item with source slide deck + slide indexes + target section + status + notes. The editing subagent uses these as the explicit "must-include" checklist.

### Updated edit-footprint estimate

The plan's original §1 estimate of "~57 concrete edits" was the structural count. The gap-audit-derived count is:
- **101 partial items** to deepen (typically 1-2 sentences each, sometimes a code snippet)
- **163 missing items** to add (varies: a sentence, a paragraph, a code block, an entire sub-section)

Many missing items naturally cluster within a single new sub-section (e.g., the 53 audio missing items map to ~5 new sub-sections; the 17 retrieval missing items map to ~5 additions across 4 chapters). The **structural footprint** is unchanged: ~22 chapters touched, 2 new appendices (E, G), 1 new chapter (Ch 38 LLM-RecSys), plus the 5 new sub-sections in Ch 20.

### Recommended sequencing

Phase 1 (largest pure new content, lowest risk): Appendix E (PyTorch mini-book), Appendix G (signal processing for audio).
Phase 2: Ch 20 audio expansion (5 new sub-sections; absorbs Family E entirely).
Phase 3 (parallel): Chapter-family editor subagents in parallel waves, one per family, each receiving its slide files + its gap-audit JSON + the integration plan. Family E already covered by Phase 2; the remaining waves are A, B, C, D, F, G, H.
Phase 4: New Ch 38 (LLM-RecSys) — uses slide 1416 only, no gap audit needed since net-new.
Phase 5: Asset generation (Mermaid + Gemini illustrations).
Phase 6: Cross-reference + bibliography sweep.
Phase 7: Controller QA + audit gate.

---

**END OF PLAN — gap-audited and ready to execute.**
