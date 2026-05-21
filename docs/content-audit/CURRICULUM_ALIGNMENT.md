# Curriculum Alignment Audit (Cycle 1.5 Retry)

Agent: 01-curriculum-alignment
Date: 2026-05-19
Branch: v2.0
Scope: Verified prerequisites and cross-part references in chapter index pages,
focusing on the chapters flagged by cycle 1.5's narrative-continuity findings,
plus a sampling of others across Parts IV-XI.

## Chapters checked (17 chapters total)

Priority list from cycle 1.5:
- Chapter 19 (Part IV Tools of the Trade)
- Chapter 25 (Part V Tools of the Trade)
- Chapter 29 (Specialized Agents)
- Chapter 30 (Part VI Tools of the Trade)
- Chapter 32 (RAG Fundamentals)
- Chapter 37 (Conversational AI)
- Chapter 45 (Part IX Tools of the Trade)

Random sample across Parts IV-XI:
- Chapter 15 (Synthetic Data, Part IV)
- Chapter 20 (Audio/Video, Part V)
- Chapter 21 (Document Understanding, Part V)
- Chapter 26 (AI Agent Foundations, Part VI)
- Chapter 27 (Tool Use, Part VI)
- Chapter 28 (Multi-Agent Systems, Part VI)
- Chapter 31 (Embeddings, Part VII)
- Chapter 33 (Cross-Modal RAG, Part VII)
- Chapter 34 (NER, Part VII)
- Chapter 35 (Advanced RAG, Part VII)
- Chapter 36 (Retrieval Tools, Part VII)
- Chapter 40 (Voice/Realtime, Part VIII)
- Chapter 41 (Conv AI Tools, Part VIII)
- Chapter 42 (Eval Foundations, Part IX)
- Chapter 46 (LLM-as-Judge, Part IX)
- Chapter 47 (Adversarial Security, Part X)
- Chapter 48 (Guardrails, Part X)
- Chapter 49 (Agent Safety, Part X)
- Chapter 50 (Privacy, Part X)
- Chapter 51 (Part X Tools of the Trade)
- Chapter 52 (Bias/Fairness, Part XI)

## Fixes applied (15 edits across 13 files)

### Cross-part / cross-chapter reference corrections

1. **Chapter 15, Learning Objectives**: "preparing data for fine-tuning
   (Chapter 18) and alignment (Chapter 20)" -> Chapter 16 and Chapter 18.
   Chapter 16 is Fine-Tuning Fundamentals; Chapter 18 is Alignment.

2. **Chapter 26, Looking Back**: "Parts I through V built up to 'an LLM that
   retrieves, fine-tunes, and converses.'" -> reframed to "read, write, reason,
   and perceive across modalities" since retrieval (Part VII) and conversation
   (Part VIII) come AFTER Part VI. Also corrected "Chapter 14" -> "Chapter 12
   and Chapter 11" for prompt-pattern attribution.

3. **Chapter 27, Big Picture**: "prerequisites for the specialized and
   multi-agent systems in Chapters 24 and 25" -> Chapters 28 and 29
   (multi-agent and specialized agents).

4. **Chapter 28, Chapter Overview + Big Picture**: "safety considerations in
   Chapter 25" -> "agent safety considerations in Chapter 49" (twice).
   Chapter 25 is Multimodal Tools; agent safety is Chapter 49.

5. **Chapter 31, Looking Back**: "Part IV adapted the model. Part V gives the
   model memory. Everything in Chapter 23 (RAG) and Chapter 24 (Conversational
   AI) sits on this layer." -> "Part VI gave the model agency. Part VII gives
   it memory. Everything in Chapter 32 (RAG), Chapter 33 (Multimodal RAG), and
   Chapter 37 (Conversational AI) sits on this layer."

6. **Chapter 37, Looking Back**: "RAG (Chapter 23) handles a single question"
   -> "RAG (Chapter 32)". RAG is Chapter 32, not 23.

### Part-number drift fixes

7. **Chapter 45, Big Picture**: "Part VIII split into two halves: evaluation
   and production" -> "Part IX split into two halves." Chapter 45 is in Part
   IX; the old text referenced Part VIII (Conversational AI).

8. **Chapter 45, Section 45.4 descriptor**: "Two model categories matter for
   Part VIII" -> "Part IX".

9. **Chapter 45, Section 45.5 descriptor**: "Part VIII's literature is split
   between the academic eval community" -> "Part IX's literature".

