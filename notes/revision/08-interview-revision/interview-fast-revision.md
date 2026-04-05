# Interview Fast Revision

## 30-second concepts
- Epoch: one full pass over training data.
- Backprop: computes gradients.
- Gradient descent: updates weights to reduce loss.
- RAG: retrieval + generation for grounded answers.
- Hybrid retrieval: keyword + dense (often better recall).
- MCP: standard tool protocol for model ecosystems.

## Common compare questions
- RAG vs long context
  - RAG: scalable, citations, freshness.
  - Long context: simpler for smaller one-off input sets.
- API vs MCP
  - API: simple fixed integrations.
  - MCP: multi-tool standardization and portability.

## Common misconception checks
- Does tokenizer drop context?
  - No. Orchestrator/prompt builder drops or compresses context.
- Is context dropped by token limit called underfitting?
  - No. Use context overflow or prompt truncation.
- Can RAG hide user intent?
  - Yes. Context dominance/overshadowing.
- Context dominance vs context poisoning?
  - Dominance = too much context buries query; poisoning = harmful/untrusted context actively misleads output.
- Who decides retrieval strategy?
  - Orchestrator (rules/classifier/LLM router).
- Who rebuilds final prompt?
  - Orchestrator/prompt builder.

## Quick self-check
- Can I explain training loop in 20 seconds?
- Can I explain when RAG is not needed?
- Can I explain why hybrid retrieval helps?
- Can I explain orchestrator routing with one example?

## Add more notes
- 
