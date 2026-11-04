"""
Auditoria reprodutível do processo experimental (registro R05).

Verifica, sem chamadas de API:
  1. Hiperparâmetros usados na Baseline A vs. scripts oficiais do HeLa-Mem.
  2. O que mudou entre a rodada de 64,60% (commit d279613) e a de 65,60% (f05bfda) da Proposta B.

Pré-requisitos:
  - submódulo external/HeLa-Mem inicializado (git submodule update --init)
  - results/temporal_encoded_500.zip presente
  - repositório git com o commit d279613

Uso:
  python src/analysis/audit_process.py
"""

import json
import re
import subprocess
import sys
import zipfile
from collections import Counter
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent.parent
HELA = ROOT / "external" / "HeLa-Mem"
A_SUM = ROOT / "results" / "longmemeval_baseline_full" / "eval_results" / "eval_summary.json"
B_SUM = ROOT / "results" / "longmemeval_temporal_full" / "eval_results" / "eval_summary.json"
B_ZIP = ROOT / "results" / "temporal_encoded_500.zip"
OLD_B_COMMIT = "d279613"
OLD_B_PATH = "results/longmemeval_temporal_full/eval_results/eval_summary.json"


def by_id(results):
    return {r["question_id"]: r for r in results}


def audit_hyperparams() -> None:
    print("=" * 70)
    print("1. Hiperparâmetros: Baseline A vs. scripts oficiais")
    print("=" * 70)
    params = json.load(open(A_SUM, encoding="utf-8"))["params"]
    script = (HELA / "scripts" / "eval_longmemeval.sh").read_text(encoding="utf-8")
    official = dict(re.findall(r'export (HEBBIAN_\w+)="\$\{\w+:-([^}]+)\}"', script))
    mapping = {
        "HEBBIAN_MAX_FLIPPED": "max_flipped",
        "HEBBIAN_KEYWORD_WEIGHT": "keyword_weight",
        "HEBBIAN_LEARNING_RATE": "learning_rate",
        "HEBBIAN_ACTIVATION_ALPHA": "activation_alpha",
        "HEBBIAN_SPREADING_THRESHOLD": "spreading_threshold",
        "HEBBIAN_DECAY_RATE": "decay_rate",
        "HEBBIAN_TAU": "tau",
        "HEBBIAN_TOP_K": "top_k",
        "HEBBIAN_SEMANTIC_TOP_K": "semantic_top_k",
    }
    print(f"{'parâmetro':<30}{'script oficial':>16}{'Baseline A':>14}  status")
    for env, key in mapping.items():
        off = official.get(env, "-")
        got = str(params.get(key, "-"))
        same = off == "-" or float(off) == float(got)
        print(f"{env:<30}{off:>16}{got:>14}  {'ok' if same else 'DIVERGE'}")
    print()


def audit_reencoding() -> None:
    print("=" * 70)
    print(f"2. Proposta B: rodada {OLD_B_COMMIT} (64,60%) vs. atual (65,60%)")
    print("=" * 70)
    old_raw = subprocess.run(
        ["git", "show", f"{OLD_B_COMMIT}:{OLD_B_PATH}"],
        cwd=ROOT, capture_output=True, check=True,
    ).stdout.decode("utf-8")
    old = by_id(json.loads(old_raw)["results"])
    new = by_id(json.load(open(B_SUM, encoding="utf-8"))["results"])
    A = by_id(json.load(open(A_SUM, encoding="utf-8"))["results"])
    data = json.load(open(HELA / "data" / "longmemeval_s.json", encoding="utf-8"))
    pos = {d["question_id"]: i for i, d in enumerate(data)}

    with zipfile.ZipFile(B_ZIP) as z:
        reenc = sorted(
            info.filename.replace("_long_term_kb_graph.json", "")
            for info in z.infolist()
            if info.filename.endswith("_long_term_kb_graph.json") and info.date_time[:3] == (2026, 11, 3)
        )

    empty_old = [q for q, r in old.items() if r.get("num_semantic_retrieved") == 0]
    changed_outside = [q for q in new if q not in reenc and old[q]["correct"] != new[q]["correct"]]

    print(f"Itens recodificados em 2026-11-03: {len(reenc)}")
    print(f"Posições no dataset: {min(pos[q] for q in reenc)}–{max(pos[q] for q in reenc)}")
    print(f"Tipos: {dict(Counter(old[q]['question_type'] for q in reenc))}")
    print(f"Itens com 0 fatos recuperados na rodada antiga: {len(empty_old)} "
          f"(todos recodificados: {set(empty_old) <= set(reenc)})")
    print(f"Acertos nesses itens — A: {sum(A[q]['correct'] for q in reenc)} | "
          f"B antiga: {sum(old[q]['correct'] for q in reenc)} | B atual: {sum(new[q]['correct'] for q in reenc)}")
    print(f"Itens fora do lote que mudaram de resultado: {len(changed_outside)}")
    print(f"Total — B antiga: {sum(r['correct'] for r in old.values())} | B atual: {sum(r['correct'] for r in new.values())}")
    ku_old = sum(r["correct"] for r in old.values() if r["question_type"] == "knowledge-update")
    ku_new = sum(r["correct"] for r in new.values() if r["question_type"] == "knowledge-update")
    ku_a = sum(r["correct"] for r in A.values() if r["question_type"] == "knowledge-update")
    print(f"knowledge-update (78) — A: {ku_a} | B antiga: {ku_old} | B atual: {ku_new}")
    print()


if __name__ == "__main__":
    audit_hyperparams()
    audit_reencoding()
