# Relatório Experimental — PROPOSTA B (Validade Temporal)

**Data da Execução:** 2026-11-05 10:40:03
**Amostra:** 500 itens (fatia [0:500])
**Diretório:** `results/longmemeval_temporal_full` (resultados em `eval_results_b_rerun/`)
**Ablação:** `none`
**Tempo de Execução:**
- Encoding: 0.0s (0.00 min)
- Evaluation: 17.2s (0.29 min)
- Total: 17.2s (0.29 min)
- Ritmo médio por item: 0.03s/item
- Projeção para 500 itens: 0.3 minutos

---

## Resultados Consolidados — PROPOSTA B (Validade Temporal)

**Acurácia Geral:** **64.00%** (320/500)

| Categoria / Question Type | Total | Acertos | ACC (%) |
| :--- | :---: | :---: | :---: |
| `knowledge-update` | 78 | 65 | **83.33%** |
| `multi-session` | 133 | 67 | **50.38%** |
| `single-session-assistant` | 56 | 50 | **89.29%** |
| `single-session-preference` | 30 | 10 | **33.33%** |
| `single-session-user` | 70 | 60 | **85.71%** |
| `temporal-reasoning` | 133 | 68 | **51.13%** |

---

## Comparação A/B Pareada com Baseline A

- **Ganhos (Erro -> Acerto):** +43
- **Regressões (Acerto -> Erro):** -29
- **Saldo Líquido:** +14 acertos
- **Mantidos Corretos:** 277
- **Mantidos Errados:** 151