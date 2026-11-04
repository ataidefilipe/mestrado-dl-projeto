"""
Módulo para visualização e exploração do dataset LongMemEval-S e seus grafos de memória.
Interface autossuficiente em HTML (Dark Mode Limpo e Focado).
Design despoluído: sem badges desnecessárias, com comparação direta lado a lado
entre a Pergunta do Teste, o Gabarito (Ground Truth) e a Resposta Gerada pelo Modelo.
"""

from __future__ import annotations

import argparse
import html
import json
from pathlib import Path
from typing import Any, Dict, List, Optional


def load_dataset(dataset_path: Path) -> List[Dict[str, Any]]:
    with open(dataset_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError(f"Formato inesperado de dataset em {dataset_path}. Esperava lista.")
    return data


def scan_pilot_and_results(results_dir: Optional[Path]) -> Dict[str, Dict[str, Any]]:
    """
    Mapeia os resultados de avaliação oficiais e arquivos de grafos gerados.
    Prioriza `longmemeval_baseline_full/eval_results` (que contém o run completo com 495 itens avaliados).
    """
    info_map: Dict[str, Dict[str, Any]] = {}
    if not results_dir or not results_dir.exists():
        return info_map

    # 1. Carregar primeiro os resultados de avaliação válidos (priorizando a pasta oficial final)
    # Ordem: pilot -> interrupted -> baseline_full
    eval_dirs = [
        results_dir / "longmemeval_baseline_pilot" / "eval_results",
        results_dir / "longmemeval_baseline_full" / "eval_results",
    ]

    for edir in eval_dirs:
        if edir.exists():
            for p in edir.glob("result_*.json"):
                qid = p.stem.replace("result_", "")
                try:
                    with open(p, "r", encoding="utf-8") as rf:
                        res_data = json.load(rf)
                    info_map.setdefault(qid, {})["eval"] = {
                        "correct": res_data.get("correct"),
                        "generated_answer": res_data.get("generated_answer"),
                        "ground_truth": res_data.get("ground_truth"),
                        "eval_time": res_data.get("eval_time"),
                        "num_retrieved": res_data.get("num_retrieved"),
                        "num_nodes": res_data.get("num_nodes"),
                    }
                except Exception:
                    pass

    # 2. Mapear grafos Hebbianos e HTMLs gerados
    for p in results_dir.rglob("*.json"):
        fname = p.name
        if fname.endswith("_hebbian.json"):
            qid = fname[:-len("_hebbian.json")]
            info_map.setdefault(qid, {})["has_hebbian"] = True
            info_map[qid]["hebbian_path"] = str(p.resolve())
            vis_html = p.parent / "visualizations" / f"{qid}_hebbian.html"
            if vis_html.exists():
                info_map[qid]["hebbian_html"] = str(vis_html.resolve())
        elif fname.endswith("_long_term_kb_graph.json"):
            qid = fname[:-len("_long_term_kb_graph.json")]
            info_map.setdefault(qid, {})["has_kb_graph"] = True
            info_map[qid]["kb_graph_path"] = str(p.resolve())
            vis_html = p.parent / "visualizations" / f"{qid}_long_term_kb_graph.html"
            if vis_html.exists():
                info_map[qid]["kb_graph_html"] = str(vis_html.resolve())

    return info_map


def build_clean_explorer_html(
    dataset: List[Dict[str, Any]],
    results_map: Dict[str, Dict[str, Any]],
    title: str = "Explorador da Base de Memória & Conversas",
    dataset_name: str = "longmemeval_s.json",
    limit: Optional[int] = None,
) -> str:
    """Monta o HTML em Dark Mode limpo, sem poluição visual, com teste e resposta destacados."""
    items = dataset[:limit] if limit else dataset

    processed_items = []
    types_count: Dict[str, int] = {}

    type_pt_names = {
        "temporal-reasoning": "Raciocínio Temporal",
        "knowledge-update": "Atualização de Conhecimento",
        "multi-session": "Múltiplas Sessões",
        "single-session-preference": "Preferência (Sessão Única)",
        "single-session-assistant": "Assistente (Sessão Única)",
        "single-session-user": "Usuário (Sessão Única)",
    }

    for idx, d in enumerate(items):
        qid = d.get("question_id", f"item_{idx}")
        qtype = d.get("question_type", "unknown")
        types_count[qtype] = types_count.get(qtype, 0) + 1

        haystack_sessions = d.get("haystack_sessions", [])
        haystack_dates = d.get("haystack_dates", [])
        haystack_session_ids = d.get("haystack_session_ids", [])
        answer_session_ids = set(d.get("answer_session_ids", []))

        total_messages = 0
        evidence_sessions_count = 0

        for s_idx, s in enumerate(haystack_sessions):
            if isinstance(s, list):
                total_messages += len(s)
                has_ans = any(msg.get("has_answer") for msg in s)
                if has_ans or (s_idx < len(haystack_session_ids) and haystack_session_ids[s_idx] in answer_session_ids):
                    evidence_sessions_count += 1

        res_info = results_map.get(qid, {})

        processed_items.append({
            "idx": idx,
            "question_id": qid,
            "question_type": qtype,
            "type_label": type_pt_names.get(qtype, qtype),
            "question": d.get("question", ""),
            "answer": d.get("answer", ""),
            "question_date": d.get("question_date", ""),
            "total_sessions": len(haystack_sessions),
            "evidence_sessions": evidence_sessions_count,
            "total_messages": total_messages,
            "haystack_dates": haystack_dates,
            "haystack_session_ids": haystack_session_ids,
            "answer_session_ids": list(answer_session_ids),
            "sessions": haystack_sessions,
            "has_hebbian": res_info.get("has_hebbian", False),
            "has_kb_graph": res_info.get("has_kb_graph", False),
            "hebbian_html": res_info.get("hebbian_html"),
            "kb_graph_html": res_info.get("kb_graph_html"),
            "eval": res_info.get("eval"),
        })

    items_json = json.dumps(processed_items, ensure_ascii=False)
    types_json = json.dumps(types_count, ensure_ascii=False)
    type_pt_json = json.dumps(type_pt_names, ensure_ascii=False)

    html_code = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html.escape(title)}</title>
  <style>
    :root {{
      --bg: #090d16;
      --surface: #111827;
      --surface-subtle: #162032;
      --border: #1e293b;
      --border-focus: #38bdf8;
      
      --text: #f1f5f9;
      --text-muted: #94a3b8;
      --text-soft: #64748b;
      
      --cyan: #38bdf8;
      --green: #10b981;
      --green-bg: rgba(16, 185, 129, 0.1);
      --red: #ef4444;
      --red-bg: rgba(239, 68, 68, 0.1);
      --gold: #f59e0b;
      --gold-bg: rgba(245, 158, 11, 0.08);

      --user-bg: #1e293b;
      --ai-bg: #0f172a;
    }}

    * {{ box-sizing: border-box; margin: 0; padding: 0; }}

    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
      background-color: var(--bg);
      color: var(--text);
      height: 100vh;
      display: flex;
      flex-direction: column;
      overflow: hidden;
    }}

    /* Topbar limpa */
    header {{
      background: var(--surface);
      border-bottom: 1px solid var(--border);
      padding: 12px 24px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-shrink: 0;
    }}
    .header-title {{
      font-size: 1.1rem;
      font-weight: 700;
      color: var(--text);
      display: flex;
      align-items: center;
      gap: 10px;
    }}
    .header-sub {{
      font-size: 0.8rem;
      color: var(--text-muted);
    }}

    /* Estrutura principal */
    #layout {{
      display: flex;
      flex: 1;
      height: calc(100vh - 53px);
      overflow: hidden;
    }}

    /* Sidebar limpa */
    #sidebar {{
      width: 400px;
      background: var(--surface);
      border-right: 1px solid var(--border);
      display: flex;
      flex-direction: column;
      flex-shrink: 0;
    }}
    .sidebar-controls {{
      padding: 14px;
      border-bottom: 1px solid var(--border);
      display: flex;
      flex-direction: column;
      gap: 8px;
    }}
    .search-input {{
      width: 100%;
      padding: 8px 12px;
      font-size: 0.85rem;
      border: 1px solid var(--border);
      border-radius: 6px;
      background: var(--bg);
      color: var(--text);
      outline: none;
    }}
    .search-input:focus {{
      border-color: var(--cyan);
    }}
    .filters-row {{
      display: flex;
      gap: 8px;
    }}
    select.filter-select {{
      flex: 1;
      padding: 6px 10px;
      font-size: 0.78rem;
      border: 1px solid var(--border);
      border-radius: 6px;
      background: var(--bg);
      color: var(--text);
      outline: none;
      cursor: pointer;
    }}

    /* Lista lateral despoluída */
    #items-list {{
      flex: 1;
      overflow-y: auto;
      list-style: none;
    }}
    .list-item {{
      padding: 12px 16px;
      border-bottom: 1px solid var(--border);
      cursor: pointer;
      display: flex;
      flex-direction: column;
      gap: 5px;
      transition: background 0.1s;
    }}
    .list-item:hover {{
      background: rgba(255, 255, 255, 0.03);
    }}
    .list-item.selected {{
      background: rgba(56, 189, 248, 0.08);
      border-left: 3px solid var(--cyan);
    }}
    .item-top {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      font-size: 0.75rem;
      color: var(--text-soft);
    }}
    .item-question {{
      font-size: 0.86rem;
      font-weight: 500;
      line-height: 1.35;
      color: var(--text);
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }}
    .item-meta {{
      font-size: 0.72rem;
      color: var(--text-muted);
    }}

    /* Indicador discreto de acerto/erro */
    .indicator-dot {{
      display: inline-block;
      width: 8px;
      height: 8px;
      border-radius: 50%;
      margin-left: 6px;
    }}
    .dot-pass {{ background-color: var(--green); }}
    .dot-fail {{ background-color: var(--red); }}

    /* Painel Central */
    #content-pane {{
      flex: 1;
      overflow-y: auto;
      background: var(--bg);
      padding: 24px 32px;
      display: flex;
      flex-direction: column;
      gap: 16px;
    }}

    /* Cartão Principal */
    .card {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 18px 22px;
      display: flex;
      flex-direction: column;
      gap: 12px;
    }}
    .card-title {{
      font-size: 0.72rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--text-muted);
    }}
    .question-text {{
      font-size: 1.25rem;
      font-weight: 600;
      line-height: 1.4;
      color: #ffffff;
    }}
    .meta-line {{
      display: flex;
      gap: 20px;
      font-size: 0.8rem;
      color: var(--text-muted);
    }}

    /* Comparação Lado a Lado: Gabarito vs Resposta do Modelo */
    .eval-comparison {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 14px;
    }}
    .eval-box {{
      padding: 14px 16px;
      border-radius: 8px;
      display: flex;
      flex-direction: column;
      gap: 6px;
    }}
    .box-truth {{
      background: var(--gold-bg);
      border: 1px solid rgba(245, 158, 11, 0.3);
    }}
    .box-truth-label {{
      font-size: 0.72rem;
      font-weight: 700;
      color: var(--gold);
      text-transform: uppercase;
    }}
    .box-truth-value {{
      font-size: 1.05rem;
      font-weight: 600;
      color: #fef08a;
    }}

    .box-model-pass {{
      background: var(--green-bg);
      border: 1px solid rgba(16, 185, 129, 0.35);
    }}
    .box-model-fail {{
      background: var(--red-bg);
      border: 1px solid rgba(239, 68, 68, 0.35);
    }}
    .box-model-label {{
      font-size: 0.72rem;
      font-weight: 700;
      text-transform: uppercase;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }}
    .box-model-value {{
      font-size: 1.05rem;
      font-weight: 600;
      color: #ffffff;
    }}

    /* Seletor de Visão do Histórico */
    .history-header {{
      display: flex;
      align-items: center;
      justify-content: space-between;
    }}
    .toggle-buttons {{
      display: flex;
      gap: 6px;
    }}
    .btn-toggle {{
      padding: 5px 12px;
      font-size: 0.76rem;
      font-weight: 600;
      border-radius: 6px;
      border: 1px solid var(--border);
      background: var(--surface-subtle);
      color: var(--text-muted);
      cursor: pointer;
    }}
    .btn-toggle.active {{
      background: var(--cyan);
      color: #090d16;
      border-color: var(--cyan);
    }}

    /* Sessões de Diálogo */
    .sessions-list {{
      display: flex;
      flex-direction: column;
      gap: 12px;
    }}
    .session-card {{
      border: 1px solid var(--border);
      border-radius: 6px;
      background: var(--surface);
      overflow: hidden;
    }}
    .session-card.evidence {{
      border-color: rgba(245, 158, 11, 0.4);
    }}
    .session-bar {{
      padding: 9px 14px;
      background: var(--surface-subtle);
      display: flex;
      align-items: center;
      justify-content: space-between;
      cursor: pointer;
      font-size: 0.8rem;
    }}
    .session-card.evidence .session-bar {{
      background: rgba(245, 158, 11, 0.08);
    }}
    .session-messages {{
      padding: 12px 16px;
      display: flex;
      flex-direction: column;
      gap: 10px;
      background: #0b101b;
    }}
    .chat-bubble {{
      padding: 10px 14px;
      border-radius: 6px;
      font-size: 0.88rem;
      line-height: 1.45;
      max-width: 92%;
      white-space: pre-wrap;
      word-break: break-word;
    }}
    .bubble-user {{
      align-self: flex-start;
      background: var(--user-bg);
      border: 1px solid #334155;
      color: #e2e8f0;
    }}
    .bubble-ai {{
      align-self: flex-start;
      background: var(--ai-bg);
      border: 1px solid var(--border);
      color: #cbd5e1;
    }}
    .bubble-evidence {{
      border: 1px solid var(--gold) !important;
      background: #252013 !important;
    }}
    .bubble-role {{
      font-size: 0.68rem;
      font-weight: 700;
      text-transform: uppercase;
      margin-bottom: 4px;
      color: var(--text-soft);
    }}

    /* Botão de Grafo */
    .btn-graph {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 7px 14px;
      border-radius: 6px;
      font-size: 0.8rem;
      font-weight: 600;
      text-decoration: none;
      background: #0284c7;
      color: #ffffff;
      border: 1px solid #38bdf8;
      cursor: pointer;
    }}
    .btn-graph:hover {{
      background: #0369a1;
    }}
  </style>
