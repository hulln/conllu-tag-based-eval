# Table-style content comparison (Trankit aligned vs CLASSLA aligned)

Columns 7-8 are compared directly (HEAD and DEPREL), with concrete token examples.

## Scope
- Gold sentences: 1282
- Trankit aligned sentences: 1282
- CLASSLA aligned sentences: 1282

## Trankit aligned - error content tables
- Compared tokens: 25442
- LAS-correct tokens: 24037 (94.48%)

### A) HEAD wrong, DEPREL correct
| Rank | Gold DEPREL | Pred DEPREL | Count | Example |
|---|---|---|---:|---|
| 1 | punct | (same DEPREL, wrong HEAD) | 199 (0.78%) | sid=ssj562.2919.10334; tok="#4; gold=(6,punct); pred=(5,punct); text="Namreč po zdravi "kmečki pameti" in lastnih izkušnjah še nobena reforma ni prinesla nečesa ve..." |
| 2 | advmod | (same DEPREL, wrong HEAD) | 94 (0.37%) | sid=ssj562.2919.10334; tok=še#11; gold=(13,advmod); pred=(15,advmod); text="Namreč po zdravi "kmečki pameti" in lastnih izkušnjah še nobena reforma ni prinesla nečesa ve..." |
| 3 | nmod | (same DEPREL, wrong HEAD) | 83 (0.33%) | sid=ssj562.2923.10352; tok=Čepinci#17; gold=(14,nmod); pred=(16,nmod); text="Tukaj srečamo več avtomobilov z madžarskimi registracijami, saj je v bližini mejni prehod z M..." |
| 4 | conj | (same DEPREL, wrong HEAD) | 77 (0.30%) | sid=ssj562.2919.10334; tok=izkušnjah#10; gold=(6,conj); pred=(5,conj); text="Namreč po zdravi "kmečki pameti" in lastnih izkušnjah še nobena reforma ni prinesla nečesa ve..." |
| 5 | obl | (same DEPREL, wrong HEAD) | 30 (0.12%) | sid=ssj562.2923.10351; tok=enem#2; gold=(8,obl); pred=(11,obl); text="V enem od "centrov" Čepinec so še vedno neobnovljene stavbe, je pa tam kot posebnost velika l..." |
| 6 | parataxis | (same DEPREL, wrong HEAD) | 30 (0.12%) | sid=ssj562.2923.10351; tok=je#14; gold=(8,parataxis); pred=(11,parataxis); text="V enem od "centrov" Čepinec so še vedno neobnovljene stavbe, je pa tam kot posebnost velika l..." |
| 7 | advcl | (same DEPREL, wrong HEAD) | 22 (0.09%) | sid=ssj563.2928.10376; tok=interpelirana#34; gold=(29,advcl); pred=(28,advcl); text="Skupaj s »pozitivnim« konceptom ideologije (ideologija je družbena vez) moramo pač razviti tu..." |
| 8 | acl | (same DEPREL, wrong HEAD) | 22 (0.09%) | sid=ssj563.2929.10383; tok=posledica#47; gold=(39,acl); pred=(37,acl); text="Sedanji kulturnorelativistični »trend« je namreč uvoz iz ZDA; a v ZDA se je kulturni relativi..." |
| 9 | cc | (same DEPREL, wrong HEAD) | 20 (0.08%) | sid=ssj563.2927.10374; tok=Ali#1; gold=(4,cc); pred=(9,cc); text="Ali, preprosto povedano: iz koncepta je mogoče izpeljati domačinsko predstavo, iz domačinske ..." |
| 10 | appos | (same DEPREL, wrong HEAD) | 17 (0.07%) | sid=ssj565.2934.10401; tok=vidika#26; gold=(23,appos); pred=(18,appos); text="Mimi Podkrižnik Komisijo za šolsko prehrano sestavljajo ravnatelj ali pomočnik, vodja šolske ..." |
| 11 | cop | (same DEPREL, wrong HEAD) | 14 (0.06%) | sid=ssj566.2935.10408; tok=je#7; gold=(9,cop); pred=(1,cop); text="Ena od odlik knjižne zbirke Scripta je njena neprofitnost, ki nam ob finančni pomoči ŠOU omog..." |
| 12 | mark | (same DEPREL, wrong HEAD) | 13 (0.05%) | sid=ssj570.2943.10447; tok=da#5; gold=(6,mark); pred=(8,mark); text="// Recimo, da ste kadrovski direktor in da je vaše delo preverjanje kandidatov ter zaposlovan..." |
| 13 | aux | (same DEPREL, wrong HEAD) | 12 (0.05%) | sid=ssj563.2931.10394; tok=bi#8; gold=(10,aux); pred=(9,aux); text="Če se že poskušamo z anahronizmi, bi bilo produktivneje Himenino ljubezen razumeti kot protes..." |
| 14 | case | (same DEPREL, wrong HEAD) | 10 (0.04%) | sid=ssj562.2919.10334; tok=po#2; gold=(6,case); pred=(5,case); text="Namreč po zdravi "kmečki pameti" in lastnih izkušnjah še nobena reforma ni prinesla nečesa ve..." |
| 15 | nsubj | (same DEPREL, wrong HEAD) | 9 (0.04%) | sid=ssj562.2923.10351; tok=stavbe#12; gold=(8,nsubj); pred=(11,nsubj); text="V enem od "centrov" Čepinec so še vedno neobnovljene stavbe, je pa tam kot posebnost velika l..." |
| 16 | amod | (same DEPREL, wrong HEAD) | 8 (0.03%) | sid=ssj562.2919.10334; tok=zdravi#3; gold=(6,amod); pred=(5,amod); text="Namreč po zdravi "kmečki pameti" in lastnih izkušnjah še nobena reforma ni prinesla nečesa ve..." |
| 17 | obj | (same DEPREL, wrong HEAD) | 4 (0.02%) | sid=ssj594.3050.10807; tok=kaj#4; gold=(8,obj); pred=(7,obj); text="Tuhtal je, kaj vse ji mora povedati, da bo hotela ostati." |
| 18 | det | (same DEPREL, wrong HEAD) | 4 (0.02%) | sid=ssj607.3126.11108; tok=kakih#26; gold=(28,det); pred=(27,det); text="Na začetku decembra 2000 je Nasa s pomočjo antene s premerom 70 m v kalifornijskem observator..." |
| 19 | nummod | (same DEPREL, wrong HEAD) | 3 (0.01%) | sid=ssj590.3028.10719; tok=19#40; gold=(39,nummod); pred=(41,nummod); text="Ker se 19-palčni monitorji z visoko ločljivostjo niso »prijeli« med uporabniki, je kmalu veči..." |
| 20 | expl | (same DEPREL, wrong HEAD) | 3 (0.01%) | sid=ssj596.3066.10859; tok=se#3; gold=(4,expl); pred=(5,expl); text="Kmetice so se bale delati v dneh, ki jih je torka prepovedovala." |

