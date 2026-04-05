# GenAI Detailed Revision Notes

Personal revision notes. Slightly detailed, still scan-friendly.

---

## 1) Transformers & LLM Basics

### What transformers do (high-level)
- Take tokenized text and build contextual token representations.
- Process all tokens in parallel (better training speed vs old sequential models).
- Learn statistical language patterns, then generate next token repeatedly.
- Stacking layers increases ability to capture syntax + semantics + reasoning patterns.

### Self-attention (why it matters)
- Each token can attend to all tokens in current context.
- Helps resolve meaning by context:
  - "bank" in "river bank" vs "bank loan".
- Captures long-range dependencies better than RNN/LSTM style.
- Multi-head attention lets model learn different relation types in parallel.

### Context windows
- Max tokens model can consider in one pass.
- If critical info falls outside context window, model cannot directly use it.
- Tradeoff:
  - larger context = more coverage
  - but more cost, latency, and potential distraction/noise
- Practical note:
  - retrieval and good context packing are still needed even with long-context models.

### Why LLMs hallucinate
- Training objective is next-token likelihood, not truth guarantee.
- If prompt/context is incomplete, model fills gaps with likely text.
- Weak retrieval or outdated sources inject wrong evidence.
- Overly broad prompts cause model to over-generalize.
- Sampling settings can increase uncertainty (especially high temperature).

Quick fix checklist:
- Improve prompt constraints.
- Use grounded context (RAG).
- Ask model to state uncertainty when evidence missing.
- Add citations or evidence requirement.

---

## 2) Embeddings & Vector Search

### What embeddings represent
- Dense vectors that encode semantic meaning.
- Similar ideas map to nearby vectors.
- Used for semantic search, deduplication, clustering, recommendation.

### Dense retrieval vs keyword search
- Dense retrieval:
  - good for semantic matches and paraphrases.
  - can fail on exact IDs, rare terms, numeric strings.
- Keyword/BM25:
  - good for exact token matching and lexical precision.
  - can miss semantic variants.
- Best default in many apps: hybrid retrieval.

### Cosine similarity
- Measures angle similarity between vectors.
- Independent of vector magnitude.
- Common metric for ranking semantic closeness.

### Chunking strategies
- Fixed-size chunks:
  - easy baseline.
  - may split meaning awkwardly.
- Overlap chunking:
  - preserves context across chunk boundaries.
  - increases index size.
- Semantic chunking:
  - split on heading/topic boundaries.
  - better coherence, often better retrieval quality.

Practical chunk notes:
- Tune chunk size per document type (API docs vs legal docs vs chats).
- Keep metadata (title, date, section, source) for filtering and ranking.

### Vector DB basics (FAISS, HNSW)
- FAISS:
  - efficient similarity search library.
  - common local setup for prototypes and offline apps.
- HNSW:
  - graph-based ANN index.
  - strong speed/recall tradeoff.
- Core operations:
  - upsert embeddings
  - similarity query top-k
  - filter by metadata

### ANN search (why it’s fast)
- ANN avoids exact brute-force scan of all vectors.
- Uses index structures to explore most promising neighborhood quickly.
- Main tradeoff: speed vs recall.

---

## 3) RAG (Retrieval-Augmented Generation)

### Retriever -> Ranker -> Generator flow
- Retriever fetches candidate chunks.
- Ranker/reranker reorders by relevance.
- Generator answers based on top context.

ASCII:

Query
  |
Retriever (dense/BM25/hybrid)
  |
Top-N candidates
  |
Reranker
  |
Top-K evidence
  |
Prompt builder
  |
LLM generator
  |
Answer + citations

### Why RAG reduces hallucinations
- Grounds model output in external evidence.
- Reduces reliance on stale parametric memory.
- Gives traceability via cited chunks/docs.

### Context injection
- Add only high-signal context into prompt.
- Order context by relevance.
- Keep each chunk clearly separated with source labels.
- Avoid context overload.

### RAG prompt structure
- Role/instruction block.
- Rules block:
  - answer from context only
  - if missing evidence, say not found
  - cite sources
- Context block(s).
- User question.
- Output schema (optional).

### Common failure modes
- Bad retrieval:
  - wrong chunks selected.
- Good chunks but poor ranking:
  - key evidence not in top positions.
- Chunk fragmentation:
  - fact split across chunks.
- Stale index:
  - outdated information.
- Prompt leakage/noise:
  - model gets distracted.
- Context dominance:
  - retrieved context overshadows user question.
- Token overflow:
  - important context or query parts get truncated.

### How to fix/mitigate
- Improve chunking + overlap.
- Add reranker.
- Use hybrid retrieval.
- Tight metadata filters (date/team/product).
- Reindex regularly.
- Keep top-k tight and high quality.
- Add fallback response if evidence confidence is low.
- Enforce section-level token budgets (instructions/context/query/output).
- Compress low-priority chunks before prompt assembly.

---

## 4) Orchestrators

### What an orchestrator is
- Control layer that routes queries to the right path.
- Decides how to combine tools, retrieval, and model calls.

### Intent classification
- Classify intent early:
  - informational
  - live-data lookup
  - multi-step analysis
  - action/automation
  - pure writing

### Tool selection logic
- Route based on:
  - freshness needed
  - source of truth
  - confidence threshold
  - cost/latency limits

### When to use API vs vector search vs LLM-only
- API path:
  - real-time, structured, authoritative data.
- Vector path:
  - private docs, historical records, knowledge base.
- LLM-only:
  - transformation tasks (rewrite/summarize/brainstorm) where strict factual grounding not required.

### Prompt building
- Build prompt in layers:
  - system constraints
  - task intent
  - retrieved/tool outputs
  - user input
  - output format

