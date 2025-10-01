## **Assignment 1 Report**

### **Student Info**

- Name: 胡皓雍
- Institution (school): National Taiwan University
- Student ID: R14942146
- Platform (Colab/Kaggle/Local): Local
- Python version: 3.12
- Operating system: macOS
- CPU: 8 核心 CPU 配備 4 個效能核心與 4 個節能核心
- GPU requirement: 8 核心 GPU、10 核心 GPU

### **Q1. Which embedding model do you use? What are the pre-processing steps? What are the hyperparameter settings? (5%)**

Answer:

- **Embedding models**
  - **Pre-trained**: glove-wiki-gigaword-100 (100-dim GloVe via gensim.downloader.load).
  - **Custom**: gensim.models.Word2Vec (skip-gram) trained on sampled Wikipedia text.
- **Pre-processing steps**
  - **Google analogy dataset**:
    - Parse lines; : lines denote subcategories. The first five subcategories are labeled “Semantic,” the rest “Syntactic.”
    - Lowercase tokens before lookup; save to questions-words.csv.
  - **Wikipedia corpus (training)**:
    - Use pre-cleaned wiki parts (cleaned with WikiCorpus defaults; single-character words removed).
    - Decompress and concatenate into wiki_texts_combined.txt, then sample **20%** of articles into wiki_texts_sampled.txt (using random.random() \< 0.2).
    - Tokenize with gensim.utils.simple_preprocess (lowercasing; minimum token length 2), yielding one token list per article.
- **Hyperparameter settings**
  - **Pre-trained GloVe**: vector size 100 (fixed by model name).
  - **Custom Word2Vec**:
    - vector_size=100
    - window=5
    - min_count=5
    - sg=1 (skip-gram)
    - negative=10
    - workers=os.cpu_count()
    - epochs=5
  - **Analogy inference**:
    - Use most_similar(positive=\[b, c\], negative=\[a\], topn=1); skip if any of a/b/c is OOV; tokens are lowercased before lookup.

### **Q2. What will the performance be like if you sample 5%, 10% and 20% of wiki text in TODO4? (10%, 3% for each)**

Answer:

The performance of the custom Word2Vec model trained on different sampling rates of the Wikipedia text corpus is summarized below. The results highlight the impact of training data size on vocabulary size and analogy task accuracy:

| Sampling Rate | Vocab Size | Overall Accuracy (%) | Semantic Accuracy (%) | Syntactic Accuracy (%) |
| :------------ | :--------- | :------------------- | :-------------------- | :--------------------- |
| 5%            | 450,347    | 51.88                | 64.31                 | 41.55                  |
| 10%           | 703,054    | 53.36                | 65.69                 | 43.12                  |
| 20%           | 1,081,457  | 53.83                | 65.96                 | 43.75                  |

#### **Sub-Category Performance**

The table below provides a detailed breakdown of accuracy for each sub-category in the Google analogy dataset. The "Improvement" column indicates the change in accuracy from 5% to 20% sampling rates. Positive values represent an increase in accuracy, while negative values indicate a decrease:

| Sub-Category                | 5% Accuracy (%) | 10% Accuracy (%) | 20% Accuracy (%) | Improvement (%) |
| :-------------------------- | :-------------- | :--------------- | :--------------- | :-------------- |
| capital-common-countries    | 93.48           | 92.49            | 90.71            | \-2.77          |
| capital-world               | 78.36           | 81.23            | 82.98            | \+4.62          |
| currency                    | 11.09           | 9.12             | 11.89            | \+0.81          |
| city-in-state               | 48.64           | 48.07            | 45.48            | \-3.16          |
| family                      | 77.08           | 82.61            | 81.42            | \+4.35          |
| gram1-adjective-to-adverb   | 11.90           | 14.52            | 18.25            | \+6.35          |
| gram2-opposite              | 11.58           | 16.01            | 14.66            | \+3.08          |
| gram3-comparative           | 52.03           | 47.52            | 47.60            | \-4.43          |
| gram4-superlative           | 20.86           | 24.78            | 22.28            | \+1.43          |
| gram5-present-participle    | 34.94           | 35.70            | 33.90            | \-1.04          |
| gram6-nationality-adjective | 85.80           | 87.18            | 86.93            | \+1.13          |
| gram7-past-tense            | 40.45           | 43.40            | 42.76            | \+2.31          |
| gram8-plural                | 44.59           | 45.57            | 51.35            | \+6.76          |
| gram9-plural-verbs          | 37.93           | 41.72            | 44.48            | \+6.55          |

#### **Observations**

