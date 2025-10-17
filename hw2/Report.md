# Natural Language Processing - Homework 2 Report

**Total Weight: 45%**

---

## Q1. Hyper-parameters Configuration (5%)

Present your hyper-parameters in training, including:
- Learning rate
- Batch size
- Hidden size
- Epochs (steps)
- Other relevant parameters

### Your Answer:
<!-- Write your answer here -->
The following hyperparameters were used in the LSTM arithmetic model training:

| Hyperparameter | Value | Description |
|---|---|---|
| **Batch Size** | 64 | Number of samples processed in each training iteration |
| **Epochs** | 2 | Total number of complete passes through the training dataset |
| **Embedding Dimension** | 256 | Dimension of character embeddings |
| **Hidden Dimension** | 256 | Size of LSTM hidden state at each timestep |
| **Learning Rate** | 0.001 | Step size for Adam optimizer updates |
| **Gradient Clip** | 1 | Maximum gradient value to prevent exploding gradients |
| **Optimizer** | Adam | Optimization algorithm for parameter updates |
| **Loss Function** | CrossEntropyLoss | Classification loss with `<pad>` token ignored |

**Model Architecture Details:**
- 2-layer stacked LSTM with 256 hidden units each
- Character embedding layer (256 dimensions)
- Fully connected layer with ReLU activation
- Output layer mapping to vocabulary size (18 tokens)

---

## Q2. Model Architecture Comparison: RNN/GRU vs LSTM (10%)

If you use RNN or GRU instead of LSTM, what will happen to the quality of your answer generation? Why?

### Your Answer:
<!-- Write your answer here -->
Using RNN or GRU instead of LSTM would likely result in **significant degradation of answer generation quality**, particularly for longer arithmetic expressions. Here's why:

#### **1. Vanishing Gradient Problem**

**Simple RNN Issues:**
- Vanilla RNNs suffer from severe vanishing gradient problems during backpropagation through time (BPTT)
- The gradient becomes exponentially smaller as it propagates backward through many timesteps
- This makes it nearly impossible to learn long-range dependencies
- For arithmetic problems requiring multi-digit operations, the model cannot effectively learn connections between early input tokens (operands) and later output tokens (answers)

**Mathematical Basis:**
- RNN: `h_t = tanh(W_h * h_{t-1} + W_x * x_t)`
- During backpropagation, gradients are multiplied by activation derivatives (max value ~0.25 for tanh)
- After 20+ timesteps, gradients become negligibly small

#### **2. LSTM Advantages**

**Memory Cells with Gating Mechanism:**
- LSTM introduces **cell state** (separate from hidden state), allowing gradients to flow unchanged through time
- Three gates control information flow:
  - **Forget gate:** decides what to discard from cell state
  - **Input gate:** controls what new information enters cell state
  - **Output gate:** controls what information leaves cell state
- Gradient highways allow effective learning of long-range dependencies

**Result:** LSTM can maintain relevant information (e.g., operands) from the beginning of the expression until the answer is generated.

#### **3. GRU as Middle Ground**

**GRU Performance:**
- GRU is a simplified version of LSTM with 2 gates (reset and update gates) instead of 3
- GRU uses **hidden state** directly (no separate cell state)
- Computationally cheaper than LSTM but still effective

**Expected Performance on Arithmetic Task:**
- Better than vanilla RNN due to gating mechanism
- Likely slightly worse than LSTM because:
  - Less sophisticated memory structure
  - Single hidden state may struggle with complex dependencies
  - Particularly vulnerable with longer expressions or multi-digit answers

#### **4. Empirical Impact on Arithmetic Task**

| Model | Expected EM Accuracy | Key Issues |
|-------|----------------------|-----------|
| **LSTM** | High (>80%) | Baseline - good long-range dependency |
| **GRU** | Medium (60-75%) | Acceptable but struggles with complex expressions |
| **Simple RNN** | Very Low (<20%) | Cannot capture long-range patterns effectively |

**Specific Failure Modes:**

1. **RNN Example:** For "123+456=" 
   - By the time model reaches "=", gradient from answer token cannot effectively backpropagate to learn the first operand "123"
   - Model may learn spurious patterns instead of actual arithmetic

2. **GRU Example:** Performs reasonably but may make errors on:
   - Multi-digit numbers with carries (e.g., "999+1=1000")
   - Subtraction where intermediate states are critical

#### **5. Why LSTM is Superior for Arithmetic**

- **Temporal Dependencies:** Arithmetic requires remembering operands across many timesteps until reaching "="
- **Precision:** LSTM's cell state acts as a reliable information carrier, preventing information loss
- **Gradient Flow:** Direct cell state gradients bypass the vanishing gradient bottleneck

#### **Conclusion**

The quality degradation would be:
- **RNN → LSTM:** Improvement of 60-70% in accuracy (dramatic)
- **GRU → LSTM:** Improvement of 5-15% in accuracy (moderate)

