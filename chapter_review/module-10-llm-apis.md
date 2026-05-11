# Module 10: Working with LLM APIs

**Audit date**: 2026-05-11
**Sections reviewed**: 10.1, 10.2, 10.3, 10.4
**Total word count**: ~16,500 prose words (HTML wc ~29,700)

## Summary
Module 10 is a strong, practitioner-focused tour of OpenAI / Anthropic / Gemini APIs, LiteLLM, caching, circuit breakers, and reasoning/multimodal endpoints. The voice is consistent and engaging (Pip the AI agent, "QWERTY of LLM APIs"), code is runnable, and pricing claims are bracketed by a sensible "as of early 2025" warning. The dominant problems are not content quality but mechanical cleanup: figure/code numbering is broken in many places, the chapter index has stale hrefs, and several auto-generated cross-reference fragments produce nonsense link text.

## Inconsistencies
- `index.html` line 123: section 10.5 list item points to `href="section-9.5.html"` (wrong file). The card is titled "10.5 Model Pruning and Sparsity" but section-10.5 does not exist in the directory; this stale entry should be removed since the chapter only ships 10.1-10.4.
- `section-10.1.html` line 35 (Prerequisites): "familiarity with the [Section 4.1] from [Section 04.1]" - duplicated/broken auto-cross-ref. Same garbled "Section X from Section 0X.Y" pattern recurs in 10.4 line 34.
- `section-10.1.html` line 40 caption is "Figure 10.1.2" but immediately followed at line 55 by another figure also labeled "Figure 10.1.2". Two figures share the same number (illustration vs. diagram).
- `section-10.1.html` line 66 figcaption says "Figure 10.1.5" but appears between 10.1.2 and 10.1.5 sections; the actual Figure 10.1.5 (request/response cycle, line 443) is then a third use of the number 10.1.5 (figcaption at line 114 also says 10.1.5 for streaming SSE conveyor).
- `section-10.1.html` line 346: "Code Fragment 10.1.5 shows this approach" but the actual code block is captioned "Code Fragment 10.1.9". Caption misnumbering.
- `section-10.1.html` line 286: orphan `<div class="code-caption"><strong>Code Fragment 10.1.7:</strong>` floats outside any `<pre>` block, immediately preceding the LiteLLM Library Shortcut callout.
- `section-10.1.html` line 382: comparison table title is "7. Provider Comparison Intermediate" - auto-generated label leak.
- `section-10.1.html` line 78 says "Code Fragment 10.1.2 demonstrates the approach" but the block immediately below is captioned "Code Fragment 10.1.1". Off-by-one in nearly every cross-reference between body prose and the block captions.
- `section-10.3.html` line 40 figcaption "Figure 10.3.5" used for the very first figure in the section, while a later figure (line 254 semantic caching) is also labeled "Figure 10.3.5".
- `section-10.3.html` line 47: "Code Fragment 10.3.2 shows the Anthropic Messages API" introduces a LiteLLM example - wrong description for the block that follows.
- `section-10.4.html` line 30: the `<strong>` tag wraps an entire 5-sentence Big Picture paragraph - styling regression.
- `section-10.4.html` line 51: "Code Fragment 10.4.2 shows..." but the actual block below is "Code Fragment 10.4.1". Same off-by-one.
- `section-10.4.html` line 151: "Code Fragment 10.4.6 shows" but block is captioned "Code Fragment 10.4.3".
- `section-10.4.html` lines 121-122: prose was tokenized into Pygments spans - "70<span class="si">% g</span>ross margins" - corrupted percent sign caused the highlighter to mark literal text as f-string formatting.

## Gaps
- 10.1's "Provider Comparison" table mentions Gemini Batch API as "No dedicated batch" but Gemini's Batch API has been GA since mid-2024. Outdated.
- 10.1.5 (Bedrock/Azure) gives a Bedrock Anthropic example only; Azure OpenAI is described in prose but no code sample is shown despite being a top-three enterprise wrapper.
- 10.3.4.2 promises a semantic-cache example but the displayed code only initializes the class - the demonstration of the actual hit/miss flow is truncated.
- 10.4 promises "multimodal APIs" in title but the visible content focuses overwhelmingly on reasoning models; the multimodal coverage (images, audio, video) is shallow given the section title.
- The chapter index lists "Section 10.5 Model Pruning and Sparsity" as a learning objective and TOC card, but no such section ships - 10.5 was apparently dropped without updating the index.
- "We will explore this routing pattern in detail in Section 10.3" appears multiple times in 10.1 but 10.3.1's LiteLLM coverage is brief; the deeper "model routing" promise is partially unfulfilled.

## Errors
- `section-10.1.html` Code Fragment 10.1.3 caption says "Set up the OpenAI client and send a chat completion request" but the code is the Batch API example - caption is the wrong stock string.
- `section-10.1.html` line 286 LiteLLM library-shortcut: the three calls have no `print` or assertion; output block is missing yet the prose implies the snippet is executable.
- `section-10.4.html` Code Fragment 10.4.3 references `response.usage_metadata.thinking_tokens` - the actual google-genai SDK exposes `thoughts_token_count`, not `thinking_tokens`. Will raise AttributeError.
- `section-10.4.html` 10.4.1.1: "Anthropic returns the full thinking trace (not just a summary)" - true for some tiers but Anthropic also supports redacted/summarized thinking; statement is overconfident.
- `section-10.1.html` Provider Comparison row "Prompt caching: OpenAI - Automatic" is correct as of 2024 update, but the prose at line 230 frames Anthropic caching as if OpenAI lacks it, then the table contradicts that prose. Reconcile.
- The 10.1 fintech Big-Picture story mentions "Anthropic's prompt caching could have cut costs by 90%" - this 90% figure applies to cache READ pricing vs full prefill; framing as "cut costs by 90%" without nuance can mislead.

## Improvements
- Run a single regen pass that re-numbers all `Figure N.M.P` and `Code Fragment N.M.P` captions sequentially per section and updates body cross-refs to match. The off-by-one and duplicate-number issues are mechanical and pervasive.
- Consolidate the three "Fun Note" callouts in 10.1 that all say variants of "OpenAI format is the de facto standard" (lines 51, 60, 561) into one.
- Add a small comparison diagram or table for the three reasoning model "thinking budget" parameters (`effort` vs `budget_tokens` vs `thinking_budget`) since the prose buries this contrast.
- Add a "diff with normal chat completions" callout in 10.4 explicitly listing what changes when you opt into reasoning (output items, billing for reasoning tokens, latency).
- The chapter has zero mention of Anthropic Batch API pricing despite a long OpenAI Batch discussion. A one-sentence note would balance.

## One-thing-only fix
Repair `index.html`: remove the stale "Section 10.5" card (or restore the missing file), then run the sequential renumber on figures and code fragments across all four sections. The numbering chaos is the single biggest reader-trust hit and almost every body cross-reference is currently wrong.
