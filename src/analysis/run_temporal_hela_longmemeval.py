"""
Execution runner for Temporal Validity-Aware HeLa-Mem on LongMemEval-S.
Supports:
1. Resumable checkpointing (idempotent, skips already processed items)
2. Controlled episodic reuse from Baseline A (ensures rigorous A/B comparison)
3. Stepwise execution: --stage encode, --stage eval, or --stage all
4. Targeted testing on specific case IDs (--target_ids 07741c44,07741c45)
5. Automated side-by-side comparison report against Baseline A
"""

import os
import sys
import json
import time
import shutil
import argparse
from datetime import datetime
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Dict, List, Optional, Tuple
from dotenv import load_dotenv

# UTF-8 encoding for Windows streams
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(ROOT_DIR / ".env")

HELA_DIR = ROOT_DIR / "external" / "HeLa-Mem"
sys.path.insert(0, str(ROOT_DIR))
sys.path.insert(0, str(HELA_DIR))

from hela_mem.hebbian_memory import HebbianMemoryGraph
from hela_mem.profile_utils import OpenAIClient, gpt_personality_analysis, gpt_update_profile
from hela_mem.eval_longmemeval import (
    get_anscheck_prompt,
    parse_judge_response,
    CORRUPTED_INDICES,
)
from hela_mem.utils import (
    load_api_keys,
    gpt_generate_answer_with_rotation,
    get_timestamp,
    get_embedding,
)
from src.modeling.temporal_knowledge_memory import TemporalKnowledgeMemory, parse_date
from src.modeling.validity_aware_retriever import ValidityAwareRetriever


def extract_session_turns(item: Dict[str, Any]) -> List[Tuple[str, List[Dict[str, str]]]]:
    """
    Groups turns by session to preserve explicit session timestamps.
    Returns: List of (session_date, list_of_turns)
    """
    sessions = item.get("haystack_sessions", [])
    dates = item.get("haystack_dates", [])
    grouped = []

    for s_idx, session in enumerate(sessions):
        date = dates[s_idx] if s_idx < len(dates) else get_timestamp()
        turns = []
        start = 0
        while start < len(session) and session[start].get("role") != "user":
            start += 1
        i = start
        while i + 1 < len(session):
            if session[i].get("role") == "user" and session[i + 1].get("role") == "assistant":
                turns.append({
                    "user_text": session[i].get("content", ""),
                    "ai_text": session[i + 1].get("content", ""),
                    "timestamp": date,
                })
                i += 2
            else:
                i += 1
        if turns:
            grouped.append((date, turns))

    return grouped


