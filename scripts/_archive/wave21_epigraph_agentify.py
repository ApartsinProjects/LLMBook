"""Wave 21: convert non-AI-agent epigraphs to the canonical AI-agent style.

Canonical epigraph format:
  <blockquote class="epigraph">
  <p>"quote"</p>
  <span class="agent-avatar-inline" style="background-color: #COLOR;"><img alt="AgentName" height="28" src="REL_PATH/agents/SLUG.png" width="28"/></span><cite>AgentName, <span class="agent-desc">Trait AI Agent</span></cite>
  </blockquote>

The audit found 66 violations. For each, we:
  1. Keep the existing quote text (rewrap in proper <p> if needed)
  2. Replace the cite block with the canonical agent attribution
  3. Use the canonical agent + color from the rest of the book
"""
from pathlib import Path
import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]

# Canonical color per agent (from existing book usage)
AGENT_COLORS = {
    'Tensor': '#3498db', 'Lexica': '#9b59b6', 'Token': '#d35400',
    'Attn': '#e94560', 'Norm': '#95a5a6', 'Sage': '#7f8c8d',
    'Pip': '#3498db', 'Chinchilla': '#8e44ad', 'Spectra': '#3498db',
    'Bert': '#f39c12', 'Greedy': '#27ae60', 'Quant': '#1abc9c',
    'KV': '#16a085', 'Probe': '#34495e', 'Prompt': '#16a085',
    'Synth': '#f1c40f', 'Finetune': '#27ae60', 'LoRA': '#27ae60',
    'Reward': '#2ecc71', 'Distill': '#1abc9c', 'Pixel': '#1abc9c',
    'Vec': '#8e44ad', 'RAG': '#2980b9', 'Echo': '#f39c12',
    'Compass': '#34495e', 'Census': '#9b59b6', 'Label': '#d35400',
    'Eval': '#7f8c8d', 'Sentinel': '#e67e22', 'Guard': '#c0392b',
    'Scale': '#2c3e50', 'Deploy': '#2c3e50', 'Frontier': '#e94560',
}

