"""Fix structural/formatting issues in Part 9 section files.

Fixes applied:
1. Move code-caption divs from above <pre> to below </pre></code>
2. Remove FIXME stacked caption comments and their duplicate captions
3. Fix epigraph attributions to follow 'A [Adjective] AI Agent' pattern
"""
import re
import sys
from pathlib import Path

ROOT = Path(r"E:\Projects\LLMCourse")
PART9 = ROOT / "part-9-safety-strategy"

DRY_RUN = "--dry-run" in sys.argv

# Map section topics to appropriate epigraph adjectives
SECTION_ADJECTIVES = {
    "section-32.1": "Vigilant",      # LLM Security Threats
    "section-32.2": "Principled",    # Responsible AI Frameworks
    "section-32.3": "Watchful",      # Bias Detection and Mitigation
    "section-32.4": "Meticulous",    # Privacy-Preserving LLM Systems
    "section-32.5": "Steadfast",     # Content Moderation and Safety Filters
    "section-32.6": "Transparent",   # Explainability and Interpretability
    "section-32.7": "Diligent",      # Regulatory Compliance
    "section-32.8": "Battle-Tested", # Red Teaming and Adversarial Testing
    "section-32.9": "Resolute",      # Incident Response for AI Systems
    "section-32.10": "Reflective",   # Cross-Cultural AI Ethics
    "section-32.11": "Conscientious",# Environmental Impact
    "section-32.12": "Cautious",     # Governance Frameworks
    "section-32.13": "Farsighted",   # Chapter Summary
    "section-33.1": "Strategic",     # AI Strategy Frameworks
    "section-33.2": "Pragmatic",     # Product-Market Fit for AI
    "section-33.3": "Analytical",    # ROI and Business Cases
    "section-33.4": "Resourceful",   # Build vs Buy Decisions
    "section-33.5": "Calculated",    # Cost Optimization
    "section-33.6": "Perceptive",    # Organizational Change
    "section-33.7": "Visionary",     # Scaling AI Teams
    "section-33.8": "Methodical",    # Chapter Summary
}

changes_log = {}

for html_file in sorted(PART9.rglob("section-*.html")):
    rel = str(html_file.relative_to(ROOT))
    section_key = html_file.stem  # e.g., "section-32.1"
    content = html_file.read_text(encoding="utf-8")
    original = content
    fixes = []

    # === FIX 1: Move code-caption from above <pre> to after </code></pre> ===
    # Pattern: <div class="code-caption">...</div>\n<pre><code...>...</code></pre>
    def move_caption_below(m):
        caption = m.group(1)
        pre_block = m.group(2)
        fixes.append(f"Moved caption below code block: {caption[:60]}...")
        return f"{pre_block}\n{caption}"

    content = re.sub(
        r'(<div class="code-caption">.*?</div>)\s*\n(\s*<pre><code.*?</code></pre>)',
        move_caption_below,
        content,
        flags=re.DOTALL
    )

    # Also handle <p class="code-caption"> variant
    content = re.sub(
        r'(<p class="code-caption">.*?</p>)\s*\n(\s*<pre><code.*?</code></pre>)',
        move_caption_below,
        content,
        flags=re.DOTALL
    )

    # === FIX 2: Remove FIXME stacked caption comments and their associated stacked captions ===
    # Pattern: <!-- FIXME: stacked caption, needs manual review -->\n<div class="code-caption">...</div>
    stacked_pattern = r'\s*<!-- FIXME: stacked caption, needs manual review -->\s*\n\s*<div class="code-caption">.*?</div>'
    stacked_matches = re.findall(stacked_pattern, content, re.DOTALL)
    if stacked_matches:
        for sm in stacked_matches:
            fixes.append(f"Removed stacked caption FIXME block")
        content = re.sub(stacked_pattern, '', content, flags=re.DOTALL)

    # Also handle <p> variant of stacked captions
    stacked_pattern_p = r'\s*<!-- FIXME: stacked caption, needs manual review -->\s*\n\s*<p class="code-caption">.*?</p>'
    stacked_matches_p = re.findall(stacked_pattern_p, content, re.DOTALL)
    if stacked_matches_p:
        for sm in stacked_matches_p:
            fixes.append(f"Removed stacked caption FIXME block (p variant)")
        content = re.sub(stacked_pattern_p, '', content, flags=re.DOTALL)

    # === FIX 3: Fix epigraph attributions ===
    # Current pattern: Guard</a> <span class="agent-desc">AI Agent</span>
    # Need: A Vigilant Guard</a> <span class="agent-desc">AI Agent</span>
    # But the "A Adjective" should go before the agent name link
    adj = SECTION_ADJECTIVES.get(section_key, "Wise")

    # Pattern: >Guard</a> <span class="agent-desc">AI Agent</span>
    # Replace with: >A {adj} Guard</a> <span class="agent-desc">AI Agent</span>
    # But we need the agent name dynamically
    def fix_attribution(m):
        agent_name = m.group(1)
        article = "An" if adj[0] in "AEIOUaeiou" else "A"
        fixes.append(f"Fixed epigraph attribution: '{article} {adj} {agent_name} AI Agent'")
        return f">{article} {adj} {agent_name}</a> <span class=\"agent-desc\">AI Agent</span>"

    content = re.sub(
        r'>(\w+)</a> <span class="agent-desc">AI Agent</span>',
        fix_attribution,
        content,
        count=1  # Only fix the first (epigraph) attribution
    )

    # Only write if changed
    if content != original:
        if not DRY_RUN:
            html_file.write_text(content, encoding="utf-8")
        changes_log[rel] = fixes
        print(f"\n{'[DRY RUN] ' if DRY_RUN else ''}Fixed: {rel}")
        for fix in fixes:
            print(f"  - {fix}")

print(f"\n\nTotal files modified: {len(changes_log)}")