### B) HEAD correct, DEPREL wrong
| Rank | Gold DEPREL | Pred DEPREL | Count | Example |
|---|---|---|---:|---|
| 1 | iobj | obj | 17 (0.07%) | sid=ssj562.2919.10336; tok=besedi#7; gold=(6,iobj); pred=(6,obj); text="Ob tem sem se namenoma izognil besedi denarja, saj lahko gre tudi za druge stvari." |
| 2 | obj | iobj | 15 (0.06%) | sid=ssj563.2926.10367; tok=individua#5; gold=(16,obj); pred=(16,iobj); text="Zato nacionalna ničta institucija individua, ki ga je zgrabila v svoj interpelacijski mehaniz..." |
| 3 | nmod | flat | 14 (0.06%) | sid=ssj567.2936.10414; tok=Lafayette#24; gold=(23,nmod); pred=(23,flat); text="Če pa vam raziskovalni duh ne da posedati v sobi, se lahko podate po nakupih v bližnji največ..." |
| 4 | orphan | advmod | 11 (0.04%) | sid=ssj562.2919.10334; tok=predvsem#23; gold=(27,orphan); pred=(27,advmod); text="Namreč po zdravi "kmečki pameti" in lastnih izkušnjah še nobena reforma ni prinesla nečesa ve..." |
| 5 | conj | parataxis | 11 (0.04%) | sid=ssj562.2924.10358; tok=olupimo#6; gold=(2,conj); pred=(2,parataxis); text="Krompir operemo, skuhamo, olupimo in pretlačimo." |
| 6 | nsubj | obj | 10 (0.04%) | sid=ssj573.2950.10479; tok=Čas#1; gold=(5,nsubj); pred=(5,obj); text="Čas enega obrata t0 izmerijo s pomočjo sunkov iz merilne tuljavice, ki je pritrjena na vilice..." |
| 7 | obj | nsubj | 8 (0.03%) | sid=ssj565.2934.10406; tok=vodjo#22; gold=(21,obj); pred=(21,nsubj); text="»Glavno merilo pri dobavljanju hrane - nabava poteka na podlagi javnega razpisa - je vse prep..." |
| 8 | parataxis | conj | 7 (0.03%) | sid=ssj579.2969.10534; tok=poskusili#8; gold=(6,parataxis); pred=(6,conj); text="Na obeh tekmah smo dobro igrali, poskusili vse, a žal smo bili prekratki za en gol in smo se ..." |
| 9 | nmod | obl | 7 (0.03%) | sid=ssj596.3060.10840; tok=kroge#10; gold=(7,nmod); pred=(7,obl); text="Slavna slovenska potica, povitica, povita v zapeljive kroge, napolnjene z orehi, lešniki, sku..." |
| 10 | cc | advmod | 6 (0.02%) | sid=ssj568.2937.10418; tok=tako#8; gold=(9,cc); pred=(9,advmod); text="Zmanjševanje javne porabe se mu ne zdi tako pomembno kot njeno pravilno uravnoteženje, to, da..." |
| 11 | appos | nmod | 6 (0.02%) | sid=ssj579.2985.10579; tok=uri#9; gold=(3,appos); pred=(3,nmod); text="KRŠKO: 25. in 26. (ob 20. uri) in 28. 1. (ob 18. uri) ameriška akcijska komedija Apollo 13." |
| 12 | advmod | cc | 5 (0.02%) | sid=ssj562.2919.10334; tok=Namreč#1; gold=(15,advmod); pred=(15,cc); text="Namreč po zdravi "kmečki pameti" in lastnih izkušnjah še nobena reforma ni prinesla nečesa ve..." |
| 13 | conj | flat | 5 (0.02%) | sid=ssj570.2945.10468; tok=Row#5; gold=(3,conj); pred=(3,flat); text="Psychology, Harper& Row, New York, 1987." |
| 14 | advmod | obl | 5 (0.02%) | sid=ssj578.2960.10504; tok=prihodnje#11; gold=(12,advmod); pred=(12,obl); text="In kdo bo tisti, ki se bo moral v prihodnje spopadati s »pritiski, prisiljenimi odločitvami, ..." |
| 15 | nmod | appos | 5 (0.02%) | sid=ssj579.2976.10560; tok=praznik#10; gold=(4,nmod); pred=(4,appos); text="TREBNJE - V soboto, 6. januarja, na praznik sv. treh kraljev," |
| 16 | appos | conj | 5 (0.02%) | sid=ssj581.2995.10606; tok=norm#13; gold=(11,appos); pred=(11,conj); text="Njegova Teorija Idej je potrdila nadzor vedenja s pomočjo avtoritarnih konceptov - norm tako,..." |
| 17 | advcl | ccomp | 4 (0.02%) | sid=ssj563.2926.10367; tok=prepusti#20; gold=(16,advcl); pred=(16,ccomp); text="Zato nacionalna ničta institucija individua, ki ga je zgrabila v svoj interpelacijski mehaniz..." |
| 18 | iobj | expl | 4 (0.02%) | sid=ssj567.2936.10413; tok=si#21; gold=(24,iobj); pred=(24,expl); text="Prepustite pa se lahko tudi vsem prepotrebnim udobnostim, od crkljanja v najmehkejši halji in..." |
| 19 | amod | nmod | 4 (0.02%) | sid=ssj579.2970.10537; tok=trafo#16; gold=(17,amod); pred=(17,nmod); text="Ekipe Elektra so še vedno na terenu in je bilo ponoči zunaj napetosti še 6 trafo postaj na te..." |
| 20 | nmod | amod | 4 (0.02%) | sid=ssj589.3025.10692; tok=najdaljših#14; gold=(13,nmod); pred=(13,amod); text="Obdobje, v katerem se je končala človekova biološka evolucija, je eno najdaljših in najbolj d..." |

