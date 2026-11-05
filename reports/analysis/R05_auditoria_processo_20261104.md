# R05 — Auditoria do processo experimental frente às premissas do projeto

**Data da análise:** 2026-11-04
**Escopo:** todo o processo até o Draft 2 (commit `f05bfda`, 65,60% no LongMemEval-S)
**Script reprodutível:** [`src/analysis/audit_process.py`](../../src/analysis/audit_process.py), que não faz chamadas de API
**Plano de correção:** [`docs/plano_resolucao_R05.md`](../../docs/plano_resolucao_R05.md)

---

## 1. Objetivo

Verificar se o processo seguido respeita as premissas definidas em três documentos:

1. **Diretrizes da disciplina:** [`docs/projeto_diretrizes.md`](../../docs/projeto_diretrizes.md)
2. **Proposta do projeto:** [`docs/proposta_doc.md`](../../docs/proposta_doc.md), em especial: *"Os demais elementos do experimento serão mantidos constantes para permitir uma comparação controlada."*
3. **Regras de análise:** [`AGENT.MD`](../../AGENT.MD) (§8 causalidade, §11 estatística, §15 reprodutibilidade, §16 registro, §19 sensibilidade, §21 incerteza, §24 não otimizar para confirmar a hipótese)

Pergunta central: **os +4,40 p.p. de A → B podem ser atribuídos ao mecanismo de validade temporal?**

## 2. Dados utilizados

| Fonte | Conteúdo |
|---|---|
| `results/longmemeval_baseline_full/eval_results/eval_summary.json` | Baseline A: 500 itens, 306 acertos, parâmetros da execução |
| `results/longmemeval_temporal_full/eval_results/eval_summary.json` | Proposta B atual: 328 acertos |
| `git show d279613:results/.../eval_summary.json` | Proposta B, rodada anterior: 323 acertos |
| `results/temporal_encoded_500.zip` | Grafos de B: episódicos, semânticos e resultados por item, com datas |
| `results/baseline_episodic_500.zip` | Apenas os grafos **episódicos** de A. A memória semântica de A não foi versionada |
| `external/HeLa-Mem` @ `68f19b3` | Código e scripts oficiais |
| `reports/analysis/R03_*`, `R04_*`, `reports/relatorio_entrega2_draft2.md` | Registros anteriores |

Não há logs de codificação da Baseline A no repositório.

## 3. Achados

Níveis de certeza conforme o AGENT.MD §21.

### Achado 1 — A Baseline A não usou a configuração dos scripts oficiais
**Nível:** fato observado

A Baseline A foi executada chamando `hela_mem.eval_longmemeval` diretamente, sem `scripts/eval_longmemeval.sh`. Com isso valeram os valores padrão do código Python, que diferem do script em dois parâmetros:

| Parâmetro | Script oficial | Baseline A |
|---|:---:|:---:|
| `HEBBIAN_MAX_FLIPPED` | 3 | **5** |
| `HEBBIAN_KEYWORD_WEIGHT` | 0,7 | **0,5** |
| demais (lr, alpha, threshold, decay, tau, top_k, semantic_top_k) | iguais | iguais |

O script de codificação (`encode_longmemeval.sh`) também define `MAX_FLIPPED=3`. Não é possível saber se a codificação de A usou o script, porque não há logs.

**Consequências:**
- A frase "reprodução sem modificações" (R03, Draft 2) não se sustenta tal como está escrita.
- Os desvios podem explicar parte da diferença entre a reprodução (61,20%) e o artigo (65,40%). Isso é hipótese, não testada.
- **Na comparação A × B o desvio é neutro**, porque B reaproveita os grafos episódicos de A e roda com o mesmo ambiente.

### Achado 2 — Os 360 grafos semânticos vazios de A podem ser falha de execução
**Nível:** indício (não determinado)

O Draft 2 atribui os 360/500 grafos vazios ao buffer de 10 turnos que "misturava datas distintas". Há três razões para duvidar dessa explicação:

