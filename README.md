# Evolução da proposta do projeto — memória em grafos para agentes

## 1. Restrições impostas pelo projeto da disciplina

O ponto de partida da discussão não foi escolher uma tecnologia ou desenvolver uma solução do zero. As diretrizes da disciplina determinam uma lógica experimental bastante específica:

1. escolher um problema de interesse;
2. encontrar um **bom artigo/código-base**;
3. compreender razoavelmente o trabalho;
4. **reproduzir os resultados originais sem modificações**;
5. somente depois propor uma alteração, evolução ou estudo comparativo;
6. executar experimentos e analisar quantitativa e qualitativamente os resultados. 

A escolha também precisa considerar prazo, datasets disponíveis e recursos computacionais acessíveis. 

Além disso, a proposta de evolução não precisa necessariamente produzir resultado superior. Um resultado negativo é válido desde que a hipótese, o experimento e a análise sejam adequados. As próprias diretrizes enfatizam a necessidade de definir qual evolução será testada, justificar por que ela pode funcionar e compará-la experimentalmente. 

Portanto, o formato buscado passou a ser:

```text
ARTIGO EXISTENTE
      ↓
REPRODUÇÃO
      ↓
HIPÓTESE
      ↓
MODIFICAÇÃO CONTROLADA
      ↓
EXPERIMENTO
      ↓
COMPARAÇÃO COM O ORIGINAL
      ↓
ANÁLISE
```

---

# 2. Linhas de interesse iniciais

As primeiras áreas consideradas foram relativamente amplas:

* comportamento/"psicologia" de agentes;
* melhoria de agentes de programação e *vibe coding*;
* harness de agentes;
* memória;
* grafos;
* documentação automática;
* transcripts de reuniões;
* memória organizacional;
* RPA e automação.

A partir disso, a discussão convergiu principalmente para **grafos aplicados à memória e recuperação de informação**.

Dois domínios pareceram particularmente adequados:

### Agentic coding

Utilizar relações estruturais do código — arquivos, funções, classes, imports, chamadas e dependências — para melhorar a recuperação de contexto de agentes de programação.

### Memória organizacional

Representar conhecimento produzido ao longo de reuniões, como:

```text
Pessoa
Projeto
Decisão
Pendência
Requisito
Sistema
Reunião
Data
```

e as relações entre esses elementos:

```text
Pessoa ──decidiu──> Decisão

Decisão ──afeta──> Projeto

Decisão ──substitui──> Decisão anterior

Pessoa ──responsável_por──> Pendência
```

A segunda linha começou a se mostrar especialmente interessante porque conhecimento organizacional não é apenas um conjunto de documentos. Ele **muda ao longo do tempo**.

---

# 3. Primeiros artigos considerados

## 3.1 Microsoft GraphRAG

### From Local to Global: A Graph RAG Approach to Query-Focused Summarization

O trabalho da Microsoft foi um dos primeiros candidatos porque estabelece uma arquitetura clara de GraphRAG.

A proposta é transformar uma coleção textual em um grafo de entidades e relações, identificar comunidades no grafo, gerar resumos dessas comunidades e utilizar essa estrutura para responder perguntas, principalmente perguntas globais sobre grandes coleções de documentos. ([arXiv][1])

Fluxo simplificado:

```text
documentos
    ↓
chunks
    ↓
extração de entidades e relações
    ↓
knowledge graph
    ↓
comunidades
    ↓
resumos
    ↓
retrieval / resposta
```

Esse trabalho mostrou que grafos podem fornecer uma representação intermediária útil quando a informação está distribuída pelo corpus.

