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
- UAS proxy (HEAD only): 10207/11443 = 89.20%
- DEPREL accuracy: 10798/11443 = 94.36%
- LAS proxy (HEAD+DEPREL): 9939/11443 = 86.86%

## Error buckets
- Wrong head only: 859
- Wrong relation only: 268
- Wrong head and relation: 377

## Wrong head only (top)

gold_deprel	count
punct	308
discourse	123
advmod	80
conj	67
parataxis	62
reparandum	39
obl	23
cc	21
mark	18
nsubj	18
advcl	15
nmod	15
acl	14
obj	10
aux	9
cop	9
case	7
orphan	4
appos	4
nummod	3

## Wrong relation only (top)

gold_deprel	pred_deprel	count
parataxis	conj	11
conj	parataxis	9
discourse	advmod	8
advmod	orphan	7
advmod	discourse	7
orphan	advmod	7
appos	conj	7
cc	advmod	7
obj	iobj	7
nmod	obl	6
parataxis	cc	6
obj	nsubj	6
discourse	cc	5
obl	obj	5
obl	advmod	5
nsubj	obj	4
obl	nmod	4
iobj	obj	4
appos	nmod	4
conj	appos	4

## Wrong head and relation (top)

gold_deprel	pred_deprel	count
parataxis	root	14
root	parataxis	14
nmod	obl	12
conj	parataxis	9
orphan	advmod	8
parataxis	acl	8
reparandum	root	7
parataxis	nsubj	7
obl	nmod	7
cop	parataxis	7
nsubj	root	6
fixed	advmod	6
advcl	acl	5
appos	obj	5
reparandum	conj	5
reparandum	orphan	4
root	advmod	4
appos	obl	4
root	cop	4
appos	parataxis	4
