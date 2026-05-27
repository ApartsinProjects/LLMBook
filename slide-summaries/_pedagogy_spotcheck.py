"""Spot-check 50 named techniques across the book for pedagogy completeness."""
import re
from pathlib import Path

TARGET_NAMES = [
    'Toolformer', 'ToolkenGPT', 'Gorilla', 'ReWoo', 'RAPTOR', 'RAFT',
    'CAG', 'MMR', 'CLAP', 'BERTopic', 'MoE', 'Mixtral', 'LangGraph',
    'DPO', 'PPO', 'GRPO', 'LoRA', 'QLoRA', 'wav2vec', 'HuBERT',
    'EnCodec', 'SoundStream', 'AST', 'Whisper', 'CTC', 'Conformer',
    'TIGER', 'LLaRA', 'P5 ', 'SAM', 'NeRF', 'DETR', 'ImageGPT',
    'CLIP', 'SigLIP', 'BLIP', 'LLaVA', 'BERT ', 'RoBERTa', 'XLM',
    'mBERT', 'mT5', 'NLLB', 'Aya', 'RoPE', 'YaRN', 'FSDP', 'AdamW',
    'MCP', 'SimCSE', 'SBERT', 'SDAE', 'MTEB', 'SetFit', 'BPE',
    'Switch Transformer', 'Mamba', 'RetNet', 'GShard', 'VITS', 'Bark',
    'MusicGen', 'MusicLM', 'DPR', 'HyDE', 'GraphRAG',
]


def score_block(body: str) -> dict:
    has_fig = bool(re.search(r'<figure\b|<svg\b|diagram-container|class="[^"]*illustration', body, re.I))
    has_math = bool(re.search(r'\$\$[^$]+\$\$|\$[^$\n]{2,}\$', body))
    has_code = bool(re.search(r'<pre[^>]*><code[^>]*class="[^"]*language-(python|bash|json|yaml|c|rust|go)', body, re.I))
    has_example = bool(re.search(r'<div\s+class="[^"]*callout\s+(practical-example|numeric-example|key-insight|algorithm)', body, re.I))
    return {
        'fig': has_fig, 'math': has_math, 'code': has_code, 'ex': has_example,
        'score': sum([has_fig, has_math, has_code, has_example]),
    }


def main():
    root = Path('.')
    results = {}
    # For each target name, find its primary h2 or h3 section (first occurrence in any file)
    h_pattern = re.compile(r'<(h[23])\b[^>]*>(.*?)</\1>(.*?)(?=<h[23]\b|</main)', re.DOTALL | re.IGNORECASE)
    for path in root.glob('**/section-*.html'):
        if any(p in path.parts for p in ('_downloads', 'node_modules', '.book-update')):
            continue
        try:
            html = path.read_text(encoding='utf-8', errors='ignore')
        except Exception:
            continue
        for m in h_pattern.finditer(html):
            title_text = re.sub(r'<[^>]+>', '', m.group(2)).strip()
            body = m.group(3)
            for t in TARGET_NAMES:
                if t in title_text and t not in results:
                    score = score_block(body)
                    parts = list(path.parts)
                    loc = '/'.join(parts[-2:]) if len(parts) >= 2 else str(path)
                    score['title'] = title_text[:55]
                    score['file'] = loc
                    score['body_len'] = len(body)
                    results[t] = score

    print(f"{'Technique':30s} {'Score':6s} Fig Math Code Ex   Section")
    print("-" * 110)
    sorted_targets = sorted(TARGET_NAMES, key=lambda t: (results.get(t, {'score': -1})['score'], t))
    for t in sorted_targets:
        if t in results:
            r = results[t]
            f, m, c, e = ('Y' if r['fig'] else '.', 'Y' if r['math'] else '.',
                          'Y' if r['code'] else '.', 'Y' if r['ex'] else '.')
            star = ' *' if r['score'] <= 1 else '  '
            print(f"{star}{t:28s} {r['score']}/4    {f}   {m}    {c}    {e}    {r['file']}")
        else:
            print(f"  {t:28s}  NOT FOUND in any h2/h3 title")


if __name__ == '__main__':
    main()
