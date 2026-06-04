# Table-style content comparison (Trankit aligned vs CLASSLA aligned)

Columns 7-8 are compared directly (HEAD and DEPREL), with concrete token examples.

## Scope
- Gold sentences: 432
- Trankit aligned sentences: 432
- CLASSLA aligned sentences: 432

## Trankit aligned - error content tables
- Compared tokens: 11443
- LAS-correct tokens: 9939 (86.86%)

### A) HEAD wrong, DEPREL correct
| Rank | Gold DEPREL | Pred DEPREL | Count | Example |
|---|---|---|---:|---|
| 1 | punct | (same DEPREL, wrong HEAD) | 308 (2.69%) | sid=Gos162.s501; tok=,#4; gold=(3,punct); pred=(5,punct); text="t- , tudi , mogoče , tudi mogoče zaradi tega , če bosta res šla vidva v dvoboj , da imaš pač ..." |
| 2 | discourse | (same DEPREL, wrong HEAD) | 123 (1.07%) | sid=Gos160.s153; tok=ne#8; gold=(5,discourse); pred=(2,discourse); text="samo toliko , da zadiši vino , ne ." |
| 3 | advmod | (same DEPREL, wrong HEAD) | 80 (0.70%) | sid=Gos160.s151; tok=še#5; gold=(6,advmod); pred=(7,advmod); text="jaz bom dal pa še majčkeno timijana ." |
| 4 | conj | (same DEPREL, wrong HEAD) | 67 (0.59%) | sid=Gos163.s224; tok=in#19; gold=(7,conj); pred=(3,conj); text="e , je pa tako , dal sem mu tudi druge naloge , ker morajo biti opravljene , in" |
| 5 | parataxis | (same DEPREL, wrong HEAD) | 62 (0.54%) | sid=Gos163.s226; tok=povedal#19; gold=(8,parataxis); pred=(5,parataxis); text="tako kot sem mu naročil , tako je treba to narediti , eee , sem mu vse lepo povedal in razlož..." |
| 6 | reparandum | (same DEPREL, wrong HEAD) | 39 (0.34%) | sid=Gos162.s501; tok=t-#1; gold=(5,reparandum); pred=(3,reparandum); text="t- , tudi , mogoče , tudi mogoče zaradi tega , če bosta res šla vidva v dvoboj , da imaš pač ..." |
| 7 | obl | (same DEPREL, wrong HEAD) | 23 (0.20%) | sid=Gos165.s178; tok=gimnaziji#4; gold=(8,obl); pred=(9,obl); text="no , po gimnaziji si si zelo želela iti na potovanje po Španiji ." |
| 8 | cc | (same DEPREL, wrong HEAD) | 21 (0.18%) | sid=Gos165.s185; tok=in#3; gold=(17,cc); pred=(5,cc); text="no , in potem so , eee , na Kranjski koči na Ledinah jim je ravnokar odpovedala oskrbnica in ..." |
| 9 | mark | (same DEPREL, wrong HEAD) | 18 (0.16%) | sid=Gos162.s502; tok=če#7; gold=(11,mark); pred=(8,mark); text="če bosta seveda šla vidva , če ne , bojo šle punce , ali ?" |
| 10 | nsubj | (same DEPREL, wrong HEAD) | 18 (0.16%) | sid=Gos171.s268; tok=poraz#13; gold=(24,nsubj); pred=(22,nsubj); text="to je tekma , ki jo seveda morejo dobiti , toda ta poraz , že drugi na gostovanju , bi precej..." |
| 11 | advcl | (same DEPREL, wrong HEAD) | 15 (0.13%) | sid=Gos163.s217; tok=opravili#13; gold=(6,advcl); pred=(7,advcl); text="ki jo boste , boste mogli opraviti , če boste to nalogo opravili ." |
| 12 | nmod | (same DEPREL, wrong HEAD) | 15 (0.13%) | sid=Gos165.s180; tok=Jezerskim#11; gold=(7,nmod); pred=(9,nmod); text="in si služila denar v gorski koči na Ledinah nad Jezerskim , kako si zašla tja , ljubezen do ..." |
| 13 | acl | (same DEPREL, wrong HEAD) | 14 (0.12%) | sid=Gos216.s237; tok=se#19; gold=(16,acl); pred=(28,acl); text="zdaj , če greva klasična polena reči , potem je takoj , potem je to peč , kjer se zdaj te , k..." |
| 14 | obj | (same DEPREL, wrong HEAD) | 10 (0.09%) | sid=Gos163.s217; tok=jo#2; gold=(7,obj); pred=(3,obj); text="ki jo boste , boste mogli opraviti , če boste to nalogo opravili ." |
| 15 | aux | (same DEPREL, wrong HEAD) | 9 (0.08%) | sid=Gos171.s268; tok=bi#20; gold=(24,aux); pred=(22,aux); text="to je tekma , ki jo seveda morejo dobiti , toda ta poraz , že drugi na gostovanju , bi precej..." |
| 16 | cop | (same DEPREL, wrong HEAD) | 9 (0.08%) | sid=Gos216.s238; tok=so#8; gold=(11,cop); pred=(10,cop); text="se pravi , da je to , so zelo učinkovite peči na polena , ki imajo , ki , mmm , recimo temu n..." |
| 17 | case | (same DEPREL, wrong HEAD) | 7 (0.06%) | sid=Gos165.s194; tok=po#10; gold=(12,case); pred=(13,case); text="in mi je vsako jutro že za zajtrk skuhala po ene pet jajc pa masonek ." |
| 18 | orphan | (same DEPREL, wrong HEAD) | 4 (0.03%) | sid=Gos160.s163; tok=lahko#4; gold=(1,orphan); pred=(6,orphan); text="to pa kar lahko z roko ." |
| 19 | appos | (same DEPREL, wrong HEAD) | 4 (0.03%) | sid=Gos170.s139; tok=menedžer#8; gold=(5,appos); pred=(2,appos); text="tu David Healy in Nigel Worthington , menedžer oziroma selektor reprezentance ." |
| 20 | nummod | (same DEPREL, wrong HEAD) | 3 (0.03%) | sid=Gos179.s156; tok=šestdeset#7; gold=(4,nummod); pred=(6,nummod); text="on je lastnik Podjetja za informiranje šestdeset ." |

