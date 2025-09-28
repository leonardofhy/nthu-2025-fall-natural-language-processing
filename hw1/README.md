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