</head>
<body>
  <header>
    <div class="header-title">
      <span>{html.escape(title)}</span>
      <span style="font-size: 0.75rem; color: var(--text-muted); font-weight: normal;">• {len(items)} casos</span>
    </div>
    <div class="header-sub">
      LongMemEval-S: Pergunta de Teste, Gabarito e Resposta do Modelo
    </div>
  </header>

  <div id="layout">
    <!-- Barra Lateral -->
    <div id="sidebar">
      <div class="sidebar-controls">
        <input type="text" id="search-input" class="search-input" placeholder="Buscar pergunta, ID ou termo...">
        <div class="filters-row">
          <select id="type-filter" class="filter-select">
            <option value="">Todas as categorias ({len(items)})</option>
          </select>
          <select id="status-filter" class="filter-select">
            <option value="">Todos os resultados</option>
            <option value="correct">Acertou (Correto)</option>
            <option value="incorrect">Errou (Incorreto)</option>
            <option value="with_graph">Com Grafo</option>
          </select>
        </div>
      </div>
      <ul id="items-list"></ul>
    </div>

    <!-- Conteúdo Principal -->
    <div id="content-pane">
      <div id="empty-state" style="margin: 120px auto; text-align: center; color: var(--text-muted);">
        <p>Selecione um caso de teste na lista lateral para visualizar.</p>
      </div>

      <div id="main-detail" style="display: none; display: flex; flex-direction: column; gap: 16px;">
        <!-- Card 1: Pergunta de Teste -->
        <div class="card">
          <div class="card-title">Pergunta Final do Teste</div>
          <div class="question-text" id="detail-question"></div>
          
          <div class="meta-line">
            <span>Categoria: <b id="detail-qtype" style="color: var(--text);"></b></span>
            <span>Data: <b id="detail-qdate" style="color: var(--text);"></b></span>
            <span>ID: <code id="detail-qid" style="color: var(--cyan);"></code></span>
          </div>

          <div id="graph-button-area" style="margin-top: 4px;"></div>
        </div>

        <!-- Card 2: Gabarito e Resposta do Modelo (Lado a Lado) -->
        <div class="card">
          <div class="card-title">Avaliação do Teste (Gabarito vs Modelo)</div>
          <div class="eval-comparison">
            <!-- Coluna 1: Gabarito -->
            <div class="eval-box box-truth">
              <div class="box-truth-label">Gabarito Oficial (Ground Truth)</div>
              <div class="box-truth-value" id="detail-answer"></div>
            </div>

            <!-- Coluna 2: Resposta do Modelo -->
            <div class="eval-box" id="detail-model-box">
              <div class="box-model-label" id="detail-model-header">
                <span>Resposta Dada pelo Modelo</span>
                <span id="detail-model-status"></span>
              </div>
              <div class="box-model-value" id="detail-model-answer"></div>
            </div>
          </div>
        </div>

        <!-- Card 3: Histórico de Diálogos Passados -->
        <div class="card">
          <div class="history-header">
            <div class="card-title">Conversas Anteriores da IA (<span id="detail-sessions-stat"></span>)</div>
            <div class="toggle-buttons">
              <button class="btn-toggle active" id="btn-evidence" onclick="setViewMode('evidence')">Apenas Sessão com Fatos</button>
              <button class="btn-toggle" id="btn-all" onclick="setViewMode('all')">Todas as Mensagens</button>
            </div>
          </div>
          <div class="sessions-list" id="detail-sessions"></div>
        </div>
      </div>
    </div>
  </div>

  <script>
    const dataItems = {items_json};
    const typesCount = {types_json};
    const typePtNames = {type_pt_json};

    let filteredItems = [...dataItems];
    let selectedIdx = -1;
    let currentViewMode = 'evidence';

    const typeSelect = document.getElementById('type-filter');
    Object.keys(typesCount).sort().forEach(t => {{
      const opt = document.createElement('option');
      opt.value = t;
      const label = typePtNames[t] || t;
      opt.innerText = `${{label}} (${{typesCount[t]}})`;
      typeSelect.appendChild(opt);
    }});

    const listEl = document.getElementById('items-list');
    const searchInput = document.getElementById('search-input');
    const statusSelect = document.getElementById('status-filter');

    function renderList() {{
      listEl.innerHTML = '';
      filteredItems.forEach((item) => {{
        const li = document.createElement('li');
        li.className = `list-item ${{item.idx === selectedIdx ? 'selected' : ''}}`;
        li.onclick = () => selectItem(item.idx);

        let dotHtml = '';
        if (item.eval) {{
          const isCorrect = item.eval.correct === 1 || item.eval.correct === true;
          dotHtml = `<span class="indicator-dot ${{isCorrect ? 'dot-pass' : 'dot-fail'}}" title="${{isCorrect ? 'Acertou' : 'Errou'}}"></span>`;
        }}

        li.innerHTML = `
          <div class="item-top">
            <span>#${{item.idx + 1}} • ${{item.question_id}}</span>
            <div>${{dotHtml}}</div>
          </div>
          <div class="item-question">${{escapeHtml(item.question)}}</div>
          <div class="item-meta">${{item.type_label}}</div>
        `;
        listEl.appendChild(li);
      }});
    }}

    function filterData() {{
      const q = searchInput.value.toLowerCase().trim();
      const t = typeSelect.value;
      const st = statusSelect.value;

      filteredItems = dataItems.filter(item => {{
        if (t && item.question_type !== t) return false;
        
        if (st === 'correct') {{
          if (!item.eval || !(item.eval.correct === 1 || item.eval.correct === true)) return false;
        }} else if (st === 'incorrect') {{
          if (!item.eval || item.eval.correct === 1 || item.eval.correct === true) return false;
        }} else if (st === 'with_graph') {{
          if (!item.has_hebbian) return false;
        }}

        if (q) {{
          const inQ = item.question.toLowerCase().includes(q);
          const inA = item.answer.toLowerCase().includes(q);
          const inId = item.question_id.toLowerCase().includes(q);
          if (!inQ && !inA && !inId) return false;
        }}
        return true;
      }});

      renderList();
    }}

    searchInput.addEventListener('input', filterData);
    typeSelect.addEventListener('change', filterData);
    statusSelect.addEventListener('change', filterData);

    function selectItem(idx) {{
      selectedIdx = idx;
      const item = dataItems.find(d => d.idx === idx);
      if (!item) return;

      document.getElementById('empty-state').style.display = 'none';
      document.getElementById('main-detail').style.display = 'flex';

      renderList();

      document.getElementById('detail-question').innerText = item.question;
      document.getElementById('detail-qdate').innerText = item.question_date || 'N/A';
      document.getElementById('detail-qid').innerText = item.question_id;
      document.getElementById('detail-qtype').innerText = item.type_label;
      document.getElementById('detail-answer').innerText = item.answer;

      // Resposta do modelo
      const modelBox = document.getElementById('detail-model-box');
      const modelAns = document.getElementById('detail-model-answer');
      const modelStatus = document.getElementById('detail-model-status');

      if (item.eval) {{
        const isOk = item.eval.correct === 1 || item.eval.correct === true;
        modelBox.className = `eval-box ${{isOk ? 'box-model-pass' : 'box-model-fail'}}`;
        modelAns.innerText = item.eval.generated_answer || '(Resposta vazia)';
        modelStatus.innerHTML = isOk 
          ? '<span style="color:var(--green); font-weight:700;">✔ ACERTOU</span>' 
          : '<span style="color:var(--red); font-weight:700;">✖ ERROU</span>';
      }} else {{
        modelBox.className = 'eval-box';
        modelBox.style.background = 'var(--surface-subtle)';
        modelBox.style.border = '1px solid var(--border)';
        modelAns.innerText = 'Não executado ou resultado indisponível';
        modelStatus.innerText = '';
      }}

      // Botão de Grafo
      const graphArea = document.getElementById('graph-button-area');
      graphArea.innerHTML = '';
      if (item.hebbian_html) {{
        graphArea.innerHTML = `<a href="${{encodeURI(item.hebbian_html)}}" target="_blank" class="btn-graph">🕸️ Abrir Grafo Hebbiano Deste Exemplo</a>`;
      }}

      document.getElementById('detail-sessions-stat').innerText = 
        `${{item.total_sessions}} sessões (${{item.evidence_sessions}} com fatos)`;

      renderSessions(item);
    }}

    function setViewMode(mode) {{
      currentViewMode = mode;
      document.getElementById('btn-evidence').classList.toggle('active', mode === 'evidence');
      document.getElementById('btn-all').classList.toggle('active', mode === 'all');
      
      const item = dataItems.find(d => d.idx === selectedIdx);
      if (item) {{
        renderSessions(item);
      }}
    }}

    function renderSessions(item) {{
      const sessionsContainer = document.getElementById('detail-sessions');
      sessionsContainer.innerHTML = '';

      item.sessions.forEach((sess, sIdx) => {{
        const sessDate = item.haystack_dates[sIdx] || 'Sem data';
        const sessId = item.haystack_session_ids[sIdx] || `sessao_${{sIdx}}`;
        const isAnswerSess = item.answer_session_ids.includes(sessId);

        if (currentViewMode === 'evidence' && !isAnswerSess) {{
          return;
        }}

        const sessDiv = document.createElement('div');
        sessDiv.className = `session-card ${{isAnswerSess ? 'evidence' : ''}}`;

        let msgsHtml = '';
        if (Array.isArray(sess)) {{
          sess.forEach(msg => {{
            const isUser = msg.role === 'user';
            const roleClass = isUser ? 'bubble-user' : 'bubble-ai';
            const roleName = isUser ? 'Usuário' : 'Assistente IA';
            const hasAns = msg.has_answer;
            const highlightClass = hasAns ? 'bubble-evidence' : '';

            msgsHtml += `
              <div class="chat-bubble ${{roleClass}} ${{highlightClass}}">
                <div class="bubble-role">${{roleName}}</div>
                ${{escapeHtml(msg.content)}}
              </div>
            `;
          }});
        }}

        sessDiv.innerHTML = `
          <div class="session-bar" onclick="toggleSession(this)">
            <div>
              <b>Sessão #${{sIdx + 1}}</b> • ${{sessDate}}
              ${{isAnswerSess ? '<span style="color:var(--gold); margin-left:8px; font-weight:600;">(Contém a Resposta)</span>' : ''}}
            </div>
            <span style="font-size:0.75rem; color:var(--text-soft);">Recolher/Expandir ▼</span>
          </div>
          <div class="session-messages" style="display: flex;">
            ${{msgsHtml}}
          </div>
        `;
        sessionsContainer.appendChild(sessDiv);
      }});

      if (currentViewMode === 'evidence' && sessionsContainer.children.length === 0) {{
        sessionsContainer.innerHTML = '<div style="color:var(--text-soft); font-size:0.85rem; padding:8px;">Nenhuma sessão marcada como evidência direta. Alterne para "Todas as Mensagens" acima.</div>';
      }}
    }}

    function toggleSession(headerEl) {{
      const body = headerEl.nextElementSibling;
      body.style.display = (body.style.display === 'none') ? 'flex' : 'none';
    }}

    function escapeHtml(str) {{
      if (!str) return '';
      return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
    }}

    renderList();
    if (dataItems.length > 0) {{
      selectItem(0);
    }}
  </script>
