# Trankit base error analysis (gold vs predicted)

- Gold sentences: 1282
- Pred sentences: 1291
- Paired sentences: 1258
- Unmatched gold sentences: 24
- Unmatched predicted sentences: 33
- Skipped sentence pairs (length mismatch): 21
- Tokens compared (form-aligned): 24520
- Tokens skipped due to FORM mismatch: 0

## Core accuracy on compared tokens
- UAS proxy (HEAD only): 22857/24520 = 93.22%
- DEPREL accuracy: 23490/24520 = 95.80%
- LAS proxy (HEAD+DEPREL): 22403/24520 = 91.37%

## Error buckets
- Wrong head only: 1087
- Wrong relation only: 454
- Wrong head and relation: 576

## Wrong head only (top)

gold_deprel	count
advmod	346
punct	286
conj	91
nmod	82
obl	49
parataxis	44
acl	26
nsubj	20
advcl	20
cc	19
cop	18
mark	16
aux	15
appos	13
case	11
amod	8
obj	8
nummod	6
flat	3
xcomp	2

## Wrong relation only (top)

gold_deprel	pred_deprel	count
iobj	obj	51
conj	parataxis	27
orphan	advmod	25
nmod	obl	22
nsubj	obj	12
iobj	expl	12
det	nmod	12
advcl	parataxis	11
obl	obj	10
obj	nsubj	10
flat	nmod	10
cc	advmod	9
obl	nmod	8
case	advmod	7
appos	nmod	7
nmod	amod	7
orphan	nmod	6
parataxis	nsubj	6
appos	conj	6
advmod	nmod	5

## Wrong head and relation (top)

gold_deprel	pred_deprel	count
nmod	obl	51
obl	nmod	42
root	parataxis	29
orphan	advmod	23
ccomp	root	17
advcl	acl	15
parataxis	root	15
nsubj	root	15
root	nsubj	11
parataxis	conj	10
parataxis	appos	10
root	cop	9
conj	parataxis	9
flat	nmod	9
parataxis	advmod	7
obl	appos	7
orphan	conj	6
nsubj	nmod	6
orphan	obl	6
nmod	obj	6
