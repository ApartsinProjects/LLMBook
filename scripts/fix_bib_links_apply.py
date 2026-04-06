#!/usr/bin/env python3
"""Add hyperlinks to bibliography entries that lack them."""
import os
import re
import sys

# Map of (author_key, partial_title) -> URL
# We'll match by searching for substrings in the bib entry text
LINK_MAP = [
    # appendices/appendix-a section-a.5
    ("Shannon", "Mathematical Theory of Communication",
     "https://doi.org/10.1002/j.1538-7305.1948.tb01338.x"),

    # appendices/appendix-b section-b.4
    ("Papineni", "BLEU",
     "https://doi.org/10.3115/1073083.1073135"),
    ("Zhang", "BERTScore",
     "https://arxiv.org/abs/1904.09675"),

    # part-1 module-01 section-1.1
    ("Manning", "Foundations of Statistical Natural Language Processing",
     "https://nlp.stanford.edu/fsnlp/"),

    # part-1 module-02 section-2.1
    ("Schuster", "Japanese and Korean Voice Search",
     "https://doi.org/10.1109/ICASSP.2012.6289079"),

    # part-1 module-03 section-3.1
    ("Elman", "Finding Structure in Time",
     "https://doi.org/10.1016/0364-0213(90)90002-E"),
    ("Bengio", "Learning Long-Term Dependencies",
     "https://doi.org/10.1109/72.279181"),

    # part-1 module-03 section-3.3
    ("Vaswani", "Attention Is All You Need",
     "https://arxiv.org/abs/1706.03762"),
    ("Dao", "FlashAttention: Fast and Memory-Efficient",
     "https://arxiv.org/abs/2205.14135"),
    ("Ainslie", "GQA: Training Generalized Multi-Query",
     "https://arxiv.org/abs/2305.13245"),

    # part-1 module-04 section-4.1
    # Vaswani already covered above (will match)
    ("Radford", "Language Models are Unsupervised Multitask Learners",
     "https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf"),
    ("Xiong", "On Layer Normalization in the Transformer",
     "https://arxiv.org/abs/2002.04745"),

    # part-1 module-04 section-4.4
    ("Dao", "FlashAttention-2",
     "https://arxiv.org/abs/2307.08691"),
    ("Tillet", "Triton: An Intermediate Language",
     "https://arxiv.org/abs/1903.04174"),
    ("Ivanov", "Data Movement Is All You Need",
     "https://arxiv.org/abs/2007.00072"),

    # part-1 module-04 section-4.5
    ("Yun", "Are Transformers universal approximators",
     "https://arxiv.org/abs/1912.10077"),
    ("Merrill", "Expressive Power of Transformers with Chain of Thought",
     "https://arxiv.org/abs/2310.07923"),
    ("Wei, C", "Statistically Meaningful Approximation",
     "https://arxiv.org/abs/2107.13163"),

    # part-11 module-37 section-37.2
    ("Ries", "The Lean Startup",
     "https://theleanstartup.com/"),
    # part-11 module-37 section-37.5 (Ries duplicate handled, Nygard below)
    ("Nygard", "Release It",
     "https://pragprog.com/titles/mnee2/release-it-second-edition/"),

    # part-3 module-10 section-10.3 (Nygard duplicate, same URL)

    # part-4 module-13 section-13.5
    ("Cohen", "Coefficient of Agreement for Nominal Scales",
     "https://doi.org/10.1177/001316446002000104"),

    # part-5 module-21 section-21.7
    ("Vaithilingam", "RealHumanEval",
     "https://arxiv.org/abs/2404.02806"),
    ("Amershi", "Guidelines for Human-AI Interaction",
     "https://doi.org/10.1145/3290605.3300233"),
    ("Bansal", "Does the Whole Exceed its Parts",
     "https://doi.org/10.1145/3411764.3445717"),
    ("inca", "To Trust or to Think",  # Buçinca - matching partial
     "https://doi.org/10.1145/3449287"),
    ("Lee, M", "Evaluating Human-Language Model Interaction",
     "https://arxiv.org/abs/2212.09746"),
    ("Nass", "Machines and Mindlessness",
     "https://doi.org/10.1111/0022-4537.00153"),
    ("Parasuraman", "Humans and Automation",
     "https://doi.org/10.1518/001872097778543886"),
    ("Shneiderman", "Human-Centered AI",
     "https://global.oup.com/academic/product/human-centered-ai-9780192845290"),

    # part-6 module-25 section-25.7
    ("Cognition Labs", "Introducing Devin",
     "https://www.cognition.ai/blog/introducing-devin"),
    ("GitHub", "Copilot Workspace",
     "https://githubnext.com/projects/copilot-workspace"),
    ("Jimenez", "SWE-bench",
     "https://arxiv.org/abs/2310.06770"),
    ("GitHub", "Octoverse 2025",
     "https://github.blog/news-insights/octoverse/octoverse-2024/"),

    # part-7 module-27 section-27.6
    ("Liu, X", "Hierarchical Language Models for Coordinated Aerial",
     "https://arxiv.org/abs/2501.16521"),

    # part-8 module-29 section-29.12
    ("Landis", "Measurement of Observer Agreement",
     "https://doi.org/10.2307/2529310"),
    ("Krippendorff", "Reliability in Content Analysis",
     "https://doi.org/10.1111/j.1468-2958.2004.tb00738.x"),

    # part-8 module-29 section-29.13
    ("Krippendorff", "Content Analysis: An Introduction to Its Methodology",
     "https://us.sagepub.com/en-us/nam/content-analysis/book258450"),

    # part-8 module-29 section-29.8
    ("Bradley", "Rank Analysis of Incomplete Block Designs",
     "https://doi.org/10.1093/biomet/39.3-4.324"),
    ("Elo", "Rating of Chessplayers",
     "https://www.google.com/books/edition/The_Rating_of_Chessplayers_Past_and_Pres/8pMnAAAACAAJ"),

    # part-8 module-30 section-30.4 (Bradley and Elo duplicates)

    # part-9 module-32 section-32.8
    ("Zou", "Universal and Transferable Adversarial Attacks",
     "https://arxiv.org/abs/2307.15043"),
    ("Mazeika", "HarmBench",
     "https://arxiv.org/abs/2402.04249"),
    ("Perez", "Red Teaming Language Models with Language Models",
     "https://arxiv.org/abs/2202.03286"),
    ("Greshake", "Not What You",
     "https://arxiv.org/abs/2302.12173"),
    ("Ganguli", "Red Teaming Language Models to Reduce Harms",
     "https://arxiv.org/abs/2209.07858"),
    ("OWASP", "OWASP Top 10 for LLM",
     "https://owasp.org/www-project-top-10-for-large-language-model-applications/"),
    ("NIST", "AI Risk Management Framework",
     "https://doi.org/10.6028/NIST.AI.600-1"),

    # part-9 module-32 section-32.9
    ("European Parliament", "Regulation (EU) 2024/1689",
     "https://eur-lex.europa.eu/eli/reg/2024/1689/oj"),
    ("European Commission", "AI Act: General-Purpose AI Model",
     "https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai"),
    ("NIST", "Artificial Intelligence Risk Management Framework (AI RMF 1.0)",
     "https://doi.org/10.6028/NIST.AI.100-1"),
    ("NIST", "AI RMF Generative AI Profile",
     "https://doi.org/10.6028/NIST.AI.600-1"),
    ("ISO/IEC", "ISO/IEC 42001",
     "https://www.iso.org/standard/81230.html"),
    ("High-Level Expert Group", "Assessment List for Trustworthy AI",
     "https://digital-strategy.ec.europa.eu/en/library/assessment-list-trustworthy-artificial-intelligence-altai-self-assessment"),
    ("Veale", "Demystifying the Draft EU",
     "https://doi.org/10.9785/cri-2021-220402"),
    ("Hacker", "European AI Liability",
     "https://arxiv.org/abs/2311.13601"),

    # part-9 module-32 section-32.11
    ("Strubell", "Energy and Policy Considerations",
     "https://arxiv.org/abs/1906.02243"),
    ("Patterson", "Carbon Emissions and Large Neural Network",
     "https://arxiv.org/abs/2104.10350"),
    ("Schwartz", "Green AI",
     "https://arxiv.org/abs/1907.10597"),
    ("Hoffmann", "Training Compute-Optimal",
     "https://arxiv.org/abs/2203.15556"),
    ("Lannelongue", "Green Algorithms",
     "https://doi.org/10.1002/advs.202100707"),
    ("CodeCarbon", "Track and Reduce CO2",
     "https://github.com/mlco2/codecarbon"),
    ("Lacoste", "Quantifying the Carbon Emissions",
     "https://arxiv.org/abs/1910.09700"),
    ("European Parliament", "Artificial Intelligence Act",
     "https://eur-lex.europa.eu/eli/reg/2024/1689/oj"),

    # part-9 module-32 section-32.12
    ("Carlini", "Extracting Training Data from Large Language",
     "https://arxiv.org/abs/2012.07805"),
    ("Carlini", "Quantifying Memorization Across Neural",
     "https://arxiv.org/abs/2202.07646"),
    ("Abadi", "Deep Learning with Differential Privacy",
     "https://arxiv.org/abs/1607.00133"),
    ("Yousefpour", "Opacus",
     "https://arxiv.org/abs/2109.12298"),
    ("Nissenbaum", "Privacy as Contextual Integrity",
     "https://doi.org/10.2139/ssrn.534622"),
    ("Shokri", "Membership Inference Attacks",
     "https://arxiv.org/abs/1610.05820"),
    ("Li, X", "Large Language Models Can Be Strong Differentially Private",
     "https://arxiv.org/abs/2110.05679"),
    ("Microsoft Presidio", "Data Protection and De-identification",
     "https://github.com/microsoft/presidio"),

    # part-9 module-33 section-33.6
    ("a16z", "Economics of AI Infrastructure",
     "https://a16z.com/the-economic-case-for-generative-ai-and-foundation-models/"),
    ("Semianalysis", "GPU Cloud Economics",
     "https://www.semianalysis.com/"),
    ("Bain", "Open-Weight vs. Proprietary Models",
     "https://gradientflow.com/"),
    ("Patterson", "Carbon Footprint of Machine Learning Training Will Plateau",
     "https://doi.org/10.1109/MC.2022.3148714"),
    ("Bommasani", "Opportunities and Risks of Foundation Models",
     "https://arxiv.org/abs/2108.07258"),
    ("Narayanan", "Cheaply Estimating Inference Efficiency",
     "https://arxiv.org/abs/2305.02440"),
    ("LLMOps", "State of LLM Deployment",
     None),  # Skip - can't determine URL

    # part-9 module-33 section-33.7
    ("Hardt, D", "OAuth 2.0 Authorization Framework",
     "https://datatracker.ietf.org/doc/html/rfc6749"),
    ("Sakimura", "OpenID Connect Core",
     "https://openid.net/specs/openid-connect-core-1_0.html"),
    # OWASP duplicate handled above
    ("Microsoft", "Azure AI Content Safety",
     "https://learn.microsoft.com/en-us/azure/ai-services/content-safety/"),
    ("Anthropic", "Enterprise Security and Compliance",
     "https://docs.anthropic.com/en/docs/build-with-claude/enterprise-security"),

    # part-9 module-33 section-33.8
    ("Chen", "FrugalGPT",
     "https://arxiv.org/abs/2305.05176"),
    # a16z duplicate handled above
    ("Bang", "Survey on LLM-as-a-Judge",
     "https://arxiv.org/abs/2310.17631"),

    # part-5 module-21 section-21.6 - check if needed
]


