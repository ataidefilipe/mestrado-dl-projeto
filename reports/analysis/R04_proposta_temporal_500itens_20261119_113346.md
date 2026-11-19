# Relatório Experimental — PROPOSTA B (Validade Temporal)

**Data da Execução:** 2026-11-19 11:33:46
**Amostra:** 500 itens (fatia [0:500])
**Diretório:** `D:\Python Projetos\mestrado-dl-projeto\results\longmemeval_temporal_full` (resultados em `eval_results_tau90/`)
**Ablação:** `none`
**Tempo de Execução:**
- Encoding: 0.0s (0.00 min)
- Evaluation: 361.4s (6.02 min)
- Total: 361.4s (6.02 min)
- Ritmo médio por item: 0.72s/item
- Projeção para 500 itens: 6.0 minutos

---

## Resultados Consolidados — PROPOSTA B (Validade Temporal)

**Acurácia Geral:** **65.80%** (329/500)

| Categoria / Question Type | Total | Acertos | ACC (%) |
| :--- | :---: | :---: | :---: |
| `knowledge-update` | 78 | 66 | **84.62%** |
| `multi-session` | 133 | 69 | **51.88%** |
| `single-session-assistant` | 56 | 50 | **89.29%** |
| `single-session-preference` | 30 | 15 | **50.00%** |
| `single-session-user` | 70 | 58 | **82.86%** |
| `temporal-reasoning` | 133 | 71 | **53.38%** |

---

## Comparação A/B Pareada com Baseline A

- **Ganhos (Erro -> Acerto):** +50
- **Regressões (Acerto -> Erro):** -27
- **Saldo Líquido:** +23 acertos
- **Mantidos Corretos:** 279
- **Mantidos Errados:** 144