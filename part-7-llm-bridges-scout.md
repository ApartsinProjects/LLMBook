# Part VII LLM-Bridge Scout

Scope: 20 sections audited across Chapter 31 (7 sections), Chapter 32 (8 sections, 5 of which are TODO stubs), Chapter 33 (5 sections), plus the Part VII landing page and the Chapter 32 landing page. The goal is to surface, for every non-text technique, the LLM/NLP analog so a reader from Parts I-VI does not feel they have wandered into a different book.

## Summary

- Sections audited: 20 (7 in Ch 31, 8 in Ch 32, 5 in Ch 33), plus Part VII index and Ch 32 index.
- Strong existing bridges: 7. The Part VII index has the unifying-thesis callout; the Chapter 32 index has a second unifying-thesis callout; section 31.1 has the "diffusion vs autoregressive" key-insight; section 31.5 has the "actions as tokens" key-insight; section 31.6 has the "planning frequency gap" key-insight; section 32.7 has "CLIP embeddings = text embeddings" key-insight; section 31.2 has the CLIP+T5 dual-encoder callout. These set the right tone but only cover a fraction of the surface area.
- Bridge opportunities flagged: 73 (an average of 3-5 per authored section, plus targeted seed callouts for the 5 TODO stubs).
- External works to cite (2024-2026): 26, listed in the appendix.
- Section duplications flagged: 31.5 vs 32.1 (VLA), 31.6 vs 32.2 (robotics), 31.7 vs 32.3 (3D Gaussian Splatting). These three section pairs cover the same material with the Chapter 32 versions still TODO. Recommendation: keep the Chapter 31 versions for the generative-stack story, gut the Chapter 32 stubs down to short "see Section 31.X" pointers OR consolidate everything into Chapter 32 and link from Chapter 31. The recommendations below assume both copies will exist for now and propose bridges for each.

## Cross-cutting unifying bridges (apply at part level)

These are the four meta-bridges that should appear, in some form, at the top of every chapter and every major section. The Part VII index already has #1 and Chapter 32 index has the action variant; #2-#4 are gap-fillers.

1. **Alignment thesis** (already present). Every multimodal model boils down to "align a non-text embedding space with the text embedding space such that text can steer it." Already in part-7 `index.html` callout `key-insight`; reinforced in `module-32-embodied-world-models/index.html`. Recommend adding a single-paragraph reminder of this thesis to the top of the Chapter 31 index and Chapter 33 index, so the framing repeats at every chapter entry point.

2. **Loss-equivalence bridge** (gap). Next-token prediction (Sec 6.2), next-frame prediction (Sec 32.4 once authored), next-action prediction (Sec 31.5 / 32.1), next-pixel denoising (Sec 31.1) all minimize a likelihood under a learned model. The forward pass and the loss surface are structurally identical; only the substrate of "the next thing" changes. Recommend a `key-insight` callout titled "One loss, four substrates" in the Chapter 31 index and a matching version in Chapter 32 index, plus pointer callouts wherever a specific loss is derived (31.1, 31.2, 31.5, 32.4).

3. **Tokenize-everything bridge** (partly present in 31.5). Image patches (ViT), audio mel-frames (Whisper), motor commands (RT-2), video frame patches (Sora) all flow through the same softmax over a vocabulary. Section 31.5 has this for actions; section 31.1 has it implicitly for ViT patches. Recommend a unified `big-picture` callout in the Part VII index titled "Every modality becomes tokens" with concrete examples per chapter.

4. **Reasoning bridge** (gap). Chain-of-thought (Sec 14.2) is the text version; world-model rollouts (Sec 32.4), 3D scene editing in token space (Sec 32.5), VLM scratchpad reasoning (Sec 32.7) are the multimodal versions. All are "predict more tokens before committing to an answer." Recommend a thesis-thread callout in section 32.4 explicitly framing world-model rollouts as the multimodal chain-of-thought.

## Module 31 (Multimodal Generation)

### Section 31.1 Image Generation and Vision-Language Models (`module-31-multimodal/section-31.1.html`)

Existing bridges: Big-picture mentions transformer architecture; key-insight callout already states "diffusion models and LLMs solve the same problem in different spaces"; a note callout references CFG; the CLIP InfoNCE math is shown.

Gaps to fix:
- BRIDGE 1 (denoising = MLE). Diffusion noise prediction minimizes the same likelihood as next-token prediction (Sec 6.2 Pre-training Objectives, `part-2-understanding-llms/module-07-pretraining-scaling-laws/section-7.2.html`). Both are score-matching against the data distribution; both minimize an ELBO. Insert a `cross-ref` callout immediately after the existing key-insight at line ~81 titled "Why diffusion is just MLE in another wrapper" pointing to Section 7.2.
- BRIDGE 2 (cross-attention = attention). Text-to-image cross-attention uses the same scaled-dot-product attention math from Section 3.3 (`part-1-foundations/module-03-sequence-models-attention/section-3.3.html`) and Section 4.1. Only difference: K, V come from the text encoder and Q from the image latent. Insert a `looking-back` callout near the Stable Diffusion section (around line ~84) titled "You already know cross-attention" pointing to Sec 3.3 and Sec 4.1.
- BRIDGE 3 (CLIP contrastive = sentence-embedding contrastive). The InfoNCE loss in CLIP is the same as the contrastive embedding loss in Section 22.1 / Module 22 (`part-5-retrieval-conversation/module-22-embeddings-vector-db/section-22.1.html`). The CLIP big-picture references "image embeddings" but does not explicitly cite the bridge to text embeddings. Insert a `cross-ref` callout right before the CLIP math block (around line ~322) titled "CLIP and BGE-M3 are the same idea" pointing to Sec 22.1 and Sec 32.7.
- BRIDGE 4 (CFG = constrained decoding). Classifier-free guidance does an extrapolation between conditional and unconditional predictions; this is structurally identical to constrained / contrastive decoding (Section 5.3, `part-1-foundations/module-05-decoding-text-generation/section-5.3.html`) where the model output is steered by a difference of logits. Insert a `looking-back` callout in the CFG note (around line ~143) pointing to Sec 5.3.
- BRIDGE 5 (DALL-E 3 prompt rewriting = RAG). DALL-E 3's "rewrite the prompt with GPT-4 then condition the diffusion model" is the same architectural move as RAG (Sec 23.1, `part-5-retrieval-conversation/module-23-rag/section-23.1.html`): an LLM augments a downstream model's context with text it generated. Insert a `cross-ref` callout in the DALL-E paragraph (around line ~175) titled "Prompt rewriting is RAG for image generation."
- BRIDGE 6 (ControlNet = LoRA-style adapter). The frozen-base + trainable-copy pattern of ControlNet (line ~206) mirrors LoRA and the PEFT adapter pattern (Module 19, `part-4-training-adapting/module-19-peft/`). Insert a `looking-back` callout titled "ControlNet is structural LoRA" pointing to Sec 19.1.
- EXTERNAL: Stable Diffusion 3 paper (Esser et al., 2024, arXiv:2403.03206) makes the flow-matching = rectified-flow MLE bridge explicit; already cited in 33.5 but not surfaced here. Pull the explicit "this is MLE on a velocity field" framing into the flow-matching subsection.

