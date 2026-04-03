# Learning Modes, Epochs, and Training Loop

## Zero-shot vs one-shot vs few-shot
- Zero-shot: instruction only.
- One-shot: single example in prompt.
- Few-shot: multiple examples for pattern control.

## Core terms
- Sample: one data point.
- Batch: group of samples in one update.
- Step/iteration: one optimizer update.
- Epoch: one full pass over dataset.

## Training flow
1. Forward pass on batch.
2. Compute loss.
3. Backpropagate gradients.
4. Optimizer updates weights.
5. Repeat across batches and epochs.

## Gradient descent
- Updates parameters opposite to gradient direction.
- Learning rate controls update size.

## Backpropagation
- Uses chain rule to compute parameter gradients efficiently.

## What changes with error delta
- Usually data stays fixed.
- Model weights change based on gradient magnitude/direction.
- Larger error signal can produce larger updates.

## Backtracking notes
- Optimization context: reduce step size when loss gets worse.
- Agent context: retry alternative tool/path when output is weak.

## Add more notes
- 