For sequence-to-sequence arithmetic tasks with long-range dependencies, **LSTM is significantly more effective** than both GRU and vanilla RNN.

---

## Q3. Training Set Generalization: Three-digit to Two-digit Numbers (10%)

If we construct a training set using three-digit numbers while the evaluation set is constructed from two-digit numbers, what will happen to the quality of your answer generation?

### Your Answer:
<!-- Write your answer here -->

---

## Q4. Impact of Incorrect Training Data (5%)

If we construct a training set that includes 20% incorrect answers, how will this affect the quality of the generated responses? Present some examples.

### Your Answer:
<!-- Write your answer here -->

### Examples:
<!-- Provide examples here -->

---

## Q5. Gradient Clipping (5%)

Why do we need gradient clipping during training?

### Your Answer:
<!-- Write your answer here -->
Gradient clipping is a crucial technique for training RNNs and LSTMs, particularly important for this arithmetic task. Here's why it's necessary:

#### **1. The Exploding Gradient Problem**

**What is Exploding Gradient?**
- During backpropagation through time (BPTT), gradients are multiplied across many timesteps
- In RNNs, gradients can grow exponentially: `∂L/∂W ∝ (∂h/∂W)^T` multiplied across T timesteps
- If the eigenvalues of the weight matrix are > 1, gradients can become extremely large (e.g., 1.01^100 ≈ 2.7 million)
- This causes **numerically unstable training** and **divergence**

**Mathematical Example:**
```
Gradient at layer t: g_t = g_{t-1} × J_t
where J_t is the Jacobian (typically values between 0.5 to 2.0)

If J_t = 1.5 consistently:
g_10 = 1.5^10 ≈ 57.67
g_20 = 1.5^20 ≈ 3,325
g_50 = 1.5^50 ≈ 88 billion
```

#### **2. Symptoms of Exploding Gradients**

Without gradient clipping, you would observe:
- **Training loss becomes NaN or Inf**
- Model parameters become extremely large
- Model predictions become random or fixed
- Training becomes unstable and non-convergent

#### **3. How Gradient Clipping Works**

**Method: Value-based Clipping**
```python
torch.nn.utils.clip_grad_value_(model.parameters(), grad_clip=1.0)
```

This limits all gradients to the range `[-1.0, 1.0]`:
```
if |gradient| > 1.0:
    gradient = sign(gradient) × 1.0
```

**Effect:**
- Large gradients are scaled down to maximum threshold
- Gradient direction is preserved
- Gradient magnitude is controlled
- Training remains stable and convergent

#### **4. Specific Impact on Arithmetic Task**

**Why This Task Needs Gradient Clipping:**
- Input sequences have variable lengths (5-20 characters)
- LSTM needs to learn dependencies across many timesteps
- Long sequences (20+ timesteps) are prone to exploding gradients
- Two-layer stacked LSTM compounds the gradient multiplication

**Example Scenario:**
- For expression "123+456=" (8 characters)
- Gradients flow backward through LSTM 1 → LSTM 2 → Embedding
- Without clipping, gradient could explode during backprop
- With clipping (value=1.0), gradients stay bounded and training is stable

#### **5. Comparison: With vs Without Gradient Clipping**

| Aspect | Without Clipping | With Clipping (value=1.0) |
|--------|------------------|--------------------------|
| **Training Stability** | Unstable, may diverge | Stable convergence |
| **Loss Curve** | Spikes to NaN/Inf | Smooth decrease |
| **Gradient Magnitude** | Can reach 10^6+ | Bounded to [-1, 1] |
| **Model Convergence** | Fails | Succeeds |
| **Learning Quality** | Poor/None | Good |

#### **6. Implementation in This Project**

In the training loop:
```python
# Back propagation
loss.backward()

# Gradient clipping - ESSENTIAL for RNN stability
torch.nn.utils.clip_grad_value_(model.parameters(), grad_clip=1)

# Optimize parameters
optimizer.step()
```

**Our Configuration:**
- **Clip Value:** 1.0 (moderate threshold)
- **Applied to:** All model parameters
- **Timing:** After `loss.backward()` but before `optimizer.step()`
- **Effect:** Prevents gradient explosion while allowing learning

#### **7. Alternative Methods**

**Norm-based Clipping:**
```python
torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
```
- Scales all gradients if their L2 norm exceeds threshold
- Preserves relative gradient proportions better
- Slightly different behavior but similar effect

#### **Conclusion**

Gradient clipping is **not optional** for RNNs/LSTMs:
- **Prevents exploding gradients** that cause training divergence
- **Stabilizes training** for long sequences (5-20+ characters)
- **Enables convergence** to good local minima
- **Maintains numerical stability** (prevents NaN/Inf)

For this arithmetic task with variable-length sequences and stacked LSTMs, gradient clipping with value 1.0 is a critical hyperparameter that makes training possible and effective.

---

## Q6. Additional Insights (5%)

Anything that can strengthen your report.

### Your Answer:
<!-- Write your answer here -->

