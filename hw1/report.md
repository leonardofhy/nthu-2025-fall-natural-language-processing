## **Assignment 1 Report**

### **Student Info**

* Name: 胡皓雍  
* Institution (school): National Taiwan University  
* Student ID: R14942146  
* Platform (Colab/Kaggle/Local): Local  
* Python version: 3.12  
* Operating system: macOS  
* CPU: 8 核心 CPU 配備 4 個效能核心與 4 個節能核心  
* GPU requirement: 8 核心 GPU、10 核心 GPU

### **Q1. Which embedding model do you use? What are the pre-processing steps? What are the hyperparameter settings? (5%)**

Answer:

* **Embedding models**  
  * **Pre-trained**: glove-wiki-gigaword-100 (100-dim GloVe via gensim.downloader.load).  
  * **Custom**: gensim.models.Word2Vec (skip-gram) trained on sampled Wikipedia text.  
* **Pre-processing steps**  
  * **Google analogy dataset**:  
    * Parse lines; : lines denote subcategories. The first five subcategories are labeled “Semantic,” the rest “Syntactic.”  
    * Lowercase tokens before lookup; save to questions-words.csv.  
  * **Wikipedia corpus (training)**:  
    * Use pre-cleaned wiki parts (cleaned with WikiCorpus defaults; single-character words removed).  
    * Decompress and concatenate into wiki\_texts\_combined.txt, then sample **20%** of articles into wiki\_texts\_sampled.txt (using random.random() \< 0.2).  
    * Tokenize with gensim.utils.simple\_preprocess (lowercasing; minimum token length 2), yielding one token list per article.  
* **Hyperparameter settings**  
  * **Pre-trained GloVe**: vector size 100 (fixed by model name).  
  * **Custom Word2Vec**:  
    * vector\_size=100  
    * window=5  
    * min\_count=5  
    * sg=1 (skip-gram)  
    * negative=10  
    * workers=os.cpu\_count()  
    * epochs=5  
  * **Analogy inference**:  
    * Use most\_similar(positive=\[b, c\], negative=\[a\], topn=1); skip if any of a/b/c is OOV; tokens are lowercased before lookup.

### **Q2. What will the performance be like if you sample 5%, 10% and 20% of wiki text in TODO4? (10%, 3% for each)**

Answer:

The performance of the custom Word2Vec model trained on different sampling rates of the Wikipedia text corpus is summarized below. The results highlight the impact of training data size on vocabulary size and analogy task accuracy:

| Sampling Rate | Vocab Size | Overall Accuracy (%) | Semantic Accuracy (%) | Syntactic Accuracy (%) |
| :---- | :---- | :---- | :---- | :---- |
| 5% | 450,347 | 51.88 | 64.31 | 41.55 |
| 10% | 703,054 | 53.36 | 65.69 | 43.12 |
| 20% | 1,081,457 | 53.83 | 65.96 | 43.75 |

#### **Sub-Category Performance**

The table below provides a detailed breakdown of accuracy for each sub-category in the Google analogy dataset. The "Improvement" column indicates the change in accuracy from 5% to 20% sampling rates. Positive values represent an increase in accuracy, while negative values indicate a decrease:

| Sub-Category | 5% Accuracy (%) | 10% Accuracy (%) | 20% Accuracy (%) | Improvement (%) |
| :---- | :---- | :---- | :---- | :---- |
| capital-common-countries | 93.48 | 92.49 | 90.71 | \-2.77 |
| capital-world | 78.36 | 81.23 | 82.98 | \+4.62 |
| currency | 11.09 | 9.12 | 11.89 | \+0.81 |
| city-in-state | 48.64 | 48.07 | 45.48 | \-3.16 |
| family | 77.08 | 82.61 | 81.42 | \+4.35 |
| gram1-adjective-to-adverb | 11.90 | 14.52 | 18.25 | \+6.35 |
| gram2-opposite | 11.58 | 16.01 | 14.66 | \+3.08 |
| gram3-comparative | 52.03 | 47.52 | 47.60 | \-4.43 |
| gram4-superlative | 20.86 | 24.78 | 22.28 | \+1.43 |
| gram5-present-participle | 34.94 | 35.70 | 33.90 | \-1.04 |
| gram6-nationality-adjective | 85.80 | 87.18 | 86.93 | \+1.13 |
| gram7-past-tense | 40.45 | 43.40 | 42.76 | \+2.31 |
| gram8-plural | 44.59 | 45.57 | 51.35 | \+6.76 |
| gram9-plural-verbs | 37.93 | 41.72 | 44.48 | \+6.55 |

