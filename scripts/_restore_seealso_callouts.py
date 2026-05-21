"""
Restore See Also (callout cross-ref) blocks that originally sat AFTER whats-next
and before the bibliography in the source giant section. The split script ate
them. Re-insert them in the appropriate b file's tail.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BOOK = ROOT.parent

restorations = [
    # 17.5b - restore the See Also callout
    {
        "path": BOOK / "part-4-training-adaptation" / "module-17-peft" / "section-17.5b.html",
        "anchor": '<details class="bibliography-collapsible">',
        "insert_before": '<div class="callout cross-ref">\n<div class="callout-title">See Also</div>\n<p>For the reasoning-model architectures (o1, o3, R1, QwQ) whose chain-of-thought is the dominant 2024-26 distillation target, see <a href="../../part-2-understanding-llms/module-08-reasoning-test-time-compute/section-8.2.html">Section 8.2: Reasoning Model Architectures</a>. For the synthetic-reasoning-data generation pipelines that feed reasoning distillation, see <a href="../module-15-synthetic-data/section-15.6.html">Section 15.6: Synthetic Reasoning Data</a>. For the post-distillation evaluation suite (faithfulness, refusal calibration, contamination checks), see <a href="../../part-9-llm-evaluation-observability/module-42-evaluation-foundations/section-42.1.html">Section 42.1: LLM Evaluation Fundamentals</a>.</p>\n</div>\n',
    },
    # 35.5b - restore the See Also callout
    {
        "path": BOOK / "part-7-retrieval-information-extraction-with-llms" / "module-35-advanced-rag" / "section-35.5b.html",
        "anchor": '<details class="bibliography-collapsible">',
        "insert_before": '<div class="callout cross-ref">\n<div class="callout-title">See Also</div>\n<p>For the orchestration-framework comparison (LangChain, LlamaIndex, Haystack, DSPy) referenced here, see <a href="../module-36-retrieval-tools/section-36.2.html">Section 36.2: Libraries and Frameworks</a>. For the production-side workflow orchestration (Temporal, Inngest, LangGraph persistence) that RAG frameworks live inside, see <a href="../../part-13-llmops-lifecycle/module-64-workflow-orchestration/section-64.1.html">Section 64.1: Workflow Orchestration and Durable Execution</a>. For the agentic-RAG variants where the orchestrator becomes an agent loop, see <a href="../module-32-rag/section-32.2.html">Section 32.2: Deep Research and Agentic RAG</a>.</p>\n</div>\n',
    },
]


def apply(fix):
    p = Path(fix["path"])
    text = p.read_text(encoding="utf-8")
    if fix["anchor"] in text and fix["insert_before"] not in text:
        text = text.replace(fix["anchor"], fix["insert_before"] + fix["anchor"], 1)
        p.write_text(text, encoding="utf-8")
        return True
    return False


if __name__ == "__main__":
    for fix in restorations:
        ok = apply(fix)
        print(("OK" if ok else "MISS"), fix["path"])
