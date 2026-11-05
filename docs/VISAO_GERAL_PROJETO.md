# Visão Geral do Projeto — Validade Temporal em Memória Associativa Hebbiana

**Disciplina:** Deep Learning — Mestrado, CIn/UFPE (Prof. Cleber Zanchettin)
**Autor:** Filipe Augusto de Ataíde Barbosa
**Artigo-base:** *HeLa-Mem: Hebbian Learning and Associative Memory for LLM Agents* (ACL 2026)
**Situação em 2026-11-04:** Draft 2 (terceira entrega) revisado; ablação B0 executada; plano de correção R05 em andamento.

Este documento reúne em um só lugar a origem do projeto, os conceitos necessários para entendê-lo, as mudanças de rumo, o que foi implementado, os resultados e o que falta fazer. Ele foi escrito para quem nunca viu o repositório e não precisa conhecer de antemão memória para agentes, grafos ou estatística pareada: cada conceito é explicado antes de ser usado, quase sempre com um exemplo numérico. Os detalhes de cada parte estão nos documentos citados ao longo do texto.

**Como ler:**

- **Para entender o projeto rapidamente:** leia a Seção 1.
- **Para uma leitura completa:** siga a ordem do sumário.
- **Se você já conhece LLMs, embeddings e grafos:** pule a Seção 3 e consulte-a quando um termo for novo.

---

## Sumário

