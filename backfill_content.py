"""Per-section content for structural backfill (epigraph, big-picture, prereqs).

The dict CONTENT maps section paths to a dict with up to three keys:
- 'epigraph': {'quote': str, 'agent': str, 'persona': str, 'avatar': str (filename no ext)}
- 'big_picture': str  (HTML paragraph content; must mention LLM/agent/RAG/etc.)
- 'prereq': str  (HTML paragraph content)

Insertion rules:
- Epigraph goes immediately after the pagefind-meta-injected spans (top of <main>).
- Big-picture callout goes right after epigraph.
- Prereqs go after big-picture, before the first h2.
- If a section already has any of these, do not insert that one.
- No em-dashes anywhere.

Colors for agents are looked up from AGENT_COLORS.
"""

AGENT_COLORS = {
    'sage': '#7f8c8d', 'attn': '#e94560', 'compass': '#34495e', 'deploy': '#2c3e50',
    'eval': '#f39c12', 'frontier': '#16a085', 'rag': '#9b59b6', 'quant': '#1abc9c',
    'scale': '#2c3e50', 'prompt': '#e67e22', 'echo': '#f39c12', 'tensor': '#16a085',
    'sched': '#2ecc71', 'spectra': '#3498db', 'token': '#d35400', 'distill': '#1abc9c',
    'greedy': '#27ae60', 'kv': '#9b59b6', 'lexica': '#9b59b6', 'pip': '#3498db',
    'norm': '#95a5a6', 'finetune': '#16a085', 'guard': '#c0392b', 'sentinel': '#16a085',
    'reward': '#e67e22', 'merge': '#1abc9c', 'context': '#34495e', 'bert': '#3498db',
    'pixel': '#9b59b6', 'sparky': '#e67e22', 'cosine': '#1abc9c', 'chinchilla': '#34495e',
    'label': '#27ae60', 'vec': '#1abc9c', 'lora': '#9b59b6', 'probe': '#3498db',
    'synth': '#9b59b6', 'dropout': '#e67e22', 'hallux': '#c0392b', 'batch': '#34495e',
    'loss': '#c0392b', 'census': '#34495e',
}


def ep(quote, agent, persona, avatar=None):
    """Helper for epigraph entries."""
    if avatar is None:
        avatar = agent.lower()
    return {
        'quote': quote, 'agent': agent, 'persona': persona, 'avatar': avatar,
    }


