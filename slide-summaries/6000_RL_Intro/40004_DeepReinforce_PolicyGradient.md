# 40004_DeepReinforce_PolicyGradient — Per-Slide Summary

**Source file:** `40004_DeepReinforce_PolicyGradient.pptx`
**Source folder:** `SlidesPool/6000_RL_Intro/`
**Drive link:** https://drive.google.com/file/d/1pE37pMnpwyDmczoWZsHDwIsB-CCFYl8g/view
**Slide count (exact, via python-pptx):** 23
**Extraction:** Local parse + slide PNG render. Several slides embed REINFORCE math and PyTorch snippets as images, so slide PNGs were inspected to recover content for image-only or formula-heavy slides.

---

## Slide 1 — Deep Reinforcement learning
Divider for the "Policy Gradient Methods" lecture.

## Slide 2 — Deep Q-network
Recaps DQN as motivation. DQN approximates the Q-function, is off-policy (uses epsilon-greedy to generate behavior but evaluates a greedy policy at test time), and treats action selection as an argmax over predicted Q-values. The slide poses the lecture's central question: can the network instead be trained to output the next action directly, as a probability distribution over actions?

## Slide 3 — A Policy Network
Introduces the policy network pi. It takes the state and returns a probability vector over actions, with no explicit Q-function in between. This is the defining architectural difference of policy gradient methods.

## Slide 4 — Stochastic Policy Gradient
Block diagram of the stochastic policy. The state vector goes into the policy module pi and a probability distribution comes out (the example shows P(action) equal to [0.5, 0, 0.25, 0.25] for four actions). The agent samples an action from that distribution at every step.

## Slide 5 — Deterministic policy
Notes a failure mode. If the environment is fully stationary, gradient descent will drive the learned policy toward a degenerate distribution that puts all mass on a single action, that is, toward a deterministic policy. This kills exploration and is undesirable in early training.

## Slide 6 — Exploration
The cure is sampling. Even when the policy distribution becomes sharp, drawing each action from `Categorical(pi(s))` instead of taking argmax preserves a small probability of off-policy moves, keeping exploration alive without an extra epsilon-greedy hack.

## Slide 7 — Defining an objective
Defines what the policy network is being trained for. The episode is encoded as the trajectory of (state, action) pairs. If the episode ends in a win, every action taken during it should be reinforced; the probability of taking those actions in similar states should go up.

## Slide 8 — Action Reinforcement
Diagrams how reinforcement reshapes the probability vector. The policy outputs [0.25, 0.25, 0.25, 0.25]; the agent samples action 4 and the episode succeeds, so action 4's probability is pushed up and the other three are deflated proportionally, with the constraint that the output still sums to 1 (because softmax). The slide also formalizes the policy probability as pi_s(a | theta), the probability of action a given state s and parameters theta.

## Slide 9 — Log Probability
Justifies working in log-probability space. Log probabilities are unbounded below (better numerical range than [0, 1]), products turn into sums (better for trajectory likelihoods), and the gradient is well-behaved. The plotted log curve shows a steep penalty for low probabilities on the true event. The conclusion: maximize pi_s(a | theta) by minimizing -log pi_s(a | theta).

## Slide 10 — Credit Assignment
Tackles the credit-assignment problem. In a winning episode the actions closer to the win are most likely responsible, so they should be reinforced more heavily than the early ones, the opposite weighting from a "future discount" applied during reward propagation. The slide states the policy-gradient solution: weight each action's log-probability gradient by its future return (the sum of discounted rewards from that step until episode end).

## Slide 11 — Policy Training for Gridworld
A first concrete policy-training rule for Gridworld: use simple credit assignment, where each action's weight is proportional to its discounted immediate reward, and minimize the weighted negative log-probability of taken actions.

## Slide 12 — OpenAI Gym
Divider slide introducing OpenAI Gym (and Gymnasium) as the environment library for the rest of the lecture.

## Slide 13 — Environments
Overview of the major Gym environment categories: classic control (CartPole, MountainCar, Acrobot), Atari, and MuJoCo, with screenshots of representative tasks.

## Slide 14 — Cart Pole
Specifies the CartPole task used as the working example. Two discrete actions (0 = move left, 1 = move right), a four-dimensional state vector (cart position, cart velocity, pole angle, pole angular velocity), reward of +1 per timestep the pole stays within 12 degrees of vertical, and the objective of maximizing total reward (equivalently, episode length).

## Slide 15 — Cart Pole Environment
Python snippets showing how to construct the CartPole environment via `gym.make`, reset it, step it with a chosen action, and read the returned (observation, reward, done, info) tuple.

## Slide 16 — REINFORCE algorithm
Divider slide introducing the canonical REINFORCE algorithm, Williams 1992, which the rest of the deck implements step by step.

## Slide 17 — Policy Network
PyTorch model definition: an `nn.Sequential` mapping the 4-dimensional CartPole state through two linear-plus-ReLU layers to a 2-logit head, followed by `softmax` to give a length-2 probability vector over actions.

## Slide 18 — Sample an action
Python snippet for stochastic action selection: pass the state through the policy, get the action probability vector, and sample via `np.random.choice(2, p=probs)` (or `torch.distributions.Categorical(probs).sample()`).

## Slide 19 — Training
Outer training loop in Python: for each episode, reset the environment, run forward with the policy until done, store the (state, action, reward) trajectory, then compute the loss and step the optimizer.

## Slide 20 — Discounted rewards
Constructs the vector of discounted future returns G_t for the recorded trajectory: walk through rewards from the end backward, accumulating with discount factor gamma, then normalize the resulting vector (subtract mean, divide by standard deviation) to reduce gradient variance.

## Slide 21 — Loss function
The REINFORCE loss in two lines of PyTorch: `def loss_fn(preds, r): return -1 * torch.sum(r * torch.log(preds))`. The function takes the array of action probabilities (for the actions actually taken) and the array of discounted rewards, computes the log probabilities, multiplies element-wise by the discounted rewards, sums, and flips the sign so that gradient descent on the loss corresponds to gradient ascent on the expected return.

## Slide 22 — Training loop
Annotated end-to-end PyTorch training loop. Per episode: build the accumulated reward vector as duration-so-far ([1, 2, 3, ..., T]), then flip and discount so rewards decay backward in time ([gamma^(T-1), ..., gamma, 1] times the per-step rewards). The flipped, discounted, normalized reward vector is multiplied by the log-probability vector to form the loss, which is backpropagated to update the policy network.

## Slide 23 — Episode duration
Final results plot: episode length (the CartPole proxy for total reward) versus training episode. The curve rises from roughly 20 timesteps at the start to the environment's 200-step cap, showing the trained REINFORCE agent reliably balancing the pole.

---

## Deck-level takeaway

The Policy Gradient deck completes the introductory deep-RL trilogy by switching from value-based (DQN) to policy-based learning. Instead of learning Q(s, a) and acting greedily, the agent directly parameterizes a stochastic policy pi(a | s; theta) as a softmax over a small neural network, samples actions from it (which automatically gives exploration), and updates theta in the direction that increases the log-probability of actions taken during high-return episodes. The mathematical engine, REINFORCE, fits in two lines of PyTorch once one accepts three small ideas: work in log-probability space, weight each step's gradient by its discounted future return (credit assignment), and normalize the return vector to keep gradient variance manageable. The CartPole experiment in the final slides shows the algorithm working from scratch with no value function, no replay buffer, and no target network, the minimal contrast with the DQN deck. The pedagogical signature is "policy methods are simpler than they look": once the reader understands log pi times discounted return, the whole algorithm is two lines.
