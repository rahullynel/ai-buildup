# Vector DB to RAG Flow (Step-by-Step)

Simple end-to-end view.

## 1) Start with raw text documents
- Example docs:
- sports.txt
- rules.txt
- These are plain text files.
- Vector DB cannot use raw text directly for semantic search.

## 2) Chunking: split docs into smaller pieces
- Split by paragraph, fixed token size, or semantic boundaries.
- Typical size: 300 to 500 tokens.
- Use overlap to preserve context across boundaries.

Example chunks:
- chunk_1: The IPL is a professional Twenty20 cricket league in India...
- chunk_2: The 2023 IPL final was played between...
- chunk_3: In cricket, a no-ball is an illegal delivery...

- These chunks are the units that get embedded and stored.

## 3) Embeddings: convert each chunk to a vector
- Use embedding model (example: all-MiniLM-L6-v2).
- Input: text chunk.
- Output: numeric vector (example: 384 or 768 dimensions).

Conceptual view:
- chunk_1 -> [0.12, -0.98, 0.44, ...]
- chunk_2 -> [0.09, -0.77, 0.51, ...]
- chunk_3 -> [0.88, 0.02, -0.33, ...]

Key idea:
- Similar meaning tends to produce nearby vectors.

## 4) Store in vector DB
For each chunk, store:
- id
- embedding vector
- original text
- metadata (source file, section, tags, page)

Conceptual record:
{
  "id": "chunk_2",
  "embedding": [0.09, -0.77, 0.51, ...],
  "text": "The 2023 IPL final was played between...",
  "metadata": {
    "source": "sports.txt",
    "section": "IPL history"
  }
}

- Vector DB (FAISS, Chroma, etc.) builds an index for fast similarity search.

## 5) User asks a question -> embed the query
Query example:
- Who won the IPL in 2023?

- Convert query with same embedding model.
- Query -> [0.10, -0.80, 0.49, ...]

Now you have:
- query vector
- many stored chunk vectors

## 6) Similarity comparison (3 common types)

### A) Cosine similarity (most common in RAG)

$$
\mathrm{cosine\_similarity}(\mathbf{a},\mathbf{b})=\frac{\mathbf{a}\cdot\mathbf{b}}{\|\mathbf{a}\|\,\|\mathbf{b}\|}
$$

Interpretation:
- close to 1: very similar direction/meaning
- around 0: weak relation
- close to -1: opposite direction (less common in this use)

Intuition:
- Smaller angle between vectors means more similar meaning.

### B) Dot product similarity
Formula:

$$
\mathbf{a}\cdot\mathbf{b} = \sum_i a_i b_i
$$

- Higher value means stronger similarity.
- Sensitive to vector magnitude (not just direction).
- Common when embeddings are trained for inner-product search.

### C) Euclidean (L2) distance
Formula:

$$
\|\mathbf{a}-\mathbf{b}\|_2 = \sqrt{\sum_i (a_i-b_i)^2}
$$

- Smaller distance means more similar vectors.
- This is a distance metric (lower is better), not a similarity score.

### What is "k-type" (top-k / k-NN)
- k means how many nearest results you want back.
- Example:
  - top-3 -> return 3 closest chunks
  - top-5 -> return 5 closest chunks
- k-NN means k nearest neighbors to the query vector.

## 7) What FAISS and HNSW do in search
- Brute-force comparison against all vectors is slow at scale.
- FAISS/HNSW build indexes (IVF, graph structures, etc.).
- They do approximate nearest-neighbor search for speed.
- Tiny accuracy tradeoff, major latency gain.

Core question still stays the same:
- Which stored vectors are closest to query vector?

Top-k style output:
- chunk_2 -> 0.93
- chunk_5 -> 0.89
- chunk_1 -> 0.84

## 8) Retrieve top-k chunks
What you get back:
- chunk text
- metadata
- similarity score

Example:
- chunk_2: The 2023 IPL final was played between CSK and GT. CSK won the title...
- chunk_1: The IPL is a professional Twenty20 cricket league in India...

- Usually keep top 3 to 10 chunks.

## 9) Build RAG prompt with retrieved context
Prompt shape:

You are a helpful assistant. Use ONLY the context below to answer.

CONTEXT:
1) The 2023 IPL final was played between CSK and GT. CSK won the title...
2) The IPL is a professional Twenty20 cricket league in India...

QUESTION:
Who won the IPL in 2023?

If the answer is not in the context, say you don't know.

- Now the model is grounded in retrieved evidence.

## 10) LLM generates grounded answer
Model reads:
- context chunks
- question
- instruction constraints

Generated answer example:
- Chennai Super Kings (CSK) won the IPL in 2023.

Key point:
- Model is not relying only on internal memory.
- It is answering from retrieved text.

## Quick recap
- Vector DB stores embeddings, not plain keyword index only.
- Each chunk becomes vector + metadata + text record.
- Query is embedded using same model.
- Similarity is commonly cosine similarity.
- FAISS/HNSW find nearest neighbors efficiently.
- Top-k retrieved chunks are injected into prompt.
- LLM answers using that grounded context.
