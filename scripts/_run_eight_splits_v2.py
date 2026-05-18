"""
Driver to perform 8 GIANT_SECTION splits (P1 wave).

Sections:
  1. section-2.3 -> 2.3a/2.3b at h2 2.3.5 Multi-Head Attention (line 352)
  2. section-3.2 -> 3.2a/3.2b at h2 3.2.5 Understanding the Shapes (line 747) - mid-section h2 boundary
  3. section-7.1 -> 7.1a/7.1b at h2 7.1.4 Google DeepMind (line 139)
  4. section-9.1 -> 9.1a/9.1b at h2 9.1.4 Post-Training Quantization Algorithms (line 270)
  5. section-9.4 -> 9.4a/9.4b at h2 9.4.2 vLLM is split at 9.4.3 SGLang start (line 274)
     - But suggested break: at "vLLM Deep Dive" boundary (between theory and runtimes). 9.4.1 is the stack;
       9.4.2 is vLLM (long); 9.4.3+ are other runtimes. So break at the start of 9.4.3 SGLang (line 274).
  6. section-18.2 -> 18.2a/18.2b at h2 18.2.2 DPO Variants and Extensions (line 311)
  7. section-30.2 (SPECIAL HANDLER) - has outer <section> wrapper and 3 tot-subsections.
  8. section-37.5 -> 37.5a/37.5b at h2 37.5.6 Memory Consolidation Patterns (line 495)
"""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from _split_section_pair import split_html

BOOK = ROOT.parent

