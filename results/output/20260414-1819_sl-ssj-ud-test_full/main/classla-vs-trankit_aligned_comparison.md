# CLASSLA aligned vs Trankit aligned (exact difference report)

## Coverage
- Gold sentences: 1282
- CLASSLA aligned predicted sentences: 1282
- Trankit aligned predicted sentences: 1282
- Gold sentences paired with both models: 1282
- Unmatched gold for CLASSLA aligned: 0
- Unmatched gold for Trankit aligned: 0
- Unmatched predicted for CLASSLA aligned: 0
- Unmatched predicted for Trankit aligned: 0
- Skipped sentence pairs (token count mismatch): 0
- Compared tokens (FORM-aligned): 25442
- Skipped tokens (FORM mismatch): 0

## LAS exact differences
- CLASSLA aligned correct, Trankit aligned wrong: 478 (1.88%)
- Trankit aligned correct, CLASSLA aligned wrong: 1523 (5.99%)
- Both correct: 22543 (88.61%)
- Both wrong: 898 (3.53%)

## UAS exact differences
- CLASSLA aligned correct, Trankit aligned wrong: 379 (1.49%)
- Trankit aligned correct, CLASSLA aligned wrong: 1314 (5.16%)
- Both correct: 23058 (90.63%)
- Both wrong: 691 (2.72%)

## DEPREL exact differences
- CLASSLA aligned correct, Trankit aligned wrong: 294 (1.16%)
- Trankit aligned correct, CLASSLA aligned wrong: 803 (3.16%)
- Both correct: 23929 (94.05%)
- Both wrong: 416 (1.64%)

## Top LAS mistakes where CLASSLA aligned wins
gold_deprel	pred_deprel	count
punct	punct	61
conj	conj	34
advmod	advmod	28
nmod	obl	24
nmod	nmod	23
obl	nmod	17
obl	obl	15
iobj	obj	13
nsubj	obj	11
parataxis	parataxis	11
nmod	flat	9
advcl	advcl	8
appos	appos	8
nsubj	nsubj	7
acl	acl	7
root	parataxis	5
cc	cc	5
parataxis	conj	5
parataxis	root	5
nsubj	root	4

## Top LAS mistakes where Trankit aligned wins
gold_deprel	pred_deprel	count
punct	punct	218
advmod	advmod	89
conj	conj	66
obl	nmod	65
nmod	nmod	56
obl	obl	53
nmod	obl	47
acl	acl	36
cc	cc	30
aux	aux	29
nsubj	obj	27
obj	nsubj	24
parataxis	parataxis	24
mark	mark	24
nsubj	nsubj	23
root	cop	22
nsubj	root	19
cop	cop	19
obj	iobj	18
csubj	csubj	17

## Top DEPREL mistakes where CLASSLA aligned wins
gold_deprel	pred_deprel	count
nmod	obl	28
obl	nmod	19
nmod	flat	14
iobj	obj	13
nsubj	obj	11
parataxis	root	7
nsubj	root	6
root	parataxis	5
appos	nmod	5
parataxis	conj	5
advcl	acl	4
advmod	cc	4
obj	iobj	4
root	nsubj	4
advmod	mark	4
nmod	appos	4
conj	parataxis	4
obj	nsubj	4
cop	conj	3
acl	advcl	3

## Top DEPREL mistakes where Trankit aligned wins
gold_deprel	pred_deprel	count
obl	nmod	65
nmod	obl	50
nsubj	obj	27
obj	nsubj	25
root	cop	22
obj	iobj	19
nsubj	root	19
cop	root	14
cc	advmod	14
conj	parataxis	12
root	parataxis	12
nsubj	conj	11
root	nsubj	11
parataxis	root	10
flat	nmod	10
obl	nsubj	9
advmod	nsubj	8
advcl	acl	8
nsubj	nmod	8
conj	cop	8
