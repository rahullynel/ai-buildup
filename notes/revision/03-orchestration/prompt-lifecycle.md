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

## Add more notes
- 
