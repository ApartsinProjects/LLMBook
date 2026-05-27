# 45001_MARL_Introduction — Per-Slide Summary

**Source file:** `45001_MARL_Introduction.pptx`
**Source folder:** `SlidesPool/7000_MultiAgent_MARL/`
**Drive link:** https://drive.google.com/file/d/1PCbKeHw8uef_2pj_ncxkQioCEmCMk6De/view
**Slide count (exact, via python-pptx):** 14
**Extraction:** Local parse + slide PNG render. Most content is in text frames; the MARL loop diagram and the MARL dimensions table were inspected as PNGs.

---

## Slide 1 — MARL
Divider for the "1. Introduction" lecture of the multi-agent reinforcement learning module.

## Slide 2 — Multiagent Systems
Defines a multi-agent system as a collective of autonomous agents, each capable of independent decision-making, interacting in a shared environment to achieve goals. Two regimes are contrasted: shared-goal systems such as a fleet of warehouse robots, and conflicting-goal systems such as competing traders.

## Slide 3 — Learning and Uncertainty
Argues that the interactions are too complex to hand-design, so agents must learn from experience. Each agent tries actions, observes the environmental response and the behavior of other agents, and gradually becomes an expert at coordinating, the multi-agent generalization of single-agent RL.

## Slide 4 — MARL
Contrasts single-agent RL (one agent learns an optimal policy from rewards) with MARL (multiple agents simultaneously learning policies that depend on each other). The shared diagram from the canonical single-agent RL loop is shown for reference.

## Slide 5 — Environment
Describes the environment generically: a physical or virtual world with a state that evolves over time, an action space possibly depending on state, and per-agent observations that may be partial. Uses a 2D maze example with positions and orientations as the state, four movement actions, and partial nearby-agent observations.

## Slide 6 — Agents
Describes an agent: receives observations, chooses actions, possibly carries prior knowledge of the state space and dynamics, is goal-oriented through a reward function, and follows a deterministic or probabilistic policy that maps current and past observations and actions to a next action.

## Slide 7 — Example: Foraging
Concrete cooperative-foraging environment. Multiple robots, each with a skill level, must collect items; an item can only be collected when a group of adjacent robots has summed skill at least equal to the item's level. The full state is the robot positions, the item positions, and a binary "alive" vector per item. Actions per robot are the four cardinal moves plus `collect` and `noop`.

## Slide 8 — MARL loop
The canonical MARL loop diagram. Each of agents 1 through n produces an action from its own observation; a joint-action operator combines them into a single environment input; the environment computes a new state and emits per-agent observations and rewards. Episodes run from an initial state to a terminal state.

## Slide 9 — Single vs. Multiple Agent RL
Quantifies why decentralized control matters. A single agent controlling three robots with 6 actions each must search a joint action space of size 6^3 = 216, and needs reliable communication with a central authority. Decentralizing into three independent agents shrinks each action space back to 6 but introduces the new challenge of learning decentralized policies that still coordinate.

## Slide 10 — Marl Dimensions
A two-column table laying out the design dimensions that organize the rest of the book. Size (number of agents, discreteness, action vectors), Knowledge (what agents know about their own and others' rewards and dynamics), Observability (full state vs. partial noisy), Rewards (zero-sum vs. shared vs. mixed), Objective (equilibrium type, performance-during-learning vs. final-only), Centralization and Communication (central controller vs. fully independent, reliability of the channel). Each row tags the chapter that elaborates it.

## Slide 11 — Example 1; Multi-robot Warehouse
A 100-robot warehouse environment. Agents observe their own location, carried items, and current order, plus the locations and orders of other robots; act with move/pick primitives plus inter-agent communication actions; and receive both individual rewards (for completing their own order) and a common reward (when any robot completes a global order). Cooperative, mostly shared-reward.

## Slide 12 — Example 2: Competitive Game Play (Board, Video)
A purely competitive example family: board games (chess, poker) and multiplayer video games (shooting, racing). Agents may see the full game state or only a partial view (their own cards). Reward is the canonical zero-sum +1 to the winner, -1 to the loser.

## Slide 13 — Example 3: Autonomous Driving
A mixed cooperative-competitive example. Actions are steering, braking, and accelerating; observations are own and nearby vehicles with noise and partial observability; rewards combine a shared component (avoid collisions) with individual components (efficient and natural driving).

## Slide 14 — Example 4: Automated Trading
Closing example. Agents are traders; actions are buy or sell; observations are prices, key economic indicators, and news; rewards are individual return on investment. Agents can both collaborate (agreeing on prices) and compete (maximizing personal ROI), a fully mixed-motive setting.

---

## Deck-level takeaway

The MARL introduction is a setup deck: it lays out vocabulary and design space without committing to a specific algorithm. The pedagogical pattern is to start from single-agent RL (already familiar), generalize the loop to N agents producing a joint action (slide 8), then explain why decentralization is not optional, the joint-action space explodes as 6^N even for trivial action sets (slide 9). The MARL Dimensions table on slide 10 is the conceptual map: every later lecture in the module slots into one of (Size, Knowledge, Observability, Rewards, Objective, Centralization & Communication). The four motivating examples (warehouse, board games, autonomous driving, trading) are deliberately chosen to span the reward spectrum from purely cooperative through mixed-motive to purely competitive, signaling that MARL is not one problem but a family. The single take-away the reader should leave with is the picture on slide 8 (the joint-action loop) and the awareness that "MARL" is shorthand for many related but distinct learning problems.