# Per-file agent assignment + trait. (agent, personality, quote_override_or_None)
# Path is relative to repo root, with forward slashes.
ASSIGNMENTS = {
    'appendices/index.html': ('Sage', 'Reference-Hoarding'),
    'capstone/index.html': ('Sage', 'Newly-Graduated'),
    'part-1-llm-building-blocks/module-05-tools-of-the-trade/index.html': ('Pip', 'Toolbox-Curating'),
    'part-2-understanding-llms/module-09-inference-optimization/index.html': ('Quant', 'Bandwidth-Conscious'),
    'part-3-working-with-llms/index.html': ('Pip', 'Practically-Minded'),
    'part-3-working-with-llms/module-12-prompt-engineering/index.html': ('Prompt', 'Verbally-Persuasive'),
    'part-4-training-adaptation/index.html': ('Finetune', 'Gradient-Loving'),
    'part-4-training-adaptation/module-15-synthetic-data/index.html': ('Synth', 'Self-Generating'),
    'part-4-training-adaptation/module-19-tools-of-the-trade/index.html': ('Pip', 'Workflow-Optimizing'),
    'part-5-multimodal-llms/module-20-audio-music-generation/section-20.1.html': ('Echo', 'Pitch-Perfect'),
    'part-5-multimodal-llms/module-20-audio-music-generation/section-20.2.html': ('Echo', 'Voice-Curious'),
    'part-5-multimodal-llms/module-20-audio-music-generation/section-20.3.html': ('Echo', 'Melodically-Inclined'),
    'part-5-multimodal-llms/module-20-audio-music-generation/section-20.4.html': ('Echo', 'Audio-Editing'),
    'part-5-multimodal-llms/module-20-audio-music-generation/section-20.5.html': ('Echo', 'Transcription-Eager'),
    'part-5-multimodal-llms/module-20-audio-music-generation/section-20.6.html': ('Pixel', 'Frame-Diffusing'),
    'part-5-multimodal-llms/module-20-audio-music-generation/section-20.7.html': ('Pixel', 'Sora-Watching'),
    'part-5-multimodal-llms/module-20-audio-music-generation/section-20.8.html': ('Pixel', 'Camera-Controlling'),
    'part-5-multimodal-llms/module-20-audio-music-generation/section-20.9.html': ('Pixel', 'Cut-Loving'),
    'part-5-multimodal-llms/module-20-audio-music-generation/section-20.10.html': ('Pixel', 'Cinematically-Ambitious'),
    'part-5-multimodal-llms/module-22-vision-language-models/section-22.6.html': ('Pixel', 'Pipeline-Skeptical'),
    'part-5-multimodal-llms/module-22-vision-language-models/section-22.7.html': ('Pixel', 'Fusion-Curious'),
    'part-5-multimodal-llms/module-22-vision-language-models/section-22.8.html': ('Pixel', 'Any-To-Any'),
    'part-5-multimodal-llms/module-22-vision-language-models/section-22.9.html': ('Pixel', 'Omni-Aspirational'),
    'part-5-multimodal-llms/module-23-3d-generation-neural-scenes/section-23.1.html': ('Pixel', 'Splat-Curious'),
    'part-5-multimodal-llms/module-23-3d-generation-neural-scenes/section-23.2.html': ('Pixel', 'Four-Dimensional'),
    'part-5-multimodal-llms/module-23-3d-generation-neural-scenes/section-23.3.html': ('Pixel', 'Image-To-3D'),
    'part-5-multimodal-llms/module-23-3d-generation-neural-scenes/section-23.4.html': ('Pixel', 'Trellis-Trained'),
    'part-5-multimodal-llms/module-23-3d-generation-neural-scenes/section-23.5.html': ('Pixel', 'Relighting-Obsessed'),
    'part-5-multimodal-llms/module-25-tools-of-the-trade/index.html': ('Pip', 'Multimodal-Outfitted'),
    'part-6-agentic-ai/index.html': ('Compass', 'Goal-Seeking'),
    'part-6-agentic-ai/module-27-tool-use-protocols/index.html': ('Pip', 'Tool-Calling'),
    'part-6-agentic-ai/module-28-multi-agent-systems/index.html': ('Echo', 'Co-Operative'),
    'part-6-agentic-ai/module-30-tools-of-the-trade/index.html': ('Pip', 'Stack-Building'),
    'part-7-retrieval-information-extraction-with-llms/module-32-rag/index.html': ('RAG', 'Bookishly-Wise'),
    'part-7-retrieval-information-extraction-with-llms/module-33-cross-modal-reasoning-rag/section-33.1.html': ('RAG', 'Cross-Modal-Curious'),
    'part-7-retrieval-information-extraction-with-llms/module-33-cross-modal-reasoning-rag/section-33.2.html': ('RAG', 'Multimodally-Indexed'),
    'part-7-retrieval-information-extraction-with-llms/module-33-cross-modal-reasoning-rag/section-33.3.html': ('RAG', 'Retrieval-Reasoning'),
    'part-7-retrieval-information-extraction-with-llms/module-33-cross-modal-reasoning-rag/section-33.4.html': ('RAG', 'Production-Tested'),
    'part-8-conversational-ai-with-llms/module-40-voice-realtime-multimodal/section-40.2.html': ('Echo', 'Streaming-Live'),
    'part-8-conversational-ai-with-llms/module-40-voice-realtime-multimodal/section-40.3.html': ('Echo', 'Realtime-Wrangling'),
    'part-8-conversational-ai-with-llms/module-40-voice-realtime-multimodal/section-40.4.html': ('Echo', 'Latency-Allergic'),
    'part-8-conversational-ai-with-llms/module-40-voice-realtime-multimodal/section-40.5.html': ('Echo', 'Open-Realtime'),
    'part-9-llm-evaluation-observability/index.html': ('Eval', 'Chronically-Skeptical'),
    'part-9-llm-evaluation-observability/module-42-evaluation-foundations/index.html': ('Eval', 'Chronically-Skeptical'),
    'part-9-llm-evaluation-observability/module-42-evaluation-foundations/section-42.9.html': ('Eval', 'Trace-Sniffing'),
    'part-9-llm-evaluation-observability/module-44-online-eval-observability/section-44.4.html': ('Deploy', 'Perpetually-Shipping'),
    'part-9-llm-evaluation-observability/module-45-tools-of-the-trade/index.html': ('Eval', 'Spec-First'),
    'part-10-llm-security-runtime-safety/module-47-adversarial-security-red-team/index.html': ('Guard', 'Red-Team-Ready'),
    'part-10-llm-security-runtime-safety/module-51-tools-of-the-trade/index.html': ('Guard', 'Defense-In-Depth'),
    'part-11-llm-ethics-trust-governance/module-52-bias-fairness/index.html': ('Census', 'Fairness-Forward'),
    'part-11-llm-ethics-trust-governance/module-55-environmental-sustainability/index.html': ('Compass', 'Carbon-Aware'),
    'part-12-llm-systems-at-scale/module-58-frontier-systems-hardware/index.html': ('Frontier', 'Silicon-Curious'),
    'part-12-llm-systems-at-scale/module-60-edge-on-device-llms/section-60.1.html': ('Quant', 'Edge-Squeezing'),
    'part-13-llmops-lifecycle/module-63-ai-gateways-routing/section-63.1.html': ('Deploy', 'Gateway-Guarding'),
    'part-13-llmops-lifecycle/module-64-workflow-orchestration/section-64.1.html': ('Deploy', 'Workflow-Watching'),
    'part-14-designing-llm-agent-products/module-67-ideation/section-67.1.html': ('Sage', 'Idea-Vetting'),
    'part-14-designing-llm-agent-products/module-67-ideation/section-67.4.html': ('Sage', 'Spec-Writing'),
    'part-14-designing-llm-agent-products/module-68-vibe-coding/section-68.1.html': ('Pip', 'Vibe-Coding'),
    'part-14-designing-llm-agent-products/module-68-vibe-coding/section-68.4.html': ('Pip', 'MVP-Shipping'),
    'part-14-designing-llm-agent-products/module-71-tools-of-the-trade/index.html': ('Pip', 'Product-Building'),
    'part-15-applications-of-llms-across-industries/index.html': ('Compass', 'Industry-Tracking'),
    'part-15-applications-of-llms-across-industries/module-79-tools-of-the-trade/index.html': ('Pip', 'Vertical-Specializing'),
    'part-16-llm-agentic-ai-research-frontiers/index.html': ('Frontier', 'Frontier-Watching'),
    'part-16-llm-agentic-ai-research-frontiers/module-81-frontier-theory/index.html': ('Frontier', 'Theoretically-Inclined'),
    'part-16-llm-agentic-ai-research-frontiers/module-82-agi-trajectories/index.html': ('Frontier', 'AGI-Forecasting'),
    'part-16-llm-agentic-ai-research-frontiers/module-83-tools-of-the-trade/index.html': ('Frontier', 'Pre-Print-Reading'),
}


