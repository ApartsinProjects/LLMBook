# Module 31: Production Engineering & LLMOps

**Audit date**: 2026-05-11
**Sections reviewed**: 31.1, 31.2, 31.3, 31.4, 31.5, 31.6, 31.7, 31.8, 31.9
**Total word count**: ~58,000 words (raw HTML)

## Summary
A practical, current chapter on serving LLM apps in production: FastAPI + LitServe deployment, frontends, latency/scaling, LLMOps + A/B testing, AI gateway patterns, durable execution (Temporal/Inngest/LangGraph), edge deployment, resilience patterns, and Kubernetes-native operations. The technical content is up-to-date through 2026 (LiteLLM, Temporal, KServe, Volcano, MaxText). Two consistent defects undermine an otherwise strong chapter: (a) figure numbering follows the same "missing N.x.1, duplicated N.x.2/3" pattern seen in Chapter 29, and (b) almost every code block has both an in-`<pre>` `# Code Fragment X.Y.Z:` comment and a separate `<div class="code-caption">` caption — the two often disagree, and the captions sometimes literally repeat the comment text twice ("Code Fragment 31.8.1: Code Fragment 31.8.1: …").

## Inconsistencies
- **31.1** has *three* figures all labelled `Figure 31.1.3` (the chapter-opener illustration line 39, the restaurant-kitchen illustration line 57, and the three-layer architecture diagram line 139). No `Figure 31.1.1` or `Figure 31.1.2` exists in the section. The next figure is `Figure 31.1.4` (line 236) — so the entire numbering is shifted by 2.
- **31.2** has *four* figures labelled `Figure 31.2.3` (lines 38, 51, 158, 160). The first `Figure 31.2.1` and `Figure 31.2.2` are missing.
- **31.2**, line 47 in-prose says "the streaming concepts here build on the [Section 09.2], which determine how quickly tokens arrive at the frontend" — the cross-ref token has replaced what was probably "TTFT/TPOT discussion".
- **31.2**, line 47 also says "the tool use patterns from Section 22.2" but the link targets `section-22.6.html` — text says 22.2, link says 22.6.
- **31.3**, code captions are mixed: 31.3.2/31.3.4 are "Implementation of __post_init__, consume" / "Implementation of __init__, utilization, health_status" (auto-generated style), while 31.3.5 is the literal command "Install prometheus-client".
- **31.5** caption 31.5.1 reads `litellm_config.yaml - LiteLLM Proxy configuration` (file name as caption); 31.5.2 reads `Point the standard OpenAI client at the LiteLLM Proxy` (mid-sentence). Mixed caption styles.
- **31.6**, lines 85, 261, 331 have stray leading spaces in the H2 markup (`  <h2>`) — not visible to readers but indicates inconsistent template formatting.
- **31.8** code captions duplicate the in-`<pre>` comments verbatim:
  - Caption: "Code Fragment 31.8.1: Code Fragment 31.8.1: Classifying LLM failures into hard and soft categories" (line 136).
  - Caption: "Code Fragment 31.8.2: Code Fragment 31.8.2: Retry with exponential backoff for LLM APIs" (line 209).
  - Caption: "Code Fragment 31.8.4: Code Fragment 31.8.3: Fallback chain with primary, secondary, and cached responses" (line 292) — the 31.8.4 caption claims to describe 31.8.3, plus has the duplicated prefix.
- **31.9** has the same duplication pattern, *plus* the in-`<pre>` comments for every code block in the section claim to be "Code Fragment 31.9.5" while the surrounding captions number them 31.9.1, 31.9.2, 31.9.3:
  - Caption 31.9.1 says "Code Fragment 31.9.5: Kueue ClusterQueue …" (line 108).
  - Two later code blocks both have `# Code Fragment 31.9.5: Volcano Job …` and `# Code Fragment 31.9.5: PyTorchJob CRD …` headers (different content, same fragment number).
  - One caption is `Code Fragment 31.9.4` → not present, jumps from 31.9.3 to 31.9.4 to 31.9.6.
- **31.9** caption 31.9.4 is unique and reads `Code Fragment 31.9.4: Multi-tenant inference with KServe ModelMesh` (paraphrased from search) — actual content shows what should likely be `31.14.2a` style suffixed numbering inherited from a previous chapter rename. Confusing.
- **31.4**, line 186 says "Figure 31.4.1 illustrates the end-to-end A/B testing pipeline" but Figure 31.4.1 was actually defined as "The LLMOps lifecycle" (line 134). The A/B-testing figure is 31.4.2 (line 221).

