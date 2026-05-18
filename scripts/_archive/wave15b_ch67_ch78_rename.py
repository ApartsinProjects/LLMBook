"""Wave 15b: rename Ch 67 (Ideation) and Ch 78 (Manufacturing) to reflect their
actual contents.

Ch 67 has 15 sections spanning Ideation → Product Spec → PM → UX → Strategy →
Vendor Selection → Risk → Prototype Loop → Documentation → MVP. The "Ideation"
title only covers the first 3 sections. Rename to "From Idea to MVP" to cover
the full ideation-through-prototype arc.

Ch 78 has 10 sections spanning Manufacturing (78.1-78.5), Creative Industries
(78.6-78.7), and Search/Recommendation (78.8-78.10). The "Manufacturing" title
only covers the first half. Rename to "Manufacturing, Creative Industries &
Search/Recommendation".
"""
from pathlib import Path
import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]

CHAPTERS = [
    {
        'module': 'part-14-designing-llm-agent-products/module-67-ideation',
        'ch_num': 67,
        'new_title': 'From Idea to MVP',
        'new_big_picture': 'The full ideation-to-MVP arc for LLM-based products. The chapter covers finding LLM-worthy problems (heuristics, capability mapping), going from hypothesis to product spec, the LLM-PM job, UX patterns specific to AI products, strategy and prioritization, vendor evaluation (build vs buy), risk and feasibility assessment, observe-steer development, the founder\'s prototype loop, documentation as control surface, and the prototype-to-MVP transition.',
        'sections': [
            (1, 'Ideation: Finding LLM-Worthy Problems', 'Heuristics for spotting problems where LLM economics work, and the boundaries where they do not.'),
            (2, 'Problem-Discovery Heuristics', 'A taxonomy of discovery patterns: customer interviews, log mining, workflow shadowing, the unmet-needs framework.'),
            (3, 'The Bet-My-Money Test and Capability Mapping', 'A founder-level test for filtering ideas, plus the LLM capability map you use to match problem to model.'),
            (4, 'From Hypothesis to Product Spec', 'Turning a validated idea into a concrete spec: scope, success criteria, evaluation harness, rollout strategy.'),
            (5, 'LLM Product Management', 'How the PM job changes for LLM products: model lifecycle, eval ownership, prompt drift, and the data-quality flywheel.'),
            (6, 'UX and Iteration for LLM Products', 'Streaming UIs, confidence display, undo / re-try patterns, and the iteration loops that compound over weeks.'),
            (7, 'LLM Strategy & Use Case Prioritization', 'Portfolio frameworks (high-impact vs quick-win), the moat questions, and resource-allocation patterns.'),
            (8, 'LLM Vendor Evaluation & Build vs. Buy', 'Frontier API vs open-weight vs fine-tune decision tree, with cost / quality / lock-in trade-offs.'),
            (9, 'What Makes AI Products Different', 'Non-determinism, eval-driven dev, model versioning, and the operational realities that distinguish AI products.'),
            (10, 'Choosing the Model\'s Role', 'Where the LLM sits in your product: copilot, autopilot, search, generator, judge, agent loop.'),
            (11, 'Risk and Feasibility Assessment', 'Technical risk (model capability, latency, cost), product risk (adoption, churn), and governance risk.'),
            (12, 'The Observe-Steer Development Loop', 'The 2026 dev loop: log production, find regressions, write evals, ship a fix; the LLM-specific CI/CD.'),
            (13, 'The Founder\'s Prototype Loop', 'Solo / small-team prototype tactics: vibe coding, evaluation cycles, customer co-design rhythms.'),
            (14, 'Documentation as Control Surface', 'Why writing docs is the highest-leverage activity for an LLM product: prompts, evals, runbooks, decision logs.'),
            (15, 'From Prototype to MVP', 'The hardening checklist: latency budgets, cost monitoring, eval gates, on-call playbooks, the readiness review.'),
        ],
    },
    {
        'module': 'part-15-applications-of-llms-across-industries/module-78-manufacturing-llms',
        'ch_num': 78,
        'new_title': 'Manufacturing, Creative Industries, Search &amp; Recommendation',
        'new_big_picture': 'Three industry verticals in one chapter. The first half (78.1-78.5) covers manufacturing: maintenance copilots, inspection, work-order drafting, supplier risk, ERP/MES queries, plus the IT/OT boundary and regulatory framework. The second half (78.6-78.10) covers creative industries (music, video, design, marketing copy) and search/recommendation (LLM-powered search like Perplexity, ranking, personalization, conversational discovery), each with named-vendor case studies.',
        'sections': [
            (1, 'Manufacturing Use Cases That Actually Work', 'Maintenance copilots, inspection-report drafting, work-order generation, supplier risk, ERP/MES queries that pay back.'),
            (2, 'Manufacturing Failure Modes', 'IT/OT boundary risks, prompt-injection on plant data, regulator-readiness pitfalls.'),
            (3, 'Regulatory and Standards Framework', 'ISO, IEC, FDA, and OT-cyber standards that gate manufacturing AI deployment.'),
            (4, 'Plant-Floor Maintenance Copilot Architecture', 'A reference architecture for a maintenance copilot bridging engineering documentation, sensor data, and work orders.'),
            (5, 'Manufacturing Postmortems and Named-Vendor Cases', 'Real failure stories from manufacturing AI pilots and what they teach.'),
            (6, 'Music, Video, Design & Marketing Copy', 'Creative-industry tooling: Suno, Udio, Runway, Adobe Firefly, marketing-copy stacks.'),
            (7, 'Creative-Industry Failure Modes', 'IP, attribution, deepfake liability, and the union-bargaining changes that creative AI is forcing.'),
            (8, 'Ranking, Retrieval, and Personalization', 'Where LLMs displace and augment classical ranking and recommendation pipelines.'),
            (9, 'Search Architecture for LLM Era', 'Perplexity, Google AI Overviews, Bing copilot: how LLM-powered search composes retrieval and generation.'),
            (10, 'Conversational Discovery and Named-Vendor Cases', 'Pinterest Lens, Spotify DJ, and the case studies of conversational discovery that actually shipped.'),
        ],
    },
]


