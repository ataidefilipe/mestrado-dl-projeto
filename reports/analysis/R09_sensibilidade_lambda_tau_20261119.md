# Relatório Técnico R09 — Análise de Sensibilidade de $\lambda$ e $\tau$ (Etapa 7 do Plano R05)

**Data:** 2026-11-19  
**Regra Pré-Registrada (AGENT.MD §19 e Plano R05 Etapa 7):** A configuração reportada da Proposta $B$ permanece fixada em **$\lambda = 0{,}6$** e **$\tau = 60\text{ dias}$**. As variações abaixo **não** são utilizadas para seleção de hiperparâmetros no conjunto de teste; seu objetivo exclusivo é classificar a estabilidade do resultado como **Robusto**, **Sensível** ou **Inconclusivo**.  
**Grafos Base:** `results/longmemeval_temporal_full/` (500 itens, sem recodificação — apenas reavaliação).  
**Limitação registrada:** A sensibilidade de $\theta$ (`supersede_sim_threshold = 0,35`) exige recodificação completa da memória semântica e fica registrada como limitação.

---

## 1. Tabela Consolidada de Sensibilidade ($N = 500$)

| Configuração | OVERALL ($N=500$) | `knowledge-update` ($N=78$) | `temporal-reasoning` ($N=133$) | `multi-session` ($N=133$) | vs. $B_{\text{ref}}$ (ALL, McNemar) | vs. $B_0$ (KU, McNemar) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **$B_{\text{ref}}$ ($\lambda=0{,}6, \tau=60\text{d}$)** | **65,60%** (328) | **83,33%** (65) | 55,64% (74) | 48,87% (65) | referência | **+14 (+14/-0, $p=0{,}0001$)** |
| $B'$ (réplica, piso de ruído) | 64,00% (320) | 83,33% (65) | 51,13% (68) | 50,38% (67) | -8 (+14/-22, $p=0{,}243$) | **+14 (+14/-0, $p=0{,}0001$)** |
| $\lambda = 0{,}4,\; \tau = 60\text{d}$ | 65,60% (328) | 79,49% (62) | 56,39% (75) | 50,38% (67) | 0 (+19/-19, $p=1{,}000$) | **+11 (+12/-1, $p=0{,}0034$)** |
| $\lambda = 0{,}8,\; \tau = 60\text{d}$ | 66,80% (334) | 84,62% (66) | 57,89% (77) | 51,13% (68) | +6 (+26/-20, $p=0{,}461$) | **+15 (+15/-0, $p=0{,}0001$)** |
| $\lambda = 0{,}6,\; \tau = 30\text{d}$ | 66,20% (331) | 79,49% (62) | 58,65% (78) | 49,62% (66) | +3 (+21/-18, $p=0{,}749$) | **+11 (+11/-0, $p=0{,}0010$)** |
| $\lambda = 0{,}6,\; \tau = 90\text{d}$ | 65,80% (329) | 84,62% (66) | 53,38% (71) | 51,88% (69) | +1 (+16/-15, $p=1{,}000$) | **+15 (+15/-0, $p=0{,}0001$)** |
| *$B_0$ (`no_temporal`, referência)* | *64,20% (321)* | *65,38% (51)* | *57,14% (76)* | *54,14% (72)* | *-7 (+28/-35, $p=0{,}450$)* | *referência* |

---

## 2. Classificação Final: **ROBUSTO**

1. **Estabilidade Global dentro do Piso de Ruído:** Across todas as 5 configurações ($\lambda \in \{0{,}4; 0{,}6; 0{,}8\}$ e $\tau \in \{30\text{d}, 60\text{d}, 90\text{d}\}$), a acurácia global permaneceu na faixa estreita de **65,60% a 66,80%** (amplitude total de **1,20 p.p.**, inferior à própria variação de **1,60 p.p.** observada entre réplicas idênticas $B \times B'$). Nenhuma variação apresentou diferença estatisticamente significativa em relação a $B_{\text{ref}}$ ($p \ge 0{,}461$ em todos os casos).
2. **Estabilidade Causal em `knowledge-update`:** Em **100% das configurações testadas**, a acurácia em `knowledge-update` manteve-se entre **79,49% (62/78)** e **84,62% (66/78)**, com ganho altamente significativo sobre a ablação $B_0$ ($p \le 0{,}0034$ em todos os casos; 0 regressões em 4 das 5 configurações).
3. **Coerência com a Ablação Fatorial 2×2 (R08):** Atenuações mais suaves ($\lambda = 0{,}8$ ou $\tau = 90\text{d}$, que aproximam o sistema de `tags_only`) alcançaram `84,62%` em KU e `65,80%–66,80%` no geral, enquanto atenuações mais agressivas ($\lambda = 0{,}4$ ou $\tau = 30\text{d}$) ficaram em `79,49%` em KU. Isso confirma a conclusão de R08: no regime *oracle* (~9 fatos por grafo), o mecanismo principal é a sinalização explícita de vigência (`[CURRENT]`/`[HISTORICAL]`), e penalizações muito fortes em $\mathcal{V}$ não acrescentam ganho adicional.
4. **Conformidade Metodológica:** A configuração reportada no artigo permanece **$\lambda = 0{,}6$, $\tau = 60\text{d}$** (definida *a priori* antes dos experimentos), sem substituição por $\lambda = 0{,}8$.
