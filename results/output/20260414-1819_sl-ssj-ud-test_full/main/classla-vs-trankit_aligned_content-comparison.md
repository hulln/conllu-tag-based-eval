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

## Trankit aligned - error content tables
- Compared tokens: 25442
- LAS-correct tokens: 24066 (94.59%)

### A) HEAD wrong, DEPREL correct
| Rank | Gold DEPREL | Pred DEPREL | Count | Example |
|---|---|---|---:|---|
| 1 | punct | (same DEPREL, wrong HEAD) | 198 (0.78%) | sid=ssj562.2919.10334; tok=,#18; gold=(20,punct); pred=(21,punct); text="Namreč po zdravi "kmečki pameti" in lastnih izkušnjah še nobena reforma ni prinesla nečesa ve..." |
| 2 | advmod | (same DEPREL, wrong HEAD) | 97 (0.38%) | sid=ssj562.2919.10334; tok=še#11; gold=(13,advmod); pred=(15,advmod); text="Namreč po zdravi "kmečki pameti" in lastnih izkušnjah še nobena reforma ni prinesla nečesa ve..." |
| 3 | conj | (same DEPREL, wrong HEAD) | 80 (0.31%) | sid=ssj562.2919.10335; tok=imamo#14; gold=(4,conj); pred=(7,conj); text="Reforme se ne delajo, ko imamo vsega dovolj, ampak, ko imamo nečesa premalo." |
| 4 | nmod | (same DEPREL, wrong HEAD) | 76 (0.30%) | sid=ssj562.2923.10352; tok=Čepinci#17; gold=(14,nmod); pred=(16,nmod); text="Tukaj srečamo več avtomobilov z madžarskimi registracijami, saj je v bližini mejni prehod z M..." |
| 5 | obl | (same DEPREL, wrong HEAD) | 34 (0.13%) | sid=ssj562.2922.10343; tok=krompirjevih#17; gold=(13,obl); pred=(15,obl); text="Sveži gomolji imajo svojevrsten okus; kuhani, dušeni ali pečeni so sočnejši in rahlejši od kr..." |
| 6 | parataxis | (same DEPREL, wrong HEAD) | 27 (0.11%) | sid=ssj562.2923.10351; tok=je#14; gold=(8,parataxis); pred=(11,parataxis); text="V enem od "centrov" Čepinec so še vedno neobnovljene stavbe, je pa tam kot posebnost velika l..." |
| 7 | advcl | (same DEPREL, wrong HEAD) | 21 (0.08%) | sid=ssj563.2928.10379; tok=aktivirata#16; gold=(8,advcl); pred=(7,advcl); text="24 Iz tega škripca se je mogoče rešiti tako, da posameznik in posameznica »aktivirata« kakšno..." |
| 8 | acl | (same DEPREL, wrong HEAD) | 21 (0.08%) | sid=ssj563.2929.10383; tok=posledica#47; gold=(39,acl); pred=(37,acl); text="Sedanji kulturnorelativistični »trend« je namreč uvoz iz ZDA; a v ZDA se je kulturni relativi..." |
| 9 | cc | (same DEPREL, wrong HEAD) | 15 (0.06%) | sid=ssj563.2927.10371; tok=zato#10; gold=(26,cc); pred=(11,cc); text="Logika strukture zahteva družbene prakse, jih konstituira, zato so te prakse že od vsega zače..." |
| 10 | appos | (same DEPREL, wrong HEAD) | 15 (0.06%) | sid=ssj566.2935.10408; tok=tistih#34; gold=(31,appos); pred=(29,appos); text="Ena od odlik knjižne zbirke Scripta je njena neprofitnost, ki nam ob finančni pomoči ŠOU omog..." |
| 11 | nsubj | (same DEPREL, wrong HEAD) | 13 (0.05%) | sid=ssj562.2923.10351; tok=stavbe#12; gold=(8,nsubj); pred=(11,nsubj); text="V enem od "centrov" Čepinec so še vedno neobnovljene stavbe, je pa tam kot posebnost velika l..." |
| 12 | aux | (same DEPREL, wrong HEAD) | 12 (0.05%) | sid=ssj563.2931.10394; tok=bi#8; gold=(10,aux); pred=(9,aux); text="Če se že poskušamo z anahronizmi, bi bilo produktivneje Himenino ljubezen razumeti kot protes..." |
| 13 | cop | (same DEPREL, wrong HEAD) | 11 (0.04%) | sid=ssj566.2935.10408; tok=je#7; gold=(9,cop); pred=(1,cop); text="Ena od odlik knjižne zbirke Scripta je njena neprofitnost, ki nam ob finančni pomoči ŠOU omog..." |
| 14 | mark | (same DEPREL, wrong HEAD) | 10 (0.04%) | sid=ssj570.2943.10447; tok=da#5; gold=(6,mark); pred=(8,mark); text="// Recimo, da ste kadrovski direktor in da je vaše delo preverjanje kandidatov ter zaposlovan..." |
| 15 | case | (same DEPREL, wrong HEAD) | 9 (0.04%) | sid=ssj590.3029.10724; tok=v#5; gold=(8,case); pred=(7,case); text="Prednost zaslonov IPS je v veliki kotni vidljivosti, ki je pri sodobnih zaslonih že več kot 1..." |
| 16 | nummod | (same DEPREL, wrong HEAD) | 5 (0.02%) | sid=ssj575.2955.10493; tok=sedemsto#3; gold=(5,nummod); pred=(1,nummod); text="Milijon in sedemsto tisoč ljudi je umrlo v drugi svetovni vojni, da bi nas sedaj ločevali tujci." |
| 17 | amod | (same DEPREL, wrong HEAD) | 4 (0.02%) | sid=ssj590.3029.10724; tok=veliki#6; gold=(8,amod); pred=(7,amod); text="Prednost zaslonov IPS je v veliki kotni vidljivosti, ki je pri sodobnih zaslonih že več kot 1..." |
| 18 | obj | (same DEPREL, wrong HEAD) | 4 (0.02%) | sid=ssj593.3041.10781; tok=vam#3; gold=(7,obj); pred=(6,obj); text="Naj se vam ne bo težko povzpeti na kako bližnjo manjšo vzpetino in če vas prijatelj ali prija..." |
| 19 | ccomp | (same DEPREL, wrong HEAD) | 4 (0.02%) | sid=ssj596.3064.10846; tok=zgodilo#4; gold=(11,ccomp); pred=(10,ccomp); text="Kaj se bo zgodilo v prihodnjem letu, sta želela vedeti tudi koroška hlapec in dekla, ki sta n..." |
| 20 | expl | (same DEPREL, wrong HEAD) | 2 (0.01%) | sid=ssj596.3066.10859; tok=se#3; gold=(4,expl); pred=(5,expl); text="Kmetice so se bale delati v dneh, ki jih je torka prepovedovala." |

