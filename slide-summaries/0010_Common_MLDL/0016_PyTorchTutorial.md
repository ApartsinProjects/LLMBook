# 0016_PyTorchTutorial — Per-Slide Summary

**Source file:** `0016_PyTorchTutorial.pptx`
**Source folder:** `SlidesPool/0010_Common_MLDL/`
**Drive link:** https://drive.google.com/file/d/1tCLwygkMOZZekP6qZ0kfZFhH3SY5cgGz/view
**Slide count (exact, via python-pptx):** 96
**Extraction:** Local parse + slide PNG render. Roughly 30 PNGs were visually inspected because the deck is dominated by code screenshots (often the only content on the slide) and small caption-heavy diagrams pulled from Raschka's "Build a Large Language Model (From Scratch)".

---

## Slide 1 — PyTorch
Title slide introducing the deck "PyTorch: Basic Concepts" used as the foundational tools chapter of the course.

## Slide 2 — PyTorch
Frames PyTorch as the most widely used open-source Python deep learning library since 2019 and gives a Colab quickstart: open https://colab.research.google.com, switch the runtime to GPU, then verify CUDA with `import torch; torch.cuda.is_available()`. Sets the expectation that all later examples run either locally or in a free Colab GPU runtime.

## Slide 3 — PyTorch Components
Breaks PyTorch into three layers: a tensor library that extends NumPy-style array math with GPU acceleration, an autograd engine that automatically computes derivatives of tensor operations (enabling gradient descent on models), and a deep learning library that ships layers, loss functions, optimizers, and pretrained models. These three pillars structure the rest of the deck.

## Slide 4 — Tensors
Section divider opening the tensor chapter.

## Slide 5 — NumPy Arrays: Contiguous same-type data arrays
Contrasts a Python list (heterogeneous, scattered pointer-and-box memory layout) with a NumPy array (contiguous, single-dtype block of bytes) using two memory diagrams: one showing the list `[1,2,3,4,5]` with each element living at an arbitrary address, and one showing the same elements packed in a flat strided buffer with metadata (length, type, shape, strides). A second pair emphasises that Python list entries (e.g. 27.11, "Python", 27) each consume different sizes (24 / 55 / 28 bytes), whereas a NumPy array packs them as fixed 24-byte blocks. The point is that PyTorch tensors inherit the same contiguous, typed-memory model.

## Slide 6 — Understanding Tensors
Defines tensors as generalised data containers: 0D scalar, 1D vector, 2D matrix, and any higher-rank generalisation. The Raschka diagram shows a scalar (`2`), a 3-element vector, and a 3 by 4 matrix labeled as 0D, 1D, and 2D tensors.

## Slide 7 — Creating Tensors from lists
Live demo of `torch.tensor(...)` constructors: `torch.tensor(1)` builds a 0D scalar, `torch.tensor([1,2,3])` a 1D vector, `torch.tensor([[1,2],[3,4]])` a 2D matrix, and `torch.tensor([[[1,2],[3,4]],[[5,6],[7,8]]])` a 3D tensor. The annotations make explicit that tensor rank is determined by nesting depth of the Python list.

## Slide 8 — Tensor data types
Shows that PyTorch picks dtypes from the Python literal: integer list -> `torch.int64`, float list -> `torch.float32`, and a tensor can be retyped with `tensor1d.to(torch.float32)`. The three side-by-side code-and-output snippets reinforce that dtype is implicit but explicit conversion is a one-liner.

## Slide 9 — Tensor Data Types
Reference table mapping legacy PyTorch class names (`FloatTensor`, `HalfTensor`, `DoubleTensor`, `CharTensor`, `ByteTensor`, `ShortTensor`, `IntTensor`, `LongTensor`) to the modern `torch.float32 / float16 / float64 / int8 / uint8 / int16 / int32 / int64` dtype arguments. The bottom snippet shows the two equivalent constructor styles: `torch.IntTensor([1,2,3])` versus `torch.tensor([1,2,3], dtype=torch.int)`.

## Slide 10 — Tensor operations
Demonstrates the core 2D tensor API on `tensor2d = torch.tensor([[1,2,3],[4,5,6]])`: `print(tensor2d)` shows the matrix, `tensor2d.shape` returns `torch.Size([2, 3])`, `tensor2d.reshape(3, 2)` produces a 3 by 2 view, and `tensor2d.T` transposes to a 3 by 2 column-major matrix. These are the four shape and layout primitives readers will use most often.

