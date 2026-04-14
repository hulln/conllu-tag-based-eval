# Table-style content comparison (CLASSLA aligned vs Trankit aligned)

Columns 7-8 are compared directly (HEAD and DEPREL), with concrete token examples.

## Scope
- Gold sentences: 1282
- CLASSLA aligned sentences: 1282
- Trankit aligned sentences: 1282

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

## Trankit aligned - error content tables
- Compared tokens: 25442
- LAS-correct tokens: 23171 (91.07%)

### A) HEAD wrong, DEPREL correct
| Rank | Gold DEPREL | Pred DEPREL | Count | Example |
|---|---|---|---:|---|
| 1 | advmod | (same DEPREL, wrong HEAD) | 349 (1.37%) | sid=ssj562.2919.10334; tok=še#11; gold=(13,advmod); pred=(15,advmod); text="Namreč po zdravi "kmečki pameti" in lastnih izkušnjah še nobena reforma ni prinesla nečesa ve..." |
| 2 | punct | (same DEPREL, wrong HEAD) | 330 (1.30%) | sid=ssj562.2919.10334; tok="#4; gold=(6,punct); pred=(5,punct); text="Namreč po zdravi "kmečki pameti" in lastnih izkušnjah še nobena reforma ni prinesla nečesa ve..." |
| 3 | conj | (same DEPREL, wrong HEAD) | 95 (0.37%) | sid=ssj562.2919.10334; tok=izkušnjah#10; gold=(6,conj); pred=(5,conj); text="Namreč po zdravi "kmečki pameti" in lastnih izkušnjah še nobena reforma ni prinesla nečesa ve..." |
| 4 | nmod | (same DEPREL, wrong HEAD) | 86 (0.34%) | sid=ssj562.2923.10352; tok=Čepinci#17; gold=(14,nmod); pred=(16,nmod); text="Tukaj srečamo več avtomobilov z madžarskimi registracijami, saj je v bližini mejni prehod z M..." |
| 5 | obl | (same DEPREL, wrong HEAD) | 49 (0.19%) | sid=ssj562.2922.10344; tok=jed#6; gold=(1,obl); pred=(2,obl); text="Postrežemo ga lahko kot začetno jed, v juhi, prilogah, solatah, za dieto pa je lahko samostoj..." |
| 6 | parataxis | (same DEPREL, wrong HEAD) | 46 (0.18%) | sid=ssj563.2927.10372; tok=sodijo#25; gold=(19,parataxis); pred=(3,parataxis); text="Institucij pa ni, če ne obstajajo tudi »v glavah«: domačinske predstave so potemtakem integra..." |
| 7 | acl | (same DEPREL, wrong HEAD) | 27 (0.11%) | sid=ssj563.2929.10383; tok=posledica#47; gold=(39,acl); pred=(37,acl); text="Sedanji kulturnorelativistični »trend« je namreč uvoz iz ZDA; a v ZDA se je kulturni relativi..." |
| 8 | nsubj | (same DEPREL, wrong HEAD) | 21 (0.08%) | sid=ssj562.2920.10337; tok=element#8; gold=(13,nsubj); pred=(4,nsubj); text="Sedanje stanje bi strnil takole: Odločilen element zdravljenja bolnika je izbrani zdravnik na..." |
| 9 | cc | (same DEPREL, wrong HEAD) | 21 (0.08%) | sid=ssj562.2925.10361; tok=vendar#11; gold=(12,cc); pred=(14,cc); text="Glede študija pravi, da mu daje nekaj znanja, vendar je to premalo, zato tudi občasno honorar..." |
| 10 | advcl | (same DEPREL, wrong HEAD) | 20 (0.08%) | sid=ssj563.2928.10379; tok=obstaja#61; gold=(51,advcl); pred=(8,advcl); text="24 Iz tega škripca se je mogoče rešiti tako, da posameznik in posameznica »aktivirata« kakšno..." |
| 11 | cop | (same DEPREL, wrong HEAD) | 19 (0.07%) | sid=ssj568.2937.10420; tok=bil#3; gold=(5,cop); pred=(1,cop); text="Zagožen je bil nasprotnega mnenja." |
| 12 | mark | (same DEPREL, wrong HEAD) | 17 (0.07%) | sid=ssj563.2929.10383; tok=le#54; gold=(57,mark); pred=(47,mark); text="Sedanji kulturnorelativistični »trend« je namreč uvoz iz ZDA; a v ZDA se je kulturni relativi..." |
| 13 | aux | (same DEPREL, wrong HEAD) | 15 (0.06%) | sid=ssj568.2937.10420; tok=je#2; gold=(5,aux); pred=(1,aux); text="Zagožen je bil nasprotnega mnenja." |
| 14 | appos | (same DEPREL, wrong HEAD) | 14 (0.06%) | sid=ssj565.2934.10401; tok=vidika#26; gold=(23,appos); pred=(18,appos); text="Mimi Podkrižnik Komisijo za šolsko prehrano sestavljajo ravnatelj ali pomočnik, vodja šolske ..." |
| 15 | case | (same DEPREL, wrong HEAD) | 13 (0.05%) | sid=ssj562.2919.10334; tok=po#2; gold=(6,case); pred=(5,case); text="Namreč po zdravi "kmečki pameti" in lastnih izkušnjah še nobena reforma ni prinesla nečesa ve..." |

