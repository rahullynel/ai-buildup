# Portfolio Project Architecture

## Building blocks
- Local RAG assistant
- Orchestrator layer
- Hybrid retrieval
- Vector DB
- Local LLM wrapper

## End-to-end flow
1. User query enters orchestrator.
2. Orchestrator chooses API/retrieval/LLM path.
3. Context builder merges relevant evidence.
4. Local LLM generates grounded answer.
5. Return answer with source references.

## Key design choices
- Keep retrieval and generation modular.
- Use metadata filters and reranking.
- Add fallback behavior for low-confidence cases.

## Add more notes
- 
