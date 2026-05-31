"""Extract raw python source for all 21 targets and save to frag_NN.py.
Also dumps a manifest mapping NN -> (file, line).
"""
from __future__ import annotations
import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from extract_block import find_block, spans_to_text

ROOT = Path("E:/Projects/BookBlogsHome/LLMBook")
WORK = Path(__file__).parent

TARGETS = [
    ("part-1-llm-building-blocks/module-01-foundations-nlp-text-representation/section-1.8.html", 190),
    ("part-3-working-with-llms/module-13-hybrid-ml-llm/section-13.4.html", 444),
    ("part-4-training-adaptation/module-15-synthetic-data/section-15.3.html", 167),
    ("part-4-training-adaptation/module-16-fine-tuning-fundamentals/section-16.7.html", 326),
    ("part-4-training-adaptation/module-18-alignment-rlhf-dpo/section-18.1.html", 461),
    ("part-4-training-adaptation/module-18-alignment-rlhf-dpo/section-18.6.html", 143),
    ("part-7-retrieval-information-extraction-with-llms/module-31-embeddings-vector-db/section-31.7.html", 68),
    ("part-7-retrieval-information-extraction-with-llms/module-31-embeddings-vector-db/section-31.8.html", 383),
    ("part-8-conversational-ai-with-llms/module-37-conversational-ai/section-37.1.html", 668),
    ("part-8-conversational-ai-with-llms/module-37-conversational-ai/section-37.2.html", 298),
    ("part-8-conversational-ai-with-llms/module-37-conversational-ai/section-37.4.html", 70),
    ("part-8-conversational-ai-with-llms/module-37-conversational-ai/section-37.4.html", 265),
    ("part-8-conversational-ai-with-llms/module-37-conversational-ai/section-37.5.html", 269),
    ("part-9-llm-evaluation-observability/module-42-evaluation-foundations/section-42.2.html", 634),
    ("part-9-llm-evaluation-observability/module-42-evaluation-foundations/section-42.5.html", 142),
    ("part-9-llm-evaluation-observability/module-42-evaluation-foundations/section-42.5.html", 281),
    ("part-9-llm-evaluation-observability/module-42-evaluation-foundations/section-42.5.html", 362),
    ("part-13-llmops-lifecycle/module-66-reliability-slos-registry/section-66.1.html", 159),
    ("part-13-llmops-lifecycle/module-66-reliability-slos-registry/section-66.1.html", 395),
    ("part-13-llmops-lifecycle/module-66-reliability-slos-registry/section-66.1.html", 573),
    ("part-13-llmops-lifecycle/module-66-reliability-slos-registry/section-66.1.html", 703),
]


def main() -> None:
    manifest_lines = []
    for i, (relpath, line) in enumerate(TARGETS, 1):
        path = ROOT / relpath
        text = path.read_text(encoding="utf-8")
        s, e, inner = find_block(text, line)
        raw = spans_to_text(inner)
        # Save raw with a comment header
        outpath = WORK / f"frag_{i:02d}.py"
        outpath.write_text(raw, encoding="utf-8")
        manifest_lines.append(f"{i:02d}\t{relpath}\t{line}\t{s}\t{e}")
        print(f"  frag_{i:02d}.py  ({len(raw)} bytes)  {relpath}:{line}")
    (WORK / "MANIFEST.tsv").write_text("\n".join(manifest_lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
