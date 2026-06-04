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
- LAS-correct tokens: 9392 (82.08%)

### A) HEAD wrong, DEPREL correct
| Rank | Gold DEPREL | Pred DEPREL | Count | Example |
|---|---|---|---:|---|
| 1 | punct | (same DEPREL, wrong HEAD) | 370 (3.23%) | sid=Gos162.s499; tok=,#18; gold=(15,punct); pred=(20,punct); text="[name:personal] je pač mogoče ta teden izrazil željo , da bi pač rad bolj pomagal pri živalih..." |
| 2 | discourse | (same DEPREL, wrong HEAD) | 135 (1.18%) | sid=Gos160.s153; tok=ne#8; gold=(5,discourse); pred=(2,discourse); text="samo toliko , da zadiši vino , ne ." |
| 3 | advmod | (same DEPREL, wrong HEAD) | 128 (1.12%) | sid=Gos160.s151; tok=še#5; gold=(6,advmod); pred=(7,advmod); text="jaz bom dal pa še majčkeno timijana ." |
| 4 | conj | (same DEPREL, wrong HEAD) | 84 (0.73%) | sid=Gos163.s224; tok=in#19; gold=(7,conj); pred=(15,conj); text="e , je pa tako , dal sem mu tudi druge naloge , ker morajo biti opravljene , in" |
| 5 | parataxis | (same DEPREL, wrong HEAD) | 74 (0.65%) | sid=Gos162.s499; tok=izbral#20; gold=(7,parataxis); pred=(15,parataxis); text="[name:personal] je pač mogoče ta teden izrazil željo , da bi pač rad bolj pomagal pri živalih..." |
| 6 | cc | (same DEPREL, wrong HEAD) | 46 (0.40%) | sid=Gos165.s185; tok=in#31; gold=(41,cc); pred=(33,cc); text="no , in potem so , eee , na Kranjski koči na Ledinah jim je ravnokar odpovedala oskrbnica in ..." |
| 7 | mark | (same DEPREL, wrong HEAD) | 29 (0.25%) | sid=Gos162.s502; tok=če#7; gold=(11,mark); pred=(8,mark); text="če bosta seveda šla vidva , če ne , bojo šle punce , ali ?" |
| 8 | reparandum | (same DEPREL, wrong HEAD) | 25 (0.22%) | sid=Gos162.s501; tok=t-#1; gold=(5,reparandum); pred=(3,reparandum); text="t- , tudi , mogoče , tudi mogoče zaradi tega , če bosta res šla vidva v dvoboj , da imaš pač ..." |
| 9 | obl | (same DEPREL, wrong HEAD) | 25 (0.22%) | sid=Gos165.s178; tok=gimnaziji#4; gold=(8,obl); pred=(9,obl); text="no , po gimnaziji si si zelo želela iti na potovanje po Španiji ." |
| 10 | advcl | (same DEPREL, wrong HEAD) | 23 (0.20%) | sid=Gos163.s217; tok=opravili#13; gold=(6,advcl); pred=(7,advcl); text="ki jo boste , boste mogli opraviti , če boste to nalogo opravili ." |
| 11 | acl | (same DEPREL, wrong HEAD) | 23 (0.20%) | sid=Gos216.s237; tok=se#19; gold=(16,acl); pred=(28,acl); text="zdaj , če greva klasična polena reči , potem je takoj , potem je to peč , kjer se zdaj te , k..." |
| 12 | nsubj | (same DEPREL, wrong HEAD) | 22 (0.19%) | sid=Gos171.s268; tok=poraz#13; gold=(24,nsubj); pred=(22,nsubj); text="to je tekma , ki jo seveda morejo dobiti , toda ta poraz , že drugi na gostovanju , bi precej..." |
| 13 | nmod | (same DEPREL, wrong HEAD) | 20 (0.17%) | sid=Gos165.s180; tok=Jezerskim#11; gold=(7,nmod); pred=(9,nmod); text="in si služila denar v gorski koči na Ledinah nad Jezerskim , kako si zašla tja , ljubezen do ..." |
| 14 | obj | (same DEPREL, wrong HEAD) | 16 (0.14%) | sid=Gos163.s217; tok=jo#2; gold=(7,obj); pred=(3,obj); text="ki jo boste , boste mogli opraviti , če boste to nalogo opravili ." |
| 15 | aux | (same DEPREL, wrong HEAD) | 15 (0.13%) | sid=Gos165.s185; tok=sem#32; gold=(41,aux); pred=(33,aux); text="no , in potem so , eee , na Kranjski koči na Ledinah jim je ravnokar odpovedala oskrbnica in ..." |
| 16 | case | (same DEPREL, wrong HEAD) | 14 (0.12%) | sid=Gos165.s194; tok=po#10; gold=(12,case); pred=(13,case); text="in mi je vsako jutro že za zajtrk skuhala po ene pet jajc pa masonek ." |
| 17 | cop | (same DEPREL, wrong HEAD) | 10 (0.09%) | sid=Gos171.s270; tok=je#4; gold=(2,cop); pred=(6,cop); text="novi predsednik zveze je legendarni Grzegorz Lato ." |
| 18 | expl | (same DEPREL, wrong HEAD) | 9 (0.08%) | sid=Artur-J-Gvecg-P500014.s245-s248_reseg.94; tok=se#30; gold=(34,expl); pred=(31,expl); text="eem res so bili naši , tako naši člani kot eem tudi preko socialnih omrežij ostali bolniki s ..." |
| 19 | appos | (same DEPREL, wrong HEAD) | 7 (0.06%) | sid=Gos170.s139; tok=menedžer#8; gold=(5,appos); pred=(2,appos); text="tu David Healy in Nigel Worthington , menedžer oziroma selektor reprezentance ." |
| 20 | det | (same DEPREL, wrong HEAD) | 5 (0.04%) | sid=Gos216.s241; tok=vse#13; gold=(14,det); pred=(17,det); text="je tudi vso j- , vse je tudi regulirano temperaturno , imate vse o- , vse senzorje zgoraj in ..." |