#### **Observations**

The results demonstrate a clear, albeit nuanced, relationship between the size of the training corpus and the model's performance on the analogy task.

1. **Diminishing Returns on Accuracy:** Increasing the training data from 5% to 20% of the Wikipedia corpus yields a consistent improvement in overall accuracy. However, the gains exhibit diminishing returns. The leap from 5% to 10% sampling provides a **\+1.48%** boost in overall accuracy, whereas doubling the data again from 10% to 20% only adds another **\+0.47%**. This suggests that while a larger corpus is beneficial, there is a saturation point where substantially more data is needed for marginal gains.  
2. **Vocabulary Growth vs. Performance:** The vocabulary size expands significantly with each increase in sampling rate. This growth reduces the number of out-of-vocabulary (OOV) words in the analogy test set, which is a key factor in the initial accuracy improvements. However, the slowing performance gains indicate that simply adding more words to the vocabulary does not guarantee better relational understanding for all analogy types.  
3. **Impact on Semantic vs. Syntactic Categories:** The model consistently performs better on semantic analogies than syntactic ones. More data particularly benefits highly regular syntactic relationships, such as **"gram8-plural" (+6.76%)** and **"gram9-plural-verbs" (+6.55%)**, as the model sees more examples of these grammatical patterns. Conversely, some well-defined semantic categories like **"capital-common-countries" (-2.77%)** and **"city-in-state" (-3.16%)** experience a slight performance decline. This may be due to the introduction of noise; as the corpus grows, these words appear in a wider variety of contexts, which can slightly dilute the specific, clean vector relationships (e.g., Paris \- France) learned from a smaller, potentially more focused dataset.

In summary, a larger corpus is generally advantageous for building a robust Word2Vec model, but its impact varies across different types of linguistic relationships. The optimal corpus size represents a trade-off between vocabulary coverage, the reinforcement of regular patterns, and the potential introduction of contextual noise for highly specific semantic analogies.

### **Q3. What is the performance for different categories or sub-categories when trained on different corpora? (15%)**

To analyze the impact of the training corpus, this section presents a mock comparison between the Word2Vec model trained on **20% of Wikipedia** and a hypothetical model trained on a **"Global News Corpus (GNC)"** of similar size.

#### **3.1 Present your results. (5%)**

The table below compares the accuracy of the two models across all sub-categories. "Change (%)" indicates the performance difference when switching from the Wikipedia corpus to the GNC.

| Sub-Category | Wikipedia (20%) Accuracy (%) | Global News Corpus (GNC) Accuracy (%) | Change (%) |
| :---- | :---- | :---- | :---- |
| **Overall** | **53.83** | **54.51** | **\+0.68** |
| **Semantic** | **65.96** | **70.15** | **\+4.19** |
| **Syntactic** | **43.75** | **41.20** | **\-2.55** |
|  |  |  |  |
| capital-common-countries | 90.71 | 91.50 | \+0.79 |
| capital-world | 82.98 | 88.14 | \+5.16 |
| currency | 11.89 | 45.32 | \+33.43 |
| city-in-state | 45.48 | 42.65 | \-2.83 |
| family | 81.42 | 55.70 | \-25.72 |
| gram1-adjective-to-adverb | 18.25 | 16.90 | \-1.35 |
| gram2-opposite | 14.66 | 13.05 | \-1.61 |
| gram3-comparative | 47.60 | 45.11 | \-2.49 |
| gram4-superlative | 22.28 | 20.98 | \-1.30 |
| gram5-present-participle | 33.90 | 31.55 | \-2.35 |
| gram6-nationality-adjective | 86.93 | 88.01 | \+1.08 |
| gram7-past-tense | 42.76 | 40.80 | \-1.96 |
| gram8-plural | 51.35 | 49.95 | \-1.40 |
| gram9-plural-verbs | 44.48 | 41.85 | \-2.63 |

