"""
Módulo de visualização interativa de grafos de memória (HTML autossuficiente).
Renderiza grafos de memória episódica (Hebbian) e semântica (KB Graph) utilizando vis.js.
"""

from __future__ import annotations

import argparse
import html
import json
from pathlib import Path
from typing import Any, Dict, List, Optional


def load_graph_data(json_path: Path) -> Dict[str, Any]:
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_visjs_html(
    graph_data: Dict[str, Any],
    title: str = "Grafo de Memória",
    source_filename: str = "",
) -> str:
    nodes_raw = graph_data.get("nodes", {})
    edges_raw = graph_data.get("edges", {})

    # Preparar nós para o vis.js
    nodes_list: List[Dict[str, Any]] = []
    for nid, node in nodes_raw.items():
        role = node.get("role", "memory")
        timestamp = node.get("timestamp", "N/A")
        keywords = node.get("keywords", [])
        content = node.get("content", "")
        
        # Resumo para o label
        if keywords and isinstance(keywords, list):
            label_text = f"[{nid}] " + ", ".join(keywords[:2])
        else:
            first_line = content.strip().split("\n")[0]
            label_text = f"[{nid}] " + (first_line[:30] + "..." if len(first_line) > 30 else first_line)

        # Paleta de cores por papel/tipo
        if role == "interaction":
            bg_color = "#3b82f6"  # azul
            border_color = "#1d4ed8"
        elif role == "system":
            bg_color = "#10b981"  # verde
            border_color = "#047857"
        elif role == "user":
            bg_color = "#8b5cf6"  # roxo
            border_color = "#6d28d9"
        else:
            bg_color = "#f59e0b"  # amarelo/laranja
            border_color = "#d97706"

        nodes_list.append({
            "id": nid,
            "label": label_text,
            "title": f"Nó {nid} ({role})\nData: {timestamp}\nClique para ver detalhes",
            "content": content,
            "role": role,
            "timestamp": timestamp,
            "keywords": keywords if isinstance(keywords, list) else [],
            "color": {
                "background": bg_color,
                "border": border_color,
                "highlight": {"background": "#ec4899", "border": "#be185d"},
            },
            "shape": "dot",
            "size": 24,
            "font": {"color": "#f8fafc", "size": 13, "face": "system-ui, sans-serif"},
            "borderWidth": 2,
        })

    # Preparar arestas para o vis.js
    edges_list: List[Dict[str, Any]] = []
    weights: List[float] = []
    
    for src_id, target_map in edges_raw.items():
        for tgt_id, weight in target_map.items():
            w = float(weight)
            weights.append(w)
            edges_list.append({
                "from": str(src_id),
                "to": str(tgt_id),
                "weight": round(w, 4),
                "title": f"Peso sináptico: {round(w, 4)}",
            })

    min_w = min(weights) if weights else 0.0
    max_w = max(weights) if weights else 1.0

    html_template = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html.escape(title)}</title>
  <script src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
  <style>
    :root {{
      --bg-main: #0f172a;
      --bg-panel: #1e293b;
      --border-color: #334155;
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
      --accent: #38bdf8;
      --accent-hover: #0ea5e9;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      background-color: var(--bg-main);
      color: var(--text-main);
      display: flex;
      flex-direction: column;
      height: 100vh;
      overflow: hidden;
    }}
    header {{
      background-color: var(--bg-panel);
      padding: 12px 20px;
      border-bottom: 1px solid var(--border-color);
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      z-index: 10;
    }}
    header h1 {{
      font-size: 1.1rem;
      font-weight: 600;
      color: var(--text-main);
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    .badge {{
      background-color: #334155;
      color: var(--accent);
      padding: 3px 8px;
      border-radius: 6px;
      font-size: 0.75rem;
      font-weight: 500;
    }}
    .controls {{
      display: flex;
      align-items: center;
      gap: 16px;
      font-size: 0.85rem;
    }}
    .control-group {{
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    input[type="range"] {{
      accent-color: var(--accent);
      cursor: pointer;
    }}
    button {{
      background-color: #334155;
      color: var(--text-main);
      border: 1px solid var(--border-color);
      padding: 6px 12px;
      border-radius: 6px;
      cursor: pointer;
      font-size: 0.8rem;
      transition: all 0.2s;
    }}
    button:hover {{
      background-color: var(--accent);
      color: #0f172a;
    }}
    #main-container {{
      display: flex;
      flex: 1;
      height: calc(100vh - 60px);
      position: relative;
    }}
    #network-container {{
      flex: 1;
      height: 100%;
      background: radial-gradient(circle at center, #1e293b 0%, #0f172a 100%);
    }}
    #sidebar {{
      width: 400px;
      background-color: var(--bg-panel);
      border-left: 1px solid var(--border-color);
      display: flex;
      flex-direction: column;
      transition: transform 0.3s ease;
      z-index: 5;
    }}
    #sidebar.hidden {{
      transform: translateX(100%);
      position: absolute;
      right: 0;
      top: 0;
      bottom: 0;
    }}
    .sidebar-header {{
      padding: 14px 18px;
      border-bottom: 1px solid var(--border-color);
      display: flex;
      align-items: center;
      justify-content: space-between;
    }}
    .sidebar-header h2 {{
      font-size: 0.95rem;
      font-weight: 600;
      color: var(--text-main);
    }}
    .sidebar-content {{
      padding: 18px;
      overflow-y: auto;
      flex: 1;
      display: flex;
      flex-direction: column;
      gap: 14px;
      font-size: 0.85rem;
      line-height: 1.5;
    }}
    .info-card {{
      background-color: rgba(15, 23, 42, 0.6);
      border: 1px solid var(--border-color);
      border-radius: 8px;
      padding: 12px;
    }}
    .info-card h3 {{
      font-size: 0.75rem;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--text-muted);
      margin-bottom: 6px;
    }}
    .content-box {{
      white-space: pre-wrap;
      word-break: break-word;
      font-family: inherit;
      background-color: #090d16;
      border: 1px solid #1e293b;
      padding: 12px;
      border-radius: 6px;
      max-height: 320px;
      overflow-y: auto;
      color: #e2e8f0;
      font-size: 0.82rem;
    }}
    .tag-container {{
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      margin-top: 4px;
    }}
    .tag {{
      background-color: #1e3a8a;
      color: #93c5fd;
      padding: 3px 8px;
      border-radius: 4px;
      font-size: 0.75rem;
    }}
    .legend {{
      position: absolute;
      bottom: 16px;
      left: 16px;
      background-color: rgba(30, 41, 59, 0.85);
      backdrop-filter: blur(8px);
      border: 1px solid var(--border-color);
      border-radius: 8px;
      padding: 12px 16px;
      font-size: 0.75rem;
      display: flex;
      flex-direction: column;
      gap: 8px;
      z-index: 2;
    }}
    .legend-item {{
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    .legend-color {{
      width: 12px;
      height: 12px;
      border-radius: 50%;
    }}
  </style>
</head>
<body>
  <header>
    <h1>
      <span>🧠 {html.escape(title)}</span>
      <span class="badge">{len(nodes_list)} nós</span>
      <span class="badge" id="visible-edges-count">{len(edges_list)} arestas</span>
      {f'<span class="badge">{html.escape(source_filename)}</span>' if source_filename else ''}
    </h1>
    <div class="controls">
      <div class="control-group">
        <label for="weight-filter">Limiar de Peso Sináptico:</label>
        <input type="range" id="weight-filter" min="{min_w}" max="{max_w}" step="0.01" value="{min_w}">
        <span id="weight-val" style="min-width: 42px; font-weight: 600; color: var(--accent);">{min_w:.2f}</span>
      </div>
      <button onclick="resetCamera()">Centralizar</button>
      <button onclick="toggleSidebar()">Alternar Detalhes</button>
    </div>
  </header>

  <div id="main-container">
    <div id="network-container"></div>

    <div class="legend">
      <div style="font-weight: 600; margin-bottom: 2px; color: var(--text-muted);">Legenda de Nós</div>
      <div class="legend-item"><div class="legend-color" style="background: #3b82f6;"></div><span>Interação (interaction)</span></div>
      <div class="legend-item"><div class="legend-color" style="background: #10b981;"></div><span>Sistema (system)</span></div>
      <div class="legend-item"><div class="legend-color" style="background: #8b5cf6;"></div><span>Usuário (user)</span></div>
      <div class="legend-item"><div class="legend-color" style="background: #f59e0b;"></div><span>Outro</span></div>
    </div>

    <div id="sidebar">
      <div class="sidebar-header">
        <h2>Detalhes do Nó</h2>
        <span id="selected-node-id" class="badge">Nenhum nó selecionado</span>
      </div>
      <div class="sidebar-content" id="sidebar-details">
        <p style="color: var(--text-muted); text-align: center; margin-top: 40px;">
          Clique em qualquer nó no grafo para inspecionar seus atributos, palavras-chave, carimbo temporal e conteúdo textual.
        </p>
      </div>
    </div>
  </div>

  <script>
    const rawNodes = {json.dumps(nodes_list)};
    const rawEdges = {json.dumps(edges_list)};

    let network = null;
    let nodesDataSet = new vis.DataSet(rawNodes);
    let edgesDataSet = new vis.DataSet([]);

    function updateEdges(minWeight) {{
      const filtered = rawEdges
        .filter(e => e.weight >= minWeight)
        .map(e => {{
          // Normaliza largura da aresta proporcional ao peso
          const width = Math.max(1, Math.min(6, e.weight * 5));
          const opacity = Math.max(0.2, Math.min(0.9, e.weight));
          return {{
            ...e,
            width: width,
            color: {{ color: `rgba(56, 189, 248, ${{opacity}})` }},
            arrows: {{ to: {{ enabled: true, scaleFactor: 0.5 }} }},
            smooth: {{ type: 'continuous' }}
          }};
        }});

      edgesDataSet.clear();
      edgesDataSet.add(filtered);
      document.getElementById('visible-edges-count').innerText = `${{filtered.length}} arestas`;
    }}

    function initNetwork() {{
      const container = document.getElementById('network-container');
      const data = {{
        nodes: nodesDataSet,
        edges: edgesDataSet
      }};
      const options = {{
        physics: {{
          solver: 'forceAtlas2Based',
          forceAtlas2Based: {{
            gravitationalConstant: -70,
            centralGravity: 0.015,
            springLength: 120,
            springConstant: 0.08,
            damping: 0.95
          }},
          stabilization: {{ iterations: 200 }}
        }},
        interaction: {{
          hover: true,
          tooltipDelay: 150,
          zoomView: true,
          dragView: true
        }}
      }};

      network = new vis.Network(container, data, options);

      network.on('click', function(params) {{
        if (params.nodes.length > 0) {{
          const nodeId = params.nodes[0];
          showNodeDetails(nodeId);
        }}
      }});
    }}

    function showNodeDetails(nodeId) {{
      const node = rawNodes.find(n => String(n.id) === String(nodeId));
      if (!node) return;

      document.getElementById('selected-node-id').innerText = `ID: ${{node.id}}`;

      const detailsDiv = document.getElementById('sidebar-details');
      let tagsHtml = '';
      if (node.keywords && node.keywords.length > 0) {{
        tagsHtml = '<div class="tag-container">' + 
          node.keywords.map(kw => `<span class="tag">${{kw}}</span>`).join('') + 
          '</div>';
      }} else {{
        tagsHtml = '<span style="color: var(--text-muted); font-size: 0.8rem;">Nenhuma tag extraída</span>';
      }}

      // Conexões incidentes / saídas
      const outgoing = rawEdges.filter(e => String(e.from) === String(node.id));
      const incoming = rawEdges.filter(e => String(e.to) === String(node.id));

      detailsDiv.innerHTML = `
        <div class="info-card">
          <h3>Papel / Tipo</h3>
          <div style="font-weight: 600; color: ${{node.color.background}};">${{node.role.toUpperCase()}}</div>
        </div>

        <div class="info-card">
          <h3>Carimbo Temporal (Timestamp)</h3>
          <div>${{node.timestamp}}</div>
        </div>

        <div class="info-card">
          <h3>Palavras-Chave (Keywords)</h3>
          ${{tagsHtml}}
        </div>

        <div class="info-card">
          <h3>Conexões Sinápticas</h3>
          <div style="display: flex; gap: 16px; margin-top: 4px;">
            <span>Saídas: <b>${{outgoing.length}}</b></span>
            <span>Entradas: <b>${{incoming.length}}</b></span>
          </div>
        </div>

        <div class="info-card">
          <h3>Conteúdo da Memória</h3>
          <div class="content-box">${{escapeHtml(node.content)}}</div>
        </div>
      `;

      // Garante que a barra lateral esteja visível
      document.getElementById('sidebar').classList.remove('hidden');
    }}

    function escapeHtml(str) {{
      return str
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
    }}

    function resetCamera() {{
      if (network) network.fit({{ animation: true }});
    }}

    function toggleSidebar() {{
      document.getElementById('sidebar').classList.toggle('hidden');
    }}

    // Listener para o filtro de peso
    const slider = document.getElementById('weight-filter');
    const weightVal = document.getElementById('weight-val');
    slider.addEventListener('input', (e) => {{
      const val = parseFloat(e.target.value);
      weightVal.innerText = val.toFixed(2);
      updateEdges(val);
    }});

    // Inicialização
    initNetwork();
    updateEdges({min_w});
  </script>
</body>
</html>
"""
    return html_template


def generate_visualization(
    input_json: Path,
    output_html: Optional[Path] = None,
    title: Optional[str] = None,
) -> Path:
    if not input_json.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {input_json}")

    graph_data = load_graph_data(input_json)
    graph_title = title or f"Grafo de Memória: {input_json.stem}"

    if output_html is None:
        output_dir = input_json.parent / "visualizations"
        output_dir.mkdir(parents=True, exist_ok=True)
        output_html = output_dir / f"{input_json.stem}.html"
    else:
        output_html.parent.mkdir(parents=True, exist_ok=True)

    html_content = build_visjs_html(
        graph_data=graph_data,
        title=graph_title,
        source_filename=input_json.name,
    )

    with open(output_html, "w", encoding="utf-8") as f:
        f.write(html_content)

    return output_html


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Gera visualização interativa em HTML autossuficiente a partir de um grafo JSON."
    )
    parser.add_argument(
        "json_path",
        type=str,
        help="Caminho do arquivo JSON do grafo (ex: results/.../08f4fc43_hebbian.json)",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        default=None,
        help="Caminho de saída para o HTML gerado (opcional)",
    )
    parser.add_argument(
        "--title",
        "-t",
        type=str,
        default=None,
        help="Título da página de visualização",
    )
    args = parser.parse_args()

    input_path = Path(args.json_path).resolve()
    out_path = Path(args.output).resolve() if args.output else None

    result_path = generate_visualization(input_path, out_path, args.title)
    print(f"\n[Sucesso] Visualização interativa gerada em:\n{result_path}")


if __name__ == "__main__":
    main()
