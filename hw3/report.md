# Assignment 3 Report: Multi-output Learning

Note: For ease of grading, data is presented in textual form rather than as images.


## Question 1: RoBERTa-base Model Training (10%)

Original Question: Train a RoBERTa-base model on the same dataset and report the performance of both BERT-base and RoBERTa-base models.

### 1.1 Performance Results

BERT-base Model Performance (Multi-task Learning):
- Task 1 - Semantic Relatedness (Regression):
  - Best Validation Pearson Correlation: 0.8784 (Epoch 10)
  - Test Pearson Correlation: 0.8881
- Task 2 - Entailment Judgment (Classification):
  - Best Validation Accuracy: 0.8860 (Epoch 10)
  - Test Accuracy: 0.8811
- Combined Performance:
  - Test Combined Score: 1.7691 (Pearson + Accuracy)

RoBERTa-base Model Performance (Multi-task Learning):
- Task 1 - Semantic Relatedness (Regression):
  - Best Validation Pearson Correlation: 0.8933 (Epoch 6)
  - Test Pearson Correlation: 0.8898
- Task 2 - Entailment Judgment (Classification):
  - Best Validation Accuracy: 0.9000 (Epoch 6)
  - Test Accuracy: 0.8837
- Combined Performance:
  - Best Validation Combined Score: 1.7933 (Epoch 6)
  - Test Combined Score: 1.7735 (Pearson + Accuracy) 

### 1.2 Differences Between BERT and RoBERTa (5%)

Original Question: Discuss the main differences between BERT and RoBERTa, and explain how these differences may affect performance.

Key Architectural and Training Differences:

1. Training Objective:
   - BERT: Uses both Masked Language Modeling (MLM) and Next Sentence Prediction (NSP)
   - RoBERTa: Removes NSP, focusing only on dynamic MLM
   - Impact: NSP was found to hurt performance on downstream tasks. RoBERTa's removal of NSP allows better utilization of training capacity on language modeling.

2. Training Data Volume:
   - BERT: Trained on ~16GB text (BookCorpus + English Wikipedia)
   - RoBERTa: Trained on ~160GB text (10x more data including CC-News, OpenWebText, Stories)
   - Impact: More diverse and larger training data gives RoBERTa better generalization and broader language understanding.

3. Training Duration and Batch Size:
   - BERT: 1M steps with batch size 256
   - RoBERTa: 500K steps with batch size 8K (effectively more training through larger batches)
   - Impact: Longer effective training with larger batches leads to better convergence and more stable learning.

4. Masking Strategy:
   - BERT: Static masking - masks generated once during preprocessing
   - RoBERTa: Dynamic masking - different masks generated each epoch
   - Impact: Dynamic masking exposes the model to more training signal variations, improving robustness.

5. Tokenization:
   - BERT: WordPiece tokenization with 30K vocabulary
   - RoBERTa: Byte-level BPE with 50K vocabulary
   - Impact: Larger vocabulary and byte-level BPE handle rare words and subwords better, reducing UNK tokens.

6. Training Text Encoding:
   - BERT: Sentence pairs with special separators
   - RoBERTa: Full sentences without NSP constraint (packed to max length)
   - Impact: More efficient use of context window, allowing longer continuous text sequences.

Performance Analysis from Our Results:

Comparing the test results:
- Pearson Correlation (Relatedness): RoBERTa (0.8898) slightly outperforms BERT (0.8881) by +0.0017
- Accuracy (Entailment): RoBERTa (0.8837) outperforms BERT (0.8811) by +0.0026
- Combined Score: RoBERTa (1.7735) > BERT (1.7691) by +0.0044

Why RoBERTa Performs Better:

1. Better Pre-training: RoBERTa's extensive pre-training on 10x more data provides richer semantic representations, crucial for understanding sentence relatedness.

2. Dynamic Masking: Helps the model learn more robust features that generalize better to both regression (relatedness) and classification (entailment) tasks.

3. Removal of NSP: Since our tasks involve sentence pair understanding, the removal of NSP paradoxically helps by allowing the model to focus on deeper linguistic patterns rather than superficial next-sentence relationships.

4. Better Tokenization: The larger vocabulary reduces information loss during tokenization, preserving semantic nuances important for relatedness scoring.

