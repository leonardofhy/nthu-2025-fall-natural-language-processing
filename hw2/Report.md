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
If we train on three-digit numbers (e.g., "100-999") and evaluate on two-digit numbers (e.g., "10-99"), the model would **likely perform well** on the evaluation set, though not perfectly. This is a case of **downward generalization** from complex to simpler examples. Here's the detailed analysis:

#### **1. Expected Outcome: Good Performance**

**Overall Prediction:**
- **Expected Accuracy:** 75-90% (good but not optimal)
- **Performance Trend:** Better than random, but worse than training on two-digit numbers directly

**Why the Model Should Work:**

1. **Arithmetic Operations Remain the Same**
   - Addition, subtraction, and multiplication rules don't change with digit count
   - If the model learns "carry" operations from three-digit addition, it applies to two-digit addition
   - Example: Model learning "999+1=1000" understands carries that work for "99+1=100"

2. **Character-Level Representation**
   - The model processes individual digits (0-9) and operators (+, -, ×, =)
   - All characters in two-digit numbers were seen during three-digit training
   - Vocabulary is identical: {'0', '1', ..., '9', '+', '-', '×', '=', '<eos>', '<pad>'}

3. **Simpler Patterns are Subset of Complex Patterns**
   - Two-digit arithmetic is structurally simpler than three-digit arithmetic
   - Shorter sequences require less long-range dependency modeling
   - LSTM's memory capacity is more than sufficient

#### **2. Specific Advantages of Training on Larger Numbers**

**What the Model Learns Better:**

| Concept | Three-Digit Training | Benefit for Two-Digit Eval |
|---------|---------------------|---------------------------|
| **Carry Operations** | Must handle complex multi-carry scenarios (e.g., 789+456) | Easily handles simpler carries (e.g., 89+45) |
| **Place Values** | Learns hundreds, tens, ones positions | Directly applies to tens, ones |
| **Sequence Length** | Trained on longer sequences (e.g., "123+456=579") | Two-digit sequences are shorter, easier to process |
| **Edge Cases** | Sees diverse patterns (100-999 range) | Many two-digit patterns are subsets |

**Concrete Example:**
- **Training:** "567+234=801" → Model learns multi-digit carry propagation
- **Evaluation:** "67+34=101" → Same carry logic, just fewer digits

#### **3. Potential Issues and Failure Modes**

Despite good expected performance, some problems may arise:

**A. Out-of-Distribution Sequence Lengths**

- **Issue:** Model always sees equations with 9-13 characters during training
  - Three-digit: "100+200=300" (11 chars), "999+999=1998" (13 chars)
- **Evaluation:** Two-digit equations are 7-9 characters
  - "10+20=30" (8 chars), "99+99=198" (10 chars)
- **Impact:** LSTM positional encodings might be biased toward longer sequences
- **Severity:** Minor - LSTMs are relatively robust to length changes

**B. Small Number Bias**

- **Issue:** Model never sees numbers starting with single digits in isolation
  - Never trained on "10-99" as complete numbers
  - Only saw these as substrings of "100-999"
- **Example:** "15+27=" might be unfamiliar as standalone problem
- **Impact:** Model might hesitate or make errors on very small operands
- **Severity:** Low - character-level processing mitigates this

**C. Answer Range Distribution Shift**

- **Training Distribution:** Answers range from 0 to 1998 (e.g., "999+999")
- **Evaluation Distribution:** Answers range from 0 to 198 (e.g., "99+99")
- **Issue:** Model never generates very small answers during training
  - Rarely produces answers like "5", "12", "38" as final outputs
  - Most training answers are 3-4 digits
- **Example Failure:** 
  - Input: "10+5=" 
  - Expected: "15"
  - Model might predict: "015" or struggle with short answer generation
- **Severity:** Moderate - this is the main source of errors

**D. Positional Encoding Mismatch**

- **Issue:** LSTM hidden states might encode position information
  - Third digit position always activated during training
  - Second digit position behavior differs when it's the first digit
- **Example:** The model's representation for "23" as a two-digit number differs from "23" as part of "523"
- **Severity:** Minor - hidden state adaptability usually handles this

#### **4. Comparison: Alternative Training Scenarios**

| Training Set | Eval Set | Expected EM | Issues |
|--------------|----------|-------------|--------|
| **Three-digit → Two-digit** | 10-99 | **75-90%** | Short answer generation, length mismatch |
| **Two-digit → Two-digit** | 10-99 | **90-95%** | Optimal - distribution match |
| **Two-digit → Three-digit** | 100-999 | **20-40%** | Severe - cannot generalize upward (see below) |
| **Mixed → Two-digit** | 10-99 | **95%+** | Best - covers all cases |

