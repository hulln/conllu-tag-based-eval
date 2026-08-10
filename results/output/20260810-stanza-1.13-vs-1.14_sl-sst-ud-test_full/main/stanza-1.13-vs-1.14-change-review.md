# Stanza 1.13.0 vs 1.14.0 — changed-token review

Token-level comparison of Stanza 1.13.0 and 1.14.0 on the same
pretokenized SST-UD gold test set.

Only tokens whose predictions differ between versions are listed.
`FIX`, `REGRESSION`, and `BOTH WRONG` are determined against the
manually annotated gold values.

## default

Changed token rows: **56**

### Changed fields

| Field | Changed | Fixes | Regressions | Both wrong |
|---|---:|---:|---:|---:|
| LEMMA | 0 | 0 | 0 | 0 |
| UPOS | 0 | 0 | 0 | 0 |
| XPOS | 0 | 0 | 0 | 0 |
| FEATS | 0 | 0 | 0 | 0 |
| HEAD | 32 | 15 | 8 | 9 |
| DEPREL | 46 | 15 | 10 | 21 |

### Exact dependency annotation (HEAD + DEPREL)

| Outcome | Tokens |
|---|---:|
| 1.14 fixes 1.13 error | 15 |
| 1.14 regression | 8 |
| Both versions wrong | 33 |
| Both dependency-correct, another field changed | 0 |

## default_accurate

Changed token rows: **37**

### Changed fields

| Field | Changed | Fixes | Regressions | Both wrong |
|---|---:|---:|---:|---:|
| LEMMA | 10 | 5 | 3 | 2 |
| UPOS | 0 | 0 | 0 | 0 |
| XPOS | 0 | 0 | 0 | 0 |
| FEATS | 0 | 0 | 0 | 0 |
| HEAD | 16 | 10 | 5 | 1 |
| DEPREL | 23 | 6 | 8 | 9 |

### Exact dependency annotation (HEAD + DEPREL)

| Outcome | Tokens |
|---|---:|
| 1.14 fixes 1.13 error | 7 |
| 1.14 regression | 4 |
| Both versions wrong | 20 |
| Both dependency-correct, another field changed | 6 |

# Detailed review: default

## Gos165.s187 — token 11 `nekaj`

**Sentence:** od teh plinskih bomb , ki jih je bilo treba nekaj takole šraufati , pa vse živo , skratka , bilo je zelo pestro .

**Exact dependency outcome:** FIX

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| DEPREL | `advmod` | `obj` | `advmod` | **FIX** |

## Gos170.s135 — token 10 `vrsta`

**Sentence:** torej to , kar nam kaže za zdaj zadnja vrsta Poljakov , ni kdove kako obetavno .

**Exact dependency outcome:** REGRESSION

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| DEPREL | `nsubj` | `nsubj` | `xcomp` | **REGRESSION** |

## Gos179.s162 — token 1 `to`

**Sentence:** to so lastniki Dnevnik .

**Exact dependency outcome:** FIX

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| HEAD | `3` | `4` | `3` | **FIX** |

## Gos179.s165 — token 7 `pogledati`

**Sentence:** to bi bilo tudi pol zanimivo pogledati naprej , ne , kaj so to za eni .

**Exact dependency outcome:** REGRESSION

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| DEPREL | `csubj` | `csubj` | `xcomp` | **REGRESSION** |

## Gos179.s165 — token 14 `to`

**Sentence:** to bi bilo tudi pol zanimivo pogledati naprej , ne , kaj so to za eni .

**Exact dependency outcome:** BOTH WRONG

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| DEPREL | `nsubj` | `nsubj` | `expl` | **REGRESSION** |

## Gos179.s171 — token 8 `to`

**Sentence:** ja , samo vprašanje , kdo je to v resnici izza tega , ne .

**Exact dependency outcome:** FIX

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| DEPREL | `expl` | `nsubj` | `expl` | **FIX** |

## Gos189.s54 — token 1 `vse`

**Sentence:** vse nas malo povleče ven , ne , te še moremo malo potem še tiste zadnje moči , da nekako pridemo k sebi , v redu , ne , mhm .

**Exact dependency outcome:** BOTH WRONG

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| DEPREL | `det` | `obj` | `nsubj` | **BOTH WRONG** |

## Gos189.s54 — token 9 `te`

**Sentence:** vse nas malo povleče ven , ne , te še moremo malo potem še tiste zadnje moči , da nekako pridemo k sebi , v redu , ne , mhm .

**Exact dependency outcome:** FIX

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| DEPREL | `advmod` | `obj` | `advmod` | **FIX** |

## Gos189.s55 — token 6 `škoda`

**Sentence:** noter pa pisati , pa škoda mi je tega predmeta , ker je ta predmet

**Exact dependency outcome:** BOTH WRONG

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| DEPREL | `xcomp` | `nsubj` | `advmod` | **BOTH WRONG** |

## Gos193.s140 — token 8 `jih`

**Sentence:** mene s pinceto ne boli , če jih prej malo neko kremo daš noter , ne .

**Exact dependency outcome:** BOTH WRONG

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| DEPREL | `advcl` | `obj` | `reparandum` | **BOTH WRONG** |

## Gos193.s142 — token 8 `mene`

**Sentence:** ja , mene pol čisto nič , mene , eee , s pinceto ne boli , oblikovanje , čisto nič .

**Exact dependency outcome:** REGRESSION

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| DEPREL | `obj` | `obj` | `iobj` | **REGRESSION** |

## Gos193.s142 — token 17 `oblikovanje`

**Sentence:** ja , mene pol čisto nič , mene , eee , s pinceto ne boli , oblikovanje , čisto nič .

**Exact dependency outcome:** BOTH WRONG

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| DEPREL | `nsubj` | `obj` | `dislocated` | **BOTH WRONG** |

## Gos216.s231 — token 6 `to`

**Sentence:** eee , je , je to v bistvu , eee , tudi , eee , v , potrebno imeti dosti izolirano hišo ali je to bolj podobno klasiki , ne vem , olju , drva , drva , v bistvu ogrevanje na drva ?

**Exact dependency outcome:** BOTH WRONG

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| HEAD | `5` | `18` | `5` | **FIX** |

## Gos216.s233 — token 14 `vrste`

**Sentence:** ne vem , z biomaso je tako , biomaso imate vi zdaj tri vrste , bi rekel , tri vrste , ali imate klasična polena .

**Exact dependency outcome:** BOTH WRONG

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| HEAD | `20` | `10` | `6` | **BOTH WRONG** |
| DEPREL | `reparandum` | `obj` | `obl` | **BOTH WRONG** |

## Gos216.s237 — token 41 `vrste`

