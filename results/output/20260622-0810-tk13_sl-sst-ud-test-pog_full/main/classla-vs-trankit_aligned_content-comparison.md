# Table-style content comparison (Trankit aligned vs CLASSLA aligned)

Columns 7-8 are compared directly (HEAD and DEPREL), with concrete token examples.

## Scope
- Gold sentences: 420
- Trankit aligned sentences: 420
- CLASSLA aligned sentences: 420

## Trankit aligned - error content tables
- Compared tokens: 11443
- LAS-correct tokens: 9585 (83.76%)

### A) HEAD wrong, DEPREL correct
| Rank | Gold DEPREL | Pred DEPREL | Count | Example |
|---|---|---|---:|---|
| 1 | punct | (same DEPREL, wrong HEAD) | 347 (3.03%) | sid=Gos160.s153; tok=.#9; gold=(2,punct); pred=(5,punct); text="sam tok , da zadiši vino , ne ." |
| 2 | discourse | (same DEPREL, wrong HEAD) | 130 (1.14%) | sid=Gos162.s496; tok=ne#9; gold=(7,discourse); pred=(3,discourse); text="jz ne vem , kk ti zbral , ne , mogoče po šibicam , ne ." |
| 3 | advmod | (same DEPREL, wrong HEAD) | 120 (1.05%) | sid=Gos160.s158; tok=še#3; gold=(5,advmod); pred=(4,advmod); text="marinado sva še prej ohladila , bog ne dej , da date toplo gor ." |
| 4 | conj | (same DEPREL, wrong HEAD) | 83 (0.73%) | sid=Gos163.s224; tok=in#19; gold=(7,conj); pred=(3,conj); text="e , je pa tako , dal sem mu tud druge naloge , ker morjo bit opravljene , in" |
| 5 | parataxis | (same DEPREL, wrong HEAD) | 66 (0.58%) | sid=Gos162.s499; tok=zbral#20; gold=(7,parataxis); pred=(2,parataxis); text="[name:personal] je pač mogoč teti tedn izrazu željo , da bi pač rad bolj pomagal pr žvalih , ..." |
| 6 | reparandum | (same DEPREL, wrong HEAD) | 44 (0.38%) | sid=Gos162.s501; tok=t…#1; gold=(5,reparandum); pred=(3,reparandum); text="t… , tud , mogoč , tud mogoč zarad tega , čevta čevta res šla vidva v dvoboj , da maš pač ti ..." |
| 7 | obl | (same DEPREL, wrong HEAD) | 34 (0.30%) | sid=Gos179.s171; tok=tega#12; gold=(7,obl); pred=(4,obl); text="ja , sam vprašanje , kdo je to v resnici izza tega , ne ." |
| 8 | nsubj | (same DEPREL, wrong HEAD) | 33 (0.29%) | sid=Gos162.s499; tok=[name:personal]#1; gold=(7,nsubj); pred=(2,nsubj); text="[name:personal] je pač mogoč teti tedn izrazu željo , da bi pač rad bolj pomagal pr žvalih , ..." |
| 9 | cc | (same DEPREL, wrong HEAD) | 33 (0.29%) | sid=Gos165.s185; tok=in#3; gold=(17,cc); pred=(5,cc); text="no , in potem so , eee , na Kranjski koči na Ledinah jim je ravnokar odpovedala oskrbnica in ..." |
| 10 | acl | (same DEPREL, wrong HEAD) | 24 (0.21%) | sid=Gos216.s237; tok=se#19; gold=(16,acl); pred=(28,acl); text="zej , če grema klasična polena reč , potem je takoj , potem je to peč , kjer se zdaj te , ki ..." |
| 11 | mark | (same DEPREL, wrong HEAD) | 22 (0.19%) | sid=Gos162.s502; tok=če#7; gold=(11,mark); pred=(8,mark); text="če bota sveda šla vidva , če ne , ojo… šle punce , al ?" |
| 12 | advcl | (same DEPREL, wrong HEAD) | 20 (0.17%) | sid=Gos163.s217; tok=opravl#13; gold=(6,advcl); pred=(7,advcl); text="ki je borte , boste mogl opravt , če boste to nalogo opravl ." |
| 13 | nmod | (same DEPREL, wrong HEAD) | 20 (0.17%) | sid=Gos165.s180; tok=Jezerskim#11; gold=(7,nmod); pred=(9,nmod); text="in si služla dnar v gorski koči na Ledinah nad Jezerskim , kako si zašla tja , ljubezen do go..." |
| 14 | obj | (same DEPREL, wrong HEAD) | 16 (0.14%) | sid=Gos162.s499; tok=željo#8; gold=(7,obj); pred=(2,obj); text="[name:personal] je pač mogoč teti tedn izrazu željo , da bi pač rad bolj pomagal pr žvalih , ..." |
| 15 | aux | (same DEPREL, wrong HEAD) | 14 (0.12%) | sid=Gos171.s268; tok=bi#20; gold=(24,aux); pred=(22,aux); text="to je tekma , ki jo seveda morejo dobiti , toda ta poraz , že drugi na gostovanju , bi precej..." |
| 16 | cop | (same DEPREL, wrong HEAD) | 13 (0.11%) | sid=Gos216.s238; tok=so#8; gold=(11,cop); pred=(10,cop); text="se pravi , da je to , so zelo učinkovite peči na polena , ki imajo , ki , mmm , rečmo tem naj..." |
| 17 | case | (same DEPREL, wrong HEAD) | 12 (0.10%) | sid=Gos165.s194; tok=po#10; gold=(12,case); pred=(13,case); text="in mi je vsako jutro že za zajtrk skuhala po ene pet jajc pa masonek ." |
| 18 | amod | (same DEPREL, wrong HEAD) | 9 (0.08%) | sid=Gos216.s237; tok=klasična#5; gold=(6,amod); pred=(7,amod); text="zej , če grema klasična polena reč , potem je takoj , potem je to peč , kjer se zdaj te , ki ..." |
| 19 | appos | (same DEPREL, wrong HEAD) | 7 (0.06%) | sid=Gos170.s139; tok=menedžer#8; gold=(5,appos); pred=(2,appos); text="tu Dejvid Hili in Najdžl Vrfingtn , menedžer oziroma selektor reprezentance ." |
| 20 | det | (same DEPREL, wrong HEAD) | 6 (0.05%) | sid=Gos162.s499; tok=teti#5; gold=(6,det); pred=(7,det); text="[name:personal] je pač mogoč teti tedn izrazu željo , da bi pač rad bolj pomagal pr žvalih , ..." |

