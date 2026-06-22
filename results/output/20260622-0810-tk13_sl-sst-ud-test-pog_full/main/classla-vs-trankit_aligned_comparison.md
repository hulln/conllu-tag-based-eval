# Trankit aligned vs CLASSLA aligned (exact difference report)

## Coverage
- Gold sentences: 420
- Trankit aligned predicted sentences: 420
- CLASSLA aligned predicted sentences: 420
- Gold sentences paired with both models: 420
- Unmatched gold for Trankit aligned: 0
- Unmatched gold for CLASSLA aligned: 0
- Unmatched predicted for Trankit aligned: 0
- Unmatched predicted for CLASSLA aligned: 0
- Skipped sentence pairs (token count mismatch): 0
- Compared tokens (FORM-aligned): 11443
- Skipped tokens (FORM mismatch): 0

## LAS exact differences
- Trankit aligned correct, CLASSLA aligned wrong: 1652 (14.44%)
- Trankit aligned wrong, CLASSLA aligned correct: 530 (4.63%)
- Both correct: 7933 (69.33%)
- Both wrong: 1328 (11.61%)

## UAS exact differences
- Trankit aligned correct, CLASSLA aligned wrong: 1384 (12.09%)
- Trankit aligned wrong, CLASSLA aligned correct: 528 (4.61%)
- Both correct: 8509 (74.36%)
- Both wrong: 1022 (8.93%)

## DEPREL exact differences
- Trankit aligned correct, CLASSLA aligned wrong: 1030 (9.00%)
- Trankit aligned wrong, CLASSLA aligned correct: 222 (1.94%)
- Both correct: 9629 (84.15%)
- Both wrong: 562 (4.91%)

## Top LAS mistakes where Trankit aligned wins
gold_deprel	pred_deprel	count
punct	punct	231
advmod	advmod	100
discourse	discourse	96
conj	conj	40
advmod	nsubj	38
cc	cc	36
parataxis	parataxis	31
obl	nmod	30
mark	mark	29
obl	obl	26
nsubj	nsubj	26
case	case	22
obj	obj	20
aux	aux	20
obj	nsubj	16
advmod	amod	15
nsubj	root	15
root	parataxis	14
advcl	advcl	14
det	amod	14

## Top LAS mistakes where Trankit aligned loses to CLASSLA aligned
gold_deprel	pred_deprel	count
punct	punct	125
advmod	advmod	44
discourse	discourse	38
conj	conj	24
obl	obl	17
nsubj	nsubj	16
cc	cc	13
obj	obj	10
parataxis	parataxis	9
amod	amod	9
acl	acl	9
cop	cop	8
nmod	obl	8
case	case	7
parataxis	conj	7
mark	mark	7
obl	nmod	6
nmod	nmod	6
advcl	advcl	5
root	obl	5

## Top DEPREL mistakes where Trankit aligned wins
gold_deprel	pred_deprel	count
advmod	nsubj	42
obl	nmod	32
conj	parataxis	19
advmod	amod	17
obj	nsubj	17
nmod	obl	17
advmod	obj	15
nsubj	root	15
root	parataxis	14
det	amod	14
advmod	parataxis	12
fixed	advmod	12
reparandum	amod	12
parataxis	conj	12
obl	obj	11
appos	conj	11
mark	advmod	11
nsubj	obj	10
advmod	orphan	10
advmod	det	10

## Top DEPREL mistakes where Trankit aligned loses to CLASSLA aligned
gold_deprel	pred_deprel	count
parataxis	conj	12
nmod	obl	9
obl	nmod	8
conj	parataxis	7
nsubj	obj	6
root	obl	5
obj	iobj	5
parataxis	acl	5
advmod	orphan	4
obj	nsubj	4
conj	appos	4
parataxis	root	4
cop	parataxis	4
root	parataxis	3
cc	discourse	3
nsubj	advmod	3
parataxis	nsubj	3
nsubj	obl	3
cc	advmod	3
ccomp	parataxis	3