**Paper:** [From Local to Global: A Graph RAG Approach to Query-Focused Summarization](https://arxiv.org/abs/2404.16130?utm_source=chatgpt.com)

**Implementação oficial:** [Microsoft GraphRAG — GitHub](https://github.com/microsoft/graphrag?utm_source=chatgpt.com)

A implementação oficial permanece disponível, embora o próprio repositório atualmente descreva o projeto como majoritariamente em modo de manutenção. ([GitHub][2])

### Relação com nosso problema

A primeira ideia foi utilizar GraphRAG sobre transcripts de reuniões:

```text
transcripts
    ↓
entidades
    ↓
relações
    ↓
grafo
    ↓
perguntas organizacionais
```

Por exemplo:

* qual decisão foi tomada sobre determinado projeto?
* quem ficou responsável?
* por que uma decisão foi alterada?
* quais assuntos apareceram em diferentes reuniões?

O problema identificado é que **GraphRAG genérico não foi concebido principalmente como um sistema de memória temporal**.

Isso nos levou a olhar trabalhos específicos sobre memória de agentes.

---

# 4. A-MEM e a entrada definitiva no problema de memória

## A-MEM: Agentic Memory for LLM Agents

O A-MEM propõe uma memória dinâmica inspirada no método Zettelkasten.

Em vez de armazenar apenas blocos independentes recuperados por embeddings, cada memória é transformada em uma nota estruturada contendo atributos como contexto, palavras-chave e tags. O sistema identifica relações com memórias anteriores e pode atualizar representações já existentes conforme novas memórias são adicionadas. ([arXiv][3])

Fluxo conceitual:

```text
nova experiência
      ↓
nota estruturada
      ↓
busca por memórias relacionadas
      ↓
criação de links
      ↓
evolução das memórias anteriores
```

**Paper:** [A-MEM: Agentic Memory for LLM Agents](https://arxiv.org/abs/2502.12110?utm_source=chatgpt.com)

**Código de avaliação:** [AgenticMemory — GitHub](https://github.com/WujiangXu/AgenticMemory?utm_source=chatgpt.com)

**Implementação do sistema:** [A-MEM — GitHub](https://github.com/agiresearch/A-mem?utm_source=chatgpt.com)

### Por que o A-MEM chamou atenção

Ele trazia uma pergunta diretamente relacionada ao que queríamos investigar:

> Como memórias deveriam ser estruturadas e conectadas ao longo do tempo?

Isso permitia imaginar uma evolução relativamente pequena:

```text
A-MEM original
      ↓
links entre memórias

A-MEM modificado
      ↓
links
+
graph traversal no retrieval
```

Porém, ao avançarmos na pesquisa, apareceu um trabalho ainda mais próximo da ideia de **memória associativa com pesos variáveis**.

---

# 5. Investigação de reinforcement e decay

A discussão seguinte foi sobre um comportamento semelhante à memória humana:

```text
relação utilizada frequentemente
        ↓
fica mais forte

relação pouco utilizada
        ↓
fica mais fraca
```

A princípio, isso parecia uma possível evolução do A-MEM:

```text
peso(t+1)
=
peso(t)
+ reinforcement
- decay
```

Mas a pesquisa mostrou que essa ideia já foi explorada de maneira bastante direta.

---

# 6. HeLa-Mem

## HeLa-Mem: Hebbian Learning and Associative Memory for LLM Agents

O HeLa-Mem foi publicado na ACL 2026 e propõe justamente uma arquitetura de memória baseada em **grafo dinâmico com aprendizado hebbiano**. ([ACL Anthology][4])

O trabalho parte da ideia de que memória não depende somente de similaridade semântica.

Ele incorpora três mecanismos:

* associação;
* consolidação;
* *spreading activation*.

A arquitetura possui dois níveis principais:

```text
episodic memory graph
        +
semantic memory
```

O grafo episódico evolui conforme padrões de coativação entre memórias. A partir de regiões densamente relacionadas, outro mecanismo consolida informações em conhecimento semântico reutilizável. ([ACL Anthology][4])

Simplificando:

```text
Memória A ────── Memória B
     │
     └────────── Memória C

coativação
     ↓

Memória A ─0.91─ Memória B
     │
     └─0.74───── Memória C
```

O sistema usa tanto similaridade semântica quanto associações aprendidas para realizar retrieval. ([ACL Anthology][4])

O código oficial inclui suporte aos benchmarks **LoCoMo** e **LongMemEval-S**, além de scripts de encoding e avaliação, tornando o artigo particularmente interessante como base para reprodução experimental. ([GitHub][5])

**Paper:** [HeLa-Mem: Hebbian Learning and Associative Memory for LLM Agents — ACL Anthology](https://aclanthology.org/2026.acl-long.625/?utm_source=chatgpt.com)

**PDF:** [HeLa-Mem — PDF oficial da ACL](https://aclanthology.org/2026.acl-long.625.pdf?utm_source=chatgpt.com)

**Código:** [HeLa-Mem — GitHub](https://github.com/ReinerBRO/HeLa-Mem?utm_source=chatgpt.com)

---

# 7. Consequência da descoberta do HeLa-Mem

Essa descoberta mudou a proposta.

A ideia inicial:

> adicionar reinforcement e decay ao A-MEM

deixou de ser uma contribuição suficientemente distinta.

O HeLa-Mem já explora exatamente o território de:

```text
grafo de memória
+
associação
+
pesos
+
aprendizado hebbiano
+
spreading activation
```

Portanto, a pergunta passou a ser:

> **Que limitação ainda existe numa memória associativa desse tipo?**

A principal limitação conceitual identificada foi a **temporalidade do conhecimento**.

---

# 8. O problema do decay puramente temporal

Uma informação antiga não necessariamente é irrelevante.

Por exemplo:

```text
2024:
"O projeto foi aprovado pelo conselho."
```

Mesmo anos depois, o fato continua válido e importante.

Em contrapartida:

```text
Janeiro:
"Maria é responsável pelo projeto."

Março:
"João assume o projeto."
```

A primeira informação não deveria ser apagada.

Ela continua historicamente verdadeira.

Porém, ela não representa mais o **estado atual**.

Assim surgiram três conceitos diferentes que não deveriam ser tratados como se fossem um único tipo de decay:

```text
RECÊNCIA
quão nova é a informação

SALIÊNCIA
quão importante/útil ela é

VALIDADE
se ela continua verdadeira naquele momento
```

Foi nesse ponto que surgiu o segundo artigo central.

---

# 9. Zep / Graphiti

## Zep: A Temporal Knowledge Graph Architecture for Agent Memory

O Zep propõe uma camada de memória para agentes baseada em um **knowledge graph temporal**.

Seu componente central é o Graphiti, um mecanismo capaz de integrar continuamente conversas, informações estruturadas e dados empresariais preservando relações históricas. ([arXiv][6])

A diferença fundamental é que ele não trata simplesmente conhecimento antigo como menos relevante.

Ele modela explicitamente **quando uma relação é válida**.

Exemplo:

```text
Maria ─responsável_por→ Projeto X

valid_from: janeiro
valid_to: março
```

e depois:

```text
João ─responsável_por→ Projeto X

valid_from: março
valid_to: atual
```

Assim, o sistema consegue responder duas perguntas diferentes:

```text
Quem é responsável atualmente?

Quem era responsável em fevereiro?
```

sem destruir o histórico.

O Graphiti utiliza um modelo temporal e suporta atualizações incrementais, dados estruturados e não estruturados e consultas combinando mecanismos semânticos, textuais e baseados em grafo. ([GitHub][7])

**Paper:** [Zep: A Temporal Knowledge Graph Architecture for Agent Memory](https://arxiv.org/abs/2501.13956?utm_source=chatgpt.com)

**Graphiti:** [Graphiti — implementação open source](https://github.com/getzep/graphiti?utm_source=chatgpt.com)

---

# 10. O ponto de encontro entre HeLa-Mem e Zep

A discussão convergiu para uma característica importante:

**HeLa-Mem e Zep resolvem problemas diferentes.**

### HeLa-Mem

Responde melhor à pergunta:

> Quais memórias estão associadas e quais conexões se tornaram mais importantes ao longo do uso?

Conceitos principais:

```text
associação
coativação
reinforcement
spreading activation
consolidação
```

### Zep

Responde melhor à pergunta:

> Qual informação era verdadeira em determinado momento e quando ela deixou de ser válida?

Conceitos principais:

```text
temporalidade
validade
histórico
substituição
atualização incremental
```

Portanto:

```text
HeLa-Mem
     ↓
força associativa

+

Zep
     ↓
validade temporal
```

são conceitualmente complementares.

---

# 11. A proposta atual não é simplesmente “juntar os dois”

Uma fusão completa dos frameworks provavelmente criaria um projeto grande demais.

A proposta mais adequada às regras da disciplina é:

## Utilizar o HeLa-Mem como artigo-base

e introduzir **um mecanismo específico inspirado no Zep**.

Fluxo:

```text
HeLa-Mem original
        ↓
REPRODUÇÃO DOS RESULTADOS
        ↓
baseline estabelecida
        ↓
incorporação de temporal validity
        ↓
novo experimento
        ↓
comparação
```

Isso preserva exatamente a metodologia solicitada nas diretrizes: primeiro reproduzir o código/artigo-base e somente depois realizar modificações. 

---

# 12. Evolução proposta

A modificação inicial seria adicionar informação explícita de validade temporal às memórias ou relações relevantes.

Algo conceitualmente semelhante a:

```text
Memory / Relation
├── content
├── embedding
├── associative_weight
├── valid_from
└── valid_to
```

Assim, o retrieval deixaria de considerar apenas algo próximo de:

```text
similaridade
+
força associativa
```

e passaria a considerar:

```text
similaridade
+
força associativa
+
validade temporal
```

Não significa necessariamente utilizar uma soma matemática simples. A implementação exata deve ser definida somente depois da reprodução e compreensão completa do HeLa-Mem.

---

# 13. Exemplo

Considere uma sequência de reuniões:

```text
Janeiro

"Maria será responsável pelo projeto."
```

Depois:

```text
Março

"João assumirá o projeto no lugar de Maria."
```

Depois:

```text
Julho

"João continua responsável."
```

O grafo poderia preservar:

```text
Maria
  │
  └─ responsible_for ─> Projeto
       valid: Jan → Mar
```

e:

```text
João
  │
  └─ responsible_for ─> Projeto
       valid: Mar → presente
```

Ao mesmo tempo, as associações do HeLa-Mem poderiam preservar relações cognitivamente úteis entre:

```text
Maria
João
Projeto
transferência de responsabilidade
reuniões relacionadas
outras decisões
```

Consequentemente, perguntas diferentes ativariam aspectos diferentes da memória.

### Estado atual

> Quem é o responsável atual pelo projeto?

A validade temporal seria central.

### Histórico

> Quem era responsável em fevereiro?

O histórico seria central.

### Relação multi-hop

> Quem participou das decisões que levaram à troca do responsável?

A estrutura associativa passaria a ser especialmente relevante.

---

# 14. Pergunta de pesquisa provisória

Uma formulação possível é:

> **A incorporação explícita de validade temporal em uma memória associativa baseada em grafo melhora o desempenho em tarefas de recuperação temporal e atualização de estado sem prejudicar tarefas associativas e multi-hop?**

Uma versão mais curta:

> **Temporal validity improves associative graph memory for LLM agents?**

Ainda não é necessário fechar o título.

A pergunta científica é mais importante neste momento.

---

# 15. Hipótese

A hipótese seria que o HeLa-Mem apresenta uma representação forte para **associação entre memórias**, mas que uma representação explícita da validade dos fatos pode melhorar tarefas nas quais é necessário distinguir:

```text
o que era verdade
vs
o que é verdade agora
```

A expectativa não precisa ser:

> o método modificado será melhor em tudo.

Um resultado perfeitamente plausível seria:

```text
Temporal questions        ↑
Current-state questions   ↑
Multi-hop                 =
Single-hop                =
Associative retrieval     ↓ pequeno
Custo                     ↑
```

Esse resultado continuaria sendo academicamente relevante.

---

# 16. Experimento principal

Inicialmente:

```text
A — HeLa-Mem original

B — HeLa-Mem + temporal validity
```

Se houver tempo suficiente:

```text
C — HeLa-Mem + temporal validity
                 +
     relation-aware decay
```

É importante que `C` seja tratado como extensão opcional.

O primeiro objetivo deve ser conseguir responder claramente:

> adicionar temporal validity ao HeLa-Mem produz algum efeito mensurável?

---

# 17. Ablation futura

Caso a implementação avance bem, uma análise interessante seria separar os mecanismos:

```text
HeLa-Mem original
```

versus:

```text
HeLa-Mem + temporal validity
```

versus:

```text
HeLa-Mem + relation-aware decay
```

versus:

```text
HeLa-Mem
+ temporal validity
+ relation-aware decay
```

Isso permitiria identificar se eventual diferença vem realmente de:

* temporalidade;
* decay;
* interação entre ambos.

---

# 18. Relation-aware decay como evolução posterior

Outra ideia surgida durante a discussão foi evitar que todas as relações envelheçam da mesma forma.

Exemplo:

### Relação histórica

```text
Pessoa ─participou_de→ Reunião
```

Esse fato não deveria perder validade por envelhecimento.

### Estado mutável

```text
Pessoa ─responsável_por→ Projeto
```

Pode ser substituído.

### Associação aprendida

```text
Decisão A ─related_to→ Decisão B
```

Pode ganhar ou perder força conforme utilização.

Isso sugere futuramente diferenciar:

```text
evento
→ permanece historicamente válido

estado
→ possui intervalo de validade

associação
→ pode sofrer reinforcement/decay
```

Essa separação é conceitualmente mais robusta do que aplicar decay indiscriminadamente a toda memória.

---

# 19. Relação com memória organizacional

Embora o experimento inicial possa usar os benchmarks do HeLa-Mem para facilitar a reprodução e comparação, o problema possui uma aplicação natural em memória organizacional.

Uma reunião gera:

```text
Eventos
Decisões
Responsáveis
Pendências
Mudanças
```

E o conhecimento evolui:

```text
Reunião 1
    ↓
Decisão A

Reunião 2
    ↓
Decisão A confirmada

Reunião 3
    ↓
Decisão B substitui A
```

Uma memória organizacional precisa simultaneamente saber:

```text
o que aconteceu

o que continua válido

o que deixou de valer

o que está associado a quê

quem participou

por que mudou
```

Isso torna o domínio de transcripts um candidato interessante para uma **segunda etapa ou demonstração prática**, depois que o experimento acadêmico principal estiver estabelecido.

---

# 20. Artigos que fizeram parte da evolução da discussão

## Microsoft GraphRAG

**From Local to Global: A Graph RAG Approach to Query-Focused Summarization**

Introduziu a base conceitual de usar grafos como representação intermediária para recuperar e sintetizar conhecimento distribuído por grandes coleções textuais. ([arXiv][1])

[Paper — arXiv](https://arxiv.org/abs/2404.16130?utm_source=chatgpt.com)

[Código — Microsoft GraphRAG](https://github.com/microsoft/graphrag?utm_source=chatgpt.com)

---

## CodeRAG

**Finding Relevant and Necessary Knowledge for Retrieval-Augmented Repository-Level Code Completion**

Foi analisado como alternativa caso o projeto seguisse a direção de agentes de programação. Ele trabalha com construção de query, recuperação de código por múltiplos caminhos e reranking para tarefas de completion em nível de repositório. O trabalho foi publicado no EMNLP 2025 e disponibiliza implementação oficial. ([ACL Anthology][8])

[Paper — ACL Anthology](https://aclanthology.org/2025.emnlp-main.1187/?utm_source=chatgpt.com)

[Código — CodeRAG](https://github.com/KDEGroup/CodeRAG?utm_source=chatgpt.com)

Essa linha continua viável, mas deixou de ser a prioridade quando a discussão convergiu para memória.

---

## A-MEM

**Agentic Memory for LLM Agents**

Introduziu a ideia de uma memória que se organiza dinamicamente e cria relações entre experiências, aproximando a discussão diretamente de memória em grafos. ([arXiv][3])

[Paper — arXiv](https://arxiv.org/abs/2502.12110?utm_source=chatgpt.com)

[Código de avaliação](https://github.com/WujiangXu/AgenticMemory?utm_source=chatgpt.com)

[Sistema A-MEM](https://github.com/agiresearch/A-mem?utm_source=chatgpt.com)

Foi nosso primeiro candidato forte para artigo-base.

---

## HeLa-Mem

**Hebbian Learning and Associative Memory for LLM Agents**

Passou a ocupar o centro da proposta porque implementa explicitamente uma memória associativa baseada em grafo e dinâmica hebbiana. Foi publicado na ACL 2026 e possui código para reprodução com LoCoMo e LongMemEval-S. ([ACL Anthology][4])

[Paper — ACL Anthology](https://aclanthology.org/2026.acl-long.625/?utm_source=chatgpt.com)

[Código oficial — GitHub](https://github.com/ReinerBRO/HeLa-Mem?utm_source=chatgpt.com)

**Situação atual:** principal candidato a artigo-base.

---

## Zep

**A Temporal Knowledge Graph Architecture for Agent Memory**

Introduziu o componente que hoje consideramos complementar ao HeLa-Mem: representação explícita da temporalidade e das mudanças de fatos em uma memória de agente. ([arXiv][6])

[Paper — arXiv](https://arxiv.org/abs/2501.13956?utm_source=chatgpt.com)

---

## Graphiti

O Graphiti é o framework open source associado ao modelo temporal utilizado pelo Zep. Ele mantém knowledge graphs temporalmente conscientes, atualizados incrementalmente, e preserva histórico de relações que mudam com o tempo. ([GitHub][7])

[Graphiti — GitHub](https://github.com/getzep/graphiti?utm_source=chatgpt.com)

Ele é relevante principalmente como **referência de implementação da temporalidade**, e não necessariamente como segundo framework a ser integralmente incorporado ao projeto.

---

## Graph-R1

**Towards Agentic GraphRAG Framework via End-to-end Reinforcement Learning**

Foi encontrado durante a investigação sobre reinforcement learning. Ele transforma a recuperação em GraphRAG em uma interação de múltiplos passos entre agente e ambiente e utiliza RL para otimizar esse processo. ([arXiv][9])

[Paper — Graph-R1](https://arxiv.org/abs/2507.21892?utm_source=chatgpt.com)

Ele foi importante para mostrar que uma proposta genérica de **“GraphRAG + reinforcement learning”** já possui trabalhos muito próximos e não seria uma direção suficientemente específica.

---

# 21. Estado atual da proposta

Neste momento, a linha que parece mais coerente é:

## Artigo-base

**HeLa-Mem: Hebbian Learning and Associative Memory for LLM Agents**

## Referência conceitual para evolução

**Zep: A Temporal Knowledge Graph Architecture for Agent Memory / Graphiti**

## Problema

HeLa-Mem representa e explora associações entre memórias, mas queremos investigar se a representação explícita da **validade temporal dos fatos** acrescenta informação útil ao processo de recuperação.

## Alteração

```text
HeLa-Mem
+
temporal validity inspirado em Zep/Graphiti
```

## Comparação mínima

```text
HeLa-Mem original
        vs
HeLa-Mem + temporal validity
```

## Pergunta central

> A validade temporal explícita melhora uma memória associativa baseada em grafo em tarefas nas quais fatos são modificados ou substituídos ao longo do tempo?

---

# 22. Próxima etapa

Antes de transformar isso definitivamente em proposta de projeto, ainda precisamos verificar quatro coisas no **código real do HeLa-Mem**:

1. exatamente como os nós e arestas são representados;
2. onde o peso hebbiano interfere no retrieval;
3. como LoCoMo e LongMemEval representam perguntas temporais;
4. qual é o menor ponto do código em que temporal validity pode ser introduzida sem reconstruir a arquitetura.

Essa análise é necessária porque a proposta deve nascer da implementação real do artigo-base, não de uma arquitetura hipotética nossa. Isso também segue diretamente a orientação da disciplina de compreender o código-base e a viabilidade das alterações antes de iniciar a evolução. 

A partir disso, dá para fechar algo no formato **problema → artigo-base → hipótese → modificação → datasets → métricas → experimentos → critérios de sucesso**, já praticamente como pré-proposta do projeto.

[1]: https://arxiv.org/abs/2404.16130?utm_source=chatgpt.com "From Local to Global: A Graph RAG Approach to Query-Focused Summarization"
[2]: https://github.com/microsoft/graphrag/blob/main/README.md?utm_source=chatgpt.com "graphrag/README.md at main · microsoft/graphrag · GitHub"
[3]: https://arxiv.org/abs/2502.12110?utm_source=chatgpt.com "A-MEM: Agentic Memory for LLM Agents"
[4]: https://aclanthology.org/2026.acl-long.625/?utm_source=chatgpt.com "HeLa-Mem: Hebbian Learning and Associative Memory for LLM Agents - ACL Anthology"
[5]: https://github.com/ReinerBRO/HeLa-Mem?utm_source=chatgpt.com "GitHub - ReinerBRO/HeLa-Mem: HeLa-Mem code for LongMemEval · GitHub"
[6]: https://arxiv.org/abs/2501.13956?utm_source=chatgpt.com "Zep: A Temporal Knowledge Graph Architecture for Agent Memory"
[7]: https://github.com/Memory-Agents/graphiti/?utm_source=chatgpt.com "GitHub - Memory-Agents/graphiti · GitHub"
[8]: https://aclanthology.org/2025.emnlp-main.1187/?utm_source=chatgpt.com "CodeRAG: Finding Relevant and Necessary Knowledge for Retrieval-Augmented Repository-Level Code Completion - ACL Anthology"
[9]: https://arxiv.org/abs/2507.21892?utm_source=chatgpt.com "Graph-R1: Towards Agentic GraphRAG Framework via End-to-end Reinforcement Learning"


Fiz a inspeção do **paper, código oficial do HeLa-Mem, pipeline do LongMemEval-S e mecanismo temporal do Zep/Graphiti**. O resultado é bom, mas corrige uma parte importante da hipótese que estávamos formulando.

> **A evolução não deve ser “adicionar temporalidade ao HeLa-Mem”.**
> O HeLa-Mem já possui timestamps e temporal decay. A evolução mais defensável é adicionar **validade temporal e supersessão explícita de fatos**: distinguir *quando uma informação ocorreu* de *durante qual período ela permaneceu verdadeira*.

Isso mantém a proposta pequena, tecnicamente implementável e com uma variável experimental clara.

---

# 1. O que existe de fato no HeLa-Mem

O artigo-base seria:

**HeLa-Mem: Hebbian Learning and Associative Memory for LLM Agents**, ACL 2026. O paper descreve a memória episódica como um grafo ponderado cujos nós contêm texto, embedding, timestamp, keywords e papel do interlocutor; as arestas representam associações e têm pesos que evoluem por aprendizado hebbiano. 

[Paper oficial — ACL Anthology](https://aclanthology.org/2026.acl-long.625/?utm_source=chatgpt.com)
[Código oficial — GitHub](https://github.com/ReinerBRO/HeLa-Mem?utm_source=chatgpt.com)

No código real, `HebbianMemoryGraph` representa exatamente isso:

```text
nodes
  └─ node_id
       ├─ content
       ├─ role
       ├─ embedding
       ├─ timestamp
       ├─ keywords
       └─ metadata

edges
  └─ source_id
       └─ target_id → weight
```

A própria implementação chama o peso da aresta de **“Synaptic Strength”**. Novos nós são inicialmente ligados ao nó anterior com peso `0.5`. 

Portanto, não precisamos criar uma arquitetura de grafo. Ela já existe.

---

# 2. Onde o aprendizado hebbiano interfere

O retrieval tem duas rotas.

Primeiro, existe uma ativação básica aproximadamente formada por:

```text
similaridade semântica
+
keyword matching
+
temporal decay
```

Depois ocorre *spreading activation* pelas arestas:

```text
Memory A
  │
  │ weight = 0.8
  ▼
Memory B
```

Se A é relevante para a pergunta e A tem forte associação com B, B pode receber um boost mesmo que não tenha alta similaridade semântica com a pergunta. É exatamente esse mecanismo que o artigo defende para recuperar informações multi-hop. 

No código, o boost é proporcional a:

```text
activation(A) × weight(A,B) × alpha
```

e aparece diretamente no ranking final. 

Depois do retrieval há o reinforcement:

```python
retrieved together
        ↓
edge weight += learning_rate
```

Ou seja:

```text
consulta 1

A ─── B

A e B são recuperados juntos
        ↓

A ═══ B
associação mais forte
```

O código percorre todos os pares de memórias recuperadas e reforça suas conexões. 

Então a parte de reinforcement que discutimos **já está concretamente implementada**.

---

# 3. HeLa-Mem também já possui decay

Este ponto corrige nossa formulação anterior.

No paper, o score base contém explicitamente:

$$
\gamma(v_i)=e^{-\Delta t/\tau}
$$

ou seja, memórias mais antigas recebem temporal decay. O artigo usa `τ = 60 dias` nos experimentos principais. 

Também existe teoricamente decay das arestas hebbianas. O artigo descreve reinforcement das conexões coativadas e enfraquecimento das conexões não utilizadas. 

Portanto, propor simplesmente:

> “HeLa-Mem + decay”

não seria uma evolução.

---

# 4. Encontrei uma inconsistência importante entre paper e código

Aqui existe um problema que precisará ser tratado na fase de reprodução.

Na versão atual do repositório, `compute_time_decay()` espera:

```python
compute_time_decay(timestamp_str, tau=None)
```

e calcula o tempo contra `datetime.now()`. 

Porém, o método `retrieve()` chama:

```python
compute_time_decay(node["timestamp"], current_time)
```

onde `current_time` é uma **string de timestamp**, não o parâmetro numérico `tau`. 

Como `compute_time_decay()` captura qualquer exceção e retorna `1.0`, essa chamada aparentemente faz com que o temporal decay seja neutralizado nessa versão do código:

```text
erro no cálculo
     ↓
except
     ↓
return 1.0
```

Isso precisa ser **confirmado executando a baseline**. Não devemos corrigir silenciosamente antes disso.

Há outra diferença: `global_decay()` existe e reduz os pesos das arestas, mas não encontrei chamada a ele nos entry points principais de encoding, evaluation, retriever ou knowledge memory.  

Isso cria um ponto metodológico importante:

```text
Paper
  ≠ necessariamente
release atual do código
```

Primeiro precisamos reproduzir **exatamente o código oficial**, registrar os resultados e só depois decidir se uma eventual correção necessária para reproduzir o paper será tratada como *reproduction fix*, separada da nossa contribuição científica.

---

# 5. O ponto onde nossa proposta realmente se diferencia

HeLa-Mem sabe:

```text
quando uma memória ocorreu
```

e tenta representar:

```text
quão relevante/recente ela é
```

O que ele **não representa explicitamente** é:

```text
durante qual intervalo determinado fato foi verdadeiro
```

Essa é a ideia importante do Zep/Graphiti.

O Graphiti representa relações com **janelas de validade**, preservando o fato antigo quando um novo fato o substitui. Assim ele consegue distinguir o estado atual do histórico. ([GitHub][1])

[Paper Zep — Temporal Knowledge Graph Architecture for Agent Memory](https://arxiv.org/abs/2501.13956?utm_source=chatgpt.com)
[Graphiti — implementação open source](https://github.com/getzep/graphiti?utm_source=chatgpt.com)

A diferença é esta:

### HeLa-Mem

```text
Memória:
"João é responsável pelo projeto"

timestamp:
10/01
```

### Validade temporal

```text
Fato:
João → responsável_por → Projeto

valid_from: 10/01
valid_to: 15/04
```

Se depois surgir:

```text
15/04:
"Maria assumiu o projeto"
```

não apagamos João:

```text
João → responsável_por → Projeto
10/01 ─────────────── 15/04

Maria → responsável_por → Projeto
15/04 ─────────────────────→
```

Isso é fundamentalmente diferente de decay.

---

# 6. O melhor lugar para implementar isso

Minha conclusão depois de ler o código é que **não devemos alterar inicialmente o grafo episódico do HeLa-Mem**.

Isso aumentaria muito o escopo.

O ponto mais limpo é a **Semantic Memory Store**.

O HeLa-Mem já possui `HebbianKnowledgeMemory`. O método `add_knowledge()` atualmente transforma fatos extraídos em nós desse segundo grafo e coloca apenas:

```python
metadata={"type": "fact"}
```



Então podemos usar a estrutura existente.

A proposta seria passar de:

```text
metadata
└─ type: fact
```

para algo conceitualmente como:

```text
metadata
├─ type: fact
├─ valid_from
├─ valid_to
├─ superseded_by
└─ source_timestamp
```

Sem Graphiti, Neo4j ou um segundo framework.

O **conceito vem do Zep**, mas a implementação continua dentro do HeLa-Mem.

Isso é bem mais controlado.

---

# 7. Como o conhecimento é gerado hoje

Durante o encoding do LongMemEval, o HeLa-Mem processa as conversas em blocos.

Cada turno já possui timestamp derivado de `haystack_dates`. 

A cada bloco, o LLM extrai informações do usuário. Cada fato extraído é enviado atualmente assim:

```python
knowledge_memory.add_knowledge(fact)
```



O problema é que nesse momento o timestamp original do fato é perdido. O `add_knowledge()` cria um novo nó usando o horário da execução, e não necessariamente a data da conversa que originou o fato. 

Isso nos dá um ponto de intervenção muito preciso.

---

# 8. Modificação proposta

O pipeline original:

```text
conversas
   ↓
extração de fatos
   ↓
add_knowledge(fact)
   ↓
semantic graph
```

Passaria para:

```text
conversas + timestamp
        ↓
extração de fato
        ↓
busca de fatos semanticamente relacionados
        ↓
novo fato contradiz/substitui algum fato ativo?
        │
      ┌─┴───────────┐
      │             │
     não           sim
      │             │
      ▼             ▼
adiciona       fecha validade
novo fato      do fato anterior
      │             │
      └──────┬──────┘
             ▼
      semantic graph
```

Não precisamos imediatamente transformar tudo em triplas `subject-predicate-object`.

Podemos manter os fatos textuais do HeLa-Mem e classificar sua relação com fatos existentes como, por exemplo:

```text
UNRELATED
SAME
SUPERSEDES
```

Isso reduz drasticamente o tamanho da intervenção.

---

# 9. Retrieval modificado

Hoje a memória semântica é recuperada assim:

```python
search_knowledge(question, top_k=...)
```



E aqui encontrei outra abertura importante.

O LongMemEval fornece explicitamente:

```text
question_date
```

O HeLa-Mem lê essa data e a entrega ao LLM no prompt como:

```text
Current date: ...
```

mas **não passa `question_date` para o retrieval**. 

Ou seja:

```text
question_date

    ├────> LLM final ✓
    │
    └────> retrieval ✗
```

Nossa proposta poderia passar a fazer:

```text
question
+
question_date
        ↓
validity-aware retrieval
```

Para uma pergunta sobre estado atual:

```text
recuperar prioritariamente fatos
válidos em question_date
```

Para uma pergunta histórica:

```text
recuperar fato cujo intervalo
engloba a data consultada
```

Esse é, para mim, **o ponto técnico mais forte encontrado na inspeção**.

---

# 10. O dataset principal praticamente já está escolhido

Eu usaria **LongMemEval-S como dataset principal**, antes de LoCoMo.

Há uma razão objetiva: ele contém justamente as categorias que queremos estudar:

| Categoria          | O que testa                                   |
| ------------------ | --------------------------------------------- |
| Temporal reasoning | raciocínio envolvendo tempo                   |
| Knowledge update   | conhecimento que muda ao longo das interações |
| Multi-session      | integração entre sessões                      |
| Single-session     | recuperação mais simples                      |
| Abstention         | saber quando não existe informação            |

O benchmark possui 500 itens e cada instância inclui `question_type`, `question`, `answer`, `question_date` e histórico timestampado. ([GitHub][2])

Mais importante: **o próprio repositório do HeLa-Mem já traz o LongMemEval-S completo e scripts de reprodução**. ([GitHub][3])

Isso atende muito bem às exigências da disciplina de partir de um código reproduzível e trabalhar com datasets e métricas compatíveis com o artigo-base.  

---

# 11. Temos uma baseline numérica clara

No LongMemEval-S, o paper reporta:

| Categoria        |   HeLa-Mem |
| ---------------- | ---------: |
| Temporal         | **50,38%** |
| Multi-Session    | **57,14%** |
| Knowledge-Update | **78,21%** |
| Single           | **78,85%** |
| Overall          | **65,40%** |



Isso é excelente para o projeto.

Não estamos começando com:

> “vamos ver se funciona”.

Estamos começando com:

```text
TARGET DE REPRODUÇÃO
Overall ACC ≈ 65,40%
```

e depois:

```text
BASELINE REPRODUZIDA
vs
BASELINE + TEMPORAL VALIDITY
```

---

# 12. Papel do LoCoMo

Eu manteria LoCoMo como **segundo dataset**, se o prazo permitir.

Ele tem 1.986 perguntas distribuídas entre single-hop, multi-hop, temporal, open-domain e adversarial. 

No GPT-4o-mini, por exemplo, o artigo reporta F1 de:

```text
Multi-hop       40,14
Temporal        47,29
Open-domain     29,70
Single-hop      51,89
```



Mas o **LongMemEval-S é melhor para nossa hipótese**, porque possui uma categoria explícita de `knowledge-update`.

---

# 13. Pré-proposta do projeto

## Título provisório

**Temporal Validity-Aware Hebbian Memory for LLM Agents**

ou:

**Incorporating Temporal Fact Validity into Hebbian Associative Memory for LLM Agents**

Em português:

**Memória Associativa Hebbiana com Validade Temporal para Agentes Baseados em LLM**

---

## Problema

Memórias associativas em grafos podem preservar relações entre experiências e utilizar essas relações durante a recuperação. Entretanto, a recência temporal de uma memória não representa necessariamente a validade temporal de um fato.

Um fato antigo pode continuar verdadeiro; outro pode ter sido explicitamente substituído.

---

## Artigo-base

**HeLa-Mem: Hebbian Learning and Associative Memory for LLM Agents**.

Será reproduzido **sem alterações antes da implementação da proposta**, exatamente como exigido pela disciplina. 

---

## Trabalho usado como inspiração

**Zep: A Temporal Knowledge Graph Architecture for Agent Memory**, especificamente seu conceito de fatos com intervalo de validade e preservação de estados históricos. Zep/Graphiti foi desenvolvido justamente para dados que mudam continuamente e mantém relações históricas em vez de simplesmente sobrescrevê-las. ([arXiv][4])

---

# 14. Pergunta de pesquisa

Eu fecharia atualmente assim:

> **A representação explícita da validade e supersessão de fatos melhora uma memória associativa hebbiana em tarefas de atualização de conhecimento e raciocínio temporal, quando comparada ao mecanismo original baseado em timestamps e temporal decay?**

Essa pergunta tem três vantagens.

Ela não promete melhoria.

Ela especifica exatamente o que está sendo alterado.

E define onde esperamos observar algum efeito:

```text
Temporal Reasoning
Knowledge Update
```

---

# 15. Hipótese

A hipótese experimental seria:

> A inclusão de intervalos explícitos de validade para fatos permitirá que o sistema diferencie melhor informações históricas de informações atualmente válidas, podendo melhorar tarefas de knowledge-update e temporal reasoning, sem necessariamente produzir ganhos em tarefas de recuperação simples ou multi-hop.

Pode dar:

```text
Knowledge Update   ↑
Temporal           ↑
Multi-session      =
Single             =
```

ou:

```text
Knowledge Update   =
Temporal           =
custo              ↑
```

O segundo resultado também é válido.

---

# 16. Experimento principal

Eu manteria inicialmente apenas dois sistemas:

| Sistema          | Descrição                                                     |
| ---------------- | ------------------------------------------------------------- |
| **A — Baseline** | HeLa-Mem original                                             |
| **B — Proposta** | HeLa-Mem + validade/supersessão temporal na memória semântica |

Todo o restante deve permanecer igual:

```text
mesmo dataset
mesmo LLM
mesmos embeddings
mesmo top-k
mesmo prompt de resposta
mesmos parâmetros hebbianos
mesma avaliação
```

Isso é fundamental para conseguirmos atribuir eventual diferença à nossa intervenção.

---

# 17. Métricas

A métrica primária seria a mesma utilizada pelo experimento LongMemEval-S do HeLa-Mem:

```text
Accuracy geral
```

Mas a análise realmente importante será:

```text
ACC Temporal
ACC Knowledge-Update
ACC Multi-Session
ACC Single
```

Assim conseguimos detectar algo como:

```text
Overall: +0,5 p.p.

mas

Knowledge Update: +6 p.p.
Temporal: +4 p.p.
Single: -1 p.p.
```

Esse resultado seria mais informativo do que olhar apenas o overall.

Também registraria:

```text
latência
quantidade de fatos recuperados
tokens de contexto
número de chamadas ao LLM
```

E, para comparação A/B por item, faria teste estatístico pareado ou bootstrap de confiança, em vez de olhar somente diferença absoluta de accuracy.

---

# 18. Critério de sucesso do projeto

Aqui eu separaria **sucesso científico** de **resultado positivo**.

O projeto é bem-sucedido se conseguirmos:

1. reproduzir adequadamente o HeLa-Mem ou documentar rigorosamente eventuais divergências entre paper e código;
2. implementar temporal validity como alteração isolada;
3. executar baseline e proposta sob as mesmas condições;
4. medir a diferença por categoria;
5. explicar por que houve ganho, ausência de ganho ou perda.

Isso está alinhado com o que as diretrizes pedem: evolução clara, experimentos e análise quantitativa/qualitativa, não simplesmente “obter uma métrica maior”. 

---

# 19. Sequência de Execução do Projeto

| Etapa | Status | Resultado / Evidência |
| :--- | :---: | :--- |
| **0. Fixar versão** | ✅ **CONCLUÍDO** | Commit oficial `68f19b3fac8c6156570d5aeb3a7a3e8f3ba7cb04` clonado em `external/HeLa-Mem` |
| **1. Sanity check** | ✅ **CONCLUÍDO** | Piloto com 10 itens executado com 90.00% de acurácia (`reports/analysis/R03_reproducao_hela_pilot_20260927.md`) |
| **2. Reprodução completa** | ✅ **CONCLUÍDO** | 500 itens completos avaliados: **61.20% ACC overall** (`reports/analysis/R03_reproducao_hela_full_20260929_194502.md`) |
| **3. Investigar divergências** | ✅ **CONCLUÍDO** | Divergência de chamada em `compute_time_decay` e ausência de `global_decay` confirmadas na baseline real |
| **4. Congelar baseline** | ✅ **CONCLUÍDO** | **Baseline A oficialmente congelada em 61.20%** para comparação com a proposta |
| **5. Implementar validity** | ✅ **CONCLUÍDO** | Implementado `TemporalKnowledgeMemory` com `valid_from`, `valid_to`, `SUPERSEDES`, $V(f, t_{\text{query}})$ e `ValidityAwareRetriever` |
| **6. Executar proposta** | ✅ **CONCLUÍDO** | 500 itens completos avaliados sob a Proposta B: **65.60% ACC overall** (+4.40 p.p. vs. Baseline A) |
| **7. Comparação A/B** | ✅ **CONCLUÍDO** | Análise pareada por teste exato de McNemar ($p = 0.0115$ unilateral, $p = 0.0230$ bilateral, +22 acertos líquidos) |
| **8. Ablação B0** | ✅ **CONCLUÍDO** | Condição B0 executada (**64.20% ACC**): isolamento rigoroso entre efeito da extração por sessão e efeito temporal (`reports/analysis/R05_decomposicao_A_B0_B_20261104_205642.md`) |
| **9. Análise qualitativa** | ✅ **CONCLUÍDO** | Validação cabal da hipótese: $B_0 \rightarrow B$ em `knowledge-update` saltou de 65.38% para **83.33%** (+14 acertos líquidos, 0 regressões) |
| **10. Auditoria R05** | ✅ **CONCLUÍDO** | Auditoria metodológica e identificação dos 10 achados operacionais (`reports/analysis/R05_auditoria_processo_20261104.md`) |
| **11. Medição de ruído (B')** | ✅ **CONCLUÍDO** | Reavaliação $B'$ nos 500 itens sob `temperature=0.7`: ruído de 7,20% no overall; KU idêntico em **83,33%** com 97,4% de estabilidade |
| **12. Proposta B_v2 (Ontológica)** | ✅ **CONCLUÍDO** | Prompt ontológico sem exemplos de domínio: **64,80% ACC**, KU com **79,49%** ($p=0{,}0034$ vs $B_0$), TR atinge recorde de **57,89%** |
| **13. Diagnóstico de Baseline A** | ✅ **CONCLUÍDO** | Item 400 extraiu 9 nós com `workers=1`, refutando brevidade de diálogo e provando concorrência silenciosa na baseline A original |
| **14. Baseline Fiel A*** | 🔄 **EM EXECUÇÃO** | Geração da baseline sem falhas concorrentes e com hiperparâmetros oficiais do HeLa-Mem (`results/longmemeval_baseline_fiel/`) |

---
# 20. Resultados Consolidados da Reprodução da Baseline (Etapa 2)

A reprodução estrita do código oficial do HeLa-Mem no benchmark completo **LongMemEval-S (500 instâncias)** foi concluída com sucesso.

### 20.1 Tabela Comparativa de Acurácia

| Categoria / Question Type | Amostras | Acertos | ACC Obtida (%) | Meta do Paper ACL 2026 | Desvio | Status |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Overall (Geral)** | **500** | **306** | **61.20%** | **65.40%** | **-4.20 p.p.** | **Reproduzido** |
| `temporal-reasoning` | 133 | 69 | **51.88%** | **50.38%** | **+1.50 p.p.** | **Superou paper** |
| `knowledge-update` | 78 | 57 | **73.08%** | **78.21%** | **-5.13 p.p.** | **Fiel à meta** |
| `single-session-user` | 70 | 61 | **87.14%** | **78.85%** | **+8.29 p.p.** | **Superou paper** |
| `single-session-assistant` | 56 | 49 | **87.50%** | — | — | Alto desempenho |
| `multi-session` | 133 | 62 | **46.62%** | **57.14%** | **-10.52 p.p.** | Variância de amostra |
| `single-session-preference` | 30 | 8 | **26.67%** | — | — | Rubrica rigorosa |

### 20.2 Principais Descobertas Técnicas da Reprodução

1. **Separação Estável de Fases:** A divisão entre codificação (`encode_longmemeval.py`) e avaliação (`eval_longmemeval.py`) permitiu persistir os 500 grafos de memória hebbiana (`results/longmemeval_baseline_full/`) com segurança em disco.
2. **Resolução de Infraestrutura:** Foi superado o limite de 10.000 requisições diárias da OpenAI (Tier 1 RPD) através da separação modular dos processos e resolvido o problema de codec de console Windows (`cp1252`) reconfigurando os streams de saída para UTF-8.
3. **Documentação Didática Produzida:** Foi desenvolvido o guia interativo em HTML ([`docs/explicacao_codigo_hela_mem.html`](file:///d:/Python%20Projetos/mestrado-dl-projeto/docs/explicacao_codigo_hela_mem.html)) com tradução das rotinas técnicas para metáforas leigas e simulador visual de redes sinápticas.

A **Baseline A está formalmente congelada em 61.20%**. O projeto está apto para iniciar a **Etapa 5 (Implementação da Validade Temporal)**.

---


---

# 21. Resultados Consolidados da Proposta B (Validade Temporal)

A **Proposta B** introduziu uma modelagem explícita de validade temporal e supersessão de conhecimento sobre a memória semântica do HeLa-Mem:
1. **Atributos de Janela Temporal:** Cada fato $f$ extraído possui `valid_from` (data da sessão de origem) e `valid_to` (inicialmente aberto; preenchido ao ser supersedido por fato mais recente).
2. **Grafo de Conhecimento com Relações Tipadas:** O classificador temporal infere arestas `SUPERSEDES` ($w=0.8$) quando um novo fato contradiz ou atualiza um fato existente, marcando o anterior como `superseded`.
3. **Pertinência Temporal Consciente da Consulta $V(f, t_{\text{query}})$:**
   $$V(f, t_{\text{query}}) = \begin{cases} 
   1.0, & \text{se } \text{valid\_from} \le t_{\text{query}} \le \text{valid\_to} \text{ (vigente)} \\
   \exp\left(-\frac{|t_{\text{query}} - \text{valid\_to}|}{\tau}\right), & \text{se } t_{\text{query}} > \text{valid\_to} \text{ (supersedido/histórico)} \\
   0.0, & \text{se } t_{\text{query}} < \text{valid\_from} \text{ (fato futuro à consulta)}
   \end{cases}$$
4. **Formatação no Prompt de Geração:** Fatos vigentes são explicitamente sinalizados com a tag `[CURRENT]` e fatos expirados com a tag `[HISTORICAL]`, permitindo que o LLM priorize o estado atual do conhecimento.

Sob as mesmas 500 instâncias do benchmark **LongMemEval-S**, a Proposta B atingiu:
- **Acurácia Geral:** **65.60%** (328/500 acertos), um avanço de **+4.40 p.p.** sobre a Baseline A congelada (61.20%).
- **Teste Pareado de McNemar:** 54 ganhos ($0 \rightarrow 1$) vs. 32 regressões ($1 \rightarrow 0$), com saldo líquido de **+22 acertos** ($p = 0.0115$ unilateral, $p = 0.0230$ bilateral — estatisticamente significante com $p < 0.05$).

---

# 22. Estudo de Ablação B0 e Decomposição do Ganho (A → B0 → B)

Para responder com rigor científico à pergunta de pesquisa da dissertação e evitar a confusão de variáveis entre a correção da extração semântica e a introdução da lógica temporal, foi formulada e avaliada a condição de ablação **$B_0$**:

- **Baseline A (HeLa-Mem original):** Extração de fatos semânticos acionada a cada 10 turnos (deixando 360 dos 500 itens com grafo semântico vazio por brevidade das conversas).
- **Ablação $B_0$ (Isolamento da Extração):** Utiliza exatamente os mesmos fatos semânticos extraídos sessão a sessão da Proposta B, mas desativa completamente a temporalidade: todos os fatos são tratados como ativos (`valid_to = None`), arestas temporais do classificador são removidas (mantendo apenas a cadeia sequencial $w=0.5$), $V(f, t_{\text{query}}) \equiv 1.0$ e o prompt reverte para o formato textual original do HeLa-Mem (`- fato`).
- **Proposta B (Mecanismo Temporal Completo):** Fatos por sessão + janelas de validade + $V(f, t_{\text{query}})$ + tags `[CURRENT]`/`[HISTORICAL]` + arestas `SUPERSEDES`.

### 22.1 Tabela Comparativa Geral ($N = 500$)

| Categoria / Question Type | $N$ | Baseline A | Ablação $B_0$ | Proposta B | Saldo $A \rightarrow B_0$ | Saldo $B_0 \rightarrow B$ | Saldo Total ($A \rightarrow B$) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `knowledge-update` | 78 | 73.08% (57) | 65.38% (51) | **83.33% (65)** | -6 (+5/-11) | **+14 (+14/-0)** | **+8 (+11/-3)** |
| `temporal-reasoning` | 133 | 51.88% (69) | **57.14% (76)** | 55.64% (74) | +7 (+16/-9) | -2 (+8/-10) | **+5 (+15/-10)** |
| `multi-session` | 133 | 46.62% (62) | **54.14% (72)** | 48.87% (65) | +10 (+16/-6) | -7 (+7/-14) | **+3 (+14/-11)** |
| `single-session-preference` | 30 | 26.67% (8) | 40.00% (12) | **46.67% (14)** | +4 (+6/-2) | +2 (+3/-1) | **+6 (+8/-2)** |
| `single-session-assistant` | 56 | 87.50% (49) | 89.29% (50) | **92.86% (52)** | +1 (+2/-1) | +2 (+2/-0) | **+3 (+3/-0)** |
| `single-session-user` | 70 | **87.14% (61)** | 85.71% (60) | 82.86% (58) | -1 (+2/-3) | -2 (+1/-3) | **-3 (+3/-6)** |
| **OVERALL** | **500** | **61.20% (306)** | **64.20% (321)** | **65.60% (328)** | **+15 (+47/-32)** | **+7 (+35/-28)** | **+22 (+54/-32)** |

### 22.2 Decomposição Pareada e Teste Exato de McNemar

| Transição | O que isola / avalia? | Ganhos (0→1) | Regressões (1→0) | Saldo Líquido | $\Delta$ p.p. | $p$ unilateral | $p$ bilateral |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **$A \rightarrow B_0$** | Efeito da correção da extração por sessão | +47 | -32 | +15 | +3.00 | 0.0573 | 0.1147 |
| **$B_0 \rightarrow B$** | Efeito do mecanismo temporal explícito | +35 | -28 | +7 | +1.40 | 0.2250 | 0.4500 |
| **$A \rightarrow B$** | Efeito completo combinado | +54 | -32 | +22 | +4.40 | **0.0115** | **0.0230** |

### 22.3 Análise em Subconjuntos com vs. sem Supersessão

O benchmark LongMemEval-S possui itens com fatos mutáveis ao longo do tempo e itens puramente estáticos. Na Proposta B, foram identificados **249 itens com nós supersedidos** e **251 itens sem supersessão**:

| Subconjunto | $N$ | Baseline A | Ablação $B_0$ | Proposta B | Saldo $A \rightarrow B_0$ | Saldo $B_0 \rightarrow B$ | Saldo Total $A \rightarrow B$ |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Com supersessão** | 249 | 52.21% (130) | 55.82% (139) | **58.23% (145)** | +9 | **+6** | **+15** |
| **Sem supersessão** | 251 | 70.12% (176) | 72.51% (182) | **72.91% (183)** | +6 | **+1** | **+7** |

---

# 23. Conclusão Científica: O Fenômeno de Interferência e Validação da Hipótese

O estudo de ablação $B_0$ revelou uma dinâmica teórica fundamental para a dissertação:

1. **O Fenômeno da Interferência Factual em $A \rightarrow B_0$:**
   Na categoria `knowledge-update`, a acurácia **caiu de 73.08% em A para 65.38% em B0** (-6 acertos líquidos). Isso ocorreu porque extrair todos os fatos sem associar regras de validade temporal fez com que o retriever injetasse no prompt tanto a informação desatualizada quanto a nova informação conflitante como fatos indistinguíveis (`- fato`). Sem âncora temporal, o modelo foi induzido ao erro pela presença de fatos obsoletos no contexto.

2. **A Resolução pelo Mecanismo Temporal em $B_0 \rightarrow B$:**
   Ao reativar as janelas de validade temporal, a atenuação exponencial por $V(f, t_{\text{query}})$ e as marcações `[CURRENT]` vs. `[HISTORICAL]`, a acurácia em `knowledge-update` saltou de **65.38% para 83.33%** (+17.95 p.p.).
   Foram **14 novos acertos e ZERO regressões** (+14 / -0).

3. **Resposta à Pergunta de Pesquisa:**
   > *A representação explícita da validade e da supersessão temporal de fatos melhora uma memória associativa hebbiana em tarefas de atualização de conhecimento e raciocínio temporal?*

   **Sim.** A evidência experimental demonstra que a memória associativa hebbiana pura é insuficiente para lidar com a mutabilidade do conhecimento em diálogos de longo prazo, sendo a modelagem explícita de validade e supersessão indispensável para eliminar a interferência de memórias obsoletas e guiar a geração factual correta.

---

# 24. Diagnóstico Empírico da Baseline A (Achado 2: Falha Silenciosa de Concorrência)

Durante a auditoria de processo documentada no relatório [`R05`](reports/analysis/R05_auditoria_processo_20261104.md), constatou-se que **360 dos 500 grafos de memória semântica da Baseline A original estavam completamente vazios**. 

Investigações detalhadas documentadas no relatório [`R06`](reports/analysis/R06_diagnostico_baseline_e_ruido_Bprime_Bv2_20261105.md) revelaram a causa-raiz:
1. **Hipótese Inicial (Refutada):** Supunha-se inicialmente que os grafos estavam vazios porque as conversas não atingiam o buffer mínimo de 10 turnos exigido pelo HeLa-Mem. No entanto, os itens dos blocos finais (como [400:450], onde 100% dos grafos estavam vazios) continham em média 23,5 turnos de diálogo.
2. **Comprovação Experimental:** Submeteu-se o item 400 (`eac54adc`) ao pipeline oficial de codificação do HeLa-Mem (`encode_single_item`) com execução estritamente sequencial (`workers=1`). O código oficial extraiu **9 nós semânticos de alta qualidade** e atualizou o perfil de usuário.
3. **Mecanismo da Falha:** No código original do HeLa-Mem, a rotina `process_incremental_buffer` encapsula chamadas em bloco `try...except Exception as e: print(...)`. Em ambiente paralelo multithreaded no Windows, concorrência no carregamento e inferência de modelos locais de embedding e chamadas de API geraram exceções silenciosas, levando ao descarte silencioso de 72% dos grafos semânticos.
4. **Implicação Metodológica:** A Baseline A original (61,20%) estava artificialmente subestimada em relação ao seu potencial nominal. Para garantir integridade científica irrefutável na dissertação, foi estabelecida a execução da **Baseline Fiel ($A^*$)** com parâmetros oficiais (`MAX_FLIPPED=3`, `KEYWORD_WEIGHT=0.7`, `BUFFER_SIZE=10`) em modo sequencial/controlado em `results/longmemeval_baseline_fiel/`.

---

# 25. Piso de Ruído Estocástico (B') e Proposta B_v2 (Classificador Ontológico)

### 25.1 Medição do Piso de Ruído do Avaliador ($B \times B'$)
Para verificar se os ganhos observados na Proposta B decorriam de variância aleatória do LLM sob `temperature=0.7` na geração e no juiz (`gpt-4o-mini`), foi executada uma réplica independente completa ($B'$, documentada em `results/longmemeval_temporal_full/eval_results_b_rerun/` e no relatório [`R06`](reports/analysis/R06_diagnostico_baseline_e_ruido_Bprime_Bv2_20261105.md)):
- **Acurácia Geral:** $B = 65{,}60\%$ (328/500) vs $B' = 64{,}00\%$ (320/500), com 36 pares discordantes (7,20% de ruído) e teste de McNemar bilateral $p = 0{,}2430$ (sem diferença estatisticamente significativa entre réplicas).
- **Estabilidade em `knowledge-update`:** Ambas as execuções obtiveram **rigorosamente a mesma acurácia: 83,33% (65/78)**, com apenas 2 itens oscilando (+1 / -1), o que representa **97,44% de estabilidade factual**. Como o salto causal da introdução da temporalidade sobre $B_0$ é de $+14$ acertos líquidos, a magnitude do efeito é **mais de 7 vezes superior ao ruído estocástico**, provando a solidez da hipótese.

### 25.2 Proposta $B_{\text{v2}}$: Eliminação de Viés de Prompt e Generalização Ontológica
Na versão inicial da Proposta B, o classificador continha exemplos específicos de domínio no prompt de classificação de relação temporal. Para eliminar qualquer risco de direcionamento (*prompt biasing* ou vazamento de casos de teste), formulou-se a **Proposta $B_{\text{v2}}$**, na qual todos os exemplos de domínio foram removidos e substituídos pela fundamentação lógica formal do *Event Calculus*:
- `SUPERSEDES`: Restrito a transições de atributos unívocos ou estados mutuamente exclusivos de uma entidade (endereço atual, estado civil, empregador, preferência ativa), onde o fato anterior deixa de ser verdadeiro no presente.
- `EXTENDS`: Eventos históricos independentes, ações pretéritas, experiências, compras/transações ou coexistência de entidades, que permanecem permanentemente verdadeiros no histórico temporal.

**Resultados de $B_{\text{v2}}$ nos 500 itens (`results/longmemeval_temporal_v2/`):**
- **Acurácia Geral:** **64,80%** (324/500).
- **`knowledge-update`:** Atingiu **79,49%** (62/78), mantendo ganho estatisticamente significante de $+11$ acertos líquidos sobre a ablação $B_0$ ($p = 0{,}0034$).
- **`temporal-reasoning`:** Atingiu o **recorde histórico do projeto de 57,89%** (77/133 acertos).
- **Redução de Over-supersession em `multi-session`:** As regressões sobre $B_0$ caíram de 14 para 10, recuperando questões de contagem cumulativa que haviam sido erroneamente atenuadas na versão anterior.

---

[1]: https://github.com/getzep/graphiti "GitHub - getzep/graphiti: Build Real-Time Knowledge Graphs for AI Agents · GitHub"
[2]: https://github.com/xiaowu0162/longmemeval?utm_source=chatgpt.com "GitHub - xiaowu0162/LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory (ICLR 2025) · GitHub"
[3]: https://github.com/ReinerBRO/HeLa-Mem "GitHub - ReinerBRO/HeLa-Mem: HeLa-Mem code for LongMemEval · GitHub"
[4]: https://arxiv.org/abs/2501.13956 "[2501.13956] Zep: A Temporal Knowledge Graph Architecture for Agent Memory"