### C) HEAD wrong, DEPREL wrong
| Rank | Gold DEPREL | Pred DEPREL | Count | Example |
|---|---|---|---:|---|
| 1 | obl | nmod | 40 (0.16%) | sid=ssj562.2919.10334; tok=pameti#6; gold=(15,obl); pred=(5,nmod); text="Namreč po zdravi "kmečki pameti" in lastnih izkušnjah še nobena reforma ni prinesla nečesa ve..." |
| 2 | nmod | obl | 38 (0.15%) | sid=ssj562.2925.10364; tok=zaključku#17; gold=(15,nmod); pred=(12,obl); text="Pred leti pa se je njegova kreacija, ki jo je izdelal za modno revijo ob zaključku srednje šo..." |
| 3 | parataxis | root | 24 (0.09%) | sid=ssj563.2927.10374; tok=mogoče#9; gold=(4,parataxis); pred=(0,root); text="Ali, preprosto povedano: iz koncepta je mogoče izpeljati domačinsko predstavo, iz domačinske ..." |
| 4 | root | parataxis | 14 (0.06%) | sid=ssj563.2927.10374; tok=povedano#4; gold=(0,root); pred=(9,parataxis); text="Ali, preprosto povedano: iz koncepta je mogoče izpeljati domačinsko predstavo, iz domačinske ..." |
| 5 | parataxis | appos | 11 (0.04%) | sid=ssj576.2956.10496; tok=razstava#11; gold=(9,parataxis); pred=(4,appos); text="< Flash> Gorenje d. d., razstavni prostor: razstava slik akademskega slikarja Tomaža Gorjupa,..." |
| 6 | advcl | acl | 9 (0.04%) | sid=ssj562.2919.10333; tok=opisuje#10; gold=(3,advcl); pred=(6,acl); text="Deloma se strinjam z drugim delom članka, ko opisuje finančne učinke reforme." |
| 7 | nsubj | root | 9 (0.04%) | sid=ssj566.2935.10408; tok=Ena#1; gold=(9,nsubj); pred=(0,root); text="Ena od odlik knjižne zbirke Scripta je njena neprofitnost, ki nam ob finančni pomoči ŠOU omog..." |
| 8 | root | ccomp | 7 (0.03%) | sid=ssj565.2934.10406; tok=cena#18; gold=(0,root); pred=(21,ccomp); text="»Glavno merilo pri dobavljanju hrane - nabava poteka na podlagi javnega razpisa - je vse prep..." |
| 9 | root | cop | 6 (0.02%) | sid=ssj562.2923.10351; tok=so#8; gold=(0,root); pred=(11,cop); text="V enem od "centrov" Čepinec so še vedno neobnovljene stavbe, je pa tam kot posebnost velika l..." |
| 10 | root | nsubj | 6 (0.02%) | sid=ssj566.2935.10408; tok=neprofitnost#9; gold=(0,root); pred=(1,nsubj); text="Ena od odlik knjižne zbirke Scripta je njena neprofitnost, ki nam ob finančni pomoči ŠOU omog..." |
| 11 | conj | advmod | 5 (0.02%) | sid=ssj570.2939.10433; tok=malo#13; gold=(7,conj); pred=(16,advmod); text="Morda vi kot tarča prevare sploh nimate nič ali pa vsaj zelo malo z njegovo odločitvijo, da b..." |
| 12 | nmod | appos | 5 (0.02%) | sid=ssj590.3029.10720; tok=In#4; gold=(5,nmod); pred=(1,appos); text="Zaslone IPS (In Plane Switching) sta leta 1996 razvila Hitachi in NEC." |
| 13 | nmod | flat | 5 (0.02%) | sid=ssj590.3029.10720; tok=Plane#5; gold=(6,nmod); pred=(4,flat); text="Zaslone IPS (In Plane Switching) sta leta 1996 razvila Hitachi in NEC." |
| 14 | acl | advcl | 4 (0.02%) | sid=ssj563.2931.10395; tok=navzame#36; gold=(32,acl); pred=(27,advcl); text="(Glede na eno izmed teorij o trubadurski poeziji, po kateri naj bi to novo občutenje individu..." |
| 15 | parataxis | nummod | 4 (0.02%) | sid=ssj578.2965.10516; tok=17.#9; gold=(6,parataxis); pred=(8,nummod); text="Na polovici proge je bil 11. (Zrimšek 17. s pet sekund slabšim časom), v tretji četrtini 8. (..." |
| 16 | obj | nmod | 4 (0.02%) | sid=ssj579.2969.10533; tok=ekip#15; gold=(9,obj); pred=(12,nmod); text="Žreb nam ni bil naklonjen, saj smo imeli za nasprotnika eno najboljših evropskih ekip, rokome..." |
| 17 | nsubj | amod | 4 (0.02%) | sid=ssj579.2977.10562; tok=same#27; gold=(25,nsubj); pred=(29,amod); text="Ta je bil ptič v Čarodeju Fikfiku, in ker je bil ves razigran, so ga lutkarice vzele za svojo..." |
| 18 | orphan | conj | 4 (0.02%) | sid=ssj579.2982.10574; tok=lep#9; gold=(7,orphan); pred=(3,conj); text="Tam postane neumni - pameten, grdi - lep in revež - bogataš." |
| 19 | conj | flat | 4 (0.02%) | sid=ssj579.2991.10593; tok=595#19; gold=(17,conj); pred=(15,flat); text="ODKUPUJEMO HLODOVINO hrasta, bukve, smreke, jelke in kostanja.+ (061) 218-595 ali (0609) 620-..." |
| 20 | nsubj | nmod | 4 (0.02%) | sid=ssj583.2999.10621; tok=Vida#18; gold=(14,nsubj); pred=(17,nmod); text="60 LET SKUPNEGA ŽIVLJENJA - Konec tega tedna bosta v krogu svojih najbližjih praznovala 60. o..." |

## CLASSLA aligned - error content tables
- Compared tokens: 25442
- LAS-correct tokens: 23021 (90.48%)