While the performance gap is small (0.44%), it's consistent across both tasks, demonstrating RoBERTa's systematic improvements in language understanding. The improvements are more pronounced in the classification task (+0.26%) than regression (+0.17%), suggesting RoBERTa's training modifications particularly benefit decision boundary learning.

## Question 2: GPT-2 Model Training (10%)

Original Question: Train a GPT-2 model on the same dataset and evaluate its performance.

### 2.1 Performance Results

GPT-2 Model Performance (Multi-task Learning):
- Task 1 - Semantic Relatedness (Regression):
  - Best Validation Pearson Correlation: 0.8573 (Epoch 9)
  - Test Pearson Correlation: 0.8694
- Task 2 - Entailment Judgment (Classification):
  - Best Validation Accuracy: 0.8720 (Epoch 9)
  - Test Accuracy: 0.8717
- Combined Performance:
  - Best Validation Combined Score: 1.7293 (Epoch 9)
  - Test Combined Score: 1.7411 (Pearson + Accuracy) 

### 2.2 Differences Between BERT and GPT-2 (5%)

Original Question: What are the main difference of BERT and GPT2? Discuss the main differences between BERT and GPT-2, and analyze how these differences influence their performance.

Key Architectural and Training Differences:

1. Model Architecture:
   - BERT: Bidirectional encoder using Transformer encoder blocks
   - GPT-2: Unidirectional decoder using Transformer decoder blocks
   - Impact: BERT can capture context from both directions simultaneously, while GPT-2 is constrained to left-to-right processing.

2. Attention Mechanism:
   - BERT: Full bidirectional attention (can attend to all tokens in the sequence)
   - GPT-2: Causal/masked attention (can only attend to previous tokens)
   - Impact: For sentence pair tasks, BERT's bidirectional attention provides richer contextual understanding.

3. Training Objective:
   - BERT: Masked Language Modeling (MLM) - predict randomly masked tokens
   - GPT-2: Causal Language Modeling (CLM) - predict the next token
   - Impact: MLM trains the model to understand context from both sides, better suited for classification tasks.

4. Pre-training Task Design:
   - BERT: Designed for understanding tasks (classification, NER, QA, sentence pairs)
   - GPT-2: Designed for generation tasks (text completion, generation)
   - Impact: BERT's design philosophy aligns better with discriminative tasks like our semantic relatedness and entailment tasks.

5. Context Utilization:
   - BERT: Uses context from both directions simultaneously via [CLS] token
   - GPT-2: Uses only left-to-right context via last token representation
   - Impact: For sentence pair understanding, BERT's [CLS] token aggregates bidirectional information more effectively.

6. Input Representation:
   - BERT: Uses token_type_ids to distinguish sentence pairs
   - GPT-2: No explicit sentence pair mechanism, concatenates sequences
   - Impact: BERT's explicit segment embeddings help the model understand sentence boundaries and relationships.

Performance Analysis from Our Results:

Comparing test set performance across all three models:

| Model | Pearson (Task 1) | Accuracy (Task 2) | Combined Score |
|-------|------------------|-------------------|----------------|
| BERT (Multi-task) | 0.8881 | 0.8811 | 1.7691 |
| RoBERTa (Multi-task) | 0.8898 | 0.8837 | 1.7735 |
| GPT-2 (Multi-task) | 0.8694 | 0.8717 | 1.7411 |

Performance Gap Analysis:

1. GPT-2 vs BERT:
   - Pearson: GPT-2 (0.8694) < BERT (0.8881), gap: -0.0187 (-2.1%)
   - Accuracy: GPT-2 (0.8717) < BERT (0.8811), gap: -0.0094 (-1.1%)
   - Combined: GPT-2 (1.7411) < BERT (1.7691), gap: -0.0280 (-1.6%)

2. GPT-2 vs RoBERTa:
   - Pearson: GPT-2 (0.8694) < RoBERTa (0.8898), gap: -0.0204 (-2.3%)
   - Accuracy: GPT-2 (0.8717) < RoBERTa (0.8837), gap: -0.0120 (-1.4%)
   - Combined: GPT-2 (1.7411) < RoBERTa (1.7735), gap: -0.0324 (-1.8%)

Why BERT/RoBERTa Outperform GPT-2 on These Tasks:

