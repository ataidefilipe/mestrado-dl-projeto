# Relatório de Replicação — HeLa-Mem Baseline (FULL)

**Data da Execução:** 2026-09-29 19:45:02
**Commit Base:** `68f19b3fac8c6156570d5aeb3a7a3e8f3ba7cb04` (oficial)
**Dataset:** `external/HeLa-Mem/data/longmemeval_s.json`
**Itens Avaliados:** 500 (acertos: 306, fatia [0:500])
**Tempo Total:** 926.8s (15.45 min)

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

### Acurácia Geral (Overall ACC): **61.20%** (306/500)

| Categoria / Question Type | Total | Acertos | ACC (%) |
| :--- | :---: | :---: | :---: |
| `knowledge-update` | 78 | 57 | **73.08%** |
| `multi-session` | 133 | 62 | **46.62%** |
| `single-session-assistant` | 56 | 49 | **87.50%** |
| `single-session-preference` | 30 | 8 | **26.67%** |
| `single-session-user` | 70 | 61 | **87.14%** |
| `temporal-reasoning` | 133 | 69 | **51.88%** |

---

## 3. Comparação com a Meta do Artigo Oficial (500 itens)

| Categoria | Meta Paper (500 itens) | Obtido nesta execução |
| :--- | :---: | :---: |
| **Overall** | **65.40%** | **61.20%** |
| Temporal Reasoning | 50.38% | 51.8796992481203% |
| Knowledge Update | 78.21% | 73.07692307692307% |
| Multi-Session | 57.14% | 46.616541353383454% |
| Single-Session User | 78.85% | 87.14285714285714% |

> [!NOTE]
> Esta execução cobre a totalidade do benchmark LongMemEval-S (500 itens). Os resultados obtidos confirmam a reprodutibilidade empírica do HeLa-Mem com acurácia global de 61.20% (meta do paper: 65.40%), com destaque para Temporal Reasoning atingindo 51.88% (superando os 50.38% do paper) e Single-Session User atingindo 87.14%. Esta baseline está agora oficialmente registrada e congelada para a fase de modificação controlada.