### B) HEAD correct, DEPREL wrong
| Rank | Gold DEPREL | Pred DEPREL | Count | Example |
|---|---|---|---:|---|
| 1 | parataxis | conj | 12 (0.10%) | sid=Gos160.s157; tok=zloženi#5; gold=(3,parataxis); pred=(3,conj); text="piščanci so prpravljeni , zloženi ." |
| 2 | obj | iobj | 9 (0.08%) | sid=Gos206.s139; tok=ga#20; gold=(21,obj); pred=(21,iobj); text="in tam dobite naslove in pokličete nekega gospoda al pa gospo oziroma lastnika te hiše , ga p..." |
| 3 | nmod | obl | 8 (0.07%) | sid=Gos163.s226; tok=volno#32; gold=(29,nmod); pred=(29,obl); text="tako ko sem mu naroču , taku je treba to nardit , eee , sem mu vse lepo povedu in razložu , e..." |
| 4 | conj | parataxis | 8 (0.07%) | sid=Gos165.s187; tok=pestro#24; gold=(4,conj); pred=(4,parataxis); text="od teh plinskih bomb , k jih je blo treba neki tkole šravfat , pa vse živo , skratka , blo je..." |
| 5 | nsubj | obj | 7 (0.06%) | sid=Gos160.s153; tok=vino#6; gold=(5,nsubj); pred=(5,obj); text="sam tok , da zadiši vino , ne ." |
| 6 | ccomp | advcl | 7 (0.06%) | sid=Gos160.s158; tok=date#12; gold=(9,ccomp); pred=(9,advcl); text="marinado sva še prej ohladila , bog ne dej , da date toplo gor ." |
| 7 | parataxis | cc | 7 (0.06%) | sid=Gos216.s233; tok=al#22; gold=(23,parataxis); pred=(23,cc); text="ne em , z biomaso je tako , biomaso imate vi ze tri vrste , bi reku , tri vrste , al mate kla..." |
| 8 | appos | conj | 7 (0.06%) | sid=Artur-J-Gvecg-P500014.s277-s279_reseg.104; tok=Zume#30; gold=(25,appos); pred=(25,conj); text="ja , po eni strani moram povedat , no , da nekje polovica naših uporabnikov programov se je o..." |
| 9 | obl | nmod | 6 (0.05%) | sid=Gos162.s495; tok=igre#16; gold=(15,obl); pred=(15,nmod); text="eno so , eno bojo verjetno poslali domov , no , tudi to je del igre ." |
| 10 | advmod | discourse | 6 (0.05%) | sid=Gos170.s128; tok=jasno#3; gold=(9,advmod); pred=(9,discourse); text="toda , jasno , ob Vidiču in Ferdinendu nima dosti možnosti za igranje ." |
| 11 | discourse | advmod | 6 (0.05%) | sid=Gos213.s78; tok=tak#31; gold=(30,discourse); pred=(30,advmod); text="aha , kul , eee , čaki , še kako vprašanje , eee , to pa , eee , če , če nabavim to , mate k…..." |
| 12 | conj | appos | 6 (0.05%) | sid=Artur-J-Gvecg-P500028.s214-s224_reseg.237; tok=tehnologije#24; gold=(17,conj); pred=(17,appos); text="cilj je , da se nardi iz , hh , tko , da se regulira umetno inteligenco oziroma to tehnologij..." |
| 13 | discourse | orphan | 5 (0.04%) | sid=Gos163.s229; tok=na#7; gold=(8,discourse); pred=(8,orphan); text="se ni , se ni nč na premaknl ne na drugo stran ." |
| 14 | iobj | obj | 5 (0.04%) | sid=Gos179.s181; tok=jo#10; gold=(11,iobj); pred=(11,obj); text="pa , eee , moram se spomnt , da jo vprašam ." |
| 15 | advmod | orphan | 5 (0.04%) | sid=Gos193.s142; tok=pol#4; gold=(3,advmod); pred=(3,orphan); text="ja , mene pol čist nič , mene , eee , s pinceto ne boli , oblikovanje , čist nič ." |
| 16 | obj | nsubj | 5 (0.04%) | sid=Gos216.s241; tok=plamen#44; gold=(45,obj); pred=(45,nsubj); text="je tudi vso j… , vse je tudi regulirano temperaturno , mate vse o… , vse senzorje zgoraj in p..." |
| 17 | cc | advmod | 5 (0.04%) | sid=Artur-J-Gvecg-P500028.s117-s120_reseg.218; tok=celo#18; gold=(23,cc); pred=(23,advmod); text="eee , čeprov smo imel že pred nekej leti , eee , dolo… , eee , predloge celo və , eee , skupš..." |
| 18 | nsubj | advmod | 4 (0.03%) | sid=Gos163.s229; tok=nč#6; gold=(8,nsubj); pred=(8,advmod); text="se ni , se ni nč na premaknl ne na drugo stran ." |
| 19 | orphan | advmod | 4 (0.03%) | sid=Gos170.s131; tok=ponovno#4; gold=(3,orphan); pred=(3,advmod); text="tu zdaj priložnost ponovno , to je Dejvid Hili , Hili ." |
| 20 | discourse | cc | 4 (0.03%) | sid=Gos170.s135; tok=torej#1; gold=(16,discourse); pred=(16,cc); text="torej to , kar nam kaže za zdaj zadnja vrsta Poljakov , ni kdove kako obetavno ." |

