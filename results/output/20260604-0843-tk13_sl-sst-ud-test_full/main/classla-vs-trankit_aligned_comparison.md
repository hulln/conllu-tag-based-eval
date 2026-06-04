# Trankit aligned vs CLASSLA aligned (exact difference report)

## Coverage
- Gold sentences: 432
- Trankit aligned predicted sentences: 432
- CLASSLA aligned predicted sentences: 432
- Gold sentences paired with both models: 432
- Unmatched gold for Trankit aligned: 0
- Unmatched gold for CLASSLA aligned: 0
- Unmatched predicted for Trankit aligned: 0
- Unmatched predicted for CLASSLA aligned: 0
- Skipped sentence pairs (token count mismatch): 0
- Compared tokens (FORM-aligned): 11443
- Skipped tokens (FORM mismatch): 0

## LAS exact differences
- Trankit aligned correct, CLASSLA aligned wrong: 2310 (20.19%)
- Trankit aligned wrong, CLASSLA aligned correct: 322 (2.81%)
- Both correct: 7629 (66.67%)
- Both wrong: 1182 (10.33%)

## UAS exact differences
- Trankit aligned correct, CLASSLA aligned wrong: 1963 (17.15%)
- Trankit aligned wrong, CLASSLA aligned correct: 320 (2.80%)
- Both correct: 8244 (72.04%)
- Both wrong: 916 (8.00%)

## DEPREL exact differences
- Trankit aligned correct, CLASSLA aligned wrong: 1527 (13.34%)
- Trankit aligned wrong, CLASSLA aligned correct: 165 (1.44%)
- Both correct: 9271 (81.02%)
- Both wrong: 480 (4.19%)

## Top LAS mistakes where Trankit aligned wins
gold_deprel	pred_deprel	count
punct	punct	546
advmod	advmod	110
discourse	conj	99
discourse	parataxis	83
discourse	appos	72
discourse	nsubj	63
cc	cc	54
discourse	nmod	53
conj	conj	43
discourse	vocative	41
parataxis	parataxis	35
mark	mark	28
obl	nmod	23
case	case	23
discourse	discourse	21
obl	obl	21
nsubj	nsubj	18
nsubj	conj	17
cc	advmod	17
nsubj	parataxis	17

## Top LAS mistakes where Trankit aligned loses to CLASSLA aligned
gold_deprel	pred_deprel	count
punct	punct	93
advmod	advmod	24
conj	conj	21
parataxis	parataxis	10
obl	obl	9
nmod	obl	9
parataxis	conj	7
mark	mark	7
cc	cc	6
cop	parataxis	6
discourse	discourse	5
root	parataxis	5
nmod	nmod	5
advmod	cc	4
nsubj	nsubj	4
obj	nsubj	4
parataxis	nsubj	4
nsubj	obj	3
obj	obj	3
obj	reparandum	3

## Top DEPREL mistakes where Trankit aligned wins
gold_deprel	pred_deprel	count
discourse	conj	137
discourse	parataxis	98
discourse	appos	85
discourse	nmod	68
discourse	nsubj	65
discourse	vocative	45
obl	nmod	23
conj	parataxis	23
cc	advmod	19
reparandum	case	19
discourse	advmod	18
nsubj	conj	17
nsubj	parataxis	17
parataxis	conj	16
advmod	orphan	16
nmod	conj	16
root	parataxis	15
discourse	cc	15
root	cop	15
fixed	advmod	15

## Top DEPREL mistakes where Trankit aligned loses to CLASSLA aligned
gold_deprel	pred_deprel	count
parataxis	conj	11
nmod	obl	9
cop	parataxis	7
parataxis	nsubj	6
root	parataxis	5
obj	nsubj	5
nsubj	obj	4
conj	parataxis	4
advmod	cc	4
advmod	discourse	4
parataxis	acl	4
advcl	acl	3
obj	reparandum	3
discourse	cc	3
obl	nmod	3
obj	iobj	3
conj	appos	3
parataxis	root	3
conj	amod	3
nummod	det	3
