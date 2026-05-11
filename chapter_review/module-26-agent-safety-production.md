# Module 26: Agent Safety, Production & Operations

**Audit date**: 2026-05-11
**Sections reviewed**: 26.1, 26.2, 26.3, 26.4, 26.5, 26.6, 26.7, 26.8, 26.9, 26.10
**Total word count**: ~45,200 (HTML markup included)

## Summary
The largest chapter in Part VI, with comprehensive coverage of safety, sandboxing, observability, error recovery, testing, security benchmarks, supply-chain, plus three sections absorbed from Module 35 (reliability, observability/testing/CI/CD, self-improving agents). The chapter has three major issues: (1) the index lists only 7 of the 10 section files, (2) the three absorbed sections (26.8, 26.9, 26.10) still carry their original "35.X.Y" internal heading numbers, and (3) significant content overlap between the absorbed sections and the original 26.3/26.4/26.5 sections (observability, resilience, testing each appear twice).

## Inconsistencies
- **Index lists 7 cards (26.1-26.7); 10 section files exist**:
  - Cards: 26.1 Safety/Prompt Injection, 26.2 Sandboxing, 26.3 Observability/Cost, 26.4 Error Recovery/Resilience, 26.5 Testing Multi-Agent, 26.6 Security Benchmarks, 26.7 Supply-Chain
  - Files NOT linked from index: section-26.8.html (Reliability Engineering Under Production Stress), section-26.9.html (Observability, Testing, and CI/CD), section-26.10.html (Self-Improving and Adaptive Agents)
- **Absorbed sections still use old module-35 heading numbers**:
  - section-26.8.html H2s: `35.5.1`, `35.5.2`, `35.5.3`, `35.5.4`, `35.5.5` (lines 40, 67, 162, 226, 288)
  - section-26.9.html H2s: `35.6.1`, `35.6.2`, `35.6.3`, `35.6.4`, `35.6.5` (lines 36, 129, 223, 234, 250)
  - section-26.10.html H2s: `35.8.1`, `35.8.2`, `35.8.3`, `35.8.4`, `35.8.5` (lines 40, 124, 141, 195, 211)
- **Content duplication between original and absorbed sections**:
  - 26.3 "Production Observability & Cost Control" vs 26.9 "Observability, Testing, and CI/CD for Agent Workflows" - both cover tracing, OpenTelemetry, agent observability.
  - 26.4 "Error Recovery, Resilience & Graceful Degradation" vs 26.8 "Reliability Engineering Under Production Stress" - both cover circuit breakers, retry budgets, graceful degradation, failure modes.
  - 26.5 "Testing Multi-Agent Systems" vs 26.9 "Observability, Testing, and CI/CD" - both cover regression testing and CI/CD for agents; 26.9 also has 35.6.3 "Regression Testing with Golden Traces" and 35.6.5 "CI/CD Pipeline for Agents".
- **Self-improving agents (26.10)** is unmentioned in the chapter overview, big-picture callout, learning objectives, or the index. Reader cannot discover this section through normal navigation.

## Gaps
- **Three absorbed sections invisible to readers** because the index does not link them. Either add cards or merge their content into the original sections.
- **Cross-reference to "Chapter 32"** (in chapter overview, line 44, 50) - verify Chapter 32 still exists post-restructure (the project has 0-38 chapters per CLAUDE.md). 32 likely covers AI safety/alignment.
- **Prompt injection benchmarks**: 26.1 should mention Tensor Trust, AgentDojo, Tap (specific 2024-2026 benchmarks); these are essential references for prompt-injection defense and likely covered in 26.6 but should be cross-linked.
- **No coverage of Anthropic's Constitutional AI defense pattern** in 26.1 despite its relevance to agent guardrails.
- **Sandboxing (26.2)** - missing comparison of E2B vs Modal vs RunPod vs Anthropic's tool-use sandbox; only Docker/Firecracker/gVisor covered.
- **Cost control (26.3)** - no concrete examples of OpenAI Usage API, Anthropic admin API for cost tracking.

## Errors
- **Heading numbers in absorbed sections** are wrong (35.X.Y instead of 26.X.Y).
- **section-26.10 file naming**: filename is `section-26.10.html` (decimal-suffix), and the chapter sort order in directory listing puts 26.10 between 26.1 and 26.2 alphabetically, which is OK but breaks numerical sort. Consider `section-26-10.html` or padded `section-26.010.html` if production tooling expects lexical sort - though this is a small issue.
- **Cross-references between chapters**: Module 26 likely linked from module 23 (security) and module 22 (deployment 22.5/22.6); these forward/back pointers should be verified after the renumbering settles.
- **OpenTelemetry agent semantic conventions**: Verify 26.3 references the GenAI semantic conventions which were updated in 2024-2025 (otel-genai); old code samples may use deprecated attribute names.
- **Section 26.6 (Security Benchmarks)**: Should explicitly name AgentDojo, ASB (Agent Security Bench), and Anthropic's prompt-injection benchmark; currently the index card is generic.

## Improvements
- **Either expose 26.8, 26.9, 26.10 in the chapter index** (add three cards, plus update learning objectives/overview) or merge their content into 26.3/26.4/26.5/(new section). The current state is the worst of both worlds: content exists but is hidden, while the original sections cover the same ground.
- **Run a renumbering pass on the absorbed sections**: change all `35.5.X`, `35.6.X`, `35.8.X` H2 numbers to `26.8.X`, `26.9.X`, `26.10.X` (matching their new section numbers).
- **Resolve duplication**:
  - Merge 26.4 and 26.8 into a single resilience section (keep the chaos engineering content from 26.8 - it is unique).
  - Merge 26.3 and 26.9 into a single observability section (keep the CI/CD content from 26.9).
  - Keep 26.10 (self-improving agents) as a new dedicated section since it covers ground absent from the rest of the chapter; add an index card and a learning objective for it.
- **Add concrete benchmark names to 26.6** (AgentDojo, ASB, Tensor Trust, OWASP LLM Top 10).
- **Add a section-end "How this connects to Chapter 32"** callout to make the safety bridge explicit.
- **Add a comparison table of sandbox providers** (E2B, Modal, RunPod, Daytona, Pydantic Logfire sandbox, Anthropic's hosted code execution) to 26.2.
- **Cross-link 23.4 (custom tool design security)** to 26.1 explicitly and vice versa.
- **Verify all "Chapter 32" cross-references resolve** under the current chapter numbering.

## One-thing-only fix
Add the three missing index cards for sections 26.8 (Reliability Engineering), 26.9 (Observability, Testing, CI/CD), and 26.10 (Self-Improving and Adaptive Agents) to the chapter index, and renumber their internal H2 headings from `35.X.Y` to `26.8.X`/`26.9.X`/`26.10.X`. Currently, three full sections of content are orphaned (no entry in the chapter index, internal numbering still claiming they belong to the old module 35) and readers cannot find them.