### B) HEAD correct, DEPREL wrong
| Rank | Gold DEPREL | Pred DEPREL | Count | Example |
|---|---|---|---:|---|
| 1 | parataxis | conj | 11 (0.10%) | sid=Gos160.s157; tok=zloženi#5; gold=(3,parataxis); pred=(3,conj); text="piščanci so pripravljeni , zloženi ." |
| 2 | conj | parataxis | 9 (0.08%) | sid=Gos165.s187; tok=pestro#24; gold=(4,conj); pred=(4,parataxis); text="od teh plinskih bomb , ki jih je bilo treba nekaj takole šraufati , pa vse živo , skratka , b..." |
| 3 | discourse | advmod | 8 (0.07%) | sid=Gos163.s229; tok=ne#7; gold=(8,discourse); pred=(8,advmod); text="se ni , se ni nič ne premaknilo ne na drugo stran ." |
| 4 | advmod | orphan | 7 (0.06%) | sid=Gos162.s501; tok=mogoče#8; gold=(10,advmod); pred=(10,orphan); text="t- , tudi , mogoče , tudi mogoče zaradi tega , če bosta res šla vidva v dvoboj , da imaš pač ..." |
| 5 | advmod | discourse | 7 (0.06%) | sid=Gos170.s128; tok=jasno#3; gold=(9,advmod); pred=(9,discourse); text="toda , jasno , ob Vidiču in Ferdinandu nima dosti možnosti za igranje ." |
| 6 | orphan | advmod | 7 (0.06%) | sid=Gos170.s131; tok=ponovno#4; gold=(3,orphan); pred=(3,advmod); text="tu zdaj priložnost ponovno , to je David Healy , Healy ." |
| 7 | appos | conj | 7 (0.06%) | sid=Gos171.s261; tok=branilec#8; gold=(5,appos); pred=(5,conj); text="Bartosz Bosacki je izkušen nogometaš , triintridesetletni branilec , ki igra za Lech iz Pozna..." |
| 8 | cc | advmod | 7 (0.06%) | sid=Gos179.s171; tok=samo#3; gold=(4,cc); pred=(4,advmod); text="ja , samo vprašanje , kdo je to v resnici izza tega , ne ." |
| 9 | obj | iobj | 7 (0.06%) | sid=Gos206.s139; tok=ga#20; gold=(21,obj); pred=(21,iobj); text="in tam dobite naslove in pokličete nekega gospoda ali pa gospo oziroma lastnika te hiše , ga ..." |
| 10 | nmod | obl | 6 (0.05%) | sid=Gos163.s226; tok=volno#32; gold=(29,nmod); pred=(29,obl); text="tako kot sem mu naročil , tako je treba to narediti , eee , sem mu vse lepo povedal in razlož..." |
| 11 | parataxis | cc | 6 (0.05%) | sid=Gos216.s233; tok=ali#22; gold=(23,parataxis); pred=(23,cc); text="ne vem , z biomaso je tako , biomaso imate vi zdaj tri vrste , bi rekel , tri vrste , ali ima..." |
| 12 | obj | nsubj | 6 (0.05%) | sid=Gos216.s241; tok=plamen#44; gold=(45,obj); pred=(45,nsubj); text="je tudi vso j- , vse je tudi regulirano temperaturno , imate vse o- , vse senzorje zgoraj in ..." |
| 13 | discourse | cc | 5 (0.04%) | sid=Gos170.s135; tok=torej#1; gold=(16,discourse); pred=(16,cc); text="torej to , kar nam kaže za zdaj zadnja vrsta Poljakov , ni kdove kako obetavno ." |
| 14 | obl | obj | 5 (0.04%) | sid=Artur-J-Gvecg-P500014.s203-s204_reseg.85; tok=vsebine#16; gold=(10,obl); pred=(10,obj); text="to se je dogajalo tedensko , tedensko je vsak prejel po tri različne podporne video vsebine ." |
| 15 | obl | advmod | 5 (0.04%) | sid=Artur-J-Gvecg-P500028.s184-s190_reseg.233; tok=nekaj#87; gold=(85,obl); pred=(85,advmod); text="eee , zdaj zaenkrat je to sicer še mala ekipa , ki je pa naslonjena na ta bistveno večji pogo..." |
| 16 | nsubj | obj | 4 (0.03%) | sid=Gos160.s153; tok=vino#6; gold=(5,nsubj); pred=(5,obj); text="samo toliko , da zadiši vino , ne ." |
| 17 | obl | nmod | 4 (0.03%) | sid=Gos162.s495; tok=igre#16; gold=(15,obl); pred=(15,nmod); text="eno so , eno bojo verjetno poslali domov , no , tudi to je del igre ." |
| 18 | iobj | obj | 4 (0.03%) | sid=Gos165.s185; tok=jim#14; gold=(17,iobj); pred=(17,obj); text="no , in potem so , eee , na Kranjski koči na Ledinah jim je ravnokar odpovedala oskrbnica in ..." |
| 19 | appos | nmod | 4 (0.03%) | sid=Artur-J-Gvecg-P500014.s208-s212_reseg.87; tok=tem#44; gold=(40,appos); pred=(40,nmod); text="eee tako da smo na neki način jim stali ob strani eem ne le skozi ta program rehabilitacije ,..." |
| 20 | conj | appos | 4 (0.03%) | sid=Artur-J-Gvecg-P500028.s173-s176_reseg.230; tok=krogih#41; gold=(31,conj); pred=(31,appos); text="eem , o tem , ja , je bilo nekaj pisanega , tako da se mi zdi , da tisti , ki , ki so v teh ,..." |