**Sentence:** zdaj , če greva klasična polena reči , potem je takoj , potem je to peč , kjer se zdaj te , ki so novejše , so take , da v bistvu eee , da v bistvu imate dve neke vrste spodnji kurišči , kjer u- , uplinjate to , ta les in potem se v bistvu ti plini izgoreva .

**Exact dependency outcome:** BOTH WRONG

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| DEPREL | `nmod` | `obj` | `obl` | **BOTH WRONG** |

## Gos216.s237 — token 52 `les`

**Sentence:** zdaj , če greva klasična polena reči , potem je takoj , potem je to peč , kjer se zdaj te , ki so novejše , so take , da v bistvu eee , da v bistvu imate dve neke vrste spodnji kurišči , kjer u- , uplinjate to , ta les in potem se v bistvu ti plini izgoreva .

**Exact dependency outcome:** FIX

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| HEAD | `49` | `48` | `49` | **FIX** |
| DEPREL | `appos` | `obj` | `appos` | **FIX** |

## Artur-J-Gvecg-P500014.s198-s202_reseg.84 — token 9 `video`

**Sentence:** eem in sicer strokovnjaki so doma eee snemali video vsebine eee in pa nasvete eee , ki smo jih potem objavljali na spletni strani našega rehabilitacijskega programa , potem uporabnikom smo to pošiljali eee tudi po elektronski pošti , tudi ostalim našim članom smo pošiljali eem eee vse te video vsebine .

**Exact dependency outcome:** FIX

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| HEAD | `10` | `8` | `10` | **FIX** |
| DEPREL | `nmod` | `obj` | `nmod` | **FIX** |

## Artur-J-Gvecg-P500014.s218-s228_reseg.90 — token 16 `video`

**Sentence:** vsak modul eee ima , eem ko se klikne nanj , eem ima eee številne video vsebine , eem a ne , in potem so si lahko bolniki pomagali tudi v tem času eee na ta način .

**Exact dependency outcome:** FIX

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| HEAD | `17` | `13` | `17` | **FIX** |
| DEPREL | `nmod` | `obj` | `nmod` | **FIX** |

## Artur-J-Gvecg-P500014.s237-s244_reseg.93 — token 36 `skrbi`

**Sentence:** eee tukaj jih je profesor Zver informiral , kako poteka eee zdravljenje v tem času , eee kako skrbijo za to , da je zdravljenje varno , da je zdravstveno osebje , eem eee kako skrbi za vse te varne razmere , hkrati pa je bolnike spodbujal eee k pozitivnem , eee k pozitivi a ne , eem tudi vedno jim je posredoval vse kontaktne podatke , kamor jih lahko kadarkoli pokličejo na eee telefonske številke , skratka .

**Exact dependency outcome:** BOTH WRONG

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| DEPREL | `parataxis:restart` | `csubj` | `parataxis` | **BOTH WRONG** |

## Artur-J-Gvecg-P500014.s245-s248_reseg.94 — token 17 `bolniki`

**Sentence:** eem res so bili naši , tako naši člani kot eem tudi preko socialnih omrežij ostali bolniki s krvnimi raki dobro informirani pa podprti , eee tako da so se imeli na koga obrniti , a ne .

**Exact dependency outcome:** FIX

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| HEAD | `9` | `22` | `9` | **FIX** |
| DEPREL | `conj` | `nsubj` | `conj` | **FIX** |

## Artur-J-Gvecg-P500014.s249-s254_reseg.95 — token 3 `kar`

**Sentence:** eem in kar n- nam je še tako zelo pomembno , da vas v tem času smo dobili res eem tak feedback nazaj od njih ali po elektronski pošti ali po telefonu , eee da so veseli , da jim zdaj v teh težkih časih še bolj stojimo ob strani , kot smo jim morda še prej , a ne , eem in jim je to zelo olajšalo vsak dan , a ne .

**Exact dependency outcome:** REGRESSION

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| HEAD | `10` | `10` | `4` | **REGRESSION** |
| DEPREL | `nsubj` | `nsubj` | `det` | **REGRESSION** |

## Artur-J-Gvecg-P500014.s249-s254_reseg.95 — token 4 `n-`

**Sentence:** eem in kar n- nam je še tako zelo pomembno , da vas v tem času smo dobili res eem tak feedback nazaj od njih ali po elektronski pošti ali po telefonu , eee da so veseli , da jim zdaj v teh težkih časih še bolj stojimo ob strani , kot smo jim morda še prej , a ne , eem in jim je to zelo olajšalo vsak dan , a ne .

**Exact dependency outcome:** FIX

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| HEAD | `5` | `3` | `5` | **FIX** |

## Artur-J-Gvecg-P500014.s249-s254_reseg.95 — token 13 `vas`

**Sentence:** eem in kar n- nam je še tako zelo pomembno , da vas v tem času smo dobili res eem tak feedback nazaj od njih ali po elektronski pošti ali po telefonu , eee da so veseli , da jim zdaj v teh težkih časih še bolj stojimo ob strani , kot smo jim morda še prej , a ne , eem in jim je to zelo olajšalo vsak dan , a ne .

**Exact dependency outcome:** BOTH WRONG

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| DEPREL | `reparandum` | `obj` | `iobj` | **BOTH WRONG** |

## Artur-J-Gvecg-P500028.s114-s116_reseg.217 — token 10 `kar`

**Sentence:** eee , in , eee , mogoče , če kar takoj omenim to temo na področju kemičnega orožja , obstajajo določene mednarodne , eee , deklaracije , sporazumi , eee , ki govorijo o tem , da se to ne sme uporabljati , medtem ko na področju robotov pa to zaenkrat še ni .

**Exact dependency outcome:** BOTH WRONG

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| DEPREL | `advmod` | `obj` | `nsubj` | **BOTH WRONG** |

## Artur-J-Gvecg-P500028.s125-s130_reseg.220 — token 35 `to`

**Sentence:** eee , umetna inteligenca lahko zelo , zelo nadgradi kakšne druge sisteme , eee , lahko jih avtomatizira , eee , vendar to ni prav umetna inteligenca v smislu človeškega razmišljanja , ne , to , eee , mogoče nepoučen , eee , opazovalec si drugače predstavlja kot pa strokovnjak .

**Exact dependency outcome:** BOTH WRONG

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| DEPREL | `obj` | `nsubj` | `reparandum` | **BOTH WRONG** |

## Artur-J-Gvecg-P500028.s156-s159_reseg.227 — token 35 `začetek`

**Sentence:** tudi leta devetnajsto dvaindvajset , tako kot je prej omenjal robote , ali pa recimo , če omenim Slovenijo , isto mi delamo , imamo krasen primer , eee , tudi , eee , začetek robotske proze v Vidu Pečjaku , Drejček in trije marsovčki .

