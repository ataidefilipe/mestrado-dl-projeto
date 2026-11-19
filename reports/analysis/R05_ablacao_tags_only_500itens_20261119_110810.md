# Relatório Experimental — ABLACAO (tags_only)

**Data da Execução:** 2026-11-19 11:08:10
**Amostra:** 500 itens (fatia [0:500])
**Diretório:** `D:\Python Projetos\mestrado-dl-projeto\results\longmemeval_temporal_full` (resultados em `eval_results_tags_only/`)
**Ablação:** `tags_only`
**Tempo de Execução:**
- Encoding: 0.0s (0.00 min)
- Evaluation: 393.5s (6.56 min)
- Total: 393.5s (6.56 min)
- Ritmo médio por item: 0.79s/item
- Projeção para 500 itens: 6.6 minutos

---

## Resultados Consolidados — ABLACAO (tags_only)

**Acurácia Geral:** **66.20%** (331/500)

| Categoria / Question Type | Total | Acertos | ACC (%) |
| :--- | :---: | :---: | :---: |
| `knowledge-update` | 78 | 67 | **85.90%** |
| `multi-session` | 133 | 68 | **51.13%** |
| `single-session-assistant` | 56 | 51 | **91.07%** |
| `single-session-preference` | 30 | 11 | **36.67%** |
| `single-session-user` | 70 | 59 | **84.29%** |
| `temporal-reasoning` | 133 | 75 | **56.39%** |

---

## Comparação A/B Pareada com Baseline A

- **Ganhos (Erro -> Acerto):** +55
- **Regressões (Acerto -> Erro):** -30
- **Saldo Líquido:** +25 acertos
- **Mantidos Corretos:** 276
- **Mantidos Errados:** 139