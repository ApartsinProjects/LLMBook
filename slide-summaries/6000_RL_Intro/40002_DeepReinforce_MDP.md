# 40002_DeepReinforce_MDP — Per-Slide Summary

**Source file:** `40002_DeepReinforce_MDP.pptx`
**Source folder:** `SlidesPool/6000_RL_Intro/`
**Drive link:** https://drive.google.com/file/d/1YnqamS2mFWyk-81wncBePGGHm8tnbX9U/view
**Slide count (exact, via python-pptx):** 35
**Extraction:** Local parse + slide PNG render. Many slides carry diagrams, Python code, and LaTeX-rendered formulas as embedded images, so visual inspection of slide PNGs was used to recover content for image-heavy slides.

---

## Slide 1 — DRL
Divider slide opening the second lecture of the deep RL module, titled "2. Markov Decision Process".

## Slide 2 — MAB: Multi-armed Bandit
Introduces the multi-armed bandit (MAB) setting using a row of five slot machines with five different unknown reward distributions D1 through D5. The agent pulls machine k, samples from the unknown reward distribution Dk, and observes a reward. The problem statement asks how to optimize total winnings under a finite pull budget T, motivating the explore-versus-exploit trade-off.

## Slide 3 — MAB task Formally
Formalizes the bandit task: n = 10 possible actions (machines), a single action k per play, and a reward Rk drawn after each action. Defines the action-value function Qk(a), or Q-function, as the empirical mean of rewards observed so far for that action, and shows both the math (Qk(a) equals sum of Ri divided by ka) and the corresponding Python pseudocode.

## Slide 4 — Exploitation vs. Exploration
Articulates the central tension in MAB. The agent must alternate exploration (sample many machines to learn their reward distributions) and exploitation (commit to the empirically best machine to maximize cumulative reward). Pure exploitation locks in early mistakes; pure exploration never cashes in on knowledge.

## Slide 5 — Python: Best Action
Shows the greedy strategy in Python: always pick the action with the highest empirical Q-value. The slide previews the failure mode of pure greedy, which the next slide patches.

## Slide 6 — Epsilon-Greedy Strategy
Introduces epsilon-greedy: with small probability epsilon take a uniformly random action, otherwise take the greedy action. This is the simplest fix to pure greedy and the default baseline exploration scheme throughout RL.

## Slide 7 — Define reward function
Defines a Bernoulli-style simulator for each machine. Each arm has a hidden success probability p; pulling the arm flips n = 10 biased coins and returns the count of successes, so the expected reward is 10p. A Python `get_reward(prob, n=10)` function and a histogram of 2000 reward samples (centered near 7 when p = 0.7) make the simulator concrete.

## Slide 8 — Maintain reward record
For each arm the agent stores the number of plays and the running mean reward. The slide shows the standard incremental-mean update rule (new mean equals old mean plus (new reward minus old mean) divided by play count), which avoids storing the full reward history.

## Slide 9 — Solving the n-armed bandit
The full loop: at each step pick an arm via the current strategy, observe a reward, update the running mean, repeat for many rounds. Shown as side-by-side Python code blocks.

## Slide 10 — Results
A reward-vs-episode curve showing that epsilon-greedy steadily converges toward the maximum mean reward of the best machine, with the residual gap reflecting the epsilon fraction of forced exploration.

## Slide 11 — Soft-Max Selection Policy
Contrasts epsilon-greedy with softmax (Boltzmann) selection. Softmax assigns each action a selection probability proportional to exp(Q-value), so promising-but-not-top actions are still tried regularly while truly poor actions are dropped quickly, producing smoother exploration than the all-or-nothing coin flip of epsilon-greedy.

## Slide 12 — Soft-Max Temperature
Animated illustration of the softmax temperature parameter tau. High tau flattens the distribution (heavy exploration); low tau sharpens it toward a one-hot greedy choice. The temperature is the knob that interpolates between uniform random and pure greedy behavior.