**Exact dependency outcome:** BOTH WRONG

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| HEAD | `25` | `25` | `27` | **REGRESSION** |
| DEPREL | `parataxis` | `obj` | `nmod` | **BOTH WRONG** |

## Artur-J-Gvecg-P500028.s177-s180_reseg.231 — token 49 `to`

**Sentence:** eee , je bil pa to tak dolg proces , zdaj bi rekel okrog tri leta , ne , od čisto začetne ideje , da smo šli skozi vse postopke , procedure in potem še zadnje leto bolj ali manj v , v eee , slovenskem okolju , to pomeni vlada , parlament in vse ostalo .

**Exact dependency outcome:** REGRESSION

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| DEPREL | `nsubj` | `nsubj` | `obj` | **REGRESSION** |

## Artur-J-Gvecg-P500028.s184-s190_reseg.233 — token 71 `to`

**Sentence:** eee , zdaj zaenkrat je to sicer še mala ekipa , ki je pa naslonjena na ta bistveno večji pogon , ki ga imamo na Institutu Jožef Stefan na področju umetne inteligence , torej , eee , na inštitutu imamo , mislim , da okrog sto dvajset ljudi , ne , raziskovalcev , ki , ki se ukvar- , v treh oddelkih , ki se ukvarjajo z umetno inteligenco , to j- , to je približno zdaj stanje in torej aktivnosti pa zdaj trenutno odprtih kar nekaj .

**Exact dependency outcome:** BOTH WRONG

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| HEAD | `78` | `78` | `74` | **REGRESSION** |
| DEPREL | `reparandum` | `nsubj` | `reparandum` | **FIX** |

## Artur-J-Gvecg-P500054.s24-s25_reseg.428 — token 14 `parlament`

**Sentence:** zato peljemo programe , kot so Evropa v šoli , e , šolski parlament in tako dalje in še bi lahko naštevala .

**Exact dependency outcome:** FIX

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| HEAD | `7` | `6` | `7` | **FIX** |
| DEPREL | `conj` | `nsubj` | `conj` | **FIX** |

## Artur-J-Gvecg-P500054.s48-s52_reseg.438 — token 32 `dela`

**Sentence:** to so konkretne zadeve , konkretne številke , eem , tako da jaz mislim , da s tem stanjem ne moremo biti zadovoljni , da državo in odločevalce čaka zelo veliko dela .

**Exact dependency outcome:** FIX

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| DEPREL | `nsubj` | `obj` | `nsubj` | **FIX** |

## Artur-J-Gvecg-P500054.s68-s73_reseg.445 — token 24 `otroka`

**Sentence:** ta hip pa temu prav gotovo ni tako , eee , in najmanj , kar pričakujemo , pričakujemo enostavno dejstvo , da se otroka , njihove potrebe , e e e , njegove potrebe , njegovo specifiko postavi v ospredje politik .

**Exact dependency outcome:** REGRESSION

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| DEPREL | `obj` | `obj` | `nsubj` | **REGRESSION** |

## Artur-J-Gvecg-P500054.s68-s73_reseg.445 — token 27 `potrebe`

**Sentence:** ta hip pa temu prav gotovo ni tako , eee , in najmanj , kar pričakujemo , pričakujemo enostavno dejstvo , da se otroka , njihove potrebe , e e e , njegove potrebe , njegovo specifiko postavi v ospredje politik .

**Exact dependency outcome:** BOTH WRONG

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| HEAD | `34` | `38` | `24` | **BOTH WRONG** |
| DEPREL | `reparandum` | `nsubj` | `conj` | **BOTH WRONG** |

## Artur-J-Gvecg-P500054.s68-s73_reseg.445 — token 34 `potrebe`

**Sentence:** ta hip pa temu prav gotovo ni tako , eee , in najmanj , kar pričakujemo , pričakujemo enostavno dejstvo , da se otroka , njihove potrebe , e e e , njegove potrebe , njegovo specifiko postavi v ospredje politik .

**Exact dependency outcome:** BOTH WRONG

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| HEAD | `24` | `38` | `27` | **BOTH WRONG** |
| DEPREL | `appos` | `nsubj` | `appos` | **FIX** |

## Artur-J-Gvecg-P500063.s79-s83_reseg.465 — token 19 `organizacije`

**Sentence:** eem e , direktiva je uveljavila to novo založniško sorodno pravico , eem , in novinarske na- , organizacije smo nekako podpirale to novo pravico , e , predvsem zato , ker , e , podpiramo , oziroma se nam pri tem zdi ključno , e , da tukaj delež od teh pobranih nadomestil , e , je namenjen tudi za novinarje , neposredno za avtorje .

**Exact dependency outcome:** BOTH WRONG

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| HEAD | `22` | `22` | `25` | **REGRESSION** |
| DEPREL | `nsubj` | `obj` | `conj` | **BOTH WRONG** |

## Artur-J-Gvecg-P500063.s113-s118_reseg.471 — token 20 `predloga`

**Sentence:** e , zato smo predlagali tudi kar nekaj pač , e , e , izboljšav , bi rekla , predloga , e , ki bi malo bolj , e , natančno in v izogib nadaljnjim problemom pol pri uveljavljanju pravice , eem , v bistvu malo bolj o- , zamejil in v ne- v drugih , e , v drugih delih , e , bolj natančno opredelil tudi to , e , končno nadomestilo za avtorja .

**Exact dependency outcome:** BOTH WRONG

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| HEAD | `15` | `5` | `15` | **FIX** |
| DEPREL | `nmod` | `obj` | `appos` | **BOTH WRONG** |

## Artur-J-Gvecg-P500063.s125-s133_reseg.474 — token 7 `stop`

**Sentence:** imetniki dobijo na tako imenovani one stop shop , kjer pravzaprav se njihove pravice upravljajo in , e , tako dobijo uporabniki ta on stop shop , kjer dobijo vse , e , ves repertoar na enem mestu , to je sigurno rešitev , ki so si jo izmislili , bom rekel , ne vem , konec koncev v začetku dvajsetega stoletja in ki je pravzaprav , e , zelo , zelo uporabna , ne , in zato se seveda ne samo , m , kolektivne organizacije , ampak tudi imetniki , e , večinoma zavzemamo zato , da , e , bi bilo čimveč , e , pravic upravljanih kolektivno .

**Exact dependency outcome:** BOTH WRONG

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| DEPREL | `flat:foreign` | `obj` | `obl` | **BOTH WRONG** |

## Artur-J-Gvecg-P500063.s125-s133_reseg.474 — token 24 `on`

