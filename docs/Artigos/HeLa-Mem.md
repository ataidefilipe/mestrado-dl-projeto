HeLa-Mem: Hebbian Learning and Associative Memory for LLM Agents
JinchangZhu1,a*,JindongLi1*,ChengZhang2*,JiahongLiu3,MenglinYang1,b†
1TheHongKongUniversityofScienceandTechnology(Guangzhou)
|     | 2JilinUniversity | 3TheChineseUniversityofHongKong |     |     |     |     |     |     |     |
| --- | ---------------- | ------------------------------- | --- | --- | --- | --- | --- | --- | --- |
ajzhu997@connect.hkust-gz.edu.cn bmenglinyang@hkust-gz.edu.cn
|     | Abstract |     |     |     | Avg (GPT-4o-mini + GPT-4o) |     |     |          |     |
| --- | -------- | --- | --- | --- | -------------------------- | --- | --- | -------- | --- |
|     |          |     |     | 50  |                            |     |     | HeLa-Mem |     |
(Ours)
| Long-termmemoryisacriticalchallengefor |     |     |     |  Ideal Zone |     |     |     |     |     |
| -------------------------------------- | --- | --- | --- | ----------- | --- | --- | --- | --- | --- |
LargeLanguageModelagents,asfixedcontext
40
windowscannotpreservecoherenceacrossex-
)%( erocS 1F gvA
| tendedinteractions. | Existingmemorysystems |     |     |     |     |     |     |     |     |
| ------------------- | --------------------- | --- | --- | --- | --- | --- | --- | --- | --- |
30
encodeconversationhistoryasembeddingvec-
| torsandretrieveinformationthroughsemantic |     |     |     |     |     |     |     | Methods |     |
| ----------------------------------------- | --- | --- | --- | --- | --- | --- | --- | ------- | --- |
LoCoMo
| similarity.Thisparadigmfailstocapturetheas- |     |     |     | 20  |     |     |     |     |     |
| ------------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
ReadAgent
| sociativestructureofhumanmemory,wherein |     |     |     |     |     |     |     | MemoryBank |     |
| --------------------------------------- | --- | --- | --- | --- | --- | --- | --- | ---------- | --- |
MemGPT
| relatedexperiencesprogressivelystrengthenin- |     |     |     | 10  |     |     |     | A-Mem    |     |
| -------------------------------------------- | --- | --- | --- | --- | --- | --- | --- | -------- | --- |
| terconnectionsthroughrepeatedco-activation.  |     |     |     |     |     |     |     | MemoryOS |     |
HeLa-Mem
| Inspiredbycognitiveneuroscience,weidentify |     |     |     | 0   |     |     |     |     |     |
| ------------------------------------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|                                            |     |     |     | 300 |     | 1K  | 3K  | 10K | 30K |
three mechanisms central to biological mem- Token Cost (Log Scale)
| ory: association, | consolidation, | and spread- |          |     |                |     |                          |     |     |
| ----------------- | -------------- | ----------- | -------- | --- | -------------- | --- | ------------------------ | --- | --- |
|                   |                |             | Figure1: |     | Performancevs. |     | tokenefficiencyonLoCoMo, |     |     |
ingactivation,whichremainlargelyabsentin
current research. To bridge this gap, we pro- averagedacrossGPT-4o-miniandGPT-4o. HeLa-Mem
achievesstrongperformancewithfewertokens,landing
| pose HeLa-Mem, | a bio-inspired | memory ar- |     |     |     |     |     |     |     |
| -------------- | -------------- | ---------- | --- | --- | --- | --- | --- | --- | --- |
chitecturethatmodelsmemoryasadynamic intheupper-leftidealregion.
| graphwithHebbianlearningdynamics.  |            | HeLa-           |          |     |                 |     |         |          |      |
| ---------------------------------- | ---------- | --------------- | -------- | --- | --------------- | --- | ------- | -------- | ---- |
| Mememploysadual-levelorganization: |            | (1)an           |          |     |                 |     |         |          |      |
|                                    |            |                 | reliance |     | on fixed-length |     | context | windows, | LLMs |
| episodic memory                    | graph that | evolves through |          |     |                 |     |         |          |      |
co-activationpatterns,and(2)asemanticmem- struggletomaintainconsistentrepresentationsof
ory store populated via Hebbian Distillation, pastinteractionsasdialoguesextendorspanmul-
whereinaReflectiveAgentidentifiesdensely tiplesessions. Thislimitationoftenleadstofrag-
connectedmemoryhubsanddistillstheminto mentedmemory(Wuetal.,2025;Huetal.,2025;
| structured,reusablesemanticknowledge. |     | This |       |     |            |     |         |                  |     |
| ------------------------------------- | --- | ---- | ----- | --- | ---------- | --- | ------- | ---------------- | --- |
|                                       |     |      | Liang | et  | al., 2025; | Liu | et al., | 2025), resulting | in  |
dual-pathdesignleveragesbothsemanticsim-
factualinconsistencies,diminishedpersonalization,
ilarityandlearnedassociations,mirroringthe
|     |     |     | andunstableagentbehavior. |     |     |     |     | Addressinglong-term |     |
| --- | --- | --- | ------------------------- | --- | --- | --- | --- | ------------------- | --- |
episodic-semanticdistinctioninhumancogni-
memorycoherenceisthereforeessentialforLLM
| tion. Experiments | on LoCoMo | demonstrate |     |     |     |     |     |     |     |
| ----------------- | --------- | ----------- | --- | --- | --- | --- | --- | --- | --- |
superiorperformanceacrossfourquestioncat- agentsoperatinginsettingsthatrequirepersistent
egorieswhileusingsignificantlyfewercontext useradaptation,multi-sessionknowledgeretention,
| tokens. CodeisavailableonGitHub. |     |     | orstablepersonamaintenance. |     |        |            |     |         |        |
| -------------------------------- | --- | --- | --------------------------- | --- | ------ | ---------- | --- | ------- | ------ |
|                                  |     |     | Current                     |     | memory | mechanisms |     | for LLM | agents |
1 Introduction
canbebroadlycategorizedintothreemethodologi-
Largelanguagemodelshavedemonstratedremark- calparadigms. Knowledge-organizationmethods,
able capabilities in language understanding and suchasA-Mem(Xuetal.,2025),structuremem-
generation,enablingincreasinglysophisticatedin- ory into interconnected semantic networks to en-
teractiveagents(Yangetal.,2024;Liuetal.,2026; ableadaptivemanagement. Retrievalmechanism-
Lietal.,2026). However,sustainingcoherentbe- orientedapproaches,exemplifiedbyMemoryBank
havior over long time horizons remains a funda- (Zhong et al., 2024), integrate semantic retrieval
| mentalchallenge(Zhangetal.,2025). |     | Duetotheir |         |        |                     |     |        |               |           |
| --------------------------------- | --- | ---------- | ------- | ------ | ------------------- | --- | ------ | ------------- | --------- |
|                                   |     |            | with    | memory | forgetting          |     | curves | for long-term | up-       |
|                                   |     |            | dating. |        | Architecture-driven |     |        | methods,      | including |
*Equalcontribution.
†Correspondingauthor. MemGPT(Packeretal.,2023),employhierarchi-
13757
Proceedingsofthe64thAnnualMeetingoftheAssociationforComputationalLinguistics(Volume1:LongPapers),pages13757–13769
July2-7,2026©2026AssociationforComputationalLinguistics

calmemorystructureswithexplicitreadandwrite
operationstodynamicallymanagelimitedcontext
| windows. | Althougheffective,theseapproachesare |     |     |     |     |     |     |     |     |     |
| -------- | ------------------------------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- |
typicallydevelopedinisolation,eachprioritizing
| a single | dimension—memory |     | structure, | retrieval |     |     |     |     |     |     |
| -------- | ---------------- | --- | ---------- | --------- | --- | --- | --- | --- | --- | --- |
strategy,orupdatemechanism—whilelargelyover-
lookingtheirmutualinteractionandjointcontribu-
tiontolong-termcoherence.
Morefundamentally,thiscomponent-wiseopti-
mizationoftenoverlooksacriticalaspectoflong-
|                |                                 |                             |               |               |     | Figure2: ConceptualillustrationofHebbianlearning |                        |             |         |               |
| -------------- | ------------------------------- | --------------------------- | ------------- | ------------- | --- | ------------------------------------------------ | ---------------------- | ----------- | ------- | ------------- |
| termcoherence: |                                 | thedynamicevolutionofmemory |               |               |     |                                                  |                        |             |         |               |
|                |                                 |                             |               |               |     | inassociativememory.                             | Twomemorynodes(NeuronA |             |         |               |
| structure.     | Humanmemoryisnotastaticdatabase |                             |               |               |     |                                                  |                        |             |         |               |
|                |                                 |                             |               |               |     | and B) representing                              | distinct               | experiences |         | (e.g., a day- |
| where items    | are                             | stored                      | and retrieved | in isolation; |     |                                                  |                        |             |         |               |
|                |                                 |                             |               |               |     | time event                                       | and a nighttime        | event)      | develop | strength-     |
| rather,        | it is a dynamic                 | system                      | where         | connections   |     |                                                  |                        |             |         |               |
enedsynapticconnectionswhenco-activatedthrough
are continuously reorganized by experience. For sharedcontext. This"neuronsthat firetogether, wire
| example, | a topic | discussed | today might | trigger | a   |     |     |     |     |     |
| -------- | ------- | --------- | ----------- | ------- | --- | --- | --- | --- | --- | --- |
together"principleformsthetheoreticalfoundationof
memoryfromamonthago,notbecausetheyshare HeLa-Mem’sdynamicmemorygraph.
surface-levelkeywords,butbecausetheyarepartof
| thesameevolvingnarrativearc. |     |     | Currentsystems, |     |     |                                             |     |     |     |     |
| ---------------------------- | --- | --- | --------------- | --- | --- | ------------------------------------------- | --- | --- | --- | --- |
|                              |     |     |                 |     |     | ure1). Theprimarycontributionsofourworkare: |     |     |     |     |
bytreatingstorageandretrievalasseparatestatic
processes,failtocapturethisevolvingconnectivity, • WeproposeHeLa-Mem,abio-inspiredframe-
leading to agents that “remember” facts but lack workthatutilizesanOnlineEncoding&As-
the“continuity”ofadevelopingrelationship. sociation mechanism to model conversation
Tobetterunderstandhowlong-termcoherence history as a dynamic Hebbian graph, where
canbemaintained,wedrawonafundamentalprin- co-activatedmemoriesstrengthenconnections
tocapturelatentcontext.
| cipleofbiologicalmemory: |     |     | Hebbianlearning. |     | In  |     |     |     |     |     |
| ------------------------ | --- | --- | ---------------- | --- | --- | --- | --- | --- | --- | --- |
biologicalsystems,experiencesthatarerepeatedly
|              |            |       |                  |          |       | • We introduce | a     | Reflective | Consolidation |               |
| ------------ | ---------- | ----- | ---------------- | -------- | ----- | -------------- | ----- | ---------- | ------------- | ------------- |
| co-activated | gradually  |       | develop stronger | associa- |       |                |       |            |               |               |
|              |            |       |                  |          |       | framework      | using | Hebbian    |               | Distillation, |
| tions, a     | phenomenon | often | summarized       | as       | “neu- |                |       |            |               |               |
whichidentifieshubclustersandtransforms
ronsthatfiretogetherwiretogether”(illustratedin
themintostructuredsemanticknowledge,pre-
| Figure2). | Thisassociativeorganizationallowsre- |     |     |     |     |         |                 |       |           |     |
| --------- | ------------------------------------ | --- | --- | --- | --- | ------- | --------------- | ----- | --------- | --- |
|           |                                      |     |     |     |     | venting | graph explosion | while | retaining | key |
latedmemoriestobeefficientlyreactivatedthrough
information.
spreadingactivationandsupportsthegradualcon-
solidationofepisodicexperiencesintomorestable
|                    |     |                              |     |     |     | • WeimplementaDual-PathRetrievalstrategy |     |     |     |     |
| ------------------ | --- | ---------------------------- | --- | --- | --- | ---------------------------------------- | --- | --- | --- | --- |
| semanticknowledge. |     | Together,association,consol- |     |     |     |                                          |     |     |     |     |
thatleveragesspreadingactivationtotraverse
idation,andspreadingactivationformatightlycou- Hebbian edges, achieving the best average
pledmemoryprocessthatenablesbiologicalsys-
rank(1.25)acrossallquestioncategories.
temstomaintaincoherentrepresentationsoverex-
|     |     |     |     |     |     | • ComprehensiveexperimentsontheLoCoMo |     |     |     |     |
| --- | --- | --- | --- | --- | --- | ------------------------------------- | --- | --- | --- | --- |
tendedtimescales—capabilitiesthatremainlargely
absentfromcurrentartificialmemorydesigns. benchmark validate HeLa-Mem’s effective-
Buildingonthisperspective,weproposeHeLa- ness,achievingsuperiorperformanceacross
Mem (Hebbian Learning associative Memory), fourcategorieswhileusingsignificantlyfewer
contexttokens.
| a unified | memory     | architecture | for              | LLM agents. |     |               |     |     |     |     |
| --------- | ---------- | ------------ | ---------------- | ----------- | --- | ------------- | --- | --- | --- | --- |
| HeLa-Mem  | represents |              | conversational   | history     | as  |               |     |     |     |     |
| a dynamic | graph      | with         | Hebbian learning | dynam-      |     |               |     |     |     |     |
|           |            |              |                  |             |     | 2 RelatedWork |     |     |     |     |
icsandoperatesthroughcoordinatedmechanisms
ofonlineassociation,reflectiveconsolidation,and 2.1 MemoryforLLMAgents
dual-pathretrieval,establishingaunifiedmemory ExistingLargeLanguageModelsfacefundamental
management framework that captures both fine- challengesinhandlingcomplexscenariosrequiring
graineddetailsandhigh-levelpatterns. HeLa-Mem long-term coherence (Hu et al., 2025). Advance-
demonstrates superior performance on LoCoMo mentsinmemorysystemsaddressingthisproblem
whileusingsignificantlyfewercontexttokens(Fig- canbebroadlygroupedintothreecategories.
13758

Biological Hebbian Learning HebbianAssociation ReflectiveConsolidation Retrieval and Response
|     | Co-activation strengthens |          |                   |     |     |         |     | NewTurn |     | Query |     |
| --- | ------------------------- | -------- | ----------------- | --- | --- | ------- | --- | ------- | --- | ----- | --- |
|     |                           | Synapses | Episodic Hebbian  |     |     | Online  |     |         |     |       |     |
Encoding
Memory Store
|     |     |     |     | Spreading Activation |                  |     |     |     |     |     | Dual-Path  |
| --- | --- | --- | --- | -------------------- | ---------------- | --- | --- | --- | --- | --- | ---------- |
|     |     |     |     |                      | (Retrieval Path) |     |     |     |     |     | Retrieval  |
Neurons that fire together, wire together
Repetition consolidates memory trace
|     |     |     | Guide |     |     | Hebbian Distillation |     |     |     |     |     |
| --- | --- | --- | ----- | --- | --- | -------------------- | --- | --- | --- | --- | --- |
Dual-Path Ranking
Repeated co-occurrence consolidates memory
|     |     | trace |     |     |     |     |     |     | Episodic Context |     |     |
| --- | --- | ----- | --- | --- | --- | --- | --- | --- | ---------------- | --- | --- |
Semantic
|     | Spreading activation |                 |     |                         |     |                  |            | Memory Store |                  |     |     |
| --- | -------------------- | --------------- | --- | ----------------------- | --- | ---------------- | ---------- | ------------ | ---------------- | --- | --- |
|     |                      | Supports recall |     |                         |     |                  |            |              | Semantic Context |     |     |
|     |                      |                 |     |                         |     | Reflective Agent | Adaptive   |              |                  |     |     |
|     |                      |                 |     | Episodic node growth +  |     |                  | Forgetting |              |                  |     |     |
Activation spreads along associative pathways for  Hebbian update Feedback (Experience)
context-based recall
Figure3: ThearchitecturaloverviewofHeLa-Mem. Theframeworkconsistsofthreemodules: (1)Hebbian
Associationfordynamicgraphconstruction(Section3.2);(2)ReflectiveConsolidationforsemanticknowledge
distillation(Section3.3);and(3)RetrievalandResponseusingaDual-Pathstrategy(Section3.4).
Knowledge-organizationmethodsfocusoncap- dationalprincipleinneurosciencedescribinghow
turingandstructuringintermediatereasoningstates. synapticconnectionsstrengthenthroughcorrelated
Think-in-Memory(Liuetal.,2023)storesevolving activity(seeFigure2). Formally,givenactivation
chains-of-thought, enabling consistency through states x i and x j of two neurons, the connection
continualupdates. A-Mem(Xuetal.,2025)orga- weightw isupdatedas∆w = η x x ,where
|     |     |     |     |     |     |     | ij  |     | ij  | i   | j   |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     |     |     |     |     |     |     |     |     |     | · · |     |
nizes knowledge into an interconnected note net- η isthelearningrate. Thisprinciplehasbeenap-
workthatspanssessions. pliedinHopfieldnetworks(Hopfield,1982),which
Retrievalmechanism-orientedapproaches,pio- demonstrate how recurrent neural networks with
neered by RAG (Lewis et al., 2020), enrich the symmetricconnectionscanfunctionasassociative
model with external memory libraries. Memo- memories,storingandretrievingpatternsthrough
ryBank (Zhong et al., 2024) logs conversations, energy minimization. More recently, Ramsauer
etal.(2020)showthatmodernHopfieldnetworks
| events, | and | user traits | in a vector | database | and |     |     |     |     |     |     |
| ------- | --- | ----------- | ----------- | -------- | --- | --- | --- | --- | --- | --- | --- |
refreshes them using a forgetting-curve schedule. withcontinuousstatesaremathematicallyequiva-
GenerativeAgents(Parketal.,2023)keepmemo- lenttotheattentionmechanisminTransformers,re-
riesinnaturallanguageandaddareflectionloopfor vealingdeepconnectionsbetweenbiologicalmem-
relevancefiltering. EmotionalRAG(Huangetal., oryprinciplesandcontemporarydeeplearningar-
2024)retrievesmemoryentriesbycombiningse- chitectures. InthecontextofLLMagents,Hebbian
manticsimilaritywiththeagent’semotionalstate. dynamics offer a principled approach to capture
latentassociationsbetweenmemoriesthatmaynot
|     | Architecture-driven |     | designs alter | the core | con- |     |     |     |     |     |     |
| --- | ------------------- | --- | ------------- | -------- | ---- | --- | --- | --- | --- | --- | --- |
trol flow to manage context explicitly. MemGPT beapparentfromsemanticsimilarityalone.
| (Packer                       |     | et al., 2023) | adopts an OS-like | hierarchy |     |                        |     |     |     |     |     |
| ----------------------------- | --- | ------------- | ----------------- | --------- | --- | ---------------------- | --- | --- | --- | --- | --- |
|                               |     |               |                   |           |     | 3 HeLa-MemArchitecture |     |     |     |     |     |
| withdedicatedread/writecalls. |     |               | SCM(Liangetal.,   |           |     |                        |     |     |     |     |     |
2023)introducesdualbuffersandamemorycon- Inspired by the synaptic plasticity of the human
| trollerthatgatesselectiverecall. |     |     |     | Mem0(Chhikara |     |     |     |     |     |     |     |
| -------------------------------- | --- | --- | --- | ------------- | --- | --- | --- | --- | --- | --- | --- |
brain,HeLa-Memmodelsconversationhistoryasa
etal.,2025)dynamicallyextractsandconsolidates
dynamicassociativegraphratherthanastaticlog.
salientinformationforscalablelong-termmemory. Our design is guided by three neuroscience intu-
MemoryOS(Kangetal.,2025)introducesathree-
|     |     |     |     |     |     | itions: | (1)AssociationoverIsolation—memories |     |     |     |     |
| --- | --- | --- | --- | --- | --- | ------- | ------------------------------------ | --- | --- | --- | --- |
tierhierarchicalstoragewithshort-term,mid-term,
|     |     |     |     |     |     | that | co-occur | should wire | together, | forming | la- |
| --- | --- | --- | --- | --- | --- | ---- | -------- | ----------- | --------- | ------- | --- |
andlong-termmemoryunits,employingsegment- tent pathways beyond simple semantic similar-
pageorganizationfordynamicupdating. ity;(2)ActiveConsolidation—frequentlyaccessed
memoryclustersshouldsolidifyintostableknowl-
2.2 HebbianLearninginNeuralNetworks
|     |     |     |     |     |     | edge, | similar | to sleep-based | consolidation; |     | and |
| --- | --- | --- | --- | --- | --- | ----- | ------- | -------------- | -------------- | --- | --- |
Hebbian learning, summarized as “neurons that (3) Spreading Retrieval—recalling one memory
firetogetherwiretogether”(Hebb,2005),isafoun- should naturally trigger related concepts through
13759

| establishedsynapticroutes. |     |     |     |     |     |     | 3.2 OnlineEncoding&Association |     |     |     |     |     |     |
| -------------------------- | --- | --- | --- | --- | --- | --- | ------------------------------ | --- | --- | --- | --- | --- | --- |
Basedontheseprinciples(Figure3),HeLa-Mem Synapticefficacyinthebrainisnotfixed;itisplas-
operatesthroughacontinuouscognitivelifecycle:
|     |     |     |     |     |     |     | tic,evolvingbasedonactivitypatterns. |     |     |     |     | Weemulate |     |
| --- | --- | --- | --- | --- | --- | --- | ------------------------------------ | --- | --- | --- | --- | --------- | --- |
thisdynamicthroughHebbianlearningtocapture
| • OnlineEncoding&Association: |     |     |     |     |     | Conversa- |     |     |     |     |     |     |     |
| ----------------------------- | --- | --- | --- | --- | --- | --------- | --- | --- | --- | --- | --- | --- | --- |
latentassociationsthatsemanticembeddingsalone
tionturnsareencodedintotheEpisodicMem-
mightmiss.
oryGraph,whereaHebbianLearningmech-
Followingtheneuroscienceprinciplethat“neu-
| anism | dynamically |     | strengthens |     | connections |     |     |     |     |     |     |     |     |
| ----- | ----------- | --- | ----------- | --- | ----------- | --- | --- | --- | --- | --- | --- | --- | --- |
ronsthatfiretogetherwiretogether,”edgeweights
betweenco-activatedmemories.
strengthenwhenmemoriesareco-activatedduring
| • ReflectiveMemoryAgent: |     |     |     | Uponreachingas- |     |     | retrieval: |     |     |     |     |     |     |
| ------------------------ | --- | --- | --- | --------------- | --- | --- | ---------- | --- | --- | --- | --- | --- | --- |
sociativethresholds,thisagentidentifieshub
|                                          |     |     |     |     |     |     | w (t+1) | = (1 | λ)  | w (t) +η | I(v                 | ,v  | ), (1) |
| ---------------------------------------- | --- | --- | --- | --- | --- | --- | ------- | ---- | --- | -------- | ------------------- | --- | ------ |
|                                          |     |     |     |     |     |     |         |      |     |          |                     | i j | t      |
| nodesandappliesHebbianDistillationtocon- |     |     |     |     |     |     | ij      |      | − · | ij       | ·                   | ∈   | K      |
| solidatethemintostablesemanticknowledge, |     |     |     |     |     |     |         |      |     |          | activereinforcement |     |        |
synapticdecay
preventingnoiseaccumulation.
|             |     |            |     |        |       |       | where  | λ is|the | de{czay   | ra}te, | η| is    | the {z learning | } rate,    |
| ----------- | --- | ---------- | --- | ------ | ----- | ----- | ------ | -------- | --------- | ------ | -------- | --------------- | ---------- |
|             |     |            |     |        |       |       | and I( | ) is an  | indicator |        | that the | pair            | (v ,v ) is |
| • Dual-Path |     | Retrieval: |     | During | query | time, |        |          |           |        |          |                 | i j        |
·
queries activate both specific episodic de- co-activated in the current retrieval set . This
K t
tailsandbroadersemanticknowledgethrough dynamic allows frequently correlated memories
tostrengthenwhileunusedconnectionsfadeover
spreadingactivation.
time.
3.1 MemoryStorage
|     |     |     |     |     |     |     | 3.3 ReflectiveMemoryAgent |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ------------------------- | --- | --- | --- | --- | --- | --- |
3.1.1 EpisodicMemoryGraph
|              |     |       |            |     |          |      | While | associative | learning |     | happens | during | active |
| ------------ | --- | ----- | ---------- | --- | -------- | ---- | ----- | ----------- | -------- | --- | ------- | ------ | ------ |
| Conversation |     | turns | are stored |     | as nodes | in a |       |             |          |     |         |        |        |
retrieval,long-termmemorymaintenancerelieson
| weighted  | graph.  | Each       | node | contains |            | the origi- |                      |     |     |                         |     |     |     |
| --------- | ------- | ---------- | ---- | -------- | ---------- | ---------- | -------------------- | --- | --- | ----------------------- | --- | --- | --- |
|           |         |            |      |          |            |            | activeconsolidation. |     |     | Topreventmemoryoverload |     |     |     |
| nal text, | a dense | embedding, |      | the      | timestamp, | ex-        |                      |     |     |                         |     |     |     |
andcrystallizeimportantinformation,weintroduce
| tracted keywords, |     | and | the | speaker | role. | Edges |              |       |      |        |     |             |        |
| ----------------- | --- | --- | --- | ------- | ----- | ----- | ------------ | ----- | ---- | ------ | --- | ----------- | ------ |
|                   |     |     |     |         |       |       | a Reflective | Agent | that | mimics |     | the brain’s | sleep- |
betweennodesrepresentassociativeconnections,
basedconsolidationprocessthroughHebbianDis-
| with weights | indicating |     | the | strength | of  | associa- |     |     |     |     |     |     |     |
| ------------ | ---------- | --- | --- | -------- | --- | -------- | --- | --- | --- | --- | --- | --- | --- |
tillation.
tion. Initially,consecutiveturnsareconnectedwith
TheReflectiveAgentmonitorsthegraph’sstruc-
smallweights;theseweightsevolvethroughHeb-
|     |     |     |     |     |     |     | tural evolution |     | to manage |     | the memory |     | lifecycle |
| --- | --- | --- | --- | --- | --- | --- | --------------- | --- | --------- | --- | ---------- | --- | --------- |
bianlearning.
(seeFigure4),analogoustosleep-basedmemory
| 3.1.2 SemanticMemoryStore |     |     |     |     |     |     | consolidationinthebrain. |     |     |     |     |     |     |
| ------------------------- | --- | --- | --- | --- | --- | --- | ------------------------ | --- | --- | --- | --- | --- | --- |
Thesemanticlevelstoresdistilledknowledgeex- Hub Detection. Nodes that have accumulated
|               |          |              |           |                 |               |       | high total                                      | edge | weight   | through       |     | Hebbian | learning  |
| ------------- | -------- | ------------ | --------- | --------------- | ------------- | ----- | ----------------------------------------------- | ---- | -------- | ------------- | --- | ------- | --------- |
| tracted from  | episodic |              | memories: |                 | specifically, | we    |                                                 |      |          |               |     |         |           |
|               |          |              |           |                 |               |       | are identified                                  |      | as hubs. | Specifically, |     | a       | node v is |
| apply Hebbian |          | Distillation |           | on hub-centered |               | clus- |                                                 |      |          |               |     |         | i         |
|               |          |              |           |                 | distilled     | se-   | flaggedforconsolidationifitsassociativestrength |      |          |               |     |         |           |
| ters in the   | episodic | graph        | to        | produce         |               |       |                                                 |      |          |               |     |         |           |
exceedsathresholdδ
| mantic records |     | with | traceable | evidence |     | links to |     |     |     | hub : |     |     |     |
| -------------- | --- | ---- | --------- | -------- | --- | -------- | --- | --- | --- | ----- | --- | --- | --- |
theirsourceturns.
|     |     |     |     |     |     |     |     | D(v | ) = |     | w > | δ . | (2) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     |     |     |     |     |     |     |     |     | i   |     | ij  | hub |     |
j (i)
| • UserModel: |         | Stableusercharacteristics(e.g., |              |      |            |     |      |           |     | ∈XN  |          |              |     |
| ------------ | ------- | ------------------------------- | ------------ | ---- | ---------- | --- | ---- | --------- | --- | ---- | -------- | ------------ | --- |
| “enjoys      | outdoor |                                 | activities”) | with | confidence |     |      |           |     |      |          |              |     |
|              |         |                                 |              |      |            |     | Upon | detecting |     | that | a node’s | accumulative |     |
scoresandsupportingevidence.
|           |             |     |           |          |       |           | weight                   | exceeds   | the       | threshold  | δ hub                | , the      | agent trig- |
| --------- | ----------- | --- | --------- | -------- | ----- | --------- | ------------------------ | --------- | --------- | ---------- | -------------------- | ---------- | ----------- |
|           |             |     |           |          |       |           | gersHebbianDistillation. |           |           |            | Tocapturethefullcon- |            |             |
| • Factual | Memory:     |     | Extracted |          | facts | with ab-  |                          |           |           |            |                      |            |             |
|           |             |     |           |          |       |           | text, the                | agent     | retrieves | the        | hub                  | node along | with        |
| solute    | timestamps, |     | such      | as event |       | dates and |                          |           |           |            |                      |            |             |
|           |             |     |           |          |       |           | its strongly             | connected |           | neighbors. |                      | The        | LLM syn-    |
relationships.
thesizesthisclusterofrelatedmemoriestoidentify
commonthemesandcausalrelationships,abstract-
| • Agent | Knowledge: |     | The | agent’s | established |     |     |     |     |     |     |     |     |
| ------- | ---------- | --- | --- | ------- | ----------- | --- | --- | --- | --- | --- | --- | --- | --- |
persona,preferences,andbehavioralpatterns. ingthemintodeclarativesemanticentries. These
distilledrecordsarestoredintheSemanticMemory
This serves as long-term memory that persists Store,effectivelycompressingrepetitiveepisodic
beyondconversationwindows. detailsintostable,generalizableknowledge.
13760

AdaptiveForgetting. Thisprocessistriggered Reflective Agent: Memory Lifecycle Management
Hub Detection Distillation | Isolated Detection Forgetting
whenanode’sstatusfallsbelowcriticalretention
thresholds. Amemoryisflaggedforremovalonly Hub de Is g o =2 deg=8 de H g u = b 14 de H g u = b 11
if it simultaneously satisfies three criteria: (1) its deg=10
totaledgeweightisbelowδ prune (indicatingstruc- de H g u = d b 1 e Is 1 g o =2 Distillation de H g u = b 14 Hub de Is g o =3
turalirrelevance),(2)itsinactivedurationexceeds (Semantic KB) deg=10
Hub
δ (indicatingtemporaldormancy),and(3)ithas deg=9 deg=11
age deg=5
zerorecentaccess. Thisstrictcompoundcriterion deg=6 de H g u = b 17 deg=7
ensuresthatthesystemselectivelyremovesnoise de H g u = b 13 de Is g o =1 (R e F m or o g v e e t ) ting
whilepreservingstrong,albeitolder,associations. deg=9 deg=4de H g u = b 12deg=8 deg=9
Nodes: 23 | Hub: 10 (Distill) | Isolated: 4 (Forget) | Normal: 9
3.4 Dual-PathRetrieval
Hub Nodes (deg 10) Distillation
Normal Nodes
Human memory retrieval is rarely a single-step
Isolated Nodes (deg < 4) Forgetting
lookup;itisaspreadingactivationprocesswhere
Figure4: HebbianmemorygraphshowingtheReflec-
onethoughttriggersanother. HeLa-Memadoptsa
tiveAgent’sdualrole. Hubnodes(red, highdegree)
dual-pathretrievalstrategytoemulatethisinterac-
arecandidatesforHebbianDistillation,consolidatingre-
tion between direct recall and associative spread-
latedmemoriesintostructuredsemanticknowledge.Iso-
ing.
latednodes(gray,lowdegreewithdashedcircles)are
Givenaquery,retrievalproceedsintwostages. candidatesforAdaptiveForgetting,maintainingmem-
BaseActivation. Eachepisodicnodereceives oryefficiency.
an initial score combining embedding similarity,
temporaldecay,andkeywordoverlap:
Thisdual-pathapproachensuresretrievalofboth
S base (v i ) = (sim(q,e i )+α keyword_match) semanticallyrelevantmemoriesandassociatively
·
γ(v ), linkedmemoriesthatspreadingactivationsurfaces.
i
·
(3) Semantic memory entries are also retrieved and
wheresim( , )denotescosinesimilaritybetween mergedtoformthefinalcontext.
· ·
the query embedding q and node embedding e ,
i
3.5 ResponseGeneration
γ(v ) = exp( ∆t/τ)isthetemporaldecayfactor
i
−
withtimeconstantτ,andαcontrolsthebonusfor TheLLMgeneratesresponsesusingtheintegrated
keywordmatches. context (episodic memories and semantic knowl-
Spreading Activation. High-scoring nodes edge)alongwithasystempromptthatestablishes
propagateactivationthroughHebbianedges: theconversationalrole. Thedetailedpromptstruc-
tureisprovidedinAppendixA.
S(v ) = S (v )+β S (v ) w , (4)
j base j base i ij
·
i (j) 4 Experiments
∈XN
where (j) denotes the neighbors of node v in
j 4.1 ExperimentalSettings
N
thememorygraph,w istheHebbianedgeweight,
ij
Dataset. WeconductexperimentsontheLoCoMo
and β controls the spreading activation strength.
benchmark (Maharana et al., 2024), specifically
Thisenablesretrievalofmemoriesthataresemanti-
designed for assessing long-term conversational
callydistantfromthequerybutstronglyassociated
memorycapabilities. Itconsistsofultra-longdia-
withinitiallyactivatedcontent—particularlybene-
loguesaveraging300turnsandabout9Ktokensper
ficialformulti-hopreasoning.
conversation. Questionsspanmultiplecategories
Dual-Path Ranking. The final retrieval set is
tosystematicallyevaluatememoryabilities.
constructedbycombiningtworankedlists:
EvaluationMetrics. Followingpriorworkon
final = Top-k(S base ) Top-m(S v / Top-k), long-termconversationalmemory(Maharanaetal.,
R ∪ | ∈
2024;Xuetal.,2025),weemploystandardF1and
basepath flippath
(5) BLEU-1scorestoevaluateperformance.
| {z } | {z }
where the base path selects the top-k nodes by ComparedMethods. WecompareHeLa-Mem
S , and the flip path promotes up to m ad- withrepresentativememorymethodsincludingLo-
base
ditional nodes that rank highest by spreading- CoMo (Native), ReadAgent (Lee et al., 2024),
augmentedscoreS butwerenotalreadyselected. MemoryBank (Zhong et al., 2024), MemGPT
13761

(Packer et al., 2023), A-Mem (Xu et al., 2025), manceacrossallbackbones. HeLa-Memachieves
Mem0 (Chhikara et al., 2025), LightMem (Fang thebestAverageRankof1.25,significantlysur-
etal.,2025),andMemoryOS(Kangetal.,2025). passingMemoryOS(2.25). Thisconfirmsthatthe
Baseline results for GPT-4o-mini, GPT-4o, and theoreticaladvantagesofHebbiandynamicstrans-
Qwen2.5-3b are reported from Xu et al. (2025); late into robust empirical gains regardless of the
results for Qwen2.5-14b are reported from Yan underlyingLLM’sscale.
| etal.(2025). | MemoryOSresultsmarkedwith |     |     |     |     | are |     |     |     |     |     |     |
| ------------ | ------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
†
reproducedbyus.
|                            |     |          |     | We evaluate |              | HeLa- | 4.3 AblationStudy |     |     |     |     |     |
| -------------------------- | --- | -------- | --- | ----------- | ------------ | ----- | ----------------- | --- | --- | --- | --- | --- |
| Implementation             |     | Details. |     |             |              |       |                   |     |     |     |     |     |
| MemacrossfourbackboneLLMs: |     |          |     |             | GPT-4o-mini, |       |                   |     |     |     |     |     |
GPT-4o(Achiametal.,2023),Qwen2.5-14b,and Tounderstandthecontributionofeachcomponent
inHeLa-Mem,weconductablationexperimentsby
| Qwen2.5-3b(Yangetal.,2024). |     |     |     | ForHeLa-Mem, |     |     |     |     |     |     |     |     |
| --------------------------- | --- | --- | --- | ------------ | --- | --- | --- | --- | --- | --- | --- | --- |
the time decay constant is set to τ = 60 days. removingkeymodules. Table3presentstheresults
| Episodic | retrieval | uses | k = | 10, and | semantic | re- | onGPT-4o-mini. |     |     |     |     |     |
| -------- | --------- | ---- | --- | ------- | -------- | --- | -------------- | --- | --- | --- | --- | --- |
trieval uses k = 5. The Hebbian learning rate is Removing the
|                         |     |                             |     |                    |     |     | Effect     | of Reflective |       | Agent.   |             |        |
| ----------------------- | --- | --------------------------- | --- | ------------------ | --- | --- | ---------- | ------------- | ----- | -------- | ----------- | ------ |
| η = 0.02,edgedecayrateλ |     |                             | =   | 0.995,spreadingac- |     |     |            |               |       |          |             |        |
|                         |     |                             |     |                    |     |     | Reflective | Memory        | Agent | causes   | the largest | per-   |
| tivationstrengthβ       |     | = 0.1,andspreadingthreshold |     |                    |     |     |            |               |       |          |             |        |
|                         |     |                             |     |                    |     |     | formance   | drop (34.74%  |       | 29.87%), | with        | Multi- |
→
θ = 0.6.
hopreasoningsufferingmostseverely(36.04%
→
|     |     |     |     |     |     |     | 30.17%). | This | confirms | that | the meta-cognitive |     |
| --- | --- | --- | --- | --- | --- | --- | -------- | ---- | -------- | ---- | ------------------ | --- |
4.2 MainResults
componentisessentialforidentifyinghigh-degree
| Table 1 | presents | the detailed |     | performance |     | break- |           |     |            |         |               |     |
| ------- | -------- | ------------ | --- | ----------- | --- | ------ | --------- | --- | ---------- | ------- | ------------- | --- |
|         |          |              |     |             |     |        | hub nodes | and | triggering | Hebbian | Distillation, |     |
downacrossfourdifferentLLMbackbones: GPT- whichconsolidatesrelatedepisodicmemoriesinto
4o-mini,GPT-4o,Qwen2.5-14b,andQwen2.5-3b.
structuredsemanticknowledge.
ResultsshowthatHeLa-Memconsistentlyoutper-
|                                |     |        |         |       |            |     | Effect                                        | of Spreading |                               | Activation. |     | Disabling |
| ------------------------------ | --- | ------ | ------- | ----- | ---------- | --- | --------------------------------------------- | ------------ | ----------------------------- | ----------- | --- | --------- |
| forms baselines                |     | across | varying | model | sizes      | and |                                               |              |                               |             |     |           |
| capabilities.                  |     |        |         |       |            |     | spreadingactivationleadstoanotableperformance |              |                               |             |     |           |
|                                |     |        |         |       |            |     | decline(34.74%                                |              | 32.19%),particularlyaffecting |             |     |           |
| DetailedAnalysis(GPT-4o-mini). |     |        |         |       | Focusingon |     |                                               |              |                               |             |     |           |
→
|                                           |     |             |             |     |     |        | Multi-hop                    | reasoning | (36.04% |     | 33.88%).         | This |
| ----------------------------------------- | --- | ----------- | ----------- | --- | --- | ------ | ---------------------------- | --------- | ------- | --- | ---------------- | ---- |
| GPT-4o-miniasarepresentativecase,HeLa-Mem |     |             |             |     |     |        |                              |           |         |     | →                |      |
|                                           |     |             |             |     |     |        | validatesourdual-pathdesign: |           |         |     | withoutspreading |      |
| demonstrates                              |     | significant | advantages. |     | In  | Multi- |                              |           |         |     |                  |      |
activation,thesystemdegradestoasinglesemantic
hopreasoning,itachieves40.14%,outperforming
|                                   |     |     |     |     |     |      | path, failingtoretrievememoriesthatareseman- |     |     |     |     |     |
| --------------------------------- | --- | --- | --- | --- | --- | ---- | -------------------------------------------- | --- | --- | --- | --- | --- |
| MemoryOS(38.39%)andA-Mem(27.02%). |     |     |     |     |     | This |                                              |     |     |     |     |     |
ticallydistantfromthequerybutstronglyassoci-
validatestheHebbiangraph’sabilitytobridgedis-
parateinformationpiecesthroughlearnedassocia- atedthroughHebbianconnections,whichiscrucial
formulti-hopreasoningthatrequiresbridgingdis-
tions.
|     |     |     |     |     |     |     | paratepiecesofinformation. |     |     | Thisunderscoresthe |     |     |
| --- | --- | --- | --- | --- | --- | --- | -------------------------- | --- | --- | ------------------ | --- | --- |
ForTemporaltasks,HeLa-Memscores47.29%,
valueofleveraginghistoricallylearnedpathways
| surpassingMemoryOS(41.58%). |     |     |     | Thepreservation |     |     |     |     |     |     |     |     |
| --------------------------- | --- | --- | --- | --------------- | --- | --- | --- | --- | --- | --- | --- | --- |
ratherthanrelyingsolelyonstaticsemanticsimi-
| of absolute | timestamps |     | during | distillation |     | allows |     |     |     |     |     |     |
| ----------- | ---------- | --- | ------ | ------------ | --- | ------ | --- | --- | --- | --- | --- | --- |
larity.
| accurategroundingofrelativetimeexpressions. |     |     |     |     |     | In  |     |     |     |     |     |     |
| ------------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
OpenDomainquestions,itreaches29.70%,provid- Effect of Adaptive Forgetting. Interestingly,
ingusefulsemanticcontextevenfortopicsoutside removing the forgetting mechanism shows mini-
the main conversation flow. HeLa-Mem leads in mal impact on the current LoCoMo benchmark.
Single-hoptasks(51.89%),demonstratingthatthe Weattributethistothelimitedconversationlength
hierarchical retrieval approach remains effective ( 300turns),whichdoesnotyetsaturatethemem-
∼
forstraightforwardfactualqueries. ory capacity. However, forgetting is critical for
TokenEfficiency. Notably,HeLa-Memachieves scalabilityinreliableagentdeployment. Without
theseresultsusingonly 1,010tokensonaverage. it,thememorystorewouldgrowunboundedly,in-
∼
Thisefficiencystemsfromtheselectivenatureof evitablyincreasingretrievalcostsandintroducing
Hebbian retrieval, which surfaces only the most noisefromobsoleteinformation. Thismechanism
stronglyassociatedmemorieswithoutthecomputa- ensuresthatthesystem’sperformanceremainssta-
tionaloverheadofprocessingfullcontextwindows. bleregardlessofconversationduration, actingas
Robustness Across Backbones. To validate agarbagecollectionprocessforirrelevantassocia-
| stability,Table2summarizestheaveragedperfor- |     |     |     |     |     |     | tions. |     |     |     |     |     |
| -------------------------------------------- | --- | --- | --- | --- | --- | --- | ------ | --- | --- | --- | --- | --- |
13762

Table1: ExperimentalresultsonLoCoModatasetofQAtasksacrossfourcategories(MultiHop,Temporal,Open
Domain, and Single Hop) using different methods. Results are reported in F1 and BLEU-1 (%) scores. Best
performancepermodelismarkedinbold. Missingbaselinesaremarkedwith“-”(TokenLength( ): lowervalues
↓
| arebetter; | † : Reproducedresults). |     |     |          |          |      |            |      |           |      |           |
| ---------- | ----------------------- | --- | --- | -------- | -------- | ---- | ---------- | ---- | --------- | ---- | --------- |
|            |                         |     |     | MultiHop | Temporal |      | OpenDomain |      | SingleHop |      | Token     |
| Model      | Method                  |     | F1  | BLEU     | F1       | BLEU | F1         | BLEU | F1        | BLEU | Length( ) |
↓
LoCoMo 25.02 19.75 18.41 14.77 12.04 11.16 40.36 29.05 16,910
|     | ReadAgent |     | 9.15 | 6.48 | 12.60 | 8.87 | 5.31 | 5.12 | 9.67 | 7.66 | 643 |
| --- | --------- | --- | ---- | ---- | ----- | ---- | ---- | ---- | ---- | ---- | --- |
inim-o4-TPG
|     | MemoryBank |     | 5.00  | 4.77  | 9.68  | 6.99  | 5.56  | 5.94  | 6.61  | 5.16  | 432    |
| --- | ---------- | --- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ------ |
|     | MemGPT     |     | 26.65 | 17.72 | 25.52 | 19.44 | 9.15  | 7.44  | 41.04 | 34.34 | 16,977 |
|     | A-Mem      |     | 27.02 | 20.09 | 45.85 | 36.67 | 12.14 | 12.00 | 44.65 | 37.06 | 2,520  |
MemoryOS† 38.39 29.52 41.58 35.99 23.75 17.17 45.86 40.70 2,000
HeLa-Mem 40.14 31.26 47.29 41.28 29.70 23.45 51.89 46.25 1,010
|     | LoCoMo    |     | 28.00 | 18.47 | 9.09 | 5.78 | 16.47 | 14.80 | 61.56 | 54.19 | 16,910 |
| --- | --------- | --- | ----- | ----- | ---- | ---- | ----- | ----- | ----- | ----- | ------ |
|     | ReadAgent |     | 14.61 | 9.95  | 4.16 | 3.19 | 8.84  | 8.37  | 12.46 | 10.29 | 805    |
o4-TPG MemoryBank 6.49 4.69 2.47 2.43 6.43 5.30 8.28 7.10 569
MemGPT 30.36 22.83 17.29 13.18 12.24 11.87 60.16 53.35 16,987
|     | A-Mem |     | 32.86 | 23.76 | 39.41 | 31.23 | 17.10 | 15.84 | 48.43 | 42.97 | 1,216 |
| --- | ----- | --- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- |
MemoryOS† 40.23 31.89 43.57 33.55 20.58 15.85 43.85 39.03 2,000
HeLa-Mem 39.12 29.82 50.79 44.54 24.38 19.24 49.69 44.08 1,036
b41-5.2newQ A-Mem 22.09 15.28 27.19 22.05 13.49 10.74 33.75 30.04 1,300
|     | MEM0     |     | 31.73 | 24.82 | 28.96 | 26.24 | 15.03 | 11.28 | 42.58 | 35.15 | -      |
| --- | -------- | --- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ------ |
|     | MemoryOS |     |       |       | 32.24 | 27.86 | 20.27 | 15.94 | 46.33 | 41.62 | -      |
|     |          |     | 38.19 | 29.26 |       |       |       |       |       |       |        |
|     | LightMem |     | 25.45 | 19.61 | 32.03 | 27.70 | 15.81 | 11.81 | 34.92 | 31.22 | -      |
|     | HeLa-Mem |     | 36.59 | 27.02 | 36.08 | 29.91 | 24.22 | 20.23 | 49.95 | 45.15 | 944    |
|     | LoCoMo   |     | 4.61  | 4.29  | 3.11  | 2.71  | 4.55  | 5.97  | 7.03  | 5.69  | 16,910 |
b3-5.2newQ ReadAgent 2.47 1.78 3.01 3.01 5.57 5.22 3.25 2.51 776
|     | MemoryBank |     | 3.60  | 3.39  | 1.72  | 1.97  | 6.63  | 6.58  | 4.11  | 3.32  | 298    |
| --- | ---------- | --- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ------ |
|     | MemGPT     |     | 5.07  | 4.31  | 2.94  | 2.95  | 7.04  | 7.10  | 7.26  | 5.52  | 16,961 |
|     | A-Mem      |     | 18.23 | 11.94 | 24.32 | 19.74 | 16.48 | 14.31 | 23.63 | 19.23 | 1,300  |
MemoryOS† 19.20 14.84 20.85 16.05 13.57 10.86 25.65 18.78 2,000
HeLa-Mem 20.12 14.59 24.79 21.35 12.24 10.24 29.51 25.91 1,072
Table 2: Averaged results across three backbone orynodes,whereedgethicknessreflectstheassoci-
| LLMs (GPT-4o-mini, |     | GPT-4o, |     | Qwen2.5-3b). | Avg |     |     |     |     |     |     |
| ------------------ | --- | ------- | --- | ------------ | --- | --- | --- | --- | --- | --- | --- |
ationstrengthaccumulatedthroughco-activation
Rankiscomputedacrossallcategorieslowerisbetter
|     |     |     |     |     |     | duringretrieval. |     | Nodeappearanceencodesthelife- |     |     |     |
| --- | --- | --- | --- | --- | --- | ---------------- | --- | ----------------------------- | --- | --- | --- |
( † Reproducedresults).
cyclestatusassignedbytheReflectiveAgent:
|        |           |          |     |      |            |     | HubNodes(Red,Solid). |     |     | Tennodesexhibitde- |     |
| ------ | --------- | -------- | --- | ---- | ---------- | --- | -------------------- | --- | --- | ------------------ | --- |
| Method | Multi-hop | Temporal |     | Open | Single Avg |     |                      |     |     |                    |     |
F1 BL F1 BL F1 BL F1 BL Rank gree 10,indicatingdenseconnectivitywithinthe
≥
LoCoMo 19.21 14.17 10.20 7.75 11.02 10.64 36.32 29.64 5.00 graph. These nodes tend to occupy central posi-
| ReadAgent | 8.74 6.07 | 6.59 | 5.02 6.57 | 6.24 | 8.46 6.82 6.38 |     |     |     |     |     |     |
| --------- | --------- | ---- | --------- | ---- | -------------- | --- | --- | --- | --- | --- | --- |
tions,astheyserveasanchorsconnectingmultiple
| MemoryBank | 5.03 4.28 | 4.62 | 3.80 6.21 | 5.94 | 6.33 5.19 6.88 |     |     |     |     |     |     |
| ---------- | --------- | ---- | --------- | ---- | -------------- | --- | --- | --- | --- | --- | --- |
MemGPT 20.69 14.95 15.25 11.86 9.48 8.80 36.15 31.07 4.50 conversationthreads. TheReflectiveAgentidenti-
| A-Mem     | 26.04 18.60 | 36.53 | 29.21 15.24 | 14.05 38.90 | 33.09 3.00 |      |                  |     |       |             |         |
| --------- | ----------- | ----- | ----------- | ----------- | ---------- | ---- | ---------------- | --- | ----- | ----------- | ------- |
|           |             |       |             |             |            | fies | such high-degree |     | nodes | and applies | Hebbian |
| MemoryOS† | 32.61 25.42 | 35.33 | 28.53 19.30 | 14.63 38.45 | 32.84 2.25 |      |                  |     |       |             |         |
Distillationtoconsolidatetheirassociatedepisodic
| HeLa-Mem | 33.13 25.22 | 40.96 | 35.72 22.11 | 17.64 43.70 | 38.75 1.25 |                                    |     |     |     |     |              |
| -------- | ----------- | ----- | ----------- | ----------- | ---------- | ---------------------------------- | --- | --- | --- | --- | ------------ |
|          |             |       |             |             |            | clustersintostablesemanticentries. |     |     |     |     | Forinstance, |
Table3: AblationstudyonLoCoMobenchmark. Re- thenodewithdegree17inFigure4linksseveral
sultsshowF1/BLEU-1scores(%). temporallydisperseddiscussions,makingitanatu-
ralcandidateforknowledgeextraction.
Avg
Variant Multi-hop Temporal Open Single F1 Isolated Nodes (Gray, Dashed). Four nodes
|     | F1  | BL  | F1 BL | F1 BL | F1 BL |                |     |                           |     |     |     |
| --- | --- | --- | ----- | ----- | ----- | -------------- | --- | ------------------------- | --- | --- | --- |
|     |     |     |       |       |       | exhibitdegree< |     | 4andshownorecentaccessac- |     |     |     |
HeLa-Mem(Full) 36.04 26.56 46.23 40.48 29.50 23.55 45.04 39.80 34.74 tivity. Theirperipheralpositionsandweakintegra-
| w/oForgetting | 36.71 | 27.95 46.50 | 40.91 | 30.58 24.45 | 45.24 40.01 34.28 |     |     |     |     |     |     |
| ------------- | ----- | ----------- | ----- | ----------- | ----------------- | --- | --- | --- | --- | --- | --- |
tionsuggestlimitedrelevancetotheongoingnar-
| w/oSpreadingActivation | 33.88 | 25.57 44.36 | 39.62 | 27.76 22.28 | 43.34 38.33 32.19 |     |     |     |     |     |     |
| ---------------------- | ----- | ----------- | ----- | ----------- | ----------------- | --- | --- | --- | --- | --- | --- |
w/oReflectiveAgent 30.17 22.38 42.19 36.92 24.51 19.83 40.46 34.07 29.87 rative. TheAdaptiveForgettingmechanismflags
thesenodesforremoval,therebycontrollinggraph
growthandreducingretrievalnoiseoverextended
| 4.4 ReflectiveAgent: |     |     | MemoryLifecycle |     |     |                |     |     |           |      |              |
| -------------------- | --- | --- | --------------- | --- | --- | -------------- | --- | --- | --------- | ---- | ------------ |
|                      |     |     |                 |     |     | conversations. |     | The | remaining | nine | nodes (blue) |
Management
havemoderateconnectivityandareretainedinthe
episodicstore.
| Figure 4 | illustrates | the | structure | of the | Hebbian |     |     |     |     |     |     |
| -------- | ----------- | --- | --------- | ------ | ------- | --- | --- | --- | --- | --- | --- |
memorygraphafterencodingamulti-sessioncon- ThisvisualizationconfirmsthatHebbianlearn-
versation. Thegraphcomprises23episodicmem- ingenablesautomatedlifecyclemanagementwith-
13763

Memory History Dual-Path Retrieval
HeLa-Mem (Dual-Path) Results
Co-activation
1 Co-activations
n o (+Δw) accumulate weight [Turn 89] [Turn 15]
isse
S Turn 89 Turn 15 semantic Dr. Sarah Met Dr. Sarah at the HeLa-Mem
enc t o o u p r u a r g s e u d e me Learned ado c p o t n io fe n r e s n u c p e p . ort C a o n r s r w e e c r tl s y
counseling as a Association location.
Co-activation career. (Weight:0.52) Total:
9 3 0.71
n o isse (+Δw)
Wh
Q
er
u
e
e
d
r
id
y
you
Score: 0.82 Si ( m Lo :0 w .3 ) 5 He 0 b . b 36 ian: (High)
S first meet the Baseline (Similarity Only)
person who
influenced your [Turn 89] [Turn 15]
Co-activation Career?
1 6 Dr. Sarah encouraged Baseline
n o isse
S
(+Δw)
semantic
c m ou e n
c
t s
a
o e
r
l p
e
in
e
u g
r
r
.
s a u s e a (Sco N r o e t : R 0. e 3 t 5 r i < e v T e o d p-k)
a
F
n
a
s
il
w
s
e
t
r
o
.
Figure5:Dual-PathRetrievalformulti-hopreasoning.Givenaqueryrequiringboth“careerinfluence”and“meeting
location,”thesemanticpathretrievesTurn89(careercontext). TheHebbianpaththenpropagatesactivationthrough
learnedassociations(edgeweight0.52)toretrieveTurn15(locationcontext), whichsemanticsimilarityalone
wouldmiss. ThebaselinewithoutSpreadingActivationcannotbridgethesememories.
out manual annotation (see Appendix B for the callyupdated:
edge-weightheatmap).
S = 0.35 + 0.36 0.71 (6)
total
≈
Semantic Hebbian
4.5 CaseStudy: TraceAnalysisofAssociative
Recall
This score boost, d|{ezri}ved st|r{izc}tly from historical
association,promotesTurn15intotheactivecon-
We analyze the retrieval process for a multi-hop
text. By retrieving both the cue (Person) and the
query: “Where did you first meet the person who
target(Location),HeLa-Memcorrectlysynthesizes
influencedyourcareerchoice?” (seeFigure5). theanswer: “Attheadoptionsupportconference.”
Historical Context. The entities “Dr. Sarah” ThisdemonstrateshowHebbianassociationscom-
(Person)and“AdoptionSupportConference”(Lo- plementsemanticretrievalforcomplexreasoning.
cation) appeared together in Session 1, and were
subsequently co-activated in Sessions 39 and 5 Conclusion
61. Through Hebbian learning, these repeated
WeintroduceHeLa-Mem,abio-inspiredmemory
co-occurrences accumulated a strong associative
architecturethatmodelsconversationhistoryasa
weightofw 0.52betweenthecareeradvice
89,15 dynamicgraphdrivenbyHebbianlearningprinci-
≈
memory(Turn89)andthemeetingevent(Turn15).
ples. Unlike static context windows, HeLa-Mem
Thisaccumulatedweightreflectsthefrequencyand
mimicsthebrain’splasticity,where“neuronsthat
recency of co-activation across the conversation
fire together, wire together,” enabling the sponta-
history.
neous emergence of associative pathways for re-
ExperimentalTrace. Thebaselinemethodiden- trieval. Building on this foundation, our Reflec-
tifies Turn 89 (“Dr. Sarah encouraged...”) as the tiveAgentdistillstransientepisodesintostructured
topcandidateduetohighsemanticsimilarity(0.82) semantic knowledge, while Adaptive Forgetting
butfailstoretrieveTurn15(“MetDr. Sarahat...”) ensureslong-termscalability. Experimentsonthe
becauseitslowsimilarityscoreof0.35fallsbelow LoCoMobenchmarkdemonstratethatthissynergy
theretrievalthreshold. Thisresultsina“semantic betweenassociativeretentionandsemanticconsol-
trap” where the model knows the person but not idationyieldssuperiorperformanceacrossdiverse
thelocation. questiontypesandrobustnessacrossdiverseLLM
Incontrast,HeLa-MemutilizestheHebbianpath. backbones. Thesefindingssuggestthatincorporat-
Spreading activation from the retrieved Turn 89 ing neuro-symbolic dynamics offers a promising
propagatesthroughthelearnededge(0.52)toTurn direction for evolving static LLMs into lifelong
15. ThefinalretrievalscoreforTurn15isdynami- learningagents.
13764

| 6 Limitations |     |     |     |     | andefficientmemory-augmentedgeneration. |     |     |     |     |     | arXiv |
| ------------- | --- | --- | --- | --- | --------------------------------------- | --- | --- | --- | --- | --- | ----- |
preprintarXiv:2510.18866.
| While HeLa-Mem |     | effectively | models | long-term |               |       |       |     |                  |     |        |
| -------------- | --- | ----------- | ------ | --------- | ------------- | ----- | ----- | --- | ---------------- | --- | ------ |
|                |     |             |        |           | Donald Olding | Hebb. | 2005. |     | The organization |     | of be- |
memoryconsolidation,itfacesa“coldstart”chal-
|     |     |     |     |     | havior: | A neuropsychological |     |     | theory. | Psychology |     |
| --- | --- | --- | --- | --- | ------- | -------------------- | --- | --- | ------- | ---------- | --- |
lenge: Hebbianweightsrequiresufficientinterac-
press.
tionhistorytoaccumulate,meaningthebenefitsof
|             |           |          |            |          | John J Hopfield. |     | 1982. | Neural | networks |     | and physi- |
| ----------- | --------- | -------- | ---------- | -------- | ---------------- | --- | ----- | ------ | -------- | --- | ---------- |
| associative | retrieval | are less | pronounced | in early |                  |     |       |        |          |     |            |
calsystemswithemergentcollectivecomputational
| conversationstages. |     | Futureworkmayexploreini- |     |     |            |             |     |        |          |         |     |
| ------------------- | --- | ------------------------ | --- | --- | ---------- | ----------- | --- | ------ | -------- | ------- | --- |
|                     |     |                          |     |     | abilities. | Proceedings |     | of the | National | Academy | of  |
tializingHebbianedgesusingsemanticsimilarity
Sciences,79(8):2554–2558.
asaprior,allowingthegraphstructuretobootstrap
YuyangHu,ShichunLiu,YanweiYue,GuibinZhang,
| beforesufficientco-occurrencesaccumulate. |     |     |     | Addi- |     |     |     |     |     |     |     |
| ----------------------------------------- | --- | --- | --- | ----- | --- | --- | --- | --- | --- | --- | --- |
BoyangLiu,FangyiZhu,JiahangLin,HonglinGuo,
tionally,thequalityofbothSemanticMemoryand
ShihanDou,ZhihengXi,SenjieJin,JiejunTan,Yan-
HubDetectionreliesonthecapabilitiesoftheun-
|     |     |     |     |     | bin Yin, | Jiongnan | Liu, | Zeyu | Zhang, | Zhongxiang |     |
| --- | --- | --- | --- | --- | -------- | -------- | ---- | ---- | ------ | ---------- | --- |
derlyingLLM;hallucinationsorreasoningerrors Sun,YutaoZhu,HaoSun,BociPeng,and28others.
|     |     |     |     |     | 2025. | Memoryintheageofaiagents. |     |     |     | arXivpreprint |     |
| --- | --- | --- | --- | --- | ----- | ------------------------- | --- | --- | --- | ------------- | --- |
duringthedistillationprocesscouldpropagateinto
arXiv:2512.13564.
thelong-termstorage,potentiallyaffectingfuture
retrievalaccuracy. Le Huang, Hengzhi Lan, Zijun Sun, Chuan Shi, and
|     |     |     |     |     | Ting Bai. | 2024. | Emotional |     | rag: | Enhancing | role- |
| --- | --- | --- | --- | --- | --------- | ----- | --------- | --- | ---- | --------- | ----- |
7 EthicalConsiderations playingagentsthroughemotionalretrieval. In2024
IEEEInternationalConferenceonKnowledgeGraph
WeusethepubliclyavailableLoCoMobenchmark (ICKG),pages120–127.IEEE.
| anddonotcollectanyprivateuserdata. |     |     |     | Thepro- |          |       |          |     |     |       |          |
| ---------------------------------- | --- | --- | --- | ------- | -------- | ----- | -------- | --- | --- | ----- | -------- |
|                                    |     |     |     |         | Jiazheng | Kang, | Mingming | Ji, | Zhe | Zhao, | and Ting |
posedmemoryarchitectureisintendedtoenhance Bai.2025. Memoryosofaiagent. arXivpreprint
| theconsistencyofLLMagents. |     |     | However, | weac- | arXiv:2506.06326. |     |     |     |     |     |     |
| -------------------------- | --- | --- | -------- | ----- | ----------------- | --- | --- | --- | --- | --- | --- |
knowledgethatlong-termmemorysystemscould
|     |     |     |     |     | Kuang-Huei | Lee, | Xinyun | Chen, | Hiroki | Furuta, | John |
| --- | --- | --- | --- | --- | ---------- | ---- | ------ | ----- | ------ | ------- | ---- |
potentiallyreinforcebiasespresentintheunderly-
|                                |     |     |     |              | Canny, | and Ian | Fischer. | 2024. | A   | human-inspired |     |
| ------------------------------ | --- | --- | --- | ------------ | ------ | ------- | -------- | ----- | --- | -------------- | --- |
| ingLLMifnotcarefullymonitored. |     |     |     | Thedistilled |        |         |          |       |     |                |     |
readingagentwithgistmemoryofverylongcontexts.
semanticmemoriesshouldbetreatedwiththesame arXivpreprintarXiv:2402.09727.
cautionasstandardLLMgenerationsregardingac-
PatrickLewis,EthanPerez,AleksandraPiktus,Fabio
| curacyandbias. |     |     |     |     | Petroni,VladimirKarpukhin,NamanGoyal,Hein- |            |     |             |     |     |          |
| -------------- | --- | --- | --- | --- | ------------------------------------------ | ---------- | --- | ----------- | --- | --- | -------- |
|                |     |     |     |     | richKüttler,                               | MikeLewis, |     | Wen-tauYih, |     |     | TimRock- |
Acknowledgments
|     |     |     |     |     | täschel,            | Sebastian | Riedel, |            | and Douwe | Kiela.         | 2020. |
| --- | --- | --- | --- | --- | ------------------- | --------- | ------- | ---------- | --------- | -------------- | ----- |
|     |     |     |     |     | Retrieval-augmented |           |         | generation |           | for knowledge- |       |
This work was partially supported by the Guang- intensivenlptasks. Advancesinneuralinformation
dongProvincialNaturalScienceFoundationGen- processingsystems,33:9459–9474.
| eralProgram(GrantNo. |     | 2026A1515012118). |     |     |     |     |     |     |     |     |     |
| -------------------- | --- | ----------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
JindongLi,YaliFu,JiahongLiu,LinxiaoCao,WeiJi,
MenglinYang,IrwinKing,andMing-HsuanYang.
|            |     |     |     |     | 2026.                | Discretetokenizationformultimodalllms: |     |                           |     |     | A   |
| ---------- | --- | --- | --- | --- | -------------------- | -------------------------------------- | --- | ------------------------- | --- | --- | --- |
| References |     |     |     |     | comprehensivesurvey. |                                        |     | IEEETransactionsonPattern |     |     |     |
AnalysisandMachineIntelligence,pages1–24.
JoshAchiam,StevenAdler,SandhiniAgarwal,Lama
Ahmad, Ilge Akkaya, Florencia Leoni Aleman, Jiafeng Liang, Hao Li, Chang Li, Jiaqi Zhou, Shixin
DiogoAlmeida,JankoAltenschmidt,SamAltman, Jiang, Zekun Wang, Changkai Ji, Zhihao Zhu,
Shyamal Anadkat, Red Avila, Igor Babuschkin, Runxuan Liu, Tao Ren, Jinlan Fu, See-Kiong Ng,
SuchirBalaji,ValerieBalcom,PaulBaltescu,Haim- Xia Liang, Ming Liu, and Bing Qin. 2025. Ai
ingBao,MohammadBavarian,JeffBelgum,Irwan
|     |     |     |     |     | meets | brain: | Memory | systems | from | cognitive | neu- |
| --- | --- | --- | --- | --- | ----- | ------ | ------ | ------- | ---- | --------- | ---- |
Bello,and260others.2023. GPT-4technicalreport. roscience to autonomous agents. arXiv preprint
| arXivpreprintarXiv:2303.08774. |     |     |     |     | arXiv:2512.23343. |     |     |     |     |     |     |
| ------------------------------ | --- | --- | --- | --- | ----------------- | --- | --- | --- | --- | --- | --- |
PrateekChhikara,DevKhant,SaketAryan,Taranjeet XinnianLiang,BingWang,HuijiaHuang,Shuangzhi
Singh,andDeshrajYadav.2025. Mem0: Building Wu,PeihaoWu,LuLu,ZejunMa,andZhoujunLi.
production-readyaiagentswithscalablelong-term 2023. Scm: Enhancinglargelanguagemodelwith
| memory. | arXivpreprintarXiv:2504.19413. |     |     |     |                                 |     |     |     |     |               |     |
| ------- | ------------------------------ | --- | --- | --- | ------------------------------- | --- | --- | --- | --- | ------------- | --- |
|         |                                |     |     |     | self-controlledmemoryframework. |     |     |     |     | arXivpreprint |     |
arXiv:2304.13343.
| Jizhan Fang, | Xinle | Deng, Haoming |     | Xu, Ziyan Jiang, |     |     |     |     |     |     |     |
| ------------ | ----- | ------------- | --- | ---------------- | --- | --- | --- | --- | --- | --- | --- |
Yuqi Tang, Ziwen Xu, Shumin Deng, Yunzhi Yao, JiahongLiu,ZexuanQiu,ZhongyangLi,QuanyuDai,
Mengru Wang, Shuofei Qiao, Huajun Chen, and WenhaoYu,JiemingZhu,MindaHu,MenglinYang,
Ningyu Zhang. 2025. LightMem: Lightweight Tat-SengChua,andIrwinKing.2025. Asurveyof
13765

personalized large language models: Progress and ZeyuZhang,QuanyuDai,XiaoheBo,ChenMa,RuiLi,
futuredirections. arXivpreprintarXiv:2502.11528. XuChen,JiemingZhu,ZhenhuaDong,andJi-Rong
|                                            |     |     |     | Wen.2025. Asurveyonthememorymechanismof |     |               |     |
| ------------------------------------------ | --- | --- | --- | --------------------------------------- | --- | ------------- | --- |
| JiahongLiu,WenhaoYu,QuanyuDai,ZhongyangLi, |     |     |     |                                         |     | ACMTrans.Inf. |     |
largelanguagemodel-basedagents.
JiemingZhu,MenglinYang,Tat-SengChua,andIr-
Syst.,43(6).
| win King.                          | 2026. Perfit: | Exploring | personalization |     |     |     |     |
| ---------------------------------- | ------------- | --------- | --------------- | --- | --- | --- | --- |
| shiftsinrepresentationspaceofLLMs. |               |           | InTheFour-      |     |     |     |     |
WanjunZhong,LianghongGuo,QiqiGao,HeYe,and
teenthInternationalConferenceonLearningRepre- YanlinWang.2024. Memorybank: Enhancinglarge
| sentations. |     |     |     | language models | with long-term | memory. | In Pro- |
| ----------- | --- | --- | --- | --------------- | -------------- | ------- | ------- |
ceedingsoftheAAAIConferenceonArtificialIntelli-
LeiLiu,XiaoyanYang,YueShen,BinbinHu,Zhiqiang gence,volume38,pages19724–19731.
| Zhang,JinjieGu,andGuannanZhang.2023. |                |                   | Think-         |     |     |     |     |
| ------------------------------------ | -------------- | ----------------- | -------------- | --- | --- | --- | --- |
| in-memory:                           | Recalling      | and post-thinking | enable         |     |     |     |     |
| LLMs                                 | with long-term | memory.           | arXiv preprint |     |     |     |     |
arXiv:2311.08719.
| Adyasha | Maharana, Dong-Ho | Lee, | Sergey Tulyakov, |     |     |     |     |
| ------- | ----------------- | ---- | ---------------- | --- | --- | --- | --- |
MohitBansal,FrancescoBarbieri,andYuweiFang.
| 2024.              | Evaluating | very long-term         | conversational |     |     |     |     |
| ------------------ | ---------- | ---------------------- | -------------- | --- | --- | --- | --- |
| memoryofLLMagents. |            | InProceedingsofthe62nd |                |     |     |     |     |
AnnualMeetingoftheAssociationforComputational
| Linguistics(Volume1: |     | LongPapers),pages13851– |     |     |     |     |     |
| -------------------- | --- | ----------------------- | --- | --- | --- | --- | --- |
13870,Bangkok,Thailand.AssociationforCompu-
tationalLinguistics.
| Charles Packer, | Vivian | Fang, Shishir_G | Patil, Kevin |     |     |     |     |
| --------------- | ------ | --------------- | ------------ | --- | --- | --- | --- |
Lin,SarahWooders,andJoseph_EGonzalez.2023.
MemGPT:TowardsLLMsasoperatingsystems.
JoonSungPark,JosephO’Brien,CarrieJunCai,Mered-
ithRingelMorris,PercyLiang,andMichaelSBern-
| stein.2023.      | Generativeagents: | Interactivesimulacra      |     |     |     |     |     |
| ---------------- | ----------------- | ------------------------- | --- | --- | --- | --- | --- |
| ofhumanbehavior. |                   | InProceedingsofthe36than- |     |     |     |     |     |
nualacmsymposiumonuserinterfacesoftwareand
technology,pages1–22.
HubertRamsauer,BernhardSchäfl,JohannesLehner,
| Philipp | Seidl, Michael | Widrich, | Thomas Adler, |     |     |     |     |
| ------- | -------------- | -------- | ------------- | --- | --- | --- | --- |
LukasGruber,MarkusHolzleitner,MilenaPavlovic´,
| Geir Kjetil | Sandve, | Victor Greiff, | David Kreil, |     |     |     |     |
| ----------- | ------- | -------------- | ------------ | --- | --- | --- | --- |
MichaelKopp,GünterKlambauer,JohannesBrand-
| stetter, | and Sepp   | Hochreiter. | 2020. Hopfield |     |     |     |     |
| -------- | ---------- | ----------- | -------------- | --- | --- | --- | --- |
| networks | is all you | need.       | arXiv preprint |     |     |     |     |
arXiv:2008.02217.
YaxiongWu,ShengLiang,ChenZhang,YichaoWang,
YongyueZhang,HuifengGuo,RuimingTang,and
| YongLiu.2025. | FromhumanmemorytoAImemory: |     |     |     |     |     |     |
| ------------- | -------------------------- | --- | --- | --- | --- | --- | --- |
AsurveyonmemorymechanismsintheeraofLLMs.
arXivpreprintarXiv:2504.15965.
| Wujiang  | Xu, Zujie Liang, | Kai Mei,    | Hang Gao, Jun- |     |     |     |     |
| -------- | ---------------- | ----------- | -------------- | --- | --- | --- | --- |
| tao Tan, | and Yongfeng     | Zhang.      | 2025. A-MEM:   |     |     |     |     |
| Agentic  | memory for       | LLM agents. | arXiv preprint |     |     |     |     |
arXiv:2502.12110.
| BY Yan,        | Chaofan Li,                    | Hongjin Qian, | Shuqi Lu, and |     |     |     |     |
| -------------- | ------------------------------ | ------------- | ------------- | --- | --- | --- | --- |
| ZhengLiu.2025. | Generalagenticmemoryviadeep    |               |               |     |     |     |     |
| research.      | arXivpreprintarXiv:2511.18423. |               |               |     |     |     |     |
AnYang,BaosongYang,BeichenZhang,BinyuanHui,
BoZheng,BowenYu,ChengyuanLi,DayihengLiu,
FeiHuang,HaoranWei,HuanLin,JianYang,Jian-
hongTu,JianweiZhang,JianxinYang,JiaxiYang,
| Jingren   | Zhou, Junyang           | Lin, Kai | Dang, and 22 oth- |     |     |     |     |
| --------- | ----------------------- | -------- | ----------------- | --- | --- | --- | --- |
| ers.2024. | Qwen2.5technicalreport. |          | arXivpreprint     |     |     |     |     |
arXiv:2412.15115.
13766

A LLMPrompts
ThisappendixprovidesthecoreLLMpromptsusedintheHeLa-Memsystem.
A.1 HebbianDistillation
TheReflectiveAgentusesthefollowingprompttoextractstructuredknowledgefrommemoryclusters
identifiedashubs.
Prompt1: SemanticMemoryExtractionPrompt
System: You are a knowledge extraction engine analyzing conversation memories.
1
Extract ONLY factual information with direct evidence.
2
Output concise, structured entries.
3
4
User: Analyze the following memory cluster and extract:
5
6
1. USER CHARACTERISTICS:
7
- Observable traits (with evidence)
8
- Content preferences (with evidence)
9
- Interaction patterns
10
11
2. FACTUAL INFORMATION:
12
- Events with dates and locations
13
- Stated preferences
14
- Mentioned relationships
15
16
Format: Concise bullet points with supporting evidence.
17
18
Memory Cluster: {conversation}
19
A.2 ResponseGeneration
The system uses the following prompt to generate responses using retrieved episodic and semantic
memories.
Prompt2: ResponseGenerationPrompt
System: You are an AI assistant with access to conversation history.
1
Answer questions concisely using the provided context.
2
For dates, use format "15 July 2023".
3
4
User:
5
<EPISODIC MEMORIES>
6
{episodic_context}
7
8
<SEMANTIC KNOWLEDGE>
9
{semantic_knowledge}
10
11
<USER CHARACTERISTICS>
12
{user_model}
13
14
Question: {query}
15
16
Provide an extremely concise answer using concrete entities.
17
Output only the answer content, without labels.
18
13767

|     |     |     |     |     |     |     |     | Table4: | LoCoModatasetoverview. |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ------- | ---------------------- | --- | --- | --- | --- |
B HebbianWeightVisualization
| Figure   | 6 shows   | the Hebbian |     | edge   | weight   | ma- |                       |     |     |     |     |       |     |
| -------- | --------- | ----------- | --- | ------ | -------- | --- | --------------------- | --- | --- | --- | --- | ----- | --- |
|          |           |             |     |        |          |     | Metric                |     |     |     |     | Value |     |
| trix for | the first | 20 memory   |     | nodes. | Stronger |     |                       |     |     |     |     |       |     |
|          |           |             |     |        |          |     | NumberofConversations |     |     |     |     | 10    |     |
weights (darker colors) indicate associations Avg.TurnsperConversation 300
∼
formedthroughco-activation. Thematrixexhibits Avg.TokensperConversation 9,000
∼
|     |     |     |     |     |     |     | TotalQuestion-AnswerPairs |     |     |     |     | 1,986 |     |
| --- | --- | --- | --- | --- | --- | --- | ------------------------- | --- | --- | --- | --- | ----- | --- |
bothlocalassociationsnearthediagonalandcross-
| topic connections |              | between         | distant | nodes,     |          | demon- |                                                    |     |     |     |     |     |     |
| ----------------- | ------------ | --------------- | ------- | ---------- | -------- | ------ | -------------------------------------------------- | --- | --- | --- | --- | --- | --- |
| strating          | that Hebbian | learning        |         | captures   | semantic |        |                                                    |     |     |     |     |     |     |
|                   |              |                 |         |            |          |        | Table5: Distributionofquestiontypesintheevaluation |     |     |     |     |     |     |
| relationships     |              | beyond temporal |         | adjacency. |          | Nodes  |                                                    |     |     |     |     |     |     |
set.
withredbordershavehightotalconnectivity,mak-
ingthemcandidatesforHebbianDistillation. Category Count Percentage
|     |     |                            |     |     |     |     | Single-hop |     |     | 841 |     | 42.3% |     |
| --- | --- | -------------------------- | --- | --- | --- | --- | ---------- | --- | --- | --- | --- | ----- | --- |
|     |     | Hebbian Edge Weight Matrix |     |     |     |     | Multi-hop  |     |     | 282 |     | 14.2% |     |
Higher weights indicate stronger memory associations
|             |     |     |     |     |                       |     | Temporal |     |     | 321 |     | 16.2% |     |
| ----------- | --- | --- | --- | --- | --------------------- | --- | -------- | --- | --- | --- | --- | ----- | --- |
| M11.00 0.38 |     |     |     |     | Red border: Hub nodes |     |          |     |     |     |     |       |     |
M20.38 1.00 0.53 0.55 (high connectivity) Open-domain 96 4.8%
0.6
| M3 0.53 | 1.00 0.38      | 0.77           | 0.45 |      |      |     | Adversarial |     |     | 446   |     | 22.5%  |     |
| ------- | -------------- | -------------- | ---- | ---- | ---- | --- | ----------- | --- | --- | ----- | --- | ------ | --- |
| M4      | 0.38 1.00 0.32 |                |      | 0.50 |      |     |             |     |     |       |     |        |     |
| M5      | 0.32 1.00      | 0.33           |      |      |      | 0.5 | Total       |     |     | 1,986 |     | 100.0% |     |
| M6      | 0.33           | 1.00 0.31      |      |      | 0.48 |     |             |     |     |       |     |        |     |
| M7      |                | 0.31 1.00 0.40 |      |      |      |     |             |     |     |       |     |        |     |
0.4
| M8       | 0.77 | 0.40 1.00 0.32 |           |     |     | Hebbian Edge Weight |             |           |     |           |       |              |       |
| -------- | ---- | -------------- | --------- | --- | --- | ------------------- | ----------- | --------- | --- | --------- | ----- | ------------ | ----- |
| M9       |      | 0.32 1.00 0.34 |           |     |     |                     |             |           |     |           |       |              |       |
|          |      |                |           |     |     |                     | β = 0.1,    | spreading |     | threshold | θ =   | 0.4, keyword |       |
| M10      |      | 0.34 1.00 0.32 |           |     |     |                     |             |           |     |           |       |              |       |
| M11 0.55 |      | 0.32 1.00      | 0.32      |     |     | 0.3                 |             |           |     |           |       |              |       |
|          |      |                |           |     |     |                     | weight 0.7, | and       | max | flipped   | items | m =          | 3. In |
| M12      |      | 0.32           | 1.00 0.37 |     |     |                     |             |           |     |           |       |              |       |
M13 0.37 1.00 0.34 0.2 Table 7, Single denotes the merged single-hop
| M14 | 0.45 |     | 0.34 1.00 0.36 |                |     |     |                 |                                |              |     |              |     |     |
| --- | ---- | --- | -------------- | -------------- | --- | --- | --------------- | ------------------------------ | ------------ | --- | ------------ | --- | --- |
|     |      |     |                |                |     |     | group combining |                                | Single-User, |     | Single-Asst, |     | and |
| M15 |      |     | 0.36 1.00      | 0.32           |     |     |                 |                                |              |     |              |     |     |
| M16 | 0.50 |     | 0.32           | 1.00 0.33      |     | 0.1 |                 |                                |              |     |              |     |     |
|     |      |     |                |                |     |     | Single-Pref.    | Baselinenumbersarereportedfrom |              |     |              |     |     |
| M17 |      |     |                | 0.33 1.00 0.32 |     |     |                 |                                |              |     |              |     |     |
M18 0.32 1.00 0.34 0.0 Fang et al. (2025) under the same total retrieval
| M19   |          | 0.48                                         |     | 0.34 | 1.00 0.32 |     |         |     |     |     |     |     |     |
| ----- | -------- | -------------------------------------------- | --- | ---- | --------- | --- | ------- | --- | --- | --- | --- | --- | --- |
| M20   |          |                                              |     |      | 0.32 1.00 |     | budget. |     |     |     |     |     |     |
| M1 M2 | M3 M4 M5 | M6 M7 M8 M9M10M11M12M13M14M15M16M17M18M19M20 |     |      |           |     |         |     |     |     |     |     |     |
Figure6: Hebbianedgeweightmatrixforthefirst20 Table6: OverallaccuracyonLongMemEval-S.
| memory      | nodes.    | Stronger           | weights | (darker | colors)  | in- |         |     |     |     |     |        |     |
| ----------- | --------- | ------------------ | ------- | ------- | -------- | --- | ------- | --- | --- | --- | --- | ------ | --- |
| dicate more | frequent  | co-activation.     |         | Nodes   | with     | red |         |     |     |     |     |        |     |
|             |           |                    |         |         |          |     | Method  |     |     |     |     | ACC(%) |     |
| borders     | have high | total connectivity |         | across  | multiple |     |         |     |     |     |     |        |     |
|             |           |                    |         |         |          |     | LangMem |     |     |     |     | 37.20  |     |
memories.
|     |     |     |     |     |     |     | MemoryOS |     |     |     |     | 44.80 |     |
| --- | --- | --- | --- | --- | --- | --- | -------- | --- | --- | --- | --- | ----- | --- |
|     |     |     |     |     |     |     | Mem0     |     |     |     |     | 53.61 |     |
|     |     |     |     |     |     |     | FullText |     |     |     |     | 56.80 |     |
|     |     |     |     |     |     |     | NaiveRAG |     |     |     |     | 61.00 |     |
C DatasetStatistics
|                  |     |              |            |        |          |        | A-MEM    |     |     |     |     | 62.60 |     |
| ---------------- | --- | ------------ | ---------- | ------ | -------- | ------ | -------- | --- | --- | --- | --- | ----- | --- |
|                  |     |              |            |        |          |        | HeLa-Mem |     |     |     |     | 65.40 |     |
| We utilize       | the | LoCoMo       | benchmark, |        | focusing | on     |          |     |     |     |     |       |     |
| the long-context |     | conversation |            | split. | Table    | 4 pro- |          |     |     |     |     |       |     |
videsthedetailedstatisticsofthe10conversations
|     |     |     |     |     |     |     | Table7: | Category-wiseaccuracyonLongMemEval-S. |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ------- | ------------------------------------- | --- | --- | --- | --- | --- |
usedinourexperiments,whileTable5detailsthe
distributionacrossdifferentquestioncategories.
|     |     |     |     |     |     |     |        |          |     | Multi-  | Knowledge- |     |        |
| --- | --- | --- | --- | --- | --- | --- | ------ | -------- | --- | ------- | ---------- | --- | ------ |
|     |     |     |     |     |     |     | Method | Temporal |     |         |            |     | Single |
|     |     |     |     |     |     |     |        |          |     | Session | Update     |     |        |
D AdditionalBenchmark:
|               |     |     |     |     |     |     | LangMem  |     | 15.79 | 20.30 | 66.67 |     | 55.13 |
| ------------- | --- | --- | --- | --- | --- | --- | -------- | --- | ----- | ----- | ----- | --- | ----- |
| LongMemEval-S |     |     |     |     |     |     | MemoryOS |     | 32.33 | 31.06 | 48.72 |     | 64.74 |
|               |     |     |     |     |     |     | Mem0     |     | 40.15 | 46.21 | 70.12 |     | 62.82 |
We additionally evaluate HeLa-Mem on FullText 31.58 45.45 76.92 78.21
|     |     |     |     |     |     |     | NaiveRAG |     | 39.85 | 48.48 | 67.95 |     | 85.90 |
| --- | --- | --- | --- | --- | --- | --- | -------- | --- | ----- | ----- | ----- | --- | ----- |
LongMemEval-S, a 500-item long-term con- A-MEM 47.36 48.87 64.11 84.62
|             |        |         |              |     |       |     | HeLa-Mem |     | 50.38 | 57.14 | 78.21 |     | 78.85 |
| ----------- | ------ | ------- | ------------ | --- | ----- | --- | -------- | --- | ----- | ----- | ----- | --- | ----- |
| versational | memory |         | benchmark.   |     | We    | use |          |     |       |       |       |     |       |
| GPT-4o-mini |        | as both | the backbone |     | model | and |          |     |       |       |       |     |       |
the LLM judge. For retrieval, HeLa-Mem uses Thecategory-wisevaluesarenotdirectlyaveraged
top-15 episodic memories and top-5 semantic to obtain the overall ACC because the category
sizesareunequal.
| memories | (20 | total). | The best | setting |     | on this |     |     |     |     |     |     |     |
| -------- | --- | ------- | -------- | ------- | --- | ------- | --- | --- | --- | --- | --- | --- | --- |
benchmark uses learning rate η = 0.02, decay HeLa-Mem achieves the best overall accuracy
rate λ = 0.995, spreading activation strength and the best performance on the three reasoning-
13768

| intensivecategories: |     | Temporal,Multi-Session,and |     |     |     |
| -------------------- | --- | -------------------------- | --- | --- | --- |
Knowledge-Update.
E LLMUsageStatement
| We use                           | publicly | available         | large    | language       | model |
| -------------------------------- | -------- | ----------------- | -------- | -------------- | ----- |
| tools as                         | writing  | assistants        | to check | grammar        | and   |
| polishasmallnumberofsentences.   |          |                   |          | Alltechnical   |       |
| content,                         | claims,  | and contributions |          | are conceived, |       |
| written,andverifiedbytheauthors. |          |                   |          | Forschematic   |       |
figures,severaliconsorvisualelementsarerefined
| with the   | assistance       | of      | LLM-based  | design       | tools,    |
| ---------- | ---------------- | ------- | ---------- | ------------ | --------- |
| while the  | figure           | layout, | semantics, | and          | interpre- |
| tation are | fully determined |         | by         | the authors. | Since     |
thispaperinvolvesLLM-relatedresearch,allmodel
usagethataffectsexperiments,analysis,orresults
| is explicitly | documented |     | in Section | Experiments. |     |
| ------------- | ---------- | --- | ---------- | ------------ | --- |
Nootherpartsofthemanuscriptaregeneratedor
substantivelyrewrittenbyanLLM.
13769