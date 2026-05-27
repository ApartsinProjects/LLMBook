# 40001_DeepReinforce_Intro — Per-Slide Summary

**Source file:** `40001_DeepReinforce_Intro.pptx`
**Source folder:** `SlidesPool/6000_RL_Intro/`
**Drive link:** https://drive.google.com/file/d/17qr0AXI81kPe_4H12VQ34QKoX2ecKl0m/view
**Slide count (exact, via python-pptx):** 11
**Extraction:** Local parse + slide PNG render.

---

## Slide 1 — Deep Reinforcement Learning
Title slide for the first lecture of the deep RL module.

## Slide 2 — Reinforcement Learning
The one-line definition: an agent that *dynamically interacts with the environment*, in contrast to supervised learning where the dataset is fixed in advance. The diagram shows the canonical agent ↔ environment loop.

## Slide 3 — Rewards
Diagram of the reward signal — the scalar feedback the environment provides to the agent after each action. The lecture deliberately introduces rewards before policies because the reward signal is what makes the problem an RL problem rather than a control problem.

## Slide 4 — RL Framework
The formal framework: states, actions, rewards, transitions. A standard diagram showing how the agent's policy maps states to actions and how the environment maps state-action pairs to next-states and rewards.

## Slide 5 — Deep RL Agent
Diagram showing where the "deep" comes in: a neural network replaces the table-based policy or value function of classical RL, taking raw state (e.g., pixels) and outputting actions or values.

## Slide 6 — Python OpenAI Gym Library
The standard playground. OpenAI Gym (and its open-source fork *Gymnasium*) ships several pre-built environments (CartPole, Atari, MuJoCo, …) with a uniform API, so the same RL algorithm can be tested across many problems without writing per-environment code. Two screenshots.

## Slide 7 — Task-specific algorithm
A reference diagram for the per-task algorithmic choice — the slide implicitly sets up the rest of the module by hinting that there's a family of algorithms (Q-learning, policy gradient, actor-critic) and choosing one depends on the task.

## Slide 8 — Deep Q-network
First named deep RL algorithm: the *Deep Q-Network* (DQN), introduced specifically to process raw screen pixels (Atari, DeepMind 2013). The slide diagram is presumably the original DQN architecture sketch.

## Slide 9 — Why deep RL
The state-space argument for why deep RL is *necessary*, not optional. Tic-Tac-Toe has 255,168 positions — you can literally store the best action per position in a table. Atari games use 84×84 grey-scale screens, giving 256^(84×84) = 256^7056 possible states — vastly larger than the number of atoms in the observable universe. Tables are impossible; a neural network's *generalization across states* is the only way to play.

## Slide 10 — String diagram
A graphical convention used throughout the rest of the module: *string diagrams* for neural networks, showing input and output dimensions on the wires. Useful because RL architectures often have multiple heads (value head, policy head), recurrent connections, and varying input shapes.

## Slide 11 — Recurrent neural Network
Closing slide: a brief reminder of RNNs, motivated by the next-step input including the previous output — the natural choice for partially-observable RL problems where the agent must remember past observations.

---

## Deck-level takeaway

A short 11-slide opening for the deep-RL module. The pedagogical signature is *one big number*: the slide-9 comparison (Tic-Tac-Toe's 255K states vs. Atari's 256^7056 states) is the entire justification for why "deep" is part of the name — without function approximation, Atari is uncountable. Around that punchline the deck assembles the minimum vocabulary the reader needs to follow the rest of the module: agent / environment / reward / state, the Gym/Gymnasium API for hands-on experiments, DQN as the prototypical deep RL algorithm, and the string-diagram + RNN building blocks that the rest of the module will use.
