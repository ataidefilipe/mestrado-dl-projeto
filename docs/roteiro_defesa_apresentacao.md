# Roteiro de Defesa e Apresentação — Validade Temporal e Supersessão de Fatos em Memória Associativa Hebbiana para Agentes Baseados em LLM

**Autor:** Filipe Augusto de Ataíde Barbosa (`faab@cin.ufpe.br`)  
**Disciplina:** Deep Learning — Mestrado CIn/UFPE (Prof. Cleber Zanchettin)  
**Artigo-Base:** *HeLa-Mem: Hebbian Learning and Associative Memory for LLM Agents* (ACL 2026, commit `68f19b3`)  
**Inspiração Conceitual:** *Zep / Graphiti: A Temporal Knowledge Graph Architecture for Agent Memory* (2025)  
**Artigo Final:** [`reports/relatorio_final_ieee.tex`](../reports/relatorio_final_ieee.tex) | [`reports/relatorio_final.md`](../reports/relatorio_final.md)

---

## 1. Estrutura Recomendada de Slides (12 a 15 minutos)

### Slide 1 — Título e Pergunta de Pesquisa (1 min)
- **Título:** Validade Temporal e Supersessão de Fatos em Memória Associativa Hebbiana para Agentes Baseados em LLM.
- **Contexto:** Agentes conversacionais de longo prazo acumulam fatos que mudam ao longo do tempo (endereço, seguidores, metas, preferências, localização de objetos).
- **Pergunta Central:** *A representação explícita da validade temporal e da supersessão de fatos melhora uma memória associativa hebbiana em tarefas de atualização de conhecimento e raciocínio temporal, quando comparada ao mecanismo original?*
- **Fio Condutor Metodológico:** Reprodução estrita $\rightarrow$ Auditoria de processo $\rightarrow$ Isolamento causal (ablações) $\rightarrow$ Medição de ruído $\rightarrow$ Generalização ontológica e Sensibilidade.

---

### Slide 2 — O Problema: Recência $\neq$ Saliência $\neq$ Validade (1,5 min)
- **O que o HeLa-Mem (ACL 2026) faz bem:**
  - Grafo episódico e semântico com **aprendizado hebbiano** ($\Delta w_{ij} = \eta$ quando nós são coativados) e **ativação espalhada** (*spreading activation*), excelente para recuperação associativa *multi-hop*.
- **O que o HeLa-Mem não modela:**
  - Trata fatos semânticos extraídos como estáticos (`metadata = {"type": "fact"}`).
  - **Exemplo real (`a2f3aa27`):**
    - Sessão 1 (01:28): *"User has 1250 followers on Instagram."*
    - Sessão 2 (19:16): *"User has 1300 followers on Instagram."*
  - Ambos têm alta similaridade de cosseno com a pergunta *"How many followers do I have?"*. Sem validade temporal, o fato obsoleto compete em pé de igualdade com o fato vigente.

---

### Slide 3 — Diagnóstico Técnico do Código Oficial do HeLa-Mem (1 min)
Durante a inspeção do código oficial (`commit 68f19b3`), identificamos **3 falhas/limitações estruturais**:
1. **Perda da data do evento na memória semântica:** `add_knowledge(fact)` grava o horário de execução do script (`get_timestamp()`) em vez da data da sessão (`haystack_dates`).
2. **Decaimento temporal neutralizado por bug silencioso:** `retrieve()` chama `compute_time_decay(node["timestamp"], current_time)` passando uma **string** no lugar do escalar $\tau$; a função captura a exceção e retorna `1.0` silenciosamente.
3. **Omissão de $t_{\text{query}}$ no retrieval:** A data da pergunta (`question_date`) é enviada ao prompt final do LLM, mas **não é passada ao retriever**.

---

### Slide 4 — Arquitetura Proposta: `TemporalKnowledgeMemory` + `ValidityAwareRetriever` (2 min)
*(Usar Figura 1: [`reports/figures/fig1_arquitetura_proposta.png`](../reports/figures/fig1_arquitetura_proposta.png) e Figura 5: [`reports/figures/fig5_decaimento_pertinencia.png`](../reports/figures/fig5_decaimento_pertinencia.png))*

1. **Representação Formal do Fato Semântico:**
   $$f_i = \langle c_i, \mathbf{e}_i, [t_{\text{start}}^{(i)}, t_{\text{end}}^{(i)}], \mathcal{S}_i, \mathbf{w}_i \rangle$$
