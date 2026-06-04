# CLASSLA aligned error analysis (gold vs predicted)

- Gold sentences: 432
- Pred sentences: 432
- Paired sentences: 432
- Unmatched gold sentences: 0
- Unmatched predicted sentences: 0
- Skipped sentence pairs (length mismatch): 0
- Tokens compared (form-aligned): 11443
- Tokens skipped due to FORM mismatch: 0

## Core accuracy on compared tokens
- UAS proxy (HEAD only): 9754/11443 = 85.24%
- DEPREL accuracy: 10485/11443 = 91.63%
- LAS proxy (HEAD+DEPREL): 9392/11443 = 82.08%

## Error buckets
- Wrong head only: 1093
- Wrong relation only: 362
- Wrong head and relation: 596

## Wrong head only (top)

gold_deprel	count
punct	370
discourse	135
advmod	128
conj	84
parataxis	74
cc	46
mark	29
reparandum	25
obl	25
advcl	23
acl	23
nsubj	22
nmod	20
obj	16
aux	15
case	14
cop	10
expl	9
appos	7
det	5

## Wrong relation only (top)

gold_deprel	pred_deprel	count
appos	conj	18
parataxis	conj	13
discourse	advmod	13
obj	nsubj	11
orphan	advmod	10
advmod	orphan	10
nummod	det	10
iobj	obj	9
obj	iobj	9
advmod	cc	8
nmod	obl	7
cc	advmod	7
conj	parataxis	7
conj	appos	7
nsubj	obj	6
advmod	discourse	6
obl	obj	6
nmod	conj	5
obl	nmod	4
ccomp	advcl	4

## Wrong head and relation (top)

gold_deprel	pred_deprel	count
obl	nmod	24
nmod	obl	21
nsubj	root	21
parataxis	root	17
root	parataxis	15
conj	parataxis	10
root	nsubj	10
root	cop	10
conj	obl	10
advcl	acl	8
orphan	advmod	8
reparandum	case	8
nsubj	conj	8
reparandum	conj	7
parataxis	advcl	7
conj	amod	7
reparandum	root	6
cop	root	6
parataxis	acl	6
parataxis	cop	6
