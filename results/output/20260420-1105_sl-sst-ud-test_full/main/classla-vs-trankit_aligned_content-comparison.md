# Table-style content comparison (Trankit aligned vs CLASSLA aligned)

Columns 7-8 are compared directly (HEAD and DEPREL), with concrete token examples.

## Scope
- Gold sentences: 432
- Trankit aligned sentences: 432
- CLASSLA aligned sentences: 432

## Trankit aligned - error content tables
- Compared tokens: 11443
- LAS-correct tokens: 9921 (86.70%)

### A) HEAD wrong, DEPREL correct
| Rank | Gold DEPREL | Pred DEPREL | Count | Example |
|---|---|---|---:|---|
| 1 | punct | (same DEPREL, wrong HEAD) | 323 (2.82%) | sid=Gos162.s497; tok=,#2; gold=(3,punct); pred=(1,punct); text="ne , ne , ne ." |
| 2 | discourse | (same DEPREL, wrong HEAD) | 121 (1.06%) | sid=Gos160.s153; tok=ne#8; gold=(5,discourse); pred=(2,discourse); text="samo toliko , da zadiši vino , ne ." |
| 3 | advmod | (same DEPREL, wrong HEAD) | 85 (0.74%) | sid=Gos160.s151; tok=še#5; gold=(6,advmod); pred=(7,advmod); text="jaz bom dal pa še majčkeno timijana ." |
| 4 | conj | (same DEPREL, wrong HEAD) | 74 (0.65%) | sid=Gos163.s224; tok=in#19; gold=(7,conj); pred=(3,conj); text="e , je pa tako , dal sem mu tudi druge naloge , ker morajo biti opravljene , in" |
| 5 | parataxis | (same DEPREL, wrong HEAD) | 58 (0.51%) | sid=Gos163.s226; tok=povedal#19; gold=(8,parataxis); pred=(5,parataxis); text="tako kot sem mu naročil , tako je treba to narediti , eee , sem mu vse lepo povedal in razlož..." |
| 6 | reparandum | (same DEPREL, wrong HEAD) | 45 (0.39%) | sid=Gos163.s217; tok=boste#3; gold=(6,reparandum); pred=(7,reparandum); text="ki jo boste , boste mogli opraviti , če boste to nalogo opravili ." |
| 7 | cc | (same DEPREL, wrong HEAD) | 23 (0.20%) | sid=Gos165.s185; tok=in#3; gold=(17,cc); pred=(5,cc); text="no , in potem so , eee , na Kranjski koči na Ledinah jim je ravnokar odpovedala oskrbnica in ..." |
| 8 | obl | (same DEPREL, wrong HEAD) | 22 (0.19%) | sid=Gos165.s178; tok=gimnaziji#4; gold=(8,obl); pred=(9,obl); text="no , po gimnaziji si si zelo želela iti na potovanje po Španiji ." |
| 9 | nsubj | (same DEPREL, wrong HEAD) | 17 (0.15%) | sid=Gos171.s268; tok=poraz#13; gold=(24,nsubj); pred=(22,nsubj); text="to je tekma , ki jo seveda morejo dobiti , toda ta poraz , že drugi na gostovanju , bi precej..." |
| 10 | nmod | (same DEPREL, wrong HEAD) | 16 (0.14%) | sid=Gos165.s180; tok=Jezerskim#11; gold=(7,nmod); pred=(9,nmod); text="in si služila denar v gorski koči na Ledinah nad Jezerskim , kako si zašla tja , ljubezen do ..." |
| 11 | mark | (same DEPREL, wrong HEAD) | 15 (0.13%) | sid=Gos162.s502; tok=če#7; gold=(11,mark); pred=(8,mark); text="če bosta seveda šla vidva , če ne , bojo šle punce , ali ?" |
| 12 | advcl | (same DEPREL, wrong HEAD) | 15 (0.13%) | sid=Gos163.s217; tok=opravili#13; gold=(6,advcl); pred=(7,advcl); text="ki jo boste , boste mogli opraviti , če boste to nalogo opravili ." |
| 13 | acl | (same DEPREL, wrong HEAD) | 12 (0.10%) | sid=Gos216.s237; tok=se#19; gold=(16,acl); pred=(28,acl); text="zdaj , če greva klasična polena reči , potem je takoj , potem je to peč , kjer se zdaj te , k..." |
| 14 | case | (same DEPREL, wrong HEAD) | 8 (0.07%) | sid=Gos165.s194; tok=po#10; gold=(12,case); pred=(13,case); text="in mi je vsako jutro že za zajtrk skuhala po ene pet jajc pa masonek ." |
| 15 | obj | (same DEPREL, wrong HEAD) | 7 (0.06%) | sid=Gos165.s187; tok=jih#7; gold=(9,obj); pred=(13,obj); text="od teh plinskih bomb , ki jih je bilo treba nekaj takole šraufati , pa vse živo , skratka , b..." |
| 16 | aux | (same DEPREL, wrong HEAD) | 7 (0.06%) | sid=Gos171.s268; tok=bi#20; gold=(24,aux); pred=(22,aux); text="to je tekma , ki jo seveda morejo dobiti , toda ta poraz , že drugi na gostovanju , bi precej..." |
| 17 | orphan | (same DEPREL, wrong HEAD) | 4 (0.03%) | sid=Gos193.s147; tok=od#5; gold=(1,orphan); pred=(4,orphan); text="ta , kaj je od , eee ." |
| 18 | appos | (same DEPREL, wrong HEAD) | 4 (0.03%) | sid=Gos206.s133; tok=pot#9; gold=(5,appos); pred=(4,appos); text="greste na internet stran Nep , Nacionalna energetska pot , lahko jo takoj odtipkajte , če ste..." |
| 19 | cop | (same DEPREL, wrong HEAD) | 4 (0.03%) | sid=Artur-J-Gvecg-P500028.s199-s212_reseg.235; tok=je#100; gold=(105,cop); pred=(55,cop); text="eee , no , in preko centra pa tudi sicer preko inštituta , smo pravzaprav vključeni v vse rel..." |
| 20 | csubj | (same DEPREL, wrong HEAD) | 3 (0.03%) | sid=Gos216.s231; tok=imeti#19; gold=(5,csubj); pred=(18,csubj); text="eee , je , je to v bistvu , eee , tudi , eee , v , potrebno imeti dosti izolirano hišo ali je..." |