## Slide 11 — All ones and all zeros tensors
Shows the convenience constructors `torch.zeros(2, 3)` (a 2 by 3 zero matrix) and `torch.ones(1, 4, 5)` (a 1 by 4 by 5 all-ones rank-3 tensor). Useful for parameter initialisation and masks.

## Slide 12 — Construct tensors with NumPy arrays
Bridges NumPy and PyTorch with `nparr = np.array(range(10)); pt_tensor = torch.tensor(nparr, dtype=torch.int)`. The output `tensor([0,1,...,9], dtype=torch.int32)` confirms zero-copy interop with the existing scientific Python stack.

## Slide 13 — Slicing Tensors
Walks through Python-style indexing on a 46-element `heights_tensor` of body heights: positional index `heights_tensor[2]` returns the scalar `tensor(189., dtype=torch.float64)`, negative index `[-2]` returns the second-to-last element, and slice `[-5:]` returns the last five heights as a sub-tensor. Same syntax as NumPy.

## Slide 14 — Tensor Shapes
Combines several shape utilities into one demo: `.shape` reports `torch.Size([46])`, dividing by 30.48 broadcasts a scalar (cm-to-feet conversion), `torch.cat([t1, t2], dim=0)` concatenates two 46-element vectors into a length-92 vector, and `.reshape(2, 46)` reorganises into a 2 by 46 matrix from which `[1, -2]` retrieves a single scalar. Together this is the working vocabulary for tensor layout manipulation.

## Slide 15 — Tensor broadcast similar to NumPy
Explains broadcasting with three Raschka cube diagrams: `np.arange(3) + 5` (vector plus scalar), `np.ones((3,3)) + np.arange(3)` (matrix plus row vector), and `np.arange(3).reshape((3,1)) + np.arange(3)` (column plus row producing an outer-sum matrix). The accompanying text restates the broadcasting rule that the smaller array is virtually replicated along the missing axes.

## Slide 16 — PyTorch AutoGrad
Section divider for the autograd engine.

## Slide 17 — 2D Logistic regression for binary classification
Reintroduces logistic regression as a tiny computational pipeline: inputs `x1, x2`, parameters `w1, w2, b`, net input `z = x1 w1 + x2 w2 + b`, predicted probability `y_hat = sigma(z)`, and binary cross-entropy loss `L = -(y log y_hat + (1-y) log(1-y_hat))`. This minimal model is the running example for the gradient-tracking sections that follow.

## Slide 18 — Logistic Regression(1D) in PyTorch
Codes the 1D version directly in PyTorch: import `torch.nn.functional as F`, build tensors `y, x1, w1, b`, compute `z = x1 * w1 + b`, then `a = torch.sigmoid(z)` and `loss = F.binary_cross_entropy(a, y)`. Annotations label each line as true label, input feature, weight, bias, net input, and activation+output. Demonstrates that the math of the previous slide is one-for-one with PyTorch tensor operations.

## Slide 19 — Logistic Regression as a computation graph
Visualises the same logistic-regression computation as a directed graph: trainable parameter `w1` and input data `x1` feed a multiplication node producing `u = w1 * x1`, then add `b` to get `z = u + b`, apply sigmoid for `a = sigma(z)`, and combine with target `y` to compute `loss = L(a, y)`. Each intermediate is an explicit node, which is exactly how autograd stores the trace.

## Slide 20 — Node Types
Single-image slide categorising nodes in a computation graph (leaf parameters versus intermediate computed tensors versus output loss), setting up the discussion of `requires_grad` and gradient propagation.

## Slide 21 — PyTorch AutoGrad
Bullet summary: autograd tracks every tensor operation, builds the implicit graph, and on `loss.backward()` walks that graph backwards using the chain rule to compute gradients of the loss with respect to every parameter, ready for stochastic gradient descent.

## Slide 22 — Chain Rule For Differentiation
Recalls the multivariable chain rule `dw/dt = (dw/dx)(dx/dt) + (dw/dy)(dy/dt)` for `w = w(x(t), y(t))` and overlays it on the logistic-regression computation graph from slide 19, showing where each partial derivative attaches to each edge. Sets the mathematical justification for the backward pass.

## Slide 23 — Logistic Regression as a computation graph
Same diagram as slide 19, repeated as the visual anchor for the gradient walkthrough on the next slides.

## Slide 24 — AutoGrad :: Gradient of Loss Function
Overlays partial derivatives on every edge of the logistic-regression graph (`du/dw1`, `dz/db`, `da/dz`, `dL/da`) and chains them to produce `dL/dw1 = (du/dw1)(dz/du)(da/dz)(dL/da)` and `dL/db = (dz/db)(da/dz)(dL/da)`. Sidebar notes that PyTorch sets `requires_grad=True` by default on internal graph nodes.