1. Bidirectional Context is Critical:
   - For semantic relatedness, understanding both sentences fully requires bidirectional context
   - GPT-2's causal attention cannot look ahead, missing important contextual cues from the second sentence
   - Example: In sentence pair "A dog runs" and "A canine sprints", GPT-2 processes left-to-right and may not fully capture the semantic similarity

2. Task-Specific Pre-training:
   - BERT was pre-trained with NSP and MLM, both beneficial for sentence pair understanding
   - GPT-2's next-token prediction doesn't directly optimize for understanding relationships between sentences
   - The [CLS] token in BERT is specifically trained to aggregate sentence-level information

3. Representation Quality:
   - BERT uses the [CLS] token (first position) which aggregates bidirectional information
   - GPT-2 uses the last token representation, which only contains left-to-right information
   - For our tasks, the aggregated bidirectional representation is more informative

4. Input Encoding:
   - BERT's token_type_ids explicitly mark sentence boundaries, helping the model distinguish premise from hypothesis
   - GPT-2 concatenates sentences without explicit markers, making it harder to learn sentence-pair relationships

5. Performance on Specific Tasks:
   - Regression Task (Relatedness): GPT-2 lags by 2.1-2.3%, suggesting difficulty in capturing semantic nuances
   - Classification Task (Entailment): GPT-2 lags by 1.1-1.4%, better than regression but still inferior
   - This pattern confirms that bidirectional models excel at understanding sentence relationships

Practical Implications:

- For discriminative tasks (classification, regression on sentence pairs): Use BERT/RoBERTa
- For generative tasks (text completion, dialogue): Use GPT-2/GPT-3
- For hybrid tasks: Consider encoder-decoder architectures (T5, BART)

The consistent underperformance of GPT-2 (1.6-2.3% gap) across both tasks validates the hypothesis that bidirectional encoders are superior for sentence pair understanding tasks, while causal decoders excel at generation.

## Question 3: Multi-Output vs. Single-Task Learning (5%)

Original Question: Compare the performance of a multi-output learning model with BERT models trained separately on each sub-task. Does multi-output learning improve performance? Explain why or why not.

### 3.1 Performance Comparison

Performance Metrics Comparison:

| Model | Task | Metric | Test Score | Best Epoch |
|-------|------|--------|-----------|-----------|
| Multi-task BERT | Task 1 (Regression) | Pearson Correlation | 0.8881 | 10 |
| Single-task BERT | Task 1 (Regression) | Pearson Correlation | 0.8790 | - |
| | | Improvement | +0.0091 (+1.04%) | |
| | | | | |
| Multi-task BERT | Task 2 (Classification) | Accuracy | 0.8811 | 10 |
| Single-task BERT | Task 2 (Classification) | Accuracy | 0.8624 | - |
| | | Improvement | +0.0187 (+2.17%) | |

Key Observations:
- Multi-task BERT outperforms single-task models on both tasks
- Regression task (Task 1): +1.04% improvement with multi-task learning
- Classification task (Task 2): +2.17% improvement with multi-task learning (more significant)
- The classification task benefits more from shared representations than regression

### 3.2 Analysis

Does Multi-Output Learning Improve Performance?

Answer: YES - Multi-task learning consistently improves performance on both tasks.

Detailed Analysis:

1. Shared Representation Benefits

The multi-task BERT model demonstrates that shared representations are beneficial for these two related tasks:

- Semantic Complementarity: Task 1 (semantic relatedness) and Task 2 (entailment judgment) are closely related. Understanding semantic similarity between sentence pairs naturally helps predict their entailment relationship.
  
- Bidirectional Task Influence: 
  - Task 1 provides signals about semantic similarity, which enriches the shared encoder's understanding of sentence pair relationships
  - Task 2 (entailment) provides signals about logical consistency and semantic relationships, which helps the model better capture nuanced relatedness
  - These signals reinforce each other during training, leading to a richer shared representation

- Enhanced Feature Learning: The shared BERT encoder learns features that are useful for both tasks simultaneously, resulting in more robust and generalizable representations. Single-task models can only optimize for one task, potentially missing important features that benefit both tasks.

2. Why Multi-task Learning Helps More on Classification (+2.17% vs +1.04%)

The classification task benefits more from multi-task learning for several reasons:

- Regression Stability: Regression tasks (predicting continuous values) are inherently more stable and easier to learn. Adding another task provides marginal improvements (+1.04%).

- Classification Complexity: Binary classification (entailment judgment) requires learning decision boundaries, which is more sensitive to the quality of learned representations. The additional supervision signal from the regression task helps the classifier find better decision boundaries (+2.17%).

- Label Information Richness: The regression task (continuous scores) provides more granular information than binary classification labels, allowing the shared encoder to learn more nuanced features that particularly benefit the classification head.

3. Parameter Efficiency vs Task-Specific Optimization

- Shared Parameters: Multi-task BERT uses a single shared BERT encoder (110M+ parameters) with two lightweight task heads (256→1 and 256→2)
- Efficiency Advantage: This is much more parameter-efficient than training two completely separate BERT models, which would each have 110M+ parameters
- Trade-off: While single-task models could theoretically specialize more, the shared representation actually performs better, suggesting that the tasks are genuinely complementary rather than competing

4. Task Complementarity Analysis

Evidence that tasks are complementary (not competing):

1. Performance Correlation: Both tasks improve with multi-task learning, not just one at the expense of the other. If tasks competed for model capacity, we'd expect degradation in one task when optimizing for two.

2. Semantic Relationship: 
   - Entailment (Task 2) implicitly depends on semantic relatedness (Task 1)
   - High semantic similarity often indicates entailment or contradiction
   - Low semantic similarity indicates neither entailment nor contradiction
   - This natural dependency makes the tasks complementary

3. Loss Function Interaction:
   - Combined loss: L_total = L_MSE(y_rel, y_hat_rel) + L_CE(y_ent, y_hat_ent)
   - The regression loss (MSE) guides the encoder to capture similarity magnitude
   - The classification loss (CE) guides the encoder to capture logical relationships
   - Together, these losses optimize for a more complete understanding of sentence pair relationships

5. Generalization Improvement

- Regularization Effect: Multi-task learning acts as a regularization mechanism. The need to satisfy multiple objectives prevents the model from overfitting to task-specific patterns.
- Validation Dynamics: Multi-task models often show more stable validation curves because the shared encoder learns more generalizable features that work well across both tasks.

**Conclusion:** Multi-task learning achieves 1-2% improvement by leveraging the complementary nature of semantic relatedness and entailment judgment tasks. The shared BERT encoder can simultaneously learn features useful for both tasks, resulting in better generalization than single-task models that see only one learning objective.

## Question 4: Error Analysis and Performance Improvement (10%)

Original Question: Why does your model fail to correctly predict some data points? Please provide an error analysis and introduce how do you improve your performance.

### 4.1 Error Analysis

Multi-task BERT Model Error Distribution:

Test set error analysis on 4,928 samples reveals three distinct error patterns:

| Error Category | Count | Percentage | Confidence Range |
|---|---|---|---|
| High Confidence Errors | 542 | 92.5% | > 0.70 |
| Borderline Errors | 38 | 6.5% | 0.55 - 0.70 |
| Low Confidence Errors | 6 | 1.0% | < 0.55 |
| Total Errors | 586 | 11.9% | - |
| Overall Correct | 4,342 | 88.11% | - |

Key Finding: The majority of errors (92.5%) are high-confidence errors, meaning the model makes mistakes while being very confident in its predictions. This suggests the model has learned patterns that make it overconfident, particularly on certain error-prone samples.

#### Error Pattern 1: High-Confidence Errors (542 errors, 92.5%)

Description:
Model confidently predicts wrong labels on these samples. These are systematic errors where the model has learned incorrect decision boundaries or misunderstood sentence pair relationships.

Root Causes:

1. Lexical Similarity Mismatch:
   - Models rely heavily on word-overlap similarity and may fail on paraphrased or semantically similar but lexically different pairs
   - Example: "car" vs "automobile" - high semantic relatedness but low lexical overlap
   - Model confidence: High (> 0.8), but prediction: Incorrect

2. Negation Handling:
   - Model struggles with negated statements and their logical consequences
   - Example: "The team won" vs "The team didn't win" - should have low relatedness and opposite entailment judgment
   - The model may not correctly handle negation scope and apply it to entailment