### B) HEAD correct, DEPREL wrong
| Rank | Gold DEPREL | Pred DEPREL | Count | Example |
|---|---|---|---:|---|
| 1 | iobj | obj | 53 (0.21%) | sid=ssj562.2919.10336; tok=besedi#7; gold=(6,iobj); pred=(6,obj); text="Ob tem sem se namenoma izognil besedi denarja, saj lahko gre tudi za druge stvari." |
| 2 | conj | parataxis | 27 (0.11%) | sid=ssj562.2924.10358; tok=skuhamo#4; gold=(2,conj); pred=(2,parataxis); text="Krompir operemo, skuhamo, olupimo in pretlačimo." |
| 3 | orphan | advmod | 26 (0.10%) | sid=ssj562.2919.10334; tok=predvsem#23; gold=(27,orphan); pred=(27,advmod); text="Namreč po zdravi "kmečki pameti" in lastnih izkušnjah še nobena reforma ni prinesla nečesa ve..." |
| 4 | nmod | obl | 23 (0.09%) | sid=ssj563.2929.10384; tok=razsežnosti#28; gold=(25,nmod); pred=(25,obl); text="Najnovejša transakcija je sicer še sveža, vzorec pa je bržkone vselej isti: Evropi se iz Amer..." |
| 5 | nsubj | obj | 12 (0.05%) | sid=ssj562.2925.10366; tok=prepoznavnost#14; gold=(12,nsubj); pred=(12,obj); text="Mnenja je namreč, da do uspeha v tem poklicu lahko pripelje predvsem prepoznavnost, zato tudi..." |
| 6 | advcl | parataxis | 12 (0.05%) | sid=ssj563.2931.10390; tok=govori#34; gold=(30,advcl); pred=(30,parataxis); text="32 Corneille je seveda dilemo postavil kot konflikt med enako plemenitima in vzvišenima čustv..." |
| 7 | iobj | expl | 12 (0.05%) | sid=ssj567.2936.10413; tok=si#21; gold=(24,iobj); pred=(24,expl); text="Prepustite pa se lahko tudi vsem prepotrebnim udobnostim, od crkljanja v najmehkejši halji in..." |
| 8 | det | nmod | 12 (0.05%) | sid=ssj581.2995.10601; tok=vsega#4; gold=(5,det); pred=(5,nmod); text="Kajpada ljubosumno božanstvo vsega tega ni doseglo brez pomoči." |
| 9 | obl | obj | 10 (0.04%) | sid=ssj563.2929.10386; tok=nanj#25; gold=(26,obl); pred=(26,obj); text="– Tole je sicer moralistična poenostavitev, poanta pa je, da je medkulturni nesporazum lahko ..." |
| 10 | obj | nsubj | 10 (0.04%) | sid=ssj578.2965.10519; tok=svežine#6; gold=(5,obj); pred=(5,nsubj); text="Na EP mi je manjkalo svežine, ki sem jo na SP ohranil, kar je bilo odločilno,« je komentiral ..." |
| 11 | flat | nmod | 10 (0.04%) | sid=ssj579.2987.10584; tok=Gazvoda#5; gold=(4,flat); pred=(4,nmod); text="(Foto: T. Gazvoda)" |
| 12 | cc | advmod | 9 (0.04%) | sid=ssj562.2922.10342; tok=torej#15; gold=(20,cc); pred=(20,advmod); text="V primerjavi s krompirjem pa lahko topinambur brez bojazni za zdravje uživamo surov, torej sv..." |
| 13 | case | advmod | 8 (0.03%) | sid=ssj563.2926.10368; tok=ne#33; gold=(36,case); pred=(36,advmod); text="Na drugi strani so vse ideologije, ki delujejo v nacionalno konstituiranem »diskurzivnem veso..." |
| 14 | obl | nmod | 8 (0.03%) | sid=ssj563.2927.10372; tok=praksah#23; gold=(19,obl); pred=(19,nmod); text="Institucij pa ni, če ne obstajajo tudi »v glavah«: domačinske predstave so potemtakem integra..." |
| 15 | appos | nmod | 7 (0.03%) | sid=ssj563.2930.10388; tok=interpretacija#22; gold=(20,appos); pred=(20,nmod); text="45 Doslej smo brez posebnega razločka pisali o »razumevanju« in »interpretaciji«; poslej bomo..." |