</body>
</html>
"""
    return html_code


def generate_conversations_explorer(
    dataset_path: Path,
    results_dir: Optional[Path] = None,
    output_html: Optional[Path] = None,
    limit: Optional[int] = None,
) -> Path:
    if not dataset_path.exists():
        raise FileNotFoundError(f"Dataset não encontrado em: {dataset_path}")

    dataset = load_dataset(dataset_path)
    results_map = scan_pilot_and_results(results_dir)

    if output_html is None:
        out_dir = dataset_path.parent / "visualizations"
        out_dir.mkdir(parents=True, exist_ok=True)
        output_html = out_dir / "explorador_conversas.html"
    else:
        output_html.parent.mkdir(parents=True, exist_ok=True)

    html_content = build_clean_explorer_html(
        dataset=dataset,
        results_map=results_map,
        title="Explorador de Memória & Avaliação",
        dataset_name=dataset_path.name,
        limit=limit,
    )

    with open(output_html, "w", encoding="utf-8") as f:
        f.write(html_content)

    return output_html


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Gera visualizador escuro, limpo e direto para inspecionar testes, respostas e histórico."
    )
    parser.add_argument(
        "--dataset",
        "-d",
        type=str,
        default="external/HeLa-Mem/data/longmemeval_s.json",
        help="Caminho para o JSON do dataset",
    )
    parser.add_argument(
        "--results",
        "-r",
        type=str,
        default="results",
        help="Diretório onde os grafos e resultados de avaliação estão salvos",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        default="reports/visualizations/explorador_conversas.html",
        help="Caminho de saída do HTML",
    )
    parser.add_argument(
        "--limit",
        "-l",
        type=int,
        default=None,
        help="Limite de exemplos a carregar (opcional)",
    )
    args = parser.parse_args()

    dataset_path = Path(args.dataset).resolve()
    results_dir = Path(args.results).resolve() if args.results else None
    output_html = Path(args.output).resolve() if args.output else None

    out_path = generate_conversations_explorer(
        dataset_path=dataset_path,
        results_dir=results_dir,
        output_html=output_html,
        limit=args.limit,
    )
    print(f"\n[Sucesso] Explorador direto e limpo gerado em:\n{out_path}")


if __name__ == "__main__":
    main()
