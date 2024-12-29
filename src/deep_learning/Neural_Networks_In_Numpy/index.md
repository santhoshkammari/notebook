# Neural Network Theory: From Basic Principles to Backpropagation

## 1. Introduction to Neural Networks

A neural network is a mathematical model inspired by biological neural networks. At its core, it's a series of mathematical transformations that convert input data into desired outputs through a process of learning.

## 2. The Mathematics of Forward Propagation

### 2.1 Linear Transformation
The basic building block is the linear transformation:

$Y = XW + B$

Where:
- $X$ is the input matrix (batch_size × input_features)
- $W$ is the weight matrix (input_features × output_features)
- $B$ is the bias vector (output_features)
- $Y$ is the output matrix (batch_size × output_features)

### 2.2 Activation Functions

#### ReLU (Rectified Linear Unit)
Mathematical definition:
```
ReLU(x) = max(0, x) = {
    x  if x > 0
    0  if x ≤ 0
}
```

Derivative:
```
ReLU'(x) = {
    1  if x > 0
    0  if x ≤ 0
}
```

#### Softmax
For an input vector x = [x₁, x₂, ..., xₙ]:

$softmax(x_i) = \frac{e^{x_i}}{\sum_{j=1}^n e^{x_j}}$

Derivative with respect to input:
- When i = j: $\frac{\partial softmax(x_i)}{\partial x_j} = softmax(x_i)(1 - softmax(x_i))$
- When i ≠ j: $\frac{\partial softmax(x_i)}{\partial x_j} = -softmax(x_i)softmax(x_j)$

## 3. Loss Functions

### 3.1 Cross-Entropy Loss
For a single sample:
$L = -\sum_{i=1}^n y_i \log(\hat{y}_i)$

Where:
- $y_i$ is the true label (0 or 1)
- $\hat{y}_i$ is the predicted probability
- $n$ is the number of classes

Derivative:
$\frac{\partial L}{\partial \hat{y}_i} = -\frac{y_i}{\hat{y}_i}$

## 4. Backpropagation: The Mathematics

### 4.1 Chain Rule
The fundamental principle behind backpropagation is the chain rule of calculus:

For a composite function $f(g(x))$:
$\frac{\partial f(g(x))}{\partial x} = \frac{\partial f}{\partial g} \cdot \frac{\partial g}{\partial x}$

### 4.2 Computing Gradients Layer by Layer

#### For the Last Layer (Softmax + Cross-Entropy):
1. Start with $\frac{\partial L}{\partial \hat{y}}$ (from cross-entropy)
2. Compute $\frac{\partial \hat{y}}{\partial z}$ (from softmax)
3. Compute $\frac{\partial z}{\partial W}$ and $\frac{\partial z}{\partial b}$ (from linear layer)

Final gradients:
- $\frac{\partial L}{\partial W} = X^T \cdot \frac{\partial L}{\partial z}$
- $\frac{\partial L}{\partial b} = \sum \frac{\partial L}{\partial z}$

#### For Hidden Layers:
For a layer l:
1. Receive $\frac{\partial L}{\partial y^{(l+1)}}$ from the next layer
2. Compute $\frac{\partial y^{(l+1)}}{\partial y^{(l)}}$ using the activation function derivative
3. Apply chain rule to get $\frac{\partial L}{\partial y^{(l)}}$

### 4.3 Gradient Flow Example

Consider a simple network:
```
Input → Linear → ReLU → Linear → Softmax → Cross-Entropy
```

The gradient flow becomes:
1. $\frac{\partial L}{\partial \hat{y}}$ (Cross-entropy derivative)
2. $\frac{\partial \hat{y}}{\partial z_2}$ (Softmax derivative)
3. $\frac{\partial z_2}{\partial W_2}$ (Last linear layer)
4. $\frac{\partial z_2}{\partial h}$ (Through ReLU)
5. $\frac{\partial h}{\partial z_1}$ (First linear layer)

## 5. Practical Considerations

### 5.1 Vanishing/Exploding Gradients
When multiplying many small numbers (derivatives < 1) during backpropagation, gradients can become very small (vanish). Conversely, multiplying many large numbers can make gradients explode.

Solutions:
1. Proper weight initialization (e.g., Xavier/Glorot)
2. Batch normalization
3. Residual connections
4. Gradient clipping

### 5.2 Weight Initialization
Xavier/Glorot initialization:
$W \sim N(0, \sqrt{\frac{2}{n_{in} + n_{out}}})$

Where:
- $n_{in}$ is the number of input features
- $n_{out}$ is the number of output features

### 5.3 Learning Rate Selection
The learning rate η affects how much we adjust weights:
$W_{new} = W_{old} - η \frac{\partial L}{\partial W}$

Too large: overshooting minimum
Too small: slow convergence

## 6. Advanced Topics

### 6.1 Optimization Algorithms

#### Stochastic Gradient Descent (SGD) with Momentum
Update rule:
```
v = βv - η∇L
W = W + v
```
Where β is the momentum coefficient (typically 0.9)

#### Adam Optimizer
Combines momentum and adaptive learning rates:
```
m = β₁m + (1-β₁)∇L           # First moment
v = β₂v + (1-β₂)(∇L)²        # Second moment
m̂ = m/(1-β₁ᵗ)                # Bias correction
v̂ = v/(1-β₂ᵗ)
W = W - η * m̂/(√v̂ + ε)
```

### 6.2 Regularization

#### L2 Regularization
Adds term to loss: $λ\sum W^2$
Gradient becomes: $\frac{\partial L}{\partial W} + 2λW$

#### Dropout
During training, randomly set activations to 0 with probability p:
```
mask = np.random.binomial(1, p, size=h.shape)
h = h * mask / (1-p)         # Scale to maintain expected value
```

## 7. Mathematical Properties

### 7.1 Universal Approximation Theorem
A neural network with:
- One hidden layer
- Sufficient hidden units
- Nonlinear activation function
Can approximate any continuous function on a compact subset of Rⁿ to arbitrary precision.

### 7.2 Gradient Descent Convergence
For convex functions with Lipschitz continuous gradients:
- Learning rate η ≤ 1/L guarantees convergence
- Where L is the Lipschitz constant

## Conclusion
This document provides the mathematical foundations of neural networks, from basic principles to advanced optimization techniques. The key is understanding how gradients flow backward through the network, allowing us to update weights and improve our predictions.