### B) HEAD correct, DEPREL wrong
| Rank | Gold DEPREL | Pred DEPREL | Count | Example |
|---|---|---|---:|---|
| 1 | iobj | obj | 19 (0.07%) | sid=ssj562.2919.10336; tok=besedi#7; gold=(6,iobj); pred=(6,obj); text="Ob tem sem se namenoma izognil besedi denarja, saj lahko gre tudi za druge stvari." |
| 2 | nmod | flat | 17 (0.07%) | sid=ssj567.2936.10414; tok=Lafayette#24; gold=(23,nmod); pred=(23,flat); text="Če pa vam raziskovalni duh ne da posedati v sobi, se lahko podate po nakupih v bližnji največ..." |
| 3 | obj | iobj | 14 (0.06%) | sid=ssj563.2926.10367; tok=individua#5; gold=(16,obj); pred=(16,iobj); text="Zato nacionalna ničta institucija individua, ki ga je zgrabila v svoj interpelacijski mehaniz..." |
| 4 | conj | parataxis | 13 (0.05%) | sid=ssj579.2977.10562; tok=vzele#19; gold=(4,conj); pred=(4,parataxis); text="Ta je bil ptič v Čarodeju Fikfiku, in ker je bil ves razigran, so ga lutkarice vzele za svojo..." |
| 5 | nsubj | obj | 12 (0.05%) | sid=ssj573.2950.10479; tok=Čas#1; gold=(5,nsubj); pred=(5,obj); text="Čas enega obrata t0 izmerijo s pomočjo sunkov iz merilne tuljavice, ki je pritrjena na vilice..." |
| 6 | obj | nsubj | 10 (0.04%) | sid=ssj578.2965.10519; tok=svežine#6; gold=(5,obj); pred=(5,nsubj); text="Na EP mi je manjkalo svežine, ki sem jo na SP ohranil, kar je bilo odločilno,« je komentiral ..." |
| 7 | nmod | obl | 7 (0.03%) | sid=ssj563.2929.10384; tok=razsežnosti#28; gold=(25,nmod); pred=(25,obl); text="Najnovejša transakcija je sicer še sveža, vzorec pa je bržkone vselej isti: Evropi se iz Amer..." |
| 8 | orphan | advmod | 6 (0.02%) | sid=ssj562.2919.10334; tok=predvsem#23; gold=(27,orphan); pred=(27,advmod); text="Namreč po zdravi "kmečki pameti" in lastnih izkušnjah še nobena reforma ni prinesla nečesa ve..." |
| 9 | appos | nmod | 6 (0.02%) | sid=ssj565.2934.10401; tok=vidika#26; gold=(23,appos); pred=(23,nmod); text="Mimi Podkrižnik Komisijo za šolsko prehrano sestavljajo ravnatelj ali pomočnik, vodja šolske ..." |
| 10 | advcl | ccomp | 5 (0.02%) | sid=ssj563.2926.10367; tok=prepusti#20; gold=(16,advcl); pred=(16,ccomp); text="Zato nacionalna ničta institucija individua, ki ga je zgrabila v svoj interpelacijski mehaniz..." |
| 11 | iobj | expl | 5 (0.02%) | sid=ssj567.2936.10413; tok=si#21; gold=(24,iobj); pred=(24,expl); text="Prepustite pa se lahko tudi vsem prepotrebnim udobnostim, od crkljanja v najmehkejši halji in..." |
| 12 | cc | advmod | 5 (0.02%) | sid=ssj568.2937.10418; tok=tako#8; gold=(9,cc); pred=(9,advmod); text="Zmanjševanje javne porabe se mu ne zdi tako pomembno kot njeno pravilno uravnoteženje, to, da..." |
| 13 | conj | flat | 5 (0.02%) | sid=ssj570.2945.10468; tok=Row#5; gold=(3,conj); pred=(3,flat); text="Psychology, Harper& Row, New York, 1987." |
| 14 | advmod | obl | 5 (0.02%) | sid=ssj578.2960.10504; tok=prihodnje#11; gold=(12,advmod); pred=(12,obl); text="In kdo bo tisti, ki se bo moral v prihodnje spopadati s »pritiski, prisiljenimi odločitvami, ..." |
| 15 | appos | conj | 5 (0.02%) | sid=ssj581.2995.10606; tok=norm#13; gold=(11,appos); pred=(11,conj); text="Njegova Teorija Idej je potrdila nadzor vedenja s pomočjo avtoritarnih konceptov - norm tako,..." |
| 16 | advcl | advmod | 5 (0.02%) | sid=ssj584.3000.10631; tok=dobro#3; gold=(2,advcl); pred=(2,advmod); text="Ni videti dobro in še slabše se počuti." |
| 17 | orphan | nmod | 4 (0.02%) | sid=ssj581.2996.10610; tok=premožnemu#26; gold=(24,orphan); pred=(24,nmod); text="Freudov zgodovinski pomen ironično izhaja iz dejstva, da je pripomogel k prehodu od ene vrste..." |
| 18 | parataxis | conj | 4 (0.02%) | sid=ssj588.3023.10686; tok=uporabni#33; gold=(6,parataxis); pred=(6,conj); text="No, sedaj se lahko poigravamo s čemerkoli hočemo, in čeprav nadrealizem v vsebinskem in forma..." |
| 19 | nmod | amod | 4 (0.02%) | sid=ssj598.3080.10908; tok=Rogaške#4; gold=(5,nmod); pred=(5,amod); text="Tudi sogovornik iz Rogaške Slatine, ki je najprej povedal, da je Podobnik fejst fant, a je bi..." |
| 20 | advmod | cc | 3 (0.01%) | sid=ssj562.2919.10334; tok=Namreč#1; gold=(15,advmod); pred=(15,cc); text="Namreč po zdravi "kmečki pameti" in lastnih izkušnjah še nobena reforma ni prinesla nečesa ve..." |