### C) HEAD wrong, DEPREL wrong
| Rank | Gold DEPREL | Pred DEPREL | Count | Example |
|---|---|---|---:|---|
| 1 | parataxis | root | 14 (0.12%) | sid=Gos162.s502; tok=šle#11; gold=(4,parataxis); pred=(0,root); text="če bosta seveda šla vidva , če ne , bojo šle punce , ali ?" |
| 2 | root | parataxis | 14 (0.12%) | sid=Gos163.s221; tok=dobil#4; gold=(0,root); pred=(1,parataxis); text="dobimo , boste dobil kom- , konja ." |
| 3 | nmod | obl | 12 (0.10%) | sid=Gos165.s185; tok=ruzakom#28; gold=(25,nmod); pred=(29,obl); text="no , in potem so , eee , na Kranjski koči na Ledinah jim je ravnokar odpovedala oskrbnica in ..." |
| 4 | conj | parataxis | 9 (0.08%) | sid=Gos171.s268; tok=okrnil#24; gold=(3,conj); pred=(22,parataxis); text="to je tekma , ki jo seveda morejo dobiti , toda ta poraz , že drugi na gostovanju , bi precej..." |
| 5 | orphan | advmod | 8 (0.07%) | sid=Gos193.s140; tok=prej#9; gold=(8,orphan); pred=(13,advmod); text="mene s pinceto ne boli , če jih prej malo neko kremo daš noter , ne ." |
| 6 | parataxis | acl | 8 (0.07%) | sid=Gos216.s237; tok=take#28; gold=(19,parataxis); pred=(16,acl); text="zdaj , če greva klasična polena reči , potem je takoj , potem je to peč , kjer se zdaj te , k..." |
| 7 | reparandum | root | 7 (0.06%) | sid=Gos163.s221; tok=dobimo#1; gold=(4,reparandum); pred=(0,root); text="dobimo , boste dobil kom- , konja ." |
| 8 | parataxis | nsubj | 7 (0.06%) | sid=Gos193.s147; tok=kaj#3; gold=(1,parataxis); pred=(4,nsubj); text="ta , kaj je od , eee ." |
| 9 | obl | nmod | 7 (0.06%) | sid=Gos206.s133; tok=internet#3; gold=(1,obl); pred=(4,nmod); text="greste na internet stran Nep , Nacionalna energetska pot , lahko jo takoj odtipkajte , če ste..." |
| 10 | cop | parataxis | 7 (0.06%) | sid=Gos216.s237; tok=je#14; gold=(16,cop); pred=(10,parataxis); text="zdaj , če greva klasična polena reči , potem je takoj , potem je to peč , kjer se zdaj te , k..." |
| 11 | nsubj | root | 6 (0.05%) | sid=Gos216.s238; tok=to#6; gold=(5,nsubj); pred=(0,root); text="se pravi , da je to , so zelo učinkovite peči na polena , ki imajo , ki , mmm , recimo temu n..." |
| 12 | fixed | advmod | 6 (0.05%) | sid=Artur-J-Gvecg-P500014.s233-s236_reseg.92; tok=pa#11; gold=(10,fixed); pred=(13,advmod); text="eee to smo tudi objavljali na socialnih omrežjih eee in pa seveda pošiljali našim članom na p..." |
| 13 | advcl | acl | 5 (0.04%) | sid=Gos162.s501; tok=šla#15; gold=(21,advcl); pred=(10,acl); text="t- , tudi , mogoče , tudi mogoče zaradi tega , če bosta res šla vidva v dvoboj , da imaš pač ..." |
| 14 | appos | obj | 5 (0.04%) | sid=Gos165.s184; tok=prostovoljca#16; gold=(13,appos); pred=(12,obj); text="no , in sem poklicala na vsa planinska društva , če potrebujejo koga , kakšnega prostovoljca ." |
| 15 | reparandum | conj | 5 (0.04%) | sid=Gos216.s231; tok=drva#35; gold=(41,reparandum); pred=(33,conj); text="eee , je , je to v bistvu , eee , tudi , eee , v , potrebno imeti dosti izolirano hišo ali je..." |
| 16 | reparandum | orphan | 4 (0.03%) | sid=Gos189.s53; tok=pa#2; gold=(4,reparandum); pred=(1,orphan); text="zdaj pa , pa to sonce in toplo vreme zunaj in zdaj pa" |
| 17 | root | advmod | 4 (0.03%) | sid=Gos189.s55; tok=noter#1; gold=(0,root); pred=(3,advmod); text="noter pa pisati , pa škoda mi je tega predmeta , ker je ta predmet" |
| 18 | appos | obl | 4 (0.03%) | sid=Gos206.s133; tok=stran#4; gold=(3,appos); pred=(1,obl); text="greste na internet stran Nep , Nacionalna energetska pot , lahko jo takoj odtipkajte , če ste..." |
| 19 | root | cop | 4 (0.03%) | sid=Gos216.s231; tok=je#5; gold=(0,root); pred=(18,cop); text="eee , je , je to v bistvu , eee , tudi , eee , v , potrebno imeti dosti izolirano hišo ali je..." |
| 20 | appos | parataxis | 4 (0.03%) | sid=Gos216.s231; tok=olju#33; gold=(28,appos); pred=(27,parataxis); text="eee , je , je to v bistvu , eee , tudi , eee , v , potrebno imeti dosti izolirano hišo ali je..." |

## CLASSLA aligned - error content tables
- Compared tokens: 11443
- LAS-correct tokens: 7951 (69.48%)

