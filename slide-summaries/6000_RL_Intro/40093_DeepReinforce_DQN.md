# 40093_DeepReinforce_DQN — Per-Slide Summary

**Source file:** `40093_DeepReinforce_DQN.pptx`
**Source folder:** `SlidesPool/6000_RL_Intro/`
**Drive link:** https://drive.google.com/file/d/1Z1PHn94ED4i4kkox0q6CCQ3m-UGHTfnt/view
**Slide count (exact, via python-pptx):** 35
**Extraction:** Local parse + slide PNG render. Roughly half of the slides carry math, PyTorch code, or Gridworld board renderings as embedded images, so the slide PNGs were inspected visually to reconstruct the content for image-heavy slides.

---

## Slide 1 — Deep reinforcement learning
Divider for the "Deep Q-networks" lecture.

## Slide 2 — Gridwall engine
Introduces the running example: a 4x4 Gridworld populated with an Agent (A), a Wall (W), a Pit (minus), and a Goal (plus). The objective is to navigate the agent from start to goal while avoiding the pit. The board is the toy environment used throughout the deck to make Q-learning concrete.

## Slide 3 — Weighted Accumulated Rewards
Generalizes the value of a state to a weighted sum of future rewards: V_pi(s) equals the sum over t of w_i R_i. Differing weight schedules give more or less importance to recent rewards, motivating the next slide's discount factor.

## Slide 4 — Q-learning
States the Q-learning principle in four bullets: learn the action-value Q-function, predict the value of every state-action pair, compare predictions with observed accumulated rewards, and update parameters by reducing that gap. This is the prediction-then-correction loop that drives DQN.

## Slide 5 — Code
Compact Python sketch of the bare Q-learning update inside an episode loop, intended as a first scaffold to be elaborated in later slides.

## Slide 6 — Gridworld
Specifies the Gridworld state representation: a 4 by 4 by 4 tensor where the first dimension indexes the four object types (agent, wall, pit, goal), each plane carries a binary occupancy map of that object on the 4 by 4 board. Flattened, this gives a 64-dimensional binary input to the network.

## Slide 7 — Learning Process
Two side-by-side diagrams showing the inner Q-learning loop: select an action via epsilon-greedy on the predicted Q-vector, take the action, observe the reward and next state, then update the Q-network from the temporal-difference error.

## Slide 8 — Update Rule
Writes the temporal-difference update rule: Q(s, a) is moved toward r + gamma max_{a'} Q(s', a') with step size alpha. Bullets call out the two hyperparameters that appear: the learning rate alpha and the discount factor gamma.

## Slide 9 — Hyperparameters
Defines hyperparameters as values that shape learning but are not themselves learned. Focuses on the discount factor: gamma less than 1 makes the agent prefer near-term rewards, while gamma equal to 1 treats all future rewards equally, with a small numerical example.

## Slide 10 — Sparse Signaling
Explains the sparse-reward pathology in episodic games such as chess where reward arrives only at win or loss. The Gridworld design dodges this by giving plus 10 for reaching the goal, minus 10 for the pit, and minus 1 per move to penalize dawdling, producing a dense signal that Q-learning can latch onto.

## Slide 11 — Building the network
Contrasts two Q-network designs. The original Q(s, a) takes a state and an action and returns one scalar, requiring a forward pass per action. DeepMind's modification Q_A(s) takes only the state and returns the full vector of Q-values, one per action, which is far cheaper when the action space is small and discrete.

## Slide 12 — Epsilon-greed strategy
Re-states epsilon-greedy action selection on top of the predicted Q-vector: take argmax with probability 1 minus epsilon, otherwise sample uniformly.

## Slide 13 — Gridworld game engine
Five-panel snippet showing how the Gridworld engine encodes the board. Each of the four 4 by 4 planes is a separate one-hot grid for one object class, and the example walks through the placement of A, W, minus, and plus on the same board.

## Slide 14 — Neural Network as Q function
Architecture diagram: the 64-dimensional flattened state vector passes through a small MLP and emerges as a length-4 Q-value vector, one entry per movement action (up, down, left, right).

## Slide 15 — PyTorch
PyTorch model and loss snippet: `nn.Sequential(Linear, ReLU, Linear, ReLU, Linear)` for Q, plus the MSE loss between the predicted Q-value for the chosen action and the TD target.

## Slide 16 — Training Process
Pseudocode for the per-game training loop: initialize state, while the game is in progress run the Q-net for predicted rewards, choose epsilon-greedy action, run the Q-net on the next state for max Q', compute the TD target and loss, and update.

## Slide 17 — Adding Noise
Diagnostic detail. Because the input state is mostly zeros, most weights in the first linear layer receive no gradient (only the bias does) and ReLU activations stay near zero. The patch is to add a small noise vector to the input to keep gradients flowing.

## Slide 18 — (Annotated training code)
Annotated full training loop in PyTorch with margin call-outs pointing at the key lines: epsilon-greedy action selection, the forward pass on s and s', the construction of the target r + gamma max Q(s'), and the gradient step. The annotations explain each block of the bare training loop.