def find_best_url(entry_text):
    """Find the best matching URL for a bib entry."""
    for author_key, title_key, url in LINK_MAP:
        if url is None:
            continue
        if author_key in entry_text and title_key in entry_text:
            return url
    return None


def find_title_in_entry(inner_text):
    """Extract the title from a bib entry to wrap with <a> tag.

    Handles patterns like:
    - "Title Here." or "Title Here." (with smart quotes)
    - <em>Book Title</em>
    """
    # Try quoted title first (regular or smart quotes)
    # Pattern: opening quote, then content up to closing quote
    m = re.search(r'["\u201c](.*?)["\u201d]', inner_text)
    if m:
        return m.group(0), m.start(), m.end()

    # Try <em>Title</em> for books
    m = re.search(r'<em>(.*?)</em>', inner_text)
    if m:
        return m.group(0), m.start(), m.end()

    return None, None, None


def add_link_to_entry(inner_text, url):
    """Add an <a> tag wrapping the title in the bib entry."""
    title_str, start, end = find_title_in_entry(inner_text)
    if title_str is None:
        return None

    # Don't wrap if already has a link (cross-ref etc)
    if '<a ' in title_str:
        # Wrap the whole inner text instead
        return f'<a href="{url}" target="_blank" rel="noopener">{inner_text.strip()}</a>'

    linked = f'<a href="{url}" target="_blank" rel="noopener">{title_str}</a>'
    new_inner = inner_text[:start] + linked + inner_text[end:]
    return new_inner