### A) HEAD wrong, DEPREL correct
| Rank | Gold DEPREL | Pred DEPREL | Count | Example |
|---|---|---|---:|---|
| 1 | punct | (same DEPREL, wrong HEAD) | 761 (6.65%) | sid=Gos162.s489; tok=,#10; gold=(9,punct); pred=(11,punct); text="to je igra , ki jo igrajo , eee , ti , eee , člani družine ." |
| 2 | advmod | (same DEPREL, wrong HEAD) | 162 (1.42%) | sid=Gos160.s151; tok=še#5; gold=(6,advmod); pred=(7,advmod); text="jaz bom dal pa še majčkeno timijana ." |
| 3 | conj | (same DEPREL, wrong HEAD) | 82 (0.72%) | sid=Gos163.s224; tok=in#19; gold=(7,conj); pred=(3,conj); text="e , je pa tako , dal sem mu tudi druge naloge , ker morajo biti opravljene , in" |
| 4 | parataxis | (same DEPREL, wrong HEAD) | 77 (0.67%) | sid=Gos163.s226; tok=razočaran#29; gold=(8,parataxis); pred=(19,parataxis); text="tako kot sem mu naročil , tako je treba to narediti , eee , sem mu vse lepo povedal in razlož..." |
| 5 | cc | (same DEPREL, wrong HEAD) | 67 (0.59%) | sid=Gos170.s128; tok=toda#1; gold=(9,cc); pred=(3,cc); text="toda , jasno , ob Vidiču in Ferdinandu nima dosti možnosti za igranje ." |
| 6 | mark | (same DEPREL, wrong HEAD) | 41 (0.36%) | sid=Gos162.s502; tok=če#7; gold=(11,mark); pred=(8,mark); text="če bosta seveda šla vidva , če ne , bojo šle punce , ali ?" |
| 7 | discourse | (same DEPREL, wrong HEAD) | 37 (0.32%) | sid=Gos162.s496; tok=ne#9; gold=(7,discourse); pred=(11,discourse); text="jaz ne vem , kako ti zbral , ne , mogoče po šibicah , ne ." |
| 8 | obl | (same DEPREL, wrong HEAD) | 34 (0.30%) | sid=Gos165.s178; tok=gimnaziji#4; gold=(8,obl); pred=(9,obl); text="no , po gimnaziji si si zelo želela iti na potovanje po Španiji ." |
| 9 | nsubj | (same DEPREL, wrong HEAD) | 33 (0.29%) | sid=Gos162.s499; tok=[name:personal]#1; gold=(7,nsubj); pred=(4,nsubj); text="[name:personal] je pač mogoče ta teden izrazil željo , da bi pač rad bolj pomagal pri živalih..." |
| 10 | case | (same DEPREL, wrong HEAD) | 29 (0.25%) | sid=Gos165.s194; tok=po#10; gold=(12,case); pred=(13,case); text="in mi je vsako jutro že za zajtrk skuhala po ene pet jajc pa masonek ." |
| 11 | acl | (same DEPREL, wrong HEAD) | 26 (0.23%) | sid=Gos216.s238; tok=imajo#16; gold=(11,acl); pred=(13,acl); text="se pravi , da je to , so zelo učinkovite peči na polena , ki imajo , ki , mmm , recimo temu n..." |
| 12 | aux | (same DEPREL, wrong HEAD) | 25 (0.22%) | sid=Gos165.s192; tok=je#9; gold=(10,aux); pred=(8,aux); text="ja , res je , eee , kuharica je bila z Loma nad Tržičem ." |
| 13 | advcl | (same DEPREL, wrong HEAD) | 24 (0.21%) | sid=Gos163.s217; tok=opravili#13; gold=(6,advcl); pred=(7,advcl); text="ki jo boste , boste mogli opraviti , če boste to nalogo opravili ." |
| 14 | nmod | (same DEPREL, wrong HEAD) | 19 (0.17%) | sid=Gos165.s180; tok=Jezerskim#11; gold=(7,nmod); pred=(9,nmod); text="in si služila denar v gorski koči na Ledinah nad Jezerskim , kako si zašla tja , ljubezen do ..." |
| 15 | cop | (same DEPREL, wrong HEAD) | 16 (0.14%) | sid=Gos207.s8; tok=bo#16; gold=(18,cop); pred=(17,cop); text="ja , no , to je pa dobra novica , tako da , da ne bo dolga seansa , ja , ker imamo pol , saj ..." |
| 16 | obj | (same DEPREL, wrong HEAD) | 13 (0.11%) | sid=Gos165.s187; tok=jih#7; gold=(9,obj); pred=(13,obj); text="od teh plinskih bomb , ki jih je bilo treba nekaj takole šraufati , pa vse živo , skratka , b..." |
| 17 | amod | (same DEPREL, wrong HEAD) | 11 (0.10%) | sid=Gos216.s241; tok=potreben#24; gold=(25,amod); pred=(22,amod); text="je tudi vso j- , vse je tudi regulirano temperaturno , imate vse o- , vse senzorje zgoraj in ..." |
| 18 | expl | (same DEPREL, wrong HEAD) | 9 (0.08%) | sid=Gos165.s178; tok=si#6; gold=(8,expl); pred=(9,expl); text="no , po gimnaziji si si zelo želela iti na potovanje po Španiji ." |
| 19 | appos | (same DEPREL, wrong HEAD) | 4 (0.03%) | sid=Gos170.s139; tok=menedžer#8; gold=(5,appos); pred=(2,appos); text="tu David Healy in Nigel Worthington , menedžer oziroma selektor reprezentance ." |
| 20 | csubj | (same DEPREL, wrong HEAD) | 4 (0.03%) | sid=Gos216.s231; tok=imeti#19; gold=(5,csubj); pred=(18,csubj); text="eee , je , je to v bistvu , eee , tudi , eee , v , potrebno imeti dosti izolirano hišo ali je..." |

