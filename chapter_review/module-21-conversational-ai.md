# Module 21: Building Conversational AI Systems

**Audit date**: 2026-05-11
**Sections reviewed**: 21.1, 21.2, 21.3, 21.4, 21.5, 21.6
**Total word count**: ~51,500 (HTML markup included)

## Summary
A solid, modern chapter spanning dialogue architectures, persona/companionship, memory (with strong MemGPT/Letta and consolidation coverage), multi-turn flows, and voice. Two structural problems hurt the chapter: (1) the chapter index lists a Section 21.7 (HCI patterns + RealHumanEval) that does not exist on disk and whose link points incorrectly back to 21.1; (2) sections 21.5 and 21.6 substantially overlap on voice topics (OpenAI Realtime API, LiveKit, latency/turn-taking) without a clean split between "interfaces" and "agents".

## Inconsistencies
- **index.html lines 156-166**: Section 21.7 "Human-AI Interaction Patterns & Evaluation" is listed in the chapter index, but no `section-21.7.html` exists in the directory. The card link target is `section-21.1.html` (line 157), which is wrong: clicking 21.7 jumps to 21.1.
- **section-21.5 vs section-21.6 voice overlap**: 21.5 contains "21.5.6 Native Speech-to-Speech Models" + "21.5.6.5 Building with the Realtime API" + "21.5.7 Comparing Voice AI Orchestration Frameworks (Pipecat/LiveKit/Vapi)". 21.6 then re-covers OpenAI Realtime API (21.6.2), LiveKit Agents (21.6.3), latency optimization (21.6.4), turn-taking/interruption (21.6.5). 21.5 already has "21.5.4 Voice-Specific Orchestration Challenges - Interruption Handling". The two sections need a clean split or merger.
- **section-21.1 line 37**: Single illustration labeled "Figure 21.1.2" - skips 21.1.1 entirely, suggesting figure auto-numbering was applied but referenced figure 21.1.1 was deleted.
- **section-21.3 line 37**: Illustration labeled "Figure 21.3.2" while no Figure 21.3.1 exists; layered-memory SVG is also "21.3.2" (line 114). Two figures sharing 21.3.2.
- **Big-Picture callout placement**: Section 21.1's `<h3>Prerequisites</h3>` appears before the chapter intro paragraph; usual layout is Big Picture first, then prereqs. Inconsistent with module 19/20.
- **Echo agent description**: Index calls Echo "Philosophically Inclined AI Agent". Other sections may use different sub-titles - worth checking for consistency.
- **21.6 prereqs**: Section 21.6 builds on 21.5, but 21.6 prereq block does not explicitly require 21.5; readers may parachute into 21.6 without understanding the pipeline basics.

## Gaps
- **Missing section 21.7 file** entirely. Either author the section to match the index card (HCI methods, RealHumanEval, longitudinal trust calibration, over-reliance, anthropomorphism) or remove the index entry and renumber.
- **section-21.2 (personas, companionship)**: No discussion of regulated mental-health-companion concerns post-2024 (Character.AI lawsuit, FTC scrutiny). Topic is unavoidable for a 2026 textbook.
- **section-21.3 memory**: Letta is well covered; consider adding mem0 (popular memory framework as of 2025) and Zep memory in the platform comparison.
- **section-21.4 (multi-turn flows)**: No explicit treatment of state-machines + LLM hybrid (Rasa-style) for production task-oriented assistants; chapter leans on free-form LLM dialog. A short comparison would help readers selecting an architecture.
- **section-21.6 telephony**: PSTN integration discussed; would benefit from naming Twilio/Vonage/Telnyx and SIP trunking concretely.
- **No cross-reference between memory (21.3) and module 22-26 agent-memory** (which also touches persistent agent state). Forward pointer would help readers building agents.

## Errors
- **section-21.5 line 366**: Pipeline diagram describes STT + LLM + TTS with VAD/turn-taking; in 2026 the dominant architecture for production voice assistants has shifted to native speech-to-speech (covered later in 21.5.6) - the diagram's framing as the canonical pipeline is becoming outdated. Consider adding a "(legacy/cascaded)" qualifier.
- **section-21.5 STT provider table** (lines 47-100): Need to verify Deepgram/AssemblyAI pricing and Whisper version (large-v3 was current in 2024, large-v3-turbo released later) are still accurate as of 2026.
- **section-21.5 TTS provider table**: ElevenLabs, PlayHT, Cartesia all evolve rapidly; numerical claims (RTF, MOS) may be stale.
- **section-21.6 OpenAI Realtime API**: API surface (model names like `gpt-4o-realtime-preview`) changes; model name should be checked against current OpenAI docs and a "as of date" added.
- **Letta vs MemGPT naming** (21.3.5): MemGPT was renamed to Letta in 2024-2025. Chapter references both; ensure the body text uses "Letta (formerly MemGPT)" consistently rather than alternating.
- **section-21.6 line 47**: Single diagram caption "Figure 21.6.1" - no other figures in 21.6, which is unusually sparse for a 13K-word section. Add at least one architecture diagram per major sub-section.

## Improvements
- **Resolve the 21.5/21.6 overlap**: Reframe 21.5 as "voice pipelines + multimodal inputs" and 21.6 as "agentic voice systems (tool calls, telephony)". Move OpenAI Realtime API + LiveKit Agents framework discussion entirely to 21.6, leaving 21.5 with cascaded STT->LLM->TTS pipelines + Whisper/Deepgram/ElevenLabs vendor coverage.
- **Either author 21.7 or remove the index entry** (and update the chapter nav and TOC to match).
- **Standardize figure numbering** across all sections (same bug as modules 19, 20).
- **Add a "voice agent" architecture diagram** to 21.6 that contrasts pipeline-based (cascaded) and native-speech-to-speech approaches in agent-loop form.
- **Cross-link 21.3 memory to Module 26** (agent safety/production) where memory persistence and PII concerns matter.
- **Add a short "regulated personas" callout to 21.2** acknowledging consumer-protection issues.
- **Trim 21.3 length**: at 13.8K words with 10 sub-sections (21.3.1-21.3.10), it is the largest section in the chapter. Consider splitting "21.3.10 Evaluating Memory Quality" out into the evaluation chapter (29) and trimming overlap between 21.3.7 (Comparing Memory Approaches) and 21.3.8 (Memory-as-a-Service Platforms).
- **Add OpenAI gpt-4o-realtime / gpt-realtime** named-model section with current model identifiers and pricing.

## One-thing-only fix
Either add the missing `section-21.7.html` to match the index card or delete the dangling Section 21.7 entry from `module-21-conversational-ai/index.html` (currently broken: linking a "21.7" card to `section-21.1.html`). Right now the chapter index promises content the reader cannot reach.