## Slide 25 — Computing Partial Gradients
Codes the same example, calling `torch.autograd.grad(loss, w1, retain_graph=True)` and `torch.autograd.grad(loss, b, retain_graph=True)` and printing `grad_L_w1` and `grad_L_b`, which print as `(tensor([-0.0898]),)` and `(tensor([-0.0817]),)`. Side note explains that PyTorch frees the graph after `.backward()` by default, so `retain_graph=True` is needed when calling `grad` multiple times.

## Slide 26 — Computing All Gradients
Shows the canonical one-shot gradient call: `loss.backward()` populates the `.grad` attribute on every leaf tensor (here `w1` and `b`), with `print(w1.grad)` and `print(b.grad)` yielding the same `-0.0898` and `-0.0817` values as the explicit `autograd.grad` calls.

## Slide 27 — PyTorch DL lib
Section divider opening the deep learning library chapter.

## Slide 28 — Implementing Multilayer Neural Networks
Single Raschka diagram of a fully connected feed-forward network: 10-unit input layer, two hidden layers (six and four nodes, each with an extra bias node), and a three-unit output. Annotations label edges as weighted connections and call out the explicit bias-node convention used later in the linear layer math.

## Slide 29 — Linear Layer
Defines an `n_in -> n_out` linear (dense) layer as the matrix-vector product `W x + b` and unpacks it elementwise into `w1 x1 + w2 x2 + w3 x3 + w4 x4 + b` for each output unit. The colour-coded bipartite graph and the 3 by 4 weight matrix make explicit the four-input three-output mapping.

## Slide 30 — Activation Functions
Six standard activations shown side by side with formula and curve: sigmoid `sigma(x) = 1/(1+e^-x)`, `tanh(x)`, ReLU `max(0, x)`, Leaky ReLU `max(0.1x, x)`, Maxout `max(w1^T x + b1, w2^T x + b2)`, and ELU (`x` for `x >= 0`, `alpha(e^x - 1)` for `x < 0`). Visual reference for picking nonlinearities in later layers.

## Slide 31 — Python __call__
Python interlude on the `__call__` dunder method: defining `__call__` on a class makes an instance directly callable (`e()`), which is exactly the mechanism `nn.Module` uses so that `model(X)` runs the forward pass. Sets up readers to recognise `instance(...)` syntax later.

## Slide 32 — Subclass PyTorch nn.Module
Shows the canonical PyTorch model class: subclass `nn.Module`, call `super().__init__()`, then build a `nn.Sequential` of `Linear -> ReLU -> Linear -> ReLU -> Linear` in `__init__`, and implement `forward(self, x)` that returns `self.layers(x)`. The sidebar annotations explain that input/output sizes are exposed as constructor args (`num_inputs`, `num_outputs`) so the same class generalises across datasets, and that "outputs of the last layer are called logits."

## Slide 33 — PyTorch Linear
Screenshot of the official `torch.nn.Linear` documentation block: signature `Linear(in_features, out_features, bias=True, device=None, dtype=None)`, semantics "applies an affine linear transformation `y = x A^T + b`", and parameter table (in_features, out_features, bias). Reference card for the layer used everywhere in the deck.

## Slide 34 — Create and Print Model Task: 50-dim input classification into 3 classes
Instantiates `model = NeuralNetwork(50, 3)` and prints it. The captured output reveals the full architecture: `Sequential((0) Linear(50, 30), (1) ReLU, (2) Linear(30, 20), (3) ReLU, (4) Linear(20, 3))`. Demonstrates that `print(model)` is a free, structured architecture summary.

## Slide 35 — Python List Comprehension
Python interlude showing list comprehension as the Pythonic way to build a derived list: `[x*x for x in range(2, 9, 2)]` yields `[4, 16, 36, 64]`. Used later to filter or transform dataset samples.

## Slide 36 — Generator Expression
Compares list comprehension (eagerly materialises the full list) with generator expressions in parentheses (`(x*x for x in ...)`) that produce a lazy iterator, which matters for memory when iterating over large datasets.

## Slide 37 — Trainable Parameters
Counts model parameters with `sum(p.numel() for p in model.parameters() if p.requires_grad)`, prints "Total number of trainable model parameters: 2213" for the 50-30-20-3 model, and inspects internal tensors with `model.layers[0].weight`, `model.layers[0].bias`, and `model.layers[0].weight.shape` returning `torch.Size([30, 50])`. The cluster of code-output pairs gives readers a checklist for introspecting any PyTorch model.