1. **O extrator oficial engole exceções.** Em `encode_longmemeval.py`, `process_incremental_buffer` envolve a extração em `try/except Exception: print(...)`. Uma falha em `add_knowledge` (embedding ou palavras-chave) não interrompe nada e só deixa o grafo vazio.
2. **O mesmo sintoma ocorreu na Proposta B** (Achado 3): 99 itens ficaram com grafo vazio por falha de execução. A correção foi aquecer o modelo de embedding na thread principal antes de abrir o `ThreadPoolExecutor`, o que indica uma condição de corrida no carregamento do `SentenceTransformer`. O código de A tem a mesma estrutura de threads.
3. **Misturar datas não produz grafos vazios.** Cada item do LongMemEval-S gera dezenas de chamadas de extração. Para o grafo ficar vazio, todas precisariam falhar ou devolver nada.

**Não foi possível confirmar**, porque a memória semântica de A (`*_long_term*.json`) e os logs de codificação não estão no repositório.

**Por que importa:** se a hipótese se confirmar, a baseline está subestimada, e parte do ganho A → B, possivelmente grande, viria de "a extração funcionar", e não de "a extração ser por sessão" nem do mecanismo temporal. A ablação B0 **não** resolve isso, porque B0 parte dos fatos extraídos por B.

### Achado 3 — A passagem de 64,60% para 65,60% veio da recodificação de 100 itens, e isso não está documentado
**Nível:** fato observado

| Verificação | Resultado |
|---|---|
| Itens recodificados em 2026-11-03 | 100, posições **100–199** do dataset |
| Tipos | 78 `knowledge-update` (todos os da categoria) + 22 `multi-session` |
| Situação na rodada antiga | 99 dos 100 com **0 fatos recuperados**: grafo vazio por falha de execução |
| Critério de seleção | Grafo semântico vazio (`len(nodes) == 0`). É objetivo e **independente de acerto** |
| Itens fora do lote que mudaram | **0** |
| Acertos nesses 100 itens | A: 66 · B antiga: 65 · B atual: 70 |
| `knowledge-update` (78) | A: 57 · B antiga: **57** · B atual: **65** |

**Avaliação:** o procedimento é legítimo. Corrigiu uma falha de execução com um critério que não depende do resultado, e nenhum item foi escolhido por estar errado. Mas o AGENT.MD §16 exige registro, e o Draft 2 não menciona que **todo o ganho em *knowledge-update*** veio dessa segunda rodada. O commit `d279613` apresenta 64,60% como "conclusão da avaliação dos 500 itens".

**Observação lateral (indício):** na rodada antiga, os 78 itens de KU rodaram com o prompt de B mas sem nenhum fato semântico, e acertaram exatamente o mesmo que A (57). Ou seja, o ganho em KU depende dos fatos semânticos, e não só das mudanças de prompt.

### Achado 4 — A comparação A × B tem fatores de confusão
**Nível:** fato observado (desenho experimental)

De A para B mudaram ao mesmo tempo:

1. o modo de extração (buffer de 10 turnos → por sessão, com timestamp da sessão);
2. o mecanismo temporal (validade, SUPERSEDES, 𝒱(f, t_query));
3. o prompt (tags CURRENT/HISTORICAL, instrução nova no system prompt);
4. a busca semântica (fórmula λ·Sim + (1−λ)·𝒱 em vez de `HebbianMemoryGraph.retrieve` com palavras-chave).

Isso viola a premissa da proposta ("demais elementos mantidos constantes") e o AGENT.MD §8. Há evidência de que parte do ganho não vem do mecanismo temporal: nas categorias de sessão única houve **0 supersessões** e mesmo assim o saldo foi **+6**.

**Status:** a ablação B0 foi implementada (branch `feat/ablacao-b0`, commit `176f3dc`) para separar o item 2+3 do item 1+4, mas ainda não foi executada.

### Achado 5 — Não há medida do ruído de amostragem
**Nível:** fato observado

`gpt_generate_answer_with_rotation` usa `temperature=0.7`, tanto na **geração** quanto no **juiz** (`hela_mem/utils.py`). Não há semente nem repetição. Os 86 pares discordantes entre A e B incluem ruído de valor desconhecido, e o McNemar trata cada execução como determinística.

### Achado 6 — Lacunas estatísticas
**Nível:** fato observado

