# Relatório Experimental — ABLACAO B0 (no_temporal)

**Data da Execução:** 2026-11-04 20:56:35
**Amostra:** 500 itens (fatia [0:500])
**Diretório:** `D:\Python Projetos\mestrado-dl-projeto\results\longmemeval_temporal_full` (resultados em `eval_results_b0/`)
**Ablação:** `no_temporal`
**Tempo de Execução:**
- Encoding: 0.0s (0.00 min)
- Evaluation: 350.9s (5.85 min)
- Total: 350.9s (5.85 min)
- Ritmo médio por item: 0.70s/item
- Projeção para 500 itens: 5.8 minutos

---

## Resultados Consolidados — ABLACAO B0 (no_temporal)

**Acurácia Geral:** **64.20%** (321/500)

| Categoria / Question Type | Total | Acertos | ACC (%) |
| :--- | :---: | :---: | :---: |
| `knowledge-update` | 78 | 51 | **65.38%** |
| `multi-session` | 133 | 72 | **54.14%** |
| `single-session-assistant` | 56 | 50 | **89.29%** |
| `single-session-preference` | 30 | 12 | **40.00%** |
| `single-session-user` | 70 | 60 | **85.71%** |
| `temporal-reasoning` | 133 | 76 | **57.14%** |

---

## Comparação A/B Pareada com Baseline A

- **Ganhos (Erro -> Acerto):** +47
- **Regressões (Acerto -> Erro):** -32
- **Saldo Líquido:** +15 acertos
- **Mantidos Corretos:** 274
- **Mantidos Errados:** 147