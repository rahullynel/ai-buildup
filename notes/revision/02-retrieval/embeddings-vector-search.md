# Embeddings & Vector Search

## What embeddings represent
- Dense vectors that encode semantic meaning.
- Similar concepts map close together in vector space.

## Dense retrieval vs keyword search
- Dense: semantic matching, good for paraphrases.
- Keyword/BM25: exact lexical matching, good for IDs/terms.
- Practical default: combine both.

## Cosine similarity
- Measures angle similarity between vectors.
- Higher cosine = more semantically similar.

## Chunking strategies
- Fixed-size chunks: simple baseline.
- Overlap chunks: preserve continuity.
- Semantic chunks: split by topic/heading meaning.
- Keep metadata (source/date/section) for filtering.

## Vector DB basics
- FAISS: fast similarity search library.
- HNSW: graph-based ANN index with good speed/recall.

## FAISS in detail (what, why, and where it helps)

### What FAISS is
- FAISS = Facebook AI Similarity Search.
- It is a library for storing vectors and doing nearest-neighbor search efficiently.
- In RAG, it answers: "Which chunk vectors are closest to this query vector?"

### Why FAISS is useful
- Brute-force comparison against every vector gets slow as data grows.
- FAISS indexes reduce retrieval time and make semantic search practical at scale.
- It supports different index types so you can choose tradeoffs:
	- exact search (higher fidelity)
	- approximate search (lower latency at scale)

### How FAISS helps in real pipelines
- Faster top-k retrieval means lower end-to-end RAG latency.
- Better latency allows:
	- larger knowledge bases
	- tighter user-facing response times
	- room for reranking and guardrails without major slowdown

### Exact vs approximate in FAISS
- Exact example: `IndexFlatL2`
	- compares query with all vectors
	- highest retrieval fidelity
	- good for small/medium datasets and debugging

- Approximate examples: IVF, HNSW variants
	- much faster for large corpora
	- slight recall tradeoff

Practical pattern:
- Start with exact FAISS to validate quality.
- Move to approximate FAISS indexes when scale/latency requires it.

### FAISS one-line interview answer
- "FAISS turns embeddings into a fast retrieval engine; it is what makes top-k semantic context lookup feasible for RAG at real-world scale."

### Why Do We Need FAISS?
- Because embeddings are high‑dimensional vectors.
Example:
The model  produces vectors of size 384.
So a single sentence becomes something like:

If you have:
• 	10 chunks → easy
• 	100 chunks → still easy
* 10,000 chunks → slow
* 1,000,000 chunks → impossible without FAISS

- FAISS solves this by:
* storing vectors efficiently
* indexing them
* searching them in milliseconds

### What FAISS Actually Does (Conceptually)
When you ask:
“How many times has CSK won the trophy?”

Your pipeline does this:
- 1. Convert query → embedding
- 2. Compare query embedding to all chunk embeddings
- 3. Return the closest ones

FAISS handles step 2:
fast similarity search in high‑dimensional space
Without FAISS, you’d be doing:
    for each vector:
    compute distance(query, vector)

That’s slow and doesn’t scale.
FAISS uses optimized algorithms like:
- L2 distance
- cosine similarity
- HNSW
- IVF
- PQ (product quantization)
These make search insanely fast.


### Why is FAISS so fast ? 

FAISS is written in:
- C++ (core)
- SIMD optimized
- GPU‑accelerated (optional)

It can search:
- 1 million vectors in < 10 ms
- 1 billion vectors with advanced indexes
This is why every serious RAG system uses FAISS or a similar vector DB.

### What FAISS Actually computes: Distance, Not meaning..

When you embed text, you get a vector like:
[0.12, -0.04, 0.88, ..., 0.33]


FAISS doesn’t “understand” cricket or IPL or CSK.
It only understands geometry.

Your query:
“How many times has CSK won the trophy”

becomes a vector.
Your chunks become vectors.
FAISS then asks:
“Which chunk vectors are closest to the query vector in high‑dimensional space?”

That’s it.

### Two ways to measure closeness

FAISS supports many metrics, but the two most important ones are : 

## L2 Distance (Euclidean)
- IndexFlatL2

It measures:
\mathrm{distance}=\sqrt{(a_1-b_1)^2+...+(a_n-b_n)^2}
Lower distance = more similar.

- CosineSimilarity

This measures the angle between vectors, not their magnitude.
\mathrm{similarity}=\frac{a\cdot b}{||a||\cdot ||b||}
Higher similarity = more similar.


### How FAISS Fits Into a RAG Pipeline

Here’s the flow:
Document → Chunker → Embeddings → FAISS Index → Retrieval → LLM

FAISS is the retrieval engine.
Without FAISS, RAG doesn’t work.

### FAISS in One Sentence
FAISS is a super‑fast vector search engine that finds the most semantically similar chunks to your query.

## ANN search (why fast)
- Avoids full brute-force nearest-neighbor scan.
- Uses index structures for fast approximate retrieval.

## Add more notes
- 