- O McNemar global (p = 0,0115 unilateral) é adequado, mas faltam **intervalo de confiança** para a diferença e **tamanho de efeito**, como pede o §11.
- Ganhos por categoria são afirmados sem teste e sem correção para múltiplas comparações. Exemplo: "+20 p.p." em *preference* corresponde a +6 itens em n = 30.
- "Supera o artigo oficial" (65,60% contra 65,40%) é falsa precisão (§21), ainda mais com a baseline fora da configuração oficial.

### Achado 7 — Risco de ajuste no conjunto de teste
**Nível:** risco

- θ_sup = 0,35, λ = 0,6 e τ = 60 dias não têm justificativa registrada.
- O desenvolvimento usou itens do próprio conjunto de avaliação (`--target_ids 07741c44,07741c45`).
- A ablação planejada de λ ∈ {0,4; 0,6; 0,8} e τ ∈ {30, 60, 90} nos mesmos 500 itens só é válida como **análise de sensibilidade** (§19). Não pode ser usada para escolher a configuração reportada.

### Achado 8 — Diretriz de datasets não atendida
**Nível:** fato observado

As diretrizes pedem datasets diferentes, com dificuldades distintas e usados no artigo-base. Só o LongMemEval-S foi usado. O artigo-base também avalia em **LoCoMo**, com scripts prontos (`encode_locomo.sh`, `eval_locomo.sh`).

### Achado 9 — Reprodutibilidade e higiene
**Nível:** fato observado

- `requirements.txt` desatualizado: cabeçalho do projeto anterior (GraphSAGE/Reforma Tributária) e sem `openai` nem `python-dotenv`.
- `tests/` vazio.
- `eval_summary.json` de A registra o caminho `D:\Python Projetos\...` de outra máquina, sem descrever o ambiente.
- Memória semântica de A não versionada, o que impede auditar o Achado 2.
- Código e relatórios do GraphSAGE/PPI (R01, R02) misturados ao projeto atual (§25).

### Achado 10 — O arquivo `longmemeval_s.json` contém só as sessões de evidência
**Nível:** fato observado (adicionado em 2026-11-04, durante a revisão do Draft 2)

- Nos 500 itens de `external/HeLa-Mem/data/longmemeval_s.json`, `haystack_session_ids` é **igual** a `answer_session_ids`: o histórico tem apenas as sessões de evidência.
- Sessões por item: 1 a 6. A média é 1,0 nas categorias de sessão única e de 2,0 a 2,6 nas demais. O arquivo tem 15 MB.
- Segundo o artigo do LongMemEval (Wu et al., arXiv 2410.10813), o LongMemEval-S tem "approximately 115k tokens per problem" (cerca de 50 sessões, com as de evidência inseridas entre sessões de distração). O cenário *oracle* responde "with only the evidence sessions as the context".
- **Consequência:** o cenário avaliado equivale à variante *oracle*, que não testa encontrar o fato no meio de sessões de distração. Também explica a ausência de supersessão nas categorias de sessão única, que acontece por construção do método e não mede a precisão do classificador.

#### Atualização em 2026-11-05: o que dizem as fontes

Os três artigos foram lidos em arxiv.org. O README do LongMemEval no GitHub e o cartão do dataset no Hugging Face não puderam ser acessados.