2. **Supersessão Não-Destrutiva na Ingestão ($\theta_{\text{sup}} = 0{,}35$):**
   - Compara novo fato $f_{\text{new}}$ (em $t_{\text{event}}$) com até 4 candidatos ativos de sessões anteriores.
   - Classificador LLM decide entre `UNRELATED`, `EXTENDS` (reforça aresta $+\eta$) e `SUPERSEDES` (fecha $t_{\text{end}}^{(\text{cand})} \leftarrow t_{\text{event}}$, marca como `superseded` e cria aresta bidirecional $w = 0{,}8$).
3. **Pertinência Temporal Consciente da Consulta $\mathcal{V}(f_i, t_{\text{query}})$:**
   $$\mathcal{V}(f_i, t_{\text{query}}) = \begin{cases} 1, & t_{\text{start}}^{(i)} \le t_{\text{query}} \le t_{\text{end}}^{(i)} \\ \exp\left(-\frac{t_{\text{query}} - t_{\text{end}}^{(i)}}{\tau_{\text{decay}}}\right), & t_{\text{query}} > t_{\text{end}}^{(i)} \\ 0, & t_{\text{query}} < t_{\text{start}}^{(i)} \end{cases}$$
4. **Sinalização Explícita no Prompt:**
   - Etiquetas `[CURRENT / ACTIVE (Valid since: ...)]` vs. `[HISTORICAL / SUPERSEDED (Valid: ... to ...)]`.

---

### Slide 5 — Rigor Metodológico: Da Reprodução Inicial ($A$) à Baseline Fiel ($A^*$) (1,5 min)
- **Primeira Reprodução ($A$ = 61,20%):**
  - Ao auditar os artefatos ([`R05`](../reports/analysis/R05_auditoria_processo_20261104.md)), descobrimos que **360 dos 500 grafos semânticos estavam vazios** e que a chamada direta via Python usou `MAX_FLIPPED=5` e `KEYWORD_WEIGHT=0.5` (contra `3` e `0.7` nos scripts `.sh`).
- **Diagnóstico Empírico ([`R06`](../reports/analysis/R06_diagnostico_baseline_e_ruido_Bprime_Bv2_20261105.md)):**
  - O extrator oficial do HeLa-Mem engole exceções em `try/except`. Sob multithreading no Windows, condições de corrida descartaram 72% dos grafos semânticos. Rodando com `workers=1`, o item 400 extraiu 9 fatos nominais.
- **Baseline Fiel ($A^*$ = 63,40% — [`R03_reproducao_hela_fiel_500itens.md`](../reports/analysis/R03_reproducao_hela_fiel_500itens.md)):**
  - Reexecutada com `workers=2` e parâmetros estritos dos scripts oficiais: **500/500 grafos íntegros (4.978 fatos)**.
  - Em `multi-session`, a acurácia saltou de `46,62%` ($A$) para **`57,14%` (76/133)** — **coincidência matemática exata** com os `57,14%` reportados na Tabela 6 do paper ACL 2026.

---

### Slide 6 — Resultados Principais e o Fenômeno da Interferência Factual (2 min)
*(Usar Figura 2: [`reports/figures/fig2_baseline_vs_paper.png`](../reports/figures/fig2_baseline_vs_paper.png) e Figura 3: [`reports/figures/fig3_analise_pareada_ab.png`](../reports/figures/fig3_analise_pareada_ab.png))*

| Categoria (`question_type`) | $N$ | Baseline $A$ (72% vazios) | Baseline Fiel $A^*$ (0% vazios) | Ablação $B_0$ (Sem tempo) | Proposta $B$ ($\mathcal{V}$ + Tags) | Proposta $B_{\text{v2}}$ (*Event Calc.*) | `tags_only` (Só Tags) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **`knowledge-update` (KU)** | **78** | 73,08% (57) | **67,95% (53)** | **65,38% (51)** | **83,33% (65)*** | **79,49% (62)*** | **85,90% (67)*** |
| `temporal-reasoning` (TR) | 133 | 51,88% (69) | 53,38% (71) | 57,14% (76) | 55,64% (74) | **57,89% (77)** | 56,39% (75) |
| `multi-session` (MS) | 133 | 46,62% (62) | **57,14% (76)** | 54,14% (72) | 48,87% (65) | 51,13% (68) | 51,13% (68) |
| Categorias *single-session* | 156 | 75,64% (118) | 75,00% (117) | 78,21% (122) | **79,49% (124)** | 75,00% (117) | 77,56% (121) |
| **OVERALL (Global)** | **500** | **61,20% (306)** | **63,40% (317)** | **64,20% (321)** | **65,60% (328)** | **64,80% (324)** | **66,20% (331)** |

