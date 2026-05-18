"""Wave 15: miscellaneous structural fixes from content-audit cycle 1.

  1. Rename Ch 52 to "Bias, Fairness & Hallucinations" (section 52.2 is
     Hallucinations, currently lives in Bias chapter as orphan)
  2. Rename Ch 54 to "Provenance, Watermarking & Transparency" (sections
     54.6-54.10 cover transparency, missing from index)
  3. Rename Ch 55 to "Environmental Impact & AI Governance" (section 55.2
     is Governance, currently orphan in Env chapter)
  4. Add missing section cards to each chapter's index from filesystem reality
  5. Update Part 11 part-index to reflect new chapter titles
"""
from pathlib import Path
import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]

CHAPTERS = [
    {
        'module': 'part-11-llm-ethics-trust-governance/module-52-bias-fairness',
        'ch_num': 52,
        'new_title': 'Bias, Fairness &amp; Hallucinations',
        'new_big_picture': 'Two of the most common LLM trust failures: biased outputs and hallucinations. This chapter covers the algorithmic fairness frameworks (demographic parity, equalized odds), bias measurement and mitigation across pretraining and fine-tuning, plus why models hallucinate, the failure mode taxonomy, and the detection and prevention techniques that catch hallucinations before users see them.',
        'sections': [
            (1, 'Bias, Fairness, and Ethics', 'Demographic parity, equalized odds, calibration, and the algorithmic-fairness frameworks for LLM outputs.'),
            (2, 'Why LLMs Hallucinate and How to Catch Them', 'Hallucination taxonomy, detection techniques, retrieval-grounded checks, and the production patterns that prevent them.'),
        ],
    },
    {
        'module': 'part-11-llm-ethics-trust-governance/module-54-watermarking-provenance',
        'ch_num': 54,
        'new_title': 'Provenance, Watermarking &amp; Transparency',
        'new_big_picture': 'The disclosure layer of responsible AI. The first half covers provenance and watermarking: text watermarking (Kirchenbauer green-list, SynthID-Text), image and video provenance (C2PA, SynthID-Image, Content Credentials), deepfake detection, and the adversarial cat-and-mouse. The second half covers transparency mechanisms: model cards, datasheets for datasets, system cards, audit trails for compliance, and explainability for high-stakes decisions.',
        'sections': [
            (1, 'Why Provenance Matters', 'The business and regulatory case for provenance, plus the threats provenance does and does not address.'),
            (2, 'Text Watermarking: Kirchenbauer Green-List and SynthID-Text', 'Algorithmic text watermarking techniques, their detection accuracy, and their robustness to paraphrasing.'),
            (3, 'Image and Video Provenance: C2PA, SynthID-Image, Adobe Content Credentials', 'Cryptographic content credentials, signed media, and the adoption story for provenance metadata.'),
            (4, 'Deepfake and Synthetic-Media Detection', 'Classifier-based detection, biometric anti-spoofing, and the limits of detection-only approaches.'),
            (5, 'Limitations: Adversarial Watermark Removal and the Cat-and-Mouse Game', 'Paraphrase attacks, copy-paste attacks, the inherent unforgeability tradeoffs, and the hardness of universal watermarks.'),
            (6, 'Model Cards: Anatomy, Examples, Use in Procurement', 'The model-card template, what to include, how to consume them in vendor selection.'),
            (7, 'Datasheets for Datasets', 'Documenting training data provenance, consent, and known biases for downstream consumers.'),
            (8, 'System Cards and Frontier System Disclosures', 'OpenAI and Anthropic system cards, the safety evaluation disclosure pattern, and what they reveal.'),
            (9, 'Audit Trails and Logging for Compliance', 'What to log to be audit-ready, retention, and the GDPR/EU AI Act disclosure obligations.'),
            (10, 'Explainability for High-Stakes Decisions', 'Where black-box explanations fall short, the role of structured prompting + verifiable rationales, and the regulatory push for explainability.'),
        ],
    },
    {
        'module': 'part-11-llm-ethics-trust-governance/module-55-environmental-sustainability',
        'ch_num': 55,
        'new_title': 'Environmental Impact &amp; AI Governance',
        'new_big_picture': 'The macro-level questions: environmental cost and governance. The first half covers Green AI (training and inference energy, water, hardware lifecycle, carbon accounting for ML workloads). The second half covers AI governance frameworks (EU AI Act, NIST RMF, ISO 42001), open governance problems (international coordination, frontier risk, capability evaluations), and where the regulatory landscape is heading.',
        'sections': [
            (1, 'Environmental Impact and Green AI', 'Training and inference energy and water budgets, hardware lifecycle, carbon accounting, and the green-AI techniques that materially help.'),
            (2, 'AI Governance and Open Problems', 'EU AI Act, NIST AI RMF, ISO 42001, international coordination challenges, and the open governance questions of frontier AI.'),
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

    # Update title tag
    text = re.sub(
        rf'<title>Chapter {ch_num}:[^<]+</title>',
        f'<title>Chapter {ch_num}: {new_title_plain} | Building Conversational AI with LLMs and Agents</title>',
        text
    )
    # Update meta description
    text = re.sub(
        rf'(<meta content=")Chapter {ch_num}:[^"]+(" name="description")',
        rf'\1Chapter {ch_num}: {new_title_plain}. {ch["new_big_picture"][:100]}\2',
        text
    )
    # Update h1
    text = re.sub(
        r'<h1>[^<]+</h1>',
        f'<h1>{ch["new_title"]}</h1>',
        text,
        count=1
    )
    # Update pagefind chapter meta
    text = re.sub(
        rf'(<span class="pagefind-meta-injected" data-pagefind-meta="chapter:Chapter {ch_num}:)[^"]+(")',
        rf'\1 {new_title_plain}\2',
        text
    )
    # Update big-picture text
    text = re.sub(
        r'(<div class="callout big-picture">\s*<div class="callout-title">Big Picture</div>\s*<p>)[^<]+(</p>)',
        rf'\1{ch["new_big_picture"]}\2',
        text,
        count=1
    )
    # Rebuild sections-list
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