## Slide 13 — SoftMax Function
The formal softmax formula with temperature: p(a) equals exp(Q(a) / tau) divided by the sum of exp(Q(a') / tau) over all actions.

## Slide 14 — Soft-max selection
Python implementation of softmax action selection: compute the probability vector with `np.exp(Q / tau) / np.exp(Q / tau).sum()` and sample with `np.random.choice(n, p=...)`.

## Slide 15 — Softmax selection: Faster Convergence
Plots comparing epsilon-greedy and softmax learning curves on the same bandit. Softmax converges faster and reaches a higher long-run mean reward because the chance of selecting a poor arm decays continuously with its estimated value rather than staying fixed at epsilon / n.

## Slide 16 — Contextual bandits
Generalizes the bandit by adding state. Example: ad placement, where the action is which ad to serve, the reward is whether the user clicks, but the click rate now depends on the page context (a shoe ad performs better on a jewelry site than a hardware site). Contextual bandits extend MAB with an explicit state space and motivate the next stage toward MDPs.

## Slide 17 — Contextual bandit
Diagram of the contextual-bandit loop: a neural network agent reads state information (current website), chooses an ad from the action space, the ad is placed, and the user click generates a reward. The slide carries the formal definition of "state" as the set of environment information available for decision-making.

## Slide 18 — State-action pair
The action-value Q now indexes a state-action pair, not just an action. With 100 states and 10 actions, the tabular Q would have 1000 entries; with realistic state spaces this becomes infeasible, motivating a neural network to learn the mapping from state-action pairs to expected reward.

## Slide 19 — Simulation for contextual bandit
Defines a synthetic contextual-bandit environment: a random reward-probability matrix of shape (states, actions), and a uniformly random next-state transition. The randomness in next-state makes this a pure bandit per state rather than a sequential decision problem yet.

## Slide 20 — Usage
Python usage example for the contextual-bandit simulator, showing how a step returns (next_state, reward) for a chosen (state, action).

## Slide 21 — One-Hot Encoding
Quick refresher on one-hot encoding of the discrete state index into an input vector consumable by a neural network: a single 1 at the active state position, zeros elsewhere.

## Slide 22 — Linear Layer
Refresher on a fully-connected linear layer y = Wx + b, the basic building block of the neural agent that will follow.

## Slide 23 — ReLU Activation function
Refresher on ReLU, max(0, x), the standard nonlinearity placed between linear layers.

## Slide 24 — Deep Contextual bandit agent
Pulls the pieces together: a feed-forward network maps one-hot state to a vector of predicted rewards (one per action), trained to minimize squared error between predicted and observed reward. Action selection is softmax over the predicted reward vector.

## Slide 25 — Implementation
PyTorch model and training-loop code for the deep contextual-bandit agent: an `nn.Sequential` of linear and ReLU layers, an Adam optimizer, mean-squared-error loss, and the inner loop that picks an action, observes a reward, computes loss against the predicted reward, and backpropagates.

## Slide 26 — Training
The full training loop in Python: iterate over episodes, select state, predict reward vector, sample action via softmax, observe reward, compute loss, step the optimizer.

## Slide 27 — Training Progress
Mean reward versus training iteration, showing the network gradually converging toward the optimal per-state action across all states.

## Slide 28 — The Markov Property
Formalizes the Markov property: the next state and reward depend only on the current state and action, not on history. An MDP is any control task with the Markov property; this is the bridge from bandits to full RL.

## Slide 29 — Examples
Concrete examples to build intuition. Driving a car satisfies the Markov property (current positions and goal suffice); medical treatment usually does too. Stock investment does not (past performance matters); medical diagnosis (as opposed to treatment) also requires history. The point is that Markov is a modeling choice, not a universal truth.

## Slide 30 — Transition probability
Introduces the transition probability P(s' | s, a), the probability of landing in state s' after taking action a in state s. This is the third core MDP object after states and actions.

## Slide 31 — Reinforcement Learning process
The canonical RL loop diagram: the agent takes action a_t, the environment changes and produces a new state s_{t+1} and reward r_{t+1}, both fed back to the agent. The diagram is the visual anchor for every later algorithm in the module.

## Slide 32 — Policy Function
A policy pi maps states to actions (or to action distributions). It is the object the agent is ultimately optimizing.

## Slide 33 — Optimal Policy
The optimal policy pi* maximizes the expected total (cumulative discounted) reward starting from any state. Defining optimality precisely is what lets later slides talk about "learning" pi*.

## Slide 34 — Learning Optimal Policy
High-level taxonomy of how to learn pi*: directly (policy methods) or indirectly via a learned value function (value-based methods). The split previews the two algorithm families covered in the next decks.

## Slide 35 — Value Function
Defines two value functions side by side. V_pi(s) is the expected return starting in state s and following pi thereafter; Q_pi(s, a) is the expected return after taking action a in state s and then following pi. Both come with their math notation and an English gloss in a two-column table. These functions are the workhorses of all indirect (value-based) RL methods.

---

## Deck-level takeaway

The MDP lecture is the conceptual hinge of the deep-RL module. It walks the reader stepwise from the simplest decision problem (a stateless multi-armed bandit with epsilon-greedy or softmax exploration) to the full MDP formulation by gradually adding pieces: first a reward function, then exploration policies, then state (contextual bandit), then a neural-network function approximator for Q-values, and finally the Markov property and transition kernel that turn a contextual bandit into a sequential decision process. Along the way the reader writes working PyTorch code, so by slide 27 they have already trained a small deep contextual-bandit agent. The closing slides (28 through 35) install the formal vocabulary, states, actions, transitions, policy, optimal policy, V and Q value functions, that every subsequent algorithm (DQN, policy gradient, actor-critic) will assume. The pedagogical pattern is "build a working toy first, then formalize", and the punchline is that the same softmax-over-Q-values that worked for the bandit is the same object the rest of the module will scale up.
