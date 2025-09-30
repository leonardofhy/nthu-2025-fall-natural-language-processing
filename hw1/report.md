## Assignment 1 Report

### Student Info

- Name: 胡皓雍
- Institution (school): National Taiwan University
- Student ID: R14942146
- Platform (Colab/Kaggle/Local): Local
- Python version: 3.12
- Operating system: macOS
- CPU: 8 核心 CPU 配備 4 個效能核心與 4 個節能核心
- GPU requirement: 8 核心 GPU、10 核心 GPU

### Q1. Which embedding model do you use? What are the pre-processing steps? What are the hyperparameter settings? (5%)

Answer:

- **Embedding models**
  - **Pre-trained**: `glove-wiki-gigaword-100` (100-dim GloVe via `gensim.downloader.load`).
  - **Custom**: `gensim.models.Word2Vec` (skip-gram) trained on sampled Wikipedia text.
- **Pre-processing steps**
  - **Google analogy dataset**:
    - Parse lines; `:` lines denote subcategories. The first five subcategories are labeled “Semantic,” the rest “Syntactic.”
    - Lowercase tokens before lookup; save to `questions-words.csv`.
  - **Wikipedia corpus (training)**:
    - Use pre-cleaned wiki parts (cleaned with `WikiCorpus` defaults; single-character words removed).
    - Decompress and concatenate into `wiki_texts_combined.txt`, then sample **20%** of articles into `wiki_texts_sampled.txt` (using `random.random() < 0.2`).
    - Tokenize with `gensim.utils.simple_preprocess` (lowercasing; minimum token length 2), yielding one token list per article.
- **Hyperparameter settings**
  - **Pre-trained GloVe**: vector size 100 (fixed by model name).
  - **Custom Word2Vec**:
    - `vector_size=100`
    - `window=5`
    - `min_count=5`
    - `sg=1` (skip-gram)
    - `negative=10`
    - `workers=os.cpu_count()`
    - `epochs=5`
  - **Analogy inference**:
    - Use `most_similar(positive=[b, c], negative=[a], topn=1)`; skip if any of a/b/c is OOV; tokens are lowercased before lookup.

### Q2. What will the performance be like if you sample 5%, 10% and 20% of wiki text in TODO4? (10%, 3% for each)

Answer:

The performance of the custom Word2Vec model trained on different sampling rates of the Wikipedia text corpus is summarized below. The results highlight the impact of training data size on vocabulary size and analogy task accuracy:

| Sampling Rate | Vocab Size | Overall Accuracy (%) | Semantic Accuracy (%) | Syntactic Accuracy (%) |
| ------------- | ---------- | -------------------- | --------------------- | ---------------------- |
| 5%            | 450,347    | 51.88                | 64.31                 | 41.55                  |
| 10%           | 703,054    | 53.36                | 65.69                 | 43.12                  |
| 20%           | 1,081,457  | 53.83                | 65.96                 | 43.75                  |

#### Sub-Category Performance

The table below provides a detailed breakdown of accuracy for each sub-category in the Google analogy dataset. The "Improvement" column indicates the change in accuracy from 5% to 20% sampling rates. Positive values represent an increase in accuracy, while negative values indicate a decrease:

| Sub-Category                | 5% Accuracy (%) | 10% Accuracy (%) | 20% Accuracy (%) | Improvement (%) |
| --------------------------- | --------------- | ---------------- | ---------------- | --------------- |
| capital-common-countries    | 93.48           | 92.49            | 90.71            | -2.77           |
| capital-world               | 78.36           | 81.23            | 82.98            | +4.62           |
| currency                    | 11.09           | 9.12             | 11.89            | +0.81           |
| city-in-state               | 48.64           | 48.07            | 45.48            | -3.16           |
| family                      | 77.08           | 82.61            | 81.42            | +4.35           |
| gram1-adjective-to-adverb   | 11.90           | 14.52            | 18.25            | +6.35           |
| gram2-opposite              | 11.58           | 16.01            | 14.66            | +3.08           |
| gram3-comparative           | 52.03           | 47.52            | 47.60            | -4.43           |
| gram4-superlative           | 20.86           | 24.78            | 22.28            | +1.43           |
| gram5-present-participle    | 34.94           | 35.70            | 33.90            | -1.04           |
| gram6-nationality-adjective | 85.80           | 87.18            | 86.93            | +1.13           |
| gram7-past-tense            | 40.45           | 43.40            | 42.76            | +2.31           |
| gram8-plural                | 44.59           | 45.57            | 51.35            | +6.76           |
| gram9-plural-verbs          | 37.93           | 41.72            | 44.48            | +6.55           |

#### Observations

- **Overall Trends**: Increasing the sampling rate from 5% to 20% improves overall accuracy, with diminishing returns as the corpus size grows.

- **Semantic vs. Syntactic**: Semantic categories generally achieve higher accuracy than syntactic ones, reflecting the model's stronger performance on semantic relationships.

- **Sub-Category Variations**: Some sub-categories, such as "gram8-plural" and "gram9-plural-verbs," show significant improvements with larger training data, while others, like "capital-common-countries," experience slight declines due to overfitting or noise in the data.

- **Clarification on Improvement Column**: The "Improvement" column in the sub-category table quantifies the difference in accuracy between the 5% and 20% sampling rates. It helps identify which sub-categories benefit the most from increased training data and which ones may face challenges such as overfitting or data noise.

### Q3. What is the performance for different categories or sub-categories when trained on different corpora? (15%)

#### 3.1 Present your results. (5%)

#### 3.2 Introduce the corpus you selected and explain the differences between the Wikipedia corpus and your corpus. (including data size, topic difference, structural difference … ) (5%)

#### 3.3 Explain why the accuracy increases or decreases. (5%)

### Q4. Select a few words and use their embeddings to retrieve the five most similar words and present the results. What do you observe? (10%)

### Q5. Anything that can strengthen your report. (5%)
