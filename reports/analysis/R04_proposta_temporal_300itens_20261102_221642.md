# Relatório Experimental — Proposta B (Validade Temporal)

**Data da Execução:** 2026-11-02 22:16:42
**Amostra:** 300 itens (fatia [0:300])
**Diretório:** `results/longmemeval_temporal_full`
**Tempo de Execução:**
- Encoding: 110.3s (1.84 min)
- Evaluation: 62.9s (1.05 min)
- Total: 173.1s (2.89 min)
- Ritmo médio por item: 0.58s/item
- Projeção para 500 itens: 4.8 minutos

---

## Resultados Consolidados da Proposta B

**Acurácia Geral:** **61.00%** (183/300)

| Categoria / Question Type | Total | Acertos | ACC (%) |
| :--- | :---: | :---: | :---: |
| `knowledge-update` | 78 | 57 | **73.08%** |
| `multi-session` | 62 | 20 | **32.26%** |
| `single-session-assistant` | 56 | 52 | **92.86%** |
| `single-session-preference` | 30 | 14 | **46.67%** |
| `single-session-user` | 14 | 10 | **71.43%** |
| `temporal-reasoning` | 60 | 30 | **50.00%** |

---

## Comparação A/B Pareada com Baseline A

- **Ganhos (Erro -> Acerto):** +30
- **Regressões (Acerto -> Erro):** -15
- **Saldo Líquido:** +15 acertos
- **Mantidos Corretos:** 153
- **Mantidos Errados:** 102