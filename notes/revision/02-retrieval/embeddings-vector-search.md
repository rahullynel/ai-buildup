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

## ANN search (why fast)
- Avoids full brute-force nearest-neighbor scan.
- Uses index structures for fast approximate retrieval.

## Add more notes
- 