### B) HEAD correct, DEPREL wrong
| Rank | Gold DEPREL | Pred DEPREL | Count | Example |
|---|---|---|---:|---|
| 1 | discourse | parataxis | 71 (0.62%) | sid=Gos163.s224; tok=e#1; gold=(3,discourse); pred=(3,parataxis); text="e , je pa tako , dal sem mu tudi druge naloge , ker morajo biti opravljene , in" |
| 2 | discourse | nsubj | 56 (0.49%) | sid=Artur-J-Gvecg-P500014.s217_reseg.89; tok=eee#1; gold=(7,discourse); pred=(7,nsubj); text="eee v bistvu to je spletna stran , tukaj so trije moduli : prehranski , psiho-socialni in pa ..." |
| 3 | discourse | vocative | 25 (0.22%) | sid=Gos160.s154; tok=evo#1; gold=(3,discourse); pred=(3,vocative); text="evo , vidiš ." |
| 4 | cc | advmod | 22 (0.19%) | sid=Gos165.s187; tok=pa#15; gold=(17,cc); pred=(17,advmod); text="od teh plinskih bomb , ki jih je bilo treba nekaj takole šraufati , pa vse živo , skratka , b..." |
| 5 | conj | parataxis | 18 (0.16%) | sid=Gos179.s179; tok=vem#12; gold=(4,conj); pred=(4,parataxis); text="neka ista zadeva mora biti kot naš tale , samo ne vem zdaj ." |
| 6 | discourse | advmod | 15 (0.13%) | sid=Gos163.s229; tok=ne#7; gold=(8,discourse); pred=(8,advmod); text="se ni , se ni nič ne premaknilo ne na drugo stran ." |
| 7 | obj | nsubj | 15 (0.13%) | sid=Gos165.s176; tok=to#5; gold=(7,obj); pred=(7,nsubj); text="mogoče tvoja prijateljica [name:personal] to bolj ve ." |
| 8 | discourse | conj | 13 (0.11%) | sid=Gos162.s501; tok=ne#35; gold=(31,discourse); pred=(31,conj); text="t- , tudi , mogoče , tudi mogoče zaradi tega , če bosta res šla vidva v dvoboj , da imaš pač ..." |
| 9 | nmod | conj | 12 (0.10%) | sid=Artur-J-Gvecg-P500028.s181-s183_reseg.232; tok=oddelka#28; gold=(24,nmod); pred=(24,conj); text="eee , zadeva , torej ta center , funkcionira ta moment v okviru Instituta Jožef Stefan kot , ..." |
| 10 | orphan | advmod | 11 (0.10%) | sid=Gos160.s162; tok=čez#6; gold=(5,orphan); pred=(5,advmod); text="aha , in to zelenjavo čez ." |
| 11 | parataxis | conj | 11 (0.10%) | sid=Gos163.s234; tok=moje#5; gold=(2,parataxis); pred=(2,conj); text="po moje , po moje ." |
| 12 | obj | iobj | 11 (0.10%) | sid=Gos165.s177; tok=ti#2; gold=(4,obj); pred=(4,iobj); text="toliko ti je pomenil , no ." |
| 13 | appos | conj | 11 (0.10%) | sid=Artur-J-Gvecg-P500014.s183-s185_reseg.80; tok=živo#27; gold=(24,appos); pred=(24,conj); text="eee tako da smo s kolegi iskal različne načine , a ne , kako prilagoditi predvsem tiste progr..." |
| 14 | det | nummod | 10 (0.09%) | sid=Gos179.s180; tok=eno#24; gold=(26,det); pred=(26,nummod); text="veš , kaj bom danes , eee , zdajle grem , grem , ravno zdajle grem v Zagreb , pa se dobim z e..." |
| 15 | cc | mark | 10 (0.09%) | sid=Gos216.s241; tok=tako#41; gold=(45,cc); pred=(45,mark); text="je tudi vso j- , vse je tudi regulirano temperaturno , imate vse o- , vse senzorje zgoraj in ..." |
| 16 | nsubj | iobj | 9 (0.08%) | sid=Gos162.s496; tok=ti#6; gold=(7,nsubj); pred=(7,iobj); text="jaz ne vem , kako ti zbral , ne , mogoče po šibicah , ne ." |
| 17 | advmod | orphan | 9 (0.08%) | sid=Gos213.s78; tok=pa#16; gold=(15,advmod); pred=(15,orphan); text="aha , kul , eee , čakaj , še kako vprašanje , eee , to pa , eee , če , če nabavim to , imate ..." |
| 18 | nmod | obl | 7 (0.06%) | sid=Gos163.s226; tok=volno#32; gold=(29,nmod); pred=(29,obl); text="tako kot sem mu naročil , tako je treba to narediti , eee , sem mu vse lepo povedal in razlož..." |
| 19 | reparandum | amod | 7 (0.06%) | sid=Artur-J-Gvecg-P500054.s53-s54_reseg.439; tok=nedvla-#5; gold=(6,reparandum); pred=(6,amod); text="seveda , mi kot nedvla- nevladniki , e , se soočamo z dejstvom , da se vlade menjajo , menjaj..." |
| 20 | obl | nmod | 6 (0.05%) | sid=Gos162.s495; tok=igre#16; gold=(15,obl); pred=(15,nmod); text="eno so , eno bojo verjetno poslali domov , no , tudi to je del igre ." |