### C) HEAD wrong, DEPREL wrong
| Rank | Gold DEPREL | Pred DEPREL | Count | Example |
|---|---|---|---:|---|
| 1 | nmod | obl | 52 (0.20%) | sid=ssj562.2925.10364; tok=zaključku#17; gold=(15,nmod); pred=(12,obl); text="Pred leti pa se je njegova kreacija, ki jo je izdelal za modno revijo ob zaključku srednje šo..." |
| 2 | obl | nmod | 44 (0.17%) | sid=ssj562.2919.10334; tok=pameti#6; gold=(15,obl); pred=(5,nmod); text="Namreč po zdravi "kmečki pameti" in lastnih izkušnjah še nobena reforma ni prinesla nečesa ve..." |
| 3 | root | parataxis | 34 (0.13%) | sid=ssj565.2934.10406; tok=cena#18; gold=(0,root); pred=(9,parataxis); text="»Glavno merilo pri dobavljanju hrane - nabava poteka na podlagi javnega razpisa - je vse prep..." |
| 4 | orphan | advmod | 24 (0.09%) | sid=ssj562.2919.10334; tok=manj#21; gold=(20,orphan); pred=(15,advmod); text="Namreč po zdravi "kmečki pameti" in lastnih izkušnjah še nobena reforma ni prinesla nečesa ve..." |
| 5 | parataxis | root | 21 (0.08%) | sid=ssj562.2923.10351; tok=je#14; gold=(8,parataxis); pred=(0,root); text="V enem od "centrov" Čepinec so še vedno neobnovljene stavbe, je pa tam kot posebnost velika l..." |
| 6 | ccomp | root | 18 (0.07%) | sid=ssj570.2944.10466; tok=inhalirali#4; gold=(9,ccomp); pred=(0,root); text=""Ampak nismo inhalirali!" je še dodal." |
| 7 | advcl | acl | 15 (0.06%) | sid=ssj562.2919.10333; tok=opisuje#10; gold=(3,advcl); pred=(6,acl); text="Deloma se strinjam z drugim delom članka, ko opisuje finančne učinke reforme." |
| 8 | nsubj | root | 15 (0.06%) | sid=ssj562.2923.10353; tok=točka#10; gold=(4,nsubj); pred=(0,root); text="Po več podatkih je na pobočju Kalcinega brega najsevernejša točka Slovenije." |
| 9 | root | nsubj | 11 (0.04%) | sid=ssj566.2935.10408; tok=neprofitnost#9; gold=(0,root); pred=(1,nsubj); text="Ena od odlik knjižne zbirke Scripta je njena neprofitnost, ki nam ob finančni pomoči ŠOU omog..." |
| 10 | parataxis | appos | 11 (0.04%) | sid=ssj581.2996.10610; tok=reda#24; gold=(11,parataxis); pred=(16,appos); text="Freudov zgodovinski pomen ironično izhaja iz dejstva, da je pripomogel k prehodu od ene vrste..." |
| 11 | parataxis | conj | 10 (0.04%) | sid=ssj565.2934.10404; tok=plačo#28; gold=(14,parataxis); pred=(19,conj); text="Malica je pri nas uvrščena v nacionalni oziroma zagotovljeni program financiranja, torej dobi..." |
| 12 | root | cop | 9 (0.04%) | sid=ssj562.2923.10351; tok=so#8; gold=(0,root); pred=(11,cop); text="V enem od "centrov" Čepinec so še vedno neobnovljene stavbe, je pa tam kot posebnost velika l..." |
| 13 | conj | parataxis | 9 (0.04%) | sid=ssj563.2931.10393; tok=zadeva#41; gold=(15,conj); pred=(7,parataxis); text="Moderni individualisti bi bili sicer bržkone nagnjeni k anahronistični interpretaciji, ki bi ..." |
| 14 | flat | nmod | 9 (0.04%) | sid=ssj600.3086.10926; tok=Di#7; gold=(6,flat); pred=(8,nmod); text="Napad na trikilometrski klanec domačina Danila Di Luce, Gilberta Simonija in idola italijansk..." |
| 15 | parataxis | advmod | 7 (0.03%) | sid=ssj562.2919.10334; tok=nekaj#20; gold=(15,parataxis); pred=(21,advmod); text="Namreč po zdravi "kmečki pameti" in lastnih izkušnjah še nobena reforma ni prinesla nečesa ve..." |