### Section 31.2 Audio, Music and Video Generation (`module-31-multimodal/section-31.2.html`)

Existing bridges: Big-picture cites Section 24.5 (conversational AI). CLIP+T5 dual-encoder why-callout already present. MusicGen code caption links to Section 5.2 (temperature in decoding).

Gaps to fix:
- BRIDGE 1 (Bark = autoregressive LM). The section already says "Bark models speech as a sequence of audio tokens using an autoregressive transformer (similar to how GPT models text)" (around line ~110). Strengthen this into a key-insight callout: "Bark IS a language model. It just uses a vocabulary of EnCodec audio tokens instead of BPE text tokens. Same loss, same architecture, same decoding (top-k, top-p, temperature from Sec 5.2). Hand a Bark trace to someone who has only read Chapter 5 and they will recognize it as a sampling diagram." Cite Sec 5.2 (`part-1-foundations/module-05-decoding-text-generation/section-5.2.html`).
- BRIDGE 2 (MusicGen = text-conditioned next-token over audio codec tokens). MusicGen's autoregressive generation of EnCodec tokens conditioned on text is structurally the same as text generation conditioned on a system prompt. Add a `cross-ref` callout in the MusicGen subsection (around line ~252) pointing to Sec 14.1 (prompt engineering) and Sec 6.2 (pretraining objectives).
- BRIDGE 3 (Video DiT temporal attention = causal masking generalized to time). The 3D DiT splits attention into spatial-cross-temporal. The temporal axis is precisely what causal masking did in language models: a model trained to predict the next frame conditioned on prior frames is doing next-token prediction in a longer-horizon vocabulary. Insert a `key-insight` callout near the Video DiT diagram (around line ~313) titled "Next-frame prediction IS next-token prediction with bigger tokens" referencing Sec 4.2 (causal masking) and 6.2.
- BRIDGE 4 (TTS pipeline = encoder-decoder LM). Modern TTS (VITS, F5-TTS) is functionally a text-conditioned audio LM. Add a `looking-back` callout connecting Sec 31.2's TTS architecture to Sec 4.3 (encoder-decoder variants) and Sec 7.1 (T5 landmark model).
- BRIDGE 5 (multimodal composition pipeline = agentic orchestration). The Figure 31.2.3 composition pipeline (LLM script -> video gen -> TTS -> music -> compositor) is a textbook agent loop from Sec 26.X (`part-6-agentic-ai/module-26-ai-agents/`). Insert a `cross-ref` callout near Figure 31.2.3 titled "This pipeline is an agent in disguise" pointing to Sec 26.1 and Sec 27.1.
- EXTERNAL: Veo 3 technical report (Google DeepMind, 2025) explicitly compares next-frame prediction to next-token prediction (search "video as a sequence problem"). Also cite "MusicGen: Simple and Controllable Music Generation" (Copet et al., 2023, arXiv:2306.05284) which is already in 33.5 but should be pulled forward for the "audio LM" framing. Cite also "Make-A-Video to Sora: A scaling story" (Liu et al. 2024 survey, arXiv:2402.17177).
- INSERTION: open the section with a single `big-picture` paragraph saying "Audio and video models are language models. Replace the BPE tokenizer with an audio codec or a 3D patch embedder, replace the causal mask with a 1D-time or 2D-spatial-1D-time mask, and the loss is unchanged. Everything in this section is a substrate variation on Chapter 4."

### Section 31.3 Document Understanding and OCR (`module-31-multimodal/section-31.3.html`)

Existing bridges: Big-picture cites Module 22.4 (chunking) and Module 04 (transformer). LayoutLM and TrOCR architecture descriptions already cite Module 04 for encoder-decoder.

Gaps to fix:
- BRIDGE 1 (TrOCR = encoder-decoder transformer). The architecture is structurally the same encoder-decoder as a translation system; the encoder happens to be ViT instead of BERT. Insert a `looking-back` callout near the TrOCR section (around line ~50) titled "TrOCR is just T5 with a vision encoder" pointing to Sec 4.3 (T5) and Sec 7.1 (landmark models).
- BRIDGE 2 (LayoutLM = positional embeddings, generalized). LayoutLM adds 2D bounding-box embeddings to text embeddings. This is the same trick as positional encoding in vanilla transformers (Sec 4.1) and rotary embeddings (Sec 4.1, sec 8.2). The "2D position" is precisely RoPE generalized from 1D. Add a `key-insight` callout near the LayoutLMv3 architecture diagram (around line ~155) titled "2D position is just positional encoding with two axes" pointing to Sec 4.1.
- BRIDGE 3 (VLM-based document understanding = zero-shot prompting). Passing a PDF image to GPT-4V is a long-form prompt engineering exercise: structured outputs from Sec 13.3 and prompt patterns from Sec 14.1 transfer directly. Already lightly cited; strengthen into an explicit `cross-ref` callout in the VLM-based-document subsection (around line ~232).
- BRIDGE 4 (Hybrid pipeline = decision framework from Ch 15). The "when to use OCR+LayoutLM vs VLM" callout already cites Ch 15. Strengthen it to a thesis-thread callout connecting back to Sec 15.2 (the hybrid framework).
- EXTERNAL: "TextMonkey: An OCR-Free Large Multimodal Model" (Liu et al., 2024, arXiv:2403.04473) makes the bridge explicit between document understanding and language modeling. Cite "DocLLM: A Layout-Aware Generative Language Model" (JPMorgan, 2024, arXiv:2401.00908) which is exactly the synthesis the section describes.

### Section 31.4 Unified Multimodal Models and Omni-Architectures (`module-31-multimodal/section-31.4.html`)

Existing bridges: Big-picture cites Sec 22.1 for embedding space. The key-insight at line 46 has the trilingual-person analogy. Self-check Q1, Q2, Q3 reinforce the framing.