**Sentence:** imetniki dobijo na tako imenovani one stop shop , kjer pravzaprav se njihove pravice upravljajo in , e , tako dobijo uporabniki ta on stop shop , kjer dobijo vse , e , ves repertoar na enem mestu , to je sigurno rešitev , ki so si jo izmislili , bom rekel , ne vem , konec koncev v začetku dvajsetega stoletja in ki je pravzaprav , e , zelo , zelo uporabna , ne , in zato se seveda ne samo , m , kolektivne organizacije , ampak tudi imetniki , e , večinoma zavzemamo zato , da , e , bi bilo čimveč , e , pravic upravljanih kolektivno .

**Exact dependency outcome:** BOTH WRONG

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| HEAD | `21` | `21` | `26` | **REGRESSION** |
| DEPREL | `obj` | `nsubj` | `nmod` | **BOTH WRONG** |

## Artur-J-Gvecg-P500063.s141-s151_reseg.477 — token 13 `četrtega`

**Sentence:** zdaj tule mi smo svoje stališče kot Sazor podali lani pač tridesetega četrtega , ko je bil rok , e , za predajo stališč , mislim , smo tam svoje mnenje kar kompaktno in koherentno zastopali , tako da zdaj nismo dajali dodatnih , e , dodatnih komentarjev , saj za temi stališči v celoti stojimo in , eem , moram reči , da je , e , pripravljalec zakona dojel pomen direktive in da je tudi pravilno pristopil k obravnavi tega člena , ki ga je transponiral sedeminštiridesetib člen , če se ne motim .

**Exact dependency outcome:** BOTH WRONG

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| HEAD | `12` | `9` | `10` | **BOTH WRONG** |
| DEPREL | `flat` | `obj` | `nmod` | **BOTH WRONG** |

## Artur-J-Gvecg-P500063.s152-s158_reseg.478 — token 77 `test`

**Sentence:** e , in je tudi dejansko , e , sledil nekako temu , da , e , ker izobraževalna izjema za digitalno reprodukcijo je obvezna , ne , se pravi , je šel , e , v , v , v samem tekstu , medtem ko je nadomestilo podvrženo državam članicam in naša , naš pripravljalec zakona je to nadomestilo upošteval , kar se nam zdi pravilno , in tudi s tem seveda je upoštevan tristopenjski test , po katerem se te izjeme uvajajo in , eem , so naši imetniki bodo načeloma pravilno poplačani za svoje delo .

**Exact dependency outcome:** BOTH WRONG

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| HEAD | `75` | `61` | `66` | **BOTH WRONG** |
| DEPREL | `nsubj` | `nsubj` | `conj` | **REGRESSION** |

## Artur-N-G5097-P600096.s40-s45_reseg.1378 — token 7 `naštimani`

**Sentence:** no , ti kupi so pa naštimani za čas , eem , ke , ke še pride , eem , so pa revije o opremljanju stanovanja , kar , eem , v roku desetih let bi rada hišo malo preuredila .

**Exact dependency outcome:** BOTH WRONG

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| DEPREL | `root` | `nsubj` | `xcomp` | **BOTH WRONG** |

## Artur-N-G5097-P600096.s45-s47_reseg.1379 — token 4 `jih`

**Sentence:** stvari , ke jih , eem , ko vidiš načrte in ko zgradiš hišo , ne razbereš iz načrtov .

**Exact dependency outcome:** FIX

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| HEAD | `17` | `9` | `17` | **FIX** |

## Artur-N-G5097-P600096.s74-s76_reseg.1393 — token 12 `pes`

**Sentence:** ja , hobiji in družina in trije majhni otroci pa še pes ne grejo skupaj .

**Exact dependency outcome:** FIX

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| HEAD | `3` | `14` | `3` | **FIX** |
| DEPREL | `conj` | `nsubj` | `conj` | **FIX** |

## Artur-N-G6007-P600702.s67_reseg.1445 — token 5 `regijo`

**Sentence:** e , se pravi regijo Mediteranskega morja v bistvu tukaj imamo celo vrsto znamenitosti .

**Exact dependency outcome:** BOTH WRONG

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| HEAD | `0` | `11` | `4` | **BOTH WRONG** |

## Artur-N-G6007-P600702.s24-s43_reseg.1437 — token 127 `to`

**Sentence:** pravzaprav gre za domišljijsko zgodbo , kjer , e , pravzaprav poteka , eem , borba za , e , prevzem , e , oblasti nad , e , sedmimi kraljestvi , pri čemer je veliko pretendentov za ta prestol in vsak , e , pravzaprav , eee , e , izkazuje to pravico na , e , iz nekih , e , različnih razlogov in pri tem se sklepajo razna zavezništva , nastopajo različne nadnaravne , e , sile , zgodba je polna preobratov pravzaprav , eee , e , e , tako da je sama zgodba je zelo dolga , zelo težko človek na kratko , e , opiše , eee , zanimiv , eee , je tudi pravzaprav pogled , eee , kako to , ko sem že v prejšnjem vprašanju , e , razložil , v kakšnem obsegu , e , ljudje spreminjajo svoj karakter , e , nekateri so dobri oziroma zli pa potem v bistvu kaže njihovo drugo plat , čeprav v resnici obstaja tukaj , tukaj nekaj karakterjev , ki pa so dosti , e , črno-belo , eee , prikazani .

**Exact dependency outcome:** BOTH WRONG

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| HEAD | `122` | `147` | `122` | **FIX** |

## Artur-N-G6007-P600702.s24-s43_reseg.1437 — token 147 `spreminjajo`

**Sentence:** pravzaprav gre za domišljijsko zgodbo , kjer , e , pravzaprav poteka , eem , borba za , e , prevzem , e , oblasti nad , e , sedmimi kraljestvi , pri čemer je veliko pretendentov za ta prestol in vsak , e , pravzaprav , eee , e , izkazuje to pravico na , e , iz nekih , e , različnih razlogov in pri tem se sklepajo razna zavezništva , nastopajo različne nadnaravne , e , sile , zgodba je polna preobratov pravzaprav , eee , e , e , tako da je sama zgodba je zelo dolga , zelo težko človek na kratko , e , opiše , eee , zanimiv , eee , je tudi pravzaprav pogled , eee , kako to , ko sem že v prejšnjem vprašanju , e , razložil , v kakšnem obsegu , e , ljudje spreminjajo svoj karakter , e , nekateri so dobri oziroma zli pa potem v bistvu kaže njihovo drugo plat , čeprav v resnici obstaja tukaj , tukaj nekaj karakterjev , ki pa so dosti , e , črno-belo , eee , prikazani .

**Exact dependency outcome:** BOTH WRONG

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| HEAD | `127` | `122` | `127` | **FIX** |

