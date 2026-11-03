5202
naJ
02
]LC.sc[
1v65931.1052:viXra
ZEP: A TEMPORAL KNOWLEDGE GRAPH ARCHITECTURE FOR
AGENT MEMORY
PrestonRasmussen PavloPaliychuk TravisBeauvais JackRyan
ZepAI ZepAI ZepAI ZepAI
preston@getzep.com paul@getzep.com travis@getzep.com jack@getzep.com
DanielChalef
ZepAI
daniel@getzep.com
ABSTRACT
We introduceZep, a novelmemory layer service for AI agents that outperformsthe currentstate-
of-the-artsystem,MemGPT,intheDeepMemoryRetrieval(DMR)benchmark. Additionally,Zep
excelsinmorecomprehensiveandchallengingevaluationsthanDMRthatbetterreflectreal-world
enterprise use cases. While existing retrieval-augmentedgeneration (RAG) frameworks for large
languagemodel(LLM)-basedagentsarelimitedtostaticdocumentretrieval,enterpriseapplications
demanddynamicknowledgeintegrationfromdiversesourcesincludingongoingconversationsand
business data. Zep addresses this fundamentallimitation through its core componentGraphiti—a
temporally-awareknowledgegraph enginethat dynamicallysynthesizesboth unstructuredconver-
sational data and structured business data while maintaininghistorical relationships. In the DMR
benchmark,which the MemGPT team established as their primaryevaluationmetric, Zep demon-
strates superiorperformance(94.8%vs 93.4%). BeyondDMR, Zep’s capabilitiesare furthervali-
datedthroughthemorechallengingLongMemEvalbenchmark,whichbetterreflectsenterpriseuse
casesthroughcomplextemporalreasoningtasks. Inthisevaluation,Zepachievessubstantialresults
with accuracy improvements of up to 18.5% while simultaneously reducing response latency by
90%comparedtobaselineimplementations.Theseresultsareparticularlypronouncedinenterprise-
criticaltaskssuchascross-sessioninformationsynthesisandlong-termcontextmaintenance,demon-
stratingZep’seffectivenessfordeploymentinreal-worldapplications.
1 Introduction
Theimpactoftransformer-basedlargelanguagemodels(LLMs)onindustryandresearchcommunitieshasgarnered
significantattentioninrecentyears[1]. AmajorapplicationofLLMshasbeenthedevelopmentofchat-basedagents.
However, these agents’ capabilities are limited by the LLMs’ context windows, effective context utilization, and
knowledgegainedduringpre-training. Consequently,additionalcontextisrequiredtoprovideout-of-domain(OOD)
knowledgeandreducehallucinations.
Retrieval-Augmented Generation (RAG) has emerged as a key area of interest in LLM-based applications. RAG
leverages Information Retrieval (IR) techniques pioneered over the last fifty years[2] to supply necessary domain
knowledgetoLLMs.
Currentapproachesusing RAG have focusedon broaddomainknowledgeand largelystatic corpora—thatis, docu-
ment contents added to a corpus seldom change. For agents to become pervasive in our daily lives, autonomously
solvingproblemsfromtrivialtohighlycomplex,theywillneedaccesstoalargecorpusofcontinuouslyevolvingdata
fromusers’interactionswiththeagent,alongwithrelatedbusinessandworlddata. Weviewempoweringagentswith
thisbroadanddynamic"memory"asacrucialbuildingblocktoactualizethisvision,andwearguethatcurrentRAG
approaches are unsuitable for this future. Since entire conversation histories, business datasets, and other domain-
specific contentcannotfiteffectivelyinsideLLMcontextwindows,new approachesneedto bedevelopedforagent

UsingKnowledgeGraphstopowerLLM-AgentMemory
memory. Adding memory to LLM-poweredagents isn’t a new idea—this concepthas been explored previouslyin
MemGPT[3].
Recently,KnowledgeGraphs(KGs)havebeenemployedtoenhanceRAGarchitecturestoaddressmanyoftheshort-
comings of traditional IR techniques[4]. In this paper, we introduce Zep[5], a memory layer service powered by
Graphiti[6], a dynamic, temporally-aware knowledge graph engine. Zep ingests and synthesizes both unstructured
messagedataandstructuredbusinessdata. TheGraphitiKGenginedynamicallyupdatestheknowledgegraphwith
newinformationin a non-lossymanner,maintaininga timeline offactsandrelationships, includingtheirperiodsof
validity.Thisapproachenablestheknowledgegraphtorepresentacomplex,evolvingworld.
AsZepisaproductionsystem,we’vefocusedheavilyontheaccuracy,latency,andscalabilityofitsmemoryretrieval
mechanisms.Weevaluatethesemechanisms’efficacyusingtwoexistingbenchmarks:aDeepMemoryRetrievaltask
(DMR)fromMemGPT[3],aswellastheLongMemEvalbenchmark[7].
2 KnowledgeGraph Construction
In Zep, memoryis poweredby a temporally-awaredynamicknowledgegraph G = (N,E,φ), where N represents
nodes,E representsedges,andφ : E → N ×N representsaformalincidencefunction. Thisgraphcomprisesthree
hierarchicaltiersofsubgraphs:anepisodesubgraph,asemanticentitysubgraph,andacommunitysubgraph.
• Episode Subgraph Ge: Episodic nodes (episodes), ni ∈ Ne, contain raw input data in the form of mes-
sages,text,orJSON.Episodesserveasanon-lossydatastorefromwhichsemanticentitiesandrelationsare
extracted.Episodicedges,ei ∈Ee ⊆φ∗ (Ne×Ns),connectepisodestotheirreferencedsemanticentities.
• Semantic Entity Subgraph Gs: The semantic entity subgraph builds upon the episode subgraph. Entity
nodes(entities),ni ∈Ns,represententitiesextractedfromepisodesandresolvedwithexistinggraphentities.
Entityedges(semanticedges),ei ∈ Es ⊆ φ∗ (Ns ×Ns), representrelationshipsbetweenentitiesextracted
fromepisodes.
• Community Subgraph Gc: The community subgraph forms the highest level of Zep’s knowledge graph.
Communitynodes(communities),ni ∈ Nc,representclustersofstronglyconnectedentities. Communities
containhigh-levelsummarizationsoftheseclustersandrepresentamorecomprehensive,interconnectedview
ofGs’sstructure.Communityedges,ei ∈Ec ⊆φ∗ (Nc×Ns),connectcommunitiestotheirentitymembers.
Thedualstorageofbothrawepisodicdataandderivedsemanticentityinformationmirrorspsychologicalmodelsof
humanmemory. Thesemodelsdistinguishbetweenepisodicmemory,whichrepresentsdistinctevents,andsemantic
memory,whichcapturesassociationsbetweenconceptsandtheirmeanings[8]. ThisapproachenablesLLMagents
usingZeptodevelopmoresophisticatedandnuancedmemorystructuresthatbetteralignwithourunderstandingof
humanmemorysystems. Knowledgegraphsprovideaneffectivemediumforrepresentingthesememorystructures,
andourimplementationofdistinctepisodicandsemanticsubgraphsdrawsfromsimilarapproachesinAriGraph[9].
Ouruseofcommunitynodestorepresenthigh-levelstructuresanddomainconceptsbuildsuponworkfromGraphRAG
[4], enabling a more comprehensive global understanding of the domain. The resulting hierarchical organiza-
tion—fromepisodestofactstoentitiestocommunities—extendsexistinghierarchicalRAGstrategies[10][11].
2.1 Episodes
Zep’s graphconstructionbeginswith the ingestionof raw data unitscalled Episodes. Episodescan be one of three
coretypes: message,text,orJSON.Whileeachtyperequiresspecifichandlingduringgraphconstruction,thispaper
focusesonthemessagetype,asourexperimentscenteronconversationmemory. Inourcontext,amessageconsists
ofrelativelyshorttext(severalmessagescanfitwithinanLLMcontextwindow)alongwiththeassociatedactorwho
producedtheutterance.
Eachmessageincludesareferencetimestampt indicatingwhenthemessagewassent. Thistemporalinformation
ref
enablesZep toaccuratelyidentifyandextractrelativeorpartialdatesmentionedin the messagecontent(e.g.,"next
Thursday,""intwoweeks,"or"lastsummer"). Zepimplementsabi-temporalmodel,wheretimelineT representsthe
chronologicalordering of events, and timeline T′ represents the transactional order of Zep’s data ingestion. While
the T′ timelineservesthe traditionalpurposeof databaseauditing,the T timeline providesan additionaldimension
for modelingthe dynamicnatureof conversationaldata and memory. Thisbi-temporalapproachrepresentsa novel
advancementinLLM-basedknowledgegraphconstructionandunderliesmuchofZep’suniquecapabilitiescompared
topreviousgraph-basedRAGproposals.
2

UsingKnowledgeGraphstopowerLLM-AgentMemory
The episodicedges, Ee, connectepisodesto theirextractedentity nodes. Episodesandtheirderivedsemanticedges
maintainbidirectionalindicesthattracktherelationshipsbetweenedgesandtheirsourceepisodes. Thisdesignrein-
forcesthenon-lossynatureofGraphiti’sepisodicsubgraphbyenablingbothforwardandbackwardtraversal:semantic
artifactscanbetracedtotheirsourcesforcitationorquotation,whileepisodescanquicklyretrievetheirrelevantenti-
tiesandfacts. Whiletheseconnectionsarenotdirectlyexaminedinthispaper’sexperiments,theywillbeexploredin
futurework.
2.2 SemanticEntitiesandFacts
2.2.1 Entities
ntity extraction represents the initial phase of episode processing. During ingestion, the system processes both the
currentmessagecontentandthelastnmessagestoprovidecontextfornamedentityrecognition. Forthispaperand
inZep’sgeneralimplementation,n=4,providingtwocompleteconversationturnsforcontextevaluation.Givenour
focusonmessageprocessing,thespeakerisautomaticallyextractedasanentity.Followinginitialentityextraction,we
employa reflectiontechniqueinspiredbyreflexion[12] tominimizehallucinationsandenhanceextractioncoverage.
The system also extractsan entity summaryfrom the episode to facilitate subsequententity resolutionand retrieval
operations.
Afterextraction,thesystemembedseachentitynameintoa1024-dimensionalvectorspace. Thisembeddingenables
theretrievalofsimilarnodesthroughcosinesimilaritysearchacrossexistinggraphentitynodes.Thesystemalsoper-
formsaseparatefull-textsearchonexistingentitynamesandsummariestoidentifyadditionalcandidatenodes.These
candidate nodes, together with the episode context, are then processed throughan LLM using our entity resolution
prompt.Whenthesystemidentifiesaduplicateentity,itgeneratesanupdatednameandsummary.
Followingentityextractionandresolution,thesystemincorporatesthedataintotheknowledgegraphusingpredefined
Cypherqueries. We chosethisapproachoverLLM-generateddatabasequeriestoensureconsistentschemaformats
andreducethepotentialforhallucinations.
Selectedpromptsforgraphconstructionareprovidedintheappendix.
2.2.2 Facts
oreachfactcontainingitskeypredicate. Importantly,thesamefactcanbeextractedmultipletimesbetweendifferent
entities,enablingGraphititomodelcomplexmulti-entityfactsthroughanimplementationofhyper-edges.
Following extraction, the system generates embeddings for facts in preparation for graph integration. The system
performsedge deduplicationthrougha process similar to entity resolution. The hybrid search for relevant edges is
constrainedtoedgesexistingbetweenthesameentitypairsastheproposednewedge.Thisconstraintnotonlyprevents
erroneouscombinationsof similar edges between differententities but also significantly reduces the computational
complexityofthededuplicationprocessbylimitingthesearchspacetoasubsetofedgesrelevanttothespecificentity
pair.
2.2.3 TemporalExtractionandEdgeInvalidation
AkeydifferentiatingfeatureofGraphiticomparedtootherknowledgegraphenginesisitscapacitytomanagedynamic
informationupdatesthroughtemporalextractionandedgeinvalidationprocesses.
The system extractstemporalinformationaboutfacts from the episode contextusing t . This enablesaccurate ex-
ref
tractionanddatetimerepresentationofbothabsolutetimestamps(e.g.,"AlanTuringwasbornonJune23,1912")and
relativetimestamps(e.g.,"Istartedmynewjobtwoweeksago").Consistentwithourbi-temporalmodelingapproach,
thesystemtracksfourtimestamps: t′createdandt′expired ∈ T′ monitorwhenfactsarecreatedorinvalidatedinthe
system,whilet andt ∈ T trackthetemporalrangeduringwhichfactsheldtrue. Thesetemporaldatapoints
valid invalid
arestoredonedgesalongsideotherfactinformation.
Theintroductionofnewedgescaninvalidateexistingedgesinthedatabase.ThesystememploysanLLMtocompare
new edges against semantically related existing edges to identify potential contradictions. When the system identi-
fies temporallyoverlappingcontradictions, it invalidatesthe affected edgesby setting their t to the t of the
invalid valid
invalidating edge. Following the transactional timeline T′, Graphiti consistently prioritizes new information when
determiningedgeinvalidation.
Thiscomprehensiveapproachenablesthe dynamicadditionofdatatoGraphitiasconversationsevolve,whilemain-
tainingbothcurrentrelationshipstatesandhistoricalrecordsofrelationshipevolutionovertime.
3

UsingKnowledgeGraphstopowerLLM-AgentMemory
2.3 Communities
Afterestablishingtheepisodicandsemanticsubgraphs,thesystemconstructsthecommunitysubgraphthroughcom-
munity detection. While our community detection approach builds upon the technique described in GraphRAG[4],
we employalabelpropagationalgorithm[13] ratherthantheLeidenalgorithm[14]. Thischoicewasinfluencedby
label propagation’s straightforward dynamic extension, which enables the system to maintain accurate community
representationsforlongerperiodsasnewdataentersthegraph,delayingtheneedforcompletecommunityrefreshes.
The dynamicextensionimplementsthe logicof a single recursivestep in labelpropagation. When the system adds
a new entity node ni ∈ Ns to the graph, it surveys the communities of neighboring nodes. The system assigns
the new node to the community held by the plurality of its neighbors, then updates the community summary and
graphaccordingly. Whilethisdynamicupdatingenablesefficientcommunityextensionasdataflowsintothesystem,
the resulting communities gradually diverge from those that would be generated by a complete label propagation
run. Therefore,periodiccommunityrefreshesremainnecessary. However,thisdynamicupdatingstrategyprovidesa
practicalheuristicthatsignificantlyreduceslatencyandLLMinferencecosts.
Following[4],ourcommunitynodescontainsummariesderivedthroughaniterativemap-reduce-stylesummarization
of member nodes. However, our retrievalmethodsdiffer substantially from GraphRAG’smap-reduceapproach[4].
Tosupportourretrievalmethodology,wegeneratecommunitynamescontainingkeytermsandrelevantsubjectsfrom
thecommunitysummaries.Thesenamesareembeddedandstoredtoenablecosinesimilaritysearches.
3 Memory Retrieval
The memory retrieval system in Zep providespowerful, complex, and highly configurable functionality. At a high
level,theZepgraphsearchAPIimplementsafunctionf :S →S thatacceptsatext-stringqueryα∈S asinputand
returnsatext-stringcontextβ ∈S asoutput.Theoutputβ containsformatteddatafromnodesandedgesrequiredfor
anLLMagenttogenerateanaccurateresponsetoqueryα. Theprocessf(α)→β comprisesthreedistinctsteps:
• Search (ϕ): The process begins by identifying candidate nodes and edges potentially containing relevant
information. WhileZepemploysmultipledistinctsearchmethods,theoverallsearchfunctioncanberepre-
sentedasϕ : S → En×Nn×Nn. Thus,ϕtransformsaqueryintoa3-tuplecontaininglistsofsemantic
s s c
edges,entitynodes,andcommunitynodes—thethreegraphtypescontainingrelevanttextualinformation.
• Reranker(ρ): Thesecondstepreorderssearchresults. Arerankerfunctionormodelacceptsalistofsearch
resultsandproducesareorderedversionofthoseresults:ρ:ϕ(α),... →En×Nn×Nn.
s s c
• Constructor(χ): Thefinalstep, the constructor,transformsthe relevantnodesandedgesintotextcontext:
χ:E
s
n×N
s
n×Ncn →S. Foreachei ∈Es,χreturnsthefactandtvalid,tinvalidfields;foreachni ∈Ns,
thenameandsummaryfields;andforeachni ∈Nc,thesummaryfield.
With these definitions established, we can express f as a composition of these three components: f(α) =
χ(ρ(ϕ(α)))=β.
Samplecontextstringtemplate:
FACTSandENTITIESrepresentrelevantcontexttothecurrentconversation.
Thesearethemostrelevantfactsandtheirvaliddateranges. Ifthefactisaboutanevent,theeventtakesplaceduring
thistime.
format:FACT(Daterange:from-to)
<FACTS>
{facts}
</FACTS>
Thesearethemostrelevantentities
ENTITY_NAME:entitysummary
<ENTITIES>
{entities}
</ENTITIES>
3.1 Search
Zepimplementsthreesearchfunctions:cosinesemanticsimilaritysearch(ϕ ),OkapiBM25full-textsearch(ϕ ),
cos bm25
and breadth-first search (ϕ ). The first two functions utilize Neo4j’s implementation of Lucene [15][16]. Each
bfs
4

UsingKnowledgeGraphstopowerLLM-AgentMemory
searchfunctionoffersdistinctcapabilitiesinidentifyingrelevantdocuments,andtogethertheyprovidecomprehensive
coverageofcandidateresultsbeforereranking.Thesearchfieldvariesacrossthethreeobjecttypes:forEs,wesearch
the fact field; for Ns, the entity name; and for Nc, the community name, which comprises relevant keywords and
phrases covered in the community. While developed independently, our community search approach parallels the
high-levelkeysearchmethodologyinLightRAG[17]. ThehybridizationofLightRAG’sapproachwithgraph-based
systemslikeGraphitipresentsapromisingdirectionforfutureresearch.
Whilecosinesimilarityandfull-textsearchmethodologiesarewell-establishedinRAG[18],breadth-firstsearchover
knowledgegraphs has received limited attention in the RAG domain, with notable exceptionsin graph-basedRAG
systemssuchasAriGraph[9]andDistill-SynthKG[19]. InGraphiti,thebreadth-firstsearchenhancesinitialsearch
resultsbyidentifyingadditionalnodesandedgeswithinn-hops.Moreover,ϕ canacceptnodesasparametersforthe
bfs
search,enablinggreatercontroloverthesearchfunction. Thisfunctionalityprovesparticularlyvaluablewhenusing
recent episodesas seeds for the breadth-firstsearch, allowing the system to incorporaterecently mentionedentities
andrelationshipsintotheretrievedcontext.
Thethreesearchmethodseachtargetdifferentaspectsofsimilarity:full-textsearchidentifieswordsimilarities,cosine
similarity captures semantic similarities, and breadth-first search reveals contextual similarities—where nodes and
edges closer in the graph appear in more similar conversationalcontexts. This multi-facetedapproach to candidate
resultidentificationmaximizesthelikelihoodofdiscoveringoptimalcontext.
3.2 Reranker
While the initial searchmethodsaim to achievehigh recall, rerankersserve to increaseprecisionby prioritizingthe
most relevant results. Zep supports existing rerankingapproachessuch as Reciprocal Rank Fusion (RRF) [20] and
MaximalMarginalRelevance(MMR)[21]. Additionally,Zepimplementsagraph-basedepisode-mentionsreranker
that prioritizes results based on the frequency of entity or fact mentions within a conversation, enabling a system
wherefrequentlyreferencedinformationbecomesmorereadilyaccessible. Thesystemalsoincludesanodedistance
rerankerthatreordersresultsbasedontheirgraphdistancefromadesignatedcentroidnode,providingcontextlocal-
ized to specific areas of the knowledgegraph. The system’s most sophisticated rerankingcapability employscross-
encoders—LLMsthatgeneraterelevancescoresbyevaluatingnodesandedgesagainstqueriesusingcross-attention,
thoughthisapproachincursthehighestcomputationalcost.
4 Experiments
ThissectionanalyzestwoexperimentsconductedusingLLM-memorybasedbenchmarks.Thefirstevaluationemploys
theDeepMemoryRetrieval(DMR)taskdevelopedin[3],whichusesa500-conversationsubsetoftheMulti-Session
Chat dataset introduced in "Beyond Goldfish Memory: Long-Term Open-Domain Conversation" [22]. The second
evaluationutilizestheLongMemEvalbenchmarkfrom"LongMemEval:BenchmarkingChatAssistantsonLong-Term
InteractiveMemory"[7]. Specifically,weusetheLongMemEvalsdataset,whichprovidesanextensiveconversation
contextofonaverage115,000tokens.
For both experiments, we integrate the conversation history into a Zep knowledge graph through Zep’s APIs. We
thenretrievethe20mostrelevantedges(facts)andentitynodes(entitysummaries)usingthetechniquesdescribedin
Section3. Thesystemreformatsthisdataintoacontextstring,matchingthefunctionalityprovidedbyZep’smemory
APIs.
While these experiments demonstrate key retrieval capabilities of Graphiti, they represent a subset of the system’s
fullsearchfunctionality. Thisfocusedscopeenablesclearcomparisonwithexistingbenchmarkswhilereservingthe
explorationofadditionalknowledgegraphcapabilitiesforfuturework.
4.1 Choiceofmodels
OurexperimentalimplementationemploystheBGE-m3modelsfromBAAIforbothrerankingandembeddingtasks
[23][24]. Forgraphconstructionandresponsegeneration,weutilizegpt-4o-mini-2024-07-18forgraphconstruction,
andbothgpt-4o-mini-2024-07-18andgpt-4o-2024-11-20forthechatagentgeneratingresponsestoprovidedcontext.
To ensure direct comparability with MemGPT’s DMR results, we also conductedthe DMR evaluation using gpt-4-
turbo-2024-04-09.
TheexperimentalnotebookswillbemadepubliclyavailablethroughourGitHubrepository,andrelevantexperimental
promptsareincludedintheAppendix.
5

UsingKnowledgeGraphstopowerLLM-AgentMemory
Table1:DeepMemoryRetrieval
Memory Model Score
RecursiveSummarization† gpt-4-turbo 35.3%
ConversationSummaries gpt-4-turbo 78.6%
MemGPT† gpt-4-turbo 93.4%
Full-conversation gpt-4-turbo 94.4%
Zep gpt-4-turbo 94.8%
ConversationSummaries gpt-4o-mini 88.0%
Full-conversation gpt-4o-mini 98.0%
Zep gpt-4o-mini 98.2%
† Resultsreportedin[3].
4.2 DeepMemoryRetrieval(DMR)
TheDeepMemoryRetrievalevaluation,introducedby[3],comprises500multi-sessionconversations,eachcontaining
5 chatsessions with up to 12 messagesper session. Eachconversationincludesa question/answerpair formemory
evaluation.TheMemGPTframework[3]currentlyleadsperformancemetricswith93.4%accuracyusinggpt-4-turbo,
asignificantimprovementoverthe35.3%baselineachievedthroughrecursivesummarization.
To establishcomparativebaselines, weimplementedtwocommonLLMmemoryapproaches: full-conversationcon-
textandsessionsummaries. Usinggpt-4-turbo,thefull-conversationbaselineachieved94.4%accuracy,slightlysur-
passingMemGPT’sreportedresults, whilethesessionsummarybaselineachieved78.6%. Whenusinggpt-4o-mini,
bothapproachesshowedimprovedperformance: 98.0%forfull-conversationand88.0%forsessionsummaries. We
were unable to reproduce MemGPT’s results using gpt-4o-mini due to insufficient methodological details in their
publishedwork.
WethenevaluatedZep’sperformancebyingestingtheconversationsandusingitssearchfunctionstoretrievethetop
10 most relevantnodesand edges. An LLM judge comparedthe agent’s responsesto the providedgoldenanswers.
Zep achieved 94.8% accuracy with gpt-4-turboand 98.2% with gpt-4o-mini, showing marginalimprovementsover
both MemGPT and the respective full-conversationbaselines. However, these results must be contextualized: each
conversationcontainsonly60messages,easilyfittingwithincurrentLLMcontextwindows.
The limitationsof the DMR evaluationextendbeyondits small scale. Our analysisrevealedsignificantweaknesses
inthebenchmark’sdesign. Theevaluationreliesexclusivelyonsingle-turn,fact-retrievalquestionsthatfailtoassess
complex memory understanding. Many questions contain ambiguous phrasing, referencing concepts like "favorite
drinktorelaxwith"or"weirdhobby"thatwerenotexplicitlycharacterizedassuchintheconversations.Mostcritically,
the dataset poorly represents real-world enterprise use cases for LLM agents. The high performance achieved by
simple full-context approaches using modern LLMs further highlights the benchmark’s inadequacy for evaluating
memorysystems.
Thisinadequacyisfurtheremphasizedbyfindingsin[7],whichdemonstraterapidlydecliningLLMperformanceon
the LongMemEvalbenchmarkas conversation length increases. The LongMemEvaldataset [7] addresses many of
these shortcomingsby presentinglonger, more coherentconversationsthat better reflect enterprise scenarios, along
withmorediverseevaluationquestions.
4.3 LongMemEval(LME)
WeevaluatedZepusingtheLongMemEvalsdataset,whichprovidesconversationsandquestionsrepresentativeofreal-
world business applicationsof LLM agents. The LongMemEvalsdataset presentssignificant challengesto existing
LLMsandcommercialmemorysolutions[7], withconversationsaveragingapproximately115,000tokensinlength.
Thislength,whilesubstantial,remainswithinthecontextwindowsofcurrentfrontiermodels,enablingustoestablish
meaningfulbaselinesforevaluatingZep’sperformance.
The dataset incorporates six distinct question types: single-session-user, single-session-assistant, single-session-
preference,multi-session,knowledge-update,andtemporal-reasoning.Thesecategoriesarenotuniformlydistributed
throughoutthedataset;fordetaileddistributioninformation,wereferreadersto[7].
We conductedall experimentsbetween December2024andJanuary 2025. We performedtesting using a consumer
laptop from a residential location in Boston, MA, connecting to Zep’s service hosted in AWS us-west-2. This dis-
6

UsingKnowledgeGraphstopowerLLM-AgentMemory
tributed architecture introducedadditionalnetworklatency when evaluating Zep’s performance,though this latency
wasnotpresentinourbaselineevaluations.
Foranswerevaluation,weemployedGPT-4owiththequestion-specificpromptsprovidedin[7],whichhavedemon-
stratedhighcorrelationwithhumanevaluators.
4.3.1 LongMemEvalandMemGPT
ToestablishacomparativebenchmarkbetweenZepandthecurrentstate-of-the-artMemGPTsystem[3],weattempted
toevaluateMemGPTusingtheLongMemEvaldataset. GiventhatthecurrentMemGPTframeworkdoesnotsupport
directingestionofexistingmessagehistories,weimplementedaworkaroundbyaddingconversationmessagestothe
archival history. However, we were unable to achieve successful question responses using this approach. We look
forward to seeing evaluations of this benchmark by other research teams, as comparative performance data would
benefitthebroaderdevelopmentofLLMmemorysystems.
4.3.2 LongMemEvalresults
Zepdemonstratessubstantialimprovementsinbothaccuracyandlatencycomparedtothebaselineacrossbothmodel
variants. Usinggpt-4o-mini,Zepachieveda15.2%accuracyimprovementoverthebaseline,whilegpt-4oshowedan
18.5%improvement.Thereducedpromptsizealsoledtosignificantlatencycostreductionscomparedtothebaseline
implementations.
|              |             | Table2: LongMemEvals |            |                  |
| ------------ | ----------- | -------------------- | ---------- | ---------------- |
| Memory       | Model       | Score Latency        | LatencyIQR | AvgContextTokens |
| Full-context | gpt-4o-mini | 55.4% 31.3s          | 8.76s      | 115k             |
| Zep          | gpt-4o-mini | 63.8% 3.20s          | 1.31s      | 1.6k             |
| Full-context | gpt-4o      | 60.2% 28.9s          | 6.01s      | 115k             |
| Zep          | gpt-4o      | 71.2% 2.58s          | 0.684s     | 1.6k             |
Analysis by question type reveals that gpt-4o-mini with Zep showed improvements in four of the six categories,
with the most substantial gains in complex question types: single-session-preference, multi-session, and temporal-
reasoning. When using gpt-4o, Zep furtherdemonstratedimprovedperformancein the knowledge-updatecategory,
highlightingitseffectivenesswithmorecapablemodels.However,additionaldevelopmentmaybeneededtoimprove
lesscapablemodels’understandingofZep’stemporaldata.
Table3:LongMemEvalsQuestionTypeBreakdown
| QuestionType |     | Model | Full-context | Zep Delta |
| ------------ | --- | ----- | ------------ | --------- |
53.3% 77.7%↑
| single-session-preference |     | gpt-4o-mini | 30.0% |              |
| ------------------------- | --- | ----------- | ----- | ------------ |
| single-session-assistant  |     | gpt-4o-mini | 81.8% | 75.0% 9.06%↓ |
| temporal-reasoning        |     | gpt-4o-mini | 36.5% | 54.1% 48.2%↑ |
| multi-session             |     | gpt-4o-mini | 40.6% | 47.4% 16.7%↑ |
| knowledge-update          |     | gpt-4o-mini | 76.9% | 74.4% 3.36%↓ |
| single-session-user       |     | gpt-4o-mini | 81.4% | 92.9% 14.1%↑ |
| single-session-preference |     | gpt-4o      | 20.0% | 56.7% 184%↑  |
| single-session-assistant  |     | gpt-4o      | 94.6% | 80.4% 17.7%↓ |
| temporal-reasoning        |     | gpt-4o      | 45.1% | 62.4% 38.4%↑ |
| multi-session             |     | gpt-4o      | 44.3% | 57.9% 30.7%↑ |
| knowledge-update          |     | gpt-4o      | 78.2% | 83.3% 6.52%↑ |
| single-session-user       |     | gpt-4o      | 81.4% | 92.9% 14.1%↑ |
These resultsdemonstrateZep’s ability to enhanceperformanceacrossmodelscales, with the most pronouncedim-
provementsobserved in complex and nuanced question types when paired with more capable models. The latency
improvementsareparticularlynoteworthy,withZepreducingresponsetimesbyapproximately90%whilemaintain-
inghigheraccuracy.
7

UsingKnowledgeGraphstopowerLLM-AgentMemory
The decrease in performance for single-session-assistant questions—17.7% for gpt-4o and 9.06% for gpt-4o-
mini—representsa notable exceptionto Zep’s otherwiseconsistentimprovements,and suggestfurtherresearchand
engineeringworkisneeded.
5 Conclusion
We haveintroducedZep, agraph-basedapproachtoLLMmemorythatincorporatessemanticandepisodicmemory
alongside entity and community summaries. Our evaluations demonstrate that Zep achieves state-of-the-art perfor-
manceonexistingmemorybenchmarkswhilereducingtokencostsandoperatingatsignificantlylowerlatencies.
The results achievedwith Graphiti and Zep, while impressive, likely representonly initial advancesin graph-based
memory systems. Multiple research avenues could build upon these frameworks, including integration of other
GraphRAGapproachesintotheZepparadigmandnovelextensionsofourwork.
Researchhasalreadydemonstratedthevalueoffine-tunedmodelsforLLM-basedentityandedgeextractionwithin
the GraphRAG paradigm, improving accuracy while reducing costs and latency [19][25]. Similar models fine-
tuned for Graphiti prompts may enhance knowledge extraction, particularly for complex conversations. Addition-
ally, while currentresearch on LLM-generatedknowledgegraphshas primarily operatedwithoutformalontologies
[9][4][17][19][26], domain-specific ontologies present significant potential. Graph ontologies, foundational in pre-
LLMknowledgegraphwork,warrantfurtherexplorationwithintheGraphitiframework.
Our search for suitable memory benchmarks revealed limited options, with existing benchmarks often lacking ro-
bustness andcomplexity,frequentlydefaultingto simple needle-in-a-haystackfact-retrievalquestions[3]. The field
requiresadditionalmemorybenchmarks,particularlythosereflectingbusinessapplicationslikecustomerexperience
tasks,toeffectivelyevaluateanddifferentiatememoryapproaches.Notably,noexistingbenchmarksadequatelyassess
Zep’scapabilitytoprocessandsynthesizeconversationhistorywithstructuredbusinessdata. WhileZepfocuseson
LLM memory,its traditionalRAG capabilitiesshouldbe evaluatedagainstestablished benchmarkssuch as thosein
[17],[27],and[28].
CurrentliteratureonLLMmemoryandRAGsystemsinsufficientlyaddressesproductionsystemscalabilityinterms
ofcostandlatency. Wehaveincludedlatencybenchmarksforourretrievalmechanismstobeginaddressingthisgap,
followingtheexamplesetbyLightRAG’sauthorsinprioritizingthesemetrics.
6 Appendix
6.1 GraphConstructionPrompts
6.1.1 EntityExtraction
<PREVIOUSMESSAGES>
{previous_messages}
</PREVIOUSMESSAGES>
<CURRENTMESSAGE>
{current_message}
</CURRENTMESSAGE>
Given the aboveconversation,extractentity nodesfrom the CURRENT MESSAGE that are explicitly or implicitly
mentioned:
Guidelines:
1.ALWAYSextractthespeaker/actorasthefirstnode.Thespeakeristhepartbeforethecolonineachlineofdialogue.
2. Extractothersignificantentities,concepts,oractorsmentionedintheCURRENTMESSAGE.
3. DONOTcreatenodesforrelationshipsoractions.
4. DONOTcreatenodesfortemporalinformationlikedates,timesoryears(thesewillbeaddedtoedgeslater).
5. Beasexplicitaspossibleinyournodenames,usingfullnames.
6. DONOTextractentitiesmentionedonly
8

UsingKnowledgeGraphstopowerLLM-AgentMemory
6.1.2 EntityResolution
<PREVIOUSMESSAGES>
{previous_messages}
</PREVIOUSMESSAGES>
<CURRENTMESSAGE>
{current_message}
</CURRENTMESSAGE>
<EXISTINGNODES>
{existing_nodes}
</EXISTINGNODES>
Given the above EXISTING NODES, MESSAGE, and PREVIOUS MESSAGES. Determine if the NEW NODE
extractedfromtheconversationisaduplicateentityofoneoftheEXISTINGNODES.
<NEWNODE>
{new_node}
</NEWNODE>
Task:
1.IftheNewNoderepresentsthesameentityasanynodeinExistingNodes,return’is_duplicate:true’intheresponse.
Otherwise,return’is_duplicate:false’
2. Ifis_duplicateistrue,alsoreturntheuuidoftheexistingnodeintheresponse
3. Ifis_duplicateistrue,returnanameforthenodethatisthemostcompletefullname.
Guidelines:
1. Use both the name and summary of nodes to determine if the entities are duplicates, duplicate nodes may have
differentnames
6.1.3 FactExtraction
<PREVIOUSMESSAGES>
{previous_messages}
</PREVIOUSMESSAGES>
<CURRENTMESSAGE>
{current_message}
</CURRENTMESSAGE>
<ENTITIES>
{entities}
</ENTITIES>
GiventheaboveMESSAGESandENTITIES,extractallfactspertainingtothelistedENTITIESfromtheCURRENT
MESSAGE.
Guidelines:
1. Extractfactsonlybetweentheprovidedentities.
2. EachfactshouldrepresentaclearrelationshipbetweentwoDISTINCTnodes.
3. The relation_type should be a concise, all-caps description of the fact (e.g., LOVES, IS_FRIENDS_WITH,
WORKS_FOR).
4. Provideamoredetailedfactcontainingallrelevantinformation.
5. Considertemporalaspectsofrelationshipswhenrelevant.
9

UsingKnowledgeGraphstopowerLLM-AgentMemory
6.1.4 FactResolution
Giventhefollowingcontext,determinewhethertheNewEdgerepresentsanyoftheedgesinthelistofExistingEdges.
<EXISTINGEDGES>
{existing_edges}
</EXISTINGEDGES>
<NEWEDGE>
{new_edge}
</NEWEDGE>
Task:
1. IftheNewEdgesrepresentsthesamefactualinformationasanyedgeinExistingEdges,return’is_duplicate:true’
intheresponse.Otherwise,return’is_duplicate:false’
2. Ifis_duplicateistrue,alsoreturntheuuidoftheexistingedgeintheresponse
Guidelines:
1. Thefactsdonotneedtobecompletelyidenticaltobeduplicates,theyjustneedtoexpressthesameinformation.
6.1.5 TemporalExtraction
<PREVIOUSMESSAGES>
{previous_messages}
</PREVIOUSMESSAGES>
<CURRENTMESSAGE>
{current_message}
</CURRENTMESSAGE>
<REFERENCETIMESTAMP>
{reference_timestamp}
</REFERENCETIMESTAMP>
<FACT>
{fact}
</FACT>
IMPORTANT:Onlyextracttimeinformationifitispartoftheprovidedfact. Otherwiseignorethetimementioned.
Makesuretodoyourbesttodeterminethedatesifonlytherelativetimeismentioned. (eg10yearsago,2minsago)
basedontheprovidedreferencetimestamp
Iftherelationshipisnotofspanningnature,butyouarestillabletodeterminethedates,setthevalid_atonly.
Definitions:
-valid_at:Thedateandtimewhentherelationshipdescribedbytheedgefactbecametrueorwasestablished.
-invalid_at:Thedateandtimewhentherelationshipdescribedbytheedgefactstoppedbeingtrueorended.
Task:
Analyzetheconversationanddetermineiftherearedatesthatarepartoftheedgefact. Onlysetdatesiftheyexplicitly
relatetotheformationoralterationoftherelationshipitself.
Guidelines:
1. UseISO8601format(YYYY-MM-DDTHH:MM:SS.SSSSSSZ)fordatetimes.
2. Usethereferencetimestampasthecurrenttimewhendeterminingthevalid_atandinvalid_atdates.
3. Ifthefactiswritteninthepresenttense,usetheReferenceTimestampforthevalid_atdate
4. Ifnotemporalinformationisfoundthatestablishesorchangestherelationship,leavethefieldsasnull.
5. Donotinferdatesfromrelatedevents.Onlyusedatesthataredirectlystatedtoestablishorchangetherelationship.
6. Forrelativetimementionsdirectlyrelatedtotherelationship,calculatetheactualdatetimebasedonthereference
timestamp.
7. Ifonlyadateismentionedwithoutaspecifictime,use00:00:00(midnight)forthatdate.
8. Ifonlyyearismentioned,useJanuary1stofthatyearat00:00:00.
9. Alwaysincludethetimezoneoffset(useZforUTCifnospecifictimezoneismentioned).
References
[1] Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Lukasz Kaiser,
andIlliaPolosukhin. Attentionisallyouneed,2023.
[2] K.SparckJones. Astatisticalinterpretationoftermspecificityanditsapplicationinretrieval. JournalofDocu-
mentation,28(1):11–21,1972.
10

UsingKnowledgeGraphstopowerLLM-AgentMemory
[3] CharlesPacker, Sarah Wooders, Kevin Lin, VivianFang, Shishir G. Patil, IonStoica, andJoseph E. Gonzalez.
Memgpt:Towardsllmsasoperatingsystems,2024.
[4] DarrenEdge,HaTrinh,NewmanCheng,JoshuaBradley,AlexChao,ApurvaMody,StevenTruitt,andJonathan
Larson. Fromlocaltoglobal:Agraphragapproachtoquery-focusedsummarization,2024.
[5] Zep. Zep:Long-termmemoryforaiagents. https://www.getzep.com,2024. Commercialmemorylayerfor
AIapplications.
[6] Zep. Graphiti: Temporal knowledge graphs for agentic applications.
https://github.com/getzep/graphiti, 2024. Graphiti builds dynamic, temporally aware Knowledge
Graphsthatrepresentcomplex,evolvingrelationshipsbetweenentitiesovertime.
[7] DiWu,HongweiWang,WenhaoYu,YuweiZhang,Kai-WeiChang,andDongYu. Longmemeval:Benchmark-
ingchatassistantsonlong-terminteractivememory,2024.
[8] WongGonzalezandDaniela. Therelationshipbetweensemanticandepisodicmemory: Exploringtheeffectof
semanticneighbourhooddensityonepisodicmemory. PhDthesis,UniversityofWinsor,2018.
[9] Petr Anokhin, Nikita Semenov, Artyom Sorokin, Dmitry Evseev, Mikhail Burtsev, and Evgeny Burnaev. Ari-
graph:Learningknowledgegraphworldmodelswithepisodicmemoryforllmagents,2024.
[10] XinyueChen,PengyuGao,JiangjiangSong,andXiaoyangTan. Hiqa: Ahierarchicalcontextualaugmentation
ragformulti-documentsqa,2024.
[11] KrishGoelandMahekChandak. Hiro:Hierarchicalinformationretrievaloptimization,2024.
[12] NoahShinn,FedericoCassano,EdwardBerman,AshwinGopinath,KarthikNarasimhan,andShunyuYao. Re-
flexion:Languageagentswithverbalreinforcementlearning,2023.
[13] XiaojinZhuandZoubinGhahramani. Learningfromlabeledandunlabeleddatawithlabelpropagation. 2002.
[14] V.A.Traag,L.Waltman,andN.J.vanEck. Fromlouvaintoleiden: guaranteeingwell-connectedcommunities.
SciRep9,5233,2019.
[15] Neo4j. Neo4j-theworld’sleadinggraphdatabase,2012.
[16] ApacheSoftwareFoundation. Apachelucene-scoring,2011. letzterZugriff:20.Oktober2011.
[17] ZiruiGuo,LianghaoXia,YanhuaYu,TuAo,andChaoHuang. Lightrag: Simpleandfastretrieval-augmented
generation,2024.
[18] JimmyLin,RonakPradeep,TommasoTeofili,andJasperXian. Vectorsearchwithopenaiembeddings:Lucene
isallyouneed,2023.
[19] PrafullaKumarChoubey,Xin Su, Man Luo, XiangyuPeng, CaimingXiong, Tiep Le, ShacharRosenman, Va-
sudev Lal, Phil Mui, Ricky Ho, Phillip Howard, and Chien-ShengWu. Distill-synthkg: Distilling knowledge
graphsynthesisworkflowforimprovedcoverageandefficiency,2024.
[20] GordonV.Cormack,CharlesL.A.Clarke,andStefanBuettcher. Reciprocalrankfusionoutperformscondorcet
and individual rank learning methods. In Proceedings of the 32nd International ACM SIGIR Conference on
ResearchandDevelopmentinInformationRetrieval,SIGIR’09,pages758–759.ACM,2009.
[21] JaimeCarbonellandJadeGoldstein. Theuseofmmr,diversity-basedrerankingforreorderingdocumentsand
producingsummaries.InProceedingsofthe21stAnnualInternationalACMSIGIRConferenceonResearchand
Developmentin InformationRetrieval, SIGIR’98,page335–336,New York,NY, USA, 1998.Association for
ComputingMachinery.
[22] Jing Xu, Arthur Szlam, and Jason Weston. Beyond goldfish memory: Long-term open-domain conversation,
2021.
[23] ChaofanLi,ZhengLiu,ShitaoXiao,andYingxiaShao. Makinglargelanguagemodelsabetterfoundationfor
denseretrieval,2023.
[24] Jianlv Chen, Shitao Xiao, Peitian Zhang, Kun Luo, Defu Lian, and Zheng Liu. Bge m3-embedding: Multi-
lingual,multi-functionality,multi-granularitytextembeddingsthroughself-knowledgedistillation,2024.
[25] Shreyas Pimpalgaonkar, Nolan Tremelling, and Owen Colegrove. Triplex: a sota llm for knowledge graph
construction,2024.
[26] ShilongLi, YanchengHe, HangyuGuo, XingyuanBu, Ge Bai, Jie Liu, JiahengLiu, XingweiQu, Yangguang
Li,WanliOuyang,WenboSu,andBoZheng. Graphreader:Buildinggraph-basedagenttoenhancelong-context
abilitiesoflargelanguagemodels,2024.
11

UsingKnowledgeGraphstopowerLLM-AgentMemory
[27] PranabIslam,AnandKannappan,DouweKiela,RebeccaQian,NinoScherrer,andBertieVidgen.Financebench:
Anewbenchmarkforfinancialquestionanswering,2023.
[28] NandanThakur,NilsReimers,AndreasRücklé,AbhishekSrivastava,andIrynaGurevych.Beir:Aheterogenous
benchmarkforzero-shotevaluationofinformationretrievalmodels,2021.
12