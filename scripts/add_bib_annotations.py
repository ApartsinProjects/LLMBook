#!/usr/bin/env python3
"""Add bib-annotation paragraphs to bibliography entries in specified files."""
import re
import os

# Annotations keyed by (filename, author_substring)
# Each value is the annotation text
ANNOTATIONS = {
    # section-21.7.html - Human-AI Interaction in Conversational AI
    ("section-21.7.html", "Vaithilingam"): (
        "Introduces a benchmark for evaluating how well LLMs support real programming tasks, "
        "going beyond code-completion accuracy to measure actual developer productivity and satisfaction."
    ),
    ("section-21.7.html", "Amershi"): (
        "Establishes 18 design guidelines for human-AI interaction based on extensive user research at Microsoft. "
        "A foundational reference for anyone building conversational interfaces that pair users with AI assistants."
    ),
    ("section-21.7.html", "Bansal"): (
        "Investigates whether AI explanations actually help human-AI teams make better decisions. "
        "The findings challenge assumptions about transparency and highlight when explanations help versus hurt."
    ),
    ("section-21.7.html", "inca"): (  # Buçinca
        "Demonstrates that cognitive forcing functions (requiring users to commit to an answer before seeing AI output) "
        "reduce overreliance on AI. Directly applicable to designing conversational systems that keep users critically engaged."
    ),
    ("section-21.7.html", "Lee, M"): (
        "Proposes evaluation dimensions for human-LM interaction beyond task accuracy, "
        "including user experience, trust calibration, and interaction efficiency. Useful for designing holistic evaluation of conversational AI."
    ),
    ("section-21.7.html", "Nass"): (
        "Foundational study showing that people apply social rules to computers unconsciously, "
        "even when they know the computer is not human. Essential context for understanding why conversational AI persona design matters."
    ),
    ("section-21.7.html", "Parasuraman"): (
        "Classic taxonomy of automation failures: using automation when it should not be trusted (misuse), "
        "ignoring reliable automation (disuse), and designing automation that degrades human skills (abuse). Directly relevant to conversational AI deployment."
    ),
    ("section-21.7.html", "Shneiderman"): (
        "A comprehensive framework for designing AI systems that augment rather than replace human capabilities. "
        "Provides principles for building conversational AI that maintains meaningful human agency and oversight."
    ),

    # section-25.7.html - Specialized Agents (Coding Agents)
    ("section-25.7.html", "Anthropic"): (
        "Official documentation for Claude Code, an agentic coding tool that operates in the terminal. "
        "Covers architecture patterns, tool use, and best practices relevant to this section's discussion of coding agents."
    ),
    ("section-25.7.html", "OpenAI. (2025). \"Codex"): (
        "Documentation for OpenAI's autonomous coding agent, which handles multi-file tasks in a sandboxed cloud environment. "
        "Illustrates the fully autonomous end of the coding agent spectrum discussed in this section."
    ),
    ("section-25.7.html", "Cursor"): (
        "Documentation for Cursor, an AI-native code editor that integrates LLM assistance directly into the IDE experience. "
        "Representative of the editor-integrated approach to coding agents."
    ),
    ("section-25.7.html", "Cognition Labs"): (
        "Introduces Devin, a fully autonomous coding agent capable of planning, executing, and debugging multi-step software tasks. "
        "A key reference point for understanding the capabilities and limitations of autonomous coding agents."
    ),
    ("section-25.7.html", "Copilot Workspace"): (
        "Describes GitHub's approach to issue-to-pull-request automation, "
        "bridging the gap between issue tracking and code generation with human review at each stage."
    ),
    ("section-25.7.html", "Jimenez"): (
        "Introduces SWE-bench, the standard benchmark for evaluating coding agents on real-world GitHub issues. "
        "Essential for understanding how coding agent performance is measured and compared across systems."
    ),
    ("section-25.7.html", "Octoverse"): (
        "Annual report on software development trends, including AI-assisted coding adoption rates and impact metrics. "
        "Provides empirical context for the adoption patterns discussed in this section."
    ),

    # section-32.8.html - Safety: Adversarial Attacks and Red Teaming
    ("section-32.8.html", "Zou"): (
        "Demonstrates that adversarial suffixes can bypass safety alignment in multiple LLMs simultaneously. "
        "A wake-up call for the field, showing that current alignment techniques have systematic vulnerabilities."
    ),
    ("section-32.8.html", "Mazeika"): (
        "Provides a standardized framework and benchmark for evaluating both automated red teaming methods and model robustness to jailbreaks. "
        "Essential for any team building systematic safety evaluations."
    ),
    ("section-32.8.html", "PyRIT"): (
        "Microsoft's open-source toolkit for automated red teaming of generative AI systems. "
        "A practical starting point for teams building their own red teaming pipelines."
    ),
    ("section-32.8.html", "Perez"): (
        "Pioneering work on using LLMs to automatically generate test cases that expose failures in other LLMs. "
        "Established the paradigm of scalable, automated red teaming that now underpins most safety evaluation workflows."
    ),
    ("section-32.8.html", "Greshake"): (
        "Demonstrates indirect prompt injection attacks where malicious instructions are embedded in external content retrieved by LLM applications. "
        "Critical reading for anyone building RAG systems or tool-using agents."
    ),
    ("section-32.8.html", "Ganguli"): (
        "Anthropic's systematic study of red teaming practices, documenting attack taxonomies and the effectiveness of various safety interventions. "
        "Provides practical guidance for organizing red teaming exercises."
    ),
    ("section-32.8.html", "OWASP"): (
        "Industry-standard catalog of the most critical security risks in LLM applications, from prompt injection to supply chain vulnerabilities. "
        "A practical checklist for security reviews of any LLM deployment."
    ),
    ("section-32.8.html", "NIST"): (
        "The U.S. government's framework for identifying and mitigating AI risks, including generative AI-specific guidance. "
        "Provides a structured approach to risk management that maps to regulatory compliance requirements."
    ),

    # section-32.9.html - Regulation and Compliance
    ("section-32.9.html", "European Parliament"): (
        "The full text of the EU AI Act, the world's first comprehensive AI regulation. "
        "Establishes risk-based classification tiers and specific obligations for general-purpose AI model providers."
    ),
    ("section-32.9.html", "European Commission"): (
        "Official guidance on how the AI Act applies to general-purpose AI models, including transparency and systemic risk obligations. "
        "Essential for teams deploying foundation models in the EU market."
    ),
    ("section-32.9.html", "NIST. (2023)"): (
        "The foundational U.S. framework for AI risk management, providing a structured approach to identifying, assessing, and mitigating AI risks. "
        "Widely adopted as a voluntary standard by organizations seeking to demonstrate responsible AI practices."
    ),
    ("section-32.9.html", "NIST. (2024)"): (
        "Extends the AI RMF specifically for generative AI, addressing unique risks such as hallucination, data poisoning, and CSAM generation. "
        "Provides actionable guidance beyond the base framework."
    ),
    ("section-32.9.html", "ISO/IEC"): (
        "The international standard for AI management systems, providing a certifiable framework for organizational AI governance. "
        "Increasingly required by enterprise procurement processes and regulatory bodies."
    ),
    ("section-32.9.html", "High-Level Expert"): (
        "A practical self-assessment checklist for evaluating AI systems against trustworthiness requirements. "
        "Useful as a structured audit tool even outside the EU regulatory context."
    ),
    ("section-32.9.html", "Veale"): (
        "Legal analysis of the EU AI Act's draft provisions, identifying ambiguities and implementation challenges. "
        "Helpful for understanding the regulatory intent behind specific articles and their practical implications."
    ),
    ("section-32.9.html", "Hacker"): (
        "Analyzes the EU's AI liability framework, explaining how product liability and fault-based liability apply to AI systems. "
        "Critical reading for teams assessing legal exposure from AI deployment in European markets."
    ),

    # section-32.11.html - Environmental Impact
    ("section-32.11.html", "Strubell"): (
        "Landmark study quantifying the carbon emissions of training large NLP models, finding that training a single Transformer can emit as much CO2 as five cars over their lifetimes. "
        "Catalyzed the green AI movement and remains a key reference for environmental impact discussions."
    ),
    ("section-32.11.html", "Patterson"): (
        "Comprehensive measurement of carbon emissions from training large neural networks at Google, with practical recommendations for reducing environmental impact. "
        "Provides the empirical basis for many of this section's quantitative claims."
    ),
    ("section-32.11.html", "Schwartz"): (
        "Proposes the concept of Green AI, arguing that the field should prioritize computational efficiency alongside accuracy. "
        "Introduces reporting standards for compute costs that have influenced conference submission requirements."
    ),
    ("section-32.11.html", "Hoffmann"): (
        "The Chinchilla paper demonstrates that most large models are over-parameterized relative to their training data, "
        "showing that compute-optimal training can achieve better performance with less energy by balancing model size and data volume."
    ),
    ("section-32.11.html", "Lannelongue"): (
        "Introduces an online calculator for estimating the carbon footprint of computational workloads. "
        "A practical tool for researchers and teams wanting to quantify and report the environmental impact of their AI experiments."
    ),
    ("section-32.11.html", "CodeCarbon"): (
        "Open-source Python library that automatically tracks energy consumption and carbon emissions during model training and inference. "
        "Drop-in integration for PyTorch and TensorFlow workflows, enabling transparent emissions reporting."
    ),
    ("section-32.11.html", "Lacoste"): (
        "Proposes a standardized methodology for estimating ML carbon emissions based on hardware, runtime, and energy grid carbon intensity. "
        "The methodology underpins several carbon tracking tools referenced in this section."
    ),
    ("section-32.11.html", "European Parliament"): (
        "Article 53 of the EU AI Act requires providers of general-purpose AI models to report estimated energy consumption during training. "
        "A concrete example of how environmental reporting is becoming a regulatory obligation."
    ),

    # section-32.12.html - Privacy and Data Protection
    ("section-32.12.html", "Carlini, N. et al. (2021)"): (
        "Demonstrates that GPT-2 memorizes and can reproduce verbatim training data, including personal information. "
        "Established that memorization is a fundamental privacy risk in large language models, not just a theoretical concern."
    ),
    ("section-32.12.html", "Carlini, N. et al. (2023)"): (
        "Systematically measures how memorization scales with model size, finding that larger models memorize more training data. "
        "Provides the empirical foundation for this section's discussion of memorization risks."
    ),
    ("section-32.12.html", "Abadi"): (
        "The foundational paper on training deep learning models with formal differential privacy guarantees. "
        "Introduces the DP-SGD algorithm that remains the primary approach for privacy-preserving model training."
    ),
    ("section-32.12.html", "Yousefpour"): (
        "Documentation and paper for Opacus, PyTorch's official differential privacy library. "
        "The most practical entry point for implementing DP-SGD in existing PyTorch training pipelines."
    ),
    ("section-32.12.html", "Nissenbaum"): (
        "Introduces contextual integrity as a framework for reasoning about privacy, arguing that privacy norms depend on information flows within specific social contexts. "
        "Provides the theoretical foundation for evaluating when AI data usage violates user expectations."
    ),
    ("section-32.12.html", "Shokri"): (
        "Introduces membership inference attacks, showing that an adversary can determine whether a specific data point was in the training set. "
        "A key threat model for understanding privacy risks in machine learning deployments."
    ),
    ("section-32.12.html", "Li, X"): (
        "Shows that large language models can achieve strong task performance while maintaining differential privacy guarantees, "
        "challenging the assumption that privacy and utility are fundamentally at odds in the LLM setting."
    ),
    ("section-32.12.html", "Microsoft Presidio"): (
        "Open-source SDK for detecting and anonymizing personally identifiable information (PII) in text. "
        "A practical tool for preprocessing training data and sanitizing LLM inputs and outputs in privacy-sensitive applications."
    ),

    # section-33.6.html - Infrastructure Costs
    ("section-33.6.html", "a16z"): (
        "Detailed analysis of GPU, cloud, and inference costs for AI infrastructure, including cost projections and optimization strategies. "
        "Essential reading for teams building financial models for LLM deployments."
    ),
    ("section-33.6.html", "Semianalysis"): (
        "In-depth comparison of GPU cloud pricing across providers, analyzing cost-per-token economics for different hardware configurations. "
        "Useful for making informed infrastructure procurement decisions."
    ),
    ("section-33.6.html", "Bain"): (
        "Practical comparison of open-weight and proprietary model economics, including total cost of ownership analysis. "
        "Helps teams evaluate the build-versus-buy decision for their specific use case and scale."
    ),
    ("section-33.6.html", "Patterson"): (
        "Argues that ML training's carbon footprint will plateau as hardware efficiency improves and renewable energy adoption increases. "
        "Provides important context for long-term infrastructure planning and environmental impact projections."
    ),
    ("section-33.6.html", "Bommasani"): (
        "Comprehensive Stanford HAI report covering the economic, technical, and societal dimensions of foundation models. "
        "Provides the broad context for understanding why infrastructure cost decisions have strategic implications beyond engineering."
    ),
    ("section-33.6.html", "Narayanan"): (
        "Proposes efficient methods for estimating inference cost and throughput without running full benchmarks. "
        "Practically useful for capacity planning and cost estimation during the design phase of LLM applications."
    ),
    ("section-33.6.html", "LLMOps"): (
        "Community survey capturing real-world deployment patterns, infrastructure choices, and cost benchmarks from practitioners. "
        "Provides empirical grounding for the cost ranges and optimization strategies discussed in this section."
    ),

    # section-33.7.html - Security Architecture
    ("section-33.7.html", "Hardt"): (
        "The authoritative specification for OAuth 2.0, the authorization framework underlying most API authentication in LLM applications. "
        "Essential reference for implementing secure API key management and user delegation patterns."
    ),
    ("section-33.7.html", "Sakimura"): (
        "The OpenID Connect specification that builds identity verification on top of OAuth 2.0. "
        "Directly relevant to implementing user authentication in multi-tenant LLM applications."
    ),
    ("section-33.7.html", "OWASP"): (
        "Security-focused catalog of LLM-specific vulnerabilities, from prompt injection to insecure output handling. "
        "The starting checklist for any security review of an LLM-powered application."
    ),
    ("section-33.7.html", "Cedar"): (
        "AWS's open-source authorization policy language designed for fine-grained access control. "
        "Relevant to implementing the principle of least privilege for tool-using agents discussed in this section."
    ),
    ("section-33.7.html", "HashiCorp"): (
        "Documentation for Vault, a widely used secrets management platform. "
        "Practical reference for securing API keys, model credentials, and other secrets in LLM deployment pipelines."
    ),
    ("section-33.7.html", "Microsoft"): (
        "Azure's content safety service for detecting harmful content in AI-generated text and images. "
        "A practical option for implementing the output filtering guardrails discussed in this section."
    ),
    ("section-33.7.html", "Anthropic"): (
        "Anthropic's enterprise security documentation covering data handling, compliance certifications, and security architecture. "
        "Useful reference for understanding provider-side security guarantees when using managed LLM APIs."
    ),

    # section-33.8.html - Cost Optimization
    ("section-33.8.html", "Chen"): (
        "Introduces strategies for reducing LLM API costs, including model cascading, prompt adaptation, and caching. "
        "The foundational paper for the cost optimization techniques discussed throughout this section."
    ),
    ("section-33.8.html", "Anthropic"): (
        "Official documentation for Anthropic's prompt caching feature, which reduces costs and latency for repeated prompt prefixes. "
        "Directly relevant to the caching strategies discussed in this section."
    ),
    ("section-33.8.html", "OpenAI"): (
        "OpenAI's pricing page with token-level cost breakdowns for each model tier. "
        "Essential reference for the cost calculations and model selection decisions in this section."
    ),
    ("section-33.8.html", "a16z"): (
        "Analyzes the economics of AI infrastructure at scale, including how costs evolve as applications grow from prototype to production. "
        "Provides strategic context for the tactical optimizations discussed in this section."
    ),
    ("section-33.8.html", "Bang"): (
        "Surveys the use of LLMs as automated evaluators, relevant to the quality-monitoring aspect of cost optimization. "
        "Understanding LLM-as-judge reliability helps teams balance evaluation costs against human annotation budgets."
    ),
    ("section-33.8.html", "Vllm"): (
        "Documentation for vLLM, a high-throughput inference engine that uses PagedAttention for efficient memory management. "
        "The primary tool for teams self-hosting models who want to maximize throughput per GPU dollar."
    ),
    ("section-33.8.html", "GPTCache"): (
        "Open-source semantic caching library that stores and retrieves LLM responses based on query similarity. "
        "A practical implementation of the semantic caching optimization discussed in this section."
    ),
}