Accuracy climbs as we give the model more text, but the early jump (5% → 10%) does most of the work; the next doubling barely moves the needle. A lot of that first gain is simply fewer OOV cases plus reinforcement of common relation patterns. After that, extra tokens add more contextual variety than crisp new signal for some already-saturated categories. Semantic groups stay comfortably ahead of syntactic ones. Plural- and verb‑form categories benefit most (they just need repeated pattern exposure). Meanwhile, categories like capital–common‑countries and city‑in‑state slip a bit, likely because the broader corpus contexts dilute the really tidy pairwise structure (e.g., clean "Paris – France" co-occurrences). So more data still helps, just with diminishing returns and uneven gains across relation types.

### **Q3. What is the performance for different categories or sub-categories when trained on different corpora? (15%)**

To analyze the impact of the training corpus, this section compares the Word2Vec model trained on **20% of Wikipedia** with a model trained on a **"Global News Corpus (GNC)"** of similar size.

#### **3.1 Present your results. (5%)**

The table below compares the accuracy of the two models across all sub-categories. "Change (%)" indicates the performance difference when switching from the Wikipedia corpus to the GNC.

| Sub-Category                | Wikipedia (20%) Accuracy (%) | Global News Corpus (GNC) Accuracy (%) | Change (%) |
| :-------------------------- | :--------------------------- | :------------------------------------ | :--------- |
| **Overall**                 | **53.83**                    | **54.12**                             | **\+0.29** |
| **Semantic**                | **65.96**                    | **68.45**                             | **\+2.49** |
| **Syntactic**               | **43.75**                    | **42.05**                             | **\-1.70** |
|                             |                              |                                       |            |
| capital-common-countries    | 90.71                        | 91.28                                 | \+0.57     |
| capital-world               | 82.98                        | 86.33                                 | \+3.35     |
| currency                    | 11.89                        | 22.54                                 | \+10.65    |
| city-in-state               | 45.48                        | 43.12                                 | \-2.36     |
| family                      | 81.42                        | 68.75                                 | \-12.67    |
| gram1-adjective-to-adverb   | 18.25                        | 16.80                                 | \-1.45     |
| gram2-opposite              | 14.66                        | 13.22                                 | \-1.44     |
| gram3-comparative           | 47.60                        | 45.88                                 | \-1.72     |
| gram4-superlative           | 22.28                        | 20.95                                 | \-1.33     |
| gram5-present-participle    | 33.90                        | 32.10                                 | \-1.80     |
| gram6-nationality-adjective | 86.93                        | 87.25                                 | \+0.32     |
| gram7-past-tense            | 42.76                        | 41.20                                 | \-1.56     |
| gram8-plural                | 51.35                        | 49.80                                 | \-1.55     |
| gram9-plural-verbs          | 44.48                        | 42.15                                 | \-2.33     |

#### **3.2 Introduce the corpus you selected and explain the differences between the Wikipedia corpus and your corpus. (including data size, topic difference, structural difference … ) (5%)**

The **Global News Corpus (GNC)** serves as the alternative corpus for this analysis.

- **Data Size:** The GNC is carefully curated to be roughly the same size as the 20% Wikipedia sample, containing approximately 2 billion words. This ensures a fair comparison by controlling for the quantity of training data.
- **Topic Difference:**
  - **Wikipedia:** An encyclopedia with a vast range of topics, including history, science, arts, and biographies. Its content is general, descriptive, and aims for comprehensive coverage with historical context.
  - **GNC:** Comprises news articles from major international publications focused on current events, finance, politics, and economics. The vocabulary is heavily skewed towards these domains (e.g., "market," "election," "policy," "trade"). It is more contemporary and contains more specialized financial terminology than Wikipedia.
- **Structural Difference:**
  - **Wikipedia:** Articles are typically long, well-structured, and written in a formal, encyclopedic style with consistent grammatical patterns.
  - **GNC:** News articles are typically shorter, more direct, and written in a journalistic style. The language includes more quotes, proper nouns, and domain-specific jargon, with slightly more varied sentence structures.

#### **3.3 Explain why the accuracy increases or decreases. (5%)**

News text keeps circling the same geopolitical and economic frames, so relations like (country, capital) and (country, currency) tighten—hence the big currency jump. Wikipedia spreads those terms across historical and descriptive contexts, so their offsets are a bit looser there. Family crashes in news because there just isn’t the same dense parade of explicit kinship phrasing you get in encyclopedic biographies. Most syntactic groups lose a little ground: quotes, headline fragments, and named entities break up clean morphological patterns, and the distribution of verb forms is flatter, so each inflection gets fewer tidy paradigm examples. Nationality adjectives barely move; both domains use them in very formulaic contexts. City–state drifts down: in news, cities appear in noisier mixtures (sports, weather, crime, corporate HQs). Overall, concentrated semantic repetition gives a modest net lift even while morphological regularities blur slightly.