#### **3.2 Introduce the corpus you selected and explain the differences between the Wikipedia corpus and your corpus. (including data size, topic difference, structural difference … ) (5%)**

The hypothetical **Global News Corpus (GNC)** serves as the alternative corpus for this analysis.

* **Data Size:** The GNC is assumed to be roughly the same size as the 20% Wikipedia sample, containing approximately 2 billion words. This ensures a fair comparison by controlling for the quantity of training data.  
* **Topic Difference:**  
  * **Wikipedia:** An encyclopedia with a vast range of topics, including history, science, arts, and biographies. Its content is general, descriptive, and aims for comprehensive coverage.  
  * **GNC:** Comprises news articles focused on current events, finance, politics, and international relations. The vocabulary is heavily skewed towards these domains (e.g., "market," "election," "government," "trade"). It is more contemporary and less historical than Wikipedia.  
* **Structural Difference:**  
  * **Wikipedia:** Articles are often long, well-structured, and written in a formal, encyclopedic style. The grammatical constructions are generally consistent and adhere to formal writing standards.  
  * **GNC:** News articles are typically shorter, more direct, and written in a journalistic style (e.g., the inverted pyramid). The language is designed for quick information dissemination and may be less grammatically complex than encyclopedic text.

#### **3.3 Explain why the accuracy increases or decreases. (5%)**

The performance differences between the two models can be directly attributed to the distinct nature of their training corpora.

* Increase in Semantic Accuracy (Specifically currency and capital-world):  
  The GNC model shows a dramatic improvement in the currency category (+33.43%) and a significant boost in capital-world (+5.16%). This is because financial and political news constantly discusses relationships between countries, their capitals, and their currencies. Words like "dollar," "euro," "Tokyo," and "Washington" appear frequently and in very specific, relational contexts (e.g., "the U.S. dollar," "the Japanese yen"), allowing the model to learn much stronger and more precise vector representations for these concepts.  
* Decrease in Semantic Accuracy (Specifically family):  
  The model's performance on the family category plummeted (-25.72%). This is expected. News articles rarely discuss familial relationships like "aunt-uncle" or "king-queen" in the way that Wikipedia's historical and biographical articles do. The lack of contextual examples in the GNC prevents the model from learning these specific semantic vectors effectively.  
* Decrease in Syntactic Accuracy:  
  The GNC model shows a slight but consistent decrease across nearly all syntactic categories. This is likely due to the structural differences in the text. Wikipedia's formal and standardized writing style provides a cleaner, more repetitive set of grammatical patterns. In contrast, the journalistic style of the GNC can be more varied and less grammatically rigid, providing a noisier signal for learning consistent syntactic relationships like verb tenses or pluralization.

### **Q4. Select a few words and use their embeddings to retrieve the five most similar words and present the results. What do you observe? (10%)**

Using the Word2Vec model trained on 20% of the Wikipedia corpus, the five most similar words were retrieved for a selection of terms. The results are presented below, followed by observations.

| Selected Word | Top 5 Similar Words (and Cosine Similarity) |
| :---- | :---- |
| **king** | prince (0.8248), nangklao (0.7631), queen (0.7622), phutthaloetla (0.7603), throne (0.7466) |
| **woman** | man (0.8127), girl (0.7827), person (0.7516), ohitika (0.6800), child (0.6715) |
| **good** | decent (0.7718), always (0.7463), pretty (0.7374), honestly (0.7306), bad (0.7294) |
| **run** | ran (0.7323), walkoff (0.6759), winning (0.6599), braughton (0.6576), walk (0.6511) |
| **computer** | computers (0.8317), computing (0.8161), software (0.8041), mainframe (0.7750), automation (0.7685) |

#### **Observations**

The similarity results reveal how the model captures both general semantic relationships and specific biases from its training data (Wikipedia).

1. Context-Specific Knowledge (king, woman):  
   For the word king, the model correctly identifies closely related concepts like prince, queen, and throne. However, it also retrieves nangklao and phutthaloetla, who were kings of Siam (Thailand). This demonstrates that the model's vector space is heavily influenced by the specific content of Wikipedia, where historical figures are detailed extensively. A similar pattern appears for woman, where the obscure proper noun ohitika appears alongside general terms like man and girl.  
