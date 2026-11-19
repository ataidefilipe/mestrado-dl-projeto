"""
Extracts a stratified sample of SUPERSEDES transitions from Proposal B and Proposal B_v2
to audit classifier precision and over-supersession (especially in multi-session vs knowledge-update).
Makes zero API calls.
"""

import csv
import glob
import json
import os
import random
import sys
from pathlib import Path
from typing import Any, Dict, List

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
DATA_PATH = ROOT_DIR / "external" / "HeLa-Mem" / "data" / "longmemeval_s.json"
OUT_DIR = ROOT_DIR / "reports" / "analysis"


def collect_supersessions(kb_dir: Path, id2item: Dict[str, Dict[str, Any]]) -> List[Dict[str, Any]]:
    records = []
    for path_str in sorted(glob.glob(str(kb_dir / "*_long_term_kb_graph.json"))):
        qid = os.path.basename(path_str).replace("_long_term_kb_graph.json", "")
        item = id2item.get(qid, {})
        cat = item.get("question_type", "unknown")
        with open(path_str, "r", encoding="utf-8") as f:
            nodes = json.load(f).get("nodes", {})
        for nid, node in nodes.items():
            meta = node.get("metadata", {})
            if meta.get("status") == "superseded" and meta.get("superseded_by") is not None:
                new_id = str(meta["superseded_by"])
                new_node = nodes.get(new_id, {})
                records.append({
                    "question_id": qid,
                    "question_type": cat,
                    "question": item.get("question", ""),
                    "old_id": nid,
                    "old_time": meta.get("valid_from", node.get("timestamp", "")),
                    "old_fact": node.get("content", ""),
                    "new_id": new_id,
                    "new_time": meta.get("valid_to", new_node.get("timestamp", "")),
                    "new_fact": new_node.get("content", ""),
                })
    return records


def sample_stratified(records: List[Dict[str, Any]], per_cat: int = 15, seed: int = 42) -> List[Dict[str, Any]]:
    rng = random.Random(seed)
    by_cat: Dict[str, List[Dict[str, Any]]] = {}
    for r in records:
        by_cat.setdefault(r["question_type"], []).append(r)
    sampled = []
    for cat in ("knowledge-update", "multi-session", "temporal-reasoning"):
        pool = by_cat.get(cat, [])
        k = min(per_cat, len(pool))
        sampled.extend(rng.sample(pool, k))
    return sampled


def main() -> None:
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        dataset = json.load(f)
    id2item = {it["question_id"]: it for it in dataset}

    for label, dirname in [("B", "longmemeval_temporal_full"), ("B_v2", "longmemeval_temporal_v2")]:
        kb_dir = ROOT_DIR / "results" / dirname
        recs = collect_supersessions(kb_dir, id2item)
        sample = sample_stratified(recs, per_cat=15, seed=42)

        csv_path = OUT_DIR / f"audit_supersession_sample_{label}.csv"
        with open(csv_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=[
                    "question_id", "question_type", "old_time", "old_fact",
                    "new_time", "new_fact", "question", "audit_label", "notes",
                ],
            )
            writer.writeheader()
            for r in sample:
                writer.writerow({
                    "question_id": r["question_id"],
                    "question_type": r["question_type"],
                    "old_time": r["old_time"],
                    "old_fact": r["old_fact"],
                    "new_time": r["new_time"],
                    "new_fact": r["new_fact"],
                    "question": r["question"],
                    "audit_label": "",
                    "notes": "",
                })
        print(f"[{label}] Total SUPERSEDES={len(recs)} | Sampled={len(sample)} -> {csv_path}")


if __name__ == "__main__":
    main()