### A) HEAD wrong, DEPREL correct
| Rank | Gold DEPREL | Pred DEPREL | Count | Example |
|---|---|---|---:|---|
| 1 | punct | (same DEPREL, wrong HEAD) | 355 (1.40%) | sid=ssj562.2919.10334; tok=,#18; gold=(20,punct); pred=(31,punct); text="Namreč po zdravi "kmečki pameti" in lastnih izkušnjah še nobena reforma ni prinesla nečesa ve..." |
| 2 | advmod | (same DEPREL, wrong HEAD) | 161 (0.63%) | sid=ssj562.2919.10334; tok=kvečjemu#19; gold=(20,advmod); pred=(31,advmod); text="Namreč po zdravi "kmečki pameti" in lastnih izkušnjah še nobena reforma ni prinesla nečesa ve..." |
| 3 | nmod | (same DEPREL, wrong HEAD) | 116 (0.46%) | sid=ssj562.2921.10339; tok=pokal#8; gold=(4,nmod); pred=(6,nmod); text="Na nedavnem mednarodnem turnirju mladih judoistov za pokal Ptuja je sodelovalo 285 tekmovalce..." |
| 4 | conj | (same DEPREL, wrong HEAD) | 108 (0.42%) | sid=ssj562.2922.10342; tok=kuhane#19; gold=(16,conj); pred=(13,conj); text="V primerjavi s krompirjem pa lahko topinambur brez bojazni za zdravje uživamo surov, torej sv..." |
| 5 | obl | (same DEPREL, wrong HEAD) | 76 (0.30%) | sid=ssj562.2922.10343; tok=krompirjevih#17; gold=(13,obl); pred=(15,obl); text="Sveži gomolji imajo svojevrsten okus; kuhani, dušeni ali pečeni so sočnejši in rahlejši od kr..." |
| 6 | acl | (same DEPREL, wrong HEAD) | 52 (0.20%) | sid=ssj562.2920.10338; tok=izražena#20; gold=(16,acl); pred=(14,acl); text="Ta v primeru potrebe po svoji presoji napoti bolnika k specialistu na sekundarnem nivoju z na..." |
| 7 | cc | (same DEPREL, wrong HEAD) | 39 (0.15%) | sid=ssj562.2922.10342; tok=torej#15; gold=(20,cc); pred=(16,cc); text="V primerjavi s krompirjem pa lahko topinambur brez bojazni za zdravje uživamo surov, torej sv..." |
| 8 | parataxis | (same DEPREL, wrong HEAD) | 37 (0.15%) | sid=ssj562.2923.10346; tok=nekaj#24; gold=(17,parataxis); pred=(7,parataxis); text="Čepinci se vsaj po kažipotu čisto držijo Markovec, čeprav to v praksi pomeni, da je nekaj hiš..." |
| 9 | aux | (same DEPREL, wrong HEAD) | 37 (0.15%) | sid=ssj563.2931.10394; tok=bi#8; gold=(10,aux); pred=(9,aux); text="Če se že poskušamo z anahronizmi, bi bilo produktivneje Himenino ljubezen razumeti kot protes..." |
| 10 | mark | (same DEPREL, wrong HEAD) | 34 (0.13%) | sid=ssj563.2928.10378; tok=da#14; gold=(18,mark); pred=(17,mark); text="Če jih institucija sili v hipokrizijo, je razlog navadno v tem, da institucionalnih zahtev ni..." |
| 11 | nsubj | (same DEPREL, wrong HEAD) | 30 (0.12%) | sid=ssj563.2929.10385; tok=Amerika#1; gold=(4,nsubj); pred=(3,nsubj); text="Amerika je povečevalno ogledalo, v katerem Evropa ogleduje svoje mračno naličje v zvečanem me..." |
| 12 | cop | (same DEPREL, wrong HEAD) | 29 (0.11%) | sid=ssj563.2927.10371; tok=so#11; gold=(26,cop); pred=(13,cop); text="Logika strukture zahteva družbene prakse, jih konstituira, zato so te prakse že od vsega zače..." |
| 13 | advcl | (same DEPREL, wrong HEAD) | 27 (0.11%) | sid=ssj563.2928.10378; tok=sili#4; gold=(8,advcl); pred=(9,advcl); text="Če jih institucija sili v hipokrizijo, je razlog navadno v tem, da institucionalnih zahtev ni..." |
| 14 | appos | (same DEPREL, wrong HEAD) | 19 (0.07%) | sid=ssj565.2934.10401; tok=vidika#26; gold=(23,appos); pred=(18,appos); text="Mimi Podkrižnik Komisijo za šolsko prehrano sestavljajo ravnatelj ali pomočnik, vodja šolske ..." |
| 15 | csubj | (same DEPREL, wrong HEAD) | 17 (0.07%) | sid=ssj563.2927.10374; tok=izpeljati#10; gold=(9,csubj); pred=(8,csubj); text="Ali, preprosto povedano: iz koncepta je mogoče izpeljati domačinsko predstavo, iz domačinske ..." |
| 16 | case | (same DEPREL, wrong HEAD) | 17 (0.07%) | sid=ssj578.2965.10516; tok=s#10; gold=(14,case); pred=(12,case); text="Na polovici proge je bil 11. (Zrimšek 17. s pet sekund slabšim časom), v tretji četrtini 8. (..." |
| 17 | obj | (same DEPREL, wrong HEAD) | 11 (0.04%) | sid=ssj562.2921.10340; tok=nobenemu#10; gold=(12,obj); pred=(13,obj); text="Pomurci so osvojili kopico visokih mest, a se nobenemu ni uspelo povzpeti na najvišjo stopničko." |
| 18 | amod | (same DEPREL, wrong HEAD) | 10 (0.04%) | sid=ssj593.3041.10777; tok=mastne#12; gold=(16,amod); pred=(10,amod); text="Sadje in zelenjava imata zaradi svoje pestrosti ponudbe zeleno luč, mastne in preveč kaloričn..." |
| 19 | expl | (same DEPREL, wrong HEAD) | 6 (0.02%) | sid=ssj570.2939.10432; tok=se#2; gold=(3,expl); pred=(5,expl); text="Morda se počuti primoranega lagati iz strahu ali nesposobnosti predvideti posledice pogovora." |
| 20 | orphan | (same DEPREL, wrong HEAD) | 4 (0.02%) | sid=ssj565.2934.10404; tok=pa#27; gold=(28,orphan); pred=(26,orphan); text="Malica je pri nas uvrščena v nacionalni oziroma zagotovljeni program financiranja, torej dobi..." |

