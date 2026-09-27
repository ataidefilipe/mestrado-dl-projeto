# Seleção do Artigo Base — Reenquadramento de 19/09/2026

**Status:** em aberto. Quatro candidatos triados, nenhum escolhido. Busca continua.

> **Por que este documento existe.** O `04-reenquadramento.md` escolheu o cenário C (três braços,
> GraphSAGE como pós-processamento) partindo do tema — a Reforma Tributária. Uma revisão contra o
> briefing do professor mostrou que essa ordem estava invertida. Este documento registra a inversão,
> o critério de seleção que saiu dela, e os candidatos avaliados.

---

## 1. O diagnóstico que motivou a revisão

O desenho do cenário C **não evolui o artigo base**. O teste que prova isso:

> Troque o GraphSAGE por GCN, GAT ou qualquer outra GNN no braço 3. A pergunta de pesquisa não muda,
> a estrutura do estudo não muda, as conclusões possíveis não mudam.

Se o artigo base é intercambiável, o projeto o está **usando como peça**, não evoluindo. As varreduras
de agregador e profundidade K não resolvem: `mean`/`max-pool`/`LSTM` é a Tabela 1 do próprio artigo e
K=1,2,3 é a §4.4 — rodar isso num grafo novo é replicação em dado novo, não evolução.

O `03-requisitos-professor.md` já reconhecia isso no GAP 3 ("honestamente: não") e escapava pela
cláusula *"pretende fazer um estudo comparativo?"* do slide 8. É saída legítima, mas parcial: o
comparativo não compara variantes do método base.

**Decisão:** escolher o artigo base **pelo artigo**, não pelo tema. O domínio de aplicação passa a ser
consequência da escolha, não premissa dela.

---

## 2. Os 5 filtros de seleção

Um candidato precisa passar em **todos**. Ordenados por velocidade de eliminação.

| # | Pergunta | Elimina quando |
|---|---|---|
| 1 | Existe **loss e época**? | A contribuição é orquestração de LLM, serving, busca em código, prompt engineering ou harness de avaliação |
| 2 | Dá para **treinar a baseline** no hardware disponível? | A menor instanciação honesta pede multi-GPU ou dias de treino |
| 3 | A técnica está **alcançável**? | Ela vive no pré-treino e só há checkpoint liberado, ou o gerador de dados é proprietário |
| 4 | O fenômeno **sobrevive à escala pequena**? | A capacidade estudada é emergente e some junto com o modelo |
| 5 | Existe **artigo**? | É nota de release, model card ou post de blog |

Hardware de referência: CPU local sem GPU NVIDIA, mais Colab gratuito (T4, ~16 GB, sessões curtas).
Alvo ideal de tamanho: abaixo de 500M parâmetros, preferencialmente abaixo de 100M.

### O critério decisivo, e o menos óbvio

O artigo precisa ter uma **costura exposta**: uma escolha de projeto feita sem justificativa, ou um
contorno que os autores admitem. É ali que mora a modificação. Artigo redondo demais não dá o que
modificar e empurra de volta para "aplicar em domínio novo".

Formas típicas: *"we use X for simplicity"*, *"we found this worked well in practice"*, *"we leave
this to future work"*, ou admissão de propriedade violada com remendo por cima. Bônus forte quando o
artigo tem ablação que quantifica o custo de alguma escolha — isso dá piso e teto para julgar a
modificação.

### As 4 condições da estratégia "técnica nova em modelo menor"

1. A técnica tem que ser **separável da escala** — mecanismo, não comportamento emergente.
2. Você tem que conseguir **treinar a baseline** — sem isso não existe com/sem.
3. A técnica **não pode estar assada dentro do checkpoint** — se vive no pré-treino, fine-tuning não a alcança.
4. A **limitação de escala vai declarada** como seção de limitações.

---

## 3. Os quatro candidatos triados

Ordenados por viabilidade de reprodução fiel. Nenhum escolhido ainda.

### A — DLinear