### C) HEAD wrong, DEPREL wrong
| Rank | Gold DEPREL | Pred DEPREL | Count | Example |
|---|---|---|---:|---|
| 1 | discourse | conj | 124 (1.08%) | sid=Gos162.s489; tok=eee#13; gold=(7,discourse); pred=(11,conj); text="to je igra , ki jo igrajo , eee , ti , eee , člani družine ." |
| 2 | discourse | appos | 84 (0.73%) | sid=Gos162.s489; tok=eee#9; gold=(7,discourse); pred=(3,appos); text="to je igra , ki jo igrajo , eee , ti , eee , člani družine ." |
| 3 | discourse | nmod | 63 (0.55%) | sid=Gos216.s237; tok=eee#33; gold=(38,discourse); pred=(32,nmod); text="zdaj , če greva klasična polena reči , potem je takoj , potem je to peč , kjer se zdaj te , k..." |
| 4 | discourse | parataxis | 28 (0.24%) | sid=Gos160.s153; tok=ne#8; gold=(5,discourse); pred=(2,parataxis); text="samo toliko , da zadiši vino , ne ." |
| 5 | obl | nmod | 26 (0.23%) | sid=Gos165.s180; tok=koči#7; gold=(3,obl); pred=(4,nmod); text="in si služila denar v gorski koči na Ledinah nad Jezerskim , kako si zašla tja , ljubezen do ..." |
| 6 | root | parataxis | 22 (0.19%) | sid=Gos162.s495; tok=poslali#7; gold=(0,root); pred=(1,parataxis); text="eno so , eno bojo verjetno poslali domov , no , tudi to je del igre ." |
| 7 | parataxis | root | 21 (0.18%) | sid=Gos162.s502; tok=šle#11; gold=(4,parataxis); pred=(0,root); text="če bosta seveda šla vidva , če ne , bojo šle punce , ali ?" |
| 8 | discourse | vocative | 20 (0.17%) | sid=Gos163.s226; tok=eee#13; gold=(19,discourse); pred=(5,vocative); text="tako kot sem mu naročil , tako je treba to narediti , eee , sem mu vse lepo povedal in razlož..." |
| 9 | fixed | advmod | 20 (0.17%) | sid=Gos170.s135; tok=kako#15; gold=(14,fixed); pred=(16,advmod); text="torej to , kar nam kaže za zdaj zadnja vrsta Poljakov , ni kdove kako obetavno ." |
| 10 | reparandum | conj | 19 (0.17%) | sid=Gos171.s268; tok=okrnil#22; gold=(24,reparandum); pred=(3,conj); text="to je tekma , ki jo seveda morejo dobiti , toda ta poraz , že drugi na gostovanju , bi precej..." |
| 11 | nsubj | conj | 18 (0.16%) | sid=Gos162.s489; tok=člani#15; gold=(7,nsubj); pred=(11,conj); text="to je igra , ki jo igrajo , eee , ti , eee , člani družine ." |
| 12 | root | cop | 18 (0.16%) | sid=Gos165.s192; tok=je#4; gold=(0,root); pred=(3,cop); text="ja , res je , eee , kuharica je bila z Loma nad Tržičem ." |
| 13 | reparandum | case | 18 (0.16%) | sid=Gos206.s138; tok=po#9; gold=(15,reparandum); pred=(7,case); text="iskalnik je po krajih , po imenih , po , po , po , po ukrepih , ne , in tam lahko , če greste..." |
| 14 | nsubj | parataxis | 17 (0.15%) | sid=Gos165.s192; tok=kuharica#8; gold=(10,nsubj); pred=(6,parataxis); text="ja , res je , eee , kuharica je bila z Loma nad Tržičem ." |
| 15 | nsubj | root | 17 (0.15%) | sid=Gos179.s158; tok=struktura#5; gold=(3,nsubj); pred=(0,root); text="kje pa je lastniška struktura Dnevnika ?" |
| 16 | mark | fixed | 17 (0.15%) | sid=Gos189.s50; tok=da#21; gold=(24,mark); pred=(20,fixed); text="jaz moram res povedati , da bi si želela za ta predmet , da bi enkrat dlje trajal , pa da ne ..." |
| 17 | obl | conj | 17 (0.15%) | sid=Artur-J-Gvecg-P500028.s121-s124_reseg.219; tok=mehanizmi#5; gold=(8,obl); pred=(3,conj); text="tako da roboti kot mehanizmi so seveda sposobni marsičesa danes , eee , podprti s senzoriko ,..." |
| 18 | discourse | cc | 15 (0.13%) | sid=Gos162.s503; tok=a#1; gold=(6,discourse); pred=(4,cc); text="a no , daj , veš , kdo bo šel na dvoboj , kaj ti meni zdaj govoriš ?" |
| 19 | reparandum | advmod | 14 (0.12%) | sid=Artur-J-Gvecg-P500014.s193-s197_reseg.83; tok=skratka#40; gold=(41,reparandum); pred=(42,advmod); text="eee namreč eem ta program ima tri module : prehranski , fizikalni in pa psiho-socialni modul ..." |
| 20 | parataxis | conj | 13 (0.11%) | sid=Gos162.s499; tok=izbral#20; gold=(7,parataxis); pred=(15,conj); text="[name:personal] je pač mogoče ta teden izrazil željo , da bi pač rad bolj pomagal pri živalih..." |

## Direct model comparison (LAS exact)
- Compared tokens: 11443
- Trankit aligned correct, CLASSLA aligned wrong: 2310 (20.19%)
- Trankit aligned wrong, CLASSLA aligned correct: 322 (2.81%)