## Artur-N-G6007-P600702.s47-s49_reseg.1440 — token 16 `mi`

**Sentence:** všeč , eee , mi je , e , Dalmacija , o pravzaprav všeč so mi vsi , eee , cel , e , okoliš , e , Mediteranskega morja .

**Exact dependency outcome:** BOTH WRONG

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| HEAD | `15` | `15` | `25` | **REGRESSION** |

## Artur-N-G6060-P606001.s67_reseg.1607 — token 1 `meni`

**Sentence:** meni , meni so v bistvu všeč vsi stili , e , bolj je odvisno , kako se jaz počutim tisti dan .

**Exact dependency outcome:** BOTH WRONG

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| DEPREL | `reparandum` | `obj` | `reparandum` | **FIX** |

## Artur-N-G6060-P606001.s61-s62_reseg.1605 — token 2 `lindy`

**Sentence:** in lindy hop je mogoče samo eden izmed tistih , ki dopušča največ svobode , največ , e , odprtih pozicij , kot rečemo , da stojimo narazen pa imamo roke malce bolj stegnjene .

**Exact dependency outcome:** BOTH WRONG

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| HEAD | `3` | `5` | `7` | **BOTH WRONG** |

## Artur-N-G6060-P606001.s63-s66_reseg.1606 — token 2 `to`

**Sentence:** in to je v bistvu to , tako da lindy hop je tak , ki , ki ti da največ kreativnosti , ki ti da največ , eem , neke svobode pri izražanju in tudi dopušča največ napak , da temu tako rečem .

**Exact dependency outcome:** FIX

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| HEAD | `6` | `3` | `6` | **FIX** |

## Artur-N-G6060-P606001.s74-s77_reseg.1609 — token 32 `telo`

**Sentence:** ja to je zelo pomembno , e , predvsem , da se počutiš dobro , da niso kakšni materiali , ki ne morejo dihati , kajti med plesom pač telo , telo , e , zelo je aktivno in važno je , da materiali dihajo .

**Exact dependency outcome:** REGRESSION

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| HEAD | `38` | `38` | `30` | **REGRESSION** |
| DEPREL | `nsubj` | `nsubj` | `conj` | **REGRESSION** |

## Artur-N-G6060-P606001.s88-s90_reseg.1614 — token 5 `taki`

**Sentence:** eni čevlji so tudi taki , eem , ki imajo posebno pač železne podplate , tisto je pa spet , eem , en drug način plesa , ki ga pa mi med temi plesi ne uporabljamo .

**Exact dependency outcome:** BOTH WRONG

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| DEPREL | `root` | `nsubj` | `obl` | **BOTH WRONG** |

## Artur-N-G6100-P610002.s8-s14_reseg.1656 — token 11 `vilini`

**Sentence:** in kljub temu , da imajo škratje neke moči pa vilini moči , na koncu , e , v bistvu glavno vlogo odigra en majhni hobit , ki potuje skozi te dežele in nosi , e , prstan v Goro pogube , kjer ga na koncu seveda zopet ne sam , ampak s pomočjo , e , bitja Goluma , vseeno uspejo vreči v lavo , kjer se ta prstan kasneje izniči in tudi njegova moč .

**Exact dependency outcome:** FIX

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| DEPREL | `conj` | `nsubj` | `conj` | **FIX** |

## Artur-N-G6100-P610002.s8-s14_reseg.1656 — token 41 `pogube`

**Sentence:** in kljub temu , da imajo škratje neke moči pa vilini moči , na koncu , e , v bistvu glavno vlogo odigra en majhni hobit , ki potuje skozi te dežele in nosi , e , prstan v Goro pogube , kjer ga na koncu seveda zopet ne sam , ampak s pomočjo , e , bitja Goluma , vseeno uspejo vreči v lavo , kjer se ta prstan kasneje izniči in tudi njegova moč .

**Exact dependency outcome:** BOTH WRONG

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| HEAD | `40` | `34` | `38` | **BOTH WRONG** |
| DEPREL | `nmod` | `obj` | `nmod` | **FIX** |

## Artur-N-G6100-P610002.s59-s65_reseg.1676 — token 16 `ljudje`

**Sentence:** pa vseeno najdemo neko skupno točko za sodelovanje in , e , pravzaprav potem ti ljudje , večina po končanem nekem programu , ki ga v službi imamo , v smislu nenasilne komunikacije , večina ljudi pove , da jim je bilo težko priti , da niso vedeli , kaj naj pričaku- , da pa so pravzaprav sami pogovori in pa delavnice ter praktična izvedba , ki jo delamo , presegli njihova pričakovanja in da so se naučili nekaj , kar jim bo koristilo naprej v življenju tudi več , veliko jih te stvari bile pomembne , da bi se to že tudi vneslo v šolski sistem , če ne v osnovni šoli pa sigurno v srednji šoli bi mogel obstajati predmet Komunikacija in pa seveda tudi učenje o čustvih .

**Exact dependency outcome:** BOTH WRONG

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| HEAD | `35` | `37` | `3` | **BOTH WRONG** |
| DEPREL | `reparandum` | `nsubj` | `conj` | **BOTH WRONG** |

## Artur-P-G7002-P700444.s26-s27_reseg.1832 — token 2 `jih`

**Sentence:** večina jih niti ne konča uspešno osnovne šole , razlogi za tako stanje pa je dejstvo , da Romi izobrazbe zelo pogosto ne pojmujejo kot vrednoto .

**Exact dependency outcome:** REGRESSION

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| HEAD | `5` | `5` | `1` | **REGRESSION** |
| DEPREL | `nsubj` | `nsubj` | `nmod` | **REGRESSION** |

## Artur-P-G7002-P700444.s55-s56_reseg.1842 — token 4 `ic`

**Sentence:** tretji razlog so ic ne- nezainteresiranost Romov samih .

**Exact dependency outcome:** BOTH WRONG

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| HEAD | `6` | `2` | `6` | **FIX** |
| DEPREL | `reparandum` | `nsubj` | `nmod` | **BOTH WRONG** |

# Detailed review: default_accurate

## Gos179.s154 — token 7 `česa`

**Sentence:** torej , kaj , eee , česa je lastnik Dnevnik .

**Exact dependency outcome:** BOTH WRONG

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| HEAD | `9` | `9` | `10` | **REGRESSION** |
| DEPREL | `nmod` | `nsubj` | `obj` | **BOTH WRONG** |

## Gos179.s165 — token 1 `to`

**Sentence:** to bi bilo tudi pol zanimivo pogledati naprej , ne , kaj so to za eni .

**Exact dependency outcome:** BOTH WRONG

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| DEPREL | `obj` | `nsubj` | `expl` | **BOTH WRONG** |

