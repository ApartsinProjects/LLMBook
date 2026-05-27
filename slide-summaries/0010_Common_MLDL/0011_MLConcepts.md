# 0011_MLConcepts — Per-Slide Summary

**Source file:** `0011_MLConcepts.pptx`
**Source folder:** `SlidesPool/0010_Common_MLDL/`
**Drive link:** https://drive.google.com/file/d/1svfcR4EZo-zLjZhoQ_AmWgCJQPW4T1b0/view
**Slide count (exact, via python-pptx):** 14
**Extraction:** Local parse + slide PNG render. Six slides were visually inspected because their parsed bodies omitted the embedded diagrams, equations, and quote images that carry the conceptual payload.

---

## Slide 1 — AI Concepts
Title-only divider slide that opens the deck on a black background, announcing the section on foundational AI and machine learning concepts.

## Slide 2 — Machine learning vs. conventional computing
This slide contrasts two computing paradigms with a side-by-side diagram. The top track, labeled "Traditional modeling," shows a Prediction phase where Data and a Handcrafted model feed a Computer to produce a Result. The bottom track, labeled "Machine Learning," splits into two phases: a Learning phase in which Sample Data and Expected Result feed a Computer that emits a Model, and a Prediction phase in which New Data and the learned Model feed a Computer to produce a Result. The visual encodes the central reframing of ML: instead of humans authoring the rules, the computer derives the model from samples and only later applies it to new inputs.

## Slide 3 — Random process and sample
The slide introduces the vocabulary that underpins ML by anchoring it in probability. A random process (or its model) generates samples and outcomes. Two contrasting examples are given to broaden the intuition: a "real" random process such as a coin toss, and a "lack of knowledge" random process such as the price of a house given its size and location, where the randomness is epistemic rather than physical. This framing prepares the reader to treat ML problems as stochastic regardless of whether the underlying mechanism is truly random.

## Slide 4 — Theories for random processes
Building on the prior slide, this one positions two classical disciplines that study random processes from opposite directions. Probability theory starts from a stochastic model and predicts outcomes. Statistics theory starts from observed samples and describes properties of the underlying process. The pairing sets up machine learning as a third, related discipline introduced on the next slide.

## Slide 5 — Machine Learning
The deck now defines machine learning in the same idiom as probability and statistics: given samples and outcomes from a random process, machine learning aims to predict new observations or to infer unobservable properties from those samples. The compact formulation deliberately frames ML as the inferential cousin of statistics, with a stronger emphasis on prediction rather than description.

## Slide 6 — ML models are parametrized functions
The slide unifies very different ML models under a single abstraction: every model is a parametrized function f(x, theta), where x is the input and theta is the vector of parameters. Three visual anchors surround this central box. On the left, a labeled linear regression equation Y_i = beta_0 + beta_1 X_i illustrates a model with just two parameters, with arrows annotating constant/intercept, slope/coefficient, dependent variable, and independent variable. On the right, the Transformer architecture diagram from "Attention Is All You Need" stands for GPT-3 with 175 billion parameters. A small photo of George E. P. Box carries the quote "All models are wrong, but some are useful," reminding the reader that the parameter-count spectrum spans seven orders of magnitude while the abstraction remains the same.

## Slide 7 — Types of ML tasks
The slide enumerates the four canonical ML task types with one example each. Supervised learning trains on inputs paired with ground-truth labels, for example images tagged as dogs or cats. Unsupervised learning works on inputs without labels, for example clustering images by similarity. Reinforcement learning learns from interaction with an environment that returns rewards, for example learning to play chess. Self-supervised learning extracts labels from the unlabeled input itself, for example predicting the next word in a sentence, foreshadowing the LLM paradigm covered later in the book.

## Slide 8 — Supervised Learning Tasks
The slide splits supervised learning into regression and classification. Regression tasks produce a numeric output such as a predicted house price from size and location, and predictions can be ranked as better or worse. Classification tasks produce a categorical output such as whether a house will be sold next week, and predictions are typically judged as right or wrong. The slide closes with a useful caveat: the same application problem can often be framed either way, for example predicting a low/medium/high price band (classification) versus predicting the number of days until sale (regression).