Tokenizer vs orchestrator:
- Tokenizer: tokenization + length accounting only.
- Orchestrator: context selection, compression, ordering, and truncation policy.

Clarification:
- If context is dropped due to limits, this is not underfitting.
- Correct terms: context overflow / prompt truncation.

### Guardrails
- Safety policy checks.
- Allowed tools whitelist.
- Input sanitization.
- Output validation (schema/rules).
- Fallback + retry policy.

### Rule-based vs LLM-based orchestration
- Rule-based:
  - deterministic and easy to debug.
  - less adaptive.
- LLM-based:
  - flexible for ambiguous intent.
  - needs eval + controls for consistency.
- Typical production approach:
  - rules for hard constraints
  - LLM routing for soft decisions.

### Simple decision tree

User query
  |
Need real-time facts?
  |-- yes -> API
  |-- no
       |
       Need private/domain knowledge?
         |-- yes -> Retrieval (hybrid) + LLM
         |-- no
              |
              Pure writing/transformation?
                |-- yes -> LLM-only
                |-- no -> ask clarification / safe fallback

---

## 5) Hybrid Retrieval

### Combining API + vector search
- API covers latest truth.
- Vector DB covers institutional memory.
- Combined context gives better final answer quality.

### When hybrid retrieval is needed
- Questions combining "what now" + "what happened before".
- Decision support where both live metrics and prior docs matter.

### How hybrid improves accuracy
- Reduces stale or partial answers.
- Improves coverage and grounding.
- Supports better explanations with both current and historical evidence.

### Example: real-time + historical
- Question: Why did error rate spike today, and have we seen this before?
- API: latest error rate/service health.
- Vector DB: prior incidents/postmortems.
- Output: root-cause hypothesis + comparison + references.

---

## 6) Agentic AI (High-Level)

### ReAct loop (Thought -> Action -> Observation)
- Decide next step.
- Execute tool.
- Inspect result.
- Repeat until done or stopping condition met.

### Tool use
- Agent actions can include:
  - search
  - API calls
  - DB queries
  - code execution
- Reliability depends on tool correctness and clear policies.

### Planner -> Worker -> Critic pattern
- Planner:
  - decomposes task.
- Worker:
  - executes subtasks.
- Critic:
  - checks quality, consistency, missing pieces.

### Memory types
- Short-term memory:
  - current session details.
- Long-term memory:
  - durable user/project preferences.
- Vector memory:
  - retrievable episodic/doc memory.

### When agents make sense
- Multi-step workflows.
- Tool-heavy tasks.
- Open-ended tasks requiring iterative refinement.
- Not ideal for quick one-shot Q&A.

---

## 7) Evaluation

### Why evaluation matters
- Without eval, systems look good in demos and fail in real usage.
- Needed for regression detection and confidence before release.

### Faithfulness
- Is answer supported by retrieved evidence?
- No unsupported claims.

### Relevance
- Does answer actually solve user ask?
- Avoids irrelevant filler.

### Context precision
- Are retrieved chunks mostly useful?
- High precision reduces prompt noise.

### Retrieval quality checks
- Recall@k: did we retrieve needed evidence at all?
- Precision@k: how much retrieved context was truly relevant?
- nDCG/MRR: ranking quality.
- Manual eval set for hard cases.

Evaluation habit:
- Evaluate retrieval separately from generation.
- Then evaluate end-to-end answer quality.

---

## 8) Local LLMs

### Running models locally (Ollama, GGUF)
- Ollama: easy local serving workflow.
- GGUF: popular quantized format for local runtimes.

### Quantization basics
- Lower precision to reduce memory and speed up inference.
- Typical levels: 8-bit, 4-bit.
- More quantization = faster/cheaper, but possible quality drop.

### When local models are useful
- Privacy-sensitive workloads.
- Offline environments.
- Predictable cost and full deployment control.

### Tradeoffs vs cloud models
- Local pros:
  - privacy, control, no per-token cloud billing.
- Local cons:
  - weaker model quality ceiling, hardware constraints.
- Cloud pros:
  - best available models, easier scaling.
- Cloud cons:
  - cost variability, governance requirements.

---

## 9) My Portfolio Project Architecture

### Local RAG assistant
- User asks question.
- Retrieve evidence.
- Build grounded prompt.
- Generate answer with citations.

### Orchestrator
- Classifies intent.
- Picks retrieval/API/LLM route.
- Applies safety and fallback rules.

### Hybrid retrieval
- Mixes:
  - semantic retrieval from vector DB
  - real-time API context

### Vector DB
- Stores chunk embeddings + metadata.
- Enables filtered top-k retrieval.

### Local LLM wrapper
- Single interface for local model calls.
- Standardizes prompt templates and inference settings.

### End-to-end flow (simple diagram)

User Query
  |
Orchestrator
  |
  |-- API path (live data)
  |-- Retrieval path (vector/hybrid)
  |
Context Builder (select + trim + format)
  |
Local LLM Wrapper
  |
Answer + citations + confidence/fallback

### Key design decisions
- Keep retrieval modular for easier tuning.
- Add reranker after initial retrieval.
- Keep metadata-rich ingestion.
- Use strict prompting for grounded answers.
- Add fail-safe response when confidence is low.

### What I learned building it
- Retrieval quality dominates final quality.
- Better chunking often beats prompt tweaking.
- Orchestrator logic prevents many wrong routes.
- Evaluation catches hidden regressions early.
- Local-first setup is great for privacy + fast iteration.

---

## Interview Revision Checklist

- Can I explain transformers and attention in simple terms?
- Can I compare dense vs keyword retrieval with examples?
- Can I explain why RAG reduces hallucinations and where it still fails?
- Can I justify orchestrator routing rules?
- Can I define faithfulness/relevance/context precision clearly?
- Can I explain when local LLM beats cloud and when it does not?
