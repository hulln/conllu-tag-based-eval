# Stanza 1.13.0 vs 1.14.0 — changed-token review

Token-level comparison of Stanza 1.13.0 and 1.14.0 on the same
pretokenized SSJ-UD gold test set.

Only tokens whose predictions differ between versions are listed.
`FIX`, `REGRESSION`, and `BOTH WRONG` are determined against the
manually annotated gold values.

## default

Changed token rows: **61**

### Changed fields

| Field | Changed | Fixes | Regressions | Both wrong |
|---|---:|---:|---:|---:|
| LEMMA | 0 | 0 | 0 | 0 |
| UPOS | 0 | 0 | 0 | 0 |
| XPOS | 0 | 0 | 0 | 0 |
| FEATS | 0 | 0 | 0 | 0 |
| HEAD | 29 | 12 | 12 | 5 |
| DEPREL | 54 | 20 | 18 | 16 |

### Exact dependency annotation (HEAD + DEPREL)

| Outcome | Tokens |
|---|---:|
| 1.14 fixes 1.13 error | 20 |
| 1.14 regression | 19 |
| Both versions wrong | 22 |
| Both dependency-correct, another field changed | 0 |

## default_accurate

Changed token rows: **57**

### Changed fields

| Field | Changed | Fixes | Regressions | Both wrong |
|---|---:|---:|---:|---:|
| LEMMA | 43 | 14 | 20 | 9 |
| UPOS | 0 | 0 | 0 | 0 |
| XPOS | 0 | 0 | 0 | 0 |
| FEATS | 0 | 0 | 0 | 0 |
| HEAD | 4 | 1 | 3 | 0 |
| DEPREL | 13 | 5 | 4 | 4 |

### Exact dependency annotation (HEAD + DEPREL)

| Outcome | Tokens |
|---|---:|
| 1.14 fixes 1.13 error | 6 |
| 1.14 regression | 4 |
| Both versions wrong | 7 |
| Both dependency-correct, another field changed | 40 |

# Detailed review: default

## ssj562.2922.10342 — token 20 `gomolje`

**Sentence:** V primerjavi s krompirjem pa lahko topinambur brez bojazni za zdravje uživamo surov, torej sveže ali napol kuhane gomolje.

**Exact dependency outcome:** BOTH WRONG

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| DEPREL | `appos` | `obj` | `obl` | **BOTH WRONG** |

## ssj562.2923.10346 — token 8 `Markovec`

**Sentence:** Čepinci se vsaj po kažipotu čisto držijo Markovec, čeprav to v praksi pomeni, da je nekaj hiš na tem bregu, nekaj pa na onem.

**Exact dependency outcome:** BOTH WRONG

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| DEPREL | `obj` | `nsubj` | `obl` | **BOTH WRONG** |

## ssj562.2925.10366 — token 12 `pripelje`

**Sentence:** Mnenja je namreč, da do uspeha v tem poklicu lahko pripelje predvsem prepoznavnost, zato tudi želi sodelovati na opaznih prireditvah.

**Exact dependency outcome:** BOTH WRONG

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| HEAD | `1` | `2` | `1` | **FIX** |

## ssj563.2927.10369 — token 5 `koncept`

**Sentence:** Radcliffe-Brown je koncept »zafrkantskih odnosov« izpeljal iz logike strukture in iz njenih notranjih protislovij, iz strukturne potrebe po suplementaciji itn.

**Exact dependency outcome:** FIX

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| DEPREL | `obj` | `nsubj` | `obj` | **FIX** |

## ssj563.2931.10392 — token 17 `posameznica`

**Sentence:** Torej za konflikt, ki ga v načelu ni mogoče zadovoljivo rešiti: ne družba ne posameznica ne zmoreta z eno samo osjo.

**Exact dependency outcome:** BOTH WRONG

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| HEAD | `15` | `19` | `15` | **FIX** |
| DEPREL | `conj` | `nsubj` | `nmod` | **BOTH WRONG** |

## ssj563.2931.10393 — token 41 `zadeva`

**Sentence:** Moderni individualisti bi bili sicer bržkone nagnjeni k anahronistični interpretaciji, ki bi konflikt razumela kot spopad med kolektivistično lojalnostjo krvnemu sorodstvu in individualistično izbiro ljubezenskega - poročnega partnerja: a aliansa ni za Himeno nič manj »kolektivna« zadeva kakor družinska lojalnost.

**Exact dependency outcome:** BOTH WRONG

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| DEPREL | `conj` | `nsubj` | `obl` | **BOTH WRONG** |

## ssj563.2931.10396 — token 5 `izbiro`

**Sentence:** V tej interpretaciji bi izbiro ljubljenega moškega narekoval prav odpor proti statusni določitvi Himene kot predmeta v družinskih političnih strategijah: aporetičnosti institucionalne zahteve s tem ne bi likvidirali, temveč bi njeno napetost prenesli v samo subverzivno čustvo.

**Exact dependency outcome:** REGRESSION

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| DEPREL | `obj` | `obj` | `iobj` | **REGRESSION** |

## ssj563.2931.10397 — token 2 `ljubezen`

**Sentence:** Himenina ljubezen bi tedaj potrjevala institucionalno aporijo prav v svojem revoltu proti njej.

**Exact dependency outcome:** BOTH WRONG

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| DEPREL | `nsubj` | `obj` | `obl` | **BOTH WRONG** |

## ssj565.2934.10401 — token 3 `Komisijo`

**Sentence:** Mimi Podkrižnik Komisijo za šolsko prehrano sestavljajo ravnatelj ali pomočnik, vodja šolske prehrane ter predstavniki kuharskega osebja, zdravstvene in socialne službe (z vidika regresirane prehrane), učencev, staršev…

**Exact dependency outcome:** REGRESSION

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| HEAD | `7` | `7` | `1` | **REGRESSION** |
| DEPREL | `obj` | `obj` | `flat:name` | **REGRESSION** |

## ssj565.2934.10406 — token 3 `merilo`

**Sentence:** »Glavno merilo pri dobavljanju hrane - nabava poteka na podlagi javnega razpisa - je vse prepogosto cena,« moti vodjo prehrane Lucijo Nedeljkovič.

**Exact dependency outcome:** REGRESSION

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| HEAD | `18` | `18` | `21` | **REGRESSION** |

## ssj567.2936.10411 — token 7 `poživljajoče`

