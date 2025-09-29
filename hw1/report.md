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
    - Decompress and concatenate into `wiki_texts_combined.txt`, then sample approximately 10% of articles into `wiki_texts_sampled.txt`.
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

### Q3. What is the performance for different categories or sub-categories when trained on different corpora? (15%)
#### 3.1 Present your results. (5%)
Answer:

#### 3.2 Introduce the corpus you selected and explain the differences between the Wikipedia corpus and your corpus. (including data size, topic difference, structural difference … ) (5%)
Answer:

#### 3.3 Explain why the accuracy increases or decreases. (5%)
Answer:

### Q4. Select a few words and use their embeddings to retrieve the five most similar words and present the results. What do you observe?  (10%)
Answer:

### Q5. Anything that can strengthen your report.  (5%)
Answer:
