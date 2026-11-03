"""
Script para geração de figuras com qualidade de publicação (IEEE style, 300 DPI)
para a Entrega 1 do Projeto de Deep Learning (Mestrado CIn/UFPE).

Gera:
- fig1_arquitetura_proposta.png: Arquitetura comparativa (HeLa-Mem Baseline vs Proposta com Validade Temporal)
- fig2_baseline_vs_paper.png: Gráfico de barras comparando reprodução empírica vs meta do artigo ACL 2026
- fig3_distribuicao_erros_categorias.png: Análise quantitativa de desempenho por categoria e tipologia de falhas
- fig4_estudo_caso_supersessao.png: Diagrama de estudo de caso real (07741c44 vs 07741c45) demonstrando falha da baseline por falta de supersessão
"""

import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import numpy as np

# Configuração de estilo IEEE
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['axes.titlesize'] = 11
plt.rcParams['axes.labelsize'] = 10
plt.rcParams['xtick.labelsize'] = 9
plt.rcParams['ytick.labelsize'] = 9
plt.rcParams['legend.fontsize'] = 9

out_dir = Path("reports/figures")
out_dir.mkdir(parents=True, exist_ok=True)


# -------------------------------------------------------------------------
# FIGURA 1: Arquitetura Comparativa (HeLa-Mem Baseline vs Proposta)
# -------------------------------------------------------------------------
def generate_fig1():
    fig, ax = plt.subplots(figsize=(10.6, 5.5))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    # Título principal
    ax.text(0.5, 0.965,
            'Arquitetura Comparativa: HeLa-Mem Baseline vs. Extensão com Validade Temporal',
            ha='center', va='top', fontsize=12, fontweight='bold', color='#1a1a2e')

    # Painel Esquerdo: HeLa-Mem Baseline (ACL 2026)
    box_left = FancyBboxPatch((0.025, 0.04), 0.45, 0.85,
                              boxstyle="round,pad=0.015,rounding_size=0.025",
                              ec="#2b5c8f", fc="#f4f7fb", lw=1.8)
    ax.add_patch(box_left)
    ax.text(0.25, 0.855, 'Baseline: HeLa-Mem Original (ACL 2026)',
            ha='center', va='center', fontsize=10.5, fontweight='bold', color='#2b5c8f')

    # Blocos da Baseline (fluxo de cima para baixo)
    b1 = FancyBboxPatch((0.05, 0.67), 0.40, 0.12,
                        boxstyle="round,pad=0.01,rounding_size=0.015",
                        ec="#3b5998", fc="#ffffff", lw=1.1)
    ax.add_patch(b1)
    ax.text(0.25, 0.73,
            '1. Memória Episódica (Grafo Hebbiano)\n'
            'Nós: Turnos de diálogo | Arestas: Força Sináptica ($w_{ij}$)\n'
            'Reforço por coativação ($\\Delta w = \\eta$)',
            ha='center', va='center', fontsize=8.2, color='#111')

    b2 = FancyBboxPatch((0.05, 0.47), 0.40, 0.12,
                        boxstyle="round,pad=0.01,rounding_size=0.015",
                        ec="#3b5998", fc="#ffffff", lw=1.1)
    ax.add_patch(b2)
    ax.text(0.25, 0.53,
            '2. Memória Semântica Estática (HebbianKnowledgeMemory)\n'
            'Fato extraído sem data original da sessão (usa relógio runtime)\n'
            'Metadado fixo: {"type": "fact"} (sem janela de validade)',
            ha='center', va='center', fontsize=8.0, color='#111')

    b3 = FancyBboxPatch((0.05, 0.27), 0.40, 0.12,
                        boxstyle="round,pad=0.01,rounding_size=0.015",
                        ec="#b83b3b", fc="#fff5f5", lw=1.3)
    ax.add_patch(b3)
    ax.text(0.25, 0.33,
            '3. Limitação Crítica no Retrieval:\n'
            'Busca vetorial ignora a data da consulta ($t_{query}$).\n'
            'Fatos obsoletos competem igualmente com fatos atuais!',
            ha='center', va='center', fontsize=8.0, fontweight='bold', color='#b83b3b')

    b4 = FancyBboxPatch((0.05, 0.08), 0.40, 0.11,
                        boxstyle="round,pad=0.01,rounding_size=0.015",
                        ec="#495057", fc="#e9ecef", lw=1.1)
    ax.add_patch(b4)
    ax.text(0.25, 0.135,
            '4. Efeito Observado na Replicação (500 itens):\n'
            'Alucinação de estado antigo em Knowledge-Update (ACC: 73,08%)\n'
            'e gargalo em Temporal Reasoning (ACC: 51,88%)',
            ha='center', va='center', fontsize=8.0, fontweight='bold', color='#343a40')

    # Setas da Baseline apontando PARA BAIXO (xy é a ponta inferior, xytext é a base superior)
    arrow_kw_left = dict(arrowstyle="-|>,head_width=0.3,head_length=0.45", color="#2b5c8f", lw=1.6)
    ax.annotate('', xy=(0.25, 0.602), xytext=(0.25, 0.658), arrowprops=arrow_kw_left)
    ax.annotate('', xy=(0.25, 0.402), xytext=(0.25, 0.458), arrowprops=arrow_kw_left)
    ax.annotate('', xy=(0.25, 0.202), xytext=(0.25, 0.258), arrowprops=arrow_kw_left)

    # Painel Direito: Proposta com Validade Temporal & Supersessão
    box_right = FancyBboxPatch((0.525, 0.04), 0.45, 0.85,
                               boxstyle="round,pad=0.015,rounding_size=0.025",
                               ec="#1b8a5a", fc="#f3faf6", lw=1.8)
    ax.add_patch(box_right)
    ax.text(0.75, 0.855, 'Proposta: HeLa-Mem + Validade Temporal',
            ha='center', va='center', fontsize=10.5, fontweight='bold', color='#1b8a5a')

    # Blocos da Proposta (fluxo de cima para baixo)
    p1 = FancyBboxPatch((0.55, 0.67), 0.40, 0.12,
                        boxstyle="round,pad=0.01,rounding_size=0.015",
                        ec="#1b8a5a", fc="#ffffff", lw=1.1)
    ax.add_patch(p1)
    ax.text(0.75, 0.73,
            '1. Memória Episódica + Ancoragem Cronológica\n'
            'Preservação estrita dos timestamps originais (haystack_dates)\n'
            'Manutenção integral da plasticidade sináptica hebbiana',
            ha='center', va='center', fontsize=8.2, color='#111')

    p2 = FancyBboxPatch((0.55, 0.47), 0.40, 0.12,
                        boxstyle="round,pad=0.01,rounding_size=0.015",
                        ec="#1b8a5a", fc="#ffffff", lw=1.2)
    ax.add_patch(p2)
    ax.text(0.75, 0.53,
            '2. Memória Semântica com Janela de Validade:\n'
            'Tupla $f_i = \\langle c_i, \\mathbf{e}_i, [t_{start}, t_{end}], \\mathcal{S}_i, \\mathbf{w}_i \\rangle$\n'
            'Transição: UNRELATED | EXTENDS | SUPERSEDES ($t_{end} \\leftarrow t_{event}$)',
            ha='center', va='center', fontsize=8.0, color='#111')

    p3 = FancyBboxPatch((0.55, 0.27), 0.40, 0.12,
                        boxstyle="round,pad=0.01,rounding_size=0.015",
                        ec="#1b8a5a", fc="#e8f8f0", lw=1.3)
    ax.add_patch(p3)
    ax.text(0.75, 0.33,
            '3. Retrieval Ponderado por Pertinência Temporal:\n'
            'Query $Q(t_{query})$ avalia pertinência $\\mathcal{V}(f_i, t_{query})$.\n'
            'Fatos expirados ($t_{end} < t_{query}$) são atenuados antes do LLM.',
            ha='center', va='center', fontsize=8.0, fontweight='bold', color='#1b8a5a')

    p4 = FancyBboxPatch((0.55, 0.08), 0.40, 0.11,
                        boxstyle="round,pad=0.01,rounding_size=0.015",
                        ec="#0f5132", fc="#d1f2e1", lw=1.1)
    ax.add_patch(p4)
    ax.text(0.75, 0.135,
            '4. Hipótese Experimental Alvo:\n'
            'Mitigação de anacronismos em Knowledge-Update e\n'
            'ganho de consistência em Temporal Reasoning',
            ha='center', va='center', fontsize=7.8, fontweight='bold', color='#0f5132')

    # Setas da Proposta apontando PARA BAIXO
    arrow_kw_right = dict(arrowstyle="-|>,head_width=0.3,head_length=0.45", color="#1b8a5a", lw=1.6)
    ax.annotate('', xy=(0.75, 0.602), xytext=(0.75, 0.658), arrowprops=arrow_kw_right)
    ax.annotate('', xy=(0.75, 0.402), xytext=(0.75, 0.458), arrowprops=arrow_kw_right)
    ax.annotate('', xy=(0.75, 0.202), xytext=(0.75, 0.258), arrowprops=arrow_kw_right)

    plt.tight_layout()
    fig.savefig(out_dir / "fig1_arquitetura_proposta.png", dpi=300, bbox_inches='tight')
    fig.savefig(out_dir / "fig1_arquitetura_proposta.pdf", bbox_inches='tight')
    plt.close()
    print("Figura 1 gerada com sucesso.")