**Sentence:** Že samo bivanje v njih vas poživljajoče osveži, preden jo mahnete v mesto: zajtrk pod stekleno kupolo pred sestankom, manjši vrt, v katerem sprostite napetost in si spočijete pogled, ali vaša soba z vsem tehnološkim udobjem za zabavo ali za delo.

**Exact dependency outcome:** FIX

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| DEPREL | `advmod` | `nsubj` | `advmod` | **FIX** |

## ssj567.2936.10413 — token 22 `jih`

**Sentence:** Prepustite pa se lahko tudi vsem prepotrebnim udobnostim, od crkljanja v najmehkejši halji in najmehkejših copatih, kar ste si jih kdaj nadeli, do razpoloženja ugodja, ki ga pričarajo dišeče svečke in piškotki.

**Exact dependency outcome:** REGRESSION

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| DEPREL | `obj` | `obj` | `iobj` | **REGRESSION** |

## ssj570.2942.10444 — token 1 `Občutek`

**Sentence:** Občutek krivde ali obžalovanja načeloma muči večino ljudi, ki so se odločili lagati.

**Exact dependency outcome:** BOTH WRONG

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| DEPREL | `nsubj` | `obj` | `iobj` | **BOTH WRONG** |

## ssj573.2950.10480 — token 6 `kolesa`

**Sentence:** Na naperi (špici) kolesa pa je pritrjen magnet.

**Exact dependency outcome:** FIX

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| HEAD | `2` | `9` | `2` | **FIX** |
| DEPREL | `nmod` | `nsubj` | `nmod` | **FIX** |

## ssj579.2972.10550 — token 10 `kaj`

**Sentence:** Stari likalnik na oglje se mu ne zdi nič kaj posebnega, opozori pa na kamen, s katerim so nekdaj "likali" oblačila iz domačega platna.

**Exact dependency outcome:** FIX

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| DEPREL | `xcomp` | `nsubj` | `xcomp` | **FIX** |

## ssj579.2972.10552 — token 2 `zanimivost`

**Sentence:** Posebna zanimivost so tudi vrata, ki vodijo v jedilnico.

**Exact dependency outcome:** FIX

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| HEAD | `5` | `3` | `5` | **FIX** |

## ssj579.2990.10591 — token 29 `škoda`

**Sentence:** Kljub vsemu Radelj meni, da se bo zelo težko izogniti play outu, v katerem se bodo štiri moštva borila za obstanek, vendar bi bila velika škoda, če moštvo, ki ima najboljšo in najbolj množično občinstvo v prvi ligi, izpade.

**Exact dependency outcome:** BOTH WRONG

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| HEAD | `10` | `45` | `4` | **BOTH WRONG** |
| DEPREL | `conj` | `nsubj` | `conj` | **FIX** |

## ssj579.2990.10591 — token 45 `izpade`

**Sentence:** Kljub vsemu Radelj meni, da se bo zelo težko izogniti play outu, v katerem se bodo štiri moštva borila za obstanek, vendar bi bila velika škoda, če moštvo, ki ima najboljšo in najbolj množično občinstvo v prvi ligi, izpade.

**Exact dependency outcome:** FIX

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| HEAD | `29` | `4` | `29` | **FIX** |
| DEPREL | `advcl` | `ccomp` | `advcl` | **FIX** |

## ssj582.2997.10614 — token 27 `študije`

**Sentence:** Stvari bolj ali manj tečejo svojo pot, zato se podjetja trenutno ne tepejo niti za študente, ki so končali praktične oziroma delovno intenzivne MBA študije.

**Exact dependency outcome:** REGRESSION

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| HEAD | `21` | `21` | `26` | **REGRESSION** |
| DEPREL | `obj` | `obj` | `nmod` | **REGRESSION** |

## ssj583.2999.10624 — token 4 `hčerama`

**Sentence:** Pozneje sta se hčerama pridružila sinova Janči in Martin, danes pa imata 5 vnukov in 3 pravnuke, a razen enega vnuka vsi ostali živijo v Kanadi.

**Exact dependency outcome:** BOTH WRONG

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| DEPREL | `obj` | `nsubj` | `obl` | **BOTH WRONG** |

## ssj589.3027.10709 — token 6 `korak`

**Sentence:** Z vsakim požirkom je konzul korak bliže neizogibni smrti.

**Exact dependency outcome:** BOTH WRONG

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| HEAD | `4` | `4` | `5` | **REGRESSION** |
| DEPREL | `obl` | `nsubj` | `nmod` | **BOTH WRONG** |

## ssj589.3027.10712 — token 8 `kabala`

**Sentence:** Mistika, ki zlorabi svoje moči, kabala primerja s pijancem.

**Exact dependency outcome:** REGRESSION

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| DEPREL | `nsubj` | `nsubj` | `obj` | **REGRESSION** |

## ssj590.3028.10718 — token 13 `pik`

**Sentence:** 19-palčni monitorji so imeli zaslone z ločljivostjo 1600× 1200 pik, medtem ko so 17-palčniki, tako kot danes, prikazovali 1280× 1024 pik.

**Exact dependency outcome:** FIX

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| HEAD | `9` | `6` | `9` | **FIX** |
| DEPREL | `nmod` | `obj` | `nmod` | **FIX** |

## ssj590.3028.10719 — token 43 `ločljivost`

**Sentence:** Ker se 19-palčni monitorji z visoko ločljivostjo niso »prijeli« med uporabniki, je kmalu večina izdelovalcev preklopila na nižjo ločljivost tudi pri 19-palčnikih, tako da imajo danes prav vsi LCDji z diagonalo 19'' ločljivost 1280× 1024 pik.

**Exact dependency outcome:** BOTH WRONG

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| HEAD | `33` | `33` | `39` | **REGRESSION** |
| DEPREL | `obj` | `nsubj` | `nmod` | **BOTH WRONG** |

## ssj590.3029.10729 — token 9 `razlika`

**Sentence:** Kljub temu je treba izpostaviti, da je razlika predvsem pri prižiganju in ugašanju pike med obema skrajnostma (med povsem belo in povsem črno), medtem ko je razlika pri prehodu iz ene stopnje sivine v drugo med zaslonoma TN in IPS precej manjša.

**Exact dependency outcome:** BOTH WRONG

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| HEAD | `8` | `3` | `5` | **BOTH WRONG** |
| DEPREL | `nsubj` | `csubj` | `ccomp` | **BOTH WRONG** |