### B) HEAD correct, DEPREL wrong
| Rank | Gold DEPREL | Pred DEPREL | Count | Example |
|---|---|---|---:|---|
| 1 | parataxis | conj | 14 (0.12%) | sid=Gos160.s157; tok=zloženi#5; gold=(3,parataxis); pred=(3,conj); text="piščanci so pripravljeni , zloženi ." |
| 2 | appos | conj | 11 (0.10%) | sid=Gos206.s140; tok=smisel#3; gold=(1,appos); pred=(1,conj); text="cilj , smisel tega projekta pa je to , ne , da se dobijo informacije direktno od uporabnikov ..." |
| 3 | discourse | advmod | 10 (0.09%) | sid=Gos163.s229; tok=ne#7; gold=(8,discourse); pred=(8,advmod); text="se ni , se ni nič ne premaknilo ne na drugo stran ." |
| 4 | obj | iobj | 10 (0.09%) | sid=Gos165.s177; tok=ti#2; gold=(4,obj); pred=(4,iobj); text="toliko ti je pomenil , no ." |
| 5 | parataxis | cc | 8 (0.07%) | sid=Gos216.s233; tok=ali#22; gold=(23,parataxis); pred=(23,cc); text="ne vem , z biomaso je tako , biomaso imate vi zdaj tri vrste , bi rekel , tri vrste , ali ima..." |
| 6 | conj | parataxis | 7 (0.06%) | sid=Artur-J-Gvecg-P500054.s15-s24_reseg.427; tok=vemo#62; gold=(55,conj); pred=(55,parataxis); text="mi pri Zvezi prijateljev mladine Slovenije bi bili najbolj veseli , če bi bilo humanitarnega ..." |
| 7 | nmod | obl | 6 (0.05%) | sid=Gos163.s226; tok=volno#32; gold=(29,nmod); pred=(29,obl); text="tako kot sem mu naročil , tako je treba to narediti , eee , sem mu vse lepo povedal in razlož..." |
| 8 | orphan | advmod | 6 (0.05%) | sid=Gos171.s263; tok=zdaj#17; gold=(18,orphan); pred=(18,advmod); text="igral je za kratko tudi pri Nurnbergu , to je njegova edina izkušnja iz tujine in zdaj prekrš..." |
| 9 | advmod | discourse | 6 (0.05%) | sid=Gos213.s78; tok=pač#45; gold=(49,advmod); pred=(49,discourse); text="aha , kul , eee , čakaj , še kako vprašanje , eee , to pa , eee , če , če nabavim to , imate ..." |
| 10 | obj | nsubj | 6 (0.05%) | sid=Gos216.s241; tok=plamen#44; gold=(45,obj); pred=(45,nsubj); text="je tudi vso j- , vse je tudi regulirano temperaturno , imate vse o- , vse senzorje zgoraj in ..." |
| 11 | appos | nmod | 6 (0.05%) | sid=Artur-J-Gvecg-P500014.s208-s212_reseg.87; tok=tem#44; gold=(40,appos); pred=(40,nmod); text="eee tako da smo na neki način jim stali ob strani eem ne le skozi ta program rehabilitacije ,..." |
| 12 | advmod | cc | 6 (0.05%) | sid=Artur-J-Gvecg-P500054.s6_reseg.424; tok=pa#10; gold=(11,advmod); pred=(11,cc); text="ko človek nekako prodre pod , v drobovje , pa vidi , da pravzaprav ni vse tako lepo , kot se ..." |
| 13 | nsubj | obj | 5 (0.04%) | sid=Gos160.s153; tok=vino#6; gold=(5,nsubj); pred=(5,obj); text="samo toliko , da zadiši vino , ne ." |
| 14 | advmod | orphan | 5 (0.04%) | sid=Gos162.s501; tok=mogoče#8; gold=(10,advmod); pred=(10,orphan); text="t- , tudi , mogoče , tudi mogoče zaradi tega , če bosta res šla vidva v dvoboj , da imaš pač ..." |
| 15 | discourse | cc | 5 (0.04%) | sid=Gos170.s135; tok=torej#1; gold=(16,discourse); pred=(16,cc); text="torej to , kar nam kaže za zdaj zadnja vrsta Poljakov , ni kdove kako obetavno ." |
| 16 | cc | advmod | 5 (0.04%) | sid=Gos179.s171; tok=samo#3; gold=(4,cc); pred=(4,advmod); text="ja , samo vprašanje , kdo je to v resnici izza tega , ne ." |
| 17 | nmod | appos | 5 (0.04%) | sid=Artur-J-Gvecg-P500063.s94-s102_reseg.468; tok=pogajanja#12; gold=(7,nmod); pred=(7,appos); text="e , ne , naša pač zgodovina , e , nekako pogajanja z izdajatelji medijev pa kaže , da nekako ..." |
| 18 | obl | nmod | 4 (0.03%) | sid=Gos162.s495; tok=igre#16; gold=(15,obl); pred=(15,nmod); text="eno so , eno bojo verjetno poslali domov , no , tudi to je del igre ." |
| 19 | nsubj | advmod | 4 (0.03%) | sid=Gos163.s231; tok=kaj#1; gold=(3,nsubj); pred=(3,advmod); text="kaj ne gre ?" |
| 20 | obl | obj | 4 (0.03%) | sid=Artur-J-Gvecg-P500014.s203-s204_reseg.85; tok=vsebine#16; gold=(10,obl); pred=(10,obj); text="to se je dogajalo tedensko , tedensko je vsak prejel po tri različne podporne video vsebine ." |

