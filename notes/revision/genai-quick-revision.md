# GenAI Quick Revision (1-Page)

Use this before interviews/demos.

## Core blocks
- Transformer = context-aware token processor.
- Training basics = forward pass + loss + backprop + optimizer update.
- Embeddings = semantic vectors for retrieval.
- RAG = retrieval + generation for grounded answers.
- Orchestrator = routing brain.
- Hybrid retrieval = live API + historical vectors.
- Agents = iterative tool-using loops.
- Eval = measure faithfulness + relevance + retrieval quality.
- Local LLM = privacy/control, but quality/hardware tradeoff.
- MCP = standard tool protocol for model/tool integration.

## Learning and training basics
- Zero-shot: instruction only.
- Few-shot: include examples for consistent pattern.
- Epoch: one full pass over dataset.
- Batch: subset processed in one step.
- Backprop: computes gradients.
- Gradient descent: updates weights to reduce loss.
- Important: model weights are updated, not raw data itself.

## Mental model

User ask
  |
Orchestrator
  |
  |-- API (live truth)
  |-- Vector retrieval (doc memory)
  |-- LLM-only (text transform)
  |
Prompt builder
  |
LLM
  |
Answer (+ citations)

## Fast definitions
- Hallucination: confident but unsupported output.
- Cosine similarity: angle-based vector similarity.
- ANN: fast approximate nearest-neighbor search.
- Faithfulness: answer supported by evidence.
- Context precision: retrieved context is mostly relevant.
- MCP: common protocol for exposing tools/context to models.

## Prompt lifecycle
- Without RAG: query -> prompt -> LLM -> answer.
- With RAG: query -> retrieve -> build grounded prompt -> LLM -> answer with evidence.

## RAG vs long context
- RAG wins on large corpora, freshness, and citations.
- Long context wins on simplicity for small one-off inputs.
- Production pattern is often mixed: retrieval + moderate context windows.

## Common mistakes
- Wrong chunk size.
- No metadata filters.
- Too much context in prompt.
- No reranking.
- No fallback on low confidence.

## Fast fixes
- Tune chunk + overlap.
- Use hybrid retrieval.
- Add reranker.
- Tighten top-k.
- Add grounded-answer guardrail.
- Evaluate retrieval and generation separately.

## 30-sec interview lines
- "RAG reduces hallucination by grounding generation in retrieved evidence, but it still fails when retrieval is weak or context is noisy."
- "Orchestrator decides when to call APIs, when to retrieve docs, and when LLM-only is enough."
- "Hybrid retrieval improves accuracy by combining real-time structured data with semantic historical context."