## ssj590.3033.10741 — token 8 `različico`

**Sentence:** Bojazen, da bo velikan iz Redmonda različico programa za Mace preprosto opustil, se ni uresničila (Microsoft ponuja tudi Virtual PC in Virtual Server za Windows).

**Exact dependency outcome:** REGRESSION

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| HEAD | `13` | `13` | `5` | **REGRESSION** |
| DEPREL | `obj` | `obj` | `nmod` | **REGRESSION** |

## ssj593.3037.10753 — token 12 `mrežo`

**Sentence:** Ne vem, ali ima še katero slovensko podjetje tako široko mrežo po svetu.

**Exact dependency outcome:** REGRESSION

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| HEAD | `5` | `5` | `9` | **REGRESSION** |
| DEPREL | `obj` | `obj` | `nmod` | **REGRESSION** |

## ssj593.3040.10771 — token 10 `nas`

**Sentence:** V zaprašenih prostorih pa nisem bila osamljena, saj nas je bilo kar nekaj, ki smo bolj ali manj pridno pospravljali.

**Exact dependency outcome:** REGRESSION

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| DEPREL | `nsubj` | `nsubj` | `obj` | **REGRESSION** |

## ssj594.3050.10807 — token 4 `kaj`

**Sentence:** Tuhtal je, kaj vse ji mora povedati, da bo hotela ostati.

**Exact dependency outcome:** REGRESSION

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| HEAD | `8` | `8` | `7` | **REGRESSION** |

## ssj596.3062.10843 — token 2 `tepežkarji`

**Sentence:** Otroci tepežkarji seveda niso mislili na vse te stare resnice, ampak so veselo tepežkali odrasle in veselo polnili svoje malhe z darili.

**Exact dependency outcome:** FIX

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| HEAD | `1` | `5` | `1` | **FIX** |
| DEPREL | `nmod` | `nsubj` | `nmod` | **FIX** |

## ssj597.3070.10870 — token 13 `pripeljali`

**Sentence:** "Opišite mi, kaj se je zgodilo, da so vas pripeljali sem," je rekla.

**Exact dependency outcome:** FIX

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| DEPREL | `advcl` | `csubj` | `advcl` | **FIX** |

## ssj597.3072.10876 — token 7 `BMW`

**Sentence:** Nikamor ga ne morem odnesti, BMW sosed je vedno na preži.

**Exact dependency outcome:** FIX

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| HEAD | `8` | `9` | `8` | **FIX** |
| DEPREL | `nmod` | `nsubj` | `nmod` | **FIX** |

## ssj597.3072.10879 — token 15 `kar`

**Sentence:** Obraz sem imel popolnoma krvav, vključno z rokami in gornjim delom telesa, kar sem ga videl v ogledalu.

**Exact dependency outcome:** BOTH WRONG

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| DEPREL | `mark` | `obj` | `nsubj` | **BOTH WRONG** |

## ssj598.3077.10894 — token 43 `Otto`

**Sentence:** Sveže učinkujejo tudi monumentalne slikarske upodobitve kitajskih slikarjev, ki se z ironijo lotevajo mitov svoje in svetovne revolucionarne polpreteklosti, zanimivi so Gary Hume (angleški paviljon), Howard Arkley (avstralski paviljon), pa iz Ljubljane že znani Otto Zidko.

**Exact dependency outcome:** FIX

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| HEAD | `24` | `22` | `24` | **FIX** |
| DEPREL | `conj` | `nsubj` | `conj` | **FIX** |

## ssj598.3081.10914 — token 25 `jih`

**Sentence:** In drugače: z izpadom v I. krogu nedavnega svetovnega prvenstva v Koebenhavnu so vsi naši dobili manj točk (60) kot bi jih z uvrstitvijo v četrtfinale Lendava Internationala (66), ali pa celo v osmino finala MP Slovenije (72).

**Exact dependency outcome:** FIX

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| HEAD | `24` | `17` | `24` | **FIX** |

## ssj602.3091.10945 — token 8 `Séguina`

**Sentence:** Ta nepričakovani »glas ljudstva« je Séguina v hipu priklical iz globoke sence, v katero se je umaknil pred slabim letom po še danes nepojasnjenem odstopu s položaja predsednika RPR (Gibanja za republiko).

**Exact dependency outcome:** REGRESSION

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| DEPREL | `obj` | `obj` | `iobj` | **REGRESSION** |

## ssj604.3099.10983 — token 6 `čas`

**Sentence:** Uporabljati jih smemo le kratek čas in pri akutnem, kratkotrajnem zaprtju.

**Exact dependency outcome:** FIX

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| DEPREL | `obl` | `obj` | `obl` | **FIX** |

## ssj604.3099.10986 — token 6 `odvajala`

**Sentence:** Velja, da smemo ta odvajala uživati previdno in da so med nosečnostjo in dojenjem odsvetovana, razen če zdravnik odloči drugače.

**Exact dependency outcome:** BOTH WRONG

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| DEPREL | `obj` | `csubj` | `ccomp` | **BOTH WRONG** |

## ssj604.3105.11008 — token 19 `nalog`

**Sentence:** Poleg sočnosti in okusnosti hrane in njene večje nasitne vrednosti, imajo maščobe v našem telesu precej pomembnih nalog.

**Exact dependency outcome:** REGRESSION

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| HEAD | `12` | `12` | `13` | **REGRESSION** |
| DEPREL | `obj` | `obj` | `nmod` | **REGRESSION** |

## ssj606.3114.11048 — token 2 `je`

**Sentence:** Verjetno je ni substance, pri kateri bi bila raziskovalna dejavnost tako silovita kot ravno pri konoplji oz. pri kanabinoidih.

**Exact dependency outcome:** BOTH WRONG

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| DEPREL | `expl` | `nsubj` | `obj` | **BOTH WRONG** |

## ssj606.3119.11070 — token 11 `ločljivost`

**Sentence:** Zato je takrat izkušnja navidezne resničnosti večino ljudi razočarala: ločljivost naglavnih stereoskopskih prikazovalnikov je bila zelo slaba in vidno polje omejeno.

**Exact dependency outcome:** FIX

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| HEAD | `18` | `22` | `18` | **FIX** |

## ssj606.3122.11089 — token 2 `Vsakdo`

