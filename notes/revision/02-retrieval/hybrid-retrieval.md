# Hybrid Retrieval

## What it is
- Combine lexical retrieval (BM25/keyword) + dense vector retrieval.
- Optional: combine with API results for live data.

## Why it helps
- Keyword catches exact strings, IDs, codes.
- Dense catches semantic similarity and paraphrases.
- Combined approach improves recall and robustness.

## Example
- Query references an exact ticket ID and asks for similar incidents.
- Keyword finds exact ticket doc.
- Dense finds semantically similar incidents.
- Final answer is more complete and accurate.

## Add more notes
- 
