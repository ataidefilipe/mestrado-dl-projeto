# Relatório Experimental — PROPOSTA B (Validade Temporal)

**Data da Execução:** 2026-11-05 10:17:21
**Amostra:** 500 itens (fatia [0:500])
**Diretório:** `results/longmemeval_temporal_v2` (resultados em `eval_results/`)
**Ablação:** `none`
**Tempo de Execução:**
- Encoding: 3438.3s (57.30 min)
- Evaluation: 389.3s (6.49 min)
- Total: 3827.6s (63.79 min)
- Ritmo médio por item: 7.66s/item
- Projeção para 500 itens: 63.8 minutos

---

## Resultados Consolidados — PROPOSTA B (Validade Temporal)

**Acurácia Geral:** **64.80%** (324/500)

| Categoria / Question Type | Total | Acertos | ACC (%) |
| :--- | :---: | :---: | :---: |
| `knowledge-update` | 78 | 62 | **79.49%** |
| `multi-session` | 133 | 68 | **51.13%** |
| `single-session-assistant` | 56 | 49 | **87.50%** |
| `single-session-preference` | 30 | 12 | **40.00%** |
| `single-session-user` | 70 | 56 | **80.00%** |
| `temporal-reasoning` | 133 | 77 | **57.89%** |

---

## Comparação A/B Pareada com Baseline A

- **Ganhos (Erro -> Acerto):** +48
- **Regressões (Acerto -> Erro):** -30
- **Saldo Líquido:** +18 acertos
- **Mantidos Corretos:** 276
- **Mantidos Errados:** 146