### C) HEAD wrong, DEPREL wrong
| Rank | Gold DEPREL | Pred DEPREL | Count | Example |
|---|---|---|---:|---|
| 1 | parataxis | root | 16 (0.14%) | sid=Gos162.s502; tok=šle#11; gold=(4,parataxis); pred=(0,root); text="če bota sveda šla vidva , če ne , ojo… šle punce , al ?" |
| 2 | obl | nmod | 16 (0.14%) | sid=Gos206.s133; tok=internet#3; gold=(1,obl); pred=(4,nmod); text="grete na internet stran Nep , Nacionalna energetska pot , lahko jo takoj odtipkajte , če ste ..." |
| 3 | root | parataxis | 14 (0.12%) | sid=Gos163.s221; tok=dobil#4; gold=(0,root); pred=(1,parataxis); text="dobimo , boste dobil kom… , konja ." |
| 4 | nmod | obl | 14 (0.12%) | sid=Gos165.s185; tok=ruzakom#28; gold=(25,nmod); pred=(29,obl); text="no , in potem so , eee , na Kranjski koči na Ledinah jim je ravnokar odpovedala oskrbnica in ..." |
| 5 | conj | parataxis | 13 (0.11%) | sid=Gos171.s268; tok=okrnil#24; gold=(3,conj); pred=(22,parataxis); text="to je tekma , ki jo seveda morejo dobiti , toda ta poraz , že drugi na gostovanju , bi precej..." |
| 6 | parataxis | conj | 10 (0.09%) | sid=Gos206.s138; tok=odprejo#46; gold=(31,parataxis); pred=(2,conj); text="iskalnik je po krajih , po imenih , po , po , po , po ukrepih , ne , in tam lahko , če grete ..." |
| 7 | parataxis | acl | 8 (0.07%) | sid=Gos216.s237; tok=take#28; gold=(19,parataxis); pred=(16,acl); text="zej , če grema klasična polena reč , potem je takoj , potem je to peč , kjer se zdaj te , ki ..." |
| 8 | reparandum | root | 7 (0.06%) | sid=Gos163.s221; tok=dobimo#1; gold=(4,reparandum); pred=(0,root); text="dobimo , boste dobil kom… , konja ." |
| 9 | orphan | advmod | 7 (0.06%) | sid=Gos193.s140; tok=prej#9; gold=(8,orphan); pred=(13,advmod); text="mene s pinceto ne boli , če jih prej malo neko kremo daš noter , ne ." |
| 10 | parataxis | nsubj | 7 (0.06%) | sid=Gos193.s147; tok=kaj#3; gold=(1,parataxis); pred=(4,nsubj); text="toti , kaj je od , eee ." |
| 11 | reparandum | conj | 7 (0.06%) | sid=Gos216.s231; tok=drve#35; gold=(41,reparandum); pred=(33,conj); text="eee , je , je to v bistvu , eee , tud , eee , v , potrebno met dost izolirano hišo al je to b..." |
| 12 | root | obl | 6 (0.05%) | sid=Gos162.s501; tok=tega#10; gold=(0,root); pred=(8,obl); text="t… , tud , mogoč , tud mogoč zarad tega , čevta čevta res šla vidva v dvoboj , da maš pač ti ..." |
| 13 | advcl | acl | 6 (0.05%) | sid=Gos162.s501; tok=šla#15; gold=(21,advcl); pred=(10,acl); text="t… , tud , mogoč , tud mogoč zarad tega , čevta čevta res šla vidva v dvoboj , da maš pač ti ..." |
| 14 | appos | obl | 6 (0.05%) | sid=Gos206.s133; tok=stran#4; gold=(3,appos); pred=(1,obl); text="grete na internet stran Nep , Nacionalna energetska pot , lahko jo takoj odtipkajte , če ste ..." |
| 15 | appos | parataxis | 6 (0.05%) | sid=Gos216.s231; tok=olju#33; gold=(28,appos); pred=(27,parataxis); text="eee , je , je to v bistvu , eee , tud , eee , v , potrebno met dost izolirano hišo al je to b..." |
| 16 | cop | parataxis | 6 (0.05%) | sid=Gos216.s237; tok=je#14; gold=(16,cop); pred=(10,parataxis); text="zej , če grema klasična polena reč , potem je takoj , potem je to peč , kjer se zdaj te , ki ..." |
| 17 | fixed | advmod | 5 (0.04%) | sid=Gos171.s260; tok=že#3; gold=(1,fixed); pred=(2,advmod); text="kakorkol kakorkol že , druga menjava pri Poljakih ." |
| 18 | ccomp | parataxis | 5 (0.04%) | sid=Gos179.s165; tok=kaj#12; gold=(7,ccomp); pred=(6,parataxis); text="to bi blo tud pol zanimiv pogleat naprej , ne , kaj so to za eni ." |
| 19 | reparandum | orphan | 5 (0.04%) | sid=Gos189.s53; tok=pa#2; gold=(4,reparandum); pred=(1,orphan); text="zdaj pa , pa to sonce in toplo vreme zunaj in zdaj pa" |
| 20 | advmod | reparandum | 4 (0.03%) | sid=Gos162.s501; tok=tud#3; gold=(5,advmod); pred=(8,reparandum); text="t… , tud , mogoč , tud mogoč zarad tega , čevta čevta res šla vidva v dvoboj , da maš pač ti ..." |

## CLASSLA aligned - error content tables
- Compared tokens: 11443
- LAS-correct tokens: 8463 (73.96%)