**Sentence:** »Vsakdo, ki med v ta namen uporabi prvič, je osupel nad njegovo učinkovitostjo,« pravi Molan.

**Exact dependency outcome:** FIX

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| HEAD | `13` | `19` | `13` | **FIX** |

## ssj607.3128.11116 — token 11 `enoti`

**Sentence:** Za to skrbi poseben modul, ki ga priključimo osnovni enoti emulatorja in lahko deluje v naslednjih načinih: sledenje, profiliranje, programsko pokritje, podatkovno pokritje in logični analizator.

**Exact dependency outcome:** BOTH WRONG

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| DEPREL | `iobj` | `obj` | `obl` | **BOTH WRONG** |

## ssj607.3129.11118 — token 40 `ideologije`

**Sentence:** Najboljši dokaz obojega je dejstvo, da je po letu 1500 ves svet vedno bolj plesal na evropsko glasbo; takrat so namreč Evropejci s pomočjo svoje nepremagljive tehnike, prodorne znanosti in za druge prebivalce sveta popolnoma nerazumljive ideologije začeli svoj osvajalni pohod.

**Exact dependency outcome:** BOTH WRONG

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| HEAD | `29` | `41` | `24` | **BOTH WRONG** |
| DEPREL | `conj` | `nsubj` | `conj` | **FIX** |

## ssj607.3129.11119 — token 13 `stoletij`

**Sentence:** To se ne zdi logično zato, ker je Evropa le nekaj stoletij pred tem, po propadu njenega dela rimskega cesarstva, kakor kak star, zaleten avtomobil obležala v gozdu -- skoraj dobesedno, saj so celino v tistem času še prekrivali veliki, neprehodni gozdovi.

**Exact dependency outcome:** BOTH WRONG

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| DEPREL | `obl` | `nsubj` | `obl` | **FIX** |

## ssj607.3135.11133 — token 7 `sunek`

**Sentence:** Pri zunanjih defibrilatorjih dobi srce električni sunek po dveh elektrodah, ki sta postavljeni nad srcem na sprednji steni prsnega koša, ali pa po eni elektrodi na hrbtu in eni na prsih.

**Exact dependency outcome:** REGRESSION

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| HEAD | `4` | `4` | `5` | **REGRESSION** |
| DEPREL | `obj` | `obj` | `nmod` | **REGRESSION** |

## ssj607.3139.11144 — token 1 `Premik`

**Sentence:** Premik dlačic sproži v lasastih slušnih celicah elektrokemične spremembe, ki se prenesejo prek sinapse na aferentne celice slušnega živca.

**Exact dependency outcome:** FIX

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| DEPREL | `nsubj` | `obj` | `nsubj` | **FIX** |

## ssj610.3163.11250 — token 3 `nas`

**Sentence:** Spremljali so nas še lep kos poti in nič čudnega, da je bil nahrbtnik vse bolj natlačen z zelenorumenimi sadeži.

**Exact dependency outcome:** REGRESSION

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| DEPREL | `obj` | `obj` | `iobj` | **REGRESSION** |

## ssj613.3172.11264 — token 12 `povzeti`

**Sentence:** Že imeni vajinih likov sta tako kot naslov vajine druge predstave povzeti po znanem porno filmu o Debbie, ki da dol ves Dallas, za tednik Mladina sta se fotografirali goli, Nataša na plakatu za vajino zadnjo predstavo pozira z revolverjem, Irena pa s cigareto v roki.

**Exact dependency outcome:** BOTH WRONG

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| DEPREL | `root` | `csubj` | `xcomp` | **BOTH WRONG** |

## ssj616.3184.11323 — token 1 `Slednje`

**Sentence:** Slednje, obdobje prehoda, je še zlasti nepredvidljivo, a tudi posebno odprto za individualne in skupinske prispevke, saj prinaša tisto, kar sem imenoval povečanje dejavnika svobodne volje.

**Exact dependency outcome:** REGRESSION

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| DEPREL | `nsubj` | `nsubj` | `parataxis` | **REGRESSION** |

## ssj616.3184.11323 — token 25 `kar`

**Sentence:** Slednje, obdobje prehoda, je še zlasti nepredvidljivo, a tudi posebno odprto za individualne in skupinske prispevke, saj prinaša tisto, kar sem imenoval povečanje dejavnika svobodne volje.

**Exact dependency outcome:** REGRESSION

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| DEPREL | `obj` | `obj` | `iobj` | **REGRESSION** |

## ssj616.3185.11337 — token 12 `nas`

**Sentence:** Vendar pa so vsi skupaj mogočen napad na kulturo sociologije in nas ne morejo pustiti hladne.

**Exact dependency outcome:** REGRESSION

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| HEAD | `15` | `15` | `10` | **REGRESSION** |
| DEPREL | `obj` | `obj` | `conj` | **REGRESSION** |

## ssj618.3189.11357 — token 21 `količina`

**Sentence:** A simptomatično je vendarle, da se recimo količina uvožene, kot praviš, zabavljaške televizijske produkcije nenehno veča, količina, rekel bi, res nujno potrebne prevodne literature pa se seveda manjša.

**Exact dependency outcome:** BOTH WRONG

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| HEAD | `34` | `19` | `23` | **BOTH WRONG** |
| DEPREL | `nsubj` | `nsubj` | `vocative` | **REGRESSION** |

## ssj618.3189.11358 — token 11 `vsem`

**Sentence:** Pravzaprav pa želim samo poudariti, da nam je lahko vsem, ki zadevo vsaj nekako uvidimo, tovrstno druženje z don Kihotom kvečjemu škodljivo ali pač neproduktivno, zato bi bilo nemara bolje v tem kontekstu uporabiti kako bolj učinkovito držo.

**Exact dependency outcome:** BOTH WRONG

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| DEPREL | `appos` | `obj` | `iobj` | **BOTH WRONG** |

## ssj619.3192.11361 — token 7 `kar`

**Sentence:** Videz je bil seveda varljiv, kar je Fran dobro vedela.

**Exact dependency outcome:** FIX

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| DEPREL | `obj` | `nsubj` | `obj` | **FIX** |

## ssj619.3194.11369 — token 20 `žensko`

**Sentence:** Hipoma mu je ugajalo, kar je videl v Fran Simmons uravnovešeno, ljubeznivo, elegantno športno oblečeno mlado žensko.

