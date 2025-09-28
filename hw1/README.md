# HW1 Overview

## Environment Setup

1. Install [Miniconda](https://docs.conda.io/en/latest/miniconda.html) if it is not already available.
2. Create and activate the homework environment:
   ```bash
   conda env create -f environment.yml
   conda activate nthu_nlp_hw1
   ```
3. (Optional) Update the environment after pulling project changes:
   ```bash
   conda env update -n nthu_nlp_hw1 -f environment.yml --prune
   ```

## Dataset Preparation

1. Open the notebook `hw1/main.ipynb`.
2. Run the first cell to download the Google Analogy dataset (`questions-words.txt`).
3. Execute the preprocessing cell to build `questions-words.csv`. This cell:
   - Parses word analogy pairs grouped by the raw file headers (e.g. `: capital-common-countries`).
   - Assigns the first five headers to the `Semantic` category, the rest to `Syntactic`.
   - Stores the results in a dataframe and writes it to `questions-words.csv`.
4. Verify the CSV was created successfully:
   ```bash
   ls hw1/questions-words.csv
   ```

## Part II: Pre-trained Embeddings

- With the environment active, continue in the notebook to load `gensim` pre-trained embeddings (e.g. `glove-wiki-gigaword-100`).
- The notebook builds predictions for analogy questions and evaluates accuracy by category.
- Ensure the earlier cells are run so the dataframe is available.

## Part III: Training Custom Embeddings

- Download the provided Wikipedia slices using the `gdown` commands in the notebook.
- Follow the instructions to train a new embedding model and evaluate it against the analogy dataset.

## Environment Reference

The current Conda environment was exported using:
```
conda env export --name nthu_nlp_hw1 > environment.yml
```
This file captures the packages (NumPy 1.26, pandas 2.3, gensim 4.3, scikit-learn 1.7, etc.) required by the notebook. Update and re-export after adding dependencies.

## Additional Download Links
For students who cannot access the links in main.ipynb, you can download the Wiki dataset in the following links:

```
!gdown --id 1J0os1846PQ129t720aI0wMm-5GepEwSl -O wiki_texts_part_0.txt.gz
!gdown --id 1tsI3RSKPN3b2-1IZ0N7bmjgVRf-THIkW -O wiki_texts_part_1.txt.gz
!gdown --id 1koiw6RFNzDe6pe2zMTfVhsEKmpmnYyu5 -O wiki_texts_part_2.txt.gz
!gdown --id 1YSGbDqhbg2xJsWD_hYQ5z9URl0dCTC2m -O wiki_texts_part_3.txt.gz
!gdown --id 1PA3C99C8CcLFjkenT0a9iU07XEQmXyG_ -O wiki_texts_part_4.txt.gz
```
```
!gdown --id 1sSLea4hq6Z7oT6noOU_II1ahWjNOKcDX -O wiki_texts_part_5.txt.gz
!gdown --id 1i6kXTDtZkRiivJ0mj-5GkVbE4gMFlmSb -O wiki_texts_part_6.txt.gz
!gdown --id 1ain2DN1nxXfsmJ2Aj9TFZlLVJSPsu9Jb -O wiki_texts_part_7.txt.gz
!gdown --id 1UKhvielQDqQz5pMZ7J3SHv9m8_8gO-dE -O wiki_texts_part_8.txt.gz
!gdown --id 1q1zMA4hbMS7tID2GTQx-c94UPB8YQaaa -O wiki_texts_part_9.txt.gz
!gdown --id 1-kkGxwMxPsoGg5_2pdaOeE3Way6njLpH -O wiki_texts_part_10.txt.gz
```

If this is not available, you can also download the dataset from the following link: [`LINK`](https://drive.google.com/file/d/1t4cqlZEgiRJCJJOzHeja3AjU1jTWiDRa/view?usp=sharing)