### A) HEAD wrong, DEPREL correct
| Rank | Gold DEPREL | Pred DEPREL | Count | Example |
|---|---|---|---:|---|
| 1 | punct | (same DEPREL, wrong HEAD) | 453 (3.96%) | sid=Gos160.s163; tok=.#7; gold=(1,punct); pred=(4,punct); text="to pa kr lohk z roko ." |
| 2 | discourse | (same DEPREL, wrong HEAD) | 187 (1.63%) | sid=Gos160.s153; tok=ne#8; gold=(5,discourse); pred=(2,discourse); text="sam tok , da zadiši vino , ne ." |
| 3 | advmod | (same DEPREL, wrong HEAD) | 163 (1.42%) | sid=Gos160.s158; tok=še#3; gold=(5,advmod); pred=(4,advmod); text="marinado sva še prej ohladila , bog ne dej , da date toplo gor ." |
| 4 | conj | (same DEPREL, wrong HEAD) | 96 (0.84%) | sid=Gos163.s224; tok=in#19; gold=(7,conj); pred=(15,conj); text="e , je pa tako , dal sem mu tud druge naloge , ker morjo bit opravljene , in" |
| 5 | parataxis | (same DEPREL, wrong HEAD) | 78 (0.68%) | sid=Gos162.s496; tok=šibicam#13; gold=(3,parataxis); pred=(7,parataxis); text="jz ne vem , kk ti zbral , ne , mogoče po šibicam , ne ." |
| 6 | cc | (same DEPREL, wrong HEAD) | 54 (0.47%) | sid=Gos165.s185; tok=in#31; gold=(41,cc); pred=(33,cc); text="no , in potem so , eee , na Kranjski koči na Ledinah jim je ravnokar odpovedala oskrbnica in ..." |
| 7 | mark | (same DEPREL, wrong HEAD) | 45 (0.39%) | sid=Gos162.s502; tok=če#7; gold=(11,mark); pred=(8,mark); text="če bota sveda šla vidva , če ne , ojo… šle punce , al ?" |
| 8 | nsubj | (same DEPREL, wrong HEAD) | 44 (0.38%) | sid=Gos162.s499; tok=[name:personal]#1; gold=(7,nsubj); pred=(4,nsubj); text="[name:personal] je pač mogoč teti tedn izrazu željo , da bi pač rad bolj pomagal pr žvalih , ..." |
| 9 | obl | (same DEPREL, wrong HEAD) | 39 (0.34%) | sid=Gos165.s178; tok=potovanje#11; gold=(9,obl); pred=(8,obl); text="no , po gimnaziji si si zlo želela it na potovanje po Španiji ." |
| 10 | aux | (same DEPREL, wrong HEAD) | 30 (0.26%) | sid=Gos165.s185; tok=sem#32; gold=(41,aux); pred=(33,aux); text="no , in potem so , eee , na Kranjski koči na Ledinah jim je ravnokar odpovedala oskrbnica in ..." |
| 11 | nmod | (same DEPREL, wrong HEAD) | 29 (0.25%) | sid=Gos165.s180; tok=Jezerskim#11; gold=(7,nmod); pred=(9,nmod); text="in si služla dnar v gorski koči na Ledinah nad Jezerskim , kako si zašla tja , ljubezen do go..." |
| 12 | case | (same DEPREL, wrong HEAD) | 26 (0.23%) | sid=Gos165.s194; tok=po#10; gold=(12,case); pred=(13,case); text="in mi je vsako jutro že za zajtrk skuhala po ene pet jajc pa masonek ." |
| 13 | obj | (same DEPREL, wrong HEAD) | 24 (0.21%) | sid=Gos162.s499; tok=željo#8; gold=(7,obj); pred=(4,obj); text="[name:personal] je pač mogoč teti tedn izrazu željo , da bi pač rad bolj pomagal pr žvalih , ..." |
| 14 | advcl | (same DEPREL, wrong HEAD) | 24 (0.21%) | sid=Gos163.s226; tok=naroču#5; gold=(8,advcl); pred=(19,advcl); text="tako ko sem mu naroču , taku je treba to nardit , eee , sem mu vse lepo povedu in razložu , e..." |
| 15 | acl | (same DEPREL, wrong HEAD) | 24 (0.21%) | sid=Gos216.s237; tok=se#19; gold=(16,acl); pred=(28,acl); text="zej , če grema klasična polena reč , potem je takoj , potem je to peč , kjer se zdaj te , ki ..." |
| 16 | expl | (same DEPREL, wrong HEAD) | 16 (0.14%) | sid=Gos163.s229; tok=se#4; gold=(8,expl); pred=(5,expl); text="se ni , se ni nč na premaknl ne na drugo stran ." |
| 17 | cop | (same DEPREL, wrong HEAD) | 16 (0.14%) | sid=Gos171.s270; tok=je#4; gold=(2,cop); pred=(6,cop); text="novi predsednik zveze je legendarni Gžegorž Lato ." |
| 18 | amod | (same DEPREL, wrong HEAD) | 9 (0.08%) | sid=Artur-J-Gvecg-P500028.s156-s159_reseg.227; tok=devetnajsto#3; gold=(2,amod); pred=(4,amod); text="tud leta devetnajsto dvandvejsət , tko kot je prej omenjal robote , al pa recimo , če omenim ..." |
| 19 | reparandum | (same DEPREL, wrong HEAD) | 8 (0.07%) | sid=Gos163.s229; tok=ni#2; gold=(8,reparandum); pred=(5,reparandum); text="se ni , se ni nč na premaknl ne na drugo stran ." |
| 20 | det | (same DEPREL, wrong HEAD) | 8 (0.07%) | sid=Artur-J-Gvecg-P500014.s186-s189_reseg.81; tok=ta#8; gold=(12,det); pred=(9,det); text="eee In seveda , eem kako prenest ta nš eee rehabilitacijski program , ki je pač prvi te vrste..." |

