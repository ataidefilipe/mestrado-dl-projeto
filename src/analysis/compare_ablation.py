"""
Decomposes the A -> B gain into:
  A  -> B0 : effect of session-wise extraction (bug fix), no temporal mechanism
  B0 -> B  : effect of the temporal mechanism (validity windows, SUPERSEDES, V(f, t_query), tags)

Reads only eval summaries and Proposal B's encoded KB graphs; makes no API calls.
If the B0 summary does not exist yet, it reports A vs B only.

Usage:
  python src/analysis/compare_ablation.py
  python src/analysis/compare_ablation.py --b0 results/longmemeval_temporal_full/eval_results_b0/eval_summary.json
"""

import argparse
import json
import os
import sys
from datetime import datetime
from math import comb
from pathlib import Path
from typing import Dict, List, Optional, Tuple

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
RES = ROOT_DIR / "results"
DEFAULT_A = RES / "longmemeval_baseline_full" / "eval_results" / "eval_summary.json"
DEFAULT_B = RES / "longmemeval_temporal_full" / "eval_results" / "eval_summary.json"
DEFAULT_B0 = RES / "longmemeval_temporal_full" / "eval_results_b0" / "eval_summary.json"
DEFAULT_KB_DIR = RES / "longmemeval_temporal_full"

TYPE_ORDER = [
    "knowledge-update",
    "temporal-reasoning",
    "multi-session",
    "single-session-preference",
    "single-session-assistant",
    "single-session-user",
]


def load_correct(path: Path) -> Dict[str, Tuple[str, int]]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return {r["question_id"]: (r["question_type"], int(r["correct"])) for r in data["results"]}


def supersession_ids(kb_dir: Path, ids: List[str]) -> Optional[set]:
    """Items whose Proposal B KB graph has at least one superseded fact."""
    out, found = set(), 0
    for qid in ids:
        p = kb_dir / f"{qid}_long_term_kb_graph.json"
        if not p.exists():
            continue
        found += 1
        with open(p, "r", encoding="utf-8") as f:
            nodes = json.load(f).get("nodes", {})
        if any(n.get("metadata", {}).get("status") == "superseded" for n in nodes.values()):
            out.add(qid)
    return out if found else None


def rel(p: Path) -> str:
    try:
        return str(p.resolve().relative_to(ROOT_DIR))
    except ValueError:
        return str(p)


def mcnemar_exact(b: int, c: int) -> Tuple[float, float]:
    """Exact McNemar (binomial on discordant pairs). Returns (one-sided p for b > c, two-sided p)."""
    n = b + c
    if n == 0:
        return 1.0, 1.0
    tail_ge = sum(comb(n, k) for k in range(b, n + 1)) / 2 ** n
    tail_le = sum(comb(n, k) for k in range(0, b + 1)) / 2 ** n
    return tail_ge, min(1.0, 2 * min(tail_ge, tail_le))


def pair_stats(x: Dict, y: Dict, ids) -> Dict:
    gains = sum(1 for i in ids if x[i][1] == 0 and y[i][1] == 1)
    regs = sum(1 for i in ids if x[i][1] == 1 and y[i][1] == 0)
    p1, p2 = mcnemar_exact(gains, regs)
    return {"gains": gains, "regs": regs, "net": gains - regs, "p_one": p1, "p_two": p2}


def acc(d: Dict, ids) -> Tuple[int, int, float]:
    ids = list(ids)
    c = sum(d[i][1] for i in ids)
    return c, len(ids), (100.0 * c / len(ids) if ids else 0.0)


def fmt_acc(d, ids) -> str:
    c, n, a = acc(d, ids)
    return f"{c}/{n} ({a:.2f}%)"


