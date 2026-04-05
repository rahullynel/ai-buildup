# GenAI Systematic Revision Notes

Simple revision notebook. Not essay style. Keep coming back to this.

## 0) How to use this file
- 10-min pass: read sections 1, 2, 4, 5, 7, 8.
- 30-min pass: read all sections once.
- Interview pass: read section 10 only.
- If stuck on one concept, jump to section 11 (quick fixes).

---

## 1) Learning modes: zero-shot, one-shot, few-shot

### Zero-shot
- No examples in prompt.
- Model uses instruction only.
- Best for simple, common tasks.
- Weak when format is strict or domain is specialized.

### One-shot
- Give one example input-output pair.
- Helps model lock onto style and output format.

### Few-shot
- Give multiple examples.
- Better pattern control.
- Costs more tokens.
- Good for consistent formatting and domain wording.

### Quick rule
- Start zero-shot.
- If output is inconsistent, move to few-shot.
- Keep examples short and representative.

---

## 2) How training works (epoch, gradient descent, backprop)

### Core terms
- Sample: one training example.
- Batch: group of samples processed together.
- Iteration/step: one optimizer update using one batch.
- Epoch: one full pass over training dataset.

### Training loop (high level)
- Step 1: send batch through model (forward pass).
- Step 2: compute loss (prediction error).
- Step 3: compute gradients via backpropagation.
- Step 4: optimizer updates weights (gradient descent variant).
- Step 5: repeat for all batches and epochs.

### Gradient descent basics
- Goal: reduce loss.
- Update rule idea: move weights opposite gradient direction.
- If gradient is large, update is larger.
- Learning rate controls step size.

### Backpropagation
- Uses chain rule to compute how each weight contributed to error.
- Produces gradient for each trainable parameter.
- Enables efficient training of deep networks.

### What changes when error changes
- Important: data usually does not change, model weights change.
- Delta/error affects gradient magnitude and direction.
- Bigger error signal can produce bigger updates (bounded by optimizer settings).
- Very noisy gradients can destabilize training.

### Backtracking (two contexts)
- Optimization backtracking line search:
  - shrink learning step if loss does not improve.
  - helps stable convergence in some optimization setups.
- Agent/system backtracking:
  - undo last route/tool choice and try alternate path when evidence is weak.

### Practical stability notes
- Normalize/clean data before training.
- Use train/validation split.
- Monitor overfitting (train loss down, val loss up).
- Use early stopping/checkpoints.

ASCII training flow:

Data -> Batches -> Forward pass -> Loss
                         |
                         v
                   Backprop gradients
                         |
                         v
                 Optimizer weight update
                         |
                         v
                       Next batch

---

## 3) Transformers and LLM basics (quick refresher)

### What transformers do
- Process tokens in parallel.
- Build contextual token representations with attention.
- Predict next token repeatedly.

### Self-attention
- Each token scores relation with other tokens.
- Helps capture long-range context and meaning shifts.

### Context window
- Maximum tokens visible to model in one call.
- Longer windows help, but increase cost and latency.

### Why hallucinations happen
- Objective is likely text generation, not strict truth.
- Missing evidence or vague prompt causes guessing.
- Retrieval noise can inject wrong facts.

---

## 4) Prompt lifecycle (without RAG vs with RAG)

### Without RAG
- User query enters system.
- Prompt template applied.
- LLM answers from parametric memory + prompt only.

ASCII:

User query -> Prompt template -> LLM -> Answer

### With RAG
- User query enters system.
- Retrieve relevant context.
- Build grounded prompt using retrieved chunks.
- LLM answers with evidence context.

ASCII:

User query -> Retriever -> Top context -> Prompt builder -> LLM -> Answer (+ citations)

### Why this matters
- Without RAG: faster and simpler, but more risk on factual/long-tail questions.
- With RAG: more grounded, but retrieval quality becomes a new dependency.

Misconception to avoid:
- Tokenizer does not choose which context is useful.
- Orchestrator/prompt builder chooses context packing strategy.
- Tokenizer only performs tokenization and limit checks.

---

## 5) Is RAG necessary? Long-context models vs RAG

### Is RAG always required?
- No.
- If task is generic writing or simple reasoning, LLM-only may be enough.
- If task needs fresh/private/traceable facts, RAG is usually worth it.

### How long-context models help
- Can ingest larger documents directly.
- Better for single-session analysis when docs are small enough.
- Reduces need for retrieval in some narrow workflows.

### Limits of long-context only
- Cost rises with many tokens.
- Latency rises with large prompts.
- Still no guaranteed source freshness.
- Hard to scale when corpus is very large.

### RAG advantages over long-context only
- Better scalability for large knowledge bases.
- Cheaper inference by sending only top relevant chunks.
- Easier source attribution.
- Easier to update knowledge by reindexing.

### Long-context advantages over RAG
- Simpler pipeline (fewer moving parts).
- No retrieval/reranking tuning in early prototypes.
- Good when user already provides all needed documents.