## Slide 9 — Measuring the quality of a model
The slide defines training as choosing an error function between model prediction and ground truth, then finding parameters that minimize it. For regression it lists Mean Square Error and Mean Absolute Error, with the MSE equation shown to the right: MSE = (1/N) sum_{i=1..N} (y_i - y_hat_i)^2. For classification it lists the misclassification rate R = (1/N) sum 1(y_i != y_hat_i), and notes that when one class can be designated "positive" (for example relevant documents) one can use precision or recall. A portrait of Lord Kelvin appears alongside the quote "To measure is to know. If you can not measure it, you can not improve it," underscoring the motivating principle.

## Slide 10 — ML: training == minimize error
The slide formalizes training as multivariate optimization. The model f(x, theta) is a function of parameters and inputs, and the error function (ERF) is a function of the model parameters with the training data held fixed. The full MSE-as-a-function-of-theta is spelled out: MSE(theta) = (1/N) sum (y_i - y_hat_i)^2 = (1/N) sum (y_i - f(x_i, theta))^2, with theta highlighted in red. A red caption states "Find parameters that minimize a multivariate function," and the slide notes that for GPT-3 theta lies in R^{175B} so there is no analytical solution via finding zeros of the derivative. Small thumbnails of f(x, theta) and the linear regression equation in the corners tie the abstraction back to the concrete examples from slide 6.

## Slide 11 — Loss Function vs. Error Function
The slide introduces the distinction between the error function the practitioner cares about and the loss function the optimizer actually minimizes. The challenge is minimizing functions in a high-dimensional space, and gradient-based optimizers require the error function to be differentiable. MSE is differentiable, but the misclassification rate, shown to the right as R = (1/N) sum 1(y_i != y_hat_i) and R(theta) = (1/N) sum 1(y_i - f(x_i; theta)), is not. The loss function is therefore a differentiable proxy used during optimization; sometimes it equals the error function, and hopefully minimizing the loss is equivalent to minimizing the error.

## Slide 12 — Classification Loss Function
The slide derives the cross-entropy loss for classification through a short chain of equivalences. A classification model outputs the probability of the positive class (binary) or the probability of each class (multiclass). Maximizing the probability of the correct class is the same as maximizing the log of that probability, which is the same as minimizing its negative log, which is the same as minimizing the cross-entropy loss. The progression motivates cross-entropy as the natural differentiable surrogate for "predict the correct class."

## Slide 13 — Complex Loss Function
The slide describes situations where the loss is not a single clean term. A model might have many outputs, for instance jointly estimating a house price (regression) and the type of sale (classification). Optimization may need to balance multiple criteria, such as making an enhanced image both similar to the input and of higher quality. The loss can also include regularization, for example a penalty on large weights that would otherwise make predictions unstable because small input changes could cause large output changes.

## Slide 14 — Logistic Regression
The closing slide presents logistic regression as the canonical binary classifier. The problem is to predict the probability of the positive class, but plain linear regression does not return values in [0, 1]. The fix is to predict the log of the odds ratio (the logit) instead: log(p / (1 - p)) = beta_0 + beta_1 X, where the ratio of positive to negative class probabilities can take any real number. To recover the class probability one applies the inverse, the sigmoid function sigmoid(x) = 1 / (1 + e^{-x}), shown as the familiar S-curve mapping any real input to (0, 1). The two boxed images encode this pair: logit goes prob to ratio, sigmoid goes ratio to prob.

---

## Deck-level takeaway
This deck builds the conceptual scaffolding for the rest of the book by walking from probability and statistics into machine learning, then unifying all ML models under the single abstraction of a parametrized function f(x, theta). It introduces the four task families (supervised, unsupervised, reinforcement, self-supervised), separates supervised learning into regression and classification, and frames training as the multivariate minimization of an error function over the parameter vector theta.

The deck's most useful pedagogical move is the explicit split between error function and loss function: the quantity the practitioner cares about (such as misclassification rate) is often non-differentiable, so the optimizer instead minimizes a differentiable surrogate (such as cross-entropy), and logistic regression is given as the worked example that ties together logit, sigmoid, and the probability interpretation. The framing of GPT-3's 175B parameters next to linear regression's two parameters sets up the scaling story that the LLM chapters later expand on.
