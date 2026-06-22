# Trankit aligned error analysis (gold vs predicted)

- Gold sentences: 420
- Pred sentences: 420
- Paired sentences: 420
- Unmatched gold sentences: 0
- Unmatched predicted sentences: 0
- Skipped sentence pairs (length mismatch): 0
- Tokens compared (form-aligned): 11443
- Tokens skipped due to FORM mismatch: 0

## Core accuracy on compared tokens
- UAS proxy (HEAD only): 9893/11443 = 86.45%
- DEPREL accuracy: 10659/11443 = 93.15%
- LAS proxy (HEAD+DEPREL): 9585/11443 = 83.76%

## Error buckets
- Wrong head only: 1074
- Wrong relation only: 308
- Wrong head and relation: 476

## Wrong head only (top)

gold_deprel	count
punct	347
discourse	130
advmod	120
conj	83
parataxis	66
reparandum	44
obl	34
nsubj	33
cc	33
acl	24
mark	22
advcl	20
nmod	20
obj	16
aux	14
cop	13
case	12
amod	9
appos	7
det	6

## Wrong relation only (top)

gold_deprel	pred_deprel	count
parataxis	conj	12
obj	iobj	9
nmod	obl	8
conj	parataxis	8
nsubj	obj	7
ccomp	advcl	7
parataxis	cc	7
appos	conj	7
obl	nmod	6
advmod	discourse	6
discourse	advmod	6
conj	appos	6
discourse	orphan	5
iobj	obj	5
advmod	orphan	5
obj	nsubj	5
cc	advmod	5
nsubj	advmod	4
orphan	advmod	4
discourse	cc	4

## Wrong head and relation (top)

gold_deprel	pred_deprel	count
parataxis	root	16
obl	nmod	16
root	parataxis	14
nmod	obl	14
conj	parataxis	13
parataxis	conj	10
parataxis	acl	8
reparandum	root	7
orphan	advmod	7
parataxis	nsubj	7
reparandum	conj	7
root	obl	6
advcl	acl	6
appos	obl	6
appos	parataxis	6
cop	parataxis	6
fixed	advmod	5
ccomp	parataxis	5
reparandum	orphan	5
advmod	reparandum	4
