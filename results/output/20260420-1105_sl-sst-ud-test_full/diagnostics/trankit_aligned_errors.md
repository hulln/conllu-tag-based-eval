# Trankit aligned error analysis (gold vs predicted)

- Gold sentences: 432
- Pred sentences: 432
- Paired sentences: 432
- Unmatched gold sentences: 0
- Unmatched predicted sentences: 0
- Skipped sentence pairs (length mismatch): 0
- Tokens compared (form-aligned): 11443
- Tokens skipped due to FORM mismatch: 0

## Core accuracy on compared tokens
- UAS proxy (HEAD only): 10190/11443 = 89.05%
- DEPREL accuracy: 10796/11443 = 94.35%
- LAS proxy (HEAD+DEPREL): 9921/11443 = 86.70%

## Error buckets
- Wrong head only: 875
- Wrong relation only: 269
- Wrong head and relation: 378

## Wrong head only (top)

gold_deprel	count
punct	323
discourse	121
advmod	85
conj	74
parataxis	58
reparandum	45
cc	23
obl	22
nsubj	17
nmod	16
mark	15
advcl	15
acl	12
case	8
obj	7
aux	7
orphan	4
appos	4
cop	4
csubj	3

## Wrong relation only (top)

gold_deprel	pred_deprel	count
parataxis	conj	14
appos	conj	11
discourse	advmod	10
obj	iobj	10
parataxis	cc	8
conj	parataxis	7
nmod	obl	6
orphan	advmod	6
advmod	discourse	6
obj	nsubj	6
appos	nmod	6
advmod	cc	6
nsubj	obj	5
advmod	orphan	5
discourse	cc	5
cc	advmod	5
nmod	appos	5
obl	nmod	4
nsubj	advmod	4
obl	obj	4

## Wrong head and relation (top)

gold_deprel	pred_deprel	count
parataxis	root	17
root	parataxis	14
nmod	obl	11
obl	nmod	8
cop	parataxis	8
reparandum	orphan	7
orphan	advmod	7
appos	obl	7
reparandum	conj	7
parataxis	nsubj	6
advcl	acl	5
reparandum	root	5
appos	obj	5
conj	parataxis	5
root	nsubj	5
fixed	advmod	5
nsubj	root	5
root	obl	4
conj	root	4
root	advmod	4