## Gos179.s171 — token 8 `to`

**Sentence:** ja , samo vprašanje , kdo je to v resnici izza tega , ne .

**Exact dependency outcome:** FIX

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| DEPREL | `expl` | `nsubj` | `expl` | **FIX** |

## Gos193.s140 — token 8 `jih`

**Sentence:** mene s pinceto ne boli , če jih prej malo neko kremo daš noter , ne .

**Exact dependency outcome:** BOTH WRONG

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| DEPREL | `advcl` | `obj` | `iobj` | **BOTH WRONG** |

## Gos206.s138 — token 41 `hiša`

**Sentence:** iskalnik je po krajih , po imenih , po , po , po , po ukrepih , ne , in tam lahko , če greste na ukrep , ne , pogledate , eee , k- , j- , recimo pasivna hiša je , se vam odprejo primeri pasivne hiše , eee v , eee , v Sloveniji , ne .

**Exact dependency outcome:** FIX

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| HEAD | `42` | `46` | `42` | **FIX** |

## Gos216.s231 — token 6 `to`

**Sentence:** eee , je , je to v bistvu , eee , tudi , eee , v , potrebno imeti dosti izolirano hišo ali je to bolj podobno klasiki , ne vem , olju , drva , drva , v bistvu ogrevanje na drva ?

**Exact dependency outcome:** BOTH WRONG

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| DEPREL | `expl` | `nsubj` | `expl` | **FIX** |

## Gos216.s231 — token 33 `olju`

**Sentence:** eee , je , je to v bistvu , eee , tudi , eee , v , potrebno imeti dosti izolirano hišo ali je to bolj podobno klasiki , ne vem , olju , drva , drva , v bistvu ogrevanje na drva ?

**Exact dependency outcome:** BOTH WRONG

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| HEAD | `28` | `27` | `28` | **FIX** |
| DEPREL | `appos` | `obj` | `nmod` | **BOTH WRONG** |

## Gos216.s233 — token 14 `vrste`

**Sentence:** ne vem , z biomaso je tako , biomaso imate vi zdaj tri vrste , bi rekel , tri vrste , ali imate klasična polena .

**Exact dependency outcome:** BOTH WRONG

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| DEPREL | `reparandum` | `obj` | `obl` | **BOTH WRONG** |

## Gos216.s233 — token 20 `vrste`

**Sentence:** ne vem , z biomaso je tako , biomaso imate vi zdaj tri vrste , bi rekel , tri vrste , ali imate klasična polena .

**Exact dependency outcome:** REGRESSION

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| HEAD | `10` | `10` | `14` | **REGRESSION** |
| DEPREL | `obj` | `obj` | `conj` | **REGRESSION** |

## Gos216.s237 — token 15 `to`

**Sentence:** zdaj , če greva klasična polena reči , potem je takoj , potem je to peč , kjer se zdaj te , ki so novejše , so take , da v bistvu eee , da v bistvu imate dve neke vrste spodnji kurišči , kjer u- , uplinjate to , ta les in potem se v bistvu ti plini izgoreva .

**Exact dependency outcome:** BOTH WRONG

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| HEAD | `16` | `14` | `16` | **FIX** |
| DEPREL | `nsubj` | `nsubj` | `det` | **REGRESSION** |

## Artur-J-Gvecg-P500014.s271_reseg.101 — token 15 `share`

**Sentence:** eee nekaj o odzivih ste eee že povedali , zdajle lahko mogoče izklopiva tudi share screen .

**Exact dependency outcome:** BOTH WRONG

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| LEMMA | `share` | `share` | `shara` | **REGRESSION** |

## Artur-J-Gvecg-P500014.s245-s248_reseg.94 — token 17 `bolniki`

**Sentence:** eem res so bili naši , tako naši člani kot eem tudi preko socialnih omrežij ostali bolniki s krvnimi raki dobro informirani pa podprti , eee tako da so se imeli na koga obrniti , a ne .

**Exact dependency outcome:** FIX

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| HEAD | `9` | `22` | `9` | **FIX** |
| DEPREL | `conj` | `nsubj` | `conj` | **FIX** |

## Artur-J-Gvecg-P500028.s165-s172_reseg.229 — token 39 `AI`

**Sentence:** torej , khm , ja , letos smo , eem eee , ust- po dolgem procesu nekako uspeli dokončno ustanoviti ta , eee , imenuje se IRCAI , ne , International Center , eee , Research Center on AI , pod okriljem Unesca , ne .

**Exact dependency outcome:** BOTH WRONG

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| LEMMA | `AI` | `ai` | `AI` | **FIX** |

## Artur-J-Gvecg-P500028.s177-s180_reseg.231 — token 51 `vlada`

**Sentence:** eee , je bil pa to tak dolg proces , zdaj bi rekel okrog tri leta , ne , od čisto začetne ideje , da smo šli skozi vse postopke , procedure in potem še zadnje leto bolj ali manj v , v eee , slovenskem okolju , to pomeni vlada , parlament in vse ostalo .

**Exact dependency outcome:** FIX

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| DEPREL | `obj` | `nsubj` | `obj` | **FIX** |

## Artur-J-Gvecg-P500028.s199-s212_reseg.235 — token 80 `moment`

**Sentence:** eee , no , in preko centra pa tudi sicer preko inštituta , smo pravzaprav vključeni v vse relevantne , eee , mednarodne aktivnosti na to temo , tukaj bi naštel , torej poleg Unesca samega , eee eee eee , je tukaj še , eee , OECD , Svet Evrope , eee , UN , torej Združeni narodi , eee , in Evropa , to so , eee , Evropska komisija , to so nekako glavni centri ta moment mednarodni , kjer se pogovarja , eee , o teh tematikah , pa pozabil sem še GPAI , to je , eee , Globalno partnerstvo za umetno inteligenco , ki je tudi nedavno začelo delati , kjer smo tudi vključeni , a ne .

**Exact dependency outcome:** BOTH WRONG

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| DEPREL | `obl` | `nsubj` | `nmod` | **BOTH WRONG** |

## Artur-J-Gvecg-P500028.s214-s224_reseg.237 — token 15 `regulira`

**Sentence:** cilj je , da se naredi iz , hh , tako , da se regulira umetno inteligenco oziroma to tehnologijo , eee , tehnologije , ki nekako spadajo v ta okvir umetne inteligence , eee , da se jih regulira na en ta način , da ne bojo delale škode , eee eee , bodisi na mikronivoju ali pa tudi na veliko , eee , širšem nivoju , ne .

**Exact dependency outcome:** BOTH WRONG

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| HEAD | `6` | `1` | `6` | **FIX** |
| DEPREL | `parataxis:restart` | `csubj` | `advcl` | **BOTH WRONG** |

