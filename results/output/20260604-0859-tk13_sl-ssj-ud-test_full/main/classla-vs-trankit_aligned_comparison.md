# Trankit aligned vs CLASSLA aligned (exact difference report)

## Coverage
- Gold sentences: 1282
- Trankit aligned predicted sentences: 1282
- CLASSLA aligned predicted sentences: 1282
- Gold sentences paired with both models: 1282
- Unmatched gold for Trankit aligned: 0
- Unmatched gold for CLASSLA aligned: 0
- Unmatched predicted for Trankit aligned: 0
- Unmatched predicted for CLASSLA aligned: 0
- Skipped sentence pairs (token count mismatch): 0
- Compared tokens (FORM-aligned): 25442
- Skipped tokens (FORM mismatch): 0

## LAS exact differences
- Trankit aligned correct, CLASSLA aligned wrong: 1543 (6.06%)
- Trankit aligned wrong, CLASSLA aligned correct: 527 (2.07%)
- Both correct: 22494 (88.41%)
- Both wrong: 878 (3.45%)

## UAS exact differences
- Trankit aligned correct, CLASSLA aligned wrong: 1335 (5.25%)
- Trankit aligned wrong, CLASSLA aligned correct: 419 (1.65%)
- Both correct: 23018 (90.47%)
- Both wrong: 670 (2.63%)

## DEPREL exact differences
- Trankit aligned correct, CLASSLA aligned wrong: 809 (3.18%)
- Trankit aligned wrong, CLASSLA aligned correct: 311 (1.22%)
- Both correct: 23912 (93.99%)
- Both wrong: 410 (1.61%)

## Top LAS mistakes where Trankit aligned wins
gold_deprel	pred_deprel	count
punct	punct	221
advmod	advmod	98
conj	conj	70
obl	nmod	68
obl	obl	57
nmod	nmod	55
nmod	obl	45
acl	acl	37
aux	aux	30
cc	cc	29
nsubj	obj	25
mark	mark	25
parataxis	parataxis	24
obj	nsubj	23
root	cop	23
nsubj	nsubj	22
cop	cop	20
obj	iobj	20
nsubj	root	20
csubj	csubj	17

## Top LAS mistakes where Trankit aligned loses to CLASSLA aligned
gold_deprel	pred_deprel	count
punct	punct	66
conj	conj	35
advmod	advmod	30
nmod	obl	23
nmod	nmod	23
obl	nmod	17
iobj	obj	14
obl	obl	14
parataxis	parataxis	13
advcl	advcl	12
appos	appos	10
nmod	flat	9
cc	cc	9
acl	acl	8
parataxis	conj	8
nsubj	obj	7
root	parataxis	7
cop	cop	7
orphan	advmod	6
nmod	appos	6

## Top DEPREL mistakes where Trankit aligned wins
gold_deprel	pred_deprel	count
obl	nmod	68
nmod	obl	48
nsubj	obj	25
obj	nsubj	24
root	cop	23
obj	iobj	20
nsubj	root	20
cop	root	15
cc	advmod	13
root	parataxis	12
conj	parataxis	11
nsubj	conj	11
root	nsubj	11
obl	nsubj	10
nmod	flat	10
flat	nmod	10
advcl	acl	8
conj	cop	8
parataxis	root	8
appos	conj	8

## Top DEPREL mistakes where Trankit aligned loses to CLASSLA aligned
gold_deprel	pred_deprel	count
nmod	obl	26
obl	nmod	19
iobj	obj	14
nmod	flat	14
parataxis	conj	8
nsubj	obj	7
root	parataxis	7
orphan	advmod	6
nsubj	root	6
nmod	appos	6
appos	nmod	6
advcl	acl	5
advmod	cc	5
obj	iobj	5
parataxis	root	5
advmod	mark	4
root	nsubj	4
conj	flat	4
acl	advcl	3
obj	nsubj	3