### B) HEAD correct, DEPREL wrong
| Rank | Gold DEPREL | Pred DEPREL | Count | Example |
|---|---|---|---:|---|
| 1 | advmod | nsubj | 42 (0.37%) | sid=Gos162.s501; tok=lah#27; gold=(31,advmod); pred=(31,nsubj); text="t… , tud , mogoč , tud mogoč zarad tega , čevta čevta res šla vidva v dvoboj , da maš pač ti ..." |
| 2 | appos | conj | 19 (0.17%) | sid=Gos216.s231; tok=olju#33; gold=(28,appos); pred=(28,conj); text="eee , je , je to v bistvu , eee , tud , eee , v , potrebno met dost izolirano hišo al je to b..." |
| 3 | det | amod | 16 (0.14%) | sid=Gos165.s184; tok=kešnga#15; gold=(16,det); pred=(16,amod); text="no , in sem poklicala na vsa planinska društva , če potrebujejo koga , kešnga prostovoljca ." |
| 4 | advmod | obj | 14 (0.12%) | sid=Gos160.s150; tok=nč#1; gold=(3,advmod); pred=(3,obj); text="nč ne solimo ." |
| 5 | advmod | orphan | 13 (0.11%) | sid=Gos162.s501; tok=pač#22; gold=(21,advmod); pred=(21,orphan); text="t… , tud , mogoč , tud mogoč zarad tega , čevta čevta res šla vidva v dvoboj , da maš pač ti ..." |
| 6 | obj | nsubj | 13 (0.11%) | sid=Gos165.s176; tok=to#5; gold=(7,obj); pred=(7,nsubj); text="mogoče tvoja prijatlca [name:personal] to bolj ve ." |
| 7 | obl | obj | 12 (0.10%) | sid=Gos160.s165; tok=hladilnik#3; gold=(1,obl); pred=(1,obj); text="gre u hladilnik za čez noč ." |
| 8 | conj | parataxis | 12 (0.10%) | sid=Gos165.s187; tok=pestro#24; gold=(4,conj); pred=(4,parataxis); text="od teh plinskih bomb , k jih je blo treba neki tkole šravfat , pa vse živo , skratka , blo je..." |
| 9 | advmod | amod | 11 (0.10%) | sid=Gos160.s153; tok=sam#1; gold=(2,advmod); pred=(2,amod); text="sam tok , da zadiši vino , ne ." |
| 10 | mark | advmod | 11 (0.10%) | sid=Gos189.s51; tok=kr#1; gold=(8,mark); pred=(8,advmod); text="kr vse leto sem bla tak lepo zbrana , devet skoz povprečje in vse skupaj ." |
| 11 | parataxis | conj | 10 (0.09%) | sid=Gos160.s157; tok=zloženi#5; gold=(3,parataxis); pred=(3,conj); text="piščanci so prpravljeni , zloženi ." |
| 12 | nummod | det | 10 (0.09%) | sid=Gos165.s185; tok=en#36; gold=(37,nummod); pred=(37,det); text="no , in potem so , eee , na Kranjski koči na Ledinah jim je ravnokar odpovedala oskrbnica in ..." |
| 13 | discourse | advmod | 10 (0.09%) | sid=Artur-J-Gvecg-P500014.s193-s197_reseg.83; tok=pač#33; gold=(34,discourse); pred=(34,advmod); text="eee Namreč eem ta program ma tri module : prehranski , fizikalni in pa psiho-socialni modul ,..." |
| 14 | nsubj | obj | 9 (0.08%) | sid=Gos160.s151; tok=jest#1; gold=(3,nsubj); pred=(3,obj); text="jest bom dal pa še mejčken timijana ." |
| 15 | obj | iobj | 9 (0.08%) | sid=Artur-J-Gvecg-P500014.s229-s232_reseg.91; tok=nam#15; gold=(20,obj); pred=(20,iobj); text="eee Tko kot ste že vi prej omenil , eee pa in tako kot nam vedno naši strokovnjaki zdravstven..." |
| 16 | orphan | advmod | 8 (0.07%) | sid=Gos160.s162; tok=čez#6; gold=(5,orphan); pred=(5,advmod); text="aha , in to zelenjavo čez ." |
| 17 | iobj | obj | 8 (0.07%) | sid=Gos162.s503; tok=meni#16; gold=(18,iobj); pred=(18,obj); text="a no , dej , veš , kdo bo šel na dvoboj , kaj ti meni zdaj govoriš ?" |
| 18 | fixed | nmod | 8 (0.07%) | sid=Artur-J-Gvecg-P500014.s178-s182_reseg.79; tok=ane#14; gold=(13,fixed); pred=(13,nmod); text="eee Ja , tako je , ko se je že nakazovalo , ane ane , da bo pač epidemija prišla iz tujine tu..." |
| 19 | reparandum | amod | 8 (0.07%) | sid=Artur-J-Gvecg-P500014.s237-s244_reseg.93; tok=pozitivnem#50; gold=(54,reparandum); pred=(54,amod); text="eee Tukej jih je profesor Zver informiral , kako poteka eee zdravljenje v tem času , eee kako..." |
| 20 | advmod | cc | 8 (0.07%) | sid=Artur-J-Gvecg-P500054.s7-s13_reseg.425; tok=pa#31; gold=(44,advmod); pred=(44,cc); text="in kot je deklarativno znano , imamo zakone , e , mamo mednarodne kazalnike , skratka , ampak..." |