1. [Resumo em uma página](#1-resumo-em-uma-página)
2. [As regras do jogo: o que a disciplina exige](#2-as-regras-do-jogo-o-que-a-disciplina-exige)
3. [Conceitos fundamentais](#3-conceitos-fundamentais)
4. [Origem: de onde o projeto veio e por que mudou](#4-origem-de-onde-o-projeto-veio-e-por-que-mudou)
5. [O artigo-base: como o HeLa-Mem funciona](#5-o-artigo-base-como-o-hela-mem-funciona)
6. [O problema: recência não é validade](#6-o-problema-recência-não-é-validade)
7. [A proposta: validade temporal e supersessão](#7-a-proposta-validade-temporal-e-supersessão)
8. [Dados, métricas e desenho experimental](#8-dados-métricas-e-desenho-experimental)
9. [Linha do tempo da execução](#9-linha-do-tempo-da-execução)
10. [Resultados](#10-resultados)
11. [Interpretação: o que os resultados dizem sobre a hipótese](#11-interpretação-o-que-os-resultados-dizem-sobre-a-hipótese)
12. [Auditoria do processo e limitações conhecidas](#12-auditoria-do-processo-e-limitações-conhecidas)
13. [Próximos passos](#13-próximos-passos)
14. [Mapa do repositório e como reproduzir](#14-mapa-do-repositório-e-como-reproduzir)
15. [Glossário](#15-glossário)
16. [Documentos de referência](#16-documentos-de-referência)

---

## 1. Resumo em uma página

**Pergunta de pesquisa.** A representação explícita da validade temporal dos fatos, com supersessão de fatos desatualizados, melhora uma memória associativa hebbiana para agentes baseados em LLM, em especial em tarefas de atualização de conhecimento e raciocínio temporal?

**Ideia central.** Uma memória de agente pode guardar "o usuário tem 1.250 seguidores" e, horas depois, "o usuário tem 1.300 seguidores". As duas frases ficam na memória com o mesmo status, e na hora de responder o modelo pode escolher a antiga. O HeLa-Mem, artigo-base deste trabalho, organiza memórias em um grafo com aprendizado hebbiano, mas não sabe quando um fato deixou de ser verdadeiro. A proposta adiciona a cada fato uma janela de validade `[t_start, t_end]`. Um classificador detecta quando um fato novo substitui um antigo, e o antigo é marcado como histórico, sem ser apagado. Na busca, os fatos expirados perdem peso e entram no prompt com uma etiqueta de estado (atual ou histórico).

**Como foi testado.** Nas 500 questões do benchmark LongMemEval distribuídas com o código do HeLa-Mem, foram comparadas três condições:

| Condição | O que é | Acurácia |
|---|---|---|
| **A** | HeLa-Mem original (reprodução) | 61,20% (306/500) |
| **B0** | Fatos extraídos por sessão, **sem** o mecanismo temporal (ablação) | 64,20% (321/500) |
| **B** | Proposta completa (extração por sessão **com** mecanismo temporal) | 65,60% (328/500) |

**O que os resultados mostram.**

- B supera A em +22 questões (McNemar bilateral p = 0,023).
- A maior parte desse ganho (+15) vem de uma mudança secundária: extrair os fatos por sessão. O mecanismo temporal soma +7 no total, sem significância estatística (p = 0,45).
- O mecanismo temporal funciona exatamente onde a hipótese previa. Em *Knowledge Update*, B0 → B corrige **14 questões com zero regressões** (p = 0,0015 após correção de Holm), todas em diálogos onde houve supersessão.
- Ele também tem um custo: em *Multi-Session*, B0 → B perde 7 questões, porque eventos repetidos ("montei outro aquário") são tratados como substituição e deixam de ser contados.

**Conclusão atual.** A hipótese é **suportada em atualização de conhecimento** e **não suportada no total**. O próximo passo direto é ajustar o classificador para separar estados que se excluem ("moro em X" → "moro em Y") de eventos que se acumulam ("fui a um jantar" → "fui a outro jantar").

**Ressalvas importantes** (detalhadas na Seção 12):

- o arquivo de dados contém apenas as sessões de evidência de cada questão, não as ~40 sessões do LongMemEval-S oficial;
- a baseline rodou com dois hiperparâmetros diferentes dos scripts oficiais;
- geração e juiz usam `temperature=0.7`, sem repetições;
- há 360 grafos semânticos vazios na baseline cuja causa ainda está em investigação.

---

## 2. As regras do jogo: o que a disciplina exige

As diretrizes do professor ([docs/projeto_diretrizes.md](projeto_diretrizes.md)) definem uma lógica experimental específica:

1. escolher um problema de interesse;
2. partir de um **bom artigo com código** e entendê-lo razoavelmente bem;
3. **reproduzir os resultados originais sem modificações**;
4. só então propor uma evolução, uma alteração ou um estudo comparativo;
5. executar experimentos e analisar quantitativa e qualitativamente;
6. considerar prazo, dados disponíveis e hardware.

Dois pontos dessas regras orientaram todas as decisões:

- **A evolução precisa evoluir o artigo-base**, e não apenas usá-lo como peça. Esse critério derrubou a primeira versão do projeto (Seção 4).
- **Resultado negativo é resultado.** O objetivo não é "ganhar do artigo", e sim testar uma hipótese com um experimento controlado e analisar o que aconteceu.

Além das diretrizes da disciplina, o projeto segue as regras de análise do [AGENT.MD](../AGENT.MD): separar fatos de hipóteses, não confundir correlação com causa, registrar cada análise, não ajustar o método até a hipótese "dar certo", declarar o grau de certeza de cada conclusão.

---

## 3. Conceitos fundamentais

Esta seção explica, do zero, tudo o que é preciso para acompanhar o restante do documento. Os conceitos estão em ordem: cada um usa apenas os anteriores.

### 3.1 LLMs e o problema da memória

Um **LLM** (*Large Language Model*, como o GPT) gera texto a partir de um texto de entrada, chamado **prompt**. Ele só "enxerga" o que está no prompt naquele momento. O tamanho máximo do prompt é a **janela de contexto**.

Um **agente baseado em LLM** é um sistema que conversa com o usuário ao longo do tempo, por exemplo um assistente pessoal. Para lembrar o que o usuário disse semanas atrás, ele tem duas opções:

1. **Colocar a conversa inteira no prompt.** Funciona para conversas curtas, mas fica caro e lento à medida que o histórico cresce, além de esbarrar no limite da janela de contexto. Mesmo quando cabe, modelos tendem a perder detalhes no meio de textos muito longos.
2. **Ter uma memória externa.** Os trechos importantes da conversa ficam guardados fora do modelo. A cada pergunta, o sistema **busca** os trechos relevantes e coloca só esses no prompt.

Este projeto trata da segunda opção: **como organizar e buscar essa memória externa**, em especial quando as informações mudam com o tempo.

### 3.2 Embeddings e similaridade de cosseno

Para buscar "trechos relevantes", o computador precisa medir o quanto dois textos falam da mesma coisa. Isso é feito com **embeddings**.

Um **embedding** é um vetor de números que representa o significado de um texto. Um modelo treinado para isso (aqui, o `all-MiniLM-L6-v2`, que gera vetores de 384 números) coloca textos de significado parecido em pontos próximos desse espaço. "Tenho 1.250 seguidores no Instagram" e "quantos seguidores eu tenho?" ficam próximos; "comprei sandálias" fica longe.

A proximidade é medida pela **similaridade de cosseno**, o cosseno do ângulo entre os dois vetores:

- vale **1** quando os vetores apontam na mesma direção (mesmo significado);
- vale **0** quando são perpendiculares (assuntos sem relação);
- vale **−1** quando apontam em direções opostas.

Na prática, textos relacionados ficam entre 0,3 e 0,9. O HeLa-Mem e a proposta **reescalam** esse valor para o intervalo [0, 1] com a fórmula `(1 + cosseno) / 2`. Assim, um cosseno de 0,70 vira 0,85.

**Limitação importante para este projeto:** a similaridade mede **assunto**, não **verdade** nem **atualidade**. "Tenho 1.250 seguidores" e "tenho 1.300 seguidores" têm similaridade altíssima com a pergunta "quantos seguidores eu tenho?". A similaridade não tem como saber que a primeira frase está desatualizada.

### 3.3 RAG: recuperar antes de gerar

**RAG** (*Retrieval-Augmented Generation*) é o padrão de:

1. transformar a pergunta em embedding;
2. buscar os k trechos mais similares na memória (os **top-k**);
3. montar um prompt com esses trechos mais a pergunta;
4. deixar o LLM responder.

O HeLa-Mem é uma forma sofisticada de RAG: além da similaridade, ele usa as **ligações entre memórias** para decidir o que buscar.

### 3.4 Grafos e grafos de conhecimento

Um **grafo** é um conjunto de **nós** (pontos) ligados por **arestas** (ligações). As arestas podem ter **pesos**, que indicam a força da ligação.

Na memória de um agente:

- cada **nó** guarda uma memória, como um trecho de conversa ou um fato;
- cada **aresta** diz que duas memórias estão relacionadas, e o peso diz o quanto.

Um **grafo de conhecimento** é um grafo em que os nós são fatos ou entidades ("Maria", "Projeto X") e as arestas são relações ("Maria é responsável pelo Projeto X"). A vantagem sobre uma lista de textos é poder seguir as ligações: a partir de uma memória relevante, chegar a outras associadas a ela, mesmo que não sejam parecidas com a pergunta.

### 3.5 Aprendizado hebbiano

A **regra de Hebb** vem da neurociência: "neurônios que disparam juntos se conectam". Se duas memórias costumam ser usadas ao mesmo tempo, a ligação entre elas deve ficar mais forte, para que lembrar de uma ajude a lembrar da outra.

No HeLa-Mem, isso vira uma regra simples. Toda vez que um conjunto de nós é recuperado junto para responder uma pergunta, cada par desses nós ganha um reforço constante:

```text
w_ij ← min(1, w_ij + η)        com η = 0,02 (a "taxa de aprendizado")
```

**Exemplo:** dois nós consecutivos começam ligados com peso 0,5. Se forem recuperados juntos em 10 perguntas, o peso sobe para 0,5 + 10 × 0,02 = 0,70. O `min(1, …)` impede que o peso passe de 1.

É por isso que o HeLa-Mem se chama **memória associativa**: as ligações se ajustam com o uso, sem treino separado.

### 3.6 Ativação espalhada

A **ativação espalhada** (*spreading activation*) é a forma de usar essas ligações na busca:

1. cada nó recebe um score inicial pela similaridade com a pergunta (a sua "ativação");
2. os nós com ativação acima de um limiar "espalham" parte dela para os vizinhos, proporcionalmente ao peso da aresta;
3. um nó pouco parecido com a pergunta, mas fortemente ligado a um nó muito parecido, pode subir no ranking.

**Exemplo** (parâmetros do HeLa-Mem: limiar 0,4 e fator α = 0,1): um nó com score 0,8 ligado a um vizinho por uma aresta de peso 0,7 passa para ele 0,8 × 0,7 × 0,1 = **0,056** de ativação extra.

Isso é útil para perguntas de **múltiplos saltos**, em que a resposta depende de juntar memórias que, isoladas, não parecem relevantes.

### 3.7 Memória episódica e memória semântica

A psicologia distingue dois tipos de memória de longo prazo, e o HeLa-Mem adota a mesma divisão:

| | Memória episódica | Memória semântica |
|---|---|---|
| **O que guarda** | Eventos, com quando aconteceram | Fatos gerais, destilados dos eventos |
| **Exemplo humano** | "Na terça, no almoço, a Ana me contou que mudou de emprego" | "A Ana trabalha na empresa Y" |
| **No HeLa-Mem** | Trechos brutos da conversa, com a data da sessão | Frases curtas extraídas por um LLM ("User has 1250 followers on Instagram") |

A memória semântica é mais compacta e direta, mas perde detalhes e, no HeLa-Mem original, perde também a **data** de cada fato. Este projeto mexe **apenas na memória semântica**.

### 3.8 Extração de fatos por LLM

A memória semântica é preenchida por um LLM que lê trechos da conversa e devolve três coisas:

- um **perfil** do usuário (traços gerais, atualizado a cada rodada);
- **fatos sobre o usuário**: eventos, datas, locais e preferências mencionados explicitamente;
- **conhecimento do assistente**: o que o próprio assistente informou.

A forma de **agrupar** os turnos antes de mandar ao LLM importa:

- o HeLa-Mem agrupa de **10 em 10 turnos**, o que pode misturar sessões de dias diferentes num mesmo bloco;
- a proposta agrupa **por sessão**, o que permite associar cada fato à data exata em que foi dito.

Na Seção 10 vamos ver que essa diferença, que parecia um detalhe, tem efeito grande.

### 3.9 Recência, saliência e validade

Estes três conceitos costumam ser misturados sob o nome "decaimento temporal". São coisas diferentes:

| Conceito | Pergunta que responde | Exemplo |
|---|---|---|
| **Recência** | Quão nova é a informação? | "Isso foi dito ontem" |
| **Saliência** | Quão importante ou usada ela é? | "Isso é lembrado com frequência" |
| **Validade** | Ela ainda é verdadeira agora? | "Maria era responsável até março; agora é João" |

Por que a diferença importa:

- uma informação **antiga** pode continuar **válida**: "o projeto foi aprovado pelo conselho em 2024" é verdade para sempre;
- uma informação **recente** pode já estar **inválida**: no caso dos seguidores, o fato de 1.250 foi dito na manhã e substituído na tarde do mesmo dia;
- uma informação **inválida** pode continuar **útil**: "quem era responsável em fevereiro?" precisa justamente do fato antigo.

Um **decaimento por recência** (reduzir o peso de memórias antigas) erra nos três casos. A **validade** resolve: em vez de perguntar "há quanto tempo isso foi dito?", pergunta "isso era verdade na data da pergunta?".

### 3.10 Grafos de conhecimento temporais e supersessão

Um **grafo de conhecimento temporal**, como o do Zep/Graphiti, guarda em cada fato **o período em que ele é válido**:

```text
Maria ─responsável_por→ Projeto X     válido de: janeiro   até: março
João  ─responsável_por→ Projeto X     válido de: março     até: (hoje)
```

**Supersessão** é o evento em que um fato novo encerra a validade de um antigo. Ela é **não-destrutiva**: o fato antigo não é apagado, só ganha uma data de fim. Com isso o sistema responde as duas perguntas:

- "Quem é o responsável **atual**?" → João (o fato sem data de fim).
- "Quem era o responsável **em fevereiro**?" → Maria (o fato válido naquela data).

Um sistema que **sobrescreve** o fato antigo responderia a primeira e perderia a segunda. Um sistema que **acumula** sem marcar validade, como o HeLa-Mem, tem os dois fatos mas não sabe qual vale agora.

### 3.11 Avaliação com LLM como juiz

Respostas de agentes são texto livre: "1300", "1.300 seguidores" e "cerca de 1300" podem estar todas certas. Comparar strings não funciona. O **LLM-as-a-judge** resolve isso pedindo a outro LLM que compare a resposta com o gabarito e diga se está correta.

Dois cuidados:

- **o juiz erra:** ele pode aprovar "increased" e reprovar "increase" para a mesma pergunta, ou exigir um detalhe que o gabarito tem ("in my closet");
- **o juiz e o gerador são o mesmo modelo** (`gpt-4o-mini`), o que pode criar vieses em comum.

### 3.12 Temperatura e ruído entre execuções

A **temperatura** controla o quanto um LLM sorteia entre respostas possíveis:

- **temperatura 0:** escolhe sempre a resposta mais provável (quase determinístico);
- **temperatura 0,7** (usada aqui, no gerador **e** no juiz): sorteia com frequência.

Na prática, rodar exatamente o mesmo sistema duas vezes pode mudar o resultado de algumas questões, só por acaso. Por isso parte das diferenças entre A, B0 e B é **ruído**. Para saber quanto, é preciso rodar o mesmo sistema duas vezes e contar as discordâncias. Isso ainda não foi feito (execução B', Seção 13).

### 3.13 Ablação e fatores de confusão

Um **fator de confusão** aparece quando duas coisas mudam ao mesmo tempo e não dá para saber qual causou o efeito. **Exemplo:** se você troca de remédio e de dieta na mesma semana e melhora, não sabe qual dos dois funcionou.

Foi o que aconteceu de A para B: mudou o modo de extrair fatos **e** entrou o mecanismo temporal.

Uma **ablação** resolve isso removendo um componente de cada vez. A condição **B0** é B **sem** o mecanismo temporal: os mesmos fatos, mas todos tratados como válidos e sem etiquetas. Assim:

```text
A  ──(muda só a extração)──►  B0  ──(liga só o mecanismo temporal)──►  B
```

- a diferença **A → B0** é o efeito da extração;
- a diferença **B0 → B** é o efeito do mecanismo temporal.

### 3.14 Avaliação pareada e o teste de McNemar

As três condições respondem **as mesmas 500 questões**. Isso permite uma comparação **pareada**: em vez de comparar só as acurácias totais, olha-se questão por questão.

Para duas condições X e Y, cada questão cai em uma de quatro situações:

| | Y acerta | Y erra |
|---|---|---|
| **X acerta** | ambos acertam | **regressão** (c) |
| **X erra** | **ganho** (b) | ambos erram |

As questões em que ambos acertam ou ambos erram não dizem nada sobre qual sistema é melhor. Só importam os **pares discordantes**: b ganhos e c regressões.

O **teste exato de McNemar** pergunta: *se os dois sistemas fossem igualmente bons, qual a chance de ver uma divisão tão desigual entre ganhos e regressões?* Sob essa hipótese, cada par discordante teria 50% de chance de ser ganho ou regressão, como uma moeda.

**Exemplo (A → B):** b = 54 ganhos e c = 32 regressões, ou seja, 86 pares discordantes. A chance de uma moeda honesta dar uma divisão tão ou mais desigual que 54 a 32 em 86 lançamentos é **2,3%**. Esse é o **p-valor** (p = 0,023).

**Exemplo (KU, B0 → B):** 14 ganhos e 0 regressões. A chance de 14 caras seguidas é (1/2)¹⁴ ≈ 0,00006; considerando os dois sentidos (14 a 0 ou 0 a 14), p ≈ 0,00012.

### 3.15 p-valor, significância e intervalo de confiança

O **p-valor** é a probabilidade de observar um resultado tão extremo **se não houvesse efeito nenhum**. Por convenção, p < 0,05 é chamado de **estatisticamente significativo**. Três cuidados:

- p < 0,05 **não** quer dizer "95% de certeza de que o efeito existe";
- p > 0,05 **não** quer dizer "não há efeito", e sim "os dados não bastam para distinguir o efeito do acaso";
- significância estatística não é o mesmo que relevância prática.

O **intervalo de confiança de 95% (IC)** dá uma faixa de valores plausíveis para o tamanho do efeito. Para A → B, a diferença de acurácia é +4,40 p.p., com IC de **[0,79; 8,01]**: o efeito real provavelmente está entre quase nada e 8 pontos. Se o IC inclui o zero, como em B0 → B, com [−1,71; 4,51], os dados são compatíveis com efeito nulo.

O IC pareado usado aqui é calculado só com os pares discordantes:

```text
diferença = (b − c) / n
erro padrão = √(b + c − (b − c)² / n) / n
IC 95% = diferença ± 1,96 × erro padrão
```

Para A → B: diferença = 22/500 = 0,044; erro padrão ≈ 0,0184; IC = 0,044 ± 0,036 → [0,0079; 0,0801].

### 3.16 Comparações múltiplas e a correção de Holm

Se você faz **um** teste com limite de 5%, tem 5% de chance de um falso positivo. Se faz **doze**, a chance de **pelo menos um** falso positivo sobe para cerca de 46%. Aqui foram feitos 12 testes por categoria (6 categorias × 2 etapas), então algum "resultado significativo" poderia aparecer por puro acaso.

A **correção de Holm** ajusta os p-valores para isso:

1. ordene os 12 p-valores do menor para o maior;
2. multiplique o menor por 12, o segundo por 11, o terceiro por 10, e assim por diante;
3. garanta que a sequência ajustada nunca diminua (cada valor é o máximo entre ele e o anterior).

**Exemplo:** o menor p-valor é o de KU em B0 → B, 0,00012. Ajustado: 0,00012 × 12 = **0,0015**, ainda bem abaixo de 0,05. O segundo menor (Multi-Session em A → B0, p = 0,052) vira 0,052 × 11 ≈ 0,58, que não é significativo. Por isso o documento diz que **só uma** diferença por categoria resiste à correção.

### 3.17 Taxa de base

Para saber se uma categoria "concentra" erros, não basta olhar a fatia de erros. É preciso compará-la com a fatia de **questões**. **Exemplo:** na baseline, *Temporal Reasoning* e *Knowledge Update* juntas têm 43,8% dos erros, mas também 42,2% das questões. Os erros estão distribuídos na proporção esperada, então não há concentração. A comparação correta é pela **taxa de erro dentro de cada categoria** (Seção 6.4).

---

## 4. Origem: de onde o projeto veio e por que mudou

O projeto passou por três fases antes de chegar à forma atual.

### 4.1 Fase 1 — Grafo de conhecimento da Reforma Tributária (setembro de 2026)

A primeira versão (o repositório ainda se chama `kg-reforma-tributaria` em alguns lugares) pretendia construir um **grafo de conhecimento incremental a partir das normas da Reforma Tributária** (EC 132/2023, LC 214/2025, LC 227/2026 e regulamentos da CBS e do IBS) e comparar três braços:

1. extração direta de triplas por LLM;
2. extração mais validação semântica;
3. extração mais pós-processamento estrutural com **GraphSAGE**, uma rede neural para grafos (GNN) que proporia arestas faltantes.

O artigo-base seria o GraphSAGE. A reprodução foi feita no dataset PPI, uma rede de interações entre proteínas e benchmark clássico de GNNs. A primeira tentativa (R01) estava errada e foi refeita do zero (R02), com equivalência numérica exata ao PyTorch Geometric. Esses registros continuam em `reports/analysis/R01*`, `R02*` e no código `src/modeling/sage_*.py`, `reproduce_ppi.py`, `baseline_graphsage.py`.

### 4.2 Por que a Fase 1 foi abandonada

Em 19/09/2026 uma revisão contra as diretrizes ([outras-ideias (desconsiderar)/07-selecao-artigo-base.md](<../outras-ideias (desconsiderar)/07-selecao-artigo-base.md>)) mostrou que o desenho **não evoluía o artigo-base**. O teste usado foi simples: trocar o GraphSAGE por qualquer outra GNN não mudaria a pergunta de pesquisa, o estudo nem as conclusões possíveis. O artigo estava sendo usado como peça intercambiável.

A decisão foi inverter a ordem: **escolher o artigo-base pelo artigo, e não pelo tema.** O domínio de aplicação passou a ser consequência da escolha. O material dessa fase está em `outras-ideias (desconsiderar)/` e não faz parte do projeto atual.

### 4.3 Fase 2 — A busca pelo artigo certo

A busca partiu de interesses amplos (agentes de programação, memória organizacional, transcrições de reuniões, grafos) e convergiu para **grafos aplicados à memória de agentes**. Memória organizacional chamou atenção por um motivo que acabou definindo o projeto: conhecimento organizacional **muda com o tempo** (decisões são revistas, responsáveis trocam). A sequência de artigos considerados está documentada em detalhe no [README](../README.md):

| Artigo | O que propõe | Por que não bastou |
|---|---|---|
| **Microsoft GraphRAG** | Transformar documentos em grafo de entidades, detectar comunidades e resumi-las | Não é um sistema de memória temporal |
| **A-MEM** | Memória em notas estruturadas (estilo Zettelkasten) que se ligam e evoluem | A primeira ideia, "adicionar reforço e decaimento às ligações", já existia em outro trabalho |
| **HeLa-Mem** (ACL 2026) | Grafo de memória com aprendizado hebbiano, ativação espalhada e consolidação | **Escolhido como artigo-base**: código oficial, suporte ao LongMemEval, reprodutível |
| **Zep / Graphiti** | Grafo de conhecimento temporal: cada relação tem um período de validade | Não é o artigo-base, mas inspirou a evolução |

A observação decisiva foi que **HeLa-Mem e Zep respondem perguntas diferentes**:

- o HeLa-Mem responde "quais memórias estão associadas e quais conexões ficaram mais fortes com o uso?";
- o Zep responde "qual informação era verdadeira em determinado momento e quando deixou de ser?".

Juntar os dois frameworks inteiros seria grande demais. A proposta foi usar o HeLa-Mem como base e introduzir **um mecanismo específico inspirado no Zep**: a validade temporal dos fatos.

### 4.4 Fase 3 — O projeto atual

| Data | Marco |
|---|---|
| 27–29/09/2026 | Reprodução do HeLa-Mem: piloto e execução completa dos 500 itens (61,20%) |
| Entrega 1 | Relatório com a reprodução e o diagnóstico ([reports/relatorio_entrega1_enxuto.md](../reports/relatorio_entrega1_enxuto.md)) |
| 02/11/2026 | Implementação da Proposta B e execução incremental (100 → 500 itens) |
| 03/11/2026 | Draft 2 (terceira entrega) com 65,60% |
| 04/11/2026 | Auditoria do processo (R05), ablação B0, revisão do Draft 2 e dos notebooks |

---

## 5. O artigo-base: como o HeLa-Mem funciona

O HeLa-Mem combina os conceitos das Seções 3.4 a 3.8: um grafo de memória episódica com aprendizado hebbiano e ativação espalhada, mais uma memória semântica de fatos extraídos por LLM. A descrição abaixo segue o **código** (`external/HeLa-Mem/hela_mem/`), que em alguns pontos difere da descrição do artigo.

### 5.1 Codificação: como a memória é construída

Para cada questão do benchmark, o histórico de conversa é percorrido em ordem:

1. **Memória episódica** (`HebbianMemoryGraph`, em `hebbian_memory.py`):
   - cada par de turnos (fala do usuário mais resposta do assistente) vira um **nó**, com o texto, a data da sessão, o embedding e palavras-chave extraídas por LLM;
   - cada nó novo é ligado ao anterior com peso **0,5**, uma "cadeia temporal".
2. **Memória semântica** (`HebbianKnowledgeMemory`):
   - a cada **10 turnos**, um LLM lê o bloco e extrai perfil, fatos do usuário e conhecimento do assistente (Seção 3.8);
   - cada fato vira um nó com o metadado fixo `{"type": "fact"}` e o horário em que o script rodou.

### 5.2 Busca: como uma pergunta é respondida

1. **Score base** de cada nó:

   ```text
   s_i = γ_i × ( similaridade reescalada + κ × sobreposição de palavras-chave )
   ```

   O γ_i deveria ser um decaimento por tempo, κ = 0,5 é o peso das palavras-chave, e a sobreposição é a fração das palavras-chave da pergunta presentes no nó.
2. **Ativação espalhada:** nós com s_i > 0,4 passam α × s_i × w_ij (α = 0,1) a cada vizinho j.
3. **Seleção em duas vias:** entram os **top-k pelo score base** (k = 15 na memória episódica, 5 na semântica) mais até `MAX_FLIPPED` nós que só subiram graças ao espalhamento.
4. **Reforço hebbiano:** os nós recuperados juntos têm suas ligações reforçadas em η = 0,02.
5. **Geração:** o `gpt-4o-mini` recebe um prompt com os trechos episódicos (`<CONTEXT>`), os fatos semânticos (`<KNOWLEDGE BASE>`), o perfil do usuário e a data da pergunta, e responde de forma concisa.

### 5.3 Um exemplo de ponta a ponta

Pergunta: "Quantos seguidores eu tenho no Instagram agora?". O histórico tem duas sessões no mesmo dia: de manhã o usuário diz ter 1.250 seguidores; à tarde, que está perto de 1.300.

- Na memória episódica, os trechos das duas sessões viram nós, ambos muito similares à pergunta.
- Na memória semântica, se a extração funcionar, aparecem fatos como "User has 1250 followers" e "User is nearing 1300 followers", **sem data e sem indicação de qual vale agora**.
- Os dois fatos entram no prompt com o mesmo status. O modelo respondeu **"1250"**, a resposta errada.

É exatamente esse o problema que a proposta ataca.

---

## 6. O problema: recência não é validade

### 6.1 A distinção conceitual

Como explicado na Seção 3.9, **recência, saliência e validade** são coisas diferentes. Um sistema que só sabe "quão parecido com a pergunta" e, no máximo, "quão recente" não tem como distinguir "o usuário **tinha** 1.250 seguidores" de "o usuário **tem** 1.300".

### 6.2 O que a leitura do código do HeLa-Mem revelou

1. **Fatos sem data:** os fatos semânticos recebem o horário em que o script rodou (`get_timestamp()`), e não a data da sessão de onde vieram. Todos os fatos de uma questão ficam com praticamente o mesmo "horário".
2. **Fatos conflitantes competem em pé de igualdade:** quando um atributo do usuário muda, o fato antigo e o novo coexistem e disputam só por similaridade com a pergunta.
3. **Decaimento neutralizado:** a chamada `compute_time_decay(node["timestamp"], current_time)` passa uma data no lugar da constante τ. A conta falha, e a função cai silenciosamente num ramo de exceção que devolve 1. Na prática **não há decaimento**. Isso afeta o grafo episódico, que foi mantido igual em A e B.
4. **A data da pergunta é ignorada na busca:** ela só aparece no prompt final, como texto.

### 6.3 Um exemplo real

Na questão `07741c45`, o usuário guardava os tênis velhos debaixo da cama (20/05/2023) e, seis dias depois, passou a guardá-los numa sapateira no armário. Os dois trechos ficam na memória sem qualquer indicação de qual é o vigente. Perguntado "onde eu guardo meus tênis velhos **atualmente**?", o HeLa-Mem respondeu "debaixo da cama".

### 6.4 Onde a baseline erra (com taxa de base)

| Categoria | Questões | Taxa de erro da baseline |
|---|---:|---:|
| single-session-preference | 30 | 73,3% |
| multi-session | 133 | 53,4% |
| temporal-reasoning | 133 | 48,1% |
| knowledge-update | 78 | 26,9% |
| single-session-user | 70 | 12,9% |
| single-session-assistant | 56 | 12,5% |
| **total** | **500** | **38,8%** |

*Knowledge Update* erra **menos** que a média. A motivação da proposta não vem de uma concentração estatística de erros nessa categoria (Seção 3.17). Ela vem do **tipo** de erro observado nos casos de atualização: o sistema tem as duas versões do fato e escolhe a antiga.

---

## 7. A proposta: validade temporal e supersessão

A Proposta B mantém o grafo episódico do HeLa-Mem intacto e reformula a memória semântica. O código está em [src/modeling/temporal_knowledge_memory.py](../src/modeling/temporal_knowledge_memory.py) e [src/modeling/validity_aware_retriever.py](../src/modeling/validity_aware_retriever.py). São cinco mudanças.

### 7.1 Extração ancorada na sessão

Em vez de extrair fatos a cada 10 turnos, o que mistura sessões de datas diferentes, os turnos são agrupados **por sessão**, e cada fato recebe a **data real da sessão** (`haystack_dates`).

Sem isso, nenhuma das outras mudanças funciona: não dá para dizer que um fato substituiu outro sem saber qual veio antes. Esta mudança, que parecia um pré-requisito técnico, acabou sendo responsável pela maior parte do ganho total (Seção 10.2).

### 7.2 Representação de um fato

Cada fato passa a ter:

| Campo | Significado | Exemplo (`a2f3aa27`) |
|---|---|---|
| conteúdo | o texto do fato | "User has 1250 followers on Instagram" |
| embedding | vetor normalizado (Seção 3.2) | 384 números |
| `valid_from` (t_start) | data da sessão em que o fato foi observado | 2023/05/28 06:23 |
| `valid_to` (t_end) | data em que foi substituído (vazio enquanto ativo) | 2023/05/28 14:10 |
| `status` | `active` ou `superseded` | `superseded` |
| `superseded_by` / `supersedes` | ponteiros para o fato que o substituiu ou que ele substituiu | substituído pelo fato #5 |
| arestas | ligações hebbianas no grafo semântico | cadeia, EXTENDS, SUPERSEDES |

### 7.3 Supersessão: como um fato novo substitui um antigo

Quando um fato novo chega de uma sessão em `t_event`, o sistema decide se ele substitui algum fato existente.

**Passo 1 — Candidatos.** São considerados apenas fatos que:

- ainda estão **ativos**;
- vieram de uma **sessão anterior**, porque fatos da mesma conversa costumam se complementar, não se substituir;
- têm similaridade de cosseno ≥ **θ = 0,35** com o fato novo, ou seja, falam de assunto parecido.

**Passo 2 — Classificação.** Os 4 candidatos mais parecidos passam, um a um, por um **classificador LLM** que recebe os dois fatos com suas datas e escolhe um rótulo:

| Rótulo | Quando | O que acontece |
|---|---|---|
| **UNRELATED** | Assuntos diferentes, apesar de parecidos | Nada |
| **EXTENDS** | O novo complementa o antigo e os dois continuam verdadeiros | A ligação entre eles é reforçada (+η) |
| **SUPERSEDES** | O novo muda o estado descrito pelo antigo | O antigo recebe `valid_to = t_event` e status `superseded`; cria-se uma aresta forte (peso 0,8, nos dois sentidos) entre eles |

**Exemplos.** O primeiro é real (questão `a2f3aa27`); os outros dois ilustram o padrão.

- Antigo (manhã): "User has 1250 followers on Instagram". Novo (tarde): "User is nearing 1300 followers on Instagram". → **SUPERSEDES**: o número de seguidores mudou.
- Antigo: "o usuário adotou um gato". Novo: "o gato do usuário se chama Luna". → **EXTENDS**: as duas coisas continuam verdadeiras.
- Antigo: "o usuário montou um aquário". Novo: "o usuário montou outro aquário para o filho de um amigo". → deveria ser **EXTENDS**, porque agora são dois aquários. Em casos reais desse tipo (como a questão `46a3abf7`) o classificador escolheu **SUPERSEDES**, que é a principal fonte de erro da proposta (Seção 10.5).

O fato antigo **nunca é apagado** (Seção 3.10).

### 7.4 Busca ponderada pela validade

Na pergunta, feita em `t_query`, cada fato recebe uma **pertinência temporal 𝒱**, um número de 0 a 1:

| Situação do fato na data da pergunta | 𝒱 |
|---|---|
| válido (`t_start ≤ t_query`, sem `t_end` ou com `t_end ≥ t_query`) | 1 |
| expirado (`t_query > t_end`) | exp(−(t_query − t_end) / τ), com τ = 60 dias |
| ainda não existia (`t_query < t_start`) | 0 |

O decaimento exponencial é **suave**: um fato substituído há 30 dias ainda tem 𝒱 = e^(−0,5) ≈ 0,61; há 60 dias, ≈ 0,37. Ele perde força aos poucos, em vez de desaparecer, porque a pergunta pode ser sobre o passado.

O score de cada fato combina similaridade e validade:

```text
score = λ × similaridade reescalada + (1 − λ) × 𝒱 + espalhamento,   com λ = 0,6
```

**Exemplo numérico.** Um fato antigo tem cosseno 0,70 com a pergunta (reescalado: 0,85); o fato novo tem cosseno 0,56 (reescalado: 0,78). O antigo é mais parecido com a pergunta.

| Dias entre a substituição e a pergunta | 𝒱 do antigo | Score do antigo | Score do novo | Quem fica na frente |
|---:|---:|---:|---:|---|
| 0 | 1,00 | 0,910 | 0,868 | antigo |
| 7 | 0,89 | 0,866 | 0,868 | empate (cruzamento ≈ 6,7 dias) |
| 30 | 0,61 | 0,753 | 0,868 | **novo** |
| 60 | 0,37 | 0,657 | 0,868 | **novo** |

O score do antigo é 0,6 × 0,85 + 0,4 × 𝒱; o do novo é 0,6 × 0,78 + 0,4 × 1.

Duas consequências:

- logo depois da substituição, um fato antigo bem mais parecido com a pergunta **ainda pode ficar na frente**: o mecanismo de score sozinho só inverte o ranking depois de alguns dias;
- como são recuperados 5 fatos de uma média de 9 por questão, o fato antigo frequentemente **continua entre os recuperados**, só que com a etiqueta de histórico. Por isso as **etiquetas** (próxima subseção) podem ser tão importantes quanto o score.

### 7.5 Etiquetas no prompt

Os fatos recuperados entram no prompt com uma etiqueta de estado:

```text
[CURRENT / ACTIVE (Valid since: 2023/05/28 14:10)] User is nearing 1300 followers on Instagram.
[HISTORICAL / SUPERSEDED (Valid: 2023/05/28 06:23 to 2023/05/28 14:10)] User has 1250 followers on Instagram.
```

O prompt de sistema instrui o modelo a usar o estado `CURRENT` em perguntas sobre o presente e o `HISTORICAL` em perguntas sobre o passado ("onde eu morava antes?"). Com essas etiquetas, o modelo respondeu "1300 followers" no exemplo da Seção 5.3.

### 7.6 Hiperparâmetros

| Parâmetro | Valor | O que controla |
|---|---|---|
| λ | 0,6 | Peso da similaridade versus validade no score |
| τ | 60 dias | Velocidade com que um fato expirado perde força |
| θ | 0,35 | Similaridade mínima para considerar uma possível substituição |
| candidatos por fato | 4 | Quantos fatos antigos vão ao classificador |
| peso da aresta SUPERSEDES | 0,8 | Força da ligação entre a versão antiga e a nova |

Esses valores foram fixados antes da avaliação completa e **não foram ajustados** com base nos resultados. Os demais parâmetros (top_k = 15 episódico, semantic_top_k = 5, α = 0,1, η = 0,02, `gpt-4o-mini`) são os mesmos da baseline.

---

## 8. Dados, métricas e desenho experimental

### 8.1 O benchmark LongMemEval

O **LongMemEval** (ICLR 2025) foi criado para testar memória de longo prazo em assistentes conversacionais. Cada questão traz:

- um **histórico** de sessões de conversa entre usuário e assistente, cada uma com data;
- uma **pergunta**, feita numa data posterior (`question_date`);
- o **gabarito**;
- uma **categoria**.

Existem três variantes oficiais:

| Variante | Histórico por questão | O que testa |
|---|---|---|
| `longmemeval_s` | ~40 sessões (~115 mil tokens), incluindo **sessões de distração** | Encontrar a informação no meio do ruído e raciocinar sobre ela |
| `longmemeval_m` | ~500 sessões | Idem, em escala maior |
| `longmemeval_oracle` | **Apenas as sessões de evidência** (as que contêm a resposta) | Raciocinar sobre a informação, sem precisar encontrá-la |

### 8.2 Os dados usados neste projeto

São 500 questões do arquivo `data/longmemeval_s.json` que vem com o código do HeLa-Mem, distribuídas em 6 categorias:

| Categoria | Questões | O que testa | Exemplo |
|---|---:|---|---|
| `temporal-reasoning` | 133 | Datas, durações e ordem de eventos | "Qual foi o primeiro problema do meu carro depois da revisão?" |
| `multi-session` | 133 | Combinar informações de várias sessões, com contagens e somas | "Quantos aquários eu tenho?" |
| `knowledge-update` | 78 | Responder com o estado mais recente de algo que mudou | "Quantos seguidores eu tenho agora?" |
| `single-session-user` | 70 | Lembrar algo que o usuário disse | "Onde usei o cupom?" |
| `single-session-assistant` | 56 | Lembrar algo que o assistente disse | "Qual era aquele restaurante em Cihampelas Walk que você me indicou?" |
| `single-session-preference` | 30 | Usar preferências do usuário para personalizar a resposta | "Pode me sugerir um hotel para minha viagem a Miami?" |

29 questões são de **abstenção** (IDs com `_abs`): a resposta certa é dizer que a informação não existe na conversa.

> **Atenção — apesar do nome, o arquivo não é o LongMemEval-S.** Verificou-se que, nas 500 questões, o histórico contém **apenas as sessões de evidência** (1 a 6 sessões; média de 1,0 nas categorias de sessão única e de 2,0 a 2,6 nas demais). Ou seja, ele corresponde à variante *oracle*. Consequências:
> - o experimento testa **raciocinar sobre fatos que mudam**, que é o foco da proposta, mas **não** testa encontrar esses fatos no meio de dezenas de sessões irrelevantes;
> - nas categorias de sessão única há uma só sessão, então a supersessão é impossível por construção;
> - **o próprio repositório do HeLa-Mem chama este arquivo de "the complete 500-item LongMemEval-S file"**. O artigo (Apêndice D) não informa o tamanho do histórico e copia os baselines do LightMem, que os mediu no LongMemEval-S verdadeiro (cerca de 115 mil tokens por questão). Não se sabe com qual arquivo o HeLa-Mem obteve os 65,40%. Se foi com este, o artigo compara oracle com S. Se não foi, a nossa reprodução mede outra coisa. **Em qualquer caso, a comparação numérica com o artigo não vale.** A comparação interna A → B0 → B continua válida (Achado 10 da auditoria, atualizado em 05/11).

### 8.3 Métrica

A métrica é a **acurácia** (fração de questões respondidas corretamente), julgada por LLM com o prompt oficial do LongMemEval (Seção 3.11). O juiz é o mesmo `gpt-4o-mini` que gera as respostas, com `temperature=0.7` (Seção 3.12).

### 8.4 Desenho experimental

- **Pareamento:** as três condições respondem às mesmas 500 questões, e a comparação é questão a questão (Seção 3.14).
- **Mesmos grafos episódicos:** B e B0 reutilizam exatamente os grafos episódicos gerados por A (`--reuse_episodic_dir`). A diferença entre as condições está só na memória semântica e no prompt.
- **Ablação B0** (Seção 3.13): usa **os mesmos fatos** de B, mas:
  - trata todos como ativos (𝒱 = 1);
  - descarta as arestas criadas pelo classificador e mantém só a cadeia padrão do HeLa-Mem;
  - usa o prompt original do HeLa-Mem, sem etiquetas.

  A B0 só reavalia, sem extrair os fatos de novo. Isso garante que B e B0 tenham exatamente o mesmo conteúdo semântico.

| Diferença entre | A | B0 | B |
|---|---|---|---|
| Grafos episódicos | originais | iguais a A | iguais a A |
| Extração de fatos | blocos de 10 turnos | **por sessão** | por sessão (iguais a B0) |
| Validade e supersessão | não | não | **sim** |
| Score com 𝒱 | não | não (𝒱 = 1) | **sim** |
| Etiquetas no prompt | não | não | **sim** |

### 8.5 Estatística

- **Teste exato de McNemar** (Seção 3.14), bilateral.
- **Intervalo de confiança de 95%** pareado (Seção 3.15).
- **Correção de Holm** (Seção 3.16) nas 12 comparações por categoria.

---

## 9. Linha do tempo da execução

### 9.1 Reprodução da baseline (A)

O código oficial foi executado sem alterações (commit `68f19b3`, verificado) sobre as 500 questões e obteve **61,20%**, 4,2 p.p. abaixo do valor reportado no artigo (65,40%).

Dois problemas foram descobertos depois, na auditoria:

- o módulo foi chamado diretamente, sem os scripts `.sh` oficiais, e dois hiperparâmetros ficaram com os valores padrão do código: `MAX_FLIPPED` = 5 (o script usa 3) e `KEYWORD_WEIGHT` = 0,5 (o script usa 0,7);
- **360 dos 500 grafos semânticos ficaram vazios.** O extrator oficial engole exceções silenciosamente, e não há logs dessa execução, então ainda não se sabe se isso é comportamento do código ou falha de execução.

### 9.2 Proposta B: duas rodadas

A execução foi incremental (100, 200, 300, 400 e 500 itens, relatórios `R04_*`).

- **1ª rodada completa: 64,60%.** As questões nas posições 100–199 do arquivo (todas as 78 de *Knowledge Update* e 22 de *Multi-Session*) ficaram com grafo semântico vazio. A causa foi uma condição de corrida (*race condition*): várias threads tentaram carregar o modelo de embeddings ao mesmo tempo, e a falha foi engolida em silêncio.
- **Correção e 2ª rodada: 65,60%.** O modelo passou a ser carregado uma vez, antes de iniciar a execução paralela, e essas 100 questões foram recodificadas. O critério foi objetivo (grafo vazio) e independente de acerto. Nenhuma questão fora desse lote mudou de resultado. Todo o ganho em *Knowledge Update* (57 → 65) surgiu nessa segunda rodada.

### 9.3 Draft 2

Relatório da terceira entrega com 65,60%, figuras em padrão IEEE e análise qualitativa. Na versão original, o ganho era atribuído inteiramente ao mecanismo temporal, e a afirmação de "superar o artigo" era feita com base em 0,2 p.p.

### 9.4 Auditoria, ablação e revisão (04/11/2026)

- **Auditoria R05:** dez achados sobre o processo (Seção 12).
- **Ablação B0:** implementada e executada, com 64,20%.
- **Revisão do Draft 2:** a conclusão passou de "a proposta supera o artigo" para "hipótese suportada em KU, não no total". Também foram corrigidos a descrição do dataset, a comparação com o artigo, as figuras e os casos qualitativos.
- **Revisão dos notebooks:** o notebook 01 foi corrigido e o 02 virou um passo a passo completo da análise.

---

## 10. Resultados

### 10.1 Acurácia por categoria

| Categoria | N | Artigo | A | B0 | B | Δ(B0−A) | Δ(B−B0) |
|---|---:|---:|---:|---:|---:|---:|---:|
| knowledge-update | 78 | 78,21% | 57 (73,08%) | 51 (65,38%) | **65 (83,33%)** | −7,69 | **+17,95** |
| temporal-reasoning | 133 | 50,38% | 69 (51,88%) | **76 (57,14%)** | 74 (55,64%) | +5,26 | −1,50 |
| multi-session | 133 | 57,14% | 62 (46,62%) | **72 (54,14%)** | 65 (48,87%) | +7,52 | −5,26 |
| single-session-preference | 30 | — | 8 (26,67%) | 12 (40,00%) | **14 (46,67%)** | +13,33 | +6,67 |
| single-session-assistant | 56 | — | 49 (87,50%) | 50 (89,29%) | **52 (92,86%)** | +1,79 | +3,57 |
| single-session-user | 70 | — | **61 (87,14%)** | 60 (85,71%) | 58 (82,86%) | −1,43 | −2,86 |
| **Total** | **500** | **65,40%** | **306 (61,20%)** | **321 (64,20%)** | **328 (65,60%)** | **+3,00** | **+1,40** |

As colunas Δ estão em pontos percentuais (p.p.): a diferença simples entre duas porcentagens. O artigo reporta as três categorias de sessão única **agregadas** (78,85%). No agregado (n = 156): A = 75,64%, B0 = 78,21%, B = 79,49%.

**Como ler a tabela:**

- **coluna Δ(B0−A):** o que a extração por sessão fez **sozinha**. Ajudou em quase tudo, **exceto** em *Knowledge Update*, onde piorou;
- **coluna Δ(B−B0):** o que o mecanismo temporal fez **sozinho**. Ajudou muito em *Knowledge Update* e atrapalhou em *Multi-Session*.

### 10.2 Decomposição do ganho e significância

| Comparação | Ganhos / Regressões | Δ (p.p.) | IC 95% | p (bilateral) |
|---|---|---:|---|---:|
| A → B0 (extração por sessão) | +47 / −32 | +3,00 | [−0,47; 6,47] | 0,115 |
| B0 → B (mecanismo temporal) | +35 / −28 | +1,40 | [−1,71; 4,51] | 0,450 |
| A → B (total) | +54 / −32 | +4,40 | [0,79; 8,01] | 0,023 |

Só o efeito combinado é significativo no total. Nenhuma etapa isolada atinge significância global, porque seus efeitos se concentram em categorias específicas e **em sentidos opostos**: o mecanismo temporal ganha em KU e perde em Multi-Session, e no total os dois se cancelam.

Por categoria, após a correção de Holm, **apenas uma diferença é significativa**: Knowledge Update em B0 → B, com +14/−0 e p_Holm = 0,0015.

### 10.3 Estrutura dos grafos temporais

- 4.591 fatos extraídos (média de 9,18 por questão); **612 (13,33%)** foram substituídos, em **249 diálogos** (49,8%).
- Em `knowledge-update`, 72 de 78 diálogos tiveram supersessão (20,41% dos fatos substituídos); em `multi-session`, 105/133; em `temporal-reasoning`, 72/133.
- Nas categorias de sessão única não há supersessão. Isso acontece **por construção** (uma só sessão, logo uma só data), não é uma medida de precisão do classificador.
- **Onde o mecanismo agiu:** os 14 ganhos B0 → B em KU estão **todos** em diálogos com supersessão. Das 14 regressões B0 → B em *Multi-Session*, **12** também estão. Isso liga os dois efeitos diretamente à supersessão, e não a outra diferença entre B0 e B.

### 10.4 Análise qualitativa

Comparar as três condições mostra qual componente resolveu cada caso.

**Casos resolvidos pela extração (B0 já acerta):**

- `852ce960`: a pré-aprovação de financiamento passou de $350.000 para $400.000. A responde $350.000, enquanto B0 e B respondem $400.000. Com os fatos extraídos por sessão, o modelo já escolheu o valor certo, mesmo sem etiquetas.
- `50635ada`: "qual era meu status anterior no programa de milhas?". A responde "None", enquanto B0 e B respondem "Premier Silver".

**Casos resolvidos pelo mecanismo temporal (B0 erra, B acerta):**

| Questão | A | B0 | B | O que aconteceu |
|---|---|---|---|---|
| `a2f3aa27` "Quantos seguidores tenho agora?" (1.300) | 1250 ✗ | 1250 ✗ | 1300 ✓ | O fato de 1.250 foi marcado como substituído pelo de 1.300 |
| `01493427` "Quantos cartões-postais adicionei desde que voltei a colecionar?" (25) | 25 ✓ | **42** ✗ | 25 ✓ | Sem validade, a B0 somou o valor antigo ao atual (17 + 25) |
| `b6019101` "Quantos filmes da Marvel assisti?" (5) | 4 ✗ | 4 ✗ | 5 ✓ | Mesmo padrão do primeiro caso |

O caso `01493427` mostra um fenômeno importante. A baseline A, que não tinha fatos semânticos para essa questão, acertava a partir dos trechos episódicos. A B0 recebeu dois fatos ("adicionou 17 postais" em agosto e "adicionou 25 desde que voltou a colecionar" em novembro) sem saber que o segundo atualiza o primeiro, e os somou. Em **8 dos 14 ganhos B0 → B em KU**, a baseline A também acertava. Ou seja, **mais fatos sem noção de validade atrapalham**, e o mecanismo temporal desfaz esse dano. É por isso que B0 acerta *menos* que A em KU (51 contra 57).

**Caso em que todos erram:** em `07741c45` (os tênis), A e B0 respondem "debaixo da cama". B responde "numa sapateira", que é o estado certo, mas o extrator resumiu o fato sem "no armário" e o juiz exigiu o detalhe. O caso separa erro de memória temporal (corrigido) de compressão na extração (não corrigida).

**Ganhos possivelmente ruidosos:** em `c6853660`, B0 respondeu "increase" (reprovado) e B respondeu "increased" (aprovado). Isso sugere variação do juiz.

### 10.5 Regressões

- **Supersessão excessiva em contagens (*Multi-Session*):** "quantos aquários eu tenho?" (gabarito 3, B respondeu 2) e "a quantos jantares fui no último mês?" (gabarito 3, B respondeu 2). Eventos repetidos em datas diferentes foram classificados como SUPERSEDES em vez de EXTENDS. O modelo então tratou o evento antigo como "não vale mais" e deixou de contá-lo. Uma causa provável é o próprio prompt do classificador, que manda tratar como substituição qualquer fato que estabeleça "um novo estado", "mesmo se formulado como plano". Para perguntas de contagem, o certo seria EXTENDS.
- **Formato da resposta:** "quanto gastei com lavagem e estacionamento?" (gabarito $65). B listou "$15, $50" em vez de somar.
- **Excesso de contexto em *Single-Session User*:** os fatos adicionais desviaram o modelo de detalhes que só estavam no diálogo bruto. Por exemplo, ele respondeu onde um cupom foi **recebido** ("email inbox") em vez de onde foi **usado** ("Target").

---

## 11. Interpretação: o que os resultados dizem sobre a hipótese

| Pergunta | Resposta | Grau de certeza |
|---|---|---|
| B é melhor que A, como executado? | Sim, +22 questões | Evidência moderada (ruído entre execuções não medido) |
| O ganho total vem do mecanismo temporal? | **Não.** Vem principalmente da extração por sessão | Evidência moderada |
| O mecanismo temporal ajuda em atualização de conhecimento? | **Sim.** +14/−0, todas com supersessão | Evidência forte |
| O mecanismo temporal tem custo? | Sim, em contagens multi-sessão (−7) | Evidência moderada |
| A supersessão não-destrutiva ajuda em perguntas sobre o passado? | **Não determinado.** O único caso observado também é resolvido pela B0 | — |
| O ganho vem do score com 𝒱 ou das etiquetas no prompt? | **Não determinado.** A B0 remove os dois ao mesmo tempo | — |
| B supera o artigo original? | Não é possível afirmar | Configuração e dados possivelmente diferentes |

Em uma frase: **a validade temporal resolve o problema que se propôs a resolver (fatos desatualizados), mas o classificador de supersessão é agressivo demais e cria um problema novo em perguntas de contagem, que anula o ganho no total.**

O resultado é mais informativo do que o "+4,40 p.p." original. Ele mostra **onde** o mecanismo funciona, **por que** falha onde falha, e aponta uma correção concreta. Também traz um achado que não estava previsto: **extrair mais fatos sem noção de validade pode piorar um sistema de memória**, como mostra a queda de A para B0 em KU.

---

## 12. Auditoria do processo e limitações conhecidas

A auditoria completa está em [reports/analysis/R05_auditoria_processo_20261104.md](../reports/analysis/R05_auditoria_processo_20261104.md). Os achados 1 e 3 podem ser reproduzidos sem API com `python src/analysis/audit_process.py`.

| # | Achado | Situação |
|---|---|---|
| 1 | A baseline rodou com `MAX_FLIPPED` = 5 e `KEYWORD_WEIGHT` = 0,5, contra 3 e 0,7 nos scripts oficiais | Documentado no relatório; neutro para A × B |
| 2 | 360/500 grafos semânticos vazios em A; comprovada falha de execução por concorrência (item 400 extraiu 9 nós com workers=1) | **Resolvido em 05/11:** baseline A estava subestimada; construção da Baseline Fiel ($A^*$) em andamento |
| 3 | A recodificação dos itens 100–199 (64,60% → 65,60%) não estava documentada | Documentada no Draft 2 e no notebook 02 |
| 4 | Fatores de confusão entre A e B | **Resolvido** pela ablação B0 e validado na Proposta $B_{\text{v2}}$ (sem exemplos de prompt) |
| 5 | `temperature=0.7` na geração e no juiz, sem repetições | **Resolvido em 05/11:** piso de ruído medido com $B'$ (7,20% de discordância geral; KU com 97,4% de estabilidade, idêntico em 83,33%) |
| 6 | Faltavam IC, tamanho de efeito e correção para múltiplas comparações | **Resolvido** (IC 95%, Holm) |
| 7 | Risco de ajustar hiperparâmetros no conjunto de teste | Regra fixada: sensibilidade sem seleção |
| 8 | Só um dataset (a diretriz pede mais de um) | Pendente (LoCoMo planejado) |
| 9 | Reprodutibilidade (requirements desatualizado, `tests/` vazio, semântica de A não versionada) | Parcialmente pendente |
| 10 | O arquivo de dados só tem as sessões de evidência (variante *oracle*) | Fontes verificadas em 05/11: o README do HeLa-Mem chama o arquivo de LongMemEval-S, mas os baselines do artigo são do S de cerca de 115 mil tokens; falta perguntar aos autores e avaliar no S oficial |

**Por que o Achado 2 importa tanto.** Se os 360 grafos vazios forem falha de execução, a baseline A ficou artificialmente fraca, porque respondeu sem a memória semântica em 72% das questões. Nesse caso:

- a comparação com o artigo (61,20% contra 65,40%) seria explicada, ao menos em parte, por essa falha;
- parte do ganho A → B0 seria "fazer a extração funcionar", e não "extrair por sessão".

**A ablação B0 não resolve isso.** Ela isola o mecanismo temporal (B0 → B), mas não diz como seria uma baseline sem falhas.

Outras limitações:

- **o juiz é o mesmo modelo que gera as respostas** (`gpt-4o-mini`);
- **as etiquetas e a reordenação por 𝒱 ainda estão acopladas** (Seção 11);
- **a precisão do classificador de supersessão não foi medida diretamente:** isso exigiria uma amostra de supersessões rotuladas à mão.

---

## 13. Próximos passos

O plano completo, com comandos e critérios de conclusão, está em [docs/plano_resolucao_R05.md](plano_resolucao_R05.md). Em ordem de prioridade:

| Prioridade | Passo | Por quê | Custo |
|---|---|---|---|
| 1 | **Ajustar o classificador** para separar estados que se excluem (SUPERSEDES) de eventos que se acumulam (EXTENDS) | É a causa medida das regressões em *Multi-Session* | Médio (recodificar a semântica) |
| 2 | **Rodar B'** (repetir B) | Saber quanto das diferenças é ruído do juiz (Seção 3.12) | Baixo |
| 3 | **Investigar os 360 grafos vazios de A:** recuperar os arquivos originais ou recodificar 20 itens com `--workers 1` | Se for falha, a baseline está subestimada e precisa ser refeita (A*) | Baixo; alto se precisar de A* |
| 4 | **Separar etiquetas de 𝒱:** variantes "só etiquetas" e "só 𝒱" | Saber qual componente produz o ganho em KU | Baixo |
| 5 | **Sensibilidade de λ, τ e θ**, reportada sem escolher a configuração pelo resultado | Classificar o resultado como robusto ou sensível | Médio |
| 6 | **Avaliação no LongMemEval-S completo** (~40 sessões por questão), começando por uma amostra | Testar o mecanismo em meio a sessões de distração | Alto |
| 7 | **LoCoMo**, o segundo dataset do artigo-base | Atender à diretriz de mais de um dataset | Alto |
| 8 | **Precisão do classificador** numa amostra rotulada à mão | Medir diretamente erros de supersessão | Baixo (manual) |
| 9 | **Higiene:** `requirements.txt`, testes, versionar a semântica de A, mover o legado do GraphSAGE | Reprodutibilidade | Baixo |

**Uma ideia concreta para o passo 1.** Acrescentar ao prompt do classificador a distinção explícita entre:

- **atributos de estado único**, que são substituídos: endereço, emprego, número atual de seguidores, onde algo está guardado;
- **eventos contáveis**, que se acumulam: compras, visitas, jantares, aquários montados, cursos concluídos.

O critério de sucesso, definido antes de rodar, seria: recuperar as regressões de *Multi-Session* sem perder os 14 ganhos de *Knowledge Update*.

O relatório [reports/relatorio_entrega2_draft2.md](../reports/relatorio_entrega2_draft2.md) também está desatualizado em relação à versão LaTeX e precisa ser sincronizado.

---

## 14. Mapa do repositório e como reproduzir

### 14.1 Estrutura

```text
mestrado-dl-projeto/
├── README.md                       # Evolução da proposta (de onde veio a ideia)
├── AGENT.MD                        # Regras de análise seguidas no projeto
├── docs/
│   ├── VISAO_GERAL_PROJETO.md      # Este documento
│   ├── projeto_diretrizes.md       # Diretrizes da disciplina
│   ├── proposta_doc.md             # Proposta submetida
│   ├── plano_resolucao_R05.md      # Plano de correção (passo a passo, com status)
│   └── Artigos/                    # Resumos dos artigos considerados
├── external/HeLa-Mem/              # Submódulo: código oficial (commit 68f19b3)
├── src/
│   ├── modeling/
│   │   ├── temporal_knowledge_memory.py   # Memória semântica com validade e supersessão (+ modo B0)
│   │   ├── validity_aware_retriever.py    # Busca com 𝒱 e prompt com etiquetas (+ modo B0)
│   │   └── sage_*.py, reproduce_ppi.py    # Legado da Fase 1 (GraphSAGE)
│   ├── analysis/
│   │   ├── run_hela_longmemeval.py        # Execução da Baseline A
│   │   ├── run_temporal_hela_longmemeval.py  # Execução de B e B0 (--ablation, --results_subdir)
│   │   ├── compare_ablation.py            # Tabelas A/B0/B, McNemar, subconjuntos
│   │   └── audit_process.py               # Auditoria reproduzível (sem API)
│   └── visualization/generate_report_figures.py  # Figuras do artigo
├── notebooks/
│   ├── 01_replicacao_baseline_hela_mem.ipynb   # Reprodução da baseline
│   └── 02_execucao_proposta_temporal.ipynb     # Passo a passo: B, B0, estatística, casos, figuras
├── results/
│   ├── baseline_episodic_500.zip   # Grafos episódicos de A
│   ├── temporal_encoded_500.zip    # Grafos e resultados de B
│   ├── longmemeval_baseline_full/eval_results/eval_summary.json      # A
│   └── longmemeval_temporal_full/eval_results{,_b0}/eval_summary.json # B e B0
├── reports/
│   ├── relatorio_entrega2_draft2_ieee.tex   # Draft 2 (versão de referência)
│   ├── overleaf_entrega2_draft2.zip         # Pacote para o Overleaf
│   ├── figures/                             # fig1–fig5 (PNG e PDF)
│   └── analysis/                            # Registros R01–R05
└── outras-ideias (desconsiderar)/           # Material da Fase 1, fora do escopo
```

### 14.2 Reproduzir a análise (sem chave de API)

Todos os resultados estão versionados. Para refazer tabelas, estatística, casos e figuras:

```bash
git clone --recurse-submodules https://github.com/ataidefilipe/mestrado-dl-projeto.git
```

```bash
pip install numpy pandas matplotlib python-dotenv nbclient ipykernel networkx
```

Depois, abra e execute `notebooks/02_execucao_proposta_temporal.ipynb`. Ele descompacta os resultados e roda todos os passos. Pela linha de comando:

```bash
python src/analysis/compare_ablation.py
```

```bash
python src/analysis/audit_process.py
```

### 14.3 Reexecutar os experimentos (com chave de API)

Crie um arquivo `.env` na raiz com `OPENAI_API_KEY=...` e instale `sentence-transformers`, `torch` e `openai`. Então:

```bash
python src/analysis/run_temporal_hela_longmemeval.py --stage eval --ablation no_temporal --results_subdir eval_results_b0 --num_items 500
```

```bash
python src/analysis/run_temporal_hela_longmemeval.py --stage eval --results_subdir eval_results_b_rerun --num_items 500
```

O primeiro comando refaz a B0; o segundo é a repetição B' para medir ruído. O padrão de `--num_items` é 10, então informe 500 explicitamente. Cada avaliação completa faz cerca de 1.500 chamadas ao `gpt-4o-mini`.

---

## 15. Glossário

| Termo | Significado | Onde é explicado |
|---|---|---|
| **LLM** | Modelo de linguagem que gera texto a partir de um prompt | 3.1 |
| **Janela de contexto** | Quantidade máxima de texto que o LLM consegue ler de uma vez | 3.1 |
| **Agente** | Sistema baseado em LLM que interage com o usuário ao longo do tempo | 3.1 |
| **Embedding** | Vetor de números que representa o significado de um texto | 3.2 |
| **Similaridade de cosseno** | Medida de quão parecidos são dois embeddings (−1 a 1; reescalada para 0 a 1) | 3.2 |
| **RAG** | Buscar trechos relevantes e colocá-los no prompt antes de gerar a resposta | 3.3 |
| **Top-k** | Os k itens mais bem pontuados numa busca | 3.3 |
| **Grafo / nó / aresta / peso** | Estrutura de pontos ligados; o peso indica a força da ligação | 3.4 |
| **Aprendizado hebbiano** | Memórias usadas juntas têm a ligação reforçada | 3.5 |
| **η (taxa de aprendizado)** | Reforço aplicado a cada uso conjunto (0,02) | 3.5 |
| **Ativação espalhada** | Um nó relevante passa parte da relevância aos vizinhos | 3.6 |
| **Memória episódica** | Trechos de conversa com data | 3.7 |
| **Memória semântica** | Fatos condensados extraídos das conversas | 3.7 |
| **Recência / saliência / validade** | Quão novo / quão importante / se ainda é verdade | 3.9 |
| **Grafo de conhecimento temporal** | Grafo em que cada fato tem um período de validade | 3.10 |
| **Supersessão** | Um fato novo encerra a validade de um antigo, sem apagá-lo | 3.10, 7.3 |
| **SUPERSEDES / EXTENDS / UNRELATED** | Rótulos do classificador: substitui / complementa / não tem relação | 7.3 |
| **Pertinência temporal 𝒱** | Peso de 0 a 1 que indica quanto um fato é válido na data da pergunta | 7.4 |
| **λ, τ, θ** | Peso da similaridade; velocidade do decaimento; limiar de similaridade para supersessão | 7.6 |
| **LLM-as-a-judge** | Um LLM decide se a resposta gerada está correta, comparando com o gabarito | 3.11 |
| **Temperatura** | Quanto o LLM sorteia entre respostas possíveis | 3.12 |
| **Fator de confusão** | Duas mudanças simultâneas que impedem saber qual causou o efeito | 3.13 |
| **Ablação** | Remover um componente para medir o efeito dele | 3.13 |
| **Baseline A** | HeLa-Mem original, reproduzido | 8.4 |
| **Proposta B** | HeLa-Mem com validade temporal e supersessão | 7 |
| **Ablação B0** | B sem o mecanismo temporal, usada para isolar o efeito dele | 8.4 |
| **B' / A\*** | Repetição de B (medir ruído) e baseline refeita com os scripts oficiais (se necessário) | 13 |
| **Avaliação pareada** | Comparar sistemas questão a questão nas mesmas questões | 3.14 |
| **McNemar** | Teste que compara dois sistemas olhando só as questões em que discordam | 3.14 |
| **p-valor** | Chance de ver um resultado tão extremo se não houvesse efeito | 3.15 |
| **IC 95%** | Faixa de valores plausíveis para o tamanho do efeito | 3.15 |
| **p.p. (pontos percentuais)** | Diferença simples entre duas porcentagens (65,6% − 61,2% = 4,4 p.p.) | 10.1 |
| **Correção de Holm** | Ajuste dos p-valores quando se fazem vários testes | 3.16 |
| **Taxa de base** | Proporção esperada, usada como referência para dizer se algo está concentrado | 3.17 |
| **Variante oracle** | Versão do LongMemEval com apenas as sessões que contêm a resposta | 8.1 |
| **KU / TR / MS** | Knowledge Update / Temporal Reasoning / Multi-Session | 8.2 |
| **Condição de corrida** | Erro que ocorre quando várias threads acessam o mesmo recurso ao mesmo tempo | 9.2 |

---

## 16. Documentos de referência

| Documento | Conteúdo |
|---|---|
| [README.md](../README.md) | Narrativa completa de como a proposta foi construída (GraphRAG → A-MEM → HeLa-Mem → Zep) |
| [docs/projeto_diretrizes.md](projeto_diretrizes.md) | Diretrizes da disciplina |
| [docs/proposta_doc.md](proposta_doc.md) | Proposta formal submetida |
| [reports/relatorio_entrega1_enxuto.md](../reports/relatorio_entrega1_enxuto.md) | Entrega 1: reprodução e diagnóstico |
| [reports/relatorio_entrega2_draft2_ieee.tex](../reports/relatorio_entrega2_draft2_ieee.tex) | Draft 2 (versão atual, revisada) |
| [reports/analysis/R05_auditoria_processo_20261104.md](../reports/analysis/R05_auditoria_processo_20261104.md) | Auditoria do processo (10 achados) |
| [reports/analysis/R05_decomposicao_A_B0_B_20261104_205642.md](../reports/analysis/R05_decomposicao_A_B0_B_20261104_205642.md) | Resultados da ablação B0 |
| [docs/plano_resolucao_R05.md](plano_resolucao_R05.md) | Plano de correção com status por etapa |
| [notebooks/01_replicacao_baseline_hela_mem.ipynb](../notebooks/01_replicacao_baseline_hela_mem.ipynb) | Reprodução da baseline, executável |
| [notebooks/02_execucao_proposta_temporal.ipynb](../notebooks/02_execucao_proposta_temporal.ipynb) | Passo a passo executável de toda a análise |

**Artigos:**

- HeLa-Mem — Bro et al., ACL 2026 — [aclanthology.org/2026.acl-long.625](https://aclanthology.org/2026.acl-long.625) · código: [github.com/ReinerBRO/HeLa-Mem](https://github.com/ReinerBRO/HeLa-Mem)
- Zep — Chauhan et al., 2025 — [arXiv:2501.13956](https://arxiv.org/abs/2501.13956) · Graphiti: [github.com/getzep/graphiti](https://github.com/getzep/graphiti)
- LongMemEval — Wu et al., ICLR 2025 — [github.com/xiaowu0162/LongMemEval](https://github.com/xiaowu0162/LongMemEval)
- A-MEM — Xu et al., 2025 — [arXiv:2502.12110](https://arxiv.org/abs/2502.12110)
- GraphRAG — Edge et al., 2024 — [arXiv:2404.16130](https://arxiv.org/abs/2404.16130)
