# Stanza aligned error analysis (gold vs predicted)

- Gold sentences: 432
- Pred sentences: 432
- Paired sentences: 432
- Unmatched gold sentences: 0
- Unmatched predicted sentences: 0
- Skipped sentence pairs (length mismatch): 0
- Tokens compared (form-aligned): 11443
- Tokens skipped due to FORM mismatch: 0

## Core accuracy on compared tokens
- UAS proxy (HEAD only): 10150/11443 = 88.70%
- DEPREL accuracy: 10717/11443 = 93.66%
- LAS proxy (HEAD+DEPREL): 9856/11443 = 86.13%

## Error buckets
- Wrong head only: 861
- Wrong relation only: 294
- Wrong head and relation: 432

## Wrong head only (top)

gold_deprel	count
punct	312
discourse	114
advmod	99
parataxis	66
conj	53
reparandum	30
cc	25
advcl	21
mark	20
acl	19
nmod	16
obl	14
cop	12
nsubj	10
case	9
aux	9
expl	6
appos	6
det	5
obj	4

## Wrong relation only (top)

gold_deprel	pred_deprel	count
parataxis	conj	13
obj	iobj	13
discourse	advmod	11
orphan	advmod	9
appos	conj	9
advmod	orphan	8
parataxis	cc	8
nmod	obl	7
discourse	cc	7
obl	nmod	6
conj	parataxis	6
appos	nmod	6
conj	appos	6
cc	advmod	5
nmod	conj	5
ccomp	advcl	4
obl	advmod	4
reparandum	advmod	4
advmod	cc	4
parataxis	advcl	4

## Wrong head and relation (top)

gold_deprel	pred_deprel	count
obl	nmod	19
parataxis	root	14
root	parataxis	13
nmod	obl	9
parataxis	nsubj	7
conj	parataxis	7
root	nsubj	7
nsubj	root	7
acl	advcl	6
appos	obj	6
reparandum	root	6
conj	amod	6
reparandum	parataxis	6
cop	parataxis	6
appos	conj	6
reparandum	conj	5
conj	nsubj	5
reparandum	mark	5
reparandum	obl	5
reparandum	case	5
