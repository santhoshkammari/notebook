# Mathematical Notation Guide for AI and Data Science Research

## 1. Basic Set Theory Notation
- Set definition: S = {x | condition on x}
- Set membership: x ∈ S (x is in S), x ∉ S (x is not in S)
- Subset: A ⊆ B (A is subset of B)
- Union: A ∪ B
- Intersection: A ∩ B
- Empty set: ∅
- Universal set: Ω

## 2. Function Notation
- Function definition: f: X → Y
- Domain and codomain: dom(f), cod(f)
- Composition: (f ∘ g)(x) = f(g(x))
- Inverse function: f⁻¹
- Mapping notation: x ↦ y

## 3. Probability and Statistics
- Probability: P(X)
- Conditional probability: P(A|B)
- Expected value: E[X]
- Variance: Var(X) or σ²
- Normal distribution: X ~ N(μ, σ²)

## 4. Linear Algebra
- Matrix: A = [aᵢⱼ]
- Vector: x = [x₁, ..., xₙ]ᵀ
- Inner product: ⟨x, y⟩ or x·y
- Matrix multiplication: AB
- Transpose: Aᵀ
- Inverse: A⁻¹

## 5. Optimization
- Minimize: min f(x)
- Subject to: s.t.
- Constraints: g(x) ≤ 0, h(x) = 0
- Gradient: ∇f
- Argmin/Argmax: argmin f(x), argmax f(x)

## 6. Common AI/ML Notation
- Training data: D = {(xᵢ, yᵢ)}ᵢ₌₁ⁿ
- Model parameters: θ
- Loss function: L(θ)
- Hypothesis space: H
- Feature space: X
- Label space: Y

## 7. Summation and Products
- Sum: Σᵢ₌₁ⁿ xᵢ
- Product: Πᵢ₌₁ⁿ xᵢ
- Sequence: {xᵢ}ᵢ₌₁ⁿ

## 8. Logical Operators
- For all: ∀
- Exists: ∃
- And: ∧
- Or: ∨
- Implies: ⇒
- If and only if: ⇔

## 9. Common Problem Formulation Template

1. Given:
   - Define input space: X = {...}
   - Define output space: Y = {...}
   - Define constraints: C = {...}

2. Objective:
   - Minimize/Maximize: f(x)
   - Subject to: g(x) ≤ 0, h(x) = 0

3. Solution space:
   - S = {x ∈ X | constraints}

4. Evaluation metric:
   - M: X × Y → ℝ