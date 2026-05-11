# Module 22: AI Agent Foundations

**Audit date**: 2026-05-11
**Sections reviewed**: 22.1, 22.2, 22.3, 22.4, 22.5, 22.6
**Total word count**: ~35,400 (HTML markup included)

## Summary
Strong topical coverage of agents, planning, reasoning models, evaluation, deployment, and memory architectures, but the chapter is currently in a broken intermediate state from an unfinished restructure. Index card numbers no longer match section filenames or section internal numbering, and the section bodies still carry the old (pre-renumber) heading numbers. This module needs a careful renumbering audit before publication.

## Inconsistencies
- **Index has 8 cards but only 6 section files exist on disk**. Files: 22.1 through 22.6. Cards 22.7 ("Memory Architecture for Agents", linking to section-22.6.html) and 22.8 ("Research Replication Benchmarks", linking to section-22.4.html) are dangling/duplicate links to existing files.
- **Index card-to-file linking is shifted by one**:
  - Card "22.2 Agent Memory Systems" → links to `section-22.6.html` (which is *Memory Architecture for Agents*, not Agent Memory Systems)
  - Card "22.3 Planning & Agentic Reasoning" → links to `section-22.2.html` (correct content, wrong-numbered file: section-22.2.html holds Planning material)
  - Card "22.4 Reasoning Models" → links to `section-22.3.html` (which actually contains Reasoning Models)
  - Card "22.5 Agent Evaluation & Benchmarks" → links to `section-22.4.html` (which contains evaluation)
  - Card "22.6 End-to-End Agent System Architecture" → links to `section-22.5.html` (which contains the deployment blueprint)
  - Card "22.7 Memory Architecture for Agents" → links to `section-22.6.html` (which already serves card 22.2)
  - Card "22.8 Research Replication Benchmarks" → links to `section-22.4.html` (already serves card 22.5; no real 22.8 file exists)
- **Section internal heading numbers are stale (pre-renumber)**:
  - `section-22.2.html` has H2s `22.3.1`, `22.3.2`, `22.3.3` (should be 22.2.x or 22.3.x depending on intended final number)
  - `section-22.3.html` has H2s `22.4.1`, `22.4.2`, `22.4.3` (file is "22.3" by name+title, but body uses 22.4.x)
  - `section-22.4.html` has H2s `22.4.1`, `22.4.2`, `22.4.3` (matches file number, but title is "Section 22.4: Agent Evaluation" so this is actually fine - and conflicts with section-22.3 also using 22.4.x)
  - `section-22.5.html` has H2s `22.6.1`, `22.6.2`, `22.6.4`, `22.6.5`...`22.6.10` (file is 22.5 by name, title says 22.5, but body numbered 22.6.x; also note jump from 22.6.2 to 22.6.4, missing 22.6.3)
  - `section-22.6.html` has H2s `22.7.1`...`22.7.8` (file is 22.6 by name, title says 22.6, body numbered 22.7.x)
- **No 22.1.5 trim visible**: The user notes 22.1.5 was trimmed, but `section-22.1.html` still has H2 `22.1.5 Agent Memory Systems` (line 511). If trimmed it should be removed; if kept it duplicates the dedicated memory section (22.6 by file, 22.7 by index card).
- **Section 22.5 jump 22.6.2 → 22.6.4** in headings (skipping 22.6.3): either a section was deleted without renumbering or a stub is missing.
- **section-22.4.html has duplicate lab-title**: `<h3 class="lab-title">Lab: Evaluate an Agent on SWE-bench Lite</h3>` followed by `<h3 class="lab-title">Lab: Evaluate a Code Agent on SWE-bench Lite</h3>` (lines 102, 104). One is leftover.
- **Code captions in section-22.6 are doubled**: Every caption like `Code Fragment 22.6.1: Code Fragment 22.6.1: Memory storage abstraction` (line 152, 258, 352, 433, 489, 575). The inline `# Code Fragment` source comment got concatenated into the rendered caption text - same bug as Module 20's section 20.7.
- **Chapter prev-nav** points to `module-21-conversational-ai/section-21.1.html` titled "Human-AI Interaction Patterns & Evaluation" - same wrong link as Module 21's broken 21.7 entry.

## Gaps
- **No 22.7 or 22.8 file** despite the index advertising them. Either author the missing sections (especially 22.8 Research Replication Benchmarks, which would cover SciCode/MLE-bench) or remove the cards from the index.
- **Missing memory-section integration**: The chapter has memory content in three places (section-22.1.5 stub, section-22.6 = "22.7" body, and the index card "22.2 Agent Memory Systems" pointing to the same section-22.6). Pick one canonical location and prune the others.
- **Section 22.3 (Reasoning Models)** is short (~6,500 words including code) for a topic of growing importance. Consider expanding with concrete configuration examples for o3/o4, Claude Sonnet 4.5 thinking, DeepSeek-R1.

## Errors
- **Section 22.1.6 Token Budget Management** (line 537) duplicates content in section-22.6 (memory architecture)'s "22.7.4 Read Policies: Context Window Budgeting".
- **Section 22.5 (deployment blueprint) lab references SWE-bench Lite** but the underlying section is supposed to be deployment-focused; ensure the lab in 22.4 is the SWE-bench one and 22.5's lab (if any) is deployment-focused.
- **Section 22.3 cites "o1/o3" and "DeepSeek-R1"** without dates - by 2026-05 these labels may be outdated (o4-mini, DeepSeek-R1.5, etc.); add an "as of date" footnote.
- **Models referenced in epigraph attribution**: Index uses "Agent X" with avatar `attn.png` (which is the Attn agent). The agent identity ("Agent X" vs "Attn") is unclear; verify naming.

## Improvements
- **Run a single renumbering pass** to align: (a) chapter index card numbers, (b) section filenames, (c) section `<title>` and `<h1>`, (d) all internal `<h2>` numbers (22.X.Y form), and (e) all figure/code-fragment number prefixes. Currently the four numbering systems are out of sync.
- **Strip the duplicate `Code Fragment N:` text** from section-22.6 captions (same bug fix needed as in 20.7).
- **Decide between two memory sections**: either keep just section-22.6 ("Memory Architecture") and cut the 22.1.5 stub from section-22.1, or keep 22.1.5 as a brief preview and have section-22.6 do the deep dive (currently both exist with overlapping content).
- **Add a "Section status" key at the top of `module-22-ai-agents/index.html`** (or fix the cards entirely) so readers do not click the same file from two different cards.
- **Add 22.5 deployment diagram** to clarify the eight components ("22.6.1 The Eight Components" implies a diagram but none is in the heading list).
- **Standardize the chapter's epigraph** (Russell & Norvig's classic AI definition is usually attributed to "Russell & Norvig"; attributing it to "Agent X" via the textbook agent persona is fine but include the original source line for accuracy).
- **Connect 22.6 (memory) explicitly to 21.3 (memory)** since they cover overlapping material from different angles (chat memory vs agent memory). Add a forward/back pointer.
- **Add a per-section diagram inventory check**: many sections only have one figure; agent architecture content benefits from more diagrams (state machines, ReAct loops, planning trees).

## One-thing-only fix
Run a renumbering correction pass across `module-22-ai-agents/index.html` plus all six `section-22.*.html` files to align card numbers, file names, titles, internal H2 numbering (currently 22.2 file holds 22.3.x heads; 22.3 holds 22.4.x; 22.5 holds 22.6.x; 22.6 holds 22.7.x), and to delete the dangling 22.7/22.8 index cards. The chapter is functionally unreadable until this is fixed because index cards point to wrong files.