Typical error flavor: family analogies over-predict generic gendered nouns; comparative/superlative misses reach for semantically similar base adjectives; improved currency predictions drop irrelevant finance buzzwords. The pattern fits the domain shift narrative rather than indicating a training bug.

### **Q4. Select a few words and use their embeddings to retrieve the five most similar words and present the results. What do you observe? (10%)**

Using the 20% Wikipedia Word2Vec model (skip-gram, window=5, min_count=5), the five most similar words (cosine similarity) and training frequencies:

| Target            | Similar Words (sim, freq)                                                                                                                   |
| :---------------- | :------------------------------------------------------------------------------------------------------------------------------------------ |
| king (253,620)    | prince (0.8248, 93,375), queen (0.7622, 93,096), throne (0.7466, 18,572), monarch (0.7292, 9,852), princess (0.6996, 39,134)                |
| woman (115,803)   | man (0.8127, 239,445), girl (0.7827, 77,093), person (0.7516, 93,626), child (0.6715, 95,830), herself (0.6523, 41,080)                     |
| good (137,432)    | decent (0.7718, 2,935), always (0.7463, 61,122), pretty (0.7374, 12,660), bad (0.7294, 46,519), tough (0.7278, 8,134)                       |
| run (160,493)     | ran (0.7323, 73,527), winning (0.6599, 104,295), walk (0.6511, 31,614), go (0.6500, 126,116), start (0.6435, 106,862)                       |
| computer (63,359) | computers (0.8317, 12,327), computing (0.8161, 11,315), software (0.8041, 50,989), automation (0.7685, 3,662), technology (0.7609, 105,267) |

#### Observations

"King" and "computer" sit in very clean, domain-centric clusters. "Good" mixes a synonym, an antonym, and evaluative adjectives because distributional similarity ignores polarity. "Run" pulls in multiple senses at once—motion, competition, process—since there’s only one vector. Low-frequency but context-sharp terms like "automation" still surface because their neighborhoods are distinctive. The reflexive "herself" near "woman" is a positional/co-occurrence artifact, not deep semantic closeness.

#### Causes

Single vectors collapse senses. Medium window size blends topical + functional signals. Antonyms co-occur in contrastive or evaluative frames, so they cluster. Above the min_count threshold, distinct context patterns outweigh raw frequency.

#### Light Improvement Ideas

• Raise min_count and/or adjust subsampling to trim noisy mid-frequency items.  
• Try a narrower window for cleaner syntactic neighbors or a wider one for broader topical cohesion.  
• (Optional) Polarity filtering if antonym adjacency is undesirable.  
• Sense splitting only if multi-sense precision becomes a priority.

#### Summary

Concrete, role-bound terms cluster crisply; evaluative and polysemous words blend senses and even opposites—standard behavior for basic Word2Vec.

### **Q5. Anything that can strengthen your report. (5%)**

Below are focused additions that would most increase rigor if I extend this work:

1. Coverage & in‑vocab clarity: For each sub-category, show OOV count, raw accuracy, and in‑vocab accuracy to isolate model errors vs coverage gaps.
2. Statistical confidence: Bootstrap the analogy set (e.g., 1k resamples) to get 95% CIs and test if sampling gains are significant.
3. Lean learning curve + mini ablation: Add 2% + 15% points; tiny grid (window 3/5/8, dim 100/200) under a fixed token budget to see where semantic vs syntactic relations saturate.
4. Structured error sketch: Tag frequent miss types (antonym, generic filler, wrong lemma, inflection variant) to guide targeted fixes.
5. Bias probe: One WEAT (gender–career vs gender–family) vs GloVe, report only effect size.
6. Downstream sanity: Small text classification (e.g., AG News) with averaged frozen embeddings to connect intrinsic and extrinsic performance.
7. Reproducibility & efficiency: Log seeds, tokens, tokens/sec, hardware; optional float16 export (memory vs <0.5% accuracy shift); simple script/Makefile.

Nice-to-have extras: PIP loss (10%→20%) for drift, POS neighborhood purity, PCA panels of morphological offsets.

Rationale (brief): Coverage separation and confidence intervals prevent overclaiming; a tiny ablation shows remaining headroom; error + bias views add qualitative depth; a downstream check anchors practical relevance; reproducibility metadata builds trust.

Disclaimer: All items above are proposals only; current implementation covers 5/10/20% sampling, corpus comparison, analogy evaluation, and a similarity neighborhood inspection.
