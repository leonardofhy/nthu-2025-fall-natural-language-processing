# NTHU NLP HW4 RAG Assignment Tasks

## Overview
- **Goal:** Build a RAG system for Question Answering about cats.
- **Database:** `cat-facts.txt` (150 facts).
- **Test Set:** 150 QA pairs (provided in `questions_answers.txt` mostly likely, or generated).
- **Models:**
    - Generator: Llama-3.2-1B (frozen).
    - Retriever: User choice (e.g., Chroma, BM25, etc. - Guidelines mention usage of `jina-embeddings-v2-base-en`).

## Implementation Tasks (Coding Work)

### Part 1: Environment Setup (5%)
- [ ] **TODO 1:** Set up Ollama environment.
    - Install `colab-xterm` (if on Colab/Linux).
    - Install Ollama (`curl -fsSL https://ollama.com/install.sh | sh`).
    - Pull model: `ollama pull llama3.2:1b` (or similar tag).
    - Start server: `ollama serve`.

### Part 2: Database Preparation (10%)
- [ ] **TODO 2:** Load `cat-facts` dataset.
    - Download/Load `cat-facts.txt`.
    - Create `Document` objects using LangChain.
    - Create a Chroma vector store.
    - Set up a retriever (e.g., `vector_store.as_retriever`).

### Part 3: Prompt Engineering (10%)
- [ ] **TODO 3:** Set up `system_prompt` and configuration.
    - Design a system prompt to guide the LLM.
    - Create `ChatPromptTemplate`.

### Part 4: RAG System Build (10%)
- [ ] **TODO 4:** Build and run the RAG system.
    - **TODO 4-1:** Load QA chain (pass docs to model).
    - **TODO 4-2:** Create retrieval chain (retriever + QA chain).
    - **TODO 4-3:** Run on the provided queries (10 sample queries first, then full set).
    *   *Constraint:* Must use `jina-embeddings-v2-base-en` and `Llama3.2-1b`.

### Part 5: Optimization (10%)
- [ ] **TODO 5:** Improve performance for 150 questions.
    - Ensure correct answers for the dataset.
    - Generate predictions JSON.

## Evaluation & Submission

### Artifacts to Submit
1.  **Code:** `NLP_HW4_<Student_ID>.ipynb`/`.py`.
2.  **Predictions:** `NLP_HW4_<Student_ID>.json`.
    - Format: `[{"Query": "...", "Ground_Truth": "...", "Prediction": "..."}, ...]`.
3.  **Report:** `NLP_HW4_<Student_ID>.docx`/`.pdf`.
4.  **Requirements:** `requirements.txt`.
5.  **Zip:** All above zipped as `NLP_HW4_<Student_ID>.zip`.

### Metrics
- **Retrieval:** Recall@1, Recall@5.
- **Generation:** Exact Match (EM).

## Report Requirements (55%)
- [ ] **Implementation Details (5%):** System architecture, prompt used, new code vs template.
- [ ] **Prompt Analysis (10%):** Performance with different prompts.
- [ ] **Input Format Analysis (10%):** Performance with different retriever input formats.
- [ ] **Input Order Analysis (10%):** Performance with different document orders.
- [ ] **Counterfactual Analysis (10%):** Performance with counterfactual info injected.
- [ ] **Other (10%):** Any other analysis to strengthen report.