- **Descoberta Teórica Central — O Fenômeno da Interferência Factual:**
  - Por que `knowledge-update` caiu de `73,08%` ($A$, com 72% dos grafos vazios) para `67,95%` ($A^*$) e `65,38%` ($B_0$)?
  - Porque quando a memória semântica funciona e extrai todos os fatos **sem validade temporal**, ela condensa e injeta no topo do prompt tanto o fato antigo quanto o novo como verdades indistinguíveis (`- fato`). No Caso `01493427` (cartões-postais: 17 $\rightarrow$ 25), a $B_0$ chega a somar os dois estados e responder *"42"*.
- **Resolução Causal pela Validade Temporal:**
  - $B_0 \rightarrow B$ em KU: **+14 ganhos e 0 regressões** (`65,38% → 83,33%`, McNemar bilateral $p = 0{,}0001$, $p_{\text{Holm}} = 0{,}0015$).
  - $A^* \rightarrow B$ em KU: **+14 ganhos e 2 regressões** (+12 líquidos, $p = 0{,}0042$).
  - Estabilidade frente ao piso de ruído ($B'$): KU manteve **exatamente `83,33%`** (`+1/-1`, **97,44% de estabilidade**).

---

### Slide 7 — Desacoplamento Causal (Ablação 2×2) e Robustez ([`R08`](../reports/analysis/R08_ablacao_fatorial_score_vs_tags_20261119.md), [`R09`](../reports/analysis/R09_sensibilidade_lambda_tau_20261119.md)) (1,5 min)
*(Usar Figura 6: [`reports/figures/fig6_ablacao_sensibilidade.png`](../reports/figures/fig6_ablacao_sensibilidade.png))*

1. **Ablação Fatorial 2×2 (`score_only` vs. `tags_only` sobre os mesmos 500 grafos):**
   - `score_only` ($\mathcal{V}$ ligado, sem etiquetas): **`65,38%` em KU** (`+3/-3` vs. $B_0$, $p = 1{,}000$ — **efeito nulo**).
   - `tags_only` ($\mathcal{V} \equiv 1$, etiquetas ligadas): **`85,90%` em KU** (**`+16/-0`** vs. $B_0$, $p < 0{,}0001$) e **`66,20%` global** (maior marca do projeto).
   - **Por quê?** No recorte *oracle* (~9,18 fatos/grafo e `semantic_top_k=5`), tanto o fato antigo quanto o novo entram no `top-5`. Reordenar sem etiquetar não remove a contradição do contexto; as etiquetas `[CURRENT]`/`[HISTORICAL]` são o motor causal que desambigua a geração.
2. **Análise de Sensibilidade ($\lambda \in \{0{,}4; 0{,}6; 0{,}8\}$, $\tau \in \{30, 60, 90\}\text{d}$):**
   - Global permaneceu entre **`65,60%` e `66,80%`** (amplitude de `1,20 p.p.`, menor que o piso de ruído de `1,60 p.p.`).
   - KU permaneceu entre **`79,49%` e `84,62%`** (todos $p \le 0{,}0034$ vs. $B_0$). Resultado classificado como **ROBUSTO**.

---

### Slide 8 — O Trade-off de *Over-Supersession*, $B_{\text{v2}}$ (*Event Calculus*) e Auditoria [`R07`](../reports/analysis/R07_auditoria_supersessao_B_vs_Bv2.md) (1,5 min)
*(Usar Figura 4: [`reports/figures/fig4_estudo_caso_supersessao.png`](../reports/figures/fig4_estudo_caso_supersessao.png))*

- **O efeito colateral em `multi-session`:**
  - Perguntas de contagem cumulativa (ex.: *"Quantos cursos online concluí?"*) sofrem quando eventos distintos são classificados como `SUPERSEDES`.
- **Proposta $B_{\text{v2}}$ (Classificador Ontológico baseado em *Event Calculus*, sem exemplos de domínio):**
  - Restringe `SUPERSEDES` a atributos de valor único / estados mutuamente exclusivos; eventos, transações e objetos coexistentes são `EXTENDS`.
  - **Cortou o volume de supersessões em 53,6%** (`612 → 284`).
  - **Elevou a precisão auditada ($n=45$) de `33,3%` para `48,9%`** (em `temporal-reasoning`, quadruplicou de **`13,3% → 53,3%`**, explicando o recorde de **`57,89%`** em TR).
  - Manteve ganho significativo em KU (**`79,49%`**, $p = 0{,}0034$ vs. $B_0$ e $p = 0{,}0117$ vs. $A^*$).
- **Achados de Auditoria do Benchmark (`R05` Achado 10 e `R07`):**
  1. O arquivo `longmemeval_s.json` distribuído no repositório oficial do HeLa-Mem contém apenas as sessões de evidência (1–6 sessões, variante *oracle*).
  2. **34/500 itens** possuem `haystack_dates` fora de ordem cronológica no JSON, causando supersessões reversas (`valid_to < valid_from`) exclusivamente em `temporal-reasoning`.

---

### Slide 9 — Conclusões e Trabalhos Futuros (1 min)
- **Resposta à Pergunta de Pesquisa:**
  - **Fortemente suportada em atualização de conhecimento (`knowledge-update`):** ganho de +15,38 p.p. sobre $A^*$ ($p = 0{,}0042$) e +17,95 p.p. sobre $B_0$ ($p_{\text{Holm}} = 0{,}0015$), estável frente a ruído e hiperparâmetros.
  - **Não suportada como ganho global significativo:** devido ao trade-off entre atualização de estado e agregação cumulativa em `multi-session`.
- **Contribuições:**
  1. Identificação e prova empírica do **fenômeno de interferência factual** em memórias semânticas densas sem validade temporal.
  2. Demonstração via ablação fatorial 2×2 de que, em grafos compactos (*oracle*), a **sinalização de vigência no prompt (`tags_only`)** é o motor causal do ganho.
  3. Formulação ontológica via *Event Calculus* ($B_{\text{v2}}$) e descoberta de duas anomalias no benchmark oficial distribuído pelo HeLa-Mem (recorte *oracle* e 34 itens com datas fora de ordem).
- **Trabalhos Futuros:**
  - Ativar a guarda cronológica (`--chronological_guard`) e pré-ordenar sessões; avaliar no *LongMemEval-S* completo (~40 sessões/item, onde $\mathcal{V}$ atua como filtro de *recall@5*) e no *LoCoMo*.

---

## 2. Guia de Respostas para Perguntas Prováveis da Banca (Q&A)

### P1: *"Por que o ganho global ($A^* \rightarrow B$: 63,40% $\rightarrow$ 65,60%, $p = 0{,}278$) não é estatisticamente significativo, e por que isso não invalida o trabalho?"*
> **Resposta:** O benchmark LongMemEval agrega 6 categorias com demandas cognitivas opostas. Apenas `knowledge-update` (78 itens) testa diretamente a substituição de estado ao longo do tempo, enquanto `multi-session` (133 itens) testa majoritariamente contagem e agregação cumulativa de eventos. Na categoria-alvo (`knowledge-update`), o efeito é massivo e altamente significativo tanto contra a Baseline Fiel $A^*$ (+12 acertos líquidos, $p = 0{,}0042$) quanto contra a ablação controlada $B_0$ (+14 ganhos e 0 regressões, $p_{\text{Holm}} = 0{,}0015$), superando em mais de 6 vezes o piso de ruído estocástico. No agregado global, esse ganho é parcialmente compensado pela *over-supersession* em `multi-session` — um trade-off estrutural que nós isolamos, auditamos manualmente em `R07` e mitigamos com a formulação ontológica $B_{\text{v2}}$.

### P2: *"Na ablação fatorial 2×2 (`R08`), `tags_only` (66,20% global, 85,90% em KU) foi tão bom ou melhor que $B$ completo (65,60% global, 83,33% em KU), enquanto `score_only` teve efeito nulo em KU. Então a equação de pertinência $\mathcal{V}(f_i, t_{\text{query}})$ é desnecessária?"*
> **Resposta:** Ela é redundante **especificamente no regime *oracle***, e a ablação 2×2 foi fundamental para descobrir o porquê. No arquivo distribuído pelo HeLa-Mem (que contém apenas as 1 a 6 sessões de evidência), cada grafo semântico possui em média apenas **9,18 fatos**. Como o retriever recupera `semantic_top_k = 5`, tanto o fato antigo quanto o fato novo entram nos 5 fatos enviados ao prompt mesmo com $\mathcal{V} \equiv 1$. Nesse regime, o gargalo não é o *recall@5* na busca, mas sim a **desambiguação dentro do prompt**, que é resolvida pelas etiquetas `[CURRENT]` e `[HISTORICAL]`. Porém, em um cenário de memória longa com dezenas de sessões distratoras (como o LongMemEval-S completo de ~40 sessões e >150 fatos por grafo), fatos obsoletos com alta similaridade lexical ocupariam as 5 vagas do `top-k` se não fossem atenuados por $\mathcal{V}(f_i, t_{\text{query}})$. Ou seja: $\mathcal{V}$ governa o **ranking de recuperação** em grafos grandes, enquanto as etiquetas governam a **resolução de conflito na geração**.

### P3: *"Os grafos episódicos de $B$, $B_0$ e $B_{\text{v2}}$ foram reaproveitados da Baseline $A$ (`MAX_FLIPPED=5`, `KEYWORD_WEIGHT=0.5`), enquanto a Baseline Fiel $A^*$ usou os parâmetros dos scripts `.sh` (`MAX_FLIPPED=3`, `KEYWORD_WEIGHT=0.7`). Isso afeta a comparação?"*
> **Resposta:** Por isso mantivemos **duas referências complementares** no artigo:
> 1. Para isolamento causal puro do mecanismo temporal, a comparação $B_0 \rightarrow B / B_{\text{v2}} / \texttt{tags\_only}$ é **100% pareada sobre exatamente os mesmos 500 grafos episódicos e semânticos**, variando única e exclusivamente o mecanismo temporal. Nela, o ganho em KU é de +14/-0 ($p_{\text{Holm}} = 0{,}0015$) e +16/-0 em `tags_only` ($p < 0{,}0001$).
> 2. Para garantir que não estávamos vencendo uma baseline fragilizada por falha de concorrência ou desvio de hiperparâmetros, construímos a Baseline Fiel $A^*$ com 100% dos grafos íntegros e parâmetros oficiais. Contra $A^*$, a Proposta $B$ mantém +12 acertos líquidos em KU ($p = 0{,}0042$) e $B_{\text{v2}}$ mantém +9 ($p = 0{,}0117$). Além disso, a transição $A^* \rightarrow B_0$ em KU foi de 53 para 51 acertos ($p = 0{,}8145$), mostrando que a pequena diferença nos parâmetros episódicos não explica o salto em `knowledge-update`.

### P4: *"Como vocês descobriram que o dataset distribuído no repositório do HeLa-Mem é a variante *oracle*?"*
> **Resposta:** Durante a auditoria `R05` (Achado 10), inspecionamos programaticamente o JSON `external/HeLa-Mem/data/longmemeval_s.json` e verificamos que, nos 500 itens, a lista `haystack_session_ids` é idêntica a `answer_session_ids` (1 a 6 sessões por item, ~6,6 mil tokens), enquanto o artigo do LongMemEval (Wu et al., ICLR 2025) define o split `S` completo com ~40 sessões e ~115 mil tokens por item. Cruzando os papers do HeLa-Mem e do LightMem, documentamos que o repositório oficial do HeLa-Mem distribui o recorte *oracle* sob o nome `longmemeval_s.json`. Por honestidade científica, reportamos explicitamente essa característica e baseamos todas as nossas conclusões nas comparações internas pareadas sobre o mesmo arquivo.

### P5: *"Qual o custo adicional de chamadas de LLM da Proposta $B$ / $B_{\text{v2}}$?"*
> **Resposta:** Na etapa de **consulta/avaliação (inferência)**, o custo adicional de chamadas de LLM é **zero**: o cálculo de $\mathcal{V}(f_i, t_{\text{query}})$ e a formatação das etiquetas `[CURRENT]`/`[HISTORICAL]` são operações algébricas e determinísticas em Python. O custo adicional ocorre apenas na etapa de **ingestão/codificação** da memória semântica, quando um novo fato apresenta similaridade $\ge 0{,}35$ com fatos ativos de sessões anteriores (até 4 candidatos), acionando o classificador `classify_relation`. Em sessões únicas (156 dos 500 itens), esse custo extra também é zero por construção.
