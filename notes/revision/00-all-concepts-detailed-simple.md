# All Concepts Detailed (Simple Terms)

This is the single page to read when I want full understanding quickly.

---

## 1) Big picture: how a GenAI system works

- User asks something.
- System decides what path to take.
- It may fetch data (API, docs, vector search) or answer directly.
- Prompt is built with instructions + context.
- LLM generates answer.
- Guardrails and checks run before final output.

Simple flow:

User Query
  -> Orchestrator (route decision)
  -> Data path (API / Retrieval / None)
  -> Prompt Builder
  -> LLM
  -> Checks (safety + quality)
  -> Final Answer

---

## 2) Transformers and LLM basics

### What transformers do
- Break text into tokens.
- Convert tokens to vectors.
- Use attention layers to build context-aware meaning.
- Predict next token one step at a time.

### Why self-attention matters
- A token can look at other tokens in the sentence/document.
- This helps the model understand relationships and context.
- Example: the word "bank" means different things in different contexts.

### Context window
- Max tokens model can read in one request.
- If important info is outside this window, model cannot use it directly.
- Large context helps but costs more and can add noise.

### Why hallucinations happen
- LLM predicts probable text, not guaranteed truth.
- If context is weak or missing, it guesses.
- If retrieved context is wrong, output can still be wrong.

Quick anti-hallucination habits:
- Give clear instructions.
- Ground with reliable context.
- Ask for uncertainty when evidence is missing.
- Prefer citations for factual answers.

---

## 3) Learning modes: zero-shot, one-shot, few-shot

### Zero-shot
- No examples in prompt.
- Fast and cheap.
- Good for common/simple tasks.

### One-shot
- One example in prompt.
- Helps format consistency.

### Few-shot
- Multiple examples in prompt.
- Better behavior control.
- Uses more tokens.

Rule of thumb:
- Start zero-shot.
- Move to few-shot if output format or behavior is unstable.

---

## 4) How model training works

### Core terms
- Sample: one training data point.
- Batch: small group of samples processed together.
- Step/iteration: one optimizer update using one batch.
- Epoch: one full pass over all training data.

### Training loop
1. Forward pass: model predicts on a batch.
2. Loss: compare prediction vs target.
3. Backpropagation: compute gradients.
4. Optimizer step: update weights.
5. Repeat.

### Gradient descent (simple view)
- We want lower error.
- Gradient tells direction of increasing error.
- Move weights in opposite direction.
- Learning rate controls step size.

### Backpropagation (simple view)
- Computes how much each parameter contributed to error.
- Uses chain rule across layers.
- Gives gradient values for weight updates.

### What changes based on error delta
- Usually model weights change, not raw data.
- Bigger useful error signal often means stronger update.
- Learning rate and optimizer control update size.

### Backtracking meaning
- In optimization: reduce step if loss gets worse.
- In AI workflows: if tool path fails, step back and try a better path.

---

## 5) Embeddings and vector search

### What embeddings are
- Numeric vectors representing semantic meaning.
- Similar text tends to have nearby vectors.

### Dense retrieval vs keyword search
- Dense retrieval:
  - good for meaning-level matches.
  - finds paraphrases.
- Keyword/BM25:
  - good for exact words, IDs, codes.

Best practice:
- Use both for stronger retrieval.

### Cosine similarity
- Measures vector direction similarity.
- Higher cosine means closer meaning.

### Chunking strategies
- Fixed chunking: easy baseline.
- Overlap chunking: reduces context breaks.
- Semantic chunking: split by topic/heading.

Chunking tradeoff:
- Too small: lose context.
- Too large: retrieval becomes noisy.

### Vector DB and ANN
- Vector DB stores embeddings + metadata.
- FAISS and HNSW are common indexing/search tools.
- ANN (approximate nearest neighbor) is fast because it avoids brute-force full scan.

---

## 6) RAG in simple terms

RAG = Retrieval-Augmented Generation.
- Retrieve evidence first.
- Then generate answer using that evidence.

### RAG flow

Query
  -> Retriever (find candidates)
  -> Reranker (pick best)
  -> Prompt builder (inject context)
  -> LLM generator
  -> Answer + citations

### Why RAG helps
- Better factual grounding.
- Better freshness when index is updated.
- Better traceability with sources.

### Common RAG failure modes
- Wrong chunks retrieved.
- Good chunk not ranked high.
- Too much noisy context.
- Stale index.

### RAG fixes
- Better chunking.
- Hybrid retrieval.
- Reranking.
- Metadata filters.
- Tight top-k.
- Prompt rule: if context missing, say not enough evidence.

---

## 7) Prompt lifecycle with and without RAG

### Without RAG

User Query
  -> Prompt Template
  -> LLM
  -> Answer

- Simpler and faster.
- Depends mostly on model memory + current prompt.

### With RAG

User Query
  -> Retrieval
  -> Context Selection
  -> Prompt Builder
  -> LLM
  -> Answer

- More grounded for factual tasks.
- Extra moving parts to tune.

---

