# GenAI Reference Notes

Personal study notes. Keep it simple. Quick revision format.

## 1. Transformers & LLM Basics

- Transformers process tokens in parallel and learn token-to-token relationships.
- Core idea: learn patterns from huge text corpora, then predict next token.
- Attention lets model decide what parts of input matter most for each token.

### What transformers do (high-level)
- Convert text -> tokens -> embeddings.
- Pass through many transformer layers.
- Each layer mixes context and refines token representations.
- Final layer predicts probability over next token.

### Self-attention (why it matters)
- For each token, model checks all other tokens.
- Builds contextual meaning (same word can mean different things by context).
- Handles long-range dependencies better than old RNN style.

### Context windows
- Context window = max tokens model can see at once.
- If useful info is outside window, model cannot use it directly.
- Bigger window helps, but cost and latency also increase.

### Why LLMs hallucinate
- Model is trained to predict plausible text, not guaranteed truth.
- Weak/ambiguous prompts -> model fills gaps.
- Missing context -> model guesses.
- Retrieved context can be wrong/outdated.
- Temperature too high can increase creative but wrong outputs.

## 2. Embeddings & Vector Search

### What embeddings represent
- Embedding = dense numeric vector for text meaning.
- Similar meaning -> vectors are closer in vector space.
- Used for semantic search, clustering, recommendations.

### Dense retrieval vs keyword search
- Dense retrieval:
  - Semantic matching.
  - Finds related meaning even with different wording.
- Keyword (BM25 style):
  - Exact term matching.
  - Great when exact words matter.
- Practical: often combine both.

### Cosine similarity
- Measures angle between vectors.
- Closer direction = higher similarity.
- Used to rank nearest chunks in vector search.

### Chunking strategies
- Fixed-size chunks: simple baseline.
- Overlap chunks: preserve continuity across boundaries.
- Semantic chunking: split by headings/paragraph meaning.
- Rule of thumb:
  - Too small -> misses context.
  - Too large -> noisy retrieval.

### Vector DB basics (FAISS, HNSW)
- FAISS:
  - Fast similarity search library.
  - Common for local/offline vector indexing.
- HNSW:
  - Graph-based ANN index.
  - Very fast nearest-neighbor lookup with good recall.

### ANN search (why it’s fast)
- ANN = Approximate Nearest Neighbor.
- Doesn’t check every vector.
- Uses smart index structures to find very good matches quickly.
- Tradeoff: slight accuracy loss for major speed gain.

## 3. RAG (Retrieval-Augmented Generation)

### Retriever -> Ranker -> Generator flow
- Retriever gets candidate chunks.
- Ranker/reranker improves ordering by relevance.
- Generator uses top context to answer.

ASCII flow:

User Query
   |
Retriever (vector/BM25/hybrid)
   |
Candidate Chunks
   |
Ranker / Reranker
   |
Top Context
   |
LLM Generator
   |
Final Answer + (optional citations)

### Why RAG reduces hallucinations
- Injects external facts instead of relying only on model memory.
- Grounds response in retrieved evidence.
- Can cite sources for traceability.

### Context injection
- Add retrieved chunks to prompt before generation.
- Keep context clean and relevant.
- Too much context hurts quality (noise + token waste).

### RAG prompt structure
- Instruction: what model should do.
- Retrieved context block(s).
- User question.
- Output constraints:
  - answer only from context
  - say "not enough info" if missing
  - include citation tags if needed

### Common failure modes
- Bad retrieval (wrong chunks).
- Lost-in-the-middle (important chunk buried).
- Context too long/noisy.
- Outdated source data.
- Chunk boundaries break key facts.
- Context dominance (retrieved text buries the user query).
- Prompt truncation from token overflow.

### How to fix/mitigate them
- Improve chunking and overlap.
- Use hybrid retrieval (keyword + dense).
- Add reranking step.
- Limit to top-k high quality chunks.
- Add metadata filtering (date, source, domain).
- Prompt guardrail: "If not in context, say unknown."
- Evaluate retrieval and answer quality separately.
- Enforce token budgets per section (instructions/context/query).
- Compress low-priority chunks before final prompt assembly.

## 4. Orchestrators

### What an orchestrator is
- Routing/control layer deciding what happens per query.
- Chooses path: API call, retrieval, LLM-only, or combination.

### Intent classification
- Detect user intent class:
  - factual lookup
  - real-time data request
  - summarization
  - reasoning
  - action/tool task

### Tool selection logic
- Based on intent + confidence + data freshness need.
- Example:
  - real-time stock/weather -> API
  - internal docs QA -> vector search + LLM
  - creative drafting -> LLM-only

### When to use API vs vector search vs LLM-only
- API:
  - live and structured data needed.
- Vector search:
  - private knowledge/document lookup.
- LLM-only:
  - rewriting, brainstorming, generic text tasks.

### Prompt building
- System rules.
- Task instruction.
- Retrieved/tool context.
- User input.
- Output format constraints.

Tokenizer vs orchestrator clarification:
- Tokenizer only tokenizes/counts/checks limits.
- Orchestrator/prompt builder decides what context is selected, compressed, ordered, or dropped.

### Guardrails
- Refusal rules for unsafe or out-of-policy asks.
- Source-grounding requirement for factual answers.
- Output schema checks.
- Tool timeout/fallback behavior.

