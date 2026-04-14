# CoNLL-U file comparison: gold vs trankit_aligned

## File identity
- gold path: data/gold/sl_ssj-ud-test.conllu
- trankit_aligned path: predictions/runs/20260414-1215_sl-ssj-ud-test_full_trankit_aligned_predicted.conllu
- gold sha256: c14d5d2f4f20a7ad43e0f598a2e18c5e41f08364ab36be1c87d6d9eae7f5c8b0
- trankit_aligned sha256: 336695f2060ba0a8c4c9c47b88ff38f007ca79304e4ed40cca06322c5ec52feb
- Byte-identical: no

## Sentence coverage
- gold sentences: 1282
- trankit_aligned sentences: 1282
- Paired sentences: 1282
- Unmatched gold sentences: 0
- Unmatched trankit_aligned sentences: 0
- Paired sentences with token length mismatch: 0
- Paired sentences fully identical: 0
- Paired sentences with at least one difference: 1282

## Token comparison (paired sentences)
- Compared tokens (FORM-aligned): 25442
- Tokens fully identical (all fields): 0 (0.00%)
- Tokens with any field difference: 25442 (100.00%)
- Tokens skipped due to FORM mismatch: 0
- Extra tokens from sentence length mismatch: 0

## Field-level differences
- lemma: 659 (2.59% of compared tokens)
- upos: 302 (1.19% of compared tokens)
- xpos: 886 (3.48% of compared tokens)
- feats: 810 (3.18% of compared tokens)
- head: 1785 (7.02% of compared tokens)
- deprel: 1117 (4.39% of compared tokens)
- deps: 0 (0.00% of compared tokens)
- misc: 25442 (100.00% of compared tokens)

## Top DEPREL changes
gold_deprel	trankit_aligned_deprel	count
nmod	obl	75
iobj	obj	56
obl	nmod	52
orphan	advmod	50
conj	parataxis	36
root	parataxis	34
parataxis	root	21
ccomp	root	18
advcl	acl	15
nsubj	root	15
nsubj	obj	13
appos	nmod	13
advcl	parataxis	13
parataxis	appos	13
flat:foreign	nmod	13
root	nsubj	12
iobj	expl	12
det	nmod	12
list	conj	12
parataxis	conj	11

## Top HEAD changes
gold_head	trankit_aligned_head	count
3	4	17
2	4	15
5	3	14
15	17	14
0	4	13
5	1	13
13	14	13
3	6	12
6	8	12
6	3	12
6	7	12
6	5	11
1	3	11
6	1	11
2	0	10
0	1	10
7	8	10
4	6	10
23	22	10
3	5	10

## Example differing sentence pairs
a_idx	b_idx	a_sent_id	a_tokens	b_tokens	text
1	1	ssj562.2919.10333	14	14	Deloma se strinjam z drugim delom članka, ko opisuje finančne učinke reforme.
2	2	ssj562.2919.10334	32	32	Namreč po zdravi "kmečki pameti" in lastnih izkušnjah še nobena reforma ni prinesla nečesa več, kvečjemu nekaj manj, predvsem pa na drugačen način, po možnosti boljši.
3	3	ssj562.2919.10335	17	17	Reforme se ne delajo, ko imamo vsega dovolj, ampak, ko imamo nečesa premalo.
4	4	ssj562.2919.10336	17	17	Ob tem sem se namenoma izognil besedi denarja, saj lahko gre tudi za druge stvari.
5	5	ssj562.2920.10337	17	17	Sedanje stanje bi strnil takole: Odločilen element zdravljenja bolnika je izbrani zdravnik na primarnem nivoju.
6	6	ssj562.2920.10338	35	35	Ta v primeru potrebe po svoji presoji napoti bolnika k specialistu na sekundarnem nivoju z napotnico, kjer je izražena želja o vrsti pregleda, trajanju in vrsti pooblastil, ki jih prenese nanj.
7	7	ssj562.2921.10339	24	24	Na nedavnem mednarodnem turnirju mladih judoistov za pokal Ptuja je sodelovalo 285 tekmovalcev in tekmovalk iz 27 klubov Madžarske, Hrvaške in Slovenije.
8	8	ssj562.2921.10340	17	17	Pomurci so osvojili kopico visokih mest, a se nobenemu ni uspelo povzpeti na najvišjo stopničko.
9	9	ssj562.2922.10341	8	8	Način uporabe gomoljev topinamburja je podoben krompirjevim.
10	10	ssj562.2922.10342	21	21	V primerjavi s krompirjem pa lahko topinambur brez bojazni za zdravje uživamo surov, torej sveže ali napol kuhane gomolje.
11	11	ssj562.2922.10343	18	18	Sveži gomolji imajo svojevrsten okus; kuhani, dušeni ali pečeni so sočnejši in rahlejši od krompirjevih.
12	12	ssj562.2922.10344	22	22	Postrežemo ga lahko kot začetno jed, v juhi, prilogah, solatah, za dieto pa je lahko samostojna jed.
13	13	ssj562.2922.10345	18	18	Pri pripravi jedi si lahko izposodimo recepte za krompir, beluši, kolerabo, cvetačo ali artičoko.
14	14	ssj562.2923.10346	28	28	Čepinci se vsaj po kažipotu čisto držijo Markovec, čeprav to v praksi pomeni, da je nekaj hiš na tem bregu, nekaj pa na onem.
15	15	ssj562.2923.10347	10	10	Kajti največja značilnost Čepinec je prav gotovo izredna razpršenost.
16	16	ssj562.2923.10348	20	20	Domovanja dobrih 400 prebivalcev so raztresena na več kilometrih in le redko se v Čepincih več hiš drži skupaj.
17	17	ssj562.2923.10349	20	20	Tukaj prav čutimo odmaknjenost od prometnih poti, zato je ta kraj v preteklosti občutil izredno veliko demografsko ogroženost.
18	18	ssj562.2923.10350	24	24	V zadnjem času se spet pojavljajo poskusi, oživiti življenje mladih in malo manj mladih, ravno sedaj pa tam gradijo vodovodno omrežje.
19	19	ssj562.2923.10351	29	29	V enem od "centrov" Čepinec so še vedno neobnovljene stavbe, je pa tam kot posebnost velika lipa, ki raste pred okrepčevalnico z enakim imenom.
20	20	ssj562.2923.10352	37	37	Tukaj srečamo več avtomobilov z madžarskimi registracijami, saj je v bližini mejni prehod z Madžarsko Čepinci - Verica, in tudi v zgornjem delu Čepinec nas pot vodi tik ob meji z našo vzhodno sosedo.
