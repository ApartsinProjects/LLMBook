# Module 25: Specialized Agents

**Audit date**: 2026-05-11
**Sections reviewed**: 25.1, 25.2, 25.3, 25.4 (only four section files exist on disk)
**Total word count**: ~16,400 (HTML markup included)

## Summary
Topical chapter on code, browser, computer-use, research, and domain-specific agents. Like modules 22 and 24, the chapter has the unfinished-restructure problem: index advertises 8 sections (25.1-25.8) but only 4 files exist. Multiple cards link to the same files; one card even cross-jumps to module 22. Internal heading numbers in section-25.4 are stale ("25.7.x").

## Inconsistencies
- **Index has 8 cards but only 4 section files exist**:
  - Cards: 25.1 Code Generation, 25.2 Browser/Web, 25.3 Computer Use, 25.4 Research/Data Analysis, 25.5 Domain-Specific, 25.6 SWE-bench, 25.7 Code/Work Workflows, 25.8 AI-generated code analysis
  - Files: section-25.1.html, section-25.2.html, section-25.3.html, section-25.4.html
- **Card linking is wrong/duplicate**:
  - Card 25.1 Code Generation → section-25.1.html (correct)
  - Card 25.2 Browser & Web → section-25.2.html (correct)
  - Card 25.3 Computer Use → section-25.2.html (DUPLICATE - same file as 25.2)
  - Card 25.4 Research & Data → section-25.3.html (off-by-one)
  - Card 25.5 Domain-Specific → section-25.1.html (DUPLICATE - same file as 25.1)
  - Card 25.6 SWE-bench → `section-22.4.html` (CROSS-CHAPTER LINK to module 22's evaluation file)
  - Card 25.7 Code/Work Workflows → section-25.4.html (file is 25.4 by name)
  - Card 25.8 AI-Generated Code Analysis → section-25.4.html (DUPLICATE - same as 25.7)
- **Internal heading numbers in section-25.4.html use 25.7.x** (lines 36, 47, 130, 199, 235, 280, 351, 404) - matches the index card "25.7" but not the file number "25.4" or the file title "Section 25.4".
- **section-25.2 line 100**: Code Fragment 25.2.1 caption contains malformed cross-ref: "The <a class='cross-ref' href='../module-22-ai-agents/section-22.1.html'>Section 22.1</a> sends tool_use responses..." - cross-ref text was substituted into a sentence where the noun phrase should be "agent" or "code". Reads as gibberish.
- **section-25.2 line 102**: Code Fragment 25.2.2 caption explicitly labeled "Step 4 stub" - placeholder content.
- **section-25.4 covers 8 H2 sub-sections** (25.7.1-25.7.8) but title is "Section 25.4". File is misnumbered or the index is misnumbered.
- **Agent X persona**: Index attributes the epigraph to "Agent X, Versatile AI Agent" with avatar `attn.png`. Same "Agent X / Attn" identity confusion as module 22.

## Gaps
- **Sections 25.3 (Computer Use), 25.5 (Domain-Specific), 25.6 (SWE-bench), 25.8 (AI-generated code quality) have no dedicated section files**. The "Computer Use" topic is critical (Anthropic Computer Use, OS-World) and has no body content. SWE-bench is treated as cross-link to module 22. Domain-Specific (healthcare/legal/finance) is entirely missing.
- **section-25.3 Research & Data Analysis** is short (~2,700 words) for a topic of growing importance.
- **No coverage of Claude Code's actual conventions** (CLAUDE.md, hooks, plugins) - despite the chapter index promising "CLAUDE.md conventions" in card 25.7.
- **No code-quality static-analysis examples** (CodeQL, Semgrep, Bandit) despite explicit objective.
- **section-25.1 only has 2 H2s** (25.1.1, 25.1.2). Overly thin for "Code Generation Agents".
- **No evaluation methodology comparison** for code agents (pass@1 vs SWE-bench Verified vs SWE-bench Live methodology differences).
- **No mention of HumanEval, MBPP**, or competitive coding benchmarks (LiveCodeBench, CodeForces).

## Errors
- **section-25.2 line 100**: Cross-ref-replaces-noun bug as in modules 19 and 23 ("The Section 22.1 sends..."). Verify and remove the broken auto-link.
- **section-25.2 Code Fragment 25.2.2**: "Step 4 stub" label - lab content is incomplete.
- **Card 25.6 → section-22.4.html**: SWE-bench is covered both in module 22 (Section 22.4 Agent Evaluation per file naming, despite card-vs-file mismatch in module 22) and advertised again in module 25 card 25.6. Risk of either duplication or broken cross-module navigation if module 22's section-22.4 ever moves.
- **section-25.4 internal heading numbers (25.7.x) do not match file number (25.4)** - same renumbering bug as module 22's section files.
- **AI tool naming**: Verify Devin, Codex (OpenAI's renamed agentic coding agent), Cursor, Windsurf, Copilot Workspace are still the canonical 2026 names; this market churns rapidly.
- **The "85% Adoption Statistic"** (section-25.4 line 404) needs an explicit citation - this is a strong claim that requires sourcing.

## Improvements
- **Add the missing section files** (25.3 Computer Use, 25.5 Domain-Specific, 25.6 SWE-bench dedicated, 25.8 AI-Generated Code Quality) or remove the dangling index cards. Current state is broken.
- **Renumber section-25.4 internal H2s from 25.7.x to 25.4.x** OR rename the file to section-25.7.html and update the card link accordingly.
- **Fix the cross-ref-replaces-noun bug in section-25.2 line 100** ("The Section 22.1 sends...").
- **Replace "Step 4 stub" code caption** with real lab content or remove the stub.
- **Add a comparison table** for Claude Code, Cursor, Windsurf, Devin, Codex (rows) with pricing, deployment model, agent loop type, file/IDE access, sandbox model (columns). Date the table.
- **Cross-reference SWE-bench (module 22.4 file = card 22.5) and module 25 card 25.6** to one canonical location with clear forward/back pointers.
- **Add a code-quality lab** that runs CodeQL/Semgrep/Bandit against AI-generated code samples to demonstrate static analysis.
- **Add Anthropic Computer Use code example** to a future 25.3 (or expand 25.2 to include it) - currently the topic is mentioned in index but invisible in body text.
- **Cite the "85% adoption" statistic** with primary source (likely Stack Overflow Developer Survey 2024 or GitHub Octoverse).
- **Standardize agent epigraph identity** (Agent X vs Attn vs other) across all chapters.

## One-thing-only fix
Either author the four missing section files (25.3, 25.5, 25.6, 25.8) or delete those four index cards and renumber the existing four sections. The current chapter index advertises 8 sections but only 4 files exist; clicking 25.3 takes the reader to 25.2's file, clicking 25.5 takes the reader to 25.1's file, and clicking 25.6 jumps the reader entirely out of the chapter into module 22.
