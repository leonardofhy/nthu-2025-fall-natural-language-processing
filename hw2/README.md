# HW2: LSTM-Arithmetic

LSTM-based sequence-to-sequence model for arithmetic calculations.

## Setup

1. **Download dataset** from [Google Drive](https://drive.google.com/file/d/1cMuL3hF9jefka9RyF4gEBIGGeFGZYHE-/view?usp=sharing) and place in `data/` folder

2. **Create conda environment:**

   ```bash
   conda create -n nlp_hw2 python=3.12 -y
   conda activate nlp_hw2
   ```

3. **Install PyTorch:**

   CPU:

   ```bash
   conda install pytorch torchvision torchaudio cpuonly -c pytorch
   ```

   GPU (CUDA 12.1):

   ```bash
   conda install pytorch torchvision torchaudio pytorch-cuda=12.1 -c pytorch -c nvidia
   ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Run

```bash
conda activate nlp_hw2
jupyter notebook
```

Open `main.ipynb` and run the cells.