## Direct model comparison (LAS exact)
- Compared tokens: 25442
- CLASSLA aligned correct, Trankit aligned wrong: 1195 (4.70%)
- Trankit aligned correct, CLASSLA aligned wrong: 1345 (5.29%)

### Where CLASSLA aligned is better
| Rank | Gold DEPREL | Loser error pattern | Count | Example |
|---|---|---|---:|---|
| 1 | advmod | HEAD wrong, DEPREL advmod | 271 (1.07%) | sid=ssj562.2919.10334; tok=še#11; gold=(13,advmod); classla=(13,advmod); trankit=(15,advmod); text="Namreč po zdravi "kmečki pameti" in lastnih izkušnjah še nobena reforma ni prinesla nečesa ve..." |
| 2 | punct | HEAD wrong, DEPREL punct | 171 (0.67%) | sid=ssj562.2919.10334; tok="#4; gold=(6,punct); classla=(6,punct); trankit=(5,punct); text="Namreč po zdravi "kmečki pameti" in lastnih izkušnjah še nobena reforma ni prinesla nečesa ve..." |
| 3 | iobj | DEPREL iobj->obj, HEAD ok | 44 (0.17%) | sid=ssj562.2919.10336; tok=besedi#7; gold=(6,iobj); classla=(6,iobj); trankit=(6,obj); text="Ob tem sem se namenoma izognil besedi denarja, saj lahko gre tudi za druge stvari." |
| 4 | conj | HEAD wrong, DEPREL conj | 40 (0.16%) | sid=ssj562.2919.10334; tok=izkušnjah#10; gold=(6,conj); classla=(6,conj); trankit=(5,conj); text="Namreč po zdravi "kmečki pameti" in lastnih izkušnjah še nobena reforma ni prinesla nečesa ve..." |
| 5 | nmod | HEAD wrong + DEPREL nmod->obl | 25 (0.10%) | sid=ssj562.2925.10364; tok=zaključku#17; gold=(15,nmod); classla=(15,nmod); trankit=(12,obl); text="Pred leti pa se je njegova kreacija, ki jo je izdelal za modno revijo ob zaključku srednje šo..." |
| 6 | obl | HEAD wrong, DEPREL obl | 23 (0.09%) | sid=ssj562.2922.10344; tok=jed#6; gold=(1,obl); classla=(1,obl); trankit=(2,obl); text="Postrežemo ga lahko kot začetno jed, v juhi, prilogah, solatah, za dieto pa je lahko samostoj..." |
| 7 | nmod | HEAD wrong, DEPREL nmod | 23 (0.09%) | sid=ssj573.2950.10480; tok=kolesa#6; gold=(2,nmod); classla=(2,nmod); trankit=(4,nmod); text="Na naperi (špici) kolesa pa je pritrjen magnet." |
| 8 | root | HEAD wrong + DEPREL root->parataxis | 21 (0.08%) | sid=ssj570.2944.10466; tok=dodal#9; gold=(0,root); classla=(0,root); trankit=(4,parataxis); text=""Ampak nismo inhalirali!" je še dodal." |
| 9 | obl | HEAD wrong + DEPREL obl->nmod | 19 (0.07%) | sid=ssj562.2919.10334; tok=pameti#6; gold=(15,obl); classla=(15,obl); trankit=(5,nmod); text="Namreč po zdravi "kmečki pameti" in lastnih izkušnjah še nobena reforma ni prinesla nečesa ve..." |
| 10 | orphan | HEAD wrong + DEPREL orphan->advmod | 18 (0.07%) | sid=ssj562.2923.10346; tok=pa#25; gold=(24,orphan); classla=(24,orphan); trankit=(27,advmod); text="Čepinci se vsaj po kažipotu čisto držijo Markovec, čeprav to v praksi pomeni, da je nekaj hiš..." |
| 11 | nmod | DEPREL nmod->obl, HEAD ok | 18 (0.07%) | sid=ssj563.2929.10384; tok=razsežnosti#28; gold=(25,nmod); classla=(25,nmod); trankit=(25,obl); text="Najnovejša transakcija je sicer še sveža, vzorec pa je bržkone vselej isti: Evropi se iz Amer..." |
| 12 | orphan | DEPREL orphan->advmod, HEAD ok | 17 (0.07%) | sid=ssj562.2919.10334; tok=pa#24; gold=(27,orphan); classla=(27,orphan); trankit=(27,advmod); text="Namreč po zdravi "kmečki pameti" in lastnih izkušnjah še nobena reforma ni prinesla nečesa ve..." |
| 13 | parataxis | HEAD wrong, DEPREL parataxis | 17 (0.07%) | sid=ssj563.2931.10392; tok=zmoreta#19; gold=(3,parataxis); classla=(3,parataxis); trankit=(10,parataxis); text="Torej za konflikt, ki ga v načelu ni mogoče zadovoljivo rešiti: ne družba ne posameznica ne z..." |
| 14 | ccomp | HEAD wrong + DEPREL ccomp->root | 15 (0.06%) | sid=ssj570.2944.10466; tok=inhalirali#4; gold=(9,ccomp); classla=(9,ccomp); trankit=(0,root); text=""Ampak nismo inhalirali!" je še dodal." |
| 15 | cop | HEAD wrong, DEPREL cop | 11 (0.04%) | sid=ssj568.2937.10420; tok=bil#3; gold=(5,cop); classla=(5,cop); trankit=(1,cop); text="Zagožen je bil nasprotnega mnenja." |