def depth_to_root(rel_path: str) -> str:
    """Calculate the path prefix from a file at rel_path back to the repo root."""
    # rel_path is like 'part-9-.../module-42-.../section-42.1.html'
    parts = rel_path.split('/')
    depth = len(parts) - 1  # number of dirs above file
    return '../' * depth


def build_agent_block(agent: str, personality: str, rel_path: str) -> str:
    """Build the canonical avatar + cite block for an agent."""
    color = AGENT_COLORS.get(agent, '#7f8c8d')
    slug = agent.lower()
    # Image lives at front-matter/images/agents/SLUG.png; compute relative path
    if rel_path.startswith('front-matter/'):
        img_src = f'images/agents/{slug}.png'
    else:
        prefix = depth_to_root(rel_path)
        img_src = f'{prefix}front-matter/images/agents/{slug}.png'
    return (
        f'<span class="agent-avatar-inline" style="background-color: {color};">'
        f'<img alt="{agent}" height="28" src="{img_src}" width="28"/></span>'
        f'<cite>{agent}, <span class="agent-desc">{personality} AI Agent</span></cite>'
    )


def fix_epigraph_block(epigraph_html: str, agent_block: str) -> str:
    """Replace whatever's between the quote <p> and the </blockquote> with the
    proper agent block."""
    # Find the first <p>...</p>
    p_m = re.search(r'(<p>[\s\S]*?</p>)', epigraph_html)
    if not p_m:
        return None
    quote_p = p_m.group(1)
    return f'{quote_p}\n{agent_block}'


def main():
    n_fixed = 0
    n_missing = 0
    for rel, (agent, personality) in ASSIGNMENTS.items():
        p = ROOT / rel
        if not p.exists():
            print(f'  MISSING: {rel}')
            n_missing += 1
            continue
        text = p.read_text(encoding='utf-8')
        m = re.search(r'(<blockquote class="epigraph">)([\s\S]*?)(</blockquote>)', text)
        if not m:
            print(f'  no epigraph found: {rel}')
            n_missing += 1
            continue
        old_inner = m.group(2)
        agent_block = build_agent_block(agent, personality, rel)
        new_inner = fix_epigraph_block(old_inner, agent_block)
        if not new_inner:
            print(f'  no <p> in epigraph: {rel}')
            n_missing += 1
            continue
        new_block = m.group(1) + '\n' + new_inner + '\n' + m.group(3)
        text = text[:m.start()] + new_block + text[m.end():]
        p.write_text(text, encoding='utf-8')
        n_fixed += 1
    print(f'\nFixed {n_fixed} epigraphs ({n_missing} skipped)')


if __name__ == '__main__':
    main()