Gaps to fix:
- BRIDGE 1 (early fusion = interleaved token stream = same as multi-turn dialogue). The early fusion description (line ~200) tokenizes images/audio/text and interleaves them into a single sequence. This is structurally identical to multi-turn dialogue (Sec 24.1, `part-5-retrieval-conversation/module-24-conversational-ai/section-24.1.html`) and tool-use traces (Sec 27.1) where roles (user, assistant, tool) are interleaved tokens. Insert a `looking-back` callout titled "Cross-modal interleaving is just role-tagged sequences with more roles" pointing to Sec 24.1 and Sec 27.1.
- BRIDGE 2 (omni-architectures = MoE for modalities). GPT-4o-style omni models route token streams through specialist heads for the output modality. This is the routing pattern of Mixture-of-Experts (Sec 4.3, `part-1-foundations/module-04-transformer-architecture/section-4.3.html`) and the modern landscape covers MoE in Sec 8.1 (`part-2-understanding-llms/module-08-modern-llm-landscape/section-8.1.html`). The "expert" is the modality decoder; the "router" decides which decoder fires. Insert a `key-insight` callout titled "Omni = Modality-MoE" with explicit MoE references.
- BRIDGE 3 (late fusion with projection = adapter pattern). Flamingo-style late fusion uses a frozen vision encoder plus trainable cross-attention layers; this is the adapter pattern of PEFT (Sec 19.1). Insert a `cross-ref` callout near the late-fusion subsection pointing to Sec 19.1.
- BRIDGE 4 (Gemini "thinking" mode for multimodal = test-time compute extended). The research-frontier callout at line 542 already notes Gemini 2.5 thinking is test-time compute on cross-modal tasks. Strengthen this into a thesis-thread callout connecting to Sec 9.1 (`part-2-understanding-llms/module-09-reasoning-test-time-compute/section-9.1.html`), Sec 9.2 (reasoning model architectures).
- BRIDGE 5 (the "any-to-any" generation framing). Production any-to-any generation generates tokens for whichever modality is requested, much like how a single LM can answer in any language given a prompt. Add a `big-picture` callout near the section opening explicitly: "An omni model is a polyglot. Modalities are languages with different alphabets."
- EXTERNAL: GPT-4o technical card (OpenAI, May 2024), specifically the paragraph on "everything is tokens"; Gemini 2.5 technical report (Google DeepMind, 2025); "Chameleon: Mixed-Modal Early-Fusion Foundation Models" (Meta, 2024, arXiv:2405.09818) which makes the unified-vocabulary argument most cleanly. Also "Janus: Decoupling Visual Encoding for Unified Multimodal Understanding and Generation" (DeepSeek, 2024, arXiv:2410.13848).

### Section 31.5 Embodied Multimodal Agents and Vision-Language-Action Models (`module-31-multimodal/section-31.5.html`)

Existing bridges: Big-picture explicitly states "the same transformer backbone that predicts the next token can also predict the next robot action." Already has a strong `key-insight` callout at line 60 titled "Actions as Tokens." Cross-references to Sec 31.1, Sec 31.4, and Part VI tool use.

NOTE: This section duplicates Section 32.1 (currently TODO stub). The Section 31.5 version is the better-developed one and should be the canonical home. Recommend the Section 32.1 stub be replaced with a 2-paragraph cross-reference pointing here, plus a placeholder for embodied-AI-specific content (lifecycle, deployment patterns) that does not duplicate.

