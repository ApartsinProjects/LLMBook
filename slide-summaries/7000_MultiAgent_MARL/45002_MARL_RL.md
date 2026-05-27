# 45002_MARL_RL — Per-Slide Summary

**Source file:** `45002_MARL_RL.pptx`
**Source folder:** `SlidesPool/7000_MultiAgent_MARL/`
**Drive link:** https://drive.google.com/file/d/1Z4jqVxyv0LVtDF2r5YNSRY8pLLZflvbf/view
**Slide count (exact, via python-pptx):** 38
**Extraction:** Local parse + slide PNG render. Many slides embed Bellman equations and algorithm pseudocode as images, so slide PNGs were inspected to recover the algorithmic content.

---

## Slide 1 — MARL
Divider for the "2. Reinforcement Learning" lecture, the single-agent RL refresher that grounds the rest of the MARL module.

## Slide 2 — Single Agent RL
Two-bullet framing. Single-agent RL is built on Markov Decision Processes (MDPs), which represent the environment with partially or fully known parameters. RL algorithms learn an optimal policy by interacting with the MDP, knowing only some of its parameters in advance.

## Slide 3 — Definition
Formal definition slide. An MDP is a tuple (S, A, T, R, mu, gamma): state set S, action set A, transition function T(s' | s, a), reward function R(s, a, s'), initial state distribution mu, and discount factor gamma. Two formula images carry the precise notation.

## Slide 4 — Sequential Decision Process and Slution
Frames the agent loop. Per timestep the agent receives an observation, chooses an action, and gets a scalar reward. The solution is an optimal policy that maximizes the expected return (sum of returns from each state onward).

## Slide 5 — Reinforcement Learning Loop
Standard agent-environment loop diagram. The agent emits an action, the environment responds with the next state and a reward, and the cycle continues.

## Slide 6 — Trial and Error Learning
Names the central learning principle. The agent learns by trying actions, observing outcomes, and updating beliefs. This forces the exploration-exploitation dilemma: explore poorly-understood actions vs. exploit the currently-best estimate.

## Slide 7 — MDP: Markov Decision Process
Divider for the formal MDP section.

## Slide 8 — MDP
States the Markov property formally (next state and reward depend only on current state and action) and introduces the immediate (or expected) reward as the basic quantity tied to each (s, a) pair.

## Slide 9 — Example: Mars Rover MDP
Concrete worked example. A Mars rover MDP with five states (Start, Site A, Site B, Base, Destroyed, Immobile) and two actions (left, right). Each transition arc is labeled with action, probability, and reward, for instance (left from Start) goes to Site A with p = 0.9 and reward -1, or to Immobile with p = 0.1 and reward -3. Terminal states are Destroyed, Base, and Immobile. The graph makes every later abstract definition immediately checkable.

## Slide 10 — Basic RL Assumptions
Distinguishes "known model" vs. "learning from interaction". The basic RL setup assumes the agent knows the set of states and actions but not the transition function or reward function; both have to be learned through trial and error.

## Slide 11 — Multi-armed Bandit
Brief refresher on the multi-armed bandit as the degenerate MDP (single state, choose action, receive reward), used to anchor the discount factor and value definitions that follow.

## Slide 12 — POMDP
Generalizes MDP to POMDP (Partially-Observable MDP). The agent no longer sees the true state s but only an observation o derived from s. Partial observability is the rule rather than the exception in real-world MARL.

## Slide 13 — Expected Returns
Defines the expected return: the sum (or expectation over stochastic policies) of rewards from time t to end of episode. Five embedded images carry the math for finite-horizon returns and the conditional notation E[R | s, pi]. The speaker note flags that the dot in some equations is a placeholder for the random action variable.

## Slide 14 — Discounted Expected Return
Handles the infinite-horizon case. With non-terminating MDPs (e.g., a continuous stream of orders), the un-discounted return is infinite. The fix is the discounted return sum_{t=0}^{inf} gamma^t r_t, which is bounded as long as rewards lie in a finite range and gamma is less than 1.

## Slide 15 — Interpretations of discount factor
Two complementary readings of gamma. Interpretation 1: it is a per-step termination probability (the MDP terminates with probability 1 - gamma at each step, with absorbing zero-reward states modeling finite episodes inside an infinite framework). Interpretation 2: it is simply a weight that the agent assigns to future rewards (smaller gamma means more myopic agent).

## Slide 16 — Value Function and Bellman Equation
Divider for the value-function and Bellman section.

## Slide 17 — Value function for a policy
Defines V_pi(s), the state-value function, as the expected return starting in state s under policy pi. The Markov property gives a recursive form (Bellman expectation equation), V_pi(s) = sum_a pi(a | s) sum_s' T(s' | s, a) [R(s, a, s') + gamma V_pi(s')], a linear system in V given pi and the MDP.

## Slide 18 — Action Value function
Defines Q_pi(s, a), the action-value function, as the expected return for taking action a in state s then following pi. Q_pi(s, a) = sum_s' T(s' | s, a) [R(s, a, s') + gamma V_pi(s')] is the companion Bellman equation.

## Slide 19 — Optimal value
Defines V* and Q* as the maxima of V_pi and Q_pi over all policies pi.

## Slide 20 — Optimal value based on optimal decisions
Writes the Bellman optimality equations, which do not reference any specific policy pi: V*(s) = max_a Q*(s, a). The note flags that the optimal policy is deterministic whenever the max is unique, no benefit in randomizing when one action is strictly best.

## Slide 21 — Bellman Optimality Equation for Value State
Expands V*(s) = max_a sum_s' T(s' | s, a) [R(s, a, s') + gamma V*(s')], a system of m non-linear equations (the max makes it non-linear) in m unknowns where m is the number of states. The optimal policy is recovered as pi*(s) = argmax_a Q*(s, a).