### C) HEAD wrong, DEPREL wrong
| Rank | Gold DEPREL | Pred DEPREL | Count | Example |
|---|---|---|---:|---|
| 1 | obl | nmod | 44 (0.17%) | sid=ssj562.2920.10338; tok=presoji#7; gold=(8,obl); pred=(4,nmod); text="Ta v primeru potrebe po svoji presoji napoti bolnika k specialistu na sekundarnem nivoju z na..." |
| 2 | nmod | obl | 39 (0.15%) | sid=ssj562.2925.10364; tok=zaključku#17; gold=(15,nmod); pred=(12,obl); text="Pred leti pa se je njegova kreacija, ki jo je izdelal za modno revijo ob zaključku srednje šo..." |
| 3 | parataxis | root | 21 (0.08%) | sid=ssj563.2927.10374; tok=mogoče#9; gold=(4,parataxis); pred=(0,root); text="Ali, preprosto povedano: iz koncepta je mogoče izpeljati domačinsko predstavo, iz domačinske ..." |
| 4 | root | parataxis | 12 (0.05%) | sid=ssj563.2927.10374; tok=povedano#4; gold=(0,root); pred=(9,parataxis); text="Ali, preprosto povedano: iz koncepta je mogoče izpeljati domačinsko predstavo, iz domačinske ..." |
| 5 | nsubj | root | 10 (0.04%) | sid=ssj566.2935.10408; tok=Ena#1; gold=(9,nsubj); pred=(0,root); text="Ena od odlik knjižne zbirke Scripta je njena neprofitnost, ki nam ob finančni pomoči ŠOU omog..." |
| 6 | advcl | acl | 9 (0.04%) | sid=ssj562.2919.10333; tok=opisuje#10; gold=(3,advcl); pred=(6,acl); text="Deloma se strinjam z drugim delom članka, ko opisuje finančne učinke reforme." |
| 7 | parataxis | appos | 8 (0.03%) | sid=ssj562.2919.10334; tok=način#27; gold=(15,parataxis); pred=(21,appos); text="Namreč po zdravi "kmečki pameti" in lastnih izkušnjah še nobena reforma ni prinesla nečesa ve..." |
| 8 | root | cop | 7 (0.03%) | sid=ssj562.2923.10351; tok=so#8; gold=(0,root); pred=(11,cop); text="V enem od "centrov" Čepinec so še vedno neobnovljene stavbe, je pa tam kot posebnost velika l..." |
| 9 | root | ccomp | 7 (0.03%) | sid=ssj565.2934.10406; tok=cena#18; gold=(0,root); pred=(21,ccomp); text="»Glavno merilo pri dobavljanju hrane - nabava poteka na podlagi javnega razpisa - je vse prep..." |
| 10 | root | nsubj | 6 (0.02%) | sid=ssj566.2935.10408; tok=neprofitnost#9; gold=(0,root); pred=(1,nsubj); text="Ena od odlik knjižne zbirke Scripta je njena neprofitnost, ki nam ob finančni pomoči ŠOU omog..." |
| 11 | nmod | flat | 6 (0.02%) | sid=ssj579.2992.10594; tok=N.#18; gold=(17,nmod); pred=(15,flat); text="POSLOVNI PROSTOR v Čardaku 26, Črnomelj, oddam, in prodam novo blagajno Olivetti ECR 003 N.+ ..." |
| 12 | nmod | appos | 6 (0.02%) | sid=ssj590.3029.10720; tok=In#4; gold=(5,nmod); pred=(2,appos); text="Zaslone IPS (In Plane Switching) sta leta 1996 razvila Hitachi in NEC." |
| 13 | acl | advcl | 5 (0.02%) | sid=ssj579.2972.10544; tok=poročila#24; gold=(13,acl); pred=(6,advcl); text="Tudi omara v jedilnici je prišla k hiši pred več kot sto leti, ko se je Martinova stara mama ..." |
| 14 | conj | amod | 5 (0.02%) | sid=ssj590.3029.10732; tok=večpalčne#11; gold=(8,conj); pred=(12,amod); text="Danes se zasloni IPS uporabljajo le za 19- in večpalčne zaslone LCD, saj so jih pri 17- palčn..." |
| 15 | appos | nmod | 4 (0.02%) | sid=ssj578.2965.10516; tok=sek.#27; gold=(23,appos); pred=(22,nmod); text="Na polovici proge je bil 11. (Zrimšek 17. s pet sekund slabšim časom), v tretji četrtini 8. (..." |
| 16 | obj | nmod | 4 (0.02%) | sid=ssj579.2969.10533; tok=ekip#15; gold=(9,obj); pred=(12,nmod); text="Žreb nam ni bil naklonjen, saj smo imeli za nasprotnika eno najboljših evropskih ekip, rokome..." |
| 17 | nmod | obj | 4 (0.02%) | sid=ssj582.2997.10613; tok=priložnosti#7; gold=(5,nmod); pred=(12,obj); text="Kljub majskemu odprtju meja trga tisočerih priložnosti velikega povpraševanja delodajalcev ni..." |
| 18 | case | fixed | 4 (0.02%) | sid=ssj589.3025.10696; tok=kot#2; gold=(4,case); pred=(1,fixed); text="Tako kot lovsko orožje in spretnosti, ki so jih razvili, da bi ubili plen in nadzorovali svoj..." |
| 19 | appos | flat | 4 (0.02%) | sid=ssj590.3029.10720; tok=Switching#6; gold=(2,appos); pred=(4,flat); text="Zaslone IPS (In Plane Switching) sta leta 1996 razvila Hitachi in NEC." |
| 20 | appos | nummod | 4 (0.02%) | sid=ssj598.3081.10912; tok=102#31; gold=(25,appos); pred=(27,nummod); text="Za primer: zmagovalec lendavskega turnirja bo dobil manj točk kot polfinalista MP Slovenije (..." |

