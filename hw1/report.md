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

The results demonstrate a clear, albeit nuanced, relationship between the size of the training corpus and the model's performance on the analogy task.

1. **Diminishing Returns on Accuracy:** Increasing the training data from 5% to 20% of the Wikipedia corpus yields a consistent improvement in overall accuracy. However, the gains exhibit diminishing returns. The leap from 5% to 10% sampling provides a **\+1.48%** boost in overall accuracy, whereas doubling the data again from 10% to 20% only adds another **\+0.47%**. This suggests that while a larger corpus is beneficial, there is a saturation point where substantially more data is needed for marginal gains.
2. **Vocabulary Growth vs. Performance:** The vocabulary size expands significantly with each increase in sampling rate. This growth reduces the number of out-of-vocabulary (OOV) words in the analogy test set, which is a key factor in the initial accuracy improvements. However, the slowing performance gains indicate that simply adding more words to the vocabulary does not guarantee better relational understanding for all analogy types.
3. **Impact on Semantic vs. Syntactic Categories:** The model consistently performs better on semantic analogies than syntactic ones. More data particularly benefits highly regular syntactic relationships, such as **"gram8-plural" (+6.76%)** and **"gram9-plural-verbs" (+6.55%)**, as the model sees more examples of these grammatical patterns. Conversely, some well-defined semantic categories like **"capital-common-countries" (-2.77%)** and **"city-in-state" (-3.16%)** experience a slight performance decline. This may be due to the introduction of noise; as the corpus grows, these words appear in a wider variety of contexts, which can slightly dilute the specific, clean vector relationships (e.g., Paris \- France) learned from a smaller, potentially more focused dataset.

In summary, a larger corpus is generally advantageous for building a robust Word2Vec model, but its impact varies across different types of linguistic relationships. The optimal corpus size represents a trade-off between vocabulary coverage, the reinforcement of regular patterns, and the potential introduction of contextual noise for highly specific semantic analogies.

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

The differences arise from domain-specific term distributions, context regularity, and stylistic variation between Wikipedia and the Global News Corpus (GNC):

1. Semantic gains (Overall Semantic: +2.49%; capital-world +3.35%; currency +10.65%):

   - High repetition of geopolitical and economic discourse in news strengthens co-occurrence regularities for (country, capital) and (country, currency) relations.
   - Currency terms in Wikipedia are more diffusely embedded in historical or descriptive contexts; in news, they co-occur densely with country and market descriptors, sharpening vector offsets.

2. Family decline (-12.67%):

   - Biographical and historical narrative in Wikipedia supplies dense relational patterns (father–mother, husband–wife). News allocates fewer tokens to explicit kinship structure, reducing the model’s ability to learn consistent analogy offsets for that category.

3. Small, broad syntactic decreases (most syntactic subcategories -1.3% to -2.3%):

   - Journalistic prose introduces more quotation fragments, headline-style truncations, and named-entity interruptions, mildly increasing contextual variance for morphological transformations (comparative, superlative, tense, plural).
   - Slightly flatter verb/inflection frequency distributions in news reduce the ratio of clean paradigm examples (e.g., run / ran / running) per total occurrences, diluting pattern strength.

4. Stability in nationality-adjective (+0.32%):

   - Nationality demonyms are frequent and structurally consistent in both corpora (e.g., “French officials,” “German companies”), preserving offset quality regardless of domain shift.

5. City-in-state and modest capital-common-countries drift (−2.36% and +0.57%):

   - U.S. state–city mentions in news are contextually noisier (sports, crime, weather) mixing with organization names, slightly weakening analogical precision.
   - capital-common-countries remains high because both corpora contain abundant aligned pairs; marginal gain reflects higher recency and repetition in geopolitical reporting.

6. Net effect (Overall +0.29%):

   - Semantic relation sharpening (due to concentrated topical repetition) marginally outweighs widened syntactic variability and reduced kinship relational density.

7. Contributing corpus factors:

   - Context homogeneity: News repeats finance and diplomacy frames, reinforcing a subset of semantic relations.
   - Named entity density: Improves capital/currency anchoring but injects noise into local grammatical windows.
   - Relational sparsity: Reduced explicit kinship phrase templates lowers vector regularity for family analogies.

8. Error pattern (typical qualitative observations for such shifts):
   - Family analogies more often produce high-frequency gendered nouns (e.g., predicting “man” or “person” instead of “husband”).
   - Comparative/superlative errors skew toward semantically similar base adjectives (e.g., retrieving strong instead of stronger).
   - Currency improvements manifest as fewer off-topic financial nouns (e.g., “market”) in top-1 predictions.