def add_annotations(filepath):
    """Add annotations to bib entries in a file."""
    with open(filepath, 'r', encoding='utf-8') as fh:
        content = fh.read()

    filename = os.path.basename(filepath)
    changes = 0

    for (fn, author_key), annotation in ANNOTATIONS.items():
        if fn != filename:
            continue

        # Find the bib entry containing this author key
        # Pattern: <p class="bib-ref">...author_key...</p>\n <span class="bib-meta">
        pattern = re.compile(
            r'(<p\s+class=[^>]*bib-ref[^>]*>.*?' + re.escape(author_key) + r'.*?</p>\s*\n)(\s*<span class="bib-meta">)',
            re.DOTALL
        )
        match = pattern.search(content)
        if match:
            # Check if annotation already exists
            before_span = content[match.end(1):match.start(2)]
            if 'bib-annotation' in before_span:
                continue

            # Insert annotation between </p> and <span class="bib-meta">
            indent = ' '
            annotation_html = f'{indent}<p class="bib-annotation">{annotation}</p>\n'
            replacement = match.group(1) + annotation_html + match.group(2)
            content = content[:match.start()] + replacement + content[match.end():]
            changes += 1
        else:
            print(f'  WARNING: Could not find entry for "{author_key}" in {filepath}')

    if changes > 0:
        with open(filepath, 'w', encoding='utf-8', newline='') as fh:
            fh.write(content)
        print(f'  Added {changes} annotations to {filepath}')
    return changes


def main():
    files = [
        "part-5-retrieval-conversation/module-21-conversational-ai/section-21.7.html",
        "part-6-agentic-ai/module-25-specialized-agents/section-25.7.html",
        "part-9-safety-strategy/module-32-safety-ethics-regulation/section-32.8.html",
        "part-9-safety-strategy/module-32-safety-ethics-regulation/section-32.9.html",
        "part-9-safety-strategy/module-32-safety-ethics-regulation/section-32.11.html",
        "part-9-safety-strategy/module-32-safety-ethics-regulation/section-32.12.html",
        "part-9-safety-strategy/module-33-strategy-product-roi/section-33.6.html",
        "part-9-safety-strategy/module-33-strategy-product-roi/section-33.7.html",
        "part-9-safety-strategy/module-33-strategy-product-roi/section-33.8.html",
    ]

    total = 0
    for f in files:
        total += add_annotations(f)

    print(f'\nTotal annotations added: {total}')


if __name__ == '__main__':
    main()