## Slide 22 — Dynamic Programming
Divider for the Dynamic Programming section.

## Slide 23 — Dynamic Programming
DP assumes complete knowledge of the MDP (transition probabilities and rewards) and computes V and pi by alternating two steps starting from a uniform random policy: policy evaluation (compute V_pi) and policy improvement (greedify with respect to V_pi). This is the textbook policy-iteration loop.

## Slide 24 — Policy Evaluation Task
Pseudocode for policy evaluation: iterate V(s) <- sum_a pi(a | s) sum_s' T(s' | s, a) [R(s, a, s') + gamma V(s')] until convergence.

## Slide 25 — Policy Improvement Task
Pseudocode for policy improvement: given a V, set pi(s) <- argmax_a sum_s' T(s' | s, a) [R(s, a, s') + gamma V(s')] for every state.

## Slide 26 — Value Iteration Algorithm
Value iteration collapses the two steps into one. Algorithm 1 from the slide: initialize V(s) = 0; repeat V(s) <- max_a sum_s' T(s' | s, a) [R(s, a, s') + gamma V(s')] for all s until V converges; return pi*(s) = argmax_a sum_s' T(s' | s, a) [R(s, a, s') + gamma V(s')]. Uses the Bellman optimality equation directly.

## Slide 27 — Temporal-Difference Learning
Divider for the Temporal-Difference (TD) learning section, where the agent no longer knows the MDP.

## Slide 28 — TD: Temporal-Difference Learning
The shift from DP to TD: DP requires the full transition and reward functions, but TD learns V and pi from experienced (s, a, r, s', ...) tuples by combining sampled transitions with bootstrapped value estimates.

## Slide 29 — TD process
Step-by-step illustration of the TD update: the agent visits states s_t, observes r_t and s_{t+1}, and applies V(s_t) <- V(s_t) + alpha [r_t + gamma V(s_{t+1}) - V(s_t)] (the TD(0) update). Four images cover successive applications across a small example trajectory.

## Slide 30 — Sarsa algorithm
SARSA (state, action, reward, state, action) is on-policy TD control. Use the current epsilon-greedy policy to select both the current and next action, then update Q(s, a) toward r + gamma Q(s', a'). Four panels develop the four ingredients of the acronym.

## Slide 31 — Sarsa
Algorithm 2 in formal pseudocode: initialize Q(s, a) = 0, for each episode observe s^0, choose a^0 epsilon-greedily, then for t = 0, 1, 2, ... apply a^t, observe r^t and s^{t+1}, choose a^{t+1} epsilon-greedily, and update Q(s^t, a^t) <- Q(s^t, a^t) + alpha [r^t + gamma Q(s^{t+1}, a^{t+1}) - Q(s^t, a^t)].

## Slide 32 — Q-learning
Q-learning is the off-policy sibling of SARSA. The learning target uses max_a' Q(s', a') (the value of the greedy action in s') rather than Q(s', a'_taken). The two side-by-side panels make the contrast vivid: SARSA needs the next sampled action; Q-learning only needs the next state.

## Slide 33 — Q-Learning
Algorithm 3 in formal pseudocode: initialize Q(s, a) = 0, for each episode and each step observe s^t, pick a^t epsilon-greedily, apply it, observe r^t and s^{t+1}, and update Q(s^t, a^t) <- Q(s^t, a^t) + alpha [r^t + gamma max_a' Q(s^{t+1}, a') - Q(s^t, a^t)]. The single max operator is the off-policy bootstrap.

## Slide 34 — Off-policy vs. On-policy algorithm
Names the distinction. SARSA is on-policy: it both behaves and learns according to the current epsilon-greedy policy. Q-learning is off-policy: behavior can come from any policy that visits every (s, a) infinitely often, while the learned Q converges to Q*.

## Slide 35 — Evaluation with learning curves
Divider for the empirical-evaluation section.

## Slide 36 — Evaluate performance of RL algorithm
Defines the empirical protocol on the Mars rover MDP. The y-axis is the average discounted return from the initial state under the current greedy policy, averaged over 100 evaluation runs. The x-axis is the cumulative training steps across all training episodes. This is the standard "wall-clock" learning curve.

## Slide 37 — Q-learning learning rates
Discusses the learning-rate schedule alpha. With k = number of times state s and action a have been visited, a 1/k schedule guarantees convergence but is too aggressive in early learning; a constant alpha tracks non-stationary value functions better but never fully converges; the three plots show learning curves for different schedules on the rover MDP.

## Slide 38 — Different Definition of Reward Function
Closing technicality. The MDP reward function can be defined either over (s, a) (single-state form, R(s, a)) or over (s, a, s') (two-state form, R(s, a, s')). The two are equivalent: any MDP under one definition can be rewritten as an MDP under the other.

---

## Deck-level takeaway

This is a single-agent RL refresher inside the MARL course, deliberately written to make the MARL extensions in later decks land. It walks the full canonical sequence in 38 slides: MDPs and the Markov property, value and action-value functions, Bellman expectation and optimality equations, dynamic programming (policy iteration and value iteration) for known MDPs, then temporal-difference learning (SARSA on-policy and Q-learning off-policy) for unknown MDPs. The Mars-rover MDP on slide 9 is the worked example that every subsequent algorithm is checked against. The two pedagogical anchors are: (1) the SARSA vs. Q-learning contrast (slide 32) is the cleanest single illustration of the on-policy vs. off-policy distinction in all of RL, and (2) the value-iteration algorithm box on slide 26 is the reader's mental model of "use Bellman optimality directly". Once the reader has those two firmly, the rest of the MARL module can extend each piece to N agents (joint Q-learning, decentralized policies, equilibrium selection) without re-deriving the basics.