### C) HEAD wrong, DEPREL wrong
| Rank | Gold DEPREL | Pred DEPREL | Count | Example |
|---|---|---|---:|---|
| 1 | obl | nmod | 38 (0.33%) | sid=Gos165.s180; tok=koči#7; gold=(3,obl); pred=(4,nmod); text="in si služla dnar v gorski koči na Ledinah nad Jezerskim , kako si zašla tja , ljubezen do go..." |
| 2 | root | parataxis | 23 (0.20%) | sid=Gos163.s217; tok=mogl#6; gold=(0,root); pred=(3,parataxis); text="ki je borte , boste mogl opravt , če boste to nalogo opravl ." |
| 3 | nmod | obl | 23 (0.20%) | sid=Gos165.s185; tok=ruzakom#28; gold=(25,nmod); pred=(29,obl); text="no , in potem so , eee , na Kranjski koči na Ledinah jim je ravnokar odpovedala oskrbnica in ..." |
| 4 | reparandum | conj | 17 (0.15%) | sid=Gos162.s501; tok=mogoč#5; gold=(10,reparandum); pred=(3,conj); text="t… , tud , mogoč , tud mogoč zarad tega , čevta čevta res šla vidva v dvoboj , da maš pač ti ..." |
| 5 | parataxis | root | 17 (0.15%) | sid=Gos162.s502; tok=šle#11; gold=(4,parataxis); pred=(0,root); text="če bota sveda šla vidva , če ne , ojo… šle punce , al ?" |
| 6 | nsubj | root | 17 (0.15%) | sid=Gos171.s270; tok=Gžegorž#6; gold=(2,nsubj); pred=(0,root); text="novi predsednik zveze je legendarni Gžegorž Lato ." |
| 7 | conj | parataxis | 15 (0.13%) | sid=Gos216.s231; tok=podobno#27; gold=(5,conj); pred=(18,parataxis); text="eee , je , je to v bistvu , eee , tud , eee , v , potrebno met dost izolirano hišo al je to b..." |
| 8 | fixed | advmod | 14 (0.12%) | sid=Gos170.s135; tok=kako#15; gold=(14,fixed); pred=(16,advmod); text="torej to , kar nam kaže za zdaj zadnja vrsta Poljakov , ni kdove kako obetavno ." |
| 9 | advmod | root | 12 (0.10%) | sid=Gos162.s499; tok=mogoč#4; gold=(7,advmod); pred=(0,root); text="[name:personal] je pač mogoč teti tedn izrazu željo , da bi pač rad bolj pomagal pr žvalih , ..." |
| 10 | orphan | advmod | 11 (0.10%) | sid=Gos160.s163; tok=pa#2; gold=(1,orphan); pred=(4,advmod); text="to pa kr lohk z roko ." |
| 11 | conj | amod | 11 (0.10%) | sid=Gos165.s193; tok=živahna#8; gold=(3,conj); pred=(7,amod); text="eee , stara osemdeset let , zlo živahna ." |
| 12 | parataxis | conj | 11 (0.10%) | sid=Gos170.s131; tok=Hili#11; gold=(3,parataxis); pred=(8,conj); text="tu zdaj priložnost ponovno , to je Dejvid Hili , Hili ." |
| 13 | reparandum | root | 10 (0.09%) | sid=Gos163.s217; tok=borte#3; gold=(6,reparandum); pred=(0,root); text="ki je borte , boste mogl opravt , če boste to nalogo opravl ." |
| 14 | advmod | parataxis | 10 (0.09%) | sid=Gos165.s193; tok=zlo#7; gold=(8,advmod); pred=(3,parataxis); text="eee , stara osemdeset let , zlo živahna ." |
| 15 | root | cop | 10 (0.09%) | sid=Gos179.s158; tok=je#3; gold=(0,root); pred=(5,cop); text="kje pa je lastniška struktura Dnevnika ?" |
| 16 | obl | conj | 10 (0.09%) | sid=Artur-J-Gvecg-P500014.s193-s197_reseg.83; tok=onlajn#44; gold=(35,obl); pred=(38,conj); text="eee Namreč eem ta program ma tri module : prehranski , fizikalni in pa psiho-socialni modul ,..." |
| 17 | advmod | nmod | 10 (0.09%) | sid=Artur-J-Gvecg-P500028.s121-s124_reseg.219; tok=provzaprov#23; gold=(25,advmod); pred=(22,nmod); text="tko da roboti kot mehanizmi so seveda sposobni marsičesa danes , eee , podprti s senzoriko , ..." |
| 18 | advcl | acl | 9 (0.08%) | sid=Gos162.s501; tok=šla#15; gold=(21,advcl); pred=(10,acl); text="t… , tud , mogoč , tud mogoč zarad tega , čevta čevta res šla vidva v dvoboj , da maš pač ti ..." |
| 19 | parataxis | cop | 9 (0.08%) | sid=Gos213.s78; tok=je#30; gold=(7,parataxis); pred=(31,cop); text="aha , kul , eee , čaki , še kako vprašanje , eee , to pa , eee , če , če nabavim to , mate k…..." |
| 20 | nsubj | parataxis | 9 (0.08%) | sid=Artur-J-Gvecg-P500014.s217_reseg.89; tok=moduli#12; gold=(10,nsubj); pred=(7,parataxis); text="eee V bistvu to je spletna stran , tukej so trije moduli : prehranski , psiho-socialni in pa ..." |

## Direct model comparison (LAS exact)
- Compared tokens: 11443
- Trankit aligned correct, CLASSLA aligned wrong: 1652 (14.44%)
- Trankit aligned wrong, CLASSLA aligned correct: 530 (4.63%)

