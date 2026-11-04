**Título da proposta**

**Incorporação de Validade Temporal em Memória Associativa Hebbiana para Agentes Baseados em LLM**

**Equipe**

**Filipe Augusto de Ataide Barbosa**
E-mails: filipeataide@gmail.com; faab@cin.com.br

**Link para o artigo base**

**HeLa-Mem: Hebbian Learning and Associative Memory for LLM Agents** — ACL 2026
[Artigo na ACL Anthology](https://aclanthology.org/2026.acl-long.625)

O artigo propõe uma arquitetura de memória de longo prazo para agentes baseada em um grafo dinâmico, com aprendizado hebbiano, memória episódica e memória semântica. As associações entre memórias são reforçadas a partir de padrões de coativação e utilizadas durante a recuperação. ([ACL Anthology](https://aclanthology.org/2026.acl-long.625))

**Link para o código base**

**Implementação oficial do HeLa-Mem**
[Repositório oficial no GitHub](https://github.com/ReinerBRO/HeLa-Mem)

O repositório disponibiliza a implementação utilizada para os experimentos e já inclui suporte ao benchmark LongMemEval-S. ([GitHub](https://github.com/ReinerBRO/HeLa-Mem?utm_source=chatgpt.com))

**Quais dados serão usados para validar a proposta**

O principal conjunto de dados será o **LongMemEval-S**, benchmark voltado à avaliação de memória de longo prazo em agentes conversacionais.

O benchmark contém **500 instâncias de avaliação** com histórico conversacional timestampado, pergunta, resposta esperada, data da pergunta e categoria da questão. Entre as categorias estão:

* raciocínio temporal;
* atualização de conhecimento;
* raciocínio entre múltiplas sessões;
* recuperação em uma única sessão;
* abstention.

Essas categorias são particularmente adequadas à proposta porque permitem avaliar separadamente o efeito da modificação em situações nas quais uma informação muda ao longo do tempo. ([GitHub](https://github.com/xiaowu0162/LongMemEval/blob/main/README.md))

O próprio repositório do HeLa-Mem já inclui o arquivo completo com as 500 instâncias do LongMemEval-S, facilitando a reprodução dos experimentos do artigo-base. ([GitHub](https://github.com/ReinerBRO/HeLa-Mem))

**Resumo da proposta**

O trabalho parte do **HeLa-Mem**, uma arquitetura de memória associativa para agentes baseados em LLM que representa memórias por meio de um grafo dinâmico e utiliza aprendizado hebbiano para fortalecer associações entre informações recuperadas conjuntamente. ([ACL Anthology](https://aclanthology.org/2026.acl-long.625))

A proposta consiste em investigar uma limitação específica da representação temporal atual: **o momento em que uma memória foi registrada não é necessariamente equivalente ao período durante o qual o fato representado por ela permaneceu válido**.

Por exemplo, a informação “João é responsável pelo projeto” pode ser verdadeira durante determinado período e posteriormente ser substituída por “Maria é responsável pelo projeto”. A informação anterior continua historicamente correta, mas não representa mais o estado atual.

A evolução proposta será incorporar ao HeLa-Mem um mecanismo explícito de **validade temporal e supersessão de fatos**, inspirado em arquiteturas de knowledge graphs temporais. Dessa forma, fatos poderão manter informações como início e fim de validade e a relação com fatos que os substituíram.

O experimento comparará:

HeLa-Mem original

vs.

HeLa-Mem + validade temporal dos fatos

Os demais elementos do experimento serão mantidos constantes para permitir uma comparação controlada.

A principal pergunta de pesquisa será:

**A representação explícita da validade e da supersessão temporal de fatos melhora uma memória associativa hebbiana em tarefas de atualização de conhecimento e raciocínio temporal?**

A proposta será avaliada principalmente nas categorias **Knowledge Update** e **Temporal Reasoning** do LongMemEval-S, além da análise do desempenho global e das demais categorias. O objetivo não é necessariamente obter desempenho superior: resultados positivos, neutros ou negativos serão analisados para determinar em quais tipos de tarefa a representação explícita da validade temporal é útil.