### C) HEAD wrong, DEPREL wrong
| Rank | Gold DEPREL | Pred DEPREL | Count | Example |
|---|---|---|---:|---|
| 1 | parataxis | root | 17 (0.15%) | sid=Gos162.s502; tok=šle#11; gold=(4,parataxis); pred=(0,root); text="če bosta seveda šla vidva , če ne , bojo šle punce , ali ?" |
| 2 | root | parataxis | 14 (0.12%) | sid=Gos163.s221; tok=dobil#4; gold=(0,root); pred=(1,parataxis); text="dobimo , boste dobil kom- , konja ." |
| 3 | nmod | obl | 11 (0.10%) | sid=Gos165.s185; tok=ruzakom#28; gold=(25,nmod); pred=(29,obl); text="no , in potem so , eee , na Kranjski koči na Ledinah jim je ravnokar odpovedala oskrbnica in ..." |
| 4 | obl | nmod | 8 (0.07%) | sid=Gos171.s265; tok=San#7; gold=(5,obl); pred=(8,nmod); text="Poljaki bodo naslednjo tekmo igrali s San Marinom ." |
| 5 | cop | parataxis | 8 (0.07%) | sid=Gos216.s237; tok=je#14; gold=(16,cop); pred=(10,parataxis); text="zdaj , če greva klasična polena reči , potem je takoj , potem je to peč , kjer se zdaj te , k..." |
| 6 | reparandum | orphan | 7 (0.06%) | sid=Gos162.s501; tok=t-#1; gold=(5,reparandum); pred=(3,orphan); text="t- , tudi , mogoče , tudi mogoče zaradi tega , če bosta res šla vidva v dvoboj , da imaš pač ..." |
| 7 | orphan | advmod | 7 (0.06%) | sid=Gos193.s140; tok=prej#9; gold=(8,orphan); pred=(13,advmod); text="mene s pinceto ne boli , če jih prej malo neko kremo daš noter , ne ." |
| 8 | appos | obl | 7 (0.06%) | sid=Gos206.s133; tok=stran#4; gold=(3,appos); pred=(1,obl); text="greste na internet stran Nep , Nacionalna energetska pot , lahko jo takoj odtipkajte , če ste..." |
| 9 | reparandum | conj | 7 (0.06%) | sid=Gos216.s231; tok=drva#35; gold=(41,reparandum); pred=(33,conj); text="eee , je , je to v bistvu , eee , tudi , eee , v , potrebno imeti dosti izolirano hišo ali je..." |
| 10 | parataxis | nsubj | 6 (0.05%) | sid=Gos193.s147; tok=kaj#3; gold=(1,parataxis); pred=(4,nsubj); text="ta , kaj je od , eee ." |
| 11 | advcl | acl | 5 (0.04%) | sid=Gos162.s501; tok=šla#15; gold=(21,advcl); pred=(10,acl); text="t- , tudi , mogoče , tudi mogoče zaradi tega , če bosta res šla vidva v dvoboj , da imaš pač ..." |
| 12 | reparandum | root | 5 (0.04%) | sid=Gos163.s221; tok=dobimo#1; gold=(4,reparandum); pred=(0,root); text="dobimo , boste dobil kom- , konja ." |
| 13 | appos | obj | 5 (0.04%) | sid=Gos165.s184; tok=prostovoljca#16; gold=(13,appos); pred=(12,obj); text="no , in sem poklicala na vsa planinska društva , če potrebujejo koga , kakšnega prostovoljca ." |
| 14 | conj | parataxis | 5 (0.04%) | sid=Gos165.s187; tok=pestro#24; gold=(4,conj); pred=(17,parataxis); text="od teh plinskih bomb , ki jih je bilo treba nekaj takole šraufati , pa vse živo , skratka , b..." |
| 15 | root | nsubj | 5 (0.04%) | sid=Gos216.s237; tok=peč#16; gold=(0,root); pred=(14,nsubj); text="zdaj , če greva klasična polena reči , potem je takoj , potem je to peč , kjer se zdaj te , k..." |
| 16 | fixed | advmod | 5 (0.04%) | sid=Artur-J-Gvecg-P500014.s233-s236_reseg.92; tok=pa#11; gold=(10,fixed); pred=(13,advmod); text="eee to smo tudi objavljali na socialnih omrežjih eee in pa seveda pošiljali našim članom na p..." |
| 17 | nsubj | root | 5 (0.04%) | sid=Artur-J-Gvecg-P500028.s152-s155_reseg.226; tok=pogledi#21; gold=(19,nsubj); pred=(0,root); text="v tistih časih , a ne , to , eee , sega kar nekaj let nazaj , so bili drugačni pogledi ." |
| 18 | root | obl | 4 (0.03%) | sid=Gos165.s187; tok=bomb#4; gold=(0,root); pred=(17,obl); text="od teh plinskih bomb , ki jih je bilo treba nekaj takole šraufati , pa vse živo , skratka , b..." |
| 19 | conj | root | 4 (0.03%) | sid=Gos165.s187; tok=živo#17; gold=(4,conj); pred=(0,root); text="od teh plinskih bomb , ki jih je bilo treba nekaj takole šraufati , pa vse živo , skratka , b..." |
| 20 | root | advmod | 4 (0.03%) | sid=Gos189.s55; tok=noter#1; gold=(0,root); pred=(3,advmod); text="noter pa pisati , pa škoda mi je tega predmeta , ker je ta predmet" |

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
- Trankit aligned correct, CLASSLA aligned wrong: 956 (8.35%)
- Trankit aligned wrong, CLASSLA aligned correct: 427 (3.73%)