# -------------------------------------------------------------------------
# FIGURA 2: Baseline Replication vs Paper Target (ACL 2026) — Formato Coluna Única (Horizontal)
# -------------------------------------------------------------------------
def generate_fig2():
    categories = [
        "Single-Sess. User",
        "Knowledge Update",
        "Temporal Reasoning",
        "Multi-Sess. Reasoning",
        "Overall (Global)"
    ]
    paper_scores = [78.85, 78.21, 50.38, 57.14, 65.40]
    reproduced_scores = [87.14, 73.08, 51.88, 46.62, 61.20]

    y = np.arange(len(categories))
    height = 0.36

    fig, ax = plt.subplots(figsize=(3.8, 3.1))

    color_paper = "#2b5c8f"      # Azul sóbrio
    color_reprod = "#e07a5f"     # Coral

    rects1 = ax.barh(y + height/2, paper_scores, height,
                     label='Paper (ACL 2026)',
                     color=color_paper, edgecolor='black', linewidth=0.6, alpha=0.92)
    rects2 = ax.barh(y - height/2, reproduced_scores, height,
                     label='Ours (Baseline)',
                     color=color_reprod, edgecolor='black', linewidth=0.6, alpha=0.92)

    # Rótulos de porcentagem na ponta ou dentro das barras
    for rect in rects1:
        w = rect.get_width()
        ax.annotate(f'{w:.1f}%',
                    xy=(w - 2.0, rect.get_y() + rect.get_height() / 2),
                    ha='right', va='center', fontsize=6.5, fontweight='bold', color='white')

    for rect in rects2:
        w = rect.get_width()
        ax.annotate(f'{w:.1f}%',
                    xy=(w - 2.0, rect.get_y() + rect.get_height() / 2),
                    ha='right', va='center', fontsize=6.5, fontweight='bold', color='white')

    # Badges de delta na margem direita
    for i, (p, r) in enumerate(zip(paper_scores, reproduced_scores)):
        diff = r - p
        sign = "+" if diff > 0 else ""
        color_diff = "#1b8a5a" if diff >= 0 else "#b83b3b"
        ax.text(102, y[i], f"{sign}{diff:.1f} pp", ha='left', va='center',
                fontsize=6.5, fontweight='bold', color=color_diff,
                bbox=dict(boxstyle="round,pad=0.15", fc="white", ec=color_diff, lw=0.7, alpha=0.95))

    ax.set_xlabel('Acurácia (%)', fontsize=8.0, fontweight='bold')
    ax.set_title('Acurácia LongMemEval-S: Paper vs. Baseline',
                 fontsize=8.5, fontweight='bold', pad=18)
    ax.set_yticks(y)
    ax.set_yticklabels(categories, fontsize=7.0, fontweight='bold')
    ax.set_xlim(0, 126)
    ax.set_xticks([0, 25, 50, 75, 100])
    ax.grid(axis='x', linestyle='--', alpha=0.35)
    
    # Legenda limpa no topo central logo abaixo do título
    ax.legend(frameon=True, facecolor='white', edgecolor='#cccccc',
              loc='upper center', bbox_to_anchor=(0.5, 1.12), ncol=2,
              fontsize=6.8, borderpad=0.2)

    plt.tight_layout()
    fig.savefig(out_dir / "fig2_baseline_vs_paper.png", dpi=300, bbox_inches='tight')
    fig.savefig(out_dir / "fig2_baseline_vs_paper.pdf", bbox_inches='tight')
    plt.close()
    print("Figura 2 (horizontal limpa com legenda no topo) gerada com sucesso.")


