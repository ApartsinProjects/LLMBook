# 40005_DeepReinforce_ActorCritic — Per-Slide Summary

**Source file:** `40005_DeepReinforce_ActorCritic.pptx`
**Source folder:** `SlidesPool/6000_RL_Intro/`
**Drive link:** https://drive.google.com/file/d/1_Z_MTaTdgM1fH-PrMJBwnEx_HPOtqYzB/view
**Slide count (exact, via python-pptx):** 24
**Extraction:** Local parse + slide PNG render. The architecture diagrams and multiprocessing PyTorch listings live in embedded images, so slide PNGs were inspected to recover the content of image-only slides.

---

## Slide 1 — DLR
Divider for the "5. Actor-Critic" lecture.

## Slide 2 — Introduction
Side-by-side recap of the two previous algorithms. DQN works on discrete action spaces, predicts a Q-value per action, and uses a separate epsilon-greedy policy during training. REINFORCE is episodic (only updates after a complete episode finishes), predicts an action probability distribution directly, and samples actions from it during training. Each has a weakness, motivating the hybrid that follows.

## Slide 3 — Policy Function
Restates the policy-gradient loss from the previous deck: minimize -log pi(a | s) weighted by the future discounted return R from the episode. The three embedded images show the formula, the trajectory recording, and the per-step weighting that will be modified in the Actor-Critic loss.

## Slide 4 — Online learning
Diagnoses the trade-off. DQN supports per-step (online) updates, but it needs an experience replay buffer to be stable because a single update can swing the predicted Q wildly. REINFORCE is naturally on-policy and low-variance per episode but episodic, so it cannot update mid-episode. The lecture's target is DA2C (Distributed Advantage Actor-Critic), a policy-gradient method that supports online updates without a replay buffer.

## Slide 5 — Combine Value and Policy Function
Articulates the fix. DQN learns a value (expected reward) and uses it for action selection; policy gradient learns actions directly and reinforces them. Combining the two starts from a policy learner and adds a value learner whose job is to reduce the variance of the reward signal used to update the policy, increasing sample efficiency.

## Slide 6 — Combine value/policy learners
Writes the Actor-Critic loss explicitly: Loss = -log(pi(a | s)) times (R - V_pi(s)). R is the observed return; V_pi(s) is the value predicted by the critic. The difference R - V_pi(s) is the advantage, intuitively, how much better the action turned out than the critic expected. The two networks (actor and critic) are trained simultaneously.

## Slide 7 — Actor-Critic
Architectural diagram showing the actor network (state to action distribution) and the critic network (state to scalar value V), with the advantage signal flowing from the critic into the actor's gradient.

## Slide 8 — Actor-Critic Models
Full per-step Actor-Critic loop diagram. State s_t feeds the actor, the actor samples action a_t, the environment produces state s_{t+1} and reward r_{t+1}, the critic predicts the advantage of s_{t+1}, and the advantage is fed back to reinforce the action that was just taken. State s_t is also fed to the critic for training the value head.

## Slide 9 — Distributed Learning
Introduces the "distributed" half of DA2C. Spawn many worker processes, each running its own copy of the model on its own environment, then average the gradients across workers to update the central model. This decorrelates samples across workers and dramatically broadens the on-policy data the model sees per update.

## Slide 10 — Multiprocesisng
Conceptual diagram of the distributed setup: multiple workers, each with environment + model + collect + gradient, connected to a shared parameter store.

## Slide 11 — Multiprocessing
Python diagram showing the `torch.multiprocessing` model with shared CUDA tensors and gradient queues.

## Slide 12 — Manual multiprocessing
Code snippets implementing distributed Actor-Critic by hand: `mp.Process` workers, `Queue` for gradient exchange, and a master that periodically averages and broadcasts parameters.

## Slide 13 — Online advantage action-critic
Per-step Actor-Critic pseudocode in Python. Per epoch: state = environment.get_state(); value = critic(state); policy = actor(state); action = policy.sample(); next_state, reward = environment.take_action(action); value_next = critic(next_state); advantage = reward + (gamma * value_next - value); loss = -1 * policy.logprob(action) * advantage; minimize(loss). The advantage is the one-step temporal-difference signal r + gamma * V(s') - V(s), which is what makes this online.

## Slide 14 — Actor-Critic
Re-displays the actor-critic data-flow diagram, now annotated with where each piece of the per-step loss comes from.

## Slide 15 — Cart Pole
Switches back to CartPole as the running environment, with two screenshots of the rendered task.

## Slide 16 — Model
PyTorch model definition: a shared trunk (a couple of linear layers) that branches into an actor head (softmax over 2 actions) and a critic head (scalar value).

## Slide 17 — Model
Second model panel showing the `forward` method that returns `(policy_logits, value)` for the trunk-and-two-heads architecture.

## Slide 18 — Distributing the training
Code for the distributed training setup with `torch.multiprocessing`, showing the master spawning worker processes and the workers receiving a shared `model` reference.

## Slide 19 — Worker Function
The per-worker function: take the shared model and an environment copy, run episodes locally, compute the actor-critic loss, and call `loss.backward()` against the shared parameters (Hogwild-style asynchronous updates).

## Slide 20 — Running an episode
Per-episode rollout code in the worker: reset the environment, loop until done collecting (state, action, reward, value, log_prob) tuples needed for the actor-critic loss.

## Slide 21 — Running an episode
Continuation of the rollout: after collecting the trajectory the worker computes the discounted return G backward through the trajectory, used as the bootstrap target for the critic.

## Slide 22 — Update parameters
Loss assembly and parameter update on the worker side: policy loss as -log_prob * (G - value).detach(), value loss as MSE between value and G, and the combined gradient step that updates both heads of the shared model.

## Slide 23 — Training Evaluation
Episode-length-versus-training-step plot for the distributed Actor-Critic on CartPole, showing convergence to the 200-step cap, with comparison to the single-worker baseline that converges more slowly.

## Slide 24 — N-step actor-critic
Closing variant: the N-step Actor-Critic, intermediate between pure online (1-step) and full episodic (REINFORCE). The `run_episode(worker_env, worker_model, N_steps=10)` function runs up to N steps or until the episode ends, then uses the critic's value estimate at the cutoff as the bootstrap return G. This trades a small amount of bias (because G is bootstrapped) for a large reduction in variance, and is the standard form in modern implementations.

---

## Deck-level takeaway

Actor-Critic is the synthesis of the two previous algorithms: keep REINFORCE's policy network (the actor) but add DQN's value network (the critic) to provide a low-variance baseline. The single equation that makes everything work is the advantage A = R - V(s), or in the online form r + gamma * V(s') - V(s); subtracting the critic's expectation from the observed return removes most of the variance from the policy-gradient signal while leaving its expectation unchanged. The deck then scales this idea two ways: time (n-step actor-critic interpolates between purely online TD updates and purely episodic Monte Carlo returns) and parallelism (DA2C, the distributed version, runs many workers asynchronously updating shared weights, decorrelating samples without a replay buffer). The pedagogical signature is "take the best part of each prior method and glue them together": the actor reuses the REINFORCE log-probability loss, the critic reuses the DQN value-regression loss, and the only new piece is the advantage that connects them.
