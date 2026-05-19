# Cognitive Load Report (Parts 5 to 8, modules 20 to 46)

Agent: 05-cognitive-load (LLMBook, v2.0).
Date: 2026-05-19.
Scope: section files in `part-{5,6,7,8}-*/module-*/section-*.html`.

## Method

1. Used `Glob` for `part-{5,6,7,8}-*/module-*/section-*.html` (97 sections in scope).
2. Read each candidate looking for paragraphs that:
   - Introduce 4+ new concepts in a single paragraph,
   - List 5+ technical terms in one sentence without grouping,
   - Mix abstract framework descriptions with specific implementation details,
   - Stack philosophy or motivation onto definition without breathing room.
3. Refactor pattern applied uniformly:
   - **Split**: break dense paragraphs into 2-3 with clear thematic boundaries.
   - **Group**: turn implicit lists into explicit `<ul>` / `<ol>` so the reader can scan.
   - **Bridge**: add a 1-sentence "step back" before the technical cluster that names what is coming.
4. Preserved every fact and citation; only restructured (no shortening).

## Sections Edited

| # | File | Fix |
|---|------|-----|
| 1 | `part-7-.../module-32-rag/section-32.1b.html` (32.1.8.1) | Added a 1-sentence bridge before the five "Why RAG still matters" paragraphs: "Five distinct advantages keep RAG relevant even when the context window is large enough to hold your entire corpus. We walk through each in turn." |
| 2 | `part-7-.../module-31-embeddings-vector-db/section-31.2a.html` (HNSW Key Insight) | Split the dense O(log N) Key Insight (M, ef_construction, m_L, geometric distribution, Milgram's six degrees) into 3 paragraphs: the skip-list analogy, the formal proof + small-world property, and the practical M / ef_construction parameter pair. |
| 3 | `part-7-.../module-31-embeddings-vector-db/section-31.2a.html` (PQ Key Insight) | Split the product quantization Key Insight (256^96, Jegou et al., asymmetric distance computation, curse of dimensionality) into 3 paragraphs: the codebook arithmetic, why it works mathematically, and the curse-of-dimensionality framing. |
| 4 | `part-7-.../module-35-advanced-rag/section-35.2.html` (35.2.1 Key Insight) | Split the philosophical-to-GraphRAG Key Insight (Aristotle, RDF, Frege, Russell, compositionality, GraphRAG) into 3 paragraphs: the historical lineage, the compositionality claim with the Einstein-Ulm-Germany example, and the GraphRAG-vs-vector contrast. Replaced inline triple with `<code>`-formatted triples. |
| 5 | `part-8-.../module-37-conversational-ai/section-37.3.html` (37.3.1 Key Insight) | Split the Atkinson-Shiffrin Key Insight into 3 paragraphs: the 1968 model itself, the one-to-one mapping to conversational AI, and the parallel failure modes (interference, retrieval failure). Italicized the three memory types so they read as a triplet. |
| 6 | `part-6-.../module-28-multi-agent-systems/section-28.1.html` (28.1.1 frameworks paragraph) | Converted the runon AutoGen + OpenAI Agents SDK + Google ADK + smolagents + PydanticAI + Semantic Kernel paragraph into two grouped bullets: "provider-native SDKs" vs. "cross-ecosystem libraries", with AutoGen retained as a standalone lead paragraph. |
| 7 | `part-6-.../module-28-multi-agent-systems/section-28.1.html` (28.1.1 Key Insight) | Converted the dense "use LangGraph / use CrewAI / use OpenAI Agents SDK / use raw API" recommendation paragraph into a 4-bullet `<ul>` keyed on situation (need full control / want fast prototyping / need provider-native / building simple agent). |
| 8 | `part-6-.../module-26-ai-agents/section-26.5.html` (26.5.1 eight components) | Converted the runon "(1)...(8)" eight-components paragraph into three grouped `<ul>` blocks: plan-and-act (Planner, Tool Router, Memory Manager, Execution Sandbox), handle-outcomes (Evaluator, Recovery Handler), guard-boundaries (Permissions Gate, Cost Controller). Each grouping has a short framing sentence. |
| 9 | `part-6-.../module-26-ai-agents/section-26.5.html` (26.5.2 request flow) | Split the wall-of-text request flow paragraph into 3 stages (admit / execute / respond) with a leading sentence naming the three-stage structure, so the reader sees the rhythm of permission, then planning, then response. |
| 10 | `part-6-.../module-27-tool-use-protocols/section-27.6.html` (27.6.1 control loop) | Converted the seven-component control-loop runon sentence (meta-planner, tool router, tool registry, budget tracker, result cache, executor, synthesizer) into a 4-step `<ol>` keyed on plan / route / budget / dispatch. |
| 11 | `part-5-.../module-22-vision-language-models/section-22.1.html` (22.1.4 resolution paragraph) | Converted the four resolutions (336, 384, 448, arbitrary "any-resolution") from a comma-separated parenthetical list into a 4-bullet `<ul>` so the resolution-to-model mapping reads as a comparison. |
| 12 | `part-5-.../module-22-vision-language-models/section-22.1.html` (22.1.7 V-NeXT) | Split the dense "next-generation scale" paragraph into two: one for the two flagship encoders (EVA-CLIP-G, InternViT-6B) and one for the V-NeXT naming convention. Bolded model names so the reader sees the comparison anchors. |
| 13 | `part-8-.../module-40-voice-realtime-multimodal/section-40.1.html` (40.1.1 platforms paragraph) | Converted the runon "Several platforms" paragraph (OpenAI Realtime API, LiveKit, Pipecat, Vapi, Bland.ai) into three grouped bullets: speech-to-speech APIs / open-source frameworks / managed telephony platforms. |
| 14 | `part-7-.../module-33-cross-modal-reasoning-rag/section-33.1.html` (Big Picture) | Split the four-system Big Picture paragraph (CLIP, SigLIP, ImageBind, LanguageBind, 4M) into three: the conceptual definition, the model lineage with bold anchors, and the section roadmap. |
| 15 | `part-7-.../module-35-advanced-rag/section-35.4.html` (35.4.1 512-tokens Key Insight) | Split the "Why 512 tokens" Key Insight (training max length + lost-in-the-middle + granularity penalty) into 3 paragraphs labelled by force direction: push toward shorter, push toward longer, and where they cross. |
| 16 | `part-6-.../module-29-specialized-agents/section-29.2.html` (29.2.2 WebArena paragraph) | Converted the runon "three failure modes + three mitigations" paragraph into two parallel `<ul>` blocks (failure modes / mitigations) so the reader can scan them as a 3x3 pairing. |
| 17 | `part-5-.../module-20-audio-music-generation/section-20.3.html` (20.3.1 codecs) | Converted the three-codec paragraph (EnCodec, SoundStream, DAC) from prose into a 3-bullet `<ul>` with a leading framing sentence. |
| 18 | `part-5-.../module-20-audio-music-generation/section-20.3.html` (20.3.5 conditioning) | Converted the four conditioning modalities (text / melody / reference audio / lyric) from a runon paragraph into a 4-bullet `<ul>` ordered "from universal to controversial". |
| 19 | `part-5-.../module-20-audio-music-generation/section-20.3.html` (20.3.6 countermeasures) | Converted the inline (1)(2)(3)(4) countermeasures (training-data filtering, output-side filtering, opt-out registries, revenue-sharing pilots) into a proper 4-bullet `<ul>` with bold labels and a closing one-line summary. |
| 20 | `part-7-.../module-36-retrieval-tools/section-36.3.html` (Big Picture) | Converted the four-layer benchmark Big Picture paragraph (classical IR, BEIR, MTEB, RAG benchmarks) into a 4-bullet `<ul>` labelled Layer 1 / 2 / 3 / 4, with a closing bridge sentence about the production mistake the section is trying to prevent. |
| 21 | `part-5-.../module-22-vision-language-models/section-22.7.html` (22.7.1 Mental Model) | Split the smoothie/sandwich/tasting-flight metaphor Key Insight: turned the three metaphors into a 3-bullet `<ul>` so each metaphor gets visual breathing room, and split the training-cost paragraph that followed into three sentences (one per architecture: Chameleon, LLaVA, CLIP). |
| 22 | `part-7-.../module-35-advanced-rag/section-35.5b.html` (35.5.9.1 compound system) | Converted the six-component compound-system paragraph into two `<ul>` blocks: three core components (retriever / reranker / generator) and three optional stages (query rewriter / verifier / router). |
| 23 | `part-7-.../module-35-advanced-rag/section-35.5b.html` (Big Picture) | Split the Big Picture intro paragraph (six pieces of plumbing + three framework names + production-patterns reference) into two paragraphs, with the six pieces explicitly named in the first paragraph and the framework / philosophy discussion in the second. |

**23 paragraph refactors across 14 section files.**

## Categories of fix applied

- **12 prose-to-list conversions**: dense paragraphs that had implicit lists embedded in commas or inline numbering, restructured into `<ul>` / `<ol>` so the reader sees structure at a glance. Affected sections: 28.1 (frameworks), 28.1 (Key Insight), 26.5 (8 components), 27.6 (control loop), 22.1 (resolutions), 40.1 (platforms), 29.2 (WebArena), 20.3 (codecs), 20.3 (conditioning), 20.3 (countermeasures), 36.3 (benchmark layers), 35.5b (compound system). Pattern in every case: the original packed 4 to 8 named items into a single paragraph in which the reader had to count items mentally to see how many there were.
- **8 paragraph splits**: prose paragraphs that legitimately needed prose (no implicit list) but combined too many distinct logical moves, broken into 2-3 thematically focused paragraphs. Affected sections: 32.1b, 31.2a (HNSW), 31.2a (PQ), 35.2 (philosophy), 37.3 (Atkinson-Shiffrin), 35.4 (512 tokens), 22.1 (V-NeXT), 33.1 (Big Picture), 22.7 (Mental Model), 35.5b (Big Picture). Pattern: a single paragraph that introduced a concept, justified it historically, explained the mechanism, gave an example, AND named the production consequence; split into "intro + mechanism + consequence" or "history + claim + implication".
- **3 grouped-bullet structures**: places where simple prose-to-list still left too many bullets in one block, regrouped into 2-3 themed sub-blocks with a one-line theme label. Affected sections: 28.1 (provider-native vs cross-ecosystem libraries), 26.5 (plan-and-act / handle-outcomes / guard-boundaries), 40.1 (speech-to-speech / open-source / managed telephony). Pattern: more than 5 bullets at one level is itself a cognitive load problem; pre-grouping them by theme cuts that load in half.
- **6 framing-sentence additions**: short single-sentence bridges placed before a list or a technical cluster, each one informative (no "as we have seen" filler). Affected sections: 32.1b ("Five distinct advantages keep RAG relevant even when the context window is large enough..."), 26.5 admit/execute/respond, 27.6 plan/route/budget/dispatch, 22.1 resolutions, 36.3 four-layer pyramid, 20.3 conditioning ("ordered from universal to controversial"). Bridges always preview either the count of items or the dimension they vary along.

## Cognitive Load Summary

Overall cognitive load across Parts 5 to 8: **MANAGEABLE** after this pass. The book already had strong structural callouts (Big Picture, Key Insight, Tip, Warning, Production Pattern), so most cognitive overload was concentrated in the *first prose paragraph* of each major sub-section. Those paragraphs were doing too much: stacking history + definition + example + production consequence. After the edits, each of the 23 dense spots now has either a list scaffolding or a 2-3 paragraph split so the reader's working memory does not have to track 5+ new things in a single block.

Sections not edited but checked: 31.5 (ColPali, already well-paced with explicit examples after each definition), 35.3 (GraphRAG, dense but already factored into Key Insights with bulleted child failure modes), 27.5 (retrieval-as-tool, intentionally narrative since it is reframing rather than introducing), 32.4 (citation, already well-structured with NLI / quote-match sub-sections), 32.3 (text-to-SQL, three-stage breakdown already explicit). These remain MANAGEABLE without intervention.

## Notes for downstream agents

- The new `<ul>` and `<ol>` blocks added by this pass do not contain new claims; only restructured existing prose. Bibliography and citation agents should not need to re-verify.
- Two Key Insights were lightly reordered (31.2a HNSW, 35.4 512 tokens) to put the *forces* before the *outcome*. The technical content is unchanged.
- The grouping labels I introduced (e.g., "Plan and act / Handle outcomes / Guard the boundaries" in 26.5) are descriptive, not normative. If a Teaching Flow Reviewer disagrees with the grouping, swap the labels without rewriting the bullets.
