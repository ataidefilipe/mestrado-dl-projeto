"""
Script para geração de figuras com qualidade de publicação (IEEE style, 300 DPI)
para a Terceira Entrega (Draft 2) do Projeto de Deep Learning (Mestrado CIn/UFPE).

Gera 5 figuras em reports/figures/ (.png e .pdf):
- fig1_arquitetura_proposta: Arquitetura comparativa + resultados reais dos 500 grafos (4.591 fatos, 612 supersessões)
- fig2_baseline_vs_paper: Comparação tripla (Paper ACL 2026 vs. Baseline A vs. Proposta B) com badges de ganho
- fig3_analise_pareada_ab: Decomposição pareada A/B (Ganhos +54 vs. Regressões -32, McNemar p=0,0115) e taxa de supersessão
- fig4_estudo_caso_supersessao: Estudo de caso empírico triplo (852ce960 Atualização, 50635ada Estado Histórico, 07741c45 Sensibilidade do Juiz)
- fig5_decaimento_pertinencia: Curva analítica de pertinência temporal V(f_i, t_query) e impacto no score de retrieval
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import numpy as np
from pathlib import Path

# Configuração de estilo IEEE
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['axes.titlesize'] = 10.5
plt.rcParams['axes.labelsize'] = 9.5
plt.rcParams['xtick.labelsize'] = 8.5
plt.rcParams['ytick.labelsize'] = 8.5
plt.rcParams['legend.fontsize'] = 8.5

out_dir = Path("reports/figures")
out_dir.mkdir(parents=True, exist_ok=True)


# -------------------------------------------------------------------------
# FIGURA 1: Arquitetura Comparativa (HeLa-Mem Baseline vs Proposta B Executada)
# -------------------------------------------------------------------------
def generate_fig1():
    fig, ax = plt.subplots(figsize=(10.8, 5.5))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    ax.text(0.5, 0.968,
            'Arquitetura: Baseline A (HeLa-Mem) vs. Proposta B (Validade Temporal)',
            ha='center', va='top', fontsize=11.8, fontweight='bold', color='#1a1a2e')

    # Painel Esquerdo: HeLa-Mem Baseline A
    box_left = FancyBboxPatch((0.02, 0.04), 0.455, 0.86,
                              boxstyle="round,pad=0.015,rounding_size=0.025",
                              ec="#2b5c8f", fc="#f4f7fb", lw=1.8)
    ax.add_patch(box_left)
    ax.text(0.2475, 0.865, 'Baseline A: HeLa-Mem Original (ACL 2026)',
            ha='center', va='center', fontsize=10.5, fontweight='bold', color='#2b5c8f')

    b1 = FancyBboxPatch((0.045, 0.68), 0.405, 0.12,
                        boxstyle="round,pad=0.01,rounding_size=0.015",
                        ec="#3b5998", fc="#ffffff", lw=1.1)
    ax.add_patch(b1)
    ax.text(0.2475, 0.74,
            '1. Memória Episódica (Grafo Hebbiano)\n'
            'Nós: turnos de diálogo | Arestas: força sináptica ($w_{ij}$), $\\eta = 0{,}02$\n'
            'Decaimento temporal neutralizado no código (bug mantido em A e B)',
            ha='center', va='center', fontsize=8.1, color='#111')

    b2 = FancyBboxPatch((0.045, 0.48), 0.405, 0.12,
                        boxstyle="round,pad=0.01,rounding_size=0.015",
                        ec="#3b5998", fc="#ffffff", lw=1.1)
    ax.add_patch(b2)
    ax.text(0.2475, 0.54,
            '2. Memória Semântica Estática (HebbianKnowledgeMemory)\n'
            'Extração em blocos de 10 turnos, sem a data da sessão\n'
            '360/500 grafos semânticos vazios (causa em investigação)',
            ha='center', va='center', fontsize=8.0, color='#111')

    b3 = FancyBboxPatch((0.045, 0.28), 0.405, 0.12,
                        boxstyle="round,pad=0.01,rounding_size=0.015",
                        ec="#b83b3b", fc="#fff5f5", lw=1.3)
    ax.add_patch(b3)
    ax.text(0.2475, 0.34,
            '3. Busca Semântica sem Noção de Validade:\n'
            'Fatos não têm vigência e a busca ignora $t_{query}$;\n'
            'fato obsoleto e estado atual competem só por similaridade',
            ha='center', va='center', fontsize=8.0, fontweight='bold', color='#b83b3b')

    b4 = FancyBboxPatch((0.045, 0.08), 0.405, 0.12,
                        boxstyle="round,pad=0.01,rounding_size=0.015",
                        ec="#495057", fc="#e9ecef", lw=1.2)
    ax.add_patch(b4)
    ax.text(0.2475, 0.14,
            '4. Reprodução (500 instâncias):\n'
            'Acurácia Global: 61,20% (306/500) | 194 erros totais\n'
            'Knowledge Update: 73,08% | Temporal Reasoning: 51,88%',
            ha='center', va='center', fontsize=8.0, fontweight='bold', color='#343a40')

    arrow_kw_left = dict(arrowstyle="-|>,head_width=0.3,head_length=0.45", color="#2b5c8f", lw=1.6)
    ax.annotate('', xy=(0.2475, 0.612), xytext=(0.2475, 0.668), arrowprops=arrow_kw_left)
    ax.annotate('', xy=(0.2475, 0.412), xytext=(0.2475, 0.468), arrowprops=arrow_kw_left)
    ax.annotate('', xy=(0.2475, 0.212), xytext=(0.2475, 0.268), arrowprops=arrow_kw_left)

    # Painel Direito: Proposta B (Validade Temporal & Supersessão)
    box_right = FancyBboxPatch((0.525, 0.04), 0.455, 0.86,
                               boxstyle="round,pad=0.015,rounding_size=0.025",
                               ec="#1b8a5a", fc="#f3faf6", lw=1.8)
    ax.add_patch(box_right)
    ax.text(0.7525, 0.865, 'Proposta B: TemporalKnowledgeMemory + ValidityRetriever',
            ha='center', va='center', fontsize=10.2, fontweight='bold', color='#1b8a5a')

    p1 = FancyBboxPatch((0.55, 0.68), 0.405, 0.12,
                        boxstyle="round,pad=0.01,rounding_size=0.015",
                        ec="#1b8a5a", fc="#ffffff", lw=1.1)
    ax.add_patch(p1)
    ax.text(0.7525, 0.74,
            '1. Mesmos grafos episódicos de A + Extração por Sessão\n'
            'Fatos ancorados na data real da sessão (haystack_dates)\n'
            '4.591 fatos semânticos (500/500 grafos populados)',
            ha='center', va='center', fontsize=8.0, color='#111')

    p2 = FancyBboxPatch((0.55, 0.48), 0.405, 0.12,
                        boxstyle="round,pad=0.01,rounding_size=0.015",
                        ec="#1b8a5a", fc="#ffffff", lw=1.2)
    ax.add_patch(p2)
    ax.text(0.7525, 0.54,
            '2. Supersessão Explícita e Janela $[t_{start}, t_{end}]$:\n'
            'Tupla $f_i = \\langle c_i, \\mathbf{e}_i, [t_{start}, t_{end}], \\mathcal{S}_i, \\mathbf{w}_i \\rangle$\n'
            '612 transições SUPERSEDES em 249 diálogos (92,3% em Knowl.-Update)',
            ha='center', va='center', fontsize=7.9, color='#111')

    p3 = FancyBboxPatch((0.55, 0.28), 0.405, 0.12,
                        boxstyle="round,pad=0.01,rounding_size=0.015",
                        ec="#1b8a5a", fc="#e8f8f0", lw=1.3)
    ax.add_patch(p3)
    ax.text(0.7525, 0.34,
            '3. Retrieval Ponderado por $\\mathcal{V}(f_i, t_{query})$ + Status Tags:\n'
            'Atenuação exponencial de fatos expirados ($t_{query} > t_{end}$)\n'
            'Tags: [CURRENT / ACTIVE] vs. [HISTORICAL / SUPERSEDED]',
            ha='center', va='center', fontsize=7.5, fontweight='bold', color='#1b8a5a')

    p4 = FancyBboxPatch((0.55, 0.08), 0.405, 0.12,
                        boxstyle="round,pad=0.01,rounding_size=0.015",
                        ec="#0f5132", fc="#d1f2e1", lw=1.3)
    ax.add_patch(p4)
    ax.text(0.7525, 0.14,
            '4. Resultado Preliminar (500 instâncias):\n'
            'Acurácia Global: 65,60% (+4,40 p.p. sobre A)\n'
            'Knowledge Update: 83,33% | Temporal Reasoning: 55,64%',
            ha='center', va='center', fontsize=8.0, fontweight='bold', color='#0f5132')

    arrow_kw_right = dict(arrowstyle="-|>,head_width=0.3,head_length=0.45", color="#1b8a5a", lw=1.6)
    ax.annotate('', xy=(0.7525, 0.612), xytext=(0.7525, 0.668), arrowprops=arrow_kw_right)
    ax.annotate('', xy=(0.7525, 0.412), xytext=(0.7525, 0.468), arrowprops=arrow_kw_right)
    ax.annotate('', xy=(0.7525, 0.212), xytext=(0.7525, 0.268), arrowprops=arrow_kw_right)

    plt.tight_layout()
    fig.savefig(out_dir / "fig1_arquitetura_proposta.png", dpi=300, bbox_inches='tight')
    fig.savefig(out_dir / "fig1_arquitetura_proposta.pdf", bbox_inches='tight')
    plt.close()
    print("Figura 1 gerada com sucesso.")


# -------------------------------------------------------------------------
# FIGURA 2: Evolução de Desempenho por Categoria (Paper vs Baseline A vs Proposta B)
# -------------------------------------------------------------------------
def generate_fig2():
    # (rótulo, n, acertos A, acertos B, % artigo ou None quando o artigo não reporta, acertos B0)
    rows = [
        ("Single-Sess. Preference", 30, 8, 14, None, 12),
        ("Single-Sess. Assistant", 56, 49, 52, None, 50),
        ("Single-Sess. User", 70, 61, 58, None, 60),
        ("Single-Session (agregado)", 156, 118, 124, 78.85, 122),
        ("Multi-Session", 133, 62, 65, 57.14, 72),
        ("Temporal Reasoning", 133, 69, 74, 50.38, 76),
        ("Knowledge Update", 78, 57, 65, 78.21, 51),
        ("OVERALL", 500, 306, 328, 65.40, 321),
    ]
    categories = [f"{r[0]}\n(n={r[1]})" for r in rows]
    base_scores = [100.0 * r[2] / r[1] for r in rows]
    prop_scores = [100.0 * r[3] / r[1] for r in rows]
    b0_scores = [100.0 * r[5] / r[1] for r in rows]
    paper_scores = [r[4] for r in rows]
    pct = lambda v: f"{v:.1f}".replace(".", ",") + "%"

    y = np.arange(len(categories))
    height = 0.2

    fig, ax = plt.subplots(figsize=(6.8, 5.8))

    c_paper = "#6c757d"   # Cinza azulado (Referência ACL 2026)
    c_base  = "#e07a5f"   # Coral (Baseline A Replicada)
    c_prop  = "#1b8a5a"   # Verde Esmeralda (Proposta B)

    paper_y = [yy + 1.5 * height for yy, p in zip(y, paper_scores) if p is not None]
    paper_v = [p for p in paper_scores if p is not None]
    rects_paper = ax.barh(paper_y, paper_v, height,
                          label='Artigo (valor reportado)',
                          color=c_paper, edgecolor='black', linewidth=0.5, alpha=0.75)
    rects_base  = ax.barh(y + 0.5 * height, base_scores, height,
                          label='Baseline A',
                          color=c_base, edgecolor='black', linewidth=0.6, alpha=0.90)
    rects_b0    = ax.barh(y - 0.5 * height, b0_scores, height,
                          label='B0 (extração por sessão, sem tempo)',
                          color='#8d99ae', edgecolor='black', linewidth=0.6, alpha=0.95)
    rects_prop  = ax.barh(y - 1.5 * height, prop_scores, height,
                          label='Proposta B',
                          color=c_prop, edgecolor='black', linewidth=0.6, alpha=0.95)

    for rects in (rects_paper, rects_base, rects_b0, rects_prop):
        for rect in rects:
            w = rect.get_width()
            ax.annotate(pct(w),
                        xy=(w - 1.2, rect.get_y() + rect.get_height() / 2),
                        ha='right', va='center', fontsize=6.5, fontweight='bold', color='white')

    # Δ B0→B (efeito do mecanismo temporal), calculado a partir das contagens
    for i, r in enumerate(rows):
        diff = 100.0 * (r[3] - r[5]) / r[1]
        color_diff = "#0f5132" if diff >= 0 else "#b83b3b"
        bg_diff = "#d1f2e1" if diff >= 0 else "#ffe3e3"
        max_w = max(v for v in (paper_scores[i], base_scores[i], b0_scores[i], prop_scores[i]) if v is not None)
        label = f"Δ B0→B: {diff:+.2f}".replace(".", ",") + " p.p."
        ax.text(max_w + 1.8, y[i] - height, label,
                ha='left', va='center', fontsize=7.0, fontweight='bold', color=color_diff,
                bbox=dict(boxstyle="round,pad=0.18", fc=bg_diff, ec=color_diff, lw=0.8))

    # Separadores: sessão única detalhada | agregado | OVERALL
    ax.axhline(2.5, color='#333333', linestyle=':', linewidth=0.9, alpha=0.5)
    ax.axhline(len(categories) - 1.5, color='#333333', linestyle='-', linewidth=1.0, alpha=0.5)

    ax.set_xlabel('Acurácia (%)', fontsize=9.0, fontweight='bold')
    ax.set_yticks(y)
    ax.set_yticklabels(categories, fontsize=7.8, fontweight='bold')
    ax.set_xlim(0, 120)
    ax.set_xticks([0, 20, 40, 60, 80, 100])
    ax.grid(axis='x', linestyle='--', alpha=0.35)

    ax.legend(frameon=True, facecolor='white', edgecolor='#cccccc',
              loc='upper center', bbox_to_anchor=(0.5, -0.09), ncol=2,
              fontsize=7.4, borderpad=0.3)

    plt.tight_layout()
    fig.savefig(out_dir / "fig2_baseline_vs_paper.png", dpi=300, bbox_inches='tight')
    fig.savefig(out_dir / "fig2_baseline_vs_paper.pdf", bbox_inches='tight')
    plt.close()
    print("Figura 2 gerada com sucesso.")


# -------------------------------------------------------------------------
# FIGURA 3: Análise Pareada A/B (Ganhos vs Regressões) e Taxa de Supersessão
# -------------------------------------------------------------------------
def generate_fig3():
    cats_short = [
        "Knowledge Update\n(n=78)",
        "Single-Sess. Pref.\n(n=30)",
        "Temporal Reas.\n(n=133)",
        "Multi-Session\n(n=133)",
        "Single-Sess. Asst.\n(n=56)",
        "Single-Sess. User\n(n=70)"
    ]
    # Transições pareadas por etapa (ganhos, regressões), mesma ordem de cats_short
    a_b0 = [(5, 11), (6, 2), (16, 9), (16, 6), (2, 1), (2, 3)]
    b0_b = [(14, 0), (3, 1), (8, 10), (7, 14), (2, 0), (1, 3)]
    net_a_b0 = np.array([g - r for g, r in a_b0])
    net_b0_b = np.array([g - r for g, r in b0_b])

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.2, 4.0), gridspec_kw={'width_ratios': [1.35, 1.0]})

    y = np.arange(len(cats_short))
    hh = 0.36

    # Subplot A: decomposição do saldo líquido por etapa
    ax1.barh(y - hh / 2, net_a_b0, height=hh, color='#8d99ae', edgecolor='black', linewidth=0.6,
             label='A → B0: extração por sessão (saldo +15)')
    ax1.barh(y + hh / 2, net_b0_b, height=hh, color='#1b8a5a', edgecolor='black', linewidth=0.6,
             label='B0 → B: mecanismo temporal (saldo +7)')
    ax1.axvline(0, color='black', linewidth=1.0)

    for i in range(len(cats_short)):
        for dy, net, (g, r) in ((-hh / 2, net_a_b0[i], a_b0[i]), (hh / 2, net_b0_b[i], b0_b[i])):
            x = net + (0.4 if net >= 0 else -0.4)
            label = f"{net:+d} (+{g}/−{r})"
            if i == 0 and dy > 0:
                label += "  Holm p = 0,0015"
            ax1.text(x, y[i] + dy, label, ha='left' if net >= 0 else 'right',
                     va='center', fontsize=6.8, fontweight='bold',
                     color='#0f5132' if (i == 0 and dy > 0) else '#222')

    ax1.set_yticks(y)
    ax1.set_yticklabels(cats_short, fontsize=8.2, fontweight='bold')
    ax1.invert_yaxis()
    ax1.set_xlim(-16, 30)
    ax1.set_xlabel('Saldo líquido de questões (ganhos − regressões)', fontsize=8.5, fontweight='bold')
    ax1.set_title('(A) Decomposição do Ganho por Etapa e Categoria',
                  fontsize=8.8, fontweight='bold', pad=22)
    ax1.grid(axis='x', linestyle='--', alpha=0.35)
    ax1.legend(loc='upper center', bbox_to_anchor=(0.45, 1.11), ncol=2,
               frameon=True, facecolor='white', edgecolor='#cccccc', fontsize=6.8, borderpad=0.25)

    # Subplot B: Ativação da Supersessão por Categoria
    x_pos = np.arange(3)
    multi_cats = ["Knowledge\nUpdate", "Multi-\nSession", "Temporal\nReasoning"]
    d_rates = [92.3, 78.9, 54.1]
    f_rates = [20.4, 15.7, 13.0]
    w = 0.34

    b_diag = ax2.bar(x_pos - w/2, d_rates, w, label='% Diálogos c/ Supersessão',
                     color='#2b5c8f', edgecolor='black', linewidth=0.6, alpha=0.9)
    b_fact = ax2.bar(x_pos + w/2, f_rates, w, label='% Fatos Substituídos (KB)',
                     color='#f4a261', edgecolor='black', linewidth=0.6, alpha=0.95)

    for rect in b_diag:
        h = rect.get_height()
        ax2.text(rect.get_x() + rect.get_width()/2, h + 1.5, f"{h:.1f}%",
                 ha='center', va='bottom', fontsize=7.5, fontweight='bold', color='#1d3f63')
    for rect in b_fact:
        h = rect.get_height()
        ax2.text(rect.get_x() + rect.get_width()/2, h + 1.5, f"{h:.1f}%",
                 ha='center', va='bottom', fontsize=7.5, fontweight='bold', color='#b5651d')

    ax2.set_xticks(x_pos)
    ax2.set_xticklabels(multi_cats, fontsize=8.2, fontweight='bold')
    ax2.set_ylim(0, 112)
    ax2.set_ylabel('Frequência Relativa (%)', fontsize=8.5, fontweight='bold')
    ax2.set_title('(B) Supersessão nas Categorias Multi-Sessão',
                  fontsize=8.8, fontweight='bold', pad=22)
    ax2.grid(axis='y', linestyle='--', alpha=0.35)
    ax2.legend(loc='upper center', bbox_to_anchor=(0.5, 1.11), ncol=2,
               frameon=True, facecolor='white', edgecolor='#cccccc', fontsize=7.3, borderpad=0.25)

    plt.tight_layout(w_pad=2.5)
    fig.savefig(out_dir / "fig3_analise_pareada_ab.png", dpi=300, bbox_inches='tight')
    fig.savefig(out_dir / "fig3_analise_pareada_ab.pdf", bbox_inches='tight')
    plt.close()
    print("Figura 3 gerada com sucesso.")


# -------------------------------------------------------------------------
# FIGURA 4: Estudos de Caso Qualitativos Reais (Sucesso, Histórico e Limitação do Juiz)
# -------------------------------------------------------------------------
def generate_fig4():
    fig, ax = plt.subplots(figsize=(10.8, 5.8))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    ax.text(0.5, 0.97,
            'Análise Qualitativa nos Grafos de B: Casos em que o Mecanismo Temporal Muda a Resposta',
            ha='center', va='top', fontsize=11.5, fontweight='bold', color='#1a1a2e')

    # --- CASO 1: Atualização de Estado (852ce960) ---
    c1_box = FancyBboxPatch((0.015, 0.64), 0.97, 0.27,
                            boxstyle="round,pad=0.01,rounding_size=0.018",
                            ec="#1b8a5a", fc="#f3faf6", lw=1.5)
    ax.add_patch(c1_box)
    ax.text(0.03, 0.885, 'Caso 1 — Estado atual recuperado pela supersessão (ID: a2f3aa27 | Knowledge-Update | A ✗   B0 ✗   B ✓)',
            ha='left', va='center', fontsize=9.0, fontweight='bold', color='#0f5132')

    # Caixas internas Caso 1
    b1_a = FancyBboxPatch((0.03, 0.665), 0.28, 0.18, boxstyle="round,pad=0.008", ec="#6c757d", fc="white", lw=1.0)
    ax.add_patch(b1_a)
    ax.text(0.17, 0.755,
            'Nó KB #0 [28/Mai/2023 06:23 → 14:10]\n'
            'Status: HISTORICAL / SUPERSEDED (por #5)\n'
            '"User has 1250 followers on Instagram\n'
            'as of May 28, 2023."',
            ha='center', va='center', fontsize=7.4, color='#333')

    ax.annotate('', xy=(0.355, 0.755), xytext=(0.315, 0.755),
                arrowprops=dict(arrowstyle="-|>,head_width=0.22,head_length=0.3", color="#e76f51", lw=1.8, linestyle="--"))
    ax.text(0.335, 0.79, 'SUPERSEDES', ha='center', va='center', fontsize=6.5, fontweight='bold', color='#d9480f')

    b1_b = FancyBboxPatch((0.36, 0.665), 0.28, 0.18, boxstyle="round,pad=0.008", ec="#1b8a5a", fc="white", lw=1.2)
    ax.add_patch(b1_b)
    ax.text(0.50, 0.755,
            'Nó KB #5 [28/Mai/2023 14:10 → ∞]\n'
            'Status: CURRENT / ACTIVE\n'
            '"User is nearing 1300 followers\n'
            'on Instagram."',
            ha='center', va='center', fontsize=7.4, color='#111')

    b1_c = FancyBboxPatch((0.66, 0.665), 0.31, 0.18, boxstyle="round,pad=0.008", ec="#0f5132", fc="#d1f2e1", lw=1.1)
    ax.add_patch(b1_c)
    ax.text(0.815, 0.755,
            'Pergunta: "How many followers do I have\non Instagram now?"  (gabarito: 1300)\n'
            '• Baseline A: "1250" ✗\n'
            '• B0 (sem validade): "1250" ✗\n'
            '• Proposta B: "1300 followers" ✓',
            ha='center', va='center', fontsize=7.4, fontweight='bold', color='#0f5132')

    # --- CASO 2: Consulta a Estado Passado / Histórico (50635ada) ---
    c2_box = FancyBboxPatch((0.015, 0.33), 0.97, 0.27,
                            boxstyle="round,pad=0.01,rounding_size=0.018",
                            ec="#2b5c8f", fc="#f4f7fb", lw=1.5)
    ax.add_patch(c2_box)
    ax.text(0.03, 0.575, 'Caso 2 — Sem validade, o fato obsoleto é somado ao atual (ID: 01493427 | Knowledge-Update | A ✓   B0 ✗   B ✓)',
            ha='left', va='center', fontsize=9.0, fontweight='bold', color='#1d3f63')

    b2_a = FancyBboxPatch((0.03, 0.355), 0.28, 0.18, boxstyle="round,pad=0.008", ec="#6c757d", fc="white", lw=1.0)
    ax.add_patch(b2_a)
    ax.text(0.17, 0.445,
            'Nó KB #0 [11/Ago/2023 → 30/Nov/2023]\n'
            'Status: HISTORICAL / SUPERSEDED (por #5)\n'
            '"User mentioned adding 17 new\n'
            'postcards to their collection."',
            ha='center', va='center', fontsize=7.4, color='#333')

    ax.annotate('', xy=(0.355, 0.445), xytext=(0.315, 0.445),
                arrowprops=dict(arrowstyle="-|>,head_width=0.22,head_length=0.3", color="#e76f51", lw=1.8, linestyle="--"))
    ax.text(0.335, 0.48, 'SUPERSEDES', ha='center', va='center', fontsize=6.5, fontweight='bold', color='#d9480f')

    b2_b = FancyBboxPatch((0.36, 0.355), 0.28, 0.18, boxstyle="round,pad=0.008", ec="#2b5c8f", fc="white", lw=1.2)
    ax.add_patch(b2_b)
    ax.text(0.50, 0.445,
            'Nó KB #5 [30/Nov/2023 → ∞]\n'
            'Status: CURRENT / ACTIVE\n'
            '"User mentioned adding 25 new postcards\n'
            'since restarting collecting."',
            ha='center', va='center', fontsize=7.4, color='#111')

    b2_c = FancyBboxPatch((0.66, 0.355), 0.31, 0.18, boxstyle="round,pad=0.008", ec="#1d3f63", fc="#dbeafe", lw=1.1)
    ax.add_patch(b2_c)
    ax.text(0.815, 0.445,
            'Pergunta: "How many new postcards have I added\nsince I started collecting again?"  (gabarito: 25)\n'
            '• Baseline A: "25" ✓\n'
            '• B0 (sem validade): "42" ✗  (17 + 25)\n'
            '• Proposta B: "25" ✓',
            ha='center', va='center', fontsize=7.2, fontweight='bold', color='#1d3f63')

    # --- CASO 3: Mudança Correta de Estado vs. Granularidade do Juiz (07741c45) ---
    c3_box = FancyBboxPatch((0.015, 0.02), 0.97, 0.27,
                            boxstyle="round,pad=0.01,rounding_size=0.018",
                            ec="#e07a5f", fc="#fff8f5", lw=1.5)
    ax.add_patch(c3_box)
    ax.text(0.03, 0.265, 'Caso 3 — Estado correto, detalhe perdido na extração (ID: 07741c45 | Knowledge-Update | A ✗   B0 ✗   B ✗)',
            ha='left', va='center', fontsize=9.0, fontweight='bold', color='#9c4221')

    b3_a = FancyBboxPatch((0.03, 0.045), 0.28, 0.18, boxstyle="round,pad=0.008", ec="#6c757d", fc="white", lw=1.0)
    ax.add_patch(b3_a)
    ax.text(0.17, 0.135,
            'Nó KB #4 [20/Mai/2023 → 26/Mai/2023]\n'
            'Status: HISTORICAL / SUPERSEDED\n'
            '"User has kept old sneakers stored\n'
            'under their bed, causing them to smell."',
            ha='center', va='center', fontsize=7.4, color='#333')

    ax.annotate('', xy=(0.355, 0.135), xytext=(0.315, 0.135),
                arrowprops=dict(arrowstyle="-|>,head_width=0.22,head_length=0.3", color="#e76f51", lw=1.8, linestyle="--"))
    ax.text(0.335, 0.17, 'SUPERSEDES', ha='center', va='center', fontsize=6.5, fontweight='bold', color='#d9480f')

    b3_b = FancyBboxPatch((0.36, 0.045), 0.28, 0.18, boxstyle="round,pad=0.008", ec="#e07a5f", fc="white", lw=1.2)
    ax.add_patch(b3_b)
    ax.text(0.50, 0.135,
            'Nó KB #9 [26/Mai/2023 → ∞]\n'
            'Status: CURRENT / ACTIVE\n'
            '"User is currently storing old\n'
            'sneakers in a shoe rack." (omitiu "in closet")',
            ha='center', va='center', fontsize=7.4, color='#111')

    b3_c = FancyBboxPatch((0.66, 0.045), 0.31, 0.18, boxstyle="round,pad=0.008", ec="#9c4221", fc="#ffedd5", lw=1.1)
    ax.add_patch(b3_c)
    ax.text(0.815, 0.135,
            'Pergunta: "Where do I currently keep my old sneakers?"\n'
            '• Baseline A: "under my bed" ✗ (estado antigo)\n'
            '• B0 (sem validade): "under your bed" ✗ (estado antigo)\n'
            '• Proposta B: "in a shoe rack" ✗ (estado certo; o juiz\n'
            '  exigiu "in a shoe rack in my closet")',
            ha='center', va='center', fontsize=7.3, fontweight='bold', color='#9c4221')

    plt.tight_layout()
    fig.savefig(out_dir / "fig4_estudo_caso_supersessao.png", dpi=300, bbox_inches='tight')
    fig.savefig(out_dir / "fig4_estudo_caso_supersessao.pdf", bbox_inches='tight')
    plt.close()
    print("Figura 4 gerada com sucesso.")


# -------------------------------------------------------------------------
# FIGURA 5: Dinâmica de Pertinência Temporal V(f_i, t_query) e Score Combinado
# -------------------------------------------------------------------------
def generate_fig5():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.8, 3.3))

    # Subplot A: Curva de Pertinência Temporal V(f_i, t_q)
    days = np.linspace(-15, 120, 500)
    # Fato f_1 válido de t=0 a t=30 dias; tau_decay = 60 dias
    v_f1 = np.zeros_like(days)
    for idx, d in enumerate(days):
        if d < 0:
            v_f1[idx] = 0.0
        elif d <= 30:
            v_f1[idx] = 1.0
        else:
            v_f1[idx] = np.exp(-(d - 30.0) / 60.0)

    # Fato f_2 (supersessor) válido de t=30 a inf
    v_f2 = np.where(days >= 30, 1.0, 0.0)

    ax1.plot(days, v_f1, label='Fato Antigo $f_1$ ($[t_1=0, t_2=30]$)', color='#e63946', lw=2.2)
    ax1.plot(days, v_f2, label='Fato Novo $f_2$ ($[t_2=30, \\infty)$)', color='#1b8a5a', lw=2.2, linestyle='--')
    ax1.axvline(30, color='#333', linestyle=':', lw=1.2)
    ax1.text(33, 0.45, 'Evento SUPERSEDES\n($t_{event} = 30$d)', fontsize=7.5, fontweight='bold', color='#333',
             bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none", alpha=0.85))

    ax1.fill_between(days, 0, v_f1, where=(days >= 0) & (days <= 30), color='#e63946', alpha=0.12)
    ax1.fill_between(days, 0, v_f2, where=(days >= 30), color='#1b8a5a', alpha=0.12)

    ax1.set_xlabel('Tempo Relativo da Consulta $t_{query}$ (dias)', fontsize=8.5, fontweight='bold')
    ax1.set_ylabel('Pertinência Temporal $\\mathcal{V}(f_i, t_{query})$', fontsize=8.5, fontweight='bold')
    ax1.set_title('(A) Transição de Vigência e Decaimento Pós-Supersessão', fontsize=9.0, fontweight='bold')
    ax1.set_ylim(-0.05, 1.12)
    ax1.set_xlim(-10, 120)
    ax1.grid(True, linestyle='--', alpha=0.35)
    ax1.legend(loc='lower right', fontsize=7.5, frameon=True, facecolor='white')

    # Subplot B: Inversão de Ranking no Retrieval (Sim(f1)=0.85 vs Sim(f2)=0.78, lambda=0.6)
    lam = 0.6
    sim_f1 = 0.85  # Fato antigo ligeiramente mais similar lexicalmente à pergunta
    sim_f2 = 0.78  # Fato novo com termos ligeiramente diferentes

    score_base_f1 = np.full_like(days, sim_f1)
    score_base_f2 = np.full_like(days, sim_f2)

    score_prop_f1 = lam * sim_f1 + (1 - lam) * v_f1
    score_prop_f2 = lam * sim_f2 + (1 - lam) * v_f2

    q_days = days[days >= 30]
    s_f1_after = score_prop_f1[days >= 30]
    s_f2_after = score_prop_f2[days >= 30]

    ax2.plot(q_days, s_f1_after, label='Score Proposta $f_1$ ($\\text{Sim}=0,85$, expirado)', color='#e63946', lw=2.2)
    ax2.plot(q_days, s_f2_after, label='Score Proposta $f_2$ ($\\text{Sim}=0,78$, ativo)', color='#1b8a5a', lw=2.2)
    ax2.axhline(sim_f1, color='#e63946', linestyle=':', lw=1.2, alpha=0.7, label='Só similaridade $f_1$ (0,85)')
    ax2.axhline(sim_f2, color='#1b8a5a', linestyle=':', lw=1.2, alpha=0.7, label='Só similaridade $f_2$ (0,78)')

    # Ponto de cruzamento (crossover)
    cross_idx = np.where(s_f2_after >= s_f1_after)[0][0]
    cross_day = q_days[cross_idx]
    cross_val = s_f2_after[cross_idx]
    ax2.scatter([cross_day], [cross_val], color='black', s=45, zorder=5)
    ax2.annotate(f'Inversão de Ranking\n($t_q \\approx {cross_day:.0f}$d)',
                 xy=(cross_day, cross_val), xytext=(cross_day + 10, cross_val - 0.12),
                 arrowprops=dict(arrowstyle="->", color="black", lw=1.0),
                 fontsize=7.5, fontweight='bold')

    ax2.set_xlabel('Data da Consulta $t_{query}$ após Supersessão (dias)', fontsize=8.5, fontweight='bold')
    ax2.set_ylabel('Score de Recuperação ($\\lambda=0,6$)', fontsize=8.5, fontweight='bold')
    ax2.set_title('(B) Exemplo Ilustrativo de Inversão de Ranking ($t_{query} > t_{end}$)', fontsize=9.0, fontweight='bold')
    ax2.set_xlim(30, 120)
    ax2.set_ylim(0.55, 0.96)
    ax2.grid(True, linestyle='--', alpha=0.35)
    ax2.legend(loc='lower left', fontsize=7.0, frameon=True, facecolor='white', ncol=1)

    plt.tight_layout()
    fig.savefig(out_dir / "fig5_decaimento_pertinencia.png", dpi=300, bbox_inches='tight')
    fig.savefig(out_dir / "fig5_decaimento_pertinencia.pdf", bbox_inches='tight')
    plt.close()
    print("Figura 5 gerada com sucesso.")


if __name__ == "__main__":
    generate_fig1()
    generate_fig2()
    generate_fig3()
    generate_fig4()
    generate_fig5()
    print("Todas as 5 figuras da Entrega 2 (Draft 2) foram geradas com sucesso em reports/figures/")
