# Orchestrators & Routing

## What an orchestrator is
- Control layer that routes each query to the best path.
- Chooses API, retrieval, LLM-only, or mixed flow.

## Intent classification
- Classify requests (factual lookup, live data, doc QA, rewrite, tool action).
- Use confidence thresholds and fallback paths.

## Tool selection logic
- Route by freshness need, data source, latency budget, risk.

## Core orchestrator responsibilities
1. Choose execution path:
- API, retrieval (vector/hybrid), SQL/tool call, or LLM-only.

2. Build final prompt:
- Merge system rules + retrieved/tool context + user query.
- Enforce structure, safety rules, and output schema.
- Enforce token budget before model call.

Important misconception:
- Tokenizer does not decide semantic importance.
- Orchestrator decides what context is kept, compressed, or dropped.

## If prompt is too long: what actually happens
- Tokenizer reports length (or tokenization stage fails against limits).
- Orchestrator must adapt prompt packing.

Common adaptations:
- Drop low-relevance chunks.
- Reduce top-k.
- Summarize/compress long chunks.
- Trim metadata/instruction verbosity.
- Re-run retrieval with tighter filters.

## Common routing mistakes
- Treating every query as RAG when API is better.
- Passing too many chunks and burying user intent.
- No confidence threshold before tool routing.
- No fallback path when retrieval confidence is low.

## Fast interview lines
- "Tokenizer counts tokens; orchestrator manages context budget."
- "Dropped context at inference is overflow/truncation, not underfitting."
- "Good orchestrators optimize routing and prompt packing, not just retrieval calls."

## Rule-based vs LLM-based orchestration
- Rule-based: predictable and easy to debug.
- LLM-based: flexible for ambiguous cases.
- Practical production pattern: hybrid.

## Decision tree
Start
 |
 |-- Need live data? -> API
 |-- Need domain/private docs? -> Hybrid retrieval + LLM
 |-- Need rewriting/formatting? -> LLM-only
 |-- Unclear -> ask clarification/fallback

## Add more notes
- 
