# Relatório Técnico R07 — Auditoria de Precisão do Classificador de Supersessão ($B$ vs. $B_{\text{v2}}$) e Achado de Ordenação Cronológica

**Data:** 2026-11-19  
**Amostra:** 90 transições `SUPERSEDES` amostradas de forma estratificada (`seed=42`, 15 por categoria × 3 categorias com supersessão × 2 sistemas: $B$ e $B_{\text{v2}}$).  
**Custo de API:** Zero (auditoria sobre grafos persistidos em `results/longmemeval_temporal_full/` e `results/longmemeval_temporal_v2/`).  
**Script de amostragem:** [`src/analysis/sample_supersession_audit.py`](../../src/analysis/sample_supersession_audit.py)  
**CSVs gerados:** [`audit_supersession_sample_B.csv`](audit_supersession_sample_B.csv) e [`audit_supersession_sample_B_v2.csv`](audit_supersession_sample_B_v2.csv).

---

## 1. Volume Global de Supersessões ($B$ vs. $B_{\text{v2}}$)

A substituição do prompt inicial ($B$) pela formulação ontológica baseada em *Event Calculus* sem exemplos de domínio ($B_{\text{v2}}$) reduziu o volume total de arestas `SUPERSEDES` em **53,6%** (de 612 para 284):

| Categoria | $N$ | Nós ($B$) | Sup. ($B$) | % Sup. ($B$) | Nós ($B_{\text{v2}}$) | Sup. ($B_{\text{v2}}$) | % Sup. ($B_{\text{v2}}$) | Redução de Volume |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `knowledge-update` | 78 | 779 | 159 | 20,41% | 784 | 86 | 10,97% | **-45,9%** |
| `multi-session` | 133 | 1.720 | 270 | 15,70% | 1.687 | 128 | 7,59% | **-52,6%** |
| `temporal-reasoning` | 133 | 1.405 | 183 | 13,02% | 1.408 | 70 | 4,97% | **-61,7%** |
| Categorias *single-session* | 156 | 687 | 0 | 0,00% | 681 | 0 | 0,00% | — |
| **Total** | **500** | **4.591** | **612** | **13,33%** | **4.560** | **284** | **6,23%** | **-53,6%** |

---

## 2. Descoberta Estrutural: Sessões Fora de Ordem Cronológica no Dataset

Durante a auditoria dos pares amostrados, identificou-se uma anomalia nos dados de entrada do benchmark:

- **Fato observado:** **34 dos 500 itens** do arquivo `external/HeLa-Mem/data/longmemeval_s.json` possuem `haystack_dates` **não ordenadas cronologicamente** (uma sessão mais cedo no mesmo dia aparece depois de uma sessão mais tarde na lista `haystack_sessions`).
- **Consequência no grafo temporal:** Como `extract_session_turns()` itera na ordem bruta do JSON e `add_knowledge()` verifica apenas `cand_time == ts` (igualdade exata, sem checar `parse_date(ts) < parse_date(cand_time)`), ocorreram **supersessões reversas** (`valid_to < valid_from`):
  - **Proposta $B$:** **34 / 612 (5,6%)** das supersessões são reversas — **100% concentradas em `temporal-reasoning`** (34 casos).
  - **Proposta $B_{\text{v2}}$:** **9 / 284 (3,2%)** são reversas — também **100% em `temporal-reasoning`** (9 casos).
- **Implicação para trabalho futuro:** Ordenar cronologicamente `haystack_sessions` por `parse_date(haystack_dates)` antes da codificação (e impor guarda `t_new > t_old` em `add_knowledge()`) elimina 100% dessa classe de erro sem custo adicional de LLM.

---

## 3. Precisão Empírica do Classificador (Amostra Estratificada, $n = 45$ por Sistema)

Cada transição amostrada foi rotulada segundo critério objetivo de *Event Calculus*:
- **TP (Verdadeiro Positivo):** atualização legítima de atributo unívoco, estado mutuamente exclusivo ou transição de plano para execução/revisão (ex.: *4 engineers → 5 engineers*; *page 200 → page 220*; *Sweet Baby Ray's → Kansas City Masterpiece*; *started reading X → finished reading X*).
- **FP_OVER (*Over-supersession*):** fatos cumulativos, entidades coexistentes ou eventos históricos independentes que deveriam ser `EXTENDS` ou `UNRELATED` (ex.: *50mm lens → 70-200mm lens*; *5-gallon tank → 20-gallon tank*; *friend's wedding → own wedding*; *grandmother's vase → friend's vase*).
- **FP_BACKWARD (Supersessão reversa):** erro causado por `valid_to < valid_from` devido à ordenação não-cronológica das sessões no dataset.

### 3.1 Tabela Comparativa de Precisão

| Categoria | Amostra | $B$: TP | $B$: FP_OVER | $B$: FP_BACK | **Precisão ($B$)** | $B_{\text{v2}}$: TP | $B_{\text{v2}}$: FP_OVER | $B_{\text{v2}}$: FP_BACK | **Precisão ($B_{\text{v2}}$)** |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `knowledge-update` | 15 | 10 | 5 | 0 | **66,7%** | 10 | 5 | 0 | **66,7%** |
| `multi-session` | 15 | 3 | 12 | 0 | **20,0%** | 4 | 11 | 0 | **26,7%** |
| `temporal-reasoning` | 15 | 2 | 6 | 7 | **13,3%** | 8 | 5 | 2 | **53,3%** |
| **Total Estratificado** | **45** | **15** | **23** | **7** | **33,3%** | **22** | **21** | **2** | **48,9%** |

### 3.2 Interpretação dos Achados

1. **Explicação direta do ganho de $B_{\text{v2}}$ em `temporal-reasoning` (`55,64% → 57,89%`):** A precisão do classificador em `temporal-reasoning` quadruplicou (**13,3% → 53,3%**) ao mesmo tempo em que o volume de supersessões caiu 61,7%.
2. **Explicação direta da persistência de regressões residuais em `multi-session`:** Embora $B_{\text{v2}}$ tenha cortado as supersessões em `multi-session` pela metade (270 → 128) e reduzido as regressões frente a $B_0$ (de -7 para -4), a precisão nessa categoria permanece baixa (**26,7%**). Casos como `46a3abf7` (*5-gallon tank → 20-gallon tank*) e `gpt4_2f8be40d` (*friend's wedding → own wedding*) mostram que um classificador baseado apenas em pares textuais com `gpt-4o-mini` ainda confunde eventos/objetos semanticamente similares com substituições de estado.
3. **Estabilidade em `knowledge-update`:** Ambas as versões mantêm precisão de **66,7%** na categoria-alvo, com $B_{\text{v2}}$ sendo mais conservador (86 vs. 159 supersessões), o que explica o ligeiro trade-off em `knowledge-update` (`83,33%` em $B$ vs. `79,49%` em $B_{\text{v2}}$) em troca de menor dano em `multi-session` e melhor desempenho em `temporal-reasoning`.