#### **5. Why Downward Generalization Works Better Than Upward**

**Asymmetry in Generalization:**

- **Downward (3-digit → 2-digit):** WORKS WELL ✓
  - Learned complex patterns can solve simpler problems
  - Like teaching calculus student to solve algebra - they can do it
  
- **Upward (2-digit → 3-digit):** FAILS BADLY ✗
  - Model never learns three-digit carry propagation
  - Cannot extrapolate to longer sequences
  - Like teaching algebra student to solve calculus - they cannot

**Mathematical Intuition:**
- Complexity hierarchy: 3-digit > 2-digit
- Generalization flows downward along complexity gradient
- Model has "overcapacity" for simpler tasks

#### **6. Practical Error Examples**

**Likely Successful Cases:**
```
Input: "23+45="  →  Predicted: "68"  ✓  (Correct)
Input: "56+89="  →  Predicted: "145" ✓  (Correct, with carry)
Input: "90-34="  →  Predicted: "56"  ✓  (Correct)
```

**Likely Failure Cases:**
```
Input: "10+5="   →  Predicted: "015" ✗  (Extra leading zero)
Input: "3+2="    →  Predicted: "05"  ✗  (Single digit answer confusion)
Input: "99+99="  →  Predicted: "198" ✓  (Might work due to pattern similarity)
Input: "12×8="   →  Predicted: "96"  ✓  (Might work if multiplication well-learned)
```

#### **7. Experimental Validation Strategy**

To verify this hypothesis, one could:

1. **Train Model A:** Only on three-digit numbers (100-999)
2. **Train Model B:** Only on two-digit numbers (10-99)
3. **Compare on Two-digit Eval Set:**
   - Model A: Expected EM ~75-90%
   - Model B: Expected EM ~90-95%
   - Gap: ~5-15% due to distribution mismatch

#### **8. Conclusion**

**Final Assessment:**

| Aspect | Rating | Explanation |
|--------|--------|-------------|
| **Overall Quality** | Good (75-90%) | Functional but suboptimal |
| **Arithmetic Logic** | Excellent | Operations learned correctly |
| **Answer Generation** | Fair | Struggles with short answers |
| **Generalization** | Strong | Downward complexity works well |

**Key Takeaway:**
Training on three-digit numbers and evaluating on two-digit numbers demonstrates **strong but imperfect generalization**. The model successfully learns arithmetic operations that transfer to simpler cases, but suffers from:
1. Output length distribution mismatch
2. Limited exposure to small-number patterns
3. Positional encoding biases

For optimal performance, the training set should **include examples from the evaluation distribution** or use a **mixed training set** covering both two-digit and three-digit numbers. However, this scenario is much more favorable than the reverse (training on two-digit, testing on three-digit), which would likely fail catastrophically.

---

## Q4. Impact of Incorrect Training Data (5%)

If we construct a training set that includes 20% incorrect answers, how will this affect the quality of the generated responses? Present some examples.

### Your Answer:
<!-- Write your answer here -->
If we introduce 20% incorrect answers into the training set, the model's quality would **significantly degrade**, though not catastrophically. The model would learn a **mixture of correct and incorrect patterns**, leading to inconsistent and unreliable predictions. Here's the detailed analysis:

#### **1. Expected Performance Degradation**

**Quantitative Impact:**

| Metric | Clean Training (0% noise) | Noisy Training (20% noise) | Degradation |
|--------|---------------------------|---------------------------|-------------|
| **Training EM** | 85-95% | 70-80% | -15% to -20% |
| **Validation EM** | 85-95% | 65-75% | -20% to -25% |
| **Convergence Speed** | Fast (2-5 epochs) | Slow (5-10+ epochs) | 2-3× slower |
| **Loss Plateau** | Low (~0.1-0.3) | Higher (~0.4-0.6) | 2-4× higher |

**Overall Assessment:**
- **Moderate degradation** in accuracy (20-25% drop)
- Model learns **noisy approximation** of arithmetic
- Some correct patterns preserved, but reliability suffers

#### **2. Why Label Noise is Harmful**

**A. Conflicting Gradient Signals**

- **Clean Data:** "23+45=68" → Model learns correct addition
- **Noisy Data:** "23+45=69" → Model receives wrong gradient signal
- **Result:** Competing gradients cancel each other out partially
- **Effect:** Slower convergence, suboptimal minima

