# RAG (Retrieval-Augmented Generation)

## Core flow
Retriever -> Reranker -> Prompt Builder -> Generator

## Why RAG helps
- Grounds answers in external evidence.
- Reduces factual hallucinations.
- Enables source traceability.
- Easier knowledge updates via reindexing.

## Prompt lifecycle with RAG
1. User query arrives.
2. Retrieve top candidate chunks.
3. Rerank/select best context.
4. Build grounded prompt.
5. Generate answer with citations.

## Prompt lifecycle without RAG
1. User query arrives.
2. Build instruction prompt only.
3. LLM responds from internal parametric memory.

## Is RAG necessary?
- Not always for generic writing tasks.
- Usually needed for factual, private, or frequently changing knowledge.

## RAG vs long context
- RAG advantages: scalability, citations, freshness, lower token load.
- Long-context advantages: simpler pipeline for small one-off inputs.
- Practical setup: both (retrieval + moderate context).

## Common failure modes
- Wrong retrieval.
- Important chunk not ranked high.
- Context overload/noise.
- Stale index.

## Mitigations
- Better chunking and overlap.
- Hybrid retrieval.
- Reranking.
- Metadata filtering.
- Tight top-k.
- Grounding guardrails.

## Add more notes
- 