def encode_single_temporal_item(
    item: Dict[str, Any],
    output_dir: str,
    client: Any,
    reuse_episodic_dir: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Encodes one item into Temporal Knowledge Memory.
    Optionally reuses existing episodic graph from baseline.
    """
    item_id = item["question_id"]
    t_start = time.time()

    mem_path = os.path.join(output_dir, f"{item_id}_hebbian.json")
    kb_path = os.path.join(output_dir, f"{item_id}_long_term.json")
    kb_graph_path = os.path.join(output_dir, f"{item_id}_long_term_kb_graph.json")

    # Checkpoint check (must also have non-empty KB graph nodes)
    if os.path.exists(kb_path) and os.path.exists(kb_graph_path):
        try:
            with open(kb_graph_path, "r", encoding="utf-8") as _f:
                _kb_data = json.load(_f)
            if len(_kb_data.get("nodes", {})) > 0:
                print(f"  [{item_id}] Temporal knowledge already exists ({len(_kb_data['nodes'])} facts), skipping encode.")
                return {"item_id": item_id, "status": "skipped", "encoding_time": 0.0}
        except Exception:
            pass

    # 1. Setup episodic graph
    if reuse_episodic_dir:
        src_mem = os.path.join(reuse_episodic_dir, f"{item_id}_hebbian.json")
        if os.path.exists(src_mem):
            shutil.copy2(src_mem, mem_path)
            memory_graph = HebbianMemoryGraph(file_path=mem_path)
        else:
            raise FileNotFoundError(f"Source episodic memory not found at: {src_mem}")
    else:
        memory_graph = HebbianMemoryGraph(file_path=mem_path)

    # 2. Setup Temporal Knowledge Memory
    temporal_kb = TemporalKnowledgeMemory(file_path=kb_path)

    session_groups = extract_session_turns(item)
    total_facts = 0

    for session_date, turns in session_groups:
        dialogs = [
            {
                "user_input": t["user_text"],
                "agent_response": t["ai_text"],
                "timestamp": session_date,
            }
            for t in turns
        ]

        try:
            analysis = gpt_personality_analysis(dialogs, client)
            new_profile = analysis.get("profile", "")
            new_private = analysis.get("private", "")
            assistant_knowledge = analysis.get("assistant_knowledge", "")

            # Merge profile
            old_profile = temporal_kb.get_raw_user_profile(item_id)
            if old_profile:
                updated_profile = gpt_update_profile(old_profile, new_profile, client)
            else:
                updated_profile = new_profile
            temporal_kb.update_user_profile(item_id, updated_profile)

            # Add facts with real session timestamp & supersession checking
            if new_private and new_private.strip().lower() not in ("none", "- none", ""):
                for line in new_private.split("\n"):
                    fact = line.strip().lstrip("- ").strip()
                    if fact and fact.lower() != "none" and not fact.startswith("【"):
                        temporal_kb.add_knowledge(fact, event_timestamp=session_date, client=client)
                        total_facts += 1

            # Add assistant knowledge
            if assistant_knowledge and assistant_knowledge.strip().lower() != "none":
                for line in assistant_knowledge.split("\n"):
                    ak = line.strip().lstrip("- ").strip()
                    if ak and ak.lower() != "none" and not ak.startswith("【"):
                        temporal_kb.add_assistant_knowledge(ak)

        except Exception as e:
            print(f"  [{item_id}] Extraction error on session {session_date}: {e}")

    temporal_kb.save()
    if not reuse_episodic_dir:
        memory_graph.save()

    enc_time = time.time() - t_start
    print(f"  [{item_id}] Done: {total_facts} facts encoded in {enc_time:.1f}s")
    return {
        "item_id": item_id,
        "status": "encoded",
        "num_facts": total_facts,
        "encoding_time": enc_time,
    }


def evaluate_single_temporal_item(
    item: Dict[str, Any],
    item_idx: int,
    output_dir: str,
    top_k: int = 15,
    semantic_top_k: int = 5,
    results_dir: Optional[str] = None,
) -> Dict[str, Any]:
    """Evaluates a single item using ValidityAwareRetriever and LLM judge."""
    item_id = item["question_id"]
    question_type = item["question_type"]
    question = item["question"]
    answer = item["answer"]
    question_date = item.get("question_date", "")
    is_abstention = "abs" in item_id

    # Checkpoint check
    if results_dir:
        res_file = os.path.join(results_dir, f"result_{item_id}.json")
        if os.path.exists(res_file):
            try:
                with open(res_file, "r", encoding="utf-8") as f:
                    cached = json.load(f)
                    print(f"  [{item_idx}] {item_id} - Loaded from checkpoint (Correct: {cached.get('correct')})")
                    return cached
            except Exception:
                pass

    t_start = time.time()

    if item_idx in CORRUPTED_INDICES:
        return {
            "question_id": item_id,
            "question_type": question_type,
            "correct": 0,
            "generated_answer": "[CORRUPTED]",
            "ground_truth": str(answer),
            "is_corrupted": True,
            "eval_time": 0.0,
        }

    mem_path = os.path.join(output_dir, f"{item_id}_hebbian.json")
    kb_path = os.path.join(output_dir, f"{item_id}_long_term.json")

    if not os.path.exists(mem_path) or not os.path.exists(kb_path):
        return {
            "question_id": item_id,
            "question_type": question_type,
            "correct": 0,
            "generated_answer": "[MISSING FILES]",
            "ground_truth": str(answer),
            "error": "missing memory files",
            "eval_time": 0.0,
        }

    memory_graph = HebbianMemoryGraph(file_path=mem_path)
    temporal_kb = TemporalKnowledgeMemory(file_path=kb_path)
    retriever = ValidityAwareRetriever(memory_graph=memory_graph, temporal_knowledge=temporal_kb)

    try:
        gen_ans, ep_ret, sem_ret = retriever.answer_question(
            question=question,
            question_date=question_date,
            top_k=top_k,
            semantic_top_k=semantic_top_k,
            item_id=item_id,
        )
    except Exception as e:
        print(f"  [{item_id}] Answer generation error: {e}")
        gen_ans = ""
        ep_ret, sem_ret = [], []

    # LLM Judge (LongMemEval rubric)
    try:
        judge_prompt = get_anscheck_prompt(
            question_type, question, str(answer), gen_ans, abstention=is_abstention
        )
        judge_messages = [{"role": "user", "content": judge_prompt}]
        judge_resp = gpt_generate_answer_with_rotation(judge_prompt, judge_messages)
        correct = 1 if parse_judge_response(judge_resp) else 0
    except Exception as e:
        print(f"  [{item_id}] Judge error: {e}")
        correct = 0
        judge_resp = ""

    eval_time = time.time() - t_start
    res = {
        "question_id": item_id,
        "question_type": question_type,
        "question": question,
        "ground_truth": str(answer),
        "generated_answer": gen_ans,
        "correct": correct,
        "is_abstention": is_abstention,
        "judge_response": judge_resp,
        "num_episodic_retrieved": len(ep_ret),
        "num_semantic_retrieved": len(sem_ret),
        "eval_time": eval_time,
    }

    if results_dir:
        res_file = os.path.join(results_dir, f"result_{item_id}.json")
        with open(res_file, "w", encoding="utf-8") as f:
            json.dump(res, f, ensure_ascii=False, indent=2)

    status = "CORRECT" if correct else "WRONG"
    print(f"  [{item_idx}] {item_id} ({question_type}) -> {status} | Ans: '{gen_ans}' vs True: '{answer}' ({eval_time:.1f}s)")
    return res


def run_pipeline(
    stage: str,
    data_path: str,
    output_dir: str,
    reuse_episodic_dir: Optional[str] = None,
    num_items: Optional[int] = None,
    start_item: int = 0,
    target_ids: Optional[List[str]] = None,
    workers: int = 5,
    top_k: int = 15,
    semantic_top_k: int = 5,
) -> None:
    """Orchestrates encoding, evaluation, and comparative report generation."""
    os.makedirs(output_dir, exist_ok=True)
    with open(data_path, "r", encoding="utf-8") as f:
        dataset = json.load(f)

    if target_ids:
        target_set = set(target_ids)
        items = [it for it in dataset if it["question_id"] in target_set]
        print(f"Targeted mode: selected {len(items)} items matching IDs: {target_ids}")
    else:
        items = dataset[start_item:]
        if num_items is not None:
            items = items[:num_items]

    print("=" * 80)
    print(f"TEMPORAL HELA-MEM PIPELINE — Stage: {stage.upper()}")
    print(f"Data: {data_path} ({len(items)} items)")
    print(f"Output: {output_dir}")
    print(f"Reuse Episodic: {reuse_episodic_dir or 'None'}")
    print(f"Workers: {workers} | Top-K: {top_k} | Semantic Top-K: {semantic_top_k}")
    print("=" * 80)

    # Pre-warm embedding model in main thread before spawning workers
    print("[Init] Pre-warming SentenceTransformer embedding model in main thread...")
    _ = get_embedding("warmup")
    print("[Init] Embedding model ready.")

    # 1. ENCODING
    t0_enc = time.time()
    if stage in ("all", "encode"):
        print("\n>>> ETAPA 1: Codificação de Memória Semântica Temporal <<<")
        keys = load_api_keys()
        clients = [OpenAIClient(api_key=k) for k in keys]

        enc_count = 0
        with ThreadPoolExecutor(max_workers=workers) as executor:
            futures = {
                executor.submit(
                    encode_single_temporal_item,
                    item,
                    output_dir,
                    clients[i % len(clients)],
                    reuse_episodic_dir,
                ): item["question_id"]
                for i, item in enumerate(items)
            }
            for fut in as_completed(futures):
                enc_count += 1
                try:
                    fut.result()
                except Exception as e:
                    print(f"  [ERROR] Encoding failed for {futures[fut]}: {e}")

                if enc_count % 10 == 0 or enc_count == len(items):
                    elapsed_enc = time.time() - t0_enc
                    pace_enc = elapsed_enc / enc_count
                    rem_enc = (len(items) - enc_count) * pace_enc
                    print(f"\n  [Progresso Encoding] {enc_count}/{len(items)} itens | Tempo: {elapsed_enc/60:.2f}m | Pace: {pace_enc:.1f}s/item | Restante est.: {rem_enc/60:.2f}m\n")

    t_enc_total = time.time() - t0_enc

    # 2. EVALUATION
    t0_eval = time.time()
    if stage in ("all", "eval"):
        print("\n>>> ETAPA 2: Avaliação Validity-Aware + Juiz LLM <<<")
        results_dir = os.path.join(output_dir, "eval_results")
        os.makedirs(results_dir, exist_ok=True)
        eval_results = []

        eval_count = 0
        with ThreadPoolExecutor(max_workers=workers) as executor:
            futures = {
                executor.submit(
                    evaluate_single_temporal_item,
                    item,
                    start_item + i,
                    output_dir,
                    top_k,
                    semantic_top_k,
                    results_dir,
                ): item["question_id"]
                for i, item in enumerate(items)
            }
            for fut in as_completed(futures):
                eval_count += 1
                try:
                    res = fut.result()
                    eval_results.append(res)
                except Exception as e:
                    print(f"  [ERROR] Eval failed for {futures[fut]}: {e}")

                if eval_count % 10 == 0 or eval_count == len(items):
                    elapsed_eval = time.time() - t0_eval
                    pace_eval = elapsed_eval / eval_count
                    rem_eval = (len(items) - eval_count) * pace_eval
                    print(f"\n  [Progresso Eval] {eval_count}/{len(items)} itens | Tempo: {elapsed_eval/60:.2f}m | Pace: {pace_eval:.1f}s/item | Restante est.: {rem_eval/60:.2f}m\n")

        t_eval_total = time.time() - t0_eval

        # Summary
        total = len(eval_results)
        total_corr = sum(r["correct"] for r in eval_results)
        acc = (total_corr / total * 100) if total > 0 else 0.0

        per_type = {}
        for r in eval_results:
            qt = r["question_type"]
            if qt not in per_type:
                per_type[qt] = {"total": 0, "correct": 0}
            per_type[qt]["total"] += 1
            per_type[qt]["correct"] += r["correct"]

        summary = {
            "timestamp": datetime.now().isoformat(),
            "total_items": total,
            "total_correct": total_corr,
            "overall_accuracy": acc,
            "encoding_time_seconds": t_enc_total,
            "eval_time_seconds": t_eval_total,
            "per_type": per_type,
            "results": eval_results,
        }
        sum_path = os.path.join(results_dir, "eval_summary.json")
        with open(sum_path, "w", encoding="utf-8") as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)

        print("\n" + "=" * 80)
        print(f"RESULTADOS DA PROPOSTA B (Validade Temporal)")
        print(f"Total: {total} | Acertos: {total_corr} | Acurácia: {acc:.2f}%")
        print(f"Tempo Total: Encoding={t_enc_total/60:.2f}min | Eval={t_eval_total/60:.2f}min | Total={(t_enc_total+t_eval_total)/60:.2f}min")
        for qt, stats in sorted(per_type.items()):
            qacc = (stats["correct"] / stats["total"] * 100) if stats["total"] > 0 else 0.0
            print(f"  {qt:30s}: {stats['correct']:3d}/{stats['total']:3d} ({qacc:.2f}%)")
        print("=" * 80)

        # Baseline A Comparison
        baseline_summary_path = ROOT_DIR / "results" / "longmemeval_baseline_full" / "eval_results" / "eval_summary.json"
        improved, regressed, tie_correct, tie_wrong = 0, 0, 0, 0
        if baseline_summary_path.exists():
            with open(baseline_summary_path, "r", encoding="utf-8") as f:
                base_sum = json.load(f)
            base_by_id = {r["question_id"]: r["correct"] for r in base_sum.get("results", [])}

            for r in eval_results:
                qid = r["question_id"]
                if qid in base_by_id:
                    b_corr = base_by_id[qid]
                    p_corr = r["correct"]
                    if b_corr == 0 and p_corr == 1:
                        improved += 1
                    elif b_corr == 1 and p_corr == 0:
                        regressed += 1
                    elif b_corr == 1 and p_corr == 1:
                        tie_correct += 1
                    else:
                        tie_wrong += 1

            print(f"\n[Comparativo A/B com Baseline A Congelada]")
            print(f"  Ganhos (Erro -> Acerto)     : +{improved}")
            print(f"  Regressões (Acerto -> Erro) : -{regressed}")
            print(f"  Saldo Líquido              : {improved - regressed:+d} acertos")
            print(f"  Mantidos Corretos (1 -> 1) : {tie_correct}")
            print(f"  Mantidos Errados (0 -> 0)  : {tie_wrong}")

        # Salvar relatório Markdown em reports/analysis/
        ts_tag = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_md_path = ROOT_DIR / "reports" / "analysis" / f"R04_proposta_temporal_{len(items)}itens_{ts_tag}.md"
        report_lines = [
            f"# Relatório Experimental — Proposta B (Validade Temporal)",
            f"",
            f"**Data da Execução:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"**Amostra:** {len(items)} itens (fatia [{start_item}:{start_item + len(items)}])",
            f"**Diretório:** `{output_dir}`",
            f"**Tempo de Execução:**",
            f"- Encoding: {t_enc_total:.1f}s ({t_enc_total/60:.2f} min)",
            f"- Evaluation: {t_eval_total:.1f}s ({t_eval_total/60:.2f} min)",
            f"- Total: {(t_enc_total+t_eval_total):.1f}s ({(t_enc_total+t_eval_total)/60:.2f} min)",
            f"- Ritmo médio por item: {(t_enc_total+t_eval_total)/len(items):.2f}s/item",
            f"- Projeção para 500 itens: {(t_enc_total+t_eval_total)/len(items) * 500 / 60:.1f} minutos",
            f"",
            f"---",
            f"",
            f"## Resultados Consolidados da Proposta B",
            f"",
            f"**Acurácia Geral:** **{acc:.2f}%** ({total_corr}/{total})",
            f"",
            f"| Categoria / Question Type | Total | Acertos | ACC (%) |",
            f"| :--- | :---: | :---: | :---: |",
        ]
        for qt, stats in sorted(per_type.items()):
            qacc = (stats["correct"] / stats["total"] * 100) if stats["total"] > 0 else 0.0
            report_lines.append(f"| `{qt}` | {stats['total']} | {stats['correct']} | **{qacc:.2f}%** |")

        report_lines.extend([
            f"",
            f"---",
            f"",
            f"## Comparação A/B Pareada com Baseline A",
            f"",
            f"- **Ganhos (Erro -> Acerto):** +{improved}",
            f"- **Regressões (Acerto -> Erro):** -{regressed}",
            f"- **Saldo Líquido:** {improved - regressed:+d} acertos",
            f"- **Mantidos Corretos:** {tie_correct}",
            f"- **Mantidos Errados:** {tie_wrong}",
        ])
        with open(report_md_path, "w", encoding="utf-8") as f:
            f.write("\n".join(report_lines))
        print(f"\n[Relatório] Salvo em: {report_md_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Temporal HeLa-Mem Pipeline")
    parser.add_argument("--stage", choices=["all", "encode", "eval"], default="all")
    parser.add_argument("--data_path", type=str, default=str(HELA_DIR / "data" / "longmemeval_s.json"))
    parser.add_argument("--output_dir", type=str, default=str(ROOT_DIR / "results" / "longmemeval_temporal_full"))
    parser.add_argument(
        "--reuse_episodic_dir",
        type=str,
        default=str(ROOT_DIR / "results" / "longmemeval_baseline_full"),
        help="Path to baseline episodic memories to reuse",
    )
    parser.add_argument("--num_items", type=int, default=10)
    parser.add_argument("--start_item", type=int, default=0)
    parser.add_argument("--target_ids", type=str, default=None, help="Comma-separated IDs (e.g. 07741c44,07741c45)")
    parser.add_argument("--workers", type=int, default=5)
    parser.add_argument("--top_k", type=int, default=15)
    parser.add_argument("--semantic_top_k", type=int, default=5)

    args = parser.parse_args()
    target_ids = [s.strip() for s in args.target_ids.split(",")] if args.target_ids else None

    run_pipeline(
        stage=args.stage,
        data_path=args.data_path,
        output_dir=args.output_dir,
        reuse_episodic_dir=args.reuse_episodic_dir,
        num_items=args.num_items,
        start_item=args.start_item,
        target_ids=target_ids,
        workers=args.workers,
        top_k=args.top_k,
        semantic_top_k=args.semantic_top_k,
    )


if __name__ == "__main__":
    main()