### Where Trankit aligned is better
| Rank | Gold DEPREL | Loser error pattern | Count | Example |
|---|---|---|---:|---|
| 1 | punct | HEAD wrong, DEPREL punct | 546 (4.77%) | sid=Gos162.s489; tok=,#10; gold=(9,punct); trankit=(9,punct); classla=(11,punct); text="to je igra , ki jo igrajo , eee , ti , eee , člani družine ." |
| 2 | advmod | HEAD wrong, DEPREL advmod | 110 (0.96%) | sid=Gos162.s499; tok=pač#3; gold=(7,advmod); trankit=(7,advmod); classla=(4,advmod); text="[name:personal] je pač mogoče ta teden izrazil željo , da bi pač rad bolj pomagal pri živalih..." |
| 3 | discourse | HEAD wrong + DEPREL discourse->conj | 89 (0.78%) | sid=Gos162.s489; tok=eee#13; gold=(7,discourse); trankit=(7,discourse); classla=(11,conj); text="to je igra , ki jo igrajo , eee , ti , eee , člani družine ." |
| 4 | discourse | HEAD wrong + DEPREL discourse->appos | 72 (0.63%) | sid=Gos162.s489; tok=eee#9; gold=(7,discourse); trankit=(7,discourse); classla=(3,appos); text="to je igra , ki jo igrajo , eee , ti , eee , člani družine ." |
| 5 | discourse | DEPREL discourse->parataxis, HEAD ok | 65 (0.57%) | sid=Gos163.s224; tok=e#1; gold=(3,discourse); trankit=(3,discourse); classla=(3,parataxis); text="e , je pa tako , dal sem mu tudi druge naloge , ker morajo biti opravljene , in" |
| 6 | discourse | DEPREL discourse->nsubj, HEAD ok | 55 (0.48%) | sid=Artur-J-Gvecg-P500014.s217_reseg.89; tok=eee#1; gold=(7,discourse); trankit=(7,discourse); classla=(7,nsubj); text="eee v bistvu to je spletna stran , tukaj so trije moduli : prehranski , psiho-socialni in pa ..." |
| 7 | cc | HEAD wrong, DEPREL cc | 54 (0.47%) | sid=Gos170.s128; tok=toda#1; gold=(9,cc); trankit=(9,cc); classla=(3,cc); text="toda , jasno , ob Vidiču in Ferdinandu nima dosti možnosti za igranje ." |
| 8 | discourse | HEAD wrong + DEPREL discourse->nmod | 48 (0.42%) | sid=Gos216.s237; tok=eee#33; gold=(38,discourse); trankit=(38,discourse); classla=(32,nmod); text="zdaj , če greva klasična polena reči , potem je takoj , potem je to peč , kjer se zdaj te , k..." |
| 9 | conj | HEAD wrong, DEPREL conj | 43 (0.38%) | sid=Gos170.s137; tok=uspelo#23; gold=(10,conj); trankit=(10,conj); classla=(14,conj); text="tudi drugi napadalec , izjemni David Healy , je imel priložnost , da premaga Arturja Boruca ,..." |
| 10 | parataxis | HEAD wrong, DEPREL parataxis | 35 (0.31%) | sid=Gos165.s182; tok=hočem#16; gold=(12,parataxis); trankit=(12,parataxis); classla=(3,parataxis); text="in sem rekla , zdaj moram pa nekaj zaslužiti , ker hočem v Španijo , hočem v tujino , nekaj h..." |
| 11 | mark | HEAD wrong, DEPREL mark | 28 (0.24%) | sid=Gos206.s133; tok=če#16; gold=(17,mark); trankit=(17,mark); classla=(21,mark); text="greste na internet stran Nep , Nacionalna energetska pot , lahko jo takoj odtipkajte , če ste..." |
| 12 | discourse | DEPREL discourse->vocative, HEAD ok | 23 (0.20%) | sid=Gos160.s154; tok=evo#1; gold=(3,discourse); trankit=(3,discourse); classla=(3,vocative); text="evo , vidiš ." |
| 13 | case | HEAD wrong, DEPREL case | 23 (0.20%) | sid=Artur-J-Gvecg-P500014.s213-s216_reseg.88; tok=na#19; gold=(20,case); trankit=(20,case); classla=(21,case); text="eem seveda smo mogli tudi hitro prilagoditi našo spletno stran tega rehabilitacijskega progra..." |
| 14 | discourse | HEAD wrong, DEPREL discourse | 21 (0.18%) | sid=Gos162.s497; tok=ne#3; gold=(1,discourse); trankit=(1,discourse); classla=(5,discourse); text="ne , ne , ne ." |
| 15 | obl | HEAD wrong + DEPREL obl->nmod | 21 (0.18%) | sid=Gos165.s180; tok=koči#7; gold=(3,obl); trankit=(3,obl); classla=(4,nmod); text="in si služila denar v gorski koči na Ledinah nad Jezerskim , kako si zašla tja , ljubezen do ..." |
| 16 | obl | HEAD wrong, DEPREL obl | 21 (0.18%) | sid=Gos165.s192; tok=Loma#12; gold=(10,obl); trankit=(10,obl); classla=(8,obl); text="ja , res je , eee , kuharica je bila z Loma nad Tržičem ." |
| 17 | discourse | HEAD wrong + DEPREL discourse->parataxis | 18 (0.16%) | sid=Gos162.s496; tok=ne#15; gold=(13,discourse); trankit=(13,discourse); classla=(11,parataxis); text="jaz ne vem , kako ti zbral , ne , mogoče po šibicah , ne ." |
| 18 | nsubj | HEAD wrong, DEPREL nsubj | 18 (0.16%) | sid=Gos162.s499; tok=[name:personal]#1; gold=(7,nsubj); trankit=(7,nsubj); classla=(4,nsubj); text="[name:personal] je pač mogoče ta teden izrazil željo , da bi pač rad bolj pomagal pri živalih..." |
| 19 | discourse | HEAD wrong + DEPREL discourse->vocative | 18 (0.16%) | sid=Gos163.s226; tok=eee#13; gold=(19,discourse); trankit=(19,discourse); classla=(5,vocative); text="tako kot sem mu naročil , tako je treba to narediti , eee , sem mu vse lepo povedal in razlož..." |
| 20 | nsubj | HEAD wrong + DEPREL nsubj->conj | 16 (0.14%) | sid=Gos162.s489; tok=člani#15; gold=(7,nsubj); trankit=(7,nsubj); classla=(11,conj); text="to je igra , ki jo igrajo , eee , ti , eee , člani družine ." |