### Practical decision
- Small workload, all docs in prompt, low freshness need: long-context can be enough.
- Large corpus, frequent updates, citation needs: prefer RAG.
- Common production pattern: both.

---

## 6) Hybrid retrieval: what and why

### What is hybrid retrieval
- Combine lexical retrieval (BM25/keyword) and dense vector retrieval.
- Optional extra source: APIs for live data.

### Why it helps
- Keyword search catches exact terms/IDs.
- Dense search catches semantic paraphrases.
- Combined recall is usually better than either alone.

### Example
- User asks about incident ticket INC-4821 and similar failures.
- Keyword finds exact ticket.
- Vector search finds semantically similar incidents.
- Final answer is more complete.

---

## 7) MCP and API: what, and when to use which

### What is MCP
- Model Context Protocol: standard way for models/agents to connect to tools and data sources.
- Gives a common interface for tool discovery, invocation, and context exchange.

### Why API over MCP (sometimes)
- Direct API can be simpler for one fixed integration.
- Lower abstraction overhead when you only need 1-2 endpoints.
- Easier custom auth/perf tuning in some systems.

### Why MCP over direct API (sometimes)
- Standardized tool interface across many tools.
- Better portability across model runtimes/agent frameworks.
- Cleaner tool governance in multi-tool ecosystems.

### Quick rule
- Single-purpose app with stable integrations: API-first is fine.
- Multi-tool agent platform with changing tools: MCP can reduce long-term integration pain.

---

## 8) Key blocks of an AI system

- Ingestion block: collect docs/events/data.
- Processing block: clean, chunk, enrich metadata.
- Embedding/index block: create vectors, build indexes.
- Retrieval block: lexical/dense/hybrid search.
- Reranking block: reorder candidates.
- Orchestration block: route decision and tool policy.
- Prompt construction block: system rules + context + user task.
- Model inference block: LLM call.
- Safety/guardrails block: policy checks and output validation.
- Evaluation/observability block: metrics, logs, traces, feedback loops.

---

## 9) Orchestration patterns and model routing

### Common orchestrator styles
- Rule-based router:
  - deterministic paths, easy to debug.
- Classifier router:
  - intent model chooses route.
- LLM router:
  - flexible for ambiguous asks.
- Graph/workflow orchestrator:
  - explicit multi-step state machine.

### Which model type is used where
- Small fast model:
  - intent classification, guard checks, cheap transforms.
- Embedding model:
  - vectorization for retrieval.
- Reranker model:
  - relevance ordering.
- Large reasoning model:
  - final answer generation.

### Typical routing policy
- Real-time factual ask -> API + optional retrieval + LLM synth.
- Knowledge-base ask -> hybrid retrieval + reranker + LLM.
- Creative rewrite -> LLM-only.
- Unsafe/out-of-scope ask -> refuse/safe response.

ASCII:

Query -> Intent router
  |-- live data -> API path
  |-- doc QA -> Hybrid retrieval path
  |-- rewrite -> LLM-only path
  |-- unsafe -> Guardrail response

---

## 10) Interview revision bullets (fast answers)

- What is an epoch?
- One full pass over all training data.

- How do gradient descent and backprop work together?
- Backprop computes gradients, gradient descent uses them to update weights.

- Does training modify data?
- Usually no. Training modifies model parameters. Data is preprocessed/augmented separately.

- RAG vs long context?
- RAG scales better and gives citations. Long context is simpler for smaller one-off inputs.

- What is hybrid retrieval?
- Combined keyword + dense retrieval, often with reranking; improves recall and robustness.

- Why MCP?
- Standard tool interface for agent ecosystems. Great when many tools and changing integrations are involved.

---

## 11) Common failure patterns and fixes

- Symptom: answer sounds good but wrong.
- Fix: enforce evidence grounding + citation checks.

- Symptom: missing exact IDs/names.
- Fix: add lexical retrieval and metadata filters.

- Symptom: latency too high.
- Fix: reduce top-k, compress context, use smaller router models.

- Symptom: user intent gets ignored despite retrieval.
- Fix: control context dominance with stronger reranking, tighter chunk limits, and query-salient prompt layout.

- Symptom: valid context disappears when prompt is large.
- Fix: treat as context overflow/prompt truncation; rebudget prompt sections and retry retrieval with stricter filters.

- Symptom: route picks wrong tool.
- Fix: tighten intent classes, add confidence thresholds and fallback rules.

- Symptom: training unstable.
- Fix: lower learning rate, check batch quality, use gradient clipping.

---

## 12) Personal revision checklist

- I can explain zero-shot vs few-shot with one example.
- I can explain epoch, batch, step clearly.
- I can describe backprop + gradient descent in 30 seconds.
- I can explain prompt lifecycle with and without RAG.
- I can justify when RAG is needed and when long-context is enough.
- I can explain hybrid retrieval with a practical example.
- I can explain API-first vs MCP-first choices.
- I can draw the key blocks of an AI system from memory.
