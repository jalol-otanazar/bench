# Frontier RAG Stress Benchmark

This benchmark is designed to stress modern retrieval-augmented generation systems on the failure modes that matter most in production:

- exact retrieval under noise
- semantic disambiguation across similar wording
- multi-hop synthesis across documents
- structure-sensitive list extraction
- temporal drift and version awareness
- refusal when the corpus does not support the claim
- source attribution under conflicting evidence

## Corpus
The corpus is intentionally small but dense. It contains policy, incident, FAQ, release note, runbook, and vendor agreement documents.

## Evaluation targets
A strong system should:

1. retrieve the correct supporting passage
2. rank it near the top of retrieval results
3. answer only from retrieved evidence
4. refuse unsupported or false premises
5. cite the correct source document when available

## Recommended metrics
- Recall@1 / Recall@5 / Recall@10
- MRR
- NDCG
- Answer accuracy
- Refusal accuracy
- Citation hit rate

## Question families

### Exact retrieval
Questions with direct answers from one passage.

### Temporal/versioning
Questions that require the system to identify the current document instead of an archived one.

### Multi-hop synthesis
Questions that require combining two documents.

### Semantic disambiguation
Questions that use repeated words such as retention, response time, or support across multiple docs.

### Structured enumeration
Questions that require the exact order and completeness of lists.

### Refusal
Questions that contain a false premise or ask for information not present in the corpus.

## Output format
Each prediction should be one JSON object per line:

```json
{"id":"E1","answer":"Borealis","citations":["benchmark/corpus/incident_borealis.md"]}
```

The `citations` field is optional but recommended.

## Notes
This benchmark is synthetic by design. It is meant to be easy to extend with more adversarial documents, more conflicting versions, and more difficult negative examples.