### Where Trankit aligned is better
| Rank | Gold DEPREL | Loser error pattern | Count | Example |
|---|---|---|---:|---|
| 1 | punct | HEAD wrong, DEPREL punct | 196 (0.77%) | sid=ssj562.2919.10334; tok=,#28; gold=(31,punct); classla=(27,punct); trankit=(31,punct); text="Namreč po zdravi "kmečki pameti" in lastnih izkušnjah še nobena reforma ni prinesla nečesa ve..." |
| 2 | advmod | HEAD wrong, DEPREL advmod | 86 (0.34%) | sid=ssj562.2923.10351; tok=pa#15; gold=(14,advmod); classla=(20,advmod); trankit=(14,advmod); text="V enem od "centrov" Čepinec so še vedno neobnovljene stavbe, je pa tam kot posebnost velika l..." |
| 3 | obl | HEAD wrong + DEPREL obl->nmod | 62 (0.24%) | sid=ssj562.2920.10338; tok=napotnico#16; gold=(8,obl); classla=(14,nmod); trankit=(8,obl); text="Ta v primeru potrebe po svoji presoji napoti bolnika k specialistu na sekundarnem nivoju z na..." |
| 4 | nmod | HEAD wrong, DEPREL nmod | 53 (0.21%) | sid=ssj562.2921.10339; tok=pokal#8; gold=(4,nmod); classla=(6,nmod); trankit=(4,nmod); text="Na nedavnem mednarodnem turnirju mladih judoistov za pokal Ptuja je sodelovalo 285 tekmovalce..." |
| 5 | conj | HEAD wrong, DEPREL conj | 51 (0.20%) | sid=ssj562.2922.10342; tok=kuhane#19; gold=(16,conj); classla=(13,conj); trankit=(16,conj); text="V primerjavi s krompirjem pa lahko topinambur brez bojazni za zdravje uživamo surov, torej sv..." |
| 6 | obl | HEAD wrong, DEPREL obl | 45 (0.18%) | sid=ssj563.2927.10371; tok=začetka#17; gold=(26,obl); classla=(13,obl); trankit=(26,obl); text="Logika strukture zahteva družbene prakse, jih konstituira, zato so te prakse že od vsega zače..." |
| 7 | nmod | HEAD wrong + DEPREL nmod->obl | 35 (0.14%) | sid=ssj562.2925.10366; tok=poklicu#10; gold=(7,nmod); classla=(12,obl); trankit=(7,nmod); text="Mnenja je namreč, da do uspeha v tem poklicu lahko pripelje predvsem prepoznavnost, zato tudi..." |
| 8 | acl | HEAD wrong, DEPREL acl | 32 (0.13%) | sid=ssj562.2920.10338; tok=izražena#20; gold=(16,acl); classla=(14,acl); trankit=(16,acl); text="Ta v primeru potrebe po svoji presoji napoti bolnika k specialistu na sekundarnem nivoju z na..." |
| 9 | aux | HEAD wrong, DEPREL aux | 30 (0.12%) | sid=ssj563.2931.10394; tok=bi#8; gold=(10,aux); classla=(9,aux); trankit=(10,aux); text="Če se že poskušamo z anahronizmi, bi bilo produktivneje Himenino ljubezen razumeti kot protes..." |
| 10 | cc | HEAD wrong, DEPREL cc | 26 (0.10%) | sid=ssj563.2927.10371; tok=zato#10; gold=(26,cc); classla=(13,cc); trankit=(26,cc); text="Logika strukture zahteva družbene prakse, jih konstituira, zato so te prakse že od vsega zače..." |
| 11 | nsubj | DEPREL nsubj->obj, HEAD ok | 25 (0.10%) | sid=ssj562.2923.10352; tok=pot#28; gold=(29,nsubj); classla=(29,obj); trankit=(29,nsubj); text="Tukaj srečamo več avtomobilov z madžarskimi registracijami, saj je v bližini mejni prehod z M..." |
| 12 | obj | DEPREL obj->iobj, HEAD ok | 25 (0.10%) | sid=ssj563.2926.10368; tok=jim#40; gold=(43,obj); classla=(43,iobj); trankit=(43,obj); text="Na drugi strani so vse ideologije, ki delujejo v nacionalno konstituiranem »diskurzivnem veso..." |
| 13 | obj | DEPREL obj->nsubj, HEAD ok | 24 (0.09%) | sid=ssj562.2923.10346; tok=Markovec#8; gold=(7,obj); classla=(7,nsubj); trankit=(7,obj); text="Čepinci se vsaj po kažipotu čisto držijo Markovec, čeprav to v praksi pomeni, da je nekaj hiš..." |
| 14 | root | HEAD wrong + DEPREL root->cop | 22 (0.09%) | sid=ssj563.2928.10378; tok=je#8; gold=(0,root); classla=(9,cop); trankit=(0,root); text="Če jih institucija sili v hipokrizijo, je razlog navadno v tem, da institucionalnih zahtev ni..." |
| 15 | mark | HEAD wrong, DEPREL mark | 22 (0.09%) | sid=ssj563.2928.10378; tok=da#14; gold=(18,mark); classla=(17,mark); trankit=(18,mark); text="Če jih institucija sili v hipokrizijo, je razlog navadno v tem, da institucionalnih zahtev ni..." |