### Where Trankit aligned is better
| Rank | Gold DEPREL | Loser error pattern | Count | Example |
|---|---|---|---:|---|
| 1 | punct | HEAD wrong, DEPREL punct | 231 (2.02%) | sid=Gos160.s163; tok=.#7; gold=(1,punct); trankit=(1,punct); classla=(4,punct); text="to pa kr lohk z roko ." |
| 2 | advmod | HEAD wrong, DEPREL advmod | 100 (0.87%) | sid=Gos160.s166; tok=tud#5; gold=(7,advmod); trankit=(7,advmod); classla=(6,advmod); text="temu bi lohk reku tud pijani piščanec ." |
| 3 | discourse | HEAD wrong, DEPREL discourse | 96 (0.84%) | sid=Gos160.s153; tok=ne#8; gold=(5,discourse); trankit=(5,discourse); classla=(2,discourse); text="sam tok , da zadiši vino , ne ." |
| 4 | conj | HEAD wrong, DEPREL conj | 40 (0.35%) | sid=Gos165.s187; tok=živo#17; gold=(4,conj); trankit=(4,conj); classla=(9,conj); text="od teh plinskih bomb , k jih je blo treba neki tkole šravfat , pa vse živo , skratka , blo je..." |
| 5 | advmod | DEPREL advmod->nsubj, HEAD ok | 36 (0.31%) | sid=Gos162.s501; tok=lah#27; gold=(31,advmod); trankit=(31,advmod); classla=(31,nsubj); text="t… , tud , mogoč , tud mogoč zarad tega , čevta čevta res šla vidva v dvoboj , da maš pač ti ..." |
| 6 | cc | HEAD wrong, DEPREL cc | 36 (0.31%) | sid=Gos165.s185; tok=in#31; gold=(41,cc); trankit=(41,cc); classla=(33,cc); text="no , in potem so , eee , na Kranjski koči na Ledinah jim je ravnokar odpovedala oskrbnica in ..." |
| 7 | parataxis | HEAD wrong, DEPREL parataxis | 31 (0.27%) | sid=Gos162.s496; tok=šibicam#13; gold=(3,parataxis); trankit=(3,parataxis); classla=(7,parataxis); text="jz ne vem , kk ti zbral , ne , mogoče po šibicam , ne ." |
| 8 | mark | HEAD wrong, DEPREL mark | 29 (0.25%) | sid=Gos216.s237; tok=kjer#45; gold=(48,mark); trankit=(48,mark); classla=(46,mark); text="zej , če grema klasična polena reč , potem je takoj , potem je to peč , kjer se zdaj te , ki ..." |
| 9 | obl | HEAD wrong + DEPREL obl->nmod | 28 (0.24%) | sid=Gos165.s180; tok=koči#7; gold=(3,obl); trankit=(3,obl); classla=(4,nmod); text="in si služla dnar v gorski koči na Ledinah nad Jezerskim , kako si zašla tja , ljubezen do go..." |
| 10 | obl | HEAD wrong, DEPREL obl | 26 (0.23%) | sid=Gos165.s178; tok=potovanje#11; gold=(9,obl); trankit=(9,obl); classla=(8,obl); text="no , po gimnaziji si si zlo želela it na potovanje po Španiji ." |
| 11 | nsubj | HEAD wrong, DEPREL nsubj | 26 (0.23%) | sid=Gos179.s168; tok=to#1; gold=(3,nsubj); trankit=(3,nsubj); classla=(2,nsubj); text="to je [name:surname] , naprej ." |
| 12 | case | HEAD wrong, DEPREL case | 22 (0.19%) | sid=Gos216.s229; tok=za#1; gold=(3,case); trankit=(3,case); classla=(2,case); text="za vse skupno je pa ekonomika tista , ki vam to določa ." |
| 13 | obj | HEAD wrong, DEPREL obj | 20 (0.17%) | sid=Gos162.s501; tok=prednost#24; gold=(21,obj); trankit=(21,obj); classla=(15,obj); text="t… , tud , mogoč , tud mogoč zarad tega , čevta čevta res šla vidva v dvoboj , da maš pač ti ..." |
| 14 | aux | HEAD wrong, DEPREL aux | 20 (0.17%) | sid=Gos165.s185; tok=sem#32; gold=(41,aux); trankit=(41,aux); classla=(33,aux); text="no , in potem so , eee , na Kranjski koči na Ledinah jim je ravnokar odpovedala oskrbnica in ..." |
| 15 | nsubj | HEAD wrong + DEPREL nsubj->root | 15 (0.13%) | sid=Gos171.s270; tok=Gžegorž#6; gold=(2,nsubj); trankit=(2,nsubj); classla=(0,root); text="novi predsednik zveze je legendarni Gžegorž Lato ." |
| 16 | root | HEAD wrong + DEPREL root->parataxis | 14 (0.12%) | sid=Gos163.s217; tok=mogl#6; gold=(0,root); trankit=(0,root); classla=(3,parataxis); text="ki je borte , boste mogl opravt , če boste to nalogo opravl ." |
| 17 | advcl | HEAD wrong, DEPREL advcl | 14 (0.12%) | sid=Gos165.s182; tok=hočem#12; gold=(6,advcl); trankit=(6,advcl); classla=(16,advcl); text="in sem rekla , zdej moram pa neki zaslužit , ker hočem v Španijo , hočem v tujino , neki hoče..." |
| 18 | det | DEPREL det->amod, HEAD ok | 14 (0.12%) | sid=Gos165.s184; tok=kešnga#15; gold=(16,det); trankit=(16,det); classla=(16,amod); text="no , in sem poklicala na vsa planinska društva , če potrebujejo koga , kešnga prostovoljca ." |
| 19 | nmod | HEAD wrong, DEPREL nmod | 14 (0.12%) | sid=Gos170.s139; tok=reprezentance#11; gold=(8,nmod); trankit=(8,nmod); classla=(10,nmod); text="tu Dejvid Hili in Najdžl Vrfingtn , menedžer oziroma selektor reprezentance ." |
| 20 | expl | HEAD wrong, DEPREL expl | 13 (0.11%) | sid=Gos163.s229; tok=se#4; gold=(8,expl); trankit=(8,expl); classla=(5,expl); text="se ni , se ni nč na premaknl ne na drugo stran ." |