def process_files():
    files_to_check = []
    for root, dirs, fnames in os.walk('.'):
        dirs[:] = [d for d in dirs if d != '_archive']
        norm = root.replace(os.sep, '/')
        if 'part-10-frontiers' in norm:
            continue
        for f in fnames:
            if f.endswith('.html') and (f.startswith('section-') or f == 'index.html'):
                fp = os.path.join(root, f).replace(os.sep, '/')
                if '/part-' in fp or '/appendix' in fp or '/appendices/' in fp:
                    files_to_check.append(fp)

    total_fixed = 0
    total_skipped = 0

    for fp in sorted(files_to_check):
        with open(fp, 'r', encoding='utf-8') as fh:
            content = fh.read()

        original = content
        # Find all bib-ref entries without links, working backwards to preserve positions
        entries = []
        for m in re.finditer(r'<p\s+class=[^>]*bib-ref[^>]*>', content):
            start = m.start()
            tag_end = m.end()
            end_p = content.find('</p>', start)
            if end_p < 0:
                continue
            inner = content[tag_end:end_p]
            if '<a href=' not in inner:
                entries.append((start, tag_end, end_p, inner))

        if not entries:
            continue

        # Process in reverse order to preserve positions
        for start, tag_end, end_p, inner in reversed(entries):
            url = find_best_url(inner)
            if url is None:
                clean = inner.strip().replace('\n', ' ').replace('\r', '')[:100]
                print(f'  SKIP {fp}: {clean}')
                total_skipped += 1
                continue

            new_inner = add_link_to_entry(inner, url)
            if new_inner is None:
                clean = inner.strip().replace('\n', ' ').replace('\r', '')[:100]
                print(f'  NO_TITLE {fp}: {clean}')
                total_skipped += 1
                continue

            content = content[:tag_end] + '\n ' + new_inner.strip() + '\n ' + content[end_p:]
            total_fixed += 1

        if content != original:
            with open(fp, 'w', encoding='utf-8', newline='') as fh:
                fh.write(content)
            print(f'  FIXED {fp}')

    print(f'\nTotal fixed: {total_fixed}, Skipped: {total_skipped}')


if __name__ == '__main__':
    process_files()