10. **Chapter 47, Looking Back**: "Parts III-VIII built and operated LLM
    systems. Part IX zooms out to the questions that determine whether those
    systems are allowed to exist: safety threats, hallucination defense, bias
    and fairness, regulation..." -> rewritten to "Parts III-IX built, operated,
    and evaluated LLM systems. Part X zooms in on adversarial pressure..."
    The old text conflated Part X (security) with Part XI (ethics/regulation).

11. **Chapter 47, Chapter Overview**: stale references to "production
    engineering foundations from Chapter 45" (ch 45 is Eval Tools, not
    production engineering), "alignment techniques covered in Chapter 20" (ch
    20 is Audio, not alignment), and "ROI considerations in Chapter 31"
    (ch 31 is Embeddings). Rewritten to point to Part IX evaluation, Chapter
    18 alignment, Chapter 48 runtime defenses, and Chapter 49 agent safety.

12. **Chapter 47, Big Picture**: "the alignment techniques of Chapter 20"
    -> Chapter 18.

13. **Chapter 47, Learning Objectives**: "interpretability methods from
    Chapter 11" -> Chapter 10. Chapter 11 is LLM APIs; interpretability is
    Chapter 10.

14. **Chapter 49, Big Picture**: "Chapter 47 covered safety and regulation
    for LLMs that talk" -> updated to reflect that Chapter 47 covers
    adversarial attacks/red teaming, Chapter 48 covers guardrails.

15. **Chapter 51, Section 51.1 descriptor**: "Part IX's platforms" -> "Part
    X's platforms".

16. **Chapter 51, Big Picture**: "Part IX is the safety, security, and ethics
    part of the book" -> "Part X is the security and runtime safety part of
    the book (Part XI extends to ethics, trust, and governance)."

### Broken forward-reference fixes (What's Next / What Comes Next)

17. **Chapter 47, What's Next**: pointed to Chapter 49 (Agent Safety) even
    though the chapter-nav points to Chapter 48 (Guardrails). Rewritten to
    correctly preview Chapter 48 first, then note Chapter 49 and 50 follow.

18. **Chapter 48, What's Next**: was a generic "This chapter begins with
    Section 48.1..." with no forward reference. Replaced with a proper
    preview of Chapter 49 (Agent Safety & Autonomy).

19. **Chapter 49, What Comes Next**: pointed to "Chapter 51" but the chapter-
    nav next is Chapter 50 (Privacy). Rewritten to preview Chapter 50 first
    and mention that Chapter 51 closes Part X.

20. **Chapter 50, What's Next**: was a generic intra-chapter pointer.
    Replaced with a real forward reference to Chapter 51 (Tools of the Trade).

21. **Chapter 51, What Comes Next**: claimed "Part X turns to the product
    side: idea to ship, with AI coding tools, project tooling, and analytics.
    Chapter 71 closes Part X with the product-builder toolbox." This is
    entirely the wrong part (Product Design is Part XIV). Rewritten to
    preview Part XI (Ethics, Trust & Governance) and Chapter 52 (Bias).

22. **Chapter 52, What's Next**: was a generic intra-chapter pointer.
    Replaced with a real forward reference to Chapter 53 (Regulation,
    Compliance, and Governance).

### Chapter 42 Looking Back

23. **Chapter 42**: "You have built something (Parts III-VII)" -> "Parts
    III-VIII" (forgot to include Part VIII Conversational AI in the buildup).

## Prerequisites (verified, no changes needed)

All chapters' `<div class="prerequisites">` callouts surveyed point to valid
earlier chapters. The prerequisite chains hold up: each chapter only references
content that has been covered (with the lone exception of Chapter 27 saying
"covered in detail later in the book" for RAG, which is acceptable bridge
language).

The Chapter 32 cycle-1.5 finding about "skipped chs 33-36" appears to be about
the previous draft; the current text references Chapter 33 correctly and the
chapter is followed naturally.

## Summary

- 23 concrete fixes across 13 chapter index pages
- Most issues clustered in Part X (Security/Safety chapters 47-51) where part
  numbering had drifted (Part IX vs Part X vs Part XI mixed up repeatedly)
- Several "What's Next" callouts had degenerate generic text ("each section
  builds on the previous one") instead of real forward references; replaced
  with substantive previews
- A handful of cross-chapter "see Chapter N" references pointed to the wrong
  chapter number, often off by 5-15 chapters (legacy from a prior numbering)

Overall alignment score after fixes: STRONG.

No fabricated prerequisites were added; only stale references corrected and
generic boilerplate "what's next" sections replaced with substantive previews
that match the actual chapter-nav forward pointer.
