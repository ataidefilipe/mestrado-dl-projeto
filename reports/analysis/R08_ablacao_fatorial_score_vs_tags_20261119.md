# Relatório Técnico R08 — Ablação Fatorial 2×2: Score de Pertinência $\mathcal{V}(f_i, t_{\text{query}})$ vs. Etiquetas Temporais no Prompt

**Data:** 2026-11-19  
**Dataset:** LongMemEval (500 instâncias, variante *oracle* distribuída com o HeLa-Mem)  
**Grafos Base:** `results/longmemeval_temporal_full/` (exatamente os mesmos 500 grafos episódicos e semânticos em todas as 4 condições)  
**Resultados Persistidos:**
- $B_0$ (`no_temporal`): `results/longmemeval_temporal_full/eval_results_b0/eval_summary.json`
- $B_{\text{score}}$ (`score_only`): `results/longmemeval_temporal_full/eval_results_score_only/eval_summary.json`
- $B_{\text{tags}}$ (`tags_only`): `results/longmemeval_temporal_full/eval_results_tags_only/eval_summary.json`
- $B$ (`none` — completo): `results/longmemeval_temporal_full/eval_results/eval_summary.json`

---

## 1. Desenho Experimental (2×2 Controlado)

Na ablação $B_0$ anterior (R05), o score de pertinência temporal $\mathcal{V}(f_i, t_{\text{query}})$ na recuperação e as etiquetas `[CURRENT / ACTIVE]` / `[HISTORICAL / SUPERSEDED]` no prompt haviam sido desligados simultaneamente. Este experimento desacopla os dois mecanismos mantendo **exatamente os mesmos fatos extraídos** nos 500 grafos:

| Condição | Score $\mathcal{V}(f_i, t_{\text{query}})$ no *Retrieval* | Etiquetas `[CURRENT]`/`[HISTORICAL]` + Prompt Temporal |
| :--- | :---: | :---: |
| **$B_0$ (`no_temporal`)** | Desligado ($\mathcal{V} \equiv 1{,}0$, sem arestas `SUPERSEDES`) | Desligado (prompt original HeLa-Mem) |
| **$B_{\text{score}}$ (`score_only`)** | **Ligado** ($\lambda = 0{,}6$, $\tau = 60\text{d}$) | Desligado (prompt original HeLa-Mem) |
| **$B_{\text{tags}}$ (`tags_only`)** | Desligado ($\mathcal{V} \equiv 1{,}0$) | **Ligado** |
| **$B$ (Completo)** | **Ligado** ($\lambda = 0{,}6$, $\tau = 60\text{d}$) | **Ligado** |

---

## 2. Resultados por Categoria ($N = 500$)

| Categoria | $N$ | $B_0$ (`no_temporal`) | $B_{\text{score}}$ (`score_only`) | $B_{\text{tags}}$ (`tags_only`) | $B$ (Completo) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `knowledge-update` | 78 | 51 (65,38%) | 51 (65,38%) | **67 (85,90%)** | 65 (83,33%) |
| `temporal-reasoning` | 133 | **76 (57,14%)** | 71 (53,38%) | 75 (56,39%) | 74 (55,64%) |
| `multi-session` | 133 | **72 (54,14%)** | 68 (51,13%) | 68 (51,13%) | 65 (48,87%) |
| `single-session-preference` | 30 | 12 (40,00%) | 9 (30,00%) | 11 (36,67%) | **14 (46,67%)** |
| `single-session-assistant` | 56 | 50 (89,29%) | 51 (91,07%) | 51 (91,07%) | **52 (92,86%)** |
| `single-session-user` | 70 | **60 (85,71%)** | 59 (84,29%) | 59 (84,29%) | 58 (82,86%) |
| **OVERALL** | **500** | **321 (64,20%)** | **309 (61,80%)** | **331 (66,20%)** | **328 (65,60%)** |

---

## 3. Testes Pareados Exatos de McNemar (Bilaterais)

