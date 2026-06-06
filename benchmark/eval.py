#!/usr/bin/env python3
"""Simple evaluator for the Frontier RAG Stress Benchmark.

Expected prediction format: JSON Lines, one object per question.
Each line should include:
  - id: question id
  - answer: model output
  - citations: optional list of source document paths or names

Example:
  {"id": "E1", "answer": "Borealis", "citations": ["benchmark/corpus/incident_borealis.md"]}
"""

from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

REFUSAL_MARKERS = [
    "not stated",
    "not in the corpus",
    "cannot determine",
    "unsupported",
    "no evidence",
    "not provided",
    "does not say",
]


def normalize(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def load_jsonl(path: Path) -> List[dict]:
    rows: List[dict] = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
    return rows


def citation_basename(value: str) -> str:
    return Path(value).name.lower()


def citation_hit(gold: dict, pred: dict) -> float:
    gold_docs = gold.get("supporting_docs") or []
    pred_citations = pred.get("citations") or []
    if not gold_docs:
        return 1.0 if not pred_citations else 0.0
    if isinstance(pred_citations, str):
        pred_citations = [pred_citations]

    gold_norm = {normalize(doc) for doc in gold_docs}
    gold_base = {citation_basename(doc) for doc in gold_docs}

    for citation in pred_citations:
        c_norm = normalize(str(citation))
        c_base = citation_basename(str(citation))
        if c_norm in gold_norm or c_base in gold_base:
            return 1.0
    return 0.0


def answer_score(gold: dict, pred_answer: str) -> float:
    answer_type = gold.get("answer_type", "exact")
    gold_answer = gold.get("answer", "")
    pred_norm = normalize(pred_answer or "")
    gold_norm = normalize(gold_answer or "")

    if answer_type == "list":
        required = gold.get("required_items") or []
        if not required:
            return 0.0
        return 1.0 if all(normalize(item) in pred_norm for item in required) else 0.0

    if answer_type == "refusal":
        required = gold.get("required_items") or []
        if required and all(normalize(item) in pred_norm for item in required):
            return 1.0
        if any(marker in pred_norm for marker in REFUSAL_MARKERS):
            return 1.0
        return 0.0

    if not pred_norm or not gold_norm:
        return 0.0

    if pred_norm == gold_norm:
        return 1.0
    if gold_norm in pred_norm or pred_norm in gold_norm:
        return 1.0
    return 0.0


def main() -> int:
    parser = argparse.ArgumentParser(description="Evaluate Frontier RAG Stress Benchmark predictions.")
    parser.add_argument("--gold", type=Path, required=True, help="Path to benchmark/questions.jsonl")
    parser.add_argument("--predictions", type=Path, required=True, help="Path to model predictions JSONL")
    args = parser.parse_args()

    gold_rows = load_jsonl(args.gold)
    pred_rows = load_jsonl(args.predictions)
    preds: Dict[str, dict] = {row["id"]: row for row in pred_rows if "id" in row}

    category_totals = defaultdict(float)
    category_counts = defaultdict(int)
    citation_totals = defaultdict(float)
    overall_answer = 0.0
    overall_citation = 0.0

    missing_ids: List[str] = []

    for gold in gold_rows:
        qid = gold["id"]
        pred = preds.get(qid, {})
        if qid not in preds:
            missing_ids.append(qid)

        a_score = answer_score(gold, pred.get("answer", ""))
        c_score = citation_hit(gold, pred)
        category = gold.get("category", "unknown")

        overall_answer += a_score
        overall_citation += c_score
        category_totals[category] += a_score
        citation_totals[category] += c_score
        category_counts[category] += 1

    total = len(gold_rows) or 1
    overall_answer_acc = overall_answer / total
    overall_citation_acc = overall_citation / total
    overall_score = 0.85 * overall_answer_acc + 0.15 * overall_citation_acc

    print(json.dumps({
        "total_questions": total,
        "answer_accuracy": round(overall_answer_acc, 4),
        "citation_hit_rate": round(overall_citation_acc, 4),
        "overall_score": round(overall_score, 4),
        "missing_predictions": missing_ids,
    }, indent=2))

    print("\nCategory breakdown:")
    for category in sorted(category_counts):
        count = category_counts[category]
        ans = category_totals[category] / count if count else 0.0
        cit = citation_totals[category] / count if count else 0.0
        score = 0.85 * ans + 0.15 * cit
        print(f"- {category}: answer={ans:.3f}, citation={cit:.3f}, score={score:.3f} ({count} items)")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