### B) HEAD correct, DEPREL wrong
| Rank | Gold DEPREL | Pred DEPREL | Count | Example |
|---|---|---|---:|---|
| 1 | obj | nsubj | 30 (0.12%) | sid=ssj562.2923.10346; tok=Markovec#8; gold=(7,obj); pred=(7,nsubj); text="Čepinci se vsaj po kažipotu čisto držijo Markovec, čeprav to v praksi pomeni, da je nekaj hiš..." |
| 2 | obj | iobj | 29 (0.11%) | sid=ssj563.2926.10368; tok=jim#40; gold=(43,obj); pred=(43,iobj); text="Na drugi strani so vse ideologije, ki delujejo v nacionalno konstituiranem »diskurzivnem veso..." |
| 3 | nsubj | obj | 28 (0.11%) | sid=ssj562.2923.10352; tok=pot#28; gold=(29,nsubj); pred=(29,obj); text="Tukaj srečamo več avtomobilov z madžarskimi registracijami, saj je v bližini mejni prehod z M..." |
| 4 | conj | parataxis | 16 (0.06%) | sid=ssj562.2924.10358; tok=skuhamo#4; gold=(2,conj); pred=(2,parataxis); text="Krompir operemo, skuhamo, olupimo in pretlačimo." |
| 5 | nmod | flat | 12 (0.05%) | sid=ssj579.2977.10562; tok=Fikfiku#7; gold=(6,nmod); pred=(6,flat); text="Ta je bil ptič v Čarodeju Fikfiku, in ker je bil ves razigran, so ga lutkarice vzele za svojo..." |
| 6 | obl | nsubj | 11 (0.04%) | sid=ssj570.2941.10440; tok=mikroznaki#28; gold=(26,obl); pred=(26,nsubj); text="Sporazumevamo se z nebesednim vedenjem ali telesnim jezikom, s kvaliteto glasu, z vsebino gov..." |
| 7 | iobj | obj | 10 (0.04%) | sid=ssj562.2924.10359; tok=masi#14; gold=(12,iobj); pred=(12,obj); text="Posebej skuhamo cvetačo in brokoli, odcedimo, grobo nasekljamo ter dodamo krompirjevi masi, v..." |
| 8 | appos | conj | 10 (0.04%) | sid=ssj579.2980.10568; tok=torek#30; gold=(25,appos); pred=(25,conj); text="Ker pomeni kršenje ali samovoljno spreminjanje dogovora, ki so ga sprejeli v Moharju, razlog ..." |
| 9 | cc | advmod | 9 (0.04%) | sid=ssj568.2937.10418; tok=tako#8; gold=(9,cc); pred=(9,advmod); text="Zmanjševanje javne porabe se mu ne zdi tako pomembno kot njeno pravilno uravnoteženje, to, da..." |
| 10 | flat | nmod | 9 (0.04%) | sid=ssj594.3044.10788; tok=permiso#3; gold=(2,flat); pred=(2,nmod); text="»Con permiso!« je zavpil bolniški strežnik." |
| 11 | conj | appos | 8 (0.03%) | sid=ssj563.2927.10372; tok=pogojem#33; gold=(29,conj); pred=(29,appos); text="Institucij pa ni, če ne obstajajo tudi »v glavah«: domačinske predstave so potemtakem integra..." |
| 12 | iobj | expl | 8 (0.03%) | sid=ssj567.2936.10413; tok=si#21; gold=(24,iobj); pred=(24,expl); text="Prepustite pa se lahko tudi vsem prepotrebnim udobnostim, od crkljanja v najmehkejši halji in..." |
| 13 | obl | obj | 7 (0.03%) | sid=ssj578.2964.10514; tok=katerega#20; gold=(19,obl); pred=(19,obj); text="Oboje, kostanj in dobra družba, se obetata v naslednjih nekaj tednih vsem, ki se boste udelež..." |
| 14 | advmod | amod | 6 (0.02%) | sid=ssj563.2931.10391; tok=zgodnje#7; gold=(8,advmod); pred=(8,amod); text="Vseeno je tudi v tej »zgodnje moderni« različici konflikt vreden antropološke pozornosti: saj..." |
| 15 | nsubj | obl | 6 (0.02%) | sid=ssj581.2995.10605; tok=ideje#32; gold=(23,nsubj); pred=(23,obl); text="Ironično je, da je to storil ravno v trenutku, ko so lokalno in družbeno specifične, v obredi..." |
| 16 | obl | nmod | 5 (0.02%) | sid=ssj563.2927.10372; tok=praksah#23; gold=(19,obl); pred=(19,nmod); text="Institucij pa ni, če ne obstajajo tudi »v glavah«: domačinske predstave so potemtakem integra..." |
| 17 | advmod | nsubj | 5 (0.02%) | sid=ssj579.2974.10557; tok=vedro#8; gold=(9,advmod); pred=(9,nsubj); text="Svet pripada tistemu, ki v njem vedro koraka k visokim ciljem." |
| 18 | conj | flat | 5 (0.02%) | sid=ssj579.2991.10593; tok=218#17; gold=(15,conj); pred=(15,flat); text="ODKUPUJEMO HLODOVINO hrasta, bukve, smreke, jelke in kostanja.+ (061) 218-595 ali (0609) 620-..." |
| 19 | nmod | amod | 5 (0.02%) | sid=ssj589.3025.10692; tok=najdaljših#14; gold=(13,nmod); pred=(13,amod); text="Obdobje, v katerem se je končala človekova biološka evolucija, je eno najdaljših in najbolj d..." |
| 20 | nmod | obl | 4 (0.02%) | sid=ssj562.2919.10334; tok=možnosti#30; gold=(31,nmod); pred=(31,obl); text="Namreč po zdravi "kmečki pameti" in lastnih izkušnjah še nobena reforma ni prinesla nečesa ve..." |