## Slide 38 — Random Weight Initialization
Calls `torch.manual_seed(123)` before constructing `NeuralNetwork(50, 3)` and prints `model.layers[0].weight`, which contains small symmetric random numbers (values roughly in [-0.14, +0.14]). Reinforces that default linear-layer init draws from a small uniform/normal distribution and that seeding produces reproducible weights.

## Slide 39 — Python: Objects used as functions
Recap of `__call__` from slide 31, presented again right before invoking the model as `model(X)`. Reminds the reader that the seemingly magical syntax is just instance-as-function dispatch.

## Slide 40 — Model forward pass
Runs `X = torch.rand((1, 50)); out = model(X); print(out)` which returns `tensor([[-0.1262, 0.1080, -0.1792]], grad_fn=<AddmmBackward0>)`. The slide unpacks `grad_fn`: `AddmmBackward0` records that the last op was an `Addmm` (add + matrix-multiply), which is the entry point PyTorch will walk during backprop. Side label notes the input is a single example, i.e. batch size 1.

## Slide 41 — Python Context Managers
Python interlude on `with ... as ...` blocks: the canonical `with open("hello.txt", "w") as file: file.write(...)` (auto-close on scope exit) and a custom `ToyExample` class defining `__enter__`, `__exit__`, and `__init__` to wrap arbitrary code with enter/exit logic. Foundation for the `torch.no_grad()` context shown next.

## Slide 42 — Computation without gradients
Explains that tracking gradients costs memory (intermediate activations stay alive) and compute, and is wasteful at inference. The fix is the `torch.no_grad()` context manager: `with torch.no_grad(): out = model(X); print(out)` returns the same `tensor([[-0.1262, 0.1080, -0.1792]])` but without `grad_fn`, i.e. without taping the operations.

## Slide 43 — SoftMax
Illustrates softmax as the transform from raw logits to a probability distribution: input vector `[1.3, 5.1, 2.2, 0.7, 1.1]` becomes `[0.02, 0.90, 0.05, 0.01, 0.02]` via `softmax_i = e^{z_i} / sum_j e^{z_j}`. Sets up why the output layer is left as logits and softmax is applied separately.

## Slide 44 — Last layer activation
Reinforces a key PyTorch idiom: models return raw logits, and `torch.softmax(model(X), dim=1)` is applied at evaluation only. Output `tensor([[0.3113, 0.3934, 0.2952]])` shows the three class probabilities for the 50-dim toy input. Numerically stable training (cross-entropy on logits) is the reason.

## Slide 45 — PyTorch Data Loaders
Section divider opening the data-loading chapter.

## Slide 46 — Datasets and Data Loaders
Outlines PyTorch's two-class data pipeline: a custom `Dataset` subclass that owns the on-disk format and per-sample loading, and a `DataLoader` that wraps a Dataset to provide shuffling, batching, and parallel prefetch. The same abstraction works for tiny in-memory toy data and for terabyte image datasets.

## Slide 47 — Datasets and Dataloaders
Raschka block diagram of the same pipeline: a custom `Dataset` class is instantiated into separate training and test `Dataset` objects, each fed to its own `DataLoader` instance; the DataLoader handles shuffling, batching, and "more" downstream. Annotations describe responsibility boundaries between the two classes.

## Slide 48 — Toy Dataset Class (Binary Classification)
Defines a tiny in-memory binary classification problem: `X_train` is a 5 by 2 tensor of feature vectors `[[-1.2, 3.1], [-0.9, 2.9], [-0.5, 2.6], [2.3, -1.1], [2.7, -1.5]]` with labels `y_train = [0, 0, 0, 1, 1]`, plus a 2-sample `X_test / y_test`. Used as the running example for the next slides.

## Slide 49 — Python __getitem__
Python interlude: implementing `__getitem__(self, idx)` makes a class a container that supports `obj[idx]` indexing. This is the dunder the Dataset class will implement to expose per-sample access.

## Slide 50 — (Tuples in Python)
Reference card on tuples: ordered, immutable, heterogeneous, allow duplicates. Example `T = (20, 'Jessa', 35.75, [30, 60, 90])` with positional access `T[0]..T[3]`. Justifies the `(features, label)` tuple convention the Dataset returns.

## Slide 51 — Toy Dataset Class
Implements the `ToyDataset(Dataset)` subclass: `__init__` stores `self.features = X, self.labels = y`; `__getitem__(index)` returns the tuple `(self.features[index], self.labels[index])`; `__len__` returns `self.labels.shape[0]` so that `len(obj)` works. Instantiated as `train_ds = ToyDataset(X_train, y_train)` and `test_ds = ToyDataset(X_test, y_test)`. The three dunders are the entire required Dataset interface.

