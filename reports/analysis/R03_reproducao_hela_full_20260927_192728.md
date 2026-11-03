# Relatório de Replicação — HeLa-Mem Baseline (FULL)

**Data da Execução:** 2026-09-27 19:27:28
**Commit Base:** `68f19b3fac8c6156570d5aeb3a7a3e8f3ba7cb04` (oficial)
**Dataset:** `external/HeLa-Mem/data/longmemeval_s.json`
**Itens Avaliados:** 500 (acertos: 14, fatia [0:500])
**Tempo Total:** 17776.5s (296.27 min)

---

## 1. Parâmetros de Execução

```json
{
  "top_k": 15,
  "semantic_top_k": 5,
  "use_consolidation": false,
  "max_flipped": "5",
  "learning_rate": "0.02",
  "activation_alpha": "0.1",
  "spreading_threshold": "0.4",
  "decay_rate": "0.995",
  "keyword_weight": "0.5",
  "tau": "1e7"
}
```

---

## 2. Resultados Consolidados

### Acurácia Geral (Overall ACC): **2.80%** (14/500)

| Categoria / Question Type | Total | Acertos | ACC (%) |
| :--- | :---: | :---: | :---: |
| `knowledge-update` | 78 | 2 | **2.56%** |
| `multi-session` | 133 | 4 | **3.01%** |
| `single-session-assistant` | 56 | 3 | **5.36%** |
| `single-session-preference` | 30 | 0 | **0.00%** |
| `single-session-user` | 70 | 4 | **5.71%** |
| `temporal-reasoning` | 133 | 1 | **0.75%** |

---

## 3. Comparação com a Meta do Artigo Oficial (500 itens)

| Categoria | Meta Paper (500 itens) | Obtido nesta execução |
| :--- | :---: | :---: |
| **Overall** | **65.40%** | **2.80%** |
| Temporal Reasoning | 50.38% | 0.7518796992481203% |
| Knowledge Update | 78.21% | 2.564102564102564% |
| Multi-Session | 57.14% | 3.007518796992481% |
| Single-Session User | 78.85% | 5.714285714285714% |

> [!NOTE]
> Esta execução foi um teste piloto de sanity check (10 itens). Os números por categoria possuem maior variância estatística devido ao tamanho reduzido da amostra e servem para validar a integridade do pipeline de ponta a ponta.
