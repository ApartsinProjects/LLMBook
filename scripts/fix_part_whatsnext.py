"""Add whats-next div to part index pages that are missing it."""

import re
from pathlib import Path

BASE = Path(r"E:\Projects\LLMCourse")

# Part order and titles
PARTS = [
    ("part-1-foundations", "Part I: Foundations"),
    ("part-2-understanding-llms", "Part II: Understanding LLMs"),
    ("part-3-working-with-llms", "Part III: Working with LLMs"),
    ("part-4-training-adapting", "Part IV: Training and Adapting"),
    ("part-5-retrieval-conversation", "Part V: Retrieval and Conversation"),
    ("part-6-agents-applications", "Part VI: Agents and Applications"),
    ("part-7-multimodal-applications", "Part VII: Multimodal and Applications"),
    ("part-7-production-strategy", "Part VII: Production Strategy"),
    ("part-8-evaluation-production", "Part VIII: Evaluation and Production"),
    ("part-9-safety-strategy", "Part IX: Safety and Strategy"),
    ("part-10-frontiers", "Part X: Frontiers"),
]

def main():
    fixed = 0
    for i, (dirname, title) in enumerate(PARTS):
        index_path = BASE / dirname / "index.html"
        if not index_path.exists():
            continue

        text = index_path.read_text(encoding="utf-8")
        if 'class="whats-next"' in text:
            continue

        # Determine next part
        if i < len(PARTS) - 1:
            next_dir, next_title = PARTS[i + 1]
            next_href = f"../{next_dir}/index.html"
            whats_next = f'''<div class="whats-next">
    <h2>What Comes Next</h2>
    <p>Continue to <a class="cross-ref" href="{next_href}">{next_title}</a>.</p>
</div>
'''
        else:
            whats_next = '''<div class="whats-next">
    <h2>What Comes Next</h2>
    <p>You have reached the final part of the book. Explore the <a class="cross-ref" href="../appendices/appendix-a-mathematical-foundations/index.html">Appendices</a> for reference material, or revisit any earlier part to deepen your understanding.</p>
</div>
'''

        # Insert before <footer> or </main>
        if "<footer>" in text:
            text = text.replace("<footer>", whats_next + "\n<footer>")
        elif "</main>" in text:
            text = text.replace("</main>", whats_next + "\n</main>")
        else:
            continue

        index_path.write_text(text, encoding="utf-8")
        fixed += 1
        print(f"  Added whats-next: {dirname}/index.html")

    print(f"\nTotal: {fixed} part index pages updated")

if __name__ == "__main__":
    main()
