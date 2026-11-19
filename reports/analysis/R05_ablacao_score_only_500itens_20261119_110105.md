# Relatório Experimental — ABLACAO (score_only)

**Data da Execução:** 2026-11-19 11:01:05
**Amostra:** 500 itens (fatia [0:500])
**Diretório:** `D:\Python Projetos\mestrado-dl-projeto\results\longmemeval_temporal_full` (resultados em `eval_results_score_only/`)
**Ablação:** `score_only`
**Tempo de Execução:**
- Encoding: 0.0s (0.00 min)
- Evaluation: 365.2s (6.09 min)
- Total: 365.2s (6.09 min)
- Ritmo médio por item: 0.73s/item
- Projeção para 500 itens: 6.1 minutos

---

## Resultados Consolidados — ABLACAO (score_only)

**Acurácia Geral:** **61.80%** (309/500)

| Categoria / Question Type | Total | Acertos | ACC (%) |
| :--- | :---: | :---: | :---: |
| `knowledge-update` | 78 | 51 | **65.38%** |
| `multi-session` | 133 | 68 | **51.13%** |
| `single-session-assistant` | 56 | 51 | **91.07%** |
| `single-session-preference` | 30 | 9 | **30.00%** |
| `single-session-user` | 70 | 59 | **84.29%** |
| `temporal-reasoning` | 133 | 71 | **53.38%** |

---

## Comparação A/B Pareada com Baseline A

- **Ganhos (Erro -> Acerto):** +37
- **Regressões (Acerto -> Erro):** -34
- **Saldo Líquido:** +3 acertos
- **Mantidos Corretos:** 272
- **Mantidos Errados:** 157