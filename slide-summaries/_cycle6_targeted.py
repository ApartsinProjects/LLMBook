#!/usr/bin/env python
"""Cycle 6 (v2): curated technique checks. For each of 30 decks, define ~6-10
specific canonical concept names the slide deck covers, and check whether each
appears in the target book section(s)."""
import json
import re
from pathlib import Path

ROOT = Path(r"E:/Projects/BookBlogsHome/LLMBook")
SS = ROOT / "slide-summaries"


# Curated: (deck_id, target_paths, [(concept_label, list_of_substring_aliases_to_match)])
CHECKS = [
    ("1300_LLM_TransformersInternals/1301_Attention",
     ["part-1-llm-building-blocks/module-02-sequence-models-attention/section-2.2.html",
      "part-1-llm-building-blocks/module-02-sequence-models-attention/section-2.3.html",
      "part-1-llm-building-blocks/module-02-sequence-models-attention/section-2.4.html"],
     [
        ("scaled dot-product attention", ["scaled dot-product", "scaled dot product"]),
        ("Q/K/V projections", ["query", "key", "value"]),
        ("softmax over scores", ["softmax"]),
        ("multi-head attention", ["multi-head", "multi head"]),
        ("worked numerical example", ["worked example", "numerical example", "concrete example"]),
        ("masking for causal attention", ["causal mask", "look-ahead mask", "future tokens"]),
        ("Bahdanau / additive attention origin", ["bahdanau", "additive attention", "luong"]),
        ("attention as soft alignment", ["soft alignment", "alignment"]),
     ]),
    ("1300_LLM_TransformersInternals/1302_Transformer",
     ["part-1-llm-building-blocks/module-03-transformer-architecture/section-3.1.html",
      "part-1-llm-building-blocks/module-03-transformer-architecture/section-3.2.html",
      "part-1-llm-building-blocks/module-03-transformer-architecture/section-3.3.html",
      "part-1-llm-building-blocks/module-03-transformer-architecture/section-3.4.html"],
     [
        ("positional encoding (sinusoidal)", ["sinusoidal", "positional encoding"]),
        ("layer normalization", ["layernorm", "layer norm", "layer normalization"]),
        ("residual connection / skip", ["residual", "skip connection"]),
        ("feed-forward sublayer dims", ["feed-forward", "feedforward", "ffn"]),
        ("multi-head attention", ["multi-head"]),
        ("pre-norm vs post-norm", ["pre-norm", "post-norm", "pre norm", "post norm"]),
        ("GELU activation", ["gelu", "relu"]),
        ("encoder vs decoder stacks", ["encoder stack", "decoder stack", "encoder-decoder"]),
     ]),
    ("1300_LLM_TransformersInternals/1304_SentenceEmbedding",
     ["part-4-training-adaptation/module-16-fine-tuning-fundamentals/section-16.5.html",
      "part-7-retrieval-information-extraction-with-llms/module-31-embeddings-vector-db/section-31.2.html"],
     [
        ("SBERT / Sentence-BERT", ["sbert", "sentence-bert", "sentence bert"]),
        ("siamese / triplet network", ["siamese", "triplet network", "triplet loss"]),
        ("contrastive InfoNCE", ["infonce", "info-nce"]),
        ("multiple-negatives ranking loss", ["multiple negatives", "multiple-negatives", "mnr"]),
        ("MTEB benchmark", ["mteb"]),
        ("mean pooling / [CLS]", ["mean pooling", "cls pooling", "[cls]"]),
        ("SimCSE / supervised SimCSE", ["simcse"]),
        ("STS-B evaluation", ["stsb", "sts-b", "semantic textual similarity"]),
     ]),
    ("1300_LLM_TransformersInternals/1306_FinetuningHumanFeedback",
     ["part-4-training-adaptation/module-18-alignment-rlhf-dpo/section-18.1.html",
      "part-4-training-adaptation/module-18-alignment-rlhf-dpo/section-18.2.html"],
     [
        ("preference pairs (chosen/rejected)", ["preference pair", "chosen", "rejected"]),
        ("reward model / Bradley-Terry", ["bradley-terry", "bradley terry", "reward model"]),
        ("PPO four-model setup", ["ppo", "policy", "reference model"]),
        ("KL penalty to reference", ["kl penalty", "kl divergence", "kl regularization"]),
        ("DPO objective", ["dpo", "direct preference"]),
        ("RLHF pipeline", ["rlhf"]),
        ("InstructGPT origin", ["instructgpt"]),
        ("Constitutional AI / RLAIF", ["constitutional", "rlaif"]),
     ]),
    ("1300_LLM_TransformersInternals/1307_TransformerSeq2Seq",
     ["part-1-llm-building-blocks/module-03-transformer-architecture/section-3.1.html",
      "part-1-llm-building-blocks/module-03-transformer-architecture/section-3.3.html",
      "part-1-llm-building-blocks/module-03-transformer-architecture/section-3.4.html",
      "part-1-llm-building-blocks/module-03-transformer-architecture/section-3.5.html"],
     [
        ("encoder-decoder architecture", ["encoder-decoder", "encoder decoder"]),
        ("cross-attention", ["cross-attention", "cross attention"]),
        ("T5", ["t5", "text-to-text"]),
        ("BART", ["bart"]),
        ("dual mask helpers (src/tgt)", ["src mask", "tgt mask", "source mask", "target mask"]),
        ("autoregressive decoder", ["autoregressive", "auto-regressive"]),
        ("teacher forcing", ["teacher forcing"]),
        ("machine translation example", ["machine translation", "translation example"]),
     ]),
    ("1300_LLM_TransformersInternals/1308_TransfomerMixtureOfExperts",
     ["part-1-llm-building-blocks/module-03-transformer-architecture/section-3.8.html"],
     [
        ("expert gating / router", ["router", "gating network", "gating function"]),
        ("top-k routing", ["top-k", "top k routing", "topk"]),
        ("load balancing loss", ["load balancing", "load-balancing", "auxiliary loss"]),
        ("noisy gating", ["noisy gating", "noisy top-k"]),
        ("Switch Transformer (top-1)", ["switch transformer"]),
        ("Mixtral", ["mixtral"]),
        ("DeepSeek MoE", ["deepseek"]),
        ("GShard", ["gshard"]),
        ("expert collapse / imbalance", ["expert collapse", "expert imbalance", "expert starvation", "router collapse"]),
        ("parameter arithmetic worked example", ["dense 2m", "130k", "16 experts", "active per token", "active parameters"]),
     ]),
    ("1300_LLM_TransformersInternals/1310_LLM_ExplainingTransformer",
     ["part-2-understanding-llms/module-10-interpretability/section-10.4.html"],
     [
        ("attention visualization", ["attention visualization", "attention map", "attention pattern"]),
        ("BertViz", ["bertviz"]),
        ("attention rollout", ["attention rollout"]),
        ("induction heads", ["induction head"]),
        ("circuits / interpretability", ["circuit"]),
        ("probing classifiers", ["probing"]),
        ("activation patching", ["activation patching", "causal tracing"]),
        ("logit lens", ["logit lens"]),
     ]),
    ("1300_LLM_TransformersInternals/1311_LLM_MultilinguialEncoder",
     ["part-2-understanding-llms/module-07-modern-llm-landscape/section-7.4.html"],
     [
        ("mBERT", ["mbert"]),
        ("XLM-R / XLM-RoBERTa", ["xlm-r", "xlm roberta", "xlm-roberta"]),
        ("XLM three losses (MLM/CLM/TLM)", ["tlm", "translation language model"]),
        ("mT5", ["mt5"]),
        ("NLLB-200", ["nllb"]),
        ("curse of multilinguality", ["curse of multilingual"]),
        ("tokenization fertility", ["fertility"]),
        ("language adapter", ["language adapter", "madx", "mad-x"]),
        ("Aya / Aya 23", ["aya"]),
        ("Noam learning-rate schedule", ["noam"]),
     ]),
    ("1320_LLM_TransferLearning/1321_PEFT",
     ["part-4-training-adaptation/module-17-peft/section-17.1.html",
      "part-4-training-adaptation/module-17-peft/section-17.2.html"],
     [
        ("LoRA low-rank update", ["lora", "low-rank"]),
        ("QLoRA / NF4", ["qlora", "nf4"]),
        ("adapter modules", ["adapter"]),
        ("IA3", ["ia3", "ia^3", "ia-3"]),
        ("prefix tuning", ["prefix tuning", "prefix-tuning"]),
        ("BitFit", ["bitfit"]),
        ("rank / alpha hyperparameters", ["rank ", "alpha"]),
        ("DoRA", ["dora"]),
     ]),
    ("1320_LLM_TransferLearning/1322_PromptTuning",
     ["part-4-training-adaptation/module-17-peft/section-17.4.html"],
     [
        ("soft prompts / virtual tokens", ["soft prompt", "virtual token"]),
        ("P-tuning / P-tuning v2", ["p-tuning", "p tuning"]),
        ("prompt tuning origin (Lester)", ["lester"]),
        ("prefix tuning", ["prefix tuning"]),
        ("hard vs soft prompts", ["hard prompt", "soft prompt"]),
        ("trainable prompt embedding", ["prompt embedding"]),
        ("initialization with vocab", ["vocab initialization", "init from vocab"]),
     ]),
    ("1320_LLM_TransferLearning/1324_ClassificationFineTuning",
     ["part-4-training-adaptation/module-16-fine-tuning-fundamentals/section-16.6.html"],
     [
        ("classification head ([CLS])", ["classification head", "[cls]", "cls token"]),
        ("SetFit", ["setfit"]),
        ("NER fine-tuning", ["ner", "named entity"]),
        ("token classification", ["token classification"]),
        ("class imbalance / weighting", ["class imbalance", "class weight", "focal loss"]),
        ("evaluation: F1, accuracy", ["f1", "accuracy"]),
        ("multi-label classification", ["multi-label", "multilabel"]),
        ("sigmoid vs softmax head", ["sigmoid", "softmax"]),
     ]),
    ("1320_LLM_TransferLearning/1325_AdaptingForLongText",
     ["part-4-training-adaptation/module-16-fine-tuning-fundamentals/section-16.7.html"],
     [
        ("RoPE", ["rope", "rotary"]),
        ("YaRN", ["yarn"]),
        ("NTK-aware interpolation", ["ntk"]),
        ("position interpolation (Su)", ["position interpolation"]),
        ("LongLoRA", ["longlora"]),
        ("Longformer / BigBird", ["longformer", "bigbird"]),
        ("sliding window attention", ["sliding window"]),
        ("needle in haystack eval", ["needle in", "needle-in", "haystack"]),
        ("hierarchical / chunk-and-fuse", ["hierarchical", "chunk and fuse", "chunk-and-fuse"]),
        ("lost in the middle", ["lost in the middle", "lost-in-the-middle"]),
     ]),
    ("1320_LLM_TransferLearning/1326_LLMDistilation",
     ["part-4-training-adaptation/module-17-peft/section-17.5.html",
      "part-4-training-adaptation/module-17-peft/section-17.6.html"],
     [
        ("teacher-student KD", ["teacher", "student", "distillation"]),
        ("KL on soft logits", ["kl", "kullback", "soft target", "soft logit"]),
        ("temperature in softmax", ["temperature"]),
        ("DistilBERT", ["distilbert"]),
        ("MiniLM / TinyBERT", ["minilm", "tinybert"]),
        ("response/rationale distillation", ["response distillation", "rationale distillation"]),
        ("task-agnostic vs task-specific KD", ["task-agnostic", "task agnostic"]),
        ("Hinton 2015 origin", ["hinton"]),
     ]),
    ("1320_LLM_TransferLearning/1327_LLMMerge",
     ["part-4-training-adaptation/module-17-peft/section-17.7.html"],
     [
        ("model soup / averaging", ["model soup", "weight averag", "averaging weights"]),
        ("Task Arithmetic", ["task arithmetic"]),
        ("TIES merging", ["ties merge", "ties-merge", "ties merging"]),
        ("DARE", ["dare merge", "dare drop", " dare "]),
        ("SLERP", ["slerp"]),
        ("mergekit library", ["mergekit"]),
        ("task vector", ["task vector"]),
        ("Frankenmerge / passthrough", ["frankenmerge", "passthrough"]),
     ]),
    ("1400_LLM_RAG/1401_VectorStores",
     ["part-7-retrieval-information-extraction-with-llms/module-31-embeddings-vector-db/section-31.5.html"],
     [
        ("FAISS", ["faiss"]),
        ("HNSW", ["hnsw"]),
        ("IVF / inverted file", ["ivf", "inverted file"]),
        ("product quantization (PQ)", ["product quantization", " pq "]),
        ("scalar quantization", ["scalar quantization"]),
        ("Annoy", ["annoy"]),
        ("ScaNN / DiskANN", ["scann", "diskann"]),
        ("Milvus / Pinecone / Weaviate / Qdrant / Chroma", ["milvus", "pinecone", "weaviate", "qdrant", "chroma"]),
        ("metric: cosine / dot / L2", ["cosine", "dot product", "l2 distance", "euclidean"]),
        ("recall vs latency tradeoff", ["recall", "latency"]),
     ]),
    ("1400_LLM_RAG/1402_RAG_Intro",
     ["part-7-retrieval-information-extraction-with-llms/module-32-rag/section-32.1.html"],
     [
        ("naive RAG pipeline", ["naive rag", "naïve rag", "rag pipeline"]),
        ("retriever / generator split", ["retriever", "generator"]),
        ("dense retrieval", ["dense retriev", "bi-encoder", "biencoder", "dense passage"]),
        ("hybrid (BM25 + dense)", ["bm25", "hybrid"]),
        ("chunking strategies", ["chunk"]),
        ("re-ranking", ["rerank", "re-rank"]),
        ("context window stuffing", ["context window", "context stuffing"]),
        ("DPR / Karpukhin", ["dpr ", "karpukhin"]),
     ]),
    ("1400_LLM_RAG/1403_RAG_Evaluations",
     ["part-7-retrieval-information-extraction-with-llms/module-32-rag/section-32.2.html"],
     [
        ("RAGAS", ["ragas"]),
        ("ARES", ["ares"]),
        ("TruLens / RAG triad", ["trulens", "rag triad"]),
        ("faithfulness / groundedness", ["faithfulness", "groundedness"]),
        ("context precision / recall", ["context precision", "context recall"]),
        ("answer relevance", ["answer relevance"]),
        ("MRR / NDCG / recall@k", ["mrr", "ndcg", "recall@"]),
        ("LLM-as-judge", ["llm-as-judge", "llm as judge"]),
        ("BLEU / ROUGE / BERTScore", ["bleu", "rouge", "bertscore"]),
     ]),
    ("1400_LLM_RAG/1404_AdvancedRAG",
     ["part-7-retrieval-information-extraction-with-llms/module-35-advanced-rag/section-35.1.html",
      "part-7-retrieval-information-extraction-with-llms/module-35-advanced-rag/section-35.2.html"],
     [
        ("HyDE", ["hyde"]),
        ("HyPE", ["hype"]),
        ("Self-RAG", ["self-rag", "self rag"]),
        ("CRAG (corrective)", ["crag", "corrective rag"]),
        ("query rewriting / decomposition", ["query rewriting", "decomposition"]),
        ("RAG-Fusion / RRF", ["rag-fusion", "rag fusion", "rrf"]),
        ("MultiQueryRetriever", ["multiquery", "multi-query"]),
        ("MMR diversity", ["mmr", "maximal marginal relevance"]),
        ("RAPTOR (tree)", ["raptor"]),
        ("RAFT / FiD", ["raft", "fid "]),
     ]),
    ("1420_LLM_Agents/1421_Tools_FunctionCalls",
     ["part-6-agentic-ai/module-27-tool-use-protocols/section-27.1.html"],
     [
        ("JSON schema for tool args", ["json schema", "tool schema", "function schema"]),
        ("OpenAI tool / function calling", ["function calling", "tool calling"]),
        ("structured output / mode", ["structured output", "structured response"]),
        ("Toolformer", ["toolformer"]),
        ("ToolkenGPT", ["toolkengpt", "toolken"]),
        ("parallel tool calls", ["parallel tool"]),
        ("tool error / retry handling", ["tool error", "tool failure", "retry"]),
        ("OpenAPI / OAS tool spec", ["openapi", "swagger"]),
     ]),
    ("1420_LLM_Agents/1422_Tools_MCP",
     ["part-6-agentic-ai/module-27-tool-use-protocols/section-27.2.html"],
     [
        ("MCP host / client / server", ["mcp host", "mcp client", "mcp server"]),
        ("tools primitive", ["tools primitive"]),
        ("resources primitive", ["resources primitive"]),
        ("prompts primitive", ["prompts primitive"]),
        ("sampling primitive", ["sampling primitive"]),
        ("Streamable HTTP transport", ["streamable http", "stdio transport", "sse transport"]),
        ("MCP specification revision", ["2025-06", "2024-11", "2025-03"]),
        ("Anthropic / OpenAI / Google adoption", ["anthropic", "claude desktop"]),
     ]),
    ("1420_LLM_Agents/1424_LangGraph_Intro",
     ["part-6-agentic-ai/module-30-tools-of-the-trade/section-30.2.html"],
     [
        ("StateGraph", ["stategraph"]),
        ("reducer pattern", ["reducer"]),
        ("nodes and edges", ["langgraph node", "graph node"]),
        ("tools_condition router", ["tools_condition", "conditional edge"]),
        ("ReAct agent in graph", ["react agent", "react pattern"]),
        ("checkpointer / threads", ["checkpointer", "thread_id", "thread id"]),
        ("streaming output", ["streaming", "stream events"]),
        ("HITL / interrupt", ["human-in-the-loop", "interrupt"]),
        ("LangGraph Studio", ["langgraph studio"]),
        ("Supervisor pattern", ["supervisor"]),
     ]),
    ("1420_LLM_Agents/1427_Agents_AgenticRAG",
     ["part-7-retrieval-information-extraction-with-llms/module-32-rag/section-32.3.html"],
     [
        ("agent-as-router for RAG", ["agentic rag", "agent rag", "agent router"]),
        ("Self-RAG with reflection", ["self-rag", "self rag"]),
        ("CRAG corrective loop", ["crag", "corrective"]),
        ("query planning", ["query planning", "plan and execute"]),
        ("multi-hop retrieval", ["multi-hop", "multihop"]),
        ("iterative retrieval", ["iterative retrieval"]),
        ("Deep Research pattern", ["deep research"]),
        ("evaluator-optimizer loop", ["evaluator", "critic loop"]),
        ("citation grounding", ["citation"]),
     ]),
    ("1420_LLM_Agents/1428_Agents_Planning",
     ["part-6-agentic-ai/module-26-ai-agents/section-26.2.html"],
     [
        ("ReAct (reason + act)", ["react ", "reason and act"]),
        ("Plan-and-Execute", ["plan-and-execute", "plan and execute"]),
        ("ReWoo (E1/E2)", ["rewoo"]),
        ("Tree of Thoughts", ["tree of thoughts", "tot"]),
        ("Chain of Thought", ["chain of thought", "cot"]),
        ("Reflexion / Responder+Revisor", ["reflexion", "responder", "revisor"]),
        ("LLM Compiler / parallel planning", ["llm compiler"]),
        ("Baby-AGI", ["baby-agi", "babyagi"]),
        ("hierarchical task network", ["htn", "hierarchical task"]),
     ]),
    ("5012_Audio_Processing/5012_Audio_Data",
     ["part-5-multimodal-llms/module-20-audio-music-generation/section-20.0.1.html"],
     [
        ("sample rate (kHz)", ["sample rate", "khz", "sampling rate"]),
        ("bit depth", ["bit depth", "16-bit", "24-bit"]),
        ("mono vs stereo channels", ["mono", "stereo", "channel"]),
        ("mel-spectrogram", ["mel-spectrogram", "mel spectrogram"]),
        ("MFCC", ["mfcc"]),
        ("STFT framing/window", ["stft", "short-time fourier", "windowing", "framing"]),
        ("Hann/Hamming window", ["hann window", "hamming window"]),
        ("WAV / FLAC / MP3 formats", ["wav", "flac", "mp3"]),
        ("Nyquist sampling", ["nyquist"]),
     ]),
    ("5012_Audio_Processing/5013_Audio_VectorQuant",
     ["part-5-multimodal-llms/module-20-audio-music-generation/section-20.0.2.html"],
     [
        ("Residual Vector Quantization (RVQ)", ["rvq", "residual vector quant"]),
        ("SoundStream", ["soundstream"]),
        ("EnCodec", ["encodec"]),
        ("Descript Audio Codec (DAC)", ["descript audio", " dac "]),
        ("Mimi codec (Moshi)", ["mimi codec", "mimi (moshi)", "moshi"]),
        ("codebook collapse footgun", ["codebook collapse"]),
        ("EMA codebook update", ["ema", "exponential moving average"]),
        ("nq (number of quantizers)", ["nq", "n_q", "number of quantizers"]),
        ("bitrate per stream", ["bitrate", "kbps"]),
        ("encoder-quantizer-decoder pipeline", ["quantizer", "encoder decoder"]),
     ]),
    ("5015_Audio_FM/5015_PretrainedAudioModels",
     ["part-5-multimodal-llms/module-20-audio-music-generation/section-20.5.html"],
     [
        ("Whisper (v1/v2/v3)", ["whisper"]),
        ("Distil-Whisper", ["distil-whisper", "distilwhisper"]),
        ("WhisperX", ["whisperx"]),
        ("Canary / NeMo", ["canary", "nemo"]),
        ("SeamlessM4T", ["seamlessm4t", "seamless m4t"]),
        ("Conformer encoder", ["conformer"]),
        ("CTC head", ["ctc"]),
        ("multilingual ASR", ["multilingual asr"]),
        ("VAD / diarization", ["voice activity", "diarization"]),
        ("WER benchmark", ["wer"]),
     ]),
    ("5020_Audio_Encoders/5021_Audio_Encoders",
     ["part-5-multimodal-llms/module-20-audio-music-generation/section-20.0.4.html"],
     [
        ("wav2vec 2.0", ["wav2vec"]),
        ("HuBERT (iterative k-means)", ["hubert"]),
        ("WavLM", ["wavlm"]),
        ("BEATs", ["beats"]),
        ("contrastive task", ["contrastive"]),
        ("masked prediction objective", ["masked prediction", "mask prediction"]),
        ("quantized targets / context vectors", ["quantized target", "context vector"]),
        ("CPC origin (contrastive predictive)", ["cpc", "contrastive predictive coding"]),
        ("downstream SUPERB benchmark", ["superb"]),
     ]),
    ("5040_Audio_Speech2Text/5041_Audio_Speech2Text",
     ["part-5-multimodal-llms/module-20-audio-music-generation/section-20.5.html",
      "part-5-multimodal-llms/module-20-audio-music-generation/section-20.0.3.html"],
     [
        ("Whisper encoder-decoder", ["whisper"]),
        ("CTC vs seq2seq decoding", ["ctc", "seq2seq"]),
        ("beam search decoding", ["beam search"]),
        ("language ID / timestamps", ["language id", "timestamp"]),
        ("streaming ASR", ["streaming asr", "streaming whisper"]),
        ("HF transformers pipeline('automatic-speech-recognition')", ["automatic-speech-recognition", "asr pipeline"]),
        ("WER metric", ["wer"]),
        ("punctuation/capitalization restoration", ["punctuation"]),
     ]),
    ("0010_Common_MLDL/0016_PyTorchTutorial",
     ["appendices/appendix-e-pytorch-reference/index.html",
      "appendices/appendix-e-pytorch-reference/section-e.1.html",
      "appendices/appendix-e-pytorch-reference/section-e.2.html",
      "appendices/appendix-e-pytorch-reference/section-e.3.html",
      "appendices/appendix-e-pytorch-reference/section-e.4.html",
      "appendices/appendix-e-pytorch-reference/section-e.5.html",
      "appendices/appendix-e-pytorch-reference/section-e.6.html",
      "appendices/appendix-e-pytorch-reference/section-e.7.html",
      "appendices/appendix-e-pytorch-reference/section-e.8.html",
      "appendices/appendix-e-pytorch-reference/section-e.9.html",
      "appendices/appendix-e-pytorch-reference/section-e.10.html"],
     [
        ("Tensor creation / dtype / device", ["tensor", "dtype", "device"]),
        ("autograd / backward", ["autograd", "backward"]),
        ("nn.Module", ["nn.module"]),
        ("Dataset / DataLoader", ["dataloader", "dataset"]),
        ("training loop (optimizer, loss)", ["optimizer", "loss"]),
        ("AMP / mixed precision", ["amp", "mixed precision", "bfloat16"]),
        ("torch.compile", ["torch.compile"]),
        ("DDP / FSDP distributed", ["ddp", "fsdp", "distributeddataparallel"]),
        ("profiler", ["profiler"]),
        ("hooks (forward/backward)", ["hook"]),
        ("state_dict save/load", ["state_dict", "state dict"]),
        ("gradient clipping", ["gradient clipping", "clip_grad"]),
     ]),
    ("1410_LLM_TopicModeling/1411_BERTTopics",
     ["part-7-retrieval-information-extraction-with-llms/module-31-embeddings-vector-db/section-31.7.html"],
     [
        ("BERTopic pipeline", ["bertopic"]),
        ("UMAP dimensionality reduction", ["umap"]),
        ("HDBSCAN clustering", ["hdbscan"]),
        ("c-TF-IDF representation", ["c-tf-idf", "ctfidf", "class tf-idf"]),
        ("KeyBERTInspired", ["keybert"]),
        ("MMR for representations", ["mmr", "maximal marginal"]),
        ("LDA comparison", ["lda"]),
        ("topic visualization", ["topic visualization", "intertopic"]),
        ("OpenAI label representation", ["openai", "llm representation"]),
     ]),
]


