# Local LLM Basics

## Running locally
- Tools like Ollama make local serving easy.
- GGUF is a common quantized model format.

## Quantization
- Reduce precision to cut memory and speed up inference.
- Typical levels: 8-bit, 4-bit.
- Tradeoff: too much quantization can reduce quality.

## When local models are useful
- Privacy-sensitive use cases.
- Offline usage.
- Better cost control.

## Local vs cloud tradeoff
- Local: control/privacy, but hardware-limited.
- Cloud: stronger models/scaling, but recurring cost.

## Add more notes
- 

## Related pipeline note (token limits)
- Tokenizer itself is mechanical: tokenize + count + limit check.
- In RAG systems, orchestrator/prompt builder decides what context to keep/drop/compress.
- If context is dropped at inference, call it context overflow or prompt truncation (not underfitting).

For deeper revision, see orchestration and retrieval notes in:
- 03-orchestration/
- 02-retrieval/