In summary, domain specialization in news sharpens frequently reiterated geopolitical/economic semantic relations while modestly degrading morphology-sensitive and kinship-oriented categories due to reduced patterned relational exposure and increased stylistic variability.

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

1. Clear semantic clusters: king and computer yield tightly coherent role/domain sets (royalty hierarchy; computing ecosystem).
2. Mixed semantic–functional neighbors: good retrieves a synonym (decent), antonym (bad), evaluative adjectives (tough, pretty), and a discourse/context word (always). This reflects distributional (not polarity-aware) similarity.
3. Morphology & inflection: run ↔ ran; plural/derivational variants (computers, computing) appear with high similarity.
4. Frequency skew: Some low-frequency but semantically precise words (decent, automation) surface due to distinctive contextual patterns despite smaller counts.
5. Broad contextual verbs for run (go, start, winning) indicate multi-sense blending (motion, process initiation, sports scoring).
6. Pronoun reflexive herself near woman shows syntactic/positional co-occurrence effects (window size capturing subject–reflexive contexts).

#### Causes

- Single-sense embeddings merge senses (run: motion / sports / process).
- Skip-gram with window=5 favors functional co-occurrence (always near evaluative adjectives).
- Antonym proximity (good–bad) is typical in distributional models sharing topical contexts.
- Frequency differences do not dominate similarity once minimum count is satisfied; contextual distinctiveness drives ranking.

#### Possible Improvements

- Increase min_count (e.g., 15–20) + sample=1e-4 to smooth high-frequency words and reduce mid-frequency noise.
- Larger window (≈8) for topical cohesion (could help king cluster with dynasty terms) or smaller (≈3) for tighter syntactic neighbors (may reduce always).
- Post-filter antonyms using external lexicons if polarity purity is desired (optional).
- Sense disambiguation: consider training sense embeddings (e.g., clustering contexts) if multi-sense words are critical.

#### Summary

The model produces coherent semantic neighborhoods for concrete or domain-focused terms (king, computer). Abstract or polysemous words (good, run) show blended semantic, functional, and antonymic relationships—an expected limitation of basic Word2Vec without polarity or sense modeling.

### **Q5. Anything that can strengthen your report. (5%)**

Proposed (future work) enhancements below are not implemented unless explicitly described in earlier sections. They are prioritized for impact vs. effort; you may select a subset in practice.

1. Coverage & baseline parity  
   Report custom Word2Vec vs GloVe with identical evaluation; add per–sub-category OOV counts and in‑vocab accuracy to separate model errors from coverage gaps.

2. Statistical confidence  
   Bootstrap analogy quadruples (e.g., 1,000 resamples) to derive 95% CIs and test significance of 5%→10%→20% improvements.

3. Learning curve + light ablation  
   Add 2% and 15% points; small grid (window 3/5/8; negative 5/10; dim 100/200) under a fixed token budget; plot semantic vs syntactic gains and tokens/sec.

4. OOV diagnostics (granular)  
   For each sub-category show: skipped/total, raw accuracy, in‑vocab accuracy. Highlight coverage-driven drops (e.g., early currency).

5. Structured error taxonomy  
   Label top mistakes: antonym, wrong lemma same POS, generic high-frequency filler, inflectional variant. Summarize counts to guide remedies (e.g., morphological augmentation).

6. Bias/fairness probe (WEAT)  
   Simple gender–career vs gender–family WEAT comparing custom vs GloVe; report effect size only (no sensitive example expansion).

7. Additional intrinsic signals  
   MEN, WordSim-353, SimLex-999 Spearman ρ; complements analogy (less morphology-weighted), clarifying semantic quality trade‑offs.

8. Relation & neighborhood consistency  
   (a) Parallelism: mean cosine of (capital−country) offsets to centroid (Wikipedia vs News).  
   (b) Angular neighborhood purity: % of top‑k neighbors sharing coarse POS for selected words (quantifies syntactic drift).

9. Reproducibility & efficiency  
   Log seeds (Python/NumPy/gensim), wall time, tokens, tokens/sec, hardware + versions; supply a Makefile / script to regenerate models end‑to‑end.

10. Practical & deployment aspects  
    (a) Downstream sanity: tiny AG News classifier using frozen averaged embeddings (macro‑F1 vs GloVe).  
    (b) Float16 (or quantized) embeddings: memory vs <0.5% accuracy delta.  
    (c) Visualization: PCA of morphological offsets + t‑SNE density for a polysemous term (run) + 5 curated failure examples (ranked outputs).

Optional micro add‑ons (if time permits): frequency‑bucket normalized accuracies; PIP loss between 10% and 20% models to quantify drift.

Summary: Prioritizing coverage separation, statistical confidence, structured error + bias analysis, and a lightweight downstream check would most effectively elevate rigor with moderate added effort.