### B) HEAD correct, DEPREL wrong
| Rank | Gold DEPREL | Pred DEPREL | Count | Example |
|---|---|---|---:|---|
| 1 | appos | conj | 18 (0.16%) | sid=Gos216.s231; tok=olju#33; gold=(28,appos); pred=(28,conj); text="eee , je , je to v bistvu , eee , tudi , eee , v , potrebno imeti dosti izolirano hišo ali je..." |
| 2 | parataxis | conj | 13 (0.11%) | sid=Gos160.s157; tok=zloženi#5; gold=(3,parataxis); pred=(3,conj); text="piščanci so pripravljeni , zloženi ." |
| 3 | discourse | advmod | 13 (0.11%) | sid=Gos163.s229; tok=ne#7; gold=(8,discourse); pred=(8,advmod); text="se ni , se ni nič ne premaknilo ne na drugo stran ." |
| 4 | obj | nsubj | 11 (0.10%) | sid=Gos165.s176; tok=to#5; gold=(7,obj); pred=(7,nsubj); text="mogoče tvoja prijateljica [name:personal] to bolj ve ." |
| 5 | orphan | advmod | 10 (0.09%) | sid=Gos160.s162; tok=čez#6; gold=(5,orphan); pred=(5,advmod); text="aha , in to zelenjavo čez ." |
| 6 | advmod | orphan | 10 (0.09%) | sid=Gos162.s501; tok=mogoče#8; gold=(10,advmod); pred=(10,orphan); text="t- , tudi , mogoče , tudi mogoče zaradi tega , če bosta res šla vidva v dvoboj , da imaš pač ..." |
| 7 | nummod | det | 10 (0.09%) | sid=Gos165.s185; tok=en#36; gold=(37,nummod); pred=(37,det); text="no , in potem so , eee , na Kranjski koči na Ledinah jim je ravnokar odpovedala oskrbnica in ..." |
| 8 | iobj | obj | 9 (0.08%) | sid=Gos162.s503; tok=meni#16; gold=(18,iobj); pred=(18,obj); text="a no , daj , veš , kdo bo šel na dvoboj , kaj ti meni zdaj govoriš ?" |
| 9 | obj | iobj | 9 (0.08%) | sid=Gos165.s177; tok=ti#2; gold=(4,obj); pred=(4,iobj); text="toliko ti je pomenil , no ." |
| 10 | advmod | cc | 8 (0.07%) | sid=Artur-J-Gvecg-P500028.s184-s190_reseg.233; tok=pa#82; gold=(85,advmod); pred=(85,cc); text="eee , zdaj zaenkrat je to sicer še mala ekipa , ki je pa naslonjena na ta bistveno večji pogo..." |
| 11 | nmod | obl | 7 (0.06%) | sid=Gos163.s226; tok=volno#32; gold=(29,nmod); pred=(29,obl); text="tako kot sem mu naročil , tako je treba to narediti , eee , sem mu vse lepo povedal in razlož..." |
| 12 | cc | advmod | 7 (0.06%) | sid=Gos165.s187; tok=pa#15; gold=(17,cc); pred=(17,advmod); text="od teh plinskih bomb , ki jih je bilo treba nekaj takole šraufati , pa vse živo , skratka , b..." |
| 13 | conj | parataxis | 7 (0.06%) | sid=Gos165.s193; tok=živahna#8; gold=(3,conj); pred=(3,parataxis); text="eee , stara osemdeset let , zelo živahna ." |
| 14 | conj | appos | 7 (0.06%) | sid=Gos206.s138; tok=imenih#7; gold=(4,conj); pred=(4,appos); text="iskalnik je po krajih , po imenih , po , po , po , po ukrepih , ne , in tam lahko , če greste..." |
| 15 | nsubj | obj | 6 (0.05%) | sid=Gos160.s153; tok=vino#6; gold=(5,nsubj); pred=(5,obj); text="samo toliko , da zadiši vino , ne ." |
| 16 | advmod | discourse | 6 (0.05%) | sid=Gos170.s128; tok=jasno#3; gold=(9,advmod); pred=(9,discourse); text="toda , jasno , ob Vidiču in Ferdinandu nima dosti možnosti za igranje ." |
| 17 | obl | obj | 6 (0.05%) | sid=Artur-J-Gvecg-P500063.s87-s93_reseg.467; tok=sedemdeset#63; gold=(62,obl); pred=(62,obj); text="e , in , e , mi imamo na primer že zdaj v našem , eem , eem , pač zakonu o avtorskih sorodnih..." |
| 18 | nmod | conj | 5 (0.04%) | sid=Artur-J-Gvecg-P500063.s136-s140_reseg.476; tok=del#26; gold=(15,nmod); pred=(15,conj); text="e , zdaj , kar zadeva naše imetnike , se pravi , e , avtorje in založnike , e , literarnih , ..." |
| 19 | obl | nmod | 4 (0.03%) | sid=Gos162.s495; tok=igre#16; gold=(15,obl); pred=(15,nmod); text="eno so , eno bojo verjetno poslali domov , no , tudi to je del igre ." |
| 20 | ccomp | advcl | 4 (0.03%) | sid=Gos165.s184; tok=potrebujejo#12; gold=(5,ccomp); pred=(5,advcl); text="no , in sem poklicala na vsa planinska društva , če potrebujejo koga , kakšnega prostovoljca ." |