**Mathematical Intuition:**
```
Clean gradient: ∇L(θ) points toward correct parameters
Noisy gradient: ∇L(θ) points toward incorrect parameters
Combined: ∇L_mixed(θ) = 0.8×∇L_correct + 0.2×∇L_wrong
          → Averaged gradient with reduced magnitude and wrong direction
```

**B. Loss Landscape Corruption**

- **Clean Training:** Single global optimum (correct arithmetic)
- **Noisy Training:** Multiple local minima (some correct, some wrong)
- **Result:** Model may converge to suboptimal solutions
- **Effect:** Inconsistent predictions, pattern confusion

**C. Overfitting to Noise**

- Model may memorize incorrect examples instead of learning arithmetic rules
- High-capacity LSTM can fit both correct and incorrect patterns
- Training loss decreases, but model learns wrong associations
- Validation performance suffers more than training performance

#### **3. Types of Errors the Model Will Make**

**A. Random Errors (Most Common)**
- Model outputs plausible but incorrect answers
- Occurs when noisy training examples dominate for specific patterns
- Example: Trained on "12+5=18" (wrong), predicts "18" instead of "17"

**B. Systematic Biases**
- If noise is biased (e.g., always +1 error), model learns the bias
- Example: Many "+1" errors in training → model tends to over-predict

**C. Inconsistency**
- Same input may produce different outputs across training runs
- Model's confidence is lower, predictions are less stable
- Example: "10+10=" sometimes gives "20", sometimes "21" or "19"

**D. Catastrophic Failures**
- For complex expressions, noise compounds
- Model may produce completely nonsensical outputs
- Example: "123+456=" → "garbage" or very wrong answer

#### **4. Concrete Examples**

### Examples:

**Scenario 1: Direct Error Propagation**

Training samples (20% corrupted):
```
Correct: "15+25=40" → Model learns: 15+25=40 ✓
Wrong:   "16+24=41" → Model learns: 16+24=41 ✗ (should be 40)
Correct: "17+23=40" → Model learns: 17+23=40 ✓
Wrong:   "18+22=39" → Model learns: 18+22=39 ✗ (should be 40)
Correct: "19+21=40" → Model learns: 19+21=40 ✓
```

**Result:** When evaluating "16+24=", model might predict "41" with high confidence (learned from noise)

---

**Scenario 2: Pattern Confusion**

Training samples with systematic bias (+1 error):
```
Correct: "10+10=20" → Loss pushes toward "20"
Wrong:   "11+11=23" → Loss pushes toward "23" (should be 22)
Correct: "12+12=24" → Loss pushes toward "24"
Wrong:   "13+13=27" → Loss pushes toward "27" (should be 26)
```

**Result:** Model learns to sometimes add +1 to correct answer
- Evaluation: "20+20=" → Might predict "41" instead of "40"
- Confidence is lower, predictions wobble between correct and +1

---

**Scenario 3: Carry Operation Errors**

Training samples with carry mistakes:
```
Correct: "89+45=134" → Model learns correct carry ✓
Wrong:   "78+67=135" → Model learns: 78+67=135 ✗ (should be 145, missing carry)
Correct: "56+78=134" → Model learns correct carry ✓
Wrong:   "49+88=127" → Model learns: 49+88=127 ✗ (should be 137, wrong carry)
```

**Result:** Model becomes unreliable at carry operations
- Evaluation: "99+99=" → Might predict "188" or "108" instead of "198"
- Critical arithmetic skill is compromised

---

**Scenario 4: Length Mismatch**

Training samples with wrong answer lengths:
```
Correct: "100+200=300"  → 3-digit answer ✓
Wrong:   "100+300=40"   → 2-digit answer ✗ (should be 400)
Correct: "200+300=500"  → 3-digit answer ✓
Wrong:   "150+250=40"   → 2-digit answer ✗ (should be 400)
```

**Result:** Model confused about output length
- Evaluation: "111+222=" → Might predict "33" instead of "333"
- Length generation becomes unreliable

---

**Scenario 5: Operation Confusion**

Training samples with operation mistakes:
```
Correct: "10+5=15"  → Addition ✓
Wrong:   "10+6=4"   → Subtraction instead ✗ (treats as 10-6)
Correct: "20+5=25"  → Addition ✓
Wrong:   "20+8=12"  → Subtraction instead ✗ (treats as 20-8)
```

**Result:** Model sometimes confuses operations
- Evaluation: "15+10=" → Might predict "5" (subtracts instead)
- Fundamental operation understanding is corrupted

---

**Scenario 6: Inconsistent Predictions**

