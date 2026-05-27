# 0013_Optimization — Per-Slide Summary

**Source file:** `0013_Optimization.pptx`
**Source folder:** `SlidesPool/0010_Common_MLDL/`
**Drive link:** https://drive.google.com/file/d/11UUDw1m9nfUH8vWLorfbTRLwyR1cJCWa/view
**Slide count (exact, via python-pptx):** 11
**Extraction:** Local parse + slide PNG render. Visually inspected slides 3, 4, 5, 6, 7, 8, 10, and 11 since several bodies were short labels (Definition, Reminder, Analytically, Animation) with embedded math, derivative tables, gradient surfaces, and optimizer trajectory plots that carry the pedagogical weight.

---

## Slide 1 — Optimization
Title-only divider slide opening the deck on optimization as the engine behind ML training.

## Slide 2 — What does it mean to train a model?
The deck frames training as minimizing a differentiable loss function over the training data so that the learned parameters drive the loss, and ideally the underlying error function, to its smallest value. In some cases the loss and the error are the same function, while in others the loss is a tractable surrogate. The minimization is carried out as a numerical search rather than a closed-form solution. Concretely, gradient descent is used as the iterative method of choice. Each iteration requires evaluating the function's gradient at the current parameter point, which the authors note must be computable numerically in Python code.

## Slide 3 — Function Derivatives
The slide places the formal definition of the derivative as the limit of (f(x+h) - f(x)) / h next to a geometric interpretation drawn on a parabola. On the parabola, two tangent segments are highlighted: one on the decreasing arm labelled "negative slope" with Delta_x and Delta_f arrows showing f going down as x increases, and one on the increasing arm labelled "positive slope" with Delta_x and Delta_f going up together. The pairing teaches the reader to read a derivative simultaneously as a limit of a difference quotient and as the slope of the tangent at a point.

## Slide 4 — Multivariate function and partial derivatives
This is a reminder slide that lifts derivatives from one variable to several. The embedded panel uses the example f(x,y) = x^3 y + y^2 and computes partial_f/partial_x = 3x^2 y and partial_f/partial_y = x^3 + 2y. A footer line plugs in the point (x=2, y=2) and reports the partial derivatives as (24, 12), giving the reader a concrete numeric anchor for the abstract operator notation.

## Slide 5 — Gradients: Vector of Partial Derivatives
The gradient is introduced as the column vector whose entries are the partial derivatives partial_f/partial_x_1 through partial_f/partial_x_n, written as nabla f(p). Alongside the formula, two visualizations of f(x,y) = 4 + x^2 + y^2 - 3xy are shown: a top-down contour map with red arrows pointing along the local steepest-ascent direction, and a 3D saddle-like surface. The accompanying bullets state the geometric reading: the gradient points in the direction of steepest increase in the 2D input space, the largest increase for a fixed step size lies along the gradient, and the largest decrease for the same step lies opposite to it.

## Slide 6 — Derivative of table functions
The slide presents an analytic lookup table covering common scalar derivatives: power x^n, logarithm ln(x), trigonometric functions and their reciprocals, inverse trig, hyperbolic, and their inverses, with the matching f'(x) entries. To the right, a worked partial-derivative example shows partial(3x^2 y)/partial_x = 6yx and partial(3x^2 y)/partial_y = 3x^2, demonstrating how the entries from the table combine with the partial-derivative rules from slide 4 to handle multivariate expressions analytically.

## Slide 7 — Chain Rule for complex functions
A single boxed equation states the chain rule: d/dx [f(g(x))] = f'(g(x)) g'(x). The title underlines that this rule is the mechanism for differentiating composed expressions, which is exactly what neural network forward passes produce. This slide is the conceptual bridge from manual calculus to backpropagation, even though backpropagation itself is not yet named.

## Slide 8 — Minimizing function with Gradient Descent
Three visual panels assemble the gradient descent picture. A small contour plot marks the directions of steepest ascent and steepest descent, noting that the descent direction is the opposite of the gradient. A second panel writes the update rule w^(t+1) = w^(t) - alpha nabla f(w^(t)) and annotates each piece: position of next iteration, position of previous step, learning rate alpha, and the gradient-scaled step. The third panel is an animated 3D loss surface with a trajectory snaking from a high ridge down toward a basin, illustrating how repeated application of the rule walks the parameters downhill.

## Slide 9 — Batch Stochastic Gradient Descent
The slide contrasts full gradient descent, which optimizes against the entire loss summed over all training data, with minibatch stochastic gradient descent, which at each step selects a subset of the training data, the "batch" of size B, and computes the gradient only on that subset. The framing motivates the practical compromise behind modern deep learning: full batches are accurate but expensive, single-example updates are cheap but noisy, and minibatches trade off cost and variance.

## Slide 10 — Optimization Techniques
This slide consolidates the lesson. ML training is reframed as loss function minimization, with the caveat that the parameter space can reach 500B dimensions in large models. The recipe stays the same: iteratively run stochastic gradient descent, compute gradients of the loss at the current point, update the parameters, and hope for the best. The slide closes by acknowledging that many improvements have been layered on top of vanilla SGD, but tuning the whole stack remains an art. The inset reproduces the SGD update rule w^(t+1) = w^(t) - alpha nabla f(w^(t)) as a reminder of the core mechanism that all later improvements modify.

## Slide 11 — Moments and Learning rates
The closing slide previews the two major families of SGD enhancements. Moments remember the last update and dampen sudden direction changes, smoothing the trajectory through noisy gradients. Learning rate strategies make the step size smaller as training progresses toward the minimum, and assign a separate learning rate to each parameter. A small chart on the right plots optimizer trajectories on a contoured loss surface with a legend listing SGD, Momentum, NAG, Adagrad, Adadelta, and Rmsprop, visually contrasting how each method threads its way toward the minimum.

---

## Deck-level takeaway
The deck builds the mathematical machinery of model training from first principles: it defines derivatives, generalizes to partial derivatives and gradients, introduces the chain rule that makes composition differentiable, and assembles these pieces into the gradient descent update rule w^(t+1) = w^(t) - alpha nabla f(w^(t)). It then moves from theory to practice by replacing full-batch descent with minibatch stochastic gradient descent and previewing the moment- and learning-rate-based enhancements (Momentum, NAG, Adagrad, Adadelta, RMSprop) that real systems use.

For an LLM-focused book, this deck is the canonical "how does training actually work" foundation that sits beneath every later chapter on pretraining, fine-tuning, and optimization tricks. Its candor that training at 500B parameters remains "still an art" sets up the reader to expect engineering nuance, not pure mathematics, in the chapters on optimizer selection, scheduling, and large-scale training stability.
