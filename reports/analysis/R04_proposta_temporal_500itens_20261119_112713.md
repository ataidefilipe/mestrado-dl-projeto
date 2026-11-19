# Relatório Experimental — PROPOSTA B (Validade Temporal)

**Data da Execução:** 2026-11-19 11:27:13
**Amostra:** 500 itens (fatia [0:500])
**Diretório:** `D:\Python Projetos\mestrado-dl-projeto\results\longmemeval_temporal_full` (resultados em `eval_results_tau30/`)
**Ablação:** `none`
**Tempo de Execução:**
- Encoding: 0.0s (0.00 min)
- Evaluation: 347.9s (5.80 min)
- Total: 347.9s (5.80 min)
- Ritmo médio por item: 0.70s/item
- Projeção para 500 itens: 5.8 minutos

---

## Resultados Consolidados — PROPOSTA B (Validade Temporal)

**Acurácia Geral:** **66.20%** (331/500)

| Categoria / Question Type | Total | Acertos | ACC (%) |
| :--- | :---: | :---: | :---: |
| `knowledge-update` | 78 | 62 | **79.49%** |
| `multi-session` | 133 | 66 | **49.62%** |
| `single-session-assistant` | 56 | 51 | **91.07%** |
| `single-session-preference` | 30 | 14 | **46.67%** |
| `single-session-user` | 70 | 60 | **85.71%** |
| `temporal-reasoning` | 133 | 78 | **58.65%** |

---

## Comparação A/B Pareada com Baseline A

- **Ganhos (Erro -> Acerto):** +56
- **Regressões (Acerto -> Erro):** -31
- **Saldo Líquido:** +25 acertos
- **Mantidos Corretos:** 275
- **Mantidos Errados:** 138