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
- UAS proxy (HEAD only): 8564/11443 = 74.84%
- DEPREL accuracy: 9436/11443 = 82.46%
- LAS proxy (HEAD+DEPREL): 7951/11443 = 69.48%

## Error buckets
- Wrong head only: 1485
- Wrong relation only: 613
- Wrong head and relation: 1394

## Wrong head only (top)

gold_deprel	count
punct	761
advmod	162
conj	82
parataxis	77
cc	67
mark	41
discourse	37
obl	34
nsubj	33
case	29
acl	26
aux	25
advcl	24
nmod	19
cop	16
obj	13
amod	11
expl	9
appos	4
csubj	4

## Wrong relation only (top)

gold_deprel	pred_deprel	count
discourse	parataxis	71
discourse	nsubj	56
discourse	vocative	25
cc	advmod	22
conj	parataxis	18
discourse	advmod	15
obj	nsubj	15
discourse	conj	13
nmod	conj	12
orphan	advmod	11
parataxis	conj	11
obj	iobj	11
appos	conj	11
det	nummod	10
cc	mark	10
nsubj	iobj	9
advmod	orphan	9
nmod	obl	7
reparandum	amod	7
obl	nmod	6

## Wrong head and relation (top)

gold_deprel	pred_deprel	count
discourse	conj	124
discourse	appos	84
discourse	nmod	63
discourse	parataxis	28
obl	nmod	26
root	parataxis	22
parataxis	root	21
discourse	vocative	20
fixed	advmod	20
reparandum	conj	19
nsubj	conj	18
root	cop	18
reparandum	case	18
nsubj	parataxis	17
nsubj	root	17
mark	fixed	17
obl	conj	17
discourse	cc	15
reparandum	advmod	14
parataxis	conj	13