## Gaps
- **31.1** Big Picture mentions "build on the serving frameworks from Section 09.4" but never names a specific subsection of Chapter 9 that justifies the cross-reference.
- **31.5** (AI Gateway): no mention of OpenRouter, which is one of the most-used hosted alternatives in 2025-2026; LiteLLM is covered in depth but the broader landscape is left out.
- **31.6** (Durable Execution): no comparison to Cloudflare Durable Objects or Vercel Workflows, which compete in this space; the chapter only covers the three Python-centric options.
- **31.7** (Edge): only covers llama.cpp, Ollama, MLX. No coverage of mistral.rs, MLC LLM, or Apple's MLX-Distributed (mid-2025). The Apple Silicon section (31.7.4) reads as if MLX is the only path on macOS.
- **31.8** (Resilience): no discussion of *prompt-level* failure modes (model returning wrong format, partial JSON) that are arguably the most common LLM-specific failures in production. Focus is on infra failures (timeouts, rate limits) which are well-trodden.
- **31.9** (Kubernetes): Kubeflow Training Operator is covered but KubeRay (which is closer to LLM-fine-tuning ergonomics in 2026) is absent.
- No section on *cost* observability beyond what 29.10 covers — a glaring gap for a "production engineering" chapter.

## Errors
- **31.1**, the FastAPI streaming code (line 169) defines `stream_response` at module-top with `async def stream_response(req: ChatRequest)` but does not wrap the SSE chunks in a try/except that handles disconnected clients — production code will leak generators on cancellation. Not a bug per se, but the prose immediately after says "production-ready" pattern.
- **31.1**, code output panel (line 179-185) shows a paragraph explaining transformer attention — that output has nothing to do with the FastAPI snippet above it. Output mismatch (same class of bug as Chapter 27).
- **31.4**, Figure 31.4.1 caption is "The LLMOps lifecycle ..." but the inline reference at line 186 calls it "the end-to-end A/B testing pipeline" — caption-vs-reference disagreement.
- **31.5**, code fragment 31.5.5 is described as "Token-aware rate limiter" (line 319) but immediately above (line 317) caption 31.5.4 is described as "A token-aware rate limiter". Two different captions for what looks like substantially similar content (probably a duplicate/forked block).
- **31.8** and **31.9** in-`<pre>` headers number themselves wrongly (see Inconsistencies above) — code that a reader might copy-paste with the comment header will have a misleading "fragment number" comment.
- **31.9**, the Volcano Job example uses `RestartJob` on eviction "ensures the entire job restarts rather than running with missing workers" (line 172) — the actual Volcano `RestartJob` policy restarts the job *task*, not the job; the prose conflates the two.
- **31.7**, line 339 caption "Ollama exposes an OpenAI-compatible API on localhost:11434" — true but the code immediately after calls `chat.completions.create` against `base_url="http://localhost:11434/v1"` (correct); no error here, just calling out that the caption is good in this case unlike most others in the chapter.

## Improvements
- **Renumber figures in 31.1, 31.2, 31.3** to fix the missing-first-figure / duplicated-second pattern. Same issue as Chapter 29.
- Strip duplicated `Code Fragment X.Y.Z:` prefixes from captions in 31.8 and 31.9. Easiest path: a single Python script that scans for `code-caption.*Code Fragment .*Code Fragment` and dedupes.
- Re-pair `<div class="code-output">` payloads with the correct code blocks (at least one mismatch in 31.1).
- Add a note in 31.5 directing readers to OpenRouter and equivalent alternatives.
- Add prompt-level resilience patterns (JSON-schema retries, repair prompts, format-fallback) to 31.8.
- Add KubeRay coverage to 31.9 (or at minimum a sidebar mentioning it).
- Add an inline cost-observability subsection to 31.5 (token quotas, per-tenant cost attribution) — most of the building blocks are in 29.10 but 31.5 should mention them.
- Fix the "Section 22.2" / link-to-22.6 mismatch in 31.2.
- Convert in-`<pre>` `# Code Fragment X.Y.Z` comments to a single source of truth (drop the inline comment, keep only the caption div).

## One-thing-only fix
Renumber the figures in section 31.1 (the chapter-opener `Figure 31.1.3` should be `31.1.1`, the restaurant-kitchen illustration should be `31.1.2`, the three-layer architecture diagram should be `31.1.3`), and apply the same fix to 31.2's four duplicated `Figure 31.2.3` occurrences. This single change kills the "where did Figure 31.1.1 go?" reader friction that begins the chapter and propagates suspicion into every subsequent figure reference. The chapter's content is otherwise the strongest in this batch.
