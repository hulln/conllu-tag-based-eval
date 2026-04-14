# CLASSLA base error analysis (gold vs predicted)

- Gold sentences: 1282
- Pred sentences: 1287
- Paired sentences: 1279
- Unmatched gold sentences: 3
- Unmatched predicted sentences: 8
- Skipped sentence pairs (length mismatch): 7
- Tokens compared (form-aligned): 25222
- Tokens skipped due to FORM mismatch: 0

## Core accuracy on compared tokens
- UAS proxy (HEAD only): 23258/25222 = 92.21%
- DEPREL accuracy: 24026/25222 = 95.26%
- LAS proxy (HEAD+DEPREL): 22846/25222 = 90.58%

## Error buckets
- Wrong head only: 1180
- Wrong relation only: 412
- Wrong head and relation: 784

## Wrong head only (top)

gold_deprel	count
punct	345
advmod	160
nmod	115
conj	106
obl	74
acl	52
cc	39
parataxis	36
aux	36
mark	33
nsubj	29
cop	28
advcl	27
appos	19
csubj	16
case	16
obj	11
amod	10
expl	6
nummod	5

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
obl	nmod	88
nmod	obl	62
root	cop	28
nsubj	root	24
parataxis	root	23
root	parataxis	18
cop	root	14
root	nsubj	13
obj	nmod	11
advcl	acl	11
nsubj	conj	10
parataxis	appos	9
conj	cop	9
nmod	nsubj	9
nsubj	parataxis	8
cc	advmod	8
nsubj	nmod	8
acl	advcl	7
root	ccomp	7
parataxis	acl	7