CONTENT = {

    # ==================================================================
    # Module 6 (Pretraining)
    # ==================================================================
    'part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.9.html': {
        'epigraph': ep(
            "I burned a real GPU-hour on real tokens last Tuesday, and now I understand cross-entropy in a way no slide deck ever managed.",
            'Tensor', 'GPU-Hour-Veteran'),
        'prereq': 'This lab assumes the transformer internals from <a href="../../part-1-llm-building-blocks/module-04-transformer-architecture-self-attention/section-4.1.html">Section 4.1</a>, the next-token prediction objective from <a href="section-6.2.html">Section 6.2</a>, and the scaling-law intuitions from <a href="section-6.3.html">Section 6.3</a>. You should be comfortable with PyTorch modules, dataloaders, and basic CUDA tensor operations from <a href="../../part-1-llm-building-blocks/module-00-ml-pytorch-foundations/section-0.3.html">Section 0.3</a>. Access to a single GPU with 8 GB or more of VRAM is enough; the lab also runs on CPU for the smallest configuration.',
    },

    # ==================================================================
    # Module 10 (Interpretability tools-of-trade pages: 10.5-10.9)
    # ==================================================================
    'part-2-understanding-llms/module-10-interpretability/section-10.5.html': {
        'epigraph': ep(
            "Every platform promises to make serving a 70B model easy. The one that wins is the one that admits it never gets easier, only different.",
            'Deploy', 'Platform-Weary'),
        'big_picture': 'Part II\'s platform question shifts from "where do I run a 100-million-parameter model" to "where do I run a 70-billion-parameter LLM and still pay rent". This section catalogs the inference platforms (vLLM, TGI, TensorRT-LLM, Together, Anyscale, Modal) that have consolidated around the open-weights LLM stack in 2026, and it tells you which platform fits which workload shape, from local-laptop experimentation to multi-region agentic RAG production.',
        'prereq': 'This section assumes you understand inference-time compute costs from <a href="../module-09-inference-deployment/section-9.1.html">Section 9.1</a>, the open-versus-closed model split from <a href="../../part-3-working-with-llms/module-11-llm-apis/section-11.1.html">Section 11.1</a>, and the KV-cache mechanics from <a href="../module-09-inference-deployment/section-9.3.html">Section 9.3</a>. Quantization basics from <a href="section-10.1.html">Section 10.1</a> will help you compare platforms on like-for-like throughput.',
    },
    'part-2-understanding-llms/module-10-interpretability/section-10.6.html': {
        'epigraph': ep(
            "TGI, vLLM, and TensorRT-LLM all post the same throughput on the same benchmark. The one you pick will be decided by which one your on-call engineer can fix at 3 AM.",
            'Pip', 'Library-Triage'),
        'prereq': 'This section assumes familiarity with the Hugging Face transformers ecosystem from <a href="../../part-3-working-with-llms/module-12-llm-libraries-frameworks/section-12.1.html">Section 12.1</a> and LLM inference fundamentals from <a href="../module-09-inference-deployment/section-9.1.html">Section 9.1</a>. The platform shelf in <a href="section-10.5.html">Section 10.5</a> provides the context for why each library exists.',
    },
    'part-2-understanding-llms/module-10-interpretability/section-10.7.html': {
        'epigraph': ep(
            "Trillions of tokens go in, sometimes a model comes out, and then we argue for three years about which thousand of those tokens mattered.",
            'Census', 'Data-Census-Pedant'),
        'big_picture': 'Pretraining corpora and evaluation benchmarks are the two halves of an LLM\'s empirical identity. This section maps the corpora that frontier labs use (RedPajama, FineWeb, Dolma, The Stack) and the benchmarks that gate every release (MMLU, MMLU-Pro, GSM8K, HumanEval, MATH, HellaSwag, ARC, BBH, IFEval, AGIEval), so when an LLM paper claims state-of-the-art you know what that benchmark measures and where its known contamination leaks live.',
        'prereq': 'This section assumes the pretraining objective from <a href="../module-06-pretraining-scaling-laws/section-6.2.html">Section 6.2</a>, the deduplication-and-quality-filter pipeline from <a href="../module-06-pretraining-scaling-laws/section-6.4.html">Section 6.4</a>, and the eval-leakage discussion from <a href="../../part-9-llm-evaluation-observability/module-42-evaluation-foundations/section-42.4.html">Section 42.4</a>.',
    },
    'part-2-understanding-llms/module-10-interpretability/section-10.8.html': {
        'epigraph': ep(
            "A quantized model is still the same model, just one that learned to mumble. The trick is making sure it mumbles the right answer.",
            'Quant', 'Bit-Whisperer'),
        'big_picture': 'This section is a practical companion to the quantization theory earlier in Chapter 10. It tells you which open-weights LLMs (Llama 3, Mistral, Qwen, Gemma, Phi, DeepSeek, Mixtral, Falcon, Yi, Command R) actually run on which hardware in 2026, at which quantization level, and with which expected quality hit. This is the model-zoo lookup you reach for when an agent product needs to pick between API and local deployment.',
        'prereq': 'This section assumes the quantization formats covered in <a href="section-10.1.html">Section 10.1</a> through <a href="section-10.3.html">Section 10.3</a>, the inference-stack platforms in <a href="section-10.5.html">Section 10.5</a>, and the open-versus-closed licensing landscape from <a href="../../part-3-working-with-llms/module-11-llm-apis/section-11.1.html">Section 11.1</a>.',
    },
    'part-2-understanding-llms/module-10-interpretability/section-10.9.html': {
        'epigraph': ep(
            "The papers that matter this quarter are not yet on arXiv. Half are on X, half are on Discord, and a third (the math is fuzzy here) are still in someone's notebook.",
            'Frontier', 'Pre-Print-Wanderer'),
        'big_picture': 'Part II\'s external-reading list is centrally about three things: keeping current with the frontier model releases, internalizing the canonical pretraining and inference papers, and finding the working LLM-research community (Discords, mailing lists, conferences) where the actual debugging happens. This section is the curated map of where to look when the textbook ends and the field continues moving.',
        'prereq': 'This section is the end-of-part reading list and assumes you have worked through the rest of Part II (modules 6 through 10). No new technical prerequisites; some sources presuppose comfort with transformer mechanics, scaling laws, and quantization formats from earlier sections.',
    },

    # ==================================================================
    # Module 14 (Tools-of-the-trade for Part III: 14.1-14.5)
    # ==================================================================
    'part-3-working-with-llms/module-14-tools-of-the-trade/section-14.1.html': {
        'epigraph': ep(
            "An API key is a six-month commitment to a vendor's roadmap. Choose the vendor, not the model.",
            'Compass', 'Vendor-Locked-In-But-Honest'),
        'big_picture': '"Platform" in Part III means something different from Parts I and II: in those parts the platform was a GPU cluster or an inference server, but here it is the LLM-as-a-service vendor whose API your agent code lives against (OpenAI, Anthropic, Google, Mistral, Cohere, Together, Groq, Replicate, Fireworks, Bedrock, Vertex). This section maps that vendor shelf and tells you when each platform earns its monthly invoice.',
        'prereq': 'This section assumes you have built simple LLM API calls from <a href="../module-11-llm-apis/section-11.1.html">Section 11.1</a>, understand auth and retry patterns from <a href="../module-11-llm-apis/section-11.4.html">Section 11.4</a>, and have a working mental model of the closed-versus-open split from <a href="../../part-2-understanding-llms/module-10-interpretability/section-10.5.html">Section 10.5</a>.',
    },
    'part-3-working-with-llms/module-14-tools-of-the-trade/section-14.2.html': {
        'epigraph': ep(
            "LangChain was a strange thing. Then LlamaIndex was a strange thing. Now they are both stable, and we have new strange things, which is the field working as intended.",
            'Pip', 'Framework-Archeologist'),
        'prereq': 'This section assumes the LLM API basics from <a href="../module-11-llm-apis/section-11.1.html">Section 11.1</a>, the prompt-engineering vocabulary from <a href="../module-15-prompt-engineering/section-15.1.html">Section 15.1</a>, and at least one finished tool-use example from <a href="../../part-6-llm-agents/module-26-agent-foundations/section-26.3.html">Section 26.3</a>. Reading 14.1 first gives you the vendor map these frameworks compose over.',
    },
    'part-3-working-with-llms/module-14-tools-of-the-trade/section-14.3.html': {
        'epigraph': ep(
            "The benchmark is the prompt is the curriculum is the evaluation. Pick a dataset and you have picked a worldview.",
            'Census', 'Benchmark-Genealogist'),
        'big_picture': 'Part III\'s dataset layer differs from Part II\'s: instead of pretraining corpora at trillion-token scale, you care about instruction-tuning sets (Alpaca, ShareGPT, OpenAssistant, UltraChat), preference data (HH-RLHF, UltraFeedback, PRM800K), and the evaluation benchmarks that govern your prompt and your agent (MT-Bench, AlpacaEval, Arena-Hard, IFEval). This section catalogs them and tells you which to use when.',
        'prereq': 'This section assumes the instruction-tuning recipes from <a href="../module-08-instruction-tuning-rlhf/section-8.1.html">Section 8.1</a>, the LLM-as-judge methodology from <a href="../../part-9-llm-evaluation-observability/module-46-llm-as-judge-automated-evaluation/section-46.1.html">Section 46.1</a>, and basic familiarity with HuggingFace Datasets from <a href="../module-12-llm-libraries-frameworks/section-12.4.html">Section 12.4</a>.',
    },
    'part-3-working-with-llms/module-14-tools-of-the-trade/section-14.4.html': {
        'epigraph': ep(
            "We split the world into closed APIs, open weights, and the thing you wrote last weekend on Modal. Each tier solves one problem and creates three.",
            'Frontier', 'Tier-Aware'),
        'big_picture': 'The LLMs you call in Part III split into three tiers by access mode: closed APIs (GPT, Claude, Gemini, the frontier you rent), open weights (Llama, Mistral, Qwen, DeepSeek, the foundation you can host), and customised checkpoints (your fine-tune, your distillation, your LoRA on top of a base). This section tells you which tier earns which call inside an agent or RAG system.',
        'prereq': 'This section assumes the frontier-model lineage from <a href="../module-11-llm-apis/section-11.1.html">Section 11.1</a> through <a href="../module-11-llm-apis/section-11.3.html">Section 11.3</a>, the open-weights model zoo from <a href="../../part-2-understanding-llms/module-10-interpretability/section-10.8.html">Section 10.8</a>, and the fine-tuning recipes from <a href="../module-13-llm-customization/section-13.1.html">Section 13.1</a>.',
    },
    'part-3-working-with-llms/module-14-tools-of-the-trade/section-14.5.html': {
        'epigraph': ep(
            "The vendor documentation is the canonical source. The Discord is where it actually gets debugged. Plan accordingly.",
            'Sage', 'Documentation-Pragmatist'),
        'big_picture': 'Part III\'s external resources split between provider documentation (canonical for API behavior, version-stable), and the community venues (Anthropic Discord, OpenAI forum, r/LocalLLaMA, LangChain Discord) where the half-documented LLM agent gotchas actually surface. This section is the curated map you keep open in a tab next to your API console.',
        'prereq': 'This is an end-of-part reading list and assumes familiarity with the Part III modules on APIs (Chapter 11), libraries (Chapter 12), customization (Chapter 13), and tooling (Chapter 14). No new technical prerequisites.',
    },

    # ==================================================================
    # Module 20 (Audio/Music/Video) -- prereq-only
    # ==================================================================
    'part-5-multimodal-llms/module-20-audio-music-generation/section-20.1.html': {
        'prereq': 'This section assumes the transformer mechanics from <a href="../../part-1-llm-building-blocks/module-04-transformer-architecture-self-attention/section-4.1.html">Section 4.1</a>, the tokenization and vocabulary discussion from <a href="../../part-1-llm-building-blocks/module-02-tokenization/section-2.1.html">Section 2.1</a>, and the autoregressive next-token loss from <a href="../../part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.2.html">Section 6.2</a>. A brief detour through diffusion-model basics (the image variant covered in <a href="../module-19-multimodal-foundations/section-19.6.html">Section 19.6</a>) helps with the flow-matching half of the section.',
    },
    'part-5-multimodal-llms/module-20-audio-music-generation/section-20.2.html': {
        'prereq': 'This section assumes the codec-LM and flow-matching TTS pipelines from <a href="section-20.1.html">Section 20.1</a>, the speaker-embedding intuition from <a href="../module-19-multimodal-foundations/section-19.2.html">Section 19.2</a>, and the deepfake-detection background from <a href="../../part-11-llm-ethics-trust-governance/module-54-watermarking-provenance/section-54.4.html">Section 54.4</a>.',
    },
    'part-5-multimodal-llms/module-20-audio-music-generation/section-20.3.html': {
        'prereq': 'This section assumes the audio-codec tokenization from <a href="section-20.1.html">Section 20.1</a>, the transformer fundamentals from <a href="../../part-1-llm-building-blocks/module-04-transformer-architecture-self-attention/section-4.1.html">Section 4.1</a>, and an understanding of latent diffusion from <a href="../module-19-multimodal-foundations/section-19.6.html">Section 19.6</a>.',
    },
    'part-5-multimodal-llms/module-20-audio-music-generation/section-20.4.html': {
        'prereq': 'This section assumes the music-generation foundations from <a href="section-20.3.html">Section 20.3</a>, the source-separation and audio-codec topics in <a href="section-20.1.html">Section 20.1</a>, and the diffusion-inpainting intuition from <a href="../module-19-multimodal-foundations/section-19.6.html">Section 19.6</a>.',
    },
    'part-5-multimodal-llms/module-20-audio-music-generation/section-20.5.html': {
        'prereq': 'This section assumes the sequence-to-sequence transformer architecture from <a href="../../part-1-llm-building-blocks/module-04-transformer-architecture-self-attention/section-4.4.html">Section 4.4</a> and the conditional-LM intuition from <a href="../../part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.2.html">Section 6.2</a>. The TTS pipelines in <a href="section-20.1.html">Section 20.1</a> are the symmetric inverse problem worth comparing against.',
    },
    'part-5-multimodal-llms/module-20-audio-music-generation/section-20.6.html': {
        'prereq': 'This section assumes the image-DiT architecture from <a href="../module-19-multimodal-foundations/section-19.7.html">Section 19.7</a>, the attention mechanics from <a href="../../part-1-llm-building-blocks/module-04-transformer-architecture-self-attention/section-4.2.html">Section 4.2</a>, and the diffusion training objective from <a href="../module-19-multimodal-foundations/section-19.6.html">Section 19.6</a>.',
    },
    'part-5-multimodal-llms/module-20-audio-music-generation/section-20.7.html': {
        'prereq': 'This section assumes the video DiT architecture from <a href="section-20.6.html">Section 20.6</a> and the platform-selection patterns from <a href="../module-25-tools-of-the-trade/section-25.1.html">Section 25.1</a>. Familiarity with the closed-versus-open trade-off from <a href="../../part-2-understanding-llms/module-10-interpretability/section-10.5.html">Section 10.5</a> helps you read the capability matrix.',
    },
    'part-5-multimodal-llms/module-20-audio-music-generation/section-20.8.html': {
        'prereq': 'This section assumes the video DiT internals from <a href="section-20.6.html">Section 20.6</a>, the ControlNet image-conditioning pattern from <a href="../module-19-multimodal-foundations/section-19.9.html">Section 19.9</a>, and the camera-pose vocabulary from <a href="../module-23-3d-generation-neural-scenes/section-23.1.html">Section 23.1</a>.',
    },
    'part-5-multimodal-llms/module-20-audio-music-generation/section-20.9.html': {
        'prereq': 'This section assumes the video generation models from <a href="section-20.7.html">Section 20.7</a>, the inpainting and editing patterns from <a href="../module-19-multimodal-foundations/section-19.9.html">Section 19.9</a>, and basic familiarity with optical flow and frame interpolation networks.',
    },
    'part-5-multimodal-llms/module-20-audio-music-generation/section-20.10.html': {
        'prereq': 'This section assumes the leading video models from <a href="section-20.7.html">Section 20.7</a>, the camera and motion control techniques from <a href="section-20.8.html">Section 20.8</a>, and the multimodal LLM agent patterns from <a href="../../part-6-llm-agents/module-26-agent-foundations/section-26.1.html">Section 26.1</a>.',
    },

    # ==================================================================
    # Module 21 (Document Understanding/OCR)
    # ==================================================================
    'part-5-multimodal-llms/module-21-document-understanding-ocr/section-21.1.html': {
        'prereq': 'This section assumes the encoder-decoder transformer architecture from <a href="../../part-1-llm-building-blocks/module-04-transformer-architecture-self-attention/section-4.4.html">Section 4.4</a>, the Vision Transformer (ViT) patch-embedding mechanics from <a href="../module-22-vision-language-models/section-22.1.html">Section 22.1</a>, and the autoregressive decoding loop from <a href="../../part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.2.html">Section 6.2</a>.',
    },

    # ==================================================================
    # Module 22 (Vision-Language Models)
    # ==================================================================
    'part-5-multimodal-llms/module-22-vision-language-models/section-22.1.html': {
        'prereq': 'This section assumes the transformer mechanics from <a href="../../part-1-llm-building-blocks/module-04-transformer-architecture-self-attention/section-4.1.html">Section 4.1</a>, the tokenization and embedding intuition from <a href="../../part-1-llm-building-blocks/module-02-tokenization/section-2.1.html">Section 2.1</a>, and the basic CNN-versus-attention contrast from <a href="../../part-1-llm-building-blocks/module-00-ml-pytorch-foundations/section-0.4.html">Section 0.4</a>.',
    },
    'part-5-multimodal-llms/module-22-vision-language-models/section-22.7.html': {
        'prereq': 'This section assumes the VLM architecture from <a href="section-22.1.html">Section 22.1</a> through <a href="section-22.4.html">Section 22.4</a>, and the cross-attention mechanics from <a href="../../part-1-llm-building-blocks/module-04-transformer-architecture-self-attention/section-4.3.html">Section 4.3</a>.',
    },
    'part-5-multimodal-llms/module-22-vision-language-models/section-22.8.html': {
        'prereq': 'This section assumes the unified vision-language pipelines from <a href="section-22.1.html">Section 22.1</a> through <a href="section-22.6.html">Section 22.6</a>, the audio-codec tokenization from <a href="../module-20-audio-music-generation/section-20.1.html">Section 20.1</a>, and the diffusion-model basics from <a href="../module-19-multimodal-foundations/section-19.6.html">Section 19.6</a>.',
    },
    'part-5-multimodal-llms/module-22-vision-language-models/section-22.9.html': {
        'prereq': 'This section assumes the VLM and any-to-any architectures from <a href="section-22.1.html">Section 22.1</a> through <a href="section-22.8.html">Section 22.8</a>, the speech and audio pipelines from <a href="../module-20-audio-music-generation/section-20.1.html">Section 20.1</a>, and the frontier-API platform shelf from <a href="../../part-3-working-with-llms/module-14-tools-of-the-trade/section-14.1.html">Section 14.1</a>.',
    },

    # ==================================================================
    # Module 23 (3D Generation, Neural Scenes)
    # ==================================================================
    'part-5-multimodal-llms/module-23-3d-generation-neural-scenes/section-23.2.html': {
        'prereq': 'This section assumes the static 3D Gaussian Splatting fundamentals from <a href="section-23.1.html">Section 23.1</a>, the diffusion-model basics from <a href="../module-19-multimodal-foundations/section-19.6.html">Section 19.6</a>, and basic familiarity with camera intrinsics and extrinsics.',
    },
    'part-5-multimodal-llms/module-23-3d-generation-neural-scenes/section-23.4.html': {
        'prereq': 'This section assumes the diffusion-model fundamentals from <a href="../module-19-multimodal-foundations/section-19.6.html">Section 19.6</a>, the latent-space autoencoder intuition from <a href="../module-19-multimodal-foundations/section-19.5.html">Section 19.5</a>, and the 3DGS representations from <a href="section-23.1.html">Section 23.1</a>.',
    },
    'part-5-multimodal-llms/module-23-3d-generation-neural-scenes/section-23.5.html': {
        'prereq': 'This section assumes the 3D scene representations from <a href="section-23.1.html">Section 23.1</a>, the inverse-rendering and BRDF basics from <a href="section-23.3.html">Section 23.3</a>, and the language-grounding patterns from VLMs in <a href="../module-22-vision-language-models/section-22.4.html">Section 22.4</a>.',
    },

    # ==================================================================
    # Module 24 (VLA Models)
    # ==================================================================
    'part-5-multimodal-llms/module-24-vla-models/section-24.1.html': {
        'epigraph': ep(
            "I learned to read a wrist camera in three weeks. Learning what to do with a wrist camera took the other 47.",
            'Sage', 'Embodied-and-Confused'),
        'prereq': 'This section assumes the next-token factorization from <a href="../../part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.2.html">Section 6.2</a>, the multimodal token-fusion patterns from <a href="../module-22-vision-language-models/section-22.7.html">Section 22.7</a>, and a working intuition for KV-cache mechanics from <a href="../../part-2-understanding-llms/module-09-inference-deployment/section-9.3.html">Section 9.3</a>.',
    },
    'part-5-multimodal-llms/module-24-vla-models/section-24.2.html': {
        'epigraph': ep(
            "Open the weights, read the tokenizer, run the policy. That is the whole pedagogy in one sentence.",
            'Pip', 'Reference-Implementation-Reader'),
        'prereq': 'This section assumes the VLA equation and action tokenization from <a href="section-24.1.html">Section 24.1</a>, the VLM backbone fundamentals from <a href="../module-22-vision-language-models/section-22.1.html">Section 22.1</a>, and the LoRA fine-tuning recipe from <a href="../../part-3-working-with-llms/module-13-llm-customization/section-13.3.html">Section 13.3</a>.',
    },
    'part-5-multimodal-llms/module-24-vla-models/section-24.3.html': {
        'epigraph': ep(
            "Flow matching for robots: the diffusion paper from 2022 finally found its physical body in 2025.",
            'Synth', 'Flow-Matched'),
        'prereq': 'This section assumes the VLA equation from <a href="section-24.1.html">Section 24.1</a>, the flow-matching objective from <a href="../module-19-multimodal-foundations/section-19.6.html">Section 19.6</a>, and the action-tokenization vocabulary from the same chapter\'s opening section.',
    },
    'part-5-multimodal-llms/module-24-vla-models/section-24.4.html': {
        'epigraph': ep(
            "We mixed 22 robot datasets in one tokenizer, and somewhere a control theorist quietly closed their laptop.",
            'Scale', 'Data-Mixed-And-Proud'),
        'prereq': 'This section assumes the VLA architecture from <a href="section-24.1.html">Section 24.1</a> and the scaling-law intuitions from <a href="../../part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.3.html">Section 6.3</a>. Familiarity with cross-domain transfer from <a href="../../part-3-working-with-llms/module-13-llm-customization/section-13.4.html">Section 13.4</a> helps with the cross-embodiment discussion.',
    },
    'part-5-multimodal-llms/module-24-vla-models/section-24.5.html': {
        'epigraph': ep(
            "Six VLAs, eight metrics, one comparison table. Pick a column and you have picked a vendor.",
            'Compass', 'Capability-Matrix-Operator'),
        'prereq': 'This section assumes the architectures in <a href="section-24.1.html">Section 24.1</a> through <a href="section-24.4.html">Section 24.4</a> and the licensing landscape from <a href="../../part-2-understanding-llms/module-10-interpretability/section-10.5.html">Section 10.5</a>.',
    },
    'part-5-multimodal-llms/module-24-vla-models/section-24.6.html': {
        'epigraph': ep(
            "I can pick up a block. I can pour a cup of water. I cannot tie my shoelaces, and 2026 still owes me an answer.",
            'Hallux', 'Honestly-Limited'),
        'prereq': 'This section assumes the VLA mechanics from <a href="section-24.1.html">Section 24.1</a> and the safety considerations introduced in <a href="../../part-10-trustworthy-llms/module-49-llm-safety-alignment/section-49.1.html">Section 49.1</a>.',
    },
    'part-5-multimodal-llms/module-24-vla-models/section-24.7.html': {
        'epigraph': ep(
            "Say what you want, and a value function will tell you whether you can. The robot does the rest.",
            'Reward', 'Value-Function-Whisperer'),
        'prereq': 'This section assumes the LLM-as-planner pattern from <a href="../../part-6-llm-agents/module-26-agent-foundations/section-26.4.html">Section 26.4</a>, the affordance vocabulary from classical robotics (covered briefly in the intro to this chapter), and the policy-gradient value-function basics from <a href="../../part-1-llm-building-blocks/module-00-ml-pytorch-foundations/section-0.4.html">Section 0.4</a>.',
    },
    'part-5-multimodal-llms/module-24-vla-models/section-24.8.html': {
        'epigraph': ep(
            "When the planner is the programmer, every robot is a chat-completion away from a new behavior.",
            'Tensor', 'Compile-And-Run'),
        'prereq': 'This section assumes the LLM-as-planner pattern from <a href="section-24.7.html">Section 24.7</a>, the tool-use and code-generation patterns from <a href="../../part-6-llm-agents/module-26-agent-foundations/section-26.3.html">Section 26.3</a>, and basic Python control-flow fluency.',
    },
    'part-5-multimodal-llms/module-24-vla-models/section-24.9.html': {
        'epigraph': ep(
            "The map is the cost field, and the cost field is the language. Move accordingly.",
            'Compass', 'Voxel-Grid-Native'),
        'prereq': 'This section assumes the LLM-grounded planning pattern from <a href="section-24.7.html">Section 24.7</a> and <a href="section-24.8.html">Section 24.8</a>, plus the basic 3D scene-representation vocabulary from <a href="../module-23-3d-generation-neural-scenes/section-23.1.html">Section 23.1</a>.',
    },
    'part-5-multimodal-llms/module-24-vla-models/section-24.10.html': {
        'epigraph': ep(
            "One LLM, ten robots, and an open question about whose latency budget is whose.",
            'Sched', 'Coordinator-In-Chief'),
        'prereq': 'This section assumes the single-robot VLA patterns from <a href="section-24.1.html">Section 24.1</a> through <a href="section-24.5.html">Section 24.5</a> and the multi-agent coordination vocabulary from <a href="../../part-6-llm-agents/module-29-multi-agent-systems/section-29.1.html">Section 29.1</a>.',
    },
    'part-5-multimodal-llms/module-24-vla-models/section-24.11.html': {
        'epigraph': ep(
            "ROS 2 is the cable that connects 'think' to 'move'. The cable is held together by topic names and good intentions.",
            'Pip', 'Topic-Subscriber'),
        'prereq': 'This section assumes Python familiarity, the LLM-tool-use pattern from <a href="../../part-6-llm-agents/module-26-agent-foundations/section-26.3.html">Section 26.3</a>, and the single-robot VLA architecture from <a href="section-24.1.html">Section 24.1</a>. Familiarity with publish/subscribe messaging is useful but not strictly required.',
    },
    'part-5-multimodal-llms/module-24-vla-models/section-24.12.html': {
        'epigraph': ep(
            "Four planners, four trade-offs, one decision rubric. Pick the planner that matches your robot, not the paper.",
            'Compass', 'Trade-Off-Matrix-Native'),
        'prereq': 'This section assumes the planner architectures from <a href="section-24.7.html">Section 24.7</a> through <a href="section-24.11.html">Section 24.11</a> and the comparison-matrix methodology from <a href="../../part-9-llm-evaluation-observability/module-42-evaluation-foundations/section-42.1.html">Section 42.1</a>.',
    },
    'part-5-multimodal-llms/module-24-vla-models/section-24.13.html': {
        'epigraph': ep(
            "Simulation said yes. Reality said maybe. The gap between yes and maybe is where the PhD thesis lives.",
            'Eval', 'Sim2Real-Pessimist'),
        'prereq': 'This section assumes the VLA architectures from <a href="section-24.1.html">Section 24.1</a> through <a href="section-24.4.html">Section 24.4</a> and the evaluation methodology for embodied agents from <a href="../../part-9-llm-evaluation-observability/module-42-evaluation-foundations/section-42.1.html">Section 42.1</a>.',
    },

    # ==================================================================
    # Module 25 (Tools-of-the-trade for Part V)
    # ==================================================================
    'part-5-multimodal-llms/module-25-tools-of-the-trade/section-25.1.html': {
        'epigraph': ep(
            "Image API: dollars per call. Video API: dollars per second. Audio API: dollars per minute. Welcome to multimodal billing.",
            'Quant', 'Per-Token-Counter'),
        'big_picture': 'Multimodal platforms split the same way the text-LLM platforms in Section 14.1 do: closed APIs at the frontier, open weights behind them. This section maps the 2026 platform shelf (Midjourney, OpenAI Images, Imagen, FLUX, SD, Sora, Veo, Runway, Kling, ElevenLabs, Suno, Udio, Cartesia) and tells you which platform earns each call in an LLM-driven multimodal agent product.',
        'prereq': 'This section assumes the text-LLM API patterns from <a href="../../part-3-working-with-llms/module-11-llm-apis/section-11.1.html">Section 11.1</a> and the closed-versus-open trade-off from <a href="../../part-2-understanding-llms/module-10-interpretability/section-10.5.html">Section 10.5</a>. Familiarity with the multimodal architectures in <a href="../module-22-vision-language-models/section-22.1.html">Section 22.1</a> and <a href="../module-20-audio-music-generation/section-20.1.html">Section 20.1</a> helps you read pricing.',
    },
    'part-5-multimodal-llms/module-25-tools-of-the-trade/section-25.2.html': {
        'epigraph': ep(
            "HuggingFace diffusers is the multimodal analog of transformers. They both started as research demos, and they both end as production infrastructure.",
            'Pip', 'Diffusers-Native'),
        'big_picture': 'Multimodal libraries (diffusers, transformers, mmaction2, ComfyUI, accelerate, peft) sit between raw GPU code and your LLM agent pipeline. This section catalogs the ones that have consolidated as 2026 standard tooling and tells you when each library earns a dependency line.',
        'prereq': 'This section assumes the HuggingFace transformers patterns from <a href="../../part-3-working-with-llms/module-12-llm-libraries-frameworks/section-12.1.html">Section 12.1</a>, the multimodal architectures from <a href="../module-22-vision-language-models/section-22.1.html">Section 22.1</a>, and the diffusion-model fundamentals from <a href="../module-19-multimodal-foundations/section-19.6.html">Section 19.6</a>.',
    },
    'part-5-multimodal-llms/module-25-tools-of-the-trade/section-25.3.html': {
        'epigraph': ep(
            "LAION came first. Then everyone learned to filter LAION. Now we filter the filter, and the cycle continues.",
            'Census', 'Filter-Genealogist'),
        'big_picture': 'The multimodal-dataset shelf mirrors the text-pretraining-dataset shape from Section 7.4: a noisy web-scale corpus for pretraining (LAION, COYO, WebVid, CC-12M) and a curated instruction or eval set for downstream work (MMVet, MMBench, VBench, MS-COCO). This section maps both halves and tells you which dataset is safe to mention out loud in 2026.',
        'prereq': 'This section assumes the text-pretraining corpus discussion from <a href="../../part-2-understanding-llms/module-10-interpretability/section-10.7.html">Section 10.7</a>, the multimodal-architecture vocabulary from <a href="../module-22-vision-language-models/section-22.1.html">Section 22.1</a>, and the data-licensing background from <a href="../../part-11-llm-ethics-trust-governance/module-54-watermarking-provenance/section-54.1.html">Section 54.1</a>.',
    },
    'part-5-multimodal-llms/module-25-tools-of-the-trade/section-25.4.html': {
        'epigraph': ep(
            "The model zoo grows three rows a quarter. The reading list grows one row a year. Plan your career accordingly.",
            'Frontier', 'Model-Zoo-Wrangler'),
        'big_picture': 'The shape of this section mirrors the text-LLM model zoo in Module 14 and Section 12.1, but with image, audio, video, and VLA models added in. It catalogs the open-weights checkpoints (FLUX, SD3, MusicGen, Whisper, OpenVLA, Qwen2-VL, Llava-OneVision) and the closed-API equivalents that your agent or RAG pipeline calls in production.',
        'prereq': 'This section assumes the multimodal architectures across Chapters 19 through 24 and the open-versus-closed licensing landscape from <a href="../../part-2-understanding-llms/module-10-interpretability/section-10.5.html">Section 10.5</a>.',
    },
    'part-5-multimodal-llms/module-25-tools-of-the-trade/section-25.5.html': {
        'epigraph': ep(
            "Papers are written by labs. Engineering is written on Discord. The textbook lives in the middle and tries not to fall.",
            'Sage', 'Mid-Stack-Reader'),
        'big_picture': 'Like the text-LLM reading list in Section 14.5, the multimodal-stack reading list splits across foundational papers (the canonical citations every multimodal LLM engineer should know), live venues (CVPR, NeurIPS, ICCV, ICLR, ICML), and community channels (Discord, Twitter/X, Reddit) where the latest model releases get debugged in public.',
        'prereq': 'This is an end-of-part reading list and assumes familiarity with Part V (Chapters 19 through 25). No new technical prerequisites.',
    },

    # ==================================================================
    # Module 33 (Cross-modal Reasoning RAG)
    # ==================================================================
    'part-7-retrieval-information-extraction-with-llms/module-33-cross-modal-reasoning-rag/section-33.2.html': {
        'prereq': 'This section assumes the unimodal RAG architecture from <a href="../module-31-rag-retrieval-augmented-generation/section-31.1.html">Section 31.1</a>, the vector-database patterns from <a href="../module-32-vector-databases-retrieval/section-32.1.html">Section 32.1</a>, and the multimodal-embedding fundamentals from <a href="../../part-5-multimodal-llms/module-19-multimodal-foundations/section-19.2.html">Section 19.2</a>.',
    },
    'part-7-retrieval-information-extraction-with-llms/module-33-cross-modal-reasoning-rag/section-33.3.html': {
        'prereq': 'This section assumes the multimodal RAG patterns from <a href="section-33.2.html">Section 33.2</a>, the reasoning patterns (chain-of-thought, deliberation) from <a href="../../part-6-llm-agents/module-26-agent-foundations/section-26.2.html">Section 26.2</a>, and basic familiarity with the cost-latency-quality trade-off matrix from <a href="../../part-3-working-with-llms/module-14-tools-of-the-trade/section-14.1.html">Section 14.1</a>.',
    },
    'part-7-retrieval-information-extraction-with-llms/module-33-cross-modal-reasoning-rag/section-33.4.html': {
        'prereq': 'This section assumes the multimodal RAG patterns from <a href="section-33.2.html">Section 33.2</a> and <a href="section-33.3.html">Section 33.3</a>, the production-deployment recipes from <a href="../module-31-rag-retrieval-augmented-generation/section-31.7.html">Section 31.7</a>, and the LLM observability and tracing tools from <a href="../../part-9-llm-evaluation-observability/module-44-observability-tracing/section-44.1.html">Section 44.1</a>.',
    },

    # ==================================================================
    # Module 34 (Structured IE / NER)
    # ==================================================================
    'part-7-retrieval-information-extraction-with-llms/module-34-structured-information-extraction-ner/section-34.1.html': {
        'epigraph': ep(
            "Free text in, structured rows out. Forty years of NLP can be summarized in eight words and a column count.",
            'Token', 'Schema-Stable-Outputter'),
        'prereq': 'This section assumes basic familiarity with NLP tasks from <a href="../../part-1-llm-building-blocks/module-01-foundations-nlp-text-representation/section-1.1.html">Section 1.1</a>, the LLM prompting vocabulary from <a href="../../part-3-working-with-llms/module-15-prompt-engineering/section-15.1.html">Section 15.1</a>, and an intuition for the structured-output patterns introduced in <a href="../../part-3-working-with-llms/module-15-prompt-engineering/section-15.6.html">Section 15.6</a>.',
    },
    'part-7-retrieval-information-extraction-with-llms/module-34-structured-information-extraction-ner/section-34.2.html': {
        'prereq': 'This section assumes the information-extraction landscape from <a href="section-34.1.html">Section 34.1</a>, the basic token-classification vocabulary from <a href="../../part-1-llm-building-blocks/module-01-foundations-nlp-text-representation/section-1.3.html">Section 1.3</a>, and familiarity with the spaCy and Hugging Face pipeline interfaces from <a href="../../part-3-working-with-llms/module-12-llm-libraries-frameworks/section-12.1.html">Section 12.1</a>.',
    },
    'part-7-retrieval-information-extraction-with-llms/module-34-structured-information-extraction-ner/section-34.3.html': {
        'prereq': 'This section assumes the classical IE methods from <a href="section-34.2.html">Section 34.2</a>, the LLM tool-use and structured-output patterns from <a href="../../part-3-working-with-llms/module-15-prompt-engineering/section-15.6.html">Section 15.6</a>, and the function-calling vocabulary from <a href="../../part-6-llm-agents/module-26-agent-foundations/section-26.3.html">Section 26.3</a>.',
    },
    'part-7-retrieval-information-extraction-with-llms/module-34-structured-information-extraction-ner/section-34.4.html': {
        'big_picture': 'Production IE systems sit at the unglamorous core of every LLM-powered RAG, agentic-search, and document-understanding product. This section codifies the deployment patterns (grounding with provenance, deduplication, graceful degradation, schema versioning) that separate a demo from a system that survives Monday morning.',
        'prereq': 'This section assumes the hybrid IE architectures from <a href="section-34.3.html">Section 34.3</a>, the production RAG patterns from <a href="../module-31-rag-retrieval-augmented-generation/section-31.7.html">Section 31.7</a>, and the LLM observability fundamentals from <a href="../../part-9-llm-evaluation-observability/module-44-observability-tracing/section-44.1.html">Section 44.1</a>.',
    },
    'part-7-retrieval-information-extraction-with-llms/module-34-structured-information-extraction-ner/section-34.5.html': {
        'big_picture': 'Coreference resolution is the silent infrastructure of every cross-document RAG and structured-IE LLM pipeline: until you know that "Dr. Smith", "she", and "the cardiologist" refer to the same person, your downstream joins, deduplication, and entity tables are quietly wrong. This section covers the modern transformer-based coreference systems and how they slot into production document pipelines.',
        'prereq': 'This section assumes the IE architectures from <a href="section-34.1.html">Section 34.1</a> through <a href="section-34.4.html">Section 34.4</a>, the encoder-only transformer architecture from <a href="../../part-1-llm-building-blocks/module-04-transformer-architecture-self-attention/section-4.4.html">Section 4.4</a>, and the BERT-style pretraining objective from <a href="../../part-2-understanding-llms/module-05-encoder-models-bert/section-5.1.html">Section 5.1</a>.',
    },

    # ==================================================================
    # Module 36 (Retrieval Tools-of-the-trade)
    # ==================================================================
    'part-7-retrieval-information-extraction-with-llms/module-36-retrieval-tools/section-36.1.html': {
        'prereq': 'This section assumes the vector-search fundamentals from <a href="../module-32-vector-databases-retrieval/section-32.1.html">Section 32.1</a>, the RAG architecture from <a href="../module-31-rag-retrieval-augmented-generation/section-31.1.html">Section 31.1</a>, and the embedding-model vocabulary from <a href="../../part-1-llm-building-blocks/module-03-embeddings/section-3.1.html">Section 3.1</a>.',
    },
    'part-7-retrieval-information-extraction-with-llms/module-36-retrieval-tools/section-36.2.html': {
        'prereq': 'This section assumes the retrieval platforms from <a href="section-36.1.html">Section 36.1</a> and the basic RAG orchestration patterns from <a href="../module-31-rag-retrieval-augmented-generation/section-31.1.html">Section 31.1</a>.',
    },
    'part-7-retrieval-information-extraction-with-llms/module-36-retrieval-tools/section-36.3.html': {
        'prereq': 'This section assumes the retrieval evaluation methodology from <a href="../module-31-rag-retrieval-augmented-generation/section-31.5.html">Section 31.5</a>, the embedding-model fundamentals from <a href="../../part-1-llm-building-blocks/module-03-embeddings/section-3.1.html">Section 3.1</a>, and the LLM-as-judge methodology from <a href="../../part-9-llm-evaluation-observability/module-46-llm-as-judge-automated-evaluation/section-46.1.html">Section 46.1</a>.',
    },
    'part-7-retrieval-information-extraction-with-llms/module-36-retrieval-tools/section-36.4.html': {
        'prereq': 'This section assumes the embedding-model architectures from <a href="../../part-1-llm-building-blocks/module-03-embeddings/section-3.1.html">Section 3.1</a>, the open-versus-closed licensing landscape from <a href="../../part-2-understanding-llms/module-10-interpretability/section-10.5.html">Section 10.5</a>, and the multilingual considerations from <a href="../module-32-vector-databases-retrieval/section-32.3.html">Section 32.3</a>.',
    },
    'part-7-retrieval-information-extraction-with-llms/module-36-retrieval-tools/section-36.5.html': {
        'prereq': 'This is an end-of-chapter reading list and assumes familiarity with the retrieval modules in Part VII. No new technical prerequisites.',
    },

    # ==================================================================
    # Module 40 (Voice / Realtime Multimodal)
    # ==================================================================
    'part-8-conversational-ai-with-llms/module-40-voice-realtime-multimodal/section-40.3.html': {
        'prereq': 'This section assumes the speech-recognition and TTS pipelines from <a href="../../part-5-multimodal-llms/module-20-audio-music-generation/section-20.1.html">Section 20.1</a> and <a href="../../part-5-multimodal-llms/module-20-audio-music-generation/section-20.5.html">Section 20.5</a>, the frontier-API patterns from <a href="../../part-3-working-with-llms/module-14-tools-of-the-trade/section-14.1.html">Section 14.1</a>, and the streaming-API patterns from <a href="../../part-3-working-with-llms/module-11-llm-apis/section-11.4.html">Section 11.4</a>.',
    },
    'part-8-conversational-ai-with-llms/module-40-voice-realtime-multimodal/section-40.4.html': {
        'prereq': 'This section assumes the audio-codec tokenization from <a href="../../part-5-multimodal-llms/module-20-audio-music-generation/section-20.1.html">Section 20.1</a>, the LLM-inference cost mechanics from <a href="../../part-2-understanding-llms/module-09-inference-deployment/section-9.1.html">Section 9.1</a>, and the realtime-API platforms from <a href="section-40.3.html">Section 40.3</a>.',
    },
    'part-8-conversational-ai-with-llms/module-40-voice-realtime-multimodal/section-40.5.html': {
        'prereq': 'This section assumes the closed-API realtime architecture from <a href="section-40.3.html">Section 40.3</a>, the latency-budget vocabulary from <a href="section-40.4.html">Section 40.4</a>, and the open-weights model zoo for speech and audio from <a href="../../part-5-multimodal-llms/module-25-tools-of-the-trade/section-25.4.html">Section 25.4</a>.',
    },

    # ==================================================================
    # Module 41 (Conv AI Tools-of-the-trade)
    # ==================================================================
    'part-8-conversational-ai-with-llms/module-41-conv-ai-tools/section-41.1.html': {
        'prereq': 'This section assumes the LLM-API patterns from <a href="../../part-3-working-with-llms/module-14-tools-of-the-trade/section-14.1.html">Section 14.1</a>, the conversational-AI fundamentals from <a href="../module-37-conversational-ai-foundations/section-37.1.html">Section 37.1</a>, and the realtime-voice platforms from <a href="../module-40-voice-realtime-multimodal/section-40.3.html">Section 40.3</a>.',
    },
    'part-8-conversational-ai-with-llms/module-41-conv-ai-tools/section-41.2.html': {
        'prereq': 'This section assumes the conversational-AI platforms from <a href="section-41.1.html">Section 41.1</a> and the LLM agent framework vocabulary from <a href="../../part-3-working-with-llms/module-14-tools-of-the-trade/section-14.2.html">Section 14.2</a>.',
    },
    'part-8-conversational-ai-with-llms/module-41-conv-ai-tools/section-41.3.html': {
        'prereq': 'This section assumes the conversational-AI evaluation methodology from <a href="../module-39-conversation-quality-and-eval/section-39.1.html">Section 39.1</a> and the LLM-as-judge patterns from <a href="../../part-9-llm-evaluation-observability/module-46-llm-as-judge-automated-evaluation/section-46.1.html">Section 46.1</a>.',
    },
    'part-8-conversational-ai-with-llms/module-41-conv-ai-tools/section-41.4.html': {
        'prereq': 'This section assumes the LLM model zoo from <a href="../../part-3-working-with-llms/module-14-tools-of-the-trade/section-14.4.html">Section 14.4</a> and the realtime-voice models from <a href="../module-40-voice-realtime-multimodal/section-40.3.html">Section 40.3</a>.',
    },
    'part-8-conversational-ai-with-llms/module-41-conv-ai-tools/section-41.5.html': {
        'prereq': 'This is an end-of-chapter reading list and assumes familiarity with the conversational-AI modules in Part VIII.',
    },

    # ==================================================================
    # Module 42 (Evaluation Foundations: section 42.12 only)
    # ==================================================================
    'part-9-llm-evaluation-observability/module-42-evaluation-foundations/section-42.12.html': {
        'epigraph': ep(
            "BLEU, ROUGE, perplexity. The three letters that keep showing up at parties long after the host stopped inviting them.",
            'Eval', 'Metric-Reference-Holder'),
        'big_picture': 'Classical ML metrics (BLEU, ROUGE, perplexity, classification precision/recall/F1) still anchor the LLM and RAG evaluation toolkit even in the era of LLM-as-judge: they are the cheap, deterministic, reproducible numbers your monitoring dashboard exposes and your paper has to report. This page is the lookup reference you reach for when an evaluation harness asks for "BLEU-4" and you need to remember what that means.',
        'prereq': 'This section assumes the train/validation/test split discussion from <a href="../../part-1-llm-building-blocks/module-00-ml-pytorch-foundations/section-0.1.html">Section 0.1</a>, the LLM evaluation framework from <a href="section-42.1.html">Section 42.1</a>, and the language-model perplexity definition from <a href="../../part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.2.html">Section 6.2</a>.',
    },

    # ==================================================================
    # Module 46 (LLM-as-Judge: section 46.5)
    # ==================================================================
    'part-9-llm-evaluation-observability/module-46-llm-as-judge-automated-evaluation/section-46.5.html': {
        'prereq': 'This section assumes the LLM-as-judge methodology from <a href="section-46.1.html">Section 46.1</a> through <a href="section-46.4.html">Section 46.4</a>, the evaluation-set-design principles from <a href="../module-42-evaluation-foundations/section-42.1.html">Section 42.1</a>, and the LLM-API patterns from <a href="../../part-3-working-with-llms/module-11-llm-apis/section-11.1.html">Section 11.1</a>.',
    },

    # ==================================================================
    # Module 54 (Watermarking & Provenance: 54.1-54.5)
    # ==================================================================
    'part-11-llm-ethics-trust-governance/module-54-watermarking-provenance/section-54.1.html': {
        'epigraph': ep(
            "Once content can lie about where it came from, every screenshot becomes a metaphysics problem.",
            'Sentinel', 'Provenance-Custodian'),
        'prereq': 'This section assumes basic familiarity with LLM and multimodal generation (text, image, audio, video) from Parts II and V, plus the LLM-safety framing from <a href="../../part-10-trustworthy-llms/module-49-llm-safety-alignment/section-49.1.html">Section 49.1</a>.',
    },
    'part-11-llm-ethics-trust-governance/module-54-watermarking-provenance/section-54.2.html': {
        'epigraph': ep(
            "Mark every other token green and pray the editor does not paraphrase. This is the entire LLM-watermarking literature in one sentence.",
            'Token', 'Green-List-Veteran'),
        'prereq': 'This section assumes the LLM token-level sampling vocabulary from <a href="../../part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.6.html">Section 6.6</a>, the basic statistical-hypothesis-test mechanics, and the provenance framing from <a href="section-54.1.html">Section 54.1</a>.',
    },
    'part-11-llm-ethics-trust-governance/module-54-watermarking-provenance/section-54.3.html': {
        'epigraph': ep(
            "C2PA is what happens when you ask metadata to be load-bearing. The metadata mostly holds, until someone uploads to Twitter.",
            'Pixel', 'Manifest-Pessimist'),
        'prereq': 'This section assumes the image-generation pipelines from <a href="../../part-5-multimodal-llms/module-19-multimodal-foundations/section-19.6.html">Section 19.6</a>, the video-generation models from <a href="../../part-5-multimodal-llms/module-20-audio-music-generation/section-20.7.html">Section 20.7</a>, and the provenance framing from <a href="section-54.1.html">Section 54.1</a>.',
    },
    'part-11-llm-ethics-trust-governance/module-54-watermarking-provenance/section-54.4.html': {
        'epigraph': ep(
            "Every deepfake detector has a generation it cannot catch. That generation is always next quarter\'s model.",
            'Hallux', 'Cat-And-Mouse-Veteran'),
        'prereq': 'This section assumes the image and video generation pipelines from <a href="../../part-5-multimodal-llms/module-19-multimodal-foundations/section-19.6.html">Section 19.6</a> and <a href="../../part-5-multimodal-llms/module-20-audio-music-generation/section-20.7.html">Section 20.7</a>, and the binary-classifier-training basics from <a href="../../part-1-llm-building-blocks/module-00-ml-pytorch-foundations/section-0.1.html">Section 0.1</a>.',
    },
    'part-11-llm-ethics-trust-governance/module-54-watermarking-provenance/section-54.5.html': {
        'epigraph': ep(
            "Adversarial-removal papers keep arriving on the same day as new watermarking papers. The arXiv RSS feed is now a duel.",
            'Frontier', 'Adversarial-Honest'),
        'prereq': 'This section assumes the watermarking and provenance techniques from <a href="section-54.2.html">Section 54.2</a>, <a href="section-54.3.html">Section 54.3</a>, and the detection methods from <a href="section-54.4.html">Section 54.4</a>.',
    },

    # ==================================================================
    # Module 54b (Transparency: 54.6-54.10)
    # ==================================================================
    'part-11-llm-ethics-trust-governance/module-54b-transparency-and-disclosure/section-54.6.html': {
        'epigraph': ep(
            "A model card is the model\'s passport. Without it, an LLM crosses every border, but no procurement officer signs off.",
            'Compass', 'Procurement-Liaison'),
        'prereq': 'This section assumes the LLM-customization lifecycle from <a href="../../part-3-working-with-llms/module-13-llm-customization/section-13.1.html">Section 13.1</a>, the evaluation-set methodology from <a href="../../part-9-llm-evaluation-observability/module-42-evaluation-foundations/section-42.1.html">Section 42.1</a>, and the responsible-AI framing from <a href="../module-50-bias-fairness/section-50.1.html">Section 50.1</a>.',
    },
    'part-11-llm-ethics-trust-governance/module-54b-transparency-and-disclosure/section-54.7.html': {
        'epigraph': ep(
            "A datasheet is what your dataset wears to the interview. The interviewer is the GDPR auditor.",
            'Census', 'Datasheet-Native'),
        'prereq': 'This section assumes the pretraining-corpus discussion from <a href="../../part-2-understanding-llms/module-10-interpretability/section-10.7.html">Section 10.7</a>, the data-licensing vocabulary from <a href="section-54.1.html">Section 54.1</a>, and the model-card pattern from <a href="section-54.6.html">Section 54.6</a>.',
    },
    'part-11-llm-ethics-trust-governance/module-54b-transparency-and-disclosure/section-54.8.html': {
        'epigraph': ep(
            "A system card extends the model card with the parts of the LLM stack that ship to humans: the safety filters, the prompts, the refusal logic.",
            'Sentinel', 'System-Card-Author'),
        'prereq': 'This section assumes the model-card and datasheet patterns from <a href="section-54.6.html">Section 54.6</a> and <a href="section-54.7.html">Section 54.7</a>, the LLM-safety framing from <a href="../../part-10-trustworthy-llms/module-49-llm-safety-alignment/section-49.1.html">Section 49.1</a>, and the frontier-API release pattern from <a href="../../part-3-working-with-llms/module-11-llm-apis/section-11.1.html">Section 11.1</a>.',
    },
    'part-11-llm-ethics-trust-governance/module-54b-transparency-and-disclosure/section-54.9.html': {
        'epigraph': ep(
            "Logging an LLM agent\'s every reasoning step is the cheapest insurance policy you will ever buy, and the only one that pays out at 3 AM.",
            'Sage', 'Audit-Log-Stewart'),
        'prereq': 'This section assumes the LLM observability and tracing tools from <a href="../../part-9-llm-evaluation-observability/module-44-observability-tracing/section-44.1.html">Section 44.1</a>, the model-card discipline from <a href="section-54.6.html">Section 54.6</a>, and the regulatory-framework vocabulary from <a href="../module-55-policy-and-regulation/section-55.1.html">Section 55.1</a>.',
    },
    'part-11-llm-ethics-trust-governance/module-54b-transparency-and-disclosure/section-54.10.html': {
        'epigraph': ep(
            "The lawsuit asks one question: why did your LLM say no? If your answer is \'because the softmax did\', plan to settle.",
            'Hallux', 'Explainability-Lawyer'),
        'prereq': 'This section assumes the LLM-interpretability vocabulary from <a href="../../part-2-understanding-llms/module-07-interpretability-mechanistic/section-7.1.html">Section 7.1</a>, the audit-log discipline from <a href="section-54.9.html">Section 54.9</a>, and the bias-and-fairness framing from <a href="../module-50-bias-fairness/section-50.1.html">Section 50.1</a>.',
    },

    # ==================================================================
    # Module 56 (Responsible AI Tools-of-the-trade: 56.1-56.5)
    # ==================================================================
    'part-11-llm-ethics-trust-governance/module-56-responsible-ai-tools/section-56.1.html': {
        'prereq': 'This section assumes the bias-and-fairness vocabulary from <a href="../module-50-bias-fairness/section-50.1.html">Section 50.1</a>, the LLM-safety framing from <a href="../../part-10-trustworthy-llms/module-49-llm-safety-alignment/section-49.1.html">Section 49.1</a>, and the model-card and audit-log patterns from <a href="../module-54b-transparency-and-disclosure/section-54.6.html">Section 54.6</a>.',
    },
    'part-11-llm-ethics-trust-governance/module-56-responsible-ai-tools/section-56.2.html': {
        'prereq': 'This section assumes the responsible-AI platforms from <a href="section-56.1.html">Section 56.1</a>, the differential-privacy fundamentals from <a href="../module-53-privacy-and-data-protection/section-53.3.html">Section 53.3</a>, and the LLM-watermarking techniques from <a href="../module-54-watermarking-provenance/section-54.2.html">Section 54.2</a>.',
    },
    'part-11-llm-ethics-trust-governance/module-56-responsible-ai-tools/section-56.3.html': {
        'prereq': 'This section assumes the LLM evaluation methodology from <a href="../../part-9-llm-evaluation-observability/module-42-evaluation-foundations/section-42.1.html">Section 42.1</a> and the bias-and-fairness vocabulary from <a href="../module-50-bias-fairness/section-50.1.html">Section 50.1</a>.',
    },
    'part-11-llm-ethics-trust-governance/module-56-responsible-ai-tools/section-56.4.html': {
        'prereq': 'This section assumes the LLM model zoo from <a href="../../part-3-working-with-llms/module-14-tools-of-the-trade/section-14.4.html">Section 14.4</a>, the LLM-safety and constitutional-AI patterns from <a href="../../part-10-trustworthy-llms/module-49-llm-safety-alignment/section-49.2.html">Section 49.2</a>, and the watermark-detection techniques from <a href="../module-54-watermarking-provenance/section-54.2.html">Section 54.2</a>.',
    },
    'part-11-llm-ethics-trust-governance/module-56-responsible-ai-tools/section-56.5.html': {
        'prereq': 'This is an end-of-chapter reading list and assumes familiarity with the responsible-AI modules in Part XI.',
    },

    # ==================================================================
    # Module 58 (Frontier Systems Hardware: 58.3-58.5)
    # ==================================================================
    'part-12-llm-systems-at-scale/module-58-frontier-systems-hardware/section-58.3.html': {
        'epigraph': ep(
            "On-device LLMs solved one problem (latency) and created another (battery). The phone heats up, but it talks back without WiFi.",
            'Quant', 'Edge-Watt-Counter'),
        'prereq': 'This section assumes the quantization formats from <a href="../../part-2-understanding-llms/module-10-interpretability/section-10.1.html">Section 10.1</a>, the open-weights model zoo from <a href="../../part-2-understanding-llms/module-10-interpretability/section-10.8.html">Section 10.8</a>, and the LLM-inference cost mechanics from <a href="../../part-2-understanding-llms/module-09-inference-deployment/section-9.1.html">Section 9.1</a>.',
    },
    'part-12-llm-systems-at-scale/module-58-frontier-systems-hardware/section-58.4.html': {
        'epigraph': ep(
            "FlashAttention is the kernel that taught a generation of researchers to read CUDA. FlashAttention-4 is the kernel that taught them to read Blackwell.",
            'Tensor', 'Kernel-Whisperer'),
        'prereq': 'This section assumes the attention mechanics from <a href="../../part-1-llm-building-blocks/module-04-transformer-architecture-self-attention/section-4.2.html">Section 4.2</a>, the FlashAttention-1 and -2 background from <a href="../../part-2-understanding-llms/module-09-inference-deployment/section-9.4.html">Section 9.4</a>, and basic CUDA familiarity.',
    },
    'part-12-llm-systems-at-scale/module-58-frontier-systems-hardware/section-58.5.html': {
        'epigraph': ep(
            "Training and inference used to be separate departments. In 2026 they share a Slack channel and an architectural budget.",
            'Sched', 'Co-Design-Native'),
        'prereq': 'This section assumes the LLM pretraining objective from <a href="../../part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.2.html">Section 6.2</a>, the inference-stack mechanics from <a href="../../part-2-understanding-llms/module-09-inference-deployment/section-9.1.html">Section 9.1</a>, and the distributed-training patterns from <a href="../module-59-distributed-training-systems/section-59.1.html">Section 59.1</a>.',
    },

    # ==================================================================
    # Module 59 (Distributed Training: section 59.5)
    # ==================================================================
    'part-12-llm-systems-at-scale/module-59-distributed-training-systems/section-59.5.html': {
        'prereq': 'This section assumes the distributed-training patterns from <a href="section-59.1.html">Section 59.1</a> through <a href="section-59.4.html">Section 59.4</a>, the LLM-pretraining lifecycle from <a href="../../part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.1.html">Section 6.1</a>, and the operational-observability fundamentals from <a href="../../part-9-llm-evaluation-observability/module-44-observability-tracing/section-44.1.html">Section 44.1</a>.',
    },

    # ==================================================================
    # Module 65 (Containers and Kubernetes: 65.1-65.4)
    # ==================================================================
    'part-13-llmops-lifecycle/module-65-containers-kubernetes/section-65.1.html': {
        'epigraph': ep(
            "It works on my machine, but my machine is now a Docker image, and your machine is also that Docker image, and so the bug is reproducible by definition.",
            'Deploy', 'Container-Native'),
        'prereq': 'This section assumes basic Linux command-line fluency, awareness of Python virtual environments, and a working mental model for what an LLM inference server is (covered in <a href="../../part-2-understanding-llms/module-09-inference-deployment/section-9.1.html">Section 9.1</a>).',
    },
    'part-13-llmops-lifecycle/module-65-containers-kubernetes/section-65.2.html': {
        'epigraph': ep(
            "A Dockerfile is a love letter to whoever has to rebuild your environment in five years. Make sure it is a polite love letter.",
            'Pip', 'Layer-Cache-Maximalist'),
        'prereq': 'This section assumes the Docker fundamentals from <a href="section-65.1.html">Section 65.1</a> and basic familiarity with Python packaging (pip, poetry, or uv).',
    },
    'part-13-llmops-lifecycle/module-65-containers-kubernetes/section-65.3.html': {
        'epigraph': ep(
            "Docker Compose is what you reach for when you need three services and zero ops engineers. The fourth service is when you stop reaching.",
            'Sched', 'Compose-Pragmatist'),
        'prereq': 'This section assumes the Docker fundamentals from <a href="section-65.1.html">Section 65.1</a>, the Dockerfile patterns from <a href="section-65.2.html">Section 65.2</a>, and the basic LLM-server vocabulary from <a href="../../part-2-understanding-llms/module-10-interpretability/section-10.5.html">Section 10.5</a>.',
    },
    'part-13-llmops-lifecycle/module-65-containers-kubernetes/section-65.4.html': {
        'epigraph': ep(
            "An LLM inference server in a container is a small chess engine inside a small chess engine. Memory, latency, and GPU access all have to line up.",
            'Deploy', 'GPU-Container-Tuner'),
        'prereq': 'This section assumes the Docker fundamentals from <a href="section-65.1.html">Section 65.1</a>, the LLM inference servers (vLLM, TGI, TensorRT-LLM) from <a href="../../part-2-understanding-llms/module-10-interpretability/section-10.5.html">Section 10.5</a>, and the NVIDIA Container Toolkit basics introduced in <a href="section-65.2.html">Section 65.2</a>.',
    },

    # ==================================================================
    # Module 67 (Ideation: 67.2, 67.3, 67.6)
    # ==================================================================
    'part-14-designing-llm-agent-products/module-67-ideation/section-67.2.html': {
        'epigraph': ep(
            "The best LLM product idea is the one your customer cannot stop describing. Your job is to listen long enough to write it down.",
            'Prompt', 'Discovery-Interview-Native'),
        'prereq': 'This section assumes the ideation fundamentals from <a href="section-67.1.html">Section 67.1</a> and a working mental model of the LLM-agent capability landscape from <a href="../../part-6-llm-agents/module-26-agent-foundations/section-26.1.html">Section 26.1</a>.',
    },
    'part-14-designing-llm-agent-products/module-67-ideation/section-67.3.html': {
        'epigraph': ep(
            "The Bet-My-Money Test asks one question: would I personally pay for this LLM product? If the answer is \'maybe\', the answer is no.",
            'Reward', 'Bet-My-Money-Veteran'),
        'prereq': 'This section assumes the problem-discovery heuristics from <a href="section-67.2.html">Section 67.2</a> and the LLM-capability map from <a href="../../part-3-working-with-llms/module-14-tools-of-the-trade/section-14.4.html">Section 14.4</a>.',
    },
    'part-14-designing-llm-agent-products/module-67-ideation/section-67.6.html': {
        'epigraph': ep(
            "Conversational AI UX is the discipline of teaching the user to be a co-author. The user did not sign up for that, so design accordingly.",
            'Lexica', 'UX-Disclosure-Native'),
        'prereq': 'This section assumes the conversational-AI fundamentals from <a href="../../part-8-conversational-ai-with-llms/module-37-conversational-ai-foundations/section-37.1.html">Section 37.1</a>, the LLM-agent product framing from <a href="section-67.1.html">Section 67.1</a>, and the vibe-coding iteration loop from <a href="../module-68-vibe-coding/section-68.1.html">Section 68.1</a>.',
    },

    # ==================================================================
    # Module 68 (Vibe Coding: 68.3, 68.5, 68.6)
    # ==================================================================
    'part-14-designing-llm-agent-products/module-68-vibe-coding/section-68.3.html': {
        'epigraph': ep(
            "Cursor, Claude Code, Cline, Zed, Windsurf, Copilot Workspace. Pick one and you have picked a workflow. Pick two and you have picked a war.",
            'Frontier', 'IDE-Switcher'),
        'prereq': 'This section assumes the vibe-coding fundamentals from <a href="section-68.1.html">Section 68.1</a>, the LLM-agent vocabulary from <a href="../../part-6-llm-agents/module-26-agent-foundations/section-26.1.html">Section 26.1</a>, and the LLM-API patterns from <a href="../../part-3-working-with-llms/module-11-llm-apis/section-11.1.html">Section 11.1</a>.',
    },
    'part-14-designing-llm-agent-products/module-68-vibe-coding/section-68.5.html': {
        'epigraph': ep(
            "An MVP is a vertical slice that someone can actually use. A horizontal slice is a PowerPoint and a regret.",
            'Distill', 'Slice-Designer'),
        'prereq': 'This section assumes the ideation framework from <a href="../module-67-ideation/section-67.1.html">Section 67.1</a>, the vibe-coding patterns from <a href="section-68.1.html">Section 68.1</a>, and the LLM-API and prompt-engineering basics from <a href="../../part-3-working-with-llms/module-15-prompt-engineering/section-15.1.html">Section 15.1</a>.',
    },
    'part-14-designing-llm-agent-products/module-68-vibe-coding/section-68.6.html': {
        'epigraph': ep(
            "The pilot tells you three things, in order: keep, pivot, or kill. Pre-committing to the kill criteria is the only honest way to read those signals.",
            'Eval', 'Pilot-Trigger-Pragmatist'),
        'prereq': 'This section assumes the vertical-slice MVP pattern from <a href="section-68.5.html">Section 68.5</a>, the LLM-evaluation fundamentals from <a href="../../part-9-llm-evaluation-observability/module-42-evaluation-foundations/section-42.1.html">Section 42.1</a>, and the ROI-measurement vocabulary from <a href="../module-69-llm-economics/section-69.1.html">Section 69.1</a>.',
    },

    # ==================================================================
    # Module 69 (LLM Economics: 69.1-69.3)
    # ==================================================================
    'part-14-designing-llm-agent-products/module-69-llm-economics/section-69.1.html': {
        'epigraph': ep(
            "ROI for an LLM product is the answer to two questions: did anyone save time, and did anyone notice?",
            'Quant', 'ROI-Skeptic'),
        'prereq': 'This section assumes the LLM-pricing fundamentals from <a href="../../part-3-working-with-llms/module-11-llm-apis/section-11.5.html">Section 11.5</a> and the basic product-evaluation framing from <a href="../module-67-ideation/section-67.1.html">Section 67.1</a>.',
    },
    'part-14-designing-llm-agent-products/module-69-llm-economics/section-69.2.html': {
        'epigraph': ep(
            "Latency, quality, cost. You can have any two, and the third is the customer support ticket.",
            'Compass', 'Three-Knob-Tuner'),
        'prereq': 'This section assumes the ROI-measurement framework from <a href="section-69.1.html">Section 69.1</a>, the inference-cost mechanics from <a href="../../part-2-understanding-llms/module-09-inference-deployment/section-9.1.html">Section 9.1</a>, and the prompt-engineering vocabulary from <a href="../../part-3-working-with-llms/module-15-prompt-engineering/section-15.1.html">Section 15.1</a>.',
    },
    'part-14-designing-llm-agent-products/module-69-llm-economics/section-69.3.html': {
        'epigraph': ep(
            "Multi-vendor arbitrage is the art of treating an LLM API like a power grid. The trick is hedging when the grid blinks.",
            'Sched', 'Vendor-Arbitrage-Operator'),
        'prereq': 'This section assumes the per-token unit-cost math from <a href="section-69.2.html">Section 69.2</a>, the LLM-API patterns from <a href="../../part-3-working-with-llms/module-11-llm-apis/section-11.1.html">Section 11.1</a>, and the vendor landscape from <a href="../../part-3-working-with-llms/module-14-tools-of-the-trade/section-14.1.html">Section 14.1</a>.',
    },

    # ==================================================================
    # Module 72 (Legal LLMs: 72.1-72.5; only some need prereq)
    # ==================================================================
    'part-15-applications-of-llms-across-industries/module-72-legal-llms/section-72.1.html': {
        'epigraph': ep(
            "Contract review by LLM: cheaper than an associate, more reliable than a paralegal, less reliable than the LLM thinks it is.",
            'Guard', 'Legal-Pragmatist'),
    },
    'part-15-applications-of-llms-across-industries/module-72-legal-llms/section-72.2.html': {
        'epigraph': ep(
            "Mata v. Avianca taught lawyers to grep their LLM citations. The bar associations are still catching up.",
            'Hallux', 'Citation-Verifier'),
        'prereq': 'This section assumes the legal LLM use cases from <a href="section-72.1.html">Section 72.1</a>, the hallucination vocabulary from <a href="../../part-10-trustworthy-llms/module-47-hallucination-and-grounding/section-47.1.html">Section 47.1</a>, and the LLM-evaluation framing from <a href="../../part-9-llm-evaluation-observability/module-42-evaluation-foundations/section-42.1.html">Section 42.1</a>.',
    },
    'part-15-applications-of-llms-across-industries/module-72-legal-llms/section-72.3.html': {
        'epigraph': ep(
            "ABA Model Rule 1.1 says competence. In 2026 that includes knowing what your LLM cannot do, and saying so out loud.",
            'Compass', 'Compliance-Reader'),
        'prereq': 'This section assumes the legal-LLM failure modes from <a href="section-72.2.html">Section 72.2</a>, the regulatory-framework vocabulary from <a href="../../part-11-llm-ethics-trust-governance/module-55-policy-and-regulation/section-55.1.html">Section 55.1</a>, and a passing familiarity with the EU AI Act risk tiers.',
    },
    'part-15-applications-of-llms-across-industries/module-72-legal-llms/section-72.4.html': {
        'epigraph': ep(
            "Verified RAG is just RAG with the promise that the citation is real. The promise is load-bearing.",
            'Rag', 'Verified-Retrieval-Architect'),
    },
    'part-15-applications-of-llms-across-industries/module-72-legal-llms/section-72.5.html': {
        'epigraph': ep(
            "The legal LLM vendor list moves quarterly. The bar-association rules move yearly. Plan procurement accordingly.",
            'Sage', 'Vendor-Watcher'),
        'prereq': 'This is a vendors-and-further-reading section. It assumes familiarity with the earlier sections in this chapter (Sections 72.1 through 72.4) and the LLM-platform vocabulary from <a href="../../part-3-working-with-llms/module-14-tools-of-the-trade/section-14.1.html">Section 14.1</a>.',
    },

    # ==================================================================
    # Module 73 (Finance LLMs: 73.1-73.5)
    # ==================================================================
    'part-15-applications-of-llms-across-industries/module-73-finance-llms/section-73.1.html': {
        'epigraph': ep(
            "Equity research synthesis, KYC, customer ops, code generation. The boring use cases that finance actually deployed, while everyone talked about robo-advisors.",
            'Quant', 'Banking-Reality-Reader'),
    },
    'part-15-applications-of-llms-across-industries/module-73-finance-llms/section-73.2.html': {
        'epigraph': ep(
            "An LLM that hallucinates a number in finance is not a curiosity. It is a regulator\'s phone call.",
            'Hallux', 'Number-Hallucination-Tracker'),
        'prereq': 'This section assumes the finance LLM use cases from <a href="section-73.1.html">Section 73.1</a>, the hallucination vocabulary from <a href="../../part-10-trustworthy-llms/module-47-hallucination-and-grounding/section-47.1.html">Section 47.1</a>, and the bias-and-fairness framing from <a href="../../part-11-llm-ethics-trust-governance/module-50-bias-fairness/section-50.1.html">Section 50.1</a>.',
    },
    'part-15-applications-of-llms-across-industries/module-73-finance-llms/section-73.3.html': {
        'epigraph': ep(
            "SR 11-7, DORA, FINRA, EU AI Act. Four acronyms, one shared message: document everything, especially what your LLM cannot do.",
            'Compass', 'Reg-Acronym-Pedant'),
        'prereq': 'This section assumes the finance LLM failure modes from <a href="section-73.2.html">Section 73.2</a>, the LLM-policy vocabulary from <a href="../../part-11-llm-ethics-trust-governance/module-55-policy-and-regulation/section-55.1.html">Section 55.1</a>, and the model-card and audit-log patterns from <a href="../../part-11-llm-ethics-trust-governance/module-54b-transparency-and-disclosure/section-54.6.html">Section 54.6</a>.',
    },
    'part-15-applications-of-llms-across-industries/module-73-finance-llms/section-73.4.html': {
        'epigraph': ep(
            "Tier 0 LLM: read-only. Tier 3: act on a million dollars. The promotion gates are where the architecture lives.",
            'Scale', 'Tier-Gate-Architect'),
        'prereq': 'This section assumes the regulatory framework from <a href="section-73.3.html">Section 73.3</a>, the LLM-agent permission patterns from <a href="../../part-6-llm-agents/module-27-agent-architectures/section-27.1.html">Section 27.1</a>, and the audit-log discipline from <a href="../../part-11-llm-ethics-trust-governance/module-54b-transparency-and-disclosure/section-54.9.html">Section 54.9</a>.',
    },
    'part-15-applications-of-llms-across-industries/module-73-finance-llms/section-73.5.html': {
        'epigraph': ep(
            "BloombergGPT, FactSet Mercury, JPMorgan IndexGPT. The vendor list is a roadmap of which LLM bet which institution actually placed.",
            'Frontier', 'Finance-Vendor-Watcher'),
        'prereq': 'This is a vendors-and-further-reading section. It assumes familiarity with the earlier sections in Chapter 73 and the LLM-platform vocabulary from <a href="../../part-3-working-with-llms/module-14-tools-of-the-trade/section-14.1.html">Section 14.1</a>.',
    },

    # ==================================================================
    # Module 74 (Healthcare LLMs: 74.1-74.5)
    # ==================================================================
    'part-15-applications-of-llms-across-industries/module-74-healthcare-llms/section-74.1.html': {
        'epigraph': ep(
            "An LLM ambient-scribe saves a physician fifteen minutes per visit. Multiply by patients per week and you have the deployment thesis in one number.",
            'Token', 'Ambient-Scribe-Realist'),
    },
    'part-15-applications-of-llms-across-industries/module-74-healthcare-llms/section-74.2.html': {
        'epigraph': ep(
            "A confident wrong answer in healthcare is the most expensive sentence an LLM can produce. The mitigation list is short and load-bearing.",
            'Hallux', 'Healthcare-Hallucination-Steward'),
        'prereq': 'This section assumes the healthcare LLM use cases from <a href="section-74.1.html">Section 74.1</a>, the hallucination vocabulary from <a href="../../part-10-trustworthy-llms/module-47-hallucination-and-grounding/section-47.1.html">Section 47.1</a>, and the bias-and-fairness framing from <a href="../../part-11-llm-ethics-trust-governance/module-50-bias-fairness/section-50.1.html">Section 50.1</a>.',
    },
    'part-15-applications-of-llms-across-industries/module-74-healthcare-llms/section-74.3.html': {
        'epigraph': ep(
            "HIPAA, FDA SaMD, EU AI Act, state licensure, CHAI. Five regulatory layers, one LLM deployment, and a permanent need for caution.",
            'Compass', 'Regulatory-Stack-Climber'),
        'prereq': 'This section assumes the healthcare-LLM failure modes from <a href="section-74.2.html">Section 74.2</a>, the LLM-policy vocabulary from <a href="../../part-11-llm-ethics-trust-governance/module-55-policy-and-regulation/section-55.1.html">Section 55.1</a>, and the audit-log discipline from <a href="../../part-11-llm-ethics-trust-governance/module-54b-transparency-and-disclosure/section-54.9.html">Section 54.9</a>.',
    },
    'part-15-applications-of-llms-across-industries/module-74-healthcare-llms/section-74.4.html': {
        'epigraph': ep(
            "BAA-covered cloud is the default. On-premises open-weight is the escape hatch. The trade-off is the entire HIPAA chapter in one decision.",
            'Deploy', 'BAA-Native'),
        'prereq': 'This section assumes the healthcare regulatory framework from <a href="section-74.3.html">Section 74.3</a>, the open-versus-closed LLM deployment trade-off from <a href="../../part-2-understanding-llms/module-10-interpretability/section-10.5.html">Section 10.5</a>, and the LLMOps container patterns from <a href="../../part-13-llmops-lifecycle/module-65-containers-kubernetes/section-65.1.html">Section 65.1</a>.',
    },
    'part-15-applications-of-llms-across-industries/module-74-healthcare-llms/section-74.5.html': {
        'epigraph': ep(
            "Abridge, Suki, Glass Health, Hippocratic AI. Each vendor solves one slice of the clinic; the procurement question is which slice.",
            'Sage', 'Clinic-Vendor-Mapper'),
        'prereq': 'This is a vendors-and-further-reading section and assumes familiarity with the earlier sections in Chapter 74.',
    },

    # ==================================================================
    # Module 75 (Education LLMs: 75.1-75.5)
    # ==================================================================
    'part-15-applications-of-llms-across-industries/module-75-education-llms/section-75.1.html': {
        'epigraph': ep(
            "Socratic tutoring, assessment generation, accessibility. The three places where an LLM actually moves the needle in a classroom.",
            'Bert', 'Pedagogy-Reader'),
    },
    'part-15-applications-of-llms-across-industries/module-75-education-llms/section-75.2.html': {
        'epigraph': ep(
            "Plagiarism detectors detect students who cannot afford the latest paraphrasing tool. The LLM arms race has a class problem.",
            'Hallux', 'Detector-Skeptic'),
        'prereq': 'This section assumes the education LLM use cases from <a href="section-75.1.html">Section 75.1</a>, the hallucination vocabulary from <a href="../../part-10-trustworthy-llms/module-47-hallucination-and-grounding/section-47.1.html">Section 47.1</a>, and the LLM-watermarking-and-detection background from <a href="../../part-11-llm-ethics-trust-governance/module-54-watermarking-provenance/section-54.4.html">Section 54.4</a>.',
    },
    'part-15-applications-of-llms-across-industries/module-75-education-llms/section-75.3.html': {
        'epigraph': ep(
            "FERPA, COPPA, EU AI Act, accreditation. The four regulatory rails that decide which LLM tutor your school can actually license.",
            'Compass', 'Education-Compliance-Reader'),
        'prereq': 'This section assumes the education LLM failure modes from <a href="section-75.2.html">Section 75.2</a> and the LLM-policy vocabulary from <a href="../../part-11-llm-ethics-trust-governance/module-55-policy-and-regulation/section-55.1.html">Section 55.1</a>.',
    },
    'part-15-applications-of-llms-across-industries/module-75-education-llms/section-75.4.html': {
        'epigraph': ep(
            "Khanmigo, Magic School, Duolingo Max. The pedagogically-scaffolded tutor pattern repeats across each, with one shared lesson: the LLM is the muscle, the scaffold is the bone.",
            'Scale', 'Scaffold-Reader'),
        'prereq': 'This section assumes the education regulatory framework from <a href="section-75.3.html">Section 75.3</a>, the LLM-prompt and tool-use patterns from <a href="../../part-3-working-with-llms/module-15-prompt-engineering/section-15.1.html">Section 15.1</a>, and the RAG fundamentals from <a href="../../part-7-retrieval-information-extraction-with-llms/module-31-rag-retrieval-augmented-generation/section-31.1.html">Section 31.1</a>.',
    },
    'part-15-applications-of-llms-across-industries/module-75-education-llms/section-75.5.html': {
        'epigraph': ep(
            "ChatGPT Edu, Anthropic for Education, Khanmigo. The 2026 education-LLM vendor map is short, but its compliance terms are dense.",
            'Sage', 'EdTech-Vendor-Reader'),
        'prereq': 'This is a vendors-and-further-reading section and assumes familiarity with the earlier sections in Chapter 75.',
    },

    # ==================================================================
    # Module 76 (Cybersecurity LLMs: 76.1-76.5)
    # ==================================================================
    'part-15-applications-of-llms-across-industries/module-76-cybersecurity-llms/section-76.1.html': {
        'epigraph': ep(
            "Blue-team LLM use cases: alert triage, phishing review, code-review-for-vulns. The boring SOC work that an LLM actually moves the needle on.",
            'Sentinel', 'SOC-Triage-Native'),
    },
    'part-15-applications-of-llms-across-industries/module-76-cybersecurity-llms/section-76.2.html': {
        'epigraph': ep(
            "Red-team LLM use cases: phishing copy, vulnerability research, malware adaptation. The asymmetry of LLM offense and defense is the whole chapter in one sentence.",
            'Guard', 'Red-Team-Realist'),
        'prereq': 'This section assumes the defensive LLM use cases from <a href="section-76.1.html">Section 76.1</a>, the LLM-safety framing from <a href="../../part-10-trustworthy-llms/module-49-llm-safety-alignment/section-49.1.html">Section 49.1</a>, and the jailbreaking vocabulary from <a href="../../part-10-trustworthy-llms/module-48-llm-attack-vectors/section-48.1.html">Section 48.1</a>.',
    },
    'part-15-applications-of-llms-across-industries/module-76-cybersecurity-llms/section-76.3.html': {
        'epigraph': ep(
            "OWASP Top 10 for LLM applications: prompt injection, data leakage, supply chain. The list is short because the field is young, not because the threats are.",
            'Hallux', 'LLM-OWASP-Reader'),
        'prereq': 'This section assumes the LLM-attack-vector vocabulary from <a href="../../part-10-trustworthy-llms/module-48-llm-attack-vectors/section-48.1.html">Section 48.1</a> and the red-team use cases from <a href="section-76.2.html">Section 76.2</a>.',
    },
    'part-15-applications-of-llms-across-industries/module-76-cybersecurity-llms/section-76.4.html': {
        'epigraph': ep(
            "Input classification, output filtering, tool sandboxing, authorization. The four trust boundaries that decide whether your LLM agent gets a paycheck or a CVE.",
            'Guard', 'Trust-Boundary-Architect'),
        'prereq': 'This section assumes the LLM-attack-surface vocabulary from <a href="section-76.3.html">Section 76.3</a>, the LLM-agent permission patterns from <a href="../../part-6-llm-agents/module-27-agent-architectures/section-27.1.html">Section 27.1</a>, and the LLM-tool-use patterns from <a href="../../part-6-llm-agents/module-26-agent-foundations/section-26.3.html">Section 26.3</a>.',
    },
    'part-15-applications-of-llms-across-industries/module-76-cybersecurity-llms/section-76.5.html': {
        'epigraph': ep(
            "Security Copilot, Charlotte AI, Wiz, Tines. The 2026 security-LLM vendor map is short; the threat landscape is not.",
            'Sage', 'Security-Vendor-Reader'),
        'prereq': 'This is a vendors-and-further-reading section and assumes familiarity with the earlier sections in Chapter 76.',
    },

    # ==================================================================
    # Module 77 (Government LLMs: 77.1-77.5)
    # ==================================================================
    'part-15-applications-of-llms-across-industries/module-77-government-llms/section-77.1.html': {
        'epigraph': ep(
            "Constituent service triage, FOIA, regulatory drafting. The LLM use cases inside government are quiet, low-glamour, and saving thousands of human hours per agency per quarter.",
            'Census', 'Gov-Triage-Reader'),
    },
    'part-15-applications-of-llms-across-industries/module-77-government-llms/section-77.2.html': {
        'epigraph': ep(
            "NYC MyCity hallucinated tenant rights. Michigan MiDAS automated fraud accusations. Dutch SyRI flagged immigrants. Three case studies, one warning.",
            'Hallux', 'Public-Sector-Pessimist'),
        'prereq': 'This section assumes the government LLM use cases from <a href="section-77.1.html">Section 77.1</a>, the hallucination vocabulary from <a href="../../part-10-trustworthy-llms/module-47-hallucination-and-grounding/section-47.1.html">Section 47.1</a>, and the bias-and-fairness framing from <a href="../../part-11-llm-ethics-trust-governance/module-50-bias-fairness/section-50.1.html">Section 50.1</a>.',
    },
    'part-15-applications-of-llms-across-industries/module-77-government-llms/section-77.3.html': {
        'epigraph': ep(
            "OMB M-24-10, FedRAMP, Section 508, EU AI Act. Each one is a checklist; together they are a procurement strategy.",
            'Compass', 'FedRAMP-Reader'),
        'prereq': 'This section assumes the government LLM failure modes from <a href="section-77.2.html">Section 77.2</a> and the policy vocabulary from <a href="../../part-11-llm-ethics-trust-governance/module-55-policy-and-regulation/section-55.1.html">Section 55.1</a>.',
    },
    'part-15-applications-of-llms-across-industries/module-77-government-llms/section-77.4.html': {
        'epigraph': ep(
            "Strict-scope retrieval, citations always, refusal by default, audit log, accessibility-first. The five rules of a public-sector LLM that does not end up on the front page.",
            'Rag', 'Public-Sector-RAG-Architect'),
        'prereq': 'This section assumes the government regulatory framework from <a href="section-77.3.html">Section 77.3</a>, the RAG fundamentals from <a href="../../part-7-retrieval-information-extraction-with-llms/module-31-rag-retrieval-augmented-generation/section-31.1.html">Section 31.1</a>, and the LLM-audit-log discipline from <a href="../../part-11-llm-ethics-trust-governance/module-54b-transparency-and-disclosure/section-54.9.html">Section 54.9</a>.',
    },
    'part-15-applications-of-llms-across-industries/module-77-government-llms/section-77.5.html': {
        'epigraph': ep(
            "Palantir AIP, Anduril, FedRAMP-authorized providers. The vendor list is short; the postmortem list is shorter and more instructive.",
            'Sage', 'Gov-Vendor-Reader'),
        'prereq': 'This is a vendors-and-postmortems section and assumes familiarity with the earlier sections in Chapter 77.',
    },

    # ==================================================================
    # Module 78 (Manufacturing LLMs: 78.1-78.10)
    # ==================================================================
    'part-15-applications-of-llms-across-industries/module-78-manufacturing-llms/section-78.1.html': {
        'epigraph': ep(
            "Maintenance copilots, inspection reports, work-order drafting. The plant-floor LLM use cases that are quietly returning hours per shift, while the headlines chased robots.",
            'Token', 'Plant-Floor-Reader'),
    },
    'part-15-applications-of-llms-across-industries/module-78-manufacturing-llms/section-78.2.html': {
        'epigraph': ep(
            "An LLM hallucinated a torque spec on a plant floor in 2024. The torque was wrong. The lessons were many.",
            'Hallux', 'Spec-Hallucination-Investigator'),
        'prereq': 'This section assumes the manufacturing LLM use cases from <a href="section-78.1.html">Section 78.1</a>, the hallucination vocabulary from <a href="../../part-10-trustworthy-llms/module-47-hallucination-and-grounding/section-47.1.html">Section 47.1</a>, and a passing familiarity with IT and OT network boundaries.',
    },
    'part-15-applications-of-llms-across-industries/module-78-manufacturing-llms/section-78.3.html': {
        'epigraph': ep(
            "ISO/IEC 42001, ISA/IEC 62443, NIST SP 800-82, EU Machinery Regulation. Four acronyms, one warning: an LLM in OT is still subject to the safety case.",
            'Compass', 'Manufacturing-Compliance-Reader'),
        'prereq': 'This section assumes the manufacturing LLM failure modes from <a href="section-78.2.html">Section 78.2</a> and the LLM-policy vocabulary from <a href="../../part-11-llm-ethics-trust-governance/module-55-policy-and-regulation/section-55.1.html">Section 55.1</a>.',
    },
    'part-15-applications-of-llms-across-industries/module-78-manufacturing-llms/section-78.4.html': {
        'epigraph': ep(
            "On-premises serving, curated equipment corpus, always-cite-retrieval, never-execute-control. The four rules of a 2026 plant-floor LLM copilot.",
            'Rag', 'Plant-Floor-RAG-Architect'),
        'prereq': 'This section assumes the manufacturing regulatory framework from <a href="section-78.3.html">Section 78.3</a>, the RAG fundamentals from <a href="../../part-7-retrieval-information-extraction-with-llms/module-31-rag-retrieval-augmented-generation/section-31.1.html">Section 31.1</a>, and the LLM-container patterns from <a href="../../part-13-llmops-lifecycle/module-65-containers-kubernetes/section-65.1.html">Section 65.1</a>.',
    },
    'part-15-applications-of-llms-across-industries/module-78-manufacturing-llms/section-78.5.html': {
        'epigraph': ep(
            "Foxconn Foxbrain, Siemens Industrial Copilot, the 2024 torque-spec pilot. Three named cases that taught the industry how an LLM on a plant floor actually behaves.",
            'Sage', 'Plant-Floor-Case-Reader'),
        'prereq': 'This section assumes the plant-floor copilot architecture from <a href="section-78.4.html">Section 78.4</a> and the LLM evaluation methodology from <a href="../../part-9-llm-evaluation-observability/module-42-evaluation-foundations/section-42.1.html">Section 42.1</a>.',
    },
    'part-15-applications-of-llms-across-industries/module-78-manufacturing-llms/section-78.6.html': {
        'epigraph': ep(
            "Music, video, design, marketing copy. The four creative industries that moved fastest from \'interesting demo\' to \'in the production pipeline\'.",
            'Sparky', 'Creative-Pipeline-Reader'),
    },
    'part-15-applications-of-llms-across-industries/module-78-manufacturing-llms/section-78.7.html': {
        'epigraph': ep(
            "Suno, Runway, ElevenLabs, Firefly. Each vendor has its own answer to the rights question, and that answer is half the contract.",
            'Compass', 'IP-Litigation-Tracker'),
    },
    'part-15-applications-of-llms-across-industries/module-78-manufacturing-llms/section-78.8.html': {
        'epigraph': ep(
            "Ranking, retrieval, and personalization are the largest deployed application of ML, full stop. LLMs are just the latest layer in a forty-year stack.",
            'Vec', 'Ranking-Stack-Reader'),
    },
    'part-15-applications-of-llms-across-industries/module-78-manufacturing-llms/section-78.10.html': {
        'epigraph': ep(
            "Pinterest Lens, Spotify AI DJ, YouTube generative discovery. The conversational-discovery pattern repeats across each, with one shared lesson: the catalog is the corpus.",
            'Lexica', 'Discovery-UX-Reader'),
    },

    # ==================================================================
    # Module 82 (AGI Trajectories: 82.1-82.5)
    # ==================================================================
    'part-16-llm-agentic-ai-research-frontiers/module-82-agi-trajectories/section-82.1.html': {
        'epigraph': ep(
            "HLE, ARC-AGI-2, FrontierMath. The benchmarks that move when the frontier LLM moves, and stay still when it does not.",
            'Eval', 'Frontier-Benchmark-Reader'),
        'prereq': 'This section assumes the LLM evaluation methodology from <a href="../../part-9-llm-evaluation-observability/module-42-evaluation-foundations/section-42.1.html">Section 42.1</a>, the LLM-as-judge fundamentals from <a href="../../part-9-llm-evaluation-observability/module-46-llm-as-judge-automated-evaluation/section-46.1.html">Section 46.1</a>, and a passing familiarity with the frontier-API model zoo from <a href="../../part-3-working-with-llms/module-14-tools-of-the-trade/section-14.4.html">Section 14.4</a>.',
    },
    'part-16-llm-agentic-ai-research-frontiers/module-82-agi-trajectories/section-82.2.html': {
        'epigraph': ep(
            "Alignment at frontier scale is the test of whether RLHF, DPO, and Constitutional AI transfer to LLMs that can outsmart their evaluators.",
            'Guard', 'Alignment-Pragmatist'),
        'prereq': 'This section assumes the RLHF and DPO mechanics from <a href="../../part-3-working-with-llms/module-08-instruction-tuning-rlhf/section-8.1.html">Section 8.1</a>, the Constitutional-AI vocabulary from <a href="../../part-10-trustworthy-llms/module-49-llm-safety-alignment/section-49.2.html">Section 49.2</a>, and the LLM-safety framing from the same chapter.',
    },
    'part-16-llm-agentic-ai-research-frontiers/module-82-agi-trajectories/section-82.3.html': {
        'epigraph': ep(
            "AGI timelines are confidence intervals that change with the next benchmark. The honest answer is a range and an underline.",
            'Frontier', 'Timeline-Honest'),
        'prereq': 'This section assumes the frontier benchmark vocabulary from <a href="section-82.1.html">Section 82.1</a>, the LLM scaling-law intuition from <a href="../../part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.3.html">Section 6.3</a>, and the alignment framing from <a href="section-82.2.html">Section 82.2</a>.',
    },
    'part-16-llm-agentic-ai-research-frontiers/module-82-agi-trajectories/section-82.4.html': {
        'epigraph': ep(
            "The capability frontier is the headline. The labor market is the lede. The shape of the gap is where the policy lives.",
            'Census', 'Labor-Market-Reader'),
        'prereq': 'This section assumes the AGI-timeline vocabulary from <a href="section-82.3.html">Section 82.3</a> and the LLM-policy framing from <a href="../../part-11-llm-ethics-trust-governance/module-55-policy-and-regulation/section-55.1.html">Section 55.1</a>.',
    },
    'part-16-llm-agentic-ai-research-frontiers/module-82-agi-trajectories/section-82.5.html': {
        'epigraph': ep(
            "By 2026 the AGI debate has shrunk into a smaller set of measurable LLM-capability disagreements. Smaller is not solved, but it is progress.",
            'Sage', 'Year-End-Reckoner'),
        'prereq': 'This section assumes the rest of Chapter 82 (sections 82.1 through 82.4) and the LLM-agent capability vocabulary from <a href="../../part-6-llm-agents/module-26-agent-foundations/section-26.1.html">Section 26.1</a>.',
    },

    # ==================================================================
    # Module 83 (Frontier Tools-of-the-trade: 83.1-83.5)
    # ==================================================================
    'part-16-llm-agentic-ai-research-frontiers/module-83-tools-of-the-trade/section-83.1.html': {
        'epigraph': ep(
            "The frontier moves faster than peer review. The platforms that win are the ones that ship the same week the paper does.",
            'Frontier', 'Pre-Print-Platform-Reader'),
        'prereq': 'This section assumes the LLM-API platform vocabulary from <a href="../../part-3-working-with-llms/module-14-tools-of-the-trade/section-14.1.html">Section 14.1</a> and the frontier-benchmark vocabulary from <a href="../module-82-agi-trajectories/section-82.1.html">Section 82.1</a>.',
    },
    'part-16-llm-agentic-ai-research-frontiers/module-83-tools-of-the-trade/section-83.2.html': {
        'epigraph': ep(
            "Paper-tracking, prototyping, evaluation. Three layers of the frontier-LLM library stack, and the only ones that survive each quarterly rewrite.",
            'Pip', 'Frontier-Library-Reader'),
        'prereq': 'This section assumes the frontier-LLM platform shelf from <a href="section-83.1.html">Section 83.1</a> and the LLM-library landscape from <a href="../../part-3-working-with-llms/module-14-tools-of-the-trade/section-14.2.html">Section 14.2</a>.',
    },
    'part-16-llm-agentic-ai-research-frontiers/module-83-tools-of-the-trade/section-83.3.html': {
        'epigraph': ep(
            "Benchmarks are the field\'s empirical anchor. Their leaderboards are the field\'s scoreboard. Their contamination is the field\'s recurring scandal.",
            'Eval', 'Leaderboard-Skeptic'),
        'prereq': 'This section assumes the LLM evaluation methodology from <a href="../../part-9-llm-evaluation-observability/module-42-evaluation-foundations/section-42.1.html">Section 42.1</a> and the frontier-benchmark vocabulary from <a href="../module-82-agi-trajectories/section-82.1.html">Section 82.1</a>.',
    },
    'part-16-llm-agentic-ai-research-frontiers/module-83-tools-of-the-trade/section-83.4.html': {
        'epigraph': ep(
            "The reasoning-first tier (o3, Claude with extended thinking, Gemini 2.5 Pro). The cost-first tier (Haiku, Mini, Flash). The open-weights tier (Llama, Qwen, DeepSeek). Each tier is a deployment thesis.",
            'Frontier', 'Frontier-Model-Reader'),
        'prereq': 'This section assumes the LLM model-zoo vocabulary from <a href="../../part-3-working-with-llms/module-14-tools-of-the-trade/section-14.4.html">Section 14.4</a> and the open-weights LLM landscape from <a href="../../part-2-understanding-llms/module-10-interpretability/section-10.8.html">Section 10.8</a>.',
    },
    'part-16-llm-agentic-ai-research-frontiers/module-83-tools-of-the-trade/section-83.5.html': {
        'epigraph': ep(
            "The specific LLM tools in this book will mostly be obsolete in five years. The venues that publish them will not.",
            'Sage', 'Venue-Reader'),
        'prereq': 'This is the book\'s closing reading list and assumes familiarity with the frontier-LLM modules in Chapters 82 and 83.',
    },

}
