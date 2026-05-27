# 1306_FinetuningHumanFeedback — Per-Slide Summary

**Source file:** `1306_FinetuningHumanFeedback.pptx`
**Source folder:** `SlidesPool/1300_LLM_TransformersInternals/`
**Drive link:** https://drive.google.com/file/d/1B-Vdy8qwGU9lbAZ91R5r2ZqvZwfVwDPP/view
**Slide count (exact, via python-pptx):** 35
**Extraction:** Local parse + slide PNG render. Body bullets capture the conceptual flow; code screenshots illustrate the TRL training APIs.

---

## Slide 1 — Finetuning from Human-Feedback
Title slide for the deck on aligning LLMs to human preferences.

## Slide 2 — Align model output to human preferences
Defines the alignment objective: teach the model to produce responses that match human preferences.

## Slide 3 — Preference Scoring vs. Token-based loss
Figure contrasting preference scoring on the whole response with token-level cross-entropy loss used during SFT.

## Slide 4 — Example: Helpfulness
Concrete example illustrating helpfulness as a scoring dimension that token-level loss alone cannot teach.

## Slide 5 — Human-in-the-loop LLM training
Naive setup: the LLM generates a response, human raters assign a score, and the model is updated to maximize score. This is not feasible at scale.

## Slide 6 — Replace human-in-the-loop with a trained reward model
The reward model is a regression model that receives an instruction and a response and predicts the human score. It is trained once on a manually scored dataset and then used in place of live human feedback during LLM training.

## Slide 7 — Reward Model Architecture
A pretrained GPT transformer with a regression head on top, fed instruction plus response, returns a scalar reward.

## Slide 8 — Training the reward model with preference dataset
Direct scoring is subjective (is a response 4 or 5 in helpfulness?), so inter-annotator agreement is low. Humans are better at simple preferences, so the protocol samples two responses and asks humans to pick the preferred one. The resulting triples are (instruction, accepted response, rejected response).

## Slide 9 — Example: Preference dataset
A figure showing a row of a preference dataset with an instruction and the chosen and rejected responses.

## Slide 10 — Training a reward model with triples
Contrastive training: pass both response options through the reward model, compute their scores, and use a contrastive loss that drives the accepted score above the rejected score. The reward model receives input plus response, returns a scalar, is frequently initialized from the target model's weights, and is fine-tuned on preference datasets.

## Slide 11 — Stacking Multiple Reward Models
Multiple reward models can be stacked to fine-tune different aspects of human preferences (helpfulness, harmlessness, conciseness, etc.).

## Slide 12 — Overall finetuning process
Given a reward model "oracle" for each generation, the open question becomes how to train the LLM against it; this motivates the PPO section.

## Slide 13 — PPO
Section divider for Proximal Policy Optimization.

## Slide 14 — Reinforcement Learning from Human Feedback
RLHF formalizes the problem as RL with a delayed reward at sequence level rather than per-token. PPO updates the policy (token-prediction model) only slightly per sequence to stay close to the original. Challenges include how to backpropagate using the sequence-level oracle and how to keep the generated text high-quality.

## Slide 15 — Value Function Head
Adds a regression value head (VH) parallel to the classification head (CH) on each context vector. The value head predicts the expected reward of the entire sequence from a single context vector, trained jointly with the LLM backbone.

## Slide 16 — Definition: "Advantage" value
The advantage is the difference between the actual reward and the predicted reward. Discounted advantage weights tokens by position (first response tokens have less effect). GAE (Generalized Advantage Estimation) assumes that reward is also computed per token. Advantages are used to propagate the gradient to the underlying model.

## Slide 17 — Value Loss
Diagram showing how the value head's predictions are compared with the reward model's score: the LLM produces a prompt-response, the reward head and the value head both score it, and a value loss propagates through all reward heads once the sequence is done.

## Slide 18 — Simple Policy Loss
Without proximity, the policy loss is the log-likelihood of the correct token scaled by the (constant, no-gradient) advantage, summed over tokens.

## Slide 19 — Proximity
If only the reward model is used, the LLM may learn to hack it (high reward for gibberish). To prevent this, the overall policy is forced to change incrementally and a frozen reference model is kept; updates must not change the response too much.

## Slide 20 — Reference Model
The reference model is a (mostly) frozen copy of the original. Change is measured relative to this reference, with the loss defined by a ratio of probabilities.

## Slide 21 — Clipping ratio
PPO clips the proximity ratio to bound the magnitude of policy updates per step, yielding the canonical clipped policy loss.

## Slide 22 — KL Penalty
A KL penalty further discourages the new model from drifting too far from the reference. Unlike the ratio (one number), KL compares full next-token distributions; it is added as a regularization term to the reward.

## Slide 23 — PPO combined
A diagram showing the combined PPO objective: clipped policy loss, value loss, and KL penalty against the reference model.

## Slide 24 — DPO: Direct Policy Optimization
Section divider for Direct Preference Optimization.

## Slide 25 — DPO vs PPO
PPO first trains a reward model to provide feedback, then applies RL through PPO. DPO skips the reward model and trains directly on the preference dataset, maximizing the probability of the preferred response.

## Slide 26 — Computing Response Probability
A response's probability under the model is the product of softmax probabilities of its tokens from the classification heads.

## Slide 27 — Maximizing preference probability
The DPO loss maximizes the probability of the chosen response relative to the rejected response.

## Slide 28 — Reference Model
DPO also keeps a slow-changing reference model to prevent large output-probability changes. Sigmoid saturation plus log limits large updates.

## Slide 29 — DPO with reference model
Two diagrams showing how the reference enters the DPO loss as a denominator that anchors the model.

## Slide 30 — DPO Training
Section divider for the DPO training section that follows.

## Slide 31 — Preference Dataset
A figure showing accepted / rejected pairs as the DPO training data, identical in shape to the data used for reward-model training in PPO.

## Slide 32 — DPO Trainer
Code screenshot of the TRL DPOTrainer setup that consumes the preference dataset.

## Slide 33 — RLAIF
Section divider for Reinforcement Learning from AI feedback (RLAIF).

## Slide 34 — RLAIF
RLAIF replaces human annotators with an AI judge: probabilistic sampling generates two candidate responses, and an LLM picks the preferred one, producing the preference triples at scale.

## Slide 35 — Critic Prompt
Code screenshot of a critic prompt used by the AI judge to score or rank responses.

---

## Deck-level takeaway
The deck builds the modern alignment pipeline. Reward models replace per-response human ratings with a learned scalar over (instruction, response), trained contrastively on (chosen, rejected) preference triples that humans can label more reliably than absolute scores. PPO then uses that reward model to fine-tune the LLM, with three guardrails: a value head and the advantage signal to propagate per-token gradients from a sequence-level reward, a frozen reference model with clipped probability ratios to bound update size, and a KL penalty against the reference distribution to keep generations natural. DPO is the lighter alternative, skipping the reward model entirely and optimizing the preference likelihood directly against the same reference model. RLAIF closes the loop by replacing human raters with an AI judge whose critic prompt yields preferences at scale.
