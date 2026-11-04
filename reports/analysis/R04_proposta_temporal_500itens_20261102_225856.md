# Relatório Experimental — Proposta B (Validade Temporal)

**Data da Execução:** 2026-11-02 22:58:56
**Amostra:** 500 itens (fatia [0:500])
**Diretório:** `results/longmemeval_temporal_full`
**Tempo de Execução:**
- Encoding: 494.6s (8.24 min)
- Evaluation: 65.1s (1.09 min)
- Total: 559.7s (9.33 min)
- Ritmo médio por item: 1.12s/item
- Projeção para 500 itens: 9.3 minutos

---

## Resultados Consolidados da Proposta B

**Acurácia Geral:** **64.60%** (323/500)

| Categoria / Question Type | Total | Acertos | ACC (%) |
| :--- | :---: | :---: | :---: |
| `knowledge-update` | 78 | 57 | **73.08%** |
| `multi-session` | 133 | 68 | **51.13%** |
| `single-session-assistant` | 56 | 52 | **92.86%** |
| `single-session-preference` | 30 | 14 | **46.67%** |
| `single-session-user` | 70 | 58 | **82.86%** |
| `temporal-reasoning` | 133 | 74 | **55.64%** |

---

## Comparação A/B Pareada com Baseline A

- **Ganhos (Erro -> Acerto):** +47
- **Regressões (Acerto -> Erro):** -30
- **Saldo Líquido:** +17 acertos
- **Mantidos Corretos:** 276
- **Mantidos Errados:** 147