splits = [
    # 1) 2.3
    {
        "path": BOOK / "part-1-llm-building-blocks" / "module-02-sequence-models-attention" / "section-2.3.html",
        "break_line": 352,
        "a_title": "QKV, Scaled Dot-Product & Causal Masking",
        "a_desc": "The query-key-value abstraction, scaled dot-product attention, self vs cross attention, and causal masking for autoregressive models.",
        "b_title": "Multi-Head Attention, Complexity & Lab",
        "b_desc": "Multi-head attention, a from-scratch implementation lab, the O(n squared) complexity problem, and a complete worked example tying every piece together.",
        "a_suffix": "a",
        "b_suffix": "b",
        "b_intro_html": '<p>This continuation of <a href="section-2.3a.html">Section 2.3a</a> picks up after the single-head attention math is solid. It scales attention up to the multi-head version that real Transformers use, walks through a from-scratch PyTorch implementation, examines the quadratic complexity that drives every efficient-attention variant in later chapters, and closes with a complete worked example you can run end to end.</p>',
        "a_next_href": "section-2.3b.html",
        "a_next_label": "Section 2.3b",
        "a_next_title": "Multi-Head Attention, Complexity &amp; Lab",
        "b_prev_href": "section-2.3a.html",
        "b_prev_label": "Section 2.3a",
        "b_prev_title": "QKV, Scaled Dot-Product &amp; Causal Masking",
        "b_next_href": "../module-03-transformer-architecture/section-3.1a.html",
        "b_next_label": "Section 3.1",
        "b_next_title": "How a Transformer Computes One Token",
    },
    # 2) 3.2 - break at line 633 (h2 3.2.4 Training Loop) for balanced split
    {
        "path": BOOK / "part-1-llm-building-blocks" / "module-03-transformer-architecture" / "section-3.2.html",
        "break_line": 633,
        "a_title": "Build a Transformer: Architecture & Data Prep",
        "a_desc": "Build a decoder-only Transformer from scratch in PyTorch: what you are building, the complete model implementation walked through line by line, and the data preparation pipeline.",
        "b_title": "Transformer: Training Loop, Shapes & Debugging",
        "b_desc": "The full training loop, tracing tensor shapes through the network, running the lab end to end on a small dataset, and common bugs you will hit plus how to fix them.",
        "a_suffix": "a",
        "b_suffix": "b",
        "b_intro_html": '<p>This continuation of <a href="section-3.2a.html">Section 3.2a</a> picks up once the Transformer model is implemented and the data is ready to feed it. It wires up the full training loop, traces the tensor shapes that flow through every layer (the most useful thing to internalize when you start modifying these models), runs the lab end to end on a small character-level dataset, and catalogues the bugs that practically every from-scratch Transformer build hits along the way.</p>',
        "a_next_href": "section-3.2b.html",
        "a_next_label": "Section 3.2b",
        "a_next_title": "Transformer: Training Loop, Shapes &amp; Debugging",
        "b_prev_href": "section-3.2a.html",
        "b_prev_label": "Section 3.2a",
        "b_prev_title": "Build a Transformer: Architecture &amp; Data Prep",
        "b_next_href": "section-3.3.html",
        "b_next_label": "Section 3.3",
        "b_next_title": "Transformer Variants &amp; Efficiency",
    },
    # 3) 7.1
    {
        "path": BOOK / "part-2-understanding-llms" / "module-07-modern-llm-landscape" / "section-7.1.html",
        "break_line": 139,
        "a_title": "Frontier Models: OpenAI & Anthropic",
        "a_desc": "The frontier model landscape, OpenAI's GPT-4o and the o-series, and Anthropic's Claude family.",
        "b_title": "Frontier: Gemini, Architecture & Benchmarks",
        "b_desc": "Google's Gemini series, second-tier frontier providers, architecture unification across multimodal models, attention variants in frontier models, rate limits, the convergence trend, and benchmarking methodology including contamination.",
        "a_suffix": "a",
        "b_suffix": "b",
        "b_intro_html": '<p>This continuation of <a href="section-7.1a.html">Section 7.1a</a> picks up after OpenAI and Anthropic and covers the rest of the closed-source frontier: Google\'s Gemini series, the second-tier providers (xAI, Cohere, Mistral), the architectural patterns that converge across multimodal models, attention variants used in production frontier models, practical rate-limit constraints, the convergence trend, and the messy reality of benchmarking when contamination is everywhere.</p>',
        "a_next_href": "section-7.1b.html",
        "a_next_label": "Section 7.1b",
        "a_next_title": "Frontier: Gemini, Architecture &amp; Benchmarks",
        "b_prev_href": "section-7.1a.html",
        "b_prev_label": "Section 7.1a",
        "b_prev_title": "Frontier Models: OpenAI &amp; Anthropic",
        "b_next_href": "section-7.2.html",
        "b_next_label": "Section 7.2",
        "b_next_title": "Open-Source &amp; Open-Weight Models",
    },
    # 4) 9.1
    {
        "path": BOOK / "part-2-understanding-llms" / "module-09-inference-optimization" / "section-9.1.html",
        "break_line": 270,
        "a_title": "Quantization: Why, Math & Data Types",
        "a_desc": "Why inference is expensive, the mathematics of quantization, and the data types (INT8, INT4, NF4, FP8) used to store quantized weights.",
        "b_title": "Quantization: Algorithms, Practice & QAT",
        "b_desc": "Post-training quantization algorithms (GPTQ, AWQ, bitsandbytes), calibration strategies, quality degradation analysis, the GGUF format for local inference, and quantization-aware training.",
        "a_suffix": "a",
        "b_suffix": "b",
        "b_intro_html": '<p>This continuation of <a href="section-9.1a.html">Section 9.1a</a> picks up the algorithms that turn the quantization math into actual saved bits on disk. It covers the post-training quantization algorithms (GPTQ, AWQ, bitsandbytes), the calibration strategies that decide how much quality you lose, the GGUF format that makes local inference tractable, and quantization-aware training for the cases where post-training quantization is not enough.</p>',
        "a_next_href": "section-9.1b.html",
        "a_next_label": "Section 9.1b",
        "a_next_title": "Quantization: Algorithms, Practice &amp; QAT",
        "b_prev_href": "section-9.1a.html",
        "b_prev_label": "Section 9.1a",
        "b_prev_title": "Quantization: Why, Math &amp; Data Types",
        "b_next_href": "section-9.2.html",
        "b_next_label": "Section 9.2",
        "b_next_title": "KV Cache &amp; Memory Optimization",
    },
    # 5) 9.4
    {
        "path": BOOK / "part-2-understanding-llms" / "module-09-inference-optimization" / "section-9.4.html",
        "break_line": 274,
        "a_title": "Serving Stack & vLLM Deep Dive",
        "a_desc": "The LLM serving stack and a deep dive into vLLM, the most widely deployed open-source LLM serving framework.",
        "b_title": "Serving Runtimes: SGLang, TGI, TensorRT & Edge",
        "b_desc": "The other production runtimes: SGLang, TGI, TensorRT-LLM, LMDeploy, Ollama and llama.cpp for local inference, edge and in-browser inference, Triton Inference Server, a framework comparison, benchmarking methodology, and disaggregated inference that separates prefill from decode.",
        "a_suffix": "a",
        "b_suffix": "b",
        "b_intro_html": '<p>This continuation of <a href="section-9.4a.html">Section 9.4a</a> picks up after vLLM and surveys the rest of the serving landscape: the SGLang and TGI alternatives, NVIDIA\'s TensorRT-LLM for top-end throughput, LMDeploy, the local-inference runtimes (Ollama and llama.cpp), edge and in-browser options, Triton for multi-model serving, a head-to-head comparison, the benchmarking methodology that lets you choose between them, and the disaggregated-inference pattern that separates the prefill and decode phases for higher utilization.</p>',
        "a_next_href": "section-9.4b.html",
        "a_next_label": "Section 9.4b",
        "a_next_title": "Serving Runtimes: SGLang, TGI, TensorRT &amp; Edge",
        "b_prev_href": "section-9.4a.html",
        "b_prev_label": "Section 9.4a",
        "b_prev_title": "Serving Stack &amp; vLLM Deep Dive",
        "b_next_href": "section-9.5.html",
        "b_next_label": "Section 9.5",
        "b_next_title": "Model Pruning &amp; Sparsity",
    },
    # 6) 18.2
    {
        "path": BOOK / "part-4-training-adaptation" / "module-18-alignment-rlhf-dpo" / "section-18.2.html",
        "break_line": 311,
        "a_title": "DPO: Derivation & Single-Model Alignment",
        "a_desc": "The DPO derivation that lets a language model serve as its own reward model, and the single-model alignment objective that replaces RLHF's reward-model-plus-PPO pipeline.",
        "b_title": "DPO Variants, Datasets & Iterative DPO",
        "b_desc": "DPO variants (KTO, IPO, ORPO, SimPO), creating and synthesizing preference datasets, practical considerations for DPO training, and online and iterative DPO that pushes beyond a single training run.",
        "a_suffix": "a",
        "b_suffix": "b",
        "b_intro_html": '<p>This continuation of <a href="section-18.2a.html">Section 18.2a</a> picks up after the DPO derivation and explores the family of methods that have followed. It covers the DPO variants (KTO, IPO, ORPO, SimPO) that each address a specific limitation of the original formulation, how preference datasets are created and synthesized in practice, the practical training considerations that decide whether a DPO run actually works, and the online and iterative variants that push past a single offline training pass.</p>',
        "a_next_href": "section-18.2b.html",
        "a_next_label": "Section 18.2b",
        "a_next_title": "DPO Variants, Datasets &amp; Iterative DPO",
        "b_prev_href": "section-18.2a.html",
        "b_prev_label": "Section 18.2a",
        "b_prev_title": "DPO: Derivation &amp; Single-Model Alignment",
        "b_next_href": "section-18.3.html",
        "b_next_label": "Section 18.3",
        "b_next_title": "Constitutional AI &amp; Self-Alignment",
    },
    # 8) 37.5
    {
        "path": BOOK / "part-8-conversational-ai-with-llms" / "module-37-conversational-ai" / "section-37.5.html",
        "break_line": 495,
        "a_title": "Long-Term Memory: Vector, MemGPT & Profiles",
        "a_desc": "Long-term memory architectures: vector store memory, the MemGPT/Letta self-managing architecture, session persistence with user profiles, comparing memory approaches, and memory-as-a-service platforms.",
        "b_title": "Memory Consolidation, Evaluation & End-to-End",
        "b_desc": "Memory consolidation patterns that compress and prune over time, evaluating memory quality with the right metrics and benchmarks, and an end-to-end lab and worked example that ties short-term and long-term memory together.",
        "a_suffix": "a",
        "b_suffix": "b",
        "b_intro_html": '<p>This continuation of <a href="section-37.5a.html">Section 37.5a</a> picks up after the architectures and turns to memory operations. It covers the consolidation patterns that compress and prune memories so the store does not blow up over months of use, the evaluation metrics and benchmarks that tell you whether your memory layer is actually helping, and an end-to-end worked example that wires short-term and long-term memory into one chatbot.</p>',
        "a_next_href": "section-37.5b.html",
        "a_next_label": "Section 37.5b",
        "a_next_title": "Memory Consolidation, Evaluation &amp; End-to-End",
        "b_prev_href": "section-37.5a.html",
        "b_prev_label": "Section 37.5a",
        "b_prev_title": "Long-Term Memory: Vector, MemGPT &amp; Profiles",
        "b_next_href": "../module-40-voice-realtime-multimodal/section-40.1.html",
        "b_next_label": "Section 40.1",
        "b_next_title": "Voice Agents and Speech Interfaces",
    },
]


if __name__ == "__main__":
    for spl in splits:
        path_str = str(spl["path"])
        print(f"Splitting {path_str} at line {spl['break_line']}...")
        a_out, b_out = split_html(
            path=path_str,
            break_line=spl["break_line"],
            a_title=spl["a_title"],
            a_desc=spl["a_desc"],
            b_title=spl["b_title"],
            b_desc=spl["b_desc"],
            a_suffix=spl["a_suffix"],
            b_suffix=spl["b_suffix"],
            b_intro_html=spl["b_intro_html"],
            a_next_href=spl["a_next_href"],
            a_next_label=spl["a_next_label"],
            a_next_title=spl["a_next_title"],
            b_prev_href=spl["b_prev_href"],
            b_prev_label=spl["b_prev_label"],
            b_prev_title=spl["b_prev_title"],
            b_next_href=spl["b_next_href"],
            b_next_label=spl["b_next_label"],
            b_next_title=spl["b_next_title"],
        )
        print(f"  Wrote: {a_out}")
        print(f"  Wrote: {b_out}")
