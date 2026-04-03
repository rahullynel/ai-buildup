# Orchestrators & Routing

## What an orchestrator is
- Control layer that routes each query to the best path.
- Chooses API, retrieval, LLM-only, or mixed flow.

## Intent classification
- Classify requests (factual lookup, live data, doc QA, rewrite, tool action).
- Use confidence thresholds and fallback paths.

## Tool selection logic
- Route by freshness need, data source, latency budget, risk.

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
