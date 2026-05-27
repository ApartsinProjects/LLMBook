# 45003_MARL_Games — Per-Slide Summary

**Source file:** `45003_MARL_Games.pptx`
**Source folder:** `SlidesPool/7000_MultiAgent_MARL/`
**Drive link:** https://drive.google.com/file/d/1hHWWs4MyYCK2zq314tgL_-t1Gg4WhRJL/view
**Slide count (exact, via python-pptx):** 3
**Extraction:** Local parse + slide PNG render. The deck is a short stub that introduces the game-model hierarchy; the central Venn diagram was inspected visually.

---

## Slide 1 — MARL
Divider for the "3. Games" lecture of the MARL module.

## Slide 2 — Game models
Lays out the hierarchy of game models as nested ellipses, in order of increasing generality. At the innermost level sit two specialized models: Repeated Normal-Form Game (n agents, 1 state) and Markov Decision Process (1 agent, m states). Both are contained in Stochastic Game (n agents, m states, fully observed). Stochastic Game is contained in the outermost class, Partially Observable Stochastic Game (n agents, m states, partially observed). The diagram makes it clear that the single-agent MDP from the previous deck is a special case of the multi-agent stochastic game, and that POSG is the most general object the rest of the module will discuss.

## Slide 3 — Normal Form Games
Section-title slide for "Normal Form Games", signaling that the next lecture (or follow-up deck) will pick up the analysis of n-agent, single-state matrix games.

---

## Deck-level takeaway

A three-slide bridge deck. Its job is exactly one diagram: the nested-class Venn picture on slide 2 that places MDP and Repeated Normal-Form Game inside Stochastic Game inside Partially Observable Stochastic Game. The pedagogical point is that the reader's previous mental model (single-agent MDP) sits in a corner of a much larger taxonomy: add agents (n agents, 1 state) and a Normal-Form Game appears; add states (1 agent, m states) and an MDP appears; combine both and a Stochastic Game appears; remove full observability and a POSG appears. The last slide is a teaser title for the next deck, where Normal-Form Games (the simplest n-agent setting) will be unpacked in detail.