### C) HEAD wrong, DEPREL wrong
| Rank | Gold DEPREL | Pred DEPREL | Count | Example |
|---|---|---|---:|---|
| 1 | obl | nmod | 24 (0.21%) | sid=Gos170.s130; tok=strani#26; gold=(19,obl); pred=(22,nmod); text="danes , kot sem že rekel , igra na levi in se bo z Lewandowskym , ki bo prihajal pred severno..." |
| 2 | nmod | obl | 21 (0.18%) | sid=Gos165.s185; tok=ruzakom#28; gold=(25,nmod); pred=(29,obl); text="no , in potem so , eee , na Kranjski koči na Ledinah jim je ravnokar odpovedala oskrbnica in ..." |
| 3 | nsubj | root | 21 (0.18%) | sid=Gos171.s270; tok=Grzegorz#6; gold=(2,nsubj); pred=(0,root); text="novi predsednik zveze je legendarni Grzegorz Lato ." |
| 4 | parataxis | root | 17 (0.15%) | sid=Gos162.s502; tok=šle#11; gold=(4,parataxis); pred=(0,root); text="če bosta seveda šla vidva , če ne , bojo šle punce , ali ?" |
| 5 | root | parataxis | 15 (0.13%) | sid=Gos163.s221; tok=dobil#4; gold=(0,root); pred=(1,parataxis); text="dobimo , boste dobil kom- , konja ." |
| 6 | conj | parataxis | 10 (0.09%) | sid=Gos165.s187; tok=pestro#24; gold=(4,conj); pred=(17,parataxis); text="od teh plinskih bomb , ki jih je bilo treba nekaj takole šraufati , pa vse živo , skratka , b..." |
| 7 | root | nsubj | 10 (0.09%) | sid=Gos171.s270; tok=predsednik#2; gold=(0,root); pred=(6,nsubj); text="novi predsednik zveze je legendarni Grzegorz Lato ." |
| 8 | root | cop | 10 (0.09%) | sid=Gos179.s158; tok=je#3; gold=(0,root); pred=(5,cop); text="kje pa je lastniška struktura Dnevnika ?" |
| 9 | conj | obl | 10 (0.09%) | sid=Artur-J-Gvecg-P500014.s270_reseg.100; tok=bolniki#20; gold=(15,conj); pred=(11,obl); text="ampak ti videokonferenčni sistemi so nam omogočali , da smo bili na vezi tako mi med sabo kot..." |
| 10 | advcl | acl | 8 (0.07%) | sid=Gos162.s501; tok=šla#15; gold=(21,advcl); pred=(10,acl); text="t- , tudi , mogoče , tudi mogoče zaradi tega , če bosta res šla vidva v dvoboj , da imaš pač ..." |
| 11 | orphan | advmod | 8 (0.07%) | sid=Gos193.s140; tok=prej#9; gold=(8,orphan); pred=(13,advmod); text="mene s pinceto ne boli , če jih prej malo neko kremo daš noter , ne ." |
| 12 | reparandum | case | 8 (0.07%) | sid=Gos206.s138; tok=v#52; gold=(56,reparandum); pred=(57,case); text="iskalnik je po krajih , po imenih , po , po , po , po ukrepih , ne , in tam lahko , če greste..." |
| 13 | nsubj | conj | 8 (0.07%) | sid=Artur-J-Gvecg-P500028.s184-s190_reseg.233; tok=aktivnosti#81; gold=(85,nsubj); pred=(78,conj); text="eee , zdaj zaenkrat je to sicer še mala ekipa , ki je pa naslonjena na ta bistveno večji pogo..." |
| 14 | reparandum | conj | 7 (0.06%) | sid=Gos171.s268; tok=okrnil#22; gold=(24,reparandum); pred=(3,conj); text="to je tekma , ki jo seveda morejo dobiti , toda ta poraz , že drugi na gostovanju , bi precej..." |
| 15 | parataxis | advcl | 7 (0.06%) | sid=Gos193.s140; tok=daš#13; gold=(8,parataxis); pred=(5,advcl); text="mene s pinceto ne boli , če jih prej malo neko kremo daš noter , ne ." |
| 16 | conj | amod | 7 (0.06%) | sid=Artur-J-Gvecg-P500014.s205-s207_reseg.86; tok=skupinsko#22; gold=(18,conj); pred=(23,amod); text="eee tudi naši strokovnjaki so se zelo hitro prilagodili in so preko videokonferenčnega sistem..." |
| 17 | reparandum | root | 6 (0.05%) | sid=Gos163.s221; tok=dobimo#1; gold=(4,reparandum); pred=(0,root); text="dobimo , boste dobil kom- , konja ." |
| 18 | cop | root | 6 (0.05%) | sid=Gos179.s168; tok=je#2; gold=(3,cop); pred=(0,root); text="to je [name:surname] , naprej ." |
| 19 | parataxis | acl | 6 (0.05%) | sid=Gos216.s233; tok=imate#23; gold=(10,parataxis); pred=(20,acl); text="ne vem , z biomaso je tako , biomaso imate vi zdaj tri vrste , bi rekel , tri vrste , ali ima..." |
| 20 | parataxis | cop | 6 (0.05%) | sid=Artur-J-Gvecg-P500014.s217_reseg.89; tok=so#10; gold=(7,parataxis); pred=(12,cop); text="eee v bistvu to je spletna stran , tukaj so trije moduli : prehranski , psiho-socialni in pa ..." |