### Where Trankit aligned is better
| Rank | Gold DEPREL | Loser error pattern | Count | Example |
|---|---|---|---:|---|
| 1 | punct | HEAD wrong, DEPREL punct | 146 (1.28%) | sid=Gos162.s499; tok=,#18; gold=(15,punct); trankit=(15,punct); classla=(20,punct); text="[name:personal] je pač mogoče ta teden izrazil željo , da bi pač rad bolj pomagal pri živalih..." |
| 2 | advmod | HEAD wrong, DEPREL advmod | 71 (0.62%) | sid=Gos165.s185; tok=potem#4; gold=(5,advmod); trankit=(5,advmod); classla=(17,advmod); text="no , in potem so , eee , na Kranjski koči na Ledinah jim je ravnokar odpovedala oskrbnica in ..." |
| 3 | discourse | HEAD wrong, DEPREL discourse | 62 (0.54%) | sid=Gos162.s496; tok=ne#15; gold=(13,discourse); trankit=(13,discourse); classla=(3,discourse); text="jaz ne vem , kako ti zbral , ne , mogoče po šibicah , ne ." |
| 4 | conj | HEAD wrong, DEPREL conj | 35 (0.31%) | sid=Gos170.s137; tok=uspelo#23; gold=(10,conj); trankit=(10,conj); classla=(14,conj); text="tudi drugi napadalec , izjemni David Healy , je imel priložnost , da premaga Arturja Boruca ,..." |
| 5 | cc | HEAD wrong, DEPREL cc | 34 (0.30%) | sid=Gos165.s185; tok=in#31; gold=(41,cc); trankit=(41,cc); classla=(33,cc); text="no , in potem so , eee , na Kranjski koči na Ledinah jim je ravnokar odpovedala oskrbnica in ..." |
| 6 | parataxis | HEAD wrong, DEPREL parataxis | 29 (0.25%) | sid=Gos162.s499; tok=izbral#20; gold=(7,parataxis); trankit=(7,parataxis); classla=(15,parataxis); text="[name:personal] je pač mogoče ta teden izrazil željo , da bi pač rad bolj pomagal pri živalih..." |
| 7 | obl | HEAD wrong + DEPREL obl->nmod | 20 (0.17%) | sid=Gos170.s130; tok=strani#26; gold=(19,obl); trankit=(19,obl); classla=(22,nmod); text="danes , kot sem že rekel , igra na levi in se bo z Lewandowskym , ki bo prihajal pred severno..." |
| 8 | mark | HEAD wrong, DEPREL mark | 19 (0.17%) | sid=Gos216.s237; tok=kjer#18; gold=(19,mark); trankit=(19,mark); classla=(28,mark); text="zdaj , če greva klasična polena reči , potem je takoj , potem je to peč , kjer se zdaj te , k..." |
| 9 | nmod | HEAD wrong + DEPREL nmod->obl | 15 (0.13%) | sid=Gos165.s190; tok=kil#10; gold=(11,nmod); trankit=(11,nmod); classla=(8,obl); text="baje , da si nazaj v dolino prišla dvajset kil težja ." |
| 10 | obl | HEAD wrong, DEPREL obl | 15 (0.13%) | sid=Gos179.s165; tok=eni#16; gold=(12,obl); trankit=(12,obl); classla=(13,obl); text="to bi bilo tudi pol zanimivo pogledati naprej , ne , kaj so to za eni ." |
| 11 | nsubj | HEAD wrong, DEPREL nsubj | 15 (0.13%) | sid=Gos179.s168; tok=to#1; gold=(3,nsubj); trankit=(3,nsubj); classla=(2,nsubj); text="to je [name:surname] , naprej ." |
| 12 | advcl | HEAD wrong, DEPREL advcl | 13 (0.11%) | sid=Gos213.s78; tok=nabavim#23; gold=(26,advcl); trankit=(26,advcl); classla=(30,advcl); text="aha , kul , eee , čakaj , še kako vprašanje , eee , to pa , eee , če , če nabavim to , imate ..." |
| 13 | nsubj | HEAD wrong + DEPREL nsubj->root | 12 (0.10%) | sid=Gos171.s270; tok=Grzegorz#6; gold=(2,nsubj); trankit=(2,nsubj); classla=(0,root); text="novi predsednik zveze je legendarni Grzegorz Lato ." |
| 14 | obj | HEAD wrong, DEPREL obj | 11 (0.10%) | sid=Gos163.s217; tok=jo#2; gold=(7,obj); trankit=(7,obj); classla=(3,obj); text="ki jo boste , boste mogli opraviti , če boste to nalogo opravili ." |
| 15 | acl | HEAD wrong, DEPREL acl | 11 (0.10%) | sid=Gos216.s238; tok=imajo#16; gold=(11,acl); trankit=(11,acl); classla=(13,acl); text="se pravi , da je to , so zelo učinkovite peči na polena , ki imajo , ki , mmm , recimo temu n..." |
| 16 | case | HEAD wrong, DEPREL case | 10 (0.09%) | sid=Gos206.s135; tok=za#5; gold=(6,case); trankit=(6,case); classla=(8,case); text="uuu , nisem zdajle za raču- , Nep , Nep , ja ." |
| 17 | aux | HEAD wrong, DEPREL aux | 9 (0.08%) | sid=Gos165.s185; tok=sem#32; gold=(41,aux); trankit=(41,aux); classla=(33,aux); text="no , in potem so , eee , na Kranjski koči na Ledinah jim je ravnokar odpovedala oskrbnica in ..." |
| 18 | iobj | DEPREL iobj->obj, HEAD ok | 8 (0.07%) | sid=Gos162.s503; tok=meni#16; gold=(18,iobj); trankit=(18,iobj); classla=(18,obj); text="a no , daj , veš , kdo bo šel na dvoboj , kaj ti meni zdaj govoriš ?" |
| 19 | reparandum | HEAD wrong, DEPREL reparandum | 8 (0.07%) | sid=Gos179.s154; tok=kaj#3; gold=(7,reparandum); trankit=(7,reparandum); classla=(9,reparandum); text="torej , kaj , eee , česa je lastnik Dnevnik ." |
| 20 | nmod | HEAD wrong, DEPREL nmod | 8 (0.07%) | sid=Artur-J-Gvecg-P500014.s186-s189_reseg.81; tok=bolnike#22; gold=(17,nmod); trankit=(17,nmod); classla=(19,nmod); text="eee in seveda , eem kako prenesti ta naš eee rehabilitacijski program , ki je pač prvi te vrs..." |