# -------------------------------------------------------------------------
# FIGURA 3: Distribuição e Tipologia de Erros — Formato Coluna Única (Empilhada)
# -------------------------------------------------------------------------
def generate_fig3():
    with open("results/longmemeval_baseline_full/eval_results/eval_summary.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    types_order = [
        ("single-session-assistant", "S. Asst"),
        ("single-session-user", "S. User"),
        ("knowledge-update", "Knowl.\nUpdate"),
        ("temporal-reasoning", "Temporal\nReas."),
        ("multi-session", "Multi-\nSess."),
        ("single-session-preference", "S. Pref")
    ]

    names = [t[1] for t in types_order]
    corrects = [data["per_type"][t[0]]["correct"] for t in types_order]
    totals = [data["per_type"][t[0]]["total"] for t in types_order]
    errors = [tot - corr for corr, tot in zip(corrects, totals)]
    accs = [data["per_type"][t[0]]["accuracy"] for t in types_order]

    x = np.arange(len(names))
    width = 0.58

    # Proporção vertical para 1 coluna IEEE (3.8 x 5.6 polegadas) com subplots empilhados
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(3.8, 5.8), gridspec_kw={'height_ratios': [1.1, 1.0]})

    # Subplot 1: Barras empilhadas de Acertos vs Erros
    ax1.bar(x, corrects, width, label='Acertos (306)', color='#38b000',
            edgecolor='black', linewidth=0.6, alpha=0.88)
    ax1.bar(x, errors, width, bottom=corrects, label='Erros (194)', color='#d90429',
            edgecolor='black', linewidth=0.6, alpha=0.88)

    for i in range(len(names)):
        tot = totals[i]
        acc = accs[i]
        ax1.text(x[i], tot + 3.0, f"{acc:.0f}%\n({tot})",
                 ha='center', va='bottom', fontsize=6.5, fontweight='bold')

    ax1.set_ylabel('Total de Questões', fontsize=8.0, fontweight='bold')
    ax1.set_title('(A) Acertos e Falhas por Categoria',
                  fontsize=8.5, fontweight='bold', pad=6)
    ax1.set_xticks(x)
    ax1.set_xticklabels(names, fontsize=6.8)
    ax1.set_ylim(0, 165)
    ax1.grid(axis='y', linestyle='--', alpha=0.35)
    ax1.legend(loc='upper left', frameon=True, facecolor='white', edgecolor='#cccccc', fontsize=7.0, borderpad=0.25)

    # Subplot 2: Donut da Composição dos 194 Erros Totais
    err_ku = errors[2]
    err_tr = errors[3]
    err_ms = errors[4]
    err_pref = errors[5]
    err_other = errors[0] + errors[1]

    error_labels = [
        f'Temporal (64 | 33,0%)',
        f'Multi-Sess (71 | 36,6%)',
        f'Update (21 | 10,8%)',
        f'Pref (22 | 11,3%)',
        f'Single (16 | 8,2%)'
    ]
    error_values = [err_tr, err_ms, err_ku, err_pref, err_other]
    colors_pie = ['#e63946', '#f4a261', '#e76f51', '#2a9d8f', '#457b9d']
    explode = (0.04, 0.0, 0.04, 0.0, 0.0)

    wedges, texts = ax2.pie(
        error_values,
        labels=error_labels,
        explode=explode,
        startangle=135,
        colors=colors_pie,
        wedgeprops=dict(width=0.48, edgecolor='black', linewidth=0.6),
        textprops=dict(fontsize=6.8, fontweight='normal')
    )
    # Texto central no Donut
    ax2.text(0, 0, "194 Erros\n43,8% em\nTempo/Update",
             ha='center', va='center', fontsize=7.2, fontweight='bold', color='#1a1a2e')

    ax2.set_title('(B) Decomposição dos 194 Erros (Baseline)',
                  fontsize=8.5, fontweight='bold', pad=6)

    plt.tight_layout()
    fig.savefig(out_dir / "fig3_distribuicao_erros_categorias.png", dpi=300, bbox_inches='tight')
    fig.savefig(out_dir / "fig3_distribuicao_erros_categorias.pdf", bbox_inches='tight')
    plt.close()
    print("Figura 3 (otimizada para 1 coluna vertical) gerada com sucesso.")