| Fonte | O que afirma |
|---|---|
| HeLa-Mem, Apêndice D ([arXiv 2604.16839](https://arxiv.org/html/2604.16839)) | Avalia no "LongMemEval-S, a 500-item long-term conversational memory benchmark", com gpt-4o-mini como gerador e juiz. Não traz estatísticas do histórico (sessões ou tokens) nem menciona filtragem ou oracle. Os baselines das Tabelas 6 e 7 são "reported from Fang et al. (2025)". |
| LightMem (Fang et al., [arXiv 2510.18866](https://arxiv.org/html/2510.18866)), Apêndice D.1 | É a origem dos baselines (FullText 56,80; NaiveRAG 61,00; A-MEM 62,60). Usa "specifically the LongMemEval-S split", descrito com "approximately 115k tokens per problem". |
| LongMemEval ([arXiv 2410.10813](https://arxiv.org/html/2410.10813)), Fig. 3b | Mostra o tamanho da diferença: GPT-4o lendo o histórico inteiro acerta 87,0% no oracle e 60,6% no S. |
| README do HeLa-Mem (commit `68f19b3`) | "The complete `500`-item LongMemEval-S file is bundled in this repository", apontando para `data/longmemeval_s.json`. |
| Medição local do arquivo | 500 itens, 1 a 6 sessões (média 1,9), cerca de 26 mil caracteres (aprox. 6,6 mil tokens) por item. É cerca de 17 vezes menor que o LongMemEval-S. |

**Conclusão (fato observado):** o arquivo que o repositório oficial do HeLa-Mem apresenta como "o LongMemEval-S completo" para reproduzir os resultados corresponde, na verdade, à variante oracle. Os baselines que o artigo compara foram medidos pelo LightMem no LongMemEval-S de cerca de 115 mil tokens.

**Ainda indeterminado:** com qual arquivo o artigo obteve os 65,40%.
- **Se foi com o arquivo distribuído:** a Tabela 6 do artigo compara o HeLa-Mem no oracle com baselines medidos no S. A vantagem reportada sobre os baselines estaria inflada.
- **Se foi com o LongMemEval-S oficial:** o repositório distribui o arquivo errado, e a nossa reprodução (61,20%) e a Proposta B não são comparáveis aos 65,40%.

**Nos dois casos:**
1. Os resultados deste projeto devem ser descritos como "LongMemEval, 500 questões, histórico apenas de evidência (equivalente ao oracle)".
2. A comparação numérica com o artigo e com os baselines da Tabela 6 não é válida.
3. A comparação interna A → B0 → B continua válida, porque as três condições usam o mesmo arquivo.

**Como fechar a questão:** abrir uma issue no repositório do HeLa-Mem perguntando qual arquivo gerou as Tabelas 6 e 7 (Etapa 8b do plano) e, se houver orçamento, rodar no LongMemEval-S oficial.

## 4. Pontos atendidos

| Premissa | Evidência |
|---|---|
| Bom artigo com código oficial | HeLa-Mem (ACL 2026), commit fixado |
| Entendimento do código | Auditoria encontrou bugs reais (decaimento neutralizado, timestamp de execução) |
| Reproduzir antes de modificar | R03 em 29/09, modificações em 02/11 |
| Hipótese clara e justificada | Validade temporal × recência, inspirada no Zep/Graphiti |
| Mesmas métricas do artigo | Juiz LongMemEval pelo código oficial |
| Métricas salvas em arquivo | JSON por item e resumos versionados |
| Controle da memória episódica | B reaproveita os mesmos 500 grafos episódicos de A |
| Análise de resultados negativos (§20) | 32 regressões analisadas com casos concretos |
| Análise qualitativa | Estudos de caso com nós reais dos grafos |

## 5. Conclusão

| Pergunta | Resposta | Certeza |
|---|---|---|
| B é melhor que A, como executado? | Sim, +22 itens (p = 0,0115) | Evidência moderada (ruído não medido) |
| O ganho se deve ao mecanismo temporal? | **Não determinado** | Fatores de confusão (Achados 2 e 4) |
| A baseline é uma reprodução fiel do HeLa-Mem? | **Não** | Fato (Achado 1); possível falha de execução (Achado 2) |
| B supera o artigo original? | Não é possível afirmar | Diferença de 0,2 p.p., baseline não fiel |

Hoje o processo sustenta a afirmação **"o pipeline B supera o pipeline A tal como foi executado"**. Ainda **não** sustenta a afirmação central da proposta: "a validade temporal melhora uma memória associativa hebbiana". Os passos em [`docs/plano_resolucao_R05.md`](../../docs/plano_resolucao_R05.md) separam essas duas coisas.

## 6. Decisões tomadas nesta análise

- Ablação B0 implementada e versionada na branch `feat/ablacao-b0` (sem execução).
- Script `audit_process.py` criado para que os Achados 1 e 3 sejam reproduzíveis.
- Nenhum resultado existente foi alterado.

## 7. Questões em aberto

1. Por que 360/500 grafos semânticos de A ficaram vazios? Ainda existem os arquivos `*_long_term*.json` e os logs da codificação de A (máquina `D:\` ou Colab)?
2. Qual o tamanho do ruído entre execuções (B contra B')?
3. Quanto do ganho sobra em B0 → B?
4. Os resultados se mantêm no LoCoMo?
