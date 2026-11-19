# Relatório Experimental — PROPOSTA B (Validade Temporal)

**Data da Execução:** 2026-11-19 11:15:00
**Amostra:** 500 itens (fatia [0:500])
**Diretório:** `D:\Python Projetos\mestrado-dl-projeto\results\longmemeval_temporal_full` (resultados em `eval_results_l04/`)
**Ablação:** `none`
**Tempo de Execução:**
- Encoding: 0.0s (0.00 min)
- Evaluation: 338.6s (5.64 min)
- Total: 338.6s (5.64 min)
- Ritmo médio por item: 0.68s/item
- Projeção para 500 itens: 5.6 minutos

---

## Resultados Consolidados — PROPOSTA B (Validade Temporal)

**Acurácia Geral:** **65.60%** (328/500)

| Categoria / Question Type | Total | Acertos | ACC (%) |
| :--- | :---: | :---: | :---: |
| `knowledge-update` | 78 | 62 | **79.49%** |
| `multi-session` | 133 | 67 | **50.38%** |
| `single-session-assistant` | 56 | 51 | **91.07%** |
| `single-session-preference` | 30 | 12 | **40.00%** |
| `single-session-user` | 70 | 61 | **87.14%** |
| `temporal-reasoning` | 133 | 75 | **56.39%** |

---

## Comparação A/B Pareada com Baseline A

- **Ganhos (Erro -> Acerto):** +51
- **Regressões (Acerto -> Erro):** -29
- **Saldo Líquido:** +22 acertos
- **Mantidos Corretos:** 277
- **Mantidos Errados:** 143