**Exact dependency outcome:** REGRESSION

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| DEPREL | `obj` | `obj` | `obl` | **REGRESSION** |

## elexiswsd1.1980.sl.132806 — token 4 `JavaScript`

**Sentence:** Vrednosti teh spremenljivk JavaScript lahko ročno nastavimo znotraj kode ali jih pridobimo iz statičnih ali dinamičnih virov JSON.

**Exact dependency outcome:** BOTH WRONG

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| HEAD | `3` | `7` | `1` | **BOTH WRONG** |
| DEPREL | `nmod` | `obj` | `nmod` | **FIX** |

## elexiswsd1.1982.sl.132808 — token 13 `uporablja`

**Sentence:** Poleg tega se je veliko študentov pritožilo, da se njihove fotografije uporablja brez dovoljenja.

**Exact dependency outcome:** FIX

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| DEPREL | `ccomp` | `csubj` | `ccomp` | **FIX** |

## elexiswsd1.1989.sl.132815 — token 25 `Kiklop`

**Sentence:** Eulerju se je v času njegovega bivanja v Nemčiji vid na tem očesu poslabšal do te mere, da ga je Friderik klical »Kiklop«.

**Exact dependency outcome:** FIX

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| DEPREL | `obl` | `nsubj` | `obl` | **FIX** |

## elexiswsd1.1992.sl.132818 — token 17 `funkcija`

**Sentence:** Najnižja količina energije, ki je potrebna, da elektron zapusti površino, se imenuje delovna funkcija.

**Exact dependency outcome:** FIX

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| DEPREL | `obl` | `nsubj` | `obl` | **FIX** |

## elexiswsd1.1997.sl.132823 — token 2 `usta`

**Sentence:** Imajo usta polna ostrih zob, ki so posejani tudi po jeziku.

**Exact dependency outcome:** REGRESSION

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| HEAD | `1` | `1` | `3` | **REGRESSION** |
| DEPREL | `obj` | `obj` | `nmod` | **REGRESSION** |

# Detailed review: default_accurate

## ssj562.2922.10342 — token 7 `topinambur`

**Sentence:** V primerjavi s krompirjem pa lahko topinambur brez bojazni za zdravje uživamo surov, torej sveže ali napol kuhane gomolje.

**Exact dependency outcome:** REGRESSION

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| DEPREL | `obj` | `obj` | `iobj` | **REGRESSION** |

## ssj562.2923.10353 — token 7 `Kalcinega`

**Sentence:** Po več podatkih je na pobočju Kalcinega brega najsevernejša točka Slovenije.

**Exact dependency outcome:** BOTH CORRECT

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| LEMMA | `Kalcin` | `Kalcin` | `kalcin` | **REGRESSION** |

## ssj564.2933.10400 — token 1 `Zazri`

**Sentence:** Zazri se v nebo, spomni se, kaj si o zverinicah izvedel v današnjem zvezku, in se poskusi z vprašanji kviza.

**Exact dependency outcome:** BOTH CORRECT

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| LEMMA | `zazreti` | `zazreti` | `zazeti` | **REGRESSION** |

## ssj565.2934.10401 — token 1 `Mimi`

**Sentence:** Mimi Podkrižnik Komisijo za šolsko prehrano sestavljajo ravnatelj ali pomočnik, vodja šolske prehrane ter predstavniki kuharskega osebja, zdravstvene in socialne službe (z vidika regresirane prehrane), učencev, staršev…

**Exact dependency outcome:** FIX

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| DEPREL | `parataxis` | `nsubj` | `parataxis` | **FIX** |

## ssj567.2936.10413 — token 19 `kar`

**Sentence:** Prepustite pa se lahko tudi vsem prepotrebnim udobnostim, od crkljanja v najmehkejši halji in najmehkejših copatih, kar ste si jih kdaj nadeli, do razpoloženja ugodja, ki ga pričarajo dišeče svečke in piškotki.

**Exact dependency outcome:** BOTH WRONG

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| DEPREL | `mark` | `obj` | `advmod` | **BOTH WRONG** |

## ssj568.2937.10424 — token 9 `rok`

**Sentence:** Sistem je treba spreminjati postopno, na daljši rok.

**Exact dependency outcome:** BOTH WRONG

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| LEMMA | `rok` | `roka` | `rok` | **FIX** |

## ssj570.2941.10440 — token 32 `mikroizrazi`

**Sentence:** Sporazumevamo se z nebesednim vedenjem ali telesnim jezikom, s kvaliteto glasu, z vsebino govora in z drobnimi, bežnimi sporočilci, ki jim pravimo "mikroznaki" ali "mikroizrazi".

**Exact dependency outcome:** BOTH CORRECT

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| LEMMA | `mikroizraz` | `mikroizraz` | `mikroizraza` | **REGRESSION** |

## ssj578.2960.10505 — token 3 `dva`

**Sentence:** Kandidata sta dva, Borut Miklavčič, ki se je v zdravstvu preizkusil že pred leti, ter Emil Židan.

**Exact dependency outcome:** FIX

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| DEPREL | `obl` | `nsubj` | `obl` | **FIX** |

## ssj578.2967.10529 — token 5 `p53`

**Sentence:** V drugih primerih pa p53 načne zunanji dejavnik, na primer virus.

**Exact dependency outcome:** FIX

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| DEPREL | `obj` | `nsubj` | `obj` | **FIX** |

## ssj579.2989.10588 — token 3 `PODRAŽITVIJO`

**Sentence:** STRAH PRED PODRAŽITVIJO - V Krškem prenavljajo pošto na Vidmu, a prejšnji teden so mimoidoči začudeno gledali v može, ki so z bati razbijali zunanja stekla na pošti, steklovino pa z lopatami nalagali na samokolnice.

**Exact dependency outcome:** BOTH CORRECT

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| LEMMA | `podražitev` | `podražitvoj` | `podražiteva` | **BOTH WRONG** |

## ssj579.2991.10593 — token 1 `ODKUPUJEMO`

**Sentence:** ODKUPUJEMO HLODOVINO hrasta, bukve, smreke, jelke in kostanja.+ (061) 218-595 ali (0609) 620-396, po 20. uri.

**Exact dependency outcome:** BOTH CORRECT

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| LEMMA | `odkupovati` | `odkupujevati` | `odkupujeti` | **BOTH WRONG** |