### Rule-based vs LLM-based orchestration
- Rule-based:
  - predictable, transparent, easier to debug.
  - rigid on edge cases.
- LLM-based:
  - flexible routing in ambiguous cases.
  - less deterministic, needs eval and safety controls.
- Common setup: hybrid (rules first, LLM as smart router where needed).

### Simple decision tree

Start
 |
 |-- Need live data? ---- yes --> API path
 |                         no
 |
 |-- Need private/domain docs? -- yes --> Retrieval (vector/hybrid) + LLM
 |                                no
 |
 |-- Pure writing/reasoning task? -- yes --> LLM-only
 |                                   no
 |
 --> Ask clarifying question / fallback

## 5. Hybrid Retrieval

### Combining API + vector search
- API gives fresh structured facts.
- Vector search gives historical/internal context.
- Merge both in final prompt.

### When hybrid retrieval is needed
- Questions needing both "latest" and "background".
- Domain assistants where internal docs + external live signals matter.

### How hybrid retrieval improves accuracy
- Reduces stale answers.
- Reduces blind spots from only one source type.
- Better grounding from multiple evidence channels.

### Example: real-time data + historical knowledge
- Query: "Why did this metric spike today, and how does it compare to previous incidents?"
- API: today’s metric/time-series.
- Vector DB: past incident reports/postmortems.
- LLM: combined explanation + references.

## 6. Agentic AI (High-Level)

### ReAct loop (Thought -> Action -> Observation)
- Think about next best step.
- Take tool action.
- Observe result.
- Repeat until done.

### Tool use
- Tools can be APIs, search, database queries, code execution.
- Agent quality depends on tool quality + good stopping rules.

### Planner -> Worker -> Critic pattern
- Planner breaks task into steps.
- Worker executes steps.
- Critic checks output quality and gaps.

### Memory types
- Short-term memory:
  - current conversation context.
- Long-term memory:
  - persistent user/project preferences.
- Vector memory:
  - retrieval over prior notes/docs/events.

### When agents make sense
- Multi-step tasks with branching.
- Tool-heavy workflows.
- Cases where one-shot prompt is not enough.
- Not needed for simple single-turn Q&A.

## 7. Evaluation

### Why evaluation matters
- Demo quality can hide production failures.
- Need measurable quality before shipping.

### Faithfulness
- Answer is supported by provided context.
- No unsupported claims.

### Relevance
- Answer actually addresses user question.
- No unnecessary off-topic content.

### Context precision
- Retrieved context contains mostly useful chunks.
- High precision = less noise sent to LLM.

### Retrieval quality checks
- Recall@k: did top-k contain needed evidence?
- Precision@k: how many retrieved chunks were truly relevant?
- MRR/nDCG: ranking quality.
- Manual spot checks for tricky queries.

## 8. Local LLMs

### Running models locally (Ollama, GGUF)
- Ollama simplifies local serving and model management.
- GGUF is a common quantized model format for local inference.

### Quantization basics
- Reduce precision (ex: 16-bit -> 8-bit/4-bit).
- Lower RAM/VRAM usage and faster inference.
- Too much quantization can reduce quality.

### When local models are useful
- Privacy-sensitive data.
- Offline environments.
- Cost control for frequent inference.
- Low-latency on-device setups.

### Tradeoffs vs cloud models
- Local:
  - + privacy/control/cost stability
  - - weaker quality for smaller models, hardware limits
- Cloud:
  - + top model quality, easy scaling
  - - recurring cost, data governance concerns

## 9. My Portfolio Project Architecture

### Local RAG assistant
- User asks question.
- System retrieves local knowledge.
- LLM answers with grounded context.

### Orchestrator
- Routes by intent and data need.
- Chooses among API path, retrieval path, or LLM-only path.

### Hybrid retrieval
- Uses both:
  - vector search for semantic memory
  - API for live/structured data

### Vector DB
- Stores embeddings for chunks + metadata.
- Supports top-k retrieval and filters.

### Local LLM wrapper
- Unified interface to local model runtime.
- Handles prompts, generation params, and output cleanup.

### End-to-end flow (simple diagram)

User Query
   |
Orchestrator (intent + route)
   |
   |----> API Client (live data)
   |
   |----> Vector DB Retriever (historical/internal)
   |
Context Builder (merge + trim + format)
   |
Local LLM Wrapper
   |
Answer + Source Notes

### Key design decisions
- Keep retrieval and generation separated for easier debugging.
- Add reranking when retrieval noise is high.
- Use metadata filters early (date/source/type).
- Keep prompts structured and short.
- Add fallback path when confidence is low.

### What I learned building it
- Retrieval quality matters more than prompt tricks.
- Good chunking/ranking can change output quality a lot.
- Orchestrator logic prevents many wrong answers.
- Evaluation catches hidden failures early.
- Small, clear guardrails improve reliability.

---

## Quick Personal Checklist (before demo/interview)

- Can I explain RAG in 30 seconds?
- Can I explain when to use API vs vector vs LLM-only?
- Can I describe one retrieval failure and how I fixed it?
- Can I explain evaluation metrics I used?
- Can I justify local model choice and tradeoffs?