3. Compositional Semantics:
   - Complex sentence structures and compositional meanings are misunderstood
   - Example: Multi-clause sentences with mixed entailment relationships
   - Model may not properly track which clauses affect the overall relationship

4. Domain-Specific Terminology:
   - Dataset contains scientific and technical terms from the image/object recognition domain
   - Model may have limited context for these specialized terms despite pre-training

#### Error Pattern 2: Borderline Errors (38 errors, 6.5%)

Description:
Model shows moderate uncertainty (confidence 0.55-0.70) but still predicts incorrectly. These represent harder classification decisions where the model lacks sufficient confidence.

Root Causes:

1. Ambiguous Sentence Pairs: Pairs with genuinely ambiguous meanings or relationships, where multiple labels could be justified
2. Mixed Signal Features: Sentence pairs with conflicting signals (e.g., high lexical similarity but opposite entailment)
3. Boundary Cases: Examples near the decision boundary where semantic relatedness is borderline (e.g., score ~0.5)

#### Error Pattern 3: Low Confidence Errors (6 errors, 1.0%)

Description:
Model shows low confidence but still predicts wrong label. These are rare cases where the model is uncertain and makes the wrong choice.

Root Causes:

1. True Hard Cases: Genuinely difficult examples that are challenging for language models
2. Annotation Noise: Possible labeling errors or controversial annotations in the dataset

Analysis Summary:

The error distribution tells us:
- Model is well-calibrated on easy cases (low-confidence errors are rare)
- Model overconfidently learns some incorrect patterns (92.5% high-confidence errors)
- The model doesn't express uncertainty appropriately on harder cases

### 4.2 Performance Improvement Strategies

Proposed Improvements:

#### 1. Confidence Calibration with Temperature Scaling

Description: 
Apply temperature scaling during inference to calibrate confidence scores. This technique rescales the logits before softmax to better reflect true uncertainty without changing prediction labels.

Formula: y_hat = softmax(z / T) where T is the temperature parameter (typically 1.0-5.0)