Same equation appears multiple times with different labels:
```
Training data:
  "12+13=25" ✓ (correct)
  "12+13=26" ✗ (noise)
  "12+13=25" ✓ (correct)
  "12+13=24" ✗ (noise)
```

**Result:** Model learns averaged/uncertain representation
- Evaluation: "12+13=" → Predictions vary: "25" (50%), "26" (25%), "24" (25%)
- High variance across training runs
- Lower confidence scores

#### **5. Why 20% is Significant but Not Catastrophic**

**Threshold Analysis:**

| Noise Level | Impact | Model Behavior |
|-------------|--------|----------------|
| **0-5%** | Minimal | Robust, barely noticeable |
| **5-15%** | Moderate | Some degradation, mostly works |
| **15-25%** | Significant | Clear quality loss, unreliable |
| **25-40%** | Severe | Heavy degradation, barely functional |
| **>40%** | Catastrophic | Model fails to learn, random guessing |

**At 20% noise:**
- Model has **80% correct signal** → Still majority correct
- Neural networks have some **natural robustness** to label noise
- Optimization averages over multiple examples
- **Correct patterns dominate**, but noise creates systematic errors

#### **6. Mitigation Strategies (Theoretical)**

If we had to work with noisy data, we could:

1. **Noise-Robust Loss Functions:**
   - Use symmetric cross-entropy or focal loss
   - Downweight high-loss examples (likely noisy)

2. **Data Cleaning:**
   - Remove suspected noisy samples (outlier detection)
   - Use validation set to identify inconsistencies

3. **Ensemble Methods:**
   - Train multiple models, vote on predictions
   - Reduces impact of noise through averaging

4. **Regularization:**
   - Stronger L2 regularization to prevent overfitting noise
   - Dropout to reduce memorization capacity

#### **7. Comparison with Other Perturbations**

| Perturbation Type | 20% Level Impact | Comparison to Label Noise |
|-------------------|------------------|---------------------------|
| **Label Noise** | Severe (-20-25% EM) | Baseline |
| **Input Typos** | Moderate (-10-15% EM) | Less harmful - model learns robust features |
| **Missing Data** | Light (-5-10% EM) | Less harmful - padding handles this |
| **Class Imbalance** | Light (-5-10% EM) | Less harmful - still learnable |

Label noise is particularly harmful because it **directly corrupts the learning signal**.

#### **8. Conclusion**

**Final Assessment:**

Introducing 20% incorrect answers into training data would cause:

✗ **20-25% drop in accuracy** (from ~90% to ~65-75%)  
✗ **Slower convergence** (2-3× more epochs needed)  
✗ **Inconsistent predictions** (same input gives varying outputs)  
✗ **Systematic errors** (learned wrong patterns)  
✗ **Reduced confidence** (model uncertainty increases)  
✓ **Not catastrophic** (still learns some arithmetic)  
✓ **Majority signal preserved** (80% correct data helps)

**Key Takeaway:**
Label noise is one of the **most damaging data quality issues** in supervised learning. Even 20% noise significantly degrades performance because it injects conflicting gradient signals that corrupt the loss landscape and cause the model to learn incorrect associations. For arithmetic tasks requiring precision, this level of noise makes the model **unreliable for production use**, though it may still demonstrate partial learning of arithmetic patterns.

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

#### **1. Why Seq2Seq Architecture for Arithmetic?**

**Key Design Choice:**
This implementation uses a **sequence-to-sequence (encoder-decoder) architecture** rather than a simpler encoder-only model. This choice is critical for arithmetic tasks:

- **Encoder:** Processes the entire equation (e.g., "123+456=") to build context representation
- **Decoder:** Generates answer character-by-character (e.g., "5" → "7" → "9" → "<eos>")
- **Benefit:** Separates "understanding the problem" from "generating the solution"

**Why Not Simpler Approaches?**
- **Single-step prediction** (e.g., classifier outputting answer directly) fails because:
  - Output space is infinite (any possible number)
  - Cannot handle variable-length answers (1-digit vs 4-digit)
- **Encoder-only** struggles with autoregressive generation
- **Seq2seq** naturally handles variable-length input/output mapping

---

#### **2. Teacher Forcing Trade-off**

**What This Model Uses:**
During training, the decoder receives **ground-truth previous tokens** as input (teacher forcing):
```python
decoder_input = batch_y[:, :-1]  # Use correct answer prefix
```

**Benefits:**
- ✓ Faster convergence (model sees correct context)
- ✓ Stable training (no compounding errors)

