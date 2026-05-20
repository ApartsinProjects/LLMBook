# Self-Containment R2 Audit (Retry)

Agent: 21-self-containment-verifier (round 2, retry after API overload)
Date: 2026-05-19
Scope: 21 sections, sampled every ~19th file from sorted Parts 4 to 16 section list (376 files total)

## Method
For each section, I checked whether a reader landing from a Google search could understand the topic, motivation, and dependencies within roughly the first 1000 words. Where a Big Picture callout, prerequisites box, or self-contained opening paragraph already answered those questions, the section was marked standalone. Where the section opened with bare jargon, a backward reference to another section that was not summarized, or a "Platforms"-style one-word title plus a list, I added a brief inline gloss.

## Results

| # | Section | File path | Verdict |
|---|---------|-----------|---------|
| 1 | 47.1a Prompt Injection & Jailbreaking | part-10-llm-security-runtime-safety/module-47-adversarial-security-red-team/section-47.1.html | standalone (check) |
| 2 | 51.3 Datasets & Benchmarks | part-10-llm-security-runtime-safety/module-51-tools-of-the-trade/section-51.3.html | standalone (check) |
| 3 | 54.9 Audit Trails and Logging for Compliance | part-11-llm-ethics-trust-governance/module-54b-transparency-and-disclosure/section-54.9.html | standalone (check) |
| 4 | 59.4 Pipeline Parallelism and Hybrid Strategies | part-12-llm-systems-at-scale/module-59-distributed-training-systems/section-59.4.html | fix applied: expanded DP, TP, PP acronyms inline in Big Picture so first-time readers know what the three parallelism axes are |
| 5 | 67.1 Ideation: Finding LLM-Worthy Problems | part-14-designing-llm-agent-products/module-67-ideation/section-67.1.html | standalone (check) |
| 6 | 68.5 The Vertical-Slice Pattern in Depth | part-14-designing-llm-agent-products/module-68-vibe-coding/section-68.5.html | fix applied: replaced unhinted backward reference to 67.1 ("80/20 cuts") with a linked one-sentence gloss of what those cuts are; expanded vertical-slice definition with "touching every layer from input through model call to user-visible output" |
| 7 | 72.3 Bar Association and Regulatory Rules | part-14-applications-of-llms-across-industries/module-67-legal-llms/section-67.3.html | standalone (check) |
| 8 | 76.2 Offensive (Red Team) Use Cases | part-14-applications-of-llms-across-industries/module-71-cybersecurity-llms/section-71.2.html | standalone (check) |
| 9 | 79.1 Platforms | part-14-applications-of-llms-across-industries/module-74-tools-of-the-trade/section-74.1.html | fix applied: added opening paragraph defining what "vertical-AI platforms" means and what the catalog covers, since the section title is only "Platforms" |
| 10 | 83.2 Libraries & Frameworks | part-15-llm-agentic-ai-research-frontiers/module-78-tools-of-the-trade/section-78.2.html | standalone (check) |
| 11 | 17.2 Advanced PEFT Methods | part-4-training-adaptation/module-17-peft/section-17.2.html | standalone (check) |
| 12 | 19.14 Ray Train, Ray Serve, and Ray Data | part-4-training-adaptation/module-19-tools-of-the-trade/section-19.15.html | standalone (check) |
| 13 | 20.9 Video Editing and Remixing | part-5-multimodal-llms/module-20-audio-music-generation/section-20.9.html | standalone (check) |
| 14 | 24.1 VLA Architecture in One Equation | part-5-multimodal-llms/module-24-vla-models/section-24.1.html | standalone (check) |
| 15 | 26.2 Planning & Agentic Reasoning | part-6-agentic-ai/module-26-ai-agents/section-26.2.html | standalone (check) |
| 16 | 30.1 Platforms (Agent stack) | part-6-agentic-ai/module-30-tools-of-the-trade/section-30.1.html | standalone (check) |
| 17 | 33.1 Joint Embedding Spaces for Multimodal Retrieval | part-7-retrieval-information-extraction-with-llms/module-33-cross-modal-reasoning-rag/section-33.1.html | standalone (check) |
| 18 | 36.4 Models (Retrieval models) | part-7-retrieval-information-extraction-with-llms/module-36-retrieval-tools/section-36.4.html | fix applied: added a Big Picture callout defining the section topic, since the title is only "Models" and the file previously opened directly into a figure with no orientation for a Google-search arrival |
| 19 | 41.5 External Reading and Communities | part-8-conversational-ai-with-llms/module-41-conv-ai-tools/section-41.5.html | standalone (check) |
| 20 | 44.3 Observability, Monitoring, and Drift Detection | part-9-llm-evaluation-observability/module-44-online-eval-observability/section-44.3.html | standalone (check) |
| 21 | 46.5 Multi-Judge Ensembles and Production Patterns | part-9-llm-evaluation-observability/module-46-llm-as-judge-automated-evaluation/section-46.5.html | standalone (check) |

Additional spot fixes outside the sampled 21, picked up while neighbours were open in the same module:

| # | Section | File path | Verdict |
|---|---------|-----------|---------|
| 22 | 51.1 Platforms (safety stack) | part-10-llm-security-runtime-safety/module-51-tools-of-the-trade/section-51.1.html | fix applied: replaced the one-line opener with a paragraph that defines the three platform roles (moderation APIs, red-team platforms, compliance / governance services), since the section title is only "Platforms" |

## Summary

- 21 of 21 sampled sections: standalone after fixes (16 already standalone, 5 needed a short inline gloss).
- 1 additional opportunistic fix (51.1) for the same "Platforms" title problem.
- Pattern observed: the most common self-containment gap was tools-of-the-trade sections titled only "Platforms" or "Models" that dove straight into lists without telling a Google-search arrival what the catalog covers. The Big Picture and prerequisites pattern used elsewhere in the book is the right cure.
- No Blocking-severity gaps. No backward references were left unsummarized in the sample.

Overall verdict: MOSTLY SELF-CONTAINED across Parts 4 to 16. The remaining risk is concentrated in "tools-of-the-trade" subsections whose titles are single nouns ("Platforms", "Models", "Libraries & Frameworks"); a follow-on pass should sweep those specifically to confirm each has either a Big Picture callout or an opening orientation paragraph.