## Slide 19 — Loss Plot
Loss-versus-training-step plot for the basic DQN, showing convergence but with high variance episode to episode.

## Slide 20 — Testing the model
Defines two test modes for the trained agent: static (always the same initial board) and random (each game starts from a fresh layout). The static case is what the training in the previous slides actually optimized.

## Slide 21 — Game run
Step-by-step rendered Gridworld frames from a successful agent run, showing the agent walking from start to goal under the trained policy.

## Slide 22 — Random initial condition
Demonstrates the failure mode: when the initial board is randomized, the agent fails. The conclusion noted on the slide is that the network has memorized the solution for one particular layout rather than learning a general policy.

## Slide 23 — Training on random state does not work
Loss curve from training on randomized initial states without any countermeasures. The loss does not decrease meaningfully, motivating the next two fixes (experience replay and the target network).

## Slide 24 — Catastrophic forgetting
Names the underlying cause. Successive games provide near-identical states with different optimal actions, so each gradient step partially undoes the previous one and the network never settles.

## Slide 25 — Experience Replay
Introduces experience replay: store each (state, action, reward, next_state) transition in a buffer, then train on random mini-batches sampled from the buffer rather than on the most recent step. This breaks the temporal correlation that caused catastrophic forgetting.

## Slide 26 — Experience Replay
Shows the resulting batch: each batch element is a transition from a different game with a different initial state, restoring the i.i.d.-like training conditions that standard supervised learning assumes.

## Slide 27 — (Experience replay implementation)
PyTorch implementation of experience replay using Python's `collections.deque` as a fixed-capacity FIFO buffer, plus the corresponding modifications to the training loop: append the transition every step, sample a random mini-batch of fixed size, stack tensors with `torch.gather` to pull the Q-value of the action actually taken, and only call `loss.backward()` once enough transitions are in the buffer.

## Slide 28 — DQN with experience replay
Loss-versus-training-step plot after adding experience replay. The curve is markedly smoother and converges to a lower plateau than the no-replay run.

## Slide 29 — Overfitting
Argues that experience replay alone is still insufficient. The agent can still overfit to the limited state distribution it has seen, and a deeper instability remains: the same network produces both the current prediction Q(s, a) and the target r + gamma max Q(s', a'), so any weight update shifts the target, making the regression chase a moving objective.

## Slide 30 — Target network
Introduces the target network. Keep two copies of the Q-network: Q (online, updated every step) and Q-hat (target, used only to compute r + gamma max Q-hat(s', a')). The diagram shows that Q-hat is periodically synced from Q rather than trained directly, so the target stays stationary across many updates.

## Slide 31 — Training Procedure
Updated end-to-end pseudocode with both fixes: experience replay buffer plus a target network synced every N steps. Every other line is the same as basic DQN; only the target computation switches from Q to Q-hat and a sync block is added.

## Slide 32 — Target Network
PyTorch code for the target network. Build the main `model` with `nn.Sequential`, then make `model2 = copy.deepcopy(model)` and `model2.load_state_dict(model.state_dict())`. Define `sync_freq = 50`: every 50 training steps, copy parameters from `model` into `model2`.

## Slide 33 — (Full DQN training loop)
The full training loop with both improvements wired in. The annotations highlight the sync step, the batch-sampling block, the use of `model2` for the target Q-values, and the use of `model` for the predicted Q-values.

## Slide 34 — DQN loss plot with experience replay and target network
Final loss plot: with both experience replay and a target network, the loss curve is smooth and monotonically decreasing, and the trained agent generalizes across randomized Gridworld initial states.

## Slide 35 — Training on larger boards
Closing experiment: the same DQN architecture is trained on a larger Gridworld. Performance scales but training time and data requirements grow, foreshadowing the need for the policy-gradient and actor-critic methods covered in the next decks.

---

## Deck-level takeaway

The DQN deck is the practical follow-up to the MDP lecture: the reader builds a working deep Q-network on Gridworld, then debugs the two failure modes that nearly all DQN papers attack. The first half (slides 1 through 21) constructs a baseline DQN, a 64-dimensional one-hot state, an MLP that outputs a 4-vector of Q-values, epsilon-greedy action selection, and an MSE loss against the temporal-difference target, and shows it solving Gridworld from a fixed start position. The second half (slides 22 through 35) demonstrates that the baseline fails on randomized starts because of catastrophic forgetting and target-chasing, then installs the two canonical DeepMind fixes: experience replay (mini-batches sampled from a deque buffer to decorrelate updates) and a periodically synced target network (a slow-moving copy of Q used only to compute the TD target). After both fixes the loss curve is smooth and the agent generalizes. The pedagogical signature is debugging-by-failure: every algorithmic addition is motivated by a concrete loss plot that does not converge.
