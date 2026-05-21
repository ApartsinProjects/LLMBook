"""
Driver to perform the six splits as part of the giant-section wave.
"""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from _split_section_pair import split_html

BOOK = ROOT.parent

splits = [
    # 0.3 -> 0.3a (0.3.1 .. 0.3.6) + 0.3b (0.3.7 .. 0.3.10 + Exercises)
    {
        "path": BOOK / "part-1-llm-building-blocks" / "module-00-ml-pytorch-foundations" / "section-0.3.html",
        "break_line": 495,
        "a_title": "PyTorch Tensors, Autograd & Training Loop",
        "a_desc": "PyTorch tensors, autograd, building models with nn.Module, data loading, the basic training loop, and saving/loading model state.",
        "b_title": "PyTorch Debugging, Lab & Modern Performance",
        "b_desc": "Debugging with hooks and profilers, common mistakes, the FashionMNIST classifier lab, and modern PyTorch features: torch.compile, mixed precision, and distributed training.",
        "a_suffix": "a",
        "b_suffix": "b",
        "b_intro_html": '<p>This continuation of <a href="section-0.3a.html">Section 0.3a</a> picks up after you have the basic PyTorch training loop in hand. It covers the debugging tools that turn a non-training model into a training one, a hands-on FashionMNIST lab that exercises every concept from 0.3a, and the modern PyTorch features (<code>torch.compile</code>, AMP, FSDP) that move you from a working prototype to a fast one.</p>',
        "a_next_href": "section-0.3b.html",
        "a_next_label": "Section 0.3b",
        "a_next_title": "PyTorch Debugging, Lab & Modern Performance",
        "b_prev_href": "section-0.3a.html",
        "b_prev_label": "Section 0.3a",
        "b_prev_title": "PyTorch Tensors, Autograd & Training Loop",
        "b_next_href": "section-0.4.html",
        "b_next_label": "Section 0.4",
        "b_next_title": "Reinforcement Learning Foundations",
        # A prev preserved from original (section-0.2)
    },
    # 3.1 -> 3.1a (3.1.1 .. 3.1.8) + 3.1b (3.1.9 .. 3.1.13 + Exercises)
    {
        "path": BOOK / "part-1-llm-building-blocks" / "module-03-transformer-architecture" / "section-3.1.html",
        "break_line": 692,
        "a_title": "Transformer Anatomy: Attention, FFN & LayerNorm",
        "a_desc": "The original transformer architecture: input representation, scaled dot-product attention, multi-head attention, position-wise feed-forward networks, residual connections, and layer normalization.",
        "b_title": "Transformer Init, Causal Mask & Forward Pass",
        "b_desc": "Weight initialization, the causal mask for decoder-only models, the complete forward pass end to end, information flow through the residual stream, and parameter counting.",
        "a_suffix": "a",
        "b_suffix": "b",
        "b_intro_html": '<p>This continuation of <a href="section-3.1a.html">Section 3.1a</a> picks up after the structural elements of a single transformer block. It assembles those parts into a working decoder: how weights are initialized so signal flows cleanly, how the causal mask turns self-attention into autoregressive prediction, what the full forward pass looks like in code, and how to count parameters so you can predict memory before you allocate it.</p>',
        "a_next_href": "section-3.1b.html",
        "a_next_label": "Section 3.1b",
        "a_next_title": "Transformer Init, Causal Mask & Forward Pass",
        "b_prev_href": "section-3.1a.html",
        "b_prev_label": "Section 3.1a",
        "b_prev_title": "Transformer Anatomy: Attention, FFN & LayerNorm",
        "b_next_href": "section-3.2.html",
        "b_next_label": "Section 3.2",
        "b_next_title": "Encoder, Decoder, and Encoder-Decoder Architectures",
    },
    # 17.5 -> 17.5a (17.5.1 .. 17.5.5) + 17.5b (17.5.6 .. 17.5.8 + Exercises + What Comes Next)
    {
        "path": BOOK / "part-4-training-adaptation" / "module-17-peft" / "section-17.5.html",
        "break_line": 608,
        "a_title": "Knowledge Distillation: Foundations & Pipelines",
        "a_desc": "Classical and modern knowledge distillation: the teacher-student framework, white-box vs. black-box distillation, real-world LLM case studies, small-but-capable models, and the practical distillation pipeline.",
        "b_title": "Distillation: Licensing, Speculative & Reasoning",
        "b_desc": "Licensing and policy constraints on distillation, speculative distillation for inference acceleration, and reasoning-trace (chain-of-thought) distillation that transfers thinking patterns to smaller students.",
        "a_suffix": "a",
        "b_suffix": "b",
        "b_intro_html": '<p>This continuation of <a href="section-17.5a.html">Section 17.5a</a> picks up the practical distillation pipeline and extends it to three production-relevant topics: the licensing constraints that decide whether you are even allowed to distill from a given teacher, speculative distillation that uses a small student to accelerate inference of a large model, and reasoning-trace distillation that transfers chain-of-thought capability into a model that otherwise could not afford it.</p>',
        "a_next_href": "section-17.5b.html",
        "a_next_label": "Section 17.5b",
        "a_next_title": "Distillation: Licensing, Speculative & Reasoning",
        "b_prev_href": "section-17.5a.html",
        "b_prev_label": "Section 17.5a",
        "b_prev_title": "Knowledge Distillation: Foundations & Pipelines",
        "b_next_href": "section-17.6.html",
        "b_next_label": "Section 17.6",
        "b_next_title": "Adapter Methods and Modular Fine-Tuning",
    },
    # 32.1 -> 32.1a (32.1.0 .. 32.1.5) + 32.1b (32.1.6 .. 32.1.8 + Exercises + What Comes Next)
    {
        "path": BOOK / "part-7-retrieval-information-extraction-with-llms" / "module-32-rag" / "section-32.1.html",
        "break_line": 571,
        "a_title": "RAG Foundations: Pipeline & Why It Beats Fine-Tuning",
        "a_desc": "The retrieval-augmented generation pipeline: the knowledge-storage spectrum, why RAG, the ingestion pipeline, the retrieve-and-generate pattern, context window management, and when RAG beats fine-tuning.",
        "b_title": "RAG Indexing, Evaluation & Long-Context Tradeoff",
        "b_desc": "Indexing strategies for large corpora, evaluation and common failure modes for RAG systems, and how RAG compares to long-context windows now that models support 200K+ tokens.",
        "a_suffix": "a",
        "b_suffix": "b",
        "b_intro_html": '<p>This continuation of <a href="section-32.1a.html">Section 32.1a</a> moves from \"what RAG is\" to \"how to make RAG work in production.\" It covers the indexing choices you must make for large corpora, how to measure whether your RAG pipeline is actually retrieving the right things, and the practical comparison between RAG and the increasingly capable long-context windows of frontier models.</p>',
        "a_next_href": "section-32.1b.html",
        "a_next_label": "Section 32.1b",
        "a_next_title": "RAG Indexing, Evaluation & Long-Context Tradeoff",
        "b_prev_href": "section-32.1a.html",
        "b_prev_label": "Section 32.1a",
        "b_prev_title": "RAG Foundations: Pipeline & Why It Beats Fine-Tuning",
        "b_next_href": "section-32.2.html",
        "b_next_label": "Section 32.2",
        "b_next_title": "Vector Stores and Embedding Models in RAG",
    },
    # 35.5 -> 35.5a (35.5.1 .. 35.5.6) + 35.5b (35.5.8 .. 35.5.10 + Exercises + What Comes Next)
    {
        "path": BOOK / "part-7-retrieval-information-extraction-with-llms" / "module-35-advanced-rag" / "section-35.5.html",
        "break_line": 697,
        "a_title": "RAG Frameworks: LangChain, LlamaIndex & Haystack",
        "a_desc": "Why use a RAG framework, deep dives into LangChain, LlamaIndex, and Haystack, a side-by-side framework comparison, and when to use a framework vs. building from scratch.",
        "b_title": "RAG Production: DSPy, Hardening & Security",
        "b_desc": "Production considerations for RAG systems, compound AI systems with DSPy, and the runtime security threats specific to the retrieval layer (RAG poisoning, indirect prompt injection).",
        "a_suffix": "a",
        "b_suffix": "b",
        "b_intro_html": '<p>This continuation of <a href="section-35.5a.html">Section 35.5a</a> moves past framework selection into the engineering needed to run a RAG system in production. It covers the hardening checklist, the compound-AI shift represented by DSPy where you optimize the pipeline rather than the prompt, and the unique security threats of the retrieval layer that an off-the-shelf framework will not solve for you.</p>',
        "a_next_href": "section-35.5b.html",
        "a_next_label": "Section 35.5b",
        "a_next_title": "RAG Production: DSPy, Hardening & Security",
        "b_prev_href": "section-35.5a.html",
        "b_prev_label": "Section 35.5a",
        "b_prev_title": "RAG Frameworks: LangChain, LlamaIndex & Haystack",
        "b_next_href": "../module-36-retrieval-tools/index.html",
        "b_next_label": "Chapter 36",
        "b_next_title": "Retrieval Tools of the Trade",
    },
]


if __name__ == "__main__":
    import sys
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
