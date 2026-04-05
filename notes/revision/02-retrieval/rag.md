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
- Context dominance (retrieved text buries user intent).
- Prompt truncation from token overflow.

## Important misconception
- Tokenizer does not semantically choose what context to remove.
- In production systems, orchestrator/prompt builder decides context packing.
- Tokenizer only reports tokenized length against model limits.

## Mitigations
- Better chunking and overlap.
- Hybrid retrieval.
- Reranking.
- Metadata filtering.
- Tight top-k.
- Grounding guardrails.
- Explicit token budgets for: instructions, context, and user query.
- Context compression/summarization before final prompt build.
- Retrieval retry with stricter filters when overflow is detected.

## Fast terminology
- Dropped context at inference != underfitting.
- Use: context overflow, prompt truncation, context dilution.

## Add more notes
- 
