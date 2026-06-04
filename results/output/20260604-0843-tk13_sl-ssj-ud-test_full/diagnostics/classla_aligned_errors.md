# CLASSLA aligned error analysis (gold vs predicted)

- Gold sentences: 1282
- Pred sentences: 1282
- Paired sentences: 1282
- Unmatched gold sentences: 0
- Unmatched predicted sentences: 0
- Skipped sentence pairs (length mismatch): 0
- Tokens compared (form-aligned): 25442
- Tokens skipped due to FORM mismatch: 0

## Core accuracy on compared tokens
- UAS proxy (HEAD only): 23437/25442 = 92.12%
- DEPREL accuracy: 24223/25442 = 95.21%
- LAS proxy (HEAD+DEPREL): 23021/25442 = 90.48%

## Error buckets
- Wrong head only: 1202
- Wrong relation only: 416
- Wrong head and relation: 803

## Wrong head only (top)

gold_deprel	count
punct	355
advmod	161
nmod	116
conj	108
obl	76
acl	52
cc	39
parataxis	37
aux	37
mark	34
nsubj	30
cop	29
advcl	27
appos	19
csubj	17
case	17
obj	11
amod	10
expl	6
orphan	4

## Wrong relation only (top)

gold_deprel	pred_deprel	count
obj	nsubj	30
obj	iobj	29
nsubj	obj	28
conj	parataxis	16
nmod	flat	12
obl	nsubj	11
iobj	obj	10
appos	conj	10
cc	advmod	9
flat	nmod	9
conj	appos	8
iobj	expl	8
obl	obj	7
advmod	amod	6
nsubj	obl	6
obl	nmod	5
advmod	nsubj	5
conj	flat	5
nmod	amod	5
nmod	obl	4

## Wrong head and relation (top)

gold_deprel	pred_deprel	count
obl	nmod	89
nmod	obl	62
root	cop	28
nsubj	root	24
parataxis	root	23
root	parataxis	18
cop	root	15
root	nsubj	13
advcl	acl	12
obj	nmod	11
nsubj	conj	10
nmod	nsubj	10
parataxis	appos	9
nsubj	parataxis	9
conj	cop	9
cc	advmod	8
nsubj	nmod	8
acl	advcl	7
root	ccomp	7
parataxis	acl	7
