# Stanza aligned error analysis (gold vs predicted)

- Gold sentences: 420
- Pred sentences: 420
- Paired sentences: 420
- Unmatched gold sentences: 0
- Unmatched predicted sentences: 0
- Skipped sentence pairs (length mismatch): 0
- Tokens compared (form-aligned): 11443
- Tokens skipped due to FORM mismatch: 0

## Core accuracy on compared tokens
- UAS proxy (HEAD only): 9706/11443 = 84.82%
- DEPREL accuracy: 10218/11443 = 89.29%
- LAS proxy (HEAD+DEPREL): 9209/11443 = 80.48%

## Error buckets
- Wrong head only: 1009
- Wrong relation only: 497
- Wrong head and relation: 728

## Wrong head only (top)

gold_deprel	count
punct	370
discourse	146
advmod	111
conj	69
parataxis	65
cc	36
mark	24
obl	22
reparandum	21
nmod	20
acl	20
advcl	19
nsubj	17
obj	13
case	9
cop	9
expl	7
appos	6
aux	6
orphan	5

## Wrong relation only (top)

gold_deprel	pred_deprel	count
advmod	nsubj	18
nsubj	advmod	16
conj	parataxis	13
advmod	obj	12
aux	cop	11
advmod	orphan	11
parataxis	conj	10
obj	iobj	10
advmod	obl	10
reparandum	punct	10
obl	nmod	9
nmod	obl	9
cc	advmod	9
appos	conj	9
det	amod	9
mark	discourse	8
advmod	cc	8
advmod	amod	7
cc	discourse	7
advmod	discourse	7

## Wrong head and relation (top)

gold_deprel	pred_deprel	count
obl	nmod	28
reparandum	punct	27
parataxis	root	18
conj	parataxis	13
root	parataxis	11
root	nsubj	10
fixed	advmod	10
nsubj	parataxis	9
fixed	mark	9
nmod	obl	8
parataxis	nsubj	8
cop	parataxis	8
advmod	nmod	8
advmod	root	7
advcl	acl	7
conj	nsubj	7
advcl	parataxis	7
discourse	advmod	7
fixed	discourse	7
appos	obl	7
