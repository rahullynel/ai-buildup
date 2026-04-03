# Transformers & LLM Basics

## What transformers do
- Process token sequences in parallel.
- Build contextual token representations layer by layer.
- Predict next token repeatedly to generate text.

## Self-attention (why it matters)
- Each token can reference other tokens in context.
- Helps with long-range dependencies and meaning disambiguation.
- Multi-head attention captures different relation patterns.

## Context windows
- Max tokens model can see in one request.
- If key info is outside window, model cannot directly use it.
- Bigger windows help coverage but increase cost/latency.

## Why LLMs hallucinate 
- Objective is likely text, not guaranteed truth.
- Missing context causes plausible guessing.
- Weak prompts and noisy retrieval increase wrong outputs.

## Add more notes
- 
