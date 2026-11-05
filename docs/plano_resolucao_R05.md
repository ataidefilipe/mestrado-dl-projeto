# Plano de resolução — achados da auditoria R05

**Origem:** [`reports/analysis/R05_auditoria_processo_20261104.md`](../reports/analysis/R05_auditoria_processo_20261104.md)
**Objetivo:** chegar a uma conclusão que se sustente para a pergunta da proposta: *"a validade temporal melhora uma memória associativa hebbiana?"*

A ordem abaixo segue o impacto na conclusão e o custo: primeiro o que é barato e pode mudar tudo, depois o que é caro.

| Etapa | O que resolve | Custo de API | Depende de |
|---|---|---|---|
| 0. Preparar ambiente | — | nenhum | — |
| 1. Recuperar artefatos de A | Achado 2 | nenhum | — |
| 2. Diagnóstico dos grafos vazios de A | Achado 2 | baixo (20 itens) | 0, 1 |
| 3. Baseline fiel A* (condicional) | Achados 1 e 2 | **alto** (500 itens, codificação completa) | 2 |
| 4. Medir ruído entre execuções | Achado 5 | baixo (500 respostas + juiz) | 0 |
| 5. Rodar a B0 | Achado 4 | baixo (500 respostas + juiz) | 0 |
| 6. Estatística completa | Achado 6 | nenhum | 4, 5 |
| 7. Sensibilidade de λ, τ, θ | Achado 7 | médio | 5 |
| 8. LoCoMo (opcional) | Achado 8 | alto | 3 ou A atual |
| 8b. Dataset completo | Achado 10 | nenhum (issue) / **muito alto** (rodar no S) | — |
| 9. Corrigir relatório e documentação | Achados 1, 3, 6, 9 | nenhum | 1–6 |

---

## Etapa 0 — Preparar o ambiente

Faça na máquina ou no Colab onde as execuções anteriores rodaram.

```bash
git checkout feat/ablacao-b0
git submodule update --init
pip install sentence-transformers torch openai python-dotenv numpy scipy pandas
```

1. Criar `.env` na raiz com `OPENAI_API_KEY=...` (ou `OPENAI_API_KEYS=k1,k2`).
2. Descompactar os grafos de B sem sobrescrever o que já existe:

```bash
unzip -n results/temporal_encoded_500.zip -d results/longmemeval_temporal_full
```

3. Conferir que a auditoria roda e reproduz o R05:

```bash
python src/analysis/audit_process.py
```

**Pronto quando:** `audit_process.py` mostra 100 itens recodificados e KU 57 / 57 / 65.

---

## Etapa 1 — Recuperar os artefatos semânticos da Baseline A

**Por quê:** é a única forma sem custo de testar o Achado 2.

1. Procurar, na máquina `D:\Python Projetos\mestrado-dl-projeto` ou no Drive do Colab, a pasta `results/longmemeval_baseline_full/` completa, com os arquivos `*_long_term.json`, `*_long_term_kb_graph.json` e os logs da codificação (saída de célula ou `.log`).
2. Se encontrar, contar os grafos vazios e procurar os erros engolidos:

```bash
python -c "import json,glob; fs=glob.glob('results/longmemeval_baseline_full/*_long_term_kb_graph.json'); print(len(fs), 'grafos;', sum(len(json.load(open(f,encoding='utf-8')).get('nodes',{}))==0 for f in fs), 'vazios')"
```

```bash
grep -c "Knowledge extraction error" <arquivo_de_log>
```

3. Se existirem, versionar os arquivos semânticos de A num zip (`results/baseline_semantic_500.zip`), como já foi feito para os episódicos.

**Pronto quando:** há uma resposta documentada para a pergunta "os 360 vazios vêm de erro de extração?". Se os arquivos não existirem mais, registrar isso e seguir para a Etapa 2.

---

## Etapa 2 — Diagnóstico: o código oficial gera grafos vazios por conta própria?

**Por quê:** separar "comportamento do HeLa-Mem" de "falha da nossa execução" com uma amostra barata, **sem modificar o código oficial**. Usar `--workers 1` elimina a condição de corrida no carregamento do modelo de embedding sem tocar no código.

```bash
cd external/HeLa-Mem
export HEBBIAN_MODEL=gpt-4o-mini HEBBIAN_TAU=1e7 HEBBIAN_LEARNING_RATE=0.02 HEBBIAN_DECAY_RATE=0.995 \
       HEBBIAN_ACTIVATION_ALPHA=0.1 HEBBIAN_SPREADING_THRESHOLD=0.4 HEBBIAN_MAX_FLIPPED=3 \
       HEBBIAN_KNOWLEDGE_BUFFER_SIZE=10
python -m hela_mem.encode_longmemeval --data_path data/longmemeval_s.json \
       --output_dir ../../results/diag_baseline_w1 --num_items 20 --start_item 0 --workers 1 2>&1 | tee ../../results/diag_baseline_w1.log
```

