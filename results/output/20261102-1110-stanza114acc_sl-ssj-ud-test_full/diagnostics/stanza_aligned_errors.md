# Stanza aligned error analysis (gold vs predicted)

- Gold sentences: 1282
- Pred sentences: 1282
- Paired sentences: 1282
- Unmatched gold sentences: 0
- Unmatched predicted sentences: 0
- Skipped sentence pairs (length mismatch): 0
- Tokens compared (form-aligned): 25442
- Tokens skipped due to FORM mismatch: 0

## Core accuracy on compared tokens
- UAS proxy (HEAD only): 24418/25442 = 95.98%
- DEPREL accuracy: 24768/25442 = 97.35%
- LAS proxy (HEAD+DEPREL): 24134/25442 = 94.86%

## Error buckets
- Wrong head only: 634
- Wrong relation only: 284
- Wrong head and relation: 390

## Wrong head only (top)

gold_deprel	count
punct	181
advmod	82
conj	78
nmod	76
acl	28
obl	27
parataxis	22
advcl	19
cc	18
appos	14
aux	14
mark	12
cop	11
nsubj	10
expl	7
nummod	6
obj	5
csubj	5
case	5
amod	4

## Wrong relation only (top)

gold_deprel	pred_deprel	count
obj	iobj	25
conj	parataxis	15
nmod	flat	14
iobj	obj	11
obj	nsubj	7
parataxis	conj	7
appos	conj	6
nsubj	obj	6
iobj	expl	6
advmod	cc	5
orphan	advmod	5
amod	nmod	5
obl	advmod	5
nmod	amod	5
advcl	ccomp	4
appos	nmod	4
cc	advmod	4
mark	advmod	4
conj	flat	4
advmod	obl	4

## Wrong head and relation (top)

gold_deprel	pred_deprel	count
obl	nmod	44
nmod	obl	37
parataxis	root	22
root	parataxis	14
advcl	acl	10
root	cop	9
nsubj	root	9
root	ccomp	7
parataxis	appos	7
root	nsubj	5
nmod	nsubj	5
nsubj	parataxis	5
parataxis	nsubj	5
nmod	appos	5
appos	nmod	5
nsubj	acl	5
obj	iobj	4
cop	acl	4
conj	parataxis	4
cop	root	4