### C) HEAD wrong, DEPREL wrong
| Rank | Gold DEPREL | Pred DEPREL | Count | Example |
|---|---|---|---:|---|
| 1 | obl | nmod | 89 (0.35%) | sid=ssj562.2920.10338; tok=napotnico#16; gold=(8,obl); pred=(14,nmod); text="Ta v primeru potrebe po svoji presoji napoti bolnika k specialistu na sekundarnem nivoju z na..." |
| 2 | nmod | obl | 62 (0.24%) | sid=ssj562.2925.10363; tok=izboru#18; gold=(16,nmod); pred=(13,obl); text="Posebej opazna je bila pred časom njegova kreacija, ki jo je nosila ena od finalistk na izbor..." |
| 3 | root | cop | 28 (0.11%) | sid=ssj562.2925.10366; tok=je#2; gold=(0,root); pred=(1,cop); text="Mnenja je namreč, da do uspeha v tem poklicu lahko pripelje predvsem prepoznavnost, zato tudi..." |
| 4 | nsubj | root | 24 (0.09%) | sid=ssj563.2928.10378; tok=razlog#9; gold=(8,nsubj); pred=(0,root); text="Če jih institucija sili v hipokrizijo, je razlog navadno v tem, da institucionalnih zahtev ni..." |
| 5 | parataxis | root | 23 (0.09%) | sid=ssj576.2956.10496; tok=Flash#2; gold=(4,parataxis); pred=(0,root); text="< Flash> Gorenje d. d., razstavni prostor: razstava slik akademskega slikarja Tomaža Gorjupa,..." |
| 6 | root | parataxis | 18 (0.07%) | sid=ssj564.2932.10399; tok=pride#13; gold=(0,root); pred=(2,parataxis); text="Čeprav živi skoraj ves čas pod vodo, kar nekajkrat na uro pride na površino, da zajame zrak." |
| 7 | cop | root | 15 (0.06%) | sid=ssj563.2927.10373; tok=je#5; gold=(7,cop); pred=(0,root); text="Iz koncepta logike strukture je potemtakem mogoče izpeljati, kako domačinske predstave posred..." |
| 8 | root | nsubj | 13 (0.05%) | sid=ssj578.2960.10504; tok=kdo#2; gold=(0,root); pred=(4,nsubj); text="In kdo bo tisti, ki se bo moral v prihodnje spopadati s »pritiski, prisiljenimi odločitvami, ..." |
| 9 | advcl | acl | 12 (0.05%) | sid=ssj564.2932.10399; tok=zajame#18; gold=(13,advcl); pred=(15,acl); text="Čeprav živi skoraj ves čas pod vodo, kar nekajkrat na uro pride na površino, da zajame zrak." |
| 10 | obj | nmod | 11 (0.04%) | sid=ssj563.2926.10367; tok=individua#5; gold=(16,obj); pred=(4,nmod); text="Zato nacionalna ničta institucija individua, ki ga je zgrabila v svoj interpelacijski mehaniz..." |
| 11 | nsubj | conj | 10 (0.04%) | sid=ssj563.2927.10371; tok=prakse#13; gold=(26,nsubj); pred=(8,conj); text="Logika strukture zahteva družbene prakse, jih konstituira, zato so te prakse že od vsega zače..." |
| 12 | nmod | nsubj | 10 (0.04%) | sid=ssj579.2993.10595; tok=vse#16; gold=(15,nmod); pred=(17,nsubj); text="Kako je s planinskim orlom v Sloveniji, koliko je še teh ptic, kje vse gnezdi, kaj ga ogroža ..." |
| 13 | parataxis | appos | 9 (0.04%) | sid=ssj562.2919.10334; tok=način#27; gold=(15,parataxis); pred=(21,appos); text="Namreč po zdravi "kmečki pameti" in lastnih izkušnjah še nobena reforma ni prinesla nečesa ve..." |
| 14 | nsubj | parataxis | 9 (0.04%) | sid=ssj562.2922.10343; tok=kuhani#7; gold=(13,nsubj); pred=(3,parataxis); text="Sveži gomolji imajo svojevrsten okus; kuhani, dušeni ali pečeni so sočnejši in rahlejši od kr..." |
| 15 | conj | cop | 9 (0.04%) | sid=ssj579.2970.10537; tok=bilo#10; gold=(3,conj); pred=(17,cop); text="Ekipe Elektra so še vedno na terenu in je bilo ponoči zunaj napetosti še 6 trafo postaj na te..." |
| 16 | cc | advmod | 8 (0.03%) | sid=ssj563.2931.10392; tok=ne#14; gold=(15,cc); pred=(19,advmod); text="Torej za konflikt, ki ga v načelu ni mogoče zadovoljivo rešiti: ne družba ne posameznica ne z..." |
| 17 | nsubj | nmod | 8 (0.03%) | sid=ssj578.2965.10519; tok=kolesar#26; gold=(22,nsubj); pred=(24,nmod); text="Na EP mi je manjkalo svežine, ki sem jo na SP ohranil, kar je bilo odločilno,« je komentiral ..." |
| 18 | acl | advcl | 7 (0.03%) | sid=ssj578.2960.10507; tok=prisluhnil#22; gold=(14,acl); pred=(10,advcl); text="To pomeni, da ju bo upravni odbor zavoda obravnaval na prvi naslednji seji (23. oktobra), ko ..." |
| 19 | root | ccomp | 7 (0.03%) | sid=ssj579.2972.10549; tok=uporabljamo#4; gold=(0,root); pred=(20,ccomp); text="Tako še vedno uporabljamo njene skrinje, v katerih imamo zrnje, v kofancih pa hranimo platno,..." |
| 20 | parataxis | acl | 7 (0.03%) | sid=ssj600.3086.10929; tok=drgnili#18; gold=(10,parataxis); pred=(14,acl); text="Bil sem nemara eden tistih, ki bi jih prešteli na prste ene roke, ki nismo drgnili riti." |

## Direct model comparison (LAS exact)
- Compared tokens: 25442
- Trankit aligned correct, CLASSLA aligned wrong: 1543 (6.06%)
- Trankit aligned wrong, CLASSLA aligned correct: 527 (2.07%)