## ssj579.2992.10594 — token 1 `POSLOVNI`

**Sentence:** POSLOVNI PROSTOR v Čardaku 26, Črnomelj, oddam, in prodam novo blagajno Olivetti ECR 003 N.+ (068) 51-669.

**Exact dependency outcome:** BOTH CORRECT

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| LEMMA | `posloven` | `posloven` | `poseven` | **REGRESSION** |

## ssj581.2995.10601 — token 1 `Kajpada`

**Sentence:** Kajpada ljubosumno božanstvo vsega tega ni doseglo brez pomoči.

**Exact dependency outcome:** BOTH WRONG

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| HEAD | `7` | `7` | `3` | **REGRESSION** |
| DEPREL | `advmod` | `nsubj` | `nmod` | **BOTH WRONG** |

## ssj582.2997.10613 — token 9 `povpraševanja`

**Sentence:** Kljub majskemu odprtju meja trga tisočerih priložnosti velikega povpraševanja delodajalcev nismo doživeli.

**Exact dependency outcome:** REGRESSION

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| HEAD | `12` | `12` | `7` | **REGRESSION** |
| DEPREL | `obj` | `obj` | `nmod` | **REGRESSION** |

## ssj583.2999.10625 — token 6 `čerkezi`

**Sentence:** Leta 1943 so med ofenzivo čerkezi zažgali njun dom in jima ukradli celo poročna prstana.

**Exact dependency outcome:** BOTH CORRECT

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| LEMMA | `Čerkez` | `čerkez` | `čerkeza` | **BOTH WRONG** |

## ssj589.3026.10701 — token 1 `Puruša`

**Sentence:** Puruša, kozmični velikan, daruje samega sebe bogovom, ki ga obredno usmrtijo in razkosajo; iz njegovega telesa je nastalo vesolje in družbeni razredi, ki so bili zato sveti in absolutni.

**Exact dependency outcome:** BOTH CORRECT

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| LEMMA | `Puruša` | `Puruša` | `Puruš` | **REGRESSION** |

## ssj593.3037.10750 — token 30 `delu`

**Sentence:** Prej smo bili specialisti za Jugoslavijo, po novem pa postajamo kar nekakšna multinacionalka, ki že deluje pravzaprav v vseh najpomembnejših državah Evrope, zlasti v njenem osrednjem delu.

**Exact dependency outcome:** BOTH CORRECT

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| LEMMA | `del` | `delo` | `del` | **FIX** |

## ssj596.3063.10845 — token 1 `Smučke`

**Sentence:** Smučke seveda v tistem času še niso bile takšne kot danes, saj so za smučanje uporabljali doge, deščice, starih lesenih sodov, ki so si jih privezali na noge.

**Exact dependency outcome:** BOTH CORRECT

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| LEMMA | `smučka` | `smučka` | `smuček` | **REGRESSION** |

## ssj597.3072.10876 — token 8 `sosed`

**Sentence:** Nikamor ga ne morem odnesti, BMW sosed je vedno na preži.

**Exact dependency outcome:** REGRESSION

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| HEAD | `9` | `9` | `7` | **REGRESSION** |
| DEPREL | `nsubj` | `nsubj` | `nmod` | **REGRESSION** |

## ssj597.3072.10879 — token 15 `kar`

**Sentence:** Obraz sem imel popolnoma krvav, vključno z rokami in gornjim delom telesa, kar sem ga videl v ogledalu.

**Exact dependency outcome:** FIX

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| DEPREL | `mark` | `obj` | `mark` | **FIX** |

## ssj598.3076.10887 — token 1 `Vrtljivi`

**Sentence:** Vrtljivi oder za hitro spremembo prizorišč in pisani kostumi so pripomogli k dinamiki predstave, niso pa bistveno vplivali na njeno vrednost.

**Exact dependency outcome:** BOTH CORRECT

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| LEMMA | `vrtljiv` | `Vrtljiv` | `vrtljiv` | **FIX** |

## ssj598.3076.10888 — token 21 `Heltau`

**Sentence:** Orkester pod vodstvom Uweja Theimerja je igral dobro, največja zvezda predstave pa je bil znani in izkušeni igralec Michael Heltau v vlogi živahnega bonvivana Honoréja.

**Exact dependency outcome:** BOTH CORRECT

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| LEMMA | `Heltau` | `Heltau` | `Heltao` | **REGRESSION** |

## ssj598.3076.10890 — token 3 `Mamite`

**Sentence:** V vlogah Mamite in tete Alicie sta se izkazali igralki Sylvia Lukan in Krista Stadler.

**Exact dependency outcome:** BOTH CORRECT

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| LEMMA | `Mamita` | `Mamite` | `Mamita` | **FIX** |

## ssj598.3077.10896 — token 24 `Toderi`

**Sentence:** Kar zadeva nove medije, se mi je posebej vtisnil v spomin že pravljično pripoveden video Cvet iz tisoč in ene noči Grazie Toderi in meditativna inštalacija s fotografijami lune Miza na križ Aia Weiweia.

**Exact dependency outcome:** BOTH CORRECT

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| LEMMA | `Toderi` | `Toderi` | `Toder` | **REGRESSION** |

## ssj603.3095.10959 — token 18 `falkarinola`

**Sentence:** Vsebnost te spojine v bršljanu je odvisna od letnega časa, vrste (H. helix vsebuje več falkarinola kot H. canariensis) ter od kultivarja.

**Exact dependency outcome:** BOTH CORRECT

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| LEMMA | `falkarinol` | `falkarinol` | `falkarinola` | **REGRESSION** |

## ssj603.3095.10960 — token 7 `falkarinola`

**Sentence:** Sončni žarki in vlaga povečajo delovanje falkarinola na kožo.

**Exact dependency outcome:** BOTH CORRECT

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| LEMMA | `falkarinol` | `falkarinol` | `falkarinola` | **REGRESSION** |

## ssj603.3097.10967 — token 4 `fitoterapevtike`

**Sentence:** Baldrijan spada med fitoterapevtike s srednje močnim delovanjem.

**Exact dependency outcome:** BOTH CORRECT

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| LEMMA | `fitoterapevtik` | `fitoterapevtika` | `fitoterapevtik` | **FIX** |

## ssj604.3098.10982 — token 1 `Ksantoni`