def check():
    results = []
    for deck_id, paths, concepts in CHECKS:
        # gather book text
        all_text = ""
        examined = []
        for p in paths:
            ap = ROOT / p
            if not ap.exists():
                continue
            all_text += ap.read_text(encoding="utf-8", errors="replace").lower() + "\n"
            examined.append(p)
        # gather slide text for sanity
        folder, stem = deck_id.split("/")
        md = SS / folder / f"{stem}.md"
        slide_text = md.read_text(encoding="utf-8", errors="replace") if md.exists() else ""
        present = []
        missing = []
        for label, aliases in concepts:
            hit = any(a in all_text for a in aliases)
            if hit:
                present.append(label)
            else:
                # only count as missing if slide actually covers it
                slide_lower = slide_text.lower()
                slide_has = any(a in slide_lower for a in aliases)
                if slide_has:
                    missing.append(label)
                # else, slide didn't strongly hint at it either — ignore
        verdict = "MATCH_OR_EXCEEDS" if not missing else "BOOK_SHALLOWER"
        # asset checks
        n_code = sum(len(re.findall(r"<pre[^>]*>", (ROOT/p).read_text(encoding='utf-8', errors='replace'))) for p in paths if (ROOT/p).exists())
        n_fig = sum(
            len(re.findall(r"<svg\b|<img[^>]*>|<figure", (ROOT/p).read_text(encoding='utf-8', errors='replace')))
            for p in paths if (ROOT/p).exists()
        )
        n_math = sum(
            len(re.findall(r"katex|\\\(|\\\[|<math\b", (ROOT/p).read_text(encoding='utf-8', errors='replace')))
            for p in paths if (ROOT/p).exists()
        )
        results.append({
            "deck": deck_id,
            "verdict": verdict,
            "concepts_total": len(concepts),
            "concepts_present": len(present),
            "concepts_missing": len(missing),
            "missing": missing,
            "present_sample": present[:5],
            "book_files": examined,
            "book_code_blocks": n_code,
            "book_figures": n_fig,
            "book_math_blocks": n_math,
        })
    out = SS / "_cycle6_slide_vs_book.json"
    out.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
    n_match = sum(1 for r in results if r["verdict"] == "MATCH_OR_EXCEEDS")
    n_shallow = sum(1 for r in results if r["verdict"] == "BOOK_SHALLOWER")
    print(f"Decks compared: {len(results)} | match/exceed: {n_match} | book shallower: {n_shallow}")
    print()
    for r in results:
        if r["verdict"] == "BOOK_SHALLOWER":
            print(f"  SHALLOW  {r['deck']:60s}  missing={r['concepts_missing']}/{r['concepts_total']}")
            for m in r["missing"]:
                print(f"           - {m}")
        else:
            print(f"  OK       {r['deck']:60s}  ({r['concepts_present']}/{r['concepts_total']})")


if __name__ == "__main__":
    check()