## Slide 52 — Creating DataLoaders (using built-in class)
Wraps the datasets in `DataLoader(dataset=train_ds, batch_size=2, shuffle=True, num_workers=0)` and `DataLoader(dataset=test_ds, batch_size=2, shuffle=False, num_workers=0)`. Annotations emphasise that shuffling is on for training but off for test, and that `num_workers` controls background prefetch processes.

## Slide 53 — (enumerate in Python)
PYnative-style reference slide on `enumerate(iterable, start=0)`: contrasts the non-Pythonic `for i in range(len(fruits)): print(i, fruits[i])` with the Pythonic `for i, fruit in enumerate(fruits): print(i, fruit)`. Sets up the canonical batch-iteration pattern.

## Slide 54 — Iterating with batches
Iterates the train loader as `for idx, (x, y) in enumerate(train_loader): print(f"Batch {idx+1}:", x, y)`. Output shows three batches from the 5-sample training set: Batch 1 contains two samples (rows `[-1.2, 3.1]`, `[-0.5, 2.6]`, labels `[0, 0]`); Batch 2 two samples; Batch 3 just one sample. The last batch being smaller motivates the next slide.

## Slide 55 — Drop last batch
Adds `drop_last=True` to the train DataLoader to skip the small trailing batch, which "can disturb training" because the per-batch statistics (gradient noise, batch-norm estimates) jump when batch size changes. Now the iterator yields only Batch 1 (two samples) and Batch 2 (two samples), discarding the 1-sample leftover.

## Slide 56 — Multiple Workers
Explains `num_workers > 0`: when reading and preparing data from disk is slow, the DataLoader spins up background processes that pre-prepare the next batches while the main process feeds the GPU. The Raschka diagram contrasts a serial pipeline (main thread blocked on disk) with a parallel one (workers staging the next batch in the background).

## Slide 57 — PyTorch Training Loop
Section divider for the training loop chapter.

## Slide 58 — Forward and Backward Pass
High-level diagram of one training iteration: data flows through the network in the forward pass producing predictions, the predictions are compared with targets to compute a loss, then the backward pass propagates gradients and the optimiser updates the network.

## Slide 59 — (Epoch in Machine Learning)
Reference visual contrasting three configurations on 1000 samples: one batch of 1000 (1 iteration/epoch), five batches of 200 (5 iterations/epoch), and ten batches of 100 (10 iterations/epoch). Defines "epoch" as one full pass over the data regardless of batch size.

## Slide 60 — Gradient accumulation
Hand-drawn diagram showing three mini-batches each producing a gradient, summed into a "Gradient Sum" used to update the model once. Bullets state PyTorch can simulate larger batches via accumulation, but the deck's running examples update parameters after each mini-batch (no accumulation).

## Slide 61 — Cross-Entropy Loss for Classification
Annotated formula slide: multi-class cross-entropy as `-sum_{j=1..M} y_j log(p(y_j))` (sum over classes) and the binary variant `-sum_{i=1..N} [y_i log(p(y_i)) + (1 - y_i) log(1 - p(y_i))]` (sum over samples), with arrows labelling the indicator variable, predicted class probability, label, and probability of the positive class.

## Slide 62 — PyTorch
Documentation screenshot of `torch.nn.functional.cross_entropy(input, target, ...)`. Crucially, the `input` parameter description "Predicted unnormalized logits" is circled to drive home that PyTorch's cross-entropy already includes the log-softmax: never call softmax before it.

## Slide 63 — Typical Training Loop
The deck's canonical end-to-end training script: seed, build `NeuralNetwork(2, 2)`, build `optimizer = torch.optim.SGD(model.parameters(), lr=0.5)`, then loop `for epoch in range(num_epochs): model.train(); for batch_idx, (features, labels) in enumerate(train_loader): logits = model(features); loss = F.cross_entropy(logits, labels); optimizer.zero_grad(); loss.backward(); optimizer.step(); print(...); model.eval()`. Annotations highlight that `zero_grad` prevents gradient accumulation and `step` applies the SGD update; sample log shows train loss falling from 0.75 to 0.00 across 3 epochs.

