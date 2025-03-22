# RAG Project

This README provides instructions to set up and run the RAG (Retrieval-Augmented Generation) project.

## Prerequisites

Ensure you have [Anaconda](https://www.anaconda.com/) or [Miniconda](https://docs.conda.io/en/latest/miniconda.html) or Docker installed on your system.

Get Huggingface Token from here [Huggingface](https://huggingface.co/docs/hub/en/security-tokens)

Copy ```.env.example``` file

Python 3.11.11

## Anaconda Setup Instructions

1. **Create and activate a Conda environment**

   ```sh
   conda create --name rag-env python=3.11.11 -y
   conda activate rag-env
   ```

2. **Install required dependencies**

   ```sh
   pip install -r requirements.txt
   ```

3. **Run the Streamlit application**

   ```sh
   streamlit run main.py
   ```

## Docker Setup Instruction

1. **Create Huggingface Token and Paste into env file**


2. **Build Image**
```sh
docker compose up -d
```
   




