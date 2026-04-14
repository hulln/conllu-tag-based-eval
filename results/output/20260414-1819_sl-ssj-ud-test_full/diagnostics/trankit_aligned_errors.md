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
- UAS proxy (HEAD only): 24372/25442 = 95.79%
- DEPREL accuracy: 24732/25442 = 97.21%
- LAS proxy (HEAD+DEPREL): 24066/25442 = 94.59%

## Error buckets
- Wrong head only: 666
- Wrong relation only: 306
- Wrong head and relation: 404

## Wrong head only (top)

gold_deprel	count
punct	198
advmod	97
conj	80
nmod	76
obl	34
parataxis	27
advcl	21
acl	21
cc	15
appos	15
nsubj	13
aux	12
cop	11
mark	10
case	9
nummod	5
amod	4
obj	4
ccomp	4
expl	2

## Wrong relation only (top)

gold_deprel	pred_deprel	count
iobj	obj	19
nmod	flat	17
obj	iobj	14
conj	parataxis	13
nsubj	obj	12
obj	nsubj	10
nmod	obl	7
orphan	advmod	6
appos	nmod	6
advcl	ccomp	5
iobj	expl	5
cc	advmod	5
conj	flat	5
advmod	obl	5
appos	conj	5
advcl	advmod	5
orphan	nmod	4
parataxis	conj	4
nmod	amod	4
advmod	cc	3

## Wrong head and relation (top)

gold_deprel	pred_deprel	count
obl	nmod	44
nmod	obl	39
parataxis	root	21
root	parataxis	12
nsubj	root	10
advcl	acl	9
parataxis	appos	8
root	cop	7
root	ccomp	7
root	nsubj	6
nmod	flat	6
nmod	appos	6
acl	advcl	5
conj	amod	5
appos	nmod	4
obj	nmod	4
nmod	obj	4
case	fixed	4
appos	flat	4
appos	nummod	4