## Slide 64 — Making predictions
Chains the inference idiom: `model.eval()` and `with torch.no_grad(): outputs = model(X_train)` yields raw logits, `torch.set_printoptions(sci_mode=False); probas = torch.softmax(outputs, dim=1)` converts to per-class probabilities, and `predictions = torch.argmax(probas, dim=1)` collapses to a label vector `tensor([0, 0, 0, 1, 1])`. The slide also shows that `torch.argmax(outputs, dim=1)` gives the same labels directly from logits (since argmax is monotonic under softmax) and that `predictions == y_train` plus `torch.sum(...)` is the elementary accuracy computation.

## Slide 65 — Computing Prediction Accuracy
Wraps the previous pattern into `def compute_accuracy(model, dataloader): model.eval(); correct = 0; total_examples = 0; for idx, (features, labels) in enumerate(dataloader): with torch.no_grad(): logits = model(features); predictions = torch.argmax(logits, dim=1); compare = labels == predictions; correct += torch.sum(compare); total_examples += len(compare); return (correct / total_examples).item()`, then calls it on `train_loader` and `test_loader`. Sidebar notes that `.item()` returns a Python float instead of a 0D tensor.

## Slide 66 — Saving and Loading Models
Two-line save/load idiom: `torch.save(model.state_dict(), "model.pth")` writes the parameter dictionary to disk; `model = NeuralNetwork(2, 2); model.load_state_dict(torch.load("model.pth"))` rebuilds the architecture then injects the saved weights. Saving `state_dict` rather than the model object is the portable convention.

## Slide 67 — Using GPU
Section divider opening the GPU chapter.

## Slide 68 — Computation on GPU devices
Lays the ground rules: GPU operations are fast, but all operand tensors must already live in GPU memory, and the result will be there too. Demo: `print(torch.cuda.is_available())` to check, then `tensor_1 = torch.tensor([1.,2.,3.]); tensor_2 = torch.tensor([4.,5.,6.]); tensor_1 = tensor_1.to("cuda"); tensor_2 = tensor_2.to("cuda"); print(tensor_1 + tensor_2)` yields `tensor([5., 7., 9.], device='cuda:0')`.

## Slide 69 — Mixing CPU and GPU tensors
Negative example showing the classic beginner error: moving only one operand back to CPU and adding yields `RuntimeError: Expected all tensors to be on the same device, but found at least two devices, cuda:0 and cpu!`. Operators do not auto-migrate; both inputs must be on the same device.