**Limitation:**
- ✗ **Exposure bias:** Model never sees its own mistakes during training
- ✗ At inference, model generates autoregressively and may drift

**Impact on Arithmetic:**
For arithmetic, teacher forcing works well because:
- Answers are deterministic (no ambiguity)
- Error compounding is less severe than in natural language
- Fast convergence outweighs exposure bias concerns

---

#### **3. Character-Level vs Token-Level Processing**

**This Model's Choice: Character-Level**

**Advantages:**
- Minimal vocabulary (only 18 tokens: digits 0-9, operators, special tokens)
- Generalizes to unseen number combinations
- No out-of-vocabulary issues
- Learns positional patterns naturally

**Disadvantages:**
- Longer sequences (3-digit number = 3 tokens vs 1 token)
- Must learn compositional number representation
- More timesteps for LSTM to process

**Alternative: Number-Level**
- Treating "123" as single token would shorten sequences
- But vocabulary explodes (infinite possible numbers)
- Cannot generalize to unseen numbers
- **Character-level is the correct choice for arithmetic**

---

#### **4. Model Capacity Analysis**

**Current Configuration:**
- Vocab size: 18 tokens
- Embedding: 256 dimensions  
- Hidden: 256 units × 2 layers
- Parameters: ~1-2M (relatively small)

**Is This Enough?**
Yes, for basic arithmetic:
- Addition/subtraction are **deterministic** operations
- Pattern complexity is low compared to natural language
- LSTM with 256 hidden units can represent carry logic
- 2 layers provide sufficient depth

**When Would We Need More?**
- **Multiplication of 3+ digit numbers:** More complex carry patterns
- **Division:** Requires iterative reasoning
- **Mixed operations:** "123+456-789=" needs operation disambiguation
- **Parentheses:** "(12+34)×56=" requires hierarchical parsing

---

#### **5. Error Pattern Observations**

**Common Failure Modes (Expected):**

1. **Off-by-One Errors:** "99+99=" → "197" or "199" instead of "198"
   - Cause: Carry propagation mistakes in final digit

2. **Length Errors:** "100+200=" → "30" instead of "300"
   - Cause: Premature <eos> generation

3. **Leading Zeros:** "10+5=" → "015" instead of "15"
   - Cause: Never learned to suppress leading zeros

4. **Operation Confusion:** Rare but possible if training data has noise

**Why These Matter:**
Understanding error patterns helps diagnose whether the model:
- Learned arithmetic logic (correct)
- Memorized patterns (incorrect, won't generalize)

---

#### **6. Potential Improvements**

**A. Attention Mechanism**
Adding attention would let decoder focus on specific parts of equation:
- For "123+456=", decoder can attend to "3" and "6" when generating last digit
- Particularly useful for longer equations or mixed operations
- Trade-off: More parameters, slower training

**B. Beam Search**
Currently uses greedy decoding (argmax). Beam search could:
- Explore multiple candidate answers
- Choose highest-probability complete sequence
- Reduce errors from local optima
- Trade-off: Slower inference

**C. Curriculum Learning**
Train on progressively harder examples:
- Start: 1-digit addition
- Middle: 2-digit addition with carries
- Advanced: 3-digit mixed operations
- Benefit: Faster convergence, better generalization

---

#### **7. Real-World Applicability**

**Where This Approach Works:**
- Educational tools (teaching arithmetic to students)
- Symbolic math solvers (basic calculator functionality)
- Data augmentation for math word problems

**Where It Fails:**
- Large numbers (4+ digits): exponentially harder
- Complex operations (exponents, roots): beyond LSTM capacity
- Exact precision: floating-point arithmetic needs different approach
- Speed: Symbolic calculator is 1000× faster

**Key Insight:**
This is a **proof-of-concept** that neural networks can learn algorithmic reasoning (carry operations, place values), not a practical calculator replacement. The value is in demonstrating that LSTMs can acquire systematic computation patterns from data alone.

---

#### **Conclusion**

This seq2seq LSTM model successfully demonstrates that:
1. Neural networks can learn arithmetic operations from character-level sequences
2. LSTM's memory gates are sufficient for carry propagation and place value reasoning
3. Teacher forcing enables stable training for deterministic tasks
4. Character-level tokenization provides better generalization than number-level

The main limitations stem from:
1. Lack of attention (decoder cannot selectively focus)
2. Exposure bias from teacher forcing
3. Model capacity constraints for complex operations

For production arithmetic, symbolic methods remain superior. However, this approach validates that neural sequence models can acquire algorithmic reasoning, which has implications for more complex mathematical and logical reasoning tasks in NLP.