### Where Trankit aligned is better
| Rank | Gold DEPREL | Loser error pattern | Count | Example |
|---|---|---|---:|---|
| 1 | punct | HEAD wrong, DEPREL punct | 221 (0.87%) | sid=ssj562.2919.10334; tok=,#28; gold=(31,punct); trankit=(31,punct); classla=(27,punct); text="Namreč po zdravi "kmečki pameti" in lastnih izkušnjah še nobena reforma ni prinesla nečesa ve..." |
| 2 | advmod | HEAD wrong, DEPREL advmod | 98 (0.39%) | sid=ssj562.2923.10351; tok=pa#15; gold=(14,advmod); trankit=(14,advmod); classla=(20,advmod); text="V enem od "centrov" Čepinec so še vedno neobnovljene stavbe, je pa tam kot posebnost velika l..." |
| 3 | conj | HEAD wrong, DEPREL conj | 70 (0.28%) | sid=ssj562.2922.10342; tok=kuhane#19; gold=(16,conj); trankit=(16,conj); classla=(13,conj); text="V primerjavi s krompirjem pa lahko topinambur brez bojazni za zdravje uživamo surov, torej sv..." |
| 4 | obl | HEAD wrong + DEPREL obl->nmod | 64 (0.25%) | sid=ssj562.2920.10338; tok=napotnico#16; gold=(8,obl); trankit=(8,obl); classla=(14,nmod); text="Ta v primeru potrebe po svoji presoji napoti bolnika k specialistu na sekundarnem nivoju z na..." |
| 5 | obl | HEAD wrong, DEPREL obl | 57 (0.22%) | sid=ssj562.2922.10343; tok=krompirjevih#17; gold=(13,obl); trankit=(13,obl); classla=(15,obl); text="Sveži gomolji imajo svojevrsten okus; kuhani, dušeni ali pečeni so sočnejši in rahlejši od kr..." |
| 6 | nmod | HEAD wrong, DEPREL nmod | 55 (0.22%) | sid=ssj562.2921.10339; tok=pokal#8; gold=(4,nmod); trankit=(4,nmod); classla=(6,nmod); text="Na nedavnem mednarodnem turnirju mladih judoistov za pokal Ptuja je sodelovalo 285 tekmovalce..." |
| 7 | nmod | HEAD wrong + DEPREL nmod->obl | 42 (0.17%) | sid=ssj562.2925.10363; tok=izboru#18; gold=(16,nmod); trankit=(16,nmod); classla=(13,obl); text="Posebej opazna je bila pred časom njegova kreacija, ki jo je nosila ena od finalistk na izbor..." |
| 8 | acl | HEAD wrong, DEPREL acl | 37 (0.15%) | sid=ssj562.2920.10338; tok=izražena#20; gold=(16,acl); trankit=(16,acl); classla=(14,acl); text="Ta v primeru potrebe po svoji presoji napoti bolnika k specialistu na sekundarnem nivoju z na..." |
| 9 | aux | HEAD wrong, DEPREL aux | 30 (0.12%) | sid=ssj563.2931.10395; tok=bi#26; gold=(27,aux); trankit=(27,aux); classla=(28,aux); text="(Glede na eno izmed teorij o trubadurski poeziji, po kateri naj bi to novo občutenje individu..." |
| 10 | cc | HEAD wrong, DEPREL cc | 29 (0.11%) | sid=ssj562.2922.10342; tok=torej#15; gold=(20,cc); trankit=(20,cc); classla=(16,cc); text="V primerjavi s krompirjem pa lahko topinambur brez bojazni za zdravje uživamo surov, torej sv..." |
| 11 | mark | HEAD wrong, DEPREL mark | 25 (0.10%) | sid=ssj563.2928.10378; tok=da#14; gold=(18,mark); trankit=(18,mark); classla=(17,mark); text="Če jih institucija sili v hipokrizijo, je razlog navadno v tem, da institucionalnih zahtev ni..." |
| 12 | parataxis | HEAD wrong, DEPREL parataxis | 24 (0.09%) | sid=ssj562.2923.10346; tok=nekaj#24; gold=(17,parataxis); trankit=(17,parataxis); classla=(7,parataxis); text="Čepinci se vsaj po kažipotu čisto držijo Markovec, čeprav to v praksi pomeni, da je nekaj hiš..." |
| 13 | nsubj | DEPREL nsubj->obj, HEAD ok | 24 (0.09%) | sid=ssj562.2923.10352; tok=pot#28; gold=(29,nsubj); trankit=(29,nsubj); classla=(29,obj); text="Tukaj srečamo več avtomobilov z madžarskimi registracijami, saj je v bližini mejni prehod z M..." |
| 14 | root | HEAD wrong + DEPREL root->cop | 23 (0.09%) | sid=ssj563.2928.10378; tok=je#8; gold=(0,root); trankit=(0,root); classla=(9,cop); text="Če jih institucija sili v hipokrizijo, je razlog navadno v tem, da institucionalnih zahtev ni..." |
| 15 | obj | DEPREL obj->nsubj, HEAD ok | 22 (0.09%) | sid=ssj562.2923.10346; tok=Markovec#8; gold=(7,obj); trankit=(7,obj); classla=(7,nsubj); text="Čepinci se vsaj po kažipotu čisto držijo Markovec, čeprav to v praksi pomeni, da je nekaj hiš..." |
| 16 | nsubj | HEAD wrong, DEPREL nsubj | 22 (0.09%) | sid=ssj563.2929.10385; tok=Amerika#1; gold=(4,nsubj); trankit=(4,nsubj); classla=(3,nsubj); text="Amerika je povečevalno ogledalo, v katerem Evropa ogleduje svoje mračno naličje v zvečanem me..." |
| 17 | cop | HEAD wrong, DEPREL cop | 20 (0.08%) | sid=ssj563.2927.10371; tok=so#11; gold=(26,cop); trankit=(26,cop); classla=(13,cop); text="Logika strukture zahteva družbene prakse, jih konstituira, zato so te prakse že od vsega zače..." |
| 18 | nsubj | HEAD wrong + DEPREL nsubj->root | 20 (0.08%) | sid=ssj563.2928.10378; tok=razlog#9; gold=(8,nsubj); trankit=(8,nsubj); classla=(0,root); text="Če jih institucija sili v hipokrizijo, je razlog navadno v tem, da institucionalnih zahtev ni..." |
| 19 | obj | DEPREL obj->iobj, HEAD ok | 19 (0.07%) | sid=ssj563.2928.10376; tok=skupini#30; gold=(29,obj); trankit=(29,obj); classla=(29,iobj); text="Skupaj s »pozitivnim« konceptom ideologije (ideologija je družbena vez) moramo pač razviti tu..." |
| 20 | csubj | HEAD wrong, DEPREL csubj | 17 (0.07%) | sid=ssj563.2927.10374; tok=izpeljati#10; gold=(9,csubj); trankit=(9,csubj); classla=(8,csubj); text="Ali, preprosto povedano: iz koncepta je mogoče izpeljati domačinsko predstavo, iz domačinske ..." |