| | |
|---|---|
| **Artigo** | *Are Transformers Effective for Time Series Forecasting?* · AAAI 2023 · [arXiv 2205.13504](https://arxiv.org/abs/2205.13504) |
| **Código** | github.com/cure-lab/LTSF-Linear · Apache-2.0 · scripts de treino completos |
| **Modelo** | ~65k parâmetros (seq_len=336, pred_len=96). Segundos em CPU |
| **Reprodução** | **Integral** — 9 datasets, todos os horizontes, todas as seeds |
| **Dados** | ETTh1/h2, ETTm1/m2, Electricity, Traffic, Weather, Exchange, ILI. MSE/MAE. Públicos |

**Costura (verificada pessoalmente no código-fonte):** em `models/DLinear.py`,

```python
kernel_size = 25
self.decompsition = series_decomp(kernel_size)
```

O `configs` é lido apenas para `seq_len`, `pred_len`, `individual` e `enc_in` — **`configs.moving_avg`
nunca é acessado**. E em `run_longExp.py` existe
`parser.add_argument('--moving_avg', type=int, default=25, help='window size of moving average')`.
A flag existe, está documentada no `help`, e é **silenciosamente ignorada pelo DLinear**.

No apêndice B.2 a única justificativa do valor é imitação: *"the moving average kernel size for
decomposition is 25, which is the same as Autoformer."* Não há ablação do kernel.

**Modificação habilitada:** decomposição adaptativa ou aprendida no lugar da média móvel fixa.
Hipótese física: 25 passos são 25 minutos no ETTm e 25 horas no ETTh — o mesmo número não pode estar
correto nas duas granularidades.

**Risco:** a costura pode se revelar irrelevante ("o kernel não importa"). Mitigação: a incoerência
entre granularidades sustenta a análise mesmo com ganho nulo, e resultado negativo é aceito pelo slide 8.

---

### B — FineWeb-Edu classifier

| | |
|---|---|
| **Artigo** | *The FineWeb Datasets* · **NeurIPS 2024 D&B — Spotlight** · [arXiv 2406.17557](https://arxiv.org/abs/2406.17557) |
| **Código** | github.com/huggingface/cosmopedia · Apache-2.0 · `classification/train_edu_bert.py` |
| **Modelo** | Snowflake arctic-embed-m, 109M — **mas encoder congelado**, ~591k treináveis (0,54%) |
| **Reprodução** | **Integral**, ~2 h em T4 numa sessão (ver abaixo) |
| **Dados** | `HuggingFaceFW/fineweb-edu-llama3-annotations` — ODC-BY, público, 467.424 linhas |

**Por que cabe no orçamento:** o treino congela embeddings e encoder. Reprodução ingênua seriam 20–30 h
de T4; como o encoder é congelado, dá para pré-computar os embeddings uma vez (~1–1,5 h) e treinar a
cabeça de 591k parâmetros em minutos. Cada variante posterior custa minutos — permite 10–20 rodadas
com 3 seeds numa sessão.

**Costuras (quatro, reportadas por agente de pesquisa com trechos literais):**

1. **Regressão + arredondamento, sem ablação.** `num_labels=1` e
   `preds = np.round(logits.squeeze()).clip(0, 5)`. O rótulo é escala **ordinal**, e MSE trata a
   distância 0↔1 como igual a 4↔5. Nunca comparado contra classificação ou formulação ordinal.
2. **Threshold 3 ablado só a jusante.** A Figura 17 compara thresholds treinando LMs de ablação
   (centenas de GPU-h, inacessível). Não há ablação no espaço do classificador.
3. **O F1 de 82% divulgado esconde macro-F1 de 0,50.** Por classe, a classe 5 tem **F1 = 0,02**, e a
   fronteira de decisão usada em produção opera em F1 ≈ 0,53.
4. **Desalinhamento professor↔aluno.** O Llama-3 julgou ~1.533 caracteres; o aluno tokeniza até 512
   tokens do texto completo. Não discutido no artigo.

**Modificação habilitada:** cabeça ordinal calibrada (CORN/CORAL) no lugar de regressão+arredondamento,
e mover a escolha do threshold para dentro do classificador (custo assimétrico / precisão-alvo) em vez
de fixá-lo em 3. Métrica: QWK e macro-F1 nas classes 3–5.

**Risco:** ground truth ruidoso — mede-se concordância com um professor imperfeito. Mitigação
obrigatória: anotar 200–500 documentos manualmente para checar que o ganho não é overfit ao viés do Llama-3.

**Precedente metodológico útil:** FinerWeb-10BT (NoDaLiDa 2025, arXiv 2501.07314, MIT) calibra a saída
por Platt em vez de arredondar — transforma a modificação de "ideia minha" em "prática validada em
outra pipeline".

---

### C — PairRanker (LLM-Blender)

| | |
|---|---|
| **Artigo** | *LLM-Blender* · ACL 2023 · [arXiv 2306.02561](https://arxiv.org/abs/2306.02561) |
| **Código** | github.com/yuchenlin/LLM-Blender · Apache-2.0 · `train_ranker.py` |
| **Modelo** | DeBERTa-v3-large, 435M |
| **Reprodução** | **Parcial** — subset de 10–20k contra os 100k do MixInstruct |
| **Dados** | `llm-blender/mix-instruct` — MIT, público, 100k/5k/5k |

**Costura principal (a melhor encontrada em toda a busca):** os autores **admitem** assimetria por
construção e remendam com data augmentation em vez de corrigir a arquitetura:

> *"Due to the position embeddings of the language model, the order of the candidates in a pair
> (x,yi,yj) matters... Thus, we shuffle the order of candidates within each training pair so that the
> model learns to be consistent with itself."*

A inconsistência residual **nunca é medida**. Outras duas: *"using 5 pairs per input is sufficient for
obtaining decent results"* (de 55 pares possíveis, sem ablação) e *"we find BCE is simply good enough"*
(admissão explícita de não-otimização, sem ablação quantitativa).

**Modificação habilitada:** cabeça antissimétrica por construção ou loss Bradley-Terry, medindo a taxa
de inconsistência `s(i,j)` contra `s(j,i)` — métrica que o artigo nunca reporta.

**Riscos:** abre mão da reprodução fiel antes de começar (40–80 h de T4 para o treino completo). Deriva
do repositório: o `train_ranker.sh` está hoje em phi-2 com 8×A100 e DeepSpeed ZeRO-3; voltar à config
do paper exige editar o script e possivelmente um commit mais antigo.

---

### D — Set-Encoder

| | |
|---|---|
| **Artigo** | *Set-Encoder* · ECIR 2025 · [arXiv 2404.06912](https://arxiv.org/abs/2404.06912) |
| **Código** | github.com/webis-de/set-encoder · **sem licença declarada** |
| **Modelo** | ELECTRA-base, 110M |
| **Reprodução** | **Parcial** — estágio 1 (20k passos × batch 32 × 8 passagens) não cabe no Colab grátis |
| **Dados** | MS MARCO passage, TREC DL 19/20. nDCG@10 e α-nDCG@10. Públicos via `ir_datasets` |

**Costura:** o mecanismo central é declarado como hipótese e nunca justificado —
*"We hypothesize that our additional [INT] token can also aggregate semantic information and share this
information with other passages."* Um **único** token por passagem como canal de comunicação. Os autores
ablacionam **qual** token (`[INT]` vs `[CLS]`) e nunca **quantos**, embora admitam ser um espectro:
*"using single tokens for passage interactions is on the efficiency end of a spectrum."*

**Modificação habilitada:** alargar o canal inter-passagem para k tokens (k=2/4/8) e medir o trade-off
efetividade/custo — a ablação que falta no artigo.

**Riscos:** repositório sem licença; `bf16-mixed` não roda em T4; acoplamento a versão em evolução da
`lightning-ir` (pinar commit é obrigatório); e os próprios autores registram que o ganho em relevância
é pequeno — *"the pointwise monoELECTRA model features similar effectiveness"*.

---

## 4. Comparação

| | Reprodução fiel completa? | Custo | Venue | Costuras |
|---|---|---|---|---|
| **A · DLinear** | **sim** | segundos, CPU | AAAI 2023 | 1, verificada no código |
| **B · FineWeb-Edu** | **sim** | ~2 h, uma sessão | **NeurIPS 2024 Spotlight** | 4 |
| C · PairRanker | não — só subset | 5–10 h, 2–3 sessões | ACL 2023 | 3, uma excelente |
| D · Set-Encoder | não — só reduzido | várias sessões | ECIR 2025 | 1 |

O slide 6 exige reproduzir **sem modificações antes de qualquer coisa**. Apenas **A** e **B** permitem
isso dentro do hardware disponível. C e D obrigam a declarar reprodução parcial já na concepção.

---

## 5. Descartados, com motivo

Registro para não re-litigar. **17 candidatos** vieram de feeds de trending (HuggingFace papers,
paperswithcode); **1 passou** (GLiNER2). O padrão: feeds de trending premiam release de modelo de
fronteira, framework de agente e paper de infraestrutura.

**Por falta de loss/época (filtro 1):** TradingAgents, Self-Evolving Search Index, Meta-Harness
(COLM 2026), MatrAIx, AI for Games (survey), PagedAttention/vLLM.

**Por custo (filtro 2):** Agent Lightning, NeoHorse-1, Harness-1, LynnReal-Omni, DeepSeek-V4.1-Flash,
Dream-RSI, xCOMET-lite (14M exemplos), UniEval (t5-v1.1-**large** 783M, não base — verificado no
`config.json`; OOM garantido em T4).

**Por técnica inalcançável (filtro 3):** LimiX-2 (código de pré-treino e gerador de dados por SCM
**não liberados**); Kronos pela rota do checkpoint (a tokenização vive no pré-treino);
*LLM Distillation for Efficient Few-Shot MCQA* (2412.09807, Findings EMNLP 2025 — costura ótima, **sem
repositório em lugar nenhum**).

**Por escala-dependência (filtro 4):** Context-Folding (ICML 2026) — gestão de contexto em horizonte
longo não sobrevive em modelo pequeno.

**Por não existir artigo (filtro 5):** Bonsai 27B (anúncio de release), GLiNER2.5 (nota de release sem
arXiv), JEV (zero resultados no arXiv; site `simplejev.ai` **bloqueado pelo filtro de DNS corporativo
como ameaça de segurança** — não contornado).

**Trilha guardrail, descartada após inspeção de repositório:** Llama Guard (zero código de treino),
ShieldGemma (sem venue, dados internos), WildGuard (só inferência, Mistral-7B), Aegis (menor modelo 7B),
NeMo Guardrails (framework), Llama Prompt Guard 2 (sem paper), LionGuard (repo inexistente; v2 depende
de API paga da OpenAI), Granite Guardian (sem código de treino), ToxicChat (T5-large 770M).

**Costuras já abladas pelos próprios autores:** PatchTST (Figura 4 conclui que o MSE não varia
significativamente com o patch length), SimCSE (dropout, τ e α medidos nas Tabelas 3, D.1 e 7),
PURE (W=100 ablado na Figura 2, e ACE04/05 atrás de licença LDC).

**Sobreviventes não promovidos:** GLiNER2 (arXiv 2507.18546, ACL-adjacente, Apache-2.0, 74M — a costura
é enumeração de spans vs. predição de fronteira, e o GLiNER2.5 que usa fronteira saiu **sem artigo**,
logo ninguém publicou comparação controlada); HarmAug (ICLR 2025, arXiv 2410.01524 — α=0,5 hard-coded
entre CE e KL, sem temperatura de destilação, sem ablação); SetFit (venue de workshop);
COMET (`nr_frozen_epochs: 0.3` como número mágico).

---

## 6. Ressalvas de método

Seguindo o `AGENT.MD` §21, separo o que verifiquei do que foi reportado:

- **Verificado pessoalmente:** o `kernel_size = 25` hardcoded e a flag `--moving_avg` ignorada no
  DLinear (li o fonte de `models/DLinear.py` e `run_longExp.py`); a inexistência de artigo do
  GLiNER2.5 e do JEV no arXiv; o bloqueio de DNS do `simplejev.ai`.
- **Reportado por agentes de pesquisa, não re-verificado por mim:** todos os trechos literais de
  FineWeb-Edu, PairRanker, Set-Encoder e HarmAug, e os números de custo em T4. Antes de fechar a
  escolha, o candidato vencedor precisa ter suas costuras conferidas no fonte.
- **Lacuna conhecida de cobertura:** um dos agentes tratou IDs de arXiv de 2026 (`2603.*`, `2605.*`)
  como "ruído de índice" por noção errada da data atual. A cobertura de artigos de 2026 no domínio de
  julgamento/scoring é **não confiável** e pode ter descartado candidato legítimo.
- **Não lido:** pareceres do OpenReview do FineWeb (`n6SCkn2QaG`) — a API exigiu verificação anti-bot.

---

## 7. Destino do corpus da Reforma Tributária

Decisão registrada: **em suspenso**, a decidir depois dos resultados. Deixa de ser objetivo e passa a
ser, no máximo, domínio de transferência — "a conclusão obtida nos benchmarks do artigo se sustenta
neste corpus?". O trabalho de `01-levantamento-corpus.md` fica preservado, não descartado.

O que já estava feito e permanece válido independentemente da escolha: a reprodução fiel do GraphSAGE
com equivalência exata ao `SAGEConv` (`R02`), que continua sendo evidência do slide 6 caso o GraphSAGE
volte a ser o artigo base.