## Artur-J-Gvecg-P500054.s60-s65_reseg.443 — token 28 `te`

**Sentence:** in če nimamo programa z akcijskim načrtom , kjer bi država , bi rekla , naredila neki spisek prioritet , na primer , v zdravstvu so prioritete te in te , na področju šolstva te in te , na področju sociala- sociale je naša prioriteta na primer , da v treh letih prepolovimo to številko petinštirideset tisoč , ki je res , e , mislim , da , e , grozljiva , nam ni v ponos .

**Exact dependency outcome:** BOTH WRONG

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| HEAD | `27` | `26` | `27` | **FIX** |
| DEPREL | `nsubj` | `nsubj` | `nmod` | **REGRESSION** |

## Artur-J-Gvecg-P500063.s75-s78_reseg.464 — token 5 `direktiva`

**Sentence:** ja , se pravi direktiva to naše področje medijsko , no , medijsko je zelo široko področje , novinarsko področje , založniško , bom tako rekla , novinarsko zaro- , založniško e , nekako obravnava v petnajstem členu direktive , oziroma to je sto devetintrideseti člen , eem , zakona Zasp-a , predloga Zasp-a .

**Exact dependency outcome:** BOTH WRONG

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| HEAD | `35` | `17` | `9` | **BOTH WRONG** |

## Artur-J-Gvecg-P500063.s75-s78_reseg.464 — token 9 `medijsko`

**Sentence:** ja , se pravi direktiva to naše področje medijsko , no , medijsko je zelo široko področje , novinarsko področje , založniško , bom tako rekla , novinarsko zaro- , založniško e , nekako obravnava v petnajstem členu direktive , oziroma to je sto devetintrideseti člen , eem , zakona Zasp-a , predloga Zasp-a .

**Exact dependency outcome:** BOTH WRONG

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| HEAD | `8` | `8` | `17` | **REGRESSION** |

## Artur-J-Gvecg-P500063.s94-s102_reseg.468 — token 12 `pogajanja`

**Sentence:** e , ne , naša pač zgodovina , e , nekako pogajanja z izdajatelji medijev pa kaže , da nekako , e , v teh , e , že skoraj desetih letih nismo uspeli , e , priti nikamor , da nismo uspeli , eem , ustanoviti kolektivne organizacije , e , da novinarji ne participirajo , e , na tej pravici , e , oziroma na teh nadomestilih , e , oziroma , da so ta nadomestila predmet nekih bilateralnih pogodb med kliping agencijami in vel- , velikimi recimo časopisnimi predvsem izdajatelji .

**Exact dependency outcome:** BOTH WRONG

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| HEAD | `7` | `17` | `7` | **FIX** |
| DEPREL | `nmod` | `nsubj` | `appos` | **BOTH WRONG** |

## Artur-J-Gvecg-P500063.s141-s151_reseg.477 — token 18 `rok`

**Sentence:** zdaj tule mi smo svoje stališče kot Sazor podali lani pač tridesetega četrtega , ko je bil rok , e , za predajo stališč , mislim , smo tam svoje mnenje kar kompaktno in koherentno zastopali , tako da zdaj nismo dajali dodatnih , e , dodatnih komentarjev , saj za temi stališči v celoti stojimo in , eem , moram reči , da je , e , pripravljalec zakona dojel pomen direktive in da je tudi pravilno pristopil k obravnavi tega člena , ki ga je transponiral sedeminštiridesetib člen , če se ne motim .

**Exact dependency outcome:** BOTH CORRECT

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| LEMMA | `rok` | `roka` | `rok` | **FIX** |

## Artur-J-Gvecg-P500063.s141-s151_reseg.477 — token 89 `sedeminštiridesetib`

**Sentence:** zdaj tule mi smo svoje stališče kot Sazor podali lani pač tridesetega četrtega , ko je bil rok , e , za predajo stališč , mislim , smo tam svoje mnenje kar kompaktno in koherentno zastopali , tako da zdaj nismo dajali dodatnih , e , dodatnih komentarjev , saj za temi stališči v celoti stojimo in , eem , moram reči , da je , e , pripravljalec zakona dojel pomen direktive in da je tudi pravilno pristopil k obravnavi tega člena , ki ga je transponiral sedeminštiridesetib člen , če se ne motim .

**Exact dependency outcome:** BOTH CORRECT

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| LEMMA | `sedeminštirideseti` | `sedeminštiridesetib` | `sedeminštirideseti` | **FIX** |

## Artur-J-Gvecg-P500063.s159-s162_reseg.479 — token 5 `kar`

**Sentence:** e , drugo , kar je , e , upošteval je tudi naš pripravljalec zakona , e , to , da se iste izjeme izvzame , se pravi , e , izjema je od izjeme , gradiva , ki so namenjena izključno pouku , kar , kar direktiva tudi jasno predvideva , e , to nam tudi nudi možnost , da , tam , kjer so licence že prisotne , to je tako imenovani licence over right .

**Exact dependency outcome:** BOTH WRONG

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| DEPREL | `nsubj` | `nsubj` | `mark` | **REGRESSION** |

## Artur-J-Gvecg-P500063.s159-s162_reseg.479 — token 37 `gradiva`

**Sentence:** e , drugo , kar je , e , upošteval je tudi naš pripravljalec zakona , e , to , da se iste izjeme izvzame , se pravi , e , izjema je od izjeme , gradiva , ki so namenjena izključno pouku , kar , kar direktiva tudi jasno predvideva , e , to nam tudi nudi možnost , da , tam , kjer so licence že prisotne , to je tako imenovani licence over right .

**Exact dependency outcome:** FIX

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| HEAD | `35` | `33` | `35` | **FIX** |
| DEPREL | `appos` | `nsubj` | `appos` | **FIX** |

## Artur-N-G5097-P600096.s14-s18_reseg.1369 — token 30 `mi`

**Sentence:** otroka , ta starejša dva , sta se imela doma tako lepo , da sta potem nazaj v šolo težko šla , ko so se šole odprle , kar mi je po eni strani kar mi godi , po drugi strani pa vem , da jima očitno čisto preveč nudim in čisto preveč dam .

**Exact dependency outcome:** BOTH WRONG

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| DEPREL | `obj` | `obj` | `iobj` | **REGRESSION** |

## Artur-N-G5097-P600096.s74-s76_reseg.1393 — token 3 `hobiji`

**Sentence:** ja , hobiji in družina in trije majhni otroci pa še pes ne grejo skupaj .

**Exact dependency outcome:** REGRESSION

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| DEPREL | `nsubj` | `nsubj` | `dislocated` | **REGRESSION** |