## Direct model comparison (LAS exact)
- Compared tokens: 11443
- Trankit aligned correct, CLASSLA aligned wrong: 975 (8.52%)
- Trankit aligned wrong, CLASSLA aligned correct: 428 (3.74%)

### Where Trankit aligned is better
| Rank | Gold DEPREL | Loser error pattern | Count | Example |
|---|---|---|---:|---|
| 1 | punct | HEAD wrong, DEPREL punct | 153 (1.34%) | sid=Gos162.s499; tok=,#18; gold=(15,punct); trankit=(15,punct); classla=(20,punct); text="[name:personal] je pač mogoče ta teden izrazil željo , da bi pač rad bolj pomagal pri živalih..." |
| 2 | advmod | HEAD wrong, DEPREL advmod | 75 (0.66%) | sid=Gos165.s185; tok=potem#4; gold=(5,advmod); trankit=(5,advmod); classla=(17,advmod); text="no , in potem so , eee , na Kranjski koči na Ledinah jim je ravnokar odpovedala oskrbnica in ..." |
| 3 | discourse | HEAD wrong, DEPREL discourse | 63 (0.55%) | sid=Gos162.s496; tok=ne#15; gold=(13,discourse); trankit=(13,discourse); classla=(3,discourse); text="jaz ne vem , kako ti zbral , ne , mogoče po šibicah , ne ." |
| 4 | conj | HEAD wrong, DEPREL conj | 43 (0.38%) | sid=Gos170.s137; tok=uspelo#23; gold=(10,conj); trankit=(10,conj); classla=(14,conj); text="tudi drugi napadalec , izjemni David Healy , je imel priložnost , da premaga Arturja Boruca ,..." |
| 5 | cc | HEAD wrong, DEPREL cc | 33 (0.29%) | sid=Gos165.s185; tok=in#31; gold=(41,cc); trankit=(41,cc); classla=(33,cc); text="no , in potem so , eee , na Kranjski koči na Ledinah jim je ravnokar odpovedala oskrbnica in ..." |
| 6 | parataxis | HEAD wrong, DEPREL parataxis | 27 (0.24%) | sid=Gos162.s499; tok=izbral#20; gold=(7,parataxis); trankit=(7,parataxis); classla=(15,parataxis); text="[name:personal] je pač mogoče ta teden izrazil željo , da bi pač rad bolj pomagal pri živalih..." |
| 7 | obl | HEAD wrong + DEPREL obl->nmod | 21 (0.18%) | sid=Gos170.s130; tok=strani#26; gold=(19,obl); trankit=(19,obl); classla=(22,nmod); text="danes , kot sem že rekel , igra na levi in se bo z Lewandowskym , ki bo prihajal pred severno..." |
| 8 | mark | HEAD wrong, DEPREL mark | 16 (0.14%) | sid=Artur-J-Gvecg-P500014.s186-s189_reseg.81; tok=ki#14; gold=(17,mark); trankit=(17,mark); classla=(15,mark); text="eee in seveda , eem kako prenesti ta naš eee rehabilitacijski program , ki je pač prvi te vrs..." |
| 9 | nmod | HEAD wrong + DEPREL nmod->obl | 14 (0.12%) | sid=Gos165.s190; tok=kil#10; gold=(11,nmod); trankit=(11,nmod); classla=(8,obl); text="baje , da si nazaj v dolino prišla dvajset kil težja ." |
| 10 | nsubj | HEAD wrong + DEPREL nsubj->root | 13 (0.11%) | sid=Gos171.s270; tok=Grzegorz#6; gold=(2,nsubj); trankit=(2,nsubj); classla=(0,root); text="novi predsednik zveze je legendarni Grzegorz Lato ." |
| 11 | obl | HEAD wrong, DEPREL obl | 12 (0.10%) | sid=Gos179.s165; tok=eni#16; gold=(12,obl); trankit=(12,obl); classla=(13,obl); text="to bi bilo tudi pol zanimivo pogledati naprej , ne , kaj so to za eni ." |
| 12 | nsubj | HEAD wrong, DEPREL nsubj | 12 (0.10%) | sid=Gos179.s168; tok=to#1; gold=(3,nsubj); trankit=(3,nsubj); classla=(2,nsubj); text="to je [name:surname] , naprej ." |
| 13 | acl | HEAD wrong, DEPREL acl | 12 (0.10%) | sid=Gos216.s238; tok=imajo#16; gold=(11,acl); trankit=(11,acl); classla=(13,acl); text="se pravi , da je to , so zelo učinkovite peči na polena , ki imajo , ki , mmm , recimo temu n..." |
| 14 | advcl | HEAD wrong, DEPREL advcl | 12 (0.10%) | sid=Artur-J-Gvecg-P500014.s178-s182_reseg.79; tok=nakazovalo#11; gold=(35,advcl); trankit=(35,advcl); classla=(5,advcl); text="eee ja , tako je , ko se je že nakazovalo , a ne , da bo pač epidemija prišla iz tujine tudi ..." |
| 15 | appos | DEPREL appos->conj, HEAD ok | 12 (0.10%) | sid=Artur-J-Gvecg-P500014.s183-s185_reseg.80; tok=živo#27; gold=(24,appos); trankit=(24,appos); classla=(24,conj); text="eee tako da smo s kolegi iskal različne načine , a ne , kako prilagoditi predvsem tiste progr..." |
| 16 | case | HEAD wrong, DEPREL case | 10 (0.09%) | sid=Gos206.s135; tok=za#5; gold=(6,case); trankit=(6,case); classla=(8,case); text="uuu , nisem zdajle za raču- , Nep , Nep , ja ." |
| 17 | obj | HEAD wrong, DEPREL obj | 10 (0.09%) | sid=Gos216.s231; tok=klasiki#28; gold=(27,obj); trankit=(27,obj); classla=(24,obj); text="eee , je , je to v bistvu , eee , tudi , eee , v , potrebno imeti dosti izolirano hišo ali je..." |
| 18 | nmod | HEAD wrong, DEPREL nmod | 9 (0.08%) | sid=Artur-J-Gvecg-P500014.s186-s189_reseg.81; tok=bolnike#22; gold=(17,nmod); trankit=(17,nmod); classla=(19,nmod); text="eee in seveda , eem kako prenesti ta naš eee rehabilitacijski program , ki je pač prvi te vrs..." |
| 19 | nummod | DEPREL nummod->det, HEAD ok | 8 (0.07%) | sid=Gos165.s185; tok=en#36; gold=(37,nummod); trankit=(37,nummod); classla=(37,det); text="no , in potem so , eee , na Kranjski koči na Ledinah jim je ravnokar odpovedala oskrbnica in ..." |
| 20 | root | HEAD wrong + DEPREL root->nsubj | 8 (0.07%) | sid=Gos171.s270; tok=predsednik#2; gold=(0,root); trankit=(0,root); classla=(6,nsubj); text="novi predsednik zveze je legendarni Grzegorz Lato ." |

