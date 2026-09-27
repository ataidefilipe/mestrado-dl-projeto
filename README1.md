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

# 19. Sequência que eu seguiria daqui

| Etapa                          | Resultado esperado                               |
| ------------------------------ | ------------------------------------------------ |
| **0. Fixar versão**            | commit exato do HeLa-Mem registrado              |
| **1. Sanity check**            | rodar 20–50 itens do LongMemEval                 |
| **2. Reprodução completa**     | 500 itens, baseline registrada                   |
| **3. Investigar divergências** | confirmar especialmente decay e `global_decay()` |
| **4. Congelar baseline**       | nenhuma alteração adicional                      |
| **5. Implementar validity**    | `valid_from`, `valid_to`, supersession           |
| **6. Executar proposta**       | mesmos 500 itens                                 |
| **7. Comparação**              | overall + categorias                             |
| **8. Ablations**               | somente se houver tempo                          |
| **9. LoCoMo**                  | validação secundária opcional                    |
| **10. Análise qualitativa**    | casos de acerto/erro/supersessão                 |

## Minha avaliação após olhar o código

A proposta ficou **mais forte depois da inspeção**.

Antes estávamos pensando genericamente em “HeLa-Mem + temporalidade do Zep”. Isso seria fraco, porque HeLa-Mem já possui temporal decay.

Agora temos uma diferença precisa:

```text
HeLa-Mem
"quando aconteceu?"
"quão recente é?"

              +

nossa alteração inspirada no Zep
"quando esse fato passou a ser verdadeiro?"
"quando deixou de ser verdadeiro?"
"qual fato o substituiu?"
```

E existe um encaixe concreto no código: **a memória semântica já armazena fatos, já possui `metadata`, o dataset já possui timestamps e `question_date`, e essa `question_date` hoje chega à geração mas não ao retrieval**. 

Isso é pequeno o suficiente para uma disciplina e específico o suficiente para produzir uma experimentação séria. O maior ponto a resolver antes de codificar é **reproduzir a baseline e esclarecer as inconsistências entre paper e release atual do HeLa-Mem**.

[1]: https://github.com/getzep/graphiti "GitHub - getzep/graphiti: Build Real-Time Knowledge Graphs for AI Agents · GitHub"
[2]: https://github.com/xiaowu0162/longmemeval?utm_source=chatgpt.com "GitHub - xiaowu0162/LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory (ICLR 2025) · GitHub"
[3]: https://github.com/ReinerBRO/HeLa-Mem "GitHub - ReinerBRO/HeLa-Mem: HeLa-Mem code for LongMemEval · GitHub"
[4]: https://arxiv.org/abs/2501.13956 "[2501.13956] Zep: A Temporal Knowledge Graph Architecture for Agent Memory"
