"""
Fix up the awkward 'What's Next' on the A files; the auto-generated text starts with
'pytorch tensors, autograd...' because we lowercased the description. Rewrite each
A's whats-next to flow naturally.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BOOK = ROOT.parent

fixes = [
    # 0.3a -> next is 0.3b
    {
        "path": BOOK / "part-1-llm-building-blocks" / "module-00-ml-pytorch-foundations" / "section-0.3a.html",
        "old": '<p>In the next part of this section, <a href="section-0.3b.html">Section 0.3b: PyTorch Debugging, Lab & Modern Performance</a>, pytorch tensors, autograd, building models with nn.module, data loading, the basic training loop, and saving/loading model state.</p>',
        "new": '<p>In the next part of this section, <a href="section-0.3b.html">Section 0.3b: PyTorch Debugging, Lab &amp; Modern Performance</a>, we move from "the model runs" to "the model runs <em>well</em>": debugging tools (hooks, gradient inspection, profiler), common mistakes that silently produce wrong results, a hands-on FashionMNIST classifier lab, and the modern PyTorch features (<code>torch.compile</code>, mixed precision, distributed training) that make it fast.</p>',
    },
    {
        "path": BOOK / "part-1-llm-building-blocks" / "module-03-transformer-architecture" / "section-3.1a.html",
        "old": '<p>In the next part of this section, <a href="section-3.1b.html">Section 3.1b: Transformer Init, Causal Mask & Forward Pass</a>, the original transformer architecture: input representation, scaled dot-product attention, multi-head attention, position-wise feed-forward networks, residual connections, and layer normalization.</p>',
        "new": '<p>In the next part of this section, <a href="section-3.1b.html">Section 3.1b: Transformer Init, Causal Mask &amp; Forward Pass</a>, we assemble the components into a working decoder: how to initialize weights so signal flows cleanly through many layers, how the causal mask makes self-attention autoregressive, what the complete forward pass looks like in code, and how to count parameters for a given architecture.</p>',
    },
    {
        "path": BOOK / "part-4-training-adaptation" / "module-17-peft" / "section-17.5a.html",
        "old": '<p>In the next part of this section, <a href="section-17.5b.html">Section 17.5b: Distillation: Licensing, Speculative & Reasoning</a>, classical and modern knowledge distillation: the teacher-student framework, white-box vs. black-box distillation, real-world llm case studies, small-but-capable models, and the practical distillation pipeline.</p>',
        "new": '<p>In the next part of this section, <a href="section-17.5b.html">Section 17.5b: Distillation: Licensing, Speculative &amp; Reasoning</a>, we step beyond the basic pipeline to three production-relevant topics: the provider licensing terms that determine whether you may distill at all, speculative distillation as an inference-time accelerator, and chain-of-thought distillation that transfers reasoning capability into smaller students.</p>',
    },
    {
        "path": BOOK / "part-7-retrieval-information-extraction-with-llms" / "module-32-rag" / "section-32.1a.html",
        "old": '<p>In the next part of this section, <a href="section-32.1b.html">Section 32.1b: RAG Indexing, Evaluation & Long-Context Tradeoff</a>, the retrieval-augmented generation pipeline: the knowledge-storage spectrum, why rag, the ingestion pipeline, the retrieve-and-generate pattern, context window management, and when rag beats fine-tuning.</p>',
        "new": '<p>In the next part of this section, <a href="section-32.1b.html">Section 32.1b: RAG Indexing, Evaluation &amp; Long-Context Tradeoff</a>, we shift from "what RAG is" to "how to operate RAG at scale": indexing strategies for large corpora, evaluation and common failure modes, and how RAG compares to long-context windows now that frontier models offer 200K+ tokens.</p>',
    },
    {
        "path": BOOK / "part-7-retrieval-information-extraction-with-llms" / "module-35-advanced-rag" / "section-35.5a.html",
        "old": '<p>In the next part of this section, <a href="section-35.5b.html">Section 35.5b: RAG Production: DSPy, Hardening & Security</a>, why use a rag framework, deep dives into langchain, llamaindex, and haystack, a side-by-side framework comparison, and when to use a framework vs. building from scratch.</p>',
        "new": '<p>In the next part of this section, <a href="section-35.5b.html">Section 35.5b: RAG Production: DSPy, Hardening &amp; Security</a>, we move from framework selection to running a RAG system in production: the hardening checklist, the compound-AI shift represented by DSPy (optimize the pipeline, not the prompt), and the retrieval-layer security threats (RAG poisoning, indirect prompt injection) that no framework will solve for you.</p>',
    },
]

# Also fix the B whats-next which says "we continue building on the topics covered here." Reword per file.
b_fixes = [
    {
        "path": BOOK / "part-1-llm-building-blocks" / "module-00-ml-pytorch-foundations" / "section-0.3b.html",
        "old": '<p>In the next section, <a href="section-0.4.html">Section 0.4: Reinforcement Learning Foundations</a>, we continue building on the topics covered here.</p>',
        "new": '<p>In the next section, <a href="section-0.4.html">Section 0.4: Reinforcement Learning Foundations</a>, we introduce reinforcement learning foundations, which will become essential when we study RLHF and alignment techniques later in the book.</p>',
    },
    {
        "path": BOOK / "part-1-llm-building-blocks" / "module-03-transformer-architecture" / "section-3.1b.html",
        "old": '<p>In the next section, <a href="section-3.2.html">Section 3.2: Encoder, Decoder, and Encoder-Decoder Architectures</a>, we continue building on the topics covered here.</p>',
        "new": '<p>In the next section, <a href="section-3.2.html">Section 3.2: Encoder, Decoder, and Encoder-Decoder Architectures</a>, we generalize from the single decoder block built here to the three architectural families (encoder-only, decoder-only, encoder-decoder) and what each is good at.</p>',
    },
    {
        "path": BOOK / "part-4-training-adaptation" / "module-17-peft" / "section-17.5b.html",
        "old": '<p>In the next section, <a href="section-17.6.html">Section 17.6: Adapter Methods and Modular Fine-Tuning</a>, we continue building on the topics covered here.</p>',
        "new": '<p>In the next section, <a href="section-17.6.html">Section 17.6: Adapter Methods and Modular Fine-Tuning</a>, we return to parameter-efficient methods, this time focusing on adapter layers and how multiple adapters can compose into a modular, task-routed model.</p>',
    },
    {
        "path": BOOK / "part-7-retrieval-information-extraction-with-llms" / "module-32-rag" / "section-32.1b.html",
        "old": '<p>In the next section, <a href="section-32.2.html">Section 32.2: Vector Stores and Embedding Models in RAG</a>, we continue building on the topics covered here.</p>',
        "new": '<p>In the next section, <a href="section-32.2.html">Section 32.2: Vector Stores and Embedding Models in RAG</a>, we go a layer deeper into the retrieval stack: how vector stores actually index embeddings, which embedding models you should pick for which corpus, and how their interaction sets the ceiling on RAG quality.</p>',
    },
    {
        "path": BOOK / "part-7-retrieval-information-extraction-with-llms" / "module-35-advanced-rag" / "section-35.5b.html",
        "old": '<p>In the next section, <a href="../module-36-retrieval-tools/index.html">Chapter 36: Retrieval Tools of the Trade</a>, we continue building on the topics covered here.</p>',
        "new": '<p>In the next chapter, <a href="../module-36-retrieval-tools/index.html">Chapter 36: Retrieval Tools of the Trade</a>, we move from framework-level RAG to the individual tools that make up a production retrieval stack: vector databases, embedding services, reranker APIs, and the orchestrators that glue them together.</p>',
    },
]


def apply(fix):
    p = Path(fix["path"])
    text = p.read_text(encoding="utf-8")
    if fix["old"] in text:
        text = text.replace(fix["old"], fix["new"])
        p.write_text(text, encoding="utf-8")
        return True
    return False


if __name__ == "__main__":
    for fix in fixes + b_fixes:
        ok = apply(fix)
        print(("OK" if ok else "MISS"), fix["path"])