### Where Trankit aligned loses to CLASSLA aligned
| Rank | Gold DEPREL | Loser error pattern | Count | Example |
|---|---|---|---:|---|
| 1 | punct | HEAD wrong, DEPREL punct | 125 (1.09%) | sid=Gos160.s153; tok=.#9; gold=(2,punct); trankit=(5,punct); classla=(2,punct); text="sam tok , da zadiši vino , ne ." |
| 2 | advmod | HEAD wrong, DEPREL advmod | 44 (0.38%) | sid=Gos163.s226; tok=lih#27; gold=(29,advmod); trankit=(28,advmod); classla=(29,advmod); text="tako ko sem mu naroču , taku je treba to nardit , eee , sem mu vse lepo povedu in razložu , e..." |
| 3 | discourse | HEAD wrong, DEPREL discourse | 38 (0.33%) | sid=Gos162.s496; tok=ne#9; gold=(7,discourse); trankit=(3,discourse); classla=(7,discourse); text="jz ne vem , kk ti zbral , ne , mogoče po šibicam , ne ." |
| 4 | conj | HEAD wrong, DEPREL conj | 24 (0.21%) | sid=Gos206.s139; tok=lastnika#13; gold=(8,conj); trankit=(11,conj); classla=(8,conj); text="in tam dobite naslove in pokličete nekega gospoda al pa gospo oziroma lastnika te hiše , ga p..." |
| 5 | obl | HEAD wrong, DEPREL obl | 17 (0.15%) | sid=Gos179.s171; tok=tega#12; gold=(7,obl); trankit=(4,obl); classla=(7,obl); text="ja , sam vprašanje , kdo je to v resnici izza tega , ne ." |
| 6 | nsubj | HEAD wrong, DEPREL nsubj | 16 (0.14%) | sid=Gos165.s192; tok=kuharca#8; gold=(10,nsubj); trankit=(4,nsubj); classla=(10,nsubj); text="ja , res je , eee , kuharca je bla z Loma nad Tržičem ." |
| 7 | cc | HEAD wrong, DEPREL cc | 13 (0.11%) | sid=Gos165.s185; tok=in#3; gold=(17,cc); trankit=(5,cc); classla=(17,cc); text="no , in potem so , eee , na Kranjski koči na Ledinah jim je ravnokar odpovedala oskrbnica in ..." |
| 8 | obj | HEAD wrong, DEPREL obj | 10 (0.09%) | sid=Gos165.s187; tok=jih#7; gold=(9,obj); trankit=(13,obj); classla=(9,obj); text="od teh plinskih bomb , k jih je blo treba neki tkole šravfat , pa vse živo , skratka , blo je..." |
| 9 | parataxis | HEAD wrong, DEPREL parataxis | 9 (0.08%) | sid=Gos193.s143; tok=recimo#11; gold=(18,parataxis); trankit=(9,parataxis); classla=(18,parataxis); text="al pa recimer , eee , tud kako voskanje , recimo , z onim , naj bi bolele , ne ." |
| 10 | amod | HEAD wrong, DEPREL amod | 9 (0.08%) | sid=Gos216.s237; tok=klasična#5; gold=(6,amod); trankit=(7,amod); classla=(6,amod); text="zej , če grema klasična polena reč , potem je takoj , potem je to peč , kjer se zdaj te , ki ..." |
| 11 | acl | HEAD wrong, DEPREL acl | 9 (0.08%) | sid=Artur-N-G6007-P600702.s24-s43_reseg.1437; tok=prikazani#188; gold=(175,acl); trankit=(16,acl); classla=(175,acl); text="provzaprov gre za domišljijsko zgodbo , kjer , e , provzaprov poteka , eem , borba za , e , p..." |
| 12 | cop | HEAD wrong, DEPREL cop | 8 (0.07%) | sid=Gos216.s238; tok=so#8; gold=(11,cop); trankit=(10,cop); classla=(11,cop); text="se pravi , da je to , so zelo učinkovite peči na polena , ki imajo , ki , mmm , rečmo tem naj..." |
| 13 | case | HEAD wrong, DEPREL case | 7 (0.06%) | sid=Gos206.s133; tok=na#2; gold=(3,case); trankit=(4,case); classla=(3,case); text="grete na internet stran Nep , Nacionalna energetska pot , lahko jo takoj odtipkajte , če ste ..." |
| 14 | mark | HEAD wrong, DEPREL mark | 7 (0.06%) | sid=Gos216.s237; tok=kjer#18; gold=(19,mark); trankit=(28,mark); classla=(19,mark); text="zej , če grema klasična polena reč , potem je takoj , potem je to peč , kjer se zdaj te , ki ..." |
| 15 | obl | HEAD wrong + DEPREL obl->nmod | 6 (0.05%) | sid=Gos206.s133; tok=internet#3; gold=(1,obl); trankit=(4,nmod); classla=(1,obl); text="grete na internet stran Nep , Nacionalna energetska pot , lahko jo takoj odtipkajte , če ste ..." |
| 16 | nmod | HEAD wrong, DEPREL nmod | 6 (0.05%) | sid=Artur-J-Gvecg-P500054.s89-s90_reseg.454; tok=Slovenije#11; gold=(10,nmod); trankit=(9,nmod); classla=(10,nmod); text="eee , najprej , e , hvala Zvezi prijatəljəv mladine Slovenije za pobudo za tole srečanje ." |
| 17 | advcl | HEAD wrong, DEPREL advcl | 5 (0.04%) | sid=Gos163.s217; tok=opravl#13; gold=(6,advcl); trankit=(7,advcl); classla=(6,advcl); text="ki je borte , boste mogl opravt , če boste to nalogo opravl ." |
| 18 | root | HEAD wrong + DEPREL root->obl | 5 (0.04%) | sid=Gos179.s177; tok=internetu#3; gold=(0,root); trankit=(1,obl); classla=(0,root); text="mau po internetu , če je ." |
| 19 | nmod | HEAD wrong + DEPREL nmod->obl | 5 (0.04%) | sid=Artur-J-Gvecg-P500028.s114-s116_reseg.217; tok=področju#16; gold=(14,nmod); trankit=(12,obl); classla=(14,nmod); text="eee , in , eee , mogoče , če kər takoj omenim to temo na področju kemičnega orožja , obstajaj..." |
| 20 | parataxis | DEPREL parataxis->conj, HEAD ok | 4 (0.03%) | sid=Gos206.s139; tok=pokličete#18; gold=(3,parataxis); trankit=(3,conj); classla=(3,parataxis); text="in tam dobite naslove in pokličete nekega gospoda al pa gospo oziroma lastnika te hiše , ga p..." |