### Where Trankit aligned loses to CLASSLA aligned
| Rank | Gold DEPREL | Loser error pattern | Count | Example |
|---|---|---|---:|---|
| 1 | punct | HEAD wrong, DEPREL punct | 93 (0.81%) | sid=Gos163.s226; tok=,#12; gold=(13,punct); trankit=(8,punct); classla=(13,punct); text="tako kot sem mu naročil , tako je treba to narediti , eee , sem mu vse lepo povedal in razlož..." |
| 2 | advmod | HEAD wrong, DEPREL advmod | 24 (0.21%) | sid=Gos160.s163; tok=kar#3; gold=(6,advmod); trankit=(4,advmod); classla=(6,advmod); text="to pa kar lahko z roko ." |
| 3 | conj | HEAD wrong, DEPREL conj | 21 (0.18%) | sid=Gos207.s8; tok=in#30; gold=(29,conj); trankit=(23,conj); classla=(29,conj); text="ja , no , to je pa dobra novica , tako da , da ne bo dolga seansa , ja , ker imamo pol , saj ..." |
| 4 | parataxis | HEAD wrong, DEPREL parataxis | 10 (0.09%) | sid=Gos193.s142; tok=nič#20; gold=(15,parataxis); trankit=(17,parataxis); classla=(15,parataxis); text="ja , mene pol čisto nič , mene , eee , s pinceto ne boli , oblikovanje , čisto nič ." |
| 5 | obl | HEAD wrong, DEPREL obl | 9 (0.08%) | sid=Gos179.s179; tok=tale#8; gold=(4,obl); trankit=(5,obl); classla=(4,obl); text="neka ista zadeva mora biti kot naš tale , samo ne vem zdaj ." |
| 6 | parataxis | DEPREL parataxis->conj, HEAD ok | 7 (0.06%) | sid=Gos160.s157; tok=zloženi#5; gold=(3,parataxis); trankit=(3,conj); classla=(3,parataxis); text="piščanci so pripravljeni , zloženi ." |
| 7 | mark | HEAD wrong, DEPREL mark | 7 (0.06%) | sid=Gos163.s217; tok=ki#1; gold=(6,mark); trankit=(3,mark); classla=(6,mark); text="ki jo boste , boste mogli opraviti , če boste to nalogo opravili ." |
| 8 | nmod | HEAD wrong + DEPREL nmod->obl | 7 (0.06%) | sid=Artur-J-Gvecg-P500014.s270_reseg.100; tok=sabo#17; gold=(15,nmod); trankit=(11,obl); classla=(15,nmod); text="ampak ti videokonferenčni sistemi so nam omogočali , da smo bili na vezi tako mi med sabo kot..." |
| 9 | cc | HEAD wrong, DEPREL cc | 6 (0.05%) | sid=Gos165.s185; tok=in#3; gold=(17,cc); trankit=(5,cc); classla=(17,cc); text="no , in potem so , eee , na Kranjski koči na Ledinah jim je ravnokar odpovedala oskrbnica in ..." |
| 10 | cop | HEAD wrong + DEPREL cop->parataxis | 6 (0.05%) | sid=Artur-J-Gvecg-P500054.s60-s65_reseg.443; tok=so#26; gold=(27,cop); trankit=(3,parataxis); classla=(27,cop); text="in če nimamo programa z akcijskim načrtom , kjer bi država , bi rekla , naredila neki spisek ..." |
| 11 | discourse | HEAD wrong, DEPREL discourse | 5 (0.04%) | sid=Gos165.s185; tok=no#1; gold=(17,discourse); trankit=(5,discourse); classla=(17,discourse); text="no , in potem so , eee , na Kranjski koči na Ledinah jim je ravnokar odpovedala oskrbnica in ..." |
| 12 | root | HEAD wrong + DEPREL root->parataxis | 5 (0.04%) | sid=Gos165.s185; tok=odpovedala#17; gold=(0,root); trankit=(5,parataxis); classla=(0,root); text="no , in potem so , eee , na Kranjski koči na Ledinah jim je ravnokar odpovedala oskrbnica in ..." |
| 13 | nmod | HEAD wrong, DEPREL nmod | 5 (0.04%) | sid=Artur-J-Gvecg-P500028.s156-s159_reseg.227; tok=Vidu#39; gold=(35,nmod); trankit=(37,nmod); classla=(35,nmod); text="tudi leta devetnajsto dvaindvajset , tako kot je prej omenjal robote , ali pa recimo , če ome..." |
| 14 | nsubj | HEAD wrong, DEPREL nsubj | 4 (0.03%) | sid=Artur-J-Gvecg-P500028.s106-s108_reseg.214; tok=človek#17; gold=(19,nsubj); trankit=(24,nsubj); classla=(19,nsubj); text="pravzaprav to ne vem , če je huda debata , ker je zelo logično , da človek ne poškodu- , da r..." |
| 15 | obj | DEPREL obj->nsubj, HEAD ok | 4 (0.03%) | sid=Artur-J-Gvecg-P500028.s199-s212_reseg.235; tok=GPAI#97; gold=(94,obj); trankit=(94,nsubj); classla=(94,obj); text="eee , no , in preko centra pa tudi sicer preko inštituta , smo pravzaprav vključeni v vse rel..." |
| 16 | obj | HEAD wrong, DEPREL obj | 3 (0.03%) | sid=Gos163.s217; tok=jo#2; gold=(7,obj); trankit=(3,obj); classla=(7,obj); text="ki jo boste , boste mogli opraviti , če boste to nalogo opravili ." |
| 17 | obj | HEAD wrong + DEPREL obj->reparandum | 3 (0.03%) | sid=Gos165.s184; tok=koga#13; gold=(12,obj); trankit=(16,reparandum); classla=(12,obj); text="no , in sem poklicala na vsa planinska društva , če potrebujejo koga , kakšnega prostovoljca ." |
| 18 | obl | HEAD wrong + DEPREL obl->nmod | 3 (0.03%) | sid=Gos206.s133; tok=internet#3; gold=(1,obl); trankit=(4,nmod); classla=(1,obl); text="greste na internet stran Nep , Nacionalna energetska pot , lahko jo takoj odtipkajte , če ste..." |
| 19 | advcl | HEAD wrong, DEPREL advcl | 3 (0.03%) | sid=Gos213.s78; tok=nabavim#23; gold=(26,advcl); trankit=(30,advcl); classla=(26,advcl); text="aha , kul , eee , čakaj , še kako vprašanje , eee , to pa , eee , če , če nabavim to , imate ..." |
| 20 | conj | HEAD wrong + DEPREL conj->parataxis | 3 (0.03%) | sid=Artur-J-Gvecg-P500054.s58-s59_reseg.442; tok=poglejte#13; gold=(2,conj); trankit=(17,parataxis); classla=(2,conj); text="jaz razumem , menjajo se ljudje , menjajo se ministri , ampak poglejte , otroci pa rastejo , ..." |
