# Relatório de Replicação — HeLa-Mem Baseline (PILOT)

**Data da Execução:** 2026-09-27 14:26:12
**Commit Base:** `68f19b3fac8c6156570d5aeb3a7a3e8f3ba7cb04` (oficial)
**Dataset:** `external/HeLa-Mem/data/longmemeval_s.json`
**Itens Avaliados:** 0 (fatia [0:10])
**Tempo Total:** 99.9s (1.67 min)

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

### Acurácia Geral (Overall ACC): **0.00%**

| Categoria / Question Type | Total | Acertos | ACC (%) |
| :--- | :---: | :---: | :---: |

---

## 3. Comparação com a Meta do Artigo Oficial (500 itens)

| Categoria | Meta Paper (500 itens) | Obtido nesta execução |
| :--- | :---: | :---: |
| **Overall** | **65.40%** | **0.00%** |
| Temporal Reasoning | 50.38% | N/A% |
| Knowledge Update | 78.21% | N/A% |
| Multi-Session | 57.14% | N/A% |
| Single-Session User | 78.85% | N/A% |

> [!NOTE]
> Se esta foi uma execução piloto (subconjunto de itens), os números por categoria possuem maior variância estatística devido ao tamanho reduzido da amostra.
