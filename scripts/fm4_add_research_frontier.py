"""Inject a Research Frontier callout into the last section of modules that
lack one across the whole module (per FM4_PROMISE audit).

Inserts a <div class="callout research-frontier"> with topic-appropriate
2024-2026 references, right before the closing <nav class="chapter-nav">
of the last section file.
"""
import re
from pathlib import Path

ROOT = Path(r'E:/Projects/BookBlogsHome/LLMBook')


def natural_key(p: Path):
    m = re.search(r'section-(\d+)\.(\d+)\.html', p.name)
    return (int(m.group(1)), int(m.group(2))) if m else (0, 0)


# Per-module Research Frontier HTML. Real references from 2024-2026.
RF_CONTENT = {
    'part-5-multimodal-llms/module-20-audio-music-generation': '''<div class="callout research-frontier">
<div class="callout-title">Research Frontier</div>
<p>Audio, music, and video generation are advancing on three open frontiers in 2025-2026. First, minute-plus video consistency: how do you keep a character, lighting, and physical world coherent across hundreds of frames without compounding drift? Block-sparse attention combined with hierarchical temporal tokenization (OpenAI Sora 2, 2025) and explicit world-model latents (Bruce et al., <em>Genie 2: A large-scale foundation world model</em>, 2024) are the leading approaches, but evaluation is still ad-hoc. Second, real-time streaming generation: low-latency neural codecs (Defossez et al., <em>Moshi: a speech-text foundation model for real-time dialogue</em>, <a href="https://arxiv.org/abs/2410.00037" target="_blank" rel="noopener">arXiv:2410.00037</a>) push toward sub-200ms voice agents, but joint streaming audio plus video remains unsolved.</p>
<p>Third, controllability and provenance. Music-LM-style text-to-music systems (Copet et al., <em>Simple and Controllable Music Generation</em>, <a href="https://arxiv.org/abs/2306.05284" target="_blank" rel="noopener">arXiv:2306.05284</a> and 2024 follow-ups) still struggle with multi-bar musical structure, and emerging watermarking schemes such as AudioSeal (San Roman et al., <em>Proactive Detection of Voice Cloning with Localized Watermarking</em>, <a href="https://arxiv.org/abs/2401.17264" target="_blank" rel="noopener">arXiv:2401.17264</a>) are racing against rapid synthesis-quality gains. Expect 2026 to deliver both stronger generative control and stronger detection, but the gap will tighten.</p>
</div>
''',
    'part-5-multimodal-llms/module-21-document-understanding-ocr': '''<div class="callout research-frontier">
<div class="callout-title">Research Frontier</div>
<p>Document understanding is in transition from pipeline OCR plus layout to end-to-end multimodal models that read documents the way humans do. The frontier in 2024-2026 is three-fold. First, unified document foundation models: Nougat (Blecher et al., <em>Nougat: Neural Optical Understanding for Academic Documents</em>, <a href="https://arxiv.org/abs/2308.13418" target="_blank" rel="noopener">arXiv:2308.13418</a>) and successor systems like GOT-OCR2.0 (Wei et al., <em>General OCR Theory: Towards OCR-2.0 via a Unified End-to-end Model</em>, <a href="https://arxiv.org/abs/2409.01704" target="_blank" rel="noopener">arXiv:2409.01704</a>) replace the OCR plus layout plus relation pipeline with a single VLM. Open question: how do you reliably extract structured tables, formulas, and forms when the model can hallucinate?</p>
<p>Second, long-document context. ColPali (Faysse et al., <em>ColPali: Efficient Document Retrieval with Vision Language Models</em>, <a href="https://arxiv.org/abs/2407.01449" target="_blank" rel="noopener">arXiv:2407.01449</a>) shows that late-interaction over image patches can match or exceed traditional pipeline retrieval for visually rich documents, but indexing cost remains high. Third, grounded answer generation with citations: retrieval-augmented document QA still struggles to ground claims to specific page regions in a verifiable way, which is the gating problem for legal and clinical adoption.</p>
</div>
''',
    'part-5-multimodal-llms/module-22-vision-language-models': '''<div class="callout research-frontier">
<div class="callout-title">Research Frontier</div>
<p>Vision-language models are converging on three open research questions in 2025-2026. First, native multimodal pretraining versus connector-based VLMs: Chameleon (Chameleon Team, <em>Chameleon: Mixed-Modal Early-Fusion Foundation Models</em>, <a href="https://arxiv.org/abs/2405.09818" target="_blank" rel="noopener">arXiv:2405.09818</a>) and successor work argue that interleaved early-fusion training beats projecting frozen vision encoders into an LLM, but training cost is much higher. Second, high-resolution and long-video handling: dynamic tiling (Liu et al., <em>LLaVA-NeXT: Improved reasoning, OCR, and world knowledge</em>, 2024) and token-merging schemes like LongVILA (Chen et al., <em>LongVILA: Scaling Long-Context Visual Language Models for Long Videos</em>, <a href="https://arxiv.org/abs/2408.10188" target="_blank" rel="noopener">arXiv:2408.10188</a>) attack the quadratic blow-up, but the trade-off between resolution, frames, and context budget is still ad-hoc.</p>
<p>Third, grounded reasoning and spatial understanding. Open VLMs from 2024-2026 such as Qwen2-VL (Wang et al., <em>Qwen2-VL: Enhancing Vision-Language Model's Perception of the World at Any Resolution</em>, <a href="https://arxiv.org/abs/2409.12191" target="_blank" rel="noopener">arXiv:2409.12191</a>) demonstrate strong OCR and visual grounding, yet benchmarks like MMMU and BLINK reveal that compositional and physical reasoning remain weak. Expect 2026 work to focus on world-model integration and 3D-aware perception.</p>
</div>
''',
    'part-5-multimodal-llms/module-23-3d-generation-neural-scenes': '''<div class="callout research-frontier">
<div class="callout-title">Research Frontier</div>
<p>3D generation has shifted from NeRF-based representations to fast-rendering Gaussian splatting and feed-forward priors. The frontier in 2024-2026 hinges on three open problems. First, real-time generative 3D from a single image or prompt: TripoSR (Tochilkin et al., <em>TripoSR: Fast 3D Object Reconstruction from a Single Image</em>, <a href="https://arxiv.org/abs/2403.02151" target="_blank" rel="noopener">arXiv:2403.02151</a>) and follow-up systems push single-image to mesh below one second, but textured quality and topology cleanliness still trail multi-view reconstruction. Second, large-scale scene generation: dynamic and large-scale 3D Gaussian splatting (Kerbl et al., <em>3D Gaussian Splatting for Real-Time Radiance Field Rendering</em>, <a href="https://arxiv.org/abs/2308.04079" target="_blank" rel="noopener">arXiv:2308.04079</a> and 2024-2025 extensions) enables editable scenes, but text-to-scene with object-level control remains brittle.</p>
<p>Third, video-to-3D and world models. Generative 4D from monocular video (Liu et al., <em>4D-fy: Text-to-4D Generation Using Hybrid Score Distillation Sampling</em>, <a href="https://arxiv.org/abs/2311.17984" target="_blank" rel="noopener">arXiv:2311.17984</a> and 2025 follow-ups) is the next milestone; physically consistent dynamics from a single take is the open research question. Expect 2026 to deliver hybrid Gaussian plus mesh representations and tighter coupling with VLMs as scene editors.</p>
</div>
''',
    'part-6-agentic-ai/module-27-tool-use-protocols': '''<div class="callout research-frontier">
<div class="callout-title">Research Frontier</div>
<p>Tool use protocols are the connective tissue of agentic AI, and 2024-2026 has produced both rapid standardization and open research questions. Anthropic's Model Context Protocol (MCP, 2024-2025) emerged as the de-facto standard for connecting models to tools and data sources, but the protocol does not specify how to do safe tool selection at scale. Toolformer (Schick et al., <em>Toolformer: Language Models Can Teach Themselves to Use Tools</em>, <a href="https://arxiv.org/abs/2302.04761" target="_blank" rel="noopener">arXiv:2302.04761</a>) and ToolLLM (Qin et al., <em>ToolLLM: Facilitating Large Language Models to Master 16000+ Real-world APIs</em>, <a href="https://arxiv.org/abs/2307.16789" target="_blank" rel="noopener">arXiv:2307.16789</a>) demonstrated self-supervised tool selection; recent work pushes toward retrieval-augmented tool catalogs that scale to thousands of MCP servers.</p>
<p>Two open research problems dominate 2025-2026. First, prompt injection through tool outputs: when an agent reads untrusted content (web pages, emails), how do you prevent that content from rewriting the agent's plan? See Greshake et al. (<em>Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection</em>, <a href="https://arxiv.org/abs/2302.12173" target="_blank" rel="noopener">arXiv:2302.12173</a>) and 2024-2025 follow-ups on tool-output sandboxing. Second, structured outputs and reliability: constrained decoding plus JSON-schema enforcement is now standard, but multi-turn tool-use error recovery (when a tool returns an unexpected error) remains brittle and is the focus of active benchmark work like tau-bench (Yao et al., 2024).</p>
</div>
''',
    'part-6-agentic-ai/module-29-specialized-agents': '''<div class="callout research-frontier">
<div class="callout-title">Research Frontier</div>
<p>Specialized agents (coding agents, web agents, computer-use agents, scientific-research agents) are the most measurable proving ground for LLM capabilities in 2024-2026. Three open frontiers stand out. First, coding agents at repository scale: SWE-bench (Jimenez et al., <em>SWE-bench: Can Language Models Resolve Real-World GitHub Issues?</em>, <a href="https://arxiv.org/abs/2310.06770" target="_blank" rel="noopener">arXiv:2310.06770</a>) drove rapid progress from sub-5% solve rate in 2023 to above 50% in 2025 with agents like SWE-agent (Yang et al., <em>SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering</em>, <a href="https://arxiv.org/abs/2405.15793" target="_blank" rel="noopener">arXiv:2405.15793</a>) and Claude-Sonnet-based systems, but the long-horizon "implement a feature in a 10M-LOC codebase" problem is still open.</p>
<p>Second, computer-use and visual web agents: Anthropic's Claude computer-use (October 2024) and OpenAI's Operator (early 2025) demonstrate screen-pixel grounding, but multi-step robustness, error recovery, and safety against malicious websites are unresolved. See WebArena (Zhou et al., <em>WebArena: A Realistic Web Environment for Building Autonomous Agents</em>, <a href="https://arxiv.org/abs/2307.13854" target="_blank" rel="noopener">arXiv:2307.13854</a>) and OSWorld (Xie et al., 2024). Third, scientific research agents: from AI Scientist (Lu et al., <em>The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery</em>, <a href="https://arxiv.org/abs/2408.06292" target="_blank" rel="noopener">arXiv:2408.06292</a>) to literature-review and protocol-execution agents in biology and chemistry, evaluation of genuine novelty is the unsolved bottleneck.</p>
</div>
''',
    'part-7-retrieval-information-extraction-with-llms/module-33-cross-modal-reasoning-rag': '''<div class="callout research-frontier">
<div class="callout-title">Research Frontier</div>
<p>Cross-modal RAG, where the retriever and the reader span text, images, tables, and code, is one of the most active research areas in retrieval for 2024-2026. ColPali (Faysse et al., <em>ColPali: Efficient Document Retrieval with Vision Language Models</em>, <a href="https://arxiv.org/abs/2407.01449" target="_blank" rel="noopener">arXiv:2407.01449</a>) shifted the field by indexing document pages as image patches and using late interaction, outperforming text-pipeline retrieval on ViDoRe. The open question is index size and cost: late-interaction indices are 10-100x larger than dense single-vector indices, and the engineering trade-off is still being mapped.</p>
<p>Two further frontiers in 2025-2026: cross-modal grounding for citations. Visual-RAG systems must point to a specific page region or bounding box, not just a chunk, to be trustworthy in legal and clinical settings; see VisRAG (Yu et al., <em>VisRAG: Vision-based Retrieval-augmented Generation on Multi-modality Documents</em>, <a href="https://arxiv.org/abs/2410.10594" target="_blank" rel="noopener">arXiv:2410.10594</a>). And video RAG: indexing and reasoning over hours of video with both transcript and visual evidence remains brittle. Expect 2026 to bring tighter coupling between embedding models, VLM readers, and explicit grounding signals.</p>
</div>
''',
    'part-7-retrieval-information-extraction-with-llms/module-34-structured-information-extraction-ner': '''<div class="callout research-frontier">
<div class="callout-title">Research Frontier</div>
<p>Structured information extraction with LLMs is being reshaped by two open research questions in 2024-2026. First, schema-guided extraction at scale. NuExtract and similar zero-shot extractors plus instruction-tuned extractors (Sainz et al., <em>GoLLIE: Annotation Guidelines improve Zero-Shot Information-Extraction</em>, <a href="https://arxiv.org/abs/2310.03668" target="_blank" rel="noopener">arXiv:2310.03668</a>) show strong domain transfer, but reliable extraction of nested, recursive, or relational schemas (e.g., financial filings, clinical notes) is still uneven. JSON-schema-constrained decoding (Outlines, jsonformer, and structured-output APIs) closes much of the gap, but does not solve hallucination of values that satisfy the schema but are unsupported by the source.</p>
<p>Second, grounded extraction with citations. Source-attributed extraction (Bohnet et al., <em>Attributed Question Answering</em> family of work, 2022-2024) is the foundation, but production systems still struggle to link every extracted field to the exact source span in long documents. See also the 2024-2025 ASTUTE-RAG and GroundedRAG line of work on knowledge conflicts. Expect 2026 to deliver evaluation harnesses that measure both extraction accuracy and span-level grounding jointly, plus better calibrated confidence at the field level for downstream review workflows.</p>
</div>
''',
    'part-9-llm-evaluation-observability/module-46-llm-as-judge-automated-evaluation': '''<div class="callout research-frontier">
<div class="callout-title">Research Frontier</div>
<p>LLM-as-judge has rapidly become standard practice for evaluating open-ended generation, but 2024-2026 research has exposed serious failure modes. Zheng et al. (<em>Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena</em>, <a href="https://arxiv.org/abs/2306.05685" target="_blank" rel="noopener">arXiv:2306.05685</a>) documented position bias, verbosity bias, and self-preference bias; subsequent work measured how strong these effects are in practice. Open question: how do you build a judge that is robust across model families and across the answer distribution, not just at the median? PandaLM (Wang et al., <em>PandaLM: An Automatic Evaluation Benchmark for LLM Instruction Tuning Optimization</em>, <a href="https://arxiv.org/abs/2306.05087" target="_blank" rel="noopener">arXiv:2306.05087</a>) and Prometheus 2 (Kim et al., <em>Prometheus 2: An Open Source Language Model Specialized in Evaluating Other Language Models</em>, <a href="https://arxiv.org/abs/2405.01535" target="_blank" rel="noopener">arXiv:2405.01535</a>) explore open-weight specialized judges.</p>
<p>Two frontiers stand out. First, judge calibration and meta-evaluation: how do you know your judge is right? Recent benchmarks (JudgeBench, RewardBench 2 in 2024-2025) frame this as a measurement problem and report large gaps between judges and humans on subtle correctness. Second, reward modeling overlap with judging: as judges are increasingly used as reward signals for RLHF and DPO, reward hacking becomes a safety concern (see Eisenstein et al., <em>Helping or Herding? Reward Model Ensembles Mitigate but do not Eliminate Reward Hacking</em>, <a href="https://arxiv.org/abs/2312.09244" target="_blank" rel="noopener">arXiv:2312.09244</a>). Expect 2026 to deliver multi-judge ensembles, judge-specific debiasing, and human-in-the-loop calibration as standard.</p>
</div>
''',
}


def inject_rf(section_path: Path, content: str) -> bool:
    text = section_path.read_text(encoding='utf-8')
    if 'research-frontier' in text:
        return False
    # Inject before the chapter-nav at the end of the section
    nav_re = re.compile(r'(<nav class="chapter-nav">)')
    m = nav_re.search(text)
    if not m:
        # Fallback: inject before </main>
        if '</main>' in text:
            text = text.replace('</main>', content + '</main>', 1)
        else:
            return False
    else:
        text = text[:m.start()] + content + text[m.start():]
    section_path.write_text(text, encoding='utf-8')
    return True


def natural_last(mod_path: Path) -> Path:
    secs = sorted(mod_path.glob('section-*.html'), key=natural_key)
    return secs[-1]


def main():
    n_done = 0
    for mod_rel, content in RF_CONTENT.items():
        mod = ROOT / mod_rel
        last = natural_last(mod)
        ok = inject_rf(last, content)
        status = 'OK' if ok else 'SKIP'
        print(f'{status}: {mod_rel} -> {last.name}')
        if ok:
            n_done += 1
    print(f'\nResearch Frontier inserted into {n_done} sections')


if __name__ == '__main__':
    main()
