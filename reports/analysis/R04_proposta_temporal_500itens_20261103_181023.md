# Relatório Experimental — Proposta B (Validade Temporal)

**Data da Execução:** 2026-11-03 18:10:23
**Amostra:** 500 itens (fatia [0:500])
**Diretório:** `results/longmemeval_temporal_full`
**Tempo de Execução:**
- Encoding: 405.9s (6.77 min)
- Evaluation: 49.7s (0.83 min)
- Total: 455.6s (7.59 min)
- Ritmo médio por item: 0.91s/item
- Projeção para 500 itens: 7.6 minutos

---

## Resultados Consolidados da Proposta B

**Acurácia Geral:** **65.60%** (328/500)

| Categoria / Question Type | Total | Acertos | ACC (%) |
| :--- | :---: | :---: | :---: |
| `knowledge-update` | 78 | 65 | **83.33%** |
| `multi-session` | 133 | 65 | **48.87%** |
| `single-session-assistant` | 56 | 52 | **92.86%** |
| `single-session-preference` | 30 | 14 | **46.67%** |
| `single-session-user` | 70 | 58 | **82.86%** |
| `temporal-reasoning` | 133 | 74 | **55.64%** |

---

## Comparação A/B Pareada com Baseline A

- **Ganhos (Erro -> Acerto):** +54
- **Regressões (Acerto -> Erro):** -32
- **Saldo Líquido:** +22 acertos
- **Mantidos Corretos:** 274
- **Mantidos Errados:** 140