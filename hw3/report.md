# Assignment 3 Report: Sentiment Analysis with Transformer Models

> **Remark:** For ease of grading, data is presented in textual form rather than as images.

---

## Question 1: RoBERTa-base Model Training (10%)

**Question:** Train a RoBERTa-base model on the same dataset and report the performance of both BERT-base and RoBERTa-base models.

### 1.1 Performance Results

**BERT-base Model Performance:**
- Training Accuracy: 
- Validation Accuracy: 
- Test Accuracy: 
- F1 Score: 

**RoBERTa-base Model Performance:**
- Training Accuracy: 
- Validation Accuracy: 
- Test Accuracy: 
- F1 Score: 

### 1.2 Differences Between BERT and RoBERTa (5%)

**Question:** Discuss the main differences between BERT and RoBERTa, and explain how these differences may affect performance.

**Key Architectural and Training Differences:**

1. **Training Objective:**
   - BERT uses Next Sentence Prediction (NSP) task alongside Masked Language Modeling (MLM)
   - RoBERTa removes NSP and focuses only on dynamic MLM

2. **Training Data:**
   - BERT was trained on BookCorpus and English Wikipedia (~16GB)
   - RoBERTa was trained on 160GB of text including additional datasets

3. **Training Duration:**
   - BERT trained for 1M steps
   - RoBERTa trained for significantly longer (500K steps with larger batches)

4. **Dynamic Masking:**
   - BERT uses static masking (same mask for each epoch)
   - RoBERTa uses dynamic masking (different masks each time)

5. **Byte-Pair Encoding:**
   - BERT uses WordPiece tokenization
   - RoBERTa uses BPE with a larger vocabulary (50K vs 30K tokens)

**Impact on Performance:**
- RoBERTa's longer training with more data leads to better language understanding
- Dynamic masking provides more robust representations
- Removing NSP allows the model to focus on better sequence representations
- Larger vocabulary in RoBERTa handles rare words more effectively

---

## Question 2: GPT-2 Model Training (10%)

**Question:** Train a GPT-2 model on the same dataset and evaluate its performance.

### 2.1 Performance Results

**GPT-2 Model Performance:**
- Training Accuracy: 
- Validation Accuracy: 
- Test Accuracy: 
- F1 Score: 

### 2.2 Differences Between BERT and GPT-2 (5%)

**Question:** What are the main difference of BERT and GPT2? Discuss the main differences between BERT and GPT-2, and analyze how these differences influence their performance.

**Key Architectural and Training Differences:**

1. **Model Architecture:**
   - BERT: Bidirectional encoder using Transformer encoder blocks
   - GPT-2: Unidirectional decoder using Transformer decoder blocks

2. **Attention Mechanism:**
   - BERT: Full bidirectional attention (can see entire sequence)
   - GPT-2: Causal/masked attention (can only see previous tokens)

3. **Training Objective:**
   - BERT: Masked Language Modeling (MLM) - predict masked tokens
   - GPT-2: Causal Language Modeling (CLM) - predict next token

4. **Pre-training Task:**
   - BERT: Designed for understanding tasks (classification, NER, QA)
   - GPT-2: Designed for generation tasks (text completion, generation)

5. **Context Utilization:**
   - BERT: Uses context from both directions simultaneously
   - GPT-2: Uses only left-to-right context

**Impact on Performance for Sentiment Analysis:**
- BERT's bidirectional nature is better suited for classification tasks as it can leverage full context
- GPT-2's causal architecture may miss important context from future tokens
- BERT was explicitly designed for discriminative tasks like sentiment analysis
- GPT-2 requires adaptation (e.g., using final token representation) for classification
- Expected: BERT/RoBERTa should outperform GPT-2 on this task

---

## Question 3: Multi-Output vs. Single-Task Learning (5%)

**Question:** Compare the performance of a multi-output learning model with BERT models trained separately on each sub-task. Does multi-output learning improve performance? Explain why or why not.

### 3.1 Performance Comparison

**Multi-Output Learning Model:**
- Overall Accuracy: 
- Sub-task 1 Accuracy: 
- Sub-task 2 Accuracy: 
- Sub-task 3 Accuracy: 

**Single-Task Models:**
- Model 1 (Sub-task 1) Accuracy: 
- Model 2 (Sub-task 2) Accuracy: 
- Model 3 (Sub-task 3) Accuracy: 

### 3.2 Analysis

**Does Multi-Output Learning Improve Performance?**

[Your analysis here - consider:]
- Whether shared representations help or hurt performance
- Task relationships and how they influence each other
- Parameter efficiency vs. task-specific optimization
- Whether tasks are complementary or competing

---

## Question 4: Error Analysis and Performance Improvement (10%)

**Question:** Why does your model fail to correctly predict some data points? Please provide an error analysis and introduce how do you improve your performance.

### 4.1 Error Analysis

**Common Error Patterns:**

1. **Error Type 1:**
   - Description: 
   - Example: 
   - Frequency: 

2. **Error Type 2:**
   - Description: 
   - Example: 
   - Frequency: 

3. **Error Type 3:**
   - Description: 
   - Example: 
   - Frequency: 

### 4.2 Performance Improvement Strategies

**Implemented Improvements:**

1. **Strategy 1:**
   - Description: 
   - Impact: 

2. **Strategy 2:**
   - Description: 
   - Impact: 

3. **Strategy 3:**
   - Description: 
   - Impact: 

**Results After Improvements:**
- Baseline Accuracy: 
- Improved Accuracy: 
- Performance Gain: 

---

## Question 5: Additional Insights (5%)

**Question:** Anything that can strengthen your report.

### 5.1 Additional Experiments and Observations

[Your additional insights here - consider:]
- Hyperparameter tuning results
- Ensemble methods
- Data augmentation techniques
- Learning rate schedules
- Other architectural modifications

---

## Appendix: Training Logs and Accuracy (10%)

**Question:** The screenshot of your testing logs and accuracy. (One Figure only)

### Final Test Results Summary

```
Model              | Test Accuracy | F1-Score | Training Time
-------------------|---------------|----------|---------------
BERT-base          |               |          |
RoBERTa-base       |               |          |
GPT-2              |               |          |
Multi-Output BERT  |               |          |
```

### Training Visualization

[Include your training logs screenshot here - showing loss curves, accuracy progression, and final metrics]