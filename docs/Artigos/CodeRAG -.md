|     | CodeRAG:            |     | Finding |     | Relevant |                  | and Necessary |      | Knowledge  |     |     | for |     |
| --- | ------------------- | --- | ------- | --- | -------- | ---------------- | ------------- | ---- | ---------- | --- | --- | --- | --- |
|     | Retrieval-Augmented |     |         |     |          | Repository-Level |               | Code | Completion |     |     |     |     |
ShengZhang1,†, YifanDing1,†, ShuquanLian1, ShunSong2, HuiLi1,§
1KeyLaboratoryofMultimediaTrustedPerceptionandEfficientComputing
MinistryofEducationofChina,XiamenUniversity
2AntGroup
{sheng,dingyf,shuquanlian}@stu.xmu.edu.cn, songshun.ss@antgroup.com
hui@xmu.edu.cn
|                  |     | Abstract |                 |     |           |     | filethattheprogrammerisworkingon)(Lietal., |     |            |     |          |            |     |
| ---------------- | --- | -------- | --------------- | --- | --------- | --- | ------------------------------------------ | --- | ---------- | --- | -------- | ---------- | --- |
|                  |     |          |                 |     |           |     | 2018; Wang                                 | and | Li, 2021). |     | However, | real-world |     |
| Repository-level |     |          | code completion |     | automati- |     |                                            |     |            |     |          |            |     |
softwaresourcecodegenerallyconsistsofmultiple
| cally | predicts | the | unfinished | code | based | on  |     |     |     |     |     |     |     |
| ----- | -------- | --- | ---------- | ---- | ----- | --- | --- | --- | --- | --- | --- | --- | --- |
codefileswithcomplexinterdependencies,which
| the | broader | information |     | from the | repository. |     |                              |     |     |     |                |     |     |
| --- | ------- | ----------- | --- | -------- | ----------- | --- | ---------------------------- | --- | --- | --- | -------------- | --- | --- |
|     |         |             |     |          |             |     | wereneglectedbyearlymethods. |     |     |     | Thesecodefiles |     |     |
RecentstridesinCodeLargeLanguageMod-
|     |       |       |              |     |              |     | areessential | ingredientsfor |     |     | programmers |     | tocon- |
| --- | ----- | ----- | ------------ | --- | ------------ | --- | ------------ | -------------- | --- | --- | ----------- | --- | ------ |
| els | (code | LLMs) | have spurred |     | the develop- |     |              |                |     |     |             |     |        |
mentofrepository-levelcodecompletionmeth- sider when developing unfinished code and they
ods,yieldingpromisingresults. Nevertheless, aretypicallyorganizedasasourcecoderepository.
they suffer from issues such as inappropriate Thus, a practical code completion tool should be
queryconstruction,single-pathcoderetrieval, repository-levelandleveragebothcodecontextand
andmisalignmentbetweencoderetrieverand
informationretrievedfromtheentirecodebaseto
codeLLM.Toaddresstheseproblems,wein-
|         |          |     |             |     |          |     | provide | more | accurate | and | comprehensive |     | code |
| ------- | -------- | --- | ----------- | --- | -------- | --- | ------- | ---- | -------- | --- | ------------- | --- | ---- |
| troduce | CodeRAG, |     | a framework |     | tailored | to  |         |      |          |     |               |     |      |
suggestions(Zhangetal.,2023).
identifyrelevantandnecessaryknowledgefor
retrieval-augmentedrepository-levelcodecom- Sincerepository-levelcodecompletioncanbet-
pletion. Itscorecomponentsincludelogprob- ter facilitate collaborative development and soft-
| ability | guided | query | construction, |     | multi-path |     |                   |     |       |     |         |     |         |
| ------- | ------ | ----- | ------------- | --- | ---------- | --- | ----------------- | --- | ----- | --- | ------- | --- | ------- |
|         |        |       |               |     |            |     | ware maintenance, |     | there | is  | a surge | of  | work in |
coderetrieval,andpreference-alignedBESTFIT
|            |     |           |             |     |           |     | this direction |     | (Zhang     | et al., | 2023; | Liu     | et al., |
| ---------- | --- | --------- | ----------- | --- | --------- | --- | -------------- | --- | ---------- | ------- | ----- | ------- | ------- |
| reranking. |     | Extensive | experiments |     | on bench- |     |                |     |            |         |       |         |         |
|            |     |           |             |     |           |     | 2024; Cheng    | et  | al., 2024) | and     | most  | of them | con-    |
marksReccEvalandCCEvaldemonstratethat
|         |     |               |     |              |     |      | sider applying |     | Retrieval-Augmented |     |     | Generation |     |
| ------- | --- | ------------- | --- | ------------ | --- | ---- | -------------- | --- | ------------------- | --- | --- | ---------- | --- |
| CodeRAG |     | significantly | and | consistently |     | out- |                |     |                     |     |     |            |     |
performsstate-of-the-artmethods. Theimple- (RAG),aprevalentsolutionincorporatingexternal
mentationofCodeRAGisavailableathttps:
knowledgetohelpLLMsgeneratemoreaccurate
//github.com/KDEGroup/CodeRAG. text(Gaoetal.,2023). BasedontheideaofRAG,
|     |     |     |     |     |     |     | these methods |     | retrieve | relevant | code | knowledge |     |
| --- | --- | --- | --- | --- | --- | --- | ------------- | --- | -------- | -------- | ---- | --------- | --- |
1 Introduction
fromtheentirerepositoryassupplementarytocode
contextwhenpredictingtheunfinishedcode.
| Recent | years | havewitnessed |     | the remarkablesuc- |     |     |     |     |     |     |     |     |     |
| ------ | ----- | ------------- | --- | ------------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- |
cessofLargeLanguageModels(LLMs)invarious Despitetheblossomofrelatedapproaches,they
areas (Zhao et al., 2023). As a branch of LLMs, stillsufferfromthefollowingshortcomings:
| Code | Large Language |     | Models | (code | LLMs), | are | •   |     |     |     |     |     | Previ- |
| ---- | -------------- | --- | ------ | ----- | ------ | --- | --- | --- | --- | --- | --- | --- | ------ |
P1: InappropriateQueryConstruction.
| trained    | on massive |              | code data, | enabling  | them | to       |                                |     |     |     |     |             |     |
| ---------- | ---------- | ------------ | ---------- | --------- | ---- | -------- | ------------------------------ | --- | --- | --- | --- | ----------- | --- |
|            |            |              |            |           |      |          | ousapproachesuseeitherthelastk |     |     |     |     | linesbefore |     |
| comprehend |            | and generate | code       | snippets, |      | thus as- |                                |     |     |     |     |             |     |
thecursorposition(Tanetal.,2024)orthelast
sistingprogrammersincodingtasksandboosting
|     |     |     |     |     |     |     | k lines | together | with | the | generated | code | from |
| --- | --- | --- | --- | --- | --- | --- | ------- | -------- | ---- | --- | --------- | ---- | ---- |
developmentefficiency(Nijkampetal.,2023;Roz-
codeLLM(Zhangetal.,2023)asthequeryfor
ièreetal.,2023;Lietal.,2023).
coderetrievalandfindrelevantcodeknowledge
AtypicalapplicationofcodeLLMsiscodecom-
|     |     |     |     |     |     |     | to assist | completion, |     | causing | information |     | loss |
| --- | --- | --- | --- | --- | --- | --- | --------- | ----------- | --- | ------- | ----------- | --- | ---- |
pletion, which automatically predicts the unfin- andintroducingnoises. Forexample,program-
| ishedcode(Svyatkovskiyetal.,2019). |     |     |     |     | Earlycode |     |          |        |     |           |     |              |     |
| ---------------------------------- | --- | --- | --- | --- | --------- | --- | -------- | ------ | --- | --------- | --- | ------------ | --- |
|                                    |     |     |     |     |           |     | mers may | define | key | variables |     | and classes, | or  |
completionmethodssolelyleveragecodecontext
importpackagesatthebeginningofafile,which
(i.e.,informationfromthefunctionorsourcecode
areessentialforunderstandingandcompleting
|     |     |     |     |     |     |     | thecodeaccurately. |     |     | Ifthelastk |     | linescontainir- |     |
| --- | --- | --- | --- | --- | --- | --- | ------------------ | --- | --- | ---------- | --- | --------------- | --- |
†Thefirsttwoauthorscontributeequally.
§HuiLiisthecorrespondingauthors. relevantcode,theretrievedcodeknowledgewill
23278
Proceedingsofthe2025ConferenceonEmpiricalMethodsinNaturalLanguageProcessing,pages23278–23288
November4-9,2025©2025AssociationforComputationalLinguistics

Sparse Retrieval Code Knowledge 1 edgebasetobenefitfromtheuniqueadvantage
c o n fi g   =   T5Config.from_pretrained() c o n fi g =   AutoModelConfig.from_pretrained() ofeachcode-specificretrievalpath.
| M o d e l   =   |     |     | m o d e l = |     |     |     |     |     |     |     |     |     |     |
| --------------- | --- | --- | ----------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
AutoModelForCausalLM.from_pretrained()
T5ForCausalLM.from_pretrained()
|     |     |     |     |     |     |     | • To alleviate | P3, | CodeRAG |     | adopts | preference- |     |
| --- | --- | --- | --- | --- | --- | --- | -------------- | --- | ------- | --- | ------ | ----------- | --- |
Dense Retrieval Code Knowledge 2 aligned BESTFIT reranking to efficiently find
| #  b ui ld  s e a r ch   e | n g in e |     | defr e t ri e | v e r ( e n g i n e _ | n a m e ) : |     |     |     |     |     |     |     |     |
| -------------------------- | -------- | --- | ------------- | --------------------- | ----------- | --- | --- | --- | --- | --- | --- | --- | --- |
na m e  =  " s o m e   n a m e ” ‘‘ ‘c o n s t r u c t  t h e   re t r ie va l   engine’’’ necessarycodeknowledge. Theretrievedcode
pass
searcher = retriever(name)  knowledgeisrerankedviaLLMrerankeraccord-
Dataflow-guided  Code Knowledge 3 ing to code LLM’s preference. To reduce the
Retrieval
classModelProvider:
model = ModelProvider(args) def__init__(self): reranking overhead, we further distill the pref-
| model.select_model(some_args) |     |     | defselect_model(self): |     |     |     |     |     |     |     |     |     |     |
| ----------------------------- | --- | --- | ---------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
erenceofLLMrerankerintoasmallerreranker
| Figure 1: | Examples | of different |     | code | retrieval | paths, |     |     |     |     |     |     |     |
| --------- | -------- | ------------ | --- | ---- | --------- | ------ | --- | --- | --- | --- | --- | --- | --- |
anduseittoconductreranking.
wherethegraytextindicatesthecodetobegenerated.
|     |     |     |     |     |     |     | • CodeRAG | feeds | the reranked |     | code | knowledge |     |
| --- | --- | --- | --- | --- | --- | --- | --------- | ----- | ------------ | --- | ---- | --------- | --- |
misleadcodeLLMtogenerateinaccuratecode. intocodeLLMforrepository-levelcodecomple-
tion. ExperimentsonbenchmarksReccEvaland
| • P2: Single-pathCodeRetrieval. |       |      |     |            | Existingmeth- |       |        |      |              |     |               |     |     |
| ------------------------------- | ----- | ---- | --- | ---------- | ------------- | ----- | ------ | ---- | ------------ | --- | ------------- | --- | --- |
|                                 |       |      |     |            |               |       | CCEval | show | that CodeRAG |     | significantly |     | and |
| ods either                      | model | code | as  | plain text | and           | chuck |        |      |              |     |               |     |     |
consistentlyexceedsstate-of-the-artmethods.
| code to      | construct | the       | knowledge |     | base       | for later |                    |     |     |     |     |     |     |
| ------------ | --------- | --------- | --------- | --- | ---------- | --------- | ------------------ | --- | --- | --- | --- | --- | --- |
| sparse/dense |           | retrieval | (Zhang    | et  | al., 2023; | Wu        |                    |     |     |     |     |     |     |
|              |           |           |           |     |            |           | 2 OurMethodCodeRAG |     |     |     |     |     |     |
etal.,2024),orconstructspecificdatastructures
(e.g.,dataflowgraph)representingcodeforlater AsdepictedinFig.2,CodeRAGinvolvesfiveparts:
|           |      |         |       |       |         |        | code knowledge |     | base construction |     | (Sec. | 2.1), | re- |
| --------- | ---- | ------- | ----- | ----- | ------- | ------ | -------------- | --- | ----------------- | --- | ----- | ----- | --- |
| retrieval | (Liu | et al., | 2024; | Cheng | et al., | 2024). |                |     |                   |     |       |       |     |
Whileeachmethodhasitsuniqueadvantageand trieval query construction (Sec. 2.2), multi-path
mayapplytosomecodecompletioncases,nei- code retrieval (Sec. 2.2.1), preference-aligned
|         |      |            |     |            |     |       | BESTFIT | code reranking |     | (Sec. | 2.3) and | retrieval- |     |
| ------- | ---- | ---------- | --- | ---------- | --- | ----- | ------- | -------------- | --- | ----- | -------- | ---------- | --- |
| ther of | them | can handle | all | completion |     | cases |         |                |     |       |          |            |     |
well. For instance, Fig. 1 depicts three code augmentedrepository-levelcodecompletion.
completionexamplesandeachfitsoneretrieval
|         |                                    |     |     |     |     |     | 2.1 CodeKnowledgeBaseConstruction |     |     |     |     |     |     |
| ------- | ---------------------------------- | --- | --- | --- | --- | --- | --------------------------------- | --- | --- | --- | --- | --- | --- |
| method. | Sparseretrievalisidealwhenthequery |     |     |     |     |     |                                   |     |     |     |     |     |     |
Constructingcodeknowledgebaseinvolvespars-
| andcodeknowledgedirectlyoverlap. |     |     |     |     | Densere- |     |     |     |     |     |     |     |     |
| -------------------------------- | --- | --- | --- | --- | -------- | --- | --- | --- | --- | --- | --- | --- | --- |
trievalismoreappropriatewhenthequeryand ingandprocessingthecodeintherepository,trans-
codeknowledgearesemanticallyrelated. Incon- formingcodeintostructuredknowledgetoenable
moreefficientretrieval,understanding,andreuse.
| trast, dataflow-guided |     |     | retrieval | facilitates |     | addi- |     |     |     |     |     |     |     |
| ---------------------- | --- | --- | --------- | ----------- | --- | ----- | --- | --- | --- | --- | --- | --- | --- |
tionalsearchesbasedonvariableinstantiation. To construct the knowledge base for retrieval,
|                    |         |             |         |                 |           |        | general RAG    | methods | typically  |         | segment | the            | text   |
| ------------------ | ------- | ----------- | ------- | --------------- | --------- | ------ | -------------- | ------- | ---------- | ------- | ------- | -------------- | ------ |
| • P3: Misalignment |         |             | between | Code            | Retriever |        |                |         |            |         |         |                |        |
|                    |         |             |         |                 |           |        | corpus based   | on      | predefined | rules,  | such    | as             | split- |
| and Code           | LLM.    | Similar     |         | to other        | RAG       | appli- |                |         |            |         |         |                |        |
|                    |         |             |         |                 |           |        | ting by length | or      | delimiters | (Sarthi |         | et al., 2024). |        |
| cations            | (Jin et | al., 2024), |         | inconsistencies |           | may    |                |         |            |         |         |                |        |
However,applyingtheseapproachestocodedata
existbetweenretrievedcodeknowledgeandnec-
|     |     |     |     |     |     |     | compromises | the | structural | integrity |     | and leads | to  |
| --- | --- | --- | --- | --- | --- | --- | ----------- | --- | ---------- | --------- | --- | --------- | --- |
essaryknowledgeforcodeLLM,duetothesep-
|     |     |     |     |     |     |     | thelossofpertinentinformation. |     |     |     | Forinstance,di- |     |     |
| --- | --- | --- | --- | --- | --- | --- | ------------------------------ | --- | --- | --- | --------------- | --- | --- |
aratetrainingprocessandlearningobjectiveof
|                |     |          |      |       |      |       | viding a | class arbitrarily |     | may | result | in omitting |     |
| -------------- | --- | -------- | ---- | ----- | ---- | ----- | -------- | ----------------- | --- | --- | ------ | ----------- | --- |
| code retriever |     | and code | LLM. | While | this | issue |          |                   |     |     |        |             |     |
essentialclass-relateddetails.
| has recently |     | been studied |     | in various | works | on  |              |     |       |          |     |         |     |
| ------------ | --- | ------------ | --- | ---------- | ----- | --- | ------------ | --- | ----- | -------- | --- | ------- | --- |
|              |     |              |     |            |       |     | To alleviate | the | above | problem, | we  | propose | a   |
RAGforquestionanswering(Zhangetal.,2024;
segmentationstrategytailoredtotheconstruction
| Dong et | al., 2024), | it  | is still | underexplored |     | for |                      |     |     |                         |     |     |     |
| ------- | ----------- | --- | -------- | ------------- | --- | --- | -------------------- | --- | --- | ----------------------- | --- | --- | --- |
|         |             |     |          |               |     |     | ofcodeknowledgebase. |     |     | Specifically,weconsider |     |     |     |
repository-levelcodecompletion.
fourelementsinconstructingthecodeknowledge
Toaddresstheseissues,weproposeanewframe-
|     |     |     |     |     |     |     | base: functions, |     | global | variables, | class | variables, |     |
| --- | --- | --- | --- | --- | --- | --- | ---------------- | --- | ------ | ---------- | ----- | ---------- | --- |
workCodeRAGforfindingrelevantandnecessary
|     |     |     |     |     |     |     | and class | functions, | as  | depicted | in Fig. | 3.  | For a |
| --- | --- | --- | --- | --- | --- | --- | --------- | ---------- | --- | -------- | ------- | --- | ----- |
knowledgeinretrieval-augmentedrepository-level
targetcoderepository,wefirstextracttheAbstract
| codecompletion. |     | Ourcontributionsare: |     |          |      |          |                                        |       |         |      |       |       |      |
| --------------- | --- | -------------------- | --- | -------- | ---- | -------- | -------------------------------------- | ----- | ------- | ---- | ----- | ----- | ---- |
|                 |     |                      |     |          |      |          | Syntax Tree                            | (AST) | of each | code | file. | Then, | we   |
| • To overcome   |     | P1, instead          |     | of using | last | k lines, |                                        |       |         |      |       |       |      |
|                 |     |                      |     |          |      |          | extractthefourtypesofelementsfromASTs. |       |         |      |       |       | This |
CodeRAGadoptslogprobabilityguidedprobing
|     |     |     |     |     |     |     | way, the | code repository |     | can be | transformed |     | into |
| --- | --- | --- | --- | --- | --- | --- | -------- | --------------- | --- | ------ | ----------- | --- | ---- |
toconstructretrievalqueryforcoderetrieval.
|     |     |     |     |     |     |     | a structured | knowledge |     | base, | including | function |     |
| --- | --- | --- | --- | --- | --- | --- | ------------ | --------- | --- | ----- | --------- | -------- | --- |
• To address P2, CodeRAG employs multi-path callsandvariableusage,providingdatasupportfor
coderetrievalovertheconstructedcodeknowl- repository-levelcodecompletion.
23279

2 Retrieval Query Construction via Log  3 Multi-path Code Retrieval
Probability Guided Probing
|     |                   |     |     |     | Code Retrieval |     | Sparse    |     | Dense     |     | Dataflow   |
| --- | ----------------- | --- | --- | --- | -------------- | --- | --------- | --- | --------- | --- | ---------- |
|     |                   |     |     |     | Query r        |     | Retrieval |     | Retrieval |     | Guided     |
|     | Current Code File |     |     |     |                |     |           |     |           |     | Retrieval  |
|     |                   |     |     |     |                |     | 1 0       | 1   |           |     | var.unlink |
Code Chunk 1
|     |     |     |     | …   |     |     | 1 1 | 0   |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
…
|     | Code Chunk 2 |     |     |     |     |     | 0 0 | 1   | Encoder |     | var = func() |
| --- | ------------ | --- | --- | --- | --- | --- | --- | --- | ------- | --- | ------------ |
…
|     |              |     |     |     | s2 0.4 0.2     | 0.3 |              |     |           |     |             |
| --- | ------------ | --- | --- | --- | -------------- | --- | ------------ | --- | --------- | --- | ----------- |
|     | Target Chunk |     |     |     |                |     | K ey w o rd  |     | Sim Score |     |             |
|     |              |     |     |     | s0 .40.20.30.1 | 0.1 | m a tr ix    |     |           |     | def func(): |
|     |              |     |     |     | 1              |     |              |     |           |     | pass        |
Code LLM
|     |     |     |     |     |     |             | Code … |     | Code        |     |     |
| --- | --- | --- | --- | --- | --- | ----------- | ------ | --- | ----------- | --- | --- |
|     |     |     |     |     |     | Knowledge 1 |        |     | Knowledge n |     |     |
BestFit
Distilled
|     |     |     |     |     |     | Prompting | LLM |     | Reranker | 5 Retrieval-Augmented |     |
| --- | --- | --- | --- | --- | --- | --------- | --- | --- | -------- | --------------------- | --- |
Reranker
Code Completion
|     | Code Files |     | ASTs |     | Code |     |     |     |     |     |     |
| --- | ---------- | --- | ---- | --- | ---- | --- | --- | --- | --- | --- | --- |
rerank
|     | in the |     |     | Knowledge Base |     |     |     |     |     |     |     |
| --- | ------ | --- | --- | -------------- | --- | --- | --- | --- | --- | --- | --- |
Repository
|     |     |     |     |     |     |             | Code … |     | Code        |     |     |
| --- | --- | --- | --- | --- | --- | ----------- | ------ | --- | ----------- | --- | --- |
|     |     |     |     |     |     | Knowledge 4 |        |     | Knowledge 2 |     |     |
Code LLM
1 Code Knowledge Base Construction
4 Preference-Aligned BestFitReranking
|     |     |             |     |           | Figure2:  | OverviewofCodeRAG. |                                              |     |     |     |        |
| --- | --- | ----------- | --- | --------- | --------- | ------------------ | -------------------------------------------- | --- | --- | --- | ------ |
|     |     | Element     |     | Knowledge |           |                    | Algorithm1:ConstructRetrievalQuery           |     |     |     |        |
|     |     |             |     | def fu n  | c(*args): |                    | Input:C(codefiletobCeodceo Bmlopckl e1ted),f |     |     |     | (chunk |
|     |     | 1 Functions |     | p as      | s         |                    |                                              |     |     |     |        |
length),m(numCbodeer Bolofcgk e2nerationstep),g
(numberofselectedchunks)
Code Block 3
|     |     |     |     | VAR_CONST= “test” |     |     | Output:r(coderetrievalquery) |     |     |     |     |
| --- | --- | --- | --- | ----------------- | --- | --- | ---------------------------- | --- | --- | --- | --- |
2 Variables
FunctionQueryConstruction(C,f,m,g):
DivideCintofine-grUaninfineidshcedhunksandeachchunk
classmyClass:
|     |     | 3 ClsFuncs |     |     |     |     |     | havingf | lines. |     |     |
| --- | --- | ---------- | --- | --- | --- | --- | --- | ------- | ------ | --- | --- |
deffunc(self)
|     |     |           |     |               |     |     | foreachchunkc |                          | ido                |     |     |
| --- | --- | --------- | --- | ------------- | --- | --- | ------------- | ------------------------ | ------------------ | --- | --- |
|     |     |           |     |               |     |     |               | ifc isthetargetchunkthen |                    |     |     |
|     |     | 4 ClsVars |     | classmyClass: |     |     |               | i                        |                    |     |     |
|     |     |           |     | self.name=“”  |     |     |               | Pass.                    |                    |     |     |
|     |     |           |     |               |     |     |               | Concatenatec             | itothetargetchunk. |     |     |
Figure3: ExamplesofCodeKnowledgeBaseItems. FeedtheconcatenationintocodeLLMto
generatemnewtokens.
Recordthehighestlogprobabilityforalltokens
2.2 RetrievalQueryConstructionviaLog
inthevocabularyateachgenerationstep.
ProbabilityGuidedProbing Summprobabilityscoresastheconfidence
|     |     |     |     |     |     |     |     | scores | i.  |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ------ | --- | --- | --- |
In standard RAG, a retrieval query conveys the Selectthetop-gchunkswiththehighest
confidencescoress.
| user | intent | from | the user | query | or consists | of a |     |     |     |     |     |
| ---- | ------ | ---- | -------- | ----- | ----------- | ---- | --- | --- | --- | --- | --- |
Concatenatethegchunkswiththetargetchunkas
specific text chunk from a document. Using the theretrievalqueryr.
| retrieval             | query,    | the | RAG  | framework                  | can       | retrieve | returnr. |     |     |     |     |
| --------------------- | --------- | --- | ---- | -------------------------- | --------- | -------- | -------- | --- | --- | --- | --- |
| relevant              | knowledge |     | from | the                        | knowledge | base to  |          |     |     |     |     |
| assisttextgeneration. |           |     |      | Inexistingrepository-level |           |          |          |     |     |     |     |
codecompletionmethods,theconceptofretrieval logprobabilitytofindthefine-grainedcodechunks
query shifts to represent an incomplete code seg- that are most important to constructing code re-
ment (Zhang et al., 2023), which could be an un- trievalquery. Inrepository-levelcodecompletion,
finishedfunction,apartiallydefinedvariable,ora we can view log probability as the confidence of
methodcallwithinaclass(i.e.,codecontext). code LLMs, given the code retrieval query. In
To overcome the limitation of using the last k other words, log probability can reveal the rele-
linesasthecoderetrievalquery(i.e.,P1illustrated vanceofthecodechunksintheretrievalquery.
in Sec. 1), we propose to construct the code re- As shown in Alg. 1, we first chunk the code
trieval query based on the log probability gain. file that the programmer is working on into fine-
Alg. 1 depicts the overall procedure for code re- grainedpiecesandeachofthemcontainsf lines.
trievalqueryconstruction. Thecoreideaistouse Then,weconcatenateeachfine-grainedchunkto
23280

the chunk containing unfinished code (the target representations. Thequeryisencodedatthechunk
chunk) as the probe and feed it to code LLM to level,whereastheitemsintheknowledgebaseare
generate m tokens. For simplicity, we choose either at the function level (functions) or the line
the token with the maximum log probability at level (variables). Code knowledge that has high
eachstepanduseCodeT5p-220m1
|     |     |     |     | ascodeLLM |     | similaritywiththeretrievalqueryw.r.t. |     |     |     |     |     | theirrep- |
| --- | --- | --- | --- | --------- | --- | ------------------------------------- | --- | --- | --- | --- | --- | --------- |
forthisstep. Thesumofthelogprobabilitiesfor resentationsisretrieved. Weusecosinesimilarity
all generated token is recorded as the relevance asthesimilaritymeasureandadoptthepre-trained
scoreforthefine-grainedchunkcorrespondingto encoderinCodeT5p-220mastheencodingmodel.
| the probe. | Finally, | the | top-g | fine-grained | chunks |                           |     |     |     |                    |     |     |
| ---------- | -------- | --- | ----- | ------------ | ------ | ------------------------- | --- | --- | --- | ------------------ | --- | --- |
|            |          |     |       |              |        | Dataflow-GuidedRetrieval. |     |     |     | Itfindsrelevantin- |     |     |
withthehighestrelevancescoresareconcatenated
|     |     |     |     |     |     | formationw.r.t. |     | thetargetchunkinthecurrentcode |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --------------- | --- | ------------------------------ | --- | --- | --- | --- |
togetherwiththetargetchunkastheretrievalquery. file according to data dependency relations. Fol-
lowingChengetal.(2024),wefirstformulatethe
2.2.1 Multi-pathCodeRetrieval
|     |     |     |     |     |     | unfinished | code | file | into | a dataflow | graph. | Once |
| --- | --- | --- | --- | --- | --- | ---------- | ---- | ---- | ---- | ---------- | ------ | ---- |
AsanessentialpartofRAG,coderetrieverfindsrel-
thegraphisbuilt,wecanretrievethedependency
evantcodeknowledgefromcodeknowledgebase startingfromthelastunfinishedlineinthedataflow
accordingtothecoderetrievalquery. Earlycode graphastheretrievedcodeknowledge.
| retrieval | methods | rely | on traditional | information |     |            |     |           |            |     |        |          |
| --------- | ------- | ---- | -------------- | ----------- | --- | ---------- | --- | --------- | ---------- | --- | ------ | -------- |
|           |         |      |                |             |     | For sparse |     | and dense | retrieval, |     | we use | the con- |
retrievalmethodslikeTF-IDFandBM25(sparsere-
|     |     |     |     |     |     | structed | retrieval | query | to  | retrieve | j results | from |
| --- | --- | --- | --- | --- | --- | -------- | --------- | ----- | --- | -------- | --------- | ---- |
trieval),andrecentcoderetrievalapproachescom-
|                            |       |           |          |                    |         | eachpath.       | Ifdatadependencyexistsinthedataflow |            |                    |       |           |          |
| -------------------------- | ----- | --------- | -------- | ------------------ | ------- | --------------- | ----------------------------------- | ---------- | ------------------ | ----- | --------- | -------- |
| monly                      | adopt | embedding | based    | methods            | (Dense  |                 |                                     |            |                    |       |           |          |
|                            |       |           |          |                    |         | graph,          | we retrieve                         |            | dependency-related |       |           | code via |
| Retrieval)(Sunetal.,2024). |       |           |          | Mostrecently,Cheng |         |                 |                                     |            |                    |       |           |          |
|                            |       |           |          |                    |         | dataflow-guided |                                     | retrieval. |                    | After | receiving | all re-  |
| et al. (2024)              | find  | that      | dataflow | can also           | be used |                 |                                     |            |                    |       |           |          |
trievedresultsfromthreepaths,weaddthemtoa
toguidecoderetrieval(dataflow-guidedretrieval).
|     |     |     |     |     |     | retrievallistcontainingn(i.e.,2j |     |     |     |     | +1)results. |     |
| --- | --- | --- | --- | --- | --- | -------------------------------- | --- | --- | --- | --- | ----------- | --- |
Thesemethodsconsidercoderetrievalfromasin-
gleperspectiveandretrieveword-matchingknowl- 2.3 FindNecessaryCodeKnowledgethrough
edge,semanticallyrelevantknowledge,orknowl- Preference-Aligned BESTFITReranking
edgehavingdatadependencyrelationswiththetar-
Theretrievedcodeknowledgeisusedtoaugment
| getchunk. | Eachofthemhasitsuniqueadvantages |     |     |     |     |     |     |     |     |     |     |     |
| --------- | -------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
thecodecompletionprompt,directlyaffectingthe
andcanwellprovideretrievedcodeknowledgefor
|     |     |     |     |     |     | qualityofcodecompletion. |     |     |     | Solelyusingthemulti- |     |     |
| --- | --- | --- | --- | --- | --- | ------------------------ | --- | --- | --- | -------------------- | --- | --- |
somecodecompletioncases. Hence,wearguethat pathcoderetrievermaynotprovideanappropriate
conductingamulti-pathcoderetrievalcanbetterof-
|                                         |     |     |     |     |     | order of | relevant | knowledge. |     | The | reason | is the |
| --------------------------------------- | --- | --- | --- | --- | --- | -------- | -------- | ---------- | --- | --- | ------ | ------ |
| fercodeknowledgeforlatercodecompletion. |     |     |     |     | Our |          |          |            |     |     |        |        |
misalignmentbetweenthecoderetrieverandcode
designedmulti-pathcoderetrievalstepinvolvesthe LLM,whichiscausedbytheirseparatetrainingob-
followingthreecoderetrievalpaths:
|     |     |     |     |     |     | jectives(Zhangetal.,2024). |     |     |     | Therefore,wefurther |     |     |
| --- | --- | --- | --- | --- | --- | -------------------------- | --- | --- | --- | ------------------- | --- | --- |
Sparse Retrieval. Sparse retrieval relies on key- deploy a reranking module that reranks retrieved
word matching between the retrieval query and codeknowledgeaccordingtocodeLLM’sprefer-
codeknowledgeinthecodeknowledgebase,which enceandonlykeeptop-ucodeknowledge(u < n).
identifiesexactorcloselyrelatedkeywordswithin
2.3.1 BESTFITCodeReranking
thecodebase,toobtainrelevantinvocationdetails,
|     |     |     |     |     |     | To address | the | misalignment, |     | a   | natural | way is to |
| --- | --- | --- | --- | --- | --- | ---------- | --- | ------------- | --- | --- | ------- | --------- |
APIcalls,andcodesnippetsthatsharesimilarstruc-
trainthererankerusingfeedbacksignalsfromcode
| turesorfunctionality. |     |     | Sparseretrievalisefficient |     |     |               |     |     |                  |     |      |         |
| --------------------- | --- | --- | -------------------------- | --- | --- | ------------- | --- | --- | ---------------- | --- | ---- | ------- |
|                       |     |     |                            |     |     | LLM. However, |     | in  | repository-level |     | code | comple- |
andparticularlyeffectivewhensearchingsyntacti-
|     |     |     |     |     |     | tion, it | is very | difficult | to  | acquire | feedback | from |
| --- | --- | --- | --- | --- | --- | -------- | ------- | --------- | --- | ------- | -------- | ---- |
callysimilarcodeorcommonlyusedfunctions,as
|     |     |     |     |     |     | code LLM | that | can | perfectly | show | the | quality of |
| --- | --- | --- | --- | --- | --- | -------- | ---- | --- | --------- | ---- | --- | ---------- |
itcanquicklypinpointsegmentsthatcontainspe-
|             |     |              |     |            |         | the generated |     | code. | One | possible | solution | is ap- |
| ----------- | --- | ------------ | --- | ---------- | ------- | ------------- | --- | ----- | --- | -------- | -------- | ------ |
| cific terms | or  | identifiers. | We  | use TF-IDF | (Jones, |               |     |       |     |          |          |        |
plyingunittestsonthegeneratedcodefromcode
2004)forsparseretrieval.
|                 |       |                              |     |           |           | LLM(Maetal.,2025). |        |                  | Whileconductingunittests |      |             |           |
| --------------- | ----- | ---------------------------- | --- | --------- | --------- | ------------------ | ------ | ---------------- | ------------------------ | ---- | ----------- | --------- |
| DenseRetrieval. |       | Denseretrievalleveragesanen- |     |           |           |                    |        |                  |                          |      |             |           |
|                 |       |                              |     |           |           | is possible        | for    | function-level   |                          | code | completion, | it        |
| coding          | model | to encode                    | the | retrieval | query and |                    |        |                  |                          |      |             |           |
|                 |       |                              |     |           |           | is costly          | in the | repository-level |                          |      | setting     | where the |
codeknowledgeinthecodeknowledgebaseinto
completeprojectmustbeexecutedinordertosee
|     |     |     |     |     |     | the impact | of  | inserting | generated |     | code. | Besides, |
| --- | --- | --- | --- | --- | --- | ---------- | --- | --------- | --------- | --- | ----- | -------- |
1https://huggingface.co/Salesforce/
| codet5p-220m |     |     |     |     |     | unlikefunction-levelcodecompletionwhereinputs |     |     |     |     |     |     |
| ------------ | --- | --- | --- | --- | --- | --------------------------------------------- | --- | --- | --- | --- | --- | --- |
23281

|     |     |     |     |     |     |     | Retrieved |     |     | LLM |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --------- | --- | --- | --- | --- | --- | --- |
Which of the retrieved code snippets is most Listwise Prompting Results
|     |     |     |     |     |     |     | Code |     |     | Reranker |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ---- | --- | --- | -------- | --- | --- | --- |
helpfulforcompletingthefollowingcodesnippet?
|     |     |     |     |     |     |     |     | … rank code knowledge |     |     |     | [Index 1]…[Index u] |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --------------------- | --- | --- | --- | ------------------- | --- |
…
Thecodesnippettobecompleted:
|         |     |     |     |     |     |     |     | …   w h ic h     | c o d e  k n owledge |     |     | [Index x] |     |
| ------- | --- | --- | --- | --- | --- | --- | --- | ---------------- | -------------------- | --- | --- | --------- | --- |
| {query} |     |     |     |     |     |     |     | is  m o s t  r e | l e va n t  …        |     |     |           |     |
BestFitPrompting
Theretrievedcodesnippet(s):
Figure5:Acomparisonbetweenlistwisecodereranking
{codesnippets}
andBESTFITcodereranking.
Pleaseprovideonlythelabelofthemosthelpful
| retrieved       | code    | snippet, |             | enclosed | in          | square |     |     |     |     |     |     |     |
| --------------- | ------- | -------- | ----------- | -------- | ----------- | ------ | --- | --- | --- | --- | --- | --- | --- |
| brackets,within |         | the      | answertags. |          | Forexample, | if     |     |     |     |     |     |     |     |
| the code        | snippet |          | C is the    | most     | helpful,    | the    |     |     |     |     |     |     |     |
answershouldbe:<answer>[C]</answer>
| Figure4:    | PromptforLLM-basedBESTFITreranking. |      |          |      |            |        |     |     |     |     |     |     |     |
| ----------- | ----------------------------------- | ---- | -------- | ---- | ---------- | ------ | --- | --- | --- | --- | --- | --- | --- |
| and outputs | to                                  | unit | test are | easy | to design, | craft- |     |     |     |     |     |     |     |
inginputsandlabelingoutputstounittestsinthe Figure6: Heapsortoperationfinallymovestop-ucode
|     |     |     |     |     |     |     | knowledge | pieces | to the | top. Each | circle | denotes | a   |
| --- | --- | --- | --- | --- | --- | --- | --------- | ------ | ------ | --------- | ------ | ------- | --- |
repository-levelsettingismuchharder(e.g.,more
executionparametersoroutputsarenotvariables). windowof3codeknowledgepieces.
Consideringtheabovedifficulty,analternative
ToavoidexceedingLLM’sinputlength,weim-
| is to apply | an  | LLM | as a zero-shot |     | reranker | (Sun |     |     |     |     |     |     |     |
| ----------- | --- | --- | -------------- | --- | -------- | ---- | --- | --- | --- | --- | --- | --- | --- |
plementaslidingwindowstrategythatdividesthe
| et al., 2023). |     | And | the LLM | is  | instructed | to di- |     |     |     |     |     |     |     |
| -------------- | --- | --- | ------- | --- | ---------- | ------ | --- | --- | --- | --- | --- | --- | --- |
retrievallistintoseveralequal-sizedwindows,and
| rectly produce |     | the | reranking | list | of the | retrieval |              |     |         |       |     |      |        |
| -------------- | --- | --- | --------- | ---- | ------ | --------- | ------------ | --- | ------- | ----- | --- | ---- | ------ |
|                |     |     |           |      |        |           | the adjacent | two | windows | share | one | code | knowl- |
codeknowledgepiecesaccordingtotheirrelevance
|               |     |          |        |         |      |         | edge. Fig.6 | providesan                    |     | example | withawindow |     |     |
| ------------- | --- | -------- | ------ | ------- | ---- | ------- | ----------- | ----------------------------- | --- | ------- | ----------- | --- | --- |
| to the query. |     | Although | recent | studies | (Sun | et al., |             |                               |     |         |             |     |     |
|               |     |          |        |         |      |         | sizeof3.    | Eachtime,wefeedonewindowtoLLM |     |         |             |     |     |
2023;Pradeepetal.,2023)haveshownthestrong
|     |     |     |     |     |     |     | reranker | and ask | it to | pick only | the | most helpful |     |
| --- | --- | --- | --- | --- | --- | --- | -------- | ------- | ----- | --------- | --- | ------------ | --- |
abilityofLLMsonzero-shotdocumentreranking,
|     |     |     |     |     |     |     | codeknowledge. |     | Inspiredbypriorwork(Qinetal., |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | -------------- | --- | ----------------------------- | --- | --- | --- | --- |
weempiricallyfindthatthislistwisepromptingso-
2024;Zhuangetal.,2024)thatusessortingalgo-
lutiondoesnotworkwellonrerankingcodeknowl-
rithmstospeedupLLM-basedpairwisereranking,
edge: (1)LLMswithafewbillionparametersthat
|     |     |     |     |     |     |     | we apply | heap | sort to | accelerate | BESTFIT |     | code |
| --- | --- | --- | --- | --- | --- | --- | -------- | ---- | ------- | ---------- | ------- | --- | ---- |
canbedeployedlocallymoreeasilydonotstrictly
|     |     |     |     |     |     |     | reranking. | Windowsareorganizedasaheaptree |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ---------- | ------------------------------ | --- | --- | --- | --- | --- |
adheretolistwiseprompting,whilecallingAPIsof
|     |     |     |     |     |     |     | and each | time | we use | LLM reranker |     | as the | com- |
| --- | --- | --- | --- | --- | --- | --- | -------- | ---- | ------ | ------------ | --- | ------ | ---- |
onlineLLMsthathavemuchlargermodelsizesand
paratortofindthemostrelevantcodeinawindow.
canunderstandandstrictlyfollowlistwiseprompt-
Heapsortcanquicklyfindthetop-umostrelevant
| ingincurshighoverhead. |     |     |     | (2)Listwiseprompting |     |     |                                  |     |     |     |     |          |     |
| ---------------------- | --- | --- | --- | -------------------- | --- | --- | -------------------------------- | --- | --- | --- | --- | -------- | --- |
|                        |     |     |     |                      |     |     | codeknowledgeinthererankinglist. |     |     |     |     | Wechoose |     |
itselfiscomputationallyintensivesincethererank-
heapsortinsteadofothersortingmethodsdueto
| inglistisgeneratedtokenbytoken.           |     |      |        |            | LLMreranker |         |                               |         |     |      |           |      |     |
| ----------------------------------------- | --- | ---- | ------ | ---------- | ----------- | ------- | ----------------------------- | ------- | --- | ---- | --------- | ---- | --- |
|                                           |     |      |        |            |             |         | itssimplicityandthecomplexity |         |     |      | (NlogN).  |      |     |
| mustdooneinferenceforeachnexttokenpredic- |     |      |        |            |             |         |                               |         |     |      | O         |      |     |
| tionduringrerankinglistgeneration.        |     |      |        |            |             |         | 2.3.2 DistilledReranker       |         |     |      |           |      |     |
| To overcome                               |     | this | issue, | we propose |             | BESTFIT |                               |         |     |      |           |      |     |
|                                           |     |      |        |            |             |         | Even though                   | BESTFIT |     | code | reranking | only | re- |
codererankingthatpromptstheLLMrerankerto
quirestheLLMrerankertohaveafewbillionpa-
| pick the  | most    | relevant | code          | knowledge |        | from the    |                                      |          |           |     |         |          |        |
| --------- | ------- | -------- | ------------- | --------- | ------ | ----------- | ------------------------------------ | -------- | --------- | --- | ------- | -------- | ------ |
|           |         |          |               |           |        |             | rameters,                            | directly | employing |     | the LLM | reranker |        |
| retrieval | list to | the      | query.        | The       | prompt | is listed   |                                      |          |           |     |         |          |        |
|           |         |          |               |           |        |             | maystillincurahighcomputationalcost. |          |           |     |         |          | Hence, |
| in Fig.   | 4. This | way,     | the inference |           | cost   | is signifi- |                                      |          |           |     |         |          |        |
wedistillthepreferenceoftheLLMrerankerinto
| cantly reduced |     | as we | only | need | a single | forward |     |     |     |     |     |     |     |
| -------------- | --- | ----- | ---- | ---- | -------- | ------- | --- | --- | --- | --- | --- | --- | --- |
amuchsmallerrerankermodel.
| passoftheLLMreranker. |     |     |     | Fig.5depictsthediffer- |     |     |     |     |     |     |     |     |     |
| --------------------- | --- | --- | --- | ---------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Totrainthedistilledreranker,wefirstuseadata
encebetweenlistwiseandBESTFITcodereranking.
augmentationstrategy(Alg.2)toconstructdistil-
Moreover,wefindthatanLLMwithafewbillion
|            |     |          |        |         |     |         | lationtrainingdata. |     | Weuseunfinishedcodeinthe |     |     |     |     |
| ---------- | --- | -------- | ------ | ------- | --- | ------- | ------------------- | --- | ------------------------ | --- | --- | --- | --- |
| parameters | can | strictly | follow | BESTFIT |     | prompt- |                     |     |                          |     |     |     |     |
trainingdatatoformulatecoderetrievalqueriesand
| ing. Hence, | we  | directly | use | Qwen3-8B |     | as LLM |     |     |     |     |     |     |     |
| ----------- | --- | -------- | --- | -------- | --- | ------ | --- | --- | --- | --- | --- | --- | --- |
conductmulti-pathcoderetrievaltoproduceinitial
reranker2,avoidingadditionalinstructingtuningof
|     |     |     |     |     |     |     | retrievallists. | Then,weconductdataaugmentation |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --------------- | ------------------------------ | --- | --- | --- | --- | --- |
LLMrerankerorcallingonlineLLMAPIs.
bygeneratingmultiplevariationsofeachinitialre-
2https://huggingface.co/Qwen/Qwen3-8B trievallist ,whereeachvariationcontainsdiffer-
L
23282

Algorithm2:ConstructDistillationData codeLLMtogeneratethecompletion.
Input:r(coderetrievalquery),
L
|     | (initialretrievallistforr), |     |     |     | (sample |     | 3 Experiment |     |     |     |     |     |     |
| --- | --------------------------- | --- | --- | --- | ------- | --- | ------------ | --- | --- | --- | --- | --- | --- |
N
numbers)
leforr)
O u tp u t: (d i s ti ll a ti o n t r a in i n g s am p 3.1 EvaluationSettings
|     |           | SDa t a C o | n s t r u c t | i o n ( r | )   |     |          |                                      |     |     |     |     |     |
| --- | --------- | ----------- | ------------- | --------- | --- | --- | -------- | ------------------------------------ | --- | --- | --- | --- | --- |
| F u | n ct io n |             |               | ,         | :   |     |          |                                      |     |     |     |     |     |
|     | foriin    |             |               | L         |     |     |          |                                      |     |     |     |     |     |
|     |           | do          |               |           |     |     | Metrics. | Weuseprevalentmetrics(Liuetal.,2024; |     |     |     |     |     |
|     | forj      | N =1to3do   |               |           |     |     |          |                                      |     |     |     |     |     |
Zhangetal.,2023)forevaluation:
|     |     | Randomlypickicodeknowledgefrom |     |     |     | as  |     |     |     |     |     |     |     |
| --- | --- | ------------------------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
theretrievedcodesnippet(s){code L • CodeMatch. ExactMatch(EM)andEditSim-
snippets}inFig.4.
|     |     |     |     |     |     |     | ilarity(ES)4 | areemployedtoassesscodealign- |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ------------ | ----------------------------- | --- | --- | --- | --- | --- |
[ ]
|     |     | C for ← z=1to5do |     |     |     |     | ment. | EMis1whenthegeneratedcodeisidenti- |     |     |     |     |     |
| --- | --- | ---------------- | --- | --- | --- | --- | ----- | ---------------------------------- | --- | --- | --- | --- | --- |
UseBESTFITrerankingpromptinFig.4 caltotheground-truthanswer,and0otherwise.
toguideLLMrerankertoselect[C]
|     |     |     |     |     |     |     | ES provides | a   | more nuanced |     | evaluation, |     | calcu- |
| --- | --- | --- | --- | --- | --- | --- | ----------- | --- | ------------ | --- | ----------- | --- | ------ |
from{codesnippets}.
|     |     | Add[C]to | .   |     |     |     | lated | as ES = | 1 Lev(x,y)/max( |     |     | x   | , y ), |
| --- | --- | -------- | --- | --- | --- | --- | ----- | ------- | --------------- | --- | --- | --- | ------ |
|     |     |          | C   |     |     |     |       |         | −               |     |     | ∥ ∥ | ∥ ∥    |
ifOnecodeknowledge[C]occursatleast
|     |     |             |     |     |     |     | whereLev( | )denotestheLevenshteindistance. |     |     |     |     |     |
| --- | --- | ----------- | --- | --- | --- | --- | --------- | ------------------------------- | --- | --- | --- | --- | --- |
|     |     | fourtimesin |     |     |     |     |           | ·                               |     |     |     |     |     |
then
Add r, codesnippets C ,[C] to . • IdentifierMatch. WeutilizeEMandF1scores
|     |        |     | { { |     | } } | S   |                                        |     |           |         |                |     |        |
| --- | ------ | --- | --- | --- | --- | --- | -------------------------------------- | --- | --------- | ------- | -------------- | --- | ------ |
|     |        |     |     |     |     |     | to evaluate                            | the | alignment | of      | identifiers    |     | in the |
|     | return | .   |     |     |     |     |                                        |     |           |         |                |     |        |
|     |        | S   |     |     |     |     | generatedcodeandtheground-truthanswer. |     |           |         |                |     |        |
|     |        |     |     |     |     |     | Baselines.                             | We  | use       | several | representative |     |        |
ingamountsofcodeknowledge. Afterthat,weuse repository-levelcodecompletionbaselines: Zero-
LLMrerankerwith BESTFIT promptingtoselect Shot,CCFinder(Dingetal.,2024),RG-1(Zhang
themosthelpfulcodeknowledgefromeachgener- et al., 2023), RepoCoder (Zhang et al., 2023),
atedvariation,repeatingthisprocessfivetimesto
DraCo(Chengetal.,2024),RepoFuse(Liangetal.,
assessselectionconsistency. WhenLLMreranker 2024),andRepoformer-3B(Wuetal.,2024).
demonstrateshighconfidenceinitsselections(i.e.,
|     |     |     |     |     |     |     | Code LLMs. |     | We use | four representative |     |     | code |
| --- | --- | --- | --- | --- | --- | --- | ---------- | --- | ------ | ------------------- | --- | --- | ---- |
whenconsistentchoicesappearinatleastfourout
|     |     |     |     |     |     |     | LLMs with | different | parameter |     | numbers | as  | code |
| --- | --- | --- | --- | --- | --- | --- | --------- | --------- | --------- | --- | ------- | --- | ---- |
offivetrials),thegeneratedlist,togetherwiththe
|     |     |     |     |     |     |     | generators: | CodeGen-350M5 |     |     | (Nijkamp |     | et al., |
| --- | --- | --- | --- | --- | --- | --- | ----------- | ------------- | --- | --- | -------- | --- | ------- |
correspondingcoderetrievalqueryandconsensus
|            |            |            |                           |              |          |      | 2023),         | SantaCoder-1.1B6 |          | (Allal | et   | al.,   | 2023), |
| ---------- | ---------- | ---------- | ------------------------- | ------------ | -------- | ---- | -------------- | ---------------- | -------- | ------ | ---- | ------ | ------ |
| selection, |            | is treated | as a                      | distillation | training | sam- |                |                  |          |        |      |        |        |
|            |            |            |                           |              |          |      | StarCoder2-3B7 |                  | (Lozhkov | et     | al., | 2024), | and    |
| ple        | . Thisway, |            | reflectsLLMreranker’smost |              |          |      |                |                  |          |        |      |        |        |
Qwen2.5-Coder-7B8
| S                         |     |     | S   |                        |     |     |     |     | (Huietal.,2024). |     |     |     |     |
| ------------------------- | --- | --- | --- | ---------------------- | --- | --- | --- | --- | ---------------- | --- | --- | --- | --- |
| reliabledecisionpatterns. |     |     |     | Weuseallcurateddistil- |     |     |     |     |                  |     |     |     |     |
lationsamplestofine-tuneQwen3-0.6B3,theback- Datasets. We use benchmarks ReccEval (Cheng
bone of the distilled reranker, using LoRA (Hu etal.,2024)andCCEval(Dingetal.,2023).
etal.,2022)andtoken-levelcross-entropyloss.
|            |     |             |           |        |          |           | EnvironmentandHyper-Parameters. |          |          |         |     | Weusea |      |
| ---------- | --- | ----------- | --------- | ------ | -------- | --------- | ------------------------------- | -------- | -------- | ------- | --- | ------ | ---- |
| Finally,   |     | the trained | distilled |        | reranker | is used   |                                 |          |          |         |     |        |      |
|            |     |             |           |        |          |           | machine                         | with two | Intel(R) | Xeon(R) |     | Silver | 4314 |
| in CodeRAG |     | to          | actually  | rerank | the      | retrieved |                                 |          |          |         |     |        |      |
CPU@2.40GHzandoneNVIDIAA800GPUfor
codeknowledgeandCodeRAGretainstop-ucode
|                               |     |     |     |     |       |     | experiments. | Themaximumnumberofgeneration |               |             |             |        |      |
| ----------------------------- | --- | --- | --- | --- | ----- | --- | ------------ | ---------------------------- | ------------- | ----------- | ----------- | ------ | ---- |
| knowledgeinthererankinglist(u |     |     |     |     | < n). |     |              |                              |               |             |             |        |      |
|                               |     |     |     |     |       |     | tokens is    | set to                       | 48. The       | temperature |             | during | gen- |
|                               |     |     |     |     |       |     | erationis    | setto                        | 0. Themaximum |             | inputlength |        | of   |
2.4 PuttingAllTogether
|         |             |         |            |               |               |           | allcodeLLMsissetto2,048bydefault. |            |            |                    |           | Weuse       |        |
| ------- | ----------- | ------- | ---------- | ------------- | ------------- | --------- | --------------------------------- | ---------- | ---------- | ------------------ | --------- | ----------- | ------ |
| During  | completion, |         | for        | an unfinished | code          | file,     |                                   |            | Inference9 |                    |           |             |        |
|         |             |         |            |               |               |           | the Text                          | Generation |            |                    | framework |             | to ac- |
| CodeRAG |             | firstly | constructs | the           | corresponding |           |                                   |            |            |                    |           |             |        |
|         |             |         |            |               |               |           | celerateLLMinference.             |            |            | Bydefault,weuseLLM |           |             |        |
| code    | retrieval   | query   | r.         | Then CodeRAG  |               | uses r to |                                   |            |            |                    |           |             |        |
|         |             |         |            |               |               |           | rerankerinCodeRAG.                |            |            | Wesetf             | andg      | to3and1     |        |
| conduct | multi-path  |         | code       | retrieval     | over          | the code  |                                   |            |            |                    |           |             |        |
|         |             |         |            |               |               |           | 4Note                             | that the   | paper of   | DraCo              | adopts    | a different | way    |
knowledgebaseandretrievestop-nrelevantcode
|     |     |     |     |     |     |     | to measure | ES (see | https://github.com/nju-websoft/ |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ---------- | ------- | ------------------------------- | --- | --- | --- | --- |
knowledge. After that, CodeRAG leverages the DraCo?tab=readme-ov-file#evaluation). Wefollowthe
BESTFIT reranker to rank the n relevant code definitionofESusedinthepaperofRepoCoder.
5https://huggingface.co/Salesforce/
| knowledge |     | and | retains | the top-u | necessary | code |     |     |     |     |     |     |     |
| --------- | --- | --- | ------- | --------- | --------- | ---- | --- | --- | --- | --- | --- | --- | --- |
codegen-350M-mono
knowledge pieces. Finally, the code context of 6https://huggingface.co/bigcode/santacoder
theunfinishedcodefileisconcatenatedwiththeu
7https://huggingface.co/bigcode/starcoder2-3b
piecesofcodeknowledge,andtheresultisfedinto 8https://huggingface.co/Qwen/Qwen2.5-Coder-7B
9https://huggingface.co/docs/
3https://huggingface.co/Qwen/Qwen3-0.6B text-generation-inference/index
23283

Table1: PerformanceonReccEval(Use100%dataforevaluation). Boldandunderlinedvaluesindicatethebest
andthesecond-bestresults,respectively.
|     |     | CodeGen-350M |     |     | SantaCoder-1.1B |     | StarCoder2-3B |     |     | Qwen2.5-Coder-7B |     |     |
| --- | --- | ------------ | --- | --- | --------------- | --- | ------------- | --- | --- | ---------------- | --- | --- |
CodeMatch IdentifierMatch CodeMatch IdentifierMatch CodeMatch IdentifierMatch CodeMatch IdentifierMatch
Methods
|     |     | EM ES | EM  | F1  | EM ES EM | F1 EM | ES  | EM  | F1  | EM  | ES  | EM F1 |
| --- | --- | ----- | --- | --- | -------- | ----- | --- | --- | --- | --- | --- | ----- |
Zero-Shot 4.04 38.36 9.74 26.06 6.27 42.22 12.89 30.08 7.86 45.04 14.44 33.34 11.48 47.72 18.37 36.43
CCFinder 16.50 47.71 23.34 40.12 19.08 50.99 26.67 43.31 28.12 58.93 36.44 53.42 28.43 58.95 36.76 53.09
RG-1 20.04 50.30 26.53 41.35 24.07 54.72 31.26 46.29 29.35 59.43 36.76 52.27 33.01 61.55 40.15 54.68
RepoCoder 23.96 53.27 31.01 45.87 26.78 56.59 34.31 49.07 34.27 63.09 42.30 57.39 34.99 62.71 42.38 56.20
DraCo 21.85 51.44 29.44 45.92 30.27 59.38 38.97 55.50 36.57 64.31 45.61 61.42 39.99 66.26 48.55 63.41
RepoFuse 21.20 51.18 27.81 43.84 28.73 57.89 36.50 51.74 33.88 61.96 41.43 56.52 38.24 65.11 45.88 60.11
CodeRAGllmr 26.81 55.54 34.02 50.13 36.17 63.00 44.17 59.64 42.69 68.07 51.34 65.73 47.48 70.82 55.47 68.68
Table2: PerformanceonCCEval(Use100%dataforevaluation). Boldandunderlinedvaluesindicatethebestand
thesecond-bestresults,respectively.
|     |     | CodeGen-350M |     |     | SantaCoder-1.1B |     | StarCoder2-3B |     |     | Qwen2.5-Coder-7B |     |     |
| --- | --- | ------------ | --- | --- | --------------- | --- | ------------- | --- | --- | ---------------- | --- | --- |
Methods CodeMatch IdentifierMatch CodeMatch IdentifierMatch CodeMatch IdentifierMatch CodeMatch IdentifierMatch
|     |     | EM ES | EM  | F1  | EM ES EM | F1 EM | ES  | EM  | F1  | EM  | ES  | EM F1 |
| --- | --- | ----- | --- | --- | -------- | ----- | --- | --- | --- | --- | --- | ----- |
Zero-Shot 2.70 43.02 8.26 37.85 4.35 46.52 10.58 41.88 6.53 48.56 12.91 44.52 11.11 52.19 18.09 48.35
CCFinder 10.58 48.65 17.19 45.96 14.63 53.44 23.08 51.90 21.08 58.11 29.42 57.46 24.80 59.52 33.47 62.61
RG-1 8.78 49.54 16.47 46.33 12.83 53.78 21.99 51.76 17.78 57.74 27.35 56.55 22.51 61.84 32.91 60.68
RepoCoder 10.58 51.07 19.06 48.93 15.12 55.66 24.62 53.78 21.24 60.90 31.56 60.00 25.89 63.65 36.21 63.09
DraCo 12.83 50.71 20.33 48.91 19.70 57.17 29.04 56.82 26.68 62.11 36.29 62.75 30.69 65.46 40.64 66.26
RepoFuse 11.22 50.78 19.29 48.77 17.64 56.52 27.02 55.65 23.34 61.28 33.43 61.16 27.73 64.76 38.39 64.82
CodeRAGllmr 14.11 52.44 22.28 51.56 22.89 59.92 32.42 60.24 30.66 65.46 41.13 66.62 35.20 68.93 45.97 70.47
Table 3: Performance of RepoFormer-3B (Use 100% they are surpassed by more sophisticated ap-
| dataforevaluation). |     | “l”:onlyuseleftcontext. |     |     | “lr”:use |           |     |                                  |     |     |     |     |
| ------------------- | --- | ----------------------- | --- | --- | -------- | --------- | --- | -------------------------------- | --- | --- | --- | --- |
|                     |     |                         |     |     |          | proaches. |     | TheresultsindicatethatgeneralRAG |     |     |     |     |
bothleftandrightcontexts.
|     |     |     |     |     |     | indeed | enhances |     | completion |     | but the | improve- |
| --- | --- | --- | --- | --- | --- | ------ | -------- | --- | ---------- | --- | ------- | -------- |
Dataset RepoFormer-3B mentsarelimitedsincegeneralRAGisnottai-
|     |     | CodeMatch |     | IdentifierMatch |     |     |     |     |     |     |     |     |
| --- | --- | --------- | --- | --------------- | --- | --- | --- | --- | --- | --- | --- | --- |
loredtorepository-levelcodecompletion.
|     |     | EM  | ES  | EM  | F1  |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
ReccEvall 12.88 48.21 19.81 36.93 • RepoCoderconsistentlyoutperformsCCFinder
CCEvall 8.18 50.19 15.53 46.25 and RG-1, demonstrating that iterative re-
|     | CCEvallr | 25.29 | 63.45 | 33.77 | 61.48 |         |       |     |            |         |       |     |
| --- | -------- | ----- | ----- | ----- | ----- | ------- | ----- | --- | ---------- | ------- | ----- | --- |
|     |          |       |       |       |       | trieval | (Shao | et  | al., 2023) | exceeds | naive | RAG |
inrepository-levelcodecompletion.
| inAlg.1,respectively. |     |     | Wesetj | to15inmulti-path |     |     |     |     |     |     |     |     |
| --------------------- | --- | --- | ------ | ---------------- | --- | --- | --- | --- | --- | --- | --- | --- |
• DraCoandRepoFuseshowcompetitiveperfor-
| code | retrieval   | and | u to 10  | in reranking. | We use |                                          |     |             |      |             |         |            |
| ---- | ----------- | --- | -------- | ------------- | ------ | ---------------------------------------- | --- | ----------- | ---- | ----------- | ------- | ---------- |
|      |             |     |          |               |        | mance                                    | and | they        | show | much better | results | than       |
| =    | 2,3,4,5,6,7 |     | inAlg.2. |               |        |                                          |     |             |      |             |         |            |
| N    | {           |     | }        |               |        | otherbaselineswhenlargercodeLLMsareused, |     |             |      |             |         |            |
|      |             |     |          |               |        | showing                                  |     | that larger | code | LLMs        | may     | better un- |
3.2 EvaluationResults
|     |     |     |     |     |     | derstand |     | data dependence |     | features, |     | which are |
| --- | --- | --- | --- | --- | --- | -------- | --- | --------------- | --- | --------- | --- | --------- |
3.2.1 OverallPerformance
exploredbyDraCoandRepoFuse.
| Wefirst                    | report | theresults |      | whenusing            | all datafor |                 |     |        |            |        |        |         |
| -------------------------- | ------ | ---------- | ---- | -------------------- | ----------- | --------------- | --- | ------ | ---------- | ------ | ------ | ------- |
|                            |        |            |      |                      |             | • RepoFormer-3B |     |        | using      | only   | left   | context |
| evaluationinTab.1andTab.2. |        |            |      | Inthiscase,LLM       |             |                 |     |        |            |        |        |         |
|                            |        |            |      |                      |             | (ReccEval       |     | and    | CCEval     | ) lags | behind | other   |
|                            |        |            |      |                      |             |                 |     | l      |            | l      |        |         |
| reranker(i.e.,CodeRAG      |        |            |      | )isusedinsteadofdis- |             |                 |     |        |            |        |        |         |
|                            |        |            | llmr |                      |             | methods         |     | except | Zero-Shot. | The    | reason | is that |
tilled reranker (i.e., CodeRAG disr ) since distilled it is optimized to consider both left and right
| rerankerrequirestrainingdata. |          |          |     | Theresultsofsplit- |               |          |          |       |               |         |        |          |
| ----------------------------- | -------- | -------- | --- | ------------------ | ------------- | -------- | -------- | ----- | ------------- | ------- | ------ | -------- |
|                               |          |          |     |                    |               | contexts |          | while | all other     | methods | are    | designed |
| ting                          | data for | training | and | evaluating         | the distilled |          |          |       |               |         |        |          |
|                               |          |          |     |                    |               | to only  | consider |       | left context. |         | Unlike | ReccEval |
rerankerareanalyzedinSec.3.2.3. Theresultsof where the right context for each completion
RepoFormer-3BareprovidedseparatelyinTab.3
caseisunknown,CCEvalhasbothleftandright
sinceitdoesnotrelyonextracodeLLMtogenerate
|     |     |     |     |     |     | contexts. |     | WecanseethatRepoFormer-3Bwhich |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --------- | --- | ------------------------------ | --- | --- | --- | --- |
code. Fromtheresults,wecanobserve:
|     |     |     |     |     |     | takesbothleftandrightpartsasinput(CCEval |     |     |     |     |     | lr ) |
| --- | --- | --- | --- | --- | --- | ---------------------------------------- | --- | --- | --- | --- | --- | ---- |
• Zero-Shotshowstheworstperformanceacross surpasses CCEval , but it is still worse than
l
allsettings,indicatingthatsolelyrelyingoncode CodeRAG using StarCoder2-3B which has the
LLMscannotprovidesatisfyingcompletion.
samemodelsizeasRepoFormer-3B.
• CCFinder and RG-1 using general RAG tech- • CodeRAGachievesthebestperformanceacross
niquessignificantlyoutperformsZero-Shotbut allsettings, showing itseffectiveness. Besides,
23284

the performance gains over baselines consis- 47.48 70.14 70.82
|     |     |     |     |     |     |     |     |     | 44.67 46.54 |     | 70  | 69.04 |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ----------- | --- | --- | ----- | --- |
64.26
| tentlyexistasthesizeofcodeLLMvaries,show- |     |     |     |     |     |     |     | 40    |             |       | 60       |             |       |
| ----------------------------------------- | --- | --- | --- | --- | --- | --- | --- | ----- | ----------- | ----- | -------- | ----------- | ----- |
|                                           |     |     |     |     |     |     |     | 37.27 |             |       |          | 55.23 55.45 | 55.54 |
| ingtherobustnessofCodeRAG.                |     |     |     |     |     |     |     |       |             |       | 50 51.53 |             |       |
|                                           |     |     |     |     |     |     |     | 30    | 26.31 26.65 | 26.81 |          |             |       |
|                                           |     |     |     |     |     |     | ME  |       |             | SE    | 40       |             |       |
21.50
| 3.2.2     | AblationStudy |              |     |         |      |     |     | 20  |     |     | 30  |                  |     |
| --------- | ------------- | ------------ | --- | ------- | ---- | --- | --- | --- | --- | --- | --- | ---------------- | --- |
|           |               |              |     |         |      |     |     |     |     |     | 20  | CodeGen-350m     |     |
| To assess | the           | contribution |     | of each | part | in  |     |     |     |     |     | Qwen2.5-Coder-7B |     |
10
10
| CodeRAG,  | we       | compare  | CodeRAG |                 | with its | vari- |          |     |                                        |     |     |     |      |
| --------- | -------- | -------- | ------- | --------------- | -------- | ----- | -------- | --- | -------------------------------------- | --- | --- | --- | ---- |
|           |          |          |         |                 |          |       |          | 0   |                                        |     | 0   |     |      |
|           |          |          |         |                 |          |       |          | 1   | 3 5                                    | 10  | 1   | 3   | 5 10 |
| ations on | ReccEval |          | in Tab. | 4. Subscripts   |          | “df”, |          |     |                                        |     |     |     |      |
|           |          |          |         |                 |          |       | Figure7: |     | Impactsofnumbersofretainedrerankedcode |     |     |     |      |
| “s”, “d”  | and “lr” | indicate | using   | dataflow-guided |          |       |          |     |                                        |     |     |     |      |
knowledgeonReccEval(Use100%dataforevaluation).
retrieval,sparseretrieval,denseretrievalandLLM
reranker,respectively. Hence,CodeRAG is multi-pathcoderetrieval,thecostisdecidedbythe
df+s+d+lr
identicaltoCodeRAG llmr inTab.1. slowestpath(i.e.,dataflow-guidedretrieval).
| From | the results, |     | we can | observe | that incorpo- |     |     |       |          |         |           |     |            |
| ---- | ------------ | --- | ------ | ------- | ------------- | --- | --- | ----- | -------- | ------- | --------- | --- | ---------- |
|      |              |     |        |         |               |     |     | Since | the main | goal of | this work | is  | not accel- |
rating more retrieval paths brings improvements erating code completion and we do not apply ad-
to code completion in most cases. Besides, us- vancedaccelerationtechniques,webelievethecost
ingrerankingmodulecansignificantlyboostper-
ofCodeRAGcanbefurtherreducedanditwillnot
| formance. | These | findings | highlight |     | the effective- |     |                                 |     |     |     |     |           |     |
| --------- | ----- | -------- | --------- | --- | -------------- | --- | ------------------------------- | --- | --- | --- | --- | --------- | --- |
|           |       |          |           |     |                |     | hinderthepracticaluseofCodeRAG. |     |     |     |     | Wesuggest |     |
nessofeachcomponentofCodeRAGinimproving some possible directions, including constructing
repository-levelcodecompletion. retrieval query in batches and parallelization, ac-
celeratinglogprobabilityguidedprobingthrough
3.2.3 ComparisonsbetweenLLMReranker
|     |     |     |     |     |     |     | applying |     | an inference | speedup |     | framework | (e.g., |
| --- | --- | --- | --- | --- | --- | --- | -------- | --- | ------------ | ------- | --- | --------- | ------ |
andDistilledReranker
vLLM10)ontheproberLLM,usingfastsparseand
We further compare the results of using LLM denseretrievallibraries(e.g.,Faiss11)anddistilling
reranker (CodeRAG ) and using distilled LLMrerankerintoasmallerdistilledreranker.
llmr
| reranker(CodeRAG |     |     | )onReccEvalinTab.5. |     |     | As  |     |     |     |     |     |     |     |
| ---------------- | --- | --- | ------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
disr
|         |      |                                 |     |     |     |     | 3.2.5 | ImpactsofNumbersofRetained |     |     |     |     |     |
| ------- | ---- | ------------------------------- | --- | --- | --- | --- | ----- | -------------------------- | --- | --- | --- | --- | --- |
| CodeRAG | disr | requirestraining,werandomlysam- |     |     |     |     |       |                            |     |     |     |     |     |
ple70%datafortrainingandtheremaining30% RerankedCodeKnowledgePieces
data is used for testing. The results in Tab. 5 are ThererankingstepinCodeRAGonlyretainstop-u
|          |      |          |       |          |          |     | pieces | of  | relevant | code knowledge. |     | In Fig. | 7, we |
| -------- | ---- | -------- | ----- | -------- | -------- | --- | ------ | --- | -------- | --------------- | --- | ------- | ----- |
| reported | over | the test | data. | From the | results, | we  |        |     |          |                 |     |         |       |
canobservethatusingthedistilledrerankeraffects reportthedifferentresultsw.r.t. EMandES(code
theperformancecomparedtousingLLMreranker, match)whensettinguto1,3,5and10. Fromthe
buttheperformanceisstillcompetitive. results,wecanobservethat:
• RegardlessoftheusedcodeLLM,usingalarger
3.2.4 ComputationalCost
ucanenhancethequalityofcodecompletion.
Tab.6providestheaveragecostforaqueryonRec-
• Theimprovementsarenoticeablewhenuisin-
| cEval, excluding |     | the | cost of | code LLM. | We  | can |     |     |     |     |     |     |     |
| ---------------- | --- | --- | ------- | --------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
creasedfromasmallvalue(e.g.,increasefrom
| see that | DraCo | is the | fastest | since it | only | uses a |     |     |     |     |     |     |     |
| -------- | ----- | ------ | ------- | -------- | ---- | ------ | --- | --- | --- | --- | --- | --- | --- |
1to3),buttheenhancementbecomesmarginal
single-way,dataflow-guidedretrieval,andnosimi-
|                       |     |      |                       |            |     |         |     | when u                                     | further | grows (e.g., | increase |     | from 5 to |
| --------------------- | --- | ---- | --------------------- | ---------- | --- | ------- | --- | ------------------------------------------ | ------- | ------------ | -------- | --- | --------- |
| laritysearchisneeded. |     |      | Othermethodsareslower |            |     |         |     |                                            |         |              |          |     |           |
|                       |     |      |                       |            |     |         |     | 10). Thediminishingimprovementsuggeststhat |         |              |          |     |           |
| than DraCo            | as  | they | all require           | similarity |     | search. |     |                                            |         |              |          |     |           |
largerumaypotentiallyintroducelessrelevant
CodeRAGincurshighercostthanbaselinessince
andnecessarycodeknowledgethatdoesnotsig-
| it uses more | ways | of  | retrieval, | applies | log | proba- |     |     |     |     |     |     |     |
| ------------ | ---- | --- | ---------- | ------- | --- | ------ | --- | --- | --- | --- | --- | --- | --- |
nificantlycontributetocodecompletion.
bilityguidedprobingandadistilledrerankerfrom
| BESTFIT     | code | reranking. |           | However, | the       | cost of |           |             |                                   |     |     |     |     |
| ----------- | ---- | ---------- | --------- | -------- | --------- | ------- | --------- | ----------- | --------------------------------- | --- | --- | --- | --- |
|             |      |            |           |          |           |         | 4         | RelatedWork |                                   |     |     |     |     |
| CodeRAG     | is   | close to   | RepoCoder | and      | RepoFuse  |         |           |             |                                   |     |     |     |     |
|             |      |            |           |          |           |         | Recently, |             | thereisasurgeofworksonrepository- |     |     |     |     |
| even though |      | we do      | not use   | advanced | accelera- |         |           |             |                                   |     |     |     |     |
tionmethods. Consideringthesignificantimprove- level code completion. RepoFusion (Shrivastava
etal.,2023)modelstheentirerepositorystructure
mentsofCodeRAGoverbaselines,webelievethe
|     |     |     |     |     |     |     | forcontext-awarecompletion. |     |     |     | RepoCoder(Zhang |     |     |
| --- | --- | --- | --- | --- | --- | --- | --------------------------- | --- | --- | --- | --------------- | --- | --- |
subtleincreaseofoverheadisacceptable.
|     |     |     |     |     |     |     | et  | al., 2023) | employs | an  | iterative | code | retrieval |
| --- | --- | --- | --- | --- | --- | --- | --- | ---------- | ------- | --- | --------- | ---- | --------- |
Tab.7reportstheaveragecostforeachstepof
| CodeRAGonReccEval. |     |     | Wecanseethatthelargest |     |     |     |     |     |     |     |     |     |     |
| ------------------ | --- | --- | ---------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
10https://github.com/vllm-project/vllm
costcomesfromqueryconstruction. Notethat,for 11https://github.com/facebookresearch/faiss
23285

Table4: ComparisonsamongdifferentvariationsofCodeRAGonReccEval(Use100%dataforevaluation). Bold
andunderlinedvaluesindicatethebestandthesecond-bestresults,respectively.
|     |     | CodeGen-350M |     |     | SantaCoder-1.1B |     |     |     | StarCoder2-3B |     |     | Qwen2.5-Coder-7B |     |
| --- | --- | ------------ | --- | --- | --------------- | --- | --- | --- | ------------- | --- | --- | ---------------- | --- |
CodeMatch IdentifierMatch CodeMatch IdentifierMatch CodeMatch IdentifierMatch CodeMatch IdentifierMatch
Methods
|     |     | EM ES | EM  | F1  | EM ES | EM  | F1  | EM  | ES EM | F1  | EM  | ES  | EM F1 |
| --- | --- | ----- | --- | --- | ----- | --- | --- | --- | ----- | --- | --- | --- | ----- |
CodeRAGs 22.07 51.31 29.03 44.80 23.95 56.37 31.36 47.71 33.83 62.03 41.95 57.18 39.89 59.46 36.76 61.24
CodeRAGd 20.49 50.36 27.33 43.41 23.04 55.58 30.52 46.90 32.81 61.53 41.18 56.55 39.66 58.47 36.05 60.90
CodeRAGd+s 22.88 51.95 29.42 45.51 24.90 57.23 32.38 48.58 35.27 63.23 43.80 58.96 41.95 59.59 37.95 62.14
CodeRAGdf 21.28 50.94 28.82 45.20 25.68 57.38 33.98 50.99 35.13 63.25 43.91 60.15 41.86 59.06 37.61 62.79
CodeRAGdf+s 24.21 53.01 31.93 47.94 27.18 59.52 35.47 52.10 39.85 66.35 48.72 64.01 44.21 62.36 52.80 66.62
CodeRAGdf+s+d 23.89 52.86 31.56 47.80 27.70 59.96 36.10 52.72 40.52 66.87 49.65 64.83 44.61 68.81 53.75 66.57
CodeRAGdf+s+d+lr 26.81 55.54 34.02 50.13 36.17 63.00 44.17 59.64 42.69 68.07 51.34 65.73 47.48 70.82 55.47 68.68
Table5: PerformanceonReccEval(Use30%dataforevaluation). Boldandunderlinedvaluesindicatethebestand
thesecond-bestresults,respectively.
|     |     | CodeGen-350M |     |     | SantaCoder-1.1B |     |     |     | StarCoder2-3B |     |     | Qwen2.5-Coder-7B |     |
| --- | --- | ------------ | --- | --- | --------------- | --- | --- | --- | ------------- | --- | --- | ---------------- | --- |
CodeMatch IdentifierMatch CodeMatch IdentifierMatch CodeMatch IdentifierMatch CodeMatch IdentifierMatch
Methods
|     | EM  | ES  | EM F1 | EM  | ES  | EM  | F1  | EM  | ES EM | F1  | EM  | ES EM | F1  |
| --- | --- | --- | ----- | --- | --- | --- | --- | --- | ----- | --- | --- | ----- | --- |
Zero-Shot 4.46 38.09 9.33 26.24 6.87 42.52 13.22 30.28 8.30 44.81 13.99 33.17 12.20 47.55 18.20 36.36
CCFinder 17.68 48.31 23.73 40.82 19.58 50.93 26.76 43.24 28.24 59.22 36.13 53.50 29.52 59.04 37.11 53.36
RG-1 17.63 48.94 24.07 39.54 24.04 54.80 31.06 46.44 29.63 58.96 35.73 51.81 33.52 61.59 39.67 54.93
RepoCoder 20.35 50.84 27.21 42.78 26.86 56.79 34.24 49.22 35.21 63.14 41.82 57.26 34.65 62.19 41.16 55.52
DraCo 22.71 51.83 29.98 46.40 30.19 59.70 39.21 55.66 36.60 64.78 45.41 61.76 39.98 66.23 48.18 62.82
RepoFuse 21.58 51.54 28.81 44.70 29.98 58.60 37.62 52.71 34.03 62.24 41.62 56.94 39.11 65.54 46.03 60.13
CodeRAGllmr 27.73 55.73 34.75 49.97 35.83 63.32 44.08 59.79 43.31 68.54 51.10 65.78 47.57 70.82 54.84 68.38
CodeRAGdisr 23.58 53.31 30.55 47.20 32.65 61.37 41.16 57.06 39.88 66.21 47.62 62.89 44.34 68.42 52.18 64.47
Table6: Averagecost(second)foraqueryonReccEval, donotfullyaddressproblemsdiscussedinSec.1.
excludingthecostforcodegenerationofcodeLLM.
| RepoCoder |     | DraCo | RepoFuse | CodeRAG |      |     | 5                | Conclusion |         |                 |     |          |     |
| --------- | --- | ----- | -------- | ------- | ---- | --- | ---------------- | ---------- | ------- | --------------- | --- | -------- | --- |
| 0.21      |     | 0.04  | 0.15     |         | 0.23 |     |                  |            |         |                 |     |          |     |
|           |     |       |          |         |      |     | We               | present    | a novel | framework       |     | CodeRAG  | for |
|           |     |       |          |         |      |     | repository-level |            |         | code completion |     | CodeRAG. | Its |
Table 7: Average cost (second) for each step of corepartsincludethelogprobabilityguidedquery
CodeRAGonReccEval.
|            |     |                     |     |     |           |     | construction, |     | a multi-path       |     | code | retrieval  | mecha-  |
| ---------- | --- | ------------------- | --- | --- | --------- | --- | ------------- | --- | ------------------ | --- | ---- | ---------- | ------- |
| QueryQuery |     | Multi-pathRetrieval |     |     | Distilled |     |               |     |                    |     |      |            |         |
|            |     |                     |     |     |           |     | nism,         | and | preference-aligned |     |      | reranking. | Experi- |
Construction Sparse Dense Dataflow Reranker mentsdemonstratethatCodeRAGsignificantlyand
0.14 0.002 0.015 0.03 0.06 consistentlyoutperformsstate-of-the-artmethods
|     |     |     |     |     |     |     | onbenchmarks. |          |     | Inthefuture,weplantoexplore |     |          |        |
| --- | --- | --- | --- | --- | --- | --- | ------------- | -------- | --- | --------------------------- | --- | -------- | ------ |
|     |     |     |     |     |     |     | joint         | training | of  | code retriever              |     | and code | LLM to |
andgenerationmechanism. CoCoMIC(Dingetal., furtheralleviatetheirmisalignment.
2024)enhancesaccuracybycombiningcross-file
| and intra-file | contexts. |     | RepoFormer |     | (Wu | et al., | Limitations |     |     |     |     |     |     |
| -------------- | --------- | --- | ---------- | --- | --- | ------- | ----------- | --- | --- | --- | --- | --- | --- |
2024)fine-tunesmodelstodynamicallydecidecon-
|                     |     |                           |     |     |     |     | We  | address | the | misalignment |     | between | code re- |
| ------------------- | --- | ------------------------- | --- | --- | --- | --- | --- | ------- | --- | ------------ | --- | ------- | -------- |
| textretrievalneeds. |     | GraphCoder(Liuetal.,2024) |     |     |     |     |     |         |     |              |     |         |          |
trieverandcodeLLMfromtheperspectiveofde-
modelscontrol-flowdependency,datadependency,
|     |     |     |     |     |     |     | signing | rerankers |     | and modifying |     | retrieval | results |
| --- | --- | --- | --- | --- | --- | --- | ------- | --------- | --- | ------------- | --- | --------- | ------- |
andcontroldependencytoconstructcodeknowl-
|                              |     |     |     |                 |     |     | whilecodeLLMisnotupdatedaccordingly. |     |     |     |     |     | This |
| ---------------------------- | --- | --- | --- | --------------- | --- | --- | ------------------------------------ | --- | --- | --- | --- | --- | ---- |
| edgegraphsforcodecompletion. |     |     |     | ProCC(Tanetal., |     |     |                                      |     |     |     |     |     |      |
2024)integratespromptengineeringwithcontex- ideamaynotfullyalleviatethemisalignment,and
futureworkmayinvolvedesigningnewstrategies,
tualbanditsformulti-perspectivecodecompletion.
suchasjointtrainingormoreefficientinterfacing
DraCo(Chengetal.,2024)andRepoFuse(Liang
mechanismsforbothcoderetrievalandcodeLLM.
| et al., 2024)   | are | closely         | related | to  | CodeRAG.    |     |     |     |     |     |     |     |     |
| --------------- | --- | --------------- | ------- | --- | ----------- | --- | --- | --- | --- | --- | --- | --- | --- |
| DraCo retrieves |     | dataflow-guided |         |     | information |     |     |     |     |     |     |     |     |
Acknowledgments
| to augment | code | completion |     | prompt. |     | Repo- |     |     |     |     |     |     |     |
| ---------- | ---- | ---------- | --- | ------- | --- | ----- | --- | --- | --- | --- | --- | --- | --- |
Fuse (Liang et al., 2024) fuses analogy context This work was supported by National Natural
and rationale context, and uses a code LM like Science Foundation of China (No. 62572410,
UniXcoder(Guoetal.,2022)tochoosethemost 42171456), Natural Science Foundation of Xia-
similarchunkstothetargetchunktoconstructcode men,China(No. 3502Z202471028)andAntGroup
completion prompt. Despite their accuracy, they throughCCF-AntResearchFund.
23286

References Jian Li, Yue Wang, Michael R. Lyu, and Irwin King.
|            |        |             |        |        |           | 2018.            | Code completion |                         | with | neural attention | and |
| ---------- | ------ | ----------- | ------ | ------ | --------- | ---------------- | --------------- | ----------------------- | ---- | ---------------- | --- |
| Loubna Ben | Allal, | Raymond     | Li,    | Denis  | Kocetkov, |                  |                 |                         |      |                  |     |
|            |        |             |        |        |           | pointernetworks. |                 | InIJCAI,pages4159–4165. |      |                  |     |
| Chenghao   | Mou,   | Christopher | Akiki, | Carlos | Muñoz     |                  |                 |                         |      |                  |     |
Ferrandis, Niklas Muennighoff, Mayank Mishra, Raymond Li, Loubna Ben Allal, Yangtian Zi, Niklas
| Alex Gu, | Manan | Dey, | Logesh | Kumar | Umapathi, |     |     |     |     |     |     |
| -------- | ----- | ---- | ------ | ----- | --------- | --- | --- | --- | --- | --- | --- |
Muennighoff,DenisKocetkov,ChenghaoMou,Marc
| Carolyn | Jane | Anderson, | Yangtian | Zi, | Joel Lamy- |         |             |        |     |         |             |
| ------- | ---- | --------- | -------- | --- | ---------- | ------- | ----------- | ------ | --- | ------- | ----------- |
|         |      |           |          |     |            | Marone, | Christopher | Akiki, |     | Jia Li, | Jenny Chim, |
Poirier,HaileySchoelkopf,SergeyTroshin,Dmitry
QianLiu,EvgeniiZheltonozhskii,TerryYueZhuo,
Abulkhanov,ManuelRomero,MichaelLappert,and ThomasWang,OlivierDehaene,MishigDavaadorj,
22 others. 2023. Santacoder: don’t reach for the JoelLamy-Poirier,JoãoMonteiro,OlehShliazhko,
stars! arXivPreprint.
|                                 |           |                       |     |                      |           | and48others.2023. |                             | Starcoder: |       | maythesourcebe |        |
| ------------------------------- | --------- | --------------------- | --- | -------------------- | --------- | ----------------- | --------------------------- | ---------- | ----- | -------------- | ------ |
|                                 |           |                       |     |                      |           | withyou!          | Trans.Mach.Learn.Res.,2023. |            |       |                |        |
| WeiCheng,YuhanWu,andWeiHu.2024. |           |                       |     |                      | Dataflow- |                   |                             |            |       |                |        |
| guided                          | retrieval | augmentation          |     | for repository-level |           |                   |                             |            |       |                |        |
|                                 |           |                       |     |                      |           | Ming Liang,       | Xiaoheng                    | Xie,       | Gehao | Zhang,         | Xunjin |
| codecompletion.                 |           | InACL,pages7957–7977. |     |                      |           |                   |                             |            |       |                |        |
Zheng,PengDi,WeiJiang,HongweiChen,Cheng-
|     |     |     |     |     |     | peng Wang, | and | Gang | Fan. | 2024. | REPOFUSE: |
| --- | --- | --- | --- | --- | --- | ---------- | --- | ---- | ---- | ----- | --------- |
YangruiboDing,ZijianWang,WasiUddinAhmad,Han-
tianDing,MingTan,NihalJain,MuraliKrishnaRa- repository-levelcodecompletionwithfuseddualcon-
| manathan,RameshNallapati,ParminderBhatia,Dan |     |     |                |     |      | text. arXivPreprint. |     |     |     |     |     |
| -------------------------------------------- | --- | --- | -------------- | --- | ---- | -------------------- | --- | --- | --- | --- | --- |
| Roth,andBingXiang.2023.                      |     |     | Crosscodeeval: |     | Adi- |                      |     |     |     |     |     |
WeiLiu,AilunYu,DaoguangZan,BoShen,WeiZhang,
verseandmultilingualbenchmarkforcross-filecode
|             |                             |     |     |     |     | Haiyan      | Zhao, Zhi                         | Jin, and | Qianxiang   |     | Wang. 2024.   |
| ----------- | --------------------------- | --- | --- | --- | --- | ----------- | --------------------------------- | -------- | ----------- | --- | ------------- |
| completion. | InNeurIPS,pages46701–46723. |     |     |     |     |             |                                   |          |             |     |               |
|             |                             |     |     |     |     | Graphcoder: | Enhancingrepository-levelcodecom- |          |             |     |               |
|             |                             |     |     |     |     | pletion     | via code                          | context  | graph-based |     | retrieval and |
YangruiboDing,ZijianWang,WasiUddinAhmad,Mu-
raliKrishnaRamanathan,RameshNallapati,Parmin- languagemodel. arXivPreprint.
| der Bhatia, | Dan | Roth, | and Bing | Xiang. | 2024. Co- |     |     |     |     |     |     |
| ----------- | --- | ----- | -------- | ------ | --------- | --- | --- | --- | --- | --- | --- |
comic: Codecompletionbyjointlymodelingin-file AntonLozhkov,RaymondLi,LoubnaBenAllal,Fed-
|                |     |          |                 |     |       | ericoCassano, | JoelLamy-Poirier, |     |     | NouamaneTazi, |     |
| -------------- | --- | -------- | --------------- | --- | ----- | ------------- | ----------------- | --- | --- | ------------- | --- |
| and cross-file |     | context. | In LREC/COLING, |     | pages |               |                   |     |     |               |     |
AoTang,DmytroPykhtar,JiaweiLiu,YuxiangWei,
3433–3445.
|     |     |     |     |     |     | Tianyang | Liu, Max | Tian, | Denis | Kocetkov, | Arthur |
| --- | --- | --- | --- | --- | --- | -------- | -------- | ----- | ----- | --------- | ------ |
GuantingDong,YutaoZhu,ChenghaoZhang,Zechen Zucker, Younes Belkada, Zijian Wang, Qian Liu,
Wang,ZhichengDou,andJi-RongWen.2024. Un- Dmitry Abulkhanov, Indraneil Paul, and 38 others.
derstand what LLM needs: Dual preference align- 2024. Starcoder2andthestackv2: Thenextgenera-
| ment for | retrieval-augmented |     |     | generation. | arXiv | tion. arXivPreprint. |     |     |     |     |     |
| -------- | ------------------- | --- | --- | ----------- | ----- | -------------------- | --- | --- | --- | --- | --- |
Preprint.
|     |     |     |     |     |     | Yichuan | Ma, Yunfan | Shao, | Peiji | Li, Demin | Song, |
| --- | --- | --- | --- | --- | --- | ------- | ---------- | ----- | ----- | --------- | ----- |
Yunfan Gao, Yun Xiong, Xinyu Gao, Kangxiang Jia, QipengGuo,LinyangLi,XipengQiu,andKaiChen.
JinliuPan,YuxiBi,YiDai,JiaweiSun,QianyuGuo,
|     |     |     |     |     |     | 2025. | Unitcoder: | Scalableiterativecodesynthesis |     |     |     |
| --- | --- | --- | --- | --- | --- | ----- | ---------- | ------------------------------ | --- | --- | --- |
Meng Wang, and Haofen Wang. 2023. Retrieval- withunittestguidance. arXivPreprint.
| augmentedgenerationforlargelanguagemodels: |     |     |     |     | A   |     |     |     |     |     |     |
| ------------------------------------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
survey. arXivPreprint. ErikNijkamp,BoPang,HiroakiHayashi,LifuTu,Huan
Wang,YingboZhou,SilvioSavarese,andCaiming
DayaGuo,ShuaiLu, NanDuan, YanlinWang, Ming Xiong. 2023. Codegen: An open large language
| Zhou,andJianYin.2022.                   |     |     | Unixcoder: | Unifiedcross- |        |       |               |            |     |         |            |
| --------------------------------------- | --- | --- | ---------- | ------------- | ------ | ----- | ------------- | ---------- | --- | ------- | ---------- |
|                                         |     |     |            |               |        | model | for code with | multi-turn |     | program | synthesis. |
| modalpre-trainingforcoderepresentation. |     |     |            |               | InACL, |       |               |            |     |         |            |
InICLR.
pages7212–7225.
RonakPradeep,SahelSharifymoghaddam,andJimmy
| Edward J. | Hu, Yelong | Shen, | Phillip | Wallis, | Zeyuan |           |             |     |                           |     |     |
| --------- | ---------- | ----- | ------- | ------- | ------ | --------- | ----------- | --- | ------------------------- | --- | --- |
|           |            |       |         |         |        | Lin.2023. | Rankvicuna: |     | Zero-shotlistwisedocument |     |     |
Allen-Zhu,YuanzhiLi,SheanWang,LuWang,and
rerankingwithopen-sourcelargelanguagemodels.
| WeizhuChen.2022. |     | Lora: | Low-rankadaptationof |     |     |     |     |     |     |     |     |
| ---------------- | --- | ----- | -------------------- | --- | --- | --- | --- | --- | --- | --- | --- |
arXivPreprint.
| largelanguagemodels. |      |       | InICLR.   |       |            |           |                |     |          |         |         |
| -------------------- | ---- | ----- | --------- | ----- | ---------- | --------- | -------------- | --- | -------- | ------- | ------- |
|                      |      |       |           |       |            | Zhen Qin, | Rolf Jagerman, |     | Kai Hui, | Honglei | Zhuang, |
| Binyuan Hui,         | Jian | Yang, | Zeyu Cui, | Jiaxi | Yang, Day- |           |                |     |          |         |         |
JunruWu,LeYan,JiamingShen,TianqiLiu,Jialu
| iheng Liu, | Lei | Zhang, | Tianyu | Liu, Jiajun | Zhang, |                     |     |              |     |     |            |
| ---------- | --- | ------ | ------ | ----------- | ------ | ------------------- | --- | ------------ | --- | --- | ---------- |
|            |     |        |        |             |        | Liu, DonaldMetzler, |     | XuanhuiWang, |     |     | andMichael |
BowenYu,KaiDang,AnYang,RuiMen,FeiHuang,
|     |     |     |     |     |     | Bendersky.2024. |     | Largelanguagemodelsareeffec- |     |     |     |
| --- | --- | --- | --- | --- | --- | --------------- | --- | ---------------------------- | --- | --- | --- |
XingzhangRen,XuanchengRen,JingrenZhou,and
|                  |     |                               |     |     |     | tivetextrankerswithpairwiserankingprompting. |     |     |     |     | In  |
| ---------------- | --- | ----------------------------- | --- | --- | --- | -------------------------------------------- | --- | --- | --- | --- | --- |
| JunyangLin.2024. |     | Qwen2.5-codertechnicalreport. |     |     |     |                                              |     |     |     |     |     |
| arXivPreprint.   |     |                               |     |     |     | NAACL-HLT(Findings),pages1504–1518.          |     |     |     |     |     |
JiajieJin,YutaoZhu,YujiaZhou,andZhichengDou. BaptisteRozière,JonasGehring,FabianGloeckle,Sten
|     |     |     |     |     |     | Sootla, | Itai Gat, | Xiaoqing | Ellen | Tan, | Yossi Adi, |
| --- | --- | --- | --- | --- | --- | ------- | --------- | -------- | ----- | ---- | ---------- |
2024. BIDER:bridgingknowledgeinconsistencyfor
|     |     |     |     |     |     | Jingyu | Liu, Tal | Remez, | Jérémy | Rapin, | Artyom |
| --- | --- | --- | --- | --- | --- | ------ | -------- | ------ | ------ | ------ | ------ |
efficientretrieval-augmentedllmsviakeysupporting
|           |                               |     |     |     |     | Kozhevnikov, | Ivan | Evtimov, |     | Joanna Bitton, | Man- |
| --------- | ----------------------------- | --- | --- | --- | --- | ------------ | ---- | -------- | --- | -------------- | ---- |
| evidence. | InACL(Findings),pages750–761. |     |     |     |     |              |      |          |     |                |      |
ishBhatt,CristianCanton-Ferrer,AaronGrattafiori,
KarenSpärckJones.2004. Astatisticalinterpretation WenhanXiong,AlexandreDéfossez,JadeCopet,and
oftermspecificityanditsapplicationinretrieval. J. 6others.2023. Codellama:Openfoundationmodels
| Documentation,60(5):493–502. |     |     |     |     |     | forcode. | arXivPreprint. |     |     |     |     |
| ---------------------------- | --- | --- | --- | --- | --- | -------- | -------------- | --- | --- | --- | --- |
23287

Parth Sarthi, Salman Abdullah, Aditi Tuli, Shubh ShengyaoZhuang,HongleiZhuang,BevanKoopman,
Khanna,AnnaGoldie,andChristopherD.Manning. and Guido Zuccon. 2024. A setwise approach for
2024. RAPTOR:recursiveabstractiveprocessingfor effectiveandhighlyefficientzero-shotrankingwith
tree-organizedretrieval. InICLR. largelanguagemodels. InSIGIR,pages38–47.
Zhihong Shao, Yeyun Gong, Yelong Shen, Minlie
Huang,NanDuan,andWeizhuChen.2023. Enhanc-
ingretrieval-augmentedlargelanguagemodelswith
iterative retrieval-generation synergy. In EMNLP
(Findings),pages9248–9274.
Disha Shrivastava, Denis Kocetkov, Harm de Vries,
DzmitryBahdanau,andTorstenScholak.2023. Re-
pofusion: Trainingcodemodelstounderstandyour
repository. arXivPreprint.
Weisong Sun, Chunrong Fang, Yifei Ge, Yuling Hu,
YuchenChen,QuanjunZhang,XiutingGe,YangLiu,
and Zhenyu Chen. 2024. A survey of source code
search: A 3-dimensional perspective. ACM Trans.
Softw.Eng.Methodol.,33(6):166.
Weiwei Sun, Lingyong Yan, Xinyu Ma, Shuaiqiang
Wang,PengjieRen,ZhuminChen,DaweiYin,and
Zhaochun Ren. 2023. Is chatgpt good at search?
investigating large language models as re-ranking
agents. InEMNLP,pages14918–14937.
AlexeySvyatkovskiy,YingZhao,ShengyuFu,andNeel
Sundaresan.2019. Pythia: Ai-assistedcodecomple-
tionsystem. InKDD,pages2727–2735.
HanzhuoTan,QiLuo,LingJiang,ZizhengZhan,Jing
Li,HaotianZhang,andYuqunZhang.2024. Prompt-
basedcodecompletionviamulti-retrievalaugmented
generation. arXivPreprint.
Yanlin Wang and Hui Li. 2021. Code completion by
modelingflattenedabstractsyntaxtreesasgraphs. In
AAAI,pages14015–14023.
DiWu,WasiUddinAhmad,DejiaoZhang,MuraliKr-
ishna Ramanathan, and Xiaofei Ma. 2024. Repo-
former: Selectiveretrievalforrepository-levelcode
completion. InICML,pages53270–53290.
FengjiZhang,BeiChen,YueZhang,JackyKeung,Jin
Liu,DaoguangZan,YiMao,Jian-GuangLou,and
Weizhu Chen. 2023. Repocoder: Repository-level
codecompletionthroughiterativeretrievalandgen-
eration. InEMNLP,pages2471–2484.
LingxiZhang,YueYu,KuanWang,andChaoZhang.
2024. ARL2:aligningretrieverswithblack-boxlarge
languagemodelsviaself-guidedadaptiverelevance
labeling. InACL,pages3708–3719.
Wayne Xin Zhao, Kun Zhou, Junyi Li, Tianyi Tang,
XiaoleiWang,YupengHou,YingqianMin,Beichen
Zhang,JunjieZhang,ZicanDong,YifanDu,Chen
Yang, Yushuo Chen, Zhipeng Chen, Jinhao Jiang,
RuiyangRen,YifanLi,XinyuTang,ZikangLiu,and
3others.2023. Asurveyoflargelanguagemodels.
arXivPreprint.
23288