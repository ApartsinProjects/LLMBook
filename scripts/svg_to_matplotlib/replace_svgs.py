"""Replace SVG chart blocks in HTML with <figure> img tags, archiving originals."""
import re, os, sys
from pathlib import Path

ROOT = Path(r"E:/Projects/LLMCourse")
ARCHIVE = ROOT / "_archive" / "replaced-svgs"
ARCHIVE.mkdir(parents=True, exist_ok=True)

# Each entry: (html_file, svg_index_1based, figure_id, img_filename, alt_text, caption)
replacements = [
    (
        "part-1-foundations/module-00-ml-pytorch-foundations/section-0.1.html",
        1,  # first SVG in file
        "0.1.2",
        "images/figure-0.1.2.png",
        "Gradient descent on a loss surface showing iterative steps toward a local minimum, with a global minimum marked further along the curve",
        "Gradient descent follows the slope downhill, step by step. The learning rate controls step size."
    ),
    (
        "part-1-foundations/module-00-ml-pytorch-foundations/section-0.1.html",
        2,  # second SVG in file
        "0.1.4",
        "images/figure-0.1.4.png",
        "Bias-variance tradeoff showing Bias squared, Variance, and Total Error curves with an optimal point",
        "As model complexity increases, bias decreases but variance increases. The optimal model minimizes total error."
    ),
    (
        "part-1-foundations/module-05-decoding-text-generation/section-5.2.html",
        1,
        "5.2.2",
        "images/figure-5.2.2.png",
        "Temperature scaling effect on token probability distribution, comparing T=0.3 sharp, T=1.0 original, and T=2.0 flat distributions",
        'Temperature controls the "peakiness" of the distribution. Lower temperatures concentrate probability on top tokens; higher temperatures spread it more evenly.'
    ),
    (
        "part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.3.html",
        2,  # second SVG (first is likely another diagram)
        "6.3.6",
        "images/figure-6.3.6.png",
        "Side-by-side comparison: exact match accuracy showing apparent emergence versus log-likelihood showing smooth scaling",
        "The same underlying capability can appear emergent or smoothly scaling depending on the evaluation metric chosen."
    ),
    (
        "part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.5.html",
        1,
        "6.5.3",
        "images/figure-6.5.3.png",
        "Grokking phenomenon: training accuracy rises quickly while validation accuracy plateaus for many steps before eventually catching up",
        "In grokking, the model achieves perfect training accuracy early but takes many more steps to generalize, with a long validation plateau between memorization and true learning."
    ),
    (
        "part-3-working-with-llms/module-12-hybrid-ml-llm/section-12.4.html",
        1,
        "12.4.2",
        "images/figure-12.4.2.png",
        "Pareto frontier scatter plot showing cost versus quality tradeoffs for TF-IDF, BERT, GPT-4o-mini, GPT-4o, Claude Opus, and a hybrid router approach",
        "The Pareto frontier for a classification task. The hybrid router (orange) achieves near-GPT-4o quality at a fraction of the cost by routing easy queries to cheaper models."
    ),
    (
        "part-4-training-adapting/module-14-fine-tuning-fundamentals/section-14.1.html",
        2,  # second SVG
        "14.1.4",
        "images/figure-14.1.4.png",
        "Task performance rising while general ability falls during fine-tuning, with an optimal zone marked between the crossing curves",
        "As task-specific performance improves, general capabilities may degrade. The optimal checkpoint balances both."
    ),
    (
        "part-4-training-adapting/module-14-fine-tuning-fundamentals/section-14.7.html",
        1,
        "14.7.1",
        "images/figure-14.7.1.png",
        "Perplexity versus sequence length chart showing degradation beyond training window without context extension, and stable performance with context extension",
        "Without context extension, perplexity degrades sharply beyond the training window. Context extension techniques maintain quality at longer lengths."
    ),
    (
        "part-4-training-adapting/module-16-distillation-merging/section-16.3.html",
        1,
        "16.3.1",
        "images/figure-16.3.1.png",
        "Domain performance rising while general performance falls during continual learning, with a sweet spot marked at the crossing point",
        "As domain performance improves, general capabilities degrade. The goal is to find (and maintain) the sweet spot."
    ),
    (
        "part-8-evaluation-production/module-30-observability-monitoring/section-30.2.html",
        2,  # second SVG
        "30.2.3",
        "images/figure-30.2.3.png",
        "Quality monitoring timeline showing stable performance followed by silent degradation after a provider model update, with an alert threshold crossed at Week 3.5",
        "Quality monitoring timeline showing a silent degradation caused by a provider model update."
    ),
]

def find_svg_block(html_text, svg_index):
    """Find the nth SVG block including its parent diagram-container div."""
    # Find all SVG tags
    svg_pattern = re.compile(r'<svg\b[^>]*>.*?</svg>', re.DOTALL)
    matches = list(svg_pattern.finditer(html_text))

    if svg_index > len(matches):
        return None, None, None

    svg_match = matches[svg_index - 1]

    # Look for parent diagram-container div
    # Search backwards from SVG start for <div class="diagram-container">
    before_svg = html_text[:svg_match.start()]
    container_start = before_svg.rfind('<div class="diagram-container">')

    if container_start == -1:
        # No container, just use the SVG
        return svg_match.start(), svg_match.end(), svg_match.group(0)

    # Find the closing </div> for the diagram-caption after the SVG
    after_svg = html_text[svg_match.end():]

    # Look for diagram-caption div and its closing, then container closing
    caption_match = re.search(r'\s*<div class="diagram-caption">.*?</div>\s*</div>', after_svg, re.DOTALL)
    if caption_match:
        block_end = svg_match.end() + caption_match.end()
    else:
        # Just close after svg + next </div></div>
        close_match = re.search(r'\s*</div>', after_svg)
        block_end = svg_match.end() + (close_match.end() if close_match else 0)

    return container_start, block_end, html_text[container_start:block_end]


for r in replacements:
    html_rel, svg_idx, fig_id, img_path, alt_text, caption = r
    html_path = ROOT / html_rel

    print(f"\nProcessing {html_rel} - Figure {fig_id}...")

    text = html_path.read_text(encoding='utf-8')

    start, end, svg_block = find_svg_block(text, svg_idx)
    if svg_block is None:
        print(f"  ERROR: SVG #{svg_idx} not found in {html_rel}")
        continue

    # Archive the SVG block
    section_name = html_rel.split('/')[-1].replace('.html', '')
    archive_file = ARCHIVE / f"{section_name}-figure-{fig_id}.svg"
    archive_file.write_text(svg_block, encoding='utf-8')
    print(f"  Archived to: {archive_file.name}")

    # Create replacement HTML
    replacement = f'''<figure>
    <img src="{img_path}" alt="{alt_text}" loading="lazy" style="max-width: 100%;">
    <figcaption><strong>Figure {fig_id}</strong>: {caption}</figcaption>
</figure>'''

    # Replace in text
    new_text = text[:start] + replacement + text[end:]
    html_path.write_text(new_text, encoding='utf-8')
    print(f"  Replaced SVG with <figure> tag")

print("\nDone! All SVGs replaced.")