## Direct model comparison (LAS exact)
- Compared tokens: 25442
- CLASSLA aligned correct, Trankit aligned wrong: 478 (1.88%)
- Trankit aligned correct, CLASSLA aligned wrong: 1523 (5.99%)

### Where CLASSLA aligned is better
| Rank | Gold DEPREL | Loser error pattern | Count | Example |
|---|---|---|---:|---|
| 1 | punct | HEAD wrong, DEPREL punct | 61 (0.24%) | sid=ssj562.2919.10335; tok=,#10; gold=(14,punct); classla=(14,punct); trankit=(7,punct); text="Reforme se ne delajo, ko imamo vsega dovolj, ampak, ko imamo nečesa premalo." |
| 2 | conj | HEAD wrong, DEPREL conj | 34 (0.13%) | sid=ssj562.2923.10354; tok=čudi#27; gold=(16,conj); classla=(16,conj); trankit=(7,conj); text="Po drugi strani je ta odmaknjenost poskrbela za to, da so Čepinci pravi turistični biser za l..." |
| 3 | advmod | HEAD wrong, DEPREL advmod | 28 (0.11%) | sid=ssj562.2919.10334; tok=še#11; gold=(13,advmod); classla=(13,advmod); trankit=(15,advmod); text="Namreč po zdravi "kmečki pameti" in lastnih izkušnjah še nobena reforma ni prinesla nečesa ve..." |
| 4 | nmod | HEAD wrong, DEPREL nmod | 23 (0.09%) | sid=ssj570.2943.10452; tok=službi#18; gold=(15,nmod); classla=(15,nmod); trankit=(13,nmod); text="Morda nikoli ni dokončal študija ali pa je v prošnji precenil svoja znanja in izkušnje v prej..." |
| 5 | nmod | HEAD wrong + DEPREL nmod->obl | 19 (0.07%) | sid=ssj562.2925.10364; tok=zaključku#17; gold=(15,nmod); classla=(15,nmod); trankit=(12,obl); text="Pred leti pa se je njegova kreacija, ki jo je izdelal za modno revijo ob zaključku srednje šo..." |
| 6 | obl | HEAD wrong + DEPREL obl->nmod | 16 (0.06%) | sid=ssj562.2920.10338; tok=presoji#7; gold=(8,obl); classla=(8,obl); trankit=(4,nmod); text="Ta v primeru potrebe po svoji presoji napoti bolnika k specialistu na sekundarnem nivoju z na..." |
| 7 | obl | HEAD wrong, DEPREL obl | 15 (0.06%) | sid=ssj562.2923.10351; tok=enem#2; gold=(8,obl); classla=(8,obl); trankit=(11,obl); text="V enem od "centrov" Čepinec so še vedno neobnovljene stavbe, je pa tam kot posebnost velika l..." |
| 8 | iobj | DEPREL iobj->obj, HEAD ok | 13 (0.05%) | sid=ssj562.2919.10336; tok=besedi#7; gold=(6,iobj); classla=(6,iobj); trankit=(6,obj); text="Ob tem sem se namenoma izognil besedi denarja, saj lahko gre tudi za druge stvari." |
| 9 | parataxis | HEAD wrong, DEPREL parataxis | 11 (0.04%) | sid=ssj579.2976.10560; tok=TREBNJE#1; gold=(4,parataxis); classla=(4,parataxis); trankit=(10,parataxis); text="TREBNJE - V soboto, 6. januarja, na praznik sv. treh kraljev," |
| 10 | nsubj | DEPREL nsubj->obj, HEAD ok | 9 (0.04%) | sid=ssj578.2967.10529; tok=dejavnik#8; gold=(6,nsubj); classla=(6,nsubj); trankit=(6,obj); text="V drugih primerih pa p53 načne zunanji dejavnik, na primer virus." |
| 11 | advcl | HEAD wrong, DEPREL advcl | 8 (0.03%) | sid=ssj563.2928.10379; tok=aktivirata#16; gold=(8,advcl); classla=(8,advcl); trankit=(7,advcl); text="24 Iz tega škripca se je mogoče rešiti tako, da posameznik in posameznica »aktivirata« kakšno..." |
| 12 | appos | HEAD wrong, DEPREL appos | 8 (0.03%) | sid=ssj566.2935.10408; tok=tistih#34; gold=(31,appos); classla=(31,appos); trankit=(29,appos); text="Ena od odlik knjižne zbirke Scripta je njena neprofitnost, ki nam ob finančni pomoči ŠOU omog..." |
| 13 | nmod | DEPREL nmod->flat, HEAD ok | 8 (0.03%) | sid=ssj567.2936.10414; tok=Lafayette#24; gold=(23,nmod); classla=(23,nmod); trankit=(23,flat); text="Če pa vam raziskovalni duh ne da posedati v sobi, se lahko podate po nakupih v bližnji največ..." |
| 14 | nsubj | HEAD wrong, DEPREL nsubj | 7 (0.03%) | sid=ssj562.2923.10351; tok=stavbe#12; gold=(8,nsubj); classla=(8,nsubj); trankit=(11,nsubj); text="V enem od "centrov" Čepinec so še vedno neobnovljene stavbe, je pa tam kot posebnost velika l..." |
| 15 | acl | HEAD wrong, DEPREL acl | 7 (0.03%) | sid=ssj563.2929.10383; tok=posledica#47; gold=(39,acl); classla=(39,acl); trankit=(37,acl); text="Sedanji kulturnorelativistični »trend« je namreč uvoz iz ZDA; a v ZDA se je kulturni relativi..." |
| 16 | root | HEAD wrong + DEPREL root->parataxis | 5 (0.02%) | sid=ssj563.2927.10374; tok=povedano#4; gold=(0,root); classla=(0,root); trankit=(9,parataxis); text="Ali, preprosto povedano: iz koncepta je mogoče izpeljati domačinsko predstavo, iz domačinske ..." |
| 17 | nmod | DEPREL nmod->obl, HEAD ok | 5 (0.02%) | sid=ssj563.2929.10384; tok=razsežnosti#28; gold=(25,nmod); classla=(25,nmod); trankit=(25,obl); text="Najnovejša transakcija je sicer še sveža, vzorec pa je bržkone vselej isti: Evropi se iz Amer..." |
| 18 | cc | HEAD wrong, DEPREL cc | 5 (0.02%) | sid=ssj575.2955.10493; tok=in#2; gold=(5,cc); classla=(5,cc); trankit=(3,cc); text="Milijon in sedemsto tisoč ljudi je umrlo v drugi svetovni vojni, da bi nas sedaj ločevali tujci." |
| 19 | parataxis | HEAD wrong + DEPREL parataxis->root | 5 (0.02%) | sid=ssj585.3015.10664; tok=TENS#1; gold=(13,parataxis); classla=(13,parataxis); trankit=(0,root); text="TENS (transkutana električna stimulacija živcev): elektrode na bolečih mestih oddajajo elektr..." |
| 20 | nsubj | HEAD wrong + DEPREL nsubj->root | 4 (0.02%) | sid=ssj566.2935.10408; tok=Ena#1; gold=(9,nsubj); classla=(9,nsubj); trankit=(0,root); text="Ena od odlik knjižne zbirke Scripta je njena neprofitnost, ki nam ob finančni pomoči ŠOU omog..." |

