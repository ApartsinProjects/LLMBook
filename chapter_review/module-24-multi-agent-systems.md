# Module 24: Multi-Agent Systems

**Audit date**: 2026-05-11
**Sections reviewed**: 24.1, 24.2, 24.3 (only three section files exist on disk)
**Total word count**: ~9,900 (HTML markup included)

## Summary
Compact chapter covering frameworks, architecture patterns, and human-in-the-loop. Like module 22, the chapter has an unfinished restructure: the index promises 5 sections (24.1-24.5) but only 3 files exist, and section-24.3 still uses old "24.5.x" internal heading numbers. Content depth is also thin for the size of the topic - sections 24.2 and 24.3 are very short (~3,400 and ~3,100 words including markup).

## Inconsistencies
- **Index has 5 cards but only 3 section files exist on disk**:
  - Cards 24.1 (Framework Landscape), 24.2 (Architecture Patterns), 24.3 (Communication/Consensus), 24.4 (State Management/Workflows/Orchestration), 24.5 (Human-in-the-Loop)
  - Files: section-24.1.html, section-24.2.html, section-24.3.html
- **Cards 24.2, 24.3, 24.4 all link to section-24.2.html** (lines 86, 93, 100). Three different topics resolve to the same file.
- **Card 24.5 links to section-24.3.html**, which is correct content (Human-in-the-Loop) but wrong number (file is named 24.3 by file but card is "24.5").
- **section-24.3.html internal H2s** use `24.5.1`, `24.5.2`, `24.5.3` (lines 40, 51, 110) - matches the *card* number 24.5 but not the *file* number 24.3.
- **Missing content**: Sections 24.3 (Communication/Consensus/Conflict) and 24.4 (State Management/Temporal/Checkpointing) advertised in the index do not have section files. These topics are completely missing from the chapter.
- **section-24.1 line 88**: Code-fragment caption cross-refs `module-25-specialized-agents/section-25.2.html` (research agent). Verify that link still maps to research agents in module 25.
- **section-24.1 line 141**: Code Fragment 24.1.3 caption "CrewAI: Research Agent" is a placeholder/short label, not the substantive caption used in 24.1.1 and 24.1.2.
- **Code Fragment 24.2.2 caption** (line 120) has `<div class="callout library-shortcut">` immediately concatenated at the end of the closing `</div>` - looks like a malformed merge.
- **section-24.1 line 39** illustration caption mentions "robot orchestra" - sole figure in section.
- **Census agent description** ("Crowd-Sourced AI Agent") - reasonable, no inconsistency in this chapter.

## Gaps
- **Communication/Consensus/Conflict Resolution section** (advertised as 24.3) does not exist. This omits the critical material on debate protocols, sycophantic convergence, and conflict resolution - which the chapter overview specifically promises.
- **State Management/Workflows/Orchestration section** (advertised as 24.4) does not exist. This omits the LangGraph state machine deep dive, Temporal coverage, checkpointing, and parallel execution - all promised by the chapter overview.
- **No coverage of debate patterns** (e.g., Du et al. 2023 multi-agent debate, society of mind), even though the chapter overview promises "debate topologies".
- **No coverage of swarm/hierarchical patterns** (mentioned in objectives) - section-24.2 only covers supervisor, pipeline, mesh.
- **No CrewAI Crews/Flows distinction** despite CrewAI being a featured framework.
- **No comparative cost/latency table** for the frameworks (LangGraph vs CrewAI vs OpenAI Agents SDK).
- **section-24.1 lab** ("Build the Same Agent in Three Frameworks") is set up but the steps appear thin (only "Step 1: Setup and data preparation" listed in the H3 sequence, no Step 2/3).

## Errors
- **section-24.1 line 45**: Heading "24.1.1 The Framework Landscape in 2026" - if the chapter is the 5th edition published in 2026, the "in 2026" is appropriate; verify it is consistent with publish year.
- **section-24.3 (HITL) heading numbers 24.5.x**: H2s should be 24.3.x (matching the file) or the file should be renamed to section-24.5.html (matching the card). Current state is internally inconsistent.
- **CrewAI/AutoGen/AG2 versioning**: AutoGen forked into AG2 in 2024-2025; verify the framework names match the latest project naming.
- **OpenAI Agents SDK reference**: Released in 2025; verify the API surface used in code samples (Runner.run, etc.) matches current SDK.
- **section-24.1 Code Fragment 24.1.3**: Caption is just "CrewAI: Research Agent" without prose explanation - inconsistent caption style with the rest of the file.

## Improvements
- **Author the missing sections 24.3 (Communication & Consensus) and 24.4 (State Management & Orchestration)** as advertised by the index. This is the most important content gap.
- **Either rename section-24.3.html → section-24.5.html and update internal headings, or renumber the card to "24.3"**. Pick one consistent target.
- **Expand 24.2 (Architecture Patterns)** with diagrams for swarm, hierarchical, and debate patterns to match the chapter objectives.
- **Add a framework comparison table to 24.1** (rows: LangGraph, CrewAI, AutoGen, OpenAI Agents SDK, Google ADK, smolagents, PydanticAI, Semantic Kernel; columns: orchestration model, state, observability, parallel calls, license, maturity, as-of date).
- **Add a debate-pattern code example** (multi-agent debate à la Du et al. 2023) to either 24.2 or the missing 24.3 once it exists.
- **Standardize all CrewAI/AutoGen-AG2/OpenAI-Agents-SDK code snippets with version pinning** since these libraries change weekly.
- **Cross-link 24.3 (HITL) to module 26 (agent safety)** explicitly - approval gates and graduated autonomy are core to safety.
- **Replace one-line code captions ("CrewAI: Research Agent") with substantive descriptions** explaining the abstraction being demonstrated.

## One-thing-only fix
Author the missing content for the two sections that are listed in the chapter index but have no source files: 24.3 (Communication, Consensus & Conflict Resolution) and 24.4 (State Management, Workflows & Orchestration). These cover the most important multi-agent material - debate protocols, sycophantic convergence, LangGraph state machines, and Temporal - which the chapter overview promises but currently does not deliver.
