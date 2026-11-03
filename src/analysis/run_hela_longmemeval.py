"""
Runner script for HeLa-Mem LongMemEval-S baseline replication.
Preserves HeLa-Mem original code untouched by importing it directly from external/HeLa-Mem.
Loads credentials from .env and records analytical reports into reports/analysis/.
"""

import os
import sys
import json
import time
import argparse
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# 1. Configure UTF-8 encoding for stdout/stderr to avoid Windows charmap errors
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# 2. Load .env credentials from project root
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(ROOT_DIR / ".env")

# Verify OPENAI_API_KEY
if not os.environ.get("OPENAI_API_KEY"):
    raise RuntimeError(
        "OPENAI_API_KEY is not set. Please ensure it exists in your environment or .env file."
    )

# 2. Add external/HeLa-Mem to Python path
HELA_DIR = ROOT_DIR / "external" / "HeLa-Mem"
if not HELA_DIR.exists():
    raise RuntimeError(f"HeLa-Mem directory not found at: {HELA_DIR}")

sys.path.insert(0, str(HELA_DIR))

# Import HeLa-Mem modules directly (untouched original code)
from hela_mem.encode_longmemeval import encode_longmemeval
from hela_mem.eval_longmemeval import eval_longmemeval


def generate_markdown_report(
    eval_summary: dict,
    run_type: str,
    num_items: int,
    start_item: int,
    elapsed_time: float,
    output_report_path: Path,
) -> None:
    """Generate a structured Markdown report following AGENT.MD guidelines."""
    overall_acc = eval_summary.get("overall_accuracy", 0.0)
    total_items = eval_summary.get("total_items", 0)
    total_correct = eval_summary.get("total_correct", 0)
    per_type = eval_summary.get("per_type", {})
    params = eval_summary.get("params", {})

    lines = [
        f"# Relatório de Replicação — HeLa-Mem Baseline ({run_type.upper()})",
        "",
        f"**Data da Execução:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"**Commit Base:** `68f19b3fac8c6156570d5aeb3a7a3e8f3ba7cb04` (oficial)",
        f"**Dataset:** `external/HeLa-Mem/data/longmemeval_s.json`",
        f"**Itens Avaliados:** {total_items} (acertos: {total_correct}, fatia [{start_item}:{start_item + num_items}])",
        f"**Tempo Total:** {elapsed_time:.1f}s ({elapsed_time/60:.2f} min)",
        "",
        "---",
        "",
        "## 1. Parâmetros de Execução",
        "",
        "```json",
        json.dumps(params, indent=2),
        "```",
        "",
        "---",
        "",
        "## 2. Resultados Consolidados",
        "",
        f"### Acurácia Geral (Overall ACC): **{overall_acc:.2f}%** ({total_correct}/{total_items})",
        "",
        "| Categoria / Question Type | Total | Acertos | ACC (%) |",
        "| :--- | :---: | :---: | :---: |",
    ]

    for qtype, metrics in sorted(per_type.items()):
        cnt = metrics.get("total", 0)
        corr = metrics.get("correct", 0)
        acc = metrics.get("accuracy", 0.0)
        lines.append(f"| `{qtype}` | {cnt} | {corr} | **{acc:.2f}%** |")

    lines.extend([
        "",
        "---",
        "",
        "## 3. Comparação com a Meta do Artigo Oficial (500 itens)",
        "",
        "| Categoria | Meta Paper (500 itens) | Obtido nesta execução |",
        "| :--- | :---: | :---: |",
        f"| **Overall** | **65.40%** | **{overall_acc:.2f}%** |",
        f"| Temporal Reasoning | 50.38% | {per_type.get('temporal-reasoning', {}).get('accuracy', 'N/A')}% |",
        f"| Knowledge Update | 78.21% | {per_type.get('knowledge-update', {}).get('accuracy', 'N/A')}% |",
        f"| Multi-Session | 57.14% | {per_type.get('multi-session', {}).get('accuracy', 'N/A')}% |",
        f"| Single-Session User | 78.85% | {per_type.get('single-session-user', {}).get('accuracy', 'N/A')}% |",
        "",
        "> [!NOTE]",
        f"> {'Esta execução cobre a totalidade do benchmark LongMemEval-S (500 itens). Os resultados consolidam a baseline oficial congelada.' if num_items >= 500 else 'Esta execução foi um teste piloto de sanity check. Os números por categoria possuem maior variância estatística devido ao tamanho reduzido da amostra.'}",
        "",
    ])

    output_report_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"\n[Relatório] Relatório detalhado salvo em: {output_report_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Executa replicação da baseline HeLa-Mem")
    parser.add_argument(
        "--stage",
        choices=["all", "encode", "eval"],
        default="all",
        help="Etapa a executar: all, encode, ou eval (default: all)",
    )
    parser.add_argument(
        "--data_path",
        type=str,
        default=str(HELA_DIR / "data" / "longmemeval_s.json"),
        help="Caminho para o dataset LongMemEval-S",
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        default=str(ROOT_DIR / "results" / "longmemeval_baseline"),
        help="Diretório de saída para os grafos e resultados",
    )
    parser.add_argument(
        "--num_items",
        type=int,
        default=10,
        help="Número de itens para codificar/avaliar (default: 10 para piloto)",
    )
    parser.add_argument(
        "--start_item",
        type=int,
        default=0,
        help="Índice inicial (default: 0)",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=5,
        help="Número de threads simultâneas (default: 5)",
    )
    parser.add_argument(
        "--top_k",
        type=int,
        default=15,
        help="Top-k de recuperação episódica (default: 15, conforme README oficial)",
    )
    parser.add_argument(
        "--semantic_top_k",
        type=int,
        default=5,
        help="Top-k de recuperação semântica (default: 5, conforme README oficial)",
    )
    parser.add_argument(
        "--skip_knowledge",
        action="store_true",
        help="Ignorar extração incremental de conhecimento (default: False)",
    )
    parser.add_argument(
        "--use_consolidation",
        action="store_true",
        help="Executar consolidação reflexiva antes do eval (default: False)",
    )

    args = parser.parse_args()

    print("=" * 80)
    print(f"Iniciando Replicação HeLa-Mem Baseline — Etapa: {args.stage.upper()}")
    print(f"Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Dataset: {args.data_path}")
    print(f"Itens: [{args.start_item}:{args.start_item + args.num_items}] ({args.num_items} itens)")
    print(f"Workers: {args.workers}")
    print(f"Diretório de Resultados: {args.output_dir}")
    print("=" * 80)

    t_start = time.time()
    os.makedirs(args.output_dir, exist_ok=True)

    # 1. Encoding
    if args.stage in ("all", "encode"):
        print("\n>>> ETAPA 1: Codificação dos Grafos de Memória (Encoding) <<<")
        encode_longmemeval(
            data_path=args.data_path,
            output_dir=args.output_dir,
            num_items=args.num_items,
            start_item=args.start_item,
            workers=args.workers,
            skip_knowledge=args.skip_knowledge,
        )

    # 2. Evaluation
    if args.stage in ("all", "eval"):
        print("\n>>> ETAPA 2: Avaliação e Juiz LLM (Evaluation) <<<")
        eval_longmemeval(
            data_path=args.data_path,
            mem_dir=args.output_dir,
            num_items=args.num_items,
            start_item=args.start_item,
            top_k=args.top_k,
            semantic_top_k=args.semantic_top_k,
            use_consolidation=args.use_consolidation,
            workers=args.workers,
        )

        # 3. Gerar relatório
        summary_path = Path(args.output_dir) / "eval_results" / "eval_summary.json"
        if summary_path.exists():
            with open(summary_path, "r", encoding="utf-8") as f:
                eval_summary = json.load(f)

            elapsed = time.time() - t_start
            tag = "pilot" if args.num_items < 500 else "full"
            ts_str = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_path = (
                ROOT_DIR
                / "reports"
                / "analysis"
                / f"R03_reproducao_hela_{tag}_{ts_str}.md"
            )
            generate_markdown_report(
                eval_summary=eval_summary,
                run_type=tag,
                num_items=args.num_items,
                start_item=args.start_item,
                elapsed_time=elapsed,
                output_report_path=report_path,
            )

    print("\nExecução finalizada com sucesso!")


if __name__ == "__main__":
    main()