## 8) Is RAG necessary? RAG vs long-context models

### Is RAG always needed?
- No.
- For writing/rephrasing/general tasks, LLM-only may be enough.
- For factual/private/fresh knowledge, RAG is usually better.

### Long-context models help when
- Input docs are already provided.
- Corpus is not huge.
- You want a simpler pipeline.

### RAG advantages
- Better scale over large document corpora.
- Lower token cost by sending only top relevant chunks.
- Better source attribution.
- Easier knowledge updates through reindexing.

### Long-context advantages
- Fewer components.
- Faster prototyping.
- Good for one-off document analysis.

### Practical answer
- Real systems often use both.
- Retrieval narrows context, long-context helps reasoning over selected evidence.

---

## 9) Hybrid retrieval

### What it is
- Combine lexical search + dense vector search.
- Sometimes also merge API data.

### Why it helps
- Lexical catches exact strings.
- Dense catches semantic similarity.
- Combined retrieval improves coverage and answer quality.

Example:
- Query asks for ticket INC-123 and similar incidents.
- Lexical finds exact ticket.
- Dense finds related incidents.
- Final answer is complete and grounded.

---

## 10) Orchestrators and routing

### What orchestrator does
- Decides which path to use per query.
- Path can be API, retrieval+LLM, LLM-only, or multi-step.

### Intent classification
- Understand user intent first:
  - live data lookup
  - knowledge base QA
  - rewrite/format
  - action/tool workflow

### Rule-based vs LLM-based orchestration
- Rule-based:
  - predictable, easy debug.
- LLM-based:
  - flexible, handles ambiguous requests.
- Typical production: hybrid.

Simple decision tree:

Need real-time data?
  yes -> API path
  no
Need private/doc knowledge?
  yes -> Retrieval path (often hybrid) + LLM
  no
Need rewriting/brainstorming?
  yes -> LLM-only
  no -> ask clarification

---

## 11) MCP vs API

### MCP (Model Context Protocol)
- Standardized way to connect models to tools/context.
- Helpful in multi-tool systems.

### Direct API
- Good when integrations are few and stable.
- Lower abstraction overhead.

### API over MCP when
- You only need a small fixed set of tools.
- You want simple, direct integration.

### MCP over API when
- You have many tools and changing integrations.
- You want standard interfaces and portability.

---

## 12) Agentic AI basics

### ReAct loop
- Thought -> Action -> Observation -> repeat.

### Planner -> Worker -> Critic
- Planner: break task into steps.
- Worker: execute steps.
- Critic: validate and improve output.

### Memory types
- Short-term: current conversation/session.
- Long-term: persistent preferences/facts.
- Vector memory: searchable prior notes/docs.

When agents make sense:
- Multi-step, tool-heavy tasks.
- Not needed for simple one-turn tasks.

---

## 13) Evaluation basics

### Why evaluation matters
- Good demos can hide weak reliability.
- Need measurable quality before shipping.

### Key metrics
- Faithfulness: answer supported by evidence.
- Relevance: answer solves user question.
- Context precision: retrieved chunks are mostly useful.

### Retrieval checks
- Recall@k
- Precision@k
- MRR / nDCG

Good practice:
- Evaluate retrieval first.
- Evaluate generation second.
- Evaluate end-to-end third.

---

## 14) Local LLM basics

### Running locally
- Ollama is common for local model serving.
- GGUF is common quantized model format.

### Quantization
- Lower precision to reduce memory and increase speed.
- Tradeoff: aggressive quantization can reduce quality.

### Local vs cloud
- Local pros: privacy, control, stable cost.
- Local cons: hardware limits, lower quality ceiling.
- Cloud pros: top models, easy scale.
- Cloud cons: recurring cost, governance concerns.

---

## 15) Key blocks of an AI system

- Data ingestion
- Data processing/chunking
- Embeddings/indexing
- Retrieval/reranking
- Orchestration
- Prompt building
- Model inference
- Guardrails
- Evaluation/observability

---

## 16) Portfolio architecture summary

My stack:
- Local RAG assistant
- Orchestrator
- Hybrid retrieval
- Vector DB
- Local LLM wrapper

End-to-end:

User
  -> Orchestrator
  -> API and/or Retrieval
  -> Context Builder
  -> Local LLM
  -> Answer + sources

Design decisions:
- Keep retrieval and generation modular.
- Add reranking and metadata filters.
- Add fallback path for low confidence.
- Keep prompts structured and constrained.

---

## 17) Fast interview revision block

- Epoch = one full pass over data.
- Backprop computes gradients.
- Gradient descent updates weights.
- RAG improves grounding using external evidence.
- Long-context is simpler but can be costlier for large corpora.
- Hybrid retrieval improves recall and robustness.
- MCP standardizes tool integrations in multi-tool AI systems.

---

## 18) Personal checklist

- I can explain zero-shot vs few-shot with examples.
- I can explain training loop in 20-30 seconds.
- I can explain RAG vs long context with tradeoffs.
- I can explain API vs MCP decision.
- I can draw end-to-end system blocks from memory.