Gaps to fix:
- BRIDGE 1 (RT-2 action discretization = BPE tokenization). The RT-2 paragraph (line ~67) describes mapping a 7-DOF action to integers 0-255 then converting to string tokens. This is precisely BPE tokenization (Sec 2.1, `part-1-foundations/module-02-tokenization-subword-models/section-2.1.html`) generalized to continuous signals. The same algorithm that turned text into LM-friendly tokens turns motor commands into LM-friendly tokens. Insert a `looking-back` callout titled "Action tokenization is BPE for the body" pointing to Sec 2.1.
- BRIDGE 2 (VLA fine-tuning = SFT). OpenVLA's fine-tuning on Open X-Embodiment via LoRA is the same SFT recipe as Module 18 (`part-4-training-adapting/module-18-fine-tuning-fundamentals/`). Already lightly cited but worth strengthening to a `cross-ref` callout near the OpenVLA paragraph (around line 130).
- BRIDGE 3 (VLA closed-loop control = agentic ReAct). The closed loop in Figure 31.5.1 (observation -> reasoning -> action -> new observation) is the ReAct loop from Sec 26.1 / 27.1. Add a `cross-ref` callout near Figure 31.5.1 pointing to Sec 27.1 (function calling) and Sec 26.1 (agent architectures): "A VLA is a ReAct agent whose tool is its body."
- BRIDGE 4 (action chain-of-thought). RT-2 explicitly interleaves reasoning text and action tokens. This is chain-of-thought (Sec 14.2, `part-3-working-with-llms/module-14-prompt-engineering/section-14.2.html`) where the answer is a motor command rather than a number. Add a `key-insight` callout titled "Action chain-of-thought is just chain-of-thought" with a forward pointer to Sec 9.2 (reasoning models).
- BRIDGE 5 (cross-embodiment transfer = transfer learning). The "trained on 22 robots, generalizes to a 23rd" pattern is transfer learning, same as cross-lingual transfer with multilingual LMs (Sec 7.4 data curation, Sec 8.1 modern LLMs). Add a `looking-back` callout in the Open X-Embodiment paragraph (around line 133) titled "Cross-embodiment = cross-lingual" pointing to Sec 7.4.
- EXTERNAL: "RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control" (Brohan et al., 2023, arXiv:2307.15818) is the canonical paper for the actions-as-tokens framing. "OpenVLA: An Open-Source Vision-Language-Action Model" (Kim et al., 2024, arXiv:2406.09246). "pi-0.5: Generalist Robot Policies" (Physical Intelligence, 2024, see https://www.physicalintelligence.company/blog/pi05). "Gato: A Generalist Agent" (DeepMind, 2022, arXiv:2205.06175) is the historical proof that one transformer learns text + image + action with the same loss; this is the foundational citation for the cross-cutting thesis and should appear prominently.

### Section 31.6 LLM-Powered Robotics (`module-31-multimodal/section-31.6.html`)

Existing bridges: Big-picture explicitly frames LLMs as "the cognitive layer." References Part VI (tool use) and Sec 31.5 (VLA). The `key-insight: The Planning Frequency Gap` (line ~422) is a strong existing bridge.

NOTE: Duplicates Section 32.2 (TODO stub). Same recommendation as 31.5: Section 31.6 should be canonical.

Gaps to fix:
- BRIDGE 1 (SayCan = constrained decoding with a learned reranker). SayCan combines an LLM relevance score and an affordance score by multiplication. This is structurally the same as logit-bias decoding or constrained decoding (Sec 5.3) where an external scorer reshapes the LM's distribution. Insert a `looking-back` callout titled "SayCan is constrained decoding for robots" pointing to Sec 5.3.
- BRIDGE 2 (Code-as-Policies = function-calling). The Code-as-Policies framework asks the LLM to emit code that calls primitive robot skills. This is function-calling (Sec 27.1, `part-6-agentic-ai/module-27-tool-use-protocols/section-27.1.html`) with the robot's skill library as the tool set. Add a `cross-ref` callout in the Code-as-Policies subsection titled "Code-as-Policies is function-calling, period" pointing to Sec 27.1.
- BRIDGE 3 (multi-robot coordination = multi-agent systems). Section 31.6.3 covers a multi-robot coordinator. This is multi-agent orchestration from Sec 28.X (`part-6-agentic-ai/module-28-multi-agent-systems/`). Replace the implicit framing with an explicit `cross-ref` callout pointing to Module 28.
- BRIDGE 4 (hierarchical planning = nested chain-of-thought). The hierarchical planning subsection (line ~419) has the LLM emit strategic directives translated by low-level controllers. This is hierarchical CoT (Sec 14.2). Add a `looking-back` callout pointing to Sec 14.2.
- BRIDGE 5 (edge deployment = inference optimization). The Jetson deployment section (line ~433) covers quantization, KV cache memory, latency. All these concepts come from Module 10 (`part-2-understanding-llms/module-10-inference-optimization/`). Add a `cross-ref` callout near the Jetson hardware paragraph titled "Edge robot deployment IS inference optimization" pointing to Sec 10.1 (quantization), Sec 10.3 (KV cache).
- EXTERNAL: "Code as Policies: Language Model Programs for Embodied Control" (Liang et al., 2023, arXiv:2209.07753). "Do As I Can, Not As I Say: Grounding Language in Robotic Affordances" (Ahn et al., 2022, arXiv:2204.01691) - the SayCan paper. "Voxposer: Composable 3D Value Maps for Robotic Manipulation with Language Models" (Huang et al., 2023, arXiv:2307.05973). "Inner Monologue: Embodied Reasoning through Planning with Language Models" (Huang et al., 2022, arXiv:2207.05608) makes the chain-of-thought bridge most explicitly.

### Section 31.7 3D Gaussian Splatting and Neural Scene Representation (`module-31-multimodal/section-31.7.html`)

Existing bridges: Big-picture cites Module 04 (transformer). Key-insight callout at line 68 ("Explicit vs. Implicit Representations") is a useful frame.

NOTE: Duplicates Section 32.3 (TODO stub). Same recommendation: 31.7 is canonical.

Gaps to fix:
- BRIDGE 1 (Gaussians as addressable primitives = keys in attention / KV cache). Each Gaussian is an explicit, addressable, parameterized primitive (μ, Σ, α, SH). This is structurally identical to keys/values in an attention layer, and to entries in a KV cache (Sec 10.3, `part-2-understanding-llms/module-10-inference-optimization/section-10.3.html`). Rendering = projection + soft-pooling, which is what attention does over a sequence. Insert a `key-insight` callout titled "Gaussians are keys; the camera is a query" pointing to Sec 3.3 (scaled dot-product attention) and Sec 10.3.
- BRIDGE 2 (3DGS densification = sparse-attention / token pruning). The adaptive density control (split / clone / prune) at line 89 dynamically grows the representation where the scene is complex and shrinks it where it is flat. This is exactly the routing logic in sparse attention (Sec 4.3, MoE / efficient attention) and KV-cache eviction policies (Sec 10.3). Add a `looking-back` callout titled "Adaptive density is sparse attention for geometry" pointing to Sec 4.3.
- BRIDGE 3 (SH coefficients = positional encoding for direction). Spherical harmonics are a frequency-domain basis for functions on the sphere. They serve the same role as sinusoidal positional encoding (Sec 4.1) or RoPE (Sec 4.1): a learned-coefficient frequency basis that lets the model express any function up to the chosen degree. Add a `looking-back` callout in the SH subsection (around line 102) titled "SH is positional encoding for view direction" pointing to Sec 4.1.
- BRIDGE 4 (SDS = REINFORCE with a learned reward). Score Distillation Sampling (line 176) uses a frozen 2D diffusion model as a critic, taking gradients through it back to the 3D representation. Conceptually this is RLHF (Module 20, `part-4-training-adapting/module-20-rlhf-alignment/`) with the diffusion model as the reward model and the 3D Gaussians as the policy. Insert a `key-insight` callout titled "Score Distillation is RLHF with a diffusion critic" pointing to Sec 20.1.
- BRIDGE 5 (3DGS as compressed scene representation = embedding). A million-Gaussian scene is a compressed, differentiable, queryable representation of a high-dimensional signal. This is the same role text embeddings play for documents (Sec 22.1). Add a `cross-ref` callout connecting splats to embeddings.
- BRIDGE 6 (text-to-3D = text-conditioned generation = text-to-image with one more axis). Already implicit but should be explicit: text-to-3D is text-to-image lifted to a renderable 3D representation by SDS. Insert a `looking-back` callout in the DreamGaussian paragraph pointing to Sec 31.1.
- EXTERNAL: "3D Gaussian Splatting for Real-Time Radiance Field Rendering" (Kerbl et al., 2023, arXiv:2308.04079) - already cited. "DreamFusion: Text-to-3D using 2D Diffusion" (Poole et al., 2022, arXiv:2209.14988) for the SDS=distillation framing. "Gaussian Splatting SLAM" (Matsuki et al., 2024, arXiv:2312.06741) shows how splats integrate with planning loops, useful for the bridge to robotics. "LGM: Large Multi-View Gaussian Model for High-Resolution 3D Content Creation" (Tang et al., 2024, arXiv:2402.05054) is the closest analog of "tokenize the scene then run a transformer over the tokens."

## Module 32 (Embodied AI, World Models, and Multimodal Reasoning)

### Section 32.1 Embodied Multimodal Agents and Vision-Language-Action Models (TODO stub)

This section is currently a 37-line scaffold. When authored:

- FIRST CALLOUT (big-picture, mandatory): "VLA models predict action tokens. The 'action' vocabulary is just additional tokens added to the transformer's softmax. If you understood Section 4.4 on the LM head (`part-1-foundations/module-04-transformer-architecture/section-4.4.html`) and Section 27.1 on tool-calling (`part-6-agentic-ai/module-27-tool-use-protocols/section-27.1.html`), you already understand 90 percent of VLA; the remaining 10 percent is the data-collection plumbing."
- SECOND CALLOUT (looking-back): pointer to Section 31.5 if 31.5 remains canonical. Recommend EITHER consolidating both into Section 32.1 (then leaving 31.5 as a pointer in Chapter 31) OR keeping 31.5 canonical and turning 32.1 into the deployment / embodiment-aware perspective (sim-to-real, hardware safety envelopes, edge SLOs). Either way, the bridges from 31.5 should not be duplicated; they should be referenced.
- BRIDGES to inherit from 31.5: action-tokenization-is-BPE, closed-loop-is-ReAct, action-CoT-is-CoT, cross-embodiment-is-cross-lingual.

### Section 32.2 LLM-Powered Robotics: Navigation, Planning, and Multi-Robot Coordination (TODO stub)

When authored:

- FIRST CALLOUT (big-picture): same SayCan-is-constrained-decoding, Code-as-Policies-is-function-calling framing from 31.6.
- Recommend this section absorb 31.6 (or vice versa) rather than running parallel.
- BRIDGES to inherit: SayCan, Code-as-Policies, multi-robot=multi-agent, edge=inference-optimization.

### Section 32.3 3D Gaussian Splatting and Neural Scene Representation (TODO stub)

When authored:

- FIRST CALLOUT (key-insight): "Gaussians are keys; the camera is a query." Bridge to Sec 3.3 and Sec 10.3.
- Same recommendation: consolidate with 31.7.
- BRIDGES to inherit: Gaussians-are-keys, densification-is-sparse-attention, SH-is-positional, SDS-is-RLHF.

### Section 32.4 World Models: Video Generation, Simulation, and Embodied Reasoning (TODO stub - PRIORITY)

This is the most important Chapter 32 stub because world models are the conceptual heart of "imagination" in the embodied stack. When authored:

- OPENING CALLOUT (key-insight, mandatory): "World models are next-frame predictors trained with the same maximum-likelihood objective you read in Section 6.2 (`part-2-understanding-llms/module-07-pretraining-scaling-laws/section-7.2.html`). The token is a video frame patch instead of a BPE token; the context is past frames and the current action; the loss is unchanged. When you read 'predict the next frame conditioned on the action,' read 'next-token prediction with a richer alphabet.' Everything else in this section is engineering around that loss."
- SECOND CALLOUT (thesis-thread, mandatory): "World-model rollouts are chain-of-thought, embodied. A reasoning LLM thinks before answering by generating intermediate tokens (Sec 9.1). A world-model-using agent thinks before acting by rolling out a few imagined futures and picking the action that leads to the preferred future. Same algorithm, different alphabet."
- BRIDGE 3 (V-JEPA = self-supervised representation learning, structurally identical to MLM). Yann LeCun's JEPA architecture pretrains by predicting masked patches; this is BERT's MLM (Sec 7.2) lifted to video. Add a `looking-back` callout to Sec 7.2.
- BRIDGE 4 (Genie 3 controllability = system-prompt conditioning). Genie 3 takes an image and a sequence of keyboard inputs, generating playable footage. The keyboard input is a control prompt; the image is the system context. This is the same pattern as instruction-following LMs (Sec 17.X, `part-4-training-adapting/module-17-instruction-tuning/`).
- BRIDGE 5 (model-based RL = planning over learned rollouts = MCTS over LLM samples). Model-based RL plans with a learned dynamics model. Modern reasoning models (Sec 9.X) plan with MCTS over sampled completions. Both algorithms are "look ahead in a learned simulator." Add a thesis-thread callout titled "World-model planning and o1-style MCTS are the same algorithm."
- EXTERNAL: "Genie 2: A Large-Scale Foundation World Model" (Parker-Holder et al., DeepMind, 2024, https://deepmind.google/research/breakthroughs/genie-2/). "V-JEPA: Video Joint-Embedding Predictive Architecture" (Bardes et al., Meta, 2024, arXiv:2404.08471). "GAIA-1: A Generative World Model for Autonomous Driving" (Wayve, 2023, arXiv:2309.17080). "Sora: Video Generation Models as World Simulators" (OpenAI tech report, 2024). "World Models" (Ha and Schmidhuber, 2018, arXiv:1803.10122) is the foundational paper for the framing.

### Section 32.5 3D Asset Generation and Neural Scenes (`module-32-embodied-world-models/section-32.5.html`)

Existing bridges: Big-picture cites Section 31.1 (diffusion). References Section 32.3 (Gaussian splats) and Section 32.4 (world models). Key-insight at line 40 names multi-view consistency as the bottleneck.

Gaps to fix:
- BRIDGE 1 (Trellis structured latents = compressed token vocabulary). Trellis denoises a structured latent on a sparse voxel grid. Each occupied voxel carries a latent vector; this is a learned tokenization of geometry (Sec 2.1 tokenizers, Sec 22.1 embeddings). Add a `looking-back` callout titled "Structured latents are BPE for geometry" pointing to Sec 2.1 and Sec 22.1.
- BRIDGE 2 (multi-view cross-attention = shared self-attention across "sentences"). The "modern 3D generators solve consistency by cross-attention between view tokens" is structurally identical to long-document attention where chunks attend to each other (Sec 4.3, efficient attention). Add a `cross-ref` callout.
- BRIDGE 3 (DreamGen synthetic robot trajectories = synthetic data augmentation). DreamGen generates synthetic robot trajectories to expand training data; this is the same idea as synthetic instruction data (Sec 17.X, instruction tuning) and self-instruct. Add a `looking-back` callout in the DreamGen paragraph (around line 54) pointing to Sec 17.2 or wherever self-instruct is covered. Recommend explicit framing: "Generated rollouts are to robotics what self-instruct is to LLMs."
- BRIDGE 4 (multiple decoder heads from one trunk = MoE). Trellis's "produces meshes, splats, and NeRFs from one model" is a Modality-MoE for 3D representations. Add a `key-insight` callout connecting Trellis decoders to the MoE pattern (Sec 4.3, Sec 8.1).
- EXTERNAL: "Trellis: Structured 3D Latents for Scalable and Versatile 3D Generation" (Xiang et al., Microsoft, 2024, arXiv:2412.01506). "Stable Zero123: Quality 3D Object Generation from Single Images" (Stability AI, 2023, https://stability.ai/news/stable-zero123-3d-generation). "DreamGen: Unlocking Generalization in Robot Learning through Neural Trajectories" (NVIDIA, 2025, https://research.nvidia.com/labs/gear/dreamgen/). "Genie 2: World Models for Game Worlds" (DeepMind, 2024).

### Section 32.6 Multimodal Editing and Inpainting (`module-32-embodied-world-models/section-32.6.html`)

Existing bridges: Big-picture frames editing as "conditional generation where most of the output must stay identical to the input." References Sec 31.1, Sec 31.3, Sec 22.1. Key-insight at line 42 names identity preservation as the central design pattern.

Gaps to fix:
- BRIDGE 1 (InstructPix2Pix = instruction tuning for images). The "train on (original, instruction, edit) triples" recipe at line 36 is precisely instruction tuning (Module 17). The supervised signal is the same; the input modality is different. Insert a `looking-back` callout titled "InstructPix2Pix is instruction tuning, with pixels" pointing to Sec 17.1 (instruction tuning fundamentals).
- BRIDGE 2 (FLUX.1 Kontext joint sequence = multi-turn dialog). The "treat input image and edit instruction as a joint sequence in cross-attention" architectural choice at line 40 mirrors how chat templates interleave user/assistant turns (Sec 24.1). Insert a `cross-ref` callout pointing to Sec 24.1.
- BRIDGE 3 (identity preservation via reference embedding = sentence-embedding identity). The reference embedding that captures hair / face / style is functionally an "identity embedding" in a learned space; same as a speaker embedding for voice cloning (Sec 31.2 F5-TTS) or a sentence embedding for paraphrase invariance (Sec 22.1). Add a `looking-back` callout.
- BRIDGE 4 (video temporal consistency = caching). Sharing attention across frames so "the cat" is computed once and reused throughout the clip is structurally the same as KV caching across decoding steps (Sec 10.3). Add a `looking-back` callout in the video-remixing subsection (around line 47).
- BRIDGE 5 (audio stem editing = controlled decoding with per-track conditioning). Stem-level remixing is conditional generation where the condition includes a partial reconstruction; same as constrained decoding (Sec 5.3) where part of the output is fixed and the rest is generated. Add a `looking-back` callout.
- BRIDGE 6 (scene relighting = disentangled latent edit = sparse autoencoder feature editing). The "decompose into intrinsic components, edit one, hold the rest fixed" pattern at line 56 is structurally the same as editing a sparse-autoencoder feature in an LLM (Sec 11.X interpretability). Add a `cross-ref` callout titled "Scene relighting is feature steering, for photons" pointing to Sec 11.3 or wherever sparse autoencoder steering is covered.
- EXTERNAL: "InstructPix2Pix: Learning to Follow Image Editing Instructions" (Brooks et al., 2022, arXiv:2211.09800). "Emu Edit: Precise Image Editing via Recognition and Generation Tasks" (Meta, 2023, arXiv:2311.10089). "FLUX.1 Kontext model card" (Black Forest Labs, 2024). "InstructVid2Vid" (2024) which makes the instruction-tuning analogy explicit for video.

### Section 32.7 Multimodal Reasoning and Cross-Modal Retrieval (`module-32-embodied-world-models/section-32.7.html`)

Existing bridges: The big-picture frame at line 30 already states "cross-modal retrieval and multimodal reasoning are the same problem at different temperatures." The key-insight callout at line 42 explicitly says "CLIP embeddings are the multimodal equivalent of text embeddings" and cites Sec 22.1. The Generative VLMs subsection cites Sec 22.1 and Sec 34.1. The retrieve-then-rerank pattern is explicitly framed as the multimodal analog of RAG.

This is the best-bridged section in Part VII. Minor strengthening:

- BRIDGE 1 (SigLIP sigmoid loss = pairwise contrastive loss, decoupled from batch size). The SigLIP improvement is a concrete example of "loss engineering," same family as the loss-function design discussions in pretraining (Sec 6.2). Add a small `looking-back` callout pointing to Sec 6.2.
- BRIDGE 2 (BLIP-3 / LLaVA architecture = adapter pattern). The standard VLM architecture (vision encoder + projector + LLM decoder) is the PEFT adapter pattern (Sec 19.1). Already implicit; consider a one-line cross-ref.
- BRIDGE 3 (multimodal RAG = RAG). Already implicit. Strengthen the existing connection to Sec 23.1 by explicit citation in the "retrieve then rerank" paragraph at line 58.
- BRIDGE 4 (MMMU saturation = benchmark gaming). The saturation story at line 51 is the same dynamic as MMLU saturation in text (Module 34 evaluation). Add a `cross-ref` callout to Sec 34.2.
- EXTERNAL: "SigLIP: Sigmoid Loss for Language Image Pre-Training" (Zhai et al., 2023, arXiv:2303.15343). "BLIP-3 (xGen-MM): Vision Language Models" (Salesforce, 2024, arXiv:2408.08872). "MMMU: A Massive Multi-discipline Multimodal Understanding and Reasoning Benchmark" (Yue et al., 2024, arXiv:2311.16502). "ImageBind: One Embedding Space to Bind Them All" (Meta, 2023, arXiv:2305.05665) is essential as the strongest empirical demonstration that all modalities can be aligned to a single embedding space.

### Section 32.8 Robotics, Embodied AI, and Scientific Discovery (TODO stub)

When authored:

- FIRST CALLOUT (big-picture): "Scientific discovery is the embodied version of agent loops. A scientific agent perceives an experiment (Sec 32.7 retrieval), plans the next experiment (Sec 14.2 chain-of-thought, Sec 32.4 world-model rollouts), executes via a robot (Sec 32.1 VLA), interprets the result (Sec 32.7 reasoning), updates its beliefs (Sec 23.X RAG over its own results), and decides the next move (Sec 26.1 agent architecture). Every section in Part VII contributes a brick to this loop; section 32.8 is where the bricks become a building."
- SECOND CALLOUT (thesis-thread): A discovery system is a multi-agent application (Sec 28.X) deployed against the physical world. FunSearch, A-Lab, ChemCrow are domain-specialized versions of the agent patterns in Chapter 26.
- EXTERNAL: "FunSearch: Mathematical discoveries from program search with large language models" (Romera-Paredes et al., DeepMind, 2024, Nature). "A-Lab: An autonomous materials discovery laboratory" (LBNL, 2023, Nature). "ChemCrow: Augmenting Large-Language Models with Chemistry Tools" (Bran et al., 2023, arXiv:2304.05376). "Coscientist: Autonomous chemical research with large language models" (Boiko et al., 2023, Nature). "Scientist-AI: Autonomous Generation of Hypotheses by LLMs" (Wang et al., 2024).

## Module 33 (Tools of the Trade: Multimodal Stack)

The Chapter 33 sections are short reference sheets (50-70 lines each). They are intentionally light on framing. The recommendation here is to add ONE short framing paragraph at the top of each, plus a "what to read in Parts I-VI" pointer for readers who arrive at the toolchain without the conceptual background.

### Section 33.1 Platforms (`module-33-tools-of-the-trade/section-33.1.html`)

- INSERTION: prepend a single paragraph: "Multimodal platforms split the same way text LLM platforms do (Sec 13.X): closed APIs at the frontier, open weights behind them. Reading Sec 13.1 (provider APIs) and Sec 16.1 (tool stack) prepares you for the calling patterns here. The only platform-specific surprises are the latency profiles (image: seconds; video: minutes) and pricing (multimodal tokens are large)." Connect to Sec 13.1 and Sec 16.1.
- EXTERNAL: Replicate and fal.ai documentation pages already cited; add a pointer to Modal's image-gen template (https://modal.com/docs/examples/stable-diffusion-xl) for self-hosted deployment.

### Section 33.2 Libraries and Frameworks (`module-33-tools-of-the-trade/section-33.2.html`)

- INSERTION: prepend a paragraph: "The multimodal library stack rhymes with the text LLM stack from Sec 12.X (model and tokenizer toolkit) and Sec 16.X (LLM API stack). Hugging Face's diffusers is the multimodal analog of transformers. The patterns - pipeline classes, model checkpoints, schedulers - mirror the autoregressive analogs. If you have used transformers, you can use diffusers." Cite Sec 12.1, Sec 16.1.
- INSERTION 2: in the multimodal-LLM toolkits subsection, add a one-line note that LLaVA and InternVL are loaded with the same `AutoModelForVision2Seq` interface used in Sec 31.1 code samples, which itself is the same `AutoModelFor*` family used throughout Module 12.

### Section 33.3 Datasets and Benchmarks (`module-33-tools-of-the-trade/section-33.3.html`)

- INSERTION: prepend a paragraph: "Multimodal datasets follow the same shape as text pretraining datasets (Sec 7.4 data curation): a noisy web-scale corpus for pretraining (LAION, WebVid) and curated evaluation sets for benchmarking (COCO, VBench, MMMU). The quality / scale / contamination tradeoffs from Sec 7.4 apply directly; only the modality changes." Cite Sec 7.4 (data curation) and Sec 34.2 (benchmarking).
- INSERTION 2: add MMMU explicitly to the benchmark list (it is mentioned in Section 31.4 but missing from the 33.3 catalog).
- EXTERNAL: "DataComp: In search of the next generation of multimodal datasets" (Gadre et al., 2023, arXiv:2304.14108).

### Section 33.4 Models (`module-33-tools-of-the-trade/section-33.4.html`)

- INSERTION: prepend a paragraph: "The model zoo mirrors Sec 12.X (text model zoo). Frontier APIs lead on quality, open weights lead on flexibility, and 'speed-focused' variants exist for both. The same forecasting heuristic from Sec 12.X applies: today's SOTA is next quarter's commodity; build behind an interface." Cite Sec 12.X.
- INSERTION 2: add a one-paragraph framing block titled "Same loss, different artifacts" emphasizing that Imagen, Veo, Suno, Whisper, ElevenLabs, OpenVLA all minimize a likelihood under text/audio/pixel/action data. Different artifacts, identical training paradigm.

### Section 33.5 External Reading and Communities (`module-33-tools-of-the-trade/section-33.5.html`)

- INSERTION: prepend a paragraph: "Like Sec 16.5 (LLM communities), the multimodal reading list splits across foundational papers, applied tutorials, and online communities. The convention from Sec 16.5 - skim arXiv for theory, read fast-moving blogs for practice, lurk Discord for releases - applies." Cite Sec 16.5.
- ADDITIONS to the foundational-papers list:
  - "Gato: A Generalist Agent" (DeepMind, 2022, arXiv:2205.06175) - the strongest single citation for the cross-cutting thesis.
  - "Chameleon: Mixed-Modal Early-Fusion Foundation Models" (Meta, 2024, arXiv:2405.09818) - canonical "one transformer for all modalities" paper.
  - "RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control" (Brohan et al., 2023, arXiv:2307.15818) - canonical "actions as tokens" paper.
  - "DreamFusion: Text-to-3D using 2D Diffusion" (Poole et al., 2022, arXiv:2209.14988) - canonical "distill 2D priors into 3D via SDS" paper.
  - "Sora: Video Generation Models as World Simulators" (OpenAI, 2024) - canonical "video as a sequence problem" framing.
  - "World Models" (Ha and Schmidhuber, 2018, arXiv:1803.10122) - foundational world-model paper.
  - "Genie 2: A Large-Scale Foundation World Model" (DeepMind, 2024) and Genie 3 (2025).
  - "ImageBind: One Embedding Space to Bind Them All" (Meta, 2023, arXiv:2305.05665).
- ADDITIONS to communities: r/MachineLearning, Hugging Face daily papers, LeRobot Discord (the central robotics-LM community as of 2026).

## Cross-cutting "looking-back" callouts to add

These callouts should appear in every Part VII section opening (after the prerequisites block) to set the bridge framing before the technical content. Format suggestion: a small `looking-back` callout with three bullet points naming the three Part-I-VI sections the reader can lean on, and one sentence saying why.

For each section the recommended triplet:

- 31.1 Image Generation: Sec 3.3 (attention math), Sec 6.2 (MLE pretraining), Sec 22.1 (contrastive embeddings).
- 31.2 Audio/Video: Sec 2.1 (BPE = audio codec tokens), Sec 5.2 (sampling), Sec 6.2 (MLE).
- 31.3 OCR/Documents: Sec 4.1 (positional encoding), Sec 4.3 (encoder-decoder T5), Sec 15.2 (hybrid ML decision framework).
- 31.4 Omni-Architectures: Sec 4.3 (MoE routing), Sec 24.1 (interleaved roles), Sec 9.1 (test-time compute).
- 31.5 VLA: Sec 2.1 (BPE), Sec 4.4 (LM head), Sec 27.1 (function calling / tool use).
- 31.6 Robotics Planning: Sec 5.3 (constrained decoding), Sec 14.2 (chain-of-thought), Sec 27.1 (function calling), Sec 28.1 (multi-agent).
- 31.7 Gaussian Splatting: Sec 3.3 (attention), Sec 4.1 (positional encoding for SH), Sec 10.3 (KV cache as addressable primitives), Sec 20.1 (RLHF for SDS).
- 32.1 VLA (when authored): inherit from 31.5.
- 32.2 Robotics (when authored): inherit from 31.6.
- 32.3 3DGS (when authored): inherit from 31.7.
- 32.4 World Models (when authored): Sec 6.2 (MLE next-frame), Sec 7.2 (MLM = JEPA), Sec 9.1 (test-time compute = rollouts).
- 32.5 3D Asset Generation: Sec 2.1 (latents as BPE for geometry), Sec 4.3 (MoE for multi-decoder), Sec 17.2 (self-instruct = DreamGen).
- 32.6 Editing: Sec 5.3 (constrained decoding), Sec 10.3 (KV cache = temporal sharing), Sec 11.3 (interpretability = scene relighting feature steering), Sec 17.1 (instruction tuning).
- 32.7 Multimodal Reasoning: already well-bridged. Add Sec 23.1 (RAG = retrieve-then-rerank).
- 32.8 Scientific Discovery (when authored): Sec 26.1 (agent loop), Sec 28.1 (multi-agent), Sec 23.4 (deep research RAG).
- 33.1 Platforms: Sec 13.1 (provider APIs), Sec 16.1 (LLM stack).
- 33.2 Libraries: Sec 12.1, Sec 16.1.
- 33.3 Datasets: Sec 7.4 (data curation), Sec 34.2 (benchmarks).
- 33.4 Models: Sec 12.X (text model zoo).
- 33.5 External Reading: Sec 16.5.

## Appendix: external-work citation list (alphabetical)

Each entry is the title + arxiv ID / URL. Year and one-line "why this paper is the right citation for the bridge" included.

- "3D Gaussian Splatting for Real-Time Radiance Field Rendering" (Kerbl et al., 2023, arXiv:2308.04079). The foundational 3DGS paper; already in 33.5.
- "Chameleon: Mixed-Modal Early-Fusion Foundation Models" (Meta, 2024, arXiv:2405.09818). Strongest single argument for the unified-vocabulary thesis.
- "ChemCrow: Augmenting Large-Language Models with Chemistry Tools" (Bran et al., 2023, arXiv:2304.05376). For 32.8.
- "Code as Policies: Language Model Programs for Embodied Control" (Liang et al., 2023, arXiv:2209.07753). For the function-calling=Code-as-Policies bridge in 31.6 / 32.2.
- "Coscientist: Autonomous chemical research with large language models" (Boiko et al., 2023, Nature). For 32.8.
- "DataComp: In search of the next generation of multimodal datasets" (Gadre et al., 2023, arXiv:2304.14108). For 33.3.
- "DocLLM: A Layout-Aware Generative Language Model" (JPMorgan, 2024, arXiv:2401.00908). For 31.3 bridge to language modeling.
- "DreamFusion: Text-to-3D using 2D Diffusion" (Poole et al., 2022, arXiv:2209.14988). Canonical SDS=distillation paper for 31.7 / 32.5.
- "Emu Edit: Precise Image Editing via Recognition and Generation Tasks" (Meta, 2023, arXiv:2311.10089). For 32.6 instruction-tuning bridge.
- "FunSearch: Mathematical discoveries from program search with large language models" (Romera-Paredes et al., 2024, Nature). For 32.8.
- "GAIA-1: A Generative World Model for Autonomous Driving" (Wayve, 2023, arXiv:2309.17080). For 32.4 world models.
- "Gato: A Generalist Agent" (DeepMind, 2022, arXiv:2205.06175). THE foundational citation for "one transformer learns text + image + action with the same loss." Should be the most prominent citation in the Part VII index thesis callout.
- "Gaussian Splatting SLAM" (Matsuki et al., 2024, arXiv:2312.06741). For 31.7 robotics integration.
- "Genie 2: A Large-Scale Foundation World Model" (DeepMind, 2024). For 32.4 / 32.5.
- "ImageBind: One Embedding Space to Bind Them All" (Meta, 2023, arXiv:2305.05665). Empirical proof that all modalities can share one embedding space; cite in 32.7 and Part VII index.
- "Inner Monologue: Embodied Reasoning through Planning with Language Models" (Huang et al., 2022, arXiv:2207.05608). For 31.6 chain-of-thought bridge.
- "InstructPix2Pix: Learning to Follow Image Editing Instructions" (Brooks et al., 2022, arXiv:2211.09800). For 32.6 instruction-tuning bridge.
- "Janus: Decoupling Visual Encoding for Unified Multimodal Understanding and Generation" (DeepSeek, 2024, arXiv:2410.13848). For 31.4 omni-architecture story.
- "LGM: Large Multi-View Gaussian Model for High-Resolution 3D Content Creation" (Tang et al., 2024, arXiv:2402.05054). For 31.7 / 32.5.
- "MMMU: A Massive Multi-discipline Multimodal Understanding and Reasoning Benchmark" (Yue et al., 2024, arXiv:2311.16502). For 32.7 and 33.3.
- "OpenVLA: An Open-Source Vision-Language-Action Model" (Kim et al., 2024, arXiv:2406.09246). For 31.5 / 32.1.
- "pi-0.5: A Vision-Language-Action Model for Generalist Robot Policies" (Physical Intelligence, 2024, https://www.physicalintelligence.company/blog/pi05). For 31.5 / 32.1.
- "RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control" (Brohan et al., 2023, arXiv:2307.15818). Canonical actions-as-tokens citation.
- "SigLIP: Sigmoid Loss for Language Image Pre-Training" (Zhai et al., 2023, arXiv:2303.15343). For 32.7.
- "Sora: Video Generation Models as World Simulators" (OpenAI, 2024). For 31.2 / 32.4 video-as-sequence framing.
- "Stable Diffusion 3" (Esser et al., 2024, arXiv:2403.03206). For flow-matching=MLE bridge in 31.1.
- "Stable Zero123: Quality 3D Object Generation from Single Images" (Stability AI, 2023). For 32.5.
- "TextMonkey: An OCR-Free Large Multimodal Model" (Liu et al., 2024, arXiv:2403.04473). For 31.3.
- "Trellis: Structured 3D Latents for Scalable and Versatile 3D Generation" (Xiang et al., Microsoft, 2024, arXiv:2412.01506). For 32.5.
- "V-JEPA: Video Joint-Embedding Predictive Architecture" (Bardes et al., Meta, 2024, arXiv:2404.08471). For 32.4 self-supervised=MLM bridge.
- "Voxposer: Composable 3D Value Maps for Robotic Manipulation with Language Models" (Huang et al., 2023, arXiv:2307.05973). For 31.6 / 32.2.
- "World Models" (Ha and Schmidhuber, 2018, arXiv:1803.10122). The foundational world-model paper; cite in 32.4.
