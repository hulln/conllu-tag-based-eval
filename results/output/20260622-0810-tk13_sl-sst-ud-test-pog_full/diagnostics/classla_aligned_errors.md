# CLASSLA aligned error analysis (gold vs predicted)

- Gold sentences: 420
- Pred sentences: 420
- Paired sentences: 420
- Unmatched gold sentences: 0
- Unmatched predicted sentences: 0
- Skipped sentence pairs (length mismatch): 0
- Tokens compared (form-aligned): 11443
- Tokens skipped due to FORM mismatch: 0

## Core accuracy on compared tokens
- UAS proxy (HEAD only): 9037/11443 = 78.97%
- DEPREL accuracy: 9851/11443 = 86.09%
- LAS proxy (HEAD+DEPREL): 8463/11443 = 73.96%

## Error buckets
- Wrong head only: 1388
- Wrong relation only: 574
- Wrong head and relation: 1018

## Wrong head only (top)

gold_deprel	count
punct	453
discourse	187
advmod	163
conj	96
parataxis	78
cc	54
mark	45
nsubj	44
obl	39
aux	30
nmod	29
case	26
obj	24
advcl	24
acl	24
expl	16
cop	16
amod	9
reparandum	8
det	8

## Wrong relation only (top)

gold_deprel	pred_deprel	count
advmod	nsubj	42
appos	conj	19
det	amod	16
advmod	obj	14
advmod	orphan	13
obj	nsubj	13
obl	obj	12
conj	parataxis	12
advmod	amod	11
mark	advmod	11
parataxis	conj	10
nummod	det	10
discourse	advmod	10
nsubj	obj	9
obj	iobj	9
orphan	advmod	8
iobj	obj	8
fixed	nmod	8
reparandum	amod	8
advmod	cc	8

## Wrong head and relation (top)

gold_deprel	pred_deprel	count
obl	nmod	38
root	parataxis	23
nmod	obl	23
reparandum	conj	17
parataxis	root	17
nsubj	root	17
conj	parataxis	15
fixed	advmod	14
advmod	root	12
orphan	advmod	11
conj	amod	11
parataxis	conj	11
reparandum	root	10
advmod	parataxis	10
root	cop	10
obl	conj	10
advmod	nmod	10
advcl	acl	9
parataxis	cop	9
nsubj	parataxis	9
