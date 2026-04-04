#!/usr/bin/env python3
"""Rename generated icon files from img_NNN.png to descriptive names."""
from pathlib import Path

ICON_DIR = Path("E:/Projects/LLMCourse/front-matter/images/icons")

NAMES = [
    "undergrad-engineering",
    "undergrad-research",
    "grad-engineering",
    "grad-research",
    "product-builder",
    "ml-engineer",
    "agent-builder",
    "platform-devops",
    "researcher",
    "career-changer",
    "data-scientist",
    "nlp-engineer",
    "fullstack-developer",
    "tech-leader",
    "domain-expert",
    "safety-alignment",
    "rag-search",
    "open-source",
    "hobbyist",
    "prompt-engineer",
    "multimodal-developer",
    "infra-engineer",
    "ai-educator",
    "startup-cto",
]

for i, name in enumerate(NAMES, 1):
    src = ICON_DIR / f"img_{i:03d}.png"
    dst = ICON_DIR / f"{name}.png"
    if src.exists():
        src.rename(dst)
        print(f"  {src.name} -> {dst.name}")
    else:
        print(f"  MISSING: {src.name}")

print(f"\nDone. Files in {ICON_DIR}:")
for f in sorted(ICON_DIR.glob("*.png")):
    print(f"  {f.name}")
