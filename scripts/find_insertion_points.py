"""Find the insertion point (after prerequisites div or first <p>) in each section."""
import re
from pathlib import Path

BOOK_ROOT = Path(r"E:/Projects/LLMCourse")
sections = [
    # Chapter 32 (8 sections getting illustrations)
    "part-9-safety-strategy/module-32-safety-ethics-regulation/section-32.1.html",
    "part-9-safety-strategy/module-32-safety-ethics-regulation/section-32.2.html",
    "part-9-safety-strategy/module-32-safety-ethics-regulation/section-32.3.html",
    "part-9-safety-strategy/module-32-safety-ethics-regulation/section-32.4.html",
    "part-9-safety-strategy/module-32-safety-ethics-regulation/section-32.8.html",
    "part-9-safety-strategy/module-32-safety-ethics-regulation/section-32.7.html",
    "part-9-safety-strategy/module-32-safety-ethics-regulation/section-32.11.html",
    "part-9-safety-strategy/module-32-safety-ethics-regulation/section-32.13.html",
    # Chapter 33 (8 sections getting illustrations)
    "part-9-safety-strategy/module-33-strategy-product-roi/section-33.1.html",
    "part-9-safety-strategy/module-33-strategy-product-roi/section-33.2.html",
    "part-9-safety-strategy/module-33-strategy-product-roi/section-33.3.html",
    "part-9-safety-strategy/module-33-strategy-product-roi/section-33.4.html",
    "part-9-safety-strategy/module-33-strategy-product-roi/section-33.5.html",
    "part-9-safety-strategy/module-33-strategy-product-roi/section-33.6.html",
    "part-9-safety-strategy/module-33-strategy-product-roi/section-33.7.html",
    "part-9-safety-strategy/module-33-strategy-product-roi/section-33.8.html",
]

for s in sections:
    text = (BOOK_ROOT / s).read_text(encoding="utf-8")
    lines = text.split("\n")
    # Find: end of prerequisites div, or first </p> after <h1>
    prereq_end = None
    first_p_end = None
    in_h1 = False
    for i, line in enumerate(lines):
        if "<h1>" in line:
            in_h1 = True
        if in_h1 and "</div>" in line and prereq_end is None:
            # Check if this closes a prerequisites div
            # Look backwards for prerequisites
            chunk = "\n".join(lines[max(0, i-10):i+1])
            if "prerequisites" in chunk.lower():
                prereq_end = i
        if in_h1 and "</p>" in line and first_p_end is None:
            first_p_end = i
    insertion = prereq_end if prereq_end else first_p_end
    print(f"{s}: insert after line {insertion}")