| Transição | O que isola | OVERALL ($N=500$) | `knowledge-update` ($N=78$) | `multi-session` ($N=133$) |
| :--- | :--- | :---: | :---: | :---: |
| **$B_0 \rightarrow B_{\text{score}}$** | Efeito isolado de $\mathcal{V}$ (sem etiquetas) | +17 / -29 (-12, $p = 0{,}1038$) | +3 / -3 (**0**, $p = 1{,}0000$) | +3 / -7 (-4, $p = 0{,}3438$) |
| **$B_0 \rightarrow B_{\text{tags}}$** | Efeito isolado das etiquetas (sem $\mathcal{V}$) | +37 / -27 (+10, $p = 0{,}2604$) | **+16 / -0 (+16, $p < 0{,}0001$)** | +8 / -12 (-4, $p = 0{,}5034$) |
| **$B_0 \rightarrow B$** | Efeito combinado ($\mathcal{V}$ + etiquetas) | +35 / -28 (+7, $p = 0{,}4500$) | **+14 / -0 (+14, $p = 0{,}0001$)** | +7 / -14 (-7, $p = 0{,}1892$) |
| **$B_{\text{score}} \rightarrow B$** | Adicionar etiquetas sobre $\mathcal{V}$ | **+41 / -22 (+19, $p = 0{,}0226$)** | **+14 / -0 (+14, $p = 0{,}0001$)** | +7 / -10 (-3, $p = 0{,}6291$) |
| **$B_{\text{tags}} \rightarrow B$** | Adicionar $\mathcal{V}$ sobre etiquetas | +19 / -22 (-3, $p = 0{,}7552$) | +1 / -3 (-2, $p = 0{,}6250$) | +4 / -7 (-3, $p = 0{,}5488$) |
| **$B_{\text{score}} \rightarrow B_{\text{tags}}$** | Etiquetas vs. apenas score $\mathcal{V}$ | **+45 / -23 (+22, $p = 0{,}0103$)** | **+16 / -0 (+16, $p < 0{,}0001$)** | +8 / -8 (0, $p = 1{,}0000$) |

---

## 4. Conclusão Científica (Mecanismo Causal)

1. **O motor causal do ganho em `knowledge-update` são as etiquetas de validade explícitas (`[CURRENT]` vs. `[HISTORICAL]`), não o re-ranking por $\mathcal{V}$ isolado.**
   - **`score_only` produz efeito nulo em `knowledge-update`** (`51/78` vs. `51/78`, $p = 1{,}0000$). Como os grafos semânticos no recorte *oracle* possuem em média apenas 9,18 fatos e o *retriever* recupera `semantic_top_k = 5`, tanto o fato antigo quanto o fato atualizado entram no contexto final; sem marcação explícita de vigência, apenas alterar a ordem relativa não elimina a interferência factual no LLM gerador.
   - **`tags_only` captura integralmente o ganho causal em `knowledge-update`**: salto de `65,38%` para **`85,90%`** (**+16 ganhos e 0 regressões**, $p = 0{,}00003$), atingindo **`66,20%` no geral** (maior acurácia absoluta do projeto).
   - Adicionar $\mathcal{V}$ sobre `tags_only` ($B_{\text{tags}} \rightarrow B$) produz variação não significativa dentro do piso de ruído (`-3` no geral, $p = 0{,}7552$; `-2` em KU, $p = 0{,}6250$).
2. **Conexão com o regime *oracle* vs. escala real (Achado 10):**
   - No recorte *oracle* (~9 fatos/grafo), o gargalo não é o *recall@5* (ambas as versões do fato chegam ao prompt), mas sim a **desambiguação de vigência no contexto**, resolvida pelas etiquetas `[CURRENT]`/`[HISTORICAL]`.
   - Em cenários com dezenas de sessões distratoras (como o LongMemEval-S completo de ~40 sessões), o re-ranking por $\mathcal{V}(f_i, t_{\text{query}})$ passa a ter papel estrutural para evitar que fatos obsoletos ocupem vagas do `top-k` em detrimento dos fatos vigentes.
