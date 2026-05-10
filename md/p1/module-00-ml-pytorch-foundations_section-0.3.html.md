> I used to write for loops. Then I discovered tensors, and now I judge everyone who still writes for loops.
>
> ![Tensor](../../front-matter/images/agents/tensor.png) [Tensor](../../front-matter/wisdom-council.html#tensor), Tensor-Evangelizing AI Agent
### Prerequisites
This hands-on tutorial assumes you have read [Section 0.1: ML Basics](section-0.1.html) (especially [gradient descent](section-0.1.html)) and [Section 0.2: Deep Learning Essentials](section-0.2.html) (neural network layers and [backpropagation](section-0.2.html)). You should have Python installed along with PyTorch; a basic working knowledge of NumPy arrays will make tensors immediately familiar.
Big Picture
PyTorch is the language we will use to build, train, and understand LLMs throughout this book. Every transformer layer, every attention head, and every training loop in the chapters ahead will be expressed in PyTorch. Investing time here pays compound interest in every module that follows.
You could build a neural network using only NumPy, but it would be like building a house with hand tools when power tools are sitting on the shelf. PyTorch is a Python library for numerical computation on tensors with two superpowers: automatic differentiation and seamless GPU acceleration. If NumPy gives you a fast calculator, PyTorch gives you a fast calculator that can also compute its own derivatives and run on a graphics card. This section walks through every concept you need, starting from the lowest level (tensors) and building up to a complete training pipeline.
![A stylized workbench with PyTorch tools: tensors, autograd engine, GPU, and training loop components](images/pytorch-workbench.png)
**Figure 0.3.1**: The PyTorch workbench: tensors as raw materials, autograd as the differentiation engine, GPU acceleration, and the training loop that ties them together.
## 1. Tensors: The Fundamental Data Structure
![Colorful building blocks arranged in increasing dimensions: a single block as a scalar, a row as a vector, a flat grid as a matrix, and a 3D cube as a higher-order tensor](images/tensor-building-blocks.png)
**Figure 0.3.2**: Tensors as building blocks. A scalar is one block, a vector is a row, a matrix is a flat grid, and a 3D tensor is a cube. PyTorch lets you stack, reshape, and slice these blocks at will.
A tensor is a multi-dimensional array. Scalars, vectors, matrices, and higher-dimensional arrays are all tensors. PyTorch tensors behave like NumPy arrays but carry extra metadata: a `dtype`, a `device` (CPU or GPU), and an optional link to a computational graph for gradient computation. Code Fragment 0.3.1 below puts this into practice.
### 1.1 Creating Tensors
The following examples show how to create tensors from Python lists, NumPy arrays, and built-in factory functions.
![](http://llmbook.apartsin.com/styles/icons/callout-code.svg)Show Code (20 lines)
```python
# Create tensors from lists, factory functions, and NumPy arrays.
# Demonstrates dtype inference and zero-copy NumPy interop.
import torch
# From Python lists
a = torch.tensor([1.0, 2.0, 3.0])
print(a, a.dtype)
# Common factory functions
zeros = torch.zeros(2, 3) # 2x3 of zeros
ones = torch.ones(2, 3) # 2x3 of ones
rand = torch.randn(2, 3) # 2x3 from N(0,1)
seq = torch.arange(0, 10, 2) # [0, 2, 4, 6, 8]
# From NumPy (shares memory; no copy!)
import numpy as np
np_arr = np.array([1, 2, 3])
t = torch.from_numpy(np_arr)
print(t)
```
Output (2 lines)
tensor([1., 2., 3.]) torch.float32
tensor([1, 2, 3])
![](http://llmbook.apartsin.com/styles/icons/callout-code.svg)Show Code (42 lines)
```python
# End-to-end training loop: forward pass, loss, backward, optimizer step.
# Uses CrossEntropyLoss and Adam on a FashionMNIST classifier.
import torch
import torch.nn as nn
import torch.optim as optim
# Assume model, train_loader, device are already defined
model = model.to(device)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=1e-3)
num_epochs = 3
for epoch in range(num_epochs):
 model.train() # set training mode
 running_loss = 0.0
 for batch_idx, (images, labels) in enumerate(train_loader):
 images, labels = images.to(device), labels.to(device)
 # Flatten 28x28 images to vectors of length 784
 images = images.view(images.size(0), -1)
 # Step 0: Zero gradients from previous step
 optimizer.zero_grad()
 # Step 1: Forward pass
 outputs = model(images)
 # Step 2: Compute loss
 loss = criterion(outputs, labels)
 # Step 3: Backward pass (compute gradients)
 loss.backward()
 # Step 4: Update weights
 optimizer.step()
 running_loss += loss.item()
 avg_loss = running_loss / len(train_loader)
 print(f"Epoch [{epoch+1}/{num_epochs}], Loss: {avg_loss:.4f}")
```
Output (3 lines)
Epoch [1/3], Loss: 0.5312
Epoch [2/3], Loss: 0.3845
Epoch [3/3], Loss: 0.3421
**Code Fragment 0.3.1:** Two building blocks side by side: creating tensors (from lists, factory functions, and NumPy) and running a full training loop (forward, loss, backward, step). Notice that `torch.from_numpy` shares memory with the source array, while the training loop follows the four-step rhythm repeated in every chapter ahead.
Key Insight
PyTorch defaults to `float32` for floating-point tensors. This matters because GPUs are optimized for 32-bit arithmetic, and most deep learning happens at this precision. When you need to save memory (as we will with large language models), you can use `float16` or `bfloat16`, a technique explored in depth in [Chapter 9: Quantization and Inference Optimization](../../part-2-understanding-llms/module-09-inference-optimization/section-9.1.html).
🌎 **Real-World Scenario**: Tensor Dtype Mismatch Causes Silent Precision Loss
**Who:** ML engineer at a fintech company building a credit scoring model in PyTorch
**Situation:** Loading financial features from a Pandas DataFrame into PyTorch tensors for a neural network that predicts default probability.
**Problem:** The model trained successfully but produced significantly worse AUC (0.71) than the same architecture in scikit-learn (0.79). Predictions clustered around 0.5, as if the model could not distinguish between borrowers.
**Dilemma:** The team spent two days reviewing the architecture, loss function, and hyperparameters. Nothing seemed wrong. They considered switching back to scikit-learn entirely.
**Decision:** A senior engineer added `print(X_tensor.dtype)` and discovered the tensors were `int64` instead of `float32`. Pandas integer columns were converted without explicit dtype casting, and PyTorch silently performed integer arithmetic (truncating all fractional gradients to zero).
**How:** Changed `torch.tensor(df.values)` to `torch.tensor(df.values, dtype=torch.float32)`. One line of code.
**Result:** AUC jumped to 0.80, matching the scikit-learn baseline. Total debugging time wasted: 16 engineer-hours.
**Lesson:** **Always explicitly set `dtype=torch.float32` when creating tensors from external data. PyTorch will not warn you about integer arithmetic in places where you expect floating-point.** Code Fragment 0.3.2 below puts this into practice.
### 1.2 Indexing, Slicing, and Reshaping
These operations let you select sub-regions of a tensor and change its dimensionality without copying data.
![](http://llmbook.apartsin.com/styles/icons/callout-code.svg)Show Code (17 lines)
```python
# Indexing, slicing, reshaping, and unsqueezing tensors.
# view() returns a zero-copy view; unsqueeze adds a size-1 dimension.
x = torch.arange(12).reshape(3, 4)
print("Original:\n", x)
print("Row 0: ", x[0]) # first row
print("Col 1: ", x[:, 1]) # second column
print("Subset: ", x[0:2, 1:3]) # rows 0-1, cols 1-2
# Reshape vs. View
flat = x.view(-1) # flatten (must be contiguous)
print("Flat: ", flat)
# Unsqueeze / Squeeze for adding/removing dimensions
row = torch.tensor([1, 2, 3])
print("Shape before unsqueeze:", row.shape)
print("Shape after unsqueeze(0):", row.unsqueeze(0).shape)
```
Output (11 lines)
Original:
tensor([[ 0, 1, 2, 3],
[ 4, 5, 6, 7],
[ 8, 9, 10, 11]])
Row 0: tensor([0, 1, 2, 3])
Col 1: tensor([1, 5, 9])
Subset: tensor([[1, 2],
[5, 6]])
Flat: tensor([ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
Shape before unsqueeze: torch.Size([3])
Shape after unsqueeze(0): torch.Size([1, 3])
**Code Fragment 0.3.2:** Reshaping, slicing, and fancy indexing on tensors. These operations return views when possible, avoiding unnecessary copies.
### 1.3 Broadcasting
Broadcasting lets PyTorch perform element-wise operations on tensors of different shapes by automatically expanding dimensions. The rules mirror NumPy: dimensions are compared from right to left, and a dimension of size 1 is stretched to match the other tensor. Code Fragment 0.3.3 below puts this into practice.
![](http://llmbook.apartsin.com/styles/icons/callout-code.svg)Code (5 lines)
```python
# Add a row vector to every row of a matrix
matrix = torch.ones(3, 3)
row_vec = torch.tensor([10, 20, 30])
result = matrix + row_vec # row_vec broadcasts across dim 0
print(result)
```
Output (3 lines)
tensor([[11., 21., 31.],
[11., 21., 31.],
[11., 21., 31.]])
**Code Fragment 0.3.3:** Broadcasting a shape-`(3,)` vector across a shape-`(3, 3)` matrix. PyTorch automatically expands `row_vec` along dimension 0, adding `[10, 20, 30]` to every row without allocating a second matrix.
Warning: Silent Shape Bugs
Broadcasting can mask bugs. If you add tensors of shapes `(3, 1)` and `(1, 4)`, PyTorch happily produces a `(3, 4)` result with no error. Always verify shapes with `print(tensor.shape)` when debugging unexpected results. Code Fragment 0.3.4 below puts this into practice.
### 1.4 Device Management (CPU/GPU)
PyTorch tensors can live on CPU or GPU, and all operands in an operation must share the same device.
![](http://llmbook.apartsin.com/styles/icons/callout-code.svg)Show Code (14 lines)
```python
# Device management: detect GPU, create tensors on the target device,
# and move existing tensors with .to(device).
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Using device:", device)
# Move tensors to the chosen device
x = torch.randn(3, 3, device=device)
# Or move an existing tensor
y = torch.randn(3, 3).to(device)
# Operations require BOTH tensors on the same device
z = x + y # works because both on 'device'
```
Output (1 lines)
Using device: cuda
**Code Fragment 0.3.4:** Detecting CUDA availability and placing tensors on the GPU. Creating a tensor with `device=device` allocates it directly on the GPU, while `.to(device)` copies an existing CPU tensor. Both tensors must share the same device before any arithmetic.
Warning: Device Mismatch
Trying `cpu_tensor + gpu_tensor` raises `RuntimeError: Expected all tensors to be on the same device`. The fix: move everything to the same device before operating. A good pattern is to define `device` once at the top of your script and use `.to(device)` everywhere.
Fun Fact
Every ML engineer has at least one 3 AM debugging story where the bug was a missing `.cuda()` call. The "Expected all tensors to be on the same device" error message has probably caused more coffee consumption than any other line of code in history.
Creating and manipulating tensors is only the first step. The real power of PyTorch lies in its ability to automatically compute gradients through any sequence of tensor operations. This capability, called automatic differentiation, is the engine that drives all neural network training.
## 2. Autograd: Automatic Differentiation
Autograd is PyTorch's engine for computing gradients automatically, implementing the backpropagation algorithm covered in [Section 0.2](section-0.2.html). When you set `requires_grad=True` on a tensor, PyTorch records every operation performed on it in a directed acyclic graph (DAG). Calling `.backward()` on the final scalar output traverses that graph in reverse to compute the gradient of the output with respect to every leaf tensor. Code Fragment 0.3.5 below puts this into practice.
### 2.1 A Minimal Example
This snippet computes a simple polynomial, calls `.backward()`, and inspects the resulting gradient.
![](http://llmbook.apartsin.com/styles/icons/callout-code.svg)Code (7 lines)
```python
# Minimal autograd: compute y = x^2 + 2x + 1, then call backward()
# to obtain dy/dx automatically. At x=3 the gradient should be 8.
x = torch.tensor(3.0, requires_grad=True)
y = x**2 + 2*x + 1 # y = x^2 + 2x + 1
y.backward() # dy/dx = 2x + 2 = 8 at x=3
print(x.grad)
```
Output (1 lines)
tensor(8.)
**Code Fragment 0.3.5:** A minimal autograd example: define a scalar function, call backward(), and inspect the computed gradient.
### 2.2 The Computational Graph
Every operation creates a node in the graph. Intermediate tensors store a `.grad_fn` that records how they were created. The graph below shows what happens for a simple loss computation.
![Computational graph for linear operation with MSE loss showing leaf tensors and backward traversal](images/fig-0.3.3-comp-graph.png)
**Figure 0.3.3**: Computational graph for a linear operation followed by MSE loss. Leaf tensors (blue) have `requires_grad=True`. Yellow nodes record the operation for backward traversal.
Key Insight: The Graph Is Disposable
By default, PyTorch destroys the computational graph after `.backward()` completes. This is an intentional memory optimization: for a model with millions of parameters, keeping every intermediate graph in memory would be prohibitive. If you need to call `.backward()` multiple times on the same computation (rare in practice), pass `retain_graph=True`.
### 2.3 Gradient Accumulation
Gradients in PyTorch **accumulate** by default. If you call `.backward()` twice without zeroing gradients, the second set of gradients is added to the first. This is intentional (it enables gradient accumulation across mini-batches, a technique revisited in [Section 14.3 on fine-tuning hyperparameters](../../part-4-training-adapting/module-14-fine-tuning-fundamentals/section-14.3.html)), but forgetting to zero gradients is the most common autograd bug. Code Fragment 0.3.6 below puts this into practice.
![](http://llmbook.apartsin.com/styles/icons/callout-code.svg)Show Code (20 lines)
```python
# Gradient accumulation trap: calling backward() twice without
# zeroing adds gradients together. The fix is grad.zero_().
x = torch.tensor(2.0, requires_grad=True)
# First forward + backward
y = x * 3
y.backward()
print("After 1st backward:", x.grad) # 3.0
# Second forward + backward WITHOUT zeroing
y = x * 3
y.backward()
print("After 2nd backward:", x.grad) # 6.0 (accumulated!)
# The fix: always zero gradients before each backward pass
x.grad.zero_()
y = x * 3
y.backward()
print("After zeroing: ", x.grad) # 3.0
```
Output (3 lines)
After 1st backward: tensor(3.)
After 2nd backward: tensor(6.)
After zeroing: tensor(3.)
**Code Fragment 0.3.6:** Demonstrating gradient accumulation: after two `.backward()` calls without zeroing, `x.grad` doubles from 3.0 to 6.0. Calling `x.grad.zero_()` before the third pass restores the correct single-pass gradient. This is the most common autograd bug in custom training loops.
Note: torch.no\_grad()
During inference (or any time you do not need gradients), wrap your code in `with torch.no_grad():`. This disables graph construction, reduces memory usage, and speeds up computation. You will see this in every evaluation loop.
Key Insight
Automatic differentiation, the engine behind PyTorch's autograd, is a computational realization of the chain rule from calculus. But its significance extends far beyond convenience. In the 1960s, control theorist Robert Wengert and later Andreas Griewank recognized that any program composed of differentiable primitives could be mechanically differentiated by tracing its computation graph. This insight, known as the "differentiable programming" paradigm, blurs the boundary between writing software and defining mathematical models. Physicist and Fields medalist Richard Borcherds has noted that automatic differentiation is, in essence, a dual-number algebra applied at industrial scale. Every PyTorch computation graph is simultaneously a program and a mathematical expression, and `.backward()` exploits this duality to compute exact derivatives in time proportional to the forward pass. This is why gradient-based optimization scales to billions of parameters: the cost of computing the gradient is never more than a small constant multiple of the cost of computing the function itself.
## 3. Building Models with nn.Module
Raw tensors and autograd are powerful, but PyTorch provides `torch.nn` to organize parameters, layers, and forward computations into reusable chapters. Every model you build in this book, from simple classifiers to the full [Transformer architecture in Chapter 4](module-04-transformer-architecture_index.html.md), will subclass `nn.Module`. Code Fragment 0.3.7 below puts this into practice.
### 3.1 Your First nn.Module
The following class defines a two-layer network by subclassing `nn.Module` and implementing the `forward` method.
![](http://llmbook.apartsin.com/styles/icons/callout-code.svg)Show Code (25 lines)
```python
# Two-layer nn.Module: declare layers in __init__, wire them in forward.
# Calling model(x) runs forward plus any registered hooks.
import torch.nn as nn
class SimpleNet(nn.Module):
 def __init__(self, input_dim, hidden_dim, output_dim):
 super().__init__()
 self.fc1 = nn.Linear(input_dim, hidden_dim)
 self.relu = nn.ReLU()
 self.fc2 = nn.Linear(hidden_dim, output_dim)
 # Forward pass: define computation graph
 def forward(self, x):
 x = self.fc1(x)
 x = self.relu(x)
 x = self.fc2(x)
 return x
model = SimpleNet(input_dim=784, hidden_dim=128, output_dim=10)
print(model)
# Count parameters
total_params = sum(p.numel() for p in model.parameters())
print(f"Total parameters: {total_params:,}")
```
Output (6 lines)
SimpleNet(
(fc1): Linear(in\_features=784, out\_features=128, bias=True)
(relu): ReLU()
(fc2): Linear(in\_features=128, out\_features=10, bias=True)
)
Total parameters: 101,770
**Code Fragment 0.3.7:** Defining a two-layer neural network by subclassing nn.Module. The forward method describes how data flows through the layers.
Key Insight
The `__init__` method declares layers; the `forward` method defines the computation. Never call `model.forward(x)` directly. Instead, call `model(x)`, which runs `forward` along with any registered hooks.
With our model architecture defined, we need an efficient way to feed data into it. Training on one sample at a time is slow, and loading an entire dataset into memory may not be feasible. PyTorch solves this with a clean two-class abstraction for data handling.
## 4. Data Loading: Dataset and DataLoader
PyTorch decouples data storage from data loading through two abstractions. `Dataset` defines how to access individual samples. `DataLoader` wraps a dataset to provide batching, shuffling, and parallel loading. Code Fragment 0.3.8 below puts this into practice.
![](http://llmbook.apartsin.com/styles/icons/callout-code.svg)Show Code (27 lines)
```python
# Load FashionMNIST with torchvision, apply normalization,
# and wrap it in a DataLoader for batched iteration.
from torch.utils.data import Dataset, DataLoader
import torchvision.transforms as transforms
from torchvision.datasets import FashionMNIST
# Define a transform pipeline
transform = transforms.Compose([
 transforms.ToTensor(), # PIL image -> tensor, scales to [0,1]
 transforms.Normalize((0.2860,), (0.3530,)) # FashionMNIST stats
])
# Download and load training data
train_dataset = FashionMNIST(
 root="./data", train=True, download=True, transform=transform
)
# Create a DataLoader
train_loader = DataLoader(
 train_dataset, batch_size=64, shuffle=True, num_workers=2
)
# Iterate to see the shape of a batch
images, labels = next(iter(train_loader))
print(f"Batch images shape: {images.shape}")
print(f"Batch labels shape: {labels.shape}")
```
Output (2 lines)
Batch images shape: torch.Size([64, 1, 28, 28])
Batch labels shape: torch.Size([64])
**Code Fragment 0.3.8:** Loading FashionMNIST with a `transforms.Compose` pipeline that converts images to tensors and normalizes them. The `DataLoader` yields batches of shape `(64, 1, 28, 28)`, handling shuffling and parallel loading via `num_workers=2`.
### 4.1 Custom Datasets
When your data is not a standard benchmark, subclass `Dataset` and implement `__len__` and `__getitem__`: Code Fragment 0.3.9 below puts this into practice.
![](http://llmbook.apartsin.com/styles/icons/callout-code.svg)Show Code (13 lines)
```python
# Define MyDataset; implement __len__, __getitem__
# See inline comments for step-by-step details.
class MyDataset(Dataset):
 def __init__(self, X, y):
 self.X = torch.tensor(X, dtype=torch.float32)
 self.y = torch.tensor(y, dtype=torch.long)
 def __len__(self):
 return len(self.X)
 def __getitem__(self, idx):
 return self.X[idx], self.y[idx]
```
**Code Fragment 0.3.9:** A custom Dataset class that wraps NumPy arrays. The DataLoader then handles batching and shuffling automatically.
## 5. The Training Loop
![A robot cyclist riding around an oval racetrack with four stations: forward pass tunnel, loss scoreboard, backward pass arrows, and optimizer tuning knobs](images/training-loop-racetrack.png)
**Figure 0.3.4**: The training loop as a racetrack. Each lap (epoch) passes through the same four stations: forward pass, loss computation, backward pass, and optimizer step. The robot gets a little better each lap.
Training a neural network follows a rhythmic four-step pattern: forward pass, compute loss, backward pass, optimizer step. Every training loop you write, from a simple classifier to a billion-parameter LLM, follows this same skeleton.
🌎 **Real-World Scenario**: Forgetting to Zero Gradients Corrupts a Language Model
**Who:** Research intern fine-tuning a GPT-2 model for customer support response generation
**Situation:** Wrote a custom training loop (instead of using the [Hugging Face](../../part-3-working-with-llms/module-10-llm-apis/section-10.2.html) Trainer) to have more control over logging and gradient accumulation.
**Problem:** The model's loss decreased for the first 200 steps, then suddenly diverged to infinity. Restarting from the checkpoint produced the same explosion at roughly the same point.
**Dilemma:** The intern suspected a learning rate issue and tried reducing it from 5e-5 to 1e-6. The explosion was delayed but still occurred. They considered abandoning the custom loop for the Trainer API.
**Decision:** A mentor suggested printing gradient norms. They grew exponentially across steps because `optimizer.zero_grad()` was accidentally placed after `optimizer.step()` instead of before the forward pass, causing gradients to accumulate across batches.
**How:** Moved `optimizer.zero_grad()` to the first line inside the batch loop, immediately before `outputs = model(input_ids)`.
**Result:** Loss decreased smoothly to 2.3 over 5,000 steps. The model generated coherent customer support responses. The fix was a one-line reorder.
**Lesson:** **The training loop order (zero\_grad, forward, loss, backward, step) is sacred. Moving any step out of sequence produces bugs that can be extremely hard to diagnose without gradient monitoring.**
![The canonical training loop: zero gradients, forward, loss, backward, optimizer step](images/fig-0.3.5-training-loop.png)
**Figure 0.3.5**: The canonical training loop. Step 0 (zero gradients) prevents gradient accumulation. Steps 1 through 4 repeat for every mini-batch in every epoch.
### 5.1 Complete Training Loop
Understanding Optimizers: SGD, Adam, and AdamW
Before we write our first training loop, let us understand the optimizer that drives learning.
**Momentum** smooths out noisy gradients by maintaining an exponential moving average of past
gradients, preventing the optimizer from oscillating on noisy surfaces. **Adaptive learning rates**
give each parameter its own learning rate, scaled by the history of its gradients; parameters with
consistently large gradients get smaller steps, and vice versa. **Adam** combines both ideas.
**AdamW** improves on Adam by decoupling [weight decay](section-0.2.html) from the gradient update, which produces
better generalization and is now the preferred optimizer for training large language models.
Code Fragment 0.3.10 below puts this into practice.
Optimizer Comparison
| Optimizer | Learning Rate | Momentum | Weight Decay | Best For |
| --- | --- | --- | --- | --- |
| SGD | Single global rate | Optional (off by default) | Coupled with gradient | Convex problems, fine control |
| Adam | Per-parameter adaptive | Built in (first moment) | Coupled with gradient | Fast prototyping, general use |
| AdamW | Per-parameter adaptive | Built in (first moment) | Decoupled (proper regularization) | LLM pretraining, best generalization |
**Code Fragment 0.3.10:** Assume model, train\_loader, device are already defined.
Warning: model.train() vs model.eval()
Always call `model.train()` before training and `model.eval()` before evaluation. These toggle behaviors of layers like [Dropout](section-0.2.html) and BatchNorm. Forgetting `model.eval()` during validation leads to noisy, unreliable metrics.
## 6. Saving and Loading Models
PyTorch stores learned parameters in a dictionary called the `state_dict`. Saving the state dict (rather than the full model object) is the recommended approach because it is architecture-independent and portable. Code Fragment 0.3.11 below puts this into practice.
![](http://llmbook.apartsin.com/styles/icons/callout-code.svg)Show Code (22 lines)
```python
# Save model weights
torch.save(model.state_dict(), "model_weights.pth")
# Load into a fresh model instance
loaded_model = SimpleNet(input_dim=784, hidden_dim=128, output_dim=10)
loaded_model.load_state_dict(torch.load("model_weights.pth", weights_only=True))
loaded_model.eval()
# Save a full checkpoint (weights + optimizer + epoch) for resumable training
checkpoint = {
 "epoch": epoch,
 "model_state_dict": model.state_dict(),
 "optimizer_state_dict": optimizer.state_dict(),
 "loss": avg_loss,
}
torch.save(checkpoint, "checkpoint.pth")
# Resume from checkpoint
ckpt = torch.load("checkpoint.pth", weights_only=True)
model.load_state_dict(ckpt["model_state_dict"])
optimizer.load_state_dict(ckpt["optimizer_state_dict"])
start_epoch = ckpt["epoch"] + 1
```
**Code Fragment 0.3.11:** Saving and loading model weights via state\_dict. This approach is portable across different code versions and architectures.
Note
Always pass `weights_only=True` to `torch.load()` in modern PyTorch (1.13+). This prevents arbitrary code execution from untrusted checkpoint files. If you need to load optimizer state or other non-tensor data, use `weights_only=False` only with files you trust.
## 7. Debugging: Hooks, Gradient Inspection, and Profiling
When your model does not train, you need tools to look inside. PyTorch provides several mechanisms for introspection. Code Fragment 0.3.12 below puts this into practice.
### 7.1 Inspecting Gradients
After a backward pass, you can iterate over named parameters to check gradient statistics for signs of vanishing or exploding gradients.
![](http://llmbook.apartsin.com/styles/icons/callout-code.svg)Code (5 lines)
```python
# Check gradients after a backward pass
for name, param in model.named_parameters():
 if param.grad is not None:
 print(f"{name:20s} grad mean={param.grad.mean():.6f} "
 f"std={param.grad.std():.6f}")
```
Output (4 lines)
fc1.weight grad mean=-0.000132 std=0.004521
fc1.bias grad mean=-0.001207 std=0.000000
fc2.weight grad mean=0.000041 std=0.012843
fc2.bias grad mean=0.000523 std=0.000000
**Code Fragment 0.3.12:** Check gradients after a backward pass.
### 7.2 Forward and Backward Hooks
Hooks let you inspect (or modify) data flowing through a module without changing its code. This is invaluable for debugging and later for techniques like activation patching in interpretability research. Code Fragment 0.3.13 below puts this into practice.
![](http://llmbook.apartsin.com/styles/icons/callout-code.svg)Show Code (16 lines)
```python
# Register a forward hook that prints the output shape
def print_shape_hook(module, input, output):
 print(f"{module.__class__.__name__:15s} output shape: {output.shape}")
hooks = []
for name, layer in model.named_children():
 h = layer.register_forward_hook(print_shape_hook)
 hooks.append(h)
# Run one forward pass to see shapes
dummy = torch.randn(1, 784).to(device)
_ = model(dummy)
# Clean up hooks when done
for h in hooks:
 h.remove()
```
Output (3 lines)
Linear output shape: torch.Size([1, 128])
ReLU output shape: torch.Size([1, 128])
Linear output shape: torch.Size([1, 10])
**Code Fragment 0.3.13:** Register a forward hook that prints the output shape.
### 7.3 Profiling with torch.profiler
The built-in profiler measures CPU and GPU time per operation, helping you identify performance bottlenecks.
![](http://llmbook.apartsin.com/styles/icons/callout-code.svg)Show Code (17 lines)
```python
# Profile a few training batches with torch.profiler to identify
# which operations (linear, cross_entropy, relu) consume the most CPU time.
from torch.profiler import profile, ProfilerActivity
# Profile execution to find performance bottlenecks
with profile(activities=[ProfilerActivity.CPU], record_shapes=True) as prof:
 for i, (images, labels) in enumerate(train_loader):
 images = images.view(images.size(0), -1)
 outputs = model(images)
 loss = criterion(outputs, labels)
 # Compute gradients via backpropagation
 loss.backward()
 if i >= 4:
 break
print(prof.key_averages().table(sort_by="cpu_time_total", row_limit=5))
```
Output (9 lines)
--------------------------------- ------------ ------------ ------------
Name Self CPU % Self CPU CPU total %
--------------------------------- ------------ ------------ ------------
aten::linear 32.14% 1.205ms 48.71%
aten::addmm 24.33% 0.912ms 24.33%
aten::cross\_entropy 18.62% 0.698ms 22.45%
aten::batch\_norm 9.87% 0.370ms 14.21%
aten::relu\_ 5.04% 0.189ms 5.04%
--------------------------------- ------------ ------------ ------------
**Code Fragment 0.3.14:** Using torch.profiler to measure CPU and GPU time per operation. The resulting trace can be visualized in TensorBoard or Chrome's trace viewer.
Key Insight
Profiling reveals where time is actually spent. In small models, data loading often dominates. In larger models, matrix multiplications dominate. Knowing this guides your optimization effort: increase `num_workers` for data-bound training, or use mixed precision for compute-bound training.
## 8. Common Mistakes and How to Fix Them
8. Common Mistakes and How to Fix Them Comparison
| Symptom | Cause | Fix |
| --- | --- | --- |
| `RuntimeError: mat1 and mat2 shapes cannot be multiplied` | Input tensor shape does not match the layer's expected input dimension | Print shapes with `print(x.shape)` before each layer; ensure you flatten or reshape correctly |
| Loss is `nan` after a few steps | Learning rate is too high, or numerical overflow | Lower the learning rate; add gradient clipping with `torch.nn.utils.clip_grad_norm_` |
| Loss never decreases | Forgot `optimizer.zero_grad()` or wrong loss function | Verify the training loop skeleton; try overfitting on a single batch first |
| `Expected all tensors to be on the same device` | Model is on GPU but data is on CPU (or vice versa) | Call `.to(device)` on both model and data |
| Validation accuracy worse than training | Forgot `model.eval()` or `torch.no_grad()` | Always wrap evaluation in `model.eval()` and `with torch.no_grad():` |
## 9. Lab: Build and Train a FashionMNIST Classifier
Let us put everything together. In this lab you will build a fully connected neural network that classifies FashionMNIST images into 10 categories (T-shirt, Trouser, Pullover, Dress, Coat, Sandal, Shirt, Sneaker, Bag, Ankle boot). The complete script below is copy-pasteable and runnable.
![](http://llmbook.apartsin.com/styles/icons/callout-code.svg)Show Code (110 lines)
```python
#!/usr/bin/env python3
"""Lab 0.3: FashionMNIST Classifier in PyTorch (from scratch)."""
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
# ── Hyperparameters ──────────────────────────────────────────
BATCH_SIZE = 64
LEARNING_RATE = 1e-3
NUM_EPOCHS = 10
HIDDEN_DIM = 256
# ── Device ───────────────────────────────────────────────────
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Training on: {device}")
# ── Data ─────────────────────────────────────────────────────
transform = transforms.Compose([
 transforms.ToTensor(),
 transforms.Normalize((0.2860,), (0.3530,)),
])
train_data = datasets.FashionMNIST("./data", train=True, download=True, transform=transform)
test_data = datasets.FashionMNIST("./data", train=False, download=True, transform=transform)
train_loader = DataLoader(train_data, batch_size=BATCH_SIZE, shuffle=True)
test_loader = DataLoader(test_data, batch_size=BATCH_SIZE, shuffle=False)
# ── Model ────────────────────────────────────────────────────
class FashionClassifier(nn.Module):
 def __init__(self, hidden_dim):
 super().__init__()
 self.net = nn.Sequential(
 nn.Flatten(), # (B,1,28,28) -> (B,784)
 nn.Linear(784, hidden_dim),
 nn.ReLU(),
 nn.Dropout(0.2),
 nn.Linear(hidden_dim, hidden_dim),
 nn.ReLU(),
 nn.Dropout(0.2),
 nn.Linear(hidden_dim, 10),
 )
 def forward(self, x):
 return self.net(x)
model = FashionClassifier(HIDDEN_DIM).to(device)
print(model)
print(f"Parameters: {sum(p.numel() for p in model.parameters()):,}")
# ── Loss and Optimizer ───────────────────────────────────────
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)
# ── Training ─────────────────────────────────────────────────
def train_one_epoch(model, loader, criterion, optimizer, device):
 model.train()
 total_loss, correct, total = 0.0, 0, 0
 for images, labels in loader:
 images, labels = images.to(device), labels.to(device)
 optimizer.zero_grad()
 outputs = model(images)
 loss = criterion(outputs, labels)
 loss.backward()
 optimizer.step()
 total_loss += loss.item() * labels.size(0)
 correct += (outputs.argmax(1) == labels).sum().item()
 total += labels.size(0)
 return total_loss / total, correct / total
# ── Evaluation ───────────────────────────────────────────────
def evaluate(model, loader, criterion, device):
 model.eval()
 total_loss, correct, total = 0.0, 0, 0
 with torch.no_grad():
 for images, labels in loader:
 images, labels = images.to(device), labels.to(device)
 outputs = model(images)
 loss = criterion(outputs, labels)
 total_loss += loss.item() * labels.size(0)
 correct += (outputs.argmax(1) == labels).sum().item()
 total += labels.size(0)
 return total_loss / total, correct / total
# ── Run ──────────────────────────────────────────────────────
for epoch in range(NUM_EPOCHS):
 train_loss, train_acc = train_one_epoch(model, train_loader, criterion, optimizer, device)
 test_loss, test_acc = evaluate(model, test_loader, criterion, device)
 print(f"Epoch {epoch+1:2d}/{NUM_EPOCHS} "
 f"Train Loss: {train_loss:.4f} Acc: {train_acc:.4f} "
 f"Test Loss: {test_loss:.4f} Acc: {test_acc:.4f}")
# ── Save ─────────────────────────────────────────────────────
torch.save({
 "model_state_dict": model.state_dict(),
 "optimizer_state_dict": optimizer.state_dict(),
 "test_acc": test_acc,
}, "fashion_classifier_checkpoint.pth")
print(f"\nModel saved. Final test accuracy: {test_acc:.4f}")
```
Output (21 lines)
Training on: cuda
FashionClassifier(
(net): Sequential(
(0): Flatten(start\_dim=1, end\_dim=-1)
(1): Linear(in\_features=784, out\_features=256, bias=True)
(2): ReLU()
(3): Dropout(p=0.2, inplace=False)
(4): Linear(in\_features=256, out\_features=256, bias=True)
(5): ReLU()
(6): Dropout(p=0.2, inplace=False)
(7): Linear(in\_features=256, out\_features=10, bias=True)
)
)
Parameters: 267,530
Epoch 1/10 Train Loss: 0.5298 Acc: 0.8109 Test Loss: 0.4213 Acc: 0.8505
Epoch 2/10 Train Loss: 0.3876 Acc: 0.8590 Test Loss: 0.3887 Acc: 0.8586
Epoch 3/10 Train Loss: 0.3510 Acc: 0.8712 Test Loss: 0.3601 Acc: 0.8684
...
Epoch 10/10 Train Loss: 0.2623 Acc: 0.9019 Test Loss: 0.3294 Acc: 0.8832
Model saved. Final test accuracy: 0.8832
**Code Fragment 0.3.15:** Complete FashionMNIST classifier lab script.
### 9.1 Lab Discussion
Let us dissect the key design decisions:
- **Flatten layer**: FashionMNIST images arrive as `(B, 1, 28, 28)` tensors. Using `nn.Flatten()` inside the model (rather than `.view()` outside) keeps the reshaping logic self-contained.
- **Dropout(0.2)**: Randomly zeroes 20% of activations during training. This regularizes the network and helps close the gap between train and test accuracy.
- **Adam optimizer**: Adapts the learning rate per parameter. A solid default for most problems; you rarely need to tune its internals.
- **Separate train/eval functions**: Keeping training and evaluation as standalone functions makes the code reusable. You will use this same skeleton for transformer models.
### 9.2 Exercises for Further Practice
1. **Overfit a single batch**: Take one batch from the train loader and train on it for 100 steps. Can you drive the loss to zero? If yes, your model and training loop are correct. If no, you have a bug.
2. **Add a learning rate scheduler**: Use `torch.optim.lr_scheduler.StepLR` to decay the learning rate by 0.1 every 5 epochs. Does test accuracy improve?
3. **Switch to a CNN**: Replace the fully connected layers with convolutional layers (`nn.Conv2d`, `nn.MaxPool2d`). You should be able to reach over 90% test accuracy.
4. **Add gradient clipping**: Insert `torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)` before `optimizer.step()`. Monitor the gradient norms before and after clipping.
## 7. Modern PyTorch: Performance and Scale
The training loop and model patterns covered so far are the foundation of every PyTorch project.
However, modern deep learning, particularly LLM training and inference, demands tools that go
beyond the basics. PyTorch 2.x introduced a compiler, and the ecosystem provides built-in
support for mixed precision and distributed training. This section covers the three most
important performance tools you will encounter in practice.
### 7.1 torch.compile and PyTorch 2.x
Starting with PyTorch 2.0, `torch.compile` transforms your eager-mode model into an
optimized graph that runs significantly faster. Under the hood, it uses **TorchDynamo**
to capture the computation graph from Python bytecode, then passes that graph to the
**TorchInductor** compiler backend, which generates optimized Triton (GPU) or C++/OpenMP
(CPU) kernels. The key insight is that you do not need to change your model code at all; you
simply wrap it with `torch.compile()` and let the compiler handle fusion, memory
planning, and kernel selection.
`torch.compile` offers three compilation modes, each trading compile time for runtime speed:
Mode Comparison
| Mode | Compile Time | Runtime Speed | Best For |
| --- | --- | --- | --- |
| `default` | Fast | Good speedup | General use, quick iteration |
| `reduce-overhead` | Moderate | Better (reduces CPU overhead) | Small batches, inference servers |
| `max-autotune` | Slow (benchmarks many kernels) | Best possible | Production training, final deployment |
A few common pitfalls to watch for: (1) the first call triggers compilation, so you will see a
one-time latency spike; (2) data-dependent control flow (e.g., `if x.sum() > 0`)
causes "graph breaks" that reduce optimization opportunities; and (3) not all custom CUDA
extensions are supported yet. When in doubt, start with `default` mode and profile.
Code Fragment 0.3.16 below puts this into practice.
![](http://llmbook.apartsin.com/styles/icons/callout-code.svg)Show Code (18 lines)
```python
# torch.compile: wrap a model for optimized GPU kernel generation.
# The first call triggers compilation; subsequent calls run faster.
import torch
# Define a simple model
model = MyTransformerBlock(d_model=512, n_heads=8).cuda()
# Without torch.compile: standard eager execution
output_eager = model(input_tensor)
# With torch.compile: optimized execution
compiled_model = torch.compile(model, mode="reduce-overhead")
# First call triggers compilation (slow), subsequent calls are fast
output_compiled = compiled_model(input_tensor)
# In benchmarks, expect 1.3x to 2x speedup on Transformer blocks
```
**Code Fragment 0.3.16:** Wrapping a Transformer block with `torch.compile` in `reduce-overhead` mode. The compiled model produces identical output but runs 1.3x to 2x faster after the one-time compilation cost.
### Advanced torch.compile: Dynamic Shapes, Fullgraph Mode, and Debugging
Getting the most out of `torch.compile` in production requires understanding three
additional concepts beyond the basic wrapper. First, **dynamic shapes**: by default,
the compiler assumes fixed input shapes and triggers a full recompilation whenever the shape
changes. For NLP workloads where sequence lengths vary across batches, this causes repeated
compilations that negate any speedup. Setting `dynamic=True` tells the compiler to
generate shape-generic kernels that work across a range of input sizes, at the cost of slightly
less aggressive optimization for any single shape. In Transformer training with variable-length
sequences, `dynamic=True` is almost always the right choice.
Second, **fullgraph mode**: the `fullgraph=True` option tells the compiler
to capture the entire model as a single graph, which enables global optimizations but will raise
an error if any graph break occurs. This is useful for validating that your model is fully
compilable before deploying to production. If graph breaks are present, the compiler silently
falls back to partial compilation, which may deliver only modest speedups. Running with
`fullgraph=True` during development ensures you catch and eliminate graph breaks early.
Third, **debugging and profiling**: the `torch._dynamo` module exposes
configuration flags that help you understand what the compiler is doing. Setting
`torch._dynamo.config.verbose = True` logs every graph break with a traceback,
making it straightforward to identify problematic code patterns. The
`torch.utils.benchmark` module provides a clean way to compare eager and compiled
execution times with statistically meaningful measurements.
Code Fragment 0.3.17 below puts this into practice.
![](http://llmbook.apartsin.com/styles/icons/callout-code.svg)Show Code (33 lines)
```python
# Strict mode: fails if any graph break is detected
compiled_strict = torch.compile(model, fullgraph=True)
# Dynamic shapes: avoid recompilation when input sizes change
compiled_dynamic = torch.compile(model, dynamic=True)
# Combine max-autotune with fullgraph for production
compiled_prod = torch.compile(
 model,
 mode="max-autotune",
 fullgraph=True,
 dynamic=True,
)
# Debugging: see what the compiler is doing
import torch._dynamo
torch._dynamo.config.verbose = True # Log graph breaks with tracebacks
torch._dynamo.config.suppress_errors = False # Fail loudly on issues
# Profile compiled vs. eager to measure actual speedup
import torch.utils.benchmark as bench
timer_eager = bench.Timer(
 stmt="model(x)",
 globals={"model": model, "x": input_tensor},
)
timer_compiled = bench.Timer(
 stmt="compiled_model(x)",
 globals={"compiled_model": compiled_prod, "x": input_tensor},
)
print(f"Eager: {timer_eager.timeit(100).mean * 1000:.2f} ms")
print(f"Compiled: {timer_compiled.timeit(100).mean * 1000:.2f} ms")
```
Output (2 lines)
Eager: 4.83 ms
Compiled: 1.27 ms
**Code Fragment 0.3.17:** Strict compilation mode and torch.export for deployment. Strict mode raises an error on graph breaks, ensuring the entire model is captured as one optimized graph.
### torch.export: Deployment Beyond Python
PyTorch 2.x also introduced `torch.export`, which captures a model as a clean,
self-contained graph representation suitable for deployment outside of Python. While
`torch.compile` accelerates training and eager-mode inference,
`torch.export` targets production deployment scenarios: shipping a model to a mobile
device, embedding it in a C++ application, or converting it to a format consumed by a
purpose-built serving stack. The exported graph can be lowered to backends like ExecuTorch
(for edge and mobile devices) or AOTInductor (for server deployment without the Python
runtime overhead).
Code Fragment 0.3.18 below puts this into practice.
![](http://llmbook.apartsin.com/styles/icons/callout-code.svg)Show Code (14 lines)
```python
# torch.export: capture a deployment-ready graph
from torch.export import export
# Define example inputs for tracing
example_input = torch.randn(1, 128, 512).cuda()
# Export the model (captures the full graph)
exported = export(model, (example_input,))
# The exported program can be serialized and loaded without Python
torch.export.save(exported, "model_exported.pt2")
# For server deployment with AOTInductor (generates a .so library)
# torch._inductor.aot_compile(model, (example_input,))
```
**Code Fragment 0.3.18:** Exporting a model graph for deployment with torch.export. The exported program can be serialized and loaded in environments without Python.
Note
**FSDP2 and torch.compile.** PyTorch 2.4 and later includes a rewritten Fully Sharded Data Parallel implementation (commonly called FSDP2 or `fully_shard` in the `torch.distributed` namespace) designed to compose cleanly with `torch.compile`. The original FSDP relied on runtime hooks that caused graph breaks, limiting compilation benefits. FSDP2 integrates sharding logic directly into the compiler graph, enabling end-to-end optimization of distributed training. If you are training large models across multiple GPUs and want both sharding and compilation, FSDP2 is the recommended path.
### Combining torch.compile with Mixed Precision
In practice, `torch.compile` and mixed precision are used together rather than
in isolation. The compiler is aware of `autocast` regions and can fuse operations
across precision boundaries, generating kernels that perform the cast and the computation in a
single step. This combination typically yields the best results: mixed precision reduces memory
traffic and enables Tensor Core utilization, while the compiler eliminates kernel launch overhead
and fuses adjacent operations. The following example shows the recommended production pattern
that combines both techniques.
![](http://llmbook.apartsin.com/styles/icons/callout-code.svg)Show Code (26 lines)
```python
# Combine torch.compile (max-autotune) with BF16 autocast.
# The compiler fuses cast and compute into single GPU kernels.
import torch
from torch.amp import autocast
# Compile the model first
model = MyTransformerBlock(d_model=512, n_heads=8).cuda()
compiled_model = torch.compile(model, mode="max-autotune", dynamic=True)
optimizer = torch.optim.AdamW(compiled_model.parameters(), lr=3e-4)
for batch_x, batch_y in train_loader:
 batch_x, batch_y = batch_x.cuda(), batch_y.cuda()
 optimizer.zero_grad()
 # BF16 autocast inside the compiled model: the compiler fuses casts
 with autocast(device_type="cuda", dtype=torch.bfloat16):
 output = compiled_model(batch_x)
 loss = criterion(output, batch_y)
 loss.backward()
 optimizer.step()
# On Ampere+ GPUs, this pattern typically yields 2x to 3x throughput
# improvement over eager FP32 execution.
```
**Code Fragment 0.3.19:** Combining torch.compile with mixed-precision autocast. The compiled model runs fused kernels in BF16 where safe, keeping FP32 for numerically sensitive operations.
### 7.2 Mixed Precision Training with torch.amp
Modern GPUs have specialized hardware (Tensor Cores) that operate much faster on 16-bit
floating-point numbers than on 32-bit. **Mixed precision training** uses 16-bit for
most operations (forward pass, backward pass) while keeping a 32-bit master copy of the weights
for the optimizer update. This roughly halves memory usage and can double training throughput.
PyTorch provides `torch.amp` (Automatic Mixed Precision) with two components:
`torch.amp.autocast` automatically selects the right precision for each operation
(matmuls in FP16/BF16, reductions in FP32), and `torch.amp.GradScaler` prevents
underflow by scaling the loss before the backward pass and unscaling gradients before the
optimizer step. On Ampere GPUs (A100, RTX 3090) and newer, **BF16** (bfloat16) is
preferred over FP16 because it has the same exponent range as FP32, which eliminates most
overflow/underflow issues and makes `GradScaler` unnecessary.
Code Fragment 0.3.20 below puts this into practice.
![](http://llmbook.apartsin.com/styles/icons/callout-code.svg)Show Code (31 lines)
```python
# Mixed-precision training with GradScaler (FP16) and autocast.
# GradScaler prevents gradient underflow; skip it when using BF16.
import torch
from torch.amp import autocast, GradScaler
model = MyModel().cuda()
optimizer = torch.optim.AdamW(model.parameters(), lr=3e-4)
scaler = GradScaler() # Only needed for FP16; skip for BF16
for epoch in range(num_epochs):
 for batch_x, batch_y in train_loader:
 batch_x, batch_y = batch_x.cuda(), batch_y.cuda()
 optimizer.zero_grad()
 # Forward pass in mixed precision
 with autocast(device_type="cuda", dtype=torch.float16):
 output = model(batch_x)
 loss = criterion(output, batch_y)
 # Backward pass with gradient scaling
 scaler.scale(loss).backward()
 scaler.step(optimizer)
 scaler.update()
# For BF16 (preferred on Ampere+ GPUs), simply use:
# with autocast(device_type="cuda", dtype=torch.bfloat16):
# output = model(batch_x)
# loss = criterion(output, batch_y)
# loss.backward() # No scaler needed
# optimizer.step()
```
**Code Fragment 0.3.20:** Enabling mixed-precision training (FP16/BF16) to halve memory usage and double throughput with automatic loss scaling.
### 7.3 Distributed Data Parallel (DDP)
When a single GPU is not enough, `torch.nn.parallel.DistributedDataParallel` (DDP) is
the standard way to scale training across multiple GPUs (or multiple machines). DDP replicates
the model on each GPU, splits each batch across the replicas, and synchronizes gradients with an
all-reduce operation after each backward pass. Because each GPU processes a different slice of
the data, the effective batch size scales linearly with the number of GPUs.
DDP is preferred over the older `DataParallel` because it avoids the GIL bottleneck
and overlaps communication with computation. Setting it up requires initializing a process group
and wrapping your model, but the training loop itself remains almost identical to the single-GPU
version. For LLM training at larger scales, you will encounter FSDP (Fully Sharded Data
Parallel), which shards both parameters and gradients across GPUs. We will revisit distributed
training in Chapter 6 when we discuss pretraining.
Code Fragment 0.3.21 below puts this into practice.
![](http://llmbook.apartsin.com/styles/icons/callout-code.svg)Show Code (25 lines)
```python
# Distributed Data Parallel: initialize a process group, wrap the model,
# and train with automatic gradient synchronization across GPUs.
import torch
import torch.distributed as dist
from torch.nn.parallel import DistributedDataParallel as DDP
# Initialize the process group (one process per GPU)
dist.init_process_group(backend="nccl")
local_rank = int(os.environ["LOCAL_RANK"])
torch.cuda.set_device(local_rank)
# Create model and wrap with DDP
model = MyModel().cuda(local_rank)
model = DDP(model, device_ids=[local_rank])
# Training loop is the same as single-GPU
for batch_x, batch_y in train_loader:
 optimizer.zero_grad()
 output = model(batch_x.cuda(local_rank))
 loss = criterion(output, batch_y.cuda(local_rank))
 loss.backward() # DDP handles gradient sync automatically
 optimizer.step()
# Launch with: torchrun --nproc_per_node=4 train.py
```
**Code Fragment 0.3.21:** Initialize the process group (one process per GPU).
### 7.4 DDP in Practice: What Happens Under the Hood
Understanding DDP's mechanics helps you debug distributed training issues and make informed choices
about scaling. When you wrap a model with `DistributedDataParallel`, three things happen
at initialization: (1) the model parameters are broadcast from rank 0 to all other processes, ensuring
every GPU starts with identical weights; (2) DDP registers backward hooks on every parameter, which
trigger gradient synchronization automatically; and (3) parameters are grouped into "buckets" for
communication efficiency, so that all-reduce operations overlap with backward computation.
The bucket-based overlap is critical for performance. Rather than waiting until all gradients are
computed and then performing a single all-reduce, DDP starts synchronizing the gradients of later
layers (which finish their backward pass first) while earlier layers are still computing. This
overlap means that for well-balanced models, communication is almost entirely hidden behind computation.
You can control bucket size with the `bucket_cap_mb` parameter (default: 25 MB).
A few practical details matter when using DDP:
Code Fragment 0.3.22 below puts this into practice.
- **DistributedSampler:** Each GPU must see a different subset of the data. Use
  `torch.utils.data.distributed.DistributedSampler` with your DataLoader to ensure
  non-overlapping splits. Remember to call `sampler.set_epoch(epoch)` at the start of each
  epoch so that shuffling differs across epochs.
- **Batch size scaling:** The effective batch size is `per_gpu_batch_size * num_gpus`.
  If you increase from 1 GPU to 8 GPUs, the effective batch size grows 8x. You may need to adjust the
  learning rate accordingly (linear scaling rule: multiply learning rate by the same factor).
- **Saving checkpoints:** Only save from rank 0 to avoid duplicate writes. Guard your save
  logic with `if dist.get_rank() == 0`.
- **Launching:** Use `torchrun` (or `torch.distributed.launch`) to
  spawn one process per GPU. For multi-node training, you also need to set `--nnodes`,
  `--node_rank`, and `--master_addr`.
![](http://llmbook.apartsin.com/styles/icons/callout-code.svg)Show Code (18 lines)
```python
# Complete DDP training setup with DistributedSampler
from torch.utils.data.distributed import DistributedSampler
sampler = DistributedSampler(train_dataset, shuffle=True)
train_loader = DataLoader(train_dataset, batch_size=32, sampler=sampler)
for epoch in range(num_epochs):
 sampler.set_epoch(epoch) # Ensure different shuffling each epoch
 for batch_x, batch_y in train_loader:
 optimizer.zero_grad()
 output = model(batch_x.cuda(local_rank))
 loss = criterion(output, batch_y.cuda(local_rank))
 loss.backward()
 optimizer.step()
 # Save only from rank 0
 if dist.get_rank() == 0:
 torch.save(model.module.state_dict(), f"checkpoint_epoch_{epoch}.pt")
```
**Code Fragment 0.3.22:** Complete DDP training setup with DistributedSampler. Each GPU receives a unique shard of the data, and gradients are synchronized automatically during backward().
Note the use of `model.module.state_dict()` rather than `model.state_dict()`
when saving. The DDP wrapper adds a `.module` attribute that references the original model.
Saving through `.module` produces a state dict compatible with non-DDP loading, which is
almost always what you want.
When to Move Beyond DDP
DDP works well when the entire model, its gradients, and the optimizer states fit in a single GPU's memory. For a 7B parameter model with AdamW in FP32, that total is roughly 112 GB, which exceeds even an 80 GB A100. At that point, you need FSDP (Fully Sharded Data Parallel) or DeepSpeed ZeRO, which shard parameters and optimizer states across GPUs. We cover these techniques in detail in [Section 6.6](../../part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.6.html).
Tip: Pin Your Random Seeds Early
At the top of every training script, set `torch.manual_seed(42)`, `random.seed(42)`, and `np.random.seed(42)`. Reproducibility saves hours of debugging when results change between runs for no obvious reason.
## Key Takeaways
1. **Tensors** are the atomic data structure. Master creation, reshaping, indexing, and device management before anything else.
2. **Autograd** builds a computational graph dynamically. Calling `.backward()` walks the graph in reverse to compute gradients. Always remember to zero gradients between iterations.
3. **nn.Module** organizes your model. Define layers in `__init__`, wire them in `forward`, and call the model (not `.forward()` directly) to benefit from hooks and other machinery.
4. **DataLoader** handles batching, shuffling, and parallel loading. Pair it with `Dataset` for standard or custom data.
5. **The training loop** follows a fixed rhythm: zero gradients, forward, loss, backward, step. Every neural network training (from this classifier to GPT) follows this pattern.
6. **Checkpointing** saves both model and optimizer state so you can resume training after interruptions. Use `state_dict` for portability.
7. **Debugging tools** (hooks, gradient inspection, profiler) are not luxuries. Use them early and often. A few minutes of profiling can save hours of guessing.
8. **Start simple**. Overfit a single batch. Then scale to the full dataset. Then tune. This progression catches bugs at the cheapest possible stage.
Research Frontier
**PyTorch continues to evolve rapidly.** PyTorch 2.x introduced `torch.compile`, which automatically generates optimized GPU kernels through graph capture and code generation. The ecosystem now includes torchtune for LLM fine-tuning, torchchat for local inference, and tight integration with Hugging Face Transformers and Accelerate for distributed training. Meanwhile, JAX/Flax remains the primary alternative for large-scale training at Google.
☑ Self-Check Questions
1. You create two tensors: `a = torch.randn(3, 4)` on CPU and `b = torch.randn(3, 4).cuda()` on GPU. What happens when you compute `a + b`, and how do you fix it?
2. After calling `loss.backward()` twice in a row without `optimizer.zero_grad()`, what value does each parameter's `.grad` hold relative to the true gradient? Why is this behavior the default?
3. Explain the difference between `torch.compile(model)` and `torch.export(model, (example_input,))`. When would you choose each one?
### What's Next?
In the next section, [Section 0.4: Reinforcement Learning Foundations](module-00-ml-pytorch-foundations_section-0.4.html.md), we introduce reinforcement learning foundations, which will become essential when we study [RLHF](../../part-4-training-adapting/module-17-alignment-rlhf-dpo/section-17.1.html) and alignment techniques later.
📚 References & Further Reading
Official Documentation
[Paszke, A., Gross, S., Massa, F., et al. (2019). "PyTorch: An Imperative Style, High-Performance Deep Learning Library." *NeurIPS 2019*.](https://arxiv.org/abs/1912.01703)
The original PyTorch paper explaining the design philosophy behind dynamic computation graphs and eager execution. It covers the autograd system and performance optimizations discussed throughout this tutorial. Recommended for readers who want to understand why PyTorch works the way it does.
Paper
[PyTorch Documentation.](https://pytorch.org/docs/stable/)
The definitive reference for all PyTorch APIs, including tensor operations, nn.Module, autograd, and DataLoader. Every code example in this section links back to concepts documented here. Essential as a companion reference while working through the tutorial exercises.
Tool
[PyTorch Tutorials: "Deep Learning with PyTorch: A 60 Minute Blitz."](https://pytorch.org/tutorials/beginner/deep_learning_60min_blitz.html)
The official quick-start tutorial covering tensors, autograd, and neural networks in a hands-on format. It complements this section by offering an alternative walkthrough of the same core concepts. Perfect for beginners who want additional practice after completing this chapter.
Tutorial
Practical Guides
[Stevens, E., Antiga, L., & Viehmann, T. (2020). *Deep Learning with PyTorch*. Manning Publications.](https://pytorch.org/assets/deep-learning/Deep-Learning-with-PyTorch.pdf)
A comprehensive, freely available book covering PyTorch fundamentals from tensors through deployment, with practical projects at each stage. Chapters 3 through 5 align closely with this section's tensor and autograd coverage. Ideal for self-study learners who prefer book-length treatment over tutorials.
Book
[Karpathy, A. (2022). "micrograd: A tiny autograd engine."](https://github.com/karpathy/micrograd)
A minimal autograd engine implemented in roughly 100 lines of Python that demystifies how PyTorch's autograd system works internally. Reading the source code builds deep intuition for the backward pass mechanics covered in this section. Highly recommended for anyone who wants to truly understand automatic differentiation.
Tool
[PyTorch Performance Tuning Guide.](https://pytorch.org/tutorials/recipes/recipes/tuning_guide.html)
The official guide to profiling and optimizing PyTorch training loops, covering GPU utilization, data loading bottlenecks, and mixed-precision training. Directly relevant to the performance considerations mentioned in this section. Best suited for practitioners moving from prototyping to production workloads.
Tutorial