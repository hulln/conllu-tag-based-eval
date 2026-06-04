# Trankit aligned error analysis (gold vs predicted)

- Gold sentences: 1282
- Pred sentences: 1282
- Paired sentences: 1282
- Unmatched gold sentences: 0
- Unmatched predicted sentences: 0
- Skipped sentence pairs (length mismatch): 0
- Tokens compared (form-aligned): 25442
- Tokens skipped due to FORM mismatch: 0

## Core accuracy on compared tokens
- UAS proxy (HEAD only): 24353/25442 = 95.72%
- DEPREL accuracy: 24721/25442 = 97.17%
- LAS proxy (HEAD+DEPREL): 24037/25442 = 94.48%

## Error buckets
- Wrong head only: 684
- Wrong relation only: 316
- Wrong head and relation: 405

## Wrong head only (top)

gold_deprel	count
punct	199
advmod	94
nmod	83
conj	77
obl	30
parataxis	30
advcl	22
acl	22
cc	20
appos	17
cop	14
mark	13
aux	12
case	10
nsubj	9
amod	8
obj	4
det	4
nummod	3
expl	3

## Wrong relation only (top)

gold_deprel	pred_deprel	count
iobj	obj	17
obj	iobj	15
nmod	flat	14
orphan	advmod	11
conj	parataxis	11
nsubj	obj	10
obj	nsubj	8
parataxis	conj	7
nmod	obl	7
cc	advmod	6
appos	nmod	6
advmod	cc	5
conj	flat	5
advmod	obl	5
nmod	appos	5
appos	conj	5
advcl	ccomp	4
iobj	expl	4
amod	nmod	4
nmod	amod	4

## Wrong head and relation (top)

gold_deprel	pred_deprel	count
obl	nmod	40
nmod	obl	38
parataxis	root	24
root	parataxis	14
parataxis	appos	11
advcl	acl	9
nsubj	root	9
root	ccomp	7
root	cop	6
root	nsubj	6
conj	advmod	5
nmod	appos	5
nmod	flat	5
acl	advcl	4
parataxis	nummod	4
obj	nmod	4
nsubj	amod	4
orphan	conj	4
conj	flat	4
nsubj	nmod	4