**Sentence:** Ksantoni in naftodiantroni so prisotni v manjši količini (manj kot en odstotek), zadnjo skupino pa sestavljajo floroglucinoli, katerih večjo koncentracijo (pet odstotkov) so zasledili v sveži rastlini.

**Exact dependency outcome:** BOTH CORRECT

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| LEMMA | `ksanton` | `ksanton` | `Ksantoni` | **REGRESSION** |

## ssj604.3098.10982 — token 20 `floroglucinoli`

**Sentence:** Ksantoni in naftodiantroni so prisotni v manjši količini (manj kot en odstotek), zadnjo skupino pa sestavljajo floroglucinoli, katerih večjo koncentracijo (pet odstotkov) so zasledili v sveži rastlini.

**Exact dependency outcome:** BOTH CORRECT

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| LEMMA | `floroglucinol` | `floroglucinol` | `floroglucinola` | **REGRESSION** |

## ssj604.3107.11020 — token 29 `metilendioksimetamfetamina`

**Sentence:** Kar 40 odstotkov celotne uporabe naj bi bilo v Evropi, ki je eno pomembnejših področij za proizvodnjo in uporabo sintetičnih mamil, predvsem ekstazija (3,4-metilendioksimetamfetamina) in amfetaminov.

**Exact dependency outcome:** BOTH CORRECT

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| LEMMA | `metilendioksimetamfetamin` | `metilendioksetamfetamin` | `metilendiokimamfetfemimin` | **BOTH WRONG** |

## ssj605.3111.11031 — token 44 `Computerised`

**Sentence:** Mitchell, Aldridge in Broomhead (2003) so predstavili razvoj računalniškega sistema, ki bi se na osnovi določenega števila izdelkov učencev naučil točkovanja in bi po opravljeni moderaciji navodil za točkovanje pri zunanjem ocenjevanju nadomestil človeka predmetnega strokovnjaka pri ocenjevanju (Computerised Marking).

**Exact dependency outcome:** BOTH WRONG

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| LEMMA | `computerised` | `computerised` | `Computerised` | **REGRESSION** |

## ssj606.3114.11045 — token 1 `Mleto`

**Sentence:** Mleto seme lahko uporabljamo za peko slaščic, kruha, za solate, enolončnice, sladolede itd.

**Exact dependency outcome:** BOTH CORRECT

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| LEMMA | `mlet` | `mleto` | `Mleta` | **BOTH WRONG** |

## ssj606.3114.11048 — token 2 `je`

**Sentence:** Verjetno je ni substance, pri kateri bi bila raziskovalna dejavnost tako silovita kot ravno pri konoplji oz. pri kanabinoidih.

**Exact dependency outcome:** BOTH WRONG

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| DEPREL | `expl` | `nsubj` | `obj` | **BOTH WRONG** |

## ssj606.3120.11082 — token 20 `ferrariji`

**Sentence:** Ker so Italijani uporabljali boljše materiale in izdelovali učinkovitejše zavorne sisteme, so njihovi maseratiji, alfe in predvsem ferrariji lahko do kraja izkoristili moč svojih motorjev.

**Exact dependency outcome:** BOTH CORRECT

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| LEMMA | `ferrari` | `ferrarija` | `ferrarij` | **BOTH WRONG** |

## ssj607.3129.11119 — token 20 `dela`

**Sentence:** To se ne zdi logično zato, ker je Evropa le nekaj stoletij pred tem, po propadu njenega dela rimskega cesarstva, kakor kak star, zaleten avtomobil obležala v gozdu -- skoraj dobesedno, saj so celino v tistem času še prekrivali veliki, neprehodni gozdovi.

**Exact dependency outcome:** BOTH CORRECT

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| LEMMA | `del` | `delo` | `del` | **FIX** |

## ssj607.3144.11178 — token 16 `cHTML`

**Sentence:** Spletne strani, ki omogočajo dostopanje terminalom i-mode, so napisane v jeziku cHTML (angl. Compact HyperText Markup Language), ki pa je prirejen za mobilne terminale.

**Exact dependency outcome:** BOTH CORRECT

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| LEMMA | `chtml` | `cHTML` | `chtml` | **FIX** |

## ssj607.3145.11185 — token 6 `veji`

**Sentence:** Ker pa sta ti dve veji, namreč mobilna telefonija in internet, v izjemnem porastu, je ideja o združevanju v t. i. mobilni internet, povsem umestna in polagoma dobiva pravo podobo.

**Exact dependency outcome:** FIX

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| HEAD | `3` | `29` | `3` | **FIX** |

## ssj610.3160.11232 — token 25 `delu`

**Sentence:** V izjavi za javnost je županja zapisala, da je takšno odločitev sprejela zato, ker se ne strinja z odločitvijo sodišča v tistem delu, ko meni, da v zvezi s pobudo županja ne odloča o njeni utemeljenosti po vsebini, pač pa le po formalnih merilih.

**Exact dependency outcome:** BOTH WRONG

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| LEMMA | `del` | `delo` | `del` | **FIX** |

## ssj610.3165.11252 — token 64 `mitsubishi`

**Sentence:** Na dveh kolesih je včeraj prvi v cilj pridrvel Španec Nani Roma (KTM), na štirih pa je drugo zaporedno etapno zmago (peto sta sicer dobila Francoza Stephane Peterhansel in Jean-Paul Cottret, a so ju prireditelji zaradi nedovoljene pomoči naknadno kaznovali s pribitkom petih minut) slavila japonsko-francoska naveza Hiroši Masuoka - Gilles Picard (mitsubishi pajero).

**Exact dependency outcome:** BOTH CORRECT

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| LEMMA | `mitsubishi` | `mitsubishi` | `mitsubish` | **REGRESSION** |

## ssj615.3181.11309 — token 31 `kaj`

**Sentence:** Tako je vprašanje o veljavnosti našega kolektivnega znanja in zlasti o tem, kakšni sklepi izhajajo iz njega o naših zgodovinskih sistemih, osrednje vprašanje v boju za to, kaj sestavlja substantivno racionalnost.

**Exact dependency outcome:** FIX

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| DEPREL | `nsubj` | `obj` | `nsubj` | **FIX** |

## ssj615.3181.11310 — token 1 `Utopistika`

**Sentence:** Utopistika potemtakem pomeni tudi, da moramo še enkrat natančno razmisliti o strukturah znanja in o tem, kaj zares vemo o delovanju družbenega sveta.