def fix_chapter(ch):
    module_dir = ROOT / ch['module']
    if not module_dir.exists():
        print(f"  Missing: {ch['module']}")
        return

    idx = module_dir / 'index.html'
    text = idx.read_text(encoding='utf-8')
    ch_num = ch['ch_num']
    new_title_plain = ch['new_title'].replace('&amp;', '&')

    text = re.sub(
        rf'<title>Chapter {ch_num}:[^<]+</title>',
        f'<title>Chapter {ch_num}: {new_title_plain} | Building Conversational AI with LLMs and Agents</title>',
        text
    )
    text = re.sub(
        rf'(<meta content=")Chapter {ch_num}:[^"]+(" name="description")',
        rf'\1Chapter {ch_num}: {new_title_plain}. {ch["new_big_picture"][:100]}\2',
        text
    )
    text = re.sub(
        r'<h1>[^<]+</h1>',
        f'<h1>{ch["new_title"]}</h1>',
        text,
        count=1
    )
    text = re.sub(
        rf'(<span class="pagefind-meta-injected" data-pagefind-meta="chapter:Chapter {ch_num}:)[^"]+(")',
        rf'\1 {new_title_plain}\2',
        text
    )
    text = re.sub(
        r'(<div class="callout big-picture">\s*<div class="callout-title">Big Picture</div>\s*<p>)[^<]+(</p>)',
        rf'\1{ch["new_big_picture"]}\2',
        text,
        count=1
    )
    cards = []
    for sec_n, sec_title, sec_desc in ch['sections']:
        cards.append(
            f'<li><a class="section-card" href="section-{ch_num}.{sec_n}.html">\n'
            f'<span class="section-num">{ch_num}.{sec_n}</span>\n'
            f'<span class="section-title">{sec_title}</span>\n'
            f'<span class="section-desc">{sec_desc}</span>\n'
            f'</a></li>'
        )
    if '<ul class="sections-list">' in text:
        text = re.sub(
            r'<ul class="sections-list">[\s\S]*?</ul>',
            '<ul class="sections-list">\n' + '\n'.join(cards) + '\n</ul>',
            text,
            count=1
        )
    idx.write_text(text, encoding='utf-8')
    print(f"  Fixed Ch {ch_num} ({new_title_plain})")


def main():
    for ch in CHAPTERS:
        fix_chapter(ch)


if __name__ == '__main__':
    main()