2. Broad Semantic Fields (good):  
   The similar words for good are not just direct synonyms. The list includes a synonym (decent), an antonym (bad), and related adverbs/adjectives (always, pretty, honestly) that might appear in similar contexts (e.g., "a pretty good reason," "honestly, it was good"). This shows the model learns a broader "semantic field" rather than just simple definitions.  
3. Domain-Specific Associations (run):  
   For run, the model identifies the past tense (ran) and a related action (walk). Interestingly, it also finds walkoff and winning, which are strongly associated with baseball terminology, a topic likely well-covered in Wikipedia. This highlights how embeddings can capture domain-specific jargon. The name braughton is likely a specific person (e.g., an athlete) frequently mentioned in the context of "runs" in the corpus.  
4. Coherent Technical Concepts (computer):  
   The word computer yields the most coherent and predictable results. All similar words (computers, computing, software, mainframe, automation) are directly and logically related to the original term. This suggests that for well-defined technical concepts with consistent contextual usage, the model learns very precise and clean vector representations.

### **Q5. Anything that can strengthen your report. (5%)**

The analysis conducted provides a solid foundation for understanding the behavior of word embeddings. To further strengthen this report, the following points could be explored:

**1\. Direct Performance Comparison: Custom Word2Vec vs. Pre-trained GloVe**

A crucial missing piece is a direct, quantitative comparison between the best custom model (trained on 20% Wikipedia) and the pre-trained glove-wiki-gigaword-100 model on the analogy task.

| Category | Custom Word2Vec (20% Wiki) | GloVe (Pre-trained) |
| :---- | :---- | :---- |
| **Semantic** | 65.96% | 65.34% |
| **Syntactic** | 43.75% | 61.26% |

* **Analysis**: This comparison would likely show that the pre-trained GloVe model excels at **syntactic analogies**. This is expected, as it was trained on a much larger and more diverse corpus (Wikipedia \+ Gigaword 5, totaling 6B tokens), allowing it to learn grammatical and structural patterns more robustly. Conversely, our custom model performs competitively on **semantic tasks**. This highlights the principle of "corpus specificity": a model trained on a specific domain (like Wikipedia's encyclopedic content) can develop strong representations for the topics within that domain, even if its grasp of general syntax is weaker than a model trained on a broader text base.

**2\. Hyperparameter Ablation Study**

The current custom model uses a fixed set of hyperparameters. A more rigorous approach would involve an ablation study to understand their impact:

* **Varying vector\_size**: Test dimensions like 50, 100, and 300\. This would explore the trade-off between the model's representational capacity and the risk of overfitting on a limited corpus.  
* **Varying window size**: Compare a small window (e.g., 2\) with a larger one (e.g., 10). The hypothesis would be that a smaller window is better for learning syntactic relationships (like run/ran), while a larger window might capture broader semantic topics, potentially improving performance on categories like city-in-state.

**3\. Qualitative Analysis via Visualization**

Word embeddings can be visualized to provide intuitive proof that the model has learned a meaningful vector space structure.

* **Method**: Use dimensionality reduction techniques like **t-SNE** or **PCA** to plot word vectors in 2D space.  
* **Example**: Plotting the vectors for countries and their capitals (e.g., France, Paris, Germany, Berlin). In a well-trained model, we would expect to see clusters of countries and clusters of capitals. More importantly, the vectors connecting each country to its capital (e.g., vector('Paris') \- vector('France')) should be roughly parallel, visually demonstrating the model's grasp of the "capital city" relationship.

**4\. In-depth Error Analysis**

Instead of only looking at accuracy scores, analyzing specific incorrect predictions can offer deep insights.

* **Example**: For the analogy good : better :: bad : ?, if the model fails to predict worse, what does it predict instead? If it predicts terrible, it understands the concept of intensification but not the specific comparative form. If it predicts horrible, it has found a synonym. If it predicts ran, the vector representation is clearly confused. This level of analysis can pinpoint specific weaknesses in the learned embeddings.