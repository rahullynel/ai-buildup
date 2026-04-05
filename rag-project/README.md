# RAG Step 1: Chunking + Embeddings + FAISS Search

This mini project demonstrates the core retrieval part of a RAG pipeline using a single Python script.

File covered:
- `rag_step1.py`

What this script does:
1. Takes a sample text paragraph (IPL history).
2. Splits it into fixed-size word chunks.
3. Converts chunks to embeddings using `all-MiniLM-L6-v2`.
4. Stores vectors in a FAISS index (`IndexFlatL2`).
5. Embeds a user query and retrieves top matching chunks.

This is the retrieval foundation before adding an LLM answer-generation step.

## Project Structure

- `rag_step1.py`: End-to-end retrieval demo.
- `requirements.txt`: Python dependencies.

## Requirements

- Python 3.9+ recommended
- Internet on first run (to download the sentence-transformer model)

Dependencies (already listed in `requirements.txt`):
- `sentence-transformers==2.6.1`
- `faiss-cpu==1.13.2`
- `numpy==1.26.4`

## Setup

From this folder:

```bash
pyenv activate rag-env
pip install -r requirements.txt
```

If `pyenv activate` is not available in your shell, initialize pyenv first and then activate:

```bash
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
pyenv activate rag-env
pip install -r requirements.txt
```

## Run

```bash
python rag_step1.py
```

## How the Code Works (Simple View)

### 1) Chunking
`chunk_text(text, chunk_size=20)` splits text by words and groups into chunks of 20 words.

### 2) Embedding + Indexing
`build_faiss_index(chunks)`:
- Encodes each chunk into a dense vector.
- Creates FAISS L2 index.
- Adds all chunk vectors to the index.

### 3) Retrieval
`search(query, chunks, index, embeddings, top_k)`:
- Embeds query.
- Searches nearest chunk vectors.
- Returns top-k text chunks.

## What FAISS Is and Why It Helps

FAISS stands for Facebook AI Similarity Search.

At a practical level, FAISS is a high-performance library for:
- Storing vector embeddings efficiently
- Searching for nearest vectors quickly
- Scaling vector search to large datasets

In RAG systems, once text chunks are converted to embeddings, you need a fast way to answer:
- "Which chunks are most semantically similar to this query?"

FAISS solves that retrieval problem.

### Why FAISS is useful in RAG

Without FAISS (or similar vector index), retrieval becomes slow as data grows because you would compare the query against every chunk vector each time.

FAISS helps by:
- Reducing retrieval latency
- Supporting large numbers of vectors
- Providing index types that balance speed vs accuracy
- Making top-k semantic retrieval practical for production systems

### How FAISS helps in this script

In this project, you use:

```python
index = faiss.IndexFlatL2(dim)
```

This means:
- `IndexFlatL2` stores vectors and uses L2 (Euclidean) distance
- Search is exact nearest-neighbor (not approximate)
- Good for learning, debugging, and small-to-medium datasets

When query embedding is computed, FAISS returns nearest chunk vectors:

```python
distances, indices = index.search(query_vec, top_k)
```

Then those indices are mapped back to original text chunks.

### Exact vs approximate search (important)

- Exact search (like `IndexFlatL2`):
	- highest retrieval fidelity
	- slower at very large scale

- Approximate search (IVF/HNSW-style indexes):
	- much faster on big corpora
	- slight accuracy tradeoff

Typical production pattern:
- Start with exact search for correctness
- Move to approximate FAISS indexes when scale/latency demands it

### Bottom line

FAISS is useful because it turns embeddings into a practical retrieval engine:
- fast top-k lookup
- scalable semantic search
- flexible accuracy/latency tradeoffs

That is exactly what makes RAG responsive and grounded.

## Example Query in Current Script

```text
How many times has CSK won the IPL?
```

The script then prints the top retrieved chunks.

## Notes and Practical Tips

- `top_k=8` in current script returns many chunks; for short text, try `top_k=3` to reduce noise.
- Current chunking is word-count based. For better quality later, move to semantic chunking or sentence-based chunking.
- `embeddings` is passed into `search()` but not used inside the function currently. This is okay for now, but can be removed in a cleanup.

## Common Errors and Fixes

### 1) `python: command not found`
Make sure your pyenv environment is activated:

```bash
pyenv activate rag-env
python rag_step1.py
```

### 2) `ModuleNotFoundError: No module named 'faiss'`
Install dependencies from `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 3) Slow first run
Normal behavior: model download/cache happens the first time.
