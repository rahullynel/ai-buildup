# Prompt Lifecycle (With and Without RAG)

## Without RAG
1. User query
2. Prompt template
3. LLM generation
4. Answer

Flow:
User -> Prompt Builder -> LLM -> Answer

## With RAG
1. User query
2. Retrieval (top candidates)
3. Rerank/select context
4. Prompt build with context
5. LLM generation
6. Answer with evidence/citations

Flow:
User -> Retriever -> Reranker -> Prompt Builder -> LLM -> Answer

## Key difference
- Without RAG: relies mostly on parametric memory.
- With RAG: relies on retrieved evidence + model reasoning.

## Who controls context size?
- Orchestrator/prompt builder controls context selection and trimming.
- Tokenizer only converts text to tokens and checks limits.
- LLM then applies self-attention on the final packed prompt.

## When context is dropped due to token limits
- Not a training failure.
- Better terms: context overflow, prompt truncation, context dilution.

Pipeline response should be:
- Re-rank and keep higher-signal chunks.
- Reduce top-k.
- Compress long chunks.
- Reserve token budget for user query and final instructions.

## Context overshadowing risk
If too much retrieved text is injected, user intent gets buried.

Symptoms:
- Model answers from generic chunk content, not user ask.
- Response ignores key constraints from user query.

Mitigations:
- Strong reranking + metadata filters.
- Bounded chunk size.
- Section-level token budgets.
- Prompt layout that keeps user query salient.

## Add more notes
- 