### Where Trankit aligned loses to CLASSLA aligned
| Rank | Gold DEPREL | Loser error pattern | Count | Example |
|---|---|---|---:|---|
| 1 | punct | HEAD wrong, DEPREL punct | 66 (0.26%) | sid=ssj562.2919.10334; tok="#4; gold=(6,punct); trankit=(5,punct); classla=(6,punct); text="Namreč po zdravi "kmečki pameti" in lastnih izkušnjah še nobena reforma ni prinesla nečesa ve..." |
| 2 | conj | HEAD wrong, DEPREL conj | 35 (0.14%) | sid=ssj562.2919.10334; tok=izkušnjah#10; gold=(6,conj); trankit=(5,conj); classla=(6,conj); text="Namreč po zdravi "kmečki pameti" in lastnih izkušnjah še nobena reforma ni prinesla nečesa ve..." |
| 3 | advmod | HEAD wrong, DEPREL advmod | 30 (0.12%) | sid=ssj562.2919.10334; tok=še#11; gold=(13,advmod); trankit=(15,advmod); classla=(13,advmod); text="Namreč po zdravi "kmečki pameti" in lastnih izkušnjah še nobena reforma ni prinesla nečesa ve..." |
| 4 | nmod | HEAD wrong, DEPREL nmod | 23 (0.09%) | sid=ssj578.2964.10512; tok=Tesaliji#9; gold=(6,nmod); trankit=(7,nmod); classla=(6,nmod); text="Kostanj je dobil ime po mestu Kastanis v Tesaliji, v naše kraje pa so ga prinesli Rimljani." |
| 5 | nmod | HEAD wrong + DEPREL nmod->obl | 17 (0.07%) | sid=ssj562.2925.10364; tok=zaključku#17; gold=(15,nmod); trankit=(12,obl); classla=(15,nmod); text="Pred leti pa se je njegova kreacija, ki jo je izdelal za modno revijo ob zaključku srednje šo..." |
| 6 | obl | HEAD wrong + DEPREL obl->nmod | 16 (0.06%) | sid=ssj562.2919.10334; tok=pameti#6; gold=(15,obl); trankit=(5,nmod); classla=(15,obl); text="Namreč po zdravi "kmečki pameti" in lastnih izkušnjah še nobena reforma ni prinesla nečesa ve..." |
| 7 | obl | HEAD wrong, DEPREL obl | 14 (0.06%) | sid=ssj562.2923.10351; tok=enem#2; gold=(8,obl); trankit=(11,obl); classla=(8,obl); text="V enem od "centrov" Čepinec so še vedno neobnovljene stavbe, je pa tam kot posebnost velika l..." |
| 8 | iobj | DEPREL iobj->obj, HEAD ok | 13 (0.05%) | sid=ssj562.2919.10336; tok=besedi#7; gold=(6,iobj); trankit=(6,obj); classla=(6,iobj); text="Ob tem sem se namenoma izognil besedi denarja, saj lahko gre tudi za druge stvari." |
| 9 | parataxis | HEAD wrong, DEPREL parataxis | 13 (0.05%) | sid=ssj579.2975.10559; tok=mogoča#27; gold=(6,parataxis); trankit=(14,parataxis); classla=(6,parataxis); text="Taka prostorska rešitev seveda ne more biti trajna, ker še zdaleč ni najboljša, je pa v danih..." |
| 10 | advcl | HEAD wrong, DEPREL advcl | 12 (0.05%) | sid=ssj563.2928.10376; tok=interpelirana#34; gold=(29,advcl); trankit=(28,advcl); classla=(29,advcl); text="Skupaj s »pozitivnim« konceptom ideologije (ideologija je družbena vez) moramo pač razviti tu..." |
| 11 | appos | HEAD wrong, DEPREL appos | 10 (0.04%) | sid=ssj566.2935.10408; tok=tistih#34; gold=(31,appos); trankit=(29,appos); classla=(31,appos); text="Ena od odlik knjižne zbirke Scripta je njena neprofitnost, ki nam ob finančni pomoči ŠOU omog..." |
| 12 | cc | HEAD wrong, DEPREL cc | 9 (0.04%) | sid=ssj575.2955.10493; tok=in#2; gold=(5,cc); trankit=(3,cc); classla=(5,cc); text="Milijon in sedemsto tisoč ljudi je umrlo v drugi svetovni vojni, da bi nas sedaj ločevali tujci." |
| 13 | acl | HEAD wrong, DEPREL acl | 8 (0.03%) | sid=ssj563.2929.10383; tok=posledica#47; gold=(39,acl); trankit=(37,acl); classla=(39,acl); text="Sedanji kulturnorelativistični »trend« je namreč uvoz iz ZDA; a v ZDA se je kulturni relativi..." |
| 14 | nmod | DEPREL nmod->flat, HEAD ok | 8 (0.03%) | sid=ssj567.2936.10414; tok=Lafayette#24; gold=(23,nmod); trankit=(23,flat); classla=(23,nmod); text="Če pa vam raziskovalni duh ne da posedati v sobi, se lahko podate po nakupih v bližnji največ..." |
| 15 | root | HEAD wrong + DEPREL root->parataxis | 7 (0.03%) | sid=ssj563.2927.10374; tok=povedano#4; gold=(0,root); trankit=(9,parataxis); classla=(0,root); text="Ali, preprosto povedano: iz koncepta je mogoče izpeljati domačinsko predstavo, iz domačinske ..." |
| 16 | cop | HEAD wrong, DEPREL cop | 7 (0.03%) | sid=ssj566.2935.10408; tok=je#7; gold=(9,cop); trankit=(1,cop); classla=(9,cop); text="Ena od odlik knjižne zbirke Scripta je njena neprofitnost, ki nam ob finančni pomoči ŠOU omog..." |
| 17 | orphan | DEPREL orphan->advmod, HEAD ok | 6 (0.02%) | sid=ssj562.2919.10334; tok=pa#24; gold=(27,orphan); trankit=(27,advmod); classla=(27,orphan); text="Namreč po zdravi "kmečki pameti" in lastnih izkušnjah še nobena reforma ni prinesla nečesa ve..." |
| 18 | parataxis | DEPREL parataxis->conj, HEAD ok | 6 (0.02%) | sid=ssj579.2969.10534; tok=poskusili#8; gold=(6,parataxis); trankit=(6,conj); classla=(6,parataxis); text="Na obeh tekmah smo dobro igrali, poskusili vse, a žal smo bili prekratki za en gol in smo se ..." |
| 19 | nmod | DEPREL nmod->obl, HEAD ok | 6 (0.02%) | sid=ssj596.3060.10840; tok=kroge#10; gold=(7,nmod); trankit=(7,obl); classla=(7,nmod); text="Slavna slovenska potica, povitica, povita v zapeljive kroge, napolnjene z orehi, lešniki, sku..." |
| 20 | aux | HEAD wrong, DEPREL aux | 5 (0.02%) | sid=ssj568.2937.10420; tok=je#2; gold=(5,aux); trankit=(1,aux); classla=(5,aux); text="Zagožen je bil nasprotnega mnenja." |