## Artur-N-G6007-P600702.s24-s43_reseg.1437 — token 105 `človek`

**Sentence:** pravzaprav gre za domišljijsko zgodbo , kjer , e , pravzaprav poteka , eem , borba za , e , prevzem , e , oblasti nad , e , sedmimi kraljestvi , pri čemer je veliko pretendentov za ta prestol in vsak , e , pravzaprav , eee , e , izkazuje to pravico na , e , iz nekih , e , različnih razlogov in pri tem se sklepajo razna zavezništva , nastopajo različne nadnaravne , e , sile , zgodba je polna preobratov pravzaprav , eee , e , e , tako da je sama zgodba je zelo dolga , zelo težko človek na kratko , e , opiše , eee , zanimiv , eee , je tudi pravzaprav pogled , eee , kako to , ko sem že v prejšnjem vprašanju , e , razložil , v kakšnem obsegu , e , ljudje spreminjajo svoj karakter , e , nekateri so dobri oziroma zli pa potem v bistvu kaže njihovo drugo plat , čeprav v resnici obstaja tukaj , tukaj nekaj karakterjev , ki pa so dosti , e , črno-belo , eee , prikazani .

**Exact dependency outcome:** FIX

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| HEAD | `111` | `122` | `111` | **FIX** |

## Artur-N-G6007-P600702.s47-s49_reseg.1440 — token 25 `okoliš`

**Sentence:** všeč , eee , mi je , e , Dalmacija , o pravzaprav všeč so mi vsi , eee , cel , e , okoliš , e , Mediteranskega morja .

**Exact dependency outcome:** REGRESSION

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| HEAD | `15` | `15` | `17` | **REGRESSION** |
| DEPREL | `nsubj` | `nsubj` | `nmod` | **REGRESSION** |

## Artur-N-G6060-P606001.s11-s18_reseg.1587 — token 8 `Briljatina`

**Sentence:** ples sem poznala iz filmov , predvsem Briljatina ali podobno pač ples izhaja iz dobe , e , jazza , solo jazza , dvajseta , trideseta leta prejšnjega stoletja in predvsem iz področja , eem , New Orleansa oziroma ali oko- , notrej- v New Yorku so veliko preplesali , predvsem temnopolti oziroma črnci .

**Exact dependency outcome:** BOTH CORRECT

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| LEMMA | `briljantina` | `Briljatina` | `Briljatin` | **BOTH WRONG** |

## Artur-N-G6060-P606001.s28-s30_reseg.1591 — token 14 `followerke`

**Sentence:** e , veliko ljudi pleše , sicer pa še vedno prevladujemo ženske kot followerke in , e , rabimo fante .

**Exact dependency outcome:** BOTH WRONG

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| LEMMA | `followerka` | `followerka` | `followerke` | **REGRESSION** |

## Artur-N-G6060-P606001.s77-s79_reseg.1610 — token 21 `polkadot`

**Sentence:** je pa tudi posebna moda , pač glih ta moda iz dvajsetih , tridesetih let prejšnjega stoletja , pa te polkadot pač tele pike po oblekah ali pa resice .

**Exact dependency outcome:** BOTH WRONG

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| LEMMA | `polkadot` | `polkadot` | `polkadota` | **REGRESSION** |

## Artur-N-G6100-P610002.s3-s7_reseg.1655 — token 24 `Rohoanci`

**Sentence:** e , tudi se mi zdi , tako ko je , e , e , več teh , bi rekel , Vilinci pa Rohoanci , pa je in se mi zdi tako , e , da nekako vpliva na človeško nezavedno in , e , neka razumevanja nekih stvari , ki so skozi film prikazana , predvsem ta glavna poanta , da lahko še tako majhno bitje , e , premaga največje zlo .

**Exact dependency outcome:** BOTH CORRECT

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| LEMMA | `Rohoanec` | `Rohoanca` | `Rohoanci` | **BOTH WRONG** |

## Artur-N-G6100-P610002.s59-s65_reseg.1676 — token 16 `ljudje`

**Sentence:** pa vseeno najdemo neko skupno točko za sodelovanje in , e , pravzaprav potem ti ljudje , večina po končanem nekem programu , ki ga v službi imamo , v smislu nenasilne komunikacije , večina ljudi pove , da jim je bilo težko priti , da niso vedeli , kaj naj pričaku- , da pa so pravzaprav sami pogovori in pa delavnice ter praktična izvedba , ki jo delamo , presegli njihova pričakovanja in da so se naučili nekaj , kar jim bo koristilo naprej v življenju tudi več , veliko jih te stvari bile pomembne , da bi se to že tudi vneslo v šolski sistem , če ne v osnovni šoli pa sigurno v srednji šoli bi mogel obstajati predmet Komunikacija in pa seveda tudi učenje o čustvih .

**Exact dependency outcome:** FIX

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| HEAD | `35` | `37` | `35` | **FIX** |
| DEPREL | `reparandum` | `nsubj` | `reparandum` | **FIX** |

## Artur-P-G7002-P700444.s26-s27_reseg.1832 — token 2 `jih`

**Sentence:** večina jih niti ne konča uspešno osnovne šole , razlogi za tako stanje pa je dejstvo , da Romi izobrazbe zelo pogosto ne pojmujejo kot vrednoto .

**Exact dependency outcome:** REGRESSION

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| HEAD | `5` | `5` | `1` | **REGRESSION** |
| DEPREL | `nsubj` | `nsubj` | `nmod` | **REGRESSION** |

## Artur-P-G7002-P700444.s43-s44_reseg.1836 — token 17 `le-ti`

**Sentence:** nizka stopnja izobrazbe ima za posledico veliko brezposelnost , t- torej pripadnikov romske skupnosti , saj le-ti večinoma niso zaposleni .

**Exact dependency outcome:** BOTH CORRECT

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| LEMMA | `le-ta` | `le-t` | `le-ta` | **FIX** |

## Artur-P-G7002-P700444.s48-s51_reseg.1839 — token 8 `le-teh`

**Sentence:** torej , zbiranje odpadnih surovin , prodaja le-teh , prekupčevanje , posojanje denarja , tudi za oderuške obresti , izvrševanje kaznivih dejanj in prekrški .

**Exact dependency outcome:** BOTH CORRECT

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| LEMMA | `le-ta` | `le-t` | `le-ta` | **FIX** |

## Artur-P-G7002-P700444.s55-s56_reseg.1842 — token 4 `ic`

**Sentence:** tretji razlog so ic ne- nezainteresiranost Romov samih .

**Exact dependency outcome:** BOTH WRONG

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| DEPREL | `reparandum` | `nsubj` | `advmod` | **BOTH WRONG** |