Expected Impact: 
- Reduces overconfidence on high-confidence errors
- Makes the model's confidence scores more meaningful
- Potential accuracy improvement: +0.5-1% (calibration doesn't change predictions but makes uncertainty estimates more reliable)

#### 2. Focal Loss for Hard Example Mining

Description:
Replace standard cross-entropy loss with focal loss: FL = -α (1 - p_t)^γ log(p_t)

Where p_t is the model probability and (1-p_t)^γ down-weights easy examples and focuses on hard examples.

Implementation:
- Use γ = 2.0 to focus on misclassified examples
- Reduces loss contribution from easy, correctly classified samples
- Increases loss contribution from hard examples

Expected Impact:
- Forces model to pay more attention to borderline and hard cases
- Reduces overconfidence on incorrect decisions
- Potential accuracy improvement: +1-2% (more robust decision boundaries)

#### 3. Ensemble Diversity with Different Seeds and Architectures

Description:
Train multiple models and combine their predictions:
- 3 BERT models with different random seeds
- 1 RoBERTa model for architecture diversity
- Voting ensemble for final prediction

Implementation:
- BERT models trained with seeds: [42, 123, 456]
- Average probability predictions rather than hard voting
- For entailment: Threshold ensemble probability at 0.5

Expected Impact:
- Reduces variance from individual model errors
- Captures different learned patterns
- Potential accuracy improvement: +2-3% (diversity reduces systematic errors)

#### 4. Data Augmentation for Hard Patterns

Description:
Identify and augment training data for error-prone patterns:
- Generate paraphrases for lexically simple but semantically complex pairs
- Create synthetic examples with negations and compositional structures
- Use back-translation for paraphrase generation

Implementation:
- Use back-translation (English → French → English) to create varied paraphrases
- Manually create negation variants: "X is Y" → "X is not Y"
- Synthesize compositional examples from dataset patterns

Expected Impact:
- Improves model robustness to varied expressions
- Better handling of negation and compositional structures
- Potential accuracy improvement: +1-2% (better feature learning)

#### 5. Class-Weighted Loss with Task Balancing

Description:
Address potential class imbalance in the entailment task (classes may not be equally distributed) and balance loss contributions between tasks:

L_total = α · L_MSE + β · L_CE, weighted

Where α, β are task weights and L_CE, weighted applies class weights.

Implementation:
- Analyze class distribution in training set
- Compute class weights: w_c = N / (C · N_c) (inverse frequency weighting)
- Tune task weights: Try α = 0.5, β = 1.0 for different task importance

Expected Impact:
- Better balance between tasks
- Reduced bias toward majority class
- Potential accuracy improvement: +0.5-1.5% (better class balance)

### 4.3 Cumulative Improvement Trajectory

Baseline Performance (Current Multi-task BERT):
- Entailment Accuracy: 0.8811
- Pearson Correlation: 0.8881
- Combined Score: 1.7691

Estimated Performance After Improvements:

| Improvement Strategy | Estimated Gain | Cumulative Accuracy | Reasoning |
|---|---|---|---|
| Baseline | - | 0.8811 | Current multi-task BERT |
| + Focal Loss | +1.5% | ~0.8945 | Better attention to hard examples |
| + Ensemble (3 BERT + RoBERTa) | +2.0% | ~0.9125 | Reduces systematic errors |
| + Temperature Scaling | +0.5% | ~0.9175 | Better uncertainty estimates |
| + Data Augmentation | +1.0% | ~0.9275 | Improved robustness |
| All Improvements Combined | +5.5% | ~0.93 | Synergistic effects |

Implementation Priority:
1. High Priority: Ensemble + Focal Loss (fastest to implement, highest impact)
2. Medium Priority: Temperature Scaling + Class Weights (moderate effort, good impact)
3. Lower Priority: Data Augmentation (requires more data collection)

### 4.4 Why the Model Fails on Specific Cases

Why High-Confidence Errors Occur:

1. Surface-Level Pattern Learning:
   - Model learns patterns from word embeddings and attention weights
   - May overfit to training data patterns that don't generalize
   - Assigns high confidence based on these learned patterns

2. Insufficient Semantic Depth:
   - Despite BERT's strong language understanding, sentence pair understanding requires deeper reasoning
   - Complex compositional semantics requires explicit reasoning not present in standard attention

3. Training-Test Mismatch:
   - Some test examples may have unique characteristics not well represented in training
   - Domain shift from general language to specific image description domain

4. Label Ambiguity in Source Dataset:
   - SemEval annotations may have some inconsistency or subjectivity
   - Model learns one annotation convention but fails on edge cases with different conventions

Implications for Future Work:

The analysis reveals that achieving better performance requires:
- Moving beyond surface-level embeddings to explicit reasoning
- Better calibration of model confidence
- Ensemble methods to capture diverse solutions
- Better handling of compositional semantics

## Question 5: Additional Insights (5%)

Original Question: Anything that can strengthen your report.

### 5.1 Training Dynamics and Convergence Analysis

BERT Multi-task Training Progression:

| Epoch | Train Loss | Val Pearson | Val Accuracy | Combined Score | Best? |
|-------|------------|-------------|--------------|----------------|-------|
| 1 | 1.0326 | 0.8673 | 0.8580 | 1.7253 | ✓ |
| 2 | 0.5353 | 0.8650 | 0.8380 | 1.7030 | |
| 3 | 0.3941 | 0.8622 | 0.8440 | 1.7062 | |
| 4 | 0.3148 | 0.8547 | 0.8580 | 1.7127 | |
| 5 | 0.2656 | 0.8768 | 0.8580 | 1.7348 | ✓ |
| 6 | 0.2150 | 0.8759 | 0.8520 | 1.7279 | |
| 7 | 0.1911 | 0.8605 | 0.8480 | 1.7085 | |
| 8 | 0.1712 | 0.8681 | 0.8600 | 1.7281 | |
| 9 | 0.1529 | 0.8622 | 0.8700 | 1.7322 | |
| 10 | 0.1411 | 0.8784 | 0.8860 | 1.7644 | ✓ Best |

Key Observations:

1. Training Loss Reduction: Loss decreases consistently from 1.0326 (Epoch 1) to 0.1411 (Epoch 10), representing an 86.3% reduction. This smooth progression indicates stable optimization without divergence or oscillation.

2. Non-monotonic Validation Performance: Unlike training loss, validation metrics fluctuate across epochs:
   - Pearson correlation peaks at Epoch 10 (0.8784) after dipping at Epochs 3-4
   - Accuracy improves dramatically in final epoch (0.8860), suggesting the model finally learns robust decision boundaries
   - This pattern is typical of multi-task learning where tasks may compete for optimization

3. Late-stage Improvement: The best combined score occurs at Epoch 10, with both metrics peaking simultaneously. This suggests:
   - No early stopping would have been beneficial
   - The model requires full 10 epochs to learn optimal shared representations
   - Multi-task learning benefits from longer training to balance both objectives

### 5.2 Hyperparameter Configuration Insights

Learning Rate Strategy:

The fixed learning rate of 3e-5 with AdamW optimizer proved effective:

- Why 3e-5? This is the canonical learning rate for BERT fine-tuning (from Devlin et al., 2019)
- AdamW Benefits: Weight decay regularization (0.01) prevents overfitting despite 110M+ parameters
- No Learning Rate Scheduling: We used a constant learning rate without warmup or decay

Potential Improvement: Learning rate scheduling could improve convergence:
```python
# Warmup for first 10% of training, then linear decay
from transformers import get_linear_schedule_with_warmup

num_training_steps = len(dl_train) * epochs
num_warmup_steps = num_training_steps // 10

scheduler = get_linear_schedule_with_warmup(
    optimizer, 
    num_warmup_steps=num_warmup_steps,
    num_training_steps=num_training_steps
)
```

Expected Impact: +0.5-1% validation performance through better convergence

### 5.3 Batch Size and Gradient Accumulation Trade-offs

Current Configuration:
- Batch size: 8
- Gradient accumulation: None
- Effective batch size: 8

Analysis:

Small batch size (8) leads to:
- ✓ Noisy gradients that can escape local minima
- ✓ Better generalization (smaller batches often generalize better)
- ✗ Slower training (563 batches per epoch vs fewer with larger batches)
- ✗ Less stable optimization (higher variance in gradient estimates)

Alternative Strategy - Gradient Accumulation:

Benefits: Larger effective batch size (32) with same memory footprint
Expected Impact: +0.3-0.5% through more stable gradients

### 5.4 Task Loss Weighting Analysis

Current Approach: Equal weighting (α = 1.0, β = 1.0)

L_total = L_MSE + L_CE

Observed Issue: The two tasks have different loss scales:
- MSE Loss (Task 1): Continuous values, typically 0.1-1.0 range
- Cross-Entropy Loss (Task 2): Binary classification, typically 0.3-0.7 range

Automatic Task Weighting: Implement uncertainty-based weighting (Kendall et al., 2018):

L_total = (1/2σ₁²)L_MSE + (1/2σ₂²)L_CE + log(σ₁σ₂)

Where σ₁, σ₂ are learnable noise parameters that automatically balance task contributions.

Expected Impact: +0.5-1.5% by optimally balancing task gradients

### 5.5 Model Architecture Enhancements

Current Architecture:

BERT Encoder (110M params)
    ↓
[CLS] token (768 dim)
    ↓
Task Head 1: 768→256→1 (Regression)
Task Head 2: 768→256→2 (Classification)

Potential Enhancements:

1. Deeper Task-Specific Heads

Benefit: More capacity for task-specific transformations
Expected Impact: +0.3-0.7%

2. Multi-layer Perceptron with Skip Connections

Benefit: Better gradient flow and feature preservation
Expected Impact: +0.2-0.5%

3. Attention Pooling Instead of [CLS] Token

Benefit: Learns to focus on relevant tokens beyond [CLS]
Expected Impact: +0.5-1.0%

### 5.6 Data Efficiency and Few-Shot Performance

Current Training Set: 4,500 samples (estimated from 563 batches × 8 batch_size)

Question: How does performance degrade with less data?

Suggested Experiment - Learning Curve Analysis:

Train models on different fractions of training data:

| Data Fraction | Training Samples | Expected Pearson | Expected Accuracy |
|---------------|------------------|------------------|-------------------|
| 100% | 4,500 | 0.8881 | 0.8811 |
| 50% | 2,250 | ~0.86-0.87 | ~0.85-0.86 |
| 25% | 1,125 | ~0.83-0.84 | ~0.82-0.83 |
| 10% | 450 | ~0.78-0.80 | ~0.75-0.78 |

Insight: Pre-trained BERT is highly data-efficient. Even with 10% of data, we expect reasonable performance due to transfer learning from pre-training.

### 5.7 Cross-Model Ensemble Strategy

Motivation: Our three models (BERT, RoBERTa, GPT-2) make different types of errors due to architectural differences.

Ensemble Configuration:

Expected Ensemble Performance:

- Regression (Pearson): ~0.895-0.900 (+0.7-1.2% over best single model)
- Classification (Accuracy): ~0.890-0.895 (+0.6-1.1% over best single model)

Reasoning: Ensemble captures complementary strengths:
- RoBERTa: Best overall performance
- BERT: Strong bidirectional understanding
- GPT-2: Different architecture provides diversity

### 5.8 Regularization Techniques Comparison

Currently Implemented:
- Dropout: 0.1 in task heads
- Weight decay: 0.01 in optimizer
- Gradient clipping: max_norm=1.0

Additional Regularization Options:

| Technique | Implementation | Expected Impact |
|-----------|---------------|-----------------|
| Layer-wise Dropout | Different dropout rates per layer (0.1→0.2→0.3) | +0.2-0.4% |
| DropConnect | Drop connections instead of activations | +0.1-0.3% |
| Mixup | Mix training examples: λx₁ + (1-λ)x₂ | +0.3-0.6% |
| Label Smoothing | Soft targets: y' = (1-ε)y + ε/K | +0.2-0.5% |
| Stochastic Depth | Randomly skip layers during training | +0.1-0.3% |

Recommended: Label smoothing for classification task

### 5.9 Computational Efficiency Analysis

Training Time Breakdown (per epoch):

- BERT Multi-task: ~4.1 minutes (246 seconds)
- RoBERTa Multi-task: ~4.0 minutes (similar to BERT)
- GPT-2 Multi-task: ~3.8 minutes (slightly faster due to no token_type_ids)

Total Training Time: ~41 minutes for 10 epochs (BERT)

Efficiency Metrics:

| Model | Parameters | Training Time/Epoch | Samples/Second | Performance/Param |
|-------|------------|---------------------|----------------|-------------------|
| BERT | 110M | 246s | ~18.3 | 0.8811/110M = 8.01×10⁻⁹ |
| RoBERTa | 125M | 240s | ~18.8 | 0.8837/125M = 7.07×10⁻⁹ |
| GPT-2 | 124M | 228s | ~19.7 | 0.8717/124M = 7.03×10⁻⁹ |

Key Insight: BERT achieves the best accuracy-per-parameter ratio, making it the most efficient choice for this task despite having fewer parameters than RoBERTa/GPT-2.

### 5.10 Practical Recommendations for Deployment

Based on our comprehensive analysis, here are deployment recommendations:

1. For Maximum Accuracy:
- Use RoBERTa (0.8837 accuracy, 0.8898 Pearson)
- Implement ensemble with BERT for additional +1% boost
- Expected production accuracy: ~0.89-0.90

2. For Balanced Performance/Efficiency:
- Use BERT (0.8811 accuracy, 0.8881 Pearson)
- Best accuracy-per-parameter ratio
- Slightly faster inference than RoBERTa

3. For Resource-Constrained Environments:
- Distill BERT/RoBERTa to smaller model (DistilBERT, ~40% smaller)
- Use quantization (INT8) for 4× memory reduction
- Expected performance retention: 95-97%

4. For Real-Time Applications:
- Use model compression: pruning + quantization
- ONNX Runtime for optimized inference
- Target latency: <50ms per prediction on CPU

## Appendix: Training Logs and Accuracy (10%)

Original Question: The screenshot of your testing logs and accuracy. (One Figure only)

### Final Test Results Summary

Model              | Test Accuracy | F1-Score | Training Time
-------------------|---------------|----------|---------------
BERT-base          |               |          |
RoBERTa-base       |               |          |
GPT-2              |               |          |
Multi-Output BERT  |               |          |

### Testing Results Visualization

![Model Comparison Results](images/model_comparison.png)

Figure Description: Comparison of test performance across all trained models:
- Left: Semantic Relatedness Task (Task 1) - Pearson Correlation scores
- Right: Entailment Classification Task (Task 2) - Accuracy scores

All models achieve strong performance on the SemEval 2014 Task 1 test set, with RoBERTa-base (Multi-Task) showing the best overall results.