### Where Trankit aligned loses to CLASSLA aligned
| Rank | Gold DEPREL | Loser error pattern | Count | Example |
|---|---|---|---:|---|
| 1 | punct | HEAD wrong, DEPREL punct | 99 (0.87%) | sid=Gos162.s497; tok=,#2; gold=(3,punct); trankit=(1,punct); classla=(3,punct); text="ne , ne , ne ." |
| 2 | discourse | HEAD wrong, DEPREL discourse | 48 (0.42%) | sid=Gos162.s496; tok=ne#9; gold=(7,discourse); trankit=(3,discourse); classla=(7,discourse); text="jaz ne vem , kako ti zbral , ne , mogoče po šibicah , ne ." |
| 3 | advmod | HEAD wrong, DEPREL advmod | 26 (0.23%) | sid=Gos189.s54; tok=malo#12; gold=(11,advmod); trankit=(17,advmod); classla=(11,advmod); text="vse nas malo povleče ven , ne , te še moremo malo potem še tiste zadnje moči , da nekako prid..." |
| 4 | conj | HEAD wrong, DEPREL conj | 26 (0.23%) | sid=Gos207.s8; tok=in#30; gold=(29,conj); trankit=(23,conj); classla=(29,conj); text="ja , no , to je pa dobra novica , tako da , da ne bo dolga seansa , ja , ker imamo pol , saj ..." |
| 5 | reparandum | HEAD wrong, DEPREL reparandum | 16 (0.14%) | sid=Gos163.s217; tok=boste#3; gold=(6,reparandum); trankit=(7,reparandum); classla=(6,reparandum); text="ki jo boste , boste mogli opraviti , če boste to nalogo opravili ." |
| 6 | parataxis | HEAD wrong, DEPREL parataxis | 12 (0.10%) | sid=Gos163.s226; tok=povedal#19; gold=(8,parataxis); trankit=(5,parataxis); classla=(8,parataxis); text="tako kot sem mu naročil , tako je treba to narediti , eee , sem mu vse lepo povedal in razlož..." |
| 7 | cc | HEAD wrong, DEPREL cc | 12 (0.10%) | sid=Gos165.s185; tok=in#3; gold=(17,cc); trankit=(5,cc); classla=(17,cc); text="no , in potem so , eee , na Kranjski koči na Ledinah jim je ravnokar odpovedala oskrbnica in ..." |
| 8 | obl | HEAD wrong, DEPREL obl | 12 (0.10%) | sid=Gos179.s171; tok=resnici#10; gold=(7,obl); trankit=(11,obl); classla=(7,obl); text="ja , samo vprašanje , kdo je to v resnici izza tega , ne ." |
| 9 | obl | HEAD wrong + DEPREL obl->nmod | 5 (0.04%) | sid=Gos171.s265; tok=San#7; gold=(5,obl); trankit=(8,nmod); classla=(5,obl); text="Poljaki bodo naslednjo tekmo igrali s San Marinom ." |
| 10 | reparandum | HEAD wrong + DEPREL reparandum->orphan | 5 (0.04%) | sid=Gos189.s53; tok=pa#2; gold=(4,reparandum); trankit=(1,orphan); classla=(4,reparandum); text="zdaj pa , pa to sonce in toplo vreme zunaj in zdaj pa" |
| 11 | mark | HEAD wrong, DEPREL mark | 5 (0.04%) | sid=Gos207.s8; tok=da#14; gold=(18,mark); trankit=(16,mark); classla=(18,mark); text="ja , no , to je pa dobra novica , tako da , da ne bo dolga seansa , ja , ker imamo pol , saj ..." |
| 12 | cop | HEAD wrong + DEPREL cop->parataxis | 5 (0.04%) | sid=Artur-J-Gvecg-P500054.s60-s65_reseg.443; tok=so#26; gold=(27,cop); trankit=(16,parataxis); classla=(27,cop); text="in če nimamo programa z akcijskim načrtom , kjer bi država , bi rekla , naredila neki spisek ..." |
| 13 | root | HEAD wrong + DEPREL root->parataxis | 4 (0.03%) | sid=Gos165.s185; tok=odpovedala#17; gold=(0,root); trankit=(5,parataxis); classla=(0,root); text="no , in potem so , eee , na Kranjski koči na Ledinah jim je ravnokar odpovedala oskrbnica in ..." |
| 14 | case | HEAD wrong, DEPREL case | 4 (0.03%) | sid=Gos171.s265; tok=s#6; gold=(7,case); trankit=(8,case); classla=(7,case); text="Poljaki bodo naslednjo tekmo igrali s San Marinom ." |
| 15 | obj | DEPREL obj->iobj, HEAD ok | 4 (0.03%) | sid=Gos206.s139; tok=ga#20; gold=(21,obj); trankit=(21,iobj); classla=(21,obj); text="in tam dobite naslove in pokličete nekega gospoda ali pa gospo oziroma lastnika te hiše , ga ..." |
| 16 | nmod | HEAD wrong + DEPREL nmod->obl | 4 (0.03%) | sid=Artur-J-Gvecg-P500014.s259-s261_reseg.97; tok=pripravo#13; gold=(11,nmod); trankit=(3,obl); classla=(11,nmod); text="eem pripravila imeli smo pa zdej tudi eem malo več časa za pripravo novih publikacij , tudi m..." |
| 17 | nsubj | HEAD wrong, DEPREL nsubj | 3 (0.03%) | sid=Gos179.s171; tok=kdo#6; gold=(7,nsubj); trankit=(11,nsubj); classla=(7,nsubj); text="ja , samo vprašanje , kdo je to v resnici izza tega , ne ." |
| 18 | orphan | DEPREL orphan->advmod, HEAD ok | 3 (0.03%) | sid=Gos189.s53; tok=zunaj#10; gold=(6,orphan); trankit=(6,advmod); classla=(6,orphan); text="zdaj pa , pa to sonce in toplo vreme zunaj in zdaj pa" |
| 19 | advcl | HEAD wrong, DEPREL advcl | 3 (0.03%) | sid=Gos207.s8; tok=imamo#23; gold=(18,advcl); trankit=(16,advcl); classla=(18,advcl); text="ja , no , to je pa dobra novica , tako da , da ne bo dolga seansa , ja , ker imamo pol , saj ..." |
| 20 | amod | HEAD wrong, DEPREL amod | 3 (0.03%) | sid=Gos216.s237; tok=klasična#5; gold=(6,amod); trankit=(7,amod); classla=(6,amod); text="zdaj , če greva klasična polena reči , potem je takoj , potem je to peč , kjer se zdaj te , k..." |
