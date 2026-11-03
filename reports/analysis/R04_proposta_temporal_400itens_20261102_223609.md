# Relatório Experimental — Proposta B (Validade Temporal)

**Data da Execução:** 2026-11-02 22:36:09
**Amostra:** 400 itens (fatia [0:400])
**Diretório:** `results/longmemeval_temporal_full`
**Tempo de Execução:**
- Encoding: 410.5s (6.84 min)
- Evaluation: 59.1s (0.99 min)
- Total: 469.6s (7.83 min)
- Ritmo médio por item: 1.17s/item
- Projeção para 500 itens: 9.8 minutos

---

## Resultados Consolidados da Proposta B

**Acurácia Geral:** **63.75%** (255/400)

| Categoria / Question Type | Total | Acertos | ACC (%) |
| :--- | :---: | :---: | :---: |
| `knowledge-update` | 78 | 57 | **73.08%** |
| `multi-session` | 62 | 20 | **32.26%** |
| `single-session-assistant` | 56 | 52 | **92.86%** |
| `single-session-preference` | 30 | 14 | **46.67%** |
| `single-session-user` | 70 | 58 | **82.86%** |
| `temporal-reasoning` | 104 | 54 | **51.92%** |

---

## Comparação A/B Pareada com Baseline A

- **Ganhos (Erro -> Acerto):** +38
- **Regressões (Acerto -> Erro):** -23
- **Saldo Líquido:** +15 acertos
- **Mantidos Corretos:** 217
- **Mantidos Errados:** 122