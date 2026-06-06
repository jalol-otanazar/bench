# Frontier RAG Stress Benchmark

A compact benchmark for testing modern retrieval-augmented generation systems on the failure modes that matter most:

- exact passage retrieval
- semantic disambiguation
- multi-hop synthesis
- structured enumeration
- temporal drift
- refusal on unsupported or false premises

This benchmark is fully self-contained. The source corpus lives in `benchmark/corpus/`, the question set is in `benchmark/questions.jsonl`, and the scoring helper is in `benchmark/eval.py`.

## Why this benchmark exists

Many RAG systems look strong on obvious fact lookup but break when they face:

- near-duplicate distractors
- conflicting wording across documents
- dated policy changes
- list/order sensitivity
- unsupported assumptions that should be rejected instead of answered

This benchmark is built to surface those failures.

## Files

- `benchmark/corpus/` - the source documents used for grounding
- `benchmark/questions.jsonl` - benchmark questions and answer keys
- `benchmark/eval.py` - simple evaluation script for model outputs

## Output format

Model outputs should be saved as JSON Lines, one prediction per question:

```json
{"id":"E1","answer":"USD 60 per day","citations":["policies.md"]}
```

The `citations` field is optional but recommended.

## Scoring idea

The helper script is intentionally simple and opinionated:

- exact retrieval and structured questions are scored by answer match
- multi-hop and refusal questions allow keyword-based partial validation
- citation presence can be checked separately if your system emits sources

This benchmark is meant to be a living repo. Add harder documents, more ambiguous distractors, and new question families as your RAG system improves.