# -------------------------------------------------------------------------
# FIGURA 4: Estudo de Caso Qualitativo — Falha da Baseline vs Solução Proposta
# -------------------------------------------------------------------------
def generate_fig4():
    fig, ax = plt.subplots(figsize=(10.6, 5.2))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    # Cabeçalho visível dentro de ylim(0, 1)
    ax.text(0.5, 0.965,
            'Estudo de Caso Empírico: Instâncias 07741c44 e 07741c45 (Knowledge-Update)',
            ha='center', va='top', fontsize=11.5, fontweight='bold', color='#1a1a2e')
    ax.text(0.5, 0.915,
            'Rastreamento real nos grafos gerados (07741c45_hebbian.json e 07741c45_long_term_kb_graph.json)',
            ha='center', va='top', fontsize=8.8, color='#495057')

    # Linha do Tempo Visual
    ax.plot([0.12, 0.88], [0.76, 0.76], color="#333333", lw=2.2, zorder=1)
    ax.scatter([0.16, 0.50, 0.84], [0.76, 0.76, 0.76],
               color=["#2b5c8f", "#1b8a5a", "#e07a5f"], s=110, zorder=2, edgecolors='black', linewidth=0.8)

    ax.text(0.16, 0.79, 'Sessão 1 ($t_1$)\n20 Mai 2023 (12:36)',
            ha='center', va='bottom', fontsize=8.5, fontweight='bold', color='#2b5c8f')
    ax.text(0.50, 0.79, 'Sessão 2 ($t_2$)\n26 Mai 2023 (13:05)',
            ha='center', va='bottom', fontsize=8.5, fontweight='bold', color='#1b8a5a')
    ax.text(0.84, 0.79, 'Consulta ($t_q$)\n07 Jun 2023 (04:15)',
            ha='center', va='bottom', fontsize=8.5, fontweight='bold', color='#c85a32')

    # Caixas das Sessões com espaçamento amplo para a seta superseded_by
    b_s1 = FancyBboxPatch((0.025, 0.46), 0.255, 0.22,
                          boxstyle="round,pad=0.01,rounding_size=0.015",
                          ec="#2b5c8f", fc="#f4f7fb", lw=1.2)
    ax.add_patch(b_s1)
    ax.text(0.1525, 0.57,
            'Nó Episódico #1 (em $t_1$):\n'
            '"I\'ve been keeping my old\n'
            'sneakers under my bed for\n'
            'storage, and they smell."\n'
            'Estado Factual $f_1$: under bed',
            ha='center', va='center', fontsize=7.6, color='#111')

    b_s2 = FancyBboxPatch((0.375, 0.46), 0.255, 0.22,
                          boxstyle="round,pad=0.01,rounding_size=0.015",
                          ec="#1b8a5a", fc="#f3faf6", lw=1.2)
    ax.add_patch(b_s2)
    ax.text(0.5025, 0.57,
            'Nó Episódico #11 / KB #0 ($t_2$):\n'
            '"I\'m looking forward to storing\n'
            'my old sneakers in a shoe\n'
            'rack in my closet."\n'
            'Estado Factual $f_2$: shoe rack',
            ha='center', va='center', fontsize=7.6, color='#111')

    # Seta de Supersessão conectando a Caixa 1 à Caixa 2 com badge branco legível
    ax.annotate('', xy=(0.365, 0.55), xytext=(0.29, 0.55),
                arrowprops=dict(arrowstyle="-|>,head_width=0.25,head_length=0.35",
                                color="#e76f51", lw=2.0, linestyle="--"))
    ax.text(0.3275, 0.595, 'superseded_by',
            ha='center', va='center', fontsize=7.3, fontweight='bold', color='#d9480f',
            bbox=dict(boxstyle="round,pad=0.18", fc="white", ec="#e76f51", lw=0.9))

    # Caixa da Pergunta 07741c45
    b_q = FancyBboxPatch((0.695, 0.46), 0.28, 0.22,
                         boxstyle="round,pad=0.01,rounding_size=0.015",
                         ec="#e07a5f", fc="#fff8f5", lw=1.3)
    ax.add_patch(b_q)
    ax.text(0.835, 0.57,
            'Query 07741c45 (em $t_q$):\n'
            '"Where do I currently keep\n'
            'my old sneakers?"\n\n'
            'Gabarito: "in a shoe rack\n'
            'in my closet"',
            ha='center', va='center', fontsize=7.7, color='#111')

    # Comportamento Comparado na Resposta (Inferior)
    b_res_base = FancyBboxPatch((0.03, 0.06), 0.44, 0.31,
                                boxstyle="round,pad=0.012,rounding_size=0.02",
                                ec="#b83b3b", fc="#fff5f5", lw=1.5)
    ax.add_patch(b_res_base)
    ax.text(0.25, 0.325, '[Falha Real na Replicação — HeLa-Mem Baseline]',
            ha='center', va='center', fontsize=8.6, fontweight='bold', color='#b83b3b')
    ax.text(0.25, 0.18,
            '• Predição Emitida: "under my bed" (Fato $f_1$, obsoleto)\n'
            '• Avaliação LLM-Judge: INCORRETO (Score = 0)\n'
            '• Diagnóstico no Grafo: O Nó KB #0 recebeu timestamp\n'
            '  de runtime (2026-09-27) e o retriever ignorou $t_q$.\n'
            '  A alta similaridade com "sneakers" ativou o Nó #1 ($f_1$).',
            ha='center', va='center', fontsize=7.7, color='#222')

    b_res_prop = FancyBboxPatch((0.53, 0.06), 0.44, 0.31,
                                boxstyle="round,pad=0.012,rounding_size=0.02",
                                ec="#1b8a5a", fc="#f3faf6", lw=1.5)
    ax.add_patch(b_res_prop)
    ax.text(0.75, 0.325, '[Resolução Analítica — Proposta c/ Validade Temporal]',
            ha='center', va='center', fontsize=8.6, fontweight='bold', color='#1b8a5a')
    ax.text(0.75, 0.18,
            '• Predição Alvo: "in a shoe rack in my closet" (Fato $f_2$)\n'
            '• Avaliação Esperada: CORRETO (Score = 1)\n'
            '• Mecanismo de Correção: Em $t_2$, $f_2$ aplica SUPERSEDES\n'
            '  sobre $f_1$, fechando sua janela em $[t_1, t_2]$. Como $t_q > t_2$,\n'
            '  $\\mathcal{V}(f_1, t_q)$ atenua $f_1$ e prioriza $f_2$ ($[t_2, \\infty)$).',
            ha='center', va='center', fontsize=7.7, color='#222')

    plt.tight_layout()
    fig.savefig(out_dir / "fig4_estudo_caso_supersessao.png", dpi=300, bbox_inches='tight')
    fig.savefig(out_dir / "fig4_estudo_caso_supersessao.pdf", bbox_inches='tight')
    plt.close()
    print("Figura 4 gerada com sucesso.")


if __name__ == "__main__":
    generate_fig1()
    generate_fig2()
    generate_fig3()
    generate_fig4()
    print("Todas as 4 figuras foram regeradas com sucesso em reports/figures/")