def main() -> None:
    ap = argparse.ArgumentParser(description="A vs B0 vs B decomposition")
    ap.add_argument("--a", type=Path, default=DEFAULT_A)
    ap.add_argument("--b", type=Path, default=DEFAULT_B)
    ap.add_argument("--b0", type=Path, default=DEFAULT_B0)
    ap.add_argument("--kb_dir", type=Path, default=DEFAULT_KB_DIR)
    ap.add_argument("--out", type=Path, default=None, help="Markdown report path (default: reports/analysis/R05_...)")
    args = ap.parse_args()

    A, B = load_correct(args.a), load_correct(args.b)
    B0 = load_correct(args.b0) if args.b0.exists() else None

    ids = sorted(set(A) & set(B) & (set(B0) if B0 else set(B)))
    systems = [("A", A)] + ([("B0", B0)] if B0 else []) + [("B", B)]
    pairs = [("A", A, "B0", B0), ("B0", B0, "B", B)] if B0 else []
    pairs.append(("A", A, "B", B))

    sup = supersession_ids(args.kb_dir, ids)
    by_type: Dict[str, List[str]] = {}
    for i in ids:
        by_type.setdefault(A[i][0], []).append(i)
    types = [t for t in TYPE_ORDER if t in by_type] + sorted(t for t in by_type if t not in TYPE_ORDER)

    L: List[str] = []
    L.append("# R05 — Decomposição do ganho: A → B0 → B")
    L.append("")
    L.append(f"**Gerado em:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  ")
    L.append(f"**Itens pareados:** {len(ids)}  ")
    L.append(f"**Fontes:** A=`{rel(args.a)}`, B=`{rel(args.b)}`"
             + (f", B0=`{rel(args.b0)}`" if B0 else ""))
    L.append("")
    if not B0:
        L.append("> ⚠️ Resumo da B0 ainda não encontrado — relatório mostra apenas A vs B.")
        L.append("")
    L.append("- **A**: HeLa-Mem original (extração a cada 10 turnos; 360/500 grafos semânticos vazios).")
    L.append("- **B0**: fatos da extração por sessão de B, sem validade/supersessão, 𝒱≡1, só arestas de cadeia, prompt original do HeLa-Mem.")
    L.append("- **B**: Proposta completa (validade, SUPERSEDES, 𝒱(f, t_query), tags CURRENT/HISTORICAL).")
    L.append("")

    # 1. Accuracy per category
    L.append("## 1. Acurácia por categoria")
    L.append("")
    L.append("| Categoria | N | " + " | ".join(name for name, _ in systems) + " |")
    L.append("| :--- | :---: | " + " | ".join(":---:" for _ in systems) + " |")
    for t in types:
        L.append(f"| `{t}` | {len(by_type[t])} | " + " | ".join(fmt_acc(d, by_type[t]) for _, d in systems) + " |")
    L.append(f"| **OVERALL** | **{len(ids)}** | " + " | ".join(f"**{fmt_acc(d, ids)}**" for _, d in systems) + " |")
    L.append("")

    # 2. Paired comparisons
    L.append("## 2. Comparações pareadas (McNemar exato)")
    L.append("")
    L.append("| Comparação | Ganhos (0→1) | Regressões (1→0) | Saldo | Δ p.p. | p unilateral | p bilateral |")
    L.append("| :--- | :---: | :---: | :---: | :---: | :---: | :---: |")
    for xn, x, yn, y in pairs:
        s = pair_stats(x, y, ids)
        L.append(f"| {xn} → {yn} | +{s['gains']} | -{s['regs']} | {s['net']:+d} | {100 * s['net'] / len(ids):+.2f} "
                 f"| {s['p_one']:.4f} | {s['p_two']:.4f} |")
    L.append("")

    # 3. Per-category saldo for each step
    L.append("## 3. Saldo líquido por categoria e etapa")
    L.append("")
    L.append("| Categoria | " + " | ".join(f"{xn} → {yn}" for xn, _, yn, _ in pairs) + " |")
    L.append("| :--- | " + " | ".join(":---:" for _ in pairs) + " |")
    for t in types:
        cells = []
        for _, x, _, y in pairs:
            s = pair_stats(x, y, by_type[t])
            cells.append(f"{s['net']:+d} (+{s['gains']}/-{s['regs']})")
        L.append(f"| `{t}` | " + " | ".join(cells) + " |")
    L.append("")

    # 4. Supersession subset
    if sup is not None:
        no_sup = [i for i in ids if i not in sup]
        with_sup = [i for i in ids if i in sup]
        L.append("## 4. Itens com vs. sem supersessão em B")
        L.append("")
        L.append("Sem supersessão, B e B0 diferem apenas no prompt (tags/instrução) e nas arestas EXTENDS; "
                 "o ranking por 𝒱 é idêntico. Com supersessão, o mecanismo temporal atua de fato.")
        L.append("")
        L.append("| Subconjunto | N | " + " | ".join(name for name, _ in systems) + " | "
                 + " | ".join(f"Saldo {xn}→{yn}" for xn, _, yn, _ in pairs) + " |")
        L.append("| :--- | :---: | " + " | ".join(":---:" for _ in systems) + " | "
                 + " | ".join(":---:" for _ in pairs) + " |")
        for label, sub in (("Com supersessão", with_sup), ("Sem supersessão", no_sup)):
            if not sub:
                continue
            L.append(f"| {label} | {len(sub)} | " + " | ".join(fmt_acc(d, sub) for _, d in systems) + " | "
                     + " | ".join(f"{pair_stats(x, y, sub)['net']:+d}" for _, x, _, y in pairs) + " |")
        L.append("")

    # 5. Reading guide
    L.append("## 5. Leitura")
    L.append("")
    L.append("- **A → B0** mede quanto do ganho vem só de corrigir a extração (fatos existirem para todos os itens).")
    L.append("- **B0 → B** mede a contribuição do mecanismo temporal; é este o teste da hipótese do trabalho.")
    L.append("- Geração e juiz usam `temperature=0.7` (`hela_mem/utils.py`), então parte dos pares discordantes é ruído "
             "de amostragem. Para calibrar, rode B novamente (`--results_subdir eval_results_b_rerun`) e compare B vs B'.")
    L.append("")

    report = "\n".join(L)
    print(report)

    out = args.out or (ROOT_DIR / "reports" / "analysis" /
                       f"R05_decomposicao_A_B0_B_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md")
    os.makedirs(out.parent, exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"\n[Relatório] Salvo em: {out}")


if __name__ == "__main__":
    main()