### Where Trankit aligned loses to CLASSLA aligned
| Rank | Gold DEPREL | Loser error pattern | Count | Example |
|---|---|---|---:|---|
| 1 | punct | HEAD wrong, DEPREL punct | 91 (0.80%) | sid=Gos162.s501; tok=,#19; gold=(15,punct); trankit=(21,punct); classla=(15,punct); text="t- , tudi , mogoče , tudi mogoče zaradi tega , če bosta res šla vidva v dvoboj , da imaš pač ..." |
| 2 | discourse | HEAD wrong, DEPREL discourse | 51 (0.45%) | sid=Gos162.s496; tok=ne#9; gold=(7,discourse); trankit=(3,discourse); classla=(7,discourse); text="jaz ne vem , kako ti zbral , ne , mogoče po šibicah , ne ." |
| 3 | advmod | HEAD wrong, DEPREL advmod | 27 (0.24%) | sid=Gos165.s182; tok=zdaj#5; gold=(6,advmod); trankit=(9,advmod); classla=(6,advmod); text="in sem rekla , zdaj moram pa nekaj zaslužiti , ker hočem v Španijo , hočem v tujino , nekaj h..." |
| 4 | conj | HEAD wrong, DEPREL conj | 27 (0.24%) | sid=Gos206.s139; tok=lastnika#13; gold=(8,conj); trankit=(11,conj); classla=(8,conj); text="in tam dobite naslove in pokličete nekega gospoda ali pa gospo oziroma lastnika te hiše , ga ..." |
| 5 | reparandum | HEAD wrong, DEPREL reparandum | 13 (0.11%) | sid=Gos216.s238; tok=je#5; gold=(11,reparandum); trankit=(6,reparandum); classla=(11,reparandum); text="se pravi , da je to , so zelo učinkovite peči na polena , ki imajo , ki , mmm , recimo temu n..." |
| 6 | parataxis | HEAD wrong, DEPREL parataxis | 12 (0.10%) | sid=Gos163.s226; tok=povedal#19; gold=(8,parataxis); trankit=(5,parataxis); classla=(8,parataxis); text="tako kot sem mu naročil , tako je treba to narediti , eee , sem mu vse lepo povedal in razlož..." |
| 7 | cc | HEAD wrong, DEPREL cc | 10 (0.09%) | sid=Gos165.s185; tok=in#3; gold=(17,cc); trankit=(5,cc); classla=(17,cc); text="no , in potem so , eee , na Kranjski koči na Ledinah jim je ravnokar odpovedala oskrbnica in ..." |
| 8 | obl | HEAD wrong, DEPREL obl | 9 (0.08%) | sid=Gos179.s171; tok=tega#12; gold=(7,obl); trankit=(4,obl); classla=(7,obl); text="ja , samo vprašanje , kdo je to v resnici izza tega , ne ." |
| 9 | nsubj | HEAD wrong, DEPREL nsubj | 6 (0.05%) | sid=Gos179.s171; tok=kdo#6; gold=(7,nsubj); trankit=(4,nsubj); classla=(7,nsubj); text="ja , samo vprašanje , kdo je to v resnici izza tega , ne ." |
| 10 | mark | HEAD wrong, DEPREL mark | 6 (0.05%) | sid=Artur-J-Gvecg-P500063.s113-s118_reseg.471; tok=ki#24; gold=(50,mark); trankit=(67,mark); classla=(50,mark); text="e , zato smo predlagali tudi kar nekaj pač , e , e , izboljšav , bi rekla , predloga , e , ki..." |
| 11 | obl | HEAD wrong + DEPREL obl->nmod | 5 (0.04%) | sid=Gos206.s133; tok=internet#3; gold=(1,obl); trankit=(4,nmod); classla=(1,obl); text="greste na internet stran Nep , Nacionalna energetska pot , lahko jo takoj odtipkajte , če ste..." |
| 12 | cop | HEAD wrong + DEPREL cop->parataxis | 5 (0.04%) | sid=Artur-J-Gvecg-P500054.s60-s65_reseg.443; tok=so#26; gold=(27,cop); trankit=(3,parataxis); classla=(27,cop); text="in če nimamo programa z akcijskim načrtom , kjer bi država , bi rekla , naredila neki spisek ..." |
| 13 | cop | HEAD wrong, DEPREL cop | 4 (0.03%) | sid=Gos216.s238; tok=so#8; gold=(11,cop); trankit=(10,cop); classla=(11,cop); text="se pravi , da je to , so zelo učinkovite peči na polena , ki imajo , ki , mmm , recimo temu n..." |
| 14 | nmod | HEAD wrong + DEPREL nmod->obl | 4 (0.03%) | sid=Artur-J-Gvecg-P500014.s259-s261_reseg.97; tok=pripravo#13; gold=(11,nmod); trankit=(3,obl); classla=(11,nmod); text="eem pripravila imeli smo pa zdej tudi eem malo več časa za pripravo novih publikacij , tudi m..." |
| 15 | fixed | HEAD wrong + DEPREL fixed->advmod | 4 (0.03%) | sid=Artur-P-G7155-P700259.s2-s71_reseg.1933.4; tok=pa#26; gold=(25,fixed); trankit=(27,advmod); classla=(25,fixed); text="eee , težava pri samostojnih podjetnikih , ko pride do bolezni , ki traja dlje časa , pri pod..." |
| 16 | root | HEAD wrong + DEPREL root->parataxis | 3 (0.03%) | sid=Gos165.s185; tok=odpovedala#17; gold=(0,root); trankit=(5,parataxis); classla=(0,root); text="no , in potem so , eee , na Kranjski koči na Ledinah jim je ravnokar odpovedala oskrbnica in ..." |
| 17 | cc | DEPREL cc->advmod, HEAD ok | 3 (0.03%) | sid=Gos179.s171; tok=samo#3; gold=(4,cc); trankit=(4,advmod); classla=(4,cc); text="ja , samo vprašanje , kdo je to v resnici izza tega , ne ." |
| 18 | reparandum | HEAD wrong + DEPREL reparandum->orphan | 3 (0.03%) | sid=Gos189.s53; tok=pa#2; gold=(4,reparandum); trankit=(1,orphan); classla=(4,reparandum); text="zdaj pa , pa to sonce in toplo vreme zunaj in zdaj pa" |
| 19 | case | HEAD wrong, DEPREL case | 3 (0.03%) | sid=Gos206.s133; tok=na#2; gold=(3,case); trankit=(4,case); classla=(3,case); text="greste na internet stran Nep , Nacionalna energetska pot , lahko jo takoj odtipkajte , če ste..." |
| 20 | advcl | HEAD wrong, DEPREL advcl | 3 (0.03%) | sid=Gos207.s8; tok=imamo#23; gold=(18,advcl); trankit=(16,advcl); classla=(18,advcl); text="ja , no , to je pa dobra novica , tako da , da ne bo dolga seansa , ja , ker imamo pol , saj ..." |
