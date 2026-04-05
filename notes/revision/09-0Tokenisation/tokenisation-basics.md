# Tokenisation Basics

Detailed revision note focused on tokenization, token budgets, and context packing in RAG/orchestrated systems.

## 1) What tokenisation is
- Tokenisation converts text into model-readable tokens.
- Tokens are subword units (not always full words).
- Every model has its own tokenizer and token vocabulary.
- Same sentence can produce different token counts across models.

## 2) What tokeniser does and does not do

Tokeniser does:
- Split text into tokens.
- Count prompt tokens.
- Check against model context limit.

Tokeniser does not:
- Decide semantic relevance.
- Choose which chunks to keep/drop.
- Use self-attention.
- Summarize or compress context.

Rule:
- Tokeniser is mechanical.
- Orchestrator/prompt builder is the decision layer.

## 3) Where self-attention actually happens
- Self-attention runs inside the LLM during inference.
- It is applied after the final prompt is assembled and tokenized.
- Tokeniser is pre-inference preprocessing, not reasoning.

## 4) If prompt exceeds token limits, who fixes it?
Not the tokenizer.

The orchestrator/prompt builder handles overflow by:
- Dropping low-relevance chunks.
- Reducing top-k retrieval.
- Summarizing/compressing long chunks.
- Trimming metadata and repetitive instructions.
- Re-running retrieval with stricter filters.

Tokenizer outcome is simply:
- "Too long" (hard error or truncation behavior depending on stack).

## 5) Is dropped context underfitting?
No.

- Underfitting is a training-time issue (model failed to learn patterns).
- Dropped context in RAG is an inference-time prompt budget issue.

Use these terms instead:
- Context overflow.
- Prompt truncation.
- Context dilution.

## 6) Context overshadowing / dominance

### What it is
- Retrieved context becomes too dominant, and user intent gets buried.

### Why it happens
- Too many chunks included.
- Chunk size is too large.
- Irrelevant chunks slip through retrieval/reranking.
- Prompt layout gives weak salience to user question.

### Symptoms
- Model answers from generic retrieved text, not exact user ask.
- User constraints are ignored.
- Answer drifts toward nearby but wrong subtopic.

### Mitigations
- Strong reranking and metadata filters.
- Hard chunk-length limits.
- Token budgets per prompt section.
- Keep user query salient in final prompt template.
- Compress low-priority context before packing.

### Context poisoning (related but more severe)
What it is:
- Harmful, misleading, or manipulated retrieved context steers the model away from correct behavior.
- Unlike normal dominance (too much context), poisoning includes low-quality or adversarial content that actively distorts outputs.

How it appears:
- Prompt-injection text inside retrieved chunks (for example: "ignore previous instructions").
- Outdated or untrusted documents treated as high-confidence evidence.
- Cross-tenant/noisy data leakage in shared indexes.

Mitigations:
- Source trust scoring and allowlists.
- Instruction-stripping or sanitization on retrieved context.
- Metadata-based access controls and tenant isolation.
- Retrieval-time safety filters + post-retrieval validation.
- Strong system rules that treat retrieved text as untrusted data, not instructions.

## 7) Orchestrator responsibilities related to tokenisation
Core responsibilities:
1. Retrieval/tool routing:
- Decide RAG vs API vs SQL/tool vs LLM-only.

2. Prompt construction:
- Merge system instructions + context + user query.
- Apply guardrails and formatting.
- Enforce token budget policy.

3. Overflow control:
- Re-rank, trim, compress, and rebuild prompt before model call.

## 8) Practical token budget strategy
Example budgeting flow:
1. Reserve output tokens first.
2. Reserve system instruction budget.
3. Reserve user query budget.
4. Allocate remaining tokens to context.
5. If overflow remains: trim/compress/retry retrieval.

Simple prompt packing priority:
- Must keep: system safety rules + current user query.
- High priority: top evidence chunks.
- Low priority: extra metadata, redundant context, long tails.

## 9) End-to-end mental model
User query
-> Orchestrator (intent + retrieval/tool choice + context packing)
-> Tokenizer (tokenize + count + limit check)
-> LLM (self-attention + generation)
-> Answer

Shortcut:
- Tokenizer = budget meter.
- Orchestrator = context manager.
- LLM = reasoning/generation engine.

## 10) One-line interview answers
- Does tokenizer drop context? No, orchestrator/prompt builder does.
- Does tokenizer use self-attention? No.
- Is context dropped by token limit underfitting? No, context overflow/truncation.
- Can RAG overshadow user input? Yes, context dominance/overshadowing.
- Does orchestrator rebuild the final prompt? Yes, every time in production pipelines.