Contar os vazios e comparar com o que A tinha nesses mesmos 20 itens (se a Etapa 1 recuperou os arquivos):

```bash
python -c "import json,glob; fs=glob.glob('results/diag_baseline_w1/*_long_term_kb_graph.json'); print(len(fs), 'grafos;', sum(len(json.load(open(f,encoding='utf-8')).get('nodes',{}))==0 for f in fs), 'vazios')"
```

```bash
grep -c "Knowledge extraction error" results/diag_baseline_w1.log
```

**Decisão:**

| Resultado na amostra | Interpretação | Próximo passo |
|---|---|---|
| Quase nenhum grafo vazio (bem abaixo de 72%) | Os 360 vazios de A foram **falha de execução**. A baseline atual está subestimada | **Etapa 3 é obrigatória** |
| Taxa de vazios parecida com 72%, sem erros no log | É comportamento do código oficial | Pular a Etapa 3. Documentar a causa real no relatório (ler o log para entender por que a extração não devolve fatos) |
| Taxa parecida, com erros no log | Falha sistemática (API, chave, modelo) | Corrigir o ambiente e repetir a Etapa 2 |

**Pronto quando:** a tabela acima tem uma linha marcada, com o número de vazios e de erros registrado.

---

## Etapa 3 — Baseline fiel A* (só se a Etapa 2 indicar falha de execução)

**Por quê:** é a premissa número 1 da disciplina, "reproduzir SEM MODIFICAÇÕES". Também corrige o Achado 1, pois usa os scripts oficiais.

**Decisão do usuário (custo × tempo):**

- **Opção 3a, recomendada:** reexecução oficial completa (codificação episódica + semântica + avaliação), via scripts `.sh`, com `WORKERS=1` ou poucos workers. É a reprodução mais defensável. Custo alto: há uma chamada de palavras-chave por nó episódico.
- **Opção 3b:** manter os grafos episódicos atuais de A e refazer só a extração semântica oficial (buffer de 10 turnos). É mais barata, mas exige um script próprio, ou seja, deixa de ser "sem modificações".

Comandos da opção 3a:

```bash
cd external/HeLa-Mem
bash scripts/encode_longmemeval.sh data/longmemeval_s.json ../../results/longmemeval_baseline_fiel 1
```

```bash
bash scripts/eval_longmemeval.sh data/longmemeval_s.json ../../results/longmemeval_baseline_fiel 4
```

Depois, **reconstruir B sobre a memória episódica de A***, para manter a comparação pareada:

```bash
python src/analysis/run_temporal_hela_longmemeval.py --stage all --num_items 500 \
       --reuse_episodic_dir results/longmemeval_baseline_fiel --output_dir results/longmemeval_temporal_fiel
```

**Atenção:** confira que nenhum item termina com grafo semântico vazio, nem em A* nem em B. É o mesmo problema que gerou o Achado 3. Se houver, recodifique só esses itens e **registre** quantos foram e por quê.

**Pronto quando:** A* tem acurácia registrada num novo R03, com os parâmetros iguais aos do script oficial, e B foi refeita sobre A*. A diferença entre A* e o artigo (65,40%) fica documentada, seja ela qual for.

---

## Etapa 4 — Medir o ruído entre execuções

**Por quê:** `temperature=0.7` na geração e no juiz. Sem isso não dá para saber se +22 itens, ou qualquer diferença B0 → B, é maior que o acaso.

```bash
python src/analysis/run_temporal_hela_longmemeval.py --stage eval --ablation none \
       --results_subdir eval_results_b_rerun --num_items 500
```

A subpasta separada é essencial: sem ela, o runner reaproveita os resultados de B como checkpoint e não roda nada de novo.

Comparar B com B' (`compare_ablation.py --b0 <B'>` serve como atalho): o número de pares discordantes entre B e B' é o **piso de ruído**.

**Pronto quando:** há um número "B × B': X ganhos / Y regressões" registrado. Uma comparação entre sistemas só é interpretável se os seus pares discordantes forem claramente maiores que esse piso.

---

## Etapa 5 — Rodar a ablação B0

```bash
python src/analysis/run_temporal_hela_longmemeval.py --stage eval --ablation no_temporal \
       --results_subdir eval_results_b0 --num_items 500 --workers 5