**Exact dependency outcome:** BOTH CORRECT

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| LEMMA | `utopistika` | `utopistik` | `utopistika` | **FIX** |

## ssj616.3184.11323 — token 28 `povečanje`

**Sentence:** Slednje, obdobje prehoda, je še zlasti nepredvidljivo, a tudi posebno odprto za individualne in skupinske prispevke, saj prinaša tisto, kar sem imenoval povečanje dejavnika svobodne volje.

**Exact dependency outcome:** BOTH WRONG

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| DEPREL | `obl` | `obj` | `xcomp` | **BOTH WRONG** |

## ssj619.3194.11369 — token 20 `žensko`

**Sentence:** Hipoma mu je ugajalo, kar je videl v Fran Simmons uravnovešeno, ljubeznivo, elegantno športno oblečeno mlado žensko.

**Exact dependency outcome:** REGRESSION

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| DEPREL | `obj` | `obj` | `obl` | **REGRESSION** |

## elexiswsd1.1826.sl.132652 — token 6 `Rahmonberdi`

**Sentence:** Prvi umetniški vodja gledališke skupine Rahmonberdi Madazimov je bil ustanovitelj in organizator gledališkega gibanja v Kirgizistanu.

**Exact dependency outcome:** BOTH CORRECT

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| LEMMA | `Rahmonberdi` | `Rahmonberdi` | `Rahmonberd` | **REGRESSION** |

## elexiswsd1.1843.sl.132669 — token 9 `Debelem`

**Sentence:** Zaradi tega sta danes obala in park na Debelem rtiču tudi zavarovana.

**Exact dependency outcome:** BOTH CORRECT

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| LEMMA | `debel` | `Debel` | `debel` | **FIX** |

## elexiswsd1.1848.sl.132674 — token 5 `Néelu`

**Sentence:** Imenuje se po Louisu Néelu, ki je za svoje delo na tem podočju leta 1970 prejel Nobelovo nagrado za fiziko.

**Exact dependency outcome:** BOTH CORRECT

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| LEMMA | `Néel` | `Néel` | `Néelo` | **REGRESSION** |

## elexiswsd1.1854.sl.132680 — token 1 `Žogo`

**Sentence:** Žogo raje brca z desno nogo.

**Exact dependency outcome:** BOTH CORRECT

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| LEMMA | `žoga` | `žoga` | `žogo` | **REGRESSION** |

## elexiswsd1.1866.sl.132692 — token 15 `grupoidi`

**Sentence:** Abstraktna algebra je matematično področje, ki se ukvarja z algebrskimi strukturami kot so grupoidi, kolobarji, obsegi, moduli, vektorski prostori in algebre.

**Exact dependency outcome:** BOTH CORRECT

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| LEMMA | `grupoid` | `grupoid` | `grupoidi` | **REGRESSION** |

## elexiswsd1.1873.sl.132699 — token 11 `Okimi`

**Sentence:** Anka je v tretjem letu vladanja ubil princ Majova no Okimi kot povračilo za uboj njegovega očeta.

**Exact dependency outcome:** BOTH CORRECT

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| LEMMA | `Okimi` | `Okima` | `Okim` | **BOTH WRONG** |

## elexiswsd1.1884.sl.132710 — token 1 `Malerba`

**Sentence:** Malerba je v Italiji in v Evropi pri podjetju Digital Equipment opravljal delo na področju tehnike in tehničnega upravljanja.

**Exact dependency outcome:** BOTH CORRECT

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| LEMMA | `Malerba` | `Malerba` | `Malerbo` | **REGRESSION** |

## elexiswsd1.1899.sl.132725 — token 20 `VTOL`

**Sentence:** Isto velja za Lockheed F-35B Lightning II: čeprav je operativno STOVL, ima v preizkusnih letih tudi možnost VTOL.

**Exact dependency outcome:** BOTH CORRECT

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| LEMMA | `VTOL` | `Vtol` | `VtOl` | **BOTH WRONG** |

## elexiswsd1.1921.sl.132747 — token 20 `mamboserver.com`

**Sentence:** Vodja projekta Andrew Eddie je napisal pismo, ki se je pojavilo v razdelku za obvestila na javnem forumu mamboserver.com.

**Exact dependency outcome:** BOTH CORRECT

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| LEMMA | `mamboserver.com` | `mamboserver.c` | `mamboserver.com` | **FIX** |

## elexiswsd1.1934.sl.132760 — token 16 `Švabiji`

**Sentence:** Jurij je pozneje postal močan zaveznik cesarja Maksimilijana I. in podpiral je njegove kampanje v Švabiji, Švici, Geldernu in na Madžarskem.

**Exact dependency outcome:** BOTH CORRECT

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| LEMMA | `Švabija` | `Švabija` | `Švabij` | **REGRESSION** |

## elexiswsd1.1934.sl.132760 — token 20 `Geldernu`

**Sentence:** Jurij je pozneje postal močan zaveznik cesarja Maksimilijana I. in podpiral je njegove kampanje v Švabiji, Švici, Geldernu in na Madžarskem.

**Exact dependency outcome:** BOTH CORRECT

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| LEMMA | `Geldern` | `Gelderno` | `Geldern` | **FIX** |

## elexiswsd1.1954.sl.132780 — token 1 `Posameznikova`

**Sentence:** Posameznikova svoboda izražanja je zatorej ključnega pomena za blaginjo družbe.

**Exact dependency outcome:** BOTH CORRECT

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| LEMMA | `posameznikov` | `Posameznikov` | `posameznikov` | **FIX** |

## elexiswsd1.1988.sl.132814 — token 10 `Toulouški`

**Sentence:** Vojska iz Provanse, ki jo je vodil Alfons Toulouški, je s prečkanjem morja počakala do avgusta.

**Exact dependency outcome:** BOTH CORRECT

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| LEMMA | `Toulouški` | `Toulouška` | `Toulouški` | **FIX** |

## elexiswsd1.2000.sl.132826 — token 1 `Tokonoma`

**Sentence:** Tokonoma in njegova vsebina so bistveni elementi tradicionalnega japonskega notranjega dizajna.

**Exact dependency outcome:** BOTH CORRECT

| Field | GOLD | 1.13 | 1.14 | Outcome |
|---|---|---|---|---|
| LEMMA | `tokonoma` | `Tokon` | `Tokono` | **BOTH WRONG** |
