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
- UAS proxy (HEAD only): 23657/25442 = 92.98%
- DEPREL accuracy: 24326/25442 = 95.61%
- LAS proxy (HEAD+DEPREL): 23171/25442 = 91.07%

## Error buckets
- Wrong head only: 1155
- Wrong relation only: 486
- Wrong head and relation: 630

## Wrong head only (top)

gold_deprel	count
advmod	349
punct	330
conj	95
nmod	86
obl	49
parataxis	46
acl	27
nsubj	21
cc	21
advcl	20
cop	19
mark	17
aux	15
appos	14
case	13
amod	8
obj	8
nummod	8
flat	3
xcomp	2

## Wrong relation only (top)

gold_deprel	pred_deprel	count
iobj	obj	53
conj	parataxis	27
orphan	advmod	26
nmod	obl	23
nsubj	obj	12
advcl	parataxis	12
iobj	expl	12
det	nmod	12
obl	obj	10
obj	nsubj	10
flat	nmod	10
cc	advmod	9
case	advmod	8
obl	nmod	8
appos	nmod	7
appos	conj	7
nmod	amod	7
orphan	nmod	6
parataxis	nsubj	6
nmod	flat	6

## Wrong head and relation (top)

gold_deprel	pred_deprel	count
nmod	obl	52
obl	nmod	44
root	parataxis	34
orphan	advmod	24
parataxis	root	21
ccomp	root	18
advcl	acl	15
nsubj	root	15
root	nsubj	11
parataxis	appos	11
parataxis	conj	10
root	cop	9
conj	parataxis	9
flat	nmod	9
parataxis	advmod	7
orphan	conj	7
obl	appos	7
fixed	case	6
nsubj	nmod	6
parataxis	nummod	6
