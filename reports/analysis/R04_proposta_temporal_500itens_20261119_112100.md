# Relatório Experimental — PROPOSTA B (Validade Temporal)

**Data da Execução:** 2026-11-19 11:21:00
**Amostra:** 500 itens (fatia [0:500])
**Diretório:** `D:\Python Projetos\mestrado-dl-projeto\results\longmemeval_temporal_full` (resultados em `eval_results_l08/`)
**Ablação:** `none`
**Tempo de Execução:**
- Encoding: 0.0s (0.00 min)
- Evaluation: 336.0s (5.60 min)
- Total: 336.0s (5.60 min)
- Ritmo médio por item: 0.67s/item
- Projeção para 500 itens: 5.6 minutos

---

## Resultados Consolidados — PROPOSTA B (Validade Temporal)

**Acurácia Geral:** **66.80%** (334/500)

| Categoria / Question Type | Total | Acertos | ACC (%) |
| :--- | :---: | :---: | :---: |
| `knowledge-update` | 78 | 66 | **84.62%** |
| `multi-session` | 133 | 68 | **51.13%** |
| `single-session-assistant` | 56 | 52 | **92.86%** |
| `single-session-preference` | 30 | 12 | **40.00%** |
| `single-session-user` | 70 | 59 | **84.29%** |
| `temporal-reasoning` | 133 | 77 | **57.89%** |

---

## Comparação A/B Pareada com Baseline A

- **Ganhos (Erro -> Acerto):** +56
- **Regressões (Acerto -> Erro):** -28
- **Saldo Líquido:** +28 acertos
- **Mantidos Corretos:** 278
- **Mantidos Errados:** 138