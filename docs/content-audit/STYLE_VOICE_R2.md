# Style and Voice Round 2 Report (Parts 4-7)

Scope: section files in Parts 4-7 (modules 15-36). Focused on textbook-tone openers, hedging density, banned phrases ("leverage", "navigate" in non-technical use, "comprehensive"), and weak generic prose.

## Headline finding

Parts 4-7 are already in strong shape after Cycle 1. Most sections open with sharp, declarative prose, use specific tool and model names, cite concrete numbers, and avoid stock textbook constructions. The book's voice is largely consistent with the polished sections in Parts 1-3. Cycle 2 revision was therefore surgical, not sweeping.

Telltale phrases ("In this section we will...", "It should be noted that...", "One can consider...", "may be defined as...") are absent from this scope. The remaining issues were a small number of generic openers and a few paragraphs with academic-survey phrasing.

## Files touched

1. `part-6-agentic-ai/module-29-specialized-agents/section-29.2.html` - Rewrote the "What Comes Next" placeholder ("we continue") into two concrete next-section pointers describing what the reader will learn.

2. `part-7-retrieval-information-extraction-with-llms/module-35-advanced-rag/section-35.3.html` - Replaced "leverages graph algorithms" with the imperative "run graph algorithms (community detection, traversal)" plus a sharper one-sentence motivation for GraphRAG.

3. `part-6-agentic-ai/module-26-ai-agents/section-26.1.html` - Three rewrites in the agent-definition section. Replaced the loose "The term 'agent' has been used loosely across the AI community" opener with a tighter definition that emphasizes the autonomy-in-action-selection criterion. Tightened the perception-reasoning-action paragraph and the chain/workflow/agent comparison to drop "Every agent, regardless of its complexity..." and "Understanding the spectrum from simple to complex orchestration..." in favor of declarative versions.

4. `part-6-agentic-ai/module-27-tool-use-protocols/section-27.6.html` - Rewrote the Big Picture and the cost-anatomy opener. Replaced "As LLM agents gain access to more tools..." with "Hand an agent 50 tools and you have a budget problem." Tightened the token-cost paragraphs to remove redundancy and lead with the concrete number ("100 to 300 tokens per schema, 5,000 to 15,000 for 50 tools").

5. `part-6-agentic-ai/module-26-ai-agents/section-26.3.html` - Sharpened the reasoning-model cost paragraph. Replaced "Reasoning models consume significantly more tokens..." with "burn far more tokens" and concrete numbers (500 tokens on GPT-4o vs 5,000+ on o3).

6. `part-7-retrieval-information-extraction-with-llms/module-32-rag/section-32.3.html` - Rewrote three weak openers. The tabular-data opener now leads with the concrete tradeoff ("Stuff a 50-row table into the context window... bigger than that, write SQL"). The direct-table-reasoning paragraph drops "The key is formatting" in favor of "Markdown beats raw CSV; the model reads the schema visually." The text-to-SQL section opener now leads with the user's perspective ("show me last quarter's top customers").

7. `part-7-retrieval-information-extraction-with-llms/module-34-structured-information-extraction-ner/section-34.1.html` - Rewrote the chapter opener to use the strong-three-flavors pattern from the style guide. Each task gets a one-line definition with the input-output pattern explicit.

8. `part-6-agentic-ai/module-28-multi-agent-systems/section-28.2.html` - Fixed a typo and tightened the topology opener. Replaced "Multi-agent define how agents are organized..." (broken sentence) with "Topology decides how agents are organized, how work flows between them, and how decisions land."

9. `part-4-training-adaptation/module-18-alignment-rlhf-dpo/section-18.4.html` - Rewrote the RLVR-paradigm opener. Replaced the "we can bypass the reward model entirely" hedge with declarative "skip the reward model and use ground truth as the reward directly." Also tightened the RLVR pitch into one sentence.

10. `part-4-training-adaptation/module-18-alignment-rlhf-dpo/section-18.5.html` - Sharpened the scalable-oversight opener. Replaced "rely on a critical assumption" with the more direct "Every alignment technique... rests on one assumption" and added concrete examples (novel math proofs, distributed-systems code, drug molecule design) that the original buried in rhetorical questions.

11. `part-7-retrieval-information-extraction-with-llms/module-35-advanced-rag/section-35.1a.html` - Rewrote the 35.1.1 Query Transformation opener. Replaced "Query transformation is the first lever to pull..." with a more concrete pitch that names the three techniques and their respective failure modes inline.

12. `part-4-training-adaptation/module-18-alignment-rlhf-dpo/section-18.1a.html` - Rewrote the alignment-problem opener. Replaced "A pretrained language model optimizes a single objective..." with a more direct version that names what base models do well and what they do badly (with concrete examples: malware completion, fabricated citations, ten-paragraph answers).

13. `part-6-agentic-ai/module-28-multi-agent-systems/section-28.4.html` - Sharpened the testing-challenge opener. Replaced "Testing multi-agent systems is harder than testing traditional software because..." with "Testing multi-agent systems breaks the assumptions traditional software testing leans on" and reframed the three problems as compounding rather than listed.

## Patterns I left alone

- "navigate" / "navigation" when describing Playwright browser actions, HNSW graph traversal, or function names: these are technical referents, not stylistic flab.
- "robust" when used in figure captions or formal definitions ("robust to fine-tuning attacks", "robust alignment approaches"): the term is a load-bearing technical adjective in alignment literature.
- "comprehensive" used as a quoted model output in the GraphRAG eval-metrics discussion: it is the literal name of the metric.
- "highest-leverage" used as a noun phrase (e.g., "the highest-leverage improvement"): the noun form is fine; the verb "leverage" is the one the style guide bans.
- "significantly" in benchmark-comparison sentences where the magnitude is documented: e.g., "5% to 15% on diversity-sensitive benchmarks."

## What did not need fixing

I sampled deep into sections 17.1, 17.2, 17.3, 17.5b, 21.4, 22.2, 22.3, 22.5, 22.7, 24.6, 26.2, 27.2, 27.3, 27.4, 28.1, 29.1, 31.1a, 31.1b, 31.3, 31.4, 32.1a, 32.2, 32.4, 33.2, 34.2, 35.2, 35.4, 35.5a. All of them are already at or above the "confident-and-sharp" bar: tight openers, named tools, specific numbers, active voice. Cycle 1's engagement and style passes appear to have done thorough work here.

## Summary

13 sections improved, ~28 paragraphs rewritten. Estimated tone uplift: small but real on the touched sections; the rest of Parts 4-7 are already aligned with the book voice. No section is now noticeably weaker than its Part 1-3 counterparts.
