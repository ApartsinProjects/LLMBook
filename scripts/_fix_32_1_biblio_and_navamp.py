"""
Fix two issues that the split script missed:
1) section-32.1a and section-32.1b have no bibliography (the original 32.1 used
   <details class="bibliography-collapsible" open=""> with an open attribute, which
   the splitter regex did not match).
2) Unescaped & in nav-title of newly-generated chapter-nav blocks across all 10
   new section files.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BOOK = ROOT.parent

BIBLIO_32_1 = """<details class="bibliography-collapsible">
<summary><strong>Further Reading</strong></summary>
<section class="bibliography">
<div class="bib-entry-card">
<div class="bib-ref"><a href="https://arxiv.org/abs/2005.11401" rel="noopener" target="_blank">Lewis, P. et al. (2020). "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks." <em>NeurIPS 2020</em>.</a> The foundational RAG paper that introduced the retrieve-then-generate paradigm. Useful for understanding how retrieval and generation components interact. Start here if you are new to RAG.</div>
</div>
<div class="bib-entry-card">
<div class="bib-ref"><a href="https://arxiv.org/abs/2312.10997" rel="noopener" target="_blank">Gao, Y. et al. (2024). "Retrieval-Augmented Generation for Large Language Models: A Survey." <em>arXiv preprint</em>.</a> A comprehensive survey covering RAG taxonomies, techniques, and evaluation methods. Provides an excellent map of the RAG landscape as of 2024. Ideal for practitioners seeking a broad overview.</div>
</div>
<div class="bib-entry-card">
<div class="bib-ref"><a href="https://arxiv.org/abs/2302.00083" rel="noopener" target="_blank">Ram, O. et al. (2023). "In-Context Retrieval-Augmented Language Models." <em>TACL</em>.</a> Explores how retrieval can be integrated into <a href="../../part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.7.html">in-context learning</a> without fine-tuning. Demonstrates strong performance on knowledge-intensive tasks. Recommended for researchers studying <a href="../../part-3-working-with-llms/module-12-prompt-engineering/section-12.2.html">zero-shot</a> RAG.</div>
</div>
<div class="bib-entry-card">
<div class="bib-ref"><a href="https://arxiv.org/abs/2309.15217" rel="noopener" target="_blank">Es, S. et al. (2024). "RAGAs: Automated Evaluation of Retrieval Augmented Generation." <em>arXiv preprint</em>.</a> Introduces automated metrics for evaluating RAG pipelines, including faithfulness and answer relevancy. A practical framework that has become the standard for RAG evaluation. Must-read for anyone building production RAG.</div>
</div>
<div class="bib-entry-card">
<div class="bib-ref"><a href="https://python.langchain.com/docs/tutorials/rag/" rel="noopener" target="_blank">LangChain RAG Tutorial.</a> Official tutorial covering end-to-end RAG implementation with LangChain. Includes code examples for document loading, chunking, and retrieval. Best starting point for hands-on RAG development.</div>
</div>
<div class="bib-entry-card">
<div class="bib-ref"><a href="https://docs.llamaindex.ai/en/stable/" rel="noopener" target="_blank">LlamaIndex: Build RAG Applications.</a> Comprehensive documentation for the LlamaIndex framework with a focus on data ingestion and indexing. Offers advanced features like query engines and response synthesizers. Recommended for complex RAG architectures.</div>
</div>
</section>
</details>
"""

paths_for_biblio = [
    BOOK / "part-7-retrieval-information-extraction-with-llms" / "module-32-rag" / "section-32.1a.html",
    BOOK / "part-7-retrieval-information-extraction-with-llms" / "module-32-rag" / "section-32.1b.html",
]


def insert_biblio(p: Path, biblio_html: str):
    text = p.read_text(encoding="utf-8")
    if "bibliography-collapsible" in text:
        return False
    # Insert just before the <nav class="chapter-nav"> block
    anchor = '<nav class="chapter-nav">'
    if anchor in text:
        text = text.replace(anchor, biblio_html + anchor, 1)
        p.write_text(text, encoding="utf-8")
        return True
    return False


def fix_navamp(p: Path) -> bool:
    """Replace bare & with &amp; inside nav-title spans."""
    text = p.read_text(encoding="utf-8")
    orig = text

    def repl(m):
        inner = m.group(1)
        new_inner = re.sub(r'&(?!(amp;|lt;|gt;|quot;|#))', '&amp;', inner)
        return f'<span class="nav-title">{new_inner}</span>'

    text = re.sub(r'<span class="nav-title">([^<]*?)</span>', repl, text)
    if text != orig:
        p.write_text(text, encoding="utf-8")
        return True
    return False


if __name__ == "__main__":
    print("Inserting bibliography into 32.1 splits...")
    for p in paths_for_biblio:
        ok = insert_biblio(p, BIBLIO_32_1)
        print(f"  {'OK' if ok else 'SKIP'}: {p.name}")

    print()
    print("Escaping & in nav-title text for all new section files...")
    new_files = [
        BOOK / "part-1-llm-building-blocks" / "module-00-ml-pytorch-foundations" / "section-0.3a.html",
        BOOK / "part-1-llm-building-blocks" / "module-00-ml-pytorch-foundations" / "section-0.3b.html",
        BOOK / "part-1-llm-building-blocks" / "module-03-transformer-architecture" / "section-3.1a.html",
        BOOK / "part-1-llm-building-blocks" / "module-03-transformer-architecture" / "section-3.1b.html",
        BOOK / "part-4-training-adaptation" / "module-17-peft" / "section-17.5a.html",
        BOOK / "part-4-training-adaptation" / "module-17-peft" / "section-17.5b.html",
        BOOK / "part-7-retrieval-information-extraction-with-llms" / "module-32-rag" / "section-32.1a.html",
        BOOK / "part-7-retrieval-information-extraction-with-llms" / "module-32-rag" / "section-32.1b.html",
        BOOK / "part-7-retrieval-information-extraction-with-llms" / "module-35-advanced-rag" / "section-35.5a.html",
        BOOK / "part-7-retrieval-information-extraction-with-llms" / "module-35-advanced-rag" / "section-35.5b.html",
    ]
    for p in new_files:
        ok = fix_navamp(p)
        print(f"  {'OK' if ok else 'NO CHANGE'}: {p.name}")