## Slide 70 — Single GPU training
Patches the typical training loop with three additions: `device = torch.device("cuda")`, `model = model.to(device)` (moves all parameters once), and inside the batch loop `features, labels = features.to(device), labels.to(device)` (moves each batch as it's drawn). This is the minimum diff to GPU-train any of the earlier CPU scripts.

## Slide 71 — Selecting best device
Two portable one-liners: `device = torch.device("cuda" if torch.cuda.is_available() else "cpu")` covers Nvidia, and `device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")` covers Apple M-series via the Metal Performance Shaders backend.

## Slide 72 — Multiple GPU Training
Raschka diagram of data-parallel training: the model is built on CPU, copied onto GPU 1 and GPU 2; the DataLoader produces mini-batches Mb 1 and Mb 2, and each GPU receives a different mini-batch to process independently.

## Slide 73 — Multiple GPU: Gradient Sync
Continues the diagram with steps 3 and 4: each GPU computes its forward pass and produces its own logits (Logits 1, Logits 2); each GPU computes its backward pass producing Gradients 1 and Gradients 2; the gradients are synchronised across GPUs so that the weight update is identical everywhere. This is the essence of `DistributedDataParallel`.

## Slide 74 — Example: Image Classifier
Section divider for the worked image-classifier example.

## Slide 75 — Classify Small 28x28 Fashion Images
Introduces the Fashion-MNIST task with a 3 by 7 grid of grey 28 by 28 garment images and their labels (ankle boot, t-shirt, dress, pullover, sneaker, sandal, shirt, coat, trouser, bag, etc.). Ten classes.

## Slide 76 — Learning in PyTorch
Restates the four-step learning loop with a flowchart: images become PyTorch tensors (step 1), tensors feed the deep neural network (step 2), the network outputs class probabilities (step 3), and cross-entropy loss feeds back to update the network (step 4).

## Slide 77 — Preprocessing Image Data
Builds the input pipeline with torchvision: `transform = T.Compose([T.ToTensor(), T.Normalize([0.5], [0.5])])` chains pixel-to-tensor conversion and normalisation to roughly [-1, +1]; then `train_set = torchvision.datasets.FashionMNIST(root=".", train=True, download=True, transform=transform)` and the equivalent `test_set` (with `train=False`). Annotations call out what each argument controls.

## Slide 78 — Visualize Data
Sanity-check plotting block: define `text_labels = ['t-shirt', 'trouser', ..., 'ankle boot']`, then a 3 by 8 matplotlib grid `for i in range(24): ax = plt.subplot(3, 8, i+1); img = train_set[i][0]; img = img/2 + 0.5; img = img.reshape(28, 28); plt.imshow(img, cmap="binary"); plt.axis('off'); plt.title(text_labels[train_set[i][1]], fontsize=8); plt.show()`. The arrows explain de-normalisation, reshaping, and titling.

## Slide 79 — Results
Output of the previous plotting block: 3 by 7 grid of actual Fashion-MNIST images with the correct text labels above each (ankle boot, t-shirt, dress, pullover, sneaker, sandal, ...). Visual confirmation the pipeline reads images correctly.

## Slide 80 — Binary Classification
Restricts the 10-class problem to two classes (label 0 = t-shirt, label 9 = ankle boot) via list comprehensions: `binary_train_set = [x for x in train_set if x[1] in [0, 9]]` and the equivalent test set filter. Footnote reminds the reader that each `x` is an `(img, label)` tuple, so `x[1]` is the label.

## Slide 81 — Creating Batches
Wraps the filtered binary subsets in DataLoaders with `batch_size=64`, `shuffle=True` on both train and test. The annotations call out batch size, shuffling, and that both loaders are batches "for the binary set."

## Slide 82 — Dropout Layer
Explains dropout as a regularisation technique: at training time each neuron is present with probability `p` (so the network can't over-rely on any one neuron), and at test time all neurons are present but their outputs are scaled by `p`. Side-by-side network diagrams show "Standard Neural Net" (all units active) versus "After applying dropout" (random units zeroed). Practical note: switch with `model.train()` and `model.eval()`.

## Slide 83 — Binary Classifier
Defines the binary classification model with `nn.Sequential` directly: `nn.Linear(28*28, 256), nn.ReLU(), nn.Linear(256, 128), nn.ReLU(), nn.Linear(128, 32), nn.ReLU(), nn.Dropout(p=0.25), nn.Linear(32, 1), nn.Sigmoid()` then `.to(device)`. Annotations call out the device selection, the sequential container, the linear in/out sizes, ReLU placement, and that the final sigmoid yields a single probability.

## Slide 84 — Optimizer
Configures `lr = 0.001; optimizer = torch.optim.Adam(binary_model.parameters(), lr=lr); loss_fn = nn.BCELoss()`. Reminds the reader of the BCE formula `BCE = -(1/N) sum_{i=0..N} y_i log(y_hat_i) + (1 - y_i) log(1 - y_hat_i)` so the choice of loss is grounded in math.

## Slide 85 — PyTorch detach
Single code box explaining `tensor.detach()`: returns a new tensor that shares storage with the original but is removed from the computation graph (no `grad_fn`, no gradient tracking). Used in logging to keep loss values around without retaining the graph.

## Slide 86 — Train Binary Classifier
The complete training loop for the binary model: 50 epochs, iterate `binary_train_loader`, flatten `imgs = imgs.reshape(-1, 28*28).to(device)`, remap labels with `labels = torch.FloatTensor([x if x == 0 else 1 for x in labels]).reshape(-1, 1).to(device)`, forward `preds = binary_model(imgs)`, compute `loss = loss_fn(preds, labels)`, then the standard `zero_grad / backward / step`, accumulating `tloss += loss.detach()` for logging. Side notes explain that `reshape(-1, 1)` produces a `(batch, 1)` column vector for BCE and `.detach()` strips gradient tracking from logged values.

## Slide 87 — Testing Binary Classification
The matching evaluation loop: iterate `binary_test_loader`, reshape images, map labels through `(labels/9).reshape(-1, 1)` to turn `{0, 9}` into `{0, 1}`, run `preds = binary_model(imgs)`, threshold with `pred10 = torch.where(preds > 0.5, 1, 0)`, compare `correct = (pred10 == labels)`, and accumulate `results.append(correct.detach().cpu().numpy().mean())`. Final `accuracy = np.array(results).mean()` is printed as the test-set accuracy.

## Slide 88 — Split train into validation and train
Carves a held-out validation set out of the train set: `train_set, val_set = torch.utils.data.random_split(train_set, [50000, 10000])` (Fashion-MNIST train has 60000 images total). Then builds three DataLoaders (train, val, test), each with `batch_size=batch_size, shuffle=True`.

## Slide 89 — Early Stop
Implements an `EarlyStop` class with `patience=10`: tracks the best validation loss in `self.min_loss`, resets the counter when it improves, increments when it doesn't, and `stop(val_loss)` returns `True` once `self.steps >= self.patience`. Instantiated as `stopper = EarlyStop()` for use in the multi-class training loop.

## Slide 90 — Multicategory classification
Builds a 10-class classifier as `nn.Sequential(nn.Linear(28*28, 256), nn.ReLU(), nn.Linear(256, 128), nn.ReLU(), nn.Linear(128, 64), nn.ReLU(), nn.Linear(64, 10)).to(device)`. Annotations make explicit that there are ten output neurons (one per Fashion-MNIST class) and that softmax is deliberately not applied (cross-entropy expects logits).

## Slide 91 — Train Epoch
Refactors training into a reusable `train_epoch()` function: configures `optimizer = torch.optim.Adam(model.parameters(), lr=0.001)` and `loss_fn = nn.CrossEntropyLoss()`, then iterates the train_loader, flattens images, reshapes labels, runs forward / loss / zero_grad / backward / step, accumulates `tloss += loss.detach()`, and returns the average `tloss / n`. Cleaner than inlining the loop.

## Slide 92 — Validation Epoch
Matching `val_epoch()` function: iterates `val_loader`, flattens, runs the model, computes cross-entropy, accumulates `vloss += loss.detach()`, returns `vloss / n`. Notably it does not call `zero_grad / backward / step` (no parameter updates during validation) but also does not wrap in `no_grad()` in this slide; the focus is the structural parallel with training.

## Slide 93 — Training Loop
Glues everything together: `for i in range(1, 101): tloss = train_epoch(); vloss = val_epoch(); print(f"at epoch {i}, tloss is {tloss}, vloss is {vloss}"); if stopper.stop(vloss) == True: break`. Up to 100 epochs with early stopping driven by validation loss.

## Slide 94 — Example: 5 Images + predictions
Renders five test images side by side with both the ground-truth label and the predicted label using a matplotlib loop: `plt.subplot(1, 5, i+1); img = test_set[i][0]; ... plt.imshow(img, cmap="binary"); plt.title(f"{label}; {pred}")`. The annotation arrows explain reshaping for display, prediction via the trained model, and `torch.argmax` to collapse logits.

## Slide 95 — Results
Five-image qualitative result strip: ankle boot (label 9 -> pred 9), pullover (2 -> 2), trouser (1 -> 1), trouser (1 -> 1), shirt (6 -> 6). All five correct, with the text log `the label is 9; the prediction is 9` etc. confirming the visual.

## Slide 96 — Testing and Training
Wraps up with the full test-set accuracy loop on the 10-class model: iterate `test_loader`, flatten images, run `preds = model(imgs)`, collapse with `pred10 = torch.argmax(preds, dim=1)`, count `correct = (pred10 == labels)`, accumulate `results.append(correct.detach().cpu().numpy().mean())`, and average. Final printed accuracy: `the accuracy of the predictions is 0.8819665605095541`, i.e. about 88% on Fashion-MNIST with a vanilla 4-layer MLP.

---

## Deck-level takeaway
This is a hands-on, code-first PyTorch primer that follows Sebastian Raschka's "Build a Large Language Model (From Scratch)" companion material almost lock-step. It covers tensors (creation, dtypes, shape ops, broadcasting, NumPy interop), autograd (computation graphs, chain rule, `requires_grad`, `loss.backward()`, `.grad`, `torch.no_grad()`, `.detach()`), the deep-learning library (subclassing `nn.Module`, `nn.Sequential`, `nn.Linear`, activations, dropout, softmax/cross-entropy), the data pipeline (custom `Dataset` with `__getitem__` and `__len__`, `DataLoader` with batching, shuffling, `drop_last`, `num_workers`), the canonical training loop (`zero_grad / backward / step`), GPU usage (`.to(device)`, mixed-device errors, single-GPU and multi-GPU data-parallel), and model persistence (`state_dict`). Two complete worked examples (a binary t-shirt-vs-ankle-boot classifier and a 10-class Fashion-MNIST MLP with early stopping, train/val/test split, and 88% test accuracy) anchor the abstractions in runnable code.

The pedagogical pattern is consistent across all 96 slides: introduce the math or concept on one slide, embed Python language interludes (`__call__`, `__getitem__`, `__len__`, context managers, list comprehensions, generators, `enumerate`, tuples) exactly where they unlock the PyTorch idiom, then show a screenshot of the code and its printed output side by side. This makes the deck function equally well as a 90-minute live walkthrough and as a self-contained reference card for any chapter of the course that needs PyTorch as a prerequisite tool.
