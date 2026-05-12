"""v6.31: Replace generic 'Chapter illustration' captions with descriptive ones."""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

# Per-appendix descriptive caption + alt text
CAPTIONS = {
    'appendix-k-huggingface-ecosystem': (
        'A friendly cartoon ecosystem of small models, datasets, and spaces clustered around the HuggingFace logo, with arrows showing how Transformers, Datasets, Tokenizers, and Hub libraries plug together.',
        'The HuggingFace ecosystem at a glance: Transformers, Datasets, Tokenizers, Hub, and Spaces compose into a single Python-first toolchain for shipping LLM applications.',
    ),
    'appendix-l-langchain': (
        'A whimsical chain made of interlocking links labeled "Prompt", "LLM", "Tool", "Memory", and "Agent", winding through a developer\'s workshop.',
        'LangChain composes prompts, models, tools, memory, and agents into chains and graphs. The same primitives appear under different names in LangGraph, LlamaIndex, CrewAI, and DSPy.',
    ),
    'appendix-r-experiment-tracking': (
        'A scientist\'s lab bench covered with notebooks, charts, version-tagged bottles, and a glowing dashboard tracking every training run.',
        'Experiment tracking turns ad-hoc training runs into a searchable, reproducible record. MLflow, Weights & Biases, and CometML all share the same core abstractions: experiments, runs, params, metrics, and artifacts.',
    ),
    'appendix-s-inference-serving': (
        'A factory floor where prompts arrive on a conveyor belt and exit as token streams, with workers labeled "vLLM", "TGI", "Triton", and "TensorRT-LLM" tending the machines.',
        'Inference serving is the layer between a trained model and a production request. vLLM, TGI, Triton, and TensorRT-LLM each optimize a different slice of the latency-throughput-cost frontier.',
    ),
    'appendix-t-distributed-ml': (
        'A small village of GPU "houses" connected by glowing cables, exchanging gradient packets through routers labeled "Allreduce", "Pipeline", and "ZeRO".',
        'Distributed ML coordinates many GPUs to train models too large for one device. The strategy zoo (DDP, FSDP, ZeRO, pipeline, tensor, expert, sequence) maps onto a few orthogonal partitioning choices: data, parameters, activations, and experts.',
    ),
    'appendix-u-docker-containers': (
        'A friendly stack of shipping containers loaded onto a cargo ship, each container holding a Python environment, model weights, and a "ship it" tag.',
        'Containers package an LLM application with its exact runtime so the same artifact runs on a laptop, a CI machine, and a production cluster. Docker plus a few patterns (multi-stage builds, volume mounts, GPU passthrough) covers most LLM-deployment needs.',
    ),
    'appendix-v-tooling-ecosystem': (
        'A bustling marketplace of small tool stalls labeled "vector DB", "agent framework", "evaluation harness", "fine-tuning runner", and "observability", with shoppers comparing offerings.',
        'The 2026 LLM tooling landscape. This appendix maps the categories, the leading projects in each, and how to choose between them for a real project.',
    ),
}


def main() -> int:
    fixed = 0
    for slug, (alt, cap) in CAPTIONS.items():
        p = ROOT / 'appendices' / slug / 'index.html'
        if not p.exists():
            print(f'SKIP (not found): {p}')
            continue
        text = p.read_text(encoding='utf-8')
        original = text
        # Replace alt text
        text = re.sub(
            r'(<img[^>]+src="[^"]*chapter-opener[^"]*"[^>]+alt=")Chapter illustration(")',
            lambda m: m.group(1) + alt.replace('"', '&quot;') + m.group(2),
            text,
        )
        # Replace figcaption
        text = re.sub(
            r'(<figcaption[^>]*><strong>Figure [A-Z]\.0\.1</strong>): Chapter illustration\.',
            lambda m: m.group(1) + ': ' + cap,
            text,
        )
        if text != original:
            p.write_text(text, encoding='utf-8')
            fixed += 1
            print(f'  fixed: appendices/{slug}/index.html')
    print(f'\nFixed {fixed} appendix opener captions.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
