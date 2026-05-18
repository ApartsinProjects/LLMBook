"""Verify candidate sections still lack fun-note callouts AND no comic-* image yet."""
from pathlib import Path
import re

ROOT = Path(r"E:\Projects\BookBlogsHome\LLMBook")

CANDIDATES = [
    "part-4-training-adaptation/module-16-fine-tuning-fundamentals/section-16.2.html",
    "part-4-training-adaptation/module-16-fine-tuning-fundamentals/section-16.3.html",
    "part-4-training-adaptation/module-16-fine-tuning-fundamentals/section-16.5.html",
    "part-4-training-adaptation/module-16-fine-tuning-fundamentals/section-16.7.html",
    "part-4-training-adaptation/module-15-synthetic-data/section-15.3.html",
    "part-4-training-adaptation/module-15-synthetic-data/section-15.7.html",
    "part-4-training-adaptation/module-18-alignment-rlhf-dpo/section-18.5.html",
    "part-5-multimodal-llms/module-22-vision-language-models/section-22.4.html",
    "part-5-multimodal-llms/module-22-vision-language-models/section-22.5.html",
    "part-5-multimodal-llms/module-20-audio-music-generation/section-20.5.html",
    "part-5-multimodal-llms/module-21-document-understanding-ocr/section-21.2.html",
    "part-5-multimodal-llms/module-23-3d-generation-neural-scenes/section-23.3.html",
    "part-6-agentic-ai/module-26-ai-agents/section-26.4.html",
    "part-6-agentic-ai/module-26-ai-agents/section-26.5.html",
    "part-6-agentic-ai/module-28-multi-agent-systems/section-28.2.html",
    "part-6-agentic-ai/module-28-multi-agent-systems/section-28.3.html",
    "part-6-agentic-ai/module-29-specialized-agents/section-29.3.html",
    "part-6-agentic-ai/module-27-tool-use-protocols/section-27.4.html",
    "part-7-retrieval-information-extraction-with-llms/module-33-cross-modal-reasoning-rag/section-33.2.html",
    "part-7-retrieval-information-extraction-with-llms/module-33-cross-modal-reasoning-rag/section-33.1.html",
    "part-7-retrieval-information-extraction-with-llms/module-32-rag/section-32.4.html",
    "part-7-retrieval-information-extraction-with-llms/module-36-retrieval-tools/section-36.2.html",
    "part-8-conversational-ai-with-llms/module-40-voice-realtime-multimodal/section-40.3.html",
    "part-8-conversational-ai-with-llms/module-40-voice-realtime-multimodal/section-40.4.html",
    "part-9-llm-evaluation-observability/module-44-online-eval-observability/section-44.3.html",
    "part-9-llm-evaluation-observability/module-44-online-eval-observability/section-44.5.html",
    "part-9-llm-evaluation-observability/module-43-specialized-evaluation/section-43.2.html",
    "part-9-llm-evaluation-observability/module-46-llm-as-judge-automated-evaluation/section-46.3.html",
]

FUN_NOTE = re.compile(r'<div class="callout fun-note">', re.IGNORECASE)
COMIC_IMG = re.compile(r'images/comic-[^"\']+\.png', re.IGNORECASE)
H2_RE = re.compile(r'<h2 id="([^"]+)">([^<]+)</h2>')

for cand in CANDIDATES:
    p = ROOT / cand
    if not p.exists():
        print(f"  MISS  {cand}")
        continue
    text = p.read_text(encoding="utf-8")
    has_funnote = bool(FUN_NOTE.search(text))
    comic = COMIC_IMG.search(text)
    h2s = H2_RE.findall(text)
    flag = "OK-FREE" if not has_funnote and not comic else f"SKIP (funnote={has_funnote}, comic={comic.group() if comic else None})"
    print(f"  {flag}  {cand}")
    if not has_funnote and not comic and h2s:
        for hid, title in h2s[:5]:
            print(f"      h2#{hid}: {title}")