```

```bash
python src/analysis/compare_ablation.py
```

Se a Etapa 3 foi feita, rode a B0 sobre `results/longmemeval_temporal_fiel`, com `--output_dir`.

**Leitura dos resultados:**

| A → B0 | B0 → B | Conclusão possível |
|---|---|---|
| grande | positivo e significativo, acima do piso de ruído | Hipótese **suportada**. Ganho atribuível ao mecanismo temporal, sobretudo em KU |
| grande | ≈ 0 ou dentro do ruído | Hipótese **não suportada**. O ganho vem da extração por sessão. É um resultado negativo válido (AGENT.MD §20) e deve ser reportado como tal |
| grande | negativo | O mecanismo temporal atrapalha. Analisar a supersessão excessiva em contagens (*multi-session*) |
| pequeno | positivo | O mecanismo temporal explica a maior parte do ganho |

**Pronto quando:** `R05_decomposicao_A_B0_B_*.md` foi gerado e a linha da tabela acima foi escolhida com base nos números, **sem ajustar nada depois de ver o resultado** (§24).

---

## Etapa 6 — Estatística completa

Estender `compare_ablation.py` com:

1. **Intervalo de confiança de 95%** para a diferença pareada de acurácia (bootstrap pareado com 10.000 reamostragens, ou Newcombe para proporções pareadas).
2. **Correção de Holm** nos testes por categoria (6 categorias × 2 comparações).
3. O **teste bilateral** como principal. O unilateral só vale se a direção tiver sido fixada antes (a proposta fixou: B ≥ A em KU e TR).
4. A comparação com o piso de ruído da Etapa 4.

**Pronto quando:** toda afirmação de ganho no relatório vem com IC e p corrigido. Ganhos por categoria sem significância são descritos como "tendência".

---

## Etapa 7 — Sensibilidade de λ, τ e θ (não seleção)

**Por quê:** AGENT.MD §19. Não há conjunto de validação separado, então os 500 itens são o teste.

**Regra fixada antes de rodar:** a configuração reportada continua sendo λ = 0,6, τ = 60 d, θ = 0,35. A variação serve só para classificar o resultado como **robusto, sensível ou inconclusivo**.

- λ e τ só afetam a busca, então basta a etapa de avaliação:

```bash
TEMPORAL_LAMBDA=0.4 python src/analysis/run_temporal_hela_longmemeval.py --stage eval --ablation none --results_subdir eval_results_l04 --num_items 500
```

Repetir para λ = 0,8 e para τ = 30 e 90 dias (`TEMPORAL_TAU_DECAY` em segundos: 2592000 e 7776000).

- θ afeta a codificação: exige recodificar a parte semântica, que é mais cara. Fazer com uma amostra estratificada (por exemplo, todos os 78 de KU) ou deixar como limitação.

Cada variação usa sua própria `--results_subdir`, pelo mesmo motivo da Etapa 4.

**Pronto quando:** há uma tabela de sensibilidade com a classificação final e a afirmação explícita de que a configuração não foi escolhida por esses resultados.

---

## Etapa 8 — LoCoMo (opcional, conforme o prazo)

**Por quê:** a diretriz pede mais de um dataset, e o artigo-base usa LoCoMo.

1. Reproduzir o HeLa-Mem no LoCoMo com `scripts/encode_locomo.sh` e `scripts/eval_locomo.sh`, sem modificações.
2. Adaptar o runner temporal para o LoCoMo, que tem formato próprio e datas por sessão.
3. Rodar A, B0 e B.

Se não houver tempo: registrar como limitação explícita no artigo final, citando que o LoCoMo tem menos questões de atualização de conhecimento e por isso testaria mais a ausência de dano do que o ganho.

---

## Etapa 8b — Dataset completo (Achado 10)

1. ~~Confirmar no artigo do HeLa-Mem (seção de experimentos e apêndice) qual arquivo do LongMemEval foi usado para os 65,40%.~~ **Feito em 2026-11-05, sem conclusão:** o Apêndice D diz apenas "LongMemEval-S, a 500-item … benchmark", sem estatísticas do histórico. Os baselines vêm do LightMem, que usa o S de cerca de 115 mil tokens. O README do HeLa-Mem chama de "complete 500-item LongMemEval-S" o arquivo que, na verdade, é oracle. Detalhes no Achado 10 da auditoria.
2. Abrir uma issue no repositório do HeLa-Mem (github.com/ReinerBRO/HeLa-Mem) perguntando qual arquivo gerou as Tabelas 6 e 7 do Apêndice D e se `data/longmemeval_s.json` é intencionalmente a variante oracle. É a única forma barata de fechar a questão.
3. No relatório, descrever os resultados como "LongMemEval, 500 questões, histórico apenas de evidência (equivalente ao oracle)" e não comparar numericamente com o artigo nem com os baselines da Tabela 6 (Etapa 9, item 5).
4. Se houver tempo, rodar A e B no `longmemeval_s_cleaned.json` oficial (cerca de 40 sessões por item). O custo é alto, porque a codificação cresce com o número de sessões. Começar com uma amostra estratificada (por exemplo, os 78 itens de KU) para estimar custo e efeito.

---

## Etapa 9 — Corrigir o relatório e a documentação

No relatório (`relatorio_entrega2_draft2.md` e `.tex`, ou na versão final):

1. **Reprodução:** trocar "reprodução sem modificações" por uma descrição exata, incluindo os desvios `MAX_FLIPPED` 5 ≠ 3 e `KEYWORD_WEIGHT` 0,5 ≠ 0,7, ou os resultados de A* se a Etapa 3 foi feita.
2. **Grafos vazios de A:** substituir a explicação do buffer pela causa apurada nas Etapas 1 e 2.
3. **Recodificação dos itens 100–199:** registrar o critério (grafo vazio), a contagem (100) e o efeito (64,60% → 65,60%; KU 57 → 65).
4. **Desenho experimental:** apresentar A → B0 → B, e não só A → B.
5. **Comparação com o artigo:** remover "supera o artigo oficial". Usar "equivalente ao artigo" ou comparar só com A*.
6. **Estatística:** IC, Holm, piso de ruído (Etapa 6).
7. **Limitações:** temperatura 0,7 sem repetições, hiperparâmetros sem validação separada, um único dataset (se a Etapa 8 não for feita), juiz LLM igual ao modelo gerador.

No repositório:

1. `requirements.txt`: cabeçalho correto e inclusão de `openai`, `python-dotenv` e `sentence-transformers`, com versões fixadas (`pip freeze` do ambiente usado).
2. Versionar os resultados que faltam: semântica de A, B0, B', A* (zips, como os atuais).
3. Mover o GraphSAGE/PPI (código e R01/R02) para uma pasta `legado/` ou marcar como fora do escopo no README.
4. `tests/`: pelo menos um teste de `compute_temporal_pertinence`, do modo B0 (o teste offline já usado na implementação) e de `mcnemar_exact`.
5. Atualizar o `origin` para o nome atual do repositório (`mestrado-dl-projeto`).

**Pronto quando:** o checklist do AGENT.MD §28 pode ser marcado sem ressalvas.

---

## Registro de progresso

| Etapa | Status | Data | Resultado / link |
|---|---|---|---|
| 0 | concluída | 2026-11-04 | Ambiente configurado via uv e dependências validadas. |
| 1 | concluída | 2026-11-05 | 500 grafos semânticos e episódicos de A recuperados em `results/longmemeval_baseline_full`; 360 vazios confirmados. |
| 2 | concluída | 2026-11-05 | Teste diagnóstico no item 400 (`workers=1`) gerou 9 nós semânticos com código oficial. Falha de concorrência comprovada nos 360 vazios de A. Ver `reports/analysis/R06_diagnostico_baseline_e_ruido_Bprime_Bv2_20261105.md`. |
| 3 | em andamento | 2026-11-05 | Opção A selecionada: geração da Baseline Fiel ($A^*$) com parâmetros oficiais em `results/longmemeval_baseline_fiel/`. |
| 4 | concluída | 2026-11-05 | Piso de ruído medido com $B'$ (64,00% ACC, 36 discordantes [7,20%]; KU idêntico em 83,33% com 97,4% de estabilidade). |
| 5 | concluída | 2026-11-04 | B0 = 64,20%. A→B0 +15 (p=0,11); B0→B +7 (p=0,45); KU B0→B +14/−0 (Holm p=0,0015); MS B0→B −7. `reports/analysis/R05_decomposicao_A_B0_B_20261104_205642.md`. |
| 6 | concluída | 2026-11-05 | Estatística completa implementada com McNemar exato, IC 95% e correção de Holm em `compare_ablation.py`. |
| — | concluída | 2026-11-05 | **Proposta $B_{\text{v2}}$ (Classificador Ontológico Sem Exemplos):** 64,80% ACC geral, $KU$ 79,49% ($p=0,0034$), $TR$ 57,89% (recorde), redução de regressões em $MS$. |
| 7 | pendente | | Sensibilidade de λ, τ, θ. |
| 8 | opcional | | Segundo dataset (LoCoMo). |
| 8b | em andamento | 2026-11-05 | Passo 1 feito: o artigo não informa qual arquivo usou; os baselines são do S de cerca de 115 mil tokens (LightMem); o arquivo distribuído é oracle. Falta a issue aos autores e a execução no S oficial. Ver Achado 10. |
| 9 | em andamento | 2026-11-05 | Documentação em `README.md`, `VISAO_GERAL_PROJETO.md` e relatórios técnicos R05/R06. |