### Where Trankit aligned is better
| Rank | Gold DEPREL | Loser error pattern | Count | Example |
|---|---|---|---:|---|
| 1 | punct | HEAD wrong, DEPREL punct | 218 (0.86%) | sid=ssj562.2919.10334; tok=,#28; gold=(31,punct); classla=(27,punct); trankit=(31,punct); text="Namreč po zdravi "kmečki pameti" in lastnih izkušnjah še nobena reforma ni prinesla nečesa ve..." |
| 2 | advmod | HEAD wrong, DEPREL advmod | 89 (0.35%) | sid=ssj562.2923.10351; tok=pa#15; gold=(14,advmod); classla=(20,advmod); trankit=(14,advmod); text="V enem od "centrov" Čepinec so še vedno neobnovljene stavbe, je pa tam kot posebnost velika l..." |
| 3 | conj | HEAD wrong, DEPREL conj | 66 (0.26%) | sid=ssj562.2922.10342; tok=kuhane#19; gold=(16,conj); classla=(13,conj); trankit=(16,conj); text="V primerjavi s krompirjem pa lahko topinambur brez bojazni za zdravje uživamo surov, torej sv..." |
| 4 | obl | HEAD wrong + DEPREL obl->nmod | 61 (0.24%) | sid=ssj562.2920.10338; tok=napotnico#16; gold=(8,obl); classla=(14,nmod); trankit=(8,obl); text="Ta v primeru potrebe po svoji presoji napoti bolnika k specialistu na sekundarnem nivoju z na..." |
| 5 | nmod | HEAD wrong, DEPREL nmod | 56 (0.22%) | sid=ssj562.2921.10339; tok=pokal#8; gold=(4,nmod); classla=(6,nmod); trankit=(4,nmod); text="Na nedavnem mednarodnem turnirju mladih judoistov za pokal Ptuja je sodelovalo 285 tekmovalce..." |
| 6 | obl | HEAD wrong, DEPREL obl | 53 (0.21%) | sid=ssj562.2923.10351; tok=posebnost#18; gold=(14,obl); classla=(16,obl); trankit=(14,obl); text="V enem od "centrov" Čepinec so še vedno neobnovljene stavbe, je pa tam kot posebnost velika l..." |
| 7 | nmod | HEAD wrong + DEPREL nmod->obl | 44 (0.17%) | sid=ssj562.2925.10363; tok=izboru#18; gold=(16,nmod); classla=(13,obl); trankit=(16,nmod); text="Posebej opazna je bila pred časom njegova kreacija, ki jo je nosila ena od finalistk na izbor..." |
| 8 | acl | HEAD wrong, DEPREL acl | 36 (0.14%) | sid=ssj562.2920.10338; tok=izražena#20; gold=(16,acl); classla=(14,acl); trankit=(16,acl); text="Ta v primeru potrebe po svoji presoji napoti bolnika k specialistu na sekundarnem nivoju z na..." |
| 9 | cc | HEAD wrong, DEPREL cc | 30 (0.12%) | sid=ssj562.2922.10342; tok=torej#15; gold=(20,cc); classla=(16,cc); trankit=(20,cc); text="V primerjavi s krompirjem pa lahko topinambur brez bojazni za zdravje uživamo surov, torej sv..." |
| 10 | aux | HEAD wrong, DEPREL aux | 29 (0.11%) | sid=ssj563.2931.10395; tok=bi#26; gold=(27,aux); classla=(28,aux); trankit=(27,aux); text="(Glede na eno izmed teorij o trubadurski poeziji, po kateri naj bi to novo občutenje individu..." |
| 11 | nsubj | DEPREL nsubj->obj, HEAD ok | 26 (0.10%) | sid=ssj562.2923.10352; tok=pot#28; gold=(29,nsubj); classla=(29,obj); trankit=(29,nsubj); text="Tukaj srečamo več avtomobilov z madžarskimi registracijami, saj je v bližini mejni prehod z M..." |
| 12 | parataxis | HEAD wrong, DEPREL parataxis | 24 (0.09%) | sid=ssj562.2923.10346; tok=nekaj#24; gold=(17,parataxis); classla=(7,parataxis); trankit=(17,parataxis); text="Čepinci se vsaj po kažipotu čisto držijo Markovec, čeprav to v praksi pomeni, da je nekaj hiš..." |
| 13 | mark | HEAD wrong, DEPREL mark | 24 (0.09%) | sid=ssj563.2928.10378; tok=da#14; gold=(18,mark); classla=(17,mark); trankit=(18,mark); text="Če jih institucija sili v hipokrizijo, je razlog navadno v tem, da institucionalnih zahtev ni..." |
| 14 | obj | DEPREL obj->nsubj, HEAD ok | 23 (0.09%) | sid=ssj562.2923.10346; tok=Markovec#8; gold=(7,obj); classla=(7,nsubj); trankit=(7,obj); text="Čepinci se vsaj po kažipotu čisto držijo Markovec, čeprav to v praksi pomeni, da je nekaj hiš..." |
| 15 | nsubj | HEAD wrong, DEPREL nsubj | 23 (0.09%) | sid=ssj563.2929.10385; tok=Amerika#1; gold=(4,nsubj); classla=(3,nsubj); trankit=(4,nsubj); text="Amerika je povečevalno ogledalo, v katerem Evropa ogleduje svoje mračno naličje v zvečanem me..." |
| 16 | root | HEAD wrong + DEPREL root->cop | 22 (0.09%) | sid=ssj563.2928.10378; tok=je#8; gold=(0,root); classla=(9,cop); trankit=(0,root); text="Če jih institucija sili v hipokrizijo, je razlog navadno v tem, da institucionalnih zahtev ni..." |
| 17 | nsubj | HEAD wrong + DEPREL nsubj->root | 19 (0.07%) | sid=ssj563.2928.10378; tok=razlog#9; gold=(8,nsubj); classla=(0,root); trankit=(8,nsubj); text="Če jih institucija sili v hipokrizijo, je razlog navadno v tem, da institucionalnih zahtev ni..." |
| 18 | cop | HEAD wrong, DEPREL cop | 19 (0.07%) | sid=ssj563.2928.10379; tok=je#73; gold=(79,cop); classla=(72,cop); trankit=(79,cop); text="24 Iz tega škripca se je mogoče rešiti tako, da posameznik in posameznica »aktivirata« kakšno..." |
| 19 | obj | DEPREL obj->iobj, HEAD ok | 17 (0.07%) | sid=ssj563.2926.10368; tok=jim#40; gold=(43,obj); classla=(43,iobj); trankit=(43,obj); text="Na drugi strani so vse ideologije, ki delujejo v nacionalno konstituiranem »diskurzivnem veso..." |
| 20 | csubj | HEAD wrong, DEPREL csubj | 17 (0.07%) | sid=ssj563.2927.10374; tok=izpeljati#10; gold=(9,csubj); classla=(8,csubj); trankit=(9,csubj); text="Ali, preprosto povedano: iz koncepta je mogoče izpeljati domačinsko predstavo, iz domačinske ..." |
